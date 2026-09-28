# 2026-09-28 0650 — prog (Coding Agent) — #1595 Phase 3, second deletion: TODO_QUERY_PATTERNS

**Role**: prog (Coding Agent), model Sonnet 5. Dispatched by Lead Developer, in the Lead's
worktree (`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`).
No git index touched at any point (per dispatch instruction — no staging/commit performed).
No LLM calls anywhere in this unit; no flag/env changes.

## Task

Phase 3's second deletion of the #1595 Inversion epic-0 unit 5: delete `TODO_QUERY_PATTERNS`
(10 literals) from `services/intent_service/pre_classifier.py`, following the exact procedure
the first deletion (REMINDER_PATTERNS + REMINDER_QUERY_PATTERNS, commits `eb9f85f119`/`cb52ed54d4`)
established, plus handle two new wrinkles: (a) this entry's `expected_ops` has TWO members
(`list_todos_query`, `get_top_priority` — the ruled destination for "what should I do next"),
and (b) convert every surface-1 pin the deletion breaks, including a multi-intent split-mechanism
test file the first deletion never had to touch.

## Read first

- `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (full "First deletion"
  subsection + the #1899 fifth-consumer paragraph)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress log)
- First deletion's commits: `eb9f85f119` (mechanics — tombstone form, ledger shape),
  `cb52ed54d4` (carrier test conversions)
- `scripts/inversion_phase3_deleted_patterns.json` (ledger entry shape)
- `tests/test_architecture_enforcement.py` (CEILINGS arithmetic comment,
  `phase3-deletion-ledger` resolver)
- `tests/unit/services/intent_service/_inversion_pin_helper.py` (shared stub helper)
- `services/intent_service/inversion_live.py::read_op_claims_turn` (#1899)
- `docs/internal/architecture/current/inversion-phase3-todo-query-rescore-2026-09-27.md` (the
  "what should I do next" → get_top_priority ruling, commit `657b4fc0c0`)

## Gate before deletion

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TODO_QUERY_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal
```
→ `verdict: GO (deletable) — deleting removes 10 literals: ceiling 558 -> 548`, 11/11 claimed
rows all MATCH/agreeing-REVIEW, "pattern->corpus conversion: every literal in this list is
exercised by >=1 corpus row." Matched the dispatch prompt's expected numbers exactly.

## What I did

1. **Tombstoned `TODO_QUERY_PATTERNS`** in `pre_classifier.py`: `= []  # type: List[str]`, same
   comment form as the first deletion (cites the deposits report + the todo-query rescore report
   + the 09-25 full report). `_todo_query_match` (the consumer) survives unchanged.
   `RESTORATIVE_ASK_BLOCKERS` — whose ONLY consumer is `_todo_query_match` — is now INERT for the
   same reason `REMINDER_QUERY_BLOCKERS` went inert in the first deletion; annotated with an
   "INERT since 2026-09-27" comment. `DESTRUCTIVE_ASK_BLOCKERS` stays live (shared by other
   lanes). No other `*_PATTERNS` list touched.

