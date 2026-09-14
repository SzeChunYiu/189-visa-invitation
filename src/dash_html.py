HTML = r"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SkillSelect 189 Explorer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<style>__CSS__</style>
<div class="wrap">
<header>
  <div>
    <div class="eyebrow">Subclass 189 &middot; Points-Tested Stream</div>
    <h1>Where do you stand in the 189 queue?</h1>
  </div>
  <div style="text-align:right">
    <div class="eyebrow">Pool snapshot Aug 2026 &middot; 5 rounds</div>
    <a href="findings.html">How this model works, and how it was validated &rarr;</a>
  </div>
</header>

<div class="filters">
  <div class="f combo">
    <label for="occ">Your occupation (ANZSCO)</label>
    <input id="occ" type="text" autocomplete="off" placeholder="Type to search 199 occupations&hellip;" aria-label="Occupation">
    <div class="opts" id="opts" role="listbox"></div>
  </div>
  <div class="f"><label for="pts">Your points</label>
    <input id="pts" type="number" value="85" min="0" max="180" step="5" aria-label="Your points score"></div>
  <div class="f"><label for="sz">Assume next round size</label>
    <select id="sz" aria-label="Assumed round size"></select></div>
</div>

<div class="verdict">
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

<div class="tiles" id="tiles"></div>

<div class="grid2">
  <div class="card"><div class="chead"><h2>What this occupation actually reached</h2>
    <span class="eyebrow" id="h1n"></span></div>
    <svg id="c1" viewBox="0 0 520 220" role="img" aria-labelledby="c1t"><title id="c1t">Minimum points invited, by round</title></svg>
    <p class="note">Lowest points invited in each of the five real rounds. A filled marker means that score was
    fully exhausted, so everyone at it was invited; a hollow marker means it was rationed by date of effect.
    The red rule is your score.</p></div>
  <div class="card"><div class="chead"><h2>Forecast for the next round</h2>
    <span class="eyebrow" id="h2n"></span></div>
    <svg id="c2" viewBox="0 0 520 220" role="img" aria-labelledby="c2t"><title id="c2t">Forecast cut-off by round size</title></svg>
    <p class="note">Where the cut-off lands if the next round is this size, using this group's current share of
    invitations. The shaded band is the 80% prediction interval, taken from the
    distribution of this method's own errors on held-out rounds &mdash; not an assumption. Hover any point for
    the interval and the probability it reaches your score.</p></div>
  <div class="card"><div class="chead"><h2>Who you are competing with</h2>
    <span class="eyebrow" id="h3n"></span></div>
    <svg id="c3" viewBox="0 0 520 220" role="img" aria-labelledby="c3t"><title id="c3t">Standing pool by points score</title></svg>
    <p class="note">Everyone in this occupation currently sitting in the 189 pool, by points. Your bucket is
    highlighted. Hover any column for the count.</p></div>
  <div class="card"><div class="chead"><h2>Your position in the queue</h2>
    <span class="eyebrow" id="h4n"></span></div>
    <svg id="c4" viewBox="0 0 520 220" role="img" aria-labelledby="c4t"><title id="c4t">Queue position within the unit group</title></svg>
    <p class="note">This is the mechanism itself. The curve is the cumulative number of EOIs at or above each score
    in your unit group; the dashed line is how many the last round actually invited. <b>Where they cross is the
    cut-off.</b> Your position is marked &mdash; if the dashed line sits above your marker, a round of that size
    reaches you.</p></div>
</div>

<div class="card wide"><div class="chead"><h2>Exactly who is ahead of you</h2>
  <span class="eyebrow" id="h8n"></span></div>
  <div class="scroll"><table id="qt"><thead><tr><th>Points</th><th>In your occupation</th>
    <th>In your unit group</th><th>Running total ahead of you</th><th>Standing</th></tr></thead><tbody></tbody></table></div>
  <p class="note">Every EOI counted individually, from the Aug 2026 snapshot, single-leg basis. Invitations run
  strictly by points then date of effect, so everyone above your score and everyone on your score with an earlier
  date sits ahead. All EOIs in this snapshot pre-date a newly lodged one, so the whole of your own score row counts
  as ahead.</p></div>

