"""Does the tie-break date bind only at the marginal score, or at every score?"""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V}'}}>}} %EOIID)"
SUBM=("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")
JOBS=[
 # invitations in the Jun-2026 round, by score x submission month
 ("tb_inv_bymonth.csv",[("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')"),("Score","Score"),SUBM],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'INVITED'}},{ONLY}>}} distinct %EOIID)")]),
 # the pool standing just before that round, same grain
 ("tb_pool_may26.csv",[("Score","Score"),SUBM],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[As At Month]={{'05/2026'}},[EOI Status]={{'SUBMITTED'}},{ONLY}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<22} cells={n:>5}  total={sum((r[len(dims)] or 0) for r in rows):>9,.0f}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
