"""#1886 — the add-project name-clarify carrier (the #846/#1190 pending-offer
idiom), replacing ``_handle_add_project``'s old onboarding-session
bookkeeping. Mirrors ``services/intent_service/todo_handlers.py``'s
reminder-task carrier EXACTLY (``CLARIFY_REMINDER_TASK_WORKFLOW`` /
``REMINDER_TASK_QUESTION_KIND`` / ``handle_reminder_task_turn`` /
``run_clarify_reminder_task_workflow``) — Architect's ruling, 2026-10-06,
binding on #1886: a durable per-turn carrier, NOT a re-registered
``OnboardingProcessAdapter``.

**The defect this closes** (#1867 finding 1): ``_handle_add_project``'s own
no-name ask used to create a ``PortfolioOnboardingManager`` session (the
DEREGISTERED onboarding process, ADR-059 "on ice") and read it back next
turn via a private ``_pending_ask()`` helper, gated on the next turn's text
containing an "add"/"create"/"new project" token (the ask's own taught
copy). A bare-name reply ("Klatch") carries none of those tokens, so it
never re-entered the handler and the ask silently orphaned — hours later, a
fresh no-name "add a project" wrongly hit the "I still did not catch a
project name" branch instead of asking fresh. This carrier replaces that
bookkeeping with the SAME durable per-turn store every other #1654-class
clarify uses, so the answer binds regardless of what words it contains.

**Branch-3 without re-entering the handler.** The original three-branch
design (name present → create; no name, first ask → ask once; no name,
already asked → say so and drop it) collapses here to two branches inside
``CanonicalHandlers._handle_add_project`` (name present / name absent), plus
this carrier's own turn handling for "already asked." The tricky part: a
BARE restatement of the imperative ("add project" again, no name) matches
the same "full restatement" family a GENUINE restatement-with-a-name does,
and the carrier's general rule for a full restatement is to release (return
``None``) so it routes normally. Releasing a bare, nameless restatement
would reach ``_handle_add_project`` fresh with no pending offer, which would
render the IDENTICAL first ask again — a visible double-prompt the
transcript must never show. So the bare case is resolved HERE, in the
restatement branch, without ever releasing: only a restatement that itself
carries a name releases to the ordinary create path.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

import structlog

from services.shared_types import IntentCategory as IntentCategoryEnum

logger = structlog.get_logger()

# --- the carrier's identity --------------------------------------------

ADD_PROJECT_NAME_QUESTION_KIND = "add_project_name_question"

# Generic-accept landing (a bare "yes" doesn't answer "what should I call
# it?") — registered action_triggered=False in workflow_entries (the
# #1605/#1648/#1654 clarify precedent).
CLARIFY_ADD_PROJECT_NAME_WORKFLOW = "clarify_add_project_name"


def build_add_project_name_offer(original_message: str, user_id, question=None) -> Dict[str, Any]:
    """The #846 pending-offer record arming the add-project name question
    (#1886). Mirrors ``todo_handlers.build_reminder_task_offer`` exactly —
    carries the ORIGINAL message (strings only, so the payload snapshots
    cleanly) so a restatement's own repo clause can still be recovered at
    answer time. ``question`` (#1665): the ALREADY-RENDERED ask the caller
    returns this turn — stored verbatim, never re-rendered."""
    return {
        "workflow_type": CLARIFY_ADD_PROJECT_NAME_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": ADD_PROJECT_NAME_QUESTION_KIND,
            "action": "add_project",
            "original_message": original_message,
            "user_id": str(user_id) if user_id else None,
            "summary": "add a project",
        },
        "decline_message": "Okay — I haven't added a project. Nothing was created.",
    }


# A restatement of the add/create-project imperative ("add project", "add
# project Foo", "create a new project called Foo") — the #1856 family's own
# ADD_PROJECT_PATTERNS (services/onboarding/portfolio_service.py), narrowed
# to a bare detector: #1886 only needs "is this the imperative again", not
# the capture group. Deliberately matches REGARDLESS of whether a name
# follows — see the module docstring for why the no-name case still needs
# special handling rather than a blind release.
_ADD_PROJECT_RESTATEMENT_RE = re.compile(
    r"\b(?:add|create|start|set\s+up)\s+(?:a\s+|an\s+|the\s+|my\s+)?(?:new\s+)?projects?\b",
    re.IGNORECASE,
)

_NAME_REASK_TAIL = (
    "What should the project be called? Say its name (the repo part is "
    "optional), or say 'no' to drop it."
)


def _not_a_name_reply(corrected: bool) -> Dict[str, Any]:
    """The honest #1856 branch-(3) copy: nothing created, say why, re-offer
    the one-liner. Byte-for-byte what ``CanonicalHandlers._handle_add_project``
    returned pre-#1886 for this case — only the carrier plumbing moved."""
    from services.intent_service.canonical_handlers import CanonicalHandlers

    lead = (
        "Understood, and sorry for the loop — that was not a project "
        "name and I did not get one, so I have not created anything."
        if corrected
        else "I still did not catch a project name in that, so I have " "not created anything."
    )
    message = (
        f"{lead} I have dropped the half-started add. When you want "
        f"it, put the whole thing in one line: {CanonicalHandlers._ADD_PROJECT_IMPERATIVE}."
    )
    return {
        "message": message,
        "intent_data": {
            "category": IntentCategoryEnum.PORTFOLIO.value,
            "action": "add_project_abandoned",
            "confidence": 1.0,
            "context": {
                "needs": "project_name",
                "user_corrected": corrected,
            },
        },
        "requires_clarification": False,
    }


def _rearm_name_question(intent_service, session_id, user_id, pending_offer) -> bool:
    """Re-arm the SAME offer (the pop already consumed it; a re-ask turn
    must re-store it or the next answer has nothing to bind to). Returns
    False on a store failure so the copy never claims a binding that isn't
    there. #1665: the re-armed record's open question becomes the re-ask
    tail every re-ask turn renders (set BEFORE the store — what's stored is
    what's said). Mirrors ``todo_handlers._rearm_task_question`` exactly."""
    try:
        pending_offer["question"] = _NAME_REASK_TAIL
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
        return True
    except Exception as e:  # silent-ok: #1886 — a store failure must not crash the turn; logged ERROR, and callers keep the user-facing copy honest
        logger.error("add_project_name_question_rearm_failed", error=str(e))
        return False


def _name_reask(detail: str, rearmed: bool) -> Dict[str, Any]:
    """The honest re-ask shape: nothing created, here's why, here's what
    works. Mirrors ``todo_handlers._task_reask`` exactly."""
    if rearmed:
        tail = _NAME_REASK_TAIL
    else:
        tail = (
            "I couldn't keep the question open either — ask me again "
            "('add project [name]') and I'll set it fresh."
        )
    return {
        "message": f"No project has been created yet — {detail} {tail}",
        "intent_data": {
            "category": IntentCategoryEnum.PORTFOLIO.value,
            "action": "add_project_needs_name",
            "add_project_name_question_pending": rearmed,
            "add_project_name_reasked": True,
        },
        "requires_clarification": True,
    }


async def handle_add_project_name_turn(
    pending_offer: dict,
    message: str,
    *,
    session_id: str,
    user_id,
    intent_service,
) -> Optional[Dict[str, Any]]:
    """#1886 — kind-specific turn handling for a pending add-project NAME
    question (the carrier replacing ``_handle_add_project``'s old
    onboarding-session bookkeeping), run at the offer seam BEFORE any
    classification surface (the #1605/#1648/#1654 sanctioned
    handler-internal seam; the pop already happened). Mirrors
    ``todo_handlers.handle_reminder_task_turn`` exactly, with one
    add-project-specific branch split (see the module docstring): a full
    restatement carrying its own name releases; a BARE restatement (still
    no name) is answered here directly, never released, so the identical
    first ask can never render twice in a row.

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` falls through to the generic offer flow
    (declines and bare exits drop honestly via ``decline_message``; a full
    restatement carrying its own name and pre-classifier-claimed commands
    abandon via the pop and route normally).
    """
    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )
    from services.intent_service.destructive_confirm import detect_bare_exit
    from services.onboarding.portfolio_service import (
        extract_add_project_slots,
        is_plausible_project_name,
    )

    payload = pending_offer.get("pending_action") or {}
    text = (message or "").strip()
    if not text:
        return None

    # Principal binding (the #1605 discipline): the offer belongs to the
    # user who asked — a different principal's turn must not create under it.
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(user_id) != str(offer_user):
        logger.warning(
            "add_project_name_question_principal_mismatch",
            offer_user=offer_user,
            turn_user=str(user_id),
        )
        return {
            "message": "Let's hold off on that — nothing has been created.",
            "intent_data": {
                "category": IntentCategoryEnum.PORTFOLIO.value,
                "action": "add_project",
                "principal_mismatch": True,
            },
        }

    if detect_bare_exit(text):
        return None  # generic flow → honest decline via decline_message

    _axes = declared_axes_for_workflow(CLARIFY_ADD_PROJECT_NAME_WORKFLOW)
    verdict = evaluate_acceptance(
        text,
        effect=_axes[0] if _axes else None,
        outwardness=_axes[1] if _axes else None,
        armed_question=pending_offer.get("question"),  # #1665: from the record
    )
    if verdict is AcceptanceVerdict.DECLINE:
        return None  # generic flow → honest decline via decline_message

    if _ADD_PROJECT_RESTATEMENT_RE.search(text):
        restated = extract_add_project_slots(text)
        if restated.get("name"):
            # A full restatement carrying its own name (and maybe repo) —
            # abandon via the pop and let it route normally; the ordinary
            # add-project path re-extracts and creates it (#1856 branch 1).
            logger.info(
                "add_project_name_question_restatement_released",
                session_id=session_id,
            )
            return None
        # Bare restatement, still no name — this IS the "second no-name
        # add turn" (#1867 finding 1). Resolved HERE, never releasing back
        # to _handle_add_project, which has no memory of the first ask and
        # would render the identical Q1 again. Not re-armed, same as any
        # other not-a-name answer below.
        logger.info(
            "add_project_name_question_bare_restatement",
            session_id=session_id,
        )
        return _not_a_name_reply(corrected=not is_plausible_project_name(text))

    # ARM SURVIVAL — the SILENT LOW-tier form (CXO's survival-must-be-stated
    # rule): a STATE_QUESTION verdict returns None, landing the turn on the
    # generic seam's already-adopted READ branch — that branch re-arms THIS
    # offer silently and normal processing answers the question.
    if verdict is AcceptanceVerdict.STATE_QUESTION:
        logger.info(
            "add_project_name_question_state_question_falls_through",
            session_id=session_id,
        )
        return None

    if verdict is AcceptanceVerdict.ACCEPT:
        # A bare "yes" (or an accept-led / crisp-confirm turn) doesn't name
        # a project — the honest re-ask, never a silent abandon.
        rearmed = _rearm_name_question(intent_service, session_id, user_id, pending_offer)
        logger.info(
            "add_project_name_question_reasked",
            session_id=session_id,
            rearmed=rearmed,
        )
        return _name_reask("I still need to know what to call it.", rearmed)

    # Off-intent: a turn the pre-classifier claims deterministically is
    # another product command — release it (routes normally; the question
    # is abandoned per the carrier's rules). Mirrors
    # handle_reminder_task_turn's off-intent release, with ONE add-project-
    # specific exclusion: PORTFOLIO_PATTERNS claims almost any utterance
    # that merely MENTIONS "project" as manage_portfolio with no slots
    # (confirmed: "this is not the name of the new project at all" claims
    # this way) — the carrier's OWN family, not a competing command.
    # Releasing those would bounce straight back to _handle_add_project
    # fresh with the SAME no-name text, rendering the identical first ask
    # again. Only a claim OUTSIDE this family counts as off-intent.
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None and claimed.action not in ("manage_portfolio", "add_project"):
        logger.info(
            "add_project_name_question_command_released",
            session_id=session_id,
            claimed_action=claimed.action,
        )
        return None

    # The turn IS the answer attempt. "add project" and similar bare
    # imperatives are deliberately NOT treated as plausible names (the
    # restatement branch above already owns that shape); this check is for
    # free-text answers that are neither a restatement nor a command.
    if not is_plausible_project_name(text):
        return _not_a_name_reply(corrected=True)

    original_message = (payload.get("original_message") or "").strip()
    repo_name = extract_add_project_slots(original_message).get("repo")
    canonical_handlers = intent_service.canonical_handlers
    canonical_result = await canonical_handlers._create_or_report_project(
        name=text,
        repo_name=repo_name,
        session_id=session_id,
        user_id=user_id or offer_user,
    )
    return {
        "message": canonical_result["message"],
        "intent_data": canonical_result["intent"],
        "requires_clarification": canonical_result.get("requires_clarification", False),
    }


async def run_clarify_add_project_name_workflow(
    session_id: str,
    user_id=None,
    context=None,
):
    """Generic-accept landing for the add-project name question (defense in
    depth — the kind-specific seam claims accepts itself, but a registered
    landing means a stray generic accept can never fall into
    ``_handle_unknown_intent`` and reach the floor): re-ask and re-arm.
    effect: READ (nothing written; the real write happens on an ANSWERED
    turn at the offer seam). Mirrors
    ``todo_handlers.run_clarify_reminder_task_workflow`` exactly."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != ADD_PROJECT_NAME_QUESTION_KIND or intent_service is None:
        logger.error(
            "clarify_add_project_name_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    offer = {
        "workflow_type": CLARIFY_ADD_PROJECT_NAME_WORKFLOW,
        "pending_action": dict(payload),
        "decline_message": "Okay — I haven't added a project. Nothing was created.",
    }
    rearmed = _rearm_name_question(intent_service, session_id, user_id, offer)
    return _name_reask("I still need to know what to call it.", rearmed)
