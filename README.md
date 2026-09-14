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

**4. For an 85-point physicist:** P(invited | a round is held) ≈ **77%**.
The binding uncertainty is round *occurrence*, which this data cannot predict.

## Reproduce

```bash
pip install -r requirements.txt
python src/step3_core.py && python src/step4.py && python src/step5_occ.py && python src/step6.py
python src/model.py && python src/model2.py && python src/cutoff_table.py
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

Not migration advice.
