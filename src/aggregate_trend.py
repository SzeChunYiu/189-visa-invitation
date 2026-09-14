"""Aggregate cut-off against round size, and why the model does not use it.

Across rounds the relationship has the OPPOSITE sign to the mechanism: bigger rounds
go with slightly HIGHER aggregate cut-offs. That is composition, not causation - each
round invites a different mix of occupations from a pool that is itself strengthening.
An analyst who regressed the aggregate on round size would get the sign backwards.
Recorded here so the paper can say it.
"""
import json, pathlib, statistics as st, os

os.chdir(pathlib.Path(__file__).resolve().parent.parent / "data")
B = json.load(open("bundle.json"))
INV = {"2024-09": 7735, "2024-11": 14724, "2025-08": 6450, "2025-11": 9826, "2026-06": 9748}

rows = []
for i, r in enumerate(B["rounds"]):
    cs, ws = [], []
    for o in B["occ"].values():
        rr = o["rounds"][i]
        if rr["b"] is not None and rr["n"]:
            cs.append(rr["b"]); ws.append(rr["n"])
    rows.append(dict(round=r, size=INV[r], n=len(cs),
                     median=float(st.median(cs)),
                     wmean=round(sum(c * w for c, w in zip(cs, ws)) / sum(ws), 2)))


def pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = sum((x - ma) ** 2 for x in a) ** .5
    db = sum((y - mb) ** 2 for y in b) ** .5
    return round(num / (da * db), 4) if da and db else None


size = [x["size"] for x in rows]
agg = dict(rows=rows,
           r_median=pearson(size, [x["median"] for x in rows]),
           r_wmean=pearson(size, [x["wmean"] for x in rows]),
           n=len(rows))
B["agg"] = agg
json.dump(B, open("bundle.json", "w"), separators=(",", ":"))

print("=" * 88)
print("AGGREGATE CUT-OFF vs ROUND SIZE  (the relationship the model deliberately ignores)")
print("=" * 88)
print(f"  {'round':<10}{'invitations':>13}{'occupations':>13}{'median':>9}{'weighted mean':>15}")
for x in rows:
    print(f"  {x['round']:<10}{x['size']:>13,}{x['n']:>13}{x['median']:>9.0f}{x['wmean']:>15.1f}")
print(f"\n  r(size, median cut-off) = {agg['r_median']:+.3f}   n = {agg['n']}")
print(f"  r(size, weighted mean)  = {agg['r_wmean']:+.3f}")
print("  Sign is OPPOSITE to the per-group mechanism. Composition, not causation.")
print("  -> bundle.json['agg'] written")
