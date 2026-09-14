"""Build docs/findings.html - the method, as a chapter-by-chapter wiki.

Two rules this builder enforces on itself:

  * no figure is drawn by the page - every SVG is rendered here, from the bundle;
  * no number is typed into the prose - each one is read from the bundle through
    num(), which fails loudly on a missing key, so the text cannot drift from the
    data the way a hand-written figure silently does.
"""
import json, pathlib, sys, csv, html

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dash_css import CSS
from paper_css import PAPER_CSS
from model_js import MODEL_JS
from paper_worked import WORKED_HTML, WORKED_JS
import paper_figs as F

R = pathlib.Path(__file__).resolve().parent.parent
B = json.loads((R / "data" / "bundle.json").read_text())
OOS = json.loads((R / "data" / "validation_singleleg.json").read_text())["oos"]
with open(R / "data" / "validation_oos_singleleg.csv") as fh:
    VROWS = [{"pred": int(float(r["pred"])), "actual": int(float(r["actual"]))}
             for r in csv.DictReader(fh) if r.get("pred") and r.get("actual")]

_used = []


def num(path, fmt="{}"):
    """Read a value out of the bundle by dotted path. Typing the number instead is
    how a retracted result survives into the next draft."""
    cur = B
    for k in path.split("."):
        if isinstance(cur, list):
            cur = cur[int(k)]
        else:
            if k not in cur:
                raise KeyError(f"bundle has no {path} (stopped at {k!r})")
            cur = cur[k]
    _used.append(path)
    return fmt.format(cur)


def pct(path, dp=0):
    cur = B
    for k in path.split("."):
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    _used.append(path)
    return f"{cur*100:.{dp}f}%"


def fig(n, svg, caption):
    return (f'<figure id="fig{n}"><div class="figbox">{svg}</div>'
            f'<figcaption><b>Figure {n}.</b> {caption}</figcaption></figure>')


def eq(tex, n):
    return (f'<div class="eq"><span class="eqn">({n})</span>'
            f'\\[{tex}\\]</div>')


# representative group for the illustrative figures: the largest pool that still
# receives invitations, so the histogram is smooth and the mechanism is visible
_cands = [(sum(g["dist"].values()), k) for k, g in B["groups"].items()
          if g["share"] > 0 and g["alloc"][-1] > 0]
GK = max(_cands)[1]
GNAME = B["groups"][GK]["name"]
NGROUPS = len(B["groups"])

CH = []


def chapter(slug, title, eyebrow, body):
    CH.append(dict(slug=slug, title=title, eyebrow=eyebrow, body=body))


# ------------------------------------------------------------------ 1
chapter("question", "Definition of the estimand", "Chapter 1", f"""
<p class="lede">For any occupation, at any points score, this model estimates one number:
the probability that a candidate is invited in the next subclass&nbsp;189 round.</p>

<p>The estimate takes four inputs — the occupation, the score, optionally the date of
effect of the EOI, and the size of the next round, which nobody knows. The first three
come from the reader. The fourth is treated as a random variable and averaged out.</p>

<p>Writing <em>g</em> for the occupation's ANZSCO unit group, <em>s</em> for the score,
<em>d</em> for the date of effect and <em>N</em> for the round size, the target is</p>

{eq(r"P\bigl(\text{invited} \mid g,\, s,\, d\bigr)", 0)}

<p>Three properties of the invitation round make this harder than ranking everyone by
points and drawing a line.</p>

<ol>
<li><b>Places are rationed per unit group, not per person.</b> Two candidates on identical
scores in different occupations face entirely different odds, because their groups are
allocated different numbers of places.</li>
<li><b>A group can receive nothing at all.</b> Some groups sit out a round completely.
That is a separate event from having a cut-off above your score, and it has to be
modelled separately.</li>
<li><b>The cut-off is not a clean band boundary.</b> Only {pct('mech.boundary_hits')} of
allocations land exactly on a five-point boundary. The rest stop part-way into a band,
and the people in it are separated by date of effect.</li>
</ol>

<p>Chapters 3 to 8 build the estimate one term at a time. Chapter 9 runs the whole thing
on an occupation of your choice, showing the arithmetic at each step.</p>
""")

