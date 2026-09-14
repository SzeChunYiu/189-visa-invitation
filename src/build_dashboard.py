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
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
_pl=pd.read_csv(D/"pool189_occ_score.csv"); _pl=_pl[_pl.Score.astype(str).str.fullmatch(r"\d+")]
_pl["Score"]=_pl.Score.astype(int); _pl["n"]=_pl.n.fillna(0)
_pl=_pl[_pl.OccGroup=="2349 Other Natural and Physical Science Professionals"]
POOL=[int(_pl[(_pl.AsAt==PRIOR[r])&(_pl.Score>=85)].n.sum()) for r in ROUNDS]  # all-leg, matches ALLOC basis
gm=json.load(open(D/"global_model.json")); fw=json.load(open(D/"forward_model.json"))
cal=json.load(open(D/"calibration_official.json"))
mob=json.load(open(D/"mobility.json"))
calrows=pd.read_csv(D/"calibration_official.csv")
SEP=fw["rank_by_date"]["by 30 Sep 2026"]; DEC=fw["rank_by_date"]["by 31 Dec 2026"]
ALLOC=[fw["alloc_hist"][r] for r in ROUNDS]
p190=pd.read_csv(D/"phys_190_491.csv").fillna(0)
p190=p190[p190.Score.astype(str).str.fullmatch(r"\d+")]; p190["Score"]=p190.Score.astype(int)
def st190(v):
    x=p190[(p190.Visa.str.startswith(v))&(p190.Status=="SUBMITTED")]
    return int(x.n.sum()), int(x[x.Score>=90].n.sum())
n190,g190=st190("190"); n491,g491=st190("491")
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

ALLOC=[fw["alloc_hist"][r] for r in ROUNDS]; RANK=SEP["rank"]; COV=SEP["covered"]; WTS=fw["weights"]
thr="".join(
 f"<tr><td class='rd'>{LBL[r]}</td><td class='n'>{ALLOC[i]}</td>"
 f"<td class='n dim'>{WTS[i]:.3f}</td>"
 f"<td class='n'><span class='pill {'ok' if COV[i] else 'no'}'>{'covered' if COV[i] else 'short'}</span></td></tr>"
 for i,r in enumerate(ROUNDS))
rows="".join(
 f"<tr><td class='rd'>{LBL[r]}</td><td class='n'>{SIZE[r]:,}</td><td class='n dim'>~{EST[r]:,}</td>"
 f"<td class='n'>{ALLOC[i]}</td><td class='n'>{POOL[i]}</td>"
 f"<td class='n'><span class='pill {'ok' if CUT2349[i]<=85 else 'no'}'>{CUT2349[i]}</span></td></tr>"
 for i,r in enumerate(ROUNDS))

recs=json.load(open(D/"occupation_database.json"))
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
.pill.mid{background:var(--amber-soft);color:var(--amber)}
.pill.no{background:var(--line);color:var(--muted)}
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
.theory{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:9px;font-size:14px}
.theory li{padding-left:4px}
.theory li::marker{color:var(--accent);font-family:"IBM Plex Mono",monospace;font-weight:700}
.statrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:18px}
.stat{display:flex;flex-direction:column;gap:2px}
.sv{font-family:Archivo,sans-serif;font-size:27px;font-weight:800;color:var(--ink);line-height:1;font-variant-numeric:tabular-nums}
.sl{font-size:11.5px;color:var(--muted);line-height:1.3}
.ctl{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.ctl label{font-size:13px;color:var(--muted)}
.ctl input[type=number]{width:78px;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);font:inherit;font-family:"IBM Plex Mono",monospace}
.ctl input[type=number]:focus{outline:2px solid var(--accent);outline-offset:1px}
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
    <div class="eyebrow">Probability of invitation &middot; conditional on a round being held</div>
    <div class="big">40&ndash;77%</div>
    <p class="sub" style="margin-top:8px">for a round held by <b>30 Sep 2026</b> &mdash; rising to
    <b>60&ndash;90%</b> if it slips past December. The lower bound of each band weights all five observed rounds
    equally and so ignores the trend; the upper bound halves the weight of each older round.</p>
  </div>
  <div class="vside">
    <dl class="kv" style="margin:0"><dt>Rank in ANZSCO 2349, Sep 2026</dt><dd>{SEP['rank']}</dd></dl>
    <dl class="kv" style="margin:0"><dt>Rank after Dec 2026 lapses</dt><dd>{DEC['rank']}</dd></dl>
    <dl class="kv" style="margin:0"><dt>189 pool that has re-scored</dt><dd>{mob['pct_changed']}%</dd></dl>
    <dl class="kv" style="margin:0"><dt>Invitations to 2349, last round</dt><dd>{ALLOC[-1]}</dd></dl>
    <dl class="kv" style="margin:0"><dt>Official cut-off for Physicist, Jun 2026</dt><dd>80</dd></dl>
    <dl class="kv" style="margin:0"><dt>Model vs official, 124 occupations</dt><dd>{100*cal['exact']/cal['n']:.0f}% exact</dd></dl>
  </div>
 </div>
 <div class="caveat"><b>Waiting helps you.</b> Your rank can only fall: anyone reaching 85 points after 10 Sep 2026 takes a
 later date of effect and queues behind you, while those ahead of you lapse at the two-year mark or are invited away.
 <b>What this model still cannot tell you</b> is whether a round is held, or how large it is &mdash; both are set by migration
 planning levels, not by the pool.</div>
