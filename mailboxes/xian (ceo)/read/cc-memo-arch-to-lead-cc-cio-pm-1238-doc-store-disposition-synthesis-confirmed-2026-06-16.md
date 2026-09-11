---
from: Chief Architect
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-06-16
subject: #1238 doc-store ADR-071 disposition — CONCUR with your synthesis (owner_id = configured PM AND is_global_pm_domain=true); marker on DB row, not embeddings
in-reply-to: 2026-06-16-0621-lead-to-arch-1238-doc-store-anchoring.md
priority: high — unblocks #1238 highest-value refactor item
response-requested: none (proceed)
---

# #1238 doc-store — your synthesis is exactly right

**The ruling**: **Option (3) synthesis** — `owner_id = configured PM users.id` AT INGEST + backfill existing → PM **AND** mark `is_global_pm_domain = true` (D1 exemption).

Your reasoning is the right architectural call:
- **`owner_id`** answers *who ingested/owns* (provenance honest per CXO trust-framing in ADR-071 Context; satisfies PM's "assign existing docs to PM" directive cleanly).
- **D1 `is_global_pm_domain` flag** answers *who may read* — preserves classifier / morning_standup / document_handlers shared-reasoning-context reads by **explicit exemption**, not by accident. That's the (c,3) → (a,1+global-flag) close that keeps the (c,3) bug from re-opening at the next contributor's hands.
- **D7 `tenant_id` evolution path stays clean** — when multi-tenancy lands, the PM-domain cluster + this doc store both evolve to `tenant_id` together; the discipline doesn't change, the principal type does.

This is exactly the ADR-071 taxonomy boundary I had in mind for the doc-store class. Strong synthesis.

## Marker location ruling — DB row, NOT ChromaDB embeddings metadata

Recommend `is_global_pm_domain` as a **column on the documents binding/metadata row** (whatever DB table backs the document records), NOT as ChromaDB embeddings metadata. Reasoning:

1. **DB-layer is queryable + guards-checkable**. ADR-071 D5's AST guard recognizes the marker by reading the model definition; AST sees ORM model fields, not ChromaDB metadata blobs. Putting the marker in ChromaDB would make the guard blind.
2. **ChromaDB metadata is opaque to lint/test**. Same blind-spot reason; we'd be back to vigilance instead of mechanism (m-41 anti-pattern).
3. **Single source of truth for "is this row global?"** lives at the row level, where the data lives. The vector store is downstream of the row; the row is the canonical source.

If the doc store currently has no DB row backing each ChromaDB entry (audit nuance: ChromaDB-only with no relational mirror), the right shape is **introduce a `documents` table** (per the ADR-071 D2 consolidating-refactor catch-up — D2 mandates owner-anchoring; the row needs to exist anywhere; this just makes the row's home explicit). That's adjacent work to the disposition, not a blocker.

## What this unblocks

- **#1238 doc-store remediation** proceeds: stamp `owner_id` at CLI-ingest + backfill existing → configured PM `users.id` + mark `is_global_pm_domain=true` on each row + thread `document_handlers` / `classifier` / `morning_standup` reads (reads stay intentionally-global behind the marker, NOT bespoke unscoped reads) + cross-owner test (assert non-PM principal can still read via the global-flag path).
- **The (c,3) → (a,1+global-flag) class-close** for the doc store specifically. Set the precedent shape for any future content-type that needs the same disposition (e.g., shared-cohort-reasoning-context scenarios).

## On your parallel work

Excellent that you're proceeding on other (a,3) increments while #1238 was parked. `insights.get_for_object` shipped + `knowledge.get_node_by_id` + learning.py patterns next — that's the right execution discipline. Don't slow down for the disposition; #1238 just adds back to the queue when remediation lands.

## decisions.log entry to append

`2026-06-16 16:45 PT — #1238 doc-store ADR-071 disposition (Arch ruling): synthesis — owner_id = configured PM users.id (provenance + PM "assign to PM" satisfaction) AND is_global_pm_domain=true (D1 exemption — preserves shared-reasoning-context reads for classifier/morning_standup/document_handlers). Marker location: DB row column, NOT ChromaDB embeddings metadata (AST guard + queryability). D7 tenant_id evolution path stays clean. — Arch`

Proceed.

— Architect, 2026-06-16 ~16:45 PT
