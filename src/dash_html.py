HTML = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SkillSelect 189 Explorer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<style>__CSS__</style>
<a class="skip" href="#results">Skip to result</a>
<div class="wrap">
<header>
  <div>
    <div class="eyebrow">Subclass 189 &middot; Points-Tested Stream</div>
  </div>
  <div style="text-align:right">
    <div class="eyebrow">Pool snapshot Aug 2026 &middot; 5 rounds</div>
  </div>
</header>

<div class="filters">
  <div class="f combo">
    <label for="occ">Occupation</label>
    <div class="ctl">
      <button class="stepbtn" id="occprev" type="button" aria-label="Previous occupation" title="Previous occupation (Alt + \u2190)">&#8249;</button>
      <input id="occ" type="text" autocomplete="off" spellcheck="false" placeholder="Type to search, or step with \u2039 \u203a" aria-label="Occupation">
      <button class="stepbtn" id="occnext" type="button" aria-label="Next occupation" title="Next occupation (Alt + \u2192)">&#8250;</button>
    </div>
    <div class="opts" id="opts" role="listbox"></div>
  </div>
  <div class="f"><label for="pts">Your points</label>
    <div class="ctl">
      <button class="stepbtn" id="ptsdn" type="button" aria-label="Five points lower">&#8722;</button>
      <input id="pts" type="number" value="85" min="65" max="130" step="5" aria-label="Your points score">
      <button class="stepbtn" id="ptsup" type="button" aria-label="Five points higher">&#43;</button>
    </div>
  </div>
  <div class="f dlwrap"><label for="dl">Data</label>
    <button id="dl" class="dlbtn" type="button">Download CSV</button></div>
  <div class="f"><label for="doe">EOI date <span style="opacity:.7">(optional)</span></label>
    <div class="ctl">
      <button class="stepbtn" id="doedn" type="button" aria-label="Earlier month">&#8249;</button>
      <select id="doe" aria-label="Month your EOI was submitted or last changed">
        <option value="">Not given &mdash; assume last in band</option>
      </select>
      <button class="stepbtn" id="doeup" type="button" aria-label="Later month">&#8250;</button>
    </div>
  </div>
</div>

<div class="verdict" id="results" tabindex="-1">
  <h1 class="sr-only">Your chance of a subclass 189 invitation</h1>
  <div class="vmain">
    <div id="flag" class="vflag good"></div>
    <div class="hero" id="hero"></div>
    <p class="vsub" id="vsub"></p>
  </div>
  <div class="vside" id="vside"></div>
</div>

<div class="card"><div class="chead"><span class="stepbadge">Step 6<i>your chance at each size</i></span><h2>Your chance vs round size</h2>
  <span class="eyebrow" id="h8n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n1" aria-label="Explain" data-note="n1">?</button></div>
  <div class="chartwrap"><svg id="c8" viewBox="0 0 560 268" role="img" aria-labelledby="c8t">
    <title id="c8t">Chance of an invitation against the size of the next round</title></svg></div>
  <div class="note" id="n1" hidden><ul class="ptlist"><li><b>Blue line</b> — your chance at each round size</li><li><b>Faint lines</b> — the same 5 points above and below yours</li><li><b>Shaded band</b> — every round size on record</li><li><b>Green ribbon</b> — how likely each size is</li><li><b>Dashed line</b> — the size the published planning levels imply</li></ul></div></div>


<div class="grid2">
  <div class="card"><div class="chead"><span class="stepbadge">Joint<i>both unknowns together</i></span><h2>Your chance at every score and round size</h2>
  <span class="eyebrow" id="h13n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n13" aria-label="Explain" data-note="n13">?</button></div>
  <div class="chartwrap"><svg id="c13" viewBox="0 0 560 330" role="img" aria-labelledby="c13t">
    <title id="c13t">Chance of an invitation across score and round size, with both margins</title></svg></div>
  <div class="note" id="n13" hidden><ul class="ptlist">
    <li><b>Each cell</b> — your chance at that score, if the round is that size</li>
    <li><b>Top margin</b> — the round-size distribution: how much each column counts</li>
    <li><b>Right margin</b> — the chance at each score once round size is averaged out, which is the headline read across scores</li>
    <li><b>Your cell</b> is outlined; the headline is the right margin at your score</li>
    <li>Everything else on this page is a slice through this surface</li>
  </ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 5<i>whether the group is invited</i></span><h2>Whether your group gets a round</h2>
  <span class="eyebrow" id="h10n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n10" aria-label="Explain" data-note="n10">?</button></div>
  <div class="chartwrap"><svg id="c10" viewBox="0 0 560 200" role="img" aria-labelledby="c10t">
    <title id="c10t">Invitation rate by priority tier, with your group marked</title></svg></div>
  <div class="note" id="n10" hidden><ul class="ptlist">
    <li><b>Bars</b> — invitations per 1,000 people waiting, by priority tier</li>
    <li><b>Your tier</b> — filled; the others faint</li>
    <li>Whether a group was invited last round predicts this better than its tier does, so the model uses that; the tier is why</li>
  </ul></div>
</div>
<div class="card" id="nofc" hidden><div class="chead"><span class="stepbadge">Why<i>no forecast for this group</i></span><h2>What happened to this occupation</h2>
  <span class="eyebrow" id="h14n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n14" aria-label="Explain" data-note="n14">?</button></div>
  <p class="takeaway" id="t14"></p>
  <div class="chartwrap"><svg id="c14" viewBox="0 0 560 190" role="img" aria-labelledby="c14t">
    <title id="c14t">Invitations to this unit group, round by round</title></svg></div>
  <div class="note" id="n14" hidden><ul class="ptlist">
    <li><b>Bars</b> — invitations this unit group received in each round</li>
    <li>A group with none in the most recent round has no share to carry forward, so equation 1 gives nothing to forecast</li>
    <li>This is the largest single fact about such an occupation, and it is a policy decision rather than a shortage of candidates</li>
    <li>The <a href="policy.html">Policy page</a> lists every group this happened to; <a href="findings.html#zero">chapter 8</a> tests why</li>
  </ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 1<i>how big is the next round</i></span><h2>Invitations in the next round</h2>
  <span class="eyebrow" id="h11n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n11" aria-label="Explain" data-note="n11">?</button></div>
  <div class="chartwrap"><svg id="c11" viewBox="0 0 560 214" role="img" aria-labelledby="c11t">
    <title id="c11t">Distribution of the size of the next invitation round</title></svg></div>
  <div class="note" id="n11" hidden><ul class="ptlist">
    <li><b>Curve</b> — how likely each round size is, across all occupations</li>
    <li><b>Built from</b> the published places for the year, the invitations issued per place, and how many rounds are still expected</li>
    <li><b>The bumps are real</b> — each corresponds to a different number of rounds remaining</li>
    <li>Nobody publishes this. Everything downstream is averaged over it rather than assuming one size</li>
  </ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 2<i>how many go to your group</i></span><h2>Your unit group&rsquo;s share</h2>
  <span class="eyebrow" id="h12n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n12" aria-label="Explain" data-note="n12">?</button></div>
  <div class="chartwrap"><svg id="c12" viewBox="0 0 560 214" role="img" aria-labelledby="c12t">
    <title id="c12t">Places your unit group receives, against the size of the round</title></svg></div>
  <div class="note" id="n12" hidden><ul class="ptlist">
    <li><b>Line</b> — places your unit group receives at each round size</li>
    <li><b>Share</b> — what the group took last round, over everything issued that round</li>
    <li><b>Shaded</b> — the round sizes most likely to happen</li>
    <li>Invitations are rationed at the four-digit unit group, so this is the number your occupation actually competes for</li>
  </ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 3<i>what cut-off that produces</i></span><h2>Forecast cut-off by round size</h2>
  <span class="eyebrow" id="h2n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n2f" aria-label="Explain" data-note="n2f">?</button></div>
  <div class="chartwrap"><svg id="c2" viewBox="0 0 560 250" role="img" aria-labelledby="c2t">
    <title id="c2t">Forecast cut-off against round size, with its 80% interval</title></svg></div>
  <div class="note" id="n2f" hidden><ul class="ptlist"><li><b>Line</b> — predicted cut-off at each round size</li><li><b>Band</b> — the 80% interval on that prediction</li><li>Above the band you clear comfortably; inside it the round could go either way</li></ul></div>
  <div class="tablewrap"><table id="fctab"><caption class="sr-only">Forecast cut-off at each round size</caption></table></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Summary<i>the whole calculation</i></span><h2>From the cut-off to your chance</h2>
  <span class="eyebrow" id="h9n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n9w" aria-label="Explain" data-note="n9w">?</button></div>
  <div class="chartwrap"><svg id="c9" viewBox="0 0 560 210" role="img" aria-labelledby="c9t">
    <title id="c9t">Deductions from the cut-off probability to the final chance</title></svg></div>
  <div class="note" id="n9w" hidden><ul class="ptlist"><li>The cut-off reaching your score is not the same as being invited</li><li><b>Boundary band</b> — the cut-off can land on your score, where places go by date of effect</li><li><b>Round size</b> — smaller rounds cut deeper, and they are averaged in</li><li><b>Skip risk</b> — the group can receive nothing at all</li></ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 3<i>what cut-off that produces</i></span><h2>Past rounds</h2>
    <span class="eyebrow" id="h1n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n2" aria-label="Explain" data-note="n2">?</button></div>
    <div class="chartwrap"><svg id="c1" viewBox="0 0 560 220" role="img" aria-labelledby="c1t"><title id="c1t">Minimum points invited, by round</title></svg></div>
    <div class="note" id="n2" hidden><ul class="ptlist"><li><b>Height</b> — lowest score invited that round</li><li><span style='color:var(--good)'>&#9679;</span> you would be in &nbsp;<span style='color:var(--warn)'>&#9679;</span> date decides &nbsp;<span style='color:var(--crit)'>&#9679;</span> not reached</li><li><b>Dot size</b> — invitations to this occupation</li><li><b>Right-hand column</b> — the next round, as a distribution</li></ul></div></div>
      <div class="card"><div class="chead"><span class="stepbadge">Step 3<i>what cut-off that produces</i></span><h2>Who is ahead</h2>
    <span class="eyebrow" id="h4n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n3" aria-label="Explain" data-note="n3">?</button></div>
    <div class="chartwrap"><svg id="c4" viewBox="0 0 560 220" role="img" aria-labelledby="c4t"><title id="c4t">Queue position within the unit group</title></svg></div>
    <div class="note" id="n3" hidden><ul class="ptlist"><li><b>Blue</b> — people counted from the top score down</li><li><b>Green</b> — invitations issued last round</li><li><b>Shaded area</b> — everyone ahead of you</li></ul></div></div>
</div>

<div class="card"><div class="chead"><h2>What the people at each score hold</h2>
  <span class="eyebrow" id="h3n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n3c" aria-label="Explain" data-note="n3c">?</button></div>
  <div class="chartwrap"><svg id="c3" viewBox="0 0 560 250" role="img" aria-labelledby="c3t">
    <title id="c3t">Share holding each points component, by score</title></svg></div>
  <div class="note" id="n3c" hidden><ul class="ptlist"><li>Share of people at each score holding each component, in your unit group</li><li><b>Faint bars</b> — fewer than ten people waiting, so the share is noise</li></ul></div>
</div>
<div class="card"><div class="chead"><span class="stepbadge">Step 4<i>where you sit in that band</i></span><h2>Your place in the queue</h2>
  <span class="eyebrow" id="h5n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n5q" aria-label="Explain" data-note="n5q">?</button></div>
  <div class="chartwrap"><svg id="c5" viewBox="0 0 560 230" role="img" aria-labelledby="c5t">
    <title id="c5t">Date-of-effect distribution within your score band</title></svg></div>
  <div class="note" id="n5q" hidden><ul class="ptlist"><li>Inside one score band, invitations go in date-of-effect order, earliest first</li><li><b>Curve</b> — the share of your band dated by each month</li><li>With no date set, the model assumes you are last</li></ul></div>
</div>
<div class="card"><div class="chead"><h2>Every score band</h2>
  <span class="eyebrow" id="hbn"></span><button class="q" type="button" aria-expanded="false" aria-controls="n4" aria-label="Explain" data-note="n4">?</button></div>
  <div class="lev" id="lev"></div>
  <div class="scroll"><table id="bt"><thead><tr><th>Points</th><th>This occupation</th>
    <th>Unit group</th><th>Cumulative ahead</th><th>vs you</th>
    <th>Chance</th></tr></thead><tbody></tbody></table></div>
  <div class="note" id="n4" hidden><ul class="ptlist"><li>What 5 or 10 more points would buy</li><li>Aug-2026 snapshot; order is points, then date of effect</li></ul></div></div>

<div class="card"><div class="chead"><h2>Occupations cut off since 2025</h2>
  <span class="eyebrow" id="hswn"></span></div>
  <p class="takeaway" id="tsw"></p>
  <div class="scroll"><table id="swt"><thead><tr><th>Occupation group</th><th>Waiting</th>
    <th>Sep 24</th><th>Nov 24</th><th>Aug 25</th><th>Nov 25</th><th>Jun 26</th></tr></thead><tbody></tbody></table></div>
  </div>

<div class="card"><div class="chead"><h2>2026&ndash;27 program</h2>
  <span class="eyebrow">published planning levels</span><button class="q" type="button" aria-expanded="false" aria-controls="n5" aria-label="Explain" data-note="n5">?</button></div>
  <div class="scroll"><table id="pt"><thead><tr><th>Category</th><th>2025&ndash;26</th><th>2026&ndash;27</th><th>Change</th></tr></thead><tbody></tbody></table></div>
  <p class="note" data-role="pnote" id="n5" hidden></p></div>

