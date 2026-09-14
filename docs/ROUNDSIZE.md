# Predicting the size of the next round

The model treated round size as unknowable and reported probability conditional on it. That was honest but
incomplete — the size is not *arbitrary*, it is constrained by published places and observed cadence. This is
the model, and its limits.

## Construction

**1. The annual invitation budget.** The 2026–27 program funds **21,090** Skilled Independent places. Across
2025–26 the Department issued **26,024** invitations against **16,900** places — **1.54 invitations per place**,
since not every invitation becomes a visa. Applying that rate: **≈32,476 invitations** for 2026–27.

**2. How many rounds it is split into.** Three in 2025–26 (the only complete program year in the panel); two
visible in 2024–25, though the panel starts in September 2024 so that year may be clipped. Prior used:
**2: 0.25, 3: 0.55, 4: 0.20** — weighted toward the observed three, with four allowed because a larger program
can be split further.

**3. Within-year variation.** Rounds in a year are not equal. The 2025–26 rounds were 6,450 / 9,826 / 9,748
against a mean of 8,675 — shape factors **0.74, 1.13, 1.12**. Each `budget ÷ n` case is spread by these.

## Result

| | invitations |
|---|---|
| mean | 11,637 |
| 10th percentile | 6,403 |
| median | 12,090 |
| 90th percentile | 17,050 |

| | probability |
|---|---|
| P(round ≥ 6,450 — the smallest on record) | 93% |
| P(round ≥ 10,000) | 62% |
| P(round ≥ 14,724 — the largest on record) | 17% |

## Marginalising

With a distribution over size, the dashboard's headline no longer rests on any assumed round:

```
P(invited) = Σ P(size) × P(cut-off reaches your score | size)
```

For a physicist on 85 points this gives **92%**, against 94% at the central case — slightly lower, because the
distribution carries real weight on small rounds. Both are **still conditional on a round being held.**

## What this model is not

It is built on **one complete program year**. The rounds-per-year prior is a judgement informed by two years of
partial evidence, not a measured frequency, and it is the largest single assumption in the whole project — stated
here rather than buried. It assumes the 2025–26 invitations-per-place rate carries forward, and that the
Department splits the year's budget in the pattern it did last year.

It cannot predict **whether a round is held at all**, or a ministerial direction that re-weights occupations
mid-programme. A reader who disagrees with the rounds-per-year prior can read their own answer straight off the
probability curve, which is plotted against round size precisely so the marginal is never the only number on offer.
