"""Does the method paper define what it uses?

Two coverage questions, answered against the rendered page rather than from memory:

  symbols  - every symbol that appears in an equation should be named in prose
  concepts - every term the model depends on should be explained somewhere,
             not merely mentioned

Neither is a proof of clarity. Both catch the specific failure of introducing a
symbol or a term and never saying what it is.
"""
import pathlib, re, html, sys

R = pathlib.Path(__file__).resolve().parent.parent
DOC = (R / "docs" / "findings.html").read_text()

# symbol -> the words that would constitute defining it
SYMBOLS = {
    r"A_g":        ["places", "allocation"],
    r"\sigma_g":   ["share"],
    r"\varphi":    ["single-leg", "correction factor"],
    r"a_g":        ["took", "last round"],
    r"c_g":        ["cut-off"],
    r"n_g":        ["number of people", "pool"],
    r"F":          ["legislative minimum", "floor"],
    r"N":          ["round size", "size of the next round"],
    r"s":          ["score", "points"],
    r"d":          ["date of effect"],
    r"g":          ["unit group"],
    r"R":          ["residual"],
    r"e":          ["residual", "error"],
    r"\hat{c}":    ["forecast", "prediction"],
    r"\rho_g":     ["share of your own band", "dated ahead"],
    r"f(N)":       ["distribution", "likely"],
    r"z_g":        ["skip", "receive nothing", "passed over"],
}

# added after the coverage audit found the site was showing three things the paper
# never explained: how much the share moves, the sampling error on the probability,
# and the decomposition itself
CONCEPTS = {
    "share instability":     ["coefficient of variation"],
    "probability sampling error": ["sampling error"],
    "decomposition of the answer": ["chain of deductions", "waterfall"],
    "unit group":            ["four-digit", "ANZSCO"],
    "single-leg":            ["carrying 189 and nothing else", "another subclass"],
    "date of effect":        ["earliest first", "date-of-effect order"],
    "boundary band":         ["lands on", "boundary"],
    "walk the pool":         ["walking down", "walk", "until the places run out", "consumed"],
    "residual / uncertainty":["prediction minus outcome"],
    "walk-forward":          ["immediately before it", "walk-forward"],
    "skip risk":             ["receive nothing", "passed over"],
    "priority tier":         ["four-tier", "tier"],
    "pool snapshot age":     ["snapshot", "stale"],
    "pool drift":            ["strengthen"],
    "invitations per place": ["per place"],
    "calibration vs official":["published table", "official"],
    "share uncertainty":     ["coefficient of variation", "share has ranged", "one round"],
    "curve shape tested":    ["leave-one-out", "cross-validation"],
}


def prose():
    t = re.sub(r"<svg[\s\S]*?</svg>", " ", DOC)
    t = re.sub(r"<script[\s\S]*?</script>", " ", t)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def main():
    text = prose()
    eqs = " ".join(re.findall(r'<div class="eq">([\s\S]*?)</div>', DOC))
    low = text.lower()

    print("=" * 88)
    print("SYMBOLS USED IN EQUATIONS, AND WHETHER THE PROSE NAMES THEM")
    print("=" * 88)
    miss_sym = []
    for sym, words in SYMBOLS.items():
        if sym not in eqs:
            continue
        ok = any(w.lower() in low for w in words)
        print(f"  {sym:<12} {'defined' if ok else 'NOT DEFINED':<14} looked for: {words[0]}")
        if not ok:
            miss_sym.append(sym)

    print()
    print("=" * 88)
    print("CONCEPTS THE MODEL DEPENDS ON")
    print("=" * 88)
    miss_con = []
    for con, words in CONCEPTS.items():
        ok = any(w.lower() in low for w in words)
        print(f"  {con:<26} {'explained' if ok else 'NOT EXPLAINED'}")
        if not ok:
            miss_con.append(con)

    print()
    n = len(SYMBOLS) - len(miss_sym)
    print(f"  symbols defined  : {n}/{sum(1 for k in SYMBOLS if k in eqs)}")
    print(f"  concepts covered : {len(CONCEPTS)-len(miss_con)}/{len(CONCEPTS)}")
    if miss_sym: print(f"  MISSING SYMBOLS  : {miss_sym}")
    if miss_con: print(f"  MISSING CONCEPTS : {miss_con}")
    return 1 if (miss_sym or miss_con) else 0


if __name__ == "__main__":
    sys.exit(main())
