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
               stroke=CARD, sw=0.75,
               tip=f"{n:,} people at {s} points — "
                   f"{'covered by the allocation' if taken else 'below the cut-off'}")
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
    f = Fig(560, 248, ml=52, mr=18, mt=44, mb=52)   # mt reserves a band for the 80% bracket
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
               stroke=CARD, sw=0.75,
               tip=f"{c} of {len(res)} rounds were {b:+d} points"
                   f"{' — inside the central 80%' if inside else ''}")
        if c:
            f.text(x + bw / 2, f.mt + f.ph - h - 5, c, 9.5, MUTED)
        f.text(x + bw / 2, f.h - f.mb + 15, f"{b:+d}", 9.5, MUTED)
    x0 = f.ml + (edges.index(int(u["lo80"])) if int(u["lo80"]) in edges else 0) * bw
    x1 = f.ml + ((edges.index(int(u["hi80"])) if int(u["hi80"]) in edges else len(edges) - 1) + 1) * bw
    by = f.mt - 14                      # above every bar, never across one
    f.line(x0 + 1.5, by, x1 - 1.5, by, SERIES, 2, cap="round")
    f.line(x0 + 1.5, by, x0 + 1.5, by + 5, SERIES, 2)
    f.line(x1 - 1.5, by, x1 - 1.5, by + 5, SERIES, 2)
    f.text((x0 + x1) / 2, by - 6, f"central 80%: {u['lo80']:+.0f} to {u['hi80']:+.0f} points",
           10, SERIES, "middle", "700")
    f.ylab("rounds (count)")
    f.xlab("prediction minus outcome (points)")
    return f.svg("Walk-forward residuals of the cut-off model",
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
            f.rect(x, y, cw - 1.5, ch - 1.5, RAMP[k], rx=2,
                   tip=(f"{s} points at a round of {N:,}: "
                        f"{p*100:.0f}% chance" if p is not None else f"{s} points: no forecast"))
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
                 3.1, col, stroke=CARD, sw=0.9, op=0.85,
                 tip=f"predicted {r['pred']}, actual {r['actual']} "
                     f"({r['pred'] - r['actual']:+d} points)")
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
        f.rect(x, f.mt + f.ph - h, w, h, [RAMP[5], RAMP[4], RAMP[2], DEEMPH][i], rx=4,
               tip=f"Tier {k}: {r['per_1000']:.1f} invitations per 1,000 — "
                   f"{r['groups']} groups, {r['pool']:,} waiting")
        f.text(x + w / 2, f.mt + f.ph - h - 7, f"{r['per_1000']:.0f}", 12, INK, "middle", "700")
        f.text(x + w / 2, f.h - f.mb + 16, f"Tier {k}", 11, INK, "middle", "700")
        f.text(x + w / 2, f.h - f.mb + 30, f"{r['groups']} groups", 9.5, MUTED)
        f.text(x + w / 2, f.h - f.mb + 42, f"{r['pool']:,} waiting", 9.5, MUTED)
    f.ylab("invitations per 1,000 waiting")
    return f.svg("Invitation rate by priority tier",
                 "Tiers are those of the four-tier model released under FOI. The rate spans "
                 "more than two orders of magnitude across them.")