<div class="grid2">
  <div class="card"><div class="chead"><h2>All occupations &times; all rounds</h2>
    <select id="hmsort" aria-label="Sort the landscape" style="font:inherit;font-size:11.5px;padding:4px 7px;
      border:1px solid var(--line);border-radius:7px;background:var(--paper);color:var(--body)">
      <option value="cut">by cut-off</option>
      <option value="alloc">by invitations</option>
      <option value="name">by code</option></select><button class="q" type="button" aria-expanded="false" aria-controls="n6" aria-label="Explain" data-note="n6">?</button></div>
    <div class="hm"><svg id="c6" viewBox="0 0 560 1420" role="img" aria-labelledby="c6t"><title id="c6t">Cut-off by unit group and round</title></svg></div>
    <div class="legend"><span>lowest points invited</span>
      <span class="ramp"><span style="background:var(--r1)"></span><span style="background:var(--r2)"></span><span style="background:var(--r3)"></span><span style="background:var(--r4)"></span><span style="background:var(--r5)"></span><span style="background:var(--r6)"></span><span style="background:var(--r7)"></span></span>
      <span>65 &rarr; 100+</span><span><i style="background:var(--deemph)"></i>no invitation</span></div>
    <div class="note" id="n6" hidden><ul class="ptlist"><li><b>Darker</b> — higher score needed</li><li><b>A dot</b> — no invitations that round</li><li>Click a row to load that occupation</li></ul></div></div>
  <div class="card"><div class="chead"><h2>Competition drives the score</h2>
    <span class="eyebrow">Jun 2026 round</span><button class="q" type="button" aria-expanded="false" aria-controls="n7" aria-label="Explain" data-note="n7">?</button></div>
    <p class="takeaway" id="t7"></p>
    <div class="chartwrap"><svg id="c7" viewBox="0 0 560 312" role="img" aria-labelledby="c7t"><title id="c7t">Pool size against cut-off</title></svg></div>
    <div class="note" id="n7" hidden><ul class="ptlist"><li><b>One dot</b> — one unit group</li><li><b>Right</b> — more people per invitation</li><li><b>Up</b> — higher score needed</li><li>The corner you want is bottom-left</li></ul></div></div>
</div>

<div class="card"><div class="chead"><h2>This occupation, round by round</h2><span class="eyebrow">the record for this occupation</span><button class="q" type="button" aria-expanded="false" aria-controls="n8" aria-label="Explain" data-note="n8">?</button></div>
  <div class="scroll"><table id="rt"><thead><tr><th>Round</th><th>Invited</th><th>Fully cleared to</th>
    <th>Boundary score</th><th>Boundary</th><th>Would you have been invited?</th></tr></thead><tbody></tbody></table></div>
  <div class="note" id="n8" hidden><ul class="ptlist"><li><b>Fully cleared to</b> — the lowest score where every EOI was invited</li><li>At or below that score, points alone decided it</li><li>Above it, date of effect decided it</li></ul></div></div>

<div class="card"><div class="chead"><h2>All occupations at your score</h2>
  <span style="display:flex;gap:12px;align-items:center">
    <span class="eyebrow" id="allN"></span>
    </span><button class="q" type="button" aria-expanded="false" aria-controls="n9" aria-label="Explain" data-note="n9">?</button></div>
  <div class="scroll" style="max-height:420px;overflow-y:auto"><table id="at"><thead><tr><th>Occupation</th>
    <th>Pool</th><th>At your score</th><th>Sep 24</th><th>Nov 24</th><th>Aug 25</th><th>Nov 25</th><th>Jun 26</th>
    <th>Forecast</th></tr></thead><tbody></tbody></table></div>
  <div class="note" id="n9" hidden><ul class="ptlist"><li>Click a row to load it</li><li>The CSV holds every figure behind this page, for all occupations</li></ul></div></div>

<footer>
  Built from all 24 monthly SkillSelect EOI snapshots read directly from the Qlik engine behind the Department of
  Employment's public dashboard. Counts are distinct EOIs on a single-leg basis. The model cannot predict whether a
  round is held or how large it is &mdash; both are set by migration planning levels. Not migration advice.
  <a href="https://github.com/SzeChunYiu/189-visa-invitation">Code, data and method</a> &middot;
  <a href="findings.html">Full findings</a>
</footer>
</div>
<div id="tip" role="status"></div>
<div id="popbd"></div>
<div id="pop" role="dialog" aria-modal="false" aria-labelledby="poph">
  <button type="button" id="popx" aria-label="Close">&times;</button>
  <h4 id="poph"></h4><div id="popb"></div></div>
<script>
const B=__BUNDLE__;
const S={occ:"234914 Physicist",pts:85,szi:2,doe:null};   /* szi 2 = the policy-implied central case, not a user guess */
const $=id=>document.getElementById(id);
const $$=id=>$(id)||{style:{},classList:{add(){},remove(){},toggle(){}},appendChild(){},addEventListener(){}};
const RL={"2024-09":"Sep 24","2024-11":"Nov 24","2025-08":"Aug 25","2025-11":"Nov 25","2026-06":"Jun 26"};
const OCCS=Object.keys(B.occ).sort();
const fmt=n=>n.toLocaleString();

/* ---------- verdict logic: one definition used everywhere ---------- */
function verdictFor(rd,pts){
  if(rd.b===null) return {k:"n",t:"no invitations"};
  if(rd.lc!==null && pts>=rd.lc) return {k:"good",t:"invited"};
  if(pts>=rd.b) return {k:"warn",t:"date decides"};
  return {k:"crit",t:"not reached"};
}

__MODEL__





/* ---------- svg helpers ---------- */
const NS="http://www.w3.org/2000/svg";
function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
function clear(s){while(s.childNodes.length>1)s.removeChild(s.lastChild);}
/* the code that draws owns the viewBox: a static one in the markup silently clips */
function noFc(s,W,H,line){
  const t=el("text",{x:W/2,y:H/2-6,class:"tick","text-anchor":"middle","font-weight":"700",
    fill:"var(--ink)"});
  t.textContent="No forecast for this group";s.appendChild(t);
  const t2=el("text",{x:W/2,y:H/2+10,class:"tick","text-anchor":"middle"});
  t2.textContent=line||"it received no invitations in the most recent round";s.appendChild(t2);
}
function frame(s,W,H){s.setAttribute("viewBox","0 0 "+W+" "+H);}
/* One legend beats an annotation beside every layer. kind: line | dash | band | dot */
function legend(s,x,y,items,gap){
  let cx=x;
  items.forEach(([kind,col,label])=>{
    if(kind==="line"||kind==="dash")
      s.appendChild(el("line",{x1:cx,y1:y,x2:cx+14,y2:y,stroke:col,"stroke-width":2.4,
        "stroke-dasharray":kind==="dash"?"5 3":"0","stroke-linecap":"round"}));
    else if(kind==="band")
      s.appendChild(el("rect",{x:cx,y:y-4.5,width:14,height:9,rx:2,fill:col,"fill-opacity":".3"}));
    else
      s.appendChild(el("circle",{cx:cx+7,cy:y,r:4,fill:"var(--card)",stroke:col,"stroke-width":2.2}));
    const t=el("text",{x:cx+19,y:y+3.5,class:"tick","text-anchor":"start"});
    t.textContent=label;s.appendChild(t);
    cx+=19+label.length*4.5+(gap||14);
  });
}
function tipOn(ev,html){const t=$("tip");t.innerHTML=html;t.style.display="block";
  const r=12;t.style.left=Math.min(ev.clientX+r,innerWidth-t.offsetWidth-8)+"px";
  t.style.top=Math.max(8,ev.clientY-t.offsetHeight-r)+"px";}
function tipOff(){$("tip").style.display="none";}
function on(id,ev,fn){const e=$(id); if(e) e.addEventListener(ev,fn); return !!e;}
function put(id,prop,val){const e=$(id); if(e) e[prop]=val; return !!e;}
/* Pointer-only. Marks are deliberately NOT tab stops: making 500+ of them focusable
   traps keyboard users. Every number in these charts is also in a table or the CSV. */
function hover(node,html){
  node.addEventListener("pointermove",e=>tipOn(e,html));
  node.addEventListener("pointerleave",tipOff);
  node.setAttribute("aria-hidden","true");}

function axisTitle(s,W,H,MB,xt,yt){
  if(xt){
    const x=el("text",{x:W/2,y:H-MB+33,class:"tick","text-anchor":"middle","font-weight":"600"});
    x.textContent=xt;s.appendChild(x);}
  if(yt){const y=el("text",{x:13,y:H/2,class:"tick","text-anchor":"middle","font-weight":"600",
    transform:"rotate(-90 13 "+(H/2)+")"});y.textContent=yt;s.appendChild(y);}}

/* ---------- chart 2: the forecast itself - cut-off vs round size, with its interval ---------- */
function chartForecast(g,pts){
  const s=$("c2"); if(!s) return; clear(s);
  const W=560,H=250,ML=46,MR=20,MT=22,MB=54,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g||g.share<=0){
    const q=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    noFc(s,W,H,"the cut-off cannot be projected without a share");return;}
  const grid=B.rs.grid, lo=B.floor, hi=100;
  const X=N=>ML+pw*(N-grid[0])/(grid[grid.length-1]-grid[0]);
  const Y=v=>MT+ph*(1-(v-lo)/(hi-lo));
  for(let v=lo;v<=hi;v+=5){
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    if(v%10===0){const q=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});
      q.textContent=v;s.appendChild(q);}}
  /* the 80% interval on the forecast, as a band */
  const cs=grid.map(N=>cutoffAt(g,N));
  let up="",dn="";
  grid.forEach((N,i)=>{const c=cs[i]; if(c===null) return;
    const t=Math.min(hi,c-B.unc.lo80), b=Math.max(lo,c-B.unc.hi80);
    up+=(up?"L":"M")+X(N).toFixed(1)+","+Y(t).toFixed(1)+" ";
    dn=("L"+X(N).toFixed(1)+","+Y(b).toFixed(1)+" ")+dn;});
  if(up) s.appendChild(el("path",{d:up+dn+"Z",fill:"var(--brand)",opacity:"0.14",stroke:"none"}));
  /* the forecast */
  let d="";
  grid.forEach((N,i)=>{const c=cs[i]; if(c===null) return;
    d+=(d?"L":"M")+X(N).toFixed(1)+","+Y(c).toFixed(1)+" ";});
  if(d) s.appendChild(el("path",{d:d,fill:"none",stroke:"var(--brand)","stroke-width":2.5,
    "stroke-linejoin":"round"}));
  /* your score */
  if(pts>=lo&&pts<=hi){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const q=el("text",{x:W-MR-3,y:Y(pts)-7,class:"reft","text-anchor":"end"});
    q.textContent="your "+pts;s.appendChild(q);}
  /* the likely-round-size window, so the reader knows which part of the x-axis matters */
  [["q10",B.rs.q10],["q50",B.rs.q50],["q90",B.rs.q90]].forEach(([k,N])=>{
    s.appendChild(el("line",{x1:X(N),y1:MT,x2:X(N),y2:MT+ph,
      stroke:k==="q50"?"var(--ink)":"var(--muted)","stroke-width":k==="q50"?1.5:1,
      "stroke-dasharray":"3 3"}));});
  const ml=el("text",{x:X(B.rs.q50),y:MT-6,class:"tick","text-anchor":"middle","font-weight":"700"});
  ml.textContent="likely round";s.appendChild(ml);
  /* markers at the published sizes, each hoverable */
  B.sizes.forEach((N,i)=>{const c=g.fc[i]; if(c===null||c===undefined) return;
    const cc=el("circle",{cx:X(N),cy:Y(c),r:5,fill:"var(--brand)",stroke:"var(--card)","stroke-width":2});
    s.appendChild(cc);
    hover(cc,"<b>"+c+" points</b><span>if the round is "+fmt(N)+"</span><span>80% interval "+
      (c-B.unc.hi80)+"&ndash;"+(c-B.unc.lo80)+"</span><span>At "+pts+" pts: "+fcVerdict(c,pts).t+"</span>");});
  for(const N of [grid[0],B.rs.q50,grid[grid.length-1]]){
    const q=el("text",{x:X(N),y:H-MB+18,class:"tick","text-anchor":"middle"});
    q.textContent=fmt(N);s.appendChild(q);}
  axisTitle(s,W,H,MB,"size of the next round","forecast cut-off (points)");
}
function fcTable(g,pts){
  const t=$("fctab"); if(!t) return; t.innerHTML="";
  if(!g||g.share<=0) return;
  const hd=document.createElement("tr");
  ["If the round is","Forecast cut-off","80% interval","At "+pts+" points"].forEach(h=>{
    const th=document.createElement("th");th.textContent=h;hd.appendChild(th);});
  t.appendChild(hd);
  B.sizes.forEach((N,i)=>{const c=g.fc[i];
    const tr=document.createElement("tr");
    const v=fcVerdict(c,pts);
    [[fmt(N),""],[c===null?"—":c+" pts","n"],
     [c===null?"—":(c-B.unc.hi80)+"–"+(c-B.unc.lo80),"n"],[v.t,""]].forEach(([txt,cls],k)=>{
      const td=document.createElement("td");td.textContent=txt;if(cls)td.className=cls;
      if(k===3){td.innerHTML='<span class="pill '+v.k+'">'+txt+'</span>';}
      tr.appendChild(td);});
    t.appendChild(tr);});
}

/* ---------- chart 3: what the pool's points are made of ---------- */
const COMPS=[["eng","superior English","var(--series)"],
             ["partner","partner points","var(--gold)"],
             ["study","Australian study","var(--c3)"]];
