import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
JOBS=[
 ("inv189only_occ_score.csv",[SM,("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY}>}} distinct %EOIID)")]),
 ("pool189_occ_score.csv",[("AsAt","As At Month"),("OccGroup","Occupation Group"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
 ("inv189only_occ4_score.csv",[SM,("Occupation","Occupation"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY}>}} distinct %EOIID)")]),
 ("pool189_occ4_latest.csv",[("Occupation","Occupation"),("Score","Score")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<28} cells={n:>7} total={sum((r[len(dims)] or 0) for r in rows):>12,.0f}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
