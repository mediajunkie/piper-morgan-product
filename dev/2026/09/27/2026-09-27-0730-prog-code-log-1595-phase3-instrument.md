# 2026-09-27 07:30 — prog (Coding Agent), Sonnet — #1595 Phase 3 deletion-ratchet instrument

Dispatched by Lead Developer. Worktree: `~/Development/piper-morgan-worktrees/lead`
(branch `claude/lead-cycle`). Do NOT commit/stage/touch the git index — Lead reviews and
commits.

## Task

Build the Phase-3 deletion-ratchet INSTRUMENT for #1595 epic-0 unit 5:
`scripts/inversion_phase3_deletion_gate.py` + a pinning test. No deletion, no LLM calls,
no flag/env changes. Epic's own conditions (issue #1595 body): "Deletion ratchet asserts
corpus non-regression ALONGSIDE shrink" and "pattern→corpus-case conversion is a STEP IN
the deletion procedure, not an intention."

## Reading (in full, before writing code)

- `gh issue view 1595` body — Phase-3 conditions.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` unit 5.
- `docs/internal/architecture/current/intent-routing-stack.md` — surface 1's pattern
  lists, the pre-claim shadow probe (`pre_classify_with_pattern_list`,
  `MultiIntentResult.pattern_lists`), `TestExtractionPatternRatchet`.
- `tests/test_architecture_enforcement.py::TestExtractionPatternRatchet` — the literal
  counting mechanism (AST walk over `PreClassifier`'s `*PATTERNS` class attributes).
- `services/intent_service/pre_classifier.py` — `pre_classify_with_pattern_list`,
  `detect_multiple_intents`, `pattern_groups`, `_pattern_list_name`,
  `_first_pattern_match`.
- `tests/fixtures/inversion_corpus_phase0.yaml` (116 rows) +
  `scripts/inversion_phase0_baseline.py::load_corpus` / `same_operation` / `matches`.
- Shadow reports: `inversion-phase1-shadow-score-2026-09-25.md` (full, 116 rows) +
  `-temporal-rescore.md` (14 rows, TEMPORAL only) — both carry `## Row detail
  (asserted rows)` and `## REVIEW rows` markdown tables.
- `scripts/inversion_phase1_shadow_score.py::parse_phase1_report_row_detail` — the
  existing table parser (drops the route column, so I wrote a sibling parser retaining
  it rather than editing shared scorer code).
- `services/intent_service/inversion_live.py` — `live_categories`, `resolve_live_match`
  (reused verbatim for condition (c), never re-derived).

## Built

1. **`scripts/pattern_literal_counts.py`** (new) — `per_list_literal_counts()` /
   `total_literal_count()`, the AST-walk counter factored OUT of
   `TestExtractionPatternRatchet._pre_classifier_count` so the deletion gate and the
   extraction ratchet share ONE derivation instead of two copies drifting. Verified
   byte-identical (35 lists, 567 total, matches the frozen ceiling).
2. **`tests/test_architecture_enforcement.py`** — `_pre_classifier_count` now delegates
   to the shared module (with a cross-check assertion that `MIN_PATTERN_LISTS` stays in
   lockstep). `TestExtractionPatternRatchet`'s 3 tests still pass; ceiling unchanged at
   567.
3. **`scripts/inversion_phase3_deletion_gate.py`** (new, ~600 lines) — the instrument:
   - **Census**: for every corpus row, `claim_for_phrase()` runs
     `PreClassifier.pre_classify_with_pattern_list` (single-intent entry) then, if
     unclaimed, `PreClassifier.detect_multiple_intents`'s primary intent (multi-intent
     entry) — exactly the two claim sites the pre-claim shadow probe instruments. No
     new matching logic.
   - **Router verdicts**: `RouterReports` parses both reports' asserted-rows AND
     REVIEW-rows tables (a new `parse_review_rows` — no existing parser covered that
     shape), joins by normalized/prefix-matched phrase, with TEMPORAL-category rows
     preferring the temporal-rescore report (documented precedence, tested).
   - **Live set**: `expected_action_is_live()` reuses
     `inversion_live.resolve_live_match` + `_category_by_operation` +
     `derive_routing_grammar` — the exact chain the live consult itself runs — to judge
     condition (c) for `action:`-shaped corpus expectations.
   - **GO/NO-GO**: a list is deletable iff every row it claims is (a) MATCH, (b) REVIEW
     agreeing with surface-1's own claimed action for that row, or (c) expected action
     already live. Any MISMATCH/UNSCORED/disagreeing-non-live-REVIEW fails the whole
     list, named.
   - **Conversion audit**: for a deletable list, `unexercised_literals()` calls
     `PreClassifier._first_pattern_match` (production matcher, read-only) on each
     claiming row against the KNOWN claiming list to find which literals never fired —
     printed as "needs a corpus row before deletion."
   - **Deletion ledger**: `load_deleted_pattern_lists()` /
     `check_deleted_entry_non_regression()` — reads/checks
     `scripts/inversion_phase3_deleted_patterns.json`'s `DELETED_PATTERN_LISTS` (empty
     today).
   - `--list NAME`, `--all`, `--live TOKENS` CLI.
