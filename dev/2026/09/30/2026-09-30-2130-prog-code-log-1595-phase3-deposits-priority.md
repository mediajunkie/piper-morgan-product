# 2026-09-30 2130 — prog (Coding Agent) — #1595 Phase 3 PRIORITY_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `PRIORITY_PATTERNS` only (47 literals, 43
unexercised at gate time) — the same unit shape as the 2026-09-27 GUIDANCE_PATTERNS deposits
lane. NO LLM calls made. No pattern deleted. No flag changed. Did not touch git index (dispatcher
instruction — no staging/commit performed).

## Read first (per dispatch prompt)

- `dev/2026/09/27/2026-09-27-1235-prog-code-log-1595-phase3-deposits-guidance.md` — the
  GUIDANCE_PATTERNS deposits lane this unit mirrors (method, row shape, verification
  convention). Its diff: commit `efa75b639e` (`git show efa75b639e -- scripts/
  build_inversion_corpus_phase0.py`).
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate",
  incl. "Any change to the router's prompt or catalog is scored on BOTH tables" and the
  "First deletion" / "Second deletion" subsections — the second deletion's note that
  `PRIORITY_PATTERNS` already carries an identical literal (`\bwhat should i do next\b`) since
  2026-03-22, reclaimed from `TODO_QUERY_PATTERNS` on its deletion, was directly relevant: one
  of the 4 pre-existing claimed PRIORITY rows is that reclaim.
- `services/intent_service/pre_classifier.py` — `PRIORITY_PATTERNS` (47 literals), its
  single-intent branch in `pre_classify_with_pattern_list` (line ~1874, checked AFTER
  GREETING/FAREWELL/THANKS/DISCOVERY/PROVENANCE/TRUST/INSIGHT_PULL/MEMORY/…/GUIDANCE/ANALYSIS/
  STATUS — confirmed by reading the full if-chain, not assumed), and the multi-intent pattern
  table entry `(PRIORITY_PATTERNS, IntentCategory.PRIORITY, "get_top_priority")` — single
  destination, no second op to disambiguate (unlike TODO_QUERY_PATTERNS' two-destination case
  the dispatch prompt flagged as a possibility).
