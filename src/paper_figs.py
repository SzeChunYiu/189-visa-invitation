"""The seven figures of the method paper, each computed from data/bundle.json."""
import math
from paper_fig import (Fig, nice_ticks, kfmt, INK, MUTED, GRID, AXIS, BRAND, SERIES,
                       GOOD, WARN, CRIT, DEEMPH, CARD, GOLD, RAMP)

FLOOR = 65


# ---------------------------------------------------------------- model, in Python
def cutoff_at(g, N, fr, floor=FLOOR):
    """Walk the pool from the top until the group's allocation is consumed. Mirrors
    cutoffAt() in the explorer; the audit asserts the two agree."""
    A = math.floor(g["share"] * N * fr + 0.5)   # JS Math.round, not half-to-even
    if A <= 0:
        return None
    c = 0
    for k in sorted((int(k) for k in g["dist"] if int(k) >= floor), reverse=True):
        c += g["dist"][str(k)]
        if c >= A:
            return k
    return floor


def p_le(res, fc, s):
    """P(cut-off <= s). Residual is prediction minus outcome, so the cut-off lands at
    or below s whenever the residual is at least fc - s."""
    if fc is None:
        return None
    need = fc - s
    return sum(1 for e in res if e >= need) / len(res)


def p_clear(res, fc, s, reach=0.0):
    le = p_le(res, fc, s)
    if le is None:
        return None
    lt = p_le(res, fc, s - 5)
    return lt + max(0.0, le - lt) * reach


def p_marginal(B, g, s, reach=0.0):
    rs, res = B["rs"], B["unc"]["residuals"]
    acc = w = 0.0
    for N, d in zip(rs["grid"], rs["dens"]):
        p = p_clear(res, cutoff_at(g, N, B["meta"]["fr"]), s, reach)
        if p is not None:
            acc += d * p
            w += d
    return acc / w if w > 0 else None


# ---------------------------------------------------------------- Figure 1
def fig_mechanism(B, gk):
    """The pool, and the depth the allocation reaches into it."""
    g = B["groups"][gk]
    f = Fig(560, 250, ml=54, mr=132, mt=20, mb=48)
    scores = sorted((int(k) for k in g["dist"]), reverse=True)
    N = B["rs"]["q50"]          # the median round, the same one chapter 7 reports
    A = round(g["share"] * N * B["meta"]["fr"])
    cut = cutoff_at(g, N, B["meta"]["fr"])
    mx = max(g["dist"].values())
    bw = f.pw / len(scores)
    for t in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - t / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, kfmt(t), 10, MUTED, "end")
    cum = 0
    for i, s in enumerate(scores):
        n = g["dist"][str(s)]
        x = f.ml + i * bw
        h = f.ph * n / mx
        taken = cut is not None and s >= cut
        f.rect(x + 1, f.mt + f.ph - h, bw - 3, h, BRAND if taken else DEEMPH, rx=2,
               stroke=CARD, sw=0.75)
        if s % 10 == 0:
            f.text(x + bw / 2, f.h - f.mb + 15, s, 10, MUTED)
        cum += n
    if cut is not None:
        i = scores.index(cut)
        x = f.ml + (i + 1) * bw
        f.line(x, f.mt - 4, x, f.mt + f.ph + 5, CRIT, 2, dash="4 3")
        f.text(x + 5, f.mt + 9, f"cut-off {cut}", 10.5, CRIT, "start", "700")
    # what the shaded bars add up to, stated beside the plot
    lx = f.ml + f.pw + 12
    for j, (lab, val, col) in enumerate([
            ("allocation A", f"{A:,}", BRAND),
            ("pool at or above", f"{sum(n for s, n in ((s, g['dist'][str(s)]) for s in scores) if cut and s >= cut):,}", BRAND),
            ("pool total", f"{g['pool']:,}" if "pool" in g else f"{sum(g['dist'].values()):,}", DEEMPH)]):
        y = f.mt + 16 + j * 34
        f.rect(lx, y - 8, 8, 8, col, rx=2)
        f.text(lx + 13, y, lab, 9.5, MUTED, "start")
        f.text(lx + 13, y + 13, val, 12.5, INK, "start", "700")
    f.ylab("people in the pool")
    f.xlab("points, highest first")
    return f.svg("Pool of a single occupation group, with the share the allocation reaches",
                 "Bars are the number of people at each score. Shaded bars are those the "
                 "allocation covers; the dashed line is the resulting cut-off.")


