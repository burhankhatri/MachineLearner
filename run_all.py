"""Run the full gold forecasting pipeline end to end.

    python3 run_all.py

Reproduces every number and figure in REPORT.md from data/gold_monthly_usd.csv.
"""
import subprocess, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs("reports/figures", exist_ok=True)

STEPS = [
    ("Seasonality / Muharram analysis", "src/analyze_seasonality.py"),
    ("Model backtest (RW, SARIMA, GBM, LSTM)", "src/train_models.py"),
    ("Multi-horizon Monte-Carlo forecast", "src/make_forecast.py"),
    ("Lump-sum vs dollar-cost-averaging", "src/dca_vs_lumpsum.py"),
    ("Figures", "src/make_figures.py"),
]

for title, script in STEPS:
    print(f"\n{'#'*72}\n# {title}\n{'#'*72}")
    r = subprocess.run([sys.executable, script])
    if r.returncode != 0:
        sys.exit(f"Step failed: {script}")
print("\nAll steps complete. See REPORT.md and reports/.")
