"""C-preclassify: which of the chat probes would the deterministic pre-classifier route without an LLM?"""
import sys, json; sys.path.insert(0,'.')
from services.intent_service.pre_classifier import PreClassifier
msgs=["hello","what can you do?","add a todo: email the design team","show my todos","what time is it?","what should I focus on today?","remind me to call Sam tomorrow at 3pm","what's on my calendar today?","list open issues","thanks","what's my next todo","mark todo 1 done","set my timezone to America/New_York","what did we create this session","show my projects"]
out={}
for m in msgs:
    try:
        r=PreClassifier.pre_classify(m)
        out[m]=None if r is None else f"{getattr(r.category,'name',r.category)}:{r.action}"
    except Exception as e: out[m]=f"EXC {e}"
for k,v in out.items(): print(f"{str(v):45} <- {k}")
json.dump(out,open(sys.argv[1],'w'),indent=1)
