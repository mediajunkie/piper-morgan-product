# 2026-10-02 10:00 — Coding Agent (prog), Sonnet 5 — #1595 Phase 3 sixth deletion: PRIORITY_PATTERNS

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`). Do NOT git add/commit — Lead commits by explicit pathspec after review.

## Task

GitHub issue #1595 (Inversion, epic 0 unit 5 — Phase 3 deletion ratchet). Sixth deletion: `PRIORITY_PATTERNS` (47 literals) in `services/intent_service/pre_classifier.py`. Destination: `get_top_priority`, a FLOOR-disposition action. Template: fifth deletion (`GITHUB_QUERY_PATTERNS`, commit `cf0a0ee052` — NOT `c49c5c82b2` as the dispatch said; that SHA is an unrelated merge commit. The real fifth-deletion product commit is `cf0a0ee052`, test-conversion sibling `e79b8382dd`).

New this list: condition (d) — two rows OK because surface 2 (LLM classifier) reaches the same FLOOR category in 5/5 frozen probe samples, per Arch's 2026-10-02 ruling. Ledger needs a new `surface2_verified_at_deletion` key; gate's `check_deleted_entry_non_regression` needs a new sibling branch (documented, minimal) accepting such a phrase as OK iff still UNCLAIMED post-deletion.

## BEFORE

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list PRIORITY_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo
```

```
corpus denominator: 382 rows total = 167 claimed + 215 unclaimed

## PRIORITY_PATTERNS
literals: 47  |  rows claimed: 42/382
verdict: GO (deletable) — deleting removes 47 literals: ceiling 376 -> 329
```

42/42 rows `[OK]`, 0 `[FAIL]` (confirmed via grep). Two rows carry condition (d) reasoning verbatim:
- `"what are my focus areas this sprint"` -> MISMATCH (route=get_contextual_guidance) but the destination is reached by category and surface 2 reaches the same floor (PRIORITY) in 5/5 probe samples — the pattern is not load-bearing
- `"what's my focus this week"` -> MISMATCH (route=week_calendar) but the destination is reached by category and surface 2 reaches the same floor (PRIORITY) in 5/5 probe samples — the pattern is not load-bearing

5 literals flagged "needs a corpus row before deletion" (unexercised) — not a [FAIL], same shape as prior deletions' residual-unexercised-literal notes.

Literal count confirmed: `pattern_literal_counts.total_literal_count()` → 376 (pre-deletion); `per_list_literal_counts()["PRIORITY_PATTERNS"]` → 47. `awk`+`grep -c '^\s*r"'` over the class block also → 47.

