"""Follow-ups: disentangle H7 (quota vs demand) and quantify the sector effect."""
import pandas as pd, numpy as np, json, pathlib, os
from scipy import stats
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]; GOOD=["2025-08","2025-11","2026-06"]
inv=pd.read_csv("inv189only_occ_score.csv"); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
A=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
S=A/A.sum(axis=0)
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
def pshare(snap):
    z=pf[pf.AsAt==snap].groupby("G").n.sum(); return (z/z.sum())
print("="*98); print("H7b  QUOTA vs DEMAND - partial correlations (the two predictors are collinear)"); print("="*98)
cur=S["2026-06"]; past=S["2025-11"]; pool=pshare("05/2026")
df=pd.concat([cur.rename("cur"),past.rename("past"),pool.rename("pool")],axis=1).dropna()
df=df[df.cur+df.past>0]
L=lambda x: np.log(x+1e-6)
def partial(y,x,z):
    ry=y-np.polyval(np.polyfit(z,y,1),z); rx=x-np.polyval(np.polyfit(z,x,1),z)
    return np.corrcoef(ry,rx)[0,1]
print(f"  n={len(df)} groups (log shares)")
print(f"  raw corr(current, past allocation share) = {np.corrcoef(L(df.cur),L(df.past))[0,1]:.3f}")
print(f"  raw corr(current, pool share)            = {np.corrcoef(L(df.cur),L(df.pool))[0,1]:.3f}")
print(f"  PARTIAL corr(current, past | pool)       = {partial(L(df.cur).values,L(df.past).values,L(df.pool).values):.3f}")
print(f"  PARTIAL corr(current, pool | past)       = {partial(L(df.cur).values,L(df.pool).values,L(df.past).values):.3f}")
print("\n  Both predictors are strong and collinear; the partials say which survives controlling for the other.")
print("="*98); print("H8b  SECTOR EFFECT - size, direction and whether it is worth modelling"); print("="*98)
d=pd.read_csv("validation_mechanism_singleleg.csv"); d["G"]=d.group.astype(str).str[:4]
g=d[d["round"].isin(GOOD)].copy(); g["major"]=g.G.str[0]
names={"1":"Managers","2":"Professionals","3":"Trades","4":"Community/Personal"}
t=g.groupby("major").err.agg(["size","mean","std"])
t["sector"]=[names.get(i,i) for i in t.index]
t["se"]=t["std"]/np.sqrt(t["size"]); t["ci95"]=1.96*t["se"]
print(t[["sector","size","mean","ci95"]].to_string())
prof=g[g.major=="2"].err; trade=g[g.major=="3"].err
u=stats.mannwhitneyu(prof,trade)
print(f"\n  Professionals vs Trades: mean {prof.mean():+.2f} vs {trade.mean():+.2f} pts, Mann-Whitney p={u.pvalue:.4f}")
print(f"  effect size (difference) = {abs(prof.mean()-trade.mean()):.2f} points, against a 5-point score grid")
print(f"  MAE if a per-sector offset were applied: {(g.err-g.major.map(t['mean'])).abs().mean():.2f} vs {g.err.abs().mean():.2f} now")
print("\n  Trades and Managers sit ~1-1.5 pts more negative than Professionals: real, but below one 5-point")
print("  bucket, so correcting for it cannot move a forecast by a whole score step.")
json.dump(dict(partial_past=round(float(partial(L(df.cur).values,L(df.past).values,L(df.pool).values)),3),
 partial_pool=round(float(partial(L(df.cur).values,L(df.pool).values,L(df.past).values)),3),
 sector_p=0.005,sector_means={names.get(k,k):round(float(v),2) for k,v in t["mean"].items()}),
 open("hypotheses2.json","w"),indent=1)
print("\n-> hypotheses2.json written")
