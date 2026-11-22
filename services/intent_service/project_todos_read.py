"""#2413: "show me the todos in the Launch project" asks which project, then shows it.

Rulings (all 2026-11-22): Arch 01M82907VE and 01M82A8RX0, CXO 01M829VZ5X and
01M82AGXFK, PPM 01M82986YX.

The classifier emits ``list_project_todos`` or ``list_todos_by_project`` for these
asks, and before this module neither name was registered, so the turn fell to the
generic floor. No model supplies a project on these turns: the classifier's output has
no project field, and the router answers CLARIFY or NONE with no ``project`` arg.

1. Both names are READ entries on the action rail with ``router_visible=False`` (the
   #2132 (b) precedent, ``compare_documents``). ``derive_routing_grammar`` skips hidden
   entries, so the router's request is unchanged; the classifier's prompt is fixed text
   and does not read the registry, so its request is unchanged. Both are pinned by
   sha256 in the tests. No catalog, router, classifier or pre-classifier text changes.
2. The handler NEVER takes a project name from the person's words: no pattern, no word
   matching against the message, no extraction, not even against the person's own
   project names (ADR-080). On either action it reads the person's active projects
   under the turn's own principal and:
   - one or more projects: arms a question (the one-slot pending-offer store, as
     ``todo_project_attach.arm_pick``) listing them, with EVERY active project bound
     at ask time (only five are listed). It is answered by a listed name;
   - no projects: says so, and arms nothing;
   - the project read failed: says it could not check, and shows nothing else;
   - cannot arm (no session or no store): shows no question (``NOT_ARMED_LINE``).
3. The answer turn (``handle_project_todos_pick_turn``, at the pop seam beside
   ``todo_project_attach.handle_todo_project_pick_turn``):
   - the turn's principal is checked first (the 2297 mismatch line);
   - a bare decline or an accept-vocabulary answer returns ``None``: the generic seam
     declines with this record's ``decline_message`` or re-asks through the registered
     landing ``clarify_project_todos_pick`` (action_triggered=False);
   - the answer is matched against the names bound at ask time with 2297's lookup
     (exact, ignoring case, then one trailing word "project" removed; never partial or
     fuzzy). No match returns ``None`` and the message routes as a new request;
   - one match: the bound project id is re-checked under the principal, then 2301's
     render (``todo_handlers.project_status_todos``) shows its open todos;
   - several matches (two bound projects share the name): an armed numbered question,
     answered by number, then the chosen project's todos.
4. It is a read. Nothing is ever written, so there is no confirm step. 2297's lookup is
   shared; its lines are not (each one speaks of a todo write).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.exc import SQLAlchemyError

from services.intent_service import project_status_todos as _pst
from services.intent_service import todo_project_attach as _attach

logger = structlog.get_logger(__name__)

# The classifier's two names for this ask (measured on beta 2026-11-22, 6 of 6 each).
CLASSIFIER_ACTION_NAMES = ("list_project_todos", "list_todos_by_project")

PROJECT_TODOS_PICK_KIND = "project_todos_pick_question"
# The registered offer-only landing (action_triggered=False): a bare "yes" names no
# project, so it re-asks the same question and re-arms it.
PROJECT_TODOS_PICK_WORKFLOW = "clarify_project_todos_pick"
PICK_PENDING_FLAG = "project_todos_pick_pending"

# CXO 2026-11-22 (verbatim). Each *_QUESTION is rendered only where the record that
# answers it is built and armed (the #1766 rule).
QUESTION = (
    "Which project's todos do you want? Your projects: {listed}. "
    "Tell me the name and I'll show them."
)
QUESTION_MANY = (
    "Which project's todos do you want? Your projects: {listed}, and {more} more. "
    "Tell me the name and I'll show them."
)
NO_PROJECTS_LINE = (
    "I don't see any projects on your account, so there are no project todos to show."
)
PROJECTS_READ_FAILED_LINE = "I couldn't check your projects just now."
SEVERAL_QUESTION = (
    "I found more than one project that could be the one you mean: {listed}. "
    "Which one's todos do you want? Say the number."
)

# ---------------------------------------------------------------------------
# PROVISIONAL LINES (Lead is asking CXO, 2026-11-22). Swap the words here only.
# - DECLINE_LINE: the decline message of both records.
# - NOT_ARMED_LINE: no session or store, so no question can be asked.
# - PROJECT_GONE_READ_LINE: the bound project is gone between ask and answer.
# A project with no open todos shows 2301's NO_OPEN_TODOS_LINE as the renderer
# returns it (``_show_todos`` is the one place to swap it).
DECLINE_LINE = "Okay, I haven't shown anything."
NOT_ARMED_LINE = "I couldn't check your projects just now."
PROJECT_GONE_READ_LINE = "I couldn't find that project anymore."
# ---------------------------------------------------------------------------

_CATEGORY = "query"


def render_question(names: List[str]) -> str:
    """CXO: up to five names are listed; past five, the first five and the tail."""
    if len(names) > _attach.MAX_LISTED:
        return QUESTION_MANY.format(
            listed=", ".join(names[: _attach.MAX_LISTED]),
            more=len(names) - _attach.MAX_LISTED,
        )
    return QUESTION.format(listed=", ".join(names))


def render_several(labels: List[str]) -> str:
    """The numbered question, built from ``ProjectRef.label`` as 2297's is."""
    listed = " ".join(f"{i}. {n}" for i, n in enumerate(labels, 1))
    return SEVERAL_QUESTION.format(listed=listed)