Ceiling confirmed: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` = 376 (pre-deletion).

## Plan

1. Build per-row ledger data via `gate.build_census`/`claim_for_phrase`/`row_disposition` (reuse, no hand transcription).
2. Record the two condition-(d) rows under `surface2_verified_at_deletion`.
3. Tombstone `PRIORITY_PATTERNS = []` with dated comment block.
4. Add sibling branch to `check_deleted_entry_non_regression` for `surface2_verified_at_deletion`-documented phrases (OK iff still unclaimed).
5. Post-deletion reabsorption check for all 42 phrases.
6. Ledger entry (7th), ceiling 376->329, rename ledger-count test to "seven", add non-regression pin for the new branch.
7. Run full required test scope, convert broken pins (never delete), ruff format/check.
8. Doc + dated-scope-doc updates.

(Log continues below as work proceeds.)

## Work done

1. **Tombstoned `PRIORITY_PATTERNS = []`** (`services/intent_service/pre_classifier.py`) with a
   dated comment block (date, ref 1595, sixth deletion, 47 literals, gate quote, condition (d) for
   the two surface-2-verified rows). One-line dead-code comment added at the claim branch (~1781).
   `detect_multiple_intents`'s table entry left untouched. Literal count confirmed post-deletion:
   `total_literal_count()` → 329 (376 − 47).

2. **Ledger entry (7th)** appended to `scripts/inversion_phase3_deleted_patterns.json`, built
   programmatically from `gate.build_census`/`claim_for_phrase`/`row_disposition` (no hand
   transcription) — fields: `list`, `deleted_on`, `literals`, `rows_claimed_at_deletion` (42),
   `verdict_report` (13 files, each phrase's actual source report confirmed by direct parse, not
   guessed), `expected_ops`, `expected_op_by_phrase`, `shadowed_literals` (5, per-literal
   shadowed-vs-never-exercised account, verified by regex probe against the corpus + sibling
   literals), `misserved_at_deletion` (2: "show priorities for this sprint", "not sure what to do
   about this"), **`surface2_verified_at_deletion`** (NEW key, 2 rows: "what are my focus areas
   this sprint", "what's my focus this week" — each `{probe_report, samples: "5/5", served:
   "anthropic:claude-sonnet-4-6"}`, read directly from `inversion-phase3-surface2-floor-probe-2026-
   10-02-n5-anthropic.md`, the first-listed/first-matching report per `SURFACE2_FLOOR_PROBES`'
   order), `known_reabsorptions` (`{}` — zero reabsorptions found), `note`.

3. **Gate script change** (`scripts/inversion_phase3_deletion_gate.py`,
   `check_deleted_entry_non_regression`): added the fourth documented-shape sibling branch,
   `surface2_verified_at_deletion` — OK iff the phrase is still UNCLAIMED post-deletion (same
   narrower, cheaper re-verified invariant `misserved_at_deletion` already uses; condition (d)'s
   original N=5 probe proof is a one-time GO-time fact never re-derived here, since this function
   doesn't thread `phrase` into its own `row_disposition` re-proof call). Docstring extended with
   the fourth shape's full account. Minimal, documented, ~10 lines of code + ~20 lines of
   docstring.

4. **Real-ledger non-regression check**: all 7 entries (REMINDER_PATTERNS,
   REMINDER_QUERY_PATTERNS, TODO_QUERY_PATTERNS, CALENDAR_QUERY_PATTERNS, TEMPORAL_PATTERNS,
   GITHUB_QUERY_PATTERNS, PRIORITY_PATTERNS) pass `check_deleted_entry_non_regression` under
   `CURRENT_LIVE_CATEGORIES` — confirmed via direct script run, not inferred from the pytest pin
   alone.

5. **Post-deletion reabsorption check**: ran `claim_for_phrase` for all 42 phrases against the
   live, tombstoned `PreClassifier`. **Zero reabsorptions** — STATUS_PATTERNS, GUIDANCE_PATTERNS,
   TODO_COMPLETE_PATTERNS, ANALYSIS_PATTERNS specifically checked (per dispatch's watch-list), none
   reclaim any of the 42 phrases.

6. **`--all` gate (AFTER)**: `PRIORITY_PATTERNS 0 0 NO ROWS`; corpus denominator unchanged at 382
   = 125 claimed (was 167, −42, the full claimed count — no partial reabsorption) + 257 unclaimed.

7. **Ceiling**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 376 → 329, dated comment
   block added (`tests/test_architecture_enforcement.py`).

8. **`tests/unit/test_inversion_phase3_deletion_1595.py`** updates:
   - Module docstring extended: SEVEN real entries, the fourth documented shape
     (`surface2_verified_at_deletion`) explained.
   - `test_real_ledger_has_the_first_six_deletions` → renamed `..._seven_...`, set extended with
     `PRIORITY_PATTERNS`, docstring updated.
   - **Two broken fixtures found and converted** (PRIORITY_PATTERNS had been the "still-claimed"/
     "surviving-list" fixture for three synthetic non-regression tests, written when TEMPORAL_
     PATTERNS' own deletion broke the ORIGINAL CALENDAR-based fixtures — the same cascade,
     recurring a second time):
     - `test_fails_when_phrase_is_claimed_by_a_surviving_list`: was `PRIORITY_PATTERNS`/"what
       should I do next" (now unclaimed). **Checked empirically**: no surviving list besides
       STATUS_PATTERNS claims ANY floor-expected corpus row today — but per the dispatch's own
       swap-avoidance rule (STATUS/GUIDANCE are next scheduled for deletion), I did NOT swap to
       STATUS_PATTERNS. Found a non-STATUS/GUIDANCE alternative: a real `expected: "plan"` corpus
       row (the #1606 two-op plan row) that `SET_DEFAULT_REPO_PATTERNS` claims as
       `set_default_repo` — `row_disposition` treats `"plan"` identically to `"floor"` in every
       branch this shape exercises (verified directly, both with-doc and without-doc variants).
       Swapped all three affected tests (this one, `test_passes_for_a_floor_expected_phrase_
       reclaimed_but_documented_disagreeing`, `test_fails_for_an_undocumented_reclaim_even_when_
       independently_safe`) to this SET_DEFAULT_REPO_PATTERNS/plan-row shape.
     - `TestPriorityPatternsVerdictIsReported` (verdict-reporting mechanism test, previously
       swapped to PRIORITY_PATTERNS after TEMPORAL's own fourth-deletion breakage): swapped again
       to `REPO_MANAGEMENT_PATTERNS` (2 claimed rows, GO) — again avoiding STATUS/GUIDANCE.
       Class docstring updated to explain the two swaps.
   - **New pins added**: `test_passes_for_a_surface2_verified_phrase_still_unclaimed` /
     `test_fails_for_the_same_phrase_without_the_surface2_documentation` (the new gate-script
     branch, using the real "what are my focus areas this sprint" row — verified unclaimed and
     MISMATCH beforehand); `test_priority_patterns_now_claims_zero_rows` (mirrors
     `test_temporal_patterns_now_claims_zero_rows`).
   - 39/39 tests in this file pass after conversion.

9. **Other broken pins found via the full required-scope run (5 failures on first pass) — all
   converted, never deleted**:
   - `test_contextual_query_handlers.py::test_priority_patterns_still_work` (5 phrases) — converted
     "matches + correct action" to "does not match"; no routes-survive pin added (`get_top_priority`
     has NO WorkflowEntry — confirmed via `get_action_workflows()` — so the Inversion never
     dispatches it by name; once surface 1 declines the phrase reaches the floor by CATEGORY
     through the LLM classifier, nothing a stubbed-router pin can prove).
   - `test_todo_query_handlers.py::test_next_todo_query_variants` — this test's own prior docstring
     documented the SECOND deletion's sibling-reabsorption finding ("what should I do next" claimed
     by PRIORITY_PATTERNS' own pre-existing literal). With PRIORITY_PATTERNS now gone, that sibling
     is gone too — genuinely unclaimed for the first time. Converted to pin the decline (same
     no-WorkflowEntry rationale); left the IntentCategory/assert_inversion_routes imports in place
     (still used by the file's other `list_todos_query` assertions in the same function).
   - `test_spend_free_canonical_ratchet_1818.py` — `("PRIORITY", "get_top_priority")` removed from
     `PAIR_MESSAGES` (same idiom as the fourth deletion's `("TEMPORAL", "get_current_time")`
     removal). Added a NOTE explaining this is the simpler case (already a measured-`SPENDS` pair,
     never `SPEND_FREE`, so nothing the #1818 gate protects actually changes) and flagging
     (not resolving) whether the action is reachable via the LLM classifier's own re-categorization.
   - `test_inversion_split_stand_down_1896.py` — THIRD swap of `SPLIT_TURN` in this epic (second
     deletion → TODO; fourth deletion → TEMPORAL; now sixth → PRIORITY). "give me my standup and
     what should i do next" degraded to a single STATUS claim. Swapped to "give me my standup and
     what branch are we on" (STATUS_PATTERNS + LOCAL_GIT_STATUS_PATTERNS, confirmed splitting into
     exactly 2 intents — verified directly) — avoided STATUS/GUIDANCE for the SECOND half per the
     swap-avoidance rule.
   - `test_pre_classifier.py::test_priority_next_patterns_not_greedy` — first two of three
     assertions (PRIORITY-expecting) converted to decline; third (STATUS, unaffected) unchanged.

10. **Full required-scope test run** (`tests/unit/services/intent_service/` +
    `tests/unit/services/test_pre_classifier.py` + `tests/unit/test_inversion_phase3_deletion_
    1595.py` + `tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
    `tests/test_architecture_enforcement.py` + the #1897 e2e shape pin): **5136 passed, 1 xfailed,
    0 failed** (confirmed on a clean re-run after all conversions, not just the first pass that
    found the 5 failures).

