# RADAR-PEOPLE-SOURCE — PeopleEntitySource (People as a live Radar entity type)

**Priority**: P1
**Labels**: `ui`, `enhancement`
**Milestone**: MVP
**Epic**: RADAR-ENTITY-SOURCES (umbrella) / #1090
**Related**: #1236 (pattern); `services/radar/sources.py` (contract); **CXO #1217 memo 2026-06-14** (People = typed relationship-network map; PPM-owned entity-model; backs the personhood ethics floor); #1217 (ETHICS-FLOOR-PERSONHOOD); PDR-002 Layer 2; CXO mockup; Lead→PPM memo 2026-06-14 (entity-backends sequencing).

---

## Problem Statement

### Current State
Radar (#1236) renders Conversations only. **People** is a PDR-002 Layer-2 type and must surface for beta. Unlike Document/WorkItem, **no backend exists at all** — and per CXO #1217, the People entity is not a thin "contacts list" but a **typed relationship-network map** (human / agent / stakeholder, with relationship edges) that PM elevated into an inherent capability, and which **also backs the #1217 personhood ethics floor** (the type field is the signal the floor reads). The entity-model is **PPM's lane**.

### Impact
- **Blocks**: 1 of 4 beta Radar types — and the one with the deepest product meaning (the relationship network is "who Piper knows in your world").
- **User Impact**: users can't see the people/agents Piper has learned about; the ask-once-learn-the-answer capability (#1217) has nowhere to surface.
- **Technical Debt**: this is the long pole — no backend + cross-lane (PPM model, CXO surfacing, Lead wrap + the ethics-floor dependency).

### Strategic Context
This is double-duty infrastructure: the People entity-model serves Radar surfacing **and** the #1217 ethics floor. It's the riskiest of the four to ship for beta and needs the earliest cross-lane sequencing.

---

## Goal

**Primary Objective**: A `PeopleEntitySource` that lists the user's known people/agents (from PPM's People entity-model) and maps them to `RadarEntity` (type=People, personhood-type in meta, honest provenance), wired into `_build_feed`.

**Example User Experience**:
```
Before: the people and agents Piper has learned about exist nowhere a user can see.
After:  People cards surface in Radar — each tagged human / agent / stakeholder —
        showing "who Piper knows in your world," reading the same typed map the
        #1217 ethics floor consults (one store, not two).
```

**Not In Scope**:
- ❌ The **People entity-model backend** itself (the typed relationship-network store) — **PPM's lane** (PPM to confirm/carve; this issue *consumes* it).
- ❌ The #1217 **ethics-floor classifier** logic (PA/HOST lane) — this issue surfaces the same entity, doesn't implement the floor.
- ❌ Relationship-graph **visualization** (future; this is the Radar card facet).

---

## What Already Exists

### Infrastructure
- `services/radar/sources.py` — `EntitySource` contract + `ConversationEntitySource` pattern.
- CXO #1217 memo — the People entity design intent (typed map + edges).

### What's Missing
- ❌ **People entity-model backend** — typed (human/agent/stakeholder) relationship-network store. **PPM-owned; not yet built/tracked** (the gating dependency).
- ❌ `PeopleEntitySource`.
- ❌ Registration in `_build_feed`.

---

## Requirements

### Phase 0: Cross-lane dependency + contract
- [ ] Confirm the People entity-model backend is tracked + owned (PPM); align its read shape to the `EntitySource`/`RadarEntity` contract (so the wrap is thin).
- [ ] Map People fields → `RadarEntity` (name → title; personhood-type human/agent/stakeholder → meta; relationship recency/strength → attention; person id → ref; lifecycle = ?, define with CXO/PPM).

### Phase 1: EntitySource wrap (TDD) — gated on the backend
- [ ] `PeopleEntitySource(people_model)` → `fetch(user_id) -> list[RadarEntity]` (type=People); tests mock the model layer.

### Phase 2: Wiring (TDD)
- [ ] Register in `_build_feed`; multi-source compose test (People renders attention-first with the others).

