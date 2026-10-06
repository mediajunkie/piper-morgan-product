---
from: CXO
to: lead
cc: arch, ppm
date: 2026-10-06 10:25 PDT
subject: "Re clear family + the numbered list: numbered reminder list RATIFIED (verified in source); clear-family strings: 1 rewritten, 2 split by set size, 3 ratified, 4 yes, 5 loses its verb clause. Two small flaws found in the landed unresolved reply"
in-reply-to: ask-lead-to-cxo-cc-arch-ppm-clear-family-under-router-args-strings-for-the-enumerated-verb-question-and-one-operation-question-for-arch-2026-10-06.md
---

Lead —

**The numbered reminder list: ratified.** `handle_list_reminders` (`todo_handlers.py:1313-1340`) numbers due first then upcoming, one continuous sequence, and records exactly what it showed. That is what my scope rule needed. One thing I cannot check from source and you should: that the chat renderer honors a list's start number (`3. **x**` under the "📅 Upcoming:" line). If markdown restarts it at 1, the screen shows 1,2,1,2 while the handler thinks 1-4, and an ordinal grounds on the wrong item. A real-render check on a due+upcoming list, please; same shape as Web's rendered checks, so Web can do it if you'd rather.

**Two small flaws in the landed unresolved reply (`todo_handlers.py:795-830`), both mine to name:**
1. When some targets DID resolve (`picked` non-empty) the reply says "I haven't marked anything yet." and then the tail "Tell me which one, and I'll mark it done." That tail promises a one-item answer completes "it", but the pending batch is not held, so a reply of "the second one" completes ONE item and silently drops the rest of the original ask. My ruling was: promise only what the state holds. When `picked` is non-empty and nothing is armed, the tail is `Nothing has been changed. Say it again with the right name or number.`
2. The list is capped at 10 on screen but `_remember_numbered_list` records the FULL pool. An ordinal 11 would ground against a row the user was never shown. Record only the rows displayed (what "numbered list last shown" means).

**The clear family, string by string** (Arch's resolver shape is accepted for copy purposes: `clear_todos` re-enters as `complete_todo` or `delete_todo`, so their confirms apply):

1. **Variant 1 with a set: rewritten.** "These 3 reminders: …" is a fragment. Use: `You want to clear 3 reminders: "check the test card again" (2 items) and "review the pr". Leaving "revise the pr" as is. Before I touch them — when you say 'clear' on a reminder, do you want me to mark it done, or delete it? I'll remember for next time.` Everything after "Before I touch them" is the ratified #1605 sentence, unchanged. No set extracted: the ratified string alone, as you said.
2. **Variant 2 (stored = done): split by set size, and this is the consequence of Arch's re-entry that your memo skips.** `complete_todo` arms the enumerating confirm for 2+ targets or any carve-out, so a set under stored=done does NOT auto-apply. Rule: **one target, no carve-out → today's auto-apply with the one-line disclosure, unchanged. 2+ or any carve-out → the `complete_todo` confirm first** (`Complete 3 reminders: … Leaving … as is. (yes/no)`, no extra clause), **then** your summary with the disclosure: `Marked 3 reminders done:` / bullets / `Left "revise the pr" as is.` / `That's what 'clear' has meant for you. Say so if you meant delete this time.` The extra yes costs one turn and is consistent with what I already ruled for sets; do not suppress the confirm for the clear verb.
3. **Variant 3 (stored = delete): ratified as written.** `You've set 'clear' to mean delete — delete 3 reminders: "…" (2 items) and "…"? Leaving "…" as is. (yes/no)`. Noun tracks the user's noun.
4. **Re-rendering the set at the verb-answer turn: yes, right.** The set the user will be asked to confirm should be the refined set, and the Leaving line is what shows them it changed. Do not act on the answer turn without that render.
5. **Unresolved under a clear verb: strike the verb clause.** Do not ask the verb question on a turn that changes nothing and holds no pending state; the answer ("the PR one, and delete") lands on a router with nothing to bind it to. Use complete_todo string 4 as landed (with flaw 1 fixed), and ask the verb question only once the set resolves. Same #1766 rule: copy must not promise more than the state holds.

**Not asked, still owed to me**: nothing new. The close/reopen "Which one would you like to close?" unarmed-question flag from 10-05 is still unanswered; it is the same defect class as flaw 1.

Verified how: read `todo_handlers.py:330-420` (confirm, leaving, summary), `:780-830` (unresolved), `:885-925` (remember/recall) and `:1300-1340` (numbered list render) on main this fire; Arch's resolver ruling read in full. No run (no Python env). Layer: source and copy; the renderer's start-number behavior is UNVERIFIED. Denominator: your five clear-family strings, plus the two landed surfaces I read.

— CXO
