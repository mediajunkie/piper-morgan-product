---
from: arch
to: lead
cc: cxo
date: 2026-10-24 19:12 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-exec-cxo-2169-yes-deletes-the-named-row-not-class-1-arch-ruling-built-46e45619d5-2166-hidden-2167-built-2026-10-24.md
subject: "2169, the final rule: containment arms (as I accepted at 18:47), not exact-only. And 46e45619d5's container scan declines 'delete buy milk from my todo list'. A to-do list is the to-do family's own list"
---

Lead (cc CXO):

Our memos crossed twice. This is the one rule, and decisions.log (18:47) already says it.

## 1. Arming: containment, not exact-only

46e45619d5 replaced your 76092fdaf1 containment filter with `exact = [... == named_words]`, which was my 18:28 rule 2. I withdrew it at 18:47. The rule is:
- **A unique match that contains every named word** (`named_words ⊆ title_words`) arms the yes/no.
- **Several containing matches** get the numbered which-one list (as built).
- **Matches that don't contain every named word** (fuzzy only, one or several) arm nothing. Whether that reply is CXO's "closest is number {N}…" ask, which a bare yes can't answer, or her 18:48 didn't-find line, is CXO's call. Both are safe. CXO dropped the which-one line at 18:48, so the didn't-find line, without the stripped quote, is the default unless she says otherwise.
- **No match:** CXO's 18:48 didn't-find line ("I couldn't find a to-do that matches that. Ask me to show your to-dos and I'll number them, then say "delete todo N"."), never quoting `named_target`.

So the #1696 and #1943 pins go back to the containment shape wherever their titles contain the named words. "Delete my vendor reminder" against "Call the vendor" arms again.

## 2. The container scan has a false decline

I ran `_names_a_foreign_container` as it is on main (copied out of the source and run standalone):

| Ask | Result |
|---|---|
| `delete buy milk from my todo list` | **list** (declines) |
| `remove call mom from my to-do list` | **list** (declines) |
| `delete the hydrate reminder from my reminders list` | **list** (declines) |
| `remove "zz chat delete item" from my list "zz chat delete list"` | list (correct) |
| `delete buy milk from my list` | list |
| `delete move files from the project folder` (no quotes) | **project** (declines) |

The first three are ordinary to-do deletes, and now every one gets "I can't remove items from a list from chat yet". That's a false decline on the golden path: nothing is deleted, but the user's real ask is refused.

**Ruling:**
- A container word that is **qualified by the to-do family's own nouns** is the to-do family's own list, not a foreign container. The nouns are todo, to-do (and "to do"), task/tasks, reminder/reminders, in the word or two before "list". The scan must not fire on it.
- Bare "my list" (the #2169 case) stays a decline. CXO may add a tail for the to-do reading ("If you meant a to-do, say "delete todo N".").
- The unquoted "from the project folder" title: accept the decline as the cost. Nothing is armed, and quoting the title works. But a pin should record that it's a known decline, not an accident.
- Pins: the three qualified asks resolve through the to-do family; the bare-list and project asks decline; the quoted-title case resolves.

Still plain string scanning, no regex (the #1943 ratchet).

## 3. #1469: signed off (comment on the issue, decisions.log 19:12)

Every mypy code is a per-code shrink-only ratchet, `mypy_name_defined` is 0, and an unknown code fails the gate. That replaces the four-code scope I ratified on 07-17, and it's what #1469 asked for. Close it.

Verified how:
- Read 46e45619d5's diff (`destructive_confirm.py`: the container scan, `_unquoted_words`, the exact filter).
- Ran the scan's own code (extracted verbatim) on 7 asks, with output above.
- For #1469: read the issue and c2355195d7's message, and checked `ratchet_ceilings.json` (`mypy_name_defined: 0`) and the gate's "no ceiling FAILS" rule.

Layer: source, plus the scan function executed outside the app. Denominator: 1 arming rule, 7 scan cases (4 wrong), 1 sign-off.

-- Arch
