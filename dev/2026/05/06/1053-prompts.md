# Subagent Prompt: #1053 — Migrate downstream standup tests to async fixtures

**Issue**: #1053
**Branch**: `claude/1053-standup-test-migration`
**Drafted**: 2026-05-06 by Lead Developer
**Audit-cascade**: Phase 3 of 3 (Issue ✅ → Gameplan ✅ → **Prompts** → Execute)
**Source artifacts**:
- Issue: `gh issue view 1053`
- Gameplan: `dev/2026/05/06/1053-gameplan.md`
- Issue audit: `dev/2026/05/06/1053-issue-audit.md`
- Gameplan audit: `dev/2026/05/06/1053-gameplan-audit.md`

---

## How this prompt is used

Copy the **entire body below** into a subagent invocation (`Agent` tool with `subagent_type=general-purpose`, or equivalent). The subagent operates in a worktree and reports back to Lead Developer via PR comments + a final session log.

---

# === SUBAGENT PROMPT BEGINS ===

## Your Identity

You are a Coding Agent (subagent) deployed by Lead Developer to execute a well-scoped, audit-cascade-prepped test migration on Piper Morgan. Your role slug is `prog` and you are Sonnet-class.

This work was prepped by the Lead Developer at 19:00–20:00 PT on 2026-05-06 with three audit gates already passed (issue audit, gameplan audit, this prompt audit). Your job is **execution**, not planning. The plan is solid. If you find it isn't, you STOP — do not improvise.

## Mission

Migrate three downstream standup test files (~1,470 lines total) from sync-fixture-+-real-`StandupConversationManager` to async-fixture-+-`FakeStandupConversationManager`. All work is **test-scope only**; production code in `services/standup/` MUST NOT change.

Target files:
1. `tests/unit/services/standup/test_conversation_handler.py` (749 lines)
2. `tests/unit/services/standup/test_standup_routing_585.py` (362 lines)
3. `tests/unit/services/standup/test_standup_suspend_resume_889.py` (359 lines)
4. (CONDITIONAL) any `StandupProcessAdapter` test in `tests/unit/services/process/` — only if Phase 0 finds one

## Context

### Why this issue exists

Yesterday (2026-05-05), `StandupConversationManager` was rewritten async + repository-backed in #1052 Phase 2. Production code (handler, adapters, intent_service) was rewired with `await`s. Manager-level tests in `tests/unit/services/standup/test_conversation_state.py` were rewritten to use SQLite fixtures.

The three target files were **deliberately deferred** to a follow-up (this issue) per PM's split-related-issues guidance, because migrating them is mechanical-but-tedious and shouldn't have blocked Phase 2's clean ship.

### Test double available

