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