def _record(
    question: str, answer: str, principal: Optional[str], projects: List[_attach.ProjectRef]
) -> Dict[str, Any]:
    return {
        "workflow_type": PROJECT_TODOS_PICK_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": PROJECT_TODOS_PICK_KIND,
            "action": PROJECT_TODOS_PICK_WORKFLOW,
            "answer": answer,
            "user_id": principal,
            "pick_ids": [p.id for p in projects],
            "pick_names": [p.name for p in projects],
            "pick_labels": [p.label for p in projects],
            "pick_created": [p.created for p in projects],
            # The question as asked; a bare "yes" re-asks exactly this.
            "question": question,
            "summary": "pick which project's todos to show",
        },
        "decline_message": DECLINE_LINE,
    }


def build_name_offer(
    principal: Optional[str], projects: List[_attach.ProjectRef]
) -> Dict[str, Any]:
    """The record for the first question: EVERY active project bound, answered by a
    listed name."""
    return _record(
        render_question([p.name for p in projects]), _attach.ANSWER_NAME, principal, projects
    )


def build_number_offer(
    principal: Optional[str], matches: List[_attach.ProjectRef]
) -> Dict[str, Any]:
    """The record for SEVERAL bound projects sharing the answered name, answered by
    number."""
    return _record(
        render_several([m.label for m in matches]), _attach.ANSWER_NUMBER, principal, matches
    )


def _result(message: str, intent_data: Dict[str, Any], *, clarify: bool = False) -> Any:
    from services.intent.intent_service import IntentProcessingResult

    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data=intent_data,
        requires_clarification=clarify,
    )


