"""Re-run saturation using %EOIPBDateFrom (true date of effect) instead of %SubmittedOn."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V}'}}>}} %EOIID)"
I=f"[Visa Type]={{'{V}'}},[EOI Status]={{'INVITED'}},{ONLY}"
S=f"[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}},{ONLY}"
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
JOBS=[
 ("doe_inv_grp.csv",[SM,("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<{I}>}} distinct %EOIID)"),
   ("inv_doe_max",f"Max({{<{I}>}} %EOIPBDateFrom)"),("inv_doe_min",f"Min({{<{I}>}} %EOIPBDateFrom)")]),
 ("doe_pool_grp.csv",[("AsAt","As At Month"),("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<{S}>}} distinct %EOIID)"),
   ("pool_doe_max",f"Max({{<{S}>}} %EOIPBDateFrom)"),("pool_doe_min",f"Min({{<{S}>}} %EOIPBDateFrom)")]),
 # 2349 queue on date of effect: how many at >=85 have DOE before 10 Sep 2026
 ("doe_q2349.csv",[("Score","Score"),("DoEMonth","=Date(MonthStart(%EOIPBDateFrom),'YYYY-MM')")],
  [("n",f"Count({{<{S},[As At Month]={{'08/2026'}},[Occupation Group]={{'2349 Other Natural and Physical Science Professionals'}}>}} distinct %EOIID)"),
   ("all_legs",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}},[As At Month]={{'08/2026'}},[Occupation Group]={{'2349 Other Natural and Physical Science Professionals'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<20} cells={n:>7}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
