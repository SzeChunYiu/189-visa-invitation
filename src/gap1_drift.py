"""GAP 1+2: is the pool getting stronger over time, and do the point components drive it?"""
import pandas as pd, numpy as np, json, os
os.chdir(os.path.join(os.path.dirname(__file__),"..","data"))
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
p=num(pd.read_csv("pool189_occ_score.csv")); p["n"]=p.n.fillna(0)
p=p[p.AsAt.astype(str).str.contains("/")]
p["d"]=pd.to_datetime(p.AsAt,format="%m/%Y")
tot=p.groupby("d").n.sum()
print("="*98); print("GAP 1  IS THE POOL GETTING STRONGER?  mean and upper tail of the score distribution"); print("="*98)
g=p.groupby("d").apply(lambda z:pd.Series({
    "n":z.n.sum(),
    "mean":(z.Score*z.n).sum()/z.n.sum(),
    "p90":np.interp(.9,np.cumsum(z.groupby("Score").n.sum().sort_index())/z.n.sum(),
                    sorted(z.Score.unique())),
    "share85":z[z.Score>=85].n.sum()/z.n.sum(),
    "share90":z[z.Score>=90].n.sum()/z.n.sum()}),include_groups=False)
g=g.sort_index()
print(f"  {'snapshot':<10}{'pool':>9}{'mean pts':>10}{'share >=85':>12}{'share >=90':>12}")
for d,r in g.iloc[::4].iterrows():
    print(f"  {d:%m/%Y}   {r.n:>9,.0f}{r['mean']:>10.2f}{100*r.share85:>11.1f}%{100*r.share90:>11.1f}%")
x=np.arange(len(g))
for col in ["mean","share85","share90"]:
    sl,ic=np.polyfit(x,g[col],1)
    r=np.corrcoef(x,g[col])[0,1]
    unit="pts/month" if col=="mean" else "pp/month"
    v=sl if col=="mean" else sl*100
    print(f"\n  {col:<9} trend {v:+.4f} {unit}   r={r:+.3f}")
print("\n  Over the 24 months the mean score moved {:+.2f} points in total.".format(g["mean"].iloc[-1]-g["mean"].iloc[0]))
print("  share>=85 moved {:+.1f} percentage points.".format(100*(g.share85.iloc[-1]-g.share85.iloc[0])))

print("\n"+"="*98); print("GAP 2  DO THE POINT COMPONENTS EXPLAIN IT?  composition at 85+ vs below"); print("="*98)
def comp(fn,col,top):
    d=num(pd.read_csv(fn)); d["n"]=d.n.fillna(0); d[col]=d[col].astype(str)
    hi=d[d.Score>=85]; lo=d[(d.Score>=65)&(d.Score<85)]
    f=lambda z: z[z[col].isin(top)].n.sum()/max(1,z.n.sum())
    return f(hi),f(lo)
for lbl,fn,col,top in [("max English (20 pts)","atoms_eng.csv","Eng",["20"]),
                       ("partner skills (10 pts)","atoms_partner.csv","Partner",["10"]),
                       ("Australian study","atoms_study.csv","AusStudy",["Y"])]:
    a,b=comp(fn,col,top)
    print(f"  {lbl:<26} at 85+: {100*a:>5.1f}%    at 65-84: {100*b:>5.1f}%    gap {100*(a-b):>+5.1f}pp")
print("\n  These are the levers that separate an 85+ profile from the rest of the pool.")
# the monthly series itself, so the choice of a straight line can be tested
g.reset_index().assign(d=lambda z:z.d.dt.strftime("%Y-%m")).to_csv("drift_series.csv",index=False)
json.dump(dict(mean_trend_per_month=float(np.polyfit(x,g["mean"],1)[0]),
  share85_trend_pp_per_month=float(np.polyfit(x,g.share85,1)[0]*100),
  mean_start=float(g["mean"].iloc[0]),mean_end=float(g["mean"].iloc[-1]),
  share85_start=float(g.share85.iloc[0]),share85_end=float(g.share85.iloc[-1])),
  open("drift.json","w"),indent=1)
print("\n  -> drift.json written")