function chartComp(g,gk,pts){
  const s=$("c3"); if(!s) return; clear(s);
  /* Three overlapping lines crossed each other repeatedly wherever the cells are small.
     Small multiples: one row per component, bars, nothing can overlap anything. */
  const W=560,ROW=64,ML=104,MR=16,MT=8,GAP=8,MB=34;
  const H=MT+COMPS.length*(ROW+GAP)-GAP+MB;
  frame(s,W,H);
  if(!B.comp||!g) return;
  const scores=Object.keys(g.dist).map(Number).filter(v=>v>=B.floor).sort((a,b)=>a-b);
  if(!scores.length) return;
  const pw=W-ML-MR, bw=pw/scores.length;
  const X=i=>ML+i*bw;
  COMPS.forEach(([key,label,col],ci)=>{
    const top=MT+ci*(ROW+GAP), base=top+ROW;
    const src=(B.comp[key]||{})[gk]||{};
    s.appendChild(el("line",{x1:ML,y1:base,x2:ML+pw,y2:base,stroke:"var(--line)","stroke-width":1}));
    [0.5,1].forEach(q=>s.appendChild(el("line",{x1:ML,y1:base-ROW*q,x2:ML+pw,y2:base-ROW*q,class:"gl"})));
    const nm=el("text",{x:ML-10,y:top+ROW/2-2,class:"tick","text-anchor":"end",
      "font-weight":"700",fill:col});
    nm.textContent=label;s.appendChild(nm);
    const sub=el("text",{x:ML-10,y:top+ROW/2+11,class:"tick","text-anchor":"end"});
    sub.textContent="0–100%";s.appendChild(sub);
    scores.forEach((v,i)=>{
      const share=src[String(v)]; if(share===undefined) return;
      const n=g.dist[v]||0, thin=n<10;
      const h=Math.max(share>0?1.5:0,ROW*share);
      const r=el("rect",{x:X(i)+1,y:base-h,width:Math.max(1,bw-2),height:h,
        fill:col,opacity:thin?0.3:0.92,rx:2});
      s.appendChild(r);
      hover(r,"<b>"+Math.round(share*100)+"% hold "+label+"</b><span>at "+v+" points</span>"+
        "<span>"+fmt(n)+" waiting here"+(thin?" — too few to read much into":"")+"</span>");
    });
    if(pts>=scores[0]&&pts<=scores[scores.length-1]){
      const i=scores.indexOf(Math.round(pts/5)*5);
      if(i>=0) s.appendChild(el("line",{x1:X(i)+bw/2,y1:top-2,x2:X(i)+bw/2,y2:base+2,class:"refl"}));}
  });
  const base=MT+COMPS.length*(ROW+GAP)-GAP;
  scores.forEach((v,i)=>{if(v%10===0){
    const t=el("text",{x:X(i)+bw/2,y:base+15,class:"tick","text-anchor":"middle"});
    t.textContent=v;s.appendChild(t);}});
  const i=scores.indexOf(Math.round(pts/5)*5);
  if(i>=0){const t=el("text",{x:X(i)+bw/2,y:base+27,class:"reft","text-anchor":"middle"});
    t.textContent="you";s.appendChild(t);}
}
/* ---------- chart 5: date of effect inside your own band ---------- */
function chartDoe(gk,pts){
  const s=$("c5"); if(!s) return; clear(s);
  const W=560,H=230,ML=44,MR=20,MT=22,MB=52,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  const band=B.doe_cdf&&B.doe_cdf[gk]&&B.doe_cdf[gk][String(Math.round(pts/5)*5)];
  if(!band||!band.length){
    const q=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    q.textContent="No date-of-effect data at this score";s.appendChild(q);return;}
  const M=B.doe_months, i0=band[0][0], i1=band[band.length-1][0];
  const X=i=>ML+pw*(i-i0)/Math.max(1,i1-i0);
  const Y=p=>MT+ph*(1-p);
  for(let q=0;q<=1.0001;q+=0.25){
    s.appendChild(el("line",{x1:ML,y1:Y(q),x2:ML+pw,y2:Y(q),class:"gl"}));
    const t=el("text",{x:ML-7,y:Y(q)+3.5,class:"tick","text-anchor":"end"});
    t.textContent=Math.round(q*100)+"%";s.appendChild(t);}
  /* a step curve: the share dated on or before each month */
  let d="",prev=null;
  band.forEach(([i,c])=>{
    if(prev===null){d="M"+X(i).toFixed(1)+","+Y(c).toFixed(1)+" ";}
    else{d+="L"+X(i).toFixed(1)+","+Y(prev).toFixed(1)+" L"+X(i).toFixed(1)+","+Y(c).toFixed(1)+" ";}
    prev=c;});
  s.appendChild(el("path",{d:d,fill:"none",stroke:"var(--brand)","stroke-width":2.5}));
  band.forEach(([i,c])=>{const cc=el("circle",{cx:X(i),cy:Y(c),r:3.6,fill:"var(--brand)",
    stroke:"var(--card)","stroke-width":1.5});s.appendChild(cc);
    hover(cc,"<b>"+Math.round(c*100)+"% of your band</b><span>dated on or before "+M[i]+"</span>");});
  /* the outer labels anchor inward: centred, a 7-character month runs past the edge */
  [[i0,"start"],[Math.round((i0+i1)/2),"middle"],[i1,"end"]].forEach(([i,a])=>{
    if(i<i0||i>i1) return;
    const t=el("text",{x:X(i),y:H-MB+16,class:"tick","text-anchor":a});
    t.textContent=M[i];s.appendChild(t);});
  const sh=aheadShare(gk,pts);
  if(S.doe!==null&&sh!==null){
    const idx=M.indexOf(S.doe);
    if(idx>=0){
      s.appendChild(el("line",{x1:X(idx),y1:MT,x2:X(idx),y2:MT+ph,class:"refl"}));
      const near=X(idx)>ML+pw-30;
      const t=el("text",{x:X(idx)+(near?-4:4),y:MT+11,class:"reft",
        "text-anchor":near?"end":"start"});
      t.textContent=Math.round(sh*100)+"% dated ahead of you";s.appendChild(t);}
  }
  const h=$("h5n"); if(h) h.textContent=(Math.round(pts/5)*5)+"-point band";
  axisTitle(s,W,H,MB,"date of effect","share of the band dated by then");
}

/* ---------- chart 9: the deductions between the cut-off and the answer ---------- */
function chartWaterfall(g,gk,pts){
  const s=$("c9"); if(!s) return; clear(s);
  /* No assumed round size. Each level is the density-weighted mean across the whole
     round-size distribution, with a 1-sigma whisker for the spread the round size
     alone puts on it. That also removes the separate "averaging" step: the averaging
     is now inside every bar. */
  const W=560,H=236,ML=20,MR=20,MT=54,MB=64,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g||g.share<=0){noFc(s,W,H,"there is no share to deduct from");return;}
  const res=B.unc.residuals;
  const sh=aheadShare(gk,pts), reach=(sh===null?0:Math.max(0,1-sh));
  const reaches=spread(sz=>{const c=cutoffAt(g,sz); return c===null?null:pLE(c,pts);});
  const cleared=spread(sz=>pClear(cutoffAt(g,sz),pts));
  if(!reaches||!cleared) return;
  const z=pZero(gk), fin=cleared.mean*(1-z);
  const cols=[
    {kind:"total", v:reaches.mean, sd:reaches.sd, lab:"cut-off reaches "+pts, sub:"averaged over round size"},
    {kind:"drop", from:reaches.mean, to:cleared.mean, lab:"boundary band",
     sub:sh===null?"no date given":"date of effect"},
    {kind:"drop", from:cleared.mean, to:fin, lab:"group skipped", sub:Math.round(z*100)+"% of the time"},
    {kind:"total", v:fin, sd:cleared.sd*(1-z), lab:"your chance", sub:"if a round is held"}];
  const bw=pw/cols.length, Y=v=>MT+ph*(1-Math.max(0,Math.min(1,v)));
  for(let q=0;q<=1.0001;q+=0.25) s.appendChild(el("line",{x1:ML,y1:Y(q),x2:ML+pw,y2:Y(q),class:"gl"}));
  let prevX=null, prevY=null;
  cols.forEach((c,i)=>{
    const x=ML+i*bw+bw*0.19, bwid=bw*0.62;
    let top,hgt,fill,op;
    if(c.kind==="total"){top=Y(c.v);hgt=MT+ph-top;fill=i===0?"var(--series)":"var(--brand)";op=i===0?0.38:1;}
    else{top=Y(c.from);hgt=Math.max(2,Y(c.to)-Y(c.from));fill="var(--crit)";op=0.7;}
    s.appendChild(el("rect",{x:x,y:top,width:bwid,height:hgt,rx:6,fill:fill,"fill-opacity":op}));
    /* 1 sigma across round sizes, on the levels where the round size still matters */
    if(c.kind==="total"&&c.sd>0.002){
      const cx=x+bwid/2, hi=Y(c.v+c.sd), lo=Y(c.v-c.sd);
      s.appendChild(el("line",{x1:cx,y1:hi,x2:cx,y2:lo,stroke:"var(--ink)","stroke-width":1.5}));
      [hi,lo].forEach(yy=>s.appendChild(el("line",{x1:cx-5,y1:yy,x2:cx+5,y2:yy,
        stroke:"var(--ink)","stroke-width":1.5})));
      const right=cx+bwid/2+14<W-MR;
      const sdl=el("text",{x:right?cx+bwid/2+6:cx-bwid/2-6,y:(hi+lo)/2+3.5,
        class:"tick","text-anchor":right?"start":"end"});
      sdl.textContent="±"+Math.round(c.sd*100)+"pp";s.appendChild(sdl);
    }
    const val=c.kind==="total"?Math.round(c.v*100)+"%":"−"+Math.round((c.from-c.to)*100)+"pp";
    const t=el("text",{x:x+bwid/2,y:(c.kind==="total"?Y(c.v+(c.sd||0)):top)-8,class:"vlab",
      "text-anchor":"middle",fill:c.kind==="total"?"var(--ink)":"var(--crit)"});
    t.textContent=val;s.appendChild(t);
    const l1=el("text",{x:x+bwid/2,y:H-MB+18,class:"tick","text-anchor":"middle",
      "font-weight":"700",fill:"var(--ink)"});l1.textContent=c.lab;s.appendChild(l1);
    const l2=el("text",{x:x+bwid/2,y:H-MB+31,class:"tick","text-anchor":"middle"});
    l2.textContent=c.sub;s.appendChild(l2);
    const endY=Y(c.kind==="total"?c.v:c.to);
    if(prevX!==null) s.appendChild(el("line",{x1:prevX,y1:prevY,x2:x,y2:prevY,
      stroke:"var(--muted)","stroke-width":1,"stroke-dasharray":"3 3"}));
    prevX=x+bwid; prevY=endY;
  });
  const yl=el("text",{x:ML,y:MT-30,class:"tick","text-anchor":"start","font-weight":"700",
    fill:"var(--ink)"});
  yl.textContent="Two deductions separate the cut-off reaching you from being invited";
  s.appendChild(yl);
  const y2=el("text",{x:ML,y:MT-16,class:"tick","text-anchor":"start"});
  y2.textContent="whiskers are ±1 s.d. across the round sizes that could happen";
  s.appendChild(y2);
  const h=$("h9n"); if(h) h.textContent="across all plausible round sizes";
}


