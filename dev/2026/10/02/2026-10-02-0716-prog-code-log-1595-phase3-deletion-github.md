# 2026-10-02 07:16 — Coding Agent (prog), Sonnet 5 — #1595 Phase 3 fifth deletion: GITHUB_QUERY_PATTERNS

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`). Do NOT git add/commit — Lead commits by explicit pathspec after review.

## Task

GitHub issue #1595 (Inversion, epic 0 unit 5 — Phase 3 deletion ratchet). Fifth deletion: `GITHUB_QUERY_PATTERNS` (64 literals) in `services/intent_service/pre_classifier.py`. Template: fourth deletion (`TEMPORAL_PATTERNS`, commit `dfec3e908d`, 2026-10-01).

## BEFORE

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list GITHUB_QUERY_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo
```

```
corpus denominator: 382 rows total = 232 claimed + 150 unclaimed

## GITHUB_QUERY_PATTERNS
literals: 64  |  rows claimed: 66/382
verdict: GO (deletable) — deleting removes 64 literals: ceiling 440 -> 376

rows claimed: [66 rows, all [OK], 0 [FAIL]]
pattern->corpus conversion: every literal in this list is exercised by >=1 corpus row.
```

Full BEFORE text saved at `/tmp/before_gate_clean.txt` (not committed — reproducible by re-running the gate command above).

Literal count confirmed: `awk '/GITHUB_QUERY_PATTERNS = \[/,/^    \]/' services/intent_service/pre_classifier.py | grep -c '^\s*r"'` → 64.

Ceiling confirmed: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` = 440 (pre-deletion).

## Plan

1. Build per-row ledger data (rows_claimed_at_deletion, expected_op_by_phrase) by reusing `scripts/inversion_phase3_deletion_gate.py`'s own `build_census`/`claim_for_phrase`/`row_disposition` — no re-derivation, no hand transcription. Convention confirmed against precedent (REMINDER/TODO/CALENDAR/TEMPORAL entries): `expected_op_by_phrase[phrase]` = the corpus `expected` field's op when `action:X` (→ X) or `floor`/`plan` (→ literal), else (REVIEW / category:X) → the surface-1 claim's own action (since REVIEW-agrees means router route canonically equals claim action via `same_operation`).
2. Tombstone `GITHUB_QUERY_PATTERNS = []` with dated comment block, mirroring `dfec3e908d`'s TEMPORAL_PATTERNS tombstone shape.
3. One-line dead-code comment at the claim branch (~1532).
4. Post-deletion reabsorption check: run `claim_for_phrase` (via `pre_classify_with_pattern_list`) for all 66 phrases against the live (now-tombstoned) PreClassifier.
5. Ledger entry, ceiling update, test conversions, doc section.

## Code change made

- `services/intent_service/pre_classifier.py`: `GITHUB_QUERY_PATTERNS` emptied to `[]  # type: List[str]` with dated tombstone comment block (64 literals removed). One-line dead-code comment added at the claim branch (~1484). `detect_multiple_intents`'s table entry (~2059) left untouched per instruction ("stays").
- Literal count confirmed post-deletion: `pattern_literal_counts.total_literal_count()` → 376 (440 - 64).

## Reabsorption check (step 4)

Ran `claim_for_phrase` (via `pre_classify_with_pattern_list`) for all 66 claimed phrases against the live, now-tombstoned `PreClassifier`. Result: 65 genuinely unclaimed, **1 reabsorption**:

