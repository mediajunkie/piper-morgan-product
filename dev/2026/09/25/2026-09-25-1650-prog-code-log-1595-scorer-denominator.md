# Session Log — prog (Coding Agent), 2026-09-25 16:50 PT

**Model**: Sonnet 5 (claude-sonnet-5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Task**: #1595 — fix the Phase-1 shadow-score instrument's denominator (m-44, Task A) and sharpen the
`meeting_time`/`week_calendar` grammar descriptions (PDR-006 condition 2, Task B). PM-gated re-score is
NOT run here — no LLM calls anywhere in this session, `--dry-run` only.
**Do NOT commit/stage/touch git index** — Lead reviews and commits.

## Reading done before starting
- `docs/internal/architecture/current/inversion-phase1-shadow-score-2026-09-25.md` in full, especially
  "Lead's read" at the bottom (the spec: TEMPORAL shared 4, router 3/4, baseline 4/4, REGRESSION, naming
  `what's on my calendar today?`; the HOLD on `read_temporal` pending this fix).
- `scripts/inversion_phase1_shadow_score.py` — baseline tuple (~85-101), `build_report` (~218-362),
  `run` (~365-432).
- `scripts/inversion_phase0_baseline.py` — shared corpus/matching idioms (`load_corpus`, `matches`,
  `same_operation`).
- `docs/internal/architecture/current/inversion-phase0-baseline-full-2026-08-12.md` — the baseline's own
  per-row "Row detail" table (93 rows, 39 asserted), which Task A parses as the shared-subset source.
- `services/intent_service/inversion_router.py` ~180-280 — `derive_routing_grammar`: two sources (rail
  first via `get_action_workflows()`, alias-collapsed by shared entry-point identity; then
  `ACTION_REGISTRY` actions with no rail coverage), descriptions = `entry.description` with
  `_DESC_NOISE_RE` stripping `via action dispatch (#NNNN...)` trailing noise — never hand-written here.
- `services/intent_service/action_registry.py` ~128-130 (`meeting_time`/`week_calendar` registered
  `WORKFLOW` disposition — rail-covered, so registry's own `ACTION_DESCRIPTIONS` entries at ~235-237
  are NOT what the grammar shows; the rail entry wins) and `_CALENDAR_QUERY_COHORT` /
  `_CALENDAR_QUERY_FLIP_GROUPS` in `workflow_entries.py` ~1268-1305 + the entry-construction loop
  ~2074-2096.
- `tests/unit/test_inversion_phase2_gate_1595.py` — full read, mirrored for this file's import idiom
  (`sys.path.insert(ROOT/"scripts")`, `import inversion_phase2_gate as gate`).
- `dev/2026/09/25/2026-09-25-1640-prog-code-log-1595-unit3.md` — prior prog session this run, confirmed
  no overlap (unit 3 was the `create_reminder` write-allowlist flip; unrelated to this scorer fix).

## Diagnosis (before writing code)
Ran `--dry-run` first to confirm the current grammar's derived descriptions for the two operations:
`meeting_time` → `_handle_meeting_time_query`, `week_calendar` → `_handle_week_calendar_query` — the
noise-stripped rail description is literally the private handler method name (both come from the
cohort loop's generic `f"{handler_attr} via action dispatch (#1124)"` template, identical shape for
all three calendar siblings). That's the root cause the Lead's read named: the router has no semantic
signal to distinguish "today/a day/next meeting" from "the week ahead."

## Task A — shared-subset denominator fix (m-44)

**Decision on the tuple question** (task gave a choice): kept `PHASE0_BASELINE` (the hardcoded
per-category `(asserted, matched)` tuple) UNCHANGED for the existing totals table (now marked
informational-only) — no regression risk to anything reading that table's shape. Added a NEW parsed
source, `PHASE0_BASELINE_DOC` (parsed fresh every run via `parse_baseline_row_detail`), used ONLY for
the new shared-subset table. Rationale: the tuple is a coarse per-category total that other code/docs
may already reference; the shared-subset score needs per-ROW baseline verdicts (MATCH/MISMATCH per
phrase), which only the doc's own row-detail table carries — the tuple can't be un-collapsed back into
rows.

**Matching rule** (stated per the task's ask): phrase normalized (strip + collapse internal whitespace
+ casefold), exact match required. Fallback: markdown row-detail tables in this codebase truncate long
phrases with NO ellipsis at different fixed lengths in different docs (the 08-12 baseline: `[:60]`;
this script's own asserted-rows table: `[:55]`) — on an exact-match miss, fall back to an unambiguous
≥20-char prefix match in either direction; an ambiguous multi-candidate prefix is left unmatched
(reported as dropped, never guessed). Implemented as `_norm_phrase` + `_prefix_candidates` +
`_MIN_PREFIX_LEN = 20`.

**New functions in `scripts/inversion_phase1_shadow_score.py`**:
- `parse_baseline_row_detail(path)` — parses the 08-12 doc's `## Row detail` table into
  `{phrase, category, expected, verdict}` dicts. Raises loudly on a missing section or zero rows
  parsed (m-44: a broken parser must say so, not silently score against nothing).
- `parse_phase1_report_row_detail(path)` — same idea for THIS script's own `## Row detail (asserted
  rows)` table, used only for `--dry-run` cross-validation against an already-generated report (no
  LLM call).
- `compute_shared_subset(row_results, baseline_rows)` — pure, testable. Per category: `shared`,
  `router_match`, `baseline_match`; plus `dropped` (baseline-asserted, no current match), `added`
  (current-asserted, no baseline match), and `regressed` (named phrases where baseline matched and the
  router didn't — the specific evidence behind a REGRESSION cell, not just a count).
- `build_shared_subset_section(shared)` — renders the new markdown table + matching-rule prose +
  dropped/added/named-regression listings.

**Wiring**: `run()` now parses `baseline_rows` unconditionally (both dry and full paths — a parse
failure should surface even in `--dry-run`), passes it into `build_report(..., baseline_rows=...)`.
`build_report` calls `compute_shared_subset` + `build_shared_subset_section` and inserts the new
section right after the existing totals table, with a new ⚠️ m-44 note marking that table's Δ/gate
cells informational-only from this run forward, and softening the "🔴 Per-category regressions" line
to say the same.

**Dry-run validation** (Task A ask: "exercise the parse + the shared-subset computation against the
existing 2026-09-25 report's decisions if the script can re-read them, else synthetic decisions in a
unit test" — did BOTH):
- `--dry-run` parses `PHASE0_BASELINE_DOC` (93 rows, 39 asserted — printed), then, if
  `docs/internal/architecture/current/inversion-phase1-shadow-score-2026-09-25.md` exists (it does,
  from an earlier run this session), parses ITS row-detail table via `parse_phase1_report_row_detail`
  and runs `compute_shared_subset` against real data — no LLM call, pure replay of two already-written
  markdown tables.
- Result, quoted verbatim below (Result section) — reproduces Lead's read exactly: TEMPORAL shared=4,
  router=3/4, baseline=4/4, gate=REGRESSION, named regression `["what's on my calendar today?"]`.
- Unit tests (`tests/unit/test_inversion_phase1_shadow_score_1595.py`, new file, 22 tests) cover the
  same case with hand-built synthetic rows (`test_temporal_reproduces_leads_read`), plus normalization,
  prefix-matching (unambiguous / below-threshold / ambiguous-multi-candidate), dropped/added reporting,
  REVIEW-exclusion, ERROR-as-nonmatch, the rendered-section text, and the real baseline doc's parse
  (93/39, TEMPORAL 4/4 MATCH — pins the doc against silent future edits).

## Task B — sharpen meeting_time / week_calendar descriptions

Edited `services/intent_service/workflow_entries.py` ONLY (the registry-derived source the grammar
actually reads — never a hand-written schema, never the router prompt, per PDR-006 condition 2):
- Added `_CALENDAR_QUERY_DESCRIPTIONS` dict, keyed by handler_attr, with sharpened one-line text for
  the two named operations only:
  - `_handle_meeting_time_query` → `"Meeting time today, on a specific day, or the next upcoming
    meeting (#1595)"`
  - `_handle_week_calendar_query` → `"Calendar for the week ahead, not a single day (#1595)"`
- The cohort construction loop now does
  `description = _CALENDAR_QUERY_DESCRIPTIONS.get(handler_attr, f"{handler_attr} via action dispatch
  (#1124)")` — `recurring_meetings` (the third cohort sibling) is NOT in the dict, so it keeps the
  generic fallback text unchanged, per the task's "do not touch any other operation's description."
- The `(#1595)` suffix is deliberately noise `_DESC_NOISE_RE` strips before the router ever sees it
  (same convention every other rail entry in this file uses) — it's provenance in the source, not
  prompt content.

**Before/after, quoted from `--dry-run`'s own grammar dump** (see Result section below for full
command output):
- BEFORE: `meeting_time … desc='_handle_meeting_time_query'`, `week_calendar … desc=
  '_handle_week_calendar_query'`
- AFTER: `meeting_time … desc='Meeting time today, on a specific day, or the next upcoming meeting'`,
  `week_calendar … desc='Calendar for the week ahead, not a single day'`
- Confirmed untouched: `recurring_meetings … desc='_handle_recurring_meetings_query'` (before AND
  after — identical both runs).

Did NOT run the re-score (no LLM calls anywhere this session, per dispatch instructions — the actual
re-score against these two sharpened descriptions is PM-gated and the Lead runs it).

## Gates (all read in full, quoted)

- `venv/bin/ruff format scripts/inversion_phase1_shadow_score.py services/intent_service/workflow_entries.py`:
  `1 file reformatted, 1 file left unchanged` (the shadow-score script; workflow_entries.py already
  clean).
- `venv/bin/ruff check --fix` same two files: `All checks passed!`
- `venv/bin/ruff format tests/unit/test_inversion_phase1_shadow_score_1595.py` +
  `ruff check --fix` same file: `1 file reformatted` / `All checks passed!`
- `venv/bin/python -m pytest tests/unit/test_inversion_phase1_shadow_score_1595.py
  tests/unit/test_inversion_phase2_gate_1595.py
  tests/unit/services/intent_service/test_inversion_flip_groups_1667.py -q -p no:cacheprovider`:
  **`89 passed in 1.11s`**
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q -p no:cacheprovider`:
  **`63 passed, 1 xfailed in 11.09s`**
- `scripts/run-sweep.sh ratchets` (env-stripped, `POSTGRES_PORT=5433`), full output read:
  ```
  73 passed, 1 xfailed in 18.22s
  --- mypy per-code gate (#1436) ---
  mypy gate: all 24 ratcheted codes at ceiling (total=1121; arg-type=364, assignment=227,
  attr-defined=69, call-arg=3, call-overload=6, dict-item=5, has-type=2, index=10, list-item=2,
  misc=77, no-redef=3, operator=63, override=17, return=1, return-value=48, union-attr=141,
  valid-type=14, var-annotated=69)
  ```
  `EXIT: 0`, separately verified.

No LLM calls anywhere in this session — every gate above and every `--dry-run` invocation is
deterministic (registry/grammar reads, markdown-table parsing, and synthetic-row unit tests).

## Result — quoted outputs

**Dry-run shared-subset cross-validation (Task A):**
```
baseline doc parsed: 93 rows from inversion-phase0-baseline-full-2026-08-12.md (39 asserted)
...
shared-subset cross-validation against inversion-phase1-shadow-score-2026-09-25.md: TEMPORAL shared=4 router=3/4 baseline=4/4 gate=REGRESSION
TEMPORAL dropped rows: []
TEMPORAL named regressions: ["what's on my calendar today?"]
```

**Grammar lines before/after (Task B), from `--dry-run`'s grammar dump:**
- Before: `meeting_time  [rail] aliases=['how_much_time_in_meetings', 'calendar_analysis']
  desc='_handle_meeting_time_query'`
  `week_calendar [rail] aliases=['week_ahead', 'whats_my_week_like'] desc='_handle_week_calendar_query'`
- After: `meeting_time  [rail] aliases=['how_much_time_in_meetings', 'calendar_analysis']
  desc='Meeting time today, on a specific day, or the next upcoming meeting'`
  `week_calendar [rail] aliases=['week_ahead', 'whats_my_week_like'] desc='Calendar for the week ahead,
  not a single day'`

## Verified how

- **Method**: every gate command above was run this turn and its full output read (not recalled from
  memory or an earlier pass); the before/after grammar text was captured by actually running
  `--dry-run` before editing `workflow_entries.py`, then again after, diffing the two real outputs
  (not predicted). The shared-subset TEMPORAL result was checked against Lead's read text in the
  source doc line-by-line before treating it as a match.
- **Layer**: this is grammar-derivation + report-generation + parsing logic, exercised through
  `derive_routing_grammar()` (the real, non-mocked registry-read path) and real markdown files on disk
  (the 08-12 baseline doc, the 09-25 report doc) — NOT a live routed classification (no LLM call
  anywhere). The unit tests for `compute_shared_subset` use hand-built synthetic `row_results`/baseline
  rows, stated as synthetic in the test file's own docstring (m-43) — they prove the scoring logic, not
  a live router draw. Whether the sharpened descriptions actually change the router's live decisions on
  the 14 TEMPORAL rows is unmeasured here by design (PM-gated re-score, Lead's call, not this session's).
- **Denominator**: 2 production files changed (`scripts/inversion_phase1_shadow_score.py`,
  `services/intent_service/workflow_entries.py`; `git diff --stat`: 357 insertions, 5 deletions across
  both) + 1 new test file (22 test cases, all passing) + this log. Full command-level coverage: 89
  targeted tests + 63+1xfail architecture-enforcement tests + 73+1xfail ratchet-sweep tests + mypy gate
  (24/24 ratcheted codes at ceiling, unchanged) — all re-run this turn, all green. `recurring_meetings`
  (the one calendar-cohort sibling deliberately left untouched) verified unchanged in both dry-run
  outputs, not merely asserted. No other operation's description touched — confirmed by `git diff
  services/intent_service/workflow_entries.py` showing only the `_CALENDAR_QUERY_DESCRIPTIONS` dict
  addition and the one-line lookup change in the cohort loop (24 lines changed total in that file, all
  within the calendar-cohort block).

## Sign-off
Did NOT commit, stage, or touch the git index per dispatch instructions — Lead Dev reviews and commits.
`git status` at handback: 2 modified tracked files
(`scripts/inversion_phase1_shadow_score.py`, `services/intent_service/workflow_entries.py`) + 2 new
untracked files (this log, `tests/unit/test_inversion_phase1_shadow_score_1595.py`) + the pre-existing
unrelated untracked `dev/active/canonical-retest-serving-llm.json` (present at session start, not
created by this session).