/* ---------- chart 10: whether the group gets a round at all ---------- */
function chartTierRate(g,gk){
  const s=$("c10"); if(!s) return; clear(s);
  const W=560,H=200,ML=16,MR=16,MT=40,MB=60,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!B.tiers||!B.tiers.by_tier) return;
  const bt=B.tiers.by_tier, keys=Object.keys(bt).sort();
  const mine=B.tiers.tier_of?String(B.tiers.tier_of[gk]||""):"";
  const mx=Math.max(...keys.map(k=>bt[k].per_1000));
  const bw=pw/keys.length;
  keys.forEach((k,i)=>{
    const r=bt[k], x=ML+i*bw+bw*0.2, wd=bw*0.6;
    const h=Math.max(2,ph*r.per_1000/mx), is=k===mine;
    const rect=el("rect",{x:x,y:MT+ph-h,width:wd,height:h,rx:6,
      fill:is?"var(--brand)":"var(--deemph)","fill-opacity":is?1:0.45});
    s.appendChild(rect);
    hover(rect,"<b>Tier "+k+"</b><span>"+r.per_1000.toFixed(1)+" invitations per 1,000 waiting</span>"+
      "<span>"+r.groups+" groups &middot; "+fmt(r.pool)+" people</span>"+
      "<span>received nothing in "+Math.round(r.zero_share*100)+"% of rounds</span>");
    const v=el("text",{x:x+wd/2,y:MT+ph-h-7,class:"vlab","text-anchor":"middle",
      fill:is?"var(--brand)":"var(--muted)"});
    v.textContent=r.per_1000.toFixed(0);s.appendChild(v);
    const l=el("text",{x:x+wd/2,y:H-MB+18,class:"tick","text-anchor":"middle",
      "font-weight":is?"700":"600",fill:is?"var(--ink)":"var(--muted)"});
    l.textContent="Tier "+k+(is?" — yours":"");s.appendChild(l);
    const l2=el("text",{x:x+wd/2,y:H-MB+31,class:"tick","text-anchor":"middle"});
    l2.textContent=Math.round(r.zero_share*100)+"% of rounds skipped";s.appendChild(l2);
  });
  const al=g?g.alloc[g.alloc.length-1]:0;
  const t=el("text",{x:ML,y:MT-22,class:"tick","text-anchor":"start","font-weight":"700",
    fill:"var(--ink)"});
  t.textContent=(al>0?"Your group was invited last round, so the model uses "
                     :"Your group received nothing last round, so the model uses ")+
    Math.round(pZero(gk)*100)+"% as its chance of being skipped";
  s.appendChild(t);
  const h=$("h10n"); if(h) h.textContent="invitations per 1,000 waiting";
  axisTitle(s,W,H,MB,"","");
}
/* ---------- chart 11: how big the next round is ---------- */
function chartRoundSize(){
  const s=$("c11"); if(!s) return; clear(s);
  const W=560,H=188,ML=20,MR=20,MT=18,MB=52,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!B.rs) return;
  const grid=B.rs.grid, dens=B.rs.dens, mx=Math.max(...dens);
  const X=N=>ML+pw*(N-grid[0])/(grid[grid.length-1]-grid[0]), Y=d=>MT+ph*(1-d/mx);
  const inner=grid.map((N,i)=>[N,dens[i]]).filter(([N])=>N>=B.rs.q10&&N<=B.rs.q90);
  if(inner.length){
    let bd="M"+X(inner[0][0]).toFixed(1)+","+(MT+ph).toFixed(1);
    inner.forEach(([N,d])=>{bd+=" L"+X(N).toFixed(1)+","+Y(d).toFixed(1);});
    bd+=" L"+X(inner[inner.length-1][0]).toFixed(1)+","+(MT+ph).toFixed(1)+" Z";
    s.appendChild(el("path",{d:bd,fill:"var(--brand)","fill-opacity":".16",stroke:"none"}));}
  let d="";
  grid.forEach((N,i)=>{d+=(i?" L":"M")+X(N).toFixed(1)+","+Y(dens[i]).toFixed(1);});
  s.appendChild(el("path",{d:d,fill:"none",stroke:"var(--brand)","stroke-width":2.5}));
  [["q10",B.rs.q10,"10% chance smaller"],["q50",B.rs.q50,"most likely"],["q90",B.rs.q90,"10% chance larger"]]
   .forEach(([k,N,lab])=>{
    const main=k==="q50";
    s.appendChild(el("line",{x1:X(N),y1:MT-4,x2:X(N),y2:MT+ph,
      stroke:main?"var(--ink)":"var(--muted)","stroke-width":main?1.5:1,"stroke-dasharray":"4 3"}));
    const t=el("text",{x:X(N),y:H-MB+18,class:"tick","text-anchor":"middle",
      "font-weight":main?"700":"600",fill:main?"var(--ink)":"var(--muted)"});
    t.textContent=fmt(N);s.appendChild(t);
    const t2=el("text",{x:X(N),y:H-MB+31,class:"tick","text-anchor":"middle"});
    t2.textContent=lab;s.appendChild(t2);});
  const h=$("h11n"); if(h) h.textContent="all occupations together";
  /* the derivation goes behind the (?), with the numbers it actually used */
  const nb=$("n11");
  if(nb) nb.innerHTML='<ul class="ptlist">'+
    "<li><b>"+fmt(B.policy.places["2026-27"])+" places</b> in the 189 programme for 2026&ndash;27</li>"+
    "<li><b>&times; "+B.policy.ratio+"</b> invitations issued per place, measured on the one "+
      "programme year where both numbers are published</li>"+
    "<li><b>= "+fmt(B.policy.projected_invitations)+" invitations</b> to issue, spread over the "+
      "rounds still expected &mdash; two, three or four</li>"+
    "<li><b>The bumps are real</b>: each is a different number of rounds remaining</li>"+
    "<li>Everything downstream is averaged over this curve rather than assuming one size</li></ul>";
}
/* ---------- chart 12: what your group gets out of it ---------- */
function chartGroupShare(g,gk){
  const s=$("c12"); if(!s) return; clear(s);
  const W=560,H=188,ML=52,MR=64,MT=18,MB=52,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g) return;
  const grid=B.rs.grid;
  const alloc=N=>Math.round(g.share*N*B.meta.fr);
  const mx=Math.max(1,alloc(grid[grid.length-1]),
    Math.round(g.share_hi*grid[grid.length-1]*B.meta.fr))*1.1;
  const X=N=>ML+pw*(N-grid[0])/(grid[grid.length-1]-grid[0]), Y=v=>MT+ph*(1-v/mx);
  for(const t of [0,mx*0.25,mx*0.5,mx*0.75,mx]){
    s.appendChild(el("line",{x1:ML,y1:Y(t),x2:ML+pw,y2:Y(t),class:"gl"}));
    const q=el("text",{x:ML-7,y:Y(t)+3.5,class:"tick","text-anchor":"end"});
    q.textContent=fmt(Math.round(t));s.appendChild(q);}
  [B.rs.q10,B.rs.q90].forEach(N=>s.appendChild(el("line",{x1:X(N),y1:MT,x2:X(N),y2:MT+ph,
    stroke:"var(--muted)","stroke-width":1,"stroke-dasharray":"2 4"})));
  /* the share carried forward is ONE round's. Across the rounds this group appeared in
     it has ranged this far, and that range is the honest uncertainty on this line. */
  if(g.share_hi>g.share_lo){
    const aHi=N=>Math.round(g.share_hi*N*B.meta.fr), aLo=N=>Math.round(g.share_lo*N*B.meta.fr);
    let up="",dn="";
    grid.forEach(N=>{up+=(up?"L":"M")+X(N).toFixed(1)+","+Y(Math.min(mx,aHi(N))).toFixed(1)+" ";});
    for(let i=grid.length-1;i>=0;i--) dn+="L"+X(grid[i]).toFixed(1)+","+Y(aLo(grid[i])).toFixed(1)+" ";
    s.appendChild(el("path",{d:up+dn+"Z",fill:"var(--brand)","fill-opacity":".13",stroke:"none"}));
    const rl=el("text",{x:ML+pw-4,y:Y(Math.min(mx,aHi(grid[grid.length-1])))+12,class:"tick",
      "text-anchor":"end"});
    rl.textContent="range of this group's share across past rounds";s.appendChild(rl);
  }
  let d="";
  grid.forEach((N,i)=>{d+=(i?" L":"M")+X(N).toFixed(1)+","+Y(alloc(N)).toFixed(1);});
  s.appendChild(el("path",{d:d,fill:"none",stroke:"var(--brand)","stroke-width":2.5}));
  const am=alloc(B.rs.q50);
  s.appendChild(el("line",{x1:X(B.rs.q50),y1:MT,x2:X(B.rs.q50),y2:MT+ph,
    stroke:"var(--ink)","stroke-width":1.5,"stroke-dasharray":"4 3"}));
  const dot=el("circle",{cx:X(B.rs.q50),cy:Y(am),r:5,fill:"var(--brand)",
    stroke:"var(--card)","stroke-width":2});
  s.appendChild(dot);
  hover(dot,"<b>"+fmt(am)+" places</b><span>at the most likely round of "+fmt(B.rs.q50)+"</span>");
  const aLoM=Math.round(g.share_lo*B.rs.q50*B.meta.fr),
        aHiM=Math.round(g.share_hi*B.rs.q50*B.meta.fr);
  const t=el("text",{x:X(B.rs.q50)+9,y:Y(am)-11,class:"vlab","text-anchor":"start",fill:"var(--brand)"});
  t.textContent=fmt(am)+" places";s.appendChild(t);
  if(aHiM>aLoM){
    const t2=el("text",{x:X(B.rs.q50)+9,y:Y(am)+2,class:"tick","text-anchor":"start"});
    t2.textContent=fmt(aLoM)+"–"+fmt(aHiM)+" on past shares";s.appendChild(t2);
    /* the bounds, marked where they fall */
    [[aLoM,"lowest share"],[aHiM,"highest share"]].forEach(([v,lab])=>{
      s.appendChild(el("line",{x1:X(B.rs.q50)-5,y1:Y(v),x2:X(B.rs.q50)+5,y2:Y(v),
        stroke:"var(--brand)","stroke-width":2}));});
  }
  [grid[0],grid[grid.length-1]].forEach((N,i)=>{
    const q=el("text",{x:X(N),y:H-MB+18,class:"tick","text-anchor":i?"end":"start"});
    q.textContent=fmt(N);s.appendChild(q);});
  const h=$("h12n"); if(h) h.textContent=g.name;
  const nb=$("n12");
  if(nb) nb.innerHTML='<ul class="ptlist">'+
    "<li><b>"+fmt(g.alloc[g.alloc.length-1])+" places</b> went to this group last round</li>"+
    "<li><b>= "+(g.share*100).toFixed(2)+"%</b> of everything issued that round &mdash; the share "+
      "carried forward</li>"+
    "<li><b>&times; "+B.meta.fr.toFixed(4)+"</b>, the single-leg part of a round, because the "+
      "share is measured on single-leg invitations</li>"+
    "<li><b>Line</b> &mdash; places at each round size; <b>shaded</b> &mdash; the sizes most likely to happen</li>"+
    "<li>Invitations are rationed at the four-digit unit group, so this is what your occupation "+
      "actually competes for</li></ul>";
  axisTitle(s,W,H,MB,"invitations in the round","places to your group");
}

/* ---------- chart 13: the joint surface, with both margins ---------- */
function chartJoint(g,gk,pts){
  const s=$("c13"); if(!s) return; clear(s);
  const W=560,H=336,ML=44,MR=92,MT=58,MB=52,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g||g.share<=0){noFc(s,W,H,"every cell here would be empty");return;}
  const sizes=[], dens=[];
  for(let k=0;k<B.rs.grid.length;k+=3){sizes.push(B.rs.grid[k]);dens.push(B.rs.dens[k]);}
  const scores=[]; for(let v=100;v>=B.floor;v-=5) scores.push(v);
  const cw=pw/sizes.length, chh=ph/scores.length;
  const P=(sc,N)=>pAt(g,sc,gk,N);
  /* the joint surface */
  scores.forEach((sc,r)=>{
    sizes.forEach((N,c)=>{
      const q=P(sc,N); if(q===null) return;
      const k=Math.max(0,Math.min(6,Math.floor(q*6.999)));
      const cell=el("rect",{x:ML+c*cw,y:MT+r*chh,width:Math.max(1,cw-1),height:Math.max(1,chh-1),
        rx:2,fill:"var(--r"+(k+1)+")"});
      s.appendChild(cell);
      hover(cell,"<b>"+Math.round(q*100)+"% chance</b><span>at "+sc+" points</span>"+
        "<span>if the round is "+fmt(N)+"</span>");
      if(sc===Math.round(pts/5)*5)
        s.appendChild(el("rect",{x:ML+c*cw,y:MT+r*chh,width:Math.max(1,cw-1),height:Math.max(1,chh-1),
          rx:2,fill:"none",stroke:"var(--ink)","stroke-width":1.2,"stroke-opacity":".5"}));
    });
    if(sc%10===0){const t=el("text",{x:ML-7,y:MT+r*chh+chh/2+3.5,class:"tick","text-anchor":"end"});
      t.textContent=sc;s.appendChild(t);}
  });
  /* top margin: how much each column counts */
  const dmax=Math.max(...dens), mh=28;
  let dd="M"+ML.toFixed(1)+","+(MT-6).toFixed(1);
  sizes.forEach((N,c)=>{dd+=" L"+(ML+c*cw+cw/2).toFixed(1)+","+(MT-6-mh*dens[c]/dmax).toFixed(1);});
  dd+=" L"+(ML+pw).toFixed(1)+","+(MT-6).toFixed(1)+" Z";
  s.appendChild(el("path",{d:dd,fill:"var(--brand)","fill-opacity":".3",stroke:"var(--brand)",
    "stroke-width":1.2}));
  const tl=el("text",{x:ML,y:MT-mh-12,class:"tick","text-anchor":"start",fill:"var(--brand)",
    "font-weight":"700"});
  tl.textContent="how likely each size is";s.appendChild(tl);
  /* right margin: round size averaged out - the headline, read across scores */
  const marg=scores.map(sc=>pMarginal(g,sc,gk));
  const mw=58;
  marg.forEach((q,r)=>{
    if(q===null) return;
    const bar=el("rect",{x:ML+pw+6,y:MT+r*chh+1,width:Math.max(1,mw*q),height:Math.max(1,chh-2),
      rx:2,fill:scores[r]===Math.round(pts/5)*5?"var(--brand)":"var(--deemph)",
      "fill-opacity":scores[r]===Math.round(pts/5)*5?1:.5});
    s.appendChild(bar);
    hover(bar,"<b>"+Math.round(q*100)+"%</b><span>at "+scores[r]+" points, averaged over round size</span>");
    if(scores[r]===Math.round(pts/5)*5){
      const t=el("text",{x:ML+pw+6+mw*q+5,y:MT+r*chh+chh/2+3.5,class:"vlab",
        "text-anchor":"start",fill:"var(--brand)"});
      t.textContent=Math.round(q*100)+"%";s.appendChild(t);}
  });
  const rl=el("text",{x:ML+pw+6,y:MT-20,class:"tick","text-anchor":"start",fill:"var(--muted)",
    "font-weight":"700"});
  rl.textContent="round size";s.appendChild(rl);
  const rl2=el("text",{x:ML+pw+6,y:MT-8,class:"tick","text-anchor":"start",fill:"var(--muted)"});
  rl2.textContent="averaged out";s.appendChild(rl2);
  /* the key sits top-right, clear of the axis labels it was landing on */
  const kw=Math.min(13,pw*0.30/7), kx=ML+pw-kw*7, ky=14;
  const kl=el("text",{x:kx-8,y:ky+8,class:"tick","text-anchor":"end",fill:"var(--muted)"});
  kl.textContent="chance";s.appendChild(kl);
  for(let k=0;k<7;k++)
    s.appendChild(el("rect",{x:kx+k*kw,y:ky,width:kw-1.5,height:9,rx:2,fill:"var(--r"+(k+1)+")"}));
  [["0%",kx,"start"],["100%",kx+kw*7,"end"]].forEach(([t,xx,a])=>{
    const q=el("text",{x:xx,y:ky+20,class:"tick","text-anchor":a});
    q.textContent=t;s.appendChild(q);});
  sizes.forEach((N,c)=>{if(c%3===0){
    const t=el("text",{x:ML+c*cw+cw/2,y:H-MB+16,class:"tick","text-anchor":"middle"});
    t.textContent=fmt(N);s.appendChild(t);}});
  const h=$("h13n"); if(h) h.textContent=g.name;
  axisTitle(s,W,H,MB,"invitations in the round","your points");
}

