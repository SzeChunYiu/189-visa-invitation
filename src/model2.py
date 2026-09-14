import pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/'data')
import pandas as pd, numpy as np, json
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
invg=num(pd.read_csv("inv189only_occ_score.csv")); invg["n"]=invg.n.fillna(0)
poolg=num(pd.read_csv("pool189_occ_score.csv")); poolg["n"]=poolg.n.fillna(0)
poolo=num(pd.read_csv("pool189only_occ4.csv")); poolo["only"]=poolo["only"].fillna(0)
G="2349 Other Natural and Physical Science Professionals"
ig=invg[invg.OccGroup==G]; pg=poolg[poolg.OccGroup==G]
po=poolo[poolo.Occupation.astype(str).str.startswith("2349")]

print("="*100); print("MODEL 4 - ALLOCATION vs RANK  (unit group 2349, the binding ceiling stratum)"); print("="*100)
print(f"  {'round':<10}{'2349 alloc':>12}{'pool>=85 pre':>14}{'alloc-pool':>12}{'cut-off':>9}  interpretation")
recs=[]
for rd in ROUNDS:
    alloc=ig[ig.StatusMonth==rd].n.sum()
    pre=po[(po.AsAt==PRIOR[rd])&(po.Score>=85)]["only"].sum()
    cut=ig[(ig.StatusMonth==rd)&(ig.n>0)].Score.min()
    surplus=alloc-pre
    msg = "allocation EXCEEDS the >=85 stock -> goes below 85" if surplus>0 else "allocation short -> cut-off stays above 85"
    recs.append(dict(round=rd,alloc=int(alloc),pool_ge85=int(pre),surplus=int(surplus),cutoff=int(cut)))
    print(f"  {rd:<10}{alloc:>12,.0f}{pre:>14,.0f}{surplus:>12,.0f}{cut:>9.0f}  {msg}")

print("\n### Current state entering the next round (snapshot 08/2026 + Sep arrivals)")
lat_only=po[po.AsAt=="08/2026"]; lat_all=pg[pg.AsAt=="08/2026"]
o_gt=lat_only[lat_only.Score>85]["only"].sum(); o_eq=lat_only[lat_only.Score==85]["only"].sum()
a_gt=lat_all[lat_all.Score>85].n.sum();        a_eq=lat_all[lat_all.Score==85].n.sum()
print(f"  2349 189-only basis : >85 = {o_gt:.0f}   =85 = {o_eq:.0f}   -> user's rank ~ {o_gt+o_eq+1:.0f}")
print(f"  2349 all-189  basis : >85 = {a_gt:.0f}   =85 = {a_eq:.0f}   -> user's rank ~ {a_gt+a_eq+1:.0f}")
alloc_hist=[r["alloc"] for r in recs]
print(f"  recent 2349 allocations (189-only): {alloc_hist}   last-3 mean = {np.mean(alloc_hist[-3:]):.0f}")
print(f"  => on the 189-only basis, rank {o_gt+o_eq+1:.0f} vs typical allocation {np.mean(alloc_hist[-3:]):.0f}"
      f"  -> covered {'YES' if o_gt+o_eq+1<=np.mean(alloc_hist[-3:]) else 'NO'}")

print("\n"+"="*100); print("MODEL 5 - P(invited | a round occurs), scenario-weighted"); print("="*100)
# scenario probabilities for the 2349 cut-off, recency-weighted over observed rounds (w = 2^(-age_in_rounds))
cuts=[r["cutoff"] for r in recs]; w=np.array([2.0**(-(len(cuts)-1-i)) for i in range(len(cuts))]); w/=w.sum()
print(f"  observed 2349 cut-offs {cuts} with recency weights {[round(x,3) for x in w]}")
p_below=float(w[[c<85 for c in cuts]].sum()); p_eq=float(w[[c==85 for c in cuts]].sum()); p_above=float(w[[c>85 for c in cuts]].sum())
print(f"  P(cut-off < 85)={p_below:.3f}   P(cut-off = 85)={p_eq:.3f}   P(cut-off > 85)={p_above:.3f}")
# if cut-off lands exactly at 85, user is NEWEST in the 85 tranche -> needs the tranche to clear fully
clear_rate=np.mean([1.0,1.0])   # both rounds that reached 85 cleared the tranche (79-100%, 92-100%)
p_inv_round = p_below*1.0 + p_eq*clear_rate + p_above*0.0
print(f"  P(invited | cut-off=85) = {clear_rate:.2f}  (both rounds reaching 85 cleared the whole tranche)")
print(f"\n  ==> P(invited | a round occurs) = {p_inv_round:.1%}")
# round occurrence
gaps=[2,9,3,7]
print(f"\n  round gaps (months): {gaps}; last round Jun-2026; Sep-2026 is 3 months on")
for horizon in [3,6,12]:
    p_round=min(1.0,sum(1 for g in gaps if g<=horizon+3)/len(gaps))
    print(f"   horizon {horizon:>2} mo: P(>=1 round) ~ {p_round:.2f}  ->  P(invited) ~ {p_round*p_inv_round:.1%}")
json.dump(dict(alloc=recs,rank_only=int(o_gt+o_eq+1),rank_all=int(a_gt+a_eq+1),
               p_below=p_below,p_eq=p_eq,p_above=p_above,p_inv_round=p_inv_round),
          open("model_final.json","w"),indent=1)
print("\n  -> model_final.json written")
