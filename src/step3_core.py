import asyncio, sys
from qlik import session
from hc import cube
V={"189":"189PTS Points-Tested Stream","190":"190SAS Skilled Australian Sponsored","491":"491SNR State or Territory Nominated - Regional"}
SM=("StatusMonth","=Date(MonthStart(%StatusDate),'YYYY-MM')")
SUBM=("SubMonth","=Date(MonthStart(%SubmittedOn),'YYYY-MM')")
JOBS=[]
for tag,v in V.items():
    JOBS += [
      (f"inv_score_{tag}.csv",[SM,("Score","Score")],
        [("n",f"Count({{<[Visa Type]={{'{v}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)")]),
      (f"lodg_score_{tag}.csv",[SM,("Score","Score")],
        [("n",f"Count({{<[Visa Type]={{'{v}'}},[EOI Status]={{'LODGED'}}>}} distinct %EOIID)")]),
      (f"pool_score_{tag}.csv",[("AsAt","As At Month"),("Score","Score")],
        [("n",f"Count({{<[Visa Type]={{'{v}'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
      (f"queue_{tag}.csv",[("Score","Score"),SUBM],
        [("n",f"Count({{<[Visa Type]={{'{v}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}>}} distinct %EOIID)")]),
    ]
async def one(job):
    out,dims,meas=job
    async def run(q,h):
        return await cube(q,h,dims,meas,out_csv=out)
    hdr,rows,n = await session(run)
    print(f"  wrote {out:<22} cells={n:>6}  total={sum(r[-1] or 0 for r in rows):>12,.0f}", flush=True)
async def main():
    for j in JOBS: await one(j)
asyncio.run(main())