# ---------------------------------------------------------------- Figure 8
def fig_folds(B):
    """Accuracy fold by fold. The aggregate hides that the oldest fold is the worst."""
    folds = B["val"]["folds"]
    keep = set(B["val"]["unc_folds"])
    f = Fig(560, 236, ml=52, mr=64, mt=26, mb=62)
    n = len(folds)
    bw = f.pw / n
    mx = max(x["mae"] for x in folds) * 1.18
    for v in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - v / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, f"{v:.0f}", 10, MUTED, "end")
    # MAE as bars; the folds the residual model keeps are the emphasised ones
    for i, x in enumerate(folds):
        bx = f.ml + i * bw + bw * 0.18
        w = bw * 0.4
        h = f.ph * x["mae"] / mx
        used = x["round"] in keep
        f.rect(bx, f.mt + f.ph - h, w, h, BRAND if used else DEEMPH, rx=4,
               tip=f"{x['round']} forecast from {x['trained_on']}: MAE {x['mae']:.2f}, "
                   f"exact {x['exact']*100:.0f}%, n {x['n']}"
                   f"{' — kept for the residual model' if used else ''}")
        f.text(bx + w / 2, f.mt + f.ph - h - 7, f"{x['mae']:.2f}", 10.5, INK, "middle", "700")
        f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 16, x["round"], 10.5, INK, "middle", "700")
        f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 29, f"from {x['trained_on']}", 9, MUTED)
        f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 41, f"n = {x['n']}", 9, MUTED)
    # exact-hit rate on the same panel as a line, scaled to the same box
    X = lambda i: f.ml + i * bw + bw * 0.62
    Y2 = lambda p: f.mt + f.ph * (1 - p)
    d = "".join(f"{'M' if i==0 else 'L'}{X(i):.1f},{Y2(x['exact']):.1f} "
                for i, x in enumerate(folds))
    f.path(d, GOLD, 2)
    for i, x in enumerate(folds):
        f.circle(X(i), Y2(x["exact"]), 4.5, GOLD, stroke=CARD, sw=2)
        f.text(X(i) + 9, Y2(x["exact"]) + 3.5, f"{x['exact']*100:.0f}%", 10, GOLD, "start", "700")
    lx = f.ml + f.pw + 10
    f.rect(lx, f.mt + 2, 9, 9, BRAND, rx=2)
    f.text(lx + 13, f.mt + 10, "MAE", 9.5, MUTED, "start")
    f.rect(lx, f.mt + 18, 9, 9, DEEMPH, rx=2)
    f.text(lx + 13, f.mt + 26, "older", 9.5, MUTED, "start")
    f.circle(lx + 4.5, f.mt + 38, 4.5, GOLD)
    f.text(lx + 13, f.mt + 42, "exact", 9.5, MUTED, "start")
    f.ylab("mean absolute error (points)")
    return f.svg("Forecast accuracy fold by fold",
                 "Each fold forecasts one round from the one before it. Error falls steadily "
                 "as the allocation regime settles, which is why the uncertainty model keeps "
                 "only the two most recent folds (shaded).")


# ---------------------------------------------------------------- Figure 9
def fig_official(B):
    """Measurement check: the cut-off reconstructed from the dashboard vs the published one."""
    pairs = B["val"]["official_pairs"]
    st = B["val"]["official"]
    f = Fig(560, 300, ml=52, mr=18, mt=22, mb=52)
    vs = [v for p in pairs for v in p]
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
    seen = {}
    for pr, ac in pairs:
        k = seen.get((pr, ac), 0)
        seen[(pr, ac)] = k + 1
        ang, rad = k * 2.399, (0 if k == 0 else 2.0 * math.sqrt(k))
        col = GOOD if pr == ac else (WARN if abs(pr - ac) <= 5 else CRIT)
        f.circle(X(pr) + rad * math.cos(ang), Y(ac) + rad * math.sin(ang), 3.2, col,
                 stroke=CARD, sw=0.9, op=0.85,
                 tip=f"derived {pr}, published {ac} ({pr - ac:+d} points)")
    bx, by = f.ml + 10, f.mt + 12
    f.rect(bx - 6, by - 10, 186, 48, CARD, rx=8, stroke=GRID, sw=1)
    f.text(bx, by + 2, f"n = {st['n']} occupations", 9.5, MUTED, "start")
    f.text(bx, by + 17, f"exact {st['exact']*100:.1f}%   within 5 pts {st['within5']*100:.1f}%",
           9.5, MUTED, "start")
    f.text(bx, by + 31, f"MAE {st['mae']} pts   r = {st['r']:.4f}", 9.5, MUTED, "start")
    f.ylab("cut-off the Department published")
    f.xlab("cut-off derived from the dashboard")
    return f.svg("Reconstruction against the published table",
                 "Each point is one occupation in the tie-break round. This checks the "
                 "measurement, not the forecast: that reading cut-offs out of the dashboard "
                 "reproduces what was actually published.")


# ---------------------------------------------------------------- Figure: the pool
def fig_pool_shape(B):
    """Every live EOI, by score. The shape of what the model is walking down."""
    tot = {}
    for g in B["groups"].values():
        for k, n in g["dist"].items():
            tot[int(k)] = tot.get(int(k), 0) + n
    scores = sorted(tot, reverse=True)
    f = Fig(560, 236, ml=58, mr=18, mt=22, mb=54)
    mx = max(tot.values())
    bw = f.pw / len(scores)
    for t in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - t / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, kfmt(t), 10, MUTED, "end")
    run = 0
    grand = sum(tot.values())
    for i, s in enumerate(scores):
        n = tot[s]
        run += n
        h = f.ph * n / mx
        f.rect(f.ml + i * bw + 1, f.mt + f.ph - h, bw - 2, h,
               BRAND if s >= 80 else DEEMPH, rx=2,
               tip=f"{n:,} people at {s} points — {run:,} at or above ({run/grand*100:.0f}% of the pool)")
        if s % 10 == 0:
            f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 16, s, 10, MUTED)
    f.text(f.ml + 4, f.mt + 10, f"{grand:,} live EOIs in {len(B['groups'])} groups",
           10, MUTED, "start", "700")
    f.ylab("people waiting")
    f.xlab("points, highest first")
    return f.svg("The whole 189 pool by score",
                 "Every live single-leg EOI across all modelled groups. Shaded from 80 points "
                 "up, the part of the pool most rounds reach.")


