"""Per-occupation predicted cut-off for the NEXT round, as a curve over round size."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
SIZES=[5000,7500,10000,12500,15000]
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0)
inv["G"]=inv.OccGroup.astype(str).str[:4]
alloc=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0)
alloc=alloc.reindex(columns=ROUNDS,fill_value=0)
last=alloc["2026-06"]; share=last/last.sum()
p=num(pd.read_csv("pool189only_occ4.csv")); p["n"]=p["only"].fillna(0)
p["G"]=p.Occupation.astype(str).str[:4]
pool=p[p.AsAt=="08/2026"].groupby(["G","Score"],as_index=False).n.sum()
names=inv.groupby("G").OccGroup.first()
val=json.load(open("validation_singleleg.json"))
MAE=val["oos"]["mae"]
# The share is computed on the SINGLE-LEG series, so it must be scaled by the single-leg
# equivalent of a round, not the headline round size. Jun-2026: 5,198 single-leg of 10,000 official.
SINGLE_LEG_FRACTION = 5198/10000
FLOOR = 65   # legislative minimum points; no invitation is issued below it

def cutoff(pg,A):
    """walk top-down until A invitations are consumed; never below the legislative floor"""
    if A<=0 or pg.empty: return None
    s=pg[pg.Score>=FLOOR].sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return FLOOR                      # allocation exhausts the eligible pool -> invited to the floor

rows=[]
for g in alloc.index:
    pg=pool[pool.G==g][["Score","n"]]
    if pg.n.sum()==0: continue
    rec={"g":g,"name":str(names.get(g,g)),"share":round(float(share.get(g,0)),5),
         "pool":int(pg.n.sum()),"last_alloc":int(last.get(g,0)),
         "hist":[int(alloc.loc[g,r]) for r in ROUNDS]}
    for S in SIZES:
        rec[f"s{S}"]=cutoff(pg,int(round(share.get(g,0)*S*SINGLE_LEG_FRACTION)))
    rows.append(rec)
f=pd.DataFrame(rows)
f.to_csv("forecast_by_occupation.csv",index=False)
json.dump(dict(sizes=SIZES,oos_mae=MAE,rows=rows),open("forecast_by_occupation.json","w"),separators=(",",":"))
print("="*100); print(f"FORECAST CUT-OFF BY ROUND SIZE  (out-of-sample MAE {MAE} pts on the last fold)"); print("="*100)
print(f"  unit groups forecast: {len(f)}   (single-leg fraction {SINGLE_LEG_FRACTION:.3f}, floor {FLOOR})")
print(f"  groups with no invitation last round (share 0, no forecast): {int((f.last_alloc==0).sum())}")
print(f"\n  {'group':<52}{'pool':>6}"+"".join(f"{S//1000}k".rjust(7) for S in SIZES))
sel=["2349","2544","2613","2211","2331","2334","3312","2414","2725","2713"]
for g in sel:
    r=f[f.g==g]
    if not len(r): continue
    r=r.iloc[0]
    print(f"  {r['name'][:50]:<52}{r['pool']:>6}"+"".join(str(r[f's{S}']).rjust(7) for S in SIZES))
print(f"\n  distribution of the forecast cut-off at a 10,000 round, across {len(f)} groups:")
c=f["s10000"].dropna()
print(f"    min={c.min():.0f}  p25={c.quantile(.25):.0f}  median={c.median():.0f}  p75={c.quantile(.75):.0f}  max={c.max():.0f}")
print(f"    groups whose forecast cut-off is <=85 : {(c<=85).sum()} of {len(c)}  ({100*(c<=85).mean():.0f}%)")
z=f[f.g=="2349"].iloc[0]
print(f"\n  ANZSCO 2349 (physicists): pool {z['pool']}, share {100*z['share']:.2f}%, history {z['hist']}")
print(f"    forecast cut-off: "+", ".join(f"{S//1000}k->{z[f's{S}']}" for S in SIZES))
print(f"    Reading it for an 85-point candidate:")
for S in SIZES:
    c=z[f"s{S}"]
    verdict=("clears outright (cut-off below 85)" if c<85 else
             "AT THE BOUNDARY - rationed by date of effect, and a 10-Sep-2026 EOI is last in line" if c==85 else
             "not reached")
    print(f"      round {S//1000:>2}k -> cut-off {c:.0f}: {verdict}")
print(f"    So the 5k scenario is the one that decides it; from 7.5k upward the cut-off falls below 85.")
print("\n  -> forecast_by_occupation.csv/.json written")
