import json
from paths import o
recs=json.load(open(o('recs.json')))
b=json.load(open(o('benchmarks.json')))
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
b['scatter']=[[round(r['tt_f']),round(r['tt_v']),round(r['cost']/r['tt_v']*1000,2),r['name'],r['brand'],round(r['cost'])] for r in tt]
open(o('blob.js'),'w').write("const HEBE="+json.dumps(b,separators=(',',':'))+";")
print("points:",len(b['scatter']),"| blob bytes:",len(open(o('blob.js')).read()))
print("tiers TT:",json.dumps(b['tiktok']['tiers']))
print("tiers FB:",json.dumps(b['facebook']['tiers']))
