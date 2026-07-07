"""Seasonality analysis of gold monthly returns.

Two questions:
  1. Gregorian seasonality  - is any calendar month systematically strong/weak?
  2. The 'Muharram effect'   - do gold prices tend to fall during Muharram and
     recover afterwards, as is commonly claimed in South Asia?

We use monthly LOG RETURNS (not price levels) so the test is about direction and
magnitude of moves, controlled for the long-run uptrend. Significance is checked
with a simple t-test of each group's mean return vs zero, plus a bootstrap of the
Muharram-minus-rest difference so we are not fooled by a small sample.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from gutils import load_gold, HIJRI_MONTHS


def summarise_groups(df: pd.DataFrame, key: str, labels: dict) -> pd.DataFrame:
    out = []
    for k in sorted(df[key].dropna().unique()):
        r = df.loc[df[key] == k, "ret"].dropna()
        mean = r.mean()
        # t-test of mean monthly return vs 0
        t, p = stats.ttest_1samp(r, 0.0) if len(r) > 2 else (np.nan, np.nan)
        out.append({
            "key": int(k),
            "label": labels.get(int(k), str(k)),
            "n": len(r),
            "mean_ret_%": 100 * mean,
            "share_positive_%": 100 * (r > 0).mean(),
            "t_stat": t,
            "p_value": p,
        })
    return pd.DataFrame(out)


def bootstrap_diff(group_ret: np.ndarray, other_ret: np.ndarray, n: int = 20000) -> tuple:
    """Bootstrap the difference in mean return (group - other). Returns
    (observed_diff_%, p_two_sided) using a label-permutation style resample."""
    rng = np.random.default_rng(42)
    obs = group_ret.mean() - other_ret.mean()
    pooled = np.concatenate([group_ret, other_ret])
    ng = len(group_ret)
    diffs = np.empty(n)
    for i in range(n):
        perm = rng.permutation(pooled)
        diffs[i] = perm[:ng].mean() - perm[ng:].mean()
    p = np.mean(np.abs(diffs) >= abs(obs))
    return 100 * obs, p


def main():
    df = load_gold()
    print("=" * 70)
    print("GOLD SEASONALITY ANALYSIS  (monthly log returns, 1968-2026)")
    print("=" * 70)

    print("\n--- Gregorian calendar month ---")
    greg = summarise_groups(df, "greg_month",
                            {i: pd.Timestamp(2000, i, 1).strftime("%b") for i in range(1, 13)})
    print(greg.to_string(index=False, float_format=lambda x: f"{x:7.3f}"))

    print("\n--- Islamic (Hijri) month ---")
    hij = summarise_groups(df, "hijri_month", HIJRI_MONTHS)
    print(hij.to_string(index=False, float_format=lambda x: f"{x:7.3f}"))

    # ---- The Muharram claim, tested directly -------------------------------
    print("\n" + "=" * 70)
    print("TESTING THE 'MUHARRAM' CLAIM")
    print("=" * 70)
    muh = df.loc[df["hijri_month"] == 1, "ret"].dropna().values
    rest = df.loc[df["hijri_month"] != 1, "ret"].dropna().values
    obs_diff, p_boot = bootstrap_diff(muh, rest)
    print(f"Muharram  : n={len(muh):3d}  mean monthly return = {100*muh.mean():+.3f}%  "
          f"share positive = {100*(muh>0).mean():.0f}%")
    print(f"All others: n={len(rest):3d}  mean monthly return = {100*rest.mean():+.3f}%  "
          f"share positive = {100*(rest>0).mean():.0f}%")
    print(f"Difference (Muharram - rest): {obs_diff:+.3f}% per month")
    print(f"Bootstrap two-sided p-value : {p_boot:.3f}")

    # Does it 'recover afterwards'? Compare Muharram vs Safar (the next month).
    saf = df.loc[df["hijri_month"] == 2, "ret"].dropna().values
    print(f"\nSafar (month after Muharram): mean monthly return = {100*saf.mean():+.3f}%")

    verdict = ("SUPPORTED" if (muh.mean() < 0 and p_boot < 0.10)
               else "NOT statistically supported")
    print(f"\nVERDICT: The 'gold falls in Muharram' claim is {verdict} in this data.")

    # Persist for the report
    greg.to_csv("reports/seasonality_gregorian.csv", index=False)
    hij.to_csv("reports/seasonality_hijri.csv", index=False)
    with open("reports/muharram_test.txt", "w") as f:
        f.write(f"Muharram mean monthly return: {100*muh.mean():+.3f}% (n={len(muh)})\n")
        f.write(f"Other months mean return    : {100*rest.mean():+.3f}% (n={len(rest)})\n")
        f.write(f"Difference                  : {obs_diff:+.3f}% per month\n")
        f.write(f"Bootstrap p-value           : {p_boot:.3f}\n")
        f.write(f"Verdict                     : {verdict}\n")


if __name__ == "__main__":
    main()
