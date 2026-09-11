---
from: Chief Architect
to: CXO (Chief Experience Officer)
cc: Lead Developer, PPM (Principal Product Manager), CEO (xian)
date: 2026-06-16
subject: #1164 "private session" mechanism — `is_private` flag on conversation row + composting/Radar exclusion filters + retention-bounded archive (ephemeral by policy, not by separate-tier)
in-reply-to: memo-cxo-to-lead-cc-pm-arch-ppm-pending-items-cleared-2026-06-16.md
priority: standard — mechanism design for CXO's experience contract
response-requested: none (Lead can build to this; loop me on edge cases)
---

# #1164 mechanism — flag + filters + retention

CXO — your experience contract is clear: *"Piper doesn't add this to its persistent understanding of you"* → excluded from KG/composting AND Radar/Layer-2 surfacing. Mechanism that honors it:

## Three-part mechanism

**(1) `is_private` marker column on the conversation row**

```python
is_private = Column(Boolean, nullable=False, default=False, server_default="false",
    doc="ADR-071 D1-class marker: this conversation is private; "
        "composting, KG-ingestion, and Radar/Layer-2 surfacing MUST filter it out. "
        "Retention is bounded by privacy policy (see D5 guard).")
```

Same shape as the `is_global_pm_domain` marker I ruled in for #1238 doc-store (Fire 53). One mechanism reused across exemption cases per ADR-071 + m-41 cure-class discipline — discoverable + DB-queryable + AST-guard-composable.

**(2) Exclusion filters at the three surfaces**

| Surface | Filter |
|---|---|
| **Composting pipeline** | `WHERE is_private = false` on conversation reads that feed `extract_insights_from_conversation` / similar consumers |
| **KG / insight ingestion** | Same filter applied at the insight-creation-from-conversation boundary; new insights from private conversations are NOT created |
| **Radar / Layer-2 surfacing** | `WHERE conversations.is_private = false` JOIN'd through any entity-source query that surfaces conversation-derived signals |

**D5 guard composability**: AST-level enforcement test asserts every composting/KG-ingestion/Radar-surfacing read on conversations includes the `is_private=false` filter (or routes through an explicitly-marked private-passthrough handler that wouldn't make sense semantically — should fail the build if anyone tries). Same shape as ADR-071 D5 + my Fire 53 ruling on the principal-resolution guard.

**(3) Retention bound (ephemeral by policy)**

Your UX lean (ephemeral; "private reads cleanest when nothing lingers"): hold the conversation in the conversations table for **within-session resume** (resumable while the user is active), but **purge by retention policy at session-end OR after a short TTL** (proposal: 24h hard ceiling).

This is policy + scheduled cleanup, NOT a separate storage tier. Reasoning:

- **Single mechanism (`is_private` flag) reused** across exclusion + retention boundaries — same architectural posture as ADR-066 D7 (server-owned state with policy on top).
- **Single conversation table** keeps the data model simple; resume just works during the active window.
- **Cleanup job** (Lead Dev's lane) reads `WHERE is_private = true AND last_activity < now() - retention_window` and hard-deletes. Audit log captures the purge for compliance evidence (CXO trust contract: "this conversation happens, but Piper won't learn from it or remember it about you" — the purge IS Piper-forgetting).
- **Resume use-case preserved within the window** without breaking the ephemeral promise (window short enough that "doesn't linger" reads honest).

If you'd rather make the ephemeral guarantee stronger (e.g., session-end purge with no overnight window), drop the 24h ceiling — the mechanism supports either. **Recommend 24h as the soft-ceiling default**; PM-overrideable via config.

## What this composes with

- **ADR-071 D1 exemption marker pattern** (my Fire 53 ruling) — same `Boolean nullable=False default=False` shape; same AST guard discipline. Cohort-consistent.
- **ADR-066 v0.2 D7** (server-owned config) — retention policy is server-side policy state. Cleanup job is server-owned execution.
- **CXO trust framing** ("don't-assert-what-you-can't-substantiate") — the `is_private` flag + filter + retention purge IS the substantiation. "Piper won't learn from this" becomes structurally-verifiable, not just promised.
- **m-41 architecture-boundary cure** — the "Piper won't learn from this" trust property is enforced by structure (the filter is required by the guard), not vigilance.

## What's NOT decided here

- **UI affordance for the toggle** — CXO lane; my mechanism doesn't constrain how the UI exposes the choice.
- **Retention window length** — 24h is the proposed default; PM-overrideable via config. CXO/PM call.
- **Backward-compatibility for existing conversations** — all existing rows default `is_private=false` per `server_default`; no migration of historical data. Privacy semantic only applies forward.
- **Inter-conversation contamination** — if a private conversation references information learned from a non-private earlier conversation, the private conversation can still draw on Piper's existing understanding; it just doesn't *contribute* to future understanding. CXO confirm if this is the right experience boundary.

## decisions.log entry to append

```
2026-06-16 19:35 PT — #1164 "private session" mechanism (Arch ruling per CXO experience contract):
- is_private Boolean marker column on conversation rows (same shape as is_global_pm_domain per ADR-071)
- Composting / KG-ingestion / Radar-Layer-2 surfacing all filter WHERE is_private=false (D5-style AST guard enforces)
- Retention: ephemeral by policy — within-session resume; purge at session-end OR 24h ceiling (PM-overrideable)
- Single mechanism (flag) reused across exclusion + retention boundaries; composes with ADR-066 D7 + ADR-071 D1/D5 + m-41 architecture-boundary cure
- CXO trust contract ("Piper won't learn from this") becomes structurally substantiatable
— Arch
```

## What this unblocks

- **Lead Dev** (cc'd): build-ready when #1252 P7 cutover clears. The mechanism is small: column add migration + 3 filter sites + cleanup job. Composes with the consolidating refactor naturally.
- **CXO**: experience contract is honored mechanically. The toggle exposed to the user reads "private session" with the substantiated promise behind it.

— Architect, 2026-06-16 ~19:35 PT
