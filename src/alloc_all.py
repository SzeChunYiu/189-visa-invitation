"""Per-group allocation (all-leg, own DiD baseline) + the predictability gate."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
a=pd.read_csv("alloc_all_grp.csv").fillna(0)
a=a[a.StatusMonth.astype(str).str.match(r"\d{4}-\d{2}")]
a["is_r"]=a.StatusMonth.isin(ROUNDS)
base=a[~a.is_r].groupby("OccGroup").all189.median().rename("baseline")
al=a[a.is_r].merge(base,on="OccGroup",how="left").fillna({"baseline":0})
al["alloc"]=(al.all189-al.baseline).clip(lower=0).round().astype(int)
piv=al.pivot_table(index="OccGroup",columns="StatusMonth",values="alloc",aggfunc="sum").fillna(0).astype(int)
piv=piv.reindex(columns=ROUNDS,fill_value=0)
piv.to_csv("allocation_by_group.csv")
act=piv[piv.sum(axis=1)>0]
print("="*100); print("PER-GROUP ALLOCATION (all-leg, each group's own non-round baseline)"); print("="*100)
print(f"  groups with any allocation: {len(act)}   total across rounds: {act.values.sum():,}")
print(f"  2349 check: {act.loc['2349 Other Natural and Physical Science Professionals'].tolist()}  (expected [5,21,29,43,87])")
print(f"  round totals: {dict(zip(ROUNDS,act.sum().astype(int)))}")

print("\n"+"="*100); print("GATE (section 2): IS ALLOCATION FORECASTABLE?"); print("="*100)
pairs=[]
for i in range(1,len(ROUNDS)):
    prev,cur=ROUNDS[i-1],ROUNDS[i]
    d=act[[prev,cur]]; d=d[(d[prev]>0)|(d[cur]>0)]
    r=np.corrcoef(d[prev],d[cur])[0,1]
    lr=np.corrcoef(np.log1p(d[prev]),np.log1p(d[cur]))[0,1]
    pairs.append((prev,cur,len(d),r,lr))
    print(f"  alloc({cur}) vs alloc({prev}): n={len(d):>3}  Pearson r={r:.3f}   log1p r={lr:.3f}")
pooled=np.mean([p[3] for p in pairs]); pooled_log=np.mean([p[4] for p in pairs])
print(f"\n  POOLED lag-1 autocorrelation: raw r={pooled:.3f}   log r={pooled_log:.3f}")
mono=0; nz=0
for g,row in act.iterrows():
    v=[x for x in row.tolist()]
    if sum(v)==0: continue
    nz+=1
    if all(v[i]<=v[i+1] for i in range(len(v)-1)): mono+=1
print(f"  groups with a monotone non-decreasing allocation series: {mono} of {nz}  ({100*mono/nz:.0f}%)")
print(f"  -> 2349 is {'typical' if 100*mono/nz>40 else 'UNUSUAL'} in being monotone")
sh=act.div(act.sum(axis=0),axis=1)
print("\n  stability of a group's SHARE of the round (share is what a forecast really needs):")
for i in range(1,len(ROUNDS)):
    d=sh[[ROUNDS[i-1],ROUNDS[i]]].dropna()
    print(f"   share({ROUNDS[i]}) vs share({ROUNDS[i-1]}): r={np.corrcoef(d.iloc[:,0],d.iloc[:,1])[0,1]:.3f}")
shr=[np.corrcoef(sh[ROUNDS[i-1]],sh[ROUNDS[i]])[0,1] for i in range(1,len(ROUNDS))]
print(f"\n  POOLED share autocorrelation: r={np.mean(shr):.3f}")
json.dump(dict(pooled_r=round(float(pooled),3),pooled_log_r=round(float(pooled_log),3),
               share_r=round(float(np.mean(shr)),3),monotone=int(mono),groups=int(nz)),
          open("alloc_gate.json","w"),indent=1)
print("\n  -> allocation_by_group.csv, alloc_gate.json written")
