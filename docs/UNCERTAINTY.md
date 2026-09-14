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

## Two loopholes tested and closed

**Does the interval need to widen for small groups?** No. Residual variance across pool-size buckets:

| Pool size | n | mean | sd | P(\|err\| ≤ 5) |
|---|---|---|---|---|
| <25 | 21 | −1.19 | 7.89 | 81% |
| 25–100 | 24 | −1.25 | 7.84 | 79% |
| 100–400 | 41 | +0.00 | 8.44 | 88% |
| >400 | 23 | +0.65 | 4.07 | 96% |

Levene test for equal variance: **W = 0.83, p = 0.478** — no significant difference, so one pooled interval is
justified. Caveat stated honestly: the largest bucket does show a visibly tighter spread (sd 4.07 against ~8),
and with n = 23 the test has limited power to detect it. The pooled interval is therefore mildly
*conservative* for large groups rather than anti-conservative for small ones.

**Is allocation-share error double-counted if added separately?** Yes, so it is not added. The out-of-sample
procedure forecasts each group's share from the previous round *before* deriving the cut-off, so share error is
already inside these residuals:

| residual set | n | MAE | sd |
|---|---|---|---|
| mechanism (allocation known) | 123 | 1.02 | 2.16 |
| out-of-sample (allocation forecast) | 109 | 4.40 | 7.41 |

The 3.4-point MAE gap **is** the share-forecast error. A separate share-uncertainty layer would count it twice.

## Round size is not the reader's to guess

An earlier version of the dashboard asked the reader to pick an assumed round size. That was wrong: it made the
headline probability depend on a number **nobody can know**, and quietly transferred the model's largest
uncertainty onto the user.

Round size is set by migration planning levels, not by the pool, and it is precisely what this model cannot
predict. So the dashboard no longer asks. It fixes nothing and shows **every plausible size at once**, with the
policy-implied case marked:

| Round size | Forecast cut-off | P(reaches 85) for ANZSCO 2349 |
|---|---|---|
| 5,000 | 85 | 77% |
| 7,500 | 80 | 90% |
| **10,000** — what the planning levels imply | **75** | **94%** |
| 12,500 | 75 | 94% |
| 15,000 | 70 | 96% |

The five rounds on record ranged from 6,450 to 14,724, so the panel spans the realistic range rather than a
hypothetical one. The honest answer for a physicist on 85 points is therefore **77–96%, most likely around 94%** —
a range with a marked central case, not a single number resting on someone's guess.

## What this probability does and does not cover

**Covers:** error in locating the cut-off — allocation-share forecasting, pool measurement, the 5-point score
grid, and the residual mechanism noise, all as actually observed out of sample.

**Does not cover:** whether a round is held at all, and whether the allocation share holds. Both are policy, and
neither appears in the residuals. Every figure here is explicitly *conditional on a round being held*.

This supersedes the earlier scenario-weighted "40–77%", which applied a hand-chosen `2^−age` kernel to five
historical allocations, three of which came from a different regime. The present figure is calibrated rather
than weighted by judgement.
