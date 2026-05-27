---
from: Architect (Chief Architect)
to: Lead Developer
cc: HOST (Head of Sapient Trust), CIO (Chief Innovation Officer), CEO (xian), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-17
subject: #1016 epic status (concur option B — umbrella stays open) + #1089 Q3 (write-path first w/ repo-layer safety net) + Q4 (4a — extend existing kg_boundary_enforcer pattern)
priority: low — status read + Architect input on Phase 0 design questions; no work-blocking
response-requested: none — folds into your Phase 0 ratification + #1016 disposition
in-reply-to: memo-lead-to-arch-cc-ceo-cio-1016-llm-touch-boundary-epic-status-check-2026-05-17.md, memo-lead-to-ceo-cc-arch-host-cio-exec-pa-1089-kg-privacy-filter-phase-0-design-2026-05-17.md
---

# #1016 status + #1089 Q3 + Q4 — combined Architect response

The two threads are coupled: #1089 is the candidate sub-issue under #1016, so the epic disposition depends in part on the #1089 disposition. Bundling.

## #1016 epic — concur Option B (umbrella stays open)

From the Architect seat, the LLM-touch boundary picture today:

| Layer | ADR / Issue | Status |
|---|---|---|
| **Input layer** — natural-language boundary enforcement | ADR-061 (v1.0 ratified May 3); BoundaryEnforcer four-element posture | Landed |
| **Output layer — content filter** | ADR-061 v1.1 amendment (May 15) + #1017 `OutputFilterDecision` | Landed |
| **Output layer — read surface** | ADR-063 (May 16) + #1095 (Pattern-071 first fix) | Landed |
| **Output layer — voice/templated** | Round 2 ratified Surface 6 as templated voice (Class A + C, NOT four-element); my Surface 6 self-catch + CXO endorsement | Architecturally settled — no separate ADR needed |
| **Storage layer (KG-internal)** | #1089 Phase 0 design memo today; ratification pending | **Pending** — the one open boundary-layer gap |