</div>

<section>
  <h2>Points change, and that is what sets your place in the queue</h2>
  <p class="sub">Nearly half this pool did not lodge at the score it now holds. The table records every version of an
  EOI with its own validity interval, so an upgrade is directly observable &mdash; and an upgrade
  <b>resets the date of effect</b>, which is what the queue is actually ordered on.</p>
  <div class="panel"><div class="statrow">
    <div class="stat"><span class="sv">{mob['pct_changed']}%</span><span class="sl">of the 189 pool has changed score</span></div>
    <div class="stat"><span class="sv">+8.0</span><span class="sl">mean points gained, among movers</span></div>
    <div class="stat"><span class="sv">43%</span><span class="sl">of the 85+ pool re-scored within 6 months</span></div>
    <div class="stat"><span class="sv">~{mob['entry_rate_2349']:.0f}</span><span class="sl">enter 2349's 85+ band per month</span></div>
    <div class="stat"><span class="sv">0%</span><span class="sl">of 2349's 85+ cohort scored over a year ago</span></div>
  </div></div>
  <p class="note"><b>This works in your favour.</b> Someone sitting at 80 points who reaches 85 after 10 Sep 2026 takes a
  date of effect later than yours and joins the queue <i>behind</i> you, not ahead. Because the 85+ band turns over
  almost completely within a year, your position stops eroding the moment you lodge &mdash; it only improves as those
  ahead are invited away or hit the two-year expiry. Of the 31 people ahead of you in 2349, every one has a date of
  effect before 10 Sep 2026, verified directly rather than inferred from lodgement month.</p>
</section>

<section>
  <h2>One mechanism explains every observation</h2>
  <p class="sub">Five rounds, 181 occupations, cut-offs from 65 to 100 in a single round, a published tie-break that
  appears to exclude recent applicants, and a ceiling that never binds &mdash; all of it follows from one rule.</p>
  <div class="panel">
    <ol class="theory">
      <li><b>Each round sets an allocation per ANZSCO unit group.</b> Not the published ceiling, which is a
      non-binding upper bound &mdash; 2349's ceiling is 500 and the largest round used 87.</li>
      <li><b>Within a group, invitations run strictly by points descending, then date of effect ascending.</b></li>
      <li><b>So the allocation lands on a boundary score.</b> Everything above it is fully exhausted; the boundary
      score itself is usually rationed by date (79% of groups); everything below is untouched.</li>
      <li><b>The published tie-break date is the boundary date at the national floor.</b> Of every score invited in
      Jun-2026, only 65 points stops at April 2026 &mdash; every other score reaches June. That is why it does not
      exclude a recent high-scoring applicant.</li>
    </ol>
    <p class="note" style="margin-top:12px"><b>Residual.</b> 13 of 58 rationed cells sit above their group's lowest
    invited score, which strict points-then-date forbids. Cause: submission month is not date of effect. An EOI whose
    points changed carries an old submission month but a fresh date of effect, so the exhaustion probe misreads it.
    Confirmed directly &mdash; 2349's 85-point cell fell from 10 to 1 across the Jun-2026 round, then refilled to 13 by
    August including a 2024-submitted EOI absent in June and July, which can only have re-entered at 85 with a 2026
    date of effect.</p>
  </div>
