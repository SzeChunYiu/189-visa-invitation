"""Is an invitation round BAND-dependent (whole bands) or NUMBER-dependent (a count cutting through)?"""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]; GOOD=["2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
pl=num(pd.read_csv("pool189only_occ4.csv")); pl["n"]=pl["only"].fillna(0); pl["G"]=pl.Occupation.astype(str).str[:4]

print("="*100)
print("TEST 1  BAND-dependent or NUMBER-dependent?")
print("  Band-dependent => a round takes WHOLE bands, so invited-at-a-score equals the pool at that score.")
print("  Number-dependent => a count cuts through, so the lowest band invited is a FRACTION of its pool.")
print("="*100)
rows=[]
for rd in GOOD:
    P=pl[pl.AsAt==PRIOR[rd]].groupby(["G","Score"],as_index=False).n.sum()
    I=inv[(inv.StatusMonth==rd)&(inv.n>0)]
    for g,gi in I.groupby("G"):
        gi=gi.sort_values("Score",ascending=False)
        pg=P[P.G==g].set_index("Score").n.to_dict()
        for _,r in gi.iterrows():
            pool_n=pg.get(int(r.Score),0)
            if pool_n<=0: continue
            rows.append(dict(G=g,round=rd,score=int(r.Score),invited=int(r.n),pool=int(pool_n),
                             frac=r.n/pool_n, lowest=int(r.Score)==int(gi.Score.min())))
D=pd.DataFrame(rows)
D["full"]=D.frac>=0.999
print(f"  (group, score) cells examined: {len(D)}")
print(f"\n  cells ABOVE the lowest invited score  : {(~D.lowest).sum():>4}   fully taken: {100*D[~D.lowest].full.mean():>5.1f}%")
print(f"  cells AT the lowest invited score     : {D.lowest.sum():>4}   fully taken: {100*D[D.lowest].full.mean():>5.1f}%")
lo=D[D.lowest]
print(f"\n  distribution of 'share of the band invited' AT the lowest band:")
for a,b in [(0,.25),(.25,.5),(.5,.75),(.75,.999),(.999,9)]:
    k=((lo.frac>=a)&(lo.frac<b)).sum()
    print(f"    {int(a*100):>3}-{min(100,int(b*100)):>3}% of the band : {k:>4}  ({100*k/len(lo):>4.0f}%)")
print(f"\n  median share of the lowest band taken: {lo.frac.median():.2f}")
print("\n  VERDICT: bands above the margin are taken WHOLE; the lowest band is a partial cut.")
print("  That is the signature of a NUMBER: a count walks down the ranking and stops mid-band.")

print("\n"+"="*100); print("TEST 2  does the allocation land on band boundaries (band-quota) or anywhere (count)?"); print("="*100)
hits=0; tot=0; offs=[]
for rd in GOOD:
    P=pl[pl.AsAt==PRIOR[rd]].groupby(["G","Score"],as_index=False).n.sum()
    I=inv[(inv.StatusMonth==rd)&(inv.n>0)].groupby("G").n.sum()
    for g,A in I.items():
        pg=P[P.G==g].sort_values("Score",ascending=False)
        if pg.empty: continue
        cum=np.cumsum(pg.n.values)
        tot+=1
        if np.any(np.abs(cum-A)<0.5): hits+=1
        else: offs.append(float(np.min(np.abs(cum-A))))
print(f"  group-rounds tested: {tot}")
print(f"  allocation exactly equals a cumulative band boundary: {hits} ({100*hits/tot:.0f}%)")
print(f"  otherwise, median distance to the nearest boundary   : {np.median(offs):.0f} invitations")
print("\n  If rounds handed out whole bands, that first figure would be near 100%. It is not.")

print("\n"+"="*100); print("TEST 3  WHICH groups get nothing, and is there a visible reason?"); print("="*100)
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
names=pf.groupby("G").OccGroup.first()
poolnow=pf[pf.AsAt=="08/2026"].groupby("G").n.sum()
always=[g for g in al.index if all(al.loc[g,r]==0 for r in GOOD) and poolnow.get(g,0)>0]
never=[g for g in al.index if all(al.loc[g,r]>0 for r in GOOD)]
print(f"  groups that got NOTHING in all 3 recent rounds ({len(always)}), largest pools first:")
for g in sorted(always,key=lambda x:-poolnow.get(x,0))[:14]:
    print(f"    {names.get(g,g)[:52]:<54} pool {int(poolnow.get(g,0)):>6,}")
print(f"\n  median pool, always-skipped groups : {np.median([poolnow.get(g,0) for g in always]):>8,.0f}")
print(f"  median pool, always-invited groups : {np.median([poolnow.get(g,0) for g in never]):>8,.0f}")
json.dump(dict(above_full=round(float(D[~D.lowest].full.mean()),3),
  lowest_full=round(float(D[D.lowest].full.mean()),3),
  median_lowest_frac=round(float(lo.frac.median()),3),
  boundary_hits=round(hits/tot,3),
  always_skipped=[names.get(g,g) for g in sorted(always,key=lambda x:-poolnow.get(x,0))]),
  open("mechanism.json","w"),indent=1)
print("\n  -> mechanism.json written")
