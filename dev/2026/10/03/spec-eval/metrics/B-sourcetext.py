import re,pathlib,collections,random
R=pathlib.Path("tests")
files=[f for f in R.rglob("test_*.py") if "archive" not in f.parts]
src=re.compile(r"read_text\(|inspect\.getsource|ast\.parse|\.rglob\(|ratchet|ceiling|MAX_[A-Z_]+\s*=|Path\(__file__\)",re.I)
beh=re.compile(r"TestClient|AsyncClient|await |process_intent|client\.(get|post)|mock|Mock|patch\(")
cls=collections.Counter();tests=collections.Counter();lst=collections.defaultdict(list)
for f in files:
    t=f.read_text(errors="ignore");n=len(re.findall(r"^\s*(?:async )?def test_",t,re.M))
    s=len(src.findall(t));b=len(beh.findall(t))
    name=f.name.lower()
    ratchet=bool(re.search(r"ratchet|enforcement|guard|lint|ceiling|census|honesty|boundary",name))
    k="static/source-scan" if (ratchet or (s>=3 and b<=s)) else "behavioral/other"
    cls[k]+=1;tests[k]+=n;lst[k].append(str(f))
print(len(files),dict(cls),dict(tests))
print("ratchet-named files:",sum(1 for f in files if re.search(r"ratchet|enforcement|_guard|lint|ceiling",f.name.lower())))
open("B-sourcetext.list","w").write("\n".join(lst["static/source-scan"]))
random.seed(7)
for x in random.sample(lst["static/source-scan"],12):print(" ",x)
