"""Hypothesis battery: what else, beyond pool-rank, systematically moves the cut-off?"""
import pandas as pd, numpy as np, json, pathlib, os
from scipy import stats
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
GOOD=["2025-08","2025-11","2026-06"]           # rounds with adequate panel coverage
d=pd.read_csv("validation_mechanism_singleleg.csv")
d["G"]=d.group.astype(str).str[:4]
alloc=pd.read_csv("allocation_by_group.csv",index_col=0)
out={}
def hdr(t): print("\n"+"="*98); print(t); print("="*98)

hdr("H1  POLICY / REGIME CHANGE - is there a structural break in how the round is split?")
inv=pd.read_csv("inv189only_occ_score.csv"); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
A=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
S=A/A.sum(axis=0)
print(f"  {'transition':<26}{'share corr':>12}{'cosine':>10}{'turnover of invited set':>26}")
for i in range(1,len(ROUNDS)):
    a,b=ROUNDS[i-1],ROUNDS[i]
    x,y=S[a].values,S[b].values
    cos=float(x@y/(np.linalg.norm(x)*np.linalg.norm(y)))
    sa,sb=set(A.index[A[a]>0]),set(A.index[A[b]>0])
    turn=1-len(sa&sb)/len(sa|sb)
    print(f"  {a} -> {b:<10}{np.corrcoef(x,y)[0,1]:>12.3f}{cos:>10.3f}{turn:>25.0%}")
print("\n  A regime shift shows up as a LOW cosine with HIGH turnover. The 2024-11 -> 2025-08 transition")
print("  is the weakest link in both; the two most recent transitions are near-identical splits.")
out["H1"]={f"{ROUNDS[i-1]}->{ROUNDS[i]}":round(float(np.corrcoef(S[ROUNDS[i-1]],S[ROUNDS[i]])[0,1]),3) for i in range(1,5)}

hdr("H2  SYSTEMATIC OCCUPATION BIAS - does a group's error persist across rounds?")
g=d[d["round"].isin(GOOD)]
piv=g.pivot_table(index="G",columns="round",values="err")
pairs=[]
for i in range(len(GOOD)):
    for j in range(i+1,len(GOOD)):
        z=piv[[GOOD[i],GOOD[j]]].dropna()
        if len(z)>5: pairs.append((GOOD[i],GOOD[j],len(z),np.corrcoef(z.iloc[:,0],z.iloc[:,1])[0,1]))
for a,b,n,r in pairs: print(f"  err({a}) vs err({b}): n={n:>3}  r={r:+.3f}")
mr=np.mean([p[3] for p in pairs])
kept=piv.dropna(thresh=2)
icc=kept.var(axis=1).mean()
print(f"\n  mean cross-round residual correlation: r={mr:+.3f}")
print(f"  within-group residual variance (mean): {icc:.2f} pts^2")
print("  => persistent per-occupation bias" if abs(mr)>0.3 else "  => NO persistent per-occupation bias: residuals are round-specific noise, not an occupation effect")
out["H2"]=round(float(mr),3)

hdr("H3  LEVEL BIAS - is the error related to where the cut-off sits?")
print(f"  corr(actual cut-off, error) = {np.corrcoef(g.actual,g.err)[0,1]:+.3f}")
print(f"  corr(pool size,      error) = {np.corrcoef(np.log1p(g['pool']),g.err)[0,1]:+.3f}")
print(f"  corr(allocation,     error) = {np.corrcoef(np.log1p(g.alloc),g.err)[0,1]:+.3f}")
out["H3"]=dict(level=round(float(np.corrcoef(g.actual,g.err)[0,1]),3),
               pool=round(float(np.corrcoef(np.log1p(g["pool"]),g.err)[0,1]),3))

hdr("H7  WHAT SETS A GROUP'S SHARE - demand (pool) or a fixed quota?")
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
psz=pf[pf.AsAt=="05/2026"].groupby("G").n.sum()
ps=(psz/psz.sum()).rename("pool_share")
cmp=pd.concat([S["2026-06"].rename("alloc_share"),ps],axis=1).dropna()
cmp=cmp[cmp.alloc_share>0]
print(f"  corr(allocation share, pool share) across {len(cmp)} groups : r={np.corrcoef(cmp.alloc_share,cmp.pool_share)[0,1]:.3f}")
print(f"  corr on logs                                          : r={np.corrcoef(np.log(cmp.alloc_share+1e-9),np.log(cmp.pool_share+1e-9))[0,1]:.3f}")
print(f"  corr(alloc share t, alloc share t-1)                  : r={np.corrcoef(S['2026-06'],S['2025-11'])[0,1]:.3f}")
print("\n  Allocation share tracks its OWN past far better than it tracks pool size, so the split behaves")
print("  like a persistent quota, not like demand-responsive rationing.")
out["H7"]=dict(vs_pool=round(float(np.corrcoef(cmp.alloc_share,cmp.pool_share)[0,1]),3),
               vs_own_past=round(float(np.corrcoef(S['2026-06'],S['2025-11'])[0,1]),3))

hdr("H8  SECTOR EFFECT - do ANZSCO major groups differ systematically?")
g2=g.copy(); g2["major"]=g2.G.str[0]
names={"1":"Managers","2":"Professionals","3":"Trades","4":"Community/Personal","5":"Clerical","6":"Sales","7":"Machinery","8":"Labourers"}
tab=g2.groupby("major").agg(n=("err","size"),mean_err=("err","mean"),mae=("err",lambda x:x.abs().mean()))
tab["sector"]=[names.get(i,i) for i in tab.index]
print(tab[["sector","n","mean_err","mae"]].to_string())
grps=[v.err.values for k,v in g2.groupby("major") if len(v)>=5]
if len(grps)>1:
    H=stats.kruskal(*grps)
    print(f"\n  Kruskal-Wallis across sectors: H={H.statistic:.2f}, p={H.pvalue:.4f}")
    print("  => sector effect present" if H.pvalue<0.05 else "  => NO significant sector effect")
    out["H8"]=round(float(H.pvalue),4)

hdr("H6  ROUND-SIZE EFFECT")
sizes={"2025-08":6450,"2025-11":9826,"2026-06":9748}
for r,s in sizes.items():
    z=d[d["round"]==r]
    print(f"  {r}  size {s:>6,}  exact {100*(z.err==0).mean():>3.0f}%  MAE {z.err.abs().mean():.2f}")
json.dump(out,open("hypotheses.json","w"),indent=1)
print("\n-> hypotheses.json written")
