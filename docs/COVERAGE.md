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

## The six gaps, now closed

Each was either **modelled** or **shown not to matter**, with the test that settled it.

### 1. Pool strengthening — MODELLED (and it is real)

The pool is getting stronger, not just bigger:

| | 09/2024 | 08/2026 | Trend |
|---|---|---|---|
| mean score | 73.02 | 74.13 | **+0.046 pts/month** (r = +0.68) |
| share at 85+ | 16.5% | 22.1% | **+0.21 pp/month** (r = +0.83) |
| share at 90+ | 7.1% | 11.3% | +0.20 pp/month (r = +0.85) |

This is a genuine headwind — competition at the top is intensifying. It is **already priced** by the horizon
correction, which measures forecast error against pool age end-to-end and so absorbs drift whatever drives it.
Adding a separate drift term would double-count.

### 2. Point components — MODELLED, and the most actionable finding on the page

Share holding each component, at 85+ versus 65–84:

| Component | At 85+ | At 65–84 | Gap |
|---|---|---|---|
| **Max English (20 pts)** | **83.6%** | **19.3%** | **+64.3 pp** |
| Partner skills (10 pts) | 84.4% | 63.3% | +21.2 pp |
| Australian study | 82.0% | 62.7% | +19.3 pp |

**English is the dividing line.** It separates high scorers from the rest more than everything else combined,
and it is the one component most applicants can still change. Now shown on the page.

### 3. Cross-group budget coupling — NOT PRESENT

Crowding-out would make group shares **negatively** correlated. They are **positive**: mean pairwise r = +0.065
raw, and +0.079 after de-meaning each round to strip the round-size effect. Positive means groups rise and fall
together — the policy regime, which persistence already captures — not competition for one budget.

*(My first automated verdict here was wrong: the threshold test compared magnitude and ignored sign, so it
reported "groups do compete" on a positive correlation. Corrected.)*

**Conclusion: modelling groups independently and normalising is valid.**

### 4. Seasonality — NO POWER TO FIT, and said so

Round months: Sep, Nov, Aug, Nov, Jun. χ² against uniform = 11.8 on 11 df, **p = 0.379**. Five rounds cannot
support a seasonal term. The model conditions on "a round is held" rather than pretending to time it.

### 5. 491 redirection — WATCH ITEM, not yet observable

The Regional cut applies from July 2026 and the panel ends August 2026, so at most two months are visible.
189 pool growth has **not** accelerated: **+3,756/month in 2026 against +6,912/month over the whole panel**.
189 and 491 growth correlate **+0.70**, moving together rather than one feeding the other. Re-check when later
snapshots publish.

### 6. Unit group vs 6-digit occupation — UNIT GROUP IS CORRECT

Within-group spread of the cut-off: **1.39 points**. Between-occupation spread overall: **7.88 points**.
**82% of the variation is between unit groups, not within them.** Modelling 6-digit occupations separately
would add noise, not signal — and ceilings apply at unit-group level anyway.

## Hard limits of the source

- The EOI panel starts **September 2024**. No earlier snapshot is published, so no pool, queue or date-of-effect
  figure can go back further.
- The tier model is an **internal planning tool** known through a secondary summary; homeaffairs.gov.au returns
  403 to automated fetching.
- Round dates and sizes before 2024 were not retrieved. A verified 2020–2026 series remains the single most
  valuable open improvement.
