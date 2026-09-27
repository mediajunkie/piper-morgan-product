# 2026-09-27 1235 — prog (Coding Agent) — #1595 Phase 3 GUIDANCE_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `GUIDANCE_PATTERNS` only (21 literals,
20 unexercised) — the next list in the Phase-3 deletion-gate pipeline after the
REMINDER_PATTERNS / REMINDER_QUERY_PATTERNS / TODO_QUERY_PATTERNS lanes. NO LLM calls
made. No pattern deleted. No flag changed. Did not touch git index (dispatcher's
instruction — no staging/commit performed).

## Read first (per dispatch prompt)

- `git show b3cdeb5f31` resolved to a merge commit with no phase3-conversion diff of
  its own — the real precedent commit is `558afa0f19` (`corpus(inversion): Phase 3
  pattern→corpus conversion for REMINDER (4), REMINDER_QUERY (3), TODO_QUERY (8)`),
  found via `git log --all --oneline --grep=phase3 -i`. Used its diff to
  `scripts/build_inversion_corpus_phase0.py` / `tests/fixtures/inversion_corpus_phase0.yaml`
  / `tests/unit/test_inversion_phase3_deletion_1595.py` as the format precedent.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — Phase 3 procedure
  and full progress log (units 1–5, first deletion).
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion
  gate" incl. "First deletion" subsection.
- `services/intent_service/pre_classifier.py`: `GUIDANCE_PATTERNS` (21 literals) and
  its consumer at `pre_classify` — confirmed it produces
  `category=GUIDANCE, action="get_contextual_guidance"` (list checked well before
  ANALYSIS/STATUS/etc.).
- `services/intent_service/action_registry.py` — confirmed `("GUIDANCE",
  "get_contextual_guidance")` is `ActionDisposition.CANONICAL` (not an alias), so
  every deposit row's `expected` is `action:get_contextual_guidance` with no
  alias note needed.
- Prior prog session log `dev/2026/09/27/2026-09-27-0805-prog-code-log-1595-phase3-deposits.md`
  — the verification methodology (`pre_classify_with_pattern_list` for list identity,
  `_first_pattern_match` for literal identity) and the rewording-for-shadowing lesson.

## What I did

1. Ran the gate: `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list
   GUIDANCE_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
   — confirmed 20 unexercised literals out of 21 (`\bget started\b` already exercised
   by the existing "how do I get started?" corpus row).

2. Derived one natural PM-style phrasing per unexercised literal and verified each
   empirically in a Python REPL against the real production matcher:
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list
     name == `"GUIDANCE_PATTERNS"`.
   - `PreClassifier._first_pattern_match(cleaned_phrase, PreClassifier.GUIDANCE_PATTERNS)`
     → asserted `.re.pattern` equals the specific cited literal.

   One finding: my first attempt "how do I set up my portfolio" was claimed by the
   earlier sibling literal `\bhow do i.*set up\b` before reaching the target
   `\bset up.*portfolio\b` — reworded to "I'd like to set up my portfolio" (no leading
   "how do I"), which verified cleanly. All 20 other phrases verified on the first
   attempt. No literal was unreachable/shadowed after rewording — all 20 landed.

3. Deposited a `# — GUIDANCE_PATTERNS` delimited block (extending the existing
   `# phase3-conversion` HAND_ROWS section) in `scripts/build_inversion_corpus_phase0.py`:
   20 rows, `category: GUIDANCE` (matching the existing "how do I get started?" row's
   convention, not the QUERY category used by the separate
   INTEGRATION_CONNECT_PATTERNS-claimed rows that also expect
   `get_contextual_guidance`), `expected: action:get_contextual_guidance`, each `source`
   citing `phase3-conversion/GUIDANCE_PATTERNS literal r"<the literal>"`.

4. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py`
   — 131 → 151 rows (+20). `git diff --stat` on the yaml: 81 insertions, 0 deletions
   (purely additive).

5. Updated the pinned corpus total in
   `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 131 → 151 (claimed 90 → 110,
   unclaimed unchanged at 41), docstring updated to name this deposit. Searched for
   other pinned corpus-size constants: `git grep -n "131" -- tests scripts` — no other
   hits besides the one just fixed (plus one unrelated `large_text.txt` line number and
   SVG binary noise, both irrelevant).

6. Re-ran the gate for GUIDANCE_PATTERNS: 21/21 literals now claimed, **0** "needs a
   corpus row before deletion" lines (grep-count confirmed). The 20 new rows correctly
   show `verdict=UNSCORED` — scoring is the Lead's budgeted (LLM-calling) run, not part
   of this unit.

7. Ran both dry-run validations — no LLM calls (each script self-reports this):
   - `inversion_phase1_shadow_score.py --dry-run` → "dry-run complete: corpus +
     grammar + selections validated, no LLM calls." Exit 0. Same pre-existing TEMPORAL
     shared-subset cross-validation note as prior sessions (`what's on my calendar
     today?` REGRESSION) — unrelated to and unaffected by GUIDANCE deposits (no
     TEMPORAL rows touched).
   - `inversion_phase2_gate.py --dry` → "dry run complete... No LLM calls made." Exit
     0. Reports `phase0 corpus: 151 rows (untouched)`.