/* ---------- chart 14: why this group has no forecast ---------- */
function chartNoFc(o,g,gk,pts){
  const card=$("nofc"); if(!card) return;
  const none=!g||g.share<=0;
  card.hidden=!none;
  if(none===false) return;
  const s=$("c14"); if(!s) return; clear(s);
  const W=560,H=190,ML=40,MR=20,MT=26,MB=52,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g) {noFc(s,W,H,"this occupation has no unit-group record at all");return;}
  const al=g.alloc, mx=Math.max(1,...al), bw=pw/al.length;
  for(const t of [0,mx/2,mx]){
    s.appendChild(el("line",{x1:ML,y1:MT+ph*(1-t/mx),x2:ML+pw,y2:MT+ph*(1-t/mx),class:"gl"}));
    const q=el("text",{x:ML-7,y:MT+ph*(1-t/mx)+3.5,class:"tick","text-anchor":"end"});
    q.textContent=fmt(Math.round(t));s.appendChild(q);}
  al.forEach((v,i)=>{
    const x=ML+i*bw+bw*0.22, wd=bw*0.56, hh=ph*v/mx;
    const r=el("rect",{x:x,y:MT+ph-hh,width:wd,height:Math.max(v?2:0,hh),rx:4,
      fill:v>0?"var(--brand)":"var(--crit)","fill-opacity":v>0?0.85:0.25});
    s.appendChild(r);
    hover(r,"<b>"+fmt(v)+" invitation"+(v===1?"":"s")+"</b><span>"+RL[B.rounds[i]]+"</span>");
    const t=el("text",{x:x+wd/2,y:MT+ph-hh-6,class:"vlab","text-anchor":"middle",
      fill:v>0?"var(--ink)":"var(--crit)"});
    t.textContent=fmt(v);s.appendChild(t);
    const l=el("text",{x:x+wd/2,y:H-MB+16,class:"tick","text-anchor":"middle"});
    l.textContent=RL[B.rounds[i]];s.appendChild(l);});
  const waiting=Object.values(g.dist).reduce((a,b)=>a+b,0);
  const atOrAbove=Object.keys(g.dist).map(Number).filter(k=>k>=Math.round(pts/5)*5)
    .reduce((a,k)=>a+g.dist[k],0);
  const tier=B.tiers&&B.tiers.tier_of?B.tiers.tier_of[gk]:null;
  const rate=(tier&&B.tiers.by_tier[tier])?B.tiers.by_tier[tier].per_1000:null;
  say("t14","crit",
    '<span class="stat"><b>'+fmt(waiting)+'</b><i>waiting in this group</i></span>'+
    '<span class="stat"><b>'+fmt(atOrAbove)+'</b><i>at '+Math.round(pts/5)*5+' points or more</i></span>'+
    (tier?'<span class="stat verdict-crit"><b>Tier '+tier+'</b><i>'+
      (rate!==null?rate.toFixed(0)+" invited per 1,000":"lowest priority")+'</i></span>':'')+
    '<span class="stat verdict-crit"><b>'+Math.round(pZero(gk)*100)+'%</b><i>chance of nothing again</i></span>');
  const h=$("h14n"); if(h) h.textContent=g.name;
  axisTitle(s,W,H,MB,"","invitations to the group");
}
/* ---------- chart 1: cut-off by round ---------- */
function chartRounds(o,pts){
  const s=$("c1"); if(!s) return; clear(s);
  const W=560,H=230,ML=58,MR=46,MT=22,MB=54,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  const rs=o.rounds, vals=rs.map(r=>r.b).filter(v=>v!==null);
  const _fcs=(typeof CURG!=="undefined"&&B.groups[CURG])?B.groups[CURG].fc.filter(v=>v!==null):[];
  const _sp=_fcs.length?[Math.min(..._fcs)-B.unc.hi80,Math.max(..._fcs)-B.unc.lo80]:[];
  const lo=Math.min(60,pts-5,...vals,..._sp), hi=Math.max(pts+5,...vals,100,..._sp);
  /* rs.length history slots plus one projection slot */
  const NS=rs.length+1;
  const X=i=>ML+(NS===1?pw/2:pw*i/(NS-1));
  const Y=v=>MT+ph*(1-(v-lo)/(hi-lo));
  const maxN=Math.max(1,...rs.map(r=>r.n));
  const COL={good:"var(--good)",warn:"var(--warn)",crit:"var(--crit)",n:"var(--deemph)"};
  for(let v=Math.ceil(lo/10)*10;v<=hi;v+=10){
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    const q=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});q.textContent=v;s.appendChild(q);}
  if(pts>=lo&&pts<=hi){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const q=el("text",{x:ML+2,y:Y(pts)-6,class:"reft"});q.textContent="your "+pts;s.appendChild(q);}
  /* the connecting line stays neutral: the MARKS carry the meaning */
  let d="",started=false;
  rs.forEach((r,i)=>{if(r.b===null){started=false;return;}
    d+=(started?" L":"M")+X(i).toFixed(1)+","+Y(r.b).toFixed(1);started=true;});
  if(d) s.appendChild(el("path",{d:d,fill:"none",stroke:"var(--deemph)","stroke-width":1.5}));
  rs.forEach((r,i)=>{
    const q=el("text",{x:X(i),y:H-MB+16,class:"tick","text-anchor":"middle"});q.textContent=RL[r.r];s.appendChild(q);
    if(r.b===null){
      const z=el("text",{x:X(i),y:MT+ph/2,class:"tick","text-anchor":"middle"});z.textContent="—";s.appendChild(z);
      const c0=el("circle",{cx:X(i)-9,cy:H-MB+30,r:5,fill:"var(--deemph)"});s.appendChild(c0);
      const z0=el("text",{x:X(i)+1,y:H-MB+34,class:"tick","text-anchor":"start",fill:"var(--ink)"});
      z0.textContent="(0)";s.appendChild(z0);
      hover(c0,"<b>no invitations</b><span>"+RL[r.r]+"</span>");return;}
    const v=verdictFor(r,pts);
    /* radius carries how many this occupation got; colour carries your outcome */
    const rad=4+Math.sqrt(r.n/maxN)*6;
    const c=el("circle",{cx:X(i),cy:Y(r.b),r:rad,fill:COL[v.k],stroke:"var(--card)","stroke-width":2});
    s.appendChild(c);
    hover(c,"<b>"+r.b+" points</b><span>"+RL[r.r]+" &middot; "+fmt(r.n)+" invited in this occupation</span><span>"+
      (r.s==="C"?"everyone at that score got in":"rationed by date")+"</span><span>At "+pts+" pts: "+v.t+"</span>");
    const lab=el("text",{x:X(i),y:Y(r.b)-rad-6,class:"vlab","text-anchor":"middle"});
    lab.textContent=r.b;s.appendChild(lab);
    /* the same verdict repeated as a dot strip on the axis - readable without the y-scale */
    /* the dot and its count read as one unit, on one line */
    const c2=el("circle",{cx:X(i)-9,cy:H-MB+30,r:5,fill:COL[v.k]});s.appendChild(c2);
    const nl=el("text",{x:X(i)+1,y:H-MB+34,class:"tick","text-anchor":"start",fill:"var(--ink)"});
    nl.textContent=r.n?"("+fmt(r.n)+")":"";s.appendChild(nl);});
  /* ---- the round that has not happened yet ---- */
  const pj=X(rs.length), fcN=(typeof CURG!=="undefined"&&B.groups[CURG])?fcAt(B.groups[CURG]):null;
  s.appendChild(el("line",{x1:pj-0.5,y1:MT-6,x2:pj-0.5,y2:H-MB+6,stroke:"var(--line)",
    "stroke-width":1,"stroke-dasharray":"2 3"}));
  /* the fan: from the last cut-off actually observed, widening to the 80% interval
     on the next one. A forecast track, not a separate bar to decode. */
  const lastObs=[...rs].reverse().find(r=>r.b!==null);
  if(lastObs&&fcN!==null&&fcN!==undefined){
    const li=rs.lastIndexOf(lastObs), lx=X(li), ly=Y(lastObs.b);
    const hiY=Y(Math.min(hi,fcN-B.unc.lo80)), loY=Y(Math.max(lo,fcN-B.unc.hi80));
    s.appendChild(el("path",{d:"M"+lx.toFixed(1)+","+ly.toFixed(1)+" L"+pj.toFixed(1)+","+
      hiY.toFixed(1)+" L"+pj.toFixed(1)+","+loY.toFixed(1)+" Z",
      fill:"var(--brand)","fill-opacity":".12",stroke:"none"}));
    s.appendChild(el("line",{x1:lx,y1:ly,x2:pj,y2:Y(fcN),stroke:"var(--brand)",
      "stroke-width":1.5,"stroke-dasharray":"4 3"}));
  }
  if(fcN!==null&&fcN!==undefined){
    /* the forecast is a distribution, not a point: every held-out error, applied */
    const R=B.unc.residuals, cnt={};
    R.forEach(e=>{const v=fcN-e; cnt[v]=(cnt[v]||0)+1;});
    const vals=Object.keys(cnt).map(Number).sort((a,b)=>a-b);
    const cmax=Math.max(...vals.map(v=>cnt[v])), halfW=Math.min(26,(pw/NS)*0.42);
    vals.forEach(v=>{
      if(v<lo||v>hi) return;
      const w=halfW*cnt[v]/cmax, y=Y(v), bh=Math.max(3,ph/((hi-lo)/5)-2);
      const good=v<=pts;
      const r=el("rect",{x:pj-w,y:y-bh/2,width:w*2,height:bh,rx:2,
        fill:good?"var(--good)":"var(--crit)","fill-opacity":good?".55":".4"});
      s.appendChild(r);
      hover(r,"<b>cut-off "+v+"</b><span>"+Math.round(100*cnt[v]/R.length)+
        "% of held-out rounds landed here</span><span>at "+pts+" pts: "+
        (good?"you are in":"not reached")+"</span>");});
    const cd=el("circle",{cx:pj,cy:Y(fcN),r:4.5,fill:"var(--ink)",stroke:"var(--card)","stroke-width":2});
    s.appendChild(cd);
    hover(cd,"<b>forecast "+fcN+" points</b><span>central estimate for the next round</span>");
  } else {
    const q=el("text",{x:pj,y:MT+ph/2,class:"tick","text-anchor":"middle"});
    q.textContent="no forecast";s.appendChild(q);}
  const pl=el("text",{x:pj,y:H-MB+16,class:"tick","text-anchor":"middle","font-weight":"700"});
  pl.textContent="next";s.appendChild(pl);
  const yl=el("text",{x:ML-7,y:MT-8,class:"tick","text-anchor":"end"});yl.textContent="pts";s.appendChild(yl);
  const nl2=el("text",{x:2,y:H-MB+34,class:"tick","text-anchor":"start",fill:"var(--ink)",
    "font-weight":"700"});nl2.textContent="invites";s.appendChild(nl2);
  
}
/* ---------- chart 4: the mechanism itself - cumulative queue vs allocation ---------- */
function chartQueue(g,pts){
  const s=$("c4"); if(!s) return; clear(s);
  const W=560,H=220,ML=46,MR=60,MT=16,MB=42,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g){const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No unit-group data.";s.appendChild(t);return;}
  const keys=Object.keys(g.dist).map(Number).sort((a,b)=>b-a).filter(k=>k>=B.floor);
  if(!keys.length){const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No EOIs at or above the 65-point floor.";s.appendChild(t);return;}
  let cum=0; const step=keys.map(k=>{cum+=g.dist[k];return {sc:k,cum:cum};});
  const alloc=g.alloc[g.alloc.length-1];
  const fc=fcAt(g);
  const yMax=Math.max(cum,alloc)*1.08;
  const X=i=>ML+pw*i/Math.max(1,keys.length-1), Y=v=>MT+ph*(1-v/yMax);
  for(let i=0;i<=4;i++){const v=yMax*i/4,y=MT+ph*(1-i/4);
    s.appendChild(el("line",{x1:ML,y1:y,x2:W-MR,y2:y,class:"gl"}));
    const q=el("text",{x:ML-7,y:y+3.5,class:"tick","text-anchor":"end"});q.textContent=Math.round(v);s.appendChild(q);}
  /* step curve: cumulative EOIs at or above each score */
  let d="";
  step.forEach((p,i)=>{const x=X(i),y=Y(p.cum);
    if(i===0){d+="M"+ML.toFixed(1)+","+Y(0).toFixed(1)+" L"+ML.toFixed(1)+","+y.toFixed(1);}
    else {d+=" L"+x.toFixed(1)+","+Y(step[i-1].cum).toFixed(1)+" L"+x.toFixed(1)+","+y.toFixed(1);}});
  d+=" L"+X(keys.length-1).toFixed(1)+","+Y(step[step.length-1].cum).toFixed(1);
  /* the people ahead of you: the same step curve, closed to the baseline and filled,
     so the quantity the card is about is an area rather than a number to look up */
  const myS=Math.round(pts/5)*5, myI=keys.indexOf(myS);
  const lastI = myI>=0 ? myI : (myS>keys[0] ? -1 : keys.length-1);
  if(lastI>=0){
    let ad="M"+ML.toFixed(1)+","+Y(0).toFixed(1);
    for(let i=0;i<=lastI;i++){
      const x=X(i);
      if(i===0) ad+=" L"+ML.toFixed(1)+","+Y(step[0].cum).toFixed(1);
      else ad+=" L"+x.toFixed(1)+","+Y(step[i-1].cum).toFixed(1)+" L"+x.toFixed(1)+","+Y(step[i].cum).toFixed(1);
    }
    ad+=" L"+X(lastI).toFixed(1)+","+Y(0).toFixed(1)+" Z";
    const ar=el("path",{d:ad,fill:"var(--crit)","fill-opacity":".13",stroke:"none"});
    s.appendChild(ar);
    hover(ar,"<b>"+fmt(step[lastI].cum)+" ahead of you</b><span>everyone scoring "+myS+
      " or more in this group</span>");
  }
  s.appendChild(el("path",{d:d,class:"ln"}));
  /* allocation reference: where the last round stopped */
  const ay=Y(alloc);
  s.appendChild(el("line",{x1:ML,y1:ay,x2:W-MR,y2:ay,stroke:"var(--good)","stroke-width":1.5,"stroke-dasharray":"5 4"}));
  const at=el("text",{x:W-MR+4,y:ay+3.5,fill:"var(--good)","font-size":"9.5","font-weight":"650"});
  at.textContent=fmt(alloc)+" invited";s.appendChild(at);
  /* the reader's position */
  const my=Math.round(pts/5)*5, mi=keys.indexOf(my);
  const aboveAll = my>keys[0];
  if(mi>=0 || aboveAll){
    const idx = aboveAll?0:mi;
    const ahead = aboveAll?0:step[mi].cum;
    const mx = aboveAll?ML:X(mi);
    s.appendChild(el("line",{x1:mx,y1:MT,x2:mx,y2:MT+ph,class:"refl"}));
    const c=el("circle",{cx:mx,cy:Y(ahead),r:6,fill:"var(--crit)",stroke:"var(--card)","stroke-width":2});
    s.appendChild(c);
    hover(c,"<b>"+fmt(ahead)+" ahead of you</b><span>everyone at "+my+" points or above</span><span>"+
      (alloc>=ahead?"last round reached past you":"last round stopped short of you")+"</span>");
    const lt=el("text",{x:mx,y:Math.max(MT+11,Y(ahead)-12),class:"reft","text-anchor":aboveAll?"start":"middle"});
    lt.textContent=aboveAll?"nobody ahead":fmt(ahead)+" ahead";s.appendChild(lt);}
  keys.forEach((k,i)=>{
    if(keys.length<=12||i%2===0){
      const q=el("text",{x:X(i),y:H-MB+15,class:"tick","text-anchor":"middle"});q.textContent=k;s.appendChild(q);}
    const hit=el("rect",{x:X(i)-8,y:MT,width:16,height:ph,class:"hit"});
    hover(hit,"<b>"+fmt(step[i].cum)+"</b><span>EOIs at "+k+" points or above</span>");s.appendChild(hit);});
  axisTitle(s,W,H,MB,"points, highest first","people ahead (cumulative)");
}
/* ---------- chart 5: forecast matrix (score x round size) ---------- */
const SCORES=[120,115,110,105,100,95,90,85,80,75,70,65];
/* ---------- chart 6: annotated landscape heatmap (group x round) ---------- */
/* Red-earth ramp, read from CSS so it swaps with the theme. Both variants were validated
   as ordinal ramps (monotone lightness, >=0.06 step gaps, light end clears 2:1 on its surface). */
function rampSteps(){
  const cs=getComputedStyle(document.documentElement);
  return [1,2,3,4,5,6,7].map(i=>cs.getPropertyValue("--r"+i).trim()).filter(Boolean);
}
let RAMP=rampSteps();
function rampIdx(v){ return Math.max(0,Math.min(RAMP.length-1,Math.round((v-65)/6))); }
function rampFor(v){ return (v===null||v===undefined)?"var(--deemph)":(RAMP[rampIdx(v)]||RAMP[0]); }
function inkOn(v){ return (v===null||v===undefined)?"var(--muted)":(rampIdx(v)>=3?"#ffffff":"#0b0b0b"); }
let HMSORT="cut";
function chartLandscape(selG,pts){
  const s=$("c6"); if(!s) return; RAMP=rampSteps(); clear(s);
  const keys=Object.keys(B.groups);
  const alloc=g=>{const f=B.groups[g].alloc;return f[f.length-1];};
  const cmp={
    cut:(a,b)=>{const av=lastCut(a),bv=lastCut(b);
      if(av===null&&bv===null)return alloc(b)-alloc(a);
      if(av===null)return 1; if(bv===null)return -1; return av-bv||alloc(b)-alloc(a);},
    alloc:(a,b)=>alloc(b)-alloc(a),
    name:(a,b)=>B.groups[a].name.localeCompare(B.groups[b].name)
  }[HMSORT];
  keys.sort(cmp);
  const ML=190,MR=12,MT=26,rh=19,W=520,H=MT+keys.length*rh+8;
  s.setAttribute("viewBox","0 0 "+W+" "+H);
  const cw=(W-ML-MR)/B.rounds.length;
  B.rounds.forEach((r,i)=>{const q=el("text",{x:ML+cw*(i+.5),y:MT-10,class:"tick","text-anchor":"middle",
    "font-weight":"600"});q.textContent=RL[r];s.appendChild(q);});
  
  keys.forEach((gk,ri)=>{
    const G=B.groups[gk], y=MT+ri*rh, on=(gk===selG);
    const nm=G.name.replace(/^\d+\s/,"");
    const lt=el("text",{x:ML-8,y:y+rh/2,class:"rowlab"+(on?" on":""),"text-anchor":"end"});
    lt.textContent=gk+" "+(nm.length>26?nm.slice(0,25)+"…":nm);s.appendChild(lt);
    B.rounds.forEach((r,ci)=>{
      const v=cutOf(gk,r);
      const rect=el("rect",{x:ML+cw*ci,y:y+1.5,width:cw,height:rh-3,rx:2,fill:rampFor(v),class:"cell"});
      s.appendChild(rect);
      /* value annotation - identity never rests on colour alone */
      const vt=el("text",{x:ML+cw*(ci+.5),y:y+rh/2+3.5,"text-anchor":"middle","font-size":"10",
        "font-weight":"650",fill:inkOn(v),"pointer-events":"none"});
      vt.textContent=(v===null?"·":v);s.appendChild(vt);
      hover(rect,"<b>"+(v===null?"no invitations":v+" points")+"</b><span>"+G.name+"</span><span>"+
        RL[r]+" &middot; "+fmt(G.alloc[B.rounds.indexOf(r)])+" invited</span>");
      rect.addEventListener("click",()=>{
        const first=OCCS.find(o=>B.occ[o].g===gk);
        if(first){S.occ=first;put("occ","value",first);render();window.scrollTo({top:0,behavior:"smooth"});}});});
    if(on)s.appendChild(el("rect",{x:ML,y:y+1.5,width:W-ML-MR,height:rh-3,rx:2,fill:"none",
      stroke:"var(--ink)","stroke-width":2,"pointer-events":"none"}));});
}
function cutOf(gk,round){
  let best=null;
  for(const o of OCCS){const oc=B.occ[o]; if(oc.g!==gk) continue;
    const r=oc.rounds.find(x=>x.r===round); if(r&&r.b!==null) best=(best===null?r.b:Math.min(best,r.b));}
  return best;
}
function lastCut(gk){ return cutOf(gk,B.rounds[B.rounds.length-1]); }
/* ---------- chart 7: competition ratio vs cut-off ---------- */
function chartScatter(selG,pts){
  const s=$("c7"); if(!s) return; clear(s);
  const W=560,H=312,ML=42,MR=18,MT=18,MB=62,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  const P=[];
  for(const gk in B.groups){
    const G=B.groups[gk], pool=Object.values(G.dist).reduce((a,b)=>a+b,0);
    const al=G.alloc[G.alloc.length-1], c=lastCut(gk);
    if(!pool||!al||c===null) continue;
    P.push({gk,name:G.name,pool,al,cut:c,ratio:pool/al});}
  if(!P.length){const q=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    q.textContent="Not enough data.";s.appendChild(q);return;}
  const L=v=>Math.log10(v);
  const x0=Math.min(...P.map(p=>L(p.ratio))), x1=Math.max(...P.map(p=>L(p.ratio)));
  const y0=Math.min(60,...P.map(p=>p.cut)), y1=Math.max(100,...P.map(p=>p.cut));
  const X=v=>ML+pw*(L(v)-x0)/(x1-x0||1), Y=v=>MT+ph*(1-(v-y0)/(y1-y0));
  for(let v=Math.ceil(y0/10)*10;v<=y1;v+=10){
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    const q=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});q.textContent=v;s.appendChild(q);}
  [1,2,3,5,10,20,50,100].filter(v=>L(v)>=x0-0.02&&L(v)<=x1+0.02).forEach(v=>{
    const q=el("text",{x:X(v),y:H-MB+15,class:"tick","text-anchor":"middle"});q.textContent=v;s.appendChild(q);});
  /* least-squares trend: the relationship is the point of this chart */
  const xs=P.map(p=>L(p.ratio)), ys=P.map(p=>p.cut), n=P.length;
  const mx=xs.reduce((a,b)=>a+b,0)/n, my=ys.reduce((a,b)=>a+b,0)/n;
  const sl=xs.reduce((a,x,i)=>a+(x-mx)*(ys[i]-my),0)/xs.reduce((a,x)=>a+(x-mx)**2,0);
  const ic=my-sl*mx;
  const fit=x=>sl*x+ic;
  s.appendChild(el("line",{x1:ML,y1:Y(Math.max(y0,Math.min(y1,fit(x0)))),
    x2:W-MR,y2:Y(Math.max(y0,Math.min(y1,fit(x1)))),stroke:"var(--muted)","stroke-width":1.5,"stroke-dasharray":"6 4"}));
  const ft=el("text",{x:W-MR-2,y:Y(Math.max(y0,Math.min(y1,fit(x1))))-7,class:"tick","text-anchor":"end"});
  ft.textContent="the trend";s.appendChild(ft);
  if(pts>=y0&&pts<=y1){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const q=el("text",{x:ML+3,y:Y(pts)-6,class:"reft"});q.textContent="your "+pts+" points";s.appendChild(q);}
  const maxP=Math.max(...P.map(p=>p.pool));
  P.sort((a,b)=>b.pool-a.pool).forEach(p=>{
    const r=Math.max(3.5,Math.min(13,Math.sqrt(p.pool/maxP)*15)), on=p.gk===selG;
    const c=el("circle",{cx:X(p.ratio),cy:Y(p.cut),r:r,class:"pt"+(on?" on":""),
      fill:"var(--series)","fill-opacity":on?1:.5});
    s.appendChild(c);
    hover(c,"<b>"+p.ratio.toFixed(1)+" people per invitation</b><span>"+p.name+
      "</span><span>"+fmt(p.pool)+" waiting &middot; "+fmt(p.al)+" invited &middot; cut-off "+p.cut+"</span>");
    c.addEventListener("click",()=>{const f=OCCS.find(o=>B.occ[o].g===p.gk);
      if(f){S.occ=f;put("occ","value",f);render();window.scrollTo({top:0,behavior:"smooth"});}});});
  axisTitle(s,W,H,MB,"people per invitation","lowest score invited");
  
  const nt=el("text",{x:(ML+W-MR)/2,y:H-MB+50,class:"tick","text-anchor":"middle","font-style":"italic"});
  nt.textContent="right = more competition";s.appendChild(nt);
}





