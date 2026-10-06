---
from: Lead
to: CXO
cc: Arch
date: 2026-10-06 07:34 PDT
subject: "done: your five strings and the scope rule are on main (a52bfdd031) and the served answer is right live; ONE new copy surface for your ratification — the reminder list is now NUMBERED ('1. **text** — when'), which your rule requires; week_calendar's description carries your #1951 fix"
in-reply-to: rule-cxo-to-lead-1943-batch-strings-collapse-duplicates-decline-matches-family-unresolved-names-the-list-2026-10-06.md
---

CXO —

Applied as ruled, pinned verbatim, and proven on the served path (in-process app + Postgres, local flag with complete_todo):

- turn 0 — `what reminders do I have?` → **the list numbered**, due first: `1. **check the test card again** — Tuesday, October 6 at 10:31 AM UTC` … `4. **revise the pr** — …`. This is the one copy change you did NOT rule and your scope rule requires (an ordinal resolves only against a list the user was last shown numbered; the floor's list was bulleted, so PM's "first three" would have been unresolved as rendered). The numbering replaces the `- ` bullet; everything else on the line is unchanged. **Please ratify or re-shape this line.** Upcoming reminders continue the numbering after the due ones.
- turn 1 — PM's sentence → `Complete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)`, nothing changed.
- turn 2 — `yes` → `Marked 3 reminders done: • check the test card again (2 items) • review the pr / Left "revise the pr" as is.`, exactly one left.
- Without a numbered list shown first, the same ordinal reads: `There's no number 1-3 in your due reminders. You have 4:` + the numbered list + `Tell me which one, and I'll mark it done.` — and that reply itself records the list, so the next ordinal grounds. Your "never guess which second one" holds by construction.
- Decline is `Okay — I won't mark those done. Nothing has been changed.`; the summary reports only what completed, with `Couldn't mark "X" done — it's no longer there.` per lost item.

Arch — the mechanism for your scope question is `ConversationContext.last_numbered_list` (in-memory, within-session), written by any render that numbers a list and read by the targets handler. Not serialized; a restart forgets it and the ordinal becomes the honest ask, never a guess.

#1951: `week_calendar`'s description now says it is a listing only (no conflict/overlap/free-time/availability check, no yes/no). Per the 09-29 rule that's a catalog change, so the full corpus is being re-scored now; the conflict row's ×6 runs with it. I'll report the number, not the expectation.

Verified how: `pytest` of the 1943 file + todo/reminder/dispatcher/confirm/enforcement suites → 355 passed; `tests/e2e/test_complete_todo_router_targets_live.py -m llm` → 1 passed, replies quoted from its output. Layer: unit + the in-process live path; not alpha (its flag lacks complete_todo). Denominator: your five strings, the scope rule, the one new list line.

— Lead
