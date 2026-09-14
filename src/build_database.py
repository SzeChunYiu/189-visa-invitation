"""One coherent row per occupation x round: what a candidate at score S would have experienced."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
EPOCH=pd.Timestamp("1899-12-30")
qd=lambda x: EPOCH+pd.to_timedelta(pd.to_numeric(x,errors="coerce"),unit="D")
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df

inv=num(pd.read_csv("sat_inv_occ.csv")); pool=num(pd.read_csv("sat_pool_occ.csv"))
inv["n"]=inv.n.fillna(0); pool["n"]=pool.n.fillna(0)
inv["inv_max"]=qd(inv.maxsub); pool["pool_max"]=qd(pool.maxsub)
inv=inv[inv.StatusMonth.isin(ROUNDS)&(inv.n>0)]

rows=[]
for rd in ROUNDS:
    I=inv[inv.StatusMonth==rd][["Occupation","Score","n","inv_max"]]
    P=pool[pool.AsAt==PRIOR[rd]][["Occupation","Score","n","pool_max"]].rename(columns={"n":"pool_n"})
    m=P.merge(I,on=["Occupation","Score"],how="outer")
    m["n"]=m.n.fillna(0); m["pool_n"]=m.pool_n.fillna(0)
    m["state"]=np.where(m.n==0,"UNTOUCHED",np.where(m.inv_max>=m.pool_max,"CLEARED","PARTIAL"))
    for occ,g in m.groupby("Occupation"):
        t=g[g.n>0]
        if not len(t): continue
        cl=t[t.state=="CLEARED"].Score
        boundary=int(t.Score.min())
        bstate=t.loc[t.Score.idxmin(),"state"]
        nid=t.loc[t.Score.idxmin(),"inv_max"]
        rows.append(dict(occupation=occ,round=rd,
            lowest_cleared_score=int(cl.min()) if len(cl) else None,
            boundary_score=boundary, boundary_state=bstate,
            newest_invited=None if pd.isna(nid) else nid.strftime("%Y-%m-%d"),
            invited_n=int(t.n.sum()), pool_n=int(g.pool_n.sum())))
db=pd.DataFrame(rows)
db.to_csv("occupation_database.csv",index=False)
print(f"occupation x round rows: {len(db)}   distinct occupations: {db.occupation.nunique()}")
print(f"boundary states: {db.boundary_state.value_counts().to_dict()}")
print("\nPhysicist:"); print(db[db.occupation=="234914 Physicist"].to_string(index=False))

# wide form for the dashboard: one row per occupation
wide=[]
latest=pool[pool.AsAt=="08/2026"]
for occ,g in db.groupby("occupation"):
    r={"o":occ}
    for rd in ROUNDS:
        x=g[g["round"]==rd]
        if len(x):
            x=x.iloc[0]
            r[rd]=[None if pd.isna(x.lowest_cleared_score) else int(x.lowest_cleared_score),
                   int(x.boundary_score), x.boundary_state[0], int(x.invited_n)]
        else: r[rd]=None
    lp=latest[latest.Occupation==occ]
    r["pool"]=int(lp.n.sum()); r["p85"]=int(lp[lp.Score==85].n.sum()); r["pg"]=int(lp[lp.Score>85].n.sum())
    wide.append(r)
json.dump(wide,open("occupation_database.json","w"),separators=(",",":"))
print(f"\n-> occupation_database.csv ({len(db)} rows) and .json ({len(wide)} occupations) written")
print("\nlegend: [lowest_fully_cleared_score, boundary_score, C|P|U, invited_n]")
print("  at or above lowest_cleared_score -> invited regardless of date")
print("  at boundary_score with state P   -> depends on your date vs newest_invited")
