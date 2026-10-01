# 2026-09-30 2150 — prog (Coding Agent) — #1595 Phase 3 CALENDAR_QUERY_PATTERNS deposits

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: pattern→corpus conversion deposits for `CALENDAR_QUERY_PATTERNS` only (52 literals, 49
unexercised at gate time) — same unit shape as the 2026-09-30 PRIORITY_PATTERNS deposits lane
this unit mirrors. NO LLM calls made. No pattern deleted. No flag changed. Did not touch git
index (dispatcher instruction — no staging/commit performed). Did not touch
`services/intent_service/reminder_clear.py` or `workflow_entries.py` — a concurrent lane in this
shared worktree owns those (confirmed `reminder_clear.py` modified-but-untouched-by-me at
session end via `git status`).

## Read first (per dispatch prompt)

- `dev/2026/09/30/2026-09-30-2130-prog-code-log-1595-phase3-deposits-priority.md` — the
  PRIORITY_PATTERNS deposits lane this unit mirrors (method: call the REAL production matcher
  directly, not re-derive regex by hand; row-shape convention; `notes` field for reworded rows;
  "report, don't deposit" convention for structurally unreachable literals).
- `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 — deletion gate".
- `services/intent_service/pre_classifier.py` — `CALENDAR_QUERY_PATTERNS` (52 literals, lines
  399–464), its branch in `pre_classify_with_pattern_list` (~line 1499, checked AFTER
  CONTEXTUAL_QUERY and BEFORE MILESTONE_STATUS_INLINE/LOCAL_GIT_STATUS — confirmed by reading
  the full if-chain), and the `_is_destructive_ask` decline-guard (#1756) ahead of the claim
  (none of the 46 deposited phrases match a destructive-ask blocker — checked).
- `services/intent_service/action_registry.py` — confirmed `meeting_time` / `recurring_meetings`
  / `week_calendar` are the only three canonical actions `pre_classify` ever emits for this list
  (all `ActionDisposition.WORKFLOW`); the aliases named in `_CALENDAR_QUERY_COHORT`
  (`how_much_time_in_meetings`, `calendar_analysis`, `review_recurring_meetings`,
  `audit_meetings`) are WORKFLOW-dispatch aliases, not actions the pre-classifier itself ever
  returns — read only, not asserted against in any row.
- `services/intent_service/workflow_entries.py` (READ ONLY, per dispatcher instruction — not
  edited) — `_CALENDAR_QUERY_FLIP_GROUPS` (line 1320): all three destination handlers
  (`_handle_meeting_time_query`, `_handle_recurring_meetings_query`,
  `_handle_week_calendar_query`) map to flip group `"read_temporal"`, which IS in the dispatch's
  `--live` set — so every deposited row is live-routable under the gate's group-live mechanism
  (noted per the dispatch's ask to record this for the Lead).

## What I did

1. Ran the gate exactly as specified. Confirmed 52 literals, 3/235 (at that point 189-row corpus)
   rows claimed, 49 unexercised (matches dispatch's stated numbers).

2. Derived one natural PM-style phrase per unexercised literal and verified each empirically
   against the REAL production matcher in a Python script (not inferred from regex text):
   - `PreClassifier.pre_classify_with_pattern_list(phrase)` → asserted returned list name ==
     `"CALENDAR_QUERY_PATTERNS"`, and `intent.action` read directly (not re-derived by hand —
     see the "agenda.*this week" finding below for why hand-derivation would have been wrong).
   - `PreClassifier._first_pattern_match(cleaned, PreClassifier.CALENDAR_QUERY_PATTERNS)` →
     asserted `.re.pattern` equals the specific cited literal (proves the claim isn't stolen by
     an earlier sibling literal in the same list).

   First pass: 41/49 phrases verified cleanly. 8 failed — all 8 were claimed by an EARLIER
   sibling literal in the same list (first-match-wins). Reworded 5 of the 8 and re-verified
   clean (documented per-row in the deposit's `notes` field). The remaining 3 were tested with 2
   different phrasings each and found STRUCTURALLY unreachable — every phrasing attempt was
   claimed by the same earlier sibling literal both times. No deposit for these 3.

3. **Finding during verification** (recorded in the deposit's header comment and per-row
   `notes`): the literal that CLAIMS a message (via `_first_pattern_match` against
   `CALENDAR_QUERY_PATTERNS`, full-list order) and the literal that DETERMINES the action (via a
   SEPARATE re-match of the message against two hardcoded sub-lists inside the branch body) are
   independent checks. "what's my agenda this week" is claimed by `\bagenda.*this week\b` (that
   literal is NOT in the meeting_time sub-list), but its action comes out `meeting_time` because
   the same string also contains the word-bounded substring "my agenda", which IS in that
   sub-list. Confirmed directly via `intent.action`, not assumed from which CALENDAR_QUERY list
   literal claimed — this is why the dispatch's instruction to "read the CALENDAR branch" for
   actions needed empirical confirmation per phrase rather than hand-tracing the if/elif, which
   would have mis-predicted this and a sibling row ("what's my agenda next week", same
   mechanism).

4. Deposited a `# — CALENDAR_QUERY_PATTERNS` delimited block (extending the existing
   `# phase3-conversion` HAND_ROWS section, after the PRIORITY block) in
   `scripts/build_inversion_corpus_phase0.py`: 46 rows, `category: QUERY` (matching the two
   pre-existing CALENDAR rows' category, not a new bucket), `expected: action:<meeting_time|
   recurring_meetings|week_calendar>` per row (the specific action that exact phrase routes to —
   this list has THREE destinations, unlike PRIORITY's one), each `source` citing
   `phase3-conversion/CALENDAR_QUERY_PATTERNS literal r"<the literal>"`.

5. Regenerated the corpus: `venv/bin/python scripts/build_inversion_corpus_phase0.py` — 189 → 235
   rows (+46). `git diff --stat` on the yaml + builder: 191 + 369 insertions, 0 deletions
   (purely additive, confirmed via `git diff --stat`).

6. Updated the pinned corpus total in `tests/unit/test_inversion_phase3_deletion_1595.py`:
   `test_claimed_plus_unclaimed_equals_corpus_size` 189 → 235 (claimed 138 → 184, unclaimed
   unchanged at 51 — confirmed by direct `gate.build_census()` + `inversion_phase0_baseline.
   load_corpus()` call, not inferred). Searched for other pinned `\b189\b` constants:
   `git grep -n "\b189\b" -- tests scripts` — only the one just-fixed hit plus unrelated binary
   fixture / logo-file / large_text.txt line-189 matches (irrelevant).

7. Re-ran the gate for CALENDAR_QUERY_PATTERNS: 49/52 literals now claimed (3 pre-existing + 46
   new). **Important difference from the PRIORITY lane**: verdict stays **GO (deletable)**, not
   NO-GO — because `meeting_time`/`recurring_meetings`/`week_calendar` are all in the live flip
   group `read_temporal`, the gate marks every UNSCORED new row `[OK]` with reason "UNSCORED but
   expected action live via group". The gate's "needs a corpus row before deletion" section is
   gated on `if lv.deletable and lv.rows:` (`scripts/inversion_phase3_deletion_gate.py` line
   ~624) — since CALENDAR stays GO/deletable (unlike PRIORITY, which flipped to NO-GO and so
   suppressed that section entirely), this section DOES print, and it correctly lists the 3
   structurally-unreachable literals by name. **This is accurate gate behavior, not a coverage
   gap**: those 3 literals can never be converted into a claiming corpus row by construction (no
   phrase can make them win against the earlier sibling that always shadows them). The dispatch
   prompt's "0 CALENDAR 'needs a corpus row' lines" expectation does not hold here the way it
   happened to for PRIORITY (where NO-GO suppressed the section as a side effect of FLOOR
   disposition, not because the unreachable literals got rows) — flagging this explicitly for
   the Lead rather than silently declaring 0.

8. Ran both dry-run validations — no LLM calls (each script self-reports this):
   - `inversion_phase1_shadow_score.py --dry-run` → "dry-run complete: corpus + grammar +
     selections validated, no LLM calls." Exit 0. Same pre-existing TEMPORAL shared-subset
     cross-validation note as prior sessions (`what's on my calendar today?` REGRESSION) —
     unrelated to and unaffected by this unit (no TEMPORAL rows touched, pre-existing row only).
   - `inversion_phase2_gate.py --dry` → "dry run complete... No LLM calls made." Exit 0. Reports
     `phase0 corpus: 235 rows (untouched)`.

9. `ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes needed;
   `ruff format --check` + `ruff check` both clean on re-run.

10. Tests (all run this turn, output quoted below):
    - `tests/unit/test_inversion_phase3_deletion_1595.py` — 19 passed.
    - `tests/unit/services/intent_service/test_preclaim_shadow.py` — 29 passed.
    - `tests/test_architecture_enforcement.py` — **63 passed, 1 xfailed, clean** — the
      concurrent, unrelated `llm_domain_service.py` / `test_only_the_shadow_observer_may_
      import_the_router` failure the PRIORITY lane flagged at 21:30 has since cleared (another
      lane's in-flight #1897 work landed/resolved between that session and this one); no action
      needed from this unit.
    - Extraction ceiling re-confirmed 548 via direct `pattern_literal_counts.
      total_literal_count()` call AND via the `ExtractionPatternRatchet`-family tests in
      isolation (3 passed, 0 failed, 61 deselected).

11. Added a progress-log entry to `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`.

## Rows added — CALENDAR_QUERY_PATTERNS (category QUERY)

All actions verified directly via `intent.action` from the real production function, not
hand-derived from reading the branch's if/elif (see finding #3 above for why that matters).

| phrase | literal exercised | action | flip group | reworded? |
|---|---|---|---|---|
| "what is on my calendar" | `\bwhat is on my calendar\b` | meeting_time | read_temporal | no |
| "show me my calendar today" | `\bmy calendar today\b` | meeting_time | read_temporal | no |
| "calendar today please" | `\bcalendar today\b` | meeting_time | read_temporal | no |
| "what meetings today" | `\bmeetings today\b` | meeting_time | read_temporal | no |
| "do i have any meetings" | `\bdo i have any meetings\b` | meeting_time | read_temporal | no |
| "do i have meetings" | `\bdo i have meetings\b` | meeting_time | read_temporal | no |
| "what meetings do i have" | `\bwhat meetings do i have\b` | meeting_time | read_temporal | no |
| "what meetings are coming up" | `\bwhat meetings\b` | meeting_time | read_temporal | no |
| "what's my schedule today" | `\bmy schedule today\b` | meeting_time | read_temporal | no |
| "today's schedule please" | `\btoday'?s schedule\b` | meeting_time | read_temporal | no |
| "what's the schedule for today" | `\bschedule for today\b` | meeting_time | read_temporal | no |
| "what's my agenda today" | `\bagenda.*today\b` | meeting_time | read_temporal | no |
| "what's my agenda tomorrow" | `\bagenda.*tomorrow\b` | meeting_time | read_temporal | no |
| "what's my agenda this week" | `\bagenda.*this week\b` | meeting_time | read_temporal | no (see finding #3 — action via collateral "my agenda" match) |
| "what's my agenda next week" | `\bagenda.*next week\b` | meeting_time | read_temporal | no (same mechanism) |
| "show me my agenda" | `\bmy agenda\b` | meeting_time | read_temporal | no |
| "show me calendar for tomorrow" | `\bcalendar.*tomorrow\b` | meeting_time | read_temporal | no |
| "tomorrow's calendar please" | `\btomorrow'?s calendar\b` | meeting_time | read_temporal | no |
| "how many meetings do I have tomorrow" | `\bmeetings.*tomorrow\b` | meeting_time | read_temporal | yes (avoid `\bwhat meetings do i have\b`) |
| "what's the schedule tomorrow" | `\bschedule.*tomorrow\b` | meeting_time | read_temporal | no |
| "tomorrow's schedule please" | `\btomorrow'?s schedule\b` | meeting_time | read_temporal | no |
| "what's happening tomorrow" | `\bwhat'?s.*tomorrow\b` | week_calendar | read_temporal | no |
| "show calendar this week" | `\bcalendar.*this week\b` | week_calendar | read_temporal | no |
| "show calendar next week" | `\bcalendar.*next week\b` | week_calendar | read_temporal | no |
| "what's the schedule this week" | `\bschedule.*this week\b` | week_calendar | read_temporal | no |
| "what's the schedule next week" | `\bschedule.*next week\b` | week_calendar | read_temporal | no |
| "how many meetings this week" | `\bmeetings.*this week\b` | week_calendar | read_temporal | no |
| "how many meetings next week" | `\bmeetings.*next week\b` | week_calendar | read_temporal | no |
| "how much time in meetings do I have" | `\bhow much time in meetings\b` | meeting_time | read_temporal | yes (avoid `\bmeetings today\b`) |
| "how much time do I spend sitting in meetings" | `\bhow much time.*meetings\b` | meeting_time | read_temporal | no |
| "time spent in meetings is high lately" | `\btime spent in meetings\b` | meeting_time | read_temporal | yes (avoid `\bmeetings.*this week\b`) |
| "what's my meeting time today" | `\bmeeting time\b` | meeting_time | read_temporal | no |
| "let's review my recurring meetings" | `\breview.*recurring meetings\b` | recurring_meetings | read_temporal | no |
| "audit my standing meetings" | `\baudit.*standing meetings\b` | recurring_meetings | read_temporal | no |
| "recurring meetings keep piling up" | `\brecurring meetings\b` | recurring_meetings | read_temporal | yes (avoid `\bshow.*recurring meetings\b`) |
| "show me my week" | `\bshow.*my week\b` | week_calendar | read_temporal | no |
| "what's the week ahead look like" | `\bweek ahead\b` | week_calendar | read_temporal | no |
| "show the week calendar" | `\bweek calendar\b` | week_calendar | read_temporal | no |
| "check my calendar for conflicts" | `\bcheck.{0,10}calendar\b` | week_calendar | read_temporal | no |
| "is my calendar showing any conflict" | `\bcalendar.*conflict\b` | week_calendar | read_temporal | yes (avoid `\bcalendar.*tomorrow\b` / `\bcheck.{0,10}calendar\b`) |
| "does my calendar overlap with hers" | `\bcalendar.*overlap\b` | week_calendar | read_temporal | no |
| "is there a conflict on my calendar" | `\bconflict.*calendar\b` | week_calendar | read_temporal | no |
| "find time for a 1:1 with sarah" | `\bfind time for\b` | week_calendar | read_temporal | no |
| "find some time for a sync" | `\bfind.{0,10}time.{0,10}(?:meeting\|1:1\|1 on 1\|sync\|chat)\b` | week_calendar | read_temporal | no |
| "schedule a quick call" | `\bschedule.{0,10}(?:1:1\|1 on 1\|meeting\|sync\|call)\b` | week_calendar | read_temporal | no |
| "book a slot with the team" | `\bbook.{0,10}(?:meeting\|time\|1:1\|slot)\b` | week_calendar | read_temporal | no |

46 rows total. All live-routable (flip group `read_temporal` is in the `--live` set).

## Unreachable literals (3) — no deposit, reported as findings

All three are structurally shadowed by an earlier literal in the SAME `CALENDAR_QUERY_PATTERNS`
list (first-match-wins in `_first_pattern_match`): every string satisfying the later pattern
necessarily also satisfies the earlier one. Confirmed empirically with 2 different phrasings
each (not just inferred from the regex text):

1. `r"\bon my agenda\b"` — any match necessarily contains the word-bounded substring "my
   agenda" (the "on " is just a prefix), claimed first by `r"\bmy agenda\b"` (earlier in the
   list).
2. `r"\bwhat'?s on my calendar.*tomorrow\b"` — any match necessarily contains "what's on my
   calendar" (or "what is on my calendar") as a prefix, claimed first by `r"\bwhat'?s on my
   calendar\b"` (list position 0) or `r"\bwhat is on my calendar\b"`.
3. `r"\bmy calendar tomorrow\b"` — any match necessarily contains "calendar" immediately
   followed (within `.*`) by "tomorrow", claimed first by `r"\bcalendar.*tomorrow\b"` (earlier
   in the list).

Not filed as separate GitHub issues — same convention the PRIORITY/GUIDANCE lanes used; these
are a property of the existing regex ordering, not new bugs.

**Divergence from the PRIORITY lane's experience, flagged for the Lead**: PRIORITY's gate re-run
reported 0 "needs a corpus row" lines after its 5 unreachable literals, but that was because
PRIORITY's verdict flipped to NO-GO (FLOOR disposition, no flip group) — which suppresses the
entire missing-literals section as a side effect, not because those 5 got rows. CALENDAR's
verdict stays GO (all three destinations live via the `read_temporal` flip group), so the
section does NOT suppress, and it correctly lists these 3 unreachable literals by name in the
post-deposit gate output (quoted below). This is the gate behaving correctly — it is not a
shortfall in this unit's deposit coverage.

## Gate output — before

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 189 rows total = 138 claimed + 51 unclaimed

## CALENDAR_QUERY_PATTERNS
literals: 52  |  rows claimed: 3/189
verdict: GO (deletable) — deleting removes 52 literals: ceiling 548 -> 496

rows claimed:
  [OK] "what's on my calendar today?" -> claim=meeting_time expected=action:meeting_time router=meeting_time@1.0 verdict=MATCH :: MATCH
  [OK] "show my recurring meetings" -> claim=recurring_meetings expected=REVIEW router=recurring_meetings@1.0 verdict=REVIEW :: REVIEW-agrees (route=recurring_meetings == claim=recurring_meetings)
  [OK] "what's my week look like?" -> claim=week_calendar expected=REVIEW router=week_calendar@1.0 verdict=REVIEW :: REVIEW-agrees (route=week_calendar == claim=week_calendar)

pattern->corpus conversion needed (49 literal(s) unexercised):
  [... 49 lines, one per unexercised literal ...]
```

## Gate output — after

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 235 rows total = 184 claimed + 51 unclaimed

## CALENDAR_QUERY_PATTERNS
literals: 52  |  rows claimed: 49/235
verdict: GO (deletable) — deleting removes 52 literals: ceiling 548 -> 496

rows claimed:
  [OK] "what's on my calendar today?" -> claim=meeting_time expected=action:meeting_time router=meeting_time@1.0 verdict=MATCH :: MATCH
  [OK] "show my recurring meetings" -> claim=recurring_meetings expected=REVIEW router=recurring_meetings@1.0 verdict=REVIEW :: REVIEW-agrees (route=recurring_meetings == claim=recurring_meetings)
  [OK] "what's my week look like?" -> claim=week_calendar expected=REVIEW router=week_calendar@1.0 verdict=REVIEW :: REVIEW-agrees (route=week_calendar == claim=week_calendar)
  [OK] "what is on my calendar" -> claim=meeting_time expected=action:meeting_time router=None@None verdict=UNSCORED :: UNSCORED but expected action live via group
  [... 45 more [OK]/UNSCORED lines, one per new deposit row — all correctly UNSCORED, "expected
       action live via group" (not NO-GO — see note above re: flip-group live mechanism) ...]

pattern->corpus conversion needed (3 literal(s) unexercised):
  needs a corpus row before deletion: r"\bon my agenda\b"  (list=CALENDAR_QUERY_PATTERNS)
  needs a corpus row before deletion: r"\bwhat'?s on my calendar.*tomorrow\b"  (list=CALENDAR_QUERY_PATTERNS)
  needs a corpus row before deletion: r"\bmy calendar tomorrow\b"  (list=CALENDAR_QUERY_PATTERNS)
```

`UNSCORED`/"expected action live via group" is EXPECTED and correct for this unit — the deposit
rows score `UNSCORED` until the Lead's budgeted (LLM-calling) shadow-score run judges them; that
run is explicitly out of scope here. The 3 remaining "needs a corpus row" lines are the 3
structurally-unreachable literals, not a gap — they cannot ever be satisfied by any corpus row
(see "Divergence from the PRIORITY lane" above).

## New corpus total

189 → **235** rows (+46). Per-category denominators after rebuild: **QUERY 85** (was 39),
PRIORITY 41, GUIDANCE 26, TEMPORAL 21, EXECUTION 18, PORTFOLIO 16, STATUS 8, CONVERSATION 5,
SYNTHESIS 4, IDENTITY 3, MEMORY 3, DISCOVERY 2, PROVENANCE 1, TRUST 1, ANALYSIS 1.

## Test / gate exit status

- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → wrote 235 rows (59 REVIEW), exit 0.
- `git diff --stat tests/fixtures/inversion_corpus_phase0.yaml scripts/build_inversion_corpus_phase0.py`
  → `2 files changed, 560 insertions(+)`, zero deletions.
- `venv/bin/python scripts/inversion_phase1_shadow_score.py --dry-run` → exit 0, "no LLM calls"
  self-reported.
- `venv/bin/python scripts/inversion_phase2_gate.py --dry` → exit 0, "No LLM calls made"
  self-reported; `phase0 corpus: 235 rows (untouched)`.
- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list CALENDAR_QUERY_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  → exit 0, 49/52 claimed, verdict GO, 3 "needs a corpus row" lines (the 3 unreachable literals,
  grep-confirmed: `grep -c "needs a corpus row"` → 3).
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` → **19
  passed**, exit 0.
- `venv/bin/python -m pytest tests/unit/services/intent_service/test_preclaim_shadow.py -q` →
  **29 passed**, exit 0.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63 passed, 1
  xfailed**, exit 0 (clean — no concurrent failures this run).
- `venv/bin/python -c "import sys; sys.path.insert(0,'scripts'); import pattern_literal_counts
  as plc; print(plc.total_literal_count())"` → **548**, unchanged (ceiling untouched — no
  pre_classifier literal edited/deleted).
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q -k
  "ExtractionPattern or CEILINGS or pattern_literal"` → **3 passed**, exit 0 (ceiling ratchet
  specifically, isolated).
- `venv/bin/ruff format` + `ruff check --fix` on both touched `.py` files → clean, no changes
  needed; `ruff format --check` + `ruff check` both clean on re-run.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (HAND_ROWS: +46 rows in a `# —
  CALENDAR_QUERY_PATTERNS` delimited block, extending the existing `# phase3-conversion`
  section, after the PRIORITY block)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, purely additive, 189→235 rows)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (one pinned constant corrected 189→235,
  with updated docstring)
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (progress-log entry added)

