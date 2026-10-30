"""#2223: an armed offer is acted on only under the principal that armed it.

Arch's ruling (decisions.log 2026-10-30 10:36 PT, generalizing 2026-10-29
13:04, #2199, #2207, #2222). The #846 pending-offer store is session-keyed and
``/api/v1/intent`` takes optional auth, so a turn with no principal, or a
different one, can pop an offer an authenticated user armed. The generic accept
seam then dispatched the record's workflow, and ``confirm_pending_action``
re-dispatched the STORED Intent, whose context carries the arming user: the
held write ran under that user on a turn that authenticated nobody.

The rule, applied ONCE at the pop seam (``IntentService._process_intent_internal``,
right after ``get_and_clear_pending_offer``):

- The record's principal is every user id it names: ``pending_action["user_id"]``
  and the stored Intent's ``context["user_id"]`` (``pending_action["intent"]``).
- A record that names a principal is acted on only when the turn's
  authenticated principal equals it (all named ids must equal it).
- A None or different turn principal DROPS the offer: logged
  ``pending_offer_dropped_principal_mismatch``; no kind handler acts, no
  generic accept or decline runs, and the turn routes normally.
- A record that names no principal (armed on an anonymous turn, or one of the
  read-only offers listed below) behaves exactly as before.

The per-kind checks (#2199 milestone pick, #2207/#2222 repo question, the
#1532/#1605 mismatch checks) stay in place; this check runs first and
subsumes them.

Presentation: the drop renders nothing of its own. For a DIFFERENT
authenticated principal, a kind whose handler already answered that turn with
its own "Let's hold off on that" line still does: the handler is called and its
reply is used only when it is flagged ``principal_mismatch``. Each listed
handler reaches its mismatch check before any read or write.
"""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional

import structlog

logger = structlog.get_logger(__name__)

# SHRINK-ONLY. Kinds of WRITE-effect offer whose arm site cannot record the
# arming principal, so the pop-seam check cannot protect them. Empty at #2223:
# every write-effect arm site records ``pending_action["user_id"]`` or carries
# the stored Intent (whose context holds the principal stamped at the host
# boundary). The two record shapes that name no principal are not write-effect:
# the soft workflow offer (``_apply_soft_offer``; only registered types arm,
# and the one registered soft type, ``meeting``, is READ) and the canonical
# ``action_required`` offer (``priority_check`` / ``project_setup`` / ``setup``,
# none registered, so an accept routes to the floor under the turn's own
# principal). Pinned by size in
# ``tests/unit/services/intent_service/test_offer_principal_2223.py``: a new
# entry needs Arch's ruling and a reason here, and the pin only goes down.
UNRECORDED_PRINCIPAL_WRITE_OFFER_KINDS: FrozenSet[str] = frozenset()

# Kinds whose turn handler already answers a DIFFERENT authenticated principal
# with its own hold-off line, reached before any read or write. Only these are
# called on a mismatch, and only a reply flagged ``principal_mismatch`` is used.
_KINDS_WITH_OWN_MISMATCH_REPLY: FrozenSet[str] = frozenset(
    {
        "issue_repo_question",
        "add_project_offer_question",
        "add_project_name_question",
        "add_project_confirm_question",
        "delete_todo_pick_question",
        "reminder_clear_verb_question",
        "reminder_clear_correction",
        "reminder_clear_pick_target_question",
    }
)


def _intent_context(intent: Any) -> Optional[Dict[str, Any]]:
    if intent is None:
        return None
    ctx = intent.get("context") if isinstance(intent, dict) else getattr(intent, "context", None)
    return ctx if isinstance(ctx, dict) else None


def recorded_offer_principals(record: Any) -> FrozenSet[str]:
    """Every user id the offer record names (empty when it names none)."""
    if not isinstance(record, dict):
        return frozenset()
    payload = record.get("pending_action")
    if not isinstance(payload, dict):
        return frozenset()
    found = set()
    if payload.get("user_id"):
        found.add(str(payload["user_id"]))
    ctx = _intent_context(payload.get("intent"))
    if ctx and ctx.get("user_id"):
        found.add(str(ctx["user_id"]))
    return frozenset(found)


def offer_principal_mismatch(record: Any, turn_user_id: Optional[Any]) -> bool:
    """True when the record names a principal the turn's does not equal.

    A None turn principal against a record that names one is a mismatch; a
    record that names none never is (behaves as before)."""
    recorded = recorded_offer_principals(record)
    if not recorded:
        return False
    turn = str(turn_user_id) if turn_user_id else None
    return turn is None or recorded != {turn}


async def _kind_mismatch_reply(
    record: Dict[str, Any],
    message: str,
    *,
    session_id: str,
    user_id: str,
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    kind = (record.get("pending_action") or {}).get("kind")
    if kind not in _KINDS_WITH_OWN_MISMATCH_REPLY:
        return None
    if kind == "issue_repo_question":
        from services.intent_service.repo_clarification import handle_repo_question_turn

        turn = await handle_repo_question_turn(
            record, message, session_id=session_id, user_id=user_id, intent_service=intent_service
        )
    elif kind == "add_project_offer_question":
        from services.intent_service.add_project_clarify import handle_add_project_offer_turn

        turn = await handle_add_project_offer_turn(
            record, message, session_id=session_id, user_id=user_id
        )
    elif kind == "add_project_name_question":
        from services.intent_service.add_project_clarify import handle_add_project_name_turn

        turn = await handle_add_project_name_turn(
            record, message, session_id=session_id, user_id=user_id, intent_service=intent_service
        )
    elif kind == "add_project_confirm_question":
        from services.intent_service.add_project_clarify import handle_add_project_confirm_turn

        turn = await handle_add_project_confirm_turn(
            record, message, session_id=session_id, user_id=user_id, intent_service=intent_service
        )
    elif kind == "delete_todo_pick_question":
        from services.intent_service.delete_todo_pick import handle_delete_todo_pick_turn

        turn = await handle_delete_todo_pick_turn(
            record, message, session_id=session_id, user_id=user_id, intent_service=intent_service
        )
    else:
        from services.intent_service.reminder_clear import handle_reminder_clear_turn

        turn = await handle_reminder_clear_turn(
            record, message, session_id=session_id, user_id=user_id, intent_service=intent_service
        )
    if turn and (turn.get("intent_data") or {}).get("principal_mismatch"):
        return turn
    return None


async def drop_offer_on_principal_mismatch(
    record: Optional[Dict[str, Any]],
    message: str,
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The pop-seam check. Returns None when the offer may be acted on (the
    caller proceeds unchanged). Otherwise the offer is dropped and this returns
    ``{"reply": <the kind's own hold-off reply or None>}``; the caller acts on
    nothing from the offer and, with no reply, routes the turn normally."""
    if not record or not offer_principal_mismatch(record, user_id):
        return None
    payload = record.get("pending_action") or {}
    logger.warning(
        "pending_offer_dropped_principal_mismatch",
        offer_user=sorted(recorded_offer_principals(record)),
        turn_user=str(user_id) if user_id else None,
        kind=payload.get("kind"),
        workflow_type=record.get("workflow_type"),
        session_id=session_id,
    )
    reply = None
    if user_id:
        reply = await _kind_mismatch_reply(
            record,
            message,
            session_id=session_id,
            user_id=str(user_id),
            intent_service=intent_service,
        )
    return {"reply": reply}