2. **Ledger entry** in `scripts/inversion_phase3_deleted_patterns.json`: all 11
   `rows_claimed_at_deletion` phrases, `verdict_report` lists all three reports,
   `expected_ops: ["list_todos_query", "get_top_priority"]`.

   **Precision fix, found by inspecting the checker rather than trusting it** (per the dispatch
   prompt's explicit ask): `check_deleted_entry_non_regression`'s un-asserted-REVIEW fallback
   previously accepted a route iff it matched **any** of `expected_ops` — correct for every
   single-op entry, but for a two-op entry that "any" check could in principle accept a REVIEW
   row that drifted to the OTHER destination it was never actually scored against. Added
   `expected_op_by_phrase` to the ledger entry (per-row precision) and a new
   `expected_op_for_phrase()` function in `scripts/inversion_phase3_deletion_gate.py` with
   explicit precedence: (1) the corpus row's own asserted `action:` expectation, (2) the entry's
   `expected_op_by_phrase` map, (3) `expected_ops` only when it has exactly one member. Both
   `check_deleted_entry_non_regression` and the reachability ratchet's `phase3-deletion-ledger`
   resolver (`tests/test_architecture_enforcement.py::_phase3_ledger_resolve`) now consult this
   shared helper instead of their respective old logic — the ratchet's old form
   (`if len(expected_ops) != 1: continue`) would have SILENTLY REFUSED to resolve every row in
   this entry, including the 10 unambiguous `list_todos_query` ones, breaking the `page:/todos`
   POINTER ("show me my todos", `chat_pointers.py`) on the reachability ratchet — verified this
   would have been a real regression, not a hypothetical, by tracing the exact code path.

3. **CEILINGS arithmetic**: `558 → 548` (558 − 10 = 548), comment updated, confirmed via
   `pattern_literal_counts.total_literal_count()` → 548.

4. **Sibling-takeover finding, named not hidden** (per task item 6): post-deletion census
   measured corpus claimed dropping **110 → 100**, not 110 → 99. "what should I do next" is now
   claimed DIRECTLY by `PRIORITY_PATTERNS` — verified via `git blame` that
   `r"\bwhat should i do next\b"` has been in `PRIORITY_PATTERNS` since commit `33f3a43ad42`
   (2026-03-22), six months predating this deletion — it was DEAD CODE for this exact phrase the
   whole time, shadowed by `TODO_QUERY_PATTERNS`'s earlier position in `pre_classify`'s
   if-chain. Once emptied, the shadow lifted, and `PRIORITY_PATTERNS` claims it landing on the
   SAME `get_top_priority` destination the rescore ruling established (benign, verified-agreeing,
   not a routing regression). Documented as a new `known_reabsorptions` ledger field (phrase →
   reclaiming list + rationale), and `check_deleted_entry_non_regression` extended to treat a
   reclaim as OK **only** when (a) the phrase is named in `known_reabsorptions`, (b) the
   reclaiming list matches the one named there, and (c) the reclaiming list's CURRENT action
   still agrees with the phrase's own target op — any other reclaim (different list, undocumented
   phrase, or a documented one whose answer has since drifted) still fails loud, unchanged. No
   other sibling reabsorbed any of the other 10 phrases (confirmed: `lists with ZERO corpus
   claims` includes TODO_QUERY_PATTERNS itself, and none of the 10 unambiguous phrases appear
   under any other list in the `--all` census).

