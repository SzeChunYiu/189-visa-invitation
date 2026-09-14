"""Date-of-effect queue for every unit group, plus the points-component mix of the competition."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"
CUR=f"[Visa Type]={{'{V}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}"
DOE=("DoEMonth","=Date(MonthStart(%EOIPBDateFrom),'YYYY-MM')")
JOBS=[
 # queue by date of effect, every group - lets a user place themselves exactly in their score band
 ("doe_all_grp.csv",[("OccGroup","Occupation Group"),("Score","Score"),DOE],
  [("n",f"Count({{<{CUR}>}} distinct %EOIID)")]),
 # what the competition's points are actually made of
 ("atoms_eng.csv",[("OccGroup","Occupation Group"),("Score","Score"),("Eng","English Test Score")],
  [("n",f"Count({{<{CUR}>}} distinct %EOIID)")]),
 ("atoms_partner.csv",[("OccGroup","Occupation Group"),("Score","Score"),("Partner","PartnerSkills Score")],
  [("n",f"Count({{<{CUR}>}} distinct %EOIID)")]),
 ("atoms_study.csv",[("OccGroup","Occupation Group"),("Score","Score"),("AusStudy","Australian Study Flag")],
  [("n",f"Count({{<{CUR}>}} distinct %EOIID)")]),
 # the state-nominated alternatives, by state
 ("state_alt.csv",[("Visa","Visa Type"),("OccGroup","Occupation Group"),("State","Nominated State")],
  [("n",f"Count({{<[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out,page_cells=9000)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<22} cells={n:>7}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
