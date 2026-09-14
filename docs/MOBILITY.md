# Points mobility and the date of effect

## The question

Many people lodge an EOI at a low score and gain points later. Does the data show it, and what does it do to
queue position?

**Yes — directly.** The fact table is a slowly-changing dimension: every version of an EOI is a row carrying its own
`Score` and its own validity interval (`%EOIPBDateFrom`/`%EOIPBDateTo` for the points breakdown). A points change
creates a new version, so upgrades are observable without inference.

## How much movement there is

| Measure | Value |
|---|---|
| EOIs in the 189 pool whose score changed over its life | **47.3%** |
| Gained +5 | 28.4% |
| Gained +10 | 12.4% |
| Gained +15 | 4.1% |
| Gained +20 or more | 2.4% |
| Mean gain among movers | **+8.0 points** |

The 85+ band is not a stable population. Across the whole 189 pool, **43% of everyone now at 85+ acquired those
points within the last six months**, and roughly 4,500 EOIs enter the 85+ band every month. In ANZSCO 2349
specifically, about 6 enter per month, and **none** of the current 85+ cohort has held its score for more than a year.

## Why this is the crux of queue position

Invitations rank by points, then **date of effect** — and a points change **resets the date of effect**. So an
upgrade does not buy seniority: it puts the upgraded EOI at the *back* of its new points band.

Consequences:

- Someone at 80 points who reaches 85 after 10 Sep 2026 takes a later date of effect and queues **behind** a
  10 Sep applicant, not ahead.
- Because the 85+ band turns over almost completely within a year, an applicant's position **stops eroding once
  lodged** and improves only — as those ahead are invited away or hit the two-year expiry.
- Of the 31 EOIs ahead in 2349 at 85+, **100% hold a date of effect before 10 Sep 2026**, verified directly.

## Measurement caveat — one approach was tried and discarded

Re-running the saturation test with `%EOIPBDateFrom` aggregated **across snapshots** produced impossible values:
79.6% of cells showed a pool date of effect *later than the snapshot they belonged to*, overshooting by up to 702
days. The cross-snapshot aggregation is not snapshot-restricted, so **those results were discarded, not reported**.

Restricted to a **single snapshot** (08/2026) the same field is clean — 1 stray row out of 31 EOIs — and that is the
only form used here, for the rank calculation. The cross-snapshot saturation states in
[THEORY.md](THEORY.md) therefore remain on submission-date, with the residual named there.

## Effect on the answer

Correcting the rank from a submission-month proxy to the true date of effect moves it from 30 to **32**, and removes
the "60–90% if the round slips past December" branch, which was an artefact of the proxy. The band is now
**stable at 40–77%** across round timing: only the two largest allocations 2349 has ever received (43, 87) clear
this rank; the three smaller ones (5, 21, 29) do not.
