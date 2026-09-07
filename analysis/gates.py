import json, statistics as st
S='/tmp/claude-0/-home-user-HeBE-KOL/e7909b51-e34c-500b-a163-0fd30d39b367/scratchpad/'
recs=json.load(open(S+'recs.json'))
tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
for r in tt:
    r['cpm']=r['cost']/r['tt_v']*1000; r['vfr']=r['tt_v']/r['tt_f']
    e=(r['tt_l'] or 0)+(r['tt_c'] or 0)
    r['ver']=e/r['tt_v']; r['ser']=(r['tt_s'] or 0)/r['tt_v']
TIERS=[("micro",0,100e3),("mid",100e3,500e3),("macro",500e3,1e6),("mega",1e6,9e9)]
print("HeBE-calibrated gate thresholds (TikTok) — GREEN = better than book p25 for that tier\n")
print("%-7s %3s | %-22s | %-20s | %-18s | %s"%("tier","n","view rate (VR)","eCPM","engagement (VER)","min views"))
out={}
for nm,lo,hi in TIERS:
    g=[r for r in tt if lo<=r['tt_f']<hi]
    if not g: continue
    q=lambda a,p: sorted(a)[int(p*(len(a)-1))]
    vr=[r['vfr'] for r in g]; cp=[r['cpm'] for r in g]
    ver=[r['ver'] for r in g]; mv=[r['tt_v'] for r in g]
    out[nm]={"n":len(g),
      "vr_green":round(q(vr,.50),4),"vr_amber":round(q(vr,.25),4),
      "cpm_green":round(q(cp,.25),2),"cpm_amber":round(q(cp,.50),2),
      "ver_green":round(q(ver,.50),4),"ver_amber":round(q(ver,.25),4),
      "minv_green":round(q(mv,.25))}
    print("%-7s %3d | GREEN ≥%5.1f%%  amber ≥%4.1f%% | GREEN ≤$%5.2f amber ≤$%5.2f | GREEN ≥%4.1f%% amber ≥%4.1f%% | ≥%s"%(
      nm,len(g),out[nm]["vr_green"]*100,out[nm]["vr_amber"]*100,
      out[nm]["cpm_green"],out[nm]["cpm_amber"],
      out[nm]["ver_green"]*100,out[nm]["ver_amber"]*100,f"{out[nm]['minv_green']:,}"))
ser=[r['ser'] for r in tt]
q=lambda a,p: sorted(a)[int(p*(len(a)-1))]
out['share']={"green":round(q(ser,.50),5),"amber":round(q(ser,.25),5)}
print("\nShare rate (all tiers): GREEN ≥%.2f%%  amber ≥%.2f%%"%(out['share']['green']*100,out['share']['amber']*100))
print("\nJin report used: micro VR≥5.5%%, mid VR≥3.5%%, macro VR≥2%%, eCPM ≤$4/$6/$8, VER≥2.5%%, SER≥0.4%%")
print("Those VR bars sit far BELOW HeBE's real medians — they would pass almost anything.")
json.dump(out,open(S+'gates.json','w'),indent=1)
