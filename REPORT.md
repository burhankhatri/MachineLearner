# Gold Price Forecasting — Full Analysis & Investment Assessment

*Generated 7 July 2026. Data: monthly London/LBMA gold fixing, USD/oz, 1968–June 2026.
Current spot at time of writing: ~$4,150/oz (XAU/USD, 7 Jul 2026).*

> **This is a data analysis, not financial advice.** Nobody — no bank, no fund, no
> neural network — can reliably predict the price of gold years into the future. The
> value of this report is that it quantifies the *uncertainty* honestly, so a decision
> about real retirement money is made with eyes open. Please read the "Bottom line"
> section, and consider a licensed financial advisor before committing a lump sum.

---

## 1. What was actually built

A reproducible pipeline (`python3 run_all.py`) that:

1. Loads 58 years of real monthly gold prices (the free-floating era; pre-1968 gold
   was price-*fixed* under the gold standard / Bretton Woods, so it is **not** a market
   price and would corrupt any model — it is excluded from modelling).
2. Tests the **Muharram seasonality** belief statistically.
3. Trains and **honestly backtests** four forecasting approaches (walk-forward, out-of-sample):
   a random-walk benchmark, a SARIMA statistical model, a Gradient-Boosting ML model,
   and an **LSTM deep-learning neural network**.
4. Produces **probabilistic** 1/2/3/4/5/10-year forecasts via Monte-Carlo simulation.
5. Compares **buying now (lump sum) vs spreading the purchase (dollar-cost averaging)**.

---

## 2. The "Muharram effect" — tested, not assumed

The common belief in South Asia is that gold falls during Muharram and rebounds after.
Using each month's Hijri (Islamic) calendar month over 1968–2026:

| | Mean monthly return | Share of months positive |
|---|---|---|
| **Muharram** (n=60) | **+0.44%** | 42% |
| All other months (n=641) | +0.70% | 51% |
| Difference | −0.27%/month | — |
| Bootstrap p-value | **0.675** | (not significant) |

**Verdict: NOT statistically supported.** Gold does *not* reliably fall in Muharram —
its average Muharram return is still *positive*. There is a *faint* echo of the folklore
(fewer Muharram months are "up", and the following month, Safar, averages a healthy
+1.12%), but it is swamped by noise and is **not tradeable**. The one genuinely
significant *Gregorian* seasonal is a strong **January** (+2.47%/month, p=0.008), broadly
consistent with documented turn-of-year and festival-demand effects. See
`reports/figures/02_seasonality.png`.

---

## 3. Model backtest — can any model actually predict gold?

Walk-forward, out-of-sample, 1-month horizon (this is the honest test; in-sample fit is
meaningless):

| Model | Approx. price error | Directional accuracy |
|---|---|---|
| Random walk (benchmark) | 3.89% | 56% |
| SARIMA (statistical) | 3.89% | 61% |
| **Gradient Boosting (ML)** | **2.94%** | **70%** |
| LSTM (deep learning) | 4.39% | 58% |

**Takeaways, stated plainly:**

- The **Gradient-Boosting ML model genuinely beats a coin-flip** at short horizons
  (70% directional accuracy). That is a real, if modest, edge for *timing*, not for
  long-range price targets.
- The **LSTM neural network under-performs even a random walk.** Deep learning is not
  magic on a short, noisy monthly series — reporting otherwise would be dishonest. It is
  included because you asked for it, and its failure here is itself a useful result.
- Crucially, **all of these are 1-month errors.** Nobody demonstrated skill at
  multi-*year* price prediction, because that skill does not exist. That is why the
  long-horizon forecast below is a **probability fan, not a line.**

See `reports/figures/03_backtest.png`.

---

## 4. The forecast — 1 to 10 years, as probabilities

Because point forecasts years out are fantasy, we simulate **10,000 possible futures**
two ways.

### A) Block-bootstrap (resamples gold's own real history)

| Horizon | P10 (bad) | Median | P90 (good) | Chance below today | Median CAGR |
|---|---|---|---|---|---|
| 1 yr | $3,543 | $4,387 | $5,852 | 38% | +5.7% |
| 2 yr | $3,411 | $4,770 | $7,239 | 31% | +7.2% |
| 3 yr | $3,367 | $5,197 | $8,537 | 26% | +7.8% |
| 4 yr | $3,410 | $5,566 | $9,911 | 22% | +7.6% |
| 5 yr | $3,426 | $6,043 | $11,580 | 20% | +7.8% |
| 10 yr | $4,014 | $9,179 | $22,833 | 11% | +8.3% |

