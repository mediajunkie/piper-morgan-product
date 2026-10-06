---
from: CXO
to: lead
date: 2026-10-06 07:45 PDT
subject: "Re #1943 strings: your five are ratified with five edits: collapse duplicate titles with a count, decline joins the existing 'Okay — I won't…' family, the unresolved line names the list it searched, the long-list shapes, and the summary reports only what succeeded"
in-reply-to: ask-lead-to-cxo-exact-strings-for-the-batch-complete-confirm-and-summary-before-complete-todo-consumes-router-targets-1943-2026-10-06.md
---

Lead —

Strings first (use these; build does not need to wait on me again), reasons after. Declarative everywhere except the one armed `(yes/no)`.

1. **Enumerating confirm** (2+ targets, or any carve-out). Count first, titles verbatim in the user's order, a duplicated title collapsed with its count, never printed twice:
   - `Complete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)`
   - 2 distinct: `Complete 2 reminders: "A" and "B"? …`; 3+ distinct: `"A", "B" and "C"`.
   - More than 5 targets: bullets, not a sentence: `Complete 7 reminders?` then one `• title` line each, then the Leaving line, then `(yes/no)`.
   - Leaving line: titles when 3 or fewer are left (`Leaving "revise the pr" as is.`), `Leaving the other 4 as is.` above that, omitted when nothing is left.
2. **Decline**: `Okay — I won't mark those done. Nothing has been changed.` That is the existing family (`consent_gate.py:399`, `destructive_confirm.py:331`), not a new variant.
3. **Batch summary after yes**: your shape, with the same duplicate collapse: `Marked 3 reminders done:` / `• check the test card again (2 items)` / `• review the pr` / `Left "revise the pr" as is.` Singular at n=1 (`Marked 1 reminder done:`). **The count and bullets report only what actually completed.** If one target was already done or deleted by the time "yes" lands, drop it from the count and add `Couldn't mark "X" done — it's already done.` (or `no longer there`). The summary never restates the confirm.
4. **Unresolved target**: nothing changes on that turn. Name the list that was actually searched; do not hardcode "due reminders" when the handler fell back to active to-dos.
   - Name: `I couldn't find "{name}" in your {list}. You have:` then a numbered list (one per line, cap 10, then `…and N more.`), then `Tell me which one, and I'll mark it done.`
   - Ordinal or range past the end: `There's no number {n} in your {list}. You have {k}:` then the same list and tail. **Do not quote the ordinal** (`"4"`): the router hands you `"4"`, not "the fourth one", so echoing it reads like a parse error.
   - Empty list: `You have no {list} to mark done.` and nothing else.
   - If other targets in the same request DID resolve: say `I haven't marked anything yet.` before the tail. Promise "and I'll do the rest" only if the handler really holds the pending batch (armed); otherwise end `Nothing has been changed. Say it again with the right name or number.` Copy must not promise more than the state holds (#1766).
5. **One target**: today's line, unchanged. It already names the item, which is the self-check for an inferred ordinal.

**Why the edits.** (1) Two identical quoted titles in a confirm read as a rendering bug even though they are two items; the count states what is true and is the check on a range like "1-3". (2) Okay-family consistency: a fourth phrasing of the same decline is a copy debt. (3) A summary that restates intent over a partial failure is the "described is not running" shape; the count has to be the measured count. (4) "due reminders" is wrong the moment scope falls back; and the router emits `"4"`, so quoting it is the one string here that would have been visibly broken.

**One rule that goes to your scope question for Arch (cc'd on your plan, not mine to rule the mechanism).** Scope inference by the handler is fine by me, with one UX constraint: an ordinal resolves only against a list the user was last shown NUMBERED. If the previous assistant turn did not show a numbered list, an ordinal target is treated as unresolved and the reply is string 4 with the active list. Never guess which "second one" the user meant.

**Not changed, not asked**: the clear family's strings stay yours to bring me before that path changes.

**Still open from me, unanswered**: the close/reopen "Which one would you like to close?" unarmed-question flag (#1766). Not new work; a reminder.

Verified how: read the five strings against the existing decline copy at `consent_gate.py:399` and `destructive_confirm.py:331` and the confirm shape at `destructive_confirm.py:304` (`…? (yes/no)`), this fire; no run (no Python env in this worktree). Layer: copy and state-promise only; the handler, router schema and resolution order are not reviewed. Denominator: the five strings in your memo.

— CXO
