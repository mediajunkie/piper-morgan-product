---
from: Lead Developer
to: Architect
cc: CIO, PM (xian)
date: 2026-06-15
subject: #1241 audit findings (analytical phase complete) — ADR-071 grounding + your D1 global-by-design ruling needed
in-reply-to: memo-lead-to-arch-cc-pm-cio-1241-framing-confirmed-audit-starting-2026-06-15.md
priority: high — ADR-071 scoping
response-requested: (1) D1 ruling on the PM-domain cluster; (2) confirm the D-section grounding; then I draft ADR-071
---

# #1241 audit — the evidence to scope ADR-071

Ran both axes + the resolution sub-inventory across all content stores (`services/database/models.py` 37 tables + the ChromaDB doc store). Full detail: `dev/2026/06/15/1241-content-anchoring-audit.md`. Headlines:

## What I found (and one correction)
**Correction first**: my first write-axis pass over-claimed "~half the tables unanchored" — I'd grepped only `user_id` and missed `owner_id`. Corrected: **most content tables ARE owner-anchored.** The real finding is **inconsistency**, not raw count.

1. **The user_id/owner_id split is semantic, not naming** — `owner_id` = UUID FK→`users.id` (read-scope = join through users); `user_id` = the external auth-principal, often `Column(String)`, NOT a FK (read-scope = filter by principal string). `projects` carries **both**. Three coexisting styles (user_id-string / owner_id-FK / none), no canonical one → the recurrence. **This is D2 + the consolidating refactor.** (PM endorsed both 6/15.)

2. **(c,3) store gaps — the real privacy bugs**: the **ChromaDB doc store** (`document_service.py` queries by timeframe / empty `where`) + **`stakeholders`** (no owner column; the People-entity backend). → D2/D6; doc store = first migration instance (#1238).

3. **(a,3) leak PATHS in owner-stamped stores** (verified by hand): `conversations.get_by_id():1544` fetches by PK with no owner check; `insights.get_for_object():2316` filters object_id only; `knowledge_nodes` scopes only if `owner_id` is passed; `artifacts.get_by_id` filters post-hoc in Python. → **D3** (scoping-at-read invariant) + **D5** (AST guard: a content-store read must take + apply a principal).

4. **Resolution degradation — the biggest finding (your refinement B)**: the principal IS resolved at the boundary (`auth_middleware.py:177/316`) but then **re-fetched opportunistically** as `user_id = intent.context.get("user_id") if intent.context else None` at **40+ sites** (`classifier.py`, `conversation_handler.py`, `intent_service.py` handlers). Missing/empty context → principal silently becomes `None` → some paths proceed unscoped. **The principal isn't threaded as a required parameter.** → **D4** (principal-resolution-at-the-boundary), likely the highest-leverage fix.

## What I need from you
1. **D1 global-by-design ruling**: the PM-domain cluster — `products`, `features`, `work_items`, `intents`, `workflows`, `tasks` — has no owner. In the single-PM model these read as intentionally-global PM work objects (not leaks). Is that your call (global-by-design, D1 over-anchoring guard), or do they need anchoring for the multi-tenant path? This determines whether `work_items` (the Radar WorkItem backend) needs anchoring before #1239.
2. **Confirm the D1–D7 grounding above** maps to your strawperson (it does, closely — D4 is bigger than the strawperson implied; the resolution epidemic is the dominant vector).
3. Then **I draft ADR-071** (Lead-author / Arch-ratify, post-audit per your sequencing), grounded in this evidence, with the consolidating refactor as the migration (m-40), doc store first.

Audit analytical phase is complete; ADR draft is gated only on your D1 ruling + grounding confirm. — Lead, 2026-06-15
