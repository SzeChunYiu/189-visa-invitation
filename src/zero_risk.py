"""P(your occupation group gets NOTHING in a round) - a gap the model did not price."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
GOOD=["2025-08","2025-11","2026-06"]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0)
inv["G"]=inv.OccGroup.astype(str).str[:4]
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
pool=pd.DataFrame({r:pf[pf.AsAt==PRIOR[r]].groupby("G").n.sum() for r in ROUNDS}).fillna(0)
groups=sorted(set(al.index)|set(pool.index))
al=al.reindex(groups,fill_value=0); pool=pool.reindex(groups,fill_value=0)

print("="*98); print("HOW OFTEN DOES A GROUP WITH PEOPLE WAITING GET ZERO INVITATIONS?"); print("="*98)
rows=[]
for r in ROUNDS:
    has=pool[r]>0
    zero=(al[r]==0)&has
    rows.append(dict(round=r,with_pool=int(has.sum()),got_zero=int(zero.sum()),
                     share=float(zero.sum()/max(1,has.sum()))))
for x in rows:
    print(f"  {x['round']}: {x['with_pool']:>3} groups had people waiting, {x['got_zero']:>3} got NOTHING  ({x['share']:.0%})")
rec=[x for x in rows if x["round"] in GOOD]
base=np.mean([x["share"] for x in rec])
print(f"\n  current-regime average: {base:.0%} of groups with a pool get nothing in a given round")

print("\n"+"="*98); print("IS IT RANDOM, OR DO THE SAME GROUPS KEEP MISSING OUT?"); print("="*98)
recent=al[GOOD]
haspool=pool[GOOD].gt(0).all(axis=1)
z=(recent==0)&pool[GOOD].gt(0)
cnt=z.sum(axis=1)[haspool]
print(f"  groups with a pool in all 3 recent rounds: {int(haspool.sum())}")
for k in range(4):
    print(f"    missed out in {k} of 3 rounds: {int((cnt==k).sum()):>3}")
print(f"\n  If zero-allocation were independent per round at {base:.0%}, you would expect")
exp=[(1-base)**3,3*base*(1-base)**2,3*base**2*(1-base),base**3]
for k,e in enumerate(exp): print(f"    missed in {k} of 3: {e*haspool.sum():.1f} expected vs {int((cnt==k).sum())} observed")
from scipy import stats
obs=[int((cnt==k).sum()) for k in range(4)]
expc=[e*haspool.sum() for e in exp]
chi=sum((o-e)**2/e for o,e in zip(obs,expc) if e>0)
print(f"\n  chi-square vs independent: {chi:.1f} on 3 df, p={1-stats.chi2.cdf(chi,3):.4f}")
print("  => zero-allocation is CLUSTERED, not random: the same groups keep getting nothing."
      if 1-stats.chi2.cdf(chi,3)<0.05 else "  => consistent with independent draws")

print("\n"+"="*98); print("WHAT PREDICTS GETTING NOTHING?"); print("="*98)
last=al["2026-06"]; prev=al["2025-11"]
p_now=pool["2026-06"]
df=pd.DataFrame({"zero":(last==0).astype(int),"prev_alloc":prev,"pool":p_now}).query("pool>0")
print(f"  P(zero | got nothing last round too)  = {df[df.prev_alloc==0].zero.mean():.0%}  (n={int((df.prev_alloc==0).sum())})")
print(f"  P(zero | got something last round)    = {df[df.prev_alloc>0].zero.mean():.0%}  (n={int((df.prev_alloc>0).sum())})")
big=df[df.pool>=df.pool.median()]
print(f"  P(zero | pool above median)           = {big.zero.mean():.0%}")
small=df[df.pool<df.pool.median()]
print(f"  P(zero | pool below median)           = {small.zero.mean():.0%}")
per={}
for g in groups:
    hp=[r for r in GOOD if pool.loc[g,r]>0]
    if not hp: continue
    per[g]=dict(rounds_with_pool=len(hp),zero=int(sum(al.loc[g,r]==0 for r in hp)),
                last_alloc=int(al.loc[g,"2026-06"]))
json.dump(dict(base_rate=round(float(base),3),per_group=per,
  p_zero_given_prev_zero=round(float(df[df.prev_alloc==0].zero.mean()),3),
  p_zero_given_prev_nonzero=round(float(df[df.prev_alloc>0].zero.mean()),3)),
  open("zero_risk.json","w"),indent=1)
z2349=per.get("2349")
print(f"\n  ANZSCO 2349: {z2349}")
print("\n  -> zero_risk.json written")
