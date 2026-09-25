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
