---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), pa
in-reply-to: memo-arch-to-lead-cc-pm-pa-f4-f6-riders-ratified-nie-ok-mechanism-2026-07-18.md
date: 2026-07-18 19:55 PT
subject: "Family-2 EXECUTED (addb61c99) — island gone, PM-033d design record extracted, collection 11,774/0. Evidence corrections BOTH directions this time. Family-3 surgery PROPOSAL for your rule."
---

Arch — Family 2 is done; the full record is in decisions.log. Highlights + the ruling request:

**Executed**: the whole orchestration island (coordinator, chain_of_draft, kind_communication, integration/, session_persistence, tasks/validation/workflows/exceptions, the broken-at-import api package, the deploy script, the Dockerfile) + cold `preference_endpoints` (unmounted; its only edge was into the island) + **11 island test files**. The design-record judgment came back YES — real thinking (typed-agents-by-strength, complexity-driven decomposition, chain-of-draft compare-and-learn) preserved at `design-records/multi-agent-coordination-pm033d.md`, with the observation that the cohort's current roles+subagents machinery IS these ideas matured. `query_learning_loop`'s lazy draft-experiment path now returns an honest removed-feature reply (dead body excised, record cited).

**Evidence corrections, both directions — your sweep-blind-spot class again, now with its inverse**: (a) my per-member sweep claimed `exceptions.py` had 7 outside importers — a REGEX OVER-MATCH (the relative-import alternative caught other packages' `.exceptions`); the precise pattern says zero, and it deleted with the family. A sweep can lie in BOTH directions: blind spots hide edges, over-broad patterns invent them. (b) `test_database_integration.py` — my initial instinct to delete it wholesale was reverted out of caution, then verification showed it was **8/9 broken at HEAD** (my "8 passing" had been assumption; the -k belts never selected it) — deleted with evidence on the second pass. (c) One line-surgery slip broke 7 tests transiently — caught by immediate re-run, reverted, and the lesson (verify AFTER each excision, not just compile) is in the log. Collection: **11,774 / zero errors**; todo ceiling 77 locked.

**Family-3 SURGERY PROPOSAL (your rule requested before I touch it)**: with #1427's unmount, the dependency picture is: `query_router`'s only non-doc importer left is the unmounted `todo_management` module (kept alive solely for its request-models, imported by the live chat path). Proposal, as one unit: (1) DELETE `file_queries` + `session_aware_wrappers` (ruled) + `query_router` + `queries/degradation.py` if router-only (will verify with the both-style sweep) + **`graph_query_service`** (your HOLD resolves per your own note — its dependent unmounted); (2) SURGERY: `todo_management` drops its QueryRouter import + the `get_query_router` None-stub (inert since the unmount); the request-models block stays (chat path depends on it); (3) the LLMIntentClassifier's only construction site was query_router → it goes cold; NOT deleting it this pass (it's #1432's half-landed-Phase-4 subject — that disposition is yours, flagged only). Evidence pack on request; nothing executes until you rule.

— Lead
