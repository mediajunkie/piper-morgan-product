# Gameplan: #951 — Wire calendar + deadline context into the floor

**Date**: 2026-04-16
**Author**: Lead Dev (code-opus)
**Issue**: #951 CONTEXT-ASSEMBLER-EXPAND
**Template**: `knowledge/gameplan-template.md`

---

## Phase -1: Infrastructure Verification

**Nature of work**: Add helper functions to existing Python module + thread through two existing gatherers. Not a schema change. Not a new service.

**Infrastructure facts** (verified via read-only scan):
- `services/intent_service/context_assembler.py` — exists, 446 lines, has `_gather_temporal_context` and `_gather_status_priority_context` already
- `services/integrations/calendar/calendar_integration_router.py` — exists, has `get_temporal_summary(user_id)` at line 230 (single call returns everything we need)
- `services/domain/models.py:1411` — `Todo.due_date: Optional[datetime]`
- `services/todo/todo_management_service.py:74` — `list_todos` accepts due_date filter, returns todos with the field
- `services/intent_service/conversational_floor.py:316-330` — formatter already expects `calendar: {next_meeting, next_free_block, time_available_minutes}` schema
- `tests/unit/services/intent_service/` — test location for assembler tests (verified exists)

**Worktree assessment**: SKIP. Single file touched, sequential work, small surface area. Rationale: overhead > benefit.

**Proceed/Revise**: PROCEED. Gap analysis matches filesystem state. No hidden prerequisites.

---

## Phase 0: GitHub Investigation — COMPLETED

- ✅ `gh issue view 951` — issue exists, milestone MVP, assigned via update
- ✅ #951 body updated with scope-corrected acceptance criteria
- ✅ Relevant source files read: context_assembler.py (all 446 lines), calendar_integration_router.py (key sections), relevant bits of conversational_floor.py + todo_management_service.py + models.py
- ✅ Gap analysis captured in `951-issue-audit.md`

---

## Phase 0.5 / 0.6 / 0.7: N/A

- No frontend-backend contract (pure Python, no routes)
- No multi-layer data flow change (existing flows; just adds a data source)
- Not a multi-turn conversation feature

---

## Phase 1: Deadline Proximity Helper (TDD)

**Objective**: Pure function with complete test coverage, landed before the calendar wiring that depends on it.

### Tasks

- [ ] Write failing unit tests for `_compute_deadline_proximity` covering:
  - `None` → `"none"`
  - due in past → `"overdue"`
  - due before end of today (local time) → `"due_today"`
  - due within 7 days from now → `"due_this_week"`
  - due > 7 days out → `"later"`
  - Edge: due_date == now → `"due_today"` (not overdue)
- [ ] Implement `_compute_deadline_proximity(due_date: Optional[datetime]) -> str` as a module-level function (not method — no self dependencies)
- [ ] Run tests → PASS

### Deliverables

- New tests in `tests/unit/services/intent_service/test_context_assembler_deadline.py`
- Helper function added to `services/intent_service/context_assembler.py` (top-level)

### STOP conditions

- Timezone confusion (deadline proximity depends on "today" — decide UTC vs local; for MVP, use `datetime.now()` naive to match existing gatherer pattern; flag if different needed)
- Over-engineering — don't introduce a `DeadlineProximity` enum if a string suffices

---

## Phase 2: Surface `due_date` in pending_todos

**Objective**: Existing `pending_todos` dict entries gain `due_date` and `deadline_proximity` fields.

### Tasks

