# Console check (the reliable guard for undefined-reference bugs)

A static "every called helper is defined" check was attempted in `src/audit.py` and **removed**: the list of
known helpers must be derived from the same file whose definition may have been deleted, so the check passes
exactly when it should fail. A deliberate rename of `queueTable()` went straight through it.

Undefined references are caught by executing the page instead. After any rebuild:

1. Serve `docs/` and open `index.html`.
2. Exercise every control: points input, round-size select, heatmap sort, occupation combobox, a scatter dot
   click, a heatmap row click.
3. Assert the console is empty.

```js
const errs=[];window.addEventListener('error',e=>errs.push(e.message));
// ...drive the controls...
console.log(errs);   // must be []
```

Two real regressions were caught this way and by nothing else: the `allN` element removed while `renderAll`
still wrote to it, and `queueTable`/`policyTable` deleted by a source splice while `render()` still called them.

## Responsive and theme checks (add to the same pass)

Both were skipped for four iterations and each hid a real defect.

**Light theme.** Emulate `prefers-color-scheme: light` and check the heatmap cell annotations (ink flips with
ramp darkness), the status pills, and the takeaway banners. All verified legible.

**Mobile, 375px.** Measure what chart labels actually render at:

```js
const s=document.getElementById('c1'), r=s.getBoundingClientRect();
const vb=s.getAttribute('viewBox').split(' ').map(Number);
10.5 * r.width / vb[2]   // rendered px for a 10.5-unit label
```

A 520-unit viewBox squeezed into a 311px card rendered labels at **6px**. The fix is `.chartwrap{overflow-x:auto}`
with `min-width:470px` on the SVG below 640px, which holds labels at 9.5px and lets the reader scroll sideways.
Assert `document.body.scrollWidth <= innerWidth` so the *page* still never scrolls horizontally.
