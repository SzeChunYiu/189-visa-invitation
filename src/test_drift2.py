import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"
async def run(q,h):
    print("### B1. Is the INVITED row's validity interval consistent with its StatusDate?")
    hdr,rows,n=await cube(q,h,
      [("contained","=If(%StatusDate>=%CombinedFrom and %StatusDate<=%CombinedTo,'status_inside_version','status_OUTSIDE_version')")],
      [("eois",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
       ("rows",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}}>}} %EOIID)")],
      out_csv="b1_containment.csv")
    for r in sorted(rows): print(f"   {r[0]:<28} eois={r[1] or 0:>9,.0f} rows={r[2] or 0:>10,.0f}")
asyncio.run(session(run))
