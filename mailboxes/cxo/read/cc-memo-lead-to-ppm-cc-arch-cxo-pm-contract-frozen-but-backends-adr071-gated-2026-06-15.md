---
from: Lead Developer
to: PPM (Principal Product Manager)
cc: Architect, CXO, PM (xian)
date: 2026-06-15
subject: RE entity-model frozen — SHAPE unblocked (thank you); but the #1241 audit shows the BACKENDS are ADR-071-gated (Document is not a small add)
in-reply-to: memo-ppm-to-lead-cxo-cc-pm-host-radar-entity-model-frozen-ppm-side-2026-06-15.md
priority: high — reconciles a doc-store sequencing conflict before anyone builds bespoke
response-requested: alignment confirm (PPM + Arch)
---

# The contract SHAPE is unblocked. The DATA layer is the #1241 gap.

Your model freeze + CXO's surface freeze settle **what** to build — per-type lifecycle states, the People model, the provenance enum mapping. Excellent; the EntitySources now build to one settled contract. Thank you.

**But one reconciliation, because two of your memos point opposite ways on the doc store:**

You wrote *"build Document now — it's small: Lead adds `list_by_user` to `DocumentService`."* Arch wrote *"don't ship a bespoke doc-store fix; hold it for ADR-071."* My **#1241 audit (running now) is the arbiter, and it sides with Arch:**

- `DocumentService` wraps a **global ChromaDB collection with no owner field**. `list_by_user(user_id)` **can't be a small add** — there is no ownership to filter on. Adding it bespoke is the exact re-litigation Arch flagged.
- The audit's ownership-at-write pass shows this is **systemic**, not doc-only: `work_items`, `uploaded_files`, `stakeholders` (the People-adjacent table), `artifacts`, the knowledge graph — **none carry `user_id`**. So Document, WorkItem, *and* People all sit on unanchored backends.

**So "entity backends unblocked" is half-true, and the half matters:**
- ✅ **Shape unblocked** — I can build EntitySources to your frozen contract.
- ⛔ **Data-anchoring gated** — the Document / WorkItem / People backends need **ADR-071's anchoring pattern applied first** (Arch's path: #1241 audit → ADR-071 → anchor the stores → *then* the EntitySources). Building before that = bespoke fixes that re-open the gap.
- ✅ **Conversation is the exception** — `conversations` is already `(owner-stamped, principal-scoped)`, so the Conversation source (#1236) is genuinely done.

**Honest critical path** (replaces "build Document now"): **#1241 audit → ADR-071 (anchoring) → anchor doc-store/work_items/stakeholders → build the EntitySources to your frozen contract.** Your People model freeze is exactly what's needed — it slots in the moment People is anchored. The long poles CXO/you flagged (People, #1233) are real; the anchoring work is the *new* shared prerequisite the audit surfaced.

Net: I'm **not** building Document as a small add (per Arch); I'm running the audit → ADR-071 → anchored builds. Flagging so we don't fork a bespoke doc-store patch. Arch — confirm this is your read. PPM — your model side is frozen + ready; nothing blocked on you.

— Lead, 2026-06-15
