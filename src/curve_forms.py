"""Is a straight line the right shape for the two trends the model fits?

Two places assume a functional form: error against how stale the pool snapshot is
(horizon.py) and the pool's strengthening over time (gap1_drift.py). Both take a
first-degree polyfit. This tests that choice against alternatives rather than
asserting it, using leave-one-out cross-validation, which is the honest criterion
when n is this small - in-sample R^2 always rewards the more flexible shape.
"""
import json, math, pathlib, os
import numpy as np

os.chdir(pathlib.Path(__file__).resolve().parent.parent / "data")

FORMS = {
    "linear      a+bx":        (lambda x: np.c_[np.ones_like(x), x]),
    "sqrt        a+b*sqrt(x)": (lambda x: np.c_[np.ones_like(x), np.sqrt(x)]),
    "log         a+b*ln(x)":   (lambda x: np.c_[np.ones_like(x), np.log(x)]),
    "quadratic   a+bx+cx^2":   (lambda x: np.c_[np.ones_like(x), x, x**2]),
    "saturating  a+b*x/(1+x)": (lambda x: np.c_[np.ones_like(x), x / (1.0 + x)]),
}


def loo(x, y, design):
    """Leave-one-out prediction error. A shape that only wins in-sample loses here."""
    err = []
    for i in range(len(x)):
        m = np.ones(len(x), bool); m[i] = False
        A = design(x[m])
        if np.linalg.matrix_rank(A) < A.shape[1]:
            return float("inf")
        beta, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        err.append(y[i] - design(x[i:i+1]) @ beta)
    return float(np.sqrt(np.mean(np.square(err))))


def insample(x, y, design):
    A = design(x)
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ beta
    ss = 1 - r.var() / y.var() if y.var() > 0 else float("nan")
    return float(np.sqrt(np.mean(r**2))), float(ss)


RESULT = {}


def compare(name, x, y, note="", key=None):
    print("=" * 86)
    print(f"{name}   n = {len(x)}   {note}")
    print("=" * 86)
    print(f"  {'form':<26}{'in-sample RMSE':>16}{'R^2':>8}{'LOO RMSE':>12}")
    rows = []
    for label, design in FORMS.items():
        ri, r2 = insample(x, y, design)
        rows.append((loo(x, y, design), ri, r2, label))
    rows.sort()
    for lo, ri, r2, label in rows:
        best = "  <-- best out of sample" if lo == rows[0][0] else ""
        print(f"  {label:<26}{ri:>16.4f}{r2:>8.3f}{lo:>12.4f}{best}")
    lin = [r for r in rows if r[3].startswith("linear")][0]
    win = rows[0]
    print()
    if win[3].startswith("linear"):
        print("  -> the straight line is already the best shape out of sample.")
    else:
        print(f"  -> {win[3].split()[0]} beats linear out of sample "
              f"({win[0]:.4f} vs {lin[0]:.4f}, {100*(1-win[0]/lin[0]):.0f}% lower error).")
    print()
    if key:
        RESULT[key] = dict(best=win[3].split()[0], best_loo=round(win[0], 4),
                           linear_loo=round(lin[0], 4),
                           gain=round(1 - win[0] / lin[0], 4) if lin[0] else 0.0,
                           n=int(len(x)),
                           forms={r[3].split()[0]: dict(loo=round(r[0], 4), r2=round(r[2], 3))
                                  for r in rows})
    return rows


h = json.load(open("horizon.json"))
lags = sorted((int(k) for k in h if k.isdigit()))
# lag 0 is excluded upstream: that snapshot is published after the round it would predict
x = np.array([l for l in lags if l >= 1], float)
y = np.array([h[str(int(l))]["mae"] for l in x], float)
compare("ERROR AGAINST POOL-SNAPSHOT STALENESS", x, y,
        "lag 0 excluded - that snapshot postdates the round", key="staleness")

import pandas as pd
_f = pathlib.Path("drift_series.csv")
if _f.exists():
    _d = pd.read_csv(_f)
    _x = np.arange(1, len(_d) + 1, dtype=float)
    compare("POOL MEAN SCORE OVER TIME", _x, _d["mean"].to_numpy(float),
            "monthly snapshots", key="pool_mean")
    compare("SHARE OF THE POOL AT 85 OR MORE", _x, _d["share85"].to_numpy(float) * 100,
            "monthly snapshots, percentage points", key="pool_share85")
else:
    print("drift_series.csv missing - run gap1_drift.py first")

import pandas as pd
d = pd.read_csv("doe_pool_grp.csv") if pathlib.Path("doe_pool_grp.csv").exists() else None
g = json.load(open("drift.json"))
print("=" * 86)
print("WHAT THE MODEL ACTUALLY FITS")
print("=" * 86)
print("  cut-off          no functional form - the pool is walked until places run out")
print("  residual spread  empirical, deliberately NOT fitted to a normal")
print("  group share      last round's value carried forward, no curve")
print("  round size       a mixture from published places and a rounds-remaining prior")
print(f"  staleness        LINEAR, tested above")
print(f"  pool drift       LINEAR at {g['mean_trend_per_month']:+.4f} points/month, tested above")

_b = json.load(open("bundle.json"))
_b["curves"] = RESULT
json.dump(_b, open("bundle.json", "w"), separators=(",", ":"))
print("\n  -> bundle.json['curves'] written")
