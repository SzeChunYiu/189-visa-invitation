import asyncio
from qlik import session
from hc import cube
V189="189PTS Points-Tested Stream"
S="[Visa Type]={'%s'},[As At Month]={'08/2026'},[EOI Status]={'SUBMITTED'}" % V189
async def run(q,h):
    # A: direct small-cell read for Physicist by score
    hdr,rows,n = await cube(q,h,[("Score","Score")],
        [("direct", f"Count({{<{S},[Occupation]={{'234914 Physicist'}}>}} distinct %EOIID)"),
         # B: complement trick -> ALL minus ALL-except-Physicist
         ("all",     f"Count({{<{S}>}} distinct %EOIID)"),
         ("notphys", f"Count({{<{S},[Occupation]-={{'234914 Physicist'}}>}} distinct %EOIID)")],
        out_csv="suppress_test.csv")
    print(f"{'Score':<7}{'direct':>9}{'all':>10}{'notPhys':>10}{'all-notPhys':>13}{'match':>7}")
    td=tc=0
    for r in sorted(rows,key=lambda x:-(int(x[0]) if x[0].isdigit() else -1)):
        d,a,nn = r[1] or 0, r[2] or 0, r[3] or 0
        diff=a-nn; td+=d; tc+=diff
        print(f"{r[0]:<7}{d:>9,.0f}{a:>10,.0f}{nn:>10,.0f}{diff:>13,.0f}{'OK' if abs(d-diff)<0.5 else ' <<DIFF':>7}")
    print(f"\nTOTAL direct={td:,.0f}  complement={tc:,.0f}")
asyncio.run(session(run))
