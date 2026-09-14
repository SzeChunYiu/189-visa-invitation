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
    <h1>Will you be invited?</h1>
  </div>
  <div style="text-align:right">
    <div class="eyebrow">Pool snapshot Aug 2026 &middot; 5 rounds</div>
    <a href="findings.html">How this model works, and how it was validated &rarr;</a>
  </div>
</header>

<div class="filters">
  <div class="f combo">
    <label for="occ">Occupation</label>
    <input id="occ" type="text" autocomplete="off" placeholder="Search 199 occupations" aria-label="Occupation">
    <div class="opts" id="opts" role="listbox"></div>
  </div>
  <div class="f"><label for="pts">Your points</label>
    <input id="pts" type="number" value="85" min="0" max="180" step="5" aria-label="Your points score"></div>
  <div class="f"><label for="doe">EOI date <span style="opacity:.7">(optional)</span></label>
    <input id="doe" type="month" min="2024-07" max="2026-12" aria-label="Month your EOI was submitted or last changed"></div>

</div>

<div class="verdict" id="results" tabindex="-1">
  <div class="vmain">
    <div id="flag" class="vflag good"></div>
    <div class="hero" id="hero"></div>
    <p class="vsub" id="vsub"></p>
    <div class="meter">
      <div class="mtrack"><div class="mfill" id="mfill"></div></div>
      <div class="mlab"><span id="mleft"></span><span id="mright"></span></div>
    </div>
  </div>
  <div class="vside" id="vside"></div>
</div>

<div class="card"><div class="chead"><h2>Your chance vs round size</h2>
  <span class="eyebrow" id="h8n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n1" aria-label="Explain" data-note="n1">?</button></div>
  <p class="takeaway" id="t8"></p>
  <div class="movestrip" id="mv"></div>
  <div class="chartwrap"><svg id="c8" viewBox="0 0 586 268" role="img" aria-labelledby="c8t">
    <title id="c8t">Chance of an invitation against the size of the next round</title></svg></div>
  <p class="note" id="n1" hidden>Blue line: your chance at each round size. Faint lines: 5 points above and below. Shaded band: every round size on record. Green ribbon: how likely each size is, from the 2026&ndash;27 planning levels. Dashed line: the size those levels imply. Pool is the Aug-2026 snapshot; each extra month before the round makes this forecast ~0.7 points optimistic, so a December round would sit ~2 points higher than shown.</p></div>

<div class="tiles" id="tiles"></div>

<div class="grid2">
  <div class="card"><div class="chead"><h2>Past rounds</h2>
    <span class="eyebrow" id="h1n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n2" aria-label="Explain" data-note="n2">?</button></div>
    <p class="takeaway" id="t1"></p>
    <div class="chartwrap"><svg id="c1" viewBox="0 0 520 220" role="img" aria-labelledby="c1t"><title id="c1t">Minimum points invited, by round</title></svg></div>
    <p class="note" id="n2" hidden>Height = lowest score invited. <span style='color:var(--good)'>&#9679;</span> in &middot; <span style='color:var(--warn)'>&#9679;</span> date decides &middot; <span style='color:var(--crit)'>&#9679;</span> not reached. Dot size = invitations to this occupation.</p></div>
      <div class="card"><div class="chead"><h2>Who is ahead</h2>
    <span class="eyebrow" id="h4n"></span><button class="q" type="button" aria-expanded="false" aria-controls="n3" aria-label="Explain" data-note="n3">?</button></div>
    <p class="takeaway" id="t4"></p>
    <div class="chartwrap"><svg id="c4" viewBox="0 0 520 220" role="img" aria-labelledby="c4t"><title id="c4t">Queue position within the unit group</title></svg></div>
    <p class="note" id="n3" hidden>Blue = people counted from the top score down. Green = invitations last round. <b>Red dot below green &rarr; they reach you.</b></p></div>
</div>

