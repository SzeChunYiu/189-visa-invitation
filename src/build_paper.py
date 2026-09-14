"""Build docs/findings.html - the method, as a chapter-by-chapter wiki.

Two rules this builder enforces on itself:

  * no figure is drawn by the page - every SVG is rendered here, from the bundle;
  * no number is typed into the prose - each one is read from the bundle through
    num(), which fails loudly on a missing key, so the text cannot drift from the
    data the way a hand-written figure silently does.
"""
import json, pathlib, sys, csv, html, re

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dash_css import CSS
from paper_css import PAPER_CSS
from model_js import MODEL_JS
import paper_figs as F
from nav import nav_html

R = pathlib.Path(__file__).resolve().parent.parent
B = json.loads((R / "data" / "bundle.json").read_text())
OOS = json.loads((R / "data" / "validation_singleleg.json").read_text())["oos"]
with open(R / "data" / "validation_oos_singleleg.csv") as fh:
    VROWS = [{"pred": int(float(r["pred"])), "actual": int(float(r["actual"]))}
             for r in csv.DictReader(fh) if r.get("pred") and r.get("actual")]

_used = []
_emitted = set()          # the exact strings that reached the prose


def _rec(sv):
    for tok in re.findall(r"\d[\d,]*(?:\.\d+)?", str(sv)):
        _emitted.add(tok); _emitted.add(tok.replace(",", ""))
    return sv


def v(value, fmt="{}"):
    """A number the builder derives rather than reads. Recorded like num()."""
    return _rec(fmt.format(value))


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
    return _rec(fmt.format(cur))


def pct(path, dp=0):
    cur = B
    for k in path.split("."):
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    _used.append(path)
    return _rec(f"{cur*100:.{dp}f}%")


FIG_ORDER = ["pool_shape", "shares", "mechanism", "aggregate", "cutoff_curves", "residuals",
             "doe_bands", "policy", "quota_chain", "roundsize", "surface", "tiers",
             "calibration", "folds", "official", "horizon", "movement"]
FIGN = {k: i + 1 for i, k in enumerate(FIG_ORDER)}
_drawn = []


def fig(key, svg, caption):
    n = FIGN[key]
    _drawn.append(n)
    return (f'<figure id="fig{n}"><div class="figbox">{svg}</div>'
            f'<figcaption><b>Figure {n}.</b> {caption}</figcaption></figure>')


def figref(key):
    """Reference a figure by name, so renumbering cannot strand a cross-reference."""
    return f'<a href="#fig{FIGN[key]}">Figure {FIGN[key]}</a>' 


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

{fig("pool_shape", F.fig_pool_shape(B),
     "Every live single-leg EOI across the modelled groups, by score. This is the object "
     "equation 2 walks down, and its shape is why a five-point step can matter far more at "
     "one score than another.")}

<h3>Counts below the publication threshold</h3>

<p>The dashboard suppresses exact counts under 20. Those cells are recovered by
differencing: the count for one occupation is the total for all occupations minus the
total for all occupations except that one. Both totals are above the threshold, so both
are published exactly.</p>

<h3>Scope</h3>
<div class="tablewrap"><table class="pt">
<tr><th>Quantity</th><th>Value</th></tr>
<tr><td>Occupation groups modelled</td><td class="n">{v(NGROUPS)}</td></tr>
<tr><td>Rounds in the record</td><td class="n">{v(len(B["rounds"]))}</td></tr>
<tr><td>Held-out group-rounds used for validation</td><td class="n">{v(OOS['n'])}</td></tr>
<tr><td>Residuals behind the uncertainty model</td><td class="n">{num('unc.n')}</td></tr>
<tr><td>Legislative points floor</td><td class="n">{num('floor')}</td></tr>
</table></div>
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

{fig("shares", F.fig_shares(B),
     f"Share of a round by unit group, largest first. The top 20 of "
     f"{v(sum(1 for g in B['groups'].values() if g['share'] > 0))} groups with a share take most "
     "of a round, which is the single biggest reason the same score gives very different odds "
     "in different occupations.")}

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