<div class="card"><div class="chead"><h2>Policy: the 2026&ndash;27 program</h2>
  <span class="eyebrow">published planning levels</span></div>
  <div class="scroll"><table id="pt"><thead><tr><th>Category</th><th>2025&ndash;26</th><th>2026&ndash;27</th><th>Change</th></tr></thead><tbody></tbody></table></div>
  <p class="note" id="pnote"></p></div>

<div class="card"><div class="chead"><h2>Your forecast at every score</h2>
  <span class="eyebrow" id="h5n"></span></div>
  <svg id="c5" viewBox="0 0 520 300" role="img" aria-labelledby="c5t"><title id="c5t">Outcome by points score and round size</title></svg>
  <div class="legend"><span><i style="background:var(--good)"></i>invited regardless of date</span>
    <span><i style="background:var(--warn)"></i>on the boundary, date decides</span>
    <span><i style="background:var(--crit)"></i>not reached</span></div>
  <p class="note">Every combination of points and round size for this occupation group, read like a forecast grid.
  Your row is outlined. Reading across a row shows how much a bigger round helps; reading down a column shows how
  much each extra 5 points is worth.</p></div>

<div class="grid2">
  <div class="card"><div class="chead"><h2>The whole landscape</h2>
    <span class="eyebrow">82 unit groups &times; 5 rounds</span></div>
    <div class="hm"><svg id="c6" viewBox="0 0 520 1420" role="img" aria-labelledby="c6t"><title id="c6t">Cut-off by unit group and round</title></svg></div>
    <div class="legend"><span>lowest points invited</span>
      <span class="ramp"><span style="background:#cde2fb"></span><span style="background:#9ec5f4"></span><span style="background:#6da7ec"></span><span style="background:#3987e5"></span><span style="background:#256abf"></span><span style="background:#184f95"></span><span style="background:#0d366b"></span></span>
      <span>65 &rarr; 100+</span><span><i style="background:var(--deemph)"></i>no invitation</span></div>
    <p class="note">Darker means a higher points bar. Sorted by the most recent round. Click any row to load that
    group's occupations. Your group is highlighted.</p></div>
  <div class="card"><div class="chead"><h2>Where your occupation sits</h2>
    <span class="eyebrow">pool vs cut-off, Jun 2026</span></div>
    <svg id="c7" viewBox="0 0 520 300" role="img" aria-labelledby="c7t"><title id="c7t">Pool size against cut-off</title></svg>
    <p class="note">Each dot is a unit group: how many EOIs it holds against the points bar it actually reached.
    Dot area is the invitations it received. Yours is outlined. Big pools do not automatically mean high
    cut-offs &mdash; what matters is the pool relative to the group's allocation.</p></div>
</div>

<div class="card"><div class="chead"><h2>Round by round</h2><span class="eyebrow">the record for this occupation</span></div>
  <div class="scroll"><table id="rt"><thead><tr><th>Round</th><th>Invited</th><th>Fully cleared to</th>
    <th>Boundary score</th><th>Boundary</th><th>Would you have been invited?</th></tr></thead><tbody></tbody></table></div>
  <p class="note"><b>Fully cleared to</b> is the lowest score at which every single EOI was invited. At or above it
  you are in regardless of date. On a rationed boundary, your date of effect decides.</p></div>

<div class="card"><div class="chead"><h2>Every occupation at your score</h2>
  <span class="eyebrow" id="allN"></span></div>
  <div class="scroll" style="max-height:420px;overflow-y:auto"><table id="at"><thead><tr><th>Occupation</th>
    <th>Pool</th><th>At your score</th><th>Sep 24</th><th>Nov 24</th><th>Aug 25</th><th>Nov 25</th><th>Jun 26</th>
    <th>Next round</th></tr></thead><tbody></tbody></table></div>
  <p class="note">Sorted by pool size. Click a row to load that occupation above.</p></div>

<footer>
  Built from all 24 monthly SkillSelect EOI snapshots read directly from the Qlik engine behind the Department of
  Employment's public dashboard. Counts are distinct EOIs on a single-leg basis. The model cannot predict whether a
  round is held or how large it is &mdash; both are set by migration planning levels. Not migration advice.
  <a href="https://github.com/SzeChunYiu/189-visa-invitation">Code, data and method</a> &middot;
  <a href="findings.html">Full findings</a>
