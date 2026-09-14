# Deploying

The site is **fully static** — the whole dataset (199 occupations, 82 unit groups, all five rounds,
forecasts) is an 88 KB JSON bundle compiled into `docs/index.html` at build time. There is no server,
no API and no database, so **Supabase is not needed**. If the dashboard later grows features that must
persist across visitors — saved profiles, alerts when a round is announced, a comments thread — that is
when a database earns its place.

## GitHub Pages (live now)

Serves `docs/` on push to `main`: <https://szechunyiu.github.io/189-visa-invitation/>

## Vercel

`vercel.json` points Vercel at `docs/` with no build step. From the repo root:

```bash
vercel login
```

```bash
vercel deploy --prod
```

The CLI on this machine is 50.39.0 and its stored token has expired, which is why `vercel login` comes
first. Worth upgrading while you are there:

```bash
npm i -g vercel@latest
```

## Rebuilding the pages

Both pages are generated, never hand-edited:

```bash
python3 src/build_bundle.py && python3 src/build_dash.py && python3 src/build_dashboard.py
```

- `src/build_bundle.py` → `data/bundle.json` (the dataset the dashboard reads)
- `src/build_dash.py` → `docs/index.html` (the interactive explorer)
- `src/build_dashboard.py` → `docs/findings.html` (the written analysis)
