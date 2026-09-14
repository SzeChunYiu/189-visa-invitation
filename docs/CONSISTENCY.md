# Cross-occupation, cross-time consistency

The model is run for **every unit group in every round** — 315 group-rounds — not the single round it was first
checked on.

## A basis error the universal test exposed

An earlier version of this repo reported "49 of 49 occupations within ±5 points, r = 0.941" for Jun-2026.
That compared **single-leg invitations against an all-leg pool**. Run on a consistent all-leg basis the model
collapses: 38% exact, r = 0.52, and bias **+17.9 points** for groups with pools over 1,500.

Cause: the all-leg minimum invited score is contaminated downward, because an EOI invited for 190/491 still
carries a 189 leg.

| | mean gap (single-leg minus all-leg cut-off) |
|---|---|
| All groups | **+7.26 pts** |
| Groups with ≥200 invited | **+11.25 pts** |
| Groups with <20 invited | +5.00 pts |

Everything below is on a consistent **single-leg** basis — the basis that matched the official Home Affairs table
at 90.3%.

## Mechanism test (cut-off from pool + actual allocation)

| Round | Panel coverage | Groups | Exact | Within ±5 | MAE | Bias |
|---|---|---|---|---|---|---|
| Sep 2024 | 12% | 63 | 13% | 38% | 9.92 | −9.92 |
| Nov 2024 | 20% | 73 | 15% | 45% | 8.70 | −8.01 |
| Aug 2025 | 69% | 56 | **88%** | 96% | 0.80 | −0.62 |
| Nov 2025 | 81% | 61 | **75%** | 100% | 1.23 | −1.07 |
| Jun 2026 | 98% | 62 | **85%** | 98% | 0.81 | −0.81 |
| **All** | | **315** | 53% | 74% | 4.54 | −4.32 |

**The inconsistency is explained, not averaged away.** Correlation between panel coverage and error is **−0.962**.

- Rounds with ≥69% coverage: **83% exact, MAE 0.95**
- Rounds with ≤20% coverage: 14% exact, MAE 9.26

The 2024 bias is **negative**, which is precisely what an understated pool produces: the top-down walk exhausts the
recorded pool too early and dives too deep. The failure is confined to the period when the dashboard had captured
only 12–20% of the eventual pool.

## Out-of-sample (allocation forecast from the prior round only)

| Fold | Groups | Exact | Within ±5 | MAE |
|---|---|---|---|---|
| Nov 2024 | 65 | 18% | 55% | 8.08 |
| Aug 2025 | 46 | 37% | 70% | 5.11 |
| Nov 2025 | 53 | 42% | 81% | 5.00 |
| Jun 2026 | 56 | **45%** | **91%** | **3.84** |
| All | 220 | 34.5% | 73.6% | 5.64 |

Round size is taken as given — it is exogenous policy. The gap between knowing the allocation (MAE 4.54) and
forecasting it (5.64) is **1.1 points**: the ranking rule is the reliable part, the allocation is the uncertain input.

## Consistency by occupation size

| Pool size | Cells | Exact | Within ±5 | MAE |
|---|---|---|---|---|
| <25 | 93 | 48% | 65% | 5.70 |
| 25–100 | 73 | 45% | 67% | 5.68 |
| 100–400 | 88 | 58% | 80% | 3.75 |
| 400–1500 | 53 | 57% | 87% | 2.92 |
| >1500 | 8 | 100% | 100% | 0.00 |

No size-dependent breakdown once the basis is consistent; thin cells are noisier, as expected.

## Is allocation forecastable?

| Transition | Pearson r | Share r |
|---|---|---|
| Nov 2024 ← Sep 2024 | 0.799 | 0.805 |
| Aug 2025 ← Nov 2024 | 0.495 | 0.500 |
| Nov 2025 ← Aug 2025 | 0.918 | 0.920 |
| Jun 2026 ← Nov 2025 | **0.960** | **0.961** |
| Pooled | **0.793** | 0.797 |

Forecasting is defensible, so the per-occupation forecast table ships as cut-offs conditional on round size rather
than as unconditional probabilities.

## Two caveats about ANZSCO 2349 specifically

1. **Its monotone allocation series is unusual.** Only **15 of 84 groups (18%)** have a monotone non-decreasing
   allocation. Earlier write-ups leaned on 2349's 5→21→29→43→87 trend as if it were typical. It is not.
2. **Its clean-step boundary is partly a small-numbers artefact.** Groups with no rationed boundary cell have
   significantly smaller pools (Mann-Whitney p < 0.0001; median pool 3 versus 59). 2349's cells are thin, so
   "CLEARED" there is more easily obtained by chance than in a large group.

## Still not modelled

Per-occupation pool inflow dynamics, and what actually *sets* each group's allocation. The published ceilings
would be the natural candidate, but only the science-group ceilings were obtained (all 500, and non-binding for
2349), so inferring the rule from the allocations themselves would be circular. Named as an unexplained input.
