# 2026-10-01 0745 — prog (Coding Agent) — #1595 Phase 3, third deletion: CALENDAR_QUERY_PATTERNS (first live list)

**Role**: prog (Coding Agent), model Sonnet 5. Dispatched by Lead Developer, in the Lead's
worktree (`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`).
No git index touched at any point (per dispatch instruction — no staging/commit performed).
No LLM calls anywhere in this unit; no flag/env changes.

## Task

Phase 3's third deletion of the #1595 Inversion epic-0 unit 5 — delete `CALENDAR_QUERY_PATTERNS`
(52 literals), the FIRST deletion whose corpus rows route to LIVE rail keys
(meeting_time/week_calendar/recurring_meetings, flip_group `read_temporal`) rather than pure
pattern-vs-pattern evidence, following the exact procedure the first two deletions established.

## Read first

- `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (full "First deletion" +
  "Second deletion" subsections, the "fifth consumer"/#1899 paragraph, the "scored on BOTH
  tables" rule, the `get_current_time` rail-key ruling)
- First + second deletion logs: `dev/2026/09/27/2026-09-27-0850-prog-code-log-1595-phase3-delete-reminder-lists.md`,
  `dev/2026/09/28/2026-09-28-0650-prog-code-log-1595-phase3-delete-todo-query.md`
- `scripts/inversion_phase3_deleted_patterns.json` (ledger entry shape, 3 prior entries)
- `tests/unit/services/intent_service/_inversion_pin_helper.py` (shared stub helper)

## Gate before deletion

```
venv/bin/python scripts/inversion_phase3_deletion_gate.py --list CALENDAR_QUERY_PATTERNS \
  --live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal
```
→ `live set source: --live = [...]`, `corpus denominator: 283 rows total = 232 claimed + 51 unclaimed`,
`literals: 52  |  rows claimed: 49/283`, `verdict: GO (deletable) — deleting removes 52 literals:
ceiling 548 -> 496`, `pattern->corpus conversion: ... 3 literal(s) unexercised` — exactly matching
the dispatch prompt's expected numbers (49 rows claimed, 52 literals, 3 structurally shadowed).

## What I did

1. **Tombstoned `CALENDAR_QUERY_PATTERNS`** in `pre_classifier.py`: `= []  # type: List[str]`, same
   tombstone form as the first two deletions. Added comments at THREE sites noting the resulting
   dead code is intentional and survives: (a) the class attribute itself (cites the Haiku baseline,
   the CALENDAR-specific rescores, CXO's 10-01 floor ruling, the 3 shadowed literals); (b) the
   `pre_classify` inline branch whose meeting_time/recurring_meetings/week_calendar sub-lists only
   ever ran to disambiguate an already-claimed phrase — now structurally unreachable; (c)
   `_get_calendar_action` (the `detect_multiple_intents` equivalent) and (d)
   `CALENDAR_QUERY_PATTERNS`'s membership in `_READ_LANE_GROUPS`. No other `*_PATTERNS` list
   touched (TEMPORAL_PATTERNS explicitly left alone, per dispatch instruction).

2. **Ledger entry** in `scripts/inversion_phase3_deleted_patterns.json`: all 49
   `rows_claimed_at_deletion` phrases; `expected_ops: ["meeting_time", "week_calendar",
   "recurring_meetings"]` (the three real ops — "floor" is not an op); `expected_op_by_phrase` for
   every one of the 49 rows (floor-ruled rows get the literal string `"floor"`); `shadowed_literals`
   naming the 3 unreachable literals and which sibling shadows each; `verdict_report` listing the
   Haiku baseline + the 3 CALENDAR-specific reports; a full `note`.

3. **`known_reabsorptions` — the defining finding of this unit**: post-deletion census shows
   `TEMPORAL_PATTERNS` reabsorbing **19 of the 49** claimed phrases, ALL disagreeing (claimed as
   `get_current_time`, never the ruled destination). Per the dispatch's explicit instruction
   ("ONLY if the claimed action agrees... if TEMPORAL claims a calendar phrase as get_current_time,
   that is a real finding... report it, do not silence it"), none of these 19 qualify for the
   AGREEING shape the second deletion's `known_reabsorptions` precedent used. Documented each with
   an explicit `"agrees": false` field, the reclaiming list, the claimed action, and a note
   explaining why production is still safe (`consult_inversion_live` precedence — the live
   Inversion consult runs BEFORE this surface-1 fallback and already proves each row safe when the
   live flag carries `read_temporal`; the fallback claim only bites when the live consult stands
   down).

4. **Mechanism gap found and fixed** (`scripts/inversion_phase3_deletion_gate.py`): neither the
   reclaimed-phrase branch NOR the unclaimed-phrase branch of `check_deleted_entry_non_regression`
   had ever needed a live-flag-aware (condition-c, MISMATCH-but-live-route) escape, because no
   earlier ledger entry's rows needed one. CALENDAR's entry exposed this immediately (3 rows: 1
   unclaimed-but-MISMATCH-live — "what meetings are coming up" — and 2
   reclaimed-but-disagreeing-yet-independently-safe — "what is on my calendar", "is there a
   conflict on my calendar"). Fixed by unifying both branches onto ONE re-derivation of
   `row_disposition` (the exact MATCH/agreeing-REVIEW/live-MISMATCH proof `build_census` uses at
   gate time), fed a synthetic `ClaimResult` carrying the phrase's resolved target op
   (`expected_op_for_phrase`) instead of the (possibly wrong) surviving pattern's own claim. Added
   a `cats: Optional[frozenset]` parameter to `check_deleted_entry_non_regression`, threaded by
   callers — omitted/`None` reproduces every earlier ledger entry's behavior byte-for-byte (none of
   REMINDER_PATTERNS/REMINDER_QUERY_PATTERNS/TODO_QUERY_PATTERNS' rows ever needed a live
   condition). `known_reabsorptions` gained an `"agrees"` field (omitted/`true` = the original,
   unchanged agreeing shape); a documented `"agrees": false` entry can still pass non-regression
   when the phrase's OWN frozen router evidence independently re-proves it safe — an UNDOCUMENTED
   reclaim still fails loud unconditionally (the surprise itself, not just eventual safety, is what
   the check exists to catch).

   Verified the fix precisely: with `cats=None` (no live flag), the real CALENDAR entry's
   non-regression check correctly FAILS on exactly the 3 rows that need the live escape
   (`live-set-unknown` in each reason string); with `cats` covering `read_temporal` (the same set
   the gate run used), it passes clean (`ok=True`).

5. **Ceiling**: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 548 → 496
   (`pattern_literal_counts.total_literal_count()` confirms 496), arithmetic in the comment.

6. **Converted every broken surface-1 pin** (18 failures on the first full-suite pass after
   emptying the list; a further 2 surfaced after converting the first round, both TEMPORAL
   reabsorption casualties outside the 49 corpus rows — found empirically, not predicted). Every
   failure converted, never deleted, across 7 test files:
   - `test_calendar_query_handlers.py::TestPreClassifierRoutingIntegration` — converted to the
     decline+inversion-routes idiom via `_inversion_pin_helper.assert_inversion_routes`
     (`live_categories="read_temporal"`); plus a new
     `test_meeting_time_variants_reabsorbed_by_temporal` pinning 2 test-local TEMPORAL-reabsorption
     casualties ("how much time in meetings today", "meeting time today") found only after the
     first conversion pass.
   - `test_action_registry.py::TestRegistryCoverage::test_example_messages_classify_correctly` —
     gained a documented `_KNOWN_TEMPORAL_REABSORPTION_EXAMPLES` skip-list for the ONE
     `ACTION_EXAMPLES` production documentation string ("How much time do I spend in meetings
     today?") that is itself a TEMPORAL-reabsorption casualty.
   - `test_action_registry.py::TestMultiIntentSubsumption::test_calendar_check_does_not_produce_temporal`
     — rewritten: the #919 premise it pinned (QUERY should subsume TEMPORAL for calendar-conflict
     checks) no longer holds (CXO ruled this a floor ask, no QUERY claim exists); now asserts no
     QUERY claim survives AND pins the current (reported) TEMPORAL reabsorption explicitly rather
     than asserting its absence.
   - `test_keyword_disambiguation_901.py::TestKeywordDisambiguationQ33`/`Q62` — 7 tests rewritten:
     these two classes pinned the ORIGINAL #901 disambiguation fix (calendar-shaped asks →
     QUERY, not TEMPORAL) that `CALENDAR_QUERY_PATTERNS` existed to provide — a fix this deletion
     plus the CXO floor ruling intentionally SUPERSEDES, not breaks. Capability-gap phrases now
     assert decline (`None`); the two phrases that are TEMPORAL-reabsorption casualties now assert
     the documented reabsorption explicitly.
   - `test_greeting_pleasantry_only_1416.py::test_agenda_phrasing_still_reaches_agenda_not_greeting`
     — converted to a STRONGER form of its own contract: the compound message now declines
     entirely at `pre_classify` (TEMPORAL_PATTERNS has no "agenda" vocabulary, confirmed
     empirically) rather than merely avoiding a "greeting" mislabel.
   - `test_preclaim_shadow.py::TestSampledOn::test_multi_intent_surface_schedules_with_all_lists`
     and `TestPatternIdentityThreading::test_multi_surface_pattern_lists_align_with_intents` — both
     swapped from "hi piper! what's on my agenda?" (greeting + calendar) to "hi piper! what's
     blocking the milestone?" (greeting + ANALYSIS_PATTERNS) — same idiom as the first two
     deletions' "give me my standup" swaps (the agenda pairing collapses to greeting-only
     post-deletion since TEMPORAL_PATTERNS doesn't claim "agenda").

7. **Reachability ratchet**: `git grep` for `meeting_time`/`week_calendar`/`recurring_meetings` and
   for calendar/meeting/schedule/agenda vocabulary in `chat_pointers.py` — no POINTER row uses a
   CALENDAR-shaped canonical phrase, so `TestChatPointersReachabilityRatchet`'s
   `phase3-deletion-ledger` resolver is never exercised for this entry. Confirmed, not assumed.

8. **New synthetic tests** in `test_inversion_phase3_deletion_1595.py` (9 total): the floor
   expectation's handling (unclaimed-and-MATCH, reclaimed-and-documented-disagreeing, both pass
   without needing `cats`; undocumented reclaim still fails even when independently safe); the
   MISMATCH-but-live-route case genuinely needing `cats`; plus 2 ledger-specific tests
   (`test_real_ledger_has_the_first_four_deletions` updated; new
   `test_calendar_entry_fails_non_regression_without_the_live_flag`,
   `test_calendar_entry_known_reabsorptions_are_all_documented_disagreements`).

