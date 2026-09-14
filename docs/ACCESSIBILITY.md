# Accessibility

## The trap I built and removed

The tooltip helper set `tabindex="0"` on every hoverable mark. With 410 heatmap cells, 62 scatter dots and the
bar/line hit targets, the page had **525 tab stops, 518 of them inside charts**. A keyboard user would have
pressed Tab more than five hundred times to get past the graphics.

That is worse than no keyboard support. Charts are now **pointer-only and `aria-hidden`**, and every number in
them is reachable another way:

| Chart | Where the same numbers live |
|---|---|
| Would you have got in before? | Round-by-round table |
| How many people are ahead of you | The exact head-count table |
| Your chance vs invitations | The takeaway sentence, and the CSV |
| The whole landscape | Every-occupation table, and the CSV |
| Why some occupations need more points | Every-occupation table, and the CSV |

**Tab stops now: 8** — skip link, two header/footer links, occupation, points, sort, download, footer link.

## Keyboard

The occupation picker is a real combobox, not a text box with a mouse menu:

- `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant`
- **↓ / ↑** move through matches, **Home / End** jump to the ends
- **Enter** selects the highlighted match
- **Escape** closes and restores the current occupation
- options carry `role="option"` and `aria-selected`

A **skip link** jumps straight to the result, so a keyboard user does not traverse the filters to read the answer.
`:focus-visible` outlines are defined for every control.

## Colour

No result rests on colour alone:

- Verdict flags pair colour with an icon **and** a word ("✓ Likely invited", "✕ Unlikely at this score").
- Heatmap cells print the cut-off value in every cell; colour is redundant encoding.
- Round-by-round and occupation tables carry text labels ("fully cleared", "rationed by date") beside every pill.
- Charts use one hue plus a de-emphasis grey — the emphasis pattern — rather than a categorical palette needing
  colour discrimination.

Status colours are reserved for good/warning/critical and never reused as a series colour.

## Still to verify

Tested with automation, not with a real screen reader. The chart `<title>` elements and table semantics should be
checked with VoiceOver or NVDA before claiming conformance.
