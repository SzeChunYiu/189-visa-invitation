# Data source and inventory

## Source

Department of Employment and Workplace Relations, SkillSelect EOI dashboard.
Qlik Sense mashup; data read directly from the **Qlik Engine JSON API** over an anonymous
websocket — no login required.

```
wss://api.dynamic.reports.employment.gov.au/anonap/app/aaac76b5-ad30-477e-9ca0-472f8ab57fc8
```

`src/qlik.py` opens the session (`OpenDoc`, handle −1); `src/hc.py` builds hypercubes,
pages them, and asserts `len(rows) == qSize.qcy` so truncation cannot pass silently.

## Data model

| Table | Rows | Role |
|---|---|---|
| `EOI State Visa Points Table NoLimits` | 19,556,923 | Fact table — one row per EOI × visa × state × points-version × validity interval |
| `EOIAsAtBridge` | 34,542,338 | Maps EOI versions to monthly snapshots |
| `AsAtMonthFilterList` | 24 | Snapshots, 09/2024 → 08/2026 |
| `VisaTypeList` | 9 | Visa subclasses |

## Fields used

| Field | Notes |
|---|---|
| `%EOIID` | Hidden; **cannot be used as a dimension**, only inside `Count(distinct …)` and set expressions |
| `Score` | Total points for that visa leg. 189 and 190 legs of one EOI differ by 5 |
| `EOI Status` | SUBMITTED / INVITED / LODGED / HOLD / CLOSED — **EOI-level, see METHODOLOGY trap 1** |
| `%StatusDate` | When the current status was set; inside the row-version's interval 99.4% of the time |
| `Occupation` / `Occupation Group` | 495 occupations / 206 ANZSCO unit groups |
| `Nominated State` | `N/A` for 189 legs; a state for 190/491 legs |
| `English Test Score`, `PartnerSkills Score`, `Australian Study Flag`, `Regional Study`, `Comm Language Qual`, `Specialist Education`, `Professional Year` | Point components. Addends of `Score` — carry no independent ranking signal for 189 |

## Extracted files (`data/`)

| File | Grain |
|---|---|
| `inv189only_occ4_score.csv` | status month × occupation × score — **the true 189 rounds** |
| `inv189only_occ_score.csv` | status month × unit group × score |
| `pool189only_occ4.csv` | snapshot × occupation × score, single-leg SUBMITTED pool |
| `pool189_occ_score.csv` | snapshot × unit group × score, full SUBMITTED pool |
| `queue189_full.csv` | score × submission month at 08/2026 (queue position proxy) |
| `cutoff_by_occupation.csv` | **per-occupation cut-off per round + current pool** — the reusable table |
| `panel_status_{189,190,491}.csv` | snapshot × status stock for all three subclasses |
| `model_hazards.json`, `model_final.json` | Model outputs |

## Snapshot coverage caveat

The 189 SUBMITTED pool grows 21,683 → 180,651 across the panel. Coverage effectively begins
Sep-2024; almost no EOI in the current pool has a submission month before then. Early snapshots
therefore understate the true standing pool, and pre-2025 hazards should be read as lower bounds.