<div class="card"><div class="chead"><h2>Every score band</h2>
  <span class="eyebrow" id="hbn"></span><button class="q" type="button" aria-expanded="false" aria-controls="n4" aria-label="Explain" data-note="n4">?</button></div>
  <div class="scroll"><table id="bt"><thead><tr><th>Points</th><th>This occupation</th>
    <th>Unit group</th><th>Cumulative ahead</th><th>vs you</th>
    <th>Chance</th></tr></thead><tbody></tbody></table></div>
  <p class="note" id="n4" hidden>What 5 or 10 more points would buy. Aug-2026 snapshot; order is points, then date of effect. Without a date, your whole band counts as ahead.</p></div>

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
    <div class="hm"><svg id="c6" viewBox="0 0 520 1420" role="img" aria-labelledby="c6t"><title id="c6t">Cut-off by unit group and round</title></svg></div>
    <div class="legend"><span>lowest points invited</span>
      <span class="ramp"><span style="background:var(--r1)"></span><span style="background:var(--r2)"></span><span style="background:var(--r3)"></span><span style="background:var(--r4)"></span><span style="background:var(--r5)"></span><span style="background:var(--r6)"></span><span style="background:var(--r7)"></span></span>
      <span>65 &rarr; 100+</span><span><i style="background:var(--deemph)"></i>no invitation</span></div>
    <p class="note" id="n6" hidden>Darker = higher score needed. A dot = no invitations. Click a row to load that group.</p></div>
  <div class="card"><div class="chead"><h2>Competition drives the score</h2>
    <span class="eyebrow">Jun 2026 round</span><button class="q" type="button" aria-expanded="false" aria-controls="n7" aria-label="Explain" data-note="n7">?</button></div>
    <p class="takeaway" id="t7"></p>
    <div class="chartwrap"><svg id="c7" viewBox="0 0 520 312" role="img" aria-labelledby="c7t"><title id="c7t">Pool size against cut-off</title></svg></div>
    <p class="note" id="n7" hidden>One dot per group. Right = more people per invitation. Up = higher score needed. Dot size = occupation size. <b>Yours is ringed.</b> Raw size barely matters (r&nbsp;=&nbsp;0.12); people per invitation does (r&nbsp;=&nbsp;0.61).</p></div>
</div>

<div class="card"><div class="chead"><h2>This occupation, round by round</h2><span class="eyebrow">the record for this occupation</span><button class="q" type="button" aria-expanded="false" aria-controls="n8" aria-label="Explain" data-note="n8">?</button></div>
  <div class="scroll"><table id="rt"><thead><tr><th>Round</th><th>Invited</th><th>Fully cleared to</th>
    <th>Boundary score</th><th>Boundary</th><th>Would you have been invited?</th></tr></thead><tbody></tbody></table></div>
  <p class="note" id="n8" hidden><b>Fully cleared to</b> = the lowest score where every EOI was invited. At or above it you are in regardless of date. On a rationed boundary, your date decides.</p></div>

<div class="card"><div class="chead"><h2>All occupations at your score</h2>
  <span style="display:flex;gap:12px;align-items:center">
    <span class="eyebrow" id="allN"></span>
    <button id="dl" style="font:inherit;font-size:11.5px;padding:5px 10px;border:1px solid var(--line);
      border-radius:7px;background:var(--paper);color:var(--brand);cursor:pointer">Download CSV</button>
  </span><button class="q" type="button" aria-expanded="false" aria-controls="n9" aria-label="Explain" data-note="n9">?</button></div>
  <div class="scroll" style="max-height:420px;overflow-y:auto"><table id="at"><thead><tr><th>Occupation</th>
    <th>Pool</th><th>At your score</th><th>Sep 24</th><th>Nov 24</th><th>Aug 25</th><th>Nov 25</th><th>Jun 26</th>
    <th>Forecast</th></tr></thead><tbody></tbody></table></div>
  <p class="note" id="n9" hidden>Click a row to load it. The CSV holds every figure behind this page, for all 199 occupations at your score.</p></div>

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
/* Empirical P(actual cut-off <= pts) given a forecast, from held-out residuals. */
function pLE(fc,pts){
  if(fc===null||fc===undefined) return null;
  const R=B.unc.residuals, need=fc-pts;
  return R.filter(e=>e>=need).length/R.length;
}
/* Share of your own points band dated BEFORE you. null when the reader gives no date,
   in which case we assume the worst - last in the band. */
