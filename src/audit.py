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
from nav import PAGES   # one list, so a new page cannot escape the audit
SITE_IDS=set()
SITE_REFS={}
for page in PAGES:
    html=(pathlib.Path("../docs")/page).read_text()
    js=_code(html)
    ids=set(_re.findall(r'id="([A-Za-z0-9_-]+)"', html))
    refs=set(_re.findall(r'\$\("([A-Za-z0-9_-]+)"\)', js)) | set(
        _re.findall(r'getElementById\("([A-Za-z0-9_-]+)"\)', js))
    SITE_IDS |= ids; SITE_REFS[page]=refs
    # Post-split a page legitimately lacks ids owned by another page - the render helpers
    # guard for it (on/put/early return), so the old per-page "id exists" check became a
    # false positive by design. What must still hold is that every absent id is reached
    # only through a guarded accessor.
    def _guarded(r):
        # reached through the null-safe accessors, or inline-tested
        if f'on("{r}"' in js or f'put("{r}"' in js or f'if($("{r}"))' in js:
            return True
        # bound to a local that is then tested either way round: if(v) ... or if(!v) return
        for m in _re.finditer(r'(?:(?:const|let|var)\s+|,\s*)(\w+)\s*=\s*\$\("%s"\)'%_re.escape(r), js):
            v=_re.escape(m.group(1))
            if _re.search(r'if\s*\(\s*!?\s*%s\s*[)&|]'%v, js): return True
        return False
    unguarded=sorted(r for r in refs-ids if not _guarded(r))
    chk(f"{page}: absent ids are reached only through guarded accessors",len(unguarded)==0,
        f"unguarded {unguarded}" if unguarded else f"{len(refs-ids)} absent, all guarded")
    if page=="index.html":
        # a guard detector that cannot fail is worthless: plant a bare $("x") with no guard
        # and a guarded twin, and require exactly the bare one to be flagged
        js_probe=js+'\n$("__bare_probe__");\nconst _pz=$("__safe_probe__"); if(!_pz) return;'
        _js_save=js; js=js_probe
        flagged=[r for r in ["__bare_probe__","__safe_probe__"] if not _guarded(r)]
        js=_js_save
        chk("  (control) the guard detector flags a bare $() and clears a tested one",
            flagged==["__bare_probe__"], f"control flagged {flagged}")
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

# The paper renders its figures from a Python copy of the model. If that copy drifts
# from the forecast the pages publish, the figures would illustrate a model nobody runs.
import json as _json
_B=_json.loads((pathlib.Path("../data")/"bundle.json").read_text())
import paper_figs as _PF
_mis=[]
for _gk,_g in _B["groups"].items():
    for _i,_S in enumerate(_B["sizes"]):
        _mine=_PF.cutoff_at(_g,_S,_B["meta"]["fr"])
        _pub=_g["fc"][_i]
        if _mine!=_pub: _mis.append((_gk,_S,_mine,_pub))
chk("paper figures reproduce the published forecast exactly",len(_mis)==0,
    f"{len(_mis)} mismatches e.g. {_mis[:2]}" if _mis
    else f"{len(_B['groups'])} groups x {len(_B['sizes'])} sizes agree")
# the comparison is only meaningful if a wrong factor would break it
_ctl=any(_PF.cutoff_at(_g,_S,_B["meta"]["fr"]*2)!=_g["fc"][_i]
         for _gk,_g in _B["groups"].items() for _i,_S in enumerate(_B["sizes"]))
chk("  (control) a wrong single-leg factor would fail that check",_ctl,
    "doubling phi changes the cut-offs" if _ctl else "check is insensitive - worthless")

# A CSS variable used but never defined resolves to nothing and fails silently - this
# shipped once as var(--accent) on the method nav. Check the BUILT html, so a token any
# future builder introduces is covered.
for _pg in PAGES:
    _h=(pathlib.Path("../docs")/_pg).read_text()
    _css="\n".join(_re.findall(r"<style>(.*?)</style>",_h,_re.S))
    _def=set(_re.findall(r"(--[a-z0-9-]+)\s*:",_css))
    _use=set(_re.findall(r"var\((--[a-z0-9-]+)\)",_h))
    _undef=sorted(_use-_def)
    chk(f"{_pg}: every CSS variable used is defined",len(_undef)==0,
        f"undefined {_undef}" if _undef else f"{len(_use)} tokens, all defined")
