"""Refines the cut-off into three states per (stratum, score): CLEARED / PARTIAL / UNTOUCHED."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
EPOCH=pd.Timestamp("1899-12-30")
def qdate(x): return EPOCH+pd.to_timedelta(pd.to_numeric(x,errors="coerce"),unit="D")
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df

def build(invf,poolf,key):
    inv=num(pd.read_csv(invf)); pool=num(pd.read_csv(poolf))
    inv["n"]=inv.n.fillna(0); pool["n"]=pool.n.fillna(0)
    inv["inv_max"]=qdate(inv.maxsub); pool["pool_max"]=qdate(pool.maxsub)
    inv=inv[inv.StatusMonth.isin(ROUNDS)&(inv.n>0)]
    rows=[]
    for rd in ROUNDS:
        pm=PRIOR[rd]
        I=inv[inv.StatusMonth==rd][[key,"Score","n","inv_max"]]
        P=pool[pool.AsAt==pm][[key,"Score","n","pool_max"]].rename(columns={"n":"pool_n"})
        m=P.merge(I,on=[key,"Score"],how="outer")
        m["round"]=rd; m["n"]=m.n.fillna(0); m["pool_n"]=m.pool_n.fillna(0)
        # saturated: the newest-dated EOI standing in the pool was itself invited
        m["state"]=np.where(m.n==0,"UNTOUCHED",
                    np.where(m.inv_max>=m.pool_max,"CLEARED","PARTIAL"))
        rows.append(m)
    return pd.concat(rows,ignore_index=True)

g=build("sat_inv_grp.csv","sat_pool_grp.csv","OccGroup")
print("="*100); print("SATURATION STATES per (unit group, score, round)"); print("="*100)
print(g[g.pool_n>0].groupby(["round","state"]).size().unstack(fill_value=0).to_string())

print("\n### The decisive question: was the 85-point cell in ANZSCO 2349 fully cleared?")
z=g[(g.OccGroup=="2349 Other Natural and Physical Science Professionals")&(g.Score==85)]
for _,r in z.sort_values("round").iterrows():
    im = "-" if pd.isna(r.inv_max) else r.inv_max.strftime("%Y-%m-%d")
    pm = "-" if pd.isna(r.pool_max) else r.pool_max.strftime("%Y-%m-%d")
    print(f"  {r['round']}  pool={r.pool_n:>3.0f} invited={r.n:>3.0f}  newest in pool={pm}  newest invited={im}  -> {r.state}")

print("\n### 2349 by score, last two rounds (where the true cut-off sits)")
for rd in ["2025-11","2026-06"]:
    print(f"\n  ROUND {rd}")
    zz=g[(g.OccGroup=="2349 Other Natural and Physical Science Professionals")&(g["round"]==rd)&((g.pool_n>0)|(g.n>0))]
    for _,r in zz.sort_values("Score",ascending=False).iterrows():
        if r.Score<70: continue
        im = "-" if pd.isna(r.inv_max) else r.inv_max.strftime("%Y-%m")
        pm = "-" if pd.isna(r.pool_max) else r.pool_max.strftime("%Y-%m")
        print(f"    {int(r.Score):>4} pts  pool={r.pool_n:>4.0f} inv={r.n:>4.0f}  newest_pool={pm}  newest_inv={im}  {r.state}")
g.to_csv("saturation_grp.csv",index=False)

print("\n"+"="*100); print("WHAT THE STATES IMPLY - the boundary score per round (2349)"); print("="*100)
for rd in ROUNDS:
    zz=g[(g.OccGroup=="2349 Other Natural and Physical Science Professionals")&(g["round"]==rd)]
    cl=zz[zz.state=="CLEARED"].Score; pa=zz[zz.state=="PARTIAL"].Score
    print(f"  {rd}: lowest FULLY cleared score = {cl.min() if len(cl) else '-':>4}   "
          f"partially-filled scores = {sorted(pa.tolist()) if len(pa) else 'none'}")