**Not touched**: git index (no staging/commit — per dispatcher instruction),
`services/intent_service/pre_classifier.py` (no pattern edited/deleted, read only),
`services/intent_service/reminder_clear.py` and `services/intent_service/workflow_entries.py`
(the dispatcher's named concurrent-lane files — explicitly excluded; `workflow_entries.py` was
read-only consulted for `_CALENDAR_QUERY_FLIP_GROUPS`/`_CALENDAR_QUERY_COHORT`, never edited),
any flag/env var, `scripts/inversion_phase3_deleted_patterns.json` (no deletion performed).

## Verified how

- **Method**: for each of the 49 unexercised literals, called the REAL production functions
  directly in a Python script against this worktree's code —
  `PreClassifier.pre_classify_with_pattern_list(phrase)` (list-name assertion AND `intent.action`
  read directly, not hand-derived — see finding #3 on why hand-tracing the if/elif would have
  mispredicted two rows) and `PreClassifier._first_pattern_match(cleaned,
  PreClassifier.CALENDAR_QUERY_PATTERNS)` (literal-identity assertion). For the 3 unreachable
  literals, tested 2 independent phrasings each before concluding structural unreachability.
  Gate re-runs, pytest, and ruff invocations were all run this turn via Bash and their output is
  quoted/counted above, not recalled from memory.
