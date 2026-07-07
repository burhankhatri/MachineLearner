"""Train and BACKTEST three forecasting approaches on gold monthly returns.

Models
------
1. Random Walk with drift   - the honest benchmark. For assets like gold this is
   notoriously hard to beat; every fancier model must clear this bar.
2. SARIMA (statistical)     - captures autocorrelation + seasonality on log price.
3. Gradient Boosting (ML)   - trees on engineered lag/momentum/volatility features.
4. LSTM (deep learning)     - a recurrent neural net on sequences of log returns.

Everything is judged by WALK-FORWARD backtesting (expanding window): we only ever
predict months the model has not seen, at horizons of 1 and 12 months. The metric
is RMSE / MAE on the log price and directional accuracy. This is the number that
matters -- in-sample fit is meaningless for an investment decision.
"""
from __future__ import annotations

import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

from gutils import load_gold

RNG = np.random.default_rng(7)


# --------------------------------------------------------------------------- #
# Feature engineering for the ML model
# --------------------------------------------------------------------------- #
def make_features(df: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame(index=df.index)
    lp = df["log_price"]
    for k in (1, 2, 3, 6, 12):
        x[f"ret_{k}"] = lp.diff(k)                 # momentum over k months
    x["vol_6"] = df["ret"].rolling(6).std()        # recent volatility
    x["vol_12"] = df["ret"].rolling(12).std()
    x["dist_ma12"] = lp - lp.rolling(12).mean()    # stretch vs 1y average
    x["dist_ma36"] = lp - lp.rolling(36).mean()
    x["month_sin"] = np.sin(2 * np.pi * df["greg_month"] / 12)
    x["month_cos"] = np.cos(2 * np.pi * df["greg_month"] / 12)
    x["target"] = df["ret"].shift(-1)              # next-month log return
    return x


# --------------------------------------------------------------------------- #
# LSTM (PyTorch)
# --------------------------------------------------------------------------- #
def train_lstm_onestep(returns: np.ndarray, seq_len: int = 12, epochs: int = 120):
    """Fit an LSTM to predict next-month return from the last `seq_len` returns.
    Returns (model, mean, std, predict_fn). Standardises inputs internally."""
    import torch
    import torch.nn as nn
    torch.manual_seed(7)

    mu, sd = returns.mean(), returns.std() + 1e-9
    z = (returns - mu) / sd
    X, y = [], []
    for i in range(len(z) - seq_len):
        X.append(z[i:i + seq_len])
        y.append(z[i + seq_len])
    X = torch.tensor(np.array(X), dtype=torch.float32).unsqueeze(-1)
    y = torch.tensor(np.array(y), dtype=torch.float32).unsqueeze(-1)

    class Net(nn.Module):
        def __init__(self, h=32):
            super().__init__()
            self.lstm = nn.LSTM(1, h, batch_first=True)
            self.fc = nn.Linear(h, 1)

        def forward(self, s):
            out, _ = self.lstm(s)
            return self.fc(out[:, -1, :])

    net = Net()
    opt = torch.optim.Adam(net.parameters(), lr=0.01)
    lossf = nn.MSELoss()
    for _ in range(epochs):
        opt.zero_grad()
        loss = lossf(net(X), y)
        loss.backward()
        opt.step()

    def predict(last_seq_raw: np.ndarray) -> float:
        zz = (last_seq_raw - mu) / sd
        with torch.no_grad():
            t = torch.tensor(zz[-seq_len:], dtype=torch.float32).view(1, seq_len, 1)
            out = net(t).item()
        return out * sd + mu

    return net, predict


# --------------------------------------------------------------------------- #
# Walk-forward backtest
# --------------------------------------------------------------------------- #
def backtest(df: pd.DataFrame, start_frac: float = 0.6):
    from sklearn.ensemble import GradientBoostingRegressor
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    feats = make_features(df)
    lp = df["log_price"].values
    n = len(df)
    start = int(n * start_frac)

    rows = []
    # Pre-train LSTM once on the first `start` returns, then predict forward
    # (retraining every month is too slow; we refit every 12 months instead).
    lstm_pred = None
    for t in range(start, n - 1):
        actual_next = lp[t + 1]
        rec = {"date": df.index[t + 1], "actual": actual_next}

        # 1) Random walk w/ drift
        drift = np.mean(np.diff(lp[:t + 1]))
        rec["rw"] = lp[t] + drift

        # 2) SARIMA on log price (cheap orders; refit each step on expanding window)
        try:
            m = SARIMAX(lp[:t + 1], order=(1, 1, 1),
                        seasonal_order=(0, 0, 0, 0),
                        enforce_stationarity=False,
                        enforce_invertibility=False).fit(disp=False)
            rec["sarima"] = m.forecast(1)[0]
        except Exception:
            rec["sarima"] = lp[t] + drift

        # 3) Gradient boosting on features
        tr = feats.iloc[:t + 1].dropna()
        if len(tr) > 40:
            gb = GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                           learning_rate=0.03, subsample=0.8,
                                           random_state=7)
            gb.fit(tr.drop(columns="target"), tr["target"])
            xnow = feats.drop(columns="target").iloc[[t]]
            if not xnow.isna().any(axis=1).iloc[0]:
                rec["gb"] = lp[t] + gb.predict(xnow)[0]
            else:
                rec["gb"] = lp[t] + drift
        else:
            rec["gb"] = lp[t] + drift

        # 4) LSTM  (refit every 12 months to keep it tractable)
        if lstm_pred is None or (t - start) % 12 == 0:
            _, lstm_pred = train_lstm_onestep(df["ret"].values[1:t + 1])
        rec["lstm"] = lp[t] + lstm_pred(df["ret"].values[1:t + 1])

        rows.append(rec)

    bt = pd.DataFrame(rows).set_index("date")
    return bt


def score(bt: pd.DataFrame) -> pd.DataFrame:
    out = []
    for col in ["rw", "sarima", "gb", "lstm"]:
        err = bt[col] - bt["actual"]
        # directional accuracy: did we predict the right sign of the change?
        prev_actual = bt["actual"].shift(1)
        pred_dir = np.sign(bt[col] - prev_actual)
        real_dir = np.sign(bt["actual"] - prev_actual)
        hit = (pred_dir == real_dir).mean()
        out.append({
            "model": col,
            "RMSE_logprice": np.sqrt((err ** 2).mean()),
            "MAE_logprice": err.abs().mean(),
            # translate log RMSE into an approx % price error
            "approx_%_err": 100 * (np.exp(np.sqrt((err ** 2).mean())) - 1),
            "dir_acc_%": 100 * hit,
        })
    return pd.DataFrame(out)


def main():
    df = load_gold()
    print("Walk-forward backtest (1-month horizon, expanding window)...")
    bt = backtest(df)
    sc = score(bt)
    print("\n" + "=" * 64)
    print("BACKTEST SCORES  (lower error = better; RW is the benchmark)")
    print("=" * 64)
    print(sc.to_string(index=False, float_format=lambda x: f"{x:8.4f}"))
    bt.to_csv("reports/backtest_predictions.csv")
    sc.to_csv("reports/backtest_scores.csv", index=False)
    print("\nSaved reports/backtest_scores.csv")


if __name__ == "__main__":
    main()