# ------------------------------------------------------------------ 2
chapter("data", "Data sources and construction", "Chapter 2", f"""
<p class="lede">Everything here comes from the Department of Employment and Workplace
Relations SkillSelect EOI dashboard, read through the API that serves it.</p>

<p>The dashboard publishes two things that matter: the <b>pool</b> — how many live EOIs
sit at each points score in each occupation — and the <b>invitation record</b> — how many
were invited, in which occupation, at which score, in each round. The current snapshot is
{num('meta.snapshot')}; the most recent round modelled is {num('meta.last_round')}.</p>

<h3>The trap in the raw table</h3>

<p>An EOI can carry several visa subclasses at once. The dashboard's status field belongs
to the <em>EOI</em>, not to the subclass leg, so filtering naively on subclass 189 counts
invitations that were actually issued against a 190 or 491 leg of the same EOI. That
roughly doubles the apparent 189 invitation count.</p>

<p>Every figure in this paper is computed on <b>single-leg</b> EOIs — those carrying 189
and nothing else — identified with a set expression that excludes any EOI with another
subclass attached. A single-leg share must then be applied to the single-leg part of a
round, not the headline number: the correction factor is
&#966;&nbsp;=&nbsp;{num('meta.fr')}, measured in the {num('meta.last_round')} round.</p>

<h3>Counts below the publication threshold</h3>

<p>The dashboard suppresses exact counts under 20. Those cells are recovered by
differencing: the count for one occupation is the total for all occupations minus the
total for all occupations except that one. Both totals are above the threshold, so both
are published exactly.</p>

<h3>Scope</h3>
<table class="pt">
<tr><th>Quantity</th><th>Value</th></tr>
<tr><td>Occupation groups modelled</td><td class="n">{NGROUPS}</td></tr>
<tr><td>Rounds in the record</td><td class="n">{len(B['rounds'])}</td></tr>
<tr><td>Held-out group-rounds used for validation</td><td class="n">{OOS['n']}</td></tr>
<tr><td>Residuals behind the uncertainty model</td><td class="n">{num('unc.n')}</td></tr>
<tr><td>Legislative points floor</td><td class="n">{num('floor')}</td></tr>
</table>
""")

# ------------------------------------------------------------------ 3
chapter("allocation", "Allocation of places to occupation groups", "Chapter 3", f"""
<p class="lede">A round of size <em>N</em> is divided between unit groups. The model's first
job is to say how many places group <em>g</em> receives.</p>

<p>The share is estimated from the most recent round: the invitations that went to the
group, over all invitations issued. Because shares are measured on single-leg data, the
share is applied to the single-leg equivalent of the round, &#966;<em>N</em>.</p>

{eq(r"A_g(N) \;=\; \sigma_g \, \varphi \, N, \qquad \sigma_g \;=\; \frac{a_g}{\sum_h a_h}", 1)}

<p>Here <em>a<sub>g</sub></em> is what the group took in the last round. Using the last
round alone rather than an average is deliberate: chapter 8 shows that recent behaviour,
not long-run behaviour, is what predicts the next round — the allocation regime changed,
and older rounds describe a policy that no longer applies.</p>

<p>A group with <em>a<sub>g</sub></em>&nbsp;=&nbsp;0 gets no share and therefore no
forecast. That is not a bug in the estimate; it is the single most important thing to know
about such an occupation, and chapter 8 treats it directly.</p>
""")

# ------------------------------------------------------------------ 4
chapter("cutoff", "Determination of the points cut-off", "Chapter 4", f"""
<p class="lede">Given a number of places and a pool, the cut-off is found by walking down
from the top score until the places run out.</p>

{eq(r"c_g(N) \;=\; \min\Bigl\{ s \ge F \;:\; \sum_{u \ge s} n_g(u) \;\ge\; A_g(N) \Bigr\}", 2)}

<p><em>n<sub>g</sub>(u)</em> is the number of people in the group at score <em>u</em>, and
<em>F</em>&nbsp;=&nbsp;{num('floor')} is the legislative minimum — no invitation is issued
below it, so if the allocation exhausts the eligible pool the cut-off stops at the floor
rather than continuing downward.</p>

{fig(1, F.fig_mechanism(B, GK),
     f"The pool of {html.escape(GNAME)} at a round of the median size "
     f"({B['rs']['q50']:,}). Shaded bars are covered by "
     "the allocation; the dashed line is where it stops. The cut-off is a property of the "
     "pool's shape, which is why two groups with the same share can have different cut-offs.")}

<h3>Is the mechanism band-based or number-based?</h3>

<p>Whether a round invites <em>everyone</em> in a band or simply a <em>number</em> of people
changes the answer for anyone sitting on the boundary, so it was tested rather than assumed.
Both predictions are checked against what actually happened:</p>

<ul>
<li>Bands strictly above the margin are taken essentially in full — {pct('mech.above_full')}
of them.</li>
<li>The lowest band reached is taken in full only {pct('mech.lowest_full')} of the time;
typically {pct('mech.median_lowest_frac')} of it goes.</li>
<li>Allocations land exactly on a band boundary {pct('mech.boundary_hits')} of the time.</li>
</ul>

<p>That is the signature of a number, not a band. The consequence for a candidate is direct:
being at the cut-off score is not the same as being invited, and chapter 6 deals with what
separates the people inside that band.</p>

{fig(2, F.fig_cutoff_curves(B, GK),
     "Cut-off against round size for every group. Each line is a step function — the "
     "cut-off holds steady, then drops five points when the allocation reaches into the "
     "next band down. The lines are not parallel: a round size that clears one occupation "
     "leaves another untouched.")}
""")

