"""#2219 Gap A: an ordinal on a grouped line of the todo list asks one, or all.

"show my todos" numbers its lines and groups repeats ("3. review prs (×3)").
A number names a LINE, not a copy (CXO 11-06 07:35), so "complete the third
one" on a grouped line cannot know whether the person means one copy or all
of them. It asks, in CXO's words:

``"review prs" is on your list 3 times. Complete one, or all 3?``

The answer "one" completes the FIRST copy in list order; "all" / "all 3" /
"both" completes every copy. A one-copy line never reaches here (it completes
at once, Gap B).

Complete only. CXO's delete form ("Delete one …, or all 3?") would delete
several rows on one answer, which xian's #2019 cap (``delete_cap.DELETE_CAP``
= 1) forbids until soft delete and undo (issue 2021); a grouped delete binds
one copy and gets the one-item confirm in ``todo_handlers`` instead. Arch
11-06 09:17: no delete path may live here while the cap holds, so
``arm_group_line_question`` refuses any other verb.

The question ARMS via the #846 pending-offer store and is answered at the pop
seam kind-specifically, before generic accept/decline: the #1987
``delete_todo_pick`` shape. The record carries the copies' ids bound at ask
time (#1665), so the answer acts on exactly the rows the question named.
Pleasantries survive, a farewell releases, a decline drops honestly, a bare
"yes" lands on the registered offer-only workflow (``clarify_todo_group_line``,
action_triggered=False) which re-asks, a claimed command releases and routes,
and a second unresolved answer releases. The answer is read with word-set
checks only: no new extraction regex (the #1595 ratchet does not move).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

logger = structlog.get_logger(__name__)

# The #846 record kind (handled kind-specifically at the pop seam).
GROUP_LINE_KIND = "todo_group_line_question"
# The registered offer-only workflow: the generic seam's ACCEPT path lands a
# bare "yes" here, which re-asks and re-arms.
CLARIFY_GROUP_LINE_WORKFLOW = "clarify_todo_group_line"
# The intent_data flag a turn that (re-)arms the question stamps, so
# ``_apply_soft_offer`` never clobbers the one-slot store (the #1648 belt).
GROUP_LINE_PENDING_FLAG = "todo_group_line_pending"

VERB_COMPLETE = "complete"

# Word sets for the answer (CXO: "one" / "all" / "all 3" / "both"). The line's
# own count joins the all-set per question ("3" against "or all 3?").
_ONE_WORDS = frozenset({"one", "1", "single"})
_ALL_WORDS = frozenset({"all", "both", "every", "everything"})
# The pleasantries an armed question survives, as in delete_todo_pick (CXO's
# 2026-10-13 copy); a farewell releases.
_PLEASANTRY_ACTIONS = frozenset({"greeting", "thanks"})
_PLEASANTRY_ACK = {"thanks": "You're welcome.", "greeting": "Hi!"}


def render_group_line_question(verb: str, text: str, count: int) -> str:
    """CXO's words (11-06 07:35), verbatim."""
    return f'"{text}" is on your list {count} times. Complete one, or all {count}?'


def _decline_message(verb: str, text: str) -> str:
    """The existing Okay-family decline (#1943 complete)."""
    return "Okay — I won't mark those done. Nothing has been changed."


def _offer(
    verb: str,
    ids: List[str],
    text: str,
    noun: str,
    principal: Optional[str],
    original_message: str,
    question: str,
    reasked: bool = False,
) -> Dict[str, Any]:
    return {
        "workflow_type": CLARIFY_GROUP_LINE_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": GROUP_LINE_KIND,
            "action": CLARIFY_GROUP_LINE_WORKFLOW,
            "user_id": principal,
            "verb": verb,
            "line_ids": list(ids),
            "line_text": text,
            "noun": noun,
            "original_message": original_message,
            "line_reasked": reasked,
            "summary": f"{verb} one or all of a repeated {noun}",
        },
        "decline_message": _decline_message(verb, text),
    }


