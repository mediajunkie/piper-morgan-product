# 2026-09-30 2155 — prog (Coding Agent) — #1595 Phase 3 TEMPORAL_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `TEMPORAL_PATTERNS` only (56 literals, 54
unexercised at gate time) — same unit shape as the 2026-09-30 CALENDAR_QUERY_PATTERNS deposits
lane this unit mirrors. NO LLM calls made. No pattern deleted. No flag changed. Did not touch git
index (dispatcher instruction — no staging/commit performed). Did not touch
`services/intent_service/reminder_clear.py`, `services/intent_service/workflow_entries.py`, or
`services/intent/intent_service.py` — a concurrent lane in this shared worktree owns those
(confirmed untouched-by-me at session end via the fact I never opened them for edit).

## Read first (per dispatch prompt)

- `dev/2026/09/30/2026-09-30-2150-prog-code-log-1595-phase3-deposits-calendar.md` — the
  CALENDAR_QUERY_PATTERNS deposits lane this unit mirrors (method: call the REAL production
  matcher directly; row-shape convention; `notes` field for reworded rows; the
  claiming-literal-vs-action-determining-match independence finding; "report, don't deposit" for
  structurally unreachable literals).
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate",
  including the 2026-09-27 measurement note flagging TEMPORAL_PATTERNS claims only 2/10 TEMPORAL
  corpus rows directly.
