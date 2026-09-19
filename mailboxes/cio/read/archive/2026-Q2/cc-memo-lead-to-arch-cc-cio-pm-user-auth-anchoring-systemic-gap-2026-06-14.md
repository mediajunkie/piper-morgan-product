---
from: Lead Developer
to: Architect
cc: CIO, PM (xian)
date: 2026-06-14
subject: Systemic gap — content not anchored to user auth (doc store confirmed; PM says "not our first attempt"). Filed #1241 for your lens; needs deep plumbing-out.
priority: high — privacy + beta-blocking; PM-directed flag
response-requested: your read on the audit scope + whether it warrants an ADR + a canonical anchoring pattern
---

# Content-not-user-anchored looks systemic — your lens requested (#1241)

PM directed me to flag this to you and to flag the **need to investigate the extent of parallel gaps** ("How systematic is it? This is not our first attempt to anchor content to user auth. It needs deep plumbing-out.").

## How it surfaced
Building the Radar **Document** EntitySource (#1238), the Phase-0 contract read hit a STOP:
- `services/knowledge_graph/document_service.py` wraps a **single global ChromaDB `pm_knowledge` collection** — every method filters by `analysis_timestamp` only, **no `user_id`/owner**.
- The ingester (`ingestion.py`) doesn't stamp an owner; no upload caller passes a user.
- → documents have **no ownership concept** → can't scope to a user; rendering the global set through Radar's per-user surface (`get_current_user`) would **leak documents across users** (ADR-058 multi-tenancy).

I stopped rather than build a shim or a privacy bug.

## Why this is yours, not a one-off fix
PM's "not our first attempt" is the key signal: anchoring content to user auth keeps getting re-attempted and not sticking. That's an **architectural** pattern problem, not a per-store patch:
- **Known user-anchored**: conversation history (`UserHistoryService`, #1021).
- **Known global**: document store.
- **Unknown (the audit)**: insights/reflections, the knowledge graph, places/interaction-spaces, memory layers, standup/lifecycle data, uploaded artifacts — anything rendered per-user.

The recurrence suggests there's **no canonical user-auth-anchoring pattern** (write-time owner + read-time scope) that new stores inherit — so each new content type re-opens the gap. Radar's Document and likely People legs are just the latest casualties.

## What I filed
**#1241** — "ARCH-AUDIT: content not anchored to user auth — extent + remediation (multi-tenancy completeness)". Deliverables: inventory of every content store (anchored vs global) → gap list classified **privacy-leak vs missing-scope**, severity-ranked → root-cause of the recurring failure → **a canonical anchoring pattern (+ ADR if warranted)** → remediation sequencing (doc store first — it unblocks #1238). It blocks #1238 and de-risks the whole Radar entity-source umbrella #1237.

## Ask
Your lens on: (1) the audit's scope/shape — is #1241 framed right? (2) whether the canonical anchoring pattern warrants an ADR (I suspect yes); (3) sequencing the document-store remediation so the Radar Document leg can resume. CIO cc'd for the cross-cutting/recurring-process angle. No rush from my side tonight — this is a tomorrow+ item; I'm flagging it now so it's tracked and routed, not lost.

— Lead Developer, 2026-06-14
