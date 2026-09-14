import asyncio
from qlik import session
from hc import cube
V9="189PTS Points-Tested Stream"; V0="190SAS Skilled Australian Sponsored"; V1="491SNR State or Territory Nominated - Regional"
async def run(q,h):
    hdr,rows,n = await cube(q,h,[("m","=Date(MonthStart(%StatusDate),'YYYY-MM')")],
      [("inv_189", f"Count({{<[Visa Type]={{'{V9}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
       ("inv_190", f"Count({{<[Visa Type]={{'{V0}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
       ("inv_491", f"Count({{<[Visa Type]={{'{V1}'}},[EOI Status]={{'INVITED'}}>}} distinct %EOIID)"),
       ("inv_ANYVISA", "Count({<[EOI Status]={'INVITED'}>} distinct %EOIID)"),
       ("inv_189_ONLYLEG", f"Count({{<[EOI Status]={{'INVITED'}},[Visa Type]={{'{V9}'}}>}} distinct %EOIID)"
                           f"-Count({{<[EOI Status]={{'INVITED'}},[Visa Type]={{'{V9}','{V0}','{V1}'}}>}} distinct %EOIID)"
                           f"+Count({{<[EOI Status]={{'INVITED'}},[Visa Type]={{'{V0}','{V1}'}}>}} distinct %EOIID)")],
      out_csv="overlap.csv")
    print(f"{'month':<9}{'189':>8}{'190':>8}{'491':>8}{'sum':>9}{'ANY(distinct)':>15}{'overlap%':>10}")
    for r in sorted(rows,key=lambda x:x[0]):
        if not str(r[0]).startswith("202"): continue
        a,b,c,anyv = (r[1] or 0),(r[2] or 0),(r[3] or 0),(r[4] or 0)
        s=a+b+c
        if anyv==0: continue
        print(f"{r[0]:<9}{a:>8,.0f}{b:>8,.0f}{c:>8,.0f}{s:>9,.0f}{anyv:>15,.0f}{100*(s-anyv)/anyv:>9.0f}%")
asyncio.run(session(run))
