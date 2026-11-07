"""#2308 (link_repo slice, pulled forward by PPM 11-06 16:24; #2271): link_repo's held
write ask names the thing.

Arch 11-06 15:59 (4)(b): the ask reads ONLY the handler's own resolver
(``canonical_handlers.resolve_link_repo_request``, the parse ``_handle_link_repo``
has always run, lifted out of the method in the same file so both read the one
function; no new pattern, and the file's binder count is unchanged), binds what it
shows (13:23), and writes nothing before "yes". The alias rules for link_repo stand:
it never creates a project, and it asks and writes nothing unless both an owner/name
and an EXISTING project are found.

CXO's words (11-06 15:58, restated final 16:33), on a held turn
(``write_confirm_words.link_repo_write_ask``):

- both resolved: ``Link {owner/name} to {project}? (yes/no)``, the values bound;
- project resolved, repo missing: ``Which repository should I link to {project}? Say
  it as owner/name.``, ARMED here (the #1730 rule: an ask that cannot be armed is not
  asked); the answer's owner/name, read with the same parse, arms the bound yes/no;
- a named project that doesn't exist: the handler's not-found line, a statement;
- neither (and a repo with no project, which CXO's table has no row for): the
  not-sure line, nothing armed.

``{project}`` is the project's stored name as found; the repo is as the person typed
it. The armed which-repository record mirrors ``project_archive_pick``: its own kind,
a registered READ landing for a bare "yes" (re-asks, re-arms), an answer-turn handler
at the pop seam with the principal check, and release of anything else.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)

LINK_REPO_REPOSITORY_KIND = "link_repo_repository_question"
# The registered offer-only landing (action_triggered=False): the generic seam's
# ACCEPT path lands a bare "yes" here, which re-asks and re-arms.
CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW = "clarify_link_repo_repository"
REPOSITORY_PENDING_FLAG = "link_repo_repository_question_pending"

# CXO 11-06 15:58 (verbatim). Named *_QUESTION: rendered only where the record that
# stores it as ``question`` is armed (the #1766 rule).
WHICH_REPOSITORY_QUESTION = "Which repository should I link to {project}? Say it as owner/name."
# The handler's existing not-found reply (moved here so the ask and the handler say
# the same line). A statement; nothing is armed.
PROJECT_NOT_FOUND_LINE = (
    "I couldn't find a project called '{name}'. "
    "Check the name and try again, or say 'show my projects' "
    "to see your project list."
)
# PROPOSED (CXO to judge): a "no" to the which-repository question, and a short
# answer that carries no owner/name. Statements; nothing is armed.
REPOSITORY_DECLINE_LINE = "Okay, I won't link a repository to {project}. Nothing has been changed."
NO_REPOSITORY_IN_ANSWER_LINE = (
    "I didn't see a repository in owner/name form, so I haven't linked anything to {project}."
)
PRINCIPAL_MISMATCH_LINE = "Let's hold off on that — nothing has been changed."

# An answer without an owner/name gets the no-repository statement only when it is
# one bare word (a repo named without its owner, "piper-test-activity") that surface
# 1 doesn't claim. Anything longer ("show my todos") is a new request and routes
# normally: an unrelated command is never swallowed as a failed answer.
_MAX_ANSWER_WORDS = 1


async def find_link_project(project_name: str, user_id: str) -> Any:
    """The handler's own project lookup (owner-scoped, active, the #1857 ladder).
    A read; nothing is written."""
    from services.database.repositories import ProjectRepository
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        return await ProjectRepository(session).find_by_name(name=project_name, owner_id=user_id)


def _repository_record(
    principal: Optional[str], project_id: str, project_name: str, original_message: str
) -> Dict[str, Any]:
    question = WHICH_REPOSITORY_QUESTION.format(project=project_name)
    return {
        "workflow_type": CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": LINK_REPO_REPOSITORY_KIND,
            "action": CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW,
            "user_id": principal,
            "project_id": project_id,
            "project_name": project_name,
            "original_message": original_message,
            "summary": f"link a repository to {project_name}",
        },
        "decline_message": REPOSITORY_DECLINE_LINE.format(project=project_name),
    }


def arm_which_repository(
    offers: Any,
    session_id: Optional[str],
    principal: Optional[str],
    project: Any,
    original_message: str,
) -> Optional[str]:
    """Arm CXO's which-repository question for ``project`` and return it, or None
    when there is nowhere to arm it (then it is not asked)."""
    if offers is None or not session_id:
        logger.warning("link_repo_repository_question_not_armed", session_id=session_id)
        return None
    record = _repository_record(principal, str(project.id), str(project.name), original_message)
    offers.set_pending_offer(session_id, record, user_id=principal)
    logger.info("link_repo_repository_question_armed", session_id=session_id)
    return record["question"]


def _bound_confirm(
    principal: str, repo_name: str, project_id: str, project_name: str, original_message: str
) -> Any:
    """The #1190 confirm for an answered repository: a link_repo Intent with the
    values bound (``write_ask_bound``), so "yes" writes exactly these."""
    from services.domain.models import Intent
    from services.intent_service.destructive_confirm import build_confirmation_offer
    from services.intent_service.write_confirm_words import (
        bind_write_values,
        link_repo_confirm_words,
    )
    from services.shared_types import IntentCategory

    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="link_repo",
        confidence=1.0,
        original_message=original_message,
        context={"original_message": original_message, "user_id": principal},
    )
    bind_write_values(
        intent,
        "link_repo",
        repo_name=repo_name,
        project_name=project_name,
        project_id=project_id,
    )
    return build_confirmation_offer(intent, link_repo_confirm_words(repo_name, project_name))


async def handle_link_repo_repository_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam (before generic accept/decline). An answer
    carrying an owner/name (the same parse) arms the bound ``Link … to …? (yes/no)``;
    nothing is written here. ``None`` falls through to the generic seam: a decline
    (``decline_message``), a bare "yes" (the registered landing re-asks), a state
    question, a full new request naming a project, or any claimed or longer command
    (routes normally; the record is already popped). A one-word answer with no
    owner/name is a statement; nothing armed."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != LINK_REPO_REPOSITORY_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None
    from services.intent_service.reminder_clear import _principal_mismatch

    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "link_repo_repository_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": {
                "category": "portfolio",
                "action": CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )

    axes = declared_axes_for_workflow(CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW)
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
        return None

    project_name = str(payload.get("project_name") or "")
    project_id = str(payload.get("project_id") or "")
    from services.intent_service.canonical_handlers import resolve_link_repo_request

    repo_name, named_project = resolve_link_repo_request(text)
    if repo_name and not named_project:
        offer = _bound_confirm(
            str(user_id),
            repo_name,
            project_id,
            project_name,
            str(payload.get("original_message") or ""),
        )
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, offer.offer, user_id=str(user_id)
        )
        logger.info("link_repo_repository_bound_confirm_armed", session_id=session_id)
        return {
            "message": offer.question,
            "intent_data": {
                "category": "portfolio",
                "action": "link_repo",
                "confidence": 1.0,
                "destructive_confirmation_pending": True,
            },
            "requires_clarification": True,
        }
    if repo_name:
        return None  # a full request naming its own project: routes normally

    from services.intent_service.pre_classifier import PreClassifier

    if PreClassifier.pre_classify(text) is not None or len(text.split()) > _MAX_ANSWER_WORDS:
        logger.info("link_repo_repository_question_released", session_id=session_id)
        return None
    return {
        "message": NO_REPOSITORY_IN_ANSWER_LINE.format(project=project_name),
        "intent_data": {
            "category": "portfolio",
            "action": "link_repo",
            "confidence": 1.0,
            "context": {"project_name": project_name, "status": "no_repository_named"},
        },
        "requires_clarification": False,
    }


async def run_clarify_link_repo_repository_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_link_repo_repository``,
    action_triggered=False): a bare "yes" names no repository, so ask again for the
    same bound project and re-arm it. effect: READ."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != LINK_REPO_REPOSITORY_KIND or intent_service is None:
        logger.error(
            "link_repo_repository_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    project_name = str(payload.get("project_name") or "")
    record = _repository_record(
        payload.get("user_id"),
        str(payload.get("project_id") or ""),
        project_name,
        str(payload.get("original_message") or ""),
    )
    intent_service.workflow_offer_service.set_pending_offer(session_id, record, user_id=user_id)
    return {
        "message": record["question"],
        "intent_data": {
            "category": "portfolio",
            "action": CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW,
            REPOSITORY_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
