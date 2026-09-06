import json, math, statistics as st
recs=json.load(open('recs.json'))

def pear(xs,ys):
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    num=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    dx=math.sqrt(sum((a-mx)**2 for a in xs)); dy=math.sqrt(sum((b-my)**2 for b in ys))
    return num/(dx*dy) if dx and dy else 0
def spear(xs,ys):
    def rank(v):
        s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
        for pos,i in enumerate(s): r[i]=pos+1
        return r
    return pear(rank(xs),rank(ys))

tt=[r for r in recs if r['cost'] and r['tt_v'] and r['tt_f']]
print("=== TIKTOK (n=%d) ==="%len(tt))
f=[r['tt_f'] for r in tt]; v=[r['tt_v'] for r in tt]; c=[r['cost'] for r in tt]
print("  followers vs views      Pearson %+.3f  Spearman %+.3f"%(pear(f,v),spear(f,v)))
print("  followers vs cost       Pearson %+.3f  Spearman %+.3f"%(pear(f,c),spear(f,c)))
print("  cost vs views           Pearson %+.3f  Spearman %+.3f"%(pear(c,v),spear(c,v)))
cpm=[r['cost']/r['tt_v']*1000 for r in tt]
print("  followers vs CPM        Spearman %+.3f  (>0 = bigger acct = WORSE value)"%spear(f,cpm))
print("  cost vs CPM             Spearman %+.3f"%spear(c,cpm))

fb=[r for r in recs if r['cost'] and r['fb_v'] and r['fb_f']]
print("\n=== FACEBOOK (n=%d) ==="%len(fb))
f2=[r['fb_f'] for r in fb]; v2=[r['fb_v'] for r in fb]; c2=[r['cost'] for r in fb]
print("  followers vs views      Pearson %+.3f  Spearman %+.3f"%(pear(f2,v2),spear(f2,v2)))
print("  followers vs cost       Pearson %+.3f  Spearman %+.3f"%(pear(f2,c2),spear(f2,c2)))
print("  cost vs views           Pearson %+.3f  Spearman %+.3f"%(pear(c2,v2),spear(c2,v2)))

# VFR = view/follower ratio
print("\n=== VIEW-TO-FOLLOWER RATIO (VFR) — TikTok ===")
vfr=sorted([(r['tt_v']/r['tt_f'],r) for r in tt])
qs=[0.10,0.25,0.50,0.75,0.90]
vals=[x[0] for x in vfr]
for q in qs:
    print("  p%02d  %.3f"%(q*100, vals[int(q*(len(vals)-1))]))
print("  VFR vs CPM Spearman %+.3f (should be strongly negative = VFR predicts value)"%spear(vals,[x[1]['cost']/x[1]['tt_v']*1000 for x in vfr]))
print("\n  WORST 8 VFR (paid for followers, got no views):")
for r0,r in vfr[:8]:
    print("   %-16s %-12s f=%9.0f v=%9.0f VFR=%.3f  $%4.0f  CPM=$%7.2f"%(r['name'],r['brand'],r['tt_f'],r['tt_v'],r0,r['cost'],r['cost']/r['tt_v']*1000))
print("\n  BEST 8 VFR:")
for r0,r in vfr[-8:][::-1]:
    print("   %-16s %-12s f=%9.0f v=%9.0f VFR=%.3f  $%4.0f  CPM=$%7.2f"%(r['name'],r['brand'],r['tt_f'],r['tt_v'],r0,r['cost'],r['cost']/r['tt_v']*1000))
