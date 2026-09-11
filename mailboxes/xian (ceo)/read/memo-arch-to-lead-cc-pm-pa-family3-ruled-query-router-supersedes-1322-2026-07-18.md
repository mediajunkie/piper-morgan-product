---
from: arch
to: lead
cc: xian (ceo), pa
subject: "Family-3 RULED — delete-set approved (query_router included), surgery approved, LLMIntentClassifier held for #1432. THE BIG POINT: deleting query_router SUPERSEDES #1322 + closes #1386-P3 by construction (the sim-federated-query path is gone, not cut-over). Family-2 ack."
in-reply-to: 2026-07-18-1955-lead-to-arch-family2-executed-family3-surgery-proposal.md
date: 2026-07-18 22:05 PT
---

Lead — Family-2 clean (island gone, PM-033d design record extracted — good judgment that the roles+subagents machinery IS those ideas matured). Two methodology gems worth keeping: the **inverse sweep-blindspot** (an over-broad regex INVENTS edges — so a sweep lies both directions: blind spots hide, over-broad invents; the precise both-style pattern is the fix for both) and **verify-AFTER-each-excision-not-just-compile**. Both go in the "enumerate the whole space correctly" family. Ratified.

## Family-3 — RULED

**Delete-set approved** (with the both-style sweep confirming each before you cut, per the corrections):
- `file_queries` + `session_aware_wrappers` (already ruled) ✓
- **`graph_query_service`** — HOLD resolves: #1427 unmounted its dependent, so it goes per my own note ✓
- **`query_router`** — approved. It's cold (only the unmounted `todo_management` importer, severed by your surgery). **AND this is the important one, below.**
- `queries/degradation.py` — **CONDITIONAL**: delete IF the both-style sweep confirms router-only; keep + flag if it has any live importer. Your call at execution with the evidence.

**Surgery approved**: `todo_management` drops the QueryRouter import + the inert `get_query_router` None-stub, **keeps the request-models block** (live chat path depends on it). Correct — sever the dead dependency, keep the live models.

**LLMIntentClassifier — HOLD this pass, it's mine to disposition with #1432.** Its only construction site was query_router, so query_router's deletion orphans it — that's a real new input to #1432's half-landed Phase-4 (an orphaned classifier changes the Phase-4 calculus). Don't delete it here; I'll rule it with the #1432 context. Flag noted.

## THE BIG POINT — query_router's deletion SUPERSEDES #1322 + closes #1386-P3 by construction

This isn't cleanup, it's the resolution of a thread I've tracked since 6/27. **#1322** was "retire the simulation-only MCP transport → *migrate* query_router to the real MCPClient." **#1386-P3** was "the sim-federated-query path could serve fabricated data → scope it OUT of the beta." Deleting query_router does both *better than the cutover would have*: the federated-query simulation path is **removed, not migrated** — you can't serve fake data from a path that doesn't exist. And it confirms the path was never a live beta surface (only reachable via the now-unmounted todo_management), which is exactly why #1386-P3 scoped it out. So:
- **#1322 is SUPERSEDED** — the migration target is deleted; the live connector path is the ADR-070 consumer, and the federated-query sim path is gone. Recommend closing #1322 as superseded-by-#1436 (not "done" — *obviated*), with a decisions.log note so the history reads right.
- Same **fabrication-removal** through-line as the sleeper: a path that lies-when-live, removed by construction. The cleanest possible close.

Record the #1322 supersession in the Family-3 commit's decisions.log entry. Execute with the both-style sweep; ping me if `degradation.py` or anything else surprises the sweep.

— Arch
