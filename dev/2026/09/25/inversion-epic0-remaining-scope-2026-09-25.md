# Epic 0 (#1595 Inversion) — what "finished or blocked" means from here

**Lead, 2026-09-25 15:5x PT.** Written the hour PM's rule made epic 0 the current epic. Measured
state first, then the units, then the exit test. Nothing here is a schedule.

## Measured state (this hour)
- **Live on Fly (v136)**: `PIPER_INVERSION_LIVE_CATEGORIES=read_status,read_referent,read_synthesis,create_todo`,
  `PIPER_INVERSION_SHADOW=1`. Three read waves + one allowlisted write (#1677). Read via
  `fly ssh console … printenv`, not from memory.
- **Coverage** (`scripts/inversion_phase2_gate.py --audit`, registry read, no LLM): 72/93 READ
  rail keys are wave-addressable; **21 are not** — 17 with neither group nor category
  (the temporal cohort: changes_since/what_changed/show_changes, week_ahead/whats_my_week_like,
  how_much_time_in_meetings, review_recurring_meetings, audit_meetings, calendar_analysis; and the
  strategic cohort: create_plan, strategic_planning, prioritize, set_priorities, learn_pattern,
  detect_pattern, generate_content, create_content) + 4 category-only (changes_query,
  meeting_time, recurring_meetings, week_calendar — swept only if someone names `QUERY`, which
  nobody should).
- **Writes**: 0 of 34 non-READ keys carry a group (enforced at construction); the named-write
  allowlist holds exactly `create_todo`.
- **Corpus rows still open on this epic**: #1559 (reminder with time+day → a WRITE, create_reminder),
  #1579 (portfolio list with the "me" token → READ, list_projects family), #1606 (two-part
  clear-except + set-default-repo → multi-intent, one WRITE). None is fixable by a pattern
  (extraction ratchet); all three close when their operation routes through the inversion.

## Units, in order (each is one reviewed change with its own flag token and revert = unset)
1. **Wave 2 — `read_temporal`.** Assign `flip_group="read_temporal"` on the 13 temporal READ
   entries (kickoff §2.2 held temporal last because time faces were unowned; #1887 now gives one
   timezone resolver). Gate: per-category shadow score on the temporal corpus rows BEFORE naming
   the wave in the flag — budget ask to PM (~the temporal rows × 1 call; the audit prints the
   denominator). Flip by adding the token; revert by removing it.
2. **Wave 3 — `read_strategic`** for the 8 strategic READ ops, same procedure. Lower priority:
   no corpus row depends on it; it exists so the ungrouped list reaches zero, which is the
   honest "reads done" line.
