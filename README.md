# Gold Price Forecasting

Machine-learning / deep-learning analysis of gold (XAU/USD) using 58 years of real
monthly price history (1968–2026), built to answer one practical question:
**is gold a good lump-sum investment at today's price (~$4,150/oz, July 2026)?**

👉 **Read [`REPORT.md`](REPORT.md) for the full findings and the investment assessment.**

## What's inside

| File | What it does |
|---|---|
| `data/gold_monthly_usd.csv` | Monthly LBMA/London gold price, USD/oz, 1968–2026 |
| `src/gutils.py` | Data loading + Hijri-calendar features |
| `src/analyze_seasonality.py` | Tests the "gold falls in Muharram" belief |
| `src/train_models.py` | Walk-forward backtest: Random Walk, SARIMA, Gradient Boosting, LSTM |
| `src/make_forecast.py` | Monte-Carlo 1/2/3/4/5/10-year probabilistic forecasts |
| `src/dca_vs_lumpsum.py` | Lump-sum vs dollar-cost-averaging entry strategies |
| `src/make_figures.py` | Charts → `reports/figures/` |
| `run_all.py` | Runs the whole pipeline |

## Run it

```bash
pip install -r requirements.txt
python3 run_all.py
```

## Key results (see REPORT.md for detail & caveats)

- **Muharram effect: not statistically supported** (p=0.68). January is the one real seasonal.
- **Gradient Boosting beats a random walk** at 1-month timing (70% directional). The
  **LSTM neural net does not** — deep learning isn't magic on short, noisy data.
- **No model can reliably predict multi-year prices** → forecasts are given as probability
  fans, not lines.
- Gold is **~43% above its 3-year trend** after a +73%/2-yr run and is already correcting
  from an all-time high — a **risky entry for a lump sum.**

> ⚠️ Data analysis, **not financial advice.** Consult a licensed advisor before investing
> retirement money.
