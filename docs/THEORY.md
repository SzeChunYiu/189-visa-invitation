# The mechanism

One rule reproduces every observation in the panel.

## The rule

1. **Each round sets an allocation per ANZSCO unit group.** This is *not* the published occupation ceiling, which is
   a non-binding upper bound: 2349's ceiling is 500 and the largest observed round used 87.
2. **Within a group, invitations run strictly by points descending, then date of effect ascending.**
3. **The allocation therefore lands on a boundary score.** Above it, every score is fully exhausted; the boundary
   score itself is usually rationed by date; below it, nothing is touched.

## The saturation test

The three states are directly observable. For each (occupation, score, round), compare the newest-dated EOI standing
in the pool against the newest-dated EOI invited:

| State | Condition | What it means for a candidate |
|---|---|---|
| **CLEARED** | newest invited ≥ newest in pool | Invited regardless of EOI date |
| **PARTIAL** | some invited, newest invited < newest in pool | Your date of effect decides |
| **UNTOUCHED** | none invited | Not reached |

In Jun-2026, across 62 unit groups receiving invitations: 79% had at least one rationed boundary cell, and 78% of
rationed cells sat at the group's lowest invited score — exactly where an allocation runs out.

## What it explains

| Observation | Explanation |
|---|---|
| Every round invites someone at 65 while 85-pointers wait | Different groups, different allocations |
| Per-occupation minimums span 65–100 in one round | Each allocation lands at a different depth |
| Occupation ceiling never binds | The operative allocation is far below the ceiling |
| Published tie-break "April 2026" seemed to exclude recent EOIs | It is the boundary date **at the national floor** — of every score invited in Jun-2026, only 65 stops at April; every other score reaches June |
| 2349's allocation grew 5→21→29→43→87 while its cut-off fell 95→90→90→85→80 | A growing allocation reaches deeper into a small pool |
| Late-submitted EOIs had *higher* invitation rates at a given score | Composition: the old residue at a score is concentrated in groups whose allocation never reaches it |

## Residual

**13 of 58 rationed cells sit above their group's lowest invited score**, which strict points-then-date forbids.

Cause: **submission month is not date of effect.** An EOI whose points changed keeps its old submission month but
takes a fresh date of effect, so the exhaustion probe misreads it as an un-invited early applicant.

Confirmed directly in 2349's 85-point cell: it fell from 10 to 1 across the Jun-2026 round, then refilled to 13 by
August — including a 2024-submitted EOI absent from both the June and July snapshots, which can only have re-entered
at 85 points with a 2026 date of effect.

This residual does not affect the applicant's case: every EOI in the 08/2026 snapshot has a date of effect on or
before 31 Aug 2026, hence still ahead of a 10 Sep lodgement. It does mean per-cell date comparisons carry
measurement error, and the expiry clock runs from **submission** date, not date of effect.

## A rejected alternative

The official results look like priority tiers (trades 65, healthcare 75, professional 80). They are not: Sonographer
(85) splits from Medical Diagnostic Radiographer (80), Metal Machinist (85) from Metal Fabricator (80), and Musician
(Instrumental) (80) sits beside Barrister and Petroleum Engineer. No coherent priority schedule produces that. The
allocation-plus-ranking rule does, and it is estimable from this data whereas a tier schedule is not.
