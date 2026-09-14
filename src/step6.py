import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"
PH="[Occupation]={'234914 Physicist'}"
JOBS=[
 # consistent 189-ONLY pool by occupation x score x snapshot
 ("pool189only_occ4.csv",[("AsAt","As At Month"),("Occupation","Occupation"),("Score","Score")],
  [("only",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}},{ONLY}>}} distinct %EOIID)")]),
 # submission-month profile of the CURRENT 189 pool (does coverage start Sep-2024?)
 ("subprofile.csv",[("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")],
  [("pool_all",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)"),
   ("pool85",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},Score={{85}}>}} distinct %EOIID)"),
   ("phys85",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},Score={{85}},{PH}>}} distinct %EOIID)")]),
 # physicist queue detail: score x submission month at latest snapshot
 ("phys_queue.csv",[("Score","Score"),("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},{PH}>}} distinct %EOIID)")]),
 # atomic point components for the >=85 physicist-group pool (reconciliation)
 ("atoms_phys.csv",[("Score","Score"),("Eng","English Test Score"),("Partner","PartnerSkills Score"),
                    ("AusStudy","Australian Study Flag"),("Regional","Regional Study"),
                    ("CommLang","Comm Language Qual"),("Specialist","Specialist Education"),("ProfYear","Professional Year")],
  [("n",f"Count({{<[Visa Type]={{'{V189}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}},{PH}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<26} cells={n:>7} total={sum((r[len(dims)] or 0) for r in rows):>12,.0f}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
