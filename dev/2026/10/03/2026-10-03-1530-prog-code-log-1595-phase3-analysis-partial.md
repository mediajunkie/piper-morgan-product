# 2026-10-03 — Coding Agent (prog), model: Sonnet 5 — #1595 Phase 3 twelfth deletion (ANALYSIS_PATTERNS, PARTIAL)

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead`,
branch `claude/lead-cycle`. Do NOT commit (Lead commits by pathspec after review). No LLM calls, no
`gh`, no env/flag/deploy/web touches.

## Task

Twelfth deletion in the #1595 Phase 3 ratchet, the SIXTH PARTIAL one: `ANALYSIS_PATTERNS` (16
literals) in `services/intent_service/pre_classifier.py` — 12 literals go, 4 SURVIVE
(`\bwhat.*obstacle\b`, `\bwhat'?s in the way\b`, `\banalyze.*(?:risk|impact|blocker|bottleneck)\b`,
`\bimpact analysis\b`).

## STEP 1 — BEFORE gate + literal audit

Ran:
```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list ANALYSIS_PATTERNS \
  --live create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,read_synthesis,read_temporal
```

Result (log noise stripped):
```
corpus denominator: 447 rows total = 77 claimed + 370 unclaimed

## ANALYSIS_PATTERNS
literals: 16  |  rows claimed: 16/447
verdict: GO (partial) — 4 load-bearing literal(s) SURVIVE, deleting the other 12: ceiling 213 -> 201
  survives: r"\bwhat.*obstacle\b"  <- "what's the main obstacle here"
  survives: r"\bwhat'?s in the way\b"  <- "what's in the way of finishing this"
  survives: r"\banalyze.*(?:risk|impact|blocker|bottleneck)\b"  <- "let's analyze the risk here"
  survives: r"\bimpact analysis\b"  <- 'can you run an impact analysis on this change'

rows claimed:
  [OK] "what's blocking the milestone?" -> claim=analyze_blockers expected=REVIEW router=analyze_blockers@1.0 verdict=REVIEW :: REVIEW-agrees (route=analyze_blockers == claim=analyze_blockers; live via group)
  [OK] "what is blocking this release" -> expected=action:analyze_blockers router=analyze_blockers@0.92 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what tasks are blocking our sprint" -> expected=action:analyze_blockers router=analyze_blockers@0.95 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "blockers for the release" -> expected=action:analyze_blockers router=analyze_blockers@0.95 verdict=MATCH :: MATCH (expected action live via group)
  [FAIL] "what's the main obstacle here" -> router=CLARIFY@0.4 verdict=MISMATCH :: the pattern is the live path; surface 2 names analyze_blockers only 0/10
  [FAIL] "what's in the way of finishing this" -> router=CLARIFY@0.4 verdict=MISMATCH :: same
  [FAIL] "let's analyze the risk here" -> router=CLARIFY@0.4 verdict=MISMATCH :: same
  [OK] "I'd like a risk assessment for this project" -> expected=action:analyze_blockers router=analyze_blockers@0.72 verdict=MATCH :: MATCH (expected action live via group)
  [FAIL] "can you run an impact analysis on this change" -> router=CLARIFY@0.4 verdict=MISMATCH :: same
  [OK] "is there a bottleneck analysis available" -> claim=analyze_blockers expected=action:get_capabilities router=get_capabilities@0.92 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what risks does this project have" -> expected=action:analyze_blockers router=analyze_blockers@0.85 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what risk do we have in this plan" -> expected=action:analyze_blockers router=analyze_blockers@0.85 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "please identify the risks in this plan" -> expected=action:analyze_blockers router=analyze_blockers@0.72 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "risks we should flag before launch" -> expected=action:analyze_blockers router=analyze_blockers@0.85 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "threats to our timeline this week" -> expected=action:analyze_blockers router=analyze_blockers@0.92 verdict=MATCH :: MATCH (expected action live via group)
  [OK] "what could threaten this deadline" -> expected=action:analyze_blockers router=analyze_blockers@0.85 verdict=MATCH :: MATCH (expected action live via group)
```
Matches the dispatch's expectation exactly (GO (partial), 4 survivors, ceiling 213 -> 201) — no
STOP.

Confirmed independently: `pattern_literal_counts.total_literal_count()` → 213 (pre-deletion
baseline); `per_list_literal_counts()["ANALYSIS_PATTERNS"]` → 16.

