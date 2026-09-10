import json, math, statistics as st
from paths import o
recs=json.load(open(o('recs.json')))
def pear(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    nu=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    dx=math.sqrt(sum((a-mx)**2 for a in xs)); dy=math.sqrt(sum((b-my)**2 for b in ys))
    return nu/(dx*dy) if dx and dy else 0
def spear(xs,ys):
    def rk(v):
        s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
        for p,i in enumerate(s): r[i]=p+1
        return r
    return pear(rk(xs),rk(ys))

tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f'] and r['tt_l'] is not None]
for r in tt:
    r['cpm']=r['cost']/r['tt_v']*1000; r['vfr']=r['tt_v']/r['tt_f']
    eng=(r['tt_l'] or 0)+(r['tt_c'] or 0)+(r['tt_s'] or 0)
    r['erv']=eng/r['tt_v']; r['sr']=(r['tt_s'] or 0)/r['tt_v']; r['cr']=(r['tt_c'] or 0)/r['tt_v']
print("n =",len(tt))
print("\nPredictor -> CPM (Spearman; negative = higher value). |rho| sets the weight:")
cpm=[r['cpm'] for r in tt]
for nm,key in [("VFR (views/followers)",'vfr'),("ER-by-view",'erv'),("Share rate",'sr'),
               ("Comment rate",'cr'),("Followers",'tt_f')]:
    print("  %-24s %+.3f"%(nm,spear([r[key] for r in tt],cpm)))

print("\nPredictor -> raw VIEWS delivered (what you actually buy):")
vv=[r['tt_v'] for r in tt]
for nm,key in [("VFR",'vfr'),("ER-by-view",'erv'),("Share rate",'sr'),("Comment rate",'cr'),("Followers",'tt_f')]:
    print("  %-24s %+.3f"%(nm,spear([r[key] for r in tt],vv)))

# multivariate-lite: does ERV add anything ON TOP of VFR? split by VFR band
print("\nWithin high-VFR deals (VFR>=0.15), does engagement quality still separate CPM?")
hi=[r for r in tt if r['vfr']>=0.15]
print("  n=%d  ERV->CPM %+.3f   ShareRate->CPM %+.3f   CommentRate->CPM %+.3f"%(
    len(hi),spear([r['erv'] for r in hi],[r['cpm'] for r in hi]),
    spear([r['sr'] for r in hi],[r['cpm'] for r in hi]),
    spear([r['cr'] for r in hi],[r['cpm'] for r in hi])))
lo=[r for r in tt if r['vfr']<0.15]
print("  low-VFR n=%d  ERV->CPM %+.3f"%(len(lo),spear([r['erv'] for r in lo],[r['cpm'] for r in lo])))

# log-log regression: views ~ followers^a * vfr... trivially true. Instead:
# how well does followers alone predict views vs vfr*followers
print("\nR^2 (log10) predicting VIEWS:")
import math
lf=[math.log10(r['tt_f']) for r in tt]; lv=[math.log10(r['tt_v']) for r in tt]
print("  log(followers) -> log(views)  R^2 = %.3f"%(pear(lf,lv)**2))
