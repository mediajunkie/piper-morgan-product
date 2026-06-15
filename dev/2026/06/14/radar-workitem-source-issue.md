# RADAR-WORKITEM-SOURCE — WorkItemEntitySource (Work items as a live Radar entity type)

**Priority**: P1
**Labels**: `ui`, `enhancement`
**Milestone**: MVP
**Epic**: RADAR-ENTITY-SOURCES (umbrella) / #1090
**Related**: #1236 (pattern); `services/radar/sources.py` (contract); `services/integrations/github/github_integration_router.py:237` (`list_issues`); `services/mcp/consumer/github_adapter.py:857` (`list_issues_via_mcp`); **#1233 (RECONNECT-WS9 identity — the gating dependency)**; #716 (MUX features-view, Fast Follow); PDR-002 Layer 2; CXO mockup.

---

## Problem Statement

### Current State
Radar (#1236) renders Conversations only. **WorkItem** is a PDR-002 Layer-2 type and must surface for beta. GitHub issues are listable — `list_issues(repository, **kwargs)` — but **repo-scoped, not user-scoped**: there's no clean "this user's work items" path because the user→repo/connector-identity mapping is still being built in RECONNECT-WS9 (#1233).

### Impact
- **Blocks**: 1 of 4 beta Radar types. The "what work is on my plate / in-review / blocked" story — arguably the most PM-resonant Radar facet.
- **User Impact**: users can't see their work items' state at a glance until this lands.
- **Technical Debt**: depends on the identity work (#1233); building user-scoping here before #1233 would duplicate/pre-empt it.

### Strategic Context
The work-item facet is high-value for a PM tool, but it's **identity-gated** — honest sequencing puts it after (or alongside) #1233.

---

## Goal

**Primary Objective**: A `WorkItemEntitySource` that lists the user's work items (GitHub issues for their connected repo(s), via the #1233 identity mapping) and maps them to `RadarEntity` (type=WorkItem, lifecycle from issue state, honest provenance), wired into `_build_feed`.

**Example User Experience**:
```
Before: a user's open issues are invisible in Radar.
After:  once their identity resolves to a connected repo (#1233), their work items
        appear as WorkItem cards with a state badge (open / in-review / blocked),
        attention-first — "what's on my plate" answerable from Radar.
```

**Not In Scope**:
- ❌ The MUX **features-view** (#716, Fast Follow).
- ❌ Building the identity mapping itself — that's #1233; this **consumes** it.
- ❌ Non-GitHub work-item sources (future).

---

## What Already Exists

### Infrastructure
- `services/integrations/github/github_integration_router.py:237` — `list_issues(repository, **kwargs)`; `:675` `get_issues_by_priority()`.
- `services/mcp/consumer/github_adapter.py:857` — `list_issues_via_mcp(...)`.
- `services/radar/sources.py` — `EntitySource` contract + `ConversationEntitySource` pattern.

### What's Missing
- ❌ User→repo(s) resolution (the per-user scope) — **#1233**.
- ❌ `WorkItemEntitySource`.
- ❌ Registration in `_build_feed`.

---

## Requirements

### Phase 0: Dependency + contract verification
- [ ] Confirm #1233 provides a user→connected-repo(s) resolution this source can call; if not yet, define the seam + STOP for sequencing.
- [ ] Map GitHub issue fields → `RadarEntity` (state open/closed → lifecycle; labels/assignee → meta; updated_at → attention; url/number → ref).

### Phase 1: User-scoped listing (TDD)
- [ ] Resolve the user's repo(s) via #1233; list their issues (assigned/authored, per the mockup's "work" definition); tests first (mock the identity + github layers — wiring-test discipline).

### Phase 2: EntitySource + wiring (TDD)
- [ ] `WorkItemEntitySource(...)` → `fetch(user_id) -> list[RadarEntity]` (type=WorkItem); register in `_build_feed`; multi-source compose test.

### Phase Z: Completion & Handoff
- [ ] AC met + evidence; session log + close-properly; umbrella matrix updated.

---

## Acceptance Criteria

### Functionality
- [ ] `WorkItemEntitySource.fetch(user_id)` returns the user's work items as `RadarEntity` (type=WorkItem).
- [ ] Lifecycle badge derived from real issue state (open/in-review/blocked/closed per available signals).
- [ ] Renders attention-first alongside other types.
- [ ] Honest provenance: only `● observed` real items; no fabrication.

### Testing
- [ ] TDD; mock only the identity + GitHub layers (don't mock internals — #490 lesson).
- [ ] No regression to other sources / `?radar=1` fallback.

### Quality
- [ ] Failing/empty source never blanks Radar.
- [ ] No duplication of #1233's identity logic — consume it.

### Documentation
- [ ] AC cites PDR-002 Layer 2 + the CXO mockup; session log + umbrella matrix updated.

---

## Completion Matrix
| Component | Status | Evidence |
|---|---|---|
| User→repo resolution (via #1233) | ❌ | |
| `WorkItemEntitySource` | ❌ | |
| `_build_feed` registration | ❌ | |
| Tests | ❌ | |

---

## Testing Strategy
**Unit**: field mapping (issue state → lifecycle); EntitySource (WorkItem type, observed provenance); compose test. **Manual**: `?radar=1` shows the user's work items once #1233 identity resolves.

---

## Effort Estimate
**Overall Size**: Medium. Gated on #1233. Phase 0 (S) · Phase 1 (M, identity-dependent) · Phase 2 (S). **Complexity**: the user-scoping is the unknown; bounded by #1233's shape.

---

## Dependencies
### Required (Must be complete first)
- [ ] **#1233** — RECONNECT-WS9 identity (user→connector/repo mapping). **This is the gate.**
- [ ] #1236 EntitySource seam (done).
### Optional
- [ ] CXO conformance pass on the WorkItem card.

---

## Success Metrics
### Quantitative
- A user's open/assigned issues for their connected repo all render; correct issue-state→lifecycle mapping; new module carries unit-test coverage.
### Qualitative
- "What work is on my plate / in-review / blocked" is answerable from Radar at a glance.

## STOP Conditions
**STOP and escalate if**: infrastructure doesn't match assumptions; any test fails (don't rationalize); performance degrades; a security/privacy concern surfaces (esp. surfacing another user's issues); the pattern already exists elsewhere; user data at risk; completion bias; can't provide evidence. **WorkItem-specific**: if #1233 isn't far enough along to provide user→repo resolution, STOP and sequence with PM/PPM rather than building a throwaway user-scoping shim.

## Related Documentation
- **Architecture**: PDR-002 Layer 2; `services/radar/` DDD (`EntitySource` contract); GitHub integration (`services/integrations/github/`, `services/mcp/consumer/github_adapter.py`).
- **Methodology**: audit-cascade (Pattern-049); close-issue-properly; the #490 wiring-test discipline.
- **Strategic**: CXO mockup; #1233 (RECONNECT-WS9 identity — the gate); #716 (MUX features-view, Fast Follow); RADAR-ENTITY-SOURCES umbrella.

## Notes for Implementation
Consume #1233's identity mapping — do not duplicate or pre-empt it. Mirror `ConversationEntitySource`. PM/architect may add guidance here.

## Evidence Section
_(filled during/after implementation — commits, test output, render evidence.)_

## Completion Checklist
**Status**: Drafted / pending PM authorization to create.

_Issue drafted: 2026-06-14 (Lead Dev) — pending PM authorization to create._
