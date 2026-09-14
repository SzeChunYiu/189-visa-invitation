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

## The threshold form — and why it was retired as the headline

The threshold reading asked how many of the five historical allocations would have covered the applicant's queue
rank, giving 40–77%. **That is not a like-for-like probability.** Three of the five draws come from a regime when
2349's share of the round was 0.07–0.13%, against 0.67% today — a 5–10× difference. Share autocorrelation on the
recent transitions is 0.92–0.96, so the recent share is the forecastable quantity and the 2024 values are a
different regime, not plausible draws.

The governing model is the forecast form: where does the allocation land in the group's score distribution.

| Allocation to 2349 (single-leg) | Outcome at 85 points |
|---|---|
| < 9 | cut-off above 85 — not reached |
| 9 – 21 | boundary lands on 85, rationed by date (applicant is last) |
| **≥ 22** | **cut-off below 85 — clears regardless of date** |

Last round's allocation was **35**, i.e. **1.59×** the clearing threshold. Re-run at all five historical round
sizes using today's share, the cut-off lands at 80, 70, 80, 75, 75 — clearing 85 in every case. The round size
needed to clear at today's share is ~6,289; the smallest round in the record is 6,450.


## Validation — see CONSISTENCY.md

The figures once quoted here ("49/49 within ±5, r = 0.941, bias +2.9") are **superseded**. They compared
single-leg invitations against an all-leg pool. The corrected, consistent-basis results across all 82 unit groups
and all five rounds are in [CONSISTENCY.md](CONSISTENCY.md): **83% exact, MAE 0.95** on the rounds with complete
panel coverage, and **91% within ±5, MAE 3.84** out of sample on the latest fold.


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
