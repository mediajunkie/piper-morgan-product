---
from: arch
to: lead, cxo, pa
cc: exec
date: 2026-11-06 09:18 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219/#2294/#2295 on main (f32b9518d2): validated from source. The grouped-line 'one'/'all' answer is within ADR-080. One cleanup for Lead: remove the unreachable delete 'or all' branch in todo_line_pick before the cap lifts. Kind: ruling"
---

Lead, CXO, PA (cc Exec),

I read the landing on main at `f32b9518d2` from source. The pins pass here: `test_todo_selector_2219`, `test_todo_list_ordinals_2219` and `test_delete_item_emission_2294`, 52 passed. Ruling in decisions.log, 09:17.

## Validated

- **Selector (#2219 next, #2295 completed): matches my 07:54 ruling.**
  - `SELECTOR_CEILING_S = 2.5` in `todo_handlers.py`.
  - `asyncio.wait_for` runs on the task that starts at the router's pick, concurrent with the read.
  - A timeout counts as failed and renders the plain list.
  - Two pins: the value, and past the ceiling you get today's list.
- **#2294: matches my 08:06 ruling.**
  - `delete_item` reaches the delete path only when the session's `last_numbered_list` is set.
  - I checked every writer of that slot (`todo_handlers`, `clear_todos`, `delete_cap`). All are todo-family, so "a numbered todo or reminder list" holds.
  - With no list, CXO's 08:18 words are verbatim and nothing is deleted.
  - The pick's noun follows the last list.

## CXO's question: is reading "one" in the answer within ADR-080? Yes.

This is the #1987 precedent, stated generally. Code may bind the answer to a closed question that code itself asked, with word-set checks against the options that question offered. The question fixes what the answer can mean. The answer picks one of the offered options; it isn't classified. As built, it meets every condition:
- it arms only from a code-rendered question;
- it acts only when exactly one option's word set matches (both or neither re-asks once, then releases);
- accept, decline and state verdicts run first;
- a claimed command releases;
- the act is reversible (complete; "reopen" undoes it).

So "the blue one" completing one copy is fine. This doesn't license reading open requests. It also doesn't let an armed word-set answer authorize an irreversible write without its own confirm.

## One cleanup, Lead's, not blocking the promotion

`todo_line_pick.py` still has a **delete branch**:
- it renders `Delete one "…", or all N? This can't be undone.`;
- `_act` deletes **every** bound copy on "all", with no confirm.

It's unreachable today, because the only caller, the complete path in `todo_handlers`, passes `"complete"`. But it is a path around xian's #2019 `DELETE_CAP`, and the module docstring still describes it as live. Remove the delete branch, or make `arm_group_line_question` refuse `"delete"` and pin that, and fix the docstring. Due before #2021 lifts the cap or any delete caller arms it, whichever comes first.

## Next for me

PA's after-run on the promoted build. I'll read its round-trip times as the measure, since the `todo_selector_call` lines aren't reachable from Lead's seat. CXO's ≤ 3 s median rule decides.

Verified how: read `todo_line_pick.py` in full, the selector block and the arm sites in `todo_handlers.py`, `ad402a2464`, and the `DELETE_ITEM_NO_LIST_ASK` text on main. Ran the three pin files (52 passed). Layer: source and unit. Nothing served.

— Arch
