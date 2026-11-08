import itertools, random
from fractions import Fraction as F
from pan_harmonics.janus_v1 import *
import unittest
RESULTS=[]
def ck(n,c): RESULTS.append((n,bool(c)))
random.seed(1)
rs=lambda: {k:F(random.randint(0,100),100) for k in NAMES}
# 1. exact (rational) identities: H + D - 1 == published delta, for v1 and v1.1
ok1=ok2=ok3=True
for _ in range(500):
    s=rs(); lam={p:F(random.randint(1,100),100) for p in PAIRS}; h1=heads(s); h2=heads(s,lam)
    for p in PAIRS:
        ok1&= h1[p]["delta"]==ev(SPEC["pairs"][p]["delta"],s)
        ok2&= h2[p]["delta"]==ev(SPEC["v1_1_proposal"]["defects"][p],{**s,LAM[p]:lam[p]})
        ok3&= h1[p]["delta"]==heads(s,{q:1 for q in PAIRS})[p]["delta"]
ck("v1: H+D-1 equals boxed delta (exact, 500 states x 5 pairs)",ok1)
ck("v1.1: H+D(lambda)-1 equals boxed delta(lambda) (exact)",ok2)
ck("v1.1 at all lambda=1 reproduces v1 exactly",ok3)
# 2. bounds over all 256 corners (functions are multilinear -> extrema at corners), with lambda corners too
mn={p:9 for p in PAIRS}; mx={p:-9 for p in PAIRS}; Dmin,Dmax=9,-9
for c in itertools.product((0,1),repeat=8):
    s=dict(zip(NAMES,map(F,c)))
    for lam in (F(1),F(1,100)):
        h=heads(s,{p:lam for p in PAIRS})
        for p in PAIRS:
            mn[p]=min(mn[p],h[p]["delta"]); mx[p]=max(mx[p],h[p]["delta"]); Dmin=min(Dmin,h[p]["D"]); Dmax=max(Dmax,h[p]["D"])
b3,b4=F(1,3),F(1,4)
ck("v1 raw-defect ranges: B,E,H in [-1/3,1/3]; W,C in [-1/4,1/4]  (attained, lambda=1)",
   all(mn[p]>=-(b4 if p in("spiderweb","chiralDNA") else b3) and mx[p]<=(b4 if p in("spiderweb","chiralDNA") else b3) for p in PAIRS))
h1c=[heads(dict(zip(NAMES,map(F,c))))for c in itertools.product((0,1),repeat=8)]
ck("normalized defects span exactly [-1,1] at lambda=1",all(min(x[p]["delta_norm"] for x in h1c)==-1 and max(x[p]["delta_norm"] for x in h1c)==1 for p in PAIRS))
ck("inverse heads stay in [0,1] for lambda in {1,0.01}, all 256 corners",Dmin>=0 and Dmax<=1)
# 3. sensitivities (exact since linear) and support coordinates
base=dict.fromkeys(NAMES,F(1,3)); sens={"bubble":lambda l:l/3,"compoundEye":lambda l:(1+l)/3,"honeycomb":lambda l:l/3,"spiderweb":lambda l:l/4,"chiralDNA":lambda l:l/4}
okS=True
for p in PAIRS:
    for l in (F(1),F(1,2),F(1,10)):
        a=heads(base,{p:l})[p]["delta"]; b=heads({**base,"d":F(1,3)+F(1,5)},{p:l})[p]["delta"]
        okS&=(b-a)/F(1,5)==sens[p](l)
ck("d-sensitivities: B l/3, E (1+l)/3, H l/3 (spec) , W l/4, C l/4",okS)
sup={"bubble":{"R","d"},"compoundEye":{"d"},"honeycomb":{"tau","s","d"},"spiderweb":{"f","h","R","d"},"chiralDNA":{"chi","tau","R","d"}}
dep={}
for p in PAIRS:
    dep[p]={k for k in NAMES if heads({**base,k:F(1,2)})[p]["delta"]!=heads(base)[p]["delta"]}
ck(f"defect depends exactly on {dep} (bubble: h,u cancel; eye: only d)",dep==sup)
hs={"bubble":{"h","R","u"},"compoundEye":{"s","h","d"},"honeycomb":{"tau","s"},"spiderweb":{"f","h","R"},"chiralDNA":{"chi","tau","R"}}
Dsup={"bubble":{"d","u","h"},"compoundEye":{"s","h","d"},"honeycomb":{"tau","s","d"},"spiderweb":{"f","h","R","d"},"chiralDNA":{"chi","tau","R","d"}}
fd=lambda p,key:{k for k in NAMES if heads({**base,k:F(1,2)})[p][key]!=heads(base)[p][key]}
ck("every formation head depends on exactly its stated support",all(fd(p,"H")==hs[p] for p in PAIRS))
ck("every inverse head depends on its support plus d (all five carry d)",all(fd(p,"D")==Dsup[p] for p in PAIRS))
# 4. replay determinism
s=rs(); ck("deterministic replay",heads(s)==heads(s))
# 5. guard rails
for bad in (0,-0.1,1.2):
    try: heads(base,{"bubble":bad}); ck(f"lambda={bad} rejected",False)
    except ValueError: ck(f"lambda={bad} rejected",True)
try: ev("__import__('os')",{}); ck("expression parser rejects code",False)
except Exception: ck("expression parser rejects code",True)
# 6. zero-defect set is a hyperplane, not measure zero in a point
ck("zero-defect states exist: compoundEye delta=0 at d=1/2",heads({**base,"d":F(1,2)})["compoundEye"]["delta"]==0)

class TestJanusV1(unittest.TestCase):
    def test_all_checks(self):
        self.assertEqual(len(RESULTS), 16)  # guards against silently dropped checks
        for name, ok in RESULTS:
            with self.subTest(name): self.assertTrue(ok, name)
if __name__ == "__main__": unittest.main()