8. Tests and gates (all run this turn, output quoted below):
   - `ruff format` + `ruff check --fix` on both touched `.py` files — one formatting
     pass needed on `build_inversion_corpus_phase0.py` (ruff rewrapped the multi-quote
     "process for" source string cleanly after I fixed an initially-ugly manual
     concatenation); `ruff format --check` + `ruff check` both clean on the second pass.
   - `tests/unit/test_inversion_phase3_deletion_1595.py` — 19 passed.
   - `tests/unit/services/intent_service/test_preclaim_shadow.py` — 29 passed.
   - `tests/test_architecture_enforcement.py` — 63 passed, 1 xfailed (unchanged
     baseline — extraction ceiling confirmed still 558 via
     `pattern_literal_counts.total_literal_count()`, since deposits add corpus rows
     only and touch no pre_classifier literal).

9. Added a progress-log line to
   `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Rows added — GUIDANCE_PATTERNS (category GUIDANCE, expected `action:get_contextual_guidance`)

| phrase | literal exercised |
|---|---|
| "where should I focus this week" | `\bwhere should i focus\b` |
| "I could use some guidance on this" | `\bguidance\b` |
| "do you have a recommendation" | `\brecommendation\b` |
| "what's your advice here" | `\badvice\b` |
| "ok that's merged, what now?" | `\bwhat now\b` |
| "what are the next steps" | `\bnext steps\b` |
| "what should I do about this bug" | `\bwhat should (i\|we) do (about\|with)\b` |
| "advise me on this decision" | `\badvise (me\|us) on\b` |
| "what's the process for filing a bug" | `\bwhat('?s\| is) the process for\b` |
| "can you help me setup the integration" | `\bhelp.*setup\b` |
| "can you help me configure the connector" | `\bhelp.*configure\b` |
| "I need to setup my projects" | `\bsetup.*projects?\b` |
| "how do I configure my projects" | `\bconfigure.*projects?\b` |
| "how do I setup the connector" | `\bhow do i.*setup\b` |
| "how do I configure the connector" | `\bhow do i.*configure\b` |
| "just getting started here" | `\bgetting started\b` |
| "can you help me set up the integration" | `\bhelp.*set up\b` |
| "I want to set up my projects" | `\bset up.*projects?\b` |
| "how do I set up the connector" | `\bhow do i.*set up\b` |
| "I'd like to set up my portfolio" | `\bset up.*portfolio\b` (reworded from "how do I set up my portfolio" to avoid the earlier sibling literal `\bhow do i.*set up\b` stealing the claim first) |

**Unreachable/shadowed literals found**: none. All 20 target literals were reachable
with a natural phrasing; one required rewording to avoid an earlier literal in the
same list stealing the claim.

## Gate output — before

```
=== GUIDANCE_PATTERNS ===
corpus denominator: 131 rows total = 90 claimed + 41 unclaimed
## GUIDANCE_PATTERNS
literals: 21  |  rows claimed: 1/131
verdict: GO (deletable) — deleting removes 21 literals: ceiling 567 -> 546
rows claimed:
  [OK] "how do I get started?" -> claim=get_contextual_guidance expected=REVIEW router=get_contextual_guidance@0.9 verdict=REVIEW :: REVIEW-agrees (route=get_contextual_guidance == claim=get_contextual_guidance)
pattern->corpus conversion needed (20 literal(s) unexercised):
  needs a corpus row before deletion: r"\bwhere should i focus\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bguidance\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\brecommendation\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\badvice\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bwhat now\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bnext steps\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bwhat should (i|we) do (about|with)\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\badvise (me|us) on\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bwhat('?s| is) the process for\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhelp.*setup\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhelp.*configure\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bsetup.*projects?\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bconfigure.*projects?\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhow do i.*setup\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhow do i.*configure\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bgetting started\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhelp.*set up\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bset up.*projects?\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bhow do i.*set up\b"  (list=GUIDANCE_PATTERNS)
  needs a corpus row before deletion: r"\bset up.*portfolio\b"  (list=GUIDANCE_PATTERNS)
```

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 151 rows total = 110 claimed + 41 unclaimed

## GUIDANCE_PATTERNS
literals: 21  |  rows claimed: 21/151
verdict: NO-GO

rows claimed:
  [OK] "how do I get started?" -> claim=get_contextual_guidance expected=REVIEW router=get_contextual_guidance@0.9 verdict=REVIEW :: REVIEW-agrees (route=get_contextual_guidance == claim=get_contextual_guidance)
  [FAIL] "where should I focus this week" -> claim=get_contextual_guidance expected=action:get_contextual_guidance router=None@None verdict=UNSCORED :: UNSCORED; not-live (...)
  [FAIL] "I could use some guidance on this" -> ... verdict=UNSCORED
  [FAIL] "do you have a recommendation" -> ... verdict=UNSCORED
  [FAIL] "what's your advice here" -> ... verdict=UNSCORED
  [FAIL] "ok that's merged, what now?" -> ... verdict=UNSCORED
  [FAIL] "what are the next steps" -> ... verdict=UNSCORED
  [FAIL] "what should I do about this bug" -> ... verdict=UNSCORED
  [FAIL] "advise me on this decision" -> ... verdict=UNSCORED
  [FAIL] "what's the process for filing a bug" -> ... verdict=UNSCORED
  [FAIL] "can you help me setup the integration" -> ... verdict=UNSCORED
  [FAIL] "can you help me configure the connector" -> ... verdict=UNSCORED
  [FAIL] "I need to setup my projects" -> ... verdict=UNSCORED
  [FAIL] "how do I configure my projects" -> ... verdict=UNSCORED
  [FAIL] "how do I setup the connector" -> ... verdict=UNSCORED
  [FAIL] "how do I configure the connector" -> ... verdict=UNSCORED
  [FAIL] "just getting started here" -> ... verdict=UNSCORED
  [FAIL] "can you help me set up the integration" -> ... verdict=UNSCORED
  [FAIL] "I want to set up my projects" -> ... verdict=UNSCORED
  [FAIL] "how do I set up the connector" -> ... verdict=UNSCORED
  [FAIL] "I'd like to set up my portfolio" -> ... verdict=UNSCORED
```

`[FAIL]`/NO-GO/UNSCORED is EXPECTED and correct for this unit — the deposit rows score
`UNSCORED` until the Lead's budgeted (LLM-calling) shadow-score run judges them; that
run is explicitly out of scope here. What this unit was required to produce, and did:
**zero** "needs a corpus row before deletion" lines for GUIDANCE_PATTERNS, confirmed by
grep count (0).

## New corpus total

131 → **151** rows (+20). Per-category denominators after rebuild: QUERY 39,
**GUIDANCE 26** (was 6), TEMPORAL 21, EXECUTION 18, PORTFOLIO 16, STATUS 8,
CONVERSATION 5, SYNTHESIS 4, PRIORITY 3, IDENTITY 3, MEMORY 3, DISCOVERY 2,
PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 151 rows (59
  REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml` → `1 file changed, 81
  insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0,
  "no LLM calls" self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls
  made" self-reported; `phase0 corpus: 151 rows (untouched)`.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list GUIDANCE_PATTERNS
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 0 "needs a corpus row" lines (grep-confirmed).
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` →
  **19 passed**, exit 0.
- `venv/bin/python -m pytest
  tests/unit/services/intent_service/test_preclaim_shadow.py -q` → **29 passed**,
  exit 0.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63
  passed, 1 xfailed**, exit 0 (unchanged from baseline).
- `venv/bin/python -c "import pattern_literal_counts as plc;
  print(plc.total_literal_count())"` → **558**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted).
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files → clean
  after one formatting pass (ruff rewrapped a manually-concatenated source string);
  `ruff format --check` + `ruff check` both clean on re-run.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +20 rows in a
  `# — GUIDANCE_PATTERNS` delimited block, extending the existing `# phase3-conversion`
  section)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive,
  131→151 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected
  131→151, with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log line
  added)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
