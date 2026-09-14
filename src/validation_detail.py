"""Per-fold breakdown of every validation the paper reports, written into the bundle.

Three separate exercises are reported. They answer different questions and were being
conflated in one table:

  mechanism  - cut-off from (pool, ACTUAL allocation): does the walk-the-pool rule hold?
  forecast   - cut-off from (pool, allocation SHARE carried from the previous round),
               walk-forward, each round predicted from its immediate predecessor
  official   - cut-off derived from the dashboard vs the Department's published table:
               does the reconstruction reproduce what was actually published?
"""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent / "data")

ROUNDS = ["2024-09", "2024-11", "2025-08", "2025-11", "2026-06"]
UNC_FOLDS = ["2025-11", "2026-06"]      # folds uncertainty.py keeps: the current regime


def stats(z):
    e = z.pred - z.actual
    return dict(n=int(len(z)), exact=round(float((e == 0).mean()), 4),
                within5=round(float((e.abs() <= 5).mean()), 4),
                mae=round(float(e.abs().mean()), 2), bias=round(float(e.mean()), 2),
                r=round(float(np.corrcoef(z.pred, z.actual)[0, 1]), 4) if len(z) > 2 else None)


o = pd.read_csv("validation_oos_singleleg.csv")
folds = [dict(round=rd, trained_on=ROUNDS[ROUNDS.index(rd) - 1], **stats(o[o["round"] == rd]))
         for rd in ROUNDS[1:] if (o["round"] == rd).any()]

c = pd.read_csv("calibration_official.csv")
c = c.rename(columns={"official": "actual", "derived": "pred"})
c["pred"] = c.pred.astype(int); c["actual"] = c.actual.astype(int)

# in equation 1, and until now quantified nowhere
_B0 = json.load(open("bundle.json"))
_cv = []
for _g in _B0["groups"].values():
    _nz = [x for x in _g.get("share_hist", []) if x > 0]
    if len(_nz) > 2:
        _m = sum(_nz) / len(_nz)
        _sd = (sum((x - _m) ** 2 for x in _nz) / len(_nz)) ** .5
        if _m > 0:
            _cv.append(_sd / _m)
_cv.sort()
share_var = dict(n=len(_cv),
                 median=round(_cv[len(_cv) // 2], 3),
                 q1=round(_cv[len(_cv) // 4], 3),
                 q3=round(_cv[3 * len(_cv) // 4], 3))

val = dict(
    folds=folds,
    oos=stats(o),
    official=dict(**stats(c), tie_break=json.load(open("calibration_official.json"))["tie_break"]),
    official_pairs=[[int(r.pred), int(r.actual)] for r in c.itertuples()],
    unc_folds=UNC_FOLDS,
    unc_n=int(o["round"].isin(UNC_FOLDS).sum()),
    mech=json.load(open("validation_singleleg.json"))["mech"],
    share_var=share_var,
)

# how much a group's share actually moves between rounds - the dominant uncertainty

B = json.load(open("bundle.json"))
B["val"] = val
json.dump(B, open("bundle.json", "w"), separators=(",", ":"))

print("=" * 92)
print("WALK-FORWARD FOLDS  (each round forecast from the one before it)")
print("=" * 92)
print(f"  {'held-out round':<16}{'trained on':<14}{'n':>5}{'exact':>8}{'within5':>9}{'MAE':>7}{'bias':>7}{'r':>7}")
for f in folds:
    print(f"  {f['round']:<16}{f['trained_on']:<14}{f['n']:>5}{f['exact']:>7.0%}{f['within5']:>9.0%}"
          f"{f['mae']:>7.2f}{f['bias']:>+7.2f}{f['r']:>7.3f}")
a = val["oos"]
print(f"  {'ALL FOLDS':<30}{a['n']:>5}{a['exact']:>7.0%}{a['within5']:>9.0%}{a['mae']:>7.2f}{a['bias']:>+7.2f}{a['r']:>7.3f}")
print(f"\n  residual distribution uses only {val['unc_n']} of {a['n']} — folds {UNC_FOLDS} (current regime)")
ofc = val["official"]
print(f"\n  official-table calibration: n={ofc['n']}  exact={ofc['exact']:.1%}  "
      f"within5={ofc['within5']:.1%}  MAE={ofc['mae']}  r={ofc['r']}")
print(f"\n  share coefficient of variation across rounds: median {share_var['median']}"
      f"  quartiles {share_var['q1']}-{share_var['q3']}  (n={share_var['n']} groups)")
print("  -> bundle.json['val'] written")
