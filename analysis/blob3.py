import json
S='/tmp/claude-0/-home-user-HeBE-KOL/e7909b51-e34c-500b-a163-0fd30d39b367/scratchpad/'
b=json.load(open(S+'blob2.json')); g=json.load(open(S+'gates.json'))
b['gates']=g
# gate catalogue: id, name, weight, what it means, what it catches, fraud flag
b['gatespec']=[
 ["G0","Data sufficiency",3,"Are there enough recent posts to judge this account?","Stale or thin accounts that cannot be read reliably",0],
 ["G1","Spike ratio",3,"Do views depend on a few viral hits? (mean ÷ median)","Quiet accounts inflated by one or two spikes",0],
 ["G2","Floor ratio",3,"Do weak posts still hold a floor? (p25 ÷ median)","Only the wins show; everyday posts barely seen",0],
 ["G3","Peak ratio",2,"Is the best post abnormally spiky? (max ÷ median)","One mega-hit distorting the average",0],
 ["G4","Top-3 share",2,"How concentrated are views in the best 3 posts?","Most reach coming from three lucky posts",0],
 ["G5","View rate",5,"How many watch versus follow (views ÷ followers)","Big follower count, little real reach",0],
 ["G6","Engagement rate",4,"How strongly viewers react (likes + comments ÷ views)","People watch but nobody responds",0],
 ["G7","View floor",2,"Do large accounts hold a minimum view level?","Many followers but bottomed-out views",0],
 ["G8","Share rate",2,"How shareable the content is (shares ÷ views)","No organic spread beyond the creator's feed",0],
 ["G9","Cost efficiency",4,"Is the ask fair for the reach (eCPM)","Price far above what the views are worth",0],
 ["G10","Follow-back ratio",2,"Follower count padded by mutual follows? (following ÷ followers)","Follow-for-follow padding, bought followers",1],
 ["G11","Upload consistency",3,"Are uploads regular and recent?","Long gaps or burst posting; unreliable delivery",0],
 ["G12","Comment-pod signal",2,"Do the same people comment across many posts?","Engagement pods faking response",1],
 ["G13","Category fit",3,"What share of recent posts are in your category? (CFR)","Off-category creator whose audience ignores the product",0]]
b['pricebands']=[["Great value",0,0.5],["Good deal",0.5,1.0],["Slightly overpriced",1.0,1.6],["Overpriced",1.6,99]]
open(S+'blob3.js','w').write("const HEBE="+json.dumps(b,separators=(',',':'))+";")
print("gates tiers:",list(g.keys()))
print("blob bytes:",len(open(S+'blob3.js').read()))