9. **Docs**: `intent-routing-stack.md` gains a "Third deletion (2026-10-01): CALENDAR_QUERY_PATTERNS
   — the first live list" subsection (full account — gate evidence, the sibling-takeover finding,
   the mechanism fix, every converted test file, the reachability-ratchet confirmation). Scope doc
   `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` gets a 2026-10-01 progress-log
   entry.

10. **`ruff format` + `ruff check --fix`** on all 9 touched `.py` files — clean, no changes needed
    beyond what was already written correctly.

## Evidence

- Gate (before deletion, quoted in full above): GO, 49/49 claimed, 52 literals, ceiling
  548 → 496, 3 unexercised literals (the known shadowed set, not a blocker).
- Gate (`--all`, after deletion, same `--live` flag): `corpus denominator: 283 rows total = 202
  claimed + 81 unclaimed` (232 → 202, a drop of 30 = 49 minus the 19 reabsorbed-but-independently-safe
  phrases — `CALENDAR_QUERY_PATTERNS` shows `0 0 NO ROWS`).
- `pattern_literal_counts.total_literal_count()` = 496 confirmed directly.
- `tests/unit/services/intent_service/ tests/unit/services/intent/`: **5020 passed** (full run,
  no `-x`/`--maxfail=1` early-stop, every failure surfaced and converted across two passes).
- `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py`:
  **95 passed, 1 xfailed** (ceiling exact at 496).
