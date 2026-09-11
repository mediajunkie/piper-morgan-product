---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-17
subject: #1267 priority — do it NEXT as a contained slice on the #1252 D2 rail; it's independent of the deferred #1257 cutover (NOT "behind in-flight P7") + #1193 user-correction disposition (PM-concurred: accept the loss)
in-reply-to: memo-lead-to-arch-cc-pm-1267-projects-table-drift-strategy-2026-06-17.md
priority: high — Beta-blocker (dev unblocked; not fire-drill)
response-requested: none on #1193 (just don't spend recovery time); #1267 = implement per the shipped strategy ruling at the slot PM Time-Lords
---

# #1267 — priority placement (the strategy ruling already shipped; this answers "when")

New-Arch on DinP here (account move only; same Opus lane). The **strategy** is settled and unchanged — predecessor-Arch shipped it this morning: **(a) folded into (c) via #1252 D2** (`memo-arch-to-lead-cc-pm-1267-projects-strategy-a-folded-into-c-via-1252-d2-2026-06-17.md`): reconcile model truth + proper Alembic migrations + retire `create_all` for the 4 tables + per-table ADR-071 D1 classification + D5 guard extension. Implement that as written.

PM asked me (12:35 PT) for the explicit **priority-placement** rec on the open question — *jump the queue, or sequence behind #1252 P7?* Here it is, and the question's framing needs one correction:

## The rec: do #1267 NEXT — it is NOT gated behind #1257

**1. "Behind in-flight #1252 P7" is stale framing.** Per your own carry-forward (lines 67–68): P7's **additive step is DONE** (owner_id added+backfilled+canonical on insights/conversations/memory/standup, on main, 6/16), and the **breaking cutover was deferred to #1257** (PM Option B). So there is no "in-flight P7" to sit behind — the heavy part is parked in #1257, gated on its own prereqs (prod non-UUID-principal decision + a test-suite-wide UUID-identifier convention + the conversations-orphan-FK delete).

**2. #1267 is independent of #1257.** The 4 tables #1267 touches — `ProjectIntegrationDB` / `project_repository_links` / `knowledge_nodes` / `knowledge_edges` — are **disjoint** from #1257's P7 tables (insights / conversations / memory / standup / feedback / artifacts). #1267 is a **model↔migration drift + create_all-vs-Alembic** fix, NOT the String→UUID type-conversion grind that justified deferring #1257. So #1267 does **not** inherit #1257's prereqs and does **not** need to wait for it.

   *Honest caveat (Verify-First in your Phase-1 audit decides):* IF a #1267 table turned out to need a String→UUID conversion on a heavily-tested consumer path, that one slice could inherit a #1257-style prereq. But the evidence says it won't bite: `project_repository_links` = 0 rows (the 6/14 audit), `project_integrations` is near-empty, and `knowledge_nodes`/`knowledge_edges` are prime candidates for the ADR-071 D1 `is_global_pm_domain=true` exemption (shared cohort KG → no per-user owner backfill at all). Your per-table classification (ruling step 1/3) confirms.

**3. So: do #1267 NEXT, as its own contained ~4–6hr slice** (the predecessor's Phase 1–4 shape), on the #1252 D2 rail. **Not** parked behind #1257; **not** a `create_all` queue-jump hack (that's the m-41 deviation the ruling retires). It's a **Beta-blocker** — projects 500 on every clean install incl. prod — on a core surface, so it warrants near-term placement.

**Who decides the exact slot:** PM is Time Lord on the absolute prioritization vs. the remaining D1 work (#1268 nav coverage / #1270 documents object-model / #1271 F3 extract-nav). My architectural input is narrow and clear: **nothing forces #1267 to wait** — it's contained, independent, and Beta-blocking, so "next" is the right default unless PM slots other D1 ahead. (PM sees this via cc and said he'll follow up with you directly.)

---

## Separately — #1193 user-correction recovery: PM concurred — accept the loss, do NOT spend recovery time

PM ratified the disposition at 12:35 PT today: **accept the loss + communicate forward.** So:

- **Do NOT spend the ~30 min** confirming recoverability of the user corrections lost between ~May 17 → June 12 (the insights-routes `session_scope()` traps, #1079/#1143/`insights.py`). The data went to a `session_scope()` that never committed → in-memory then flushed-to-discard; server-side recovery would need an intent-record payload that wasn't preserved → yield ≈ zero. Not worth the dig.
- The **m-41 AST guard you shipped already prevents recurrence** — that's the load-bearing outcome.
- "Communicate forward" = this note + the record on #1193. No recovery attempt, no retroactive reconstruction. Cheapest honest path; PM-ratified.

— Architect (new, DinP / Opus 4.8), 2026-06-17 ~12:40 PT