any flag/env var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion
performed by this unit).

## Verified how

- **Method**: for each of the 20 deposited phrases, called the REAL production
  functions directly in a Python REPL against this worktree's code —
  `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion) and
  `PreClassifier._first_pattern_match(cleaned, PreClassifier.GUIDANCE_PATTERNS)`
  (literal-identity assertion) — not a re-derived regex, not a read-and-guess. Gate
  re-runs, pytest, and ruff invocations were all run this turn via Bash and their
  output is quoted/counted above, not recalled from memory.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of
  this unit — the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls
  made anywhere in this session, confirmed by each script's own self-report and the
  absence of any LLM-client invocation in the commands run).
- **Denominator**: 1 target list (GUIDANCE_PATTERNS) — 20 of 20 previously-flagged
  unexercised literals now have a corpus row; 0 "needs a corpus row" lines (grep-count
  confirmed, not sampled). Test denominator: 19/19 in the target Phase-3 test file
  pass, 29/29 in the pre-claim shadow test file pass, 63 passed + 1 xfailed
  (pre-existing, unrelated) in the full architecture-enforcement suite (full file run,
  not a subset). Ceiling denominator: 558/558 unchanged, confirmed by direct AST-walk
  call, not inferred.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md`
  §"Phase 3 — deletion gate" (the gate's contract + precedence rules);
  `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress
  log); prior prog session log `2026-09-27-0805-prog-code-log-1595-phase3-deposits.md`
  (verification methodology, format precedent); `action_registry.py`
  (`ActionDisposition.CANONICAL` lookup for `get_contextual_guidance`).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline
  sections (this is a bounded prog dispatch inside an existing worktree — no mailbox
  write, no sign-off merge, per dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient.

## Discovered work

None filed. No unreachable/shadowed literal found after the one rewording — reported
inline in the deposited row's `notes` field, not filed as a separate issue (same
convention as the prior deposit session).
