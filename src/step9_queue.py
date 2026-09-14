"""2349 queue by score x submission month, and cohort survival for the expiry model."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"; G="2349 Other Natural and Physical Science Professionals"
SUBM=("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")
JOBS=[
 ("q2349.csv",[("Score","Score"),SUBM],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},[Occupation Group]={{'{G}'}}>}} distinct %EOIID)")]),
 # cohort survival: how much of each submission cohort is still SUBMITTED at each snapshot
 ("cohort_surv.csv",[("AsAt","As At Month"),SUBM],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<18} cells={n:>6} total={sum((r[len(dims)] or 0) for r in rows):>11,.0f}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
