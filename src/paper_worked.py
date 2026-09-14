"""The worked example: the same functions the explorer runs, narrated one step at a time.

It calls the shared model (model_js.MODEL_JS) rather than reimplementing it, so the
arithmetic shown here is by construction the arithmetic that produced the headline.
"""
WORKED_HTML = r"""
<div class="wk">
  <div class="wkin">
    <div><label for="wocc">Occupation</label>
      <input id="wocc" list="wopts" autocomplete="off" spellcheck="false"></div>
    <datalist id="wopts"></datalist>
    <div><label for="wpts">Points</label>
      <input id="wpts" type="number" min="65" max="100" step="5" value="85" style="min-width:92px"></div>
    <div><label for="wdoe">Date of effect</label>
      <select id="wdoe"><option value="">not given — assume last in band</option></select></div>
  </div>
  <p class="note" style="margin:2px 0 0;font-size:12px;color:var(--muted)">
    Every number below is recomputed by the same functions the result page runs.</p>
</div>
<div id="wsteps"></div>
<div class="wkout" id="wres"></div>
"""

WORKED_JS = r"""
(function(){
  var $w=function(i){return document.getElementById(i)};
  if(!$w("wsteps")) return;
  var OCCS=Object.keys(B.occ).sort();
  var dl=$w("wopts");
  OCCS.forEach(function(k){var o=document.createElement("option");o.value=k;dl.appendChild(o);});
  var sel=$w("wdoe");
  (B.doe_months||[]).forEach(function(m){var o=document.createElement("option");o.value=m;o.textContent=m;sel.appendChild(o);});
  $w("wocc").value = OCCS.indexOf("234914 Physicist")>=0 ? "234914 Physicist" : OCCS[0];

  function fmt(n){return Number(n).toLocaleString("en-AU")}
  function pc(x){return (x*100).toFixed(1)+"%"}
  function step(n,h,body,calc){
    return '<div class="step"><div class="stepn">'+n+'</div><div><div class="steph">'+h+'</div>'+
           '<div class="stepb">'+body+(calc?'<div class="calc">'+calc+'</div>':'')+'</div></div></div>';
  }
  function run(){
    var key=$w("wocc").value, pts=Math.round((+$w("wpts").value||65)/5)*5;
    var o=B.occ[key];
    if(!o){$w("wsteps").innerHTML='<p class="stepb">Pick an occupation from the list.</p>';
           $w("wres").innerHTML="";return;}
    var gk=o.g, g=B.groups[gk];
    S.occ=key; S.pts=pts; S.doe=$w("wdoe").value||null; CURG=gk;
    var out="";

    // 1 - the unit group
    out+=step(1,"Find the unit group the occupation sits in",
      "Invitations are rationed at the ANZSCO four-digit unit group, not at the six-digit "+
      "occupation. <b>"+key+"</b> sits in <b>"+g.name+"</b>, so everyone in that group competes together.",
      "occupation "+key+" &rarr; unit group <span class=\"res\">"+gk+"</span>");

    // 2 - the pool
    var scores=Object.keys(g.dist).map(Number).sort(function(a,b){return b-a});
    var total=scores.reduce(function(a,s){return a+g.dist[s]},0);
    var atOrAbove=scores.filter(function(s){return s>=pts}).reduce(function(a,s){return a+g.dist[s]},0);
    var above=scores.filter(function(s){return s>pts}).reduce(function(a,s){return a+g.dist[s]},0);
    out+=step(2,"Count who is waiting, and how many outrank you",
      "The pool is everyone with a live EOI in the group, counted at each score. Only people "+
      "at or above your score can take a place before you do.",
      "pool n<sub>g</sub> = "+fmt(total)+" &nbsp;·&nbsp; strictly above "+pts+" pts = <span class=\"res\">"+
      fmt(above)+"</span> &nbsp;·&nbsp; at "+pts+" pts = "+fmt(g.dist[pts]||0));

    // 3 - share
    var lastAlloc=g.alloc[g.alloc.length-1];
    out+=step(3,"Work out the group&rsquo;s share of a round (equation 1)",
      "The share is what the group took in the most recent round, divided by everything issued "+
      "that round. It is measured on single-leg invitations, so it has to be applied to the "+
      "single-leg part of a round: &#966; = "+B.meta.fr.toFixed(4)+".",
      "&#963;<sub>g</sub> = "+fmt(lastAlloc)+" &divide; total = <span class=\"res\">"+
      (g.share*100).toFixed(3)+"%</span>");

    // 4 - allocation and cut-off at the median round
    var N=B.rs.q50, A=Math.round(g.share*N*B.meta.fr), c=cutoffAt(g,N);
    out+=step(4,"Turn a round size into a cut-off (equations 1 and 2)",
      "Take a round of the most likely size, give the group its share, then walk down the pool "+
      "from the top until those places run out. The score you stop on is the cut-off.",
      "A<sub>g</sub>("+fmt(N)+") = "+(g.share*100).toFixed(3)+"% &times; "+fmt(N)+" &times; "+
      B.meta.fr.toFixed(4)+" = "+fmt(A)+" places &nbsp;&rarr;&nbsp; c<sub>g</sub> = <span class=\"res\">"+
      (c===null?"—":c+" pts")+"</span>");

    // 5 - the residual distribution
    var le=pLE(c,pts), lt=pLE(c,pts-5), eq=Math.max(0,le-lt);
    out+=step(5,"Convert the cut-off into a probability (equation 3)",
      "The cut-off is a forecast, not a fact. Its error is read straight off "+B.unc.n+
      " held-out rounds rather than assumed normal: count what fraction of those errors would "+
      "still put the cut-off at or below your score.",
      "P(c &lt; "+pts+") = <span class=\"res\">"+pc(lt)+"</span> &nbsp;·&nbsp; P(c = "+pts+
      ") = <span class=\"res\">"+pc(eq)+"</span>");

    // 6 - rationing inside the band
    var sh=aheadShare(gk,pts), reach=(sh===null?0:Math.max(0,1-sh));
    out+=step(6,"Handle the case where the cut-off lands on your own score (equation 4)",
      (S.doe===null
        ? "When the cut-off lands exactly on your band, places inside that band go by date of "+
          "effect. With no date given the model assumes the worst — last in the band — so this "+
          "term contributes nothing."
        : "Places inside the boundary band go by date of effect. With "+S.doe+", "+pc(sh)+
          " of that band is dated ahead of you, so you reach the front of it "+pc(reach)+" of the time."),
      "P<sub>clear</sub> = "+pc(lt)+" + "+pc(eq)+" &times; "+pc(reach)+" = <span class=\"res\">"+
      pc(pClear(c,pts))+"</span>");

    // 7 - marginalise
    var cond=0,w=0;
    B.rs.grid.forEach(function(sz,i){var p=pClear(cutoffAt(g,sz),pts);
      if(p!==null){cond+=B.rs.dens[i]*p;w+=B.rs.dens[i];}});
    cond = w>0 ? cond/w : 0;
    out+=step(7,"Average over every round size that could happen (equation 5)",
      "Nobody knows how large the next round will be. Rather than pick one, the model computes "+
      "the probability at each size and weights it by how likely that size is — the "+
      "distribution in chapter 7, with a median of "+fmt(B.rs.q50)+".",
      "P<sub>cond</sub> = &Sigma; f(N) &times; P<sub>clear</sub>(N) = <span class=\"res\">"+pc(cond)+"</span>");

    // 8 - skip risk
    var z=pZero(gk);
    out+=step(8,"Discount the chance the group is passed over entirely",
      "Some groups receive nothing in a given round. Whether the group was invited last round "+
      "is by far the strongest predictor of that, so the model branches on it: "+
      pc(B.zr.p_zero_given_prev_nonzero)+" if it was, "+pc(B.zr.p_zero_given_prev_zero)+" if it was not. "+
      "This group "+(lastAlloc>0?"was invited last round":"received nothing last round")+".",
      "P = "+pc(cond)+" &times; (1 &minus; "+pc(z)+") = <span class=\"res\">"+pc(cond*(1-z))+"</span>");

    $w("wsteps").innerHTML=out;
    var P=pMarginal(g,pts,gk);
    $w("wres").innerHTML = P===null
      ? '<b>—</b><span>No forecast: this group took no invitations in the most recent round, so it has no share to apply.</span>'
      : '<b>'+Math.round(P*100)+'%</b><span>chance of an invitation for '+key+' at '+pts+
        ' points, conditional on a round being held.</span>';
  }
  ["wocc","wpts","wdoe"].forEach(function(i){
    var e=$w(i); if(e){e.addEventListener("input",run); e.addEventListener("change",run);}});
  run();
})();
"""
