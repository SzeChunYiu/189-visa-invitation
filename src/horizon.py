"""Unmodelled dynamic: the pool keeps growing after the snapshot. Does forecast error grow with staleness?"""
import pandas as pd, numpy as np, json, os
os.chdir(os.path.join(os.path.dirname(__file__),"..","data"))
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]; GOOD=["2025-08","2025-11","2026-06"]
SNAP=["09/2024","10/2024","11/2024","12/2024","01/2025","02/2025","03/2025","04/2025","05/2025","06/2025",
      "07/2025","08/2025","09/2025","10/2025","11/2025","12/2025","01/2026","02/2026","03/2026","04/2026",
      "05/2026","06/2026","07/2026","08/2026"]
RD_SNAP={"2025-08":"08/2025","2025-11":"11/2025","2026-06":"06/2026"}
FLOOR=65
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
al=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0)
pl=num(pd.read_csv("pool189only_occ4.csv")); pl["n"]=pl["only"].fillna(0); pl["G"]=pl.Occupation.astype(str).str[:4]
def cutoff(pg,A):
    if A<=0: return None
    s=pg[pg.Score>=FLOOR].sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return FLOOR
print("="*96); print("DOES A STALE POOL BIAS THE FORECAST?  same allocation, pool taken k months earlier"); print("="*96)
print(f"  {'lag':>4}{'cells':>7}{'exact':>8}{'within5':>9}{'MAE':>8}{'bias':>8}")
out={}
for lag in range(0,7):
    errs=[]
    for rd in GOOD:
        si=SNAP.index(RD_SNAP[rd])-lag
        if si<0: continue
        snap=SNAP[si]
        P=pl[pl.AsAt==snap]
        act=inv[(inv.StatusMonth==rd)&(inv.n>0)].groupby("G").Score.min()
        for g,a in act.items():
            pg=P[P.G==g][["Score","n"]]
            if pg.empty: continue
            A=int(al.loc[g,rd]) if g in al.index else 0
            c=cutoff(pg,A)
            if c is None: continue
            errs.append(c-a)
    e=np.array(errs,float)
    if not len(e): continue
    out[lag]=dict(n=len(e),exact=float((e==0).mean()),w5=float((np.abs(e)<=5).mean()),
                  mae=float(np.abs(e).mean()),bias=float(e.mean()))
    print(f"  {lag:>4}{len(e):>7}{100*out[lag]['exact']:>7.0f}%{100*out[lag]['w5']:>8.0f}%{out[lag]['mae']:>8.2f}{out[lag]['bias']:>+8.2f}")
ks=sorted(out); maes=[out[k]["mae"] for k in ks]
print(f"\n  correlation(lag, MAE) = {np.corrcoef(ks,maes)[0,1]:+.3f}")
slope=np.polyfit(ks,maes,1)[0]
print(f"  MAE grows {slope:+.3f} points per month of pool staleness")
print(f"\n  The live forecast uses the 08/2026 snapshot. A round in late Sep is ~1 month stale;")
print(f"  one in Dec is ~4 months. Extra error at 4 months vs 1: {(out.get(4,{}).get('mae',float('nan'))-out.get(1,{}).get('mae',float('nan'))):+.2f} pts")
json.dump({str(k):{kk:round(vv,4) for kk,vv in v.items()} for k,v in out.items()}|
          {"slope_per_month":round(float(slope),4)},open("horizon.json","w"),indent=1)
print("\n  -> horizon.json written")
