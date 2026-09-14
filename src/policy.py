"""Translate published planning levels into an expected round size."""
import json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
PLACES={"2025-26":16900,"2026-27":21090}
# all-leg 189 invitations by round (DiD-corrected; Jun-2026 validated at 9,748 vs 10,000 official)
INV={"2024-09":7735,"2024-11":14724,"2025-08":6450,"2025-11":9826,"2026-06":9748}
PY2025_26=["2025-08","2025-11","2026-06"]      # program year Jul 2025 - Jun 2026
PY2024_25=["2024-09","2024-11"]                # partial: panel starts Sep 2024
tot=sum(INV[r] for r in PY2025_26)
ratio=tot/PLACES["2025-26"]
print("="*96); print("POLICY INPUT - published planning levels -> expected round size"); print("="*96)
print(f"  2025-26 program year rounds : {', '.join(PY2025_26)}")
print(f"  invitations issued          : {tot:,}  ({'+'.join(f'{INV[r]:,}' for r in PY2025_26)})")
print(f"  places in the 189 program    : {PLACES['2025-26']:,}")
print(f"  invitations per place        : {ratio:.2f}x   (not every invitation becomes a visa)")
print(f"\n  2026-27 places               : {PLACES['2026-27']:,}  (+{100*(PLACES['2026-27']/PLACES['2025-26']-1):.1f}%)")
proj=PLACES["2026-27"]*ratio
print(f"  implied invitations 2026-27  : {proj:,.0f}")
for n in (2,3,4):
    print(f"    across {n} rounds           : {proj/n:>7,.0f} per round")
print(f"\n  The last three rounds averaged {tot/3:,.0f}. A 24.8% larger program at the same cadence implies")
print(f"  roughly {proj/3:,.0f} per round - which is why 10,000 is the dashboard's default scenario.")
print(f"\n  Regional (491) was cut 33,000 -> 14,110 (-57%). That does NOT enter the model directly, but it is")
print(f"  the clearest channel by which the 189 pool could grow faster than it has: applicants who would have")
print(f"  gone regional have fewer places to aim at. The model reads the pool from the panel, so a surge would")
print(f"  show up in the next snapshots rather than being predicted here.")
json.dump(dict(places=PLACES,ratio=round(ratio,3),projected_invitations=round(proj),
  inv_by_round=INV, py={"2025-26":PY2025_26,"2024-25":PY2024_25},
  inv_2025_26=tot,
  per_round={str(n):round(proj/n) for n in (2,3,4)},
  regional_cut={"2025-26":33000,"2026-27":14110},
  nominated={"2025-26":33000,"2026-27":35500},
  employer={"2025-26":44000,"2026-27":58040}),open("policy.json","w"),indent=1)
print("\n  -> policy.json written")
