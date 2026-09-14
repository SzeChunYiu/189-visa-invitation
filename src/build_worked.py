"""Build docs/worked.html - the calculation, one step at a time, for any occupation.

Promoted out of the method paper: it is the page a reader uses, not a chapter they
read once, and it belongs beside the result rather than eleven chapters into a paper.
It calls the shared model (model_js.MODEL_JS), so the arithmetic it narrates is the
arithmetic behind the headline.
"""
import json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dash_css import CSS
from paper_css import PAPER_CSS
from model_js import MODEL_JS
from paper_worked import WORKED_HTML, WORKED_JS
from nav import nav_html

R = pathlib.Path(__file__).resolve().parent.parent
BUNDLE = (R / "data" / "bundle.json").read_text()

THEME = r"""
(function(){var k="sk189-theme";try{var v=localStorage.getItem(k);if(v)document.documentElement.setAttribute("data-theme",v);}catch(e){}
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("themebtn");if(!b)return;
var d=document.documentElement.getAttribute("data-theme")==="dark";
b.textContent=d?"Light":"Dark";b.setAttribute("aria-pressed",d?"true":"false");
b.addEventListener("click",function(){var on=document.documentElement.getAttribute("data-theme")==="dark";
document.documentElement.setAttribute("data-theme",on?"light":"dark");
try{localStorage.setItem(k,on?"light":"dark")}catch(e){}
b.textContent=on?"Dark":"Light";b.setAttribute("aria-pressed",on?"false":"true");});});})();
"""

STATE = r"""
(function(){var k="sk189-state";
try{var v=JSON.parse(localStorage.getItem(k)||"{}");
 if(v.occ&&B.occ[v.occ])S.occ=v.occ; if(v.pts)S.pts=v.pts; if(v.doe!==undefined)S.doe=v.doe;}catch(e){}
var q=new URLSearchParams(location.search);
if(q.get("occ")&&B.occ[q.get("occ")])S.occ=q.get("occ");
if(q.get("pts"))S.pts=+q.get("pts")||S.pts;
window.__saveState=function(){try{localStorage.setItem(k,JSON.stringify({occ:S.occ,pts:S.pts,doe:S.doe}))}catch(e){}};})();
"""

page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The calculation, step by step</title>
<meta name="description" content="Every step of the subclass 189 invitation calculation, run on any occupation and score, with the arithmetic shown.">
<style>{CSS}{PAPER_CSS}
.wkpage{{max-width:860px;margin:0 auto;padding:0 20px 72px}}
.wkpage .wk{{margin-top:0}}
.wkpage .steph{{font-size:14px}}
</style>
</head><body>
<div class="wrap" style="padding-bottom:6px">
{nav_html("worked.html")}
<header>
  <p class="kicker">Step by step</p>
  <h1>How your number is worked out</h1>
  <p class="sub">Pick an occupation and a score. Every step of the calculation is shown with
  its arithmetic, in the order the model runs it.</p>
</header>
</div>
<div class="wkpage">
{WORKED_HTML}
<div id="wsteps"></div>
<div class="wkout" id="wres"></div>
<p class="note" style="margin-top:22px;font-size:13px;color:var(--muted)">
  Each step links to the chapter that derives it:
  <a href="findings.html#allocation">allocation</a>,
  <a href="findings.html#cutoff">cut-off</a>,
  <a href="findings.html#uncertainty">uncertainty</a>,
  <a href="findings.html#band">boundary band</a>,
  <a href="findings.html#roundsize">round size</a>,
  <a href="findings.html#zero">exclusion</a>.
</p>
</div>
<script>
const B={BUNDLE};
const S={{occ:null,pts:85,doe:null,szi:2}};
{MODEL_JS}
{STATE}
{WORKED_JS}
{THEME}
</script>
</body></html>
"""
(R / "docs" / "worked.html").write_text(page)
print(f"wrote docs/worked.html  ({len(page)/1024:.0f} KB)")