- `"any update on the next milestone"` → reclaimed by `STATUS_PATTERNS` (its own pre-existing `\bnext milestone\b` literal — git blame: commits `33f3a43ad4`/`dc467511eb`, #898/#1039 era, many months before this deletion). Claimed action: `get_project_status`. **AGREES** with the ruled destination (`get_project_status`, router MATCH@0.85) — same agreeing-reclaim shape TODO_QUERY_PATTERNS' PRIORITY_PATTERNS case established, not a new mechanism. No disagreement, no STOP condition.

Corrected the tombstone comment in pre_classifier.py (first draft wrongly said "0 reabsorptions" before I'd actually run the check — fixed to document the 1 found).

## AFTER gate (--all)

`corpus denominator: 382 rows total = 167 claimed + 215 unclaimed` (was 232 claimed + 150 unclaimed; 232-167=65 = 66 GITHUB rows minus 1 reabsorbed into STATUS_PATTERNS, which rose 51→52 claimed). `GITHUB_QUERY_PATTERNS  0  0  NO ROWS` confirmed.

## Ledger entry + ceiling

Appended 6th `DELETED_PATTERN_LISTS` entry (`GITHUB_QUERY_PATTERNS`) to `scripts/inversion_phase3_deleted_patterns.json`, built programmatically from `gate.build_census`/`claim_for_phrase`/`row_disposition` (no hand transcription) — script at `/private/tmp/.../scratchpad/build_github_ledger_rows.py` and `append_ledger_entry.py` (scratchpad only, not committed). `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` lowered 440→376 in `tests/test_architecture_enforcement.py`.

## Test conversion (step 7) — IN PROGRESS

First targeted run (`tests/unit/services/intent_service/` + ledger + enforcement + `test_pre_classifier.py`, no `-x`): **124 failed, 4992 passed, 1 xfailed** out of ~5117. Converting file by file, logging each as I go below.

### `test_acceptance_contract_1739.py` (1 failure, found via first default `--maxfail=1` run, fixed before the full sweep)
`TestConfirmSeamAdopted::test_state_question_rearms_visibly_never_silently` — `_arm_close_confirm`'s "close issue #108" no longer claims at surface 1 (`close_issue_query` has no live-rail `flip_group`, so there's no zero-LLM path either — discovered-gap, not resolved, same shape as TEMPORAL's "what time is it?"). Converted (not deleted): `_arm_close_confirm` now stubs `classify()` with a function that returns the canned `close_issue_query` Intent ONLY for the exact arm message "close issue #108" and raises the same "LLM boundary touched" AssertionError for any other message (preserving the explosive-LLM proof for every later message in both tests that use this helper). 78/78 pass after.

### `test_pre_classifier_milestones_releases_1039.py` (31 failures) + `test_pre_classifier_labels_branches_1040.py` (30 failures)
Both directly tested `PreClassifier._matches_patterns(..., GITHUB_QUERY_PATTERNS)` / `_get_github_action` -- now dead code (empty list). Converted every `test_positive_match`/`test_existing_patterns_unchanged` assertion from "matches + correct action" to "does not match" (decline), with a docstring citing the deletion. Added a new `TestInversionRoutesSurvive` class in each file with 2 representative `assert_inversion_routes` pins (stubbed router, no LLM) proving `list_milestones_query`/`list_releases_query`/`list_labels_query`/`list_branches_query` (all flip_group `read_status`, confirmed via direct probe of `get_action_workflows()`) are still reachable through the Inversion. `TestActionRegistry` (registry-only, unaffected) left untouched. 43/43 and 38/38 pass.

### `test_github_query_handlers.py` (12 failures)
`TestPreClassifierRoutingIntegration` (shipped/stale_prs/review_issue/close_issue/comment_issue "routes to QUERY" tests) and `TestListPRsPreClassifierRouting` (list_prs) -- same conversion (assert `result is None`). Added `TestGithubInversionRoutesSurvive` with 4 live-routes pins (shipped_query, stale_prs_query, review_issue_query [flip_group `read_referent`], list_prs_query -- all `read_status` except review_issue_query). close_issue_query/comment_issue_query excluded from the live-routes pin -- confirmed via direct probe (`get_action_workflows()`) that BOTH have `flip_group=None`, i.e. no registered live-rail key at all, so there is nothing for `assert_inversion_routes` to prove for them (discovered gap, documented in the class docstring, not resolved here). `test_get_github_action_returns_list_prs_query` untouched -- `_get_github_action` is a pure string-matching helper independent of the (now-empty) list, still dead-code-correct. 60/60 pass.

### `test_read_lane_destructive_greed_1756.py` (4 failures)
`TestGithubLaneDestructiveGreed1794.test_gated_rail_claims_keep_their_lane` (close/reopen) and `test_plain_reads_unchanged` (list_issues/stale_prs) -- converted to assert decline on both single- and multi-intent surfaces (the per-claim discrimination this class existed to test is now dead code -- nothing left to discriminate). Added `TestGithubPatternsNowDeclineAtSurfaceOne` with 2 live-routes pins for the plain-read actions (list_issues_query, stale_prs_query). `test_close_family_is_actually_gated_not_assumed` and `test_destructive_asks_fall_through_on_both_surfaces` untouched (unaffected -- registry-only / already-declining). 264/264 pass.

### `test_destructive_confirm_1190.py` (7 failures) + `test_confirm_crisp_accept_1650.py` (11 failures)
Both are end-to-end confirm-gate suites with an EXPLOSIVE-LLM `live_service` fixture, arming via a bare `process_intent(message="close issue #108"/"reopen issue #42", ...)` call with NO classify stub (this is exactly what GITHUB_QUERY_PATTERNS used to make deterministic for free). Added a shared `_stub_close_reopen_classify`/`_stub_close_classify` helper (same idiom as 1739's `_arm_close_confirm` fix): a `classify()` monkeypatch returning the canned `close_issue_query`/`reopen_issue_query` Intent for the exact arm message(s) this file sends, raising the same "LLM boundary touched" AssertionError for every other message -- so the rest of each test (yes/no/cancel/off-intent/#1631-prose/#1650-crisp-accept mechanics) is proved exactly as before. 28/28 and 65/65 pass.

### `test_consent_gate_1509.py` (1 failure) + `test_repo_wiring_1641.py` (2 failures)
Same explosive-LLM arm-step shape as 1190/1650: inline classify() stubs added for "close issue #108" (1509) and for "reopen issue #108"/"comment on issue #123..." (1641, via a shared `_stub_github_arm_classify(monkeypatch, service, keyword, action)` helper since this file's module docstring itself documents reopen/comment "ride the pre-classifier" for the arm turn). 118/118 and 38/38 pass.

### Single-failure files: `test_action_fabrication_1648.py`, `test_action_registry.py`, `test_drafted_issue_1571.py`, `test_drafted_issue_body_steal_1627.py`, `test_drafted_issue_subjectless_1630.py`, `test_reminder_clear_pick_target_1906.py`, `tests/unit/services/test_pre_classifier.py`
- 1648/1571/1627/1630: all four are the SAME off-intent shape ("close issue #108" abandons an armed draft and arms its OWN #1190 confirm) — same classify-stub idiom inlined per test. 50/50, 75/75 pass.
- `test_action_registry.py::test_single_intent_not_affected`: swapped example message "Close issue #42" -> "What branch are we on" (LOCAL_GIT_STATUS_PATTERNS, same QUERY category, unaffected). 89/89 pass.
- `test_reminder_clear_pick_target_1906.py::TestOffIntentReleases::test_unrelated_command_releases`: **DISCOVERED WORK, flagged not fixed in product code** — `_handle_pick_target_turn`'s #1899 "unrelated command releases the pick" discriminator (`services/intent_service/reminder_clear.py` ~1481) checks `PreClassifier.pre_classify(text) is not None` first, falling back to `read_op_claims_turn` (READ-only) second. With GITHUB_QUERY_PATTERNS gone, "close issue #108" passes NEITHER check (pre_classify declines; close_issue_query is destructive, not a READ op) — confirmed empirically: the discriminator now returns a "Still not sure which one" RE-ASK instead of releasing. This is live product behavior, not a test-fixture artifact. Converted the TEST (swapped example to "give me my standup", STATUS_PATTERNS, which still releases correctly) WITHOUT touching product code, per the dispatch's STOP condition for product-code-requiring fixes — but the underlying gap (no destructive/non-READ surviving pattern can trigger this release path any more) is real and belongs to the Lead/Arch to decide. 28/28 pass.
- `tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_current_time_still_routes_to_temporal`: **NOT caused by this deletion** — root cause is the FOURTH deletion (TEMPORAL_PATTERNS, commit `dfec3e908d`, 2026-10-01), confirmed via `git show HEAD:services/intent_service/pre_classifier.py` (TEMPORAL_PATTERNS was already `[]` before I touched anything today). This file sits outside the directory scope that commit's own "full suite" verification covered (`tests/unit/services/intent_service/` + `tests/unit/services/intent/`, not the sibling `tests/unit/services/` root) — a pre-existing gap surfaced only because today's dispatch's required run scope happens to include it. Converted anyway (decline + new `test_current_time_routes_live_via_inversion` live-routes pin, same idiom as the fourth deletion's own TEMPORAL conversions) rather than left red. 33/33 pass.

### `test_inversion_multi_intent_unit4_1595.py` (13 failures — the hardest conversion)
The file's three core test turns (`TURN_READ_FIRST`/`TURN_ISSUES_FIRST`/`TURN_TWO_NAMED`/`TURN_UNRAILED_HALF`) paired "what are my open issues" (GITHUB_QUERY_PATTERNS, list_issues_query) with "what did we create this session" (SESSION_ACTIVITY_QUERY_PATTERNS) — with GITHUB gone, the paired turn stopped splitting into two siblings at all (collapsed from 2 intents to 1, confirmed empirically), breaking the file's entire premise.
- Swapped the first segment to "what branch are we on" (`LOCAL_GIT_STATUS_PATTERNS`, action `local_git_status_query`, confirmed: still splits into 2 siblings, category QUERY, registered rail key with `effect=READ`). Updated the 3 `TURN_*` constants + `SEG_ISSUES_AND`, every `"list_issues_query"` expected-action assertion -> `"local_git_status_query"`, the greeting-prefix segment-boundary assertion (now the FULL phrase rides through unchanged, since LOCAL_GIT_STATUS_PATTERNS' literal requires the whole "what branch are we on" — no shorter partial match exists, unlike GITHUB's), and `_named_delete_target(SEG_ISSUES_AND)`'s expected output ("what are open issues" -> "what branch are", verified via direct call).
- Renamed the `todo_boundary` fixture's first row from `_todo("open issues")` to `_todo("branch check")` (verified via `fuzzy_todo_match_score("what branch are", "branch check")` = 0.33, above the 0.3 threshold, uniquely — "create session"/"hydrate" score 0) and updated the 6 downstream literal-text assertions (confirm-question copy, delete-target binding, post-delete reply text) to match.
- **One test needed a DIFFERENT swap, not the same one**: `test_the_destructive_phrasings_the_dispatch_named_do_not_split` relies on the #1794-family destructive-ask guard suppressing a READ claim when the destructive ask comes FIRST in the message — `LOCAL_GIT_STATUS_PATTERNS` is NOT a member of `_READ_LANE_GROUPS` (confirmed by inspection), so it does NOT get this suppression (measured: "delete my hydrate reminder and what branch are we on" still returns 1 intent, not 0, unlike the old GITHUB behavior). Used "give me my standup" (STATUS_PATTERNS, which IS a `_READ_LANE_GROUPS` member) for this one test's two inline phrasings instead, reproducing the exact suppression property; `get_project_status` has no WorkflowEntry (floor-routed) so this phrase is deliberately NOT reused for the rail-dispatchability tests.
- Also updated `test_surface_one_emits_no_write_or_destructive_sibling`'s two inline destructive-paired phrasings to the same "give me my standup" swap (not independently broken, but shares the stale "what are my open issues" literal — fixed for consistency since a currently-passing assertion would otherwise rest on the same now-dead claim).
32/32 pass after.

### `test_subsumption_1084.py` (4 failures)
The #1084 GITHUB-subsumes-STATUS collapse rule is now vacuous ("What's the next milestone?" only ever matched STATUS_PATTERNS now -- nothing left to subsume). Converted all 4 tests to pin the new reality (single-intent STATUS/get_project_status, not QUERY/list_milestones_query); swapped the pure-QUERY control case ("list milestones" -> "what branch are we on", its own GITHUB-based control no longer claims either). 6/6 pass.

### `test_inversion_counterfactual_1668.py` (2 failures)
`TestModeBranching::test_inversion_routed_turn_runs_counterfactual_not_reroute` and `TestLegsAndCost::test_deterministic_claim_spends_no_llm_call` both used "show my issues"/operation "list_issues" -- swapped to "what branch are we on"/"local_git_status" (local_git_status_query and local_git_status are registered aliases of the same rail entry_point, same canonical shape list_issues_query/list_issues had). Left the OTHER 5 occurrences of "show my issues" in this file untouched (not failing -- they test different properties that don't need a deterministic surface-1 claim, e.g. router-shadow-unchanged, flag-off short-circuit). 19/19 pass.

## Final verification

Full required scope (`tests/unit/services/intent_service/` + `tests/unit/test_inversion_phase3_deletion_1595.py` + `tests/test_architecture_enforcement.py` + `tests/unit/services/test_pre_classifier.py`): **5127 passed, 1 xfailed, 0 failed** (confirmed twice).

`scripts/run-sweep.sh ratchets`: 1 PRE-EXISTING failure, `test_todo_marker_ratchet` (count 36 vs ceiling 35) -- independently re-computed the exact same scan (services/+web/ .py files, excluding archive/__pycache__) and confirmed zero of the 36 hits are in any file this unit touched; the scan doesn't even look at tests/. 72 passed, 1 xfailed otherwise. Not fixed (out of scope -- "do the work, file an issue and reference it, or delete the stale marker" per the ratchet's own guidance, not a Phase 3 deletion task).

`ruff format` + `ruff check --fix` on all 23 touched .py files: 5 reformatted (whitespace only), all checks pass. Re-ran the full suite after reformatting: still 5127/5127 (one run picked up an UNRELATED flaky failure, `test_inversion_router_1595.py::TestRouteEnforcement::test_real_call_routes_within_grammar` -- this test makes a REAL live LLM call by its own docstring design ("One real Haiku-class call"), passed cleanly in isolation, not a file this unit touched).

`tests/e2e/test_1897_two_part_turn_live.py::test_shape_is_the_1897_shape_before_spending` (the task's explicit extra spend-free check): **FAILING, pre-existing, NOT fixed** -- confirmed present and broken at HEAD before this session (root cause: TEMPORAL_PATTERNS already `[]` from the fourth deletion; no surviving surface-1 list can ever produce get_current_time again, so unlike my other swaps there is no phrase substitute that preserves what the test is actually proving). Reported per the dispatch's STOP condition, not guessed at.

Doc updated: `docs/internal/architecture/current/intent-routing-stack.md` "Fifth deletion" subsection appended (full detail). `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` dated entry appended.

## Discovered work (per CLAUDE.md discipline -- flagging, no bd/gh tool access in this session)

1. **`test_reminder_clear_pick_target_1906.py`'s underlying product gap**: `_handle_pick_target_turn`'s #1899 off-intent discriminator (`services/intent_service/reminder_clear.py` ~1481) can no longer release on a destructive/non-READ command now that GITHUB_QUERY_PATTERNS is gone (confirmed empirically). Test converted to a different example; product gap NOT fixed, flagged for Lead/Arch.
2. **`tests/e2e/test_1897_two_part_turn_live.py`**: already broken before this session by the FOURTH deletion (TEMPORAL_PATTERNS). Not fixable by phrase substitution -- a genuine test-design decision needed.
3. **`tests/unit/services/test_pre_classifier.py::test_current_time_still_routes_to_temporal`**: same FOURTH-deletion root cause as #2, but this one WAS fixable by conversion (did so) since the file only needed a decline+routes pin, not a specific action.
4. **`test_todo_marker_ratchet`** (scripts/ratchet_ceilings.json): pre-existing, count 36 vs ceiling 35, unrelated to this unit's files.

None of 1-4 required touching product code in THIS unit; all are reported for the Lead to triage/file as separate issues.