**Unexercised-literal audit (STEP 2) — the CLEAN case** (16 rows claimed for 16 literals): computed
via the gate's own `unexercised_literals("ANALYSIS_PATTERNS", lv.rows)` → empty list. All 16
literals exercised 1:1 by a claimed row. No shadowing audit needed, no corpus deposit needed, no
STOP.

Consulted the seventh (STATUS) partial entry's style for the surface-2/misserved shapes as
instructed, and found one applicable finding here: "is there a bottleneck analysis available"
claims `analyze_blockers` (via the now-deleted `\bbottleneck.*(?:analysis|report)\b` literal) but
the corpus's ruled expected action is `get_capabilities` (RULED 2026-10-02 by PPM, per the
fixture's own `notes` field in `tests/fixtures/inversion_corpus_phase0.yaml`: "is there X
available" is the DISCOVERY existence question, not an ANALYSIS request). Unlike the eleventh
deletion's (MEMORY) mis-serve row, this one is credited through the ORDINARY live-MATCH branch of
`row_disposition` — the router independently MATCHes `get_capabilities@0.92`, and the expected
action is live via group, so the gate's "mis-serves this row" escape branch is never even reached.
But informationally, the pattern's own claim IS already wrong today regardless of which branch
credits the row — deleting it cannot make the surviving fallback (the router's own live route) any
worse. Recorded as `misserved_at_deletion` in the ledger entry for the same reason the eleventh
deletion recorded its analogous row, even though the credit mechanism differs.

| literal | status | evidence |
|---|---|---|
| 11 of 12 to-be-deleted literals | exercised, 1:1, live MATCH/REVIEW-agrees | each claims exactly one `[OK]` row, expected action live via group |
| 1 to-be-deleted literal (`\bbottleneck.*(?:analysis\|report)\b`) | exercised, mis-serve (informational) | claims "is there a bottleneck analysis available" as `analyze_blockers`, disagreeing with ruled `get_capabilities`; router independently MATCHes `get_capabilities@0.92` live — credited via the ordinary live-MATCH branch, not the mis-serve escape |
| 4 survivors | exercised | each claims its own `[FAIL]` row |

## STEP 3 — applied the partial deletion

`services/intent_service/pre_classifier.py`: `ANALYSIS_PATTERNS` now exactly the 4 survivor
literals, in their original relative order, each with a one-line comment naming the corpus row it
carries, preceded by a dated comment block recording the deletion, the gate quote, the clean
unexercised-literal audit, the mis-serve finding, and the ceiling arithmetic. Claim branch
(`pre_classify`'s `ANALYSIS_PATTERNS` if-block) left untouched (still live, non-empty list).
Confirmed via `pattern_literal_counts.total_literal_count()` → 201,
`per_list_literal_counts()["ANALYSIS_PATTERNS"]` → 4.

`ruff check`/`ruff format --check` on the edited file: clean, no changes needed.

## STEP 4 — reabsorption check + AFTER gate

For each of the 12 deleted-literal corpus-row phrases, ran `gate.claim_for_phrase(PreClassifier,
phrase)` (both entry surfaces internally) against the live, post-deletion `PreClassifier`:

```
=== deleted corpus rows (12) ===
"what's blocking the milestone?"                 -> UNCLAIMED
'what is blocking this release'                   -> UNCLAIMED
'what tasks are blocking our sprint'               -> UNCLAIMED
'blockers for the release'                         -> UNCLAIMED
"I'd like a risk assessment for this project"      -> UNCLAIMED
'is there a bottleneck analysis available'         -> UNCLAIMED
'what risks does this project have'                -> UNCLAIMED
'what risk do we have in this plan'                -> UNCLAIMED
'please identify the risks in this plan'           -> UNCLAIMED
'risks we should flag before launch'               -> UNCLAIMED
'threats to our timeline this week'                -> UNCLAIMED
'what could threaten this deadline'                -> UNCLAIMED

=== survivor rows still claimed ===
"what's the main obstacle here"                          -> list=ANALYSIS_PATTERNS action=analyze_blockers
"what's in the way of finishing this"                     -> list=ANALYSIS_PATTERNS action=analyze_blockers
"let's analyze the risk here"                              -> list=ANALYSIS_PATTERNS action=analyze_blockers
'can you run an impact analysis on this change'            -> list=ANALYSIS_PATTERNS action=analyze_blockers
```

**Zero reabsorptions**: all 12 deleted-row phrases are genuinely UNCLAIMED. Checked carefully for
accidental breadth in the 2 broadest survivors (`\bwhat.*obstacle\b`, `\banalyze.*
(?:risk|impact|blocker|bottleneck)\b`) — neither catches any of the 12 deleted phrases (none
contain "obstacle", and none contain the literal substring "analyze"). No other surviving list
reclaims any of the 12 either.

`--all` gate: `ANALYSIS_PATTERNS 4 4 NO-GO` (4 literals, 4 rows — exactly the 4 survivors, all
still `[FAIL]`, expected for a partial list's remainder with zero reabsorptions). Corpus
denominator: 447 = 65 claimed + 382 unclaimed (down from 77 claimed pre-deletion; 77 − 65 = 12, the
full set of deleted-row claims, none reabsorbed). `pattern_literal_counts.total_literal_count()` →
201 confirmed again post-edit.

## STEP 5 — ceiling + ledger

`CEILINGS["pre-classifier"]` 213 → 201 in `tests/test_architecture_enforcement.py`, dated comment
block matching the established per-deletion style.

Appended the 13th `DELETED_PATTERN_LISTS` entry to `scripts/inversion_phase3_deleted_patterns.json`
via a one-off Python build script (never hand-typed): `"partial": true`, `"surviving_literals"`
(4-literal map), `"literals": 12` (deleted count), `rows_claimed_at_deletion` (12 phrases),
`verdict_report` (`inversion-phase1-shadow-score-2026-09-25.md` +
`inversion-phase3-analysis-rescore-2026-10-03.md`, mirroring the DISCOVERY/TRUST/MEMORY style),
`expected_op_by_phrase` (12 entries: 11 `analyze_blockers`, 1 `get_capabilities` for the mis-serve
row), `shadowed_literals: {}` (empty — clean case), `misserved_at_deletion` (1 entry — "is there a
bottleneck analysis available"), `surface2_verified_at_deletion: {}` (empty), `known_reabsorptions:
{}` (empty — zero reabsorptions). Built with `ensure_ascii=True` (the DEFAULT) this time — the
eleventh deletion's own session note flagged that `ensure_ascii=False` silently re-encodes 3
PRE-EXISTING em-dash escapes elsewhere in the ledger file as literal em-dash bytes, producing an
unwanted diff on unrelated entries; the first attempt here hit exactly that (confirmed via
`git diff --numstat` showing 72 insertions / 4 deletions instead of a pure insertion), reverted via
`git checkout -- scripts/inversion_phase3_deleted_patterns.json` (single explicit tracked path, my
own uncommitted edit, in my own worktree — not PM's main checkout), and rebuilt with the default
`ensure_ascii=True`. Second attempt: `git diff --numstat` → 68 insertions, 0 deletions — pure
insertion confirmed. **Reloaded with `json.load` immediately after writing** — confirmed 13
entries, parses cleanly, no escaping artifacts in the new entry (manually inspected the diff).

## STEP 6 — test conversion

Ran the specified suite set under `-x --maxfail=1`. First run stopped at
`tests/unit/services/test_pre_classifier.py::TestPreClassifier::test_analysis_risk_patterns`
(1 failed, 5032 passed). Found and converted, across 3 files:

1. **`tests/unit/services/test_pre_classifier.py`**:
   - `test_analysis_risk_patterns` (3 phrasings: "What risks should I be aware of?", "What risks do
     we face?", "Identify risks in the project" — all matched now-deleted literals, none covered by
     a survivor) renamed to `test_analysis_risk_patterns_now_unclaimed_by_surface_1`, flipped to
     assert `PreClassifier.pre_classify(query) is None` for all 3.
   - Added `test_analysis_risk_survivor_literal_still_matches` for the surviving
     `\banalyze.*(?:risk|impact|blocker|bottleneck)\b` literal ("let's analyze the risk here" →
     ANALYSIS/`analyze_blockers`, confidence 1.0).
   - `test_blocker_analysis_patterns` (2 phrasings: "What's blocking the milestone?", "What's
     blocking the sprint?" — both matched the now-deleted `\bwhat'?s blocking\b` literal) renamed
     to `test_blocker_analysis_patterns_now_unclaimed_by_surface_1`, flipped to assert `None` for
     both.
   - Full file run (after fix): passed, included in the full-suite count below.

2. **`tests/unit/services/intent_service/test_keyword_disambiguation_901.py`**:
   - `TestKeywordDisambiguationQ43`'s 4 tests all used now-deleted-literal phrases ("What's
     blocking the milestone?", "What is blocking the release?", "What are the blockers for the
     sprint?", "I need a risk assessment"). Renamed and swapped 1:1 to the 4 surviving literals'
     own corpus phrases: `test_main_obstacle_routes_to_analysis` ("what's the main obstacle here"),
     `test_in_the_way_routes_to_analysis` ("what's in the way of finishing this"),
     `test_analyze_risk_routes_to_analysis` ("let's analyze the risk here"),
     `test_impact_analysis_routes_to_analysis` ("can you run an impact analysis on this change") —
     preserves the Q43 disambiguation point (ANALYSIS reachable at surface 1, not misrouted to
     STATUS). Class docstring updated with the twelfth-deletion context.
   - Full file run: 22 passed.

3. **`tests/unit/services/intent_service/test_preclaim_shadow.py`**:
   - 4 call sites (plus their explanatory comments/docstrings) used "what's blocking the
     milestone?" as the canonical multi-intent / "3+ distinct claiming lists" `ANALYSIS_PATTERNS`
     fixture — matched the now-deleted `\bwhat.*block(?:s|ing|ed)\s+(?:the|my|our)\b` literal (the
     same literal two prior deletions, CALENDAR_QUERY_PATTERNS' third and TEMPORAL_PATTERNS'
     fourth, had already forced this exact phrase into as their own substitution target). Swapped
     throughout to "what's the main obstacle here" (via the surviving `\bwhat.*obstacle\b`
     literal, confirmed live this session, same GREETING_PATTERNS + ANALYSIS_PATTERNS 2-intent
     shape for the multi-intent cases):
     `TestSampledOn.test_multi_intent_surface_schedules_with_all_lists`, the
     `TestPatternIdentityThreading.test_pre_classify_surface_names_its_list` parametrize row,
     `test_multi_surface_pattern_lists_align_with_intents`, and
     `test_identity_reaches_telemetry_for_three_lists`.
   - Full file run: 29 passed.

**Checked, NOT touched** (per the task's explicit `git grep -l -e ANALYSIS_PATTERNS -e
analyze_blockers -- tests/` and manual follow-up greps for deleted-row phrase substrings):
- `tests/unit/services/intent_service/test_action_registry.py` +
  `tests/unit/services/intent_service/test_read_floor_rail_1595.py` — both test `(category,
  action)` registry/rail membership directly (`get_disposition("ANALYSIS", "analyze_blockers")`,
  the `read_floor` flip-group's `MEMBERS` set), never a surface-1 literal match.
- `tests/e2e/test_read_floor_live.py` — `pytest.mark.llm`-gated (skipped without a live header
  key), tests end-to-end router/floor dispatch, not which literal matched at surface 1.
- `tests/e2e/test_canonical_conversations.py` — found via a broader grep for "blocking the
  milestone"/"risks should I be aware"; contains both phrases as canonical rows with
  `expected_destination="floor"`. `tests/e2e/`, requires a live DB/app, outside this dispatch's
  tests/unit scope — and its expected destination is already "floor" regardless of which surface
  claims the phrase (analyze_blockers is itself a FLOOR-disposition action).
- `tests/unit/services/intent_service/test_conversational_floor.py` — found via the same broader
  grep ("What risks should I be aware of?" appears as a literal string value). Builds a
  `FloorContext` dataclass directly, never calls `PreClassifier.pre_classify`.
- `services/intent_service/chat_pointers.py` — grepped for `ANALYSIS`/`analyze_blockers`; no
  `CHAT_POINTERS` entry resolves through `ANALYSIS_PATTERNS`.
- `tests/fixtures/inversion_corpus_phase0.yaml` — ground-truth corpus data, never edited by the
  deletion procedure.
- `tests/unit/services/intent_service/test_analysis_repo_threading_1646.py` +
  `test_analyze_findings_1660.py` — grepped by filename similarity; neither calls `pre_classify` or
  references `ANALYSIS_PATTERNS`/literal phrases.

Full suite run (`tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
+ `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` +
`tests/unit/test_inversion_phase3_surface2_floor_1595.py` +
`tests/unit/test_inversion_phase1_shadow_score_1595.py`, one combined invocation, run in background
due to runtime, twice — once to find the two failing tests under `-x --maxfail=1` (1 failed, 5032
passed, 136.51s), once clean after converting them): **5188 passed, 1 xfailed, 0 failed, exit code
0, 152.67s**.

`tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures per the dispatch,
run separately with `-o addopts="--import-mode=importlib --tb=line"`): **16 failed, 11 passed** —
identical count to the dispatch's stated baseline (16), confirming no new failures.

`ruff format`/`ruff check` run on exactly the touched `.py` files (confirmed via `git status
--short` before invoking ruff — the ledger JSON was never in the argument list): all clean, no
formatting needed, both before and after the test-conversion round.

## STEP 7 — docs

Appended "### Twelfth deletion (2026-10-03): `ANALYSIS_PATTERNS` (partial — 12 of 16)" to
`docs/internal/architecture/current/intent-routing-stack.md` (full BEFORE/AFTER gate quotes, the
partial rule, the clean unexercised-literal audit, the one `misserved_at_deletion` row — credited
via the ordinary live-MATCH branch rather than the mis-serve escape, a new wrinkle this entry
surfaces — the zero `known_reabsorptions`, all converted/checked-not-touched test files, ceiling
arithmetic, full suite counts). Dated entry appended to
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

**Files touched** (no commits — Lead commits by pathspec):
`services/intent_service/pre_classifier.py`, `scripts/inversion_phase3_deleted_patterns.json`,
`tests/test_architecture_enforcement.py`, `tests/unit/test_inversion_phase3_deletion_1595.py`,
`tests/unit/services/test_pre_classifier.py`,
`tests/unit/services/intent_service/test_keyword_disambiguation_901.py`,
`tests/unit/services/intent_service/test_preclaim_shadow.py`,
`docs/internal/architecture/current/intent-routing-stack.md`,
`dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`, this session log.

**Not mine, found modified, left untouched**: `dev/state/lead-last-pm-scan` appeared in `git
status --short` as modified but was never touched by this dispatch — flagging to Lead in the
handback rather than staging or reverting it (not my file, outside this task's scope, and this
worktree may have another process writing to it).

No product code outside `pre_classifier.py`'s pattern-literal edit was changed. No `.json` file
was ever passed to ruff. No `gh`/issue tooling used (off-limits for this dispatch). No env/flag/
deploy/web touches. No LLM calls made anywhere in this session.

## Verified how

**Method**: every gate run quoted above was executed this session against the live repo state
(not recalled); `pattern_literal_counts.total_literal_count()`/`per_list_literal_counts()` called
directly against the live, edited `PreClassifier` class before and after the edit;
`unexercised_literals`/`claim_for_phrase` run empirically for the unexercised-literal audit (empty
result, confirmed) and the AFTER reabsorption scan (12 deleted-row phrases + 4 survivor rows, 16
total); the ledger entry was built via a one-off Python script, reloaded with `json.load`
immediately, and a `git diff --numstat` check caught the `ensure_ascii=False` re-encoding issue on
the first attempt before it was fixed and re-verified as a pure insertion; the full specified test
suite was run to completion twice with explicit pass/fail counts quoted (one combined background
invocation each time, confirmed via exit code and the printed summary line) — the first run's
single failure was root-caused to two specific test functions, both converted, then the suite was
re-run clean; the `test_multi_intent.py` baseline-failure count was re-measured this session (not
assumed from the dispatch's stated number) and found identical; `ruff`'s file list was the exact
set of touched `.py` files, confirmed via `git status --short` immediately before each ruff
invocation, both before and after the test-conversion round.

**Layer measured**: surface-1 pattern-literal matching only (`PreClassifier.pre_classify` /
`pre_classify_with_pattern_list` / `detect_multiple_intents`, the real if-chain, never
`_first_pattern_match` in isolation except for the (empty) shadowing audit) — no LLM calls, no live
router calls, no app/DB. The gate's router-verdict layer is read from frozen, already-scored report
files (`inversion-phase1-shadow-score-2026-09-25.md`, `inversion-phase3-analysis-rescore-2026-10-03.md`),
never re-derived.

**Denominator**: 16 of 16 `ANALYSIS_PATTERNS` corpus rows claimed pre-deletion, all 16 accounted
for in the gate's row-by-row disposition (12 `[OK]` deleted, 4 `[FAIL]` survivors); 12 of 12
deleted-row phrases checked for reabsorption post-deletion (zero found); the full specified test
suite (6 paths) run to completion, 5188 of 5188 passing (plus 1 pre-existing xfail); the
pre-existing `test_multi_intent.py` baseline (16 failures) re-measured, not assumed, and found
unchanged (16 of 16 identical failures, 11 of 11 identical passes).

## Discovered work

None filed. The `dev/state/lead-last-pm-scan` modification noted above is flagged to Lead directly
in the handback, not filed as a tracked issue (too small/ambiguous to be "discovered work" — may
just be a concurrent duty-cycle write).
