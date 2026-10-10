# Session log — Coding Agent (prog-code), 2026-10-10 08:15 PDT

**Model**: Sonnet 5 (claude-sonnet-5)
**Role**: Coding Agent (prog-code), dispatched by Lead Developer
**Issue**: #1970 (ADR-080 D1/D6) — Arch's design item 1 (router prompt) + what the full-corpus run
needs to SCORE framing. Step 1 (plumbing, `RoutingDecision.framing` parsing/validation, `evaluate_consent`
asymmetry, disagreement telemetry) landed earlier today (2d7426baa4) by a prior prog-code session
(`2026-10-10-0650-prog-code-log-1970-framing-plumbing.md`).
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Constraint**: no commit/push/mail/LLM calls — Lead reviews, lands, and runs the served scoring himself.

## What I was asked to build

1. Router prompt (`inversion_router.py` `_SYSTEM_PROMPT`): add the top-level `"framing"` field to the
   JSON schema the prompt asks for, one line per gate value with one example each, beside `"outcome"`
   in both the single-op and plan shapes.
2. Corpus: an EXPECTED-framing mapping the scorer uses, without hand-editing ~570 rows.
3. Scorer (`inversion_phase1_shadow_score.py`): record the router's `framing` per row, add a framing
   verdict column (appended LAST so the deletion gate's column-sliced parsers don't shift), plus a
   framing summary section — while keeping every existing column/section/parser working.
4. Tests: deterministic, no LLM.
5. Update `intent-routing-stack.md`.

## What I did

