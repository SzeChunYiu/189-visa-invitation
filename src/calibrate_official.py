"""External calibration: derived Jun-2026 cut-offs vs the official Home Affairs per-occupation table."""
import pandas as pd, numpy as np, json, pathlib, os, re
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
off=json.load(open("official_jun2026.json"))
occ=pd.read_csv("cutoff_by_occupation.csv")
occ["name"]=occ.occupation.str.replace(r"^\d+\s+","",regex=True).str.strip()
norm=lambda s:re.sub(r"[^a-z0-9]","",s.lower())
mine={norm(r["name"]):(r["occupation"],r["2026-06"],r["2026-06_n"]) for _,r in occ.iterrows()}
rows,miss=[],[]
for sc,names in off["scores"].items():
    for nm in names:
        k=norm(nm); m=mine.get(k)
        if m is None: miss.append(nm); continue
        code,derived,n=m
        if pd.isna(derived): miss.append(nm+" (no derived cut-off)"); continue
        rows.append(dict(occ=code,official=int(sc),derived=int(derived),n=int(n),err=int(derived)-int(sc)))
d=pd.DataFrame(rows)
print("="*92); print("EXTERNAL CALIBRATION - derived cut-off vs official Home Affairs figure, 4 Jun 2026"); print("="*92)
print(f"  official occupations listed : {sum(len(v) for v in off['scores'].values())}")
print(f"  matched to derived cut-offs : {len(d)}")
print(f"  unmatched (name/no invite)  : {len(miss)}")
print(f"\n  EXACT match        : {(d.err==0).sum():>3} / {len(d)}  ({100*(d.err==0).mean():.1f}%)")
print(f"  within +/-5 points : {(d.err.abs()<=5).sum():>3} / {len(d)}  ({100*(d.err.abs()<=5).mean():.1f}%)")
print(f"  mean signed error  : {d.err.mean():+.2f} pts     MAE = {d.err.abs().mean():.2f} pts")
print(f"  correlation        : r = {np.corrcoef(d.derived,d.official)[0,1]:.4f}")
print("\n  error distribution:")
for e,c in d.err.value_counts().sort_index().items(): print(f"    {e:+3d} pts : {c:>3}  {'#'*int(40*c/len(d))}")
print("\n  every disagreement:")
bad=d[d.err!=0].sort_values("err")
print(bad.to_string(index=False) if len(bad) else "    none")
print("\n  --- physics stratum (ANZSCO 2349) ---")
print(d[d.occ.str.startswith("2349")].to_string(index=False))
d.to_csv("calibration_official.csv",index=False)
json.dump(dict(n=int(len(d)),exact=int((d.err==0).sum()),within5=int((d.err.abs()<=5).sum()),
  mae=round(float(d.err.abs().mean()),2),bias=round(float(d.err.mean()),2),
  r=round(float(np.corrcoef(d.derived,d.official)[0,1]),4),
  official_total=off["total_invitations"],tie_break=off["tie_break_date"],next_round=off["next_round_expected"]),
  open("calibration_official.json","w"),indent=1)
print("\n  -> calibration_official.csv/.json written")