11. **`scripts/run-sweep.sh ratchets`**: 1 PRE-EXISTING failure, `test_todo_marker_ratchet` (count
    36 vs ceiling 35) — independently re-verified: `grep -Hn` for the same marker regex against
    every file touched this unit found exactly 2 hits, both in `pre_classifier.py`
    ("# Todo queries", "# Todo patterns" — pre-existing comment headers, confirmed via `git diff`
    showing zero changes to those lines), and both are outside the ratchet's own scan scope
    (`services/`+`web/` only — these ARE in `services/`, but `git diff` confirms they predate this
    session entirely and were already counted in the frozen baseline of 36 before I touched
    anything). 72 passed, 1 xfailed otherwise. Not fixed — out of scope per the ratchet's own
    guidance, same as the fifth deletion found and left.

12. **`ruff format` + `ruff check --fix`** on all 9 touched `.py` files: 0 changes needed (all
    already clean), 0 lint errors. JSON ledger file validated with `python3 -c "import json;
    json.load(...)"`.

13. **Docs**: `docs/internal/architecture/current/intent-routing-stack.md` "Sixth deletion"
    subsection appended (BEFORE/AFTER gate quotes, condition-(d) detail, all 6 converted test files
    with per-file rationale, ceiling arithmetic, final pass/fail counts). `dev/2026/09/25/inversion-
    epic0-remaining-scope-2026-09-25.md` dated entry appended (same structure as the fifth
    deletion's).

## Discovered work (flagged, not resolved — no bd/gh tool access in this session)

1. Same shape as the fifth deletion's finding #1: whether `get_top_priority` is reachable AT ALL
   via the LLM classifier's own re-categorization (now that no surface-1 pattern can ever produce
   it deterministically) is outside the #1818 spend-free ratchet's step-1 contract — flagged in
   that test file's NOTE, not resolved here.
