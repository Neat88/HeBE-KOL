import json, statistics as st
recs=json.load(open('recs.json'))
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
for r in tt:
    r['cpm']=r['cost']/r['tt_v']*1000; r['vfr']=r['tt_v']/r['tt_f']

print("=== BLOWUP RISK BY TIER (share of deals with CPM > $20) ===")
tiers=[("Micro <100K",0,100e3),("Mid 100-500K",100e3,500e3),("Macro 500K-1M",500e3,1e6),("Mega 1M+",1e6,9e9)]
for nm,lo,hi in tiers:
    g=[r for r in tt if lo<=r['tt_f']<hi]
    if not g: continue
    bad=[r for r in g if r['cpm']>20]
    vf=[r['vfr'] for r in g]
    print("  %-14s n=%2d  blowups %2d (%3.0f%%)  VFR med %.3f  VFR p25 %.3f  spend-at-risk $%.0f"%(
        nm,len(g),len(bad),len(bad)/len(g)*100,st.median(vf),sorted(vf)[int(.25*(len(vf)-1))],sum(r['cost'] for r in bad)))

print("\n=== VFR AS A GATE: outcomes by VFR band ===")
bands=[("VFR < 0.05 (dead)",0,0.05),("0.05-0.15",0.05,0.15),("0.15-0.40",0.15,0.40),("0.40+ (viral engine)",0.40,99)]
for nm,lo,hi in bands:
    g=[r for r in tt if lo<=r['vfr']<hi]
    if not g: continue
    c=sum(r['cost'] for r in g); v=sum(r['tt_v'] for r in g)
    print("  %-22s n=%2d  aggCPM $%7.2f  medCPM $%7.2f  avg fee $%4.0f  spend $%5.0f"%(nm,len(g),c/v*1000,st.median([r['cpm'] for r in g]),c/len(g),c))

print("\n=== REPEAT KOLs (used 2+ times) — consistency ===")
by={}
for r in tt: by.setdefault(r['name'],[]).append(r)
rep={k:v for k,v in by.items() if len(v)>1}
for k,v in sorted(rep.items(),key=lambda x:-len(x[1])):
    cpms=[x['cpm'] for x in v]; vfrs=[x['vfr'] for x in v]
    print("  %-16s n=%d  CPM %s  VFR %s"%(k,len(v)," / ".join("$%.1f"%c for c in cpms)," / ".join("%.2f"%f for f in vfrs)))

print("\n=== FACEBOOK benchmark ===")
fb=[r for r in recs if r['cost'] and r['fb_v'] and r['fb_f']]
for r in fb:
    r['cpm']=r['cost']/r['fb_v']*1000; r['vfr']=r['fb_v']/r['fb_f']
    eng=(r['fb_l'] or 0)+(r['fb_c'] or 0)+(r['fb_s'] or 0); r['erv']=eng/r['fb_v']
v=sorted(r['cpm'] for r in fb)
print("  FB CPM  p10 $%.2f  p25 $%.2f  p50 $%.2f  p75 $%.2f  p90 $%.2f"%tuple(v[int(q*(len(v)-1))] for q in [.1,.25,.5,.75,.9]))
v=sorted(r['vfr'] for r in fb)
print("  FB VFR  p10 %.3f  p25 %.3f  p50 %.3f  p75 %.3f  p90 %.3f"%tuple(v[int(q*(len(v)-1))] for q in [.1,.25,.5,.75,.9]))
v=sorted(r['erv'] for r in fb)
print("  FB ERV  p10 %.2f%% p25 %.2f%% p50 %.2f%% p75 %.2f%% p90 %.2f%%"%tuple(v[int(q*(len(v)-1))]*100 for q in [.1,.25,.5,.75,.9]))
print("\n  Dual-platform posts: %d of %d — FB adds avg %.0f%% more views"%(
    len([r for r in recs if r['tt_v'] and r['fb_v']]),len(recs),
    st.median([r['fb_v']/r['tt_v'] for r in recs if r['tt_v'] and r['fb_v']])*100))
