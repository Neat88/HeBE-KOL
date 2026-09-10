import json, math, statistics as st
from paths import o
recs=json.load(open(o('recs.json')))
tt=[r for r in recs if r['tt_v'] and r['tt_c'] is not None and r['tt_v']>0]
# log-log fit: comments = a * views^b
X=[math.log10(r['tt_v']) for r in tt]; Y=[math.log10(max(r['tt_c'],0.5)) for r in tt]
n=len(X); mx=sum(X)/n; my=sum(Y)/n
b=sum((x-mx)*(y-my) for x,y in zip(X,Y))/sum((x-mx)**2 for x in X)
a=my-b*mx
res=[y-(a+b*x) for x,y in zip(X,Y)]
sd=st.pstdev(res)
print("TikTok comment expectation: log10(comments) = %.4f + %.4f*log10(views)   (n=%d, resid sd=%.3f)"%(a,b,n,sd))
print("  -> expected comments at 10K views: %.0f | 100K: %.0f | 1M: %.0f"%(
    10**(a+b*4),10**(a+b*5),10**(a+b*6)))
# same for likes (engagement authenticity)
Y2=[math.log10(max(r['tt_l'],0.5)) for r in tt if r['tt_l']]
X2=[math.log10(r['tt_v']) for r in tt if r['tt_l']]
n2=len(X2); mx2=sum(X2)/n2; my2=sum(Y2)/n2
b2=sum((x-mx2)*(y-my2) for x,y in zip(X2,Y2))/sum((x-mx2)**2 for x in X2)
a2=my2-b2*mx2
sd2=st.pstdev([y-(a2+b2*x) for x,y in zip(X2,Y2)])
print("TikTok like expectation:    log10(likes)    = %.4f + %.4f*log10(views)   (n=%d, resid sd=%.3f)"%(a2,b2,n2,sd2))

fb=[r for r in recs if r['fb_v'] and r['fb_c'] is not None and r['fb_v']>0]
X3=[math.log10(r['fb_v']) for r in fb]; Y3=[math.log10(max(r['fb_c'],0.5)) for r in fb]
n3=len(X3); mx3=sum(X3)/n3; my3=sum(Y3)/n3
b3=sum((x-mx3)*(y-my3) for x,y in zip(X3,Y3))/sum((x-mx3)**2 for x in X3)
a3=my3-b3*mx3
sd3=st.pstdev([y-(a3+b3*x) for x,y in zip(X3,Y3)])
print("FB comment expectation:     log10(comments) = %.4f + %.4f*log10(views)   (n=%d, resid sd=%.3f)"%(a3,b3,n3,sd3))

# FB VFR / tier for benchmarks
fbu=[r for r in recs if r['cost'] and r['fb_v'] and r['fb_f']]
print("\nFB tiers:")
for nm,lo,hi in [("<100K",0,100e3),("100-500K",100e3,500e3),("500K-1M",500e3,1e6),("1M+",1e6,9e9)]:
    g=[r for r in fbu if lo<=r['fb_f']<hi]
    if not g: continue
    print("  %-10s n=%2d medVFR %.3f  medCPM $%.2f  avg fee $%.0f"%(nm,len(g),
      st.median([r['fb_v']/r['fb_f'] for r in g]),st.median([r['cost']/r['fb_v']*1000 for r in g]),
      sum(r['cost'] for r in g)/len(g)))

# fee vs followers curve (what market charges) - for "market rate" reference
u=[r for r in recs if r['cost'] and r['tt_f']]
print("\nMARKET FEE by TT follower tier (what HeBE actually paid):")
for nm,lo,hi in [("<50K",0,50e3),("50-100K",50e3,100e3),("100-300K",100e3,300e3),("300K-700K",300e3,700e3),("700K-1.5M",700e3,1.5e6),("1.5M+",1.5e6,9e9)]:
    g=[r['cost'] for r in u if lo<=r['tt_f']<hi]
    if not g: continue
    print("  %-10s n=%2d  median $%4.0f  p25 $%4.0f  p75 $%4.0f"%(nm,len(g),st.median(g),
        sorted(g)[int(.25*(len(g)-1))],sorted(g)[int(.75*(len(g)-1))]))
