"""Server-side SVG for the method paper.

The figures are rendered in Python at build time rather than drawn by the page,
for two reasons: a document has no interactive state to drive, and the explorer's
whole class of null-container defects cannot occur in markup that is already final.

Every figure takes its numbers from data/bundle.json. Nothing here is typed by hand.
"""
import math

# palette tokens, so the figures follow the site's light/dark themes
INK, MUTED, GRID, AXIS = "var(--ink)", "var(--muted)", "var(--grid)", "var(--axis)"
BRAND, SERIES, GOOD, WARN, CRIT = "var(--brand)", "var(--series)", "var(--good)", "var(--warn)", "var(--crit)"
DEEMPH, CARD, GOLD = "var(--deemph)", "var(--card)", "var(--gold)"
RAMP = [f"var(--r{i})" for i in range(1, 8)]


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Fig:
    """A plot area with room reserved for its outermost labels.

    The drawing owns its viewBox (see frame() in the explorer): a hand-written one
    silently clips, which is exactly how the bottom tick row was lost there.
    """

    def __init__(self, w, h, ml=52, mr=18, mt=18, mb=46):
        self.w, self.h = w, h
        self.ml, self.mr, self.mt, self.mb = ml, mr, mt, mb
        self.pw, self.ph = w - ml - mr, h - mt - mb
        self.parts = []

    def add(self, s):
        self.parts.append(s)
        return self

    def line(self, x1, y1, x2, y2, stroke=GRID, w=1, dash=None, cap=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        c = f' stroke-linecap="{cap}"' if cap else ""
        return self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                        f'stroke="{stroke}" stroke-width="{w}"{d}{c}/>')

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=1):
        if w <= 0 or h <= 0:
            return self
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        return self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
                        f'rx="{rx}" fill="{fill}"{s}/>')

    def circle(self, cx, cy, r, fill, stroke=None, sw=2, op=None):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' opacity="{op}"' if op is not None else ""
        return self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"{s}{o}/>')

    def path(self, d, stroke=SERIES, w=2, fill="none", op=None):
        o = f' opacity="{op}"' if op is not None else ""
        return self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" '
                        f'stroke-linejoin="round" stroke-linecap="round"{o}/>')

    def text(self, x, y, t, size=11, fill=MUTED, anchor="middle", weight=None, rot=None):
        w_ = f' font-weight="{weight}"' if weight else ""
        r_ = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
        return self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{fill}" '
                        f'text-anchor="{anchor}"{w_}{r_}>{esc(t)}</text>')

    def ylab(self, t):
        return self.text(13, self.mt + self.ph / 2, t, 11, MUTED, "middle", "600", -90)

    def xlab(self, t):
        return self.text(self.ml + self.pw / 2, self.h - 8, t, 11, MUTED, "middle", "600")

    def svg(self, title, desc=""):
        return (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(title)}" '
                f'xmlns="http://www.w3.org/2000/svg">'
                f'<title>{esc(title)}</title>'
                + (f"<desc>{esc(desc)}</desc>" if desc else "")
                + "".join(self.parts) + "</svg>")


def nice_ticks(lo, hi, n=5):
    """Ticks on a round step, so every label names a value the axis actually reaches."""
    if hi <= lo:
        return [lo]
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min((s for s in (1, 2, 2.5, 5, 10) if s * mag >= raw), default=10) * mag
    t, out = math.ceil(lo / step) * step, []
    while t <= hi + 1e-9:
        out.append(round(t, 10))
        t += step
    return out


def kfmt(v):
    v = float(v)
    if abs(v) >= 1000:
        s = f"{v/1000:.1f}".rstrip("0").rstrip(".")
        return s + "k"
    return f"{v:.0f}"
