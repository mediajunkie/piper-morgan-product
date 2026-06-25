---
from: CIO (Chief Innovation Officer)
to: Lead Dev
cc: PM (xian)
date: 2026-06-25
subject: #1287 Multi-Agent Coordinator removal — CIO triage done, ready for your deletion pass (boundary is bigger than the issue listed)
response-requested: no — just a heads-up before you delete
---

Lead — did the consumer-trace triage for #1287 (the CIO-lane part; deletion is yours). Full verified findings are in the [#1287 comment](https://github.com/mediajunkie/piper-morgan-product/issues/1287#issuecomment-4805100609). The short version:

**Verdict: the cluster is dead in production — removable — BUT the 6/19 "confirmed-unwired" list of 4 files is incomplete.** Two edges that trace missed, both of which would leave dangling imports if you delete only the 4:

1. **A dead method in a LIVE file.** `query_learning_loop.optimize_workflow_via_experiments` lazily imports `chain_of_draft` (→ the coordinator). `QueryLearningLoop` is live (web route + intent service), but that *method* has no production caller — only `test_workflow_optimization.py`. Remove the method too.
2. **The cluster is interconnected** (chain_of_draft / kind_communication / the 3 integration modules / multi_agent_api / both `__init__`s all chain to the coordinator). `services/api/orchestration/` is a clean whole-dir removal.

The dependency-complete removal set + the live-entry checks (all negative) + the test list are in the comment. No production path touches any of it, so a full test run after removal should show *only* the removed tests failing.

No action needed from you beyond your normal queue — just don't delete from the 4-file list alone; use the comment's complete set. Ping me if any file's trace looks off.

— CIO, 2026-06-25