function aheadShare(g,pts){
  if(S.doe===null) return null;
  const band=B.doe_cdf[g]&&B.doe_cdf[g][String(Math.round(pts/5)*5)];
  if(!band) return null;
  const i=B.doe_months.indexOf(S.doe);
  if(i<0) return S.doe<B.doe_months[0]?0:1;
  let sh=0;
  for(const [mi,c] of band){ if(mi<i) sh=c; else break; }
  return sh;
}
/* P(invited) = P(cut-off lands below your band) + P(it lands ON your band) x P(it reaches you within it). */
function pClear(fc,pts){
  const le=pLE(fc,pts); if(le===null) return null;
  const lt=pLE(fc,pts-5);
  const eq=Math.max(0,le-lt);
  const sh=(typeof CURG!=="undefined"&&CURG)?aheadShare(CURG,pts):null;
  const reach = sh===null ? 0 : Math.max(0,1-sh);
  return lt+eq*reach;
}
let CURG=null;
function pBand(fc){ return fc===null?null:[fc-B.unc.hi80, fc-B.unc.lo80]; }
function fcVerdict(c,pts){
  if(c===null||c===undefined) return {k:"n",t:"no forecast"};
  if(pts>c) return {k:"good",t:"clears"};
  if(pts===c) return {k:"warn",t:"on the boundary"};
  return {k:"crit",t:"not reached"};
}
/* ---------- svg helpers ---------- */
const NS="http://www.w3.org/2000/svg";
function el(t,a){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e;}
function clear(s){while(s.childNodes.length>1)s.removeChild(s.lastChild);}
function tipOn(ev,html){const t=$("tip");t.innerHTML=html;t.style.display="block";
  const r=12;t.style.left=Math.min(ev.clientX+r,innerWidth-t.offsetWidth-8)+"px";
  t.style.top=Math.max(8,ev.clientY-t.offsetHeight-r)+"px";}
function tipOff(){$("tip").style.display="none";}
/* Pointer-only. Marks are deliberately NOT tab stops: making 500+ of them focusable
   traps keyboard users. Every number in these charts is also in a table or the CSV. */
function hover(node,html){
  node.addEventListener("pointermove",e=>tipOn(e,html));
  node.addEventListener("pointerleave",tipOff);
  node.setAttribute("aria-hidden","true");}

function axisTitle(s,W,H,MB,xt,yt){
  const x=el("text",{x:W/2,y:H-MB+33,class:"tick","text-anchor":"middle","font-weight":"600"});
  x.textContent=xt;s.appendChild(x);
  if(yt){const y=el("text",{x:10,y:H/2,class:"tick","text-anchor":"middle","font-weight":"600",
    transform:"rotate(-90 10 "+(H/2)+")"});y.textContent=yt;s.appendChild(y);}}
function panel(s,letter){
  const t=el("text",{x:2,y:11,fill:"var(--ink)","font-size":"12","font-weight":"750"});
  t.textContent=letter;s.appendChild(t);}
/* ---------- chart 1: cut-off by round ---------- */
function chartRounds(o,pts){
  const s=$("c1");clear(s);
  const W=520,H=230,ML=36,MR=18,MT=22,MB=54,pw=W-ML-MR,ph=H-MT-MB;
  const rs=o.rounds, vals=rs.map(r=>r.b).filter(v=>v!==null);
  const lo=Math.min(60,pts-5,...vals), hi=Math.max(pts+5,...vals,100);
  const X=i=>ML+(rs.length===1?pw/2:pw*i/(rs.length-1));
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
      const c0=el("circle",{cx:X(i),cy:H-MB+32,r:5,fill:"var(--deemph)"});s.appendChild(c0);
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
    const c2=el("circle",{cx:X(i),cy:H-MB+32,r:5,fill:COL[v.k]});s.appendChild(c2);
    const nl=el("text",{x:X(i),y:H-MB+47,class:"tick","text-anchor":"middle"});
    nl.textContent=r.n?fmt(r.n):"";s.appendChild(nl);});
  const yl=el("text",{x:ML-7,y:MT-8,class:"tick","text-anchor":"end"});yl.textContent="pts";s.appendChild(yl);
  const nl2=el("text",{x:ML-7,y:H-MB+47,class:"tick","text-anchor":"end"});nl2.textContent="invites";s.appendChild(nl2);
  panel(s,"a");
}
/* ---------- chart 4: the mechanism itself - cumulative queue vs allocation ---------- */
function chartQueue(g,pts){
  const s=$("c4");clear(s);
  const W=520,H=220,ML=46,MR=60,MT=16,MB=42,pw=W-ML-MR,ph=H-MT-MB;
  if(!g){const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No unit-group data.";s.appendChild(t);return;}
  const keys=Object.keys(g.dist).map(Number).sort((a,b)=>b-a).filter(k=>k>=B.floor);
  if(!keys.length){const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No EOIs at or above the 65-point floor.";s.appendChild(t);return;}
  let cum=0; const step=keys.map(k=>{cum+=g.dist[k];return {sc:k,cum:cum};});
  const alloc=g.alloc[g.alloc.length-1];
  const fc=g.fc[S.szi];
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
  s.appendChild(el("path",{d:d,class:"ln"}));
  /* allocation reference: where the last round stopped */
  const ay=Y(alloc);
  s.appendChild(el("line",{x1:ML,y1:ay,x2:W-MR,y2:ay,stroke:"var(--good)","stroke-width":1.5,"stroke-dasharray":"5 4"}));
  const at=el("text",{x:W-MR+4,y:ay+3.5,fill:"var(--good)","font-size":"10.5","font-weight":"650"});
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
  axisTitle(s,W,H,MB,"points, highest first","people ahead (cumulative)");panel(s,"d");
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
  RAMP=rampSteps();
  const s=$("c6");clear(s);
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
  panel(s,"f");
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
        if(first){S.occ=first;$("occ").value=first;render();window.scrollTo({top:0,behavior:"smooth"});}});});
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
  const s=$("c7");clear(s);
  const W=520,H=312,ML=42,MR=18,MT=18,MB=62,pw=W-ML-MR,ph=H-MT-MB;
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
      if(f){S.occ=f;$("occ").value=f;render();window.scrollTo({top:0,behavior:"smooth"});}});});
  axisTitle(s,W,H,MB,"people per invitation","lowest score invited");
  panel(s,"g");
  const nt=el("text",{x:(ML+W-MR)/2,y:H-MB+50,class:"tick","text-anchor":"middle","font-style":"italic"});
  nt.textContent="right = more competition";s.appendChild(nt);
}





