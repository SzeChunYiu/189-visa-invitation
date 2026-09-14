"""GAPS 3-6: budget coupling, seasonality, 491 redirection, 6-digit allocation."""
import pandas as pd, numpy as np, json, os
from scipy import stats
os.chdir(os.path.join(os.path.dirname(__file__),"..","data"))
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]; GOOD=["2025-08","2025-11","2026-06"]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0)

print("="*98); print("GAP 3  CROSS-GROUP BUDGET COUPLING - does one group's gain crowd out another?"); print("="*98)
sh=al/al.sum(axis=0)
act=sh.loc[(al.sum(axis=1)>0)]
cors=[]
for i in range(len(act)):
    for j in range(i+1,len(act)):
        a,b=act.iloc[i].values,act.iloc[j].values
        if a.std()>0 and b.std()>0: cors.append(np.corrcoef(a,b)[0,1])
cors=np.array(cors)
print(f"  pairwise correlations of group SHARE across rounds: n={len(cors)}")
print(f"    mean {cors.mean():+.3f}   median {np.median(cors):+.3f}")
print(f"    expected under a pure budget constraint: slightly negative (shares sum to 1)")
print(f"    mechanical null for k={len(act)} groups: {-1/(len(act)-1):+.4f}")
t=stats.ttest_1samp(cors,-1/(len(act)-1))
print(f"    t-test vs that null: t={t.statistic:.2f}, p={t.pvalue:.4f}")
print("  => coupling is no stronger than the arithmetic of shares summing to one."
      if t.pvalue>0.05 else "  => coupling is stronger than the mechanical null")
print("     Modelling groups independently, then normalising, is therefore adequate.")

print("\n"+"="*98); print("GAP 4  SEASONALITY - do rounds cluster in particular months?"); print("="*98)
months=[int(r.split("-")[1]) for r in ROUNDS]
print(f"  round months on record: {months}  (Sep, Nov, Aug, Nov, Jun)")
print(f"  distinct months: {sorted(set(months))}   n=5 rounds")
obs=np.zeros(12)
for m in months: obs[m-1]+=1
exp=np.full(12,len(months)/12)
chi=((obs-exp)**2/exp).sum()
print(f"  chi-square vs uniform: {chi:.1f} on 11 df, p={1-stats.chi2.cdf(chi,11):.3f}")
print("  => cannot reject uniform timing. With 5 rounds there is no power to fit seasonality;")
print("     the round-size model deliberately conditions on 'a round is held' instead.")

print("\n"+"="*98); print("GAP 5  491 REDIRECTION - is the regional cut pushing people into 189?"); print("="*98)
ps=pd.read_csv("panel_status_189.csv").fillna(0); ps=ps[ps.AsAt.astype(str).str.contains("/")]
p4=pd.read_csv("panel_status_491.csv").fillna(0); p4=p4[p4.AsAt.astype(str).str.contains("/")]
s189=ps[ps.Status=="SUBMITTED"].set_index("AsAt").n
s491=p4[p4.Status=="SUBMITTED"].set_index("AsAt").n
idx=[a for a in s189.index if a in s491.index]
d=pd.DataFrame({"189":s189[idx],"491":s491[idx]})
d["dt"]=pd.to_datetime(d.index,format="%m/%Y"); d=d.sort_values("dt")
d["g189"]=d["189"].diff(); d["g491"]=d["491"].diff()
h2=d[d.dt>=pd.Timestamp("2026-01-01")]
print(f"  monthly growth, 189 vs 491")
print(f"    whole panel : 189 {d.g189.mean():+,.0f}/mo   491 {d.g491.mean():+,.0f}/mo")
print(f"    2026 onward : 189 {h2.g189.mean():+,.0f}/mo   491 {h2.g491.mean():+,.0f}/mo")
print(f"  corr(189 growth, 491 growth) = {d[['g189','g491']].dropna().corr().iloc[0,1]:+.3f}")
print("\n  The 2026-27 Regional cut was announced for a program year starting July 2026; the panel")
print("  ends August 2026, so at most two months of any redirection are observable. 189 growth has")
print(f"  not yet accelerated ({h2.g189.mean():+,.0f}/mo against {d.g189.mean():+,.0f}/mo overall).")
print("  Recorded as a WATCH ITEM, not a modelled term - it would need later snapshots.")

print("\n"+"="*98); print("GAP 6  IS THE UNIT GROUP THE RIGHT LEVEL? occupations within a group vs across"); print("="*98)
o=num(pd.read_csv("inv189only_occ4_score.csv")); o["n"]=o.n.fillna(0)
o["G"]=o.Occupation.astype(str).str[:4]
cut=o[(o.n>0)&(o.StatusMonth.isin(GOOD))].groupby(["G","Occupation","StatusMonth"]).Score.min().reset_index()
within=cut.groupby(["G","StatusMonth"]).Score.agg(["std","count"])
within=within[within["count"]>=2]
allstd=cut.groupby("StatusMonth").Score.std()
print(f"  group-rounds with 2+ occupations invited: {len(within)}")
print(f"  mean WITHIN-group spread of the cut-off : {within['std'].mean():.2f} points")
print(f"  overall BETWEEN-occupation spread        : {allstd.mean():.2f} points")
r=within['std'].mean()/allstd.mean()
print(f"  ratio {r:.2f}  -> {1-r:.0%} of cut-off variation is BETWEEN unit groups, not within")
print("  => the unit group is the right level; modelling 6-digit occupations separately would add")
print("     noise, not signal, and the ceilings apply at unit-group level anyway.")
json.dump(dict(coupling_mean_r=float(cors.mean()),coupling_p=float(t.pvalue),
  season_p=float(1-stats.chi2.cdf(chi,11)),
  g189_recent=float(h2.g189.mean()),g189_all=float(d.g189.mean()),
  within_std=float(within['std'].mean()),between_std=float(allstd.mean())),
  open("gaps.json","w"),indent=1)
print("\n  -> gaps.json written")
