"""Does the tier theory beat plain persistence? Decide out of sample, not by story."""
import pandas as pd, numpy as np, json, os
os.chdir(os.path.join(os.path.dirname(__file__),"..","data"))
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
FLOOR=65
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
pl=num(pd.read_csv("pool189only_occ4.csv")); pl["n"]=pl["only"].fillna(0); pl["G"]=pl.Occupation.astype(str).str[:4]
tiers=json.load(open("tiers.json"))["tier_of"]
pool={r:pl[pl.AsAt==PRIOR[r]].groupby("G").n.sum() for r in ROUNDS}

def cutoff(pg,A):
    if A<=0: return None
    s=pg[pg.Score>=FLOOR].sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return FLOOR

def evaluate(predict_share, folds=("2025-08","2025-11","2026-06")):
    errs=[]
    for rd in folds:
        i=ROUNDS.index(rd); prev=ROUNDS[i-1]
        tot=al[rd].sum()
        P=pl[pl.AsAt==PRIOR[rd]]
        share=predict_share(prev,rd)
        if share is None: continue
        share=share/share.sum() if share.sum()>0 else share
        act=inv[(inv.StatusMonth==rd)&(inv.n>0)].groupby("G").Score.min()
        for g,a in act.items():
            pg=P[P.G==g][["Score","n"]]
            if pg.empty: continue
            A=int(round(share.get(g,0)*tot))
            c=cutoff(pg,A)
            if c is None: continue
            errs.append(c-a)
    e=np.array(errs,float)
    return dict(n=len(e),exact=float((e==0).mean()),within5=float((np.abs(e)<=5).mean()),
                mae=float(np.abs(e).mean()),bias=float(e.mean()))

groups=al.index
# M0 incumbent: this round's split looks like last round's
M0=lambda prev,rd: al[prev].copy()
# M1 tier theory: allocation proportional to pool x a per-tier rate fitted on EARLIER rounds only
def M1(prev,rd):
    i=ROUNDS.index(rd)
    hist=ROUNDS[:i]
    rate={}
    for t in (1,2,3,4):
        gs=[g for g in groups if tiers.get(g)==t]
        a=sum(al.loc[g,r] for g in gs for r in hist)
        p=sum(pool[r].get(g,0) for g in gs for r in hist)
        rate[t]=a/p if p>0 else 0
    return pd.Series({g: pool[rd].get(g,0)*rate.get(tiers.get(g,3),0) for g in groups})
# M2 blend: geometric mean of the two
def M2(prev,rd):
    a=M0(prev,rd); b=M1(prev,rd)
    a=a/a.sum() if a.sum()>0 else a; b=b/b.sum() if b.sum()>0 else b
    return pd.Series(np.sqrt(a.reindex(groups,fill_value=0)*b.reindex(groups,fill_value=0)),index=groups)

print("="*96); print("MODEL COMPARISON - predicting each round's cut-offs from information available before it"); print("="*96)
print(f"  {'model':<34}{'n':>5}{'exact':>8}{'within5':>9}{'MAE':>8}{'bias':>8}")
res={}
for name,f in [("M0 persistence (incumbent)",M0),("M1 tier x pool",M1),("M2 blend of the two",M2)]:
    r=evaluate(f); res[name]=r
    print(f"  {name:<34}{r['n']:>5}{100*r['exact']:>7.0f}%{100*r['within5']:>8.0f}%{r['mae']:>8.2f}{r['bias']:>+8.2f}")
print("\n  latest fold only (Jun-2026):")
for name,f in [("M0 persistence (incumbent)",M0),("M1 tier x pool",M1),("M2 blend of the two",M2)]:
    r=evaluate(f,folds=("2026-06",))
    print(f"  {name:<34}{r['n']:>5}{100*r['exact']:>7.0f}%{100*r['within5']:>8.0f}%{r['mae']:>8.2f}{r['bias']:>+8.2f}")
best=min(res,key=lambda k:res[k]["mae"])
print(f"\n  BEST BY OUT-OF-SAMPLE MAE: {best}  (MAE {res[best]['mae']:.2f})")
json.dump({k:{kk:round(vv,4) for kk,vv in v.items()} for k,v in res.items()}|{"best":best},
          open("theory_compare.json","w"),indent=1)
print("  -> theory_compare.json written")
