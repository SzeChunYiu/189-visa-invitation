import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
ONLY=f"%EOIID=E({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"      # EOIs with NO non-189 leg
MULTI=f"%EOIID=P({{<[Visa Type]-={{'{V189}'}}>}} %EOIID)"     # EOIs WITH some other leg
async def run(q,h):
    hdr,rows,n=await cube(q,h,[("m","=Date(MonthStart(%StatusDate),'YYYY-MM')")],
      [("inv189_all",  f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
       ("inv189_only", f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{ONLY}>}} distinct %EOIID)"),
       ("inv189_multi",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'INVITED'}},{MULTI}>}} distinct %EOIID)"),
       ("pool189_only",f"Count({{<[Visa Type]={{'{V189}'}},[EOI Status]={{'SUBMITTED'}},{ONLY}>}} distinct %EOIID)")],
      out_csv="only189_check.csv")
    print(f"{'month':<9}{'all':>8}{'only':>8}{'multi':>8}{'only+multi':>12}{'identity':>10}")
    ok=True
    for r in sorted(rows,key=lambda x:str(x[0])):
        if not str(r[0]).startswith("202"): continue
        a,o,m=(r[1] or 0),(r[2] or 0),(r[3] or 0)
        good = abs(a-(o+m))<0.5
        ok &= good
        print(f"{r[0]:<9}{a:>8,.0f}{o:>8,.0f}{m:>8,.0f}{o+m:>12,.0f}{'OK' if good else ' MISMATCH':>10}")
    print("\nIDENTITY all == only+multi :", "PASS" if ok else "FAIL")
asyncio.run(session(run))
