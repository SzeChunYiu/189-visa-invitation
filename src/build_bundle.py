"""One JSON bundle powering the interactive dashboard: everything for every occupation."""
import pandas as pd, numpy as np, json, pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/"data")
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
SIZES=[5000,7500,10000,12500,15000]
FLOOR=65; FR=5198/10000
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df

db=pd.read_csv("occupation_database.csv")
pool=num(pd.read_csv("pool189only_occ4.csv")); pool["n"]=pool["only"].fillna(0)
pool["G"]=pool.Occupation.astype(str).str[:4]
latest=pool[pool.AsAt=="08/2026"]
inv=num(pd.read_csv("inv189only_occ_score.csv")); inv["n"]=inv.n.fillna(0); inv["G"]=inv.OccGroup.astype(str).str[:4]
alloc=inv[inv.StatusMonth.isin(ROUNDS)].pivot_table(index="G",columns="StatusMonth",values="n",aggfunc="sum").fillna(0).reindex(columns=ROUNDS,fill_value=0).astype(int)
share=alloc["2026-06"]/alloc["2026-06"].sum()
gname=inv.groupby("G").OccGroup.first()
val=json.load(open("validation_singleleg.json")); cal=json.load(open("calibration_official.json"))
mob=json.load(open("mobility.json")); gate=json.load(open("alloc_gate.json"))
pol=json.load(open("policy.json"))
unc=json.load(open("uncertainty.json"))
rs=json.load(open("roundsize.json"))

def cutoff(pg,A):
    if A<=0: return None
    s=pg[pg.Score>=FLOOR].sort_values("Score",ascending=False); c=0
    for _,r in s.iterrows():
        c+=r.n
        if c>=A: return int(r.Score)
    return FLOOR

groups={}
for g in alloc.index:
    pg=latest[latest.G==g].groupby("Score",as_index=False).n.sum()
    if pg.n.sum()==0: continue
    dist={int(r.Score):int(r.n) for _,r in pg.iterrows() if r.n>0}
    groups[g]=dict(name=str(gname.get(g,g)),alloc=[int(alloc.loc[g,r]) for r in ROUNDS],
        share=round(float(share.get(g,0)),6),dist=dist,
        fc=[cutoff(pg,int(round(share.get(g,0)*S*FR))) for S in SIZES])

occ={}
for o,gg in db.groupby("occupation"):
    g=str(o)[:4]
    rounds=[]
    for rd in ROUNDS:
        x=gg[gg["round"]==rd]
        if len(x):
            x=x.iloc[0]
            rounds.append(dict(r=rd,lc=None if pd.isna(x.lowest_cleared_score) else int(x.lowest_cleared_score),
                b=int(x.boundary_score),s=x.boundary_state[0],n=int(x.invited_n)))
        else: rounds.append(dict(r=rd,lc=None,b=None,s="U",n=0))
    lp=latest[latest.Occupation==o]
    occ[o]=dict(g=g,rounds=rounds,pool=int(lp.n.sum()),
                dist={int(r.Score):int(r.n) for _,r in lp.iterrows() if r.n>0})
# occupations present in the pool but never invited still deserve a row
for o,x in latest.groupby("Occupation"):
    if o in occ: continue
    occ[o]=dict(g=str(o)[:4],rounds=[dict(r=r,lc=None,b=None,s="U",n=0) for r in ROUNDS],
                pool=int(x.n.sum()),dist={int(r.Score):int(r.n) for _,r in x.iterrows() if r.n>0})

bundle=dict(rounds=ROUNDS,sizes=SIZES,floor=FLOOR,groups=groups,occ=occ,policy=pol,unc=unc,rs=rs,
  meta=dict(fr=round(FR,6),round_min=6450,round_max=14724,oos_mae=val["oos"]["mae"],oos_within5=val["oos"]["within5"],oos_bias=val["oos"]["bias"],
            mech_exact=val["mech"]["exact"],cal_exact=round(cal["exact"]/cal["n"],3),cal_n=cal["n"],
            official_total=cal["official_total"],mobility=mob["pct_changed"],alloc_r=gate["pooled_r"],
            snapshot="08/2026",last_round="2026-06"))
json.dump(bundle,open("bundle.json","w"),separators=(",",":"))
sz=pathlib.Path("bundle.json").stat().st_size
print(f"occupations: {len(occ)}   groups: {len(groups)}   bundle: {sz/1024:.0f} KB")
print(f"physicist rounds: {occ['234914 Physicist']['rounds']}")
print(f"2349 forecast: {groups['2349']['fc']}  alloc {groups['2349']['alloc']}")