/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */







/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */


/* ---------- every score band ---------- */
function bandTable(o,g,pts){
  if(!document.querySelector("#bt tbody")) return;
  const tb=document.querySelector("#bt tbody"); if(!tb||!g) return; tb.innerHTML="";
  const cen=B.policy?B.policy.per_round["3"]:10000, fc=cutoffAt(g,cen);
  const my=Math.round(pts/5)*5;
  const keys=[...new Set([...Object.keys(g.dist).map(Number),my])].filter(k=>k>=B.floor).sort((a,b)=>b-a);
  keys.forEach(k=>{
    const above=Object.keys(g.dist).map(Number).filter(x=>x>k).reduce((a,x)=>a+g.dist[x],0);
    const saveP=S.pts; S.pts=k;
    const P=pMarginal(g,k,o.g); S.pts=saveP;
    const reaches = fc===null?null:(k>fc?"yes":k===fc?"on the boundary":"no");
    const tr=document.createElement("tr"); if(k===my)tr.className="hl";
    const cells=[k+(k===my?" (you)":""),fmt(o.dist[k]||0),fmt(g.dist[k]||0),fmt(above),reaches||"—",""];
    cells.forEach((c,i)=>{const td=document.createElement("td");
      if(i===5){const sp=document.createElement("span");
        sp.className="pill "+(P===null?"n":P>=.8?"good":P>=.5?"warn":"crit");
        sp.textContent=P===null?"—":Math.round(P*100)+"%";td.appendChild(sp);}
      else td.textContent=c;
      tr.appendChild(td);});
    tb.appendChild(tr);});
  const hb=$("hbn"); if(hb) hb.textContent="averaged over round size";
}
/* ---------- exact queue table ---------- */
function queueTable(o,g,pts){
  const tb=document.querySelector("#qt tbody");if(!tb)return;tb.innerHTML="";
  const my=Math.round(pts/5)*5;
  const keys=new Set([...Object.keys(o.dist).map(Number),...(g?Object.keys(g.dist).map(Number):[])]);
  const list=[...keys].filter(k=>k>=my).sort((a,b)=>b-a);
  let run=0;
  list.forEach(k=>{
    const oc=o.dist[k]||0, gc=(g&&g.dist[k])||0; run+=gc;
    const tr=document.createElement("tr"); const mine=(k===my); if(mine)tr.className="hl";
    [k+(mine?" (you)":""),fmt(oc),fmt(gc),fmt(run),""].forEach((c,i)=>{
      const td=document.createElement("td");
      if(i===4){const sp=document.createElement("span");sp.className="pill "+(k>my?"crit":"warn");
        sp.textContent=k>my?"ahead on points":"ahead on date";td.appendChild(sp);}
      else td.textContent=c;
      tr.appendChild(td);});
    tb.appendChild(tr);});
  const tr=document.createElement("tr");
  const td=document.createElement("td");td.colSpan=3;td.innerHTML="<b>Total ahead of you in the unit group</b>";
  const td2=document.createElement("td");td2.innerHTML="<b>"+fmt(run)+"</b>";
  const td3=document.createElement("td");
  const al=g?g.alloc[g.alloc.length-1]:0;
  const sp=document.createElement("span");sp.className="pill "+(al>=run?"good":"crit");
  sp.textContent=al>=run?"last round reached "+fmt(al):"last round reached only "+fmt(al);
  td3.appendChild(sp);
  tr.appendChild(td);tr.appendChild(td2);tr.appendChild(td3);tb.appendChild(tr);
  const hh=$("h8n"); if(hh) hh.textContent=fmt(run)+" ahead in "+o.g;
}
/* ---------- policy table ---------- */
function policyTable(){
  if(!document.querySelector("#pt tbody")) return;
  const P=B.policy; if(!P) return;
  const tb=document.querySelector("#pt tbody"); if(!tb) return;
  const rows=[["Skilled Independent (189)",P.places["2025-26"],P.places["2026-27"]],
    ["State/Territory Nominated (190)",P.nominated["2025-26"],P.nominated["2026-27"]],
    ["Regional (491)",P.regional_cut["2025-26"],P.regional_cut["2026-27"]],
    ["Employer Sponsored",P.employer["2025-26"],P.employer["2026-27"]]];
  tb.innerHTML="";
  rows.forEach(([lab,a,b])=>{
    const pc=(b/a-1)*100, tr=document.createElement("tr");
    [lab,fmt(a),fmt(b),""].forEach((c,i)=>{const td=document.createElement("td");
      if(i===3){const sp=document.createElement("span");
        sp.className="pill "+(pc>1?"good":pc<-1?"crit":"n");
        sp.textContent=(pc>0?"+":"")+pc.toFixed(0)+"%";td.appendChild(sp);}
      else td.textContent=c;tr.appendChild(td);});
    tb.appendChild(tr);});
  const nt=document.querySelector('[data-role="pnote"]'); if(!nt) return;
  nt.innerHTML="189 grew <b>+"+((P.places["2026-27"]/P.places["2025-26"]-1)*100).toFixed(0)+
    "%</b>. At <b>"+P.ratio.toFixed(2)+"</b> invitations per place, "+fmt(P.places["2026-27"])+
    " places &rarr; ~<b>"+fmt(P.projected_invitations)+"</b> invitations, ~<b>"+fmt(P.per_round["3"])+
    "</b> per round over three rounds. Regional fell 57% &mdash; the likeliest route to a bigger 189 pool, "+
    "visible only in later snapshots.";
}