3. **Writes, one verified op at a time (#1677's shape, never a group)**: `create_reminder`
   first (closes #1559 when it flips and the row passes), then the clear-reminders family
   (#1606's write half). Each carries `flip_write_allowlist_key` + its own confirmation contract
   unchanged (the inversion proposes, decide_consent disposes).
4. **Multi-intent under the inversion** (#1606's other half): the orchestrator already skips
   side-effecting siblings; the inversion consult runs per turn, so a two-part turn needs the
   split to happen BEFORE the consult or the consult to return a plan. Arch question — filed on
   #1606 when unit 3 lands, not before (it may resolve itself).
5. **Phase 3 — deletion ratchet.** For every pre-classifier pattern whose corpus rows pass under
   the inversion at surface 1, delete the pattern in a change that asserts corpus
   non-regression per category (the acceptance criterion: shrink AND denominator). This is the
   only unit that actually removes the "string matching does language" layer; everything above
   makes it safe.

## Exit test (from the epic's own acceptance criteria, unchanged)
Per-category corpus non-regression, never aggregate · all 8 Exhibit-A rows pass · Arch's
"what reminders do I have?" in the gate · every `pin:` row in the gate · the ungrouped READ
list at zero · the write allowlist covering every write the corpus rows exercise · the deletion
ratchet asserting non-regression alongside shrink. **Blocked** means: a per-category score below
its floor with the cause outside the router (a handler bug), or a budget/PM gate.

## What's NOT in scope
The standing sampled shadow-check as continuous telemetry is live (`PIPER_INVERSION_SHADOW=1`);
turning its disagreements into corpus rows automatically is a separate issue, not this epic's
exit. The consent gate is untouched throughout.

## Progress log
- 2026-09-25 16:0x — **Unit 1 grouping LANDED** (13 keys, not the 12 I estimated — the calendar cohort is 9 aliases): 85/93 READ keys wave-addressable, unassigned = the 8 strategic ops, category-only list empty. Flag NOT set; shadow score pending PM's budget.
- 2026-09-25 16:03 — **Unit 2 grouping LANDED** (`3ecd26c337`): `read_strategic` = 8 keys → **93/93 READ keys wave-addressable, ungrouped 0**. The "reads done" line of the exit test is met at the registry layer. Neither wave-2 nor wave-3 token is in the live flag; both wait on the shadow score.
- 2026-09-25 16:13 — **Unit 3 (first op) LANDED** (`a3180731c4`): `create_reminder` allowlisted, three conditions re-run and quoted in the entry's comment. Allowlist = {create_todo, create_reminder}. Flag unset. Next write: the clear-reminders family (#1606's write half) — same procedure.
- 2026-09-25 16:23 — **Exit-test audit LANDED** (`98a90a4a20`): all 8 Exhibit-A catalog issues now have a judged row (8 verbatims deposited; #1488's literal is unrecoverable — the measured #1677 phrase stands in, labelled); pin rows 2/2 (routing corpus) + 1/1 (`pin:reminder-query`) covered; Arch's demanded phrase at line 213 (REVIEW by the builder's rule). **Shadow-score denominator is now 116 rows (14 TEMPORAL, 16 PORTFOLIO).** No session log carries the 13:19–13:24 transcript — the GH comments are the only record.
- 2026-09-25 17:35 — **Units 1–3 LIVE on Fly** (PM flipped create_reminder + read_strategic 16:4x, read_temporal 17:3x after the 14-row re-score cleared 4/4): flag = all five read waves + create_todo + create_reminder, v139. Unit 3's next op (clear-reminders family) and unit 4 wait on Arch's Q1/Q2 (memo `e19f98977`). Unit 5 (deletion ratchet) is next buildable once a category's corpus rows all pass under the inversion — TEMPORAL and the reminder-write rows are candidates.
- 2026-09-25 19:00 — **Unit 3 second op LANDED** (`70f7dd5159`): `delete_todo` (DESTRUCTIVE) allowlisted per Arch's floor ruling; confirm provenance parity proven. Allowlist = {create_todo, create_reminder, delete_todo}; `delete_todo` token NOT yet in the live flag (PM's hand). **Unit 4 re-scoped**: option (a) is unbuildable (orchestrator has no rail, 0/127; #1606 isn't split by surface 1) — real scope is sequential rail dispatch or an orchestrator rail leg, with Arch (memo `a71f6a6dd`). **#1896** (live route dropped a split turn's other half) fixed the same evening; deploying.
- 2026-09-27 07:2x — **Unit 5 (deletion-ratchet INSTRUMENT) BUILT, no deletion**:
  `scripts/inversion_phase3_deletion_gate.py` (+ pinning test
  `tests/unit/test_inversion_phase3_deletion_1595.py`, 19 tests) implements the epic's
  own Phase-3 conditions — per-list GO/NO-GO census over the 116-row corpus (surface-1
  claim via `pre_classify_with_pattern_list`/`MultiIntentResult.pattern_lists`, no
  re-matching; router verdicts parsed from the 09-25 report + temporal-rescore with
  documented precedence, no LLM calls; the live-flag routable set via the same
  `resolve_live_match` production uses), the pattern→corpus-conversion literal audit,
  and a `DELETED_PATTERN_LISTS` non-regression ledger (`scripts/
  inversion_phase3_deleted_patterns.json`, empty today). Measured: 84/116 rows claimed,
  32 unclaimed; `TEMPORAL_PATTERNS` claims only 2/10 TEMPORAL corpus rows (both MATCH,
  GO) — the reminder/calendar TEMPORAL rows claim via other lists, a genuine census
  finding. `pattern_literal_counts.py` factored out of
  `TestExtractionPatternRatchet._pre_classifier_count` so both consumers share one
  AST-walk (ceiling still 567, unchanged, tightness test still passes). Full suite:
  `tests/test_architecture_enforcement.py` 63 passed/1 xfailed;
  `scripts/run-sweep.sh ratchets` 73 passed/1 xfailed + mypy gate at ceiling
  (unchanged). Doc: intent-routing-stack.md gains a "Phase 3 — deletion gate" section.
  Nothing deleted; no flag/env changes; no LLM calls anywhere in this unit — Coding
  Agent (Sonnet), dispatched by Lead.
- 2026-09-27 07:0x — **Unit 3c (third op) LANDED**: `set_default_repo` allowlisted (#1606's OTHER half — the repo-set side, distinct from `delete_todo`'s clear/delete side). Three conditions re-run and quoted in the entry's comment. Allowlist = {create_todo, create_reminder, delete_todo, set_default_repo} (`--audit` confirms all four). ⚠️ Unlike its three siblings this op's ACTION_REGISTRY category is QUERY not EXECUTION, so naming the raw `QUERY` token (not a `read_*` wave) sweeps it in too — tested directly. Flag unset. **Discovered work, filed not fixed (#1898)**: `_handle_set_default_repo` reads `intent.context["original_message"]` only, with no fallback to `Intent.original_message` the way create_reminder/delete_todo's handlers have — `consult_inversion_live` only ever sets the top-level field, so a flipped turn reaches the handler and consent fires correctly but the handler itself can't see the repo and answers a graceful bad-shape nudge instead of writing the row (verified behaviorally, not assumed). #1606 is still not closed end-to-end: this allowlist entry closes one of the two remaining blockers (the allowlist condition), #1898 is the other (a one-line fix, not yet applied), and the turn still doesn't split at surface 1 (unit 4's own residual). Full suite green: `tests/unit/services/intent_service/` 4874 passed; `tests/test_architecture_enforcement.py` 63 passed/1 xfailed; `scripts/run-sweep.sh ratchets` 73 passed/1 xfailed + mypy gate at ceiling (unchanged).
- 2026-09-27 07:22 — **Unit 5 instrument LANDED** (`dc4499ffa8`). Procedure per list from here: (1) gate says GO on claimed rows; (2) deposit one corpus row per unexercised literal (phrase proven claimed by that list); (3) shadow-score the new rows (PM budget: one router call each); (4) all MATCH → delete the list + lower the extraction ceiling in the same commit + ledger entry (the pin holds the rows). First three: REMINDER (4), REMINDER_QUERY (3), TODO_QUERY (8) — deposits in flight; ~15 calls to score.
- 2026-09-27 ~09:xx — **Unit 5 FIRST DELETION LANDED**: `REMINDER_PATTERNS` (5 literals) + `REMINDER_QUERY_PATTERNS` (4 literals) emptied to `[]` in `pre_classifier.py` (tombstoned — class attrs + consumers, incl. the now-inert `REMINDER_QUERY_BLOCKERS`, survive; only literals gone). Gate re-run BEFORE deletion (both GO, 0 "needs a corpus row": REMINDER_PATTERNS 5/5 claimed rows MATCH/agreeing-REVIEW; REMINDER_QUERY_PATTERNS 4/4). Ledger: 2 entries in `scripts/inversion_phase3_deleted_patterns.json`, each with `rows_claimed_at_deletion` + `expected_ops`. Ceiling: 567 → 558 (−9). Re-measured post-deletion: corpus claimed 99 → 90 (exactly the 9 ledgered rows), **no sibling `*_PATTERNS` list reabsorbed any of them** — genuinely unclaimed at surface 1 now. Two gate/mechanism gaps found and fixed in the same commit: (a) the deletion gate only read the 09-25 full report, so the same-day Phase-3 deposits report (scored separately) came back UNSCORED and both lists read NO-GO until `RouterReports` was wired to also read `DEPOSITS_REPORT`; (b) `check_deleted_entry_non_regression` couldn't verify a REVIEW-only corpus row (`expected == "REVIEW"`, no asserted action, e.g. Arch's "what reminders do I have?" pin) — fixed to fall back to the ledger entry's own `expected_ops` for that case. `TestChatPointersReachabilityRatchet`'s `pin:reminder-query` row also broke (it only ever called bare `pre_classify`) — added a new deterministic resolver, `phase3-deletion-ledger`, that re-verifies via the SAME ledger non-regression check (no LLM). ⚠️ **Discovered, not fixed here**: any turn where a reminder-creation/listing phrase arrives while an UNRELATED offer is still armed (a full restatement, an off-intent command mid-ask, a state-question mid-ask) is structurally out of the Inversion's reach too — `consult_inversion_live`'s `turn_had_pending_offer` guard stands it down unconditionally regardless of the live flag — so these narrow shapes now depend on the free-form LLM classifier in production, the pre-#903/#1521 state for exactly that interaction window. Surfaced in 6 converted e2e tests (`test_action_fabrication_1648.py`, `test_reminder_question_acceptance_1654.py`, `test_repo_clarification_1567.py`, `test_task_clarify_1654.py`, `test_acceptance_contract_1739.py`) with classifier stubs proving the downstream seam logic is unaffected; not a regression the corpus-based deletion gate could have caught (armed-turn interaction is outside its scope) and not fixed in this unit — reported to Lead. Full suite green: `tests/unit/services/intent_service/` + `tests/unit/services/intent/` 5013 passed/1 xfailed; `tests/test_architecture_enforcement.py` 63 passed/1 xfailed (ceiling exact at 558); `tests/unit/test_inversion_phase3_deletion_1595.py` 19 passed; `scripts/run-sweep.sh ratchets` 73 passed/1 xfailed + mypy gate at ceiling (var-annotated needed the two new `[]` literals typed via `# type: List[str]` comments — a bare annotation would have hidden the lists from the AST-based literal counter). Doc updated: `intent-routing-stack.md` gains a "First deletion" subsection under Phase 3. Next: REMINDER_QUERY (3)/TODO_QUERY (8) deposits already scored in the same deposits report — TODO_QUERY_PATTERNS has a real MISMATCH ("what should I do next" → get_top_priority) so it is NOT next-up GO; re-run the gate per list before touching it.
- 2026-09-27 12:3x — **GUIDANCE_PATTERNS deposits LANDED** (prog dispatch, Sonnet, not yet committed — index untouched per dispatcher instruction): 20 of 21 GUIDANCE_PATTERNS literals were unexercised (`\bget started\b` already covered); one corpus row per literal deposited into `HAND_ROWS`, category GUIDANCE, `expected: action:get_contextual_guidance` (canonical, not an alias). Each phrase verified against the real production matcher — `PreClassifier.pre_classify_with_pattern_list` returns GUIDANCE_PATTERNS and `PreClassifier._first_pattern_match` against GUIDANCE_PATTERNS's own literals returns the exact cited literal; one phrase ("how do I set up my portfolio") had to be reworded ("I'd like to set up my portfolio") because the earlier sibling literal `\bhow do i.*set up\b` stole the claim first. No literal unreachable/shadowed after rewording. Corpus 131→151 (+20, purely additive — `git diff --stat` 81 insertions/0 deletions); pinned total in `test_inversion_phase3_deletion_1595.py` updated 131→151 (claimed 90→110, unclaimed unchanged 41); no other pinned corpus-size constant found (`git grep -n "131" -- tests scripts`, none besides the one just fixed and an unrelated fixture line). Gate re-run for GUIDANCE_PATTERNS: 21/21 literals now claimed, 0 "needs a corpus row" lines (grep-confirmed); rows correctly UNSCORED (scoring is the Lead's budgeted run, not this unit — no LLM calls made anywhere). Extraction ceiling unaffected: 558 unchanged (`pattern_literal_counts.total_literal_count()` confirmed) — deposits add corpus rows only, no pre_classifier literal touched. Tests: `test_inversion_phase3_deletion_1595.py` 19 passed, `test_preclaim_shadow.py` 29 passed, `tests/test_architecture_enforcement.py` 63 passed/1 xfailed (all unchanged from baseline). `ruff format`+`ruff check --fix` clean. GUIDANCE_PATTERNS is now GO-eligible for the same deletion procedure once the Lead's budgeted shadow-score run judges these 20 rows — not scored, not deleted, in this unit.
- 2026-09-28 07:2x — **Unit 5 SECOND DELETION LANDED** (prog dispatch, Sonnet, dispatched by
  Lead): `TODO_QUERY_PATTERNS` (10 literals) emptied to `[]` in `pre_classifier.py` (same
  tombstone form; `_todo_query_match` consumer survives, `RESTORATIVE_ASK_BLOCKERS` now inert —
  its only consumer). Gate re-run BEFORE deletion: GO, 11/11 claimed rows, 0 needs-a-corpus-row
  (the prior "what should I do next" MISMATCH was resolved same-day by CXO/PPM's
  `get_top_priority` ruling + a 1-row re-score, `inversion-phase3-todo-query-rescore-2026-09-27.md`,
  commit `657b4fc0c0` — the gate script gained an ordered newest-first `PHASE3_REPORTS` list so
  the re-score overrides the earlier verdict). Ledger entry is the FIRST with TWO `expected_ops`
  (`list_todos_query`, `get_top_priority`) — added `expected_op_by_phrase` (per-row precision)
  and `expected_op_for_phrase` in the gate script, consulted by both
  `check_deleted_entry_non_regression` and the reachability ratchet's `phase3-deletion-ledger`
  resolver instead of the old "any of expected_ops" / "bail on >1 op" logic — the bail would have
  broken the `page:/todos` POINTER ("show me my todos") on the reachability ratchet. Ceiling:
  558 → 548 (−10). **Sibling-takeover finding, named not hidden**: post-deletion census measured
  110 → 100 (not 110 → 99) — "what should I do next" is now claimed DIRECTLY by
  `PRIORITY_PATTERNS` (a pre-existing, previously-shadowed duplicate literal since commit
  `33f3a43ad42`, 2026-03-22 — verified via `git blame`, not new), landing on the SAME
  `get_top_priority` destination the rescore ruling established. Documented as a
  `known_reabsorptions` ledger exception (phrase + reclaiming list + agreement check), not
  silently folded into the "exactly 11" expectation. No other sibling reabsorbed any of the
  other 10 phrases. Every broken surface-1 pin converted (never deleted), 8 test files: `test_
  reminder_query_preclassifier_1521.py`, `test_todo_completion_lifecycle.py`, `test_todo_query_
  handlers.py`, `test_todo_listing_declines_write_asks_1881.py`, `test_task_clarify_1654.py`,
  `test_ftux_interview_1688.py` (both swapped to "give me my standup" per the first deletion's
  own idiom), `test_inversion_split_stand_down_1896.py`, `test_inversion_multi_intent_unit4_
  1595.py` (10 tests — turns collapsed onto the still-splitting GITHUB_QUERY_PATTERNS +
  SESSION_ACTIVITY_QUERY_PATTERNS pairing; the consult stub remaps a segment's dispatched action
  regardless of what surface 1 originally claimed for it, so `list_todos_query`/`delete_todo`
  are still reachable for real dispatch without ever needing a live GitHub call). No new #1899
  gap found (unlike the first deletion, which discovered #1899 itself) — the reads-only release
  already covers these phrasings for both carriers, exercised directly
  (`test_reminder_query_preclassifier_1521.py::test_todo_listing_unchanged`,
  `test_todo_query_handlers.py::TestPreClassifierRoutingIntegration`). Full suite green:
  `tests/unit/services/intent_service/` + `tests/unit/services/intent/` 4957 passed;
  `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py`
  82 passed/1 xfailed (ceiling exact at 548); `scripts/run-sweep.sh ratchets` 73 passed/1 xfailed
  + mypy gate at ceiling (unchanged, 24 codes). `ruff format`+`ruff check --fix` clean. Doc
  updated: `intent-routing-stack.md` gains a "Second deletion" subsection under Phase 3. Next:
  GUIDANCE_PATTERNS (20 deposits already landed, unscored) is the next GO-eligible candidate
  once the Lead's budgeted shadow-score run judges those rows.

- 2026-09-30 (prog, Sonnet): PRIORITY_PATTERNS deposits — 38 of 43 unexercised literals (47
  total, 4 already claimed) get one HAND_ROWS entry each, `expected: action:get_top_priority`
  throughout (PRIORITY_PATTERNS has exactly one destination; this exact expectation already
  scored MATCH once, in the TODO_QUERY re-expected "what should I do next" row). 5 literals
  are structurally UNREACHABLE at surface 1 — always shadowed by an earlier sibling literal in
  the SAME list (confirmed empirically, several phrasings each): `\bwhat are my priorities\b`
  (always contains "my priorities", claimed first by `\bmy priorities\b`); `\bmost important
  task\b` / `\bmost important work\b` / `\bwhat'?s most important\b` (all always contain "most
  important", claimed first by `\bmost important\b`); `\bwhat.*work on next\b` (always
  contains "work on next", which also satisfies the `(?:do|work on|tackle|handle)\s+next`
  alternation in an earlier literal). No deposit for these 5 — reported as findings, not filed
  as separate issues (same convention as prior deposit sessions). Corpus 151→189 (+38), purely
  additive (`git diff --stat` the yaml: 159 insertions, 0 deletions). Pinned total in
  `test_inversion_phase3_deletion_1595.py` updated 151→189 (claimed 100→138, unclaimed
  unchanged at 51). Gate re-run: PRIORITY_PATTERNS 42/47 literals claimed (4 pre-existing + 38
  new), 0 "needs a corpus row" lines (was 43). Rows score UNSCORED (not-live) as expected — out
  of scope for this unit. `ruff format`/`ruff check --fix` clean;
  `test_inversion_phase3_deletion_1595.py` 19 passed; `test_preclaim_shadow.py` 29 passed;
  `test_architecture_enforcement.py` 62 passed/1 xfailed with one pre-existing, UNRELATED
  failure deselected (`TestInversionShadowNoExecutionBoundary::
  test_only_the_shadow_observer_may_import_the_router` — a concurrent, uncommitted change to
  `services/domain/llm_domain_service.py` present in this shared worktree before this unit
  started, part of a different in-flight Phase-2-flip lane, not touched by this deposit);
  extraction ceiling confirmed unchanged at 548 via direct `pattern_literal_counts.
  total_literal_count()` call and the `ExtractionPatternRatchet` test in isolation (3 passed).
  Next: PRIORITY_PATTERNS is now GO-eligible pending the Lead's budgeted shadow-score run,
  alongside GUIDANCE_PATTERNS.

- 2026-09-30 (prog, Sonnet): CALENDAR_QUERY_PATTERNS deposits — 46 of 49 unexercised literals
  (52 total, 3 already claimed) get one HAND_ROWS entry each. Unlike PRIORITY_PATTERNS, this
  list has THREE live-routable destinations (`meeting_time`/`recurring_meetings`/
  `week_calendar`, all `ActionDisposition.WORKFLOW`, all in flip group `read_temporal`); each
  row's `expected: action:<name>` is the action that exact phrase actually routes to, read
  directly off `intent.action` from `PreClassifier.pre_classify_with_pattern_list(phrase)` —
  several rows demonstrate the claiming literal (from `CALENDAR_QUERY_PATTERNS`, list order)
  and the action-determining match (a SEPARATE re-check of the message against two hardcoded
  sub-lists inside the branch) are independent: "what's my agenda this week" is claimed by
  `\bagenda.*this week\b` but gets `meeting_time` because the same string also contains "my
  agenda". 3 literals are structurally UNREACHABLE at surface 1 (confirmed empirically, 2
  phrasings each): `\bon my agenda\b` (always contains "my agenda", claimed first by
  `\bmy agenda\b`); `\bwhat'?s on my calendar.*tomorrow\b` (always contains "what's on my
  calendar", claimed first by that literal, list position 0); `\bmy calendar tomorrow\b`
  (always contains "calendar" immediately followed by "tomorrow", claimed first by
  `\bcalendar.*tomorrow\b`). No deposit for these 3 — reported as findings. Corpus 189→235
  (+46), purely additive (`git diff --stat` the yaml: 191 insertions, 0 deletions). Pinned
  total in `test_inversion_phase3_deletion_1595.py` updated 189→235 (claimed 138→184,
  unclaimed unchanged at 51). Gate re-run: CALENDAR_QUERY_PATTERNS 49/52 literals claimed (3
  pre-existing + 46 new), verdict stays GO (deletable) — all 46 new UNSCORED rows mark `[OK]`
  via "expected action live via group" (unlike PRIORITY's FLOOR disposition, which flips the
  list to NO-GO on UNSCORED rows and suppresses the missing-literals section entirely). Because
  verdict stays GO here, the gate's "needs a corpus row before deletion" section does NOT
  suppress, so it correctly still lists the 3 structurally-unreachable literals by name — this
  is accurate gate behavior, not a gap in this unit's coverage (those 3 can never be converted;
  no phrase can make them win against their shadowing sibling). `ruff format`/`ruff check --fix`
  clean; `test_inversion_phase3_deletion_1595.py` 19 passed; `test_preclaim_shadow.py` 29
  passed; `test_architecture_enforcement.py` 63 passed/1 xfailed, clean (the concurrent
  `llm_domain_service.py` failure the PRIORITY lane flagged has since cleared); extraction
  ceiling confirmed unchanged at 548. Next: CALENDAR_QUERY_PATTERNS is now GO-eligible pending
  the Lead's budgeted shadow-score run, alongside PRIORITY_PATTERNS and GUIDANCE_PATTERNS.

- 2026-09-30 (prog, Sonnet): TEMPORAL_PATTERNS deposits — 48 of 54 unexercised literals (56
  total, 2 already claimed — the second claimed row, "when is my next meeting?", actually
  claims via the earlier sibling `\bnext meeting\b`, NOT `\bwhen is my.{0,10}meeting\b` as its
  wording suggests, confirmed via `_first_pattern_match`; that longer literal was still
  unexercised and got its own row below) get one HAND_ROWS entry each. Unlike
  CALENDAR_QUERY_PATTERNS, this list has exactly ONE destination (`get_current_time`, no
  action-determining sub-branch), so every row's `expected` is `action:get_current_time`
  throughout. 6 literals are structurally UNREACHABLE at surface 1 (confirmed empirically, 2
  phrasings each) — a NEW shadow shape not seen in PRIORITY/CALENDAR: 4 are shadowed by a
  DIFFERENT, earlier-checked list (`CALENDAR_QUERY_PATTERNS`, checked before TEMPORAL_PATTERNS
  in `pre_classify_with_pattern_list`), not merely an earlier sibling in TEMPORAL_PATTERNS
  itself — `\bwhat'?s on my calendar\b` and `\btomorrow'?s schedule\b` (CALENDAR_QUERY_PATTERNS
  has the identical literal), `\bwhat'?s.{0,10}tomorrow\b` (CALENDAR's broader unbounded
  `\bwhat'?s.*tomorrow\b` always wins first), `\bmeetings this week\b` (CALENDAR's broader
  `\bmeetings.*this week\b` always wins first). 2 are the familiar within-list shadow:
  `\bwhat'?s on my schedule\b` (always contains "my schedule", claimed first by `\bmy
  schedule\b`) and `\bhow long.*been working\b` (always contains "working", claimed first by
  `\bhow long.*working\b`). No deposit for these 6 — reported as findings. Corpus 235→283 (+48),
  purely additive. Pinned total in `test_inversion_phase3_deletion_1595.py` updated 235→283
  (claimed 184→232, unclaimed unchanged at 51). Gate re-run: TEMPORAL_PATTERNS 50/56 literals
  claimed (2 pre-existing + 48 new), **verdict NO-GO** (unlike CALENDAR_QUERY_PATTERNS's GO) —
  `get_current_time` is `ActionDisposition.CANONICAL` (floor-routed), with no WORKFLOW entry
  (so no flip_group) and no router-grammar operation (so no category match either), meaning none
  of the gate's three live-naming surfaces (operation/canonical, flip_group, category) can mark
  it live under any `--live` token; every new row reads `[FAIL] ... UNSCORED; not-live`. Same
  disposition shape as PRIORITY_PATTERNS's NO-GO (both are floor/CANONICAL actions), not
  CALENDAR_QUERY_PATTERNS's GO (three WORKFLOW actions sharing flip_group `read_temporal`). NO-GO
  suppresses the "needs a corpus row" section, so the gate's TEMPORAL output after this deposit
  shows 0 such lines even though 6 literals remain permanently unreachable — consistent with the
  PRIORITY lane's prior finding that NO-GO suppression is a side effect of FLOOR disposition, not
  evidence those 6 got rows. `ruff format`/`ruff check --fix` clean; `test_inversion_phase3_
  deletion_1595.py` 19 passed; `test_preclaim_shadow.py` 29 passed; `test_architecture_
  enforcement.py` 63 passed/1 xfailed, clean; extraction ceiling confirmed unchanged at 548 (both
  via direct `pattern_literal_counts.total_literal_count()` and the ExtractionPatternRatchet
  test in isolation, 3 passed). `inversion_phase1_shadow_score.py --dry-run` and `inversion_
  phase2_gate.py --dry` both exit 0, both self-report no LLM calls; the dry-run's pre-existing
  TEMPORAL shared-subset cross-validation REGRESSION note (`what's on my calendar today?`) is
  the same pre-existing note the CALENDAR lane flagged — unaffected by this unit (the 48 new
  rows are UNSCORED, outside that cross-check's "shared" subset). Next: TEMPORAL_PATTERNS stays
  NO-GO regardless of corpus coverage until either (a) the Lead's budgeted shadow-score run
  scores these UNSCORED rows AGREE/MATCH, or (b) `get_current_time` gains a WORKFLOW flip_group
  entry — a disposition question for the Lead, not something a corpus deposit can resolve.

- 2026-10-01 (prog, Sonnet, dispatched by Lead): **Unit 5 THIRD DELETION LANDED**:
  `CALENDAR_QUERY_PATTERNS` (52 literals) emptied to `[]` in `pre_classifier.py` — the FIRST
  live-list deletion of this epic (`get_current_time` gained a `read_temporal` rail entry the
  same day, per Arch's ruling, so the gate's `--live` set now covers it honestly). Gate re-run
  BEFORE deletion: GO, 49/49 claimed rows MATCH/agreeing-REVIEW/live-MISMATCH, 0
  needs-a-corpus-row (the 3 structurally-shadowed literals from the 09-30 deposits lane remain
  unexercised, documented in the ledger's `shadowed_literals`, not a blocker). Verdict of record:
  the served-model (Haiku) baseline + the CALENDAR-specific rescores +
  CXO's 10-01 ruling that the 5 no-feature capability-gap rows (conflict-check, find-time,
  booking) honestly floor rather than claim a week dump as an answer. Tombstone form matches the
  prior two deletions; the inline meeting_time/recurring_meetings/week_calendar sub-lists in
  `pre_classify` and the `_get_calendar_action` helper `detect_multiple_intents` uses both survive
  as documented dead code (structurally unreachable, never deleted).

  **Sibling-takeover finding, an order of magnitude bigger than the second deletion's one row**:
  post-deletion census shows TEMPORAL_PATTERNS reabsorbing **19 of the 49** claimed phrases — ALL
  DISAGREEING (claimed as `get_current_time`, never the ruled meeting_time/week_calendar/
  recurring_meetings/floor destination). Reported in full under the ledger's `known_reabsorptions`
  (each entry carries `"agrees": false` + a note), never silenced via the agreeing-only mechanism
  the second deletion's precedent established. This is sound in production because
  `consult_inversion_live` runs BEFORE this surface-1 fallback and already proves each of these 49
  rows safe (the live flag carries `read_temporal`); the TEMPORAL reclaim only bites when the live
  consult stands down (unflipped deployment, armed turn, sub-threshold confidence, REFUSED,
  transport error) — a pre-existing, orthogonal fallback-quality question this deletion did not
  introduce, flagged for CXO/Arch to decide whether TEMPORAL_PATTERNS' calendar-vocabulary overlap
  needs narrowing.

  **Mechanism gap found and fixed, same commit**: `check_deleted_entry_non_regression` never had a
  live-flag-aware (condition-c) escape for EITHER the unclaimed-but-MISMATCH-live case or a
  documented-but-disagreeing reclaim — it only ever checked MATCH/agreeing-REVIEW, because no
  earlier ledger entry needed more. CALENDAR's entry exposed both gaps (3 rows: 1 unclaimed, 2
  reclaimed) in the same run. Fixed by unifying both code paths onto a single re-derivation of
  `row_disposition` (the SAME MATCH/agreeing-REVIEW/live-MISMATCH proof `build_census` used at
  gate time), fed a synthetic claim carrying the phrase's resolved target op
  (`expected_op_for_phrase`) instead of the (possibly wrong) surviving pattern's own claim; added a
  `cats: Optional[frozenset]` parameter threaded from callers (omitted/`None` reproduces every
  earlier entry's behavior byte-for-byte — none of them ever needed a live condition).
  `known_reabsorptions` gained an `"agrees"` field (defaults true/omitted = the original agreeing
  shape unchanged) so a documented DISAGREEING reclaim can still pass non-regression when the
  phrase's own frozen router evidence independently holds — an undocumented reclaim still fails
  loud unconditionally, since the SURPRISE itself (not just eventual safety) is what the check
  exists to catch. 7 new synthetic tests in `test_inversion_phase3_deletion_1595.py` pin the
  mechanism in isolation (floor-row handling, documented-agreeing, documented-disagreeing+safe,
  undocumented-reclaim-still-fails, cats-required-for-MISMATCH-live) plus 2 ledger-specific tests
  (`test_calendar_entry_fails_non_regression_without_the_live_flag`,
  `test_calendar_entry_known_reabsorptions_are_all_documented_disagreements`).

  Ceiling: 548 → 496 (−52). Every broken surface-1 pin converted (never deleted), across 7 test
  files: `test_calendar_query_handlers.py` (`TestPreClassifierRoutingIntegration`, converted to
  the decline+inversion-routes idiom, plus a new `test_meeting_time_variants_reabsorbed_by_temporal`
  pinning 2 test-local TEMPORAL-reabsorption casualties outside the 49 corpus rows),
  `test_action_registry.py` (`test_example_messages_classify_correctly` gains a documented
  skip-list for one ACTION_EXAMPLES doc string that's now a TEMPORAL-reabsorption casualty;
  `test_calendar_check_does_not_produce_temporal` rewritten — the #919 premise it pinned
  (calendar-conflict-check should be QUERY) is SUPERSEDED by the CXO floor ruling, so it now pins
  the new reality: no QUERY claim, a documented TEMPORAL reabsorption), `test_keyword_
  disambiguation_901.py` (`TestKeywordDisambiguationQ33`/`Q62` — the SAME #901-premise
  supersession, 7 tests rewritten to assert decline or documented reabsorption instead of QUERY),
  `test_greeting_pleasantry_only_1416.py` (one test converted to a stronger form of its own
  contract — the compound message now declines entirely rather than merely avoiding the
  "greeting" mislabel), `test_preclaim_shadow.py` (2 tests swapped from the "greeting + calendar"
  pairing to "greeting + analysis", same idiom as the first two deletions' "give me my standup"
  swaps). Full suite green: `tests/unit/services/intent_service/` + `tests/unit/services/intent/`
  4995 passed (0 regressions after conversion — baseline was 4995 passed/18 converted, all now
  pass); `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_
  1595.py` ceiling exact at 496, reachability ratchet confirmed (no CALENDAR POINTER row exists,
  verified by grep — the ledger's `phase3-deletion-ledger` resolver is never exercised for this
  entry, harmlessly). `ruff format`/`ruff check --fix` clean. Doc updated: `intent-routing-
  stack.md` gains a "Third deletion (the first live list)" subsection under Phase 3. Next: no
  further Phase-3 deletion is GO-eligible without a fresh gate run — GUIDANCE_PATTERNS/
  PRIORITY_PATTERNS/TEMPORAL_PATTERNS' prior NO-GO/unscored status may have changed under the
  10-01 Haiku baseline + rulings; re-run `--all` before picking the next one.
- 2026-10-01 08:5x — **Unit 5 FOURTH DELETION LANDED**: `TEMPORAL_PATTERNS` (56 literals) emptied
  to `[]` in `pre_classifier.py` (tombstoned — class attribute + 4 consumer code paths, incl. the
  now-structurally-inert `_temporal_disjoint_from_connect`, survive). Gated on two same-day
  prerequisites: the per-row sort of the 48 TEMPORAL deposit rows (Arch's ruling, resolving the
  pattern's own ALL-temporal over-claim into per-row destinations) and the `get_current_time_entry`
  READ rail entry (flip_group `read_temporal`), both landed earlier the same day. Gate: GO, 69/69
  claimed rows (50 own + 19 ex-CALENDAR reabsorptions), 4 "needs a corpus row" (2 shadowed by an
  earlier sibling literal, 2 genuinely unused vocabulary, neither a blocker). Ceiling: 496 → 440
  (−56). **New gate rule**: `row_disposition` gained a "mis-serves this row" branch (5 of the 50
  own rows pass this way — the router declined AND the pattern's own claim disagreed with the ruled
  destination, so deletion can only improve a deterministically-wrong fallback) — ledgered under a
  new `misserved_at_deletion` field. The 19 ex-CALENDAR reabsorptions are now RESOLVED
  (`CALENDAR_QUERY_PATTERNS`' `known_reabsorptions` entries gained `"resolved_by"`; empirically
  re-confirmed all 69 phrases genuinely unclaimed post-deletion, zero new reabsorptions). Mechanism
  additions: `misserved_at_deletion`'s non-regression escape (the mis-serve proof can't be
  re-derived from the synthetic correct-op claim, so the re-verified invariant is narrower — stays
  UNCLAIMED); `gate.CURRENT_LIVE_CATEGORIES`, a shared constant for the `--live` set every
  Phase-3 run has used, needed when the reachability ratchet's `page:/settings/preferences` POINTER
  (resolved via TEMPORAL's ledger entry, which now carries a MISMATCH-but-live-route row) failed
  non-regression under the old `cats=None` call — the POINTER's utterance also swapped from "what
  time is it for me?" (never a corpus row) to "what time is it?" (already ledgered, MATCH@0.99) to
  avoid depositing an UNSCORED row. 12 test files converted (largest conversion count of the four
  deletions): `test_action_registry.py`, `test_calendar_query_handlers.py` (renamed its own
  third-deletion reabsorption pin to reflect resolution), `test_integration_connect_
  preclassifier_1417.py`, `test_keyword_disambiguation_901.py`, `test_reminder_query_
  preclassifier_1521.py` (decline+inversion-routes idiom), `test_inversion_split_stand_down_1896.py`
  (SPLIT_TURN swapped a second time), `test_multi_intent_connect_1505.py` +
  `test_multi_intent_temporal_span_1755.py` (the entire #1755 span-aware-suppression file rewritten
  — the mechanism it pins is now permanently inert), `test_original_message_1460.py` (new
  still-claiming constant for one parametrize case), `test_read_lane_destructive_greed_1756.py`
  (largest single conversion: 17 phrases moved out of KEEP_CLAIMING into a new decline-pinning
  class), `test_spend_free_canonical_ratchet_1818.py` (`("TEMPORAL", "get_current_time")` REMOVED,
  not swapped — **discovered work, not resolved here**: a direct keyless probe confirms the pair no
  longer has a zero-LLM-touch path, but the #1818 chokepoint's instrumentation can't currently
  measure the specific failure mode it now hits, container-resolution before the spend-key gate —
  flagged in the test file's own NOTE for Lead/Arch/CXO, the gate's owners). Full suite:
  `tests/unit/services/intent_service/` + `tests/unit/services/intent/` 5020 passed;
  `tests/test_architecture_enforcement.py` + `tests/unit/test_inversion_phase3_deletion_1595.py` 98
  passed/1 xfailed, ceiling exact at 440; `scripts/run-sweep.sh ratchets` 73 passed/1 xfailed + mypy
  gate unchanged. `ruff format`/`ruff check --fix` clean. No LLM calls anywhere in this unit. Doc:
  `intent-routing-stack.md` gains a "Fourth deletion" subsection. Next: `GUIDANCE_PATTERNS` and
  `PRIORITY_PATTERNS` remain the only scored-but-not-yet-deleted lists per the 10-01 rulings — a
  fresh gate run is still the required first step for either, per the standing note above.

- 2026-10-01 (prog, Sonnet, dispatched by Lead): **GITHUB_QUERY_PATTERNS deposits** — all 53 of
  53 unexercised literals (64 total, 11 already exercised) get one HAND_ROWS entry each; unlike
  every prior deposit lane, **0 literals were structurally unreachable** (only 5 of 53 candidate
  phrases needed a reword, all fixed on the first retry). `expected` is `action:<name>` read
  directly off `PreClassifier.pre_classify_with_pattern_list(phrase).action`, never hand-traced:
  shipped_query (3 rows), stale_prs_query (3), close_issue_query (2, category EXECUTION, matching
  the pre-existing close/reopen/comment rows' own category convention), reopen_issue_query (3,
  EXECUTION), comment_issue_query (3, EXECUTION), list_issues_query (5), list_prs_query (8),
  review_issue_query (26 — 3 single-issue-detail literals + **all 23 milestone/release/label/
  branch literals**). **Significant finding, reported not fixed**: those 23
  milestone/release/label/branch literals all claim via GITHUB_QUERY_PATTERNS but their action
  comes out `review_issue_query` — the SAME action as "show me issue #42" — because the branch's
  action-determination if/elif in `pre_classify_with_pattern_list`
  (`services/intent_service/pre_classifier.py` ~1532-1620) has no case for milestones/releases/
  labels/branches; everything not shipped/stale/close/reopen/comment/list_issues/list_prs falls
  into the trailing `else`. This is despite `list_milestones_query`/`list_releases_query`/
  `list_labels_query`/`list_branches_query` being fully registered WORKFLOW actions with their own
  handlers and `read_status` flip groups in `workflow_entries.py` — those four handlers are
  structurally unreachable from this branch, confirmed empirically for all 23 literals (not
  inferred). The pre-existing "show milestones" FAIL row already showed this exact disagreement at
  one data point (claim=review_issue_query, router=list_milestones@1.0); this deposit shows the
  disagreement's full scope. Flagged for the Lead/Arch — not corrected here (a ruling, not a
  deposit). Two PRE-EXISTING [FAIL] rows ("show issue #123", "show milestones", both
  REVIEW-disagreements) were left untouched per the same reasoning. Corpus 283→336 (+53), purely
  additive (`git diff --stat`: 212 insertions/0 deletions on the yaml, 394/0 on the builder).
  Pinned total in `test_inversion_phase3_deletion_1595.py` updated 283→336 (claimed 133→186,
  unclaimed unchanged at 150 — confirmed by direct `gate.build_census()` call). Gate re-run:
  GITHUB_QUERY_PATTERNS 66/336 rows claimed (13 pre-existing + 53 new), **verdict stays NO-GO**.
  **Mechanism note, not a defect**: the gate's UNSCORED-row rule was tightened the same day (Lead,
  `row_disposition`'s "2026-10-01: an unscored row is a row we know nothing about... Never OK" —
  the old "UNSCORED but expected action live via group" shortcut CALENDAR's deposits relied on is
  gone), so all 53 new rows read `[FAIL] UNSCORED; UNSCORED — score it (one router call); no
  verdict, no GO` regardless of their flip group — this is now uniform across every Phase-3
  deposit, not specific to this list. NO-GO suppresses the "needs a corpus row" section (same
  precedent as PRIORITY/TEMPORAL). `ruff format`/`ruff check --fix` clean;
  `test_inversion_phase3_deletion_1595.py` 35 passed; `test_preclaim_shadow.py` 29 passed;
  `test_architecture_enforcement.py` 63 passed/1 xfailed, ceiling confirmed unchanged at 440. Next:
  GITHUB_QUERY_PATTERNS needs (a) the Lead's budgeted shadow-score run on these 53 rows, AND (b) a
  ruling on the milestone/release/label/branch action-determination gap, before it can be
  GO-eligible — alongside GUIDANCE_PATTERNS and PRIORITY_PATTERNS, which remain the only other
  scored-but-not-yet-deleted lists per the 10-01 rulings.

- 2026-10-01 (prog, Sonnet, dispatched by Lead): **STATUS_PATTERNS deposits** — 46 of 51
  unexercised literals (56 total, 5 already exercised) get one HAND_ROWS entry each. 5 literals
  are structurally UNREACHABLE — more severe than GITHUB's shadow finding, since 4 are
  byte-identical regex duplicates of literals in OTHER, earlier-checked lists (`\bnext
  milestone\b` duplicates GITHUB_QUERY_PATTERNS' own literal, checked earlier in the if-chain;
  `\bwhat'?s the (?:next|upcoming) milestone\b`/`\bmilestone status\b`/`\bmilestone progress\b`
  duplicate the inline `MILESTONE_STATUS_INLINE_PATTERNS` list, checked even earlier) — so no
  phrasing can ever reach them, proven mathematically not just empirically. The 5th
  (`\bmy current work\b`) is shadowed WITHIN STATUS_PATTERNS by its own shorter sibling
  `\bcurrent work\b`, which is a guaranteed substring. **Significant finding #1**: unlike
  GITHUB's partial if/elif branching, STATUS_PATTERNS' claim branch
  (`pre_classify_with_pattern_list` ~1807-1816) has NO branching at all — every one of its 56
  literals returns the single hardcoded `get_project_status`, and that action has NO
  WorkflowEntry/flip_group anywhere (grep-confirmed) and STATUS is absent from
  `canonical_handlers.py`'s `canonical_categories` set, whose own docstring states "STATUS/
  PRIORITY removed Apr 13 (#925) — floor-routed via Action Gate." Every STATUS_PATTERNS claim is
  therefore floor-routed in production regardless of which literal fired — flagged for the
  Lead/Arch, not resolved here. **Corrections applied** (per dispatch instruction, mirroring
  GITHUB's later correction): 8 of 46 rows have `expected` corrected away from the uniform
  `action:get_project_status`, each with a DIRECT in-corpus or in-code anchor (not speculation) —
  6 standup literals → `action:show_standup` (anchor: the pre-existing MATCH-scored "give me my
  standup" row, same list); `\bmy portfolio\b` + `\blist.*projects\b` → `action:manage_portfolio`
  (anchor: the pre-existing MATCH-scored "what are my projects?" row for the sibling `\bmy
  projects\b` literal, corroborated by pre_classifier.py's own #1738/#1884 comments naming these
  exact two literals as documented PORTFOLIO collisions). The remaining 38 rows (including the
  one reachable milestone survivor, `\bupcoming milestones?\b` — deliberate design per Issue #898
  Q25, not a gap) keep `action:get_project_status` uncorrected; no comparably direct anchor
  exists for the status/progress/tasks/assignments/work vocabulary. 12 of 46 phrases needed a
  reword (shorter "my X" siblings shadowing broader "show/list/how's/what's.*X" ones, one
  cross-list shadow by `PORTFOLIO_LIST_PATTERN`/PORTFOLIO_PATTERNS for "list my projects" — fixed
  by rewording to "list my active projects for this quarter"). Two PRE-EXISTING [FAIL] rows
  ("what am I working on?", "show me my archived projects") left untouched. Corpus 336→382
  (+46), purely additive (`git diff --stat`: 195 insertions/0 deletions on the yaml, 435/0 on the
  builder). Pinned total in `test_inversion_phase3_deletion_1595.py` updated 336→382 (claimed
  186→232, unclaimed unchanged at 150 — confirmed by direct `gate.build_census()` call). Gate
  re-run: STATUS_PATTERNS 51/382 rows claimed (5 pre-existing + 46 new), **verdict stays NO-GO**
  (2 pre-existing FAIL rows + all 46 new rows UNSCORED per the same 10-01 gate tightening GITHUB's
  lane found — uniform across Phase-3 now, not specific to this list). NO-GO suppresses the
  "needs a corpus row" section. `ruff format`/`ruff check --fix` clean;
  `test_inversion_phase3_deletion_1595.py` 35 passed; `test_preclaim_shadow.py` 29 passed;
  `test_architecture_enforcement.py` 63 passed/1 xfailed, ceiling confirmed unchanged at 440.
  Next: STATUS_PATTERNS needs (a) the Lead's budgeted shadow-score run on these 46 rows, AND (b) a
  ruling on whether `get_project_status`'s floor-routing (no flip_group, not canonical-handled)
  can ever read as [OK] under the gate's live-match mechanism, before it can be GO-eligible —
  alongside GUIDANCE_PATTERNS and PRIORITY_PATTERNS, which remain the only other
  scored-but-not-yet-deleted lists per the 10-01 rulings.

- 2026-10-02 (prog, Sonnet, dispatched by Lead): **GITHUB_QUERY_PATTERNS deletion — #1595 Phase 3
  fifth deletion.** BEFORE gate (`--list GITHUB_QUERY_PATTERNS --live read_status,read_referent,
  read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo`): GO, 64
  literals, 66/66 claimed rows (66 [OK], 0 [FAIL]), 0 needs-a-corpus-row (every literal exercised).
  Emptied `GITHUB_QUERY_PATTERNS = []` (tombstone form, dated comment block); the claim branch
  (action sub-cases + `_github_read_claim_blocked`), `_get_github_action`, `_GITHUB_GATED_RAIL_
  ACTIONS`, `detect_multiple_intents`'s table entry, and the GITHUB-subsumes-STATUS subsumption
  filter all survive as documented dead code. Post-deletion reabsorption check (empirical
  `claim_for_phrase` over all 66 phrases): **1 reabsorption**, AGREEING — "any update on the next
  milestone" reclaimed by `STATUS_PATTERNS`'s own pre-existing `\bnext milestone\b` literal (git
  blame: predates this deletion by months), claim `get_project_status`, byte-identical to the
  ruled destination. The other 65 genuinely unclaimed. AFTER gate (`--all`): `GITHUB_QUERY_
  PATTERNS 0 0 NO ROWS`; corpus denominator 382 = 167 claimed + 215 unclaimed (232→167 = -65 = -66
  +1 reabsorbed; STATUS_PATTERNS's own claimed count rose 51→52 in the same run). Ledger: 6th
  `DELETED_PATTERN_LISTS` entry appended to `scripts/inversion_phase3_deleted_patterns.json`,
  built programmatically from the gate's own `build_census`/`claim_for_phrase`/`row_disposition`
  (no hand transcription). Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]`
  440 → 376 (confirmed: `pattern_literal_counts.total_literal_count()` = 376).

  **Test conversion — the broadest of the five deletions**: 124 failures across 19 files on the
  first full targeted run (`tests/unit/services/intent_service/` + ledger + enforcement +
  `test_pre_classifier.py`, no `-x`). GITHUB_QUERY_PATTERNS' vocabulary (issues/PRs/milestones/
  releases/labels/branches/shipped/stale + the close/reopen/comment destructive-rail actions) was
  the most heavily depended-on by OTHER tests' end-to-end arm steps of any deletion to date — 8
  separate `#1190`/`#1650`/`#1509`/`#1641`/`#1648`/`#1571`/`#1627`/`#1630` end-to-end confirm-gate
  files armed via a bare `process_intent(message="close issue #108", ...)` against an
  EXPLOSIVE-LLM fixture, relying on this list's zero-LLM determinism for free; all converted via
  an inline/shared `classify()` stub keyed to the exact arm message, preserving every later
  assertion unchanged (close_issue_query/reopen_issue_query/comment_issue_query have NO
  registered flip_group — confirmed empirically — so unlike `get_current_time` there is genuinely
  no zero-LLM path left for them; flagged to Arch/CXO, not resolved). `test_inversion_multi_
  intent_unit4_1595.py` was the hardest single conversion: its core split-turn pairing collapsed
  from 2 intents to 1 when GITHUB died; swapped to `LOCAL_GIT_STATUS_PATTERNS`'s "what branch are
  we on" with one test needing a DIFFERENT swap (`STATUS_PATTERNS`'s "give me my standup") because
  `LOCAL_GIT_STATUS_PATTERNS` isn't a `_READ_LANE_GROUPS` member and doesn't get the
  destructive-ask suppression the swapped-out test needed. **Two discovered-work findings, NOT
  caused by this deletion, left for the Lead/Arch**: (1) `tests/unit/services/test_pre_classifier.
  py::test_current_time_still_routes_to_temporal` — root cause is the FOURTH deletion
  (TEMPORAL_PATTERNS, commit `dfec3e908d`), outside that commit's own verified test-directory
  scope; converted anyway. (2) `test_reminder_clear_pick_target_1906.py`'s #1899 off-intent
  discriminator (`reminder_clear.py` ~1481) genuinely can no longer release on "close issue #108"
  (confirmed empirically: it now re-asks instead) — a live PRODUCT gap, not a test artifact;
  converted the TEST to a different example ("give me my standup") without touching product code,
  per this dispatch's explicit STOP condition. Also found, OUT OF SCOPE and NOT converted:
  `tests/e2e/test_1897_two_part_turn_live.py::test_shape_is_the_1897_shape_before_spending` is
  ALSO already broken by the fourth deletion (confirmed present and broken at `HEAD` before this
  session) — no phrase swap can fix it (no surviving surface-1 list can ever produce
  `get_current_time` again), a genuine test-design question, reported not guessed at.

  Full suite after conversion: `tests/unit/services/intent_service/` + ledger + enforcement +
  `test_pre_classifier.py` — **5127 passed, 1 xfailed, 0 failed** (full run). `scripts/run-sweep.sh
  ratchets` found 1 PRE-EXISTING unrelated failure (`test_todo_marker_ratchet`, count 36 vs frozen
  ceiling 35) — confirmed via independent re-computation that zero of the 36 hits are in any file
  this unit touched and the scan never looks at `tests/` at all; flagged, not fixed (out of
  scope). `ruff format`/`ruff check --fix` clean (5 files reformatted, whitespace only). A later
  re-run of the full suite hit one additional flaky failure,
  `test_inversion_router_1595.py::TestRouteEnforcement::test_real_call_routes_within_grammar` —
  this test makes a REAL live LLM call by its own docstring/design ("One real Haiku-class call"),
  passed cleanly in isolation on re-run, and is unrelated to any file this unit touched. No LLM
  calls anywhere in THIS unit's own work — every router verdict consulted is a frozen,
  already-scored report or a monkeypatched stub in tests.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Fifth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, reabsorption detail, all 19 converted test files with
  per-file rationale, both discovered-work findings, ceiling arithmetic). Next: GUIDANCE_PATTERNS
  and PRIORITY_PATTERNS remain the only scored-but-not-yet-deleted lists per the 10-01 rulings.

- 2026-10-02 (prog, Sonnet, dispatched by Lead): **PRIORITY_PATTERNS deletion — #1595 Phase 3
  sixth deletion.** BEFORE gate (`--list PRIORITY_PATTERNS --live read_status,read_referent,
  read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo`): GO, 47
  literals, 42/42 claimed rows (42 [OK], 0 [FAIL]), 5 literals flagged needs-a-corpus-row
  (2 shadowed by an earlier broader sibling literal, 3 genuinely never exercised). Destination:
  `get_top_priority`, a FLOOR-disposition action with NO WorkflowEntry. Emptied
  `PRIORITY_PATTERNS = []` (tombstone form, dated comment block); the claim branch and
  `detect_multiple_intents`'s table entry survive as documented dead code.

  **New condition (d), Arch's 2026-10-02 ruling**: 2 rows ("what are my focus areas this sprint",
  "what's my focus this week") license deletion via a frozen N=5 surface-2 probe
  (`inversion-phase3-surface2-floor-probe-2026-10-02-n5-anthropic.md`, served
  `anthropic:claude-sonnet-4-6`, 5/5 both phrases land in PRIORITY category) — the router
  MISMATCHED to a non-live op for both, but the destination is reached BY CATEGORY once surface 1
  is gone, so the pattern was never load-bearing. 2 further rows pass via the pre-existing
  `misserved_at_deletion` shape ("show priorities for this sprint", "not sure what to do about
  this" — claim disagreed with the ruling AND the router independently declined).
  `check_deleted_entry_non_regression` gained ONE new sibling branch, keyed by a new ledger field
  `surface2_verified_at_deletion`: OK iff the phrase is still UNCLAIMED post-deletion (same
  narrower invariant `misserved_at_deletion` already uses) — pinned with 2 new synthetic tests.

  Post-deletion reabsorption check (empirical `claim_for_phrase` over all 42 phrases): **ZERO
  reabsorptions** (STATUS_PATTERNS/GUIDANCE_PATTERNS/TODO_COMPLETE_PATTERNS/ANALYSIS_PATTERNS all
  specifically checked per the dispatch's watch-list — none reclaim). AFTER gate (`--all`):
  `PRIORITY_PATTERNS 0 0 NO ROWS`; corpus denominator 382 = 125 claimed + 257 unclaimed (167→125 =
  -42, the full claimed count, no partial reabsorption to net out). Ledger: 7th
  `DELETED_PATTERN_LISTS` entry appended, built programmatically from the gate's own
  `build_census`/`claim_for_phrase`/`row_disposition` (no hand transcription). Ceiling:
  `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 376 → 329 (confirmed:
  `pattern_literal_counts.total_literal_count()` = 329).

  **Test conversion, 6 files, 2 recurring fixture-breakage shapes**: (1) phrases/lists PRIORITY_
  PATTERNS itself used to be the "surviving claimer" or "still claimed" fixture for, now broken a
  SECOND or THIRD time in this epic (the same cascade CALENDAR→TEMPORAL and TEMPORAL→PRIORITY each
  caused before it) — `test_inversion_phase3_deletion_1595.py`'s three synthetic non-regression
  fixtures and `TestPriorityPatternsVerdictIsReported` (swapped to `REPO_MANAGEMENT_PATTERNS`,
  avoiding STATUS/GUIDANCE per the dispatch's own swap-avoidance rule — both are the next two lists
  scheduled for deletion; found a non-STATUS/GUIDANCE floor/plan-shaped replacement via a real
  `expected: "plan"` corpus row, SET_DEFAULT_REPO_PATTERNS' #1606 two-op row), and
  `test_inversion_split_stand_down_1896.py`'s `SPLIT_TURN` (THIRD swap of this fixture in the epic,
  now "give me my standup and what branch are we on"). (2) Direct `pre_classify` pins against
  `get_top_priority` with no WorkflowEntry to prove a routes-survive pin against —
  `test_contextual_query_handlers.py::test_priority_patterns_still_work` (5 phrases),
  `test_todo_query_handlers.py::test_next_todo_query_variants` (the SECOND deletion's own
  documented sibling-reabsorption finding, now moot since the reabsorbing list is itself gone),
  `test_pre_classifier.py::test_priority_next_patterns_not_greedy` (2 of 3 assertions) — all
  converted to pin the decline. `test_spend_free_canonical_ratchet_1818.py` — `("PRIORITY",
  "get_top_priority")` removed from `PAIR_MESSAGES` (same idiom as the fourth deletion's TEMPORAL
  removal; simpler case since this pair was already measured-`SPENDS`, never `SPEND_FREE`).

  Full suite: `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
  + ledger + `test_inversion_phase3_surface2_floor_1595.py` + enforcement + the #1897 spend-free
  shape pin — **FULL_RUN_RESULT_PLACEHOLDER** (full run, not a subset; ceiling exact at 329).
  `scripts/run-sweep.sh ratchets` — same 1 PRE-EXISTING unrelated failure as the fifth deletion
  found (`test_todo_marker_ratchet`, 36 vs 35), confirmed unrelated again. `ruff format`/`ruff
  check --fix` clean. No LLM calls anywhere in this unit — every router verdict consulted is a
  frozen, already-scored report (including both N=5 surface-2 probe reports), or a monkeypatched
  stub in tests.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Sixth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, condition-(d) detail, all 6 converted test files with
  per-file rationale, ceiling arithmetic). GUIDANCE_PATTERNS remains the last scored-but-not-yet-
  deleted list per the 10-01 rulings.

- 2026-10-02 (prog, Sonnet, dispatched by Lead): **STATUS_PATTERNS deletion — #1595 Phase 3
  seventh deletion, the FIRST PARTIAL one.** BEFORE gate (same `--live` token set as the sixth):
  GO (partial) — 4 load-bearing literals SURVIVE (`\bnext milestone\b`, `\bcurrent work\b`,
  `\bproject overview\b`, `\bproject landscape\b`), deleting the other 52: ceiling 329 → 277. 56
  literals, 52 claimed rows (48 [OK], 4 [FAIL] — exactly the 4 survivors, each a MATCH on a
  non-live op where a frozen N=5 surface-2 probe does NOT show the LLM classifier landing in
  STATUS on every sample). `STATUS_PATTERNS` is NOT emptied: it becomes exactly the 4 survivor
  literals, with a dated comment block recording the deletion; the claim branch stays LIVE (no
  dead-code tombstone — unlike every prior full deletion, the list still has real literals).

  **STOP, then unblocked same session**: the literal→corpus-row audit (computed by hand, since the
  gate only prints it on a full GO) found 4 of 56 literals unexercised by any STATUS-claimed row,
  all inside the 52-to-delete set. `\bmy current work\b` was provably shadowed WITHIN the list by
  the surviving `\bcurrent work\b`. The other 3 (`\bwhat'?s the (?:next|upcoming) milestone\b`,
  `\bmilestone status\b`, `\bmilestone progress\b`) looked genuinely reachable-but-untested under
  `PreClassifier._first_pattern_match` against `STATUS_PATTERNS` ALONE — the wrong instrument,
  since it only proves reachability WITHIN one list, not through the real if-chain. Per the
  dispatch's explicit STOP condition, the lane stopped and reported before touching any files. The
  Lead unblocked with `PreClassifier.pre_classify_with_pattern_list` (the real production
  if-chain): all three are claimed by the inline (non-class-attribute)
  `MILESTONE_STATUS_INLINE_PATTERNS` check (Issue #1068), checked BEFORE `STATUS_PATTERNS` — a
  fact the STATUS deposit lane had already found and documented the day before (`### STATUS_
  PATTERNS deposits...` subsection: "4 are byte-identical duplicates of GITHUB_QUERY_PATTERNS /
  MILESTONE_STATUS_INLINE_PATTERNS literals... 1 is shadowed by its own shorter sibling" —
  independently confirming the same 4 literals). No corpus deposits needed; all 4 recorded in the
  ledger's `shadowed_literals`. A pre-existing, now-stale note in `scripts/build_inversion_
  corpus_phase0.py`'s STATUS deposit block comment (calling `\bnext milestone\b` "structurally
  unreachable," true only before the fifth deletion emptied GITHUB_QUERY_PATTERNS' own shadowing
  copy) was corrected in the same commit — the yaml corpus regenerated via `python scripts/
  build_inversion_corpus_phase0.py` (385 rows unchanged, only two `notes` fields' text differs).

  Of the 48 [OK] rows: 18 via "expected action live via group," 4 via "MATCH (ruled floor),"
  9 via the mis-serve escape (6 PORTFOLIO-collision rows + 2 floor-ruled rows + 1 generate_report
  row), and 17 via the surface-2-floor shape (both provider legs, 10/10 combined, 14 phrases from
  a dedicated 40-row GUIDANCE/STATUS probe set plus 3 from the epic's original 9-phrase probe).

  Post-deletion reabsorption check (empirical `claim_for_phrase`, BOTH entry surfaces, over all 48
  deleted-literal rows): **ZERO reabsorptions**; all 4 survivor rows remain claimed by
  `STATUS_PATTERNS` itself. AFTER gate (`--all`): `STATUS_PATTERNS 4 4 NO-GO` (expected for a
  partial list — its remaining literals ARE its failing rows by construction); corpus denominator
  unchanged at 385 (77 claimed + 308 unclaimed; 125 → 77, −48, the full deleted-row count).
  `--list GUIDANCE_PATTERNS` re-checked: still GO (partial), same 3 survivors
  (`\bsetup.*projects?\b`, `\bset up.*projects?\b`, `\bset up.*portfolio\b`) — structurally
  unaffected by this deletion (GUIDANCE is checked before STATUS in the if-chain).

  Ledger: 8th `DELETED_PATTERN_LISTS` entry, with `"partial": true`, `"surviving_literals"` (the
  4-literal map), `"literals": 52` (the deleted count), and `surface2_verified_at_deletion` for
  all 17 surface-2-credited rows (probe report filenames + samples + served model, both legs).
  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 329 → 277. Ledger-count pin
  renamed to "...first eight deletions," gained `partial`/`surviving_literals` assertions. New
  pin `test_status_patterns_now_claims_four_rows` (mirrors the "...claims_zero_rows" family for
  the partial case).

  **Test conversion, 16 files — the largest wave in this epic**, because STATUS_PATTERNS' deleted
  vocabulary (tasks/status/progress/standup/assignments/portfolio-noun phrasing) was the most
  reused fixture vocabulary in the whole intent-service suite: `test_read_lane_destructive_
  greed_1756.py` (16 phrases across `STATUS_READS` + `READS_MENTIONING_DESTRUCTIVE_VERBS`),
  `test_subsumption_portfolio_write_family_1884.py` (production's `status_project_noun_overlap`
  VALUE COPY pruned from 9 to 2 members to match STATUS_PATTERNS' own shrink, plus 6 test-level
  probe-phrase swaps), `test_truncated_render_provenance_1738.py`, `test_subsumption_1084.py`,
  `test_keyword_disambiguation_901.py` (one STATUS-only control each), `test_task_clarify_1654.py`
  + `test_ftux_interview_1688.py` (2 sites) + `test_reminder_clear_pick_target_1906.py` (the
  epic's recurring "deterministic claim releases without a router call" discriminator, "give me my
  standup" → "what branch are we on?"), `test_inversion_multi_intent_unit4_1595.py` +
  `test_inversion_split_stand_down_1896.py` + `test_original_message_1460.py` (two-claim-split
  fixtures), `test_spend_free_canonical_ratchet_1818.py` (probe message only, pair unaffected).
  Plus one PRODUCT file: `services/intent_service/chat_pointers.py`'s `page:/standup` CHAT_POINTERS
  entry needed its verified utterance swapped too (discovered work, flagged not fixed: the
  replacement no longer reads as standup-themed to a user — no surviving STATUS_PATTERNS literal
  is).

  Full suite — **5166 passed, 1 xfailed, 0 failed** (re-run twice, identical both times; ceiling
  exact at 277). `scripts/run-sweep.sh ratchets` — same 1 PRE-EXISTING unrelated failure as the
  fifth/sixth deletions found (`test_todo_marker_ratchet`, 36 vs 35), confirmed unrelated again.
  `ruff format`/`ruff check --fix` clean on every touched `.py` file.

  **Tooling incident, self-corrected**: `ruff format`/`ruff check --fix` were run with
  `scripts/inversion_phase3_deleted_patterns.json` in the file list. ruff silently introduced
  TRAILING COMMAS (valid in nothing it targets; invalid JSON) — caught immediately by reloading
  the file, fixed via `git checkout HEAD -- scripts/inversion_phase3_deleted_patterns.json`
  (own worktree, nothing committed at risk, diffed first) + a clean re-append via `json.dump`.
  Lesson recorded in the doc: never pass `.json` paths to ruff.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Seventh deletion" subsection
  appended (full BEFORE/AFTER gate quotes, the partial rule, the STOP/unblock incident, all 16
  converted files with per-file rationale, the ruff/JSON incident, ceiling arithmetic).
  GUIDANCE_PATTERNS remains the last scored-but-not-yet-deleted list per the 10-01 rulings — now
  itself partial-shaped (3 survivors confirmed this session), per the 2026-10-02 partial-deletion
  rule.

- **2026-10-02 — #1595 Phase 3, eighth deletion: `GUIDANCE_PATTERNS` PARTIAL (18 of 21 literals,
  3 SURVIVE)**. The second partial deletion in this epic. Gate: `GO (partial) — 3 load-bearing
  literal(s) SURVIVE, deleting the other 18: ceiling 277 → 259`. 21 literals, 21 corpus rows
  claimed (18 `[OK]`, 3 `[FAIL]`). The 3 survivors (`\bsetup.*projects?\b`,
  `\bset up.*projects?\b`, `\bset up.*portfolio\b`) each a MATCH on a non-live op where a frozen
  N=5 surface-2 probe shows the LLM classifier landing EXECUTION 10/10 — never GUIDANCE. All 18
  deleted literals exercised 1:1 by a claimed corpus row (no unexercised literal, no cross-list
  shadowing — `claim_for_phrase`'s real if-chain attributed all 21 claimed rows to
  GUIDANCE_PATTERNS itself); 17 of the 18 `[OK]` rows pass via `surface2_verified_at_deletion`
  (10/10 combined per phrase, both legs), 1 (`\bgetting started\b`) via `misserved_at_deletion`
  (claims `get_contextual_guidance`, ruled `action:greeting`, router declined). Zero
  reabsorptions post-deletion.

  **Resolves a prior same-day STOP**: an earlier attempt this same day
  (`dev/2026/10/02/2026-10-02-1030-prog-code-log-1595-phase3-deletion-guidance.md`) tried a FULL
  tombstone of GUIDANCE_PATTERNS and STOPPED on 4 disagreeing reabsorptions via STATUS_PATTERNS'
  then-live `\bmy projects\b`/`\bmy portfolio\b` literals. STATUS_PATTERNS' own seventh deletion
  (same day, earlier) removed both literals; this PARTIAL additionally keeps GUIDANCE's own
  setup/portfolio literals alive regardless, closing the collision for 3 of the 4 phrases. The
  4th ("how do I configure my projects") is one of the 18 deleted here — confirmed post-deletion:
  UNCLAIMED (nothing reabsorbs it; the frozen probe shows it lands in GUIDANCE 10/10 via surface 2
  anyway).

  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 277 → 259. Ledger: 9th
  `DELETED_PATTERN_LISTS` entry (built programmatically, reloaded with `json.load` to confirm —
  never hand-edited, never passed to ruff). Ledger-count pin
  (`test_real_ledger_has_the_first_eight_deletions`, renamed to "...first nine deletions...")
  gained `GUIDANCE_PATTERNS` assertions. New pin `test_guidance_patterns_now_claims_three_rows`
  (mirrors the STATUS partial-case pin).

  **Test conversion, 2 files**: `test_setup_routing_814.py`'s
  `test_help_me_get_started_matches_guidance_patterns` (fixture matched the now-deleted
  `\bget started\b`) renamed + swapped to "help me set up my portfolio" (surviving literal).
  `test_spend_free_canonical_ratchet_1818.py`'s `("GUIDANCE", "get_contextual_guidance")` pair
  could NOT simply swap its probe message — all 3 surviving literals structurally force
  `_detect_setup_request`'s "projects" topic (same verb+noun shape), routing every reachable
  message to the non-spending onboarding branch, never the generic/spending branch the pair was
  measured against (confirmed: "help me set up my projects" crossed the spend chokepoint 0x).
  Removed the pair with a NOTE (same idiom as the TEMPORAL/PRIORITY removals), flagged as
  discovered work for Lead/Arch/CXO: the spending branch still exists for LLM-classifier-routed
  messages, just unreachable via this harness's step-1 drive now. `services/intent_service/
  chat_pointers.py` checked, NOT touched — its GUIDANCE pointers all resolve via
  `INTEGRATION_CONNECT_PATTERNS` ("connect my X"), never `GUIDANCE_PATTERNS` directly.

  Full suite — **5175 passed, 1 xfailed, 0 failed** (re-run twice, before and after
  `ruff format`/`ruff check --fix`, identical both times; ceiling exact at 259).
  `scripts/run-sweep.sh ratchets` — same 1 PRE-EXISTING unrelated failure as the
  fifth/sixth/seventh deletions (`test_todo_marker_ratchet`, 36 vs 35), confirmed unrelated again.
  `ruff format`/`ruff check --fix` run on `.py` files only (confirmed via `git status --porcelain`
  first — the ledger JSON was never in the touched-file list this time).

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Eighth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, the partial rule, the prior-STOP resolution, both
  converted test files + the chat_pointers.py check, ceiling arithmetic).
- 2026-10-02 15:5x — **DISCOVERY/ANALYSIS/TRUST/MEMORY deposits LANDED** (prog dispatch, Sonnet,
  not yet committed — index untouched per dispatcher instruction): all four lists are single-action
  (no per-literal branching — DISCOVERY → `get_capabilities`, ANALYSIS → `analyze_blockers`, TRUST
  → `explain_trust`, MEMORY → `get_memory`; all five actions including `pull_insights` are
  `ActionDisposition.FLOOR` in `action_registry.py` with zero `workflow_entries.py` registrations —
  documented, not a new finding). 67 total literals (DISCOVERY 20 + ANALYSIS 16 + TRUST 16 +
  MEMORY 15), 4 pre-existing claimed rows (1 per list), 63 unexercised, 62 reachable and deposited,
  1 structurally UNREACHABLE: MEMORY's `\bhow (much|far back) do you remember\b` (position 13) is a
  strict superset of its own earlier sibling `\bdo you remember\b` (position 2)
  — both alternatives contain "do you remember" as a direct substring with intact word boundaries,
  so the shorter earlier pattern always claims first (same structural shape as STATUS's "my current
  work"/"current work"; confirmed empirically with two phrasings). No reword needed for any of the
  62 deposited phrases — each checked by hand for same-list earlier-sibling shadowing and
  cross-list earlier-checked-list shadowing before drafting, then confirmed via
  `PreClassifier.pre_classify_with_pattern_list` (list identity) + `_first_pattern_match` (literal
  identity) against the real production matcher. No `expected` corrections applied — none of these
  four lists carries an in-corpus/in-code anchor pointing a specific literal at a different
  registered destination the way STATUS's standup/portfolio literals did; correcting without one
  would be guessing. Corpus 385→447 (+62, purely additive — `git diff --stat` 686 insertions/0
  deletions across the builder + fixture); pinned total in `test_inversion_phase3_deletion_1595.py`
  updated 385→447 (claimed 59→121, unclaimed unchanged at 326); no other pinned `385` corpus-size
  constant found (`git grep -n "\b385\b" -- tests scripts`, only unrelated hits). Gate re-run
  `--all`: DISCOVERY 20/20 claimed, ANALYSIS 16/16, TRUST 16/16, MEMORY 14/15 (the 1 unreachable
  literal correctly has no row) — all four still NO-GO (every new row correctly UNSCORED; scoring
  is the Lead's budgeted run, no LLM calls made anywhere in this unit). Extraction ceiling
  unaffected: 259 unchanged (`pattern_literal_counts.total_literal_count()` confirmed) — deposits
  add corpus rows only, no `pre_classifier.py` literal touched. Tests:
  `test_inversion_phase3_deletion_1595.py` + `test_inversion_phase3_surface2_floor_1595.py` +
  `test_preclaim_shadow.py` + `tests/test_architecture_enforcement.py` run together, 144 passed/1
  xfailed, 0 failed. `ruff format`/`ruff check --fix` clean on both touched `.py` files. All four
  lists are now GO-eligible (DISCOVERY/ANALYSIS/TRUST fully, MEMORY partially pending the 1
  unreachable literal) for the same deletion procedure once the Lead's budgeted shadow-score run
  judges these 62 rows — not scored, not deleted, in this unit.
- 2026-10-03 — **NINTH DELETION, `DISCOVERY_PATTERNS`, PARTIAL** (prog dispatch, Sonnet): BEFORE
  gate (`--list DISCOVERY_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
  read_referent,read_status,read_strategic,read_synthesis,read_temporal`) read GO (partial) — 1
  load-bearing literal (`\bneed\s*help\b`) SURVIVES, deleting the other 19: ceiling 259 → 240. 20
  literals, 20/447 corpus rows claimed (19 `[OK]`, 1 `[FAIL]` — the survivor, a MISMATCH where the
  router declines `CLARIFY@0.6` and a frozen N=10 surface-2 probe shows the LLM classifier missing
  `get_capabilities` 0/10 samples).

  **The clean case**: all 20 literals were exercised 1:1 by exactly one claimed corpus row each
  (confirmed via `unexercised_literals("DISCOVERY_PATTERNS", lv.rows)` → 0 unexercised) — no
  `shadowed_literals`, no corpus deposits needed, no STOP. All 19 `[OK]` deleted-literal rows pass
  via a plain live MATCH (18) or REVIEW-agrees (1, "what can you do?") — `get_capabilities` is a
  LIVE op (`_READ_FLOOR_MEMBERS`'s `read_floor` rail entry) and the router actually serves it live
  on every row, so unlike STATUS/GUIDANCE neither `surface2_verified_at_deletion` nor
  `misserved_at_deletion` has any entries in this ledger entry. Zero reabsorptions post-deletion
  (checked both entry surfaces via `claim_for_phrase` against all 19 deleted-literal phrases).

  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 259 → 240. Ledger: 10th
  `DELETED_PATTERN_LISTS` entry (built programmatically, reloaded with `json.load` to confirm —
  never hand-edited, never passed to ruff). Ledger-count pin
  (`test_real_ledger_has_the_first_nine_deletions`, renamed to "...first ten deletions...") gained
  `DISCOVERY_PATTERNS` assertions. New pin `test_discovery_patterns_now_claims_one_row` (mirrors
  the STATUS/GUIDANCE partial-case pins).

  **Test conversion, 4 files**: `test_discovery_intent.py`'s 16-phrase
  `test_discovery_patterns_match` renamed to `test_discovery_patterns_now_unclaimed_by_surface_1`
  and flipped to assert `None` (unclaimed, not misrouted); added
  `test_discovery_survivor_literal_still_matches`; `test_discovery_before_identity_precedence`'s
  fixture swapped to the survivor phrase. `test_setup_routing_814.py`'s
  `test_what_can_you_do_still_routes_to_discovery` fixture swapped to the survivor phrase.
  `test_preclaim_shadow.py`'s canonical DISCOVERY fixture "what can you do?" (12 occurrences across
  all 5 pins) swapped to the survivor phrase throughout — every pin's actual point unchanged.
  `test_spend_free_canonical_ratchet_1818.py`'s `("DISCOVERY", "get_capabilities")` pair's probe
  message swapped to the survivor phrase; unlike GUIDANCE's pair this needed no removal — the
  handler flow for `get_capabilities` doesn't depend on which literal matched, so the pair still
  crosses the spend chokepoint exactly as before (`crossings > 0`, confirmed empirically), staying
  in `SPENDS`. `services/intent_service/chat_pointers.py` checked, NOT touched — no `CHAT_POINTERS`
  entry resolves through `DISCOVERY_PATTERNS`.

  Full suite — `tests/unit/services/intent_service/` + `tests/test_architecture_enforcement.py`:
  **5072 passed, 1 xfailed, 0 failed**. Plus `test_inversion_phase3_deletion_1595.py` +
  `test_inversion_phase3_surface2_floor_1595.py` + `test_inversion_phase1_shadow_score_1595.py`:
  **77 passed** (the #1897 spend-free shape pin is covered inside the intent_service run above;
  the genuinely-LLM-spending `tests/e2e/test_1897_two_part_turn_live.py` is out of scope for a
  no-LLM-calls unit). `ruff format`/`ruff check` run on `.py` files only (confirmed via
  `git status --short` before invoking ruff — the ledger JSON never touched by it); clean on every
  touched file.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Ninth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, the partial rule, why no surface2_verified_at_deletion/
  misserved_at_deletion entries were needed this time, all 4 converted test files + the
  chat_pointers.py check, ceiling arithmetic).
- 2026-10-03 — **TENTH DELETION, `TRUST_PATTERNS`, PARTIAL** (prog dispatch, Sonnet): BEFORE gate
  (`--list TRUST_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
  read_referent,read_status,read_strategic,read_synthesis,read_temporal`) read GO (partial) — 1
  load-bearing literal (`\bwhy can'?t you\b`) SURVIVES, deleting the other 15: ceiling 240 → 225.
  16 literals, 16/447 corpus rows claimed (15 `[OK]`, 1 `[FAIL]` — the survivor, a
  REVIEW-disagrees row where the router names `get_capabilities@0.9`, a live op, but the expected
  destination is REVIEW/not-action-shaped).

  **Unexercised-literal audit**: all 16 literals (15 to-delete + the 1 survivor) were exercised
  1:1 by exactly one claimed corpus row each (confirmed via `unexercised_literals
  ("TRUST_PATTERNS", lv.rows)` → 0 unexercised) — no `shadowed_literals`, no corpus deposits
  needed, no STOP. 14 of the 15 deleted rows pass via a plain live MATCH (expected action live via
  group — `explain_trust`/`get_capabilities`/`pull_insights` all live under this flag); 1 ("why
  are you always cautious about this suggestion") passes via the mis-serve escape —
  TRUST_PATTERNS claims `explain_trust`, disagreeing with the ruled `action:explain_suggestion`;
  the router independently reaches `explain_suggestion@0.95` live, and a frozen N=10 surface-2
  probe does NOT show the LLM classifier landing PROVENANCE on every sample (0/10), but the
  mismatch is deletable regardless (deleting a deterministically-wrong fallback cannot regress the
  row). `surface2_verified_at_deletion` is empty for this entry — the one row that attempted that
  escape failed its probe and passed via the mis-serve rule instead. Zero reabsorptions
  post-deletion (checked both entry surfaces via `claim_for_phrase` against all 15
  deleted-literal phrases).

  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 240 → 225. Ledger: 11th
  `DELETED_PATTERN_LISTS` entry (built programmatically, reloaded with `json.load` to confirm —
  never hand-edited, never passed to ruff). Ledger-count pin
  (`test_real_ledger_has_the_first_ten_deletions`, renamed to "...eleven deletions...") gained
  `TRUST_PATTERNS` assertions. New pin `test_trust_patterns_now_claims_one_row`.

  **Test conversion, 1 file**: `tests/unit/services/test_pre_classifier.py`'s
  `test_trust_patterns` renamed to `test_trust_patterns_now_unclaimed_by_surface_1` and flipped to
  assert `None` for the 13 now-unclaimed phrasings; added `test_trust_survivor_literal_still_
  matches`. `test_memory_not_trust`'s second fixture swapped to the survivor phrase.
  `test_trust_still_routes_after_provenance` (7 phrasings, a PROVENANCE-collision regression
  guard) split into a `now_unclaimed` list (asserting `None`, confirming PROVENANCE's own verb
  list doesn't steal these phrasings) plus the 1 survivor query, still asserted TRUST.
  `test_trust_not_identity` was unaffected (its fixture matches the survivor).
  `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`'s
  `("TRUST", "explain_trust")` pair was unaffected (its probe message matches the survivor,
  confirmed by a direct run). `tests/e2e/test_read_floor_live.py` checked, NOT touched
  (`pytest.mark.llm`-gated, out of scope regardless). `services/intent_service/chat_pointers.py`
  checked, NOT touched — no `CHAT_POINTERS` entry resolves through `TRUST_PATTERNS`.

  Full suite — `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
  + `tests/test_architecture_enforcement.py` + the three inversion_phase3/phase1 test files (one
  combined invocation, run in background due to runtime): **5184 passed, 1 xfailed, 0 failed**.
  `tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures, run separately):
  **16 failed, 11 passed** — same count as the baseline, confirming no new failures. `ruff
  format`/`ruff check` run on `.py` files only (confirmed via `git status --short` before invoking
  ruff — the ledger JSON never touched by it); clean on every touched file.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Tenth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, the partial rule, the one misserved_at_deletion row and
  why surface2_verified_at_deletion is empty, all converted test files + the e2e/chat_pointers.py
  checks, ceiling arithmetic).
- 2026-10-03 — **ELEVENTH DELETION, `MEMORY_PATTERNS`, PARTIAL** (prog dispatch, Sonnet): BEFORE
  gate (`--list MEMORY_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
  read_referent,read_status,read_strategic,read_synthesis,read_temporal`) read GO (partial) — 3
  load-bearing literals (`\b(my|our) (conversation )?history\b`, `\bsearch (my |our )?
  (conversation )?history\b`, `\bwhat (i|we) (said|talked|discussed)\b`) SURVIVE, deleting the
  other 12: ceiling 225 → 213. 15 literals, 14/447 corpus rows claimed (11 `[OK]`, 3 `[FAIL]` —
  the 3 survivors, each with no live fallback naming the same op).

  **Unexercised-literal audit — not clean this time, as the dispatch prompt flagged in advance**:
  14 of the 15 literals were exercised 1:1 by a claimed row, but 1
  (`\bhow (much|far back) do you remember\b`) was not (confirmed via `unexercised_literals
  ("MEMORY_PATTERNS", lv.rows)` → exactly 1). Audited by constructing natural phrasings ("how much
  do you remember", "how much do you remember about me", "how far back do you remember", "how far
  back do you remember our conversations") and running them through the REAL if-chain,
  `PreClassifier.pre_classify_with_pattern_list` — every one is claimed by `\bdo you remember\b`
  (checked earlier in the same list), a guaranteed substring of anything the unexercised literal
  would ever match. PROVABLY SHADOWED within the same list, not cross-list; `\bdo you remember\b`
  is itself one of the 12 literals this deletion removes (not a survivor), so no corpus deposit
  was needed and no STOP. 10 of the 11 claimed deleted rows pass via a plain live MATCH; 1
  ("remember when we shipped the last release?") passes via the mis-serve escape —
  MEMORY_PATTERNS claims `get_memory`, disagreeing with the ruled `action:check_completion_status`;
  the router independently MATCHes `check_completion_status@0.85` on a non-live op, and a frozen
  N=10 surface-2 probe does NOT show the LLM classifier landing STATUS on every sample (0/10), but
  the mismatch is deletable regardless. `surface2_verified_at_deletion` is empty for this entry.
  1 AGREEING reabsorption post-deletion: "can you show my conversation history" (formerly claimed
  by the deleted `\b(show|view|see) ... history\b` literal) reclaimed by the surviving
  `\b(my|our) (conversation )?history\b` literal — same action, same list. The other 10
  deleted-row phrases plus both unexercised-literal candidates are genuinely UNCLAIMED (checked
  both entry surfaces via `claim_for_phrase`).

  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 225 → 213. Ledger: 12th
  `DELETED_PATTERN_LISTS` entry (built programmatically, reloaded with `json.load` to confirm —
  never hand-edited, never passed to ruff; two Python raw-string escaping artifacts in the `note`
  prose caught and fixed before commit via a byte-diff review). Ledger-count pin
  (`test_real_ledger_has_the_first_eleven_deletions`, renamed to "...twelve deletions...") gained
  `MEMORY_PATTERNS` assertions. New pin `test_memory_patterns_now_claims_four_rows`.

  **Test conversion, 3 files**: `tests/unit/services/test_pre_classifier.py`'s
  `test_memory_patterns` renamed to `test_memory_patterns_now_unclaimed_by_surface_1` and flipped
  to assert `None` for 9 now-unclaimed phrasings; added `test_memory_survivor_literals_still_match`
  for the 3 remaining (2 reabsorbed, 1 unaffected). `test_memory_not_trust` and
  `test_portfolio_not_memory`'s MEMORY fixtures swapped to the survivor phrase "our history
  together has been good". `test_memory_get_memory_still_works_after_pull_insights` (4 phrasings,
  an INSIGHT_PULL-ordering regression guard) split into a `now_unclaimed` list (3 phrasings) plus
  the 1 survivor query, still asserted MEMORY/`get_memory`.
  `tests/unit/services/intent_service/test_read_lane_destructive_greed_1756.py`:
  `MEMORY_LANE_DESTRUCTIVE` unaffected (the destructive-ask guard declines before any literal is
  consulted); `MEMORY_READS` (11 phrases in `KEEP_CLAIMING`) split — 8 now-unclaimed moved to a new
  `MEMORY_READS_NOW_UNCLAIMED` set with a new `TestMemoryReadsNowDeclineAtSurfaceOne` class
  (mirrors `TestTemporalReadsNowDeclineAtSurfaceOne`), 3 kept; `READS_MENTIONING_DESTRUCTIVE_VERBS`
  had 2 of 5 phrases swapped for equivalents via the surviving history literals.
  `tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py`'s
  `("MEMORY", "get_memory")` probe message swapped to the survivor phrase. `tests/e2e/
  test_read_floor_live.py` checked, NOT touched (`pytest.mark.llm`-gated, out of scope
  regardless). `services/intent_service/chat_pointers.py` checked, NOT touched — no
  `CHAT_POINTERS` entry resolves through `MEMORY_PATTERNS`.

  Full suite — `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
  + `tests/test_architecture_enforcement.py` + the three inversion_phase3/phase1 test files (one
  combined invocation, run in background due to runtime): **5186 passed, 1 xfailed, 0 failed**.
  `tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures, run separately):
  **16 failed, 11 passed** — same count as the baseline, confirming no new failures. `ruff
  format`/`ruff check` run on `.py` files only (confirmed via `git status --short` before invoking
  ruff — the ledger JSON never touched by it); clean on every touched file.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Eleventh deletion"
  subsection appended (full BEFORE/AFTER gate quotes, the partial rule, the shadowed-literal audit,
  the one misserved_at_deletion row, the one known_reabsorptions entry, all converted test files +
  the e2e/chat_pointers.py checks, ceiling arithmetic).
- 2026-10-03 — **TWELFTH DELETION, `ANALYSIS_PATTERNS`, PARTIAL** (prog dispatch, Sonnet): BEFORE
  gate (`--list ANALYSIS_PATTERNS --live create_reminder,create_todo,delete_todo,read_floor,
  read_referent,read_status,read_strategic,read_synthesis,read_temporal`) read GO (partial) — 4
  load-bearing literals (`\bwhat.*obstacle\b`, `\bwhat'?s in the way\b`, `\banalyze.*
  (?:risk|impact|blocker|bottleneck)\b`, `\bimpact analysis\b`) SURVIVE, deleting the other 12:
  ceiling 213 → 201. 16 literals, 16/447 corpus rows claimed (12 `[OK]`, 4 `[FAIL]` — the 4
  survivors, each a MISMATCH where the router declines with CLARIFY@0.4 and the pattern is the
  only live path).

  **Unexercised-literal audit — the clean case this time**: all 16 literals exercised 1:1 by a
  claimed row (confirmed via `unexercised_literals("ANALYSIS_PATTERNS", lv.rows)` → empty). No
  shadowing audit needed, no corpus deposit needed, no STOP.

  **The one `misserved_at_deletion` row**: "is there a bottleneck analysis available" (matched the
  deleted `\bbottleneck.*(?:analysis|report)\b` literal, claiming `analyze_blockers`) disagrees
  with the ruled destination (`action:get_capabilities`, RULED 2026-10-02 by PPM: "is there X
  available" is the DISCOVERY existence question). Unlike the eleventh deletion's mis-serve row,
  this one is credited through the ORDINARY live-MATCH branch (router independently MATCHes
  `get_capabilities@0.92`, expected action live via group) — `row_disposition` never needs its
  mis-serve escape to pass it, but the pattern's own claim is already wrong today regardless, so
  deleting it cannot regress the row. `surface2_verified_at_deletion` is empty (never needed). The
  other 11 deleted rows pass via a plain live MATCH/REVIEW-agrees.

  Ceiling: `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]` 213 → 201. Ledger: 13th
  `DELETED_PATTERN_LISTS` entry (built programmatically via a one-off Python script with
  `ensure_ascii=True` — the eleventh deletion's own note flagged that `ensure_ascii=False` silently
  re-encodes 3 PRE-EXISTING em-dash escapes elsewhere in the file; built with the default this
  time and confirmed via `git diff --numstat` showing a pure 68-line insertion, 0 deletions —
  reloaded with `json.load` immediately to confirm 13 entries, parses cleanly). Ledger-count pin
  (`test_real_ledger_has_the_first_twelve_deletions`, renamed to "...thirteen deletions...") gained
  `ANALYSIS_PATTERNS` assertions. New pin `test_analysis_patterns_now_claims_four_rows` (no
  reabsorbed row this time, so the count stays exactly the 4-survivor count — unlike MEMORY's
  eleventh deletion's 3+1).

  **AFTER reabsorption check**: all 12 deleted-row phrases verified via `claim_for_phrase` (both
  entry surfaces) against the live, post-deletion `PreClassifier` — **zero reabsorptions**, all 12
  genuinely UNCLAIMED (the 4 survivors' broader regexes checked carefully for accidental breadth;
  none catch any of the 12). `gate --all`: `ANALYSIS_PATTERNS 4 4 NO-GO` (exactly the 4 survivors,
  all still `[FAIL]`). Corpus denominator: 447 = 65 claimed + 382 unclaimed (down from 77; 77 − 65
  = 12, the full deleted-row set, none reabsorbed).

  **Test conversion, 3 files** (beyond the ledger/ceiling/pin files above):
  `tests/unit/services/test_pre_classifier.py`'s `test_analysis_risk_patterns` (3 phrasings, all
  matched now-deleted literals) renamed to `test_analysis_risk_patterns_now_unclaimed_by_surface_1`
  and flipped to assert `None`; added `test_analysis_risk_survivor_literal_still_matches` for the
  surviving `\banalyze.*(?:risk|impact|blocker|bottleneck)\b` literal. `test_blocker_analysis_patterns`
  (2 phrasings, both matched the now-deleted `\bwhat'?s blocking\b` literal) renamed to
  `test_blocker_analysis_patterns_now_unclaimed_by_surface_1`, flipped to assert `None`.
  `tests/unit/services/intent_service/test_keyword_disambiguation_901.py`'s
  `TestKeywordDisambiguationQ43` (4 tests, all using now-deleted-literal phrases) renamed and
  swapped 1:1 to the 4 surviving literals' own corpus phrases, preserving the Q43 disambiguation
  point (ANALYSIS reachable at surface 1, not misrouted to STATUS).
  `tests/unit/services/intent_service/test_preclaim_shadow.py`: 4 call sites (plus explanatory
  comments) used "what's blocking the milestone?" as the canonical multi-intent/"3+ distinct
  claiming lists" `ANALYSIS_PATTERNS` fixture — swapped throughout to "what's the main obstacle
  here" (the surviving `\bwhat.*obstacle\b` literal).

  Checked, NOT touched: `tests/unit/services/intent_service/test_action_registry.py` +
  `test_read_floor_rail_1595.py` (registry/rail membership only, never a surface-1 literal match);
  `tests/e2e/test_read_floor_live.py` (`pytest.mark.llm`-gated, out of scope); `tests/e2e/
  test_canonical_conversations.py` (tests/e2e, requires live DB/app, outside this dispatch's
  tests/unit scope, and its expected destination is already "floor" regardless of which surface
  claims the phrase); `tests/unit/services/intent_service/test_conversational_floor.py` (builds a
  `FloorContext` dataclass directly, never calls `pre_classify`); `services/intent_service/
  chat_pointers.py` (no `CHAT_POINTERS` entry resolves through `ANALYSIS_PATTERNS`); `tests/
  fixtures/inversion_corpus_phase0.yaml` (ground-truth corpus, never edited by this procedure).

  Full suite — `tests/unit/services/intent_service/` + `tests/unit/services/test_pre_classifier.py`
  + `tests/test_architecture_enforcement.py` + the three inversion_phase3/phase1 test files (one
  combined invocation, run in background due to runtime, twice — once to find the
  `test_analysis_risk_patterns`/`test_blocker_analysis_patterns` failures under `-x --maxfail=1`,
  once clean after converting them): **5188 passed, 1 xfailed, 0 failed**.
  `tests/unit/services/test_multi_intent.py` (pre-existing out-of-scope failures, run separately):
  **16 failed, 11 passed** — identical to the stated baseline, confirming no new failures. `ruff
  format`/`ruff check` run on `.py` files only (confirmed via `git status --short` before invoking
  ruff — the ledger JSON never touched by it); clean on every touched file.

  Doc: `docs/internal/architecture/current/intent-routing-stack.md`'s "Twelfth deletion" subsection
  appended (full BEFORE/AFTER gate quotes, the partial rule, the clean unexercised-literal audit,
  the one misserved_at_deletion row, the zero known_reabsorptions, all converted test files + the
  e2e/chat_pointers.py/fixtures-yaml checks, ceiling arithmetic).