- `services/intent_service/action_registry.py` — confirmed `("PRIORITY", "get_top_priority")`
  is `ActionDisposition.FLOOR` (routes to the conversational floor, same disposition as
  `("STATUS", "get_project_status")`), not an alias of another canonical action, and not present
  in `workflow_entries.py` (FLOOR actions don't need a WORKFLOW rail entry — expected, matches
  the registry's own docstring for FLOOR).

## What I did

1. Ran the gate exactly as specified: `venv/bin/python scripts/inversion_phase3_deletion_gate.py
   --list PRIORITY_PATTERNS --live read_status,read_referent,read_synthesis,create_todo,
   create_reminder,read_strategic,read_temporal 2>/dev/null | grep -vE "^[0-9]{4}-"` — confirmed
   47 literals, 4/151 rows claimed, 43 unexercised (matches the dispatch's stated numbers).

2. Derived one natural PM-style phrasing per unexercised literal and verified each empirically
   in a Python script (not a REPL transcript, but the same two assertions) against the real
   production matcher:
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list name ==
     `"PRIORITY_PATTERNS"`.
   - `PreClassifier._first_pattern_match(cleaned_phrase, PreClassifier.PRIORITY_PATTERNS)` →
     asserted `.re.pattern` equals the specific cited literal.

   First pass: 31/43 phrases verified cleanly. 12 failed — all 12 were claimed by an EARLIER
   sibling literal in the same list (first-match-wins). Reworded 7 of the 12 and re-verified
   clean (documented per-row in the deposit's `notes` field, same convention as the GUIDANCE
   lane's one reworded row). The remaining 5 were tested with 2 different phrasings each and
   found to be STRUCTURALLY unreachable — not a phrasing problem but a logical subset relation
   between the later literal and an earlier one in the same list (detail in "Unreachable
   literals" below). No deposit for these 5.

3. Deposited a `# — PRIORITY_PATTERNS` delimited block (extending the existing
   `# phase3-conversion` HAND_ROWS section, after the GUIDANCE block) in
   `scripts/build_inversion_corpus_phase0.py`: 38 rows, `category: PRIORITY`,
   `expected: action:get_top_priority` (single destination for the whole list; this exact
   expectation already scored MATCH once, in the TODO_QUERY_PATTERNS re-expected "what should I
   do next" row), each `source` citing `phase3-conversion/PRIORITY_PATTERNS literal r"<the
   literal>"`.

4. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 151 →
   189 rows (+38). `git diff --stat` on the yaml: 159 insertions, 0 deletions (purely
   additive).

5. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 151 → 189 (claimed 100 → 138, unclaimed
   unchanged at 51 — confirmed by direct `gate.build_census()` call, not inferred), docstring
   updated to name this deposit. Searched for other pinned corpus-size constants:
   `git grep -n "\b151\b" -- tests scripts` — no other hits besides the one just fixed (one
   unrelated hit in `scripts/ratchet_ceilings.json`'s giant mypy-history comment blob,
   irrelevant).

6. Re-ran the gate for PRIORITY_PATTERNS: 42/47 literals now claimed (4 pre-existing + 38 new),
   **0** "needs a corpus row before deletion" lines (grep-count confirmed, was 43). The 38 new
   rows correctly show `verdict=UNSCORED` — scoring is the Lead's budgeted (LLM-calling) run,
   not part of this unit.

7. Ran both dry-run validations — no LLM calls (each script self-reports this):
   - `inversion_phase1_shadow_score.py --dry-run` → "dry-run complete: corpus + grammar +
     selections validated, no LLM calls." Exit 0. Same pre-existing TEMPORAL shared-subset
     cross-validation note as prior sessions (`what's on my calendar today?` REGRESSION) —
     unrelated to and unaffected by PRIORITY deposits (no TEMPORAL rows touched).
   - `inversion_phase2_gate.py --dry` → "dry run complete... No LLM calls made." Exit 0.
     Reports `phase0 corpus: 189 rows (untouched)`.

8. `ruff format` + `ruff check --fix` on both touched `.py` files — clean on the first pass
   (no reformatting needed); `ruff format --check` + `ruff check` both clean on re-run.

9. Tests (all run this turn, output quoted below):
   - `tests/unit/test_inversion_phase3_deletion_1595.py` — 19 passed.
   - `tests/unit/services/intent_service/test_preclaim_shadow.py` — 29 passed.
   - `tests/test_architecture_enforcement.py` — 1 pre-existing, UNRELATED failure found
     (`TestInversionShadowNoExecutionBoundary::
     test_only_the_shadow_observer_may_import_the_router`) — see "Unrelated concurrent finding"
     below. With that one test deselected: 62 passed, 1 xfailed (consistent with the prior
     baseline of 63 passed/1 xfailed, minus the one now-failing test). Extraction ceiling
     re-confirmed 548 via direct `pattern_literal_counts.total_literal_count()` call AND via
     the `ExtractionPatternRatchet`-family tests run in isolation (3 passed, 0 failed).

10. Added a progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Rows added — PRIORITY_PATTERNS (category PRIORITY, expected `action:get_top_priority`)

| phrase | literal exercised | reworded? |
|---|---|---|
| "what's my top priority" | `\bwhat'?s my top priority\b` | no |
| "this is top priority for the team" | `\btop priority\b` | no |
| "this is the highest priority item" | `\bhighest priority\b` | no |
| "mark this as priority one" | `\bpriority one\b` | no |
| "show priorities for this sprint" | `\bshow.*priorities\b` | yes (avoid `\bmy priorities\b`) |
| "list priorities for the team" | `\blist.*priorities\b` | yes (avoid `\bmy priorities\b`) |
| "what are my current priorities" | `\bcurrent priorities\b` | no |
| "what are the key priorities this quarter" | `\bkey priorities\b` | no |
| "what's most important right now" | `\bmost important\b` | no |
| "what matters most this week" | `\bwhat matters most\b` | no |
| "what are the key tasks for this sprint" | `\bkey tasks\b` | no |
| "what are the key items on my plate" | `\bkey items\b` | no |
| "should i focus on the bug first" | `\bshould i focus\b` | no |
| "what could I focus on" | `\bwhat.*focus on\b` | yes (avoid `\bwhat should i focus on\b`) |
| "where should my focus be today" | `\bwhere.*focus\b` | no |
| "what are my focus areas this sprint" | `\bfocus areas\b` | no |
| "let's focus on today's priorities" | `\bfocus on today\b` | yes (avoid `\bwhat should i focus on\b`) |
| "what's my focus this week" | `\bfocus this week\b` | no |
| "not sure what to focus next" | `\bwhat to focus\b` | yes (avoid `\bwhat.*focus on\b`) |
| "what's urgent right now" | `\bwhat'?s urgent\b` | no |
| "what are my urgent tasks" | `\burgent tasks\b` | no |
| "what are my urgent items" | `\burgent items\b` | no |
| "what's my urgent work today" | `\burgent work\b` | no |
| "what's the most urgent thing" | `\bmost urgent\b` | no |
| "what needs my focus today" | `\bneeds.*focus\b` | no |
| "what requires attention right now" | `\brequires attention\b` | no |
| "what's critical right now" | `\bwhat'?s critical\b` | no |
| "what are my critical tasks" | `\bcritical tasks\b` | no |
| "what are my critical items" | `\bcritical items\b` | no |
| "what's my critical work today" | `\bcritical work\b` | no |
| "what's the most critical thing" | `\bmost critical\b` | no |
| "what should I do first" | `\bwhat should i do first\b` | no |
| "what should I tackle next" | `\bwhat.*(?:do\|work on\|tackle\|handle)\s+next\b` | no |
| "what's next for me" | `\bwhat(?:'s\| is) next\b` | no |
| "what should I review first" | `\bwhat.*first\b` | no |
| "which project should get my focus today" | `\bwhich project.*focus\b` | yes (avoid `\bshould i focus\b`) |
| "which task should get my focus next" | `\bwhich task.*focus\b` | yes (avoid `\bshould i focus\b`) |
| "not sure what to do about this" | `\bwhat to do\b` | no |

38 rows total.

## Unreachable literals (5) — no deposit, reported as findings

All five are structurally shadowed by an earlier literal in the SAME `PRIORITY_PATTERNS` list
(first-match-wins in `_first_pattern_match`): any string satisfying the later pattern
necessarily also satisfies the earlier one, so the earlier literal always wins. Confirmed
empirically with 2 different phrasings each (not just inferred from the regex text):

1. `r"\bwhat are my priorities\b"` — always contains the substring "my priorities", which
   `r"\bmy priorities\b"` (list position 0, far earlier) always claims first.
2. `r"\bmost important task\b"` — always contains "most important", claimed first by
   `r"\bmost important\b"` (earlier in the list).
3. `r"\bmost important work\b"` — same shadow as #2.
4. `r"\bwhat'?s most important\b"` — same shadow as #2 ("what's/what is most important"
   contains "most important").
5. `r"\bwhat.*work on next\b"` — always contains "work on next", which also satisfies the
   `(?:do|work on|tackle|handle)\s+next` alternation inside
   `r"\bwhat.*(?:do|work on|tackle|handle)\s+next\b"` (earlier in the list), so it's always
   claimed there first.

Not filed as separate GitHub issues — same convention the GUIDANCE lane used for its one
reworded-not-unreachable finding; these are a property of the existing regex ordering, not new
bugs, and the existing corpus row "what are my priorities?" (pre-existing, `expected: REVIEW`)
already independently demonstrates #1's shadow (it's claimed by `\bmy priorities\b`, not
`\bwhat are my priorities\b`, consistent with this finding).

## Unrelated concurrent finding — NOT caused by this unit

`tests/test_architecture_enforcement.py::TestInversionShadowNoExecutionBoundary::
test_only_the_shadow_observer_may_import_the_router` failed:
`services/domain/llm_domain_service.py` now references the inversion router outside the shadow
observer. **This file was NOT modified by this unit** — `git status` confirms it is modified in
this shared worktree, but it was clean at the conversation's starting git-status snapshot (the
dispatcher's system-reminder git status at session start did not list it). Two new untracked
test files also appeared during this session
(`tests/e2e/test_1897_two_part_turn_live.py`,
`tests/unit/services/intent_service/test_inversion_router_through_domain_service_1595.py`) —
both clearly belong to a different, concurrent, in-flight lane (issue #1897, a Phase-2-flip
wiring unit) running in this same shared worktree while this unit ran. Per dispatch scope (no
git index touched, PRIORITY_PATTERNS deposits only) I did not inspect, revert, or stage these
files — flagging for the Lead to reconcile with whichever other lane owns that work. Confirmed
this is the ONLY test affected: deselecting it, the suite reads 62 passed/1 xfailed, consistent
with the pre-existing 63 passed/1 xfailed baseline minus the one now-failing (unrelated) test.

## Gate output — before

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 151 rows total = 100 claimed + 51 unclaimed

## PRIORITY_PATTERNS
literals: 47  |  rows claimed: 4/151
verdict: GO (deletable) — deleting removes 47 literals: ceiling 548 -> 501

rows claimed:
  [OK] "what should I focus on today?" -> claim=get_top_priority expected=category:PRIORITY router=get_top_priority@0.9 verdict=MATCH :: MATCH
  [OK] "what are my top priorities?" -> claim=get_top_priority expected=category:PRIORITY router=get_top_priority@0.9 verdict=MATCH :: MATCH
  [OK] "what are my priorities?" -> claim=get_top_priority expected=REVIEW router=get_top_priority@0.9 verdict=REVIEW :: REVIEW-agrees (route=get_top_priority == claim=get_top_priority)
  [OK] "what should I do next" -> claim=get_top_priority expected=action:get_top_priority router=get_top_priority@0.9 verdict=MATCH :: MATCH

pattern->corpus conversion needed (43 literal(s) unexercised):
  [... 43 lines, one per unexercised literal — full list in the dispatch prompt / reproducible
       via the command above ...]
```

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 189 rows total = 138 claimed + 51 unclaimed

## PRIORITY_PATTERNS
literals: 47  |  rows claimed: 42/189
verdict: NO-GO

rows claimed:
  [OK] "what should I focus on today?" -> ... verdict=MATCH
  [OK] "what are my top priorities?" -> ... verdict=MATCH
  [OK] "what are my priorities?" -> ... verdict=REVIEW-agrees
  [OK] "what should I do next" -> ... verdict=MATCH
  [FAIL] "what's my top priority" -> claim=get_top_priority expected=action:get_top_priority router=None@None verdict=UNSCORED :: UNSCORED; not-live
  [... 37 more FAIL/UNSCORED lines, one per new deposit row — all correctly UNSCORED, not-live;
       0 "needs a corpus row before deletion" lines remain (was 43) ...]
```

`[FAIL]`/NO-GO/UNSCORED is EXPECTED and correct for this unit — the deposit rows score
`UNSCORED` until the Lead's budgeted (LLM-calling) shadow-score run judges them; that run is
explicitly out of scope here. What this unit was required to produce, and did: **zero** "needs
a corpus row before deletion" lines for PRIORITY_PATTERNS, confirmed by grep count (0, was 43).

## New corpus total

151 → **189** rows (+38). Per-category denominators after rebuild: **PRIORITY 41** (was 3),
QUERY 39, GUIDANCE 26, TEMPORAL 21, EXECUTION 18, PORTFOLIO 16, STATUS 8, CONVERSATION 5,
SYNTHESIS 4, IDENTITY 3, MEMORY 3, DISCOVERY 2, PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 189 rows (59 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml` → `1 file changed, 159
  insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported; `phase0 corpus: 189 rows (untouched)`.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list PRIORITY_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 0 "needs a corpus row" lines (grep-confirmed, `grep -c "needs a corpus row"` → 0).
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` → **19
  passed**, exit 0.
- `venv/bin/python -m pytest tests/unit/services/intent_service/test_preclaim_shadow.py -q` →
  **29 passed**, exit 0.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **1 failed** (the
  unrelated concurrent finding above), **39 passed** (stopped at first failure, default
  maxfail behavior). Re-run with that one test deselected: **62 passed, 1 xfailed**, exit 0 —
  matches the pre-existing baseline.
- `venv/bin/python -c "import pattern_literal_counts as plc;
  print(plc.total_literal_count())"` → **548**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted).
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q -k
  "ExtractionPattern or CEILINGS or pattern_literal"` → **3 passed**, exit 0 (ceiling ratchet
  specifically, isolated from the unrelated failure).
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes
  needed; `ruff format --check` + `ruff check` both clean on re-run.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +38 rows in a `# —
  PRIORITY_PATTERNS` delimited block, extending the existing `# phase3-conversion` section,
  after the GUIDANCE block)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 151→189 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 151→189,
  with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log entry added)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only), any
flag/env var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion performed by this
unit), `services/domain/llm_domain_service.py` and the two new #1897 test files (concurrent
unrelated work in this shared worktree, left untouched and unstaged per scope).

