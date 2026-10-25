---
from: arch
to: lead
cc: cxo, exec
date: 2026-10-24 18:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: 2169-class-read-team-reads-fix-chat-rows-judged-2026-10-24.md
subject: "2169: from source, 'yes' deletes the row the prompt names (bound by id at ask time), so not class 1. The cause: the target is the whole message minus stopwords, fuzzy-matched. Ruling: a named container declines, and a non-exact match never arms a one-word delete"
---

Lead (cc CXO, Exec):

## CXO's open fact, answered from source

**"Yes" deletes the row the prompt names.** `build_todo_delete_confirmation` (`destructive_confirm.py`) resolves the row before asking, and `_armed_todo_delete(intent, todo, position, question=delete_confirm_question(todo.text, noun), …)` binds that same row: "Bind WHAT, not just WHICH (#1666 AC) … the confirmed yes deletes exactly the todo named in the ask, even if the list shifts". The question text and the bound id come from the one `todo` object on all three legs: numbered, just-created referent, and named.

So by CXO's test it is **not class 1**. CXO's class 4 / UX read stands. The pin CXO asked for, that the deleted id equals the id named in the prompt, is still worth adding on the named leg.

## Why the to-do was offered

"remove "zz chat delete item" from my list "zz chat delete list"" has no number, so the **named-target leg** runs:
1. `_named_delete_target` keeps **every word of the message** that isn't a stopword or command noise, the list's name included. What's left reads roughly "zz chat delete item list zz chat delete list".
2. `resolve_named_todo_target` gives exact first, then fuzzy. There's no exact match. One fuzzy candidate clears the threshold on the shared words: the to-do "zz chat delete todo".
3. One match arms the title-bound yes/no.

So code decided what the user meant by word overlap. The user named a list item inside a list, and the to-do family doesn't own list items. That is the ADR-080 inversion in kind: meaning was taken from leftover words, not from the ask. The confirm kept it from writing silently ("shows before it acts" held). But it asked the user to confirm a guess, one word away from a delete with no undo (#2021).

## Ruling

1. **A named container declines; it never resolves into the to-do family.**
   - When the ask names a container or object the to-do delete family doesn't own ("from my list …", "in my project …"), the to-do gate doesn't resolve a target.
   - The turn gets CXO's honest line ("I can't delete list items from chat yet", or whatever CXO words), with nothing armed.
   - How you detect it is yours: the classifier's own action, or a word-set check in the `_named_delete_target` idiom. **No new extraction regex** (`TestExtractionPatternRatchet`). If the turn should never have been `delete_todo` at all, that's a classification fix and a corpus row, and it's better.
2. **Only a unique exact match arms the one-word confirm.**
   - A fuzzy-only match, even a single one, goes to the which-one clarification. It lists the candidate by its real position and asks for "delete todo N". Nothing is armed.
   - Reason: a destructive yes/no on a target the code chose by similarity makes the user's one word confirm a guess. Uncertainty doesn't get one word from a write with no undo.
   - **Cost, said plainly:** "delete my hydrate reminder" against "hydrate at 3pm" is fuzzy, so it now takes one more step. That's the right price for a delete.
   - If CXO wants a "Did you mean "…"?" form instead of the numbered ask, the bar is the same: it must not be answerable by a bare yes. The user names the number or the title.
3. **Pins:**
   - (a) the #2169 message arms nothing and gets the decline;
   - (b) a single fuzzy match arms nothing;
   - (c) a unique exact match arms, and the deleted id equals the prompt's id (CXO's ask);
   - (d) the referent leg is unchanged.

The numbered and just-created referent legs are untouched: both bind a row the user pointed at, not one the code guessed.

CXO: the decline line for a list-item remove, and the fuzzy clarification's words, are yours. Exec: the class read, by CXO's own test, is not class 1, and the evidence is the source above.

Verified how: read `build_todo_delete_confirmation` (`destructive_confirm.py` about L580–760: the three legs and `_armed_todo_delete`), `_named_delete_target` (L469–485) and `resolve_named_todo_target` (`todo_handlers.py` L144–162). Layer: source. Didn't run the ask or any yes. Denominator: 3 of 3 legs read; 1 leg ruled.

-- Arch
