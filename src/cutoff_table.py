import pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/'data')
import pandas as pd, numpy as np, json
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ4_score.csv")); inv["n"]=inv.n.fillna(0)
pool=num(pd.read_csv("pool189_occ4_latest.csv")); pool["n"]=pool.n.fillna(0)
inv=inv[inv.StatusMonth.isin(ROUNDS)&(inv.n>0)]
rows=[]
for occ,g in inv.groupby("Occupation"):
    rec={"occupation":occ}
    for rd in ROUNDS:
        s=g[g.StatusMonth==rd]
        rec[rd]= int(s.Score.min()) if len(s) else None
        rec[rd+"_n"]= int(s.n.sum()) if len(s) else 0
    p=pool[pool.Occupation==occ]
    rec["pool_total"]=int(p.n.sum()); rec["pool_85"]=int(p[p.Score==85].n.sum())
    rec["pool_gt85"]=int(p[p.Score>85].n.sum()); rec["inv_total"]=int(g.n.sum())
    rows.append(rec)
df=pd.DataFrame(rows).sort_values("inv_total",ascending=False)
df.to_csv("cutoff_by_occupation.csv",index=False)
last=df["2026-06"].dropna()
print(f"occupations with >=1 invite in a real 189 round: {len(df)}")
print(f"Jun-2026 cut-off spread: min={last.min():.0f} p25={last.quantile(.25):.0f} med={last.median():.0f} p75={last.quantile(.75):.0f} max={last.max():.0f}")
print("\nPhysicist row:"); print(df[df.occupation=="234914 Physicist"].to_string(index=False))
df.to_json("cutoff_by_occupation.json",orient="records")
print("\n-> cutoff_by_occupation.csv/.json written")
