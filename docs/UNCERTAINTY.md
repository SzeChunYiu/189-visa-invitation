# Uncertainty

The forecast used to be a bare number. It now carries a **calibrated** interval and probability, derived from
how wrong this same method was on held-out rounds — not from an assumption about the error distribution.

## Where the interval comes from

Leave-one-round-out forecasts produce a residual per group-round, `err = forecast − actual`. Restricting to the
two folds from the current regime (Nov-2025, Jun-2026, n = 109):

| statistic | value |
|---|---|
| mean | −0.37 pts |
| sd | 7.41 pts |
| P(\|err\| ≤ 5) | 86% |
| P(err = 0) | 43% |
| 10th / 90th percentile | −6 / +5 |

So given a forecast **f**, the 80% interval on the truth is **[f − 5, f + 6]**, and

```
P(actual cut-off ≤ your score) = P(err ≥ f − your score)
```

read straight off the empirical residuals. No normality assumption — the residual distribution is discrete and
lumpy (43% exactly zero), which a Gaussian interval would misrepresent.

## Applied: ANZSCO 2349 at 85 points

| Round size | Forecast | 80% interval | P(cut-off reaches 85) |
|---|---|---|---|
| 5,000 | 85 | 80–91 | **77%** |
| 7,500 | 80 | 75–86 | **90%** |
| 10,000 | 75 | 70–81 | **94%** |
| 12,500 | 75 | 70–81 | **94%** |
| 15,000 | 70 | 65–76 | **96%** |

At the policy-implied round size (~10,800, see [POLICY.md](POLICY.md)) the figure is **94%**.

## What this probability does and does not cover

**Covers:** error in locating the cut-off — allocation-share forecasting, pool measurement, the 5-point score
grid, and the residual mechanism noise, all as actually observed out of sample.

**Does not cover:** whether a round is held at all, and whether the allocation share holds. Both are policy, and
neither appears in the residuals. Every figure here is explicitly *conditional on a round being held*.

This supersedes the earlier scenario-weighted "40–77%", which applied a hand-chosen `2^−age` kernel to five
historical allocations, three of which came from a different regime. The present figure is calibrated rather
than weighted by judgement.