function chartProb(g,pts){
  const s=$("c8"); if(!s) return; clear(s);
  const W=560,H=280,ML=44,MR=66,MT=40,MB=46,pw=W-ML-MR,ph=H-MT-MB;
  frame(s,W,H);
  if(!g||g.share<=0){const q=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    q.textContent="No invitations last round, so there is nothing to forecast at any size.";s.appendChild(q);return;}
  const S0=2000,S1=20000;
  const X=v=>ML+pw*(v-S0)/(S1-S0), Y=p=>MT+ph*(1-p);
  for(let i=0;i<=4;i++){const y=MT+ph*(1-i/4);
    s.appendChild(el("line",{x1:ML,y1:y,x2:W-MR,y2:y,class:"gl"}));
    const q=el("text",{x:ML-7,y:y+3.5,class:"tick","text-anchor":"end"});q.textContent=(i*25)+"%";s.appendChild(q);}
  const curve=sc=>{const a=[];for(let v=S0;v<=S1;v+=200){const p=pAt(g,sc,CURG,v);
    if(p!==null)a.push([v,p]);}return a;};
  const path=a=>{let d="";a.forEach((q,i)=>{d+=(i?" L":"M")+X(q[0]).toFixed(1)+","+Y(q[1]).toFixed(1);});return d;};
  /* the curve is read off n held-out residuals, so it carries a sampling error of its
     own: +/- 1 standard error of a proportion estimated from that many observations */
  {
    const n=B.unc.residuals.length, a0=curve(pts);
    if(a0.length>1){
      const se=q=>Math.sqrt(Math.max(1e-6,q*(1-q))/n);
      let up="",dn="";
      a0.forEach(([v,q])=>{up+=(up?"L":"M")+X(v).toFixed(1)+","+Y(Math.min(1,q+se(q))).toFixed(1)+" ";});
      for(let i=a0.length-1;i>=0;i--){const [v,q]=a0[i];
        dn+="L"+X(v).toFixed(1)+","+Y(Math.max(0,q-se(q))).toFixed(1)+" ";}
      s.appendChild(el("path",{d:up+dn+"Z",fill:"var(--series)","fill-opacity":".16",stroke:"none"}));
    }
  }
  {
    const a=curve(pts);
    if(a.length>1) s.appendChild(el("path",{d:path(a),fill:"none",stroke:"var(--series)",
      "stroke-width":2.5,"stroke-linejoin":"round","stroke-linecap":"round"}));
    if(a.length){
      const t=el("text",{x:W-MR+5,y:Y(a[a.length-1][1])+3.5,fill:"var(--series)",
        "font-size":"9.5","font-weight":"700","text-anchor":"start"});
      t.textContent="you at "+pts;s.appendChild(t);}
  }
  /* how likely each round size is, as a ribbon under the curve - same panel, no extra chart */
  if(B.rs){
    const dmax=Math.max(...B.rs.dens), hband=ph*0.22;
    let dd="M"+X(B.rs.grid[0]).toFixed(1)+","+(MT+ph).toFixed(1);
    B.rs.grid.forEach((sz,i)=>{if(sz<S0||sz>S1)return;
      dd+=" L"+X(sz).toFixed(1)+","+(MT+ph-hband*B.rs.dens[i]/dmax).toFixed(1);});
    dd+=" L"+X(Math.min(S1,B.rs.grid[B.rs.grid.length-1])).toFixed(1)+","+(MT+ph).toFixed(1)+" Z";
    s.appendChild(el("path",{d:dd,fill:"var(--brand)","fill-opacity":".16",stroke:"var(--brand)",
      "stroke-width":1,"stroke-opacity":".45"}));
  }
  /* the headline, on the same axes: it is the curve averaged against the ribbon below,
     which is the only honest way to show why one number is not the other */
  {
    const PM=pMarginal(g,pts,CURG);
    if(PM!==null){
      const my=Y(PM);
      s.appendChild(el("line",{x1:ML,y1:my,x2:W-MR,y2:my,stroke:"var(--brand)",
        "stroke-width":2,"stroke-dasharray":"6 4"}));
      const t=el("text",{x:W-MR-2,y:my-6,class:"tick",fill:"var(--brand)","font-weight":"700",
        "text-anchor":"end"});
      t.textContent=Math.round(PM*100)+"%";s.appendChild(t);}
  }
  /* where the curve crosses even odds - the one number the text box carried */
  {
    let prev=null, cross=null;
    for(let v=S0;v<=S1;v+=100){const q=pAt(g,pts,CURG,v);
      if(q===null){prev=null;continue;}
      if(prev!==null&&prev<0.5&&q>=0.5){cross=v;break;}
      prev=q;}
    if(cross!==null){
      const cx=X(cross), cy=Y(0.5);
      s.appendChild(el("line",{x1:ML,y1:cy,x2:W-MR,y2:cy,stroke:"var(--muted)",
        "stroke-width":1,"stroke-dasharray":"2 4"}));
      s.appendChild(el("circle",{cx:cx,cy:cy,r:4.5,fill:"var(--card)",
        stroke:"var(--series)","stroke-width":2.5}));
      const t=el("text",{x:cx+8,y:cy+14,class:"tick",fill:"var(--series)","font-weight":"700",
        "text-anchor":"start"});
      t.textContent=fmt(cross);s.appendChild(t);}
  }
  [2000,5000,8000,11000,14000,17000,20000].forEach(v=>{
    const q=el("text",{x:X(v),y:H-MB+15,class:"tick","text-anchor":"middle"});
    q.textContent=(v/1000)+"k";s.appendChild(q);});
  /* hover anywhere along the curve */
  const hoverPts=curve(pts);
  for(let i=0;i<hoverPts.length;i+=3){
    const [v,p]=hoverPts[i], c=cutoffAt(g,v);
    const hit=el("rect",{x:X(v)-4,y:MT,width:8,height:ph,class:"hit"});
    hover(hit,"<b>"+Math.round(p*100)+"% chance</b><span>if the round invites "+fmt(v)+
      "</span><span>cut-off would be about "+c+" points</span>");s.appendChild(hit);}
  legend(s,ML,MT-24,[
    ["line","var(--series)","your chance"],
    ["band","var(--series)","±1 s.e. from "+B.unc.residuals.length+" held-out rounds"],
    ["dash","var(--brand)","headline, averaged over size"]]);
  legend(s,ML,MT-10,[
    ["dot","var(--series)","even odds"],
    ["band","var(--brand)","how likely each round size is"]]);
  axisTitle(s,W,H,MB,"invitations in the round","chance IF the round is this size");
  
}
/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */
function rangeBand(g,pts){
  if(!g||g.share<=0||!B.rs) return null;
  const a=pAt(g,pts,CURG,B.rs.q10), b=pAt(g,pts,CURG,B.rs.q90);
  if(a===null||b===null) return null;
  return [Math.min(a,b),Math.max(a,b)];
}
function rangeText(g,pts){
  const r=rangeBand(g,pts); if(!r) return "—";
  const lo=Math.round(r[0]*100), hi=Math.round(r[1]*100);
  return lo===hi ? lo+"%" : lo+"–"+hi+"%";
}
function say(id,kind,html){const e=$(id);if(!e)return;e.className="takeaway"+(kind?" "+kind:"");e.innerHTML=html;}
function takeaways(o,g,pts,size){
  /* everything else this built was consumed by boxes the charts replaced; the
     competitiveness line is the one figure no chart on this page carries */
  const al=g?g.alloc[g.alloc.length-1]:0;
  const gp=g?Object.values(g.dist).reduce((a,b)=>a+b,0):0;
  if(g&&al>0){
    const ratio=gp/al;
    const all=Object.keys(B.groups).map(k=>{const G=B.groups[k],p=Object.values(G.dist).reduce((a,b)=>a+b,0),
      a2=G.alloc[G.alloc.length-1];return (p&&a2)?p/a2:null;}).filter(v=>v!==null).sort((a,b)=>a-b);
    const pct=Math.round(100*all.filter(v=>v<ratio).length/all.length);
    say("t7", pct<=33?"good":pct<=66?"warn":"crit",
      "<b>"+ratio.toFixed(1)+" people per invitation</b> in your group &mdash; "+
      (pct<=33?"<b>less competitive than most</b>":pct<=66?"<b>about average</b>":"<b>more competitive than most</b>")+
      " ("+pct+"th percentile).");}
  else say("t7","","No invitations to this group last round.");
}

