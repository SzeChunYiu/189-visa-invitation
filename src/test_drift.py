import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
async def sel(q,h,field,vals):
    f=await q.call("GetField",h,[field]); fh=f["qReturn"]["qHandle"]
    await q.call("SelectValues",fh,[[{"qText":v} for v in vals],False,True])
async def run(q,h):
    # restrict app state to the 189 legs of physics-group occupations -> small, fast Aggr
    await sel(q,h,"Visa Type",[V189])
    await sel(q,h,"Occupation Group",["2349 Other Natural and Physical Science Professionals"])
    hdr,rows,n=await cube(q,h,
      [("score_range","=Aggr(Max(Score)-Min(Score),%EOIID)")],
      [("eois","Count(distinct %EOIID)"),
       ("ever_invited","Count({<[EOI Status]={'INVITED'}>} distinct %EOIID)")],
      out_csv="drift_2349.csv")
    tot=sum(r[1] or 0 for r in rows); ti=sum(r[2] or 0 for r in rows)
    print("### A. per-EOI score range across ALL version-rows (unit group 2349, 189 leg)")
    print(f"{'range':>8}{'EOIs':>9}{'%':>8}{'everINV':>10}{'%INV':>8}")
    for r in sorted(rows,key=lambda x: float(x[0]) if str(x[0]).replace('-','').replace('.','').isdigit() else 999):
        e,i=(r[1] or 0),(r[2] or 0)
        print(f"{r[0]:>8}{e:>9,.0f}{100*e/tot:>7.1f}%{i:>10,.0f}{(100*i/ti if ti else 0):>7.1f}%")
    print(f"  TOTAL eois={tot:,.0f} ever_invited={ti:,.0f}")
asyncio.run(session(run))
