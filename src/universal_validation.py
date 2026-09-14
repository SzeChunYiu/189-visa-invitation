"""Cross-occupation, cross-time validation of the pool-rank mechanism."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
# CONSISTENT SINGLE-LEG BASIS on all three quantities.
# The all-leg cut-off is contaminated downward by 7.3 pts (11.3 for large groups) because an EOI
# invited for 190/491 still carries a 189 leg. Single-leg is the basis that matched the official table.
_p=num(pd.read_csv("pool189only_occ4.csv")); _p["n"]=_p["only"].fillna(0)
_p["OccGroup"]=_p.Occupation.astype(str).str[:4]
pool=_p.groupby(["AsAt","OccGroup","Score"],as_index=False).n.sum()
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0)
inv["OccGroup"]=inv.OccGroup.astype(str).str[:4]
alloc=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="OccGroup",columns="StatusMonth",
        values="n",aggfunc="sum").fillna(0).astype(int).reindex(columns=ROUNDS,fill_value=0)
inv=inv[inv.StatusMonth.isin(ROUNDS)]

def cutoff_from(pg,A):
    """walk the pool from the top score down until A invitations are consumed"""
    if A<=0 or pg.empty: return np.nan
    s=pg.sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return int(s.Score.min())

rows=[]
for rd in ROUNDS:
    P=pool[pool.AsAt==PRIOR[rd]]
    I=inv[inv.StatusMonth==rd]
    for g in alloc.index:
        A=int(alloc.loc[g,rd])
        ig=I[(I.OccGroup==g)&(I.n>0)]
        if not len(ig): continue
        actual=int(ig.Score.min())
        pg=P[P.OccGroup==g][["Score","n"]]
        pred=cutoff_from(pg,A)
        rows.append(dict(group=g,round=rd,alloc=A,pool=int(pg.n.sum()),
                         invited=int(ig.n.sum()),actual=actual,
                         pred=np.nan if np.isnan(pred) else int(pred)))
d=pd.DataFrame(rows).dropna(subset=["pred"])
d["err"]=d.pred-d.actual
print("="*100); print("A. MECHANISM TEST [SINGLE-LEG BASIS THROUGHOUT] - cut-off predicted from (pool, ACTUAL allocation), ALL rounds x ALL groups"); print("="*100)
print(f"  {'round':<10}{'groups':>8}{'exact':>9}{'within5':>10}{'MAE':>8}{'bias':>8}{'r':>8}")
for rd in ROUNDS:
    z=d[d["round"]==rd]
    if len(z)<3: continue
    print(f"  {rd:<10}{len(z):>8}{100*(z.err==0).mean():>8.0f}%{100*(z.err.abs()<=5).mean():>9.0f}%"
          f"{z.err.abs().mean():>8.2f}{z.err.mean():>+8.2f}{np.corrcoef(z.pred,z.actual)[0,1]:>8.3f}")
print(f"  {'ALL':<10}{len(d):>8}{100*(d.err==0).mean():>8.0f}%{100*(d.err.abs()<=5).mean():>9.0f}%"
      f"{d.err.abs().mean():>8.2f}{d.err.mean():>+8.2f}{np.corrcoef(d.pred,d.actual)[0,1]:>8.3f}")

print("\n"+"="*100); print("B. OUT-OF-SAMPLE - allocation SHARE forecast from the previous round, round size taken as given"); print("="*100)
tot=alloc[ROUNDS].sum(axis=0)
oos=[]
for i in range(1,len(ROUNDS)):
    prev,rd=ROUNDS[i-1],ROUNDS[i]
    share=alloc[prev]/max(1,alloc[prev].sum())
    P=pool[pool.AsAt==PRIOR[rd]]; I=inv[inv.StatusMonth==rd]
    for g in alloc.index:
        ig=I[(I.OccGroup==g)&(I.n>0)]
        if not len(ig): continue
        Ahat=int(round(share.get(g,0)*tot[rd]))
        pg=P[P.OccGroup==g][["Score","n"]]
        pr=cutoff_from(pg,Ahat)
        if np.isnan(pr): continue
        oos.append(dict(group=g,round=rd,pred=int(pr),actual=int(ig.Score.min()),
                        alloc_hat=Ahat,alloc_true=int(alloc.loc[g,rd]),pool=int(pg.n.sum())))
o=pd.DataFrame(oos); o["err"]=o.pred-o.actual
print(f"  {'fold':<10}{'groups':>8}{'exact':>9}{'within5':>10}{'MAE':>8}{'bias':>8}{'r':>8}")
for rd in ROUNDS[1:]:
    z=o[o["round"]==rd]
    if len(z)<3: continue
    print(f"  {rd:<10}{len(z):>8}{100*(z.err==0).mean():>8.0f}%{100*(z.err.abs()<=5).mean():>9.0f}%"
          f"{z.err.abs().mean():>8.2f}{z.err.mean():>+8.2f}{np.corrcoef(z.pred,z.actual)[0,1]:>8.3f}")
print(f"  {'ALL':<10}{len(o):>8}{100*(o.err==0).mean():>8.0f}%{100*(o.err.abs()<=5).mean():>9.0f}%"
      f"{o.err.abs().mean():>8.2f}{o.err.mean():>+8.2f}{np.corrcoef(o.pred,o.actual)[0,1]:>8.3f}")
print(f"\n  GAP mechanism -> out-of-sample: MAE {d.err.abs().mean():.2f} -> {o.err.abs().mean():.2f} pts")
print("  The gap is the cost of forecasting the allocation, not of the ranking rule.")

print("\n"+"="*100); print("C. CONSISTENCY BY OCCUPATION SIZE (mechanism test)"); print("="*100)
d["bucket"]=pd.cut(d["pool"],[0,25,100,400,1500,10**6],labels=["<25","25-100","100-400","400-1500",">1500"])
print(f"  {'pool size':<12}{'cells':>7}{'exact':>9}{'within5':>10}{'MAE':>8}{'bias':>8}")
for b,z in d.groupby("bucket",observed=True):
    print(f"  {str(b):<12}{len(z):>7}{100*(z.err==0).mean():>8.0f}%{100*(z.err.abs()<=5).mean():>9.0f}%"
          f"{z.err.abs().mean():>8.2f}{z.err.mean():>+8.2f}")
d.to_csv("validation_mechanism_singleleg.csv",index=False); o.to_csv("validation_oos_singleleg.csv",index=False)
json.dump(dict(mech=dict(n=int(len(d)),exact=round(float((d.err==0).mean()),3),within5=round(float((d.err.abs()<=5).mean()),3),
  mae=round(float(d.err.abs().mean()),2),bias=round(float(d.err.mean()),2),r=round(float(np.corrcoef(d.pred,d.actual)[0,1]),3)),
  oos=dict(n=int(len(o)),exact=round(float((o.err==0).mean()),3),within5=round(float((o.err.abs()<=5).mean()),3),
  mae=round(float(o.err.abs().mean()),2),bias=round(float(o.err.mean()),2),r=round(float(np.corrcoef(o.pred,o.actual)[0,1]),3))),
  open("validation_singleleg.json","w"),indent=1)
print("\n  -> validation_mechanism_singleleg.csv, validation_oos_singleleg.csv, validation_singleleg.json written")