- [ ] Write failing test: `_gather_temporal_context` with mocked `TodoManagementService.list_todos` returning todos with `due_date` → expect `pending_todos[i]` to contain `due_date` (ISO string) and `deadline_proximity` (one of the 5 buckets)
- [ ] Write failing test: same for `_gather_status_priority_context`
- [ ] Update both gatherers' pending_todos dict construction to include the two fields (use `getattr(t, "due_date", None)` for safety; compute proximity via helper)
- [ ] Run tests → PASS
- [ ] Verify no other tests broke (pending_todos is used in-house but the dict keys are additive — shouldn't break downstream)

### Deliverables

- Updated gatherers with deadline fields
- Tests added to existing test file (if one exists) or new test file

### STOP conditions

- If an existing test asserts `pending_todos[0] == {exact_dict}` with no `due_date` key, update the assertion (additive change is safe) — but do not silently weaken other assertions
- If `TodoManagementService.list_todos` does not actually return `Todo` objects with `due_date` attribute accessible via `getattr`, trace back to the repository / model

---

## Phase 3: Calendar Wiring

**Objective**: Assembler queries `CalendarIntegrationRouter` and fills `calendar` key in expected schema.

### Tasks

- [ ] Write failing test: `_gather_calendar_context` with mocked router returning a temporal_summary dict → expect `calendar` key with correct schema mapping
- [ ] Write failing test: `_gather_calendar_context` with mocked router raising (e.g., `RuntimeError("no calendar")`) → expect absent `calendar` key, no exception
- [ ] Write failing test: `_gather_temporal_context` invokes calendar helper (via mock) → `calendar` appears in returned context
- [ ] Write failing test: `_gather_status_priority_context` also invokes calendar helper
- [ ] Implement `_gather_calendar_context(user_id: str) -> Dict[str, Any]`:
  - Lazy-import `CalendarIntegrationRouter` (match existing pattern of lazy imports to avoid startup cost)
  - Pass `user_id` to constructor (per ADR-037 + #586 timezone awareness)
  - Call `await router.get_temporal_summary(user_id=user_id)`
  - Map response fields to the formatter's expected schema
  - Try/except — return `{}` on any error (log warning, match existing pattern)
- [ ] Invoke helper from both gatherers
- [ ] Run tests → PASS

### Deliverable

Updated `services/intent_service/context_assembler.py` with calendar wiring.

### STOP conditions

- Router response schema doesn't match formatter expectations → map fields explicitly; do not change the formatter
- Calendar call latency observed in tests > 2s on mocked calls → something's wrong with test setup; investigate before proceeding
- Import cycle detected → the lazy-import pattern should prevent this, but if it surfaces, investigate

---

## Phase 4: Verification

### Tasks

- [ ] Unit tests pass: `pytest tests/unit/services/intent_service/test_context_assembler*.py -v`
- [ ] Full unit suite pass: `pytest tests/unit/ --tb=no -q --maxfail=10` — expect 6242 + new tests, 0 failures
- [ ] Ruff clean: `ruff check .` + `ruff format --check .`
- [ ] Server smoke test: restart + one "what's on the agenda today?" query via API if calendar OAuth is live on test account
- [ ] Check whether `_format_domain_context` in `conversational_floor.py` surfaces `due_date`/`deadline_proximity` per-todo — likely NOT (current formatter only shows pending_todo_count). **Rule**: if the formatter extension is ≤ 5 lines and purely additive, include in this issue; if it requires restructuring `_format_domain_context`, file follow-up and leave assembler-side data available for #950 to pick up.
- [ ] Post progress comment to #951 with commit SHA + test pass output

### Evidence to capture

- Terminal output of new tests passing
- Full unit test count (6242 + delta)
- Sample output: run `python -c "import asyncio; from services.intent_service.context_assembler import ContextAssembler; ctx = asyncio.run(ContextAssembler().gather_context('TEMPORAL', user_id='<real_uuid>', session_id='test')); print(ctx)"`
- Save to `dev/2026/04/16/951-verification-evidence.md`

### STOP conditions

- Unit test failures → root-cause, don't paper over
- Unit test count drops below 6242 → something got deleted
- Calendar schema mismatch at runtime (smoke test) → fix before closing

---

## Phase 5: File Deferred-Scope Follow-ups

Before closing #951, file these as separate issues:

- [ ] **Sprint/milestone data assembly** — GitHub API queries for active milestone, issues in current milestone, sprint progress. Medium effort, depends on GitHub API rate-limit strategy.
- [ ] **Recent activity feed** — time-windowed queries across GitHub/Slack/calendar. Large effort, requires caching + event sourcing decision.
- [ ] **Blocked items identification** — requires label convention decision (e.g., "blocked", "needs-review") + cross-repo query. Small-medium; blocked on convention decision.
- [ ] **Redis TTL caching for context assembly** — performance optimization, fire if canonical retest shows latency > 2s. Currently deferred per docstring note in assembler ("design for Redis TTL caching later").

Each follow-up: `gh issue create` with Summary, Acceptance Criteria (short), and a link back to #951. Document filed issue numbers in the close comment.

---

## Phase Z: Closure

- [ ] Update #951 description with checkboxes marked per `close-issue-properly` skill
- [ ] Add closing comment with evidence (commit SHA, test output, sample response)
- [ ] Link the deferred follow-up issues
- [ ] Close via `gh issue close 951`
- [ ] Update session log
- [ ] Commit + push

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Calendar router behavior differs from its docstring (e.g., get_temporal_summary raises, not returns None) | Medium | Medium | Wrap in try/except per existing fail-graceful pattern |
| due_date field not consistently populated on returned Todo objects | Low | Low | `getattr(t, "due_date", None)` pattern handles absence |
| deadline_proximity timezone semantics confuse users | Medium | Low | Use naive `datetime.now()` for MVP matching existing gatherer pattern; document in helper docstring |
| Calendar call adds latency to floor responses | Medium | Medium | Phase 4 STOP condition; file caching follow-up if observed > 2s |
| Tests require extensive CalendarIntegrationRouter fixtures | Medium | Low | Use `unittest.mock.AsyncMock` at the router level; don't mock internals |
| Existing assembler tests fail due to new mandatory fields | Low | Low | Additive dict keys; existing assertions should survive |
| Pattern-062 recurrence: formatter and assembler still drift | Low | High | Phase 4 includes check that assembler output matches formatter expectations; verify in a unit test, not just at runtime |

---

## Data Flow

Context assembly flow (before → after):

```
User message → intent_service._process_intent_internal
  → ContextAssembler.gather_context(category, user_id, session_id)
    → (new) _gather_calendar_context(user_id)  — Phase 3
      → CalendarIntegrationRouter(user_id=user_id).get_temporal_summary(user_id)
      → maps to {calendar: {next_meeting, next_free_block, time_available_minutes}}
    → _gather_temporal_context OR _gather_status_priority_context
      → (new) invokes calendar helper  — Phase 3
      → (new) pending_todos entries include due_date + deadline_proximity  — Phase 2
    → returns merged context dict
  → ConversationalFloor._format_domain_context(context)
    → already handles calendar key (no change needed)
    → may need minor extension to surface per-todo deadlines (Phase 4 decision point)
  → system prompt + user message + context block → LLM
```

No schema changes to existing data sources. No new persistence.

---

## Rollback Plan

Single-file, additive-only change. If Phase 4 shows regressions:

1. `git revert <commit-sha>` — reverts cleanly since only `context_assembler.py` and new test files changed
2. Restart server
3. Verify canonical retest returns to pre-change baseline

No migrations, no schema changes. Rollback is trivial.

---

## Conversation Design Considerations

Not applicable in the Phase-0.7 sense (no multi-turn flow). But the voice transformation target is:

| Before (no calendar/deadline in context) | After (calendar + deadlines in context) |
|-----------------------------------------|-----------------------------------------|
| "Typical agenda items include..." (generic) | "You've got the CXO 1:1 at 2pm and a 90-minute block after..." |
| "What's due?" → list of todos by title | Same list + "one's due today, two are overdue" |
| "Next meeting?" → "I don't have calendar access" (when actually configured) | "Your next meeting is [title] at [time]" |

The prompt change in #950 will tell the LLM to *use* this data. This issue's job is making sure the data is *present*.

---

## Post-Completion

- Retro in session log
- Watch canonical retest TEMPORAL/STATUS scores in next verification run (either post-#950 or standalone)
- If Pattern-062 pattern shows up again (formatter/assembler drift), file a pattern-document update

---

## Open Questions (for PM if raised)

1. **Timezone semantics for `deadline_proximity`** — should "due today" use the user's timezone or UTC? MVP default: UTC via `datetime.now()` to match existing gatherer pattern. User timezones are supported elsewhere (#586) but not wired into this assembler yet.
2. **Formatter extension in Phase 4** — if surfacing per-todo deadlines requires modifying `_format_domain_context`, stay within #951 scope or defer to #950? My recommendation: make the minimal formatter change in-line (it's consistent with #951's intent) and note in closing comment.
3. **Calendar caching** — should we add a simple 5-minute in-memory TTL cache for calendar responses to avoid hammering the API on rapid successive queries? Deferring to follow-up, but flagging in case PM wants it in-scope.

---

_Gameplan created: 2026-04-16_
_Status: Ready for audit (audit cascade phase 2)_
