import openpyxl, json, math, statistics as st

def num(v):
    if v is None: return None
    if isinstance(v,(int,float)): return float(v)
    s=str(v).strip().replace(',','')
    if not s: return None
    m=1.0
    if s[-1] in 'kK': m,s=1e3,s[:-1]
    elif s[-1] in 'mM': m,s=1e6,s[:-1]
    try: return float(s)*m
    except: return None

wb=openpyxl.load_workbook("/root/.claude/uploads/e7909b51-e34c-500b-a163-0fd30d39b367/99bea245-HeBE_KH_KOL_Data_Template_update.xlsx",data_only=True)
ws=wb["KOL Data"]
rows=list(ws.iter_rows(values_only=True))
hdr=[str(h).strip() if h else '' for h in rows[0]]
recs=[]
for r in rows[1:]:
    if not r or not r[0]: continue
    d=dict(zip(hdr,r))
    rec={
      'name':str(d['name']).strip(),'brand':str(d['brand']).strip(),
      'month':d['month'],'year':d['year'],
      'product':(str(d['product']).strip() if d['product'] else ''),
      'cost':num(d['cost']),
      'tt_f':num(d['tt_follower']),'tt_v':num(d['tt_view']),'tt_l':num(d['tt_like']),
      'tt_c':num(d['tt_comment']),'tt_s':num(d['tt_share']),
      'fb_f':num(d['fb_follower']),'fb_v':num(d['fb_view']),'fb_l':num(d['fb_like']),
      'fb_c':num(d['fb_comment']),'fb_s':num(d['fb_share']),
    }
    recs.append(rec)

print(f"TOTAL ROWS: {len(recs)}")
# completeness
have_cost=[r for r in recs if r['cost']]
print("with cost:",len(have_cost))
tt_ok=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
print("TT usable (cost+views+followers):",len(tt_ok))
fb_ok=[r for r in recs if r['cost'] and r['fb_v'] and r['fb_f']]
print("FB usable:",len(fb_ok))

# total spend
print("TOTAL SPEND: $%.0f"%sum(r['cost'] for r in have_cost))
tv=sum((r['tt_v'] or 0)+(r['fb_v'] or 0) for r in recs)
print("TOTAL VIEWS: %.0f"%tv)
print("BLENDED CPM: $%.2f"%(sum(r['cost'] for r in have_cost)/tv*1000))
print()
by_brand={}
for r in recs:
    by_brand.setdefault(r['brand'],[]).append(r)
for b,rs in by_brand.items():
    c=sum(x['cost'] or 0 for x in rs); v=sum((x['tt_v'] or 0)+(x['fb_v'] or 0) for x in rs)
    print(f"{b:14s} n={len(rs):3d} spend=${c:6.0f} views={v:12.0f} CPM=${c/v*1000 if v else 0:7.2f}")
json.dump(recs,open('recs.json','w'))
