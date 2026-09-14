"""Unduplicated rank on true date of effect, plus points-mobility (upgrade) rates."""
import asyncio, sys, pathlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from qlik import session
from hc import cube
V="189PTS Points-Tested Stream"; G="2349 Other Natural and Physical Science Professionals"
S=f"[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}},[As At Month]={{'08/2026'}}"
S2349=f"{S},[Occupation Group]={{'{G}'}}"
async def run(q,h):
    print("### A. unduplicated 2349 pool at 08/2026, split by date of effect vs 10-Sep-2026")
    hdr,rows,n=await cube(q,h,
      [("Score","Score"),("doe","=If(%EOIPBDateFrom<MakeDate(2026,9,10),'ahead (DoE before 10 Sep)','behind')")],
      [("eois",f"Count({{<{S2349}>}} distinct %EOIID)")],out_csv="rank_doe.csv")
    tot={}
    for r in rows:
        if not str(r[0]).isdigit(): continue
        s=int(r[0])
        if s>=85: tot[r[1]]=tot.get(r[1],0)+(r[2] or 0)
    for k,v in sorted(tot.items()): print(f"   {k:<32} {v:>5,.0f}")
    print("\n### B. control: same cell counted WITHOUT the date split (detects double counting)")
    hdr,rows,n=await cube(q,h,[("Score","Score")],
      [("eois",f"Count({{<{S2349}>}} distinct %EOIID)")],out_csv="rank_plain.csv")
    ge=sum((r[1] or 0) for r in rows if str(r[0]).isdigit() and int(r[0])>=85)
    print(f"   2349 pool at >=85, single count: {ge:,.0f}")
    print(f"   sum of the split above          : {sum(tot.values()):,.0f}   "
          f"-> {'MATCHES (no double count)' if abs(ge-sum(tot.values()))<0.5 else 'DOUBLE COUNTED by %.0f'%(sum(tot.values())-ge)}")

    print("\n### C. points mobility: monthly flow of 189 EOIs INTO the 85+ band, whole pool")
    hdr,rows,n=await cube(q,h,
      [("DoEMonth","=Date(MonthStart(%EOIPBDateFrom),'YYYY-MM')"),
       ("band","=If(Score>=85,'85+','below 85')")],
      [("eois",f"Count({{<[Visa Type]={{'{V}'}},[EOI Status]={{'SUBMITTED'}},[As At Month]={{'08/2026'}}>}} distinct %EOIID)")],
      out_csv="mobility_band.csv")
    print("   (written to mobility_band.csv)")
asyncio.run(session(run))
