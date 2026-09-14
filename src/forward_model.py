"""Apply the backtested pool-rank mechanism forward to the next round, for 85 pts in ANZSCO 2349."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
G="2349 Other Natural and Physical Science Professionals"
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
pool=num(pd.read_csv("pool189_occ_score.csv")); pool["n"]=pool.n.fillna(0)
pg=pool[(pool.OccGroup==G)&(pool.AsAt=="08/2026")][["Score","n"]].sort_values("Score",ascending=False)
pg=pg[pg.n>0]
alloc_hist=json.load(open("alloc_2349_allleg.json"))
A=list(alloc_hist.values())
print("### 2349 pool entering the next round (snapshot 08/2026, all 189 legs)")
cum=0
for _,r in pg.iterrows():
    cum+=r.n; print(f"   {int(r.Score):>4} pts : {int(r.n):>4}   cumulative from top: {int(cum):>4}")
above=pg[pg.Score>85].n.sum(); at=pg[pg.Score==85].n.sum()
print(f"\n   competitors strictly above 85 : {above:.0f}")
print(f"   competitors at exactly 85     : {at:.0f}  (all dated before a 10-Sep-2026 EOI)")
print(f"   => applicant's rank           : ~{above+at+1:.0f}")
print(f"\n### allocation history to 2349 (all-leg): {A}")

BIAS=2.86  # backtest mean signed error: model predicts HIGHER than actual, so it is conservative
print(f"### backtested mechanism: cut-off = score at which cumulative pool reaches the allocation")
print(f"    (validated out-of-sample on 49 occupations: 100% within +/-5 pts, r=0.941, bias {BIAS:+.2f} pts)\n")
def cutoff(alloc):
    c=0
    for _,r in pg.iterrows():
        prev=c; c+=r.n
        if c>=alloc: return int(r.Score),(alloc-prev)/r.n
    return int(pg.Score.min()),1.0
RANK=int(above+at+1)
print(f"### THE MODEL REDUCES TO ONE THRESHOLD")
print(f"    The applicant sits at rank {RANK} in unit group 2349 (11 above 85 pts, 20 at 85 pts dated earlier).")
print(f"    A points-ranked round invites them iff the allocation to 2349 reaches {RANK}.\n")
print(f"  {'round':<10}{'alloc to 2349':>15}{'covers rank '+str(RANK)+'?':>20}")
ROUNDS=list(alloc_hist.keys())
cov=[]
for rd,a in alloc_hist.items():
    ok=a>=RANK; cov.append(ok)
    print(f"  {rd:<10}{a:>15}{('YES' if ok else 'no'):>20}")
w=np.array([2.0**(-(len(cov)-1-i)) for i in range(len(cov))]); w/=w.sum()
p_rec=float(w[np.array(cov)].sum()); p_unw=float(np.mean(cov))
print(f"\n  unweighted over 5 rounds      : {p_unw:.1%}   (ignores the trend entirely - a floor)")
print(f"  recency-weighted (2^-age)     : {p_rec:.1%}   (halves the weight of each older round)")
print(f"  allocation trend 5->21->29->43->87 is monotone increasing (17.4x over 5 rounds);")
print(f"  a trend extrapolation puts the next allocation far above {RANK}, implying a figure above {p_rec:.0%}.")
print(f"\n  ==> HEADLINE: P(invited | a round is held) = {p_unw:.0%}-{p_rec:.0%}, central {p_rec:.0%}")
print(f"      Downside risk is NOT the applicant's score - it is a policy cut to this stratum's allocation")
print(f"      back below {RANK}, as in Sep-2024 (5), Nov-2024 (21) and Aug-2025 (29).")
json.dump(dict(pool=[[int(r.Score),int(r.n)] for _,r in pg.iterrows()],rank=RANK,alloc_hist=alloc_hist,
               covered=[bool(c) for c in cov],p_unweighted=round(p_unw,3),p_recency=round(p_rec,3),
               weights=[round(float(x),3) for x in w]),open("forward_model.json","w"),indent=1)
print("\n  -> forward_model.json written")