# ---------------------------------------------------------------- Figure 2
def fig_cutoff_curves(B, highlight=None):
    """c_g(N) for every group: a step function, and a different one per group."""
    f = Fig(560, 250, ml=52, mr=18, mt=18, mb=50)
    grid = list(range(3000, 20001, 500))
    fr = B["meta"]["fr"]
    curves = []
    for gk, g in B["groups"].items():
        if g["share"] <= 0:
            continue
        ys = [cutoff_at(g, N, fr) for N in grid]
        if all(y is None for y in ys):
            continue
        curves.append((gk, ys))
    lo, hi = FLOOR, 100
    X = lambda N: f.ml + f.pw * (N - grid[0]) / (grid[-1] - grid[0])
    Y = lambda v: f.mt + f.ph * (1 - (v - lo) / (hi - lo))
    for t in range(lo, hi + 1, 5):
        y = Y(t)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        if t % 10 == 0:
            f.text(f.ml - 8, y + 3.5, t, 10, MUTED, "end")
    for N in nice_ticks(grid[0], grid[-1], 5):
        f.text(X(N), f.h - f.mb + 16, kfmt(N), 10, MUTED)
    for gk, ys in curves:
        d, started = "", False
        for N, v in zip(grid, ys):
            if v is None:
                started = False
                continue
            d += ("L" if started else "M") + f"{X(N):.1f},{Y(v):.1f} "
            started = True
        if d:
            f.path(d, DEEMPH, 1, op=0.32)
    if highlight and highlight in B["groups"]:
        ys = [cutoff_at(B["groups"][highlight], N, fr) for N in grid]
        d, started = "", False
        for N, v in zip(grid, ys):
            if v is None:
                started = False
                continue
            d += ("L" if started else "M") + f"{X(N):.1f},{Y(v):.1f} "
            started = True
        f.path(d, BRAND, 2.5)
        f.text(X(grid[-1]) - 4, Y(ys[-1]) - 9, B["groups"][highlight]["name"].split(" ", 1)[0],
               10.5, BRAND, "end", "700")
    f.text(f.ml + 4, f.mt + 12, f"{len(curves)} occupation groups", 10, MUTED, "start")
    f.ylab("cut-off (points)")
    f.xlab("round size N (invitations issued)")
    return f.svg("Forecast cut-off against round size, every occupation group",
                 "Each faint line is one group. The cut-off falls in discrete five-point "
                 "steps as the round grows, and at any round size the groups disagree.")


# ---------------------------------------------------------------- Figure 3
def fig_residuals(B):
    """The empirical error distribution that turns a point cut-off into a probability."""
    u = B["unc"]
    res = u["residuals"]
    f = Fig(560, 230, ml=52, mr=18, mt=20, mb=52)
    vals = sorted(set(res))
    lo, hi = min(vals), max(vals)
    edges = list(range(lo, hi + 6, 5))
    counts = [sum(1 for e in res if e == b) for b in edges]
    mx = max(counts)
    bw = f.pw / len(edges)
    for t in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - t / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, f"{t:.0f}", 10, MUTED, "end")
    for i, (b, c) in enumerate(zip(edges, counts)):
        x = f.ml + i * bw
        h = f.ph * c / mx
        inside = u["lo80"] <= b <= u["hi80"]
        f.rect(x + 1.5, f.mt + f.ph - h, bw - 3, h, SERIES if inside else DEEMPH, rx=3,
               stroke=CARD, sw=0.75)
        if c:
            f.text(x + bw / 2, f.mt + f.ph - h - 5, c, 9.5, MUTED)
        f.text(x + bw / 2, f.h - f.mb + 15, f"{b:+d}", 9.5, MUTED)
    x0 = f.ml + (edges.index(int(u["lo80"])) if int(u["lo80"]) in edges else 0) * bw
    x1 = f.ml + ((edges.index(int(u["hi80"])) if int(u["hi80"]) in edges else len(edges) - 1) + 1) * bw
    f.line(x0 + 1.5, f.mt + 4, x1 - 1.5, f.mt + 4, SERIES, 2, cap="round")
    f.text((x0 + x1) / 2, f.mt - 3, f"central 80%: {u['lo80']:+.0f} to {u['hi80']:+.0f} points",
           10, SERIES, "middle", "700")
    f.ylab("rounds (count)")
    f.xlab("prediction minus outcome (points)")
    return f.svg("Leave-one-round-out residuals of the cut-off model",
                 f"{u['n']} held-out group-rounds. The spread of this histogram, not a "
                 "normal approximation, is what the probability is read from.")


