# How the cut-off moves

Three questions the model could not previously answer: does the cut-off step or jump, does landing on
your band get you in, and what actually moves it.

## Does it step, or jump?

Change in a unit group's cut-off between consecutive rounds (current-regime rounds, n = 159):

| Change | Share |
|---|---|
| falls 10 or more | 6% |
| falls 5 | 37% |
| **no change** | **32%** |
| rises 5 | 16% |
| rises 10 or more | 10% |

**It steps.** 32% do not move at all, 53% move by exactly one 5-point band, and **15% move 10 points or
more** in either direction. Mean absolute change **4.6 points**.

So the answer to "what's the chance it suddenly jumps 10 points?" is about **one in seven**, and rises are
less common than falls — the cut-off has been drifting down as allocations grew.

## If it lands on your band, do you get in?

**No, usually not automatically.** Of 179 boundary cells in the current-regime rounds:

- **30%** were fully CLEARED — everyone in that band invited
- **70%** were PARTIAL — the allocation ran out inside the band and some were left behind on date of effect

This is why the dashboard asks for your date of effect, and why it assumes you are **last in the band** when
you do not give one.

## What moves it?

| Against the change in a group's cut-off | Correlation |
|---|---|
| log change in **allocation** (invitations to that group) | **−0.72** |
| log change in **pool** (people waiting) | **+0.60** |

More invitations push the cut-off down; more competitors push it up. Both are mechanical and both are already
inside the model.

**There is no "news" channel.** The model has no input for announcements, media coverage or sentiment — only
places and people. A policy announcement matters only once it changes one of those two, which shows up in a
later snapshot. The one exception already modelled is published planning levels, which set the annual
invitation budget ([POLICY.md](POLICY.md)).

## Can the cut-off fall to 80 and still not invite you?

**Yes — and it was not priced until now.** Two separate failures can leave you uninvited even when the score
looks fine:

1. **No round is held.** Exogenous, unpredictable, and every figure on the page is explicitly conditional on it.
2. **A round is held but your occupation group gets nothing.** This turns out to be common.

Across the current-regime rounds, **31% of unit groups that had people waiting received zero invitations.**

And it is not random. Of 86 groups with a pool in all three recent rounds:

| Missed out in | Groups | Expected if independent |
|---|---|---|
| 0 of 3 rounds | **49** | 28 |
| 1 of 3 | 13 | 38 |
| 2 of 3 | 6 | 17 |
| 3 of 3 | **18** | 3 |

χ² = 130.8 on 3 df, p < 0.0001 — **strongly clustered**. The same groups keep getting nothing.

The dominant predictor is simply last round:

| | P(zero next round) |
|---|---|
| Got nothing last round | **76%** |
| Got something last round | **8%** |

Counter-intuitively, **bigger pools are more likely to be skipped** (42% vs 14% below median) — the large
oversupplied groups such as ICT and accounting are the ones left out.

The headline probability is now multiplied by `(1 − P(skipped))`. For ANZSCO 2349, which received invitations
in all three recent rounds, that is an 8% discount: **84% → 77%**. For a group like 2613 Software and
Applications Programmers, which got nothing last round, the risk is **76%** and no forecast is offered at all.

## Where this shows on the page

As a single stacked strip above the probability curve: how often the cut-off falls, holds, or rises, with the
"rises 10+" share and the "70% of boundary bands leave someone behind" figure called out. One graphic, four
facts, no extra card.
