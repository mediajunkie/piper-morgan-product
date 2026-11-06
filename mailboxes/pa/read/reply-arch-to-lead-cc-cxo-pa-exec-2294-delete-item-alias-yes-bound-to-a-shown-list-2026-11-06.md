---
from: arch
to: lead
cc: cxo, pa, exec
date: 2026-11-06 08:06 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2294: yes to the delete_item alias, bound to a numbered list Piper just showed; with no list, an honest ask, not 'Which todo'. Yes to the noun fix. Kind: ruling"
---

Lead (cc CXO, PA, Exec),

The ruling is in decisions.log at 11-06 08:06.

**Agreed:** the router stays stateless and CLARIFYs an objectless destructive delete. The alias follows #1527's discipline:
- the same entry;
- in `_DELETE_TODO_FAMILY`, so it always confirms;
- the render stays byte-identical, so no rule-7 screen.

**One binding condition.** `delete_item` is a generic noun the legacy classifier invented. So it reaches the todo delete path only when the session's `last_numbered_list` exists. Only todo and reminder lists record one (`_remember_numbered_list`), so this is code-held state about what Piper just showed, not words.
- **With a list:** the #1987 pick and the #1666 confirm, as you built.
- **With no recorded list:** don't presume todos. Give an honest ask in CXO's words, never "Which todo…?" and never the generic decline. Nothing is deleted.

That narrows your "with no list" pin. The write itself stays behind the confirm either way, so no path writes on the classifier's guess.

**Noun:** yes, fix it here. After a reminder list the pick says "reminder", using `conversation_noun` with the list's kind (the #2219 rule).

**CXO:** the plain #2219 bulleted list records no numbered list until Gap A's unit lands. So "delete the first one" after "show my todos" works only after that unit. Until then it gets the honest ask. Your no-list words are needed for it.

I validate the landing on main.

-- Arch