# ---------------------------------------------------------------- Figure: concentration
def fig_shares(B):
    """How unevenly a round is divided between groups."""
    gs = sorted(((g["share"], k, g["name"]) for k, g in B["groups"].items() if g["share"] > 0),
                reverse=True)
    f = Fig(560, 250, ml=58, mr=18, mt=24, mb=56)
    top = gs[:20]
    mx = top[0][0]
    bw = f.pw / len(top)
    for t in nice_ticks(0, mx * 100, 4):
        y = f.mt + f.ph * (1 - (t / 100) / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, f"{t:g}%", 10, MUTED, "end")
    cum = 0
    for i, (sh, k, name) in enumerate(top):
        cum += sh
        h = f.ph * sh / mx
        f.rect(f.ml + i * bw + 1.5, f.mt + f.ph - h, bw - 3, h, BRAND, rx=2,
               tip=f"{name}: {sh*100:.2f}% of a round — {cum*100:.0f}% cumulative")
        f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 15, k, 8.5, MUTED, "middle", rot=-90)
    share20 = sum(x[0] for x in gs[:20])
    f.text(f.ml + 4, f.mt + 10,
           f"top 20 of {len(gs)} groups take {share20*100:.0f}% of a round", 10, MUTED, "start", "700")
    f.ylab("share of a round")
    f.xlab("unit group, largest share first")
    return f.svg("How a round divides between occupation groups",
                 "Share carried forward from the most recent round. The distribution is "
                 "steep, which is why the same score gives very different odds by occupation.")


