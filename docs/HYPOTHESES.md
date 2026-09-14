# Hypothesis battery

What, beyond pool-rank, systematically moves the cut-off? Each hypothesis is tested on the three rounds
with adequate panel coverage (Aug-2025, Nov-2025, Jun-2026) on a consistent single-leg basis.

## H1 — Policy / regime change: **CONFIRMED, one break**

| Transition | Share correlation | Cosine | Turnover of the invited set |
|---|---|---|---|
| Sep 24 → Nov 24 | 0.821 | 0.863 | 13% |
| **Nov 24 → Aug 25** | **0.444** | **0.532** | **38%** |
| Aug 25 → Nov 25 | 0.908 | 0.920 | 17% |
| Nov 25 → Jun 26 | 0.948 | 0.954 | 16% |

One structural break, at the 2024-25 → 2025-26 program-year boundary. The two most recent transitions are
near-identical splits. This is the measured basis for treating the 2024 allocations as a stale regime rather
than plausible draws for the next round.

## H2 — Systematic occupation bias: **NOT FOUND**

Cross-round residual correlation within a group averages **r = +0.033** (pairwise +0.145, −0.017, −0.029).
Residuals are round-specific noise, not a persistent per-occupation effect. No occupation is systematically
treated better or worse than the mechanism predicts.

## H3 — Level bias: **WEAK**

corr(actual cut-off, error) = +0.218; corr(pool size, error) = +0.074; corr(allocation, error) = −0.089.
Nothing strong enough to correct for.

## H7 — What sets a group's share: **quota, not demand**

Allocation share and pool share are collinear, so raw correlations cannot separate them. Partial correlations
on log shares can:

| | value |
|---|---|
| partial corr(current share, **past share** \| pool share) | **+0.275** |
| partial corr(current share, **pool share** \| past share) | **−0.083** |

Past allocation survives controlling for pool size; pool size adds nothing once past allocation is known.
The split behaves like a persistent quota rather than demand-responsive rationing.

*(An earlier draft compared raw correlations of 0.948 and 0.939 and claimed the first "far better" — that gap
is not meaningful, and the partials are what settle it.)*

## H8 — Sector effect: **REAL but deliberately not modelled**

| Sector | n | Mean error | 95% CI |
|---|---|---|---|
| Managers (1xxx) | 14 | −1.79 | ±1.30 |
| Professionals (2xxx) | 116 | −0.47 | ±0.34 |
| Trades (3xxx) | 46 | −1.52 | ±0.80 |

Kruskal-Wallis p = 0.005; Professionals vs Trades p = 0.007. The effect is genuine but **1.05 points on a
5-point score grid**, so it cannot move a forecast by a whole bucket. Applying a per-sector offset makes
accuracy *worse* — **MAE 1.42 against 0.95** — so it is reported and left out of the model.

## H6 — Round-size effect: **NONE**

Aug-2025 (6,450): 88% exact, MAE 0.80 · Nov-2025 (9,826): 75%, 1.23 · Jun-2026 (9,748): 85%, 0.81.

## Not testable from this data

Ministerial direction on occupation priority, and whether a round is scheduled. See
[POLICY.md](POLICY.md) for the published planning levels, which are the one exogenous input that *can* be read in.
