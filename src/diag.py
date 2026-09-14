import asyncio
from qlik import session
from hc import cube
INV="[EOI Status]={'INVITED'}"
async def run(q,h):
    print("### D1: INVITED legs - is exactly one leg 'still open' at status date?")
    hdr,rows,n=await cube(q,h,
      [("Visa","Visa Type"),("legstate","=If(%VisaCurrentTo>%StatusDate,'open','closed_at_or_before')")],
      [("eois",f"Count({{<{INV}>}} distinct %EOIID)"),("rows",f"Count({{<{INV}>}} %EOIID)")],
      out_csv="d1.csv")
    for r in sorted(rows): print(f"   {r[0]:<45} {r[1]:<22} eois={r[2] or 0:>9,.0f} rows={r[3] or 0:>10,.0f}")

    print("\n### D2: INVITED by Visa Type x Nominated State")
    hdr,rows,n=await cube(q,h,[("Visa","Visa Type"),("State","Nominated State")],
      [("eois",f"Count({{<{INV}>}} distinct %EOIID)")],out_csv="d2.csv")
    for r in sorted(rows,key=lambda x:(x[0],-(x[2] or 0))):
        if (r[2] or 0)>0 and r[0].startswith(("189","190","491")):
            print(f"   {r[0]:<45} {r[1]:<10} {r[2]:>9,.0f}")

    print("\n### D3: does %CombinedTo / %EOICurrentTo differ by leg for invited EOIs?")
    hdr,rows,n=await cube(q,h,
      [("Visa","Visa Type"),("combopen","=If(%CombinedTo>%StatusDate,'comb_open','comb_closed')")],
      [("eois",f"Count({{<{INV}>}} distinct %EOIID)")],out_csv="d3.csv")
    for r in sorted(rows):
        if r[0].startswith(("189","190","491")): print(f"   {r[0]:<45} {r[1]:<14} {r[2] or 0:>9,.0f}")
asyncio.run(session(run))
