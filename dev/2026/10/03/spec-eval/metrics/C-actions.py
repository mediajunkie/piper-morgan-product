import sys; sys.path.insert(0,'.')
from services.intent_service.action_registry import ACTION_REGISTRY as R
from collections import Counter
print('registry pairs',len(R)); print(Counter(v.value for v in R.values()))
cats=Counter(k[0] for k in R); print(dict(cats))
import json; json.dump({f"{k[0]}:{k[1]}":v.value for k,v in R.items()},open(sys.argv[1],'w'),indent=1)
try:
    from services.intent_service.workflow_entries import get_action_workflows
    w=get_action_workflows(); print('action-triggered workflows',len(w)); print(sorted(w)[:80])
except Exception as e: print('wf err',e)
