import re,pathlib,collections,subprocess,sys
R=pathlib.Path("tests")
files=[f for f in R.rglob("test_*.py") if "archive" not in f.parts]
pat={"skip_decorator":r"@pytest\.mark\.skip\(","skipif":r"@pytest\.mark\.skipif\(","xfail":r"@pytest\.mark\.xfail","pytest.skip()":r"pytest\.skip\(","importorskip":r"importorskip\(","module_skip":r"^pytestmark\s*=.*skip"}
cnt=collections.Counter();files_with=collections.Counter();reasons=collections.Counter()
for f in files:
    t=f.read_text(errors="ignore")
    for k,p in pat.items():
        n=len(re.findall(p,t,re.M))
        if n: cnt[k]+=n;files_with[k]+=1
    for m in re.finditer(r"(?:skip|xfail)(?:if)?\((?:[^)]*?)reason\s*=\s*[\"']([^\"']{0,90})",t,re.S):
        r=m.group(1).lower()
        key=("llm/key" if re.search(r"llm|api.?key|anthropic|openai",r) else "database/redis/service" if re.search(r"database|postgres|redis|chroma|server|docker",r) else "issue/#" if re.search(r"#\d{3,4}",r) else "deprecated/removed/dead" if re.search(r"deprecat|removed|obsolete|legacy|dead|no longer",r) else "needs-impl/todo" if re.search(r"todo|not implemented|pending|wip|future",r) else "other")
        reasons[key]+=1
print(len(files),"test files");print(dict(cnt));print(dict(files_with));print(dict(reasons))
