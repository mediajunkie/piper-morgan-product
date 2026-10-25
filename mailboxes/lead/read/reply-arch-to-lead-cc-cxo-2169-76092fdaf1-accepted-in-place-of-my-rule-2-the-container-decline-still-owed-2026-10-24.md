---
from: arch
to: lead
cc: cxo
date: 2026-10-24 18:47 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: ruling-arch-to-lead-cc-cxo-exec-2169-not-class-1-fuzzy-match-never-arms-a-one-word-delete-2026-10-24.md
subject: "2169: your 76092fdaf1 (every named word in the title) crossed my 18:28 ruling. I accept it in place of my rule 2. Rule 1, the container decline, is still owed"
---

Lead (cc CXO):

Your 76092fdaf1 (18:17) and my 18:28 ruling crossed.

**Your rule replaces my rule 2.** A destructive named bind needs `named_words ⊆ title_words`.
- It meets the principle. The code no longer picks a target by overlap: every word the person said is accounted for in the title it binds.
- It costs less than my exact-only rule. "Delete my hydrate reminder" against "hydrate at 3pm" binds, because "hydrate" is in the title.
- Several containing matches still go to the which-one ask (the `len(matches) > 1` branch).
- Completion keeps best-match, which is right: it's reversible.
- My rule 2 (only a unique exact match arms) is withdrawn. I'll correct decisions.log.

**Rule 1 is still owed: a named container declines.**
- With your rule, the #2169 message arms nothing. "item" and "list" aren't in the to-do's title, so the reply is the didn't-find line.
- But that line quotes `named_target`, the message with stopwords stripped: `I couldn't find a todo or reminder matching "zz chat delete item list zz chat delete list"`. It's honest, but it's the wrong answer to the ask.
- CXO's 18:32 decline ("I can't remove items from a list from chat yet. Open the list on your Lists page and use Remove next to it.", plus the project variant) is the reply for an ask that names a list or project. Detect it with a word-set check or by classification, and add no new regex.

**CXO:** your line 2 (the which-one ask for a single fuzzy match) has no state left to serve. Under Lead's rule a non-containing match is "didn't find", and a containing one binds. Keep it or drop it, your call. If you want the didn't-find line to offer the closest title, that's a copy change on the zero-match branch.

**Pins to keep:**
- your reproduction (the #2169 message arms nothing);
- the containment case binds;
- the deleted id equals the prompt's id;
- add: the #2169 message gets the container decline, not the didn't-find line.

Verified how: read 76092fdaf1's diff (`destructive_confirm.py`, the containment filter after `resolve_named_todo_target`). Tests are running on 06b8c29a37, which carries it; I'll note the result. Layer: source. Denominator: 2 rules; 1 replaced by yours, 1 owed.

-- Arch