</footer>
</div>
<div id="tip" role="status"></div>
<script>
const B=__BUNDLE__;
const S={occ:"234914 Physicist",pts:85,szi:2};
const $=id=>document.getElementById(id);
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
function pClear(fc,pts){
  if(fc===null||fc===undefined) return null;
  const R=B.unc.residuals, need=fc-pts;
  return R.filter(e=>e>=need).length/R.length;
}
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
function hover(node,html){node.addEventListener("pointermove",e=>tipOn(e,html));
  node.addEventListener("pointerleave",tipOff);node.setAttribute("tabindex","0");
  node.addEventListener("focus",e=>{const b=node.getBoundingClientRect();
    tipOn({clientX:b.left+b.width/2,clientY:b.top},html);});node.addEventListener("blur",tipOff);}

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
  const W=520,H=220,ML=34,MR=18,MT=18,MB=40,pw=W-ML-MR,ph=H-MT-MB;
  const rs=o.rounds, vals=rs.map(r=>r.b).filter(v=>v!==null);
  const lo=Math.min(60,pts-5,...vals), hi=Math.max(pts+5,...vals,100);
  const X=i=>ML+(rs.length===1?pw/2:pw*i/(rs.length-1));
  const Y=v=>MT+ph*(1-(v-lo)/(hi-lo));
  for(let v=Math.ceil(lo/5)*5;v<=hi;v+=5){ if((v%10)!==0) continue;
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    const t=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});t.textContent=v;s.appendChild(t);}
  if(pts>=lo&&pts<=hi){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const t=el("text",{x:W-MR,y:Y(pts)-6,class:"reft","text-anchor":"end"});t.textContent="your "+pts+" pts";s.appendChild(t);}
  const pts2=rs.map((r,i)=>r.b===null?null:[X(i),Y(r.b)]);
  let d="",started=false;
  pts2.forEach(p=>{if(!p){started=false;return;} d+=(started?" L":"M")+p[0].toFixed(1)+","+p[1].toFixed(1);started=true;});
  if(d) s.appendChild(el("path",{d:d,class:"ln"}));
  rs.forEach((r,i)=>{
    const t=el("text",{x:X(i),y:H-MB+16,class:"tick","text-anchor":"middle"});t.textContent=RL[r.r];s.appendChild(t);
    if(r.b===null){const q=el("text",{x:X(i),y:MT+ph/2,class:"tick","text-anchor":"middle"});q.textContent="—";s.appendChild(q);return;}
    const cleared=r.s==="C";
    const c=el("circle",{cx:X(i),cy:Y(r.b),r:5.5,class:"dot"});
    if(!cleared){c.setAttribute("fill","var(--card)");c.setAttribute("stroke","var(--series)");}
    s.appendChild(c);
    const lab=el("text",{x:X(i),y:Y(r.b)-11,class:"vlab","text-anchor":"middle"});lab.textContent=r.b;s.appendChild(lab);
    const v=verdictFor(r,pts);
    const h=el("rect",{x:X(i)-24,y:MT,width:48,height:ph,class:"hit"});
    hover(h,"<b>"+r.b+" points</b><span>"+RL[r.r]+" &middot; "+fmt(r.n)+" invited &middot; "+
      (cleared?"fully cleared":"rationed by date")+"</span><span>At "+pts+" pts: "+v.t+"</span>");
    s.appendChild(h);});
  axisTitle(s,W,H,MB,"invitation round","minimum points invited");panel(s,"a");
}
/* ---------- chart 2: forecast by round size ---------- */
function chartForecast(g,pts){
  const s=$("c2");clear(s);
  const W=520,H=220,ML=34,MR=18,MT=18,MB=40,pw=W-ML-MR,ph=H-MT-MB;
  if(!g||!g.fc||g.fc.every(v=>v===null)){
    const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No invitations last round, so no share to forecast from.";s.appendChild(t);return;}
  const vals=g.fc.filter(v=>v!==null);
  const lo=Math.min(60,pts-5,...vals), hi=Math.max(pts+5,...vals,95);
  const X=i=>ML+pw*i/(B.sizes.length-1), Y=v=>MT+ph*(1-(v-lo)/(hi-lo));
  for(let v=Math.ceil(lo/10)*10;v<=hi;v+=10){
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    const t=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});t.textContent=v;s.appendChild(t);}
  if(pts>=lo&&pts<=hi){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const t=el("text",{x:W-MR,y:Y(pts)-6,class:"reft","text-anchor":"end"});t.textContent="your "+pts+" pts";s.appendChild(t);}
  const up=[],dn=[];
  g.fc.forEach((v,i)=>{if(v===null)return;const b=pBand(v);
    up.push([X(i),Y(Math.min(hi,b[1]))]);dn.push([X(i),Y(Math.max(lo,b[0]))]);});
  if(up.length>1){
    let bd="M"+up.map(p=>p[0].toFixed(1)+","+p[1].toFixed(1)).join(" L")+
           " L"+dn.reverse().map(p=>p[0].toFixed(1)+","+p[1].toFixed(1)).join(" L")+" Z";
    s.appendChild(el("path",{d:bd,fill:"var(--series)","fill-opacity":".12",stroke:"none"}));}
  let d="";g.fc.forEach((v,i)=>{if(v===null)return;d+=(d?" L":"M")+X(i).toFixed(1)+","+Y(v).toFixed(1);});
  s.appendChild(el("path",{d:d,class:"ln"}));
  g.fc.forEach((v,i)=>{
    const t=el("text",{x:X(i),y:H-MB+16,class:"tick","text-anchor":"middle"});
    t.textContent=(B.sizes[i]/1000)+"k";s.appendChild(t);
    if(v===null)return;
    s.appendChild(el("circle",{cx:X(i),cy:Y(v),r:i===S.szi?6.5:5,class:"dot"}));
    const lab=el("text",{x:X(i),y:Y(v)-11,class:"vlab","text-anchor":"middle"});lab.textContent=v;s.appendChild(lab);
    const fv=fcVerdict(v,pts);
    const h=el("rect",{x:X(i)-26,y:MT,width:52,height:ph,class:"hit"});
    const bb=pBand(v), pp=pClear(v,pts);
    hover(h,"<b>cut-off "+v+"</b><span>if the round invites "+fmt(B.sizes[i])+
      "</span><span>80% interval "+bb[0]+"–"+bb[1]+"</span><span>P(reaches "+pts+" pts) = "+
      Math.round(pp*100)+"%</span>");
    s.appendChild(h);});
  axisTitle(s,W,H,MB,"assumed size of the next round","forecast cut-off (points)");panel(s,"b");
}
/* ---------- chart 3: pool by score (emphasis) ---------- */
function chartPool(o,pts){
  const s=$("c3");clear(s);
  const W=520,H=220,ML=34,MR=14,MT=18,MB=40,pw=W-ML-MR,ph=H-MT-MB;
  const keys=Object.keys(o.dist).map(Number).sort((a,b)=>a-b);
  if(!keys.length){const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No EOIs in the pool for this occupation.";s.appendChild(t);return;}
  const max=Math.max(...keys.map(k=>o.dist[k]));
  const band=pw/keys.length, bw=Math.min(24,band-2);
  for(let i=0;i<=4;i++){const v=max*i/4,y=MT+ph*(1-i/4);
    s.appendChild(el("line",{x1:ML,y1:y,x2:W-MR,y2:y,class:"gl"}));
    const t=el("text",{x:ML-7,y:y+3.5,class:"tick","text-anchor":"end"});t.textContent=Math.round(v);s.appendChild(t);}
  keys.forEach((k,i)=>{
    const n=o.dist[k], h=Math.max(2,ph*n/max), x=ML+band*i+(band-bw)/2, y=MT+ph-h;
    const on=(k===Math.round(pts/5)*5);
    const r=el("rect",{x:x,y:y,width:bw,height:h,rx:4,class:"bar"+(on?" on":"")});
    s.appendChild(r);
    hover(r,"<b>"+fmt(n)+"</b><span>EOIs at "+k+" points</span>");
    if(keys.length<=14||i%2===0){
      const t=el("text",{x:x+bw/2,y:H-MB+16,class:"tick","text-anchor":"middle"});t.textContent=k;s.appendChild(t);}
    if(on){const t=el("text",{x:x+bw/2,y:y-6,class:"vlab","text-anchor":"middle"});t.textContent=fmt(n);s.appendChild(t);}});
  axisTitle(s,W,H,MB,"points score","EOIs in the pool");panel(s,"c");
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
  axisTitle(s,W,H,MB,"points score (descending)","cumulative EOIs at or above");panel(s,"d");
}
/* ---------- chart 5: forecast matrix (score x round size) ---------- */
const SCORES=[120,115,110,105,100,95,90,85,80,75,70,65];
function chartMatrix(g,pts){
  const s=$("c5");clear(s);
  const W=520,H=300,ML=34,MR=14,MT=26,MB=34;
  if(!g||!g.fc||g.fc.every(v=>v===null)){
    const t=el("text",{x:W/2,y:H/2,class:"tick","text-anchor":"middle"});
    t.textContent="No invitations last round, so no forecast for this group.";s.appendChild(t);return;}
  const cols=B.sizes.length, cw=(W-ML-MR)/cols, ch=(H-MT-MB)/SCORES.length;
  const col={good:"var(--good)",warn:"var(--warn)",crit:"var(--crit)",n:"var(--deemph)"};
  B.sizes.forEach((sz,i)=>{const t=el("text",{x:ML+cw*(i+.5),y:MT-9,class:"tick","text-anchor":"middle"});
    t.textContent=(sz/1000)+"k";s.appendChild(t);});
  const xl=el("text",{x:(ML+W-MR)/2,y:H-MB+24,class:"tick","text-anchor":"middle","font-weight":"600"});
  xl.textContent="assumed size of the next round";s.appendChild(xl);panel(s,"e");
  SCORES.forEach((sc,r)=>{
    const y=MT+ch*r, mine=(sc===Math.round(pts/5)*5);
    const lt=el("text",{x:ML-8,y:y+ch/2,class:"rowlab"+(mine?" on":""),"text-anchor":"end"});
    lt.textContent=sc;s.appendChild(lt);
    B.sizes.forEach((sz,c)=>{
      const v=fcVerdict(g.fc[c],sc);
      const rect=el("rect",{x:ML+cw*c,y:y,width:cw,height:ch,rx:3,fill:col[v.k],class:"cell"});
      s.appendChild(rect);
      hover(rect,"<b>"+sc+" points</b><span>round of "+fmt(sz)+" &middot; forecast cut-off "+
        (g.fc[c]===null?"—":g.fc[c])+"</span><span>"+v.t+"</span>");
      if(mine){const o=el("rect",{x:ML+cw*c+1,y:y+1,width:cw-2,height:ch-2,rx:3,fill:"none",
        stroke:"var(--ink)","stroke-width":2,"pointer-events":"none"});s.appendChild(o);}});});
}
/* ---------- chart 6: landscape heatmap (group x round) ---------- */
const RAMP=["#cde2fb","#9ec5f4","#6da7ec","#3987e5","#256abf","#184f95","#0d366b"];
function rampFor(v){ if(v===null||v===undefined) return "var(--deemph)";
  const i=Math.max(0,Math.min(RAMP.length-1,Math.round((v-65)/6))); return RAMP[i]; }
function chartLandscape(selG,pts){
  const s=$("c6");clear(s);
  const keys=Object.keys(B.groups);
  const last=g=>{const f=B.groups[g].alloc; return f[f.length-1];};
  keys.sort((a,b)=>{
    const av=lastCut(a), bv=lastCut(b);
    if(av===null&&bv===null) return last(b)-last(a);
    if(av===null) return 1; if(bv===null) return -1;
    return av-bv || last(b)-last(a);});
  const ML=176,MR=14,MT=22,rh=16,W=520;
  const H=MT+keys.length*rh+10;
  s.setAttribute("viewBox","0 0 "+W+" "+H);
  const cw=(W-ML-MR)/B.rounds.length;
  B.rounds.forEach((r,i)=>{const t=el("text",{x:ML+cw*(i+.5),y:MT-8,class:"tick","text-anchor":"middle"});
    t.textContent=RL[r];s.appendChild(t);});
  panel(s,"f");
  keys.forEach((gk,ri)=>{
    const G=B.groups[gk], y=MT+ri*rh, on=(gk===selG);
    const lt=el("text",{x:ML-8,y:y+rh/2,class:"rowlab"+(on?" on":""),"text-anchor":"end"});
    lt.textContent=(G.name.length>30?G.name.slice(0,29)+"…":G.name);s.appendChild(lt);
    B.rounds.forEach((r,ci)=>{
      const v=cutOf(gk,r);
      const rect=el("rect",{x:ML+cw*ci,y:y+1,width:cw,height:rh-2,rx:2,fill:rampFor(v),class:"cell"});
      s.appendChild(rect);
      hover(rect,"<b>"+(v===null?"no invitations":v+" points")+"</b><span>"+G.name+"</span><span>"+RL[r]+"</span>");
      rect.addEventListener("click",()=>{
        const first=OCCS.find(o=>B.occ[o].g===gk); if(first){S.occ=first;$("occ").value=first;render();
          window.scrollTo({top:0,behavior:"smooth"});}});});
    if(on){s.appendChild(el("rect",{x:ML,y:y+1,width:W-ML-MR,height:rh-2,rx:2,fill:"none",
      stroke:"var(--ink)","stroke-width":2,"pointer-events":"none"}));}});
}
function cutOf(gk,round){
  let best=null;
  for(const o of OCCS){const oc=B.occ[o]; if(oc.g!==gk) continue;
    const r=oc.rounds.find(x=>x.r===round); if(r&&r.b!==null) best=(best===null?r.b:Math.min(best,r.b));}
  return best;
}
function lastCut(gk){ return cutOf(gk,B.rounds[B.rounds.length-1]); }
/* ---------- chart 7: scatter pool vs cut-off ---------- */
function chartScatter(selG,pts){
  const s=$("c7");clear(s);
  const W=520,H=300,ML=40,MR=18,MT=18,MB=44,pw=W-ML-MR,ph=H-MT-MB;
  const pts2=[];
  for(const gk in B.groups){
    const G=B.groups[gk], pool=Object.values(G.dist).reduce((a,b)=>a+b,0), c=lastCut(gk);
    if(pool<1) continue;
    pts2.push({gk:gk,name:G.name,pool:pool,cut:c,alloc:G.alloc[G.alloc.length-1]});}
  const xs=pts2.map(p=>Math.log10(Math.max(1,p.pool)));
  const x0=Math.floor(Math.min(...xs)),x1=Math.ceil(Math.max(...xs));
  const cuts=pts2.filter(p=>p.cut!==null).map(p=>p.cut);
  const y0=Math.min(60,...cuts), y1=Math.max(100,...cuts);
  const X=v=>ML+pw*(Math.log10(Math.max(1,v))-x0)/(x1-x0), Y=v=>MT+ph*(1-(v-y0)/(y1-y0));
  for(let v=Math.ceil(y0/10)*10;v<=y1;v+=10){
    s.appendChild(el("line",{x1:ML,y1:Y(v),x2:W-MR,y2:Y(v),class:"gl"}));
    const t=el("text",{x:ML-7,y:Y(v)+3.5,class:"tick","text-anchor":"end"});t.textContent=v;s.appendChild(t);}
  for(let e=x0;e<=x1;e++){const xv=Math.pow(10,e);
    const t=el("text",{x:X(xv),y:H-MB+16,class:"tick","text-anchor":"middle"});
    t.textContent=xv>=1000?(xv/1000)+"k":xv;s.appendChild(t);}

  axisTitle(s,W,H,MB,"EOIs in the group's pool (log scale)","minimum points invited");panel(s,"g");
  if(pts>=y0&&pts<=y1){
    s.appendChild(el("line",{x1:ML,y1:Y(pts),x2:W-MR,y2:Y(pts),class:"refl"}));
    const t=el("text",{x:W-MR,y:Y(pts)-6,class:"reft","text-anchor":"end"});t.textContent="your "+pts+" pts";s.appendChild(t);}
  const maxA=Math.max(...pts2.map(p=>p.alloc||1));
  pts2.filter(p=>p.cut!==null).sort((a,b)=>b.pool-a.pool).forEach(p=>{
    const r=Math.max(3.5,Math.min(13,Math.sqrt((p.alloc||1)/maxA)*15));
    const on=p.gk===selG;
    const c=el("circle",{cx:X(p.pool),cy:Y(p.cut),r:r,class:"pt"+(on?" on":""),
      fill:on?"var(--series)":"var(--series-soft)","fill-opacity":on?1:.85});
    if(!on)c.setAttribute("fill","var(--series)"),c.setAttribute("fill-opacity",".55");
    s.appendChild(c);
    hover(c,"<b>"+p.cut+" points</b><span>"+p.name+"</span><span>"+fmt(p.pool)+" in pool &middot; "+fmt(p.alloc)+" invited</span>");
    c.addEventListener("click",()=>{const f=OCCS.find(o=>B.occ[o].g===p.gk);
      if(f){S.occ=f;$("occ").value=f;render();window.scrollTo({top:0,behavior:"smooth"});}});});
}


/* ---------- exact queue table ---------- */
function queueTable(o,g,pts){
  const tb=document.querySelector("#qt tbody");tb.innerHTML="";
  const my=Math.round(pts/5)*5;
  const keys=new Set([...Object.keys(o.dist).map(Number),...(g?Object.keys(g.dist).map(Number):[])]);
  const list=[...keys].filter(k=>k>=my).sort((a,b)=>b-a);
  let run=0;
  list.forEach(k=>{
    const oc=o.dist[k]||0, gc=(g&&g.dist[k])||0;
    run+=gc;
    const tr=document.createElement("tr");
    const mine=(k===my); if(mine)tr.className="hl";
    const cells=[k+(mine?" (you)":""),fmt(oc),fmt(gc),fmt(run),""];
    cells.forEach((c,i)=>{const td=document.createElement("td");
      if(i===4){const sp=document.createElement("span");
        sp.className="pill "+(k>my?"crit":"warn");
        sp.textContent=k>my?"ahead on points":"ahead on date";
        td.appendChild(sp);} else td.textContent=c;
      tr.appendChild(td);});
    tb.appendChild(tr);});
  const tr=document.createElement("tr");
  const td=document.createElement("td");td.colSpan=3;
  td.innerHTML="<b>Total ahead of you in the unit group</b>";
  const td2=document.createElement("td");td2.innerHTML="<b>"+fmt(run)+"</b>";
  const td3=document.createElement("td");
  const al=g?g.alloc[g.alloc.length-1]:0;
  const sp=document.createElement("span");sp.className="pill "+(al>=run?"good":"crit");
  sp.textContent=al>=run?"last round reached "+fmt(al):"last round reached only "+fmt(al);
  td3.appendChild(sp);
  tr.appendChild(td);tr.appendChild(td2);tr.appendChild(td3);tb.appendChild(tr);
  $("h8n").textContent=fmt(run)+" ahead in "+o.g;
}
/* ---------- policy table ---------- */
function policyTable(){
  const P=B.policy; if(!P) return;
  const rows=[["Skilled Independent (189)",P.places["2025-26"],P.places["2026-27"]],
    ["State/Territory Nominated (190)",P.nominated["2025-26"],P.nominated["2026-27"]],
    ["Regional (491)",P.regional_cut["2025-26"],P.regional_cut["2026-27"]],
    ["Employer Sponsored",P.employer["2025-26"],P.employer["2026-27"]]];
  const tb=document.querySelector("#pt tbody");tb.innerHTML="";
  rows.forEach(([lab,a,b])=>{
    const pc=(b/a-1)*100, tr=document.createElement("tr");
    [lab,fmt(a),fmt(b),""].forEach((c,i)=>{const td=document.createElement("td");
      if(i===3){const sp=document.createElement("span");
        sp.className="pill "+(pc>1?"good":pc<-1?"crit":"n");
        sp.textContent=(pc>0?"+":"")+pc.toFixed(0)+"%";td.appendChild(sp);}
      else td.textContent=c;tr.appendChild(td);});
    tb.appendChild(tr);});
  $("pnote").innerHTML="The 189 program grew <b>"+
    ((P.places["2026-27"]/P.places["2025-26"]-1)*100).toFixed(1)+"%</b>. Across 2025&ndash;26 the Department issued "+
    "<b>"+P.ratio.toFixed(2)+"</b> invitations per place (not every invitation becomes a visa), so "+
    fmt(P.places["2026-27"])+" places implies roughly <b>"+fmt(P.projected_invitations)+
    "</b> invitations in 2026&ndash;27 &mdash; about <b>"+fmt(P.per_round["3"])+
    "</b> per round at the observed cadence of three rounds a year. That is why 10,000 is the default scenario above. "+
    "Regional was cut 57%, which this model does not predict but is the clearest route by which the 189 pool could "+
    "swell faster than it has: it would appear in later snapshots, not in today's forecast.";
}

/* ---------- render ---------- */
function render(){
  const o=B.occ[S.occ]; if(!o) return;
  const g=B.groups[o.g]; const pts=S.pts; const size=B.sizes[S.szi];
  const last=o.rounds[o.rounds.length-1];
  const fc=g?g.fc[S.szi]:null;
  const v=fcVerdict(fc,pts);
  const P=pClear(fc,pts), bb=pBand(fc);
  const band = P===null?null:(P>=.8?"good":P>=.5?"warn":"crit");
  $("flag").className="vflag "+(band||"crit");
  $("flag").textContent = P===null ? "✕ No forecast available"
    : (P>=.8?"✓ Likely invited":P>=.5?"! Could go either way":"✕ Unlikely at this score");
  $("hero").textContent = P===null ? "—" : Math.round(P*100)+"%";
  $("vsub").innerHTML = P===null
    ? "This occupation received no invitations in the most recent round, so there is no allocation share to forecast from. The round-by-round record below still applies."
    : "is the probability that the cut-off for <b>"+o.g+" "+(g?g.name.replace(/^\d+\s/,""):"")+
      "</b> reaches <b>"+pts+" points</b> in a round of "+fmt(size)+
      ", <b>if a round is held</b>. Central forecast <b>"+fc+" points</b> (80% interval "+bb[0]+"–"+bb[1]+
      "). Calibrated on how wrong this same method was on the two most recent held-out rounds, not on a judgement call.";
  const ge=g?Object.keys(g.dist).map(Number).filter(k=>k>=pts).reduce((a,k)=>a+g.dist[k],0):0;
  const al=g?g.alloc[g.alloc.length-1]:0;
  const ratio=ge>0?al/ge:0;
  $("mfill").style.width=Math.max(2,Math.min(100,ratio*50))+"%";
  $("mleft").textContent="last round allocated "+fmt(al)+" to this group";
  $("mright").textContent=fmt(ge)+" sit at "+pts+"+ · "+(ge>0?ratio.toFixed(2)+"×":"—");
  $("vside").innerHTML="";
  const rows=[["Pool in this occupation",fmt(o.pool)],
    ["At your score",fmt(o.dist[Math.round(pts/5)*5]||0)],
    ["Unit group",o.g],["Group allocation last round",fmt(al)],
    ["Ahead of you in the group",fmt(ge)]];
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
  $("h1n").textContent=S.occ; $("h2n").textContent=o.g+" group";
  $("h3n").textContent=fmt(o.pool)+" EOIs"; $("h4n").textContent=o.g+" group";
  chartRounds(o,pts);chartForecast(g,pts);chartPool(o,pts);chartQueue(g,pts);
  chartMatrix(g,pts);chartLandscape(o.g,pts);chartScatter(o.g,pts);
  queueTable(o,g,pts);policyTable();
  $("h5n").textContent=o.g+" group";
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
  $("allN").textContent=list.length+" occupations";
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
  function show(f){box.innerHTML="";
    const m=OCCS.filter(o=>o.toLowerCase().includes(f.toLowerCase())).slice(0,60);
    m.forEach(o=>{const d=document.createElement("div");d.textContent=o;d.setAttribute("role","option");
      if(o===S.occ)d.className="sel";
      d.addEventListener("mousedown",e=>{e.preventDefault();S.occ=o;inp.value=o;box.classList.remove("on");render();});
      box.appendChild(d);});
    box.classList.toggle("on",m.length>0);}
  inp.addEventListener("focus",()=>show(""));
  inp.addEventListener("input",()=>show(inp.value));
  inp.addEventListener("blur",()=>setTimeout(()=>box.classList.remove("on"),120));
  inp.value=S.occ;
}
B.sizes.forEach((s,i)=>{const o=document.createElement("option");o.value=i;o.textContent=s.toLocaleString();
  if(i===2)o.selected=true;$("sz").appendChild(o);});
$("pts").addEventListener("input",e=>{S.pts=+e.target.value||0;render();});
$("sz").addEventListener("change",e=>{S.szi=+e.target.value;render();});
initCombo();render();
</script>
"""
