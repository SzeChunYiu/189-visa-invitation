# 189-visa-invitation

A quantitative queue model for **Australian subclass 189 (Skilled Independent)** invitation rounds,
built from the complete 24-month panel behind the public SkillSelect EOI dashboard.

**Live dashboard → [SzeChunYiu.github.io/189-visa-invitation](https://SzeChunYiu.github.io/189-visa-invitation/)**

---

## Read in this order

| File | What it holds |
|---|---|
| **README.md** (this file) | Headline results and how to reproduce |
| [docs/METHODOLOGY.md](docs/METHODOLOGY.md) | The three data traps and how each was defeated |
| [docs/MODEL.md](docs/MODEL.md) | Model spec, assumptions, and what it cannot do |
| [docs/DATA.md](docs/DATA.md) | Source, field dictionary, extraction inventory |

## Headline results

**1. There were five 189 rounds in 24 months**, not twenty-four:
Sep-2024, Nov-2024, Aug-2025, Nov-2025, Jun-2026. Every other month's apparent "189 invitations"
are 190/491 state nominations leaking through a status field shared across visa legs.

**2. There is no single national 189 cut-off.** Every round invites someone at 65 points.
Rounds are stratified by ANZSCO unit group; in Jun-2026 the per-occupation minimum invited score
ranged from **65 to 100**.

**3. The physics stratum (ANZSCO 2349) cut-off has fallen monotonically:**

| Round | Sep 2024 | Nov 2024 | Aug 2025 | Nov 2025 | Jun 2026 |
|---|---|---|---|---|---|
| 2349 cut-off | 95 | 90 | 90 | **85** | **80** |
| Invitations to 2349 | 3 | 11 | 15 | 24 | 35 |
| National floor | 65 | 65 | 65 | 65 | 65 |

**4. The model reduces to one threshold.** An 85-point physicist sits at **rank 32** in unit group 2349
(11 above 85 points, 20 at 85 with earlier dates). They are invited iff the next round allocates ≥32 invitations
to 2349. Allocation history: **5 → 21 → 29 → 43 → 87** — the last two rounds clear it, the first three do not.

P(invited | a round is held) = **40%** unweighted (a floor that ignores the trend) to **77%** recency-weighted
(2^−age). The allocation trend is monotone increasing and argues above 77%. The binding uncertainty is round
*occurrence* and *size*, which this data cannot predict; the downside risk is a policy cut to this stratum,
not the applicant's score.

**5. The mechanism is validated out of sample.** Ranking each occupation's pool by points and allocating top-down
predicts the Jun-2026 cut-off **within ±5 points for 49 of 49 occupations** (r = 0.941, MAE 2.86, bias +2.9 pts —
real rounds go deeper than predicted, so the estimate is conservative).

## Reproduce

```bash
pip install -r requirements.txt
python src/step3_core.py && python src/step4.py && python src/step5_occ.py && python src/step6.py
python src/model.py && python src/model2.py && python src/cutoff_table.py
python src/global_model.py && python src/forward_model.py
python src/build_dashboard.py
```

Extraction talks to the Qlik Engine JSON API over an anonymous websocket — no credentials needed.
Every hypercube asserts `fetched rows == qSize.qcy`, so silent truncation fails loudly.

## Verification scripts

| Script | Proves |
|---|---|
| `src/test_overlap.py` | `EOI Status` is EOI-level; visa filters overlap ~50% |
| `src/test_only189.py` | Single-leg identification is exact (`all == only + multi`) |
| `src/test_suppress.py` | Engine returns exact sub-20 counts (complement differencing) |
| `src/test_drift.py` / `test_drift2.py` | `Score` on an INVITED row is the score at invitation |
| `src/global_model.py` | Out-of-sample backtest + conservation check + macro drivers |
| `src/forward_model.py` | Applies the validated mechanism to the next round |

Not migration advice.