_h=(pathlib.Path("../docs")/"index.html").read_text()+'x{color:var(--never-defined)}'
_css="\n".join(_re.findall(r"<style>(.*?)</style>",_h,_re.S))
_ctl=sorted(set(_re.findall(r"var\((--[a-z0-9-]+)\)",_h))-set(_re.findall(r"(--[a-z0-9-]+)\s*:",_css)))
chk("  (control) the CSS-token check flags a token planted in real page CSS",
    _ctl==["--never-defined"], f"control saw {_ctl}")

# chapter cross-references in the paper must point at a chapter that exists
_f=(pathlib.Path("../docs")/"findings.html").read_text()
_nch=_f.count('<article class="chap"')
_bad=sorted({int(n) for n in _re.findall(r"[Cc]hapters? (\d+)",_f)} |
            {int(n) for n in _re.findall(r"[Cc]hapters \d+ to (\d+)",_f)} - {0}
            ) if _nch else []
_bad=[n for n in _bad if not (1<=n<=_nch)]
chk("paper cross-references point at chapters that exist",len(_bad)==0,
    f"out of range {_bad} (paper has {_nch})" if _bad else f"all within 1-{_nch}")

# The method page loads BOTH stylesheets. A class defined in each, unscoped, silently
# takes properties from the other - .step meant "stepper button" in one and "worked
# example row" in the other, and width:34px crushed every step on the paper.
_a=pathlib.Path("../src/dash_css.py").read_text()
_b=pathlib.Path("../src/paper_css.py").read_text()
def _sels(t):
    return set(_re.findall(r'(?:^|[,}\n])\s*(\.[a-zA-Z][\w-]*)\s*[{,:]', t, _re.M))
_clash=sorted(_sels(_a) & _sels(_b))
chk("no unscoped class is defined in both stylesheets",len(_clash)==0,
    f"defined in both: {_clash}" if _clash else f"{len(_sels(_a))} + {len(_sels(_b))} selectors, disjoint")
_ctl=sorted((_sels(_a)|{".__planted__"}) & (_sels(_b)|{".__planted__"}))
chk("  (control) the stylesheet-clash check catches a planted shared class",
    _ctl==[".__planted__"], f"control saw {_ctl}")

# Three different probabilities were all being displayed as "your chance": the
# marginalised one in the hero (77%), pClear without the skip risk on the chart whose
# axis says "chance of an invitation" (90%), and pLE, a statement about the cut-off
# rather than about being invited (94%). Any surface that shows a chance must go
# through pAt() or pMarginal(), which apply the skip factor.
_dh=pathlib.Path("../src/dash_html.py").read_text()
_ALLOWED={"pAt","pMarginal","chartWaterfall"}   # the waterfall deducts it explicitly, by step
def _owner(src,pos):
    m=_re.findall(r"function (\w+)\(", src[:pos])
    return m[-1] if m else "?"
_bare=sorted({_owner(_dh,m.start()) for m in _re.finditer(r"\bpClear\(", _dh)} - _ALLOWED)
chk("no surface shows pClear without the skip risk",len(_bare)==0,
    f"bare pClear in {_bare}" if _bare else f"pClear confined to {sorted(_ALLOWED)}")
_ctl=sorted(({"pAt","chartProb"} | set()) - _ALLOWED)
chk("  (control) that check would flag a chart calling pClear directly",
    _ctl==["chartProb"], f"control saw {_ctl}")

allrefs=set().union(*SITE_REFS.values())
orphans=sorted(allrefs-SITE_IDS)
chk(f"no JS reference is orphaned across all {len(PAGES)} pages",len(orphans)==0,
    f"orphaned {orphans}" if orphans else f"{len(allrefs)} refs, all defined on some page")
# the check is only worth its PASS if it can fail: plant an id no page defines
_ctl=sorted((allrefs|{"__planted_missing_id__"})-SITE_IDS)
chk("  (control) the orphan check catches a planted missing id",
    _ctl==["__planted_missing_id__"], f"control saw {_ctl}")

print("\n"+"="*96)
import sys as _sys
print(f"AUDIT: {len(fails)} failure(s)" + (": "+", ".join(fails) if fails else " - all checks pass"))
_sys.exit(1 if fails else 0)   # so build_all.py actually stops on a failure
