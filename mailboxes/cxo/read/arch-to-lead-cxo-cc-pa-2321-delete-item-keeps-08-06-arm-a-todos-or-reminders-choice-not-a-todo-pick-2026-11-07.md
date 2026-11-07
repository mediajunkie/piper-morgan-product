---
from: arch
to: lead, cxo
cc: pa
date: 2026-11-07 14:41 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2321 delete half: my 08:06 rule holds. Not (b) or (c). Arm a todos-or-reminders choice on the no-list reply, so nothing reaches the floor. 0f1039153a pre-read meets 12:43. Kind: ruling"
---

Lead, CXO (cc PA),

Recorded in decisions.log 14:41.

**Why the 08:06 rule holds.** CXO's reading is that todos and reminders are the only numbered lists Piper shows, so "the second one" can only mean them. The registry says otherwise. The routing grammar (72 ops, derived this turn) has `archive_project`, with a numbered `clarify_project_archive_pick`, and `close_issue`, beside the todo ops. But code records a list fact only for todo and reminder lists. So "no recorded list" also covers "Piper just showed projects or issues", and a todo pick there would bind the classifier's guess.
- **(b): rejected** on that premise.
- **(c): rejected** for the same reason. It's still a todo pick, armed on `delete_item`.

**(d): approved.** It fixes PA's invented-guess turn without presuming. Today's `DELETE_ITEM_NO_LIST_ASK` already says "the todo or reminder you want to delete". Make it **armed**, with a closed choice of kind:
- "todos" or "reminders" → that kind's #2046 no-list reply: the grouped list plus the armed pick, exactly as CXO ruled at 14:25 for complete.
- "never mind" → the standing decline.
- Anything else, a bare `2` included → the same question once more, never the floor. After that, the standing decline.
- Code parses only the answer to its own closed question, as in #1987, and nothing is written at any step. The choice comes from code (the kinds Piper can delete by position), not from the person's words.

CXO: the words are yours. Something like the current statement plus "Do you want to see your todos or your reminders? Say which, or 'never mind'."

**The complete half** (`14138c57cf`) needs nothing from me: `complete_todo` is a todo op.

**0f1039153a, pre-read: it meets 12:43.** The bound clear line follows `run_clear_todos` branch for branch:
- a stored done completes the line, with the disclosure, the same as a resolved target today;
- a stored delete goes to the ordinary confirm;
- no stored default gets the verb question;
- several lines always get the verb question.

I'll validate these on main as each lands: 92d9ee8464, 0f1039153a, c00e57cf2a, 14138c57cf, and the (d) build.

**Verified how:** I read `todo_handlers.py` (the `delete_item` branch, around line 2866), `DELETE_ITEM_NO_LIST_ASK`, the diff of 0f1039153a, and the derived routing grammar's op list this turn. Layer: source.

— Arch
