import ast,pathlib,random,collections,json
R=pathlib.Path("tests")
files=[f for f in R.rglob("test_*.py") if "archive" not in f.parts]
def analyze(f):
    try: tree=ast.parse(f.read_text(errors="ignore"))
    except Exception: return None
    res=dict(tests=0,noassert=0,trivial=0,mockonly=0,patches=0,asserts=0)
    for n in ast.walk(tree):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith("test_"):
            res["tests"]+=1
            a=[x for x in ast.walk(n) if isinstance(x,ast.Assert)]
            raises=any(isinstance(x,ast.Call) and getattr(x.func,"attr",getattr(x.func,"id",""))in("raises","warns","fail") for x in ast.walk(n))
            calls=[getattr(x.func,"attr","") for x in ast.walk(n) if isinstance(x,ast.Call)]
            mock_asserts=[c for c in calls if c.startswith("assert_")]
            res["asserts"]+=len(a)
            if not a and not raises and not mock_asserts: res["noassert"]+=1
            if a and all(isinstance(x.test,ast.Constant) and x.test.value is True or (isinstance(x.test,ast.Compare) and isinstance(x.test.left,ast.Constant) and False) for x in a): res["trivial"]+=1
            if mock_asserts and not a and not raises: res["mockonly"]+=1
            res["patches"]+=sum(1 for c in calls if c in("patch","MagicMock","AsyncMock","Mock"))
    return res
tot=collections.Counter();per={}
for f in files:
    r=analyze(f)
    if r: per[str(f)]=r; tot.update(r)
print("ALL",len(files),dict(tot))
# stratified sample 40: by top dir weight
random.seed(11)
strata={"unit/services":[f for f in per if f.startswith("tests/unit/services")],"unit/web":[f for f in per if f.startswith("tests/unit/web")],"unit/other":[f for f in per if f.startswith("tests/unit") and not f.startswith(("tests/unit/services","tests/unit/web"))],"integration":[f for f in per if f.startswith("tests/integration")],"other":[f for f in per if not f.startswith(("tests/unit","tests/integration"))]}
alloc={"unit/services":14,"unit/web":4,"unit/other":8,"integration":7,"other":7}
sample=[]
for k,n in alloc.items(): sample+=random.sample(strata[k],min(n,len(strata[k])))
json.dump(sample,open("/home/user/piper-morgan-product/dev/2026/10/03/spec-eval/metrics/B-sample40.json","w"))
s=collections.Counter()
for f in sample: s.update(per[f])
print("SAMPLE",len(sample),dict(s))
for f in sample: print(f, per[f]["tests"], per[f]["asserts"], per[f]["patches"], per[f]["noassert"],per[f]["mockonly"])
