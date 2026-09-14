"""All-leg invitation series per unit group per month -> per-group allocation via its own DiD baseline."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"
NO189=f"%EOIID=E({{<[Visa Type]={{'{V}'}}>}} %EOIID)"
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
JOBS=[
 # all-leg 189 invitations, and the no-189 control, per group per month
 ("alloc_all_grp.csv",[SM,("OccGroup","Occupation Group")],
  [("all189",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
   ("no189", f"Count({{<[EOI Status]={{'INVITED'}},{NO189}>}} distinct %EOIID)")]),
 # full (all-leg) pool per group per snapshot per score  - already have pool189_occ_score, but refresh with dates
 ("poolfull_grp.csv",[("AsAt","As At Month"),("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
 # all-leg invitations per group x score x round (for cut-off on the same basis as allocation)
 ("invfull_grp.csv",[SM,("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<20} cells={n:>7}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