</section>

<section>
  <h2>Checked against the official round results</h2>
  <p class="sub">The Department published per-occupation minimum scores for the 4 June 2026 round. Those figures were
  not used to build this model &mdash; they are an independent answer key for cut-offs derived from raw EOI records.</p>
  <div class="panel"><div class="statrow">
    <div class="stat"><span class="sv">{cal['n']}</span><span class="sl">occupations cross-checked</span></div>
    <div class="stat"><span class="sv">{100*cal['exact']/cal['n']:.1f}%</span><span class="sl">exactly right</span></div>
    <div class="stat"><span class="sv">{100*cal['within5']/cal['n']:.1f}%</span><span class="sl">within &plusmn;5 points</span></div>
    <div class="stat"><span class="sv">{cal['r']}</span><span class="sl">correlation r</span></div>
    <div class="stat"><span class="sv">{cal['bias']:+.2f}</span><span class="sl">bias, points</span></div>
  </div></div>
  <p class="note"><b>Every one of the 12 disagreements is positive</b> (+5 in eleven cases, +10 in one) and none negative.
  That is the signature of the single-leg filter: where the marginal invitee was a multi-leg EOI, the derived cut-off lands
  one tier high. The method is conservative by construction &mdash; it cannot overstate a candidate's chances.
  The round-size estimate is validated too: <b>9,761 derived against 10,000 official</b>, a 2.4% error.
  For Physicist the model derived <b>80</b> and the Department published <b>80</b>.</p>
</section>

<section>
  <h2>The whole model reduces to one threshold</h2>
  <p class="sub">Within a unit group, a round invites strictly down the points order. {fw['ahead_now']} people in ANZSCO 2349
  sit ahead of you on 85+ points &mdash; every one of them verified to hold a date of effect before 10 Sep 2026.
  You are invited if and only if the round allocates at least that many invitations to 2349.</p>
  <div class="panel scroll" style="margin-bottom:14px"><table>
    <thead><tr><th>If the round is held</th><th>Ahead of you lapsed</th><th>Your rank</th><th>Allocation needed</th></tr></thead>
    <tbody>
     <tr><td class="rd">by 30 Sep 2026</td><td class="n">2</td><td class="n">{SEP['rank']}</td><td class="n">&ge; {SEP['rank']}</td></tr>
     <tr><td class="rd">by 31 Dec 2026</td><td class="n">4</td><td class="n">{DEC['rank']}</td><td class="n">&ge; {DEC['rank']}</td></tr>
    </tbody></table></div>
  <div class="panel scroll"><table>
    <thead><tr><th>Round</th><th>Allocation to 2349</th><th>Recency weight</th><th>Covers a Sep-2026 round?</th></tr></thead>
    <tbody>{thr}</tbody></table></div>
  <p class="note">Allocation history <b>5 &rarr; 21 &rarr; 29 &rarr; 43 &rarr; 87</b> &mdash; monotone increasing, 17.4&times; over
  five rounds, and 2349's share of the round grew from 0.12% to 1.67%. <b>The downside risk is not your score.</b>
  It is a policy cut returning this stratum's allocation below {RANK}, as in Sep-2024, Nov-2024 and Aug-2025.</p>
</section>

<section>
  <h2>Why trust the mechanism: it predicts other occupations out of sample</h2>
  <p class="sub">Take each occupation's standing pool and its allocation, walk down the points order, and read off where
  the invitations run out. Tested against every occupation receiving 5+ invitations in Jun-2026 &mdash; a round the rule
  was not fitted to.</p>
  <div class="panel"><div class="statrow">
    <div class="stat"><span class="sv">49</span><span class="sl">occupations tested</span></div>
    <div class="stat"><span class="sv">100%</span><span class="sl">within &plusmn;5 points</span></div>
    <div class="stat"><span class="sv">43%</span><span class="sl">exactly right</span></div>
    <div class="stat"><span class="sv">0.94</span><span class="sl">correlation r</span></div>
    <div class="stat"><span class="sv">+2.9</span><span class="sl">bias, pts (conservative)</span></div>
  </div></div>
  <p class="note">The bias is positive: real rounds go <i>deeper</i> than the rule predicts, so applying it to your case understates your odds.</p>
