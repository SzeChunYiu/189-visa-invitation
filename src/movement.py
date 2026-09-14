"""How does a cut-off MOVE between rounds? Step or jump, and does a band clear?"""
import pandas as pd, numpy as np, json, pathlib, os
from scipy import stats
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
GOOD=["2025-08","2025-11","2026-06"]          # rounds with adequate panel coverage
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0)
inv["G"]=inv.OccGroup.astype(str).str[:4]
cut=inv[(inv.n>0)&(inv.StatusMonth.isin(ROUNDS))].groupby(["G","StatusMonth"]).Score.min().unstack()
cut=cut.reindex(columns=ROUNDS)

print("="*98); print("Q1  DOES THE CUT-OFF STEP OR JUMP?  distribution of the change between consecutive rounds"); print("="*98)
deltas=[]
for i in range(1,len(ROUNDS)):
    a,b=ROUNDS[i-1],ROUNDS[i]
    d=(cut[b]-cut[a]).dropna()
    for g,v in d.items(): deltas.append(dict(G=g,frm=a,to=b,d=int(v),recent=b in GOOD))
D=pd.DataFrame(deltas)
for lbl,z in [("all transitions",D),("current-regime only",D[D.recent])]:
    vc=z.d.value_counts().sort_index()
    print(f"\n  {lbl}  (n={len(z)})")
    print(f"  {'change':>8}{'count':>7}{'share':>8}   ")
    for k,v in vc.items():
        bar="#"*int(38*v/len(z))
        print(f"  {k:>+8}{v:>7}{100*v/len(z):>7.0f}%   {bar}")
    print(f"    stays put      : {100*(z.d==0).mean():>4.0f}%")
    print(f"    moves by 5     : {100*(z.d.abs()==5).mean():>4.0f}%")
    print(f"    moves by 10+   : {100*(z.d.abs()>=10).mean():>4.0f}%")
    print(f"    mean |change|  : {z.d.abs().mean():.1f} pts")

print("\n"+"="*98); print("Q2  IF IT LANDS ON A BAND, DOES THE WHOLE BAND GET IN?"); print("="*98)
sat=pd.read_csv("saturation_grp.csv")
t=sat[(sat["round"].isin(GOOD))&(sat.state!="UNTOUCHED")].copy()
lo=t.groupby(["round","OccGroup"]).Score.min().rename("boundary")
t=t.merge(lo,on=["round","OccGroup"])
bnd=t[t.Score==t.boundary]
print(f"  boundary cells examined (current-regime rounds): {len(bnd)}")
print(f"    fully CLEARED - everyone in that band invited : {(bnd.state=='CLEARED').sum():>4}  ({100*(bnd.state=='CLEARED').mean():.0f}%)")
print(f"    PARTIAL - some left behind on date            : {(bnd.state=='PARTIAL').sum():>4}  ({100*(bnd.state=='PARTIAL').mean():.0f}%)")
print("\n  => landing on your band is usually NOT a free pass: roughly two in three boundary bands")
print("     are rationed, which is exactly why a date of effect matters at the margin.")

print("\n"+"="*98); print("Q3  WHAT MOVES IT?  change in cut-off against change in allocation and pool"); print("="*98)
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS)
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
pool=pd.DataFrame({r:pf[pf.AsAt==PRIOR[r]].groupby("G").n.sum() for r in ROUNDS})
rows=[]
for i in range(1,len(ROUNDS)):
    a,b=ROUNDS[i-1],ROUNDS[i]
    for g in cut.index:
        if pd.isna(cut.loc[g,a]) or pd.isna(cut.loc[g,b]): continue
        if al.loc[g,a]<=0 or pool.get(a,{}).get(g,0)<=0: continue
        rows.append(dict(d=cut.loc[g,b]-cut.loc[g,a],
                         dAlloc=np.log((al.loc[g,b]+1)/(al.loc[g,a]+1)),
                         dPool=np.log((pool.loc[g,b]+1)/(pool.loc[g,a]+1)),
                         recent=b in GOOD))
R=pd.DataFrame(rows)
for lbl,z in [("all",R),("current regime",R[R.recent])]:
    if len(z)<8: continue
    print(f"\n  {lbl} (n={len(z)})")
    print(f"    corr(cut-off change, log change in ALLOCATION) = {np.corrcoef(z.d,z.dAlloc)[0,1]:+.3f}")
    print(f"    corr(cut-off change, log change in POOL)       = {np.corrcoef(z.d,z.dPool)[0,1]:+.3f}")
print("\n  More invitations push the cut-off DOWN; a bigger pool pushes it UP. Both are mechanical,")
print("  and neither is 'news' - the model has no channel for announcements, only for places and people.")
json.dump(dict(delta_all={int(k):int(v) for k,v in D.d.value_counts().items()},
  delta_recent={int(k):int(v) for k,v in D[D.recent].d.value_counts().items()},
  p_stay=round(float((D[D.recent].d==0).mean()),3),
  p_move5=round(float((D[D.recent].d.abs()==5).mean()),3),
  p_move10=round(float((D[D.recent].d.abs()>=10).mean()),3),
  boundary_cleared=round(float((bnd.state=='CLEARED').mean()),3),
  n_boundary=int(len(bnd))),open("movement.json","w"),indent=1)
print("\n  -> movement.json written")
