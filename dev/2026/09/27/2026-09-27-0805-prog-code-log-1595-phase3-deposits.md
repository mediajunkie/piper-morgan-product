# 2026-09-27 0805 — prog (Coding Agent) — #1595 Phase 3 pattern→corpus deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for the three lists the Phase-3
deletion gate (`scripts/inversion_phase3_deletion_gate.py`) reported as
"needs a corpus row before deletion": `REMINDER_PATTERNS`,
`REMINDER_QUERY_PATTERNS`, `TODO_QUERY_PATTERNS`. NO LLM calls made. No
pattern deleted. No flag changed. Did not touch git index (dispatcher's
instruction — no staging/commit performed).

## Read first (per dispatch prompt)

- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 —
  deletion gate" (lines ~1129-1183)
- `scripts/inversion_phase3_deletion_gate.py` (full read)
- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS shape + main())
- Exhibit-A precedent commit `5ec59b8098` (`corpus(inversion): Exhibit-A
  completeness (1595 exit test)`) — used as the format precedent for
  hand-inlined rows with citations
- `services/intent_service/pre_classifier.py`: `REMINDER_PATTERNS`,
  `REMINDER_QUERY_PATTERNS` (+ `REMINDER_QUERY_BLOCKERS`), `TODO_QUERY_PATTERNS`
  (+ `RESTORATIVE_ASK_BLOCKERS`, `_is_destructive_ask`), the action-refinement
  helpers `_get_todo_action` (single-intent path has its own inline refinement
  with THREE buckets: `list_completed_todos` / `list_todos_query` /
  `next_todo_query`, more granular than the multi-intent path's `_get_todo_action`
  which only splits list vs next) and the pre_classify order (confirmed
  REMINDER_QUERY_PATTERNS → REMINDER_PATTERNS → TODO_COMPLETE_PATTERNS →
  TODO_QUERY_PATTERNS, all well before PRIORITY_PATTERNS)

## What I did

1. Ran the gate for all three lists — confirmed the task brief's expected
   counts exactly: REMINDER_PATTERNS 4 unexercised literals,
   REMINDER_QUERY_PATTERNS 3, TODO_QUERY_PATTERNS 8 (15 total).

2. For each of the 15 literals, derived one natural phrasing from the
   regex's own words and **proved it empirically** against the real
   production matcher (not by reading the regex and guessing):
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted the
     returned list name equals the target list.
   - `PreClassifier._first_pattern_match(cleaned_phrase, target_list_patterns)`
     → asserted the returned match's `.re.pattern` equals the SPECIFIC cited
     literal (not just "some literal in the list" — the gate's
     `unexercised_literals()` counts a literal exercised only when it's the
     FIRST pattern in list order to fire on a claiming row, so a phrase whose
     first hit is an earlier sibling literal in the same list doesn't count).

   One finding from this step: my first attempt at "show all my todos"
   (with "my") always hit `\bmy todos\b` (an earlier, already-exercised
   literal in `TODO_QUERY_PATTERNS`) before reaching
   `\bshow\s+all\s+(?:my\s+)?todos\b` — had to drop "my" ("show all todos")
   to isolate the target literal. Similarly "what do I do next" does NOT
   match `\bwhat.*next.*do\b` (the literal requires "next" to appear
   textually BEFORE "do" — the phrase has "do" before "next" twice) and
   fell through to `PRIORITY_PATTERNS` instead; I did not force that phrase
   in — I rephrased to "what do I have next to do" (next-before-do word
   order) and verified it lands on the correct literal. (No literal was
   reported unreachable/shadowed after rephrasing — all 15 landed cleanly.)

3. Deposited a `# phase3-conversion` delimited block per list into
   `HAND_ROWS` in `scripts/build_inversion_corpus_phase0.py`, each row citing
   `source: "phase3-conversion/<LIST_NAME> literal r\"<the literal>\""`.
   `category` follows the existing asserted-row convention for these actions
   (verified against existing corpus rows, not guessed): TEMPORAL for
   reminder actions (`create_reminder`, `list_reminders_query`), QUERY for
   todo actions. `expected` uses the REGISTRY CANONICAL action
   (`scripts/inversion_phase1_shadow_score.py --dry-run`'s grammar table:
   `list_completed_todos` and `next_todo_query` are aliases of canonical
   `list_todos_query`; `create_reminder` and `list_reminders_query` are
   themselves canonical) — so all 5 TODO_QUERY_PATTERNS deposit rows carry
   `expected: action:list_todos_query` even though surface 1's raw claim on
   3 of them is the alias action name (noted per-row).

4. Regenerated the yaml (`venv/bin/python scripts/build_inversion_corpus_phase0.py`)
   — 116 → 131 rows (+15, exactly the deposit count). `git diff --stat` on
   the yaml: `1 file changed, 65 insertions(+)` — zero deletions (the lone
   `^-` line in a raw diff grep is just the `---` file header). Purely
   additive, confirmed.

5. Ran both dry-run validations — no LLM calls (confirmed by each script's
   own printed statement):
   - `inversion_phase1_shadow_score.py --dry-run` → "dry-run complete: corpus
     + grammar + selections validated, no LLM calls." Exit 0. (The script
     also prints a pre-existing TEMPORAL shared-subset cross-validation note
     against the 2026-09-25 report — `gate=REGRESSION` on
     "what's on my calendar today?" — this is the documented
     pre-sharpening-vs-rescore precedence gap the routing-stack doc already
     describes, unrelated to and unaffected by my TEMPORAL deposits, which
     have `expected: action:` values, not REVIEW, and were not part of that
     2026-09-25 report to begin with.)
   - `inversion_phase2_gate.py --dry` → "dry run complete: fixtures build the
     real dataclass, serialize under the cap, pairs are twinned. No LLM calls
     made." Exit 0. Reports `phase0 corpus: 131 rows (untouched)`.

