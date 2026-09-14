# Policy inputs

The model treats round occurrence and round size as **exogenous** — they are set by migration planning
levels, not by the EOI pool. Those levels are published, so they can at least be read in.

## 2026–27 Migration Program planning levels

| Category | 2025–26 | 2026–27 | Change |
|---|---|---|---|
| **Skilled Independent (189)** | 16,900 | **21,090** | **+24.8%** |
| State/Territory Nominated (190) | 33,000 | 35,500 | +7.6% |
| Regional (491) | 33,000 | **14,110** | **−57.2%** |
| Employer Sponsored | 44,000 | 58,040 | +31.9% |

Total program unchanged at 185,000.

## Translating places into round size

Across the 2025–26 program year the three rounds (Aug-2025, Nov-2025, Jun-2026) issued **26,024**
invitations against **16,900** places — **1.54 invitations per place**, since not every invitation becomes
a visa.

Applying that ratio to 2026–27:

- implied invitations: **32,476**
- at 2 rounds: 16,238 each · at **3 rounds: 10,825** each · at 4 rounds: 8,119 each

Three rounds a year is the observed cadence, so ~10,800 per round is the central expectation — which is why
the dashboard defaults to the 10,000 scenario.

## The Regional cut is the main unmodelled risk

491 lost 57% of its places. This does **not** enter the model directly, but it is the clearest channel by
which the 189 pool could grow faster than it has: applicants who would have aimed regional have far fewer
places to aim at, and some will redirect to 189. The model reads the pool from the monthly panel, so any
such surge shows up in later snapshots rather than being anticipated here. Re-run
`src/build_bundle.py` against a fresh extract once new snapshots land.

## What is still not observable

Ministerial direction on occupation priority, and whether a round is scheduled at all. Neither appears in
the published planning levels or in the EOI panel. The structural-break test in
[CONSISTENCY.md](CONSISTENCY.md) detects *that* a regime changed (2024-11 → 2025-08, share cosine 0.53
against 0.92–0.95 for recent transitions) but not why.

## Sources

- 2026–27 planning levels as published by the Department of Home Affairs and reported by
  [Work Visa Lawyers](https://www.workvisalawyers.com.au/news/all/australia-s-2026-27-permanent-migration-program-planning-levels-understanding-the-australian-visa-numbers-and-permanent-residency.html)
  and [VisaEnvoy](https://visaenvoy.com/migration-program-planning-levels/).
- Invitation counts are this repo's own DiD-corrected figures, validated against the official
  4 Jun 2026 total (9,748 derived vs 10,000 official).
