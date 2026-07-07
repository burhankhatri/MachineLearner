"""Long-horizon forecast for gold, done HONESTLY.

A single price line 10 years out is fantasy. What actually helps a decision is the
DISTRIBUTION of outcomes. We generate it two ways and cross-check:

  A) Block-bootstrap Monte Carlo -- resample real historical 12-month blocks of
     monthly returns (preserves fat tails, momentum and crashes) and compound
     forward from today's price. 10,000 paths.

  B) Scenario drift Monte Carlo   -- geometric Brownian motion under explicit
     bear / base / bull annual drift assumptions, so the reader can see how the
     answer depends on the assumption rather than trusting a black box.

We also quantify how STRETCHED gold is right now (distance above trend), because
buying after a parabolic move is the single biggest risk to a lump-sum purchase.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from gutils import load_gold, cagr

CURRENT_SPOT = 4150.0   # XAU/USD spot, ~7 Jul 2026 (from live quote, see README)
HORIZONS = [1, 2, 3, 4, 5, 10]
N_PATHS = 10000
RNG = np.random.default_rng(2026)


def valuation_stretch(df: pd.DataFrame) -> dict:
    lp = df["log_price"]
    ma12 = lp.rolling(12).mean().iloc[-1]
    ma36 = lp.rolling(36).mean().iloc[-1]
    now = np.log(CURRENT_SPOT)
    ret_12m = CURRENT_SPOT / df["price"].iloc[-12] - 1
    ret_24m = CURRENT_SPOT / df["price"].iloc[-24] - 1
    # z-score of the trailing 12m return vs history of 12m returns
    r12_hist = (df["price"] / df["price"].shift(12) - 1).dropna()
    z = (ret_12m - r12_hist.mean()) / r12_hist.std()
    return {
        "spot": CURRENT_SPOT,
        "pct_above_ma12": 100 * (np.exp(now - ma12) - 1),
        "pct_above_ma36": 100 * (np.exp(now - ma36) - 1),
        "ret_12m_%": 100 * ret_12m,
        "ret_24m_%": 100 * ret_24m,
        "ret_12m_zscore": z,
        "pctile_of_12m_ret": 100 * (r12_hist < ret_12m).mean(),
    }


def block_bootstrap_paths(rets: np.ndarray, months: int, n: int, block: int = 12):
    """Compound n paths of `months` returns by stitching random historical blocks."""
    paths = np.empty((n, months))
    L = len(rets)
    for i in range(n):
        seq = []
        while len(seq) < months:
            s = RNG.integers(0, L - block)
            seq.extend(rets[s:s + block])
        paths[i] = seq[:months]
    return CURRENT_SPOT * np.exp(np.cumsum(paths, axis=1))


def gbm_paths(annual_drift: float, annual_vol: float, months: int, n: int):
    mu_m = annual_drift / 12 - 0.5 * (annual_vol ** 2) / 12
    sd_m = annual_vol / np.sqrt(12)
    shocks = RNG.normal(mu_m, sd_m, size=(n, months))
    return CURRENT_SPOT * np.exp(np.cumsum(shocks, axis=1))


def summarise(paths: np.ndarray, months: int) -> dict:
    end = paths[:, months - 1]
    yrs = months / 12
    return {
        "P10": np.percentile(end, 10),
        "P25": np.percentile(end, 25),
        "P50": np.percentile(end, 50),
        "P75": np.percentile(end, 75),
        "P90": np.percentile(end, 90),
        "prob_below_today_%": 100 * (end < CURRENT_SPOT).mean(),
        "median_CAGR_%": 100 * cagr(CURRENT_SPOT, np.percentile(end, 50), yrs),
    }


def main():
    df = load_gold()
    rets = df["ret"].dropna().values
    ann_vol = rets.std() * np.sqrt(12)

    print("=" * 72)
    print("HOW STRETCHED IS GOLD RIGHT NOW?  (context for a lump-sum buy)")
    print("=" * 72)
    vs = valuation_stretch(df)
    for k, v in vs.items():
        print(f"  {k:22s}: {v:10.2f}")
    print(f"\n  Annualised volatility of gold (1968-2026): {100*ann_vol:.1f}%")

    # -- A) block bootstrap ------------------------------------------------
    print("\n" + "=" * 72)
    print("A) BLOCK-BOOTSTRAP MONTE CARLO  (resamples real gold history)")
    print("=" * 72)
    print(f"{'Horizon':>8} {'P10':>9} {'P25':>9} {'MEDIAN':>9} {'P75':>9} {'P90':>9}"
          f" {'P(loss)':>9} {'med CAGR':>9}")
    boot_rows = {}
    for h in HORIZONS:
        p = block_bootstrap_paths(rets, h * 12, N_PATHS)
        s = summarise(p, h * 12)
        boot_rows[h] = s
        print(f"{h:>6}y  {s['P10']:>9.0f} {s['P25']:>9.0f} {s['P50']:>9.0f}"
              f" {s['P75']:>9.0f} {s['P90']:>9.0f} {s['prob_below_today_%']:>8.0f}%"
              f" {s['median_CAGR_%']:>8.1f}%")

    # -- B) scenario drift -------------------------------------------------
    print("\n" + "=" * 72)
    print("B) SCENARIO-DRIFT MONTE CARLO  (you choose the assumption)")
    print("=" * 72)
    scenarios = {
        "Bear  (-4%/yr, mean-reverts)": -0.04,
        "Base  (+3%/yr ~ inflation)": 0.03,
        "Bull  (+8%/yr momentum holds)": 0.08,
    }
    scen_out = {}
    for name, drift in scenarios.items():
        print(f"\n  {name}   [vol={100*ann_vol:.0f}%]")
        print(f"    {'Horizon':>8} {'P10':>9} {'MEDIAN':>9} {'P90':>9} {'P(loss)':>9}")
        scen_out[name] = {}
        for h in HORIZONS:
            p = gbm_paths(drift, ann_vol, h * 12, N_PATHS)
            s = summarise(p, h * 12)
            scen_out[name][h] = s
            print(f"    {h:>6}y  {s['P10']:>9.0f} {s['P50']:>9.0f} {s['P90']:>9.0f}"
                  f" {s['prob_below_today_%']:>8.0f}%")

    # persist
    pd.DataFrame(boot_rows).T.to_csv("reports/forecast_bootstrap.csv")
    rows = []
    for name, d in scen_out.items():
        for h, s in d.items():
            rows.append({"scenario": name, "horizon_y": h, **s})
    pd.DataFrame(rows).to_csv("reports/forecast_scenarios.csv", index=False)
    pd.Series(vs).to_csv("reports/valuation_stretch.csv")
    print("\nSaved forecast CSVs to reports/")


if __name__ == "__main__":
    main()
