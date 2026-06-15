# RADAR-ENTITY-SOURCES — all four Layer-2 EntitySources for beta (no partial ship)

**Priority**: P1
**Labels**: `ui`, `enhancement`, `epic`
**Milestone**: MVP
**Epic**: #1090 (UI-1.0-PLAN)
**Related**: #1236 (Radar surface + ConversationEntitySource — the proven pattern); PDR-002 Layer 2 (the 4-type entity model); CXO mockup `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` (binding spec); CXO #1217 memo 2026-06-14 (People = relationship-network map, PPM-owned, backs the ethics floor); #1233 (RECONNECT-WS9 identity — WorkItem dependency); #1214/#1216 (honest provenance); ~~#706~~ (CLOSED discovery epic — *not* the impl; the miscited referent this umbrella corrects).

---

## Problem Statement

### Current State
The Radar surface (#1236) is live in the history slot and renders **one** of the four PDR-002 Layer-2 entity types — **Conversation**. The other three — **WorkItem, Document, People** — have **no `EntitySource` implementation**, and (3 of 4) **no queryable per-user backend** behind them. #1236 deferred them as "richer types later, non-blocking, gated on #706" — but **#706 is closed** (a *design* discovery epic, not the backend impl), so the deferral pointed at a referent that doesn't deliver the work.

### Impact
- **Blocks**: a beta-credible Radar. PM directive (2026-06-14): *"there is no partial ship. we are in alpha headed for beta. we need to ship it all."* A Radar that surfaces only chats while the empty-state copy promises "issues, docs, people, chats" is a soft over-claim, not a beta surface.
- **User Impact**: the collaborator product story (entities + their state, not just a chat list) is the whole point of Radar; one of four types doesn't deliver it.
- **Technical Debt**: without a single tracker tying "Radar ships when all four EntitySources exist," the surface workstream (Lead) and the entity-model workstream (PPM/CXO) drift — which is exactly how this gap formed.

### Strategic Context
PM-ratified consolidate-on-Radar (6/13) + attention-first + two-states (6/14), now with the **no-partial-ship beta bar** (6/14). This umbrella is the durable home for the full four-type requirement + the integration that ties the per-source work to the surface.

---

## Goal

**Primary Objective**: All **four** PDR-002 Layer-2 EntitySources (Conversation, Document, WorkItem, People) render live in the Radar surface for the 0.9 beta — attention-first across types, honest provenance (`● observed` only in default), entity-search spanning types.

**Example User Experience**:
```
Before: the Radar sidebar shows only recent chats — a Layer-1 duplicate of the chat-nav.
After:  Radar shows, in one attention-first feed, the documents you touched this week,
        the work items on your plate (open / in-review / blocked), the people and agents
        Piper has learned you work with, and your active conversations — each with a
        lifecycle badge and an honest ● observed marker. "What is Piper keeping an eye on
        for me?" is answerable at a glance, across types, not just chats.
```

**Not In Scope** (explicitly):
- ❌ The Radar **surface/render** itself — done in #1236 (this umbrella consumes it).
- ❌ The design-floor #1169–1173 (separate D1 issues).
- ❌ Re-architecting the `EntitySource` protocol — it exists (`services/radar/sources.py`) and is the integration contract; this work *implements against* it.

---

## What Already Exists

### Infrastructure
- **The surface** (#1236): `templates/components/history_sidebar.html` Radar render + `home.html` `?radar=1`; `web/api/routes/radar.py` GET `/api/v1/radar`; `_build_feed()` — **the composition seam where additional sources slot in**.
- **The contract**: `services/radar/sources.py` `EntitySource` protocol — `async fetch(user_id) -> list[RadarEntity]`; `RadarEntity` facets = `entity_type, title, lifecycle_state, provenance, meta, attention, ref`. `ConversationEntitySource` is the reference implementation.
- **Conversation backend** ✅: `UserHistoryService.get_history(user_id,…)` (#1021).

### What's Missing
- ❌ **DocumentEntitySource** — `DocumentService` exists (`services/knowledge_graph/document_service.py`) but has **no per-user list method** (small add). → child issue.
- ❌ **WorkItemEntitySource** — GitHub `list_issues(repository,…)` is **repo-scoped, not user-scoped** → needs identity mapping (#1233). → child issue.
- ❌ **PeopleEntitySource** + its backend — **no people/relationship backend exists**; the People entity-model (typed human/agent/stakeholder map + edges) is **PPM's lane** (memo sent 6/14; CXO #1217). → child issue (Lead wrap) + PPM entity-model (PPM to confirm/carve).

---

## Requirements

### Phase 0: Tracking + contract freeze
- [ ] This umbrella created as the durable home (closes the integration-tracking gap).
- [ ] Freeze the `EntitySource` / `RadarEntity` facet contract with PPM (~20 min) so Document/WorkItem/People models land Radar-consumable.
- [ ] Confirm with PPM where the **People entity-model backend** is tracked; if untracked, PPM carves it (their lane).

### Phase 1: DocumentEntitySource (Lead — unblocked)
- [ ] Child issue: add `DocumentService.list_for_user(user_id)` + `DocumentEntitySource` + wire into `_build_feed` + tests.

### Phase 2: WorkItemEntitySource (Lead — gated on #1233 identity)
- [ ] Child issue: user-scoped work-item listing + `WorkItemEntitySource` + wire + tests.

### Phase 3: PeopleEntitySource (Lead wrap — gated on PPM entity-model)
- [ ] Child issue: `PeopleEntitySource` wrapping PPM's People entity-model + wire + tests.

### Phase Z: Completion & Handoff
- [ ] All four types render live with honest provenance; #1236 closure gate (PDR-002 + mockup) re-satisfied with all four.
- [ ] CXO conformance review; session log + close-properly.

---

## Acceptance Criteria

### Functionality
- [ ] All four EntitySources (Conversation ✅, Document, WorkItem, People) return live entities.
- [ ] Radar renders all four types, **attention-first across types** (not type-grouped).
- [ ] **Entity-search spans all four types** (subsumes chat-search).
- [ ] **Honest provenance** maintained across all types: only `● observed` real entities in default; no seed/dev rendered as observed (#1214/#1216).
- [ ] Each type carries a correct `lifecycle_state` badge per the mockup.

### Testing
- [ ] Each EntitySource has unit tests (TDD); the `_build_feed` composition has a multi-source test.
- [ ] No regression to #1236 (Conversation path + the `?radar=1` flag + graceful fallback).

### Quality
- [ ] Honest-degradation: a failing/empty source never blanks the surface (per-source isolation).
- [ ] Part-B token-conformant (CXO review).

### Documentation
- [ ] AC cites **PDR-002 Layer 2 + the CXO mockup** (closure gate).
- [ ] This umbrella + children reflect final state; session log complete.

---

## Completion Matrix
| EntitySource | Backend status | Owner | Status |
|---|---|---|---|
| Conversation | ✅ exists (#1021) | Lead | ✅ done (#1236) |
| Document | ⚠️ add per-user list | Lead | ❌ child issue |
| WorkItem | ⚠️ needs identity (#1233) | Lead | ❌ child issue |
| People (source) | ❌ wrap PPM model | Lead | ❌ child issue |
| People (entity-model backend) | ❌ no backend | **PPM** | ❌ PPM to confirm/carve |

---

## Dependencies

### Required (Must be complete first)
- [ ] #1233 — RECONNECT-WS9 identity (user→connector mapping) — for WorkItem user-scoping
- [ ] PPM People entity-model backend (memo sent 6/14; PPM to confirm tracking) — for People

### Optional
- [ ] CXO conformance pass on each new card type as it lands

---

## Effort Estimate
**Overall Size**: Large (3 child builds + 1 cross-lane backend dependency)
- Document source: Small
- WorkItem source: Medium (identity-gated)
- People source: Medium (model-gated, cross-lane)

**Complexity Notes**: 2 of 3 remaining have hard cross-lane dependencies (#1233 identity, PPM entity-model). This is a sequenced multi-lane effort, not a single build.

---

## Testing Strategy
- **Unit**: each EntitySource has its own tests (mapping + provenance + lifecycle); the `EntitySource` contract is honored by each.
- **Integration**: `_build_feed` composes all four sources — a multi-source test asserts attention-first ordering across types + per-source isolation (one failing source doesn't blank the feed).
- **Manual**: `?radar=1` on a populated account shows all four card types, mixed attention-first, all `● observed`; on an empty account shows the explainer + one `○ example`.

## Success Metrics
### Quantitative
- All 4 entity types return live entities for a populated account; **0** seed/example cards render as `● observed` in default.
- Composed-feed assembly stays within latency budget (target <300ms p50 for `_build_feed`).
- New per-source modules carry unit-test coverage (TDD).
### Qualitative
- A user can answer "what is Piper keeping an eye on for me?" at a glance, across types — the collaborator story, not a chat list.

## STOP Conditions
**STOP and escalate if**: infrastructure doesn't match assumptions (a backend isn't shaped as recon assumed); any test fails (don't rationalize); performance degrades unacceptably; a security/privacy concern surfaces (esp. cross-user entity leakage); a pattern already exists elsewhere; user data at risk; completion bias (claiming a type "renders" without live evidence); can't provide verification evidence. **Umbrella-specific**: do not fake "all four ship" by rendering empty/seed sources as if observed — an empty source shows nothing, honestly.

## Related Documentation
- **Architecture**: PDR-002 (Layer-2 entity model — the 4 types); `services/radar/` DDD (`EntitySource`/`RadarEntity`/`RadarFeed`).
- **Methodology**: audit-cascade (Pattern-049) — this umbrella is itself an audit-cascade artifact; close-issue-properly for each child.
- **Strategic**: CXO mockup (binding spec); #1090 UI-1.0 plan; CXO #1217 memo (People entity); Lead→PPM memo 2026-06-14 (entity-backends sequencing).

## Notes for Implementation
See the **Methodology note** below for why this umbrella exists (the dependency-completeness audit miss). Sequencing is honest-and-gated: Document (unblocked) → WorkItem (gated on #1233) → People (gated on PPM entity-model). PM/architect may add guidance here.

## Evidence Section
_(filled during/after implementation — per-source commits, test outputs, the all-four-live render.)_

## Completion Checklist
**Status**: Drafted / pending PM authorization to create. (Becomes In Progress → Ready for Review → Complete as children land.)

---

## Methodology note — why this umbrella exists (the audit-cascade learning)

The initial audit-cascade on #1236 (issue + gameplan gates) verified **template conformance** but missed the **dependency-completeness dimension**: it accepted "richer types later, gated on #706" without (a) verifying #706 was a real *open* dependency (it was closed, and a discovery epic), or (b) confirming the deferred scope had a durable tracked home + a realistic backend path. The gameplan's Phase-0.5/0.6 integration-verification was scoped to the *conversation path being built*, not to the *full four-type capability the issue claimed*.

**The fix (proposed for the audit-cascade skill)**: add a **referent-verification / dependency-completeness check** to every issue/gameplan audit — for each capability or entity the artifact claims, trace it to a *concrete, existing, verified* backend referent; a deferred dependency must cite an *open* tracked issue, not a closed/absent one. This is the investigate-before-extending discipline applied to product scope. (Stacks with the "minimal deliverable needs a durably-tracked fleshing-out plan" lesson.)

---

_Issue drafted: 2026-06-14 (Lead Dev) — pending PM authorization to create on the board._
