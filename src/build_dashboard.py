"""Render docs/index.html from the extracted CSV/JSON artefacts."""
import pandas as pd, json, pathlib, html
D=pathlib.Path(__file__).resolve().parent.parent/"data"
OUT=pathlib.Path(__file__).resolve().parent.parent/"docs"/"index.html"
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
LBL={"2024-09":"Sep 2024","2024-11":"Nov 2024","2025-08":"Aug 2025","2025-11":"Nov 2025","2026-06":"Jun 2026"}
occ=pd.read_csv(D/"cutoff_by_occupation.csv")
fin=json.load(open(D/"model_final.json"))
haz=json.load(open(D/"model_hazards.json"))
SIZE={r["round"]:r["size"] for r in haz["cutoffs"]}
EST={"2024-09":7814,"2024-11":14507,"2025-08":6705,"2025-11":9821,"2026-06":9761}
CUT2349=[r["cut_2349"] for r in haz["cutoffs"]]
ALLOC=[r["alloc"] for r in fin["alloc"]]
POOL=[r["pool_ge85"] for r in fin["alloc"]]
phys=occ[occ.occupation=="234914 Physicist"].iloc[0]
PHYS_N=[int(phys[r+"_n"]) for r in ROUNDS]

# ---- cut-off trajectory chart (computed coords, labels inside viewBox) ----
W,H,ML,MR,MT,MB=760,300,58,24,26,54
pw,ph=W-ML-MR,H-MT-MB
ys,ye=65,100
def X(i): return ML+pw*(i/(len(ROUNDS)-1))
def Y(v): return MT+ph*(1-(v-ys)/(ye-ys))
grid="".join(f'<line x1="{ML}" y1="{Y(v):.1f}" x2="{W-MR}" y2="{Y(v):.1f}" class="g"/>'
             f'<text x="{ML-10}" y="{Y(v)+4:.1f}" class="ax" text-anchor="end">{v}</text>' for v in range(65,101,5))
band=f'<rect x="{ML}" y="{Y(ye):.1f}" width="{pw}" height="{Y(85)-Y(ye):.1f}" class="above"/>'
line85=(f'<line x1="{ML}" y1="{Y(85):.1f}" x2="{W-MR}" y2="{Y(85):.1f}" class="mark"/>'
        f'<text x="{W-MR-4}" y="{Y(85)-8:.1f}" class="marklbl" text-anchor="end">your 85 points</text>')
pts=[(X(i),Y(c)) for i,c in enumerate(CUT2349)]
path="M"+" L".join(f"{x:.1f},{y:.1f}" for x,y in pts)
dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{6 if i==len(pts)-1 else 4.5}" class="{"dot end" if i==len(pts)-1 else "dot"}"/>'
             f'<text x="{x:.1f}" y="{y-14:.1f}" class="val" text-anchor="middle">{CUT2349[i]}</text>' for i,(x,y) in enumerate(pts))
xlab="".join(f'<text x="{X(i):.1f}" y="{H-MB+20}" class="ax" text-anchor="middle">{LBL[r]}</text>'
             f'<text x="{X(i):.1f}" y="{H-MB+34}" class="axs" text-anchor="middle">{PHYS_N[i]} invited</text>' for i,r in enumerate(ROUNDS))