/* ---------- how the cut-off moves between rounds ---------- */
/* ---------- the occupations switched off, and the one that was not ---------- */
function switchTable(){
  if(!document.querySelector("#swt tbody")) return;
  const tb=document.querySelector("#swt tbody"); if(!tb||!B.sw) return; tb.innerHTML="";
  const row=(o,cls)=>{
    const tr=document.createElement("tr"); if(cls)tr.className=cls;
    const td=document.createElement("td");td.textContent=o.name;tr.appendChild(td);
    const p=document.createElement("td");p.textContent=fmt(o.pool);tr.appendChild(p);
    (o.hist||[]).forEach(n=>{const c=document.createElement("td");
      const sp=document.createElement("span");sp.className="pill "+(n>0?"good":"crit");
      sp.textContent=n>0?fmt(n):"0";c.appendChild(sp);tr.appendChild(c);});
    tb.appendChild(tr);};
  B.sw.switched_off.slice(0,8).forEach(o=>row(o));
  const keep=B.sw.still_invited_large&&B.sw.still_invited_large[0];
  if(keep){
    const tr=document.createElement("tr");
    const td=document.createElement("td");td.colSpan=7;
    td.innerHTML="<b>Contrast &mdash; "+keep.name+"</b> holds "+fmt(keep.pool)+
      " people and kept being invited throughout, so this is not about pool size.";
    td.style.cssText="padding-top:10px;color:var(--body)";
    tr.appendChild(td);tb.appendChild(tr);}
  const hs=$("hswn"); if(hs) hs.textContent=B.sw.switched_off.length+" groups, "+fmt(B.sw.people_affected)+" people";
  say("tsw","crit",
    "<b>60% of the pool</b> gets nothing. "+B.sw.switched_off.length+" groups, "+fmt(B.sw.people_affected)+
    " people, cut off since 2025&ndash;26 &mdash; matching an FOI'd Home Affairs tier model "+
    "(Tier 4: <b>"+(B.tiers?B.tiers.by_tier[4].per_1000.toFixed(1):"1.3")+"</b> invites per 1,000; Tier 2: <b>"+
    (B.tiers?B.tiers.by_tier[2].per_1000.toFixed(0):"117")+"</b>).");
}
const TIERNAMES={1:"Tier 1 — highest priority (health)",2:"Tier 2 — government priority (teaching, social work)",3:"Tier 3 — broad skills mix (engineers, trades, sciences)",4:"Tier 4 — oversupplied (accounting, ICT, chefs)"};
function tierLabel(gk){
  const t=B.tiers&&B.tiers.tier_of&&B.tiers.tier_of[gk];
  if(!t) return "—";
  const per=B.tiers.by_tier&&B.tiers.by_tier[t];
  return "Tier "+t+(per?" · "+per.per_1000.toFixed(0)+" per 1,000 waiting":"");
}
/* ---------- what separates a high-scoring profile ---------- */
function levers(){
  if(!$("lev")) return;
  const box=$("lev"); if(!box) return;
  const L=[["Max English (20 pts)",83.6,19.3],["Partner skills (10 pts)",84.4,63.3],["Australian study",82.0,62.7]];
  box.innerHTML="";
  L.forEach(([lab,hi,lo])=>{
    const d=document.createElement("div");d.className="lrow";
    d.innerHTML='<span class="llab">'+lab+'</span>'+
      '<span class="lbar"><i style="width:'+hi+'%"></i></span><span class="lval">'+hi.toFixed(0)+'%</span>'+
      '<span class="lbar dim"><i style="width:'+lo+'%"></i></span><span class="lval dim">'+lo.toFixed(0)+'%</span>';
    box.appendChild(d);});
  const c=document.createElement("p");c.className="note";c.hidden=false;
  c.style.cssText="margin:6px 0 0;font-size:11px";
  c.innerHTML="Share holding each component, <b>at 85+</b> vs <b>65&ndash;84</b>. English is the dividing line. "+
    "The pool is also strengthening: share at 85+ is up <b>"+
    (B.drift?((B.drift.share85_end-B.drift.share85_start)*100).toFixed(1):"5.6")+" points</b> over 24 months.";
  box.appendChild(c);
}
/* ---------- render ---------- */
function render(){
  const o=B.occ[S.occ]; if(!o) return;
  CURG=o.g;
  const g=B.groups[o.g]; const pts=S.pts; const size=SZ();
  const last=o.rounds[o.rounds.length-1];
  const fc=g?fcAt(g):null;
  const v=fcVerdict(fc,pts);
  const P=pMarginal(g,pts,o.g), bb=pBand(fc);
  chartProb(g,pts);
  chartForecast(g,pts);fcTable(g,pts);chartWaterfall(g,o.g,pts);
  chartComp(g,o.g,pts);chartDoe(o.g,pts);chartTierRate(g,o.g);
  chartRoundSize();chartGroupShare(g,o.g);chartJoint(g,o.g,pts);
  chartNoFc(o,g,o.g,pts);
  const band = P===null?null:(P>=.8?"good":P>=.6?"good":P>=.4?"warn":"crit");
  if($("flag")){$("flag").className="vflag "+(band||"crit");}
  if($("flag"))$("flag").textContent = P===null ? "✕ No forecast"
    : P>=.8 ? "✓ Likely invited"
    : P>=.6 ? "✓ Favourable, not certain"
    : P>=.4 ? "! Could go either way"
    : "✕ Unlikely at this score";
  if($("hero"))$("hero").textContent = P===null ? "—" : Math.round(P*100)+"%";
  if($("vsub"))$("vsub").innerHTML = P===null
    ? "This occupation received no invitations in the most recent round, so there is no allocation share to forecast from. The round-by-round record below still applies."
    : "at <b>"+pts+" points</b> in <b>"+o.g+"</b>, averaged over likely round sizes "+
      "&mdash; if a round is held at all.";
  const ge=g?Object.keys(g.dist).map(Number).filter(k=>k>=pts).reduce((a,k)=>a+g.dist[k],0):0;
  const al=g?g.alloc[g.alloc.length-1]:0;
  const ratio=ge>0?al/ge:0;
  const vside=$("vside"); if(vside) vside.innerHTML="";
  /* "Your chance vs round size" already plots the chance and the size range,
     and "Who is ahead" plots the queue - only what no chart shows survives here */
  const rows=[["Forecast cut-off",fc===null?"—":fc+" pts (80% "+bb[0]+"–"+bb[1]+")"],
    ["Risk of no invitations",Math.round(pZero(o.g)*100)+"%"],
    ["Priority tier",tierLabel(o.g)]];
  rows.forEach(([k,val])=>{const dl=document.createElement("dl");dl.className="kv";
    const dt=document.createElement("dt");dt.textContent=k;const dd=document.createElement("dd");dd.textContent=val;
    dl.appendChild(dt);dl.appendChild(dd);if(vside)vside.appendChild(dl);});
  const inv=o.rounds.filter(r=>verdictFor(r,pts).k==="good").length;
  /* the tile row restated "Past rounds" four different ways; the charts carry it */
  put("h1n","textContent",S.occ); put("h8n","textContent",""); 
  put("h4n","textContent","");
  chartRounds(o,pts);chartQueue(g,pts);
  chartLandscape(o.g,pts);chartScatter(o.g,pts);
  takeaways(o,g,pts,size);
  bandTable(o,g,pts);levers();switchTable();policyTable();
  
  const tb=document.querySelector("#rt tbody"); if(tb){tb.innerHTML="";
  o.rounds.forEach(r=>{const v2=verdictFor(r,pts);const tr=document.createElement("tr");
    const cells=[RL[r.r],r.n?fmt(r.n):"—",r.lc===null?"—":r.lc,r.b===null?"—":r.b,
      r.b===null?"—":(r.s==="C"?"fully cleared":"rationed by date"),""];
    cells.forEach((c,i)=>{const td=document.createElement("td");
      if(i===5){const sp=document.createElement("span");sp.className="pill "+v2.k;sp.textContent=v2.t;td.appendChild(sp);}
      else td.textContent=c;tr.appendChild(td);});
    tb.appendChild(tr);});}
  renderAll(pts);
}
function renderAll(pts){
  if(!document.querySelector("#at tbody")) return;
  const tb=document.querySelector("#at tbody");tb.innerHTML="";
  const list=OCCS.map(k=>({k:k,o:B.occ[k]})).sort((a,b)=>b.o.pool-a.o.pool);
  ($(  "allN")||{}).textContent=list.length+" occupations";
  list.forEach(({k,o})=>{
    const g=B.groups[o.g];const tr=document.createElement("tr");
    if(k===S.occ)tr.className="hl";
    const td0=document.createElement("td");td0.textContent=k;tr.appendChild(td0);
    [fmt(o.pool),fmt(o.dist[Math.round(pts/5)*5]||0)].forEach(x=>{
      const td=document.createElement("td");td.textContent=x;tr.appendChild(td);});
    o.rounds.forEach(r=>{const v=verdictFor(r,pts);const td=document.createElement("td");
      const sp=document.createElement("span");sp.className="pill "+v.k;
      sp.textContent=r.b===null?"—":r.b;td.appendChild(sp);tr.appendChild(td);});
    const fv=fcVerdict(g?fcAt(g):null,pts);const td=document.createElement("td");
    const sp=document.createElement("span");sp.className="pill "+fv.k;
    sp.textContent=(g&&fcAt(g)!==null)?fcAt(g):"—";td.appendChild(sp);tr.appendChild(td);
    tr.addEventListener("click",()=>{S.occ=k;put("occ","value",k);render();window.scrollTo({top:0,behavior:"smooth"});});
    tr.style.cursor="pointer";tb.appendChild(tr);});
}

/* ---------- steppers: every box is walkable without typing ---------- */
function initDoe(){
  const sel=$("doe"); if(!sel||!B.doe_months) return;
  B.doe_months.forEach(m=>{const o=document.createElement("option");
    o.value=m; o.textContent=m; sel.appendChild(o);});
  /* a native <input type="month"> renders in the browser's own locale, which showed
     as ----年--月; the months on record are a short known list, so offer exactly those */
}
function stepPts(d){
  const e=$("pts"); if(!e) return;
  const lo=+e.min||65, hi=+e.max||130;
  S.pts=Math.max(lo,Math.min(hi,(+e.value||lo)+d*5));
  e.value=S.pts; render(); if(window.__saveState)__saveState();
}
function stepDoe(d){
  const sel=$("doe"); if(!sel) return;
  const i=Math.max(0,Math.min(sel.options.length-1,sel.selectedIndex+d));
  sel.selectedIndex=i; S.doe=sel.value||null; render(); if(window.__saveState)__saveState();
}
function stepOcc(d){
  const keys=OCCS, i=keys.indexOf(S.occ);
  const j=Math.max(0,Math.min(keys.length-1,(i<0?0:i)+d));
  S.occ=keys[j]; put("occ","value",S.occ); render(); if(window.__saveState)__saveState();
}
function initSteppers(){
  on("ptsdn","click",()=>stepPts(-1));  on("ptsup","click",()=>stepPts(1));
  on("doedn","click",()=>stepDoe(-1));  on("doeup","click",()=>stepDoe(1));
  on("occprev","click",()=>stepOcc(-1));on("occnext","click",()=>stepOcc(1));
  /* Alt + arrows step the occupation from anywhere, so the list does not have to be open */
  addEventListener("keydown",e=>{
    if(!e.altKey||e.metaKey||e.ctrlKey) return;
    if(e.key==="ArrowLeft"){e.preventDefault();stepOcc(-1);}
    else if(e.key==="ArrowRight"){e.preventDefault();stepOcc(1);}});
  /* the points box already steps by 5 on Up/Down because of step="5"; mirror that on
     the month select, which otherwise only moves one option at a time on focus */
  const sel=$("doe");
  if(sel) sel.addEventListener("keydown",e=>{
    if(e.key==="Home"){e.preventDefault();sel.selectedIndex=0;sel.dispatchEvent(new Event("input"));}
    else if(e.key==="End"){e.preventDefault();sel.selectedIndex=sel.options.length-1;
      sel.dispatchEvent(new Event("input"));}});
}
/* ---------- controls ---------- */
function initCombo(){
  const inp=$("occ"),box=$("opts");
  if(!inp||!box) return;
  let active=-1;
  inp.setAttribute("role","combobox");
  inp.setAttribute("aria-expanded","false");
  inp.setAttribute("aria-autocomplete","list");
  inp.setAttribute("aria-controls","opts");
  function opts(){return [...box.children];}
  function mark(i){
    const o=opts();
    o.forEach(d=>{d.classList.remove("sel");d.removeAttribute("aria-selected");});
    if(i>=0&&i<o.length){
      active=i;o[i].classList.add("sel");o[i].setAttribute("aria-selected","true");
      o[i].id="opt"+i;inp.setAttribute("aria-activedescendant","opt"+i);
      o[i].scrollIntoView({block:"nearest"});
    } else { active=-1; inp.removeAttribute("aria-activedescendant"); }
  }
  function open(on){box.classList.toggle("on",on);inp.setAttribute("aria-expanded",on?"true":"false");
    if(!on){active=-1;inp.removeAttribute("aria-activedescendant");}}
  function pick(o){S.occ=o;inp.value=o;open(false);render();}
  function show(f){
    box.innerHTML="";
    const m=OCCS.filter(o=>o.toLowerCase().includes(f.toLowerCase())).slice(0,60);
    m.forEach((o,i)=>{
      const d=document.createElement("div");d.textContent=o;d.setAttribute("role","option");d.id="opt"+i;
      d.addEventListener("mousedown",e=>{e.preventDefault();pick(o);});
      box.appendChild(d);});
    open(m.length>0);
    mark(m.findIndex(o=>o===S.occ));
  }
  inp.addEventListener("focus",()=>show(inp.value===S.occ?"":inp.value));
  inp.addEventListener("input",()=>show(inp.value));
  inp.addEventListener("blur",()=>setTimeout(()=>open(false),120));
  inp.addEventListener("keydown",e=>{
    const o=opts();
    if(e.key==="ArrowDown"){e.preventDefault();if(!o.length)return show("");mark(Math.min(active+1,o.length-1));}
    else if(e.key==="ArrowUp"){e.preventDefault();mark(Math.max(active-1,0));}
    else if(e.key==="Home"&&o.length){e.preventDefault();mark(0);}
    else if(e.key==="End"&&o.length){e.preventDefault();mark(o.length-1);}
    else if(e.key==="Enter"){if(active>=0&&o[active]){e.preventDefault();pick(o[active].textContent);}}
    else if(e.key==="Escape"){open(false);inp.value=S.occ;}
  });
  inp.value=S.occ;
}

on("pts","input",e=>{S.pts=+e.target.value||0;render();});
on("doe","input",e=>{S.doe=e.target.value||null;render();});
on("doe","change",e=>{S.doe=e.target.value||null;render();});
on("hmsort","change",e=>{HMSORT=e.target.value;render();});
on("dl","click",()=>{
  const rows=[["occupation","unit_group","pool","at_your_score","your_points",
    ...B.rounds.map(r=>"boundary_"+r),...B.rounds.map(r=>"state_"+r),
    ...B.sizes.map(s=>"forecast_"+s),"assumed_round_size","p_reaches_your_score"]];
  const my=Math.round(S.pts/5)*5;
  OCCS.forEach(k=>{const o=B.occ[k],g=B.groups[o.g];
    const fc=g?fcAt(g):null, p=pAt(g,S.pts,CURG,SZ());
    rows.push([k,o.g,o.pool,o.dist[my]||0,S.pts,
      ...o.rounds.map(r=>r.b===null?"":r.b),
      ...o.rounds.map(r=>r.b===null?"":(r.s==="C"?"cleared":"partial")),
      ...(g?g.fc.map(v=>v===null?"":v):B.sizes.map(()=>"")),
      SZ(), p===null?"":p.toFixed(3)]);});
  const csv=rows.map(r=>r.map(c=>{const s=String(c);
    return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}).join(",")).join("\n");
  const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
  const a=document.createElement("a");a.href=url;
  a.download="skillselect189_"+S.pts+"pts_"+SZ()+".csv";
  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);});
/* (?) opens a small popover beside the button, not an inline expansion */
let POPFOR=null;
function closePop(){
  if($("pop"))$("pop").classList.remove("on"); if($("popbd"))$("popbd").classList.remove("on");
  if(POPFOR){POPFOR.setAttribute("aria-expanded","false"); POPFOR.focus(); POPFOR=null;}
}
function openPop(btn){
  const src=$(btn.dataset.note); if(!src) return;
  const card=btn.closest(".card"), h2=card?card.querySelector("h2"):null;
  put("poph","textContent",h2?h2.textContent:"About this panel");
  put("popb","innerHTML",src.innerHTML);
  const pop=$("pop");
  pop.classList.add("on"); if($("popbd"))$("popbd").classList.add("on");
  const r=btn.getBoundingClientRect(), pr=pop.getBoundingClientRect();
  let left=Math.min(r.right-pr.width, innerWidth-pr.width-10);
  left=Math.max(10,left);
  let top=r.bottom+8;
  if(top+pr.height>innerHeight-10) top=Math.max(10,r.top-pr.height-8);
  pop.style.left=left+"px"; pop.style.top=top+"px";
  btn.setAttribute("aria-expanded","true"); POPFOR=btn;
  $("popx").focus();
}
document.querySelectorAll(".q").forEach(b=>b.addEventListener("click",e=>{
  e.stopPropagation();
  if(POPFOR===b){closePop();return;}
  closePop(); openPop(b);}));
on("popx","click",closePop);
on("popbd","click",closePop);
addEventListener("keydown",e=>{if(e.key==="Escape")closePop();});
addEventListener("resize",closePop);
initDoe();initSteppers();initCombo();render();
</script>
"""
