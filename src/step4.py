import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"
MULTI=f"%EOIID=P({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"
NO189=f"%EOIID=E({{<[Visa Type]={{'{V189}'}}>}} %EOIID)"
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
PHYS="[Occupation]={'234914 Physicist'}"
JOBS=[
 # true 189 round composition by score (unambiguous 189-only EOIs)
 ("inv189only_score.csv",[SM,("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY}>}} distinct %EOIID)")]),
 # multi-leg invited (ambiguous) and no-189 invited (pure state) for the DiD attribution
 ("inv_did.csv",[SM],
  [("multi189",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{MULTI}>}} distinct %EOIID)"),
   ("no189",   f"Count({{<[EOI Status]={{'INVITED'}},{NO189}>}} distinct %EOIID)")]),
 # FULL 189 competing pool by snapshot x score (all 189 legs, SUBMITTED)
 ("pool189_full.csv",[("AsAt","As At Month"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)"),
   ("only",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}},{ONLY}>}} distinct %EOIID)")]),
 # queue at latest snapshot: score x submission month (date-of-effect proxy)
 ("queue189_full.csv",[("Score","Score"),("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
 # physicist: pool by snapshot x score, and invitations
 ("phys_pool.csv",[("AsAt","As At Month"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}},{PHYS}>}} distinct %EOIID)")]),
 ("phys_inv.csv",[SM,("Score","Score")],
  [("all",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{PHYS}>}} distinct %EOIID)"),
   ("only",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY},{PHYS}>}} distinct %EOIID)")]),
 # occupation-group composition of the >=85 pool (for the null test on occupation effects)
 ("occ_pool85.csv",[("OccGroup","Occupation Group")],
  [("ge85",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},Score={{'>=85'}}>}} distinct %EOIID)"),
   ("inv_jun26",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY},%StatusDate={{'>=44000'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<24} cells={n:>6} total={sum((r[len(dims)] or 0) for r in rows):>12,.0f}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
