"""#2271 (Arch 11-06 11:26; CXO's words): ``hide_project`` archives by EXACT name.

With the surface-1 hide literal absent, the legacy classifier emits
``execution/hide_project`` for "hide the project Beta". ``hide_project`` is a rail
alias of the ``archive_project`` entry (the #1527 discipline), and on THAT emission
``CanonicalHandlers._handle_archive_project`` resolves here instead of through the
tolerant ``find_project_by_name`` (#1857 normalised + single-candidate substring):

- the project is matched by its WHOLE name, case-insensitively, among the person's
  own ACTIVE projects. The name the user said is read with the handler's existing
  ``ARCHIVE_PATTERNS`` capture (no new pattern); the capture's leading filler words
  ("the", "my", "project", "called", "named") are dropped one at a time and each
  remainder, before and after ``clean_project_name``, is a candidate the whole
  stored name must equal. Word lists and string comparison only, no regex.
- one match archives it and says how to restore it;
- none archives nothing and says so;
- more than one archives nothing and ASKS which, armed (the #1987 shape): the
  record carries the matched project ids in the order shown, bound at ask time, and
  the answer turn binds a number at the pop seam (``handle_project_archive_pick_turn``).

Every other archive caller (``archive_project`` emissions, the legacy sniff's
``manage_portfolio`` hand-off) keeps today's resolution and copy unchanged.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)

HIDE_PROJECT_ACTION = "hide_project"
PROJECT_ARCHIVE_PICK_KIND = "project_archive_pick_question"
# The registered offer-only landing (action_triggered=False): the generic seam's
# ACCEPT path lands a bare "yes" here, which re-asks and re-arms.
PROJECT_ARCHIVE_PICK_WORKFLOW = "clarify_project_archive_pick"
PICK_PENDING_FLAG = "project_archive_pick_pending"
# The result key the several-match record rides from the handler to the rail
# adapter (run_archive_project_workflow), which arms it.
PICK_RECORD_KEY = "project_archive_pick_offer"

# CXO's words (verbatim; the name as resolved, quoted, and the restore phrase).
ARCHIVED_LINE = (
    'Archived "{name}". It\'s out of your active list. '
    'Say "restore project {name}" to bring it back.'
)
NOT_FOUND_LINE = (
    "I couldn't find a project called \"{name}\", so I haven't archived anything. "
    'Check the name, or say "show my projects".'
)
# Named *_QUESTION: rendered only by build_pick_offer, which stores it as the
# record's ``question`` and hands the record back to be armed (the #1766 rule).
SEVERAL_QUESTION = (
    "I found more than one project with that name: {listed}. "
    "Which one should I archive? Say the number."
)
# The existing adopted-write decline copy (CXO 2026-10-16), for a "no" to the pick.
PICK_DECLINE_LINE = 'Okay, I won\'t archive "{name}". Nothing has been changed.'
PRINCIPAL_MISMATCH_LINE = "Let's hold off on that — nothing has been changed."

_LEADING_FILLER = frozenset({"the", "my", "project", "called", "named"})
# A pick answer is a short reply ("2", "the second one", "number 2"); a longer
# message is a new request and routes normally.
_MAX_ANSWER_WORDS = 3


def _key(name: Optional[str]) -> str:
    return " ".join(str(name or "").split()).casefold()


def name_candidates(capture: Optional[str]) -> List[str]:
    """Every whole-name reading of the ARCHIVE_PATTERNS capture, as match keys."""
    from services.onboarding.portfolio_service import clean_project_name

    words = (capture or "").split()
    keys: List[str] = []
    for start in range(len(words)):
        if start and words[start - 1].casefold() not in _LEADING_FILLER:
            break
        rest = " ".join(words[start:]).strip().rstrip(".,!?;:")
        for form in (rest, clean_project_name(rest)):
            key = _key(form)
            if key and key not in keys:
                keys.append(key)
    return keys


def display_name(capture: Optional[str]) -> str:
    """The name to echo when nothing matched: the capture without its leading
    filler words, cleaned of politeness and quotes."""
    from services.onboarding.portfolio_service import clean_project_name

    words = (capture or "").split()
    while len(words) > 1 and words[0].casefold() in _LEADING_FILLER:
        words = words[1:]
    return clean_project_name(" ".join(words)) or (capture or "").strip()


def exact_matches(projects: List[Any], capture: Optional[str]) -> List[Any]:
    """The projects whose whole name equals a candidate, case-insensitively, in
    the order given (the active list's order)."""
    keys = set(name_candidates(capture))
    return [p for p in projects or [] if _key(getattr(p, "name", None)) in keys]


def render_several(names: List[str]) -> str:
    listed = " ".join(f"{i}. {n}" for i, n in enumerate(names, 1))
    return SEVERAL_QUESTION.format(listed=listed)


def build_pick_offer(principal: Optional[str], projects: List[Any], original_message: str) -> Dict:
    """The #846 record: the matched projects bound at ask time (ids and names in
    the order the question numbers them), handed back under ``PICK_RECORD_KEY``
    so the archive rail adapter arms it (a CanonicalHandlers method has no
    store; see ``arm_pick_from_result``)."""
    ids = [str(p.id) for p in projects]
    names = [str(p.name) for p in projects]
    question = render_several(names)
    return {
        "workflow_type": PROJECT_ARCHIVE_PICK_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": PROJECT_ARCHIVE_PICK_KIND,
            "action": PROJECT_ARCHIVE_PICK_WORKFLOW,
            "user_id": principal,
            "pick_ids": ids,
            "pick_names": names,
            "original_message": original_message,
            "summary": "pick which project to archive",
        },
        "decline_message": PICK_DECLINE_LINE.format(name=names[0] if names else ""),
    }