/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */







/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */


function probTakeaway(g,pts){
  if(!g||g.share<=0){say("t8","","No invitations last round, so nothing to forecast.");return;}
  const cen=B.policy?B.policy.per_round["3"]:10000;
  const cp=pClear(cutoffAt(g,cen),pts);
  let need=null;
  for(let v=2000;v<=20000;v+=200){const p=pClear(cutoffAt(g,v),pts); if(p!==null&&p>=.5){need=v;break;}}
  say("t8", cp===null?"":cp>=.8?"good":cp>=.5?"warn":"crit",
    "<b>"+rangeText(g,pts)+"</b> across plausible round sizes"+
    (need?" &middot; even odds from <b>"+fmt(need)+"</b> invitations":" &middot; never reaches even odds")+".");
}
/* ---------- every score band ---------- */
function bandTable(o,g,pts){
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

/* ---------- chance against round size: the whole function, not five samples ---------- */
function cutoffAt(g,S){
  const A=Math.round(g.share*S*B.meta.fr);
  if(A<=0) return null;
  const keys=Object.keys(g.dist).map(Number).filter(k=>k>=B.floor).sort((a,b)=>b-a);
  let c=0;
  for(const k of keys){c+=g.dist[k]; if(c>=A) return k;}
  return B.floor;
}
/* P(this group gets NOTHING next round). Strongly clustered: whether it got something
   last round is the dominant predictor (8% vs 76%), so use that branch. */
function pZero(gk){
  if(!B.zr) return 0;
  const rec=B.zr.per_group&&B.zr.per_group[gk];
  if(!rec) return B.zr.base_rate;
  return rec.last_alloc>0 ? B.zr.p_zero_given_prev_nonzero : B.zr.p_zero_given_prev_zero;
}
/* Marginal over round size, THEN discounted by the chance the group is skipped entirely. */
function pMarginal(g,pts,gk){
  if(!g||g.share<=0||!B.rs) return null;
  let acc=0,wsum=0;
  B.rs.grid.forEach((sz,i)=>{const p=pClear(cutoffAt(g,sz),pts);
    if(p!==null){acc+=B.rs.dens[i]*p;wsum+=B.rs.dens[i];}});
  if(wsum<=0) return null;
  const conditional=acc/wsum;
  const skip=pZero(gk||(typeof CURG!=="undefined"?CURG:null));
  return conditional*(1-skip);
}
function chartProb(g,pts){
  const s=$("c8");clear(s);
  const W=586,H=268,ML=44,MR=66,MT=30,MB=46,pw=W-ML-MR,ph=H-MT-MB;
  if(!g||g.share<=0){const q=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    q.textContent="No invitations last round, so there is nothing to forecast at any size.";s.appendChild(q);return;}
  const S0=2000,S1=20000;
  const X=v=>ML+pw*(v-S0)/(S1-S0), Y=p=>MT+ph*(1-p);
  for(let i=0;i<=4;i++){const y=MT+ph*(1-i/4);
    s.appendChild(el("line",{x1:ML,y1:y,x2:W-MR,y2:y,class:"gl"}));
    const q=el("text",{x:ML-7,y:y+3.5,class:"tick","text-anchor":"end"});q.textContent=(i*25)+"%";s.appendChild(q);}
  /* the range of round sizes actually observed - context for what is plausible */
  const bx0=X(B.meta.round_min), bx1=X(B.meta.round_max);
  s.appendChild(el("rect",{x:bx0,y:MT,width:bx1-bx0,height:ph,fill:"var(--series)","fill-opacity":".07"}));
  const bl=el("text",{x:(bx0+bx1)/2,y:MT-5,class:"tick","text-anchor":"middle"});
  bl.textContent="observed range";s.appendChild(bl);
  /* context: the same curve 5 points below and above, so the value of more points is visible */
  const curve=sc=>{const a=[];for(let v=S0;v<=S1;v+=200){const p=pClear(cutoffAt(g,v),sc);
    if(p!==null)a.push([v,p]);}return a;};
  const path=a=>{let d="";a.forEach((q,i)=>{d+=(i?" L":"M")+X(q[0]).toFixed(1)+","+Y(q[1]).toFixed(1);});return d;};
  const ends=[];
  [[pts+5,(pts+5)+" pts","var(--deemph)"],[pts,"YOU \u2192 "+pts,"var(--series)"],[pts-5,(pts-5)+" pts","var(--deemph)"]]
   .forEach(([sc,lab,col])=>{
    const a=curve(sc); if(a.length<2) return;
    const main=(sc===pts);
    s.appendChild(el("path",{d:path(a),fill:"none",stroke:main?"var(--series)":"var(--deemph)",
      "stroke-width":main?2:1.5,"stroke-linejoin":"round","stroke-linecap":"round"}));
    ends.push({y:Y(a[a.length-1][1]),lab,col,main});});
  /* push labels apart so none overlaps another */
  ends.sort((a,b)=>a.y-b.y);
  for(let i=1;i<ends.length;i++) if(ends[i].y-ends[i-1].y<13) ends[i].y=ends[i-1].y+13;
  const shift=Math.max(0,ends[ends.length-1].y-(MT+ph));
  ends.forEach(e=>{
    const q=el("text",{x:W-MR+5,y:e.y-shift+3.5,fill:e.col,"font-size":e.main?"11":"10",
      "font-weight":e.main?"700":"600","text-anchor":"start"});
    q.textContent=e.lab;s.appendChild(q);});
  /* how likely each round size is, as a ribbon under the curve - same panel, no extra chart */
  if(B.rs){
    const dmax=Math.max(...B.rs.dens), hband=ph*0.22;
    let dd="M"+X(B.rs.grid[0]).toFixed(1)+","+(MT+ph).toFixed(1);
    B.rs.grid.forEach((sz,i)=>{if(sz<S0||sz>S1)return;
      dd+=" L"+X(sz).toFixed(1)+","+(MT+ph-hband*B.rs.dens[i]/dmax).toFixed(1);});
    dd+=" L"+X(Math.min(S1,B.rs.grid[B.rs.grid.length-1])).toFixed(1)+","+(MT+ph).toFixed(1)+" Z";
    s.appendChild(el("path",{d:dd,fill:"var(--brand)","fill-opacity":".16",stroke:"var(--brand)",
      "stroke-width":1,"stroke-opacity":".45"}));
    const dl=el("text",{x:ML+4,y:MT+ph-hband-6,class:"tick","text-anchor":"start",fill:"var(--brand)"});
    dl.textContent="likely round sizes";s.appendChild(dl);}
  /* the policy-implied central case */
  const cen=B.policy?B.policy.per_round["3"]:10000;
  const cp=pClear(cutoffAt(g,cen),pts);
  s.appendChild(el("line",{x1:X(cen),y1:MT,x2:X(cen),y2:MT+ph,stroke:"var(--brand)","stroke-width":1.5,"stroke-dasharray":"5 4"}));
  if(cp!==null){
    s.appendChild(el("circle",{cx:X(cen),cy:Y(cp),r:6,fill:"var(--brand)",stroke:"var(--card)","stroke-width":2}));
    const lab=el("text",{x:X(cen)+9,y:Y(cp)-9,fill:"var(--brand)","font-size":"12","font-weight":"700"});
    lab.textContent=Math.round(cp*100)+"%";s.appendChild(lab);}
  const cl=el("text",{x:X(cen)-7,y:MT+10,fill:"var(--brand)","font-size":"10","font-weight":"650",
    "text-anchor":"end"});
  cl.textContent="planning levels";s.appendChild(cl);
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
  axisTitle(s,W,H,MB,"invitations in the round","chance of an invitation");
  panel(s,"h");
}
/* ---------- every round-size case, side by side ---------- */
/* The range quoted everywhere: across the 10-90% band of plausible round sizes. */
function rangeBand(g,pts){
  if(!g||g.share<=0||!B.rs) return null;
  const a=pClear(cutoffAt(g,B.rs.q10),pts), b=pClear(cutoffAt(g,B.rs.q90),pts);
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
  const inv=o.rounds.filter(r=>verdictFor(r,pts).k==="good").length;
  const dated=o.rounds.filter(r=>verdictFor(r,pts).k==="warn").length;
  say("t1", inv>=3?"good":inv>0?"warn":"crit",
    "<b>"+inv+" of 5</b> past rounds would have invited you"+(dated?", <b>"+dated+"</b> on date":"")+".");
  const fc=g?g.fc[S.szi]:null, P=pClear(fc,pts);
  say("t2", P===null?"":P>=.8?"good":P>=.5?"warn":"crit",
    P===null ? "This occupation got no invitations last round, so there is nothing to forecast from."
    : "If the next round invites <b>"+fmt(size)+"</b> people, the lowest score getting in should be about <b>"+fc+
      "</b>. You are on <b>"+pts+"</b>, so your chance is <b>"+Math.round(P*100)+"%</b>.");
  const my=Math.round(pts/5)*5, same=o.dist[my]||0, above=Object.keys(o.dist).map(Number).filter(k=>k>my)
    .reduce((a,k)=>a+o.dist[k],0);
  say("t3","", same===0 && above===0
    ? "Nobody waiting at your score or above."
    : "<b>"+fmt(same)+"</b> on your score, <b>"+fmt(above)+"</b> above it, in this occupation.");
  const ge=g?Object.keys(g.dist).map(Number).filter(k=>k>=my).reduce((a,k)=>a+g.dist[k],0):0;
  const al=g?g.alloc[g.alloc.length-1]:0;
  say("t4", al>=ge?"good":"crit",
    "<b>"+fmt(ge)+"</b> ahead &middot; last round invited <b>"+fmt(al)+"</b> &mdash; "+
    (al>=ge?"<b>reaches you</b>.":"<b>stops short</b>."));
  const need=g?B.sizes.find((sz,i)=>{const p=pClear(g.fc[i],pts);return p!==null&&p>=.8;}):null;
  say("t5","", need
    ? "Comfortably in above <b>"+fmt(need)+"</b> invitations."
    : "No round size in range gets you comfortably in at <b>"+pts+"</b>.");
  const gp=g?Object.values(g.dist).reduce((a,b)=>a+b,0):0;
  if(g&&al>0){const ratio=gp/al;
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
function moveStrip(){
  const box=$("mv"); if(!box||!B.mv) return; box.innerHTML="";
  const M=B.mv, R=M.delta_recent||{};
  const g=k=>R[k]||0;
  const segs=[["cut-off falls 10 or more",g("-25")+g("-15")+g("-10"),"var(--good)"],
              ["cut-off falls 5",g("-5"),"var(--good)"],
              ["no change",g("0"),"var(--deemph)"],
              ["rises 5",g("5"),"var(--warn)"],
              ["rises 10 or more",g("10")+g("15")+g("20")+g("25"),"var(--crit)"]];
  const tot=segs.reduce((a,x)=>a+x[1],0)||1;
  const bar=document.createElement("div");bar.className="mbar";
  segs.forEach(([lab,n,col],i)=>{
    if(!n) return;
    const d=document.createElement("div");
    d.style.cssText="flex:"+n+" 0 0;background:"+col+(i===0||i===1?";color:#fff":"");
    d.title=lab+" — "+Math.round(100*n/tot)+"% of round-to-round moves";
    if(n/tot>0.11) d.textContent=Math.round(100*n/tot)+"%";
    bar.appendChild(d);});
  box.appendChild(bar);
  const key=document.createElement("div");key.className="mkey";
  key.innerHTML='<span><i style="background:var(--good)"></i>falls</span>'+
    '<span><i style="background:var(--deemph)"></i>unchanged</span>'+
    '<span><i style="background:var(--warn)"></i>rises 5</span>'+
    '<span><i style="background:var(--crit)"></i>rises 10+ ('+Math.round(M.p_move10*100)+'%)</span>'+
    '<span style="margin-left:auto">'+Math.round((1-M.boundary_cleared)*100)+
    '% of boundary bands leave someone behind</span>';
  box.appendChild(key);
}
/* ---------- the occupations switched off, and the one that was not ---------- */
function switchTable(){
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
/* ---------- render ---------- */
function render(){
  const o=B.occ[S.occ]; if(!o) return;
  CURG=o.g;
  const g=B.groups[o.g]; const pts=S.pts; const size=B.sizes[S.szi];
  const last=o.rounds[o.rounds.length-1];
  const fc=g?g.fc[S.szi]:null;
  const v=fcVerdict(fc,pts);
  const P=pMarginal(g,pts,o.g), Pc=pClear(fc,pts), bb=pBand(fc);
  chartProb(g,pts);probTakeaway(g,pts);moveStrip();
  const band = P===null?null:(P>=.8?"good":P>=.6?"good":P>=.4?"warn":"crit");
  $("flag").className="vflag "+(band||"crit");
  $("flag").textContent = P===null ? "✕ No forecast"
    : P>=.8 ? "✓ Likely invited"
    : P>=.6 ? "✓ Favourable, not certain"
    : P>=.4 ? "! Could go either way"
    : "✕ Unlikely at this score";
  $("hero").textContent = P===null ? "—" : Math.round(P*100)+"%";
  $("vsub").innerHTML = P===null
    ? "This occupation received no invitations in the most recent round, so there is no allocation share to forecast from. The round-by-round record below still applies."
    : "at <b>"+pts+" points</b> in <b>"+o.g+"</b>. Averaged over likely round sizes, less a <b>"+
      Math.round(pZero(o.g)*100)+"%</b> chance this group is skipped. Assumes a round is held &mdash; that is "+
      "the one thing no model can predict.";
  const ge=g?Object.keys(g.dist).map(Number).filter(k=>k>=pts).reduce((a,k)=>a+g.dist[k],0):0;
  const al=g?g.alloc[g.alloc.length-1]:0;
  const ratio=ge>0?al/ge:0;
  $("mfill").style.width=Math.max(2,Math.min(100,ratio*50))+"%";
  $("mleft").textContent="last round allocated "+fmt(al)+" to this group";
  $("mright").textContent=fmt(ge)+" sit at "+pts+"+ · "+(ge>0?ratio.toFixed(2)+"×":"—");
  $("vside").innerHTML="";
  const rows=[["At likely round size",Pc===null?"—":Math.round(Pc*100)+"%"],
    ["Forecast cut-off",fc===null?"—":fc+" pts (80% "+bb[0]+"–"+bb[1]+")"],
    ["Likely round size",fmt(B.rs.q50)+" ("+fmt(B.rs.q10)+"–"+fmt(B.rs.q90)+")"],
    ["Ahead of you in "+o.g,fmt(ge)],
    ["Risk of no invitations",Math.round(pZero(o.g)*100)+"%"],
    ["Priority tier",tierLabel(o.g)]];
  rows.forEach(([k,val])=>{const dl=document.createElement("dl");dl.className="kv";
    const dt=document.createElement("dt");dt.textContent=k;const dd=document.createElement("dd");dd.textContent=val;
    dl.appendChild(dt);dl.appendChild(dd);$("vside").appendChild(dl);});
  const inv=o.rounds.filter(r=>verdictFor(r,pts).k==="good").length;
  const tiles=[[inv+" of 5",'rounds that would have invited you at '+pts+' pts'],
    [fmt(o.rounds.reduce((a,r)=>a+r.n,0)),"invitations to this occupation, all rounds"],
    [last.b===null?"—":last.b,"lowest points invited, most recent round"],
    [g?g.alloc.join(" → "):"—","allocation to your unit group, by round"],
    [B.meta.cal_exact*100+"%","of occupations matched the official table exactly"]];
  $("tiles").innerHTML="";
  tiles.forEach(([v2,l])=>{const c=document.createElement("div");c.className="tile";
    const a=document.createElement("div");a.className="tval";a.textContent=v2;
    const b=document.createElement("div");b.className="tlab";b.textContent=l;
    c.appendChild(a);c.appendChild(b);$("tiles").appendChild(c);});
  $("h1n").textContent=S.occ; $("h8n").textContent=""; 
  $("h4n").textContent="";
  chartRounds(o,pts);chartQueue(g,pts);
  chartLandscape(o.g,pts);chartScatter(o.g,pts);
  takeaways(o,g,pts,size);
  bandTable(o,g,pts);switchTable();policyTable();
  
  const tb=document.querySelector("#rt tbody");tb.innerHTML="";
  o.rounds.forEach(r=>{const v2=verdictFor(r,pts);const tr=document.createElement("tr");
    const cells=[RL[r.r],r.n?fmt(r.n):"—",r.lc===null?"—":r.lc,r.b===null?"—":r.b,
      r.b===null?"—":(r.s==="C"?"fully cleared":"rationed by date"),""];
    cells.forEach((c,i)=>{const td=document.createElement("td");
      if(i===5){const sp=document.createElement("span");sp.className="pill "+v2.k;sp.textContent=v2.t;td.appendChild(sp);}
      else td.textContent=c;tr.appendChild(td);});
    tb.appendChild(tr);});
  renderAll(pts);
}
function renderAll(pts){
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
    const fv=fcVerdict(g?g.fc[S.szi]:null,pts);const td=document.createElement("td");
    const sp=document.createElement("span");sp.className="pill "+fv.k;
    sp.textContent=(g&&g.fc[S.szi]!==null)?g.fc[S.szi]:"—";td.appendChild(sp);tr.appendChild(td);
    tr.addEventListener("click",()=>{S.occ=k;$("occ").value=k;render();window.scrollTo({top:0,behavior:"smooth"});});
    tr.style.cursor="pointer";tb.appendChild(tr);});
}
/* ---------- controls ---------- */
function initCombo(){
  const inp=$("occ"),box=$("opts");
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

$("pts").addEventListener("input",e=>{S.pts=+e.target.value||0;render();});
$("doe").addEventListener("input",e=>{S.doe=e.target.value||null;render();});
$("hmsort").addEventListener("change",e=>{HMSORT=e.target.value;render();});
$("dl").addEventListener("click",()=>{
  const rows=[["occupation","unit_group","pool","at_your_score","your_points",
    ...B.rounds.map(r=>"boundary_"+r),...B.rounds.map(r=>"state_"+r),
    ...B.sizes.map(s=>"forecast_"+s),"assumed_round_size","p_reaches_your_score"]];
  const my=Math.round(S.pts/5)*5;
  OCCS.forEach(k=>{const o=B.occ[k],g=B.groups[o.g];
    const fc=g?g.fc[S.szi]:null, p=pClear(fc,S.pts);
    rows.push([k,o.g,o.pool,o.dist[my]||0,S.pts,
      ...o.rounds.map(r=>r.b===null?"":r.b),
      ...o.rounds.map(r=>r.b===null?"":(r.s==="C"?"cleared":"partial")),
      ...(g?g.fc.map(v=>v===null?"":v):B.sizes.map(()=>"")),
      B.sizes[S.szi], p===null?"":p.toFixed(3)]);});
  const csv=rows.map(r=>r.map(c=>{const s=String(c);
    return /[",\n]/.test(s)?'"'+s.replace(/"/g,'""')+'"':s;}).join(",")).join("\n");
  const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));
  const a=document.createElement("a");a.href=url;
  a.download="skillselect189_"+S.pts+"pts_"+B.sizes[S.szi]+".csv";
  document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);});
/* (?) opens a small popover beside the button, not an inline expansion */
let POPFOR=null;
function closePop(){
  $("pop").classList.remove("on"); $("popbd").classList.remove("on");
  if(POPFOR){POPFOR.setAttribute("aria-expanded","false"); POPFOR.focus(); POPFOR=null;}
}
function openPop(btn){
  const src=$(btn.dataset.note); if(!src) return;
  const card=btn.closest(".card"), h2=card?card.querySelector("h2"):null;
  $("poph").textContent=h2?h2.textContent:"About this panel";
  $("popb").innerHTML=src.innerHTML;
  const pop=$("pop");
  pop.classList.add("on"); $("popbd").classList.add("on");
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
$("popx").addEventListener("click",closePop);
$("popbd").addEventListener("click",closePop);
addEventListener("keydown",e=>{if(e.key==="Escape")closePop();});
addEventListener("resize",closePop);
initCombo();render();
</script>
"""
