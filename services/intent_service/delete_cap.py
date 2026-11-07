"""Interim one-item cap on todo/reminder deletes (issue 2019).

xian's ruling (2026-10-14): no irreversible bulk delete until soft delete with
undo exists (issue 2021; Arch's design note
``docs/internal/architecture/design-records/design-note-todo-soft-delete-undo-2026-10-14.md``
holds the exit criteria that lift this cap). PPM's interim (B), Arch's
placement: the cap lives in the DELETE HANDLERS, not the router allowlist, so
every way into a delete gets it.

When the RESOLVED set has more than one item, Piper arms no delete carrier,
deletes nothing, and answers with CXO's capped copy (the issue's copy comment,
2026-10-14), which names the items in the order the user sees them and ends
on the same "Nothing has been changed." the N5 decline uses. A single delete
keeps its existing named confirm; mark done on a bulk set stays uncapped.

#2318 (CXO 11-07 09:2x; Arch 09:24, mechanism): where the cap can bind an answer,
it asks an ARMED question instead (``delete_todo_pick.capped_pick_question``, the
#1987 pick over the capped lines, labelled as the person saw them), so "2" or the
name reaches the single-line confirm. The 10-14 closing instruction "Tell me which
one to delete first." stays only where nothing can be armed.

The copy lives HERE, in one place; every capped site calls
:func:`capped_delete_reply`. Callers (see the issue-2019 session log for the
full entry-path map): ``todo_handlers.handle_delete_todo_targets`` (ask and
confirmed re-entry; the ``clear_todos`` re-entries land here),
``delete_todo_pick.handle_delete_todo_pick_turn`` (an answer naming several
candidates), and ``reminder_clear``'s bulk-delete arms (explicit bulk,
variant 3, the verb answer, the ALWAYS_ASK this-time branch, the correction
turn) plus its confirmed sink ``run_clear_reminders_delete_workflow``.
"""

from __future__ import annotations

from typing import Any, Optional, Sequence

# The most items one delete may touch while the cap holds. Lifted (with this
# module) once soft delete + undo is live (issue 2021).
DELETE_CAP = 1

# intent_data marker on every capped turn (observability; tests pin it).
DELETE_CAPPED_FLAG = "delete_capped"


def exceeds_delete_cap(count: int) -> bool:
    """True when a resolved delete set is larger than the cap allows."""
    return count > DELETE_CAP


def capped_delete_reply(
    texts: Sequence[str], noun: str = "reminder", copies: Optional[Sequence[int]] = None
) -> str:
    """CXO's capped reply, verbatim, with the resolved items numbered 1..N in
    the order the user sees them. ``noun`` is the kind word the calling path
    already uses ("reminder" or "todo"). ``copies`` (#2219, CXO 11-06 09:16): an
    item that is one copy of a grouped list line shows the line's count as the
    list showed it, ``"review prs" (×3)``; 1 or absent shows no count."""
    counts = list(copies) if copies is not None else [1] * len(texts)
    lines = [f"I can delete one {noun} at a time for now. You asked about these:"]
    lines += [
        f'{i}. "{text}"' + (f" (×{n})" if n > 1 else "")
        for i, (text, n) in enumerate(zip(texts, counts), 1)
    ]
    # Blank line before the instruction: the chat page renders Markdown, and a
    # line straight after a list item would render inside it (#2002).
    return "\n".join(lines) + "\n\nTell me which one to delete first. Nothing has been changed."


def remember_capped_list(
    session_id: Optional[str],
    principal: Any,
    ids: Sequence[Any],
    texts: Sequence[str],
    kind: str,
) -> None:
    """Record the capped list as the session's last NUMBERED list, so the
    user's follow-up ("delete the first one") binds against the numbers they
    were just shown. Context only: this arms nothing. Best-effort, like every
    other numbered-list write."""
    from services.intent_service.todo_handlers import TodoIntentHandlers

    TodoIntentHandlers._remember_numbered_list(
        session_id, principal, kind, [str(i) for i in ids], list(texts)
    )
