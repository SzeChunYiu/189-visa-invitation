# Model specification

## Unit of analysis

The binding stratum is the **ANZSCO 4-digit unit group**, where occupation ceilings apply —
for a physicist (234914) that is **2349 Other Natural and Physical Science Professionals**.
234914 alone is used only as a consistency check; its per-round counts (3, 4, 9, 15, 23) are
too small to carry the estimate.

## Estimands

1. **Cut-off** `c(g, r)` — minimum points invited in unit group *g* in round *r*.
   Robust, directly observed, and the decisive statistic.
2. **Clearance** at a score — invitations at that score over the standing pool, bracketed
   between the pre-round and round-month snapshots because EOIs arrive between the two.
3. **Rank** — competitors ahead of the applicant: everyone above their score, plus everyone
   at their score with an earlier date of effect.

## Result for 85 points, ANZSCO 2349

- Cut-off trajectory: **95 → 90 → 90 → 85 → 80**, monotone non-increasing.
- Both rounds that reached 85 cleared the whole 85-point tranche (clearance 79–100%, 92–100%);
  the stratum's 85-point pool collapses from ~10 to ~1 immediately after a round.
- Applicant rank entering the next round: **~23** (single-leg basis) or **~32** (all-leg basis).
  Last round's allocation to 2349 was **35** single-leg (~66 all-leg). Rank is covered on both bases.

Recency-weighted over the five observed rounds (weight 2^−age):

| P(cut-off < 85) | P(cut-off = 85) | P(cut-off > 85) |
|---|---|---|
| 0.516 | 0.258 | 0.226 |

## The threshold form

Both routes above reduce to the same binary, because a round invites strictly down the points order within a
unit group. The applicant is at **rank 32** in 2349. They are invited **iff the round allocates ≥32 invitations
to 2349**:

| Round | Sep 2024 | Nov 2024 | Aug 2025 | Nov 2025 | Jun 2026 |
|---|---|---|---|---|---|
| Allocation to 2349 (all-leg) | 5 | 21 | 29 | **43** | **87** |
| Covers rank 32 | no | no | no | yes | yes |

- **Unweighted: 40%.** Ignores the trend entirely — treat as a floor.
- **Recency-weighted (2^−age): 77%.** The weighting kernel is arbitrary over n=5 and is stated so the reader can
  discount it; it halves each older round's weight.
- **Trend: above 77%.** Allocation is monotone increasing, 17.4× over five rounds, and 2349's share of the round
  grew 0.12% → 1.67%.

The downside risk is **not the applicant's score**. It is a policy cut returning this stratum's allocation below 32.

## Out-of-sample validation

The mechanism — rank the stratum's pool by points, allocate top-down, read the cut-off where invitations run out —
was tested against Jun-2026 for every occupation receiving ≥5 invitations:

| Occupations | Within ±5 pts | Exact | r | MAE | Mean signed error |
|---|---|---|---|---|---|
| 49 | 49 (100%) | 21 (43%) | 0.941 | 2.86 pts | **+2.86 pts** |

The bias is positive: real rounds go *deeper* than the rule predicts, so applying it to the applicant understates
their odds. A conservation check confirms per-occupation invitations sum exactly to each round total (residual 0).

## What the model cannot do

- **See exogenous policy.** Annual migration planning levels and ministerial direction on occupation priority set
  round size and cadence. They are not in this data and no EOI-derived quantity substitutes for them.
- **Predict whether a round happens, or its size.** Both are set by planning levels, not by the
  pool. Gaps between the five observed rounds were 2, 9, 3 and 7 months — n=4 gaps supports no
  dated forecast.
- **Resolve date of effect.** `Month Submitted` is the proxy; a points change resets date of
  effect. For a *recently submitted* EOI this biases the estimated rank **conservative**
  (some apparently-earlier competitors have later effective dates).
- **See EOIs submitted after Aug 2026.** The latest snapshot is 08/2026 and predates a
  10-Sep-2026 lodgement, so the applicant is not in the extract.

## Sensitivity

The dominant sensitivity is not round size but the **depletion trend**: the stock above 85 in
2349 is now only ~11, so any round of typical size exhausts it and pushes the cut-off to or
below 85. A reversal would require either a sharp influx of high-point competitors into 2349
or a cut in the group's allocation.
