# Gameplan: #1053 — Migrate downstream standup tests to async fixtures (Fake-based)

**Issue**: #1053
**Branch**: `claude/1053-standup-test-migration` (subagent worktree)
**Drafted**: 2026-05-06 by Lead Developer
**Template**: gameplan-template.md (v9.3-equivalent)
**Audit-cascade artifact**: yes — issue audit at `dev/2026/05/06/1053-issue-audit.md`

**PM disposition**: Subagent execution per PM May 5 direction ("tackle that tedious work as a follow-on"). Audit-cascade gating per PM May 6 direction.

---

## Summary

Migrate three downstream standup test files (~1,470 lines total) from sync-fixture-+-real-manager to async-fixture-+-`FakeStandupConversationManager`. All work is test-scope; no production code in `services/standup/` should change. Subagent-driven; Lead Dev verifies via post-execution audit.

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Dev's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (not relevant — test scope only)
- [x] Testing framework: pytest + pytest-asyncio (relevant; in venv already)
- [x] Database: PostgreSQL prod / aiosqlite for unit tests (we're staying out of DB entirely)
- [x] Existing endpoints: N/A (test code)
- [x] Existing fixtures pattern in target files: `@pytest.fixture` (sync) — needs conversion
- [x] Test double `FakeStandupConversationManager` exists at `tests/unit/services/standup/_fake_conversation_manager.py` — verified
- [x] Reference implementation `test_conversation_state.py` (post-#1052 Phase 2) — verified passes
- [x] InsightJournal precedent at `tests/unit/services/mux/_fake_insight_journal.py` — verified exists

**My understanding of the task**:
- Mechanical migration: sync `@pytest.fixture` → `@pytest_asyncio.fixture async def`; add `await` to all manager method calls; replace direct `_conversations` dict access with public-API calls (`get_conversation`, `get_suspended_for_user`, etc.)
- Three target files; possible 4th (adapter test) if Phase 0 finds it
- No production code changes
- Pattern is well-understood; risk is concentrated in size of largest file (Phase 1, 749 lines)

### Part A.2: Work Characteristics Assessment

**Worktree assessment:**
- ☑ Multiple agents will work (Lead Dev preps, subagent executes) → favors worktree
- ☑ Task duration > 30 minutes (~2-3 hours) → favors worktree
- ☑ Single-component work (test files only) → mild against
- ☐ Parallel agents on different files? Plausible (3 files = 3 sequential phases or 3 parallel subagents) — but linear-sequential is safer for review
- ☐ Time-critical? No.

**Decision: USE WORKTREE** — durability + isolation matter more than overhead. Branch: `claude/1053-standup-test-migration`. Subagent will operate in `.trees/1053-standup-test-migration/` (or equivalent path the subagent harness chooses).

### Part B: PM Verification Required

**This gameplan operates against established context** (#1052 Phase 2 just shipped yesterday; Lead Dev ran the audit cascade tonight). PM has already:
- Confirmed Option B for issue's "Example User Experience" interpretation (Developer Experience)
- Approved the subagent + audit-cascade approach (May 5 + May 6)

No additional PM verification needed for Phase -1. Proceed/Revise: **PROCEED**.

### Part C: Proceed/Revise Decision

- [x] **PROCEED** — Understanding is correct; gameplan appropriate; PM context confirmed.

---

## Phase 0: GitHub Investigation + Pre-flight

**Subagent first step**. ~15 min.

### Required Actions

```bash
gh issue view 1053
git log --oneline -10  # confirm post-1057 main
ls tests/unit/services/standup/_fake_conversation_manager.py  # double verify the Fake exists
ls tests/unit/services/standup/test_conversation_state.py  # reference impl
```

### Inventory pass on the 3 target files

For each target file:

```bash
# Inventory fixtures
grep -n "@pytest.fixture\|@pytest_asyncio.fixture" tests/unit/services/standup/test_conversation_handler.py

# Inventory direct _conversations access
grep -n "_conversations" tests/unit/services/standup/test_conversation_handler.py

# Inventory manager method calls in test bodies
grep -n "manager\.\|\.manager\." tests/unit/services/standup/test_conversation_handler.py
```

Repeat for:
- `tests/unit/services/standup/test_standup_routing_585.py`
- `tests/unit/services/standup/test_standup_suspend_resume_889.py`

### Possible adapter test discovery

```bash
ls tests/unit/services/process/ 2>/dev/null
grep -rln "StandupProcessAdapter" tests/ 2>/dev/null
```

### Phase 0.5–0.8 explicitly N/A (PM-approved 2026-05-06)

- **0.5 Frontend-Backend Contract**: N/A. Pure test migration; no UI surface, no API contracts touched.
- **0.6 Data Flow & Integration**: N/A. No new data flows or integrations; tests stay in-process and DB-free.
- **0.7 Conversation Design**: N/A. Not a conversational feature.
- **0.8 Post-Completion Integration**: N/A. No new wiring or state-machine endpoints.

PM approval recorded in turn-log on 2026-05-06 ~19:55, after Lead Dev surfaced the four sub-phases via audit-cascade Phase 2 stop-and-ask.

If found: scope into Phase 4. If not: skip Phase 4.

### Test count baseline

```bash
venv/bin/python -m pytest tests/unit/services/standup/ --collect-only -q 2>&1 | tail -5
```

Record total collect count. Post-migration count must be ≥ this baseline.

### STOP Conditions

- If `_fake_conversation_manager.py` doesn't exist or its API surface is missing methods used by the target files → STOP and surface
- If a target file has structural issues beyond async migration (e.g., references deleted services) → STOP
- If `test_conversation_state.py` is failing on main → infrastructure broken, STOP

---

## Phase 1: `test_conversation_handler.py` migration (largest, 749 lines)

**Estimate**: 45 min subagent-execution

### Files
- `tests/unit/services/standup/test_conversation_handler.py` (modify)

### Tasks

1. Replace `StandupConversationHandler()` instantiations with `StandupConversationHandler(conversation_manager=FakeStandupConversationManager())`. Add the import: `from tests.unit.services.standup._fake_conversation_manager import FakeStandupConversationManager`.

2. Convert `@pytest.fixture` bodies that call manager methods to `@pytest_asyncio.fixture async def ...`. Add `await` on every manager call inside the fixture. Update fixture import to `import pytest_asyncio` if missing.

3. Update test bodies that call manager methods directly to `await` them.

4. Replace direct `_conversations` access: most likely either `.get_conversation_by_session(...)` (most common) or `.get_suspended_for_user(...)` (resume tests).

5. Run file in isolation iteratively until green:
   ```bash
   venv/bin/python -m pytest tests/unit/services/standup/test_conversation_handler.py -p no:cacheprovider --no-header
   ```

### Acceptance for Phase 1

- All tests in `test_conversation_handler.py` pass
- Test count preserved (or strictly justified if any test became obsolete)
- No DB connection attempts (verify via Postgres-down test if doubt)

### Verification gate

Subagent must report:
- Count of tests in file (pre + post)
- Pytest output showing all passing
- Any tests that became obsolete + reason

---

## Phase 2: `test_standup_routing_585.py` migration (362 lines)

**Estimate**: 30 min subagent-execution

### Files
- `tests/unit/services/standup/test_standup_routing_585.py` (modify)

### Tasks
Same shape as Phase 1, scoped to routing tests. Specific watchpoints:
- Routing tests likely have direct `manager._conversations` reads to assert state
- Replace with `await manager.get_conversation_by_session(...)` / `get_conversation_by_user(...)`

### Acceptance / Verification
Same shape as Phase 1.

---

## Phase 3: `test_standup_suspend_resume_889.py` migration (359 lines)

**Estimate**: 30 min subagent-execution + bind_session_id coverage if needed.

### Files
- `tests/unit/services/standup/test_standup_suspend_resume_889.py` (modify)

### Tasks

Same fixture conversion as Phases 1+2 PLUS:

**Verify `bind_session_id` E2E coverage** (added in #1052 Phase 2 to fix the resume-flow bug). If the file doesn't already exercise the path "suspend conv on session-A → resume on session-B → bind happens → adapter routes via session-B":
- Add 1-2 tests covering this scenario
- Use `FakeStandupConversationManager` + `StandupProcessAdapter` (the real adapter)

### Acceptance / Verification

Same shape as Phases 1+2, plus:
- `grep -n "bind_session_id" tests/unit/services/standup/test_standup_suspend_resume_889.py` returns non-empty

---

## Phase 4: Possible adapter test (CONDITIONAL on Phase 0 finding)

If Phase 0 discovers a file in `tests/unit/services/process/` that targets `StandupProcessAdapter`:

**Estimate**: 15 min subagent-execution

### Tasks
- Same migration shape applied to that file
- Likely involves `await manager.get_suspended_for_user(...)` for `has_suspended_session()` test cases (per the Phase 2 cleanup in #1052)

### If no such file exists
Skip this phase entirely. Subagent reports "Phase 4 skipped — no adapter test file found for StandupProcessAdapter."

---

## Phase 5: Tests + verification

**Estimate**: 15 min subagent-execution

### Required actions

1. Full standup directory pass:
   ```bash
   venv/bin/python -m pytest tests/unit/services/standup/ -p no:cacheprovider --no-header
   ```
   Expected: all green; count ≥ baseline from Phase 0.

2. Touched-area regression:
   ```bash
   venv/bin/python -m pytest tests/unit/services/ -p no:cacheprovider --no-header --tb=no -q 2>&1 | tail -10
   ```
   Expected: no NEW failures vs pre-PR baseline (record any pre-existing for sanity).

3. No `_conversations` direct access:
   ```bash
   grep -rn "manager\._conversations\|\._conversations\b" tests/unit/services/standup/
   ```
   Expected: empty.

4. Postgres-down sanity (optional but recommended):
   ```bash
   POSTGRES_PORT=99999 venv/bin/python -m pytest tests/unit/services/standup/ -p no:cacheprovider --no-header -q 2>&1 | tail -5
   ```
   Expected: all green (proves no real DB connections).

### Test scope requirements
- [x] **Unit tests**: each migrated file passes in isolation
- [x] **Integration tests**: full standup directory passes
- [x] **Wiring tests**: `bind_session_id` E2E covered in Phase 3
- [x] **Regression tests**: `tests/unit/services/` no new failures

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. Update issue #1053 with evidence: pytest outputs, grep verification, before/after test counts.
2. Run sign-off discipline (per CLAUDE.md): branch fully merged or NOTICE filed; commits pushed.
3. Lead Dev runs **post-execution audit** of subagent's work against this gameplan + the prompts. Flag drift if any.
4. PM approval request via comment on #1053.

### Evidence Summary template (subagent fills in)

```bash
$ pytest tests/unit/services/standup/  # all green, N tests
$ grep -rn "manager\._conversations" tests/unit/services/standup/  # empty
$ POSTGRES_PORT=99999 pytest tests/unit/services/standup/  # still green
$ pytest tests/unit/services/  # no new failures vs baseline
```

### Handoff to PM

Subagent posts on issue:

```markdown
#1053 ready for review.

- All target files migrated: ✓ (file list + commit hash)
- Standup directory: N/N passing
- _conversations access points: 0
- bind_session_id E2E: covered (test names)
- Touched-area regression: clean

Awaiting Lead Dev post-execution audit + PM approval.
```

---

## STOP Conditions (apply throughout all phases)

The subagent MUST STOP and escalate to Lead Dev (via PR comment, GitHub issue comment, or session log) if:

1. **Fake API surface gap**: a test needs a manager method or behavior the Fake doesn't provide → file as separate issue, don't extend the Fake on the fly
2. **Test asserts on internal state with no public-API equivalent**: file + escalate
3. **More than 5 tests become obsolete**: rethink scope with Lead Dev/PM
4. **Production code in `services/standup/` looks like it needs to change**: NOT in scope, flag for separate issue
5. **Touched-area regression introduces new failures**: investigate before continuing
6. **Cross-cutting structural issues** in a target file beyond mechanical async conversion: STOP
7. **Cross-agent git collision** (parallel agent on same branch/files): STOP, surface, do NOT force-push
8. **Test count drops more than +/-2 from baseline without explicit justification**: STOP

When stopped: document in PR / issue comment, options analysis, wait for Lead Dev or PM decision.

---

## Multi-Agent Coordination Plan

### Agent deployment

- **Lead Developer (this session)**: Phase -1, audit-cascade prep (issue/gameplan/prompts), post-execution verification audit
- **Subagent (general-purpose, claude-code Sonnet equivalent)**: Phase 0 → Phase Z execution
- **PM**: final approval at Phase Z

### Verification gates

| Phase | Verifier | Verification artifact |
|-------|---|---|
| -1 (planning) | Lead Dev | `1053-issue-audit.md`, `1053-gameplan-audit.md` |
| 0 (investigation) | Subagent self-verification | Phase 0 inventory output in PR |
| 1-4 (per-file migration) | Subagent self-test (in-isolation green) | Pytest output per file |
| 5 (verification) | Subagent | Full pytest + grep + Postgres-down |
| Z (handoff) | Lead Dev (post-execution audit) | Audit document at `dev/YYYY/MM/DD/1053-execution-audit.md` |
| Approval | PM | Issue closure |

---

## Effort Estimate (consolidated)

| Phase | Estimate |
|---|---|
| Phase -1 (planning, this session) | 30 min Lead Dev (DONE post-this-document) |
| Phase 0 (investigation) | 15 min subagent |
| Phase 1 (test_conversation_handler.py) | 45 min subagent |
| Phase 2 (test_standup_routing_585.py) | 30 min subagent |
| Phase 3 (test_standup_suspend_resume_889.py) | 30 min subagent + extra if bind_session_id needs new tests |
| Phase 4 (adapter test, conditional) | 15 min subagent |
| Phase 5 (verification) | 15 min subagent |
| Phase Z (handoff + Lead Dev audit) | 30 min Lead Dev |

**Subagent total**: ~2-3 hours (per issue body estimate). **Lead Dev total**: ~1 hour planning + audit.

---

## Dependencies

### Required
- [x] #1052 Phase 2 closed (manager async rewrite)
- [x] `FakeStandupConversationManager` test double exists
- [x] `test_conversation_state.py` (manager-level reference) passes on main

### Optional
- None

---

## Evidence Requirements

Subagent must collect and post on #1053:

- Commit hashes per phase (or one consolidated commit if work is small)
- Pytest output per migrated file (in-isolation passing)
- Full standup directory pytest output
- Grep verification output (no `_conversations` access)
- Postgres-down sanity output (optional)
- Touched-area regression output

---

## Audit Cascade Matrix

This document is Phase 2 of the audit cascade. Issue audit is Phase 1 (`1053-issue-audit.md`). Prompts will be Phase 3 (`1053-prompts.md` + audit). Subagent execution is post-cascade.
