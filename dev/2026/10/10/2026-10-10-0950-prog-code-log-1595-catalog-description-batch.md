# Session log — prog-code — #1595 catalog description batch

**Role**: Coding Agent (prog-code)
**Model**: Sonnet (claude-sonnet-5)
**Date**: 2026-10-10
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) — dispatched by Lead, NOT committed/pushed/mailed per instructions.

## Task

Find router catalog DESCRIPTION-only wording (no prompt-structure change) for ONE batched catalog
change covering:

- **(A)** Arch's 10-08 queued fix: add the clause "the user's own calendar only; never a team's, a
  shared or another person's calendar" to `week_calendar`'s description, ADDED to CXO's 10-06 clause
  (not replacing it).
- **(B)** Three rows Arch's 10-10 ruling (#1970) named as "worth having for their own sake, as
  ordinary description changes":
  1. "show priorities for this sprint" → get_top_priority (was: prioritize @0.85)
  2. "pull up my schedule" → week_calendar (was: meeting_time @0.72)
  3. "show today's tasks" → list_todos_query (was: attention_query @0.85)

Hard cap: 200 live router calls via `scripts/inversion_phase1_shadow_score.py --phrase`. No full-corpus run (Lead's, at review).

## Context read first (mandatory)

`docs/internal/architecture/current/intent-routing-stack.md` — too large to read whole (440KB);
grepped the load-bearing rule instead: **"The router reads a rail entry's description in preference
to `ACTION_DESCRIPTIONS` once an op has an entry"** (`derive_routing_grammar`). `get_top_priority` has
NO WorkflowEntry (FLOOR disposition, confirmed via `ACTION_REGISTRY` — `("PRIORITY",
"get_top_priority"): ActionDisposition.FLOOR`), so its only description lever is `ACTION_DESCRIPTIONS`
in `services/intent_service/action_registry.py`. `prioritize`, `week_calendar`, `meeting_time`,
`attention_query`, `list_todos_query` all have rail `WorkflowEntry`s in
`services/intent_service/workflow_entries.py`, so their descriptions live there and win over any
`ACTION_DESCRIPTIONS` text.

Also read the mailbox trail establishing the exact asks:
- `mailboxes/ppm/read/rule-arch-to-lead-cc-cxo-ppm-team-calendar-real-read-miss-no-restore-batch-description-fix-per-row-reledger-never-bulk-swap-2026-10-08.md` — (A)'s source.
- `mailboxes/lead/sent/done-lead-to-cxo-cc-arch-batch...` / `...done-lead-to-cxo-cc-arch-ppm-condition-a-probe...2026-10-08.md` — confirms the current (CXO 10-06 + Arch 10-08-queued) week_calendar text and that the own-calendar clause is additive, not a replace.
- `mailboxes/ppm/read/ask-lead-to-arch-cc-ppm-1970-framing-prompt-held-...2026-10-10.md` + `mailboxes/ppm/read/ruling-arch-to-lead-cc-ppm-1970-option-c-...2026-10-10.md` — Arch's ruling naming the 3 (B) rows as "fixes" worth doing as plain description changes, independent of the held/rejected framing-prompt change. Treated the ruling's named destinations (get_top_priority / week_calendar / list_todos_query) as authoritative even though the corpus YAML's stale `expected: floor` field for row 1 predates this ruling — not in scope to edit the corpus itself.

## Method

Single-row scorer only (`--provider anthropic --phrase "<phrase>"`), one Haiku-class call per
invocation. Wrote a small zsh helper (`score.sh` in scratchpad) that runs the scorer quietly and
greps the row-detail line. Edited the catalog in place, iterated, and verified; never ran a
full-corpus pass.

**Guard set** (11 rows, chosen per the dispatcher's criteria — the 5 named phrases plus up to 6 more
corpus rows whose expected op is one of the 6 touched ops, preferring different phrasings):

| # | Guard phrase | Expected op |
|---|---|---|
| G1 | "what's my agenda today" | meeting_time |
| G2 | "how many meetings this week" (stand-in for "how much time am I in meetings this week" — no exact corpus row) | week_calendar |
| G3 | "what's my top priority" | get_top_priority |
| G4 | "what are my todos" | list_todos_query |
| G5 | "what needs my attention?" | attention_query |
| G6 | "this is top priority for the team" | get_top_priority |
| G7 | "mark this as priority one" | prioritize |
| G8 | "what is on my calendar" | week_calendar |
| G9 | "calendar today please" | meeting_time |
| G10 | "list my todos" | list_todos_query |
| G11 | "this project needs my attention today" | attention_query |

### Baseline (unchanged tree), ×3 each = 33 calls

All MATCH except two already-failing/flaky rows on **origin/main, before any edit**:
- G6 "this is top priority for the team" → `NONE`@0.95 ×3, counted MATCH only via the FLOOR-op
  leniency rule (get_top_priority has no rail entry).
- G7 "mark this as priority one" → `CLARIFY`@0.4 ×3, genuine MISMATCH pre-existing.
- G11 "this project needs my attention today" → `NONE`@0.95 ×3, genuine MISMATCH pre-existing.

These three were already imperfect before this change; the bar is "doesn't get worse," not "now
perfect."

## Edits made (final, in the tree — uncommitted)

1. **`services/intent_service/action_registry.py`** — `("PRIORITY", "get_top_priority")` in
   `ACTION_DESCRIPTIONS`:
   - Old: `"Answer what-should-I-work-on-first / top-priority questions"`
   - New: `"Answer what-should-I-work-on-first / top-priority questions, including requests to show
     or list the current priorities for a sprint or project — not a request to set, rank, or reorder
     specific named items, which is prioritize (#1595)"`

2. **`services/intent_service/workflow_entries.py`** — `prioritization_entry.description`:
   - Old: `"Prioritization via action dispatch (#1124)"`
   - New: `"Re-rank, reorder, or set the priority of specific NAMED items (e.g. 'mark this as priority
     one', 'set the priority order of these three tasks') — not a request to see or list the current
     priorities, which is get_top_priority (#1124, #1595)"`

3. **`services/intent_service/workflow_entries.py`** — `_CALENDAR_QUERY_DESCRIPTIONS["_handle_week_calendar_query"]`
   (combines (A)'s own-calendar clause AND the row-2 "schedule" synonym fix in one text, since both
   land on the same field):
   - Old: `"Calendar for the WEEK ahead or several days (this week, next week, the coming days),
     including the free time in it — never a single day. It lists the calendar; it does not judge
     conflicts, overlaps, double-bookings or clashes, and does not answer yes/no questions about the
     calendar (#1595)"`
   - New: `"Calendar or schedule for the WEEK ahead or several days (this week, next week, the coming
     days), including the free time in it — never a single day. It lists the calendar; it does not
     judge conflicts, overlaps, double-bookings or clashes, and does not answer yes/no questions
     about the calendar. It is the user's own calendar only — never a team's, a shared, or another
     person's calendar (#1595)"`

4. **`services/intent_service/workflow_entries.py`** — the todo-query `_qentry` description (feeds
   `list_todos_query`/`list_completed_todos`/`next_todo_query`):
   - Old: `"todo list/next query via action dispatch"`
   - New: `"List the user's todos or tasks as they stand — show my todos, list my tasks, what are my
     todos, today's tasks, my to-do list — a plain listing, not ranked by urgency, which is
     attention_query (#1595)"`

`meeting_time`'s and `attention_query`'s own descriptions were left **unchanged** — both target
fixes (row 2, row 3) were achievable by sharpening the *other* side of the pair only, which is the
smaller-footprint edit.

## Verification (per-candidate, then final combined pass)

Each candidate was tested standalone (target ×6 + its directly-neighboring guards ×3) immediately
after editing, with all prior edits in the tree (so by row 3's test, rows 1+2's edits were already
live). After all four edits landed, ran a **final combined pass**: all 3 targets ×6 + all 11 guards
×3 + "show the team calendar" ×3, to rule out cross-op interaction (low a priori risk — priority /
calendar / todo are semantically disjoint clusters — but worth the cheap confirmation).

**Row 1 — "show priorities for this sprint"**: 6/6 `get_top_priority`@0.95 (both standalone and
final pass). Guards G3/G6/G7 held (G7 "mark this as priority one" actually *improved*,
`CLARIFY`@0.4 → `prioritize`@0.85–0.95 MATCH — a bonus, not required). Spot-checked the untouched
sibling "list priorities for the team" (expected floor, not a formal guard per the dispatcher's
criteria but an obvious contamination risk from broadening get_top_priority's text) ×3: stayed
`NONE`@0.85 MATCH, no regression.

**Row 2 — "pull up my schedule"**: 6/6 `week_calendar`@0.85 (both passes). Guards G1/G2/G8/G9 held
exactly (meeting_time untouched, so no risk there).

**(A) "show the team calendar"**: 3/3 `NONE`@0.95 (floor) after the own-calendar clause — does not
route to week_calendar, as required.

**Row 3 — "show today's tasks"**: 6/6 `list_todos_query`@0.95 (both passes). Guards G4/G5/G10 held
exactly. G11 "this project needs my attention today" (already flaky pre-edit, 3/3 `NONE`) showed
1/3 `attention_query`@0.85 + 2/3 `NONE`@0.95 in both the standalone and final pass — never flipped to
`list_todos_query` or any new wrong destination; the one changed outcome is the row's *correct*
expected answer, so this reads as pre-existing instability, not a regression caused by the edit.

**Final combined pass** (all 4 edits live simultaneously): all 3 targets 6/6 at their new ops; all
11 guards + team-calendar held exactly as in their standalone checks (same G11 flakiness, unchanged
from the standalone row-3 check).

## Call budget

| Phase | Calls |
|---|---|
| Mechanics check (1 throwaway call establishing baseline for row 2, folded into "before" evidence) | 1 |
| Baseline guards ×3 × 11 | 33 |
| Row 1: target ×6 + guards G3/G6/G7 ×3×3 | 15 |
| Row 1 sibling spot-check ("list priorities for the team") ×3 | 3 |
| Row 2: target ×6 + guards G1/G2/G8/G9 ×3×4 | 18 |
| (A) team-calendar ×3 (mid-pass) | 3 |
| Row 3: target ×6 + guards G4/G5/G10/G11 ×3×4 | 18 |
| Final combined: 3 targets ×6×3 | 18 |
| Final combined: 11 guards ×3×11 + team-calendar ×3 | 36 |
| **Total** | **145** |

145 of the 200-call budget used. No full-corpus run.

## Test + lint evidence

- Grepped `tests/` for every old description string before editing — no test pins any of the
  four changed strings (`Prioritization via action dispatch`, `todo list/next query via action
  dispatch`, the old `get_top_priority` text, the old `week_calendar` text). No test file needed
  updating.
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py tests/unit/services/intent_service -q -p no:cacheprovider`
  → **`5444 passed, 29 warnings in 145.91s (0:02:25)`**, exit code 0. (29 warnings are pre-existing
  `RuntimeWarning: coroutine ... was never awaited` / one stray `@pytest.mark.asyncio` marker in
  unrelated test files — not touched by this change, not new.)
- `venv/bin/ruff format --check services/intent_service/action_registry.py services/intent_service/workflow_entries.py`
  → `2 files already formatted`.
- `venv/bin/ruff check services/intent_service/action_registry.py services/intent_service/workflow_entries.py`
  → `All checks passed!`

## Verified how

Method: `scripts/inversion_phase1_shadow_score.py --provider anthropic --phrase "<phrase>"`, one
live Haiku-class router call per invocation, reading the row-detail table line from each run's
output file. Layer: the INVERSION ROUTER ONLY (per the script's own m-43 note) — an empty session
snapshot, not the full production chain; a router MATCH here is not itself proof of the full
chat-path behavior, only of the catalog-grammar-level routing decision this task is scoped to.
Denominator: 3 of the 6 target rows' candidates were tested at the stated ×6/×3 depths; the other 3
corpus rows named in the task body (B's own phrasing) ARE the 3 target rows scored. 11 of the
corpus's full set of rows neighboring the 6 touched ops were used as guards (not the full neighbor
set — picked per the dispatcher's own criteria, diversity-preferring). No full-corpus run was
performed or claimed.

## Discovered work

- "list priorities for the team" (expected floor) sits one semantic step from "show priorities for
  this sprint" (now get_top_priority) and from "mark this as priority one" (prioritize) — all three
  share the word "priorities" but resolve to three different ops/floor. Spot-checked clean (×3,
  stays floor) but this triad is worth a note for whoever next touches PRIORITY descriptions: it's a
  tight corner, verify before extending further.
- G11 "this project needs my attention today" is flaky independent of this change (3/3 NONE on
  origin/main, 1/3 attention_query + 2/3 NONE after) — pre-existing instability, not filed as a new
  issue since it's a known_live_miss-shaped situation Arch/Lead already have a pattern for (see the
  team-calendar precedent); flagging in this log per "write it down even if not ratified," leaving
  the filing decision to Lead.

## Git status at handoff

Not committed/pushed per instructions (Coding Agent dispatch: work only in the worktree, no commit/push/mail).
