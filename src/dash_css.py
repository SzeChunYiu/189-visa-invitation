CSS = """
:root{
  --paper:#f7f8f7; --card:#ffffff; --ink:#101418; --body:#38414b; --muted:#6b7684; --line:#e3e7e5;
  --brand:#2f6f5e; --brand-soft:#e9f1ee;
  --series:#2a78d6; --series-soft:rgba(42,120,214,.12); --deemph:#c9ced6;
  --good:#0ca30c; --warn:#fab219; --crit:#d03b3b;
  --good-bg:#e8f6e8; --warn-bg:#fdf3de; --crit-bg:#fbeaea;
  --grid:#e8ebe9; --axis:#c8cfcb;
  --shadow:0 1px 2px rgba(16,20,24,.05), 0 10px 28px -20px rgba(16,20,24,.3);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0d1014; --card:#161b21; --ink:#eef2f6; --body:#c0c8d2; --muted:#8a94a1; --line:#242c34;
  --brand:#63b39b; --brand-soft:#16302a;
  --series:#3987e5; --series-soft:rgba(57,135,229,.18); --deemph:#3a444f;
  --good:#0ca30c; --warn:#fab219; --crit:#e06b6b;
  --good-bg:#12301a; --warn-bg:#332a14; --crit-bg:#3a1f1f;
  --grid:#222a32; --axis:#39434d;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 12px 32px -22px rgba(0,0,0,.8);
}}
:root[data-theme="dark"]{
  --paper:#0d1014; --card:#161b21; --ink:#eef2f6; --body:#c0c8d2; --muted:#8a94a1; --line:#242c34;
  --brand:#63b39b; --brand-soft:#16302a;
  --series:#3987e5; --series-soft:rgba(57,135,229,.18); --deemph:#3a444f;
  --good:#0ca30c; --warn:#fab219; --crit:#e06b6b;
  --good-bg:#12301a; --warn-bg:#332a14; --crit-bg:#3a1f1f;
  --grid:#222a32; --axis:#39434d;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 12px 32px -22px rgba(0,0,0,.8);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--body);
  font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1240px;margin:0 auto;padding:26px 20px 72px;display:flex;flex-direction:column;gap:20px}
h1,h2,h3{margin:0;color:var(--ink);letter-spacing:-.015em;text-wrap:balance}
h1{font-size:23px;font-weight:700}
h2{font-size:15px;font-weight:650}
h3{font-size:12px;font-weight:650}
.eyebrow{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:650}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;
  border-bottom:1px solid var(--line);padding-bottom:16px}
header a{color:var(--brand);font-size:13px}
/* ---- filter row: one row above everything ---- */
.filters{display:grid;grid-template-columns:minmax(260px,2.2fr) minmax(110px,.7fr) minmax(150px,1fr);
  gap:12px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;box-shadow:var(--shadow)}
@media(max-width:760px){.filters{grid-template-columns:1fr}}
.f label{display:block;font-size:11px;color:var(--muted);margin-bottom:5px;font-weight:600}
.f input,.f select{width:100%;padding:9px 11px;border:1px solid var(--line);border-radius:8px;
  background:var(--paper);color:var(--ink);font:inherit;font-size:14px}
.f input:focus,.f select:focus{outline:2px solid var(--brand);outline-offset:1px}
.combo{position:relative}
.opts{position:absolute;z-index:40;top:100%;left:0;right:0;max-height:300px;overflow-y:auto;margin-top:4px;
  background:var(--card);border:1px solid var(--line);border-radius:9px;box-shadow:var(--shadow);display:none}
.opts.on{display:block}
.opts div{padding:8px 11px;font-size:13.5px;cursor:pointer;color:var(--body)}
.opts div:hover,.opts div.sel{background:var(--brand-soft);color:var(--ink)}
/* ---- verdict ---- */
.verdict{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:0;
  background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:var(--shadow)}
@media(max-width:860px){.verdict{grid-template-columns:1fr}}
.vmain{padding:22px 24px;border-right:1px solid var(--line)}
@media(max-width:860px){.vmain{border-right:0;border-bottom:1px solid var(--line)}}
.vflag{display:inline-flex;align-items:center;gap:8px;padding:5px 12px;border-radius:999px;
  font-size:12.5px;font-weight:700;letter-spacing:.02em}
.vflag.good{background:var(--good-bg);color:var(--good)} .vflag.warn{background:var(--warn-bg);color:#8a6412}
.vflag.crit{background:var(--crit-bg);color:var(--crit)}
:root[data-theme="dark"] .vflag.warn,
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .vflag.warn{color:var(--warn)}}
.hero{font-size:46px;font-weight:750;color:var(--ink);line-height:1.05;margin:12px 0 2px}
.vsub{font-size:14px;color:var(--body);max-width:60ch}
.vside{padding:22px 24px;display:flex;flex-direction:column;gap:13px;justify-content:center}
.meter{margin-top:14px}
.mtrack{height:9px;border-radius:999px;background:var(--deemph);overflow:hidden;position:relative}
.mfill{height:100%;border-radius:999px;background:var(--series)}
.mlab{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:11px;color:var(--muted);margin-top:5px}
.mlab span:last-child{text-align:right}
dl.kv{display:flex;justify-content:space-between;gap:14px;align-items:baseline;margin:0;font-size:13px}
dl.kv dt{color:var(--muted)} dl.kv dd{margin:0;color:var(--ink);font-weight:650;font-variant-numeric:tabular-nums}
/* ---- tiles + charts ---- */
.scen{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.scard{border:1px solid var(--line);border-radius:10px;padding:12px 13px;position:relative;background:var(--paper)}
.scard.mid{border-width:2px;border-color:var(--brand);background:var(--brand-soft)}
.scard.good .spct{color:var(--good)} .scard.warn .spct{color:#8a6412}
:root[data-theme="dark"] .scard.warn .spct{color:var(--warn)} .scard.crit .spct{color:var(--crit)}
.scard.n .spct{color:var(--muted)}
.spct{font-size:28px;font-weight:750;line-height:1.05;font-variant-numeric:tabular-nums}
.ssub{font-size:12px;color:var(--body);margin-top:2px}
.scut{font-size:10.5px;color:var(--muted);margin-top:4px;font-variant-numeric:tabular-nums}
.stag{font-size:9.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--brand);font-weight:700;margin-top:7px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:12px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 15px;box-shadow:var(--shadow)}
.tval{font-size:26px;font-weight:700;color:var(--ink);line-height:1.1}
.tlab{font-size:11.5px;color:var(--muted);margin-top:3px;line-height:1.35}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 17px 12px;box-shadow:var(--shadow)}
.chead{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:10px}
.takeaway{margin:0 0 10px;font-size:13px;line-height:1.45;color:var(--ink);
  background:var(--brand-soft);border-left:3px solid var(--brand);padding:8px 11px;border-radius:0 7px 7px 0}
.takeaway b{font-weight:700}
.takeaway.good{background:var(--good-bg);border-left-color:var(--good)}
.takeaway.warn{background:var(--warn-bg);border-left-color:var(--warn)}
.takeaway.crit{background:var(--crit-bg);border-left-color:var(--crit)}
.note{font-size:11.5px;color:var(--muted);margin:8px 0 0;line-height:1.45}
svg{width:100%;height:auto;display:block;overflow:visible}
.chartwrap{overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch}
/* Below this width an SVG scaled to fit would render its 10.5px labels at ~6px.
   Hold a legible minimum and let the reader scroll sideways instead. */
@media(max-width:640px){
  .chartwrap svg{min-width:470px}
  .hm svg{min-width:470px}
  .hm{max-height:360px}
  .hero{font-size:38px}
  .wrap{padding:18px 14px 56px}
  .tiles{grid-template-columns:repeat(auto-fit,minmax(132px,1fr))}
  .chartwrap::after{content:"";display:block;height:2px}
  .mlab{flex-direction:column;gap:2px}
  .mlab span:last-child{text-align:left}
  header{gap:10px}
  header>div:last-child{text-align:left}
}
.gl{stroke:var(--grid);stroke-width:1}
.ax{stroke:var(--axis);stroke-width:1}
.tick{fill:var(--muted);font-size:10.5px;font-variant-numeric:tabular-nums}
.ttl{fill:var(--ink);font-size:11px;font-weight:650}
.ln{fill:none;stroke:var(--series);stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.dot{fill:var(--series);stroke:var(--card);stroke-width:2}
.bar{fill:var(--deemph)} .bar.on{fill:var(--series)}
.refl{stroke:var(--crit);stroke-width:1.5;stroke-dasharray:0}
.reft{fill:var(--crit);font-size:10.5px;font-weight:650}
.vlab{fill:var(--ink);font-size:10.5px;font-weight:650;font-variant-numeric:tabular-nums}
.hit{fill:transparent;cursor:pointer}
#tip{position:fixed;z-index:90;pointer-events:none;display:none;background:var(--card);color:var(--ink);
  border:1px solid var(--line);border-radius:8px;padding:7px 10px;font-size:12px;box-shadow:var(--shadow);max-width:240px}
#tip b{font-size:13.5px;font-variant-numeric:tabular-nums}
#tip span{color:var(--muted);display:block;font-size:11px}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th{font-size:10px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);font-weight:650;
  text-align:right;padding:0 9px 8px;border-bottom:1px solid var(--line);white-space:nowrap}
th:first-child{text-align:left}
td{padding:7px 9px;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums;text-align:right}
td:first-child{text-align:left;color:var(--ink)}
tbody tr:last-child td{border-bottom:0}
tbody tr.hl{background:var(--brand-soft)}
.scroll{overflow-x:auto}
.pill{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:999px;font-size:11.5px;font-weight:650}
.pill.good{background:var(--good-bg);color:var(--good)} .pill.warn{background:var(--warn-bg);color:#8a6412}
.pill.crit{background:var(--crit-bg);color:var(--crit)} .pill.n{background:var(--line);color:var(--muted)}
.cell{stroke:var(--card);stroke-width:2;cursor:pointer}
.cell:hover{stroke:var(--ink);stroke-width:2}
.rowlab{fill:var(--body);font-size:10.5px;dominant-baseline:middle}
.rowlab.on{fill:var(--ink);font-weight:700}
.hm{overflow-y:auto;max-height:430px;border:1px solid var(--line);border-radius:9px;padding:8px 4px}
.legend{display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:11px;color:var(--muted);margin-top:9px}
.legend i{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:5px;vertical-align:-1px}
.ramp{display:flex;height:9px;border-radius:3px;overflow:hidden;width:110px}
.ramp span{flex:1}
.pt{stroke:var(--card);stroke-width:1.5}
.pt.on{stroke:var(--ink);stroke-width:2.5}
.wide{grid-column:1/-1}
footer{border-top:1px solid var(--line);padding-top:16px;font-size:11.5px;color:var(--muted)}
footer a{color:var(--brand)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""
