"""The probability model, in JavaScript — the ONE copy.

Both the explorer pages and the method paper interpolate this string, so a change
to the model cannot reach one page and miss the other. The paper's worked example
walks through these very functions.
"""
MODEL_JS = r"""
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
/* The round-size distribution, pushed through equation 1 into a distribution of PLACES
   for one group. This is the quantity a reader actually wants out of step 2, and the
   line alone never stated it. */
function placesDist(g){
  if(!g||g.share<=0) return null;
  const by={}; let w=0;
  B.rs.grid.forEach((N,i)=>{
    const pl=Math.round(g.share*N*B.meta.fr), d=B.rs.dens[i];
    by[pl]=(by[pl]||0)+d; w+=d;});
  if(w<=0) return null;
  const vals=Object.keys(by).map(Number).sort((a,b)=>a-b);
  let m=0; vals.forEach(v=>m+=v*by[v]/w);
  let c=0, q={};
  vals.forEach(v=>{c+=by[v]/w;
    if(q.p10===undefined&&c>=.10) q.p10=v;
    if(q.p50===undefined&&c>=.50) q.p50=v;
    if(q.p90===undefined&&c>=.90) q.p90=v;});
  let sd=0; vals.forEach(v=>sd+=by[v]/w*(v-m)*(v-m));
  return {vals:vals, dens:vals.map(v=>by[v]/w), mean:m, sd:Math.sqrt(sd),
          p10:q.p10, p50:q.p50, p90:q.p90, max:Math.max(...vals.map(v=>by[v]/w))};
}

/* The chance of an invitation AT ONE ROUND SIZE - the same quantity as the headline,
   just not yet averaged over sizes. Anything the page labels "your chance" must use
   this: pClear alone omits the skip risk and reads well over ten points too high. */
/* The single round size to use wherever one is needed: the median of the distribution,
   not an arbitrary entry of the published grid. The page used B.sizes[2] = 10,000 in
   eight places while the headline averaged over everything. */
function SZ(){ return B.rs.q50; }
function fcAt(g){ return cutoffAt(g,SZ()); }

/* Density-weighted mean and standard deviation of q(N) across the round-size
   distribution - the 1-sigma spread the round size alone puts on a quantity. */
function spread(fn){
  let m=0,w=0;
  B.rs.grid.forEach((sz,i)=>{const q=fn(sz); if(q!==null){m+=B.rs.dens[i]*q;w+=B.rs.dens[i];}});
  if(w<=0) return null;
  m/=w;
  let v=0;
  B.rs.grid.forEach((sz,i)=>{const q=fn(sz); if(q!==null)v+=B.rs.dens[i]*(q-m)*(q-m);});
  return {mean:m, sd:Math.sqrt(v/w)};
}
function pAt(g,pts,gk,size){
  const q=pClear(cutoffAt(g,size),pts);
  return q===null?null:q*(1-pZero(gk||CURG));
}
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
"""
