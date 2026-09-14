"""Stratum-specific DiD for 2349 all-leg allocation, and 190/491 standing for physicists."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream";V190="190SAS Skilled Australian Sponsored";V491="491SNR State or Territory Nominated - Regional"
G="2349 Other Natural and Physical Science Professionals"
NO189=f"%EOIID=E({{<[Visa Type]={{'{V189}'}}>}} %EOIID)"
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
PH="[Occupation]={'234914 Physicist'}"
JOBS=[
 ("did_2349.csv",[SM],
  [("all189_2349",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},[Occupation Group]={{'{G}'}}>}} distinct %EOIID)"),
   ("no189_2349", f"Count({{<[EOI Status]={{'INVITED'}},[Occupation Group]={{'{G}'}},{NO189}>}} distinct %EOIID)")]),
 ("phys_190_491.csv",[("Visa","Visa Type"),("Score","Score"),("Status","EOI Status")],
  [("n",f"Count({{<[As At Month]={{'08/2026'}},{PH}>}} distinct %EOIID)")]),
]
async def one(job):
    out,dims,meas=job
    async def run(q,h): return await cube(q,h,dims,meas,out_csv=out)
    hdr,rows,n=await session(run)
    print(f"  wrote {out:<20} cells={n}",flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
