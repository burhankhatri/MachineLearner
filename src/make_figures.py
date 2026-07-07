"""Generate report figures (saved to reports/figures/)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from gutils import load_gold
from make_forecast import (CURRENT_SPOT, HORIZONS, N_PATHS,
                           block_bootstrap_paths, gbm_paths)

plt.rcParams.update({"figure.dpi": 120, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.25})
GOLD = "#C8A227"
FIG = "reports/figures"


def fig_history(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(df.index, df["price"], color=GOLD, lw=1.4)
    ax.axhline(CURRENT_SPOT, color="crimson", ls="--", lw=1, alpha=0.7,
               label=f"Spot ~${CURRENT_SPOT:,.0f} (Jul 2026)")
    ma36 = df["price"].rolling(36).mean()
    ax.semilogy(df.index, ma36, color="steelblue", lw=1, alpha=0.7, label="36-month avg")
    ax.set_title("Gold price, USD/oz (log scale), free-floating era 1968-2026")
    ax.set_ylabel("USD / oz (log)")
    ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/01_history.png"); plt.close(fig)


def fig_seasonality():
    greg = pd.read_csv("reports/seasonality_gregorian.csv")
    hij = pd.read_csv("reports/seasonality_hijri.csv")
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    c1 = ["crimson" if v < 0 else GOLD for v in greg["mean_ret_%"]]
    axes[0].bar(greg["label"], greg["mean_ret_%"], color=c1)
    axes[0].set_title("Avg monthly return by Gregorian month")
    axes[0].axhline(0, color="k", lw=0.6); axes[0].tick_params(axis="x", rotation=45)
    c2 = ["crimson" if l == "Muharram" else ("steelblue" if v < 0 else GOLD)
          for l, v in zip(hij["label"], hij["mean_ret_%"])]
    axes[1].bar(hij["label"], hij["mean_ret_%"], color=c2)
    axes[1].set_title("Avg monthly return by Islamic month (Muharram in red)")
    axes[1].axhline(0, color="k", lw=0.6); axes[1].tick_params(axis="x", rotation=75)
    fig.tight_layout(); fig.savefig(f"{FIG}/02_seasonality.png"); plt.close(fig)


def fig_backtest():
    sc = pd.read_csv("reports/backtest_scores.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].bar(sc["model"], sc["approx_%_err"], color=GOLD)
    axes[0].set_title("1-month backtest error (%)  -- lower better")
    axes[1].bar(sc["model"], sc["dir_acc_%"], color="steelblue")
    axes[1].axhline(50, color="crimson", ls="--", lw=1, label="coin flip")
    axes[1].set_title("Directional accuracy (%)  -- higher better")
    axes[1].legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/03_backtest.png"); plt.close(fig)


def fig_fan(df):
    rets = df["ret"].dropna().values
    fig, ax = plt.subplots(figsize=(10, 5.5))
    months = 10 * 12
    paths = block_bootstrap_paths(rets, months, N_PATHS)
    t = np.arange(1, months + 1) / 12
    for lo, hi, a in [(10, 90, 0.15), (25, 75, 0.22)]:
        ax.fill_between(t, np.percentile(paths, lo, axis=0),
                        np.percentile(paths, hi, axis=0), color=GOLD, alpha=a,
                        label=f"P{lo}-P{hi}")
    ax.plot(t, np.percentile(paths, 50, axis=0), color="black", lw=1.6, label="median")
    ax.axhline(CURRENT_SPOT, color="crimson", ls="--", lw=1, label="today")
    ax.set_title("Gold forecast fan, block-bootstrap Monte Carlo (10,000 paths)")
    ax.set_xlabel("years from now"); ax.set_ylabel("USD / oz"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/04_forecast_fan.png"); plt.close(fig)


def fig_scenarios():
    sc = pd.read_csv("reports/forecast_scenarios.csv")
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, g in sc.groupby("scenario"):
        ax.plot(g["horizon_y"], g["P50"], marker="o", label=name.split("(")[0].strip())
    ax.axhline(CURRENT_SPOT, color="crimson", ls="--", lw=1, label="today")
    ax.set_title("Median gold price by scenario")
    ax.set_xlabel("years from now"); ax.set_ylabel("USD / oz"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{FIG}/05_scenarios.png"); plt.close(fig)


def main():
    df = load_gold()
    fig_history(df)
    fig_seasonality()
    fig_backtest()
    fig_fan(df)
    fig_scenarios()
    print("Figures written to reports/figures/")


if __name__ == "__main__":
    main()
