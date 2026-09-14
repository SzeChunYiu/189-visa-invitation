# What is modelled, and what is not

An honest inventory. "Modelled" means it changes a number the page reports, and was validated.

## Modelled

| Dynamic | How | Evidence |
|---|---|---|
| Inclusion / exclusion | tier filter + persistence | 87% accuracy predicting who gets zero |
| Allocation size | persistence of group share | share autocorrelation 0.92–0.96 |
| Distribution within a group | points desc, then date asc, stopping mid-band | 94.5% of bands above margin taken whole; 28.8% at the margin |
| Round size | distribution from published places × observed invitations-per-place | median 12,090, 10–90% 6,402–17,050 |
| Forecast error | empirical prediction interval from held-out residuals | 80% interval, no normality assumed |
| Group skipped entirely | P(zero) conditioned on last round | 8% vs 76% |
| Cut-off movement | empirical Δ distribution | 32% no change, 53% ±5, 15% ±10 |
| Your position within a band | date-of-effect CDF | optional input; worst case assumed without it |
| EOI expiry | two-year cliff | survival 77% at 18–24 months, 0.8% beyond |
| Points mobility | 47.3% re-score, mean +8.0 | date of effect resets, so upgraders queue behind |
| Panel coverage | 2024 rounds excluded from fitting | corr(coverage, error) = −0.96 |
| **Forecast horizon** | **+0.66 pts per month of pool staleness** | **r(lag, MAE) = +0.97, r(lag, bias) = −0.92** |

### The horizon finding

Re-running the forecast with the pool taken *k* months before each round:

| Lag (months) | Exact | MAE | Bias |
|---|---|---|---|
| 1 | 88% | 0.61 | −0.50 |
| 2 | 66% | 1.87 | −1.87 |
| 4 | 55% | 2.57 | −2.07 |
| 6 | 35% | 4.83 | −4.55 |

Bias is **negative and growing**: an older pool is a smaller pool, so the count walks deeper than it really
would. **A stale forecast is optimistic.** The live page uses the Aug-2026 snapshot, so a late-September round
needs no correction; a December round would sit about 2 points higher than shown.

*(Lag 0 was excluded: that snapshot postdates the round, so the pool is already drained — a look-ahead error of
−6.23, not a horizon effect.)*

## Not modelled

| Gap | Why it matters | Status |
|---|---|---|
| **Component drift** (English, partner, Australian study) | if competitors accumulate points, the pool strengthens and cut-offs rise | extracted, not modelled — **partly absorbed** by the horizon correction, which measures net pool drift empirically |
| **Score-distribution drift** | same channel | same |
| **Cross-group budget coupling** | groups share one round budget, so a big allocation to one crowds out others; treated as independent | unmodelled |
| **Seasonality** | rounds cluster Aug / Nov / Jun | unmodelled; only 5 rounds, too thin to fit |
| **491 redirection** | Regional was cut 57%; displaced applicants may enter the 189 pool | unmodelled; would appear in later snapshots |
| **6-digit occupation allocation** | modelled at 4-digit unit group, the level ceilings apply at | deliberate |
| **Whether a round happens** | the dominant uncertainty | **not modellable from this data** — every figure is conditional on it |

The horizon correction is a **reduced-form catch-all** for pool dynamics: it measures how wrong the forecast
gets as the pool ages, whatever the mix of inflow, upgrades and expiry driving it. That is weaker than modelling
each channel, but it is measured rather than assumed, and it captures their net effect.

## Hard limits of the source

- The EOI panel starts **September 2024**. No earlier snapshot is published, so no pool, queue or date-of-effect
  figure can go back further.
- The tier model is an **internal planning tool** known through a secondary summary; homeaffairs.gov.au returns
  403 to automated fetching.
- Round dates and sizes before 2024 were not retrieved. A verified 2020–2026 series remains the single most
  valuable open improvement.
