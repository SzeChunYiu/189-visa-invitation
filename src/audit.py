"""Consistency audit: does every published figure agree with every other?"""
import pandas as pd, numpy as np, json, pathlib, os, re
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
fails=[]
def chk(name,ok,detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok: fails.append(name)
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df

B=json.load(open("bundle.json"))
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
pool=num(pd.read_csv("pool189only_occ4.csv")); pool["n"]=pool["only"].fillna(0); pool["G"]=pool.Occupation.astype(str).str[:4]
lat=pool[pool.AsAt=="08/2026"]

print("="*96); print("A. BUNDLE vs SOURCE EXTRACTS"); print("="*96)
# group cut-off: dashboard derives it as min over member occupations; extraction takes it group-wise
bad=[]
for gk in B["groups"]:
    for rd in ROUNDS:
        src=inv[(inv.G==gk)&(inv.StatusMonth==rd)&(inv.n>0)]
        src_min=int(src.Score.min()) if len(src) else None
        occ_min=None
        for o,oc in B["occ"].items():
            if oc["g"]!=gk: continue
            r=[x for x in oc["rounds"] if x["r"]==rd]
            if r and r[0]["b"] is not None:
                occ_min=r[0]["b"] if occ_min is None else min(occ_min,r[0]["b"])
        if src_min!=occ_min: bad.append((gk,rd,src_min,occ_min))
chk("group cut-off from occupations == group-wise extraction",len(bad)==0,
    f"{len(bad)} mismatches" + (f" e.g. {bad[:3]}" if bad else ""))
# group pool == sum of member occupation pools
bad2=[]
for gk,G in B["groups"].items():
    a=sum(G["dist"].values())
    b=int(lat[lat.G==gk].n.sum())
    if a!=b: bad2.append((gk,a,b))
chk("bundle group pool == extract group pool",len(bad2)==0,f"{len(bad2)} mismatches")
# occupation pool == sum of its dist
bad3=[o for o,oc in B["occ"].items() if sum(oc["dist"].values())!=oc["pool"]]
chk("occupation pool == sum of its score distribution",len(bad3)==0,f"{len(bad3)} mismatches")

print("\n"+"="*96); print("B. INTERNAL LOGIC OF THE SATURATION STATES"); print("="*96)
bad4=[]
for o,oc in B["occ"].items():
    for r in oc["rounds"]:
        if r["b"] is None: continue
        if r["lc"] is not None and r["lc"]<r["b"]: bad4.append((o,r["r"],"cleared below boundary"))
        if r["s"]=="C" and r["lc"]!=r["b"]: bad4.append((o,r["r"],"boundary CLEARED but lc!=b"))
        if r["s"]=="P" and r["lc"] is not None and r["lc"]<=r["b"]: bad4.append((o,r["r"],"boundary PARTIAL but lc<=b"))
chk("lowest_cleared >= boundary, and states agree with them",len(bad4)==0,
    f"{len(bad4)} violations" + (f" e.g. {bad4[:3]}" if bad4 else ""))

print("\n"+"="*96); print("C. FORECAST MONOTONICITY & FLOOR"); print("="*96)
bad5=[gk for gk,G in B["groups"].items()
      if any(a is not None and b is not None and b>a for a,b in zip(G["fc"],G["fc"][1:]))]
chk("forecast cut-off is non-increasing in round size",len(bad5)==0,f"{len(bad5)} groups violate")
bad6=[gk for gk,G in B["groups"].items() if any(v is not None and v<B["floor"] for v in G["fc"])]
chk(f"no forecast below the {B['floor']}-point legislative floor",len(bad6)==0,f"{len(bad6)} groups violate")
bad7=[gk for gk,G in B["groups"].items() if sum(G["dist"].values())==0 and any(v is not None for v in G["fc"])]
chk("no forecast for a group with an empty pool",len(bad7)==0)

print("\n"+"="*96); print("D. PUBLISHED NUMBERS vs RECOMPUTED"); print("="*96)
pol=json.load(open("policy.json")); cal=json.load(open("calibration_official.json"))
val=json.load(open("validation_singleleg.json"))
g2349=B["groups"].get("2349")
chk("2349 allocation series is [3,11,15,24,35] single-leg",g2349["alloc"]==[3,11,15,24,35],str(g2349["alloc"]))
chk("2349 forecast is [85,80,75,75,70]",g2349["fc"]==[85,80,75,75,70],str(g2349["fc"]))
ge=sum(v for k,v in g2349["dist"].items() if int(k)>=85)
chk("2349 stock at >=85 is 22 (single-leg)",ge==22,str(ge))
chk("invitations-per-place ratio recomputes to 1.54",abs(pol["ratio"]-1.54)<0.01,str(pol["ratio"]))
chk("calibration exact rate is 90.3%",abs(cal["exact"]/cal["n"]-0.903)<0.002,f"{100*cal['exact']/cal['n']:.1f}%")
chk("out-of-sample MAE is 5.64 overall",abs(val["oos"]["mae"]-5.64)<0.01,str(val["oos"]["mae"]))

print("\n"+"="*96); print("E. CROSS-DOC CLAIM SCAN"); print("="*96)
docs=list(pathlib.Path("../docs").glob("*.md"))+[pathlib.Path("../README.md")]
stale=[]
for f in docs:
    t=f.read_text()
    for pat,why in [(r"49\s*of\s*49",'superseded 49/49 claim'),(r"r\s*=\s*0\.941",'superseded r=0.941'),
                    (r"rank\s*32\s*needs",'retired threshold framing')]:
        for m in re.finditer(pat,t):
            ctx=t[max(0,m.start()-90):m.start()+60].replace("\n"," ")
            if not re.search(r"supersede|retired|earlier|was wrong|corrected|old ",ctx,re.I):
                stale.append((f.name,why,ctx[:110]))
chk("no unlabelled superseded claims in the docs",len(stale)==0,f"{len(stale)} found")
for s in stale[:5]: print(f"        {s[0]}: {s[1]} -> …{s[2]}…")
print("\n"+"="*96); print("F. BUILT PAGE: every reference resolves"); print("="*96)
import re as _re
def _code(html):
    """JS with the embedded data literal removed - occupation names parse as calls otherwise."""
    js="\n".join(_re.findall(r"<script>(.*?)</script>", html, _re.S))
    return _re.sub(r"const B=\{.*?\};", "const B={};", js, flags=_re.S)
for page in ["index.html","findings.html"]:
    html=(pathlib.Path("../docs")/page).read_text()
    js=_code(html)
    ids=set(_re.findall(r'id="([A-Za-z0-9_-]+)"', html))
    refs=set(_re.findall(r'\$\("([A-Za-z0-9_-]+)"\)', js)) | set(
        _re.findall(r'getElementById\("([A-Za-z0-9_-]+)"\)', js))
    missing=sorted(refs-ids)
    chk(f"{page}: every element id referenced by JS exists",len(missing)==0,
        f"missing {missing}" if missing else f"{len(refs)} refs checked")
    # Duplicate definitions: JS silently lets the LAST one win, so a stale copy can shadow a
    # rewritten function and every functional test still passes. This bit three times before it
    # was caught, once with bandTable defined FOUR times.
    def _blocks(src):
        out=[]
        for m in _re.finditer(r'\bfunction\s+([A-Za-z0-9_]+)\s*\(', src):
            i=src.index("{", m.end()-1); depth=0; j=i
            while j < len(src):
                if src[j]=="{": depth+=1
                elif src[j]=="}":
                    depth-=1
                    if depth==0: break
                j+=1
            out.append(m.group(1))
        return out
    import collections as _c
    names=_blocks(js)
    dup={k:v for k,v in _c.Counter(names).items() if v>1}
    chk(f"{page}: no function defined more than once",not dup,
        f"duplicates {dup}" if dup else f"{len(set(names))} helpers, all unique")

    # A static "is every called helper defined" check was tried and REMOVED: the known-helper list has to
    # be derived from the same file whose definition may have been deleted, so it passes when it should fail.
    # A deliberate rename of queueTable() slipped straight through it. Undefined-function regressions are
    # caught instead by loading the page and asserting an empty console - see scripts/check_console.md.

print("\n"+"="*96)
print(f"AUDIT: {len(fails)} failure(s)" + (": "+", ".join(fails) if fails else " - all checks pass"))