6. Re-ran the gate for all three lists — each now reports **0** "needs a
   corpus row" lines (grep count confirmed 0/0/0) and the 15 new rows show
   `verdict=UNSCORED` (no router verdict — correctly not scored by this
   unit, per the dispatch instruction that scoring is the Lead's budgeted
   run). Full verdict blocks quoted below.

7. Tests:
   - `tests/unit/test_inversion_phase2_gate_1595.py` +
     `tests/unit/test_inversion_phase3_deletion_1595.py`: one failure —
     `TestCensusDenominators::test_claimed_plus_unclaimed_equals_corpus_size`
     had `116` pinned. Fixed honestly to `131` (claimed 99 + unclaimed 32 =
     131; unclaimed count unchanged since all 15 new rows are claimed by
     design) with an updated docstring naming this deposit. Searched both
     files for any other pinned `116`/`84` counts — none found. Re-ran: 41
     passed.
   - `tests/test_architecture_enforcement.py`: 63 passed, 1 xfailed (no
     change from baseline — I did not touch any extraction-pattern surface,
     only corpus data + one test's pinned constant).
   - `ruff format` + `ruff check --fix` on
     `scripts/build_inversion_corpus_phase0.py` and
     `tests/unit/test_inversion_phase3_deletion_1595.py`: both clean, no
     changes needed.

## Rows added

### REMINDER_PATTERNS (category TEMPORAL, expected `action:create_reminder`)
| phrase | literal exercised |
|---|---|
| "set a reminder for the dentist appointment" | `\bset\s+(?:a\s+)?reminder\b` |
| "create a reminder to call the plumber" | `\bcreate\s+(?:a\s+)?reminder\b` |
| "don't let me forget to submit the report" | `\bdon'?t\s+let\s+me\s+forget\b` |
| "I need to remember to submit my timesheet" | `\bneed\s+to\s+remember\s+to\b` |

### REMINDER_QUERY_PATTERNS (category TEMPORAL, expected `action:list_reminders_query`)
| phrase | literal exercised |
|---|---|
| "what are my reminders" | `\bmy reminders\b` |
| "show reminders" | `\b(?:show\|list\|view\|see\|check)\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?reminders\b` |
| "do I have any reminders" | `\bdo i have (?:any\s+)?reminders\b` |

### TODO_QUERY_PATTERNS (category QUERY, expected `action:list_todos_query` [canonical])
| phrase | literal exercised | surface-1 raw claim |
|---|---|---|
| "show todos" | `\bshow\s+(?:my\s+)?todos\b` | list_todos_query |
| "list my todos" | `\blist\s+(?:my\s+)?todos\b` | list_todos_query |
| "what are my todos" | `\bwhat are my todos\b` | list_todos_query |
| "show me completed todos" | `\bshow.*completed\s+todos\b` | list_completed_todos (alias) |
| "show all todos" | `\bshow\s+all\s+(?:my\s+)?todos\b` | list_completed_todos (alias) |
| "next todo" | `\bnext todo\b` | next_todo_query (alias) |
| "what should I do next" | `\bwhat should i do next\b` | next_todo_query (alias) |
| "what do I have next to do" | `\bwhat.*next.*do\b` | next_todo_query (alias) |

**Unreachable/shadowed literals found**: none. All 15 target literals were
reachable with a natural phrasing once word order / absence of a
shadowing sibling substring was respected (two required rephrasing to avoid
an earlier literal in the same list stealing the claim — see item 2 above).

## Gate verdict blocks after deposit (2026-09-27, no `--live`)

```
=== REMINDER_PATTERNS ===
corpus denominator: 131 rows total = 99 claimed + 32 unclaimed
## REMINDER_PATTERNS
literals: 5  |  rows claimed: 5/116
verdict: NO-GO
rows claimed:
  [OK] "remind me to review the roadmap tomorrow" -> claim=create_reminder expected=REVIEW router=create_reminder@1.0 verdict=REVIEW :: REVIEW-agrees (route=create_reminder == claim=create_reminder)
  [FAIL] "set a reminder for the dentist appointment" -> claim=create_reminder expected=action:create_reminder router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "create a reminder to call the plumber" -> claim=create_reminder expected=action:create_reminder router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "don't let me forget to submit the report" -> claim=create_reminder expected=action:create_reminder router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "I need to remember to submit my timesheet" -> claim=create_reminder expected=action:create_reminder router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
```

```
=== REMINDER_QUERY_PATTERNS ===
corpus denominator: 131 rows total = 99 claimed + 32 unclaimed
## REMINDER_QUERY_PATTERNS
literals: 4  |  rows claimed: 4/116
verdict: NO-GO
rows claimed:
  [OK] "what reminders do I have?" -> claim=list_reminders_query expected=REVIEW router=list_reminders_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=list_reminders_query == claim=list_reminders_query)
  [FAIL] "what are my reminders" -> claim=list_reminders_query expected=action:list_reminders_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "show reminders" -> claim=list_reminders_query expected=action:list_reminders_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "do I have any reminders" -> claim=list_reminders_query expected=action:list_reminders_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
```

```
=== TODO_QUERY_PATTERNS ===
corpus denominator: 131 rows total = 99 claimed + 32 unclaimed
## TODO_QUERY_PATTERNS
literals: 10  |  rows claimed: 11/116
verdict: NO-GO
rows claimed:
  [OK] "show me my todos" -> claim=list_todos_query expected=REVIEW router=list_todos_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=list_todos_query == claim=list_todos_query)
  [OK] "show all my todos" -> claim=list_completed_todos expected=REVIEW router=list_todos_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=list_todos_query == claim=list_completed_todos)
  [OK] "what's my next todo?" -> claim=next_todo_query expected=REVIEW router=list_todos_query@1.0 verdict=REVIEW :: REVIEW-agrees (route=list_todos_query == claim=next_todo_query)
  [FAIL] "show todos" -> claim=list_todos_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "list my todos" -> claim=list_todos_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "what are my todos" -> claim=list_todos_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "show me completed todos" -> claim=list_completed_todos expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "show all todos" -> claim=list_completed_todos expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "next todo" -> claim=next_todo_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "what should I do next" -> claim=next_todo_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
  [FAIL] "what do I have next to do" -> claim=next_todo_query expected=action:list_todos_query router=None@None verdict=UNSCORED :: UNSCORED; live-set-unknown
```

Note: the `[FAIL]`/`NO-GO` marks here are EXPECTED and correct for this
unit — a row scores `[FAIL]`/UNSCORED until the (budgeted, LLM-calling)
Phase-1 shadow-score run judges it; that run is explicitly NOT part of this
task. What this unit was required to produce, and did produce, is **zero**
"needs a corpus row before deletion" lines per list — confirmed by grep
count (0/0/0) above.

## New corpus total

116 → **131** rows (+15). Per-category denominators after rebuild:
QUERY 39, TEMPORAL 21, EXECUTION 18, PORTFOLIO 16, STATUS 8, GUIDANCE 6,
CONVERSATION 5, SYNTHESIS 4, PRIORITY 3, IDENTITY 3, MEMORY 3, DISCOVERY 2,
PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 131
  rows (59 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml` → `1 file
  changed, 65 insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` →
  exit 0, "no LLM calls" self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM
  calls made" self-reported.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list <L>` for
  all three lists → each exit 0, 0 "needs a corpus row" lines.
- `venv/bin/python -m pytest tests/unit/test_inversion_phase2_gate_1595.py
  tests/unit/test_inversion_phase3_deletion_1595.py -q` → **41 passed**,
  exit 0 (after fixing the one honestly-stale pinned `116` → `131`).
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` →
  **63 passed, 1 xfailed**, exit 0.
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files →
  clean, no changes needed.

## Files touched

- `/Users/xian/Development/piper-morgan-worktrees/lead/scripts/build_inversion_corpus_phase0.py`
  (HAND_ROWS: +15 rows in a delimited `# phase3-conversion` block)
- `/Users/xian/Development/piper-morgan-worktrees/lead/tests/fixtures/inversion_corpus_phase0.yaml`
  (regenerated, purely additive, 116→131 rows)
- `/Users/xian/Development/piper-morgan-worktrees/lead/tests/unit/test_inversion_phase3_deletion_1595.py`
  (one pinned constant corrected 116→131, with updated docstring)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read
only), any flag/env var, `scripts/inversion_phase3_deleted_patterns.json`
(still empty — no deletion performed by this unit).

## Verified how

- **Method**: for each of the 15 deposited phrases, called the REAL
  production functions directly in a Python REPL against this worktree's
  code — `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name
  assertion) and `PreClassifier._first_pattern_match(cleaned, target_list)`
  (literal-identity assertion) — not a re-derived regex, not a read-and-guess.
  Gate re-runs and pytest/ruff invocations were all run this turn via Bash
  and their output is quoted/counted above, not recalled from memory.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by
  design of this unit — the Phase-1 router/LLM layer is deliberately
  UNSCORED here (no LLM calls made anywhere in this session, confirmed by
  each script's own self-report plus the absence of any LLM-client import in
  the commands I ran).
- **Denominator**: all 3 target lists (REMINDER_PATTERNS,
  REMINDER_QUERY_PATTERNS, TODO_QUERY_PATTERNS) — 15 of 15 previously-flagged
  unexercised literals now have a corpus row and score 0 "needs a corpus
  row" lines each (3/3 lists confirmed by direct grep count, not sampled).
  Test denominator: 41/41 in the two target test files pass; 63 passed +
  1 xfailed (pre-existing, unrelated) in the architecture-enforcement suite,
  full file run not a subset.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md`
  §"Phase 3 — deletion gate" (the gate's contract + precedence rules);
  Exhibit-A commit `5ec59b8098` (HAND_ROWS deposit format/citation
  convention); existing corpus rows for `create_reminder`/
  `list_reminders_query`/todo-query actions (category convention, TEMPORAL
  vs QUERY).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off
  discipline sections (this is a bounded prog dispatch inside an existing
  worktree — no mailbox write, no sign-off merge, per dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were
  sufficient.

## Discovered work

None filed. The one incidental finding (`\bwhat.*next.*do\b` unreachable
under the word order "what do I do next", reachable under "what ... next ...
do" order) is not a bug — it's the literal's designed left-to-right
semantics — and is noted inline in the deposited row's `notes` field rather
than filed as a separate issue, per the task's own framing ("that is itself
a finding... report it, don't delete it" — reported here and in-file, no
NO-GO list required a deletion decision this unit).
