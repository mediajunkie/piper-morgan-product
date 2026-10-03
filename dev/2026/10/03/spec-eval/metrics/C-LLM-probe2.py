"""C-LLM probe 2: realistic multi-step / ambiguous / out-of-scope PM tasks."""
import importlib.util,sys,json
spec=importlib.util.spec_from_file_location("L","C-LLM-lib.py");L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
c=L.client(); L.login(c,"llmgood"); H={"X-User-Api-Key":L.KEY}
msgs=["add three todos for the launch: write release notes, update the docs, announce on Slack",
"what's on my plate this week",
"summarize my project status",
"draft a standup",
"can you take care of the thing from yesterday",
"book me a flight to Denver next Tuesday",
"mark the docs todo done and the release notes one too",
"create a project called Launch Q4 and put the Slack announcement todo in it"]
log=[]
for m in msgs:
    r=L.ask(c,m,log,hdr=H,tag="p2")
    b=r["body"];i=b.get("intent") or {}
    print(r["secs"],r["status"],i.get("category"),i.get("action"),i.get("confidence"),"clar=",b.get("requires_clarification"),"|",m[:50],"=>",(b.get("message") or "")[:300].replace("\n"," "))
json.dump(log,open("C-LLM-probe2.json","w"),indent=1)
