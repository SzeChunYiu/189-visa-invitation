"""Points mobility: who upgrades, by how much, and what it does to queue position."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
mob=pd.read_csv("doe_mobility.csv"); mob["eois"]=mob.eois.fillna(0)
mob=mob[mob.delta.astype(str).str.fullmatch(r"-?\d+")].copy(); mob["delta"]=mob.delta.astype(int)
tot=mob.eois.sum(); changed=mob[mob.delta>0].eois.sum()
print("="*94); print("POINTS MOBILITY - do people lodge low and gain points later?  (189 pool, single-leg)"); print("="*94)
print(f"  EOIs in pool                      : {tot:>9,.0f}")
print(f"  whose score CHANGED over its life  : {changed:>9,.0f}  ({100*changed/tot:.1f}%)")
print(f"  {'points gained':<18}{'EOIs':>10}{'share':>9}{'share of movers':>18}")
for _,r in mob[mob.delta>0].sort_values("delta").iterrows():
    if r.eois<1: continue
    print(f"  {('+'+str(r.delta)):<18}{r.eois:>10,.0f}{100*r.eois/tot:>8.1f}%{100*r.eois/changed:>17.1f}%")
print(f"\n  mean gain among movers: {(mob[mob.delta>0].delta*mob[mob.delta>0].eois).sum()/changed:.1f} points")

b=pd.read_csv("mobility_band.csv"); b["eois"]=b.eois.fillna(0)
b=b[b.DoEMonth.astype(str).str.match(r"\d{4}-\d{2}")]
hi=b[b.band=="85+"].groupby("DoEMonth").eois.sum().sort_index()
print("\n"+"="*94); print("FLOW INTO THE 85+ BAND - by date of effect (whole 189 pool, snapshot 08/2026)"); print("="*94)
print("  date of effect of the CURRENT points, for everyone now sitting at 85+:")
for m,v in hi.tail(10).items(): print(f"   {m}: {v:>7,.0f}")
rec=hi.tail(6)
print(f"\n  mean monthly entry into 85+ over the last 6 months: {rec.mean():,.0f}")
print(f"  share of the whole 85+ pool whose points date from the last 6 months: "
      f"{100*rec.sum()/hi.sum():.0f}%")

d=pd.read_csv("doe_q2349.csv")
d=d[d.Score.astype(str).str.fullmatch(r"\d+")].copy(); d["Score"]=d.Score.astype(int)
d=d[d.DoEMonth.astype(str).str.match(r"\d{4}-\d{2}")]; d["all_legs"]=d.all_legs.fillna(0)
g=d[d.Score>=85].groupby("DoEMonth").all_legs.sum().sort_index()
rate=g.tail(4).mean()
print("\n"+"="*94); print("WHAT THIS DOES TO THE APPLICANT'S QUEUE POSITION (ANZSCO 2349)"); print("="*94)
print(f"  entries into 2349's 85+ band, recent months: {dict(g.tail(4).astype(int))}")
print(f"  mean ~{rate:.0f} per month")
print(f"\n  Confirmed ahead at 08/2026 (date of effect before 10 Sep) : 31")
print(f"  Expected additions with a date of effect in 1-9 Sep 2026   : ~{rate*9/30:.0f}")
print(f"  => realistic rank entering a late-Sep round                : ~{31+rate*9/30+1:.0f}")
print(f"\n  Anyone upgrading to 85+ AFTER 10 Sep takes a later date of effect and queues BEHIND.")
print(f"  Since 100% of the current 85+ cohort in 2349 acquired its points within the last year,")
print(f"  this band turns over fast - which is why the applicant's position stops eroding once lodged.")
json.dump(dict(pool=int(tot),changed=int(changed),pct_changed=round(100*changed/tot,1),
  dist={int(r.delta):int(r.eois) for _,r in mob.iterrows() if r.eois>0},
  entry_rate_2349=round(float(rate),1),rank_sep=int(round(31+rate*9/30+1))),
  open("mobility.json","w"),indent=1)
print("\n  -> mobility.json written")
