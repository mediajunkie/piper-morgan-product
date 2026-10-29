"""#2184 — the milestones list ARMS an exact-title milestone pick (Arch's ruling 2026-10-28 12:45).

xian's served exchange (alpha a1f46faafc, 10:12 PT): "can you show me issues from
just one milestone?", then "MVP". (Corrected 2026-10-29, Arch's diagnosis of the
49e0904c3c FAIL: turn 1 routes CLARIFY with no args and a MODEL composes the
which-milestone question, so this module's arm site never ran. Turn 1 reaches the
milestones read only through the router, a ``list_milestones`` description under
rule 7.) The second turn routes CLARIFY @0.30 at the router (×3 on main, Lead's
control), nothing claims it, and the floor composed three real issue numbers from
the priority slice as "the MVP milestone's" (#2042's class). PPM's close bar for
#2184 is that two-step exchange, served.

Rung 1 (code holds the truth): the only turn on which a bare milestone title has
one reading is the turn after this handler's own read printed that title. So
``_handle_list_milestones_query`` arms a pick on the titles it rendered, carrying
the repo the list was read from (Arch's condition 1: the issues read without a
repo is ``assignee:@me`` across all repos and its count would disagree with the
"3 open" just shown). On the next turn, at the pop seam before classification,
a message that is EXACTLY one listed title (case, whitespace, quotes and trailing
punctuation trimmed — condition 2) runs the issues read with that milestone and
that repository through the #2186 handler and rail. Anything else pops and routes
as today (one turn). Numbers do not bind: the milestones reply renders none
(condition 3). The arm happens ONLY from this handler's read, never from a
floor-composed list (condition 4, D2).

Carrier: the #1906/#1987 pick shape on the #846 one-slot pending-offer store —
the record carries the candidates bound at arm time; the bind is an exact match
in code; a bare affirmative lands on the registered re-ask workflow
(``clarify_milestone_pick``, action_triggered=False). No regex (the #1595 ratchet
is untouched); the only text reads are strip/casefold.

#2184 two-step (Arch 2026-10-29, comment 6501638087; CXO 2026-10-29 09:01):
when the pick arms, the milestones reply ENDS with
``MILESTONE_PICK_ARM_QUESTION`` (the handler appends it only when
``arm_milestone_pick`` returned True), so a user who asked for "issues from
just one milestone" is asked which one by code that read and rendered the
titles. The record's stored ``question`` stays empty and its decline copy
neutral: a decline after a milestones list means nothing happened and says so. The pick is skipped when the list armed a
remainder offer (a capped list) — both live in the same one-slot store and the
printed "say the word" promise wins.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()

MILESTONE_PICK_KIND = "milestone_pick_question"
MILESTONE_PICK_WORKFLOW = "clarify_milestone_pick"
PICK_PENDING_FLAG = "milestone_pick_pending"
MAX_TITLES = 50

# CXO ruled 13:04 10-28: a silent arm's decline has nothing to refuse; the shortest acknowledgement.
PICK_DECLINE_LINE = "Okay."
# CXO 2026-10-29 09:01: the closing line of a milestones reply that armed the pick,
# appended by _handle_list_milestones_query only when arm_milestone_pick returned True
# (CXO: on a plain "list my milestones" too, since the handler cannot tell the two
# asks apart). Named *_QUESTION: the #1766 census's named-question-holder rule.
MILESTONE_PICK_ARM_QUESTION = "Which milestone do you want to see issues from? Say its name."
# CXO 13:04 10-28: no titles and no ellipsis; the list is on screen. Named *_QUESTION:
# it is rendered only by run_clarify_milestone_pick_workflow, which stores it on the
# #846 record and arms it (the #1766 census's named-question-holder rule).
MILESTONE_PICK_REASK_QUESTION = "Which milestone? Say its name from the list above."


def normalize_title(text: Optional[str]) -> str:
    """Exact-match key: whitespace collapsed, surrounding quotes/backticks and
    trailing sentence punctuation trimmed, casefolded. No regex."""
    if not text:
        return ""
    s = " ".join(str(text).split())
    s = s.strip("\"'`“”‘’")
    s = s.rstrip(".!?,;:")
    s = s.strip("\"'`“”‘’")
    return s.casefold()


def _record(
    principal: Optional[str],
    titles: List[str],
    repository: Optional[str],
    original_message: str,
) -> Dict[str, Any]:
    return {
        "workflow_type": MILESTONE_PICK_WORKFLOW,
        "question": "",
        "pending_action": {
            "kind": MILESTONE_PICK_KIND,
            "action": MILESTONE_PICK_WORKFLOW,
            "user_id": principal,
            "pick_titles": list(titles),
            "repository": repository,
            "original_message": original_message,
            "summary": "pick a milestone to list its issues",
        },
        "decline_message": PICK_DECLINE_LINE,
    }


def arm_milestone_pick(
    *,
    session_id: Optional[str],
    principal: Optional[str],
    offer_service: Any,
    titles: List[str],
    repository: Optional[str],
    original_message: str,
) -> bool:
    """The ARM half, called by ``_handle_list_milestones_query`` after its own
    successful, non-empty read. Returns True when armed. Never raises."""
    if not session_id or offer_service is None:
        return False
    clean = [t for t in (titles or []) if isinstance(t, str) and normalize_title(t)]
    if not clean:
        return False
    clean = clean[:MAX_TITLES]
    try:
        offer_service.set_pending_offer(
            session_id, _record(principal, clean, repository, original_message), user_id=principal
        )
    except Exception as e:  # silent-ok: logged; an un-armed pick leaves today's behaviour
        logger.warning("milestone_pick_arm_failed", error=str(e), session_id=session_id)
        return False
    logger.info(
        "milestone_pick_armed",
        session_id=session_id,
        titles=len(clean),
        repository=repository,
    )
    return True


def match_title(message: str, titles: List[str]) -> Optional[str]:
    """The listed title the message IS (exact after normalisation), else None."""
    key = normalize_title(message)
    if not key:
        return None
    for t in titles or []:
        if normalize_title(t) == key:
            return t
    return None


async def handle_milestone_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam (before generic accept/decline). An
    exact listed title runs the issues read with that milestone and the listed
    repository (both CODE-bound into the intent, so the #1976 word-set guard,
    meant for LLM-written args, cannot drop them). Anything else returns None:
    the generic seam then handles a decline (neutral line), a bare accept (the
    registered re-ask) or an unrelated command (routes normally; the offer is
    already popped)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != MILESTONE_PICK_KIND:
        return None
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(offer_user) != str(user_id):
        logger.warning(
            "milestone_pick_principal_mismatch", offer_user=offer_user, turn_user=user_id
        )
        return None
    titles = payload.get("pick_titles") or []
    title = match_title(message or "", titles)
    if title is None:
        return None
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    repository = payload.get("repository")
    # #2199 (xian's row-0 read on b9a8a43600, 2026-10-29 12:50): this Intent is
    # built HERE, not at the host boundary, so nothing had stamped the request
    # principal onto it. `_principal_from_intent` then read None, the connector
    # read degraded for want of a credential, and the handler's native fallback
    # resolved no default repo for a None user: the user who had just been
    # promised "Say its name" got "I couldn't tell which repository you mean."
    # The principal is the one the arm recorded (checked equal to this turn's
    # user above), written under the same key process_intent uses.
    principal = offer_user or user_id
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        context={
            "original_message": message,
            "user_id": str(principal) if principal else None,
            "list_scope_milestone": title,
            "list_scope_repository": repository if isinstance(repository, str) else None,
            "milestone_pick_bound": True,
        },
    )
    # #1459: the ONE writer for the user's message (both surfaces together).
    intent.bind_original_message(message)
    logger.info(
        "milestone_pick_bound",
        session_id=session_id,
        milestone=title,
        repository=repository,
    )
    result = await intent_service._handle_list_issues_query(
        intent, "milestone_pick", session_id=session_id
    )
    return {
        "message": getattr(result, "message", ""),
        "intent_data": getattr(result, "intent_data", None) or {},
        "requires_clarification": False,
    }


async def run_clarify_milestone_pick_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_milestone_pick``,
    action_triggered=False): a bare "yes" names no milestone — ask which, and
    re-arm the same titles. effect: READ."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != MILESTONE_PICK_KIND or intent_service is None:
        logger.error(
            "milestone_pick_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    titles = [t for t in (payload.get("pick_titles") or []) if isinstance(t, str)]
    question = MILESTONE_PICK_REASK_QUESTION
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        _record(
            payload.get("user_id"),
            titles,
            payload.get("repository"),
            payload.get("original_message") or "",
        )
        | {"question": question},
        user_id=user_id,
    )
    return {
        "message": question,
        "intent_data": {
            "category": "query",
            "action": MILESTONE_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }


__all__ = (
    "MILESTONE_PICK_KIND",
    "MILESTONE_PICK_WORKFLOW",
    "PICK_PENDING_FLAG",
    "MILESTONE_PICK_ARM_QUESTION",
    "normalize_title",
    "match_title",
    "arm_milestone_pick",
    "handle_milestone_pick_turn",
    "run_clarify_milestone_pick_workflow",
)
