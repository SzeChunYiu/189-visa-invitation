# Methodology: three traps in the SkillSelect panel

The public dashboard is a Qlik Sense mashup (app `aaac76b5-ad30-477e-9ca0-472f8ab57fc8`).
Reading it naively produces confidently wrong numbers. Three traps, in order of severity.

## Trap 1 — `EOI Status` is recorded per EOI, not per visa leg

**Symptom.** Filter `Visa Type = 189PTS` and count `INVITED`, and you get 500–800 invitations
in *every* month, with invitations appearing at 50–65 points and 15,191 in a single month —
impossible for a stream of ~16,900 places a year.

**Cause.** One EOI may nominate 189, 190 and 491 simultaneously. Status attaches to `%EOIID`,
so an EOI invited for 190 still reads as `INVITED` under its 189 leg. Summing the three visa
filters exceeds the distinct invited count by **~50% in every month** (`test_overlap.py`).

**No leg-level discriminator exists.** All validity intervals (`%VisaCurrentTo`, `%CombinedTo`)
stay open on every leg of an invited EOI — checked and ruled out (`diag.py`).

**Fix — single-leg identification.** Restrict to EOIs whose *only* visa leg is 189, using Qlik's
exclusion-set function:

```
%EOIID = E({<[Visa Type] -= {'189PTS Points-Tested Stream'}>} %EOIID)
```

For these the invitation is unambiguously a 189 invitation. Validated by the partition identity
`all == only + multi` in all 24 months (`test_only189.py`).

**Result.** The 189-only series is *exactly zero* in 19 of 24 months and large in five. That
is what exposes the real round calendar. Total round size is then recovered by attributing
multi-leg invitations with a difference-in-differences correction against non-round months
(baseline multi/no-189 ratio = 0.306).

## Trap 2 — rows are versions, not EOIs

The fact table is a slowly-changing dimension: 19.5M rows over ~10M EOIs, ~1.93–2.11 rows per
EOI per snapshot. **Every measure must be `Count(distinct %EOIID)`.** Row counts overstate by ~2×.

## Trap 3 — front-end small-cell masking is not in the data

The Qlik sheets mask counts below 20. The engine underneath does not. Confirmed by complement
differencing — `all` minus `all-except-occupation` reproduced the direct count exactly (72 = 72)
including cells of 1, 2 and 3 (`test_suppress.py`). *Credit to the complement-differencing idea,
which turned a suspected limitation into a positive proof of exactness.*

## Confound checked and cleared: score drift

31% of EOIs change points over their lifetime, so "the score on the INVITED row" could in
principle be a later score. Two independent checks:

1. **99.4%** of INVITED rows have `%StatusDate` inside that row-version's own validity interval —
   so the score is the score held at invitation (`test_drift2.py`).
2. Pool drops track attributed invitations score-by-score at **r = 0.96** across the Jun-2026 round.

Occupation stratification therefore stands as a real mechanism, not a measurement artefact.
