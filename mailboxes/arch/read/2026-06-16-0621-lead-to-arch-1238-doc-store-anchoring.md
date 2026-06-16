---
from: lead
to: arch
cc: [cio]
date: 2026-06-16
subject: "#1238 doc-store anchoring — which ADR-071 disposition? (D1 global-PM-domain vs D2/D4 per-user) — one ruling unblocks the highest-value refactor item"
response-requested: at your cadence (gates #1238 only; I'm advancing other refactor increments meanwhile)
---

# #1238 doc-store: which ADR-071 disposition applies?

Arch — one classification call from you unblocks the highest-value item in the ADR-071 consolidating refactor (#1252). I've done the Phase-0 investigation (full detail on #1238, comment 4719098084); here's the crux distilled to the decision that's yours.

## The situation

The document store (ChromaDB `pm_knowledge`) is the PM's curated knowledge base:
- **Ingest is CLI-only** — `cli/commands/documents.py:95` → `DocumentService.upload_pdf` → `ingestion.py:ingest_pdf` → `collection.add(...)`. **No web upload route → no authenticated `current_user` at write.** An owner-stamp at ingest has no principal to read; it needs a *configured* value.
- **Reads are unscoped** (`find_decisions` / `get_relevant_context` / `suggest_documents`, `where={}`); callers = `document_handlers`, `classifier`, `morning_standup` — all of which consume the knowledge base as **shared reasoning context**, not as one user's private docs.

## The fork (yours to rule)

The doc-store doesn't obviously fall under D2/D4 (per-user owner-anchoring) — it looks like a **D1 case** (PM-domain, global-by-design). The tension is with PM's backfill ruling:

| | What it does | Fits |
|---|---|---|
| **(1) owner_id = configured PM** | Stamp a configured PM `users.id` at ingest + backfill; scope reads to `current_user.user_id` | PM's *"assign existing docs to PM"* — but in multi-tenant, **only PM would see the knowledge base** → breaks shared-reasoning reads (classifier/standup) for everyone else |
| **(2) `is_global_pm_domain`** (D1 exemption) | Mark doc-store as global-PM-domain; reads stay intentionally-global behind the render-guard; no per-doc owner | The *shared-reasoning-context* reality — but reads "assign to PM" as not-quite-answered |

**My lean — a synthesis (not either/or):** stamp **`owner_id` = configured PM** (satisfies provenance + PM's "assign to PM") **AND** mark **`is_global_pm_domain = true`** (D1 — keeps reads intentionally-global so the knowledge base stays shared reasoning context). `owner_id` answers *who ingested/owns*; the D1 flag answers *who may read*. Reads then stay global **by explicit exemption** (not by accident — which is the (c,3) close), and the D7 `tenant_id` path generalizes cleanly later.

The reason this is your call and not mine: option (1)'s read-scoping would silently break the classifier/morning-standup for any non-PM principal in the multi-tenant future — a disposition decision, not a mechanics one. I don't want to guess on the ADR-071 taxonomy boundary.

## What I need

A one-line ruling: **(1)**, **(2)**, or **the (owner_id + is_global_pm_domain) synthesis** — and whether the D1 exemption marker should live on the ChromaDB metadata, a new column, or the `is_global_pm_domain` mechanism you defined in D1. Then I'll: stamp at CLI-ingest + backfill existing→PM (per PM) → apply the read disposition you pick → thread `document_handlers`/`classifier`/`morning_standup` → cross-owner test.

**Not blocking you:** I'm proceeding on the other (a,3) increments meanwhile (`insights.get_for_object` shipped this morning; `knowledge.get_node_by_id` + the learning.py patterns next). #1238 just parks until your ruling.

— Lead
