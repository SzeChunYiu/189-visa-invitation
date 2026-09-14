"""Run the whole build in the one order that works.

build_bundle.py writes bundle.json from scratch; validation_detail.py then adds the
per-fold breakdown to it. Running the first alone silently drops the second's work,
and the page builders only notice because num() raises on the missing key. This is
that order, written down and executable.
"""
import subprocess, sys, pathlib

SRC = pathlib.Path(__file__).resolve().parent
# The analysis layer. build_bundle.py reads sixteen json files; until now not one of
# them was rebuilt by this pipeline, so editing a fit left the site serving the old
# numbers and the build still said OK. Three inputs stay out: uncertainty.json is
# produced from bundle.json and so cannot precede it, and horizon_corr.json and
# switch.json have no producing script at all. audit.py now names those three rather
# than letting the gap go unrecorded.
REFIT = [
    ("policy",     "policy.py"),             # policy.json - read by roundsize.py
    ("roundsize",  "roundsize.py"),
    ("zero_risk",  "zero_risk.py"),
    ("tiers",      "tiers.py"),
    ("mechanism",  "mechanism.py"),
    ("movement",   "movement.py"),
    ("horizon",    "horizon.py"),
    ("mobility",   "mobility_model.py"),
    ("alloc_gate", "alloc_all.py"),
    ("drift",      "gap1_drift.py"),
    ("gaps",       "gap2_rest.py"),
    ("official",   "calibrate_official.py"),
    ("singleleg",  "universal_validation.py"),
]

STEPS = REFIT + [
    ("bundle",     "build_bundle.py"),       # writes data/bundle.json
    ("validation", "validation_detail.py"),  # adds bundle["val"] - must follow the bundle
    ("aggregate",  "aggregate_trend.py"),  # adds bundle["agg"] - after validation
    ("curves",     "curve_forms.py"),    # tests the two fitted shapes, writes ["curves"]
    ("explorer",   "build_dash.py"),
    ("pages",      "build_pages.py"),
    ("worked",     "build_worked.py"),
    ("paper",      "build_paper.py"),
    ("claims",     "claims.py"),      # every prose number traceable to the bundle
    ("concepts",   "concepts.py"),   # every symbol and concept the paper uses is defined
    ("audit",      "audit.py"),
]

fail = 0
for name, script in STEPS:
    r = subprocess.run([sys.executable, str(SRC / script)], capture_output=True, text=True)
    tail = (r.stdout or "").strip().splitlines()
    ok = r.returncode == 0
    print(f"  [{'ok ' if ok else 'FAIL'}] {name:<11} {tail[-1][:88] if tail else ''}")
    if not ok:
        fail += 1
        print((r.stderr or "").strip()[-900:])
        break
print("BUILD OK" if not fail else "BUILD FAILED")
sys.exit(1 if fail else 0)
