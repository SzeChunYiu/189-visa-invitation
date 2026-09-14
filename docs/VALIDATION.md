# Validation

Three independent checks. None of the external figures were used to build the model.

## 1. External — per-occupation cut-offs vs the official round

The Department published per-occupation minimum points for the **4 June 2026** round. Cut-offs derived here come
from raw EOI records and never saw that table.

| Occupations cross-checked | Exact | Within ±5 pts | r | MAE | Bias |
|---|---|---|---|---|---|
| 124 | 112 (**90.3%**) | 123 (99.2%) | 0.9755 | 0.52 pts | **+0.52 pts** |

**Physicist (234914): derived 80, official 80.** Metallurgist: 80 / 80.

**The bias is one-sided.** All 12 disagreements are positive (+5 ×11, +10 ×1); none negative. This is the signature
of the single-leg filter — where the marginal invitee was a multi-leg EOI, the derived cut-off lands one tier high.
**The method cannot overstate a candidate's odds.**

## 2. External — round size vs the official total

DiD-attributed round size for Jun-2026: **9,761**. Official: **10,000**. Error **2.4%**.
This validates the difference-in-differences correction described in [METHODOLOGY.md](METHODOLOGY.md).

## 3. Internal — out-of-sample mechanism backtest

Rank each occupation's pool by points, allocate top-down, read the cut-off where invitations run out.
Tested on Jun-2026 for every occupation with ≥5 invitations: **49/49 within ±5 points**, 43% exact, r = 0.941.
Conservation check: per-occupation invitations sum exactly to each round total (residual 0).

## Questions the data settled

**The tie-break date does not exclude a recent EOI.** June 2026's tie-break was April 2026, which appears fatal for a
10 Sep lodgement. It is not: **20.2% of invitations at 90+ points went to EOIs dated after the tie-break**. The date
binds only at the marginal position within a score.

**The published tie-break describes the national floor.** Of every score invited in Jun-2026, only **65 points**
stops at April 2026; every other score reaches June. That closes the apparent mismatch between the published
tie-break and the observed rationing dates.

**EOIs expire on a hard two-year cliff.** Cohort survival: 95.7% (0–6 months), 87.1% (6–12), 82.0% (12–18),
77.2% (18–24), then **0.8% beyond 24 months**.

**The occupation ceiling is not binding for 2349.** Annual ceiling 500 (FY2025-26); the largest observed round used 87.

## Not examined

`HOLD` status, and reconciliation of the seven atomic point components against `Score`. Both are data-integrity
checks with no path to the invitation question. `LODGED` cross-validation was made redundant by the official total.

## Sources

- Home Affairs SkillSelect round results, 4 Jun 2026, as republished by
  [ahclawyers.com](https://www.ahclawyers.com/news-articles/26/06/25/skillselect-invitation-round-results-subclass-189-4-june-2026)
  and [studynash.co](https://www.studynash.co/blog/189-invitation-round-june-2026-scores-explained).
  homeaffairs.gov.au returned HTTP 403 to automated fetch, so these are secondary sources; the
  "next round expected by 30 September 2026" date is a paraphrase, **not** a verified departmental commitment.
- Occupation ceilings FY2025-26 via [immitrend.com.au](https://immitrend.com.au/occupation-ceilings).
