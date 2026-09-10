import json
from paths import o

b=json.load(open(o('benchmarks.json'))); br=json.load(open(o('brands.json')))
recs=json.load(open(o('recs.json')))
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
b['scatter']=[[round(r['tt_f']),round(r['tt_v']),round(r['cost']/r['tt_v']*1000,2),r['name'],r['brand'],round(r['cost'])] for r in tt]
b['rows']=br['rows']; b['brands']=br['brands']

# objective weight matrix (pillars: cost, reach, response, reliability, trust)
b['objectives']={
 "awareness":{"label":"Awareness","goal":"Cheapest possible reach",
   "primary":"CPM","w":{"cost":35,"reach":30,"response":5,"reliability":15,"trust":15}},
 "engagement":{"label":"Engagement","goal":"Conversation and saves",
   "primary":"ER-V / CPE","w":{"cost":20,"reach":20,"response":30,"reliability":10,"trust":20}},
 "conversion":{"label":"Conversion","goal":"Clicks and purchases",
   "primary":"Share rate + trust","w":{"cost":20,"reach":15,"response":25,"reliability":10,"trust":30}}}

json.dump(b,open(o('blob2.json'),'w'),separators=(',',':'))
open(o('blob2.js'),'w').write("const HEBE="+json.dumps(b,separators=(',',':'))+";")
print("rows",len(b['rows']),"brands",len(b['brands']),"scatter",len(b['scatter']))
print("blob bytes",len(open(o('blob2.js')).read()))
