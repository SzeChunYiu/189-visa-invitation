"""The site's navigation, defined once.

Two builders emit pages (build_pages.py for the explorer, build_paper.py for the
method paper). They each carried their own copy of the nav markup, which is how the
method tab ended up styled with var(--accent) — a token defined in neither stylesheet.
Both now call nav_html() here, so a page added or renamed changes one list.
"""

NAV = [
    ("index.html", "Your result"),
    ("worked.html", "Step by step"),
    ("landscape.html", "All occupations"),
    ("policy.html", "Policy"),
    ("findings.html", "Method"),
]

PAGES = [h for h, _ in NAV]


def nav_html(current, theme_button=True):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{n}</a>'
        for h, n in NAV)
    btn = ('<button class="themebtn" id="themebtn" type="button" '
           'aria-pressed="false">Dark</button>') if theme_button else ""
    return f'<nav class="top" aria-label="Sections">{links}{btn}</nav>'
