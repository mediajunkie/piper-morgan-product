"""C-LLM probe 1: C's 15 everyday phrasings (superset of its 9 chat probes) with a real LLM, via X-User-Api-Key header."""
import importlib.util,sys,json
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
c=L.client(); L.login(c,"llmgood"); H={"X-User-Api-Key":L.KEY}
msgs=["hello","what can you do?","add a todo: email the design team","show my todos","what time is it?","what should I focus on today?","remind me to call Sam tomorrow at 3pm","what's on my calendar today?","list open issues","thanks","what's my next todo","mark todo 1 done","set my timezone to America/New_York","what did we create this session","show my projects"]
log=[]
for m in msgs:
    r=L.ask(c,m,log,hdr=H,tag="p1")
    b=r["body"];i=b.get("intent") or {}
    print(r["secs"],r["status"],i.get("category"),i.get("action"),i.get("confidence"),"|",m,"=>",(b.get("message") or "")[:140].replace("\n"," "))
json.dump(log,open("C-LLM-probe1.json","w"),indent=1)
