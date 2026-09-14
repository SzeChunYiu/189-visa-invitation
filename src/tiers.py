"""Test the FOI'd four-tier model against invitation data it never saw."""
import pandas as pd, numpy as np, json, os, re
os.chdir(os.path.join(os.path.dirname(__file__),"..","data"))
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]; NEW=["2025-08","2025-11","2026-06"]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)
pf=pd.read_csv("poolfull_grp.csv"); pf=pf[pf.Score.astype(str).str.fullmatch(r"\d+")]
pf["n"]=pf.n.fillna(0); pf["G"]=pf.OccGroup.astype(str).str[:4]
names=pf.groupby("G").OccGroup.first(); pool=pf[pf.AsAt=="08/2026"].groupby("G").n.sum()

# Tiers as described in the FOI summary - assigned from ANZSCO structure, BEFORE looking at outcomes.
def tier(g):
    if g.startswith(("2531","2532","2533","2534","2535","2536","2537","2538","2539",
                     "2541","2542","2543","2544","2545","2546","2525","2524","2527")): return 1
    if g.startswith(("2411","2412","2413","2414","2415","2723","2725","2721")): return 2
    if g.startswith(("2211","2212")) or g.startswith(("261","262","263")) or g=="3513": return 4
    if g.startswith(("233","2321","2322","234","2713","2714","231","2347","2421","2422")) or g.startswith("3"): return 3
    return 3
gs=[g for g in pool.index if pool[g]>0]
df=pd.DataFrame({"G":gs})
df["tier"]=[tier(g) for g in df.G]
df["pool"]=[int(pool[g]) for g in df.G]
df["new_alloc"]=[int(sum(al.loc[g,r] for r in NEW)) if g in al.index else 0 for g in df.G]
df["old_alloc"]=[int(sum(al.loc[g,r] for r in ROUNDS[:2])) if g in al.index else 0 for g in df.G]
df["zero_now"]=(df.new_alloc==0).astype(int)
print("="*100); print("DOES THE FOI TIER MODEL PREDICT WHO GETS INVITED?  (tiers assigned from ANZSCO, not from outcomes)"); print("="*100)
t=df.groupby("tier").agg(groups=("G","size"),pool=("pool","sum"),
    invites_2025_26=("new_alloc","sum"),share_zero=("zero_now","mean"))
t["invites_per_1000_waiting"]=1000*t.invites_2025_26/t.pool
print(t.to_string(float_format=lambda v:f"{v:,.2f}"))
print("\n  Monotone in the predicted direction?",
      list(t.invites_per_1000_waiting) == sorted(t.invites_per_1000_waiting,reverse=True))
print("\n  Tier 4 (oversupplied: accountants, auditors, ICT, chefs)")
for g in df[df.tier==4].sort_values("pool",ascending=False).G[:8]:
    r=df[df.G==g].iloc[0]
    print(f"    {names.get(g,g)[:48]:<50} pool {r['pool']:>6,}  2024 {r.old_alloc:>4}  2025-26 {r.new_alloc:>4}")
print(f"\n  Tier 4 groups receiving ZERO in 2025-26: {int(df[df.tier==4].zero_now.sum())} of {int((df.tier==4).sum())}")
print("\n  WHERE THE TIER MODEL DOES NOT FIT - Tier 3 engineers, which should get a medium share:")
eng=[g for g in df.G if g.startswith("233")]
for g in sorted(eng,key=lambda z:-pool.get(z,0))[:6]:
    r=df[df.G==g].iloc[0]
    print(f"    {names.get(g,g)[:48]:<50} pool {r['pool']:>6,}  2024 {r.old_alloc:>4}  2025-26 {r.new_alloc:>4}")
print("\n  Tier 3 NON-engineering for contrast (trades and sciences):")
for g in ["3312","3411","2349","2347","2713"]:
    if g in df.G.values:
        r=df[df.G==g].iloc[0]
        print(f"    {names.get(g,g)[:48]:<50} pool {r['pool']:>6,}  2024 {r.old_alloc:>4}  2025-26 {r.new_alloc:>4}")
from scipy import stats
tab=pd.crosstab(df.tier,df.zero_now)
chi2,p,_,_=stats.chi2_contingency(tab)
print(f"\n  tier x (gets nothing) chi-square = {chi2:.1f}, p = {p:.5f}")
json.dump(dict(by_tier={int(k):dict(groups=int(v.groups),pool=int(v.pool),invites=int(v.invites_2025_26),
    groups_zero_year=round(float(v.share_zero),3),per_1000=round(float(v.invites_per_1000_waiting),2))
    for k,v in t.iterrows()},chi2=round(float(chi2),1),p=float(p),
    tier_of={g:int(tier(g)) for g in gs}),open("tiers.json","w"),indent=1)
print("\n  -> tiers.json written")