# ---------------------------------------------------------------- Figure 4
def fig_surface(B, gk):
    """P(invited) over score and round size - the object the model actually produces."""
    g = B["groups"][gk]
    res, fr = B["unc"]["residuals"], B["meta"]["fr"]
    sizes = list(range(4000, 18001, 1000))
    scores = list(range(FLOOR, 101, 5))
    f = Fig(560, 300, ml=52, mr=92, mt=22, mb=52)
    cw, ch = f.pw / len(sizes), f.ph / len(scores)
    for i, N in enumerate(sizes):
        c = cutoff_at(g, N, fr)
        for j, s in enumerate(reversed(scores)):
            p = p_clear(res, c, s, 0.0)
            x, y = f.ml + i * cw, f.mt + j * ch
            k = 0 if p is None else min(6, int(p * 6.999))
            f.rect(x, y, cw - 1.5, ch - 1.5, RAMP[k], rx=2)
            if p is not None and cw > 26 and p > 0.02:
                f.text(x + cw / 2 - 0.75, y + ch / 2 + 3.2, f"{round(p*100)}",
                       8.5, INK if p < 0.55 else CARD, "middle")
    for j, s in enumerate(reversed(scores)):
        f.text(f.ml - 8, f.mt + j * ch + ch / 2 + 3.5, s, 10, MUTED, "end")
    for i, N in enumerate(sizes):
        if i % 2 == 0:
            f.text(f.ml + i * cw + cw / 2, f.h - f.mb + 16, kfmt(N), 10, MUTED)
    lx = f.ml + f.pw + 16
    f.text(lx, f.mt + 2, "P(invited)", 9.5, MUTED, "start", "700")
    for k in range(7):
        y = f.mt + 12 + (6 - k) * 15
        f.rect(lx, y, 13, 13, RAMP[k], rx=2)
        f.text(lx + 18, y + 10, f"{int(k/7*100)}–{int((k+1)/7*100)}%", 9, MUTED, "start")
    f.ylab("your points")
    f.xlab("round size N")
    return f.svg("Invitation probability across score and round size, one occupation group",
                 "Every cell is the probability for a candidate at that score if the round "
                 "is that size. The same grid is computed for each of the groups.")


# ---------------------------------------------------------------- Figure 5
def fig_roundsize(B):
    """The round-size distribution the conditional probability is averaged over."""
    rs = B["rs"]
    f = Fig(560, 220, ml=52, mr=18, mt=22, mb=50)
    grid, dens = rs["grid"], rs["dens"]
    mx = max(dens)
    X = lambda N: f.ml + f.pw * (N - grid[0]) / (grid[-1] - grid[0])
    Y = lambda d: f.mt + f.ph * (1 - d / mx)
    for N in nice_ticks(grid[0], grid[-1], 5):
        x = X(N)
        f.line(x, f.mt, x, f.mt + f.ph, GRID)
        f.text(x, f.h - f.mb + 16, kfmt(N), 10, MUTED)
    # enumerate() before the filter numbered the WHOLE grid, so the first kept point
    # could carry i>0 and the path opened with L instead of M - an invalid path
    inner = [(N, d) for N, d in zip(grid, dens) if rs["q10"] <= N <= rs["q90"]]
    band = "".join(f"{'M' if i==0 else 'L'}{X(N):.1f},{Y(d):.1f} "
                   for i, (N, d) in enumerate(inner))
    if band:
        xs = [N for N, _ in inner]
        f.path(band + f"L{X(xs[-1]):.1f},{Y(0):.1f} L{X(xs[0]):.1f},{Y(0):.1f} Z",
               "none", 0, fill=BRAND, op=0.16)
    f.path("".join(f"{'M' if i==0 else 'L'}{X(N):.1f},{Y(d):.1f} "
                   for i, (N, d) in enumerate(zip(grid, dens))), BRAND, 2)
    for q, lab in ((rs["q10"], "10%"), (rs["q50"], "median"), (rs["q90"], "90%")):
        x = X(q)
        f.line(x, f.mt + 6, x, f.mt + f.ph, INK if lab == "median" else MUTED, 1.5, dash="3 3")
        f.text(x, f.mt - 4, f"{lab} {q:,}", 9.5, INK if lab == "median" else MUTED, "middle", "700")
    f.ylab("relative likelihood")
    f.xlab("round size N")
    return f.svg("Distribution of the next round's size",
                 "Built from the published places for the program year, the number of rounds "
                 "still to be held, and the observed spread of past round sizes.")


