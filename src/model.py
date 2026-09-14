import pathlib, os
os.chdir(pathlib.Path(__file__).resolve().parent.parent/'data')
import pandas as pd, numpy as np, json
ROUNDS=["2024-09","2024-11","2025-08","2025-11","2026-06"]
PRIOR={"2024-09":"09/2024","2024-11":"10/2024","2025-08":"07/2025","2025-11":"10/2025","2026-06":"05/2026"}
SAME={"2024-09":"09/2024","2024-11":"11/2024","2025-08":"08/2025","2025-11":"11/2025","2026-06":"06/2026"}
def num(df,c="Score"):
    df=df[df[c].astype(str).str.fullmatch(r"\d+")].copy(); df[c]=df[c].astype(int); return df
invo=num(pd.read_csv("inv189only_occ4_score.csv")); invo["n"]=invo.n.fillna(0)
poolo=num(pd.read_csv("pool189only_occ4.csv")); poolo["only"]=poolo["only"].fillna(0)
inva=num(pd.read_csv("inv189only_score.csv")); inva["n"]=inva.n.fillna(0)
st=lambda df,c: df[df.Occupation.astype(str).str.startswith(c)]
STRATA={"Physicist 234914":("234914",),"Unit group 2349":("2349",)}
out={"rounds":ROUNDS}

print("="*100)
print("MODEL 1 - OCCUPATION-CONDITIONAL CUT-OFF  (minimum points invited, 189-only EOIs)")
print("="*100)
print(f"  {'round':<10}{'round size':>12}{'ALL-occ cutoff':>16}{'2349 cutoff':>13}{'Physicist cutoff':>18}")
rows=[]
for rd in ROUNDS:
    tot=inva[inva.StatusMonth==rd].n.sum()
    ca=inva[(inva.StatusMonth==rd)&(inva.n>0)].Score.min()
    cg=st(invo,("2349",)); cg=cg[(cg.StatusMonth==rd)&(cg.n>0)].Score.min()
    cp=st(invo,("234914",)); cp=cp[(cp.StatusMonth==rd)&(cp.n>0)].Score.min()
    rows.append(dict(round=rd,size=int(tot),cut_all=int(ca),cut_2349=int(cg),cut_phys=int(cp)))
    print(f"  {rd:<10}{tot:>12,.0f}{ca:>16.0f}{cg:>13.0f}{cp:>18.0f}")
out["cutoffs"]=rows
cg=[r["cut_2349"] for r in rows]
print(f"\n  2349 cut-off trajectory: {cg}  -> monotone non-increasing: {all(cg[i]>=cg[i+1] for i in range(len(cg)-1))}")
print(f"  Last 2 rounds cut-off <= 85 for the physics stratum: {sum(c<=85 for c in cg[-2:])}/2")

print("\n"+"="*100)
print("MODEL 2 - STRATUM CLEARANCE AT 85 PTS  (denominator bracketed: pre-round vs round-month pool)")
print("="*100)
clear={}
for name,codes in STRATA.items():
    iv=st(invo,codes); pl=st(poolo,codes)
    print(f"\n  ### {name}")
    print(f"  {'round':<10}{'pool85_pre':>12}{'pool85_at':>11}{'inv85':>7}{'clearance_lo':>14}{'clearance_hi':>14}{'cleared?':>10}")
    cl=[]
    for rd in ROUNDS:
        pre=pl[(pl.AsAt==PRIOR[rd])&(pl.Score==85)]["only"].sum()
        at =pl[(pl.AsAt==SAME[rd])&(pl.Score==85)]["only"].sum()
        i85=iv[(iv.StatusMonth==rd)&(iv.Score==85)].n.sum()
        den_hi=max(pre,at+i85); den_lo=max(pre,at,i85)
        lo=i85/den_hi if den_hi else np.nan; hi=i85/den_lo if den_lo else np.nan
        cut=iv[(iv.StatusMonth==rd)&(iv.n>0)].Score.min()
        done = (not np.isnan(cut)) and cut<=85
        cl.append(dict(round=rd,pool_pre=int(pre),pool_at=int(at),inv85=int(i85),
                       clear_lo=None if np.isnan(lo) else round(lo,3),
                       clear_hi=None if np.isnan(hi) else round(hi,3),cleared=bool(done)))
        assert lo<=1.0001, f"clearance_lo>1 {name} {rd}"
        print(f"  {rd:<10}{pre:>12,.0f}{at:>11,.0f}{i85:>7,.0f}{100*lo:>13.0f}%{100*hi:>13.0f}%{str(done):>10}")
    clear[name]=cl
out["clearance"]=clear

print("\n"+"="*100)
print("MODEL 3 - WHERE THE USER SITS  (Physicist, 85 pts, EOI dated 10-Sep-2026)")
print("="*100)
pq=num(pd.read_csv("phys_queue.csv")); pq["n"]=pq.n.fillna(0)
q85=pq[pq.Score==85].sort_values("SubMonth")
print("  189 pool of physicists at exactly 85 pts (snapshot 08/2026), by submission month:")
for _,r in q85.iterrows():
    if r.n>0: print(f"     {r.SubMonth}: {int(r.n)}")
print(f"     TOTAL ahead of a 10-Sep-2026 EOI (all submitted earlier): {q85.n.sum():.0f}")
pl=st(poolo,("2349",)); latest=pl[pl.AsAt=="08/2026"]
print(f"\n  Unit group 2349 pool at 08/2026 (189-only):  =85pts -> {latest[latest.Score==85]['only'].sum():.0f}"
      f"   >85pts -> {latest[latest.Score>85]['only'].sum():.0f}")
phl=st(poolo,("234914",)); phl=phl[phl.AsAt=="08/2026"]
print(f"  Physicist pool at 08/2026 (189-only):        =85pts -> {phl[phl.Score==85]['only'].sum():.0f}"
      f"   >85pts -> {phl[phl.Score>85]['only'].sum():.0f}")
json.dump(out,open("model_hazards.json","w"),indent=1)
print("\n  -> model_hazards.json written  (all assertions passed)")
