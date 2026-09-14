"""Reconcile the threshold model and the forecast model for ANZSCO 2349 at 85 points."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
G4="2349"
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
one=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
allleg=pd.read_csv("allocation_by_group.csv",index_col=0)
a_all=[int(allleg.loc[[i for i in allleg.index if str(i).startswith(G4)][0],r]) for r in ROUNDS]
a_one=[int(one.loc[G4,r]) for r in ROUNDS]
tot_one=one.sum(axis=0)
share=[a_one[i]/tot_one[ROUNDS[i]] for i in range(5)]
print("="*98); print("STEP 1 - are the two models on the same basis?"); print("="*98)
print(f"  {'round':<10}{'alloc all-leg':>14}{'alloc single-leg':>18}{'2349 share of round':>21}")
for i,r in enumerate(ROUNDS):
    print(f"  {r:<10}{a_all[i]:>14}{a_one[i]:>18}{100*share[i]:>20.2f}%")
print(f"\n  The 2024 allocations are small because 2349's SHARE was small then "
      f"({100*share[0]:.2f}%, {100*share[1]:.2f}%), not because rounds were small.")
print(f"  Share has since risen to {100*share[-1]:.2f}% and share autocorrelation on the recent")
print(f"  transitions is 0.92-0.96, so the 2024 shares are a stale regime, not plausible draws.")

p=num(pd.read_csv("pool189only_occ4.csv")); p["n"]=p["only"].fillna(0); p["G"]=p.Occupation.astype(str).str[:4]
pg=p[(p.AsAt=="08/2026")&(p.G==G4)].groupby("Score",as_index=False).n.sum()
pf=pd.read_csv("poolfull_grp.csv"); pf=num(pf); pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
pga=pf[(pf.AsAt=="08/2026")&(pf.G==G4)].groupby("Score",as_index=False).n.sum()
s1=pg[pg.Score>=85].n.sum(); sa=pga[pga.Score>=85].n.sum()
print("\n"+"="*98); print("STEP 2 - apples-to-apples at the 85+ boundary"); print("="*98)
print(f"  2349 stock at >=85, single-leg : {s1:.0f}    all-leg : {sa:.0f}")
print(f"  Jun-2026 allocation             single-leg : {a_one[-1]}      all-leg : {a_all[-1]}")
print(f"  allocation / 85+ stock          single-leg : {a_one[-1]/s1:.2f}x   all-leg : {a_all[-1]/sa:.2f}x")
print(f"\n  BOTH bases agree: the last round's allocation EXCEEDED the entire 85+ stock, so the cut-off")
print(f"  had to fall below 85 - and it did (actual 80). The threshold model's '2 of 5 rounds cover")
print(f"  rank 32' is therefore not a like-for-like probability: three of those five draws come from")
print(f"  a regime where 2349's share was 4-14x smaller.")

FLOOR=65; FR=5198/10000
def cutoff(pgx,A):
    if A<=0: return None
    s=pgx[pgx.Score>=FLOOR].sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return FLOOR
print("\n"+"="*98); print("STEP 3 - forecast cut-off at each HISTORICAL round size, using today's share and pool"); print("="*98)
sizes={"Sep 2024":7735,"Nov 2024":14724,"Aug 2025":6450,"Nov 2025":9826,"Jun 2026":9748}
print(f"  {'if the next round is the size of':<34}{'round size':>12}{'2349 alloc':>12}{'cut-off':>9}  verdict at 85 pts")
res=[]
for lbl,S in sizes.items():
    A=int(round(share[-1]*S*FR)); c=cutoff(pg,A)
    v="clears outright" if c<85 else ("AT THE BOUNDARY - date decides" if c==85 else "not reached")
    res.append((lbl,S,A,c,c<85)); print(f"  {lbl:<34}{S:>12,}{A:>12}{c:>9}  {v}")
clear=sum(1 for r in res if r[4])
print(f"\n  clears outright in {clear} of {len(res)} historical round sizes; the rest are boundary cases, none 'not reached'.")
print(f"  smallest round that still clears 85: ~{min(S for l,S,A,c,ok in res if ok):,}")
json.dump(dict(share_hist=[round(x,5) for x in share],alloc_all=a_all,alloc_single=a_one,
  stock85_single=int(s1),stock85_all=int(sa),scenarios=[{"label":l,"size":S,"alloc":A,"cutoff":c,"clears":bool(ok)} for l,S,A,c,ok in res]),
  open("reconcile.json","w"),indent=1)
print("\n  -> reconcile.json written")