</section>

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
   <thead><tr><th>Round</th><th>189-only invites</th><th>Est. total</th><th>To 2349</th><th>2349 stock &ge;85</th><th>2349 cut-off</th></tr></thead>
   <tbody>{rows}</tbody></table></div>
  <p class="note">Allocation to 2349 and its &ge;85 stock are both on the all-leg basis, so they are directly comparable;
  round size is quoted single-leg with a difference-in-differences estimate of the true total.
  The 2024 rows look self-contradictory &mdash; Nov-2024 allocated 21 against a recorded stock of 14 yet held the cut-off at 90
  &mdash; because the panel was still filling in late 2024 and understates the true standing pool then. The backtest below is run
  on Jun-2026 only, where coverage is complete.
  "189-only" counts EOIs whose <i>only</i> visa leg is 189, so the invitation is unambiguously a 189 invitation.
  "Est. total" adds multi-leg EOIs via a difference-in-differences correction against non-round months.</p>
</section>

<section>
  <h2>Macroscopic drivers</h2>
  <p class="sub">What moves the answer is not any one applicant's attributes but the balance between a pool growing
  faster than it is cleared, and an allocation to small scientific occupations that has been expanding sharply.</p>
  <div class="panel"><div class="statrow">
    <div class="stat"><span class="sv">+{gm['inflow']:,}</span><span class="sl">net EOIs added to the 189 pool each month</span></div>
    <div class="stat"><span class="sv">180,651</span><span class="sl">standing 189 pool, Aug 2026</span></div>
    <div class="stat"><span class="sv">{gm['concentration_top10']}%</span><span class="sl">of Jun-2026 went to 10 occupations</span></div>
    <div class="stat"><span class="sv">17.4&times;</span><span class="sl">growth in 2349's allocation</span></div>
    <div class="stat"><span class="sv">1.67%</span><span class="sl">2349 share of the round, up from 0.12%</span></div>
  </div></div>
  <div class="findings" style="margin-top:16px">
    <div class="find"><h3>The tie-break date does not lock out a recent EOI</h3>
    <p>June 2026's published tie-break was April 2026, which sounds fatal for a 10 Sep lodgement. It is not:
    <b>20.2% of invitations at 90+ points went to EOIs dated after that tie-break</b>. The date binds only at the
    marginal position within a score, not across all scores.</p></div>
    <div class="find"><h3>EOIs expire on a hard two-year cliff</h3>
    <p>Cohort survival runs 96% at 0&ndash;6 months, 82% at 12&ndash;18, 77% at 18&ndash;24, then collapses to
    <b>0.8% beyond 24 months</b>. Four of the 31 people ahead of you in 2349 lapse by the end of 2026, which is
    why your rank improves simply by waiting.</p></div>
    <div class="find"><h3>The occupation ceiling is not the binding constraint</h3>
    <p>ANZSCO 2349's annual ceiling is <b>500</b>, and the largest round used only <b>87</b> of it. Nothing caps this
    group from going deeper &mdash; a downside risk this model had flagged and can now discharge.</p></div>
  </div>
  <p class="note">Invitations are highly concentrated: ten unit groups absorb two thirds of a round, thirty absorb 94%.
  Being in a small, low-competition group is an advantage here &mdash; 2349's cut-off fell while the national floor stayed at 65.
  <b>Not visible in this data:</b> annual planning levels and ministerial direction on occupation priority. Those set
  round size and cadence, and no amount of EOI data substitutes for them.</p>
</section>