⚠️ **This method is optimistic by construction** — it assumes the future resembles gold's
historically *exceptional* run (including the one-off repricing after the gold standard
ended and the 2000s boom). Treat it as the bullish end of plausible.

### B) Scenario-drift (you pick the assumption)

Chance of being **below today's price**, by assumed long-run drift:

| Horizon | Bear (−4%/yr) | Base (+3%/yr ≈ inflation) | Bull (+8%/yr) |
|---|---|---|---|
| 1 yr | 63% | 46% | 33% |
| 2 yr | 68% | 44% | 28% |
| 5 yr | 76% | 41% | 18% |
| 10 yr | 85% | 37% | 10% |

**The honest conclusion:** the answer depends almost entirely on an assumption nobody can
verify. If gold merely tracks inflation from here (the "base" case most economists would
defend for a metal that pays no yield), buying now is close to a **coin-flip over 5 years.**
See `reports/figures/04_forecast_fan.png` and `05_scenarios.png`.

---

## 5. The single most important fact for your decision: gold is *stretched*

Your father would be deploying a lump sum **after a near-parabolic rally**:

- Spot ~$4,150 is **+43% above its 3-year average.**
- Gold is up **+24% over 12 months** and **+73% over 24 months.**
- It has already **fallen ~17% from the February-2026 peak of $5,020** — i.e. a
  correction is *already underway.*

Historically, buying gold when it is this far above trend has produced below-average
forward returns and above-average risk of a multi-year drawdown (gold fell ~65% in
real terms from its 1980 peak and took ~28 years to recover; it fell ~45% from 2011 to
2015). This does **not** mean gold *will* fall — but it means the *entry point* is
unusually risky for a one-shot purchase.

---

## 6. How to enter, if you do: lump sum vs dollar-cost averaging

Simulated across every historical start month (value of $1 after 5 years):

| Strategy | Median | P10 (worst) | Chance of loss |
|---|---|---|---|
| Lump sum (all in now) | 1.38 | 0.75 | 30% |
| DCA over 12 months | 1.31 | **0.76** | 28% |
| DCA over 24 months | 1.26 | **0.77** | 29% |

Spreading the purchase gives up a little upside (gold trends up over time) but **reduces
the worst-case timing loss** — exactly the risk that matters when buying after a big
run-up. For retirement money, that trade is usually worth it.

---

## 7. Bottom line — is it a good investment *right now*?

**A measured "not as a lump sum at today's price, and not with most of the money."**

The reasoning, in one paragraph: Gold has been a superb store of value over decades and is
a legitimate *diversifier* and inflation/geopolitical hedge — especially relevant in
Pakistan, where it also hedges rupee depreciation. But the models find **no reliable way
to predict multi-year prices**, the honest simulations show a **material (roughly 30–45%
in the base case) chance of being underwater in 1–5 years**, and gold is **currently ~43%
above trend and already correcting from an all-time high.** Deploying a retiree's entire
lump sum into a single, no-yield, volatile asset at a stretched price concentrates exactly
the risks a retiree can least afford.

**A more defensible plan (not advice, a framework to discuss with a licensed advisor):**

1. **Size it as a hedge, not a bet** — a *portion* of the savings (many advisors suggest
   ~5–15% of a portfolio in gold), not the whole retirement sum.
2. **Average in over 12–24 months** rather than buying it all this week, to blunt the
   timing risk highlighted above.
3. **Keep the rest diversified** — inflation-protected instruments, dividend/rental income,
   and an emergency cash buffer matter more for a retiree than chasing a hot commodity.
4. **In Pakistan specifically**, factor in dealer premiums/making charges, purity
   verification, storage/security, and that local prices already embed the PKR/USD rate —
   so a stronger rupee can erase a USD gold gain (and vice-versa).

If the goal is *capital preservation with some inflation protection*, a measured, phased,
minority allocation to gold is reasonable. If the goal is *growing* retirement capital,
gold at a stretched price is a weak primary vehicle and should not carry that load alone.

---

## Reproduce

```bash
pip install -r requirements.txt
python3 run_all.py          # regenerates every number and figure here
```

Outputs land in `reports/` (CSVs) and `reports/figures/` (charts).

*Data source: LBMA/London gold fixing, monthly, via the public `datasets/gold-prices`
series; current spot cross-checked against live XAU/USD quotes on 7 Jul 2026. No paid
data, no API keys.*
