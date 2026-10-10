# Session log — prog-code — 2026-10-09 20:05 PT

**Role**: prog-code (Coding Agent subagent, dispatched by Lead)
**Model**: Sonnet 5 (claude-sonnet-5)
**Issue**: #1595 Inversion Phase 3 — pre-classifier literal deletion
**Worktree**: /Users/xian/Development/piper-morgan-worktrees/lead (branch claude/lead-cycle)
**Scope**: delete GUIDANCE_PATTERNS' last 3 literals (the eighth-deletion survivors:
`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`), convert the CI-tier
pins that break, update the ledger/doc/ceiling. Did NOT commit, push, or send mail — Lead reviews
and lands.

## What shipped

1. `git fetch -q origin main && git merge -q --no-edit origin/main` — fast-forward merge, no conflicts.
2. `services/intent_service/pre_classifier.py`: `GUIDANCE_PATTERNS = []  # type: List[str]`.
   Replaced the 2026-10-09 "HELD under rule 10" comment above it with a FULL-deletion tombstone
   comment: cites the 3 eighth-deletion survivors, the evidence (3 own rows + 6 rule-10 pin rows,
   all MATCH get_contextual_guidance 0.85-0.95), rule 10/11 clean, ceiling 124 -> 121.
3. `scripts/inversion_phase3_deletion_gate.py`: removed the `GUIDANCE_PATTERNS` entry from
   `HELD_FOR_CAUSE` (kept `COMPLETION_HISTORY_PATTERNS`).
4. `scripts/inversion_phase3_deleted_patterns.json`: updated the existing GUIDANCE_PATTERNS entry
   in place (no new entry) — `literals` 18 -> 21, `partial` true -> false, `surviving_literals` ->
   `{}`, appended the 3 own rows + 6 pin phrasings to `rows_claimed_at_deletion` and
   `expected_op_by_phrase` (all `get_contextual_guidance`), prepended both 2026-10-09 report
   filenames to `verdict_report`, appended a dated sentence to `note`. `git diff --numstat` confirms
   only this entry's span changed (26 insertions / 16 deletions, all within the GUIDANCE_PATTERNS
   object).
5. `tests/test_architecture_enforcement.py`: `CEILINGS["pre-classifier"]` 124 -> 121, dated comment.
   Verified via `scripts/pattern_literal_counts.py | tail -1` -> `TOTAL: 121 (36 lists)`.
6. `tests/unit/test_inversion_phase3_deletion_1595.py`: updated the GUIDANCE ledger pin (partial
   False, literals 21, surviving set()). Renamed `test_guidance_patterns_now_claims_three_rows` ->
   `test_guidance_patterns_now_claims_zero_rows` (same idiom as
   `test_temporal_patterns_now_claims_zero_rows`/`test_priority_patterns_now_claims_zero_rows`).
   Removed GUIDANCE from `test_held_for_cause_lists_render_held_naming_their_issue` (kept
   COMPLETION_HISTORY).
7. Converted the 8 broken CI-tier pins (see table below) plus one additional pin found by grep
   (`test_help_not_guidance`'s second half) not in the original list.
8. `docs/internal/architecture/current/intent-routing-stack.md`: replaced the GUIDANCE bullet under
   "Standing rule 11 (2026-10-09), and the two GOs it surfaced" with a short FULL-deletion note
   (ceiling 124 -> 121, pins converted per A/B/C); updated the section's own heading (dropped the
   now-inaccurate "both HELD, nothing deleted") and the "Ceiling unchanged at 124" line below the
   evidence sentence.

## Pins converted

