# RADAR-DOC-SOURCE — DocumentEntitySource (Document as a live Radar entity type)

**Priority**: P1
**Labels**: `ui`, `enhancement`
**Milestone**: MVP
**Epic**: RADAR-ENTITY-SOURCES (umbrella) / #1090
**Related**: #1236 (surface + ConversationEntitySource pattern to mirror); `services/radar/sources.py` (`EntitySource` contract); `services/knowledge_graph/document_service.py` (`DocumentService`); #712/#713 (MUX document viewer/lifecycle UI); PDR-002 Layer 2; CXO mockup (binding spec).

---

## Problem Statement

### Current State
Radar (#1236) renders Conversations only. **Document** is one of the four PDR-002 Layer-2 entity types and must surface for beta (umbrella: no partial ship). `DocumentService` exists but its public surface is `get_relevant_context(timeframe)` — there is **no per-user document list** to feed an `EntitySource`.

### Impact
- **Blocks**: 1 of the 4 entity types the beta Radar must surface.
- **User Impact**: users can't see their documents' state (e.g., recently-added, processed, stale) at a glance in Radar.
- **Technical Debt**: none introduced; this adds a thin read path on an existing service.

### Strategic Context
First of the three remaining EntitySources (the unblocked one — no cross-lane dependency), so it's the natural next build after #1236.

---

## Goal

**Primary Objective**: A `DocumentEntitySource` that lists the user's documents and maps them to `RadarEntity` objects (type=Document, honest provenance, a lifecycle badge), wired into Radar's `_build_feed` so Documents render alongside Conversations.

**Example User Experience**:
```
Before: a user with a dozen uploaded documents sees none of them in Radar.
After:  their recently-touched / processing documents appear as Document cards
        (title · lifecycle badge · ● observed), interleaved attention-first with
        their conversations.
```

**Not In Scope**:
- ❌ The document **viewer/lifecycle UI** (#712/#713 — separate).
- ❌ Net-new document storage — wrap the existing `DocumentService`.
- ❌ Document **search** UI beyond contributing Documents to the existing entity-search facet.

---

## What Already Exists

### Infrastructure
- `services/knowledge_graph/document_service.py` — `DocumentService` (+ `get_document_service()` factory).
- `services/radar/sources.py` — `EntitySource` protocol + `ConversationEntitySource` (the mapping pattern to mirror).
- `web/api/routes/radar.py` — `_build_feed()` (where the new source registers).

### What's Missing
- ❌ A per-user document list method on `DocumentService` (e.g., `list_for_user(user_id)` returning id/title/timestamps/state).
- ❌ `DocumentEntitySource`.
- ❌ Registration in `_build_feed`.

---

## Requirements

### Phase 0: Contract verification
- [ ] Read `DocumentService` fully: confirm the underlying store, whether documents are user-scoped, and what fields exist (title, created/updated, processing/lifecycle status, owner).
- [ ] Confirm the `RadarEntity` facet mapping (what becomes `lifecycle_state`, `meta`, `attention`, `ref`).

### Phase 1: Backend read path (TDD)
- [ ] Add a per-user list method to `DocumentService` (returns the fields a Document entity needs); tests first.
- [ ] Honest provenance: real documents = `observed`; never fabricate counts/state.

### Phase 2: EntitySource + wiring (TDD)
- [ ] `DocumentEntitySource(document_service)` implementing `fetch(user_id) -> list[RadarEntity]` (type=Document); tests mirror `test_radar_domain` / `test_radar` patterns.
- [ ] Register in `_build_feed`; multi-source test (Conversation + Document compose, attention-first).

### Phase Z: Completion & Handoff
- [ ] AC met + evidence; session log + close-properly; umbrella matrix updated.

---

## Acceptance Criteria

### Functionality
- [ ] `DocumentEntitySource.fetch(user_id)` returns the user's documents as `RadarEntity` (type=Document).
- [ ] Documents render in Radar alongside Conversations, attention-first (mixed, not grouped).
- [ ] Each Document card shows a lifecycle badge derived from real document state.
- [ ] Honest provenance: only `● observed` documents in default; no seed/example as observed.

### Testing
- [ ] TDD: tests-first for the list method + the EntitySource mapping + the multi-source compose.
- [ ] No regression to the Conversation path or `?radar=1` fallback.

### Quality
- [ ] A failing/empty document source never blanks Radar (per-source isolation).
- [ ] Lifecycle/`meta` derived from real data only (no fabrication).

### Documentation
- [ ] AC cites PDR-002 Layer 2 + the CXO mockup.
- [ ] Session log + umbrella matrix updated.

---

## Completion Matrix
| Component | Status | Evidence |
|---|---|---|
| `DocumentService` per-user list | ❌ | |
| `DocumentEntitySource` | ❌ | |
| `_build_feed` registration | ❌ | |
| Tests (list + source + compose) | ❌ | |

---

## Testing Strategy
**Unit**: list method (user scoping, fields); `DocumentEntitySource` mapping (Document type, lifecycle derivation, observed provenance); `_build_feed` compose (Conversation + Document, attention-first). **Manual**: `?radar=1` shows Document cards for a user with documents; empty for one without.

---

## Effort Estimate
**Overall Size**: Small. Phase 0 (S) · Phase 1 (S) · Phase 2 (S). **Complexity**: low — the only unknown is whether `DocumentService`'s store is cleanly user-scoped (Phase 0 resolves it).

---

## Dependencies
### Required
- [ ] `DocumentService` operational (it is).
- [ ] #1236 EntitySource seam (done).
### Optional
- [ ] CXO conformance pass on the Document card.

---

## Success Metrics
### Quantitative
- 100% of a user's listable documents render as Document cards; new module carries unit-test coverage; negligible added `_build_feed` latency.
### Qualitative
- Document state (recent / processing / stale) is legible at a glance in Radar.

## STOP Conditions
**STOP and escalate if**: infrastructure doesn't match assumptions; any test fails (don't rationalize); performance degrades; a security/privacy concern surfaces (esp. cross-user document leakage); the pattern already exists elsewhere; user data at risk; completion bias (claiming render without live evidence); can't provide evidence. **Document-specific**: if `DocumentService`'s store turns out **not** user-scoped (documents are global/shared), STOP and escalate — user-scoping may be a larger change than this issue assumes.

## Related Documentation
- **Architecture**: PDR-002 Layer 2; `services/radar/` DDD (`EntitySource` contract); `DocumentService` (`services/knowledge_graph/document_service.py`).
- **Methodology**: audit-cascade (Pattern-049); close-issue-properly; the UI-fix render-test discipline.
- **Strategic**: CXO mockup; #712/#713 (MUX document UI); RADAR-ENTITY-SOURCES umbrella.

## Notes for Implementation
Mirror `ConversationEntitySource` exactly (the proven pattern). The only real unknown is Phase 0 (is `DocumentService`'s store user-scoped?). PM/architect may add guidance here.

## Evidence Section
_(filled during/after implementation — commits, test output, render evidence.)_

## Completion Checklist
**Status**: Drafted / pending PM authorization to create.

_Issue drafted: 2026-06-14 (Lead Dev) — pending PM authorization to create._
