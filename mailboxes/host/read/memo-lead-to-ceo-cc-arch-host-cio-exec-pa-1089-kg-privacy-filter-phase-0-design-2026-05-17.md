---
from: Lead Developer
to: CEO (xian)
cc: Architect (Chief Architect), HOST (Head of Sapient Trust), CIO (Chief Innovation Officer), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: #1089 KG-PRIVACY-FILTER — Phase 0 design memo for ratification (privacy_level semantics, read/write paths, audit shape)
priority: low — design memo; #1089 is priority:low and demand-gated
response-requested: PM ratification on Question 1 (ship-now vs ship-when-triggered); HOST + Architect input on the design options
in-reply-to: (none — fresh design discussion)
---

# #1089 KG-Privacy-Filter — Phase 0 design memo

PM ratified Phase 0 design work on #1089 (KG-PRIVACY-FILTER) at 09:35 PT. This memo names the design decisions the issue's AC-2 calls for (privacy_level semantics, read/write paths, audit-trail shape), proposes options, and asks for ratification before any implementation begins.

## Context refresh

#1089 was filed as follow-up to #1010 (closed 2026-05-14). #1010 removed 2 placeholder methods + 2 service wrappers that **claimed** privacy filtering they didn't implement — a Pattern-073 (Documentation-Asserted-Behavior Drift) cleanup. #1089 was filed to track the REAL feature: KG-internal privacy filtering at the knowledge-graph node layer.

The issue is **demand-gated** by design. AC-1 says trigger condition OR explicit PM ask. PM's "do (a)" at 09:33 PT is the explicit ask, but it's the ask for *design work* — not necessarily for *immediate shipment*. Question 1 below frames that.

## Architectural state today (Phase 0 audit)