- `services/intent_service/pre_classifier.py` — `TEMPORAL_PATTERNS` (56 literals, lines
  203–268), its single-destination branch in `pre_classify_with_pattern_list` (~line 1835,
  guarded by `not _is_destructive_ask`, checked AFTER CALENDAR_QUERY_PATTERNS,
  CONTEXTUAL_QUERY_PATTERNS, COMPLETION_HISTORY_PATTERNS, INTEGRATION_CONNECT_PATTERNS, and
  several more — full if-chain read, not assumed), and `action_registry.py` confirming
  `("TEMPORAL", "get_current_time")` is `ActionDisposition.CANONICAL` (floor-routed, not
  WORKFLOW — same disposition class as PRIORITY_PATTERNS/`get_top_priority`, unlike
  CALENDAR_QUERY_PATTERNS's three WORKFLOW destinations).

## What I did

1. Ran the gate exactly as specified. Confirmed 56 literals, 2/235 rows claimed, 54 unexercised
   (matches dispatch's stated "gate says 2 rows claimed").

2. Read the full `TEMPORAL_PATTERNS` literal list and the full precedence chain in
   `pre_classify_with_pattern_list` (every list checked before TEMPORAL_PATTERNS: GREETING/
   FAREWELL/THANKS, DISCOVERY, PROVENANCE, TRUST, INSIGHT_PULL, MEMORY, GET/SET_DEFAULT_REPO,
   STAKEHOLDER_UPDATE, DOCUMENT_QUERY, REPO_MANAGEMENT, PORTFOLIO, FEATURE_INFO, IDENTITY,
   CONTEXTUAL_QUERY, CALENDAR_QUERY (destructive-guarded), MILESTONE_STATUS_INLINE,
   LOCAL_GIT_STATUS, GITHUB_QUERY, REMINDER_QUERY, REMINDER, TODO_COMPLETE, TODO_QUERY,
   COMPLETION_HISTORY, INTEGRATION_CONNECT) — this precedence reading is what let me predict
   (and then empirically confirm) which TEMPORAL literals are shadowed by an entirely different,
   earlier-checked list (CALENDAR_QUERY_PATTERNS), not just an earlier sibling in TEMPORAL's own
   list — a shadow shape the PRIORITY and CALENDAR_QUERY lanes didn't need, since neither had a
   same-category sibling list checked ahead of it with overlapping literal text.

3. Derived one natural PM-style phrase per unexercised literal, verified empirically against the
   REAL production matcher in a Python script (not inferred from regex text):
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list name ==
     `"TEMPORAL_PATTERNS"` and `intent.action == "get_current_time"` (TEMPORAL_PATTERNS has no
     action-determining sub-branch the way CALENDAR_QUERY_PATTERNS does — one destination only,
     confirmed by reading the branch body at line 1835-1841).
   - `PreClassifier._first_pattern_match(cleaned, PreClassifier.TEMPORAL_PATTERNS)` → asserted
     `.re.pattern` equals the specific cited literal.

   First pass (54 literals): 46 resolved cleanly or after one reword. **One bookkeeping mistake
   caught and corrected during this pass**: I initially treated
   `r"\bwhen is my.{0,10}meeting\b"` as already-claimed (assuming the existing corpus row "when
   is my next meeting?" matched it) and skipped it. Re-checking with `_first_pattern_match`
   showed that row actually claims via the earlier sibling `r"\bnext meeting\b"` — the longer
   literal was genuinely unexercised and is in the gate's own 54-line unexercised dump. Added a
   row for it (`"when is my team meeting"`, avoiding the word "next" so it doesn't fall to the
   earlier sibling). This is exactly the kind of "wording resembles an existing row" trap the
   dispatch's "mind the neighbours" instruction was warning about, just inside TEMPORAL's own
   list rather than against CALENDAR_QUERY_PATTERNS.

   Six literals, after 2 independent phrasing attempts each, were confirmed STRUCTURALLY
   unreachable — no deposit:
   - `r"\bwhat'?s on my calendar\b"` and `r"\btomorrow'?s schedule\b"` — CALENDAR_QUERY_PATTERNS
     has the IDENTICAL literal and is checked before TEMPORAL_PATTERNS entirely; any match is
     claimed there first.
   - `r"\bwhat'?s.{0,10}tomorrow\b"` — CALENDAR_QUERY_PATTERNS has the broader, unbounded
     `r"\bwhat'?s.*tomorrow\b"`, checked first; every string the bounded TEMPORAL literal can
     match (gap ≤ 10 chars) also satisfies the unbounded CALENDAR one.
   - `r"\bmeetings this week\b"` — CALENDAR_QUERY_PATTERNS has the broader
     `r"\bmeetings.*this week\b"`, checked first; same shape.
   - `r"\bwhat'?s on my schedule\b"` — always contains "my schedule", claimed first by the
     earlier TEMPORAL_PATTERNS sibling `r"\bmy schedule\b"`.
   - `r"\bhow long.*been working\b"` — "been working" always contains "working", so any match
     also satisfies the earlier sibling `r"\bhow long.*working\b"`.

   These first four are a genuinely new shadow shape vs. the PRIORITY/CALENDAR lanes: a
   TEMPORAL_PATTERNS literal permanently shadowed by a DIFFERENT, earlier-checked list, not an
   earlier sibling in its own list. Noted in the builder's block comment and in the progress log
   for the Lead.

4. Deposited a `# — TEMPORAL_PATTERNS` delimited block (extending the existing
   `# phase3-conversion` HAND_ROWS section, after the CALENDAR_QUERY_PATTERNS block) in
   `scripts/build_inversion_corpus_phase0.py`: 48 rows, `category: TEMPORAL` (matching the two
   pre-existing TEMPORAL corpus rows' category), `expected: action:get_current_time` for every
   row (single destination — no per-row action variation the way CALENDAR_QUERY_PATTERNS
   needed), each `source` citing `phase3-conversion/TEMPORAL_PATTERNS literal r"<the literal>"`.

5. **Verification pass on the deposited file itself** (not just my scratch script): wrote a
   second script that re-extracts all 48 dict entries directly from
   `scripts/build_inversion_corpus_phase0.py` (regex + `ast.literal_eval`, not hand-copied) and
   re-ran both checks (`pre_classify_with_pattern_list` list/action, `_first_pattern_match`
   literal identity) against the actual file content. 0 mismatches / 48, 48 unique literals cited
   (no duplicates). This catches transcription errors between my scratch verification and what I
   actually typed into the builder — the CALENDAR lane's log didn't describe this second pass
   explicitly, so I added it as an extra check given this unit's larger row count.

6. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 235 → 283
   rows (+48), confirmed by the script's own stdout row count both before and after `ruff
   format` reformatted the builder file (regenerated again post-format to rule out any
   formatting-induced string change; same 283).

7. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 235 → 283 (claimed 184 → 232, unclaimed
   unchanged at 51 — confirmed by direct `gate.build_census()` + `inversion_phase0_baseline.
   load_corpus()` call: `corpus_size 283 claimed 232 unclaimed 51 sum 283`). Searched for other
   pinned `\b235\b` constants: `git grep -n "\b235\b" -- tests scripts` — only the one
   just-fixed hit (now reading "235 + 48" as historical context) plus an unrelated
   `mypy-ceiling`-comment number and `tests/fixtures/large_text.txt`'s line-235 marker
   (irrelevant).

8. Re-ran the gate for TEMPORAL_PATTERNS: 50/56 literals now claimed (2 pre-existing + 48 new).
   **Verdict: NO-GO** — a materially different outcome from the CALENDAR_QUERY_PATTERNS lane's
   GO, and the dispatch prompt did not predict either way for TEMPORAL. Every one of the 48 new
   rows reads `[FAIL] ... UNSCORED; not-live (checked op/canonical/group/category, none in
   [...])`. Traced the cause in `services/intent_service/inversion_live.py`'s
   `expected_action_is_live` / `resolve_live_match`: `get_action_workflows().get("get_current_time")`
   returns `None` (no WORKFLOW entry exists for it — confirmed `action_registry.py` disposition
   is CANONICAL, not WORKFLOW), so `flip_group` is `None`; `_category_by_operation(grammar).get(
   "get_current_time")` also returns `None` because the INVERSION router's own grammar never
   offers `get_current_time` as an operation to route to (it is a floor/pre-classifier-only
   action, never proposed by the router). With `operation`/`canonical` also not literally one of
   the `--live` tokens, none of the gate's three live-naming surfaces (operation/canonical,
   flip_group, category) can match — so `get_current_time` is structurally ineligible for
   "live" under this mechanism regardless of corpus coverage. This is the SAME disposition shape
   PRIORITY_PATTERNS hit (both are `ActionDisposition.CANONICAL`/floor-routed with no WORKFLOW
   flip_group), not CALENDAR_QUERY_PATTERNS's shape (three WORKFLOW actions sharing flip_group
   `read_temporal`). NO-GO suppresses the gate's "needs a corpus row before deletion" section
   (confirmed: 0 such lines print after this deposit), consistent with the PRIORITY lane's
   established finding that NO-GO suppression is a FLOOR-disposition side effect, not evidence
   the 6 unreachable literals above got rows.

9. Ran both dry-run validations — no LLM calls (each script self-reports this):
   - `inversion_phase1_shadow_score.py --dry-run` → "dry-run complete: corpus + grammar +
     selections validated, no LLM calls." Exit 0. Same pre-existing TEMPORAL shared-subset
     cross-validation note the CALENDAR lane flagged (`what's on my calendar today?`
     REGRESSION, shared=4/router=3/4/baseline=4/4) — unaffected by this unit: the 48 new rows
     are UNSCORED and outside that cross-check's "shared" (pre-existing, frozen-report) subset.
   - `inversion_phase2_gate.py --dry` → "dry run complete... No LLM calls made." Exit 0.

10. `ruff format` + `ruff check --fix` on both touched `.py` files → 1 file reformatted
    (`build_inversion_corpus_phase0.py`, whitespace/line-wrap only), 1 unchanged; re-ran
    `ruff format --check` + `ruff check` after → both clean. Regenerated the corpus again
    post-reformat to confirm the reformatting didn't change any string content (same 283 rows).

11. Tests (all run this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` — 19 passed.
    - `tests/unit/services/intent_service/test_preclaim_shadow.py` — 29 passed.
    - `tests/test_architecture_enforcement.py` — 63 passed, 1 xfailed, clean (no concurrent
      failures this run).
    - Extraction ceiling re-confirmed 548 via direct `pattern_literal_counts.
      total_literal_count()` call AND the `ExtractionPatternRatchet`-family tests in isolation
      (3 passed, 61 deselected).

12. Added a progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Rows added — TEMPORAL_PATTERNS (category TEMPORAL, all expected: action:get_current_time)

All 48 verified directly via `intent.action` and `_first_pattern_match` against the ACTUAL
builder-file content (not just scratch phrasing), per the extra verification pass in step 5.

| phrase | literal exercised | reworded? |
|---|---|---|
| "what's the time" | `\bwhat'?s the time\b` | no |
| "current time please" | `\bcurrent time\b` | no |
| "give me the time now" | `\btime now\b` | no |
| "tell me the time" | `\btell me the time\b` | no |
| "what day is it" | `\bwhat day is it\b` | no |
| "what's the date" | `\bwhat'?s the date\b` | no |
| "current date please" | `\bcurrent date\b` | no |
| "today's date please" | `\btoday'?s date\b` | no |
| "what's today" | `\bwhat'?s today\b` | no |
| "give me the date and time" | `\bdate and time\b` | no |
| "what day of the week is it" | `\bday of the week\b` | no |
| "tell me the date" | `\btell me the date\b` | no |
| "what date is it" | `\bwhat date is it\b` | no |
| "remind me today's day" | `\btoday'?s day\b` | yes (avoid `\bwhat'?s today\b`) |
| "pull up my calendar" | `\bmy calendar\b` | no |
| "show the team calendar" | `\bshow.{0,10}calendar\b` | yes (avoid `\bmy calendar\b`) |
| "pull up my schedule" | `\bmy schedule\b` | no |
| "show the team schedule" | `\bshow.{0,10}schedule\b` | yes (avoid `\bmy schedule\b`) |
| "calendar check for today" | `\bcalendar.*today\b` | no |
| "schedule check for today" | `\bschedule.*today\b` | no |
| "walk me through my appointments" | `\bmy appointments\b` | no |
| "show all appointments" | `\bshow.{0,10}appointments\b` | yes (gap-fit) |
| "walk me through my meetings" | `\bmy meetings\b` | no |
| "what are the upcoming meetings" | `\bupcoming meetings\b` | no |
| "when is my team meeting" | `\bwhen is my.{0,10}meeting\b` | yes (avoid "next meeting"; see bookkeeping note above) |
| "when am i in a meeting" | `\bwhen am i.{0,10}meeting\b` | no |
| "meeting check for today" | `\bmeeting.*today\b` | no |
| "meeting check for tomorrow" | `\bmeeting.*tomorrow\b` | no |
| "walk me through my events" | `\bmy events\b` | no |
| "show all events" | `\bshow.{0,10}events\b` | yes (gap-fit, avoid "upcoming") |
| "what are the upcoming events" | `\bupcoming events\b` | no |
| "events check for today" | `\bevents.*today\b` | no |
| "events check for tomorrow" | `\bevents.*tomorrow\b` | no |
| "when's the next event" | `\bnext event\b` | no |
| "what did I work on today" | `\bwork on today\b` | no |
| "what happened in the meeting yesterday" | `\bwhat.*yesterday\b` | no |
| "did I finish the report yesterday" | `\bdid.*yesterday\b` | yes (avoid `\bwhat.*yesterday\b`) |
| "a lot happened yesterday" | `\bhappened yesterday\b` | yes (avoid `\bwhat.*yesterday\b`) |
| "when was the last time I worked on this" | `\blast time.*worked\b` | no |
| "how long have I been working on this" | `\bhow long.*working\b` | no |
| "this week's priorities, remind me" | `\bthis week'?s\b` | no |
| "next week's priorities, remind me" | `\bnext week'?s\b` | no |
| "this month's numbers, remind me" | `\bthis month'?s\b` | no |
| "when am i free" | `\bwhen am i free\b` | no |
| "when's my next free slot" | `\bwhen'?s my next.{0,10}free\b` | no |
| "what's my available time" | `\bavailable time\b` | no |
| "when do I have free time" | `\bfree time\b` | no |
| "what are my open slots" | `\bopen slots\b` | no |

48 rows total. All UNSCORED (as expected — the budgeted LLM shadow-score run is out of scope for
this unit).

## Unreachable literals (6) — no deposit, reported as findings

Confirmed with 2 independent phrasing attempts each. Four are a NEW shadow shape vs. the
PRIORITY/CALENDAR lanes — shadowed by a DIFFERENT, earlier-checked list
(`CALENDAR_QUERY_PATTERNS`), not an earlier sibling in TEMPORAL_PATTERNS's own list:

1. `r"\bwhat'?s on my calendar\b"` — `CALENDAR_QUERY_PATTERNS` has the IDENTICAL literal and is
   checked before `TEMPORAL_PATTERNS` entirely (confirmed by reading the if-chain, lines ~1499
   vs. ~1835); any match is claimed there first.
2. `r"\btomorrow'?s schedule\b"` — same: `CALENDAR_QUERY_PATTERNS` has the IDENTICAL literal,
   checked first.
3. `r"\bwhat'?s.{0,10}tomorrow\b"` — `CALENDAR_QUERY_PATTERNS` has the broader, unbounded
   `r"\bwhat'?s.*tomorrow\b"`, checked first; every string the bounded TEMPORAL literal can
   match also satisfies the unbounded CALENDAR one.
4. `r"\bmeetings this week\b"` — `CALENDAR_QUERY_PATTERNS` has the broader
   `r"\bmeetings.*this week\b"`, checked first; any string satisfying the TEMPORAL literal
   trivially satisfies the CALENDAR one.

Two are the familiar within-list shadow (earlier sibling in `TEMPORAL_PATTERNS` itself always
wins first):

5. `r"\bwhat'?s on my schedule\b"` — always contains "my schedule", claimed first by
   `r"\bmy schedule\b"` (earlier in the list).
6. `r"\bhow long.*been working\b"` — "been working" always contains "working", so any match
   also satisfies `r"\bhow long.*working\b"` (earlier in the list), which wins first.

Not filed as separate GitHub issues — same convention the PRIORITY/CALENDAR lanes used; these
are a property of existing regex ordering/precedence, not new bugs.

## Verdict: NO-GO (differs from CALENDAR_QUERY_PATTERNS's GO) — flagged for the Lead

Unlike the CALENDAR lane, the dispatch prompt gave no prediction for TEMPORAL's verdict. After
this deposit, the gate reads **NO-GO**, and will keep reading NO-GO regardless of further corpus
coverage, because `get_current_time` is `ActionDisposition.CANONICAL` (floor-routed) with no
`WorkflowEntry` (so no `flip_group`) and no entry in the INVERSION router's own operation
grammar (so no `category` match either) — none of the gate's three live-naming surfaces
(operation/canonical name, flip_group, category) can mark it live under any `--live` token set.
This is the same disposition shape `PRIORITY_PATTERNS` hit, not `CALENDAR_QUERY_PATTERNS`'s (its
three actions are all `WORKFLOW`-dispatched, sharing flip_group `read_temporal`). Resolving this
NO-GO is a disposition question (does `get_current_time` get a WORKFLOW/flip_group registration,
or does it wait on the Lead's budgeted LLM shadow-score run to score these 48 UNSCORED rows
AGREE/MATCH) — not something a corpus deposit alone can fix, and explicitly out of this unit's
scope (no flag/env changes, no LLM calls, per dispatch).

## Gate output — before

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 235 rows total = 184 claimed + 51 unclaimed

## TEMPORAL_PATTERNS
literals: 56  |  rows claimed: 2/235
verdict: GO (deletable) — deleting removes 56 literals: ceiling 548 -> 492

rows claimed:
  [OK] "when is my next meeting?" -> claim=get_current_time expected=action:meeting_time router=meeting_time@1.0 verdict=MATCH :: MATCH
  [OK] "what time is it?" -> claim=get_current_time expected=category:TEMPORAL router=get_current_time@1.0 verdict=MATCH :: MATCH

pattern->corpus conversion needed (54 literal(s) unexercised):
  [... 54 lines, one per unexercised literal ...]
```

Note: the PRE-deposit verdict read GO (only the 2 already-MATCHed rows existed; the gate's
per-list verdict with 0 UNSCORED rows and no live-requirement failures reads GO by default). The
verdict flips to NO-GO only once the 48 new UNSCORED/not-live rows are added — this is the gate
correctly re-evaluating with the fuller row set, not a regression caused by this deposit; the
list was never actually deletable (52/56 literals had zero coverage either way).

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 283 rows total = 232 claimed + 51 unclaimed

## TEMPORAL_PATTERNS
literals: 56  |  rows claimed: 50/283
verdict: NO-GO

rows claimed:
  [OK] "when is my next meeting?" -> claim=get_current_time expected=action:meeting_time router=meeting_time@1.0 verdict=MATCH :: MATCH
  [OK] "what time is it?" -> claim=get_current_time expected=category:TEMPORAL router=get_current_time@1.0 verdict=MATCH :: MATCH
  [FAIL] "what's the time" -> claim=get_current_time expected=action:get_current_time router=None@None verdict=UNSCORED :: UNSCORED; not-live (checked op/canonical/group/category, none in [...])
  [... 47 more [FAIL] lines, one per new deposit row, all "UNSCORED; not-live" ...]

(no "pattern->corpus conversion needed" section — NO-GO suppresses it, per the PRIORITY lane's
established finding)
```

## New corpus total

235 → **283** rows (+48). Per-category denominators after rebuild: **QUERY 85**, **TEMPORAL 69**
(was 21), PRIORITY 41, GUIDANCE 26, EXECUTION 18, PORTFOLIO 16, STATUS 8, CONVERSATION 5,
SYNTHESIS 4, IDENTITY 3, MEMORY 3, DISCOVERY 2, PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 283 rows (59 REVIEW), exit 0
  (confirmed twice: once pre-ruff-format, once post, identical 283).
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 50/56 claimed, **verdict NO-GO**, 0 "needs a corpus row" lines (suppressed by NO-GO,
  not evidence of 0 unreachable literals — 6 exist, see above).
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported.
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` → **19
  passed**, exit 0.
- `venv/bin/python -m pytest tests/unit/services/intent_service/test_preclaim_shadow.py -q` →
  **29 passed**, exit 0.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63 passed, 1
  xfailed**, exit 0, clean.
- `venv/bin/python -c "...pattern_literal_counts.total_literal_count()"` → **548**, unchanged.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q -k "ExtractionPattern or
  CEILINGS or pattern_literal"` → **3 passed, 61 deselected**, exit 0.
- `venv/bin/ruff format` + `ruff check --fix` → 1 file reformatted (whitespace only), both
  clean on re-check.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (48-row `# — TEMPORAL_PATTERNS` HAND_ROWS block
  added, extending the existing `# phase3-conversion` section)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, 235 → 283 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 235→283,
  with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log entry added)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/reminder_clear.py`, `services/intent_service/workflow_entries.py`,
`services/intent/intent_service.py` (the dispatcher's named concurrent-lane files — never opened
for edit), `services/intent_service/inversion_live.py` (read only, to understand the NO-GO
cause), any flag/env var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion
performed).

## Verified how

- **Method**: for each of the 54 unexercised literals, called the REAL production functions
  directly in a Python script against this worktree's code —
  `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion AND `intent.action`
  read directly) and `PreClassifier._first_pattern_match(cleaned, PreClassifier.TEMPORAL_
  PATTERNS)` (literal-identity assertion). For the 6 unreachable literals, tested 2 independent
  phrasings each before concluding structural unreachability. **Additionally**, re-extracted all
  48 deposited rows directly from the builder file's actual text (regex + `ast.literal_eval`,
  not hand-copied from my scratch script) and re-ran both checks against that extracted content
  — 0 mismatches, 48 unique literals, no duplicates — so the verification covers what actually
  landed in the file, not just what I intended to type. Gate re-runs, pytest, and ruff
  invocations were all run this turn via Bash and their output is quoted/counted above, not
  recalled from memory. The NO-GO cause was traced by reading
  `services/intent_service/inversion_live.py`'s `expected_action_is_live`/`resolve_live_match`
  and confirming via `action_registry.py` that `("TEMPORAL", "get_current_time")` is
  `ActionDisposition.CANONICAL`, not `WORKFLOW`.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit
  — the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in
  this session, confirmed by each script's own self-report and the absence of any LLM-client
  invocation in the commands run). The NO-GO-cause trace is a code-reading/static layer
  (action_registry.py disposition, workflow_dispatcher's registered entries, the router's
  grammar construction), not a live/runtime measurement.
