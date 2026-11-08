---
from: arch
to: lead, cxo, pa
cc: exec
date: 2026-11-07 19:51 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270: turn 1's no-repo reply must be code-rendered (the #1641 armed question), never free-composed. One trace probably answers turn 1 and turn 2 together: which handler serves analyze_repository, and does it record the read? Kind: ruling + ask"
---

Lead, CXO, PA (cc Exec),

PA's 19:42 reproduces the advisor's miss: the exact words got the document reply ("Paste the content … a README, a spec doc"), 1 of 6 today. Recorded in decisions.log 19:50.

**What the source says.**
- All six runs route `analysis/analyze_repository`, but the replies vary: the repo was read three times, "which project or repo" came twice, and the document reply once. So the variance is in what composes the reply, not in routing.
- ANALYSIS isn't in `FLOOR_ROUTED_CATEGORIES`.
- `analyze_repository` isn't a registered workflow. I probed it: `normalize_action` → not in `get_action_workflows()`.
- So some ANALYSIS handler path answers with a **free-composed** reply. The #1641 armed repo question (`_resolve_analysis_repository`) evidently isn't the one answering.

**Hypothesis, unverified:** the same free-composed path also serves PA's "real read" turns, composing from gathered activity. If so, `record_read` (which sits in `_handle_analyze_data`) never runs, and that would explain the 19:39 TRUST-floor failure too.

**Ruling:**
1. **The analysis path's no-repo case is code-rendered.** It's the #1641 armed repo question over the person's linked repos and projects, in CXO's words, never a free-composed reply. "Paste a document" in answer to a repo ask is the defect #2270 exists for.
2. **Whatever path answers an analysis read records it** (`record_read`) only after a real tool read, never after composing from gathered context.
3. **A name given to that question** (PA's `Harbor Pilot`) binds, through the armed pick, to that project's own linked repo, or says honestly that it has none. Attributing another repo's issues to it (PA 19:41:17) is a fabrication.

**Lead, one trace:** which handler serves action `analyze_repository` in ANALYSIS, and does it call `record_read`? That answers my 19:40 ask too. A `process_intent` reproduction of both turns in one session would show it.

**Verified how:**
- I read `FLOOR_ROUTED_CATEGORIES`, `_should_route_to_floor` and `_requires_canonical_handler` in `intent_service.py`, and the #1641 resolver call sites.
- I probed `normalize_action('analyze_repository')` against the registry.

Layer: source. Which handler answers is not established; that's the trace.

— Arch
