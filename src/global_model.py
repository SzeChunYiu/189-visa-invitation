"""Global occupation-level model + conservation check + out-of-sample backtest."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0)
pool=num(pd.read_csv("pool189_occ_score.csv")); pool["n"]=pool.n.fillna(0)

def predicted_cutoff(pool_g, alloc):
    """Walk the stratum's pool from the top score down until `alloc` invitations are used up."""
    if alloc<=0 or pool_g.empty: return np.nan, np.nan
    s=pool_g.sort_values("Score",ascending=False)
    cum=0
    for _,r in s.iterrows():
        prev=cum; cum+=r.n
        if cum>=alloc:
            frac=(alloc-prev)/r.n if r.n else 1.0   # partial clearance at the boundary score
            return int(r.Score), float(frac)
    return int(s.Score.min()), 1.0                  # allocation exhausts the whole pool

print("="*104)
print("BACKTEST  -  train on rounds 1-4, predict Jun-2026 cut-off per occupation from (pool, allocation)")
print("="*104)
rows=[]
for g,gi in inv[inv.StatusMonth=="2026-06"].groupby("OccGroup"):
    alloc=gi.n.sum()
    if alloc<5: continue
    pg=pool[(pool.OccGroup==g)&(pool.AsAt==PRIOR["2026-06"])][["Score","n"]]
    pc,frac=predicted_cutoff(pg,alloc)
    ac=gi.loc[gi.n>0,"Score"].min()
    if np.isnan(pc): continue
    rows.append(dict(occ=g,alloc=int(alloc),pred=pc,actual=int(ac),err=pc-int(ac)))
bt=pd.DataFrame(rows)
print(f"  occupations tested: {len(bt)}   (>=5 invitations in Jun-2026)")
print(f"  exact hits         : {(bt.err==0).sum()}  ({100*(bt.err==0).mean():.0f}%)")
print(f"  within +/-5 pts    : {(bt.err.abs()<=5).sum()}  ({100*(bt.err.abs()<=5).mean():.0f}%)")
print(f"  mean signed error  : {bt.err.mean():+.2f} pts    MAE = {bt.err.abs().mean():.2f} pts")
print(f"  correlation pred vs actual : r = {np.corrcoef(bt.pred,bt.actual)[0,1]:.3f}")
print("\n  worst misses:"); print(bt.reindex(bt.err.abs().sort_values(ascending=False).index).head(5).to_string(index=False))

print("\n"+"="*104)
print("CONSERVATION CHECK  -  do per-occupation expected invitations sum to the observed round total?")
print("="*104)
for rd in ROUNDS:
    tot=inv[inv.StatusMonth==rd].n.sum()
    per=inv[inv.StatusMonth==rd].groupby("OccGroup").n.sum()
    print(f"  {rd}: occupations invited={len(per[per>0]):>4}   sum of per-occupation invites={per.sum():>7,.0f}"
          f"   observed round total={tot:>7,.0f}   residual={per.sum()-tot:>4.0f}")
top=inv[inv.StatusMonth=="2026-06"].groupby("OccGroup").n.sum().sort_values(ascending=False)
print(f"\n  Jun-2026 concentration: top-10 occupations take {100*top.head(10).sum()/top.sum():.1f}% of the round;"
      f" top-30 take {100*top.head(30).sum()/top.sum():.1f}%")

print("\n"+"="*104); print("MACRO DRIVERS observable in the panel"); print("="*104)
ps=pd.read_csv("panel_status_189.csv").fillna(0)
ps=ps[ps.AsAt.astype(str).str.contains("/")]
piv=ps.pivot_table(index="AsAt",columns="Status",values="n",aggfunc="sum").fillna(0)
piv.index=pd.to_datetime(piv.index,format="%m/%Y"); piv=piv.sort_index()
sub=piv["SUBMITTED"]
infl=sub.diff().tail(12).mean()
sizes=[int(inv[inv.StatusMonth==r].n.sum()) for r in ROUNDS]
a2349=json.load(open("alloc_2349_allleg.json"))
print(f"  189 pool (SUBMITTED)      : {sub.iloc[0]:,.0f} -> {sub.iloc[-1]:,.0f}   net inflow last 12m = {infl:+,.0f}/month")
print(f"  round size (189-only)     : {sizes}   trend = {'growing' if sizes[-1]>sizes[0] else 'flat/falling'}")
print(f"  allocation to 2349        : {list(a2349.values())}   ratio last/first = {list(a2349.values())[-1]/max(1,list(a2349.values())[0]):.1f}x")
print(f"  2349 share of round       : "+", ".join(f"{rd[-7:]}={100*int(a2349[rd])/sizes[i]:.2f}%" for i,rd in enumerate(ROUNDS)))
print(f"  CLOSED (expiry/withdrawal): {piv['CLOSED'].iloc[-1]:,.0f} cumulative; last-12m mean = {piv['CLOSED'].diff().tail(12).mean():+,.0f}/month")
print("\n  NOT observable here (exogenous policy): annual migration planning levels, ministerial direction on")
print("  occupation priority, and whether a round is scheduled at all. These set round size and cadence.")

out=dict(backtest=dict(n=int(len(bt)),exact=int((bt.err==0).sum()),within5=int((bt.err.abs()<=5).sum()),
                       mae=round(float(bt.err.abs().mean()),2),r=round(float(np.corrcoef(bt.pred,bt.actual)[0,1]),3)),
         sizes=sizes,alloc2349=a2349,inflow=round(float(infl)),
         concentration_top10=round(float(100*top.head(10).sum()/top.sum()),1))
json.dump(out,open("global_model.json","w"),indent=1)
print("\n  -> global_model.json written")
