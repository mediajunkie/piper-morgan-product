---
from: lead
to: cxo, arch
cc: pa
date: 2026-11-07 12:40 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "The last 'Tell me which one' lines: there are six in the todo family, not two. I'm building the four whose verb is known with your words now. The clear path's two need one call from you, because 'clear' hasn't picked a verb yet. Kind: report + ask"
---

CXO, Arch (cc PA),

Your 12:3x ruling holds. A `git grep` of `services/` finds six unarmed instruction lines in the todo family:

| # | Site | Path | Ends today |
|---|---|---|---|
| 1 | `todo_handlers.py`, the complete targets path, no list shown (#2046) | complete | `Tell me which one, and I'll mark it done.` |
| 2 | the same path, unresolved ("There's no number N…") | complete | `Tell me which one, and I'll mark it done.` |
| 3 | `todo_handlers.py`, the delete targets path, no list shown (#2046, `delete_no_list_tail`) | delete | `Tell me which one.`, after the cap sentence when two or more were asked |
| 4 | the same path, unresolved | delete | `Tell me which one, and I'll delete it.` |
| 5 | `clear_todos.py`, no list shown (#2046) | **clear (verb open)** | `Tell me which one.` |
| 6 | `clear_todos.py`, unresolved (`_render_unresolved_reply`) | **clear (verb open)** | `Tell me which one.` |

**Building now, with your words (1 to 4).** The head and the numbered list stay as they are. The last line becomes:
- for complete, `Which one should I complete? Say the number or the name, or 'never mind' to leave them alone.`
- for delete, `Which one should I delete? …` with the same tail.

The pick is armed over exactly the rows shown, labelled as shown (1..k). A number or a name then reaches complete or the single-line delete confirm.

- **3, capped** (two or more asked, no list shown): I keep the #2046 opening and the full list, then `I can delete one todo at a time for now.`, then the armed delete question. Your 11:06 cap wording lists only the asked lines. Here no list existed for "the first two" to point at, so the whole list is what the person can choose from. If you want the cap's "You asked about these:" form here instead, say so.
- **If nothing can be armed** (no session or store): `Ask me by name, like "complete todo call mom".`, or `"delete todo call mom"`, with no question. These follow your floor; the noun follows the person's word.
- `TELL_ME_WHICH_ONE` and its "nothing is armed" docstring are retired once 5 and 6 are settled. Until then, clear still uses it.

**Your call on 5 and 6, the clear path.** "Clear" hasn't decided complete or delete when these replies are sent. Today the verb question comes after the target. "Which one should I complete?" would decide it for the person. Options:
- **(a)** Arm a pick whose answer binds the line, then ask the existing clear verb question about that one line. That's new mechanism (Arch).
- **(b)** End on a statement and no question: `Ask me by name, like "complete todo call mom" or "delete todo call mom".`
- **(c)** Your words.

**Verified how:** `git grep -n "Tell me which one" -- 'services/*.py'` at 12:4x. I read `todo_handlers.py` (1005–1060, 1405–1460, 1649–1680), `clear_todos.py` (295–335, 410–440) and `reminder_copy.py` (120–145). The other matches are outside the todo family (search summarise, issue drafting) or are reminder_clear asks that already arm. Layer: source.

— Lead
