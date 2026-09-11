"""#1651 — the standup's closing offer BINDS its referent (overdue-todo action).

PM live 2026-08-18: the standup closed with "Want me to … mark that overdue
todo done?", PM accepted verbatim ("Yes mark the overdue todo done."), and the
acceptance fell to the complete_todo handler's literal text matching — which
searched todo TITLES for the word "overdue" and failed ("I couldn't find a
todo matching 'overdue'"). Family: teach-then-deny (#1571) / offer-context-loss
— the standup had just computed WHICH todo was overdue and then threw the
referent away.

THE FIX (the reminder-clear / drafted-issue idiom, mirrored not reinvented):
when the standup's closing copy offers an action on a SPECIFIC item, the offer
rides the EXISTING #846 session-scoped pending-offer store with that item's id
BOUND at offer time — so acceptance dispatches on the bound id and never
re-parses the user's phrasing.

- **Arm** (``build_overdue_todo_offer``): ``_handle_standup_query`` resolves
  the user's overdue todos (owner-scoped, the same ``TodoManagementService``
  read every todo surface uses) after rendering a NON-EMPTY report, and arms
  ONE offer bound to the single strongest referent — the MOST overdue todo
  (earliest due date). If more are overdue the copy states the count honestly
  and still names its single bound referent — never an unbound "that todo".
- **Accept** ("yes" / "Yes mark the overdue todo done."): the generic
  offer-acceptance seam dispatches ``STANDUP_COMPLETE_TODO_WORKFLOW``
  (registered ``action_triggered=False`` — offer-seam only, the
  verify_inference/#1190 pattern), which completes the BOUND todo id via
  ``TodoManagementService.complete_todo`` — no title matching anywhere.
- **Decline** ("no"): the generic decline path answers with the stored
  honest copy; nothing fires, the todo stays.
- **State question** (#1739, adopted 2026-09-11 — PM live: "are we done with
  that standup?"): the answer turn consults ``evaluate_acceptance`` at this
  workflow's registry-declared axes; a STATE_QUESTION verdict never fires and
  never silently drops the arm. A question naming this offer's own referents
  (the standup / the bound todo) is answered AT the seam by
  :func:`state_question_reply` — honest status + the stored ask re-rendered —
  because normal processing demonstrably misreads it as a completion attempt
  (the classifier's fuzzy title match answered PM's live question with
  "I couldn't find a todo matching 'that standup?'"). Other questions keep
  the confirm-tier shape: visible re-arm, normal processing answers, the ask
  restates as a suffix.
- **Off-intent**: the pop already cancelled the offer (the #1529 off_intent
  tier); the new message routes normally. The #1631 prose floor applies via
  the predicate (PASS for prose-shaped turns), so a long free-text reply
  neither fires nor drops the offer's action beyond the pop's abandonment.

Interplay with #1591 (one ask per turn, one-slot #846 store): when this offer
arms, the mode read-back / interview invitation is NOT armed on the same turn
— the store holds one pending ask, and a bound action on the user's own data
outranks a mode nudge that honestly repeats on a later report (CXO: the
invitation is cheap and recurring by design). The EMPTY-report branch is
untouched: PPM's empty rule keeps the invitation leading there.

⚠️ COPY SEAM: the strings below are Lead-drafted mechanism copy at this seam
(the reminder_clear precedent); CXO owns the voice — adjust wording here, not
at call sites. Tests pin the mechanism-critical parts (the named referent, the
yes/no shape), not every word.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

from services.utils.datetime_utils import ensure_utc

logger = structlog.get_logger(__name__)

# pending_action ``kind`` marker (the #1190 carrier is action-agnostic; kind is
# how seams recognize an offer family without a parallel store).
STANDUP_TODO_OFFER_KIND = "standup_todo_offer"

# Offer-acceptance-only workflow (registered in workflow_entries with
# action_triggered=False — the classifier/rail can never emit it).
STANDUP_COMPLETE_TODO_WORKFLOW = "standup_complete_todo"


def _coerce_uuid(value: Any) -> Optional[UUID]:
    """Safe UUID coercion (the #1466 idiom): an unmappable id degrades to
    None — never a raise, never a default owner."""
    if not value:
        return None
    try:
        return UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return None


async def find_overdue_todos(todo_service, user_id: Any) -> List[Any]:
    """The user's ACTIVE overdue todos, most-overdue first (earliest due date).

    Owner-scoped via the same ``list_todos`` read every todo surface uses
    (#1493/#1532). Overdue = has a due_date strictly in the past, not
    completed. Both comparison sides are normalized aware-UTC (the
    #1429/#1491 guard shape — naive rows are assumed UTC). A non-UUID
    principal resolves to no referent (fail-closed, never a default owner).
    """
    user_uuid = _coerce_uuid(user_id)
    if user_uuid is None:
        return []
    todos = await todo_service.list_todos(user_id=user_uuid, include_completed=False)
    now = datetime.now(timezone.utc)
    overdue = [
        t
        for t in todos
        if not t.completed
        and (due_utc := ensure_utc(getattr(t, "due_date", None))) is not None
        and due_utc < now
    ]
    # Every t in overdue has a due date (the filter above); ``or now`` is the
    # mypy-visible spelling of that fact, never a reachable fallback.
    overdue.sort(key=lambda t: ensure_utc(t.due_date) or now)
    return overdue


@dataclass(frozen=True)
class OverdueTodoOffer:
    """What the standup handler arms: the closing question (rendered as the
    report's trailing line) and the pending-offer record for the #846 store."""

    question: str
    offer: Dict[str, Any]


def _due_phrase(todo: Any) -> str:
    due = ensure_utc(getattr(todo, "due_date", None))
    return f" (was due {due.date().isoformat()})" if due else ""


def offer_question(todo: Any, more_overdue: int) -> str:
    """The closing copy. ALWAYS names its bound referent verbatim — the
    #1651 rule: never an unbound 'that todo'. With additional overdue todos
    the count is stated honestly (m-44: the denominator) and the question
    still binds the single strongest."""
    text = getattr(todo, "text", "") or "(untitled)"
    if more_overdue > 0:
        plural = "todo is" if more_overdue == 1 else "todos are"
        return (
            f'Also: your todo "{text}" is overdue{_due_phrase(todo)}, and '
            f"{more_overdue} more {plural} overdue behind it. "
            f'Want me to mark "{text}" done? (yes/no)'
        )
    return (
        f'Also: your todo "{text}" is overdue{_due_phrase(todo)}. '
        "Want me to mark that overdue todo done? (yes/no)"
    )


def build_overdue_todo_offer(
    user_id: Optional[str],
    session_id: Optional[str],
    todo: Any,
    more_overdue: int = 0,
) -> Optional[OverdueTodoOffer]:
    """Build the bound closing offer, or None when it cannot be armed:

    - no session → nothing to bind the next turn's "yes" to;
    - no user → the todo is the USER's (#1532) — an anonymous acceptance
      would complete nobody's todo;
    - no todo id → nothing to bind (an unbound offer is the #1651 bug).
    """
    if not session_id or not user_id:
        return None
    todo_id = getattr(todo, "id", None)
    if not todo_id:
        return None
    text = getattr(todo, "text", "") or "(untitled)"
    summary = f'mark the overdue todo "{text}" done'
    question = offer_question(todo, more_overdue)
    return OverdueTodoOffer(
        question=question,
        offer={
            "workflow_type": STANDUP_COMPLETE_TODO_WORKFLOW,
            # #1665: the rendered ask rides the record — the SAME string the
            # standup renders as its trailing line (built once, above).
            "question": question,
            "pending_action": {
                "kind": STANDUP_TODO_OFFER_KIND,
                # "action" keeps the #1190 carrier's field contract (the
                # off-intent abandonment log reads it) — not a rail key.
                "action": STANDUP_COMPLETE_TODO_WORKFLOW,
                "user_id": str(user_id),
                "todo_id": str(todo_id),
                "todo_text": text,
                "summary": summary,
            },
            "decline_message": (f'Okay — "{text}" stays on your list. Nothing has been changed.'),
        },
    )


# --- #1739 STATE_QUESTION handling (adopted 2026-09-11) ----------------------

# Referent terms a state question can use to point at THIS offer's subjects:
# the standup report the offer trails, or the overdue-todo domain. A question
# naming neither is not necessarily unrelated, but the seam cannot answer it
# honestly from the offer record alone — it falls back to the confirm-tier
# visible re-arm (normal processing answers; the ask restates as a suffix).
# This is ANSWER composition for an already-delivered STATE_QUESTION verdict,
# not acceptance vocabulary — the accept/decline judgment stays with
# ``evaluate_acceptance`` (#1739's one-predicate rule).
_STANDUP_REFERENT = "standup"
_TODO_REFERENT_TERMS = ("todo", "overdue")


def state_question_reply(offer: Dict[str, Any], message: str) -> Optional[Dict[str, Any]]:
    """Seam-composed answer to a STATE_QUESTION that names this offer's own
    referents; None when it doesn't (caller falls back to visible re-arm +
    routed answer).

    Honesty is why the seam can answer at all: this offer only arms AFTER a
    non-empty standup report rendered (the arm site is the standup handler's
    closing line), so "the standup is done" is a fact the record proves; and
    while the offer pends nothing has fired, so "the todo is still open" is
    too. The stored ask re-renders verbatim in the same reply (contract doc
    §5b: a re-render is still an ASK — the caller re-arms, and the next
    "yes" binds to an ask the user saw THIS turn).

    ⚠️ COPY SEAM: Lead-drafted mechanism copy; CXO owns the voice — adjust
    wording here, not at call sites.
    """
    lowered = (message or "").lower()
    payload = offer.get("pending_action") or {}
    todo_text = payload.get("todo_text") or ""
    about_standup = _STANDUP_REFERENT in lowered
    about_todo = any(t in lowered for t in _TODO_REFERENT_TERMS) or (
        bool(todo_text) and todo_text.lower() in lowered
    )
    if not (about_standup or about_todo):
        return None
    if about_standup:
        status = "Yes — that standup is done; the full report rendered above."
    else:
        text = todo_text or "that todo"
        status = f'Not yet — "{text}" is still open; nothing has been changed.'
    question = offer.get("question") or ""
    return {
        "message": f"{status} {question}".strip(),
        "intent_data": {
            "category": "soft_offer_state_question",
            "action": STANDUP_COMPLETE_TODO_WORKFLOW,
            "state_question_answered": True,
            "offer_rearmed": bool(question),
        },
    }


async def run_standup_complete_todo_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1651: complete the BOUND overdue todo on an accepted standup offer.

    Dispatched ONLY by the offer-acceptance seam — the "yes" turn (crisp or
    PM's verbatim "Yes mark the overdue todo done.") against the offer armed
    by ``_handle_standup_query``. Registered action_triggered=False (the
    verify_inference/#1190 pattern) so the classifier/rail can never reach it.

    Completion goes by the STORED todo id through the same
    ``TodoManagementService.complete_todo`` the chat handler uses — the
    user's phrasing is never re-parsed and no title matching runs (the #1651
    failure mode). Success copy derives from the actual tool result (the
    #1571 property); a completion that didn't verifiably happen says so
    honestly — never a fabricated confirmation.
    """
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != STANDUP_TODO_OFFER_KIND:
        logger.error(
            "standup_todo_offer_missing_or_foreign_payload",
            has_payload=bool(payload),
            kind=payload.get("kind"),
        )
        return None
    if intent_service is None:
        logger.error("standup_todo_offer_missing_intent_service")
        return None

    # #1532: the todo is the USER's. The offer was built for the user it was
    # offered to; if the accepting turn's principal differs (auth changed
    # between turns), don't touch the other principal's todo — decline-shaped
    # no-op (mirrors run_verify_inference_workflow / run_standup_interview_workflow).
    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    if offer_user and principal and offer_user != principal:
        logger.warning(
            "standup_todo_offer_principal_mismatch",
            offer_user=offer_user,
            turn_user=principal,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": STANDUP_COMPLETE_TODO_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    effective_user = _coerce_uuid(principal or offer_user)
    todo_uuid = _coerce_uuid(payload.get("todo_id"))
    if effective_user is None or todo_uuid is None:
        logger.error(
            "standup_todo_offer_malformed_record",
            has_user=effective_user is not None,
            has_todo_id=todo_uuid is not None,
        )
        return None

    text = payload.get("todo_text") or "that todo"
    todo_service = intent_service.todo_handlers.todo_service
    try:
        completed = await todo_service.complete_todo(todo_id=todo_uuid, user_id=effective_user)
    except Exception as e:  # silent-ok: logged at error; the reply below states the honest non-completion instead of a fabricated confirmation (#1425)
        logger.error(
            "standup_todo_complete_failed",
            todo_id=str(todo_uuid),
            error=str(e),
            exc_info=True,
        )
        completed = None

    if completed:
        from services.consciousness.todo_consciousness import (
            format_todo_completed_conscious,
        )

        logger.info(
            "standup_todo_offer_completed",
            todo_id=str(todo_uuid),
            user_id=str(effective_user),
        )
        return {
            "message": format_todo_completed_conscious(completed),
            "intent_data": {
                "category": "execution",
                "action": STANDUP_COMPLETE_TODO_WORKFLOW,
                "completed": True,
                "todo_id": str(todo_uuid),
            },
        }

    return {
        "message": (
            f'I couldn\'t mark "{text}" done just now — it may already be '
            "completed or removed. Say 'show my todos' to check the list."
        ),
        "intent_data": {
            "category": "execution",
            "action": STANDUP_COMPLETE_TODO_WORKFLOW,
            "completed": False,
            "todo_id": str(todo_uuid),
        },
    }
