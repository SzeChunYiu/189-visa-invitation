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

## What the policy change actually was

The switch is not invisible. An **internal Department of Home Affairs policy paper dated May 2025, released
under FOI**, sets out a **four-tier occupation priority model** for subclass 189. It was never published by the
Department and is, in the source's words, *"not legislation — it is an internal planning tool."*

| Tier | Basis | Examples |
|---|---|---|
| 1 — highest | scarcity, long training, long-term demand | medical specialists, GPs, nurses, midwives, physiotherapists |
| 2 — high | government priority under Ministerial Directions | early childhood / secondary / special-ed teachers, psychologists, social workers |
| 3 — medium | maintain a broad skills mix | engineers, architects, scientists, trades, lawyers, vets, lecturers |
| 4 — lowest | **oversupplied occupations with high EOI volumes** | accountants, auditors, ICT, telecommunications, **chefs** |

### Tested against data the tier model never saw

Tiers were assigned from ANZSCO structure *before* looking at outcomes:

| Tier | Groups | People waiting | Invitations 2025–26 | **Per 1,000 waiting** |
|---|---|---|---|---|
| 2 | 5 | 16,982 | 1,990 | **117** |
| 3 | 62 | 72,077 | 6,567 | **91** |
| 4 | 9 | 74,056 | 96 | **1.3** |

Monotone in the predicted direction, and χ² for tier × gets-nothing = **21.9, p = 0.00007**. Seven of nine
Tier 4 groups received zero. The list of excluded occupations in my data — Software, ICT Business Analysts,
Accountants, Auditors, Network Professionals, Database/ICT Security, **Chefs** — is Tier 4 almost exactly.

### Where it does not fit, and a hypothesis I rejected

The big **engineering** groups are Tier 3 yet received zero: Civil (11,073 waiting), Industrial/Mechanical
(9,076), Other Engineering (8,782), Electrical (4,366). Meanwhile smaller Tier 3 groups did well — Carpenters
1,124 invitations, Solicitors 463, Veterinarians 131.

The FOI paper offers its own explanation: ceilings are *"managed across the entire skilled program"*, with 186,
190 and 491 grants counting toward a group's ceiling before 189 invitations issue. If so, groups with heavy
state-nominated demand should be squeezed out.

**Tested and rejected.** The state-to-189 pool ratio is ~4.3–5.3 for skipped and invited groups alike
(Mann-Whitney p = 0.74 overall, p = 0.83 within Tier 3; correlation −0.14). Every engineering group has a ratio
near 4.9 whether it got 0 or 252 invitations.

What *does* separate them within a tier is raw size: **corr(log 189 pool, gets nothing) = +0.68 within Tier 3**.
So the "oversupplied, high EOI volume" criterion appears to act as a **continuous filter**, not merely a tier
label — the tier is coarse, and within it the largest pools are suppressed too.

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

The tier model is an **internal planning tool released under FOI, not legislation**, and is known here through a
secondary summary rather than the primary document — I could not retrieve the FOI release itself
(homeaffairs.gov.au returns 403 to automated fetching). What is independently verified is that the invitation
data matches its predicted ordering at p = 0.00007, which is strong but is a fit to an externally reported
model, not proof the Department applies it as described.

Its within-tier behaviour is **not** as the paper describes: the program-wide ceiling mechanism it cites fails
to explain which Tier 3 groups are skipped, while pool size does.

Sources: the tier model as summarised by
[Ethos Migration Lawyers](https://ethosmigration.com.au/understanding-the-occupation-tier-system-for-sc189-invitations/)
from a May 2025 FOI release; tier composition cross-checked against invitation patterns reported by
[Phoenix Law](https://www.phoenix-law.com.au/subclass-189-skilled-independent-visa-important-updates/).
