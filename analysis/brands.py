import json, statistics as st
from paths import o
recs=json.load(open(o('recs.json')))
def eng(r,p): 
    return sum(x or 0 for x in [r[p+'_l'],r[p+'_c'],r[p+'_s']])
rows=[]
for r in recs:
    tv=r['tt_v'] or 0; fv=r['fb_v'] or 0
    tot=tv+fv
    e=eng(r,'tt')+eng(r,'fb')
    rows.append({
      "n":r['name'],"b":r['brand'],"m":r['month'],"y":r['year'],"p":r['product'],
      "c":r['cost'],"tf":r['tt_f'],"tv":r['tt_v'],"ff":r['fb_f'],"fv":r['fb_v'],
      "tot":tot or None,"eng":e or None,
      "cpm":round(r['cost']/tot*1000,2) if r['cost'] and tot else None,
      "vfr":round(r['tt_v']/r['tt_f'],3) if r['tt_v'] and r['tt_f'] else None,
      "fvfr":round(r['fb_v']/r['fb_f'],3) if r['fb_v'] and r['fb_f'] else None,
      "erv":round(e/tot,4) if e and tot else None,
    })
print("rows",len(rows))
brands={}
for r in rows: brands.setdefault(r['b'],[]).append(r)
bout=[]
for b,rs in brands.items():
    sp=sum(x['c'] or 0 for x in rs); vw=sum(x['tot'] or 0 for x in rs)
    cpms=[x['cpm'] for x in rs if x['cpm']]
    withv=[x for x in rs if x['tot'] and x['cpm'] is not None]
    best=min(withv,key=lambda x:x['cpm']) if withv else None
    worst=max(withv,key=lambda x:x['cpm']) if withv else None
    months=sorted(set((x['y'],x['m']) for x in rs))
    bout.append({"brand":b,"n":len(rs),"spend":round(sp),"views":round(vw),
      "cpm":round(sp/vw*1000,2) if vw else None,
      "med_cpm":round(st.median(cpms),2) if cpms else None,
      "avg_fee":round(sp/len([x for x in rs if x['c']])) if [x for x in rs if x['c']] else None,
      "eng":round(sum(x['eng'] or 0 for x in rs)),
      "blowups":len([c for c in cpms if c>20]),"scored":len(cpms),
      "best":{"n":best['n'],"cpm":best['cpm'],"v":best['tot'],"c":best['c']} if best else None,
      "worst":{"n":worst['n'],"cpm":worst['cpm'],"v":worst['tot'],"c":worst['c']} if worst else None,
      "period":"%d/%d–%d/%d"%(months[0][1],months[0][0],months[-1][1],months[-1][0]) if months else ""})
bout.sort(key=lambda x:-x['spend'])
for b in bout:
    print("%-13s n=%3d spend=$%6d views=%10d aggCPM=$%6.2f medCPM=$%7.2f blowups=%d/%d"%(
      b['brand'],b['n'],b['spend'],b['views'],b['cpm'] or 0,b['med_cpm'] or 0,b['blowups'],b['scored']))
json.dump({"rows":rows,"brands":bout},open(o('brands.json'),'w'))
