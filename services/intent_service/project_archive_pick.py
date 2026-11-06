"""#2271: archive a project by EXACT name; offer a near match, never act on it.

Arch's ruling (b) (decisions.log 2026-11-06 12:51) and CXO's words (12:5x). Every
``archive_project`` turn, whatever rail name reached the entry (``archive_project``,
its alias ``hide_project``, the #2057 legacy hand-off), resolves here from
``CanonicalHandlers._handle_archive_project``:

1. EXACT: the project's whole name equals what the user said, case-insensitively,
   among the person's own ACTIVE projects. The name is the handler's existing
   ``ARCHIVE_PATTERNS`` capture (no new pattern); its leading filler words ("the",
   "my", "project", "called", "named") are dropped one at a time and each remainder,
   before and after ``clean_project_name``, is a candidate the whole stored name must
   equal. Word lists and string comparison only, no regex.
   - one: archived, CXO's archived line;
   - several: nothing archived; an ARMED numbered pick (the #1987 shape), the ids
     bound at ask time, a number answer bound at the pop seam
     (``handle_project_archive_pick_turn``).
   The order is CXO's: exact active, then exact archived, then one near match,
   then none.
2. ALREADY ARCHIVED: no active exact match but an archived one (CXO 12:5x): a
   statement naming the restore phrase; nothing armed, nothing written.
3. NEAR: no exact match, but today's ``find_project_by_name`` ladder (#1857
   normalised, then one substring/prefix candidate) finds one active project: it is
   OFFERED, never acted on. One armed yes/no in CXO's words (offer memo 11-06:
   the typed name, then the candidate), the candidate bound by id; "yes" archives exactly that id (``run_confirm_project_archive_workflow``),
   "no" archives nothing.
4. NONE: the not-found line; nothing archived.

The several-match and near-match records ride the handler result under
``OFFER_RECORD_KEY`` to the rail adapter, which arms them (``arm_pick_from_result``).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)

PROJECT_ARCHIVE_PICK_KIND = "project_archive_pick_question"
# The registered offer-only landing (action_triggered=False): the generic seam's
# ACCEPT path lands a bare "yes" here, which re-asks and re-arms.
PROJECT_ARCHIVE_PICK_WORKFLOW = "clarify_project_archive_pick"
PICK_PENDING_FLAG = "project_archive_pick_pending"
# The near-match yes/no: its #846 kind and its registered WRITE landing (offer
# acceptance only, action_triggered=False), which archives the bound id.
PROJECT_ARCHIVE_CONFIRM_KIND = "project_archive_confirm_question"
PROJECT_ARCHIVE_CONFIRM_WORKFLOW = "confirm_project_archive"
# The result key an armed record (pick or confirm) rides from the handler to the
# rail adapter (run_archive_project_workflow), which arms it.
OFFER_RECORD_KEY = "project_archive_offer"

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
# CXO 11-06 (offer memo): the NEAR-match offer, typed name first, then the one
# candidate. Named *_QUESTION: rendered only by build_confirm_offer, which stores it
# as the record's ``question`` and hands the record back to be armed (#1766 rule).
NEAR_MATCH_QUESTION = 'I don\'t have a project called "{typed}". Archive "{name}" instead? (yes/no)'
# CXO 12:5x: an exact name that matches only an ARCHIVED project.
ALREADY_ARCHIVED_LINE = (
    '"{name}" is already archived. Say "restore project {name}" to bring it back.'
)
# The existing adopted-write decline copy (CXO 2026-10-16), for a "no" to the
# pick or the near-match confirm (CXO kept it 12:5x).
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
    the order the question numbers them), handed back under ``OFFER_RECORD_KEY``
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


def build_confirm_offer(
    principal: Optional[str], project: Any, typed: str, original_message: str
) -> Dict:
    """The #846 record for a NEAR match: one armed yes/no in CXO's words (the typed
    name, then the candidate), the candidate bound by id."""
    name = str(project.name)
    return {
        "workflow_type": PROJECT_ARCHIVE_CONFIRM_WORKFLOW,
        "question": NEAR_MATCH_QUESTION.format(typed=typed, name=name),
        "pending_action": {
            "kind": PROJECT_ARCHIVE_CONFIRM_KIND,
            "action": PROJECT_ARCHIVE_CONFIRM_WORKFLOW,
            "user_id": principal,
            "project_id": str(project.id),
            "project_name": name,
            "original_message": original_message,
            "summary": f'archive the project "{name}"',
        },
        "decline_message": PICK_DECLINE_LINE.format(name=name),
    }


async def archive_by_name(
    *,
    capture: str,
    lookup_name: str,
    user_id: str,
    original_message: str,
    portfolio_service: Any,
) -> Dict[str, Any]:
    """``_handle_archive_project``'s resolution (see the module docstring)."""
    from services.shared_types import IntentCategory

    category = IntentCategory.PORTFOLIO.value
    matches = exact_matches(await portfolio_service.list_active_projects(user_id=user_id), capture)
    if len(matches) == 1:
        return await _archive_one(portfolio_service, matches[0], user_id)
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
            OFFER_RECORD_KEY: offer,
            "requires_clarification": True,
        }
    archived = exact_matches(
        await portfolio_service.list_archived_projects(user_id=user_id), capture
    )
    if archived:
        name = str(archived[0].name)
        return {
            "message": ALREADY_ARCHIVED_LINE.format(name=name),
            "intent": {
                "category": category,
                "action": "archive_project",
                "confidence": 1.0,
                "context": {"project_name": name, "status": "already_archived"},
            },
            "requires_clarification": False,
        }
    # Today's ladder, on the name the user said (the capture without its leading
    # filler words, as the exact candidates above), else the handler's own name.
    typed = display_name(capture) or lookup_name
    near = await portfolio_service.find_project_by_name(name=typed, user_id=user_id)
    if near is not None:
        offer = build_confirm_offer(user_id, near, typed, original_message)
        logger.info("project_archive_near_match_offered")
        return {
            "message": offer["question"],
            "intent": {
                "category": category,
                "action": PROJECT_ARCHIVE_CONFIRM_WORKFLOW,
                "confidence": 0.8,
                "context": {"project_name": str(near.name), "near_match": True},
                PICK_PENDING_FLAG: True,
            },
            OFFER_RECORD_KEY: offer,
            "requires_clarification": True,
        }
    searched = display_name(capture)
    return {
        "message": NOT_FOUND_LINE.format(name=searched),
        "intent": {
            "category": category,
            "action": "project_not_found",
            "confidence": 0.8,
            "context": {"searched_name": searched},
        },
        "requires_clarification": False,
    }


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
    here; a several-match pick or near-match confirm record is armed in the #846 one-slot store
    before the question is shown. Without a session or store the record is
    dropped and the flag cleared, so the reply is never marked as armed."""
    record = result.pop(OFFER_RECORD_KEY, None) if isinstance(result, dict) else None
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
        kind=(record.get("pending_action") or {}).get("kind"),
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


async def run_confirm_project_archive_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``confirm_project_archive``,
    action_triggered=False): the "yes" to a near-match offer archives exactly the
    project bound by id at offer time, under the turn's own principal. effect: WRITE."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    if payload.get("kind") != PROJECT_ARCHIVE_CONFIRM_KIND or not payload.get("project_id"):
        logger.error("project_archive_confirm_missing_or_foreign_payload", kind=payload.get("kind"))
        return None
    from services.intent_service.reminder_clear import _principal_mismatch

    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "project_archive_confirm_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": {
                "category": "portfolio",
                "action": PROJECT_ARCHIVE_CONFIRM_WORKFLOW,
                "principal_mismatch": True,
            },
            "requires_clarification": False,
        }
    result = await _archive_bound_id(str(payload["project_id"]), str(user_id))
    return {
        "message": result["message"],
        "intent_data": result["intent"],
        "requires_clarification": False,
    }
