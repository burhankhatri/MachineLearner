"""Lump-sum-now vs dollar-cost-averaging (DCA), simulated on real gold history.

The practical question for a retiree with a one-off sum is NOT only 'will gold go
up' but 'how do I enter?'. We test, across every historical starting month, what
would have happened if you had:
  - put 100% in on day one (lump sum), vs
  - spread the buy evenly over 12 or 24 months (DCA).
We report the distribution of the value after 5 years for each, and how often DCA
beat / lost to lump sum. This isolates timing risk, which is what matters when you
are buying after a big run-up.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from gutils import load_gold

HORIZON_M = 60  # evaluate 5 years out


def simulate():
    df = load_gold()
    price = df["price"].values
    n = len(price)
    res = {"lump": [], "dca12": [], "dca24": []}
    for start in range(0, n - HORIZON_M - 24):
        end_price = price[start + HORIZON_M]
        # lump sum: buy all at start
        oz_lump = 1.0 / price[start]
        res["lump"].append(oz_lump * end_price)
        # DCA over 12 / 24 months: invest 1/k each month
        for k, key in ((12, "dca12"), (24, "dca24")):
            oz = sum((1.0 / k) / price[start + m] for m in range(k))
            res[key].append(oz * end_price)
    return {k: np.array(v) for k, v in res.items()}


def main():
    r = simulate()
    print("=" * 66)
    print("LUMP SUM vs DOLLAR-COST AVERAGING  (value of $1 after 5 years)")
    print("Across all historical start months, 1968-2021")
    print("=" * 66)
    print(f"{'strategy':>8} {'median':>8} {'P10':>8} {'P90':>8} {'P(<$1)':>8}")
    for key, label in (("lump", "Lump"), ("dca12", "DCA 12m"), ("dca24", "DCA 24m")):
        v = r[key]
        print(f"{label:>8} {np.median(v):>8.2f} {np.percentile(v,10):>8.2f}"
              f" {np.percentile(v,90):>8.2f} {100*np.mean(v<1):>7.0f}%")

    beat12 = 100 * np.mean(r["dca12"] > r["lump"])
    print(f"\nDCA-12m produced a HIGHER 5y value than lump sum in {beat12:.0f}% of start months.")
    print("Interpretation: DCA usually gives up a little upside (gold trends up), but")
    print("it materially cuts the worst-case timing loss -- the relevant risk when")
    print("deploying retirement money right after a parabolic rally.")

    pd.DataFrame({
        "strategy": ["lump", "dca12", "dca24"],
        "median": [np.median(r[k]) for k in ("lump", "dca12", "dca24")],
        "p10": [np.percentile(r[k], 10) for k in ("lump", "dca12", "dca24")],
        "p90": [np.percentile(r[k], 90) for k in ("lump", "dca12", "dca24")],
        "prob_loss_%": [100*np.mean(r[k] < 1) for k in ("lump", "dca12", "dca24")],
    }).to_csv("reports/dca_vs_lumpsum.csv", index=False)


if __name__ == "__main__":
    main()
