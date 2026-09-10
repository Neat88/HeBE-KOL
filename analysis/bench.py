import json, math, statistics as st
from paths import o
recs=json.load(open(o('recs.json')))
def pct(vals,q): 
    v=sorted(vals); return v[int(q*(len(v)-1))]
def dist(vals): return {("p%d"%int(q*100)):round(pct(vals,q),6) for q in (.1,.25,.5,.75,.9)}

out={"meta":{"campaigns":len(recs),"brands":sorted(set(r['brand'] for r in recs)),
     "total_spend_usd":round(sum(r['cost'] or 0 for r in recs)),
     "total_views":round(sum((r['tt_v'] or 0)+(r['fb_v'] or 0) for r in recs)),
     "market":"Cambodia (KH)","period":"Oct 2024 - Jun 2026"}}

for plat,fk,vk,lk,ck,sk in [("tiktok","tt_f","tt_v","tt_l","tt_c","tt_s"),("facebook","fb_f","fb_v","fb_l","fb_c","fb_s")]:
    g=[r for r in recs if r['cost'] and r[vk] and r[fk]]
    cpm=[r['cost']/r[vk]*1000 for r in g]; vfr=[r[vk]/r[fk] for r in g]
    ge=[r for r in g if r[lk] is not None]
    erv=[((r[lk] or 0)+(r[ck] or 0)+(r[sk] or 0))/r[vk] for r in ge]
    sr=[(r[sk] or 0)/r[vk] for r in ge]; cr=[(r[ck] or 0)/r[vk] for r in ge]
    cpe=[r['cost']/e for r,e in zip(ge,[((r[lk] or 0)+(r[ck] or 0)+(r[sk] or 0)) for r in ge]) if e]
    out[plat]={"n":len(g),"cpm":dist(cpm),"vfr":dist(vfr),"erv":dist(erv),
               "share_rate":dist(sr),"comment_rate":dist(cr),"cpe":dist(cpe),
               "agg_cpm":round(sum(r['cost'] for r in g)/sum(r[vk] for r in g)*1000,3)}
    # tiers
    tiers=[]
    for nm,lo,hi in [("Nano/Micro <100K",0,100e3),("Mid 100-500K",100e3,500e3),("Macro 500K-1M",500e3,1e6),("Mega 1M+",1e6,9e9)]:
        t=[r for r in g if lo<=r[fk]<hi]
        if not t: continue
        tc=[r['cost']/r[vk]*1000 for r in t]
        tiers.append({"label":nm,"min":lo,"max":hi,"n":len(t),
          "med_vfr":round(st.median([r[vk]/r[fk] for r in t]),4),
          "med_cpm":round(st.median(tc),2),"avg_fee":round(sum(r['cost'] for r in t)/len(t)),
          "blowup_rate":round(len([x for x in tc if x>20])/len(t),3)})
    out[plat]["tiers"]=tiers

out["auth_curve"]={
  "tiktok":{"comment":{"a":-1.6638,"b":0.6685,"sd":0.394},"like":{"a":-0.9878,"b":0.9682,"sd":0.366}},
  "facebook":{"comment":{"a":-2.2601,"b":0.7780,"sd":0.444}}}

out["market_fee_tiktok"]=[
 {"label":"<50K","min":0,"max":50e3,"p25":100,"median":275,"p75":300},
 {"label":"50-100K","min":50e3,"max":100e3,"p25":100,"median":200,"p75":300},
 {"label":"100-300K","min":100e3,"max":300e3,"p25":200,"median":250,"p75":400},
 {"label":"300-700K","min":300e3,"max":700e3,"p25":200,"median":250,"p75":550},
 {"label":"700K-1.5M","min":700e3,"max":1.5e6,"p25":200,"median":500,"p75":650},
 {"label":"1.5M+","min":1.5e6,"max":9e9,"p25":300,"median":400,"p75":600}]

out["evidence"]={
 "followers_explain_views_r2":0.124,
 "vfr_vs_cpm_spearman":-0.691,
 "followers_vs_cost_spearman":0.396,
 "cost_vs_views_spearman":0.228,
 "followers_vs_views_spearman":0.372,
 "good_half_spend_share":0.43,"good_half_view_share":0.91,
 "wasted_spend":19150,"views_lost":1885449,
 "vfr_bands":[{"band":"<0.05","n":19,"med_cpm":48.61,"avg_fee":453},
              {"band":"0.05-0.15","n":26,"med_cpm":9.28,"avg_fee":433},
              {"band":"0.15-0.40","n":21,"med_cpm":4.09,"avg_fee":346},
              {"band":"0.40+","n":16,"med_cpm":2.53,"avg_fee":400}],
 "fb_multiplier_median":1.09}

# top/bottom performers for the leaderboard
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
for r in tt: r['cpm']=r['cost']/r['tt_v']*1000; r['vfr']=r['tt_v']/r['tt_f']
s=sorted(tt,key=lambda r:r['cpm'])
key=lambda r:{"name":r['name'],"brand":r['brand'],"followers":r['tt_f'],"views":r['tt_v'],
              "cost":r['cost'],"cpm":round(r['cpm'],2),"vfr":round(r['vfr'],3)}
out["best"]=[key(r) for r in s[:10]]
out["worst"]=[key(r) for r in s[-10:][::-1]]
json.dump(out,open(o('benchmarks.json'),'w'),indent=1)
print(json.dumps(out["meta"],indent=1))
print("tiktok cpm",out["tiktok"]["cpm"]); print("tiktok vfr",out["tiktok"]["vfr"])
print("facebook cpm",out["facebook"]["cpm"]); print("facebook vfr",out["facebook"]["vfr"])
print("\nwrote benchmarks.json", len(open(o('benchmarks.json')).read()),"bytes")
