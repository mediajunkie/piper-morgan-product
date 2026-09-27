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