5. **Converted every broken surface-1 pin** (ran `pytest tests/unit/services/intent_service/
   tests/unit/services/intent/` after emptying the list; 34 failures on the first pass). Every
   failure converted, never deleted:

   - `tests/unit/services/intent_service/test_reminder_query_preclassifier_1521.py::
     test_todo_listing_unchanged` → two-part decline+inversion-routes idiom (via
     `_inversion_pin_helper.assert_inversion_routes`, flag `read_status,create_reminder`),
     mirroring the file's own existing reminder-query conversion.
   - `tests/unit/services/intent_service/test_todo_completion_lifecycle.py::
     TestCompletionPreClassifierPatterns::test_show_completed_todos_pattern` → same idiom.
   - `tests/unit/services/intent_service/test_todo_query_handlers.py::
     TestPreClassifierRoutingIntegration` (4 tests) → all converted to decline+inversion-routes;
     `test_next_todo_query_variants` handles "what should I do next" as a SEPARATE, still-claimed
     assertion (PRIORITY_PATTERNS, `get_top_priority`, no router consult needed) after the first
     pytest pass surfaced that it's genuinely claimed now (the sibling-takeover finding above),
     not unclaimed as I'd initially written.
   - `tests/unit/services/intent_service/test_todo_listing_declines_write_asks_1881.py::
     TestReadsKeepTheirClaim` (6 phrases × 2 surfaces = 12 tests) → `TestWriteAsksDecline`
     unaffected (empty list still claims nothing); `TestReadsKeepTheirClaim` converted to
     decline (surface 1) + a new `test_inversion_routes_the_read` parametrized class proving the
     legitimate READ phrases still route to `list_todos_query` downstream — the WRITE-vs-READ
     *guard predicate* itself (`RESTORATIVE_ASK_BLOCKERS`/`DESTRUCTIVE_ASK_BLOCKERS` inside
     `_todo_query_match`) is now structurally INERT (documented in the module docstring), so this
     preserves the file's semantic claim without pretending a dead guard still does the work.
   - `tests/unit/services/intent_service/test_task_clarify_1654.py::TestTaskTurnHandlerSeam::
     test_preclassifier_claim_releases_without_calling_router` → swapped "show my todos" (no
     longer claimed) for "give me my standup" (STATUS_PATTERNS, unaffected) — same idiom the
     first deletion used when swapping "list my reminders" out. Updated `todo_handlers.py`'s
     `handle_reminder_task_turn` docstring (stale example list) in the same commit-worth of work.
   - `tests/unit/services/intent_service/test_ftux_interview_1688.py::
     TestHandleFtuxInterviewTurn` (2 tests) → same swap to "give me my standup" (this file had
     ALREADY swapped once, from "list my reminders" to "show my todos", after the first
     deletion — this is the second swap, documented inline).
   - `tests/unit/services/intent_service/test_inversion_split_stand_down_1896.py` (2 tests) →
     `SPLIT_TURN`/`SINGLE_TURN` swapped from a todos+temporal pairing to "give me my standup and
     what time is it" (STATUS + TEMPORAL, unaffected) — same genuine-2-claim-split property.
   - `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py` (10 tests,
     the multi-intent SPLIT mechanism file — the deepest conversion): all four turn constants
     (`TURN_READ_FIRST`/`TURN_ISSUES_FIRST`/`TURN_TWO_NAMED` collapsed onto the same still-
     splitting phrase, "what are my open issues and what did we create this session"
     — GITHUB_QUERY_PATTERNS + SESSION_ACTIVITY_QUERY_PATTERNS, unaffected by the deletion;
     `TURN_UNRAILED_HALF` → "... and what time is it"). Key insight verified empirically before
     converting: the STUBBED router (`_route_by_segment`) freely RENAMES a segment's dispatched
     action regardless of what surface 1 originally claimed for that segment — so
     `list_todos_query` (backed by the file's own `todo_boundary` fixture, which mocks
     `TodoManagementService`) is still reachable by REMAPPING a consulted segment, for every test
     except the ONE that specifically needs an UNCONSULTED "kept" surface-1 claim
     (`TestConsultDeclinedSibling::test_it_keeps_surface_ones_intent...`) — for that one I swapped
     which segment plays "kept" vs "consulted" (session_activity_query kept, unaffected by the
     deletion and already `sm`-fixture-backed; issues segment consulted into `list_todos_query`),
     avoiding any need to real-dispatch GitHub issue listing (no mocking exists for it in this
     file — would have been a real flakiness risk). All 10 tests pass; one extra fix needed after
     first run (`test_a_greeting_keeps_its_own_words...` — the greeting-prefixed segment boundary
     text differs slightly from the bare-message one, measured and pinned to the actual value).
     Also swapped 3 raw destructive-phrasing strings ("what are my todos and delete my hydrate
     reminder" etc.) that no longer produce their originally-asserted claim counts — verified new
     counts empirically before writing new assertions.
   - Confirmed OUT of scope / unaffected without changes: `test_preclaim_shadow.py::
     test_identity_reaches_telemetry_for_three_lists` (already converted in the first deletion,
     doesn't reference TODO_QUERY_PATTERNS); `test_silent_death_unswallow_1423.py` (builds Intent
     objects directly, bypasses pre_classify entirely); `test_original_message_1460.py`,
     `test_scope_guard_1772.py` (not in the failure list — verified their "show my todos"/"what's
     on my calendar" usages don't depend on surface-1 classification).

6. **Reachability ratchet**: confirmed via the `page:/todos` POINTER
   ("show me my todos" → `("query", "list_todos_query")`) that
   `TestChatPointersReachabilityRatchet` resolves it through `phase3-deletion-ledger` post-fix,
   not special-cased — this is the exact POINTER the old `len(expected_ops) != 1` bail would have
   broken.

7. **Docs**: `intent-routing-stack.md` gains a "Second deletion" subsection under Phase 3 (full
   account: gate evidence, ledger/checker precision fix, ceiling arithmetic, the sibling-takeover
   finding, carrier coverage). Scope doc
   (`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`) gets a new progress-log entry
   dated 2026-09-28.

8. **`ruff format` + `ruff check --fix`** on all touched `.py` files — 2 files reformatted
   (`scripts/inversion_phase3_deletion_gate.py`, `tests/unit/services/intent_service/
   test_todo_query_handlers.py`, formatting only), `ruff check --fix` clean on all 13 files.

## Test evidence

- `tests/unit/services/intent_service/ tests/unit/services/intent/` (full): **5039 passed, 1
  xfailed** (final run, post all conversions + ruff).
- `tests/test_architecture_enforcement.py`: **82 passed, 1 xfailed** (combined with the ledger
  test file in the same invocation — ceiling exact at 548, `TestChatPointersReachabilityRatchet`
  green).
- `tests/unit/test_inversion_phase3_deletion_1595.py`: green, `TestDeletedPatternListsLedger`
  updated pin (`test_real_ledger_has_the_first_three_deletions`, was
  `test_real_ledger_has_the_first_two_deletions`) — all 3 ledger entries pass non-regression,
  including TODO_QUERY_PATTERNS' one documented `known_reabsorptions` exception.
- `scripts/run-sweep.sh ratchets`: **73 passed, 1 xfailed** + mypy gate — "all 24 ratcheted codes
  at ceiling" (unchanged from baseline, total=1121).

## Gate output — before/after

**Before** (quoted in full above, "Gate before deletion"): GO, 11 rows claimed, 10 literals,
0 needs-a-corpus-row.

**After** (`--all`, same `--live` flag):
```
TODO_QUERY_PATTERNS  0  0  NO ROWS
...
total rows claimed: 100
lists with ZERO corpus claims (5): ... TODO_QUERY_PATTERNS ...
```
Claimed dropped **110 → 100** (not the naively-expected 110 → 99): 10 of the 11 phrases are
genuinely unclaimed; 1 ("what should I do next") is REABSORBED by `PRIORITY_PATTERNS` — a real,
pre-existing (six-months-old, verified via `git blame`) shadowed duplicate literal, now
documented as a `known_reabsorptions` ledger exception since its destination agrees with the
ruled expectation. No other phrase was reabsorbed by any sibling list.

## Verified how

**Method**: ran the deletion gate script directly (before and after emptying the pattern list),
ran the full `tests/unit/services/intent_service/` + `tests/unit/services/intent/` suite
(5039 passed/1 xfailed), the architecture-enforcement + ledger pin suite (82 passed/1 xfailed,
ceiling exact), and `scripts/run-sweep.sh ratchets` (73 passed/1 xfailed + mypy gate at ceiling) —
all commands quoted above with their actual output, this turn. **Layer**: deterministic layer
only (pre-classifier regex matching, corpus-row lookups, router-report table parsing) — every
router "verdict" consulted is a FROZEN, already-scored report or a monkeypatched stub in tests;
zero live LLM calls anywhere in this unit (self-confirmed by the deletion gate script's own
"NO LLM CALLS" design and by every converted test using `_inversion_pin_helper`'s stubbed
`ir.route`). **Denominator**: 34/34 broken tests converted (not a sample) across 8 test files;
110-row corpus census before, 100-row after, both counts read directly from the gate script's
own output, not estimated.

## Discovered work

One finding, reported not filed as a separate issue (per the task's own framing — "name it, a
finding not a failure to hide"): `PRIORITY_PATTERNS` has carried an identical, previously-dead
literal to one of `TODO_QUERY_PATTERNS`'s (`r"\bwhat should i do next\b"`) since 2026-03-22
(commit `33f3a43ad42`) — a genuine pre-existing shadowed-duplicate pattern across two lists,
invisible until the higher-precedence list was emptied. Documented in the ledger's
`known_reabsorptions` field and in `intent-routing-stack.md`'s "Second deletion" subsection;
benign (agrees with the ruled destination) so not filed as a bug.

## Files touched

- `services/intent_service/pre_classifier.py` — `TODO_QUERY_PATTERNS` tombstoned,
  `RESTORATIVE_ASK_BLOCKERS` inert-annotated
- `services/intent_service/todo_handlers.py` — stale docstring example list fixed
- `scripts/inversion_phase3_deleted_patterns.json` — new ledger entry (+
  `expected_op_by_phrase` + `known_reabsorptions`)
- `scripts/inversion_phase3_deletion_gate.py` — `expected_op_for_phrase()` added;
  `check_deleted_entry_non_regression` uses it + the `known_reabsorptions` exception
- `tests/test_architecture_enforcement.py` — CEILINGS 558→548;
  `_phase3_ledger_resolve` uses `expected_op_for_phrase` (no more `len(expected_ops)!=1` bail)
- `tests/unit/test_inversion_phase3_deletion_1595.py` — ledger-names pin updated
- `tests/unit/services/intent_service/test_reminder_query_preclassifier_1521.py`
- `tests/unit/services/intent_service/test_todo_completion_lifecycle.py`
- `tests/unit/services/intent_service/test_todo_query_handlers.py`
- `tests/unit/services/intent_service/test_todo_listing_declines_write_asks_1881.py`
- `tests/unit/services/intent_service/test_task_clarify_1654.py`
- `tests/unit/services/intent_service/test_ftux_interview_1688.py`
- `tests/unit/services/intent_service/test_inversion_split_stand_down_1896.py`
- `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py`
- `docs/internal/architecture/current/intent-routing-stack.md` — "Second deletion" subsection
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — progress log entry

No git add/commit/staging performed at any point (dispatcher instruction). Reporting back to
Lead via SubagentHandback.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (First
  deletion subsection — the worked-example procedure this session replicated); the first
  deletion's commits `eb9f85f119`/`cb52ed54d4` (tombstone form, ledger shape, test-conversion
  idiom); `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + prior
  progress entries, esp. the deposits-report row detail for TODO_QUERY_PATTERNS);
  `_inversion_pin_helper.py` (shared stub helper, reused verbatim).
- **Loaded but not referenced**: CLAUDE.md's mailbox/sign-off/worktree-model sections (this is a
  bounded prog dispatch inside an existing worktree, no mailbox write, no sign-off merge, no git
  index touched, per dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient; the one
  genuinely new thing (PRIORITY_PATTERNS' pre-existing duplicate literal) was found by direct
  investigation (git blame), not something a briefing doc should have pre-empted.
