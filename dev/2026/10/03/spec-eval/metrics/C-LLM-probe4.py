"""C-LLM probe 4: failure behaviour with a deliberately invalid (random, well-formed) Anthropic key stored via the app's own /keys/store."""
import importlib.util,sys,json,secrets,string
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
c=L.client()
r=L.mkuser(c,"llmbad","/home/user/llm-tmp/t2"); print("create",r.status_code)
L.login(c,"llmbad")
alpha=string.ascii_letters+string.digits+"-_"
fake="sk-ant-api03-"+"".join(secrets.choice(alpha) for _ in range(95))
out={"store":None,"chat":[]}
r=c.post("/api/v1/keys/store",json={"provider":"anthropic","api_key":fake,"validate":True})
out["store"]={"status":r.status_code,"body":r.text[:600]}; print("store",r.status_code,r.text[:400])
r=c.get("/api/v1/keys/list") ; print("list",r.status_code,r.text[:300]); out["list"]=r.text[:500]
log=[]
for m in ["add a todo: test invalid key","what can you do?","what should I focus on today?"]:
    rr=L.ask(c,m,log,tag="p4"); b=rr["body"]; i=b.get("intent") or {}
    print(rr["secs"],rr["status"],i.get("category"),i.get("action"),b.get("error_type"),"|",m,"=>",(b.get("message") or "")[:300].replace("\n"," "))
out["chat"]=log
json.dump(out,open("C-LLM-probe4.json","w"),indent=1)
