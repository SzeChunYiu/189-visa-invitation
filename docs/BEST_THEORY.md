# The best theory, and what it is worth

## The theory

A 189 round runs in three stages.

**1. Inclusion — a tier filter.** An FOI'd Home Affairs paper (May 2025, never published) ranks occupations in
four priority tiers. Tier 4 — *"oversupplied occupations with high EOI volumes"* — is effectively switched off:
**1.3 invitations per 1,000 waiting, against 117 for Tier 2**. The filter is not purely the tier label: within
Tier 3 the largest pools are suppressed too (corr(log pool, gets nothing) = **+0.68**). Read it as a continuous
"oversupply" filter for which the tiers are a coarse summary.

**2. Allocation — a count per group, strongly persistent.** Each included group receives a number. That number
is highly autocorrelated round to round (share r = 0.92–0.96 on recent transitions).

**3. Distribution — points, then date, stopping mid-band.** Invitations run strictly down the points order.
Bands above the margin are taken whole (**94.5%** fully taken); the lowest band is a partial cut (**28.8%**
fully taken, median 81%). The allocation lands on a clean band boundary in only **25%** of group-rounds.

This explains every observation on record: why 31% of groups get nothing; why the cut-off steps by 5 rather
than jumping; why date of effect matters at the boundary and nowhere else; and why cut-offs have been falling
for the groups that remain — 60% of the pool was removed from competition, so the same budget reaches deeper.

**It corrects an earlier reading.** ANZSCO 2349's allocation grew 17×, which this project once read as growing
favour. It is not. Its competitors were removed.

## What the theory is worth as a predictor — tested, not assumed

Three models, each predicting a round's cut-offs from information available before it:

| Model | n | Exact | Within ±5 | MAE |
|---|---|---|---|---|
| **M0 persistence** (last round's split) | 155 | 47% | 85% | **3.74** |
| M1 tier × pool | 171 | 29% | 73% | 5.38 |
| M2 blend of the two | 159 | 50% | 89% | **3.21** |

On the latest fold alone (Jun-2026): M0 **3.21**, M2 3.75, M1 5.85.

And for predicting *who gets nothing* (86 groups):

| Predictor | Accuracy |
|---|---|
| assume everyone invited | 72% |
| Tier 4 alone | 78% |
| **got nothing last round** | **87%** |
| Tier 4 **or** nothing last round | 85% |

Among groups that got something last round, being Tier 4 adds nothing (0% of 2 went to zero, against 8% of 59).

## The honest conclusion

**The tier model does not improve the forecast. It improves the explanation.**

Persistence already carries the information — the tier and last-round-outcome encode the same exclusion. What
the tier adds is the *reason* persistence holds: without it, "these groups got nothing twice" is a two-point
coincidence; with it, it is a documented policy rule in force. That is what justifies projecting persistence
forward, and it is why the finding matters even though it does not move the numbers.

**So the operating model stays M0 persistence**, which wins within the current regime and is simpler.

**With one stated caveat.** M2's advantage is concentrated on the fold spanning the 2025 regime break, where
pure persistence fails and structure helps. If another tier revision lands, expect accuracy to degrade toward
M1's numbers. The blend is insurance against a break, not an improvement within one.
