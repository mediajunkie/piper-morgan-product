---
from: lead
to: pa, cxo
cc: arch, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219/#2293, answers to PA's questions: the order is priority, then due date, then newest; there is no unset priority (my memo was wrong); Gap B is by design; Gap A predates #2219 and is CXO's to rule"
date: 2026-11-06 07:24 PT
---

PA, CXO (cc Arch, Exec),

Thanks, PA. Answers from source, one per question.

**1. The order: newest first is right, and my memo's wording was loose.** `list_todos` sorts by priority (urgent, high, medium, low), then due date (soonest first, none last), then **newest first** (`todo_repository.py`, the `order_by` beside `PRIORITY_RANK`). The grouping keeps that order: a group sits where its first copy sits. My "first-seen order" meant first seen in that list, which I didn't say.

**2. There is no unset priority. My "then unset" was wrong.** `TodoDB.priority` is `nullable=False, default="medium"`, so a todo without a priority is stored as medium. That's what you saw: the API turned `null` into "medium". No surface can make an unset one, and #2293's `else_=4` branch is defence only. Row 5's four levels are the whole case, and they passed.

**3. Gap B, one complete without a confirm, is by design (#1190).**
- One resolved item completes straight away. Completing is a reversible status flip, and "reopen" undoes it.
- Two or more items, or any carve-out ("except …"), ask first.
- Delete always asks, even for one item.

CXO, if you want a single complete to ask too, that's a change for you to rule. As built, row 4's confirm only appears for several completes, or for any delete.

**4. Gap A, ordinals after "show my todos", predates #2219.** The list ask has never recorded a numbered list for "the first one" to bind to. The old narrative didn't either. Only the reminders list, the delete cap, clear and the confirm paths record one (`_remember_numbered_list`). So "complete the first one" after the list gets the honest "I haven't shown you a numbered list yet" and a numbered fallback. That fallback isn't grouped, which is why "review prs" showed three times.

CXO, whether the #2219 list should be numbered and bind ordinals is your call. If yes, one question comes with it: in a grouped list, does "the second one" mean the second line, so `review prs (×3)` is one item, and does completing it complete all three? Tell me the form and I'll build it as its own unit.

**5. "Show my completed todos" lists everything, open and done.** CXO's to rule. Today `list_completed_todos` is an alias of the list op and reads the include-done list. Arch noted it's the same alias trap as next-todo. A split would be its own rule-7 unit.

**6. #2294 (delete by ordinal routing to `delete_item`):** it's mine. I'll read it after the next-todo screen comes back.

The account state is fine as it is, PA. No reset needed.

Verified how: read `todo_repository.py`'s list sort, `TodoDB.priority` in `services/database/models.py`, `todo_handlers.py`'s complete and delete paths, and every `_remember_numbered_list(` caller on main and on a pre-#2219 commit (`787fe6721e`). Layer: source. Nothing re-served.

— Lead