<section>
  <h2>If you also hold 190 or 491 EOIs</h2>
  <p class="sub">State-nominated subclasses are not points-ranked federally &mdash; a state selects against its own criteria,
  so a queue model does not transfer. For context only, here is where physicists stand in those pools.</p>
  <div class="panel scroll"><table>
   <thead><tr><th>Subclass</th><th>Physicist EOIs</th><th>At 90+ pts (= 85 + nomination)</th></tr></thead>
   <tbody>
    <tr><td class="rd">190 State Nominated</td><td class="n">{n190}</td><td class="n">{g190}</td></tr>
    <tr><td class="rd">491 Regional Nominated</td><td class="n">{n491}</td><td class="n">{g491}</td></tr>
   </tbody></table></div>
  <p class="note">A 190 nomination adds 5 points and a 491 adds 15, so an 85-point 189 profile appears at 90 and 100 in those pools.</p>
</section>

<section>
  <h2>Look up any occupation</h2>
  <p class="sub">The points cut-off each ANZSCO occupation actually reached in each of the five rounds, with its current
  standing pool. Green means that round would have reached your score; set your own points below. A dash means
  the occupation received no invitation in that round. Small number beside each cut-off is that round's invitation count.</p>
  <div class="panel">
    <div class="ctl">
      <input type="search" id="q" style="flex:1;min-width:220px" placeholder="Search 181 occupations — try 'physicist', '2613', 'nurse'" aria-label="Search occupations">
      <label for="pts">Your points</label><input type="number" id="pts" value="85" min="0" max="180" step="5" aria-label="Your points score">
    </div>
    <div class="scroll" style="margin-top:14px;max-height:440px;overflow-y:auto"><table id="t">
      <thead><tr><th>Occupation</th>{''.join(f'<th>{LBL[r]}</th>' for r in ROUNDS)}<th>Pool @85</th><th>Pool &gt;85</th></tr></thead>
      <tbody></tbody></table></div>
  </div>
</section>

<section>
  <h2>Two things everyone else gets wrong about this data</h2>
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
  submission, conservative. Official round figures (4 June 2026: 10,000 invitations, per-occupation minimum scores, April 2026 tie-break,
  next round expected by 30 September 2026) are as published by the Department of Home Affairs and republished by
  ahclawyers.com and studynash.co; the Home Affairs page itself returned 403 to automated fetch, so treat the
  expected round date as a secondary-source paraphrase rather than a departmental commitment.
  Occupation ceiling for 2349 (500, FY2025-26) via immitrend.com.au. Not migration advice. Code and data:
  <a href="https://github.com/SzeChunYiu/189-visa-invitation">github.com/SzeChunYiu/189-visa-invitation</a>
</footer>
</div>
<script>
const D={DATA},R={json.dumps(ROUNDS)};
const tb=document.querySelector("#t tbody"),q=document.getElementById("q"),pts=document.getElementById("pts");
let PTS=85;
function cell(c){{
  if(!c) return "<td class='n dim'>&mdash;</td>";
  const [cleared,boundary,state,n]=c;
  let k,lab;
  if(cleared!==null && PTS>=cleared){{k="ok";lab="in";}}
  else if(PTS>=boundary){{k="mid";lab="date";}}
  else {{k="no";lab="out";}}
  const shown = (cleared!==null && PTS>=cleared) ? cleared : boundary;
  return `<td class='n'><span class='pill ${{k}}' title='lowest fully cleared ${{cleared===null?"none":cleared}}, boundary ${{boundary}} (${{state==="C"?"cleared":"rationed"}}), ${{n}} invited'>${{shown}}</span><span class='dim' style='font-size:11px'> ${{lab}}</span></td>`;}}
function render(f){{
  tb.innerHTML=D.filter(r=>r.o.toLowerCase().includes(f)).map(r=>
    `<tr><td class='rd'>${{r.o}}</td>${{R.map(k=>cell(r[k])).join("")}}<td class='n'>${{r.p85}}</td><td class='n'>${{r.pg}}</td></tr>`).join("")
    || "<tr><td colspan='8' class='dim' style='padding:18px'>No occupation matches that search.</td></tr>";}}
q.addEventListener("input",e=>render(e.target.value.toLowerCase().trim()));
pts.addEventListener("input",e=>{{PTS=+e.target.value||0;render(q.value.toLowerCase().trim());}});
q.value="physicist";render("physicist");
</script>"""
OUT.parent.mkdir(exist_ok=True); OUT.write_text(HTML)
print(f"wrote {OUT}  ({len(HTML):,} bytes, {len(recs)} occupations)")
