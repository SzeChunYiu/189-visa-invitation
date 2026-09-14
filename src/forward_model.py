"""Forward model on the TRUE date of effect (%EOIPBDateFrom), with expiry and points mobility."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
G="2349 Other Natural and Physical Science Professionals"
alloc=json.load(open("alloc_2349_allleg.json")); A=list(alloc.values())
cal=json.load(open("calibration_official.json")); mob=json.load(open("mobility.json"))
AHEAD_NOW=31           # verified unduplicated, 100% with date of effect before 10 Sep 2026
RATE=mob["entry_rate_2349"]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
q=num(pd.read_csv("q2349.csv")); q["n"]=q.n.fillna(0)
q=q[q.SubMonth.astype(str).str.match(r"\d{4}-\d{2}")]
ah=q[q.Score>=85].copy(); ah["lapse"]=pd.to_datetime(ah.SubMonth+"-01")+pd.DateOffset(years=2)

print("="*100); print("QUEUE POSITION ON THE TRUE DATE OF EFFECT"); print("="*100)
print(f"  ANZSCO 2349 pool at >=85 pts (08/2026, all legs)            : {AHEAD_NOW}")
print(f"  of which date of effect precedes 10 Sep 2026                : {AHEAD_NOW} (100%)")
print(f"  mean monthly entry into 2349's 85+ band                     : ~{RATE:.0f}")
print(f"  NOTE a points upgrade RESETS date of effect, so anyone reaching 85 after 10 Sep queues BEHIND.")
print(f"\n  {'round timing':<20}{'+ Sep entrants':>16}{'- lapsed':>10}{'rank':>7}{'allocation needed':>19}")
rows=[]
for lbl,d,sep in [("by 30 Sep 2026","2026-09-30",RATE*9/30),("by 31 Dec 2026","2026-12-31",RATE*9/30),
                  ("by 31 Mar 2027","2027-03-31",RATE*9/30)]:
    gone=ah[ah.lapse<=pd.Timestamp(d)].n.sum()
    rank=int(round(AHEAD_NOW+sep-gone+1))
    rows.append((lbl,rank))
    print(f"  {lbl:<20}{sep:>16.0f}{gone:>10.0f}{rank:>7}{('>= '+str(rank)):>19}")

print("\n"+"="*100); print("PROBABILITY"); print("="*100)
print(f"  allocation to 2349 by round: {A}")
w=np.array([2.0**(-(len(A)-1-i)) for i in range(len(A))]); w/=w.sum()
out={}
print(f"\n  {'round timing':<20}{'rank':>6}{'rounds covering':>18}{'unweighted':>12}{'recency-wtd':>13}")
for lbl,rank in rows:
    cov=np.array([a>=rank for a in A]); pu,pr=float(cov.mean()),float(w[cov].sum())
    out[lbl]=dict(rank=rank,covered=[bool(c) for c in cov],p_unweighted=round(pu,3),p_recency=round(pr,3))
    print(f"  {lbl:<20}{rank:>6}{f'{cov.sum()} of {len(A)}':>18}{pu:>11.0%}{pr:>13.0%}")
print(f"\n  Only the 43 and 87 allocations clear the Sep and Dec ranks. The Mar-2027 row turns on an exact")
print(f"  tie with the Aug-2025 allocation of 29 and should not be leaned on. The earlier '60-90% if it")
print(f"  slips past December' branch was an artefact of ranking on submission month, and does not survive")
print(f"  the correction to the true date of effect.")
print(f"\n  ==> P(invited | a round is held) = {out['by 30 Sep 2026']['p_unweighted']:.0%}"
      f"-{out['by 30 Sep 2026']['p_recency']:.0%}")
json.dump(dict(rank_by_date=out,alloc_hist=alloc,ahead_now=AHEAD_NOW,entry_rate=RATE,
               weights=[round(float(x),3) for x in w],calibration=cal,mobility=mob),
          open("forward_model.json","w"),indent=1)
print("\n  -> forward_model.json written")