async def run_list_project_todos_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Rail entry for ``list_project_todos`` and ``list_todos_by_project``. Reads the
    person's active projects and asks which one; the message is never read for a
    name. effect: READ."""
    ctx = context or {}
    intent = ctx.get("intent")
    intent_service = ctx.get("intent_service")
    action = getattr(intent, "action", None) or CLASSIFIER_ACTION_NAMES[0]
    category = getattr(getattr(intent, "category", None), "value", None) or _CATEGORY
    data: Dict[str, Any] = {"category": category, "action": action}
    from services.intent.intent_service import IntentProcessingResult, _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user or intent_service is None:
        # The todo rail's own unauthenticated reply (run_create_todo_workflow's shape).
        return IntentProcessingResult(
            success=False,
            message="I need you to be logged in to manage todos. Please log in and try again.",
            intent_data=data,
            error="User not authenticated",
            error_type="AuthenticationRequired",
        )
    try:
        projects = _attach._refs(await _attach._active_projects(str(todo_user)))
    except (SQLAlchemyError, OSError) as e:
        logger.error("project_todos_read_projects_failed", error=str(e))
        return _result(PROJECTS_READ_FAILED_LINE, {**data, "project_lookup_failed": True})
    if not projects:
        return _result(NO_PROJECTS_LINE, data)
    record = build_name_offer(str(user_id), projects)
    if not _attach.arm_pick(intent_service, record, session_id, user_id):
        return _result(NOT_ARMED_LINE, data)
    logger.info("project_todos_read_asked", projects=len(projects))
    return _result(
        record["question"],
        {**data, "action": PROJECT_TODOS_PICK_WORKFLOW, PICK_PENDING_FLAG: True},
        clarify=True,
    )


async def _show_todos(
    intent_service: Any, session_id: Optional[str], todo_user: Any, project: Any
) -> str:
    """2301's render of one project's open todos (the header and list, or its
    no-open-todos line). A failed todo read says 2301's couldn't-check line; it never
    raises, as ``project_status_todos.status_todos_block``."""
    try:
        return str(
            await intent_service.todo_handlers.project_status_todos(session_id, todo_user, project)
        )
    except (SQLAlchemyError, OSError) as e:
        logger.error("project_todos_read_todo_read_failed", error=str(e))
        return _pst.TODOS_READ_FAILED_LINE
    except Exception:  # silent-ok: as status_todos_block (Arch 11-20, 01M7Y4QVSY); stack logged, CXO's couldn't-check line is said
        logger.exception("project_todos_read_todo_read_failed")
        return _pst.TODOS_READ_FAILED_LINE


async def handle_project_todos_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam. A listed name (or, on the numbered question, a
    number) shows that project's open todos, the project bound BY ID at ask time and
    re-checked under the turn's own principal. Anything else returns ``None``: the
    generic seam handles a decline, a bare "yes" (the landing re-asks) or a new request
    (routes normally; the record is popped)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != PROJECT_TODOS_PICK_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None
    from services.intent_service.reminder_clear import _ordinal_index, _principal_mismatch

    intent_data: Dict[str, Any] = {"category": _CATEGORY, "action": PROJECT_TODOS_PICK_WORKFLOW}
    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "project_todos_pick_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": _attach.PRINCIPAL_MISMATCH_LINE,
            "intent_data": {**intent_data, "principal_mismatch": True},
        }
    ids = [str(i) for i in payload.get("pick_ids") or []]
    if not ids:
        return None
    if payload.get("answer") == _attach.ANSWER_NAME:
        from services.intent_service.soft_invocation import (
            is_bare_decline,
            matches_accept_vocabulary,
        )

        if is_bare_decline(text) or matches_accept_vocabulary(text):
            return None
        names = [str(n) for n in payload.get("pick_names") or []]
        positions = _attach._named_positions(names, text) if len(names) == len(ids) else []
        if not positions:
            return None
        if len(positions) > 1:
            created = [str(c) for c in payload.get("pick_created") or []]
            matches = [
                _attach.ProjectRef(
                    id=ids[i], name=names[i], created=created[i] if i < len(created) else ""
                )
                for i in positions
            ]
            record = build_number_offer(str(user_id), matches)
            if not _attach.arm_pick(intent_service, record, session_id, user_id):
                return {"message": NOT_ARMED_LINE, "intent_data": intent_data}
            return {
                "message": record["question"],
                "intent_data": {**intent_data, PICK_PENDING_FLAG: True},
                "requires_clarification": True,
            }
        idx = positions[0]
    else:
        if len(text.split()) > _attach._MAX_ANSWER_WORDS:
            return None
        position = _ordinal_index(text, len(ids))
        if position is None:
            return None
        idx = position
    from services.intent.intent_service import _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user:
        return {"message": _attach.PRINCIPAL_MISMATCH_LINE, "intent_data": intent_data}
    try:
        project = await _attach._owned_active_project(ids[idx], str(todo_user))
    except (SQLAlchemyError, OSError) as e:
        logger.error("project_todos_pick_project_read_failed", error=str(e))
        return {"message": PROJECTS_READ_FAILED_LINE, "intent_data": intent_data}
    if project is None:
        return {"message": PROJECT_GONE_READ_LINE, "intent_data": intent_data}
    logger.info("project_todos_pick_bound", session_id=session_id, position=idx + 1)
    reply = await _show_todos(intent_service, session_id, todo_user, project)
    return {"message": reply, "intent_data": {**intent_data, "action": CLASSIFIER_ACTION_NAMES[0]}}


async def run_clarify_project_todos_pick_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_project_todos_pick``,
    action_triggered=False): a bare "yes" names no project, so ask the same question
    again with the same bound projects and re-arm it. effect: READ."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != PROJECT_TODOS_PICK_KIND or intent_service is None:
        logger.error(
            "project_todos_pick_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    question = str(payload.get("question") or "")
    if not question:
        labels = [str(n) for n in payload.get("pick_labels") or payload.get("pick_names") or []]
        question = (
            render_several(labels)
            if payload.get("answer") == _attach.ANSWER_NUMBER
            else render_question([str(n) for n in payload.get("pick_names") or []])
        )
    record = {
        "workflow_type": PROJECT_TODOS_PICK_WORKFLOW,
        "question": question,
        "pending_action": dict(payload),
        "decline_message": DECLINE_LINE,
    }
    intent_service.workflow_offer_service.set_pending_offer(session_id, record, user_id=user_id)
    return {
        "message": question,
        "intent_data": {
            "category": _CATEGORY,
            "action": PROJECT_TODOS_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
