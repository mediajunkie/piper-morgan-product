import importlib.util,sys,json
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
user=sys.argv[1]; c=L.client(); L.login(c,user)
r=c.get("/api/v1/todos"); 
try:
    d=r.json(); items=d.get("todos",d) if isinstance(d,dict) else d
    for t in items: print({k:t.get(k) for k in ("title","text","description","status","completed","due_date","priority")})
except Exception: print(r.status_code,r.text[:300])