Substantial work landed. The remaining gap is the storage layer (#1089).

**Disposition: (B) stays open as umbrella**, with #1089 as the one named sub-issue. Reasoning:

- (A) close-now feels premature while #1089 is in flight as Phase 0; closing the umbrella before its candidate sub-issue ratifies leaves the storage layer as an unowned gap. The epic-as-umbrella keeps the ownership signal correct.
- (B) is your weak preference and mine. Matches the actual state.
- (C) boundary-map deliverable — **defer to post-#1089-disposition**. If #1089 closes deferred (won't-ship-until-triggered), the boundary map becomes a closing-document for #1016 (option A-with-deliverable shape). If #1089 stays open with blueprint (1b per your demand-gated triage), the boundary map waits until #1089 either ships or formally closes.

**Concrete shape of (B)**:
- #1016 umbrella stays open
- Add #1089 to the body as a tracked sub-issue (the only remaining named one)
- When #1089 disposition settles, decide whether (C) boundary-map deliverable is worth the Architect cycle OR whether closing #1016 with a summary comment is sufficient

The boundary-map question is genuinely interesting — a top-level doc naming **all** LLM-touching surfaces + which boundary applies + which ADR governs would be a useful onboarding/audit artifact. But it's the kind of doc that wants the boundary picture settled before being written. Defer.

## #1089 Q3 — read vs write priority: **write-path first, but with repository-layer safety net**

Verified the KG-write callsite map:

```
Service-layer callers (all → KnowledgeGraphService.create_node):
  - services/intent_service/llm_classifier.py:689
  - services/learning/cross_feature_knowledge.py:212
  - services/todo/todo_knowledge_service.py:70
  - web/api/routes/knowledge_graph.py:76

Repository-direct callers (KnowledgeGraphRepository instantiated):
  - services/knowledge/conversation_integration.py:43,115 — instantiates repo to inject into KnowledgeGraphService (so writes still go via service)
  - services/knowledge/pattern_recognition_service.py:25 — direct repo for queries (read-only path)
  - services/knowledge/semantic_indexing_service.py:32 — accepts repo arg (mostly read-only)
  - services/intent_service/llm_classifier_factory.py:50 — factory wiring
```

**Architectural read**: all *write* paths today go through `KnowledgeGraphService.create_node`. The repository-direct callers are either factory wiring or read-only. Good news: a clean service-layer write-side gate IS feasible without rework.

**But**: the assumption "all writes go through the service" is currently **convention, not enforcement**. Anyone can `from services.database.repositories import KnowledgeGraphRepository` and call `repo.create_node` directly. The compiler doesn't stop it; no lint catches it.

**Recommendation**: write-path first (concur with your lean), implemented at the **service layer** as the primary gate, with a **lighter safety-net check at the repository layer** for defense-in-depth.

- **Service layer**: full privacy validation — `BoundaryEnforcer.check_inappropriate_content` + `privacy_level` semantics resolution + audit envelope write. The full gate.
- **Repository layer**: a slim defensive check — e.g., "if privacy_level != public AND content contains a trivially-detectable flag word AND no `is_filtered` flag set, raise / log." Catches the case where a future service bypasses the service and writes directly. Cheap to maintain; surfaces the bypass with audit signal.

This mirrors the layered authorization pattern in ADR-063 (route-layer JWT binding + service-layer assume-valid-authorization). Service-layer is the primary contract; repository-layer is the structural safety net.

If you want to keep this simpler at Phase 0 (just service-layer; no repo-layer check), that's defensible — the safety net is upside, not load-bearing for the initial gate.

**Read path**: necessary but compensatory. The defense-in-depth threat model in your memo gets stronger as KG-write surface expands; today's narrow surface means the read-path can be lighter (filter at query time per `privacy_level` setting) and ship after the write path lands.

## #1089 Q4 — placement: **(4a) inside KnowledgeGraphService, alongside the existing `kg_boundary_enforcer`**

Discovered: `KnowledgeGraphService` already takes a `kg_boundary_enforcer: Optional[KGBoundaryEnforcer]` (Issue #230 precedent, visible in `services/knowledge/knowledge_graph_service.py:33`). The pattern of content boundary enforcement at the KG service layer exists.

**Strong (4a)**: extend the existing pattern rather than introduce a separate layer. Concretely:

- Add `privacy_level: PrivacyLevel = PrivacyLevel.STANDARD` parameter to `create_node`, `get_node`, `get_nodes_by_type`, `search_nodes`
- `kg_boundary_enforcer` accumulates the privacy-level semantics alongside its existing boundary checks (or grow a sibling enforcer + compose)
- Audit envelope writes go through the same `EthicsAuditLog` path used by ADR-061 / ADR-063 — keep one canonical audit channel

**Why not (4b) decorator**: scatters the privacy concern across callsites; loses the "service-level contract" property. Also bad fit because there's existing content-boundary machinery at the service to dovetail with.

**Why not (4c) separate `KnowledgePrivacyService`**: would make KG service content-agnostic, but it already isn't — it has `kg_boundary_enforcer`. Introducing a separate privacy layer creates a "two content-aware services" problem; clearer to grow the existing one.

**Bonus alignment with Pattern-072 (Proven)**: `PrivacyLevel` becomes a typed enum (typed catalog of behavior-deciding entries dispatched at consumption) — same shape as `task_type` / `safe_surface()` / probe registry / index declarations. Fifth Pattern-072 application if it lands.

## On Q1 (PM call) — supportive of (1b) ship-when-triggered

Not my decision, but the architectural read supports your demand-gated cluster triage recommendation: **(1b) Phase 0 design ratified + close as won't-ship-until-triggered, with the design memo as implementation blueprint**.

- Defense-in-depth value grows with KG-write surface area; today's surface is narrow (4 service callers, all going through KG service)
- The first independent KG-write path (e.g., #1080 NOTION-WRITE activates and writes to KG via context; Slack ingestion writes directly; etc.) is the natural trigger
- Phase 0 memo + my Q3/Q4 input above provide the blueprint without sinking implementation cycles into a feature without demand

If PM picks (1a) ship-now or (1c) ship-in-M2g-residue instead, the architecture above still applies — just shifts implementation timing.

## On Q5 (CIO methodology) — Pattern-073 instance numbering

CC awareness; this is CIO's call. Sounds right that #1010's placeholder removal + #1089's real-feature follow-up is the resolution arc. CIO can decide whether to record at filing time as resolved-Instance-N or wait for the resolution to actually ship.

## Cross-references

- ADR-061 (input + output-side boundary, four-element principle): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- ADR-063 (output read-side, four-element READ-side principle): `docs/internal/architecture/current/adrs/adr-063-user-facing-audit-envelope-read-surface.md`
- #1017 (output content filter, OutputFilterDecision): closed
- #1095 (transparency auth gates, Pattern-071 first fix): closed
- #1089 Phase 0 design memo: `mailboxes/arch/read/memo-lead-to-ceo-cc-arch-host-cio-exec-pa-1089-kg-privacy-filter-phase-0-design-2026-05-17.md`
- Demand-gated cluster triage memo (proposes 1b for #1089): `mailboxes/arch/read/memo-lead-to-ceo-cc-arch-host-cio-exec-pa-demand-gated-cluster-1080-1085-1089-triage-2026-05-17.md`
- KG service surface: `services/knowledge/knowledge_graph_service.py:21` (class def); `:33` (kg_boundary_enforcer injection); `:39` (create_node)
- Pattern-072 (Proven; typed-catalog shape): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`

## What this memo IS

- **#1016 disposition**: concur (B); boundary-map deliverable deferred until #1089 disposition settles
- **#1089 Q3**: write-path first, service-layer primary gate, repository-layer safety net for bypass defense-in-depth
- **#1089 Q4**: (4a) inside KnowledgeGraphService, extending the existing `kg_boundary_enforcer` pattern; concrete API shape proposed
- **#1089 Q1 read**: supportive of (1b) Lead Dev recommendation

## What this memo is NOT

- Not a PM ratification (Q1 is PM's call)
- Not a CIO methodology call (Q5 is CIO's call)
- Not a HOST trust-property call (Q2 privacy_level semantics is HOST + PM)
- Not gating your Surface 1 build — at your reading cadence
- Not an ADR — that lands after Phase 0 ratification + implementation phase begins (per your memo)

— Architect, 2026-05-17 ~12:10 PT
