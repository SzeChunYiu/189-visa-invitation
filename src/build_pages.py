"""Emit the explorer as four pages sharing one script: result / landscape / policy / method."""
import pathlib,re,sys,json
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from dash_css import CSS
from dash_html import HTML
from model_js import MODEL_JS
from nav import nav_html
R=pathlib.Path(__file__).resolve().parent.parent
bundle=(R/"data"/"bundle.json").read_text()
src=HTML.replace("__MODEL__",MODEL_JS).replace("__CSS__",CSS).replace("__BUNDLE__",bundle)

head=src[:src.index('<div class="wrap">')]
body=src[src.index('<div class="wrap">'):src.index('<div id="tip"')]
tail=src[src.index('<div id="tip"'):]

def block(tag,frm=0):
    i=body.find(tag,frm)
    if i<0: return None
    depth=0; j=i
    while j<len(body):
        if body.startswith("<div",j): depth+=1
        elif body.startswith("</div>",j):
            depth-=1
            if depth==0: return (i,j+6)
        j+=1
    return None
hdr=block('<header>') or (body.index('<header>'), body.index('</header>')+9)
hb=body[body.index('<header>'):body.index('</header>')+9]
fs=block('<div class="filters">'); filters=body[fs[0]:fs[1]]
vs=block('<div class="verdict"'); verdict=body[vs[0]:vs[1]]
# Cards are selected by their heading, not their index: picking by position meant
# inserting a card silently moved every later one to a different page.
cards={}; order=[]; pos=0
while True:
    b=block('<div class="card',pos)
    if not b: break
    blk=body[b[0]:b[1]]; pos=b[1]
    h=re.search(r'<h2>(.*?)</h2>',blk,re.S)
    key=re.sub(r'<[^>]+>','',h.group(1)).strip() if h else f"card{len(order)}"
    assert key not in cards, f"two cards share the heading {key!r}"
    cards[key]=blk; order.append(key)
foot=body[body.index('<footer>'):body.index('</footer>')+10]
print(f"  {len(cards)} cards: "+", ".join(order))

def pick(*titles):
    missing=[t for t in titles if t not in cards]
    assert not missing, f"no card titled {missing}; have {order}"
    return [cards[t] for t in titles]

PAGES={
 "index.html":   dict(title="Will you be invited? · SkillSelect 189",
                      parts=[filters,verdict]+pick("Your chance vs round size","Forecast cut-off by round size",
                       "Past rounds","Who is ahead","Every score band",
                       "This occupation, round by round")),
 "landscape.html":dict(title="All occupations · SkillSelect 189",
                      parts=[filters]+pick("All occupations &times; all rounds","Competition drives the score",
                       "All occupations at your score")),
 "policy.html":  dict(title="Policy · SkillSelect 189",
                      parts=pick("Occupations cut off since 2025","2026&ndash;27 program")),
}
THEME='''
(function(){var k="sk189-theme";try{var v=localStorage.getItem(k);if(v)document.documentElement.setAttribute("data-theme",v);}catch(e){}
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("themebtn");if(!b)return;
var d=document.documentElement.getAttribute("data-theme")==="dark";
b.textContent=d?"Light":"Dark";b.setAttribute("aria-pressed",d?"true":"false");
b.addEventListener("click",function(){var on=document.documentElement.getAttribute("data-theme")==="dark";
document.documentElement.setAttribute("data-theme",on?"light":"dark");
try{localStorage.setItem(k,on?"light":"dark")}catch(e){}
b.textContent=on?"Dark":"Light";b.setAttribute("aria-pressed",on?"false":"true");
if(typeof render==="function")render();});});})();
'''
STATE='''
(function(){var k="sk189-state";
try{var v=JSON.parse(localStorage.getItem(k)||"{}");
 if(v.occ&&B.occ[v.occ])S.occ=v.occ; if(v.pts)S.pts=v.pts; if(v.doe!==undefined)S.doe=v.doe;}catch(e){}
var q=new URLSearchParams(location.search);
if(q.get("occ")&&B.occ[q.get("occ")])S.occ=q.get("occ");
if(q.get("pts"))S.pts=+q.get("pts")||S.pts;
var pf=document.getElementById("pts"); if(pf)pf.value=S.pts;
var df=document.getElementById("doe"); if(df&&S.doe)df.value=S.doe;
window.__saveState=function(){try{localStorage.setItem(k,JSON.stringify({occ:S.occ,pts:S.pts,doe:S.doe}))}catch(e){}};})();
'''
for fn,cfg in PAGES.items():
    hd=head.replace("<title>SkillSelect 189 Explorer</title>",f"<title>{cfg['title']}</title>")
    page=hd+'<a class="skip" href="#results">Skip to result</a>\n<div class="wrap">\n'+nav_html(fn)+"\n"+hb+"\n"
    page+="\n".join(cfg["parts"])+"\n"+foot+"\n</div>\n"+tail
    page=page.replace("const S={occ:","/*STATE*/\nconst S={occ:")
    page=page.replace("initCombo();render();", STATE.strip()+"\ninitCombo();render();\nif(window.__saveState)__saveState();")
    page=page.replace("</script>", THEME.strip()+"\n</script>")
    page=page.replace('S.pts=+e.target.value||0;render();','S.pts=+e.target.value||0;render();if(window.__saveState)__saveState();')
    page=page.replace('S.doe=e.target.value||null;render();','S.doe=e.target.value||null;render();if(window.__saveState)__saveState();')
    page=page.replace('function pick(o){S.occ=o;inp.value=o;open(false);render();}',
                      'function pick(o){S.occ=o;inp.value=o;open(false);render();if(window.__saveState)__saveState();}')
    for marker,want in [("sk189-theme",1),("sk189-state",1),("initCombo();render();",1)]:
        got=page.count(marker)
        assert got==want, f"{fn}: {marker} injected {got}x, expected {want}"
    (R/"docs"/fn).write_text(page)
    print(f"  {fn:<16}{len(page)/1024:>7.0f} KB")
print("pages written")