- **Denominator**: 1 target list (TEMPORAL_PATTERNS) — 48 of 54 previously-flagged unexercised
  literals now have a corpus row; 6 confirmed structurally unreachable and explicitly reported
  (visible only in this log and the progress-log entry, since NO-GO suppresses the gate's own
  "needs a corpus row" section — not silently dropped, but not gate-visible either, flagged
  explicitly for the Lead). Test denominator: 19/19 in the target Phase-3 test file pass, 29/29
  in the pre-claim shadow test file pass, 63/63 (plus 1 pre-existing xfail) in the full
  architecture-enforcement suite (full file run, not a subset), 3/3 in the extraction-ceiling-
  specific test subset, 48/48 deposited rows independently re-verified against the actual file
  content (step 5 above). Ceiling denominator: 548/548 unchanged, confirmed by direct call, not
  inferred.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 —
  deletion gate" (mechanism + the 2026-09-27 TEMPORAL 2/10-claim measurement note); `dev/2026/
  09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure + progress log); prior prog
  session log `2026-09-30-2150-prog-code-log-1595-phase3-deposits-calendar.md` (verification
  methodology, row-block convention, `notes` field precedent, "mind the neighbours" framing);
  `action_registry.py` (`ActionDisposition` lookup, confirming CANONICAL for `get_current_time`);
  `services/intent_service/inversion_live.py` (read only, to trace the NO-GO cause —
  `resolve_live_match`/`expected_action_is_live`/`_category_by_operation`).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient, though
  this unit needed to read further into `inversion_live.py` than either prior lane did, to
  explain the NO-GO (not predicted by the dispatch prompt, unlike CALENDAR's "0 CALENDAR 'needs
  a corpus row' lines" expectation, which was given in advance).

## Discovered work

None filed as separate issues. Findings reported inline (matching the PRIORITY/CALENDAR
convention):
1. 6 structurally unreachable TEMPORAL_PATTERNS literals (listed above), 4 of them a NEW
   cross-list shadow shape (TEMPORAL literal shadowed by a different, earlier-checked list,
   CALENDAR_QUERY_PATTERNS) not seen in the PRIORITY/CALENDAR lanes.
2. TEMPORAL_PATTERNS verdict is NO-GO (not GO) and will STAY NO-GO regardless of further corpus
   coverage, because `get_current_time`'s CANONICAL/floor disposition gives the gate's live-match
   mechanism no surface (operation, flip_group, or category) to match against. This is a
   disposition question for the Lead — resolving it needs either a WORKFLOW/flip_group
   registration for `get_current_time` or the budgeted shadow-score run to score these rows
   AGREE/MATCH (out of this unit's scope either way).
3. One bookkeeping mistake self-caught mid-session: initially skipped
   `r"\bwhen is my.{0,10}meeting\b"` assuming the existing "when is my next meeting?" row claimed
   it; `_first_pattern_match` showed that row actually claims via `r"\bnext meeting\b"`, so the
   longer literal needed its own row (added: "when is my team meeting"). Recorded here and in
   the row's `notes` field so a future audit doesn't need to re-derive this.
