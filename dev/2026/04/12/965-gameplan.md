# Gameplan: #965 — Temporal Handlers Floor Migration

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Temporal routing: ALL TEMPORAL → canonical (intent_service.py:9886-9888)
- [x] Temporal handlers: 5 sub-handlers in canonical_handlers.py (lines 823-922)
- [x] Context assembler: NO temporal branch — falls through to empty (context_assembler.py:59-61)

**Task**: Migrate Q7-Q10 temporal queries from canonical handlers to floor routing with context assembly. Keep Q6 ("What day is it?") canonical.

**Current state**:
- `_requires_canonical_handler` returns True for ALL TEMPORAL (line 9888)
- `_handle_temporal_query` dispatches to 5 sub-methods based on pattern detection
- `ContextAssembler` has no TEMPORAL branch — returns only `current_time`
- 68 existing temporal tests in test_canonical_handlers.py
- Pre-classifier has extensive TEMPORAL_PATTERNS (lines 142-191+)

### Part A.2: Worktree Assessment

- [x] Single agent, sequential work
- [x] Tightly coupled files requiring atomic commits
- **SKIP WORKTREE** — single agent, ~5 files, sequential

### Part C: PROCEED

---

## Phase 0: Investigation (DONE — subagent research)

Key finding: The 4 failing temporal handlers (agenda, retrospective, last_activity, duration) each gather real data internally — but they format it as template-quality text. The canonical handler approach means the LLM never gets to compose a contextual response. Floor routing with context assembly would let the LLM use the same data sources but compose naturally.

Q6 ("What day is it?") is deterministic — system clock + time zone. No LLM needed. Keep canonical.

---

## Phase 0.5: Frontend-Backend Contract

Not applicable — no new endpoints or frontend changes.

---

## Phase 0.6: Data Flow

Current flow (canonical):
```
User message → Pre-classifier (TEMPORAL) → Action Gate (requires canonical=True)
  → canonical_handlers._handle_temporal_query → sub-handler → template response
```

Target flow (floor for Q7-Q10):
```
User message → Pre-classifier (TEMPORAL) → Action Gate (requires canonical=False for non-date)
  → _should_route_to_floor (TEMPORAL in floor categories)
  → _handle_floor_with_context → ContextAssembler.gather_context(TEMPORAL)
  → ConversationalFloor.respond() → LLM-generated response with temporal data
```

Target flow (canonical for Q6):
```
User message → Pre-classifier (TEMPORAL) → Action Gate (requires canonical=True for date/time)
  → canonical_handlers._handle_temporal_query → base date handler → formatted date
```

---

## Phase 1: TDD — Write Tests First

**Files**: `tests/unit/services/intent_service/test_action_gate.py`

### Tests to write BEFORE implementation:

1. **test_temporal_date_requires_canonical**: TEMPORAL with action "get_current_time" or "provide_date" → requires canonical = True
2. **test_temporal_agenda_does_not_require_canonical**: TEMPORAL with action "provide_agenda" → requires canonical = False
3. **test_temporal_retrospective_does_not_require_canonical**: TEMPORAL with action "provide_retrospective" → requires canonical = False
4. **test_temporal_last_activity_does_not_require_canonical**: TEMPORAL with action "provide_last_activity" → requires canonical = False
5. **test_temporal_duration_does_not_require_canonical**: TEMPORAL with action "provide_project_duration" → requires canonical = False
6. **test_should_route_temporal_non_date_to_floor**: TEMPORAL non-date → _should_route_to_floor = True

### Acceptance Criteria:
- [ ] All 6 tests written and failing (red)
- [ ] Tests follow existing action gate test patterns

---

## Phase 2: Route TEMPORAL Non-Date to Floor

**Files**: `services/intent/intent_service.py`

### Changes:

1. Update `_requires_canonical_handler()` (line 9886-9888):
   ```python
   if category == "TEMPORAL":
       # Q6: pure date/time query stays canonical (deterministic, sub-ms)
       action = (intent.action or "").lower()
       if action in ("get_current_time", "provide_date", "get_date"):
           return True
       # Q7-Q10: conversational temporal queries → floor with context
       return False
   ```

2. Add TEMPORAL to `_FLOOR_ROUTED_CATEGORIES` in `_should_route_to_floor()` (line 9943) — it's already there if it's listed in the set; verify.

### Acceptance Criteria:
- [ ] Phase 1 TDD tests turn green
- [ ] Q6 still routes to canonical
- [ ] Q7-Q10 route to floor

---

## Phase 3: Context Assembly for TEMPORAL

**Files**: `services/intent_service/context_assembler.py`

### Changes:

1. Add TEMPORAL branch to `gather_context()`:
   ```python
   elif category == "TEMPORAL":
       ctx = await self._gather_temporal_context(user_id, session_id)
       context.update(ctx)
   ```

2. New `_gather_temporal_context()` method:
   - `current_time` (already present in base context)
   - `current_date` with day of week
   - `calendar_summary` (today's events if calendar configured)
   - `pending_todos` (user's active todo list)
   - `completed_todos_yesterday` (for retrospective queries)
   - `project_metadata` (names, created dates — for duration queries)

   All data retrieval should be fail-graceful (empty dict on error, not throw).

### Acceptance Criteria:
- [ ] `gather_context("TEMPORAL", user_id, session_id)` returns structured data
- [ ] Each data source fails gracefully when unavailable (fresh account scenario)
- [ ] Unit test for `_gather_temporal_context` with mocked data sources

---

## Phase 4: Verify + Clean Up

1. **Run canonical retest Q7-Q10**: all must score 7+ on Colleague Test
2. **Update v3 matrix**: TEMPORAL Q7-Q10 expected routing = "floor"
3. **Clean up dead canonical handler tests**: any temporal tests that test dead code paths (the sub-handlers for agenda/retrospective/etc. that are no longer reached in production)
4. **Full test suite**: must pass (6250+)

### Acceptance Criteria:
- [ ] Canonical retest Q7-Q10 all PASS (Colleague Test 7+)
- [ ] No dead tests remain
- [ ] Full suite green

---

## Phase Z: Final Verification

- [ ] ADR-060 Migration Path updated (Phase 3 TEMPORAL = complete)
- [ ] Session log updated with evidence
- [ ] #965 ready for PM closure

---

## STOP Conditions

- If pre-classifier TEMPORAL patterns don't distinguish date queries from conversational ones → need pattern-level changes first
- If ContextAssembler can't access todo/project data → may need service wiring work
- If Q6 breaks during migration → STOP, the date handler must stay canonical
