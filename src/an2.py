import pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/'data')
import pandas as pd, numpy as np
pd.set_option("display.width",250,"display.max_columns",50)
d=pd.read_csv("inv189only_score.csv")
d=d[d.Score.astype(str).str.fullmatch(r"\d+")].copy()
d["Score"]=d.Score.astype(int); d["n"]=d.n.fillna(0)
d=d[d.n>0]
p=d.pivot_table(index="StatusMonth",columns="Score",values="n",aggfunc="sum").fillna(0)
p=p[sorted(p.columns,reverse=True)]
print("=== TRUE 189 ROUNDS: invitations by points (189-only EOIs, unambiguous) ===")
print(p.astype(int).to_string())
print("\n=== cut-off structure per round ===")
for m,row in p.iterrows():
    tot=row.sum(); nz=row[row>0]
    cum=0; 
    print(f"\n  ROUND {m}  total(189-only)={tot:,.0f}")
    for s in sorted(nz.index,reverse=True):
        cum+=nz[s]
        print(f"     {s:>4} pts : {int(nz[s]):>6,}   cum={int(cum):>6,}  ({100*cum/tot:>5.1f}%)")
print("\n=== DiD attribution: estimating FULL round size incl. multi-leg EOIs ===")
did=pd.read_csv("inv_did.csv"); did=did[did.StatusMonth.astype(str).str.startswith("202")]
did=did.set_index("StatusMonth").sort_index().fillna(0)
rounds=["2024-09","2024-11","2025-08","2025-11","2026-06"]
did["is_round"]=did.index.isin(rounds)
base=did[~did.is_round]
ratio=(base.multi189/base.no189.replace(0,np.nan)).median()
print(f"  baseline multi189/no189 ratio in NON-round months = {ratio:.4f}  (n={len(base)})")
print(f"  {'month':<9}{'multi189':>10}{'no189':>9}{'expected_state':>16}{'excess=189inv':>15}")
tot189={}
for m,r in did.iterrows():
    exp=ratio*r.no189; exc=max(0.0,r.multi189-exp)
    flag=" <ROUND" if m in rounds else ""
    if m in rounds:
        print(f"  {m:<9}{r.multi189:>10,.0f}{r.no189:>9,.0f}{exp:>16,.0f}{exc:>15,.0f}{flag}")
        tot189[m]=exc
only=p.sum(axis=1)
print(f"\n  {'round':<9}{'189-only':>10}{'multi-excess':>14}{'EST TOTAL 189':>15}")
for m in rounds:
    print(f"  {m:<9}{only.get(m,0):>10,.0f}{tot189[m]:>14,.0f}{only.get(m,0)+tot189[m]:>15,.0f}")
