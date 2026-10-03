"""C-api-exercise: login as evalc, CRUD the non-LLM features, sweep param-free GETs, send chat messages."""
import json, sys, time, httpx
B="http://127.0.0.1:8001"; OUT=sys.argv[1]
c=httpx.Client(base_url=B,timeout=60)
R={}
def rec(name,r):
    try: body=r.json()
    except Exception: body=r.text[:300]
    R[name]={"status":r.status_code,"body":(json.dumps(body)[:600])}
    print(f"{r.status_code} {name}: {json.dumps(body)[:160]}"); return body
rec("login",c.post("/api/v1/auth/login",data={"username":"evalc","password":"EvalC-pass-2026"}))
rec("me",c.get("/api/v1/auth/me"))
# todos
t=rec("todo.create",c.post("/api/v1/todos",json={"title":"Eval todo A","priority":"high"}))
tid=(t.get("id") or (t.get("todo") or {}).get("id")) if isinstance(t,dict) else None
rec("todo.list",c.get("/api/v1/todos"))
if tid:
    rec("todo.update",c.put(f"/api/v1/todos/{tid}",json={"title":"Eval todo A (edited)"}))
    rec("todo.complete",c.post(f"/api/v1/todos/{tid}/complete"))
    rec("todo.get",c.get(f"/api/v1/todos/{tid}"))
t2=rec("todo.create2",c.post("/api/v1/todos",json={"title":"Eval todo B delete-me"}))
tid2=(t2.get("id") or (t2.get("todo") or {}).get("id")) if isinstance(t2,dict) else None
if tid2: rec("todo.delete",c.delete(f"/api/v1/todos/{tid2}"))
# projects
p=rec("project.create",c.post("/api/v1/projects",json={"name":"Eval Project","description":"spec eval"}))
pid=(p.get("id") or (p.get("project") or {}).get("id")) if isinstance(p,dict) else None
rec("project.list",c.get("/api/v1/projects"))
if pid:
    rec("project.update",c.put(f"/api/v1/projects/{pid}",json={"name":"Eval Project 2","description":"x"}))
    rec("project.get",c.get(f"/api/v1/projects/{pid}"))
    rec("project.workitems",c.get(f"/api/v1/projects/{pid}/work-items"))
# lists
l=rec("list.create",c.post("/api/v1/lists",json={"name":"Eval List"}))
lid=(l.get("id") or (l.get("list") or {}).get("id")) if isinstance(l,dict) else None
if lid:
    i=rec("list.item.create",c.post(f"/api/v1/lists/{lid}/items",json={"text":"item one"}))
    rec("list.items",c.get(f"/api/v1/lists/{lid}/items"))
rec("workitem.create",c.post("/api/v1/work-items",json={"title":"Eval WI","project_id":pid}))
rec("workitem.list",c.get("/api/v1/work-items"))
rec("tz.set",c.put("/api/v1/preferences/timezone",json={"timezone":"America/Los_Angeles"}))
rec("tz.get",c.get("/api/v1/preferences/timezone"))
rec("feedback.create",c.post("/api/v1/feedback",json={"feedback_type":"general","message":"spec eval feedback","rating":4}))
rec("standup.generate",c.post("/api/v1/standup/generate",json={}))
rec("conv.create",c.post("/api/v1/conversations",json={"title":"eval chat"}))
# GET sweep
spec=json.load(open('/tmp/claude-0/-home-user/03717665-1eb6-52ef-ab7b-3677cba046df/scratchpad/openapi.json'))
sweep={}
for path,ops in spec["paths"].items():
    if "get" in ops and "{" not in path and path.startswith("/api") and "oauth" not in path:
        try: r=c.get(path); sweep[path]=r.status_code
        except Exception as e: sweep[path]=f"EXC {type(e).__name__}"
from collections import Counter
print("GET sweep",len(sweep),Counter(str(v) for v in sweep.values()))
json.dump({"results":R,"get_sweep":sweep,"ids":{"todo":tid,"project":pid,"list":lid}},open(OUT+"/C-api-exercise.json","w"),indent=1)
