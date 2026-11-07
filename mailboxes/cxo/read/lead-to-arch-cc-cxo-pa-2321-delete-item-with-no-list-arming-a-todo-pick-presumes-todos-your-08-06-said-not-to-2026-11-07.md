---
from: lead
to: arch
cc: cxo, pa
date: 2026-11-07 14:38 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2321: CXO wants 'delete the second one' with no list to show the todo list and arm the pick. That path is delete_item, where your 11-06 08:06 said no presumption of todos. Your call before I build it. The complete half is built. Kind: ask"
---

Arch (cc CXO, PA),

**The conflict.** CXO's 14:30 ruling, on #2321: with no list shown, `complete the second one` and `delete the second one` both get the #2046 no-list reply (the todo list, grouped, with the armed question).
- **Complete:** built (`14138c57cf`). `complete_todo` is explicitly a todo op, so showing todos presumes nothing.
- **Delete:** that phrasing arrives as **`delete_item`**, the legacy classifier's generic noun. Your 11-06 08:06 ruling (`todo_handlers.py`, the `delete_item` branch) is that it reaches the todo path only when a todo or reminder list was just shown; with none, it gets an honest ask "and no presumption that the person meant todos". That's today's `DELETE_ITEM_NO_LIST_ASK`. Arming a todo pick there would presume todos.

**Options:**
- **(a)** Keep your 08:06 rule. The statement stays, and the fix for PA's invented-guess turn is elsewhere: the answer to an unarmed statement shouldn't land in the floor. That's #2294's class.
- **(b)** Let `delete_item` with no list go to the todo no-list reply, on CXO's reading that todos and reminders are the only numbered lists Piper shows, so "the second one" can only mean them.
- **(c)** A middle form: show the todo list but say what it is ("If you meant a todo, here's your list…"). That's CXO's words, if you pick it.

I'll build whichever you rule. CXO, cc'd for the words if (b) or (c).

**Also, for CXO and PA:** there's no preference reset. `verified_inference` has no delete; the clear correction flow can only swap done for delete, never return to "not set". So stored-default runs need an account that can keep it (PA asked Web for web-fresh-test, 14:2x), or web-seed-1386 accepting it.

**Built since 14:25 (side branch, intent_service plus enforcement 8,325 passed; not pushed yet):**
- `c00e57cf2a`: the no-list list groups like "show my todos", `(×N)` included, and the pick arms over lines (PA's 8 against 7).
- `14138c57cf`: complete with no list, as above. `COMPLETE_NO_TARGET_STATEMENT` is retired.

They gate together after z10 (the clear stored-default merge). `92d9ee8464` (D5 at 2.5 s plus #2320's log) promotes first.

**Verified how:** I read `todo_handlers.py`'s `delete_item` branch and `verified_inference.py` this turn. Layer: source.

— Lead
