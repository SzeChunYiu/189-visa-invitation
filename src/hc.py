import asyncio, json, csv, os

async def cube(q, h, dims, measures, out_csv=None, page_cells=8000):
    """dims: list of (label, fieldOrExpr). measures: list of (label, expr).
    Asserts fetched rows == qSize.qcy. Writes CSV if out_csv."""
    def dimdef(d):
        lab, f = d
        return {"qDef":{"qFieldDefs":[f],"qFieldLabels":[lab]},"qNullSuppression":False}
    defn={"qInfo":{"qType":"tbl"},
      "qHyperCubeDef":{
        "qDimensions":[dimdef(d) for d in dims],
        "qMeasures":[{"qDef":{"qDef":m[1],"qLabel":m[0]}} for m in measures],
        "qInitialDataFetch":[], "qSuppressZero":False, "qSuppressMissing":True,
        "qInterColumnSortOrder":list(range(len(dims)+len(measures)))}}
    o=await q.call("CreateSessionObject",h,[defn]); oh=o["qReturn"]["qHandle"]
    lay=await q.call("GetLayout",oh,[])
    size=lay["qLayout"]["qHyperCube"]["qSize"]
    total, w = size["qcy"], size["qcx"]
    nd=len(dims)
    height=max(1, page_cells//max(1,w))
    rows=[]; top=0
    while top < total:
        r=await q.call("GetHyperCubeData",oh,["/qHyperCubeDef",[{"qTop":top,"qLeft":0,"qWidth":w,"qHeight":min(height,total-top)}]])
        pg=r["qDataPages"][0]["qMatrix"]
        if not pg: break
        for row in pg:
            rows.append([c.get("qText") for c in row[:nd]] + [c.get("qNum") for c in row[nd:]])
        top += len(pg)
    assert len(rows)==total, f"TRUNCATION: fetched {len(rows)} of qcy={total}"
    await q.call("DestroySessionObject",h,[lay["qLayout"]["qInfo"]["qId"]])
    hdr=[d[0] for d in dims]+[m[0] for m in measures]
    if out_csv:
        with open(out_csv,"w",newline="") as f:
            wtr=csv.writer(f); wtr.writerow(hdr); wtr.writerows(rows)
    return hdr, rows, total