# ---------------------------------------------------------------- Figure: date of effect
def fig_doe_bands(B, gk):
    """Within a band, the queue is by date. Several bands, one group."""
    cdf = B["doe_cdf"].get(gk, {})
    months = B["doe_months"]
    bands = [s for s in ("70", "75", "80", "85", "90") if cdf.get(s)]
    f = Fig(560, 250, ml=52, mr=76, mt=22, mb=54)
    if not bands:
        return f.text(f.w / 2, f.h / 2, "no date-of-effect record", 11, MUTED).svg("No data")
    idx = [i for s in bands for i, _ in cdf[s]]
    i0, i1 = min(idx), max(idx)
    X = lambda i: f.ml + f.pw * (i - i0) / max(1, i1 - i0)
    Y = lambda p: f.mt + f.ph * (1 - p)
    for q in (0, .25, .5, .75, 1):
        f.line(f.ml, Y(q), f.ml + f.pw, Y(q), GRID)
        f.text(f.ml - 8, Y(q) + 3.5, f"{q*100:.0f}%", 10, MUTED, "end")
    ramp = [RAMP[1], RAMP[2], RAMP[3], RAMP[4], RAMP[6]]
    ends = []
    for bi, s in enumerate(bands):
        pts = cdf[s]
        d, prev = "", None
        for i, c in pts:
            d += (f"M{X(i):.1f},{Y(c):.1f} " if prev is None
                  else f"L{X(i):.1f},{Y(prev):.1f} L{X(i):.1f},{Y(c):.1f} ")
            prev = c
        f.path(d, ramp[bi % len(ramp)], 2)
        ends.append([Y(pts[-1][1]), f"{s} pts", ramp[bi % len(ramp)]])
    # the curves all converge on 100%, so the labels must be pushed apart
    ends.sort(key=lambda e: e[0])
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i - 1][0] < 12:
            ends[i][0] = ends[i - 1][0] + 12
    drop = max(0, ends[-1][0] - (f.mt + f.ph))
    for y, lab, col in ends:
        f.text(f.ml + f.pw + 7, y - drop + 3.5, lab, 9.5, col, "start", "700")
    for i, a in ((i0, "start"), ((i0 + i1) // 2, "middle"), (i1, "end")):
        f.text(X(i), f.h - f.mb + 16, months[i], 10, MUTED, a)
    f.ylab("share of the band dated by then")
    f.xlab("date of effect")
    return f.svg("Date of effect within each score band",
                 "For one group, how each score band is spread by date. A band the cut-off "
                 "lands on is worked through in this order, earliest first.")


# ---------------------------------------------------------------- Figure: the programme
def fig_policy(B):
    """Where the round-size distribution comes from: published places."""
    p = B["policy"]
    f = Fig(560, 288, ml=16, mr=104, mt=30, mb=56)
    streams = [("Skilled Independent (189)", p["places"]),
               ("State nominated (190)", p["nominated"]),
               ("Regional (491)", p["regional_cut"]),
               ("Employer sponsored", p["employer"])]
    years = ["2025-26", "2026-27"]
    mx = max(v for _, d in streams for v in d.values())
    rh = f.ph / len(streams)
    for t in nice_ticks(0, mx, 4):
        x = f.ml + f.pw * t / mx
        f.line(x, f.mt, x, f.mt + f.ph, GRID)
        f.text(x, f.h - f.mb + 16, kfmt(t), 10, MUTED)
    for si, (name, d) in enumerate(streams):
        y0 = f.mt + si * rh
        f.text(f.ml, y0 + 10, name, 9.5, MUTED, "start", "700")
        for yi, yr in enumerate(years):
            v = d[yr]
            h = rh * 0.26
            yy = y0 + 18 + yi * (h + 3)
            col = BRAND if si == 0 else DEEMPH
            f.rect(f.ml, yy, f.pw * v / mx, h, col, rx=2,
                   tip=f"{name}, {yr}: {v:,} places")
            f.text(f.ml + f.pw * v / mx + 6, yy + h - 1, f"{v:,}", 9, MUTED, "start")
    f.text(f.ml + f.pw + 14, f.mt + 6, "2025-26", 9, MUTED, "start")
    f.text(f.ml + f.pw + 14, f.mt + 20, "2026-27", 9, MUTED, "start", "700")
    f.text(f.ml, f.mt - 10,
           f"189 places rise {p['ratio']:.2f}x — {p['projected_invitations']:,} invitations projected",
           10, INK, "start", "700")
    f.xlab("places in the migration programme")
    return f.svg("Published places by stream and year",
                 "The 189 line is what the round-size distribution is built from. The other "
                 "streams are shown because they compete for the same programme ceiling.")


# ---------------------------------------------------------------- Figure: staleness
def fig_horizon(B):
    """Error against how old the pool snapshot is."""
    h = B["horizon_series"]
    lags = sorted((int(k) for k in h), key=int)
    f = Fig(560, 236, ml=52, mr=74, mt=26, mb=54)
    mx = max(h[str(l)]["mae"] for l in lags) * 1.15
    X = lambda l: f.ml + f.pw * (l - lags[0]) / max(1, lags[-1] - lags[0])
    Y = lambda v: f.mt + f.ph * (1 - v / mx)
    for t in nice_ticks(0, mx, 4):
        f.line(f.ml, Y(t), f.ml + f.pw, Y(t), GRID)
        f.text(f.ml - 8, Y(t) + 3.5, f"{t:g}", 10, MUTED, "end")
    usable = [l for l in lags if l >= 1]
    d = "".join(f"{'M' if i==0 else 'L'}{X(l):.1f},{Y(h[str(l)]['mae']):.1f} "
                for i, l in enumerate(usable))
    f.path(d, BRAND, 2.5)
    for l in lags:
        r = h[str(l)]
        excluded = l == 0
        f.circle(X(l), Y(r["mae"]), 4.6, CRIT if excluded else BRAND,
                 stroke=CARD, sw=2, op=0.55 if excluded else 1,
                 tip=(f"lag {l} month{'s' if l != 1 else ''}: MAE {r['mae']:.2f}, "
                      f"exact {r['exact']*100:.0f}%, n {r['n']}"
                      + (" — excluded: this snapshot postdates the round" if excluded else "")))
        f.text(X(l), f.h - f.mb + 16, l, 10, MUTED)
    f.text(X(0) + 7, Y(h["0"]["mae"]) - 9, "excluded", 9.5, CRIT, "start", "700")
    f.text(f.ml + f.pw + 8, Y(h[str(usable[-1])]["mae"]) + 3.5, "MAE", 9.5, BRAND, "start", "700")
    f.ylab("mean absolute error (points)")
    f.xlab("months between the pool snapshot and the round")
    return f.svg("Forecast error against the age of the pool snapshot",
                 "A snapshot taken the month before a round predicts it almost exactly. The "
                 "further back it was taken, the worse it does. Lag 0 is excluded because "
                 "that snapshot is published after the round it would be predicting.")


# ---------------------------------------------------------------- Figure: the pool moves
def fig_movement(B):
    """Scores do not sit still between snapshots."""
    mv = B["mv"]
    d = mv["delta_all"]
    keys = sorted((int(k) for k in d), key=int)
    f = Fig(560, 244, ml=52, mr=18, mt=42, mb=56)   # mt reserves the summary line
    mx = max(d.values())
    bw = f.pw / len(keys)
    for t in nice_ticks(0, mx, 4):
        y = f.mt + f.ph * (1 - t / mx)
        f.line(f.ml, y, f.ml + f.pw, y, GRID)
        f.text(f.ml - 8, y + 3.5, f"{t:g}", 10, MUTED, "end")
    tot = sum(d.values())
    for i, k in enumerate(keys):
        n = d[str(k)]
        h = f.ph * n / mx
        col = DEEMPH if k == 0 else (GOOD if k > 0 else WARN)
        f.rect(f.ml + i * bw + 2, f.mt + f.ph - h, bw - 4, h, col, rx=3,
               tip=f"{n} of {tot} groups moved {k:+d} points ({n/tot*100:.0f}%)")
        f.text(f.ml + i * bw + bw / 2, f.mt + f.ph - h - 5, n, 9.5, MUTED)
        f.text(f.ml + i * bw + bw / 2, f.h - f.mb + 16, f"{k:+d}", 9.5, MUTED)
    f.text(f.ml + 4, f.mt - 24,
           f"unchanged {mv['p_stay']*100:.0f}% · moved one band {mv['p_move5']*100:.0f}% · "
           f"two or more {mv['p_move10']*100:.0f}%", 10, INK, "start", "700")
    f.ylab("observations")
    f.xlab("change in a group's cut-off between consecutive rounds (points)")
    return f.svg("How far a cut-off moves from one round to the next",
                 "The cut-off rarely repeats: it usually shifts by one five-point band, and "
                 "more often down than up.")


# ---------------------------------------------------------------- Figure: quota chain
def fig_quota_chain(B):
    """Published places to expected round size, with the one measured link in between."""
    p = B["policy"]
    f = Fig(560, 268, ml=16, mr=16, mt=58, mb=56)
    inv = p["inv_by_round"]
    py = p["py"]["2025-26"]
    steps = [
        (f"{p['places']['2025-26']:,}", "places, 2025-26", "published", DEEMPH),
        (f"{p['inv_2025_26']:,}", "invitations issued", f"{len(py)} rounds, observed", SERIES),
        (f"{p['ratio']:.2f}x", "invitations per place", "the measured link", BRAND),
        (f"{p['places']['2026-27']:,}", "places, 2026-27", "published", DEEMPH),
        (f"{p['projected_invitations']:,}", "invitations implied", "places x the link", BRAND),
    ]
    bw = f.pw / len(steps)
    for i, (val, lab, sub, col) in enumerate(steps):
        x = f.ml + i * bw
        f.rect(x + 5, f.mt, bw - 10, 66, col, rx=10,
               tip=f"{lab}: {val} ({sub})")
        f.text(x + bw / 2, f.mt + 29, val, 17, CARD, "middle", "700")
        f.text(x + bw / 2, f.mt + 47, lab, 9, CARD, "middle")
        f.text(x + bw / 2, f.mt + 82, sub, 9, MUTED, "middle")
        if i < len(steps) - 1:
            ax = x + bw - 5
            f.text(ax, f.mt + 34, "→" if i != 2 else "÷", 13, MUTED, "middle", "700")
    # what the projection then implies per round, the quantity the model needs
    y = f.mt + 108
    f.text(f.ml + 6, y, "across the rounds still expected:", 10, MUTED, "start", "700")
    per = p["per_round"]
    for j, k in enumerate(sorted(per, key=int)):
        bx = f.ml + 6 + j * (f.pw / 3)
        f.text(bx, y + 24, f"{per[k]:,}", 15, INK, "start", "700")
        f.text(bx, y + 38, f"if {k} rounds remain", 9, MUTED, "start")
    f.text(f.ml + 6, f.mt - 38,
           "A correlation between round size and the annual quota cannot be estimated:", 10, INK, "start", "700")
    f.text(f.ml + 6, f.mt - 24,
           "only one programme year has both a published level and a complete round record.", 10, MUTED, "start")
    return f.svg("From the published quota to an expected round size",
                 "The quota sets the scale of a round through one measured quantity: how many "
                 "invitations the Department issues per place. That ratio comes from the single "
                 "programme year where both numbers are known.")