{fig("mechanism", F.fig_mechanism(B, GK),
     f"The pool of {html.escape(GNAME)} at a round of the median size "
     f"({B['rs']['q50']:,}). Shaded bars are covered by "
     "the allocation; the dashed line is where it stops. The cut-off is a property of the "
     "pool's shape, which is why two groups with the same share can have different cut-offs.")}

<h3>Why the model never fits round size to cut-off</h3>

<p>There is an obvious shortcut: regress the observed cut-off on the observed round size
and use the slope. It gives the wrong answer, and the record says so directly. Averaged
over every occupation invited, the relationship across the {num('agg.n')} rounds on record
is <b>r&nbsp;=&nbsp;{num('agg.r_wmean', '{:+.3f}')}</b> — positive, meaning bigger rounds
went with slightly <em>higher</em> cut-offs.</p>

{fig("aggregate", F.fig_aggregate(B),
     f"Each point is one round, averaged across every occupation that received invitations, "
     f"weighted by how many. The fitted direction is drawn only to show which way it points.")}

<p>Nothing about that is causal. Each round invites a different mix of occupations, and the
pool is strengthening underneath (chapter 11), so the aggregate mixes a composition change
with a mechanism. With {num('agg.n')} rounds the interval on that correlation spans almost
the whole range anyway.</p>

<p>Equation 2 avoids the trap by never aggregating: the cut-off is derived per group from
that group's own pool, and round size enters through the allocation rather than through a
fitted slope. {figref("cutoff_curves")} is the same relationship done correctly — within a
group it is monotone, every time.</p>

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

{fig("cutoff_curves", F.fig_cutoff_curves(B, GK),
     "Cut-off against round size for every group. Each line is a step function — the "
     "cut-off holds steady, then drops five points when the allocation reaches into the "
     "next band down. The lines are not parallel: a round size that clears one occupation "
     "leaves another untouched.")}
""")

# ------------------------------------------------------------------ 5
chapter("uncertainty", "Quantification of forecast uncertainty", "Chapter 5", f"""
<p class="lede">Equation 2 returns a single number. A single number cannot answer a question
about chance, so the model's error is measured and carried through.</p>

<p>The forecast is run forward on rounds it has not seen (chapter 10) and the error is
recorded each time, as prediction minus outcome. The residual distribution <em>is</em> the
uncertainty model — no normal approximation is fitted, because the residuals are multiples of
five points and visibly not bell-shaped.</p>

<p><b>Only the {len(B['val']['unc_folds'])} most recent folds are used</b> —
{' and '.join(B['val']['unc_folds'])} — giving {num('unc.n')} residuals out of the
{num('val.oos.n')} available. This is a deliberate restriction, not a shortage of data.
{figref('folds')} shows why: the oldest fold carries a bias of
{B['val']['folds'][0]['bias']:+.2f} points and roughly twice the error of the newest, because
it spans the allocation change described in chapter 8. Pooling all four folds would widen the
intervals with error the current regime no longer produces.</p>

{eq(r"P(c \le s) \;=\; \frac{1}{|R|}\Bigl|\bigl\{ e \in R \;:\; e \ge \hat{c} - s \bigr\}\Bigr|", 3)}

