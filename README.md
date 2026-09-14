# 189-visa-invitation

A quantitative queue model for **Australian subclass 189 (Skilled Independent)** invitation rounds,
built from the complete 24-month panel behind the public SkillSelect EOI dashboard.

**Interactive explorer → [SzeChunYiu.github.io/189-visa-invitation](https://SzeChunYiu.github.io/189-visa-invitation/)**
Pick any of 199 occupations, enter your points, and see your position, the round-by-round record, and a
forecast for the next round on one page. The written analysis lives at
[findings.html](https://szechunyiu.github.io/189-visa-invitation/findings.html).
Deployment notes (incl. Vercel): [DEPLOY.md](DEPLOY.md).

---

## Read in this order

| File | What it holds |
|---|---|
| **README.md** (this file) | Headline results and how to reproduce |
| [docs/THEORY.md](docs/THEORY.md) | The one mechanism that explains every observation |
| [docs/MOBILITY.md](docs/MOBILITY.md) | Points upgrades, date of effect, and queue position |
| [docs/METHODOLOGY.md](docs/METHODOLOGY.md) | The three data traps and how each was defeated |
| [docs/MODEL.md](docs/MODEL.md) | Model spec, assumptions, and what it cannot do |
| [docs/VALIDATION.md](docs/VALIDATION.md) | External + internal validation, and open questions |
| [docs/CONSISTENCY.md](docs/CONSISTENCY.md) | The model run on every occupation in every round |
| [docs/DATA.md](docs/DATA.md) | Source, field dictionary, extraction inventory |

## Headline results

**1. There were five 189 rounds in 24 months**, not twenty-four:
Sep-2024, Nov-2024, Aug-2025, Nov-2025, Jun-2026. Every other month's apparent "189 invitations"
are 190/491 state nominations leaking through a status field shared across visa legs.

**2. Every cut-off resolves into three states**, not one number — `CLEARED` (invited regardless of EOI date),
`PARTIAL` (rationed by date of effect), `UNTOUCHED`. [`data/occupation_database.csv`](data/occupation_database.csv)
carries one row per occupation × round on this definition, 637 rows over 181 occupations.
For Physicist, both Nov-2025 and Jun-2026 are `CLEARED` at the boundary — an 85-point physicist would have been
invited in either **regardless of their EOI date**.

**3. There is no single national 189 cut-off.** Every round invites someone at 65 points.
Rounds are stratified by ANZSCO unit group; in Jun-2026 the per-occupation minimum invited score
ranged from **65 to 100**.

**4. The physics stratum (ANZSCO 2349) cut-off has fallen monotonically:**

| Round | Sep 2024 | Nov 2024 | Aug 2025 | Nov 2025 | Jun 2026 |
|---|---|---|---|---|---|
| 2349 cut-off | 95 | 90 | 90 | **85** | **80** |
| Invitations to 2349 | 3 | 11 | 15 | 24 | 35 |
| National floor | 65 | 65 | 65 | 65 | 65 |

**5. The model reduces to one threshold.** An 85-point physicist sits at **rank 32** in unit group 2349
(11 above 85 points, 20 at 85 with earlier dates). They are invited iff the next round allocates ≥32 invitations
to 2349. Allocation history: **5 → 21 → 29 → 43 → 87** — the last two rounds clear it, the first three do not.

P(invited | a round is held) = **40–77%**, stable across round timing. Only the two largest allocations 2349
has ever received (43, 87) clear rank 32; the three smaller ones (5, 21, 29) do not. The binding uncertainty is
round *occurrence* and *size*; the downside risk is a policy cut to this stratum, not the applicant's score.

**8. Nearly half the pool re-scores.** 47.3% of 189 EOIs changed score over their life (mean +8.0 points), and
43% of everyone now at 85+ acquired those points within six months. A points change **resets the date of effect**,
so upgraders join the back of their new band — which is why a lodged position stops eroding. All 31 EOIs ahead in
2349 were verified to hold a date of effect before 10 Sep 2026.

**6. Consistent across occupations and time — where the panel is complete.** Run on all 82 unit groups in all
five rounds (315 group-rounds), the mechanism is **83% exact with MAE 0.95 points** on the three rounds with
adequate panel coverage, and fails on the two 2024 rounds when only 12–20% of the eventual pool had been
captured. Correlation between panel coverage and error: **−0.962**. Out of sample (allocation forecast from the
prior round): **91% within ±5 points, MAE 3.84** on the latest fold. See [CONSISTENCY.md](docs/CONSISTENCY.md).

**7. Validated against the official round results.** Derived per-occupation cut-offs match the Department's
published 4 June 2026 table on **112 of 124 occupations exactly (90.3%)**, 99.2% within ±5 points, r = 0.9755.
Physicist: derived 80, official 80. Every disagreement is positive, so the method cannot overstate a
candidate's odds. Round size: 9,761 derived vs 10,000 official (2.4%). See [VALIDATION.md](docs/VALIDATION.md).

## Reproduce

```bash
pip install -r requirements.txt
python src/step3_core.py && python src/step4.py && python src/step5_occ.py && python src/step6.py
python src/model.py && python src/model2.py && python src/cutoff_table.py
python src/global_model.py && python src/calibrate_official.py && python src/forward_model.py
python src/saturation_model.py && python src/alloc_all.py && python src/universal_validation.py
python src/forecast_all.py && python src/build_database.py
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
| `src/forward_model.py` | Applies the validated mechanism to the next round, with EOI expiry |
| `src/calibrate_official.py` | Cross-checks derived cut-offs against the official round table |
| `src/step8_tiebreak.py` | Tests whether the tie-break date binds at every score |
| `src/step9_queue.py` | Queue by submission month + cohort survival for the expiry model |
| `src/step10_saturation.py` | Newest/oldest submission date per cell, for the saturation test |
| `src/saturation_model.py` | Resolves every cell into CLEARED / PARTIAL / UNTOUCHED |
| `src/build_database.py` | Builds the coherent per-occupation database |
| `src/alloc_all.py` | Per-group allocation series + the forecastability gate |
| `src/universal_validation.py` | The model run on every group in every round |
| `src/forecast_all.py` | Per-occupation forecast cut-off by round size |
| `src/step11_dateofeffect.py` | Probes the SCD interval columns for the true date of effect |
| `src/step13_mobility.py` / `mobility_model.py` | Points-upgrade rates and their effect on queue position |

Not migration advice.