### Phase Z: Completion & Handoff
- [ ] AC met + evidence; CXO conformance; coherence-check with the #1217 floor (same entity, one store); session log + close-properly; umbrella matrix updated.

---

## Acceptance Criteria

### Functionality
- [ ] `PeopleEntitySource.fetch(user_id)` returns the user's known people/agents as `RadarEntity` (type=People).
- [ ] Personhood-type (human/agent/stakeholder) surfaced in the card meta.
- [ ] Renders attention-first alongside other types.
- [ ] Honest provenance: only `● observed` (people Piper actually learned about); never seed/fabricated.

### Testing
- [ ] TDD; mock only the People entity-model layer.
- [ ] No regression to other sources / `?radar=1` fallback.

### Quality
- [ ] One store, not two: reads the same People entity-model the #1217 floor uses (coherence — no parallel contacts system).
- [ ] Failing/empty source never blanks Radar.

### Documentation
- [ ] AC cites PDR-002 Layer 2 + the CXO mockup + the #1217 coherence (People entity = floor's signal source).
- [ ] Session log + umbrella matrix updated.

---

## Completion Matrix
| Component | Status | Owner | Evidence |
|---|---|---|---|
| People entity-model backend | ❌ | **PPM** | (dependency) |
| `PeopleEntitySource` | ❌ | Lead | |
| `_build_feed` registration | ❌ | Lead | |
| Tests | ❌ | Lead | |

---

## Testing Strategy
**Unit**: People→`RadarEntity` mapping (type, personhood-type in meta, observed provenance); compose test. **Manual**: `?radar=1` shows People cards once the entity-model lands + Piper has learned people.

---

## Effort Estimate
**Overall Size**: Medium (the wrap is small; the gating dependency is large + cross-lane). Phase 0 (M, cross-lane) · Phase 1 (S) · Phase 2 (S). **Complexity**: highest of the three — no backend yet, three lanes, and the ethics-floor coherence constraint.

---

## Dependencies
### Required (Must be complete first)
- [ ] **People entity-model backend (PPM)** — typed relationship-network store. The gate. (Lead→PPM memo 6/14; PPM to confirm/carve.)
- [ ] #1236 EntitySource seam (done).
### Optional
- [ ] CXO conformance pass on the People card; HOST read on the typed-map trust implications.

---

## Success Metrics
### Quantitative
- All People entities in the model render with correct personhood-type; **one store** (no parallel contacts system); new module carries unit-test coverage.
### Qualitative
- The relationship network ("who Piper knows in your world") is visible and **coherent with the #1217 floor** (same typed map).

## STOP Conditions
**STOP and escalate if**: infrastructure doesn't match assumptions; any test fails (don't rationalize); performance degrades; a security/privacy/trust concern surfaces (a typed map of humans + agents is sensitive — loop HOST); the pattern already exists elsewhere; user data at risk; completion bias; can't provide evidence. **People-specific**: do **not** build a standalone "contacts" backend to unblock this — it must read the one People entity-model PPM owns (coherence with #1217). If that model isn't ready, STOP and sequence; don't fork a parallel store.

## Related Documentation
- **Architecture**: PDR-002 Layer 2 (People is one of the four); `services/radar/` DDD (`EntitySource` contract); #1217 (ethics-floor personhood — the coherence constraint).
- **Methodology**: audit-cascade (Pattern-049); close-issue-properly.
- **Strategic**: CXO mockup; CXO #1217 memo 2026-06-14 (People = relationship-network map); Lead→PPM memo 2026-06-14; RADAR-ENTITY-SOURCES umbrella.

## Notes for Implementation
This is the cross-lane long pole. The wrap is thin; the gate is PPM's entity-model. Coordinate the read shape early (Phase 0) so the wrap stays thin. Coherence with #1217 is load-bearing — one store. PM/architect may add guidance here.

## Evidence Section
_(filled during/after implementation — commits, test output, render evidence.)_

## Completion Checklist
**Status**: Drafted / pending PM authorization to create.

_Issue drafted: 2026-06-14 (Lead Dev) — pending PM authorization to create._
