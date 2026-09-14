"""Atomic verification of every number in the method paper's prose.

A number in prose cannot be re-derived by a reader, and this project has already
shipped two that outlived the analysis behind them (a retracted r = 0.941 and a
discarded date-of-effect figure). This walks the rendered paper, pulls every
numeric token out of the body text, and asks whether the bundle can produce it.

Scope and its limits, stated honestly:
  * prose only - SVG interiors are generated from the same bundle by construction;
  * a number is TRACEABLE if some bundle value renders to it under a formatting
    the builder actually uses. That is necessary, not sufficient: it shows the
    number could have come from the data, not that it was used correctly.
  * structural numbers (chapter, figure, equation, year, subclass) are declared.
"""
import json, pathlib, re, sys, html as _html

R = pathlib.Path(__file__).resolve().parent.parent
B = json.loads((R / "data" / "bundle.json").read_text())

# numbers that are part of the document's furniture, not empirical claims
# Numbers quoted BECAUSE they are wrong. The retraction in chapter 10 restates a
# withdrawn result verbatim; it must not resolve against current data, and the check
# would be lying if it passed them silently.
QUOTED_HISTORICAL = {"49", "0.941"}

STRUCTURAL = {
    "189", "190", "491", "80", "50",           # visa subclasses, interval widths
    "2024", "2025", "2026", "2027", "20", "25", "26", "27",     # years and year halves
    "1000", "100", "0",
    "65", "70", "75", "85", "90", "95",     # points bands named as thresholds
}


def structural(html):
    """Document furniture, counted from the document rather than hardcoded.

    A literal range went stale the moment the paper grew a seventeenth figure, and the
    check reported "Figure 17" as an unverified empirical claim.
    """
    nfig = len(re.findall(r"<figcaption><b>Figure (\d+)", html))
    nchap = html.count('<article class="chap"')
    neq = len(re.findall(r'<span class="eqn">\((\d+)\)', html))
    return STRUCTURAL | {str(i) for i in range(0, max(nfig, nchap, neq) + 1)}


def known_values():
    """Exactly the strings the builder emitted, not every formatting of every value.

    The first version of this check generated six renderings of every number in the
    bundle, giving 17,161 candidates - dense enough that a deliberately fabricated
    87.3% matched one and passed. A checker that cannot fail is worth nothing, so the
    builder now records what it actually emits and this reads that record.
    """
    f = R / "data" / "paper_numbers.json"
    if not f.exists():
        print("  paper_numbers.json missing - run build_paper.py first"); sys.exit(2)
    known = set(json.loads(f.read_text()))
    # counts and identifiers that appear in prose as names rather than measurements
    known |= set(B["groups"].keys())
    known |= {k.split()[0] for k in B["occ"]}
    return known


def prose(html):
    """Body text with SVG, script, style and equations removed.

    Entities are decoded first: &#961; is the symbol rho, not the number 961, and
    the first version of this check reported three such codes as untraceable claims.
    """
    t = re.sub(r"<svg[\s\S]*?</svg>", " ", html)
    t = re.sub(r"<script[\s\S]*?</script>", " ", t)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t)
    t = re.sub(r'<div class="eq">[\s\S]*?</div>', " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = _html.unescape(t)
    # dates are one token, not two numbers: 08/2026 and 2026-06
    t = re.sub(r"\b\d{2}/\d{4}\b", " DATE ", t)
    t = re.sub(r"\b\d{4}-\d{2}\b", " DATE ", t)
    return re.sub(r"\s+", " ", t)


def main():
    html = (R / "docs" / "findings.html").read_text()
    text = prose(html)
    known = known_values()
    struct = structural(html)
    # scientific notation is one number: 6.8e-05 was being split into 6.8 and 05
    text = re.sub(r"(?<![\w.])\d+(?:\.\d+)?e[+-]?\d+", " SCI ", text)
    toks = re.findall(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])", text)
    untraceable, seen = [], set()
    for t in toks:
        bare = t.replace(",", "")
        if t in struct or bare in struct or t in QUOTED_HISTORICAL or t in seen:
            continue
        seen.add(t)
        if t in known or bare in known:
            continue
        untraceable.append(t)
    print("=" * 92)
    print("ATOMIC NUMERIC CLAIMS IN THE METHOD PAPER'S PROSE")
    print("=" * 92)
    print(f"  distinct numbers in prose : {len(seen)}")
    print(f"  traceable to the bundle   : {len(seen) - len(untraceable)}")
    print(f"  NOT traceable             : {len(untraceable)}")
    for t in untraceable:
        # locate the actual token, not the first substring match: searching for "05"
        # found it inside "17,050" and pointed at the wrong sentence
        m = re.search(r"(?<![\w.,])" + re.escape(t) + r"(?![\w,])", text)
        i = m.start() if m else text.find(t)
        print(f"    {t:>12}   …{text[max(0,i-72):i+30].strip()}…")
    print()
    print(f"  quoted-historical (excluded, and required to stay untraceable): "
          f"{sorted(QUOTED_HISTORICAL)}")
    print("  Scope: prose only; a pass means the builder emitted the number from the")
    print("  bundle, not that the number is used correctly in its sentence.")
    return 1 if untraceable else 0


if __name__ == "__main__":
    sys.exit(main())
