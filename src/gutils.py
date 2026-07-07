"""Shared utilities for the gold forecasting project.

Loads the monthly gold series, restricts to the free-floating era, and attaches
calendar features (including the Islamic/Hijri month) used across the analysis.
"""
from __future__ import annotations

import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "gold_monthly_usd.csv")

# Gold traded at an administered/pegged price before the London Gold Pool
# collapsed (Mar 1968) and the US closed the gold window (Aug 1971). Prices
# before the free-floating era are not market prices, so we model from 1968.
FREE_FLOAT_START = "1968-01"

HIJRI_MONTHS = {
    1: "Muharram", 2: "Safar", 3: "Rabi al-Awwal", 4: "Rabi al-Thani",
    5: "Jumada al-Awwal", 6: "Jumada al-Thani", 7: "Rajab", 8: "Shaban",
    9: "Ramadan", 10: "Shawwal", 11: "Dhu al-Qadah", 12: "Dhu al-Hijjah",
}


def hijri_month_of(ts: pd.Timestamp) -> int:
    """Return the Hijri month number for the 15th of the given month."""
    from hijridate import Gregorian
    h = Gregorian(ts.year, ts.month, 15).to_hijri()
    return h.month


def load_gold(free_float_only: bool = True) -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["Date"] + "-01")
    df = df.rename(columns={"Price": "price"})[["date", "price"]].sort_values("date")
    df = df.set_index("date")
    if free_float_only:
        df = df.loc[FREE_FLOAT_START:]
    df["log_price"] = np.log(df["price"])
    df["ret"] = df["log_price"].diff()          # monthly log return
    df["greg_month"] = df.index.month
    df["hijri_month"] = [hijri_month_of(ts) for ts in df.index]
    df["hijri_name"] = df["hijri_month"].map(HIJRI_MONTHS)
    return df


def cagr(start_price: float, end_price: float, years: float) -> float:
    return (end_price / start_price) ** (1.0 / years) - 1.0


if __name__ == "__main__":
    g = load_gold()
    print(f"Rows: {len(g)}  Range: {g.index.min():%Y-%m} .. {g.index.max():%Y-%m}")
    print(g.tail(8)[["price", "ret", "hijri_name"]])
