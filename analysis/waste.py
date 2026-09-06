import json, statistics as st
recs=json.load(open('recs.json'))
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
for r in tt:
    r['cpm']=r['cost']/r['tt_v']*1000; r['vfr']=r['tt_v']/r['tt_f']
    eng=(r['tt_l'] or 0)+(r['tt_c'] or 0)+(r['tt_s'] or 0)
    r['eng']=eng; r['erv']=eng/r['tt_v']; r['cpe']=r['cost']/eng if eng else None
    r['sr']=(r['tt_s'] or 0)/r['tt_v']; r['cr']=(r['tt_c'] or 0)/r['tt_v']

s=sorted(tt,key=lambda r:r['cpm'])
med=st.median([r['cpm'] for r in s])
print("TikTok CPM percentiles ($ per 1000 views):")
v=[r['cpm'] for r in s]
for q in [0.10,0.25,0.50,0.75,0.90]:
    print("  p%02d  $%8.2f"%(q*100,v[int(q*(len(v)-1))]))
print("  mean $%.2f"%(sum(v)/len(v)))

# waste: spend on worse-than-median CPM, vs views if spent at median CPM
bad=[r for r in s if r['cpm']>med]
bs=sum(r['cost'] for r in bad); bv=sum(r['tt_v'] for r in bad)
print("\nSpend on above-median-CPM (bad half): $%.0f of $%.0f (%.0f%%)"%(bs,sum(r['cost'] for r in s),bs/sum(r['cost'] for r in s)*100))
print("  views those bought: %.0f"%bv)
print("  views if bought at MEDIAN CPM ($%.2f): %.0f"%(med,bs/med*1000))
print("  -> lost views: %.0f  (%.1fx)"%(bs/med*1000-bv,(bs/med*1000)/bv))
top=[r for r in s if r['cpm']<=med]
print("\nGood half: $%.0f -> %.0f views (%.0f%% of spend, %.0f%% of views)"%(
    sum(r['cost'] for r in top),sum(r['tt_v'] for r in top),
    sum(r['cost'] for r in top)/sum(r['cost'] for r in s)*100,
    sum(r['tt_v'] for r in top)/sum(r['tt_v'] for r in s)*100))

print("\nEngagement-rate-by-VIEW (TikTok) percentiles:")
e=sorted(r['erv'] for r in tt)
for q in [0.10,0.25,0.50,0.75,0.90]: print("  p%02d  %.2f%%"%(q*100,e[int(q*(len(e)-1))]*100))
print("\nShare rate (shares/views) percentiles:")
sr=sorted(r['sr'] for r in tt)
for q in [0.10,0.25,0.50,0.75,0.90]: print("  p%02d  %.3f%%"%(q*100,sr[int(q*(len(sr)-1))]*100))
print("\nComment rate (comments/views) percentiles:")
cr=sorted(r['cr'] for r in tt)
for q in [0.10,0.25,0.50,0.75,0.90]: print("  p%02d  %.4f%%"%(q*100,cr[int(q*(len(cr)-1))]*100))
print("\nCPE (cost per engagement) percentiles:")
cpe=sorted(r['cpe'] for r in tt if r['cpe'])
for q in [0.10,0.25,0.50,0.75,0.90]: print("  p%02d  $%.4f"%(q*100,cpe[int(q*(len(cpe)-1))]))

# tier analysis
print("\n=== BY FOLLOWER TIER (TikTok) ===")
tiers=[("Nano <30K",0,30e3),("Micro 30-100K",30e3,100e3),("Mid 100-500K",100e3,500e3),("Macro 500K-1M",500e3,1e6),("Mega 1M+",1e6,9e9)]
for nm,lo,hi in tiers:
    g=[r for r in tt if lo<=r['tt_f']<hi]
    if not g: continue
    c=sum(r['cost'] for r in g); vv=sum(r['tt_v'] for r in g)
    print("  %-15s n=%2d  avg fee $%4.0f  medVFR %.3f  aggCPM $%6.2f  medCPM $%6.2f"%(
        nm,len(g),c/len(g),st.median([r['vfr'] for r in g]),c/vv*1000,st.median([r['cpm'] for r in g])))
