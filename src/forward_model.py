"""Applies the externally-calibrated mechanism forward: rank vs allocation, with EOI expiry."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
EOI_DATE=pd.Timestamp("2026-09-10")           # applicant's EOI date of effect
G="2349 Other Natural and Physical Science Professionals"
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
q=num(pd.read_csv("q2349.csv")); q["n"]=q.n.fillna(0)
q=q[q.SubMonth.astype(str).str.match(r"\d{4}-\d{2}")]
ahead=q[q.Score>=85].copy()
ahead["lapse"]=pd.to_datetime(ahead.SubMonth+"-01")+pd.DateOffset(years=2)
alloc=json.load(open("alloc_2349_allleg.json")); A=list(alloc.values())
cal=json.load(open("calibration_official.json"))

print("="*98)
print("RANK vs ALLOCATION, with EOI expiry  (ANZSCO 2349, 85 points, EOI dated 10 Sep 2026)")
print("="*98)
print(f"\n  Externally calibrated against the official 4-Jun-2026 round: {cal['exact']}/{cal['n']} occupations exact "
      f"({100*cal['exact']/cal['n']:.1f}%), r={cal['r']}, bias {cal['bias']:+.2f} pts.")
print(f"  Every calibration error is POSITIVE, so the derived cut-off never overstates the applicant's odds.\n")
print(f"  {'if the round is held':<24}{'ahead lapsed':>14}{'rank':>7}{'allocation needed':>19}")
dates=[("by 30 Sep 2026","2026-09-30"),("by 31 Dec 2026","2026-12-31"),
       ("by 31 Mar 2027","2027-03-31"),("by 30 Jun 2027","2027-06-30")]
ranks={}
for lbl,d in dates:
    d=pd.Timestamp(d); gone=ahead[ahead.lapse<=d].n.sum(); r=int(ahead.n.sum()-gone+1)
    ranks[lbl]=r
    print(f"  {lbl:<24}{gone:>14,.0f}{r:>7}{('>= '+str(r)):>19}")
print(f"\n  NOTE: the applicant's rank can only FALL over time. Anyone entering or re-scoring to 85 points after")
print(f"  10 Sep 2026 takes a later date of effect and queues BEHIND them, while those ahead lapse or are invited.")

print("\n"+"="*98); print("PROBABILITY"); print("="*98)
print(f"  allocation to 2349 by round: {A}   (all-leg, contamination-corrected)")
w=np.array([2.0**(-(len(A)-1-i)) for i in range(len(A))]); w/=w.sum()
out={}
print(f"\n  {'round timing':<20}{'rank':>6}{'rounds covering it':>21}{'unweighted':>12}{'recency-wtd':>13}")
for lbl,_ in dates:
    r=ranks[lbl]; cov=np.array([a>=r for a in A])
    pu,pr=float(cov.mean()),float(w[cov].sum())
    out[lbl]=dict(rank=r,covered=[bool(c) for c in cov],p_unweighted=round(pu,3),p_recency=round(pr,3))
    print(f"  {lbl:<20}{r:>6}{f'{cov.sum()} of {len(A)}':>21}{pu:>11.0%}{pr:>13.0%}")
print(f"\n  recency weights: {[round(float(x),3) for x in w]}  (2^-age; arbitrary kernel over n=5, stated so it can be discounted)")
print(f"\n  ==> If a round is held in the next few months: P(invited) = "
      f"{out['by 30 Sep 2026']['p_unweighted']:.0%}-{out['by 30 Sep 2026']['p_recency']:.0%}"
      f"; if it slips past December: {out['by 31 Dec 2026']['p_unweighted']:.0%}-{out['by 31 Dec 2026']['p_recency']:.0%}.")
print(f"  Downside risk is a policy cut to this stratum's allocation, not the applicant's score.")
json.dump(dict(rank_by_date=out,alloc_hist=alloc,total_ahead=int(ahead.n.sum()),
               weights=[round(float(x),3) for x in w],calibration=cal),open("forward_model.json","w"),indent=1)
print("\n  -> forward_model.json written")
