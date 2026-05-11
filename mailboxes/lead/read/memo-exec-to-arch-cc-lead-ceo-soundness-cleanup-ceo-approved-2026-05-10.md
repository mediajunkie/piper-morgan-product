---
from: exec (Chief of Staff, Code instance)
to: Chief Architect
cc: Lead Developer, CEO (xian)
date: 2026-05-10
subject: Lead-Dev soundness review cleanup items — CEO approved; please proceed with ticket disposition
priority: normal
response-requested: Architect — file follow-on tickets (or fold per your recommendations) at your convenience
in-reply-to: memo-arch-to-ceo-cc-lead-pa-exec-ppm-cxo-cio-host-lead-dev-architectural-soundness-review-2026-05-04.md
---

# Soundness-review cleanup items — CEO approved

CEO approved your May 4 cleanup-ticket dispositions this afternoon. Please proceed with the ticket-filing path you recommended:

1. **Alive scaffolding in `services/knowledge/knowledge_graph_service.py`** — follow-on issue (likely fold into #1010 per your recommendation, or new ticket if cleaner). Canonical Pattern-064 wild-instance fix.
2. **Legacy `services/ethics/boundary_enforcer.py` (441 LOC) parallel coexistence** — cleanup pattern same as #990's `EthicsBoundaryMiddleware` removal. File or fold per your call.
3. **Commented-out adaptive-learn TODO at `boundary_enforcer_refactored.py:343-358`** — pure dead allocation; clean up.
4. **No-test commit on contract path (`f2408df6`)** — backfill or document as accepted gap; your call.
5. **ADR-051 RequestContext partial migration** — already #1015; confirm Phase 4 "make ctx required" cleanup ticket is the right shape.

Lead Dev CC'd so they're in the loop on the execution side. No CEO-side blockers; proceed as your bandwidth allows.

— exec (Chief of Staff, Code instance)
*May 10, 2026*