2. `test_todo_marker_ratchet` pre-existing ceiling breach (36 vs 35) — unrelated to this unit,
   confirmed independently (see item 11 above).

Neither required touching product code beyond the one gate-script branch this dispatch asked for.

## STOP conditions checked — none triggered requiring escalation

- Gate read GO before starting: confirmed (BEFORE section above).
- No reabsorption disagreed with a ruled op: zero reabsorptions found at all.
- No test required product-code changes beyond the one gate-script branch.
- The three synthetic non-regression fixtures that HAD only STATUS_PATTERNS as a same-shape
  surviving-list candidate were resolved via an alternative (SET_DEFAULT_REPO_PATTERNS' "plan"-
  typed row) rather than guessed past — documented in detail in item 9 above and in the test
  docstrings themselves, so this is reported, not silently decided.

## Verified how

- **Method**: `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list PRIORITY_PATTERNS
  --live ...` (BEFORE) and `--all --live ...` (AFTER), both re-run this session and quoted above;
  `venv/bin/python -m pytest tests/unit/services/intent_service/ tests/unit/services/test_pre_
  classifier.py tests/unit/test_inversion_phase3_deletion_1595.py tests/unit/test_inversion_phase3_
  surface2_floor_1595.py tests/test_architecture_enforcement.py "tests/e2e/test_1897_two_part_turn_
  live.py::test_shape_is_the_1897_shape_before_spending" -q --maxfail=1000` (full required scope,
  two full runs — first found 5 failures, second confirmed 0 after conversion);
  `scripts/run-sweep.sh ratchets`; `venv/bin/ruff format`/`ruff check --fix` on all touched files;
  direct Python probes (`claim_for_phrase`, `check_deleted_entry_non_regression`,
  `pattern_literal_counts.total_literal_count()`) for every factual claim in this log.
- **Layer**: deterministic/unit — no LLM calls anywhere in this unit. Every router verdict
  consulted is a frozen, already-scored report (including both N=5 surface-2 probe reports read
  directly, not assumed); every test uses a monkeypatched stub, never a live LLM call.
- **Denominator**: full required test scope (5137 test items: 5136 passed + 1 xfailed), not a
  subset; all 42 PRIORITY_PATTERNS-claimed corpus rows accounted for in the ledger; all 7 ledger
  entries re-verified against non-regression, not just the new one.
