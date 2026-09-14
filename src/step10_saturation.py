"""Saturation test: was a (occupation, score) cell fully exhausted in a round?
If the newest-dated EOI at that score was invited, everyone at that score was invited."""
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
 # invited: count + newest/oldest submission date, per round x unit group x score
 ("sat_inv_grp.csv",[SM,("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<{I}>}} distinct %EOIID)"),
   ("maxsub",f"Max({{<{I}>}} %SubmittedOn)"),("minsub",f"Min({{<{I}>}} %SubmittedOn)")]),
 # pool: same, per snapshot
 ("sat_pool_grp.csv",[("AsAt","As At Month"),("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<{S}>}} distinct %EOIID)"),
   ("maxsub",f"Max({{<{S}>}} %SubmittedOn)"),("minsub",f"Min({{<{S}>}} %SubmittedOn)")]),
 # same at 6-digit occupation level, invited only (for the per-occupation database)
 ("sat_inv_occ.csv",[SM,("Occupation","Occupation"),("Score","Score")],
  [("n",f"Count({{<{I}>}} distinct %EOIID)"),
   ("maxsub",f"Max({{<{I}>}} %SubmittedOn)"),("minsub",f"Min({{<{I}>}} %SubmittedOn)")]),
 ("sat_pool_occ.csv",[("AsAt","As At Month"),("Occupation","Occupation"),("Score","Score")],
  [("n",f"Count({{<{S}>}} distinct %EOIID)"),("maxsub",f"Max({{<{S}>}} %SubmittedOn)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<20} cells={n:>7}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
