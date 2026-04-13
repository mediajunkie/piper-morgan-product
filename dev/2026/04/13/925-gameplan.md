# Gameplan: #925 Phase 3 — STATUS/PRIORITY Floor Migration

## Phase -1: Infrastructure Verification

**Task**: Migrate STATUS and PRIORITY from canonical handlers to floor-first routing with context assembly. Same pattern as IDENTITY (Apr 8) and TEMPORAL (Apr 12).

**Key insight from investigation**: Both already score 9/9 on Colleague Test via the safety net (canonical → generic → floor reroute). This migration eliminates the roundtrip and gives the floor direct access to context.

**Scope**: Phase 3 only. Phase 4 (greeting refactor) deferred per ADR-059.
**Worktree**: SKIP — single agent, sequential.

## Phase 1: TDD — PRIORITY (simpler, do first)

### Tests to write (test_action_gate.py):
1. test_priority_focus_does_not_require_canonical — "What should I focus on?" → floor
2. test_priority_urgent_does_not_require_canonical — "What's urgent?" → floor
3. test_should_route_priority_to_floor — _should_route_to_floor returns True

### Implementation:
- Update _requires_canonical_handler: PRIORITY → return False
- Add PRIORITY to _FLOOR_ROUTED_CATEGORIES (already has TEMPORAL from yesterday)
- Add _gather_priority_context to ContextAssembler:
  - user priorities from user_context_service
  - high-priority GitHub issues (P0/P1/urgent/critical labels) if GitHub configured
  - graceful empty when no data

## Phase 2: TDD — STATUS

### Tests to write (test_action_gate.py):
1. test_status_project_does_not_require_canonical — "What am I working on?" → floor
2. test_status_landscape_does_not_require_canonical — "Show me project landscape" → floor
3. test_should_route_status_to_floor — _should_route_to_floor returns True

### Implementation:
- Update _requires_canonical_handler: STATUS → return False
- Add STATUS to _FLOOR_ROUTED_CATEGORIES
- Add _gather_status_context to ContextAssembler:
  - project list from user_context_service
  - project metadata (GitHub open issues, last activity) if available
  - organization name
  - graceful empty when no data

## Phase 3: Verify

- Restart server
- Run canonical retest Q11-14 (Status) and Q13/Q21 (Priority)
- Verify scores remain ≥7 (baseline is 9/9)
- Full test suite green

## Phase 4: Clean up

- Update ADR-060 migration path: Phase 3 STATUS/PRIORITY = complete
- Update v3 test matrix if routing expectations change
- Note: dead _detect_* methods and format methods left in place for now (cleanup in separate ticket)

## STOP Conditions

- If quality scores drop below 7 after migration → investigate, don't ship
- If context assembly needs GitHub data that requires async session handling → may need service wiring
