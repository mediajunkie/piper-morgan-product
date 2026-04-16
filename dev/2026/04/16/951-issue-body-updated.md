# CONTEXT-ASSEMBLER-EXPAND — Wire calendar + deadline context into the floor

**Priority**: P2
**Labels**: `feature`, `floor`, `context-assembly`
**Milestone**: MVP / M2c (Conversational Depth)
**Epic**: M2 Sprint — M2c sub-epic
**Related**: #950 (Floor Prompt — uses this context), #100 (superseded), #101 (superseded), #927-930 (testing track), ADR-060 (Floor-First Routing)

---

## Problem Statement

### Current State

`services/intent_service/context_assembler.py` has ~450 lines implementing category-specific gatherers for IDENTITY, DISCOVERY, TRUST, MEMORY, CONVERSATION, TEMPORAL, STATUS, PRIORITY (#925, #965, #903, #923, #960). Most of #951's original acceptance criteria are **already implemented** in these gatherers.

But two specific gaps remain and they matter for floor voice quality:

1. **Calendar is never assembled.** `conversational_floor.py:_format_domain_context` lines 316-330 *already expects* calendar fields (`next_meeting`, `next_free_block`, `time_available_minutes`), but the assembler never queries `CalendarIntegrationRouter` to fill them. This is a wire-up bug — the formatter was written anticipating calendar data and never got connected.

2. **Todo deadlines are not surfaced.** The `Todo` model has `due_date` support (`services/domain/models.py:1411`), and `TodoManagementService` accepts it. But the assembler's `_gather_temporal_context` and `_gather_status_priority_context` don't include `due_date` when listing pending_todos. Users asking "what's due?" or "what's my priority?" get todos with no deadline information.

### Impact

- **Blocks**: #950 verification. CXO's Pattern-045 flag in the Apr 16 direction memo: "The floor prompt can't fix what the context assembler doesn't deliver." Calendar and deadline data are what the prompt *expects* the LLM to use. Shipping #950 without them leaves a known Pattern-045 class bug.
- **User Impact**: "What's on the agenda today?" / "What's next?" / "When's my next meeting?" queries return generic responses because the calendar data isn't in context. "What's due?" returns todo titles without deadlines.
- **Technical Debt**: The formatter-without-assembler situation is exactly the kind of partial-wiring that Pattern-062 (Assembly Assumption) warns about — individually-correct components that don't compose correctly.

### Strategic Context

Per ADR-060 and the MUX analysis (`dev/2026/04/08/mux-analysis-what-survives-floor-first-2026-04-07.md`), the floor handles more than structured handlers assumed. The prerequisite is that the floor receives the right data. This issue closes two of the specific data gaps that #950 depends on for the canonical retest to show clean signal.

---

## Goal

**Primary Objective**: Wire `CalendarIntegrationRouter` into the context assembler's TEMPORAL and STATUS gatherers, and surface todo `due_date` in pending_todos output — so the floor can answer "what's next" / "what's due" / "when's my meeting" with specific, grounded responses instead of generic PM advice.

### Example User Experience

**Before (current, TEMPORAL query)**:
> User: What's on the agenda for today?
> Piper: [generic response about typical PM priorities, no meeting references]

**After (target)**:
> User: What's on the agenda for today?
> Piper: You've got the CXO 1:1 at 2pm and a 90-minute block free after that. Three pending todos, one due today — the M2c gameplan review.

Note: the "after" response uses calendar data (next_meeting, next_free_block) and deadline data (todo due_date within today) that the context assembler must provide.

### Not In Scope

- ❌ **Sprint/milestone data from GitHub API** — larger scope; file as follow-up issue
- ❌ **Recent activity feed** (commits, comments, reviews across integrations) — larger scope; file as follow-up
- ❌ **Blocked items from GitHub** — depends on label convention decisions; file as follow-up
- ❌ **Redis caching** for context assembly — performance optimization; file as follow-up if canonical retest shows latency issues
- ❌ **Rewriting existing gatherers** — IDENTITY, TRUST, MEMORY, etc. work fine; don't touch
- ❌ **Prompt changes** — that's #950; don't edit conversational_floor.py in this issue

---

## What Already Exists

### Working ✅ (in `context_assembler.py`)

- `_gather_identity_context` (#923) — capabilities + integrations from dispatcher/plugin registries
- `_gather_discovery_context` — delegates to identity
- `_gather_trust_context` — reads `UserTrustProfileRepository`
- `_gather_memory_context` — conversation turns + persistent user history
- `_gather_reminder_context` (#903) — due reminders for greeting time
- `_gather_temporal_context` (#965) — current_date, pending_todos, completed_todos, projects (names + last_updated), conversation history summary
- `_gather_status_priority_context` (#925) — projects list, priorities, organization, pending_todos, github_connected flag
- `_DATA_CATEGORIES` violation logging (#960) — warns if a data-query category reaches floor with no data
- Fail-graceful design — all gatherers catch exceptions and return partial/empty dicts

### Working ✅ (in `conversational_floor.py`)

- `_format_domain_context` already formats calendar fields when present (`next_meeting`, `next_free_block`, `time_available_minutes`) — waiting for assembler to fill them
- Fabrication guard (#960) — tells LLM to say "I don't have calendar access" when calendar key is absent

### Missing ❌

- **Calendar wiring** — `CalendarIntegrationRouter.get_next_meeting()`, `get_free_time_blocks()`, or `get_temporal_summary()` never called by assembler
- **Todo deadline surfacing** — `due_date` field excluded from assembler output for pending_todos
- **Deadline proximity helpers** — nothing computes "overdue" / "due today" / "due this week" from `due_date`

---

## Requirements

### Phase 1: Calendar wiring

**Objective**: Assembler queries calendar router and puts data under `calendar` key for floor formatter.

**Tasks**:
- [ ] Add `_gather_calendar_context(user_id)` helper that calls `CalendarIntegrationRouter.get_temporal_summary()` (single call returns next_meeting, free_blocks, recommendations)
- [ ] Invoke helper from `_gather_temporal_context` and `_gather_status_priority_context`
- [ ] Wrap in try/except — calendar unavailable (no OAuth, plugin disabled) returns absent calendar key, never throws
- [ ] Map the router response to the schema the floor formatter expects: `{calendar: {next_meeting: {title, start}, next_free_block: {start, duration_minutes}, time_available_minutes: int}}`

**Deliverables**:
- `services/intent_service/context_assembler.py` with `_gather_calendar_context`
- Unit test covering: calendar available → fields populated; calendar unavailable → absent key
- Unit test for the TEMPORAL + STATUS integration

### Phase 2: Deadline surfacing

**Objective**: Todo `due_date` appears in pending_todos output; compute deadline_proximity helper.

**Tasks**:
- [ ] Extend `pending_todos` dicts in `_gather_temporal_context` and `_gather_status_priority_context` to include `due_date` (ISO string) and `deadline_proximity` (enum: `overdue`, `due_today`, `due_this_week`, `later`, `none`)
- [ ] Add `_compute_deadline_proximity(due_date: Optional[datetime])` pure helper
- [ ] Ensure `_format_domain_context` in `conversational_floor.py` surfaces `due_date` / `deadline_proximity` when present — check formatter; may need minor update

**Deliverables**:
- Updated assembler with deadline fields
- Unit tests for `_compute_deadline_proximity` covering all 5 proximity buckets + `None`
- Unit tests for pending_todos including due_date/deadline_proximity

### Phase 3: Verification

- [ ] All unit tests pass
- [ ] `ruff check` + `ruff format` clean
- [ ] Canonical retest — TEMPORAL and STATUS categories show specific responses (calendar + deadlines referenced where present)
- [ ] Fabrication guard regression: calendar-unavailable responses remain honest ("I don't see a calendar integration…")
- [ ] Follow-up issues filed for deferred scope (sprint, activity, blocked, caching)

---

## Acceptance Criteria

### Functionality
- [x] ~~Context assembler extended to handle all floor-routed intent categories~~ (already done — removed; see "What Already Exists")
- [ ] TEMPORAL/STATUS queries receive calendar data when calendar is configured
- [ ] TEMPORAL/STATUS queries receive todo `due_date` and `deadline_proximity` fields
- [ ] Calendar-unavailable path returns absent calendar key (no exception, no empty struct masquerading as data)
- [ ] `_compute_deadline_proximity` returns one of: `overdue`, `due_today`, `due_this_week`, `later`, `none`

### Testing
- [ ] Unit tests for `_gather_calendar_context` (available + unavailable paths)
- [ ] Unit tests for `_compute_deadline_proximity` (all proximity buckets + None)
- [ ] Unit tests confirming `pending_todos` entries include `due_date` / `deadline_proximity` when populated
- [ ] Existing `tests/unit/` suite passes (6242 passed baseline)
- [ ] Canonical retest TEMPORAL / STATUS categories show specific responses when calendar + deadlines are available

### Quality
- [ ] No regressions in existing gatherers
- [ ] Calendar call failures do not propagate (fail-graceful preserved)
- [ ] Ruff clean
- [ ] No new F821/F823 warnings

### Documentation
- [ ] Gameplan at `dev/2026/04/16/951-gameplan.md`
- [ ] Audit docs at `951-issue-audit.md` + `951-gameplan-audit.md`
- [ ] Follow-up issues filed for deferred scope (at least: sprint data, activity feed, blocked items, caching)
- [ ] Close #951 with evidence via `close-issue-properly` skill

---

## Testing Strategy

### Primary: Unit tests

Focused on the new helpers. TDD where possible.

- `_compute_deadline_proximity`: pure function, trivial to test. All 5 buckets + None. Edge: exactly now, exactly 24h, exactly 7d.
- `_gather_calendar_context`: mock `CalendarIntegrationRouter.get_temporal_summary` — verify field mapping. Mock failure (router raises) — verify absent key, no exception.
- `pending_todos` contract: mock `TodoManagementService.list_todos` — verify output includes `due_date` + `deadline_proximity` when todos have due_date set.

### Secondary: Canonical retest

Post-implementation, run the canonical retest for TEMPORAL and STATUS categories. Key queries:
- "What's on the agenda for today?" — calendar references expected
- "When's my next meeting?" — calendar reference expected
- "What's due?" — deadline references expected
- "What am I working on?" — projects + deadlines if applicable

If canonical retest still shows generic responses despite real data being present, the gap is likely in the **formatter** (does `_format_domain_context` surface deadline_proximity?) or in the **prompt** (does the floor prompt tell the LLM to use these fields?). Root-cause before claiming done.

### Manual spot check

After implementing, test locally with a calendar-connected account: ask "What's on the agenda today?" via the server and verify response references a real meeting from the calendar.

---

## Success Metrics

### Quantitative
- Unit tests pass (target: +8-12 new tests, 0 failures)
- Canonical retest TEMPORAL ≥ current baseline (currently 1/9 per CXO note — aim for improvement but no specific threshold without canonical retest run first)
- No regressions in existing test count (6242 baseline)
- `_compute_deadline_proximity` ≤ 1ms per call (pure function, no I/O — should be trivial)
- Calendar call latency acceptable (target: < 2s; if consistently > 5s, escalate for caching discussion)

### Qualitative
- Calendar-available queries produce responses that reference actual meetings
- Deadline-aware queries produce responses that reference actual due dates
- Calendar-unavailable queries still produce honest fallbacks (no fabrication)

---

## STOP Conditions

- **Canonical retest regresses** on any category after implementation — root-cause before proceeding
- **Fabrication guard weakens** — if calendar-unavailable responses start inventing meetings, immediate rollback
- **Calendar router not mockable cleanly** — if tests require extensive fixtures for CalendarIntegrationRouter, escalate to PM about test strategy
- **Data schema mismatch** with `_format_domain_context` — if the assembler's output doesn't match what the formatter expects, fix assembler (don't touch formatter — that's #950 territory)
- **Performance blockers** — if calendar call adds > 5s to floor response, file caching issue and decide whether to ship with known latency or block

---

## Effort Estimate

**Overall Size**: Small-to-medium

**Breakdown**:
- Audit cascade (issue + gameplan + doc): Small (~45 min; done in session)
- Phase 1 (calendar wiring): Small-medium (~60-90 min — includes test setup for mocking router)
- Phase 2 (deadline surfacing): Small (~30-45 min)
- Phase 3 (verification + canonical retest): Small-medium (~30-60 min depending on findings)
- File follow-up issues: Small (~15 min)
- Issue closure: Small (~15 min)

Total: ~3-4 hours Lead Dev time.

---

## Dependencies

### Required (blocking)
- `CalendarIntegrationRouter` operational (already exists, verified via `grep`)
- `TodoManagementService.list_todos` returns todos with `due_date` populated (already supported per `models.py:1411`)

### Optional (nice to have)
- Calendar OAuth configured on test account for manual spot-check

### Downstream (this improves)
- #950 verification — canonical retest runs cleaner with real context available
- Future sprint/activity/blocked features (decomposed out of this issue's scope)

---

## Related Documentation

- `docs/internal/architecture/current/adrs/adr-060-*.md` — Floor-First Routing
- `docs/internal/architecture/current/adrs/adr-037-*.md` — Calendar Integration Router
- `dev/2026/04/08/mux-analysis-what-survives-floor-first-2026-04-07.md` — why context assembly is constitutional
- `mailboxes/lead/read/memo-cxo-to-lead-dev-950-direction-2026-04-16.md` — CXO flag on Pattern-045 / context assembly
- Pattern-062 — Assembly Assumption (individually-correct components don't compose)

---

## Notes for Implementation

The calendar router already has a convenient `get_temporal_summary(user_id)` method that returns everything we need in one call. Prefer this over multiple separate calls (`get_next_meeting` + `get_free_time_blocks`) for latency.

The formatter in `conversational_floor.py` lines 316-330 is the ground truth for the expected calendar schema. Match it exactly — don't invent a new schema.

Follow-up issues to file before closing #951:
1. Sprint/milestone data assembly from GitHub API
2. Recent activity feed (cross-integration, time-windowed)
3. Blocked items identification (requires label convention decision)
4. Redis caching for context assembly (if latency warrants)

---

_Issue created: 2025-? (pre-dates available history)_
_Last updated: 2026-04-16_
_Current status: Planning → Implementation_