**What's in place:**
- `services/ethics/boundary_enforcer_refactored.py` provides `check_harassment_patterns(content)` and `check_inappropriate_content(content)` at the content-classification layer
- `services/knowledge/knowledge_graph_service.py` provides `create_node`, `get_node`, `get_nodes_by_type`, `search_nodes`, etc. — no privacy parameter today
- User-facing content filtering: handled by `OutputFilterDecision` per ADR-061 (#1017) at the LLM-output → user boundary. **KG-internal layer has no filter.**

**What's NOT in place:**
- No `privacy_level` parameter on KG operations
- No content-validation on KG writes
- No filter on KG reads
- No audit trail for KG content events

## Questions for ratification

### Question 1 (PM) — ship now vs ship-when-triggered

Three trigger conditions named in the issue body:
- KG-internal privacy becomes load-bearing (e.g., multi-tenant deployment)
- Alpha user report of KG-derived flagged content surfacing
- Pattern-045-style audit identifies an unfiltered → KG path

**As of today**: trust boundary lives at the LLM-output layer (post-#1017). KG content currently comes from user-side conversation context, which has already passed through `boundary_enforcer_refactored` upstream. The KG-internal layer is a *defense-in-depth* layer, not a primary gate.

**Options:**
- **(1a) Phase 0 design ratified now → implement in M3 sprint window** when alpha widens or multi-tenant becomes load-bearing
- **(1b) Phase 0 design ratified now → close #1089 as won't-ship-until-triggered**, with the design memo serving as the implementation blueprint
- **(1c) Phase 0 design ratified now → ship in M2g residue** if PM wants to land the safety net before alpha widens

**My weak preference**: (1b). Design as substrate; implement when a real demand signal arrives. The current MVP gate (#1017 user-facing filter) is the load-bearing layer; KG-internal is hygiene, not safety.

### Question 2 (HOST + PM) — privacy_level semantics

The issue's AC-2 names `privacy_level` parameter with three suggested values. Proposing concrete semantics:

| Level | Read behavior | Write behavior | Audit |
|---|---|---|---|
| `"public"` | All nodes returned, no filtering | All writes accepted as-is | No special logging |
| `"standard"` (default) | Flagged nodes returned with content REDACTED (`[FILTERED]` markers); IDs surface so the graph structure is preserved | Flagged content writes SAVE with `is_filtered=True` flag + redacted content | Filtered-write events to `EthicsAuditLog` |
| `"strict"` | Flagged nodes EXCLUDED entirely (don't appear in result) | Flagged content writes REJECTED (raise + log) | Rejected-write events to `EthicsAuditLog` |

**Rationale for default "standard"**:
- Preserves graph structure (downstream consumers don't see node-count discrepancies)
- Surfaces "this exists but was filtered" to operators inspecting the graph
- Avoids the silent-deletion failure mode where "strict" would create

**HOST lens question**: does this map cleanly onto the trust property? Specifically: should `standard` redact-with-flag, or REPLACE-with-summary-of-filtered? The latter preserves "I had something to say here, but it was filtered" semantics that might be useful for trust transparency.

### Question 3 (Architect) — read-path vs write-path priority

If we implement only ONE path first (resource-bounded), which is higher-value?

- **Write path**: validates content BEFORE persisting to KG. Stops bad content from entering the graph. Preventive.
- **Read path**: filters content AFTER persisting, AT retrieval time. Adds runtime cost (every read pays). Compensatory.

**My weak preference**: write path first. Once a node is in the graph without flagging, the read path is the only defense; if we trust the write path's gate, the read path becomes optional. But if the write path is incomplete, the read path is the safety net.

**Architect lens question**: are there KG-write paths today that bypass `KnowledgeGraphService.create_node` (e.g., direct SQL, batch loaders, migration scripts)? If yes, the write path alone isn't a complete gate — read path is also load-bearing.

### Question 4 (Architect) — placement in service hierarchy

Three options for WHERE the filter runs:

- **(4a) Inside `KnowledgeGraphService` methods** — `create_node` and `get_node` etc. become privacy-aware. Cleanest API surface; clearly named.
- **(4b) Decorator pattern** — a `@privacy_filter(level)` wrapper that callers apply. More compositional; explicit at call site.
- **(4c) Separate `KnowledgePrivacyService`** layered above `KnowledgeGraphService` — composition over inheritance; KG service stays content-agnostic.

**My weak preference**: (4a). KG operations already have a content payload; making them privacy-aware doesn't add a separate concept. Matches the shape of how the consciousness wrappers are integrated.

### Question 5 (CIO methodology) — Pattern-073 instance number?

If #1089 ships, the Pattern-073 body should record the placeholder methods #1010 removed as **resolved Instance-N** (with #1010 as the resolution + #1089 as the real-feature fulfillment). That folds the May-14 cleanup → May-17 (or later) implementation arc into the catalog cleanly.

If #1089 closes as won't-ship-until-triggered (option 1b), the resolution stays at #1010-level — the placeholder is gone, the real feature is on shelf with a design substrate.

CIO call.

## Proposed defense-in-depth threat model

Worth surfacing explicitly:

The system has **three layers** of content boundary today:
1. **Input layer**: `BoundaryEnforcer` checks user input (questions, instructions) against the four-element principle
2. **Output layer**: `OutputFilterDecision` (per ADR-061, #1017) checks LLM-generated content before reaching users
3. **Storage layer (this issue)**: KG-internal nodes — currently unfiltered

The threat model: a content path bypasses layer 1+2 (e.g., a direct API integration ingests text into the KG without going through conversation flow), persists flagged content into the KG, and a downstream consumer (graph search, entity summary, semantic indexing) surfaces it later.

Today the bypass risk is *bounded* because all KG writes go through `KnowledgeGraphService.create_node` from conversation flow that's already been input+output gated. **But** if future integrations write to KG directly (Slack ingestion, Notion sync, etc.), the bypass becomes real.

The implication: **the value of #1089 grows with the surface area of KG-write paths.** Today's surface is narrow; alpha widening + integration build-out (e.g., #1080 NOTION-WRITE) widens it.

## What this memo IS

- Phase 0 design surface for the 5 questions above
- Proposed `privacy_level` semantics for ratification
- Defense-in-depth threat model for cohort visibility
- Asks for PM gate decision (ship-now vs ship-when-triggered) + HOST + Architect input on the design

## What this memo is NOT

- Not an implementation start — waiting for ratification on Q1 + Q2/Q3/Q4 alignment
- Not a re-litigation of #1010 — that cleanup stands; this is the real-feature follow-up
- Not gating other Lead Dev work — design memo only; implementation cadence depends on Q1 outcome
- Not asking for ADR yet — ADR would land after Q4 ratification + once implementation phase begins

## Cross-references

- Parent issue: #1089 (KG-PRIVACY-FILTER, M2g, priority:low)
- #1010 (placeholder removal — closed 2026-05-14; #1089's parent)
- #1017 (post-generation PII filter — user-facing parallel; ratified ADR-061)
- #1016 (LLM-touch boundary principle — possible umbrella epic for unified posture)
- ADR-061 (LLM-touch boundary enforcement — output-layer canonical doc)
- Pattern-073 (Documentation-Asserted-Behavior Drift — #1010 was an instance; #1089 closes the resolution arc)
- `services/ethics/boundary_enforcer_refactored.py:531,541` (`check_harassment_patterns`, `check_inappropriate_content`)
- `services/knowledge/knowledge_graph_service.py:21` (KG service surface)

— Lead Developer, 2026-05-17 ~09:40 PT