async def archive_exact(
    *, capture: str, user_id: str, original_message: str, portfolio_service: Any
) -> Dict[str, Any]:
    """The hide_project branch of ``_handle_archive_project``: resolve, then
    archive one, say none, or ask which (armed)."""
    from services.shared_types import IntentCategory

    projects = await portfolio_service.list_active_projects(user_id=user_id)
    matches = exact_matches(projects, capture)
    category = IntentCategory.PORTFOLIO.value
    if not matches:
        searched = display_name(capture)
        return {
            "message": NOT_FOUND_LINE.format(name=searched),
            "intent": {
                "category": category,
                "action": "project_not_found",
                "confidence": 0.8,
                "context": {"searched_name": searched, "exact_name": True},
            },
            "requires_clarification": False,
        }
    if len(matches) > 1:
        offer = build_pick_offer(user_id, matches, original_message)
        logger.info("project_archive_pick_built", candidates=len(matches))
        return {
            "message": offer["question"],
            "intent": {
                "category": category,
                "action": PROJECT_ARCHIVE_PICK_WORKFLOW,
                "confidence": 0.8,
                "context": {"candidates": len(matches)},
                PICK_PENDING_FLAG: True,
            },
            PICK_RECORD_KEY: offer,
            "requires_clarification": True,
        }
    return await _archive_one(portfolio_service, matches[0], user_id)


async def _archive_one(portfolio_service: Any, project: Any, user_id: str) -> Dict[str, Any]:
    from services.onboarding.portfolio_service import PortfolioActionResult
    from services.shared_types import IntentCategory

    result = await portfolio_service.archive_project(project_id=str(project.id), user_id=user_id)
    done = result.status == PortfolioActionResult.SUCCESS
    return {
        "message": ARCHIVED_LINE.format(name=project.name) if done else result.message,
        "intent": {
            "category": IntentCategory.PORTFOLIO.value,
            "action": "archive_project",
            "confidence": 1.0,
            "context": {"project_name": project.name, "status": result.status.value},
        },
        "requires_clarification": False,
    }


async def _archive_bound_id(project_id: str, user_id: str) -> Dict[str, Any]:
    from services.database.repositories import ProjectRepository
    from services.database.session_factory import AsyncSessionFactory
    from services.onboarding.portfolio_service import PortfolioService

    async with AsyncSessionFactory.session_scope() as session:
        portfolio_service = PortfolioService(ProjectRepository(session))
        project = await portfolio_service.get_project(project_id=project_id, user_id=user_id)
        if project is None:
            return {
                "message": "I couldn't find that project anymore, so I haven't archived anything.",
                "intent": {"category": "portfolio", "action": "project_not_found"},
                "requires_clarification": False,
            }
        return await _archive_one(portfolio_service, project, user_id)


def arm_pick_from_result(
    intent_service: Any, result: Dict[str, Any], session_id: str, user_id: Optional[str]
) -> None:
    """The ARM half: ``run_archive_project_workflow`` passes every handler result
    here; a several-match result's record is armed in the #846 one-slot store
    before the question is shown. Without a session or store the record is
    dropped and the flag cleared, so the reply is never marked as armed."""
    record = result.pop(PICK_RECORD_KEY, None) if isinstance(result, dict) else None
    if not record:
        return
    offer_service = getattr(intent_service, "workflow_offer_service", None)
    if not session_id or offer_service is None:
        logger.warning("project_archive_pick_not_armed", session_id=session_id)
        (result.get("intent") or {}).pop(PICK_PENDING_FLAG, None)
        return
    offer_service.set_pending_offer(session_id, record, user_id=user_id)
    logger.info(
        "project_archive_pick_armed",
        session_id=session_id,
        candidates=len(record["pending_action"]["pick_ids"]),
    )


async def handle_project_archive_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam (before generic accept/decline). A short
    answer naming one listed position archives the project bound BY ID at ask
    time. Anything else returns ``None``: the generic seam handles a decline
    (``decline_message``), a bare "yes" (the registered landing re-asks) or a new
    request (routes normally; the record is already popped)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != PROJECT_ARCHIVE_PICK_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None
    from services.intent_service.reminder_clear import _ordinal_index, _principal_mismatch

    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "project_archive_pick_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": {
                "category": "portfolio",
                "action": PROJECT_ARCHIVE_PICK_WORKFLOW,
                "principal_mismatch": True,
            },
        }
    ids = [str(i) for i in payload.get("pick_ids") or []]
    if len(text.split()) > _MAX_ANSWER_WORDS:
        return None
    idx = _ordinal_index(text, len(ids))
    if idx is None:
        return None
    logger.info("project_archive_pick_bound", session_id=session_id, position=idx + 1)
    result = await _archive_bound_id(ids[idx], str(user_id))
    return {
        "message": result["message"],
        "intent_data": result["intent"],
        "requires_clarification": False,
    }


async def run_clarify_project_archive_pick_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_project_archive_pick``,
    action_triggered=False): a bare "yes" names no project, so ask again with the
    same bound list and re-arm it. effect: READ."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != PROJECT_ARCHIVE_PICK_KIND or intent_service is None:
        logger.error(
            "project_archive_pick_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    names = [str(n) for n in payload.get("pick_names") or []]
    question = render_several(names)
    record = {
        "workflow_type": PROJECT_ARCHIVE_PICK_WORKFLOW,
        "question": question,
        "pending_action": dict(payload),
        "decline_message": PICK_DECLINE_LINE.format(name=names[0] if names else ""),
    }
    intent_service.workflow_offer_service.set_pending_offer(session_id, record, user_id=user_id)
    return {
        "message": question,
        "intent_data": {
            "category": "portfolio",
            "action": PROJECT_ARCHIVE_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