**1. Prompt** (`services/intent_service/inversion_router.py`): added a bullet describing `"framing"`
(execute/compose/ambiguous, one example each, verbatim from Arch's design: "close issue 12" → execute;
"help me draft a reply to this issue" → compose; "my default repo should be X" / "I'd like to start a
project" / "can you close issue 12?" → ambiguous). Added `"framing": "execute|compose|ambiguous"` to
BOTH the single-op JSON example and the plan JSON example (top-level, beside `"outcome"` in the plan
case — never nested in an element). No operation description touched. Existing ordering assertions
(`single_idx < plan_idx` in `test_plan_rule_in_prompt_is_the_exception_not_the_default`) still hold.

**2. Corpus mapping** (`scripts/inversion_phase0_baseline.py`, new functions `expected_framing_for_row`
and `framing_expectation_denominators`):
- `framing: question` / `framing: declarative` → `ambiguous` (the corpus's own existing 3-row marker,
  the one `TestExecuteVocabCoverage` already reads).
- A row whose `expected:` action resolves (via `derive_routing_grammar().alias_to_canonical` +
  `get_action_workflows()`, with the SAME `manage_repos` → `list_repos`/`link_repo` special-case
  resolution `TestExecuteVocabCoverage._repo_management_list_literals` uses — duplicated by the same
  "no shared import boundary from scripts/ into tests/" precedent that test's own docstring cites,
  not re-invented) to a rail entry declared `EffectClass.WRITE` → `execute`. This is exactly the scope
  `TestExecuteVocabCoverage._write_or_allowlisted_destructive_corpus_rows` +
  `test_every_corpus_write_phrase_classifies_execute` already assert classifies EXECUTE via the real
  gate classifier — reused as ground truth, never re-derived. DESTRUCTIVE-resolved rows get NO
  expectation (Arch's design item 3: framing is irrelevant for DESTRUCTIVE, CONFIRM in every cell).
- "compose": searched the corpus and the test suite — no `framing: compose` row, no test naming a
  compose-phrasing row set. Did not guess any row into this bucket; `framing_expectation_denominators`
  always reports a `compose` key so the zero is visible, not a missing key.
- Everything else → `None` (not scored).

**Denominators on the real 577-row corpus** (verified via `--dry-run`, no LLM call):
`execute=63 ambiguous=3 compose=0 none=511` (total=577).

**3. Scorer** (`scripts/inversion_phase1_shadow_score.py`):
- `score()` now computes `framing_expected` / `framing_got` / `framing_verdict` per row (additive;
  `router_matches`/operation verdict untouched) and a `framing_summary` dict (`{value: {matched,
  expected}}` for execute/ambiguous/compose).
- `build_report()`: the "Row detail (asserted rows)" table gets ONE new column, `framing`, APPENDED
  LAST (`| ... | note | framing |`) — cell is `-` when no expectation, else `{expected}:MATCH` or
  `{expected}:MISMATCH({got})`. A new "## Framing score" section renders the per-value matched/expected
  table plus the stated "(no expectation)" denominator (m-44).
- `run()`'s `--dry-run` branch now prints the expected-framing denominators before any LLM spend.
- Did NOT touch `parse_phase1_report_row_detail` (still `cols[:6]`) — appending last means both the
  existing committed 2026-09-25 report (no framing column) and a new-format sample parse identically
  on every pre-existing column. Proved this with a unit test comparing an old-format and new-format
  synthetic table, PLUS re-running the existing `TestParsePhase1ReportRowDetail` /
  `test_real_committed_report_still_parses` against the real, already-committed
  `inversion-phase1-shadow-score-2026-09-25.md`. The deletion gate's own parsers
  (`scripts/inversion_phase3_deletion_gate.py::parse_asserted_rows`/`parse_review_rows`) also slice a
  fixed `cols[:N]` prefix — did not need to touch them; their existing tests
  (`TestReportParsers::test_parse_asserted_rows_retains_route` / `test_parse_review_rows`, against
  `gate.FULL_REPORT` = the same 2026-09-25 doc) still pass unmodified, which is itself proof the old
  format still parses through the gate's own code path.

**4. Tests** (no LLM, `-m "not llm"`):
- `tests/unit/services/intent_service/test_inversion_router_1595.py`: new
  `test_framing_schema_and_examples_are_in_the_system_prompt` — asserts the schema field, all three
  values, all three examples verbatim, and that both JSON occurrences of the framing field are at the
  top level (ordering: `single_idx < plan_idx < framing_in_plan_idx`).
- `tests/unit/test_inversion_phase1_shadow_score_1595.py`: new classes
  `TestExpectedFramingForRow` (synthetic representative rows for each branch, plus a cross-check
  against the two live `manage_repos` corpus rows), `TestFramingExpectationDenominators` (including a
  vacuity guard against the real corpus — m-44), `TestScoreRecordsFraming` (MATCH/MISMATCH/no-
  expectation/summary), `TestRowDetailTableParsesOldAndNewFormat` (old-vs-new-format synthetic
  round-trip + the real committed report).

**5. Docs**: added a short subsection to `intent-routing-stack.md` under the existing #1970 step-1
entry ("The router prompt now asks for framing") describing the prompt change, the expected-framing
derivation, and the scorer's additive column/summary — flagging that this is a catalog-description-
surface change (rule 7) requiring a full-corpus served run before it ships live.

## Verification (quoted verbatim)

Env stripped per CLAUDE.md throughout: `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL
-u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS -u OPENAI_API_KEY POSTGRES_PORT=5433`.

**tests/unit** (`-m "not llm" -q -p no:cacheprovider -o addopts="--ignore=tests/archive
--ignore=services/integrations --ignore=dev/ --import-mode=importlib"`):
```
12809 passed, 227 skipped, 3 deselected, 173 warnings in 255.68s (0:04:15)
```

**tests/integration + tests/intent**, diffed against an `origin/main` baseline in a scratch worktree
(`git worktree add --detach /tmp/pm1970scratch/b1970b origin/main`, removed after), run sequentially
(baseline first, then current branch, same Postgres):
- Baseline: `31 failed, 848 passed, 36 skipped, 136 deselected, 6 xfailed, 126 warnings in 94.83s`
- Current: `31 failed, 848 passed, 36 skipped, 136 deselected, 6 xfailed, 126 warnings in 90.85s`
- `diff <(grep "^FAILED" baseline|sort) <(grep "^FAILED" current|sort)` → empty (byte-identical FAILED
  sets). Two lines my first `^(FAILED|ERROR)` grep caught were structlog application-log lines
  (`ERROR    web.api.routes.intent:...`), not pytest report lines — confirmed present identically
  (same message, different timestamp) in both logs; re-filtered to `^(FAILED|ERROR) tests/` for the
  rest-of-tests comparison below. **0 new failures.**

**Rest of tests/** (`--ignore=tests/unit --ignore=tests/integration --ignore=tests/intent` added, same
baseline-worktree method):
- Baseline: `18 failed, 1482 passed, 48 skipped, 258 deselected, 63 warnings, 10 errors in 138.91s`
- Current: `18 failed, 1483 passed, 47 skipped, 258 deselected, 63 warnings, 10 errors in 137.90s`
- `comm -13 baseline.failed.sorted current.failed.sorted` (both `grep -E "^(FAILED|ERROR) tests/"`,
  110→28 lines after removing the app-log false positives) → empty. **0 new failures.** (The
  1482→1483 passed / 48→47 skipped shift is a pre-existing one-test skip/pass flip unrelated to any
  FAILED/ERROR line — not a gate violation; did not chase further given the explicit gate is the
  FAILED/ERROR diff.) `test_pm034_claims_validation`'s latency test appeared in BOTH baseline and
  current (pre-existing flake, not new) — no rerun needed per the "if it appears [as new]" instruction.

**tests/test_architecture_enforcement.py + tests/test_completion_ratchets.py**:
```
81 passed in 20.61s
```

**ruff**: `ruff format --check .` initially flagged 4 files (my own edits, unformatted); ran
`ruff check --fix` (one import-sort fix in `inversion_phase1_shadow_score.py`) + `ruff format` on the
5 touched files. Final:
```
1915 files already formatted
All checks passed!
```
Re-ran the affected test files after formatting — all still green (see combined run below).

**mypy gate** (`venv-mypy-gate/bin/python scripts/check_mypy_gate.py`):
```
mypy gate: all 24 ratcheted codes at ceiling (total=1104; arg-type=355, assignment=219,
attr-defined=69, call-arg=3, call-overload=6, dict-item=5, has-type=2, index=10, list-item=2,
misc=77, no-redef=3, operator=63, override=17, return=1, return-value=48, union-attr=141,
valid-type=14, var-annotated=69)
```
No new codes, ceiling unchanged.

**Post-format combined re-run** (router/consent/scorer/gate/enforcement/ratchets):
```
276 passed, 1 deselected in 34.24s
```

**`--dry-run`** (`venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run`), no LLM calls:
```
corpus: 577 rows · grammar: 72 canonical operations (+NONE/CLARIFY), 86 aliases collapsed input-side
exhibit-A selection: 16 rows (expected 8) + demanded row present
baseline doc parsed: 93 rows from inversion-phase0-baseline-full-2026-08-12.md (39 asserted)
dry-run complete: corpus + grammar + selections validated, no LLM calls.
expected-framing denominators: execute=63 ambiguous=3 compose=0 none=511 (total=577, rows=577)
shared-subset cross-validation against inversion-phase1-shadow-score-2026-09-25.md: TEMPORAL shared=4
router=3/4 baseline=4/4 gate=REGRESSION
TEMPORAL dropped rows: []
TEMPORAL named regressions: ["what's on my calendar today?"]
```

**Verified how**: every number above is this turn's actual command output, quoted verbatim, not a
remembered prior run. Layer measured: unit tests measure the pure functions (scorer, corpus mapping,
prompt string) with no LLM in the loop; the integration/intent/rest-of-tests runs measure
collection+fixture-level behavior against a real Postgres, diffed against a freshly-built
`origin/main` scratch worktree (not a remembered baseline number) on the SAME Postgres, sequentially.
Denominator: tests/unit = 12809+227+3 = 13039 collected; integration+intent = 848+31+36+6 = 921;
rest-of-tests = 1483+18+47+10 = 1558 (current). The full-corpus SERVED run (rule 7, ~570 router calls)
was explicitly NOT run here — that is Lead's to run, per the task's constraint.

## What I did NOT do (out of scope for this unit, per the brief)

- Arch's design item (5), the `_EXECUTE_RE`/`MAX_EXECUTE_ALTERNATIVES` ratchet — not asked for here.
- No commit, push, mail, or LLM/API call of any kind.
- No full-corpus served-model scoring run — Lead runs that himself.

## Files touched

- `services/intent_service/inversion_router.py` — prompt schema + examples.
- `scripts/inversion_phase0_baseline.py` — `expected_framing_for_row`, `framing_expectation_denominators`.
- `scripts/inversion_phase1_shadow_score.py` — `score()` framing fields/summary, `build_report()`
  framing column + section, `--dry-run` denominators print.
- `tests/unit/services/intent_service/test_inversion_router_1595.py` — prompt content test.
- `tests/unit/test_inversion_phase1_shadow_score_1595.py` — expected-framing, scorer, parser
  round-trip tests.
- `docs/internal/architecture/current/intent-routing-stack.md` — new subsection.

## Memory & briefing surfaces referenced this session

**Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` (mandatory pre-read, and
the file I updated) — router/consent/scoring architecture; issue #1970 + its comment thread (Arch's
design, Lead's step-1 landing report) — the spec this unit implements; `tests/
test_architecture_enforcement.py::TestExecuteVocabCoverage` — the exact definition reused for the
corpus WRITE/verb-initial-imperative scope (not re-derived).

**Loaded but not referenced**: CLAUDE.md's worktree/mailbox/sign-off sections (no commit/mail this
session, so not exercised); the glossary.

**Wanted but not found**: a corpus or test marker for "compose" framing — confirmed absent by search
rather than assumed; reported as a 0-count, not guessed.

## Discovered work

None filed. No new issues discovered during this unit.
