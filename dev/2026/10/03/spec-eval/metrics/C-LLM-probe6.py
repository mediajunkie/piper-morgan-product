"""C-LLM probe 6: re-run 4 probes with a proper UUID session_id (the browser UI sends one; probes 1-5 omitted it -> 'default_session' -> RequestContext creation failed, 49 warnings)."""
import importlib.util,sys,json,uuid
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
c=L.client(); L.login(c,"llmgood"); H={"X-User-Api-Key":L.KEY}
sid=str(uuid.uuid4()); log=[]
for m in ["add a todo: review launch checklist","what did we create this session","Hello! What's on my calendar today?","mark todo 1 done"]:
    t=__import__("time").time()
    r=c.post("/api/v1/intent",json={"message":m,"session_id":sid},headers=H); L.N[0]+=1
    b=r.json(); i=b.get("intent") or {}
    log.append({"tag":"p6","msg":m,"status":r.status_code,"secs":round(__import__("time").time()-t,2),"body":json.loads(L.mask(json.dumps(b)))})
    print(round(__import__("time").time()-t,1),i.get("category"),i.get("action"),"|",m,"=>",(b.get("message") or "")[:250].replace("\n"," "))
json.dump(log,open("C-LLM-probe6.json","w"),indent=1)
