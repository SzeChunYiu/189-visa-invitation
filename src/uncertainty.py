"""Calibrated prediction intervals from the out-of-sample residual distribution."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
o=pd.read_csv("validation_oos_singleleg.csv")
o["err"]=o.pred-o.actual                       # err>0 => forecast sat ABOVE the truth
recent=o[o["round"].isin(["2025-11","2026-06"])]      # folds from the current regime
print("="*96); print("OUT-OF-SAMPLE RESIDUALS  err = forecast - actual  (positive = forecast too high)"); print("="*96)
for lbl,z in [("all folds",o),("current-regime folds (Nov-25, Jun-26)",recent)]:
    q=z.err.quantile([.05,.1,.25,.5,.75,.9,.95])
    print(f"\n  {lbl}: n={len(z)}  mean={z.err.mean():+.2f}  sd={z.err.std():.2f}")
    print("   " + "  ".join(f"p{int(k*100)}={v:+.1f}" for k,v in q.items()))
    print(f"   P(|err|<=5) = {(z.err.abs()<=5).mean():.0%}    P(err==0) = {(z.err==0).mean():.0%}")
R=recent.err.values
lo80,hi80=np.percentile(R,10),np.percentile(R,90)
lo50,hi50=np.percentile(R,25),np.percentile(R,75)
print(f"\n  80% interval on the TRUTH given a forecast f:  [f-{hi80:.0f}, f-{lo80:.0f}]")
print(f"  50% interval:                                  [f-{hi50:.0f}, f-{lo50:.0f}]")

def p_at_or_below(fc,pts,res=R):
    """P(actual cut-off <= pts) = P(err >= fc - pts), empirical."""
    return float((res>=(fc-pts)).mean())
print("\n"+"="*96); print("CALIBRATED PROBABILITY  P(cut-off lands at or below your score)"); print("="*96)
print(f"  {'forecast':>9} " + "".join(f"{p:>8}" for p in [65,70,75,80,85,90,95]))
for fc in [95,90,85,80,75,70]:
    print(f"  {fc:>9} " + "".join(f"{p_at_or_below(fc,p):>8.0%}" for p in [65,70,75,80,85,90,95]))
print("\n  Read a row as: given this forecast cut-off, the chance the real cut-off falls at or below each score.")
print("  Derived purely from how wrong the same method was on the two most recent held-out rounds.")

B=json.load(open("bundle.json"))
g=B["groups"]["2349"]
print("\n"+"="*96); print("APPLIED: ANZSCO 2349 at 85 points"); print("="*96)
print(f"  {'round size':>11}{'forecast':>10}{'80% interval':>18}{'P(cut-off <= 85)':>19}")
for i,S in enumerate(B["sizes"]):
    fc=g["fc"][i]
    if fc is None: continue
    print(f"  {S:>11,}{fc:>10}{f'[{fc-hi80:.0f}, {fc-lo80:.0f}]':>18}{p_at_or_below(fc,85):>19.0%}")
json.dump(dict(n=int(len(recent)),mean=round(float(recent.err.mean()),2),sd=round(float(recent.err.std()),2),
  lo80=float(lo80),hi80=float(hi80),lo50=float(lo50),hi50=float(hi50),
  residuals=[int(x) for x in sorted(R)]),open("uncertainty.json","w"),indent=1)
print("\n  -> uncertainty.json written")