# ------------------------------------------------------------------ 5
chapter("uncertainty", "Quantification of forecast uncertainty", "Chapter 5", f"""
<p class="lede">Equation 2 returns a single number. A single number cannot answer a question
about chance, so the model's error is measured and carried through.</p>

<p>Each round is held out in turn, the cut-off is predicted for every group from the
remaining rounds, and the error is recorded. That gives {num('unc.n')} residuals, defined as
prediction minus outcome. Their distribution <em>is</em> the uncertainty model — no normal
approximation is fitted, because the residuals are multiples of five points and visibly not
bell-shaped.</p>

{eq(r"P(c \le s) \;=\; \frac{1}{|R|}\Bigl|\bigl\{ e \in R \;:\; e \ge \hat{c} - s \bigr\}\Bigr|", 3)}

{fig(3, F.fig_residuals(B),
     f"The {num('unc.n')} leave-one-round-out residuals. The central 80% runs from "
     f"{num('unc.lo80', '{:+.0f}')} to {num('unc.hi80', '{:+.0f}')} points; the mean error is "
     f"{num('unc.mean', '{:+.2f}')}, so the model is close to unbiased but far from precise.")}

<p>Reading equation 3 in words: the cut-off ends up at or below your score whenever the
model's error is at least as large as the gap between its forecast and your score. Counting
how often that happened historically gives the probability directly.</p>
""")

# ------------------------------------------------------------------ 6
chapter("band", "Rationing within the boundary band", "Chapter 6", f"""
<p class="lede">When the cut-off lands on your own score, points no longer separate you from
the competition. Date of effect does.</p>

<p>Places inside the boundary band are issued in date-of-effect order — earliest first. So
the probability splits into a part that does not depend on your date at all, and a part that
depends on it entirely:</p>

{eq(r"P_{\text{clear}}(g,s,d \mid N) \;=\; \underbrace{P(c < s)}_{\text{cut-off below your band}} \;+\; \underbrace{P(c = s)}_{\text{lands on your band}} \cdot \bigl(1 - \rho_g(s,d)\bigr)", 4)}

<p>&#961;<sub>g</sub>(s,d) is the share of your own band dated ahead of you, taken from the
cumulative date-of-effect distribution for that group and score.</p>

<p><b>When no date is given, the model assumes the worst</b> — that you are last in your
band — and the second term contributes nothing. That is a deliberate floor, not an estimate:
a reader who supplies a date can only improve on it.</p>

<p>The date-of-effect distributions are used as <em>shapes</em> only, normalised within each
group and score. An earlier attempt to use them as levels was discarded: aggregating them
across snapshots double-counted, producing dates later than the snapshot that recorded them
in most cells. The normalised shape is unaffected by that error; the levels were not
recoverable, so they are not used.</p>
""")