# ---------------------------------------------------------------- Figure 6
def fig_calibration(rows, oos):
    """Out-of-sample: predicted cut-off against the one that actually happened."""
    f = Fig(560, 300, ml=52, mr=18, mt=22, mb=52)
    # the axis comes from the data. A hand-picked range silently pushed the ten worst
    # predictions outside the plot - the very points a calibration figure exists to show.
    vs = [r["pred"] for r in rows] + [r["actual"] for r in rows]
    lo, hi = (min(vs) // 5) * 5 - 5, -(-max(vs) // 5) * 5 + 5
    X = lambda v: f.ml + f.pw * (v - lo) / (hi - lo)
    Y = lambda v: f.mt + f.ph * (1 - (v - lo) / (hi - lo))
    for t in range(int(lo) + 10 - int(lo) % 10, int(hi) + 1, 10):
        f.line(f.ml, Y(t), f.ml + f.pw, Y(t), GRID)
        f.line(X(t), f.mt, X(t), f.mt + f.ph, GRID)
        f.text(f.ml - 8, Y(t) + 3.5, t, 10, MUTED, "end")
        f.text(X(t), f.h - f.mb + 16, t, 10, MUTED)
    f.line(X(lo), Y(lo), X(hi), Y(hi), INK, 1.5, dash="4 3")
    f.text(X(hi) - 4, Y(hi) + 14, "exact", 9.5, MUTED, "end", "700")
    # jitter identical integer pairs apart so density is visible, deterministically
    seen = {}
    for r in rows:
        key = (r["pred"], r["actual"])
        k = seen.get(key, 0)
        seen[key] = k + 1
        ang = k * 2.399
        rad = 0 if k == 0 else 1.9 * math.sqrt(k)
        err = abs(r["pred"] - r["actual"])
        col = GOOD if err == 0 else (WARN if err <= 5 else CRIT)
        f.circle(X(r["pred"]) + rad * math.cos(ang), Y(r["actual"]) + rad * math.sin(ang),
                 3.1, col, stroke=CARD, sw=0.9, op=0.85)
    bx, by = f.ml + 10, f.mt + 12
    f.rect(bx - 6, by - 10, 176, 62, CARD, rx=8, stroke=GRID, sw=1)
    f.text(bx, by + 2, f"n = {oos['n']} held-out group-rounds", 9.5, MUTED, "start")
    f.text(bx, by + 17, f"exact {oos['exact']*100:.0f}%   within 5 pts {oos['within5']*100:.0f}%",
           9.5, MUTED, "start")
    f.text(bx, by + 32, f"MAE {oos['mae']:.2f} pts   bias {oos['bias']:+.2f}", 9.5, MUTED, "start")
    f.text(bx, by + 45, f"r = {oos['r']:.3f}", 9.5, MUTED, "start")
    f.ylab("cut-off that happened")
    f.xlab("cut-off the model predicted")
    return f.svg("Out-of-sample calibration of the cut-off model",
                 "Each point is one group in one round the model never saw. Green is exact, "
                 "amber within one five-point band, red further.")


# ---------------------------------------------------------------- Figure 7
def fig_tiers(B):
    """Invitations per 1,000 in the pool, by the tier of the FOI-released model."""
    t = B["tiers"]["by_tier"]
    f = Fig(560, 216, ml=60, mr=18, mt=22, mb=64)
    keys = sorted(t, key=int)
    mx = max(t[k]["per_1000"] for k in keys)
    bw = f.pw / len(keys)
    for v in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - v / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, f"{v:.0f}", 10, MUTED, "end")
    for i, k in enumerate(keys):
        r = t[k]
        x = f.ml + i * bw + bw * 0.2
        w = bw * 0.6
        h = f.ph * r["per_1000"] / mx
        f.rect(x, f.mt + f.ph - h, w, h, [RAMP[5], RAMP[4], RAMP[2], DEEMPH][i], rx=4)
        f.text(x + w / 2, f.mt + f.ph - h - 7, f"{r['per_1000']:.0f}", 12, INK, "middle", "700")
        f.text(x + w / 2, f.h - f.mb + 16, f"Tier {k}", 11, INK, "middle", "700")
        f.text(x + w / 2, f.h - f.mb + 30, f"{r['groups']} groups", 9.5, MUTED)
        f.text(x + w / 2, f.h - f.mb + 42, f"{r['pool']:,} waiting", 9.5, MUTED)
    f.ylab("invitations per 1,000 waiting")
    return f.svg("Invitation rate by priority tier",
                 "Tiers are those of the four-tier model released under FOI. The rate spans "
                 "more than two orders of magnitude across them.")