4. **`scripts/inversion_phase3_deleted_patterns.json`** (new sibling JSON, not
   `ratchet_ceilings.json` — avoided adding a non-numeric value to the numeric-ceiling
   file other scripts iterate). `DELETED_PATTERN_LISTS: []`.
5. **`tests/unit/test_inversion_phase3_deletion_1595.py`** (new, 19 tests) — census
   denominators (claimed+unclaimed==116, real corpus/pre-classifier), the
   non-regression mechanism proven against SYNTHETIC entries (never the real empty
   ledger) for both failure modes + the pass case, the real empty ledger asserted
   empty + vacuously-clean, TEMPORAL_PATTERNS verdict printed with named rows (GO/NO-GO
   NOT pinned — only that every backing row is named with a reason), report-parser
   pins including the TEMPORAL-rescore-overrides-full-report precedence, and live-set
   resolution (unknown/override/condition-c true+false paths).
6. **Docs**: `intent-routing-stack.md` gains "## Phase 3 — deletion gate" (mechanism,
   three GO conditions, precedence, conversion step, ledger, measured 2026-09-27
   snapshot). `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` progress
   log gets the unit-5 entry.

## Verified how

- **Method**: ran the new script (`--list TEMPORAL_PATTERNS`, `--all`) and read its
  stdout directly; ran `pytest` on the new test file and on
  `TestExtractionPatternRatchet` and captured exit codes; ran `scripts/run-sweep.sh
  ratchets` and read its full output; ran `ruff format --check` / `ruff check` on every
  touched Python file.
- **Layer** (m-43): this measures the DETERMINISTIC pre-classifier + markdown-table
  parsing + the live-flag matcher, exactly as production consults each — it does NOT
  re-run the router (no LLM calls anywhere in this task) and does NOT execute a
  deletion (no `*_PATTERNS` list was touched in `pre_classifier.py`).
- **Denominator**: census covers all 116 corpus rows (84 claimed, 32 unclaimed,
  verified summing to 116); the extraction-ratchet's 35 lists / 567 literals cross-
  checked against the factored module's own output.

### Commands + outputs

```
$ venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS
live set source: unknown (UNKNOWN — pass --live)
corpus denominator: 116 rows total = 84 claimed + 32 unclaimed

## TEMPORAL_PATTERNS
literals: 56  |  rows claimed: 2/116
verdict: GO (deletable) — deleting removes 56 literals: ceiling 567 -> 511

rows claimed:
  [OK] "when is my next meeting?" -> claim=get_current_time expected=action:meeting_time router=meeting_time@1.0 verdict=MATCH :: MATCH
  [OK] "what time is it?" -> claim=get_current_time expected=category:TEMPORAL router=get_current_time@1.0 verdict=MATCH :: MATCH

pattern->corpus conversion: 54 literals unexercised (needs-a-corpus-row lines, e.g.
r"\bwhat'?s the time\b", r"\bmy calendar\b", r"\bmy meetings\b" ... full list in the
script's stdout — omitted here for length).
```