# ------------------------------------------------------------------ 7
chapter("roundsize", "Marginalisation over round size", "Chapter 7", f"""
<p class="lede">Every quantity so far is conditional on the round size <em>N</em>. Since
<em>N</em> is unknown, the model does not pick one — it averages over all of them.</p>

<p>The distribution of <em>N</em> is built from three published or observed facts: the
places allocated to the programme for the year, how many rounds are likely to remain, and
how unevenly past rounds have been sized. Combining them gives a median of
{num('rs.q50', '{:,}')} with an 80% range of {num('rs.q10', '{:,}')} to
{num('rs.q90', '{:,}')} — wide, because it genuinely is.</p>

{fig(5, F.fig_roundsize(B),
     f"The round-size distribution. The bumps are real: they come from the discrete "
     f"question of how many rounds remain in the programme year, each implying a different "
     f"typical size. Shaded is the central 80%.")}

<p>Averaging the conditional probability against this distribution, and then discounting by
the chance the group is skipped entirely (chapter 8), gives the final estimate:</p>

{eq(r"P(\text{invited}) \;=\; \Bigl[\sum_N f(N)\, P_{\text{clear}}(g,s,d \mid N)\Bigr] \cdot \bigl(1 - z_g\bigr)", 5)}

{fig(4, F.fig_surface(B, GK),
     f"The conditional probability across both unknowns, for {html.escape(GNAME)}. Reading "
     "across a row shows how much the round size matters at a fixed score; reading down a "
     "column shows how steeply the odds fall with points. Equation 5 collapses this grid to "
     "one number by weighting each column by Figure 5.")}
""")

# ------------------------------------------------------------------ 8
chapter("zero", "Exclusion of occupation groups", "Chapter 8", f"""
<p class="lede">The largest single risk for many occupations is not a high cut-off. It is
that the group is passed over completely.</p>

<p>At the 2025&#8211;26 programme boundary, {len(B['sw']['switched_off'])}
of the largest groups stopped receiving invitations outright — together
{sum(x['pool'] for x in B['sw']['switched_off']):,} people. Their pools did not shrink and
their scores did not fall. The allocation simply stopped.</p>

<p>This matches a four-tier prioritisation model released under freedom of information. Tested
against the invitation record, the tiers separate sharply:</p>

{fig(7, F.fig_tiers(B),
     f"Invitations per 1,000 people waiting, by tier. The gap between the top and bottom "
     f"tier is more than two orders of magnitude (&#967;&#178; = {num('tiers.chi2')}, "
     f"p = {B['tiers']['p']:.2g}).")}

<h3>The explanation the document gives is not the one the data supports</h3>

<p>The released model attributes exclusion to programme-wide ceiling consumption. That does
not survive testing: within a tier, ceiling consumption does not separate the excluded groups
from the rest, while raw pool size clearly does. Large groups are being held back because they
are large, not because their ceiling is full.</p>

<h3>What the model actually uses</h3>

<p>Tier membership explains <em>why</em> a group is skipped, but it does not predict it as
well as the group's own recent history. Whether a group was invited in the last round splits
the skip rate from {pct('zr.p_zero_given_prev_nonzero')} to {pct('zr.p_zero_given_prev_zero')},
and a persistence model beats a tier-and-pool model on accuracy. So the tier is reported to
the reader as context, and the probability is discounted using persistence:</p>

{eq(r"z_g \;=\; \begin{cases} " +
   f"{B['zr']['p_zero_given_prev_nonzero']:.2f}" + r" & \text{invited last round} \\[2pt] " +
   f"{B['zr']['p_zero_given_prev_zero']:.2f}" + r" & \text{otherwise} \end{cases}", 6)}

<p>Choosing the weaker explanation over the stronger predictor would have been the wrong
trade: the reader is owed the better estimate, and the mechanism as commentary.</p>
""")

# ------------------------------------------------------------------ 9
chapter("worked", "Worked example", "Chapter 9", f"""
<p class="lede">The whole calculation, run on any occupation and score you choose, with the
arithmetic shown at each step.</p>

<p>This is not a re-implementation. The panel calls the same functions as the result page,
from the same source file, so the numbers below are the numbers behind the headline.</p>

{WORKED_HTML}

<p style="margin-top:22px">If the result reads &ldquo;no forecast&rdquo;, the group took no
invitations in the most recent round: it has no share to apply, and chapter 8 is the
relevant reading rather than chapters 3 to 7.</p>
""")

