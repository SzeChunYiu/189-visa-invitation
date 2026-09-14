"""A distribution over the size of the next round, from published places and observed cadence."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
pol=json.load(open("policy.json"))
# observed all-leg round sizes, by program year (Jul-Jun)
PY2425=[7735,14724]            # Sep-2024, Nov-2024 (panel starts Sep 2024, so possibly incomplete)
PY2526=[6450,9826,9748]        # Aug-2025, Nov-2025, Jun-2026 - a complete program year
budget=pol["projected_invitations"]
print("="*98); print("A PREDICTION MODEL FOR THE SIZE OF THE NEXT ROUND"); print("="*98)
print(f"  2026-27 invitation budget implied by planning levels : {budget:,}")
print(f"  (21,090 places x {pol['ratio']:.2f} invitations per place, the 2025-26 observed rate)")
print(f"\n  complete program year on record, 2025-26: {PY2526}  mean {np.mean(PY2526):,.0f}")
shape=np.array(PY2526)/np.mean(PY2526)
print(f"  within-year shape factors (round / that year's mean): {np.round(shape,3).tolist()}")
print(f"  2024-25 (may be incomplete - panel starts Sep 2024): {PY2425}")
# rounds per year: 3 observed in the one complete year; 2 seen in the partial year
NR={2:0.25,3:0.55,4:0.20}
print(f"\n  rounds per year, prior: {NR}  (3 observed in the only complete year; 2 in the partial one;")
print(f"  4 allowed because a larger program can be split further)")
sizes=[];wts=[]
for n,pn in NR.items():
    base=budget/n
    for sh in shape:
        sizes.append(base*sh); wts.append(pn/len(shape))
sizes=np.array(sizes); wts=np.array(wts); wts/=wts.sum()
order=np.argsort(sizes); sizes,wts=sizes[order],wts[order]
cdf=np.cumsum(wts)
def q(p): return float(np.interp(p,cdf,sizes))
print(f"\n  IMPLIED DISTRIBUTION over the next round's size")
print(f"    mean  {float((sizes*wts).sum()):>9,.0f}")
for p in [.1,.25,.5,.75,.9]:
    print(f"    p{int(p*100):<4}{q(p):>9,.0f}")
print(f"\n  P(round >= 6,450, the smallest on record) = {float(wts[sizes>=6450].sum()):.0%}")
print(f"  P(round >= 10,000)                        = {float(wts[sizes>=10000].sum()):.0%}")
print(f"  P(round >= 14,724, the largest on record) = {float(wts[sizes>=14724].sum()):.0%}")
grid=np.arange(2000,20001,250)
dens=np.zeros_like(grid,dtype=float)
bw=1200.0
for s,w in zip(sizes,wts):
    dens+=w*np.exp(-0.5*((grid-s)/bw)**2)
dens/=dens.sum()
json.dump(dict(budget=int(budget),rounds_prior=NR,shape=[round(float(x),4) for x in shape],
  mean=int((sizes*wts).sum()),q10=int(q(.1)),q50=int(q(.5)),q90=int(q(.9)),
  grid=[int(g) for g in grid],dens=[round(float(d),6) for d in dens],
  atoms=[[int(s),round(float(w),4)] for s,w in zip(sizes,wts)]),open("roundsize.json","w"),indent=1)
print("\n  -> roundsize.json written (a smoothed density on a 2k-20k grid, for marginalising)")
