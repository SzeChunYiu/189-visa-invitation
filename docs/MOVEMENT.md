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

## Where this shows on the page

As a single stacked strip above the probability curve: how often the cut-off falls, holds, or rises, with the
"rises 10+" share and the "70% of boundary bands leave someone behind" figure called out. One graphic, four
facts, no extra card.