def _rearm(offer_service: Any, session_id: Optional[str], user_id: Any, payload: Dict, **kw):
    question = render_group_line_question(
        payload.get("verb") or VERB_COMPLETE,
        payload.get("line_text") or "",
        len(payload.get("line_ids") or []),
    )
    offer_service.set_pending_offer(
        session_id,
        _offer(
            payload.get("verb") or VERB_COMPLETE,
            payload.get("line_ids") or [],
            payload.get("line_text") or "",
            payload.get("noun") or "todo",
            payload.get("user_id"),
            payload.get("original_message") or "",
            question,
            reasked=kw.get("reasked", bool(payload.get("line_reasked"))),
        ),
        user_id=user_id,
    )
    return question


def arm_group_line_question(
    verb: str,
    rows: List[Any],
    noun: str,
    original_message: str,
    session_id: Optional[str],
    offer_service: Any,
    principal: Optional[str],
) -> Optional[str]:
    """The ARM half, called by the todo target handlers when a lone ordinal
    names a line with more than one copy. Returns the question, or ``None``
    when nothing could pop an answer (no session or no store)."""
    if verb != VERB_COMPLETE:
        # Arch 11-06 09:17: no path around xian's #2019 delete cap lives here.
        raise ValueError(f"todo_line_pick arms complete only, not {verb!r}")
    if not session_id or offer_service is None or len(rows) < 2:
        return None
    text = rows[0].text
    question = render_group_line_question(verb, text, len(rows))
    offer_service.set_pending_offer(
        session_id,
        _offer(verb, [str(t.id) for t in rows], text, noun, principal, original_message, question),
        user_id=principal,
    )
    logger.info("todo_group_line_armed", session_id=session_id, verb=verb, copies=len(rows))
    return question


def _answer_scope(text: str, count: int) -> Optional[str]:
    """ "one" or "all" when the answer says exactly one of them, else ``None``."""
    words = {w.strip(".,!?;:'\"()").lower() for w in (text or "").split()}
    says_all = bool(words & (_ALL_WORDS | {str(count)}))
    says_one = bool(words & _ONE_WORDS)
    if says_all and not says_one:
        return "all"
    if says_one and not says_all:
        return "one"
    return None


async def handle_todo_group_line_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam. Returns ``None`` to fall through to
    the generic seam: a state question (re-armed silently), a decline (the
    record's ``decline_message``), a bare "yes" (the registered landing
    re-asks), a released command, or a second unresolved answer."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != GROUP_LINE_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None

    from services.intent_service.reminder_clear import _principal_mismatch

    if _principal_mismatch(payload, user_id):
        logger.warning(
            "todo_group_line_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_GROUP_LINE_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )

    axes = declared_axes_for_workflow(CLARIFY_GROUP_LINE_WORKFLOW)
    verdict = evaluate_acceptance(
        text,
        effect=axes[0] if axes else None,
        outwardness=axes[1] if axes else None,
        armed_question=pending_offer.get("question"),
    )
    if verdict in (
        AcceptanceVerdict.STATE_QUESTION,
        AcceptanceVerdict.DECLINE,
        AcceptanceVerdict.ACCEPT,
    ):
        logger.info("todo_group_line_generic_seam", session_id=session_id, verdict=verdict.name)
        return None

    ids = [str(i) for i in payload.get("line_ids") or []]
    scope = _answer_scope(text, len(ids))
    if scope is not None:
        return await _act(scope, payload, ids, user_id, intent_service)

    offer_service = intent_service.workflow_offer_service
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None and claimed.action in _PLEASANTRY_ACTIONS:
        # As in delete_todo_pick (Arch's condition 3 on #1987): a pleasantry
        # keeps the question; a farewell is not in the set and releases below.
        question = _rearm(offer_service, session_id, user_id, payload)
        logger.info("todo_group_line_survives_pleasantry", session_id=session_id)
        return {
            "message": f"{_PLEASANTRY_ACK[claimed.action]}\n{question}",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_GROUP_LINE_WORKFLOW,
                GROUP_LINE_PENDING_FLAG: True,
            },
            "requires_clarification": True,
        }
    if claimed is not None:
        logger.info("todo_group_line_command_released", claimed_action=claimed.action)
        return None

    from services.intent_service.inversion_live import (
        read_op_claims_turn,
        registry_category_for,
    )

    verb = payload.get("verb") or VERB_COMPLETE
    read_op = await read_op_claims_turn(
        text,
        session_id=session_id,
        user_id=user_id,
        intent_service=intent_service,
        carrier_category=registry_category_for(f"{verb}_todo"),
    )
    if read_op is not None:
        logger.info("todo_group_line_command_released", claimed_action=read_op)
        return None
    if payload.get("line_reasked"):
        logger.info("todo_group_line_release_after_reask", session_id=session_id)
        return None  # second unresolved answer in a row: release, no loop

    question = _rearm(offer_service, session_id, user_id, payload, reasked=True)
    logger.info("todo_group_line_reasked", session_id=session_id)
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": CLARIFY_GROUP_LINE_WORKFLOW,
            GROUP_LINE_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }


async def _act(
    scope: str,
    payload: Dict[str, Any],
    ids: List[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Dict[str, Any]:
    """Complete the bound copies: the first one in list order, or all of them.
    Each row is re-read first; a copy gone since the ask is reported, never
    replaced by another row."""
    from services.intent_service.todo_handlers import _batch_summary, one_copy_result

    verb = VERB_COMPLETE
    text = payload.get("line_text") or ""
    data = {"category": "execution", "action": f"{verb}_todo", "todo_group_line": scope}
    principal = str(user_id) if user_id else payload.get("user_id")
    try:
        todo_user_id = UUID(str(principal))
    except (ValueError, TypeError):
        return {
            "message": f"I need you to be logged in to {verb} todos. Nothing has been changed.",
            "intent_data": {**data, "error_type": "AuthenticationRequired"},
        }
    service = intent_service.todo_handlers.todo_service
    try:
        rows = await service.list_todos(user_id=todo_user_id, include_completed=True)
    except (
        Exception
    ) as e:  # silent-ok: error-logged with exc_info; honest no-op copy, nothing changed
        logger.error("todo_group_line_list_failed", error=str(e), exc_info=True)
        return {
            "message": (
                "I couldn't look up your todos just now, so I haven't changed anything. "
                "Try again in a moment."
            ),
            "intent_data": data,
        }
    live = {str(t.id): t for t in rows or []}
    present = [i for i in ids if i in live and not live[i].completed]
    chosen = present[:1] if scope == "one" else present
    if not chosen:
        return {
            "message": (
                f'I can\'t find "{text}" on your list anymore. '
                "Say 'show my todos' to see the list — nothing has been changed."
            ),
            "intent_data": {**data, "line_target_gone": True},
        }

    done: List[str] = []
    failed = []
    for tid in chosen:
        try:
            ok = await service.complete_todo(todo_id=UUID(tid), user_id=todo_user_id)
        except Exception as e:  # silent-ok: counted and reported per copy, as the batch paths do
            logger.warning("todo_group_line_item_failed", todo_id=tid, error=str(e))
            ok = None
        if ok:
            done.append(text)
        else:
            failed.append((text, "no longer there"))
    logger.info("todo_group_line_acted", verb=verb, scope=scope, done=len(done))
    if scope == "one" and len(done) == 1:
        # CXO 11-06 08:3x: one copy of a grouped line says how many are still
        # open, counted from the copies the question was armed with.
        message = one_copy_result(VERB_COMPLETE, text, len(ids) - 1)
    else:
        message = _batch_summary(done, failed, [])
    return {"message": message, "intent_data": data}


async def run_clarify_todo_group_line_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_todo_group_line``,
    action_triggered=False): a bare "yes" answers neither one nor all, so
    re-ask and re-arm. effect: READ (nothing is written here; the act happens
    on an answered turn at the pop seam)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != GROUP_LINE_KIND or intent_service is None:
        logger.error(
            "todo_group_line_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    question = _rearm(intent_service.workflow_offer_service, session_id, user_id, payload)
    return {
        "message": "Just so I get it right: " + question,
        "intent_data": {
            "category": "execution",
            "action": CLARIFY_GROUP_LINE_WORKFLOW,
            GROUP_LINE_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