chart=f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Physics-stratum points cut-off by round: 95, 90, 90, 85, 80">
{band}{grid}{line85}<path d="{path}" class="ln"/>{dots}{xlab}</svg>'''

rows="".join(
 f"<tr><td class='rd'>{LBL[r]}</td><td class='n'>{SIZE[r]:,}</td><td class='n dim'>~{EST[r]:,}</td>"
 f"<td class='n'>{ALLOC[i]}</td><td class='n'>{POOL[i]}</td>"
 f"<td class='n'><span class='pill {'ok' if CUT2349[i]<=85 else 'no'}'>{CUT2349[i]}</span></td></tr>"
 for i,r in enumerate(ROUNDS))

recs=[]
for _,x in occ.iterrows():
    recs.append({"o":x.occupation,"c":[None if pd.isna(x[r]) else int(x[r]) for r in ROUNDS],
                 "n":[int(x[r+"_n"]) for r in ROUNDS],"p":int(x.pool_total),"p85":int(x.pool_85),"pg":int(x.pool_gt85)})
DATA=json.dumps(recs,separators=(",",":"))

CSS=""":root{--paper:#fbfbfc;--card:#ffffff;--ink:#141a24;--body:#39414f;--muted:#6b7589;--line:#e2e5ec;
--accent:#2f6f5e;--accent-soft:#e8f1ee;--amber:#b8792c;--amber-soft:#fbf1e3;--good:#2f7d5f;--bad:#a8453f;--shadow:0 1px 2px rgba(20,26,36,.06),0 8px 24px -16px rgba(20,26,36,.28)}
:root:not([data-theme="light"]){}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#0e1219;--card:#161c26;--ink:#eef1f6;--body:#c2c9d6;--muted:#8b95a8;--line:#262e3b;
--accent:#63b39b;--accent-soft:#16302a;--amber:#d9a259;--amber-soft:#2e2417;--good:#63b39b;--bad:#d97b74;--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -18px rgba(0,0,0,.7)}}
:root[data-theme="dark"]{--paper:#0e1219;--card:#161c26;--ink:#eef1f6;--body:#c2c9d6;--muted:#8b95a8;--line:#262e3b;
--accent:#63b39b;--accent-soft:#16302a;--amber:#d9a259;--amber-soft:#2e2417;--good:#63b39b;--bad:#d97b74;--shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -18px rgba(0,0,0,.7)}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--body);font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;line-height:1.6;margin:0;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:40px 22px 80px;display:flex;flex-direction:column;gap:34px}
h1,h2,h3{font-family:Archivo,ui-sans-serif,system-ui,sans-serif;color:var(--ink);margin:0;text-wrap:balance;letter-spacing:-.015em}
h1{font-size:clamp(28px,4.4vw,42px);font-weight:800;line-height:1.1}
h2{font-size:20px;font-weight:700}
h3{font-size:15px;font-weight:700}
.eyebrow{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);font-weight:600}
.sub{color:var(--muted);font-size:15px;max-width:66ch}
header{display:flex;flex-direction:column;gap:10px;border-bottom:1px solid var(--line);padding-bottom:26px}
.verdict{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);overflow:hidden}
.vtop{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:0}
@media(max-width:720px){.vtop{grid-template-columns:1fr}}
.vmain{padding:26px 28px;border-right:1px solid var(--line)}
@media(max-width:720px){.vmain{border-right:0;border-bottom:1px solid var(--line)}}
.big{font-family:Archivo,sans-serif;font-size:62px;font-weight:800;color:var(--accent);line-height:1;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.vside{padding:26px 28px;display:flex;flex-direction:column;gap:14px;justify-content:center}
.kv{display:flex;justify-content:space-between;gap:16px;align-items:baseline;font-size:14px}
.kv dt{color:var(--muted)}.kv dd{margin:0;font-family:"IBM Plex Mono",monospace;color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
.caveat{background:var(--amber-soft);border-top:1px solid var(--line);padding:14px 28px;font-size:13.5px;color:var(--body)}
.caveat b{color:var(--amber)}
section{display:flex;flex-direction:column;gap:14px}
.panel{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px;box-shadow:var(--shadow)}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:560px}
th{font-family:"IBM Plex Mono",monospace;font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);font-weight:600;text-align:right;padding:0 10px 9px;border-bottom:1px solid var(--line)}
th:first-child{text-align:left}
td{padding:9px 10px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
tbody tr:last-child td{border-bottom:0}
.n{text-align:right;font-family:"IBM Plex Mono",monospace}
.rd{font-weight:600;color:var(--ink)}
.dim{color:var(--muted)}
.pill{display:inline-block;min-width:38px;padding:2px 9px;border-radius:999px;font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:12.5px}
.pill.ok{background:var(--accent-soft);color:var(--good)}
.pill.no{background:var(--amber-soft);color:var(--amber)}
svg{width:100%;height:auto;display:block}
.g{stroke:var(--line);stroke-width:1}
.above{fill:var(--amber-soft);opacity:.55}
.ax{fill:var(--muted);font-family:"IBM Plex Mono",monospace;font-size:11px}
.axs{fill:var(--muted);font-family:"IBM Plex Mono",monospace;font-size:9.5px;opacity:.8}
.mark{stroke:var(--amber);stroke-width:1.5;stroke-dasharray:5 4}
.marklbl{fill:var(--amber);font-family:"IBM Plex Mono",monospace;font-size:11px;font-weight:600}
.ln{fill:none;stroke:var(--accent);stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round}
.dot{fill:var(--accent);stroke:var(--card);stroke-width:2}
.dot.end{fill:var(--amber)}
.val{fill:var(--ink);font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:700}
input[type=search]{width:100%;padding:11px 14px;border:1px solid var(--line);border-radius:9px;background:var(--paper);color:var(--ink);font:inherit;font-size:14px}
input[type=search]:focus{outline:2px solid var(--accent);outline-offset:1px}
.note{font-size:13px;color:var(--muted)}
.findings{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.find{border-left:3px solid var(--accent);padding:2px 0 2px 15px}
.find h3{margin-bottom:4px}
.find p{margin:0;font-size:13.5px}
code{font-family:"IBM Plex Mono",monospace;font-size:.9em;background:var(--accent-soft);color:var(--accent);padding:1px 5px;border-radius:4px}
footer{border-top:1px solid var(--line);padding-top:20px;font-size:12.5px;color:var(--muted)}
a{color:var(--accent)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}"""

HTML=f"""<title>189 Invitation Odds</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header>
  <div class="eyebrow">Subclass 189 &middot; Points-Tested Stream</div>
  <h1>Will an 85-point physicist be invited?</h1>
  <p class="sub">A queue model built from all 24 monthly SkillSelect snapshots (Sep 2024 &ndash; Aug 2026), read straight from the
  Qlik engine behind the Department of Employment's public EOI dashboard. Every figure here is a distinct-EOI count, not a row count.</p>
</header>

<div class="verdict">
 <div class="vtop">
  <div class="vmain">
    <div class="eyebrow">Probability of invitation</div>
    <div class="big">77%</div>
    <p class="sub" style="margin-top:8px"><b>Conditional on a round being held.</b> The physics stratum's cut-off has fallen every
    round for two years and cleared 85 points in each of the last two. The open question is not your score &mdash; it is whether
    Home Affairs runs a round at all.</p>
  </div>
  <div class="vside">
    <dl class="kv" style="margin:0"><dt>Your rank in unit group 2349</dt><dd>~{fin['rank_all']}</dd></dl>
    <dl class="kv" style="margin:0"><dt>Invitations to 2349 last round</dt><dd>{ALLOC[-1]} &rarr; ~66</dd></dl>
    <dl class="kv" style="margin:0"><dt>Physicists at 85 pts ahead of you</dt><dd>{int(phys.pool_85)}</dd></dl>
    <dl class="kv" style="margin:0"><dt>Physicists above 85 pts</dt><dd>{int(phys.pool_gt85)}</dd></dl>
    <dl class="kv" style="margin:0"><dt>P(cut-off &lt; 85) / (= 85) / (&gt; 85)</dt><dd>{fin['p_below']:.0%} / {fin['p_eq']:.0%} / {fin['p_above']:.0%}</dd></dl>
  </div>
 </div>
 <div class="caveat"><b>What this model cannot tell you:</b> whether a round happens, or how big it is. Both are set by
 planning levels, not by the pool. Five rounds in 24 months is the entire evidence base for cadence &mdash; too thin for a dated forecast.</div>
</div>

<section>
  <h2>The mechanism: rounds are stratified by occupation, not by a single national cut-off</h2>
  <p class="sub">Every round invites someone at 65 points, so there is no such thing as "the 189 cut-off". Each ANZSCO unit group
  clears to its own depth. Physicists sit in <b>2349 Other Natural and Physical Science Professionals</b> &mdash; a low-volume group
  whose cut-off has dropped 15 points in five rounds while the national floor never moved.</p>
  <div class="panel">{chart}
  <p class="note" style="margin-top:6px">Minimum points invited in unit group 2349 per round. Shaded band = scores above 85.
  Jun 2026 went <b>below</b> your score, inviting physicists at 80.</p></div>
</section>

<section>
  <h2>The five real rounds</h2>
  <p class="sub">Only five months in the whole panel contain genuine 189 invitations. The other 19 months show nothing but
  190/491 state nominations leaking through a shared status field &mdash; see the methodology note below.</p>
  <div class="panel scroll"><table>
   <thead><tr><th>Round</th><th>189-only invites</th><th>Est. total</th><th>To group 2349</th><th>2349 stock &ge;85</th><th>2349 cut-off</th></tr></thead>
   <tbody>{rows}</tbody></table></div>
  <p class="note">"189-only" counts EOIs whose <i>only</i> visa leg is 189, so the invitation is unambiguously a 189 invitation.
  "Est. total" adds multi-leg EOIs via a difference-in-differences correction against non-round months.</p>
</section>

<section>
  <h2>Look up any occupation</h2>
  <p class="sub">The points cut-off each ANZSCO occupation actually reached in each of the five rounds, with its current
  standing pool. Blank means that occupation received no invitation in that round.</p>
  <div class="panel">
    <input type="search" id="q" placeholder="Search 181 occupations — try 'physicist', '2613', 'nurse'" aria-label="Search occupations">
    <div class="scroll" style="margin-top:14px;max-height:440px;overflow-y:auto"><table id="t">
      <thead><tr><th>Occupation</th>{''.join(f'<th>{LBL[r]}</th>' for r in ROUNDS)}<th>Pool @85</th><th>Pool &gt;85</th></tr></thead>
      <tbody></tbody></table></div>
  </div>
</section>

<section>
  <h2>Two things everyone else gets wrong about this dashboard</h2>
  <div class="findings">
    <div class="find"><h3>EOI Status is recorded per EOI, not per visa leg</h3>
    <p>Filtering <code>Visa Type = 189</code> and counting <code>INVITED</code> overstates 189 invitations by roughly 2&times;,
    because an EOI invited for 190 still carries a 189 leg. Across the panel the three visa filters overlap ~50%. Isolating
    single-leg EOIs is what reveals that there were five rounds, not twenty-four.</p></div>
    <div class="find"><h3>The engine returns exact counts below 20</h3>
    <p>The Qlik front end masks small cells, but the websocket engine underneath does not. Verified by complement differencing
    &mdash; total minus total-excluding-the-occupation reproduced the direct figure exactly (72 = 72) down to cells of 1.</p></div>
  </div>
</section>

<footer>
  Source: Department of Employment and Workplace Relations SkillSelect EOI dashboard, Qlik app <code>aaac76b5</code>, snapshots
  Sep 2024 &ndash; Aug 2026. Latest snapshot is 08/2026 and therefore predates a 10 Sep 2026 EOI. <code>Month Submitted</code> is not
  <i>date of effect</i>: a points change resets date of effect, so same-score queue position is approximate and, for a recent
  submission, conservative. Not migration advice. Code and data:
  <a href="https://github.com/SzeChunYiu/189-visa-invitation">github.com/SzeChunYiu/189-visa-invitation</a>
</footer>
</div>
<script>
const D={DATA},R={json.dumps([LBL[r] for r in ROUNDS])};
const tb=document.querySelector("#t tbody"),q=document.getElementById("q");
function cell(v,n){{ if(v===null) return "<td class='n dim'>&mdash;</td>";
  const k=v<=85?"ok":"no"; return `<td class='n'><span class='pill ${{k}}'>${{v}}</span><span class='dim' style='font-size:11px'> ${{n}}</span></td>`;}}
function render(f){{
  tb.innerHTML=D.filter(r=>r.o.toLowerCase().includes(f)).map(r=>
    `<tr><td class='rd'>${{r.o}}</td>${{r.c.map((v,i)=>cell(v,r.n[i])).join("")}}<td class='n'>${{r.p85}}</td><td class='n'>${{r.pg}}</td></tr>`).join("")
    || "<tr><td colspan='8' class='dim' style='padding:18px'>No occupation matches that search.</td></tr>";}}
q.addEventListener("input",e=>render(e.target.value.toLowerCase().trim()));
q.value="physicist";render("physicist");
</script>"""
OUT.parent.mkdir(exist_ok=True); OUT.write_text(HTML)
print(f"wrote {OUT}  ({len(HTML):,} bytes, {len(recs)} occupations)")