- `scripts/run-sweep.sh ratchets`: **73 passed, 1 xfailed** + mypy gate — "all 24 ratcheted codes
  at ceiling (total=1121; ... var-annotated=69)" — identical to the prior two deletions' baseline,
  confirming the `# type: List[str]` comment-annotation idiom (not a bare `: List[str] = []`
  annotation, which an `ast.AnnAssign` would hide from `pattern_literal_counts.py`'s AST scanner)
  was applied correctly and adds no new mypy var-annotated error.
- `ruff format` + `ruff check --fix`: clean on every touched file (`9 files left unchanged` /
  `All checks passed!`).
- Non-regression mechanism directly verified: real CALENDAR ledger entry with `cats=None` → `ok=False`,
  exactly 3 problems, all naming `live-set-unknown`; with `cats` covering `read_temporal` → `ok=True`.

**Verified how**: every count above is a command run THIS session and its literal output quoted —
pytest exit summaries, the gate script's own printed census (before AND after deletion),
`pattern_literal_counts.total_literal_count()` invoked directly, and a direct
`check_deleted_entry_non_regression` call against the real (not synthetic) ledger entry with and
without `cats`. Layer: the deterministic layer only (pre-classifier regex matching, corpus-row
lookups, frozen router-report table parsing, the gate's own `row_disposition` re-derivation) — zero
live LLM calls anywhere in this unit; every router "verdict" consulted is a FROZEN, already-scored
report (the 2026-10-01 Haiku baseline + the 3 CALENDAR-specific rescores) or a monkeypatched stub in
tests. Denominator: the full `tests/unit/services/intent_service/` + `tests/unit/services/intent/`
suite (not a subset, 5020/5020), both ratchet/ledger suites, and the sweep script, all read to
completion.

## Files touched (no commit — Lead stages)

- `services/intent_service/pre_classifier.py` — the deletion + 4 tombstone/inert-dead-code comments.
- `scripts/inversion_phase3_deletion_gate.py` — `check_deleted_entry_non_regression` unified
  live-aware re-derivation (`cats` parameter, `known_reabsorptions`'s `"agrees"` field), docstring
  rewrite.
- `scripts/inversion_phase3_deleted_patterns.json` — 1 new ledger entry (49 phrases,
  `expected_op_by_phrase`, `shadowed_literals`, 19 `known_reabsorptions`, all `agrees: false`).
- `tests/test_architecture_enforcement.py` — ceiling 548→496.
- `tests/unit/test_inversion_phase3_deletion_1595.py` — ledger pin updated to 4 entries; 9 new
  tests (mechanism synthetics + 2 ledger-specific).
- `tests/unit/services/intent_service/test_calendar_query_handlers.py` — converted + 1 new test.
- `tests/unit/services/intent_service/test_action_registry.py` — 2 tests rewritten.
- `tests/unit/services/intent_service/test_keyword_disambiguation_901.py` — 7 tests rewritten.
- `tests/unit/services/intent_service/test_greeting_pleasantry_only_1416.py` — 1 test rewritten.
- `tests/unit/services/intent_service/test_preclaim_shadow.py` — 2 tests swapped.
- `docs/internal/architecture/current/intent-routing-stack.md` — "Third deletion" subsection.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — progress log entry.

No git add/commit/staging performed at any point (dispatcher instruction). Reporting back to Lead
via SubagentHandback.

## Discovered work

- **19-phrase TEMPORAL reabsorption, documented not filed separately** — per the dispatch's own
  framing ("report it, do not silence it"), this is reported in full in the ledger's
  `known_reabsorptions` and in the routing-stack doc. Whether TEMPORAL_PATTERNS' calendar/meeting/
  schedule vocabulary overlap should be narrowed is a question for CXO/Arch, flagged but not
  resolved here (out of this unit's scope — the corpus rows this deletion is licensed against are
  all independently proven safe regardless of the reclaim).
- **Mechanism gap in `check_deleted_entry_non_regression`** — fixed in this unit (item 4 above),
  not just reported, since it blocked this deletion's own ledger entry from passing.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 (First +
  Second deletion subsections, the worked-example procedure this session extended) — informed the
  whole task; the two prior deletion logs — informed tombstone form, ledger shape, test-conversion
  idiom; `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` (esp. the 09-30 CALENDAR
  deposits entry naming the 3 shadowed literals and the "4 shadowed TEMPORAL literals" finding) —
  informed the shadowed-literals documentation and the scale of the reabsorption finding;
  `_inversion_pin_helper.py` (shared stub helper, reused verbatim).
- **Loaded but not referenced**: CLAUDE.md's mailbox/sign-off/worktree-model sections (bounded prog
  dispatch inside an existing worktree, no mailbox write, no sign-off merge, no git index touched,
  per dispatcher scope).
- **Wanted but not found**: none — the dispatch prompt's cited sources were sufficient; the two
  genuinely new findings (the 19-phrase reabsorption scale, the non-regression mechanism's
  live-flag gap) were found by direct investigation (running the gate before/after, probing the
  checker with the real entry), not something a briefing doc should have pre-empted.