```
$ venv/bin/python scripts/inversion_phase3_deletion_gate.py --all
corpus denominator: 116 rows total = 84 claimed + 32 unclaimed
list                                     literals   rows      verdict
----------------------------------------------------------------------
ANALYSIS_PATTERNS                              16      1           GO
CALENDAR_QUERY_PATTERNS                        52      3           GO
COMPLETION_HISTORY_PATTERNS                     5      1           GO
CONTEXTUAL_QUERY_PATTERNS                      13      2           GO
DISCOVERY_PATTERNS                             20      1           GO
DOCUMENT_QUERY_PATTERNS                        10      2           GO
FAREWELL_PATTERNS                               5      1           GO
FEATURE_INFO_PATTERNS                           6      1           GO
FILE_REFERENCE_PATTERNS                        30      0      NO ROWS
GET_DEFAULT_REPO_PATTERNS                       5      2           GO
GITHUB_QUERY_PATTERNS                          64     13        NO-GO
GREETING_PATTERNS                               9      1           GO
GUIDANCE_PATTERNS                              21      1           GO
IDENTITY_PATTERNS                               6      1           GO
INSIGHT_PULL_PATTERNS                           7      2           GO
INTEGRATION_CONNECT_PATTERNS                    1      9        NO-GO
LOCAL_GIT_STATUS_PATTERNS                      12      1           GO
MEMORY_PATTERNS                                15      1           GO
MILESTONE_STATUS_INLINE_PATTERNS                0      1        NO-GO
PORTFOLIO_PATTERNS                             16      9        NO-GO
PRIORITY_PATTERNS                              47      3           GO
PRODUCTIVITY_QUERY_PATTERNS                     4      1           GO
PROVENANCE_PATTERNS                             8      1           GO
REMINDER_PATTERNS                               5      1           GO
REMINDER_QUERY_PATTERNS                         4      1           GO
REPO_MANAGEMENT_PATTERNS                       12      2           GO
SESSION_ACTIVITY_QUERY_PATTERNS                 6      1           GO
SET_DEFAULT_REPO_PATTERNS                       4      4        NO-GO
STAKEHOLDER_UPDATE_PATTERNS                     4      2           GO
STATUS_PATTERNS                                56      5        NO-GO
TEMPORAL_PATTERNS                              56      2           GO
THANKS_PATTERNS                                 5      1           GO
TODO_COMPLETE_PATTERNS                          7      3           GO
TODO_QUERY_PATTERNS                            10      3           GO
TRUST_PATTERNS                                 16      1        NO-GO
_PLEASANTRY_FILLER_PATTERNS                    10      0      NO ROWS
----------------------------------------------------------------------
total rows claimed: 84

lists with ZERO corpus claims (2): FILE_REFERENCE_PATTERNS, _PLEASANTRY_FILLER_PATTERNS
```

Spot-checked two NO-GO verdicts against the source reports to sanity-check the join
logic: `SET_DEFAULT_REPO_PATTERNS` fails on two REVIEW rows where the router reads the
interrogative "are you able to set my default repo for me conversationally?" as `NONE`
(not `set_default_repo`) — matches the corpus's own annotation ("interrogative parsed
as imperative," issue-1606). `TRUST_PATTERNS` fails on its one row ("why can't you
create issues?") where the router answers `get_capabilities`, not `explain_trust` — both
genuine, informative findings, not instrument bugs.

```
$ venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q
...................                                                      [100%]
19 passed in 2.45s
EXIT: 0

$ venv/bin/python -m pytest tests/test_architecture_enforcement.py -q
..........................................................x.....         [100%]
63 passed, 1 xfailed in 10.94s
EXIT: 0

$ ./scripts/run-sweep.sh ratchets
....................................................................x... [ 97%]
..                                                                       [100%]
73 passed, 1 xfailed in 20.07s
--- mypy per-code gate (#1436) ---
mypy gate: all 24 ratcheted codes at ceiling (total=1121; arg-type=364, assignment=227,
attr-defined=69, call-arg=3, call-overload=6, dict-item=5, has-type=2, index=10,
list-item=2, misc=77, no-redef=3, operator=63, override=17, return=1, return-value=48,
union-attr=141, valid-type=14, var-annotated=69)
EXIT: 0

$ venv/bin/ruff format --check <touched files>   -> "4 files already formatted", exit 0
$ venv/bin/ruff check <touched files>            -> "All checks passed!", exit 0
```

## Discovered work

None filed. Two genuine surface-1 gaps surfaced by the census (SET_DEFAULT_REPO_PATTERNS'
interrogative miss, TRUST_PATTERNS' single-row miss) are pre-existing, already-documented
corpus/REVIEW rows (issue-1606, probe-row-17) — not new findings requiring a fresh issue.

## Files touched

- `scripts/pattern_literal_counts.py` (new)
- `scripts/inversion_phase3_deletion_gate.py` (new)
- `scripts/inversion_phase3_deleted_patterns.json` (new)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (new)
- `tests/test_architecture_enforcement.py` (edited — `_pre_classifier_count` delegates)
- `docs/internal/architecture/current/intent-routing-stack.md` (edited — new section)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (edited — progress log)

Did NOT touch the git index per instructions — handing back to Lead for review/commit.

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md "Verify First, Create Second" (investigate-before-extend —
  drove the full-read-before-writing pass); CLAUDE.md "Name the layer, and state the
  denominator" (m-43/m-44 — shaped the docstrings' layer statements and the census
  denominator assertions); `intent-routing-stack.md`'s pre-claim shadow probe section
  (the exact reuse mechanism for claiming-list identity).
- **Loaded but not referenced**: MEMORY.md feedback entries (no directly relevant
  entry beyond general discipline already embedded in CLAUDE.md); ROSTER.md-adjacent
  role table (not needed — role/worktree given directly in the dispatch prompt).
- **Wanted but not found**: none — the dispatch prompt's reading list was sufficient.