## Verified how

- **Method**: for each of the 43 unexercised literals, called the REAL production functions
  directly in a Python script against this worktree's code —
  `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion) and
  `PreClassifier._first_pattern_match(cleaned, PreClassifier.PRIORITY_PATTERNS)`
  (literal-identity assertion) — not a re-derived regex, not a read-and-guess. For the 5
  unreachable literals, tested 2 independent phrasings each before concluding structural
  unreachability, and additionally traced the regex-subset relationship by hand (e.g. "most
  important task" always contains "most important" as a substring) to confirm the empirical
  result wasn't an artifact of phrasing choice. Gate re-runs, pytest, and ruff invocations were
  all run this turn via Bash and their output is quoted/counted above, not recalled from
  memory.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this
  unit — the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made
  anywhere in this session, confirmed by each script's own self-report and the absence of any
  LLM-client invocation in the commands run).
- **Denominator**: 1 target list (PRIORITY_PATTERNS) — 38 of 43 previously-flagged unexercised
  literals now have a corpus row; 5 confirmed structurally unreachable and explicitly reported,
  not silently dropped; 0 "needs a corpus row" lines (grep-count confirmed, not sampled). Test
  denominator: 19/19 in the target Phase-3 test file pass, 29/29 in the pre-claim shadow test
  file pass, 62/62 (plus 1 pre-existing xfail) in the full architecture-enforcement suite with
  the one unrelated-and-explained failure deselected (full file run, not a subset, for that
  pass), 3/3 in the extraction-ceiling-specific test subset. Ceiling denominator: 548/548
  unchanged, confirmed by direct AST-walk call, not inferred.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 —
  deletion gate" (the gate's contract + precedence rules, incl. the "scored on BOTH tables"
  rule and the First/Second deletion subsections per dispatch instruction);
  `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress log);
  prior prog session log `2026-09-27-1235-prog-code-log-1595-phase3-deposits-guidance.md`
  (verification methodology, format precedent, row-block convention); `action_registry.py`
  (`ActionDisposition` lookup for `get_top_priority`, confirming FLOOR not CANONICAL but same
  `action:` expected-field format as the CANONICAL GUIDANCE precedent).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline
  sections (this is a bounded prog dispatch inside an existing worktree — no mailbox write, no
  sign-off merge, per dispatcher scope); the shared-worktree concurrent-edit discipline WAS
  relevant in practice (the unrelated `llm_domain_service.py` finding), though no specific
  memory file was consulted for it — handled by direct `git status` comparison against the
  session-start snapshot.
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient.

## Discovered work

None filed as separate issues. Two findings reported inline (not filed separately, matching
the GUIDANCE lane's convention for its one reworded row):
1. 5 structurally unreachable PRIORITY_PATTERNS literals (listed above) — a property of
   existing regex ordering, already partially evidenced by a pre-existing corpus row.
2. An unrelated, in-flight, uncommitted change to `services/domain/llm_domain_service.py` (+
   two new #1897 test files) in this shared worktree causing one `test_architecture_
   enforcement.py` failure — flagged for the Lead to reconcile with whichever lane owns #1897,
   not actioned by this unit.
