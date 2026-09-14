"""Run the whole build in the one order that works.

build_bundle.py writes bundle.json from scratch; validation_detail.py then adds the
per-fold breakdown to it. Running the first alone silently drops the second's work,
and the page builders only notice because num() raises on the missing key. This is
that order, written down and executable.
"""
import subprocess, sys, pathlib

SRC = pathlib.Path(__file__).resolve().parent
STEPS = [
    ("bundle",     "build_bundle.py"),       # writes data/bundle.json
    ("validation", "validation_detail.py"),  # adds bundle["val"] - must follow the bundle
    ("aggregate",  "aggregate_trend.py"),  # adds bundle["agg"] - after validation
    ("explorer",   "build_dash.py"),
    ("pages",      "build_pages.py"),
    ("worked",     "build_worked.py"),
    ("paper",      "build_paper.py"),
    ("claims",     "claims.py"),      # every prose number traceable to the bundle
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
