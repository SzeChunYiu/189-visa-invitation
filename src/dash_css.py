CSS = """
:root{
  --paper:#faf8f4; --card:#ffffff; --ink:#221d18; --body:#4a4238; --muted:#6e6459; --line:#e6e0d6;
  --brand:#2f6f5e; --brand-soft:#e7f0ec;
  --series:#1479a8; --series-soft:rgba(20,121,168,.12); --deemph:#cfc6b8;
  --gold:#b97a0e;--c3:#7d4f9c; --gold-soft:#fbf1dd;
  --good:#0ca30c; --warn:#fab219; --crit:#d03b3b;
  --good-bg:#e8f6e8; --warn-bg:#fdf3de; --crit-bg:#fbeaea;
  --grid:#ece6dc; --axis:#cfc6b8;
  --r1:#dda288; --r2:#d38867; --r3:#c96e47; --r4:#b25a34; --r5:#91492a; --r6:#703821; --r7:#4f2817;
  --shadow:0 1px 2px rgba(34,29,24,.05), 0 10px 28px -20px rgba(34,29,24,.3);
}
/* Light is the default. Dark is opt-in via the toggle (data-theme="dark"),
   so an OS dark setting does not override the intended palette. */
:root[data-theme="dark"]{
  --paper:#17140f; --card:#211c16; --ink:#f3efe8; --body:#d3cabd; --muted:#9c9084; --line:#302a22;
  --brand:#6fbfa3; --brand-soft:#1a2f28;
  --series:#4faed4; --series-soft:rgba(79,174,212,.18); --deemph:#3d362d;
  --gold:#e8b341;--c3:#9d78c8; --gold-soft:#332912;
  --good:#0ca30c; --warn:#fab219; --crit:#e06b6b;
  --good-bg:#12301a; --warn-bg:#332a14; --crit-bg:#3a1f1f;
  --grid:#292319; --axis:#3d362d;
  --r1:#f4e0d7; --r2:#e8c1b0; --r3:#dda288; --r4:#d18361; --r5:#c66339; --r6:#9e502e; --r7:#773c22;
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
.f input:focus-visible,.f select:focus-visible,button:focus-visible,a:focus-visible,
select:focus-visible{outline:2px solid var(--brand);outline-offset:2px;border-radius:4px}
.f input:focus,.f select:focus{outline:2px solid var(--brand);outline-offset:1px}
.opts div[aria-selected="true"]{background:var(--brand-soft);color:var(--ink);font-weight:600}
.skip{position:absolute;left:-9999px;top:0;background:var(--card);color:var(--ink);padding:9px 14px;
  border:1px solid var(--brand);border-radius:0 0 8px 0;z-index:99}
.skip:focus{left:0}
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
:root[data-theme="dark"] .vflag.warn{color:var(--warn)}
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
.lev{margin:0 0 12px}
.lrow{display:grid;grid-template-columns:150px 1fr 38px 1fr 38px;gap:8px;align-items:center;margin-bottom:5px}
.llab{font-size:11.5px;color:var(--body)}
.lbar{height:9px;border-radius:999px;background:var(--line);overflow:hidden}
.lbar i{display:block;height:100%;background:var(--series);border-radius:999px}
.lbar.dim i{background:var(--deemph)}
.lval{font-size:10.5px;color:var(--ink);font-variant-numeric:tabular-nums;text-align:right}
.lval.dim{color:var(--muted)}
@media(max-width:640px){.lrow{grid-template-columns:110px 1fr 34px}.lrow .lbar.dim,.lrow .lval.dim{display:none}}
.movestrip{margin:0 0 12px}
.mbar{display:flex;height:16px;border-radius:5px;overflow:hidden;gap:2px}
.mbar>div{display:flex;align-items:center;justify-content:center;font-size:9.5px;font-weight:700;color:#fff}
.mkey{display:flex;gap:13px;flex-wrap:wrap;font-size:10.5px;color:var(--muted);margin-top:6px;align-items:center}
.mkey i{width:9px;height:9px;border-radius:2px;display:inline-block;margin-right:4px;vertical-align:-1px}
.takeaway{margin:0 0 10px;font-size:13px;line-height:1.45;color:var(--ink);
  background:var(--brand-soft);border-left:3px solid var(--brand);padding:8px 11px;border-radius:0 7px 7px 0}
.takeaway b{font-weight:700}
.takeaway.good{background:var(--good-bg);border-left-color:var(--good)}
.takeaway.warn{background:var(--warn-bg);border-left-color:var(--warn)}
.takeaway.crit{background:var(--crit-bg);border-left-color:var(--crit)}
#pop{position:fixed;z-index:120;max-width:340px;background:var(--card);color:var(--body);
  border:1px solid var(--line);border-radius:11px;padding:14px 16px;box-shadow:0 8px 40px -8px rgba(0,0,0,.4);
  font-size:12.5px;line-height:1.5;display:none}
#pop.on{display:block}
#pop h4{margin:0 0 7px;font-size:12px;color:var(--ink);letter-spacing:.02em}
#pop button{position:absolute;top:8px;right:9px;appearance:none;border:0;background:none;color:var(--muted);
  font-size:16px;line-height:1;cursor:pointer;padding:2px 5px;border-radius:5px}
#pop button:hover{color:var(--ink);background:var(--line)}
#popbd{position:fixed;inset:0;z-index:110;display:none}
#popbd.on{display:block}
.q{appearance:none;border:1px solid var(--line);background:var(--paper);color:var(--muted);
  width:19px;height:19px;border-radius:50%;font:inherit;font-size:11px;font-weight:700;line-height:1;
  cursor:pointer;padding:0;flex:0 0 auto}
.q:hover{border-color:var(--brand);color:var(--brand)}
.q[aria-expanded="true"]{background:var(--brand);border-color:var(--brand);color:#fff}
.chead{align-items:center}
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
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-top:10px}
.tablewrap table{min-width:400px;margin:0}
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
  clip:rect(0 0 0 0);white-space:nowrap;border:0}
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
nav.top{display:flex;gap:4px;align-items:center;flex-wrap:wrap;margin-bottom:2px}
nav.top a{font-size:12.5px;padding:6px 12px;border-radius:8px;color:var(--body);text-decoration:none;
  border:1px solid transparent}
nav.top a:hover{background:var(--brand-soft);color:var(--ink)}
nav.top a[aria-current="page"]{background:var(--brand);color:#fff;font-weight:600}
.themebtn{margin-left:auto;appearance:none;border:1px solid var(--line);background:var(--card);color:var(--muted);
  border-radius:8px;padding:6px 10px;font:inherit;font-size:12px;cursor:pointer}
.themebtn:hover{color:var(--ink);border-color:var(--brand)}
footer{border-top:1px solid var(--line);padding-top:16px;font-size:11.5px;color:var(--muted)}
footer a{color:var(--brand)}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""