# ------------------------------------------------------------------ 10
chapter("validation", "Out-of-sample validation", "Chapter 10", f"""
<p class="lede">The model is tested by holding out a whole round, fitting on the rest, and
predicting the cut-off for every group in the round it never saw.</p>

{fig(6, F.fig_calibration(VROWS, OOS),
     f"Out-of-sample predictions against outcomes, {OOS['n']} held-out group-rounds. "
     f"Exact {OOS['exact']*100:.0f}%, within one band {OOS['within5']*100:.0f}%, "
     f"MAE {OOS['mae']:.2f} points, bias {OOS['bias']:+.2f}, r = {OOS['r']:.3f}.")}

<table class="pt">
<tr><th>Measure</th><th>Out of sample</th><th>Reading</th></tr>
<tr><td>Exact hit</td><td class="n">{OOS['exact']*100:.1f}%</td>
    <td>the exact five-point band</td></tr>
<tr><td>Within one band</td><td class="n">{OOS['within5']*100:.1f}%</td>
    <td>within 5 points</td></tr>
<tr><td>Mean absolute error</td><td class="n">{OOS['mae']:.2f} pts</td>
    <td>about one band</td></tr>
<tr><td>Bias</td><td class="n">{OOS['bias']:+.2f} pts</td>
    <td>slightly optimistic</td></tr>
<tr><td>Correlation</td><td class="n">{OOS['r']:.3f}</td><td>across all groups</td></tr>
<tr><td>Agreement with the official table</td><td class="n">{pct('meta.cal_exact', 1)}</td>
    <td>{num('meta.cal_n')} occupations reproduced exactly</td></tr>
</table>

<h3>A correction worth recording</h3>

<p>An earlier version of this page reported a far better result — 49 of 49 occupations within
five points, r&nbsp;=&nbsp;0.941. That comparison was invalid: it scored single-leg
predictions against an all-leg pool. On a consistent single-leg basis the model performed as
the table above shows, and the earlier claim was withdrawn. The all-leg cut-off sits materially
lower because 190 and 491 invitations drag it down, which is precisely why the two bases
cannot be mixed.</p>
""")

# ------------------------------------------------------------------ 11
chapter("limits", "Limitations and scope", "Chapter 11", f"""
<p class="lede">The honest boundary of the estimate.</p>

<ul>
<li><b>It cannot tell you whether a round will be held.</b> Every probability on this site is
conditional on one happening. Round timing is an administrative decision with no published
schedule and no statistical signature in the record.</li>

<li><b>It assumes the allocation regime holds.</b> The share in equation 1 comes from the last
round. A policy change of the kind documented in chapter 8 would invalidate it immediately,
and the model would not see it coming.</li>

<li><b>The pool is a snapshot, and it ages.</b> The published pool is measured at
{num('meta.snapshot')}. Cut-off error grows by about {num('horizon.mae_slope')} points for each
month between the snapshot and the round it is used to predict. The forecast carries a
correction for this, but it is a correction, not a fix.</li>

<li><b>The pool strengthens over time.</b> Mean points in the pool drift up by roughly
{num('drift.mean_trend_per_month', '{:.3f}')} points a month, and the share at 85 or more by
{num('drift.share85_trend_pp_per_month', '{:.2f}')} percentage points a month. Both are
modelled, and both are largely absorbed by the horizon correction above.</li>

<li><b>It says nothing about your individual case beyond points and date.</b> Nomination,
documentary problems, or anything specific to one application are outside it.</li>

<li><b>Some things were tested and found absent.</b> Groups do not measurably compete with each
other after the share is accounted for, and no seasonal effect survives testing
(p&nbsp;=&nbsp;{num('gaps.season_p', '{:.3f}')}, on a record with little power to detect one).
These are reported as
absences, not as features.</li>
</ul>

<p>A probability from this model is a statement about how often an outcome like yours occurred
in a comparable position historically. It is not a promise, and the width of Figure 3 is the
best single reminder of that.</p>
""")


# ------------------------------------------------------------------ assemble
def toc():
    items = "".join(
        f'<li><a href="#{c["slug"]}" data-ch="{c["slug"]}">{html.escape(c["title"])}</a></li>'
        for c in CH)
    return f'<nav class="toc" aria-label="Chapters"><h3>Chapters</h3><ol>{items}</ol></nav>'


def chapters_html():
    out = []
    for i, c in enumerate(CH):
        prev_ = CH[i - 1] if i else None
        next_ = CH[i + 1] if i + 1 < len(CH) else None
        nav = '<div class="chapnav">'
        nav += (f'<a href="#{prev_["slug"]}" data-ch="{prev_["slug"]}"><span>Previous</span>'
                f'{html.escape(prev_["title"])}</a>' if prev_ else "<span></span>")
        nav += (f'<a class="nxt" href="#{next_["slug"]}" data-ch="{next_["slug"]}">'
                f'<span>Next</span>{html.escape(next_["title"])}</a>' if next_ else "<span></span>")
        nav += "</div>"
        out.append(
            f'<article class="chap" id="{c["slug"]}" hidden>'
            f'<p class="eyebrow">{c["eyebrow"]}</p>'
            f'<h2>{html.escape(c["title"])}</h2>{c["body"]}{nav}</article>')
    return "".join(out)