| Test | Rule | Conversion |
|---|---|---|
| `tests/unit/services/test_pre_classifier.py::test_help_not_guidance` | A | Split: bare-"help" half kept as-is; "help setup my project" half moved to new `test_help_setup_now_routes_via_inversion` (decline + `assert_inversion_routes`, `read_canonical`/`get_contextual_guidance`) |
| `tests/unit/services/intent_service/test_original_message_1460.py::test_attribute_populated_at_construction[help me setup my projects]` | swap (same idiom as this file's own `STILL_CLAIMED_MULTI_INTENT_MESSAGE` precedent — not A/B/C: `detect_multiple_intents` is pure surface-1 pattern matching, has no LLM/router leg to decline-then-route through) | New constant `SETUP_MESSAGE_STILL_CLAIMED = "give me a project overview"` swapped into the parametrize list; `SETUP_MESSAGE` itself kept unchanged (still used, un-classified, by `test_setup_request_detected_from_dict_only_intent`) |
| `tests/unit/services/intent_service/test_setup_routing_814.py::TestPatternCollisionFix::test_help_me_set_up_my_portfolio_matches_guidance_patterns` | A | Converted from a raw `GUIDANCE_PATTERNS` regex-match assertion to decline + `assert_inversion_routes` |
| `tests/integration/test_capability_discovery.py::test_setup_query_classifies_as_guidance` (4 params) | A | Removed the 4 plain-string params ("Help me setup my projects", "help me setup projects", "setup my projects", "How do I setup my projects?") from the existing parametrize; added new `test_setup_query_now_routes_via_inversion` (decline + `assert_inversion_routes`) parametrized over those 4 |
| `tests/intent/contracts/test_accuracy_contracts.py::test_guidance_accuracy` | B | `@pytest.mark.llm`, comment citing corpus row "Help me set up my projects" (source `phase3-rule10-guidance/...`) + the pin-rows-score report |
| `tests/intent/contracts/test_bypass_contracts.py::test_guidance_no_bypass` | B | Same as above |
| `tests/intent/contracts/test_multiuser_contracts.py::test_guidance_multiuser_authenticated` | B | Removed `"GUIDANCE"` from `_PRE_CLASSIFIED_DETERMINISTICALLY` with a dated comment (IDENTITY precedent in the same file); test body itself needed no change — the else-branch (tolerant of the Stage-2 no-LLM stub failure) already covers it, confirmed by running it |
| `tests/e2e/test_original_message_1460_e2e.py::test_setup_request_reaches_setup_flow` | C | `@pytest.mark.llm`, comment citing "help me setup my projects" (source row) + the pin-rows-score report, modeled on `test_multi_intent_schedule_turn_reaches_agenda_aggregation`'s docstring |

Grepped `tests/` for other `GUIDANCE_PATTERNS`-referencing files beyond the list given:
`test_inversion_split_stand_down_1896.py`, `test_spend_free_canonical_ratchet_1818.py`,
`test_inversion_phase3_surface2_floor_1595.py` — all narrative-only (comments documenting history;
no assertion depends on `GUIDANCE_PATTERNS` matching anything), confirmed by running their suites
(24 passed, no changes needed — rule D, untouched).

## Verification (all commands run with ANTHROPIC_*/OPENAI_API_KEY stripped, POSTGRES_PORT=5433)

- `tests/unit -m "not llm"` (full addopts per brief): **12748 passed, 227 skipped, 3 deselected,
  174 warnings in 258.44s (0:04:18), exit 0.**
- `tests/integration tests/intent` vs `origin/main` baseline (scratch worktree `$TMPDIR/gbase`,
  `git worktree add --detach`, venv symlinked in): baseline **31 failed, 850 passed, 36 skipped,
  134 deselected, 6 xfailed**; this worktree **31 failed, 848 passed, 36 skipped, 136 deselected,
  6 xfailed** (same total; delta is my 2 new `@pytest.mark.llm` conversions in the
  accuracy/bypass contracts moving from passed to deselected). `comm -13`/`comm -23` on the sorted
  `FAILED` line sets: **0 new, 0 removed — identical 31-item set both sides.** Worktree removed
  after.
- Rest of `tests/` (`--ignore=tests/unit --ignore=tests/integration --ignore=tests/intent`), same
  baseline-diff method, run sequentially (gbase first, then this worktree, never overlapping):
  baseline **17 failed, 1484 passed, 48 skipped, 257 deselected, 65 warnings, 10 errors**; this
  worktree **17 failed, 1484 passed, 47 skipped, 258 deselected, 63 warnings, 10 errors** (same
  totals; the skipped/deselected/warnings delta is downstream of the same 2 llm-mark conversions
  propagating through collection). `comm` on sorted `^(FAILED|ERROR) tests/` lines (27 each):
  **0 new, 0 removed — identical sets.**
- `tests/unit/test_inversion_phase3_deletion_1595.py tests/test_architecture_enforcement.py
  tests/test_completion_ratchets.py`: **146 passed in 32.44s.**
- `tests/unit/test_inversion_phase3_deletion_1595.py` alone (earlier, pre-conversion-of-other-pins
  check): **65 passed.**
- `ruff format --check .`: **1914 files already formatted, exit 0.**
- `ruff check .`: **All checks passed!**
- Gate `--list GUIDANCE_PATTERNS --live ...`: `## GUIDANCE_PATTERNS / literals: 0 | rows claimed:
  0/577 / verdict: NO-GO` — identical shape to `IDENTITY_PATTERNS` (another FULL tombstone, verified
  by running both side by side with the same `--live` flags).

Side note: `ruff format --check scripts/inversion_phase3_deleted_patterns.json` (passed explicitly
as a file argument) reports "would reformat" — confirmed via `git stash` that this is PRE-EXISTING
(same result on the unmodified file before my edit) and that `ruff format --check .` (the actual
brief command, directory form) does not pick the file up at all (ruff's default discovery excludes
`.json`). Not something I introduced; not in scope to fix.

## Discovered work

None filed — no new issues needed. The one extra pin found by grep
(`test_help_not_guidance`'s GUIDANCE half) was in-scope for this same deletion and converted directly,
not filed separately.

## Not touched (rule D / out of scope)

- `tests/unit/services/intent_service/test_inversion_split_stand_down_1896.py`,
  `test_spend_free_canonical_ratchet_1818.py` (lines 186-216), and
  `tests/unit/test_inversion_phase3_surface2_floor_1595.py` carry narrative comments describing
  GUIDANCE_PATTERNS as "PARTIAL" (pre-dating this session's FULL deletion) — now stale prose, but no
  assertion in any of them depends on the claim, confirmed by running all three suites clean. Left
  as-is per the brief's scope (only specific GUIDANCE pins named + "any other ... pin you find
  failing" — these aren't failing).
- The large historical module docstring in `tests/unit/test_inversion_phase3_deletion_1595.py`
  (lines ~59-148) narrates GUIDANCE_PATTERNS as the "SECOND PARTIAL deletion" — left as historical
  narrative (accurately describes the 2026-10-02 state at the time), not rewritten; only the actual
  assertions (ledger pin, zero-rows test, held-for-cause test) were updated per the brief's explicit
  scope.

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md's "Discovered Work Discipline" and "Verify First, Create Second" sections
  (checked before editing whether code/test already existed in the stated shape); the brief's own
  embedded precedents (`_inversion_pin_helper.py`, `test_identity_queries_still_work`,
  `test_multi_intent_schedule_turn_reaches_agenda_aggregation`) — these were the actual templates
  copied, read directly rather than from memory.
- **Loaded but not referenced**: the cohort MEMORY.md index (loaded via system reminder) — none of
  its entries were load-bearing for this task; it's test-code mechanics, not cohort-coordination
  content.
- **Wanted but not found**: nothing — the brief was fully self-contained (exact rules, exact file
  paths, exact precedents named).
