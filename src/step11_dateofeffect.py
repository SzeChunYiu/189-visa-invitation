"""Do the SCD interval columns carry the true date of effect (points-change date)?"""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V}'}}>}} %EOIID)"
CUR=f"[Visa Type]={{'{V}'}},[As At Month]={{'08/2026'}},[EOI Status]={{'SUBMITTED'}}"
async def run(q,h):
    print("### A. how far does each date column sit after %SubmittedOn? (189 pool, 08/2026)")
    hdr,rows,n=await cube(q,h,
      [("lag_bucket","=Class(Floor(%EOIPBDateFrom)-Floor(%SubmittedOn),30)")],
      [("eois",f"Count({{<{CUR}>}} distinct %EOIID)")],out_csv="doe_lag.csv")
    tot=sum(r[1] or 0 for r in rows)
    def lo(x):
        try: return float(str(x).split("<=")[0].strip("[ "))
        except: return 1e9
    for r in sorted(rows,key=lambda x:lo(x[0]))[:14]:
        print(f"   days after submission {str(r[0]):<22} {r[1] or 0:>9,.0f}  ({100*(r[1] or 0)/tot:>5.1f}%)")
    print(f"   total {tot:,.0f}")

    print("\n### B. do the four interval columns agree with each other?")
    hdr,rows,n=await cube(q,h,
      [("cmp","=If(Floor(%EOIPBDateFrom)=Floor(%CombinedFrom),'PB=Combined','PB<>Combined')"),
       ("cmp2","=If(Floor(%EOIPBDateFrom)=Floor(%SubmittedOn),'PB=Submitted','PB<>Submitted')")],
      [("eois",f"Count({{<{CUR}>}} distinct %EOIID)")],out_csv="doe_cmp.csv")
    for r in sorted(rows): print(f"   {r[0]:<16} {r[1]:<16} {r[2] or 0:>9,.0f}")

    print("\n### C. points mobility: EOIs whose CURRENT score differs from their FIRST observed score")
    hdr,rows,n=await cube(q,h,
      [("delta","=Aggr(Max(Score)-Min(Score),%EOIID)")],
      [("eois",f"Count({{<{CUR},{ONLY}>}} distinct %EOIID)")],out_csv="doe_mobility.csv")
    t=sum(r[1] or 0 for r in rows)
    for r in sorted(rows,key=lambda x: float(x[0]) if str(x[0]).lstrip('-').replace('.','').isdigit() else 999):
        if (r[1] or 0)>0: print(f"   score range {str(r[0]):>5} : {r[1]:>9,.0f}  ({100*r[1]/t:>5.1f}%)")
asyncio.run(session(run))
