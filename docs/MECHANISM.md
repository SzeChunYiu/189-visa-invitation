# The mechanism, tested

Three questions the model previously answered with correlation rather than cause.

## 1. Is a round band-dependent or number-dependent?

**Number-dependent.** A count walks down the ranking and stops mid-band.

| | Fully taken |
|---|---|
| Bands **above** the lowest invited score | **94.5%** |
| The **lowest** invited band | **28.8%** |

Median share of the lowest band taken: **0.81**. And if rounds handed out whole bands, the allocation would
land exactly on a cumulative band boundary every time; it does so in only **25%** of 179 group-rounds, with a
median miss of 5 invitations.

So: everything above the margin goes in its entirety, and the margin itself is a partial cut settled by date of
effect. That is exactly why a date matters at the boundary and nowhere else.

## 2. Why do some groups get nothing? It is a switch, not a ceiling

**14 occupation groups were switched off at the 2024-25 → 2025-26 program-year boundary.** They hold
**108,648 people — 60% of the entire 189 pool** — and have received zero invitations in all three rounds since.

| Group | Waiting | Sep 24 | Nov 24 | Aug 25 | Nov 25 | Jun 26 |
|---|---|---|---|---|---|---|
| 2613 Software and Applications Programmers | 25,865 | 166 | 743 | **0** | **0** | **0** |
| 2611 ICT Business and Systems Analysts | 13,069 | 52 | 339 | **0** | **0** | **0** |
| 2211 Accountants | 11,173 | 150 | 450 | **0** | **0** | **0** |
| 2332 Civil Engineering Professionals | 11,073 | 490 | 622 | **0** | **0** | **0** |
| 3513 Chefs | 10,982 | 4 | 56 | **0** | **0** | **0** |

**Not a ceiling.** A binding ceiling caps a group after it reaches its quota; these groups receive *nothing at
all* while holding thousands of people. Ceilings cap. This is a switch.

**Not pool size either.** Registered Nurses hold **14,453** people and were invited throughout — and rising
(311 → 822 → 915 → 1,377 → 1,393). Pool size alone predicts exclusion at only **AUC 0.65**. The rule is
occupation identity, not crowding.

**The timing matches the structural break already measured.** [HYPOTHESES.md](HYPOTHESES.md) found exactly one
regime change, at the 2024-11 → 2025-08 transition (share cosine 0.53 and 38% turnover, against 0.92–0.95 and
16–17% for the recent transitions). That break *is* this switch.

### What this explains

- Why 31% of groups with a pool get zero in any given round.
- Why the cut-off has been **falling** for the groups that remain: 60% of the pool was removed from
  competition, so the same invitation budget reaches further down the remaining occupations.
- Why ANZSCO 2349's allocation grew 17× across five rounds. **It did not become more favoured — its
  competitors were removed.** That is a materially different reading of the trend this project leaned on
  earlier, and the more honest one.

## 3. Is it dynamic?

Within a round, no: invitations run strictly points-then-date, and the only dynamic element is where the count
stops. Between rounds, yes — but the dynamics are mechanical, not sentimental:

| Against the change in a group's cut-off | Correlation |
|---|---|
| log change in allocation | **−0.72** |
| log change in pool | **+0.60** |

There is no channel for news or announcements. A policy decision matters only when it changes the allocation or
the pool — and when it does, as in 2025, it does so abruptly and visibly.

## Limits

The switch is inferred from the invitation data, not read from a published instrument. The Department has not
been observed here stating which occupations are excluded; what is observed is that 14 groups stopped receiving
invitations simultaneously at a program-year boundary. Whether that reflects a ministerial direction, a revised
occupation list, or an internal priority setting is **not determinable from this data**.
