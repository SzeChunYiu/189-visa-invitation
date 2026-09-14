"""Layout for the method wiki: a sticky chapter rail beside a measured column."""
PAPER_CSS = r"""
.paperwrap{display:grid;grid-template-columns:228px minmax(0,1fr);gap:34px;
  max-width:1140px;margin:0 auto;padding:0 20px 72px;align-items:start}
.toc{position:sticky;top:14px;align-self:start;max-height:calc(100vh - 28px);overflow:auto;
  padding:14px 12px;border:1px solid var(--line);border-radius:14px;background:var(--card)}
.toc h3{margin:0 0 10px;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:ch}
.toc li{counter-increment:ch;margin:0 0 1px}
.toc a{display:grid;grid-template-columns:22px minmax(0,1fr);gap:7px;align-items:baseline;
  padding:6px 8px;border-radius:8px;font-size:12.5px;line-height:1.32;
  color:var(--body);text-decoration:none}
.toc a::before{content:counter(ch);font-size:10.5px;color:var(--muted);font-variant-numeric:tabular-nums}
.toc a:hover{background:var(--brand-soft);color:var(--ink)}
.toc a[aria-current="true"]{background:var(--brand);color:#fff;font-weight:600}
.toc a[aria-current="true"]::before{color:rgba(255,255,255,.75)}

.chap{max-width:70ch;min-width:0}
main{min-width:0}
.chap[hidden]{display:none}
.chap .eyebrow{font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;color:var(--brand);
  font-weight:700;margin:0 0 6px}
.chap h2{font-size:26px;line-height:1.16;margin:0 0 14px;letter-spacing:-.015em;text-wrap:balance}
.chap h3{font-size:15px;margin:30px 0 8px;letter-spacing:-.005em}
.chap p{margin:0 0 14px;line-height:1.66}
.chap ul,.chap ol{margin:0 0 14px;padding-left:20px;line-height:1.66}
.chap li{margin:0 0 6px}
.lede{font-size:16.5px;line-height:1.6;color:var(--body)}
.chap code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9em;
  background:var(--brand-soft);padding:1px 5px;border-radius:5px}

figure{margin:26px 0;padding:0}
figure svg{display:block;width:100%;height:auto}
.figbox{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:14px 14px 6px;
  overflow-x:auto}
.figbox>svg{min-width:460px}
figcaption{margin-top:10px;font-size:12.5px;line-height:1.55;color:var(--muted)}
figcaption b{color:var(--ink);font-weight:700}

.figbox [data-tip]{cursor:crosshair}
.figtip{position:fixed;z-index:60;max-width:280px;pointer-events:none;
  background:var(--ink);color:var(--paper);font-size:12px;line-height:1.4;
  padding:7px 10px;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.22)}
.figtip[hidden]{display:none}
.eq{margin:20px 0;padding:14px 16px;border-left:3px solid var(--brand);
  background:var(--brand-soft);border-radius:0 10px 10px 0;overflow-x:auto}
.eq .katex{font-size:1.04em}
.eq .katex-display{margin:0}
.eqn{float:right;color:var(--muted);font-size:12px;font-variant-numeric:tabular-nums}

.chapnav{display:flex;justify-content:space-between;gap:12px;margin:38px 0 0;
  padding-top:18px;border-top:1px solid var(--line)}
.chapnav a{font-size:13px;color:var(--brand);text-decoration:none;max-width:46%}
.chapnav a:hover{text-decoration:underline}
.chapnav .nxt{text-align:right}
.chapnav span{display:block;font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted)}

/* worked example */
.wk{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:16px;margin:22px 0}
.wkin{display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end;margin-bottom:6px}
/* a select sizes to its longest option - 443px here - and a flex child with the
   default min-width:auto cannot shrink below that, so the page scrolled sideways */
.wkin>div{min-width:0}
.wkin select{max-width:100%;text-overflow:ellipsis}
.wkbtns{display:flex;gap:8px;align-items:flex-end;margin-left:auto}
.wkbtns button{font:inherit;font-size:13px;padding:8px 14px;border-radius:9px;cursor:pointer;
  border:1px solid var(--line);background:var(--card);color:var(--ink)}
.wkbtns button:hover{background:var(--brand-soft);border-color:var(--brand)}
.wkbtns button.primary{background:var(--brand);border-color:var(--brand);color:#fff;font-weight:600}
.wkbtns button.primary:hover{filter:brightness(1.08)}
.wkbtns button:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
.linkish{background:none;border:0;padding:0;font:inherit;font-size:12.5px;color:var(--brand);
  text-decoration:underline;cursor:pointer}
.cmph{font-size:15px;margin:30px 0 10px;letter-spacing:-.005em}
table.cmp{width:100%;border-collapse:collapse;font-size:13px;min-width:520px}
table.cmp th,table.cmp td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}
table.cmp th{font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}
table.cmp td.n{text-align:right;font-variant-numeric:tabular-nums}
.wkin label{font-size:11px;color:var(--muted);display:block;margin-bottom:4px}
.wkin input,.wkin select{font:inherit;font-size:13.5px;padding:7px 9px;border:1px solid var(--line);
  border-radius:9px;background:var(--paper);color:var(--ink);min-width:0}
.step{display:grid;grid-template-columns:26px minmax(0,1fr);gap:12px;padding:14px 0;border-top:1px solid var(--line)}
.step:first-of-type{border-top:0}
.stepn{width:24px;height:24px;border-radius:50%;background:var(--brand);color:#fff;
  font-size:11.5px;font-weight:700;display:grid;place-items:center}
.steph{margin:2px 0 6px;font-size:13.5px;font-weight:700;color:var(--ink)}
.stepb{font-size:13px;line-height:1.62;color:var(--body)}
.calc{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;
  background:var(--brand-soft);border-radius:9px;padding:9px 11px;margin:8px 0 0;
  overflow-x:auto;white-space:nowrap;color:var(--ink)}
.calc .res{color:var(--brand);font-weight:700}
.wkout{margin-top:16px;padding:14px 16px;border-radius:12px;background:var(--brand-soft);
  display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.wkout b{font-size:30px;letter-spacing:-.02em;color:var(--ink);font-variant-numeric:tabular-nums}

.chap .tablewrap{overflow-x:auto;margin:16px 0;-webkit-overflow-scrolling:touch}

.chap table.pt{width:100%;border-collapse:collapse;font-size:13px;margin:0;min-width:430px}
table.pt th,table.pt td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}
table.pt th{font-size:10.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}
table.pt td.n{text-align:right;font-variant-numeric:tabular-nums}

@media (max-width:900px){
  .paperwrap{grid-template-columns:minmax(0,1fr);gap:18px}
  .toc{position:static;max-height:none}
  .toc ol{display:flex;flex-wrap:wrap;gap:4px}
  .toc li{margin:0}
  .chap h2{font-size:22px}
}
"""
