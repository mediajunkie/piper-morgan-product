"""Issue 2046 (CXO, 2026-10-16): the reminder/to-do delete copy that names
the user's object, held in ONE place.

CXO's two rulings (the issue's copy comment and her 10-16 08:16 memo):

1. **Ordinals with no numbered list bound.** When the user points at
   positions ("delete the first two reminders", "delete reminder 1") and
   this session has shown no numbered list, Piper never answers "There's no
   number 1" (numbers the user never saw). It shows the list, numbered, one
   item per line, and asks::

       I haven't shown you a numbered list yet. Here are your reminders:

       1. "buy milk"
       2. "call mom"

       I can delete one at a time for now. Tell me which one.

   The middle sentence is the issue-2019 cap (``delete_cap``), said only
   when more than one item was asked for; a single ordinal ends on "Tell me
   which one." Showing the list BINDS it (the caller records it as the
   session's last numbered list), so the next "delete reminder 1" resolves
   against exactly these numbers. "Tell me which one." is an instruction,
   not a yes/no question: nothing is armed.

2. **One noun.** #2219 (CXO 2026-11-05 19:25) superseded #2046's default: the
   list, the confirm and the result say "todo" (the page is titled "Todos"),
   unless the person said "reminder" or "remind", and their own word always
   wins. One spelling, "todo", no hyphen. A one-item delete confirm reads
   ``Delete the todo "buy milk"? (yes/no)``, or ``Delete the reminder …`` when
   the person said reminder.

The noun VALUE follows the codebase's existing convention (#1569,
``reminder_clear.ClearAsk.noun`` / ``delete_todo_pick``): ``"reminder"`` or
``"todo"``. :func:`noun_word` is the display spelling CXO's copy uses
("todo"). Detection is a word-SET check over the user's message, never a
message-parsing regex (``TestExtractionPatternRatchet``).
"""

from __future__ import annotations

import string
from typing import Optional, Sequence

# --- CXO's strings (issue 2046) -------------------------------------------

NO_LIST_OPENING = "I haven't shown you a numbered list yet. Here are your {plural}:"
DELETE_ONE_AT_A_TIME = "I can delete one at a time for now."
TELL_ME_WHICH_ONE = "Tell me which one."
# The one-item delete confirm, every leg. Rendered by delete_confirm_question.
DELETE_CONFIRM_QUESTION = 'Delete the {noun} "{title}"?'

# How many rows the no-list reply shows (the same cap as the unresolved
# listing it replaces; only the shown rows are bound).
NO_LIST_MAX_SHOWN = 10

# #2219 (CXO 2026-11-05 19:25): "remind me" is the person saying reminder too.
_REMINDER_WORDS = frozenset({"reminder", "reminders", "remind"})
_TODO_WORDS = frozenset({"todo", "todos", "to-do", "to-dos"})


def _words(message: Optional[str]) -> set:
    return {w.strip(string.punctuation + "“”‘’").lower() for w in (message or "").split()}


def said_noun(message: Optional[str]) -> Optional[str]:
    """The noun the user said: ``"reminder"`` (wins a mixed mention, #1569),
    ``"todo"``, or None when they named neither."""
    words = _words(message)
    if words & _REMINDER_WORDS:
        return "reminder"
    if words & _TODO_WORDS:
        return "todo"
    return None


def copy_noun(message: Optional[str], default: str = "todo") -> str:
    """CXO's rule (#2219, 2026-11-05 19:25, superseding #2046's default): "todo",
    unless the person said "reminder" or "remind"; their own word always wins."""
    return said_noun(message) or default


def noun_word(noun: str) -> str:
    """Display spelling: "reminder" | "todo" (#2219: no hyphen, everywhere)."""
    return "todo" if noun == "todo" else "reminder"


def noun_plural(noun: str) -> str:
    return f"{noun_word(noun)}s"


def delete_confirm_question(title: str, noun: str = "todo", leaving: str = "") -> str:
    """``Delete the reminder "buy milk"? (yes/no)`` — the one-item confirm on
    every delete leg (numbered, by title, just-created referent, pick)."""
    q = DELETE_CONFIRM_QUESTION.format(noun=noun_word(noun), title=title)
    if leaving:
        q += f" {leaving}"
    return q + " (yes/no)"


def delete_summary_phrase(title: str, noun: str = "todo") -> str:
    """The confirm's ``summary`` (and so its decline, "Okay — I won't …")."""
    return f'delete the {noun_word(noun)} "{title}"'


def no_list_reply(texts: Sequence[str], noun: str, tail: str) -> str:
    """CXO line 1: the opening, the numbered list (quoted titles, one per
    line), then ``tail``. Blank lines around the list: the chat page renders
    Markdown, and a line straight after a list item renders INSIDE it (the
    #2002 run-together)."""
    shown = list(texts)[:NO_LIST_MAX_SHOWN]
    items = [f'{i}. "{t}"' for i, t in enumerate(shown, 1)]
    if len(texts) > len(shown):
        items.append(f"…and {len(texts) - len(shown)} more.")
    opening = NO_LIST_OPENING.format(plural=noun_plural(noun))
    return opening + "\n\n" + "\n".join(items) + "\n\n" + tail


def delete_no_list_tail(requested: int) -> str:
    """The delete tail: the issue-2019 cap sentence when more than one item
    was asked for, then the instruction."""
    from services.intent_service.delete_cap import exceeds_delete_cap

    if exceeds_delete_cap(requested):
        return f"{DELETE_ONE_AT_A_TIME} {TELL_ME_WHICH_ONE}"
    return TELL_ME_WHICH_ONE