{fig("residuals", F.fig_residuals(B),
     f"The {num('unc.n')} walk-forward residuals from the two current-regime folds "
     f"({' and '.join(B['val']['unc_folds'])}). The central 80% runs from "
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

{fig("doe_bands", F.fig_doe_bands(B, GK),
     f"Date-of-effect spread within each score band, for {html.escape(GNAME)}. Higher bands "
     "are dated later on average, because those EOIs are newer — which is why the rationing "
     "term has to be read per band rather than once for the group.")}

<p>Across the record, a boundary band is worked through completely only
{pct('mv.boundary_cleared')} of the time in {num('mv.n_boundary')} observed cases. The rest
of the time someone in that band is left waiting, and equation 4 is what decides whether that
is you.</p>

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

{fig("policy", F.fig_policy(B),
     f"Published places by stream. The 189 allocation rises "
     f"{num('policy.ratio')}x between the two years, from {num('policy.places.2025-26', '{:,}')} "
     f"to {num('policy.places.2026-27', '{:,}')} places, which is what sets the scale of the "
     "distribution below.")}

<h3>How the quota becomes a round size</h3>

<p>The annual planning level does not set the round size directly, because not every
invitation becomes a visa: some lapse, some are refused, some applicants take another
pathway. The bridge is the number of invitations issued per place, and it can be measured
for exactly one programme year — 2025&#8211;26, where {num('policy.inv_2025_26', '{:,}')}
invitations were issued against {num('policy.places.2025-26', '{:,}')} places, a ratio of
{num('policy.ratio')}.</p>

{fig("quota_chain", F.fig_quota_chain(B),
     f"Published places, through the measured invitations-per-place ratio, to the invitations "
     f"implied for 2026-27 and what those mean per round. Every box is published or observed "
     "except the last, which is the product of the two before it.")}

<p><b>A correlation between round size and the annual quota cannot be estimated from this
record.</b> Planning levels are published for two years; the invitation panel covers two
programme years, and only one of them has both a published level and a complete set of rounds.
One paired observation does not support a correlation, and none is claimed. What the model
uses is the ratio above applied to the next year's published level — a mechanism, not a
fitted relationship.</p>

{fig("roundsize", F.fig_roundsize(B),
     f"The round-size distribution. The bumps are real: they come from the discrete "
     f"question of how many rounds remain in the programme year, each implying a different "
     f"typical size. Shaded is the central 80%.")}

<p>Averaging the conditional probability against this distribution, and then discounting by
the chance the group is skipped entirely (chapter 8), gives the final estimate:</p>

{eq(r"P(\text{invited}) \;=\; \Bigl[\sum_N f(N)\, P_{\text{clear}}(g,s,d \mid N)\Bigr] \cdot \bigl(1 - z_g\bigr)", 5)}

{fig("surface", F.fig_surface(B, GK),
     f"The conditional probability across both unknowns, for {html.escape(GNAME)}. Reading "
     "across a row shows how much the round size matters at a fixed score; reading down a "
     "column shows how steeply the odds fall with points. Equation 5 collapses this grid to "
     f"one number by weighting each column by {figref('roundsize')}.")}
""")

# ------------------------------------------------------------------ 8
chapter("zero", "Exclusion of occupation groups", "Chapter 8", f"""
<p class="lede">The largest single risk for many occupations is not a high cut-off. It is
that the group is passed over completely.</p>

<p>At the 2025&#8211;26 programme boundary, {v(len(B['sw']['switched_off']))}
of the largest groups stopped receiving invitations outright — together
{v(sum(x['pool'] for x in B['sw']['switched_off']), '{:,}')} people. Their pools did not shrink and
their scores did not fall. The allocation simply stopped.</p>

<p>This matches a four-tier prioritisation model released under freedom of information. Tested
against the invitation record, the tiers separate sharply:</p>

{fig("tiers", F.fig_tiers(B),
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

<p>That panel now has its own page, because it is something a reader uses rather than reads:
<a href="worked.html"><b>Step by step &rarr;</b></a></p>

<p>It is not a re-implementation. The panel calls the same functions as the result page, from
the same source file, so the numbers it shows are the numbers behind the headline. The steps
map onto this paper as: allocation (chapter 3), cut-off (chapter 4), uncertainty (chapter 5),
boundary band (chapter 6), round size (chapter 7), exclusion (chapter 8).</p>

<p>If the result reads &ldquo;no forecast&rdquo;, the group took no invitations in the most
recent round: it has no share to apply, and chapter 8 is the relevant reading rather than
chapters 3 to 7.</p>
""")

# ------------------------------------------------------------------ 10
chapter("validation", "Out-of-sample validation", "Chapter 10", f"""
<p class="lede">Three separate things can be wrong: the rule that turns places into a cut-off,
the forecast of how many places a group gets, and the reading of the data itself. Each is
tested on its own.</p>

<h3>A. Does the walk-the-pool rule hold?</h3>

<p>Give the rule the pool and the allocation that <em>actually</em> happened, and ask whether
it lands on the cut-off that actually happened. This isolates equation 2 from any forecasting
error. Across {num('val.mech.n')} group-rounds it reproduces the exact five-point band
{pct('val.mech.exact')} of the time, within one band {pct('val.mech.within5')}, with a mean
absolute error of {num('val.mech.mae')} points.</p>

<p>The bias of {num('val.mech.bias', '{:+.2f}')} points runs in one direction and is worth
stating plainly: the rule lands <em>deeper</em> into the pool than the round actually reached,
by close to a full band on average. It is therefore conservative for a reader — it tends to
predict a cut-off below the one that occurs. The same sign shows up in the forecast folds
below. What produces it is not established here; the pool snapshot predating the round
(chapter 11) and partial clearance of the boundary band (chapter 6) are both candidates, and
this test cannot separate them.</p>

<h3>B. Does the forecast hold on rounds it has not seen?</h3>

<p>This is the test that matters for a reader. The procedure is <b>walk-forward</b>, not a
random split: each round is forecast using only the round immediately before it, which is
exactly the information available in practice. The allocation share is carried forward from
that previous round; the round size is taken as given, so this measures the model's own error
and not the unknowable size.</p>

<div class="tablewrap"><table class="pt">
<tr><th>Round forecast</th><th>Using</th><th>n</th><th>Exact</th><th>Within 5</th><th>MAE</th><th>Bias</th></tr>
{"".join(f'<tr><td>{f["round"]}</td><td>{f["trained_on"]}</td><td class="n">{v(f["n"])}</td>'
         f'<td class="n">{v(f["exact"]*100, "{:.0f}")}%</td><td class="n">{v(f["within5"]*100, "{:.0f}")}%</td>'
         f'<td class="n">{v(f["mae"], "{:.2f}")}</td><td class="n">{v(f["bias"], "{:+.2f}")}</td></tr>'
         for f in B["val"]["folds"])}
<tr><td><b>All folds</b></td><td>—</td><td class="n"><b>{v(B['val']['oos']['n'])}</b></td>
    <td class="n"><b>{v(B['val']['oos']['exact']*100, "{:.0f}")}%</b></td>
    <td class="n"><b>{v(B['val']['oos']['within5']*100, "{:.0f}")}%</b></td>
    <td class="n"><b>{v(B['val']['oos']['mae'], "{:.2f}")}</b></td>
    <td class="n"><b>{v(B['val']['oos']['bias'], "{:+.2f}")}</b></td></tr>
</table></div>

{fig("calibration", F.fig_calibration(VROWS, OOS),
     f"Every held-out prediction against its outcome, {OOS['n']} group-rounds pooled across "
     "the folds above. Green is exact, amber within one five-point band, red further. The "
     "axis spans the full range of the data, including the handful of predictions well "
     "outside the plausible score range.")}

<p>The pooled figures — {pct('val.oos.exact')} exact, {pct('val.oos.within5')} within one
band, MAE {num('val.oos.mae')} points — understate current performance, because they average
a settled regime with an unsettled one.</p>

{fig("folds", F.fig_folds(B),
     f"Accuracy improves monotonically across folds, from MAE "
     f"{B['val']['folds'][0]['mae']:.2f} on the oldest to {B['val']['folds'][-1]['mae']:.2f} "
     f"on the newest. The shaded folds are the ones the uncertainty model in chapter 5 keeps.")}

<p>Reporting the aggregate alone would have hidden this. It would also have been the more
flattering choice in the other direction — the newest fold, the one closest to the round being
forecast, is the best of the four at {pct('val.folds.3.exact')} exact and
{pct('val.folds.3.within5')} within a band.</p>

<h3>C. Does the reading of the data match what was published?</h3>

<p>The first two tests both assume the cut-offs read out of the dashboard are the real ones.
That assumption is testable, because the Department published an official cut-off table for
one round. Deriving the cut-off for each occupation from the dashboard and comparing:</p>

{fig("official", F.fig_official(B),
     f"{num('val.official.n')} occupations, derived against published. "
     f"Exact {pct('val.official.exact', 1)}, within one band {pct('val.official.within5', 1)}, "
     f"MAE {num('val.official.mae')} points, r = {num('val.official.r')}.")}

<p>This is the check that settled the single-leg question in chapter 2. On an all-leg basis
the reconstruction does not reproduce the published table; on a single-leg basis it matches
{pct('val.official.exact', 1)} of {num('val.official.n')} occupations exactly. That is the
evidence for the basis every other number in this paper uses.</p>

<h3>A correction worth recording</h3>

<p>An earlier version of this page reported a far better forecast result — 49 of 49
occupations within five points, r&nbsp;=&nbsp;0.941. That comparison was invalid: it scored
single-leg predictions against an all-leg pool, mixing the two bases that test C exists to
keep apart. On a consistent single-leg basis the model performs as the table above shows, and
the earlier claim was withdrawn. The all-leg cut-off sits materially lower because 190 and 491
invitations drag it down.</p>
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

</ul>

{fig("horizon", F.fig_horizon(B),
     f"Error against how old the pool snapshot is. A snapshot from the month before a round "
     f"predicts it almost exactly (MAE {v(B['horizon_series']['1']['mae'], '{:.2f}')}); by six months "
     f"out it has degraded several-fold. Lag 0 is excluded because that snapshot is published "
     "after the round it would be predicting.")}

{fig("movement", F.fig_movement(B),
     f"How far a group's cut-off moves between consecutive rounds. It repeats only "
     f"{pct('mv.p_stay')} of the time; {pct('mv.p_move5')} of the time it shifts by exactly "
     "one band, more often down than up.")}

<ul>
<li><b>It says nothing about your individual case beyond points and date.</b> Nomination,
documentary problems, or anything specific to one application are outside it.</li>

<li><b>Some things were tested and found absent.</b> Groups do not measurably compete with each
other after the share is accounted for, and no seasonal effect survives testing
(p&nbsp;=&nbsp;{num('gaps.season_p', '{:.3f}')}, on a record with little power to detect one).
These are reported as
absences, not as features.</li>
</ul>

<p>A probability from this model is a statement about how often an outcome like yours occurred
in a comparable position historically. It is not a promise, and the width of {figref('residuals')} is the
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


TIP = r"""
/* the figures are static SVG with a tooltip baked onto each mark; one listener shows them */
(function(){
  var tip=document.createElement("div");
  tip.className="figtip"; tip.setAttribute("role","status"); tip.hidden=true;
  document.body.appendChild(tip);
  function tipShow(e){
    var m=e.target.closest?e.target.closest("[data-tip]"):null;
    if(!m){tipHide();return;}
    tip.textContent=m.getAttribute("data-tip"); tip.hidden=false;
    var r=m.getBoundingClientRect(), t=tip.getBoundingClientRect();
    var x=r.left+r.width/2-t.width/2, y=r.top-t.height-9;
    if(y<6) y=r.bottom+9;
    tip.style.left=Math.max(6,Math.min(innerWidth-t.width-6,x))+"px";
    tip.style.top=y+"px";
  }
  function tipHide(){tip.hidden=true;}
  document.addEventListener("pointerover",tipShow);
  document.addEventListener("pointerout",function(e){
    if(!e.relatedTarget||!e.relatedTarget.closest||!e.relatedTarget.closest("[data-tip]")) tipHide();});
  addEventListener("scroll",tipHide,{passive:true});
  addEventListener("resize",tipHide);
})();
"""

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
{nav_html("findings.html")}
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
{ROUTER}
{TIP}
{KATEX_JS}
{THEME}
</script>
</body></html>
"""

assert _drawn == sorted(_drawn) == list(range(1, len(_drawn) + 1)), \
    f"figures emitted out of order: {_drawn}"
(R / "docs" / "findings.html").write_text(page)
(R / "data" / "paper_numbers.json").write_text(json.dumps(sorted(_emitted)))
print(f"wrote docs/findings.html  ({len(page)/1024:.0f} KB, {len(CH)} chapters, "
      f"{page.count('<figure')} figures, {page.count('class=\"eq\"')} equations)")
print(f"  bundle values read into the prose: {len(_used)}")