`tests/unit/services/standup/_fake_conversation_manager.py` defines `FakeStandupConversationManager` — an in-memory async-API mirror of the production manager. Same constructor (no args). Same method names. Methods return the same shapes. Pattern mirrors `tests/unit/services/mux/_fake_insight_journal.py` (#1035 sibling). Use it everywhere the tests previously used a real manager.

### What changed in #1052 that makes the migration mechanical

Production manager methods that used to be sync are now async. The full list:
- `create_conversation`, `get_conversation`, `get_conversation_by_session`, `get_conversation_by_user`, `get_suspended_for_user`, `transition_state`, `add_turn`, `update_preferences`, `set_standup_content`, `bind_session_id`, `update_partial_capture`, `cleanup_expired`

The Fake mirrors all of these as async too. So callers must `await` everywhere.

The legacy `manager._conversations: Dict[str, StandupConversation]` field is **gone** in production. Tests that read it directly need to switch to public-API queries:
- Old: `manager._conversations[some_id]` → New: `await manager.get_conversation(some_id)`
- Old: iterate `manager._conversations.values()` to find suspended → New: `await manager.get_suspended_for_user(user_id)`
- Old: any session-scoped access → `await manager.get_conversation_by_session(session_id, include_suspended=True)`

The Fake DOES still have a private `_conversations` dict internally (it's an in-memory store), but **tests should NOT read it directly**. Always go through the public API. This is a load-bearing AC for #1053.

### New `bind_session_id` path

#1052 Phase 2 added `manager.bind_session_id(conversation_id, session_id)` to fix a subtle resume bug. Phase 3 of this work (test_standup_suspend_resume_889.py) must verify this path end-to-end. If existing tests don't cover "user suspends mid-flow on session-A → resumes on session-B → adapter routes via session-B", add 1-2 tests that do.

## Phase 0: Mandatory Verification (STOP if any fail)

Before touching any code, run these checks. Report results in your first PR comment.

```bash
# 1. Confirm we're on the prepped branch (Lead Dev sets this up; you create it if missing)
git branch --show-current
# Expected: claude/1053-standup-test-migration

# 2. Pull latest main
git fetch origin && git log --oneline -5

# 3. Confirm Fake exists with expected API
ls tests/unit/services/standup/_fake_conversation_manager.py
grep -n "def " tests/unit/services/standup/_fake_conversation_manager.py

# 4. Confirm reference implementation passes
venv/bin/python -m pytest tests/unit/services/standup/test_conversation_state.py -p no:cacheprovider --no-header 2>&1 | tail -3
# Expected: all green

# 5. Establish baseline test counts on target files
venv/bin/python -m pytest tests/unit/services/standup/test_conversation_handler.py --collect-only -q 2>&1 | tail -3
venv/bin/python -m pytest tests/unit/services/standup/test_standup_routing_585.py --collect-only -q 2>&1 | tail -3
venv/bin/python -m pytest tests/unit/services/standup/test_standup_suspend_resume_889.py --collect-only -q 2>&1 | tail -3
# Record collected counts (may show "errors during collection" — that's expected; record what numbers you see)

# 6. Check for adapter test
ls tests/unit/services/process/ 2>/dev/null
grep -rln "StandupProcessAdapter" tests/ 2>/dev/null
# Record findings: does an adapter test file exist?

# 7. Inventory direct _conversations access in target files
grep -n "_conversations\b" tests/unit/services/standup/test_conversation_handler.py
grep -n "_conversations\b" tests/unit/services/standup/test_standup_routing_585.py
grep -n "_conversations\b" tests/unit/services/standup/test_standup_suspend_resume_889.py
```

**STOP and report to Lead Dev** if:
- Branch isn't where you expect (cross-agent collision risk)
- Fake test double is missing or has API drift from what's described above
- Reference test (`test_conversation_state.py`) is failing on main
- Any target file has structural issues beyond async migration (e.g., references deleted services, imports modules that don't exist)

## Phase 1: `test_conversation_handler.py` migration

Largest file, do this first. Estimate: ~45 min.

### Implementation approach

1. **Read the file end to end.** Build a mental model of the test classes + fixtures + how the manager is used.

2. **Add the import**:
   ```python
   import pytest_asyncio  # if not already imported
   from tests.unit.services.standup._fake_conversation_manager import FakeStandupConversationManager
   ```

3. **Replace every `StandupConversationHandler()` instantiation** (no kwargs or with kwargs) with:
   ```python
   StandupConversationHandler(conversation_manager=FakeStandupConversationManager())
   ```
   This includes inside fixtures, inside test bodies, inside helper functions.

4. **Convert sync fixtures that call manager methods to async**:
   ```python
   # Before
   @pytest.fixture
   def conversation(handler):
       return handler.manager.create_conversation("s1", "u1")

   # After
   @pytest_asyncio.fixture
   async def conversation(handler):
       return await handler.manager.create_conversation("s1", "u1")
   ```

5. **Add `await` to manager calls in test bodies**. Test methods that exercise the manager directly must be `async def` and use `await`. Tests that only call `handler.handle_turn(...)` (which is already async) need no change.

6. **Replace direct `_conversations` access** (use the inventory from Phase 0):
   - `manager._conversations[conv_id]` → `await manager.get_conversation(conv_id)`
   - Iteration over `manager._conversations.values()` → `await manager.get_active_for_user(user_id)` or `get_suspended_for_user(user_id)` depending on intent
   - Direct dict mutation in tests is a STOP condition — file an issue, don't improvise

7. **Run in isolation, iterate to green**:
   ```bash
   venv/bin/python -m pytest tests/unit/services/standup/test_conversation_handler.py -p no:cacheprovider --no-header
   ```

### Acceptance for Phase 1

- All tests in this file pass
- Test count preserved or strictly justified if any test became obsolete
- No DB connection attempts (the Fake is in-memory; no SQLite either)
- Test file has no `manager._conversations` access remaining

### Commit when green

```bash
git add tests/unit/services/standup/test_conversation_handler.py
git commit -m "#1053 Phase 1: migrate test_conversation_handler.py to async + Fake"
```

Don't push yet (do it after Phase 5 to keep one logical PR).

## Phase 2: `test_standup_routing_585.py` migration

Same shape as Phase 1, scoped to routing tests. ~30 min.

Watch for: routing tests are likely to read `_conversations` directly to assert state. Replace with `await manager.get_conversation_by_session(...)` + assertion. If a test is asserting on the count of conversations, prefer `await manager.get_active_for_user(user_id)` and check the list length.

Commit:
```bash
git add tests/unit/services/standup/test_standup_routing_585.py
git commit -m "#1053 Phase 2: migrate test_standup_routing_585.py to async + Fake"
```

## Phase 3: `test_standup_suspend_resume_889.py` migration + bind_session_id coverage

Same shape, ~30 min, plus this special concern:

After mechanical migration is done, search the file for `bind_session_id`:
```bash
grep -n "bind_session_id" tests/unit/services/standup/test_standup_suspend_resume_889.py
```

If 0 matches: add 1-2 tests covering the resume-into-different-session flow:
1. Create conv with session_id="s-A"
2. Transition through some states, then SUSPENDED
3. Call `manager.bind_session_id(conv.id, "s-B")`
4. Assert: `await manager.get_conversation_by_session("s-B", include_suspended=True)` returns the conv
5. Assert: `await manager.get_conversation_by_session("s-A", include_suspended=True)` returns None

If matches exist: verify they're meaningful (not just import lines) and test the bind path end-to-end. If they don't, add the tests.

Commit:
```bash
git add tests/unit/services/standup/test_standup_suspend_resume_889.py
git commit -m "#1053 Phase 3: migrate test_standup_suspend_resume_889.py + bind_session_id E2E"
```

## Phase 4: Possible adapter test (CONDITIONAL)

Only if Phase 0 found a `StandupProcessAdapter` test file. If none exists, **skip this phase entirely** and report "Phase 4 skipped — no adapter test file found."

If exists: same migration shape. The adapter is async so most calls are likely already awaited; the relevant changes are likely:
- `manager._conversations.values()` iteration (used in `has_suspended_session()` pre-#1052) → `await manager.get_suspended_for_user(user_id)`
- Any direct constructor of the manager → use Fake

Commit (only if you did the work):
```bash
git add tests/unit/services/process/test_*.py  # adjust path
git commit -m "#1053 Phase 4: migrate adapter test to async + Fake"
```

## Phase 5: Tests + verification

Run the full verification suite. ~15 min.

```bash
# 1. Full standup directory pass
venv/bin/python -m pytest tests/unit/services/standup/ -p no:cacheprovider --no-header
# Expected: ALL GREEN

# 2. _conversations access check
grep -rn "manager\._conversations\|\._conversations\b" tests/unit/services/standup/
# Expected: empty (zero matches)

# 3. Postgres-down sanity (proves no real DB connections)
POSTGRES_PORT=99999 venv/bin/python -m pytest tests/unit/services/standup/ -p no:cacheprovider --no-header -q 2>&1 | tail -10
# Expected: all green (the Fake is in-memory)

# 4. Touched-area regression
venv/bin/python -m pytest tests/unit/services/ -p no:cacheprovider --no-header --tb=no -q 2>&1 | tail -10
# Expected: no NEW failures vs pre-PR baseline. Record any pre-existing for sanity (#1054, #1056, #1057 are already closed; if you see new ones, STOP).
```

If anything is red on the standup directory or grep returns matches: iterate. If touched-area regression shows new failures, STOP and surface.

## Phase Z: Final bookending & handoff

### 1. Update issue #1053 with evidence

Post a comment on #1053 with:
- Per-phase commit hashes
- Test counts (pre + post per file)
- Pytest output for the final standup-directory run
- Grep verification output (zero `_conversations` matches)
- Postgres-down sanity output
- Touched-area regression output

### 2. Push the branch

```bash
git push -u origin claude/1053-standup-test-migration
```

### 3. Run sign-off discipline

Per CLAUDE.md sign-off section:
```bash
git status                              # clean
git log --oneline @{u}..HEAD            # empty (all commits pushed)
git fetch origin && git log --oneline main..HEAD
# If branch has commits not on main, do NOT merge yourself.
# Lead Dev runs the post-execution audit before merge.
```

**You do NOT merge to main.** Lead Dev runs the post-execution audit on your work, then PM approves, then merge happens. This is the multi-agent verification gate.

### 4. Report ready-for-review

Post on #1053:

```markdown
#1053 ready for Lead Dev post-execution audit + PM review.

- Branch: `claude/1053-standup-test-migration` at `<commit>`
- Per-phase commits:
  - Phase 1: `<hash>` test_conversation_handler.py
  - Phase 2: `<hash>` test_standup_routing_585.py
  - Phase 3: `<hash>` test_standup_suspend_resume_889.py + bind_session_id coverage
  - Phase 4: `<hash>` adapter test (or "skipped — no file found")
- Standup directory: N/N passing (was M/M pre-migration; delta justified if non-zero)
- _conversations access points: 0
- Postgres-down sanity: green
- Touched-area regression: clean (or pre-existing failures listed: #X, #Y)
- bind_session_id E2E: covered by `<test names>`

Awaiting Lead Dev audit + PM approval.
```

## STOP Conditions (apply throughout)

You MUST STOP and report to Lead Dev (via issue comment) before continuing if any of these occur:

1. **Fake API surface gap**: a test needs a manager method or behavior the Fake doesn't provide → file as separate issue, do NOT extend the Fake
2. **Test asserts on internal state with no public-API equivalent**: file + escalate
3. **More than 5 tests become obsolete during migration**: rethink scope with Lead Dev/PM
4. **Production code in `services/standup/` looks like it needs to change**: NOT in scope, flag for separate issue
5. **Touched-area regression introduces new failures (not pre-existing #1054/#1056/#1057)**: investigate before continuing
6. **Cross-cutting structural issues** in a target file beyond mechanical async conversion: STOP
7. **Cross-agent git collision** (parallel agent on same branch/files): STOP, surface, do NOT force-push
8. **Test count drops more than ±2 from baseline without explicit per-test justification**: STOP
9. **Reference impl `test_conversation_state.py` regresses**: infrastructure broken, STOP
10. **`POSTGRES_PORT=99999` test reveals real DB connection attempts**: the Fake or mocking is leaky, STOP
11. **You discover the audit-cascade prep was wrong about something fundamental**: STOP, do NOT improvise; surface to Lead Dev

When stopped: post a clear comment on #1053 with:
- What you found
- Why it's blocking
- Options you see
- Wait for Lead Dev or PM decision

## Architecture Boundaries (per gameplan)

**You may modify**:
- The 3 (or 4) target test files
- Test-only imports

**You MUST NOT modify**:
- `services/standup/conversation_manager.py`
- `services/standup/conversation_handler.py`
- `services/process/adapters.py`
- `services/intent/intent_service.py`
- `tests/unit/services/standup/_fake_conversation_manager.py` (the Fake itself — extending it is a separate issue per STOP condition #1)
- `tests/unit/services/standup/test_conversation_state.py` (already migrated in #1052 Phase 2)
- Any non-test production code

If you think one of these needs to change, STOP. That's a sign the audit-cascade prep missed something, and you should surface rather than improvise.

## Evidence Format

For each phase, your PR comment / session log entry should include:

```bash
$ pytest tests/unit/services/standup/test_conversation_handler.py -q 2>&1 | tail -3
========================== N passed in X.XXs ==========================
```

For verification:
```bash
$ grep -rn "manager\._conversations\|\._conversations\b" tests/unit/services/standup/
(empty)
$ POSTGRES_PORT=99999 pytest tests/unit/services/standup/ -q 2>&1 | tail -3
========================== N passed ==========================
```

## Self-Check Before Claiming Complete

Before posting "ready for review", confirm:
- [ ] All 4 (or 3 if Phase 4 skipped) target files have committed migration
- [ ] `pytest tests/unit/services/standup/` is fully green
- [ ] `grep -rn "manager\._conversations" tests/unit/services/standup/` is empty
- [ ] Postgres-down sanity is green
- [ ] Touched-area regression has no NEW failures (pre-existing OK to enumerate)
- [ ] Per-phase commits exist (or one consolidated commit if work was small)
- [ ] Branch pushed to origin
- [ ] No production code changed
- [ ] Issue comment posted with evidence
- [ ] You have NOT merged the branch (Lead Dev does the post-execution audit first)

## Anti-Patterns (DO NOT DO)

- ❌ Do not extend `FakeStandupConversationManager` on the fly. If a test needs something the Fake doesn't have, STOP.
- ❌ Do not modify production code "while you're in there" — out of scope.
- ❌ Do not skip the Postgres-down sanity check ("the tests pass on my machine" isn't enough — the AC is no DB connections).
- ❌ Do not merge to main yourself. Lead Dev audits, PM approves, then merge.
- ❌ Do not silence pre-existing failures by deleting them. Pre-existing means filed in another ticket; if the failure is new, STOP.
- ❌ Do not write new tests beyond the bind_session_id coverage in Phase 3 (the migration is mechanical; new coverage is a separate issue).

## Reference docs to read if needed

- Issue: `gh issue view 1053`
- Gameplan: `dev/2026/05/06/1053-gameplan.md`
- Manager surface: `services/standup/conversation_manager.py`
- Fake surface: `tests/unit/services/standup/_fake_conversation_manager.py`
- Reference impl: `tests/unit/services/standup/test_conversation_state.py`
- InsightJournal precedent: `tests/unit/services/mux/_fake_insight_journal.py`
- CLAUDE.md (worktree, sign-off, evidence discipline)
- Pattern-049 audit cascade

## Final reminder

The audit cascade was prepped tonight (2026-05-06) with three explicit gates. The plan is solid. Your job is execution + reporting. If reality contradicts the plan, **STOP**. The cost of stopping is small; the cost of improvising on a multi-agent project is large.

# === SUBAGENT PROMPT ENDS ===

---

## Lead Dev's notes (NOT part of subagent prompt)

### Deployment instructions

When ready to deploy, Lead Dev:

1. Creates the worktree branch:
   ```bash
   git checkout main && git pull origin main --ff-only
   git checkout -b claude/1053-standup-test-migration
   git push -u origin claude/1053-standup-test-migration
   ```

2. Invokes the subagent with the prompt (everything between `# === SUBAGENT PROMPT BEGINS ===` and `# === SUBAGENT PROMPT ENDS ===`).

3. After subagent reports complete: runs the **post-execution audit** at `dev/YYYY/MM/DD/1053-execution-audit.md` (verifies plan compliance), then escalates to PM for approval.

### Post-execution audit checklist (Lead Dev's own work, not the subagent's)

- [ ] Verify subagent stayed within Architecture Boundaries (no production-code changes)
- [ ] Verify all STOP conditions were respected
- [ ] Verify evidence claims by re-running pytest + grep + Postgres-down
- [ ] Verify per-phase commits exist with sensible messages
- [ ] Verify no `_conversations` access remaining
- [ ] Verify bind_session_id E2E coverage exists
- [ ] Cross-reference subagent's reported test counts against pre-migration baseline
- [ ] Confirm subagent did NOT merge to main (sign-off discipline)
- [ ] Compile final evidence + post on #1053 for PM approval