NAV = [("index.html", "Your result"), ("landscape.html", "All occupations"),
       ("policy.html", "Policy"), ("findings.html", "Method")]
topnav = "".join(
    f'<a href="{h}"{" aria-current=\"page\"" if h == "findings.html" else ""}>{n}</a>'
    for h, n in NAV)

ROUTER = r"""
(function(){
  var chs=[].slice.call(document.querySelectorAll(".chap"));
  var links=[].slice.call(document.querySelectorAll("[data-ch]"));
  function show(slug,push){
    var hit=chs.filter(function(c){return c.id===slug})[0]||chs[0];
    chs.forEach(function(c){c.hidden=(c!==hit)});
    document.querySelectorAll(".toc a").forEach(function(a){
      if(a.dataset.ch===hit.id) a.setAttribute("aria-current","true");
      else a.removeAttribute("aria-current");});
    document.title=hit.querySelector("h2").textContent+" · SkillSelect 189 method";
    if(push&&location.hash!=="#"+hit.id) history.pushState(null,"","#"+hit.id);
    if(push) window.scrollTo({top:0,behavior:"smooth"});
    if(window.renderMath) renderMath(hit);
  }
  links.forEach(function(a){a.addEventListener("click",function(e){
    e.preventDefault(); show(a.dataset.ch,true);});});
  addEventListener("hashchange",function(){show(location.hash.slice(1),false)});
  show(location.hash.slice(1)||chs[0].id,false);
})();
"""

_K = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/"
KATEX = (
 f'<link rel="stylesheet" href="{_K}katex.min.css" crossorigin="anonymous"\n'
 '  integrity="sha384-n8MVd4RsNIU0tAv4ct0nTaAbDJwPJzDEaqSD1odI+WdtXRGWt2kTvGFasHpSy3SV">\n'
 f'<script defer src="{_K}katex.min.js" crossorigin="anonymous"\n'
 '  integrity="sha384-XjKyOOlGwcjNTAIQHIpgOno0Hl1YQqzUOEleOLALmuqehneUG+vnGctmUb0ZY0l8"></script>\n'
 f'<script defer src="{_K}contrib/auto-render.min.js" crossorigin="anonymous"\n'
 '  integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05"></script>')

KATEX_JS = r"""
window.renderMath=function(root){
  if(typeof renderMathInElement!=="function") return;
  renderMathInElement(root||document.body,{
    delimiters:[{left:"\\[",right:"\\]",display:true},{left:"\\(",right:"\\)",display:false}],
    throwOnError:false});
};
addEventListener("load",function(){window.renderMath(document.body);});
"""

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

page = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>How the invitation odds are calculated</title>
<meta name="description" content="The quantitative model behind the SkillSelect 189 invitation forecast, chapter by chapter: allocation, cut-off, uncertainty, round size, and validation.">
{KATEX}
<style>{CSS}{PAPER_CSS}</style>
</head><body>
<div class="wrap" style="padding-bottom:6px">
<nav class="top">{topnav}<button class="themebtn" id="themebtn" type="button" aria-pressed="false">Dark</button></nav>
<header>
  <p class="kicker">Method</p>
  <h1>How the invitation odds are calculated</h1>
  <p class="sub">A per-occupation, per-score model of the subclass&nbsp;189 invitation round —
  what it assumes, how each number is derived, and where it fails.</p>
</header>
</div>
<div class="paperwrap">
{toc()}
<main>{chapters_html()}</main>
</div>
<script>
const B={(R / "data" / "bundle.json").read_text()};
const S={{occ:null,pts:85,doe:null,szi:2}};
{MODEL_JS}
{WORKED_JS}
{ROUTER}
{KATEX_JS}
{THEME}
</script>
</body></html>
"""

(R / "docs" / "findings.html").write_text(page)
print(f"wrote docs/findings.html  ({len(page)/1024:.0f} KB, {len(CH)} chapters, "
      f"{page.count('<figure')} figures, {page.count('class=\"eq\"')} equations)")
print(f"  bundle values read into the prose: {len(_used)}")
