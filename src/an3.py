import pandas as pd, numpy as np
pd.set_option("display.width",250,"display.max_columns",60)
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}

def num(df,col="Score"):
    df=df[df[col].astype(str).str.fullmatch(r"\d+")].copy(); df[col]=df[col].astype(int); return df

inv=num(pd.read_csv("inv189only_occ4_score.csv")); inv["n"]=inv.n.fillna(0)
pool=num(pd.read_csv("pool189_occ4_latest.csv")); pool["n"]=pool.n.fillna(0)
poolg=num(pd.read_csv("pool189_occ_score.csv")); poolg["n"]=poolg.n.fillna(0)
invg=num(pd.read_csv("inv189only_occ_score.csv")); invg["n"]=invg.n.fillna(0)

print("### 1. Occupation-conditional MINIMUM invited score per round (189-only, occ>=20 invites)")
r=inv[inv.StatusMonth.isin(ROUNDS)]
tab=r.groupby(["Occupation","StatusMonth"]).apply(lambda g:pd.Series({
    "min":g.loc[g.n>0,"Score"].min(),"tot":g.n.sum()}),include_groups=False).reset_index()
big=tab[tab.tot>=20]
piv=big.pivot(index="Occupation",columns="StatusMonth",values="min")
tot=big.groupby("Occupation").tot.sum().sort_values(ascending=False)
print("\n  --- 12 LARGEST occupations (min invited score per round) ---")
print(piv.loc[[o for o in tot.index[:12]]].to_string())
print("\n  --- spread of Jun-2026 min invited score across occupations ---")
j=big[big.StatusMonth=="2026-06"]["min"]
print(f"    n_occupations={len(j)}  min={j.min():.0f}  p25={j.quantile(.25):.0f}  median={j.median():.0f}  p75={j.quantile(.75):.0f}  max={j.max():.0f}")
print("    => occupation stratification CONFIRMED" if j.max()-j.min()>=15 else "    => no stratification")

print("\n### 2. PHYSICIST 234914 - pool vs invitations")
ph=pd.read_csv("phys_pool.csv"); ph=num(ph); ph["n"]=ph.n.fillna(0)
lp=ph[ph.AsAt=="08/2026"].set_index("Score").n
print("  pool at 08/2026 by score:", {int(k):int(v) for k,v in lp.sort_index(ascending=False).items() if v>0})
pi=inv[inv.Occupation=="234914 Physicist"]
pv=pi[pi.StatusMonth.isin(ROUNDS)].pivot_table(index="StatusMonth",columns="Score",values="n",aggfunc="sum").fillna(0)
pv=pv[sorted(pv.columns,reverse=True)]
print("\n  189-ONLY invitations (unambiguous) by round x score:")
print(pv.astype(int).to_string())

print("\n### 3. Physicist pool at 85+ over time (is the queue clearing?)")
for m in ["05/2026","06/2026","07/2026","08/2026"]:
    s=ph[ph.AsAt==m]
    print(f"   {m}: =85 -> {s[s.Score==85].n.sum():>4.0f}   >85 -> {s[s.Score>85].n.sum():>4.0f}   total -> {s.n.sum():>5.0f}")

print("\n### 4. HAZARD at 85pts: invited / pool-just-before, Physicist vs unit group 2349 vs ALL")
g2349=[g for g in poolg.OccGroup.unique() if str(g).startswith("2349")]
print("   unit group for physicist:",g2349)
for label,ip,pp in [("Physicist",pi,ph),
                    ("Grp 2349",invg[invg.OccGroup.isin(g2349)],poolg[poolg.OccGroup.isin(g2349)]),
                    ("ALL occs",invg,poolg)]:
    print(f"\n   -- {label} --")
    for rd in ROUNDS:
        pm=PRIOR[rd]
        pool85=pp[(pp.AsAt==pm)&(pp.Score==85)].n.sum()
        inv85 =ip[(ip.StatusMonth==rd)&(ip.Score==85)].n.sum()
        pool_ge=pp[(pp.AsAt==pm)&(pp.Score>=85)].n.sum()
        inv_ge =ip[(ip.StatusMonth==rd)&(ip.Score>=85)].n.sum()
        h85 = 100*inv85/pool85 if pool85 else float('nan')
        hge = 100*inv_ge/pool_ge if pool_ge else float('nan')
        print(f"      {rd}: pool85(prior {pm})={pool85:>7,.0f} inv85={inv85:>6,.0f} hazard85={h85:>6.1f}%"
              f" | pool>=85={pool_ge:>7,.0f} inv>=85={inv_ge:>6,.0f} hazard>=85={hge:>5.1f}%")