- **Layer measured**: surface 1 only (the deterministic pre-classifier), by design of this unit
  — the Phase-1 router/LLM layer is deliberately UNSCORED here (no LLM calls made anywhere in
  this session, confirmed by each script's own self-report and the absence of any LLM-client
  invocation in the commands run).
- **Denominator**: 1 target list (CALENDAR_QUERY_PATTERNS) — 46 of 49 previously-flagged
  unexercised literals now have a corpus row; 3 confirmed structurally unreachable and
  explicitly reported (and, unlike the PRIORITY lane's analogous 5, these 3 remain VISIBLE in
  the gate's post-deposit "needs a corpus row" output rather than suppressed — explained above,
  not silently dropped either way). Test denominator: 19/19 in the target Phase-3 test file
  pass, 29/29 in the pre-claim shadow test file pass, 63/63 (plus 1 pre-existing xfail) in the
  full architecture-enforcement suite (full file run, not a subset), 3/3 in the
  extraction-ceiling-specific test subset. Ceiling denominator: 548/548 unchanged, confirmed by
  direct call, not inferred.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §"Phase 3 —
  deletion gate"; `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (procedure +
  progress log); prior prog session log
  `2026-09-30-2130-prog-code-log-1595-phase3-deposits-priority.md` (verification methodology,
  row-block convention, `notes` field precedent); `action_registry.py` (`ActionDisposition`
  lookup, confirming WORKFLOW for all three CALENDAR actions, all registered — unlike PRIORITY's
  single FLOOR action); `workflow_entries.py` (`_CALENDAR_QUERY_FLIP_GROUPS` /
  `_CALENDAR_QUERY_COHORT`, read only).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing worktree — no mailbox write, no sign-off merge, per
  dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient.

## Discovered work

None filed as separate issues. Two findings reported inline (matching the PRIORITY/GUIDANCE
lanes' convention):
1. 3 structurally unreachable CALENDAR_QUERY_PATTERNS literals (listed above) — a property of
   existing regex ordering.
2. The claiming-literal / action-determining-match independence for the two "agenda...week"
   rows (finding #3 above) — not a bug, but worth the Lead knowing the branch's action isn't a
   pure function of which CALENDAR_QUERY_PATTERNS literal claims first.
