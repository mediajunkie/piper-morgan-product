"""
Workflow entry points for the workflow dispatcher.

ADR-059: Each function here is an entry point registered in the
workflow dispatcher. Adding a new workflow means:
1. Write an async entry point function here
2. Register it in register_default_workflows()

No switch statements. No modifying intent_service.py.
"""

from typing import Any, Dict, Optional

import structlog

from services.intent_service import workflow_dispatcher as _workflow_dispatcher
from services.intent_service.reminder_clear import (
    run_clarify_reminder_clear_verb_workflow,
    run_clear_reminders_delete_workflow,
    run_reminder_clear_correction_workflow,
    run_reminder_clear_pick_target_workflow,
)
from services.intent_service.standup_todo_offer import (
    run_standup_complete_todo_workflow,
)
from services.intent_service.todo_handlers import (
    run_clarify_reminder_task_workflow,
    run_clarify_reminder_time_workflow,
)
from services.intent_service.unarmed_offer import FLOOR_BOUND_OFFER_KIND
from services.intent_service.workflow_dispatcher import (
    WorkflowEntry,
    register_workflow,
)
from services.shared_types import EffectClass, IntentCategory, Outwardness

logger = structlog.get_logger(__name__)


async def start_meeting_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Start the meeting slot-filling workflow.

    Extracted from intent_service.py soft offer acceptance (line 454-489).
    Uses the slot_filling_adapter to gather meeting details.
    """
    from services.personality.formality import DEFAULT_WARMTH
    from services.slot_filling.slot_template import MEETING_TEMPLATE

    ctx = context or {}
    trigger_message = ctx.get("trigger_message", "")
    formality_baseline = ctx.get("formality_baseline", DEFAULT_WARMTH)
    slot_filling_adapter = ctx.get("slot_filling_adapter")

    if slot_filling_adapter is None:
        logger.error("meeting_workflow_missing_slot_filling_adapter")
        return None

    # Import here to avoid circular dependency
    from services.intent_service.soft_invocation import WorkflowOfferService

    workflow_offer_service = WorkflowOfferService()

    slot_response = await slot_filling_adapter.manager.start_filling(
        user_id=user_id,
        session_id=session_id,
        template=MEETING_TEMPLATE,
        initial_message=trigger_message,
        formality_baseline=formality_baseline,
    )

    acceptance_msg = workflow_offer_service.format_acceptance(
        "meeting", formality_baseline=formality_baseline
    )
    combined_msg = f"{acceptance_msg}\n\n{slot_response.message}"

    # Return the data the caller needs to build IntentProcessingResult
    return {
        "message": combined_msg,
        "intent_data": {
            "category": "soft_offer_accepted",
            "action": "meeting",
            "context": {
                "slot_filling_active": True,
                "filled_slots": slot_response.filled_slots,
                "template_name": slot_response.template_name,
            },
        },
    }


async def run_update_document_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Action-dispatch entry point for document updates (#1124 cohort 1).

    Unlike `start_meeting_workflow` (offer-triggered, multi-turn slot gathering),
    this is a direct-action workflow: the classifier already produced the
    `update_document` action, and `_handle_update_document_notion` already does
    LLM slot extraction via DOCUMENT_UPDATE_TEMPLATE (#1121). The migration here
    is purely about dispatch — routing through the workflow registry instead of
    the hand-coded `elif intent.action in [...]` chain in intent_service.py.

    The handler is an instance method holding service state (notion router, llm
    client), so the action-dispatch rail passes the IntentService plus the
    classified intent/workflow_id through `context`; this entry point invokes the
    existing handler unchanged. Returns the handler's IntentProcessingResult, or
    None on a wiring error (dispatcher then routes to the conversational floor).
    """
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    workflow_id = ctx.get("workflow_id")

    if intent_service is None or intent is None:
        logger.error(
            "update_document_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None

    return await intent_service._handle_update_document_notion(intent, workflow_id, session_id)


async def run_changes_query_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Action-dispatch entry point for "what changed since X?" (#1124 cohort 1,
    migration #3 — DISPATCH migration).

    Scope note: this routes the stable `changes_query` action family off the
    `elif` chain and through the workflow registry (the #1124 structural goal).
    `_handle_changes_query` is reused UNCHANGED — it keeps its keyword-based
    `_parse_time_expression` (days-as-int), which is an acceptable bounded
    temporal parser (not the high-severity content-regex that update-document
    had). Replacing it with LLM timeframe slot-extraction is a deferred follow-on
    tracked in the roadmap, not part of this dispatch migration.

    Returns the handler's IntentProcessingResult, or None on a wiring error
    (dispatcher then routes to the conversational floor).
    """
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    workflow_id = ctx.get("workflow_id")

    if intent_service is None or intent is None:
        logger.error(
            "changes_query_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None

    return await intent_service._handle_changes_query(intent, workflow_id, session_id)


# ─── #1124 Phase 4 step 3: issue-mutation cohort (CLOSE / REOPEN / COMMENT) ───
# These three route off the `_handle_query_intent` elif chain to the workflow
# registry — the same DISPATCH migration as update_document / changes_query above.
# Each handler is reused UNCHANGED (signature: (intent, workflow_id), no session_id).
# They are the legacy-action targets of the Phase-2 CLOSE/REOPEN/COMMENT verbs, so
# this completes the dispatch path for that verb cohort: classifier emits the verb
# → shim → legacy action → action-dispatch rail → handler (no elif branch).


async def run_close_issue_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Action-dispatch entry point for close-issue queries (#1124 step 3, CLOSE).

    #1567: ``session_id`` is threaded (keyword) so the handler's
    repository-question ask can bind via the #846 pending-offer store."""
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    workflow_id = ctx.get("workflow_id")
    if intent_service is None or intent is None:
        logger.error(
            "close_issue_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    return await intent_service._handle_close_issue_query(
        intent, workflow_id, session_id=session_id
    )


async def run_reopen_issue_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Action-dispatch entry point for reopen-issue queries (#1124 step 3, REOPEN).

    #1641 (the #1567 close-entry shape): ``session_id`` is threaded (keyword)
    so the handler's repository-question ask can bind via the #846
    pending-offer store."""
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    workflow_id = ctx.get("workflow_id")
    if intent_service is None or intent is None:
        logger.error(
            "reopen_issue_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    return await intent_service._handle_reopen_issue_query(
        intent, workflow_id, session_id=session_id
    )


async def _run_floor_bound_offer(
    pending_action: Dict[str, Any],
    *,
    session_id: str,
    user_id: Optional[str],
    intent_service: Any,
) -> Any:
    """#1855 layer 2: execute an accepted FLOOR-BOUND offer from its command.

    The binding is the command STRING, not a parsed guess (design ruling,
    Arch-approved): the floor's sentence bound it, the real extractor
    round-tripped it at arm time, and here it goes back through the ordinary
    rail — classification and all — so the user gets the same handler, the same
    copy and the same failure modes as typing it themselves.

    ⚠️ **``_process_intent_internal``, not ``process_intent``, and the reason is
    transcript honesty.** The public wrapper records the message it is given as
    a USER TURN and saves it (#563/#1122). Re-running the command through it
    would write a sentence the user never typed into the durable transcript and
    save the reply twice — once under the invented command turn, once under the
    real "yes". The internal entry is the rail itself: same classification,
    same dispatch, no fabricated turn. The outer turn (the accept) is saved by
    the caller's own wrapper with this reply, which is what actually happened.

    ⚠️ The ``destructive_confirmed`` marker (#1190) deliberately does NOT ride
    this path: there is no Intent to stamp before classification runs. That is
    a REAL constraint on the catalogue, not an oversight — see
    ``unarmed_offer.CommandFamily``: only families whose handler executes from
    an explicit imperative (EXECUTE framing → PROCEED at the #1509 consent
    gate) may be armed this way. Today's one family, add-project, is exactly
    that shape.
    """
    command = (pending_action.get("command") or "").strip()
    if not command:
        logger.error(
            "floor_bound_offer_missing_command",
            action=pending_action.get("action"),
        )
        return None

    runner = getattr(intent_service, "_process_intent_internal", None)
    if runner is None:
        logger.error("floor_bound_offer_no_rail", action=pending_action.get("action"))
        return None

    result = await runner(message=command, session_id=session_id, user_id=user_id)
    if result is None:
        logger.error("floor_bound_offer_dispatch_failed", command=command)
        return None

    logger.info(
        "floor_bound_offer_confirmed_and_executed",
        action=pending_action.get("action"),
        command=command,
    )
    if isinstance(result, dict):
        return result
    return {"message": result.message, "intent_data": result.intent_data}


async def run_confirm_pending_action_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1190: execute a confirmed pending DESTRUCTIVE action.

    Dispatched ONLY by the offer-acceptance seam in process_intent (the
    "yes" turn against a stored destructive-confirmation offer —
    ``destructive_confirm.CONFIRM_PENDING_ACTION_WORKFLOW``). Registered
    action_triggered=False so the classifier/rail can never reach it.

    The context carries the pending-action record's ``pending_action``
    payload (see destructive_confirm module docstring for the shape). This
    entry point re-dispatches the ORIGINAL rail action with the ORIGINAL
    classified Intent — the "yes" message is never re-classified, and the
    resolved parameters (issue number, repo context, principal) are exactly
    the ones the gate deferred. The ``destructive_confirmed`` context marker
    tells the handler's own in-message confirmation (#902) that the explicit
    confirmation turn already happened, so execution completes in one turn.

    Generic carrier (#1190 Part 3): nothing here is close/reopen-specific —
    any deferred rail action stored in ``pending_action`` executes the same
    way. Returns the acceptance-seam dict shape ({"message", "intent_data"});
    None on wiring gaps (caller routes to floor — safe default, no write).

    #1855 layer 2 (Arch-approved 2026-09-24, question (b)): a SECOND record
    shape rides this same carrier — ``kind == floor_bound_offer``, which stores
    a COMMAND STRING instead of a resolved Intent, because the floor has no
    handler and never produced one. Its branch re-runs that text through the
    ordinary rail, so the action executes by exactly the path the user would
    have taken by typing it — no second implementation of any action. Joining
    the five non-destructive kinds already discriminated here is precedent-
    following, not a new pattern; a dedicated workflow entry would duplicate a
    dispatch path that already works.
    """
    from services.intent_service.destructive_confirm import CONFIRMED_CONTEXT_KEY

    ctx = context or {}
    pending_action = ctx.get("pending_action")
    intent_service = ctx.get("intent_service")
    if not pending_action or intent_service is None:
        logger.error(
            "confirm_pending_action_missing_context",
            has_pending_action=bool(pending_action),
            has_intent_service=intent_service is not None,
        )
        return None

    if pending_action.get("kind") == FLOOR_BOUND_OFFER_KIND:
        return await _run_floor_bound_offer(
            pending_action, session_id=session_id, user_id=user_id, intent_service=intent_service
        )

    intent = pending_action.get("intent")
    action = pending_action.get("action")
    if intent is None or not action:
        logger.error(
            "confirm_pending_action_malformed_record",
            has_intent=intent is not None,
            action=action,
        )
        return None

    # Mark the intent confirmed so the handler executes instead of asking
    # its own #902 confirmation a second time. Copy-on-write: never mutate
    # a context dict the caller may share.
    intent.context = dict(intent.context or {})
    intent.context[CONFIRMED_CONTEXT_KEY] = True

    from services.intent_service.workflow_dispatcher import dispatch_workflow

    result = await dispatch_workflow(
        workflow_type=action,
        session_id=session_id,
        user_id=user_id,
        context={"intent": intent, "workflow_id": None, "intent_service": intent_service},
    )
    if result is None:
        logger.error("confirm_pending_action_dispatch_failed", action=action)
        return None

    logger.info("destructive_action_confirmed_and_executed", action=action)
    # The acceptance seam consumes {"message", "intent_data"}; rail handlers
    # return IntentProcessingResult — adapt without losing either shape.
    if isinstance(result, dict):
        return result
    return {"message": result.message, "intent_data": result.intent_data}


async def run_verify_inference_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1510 (inferred half): store a USER-VERIFIED inference.

    Dispatched ONLY by the offer-acceptance seam in process_intent — the
    "yes" turn against a stored verification read-back
    (``verified_inference.VERIFY_INFERENCE_WORKFLOW``). Registered
    action_triggered=False so the classifier/rail can never reach it (the
    #1190 confirm_pending_action pattern).

    The context carries the read-back's ``pending_action`` payload (built by
    ``verified_inference.build_read_back_offer``). Acceptance is the PM-ruled
    "once verified, it's stored — not re-inferred each time" write: the value
    lands in the user's verified-inference store (users.preferences JSONB —
    the ONE preference persistence, PPM+CXO) with source=user_verified
    provenance. Returns the acceptance-seam dict shape; None on wiring gaps
    (caller routes to floor — safe default, nothing stored).

    #1532 (no principal dropping): the write goes to the turn's authenticated
    user. If the offer was built for a DIFFERENT user (auth changed between
    turns), nothing is stored — never write one principal's inference into
    another's store.
    """
    from services.intent_service import verified_inference as vi

    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    if payload.get("kind") != vi.VERIFY_INFERENCE_KIND:
        logger.error(
            "verify_inference_missing_or_foreign_payload",
            has_payload=bool(payload),
            kind=payload.get("kind"),
        )
        return None

    key = payload.get("inference_key")
    description = payload.get("summary") or "that inference"
    if not key:
        logger.error("verify_inference_malformed_record", has_key=False)
        return None

    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    if offer_user and principal and offer_user != principal:
        logger.warning(
            "verify_inference_principal_mismatch",
            offer_user=offer_user,
            turn_user=principal,
        )
        return {
            "message": f"I won't assume {description} — nothing has been stored.",
            "intent_data": {
                "category": "execution",
                "action": vi.VERIFY_INFERENCE_WORKFLOW,
                "verified": False,
                "principal_mismatch": True,
            },
        }

    persisted = await vi.store_verified_inference(
        principal or offer_user,
        key,
        payload.get("inference_value"),
        source=vi.SOURCE_USER_VERIFIED,
        confidence=payload.get("confidence"),
    )
    logger.info(
        "inference_verified_and_stored",
        inference_key=key,
        persisted=persisted,
        user_id=principal or offer_user,
    )
    # Honest persistence copy (collaboration_gate.mode_confirmation_message
    # rule): a claimed-durable save that didn't happen is a confabulated
    # capability.
    message = f"Thanks — noted: {description}. I'll remember that instead of guessing next time."
    if not persisted:
        message = (
            f"Thanks — I'll go with {description} for now, but I couldn't save it "
            "just now, so I may ask again in a future session."
        )
    return {
        "message": message,
        "intent_data": {
            "category": "execution",
            "action": vi.VERIFY_INFERENCE_WORKFLOW,
            "verified": True,
            "persisted": persisted,
            "inference_key": key,
        },
    }


async def run_standup_interview_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1591: start the EXISTING #585 interactive standup interview on an
    accepted invitation.

    Dispatched ONLY by the offer-acceptance seam — the "yes" turn against the
    invitation appended after a standup report (or leading an honest-empty
    one). Registered action_triggered=False (the verify_inference/#1190
    pattern) so the classifier/rail can never reach it.

    This is pure wiring to the existing flow: acceptance calls
    ``IntentService._start_standup_conversation`` — the SAME entry the
    ``/standup`` command and the #1511 interview-token branch use — so all
    three doors open the one interview (escape tiers, resume, teaching copy
    unchanged). CXO property 3 note: DECLINE never reaches this function —
    the generic decline path answers with the offer's decline_message and
    changes nothing.
    """
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    payload = ctx.get("pending_action") or {}
    if payload.get("kind") != "standup_interview_invitation":
        logger.error(
            "standup_interview_missing_or_foreign_payload",
            has_payload=bool(payload),
            kind=payload.get("kind"),
        )
        return None
    if intent_service is None:
        logger.error("standup_interview_workflow_missing_intent_service")
        return None
    # #1532: the interview is the USER's flow. The invitation was built for
    # the user it was offered to; if the accepting turn's principal differs
    # (auth changed between turns), don't start a conversation keyed to the
    # wrong user — decline-shaped no-op (mirrors run_verify_inference_workflow).
    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    if offer_user and principal and offer_user != principal:
        logger.warning(
            "standup_interview_principal_mismatch",
            offer_user=offer_user,
            turn_user=principal,
        )
        return {
            "message": "Let's hold off on that — nothing has been started.",
            "intent_data": {
                "category": "execution",
                "action": "standup_interview",
                "principal_mismatch": True,
            },
        }
    effective_user = principal or offer_user
    if not effective_user or not session_id:
        logger.error(
            "standup_interview_workflow_missing_principal_or_session",
            has_user=bool(effective_user),
            has_session=bool(session_id),
        )
        return None
    # #1837: the acceptance ARMS the interview — the handler starts at the
    # first question instead of re-greeting ("Ready for your standup?"), which
    # is what made PM say yes twice and still get no interview.
    result = await intent_service._start_standup_conversation(
        effective_user, session_id, interview_accepted=True
    )
    # The acceptance seam consumes {"message", "intent_data"}; the interview
    # entry returns IntentProcessingResult — adapt (confirm_pending_action idiom).
    if isinstance(result, dict):
        return result
    return {"message": result.message, "intent_data": result.intent_data}


async def run_comment_issue_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Action-dispatch entry point for comment-issue queries (#1124 step 3, COMMENT)."""
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    workflow_id = ctx.get("workflow_id")
    if intent_service is None or intent is None:
        logger.error(
            "comment_issue_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    # #1122: thread session_id so the handler's slot extraction can build
    # conversation history (antecedent resolution — "that issue", "it").
    return await intent_service._handle_comment_issue_query(
        intent, workflow_id, session_id=session_id
    )


# ─── #1124 Phase 4 step 3 cohort 2: GitHub read-query cohort ──────────────────
# These handlers all share the (intent, workflow_id) signature and are reused
# UNCHANGED, so one parameterized entry-point factory covers the whole cohort
# (vs. N near-identical functions). The handler method name is explicit in each
# registration in register_default_workflows(); a unit test asserts every
# registered handler name actually exists on IntentService — closing the
# getattr-typo blind spot that a MagicMock-based test would otherwise hide.
def _make_query_dispatch_entry_point(
    handler_attr: str,
    *,
    pass_session_id: bool = False,
    pass_user_id: bool = False,
):
    """Build an action-dispatch entry point that invokes an IntentService query
    handler, reused unchanged. The handler is called positionally as
    ``handler(intent, workflow_id[, session_id][, user_id])`` — the optional 3rd/4th
    args are threaded only when the flags are set, matching the handler's signature.

    Defaults (both False) = the 2-arg ``(intent, workflow_id)`` shape, so existing
    callers are unchanged. The rail passes ``session_id`` + ``user_id`` to every entry
    point (``dispatch_workflow(..., session_id=, user_id=, ...)``); the flags select
    which a given handler accepts (e.g. the calendar/productivity handlers take
    session_id; projects takes user_id; attention takes both — #586/#849)."""

    async def _entry(
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ctx = context or {}
        intent_service = ctx.get("intent_service")
        intent = ctx.get("intent")
        workflow_id = ctx.get("workflow_id")
        if intent_service is None or intent is None:
            logger.error(
                "query_dispatch_missing_context",
                handler=handler_attr,
                has_intent_service=intent_service is not None,
                has_intent=intent is not None,
            )
            return None
        args = [intent, workflow_id]
        if pass_session_id:
            args.append(session_id)
        if pass_user_id:
            args.append(user_id)
        return await getattr(intent_service, handler_attr)(*args)

    _entry.__name__ = f"run_{handler_attr.lstrip('_')}"
    return _entry


def _make_user_scoped_query_dispatch_entry_point(handler_attr: str):
    """Build an action-dispatch entry point for a 3-arg
    ``(intent, workflow_id, user_id)`` IntentService query handler, reused
    unchanged. The action-dispatch rail passes ``user_id`` to the entry point
    (``dispatch_workflow(..., user_id=user_id, ...)``); this variant threads it to
    the handler (the calendar cohort needs it for timezone-aware queries, #586)."""

    async def _entry(
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ctx = context or {}
        intent_service = ctx.get("intent_service")
        intent = ctx.get("intent")
        workflow_id = ctx.get("workflow_id")
        if intent_service is None or intent is None:
            logger.error(
                "query_dispatch_missing_context",
                handler=handler_attr,
                has_intent_service=intent_service is not None,
                has_intent=intent is not None,
            )
            return None
        return await getattr(intent_service, handler_attr)(intent, workflow_id, user_id)

    _entry.__name__ = f"run_{handler_attr.lstrip('_')}"
    return _entry


async def run_todo_query_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1124: the execution-delegation adapter — delegates to the EXECUTION
    handler, which owns the todo handlers. Used by the todo READ queries
    (pre-classifier routes them as QUERY) AND by the create_reminder WRITE
    entry (#1560) — each rail key registers its own WorkflowEntry with its own
    declared effect; this shared entry point just mirrors the migrated elifs
    exactly. The workflow object is no longer pre-created (#883/#1094), so None
    is passed (the elif passed the `workflow` param, which the handler reduced
    to `getattr(workflow, 'id', None)` anyway)."""
    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_execution_intent(todos)",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    return await intent_service._handle_execution_intent(intent, None, session_id, user_id)


async def run_create_todo_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1685: create_todo via the action-dispatch rail (WRITE, consent-evaluated).

    Carries the removed ``elif mapped_action == "create_todo"`` branch's exact
    body: principal coercion (#1466) with its auth-failure result, then the
    real ``todo_handlers.handle_create_todo``. No seam sits between them —
    unlike the delete side, the create elif had no #1605 clear-family branch
    (the clear family is a deletion vocabulary), so this is the whole body.

    Consent lives UPSTREAM at the rail (#1509), and that is the entire point
    of the registration: WRITE derives ``needs_consent``, so
    ``consent_gate.evaluate_consent`` now EVALUATES a create-todo turn where
    previously nothing did. It is evaluation, not new ceremony — the matrix's
    PRIVATE x WRITE x execute cell is PROCEED, and every natural create
    phrasing ("add a todo to …", "create a todo …") is verb-initial
    imperative, which ``classify_framing`` reads as EXECUTE. The turn still
    creates in one step. An AMBIGUOUS-framed create emission is held for a
    consent check exactly as the already-registered create_reminder sibling
    (#1560) is — the ratified #1510/#1509 behavior for ambiguity, not a
    create-todo-specific gate.
    """
    from services.intent.intent_service import (
        IntentProcessingResult,
        _coerce_todo_principal,
    )

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "create_todo_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None

    category = intent.category.value if intent.category else "execution"
    todo_user_id = _coerce_todo_principal(user_id)  # #1466: never raises on Slack ids
    if not todo_user_id:
        return IntentProcessingResult(
            success=False,
            message="I need you to be logged in to manage todos. Please log in and try again.",
            intent_data={"category": category, "action": intent.action},
            error="User not authenticated",
            error_type="AuthenticationRequired",
        )

    message = await intent_service.todo_handlers.handle_create_todo(
        intent, session_id, user_id=todo_user_id
    )
    # Issue #748: Don't return workflow_id for synchronous operations
    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data={
            "category": category,
            "action": intent.action,
            "confidence": intent.confidence,
        },
    )


async def run_delete_todo_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1666: delete_todo via the action-dispatch rail (DESTRUCTIVE, #1190-gated).

    Carries the removed ``elif mapped_action == "delete_todo"`` branch's exact
    body: principal coercion (#1466), the #1605 clear-family seam with
    candidate effect DESTRUCTIVE (ambiguous "clear my reminders" shapes get
    the three-variant flow — this seam keeps FIRST CLAIM on them because the
    rail's confirm gate passes clear-family shapes through untouched, see
    ``destructive_confirm.build_todo_delete_confirmation``), then the real
    ``todo_handlers.handle_delete_todo``.

    Consent lives UPSTREAM at the rail (#1190): an explicit "delete todo 3"
    only reaches this entry point via ``run_confirm_pending_action_workflow``
    after a crisp confirmed yes (the gate armed the ask on the classified
    turn), or on one of the gate's verified read-only passthrough legs
    (no principal / no number / out of range — every one returns
    clarification copy, never a delete).
    """
    from services.intent.intent_service import (
        IntentProcessingResult,
        _coerce_todo_principal,
    )
    from services.intent_service import reminder_clear as _rc
    from services.shared_types import EffectClass as _EffectClass

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "delete_todo_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None

    category = intent.category.value if intent.category else "execution"
    todo_user_id = _coerce_todo_principal(user_id)  # #1466: never raises on Slack ids
    if not todo_user_id:
        return IntentProcessingResult(
            success=False,
            message="I need you to be logged in to delete todos. Please log in and try again.",
            intent_data={"category": category, "action": intent.action},
            error="User not authenticated",
            error_type="AuthenticationRequired",
        )

    # #1605: clear-family disambiguation, candidate effect DESTRUCTIVE — the
    # ask fires in EVERY meta mode below the auto-apply bar (process steering
    # never lowers a destructive ask). Explicit deletion phrasings
    # ("delete todo 3") return None and proceed unchanged.
    _clear_result = await _rc.maybe_handle_clear_family(
        intent_service, intent, session_id, user_id, todo_user_id, _EffectClass.DESTRUCTIVE
    )
    if _clear_result is not None:
        return _clear_result

    # #1696: an EXPLICIT bulk delete ("delete my reminders" — plural noun,
    # no number, no named target) used to fall to handle_delete_todo's
    # single-item which-todo ask; the one flow built for bulk clears
    # (#1605) deliberately declines explicit imperatives, so the MORE
    # explicit user got LESS capability. This seam hands the bulk shape to
    # the clear-family flow's already-#1190-gated delete leg (targets bound
    # at offer time; "yes" dispatches clear_reminders_delete). Runs AFTER
    # the clear seam so #1605 keeps first claim; every non-bulk shape
    # returns None and proceeds unchanged.
    _bulk_result = await _rc.maybe_handle_explicit_bulk_delete(
        intent_service, intent, session_id, user_id, todo_user_id
    )
    if _bulk_result is not None:
        return _bulk_result

    message = await intent_service.todo_handlers.handle_delete_todo(
        intent, session_id, user_id=todo_user_id
    )
    # Issue #748: Don't return workflow_id for synchronous operations
    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data={
            "category": category,
            "action": intent.action,
            "confidence": intent.confidence,
        },
    )


async def run_complete_todo_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3: complete_todo via the action-dispatch rail (WRITE, consent-evaluated).

    Carries the removed ``elif mapped_action == "complete_todo"`` branch's
    exact body: principal coercion (#1466) with its auth-failure result, the
    #1605 clear-family seam with candidate effect WRITE (an ambiguous
    "clear/handle/take care of" phrasing over the todo/reminder domain gets
    the three-variant flow before executing — this branch's own guess is
    completion), then the real ``todo_handlers.handle_complete_todo``.

    effect: WRITE, never DESTRUCTIVE — ``TodoManagementService.complete_todo``
    (via ``TodoRepository.complete_todo``) flips the row's ``status`` /
    ``completed`` / ``completed_at`` fields; the row is never deleted, stays
    selectable by ``list_todos(include_completed=True)`` / the
    ``list_completed_todos`` action, and ``TodoManagementService.reopen_todo``
    /``TodoRepository.reopen_todo`` reverse every one of those fields back to
    pending. A reversible status flip, not an irrecoverable removal from the
    active list — Arch's dividing line (2026-10-03 ruling, §4) for WRITE vs
    DESTRUCTIVE on this op.

    Consent lives UPSTREAM at the rail (#1509): WRITE derives ``needs_consent``,
    so ``consent_gate.evaluate_consent`` now EVALUATES a complete-todo turn
    where previously nothing did — evaluation, not new ceremony, since the
    matrix's PRIVATE x WRITE x execute cell is PROCEED and every natural
    completion phrasing ("complete todo 1", "mark the PR review as done") is
    verb-initial imperative, which ``classify_framing`` reads as EXECUTE.
    """
    from services.intent.intent_service import (
        IntentProcessingResult,
        _coerce_todo_principal,
    )
    from services.intent_service import reminder_clear as _rc
    from services.shared_types import EffectClass as _EffectClass

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "complete_todo_workflow_missing_context",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None

    category = intent.category.value if intent.category else "execution"
    todo_user_id = _coerce_todo_principal(user_id)  # #1466: never raises on Slack ids
    if not todo_user_id:
        return IntentProcessingResult(
            success=False,
            message="I need you to be logged in to complete todos. Please log in and try again.",
            intent_data={"category": category, "action": intent.action},
            error="User not authenticated",
            error_type="AuthenticationRequired",
        )

    # #1605: a clear-family verb ("clear/handle/take care of/reset" over the
    # reminder/todo domain) is an AMBIGUOUS mapping the classifier happened to
    # guess as complete — disambiguate via the three-variant flow before
    # executing. Candidate effect WRITE (this branch's guess: complete_todo).
    # Explicit completion phrasings return None and proceed unchanged.
    _clear_result = await _rc.maybe_handle_clear_family(
        intent_service, intent, session_id, user_id, todo_user_id, _EffectClass.WRITE
    )
    if _clear_result is not None:
        return _clear_result

    message = await intent_service.todo_handlers.handle_complete_todo(
        intent, session_id, user_id=todo_user_id
    )
    # Issue #748: Don't return workflow_id for synchronous operations
    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data={
            "category": category,
            "action": intent.action,
            "confidence": intent.confidence,
        },
    )


async def run_archived_projects_query_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1570: archived-projects LIST query via the action-dispatch rail.

    PM live 2026-08-10: "show me my archived projects" — the floor DENIED the
    capability. The pre-classifier claims that phrasing as
    STATUS/get_project_status (the PORTFOLIO list pattern rejects the "me"
    token), STATUS always floors, and archived-list had NO rail/ActionMapper
    key — so the #1517 capability manifest could not protect it and the #1431
    branch (inside the PORTFOLIO canonical handler) never ran. This entry is
    the sanctioned #1560 pattern: a rail key makes the capability (1) part of
    wired_chat_actions() → the floor may no longer deny it, and (2)
    deterministically dispatchable for any LLM emission of the action,
    category-independent. The pre-classifier pattern half is corpus material
    (#1559 routing moratorium) — reported on the issue, not patched here.

    Data path mirrors the #1431 canonical branch (canonical_handlers.py,
    operation == "list_archived"): owner-scoped
    PortfolioService.list_archived_projects — never the active list.
    """
    # Lazy import: IntentProcessingResult lives in intent_service, which this
    # module must not import at module level (circular).
    from services.intent.intent_service import IntentProcessingResult

    if not user_id:
        return IntentProcessingResult(
            success=True,
            message=(
                "I can show you your archived projects, but I need to know who "
                "you are first — try signing in."
            ),
            intent_data={
                "category": "portfolio",
                "action": "list_archived_projects",
                "context": {"reason": "no_user_id"},
            },
            workflow_id=None,
            requires_clarification=False,
        )

    try:
        from services.database.repositories import ProjectRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.onboarding.portfolio_service import PortfolioService

        async with AsyncSessionFactory.session_scope() as session:
            project_repo = ProjectRepository(session)
            portfolio_service = PortfolioService(project_repo)
            projects = await portfolio_service.list_archived_projects(user_id=user_id)
    except Exception as e:  # silent-ok: error-logged with context and returns success=False — honest degrade, never fake-empty (#1425)
        logger.error("archived_projects_query_failed", error=str(e), user_id=user_id)
        return IntentProcessingResult(
            success=False,
            message=(
                "I had trouble loading your archived projects right now. "
                "You can try again in a moment."
            ),
            intent_data={
                "category": "portfolio",
                "action": "list_archived_projects",
                "context": {"error": str(e)},
            },
            workflow_id=None,
            requires_clarification=False,
        )

    if projects:
        # #1738: render the FULL set — the rendered message is the only
        # per-turn record that reaches next-turn context, so a `[:5]` cap
        # here becomes the model's data next turn ("the list I got back
        # only showed five names", PM live 2026-09-09 v70). GatherOutcome
        # contract §5b: a render cap must never change what the system
        # believes it has. Same fix as the #1431 canonical branch.
        names = [p.name for p in projects]
        noun = "project" if len(projects) == 1 else "projects"
        message = f"You have {len(projects)} archived {noun}:\n\n" + "\n".join(
            f"- {name}" for name in names
        )
        # #1738 defect 1: `<name>` is swallowed by the web render as an
        # unknown HTML tag (rendered 'Say "restore "' with an empty slot).
        message += '\n\nSay "restore [project name]" to bring one back.'
    else:
        message = "You don't have any archived projects."

    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data={
            "category": "portfolio",
            "action": "list_archived_projects",
            "context": {"project_count": len(projects)},
        },
        workflow_id=None,
        requires_clarification=False,
    )


# #1661: how many account documents the naming-fallback reply will actually
# print (distinct from PPM's REMAINDER_OFFER_THRESHOLD, which decides whether
# to show the count line at all — see `_render_document_naming_reply`).
_DOCUMENT_NAMING_RENDER_CAP = 10


def _render_document_naming_reply(documents: list) -> str:
    """#1661: what the summarize rail says when a temporal file reference's
    window (7 days, or a distance the user stated) comes back empty but the
    account has documents OUTSIDE that window — the Files page would list
    them, so the flat "I don't see any uploaded documents" reply would be
    false. Names what exists instead.

    Reuses the #1762 pattern (`services.intent_service.list_remainder`):
    render the whole set when it's small (PPM's `REMAINDER_OFFER_THRESHOLD`),
    otherwise a BOUNDED list with an honest "N of M" count. This call site has
    no session/self to arm a cashable #1762 remainder — `workflow_entries.py`
    functions are plain, with no access to `IntentService._arm_list_remainder`
    — so it never promises "and N more" or "say the word for the rest"; the
    honest alternative offered is naming a specific file, which the resolver
    can act on this same turn (the `_FILENAME_TOKEN_RE` / exact-match path).

    ``# CXO copy pass pending (#1661)`` — this wording is provisional; do not
    treat it as the ratified contract copy.
    """
    from services.intent_service.list_remainder import REMAINDER_OFFER_THRESHOLD

    total = len(documents)
    shown = (
        documents if total <= REMAINDER_OFFER_THRESHOLD else documents[:_DOCUMENT_NAMING_RENDER_CAP]
    )
    lines = "\n".join(f"- {d.filename}" for d in shown)
    header = (
        "Nothing matches that time frame, but here's what's in your account " "(most recent first):"
    )
    if len(shown) == total:
        return f"{header}\n{lines}"
    return (
        f"{header}\n{lines}\n\n"
        f"That's {len(shown)} of {total} — tell me the filename and I'll summarize that one."
    )


async def run_summarize_document_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1624: chat summarize of an UPLOADED document via the action-dispatch rail.

    Fifteen months of history behind this entry (full archaeology:
    docs/internal/operations/summarize-intent-forensics-2026-08-15.md): the #290
    summarizer shipped REST-only in 2025-11 (its chat dispatch existed only in a
    guidance doc), the file-reference resolver lost its only live caller when
    main.py was gutted (2025-10-01), and #1187 closed with its `document` branch
    deferred and untracked. This entry is the repair PM ruled on 2026-08-15:
    chat reaches the SAME code path the working REST endpoint uses —
    `document_handlers.handle_summarize_document` (the function
    `POST /api/v1/documents/{file_id}/summarize` calls at
    web/api/routes/documents.py:198) — no parallel summarize implementation.

    Resolution: the orphaned-but-intact `FileResolver` (un-orphaned here; its
    repository has been owner-scoped since #1312 — the `session_id` parameter
    name is legacy, the value flowing through is owner_id) binds "the document"
    to the user's uploaded file with recency/type/name scoring + ambiguity
    detection.

    Honesty contract (the 2025 acknowledgment-theater lesson IS this issue's
    origin story):
      - github-issue / commit-range shaped requests return None → the rail
        falls through to SYNTHESIS category routing → the working #1187
        fetch-augment floor path (this guard matters because classifier.py's
        action normalization maps a bare `summarize` emission to
        `summarize_document` regardless of source).
      - no resolvable upload → a DETERMINISTIC honest reply (never a
        fabricated summary, never a floor improvisation).
      - ambiguity → ask which file, listing the candidates.

    The user's LLM key is already bound at the chat request boundary
    (web/api/routes/intent.py `request_api_key`), the same binding the REST
    route does per-request — DocumentAnalyzer sees the same credential either
    way.
    """
    import re as _re

    # Lazy import: intent_service must not be imported at module level (circular).
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent = ctx.get("intent")
    intent_context = dict(getattr(intent, "context", None) or {})
    message = (
        (getattr(intent, "original_message", "") or "")
        or intent_context.get("original_message", "")
        or ""
    )
    msg_lower = message.lower()

    def _result(text, *, success=True, clarify=False, reason=None, extra=None):
        payload = {"reason": reason} if reason else {}
        if extra:
            payload.update(extra)
        return IntentProcessingResult(
            success=success,
            message=text,
            intent_data={
                "category": "synthesis",
                "action": "summarize_document",
                "context": payload,
            },
            workflow_id=None,
            requires_clarification=clarify,
        )

    # ── Guard: not actually an uploaded-document summarize ────────────────
    # source_type is the classifier's own slot; the message heuristic mirrors
    # _fetch_summary_source_content's issue-shape inference so both layers
    # agree on who owns the request.
    source_type = intent_context.get("source_type")
    if source_type in ("github_issue", "commit_range"):
        return None  # rail fall-through → #1187 fetch-augment floor path
    if source_type in (None, "", "document"):
        if ("issue" in msg_lower and _re.search(r"#?\d+", msg_lower)) or ("commit" in msg_lower):
            return None  # issue/commit summarize that mis-landed here

    if not user_id:
        return _result(
            "I can summarize a document you've uploaded, but I need to know who "
            "you are first — try signing in.",
            reason="no_user_id",
        )

    # ── Resolve "the document" → file_id (owner-scoped) ───────────────────
    try:
        from services.database.session_factory import AsyncSessionFactory
        from services.domain.models import Intent
        from services.file_context.exceptions import AmbiguousFileReferenceError
        from services.file_context.file_resolver import FileResolver
        from services.repositories.file_repository import FileRepository
        from services.shared_types import IntentCategory

        # FileResolver reads intent.action + intent.context["original_message"];
        # hand it a detached Intent (own context dict) so the turn's
        # intent.context is never mutated (the process_intent convention).
        resolver_view = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize_document",
            original_message=message,
            context={"original_message": message},
        )

        account_documents = None  # only fetched when we actually need it, below
        try:
            async with AsyncSessionFactory.session_scope() as session:
                # #1657: candidates must be the SAME set the Files listing
                # shows — uploads ∪ the owner's generated artifacts (#355:
                # /files is a view over both). Resolver-side owner scoping is
                # unchanged; the artifact repo query is owner-scoped too.
                from services.database.repositories import ArtifactRepository

                resolver = FileResolver(
                    FileRepository(session),
                    artifact_repository=ArtifactRepository(session),
                )
                file_id, resolution_confidence = await resolver.resolve_file_reference(
                    resolver_view, user_id
                )
                # #1661: a temporal query (7 days, or a stated distance) can
                # come back empty while the account genuinely has documents
                # OUTSIDE that window — the false-empty this issue is about.
                # Fetch the account-wide fallback set NOW, inside this same
                # session, only when it's actually needed (temporal-shaped
                # message + nothing resolved) — never widen the temporal
                # query itself, which would silently bind 'yesterday' to a
                # year-old file.
                if not file_id and FileResolver.is_temporal_reference(message):
                    account_documents = await resolver.list_owner_documents(user_id)
        except AmbiguousFileReferenceError as e:
            candidates = "\n".join(f"- {f.filename}" for f in e.files)
            return _result(
                "You've uploaded a few files and I'm not sure which one you "
                f"mean — which should I summarize?\n{candidates}",
                clarify=True,
                reason="ambiguous_file_reference",
                extra={"candidates": [f.filename for f in e.files]},
            )

        if not file_id:
            if account_documents:
                # #1661: the temporal window (7 days, or the distance the
                # user stated) came back empty, but the account has documents
                # outside it — the Files page would list them, so saying "I
                # don't see any uploaded documents" here would be false. Name
                # what does exist instead of the flat honest-empty.
                # CXO copy pass pending (#1661).
                return _result(
                    _render_document_naming_reply(account_documents),
                    reason="no_documents_in_window",
                    extra={"documents_outside_window": len(account_documents)},
                )
            # Honest degrade — never fabricate a summary of a document that
            # isn't there, never hand the turn to floor improvisation.
            return _result(
                "I don't see any uploaded documents I can summarize. Upload "
                "the file on the Files page and ask me again — or paste the "
                "text into the chat and I'll summarize that directly.",
                reason="no_uploaded_documents",
            )

        # ── Summarize via the SAME path the REST endpoint uses ────────────
        from services.intent_service.document_handlers import (
            handle_summarize_document,
        )

        summary_format = "bullet"
        if "detail" in msg_lower:
            summary_format = "detailed"
        elif "paragraph" in msg_lower or "prose" in msg_lower:
            summary_format = "paragraph"

        try:
            summarized = await handle_summarize_document(
                file_id=file_id, format=summary_format, user_id=user_id
            )
        except FileNotFoundError:
            return _result(
                "I found a reference to an uploaded file but couldn't access "
                "its content anymore — it may have been removed. Try "
                "re-uploading it.",
                success=False,
                reason="file_content_missing",
            )

        return _result(
            f"Here's my summary of {summarized['filename']}:\n\n" f"{summarized['summary']}",
            extra={
                "file_id": summarized["file_id"],
                "filename": summarized["filename"],
                "summary_format": summarized["format"],
                "resolution_confidence": resolution_confidence,
            },
        )
    except Exception as e:  # silent-ok: error-logged with context and returns success=False — honest degrade, never fake success (#1425)
        logger.error("summarize_document_workflow_failed", error=str(e), user_id=user_id)
        return _result(
            "I had trouble reading that document just now. You can try again " "in a moment.",
            success=False,
            reason="summarize_failed",
        )


# handler_attr → classifier aliases (mirror the migrated elif branches exactly).
_READ_QUERY_COHORT: dict[str, list[str]] = {
    "_handle_shipped_this_week": [
        "shipped_this_week",
        "what_shipped",
        "show_closed_prs",
        "shipped_query",
    ],
    # #1283 probe (2026-07-08): live LLM emitted list_stale_prs past the four aliases.
    "_handle_stale_prs": [
        "stale_prs",
        "old_prs",
        "show_stale_prs",
        "stale_prs_query",
        "list_stale_prs",
    ],
    "_handle_review_issue_query": [
        "review_issue",
        "show_issue",
        "get_issue",
        "review_issue_query",
    ],
    "_handle_list_issues_query": ["list_issues", "list_issues_query"],
    "_handle_list_prs_query": ["list_prs", "list_prs_query", "list_pull_requests"],
    "_handle_list_milestones_query": ["list_milestones", "list_milestones_query"],
    "_handle_list_releases_query": ["list_releases", "list_releases_query"],
    "_handle_list_labels_query": ["list_labels", "list_labels_query"],
    "_handle_list_branches_query": ["list_branches", "list_branches_query"],
}


# #1762 (epic 6): handlers in this cohort that take ``session_id`` as a 3rd
# positional arg. The six GitHub LISTINGS render capped lists, and a capped
# list must ARM its unrendered remainder so "…and there are more" is a claim
# it can cash (GatherOutcome §5b) — arming is session-scoped state, so the
# session id has to reach the handler. The other three stay 2-arg:
# shipped_this_week / stale_prs / review_issue_query render no capped list
# with a hidden tail (the first two are window listings rendered whole; the
# third is one issue). Adding a handler here is a signature change — the
# factory passes the arg only for members of this set.
_READ_QUERY_SESSION_THREADED: frozenset[str] = frozenset(
    {
        "_handle_list_issues_query",
        "_handle_list_prs_query",
        "_handle_list_milestones_query",
        "_handle_list_releases_query",
        "_handle_list_labels_query",
        "_handle_list_branches_query",
    }
)


# #1667 flip groups for the read-query cohort — handler_attr → wave-1 group
# (see FLIP_GROUPS in workflow_dispatcher.py). Declared as its own map rather
# than folded into the alias dict so the alias lists stay untouched; a handler
# absent from this map is UNGROUPED, which is the safe direction (unaddressable
# by any wave flip, listed by name in `--audit`).
_READ_QUERY_FLIP_GROUPS: dict[str, str] = {
    # Listing/status reads: the answer is a list or a state summary, no
    # referent to resolve and no temporal expression to parse. shipped_this_week
    # and stale_prs carry a FIXED window (this week / the staleness threshold),
    # not a user-supplied time expression — they are listings, not temporal ops.
    "_handle_shipped_this_week": "read_status",
    "_handle_stale_prs": "read_status",
    "_handle_list_issues_query": "read_status",
    "_handle_list_prs_query": "read_status",
    "_handle_list_milestones_query": "read_status",
    "_handle_list_releases_query": "read_status",
    "_handle_list_labels_query": "read_status",
    "_handle_list_branches_query": "read_status",
    # The paradigm read_referent case (kickoff §2.2 wave 2's own example):
    # "show me issue 108" resolves a specific issue — exactly the class the
    # SessionSnapshot's recent-referent fields exist to serve.
    "_handle_review_issue_query": "read_referent",
}


# #1124 cohort: calendar query cohort (meeting_time is the directed cohort-1 target;
# recurring_meetings + week_calendar are same-signature siblings in the same elif
# block, folded in for a clean QUERY-category block — mirrors the read-query cohort
# precedent). All three share (intent, workflow_id, user_id), so they use the
# user-scoped factory. Aliases mirror the migrated elif branches exactly.
_CALENDAR_QUERY_COHORT: dict[str, list[str]] = {
    "_handle_meeting_time_query": [
        "meeting_time",
        "how_much_time_in_meetings",
        "calendar_analysis",
    ],
    "_handle_recurring_meetings_query": [
        "recurring_meetings",
        "review_recurring_meetings",
        "audit_meetings",
    ],
    "_handle_week_calendar_query": [
        "week_calendar",
        "week_ahead",
        "whats_my_week_like",
    ],
}

# #1595 Phase 1 shadow-score m-44 fix (2026-09-25, Lead's read): the calendar
# cohort loop below previously gave every handler the same generic
# `f"{handler_attr} via action dispatch (#1124)"` description (the noise
# stripper reduces that to the bare handler attr name for the router's
# grammar) — too close together for the constrained router to tell "today's
# calendar" from "the week ahead" apart. Shared-subset scoring caught the
# consequence: "what's on my calendar today?" routed to `week_calendar`
# instead of `meeting_time` (TEMPORAL regression, 3/4 vs baseline 4/4).
# Sharpened text for these two operations ONLY, per the registry-is-the-
# source-of-truth rule (PDR-006 condition 2 — never a hand-written schema,
# never the router prompt); `recurring_meetings` keeps the cohort default
# below, untouched.
# #1595 Phase 3 (2026-10-01, Lead; CXO/PPM confirmed the destinations): the
# GitHub read cohort's generic descriptions strip to the bare handler name,
# which left the served router (Haiku) declining two plain asks — "get issue
# 101" → NONE and "what's the issue count" → CLARIFY — while naming the right
# listing for every milestone/release/label/branch phrasing. Sharpened text
# for these two handlers ONLY, same discipline as the calendar map below.
_READ_QUERY_DESCRIPTIONS: dict[str, str] = {
    "_handle_review_issue_query": (
        "Fetch and show one GitHub issue: 'show issue 42', 'get issue 101' " "(#1595)"
    ),
    "_handle_list_issues_query": (
        "List or count GitHub issues — open issues, how many issues, the issue "
        "count, issues by label or state (#1595)"
    ),
    # CXO 2026-10-01: the handler's own docstring disposes "what version are we
    # on?" (#1039 Q5 — latest non-prerelease at the top); the router declined
    # it on the bare handler name.
    "_handle_list_releases_query": (
        "Recent GitHub releases, and 'what version are we on' — the latest "
        "release at the top (#1595)"
    ),
}


_CALENDAR_QUERY_DESCRIPTIONS: dict[str, str] = {
    "_handle_meeting_time_query": (
        "Calendar, agenda or schedule for ONE day — today, tomorrow, or a named "
        "day — the next upcoming meeting, and how much time is in meetings "
        "(#1595)"
    ),
    "_handle_week_calendar_query": (
        "Calendar for the WEEK ahead or several days (this week, next week, the "
        "coming days) — never a single day (#1595)"
    ),
}


# #1667/#1595 flip groups for the calendar cohort — handler_attr → wave-2
# group (see FLIP_GROUPS in workflow_dispatcher.py), mirroring
# _READ_QUERY_FLIP_GROUPS's own-map-not-folded-into-aliases shape above. All
# three calendar handlers answer over a TIME WINDOW the user expressed or
# implied (this week / how much time / recurring) — the paradigm
# read_temporal case. Held out of wave 1 for the same reason as
# changes_query above (kickoff §2.2, time faces unowned); #1887 (2026-09-24)
# gave the product one timezone resolver, which is what changed (Lead
# decision, #1595 epic-0 scope doc, 2026-09-25).
_CALENDAR_QUERY_FLIP_GROUPS: dict[str, str] = {
    "_handle_meeting_time_query": "read_temporal",
    "_handle_recurring_meetings_query": "read_temporal",
    "_handle_week_calendar_query": "read_temporal",
}


# #1595 Phase 3 (Arch's 2026-10-01 ruling, mailboxes/lead/read/rule-arch-to-
# lead-cc-ppm-cxo-temporal-give-get-current-time-a-rail-entry-...-2026-10-01.md):
# get_current_time gets a READ rail entry in flip_group read_temporal so the
# Inversion's live consult (consult_inversion_live, condition 4: dispatches
# only operations in get_action_workflows()) can route pure time/date asks,
# the same way it already routes meeting_time/week_calendar. Without this
# entry, deleting TEMPORAL_PATTERNS would strand its rows on surface 2 (the
# LLM classifier) with no live-consult fallback — Arch's finding that the
# Phase 3 deletion gate's `--live get_current_time`/`--live TEMPORAL` tokens
# were a FALSE live path (named in the flag, no WorkflowEntry to back it).
#
# entry_point wraps the EXISTING canonical handler
# (CanonicalHandlers._handle_temporal_query, canonical_handlers.py) rather
# than reimplementing the clock — the SAME function
# `_requires_canonical_handler`'s TEMPORAL floor/keyword split
# (intent_service.py ~15380) already reaches for a pure date/time ask. That
# handler does its OWN internal content-based routing (agenda / retrospective
# / last-activity / duration sub-detection before falling through to the bare
# date+time response), so wrapping it is safe even for a TEMPORAL-shaped
# message the live consult hands it that isn't a bare "what time is it" —
# the handler's existing detectors take it from there.
#
# effect: READ — _handle_temporal_query reads the clock, the user's stored
# timezone, and (best-effort) calendar context; no writes anywhere in it.
#
# ACTION_REGISTRY disposition: ("TEMPORAL", "get_current_time") STAYS
# CANONICAL (action_registry.py, unchanged by this entry) — NOT flipped to
# WORKFLOW. `can_handle()` claims the ENTIRE TEMPORAL category
# unconditionally (canonical_handlers.py, canonical_categories includes
# TEMPORAL), so in the real `_process_intent_internal` order
# (_should_route_to_floor -> canonical_handlers.can_handle ->
# _dispatch_action_rail), the canonical branch returns BEFORE the action
# rail is ever reached for any TEMPORAL intent — this rail entry is
# unreachable from that path by construction, same as every other
# TEMPORAL/GUIDANCE/PORTFOLIO/CONVERSATION/PROVENANCE canonical-category
# action (none of which has a rail entry either — verified empirically,
# 2026-10-01). Changing the registry to WORKFLOW here would make
# test_registry_disposition_matches_live_runtime
# (test_action_registry.py) FAIL: the modeled live runtime still resolves
# CANONICAL via that same short-circuit, with or without this entry. This
# rail key is consulted ONLY by consult_inversion_live (which REPLACES
# intent.action/category before the normal dispatch order resumes) and by
# the Phase 3 deletion gate's live-match mechanism — never by
# _dispatch_action_rail on the unreplaced path.
async def run_get_current_time_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 TEMPORAL rail entry: dispatches get_current_time via the
    action-dispatch rail by calling the EXISTING canonical temporal handler
    (CanonicalHandlers._handle_temporal_query), never reimplementing the
    clock. See the module-level comment above this function for the full
    disposition/effect/ACTION_REGISTRY reasoning (Arch's 2026-10-01 ruling).

    Converts the handler's dict return into IntentProcessingResult — every
    other rail entry's handler already returns that type directly (they are
    all IntentService methods); this one's source handler lives on
    CanonicalHandlers and returns a dict (the same shape
    CanonicalHandlers.handle() itself converts at the main canonical-dispatch
    call site, intent_service.py ~2800), so this entry point does the one
    conversion none of the other factories above need.
    """
    # Lazy import: IntentProcessingResult lives in intent_service, which this
    # module must not import at module level (circular).
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_temporal_query",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    result = await canonical_handlers._handle_temporal_query(intent, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


get_current_time_entry = WorkflowEntry(
    entry_point=run_get_current_time_workflow,
    effect=EffectClass.READ,
    description="get_current_time via action dispatch (#1595 Phase 3)",
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_group="read_temporal",
)


# ─── read_floor (#1595 Phase 3, Arch's ruling 2026-10-02) ─────────────────────
# Rail adapters for FLOOR-disposition ops, built by ONE factory (the
# `_make_query_dispatch_entry_point` idiom): the entry point calls the EXISTING
# `IntentService._handle_floor_with_context` with the Intent the rail built —
# category from the registry, action = the op — and resolves the user's
# formality baseline and trust stage the SAME way the main path does (the two
# helpers factored out of _process_intent_internal for exactly this). Nothing
# is re-implemented; ACTION_REGISTRY disposition stays FLOOR (a routing
# adapter, not a disposition change — same note as get_current_time's).
#
# Why: the deletion gate found DISCOVERY / TRUST / MEMORY / ANALYSIS patterns
# LOAD-BEARING — the LLM classifier never emits those categories (0 of 620
# samples), so without a pattern every capability/trust/memory question would
# land on a different floor framing (IDENTITY's, CONVERSATION's). The router
# names the right op (DISCOVERY 18/19 on the served model), so the rail is the
# honest owner. Membership is EXPLICIT — the ops those four lists target —
# never "every FLOOR op". The flip itself is Phase-2-gated like any wave.
_READ_FLOOR_MEMBERS: dict[str, str] = {
    # op → the registry category the floor engages under (read back from
    # ACTION_REGISTRY at registration, never trusted from this table alone).
    "get_capabilities": "DISCOVERY",
    "explain_trust": "TRUST",
    "get_memory": "MEMORY",
    "pull_insights": "MEMORY",
    "analyze_blockers": "ANALYSIS",
}


def _make_read_floor_entry_point(op: str, category: str):
    """Factory for a read_floor rail adapter (see the block comment above)."""

    async def run_read_floor_workflow(
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        ctx = context or {}
        intent_service = ctx.get("intent_service")
        intent = ctx.get("intent")
        if intent_service is None or intent is None:
            logger.error(
                "read_floor_missing_context",
                operation=op,
                has_intent_service=intent_service is not None,
                has_intent=intent is not None,
            )
            return None
        # The floor engages under the op's OWN category (the whole point of
        # the group — the classifier would have put it elsewhere). The rail
        # may have built the Intent under QUERY (its honest default for a
        # rail key with no registry category); re-key it to the registry's.
        try:
            intent.category = IntentCategory[category]
        except KeyError:  # defensive: the member table is pinned against the enum
            logger.error("read_floor_unknown_category", operation=op, category=category)
            return None
        intent.action = op
        formality_baseline = await intent_service._resolve_formality_baseline(user_id)
        trust_stage = await intent_service._resolve_trust_stage(user_id)
        return await intent_service._handle_floor_with_context(
            intent,
            session_id,
            user_id=user_id,
            formality_baseline=formality_baseline,
            trust_stage=trust_stage,
        )

    run_read_floor_workflow.__name__ = f"run_read_floor_{op}_workflow"
    return run_read_floor_workflow


def _read_floor_entries() -> dict[str, WorkflowEntry]:
    """One READ entry per member op, each cross-checked against ACTION_REGISTRY
    (the member must exist under that category with FLOOR disposition — a
    typo here fails loudly at registration, never at a user's turn)."""
    from services.intent_service.action_registry import (
        ACTION_DESCRIPTIONS,
        ACTION_REGISTRY,
        ActionDisposition,
    )

    entries: dict[str, WorkflowEntry] = {}
    for op, category in _READ_FLOOR_MEMBERS.items():
        disposition = ACTION_REGISTRY.get((category, op))
        if disposition is not ActionDisposition.FLOOR:
            raise ValueError(
                f"read_floor member ({category}, {op}) is not a FLOOR-disposition registry action "
                f"(got {disposition!r}) — the group is for floor adapters only"
            )
        # The ROUTER reads a rail entry's description (derive_routing_grammar
        # prefers it over ACTION_DESCRIPTIONS once an op has an entry), so the
        # adapter must carry the registry's own text for the op — found the
        # hard way 2026-10-02: a "via the read_floor rail adapter" label
        # stripped to the bare name and the router declined every TRUST row.
        registry_text = ACTION_DESCRIPTIONS.get((category, op), "")
        entries[op] = WorkflowEntry(
            entry_point=_make_read_floor_entry_point(op, category),
            effect=EffectClass.READ,
            description=f"{registry_text} (#1595 read_floor)"
            if registry_text
            else f"{op} (#1595 read_floor)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group="read_floor",
        )
    return entries


# ─── read_floor_2 (#1595 Phase 3 wave 2, Arch's ruling 2026-10-03) ────────────
# A SECOND, separate flip group for more FLOOR-disposition rail adapters —
# built as its OWN group rather than widened into `read_floor`, because
# `read_floor` is already LIVE on alpha: adding a member to that group would
# make it live on the next deploy with no PM flag token. Same shape as
# `read_floor` in every other respect (one factory — reused, not duplicated,
# since `_make_read_floor_entry_point` is already op/category-generic and
# carries no group-specific state — explicit membership, Phase-2-gated,
# NOT flipped).
#
# Membership, each checked against the handler/registry rather than assumed
# from the verb (Arch's ruling, section 1):
#   - `get_feature_info` (QUERY, GET): clean member — pre_classifier
#     FEATURE_INFO_PATTERNS is its only surface-1 path
#     (action_registry.py ACTION_DESCRIPTIONS: "Provide details about a
#     specific Piper feature or integration"); FLOOR-handled, no persistence
#     anywhere in services/ (git grep "get_feature_info" -- services/ shows
#     only the registry row and the pre_classifier pattern wiring).
#   - `check_completion_status` (STATUS, GET): clean member — same shape,
#     COMPLETION_HISTORY's only surface-1 path, FLOOR-answered, no
#     persistence (git grep shows only the registry row and pre_classifier).
#   - `write_stakeholder_update` (QUERY, COMPOSE): a member because its floor
#     path persists NOTHING. `git grep -rn stakeholder -- services/` outside
#     action_registry.py/pre_classifier.py returns nothing — there is no
#     stakeholder-update handler, save, or repository write anywhere in
#     services/. Its category (QUERY) has no dedicated branch in
#     `ContextAssembler.gather_context` (context_assembler.py:355-412), so it
#     falls to the generic `else` baseline (`_gather_status_priority_context`,
#     read-only) and `ConversationalFloor.respond()` drafts the prose
#     directly (action_registry.py's own comment: "#1256: FLOOR drafts the
#     prose for an outbound stakeholder update" — a session-snapshot answer,
#     not a saved domain record). Session text that isn't written anywhere
#     is not a domain write.
#   - `get_identity` (IDENTITY, GET): a member. Arch's check (d) — does the
#     deletion gate already credit IDENTITY_PATTERNS' rows via surface-2
#     evidence — was run FIRST and says no:
#     `scripts/inversion_phase3_deletion_gate.py --list IDENTITY_PATTERNS
#     --live create_reminder,create_todo,delete_todo,read_floor,read_referent,
#     read_status,read_strategic,read_synthesis,read_temporal` still shows
#     the one claimed row, "who are you?", as [FAIL]: "REVIEW-agrees
#     (route=get_identity == claim=get_identity) but on a NON-LIVE op
#     (not-live (no WorkflowEntry — the live consult dispatches rail keys
#     only)); no surface-2 probe for this phrase." No SURFACE2_FLOOR_PROBES
#     report carries an IDENTITY_PATTERNS phrase landing under its OWN
#     action (the IDENTITY hits in the set5 probes are DISCOVERY_PATTERNS
#     phrases like "what are your capabilities?" landing on get_capabilities
#     under the IDENTITY *category* — a different list's row, not this
#     one's). So (d) does not credit it: no rail entry exists yet (the
#     chicken-and-egg this build resolves) and no probe covers "who are
#     you?" — it stays a live behaviour change, not a same-destination
#     deletion, and this wave gives it the rail entry condition (d) was
#     testing for.
_READ_FLOOR_2_MEMBERS: dict[str, str] = {
    # op → the registry category the floor engages under (read back from
    # ACTION_REGISTRY at registration, never trusted from this table alone).
    "get_feature_info": "QUERY",
    "check_completion_status": "STATUS",
    "write_stakeholder_update": "QUERY",
    "get_identity": "IDENTITY",
}


def _read_floor_2_entries() -> dict[str, WorkflowEntry]:
    """One READ entry per `_READ_FLOOR_2_MEMBERS` op, same shape as
    `_read_floor_entries()` above but flip_group="read_floor_2" — its OWN
    group, not a widening of `read_floor` (which is already live). Reuses
    `_make_read_floor_entry_point`: that factory is op/category-generic and
    carries no group-specific state, so building a second factory here would
    just be the same code twice."""
    from services.intent_service.action_registry import (
        ACTION_DESCRIPTIONS,
        ACTION_REGISTRY,
        ActionDisposition,
    )

    entries: dict[str, WorkflowEntry] = {}
    for op, category in _READ_FLOOR_2_MEMBERS.items():
        disposition = ACTION_REGISTRY.get((category, op))
        if disposition is not ActionDisposition.FLOOR:
            raise ValueError(
                f"read_floor_2 member ({category}, {op}) is not a FLOOR-disposition registry "
                f"action (got {disposition!r}) — the group is for floor adapters only"
            )
        registry_text = ACTION_DESCRIPTIONS.get((category, op), "")
        entries[op] = WorkflowEntry(
            entry_point=_make_read_floor_entry_point(op, category),
            effect=EffectClass.READ,
            description=f"{registry_text} (#1595 read_floor_2)"
            if registry_text
            else f"{op} (#1595 read_floor_2)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group="read_floor_2",
        )
    return entries


# ─── read_canonical (#1595 Phase 3, Arch's ruling 2026-10-03, section 3:
# "Two 'CANONICAL writes' are reads") ──────────────────────────────────────
# `explain_suggestion` (PROVENANCE, CANONICAL, verb EXPLAIN) and
# `get_contextual_guidance` (GUIDANCE, CANONICAL, verb GET) mutate nothing by
# verb. Per Arch's instruction: use the `get_current_time` precedent above —
# a READ rail adapter wrapping the EXISTING canonical handler, explicit
# membership in a NAMED group (never a raw category token, since GUIDANCE
# is a whole category — CanonicalHandlers.can_handle claims it
# unconditionally), ACTION_REGISTRY disposition unchanged (CANONICAL).
#
# Verified READ end to end from each handler before grouping (Arch's
# instruction, "as wave 3 did"):
#
#   - get_contextual_guidance → CanonicalHandlers._handle_guidance_query
#     (canonical_handlers.py:4201-4333). All three setup-detection branches
#     (_handle_project_setup_request:2319-2395,
#     _format_integration_setup_guidance:2397-2492,
#     _format_general_setup_guidance:2494-2541) plus the main synthesis
#     path (_get_calendar_context, _get_project_metadata,
#     _get_priority_metadata, _synthesize_focus_recommendation,
#     _format_detailed_guidance / _format_consolidated_guidance /
#     _format_standard_guidance, _get_immediate_focus —
#     canonical_handlers.py:1387-2220) read only: user_context_service,
#     best-effort calendar context, project/priority metadata,
#     IntegrationStatusService.get_all. `sed -n '1387,2220p'
#     canonical_handlers.py | grep -n '\.save(\|\.create(\|\.update(\|
#     \.delete(\|session\.add\|session\.commit\|\.persist(\|INSERT'`
#     returns nothing over the whole span. ADR-059: interactive portfolio
#     onboarding is disabled ("on ice") — the project-setup branch returns
#     static/read-derived guidance text, never launches a workflow or
#     writes a record.
#   - explain_suggestion → CanonicalHandlers._handle_provenance_query
#     (canonical_handlers.py:5603-5764). Reads
#     conversation_context.get_or_create_context — an in-process,
#     module-level dict (`_conversation_contexts`,
#     conversation_context.py:397) scoped to the running process, never
#     persisted to the database and not a domain write — and, on a sidecar
#     miss, falls back to ConversationRepository.get_most_recent_turn_
#     provenance (a read query). No .save/.create/.update/.delete/
#     session.add/session.commit anywhere in the function; it formats a
#     colleague-prose citation from what it read and returns.
#     logger.info/warning/error calls only — no persisted or external
#     state change.
#
# ACTION_REGISTRY disposition for both STAYS CANONICAL (unchanged) — same
# reasoning as get_current_time's: CanonicalHandlers.can_handle() claims
# the WHOLE PROVENANCE/GUIDANCE category unconditionally, so in the real
# dispatch order (_should_route_to_floor -> can_handle -> action rail) the
# canonical branch returns before the action rail is ever reached for
# either intent. This rail entry is unreachable from that path by
# construction — consulted only by consult_inversion_live (which REPLACES
# intent.action/category before the normal dispatch order resumes) and by
# the Phase 3 deletion gate's live-match mechanism, never by
# _dispatch_action_rail on the unreplaced path.
#
# Collision check (2026-10-04): "read_canonical" is not in FLIP_GROUPS
# (workflow_dispatcher.py, prior to this change) and does not appear
# anywhere in derive_routing_grammar()'s output (grep over services/ and
# scripts/) — no existing op or group answers to this name.
_READ_CANONICAL_MEMBERS: dict[str, tuple[str, str]] = {
    # op → (registry category, CanonicalHandlers method name to wrap)
    "explain_suggestion": ("PROVENANCE", "_handle_provenance_query"),
    "get_contextual_guidance": ("GUIDANCE", "_handle_guidance_query"),
}


def _make_read_canonical_entry_point(op: str, handler_attr: str):
    """Factory for a read_canonical rail adapter: calls the EXISTING
    CanonicalHandlers method ``handler_attr`` directly (never reimplementing
    it), the same shape as ``run_get_current_time_workflow`` above. Unlike
    ``_make_read_floor_entry_point``, this does NOT re-key intent.category —
    neither wrapped handler branches on intent.category (verified by
    reading both; see the block comment above), so there is nothing to
    re-key before calling straight through."""

    async def run_read_canonical_workflow(
        session_id: str,
        user_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        from services.intent.intent_service import IntentProcessingResult

        ctx = context or {}
        intent_service = ctx.get("intent_service")
        intent = ctx.get("intent")
        if intent_service is None or intent is None:
            logger.error(
                "read_canonical_missing_context",
                operation=op,
                handler=handler_attr,
                has_intent_service=intent_service is not None,
                has_intent=intent is not None,
            )
            return None
        canonical_handlers = intent_service.canonical_handlers
        handler = getattr(canonical_handlers, handler_attr)
        result = await handler(intent, session_id, user_id)
        return IntentProcessingResult(
            success=True,
            message=result["message"],
            intent_data=result.get("intent"),
            workflow_id=None,
            requires_clarification=result.get("requires_clarification", False),
        )

    run_read_canonical_workflow.__name__ = f"run_read_canonical_{op}_workflow"
    return run_read_canonical_workflow


def _read_canonical_entries() -> dict[str, WorkflowEntry]:
    """One READ entry per `_READ_CANONICAL_MEMBERS` op, cross-checked
    against ACTION_REGISTRY (the member must exist under that category with
    CANONICAL disposition — a typo here fails loudly at registration, never
    at a user's turn)."""
    from services.intent_service.action_registry import (
        ACTION_DESCRIPTIONS,
        ACTION_REGISTRY,
        ActionDisposition,
    )

    entries: dict[str, WorkflowEntry] = {}
    for op, (category, handler_attr) in _READ_CANONICAL_MEMBERS.items():
        disposition = ACTION_REGISTRY.get((category, op))
        if disposition is not ActionDisposition.CANONICAL:
            raise ValueError(
                f"read_canonical member ({category}, {op}) is not a CANONICAL-disposition "
                f"registry action (got {disposition!r}) — the group is for canonical "
                "adapters only"
            )
        # The ROUTER reads a rail entry's description (derive_routing_grammar
        # prefers it over ACTION_DESCRIPTIONS once an op has an entry — the
        # read_floor rule, 2026-10-02), so the adapter must carry the
        # registry's own text for the op.
        registry_text = ACTION_DESCRIPTIONS.get((category, op), "")
        entries[op] = WorkflowEntry(
            entry_point=_make_read_canonical_entry_point(op, handler_attr),
            effect=EffectClass.READ,
            description=f"{registry_text} (#1595 read_canonical)"
            if registry_text
            else f"{op} (#1595 read_canonical)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group="read_canonical",
        )
    return entries


# ─── read_portfolio (#1595 Phase 3, Arch's ruling 2026-10-03, section 2:
# "manage_repos: split into three ops") ────────────────────────────────────
# manage_repos (PORTFOLIO, CANONICAL, verb MANAGE) splits by effect class:
# list [READ] / link [WRITE] / unlink [DESTRUCTIVE]. This group holds the
# LIST half — `list_repos` — separate from read_canonical (section 3's
# group is a distinct ruling item; this one is section 2's). link and
# unlink are NOT built here (separate task, WRITE/DESTRUCTIVE shapes with
# #1677 allowlist + confirm-build conditions per the same ruling) and are
# not members of this group.
#
# 2026-10-04 (Arch's ruling, same file §1): `search_projects` — the READ
# fourth of manage_portfolio's OWN split (a different CANONICAL action
# from manage_repos, same PORTFOLIO category) — JOINS `list_repos` in
# THIS group, not a new one. Arch's own words: "list_projects: reuse the
# LIVE QUERY entry and add search_projects to read_portfolio, with no
# re-home." `list_projects` itself is deliberately NOT a member (see the
# naming-collision note by archive_project_entry below) — only the search
# op is new here. This widens an EXISTING, already-live flip_group from
# one member to two; Exec/PM must re-run the Phase-2 gate and re-send the
# PM token naming BOTH members before flipping it (the prior token's
# evidence covered list_repos only).
#
# Same get_current_time precedent as read_canonical above: a READ rail
# adapter wrapping the EXISTING canonical handler
# (CanonicalHandlers._handle_list_repos) directly — never reimplementing
# the list logic. _handle_list_repos was ITSELF hoisted out of
# _handle_repo_management's LIST branch for this (canonical_handlers.py):
# _handle_repo_management's own LIST case now early-returns to the same
# method, so the legacy canonical dispatch (manage_repos) is unchanged
# behaviourally (pinned in test_repo_management.py) and this is the ONLY
# place the list response is built.
#
# Verified READ end to end (2026-10-04): _handle_list_repos opens a
# session_scope and only calls ProjectRepository.find_by_name,
# RepositoryRepository.list_by_project, RepositoryRepository.list_by_owner
# — all read queries. `grep -n '\.save(\|\.create(\|\.update(\|\.delete(\|
# session\.add\|session\.commit\|\.persist(\|INSERT' ` over the method
# returns nothing.
#
# ACTION_REGISTRY disposition STAYS CANONICAL (action_registry.py) — same
# reasoning as get_current_time's and read_canonical's:
# CanonicalHandlers.can_handle() claims the WHOLE PORTFOLIO category
# unconditionally (`_handle_portfolio_query` dispatches on
# `intent.action == "manage_repos"` by STRING, never reading
# intent.category's rail membership), so in the real dispatch order
# (_should_route_to_floor -> can_handle -> action rail) the canonical
# branch returns before the action rail is ever reached for a PORTFOLIO
# intent — WORKFLOW disposition here would fail
# test_registry_disposition_matches_live_runtime's oracle (verified by
# tracing `_true_disposition_for_registry_row`, test_action_registry.py:
# it checks `can_handle()` before the rail, and `can_handle` only reads
# `intent.category`). This rail entry is unreachable from the unreplaced
# dispatch path by construction — consulted only by consult_inversion_live
# (which REPLACES intent.action/category before the normal dispatch order
# resumes) and by the Phase 3 deletion gate's live-match mechanism.
#
# Collision check (2026-10-04): `list_repos` is not an ACTION_REGISTRY key,
# not a WORKFLOW_REGISTRY/rail key, and does not appear in
# derive_routing_grammar()'s output prior to this change (grep over
# services/ and scripts/) — no existing op answers to it.
# `list_repositories` (the name surface 2 probes invented) IS a live method
# name elsewhere (services/domain/github_domain_service.py,
# services/integrations/github/github_integration_router.py,
# services/mcp/consumer/github_adapter.py) but at a DIFFERENT layer and
# with a DIFFERENT meaning — "every repo on the user's GitHub account", not
# "repos linked to a project" — and is not registered as an
# ACTION_REGISTRY/rail action anywhere, so using `list_repos` here avoids
# conflating the two. `list_linked_repos` is unused anywhere in the
# codebase. "read_portfolio" is not in FLIP_GROUPS prior to this change and
# does not appear in derive_routing_grammar()'s output — no existing group
# answers to this name.
async def run_list_repos_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 PORTFOLIO rail entry: dispatches list_repos via the
    action-dispatch rail by calling the EXISTING
    CanonicalHandlers._handle_list_repos directly, never reimplementing the
    list logic. See the module-level comment above this function for the
    full disposition/effect/ACTION_REGISTRY/collision reasoning (Arch's
    2026-10-03 ruling, section 2).

    Converts the handler's dict return into IntentProcessingResult, the
    same conversion run_get_current_time_workflow does for its own
    CanonicalHandlers-sourced dict (this module's other canonical adapters
    are IntentService methods that already return IntentProcessingResult).
    """
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_list_repos",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    result = await canonical_handlers._handle_list_repos(intent, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


list_repos_entry = WorkflowEntry(
    entry_point=run_list_repos_workflow,
    effect=EffectClass.READ,
    description=(
        "List the GitHub repositories linked to a project (or all of the "
        "user's registered repositories if no project is named) (#1595 "
        "read_portfolio)"
    ),
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_group="read_portfolio",
)


# #1595 Phase 3 (Arch's 2026-10-04 ruling §1): the READ fourth of
# manage_portfolio's split (archive_project/restore_project/add_project —
# the WRITE thirds — are defined further below in this file). Same
# get_current_time precedent as list_repos directly above: a READ rail
# adapter wrapping the EXISTING canonical handler
# (CanonicalHandlers._handle_search_projects) directly — never
# reimplementing the search logic. _handle_search_projects was ITSELF
# hoisted out of _handle_portfolio_query's SEARCH branch for this
# (canonical_handlers.py): _handle_portfolio_query's own SEARCH case now
# early-returns to the same method, so the legacy canonical dispatch
# (manage_portfolio) is behaviourally unchanged (same search/results
# logic; the not-found copy was rewritten non-interrogative per the
# #1766 ratchet, documented in _handle_search_projects's own docstring)
# and this is the ONLY place the search response is built.
#
# ACTION_REGISTRY disposition STAYS CANONICAL (action_registry.py) — same
# verified reasoning as list_repos/archive_project/restore_project/
# add_project: PORTFOLIO is claimed WHOLE by
# CanonicalHandlers.can_handle() (string-tested on intent.action, never
# intent.category's rail membership), so in the real dispatch order
# (_should_route_to_floor -> can_handle -> action rail) the canonical
# branch returns before the action rail is ever reached for a PORTFOLIO
# intent — WORKFLOW disposition here would fail
# test_registry_disposition_matches_live_runtime's oracle. This rail
# entry is unreachable from the unreplaced dispatch path by construction
# — consulted only by consult_inversion_live and the Phase 3 deletion
# gate's live-match mechanism.
#
# Collision check (2026-10-04): `search_projects` is not an
# ACTION_REGISTRY key, not a WORKFLOW_REGISTRY/rail key, and does not
# appear in derive_routing_grammar()'s output prior to this change
# (`git grep -n "search_projects" services/intent_service/action_
# registry.py services/intent_service/workflow_entries.py services/
# intent_service/workflow_dispatcher.py services/intent_service/
# pre_classifier.py` returns nothing) — no existing op answers to it. The
# name IS used elsewhere as a Python method name only
# (PortfolioService.search_projects / ProjectRepository.search_projects,
# a different layer — the DB query, not the rail action) and as the
# "action" value this handler's OWN dict has returned since #675/#1762,
# never previously as a registry/rail KEY — no conflation.
async def run_search_projects_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 PORTFOLIO rail entry: dispatches search_projects via
    the action-dispatch rail by calling the EXISTING
    CanonicalHandlers._handle_search_projects directly, never
    reimplementing the search logic. See the module-level comment above
    this function for the full disposition/effect/ACTION_REGISTRY/
    collision reasoning (Arch's 2026-10-04 ruling, section 1).
    """
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_search_projects",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    result = await canonical_handlers._handle_search_projects(intent, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


search_projects_entry = WorkflowEntry(
    entry_point=run_search_projects_workflow,
    effect=EffectClass.READ,
    description=("Search the user's projects by a name substring (#1595 read_portfolio)"),
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_group="read_portfolio",
)


# ─── manage_portfolio WRITE split (#1595 Phase 3, Arch's 2026-10-04 ruling,
# mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-execute-vocab-
# coverage-portfolio-split-file-reference-2026-10-04.md §2) ───────────────
# manage_portfolio (PORTFOLIO, CANONICAL, verb MANAGE) splits by effect
# class, same rule as manage_repos above: archive_project / restore_project
# (WRITE, separate ops — inverse verbs read clearer to the router) and
# add_project (WRITE; its terminal effect creates the Project — the no-name
# turns that ask for a name are that op's slot-filling, not a separate op).
#
# NOT built here: `list_projects` (the READ fourth — active list + search).
# BLOCKING COLLISION, reported to Lead rather than silently resolved:
# "list_projects" is ALREADY a registered rail key (this file, the
# `_query_cohort` list below, alias ["list_projects", "show_projects"]) —
# CanonicalHandlers.can_handle intent_service._handle_projects_query, QUERY
# category, flip_group read_status, format via format_projects_conscious,
# active-list ONLY (no search). `_default_entries` is a single Python dict:
# a second `_default_entries["list_projects"] = ...` assignment inside THIS
# literal would be silently clobbered by the `_query_cohort` loop that runs
# later in this same module (assigns `_default_entries[alias] = entry` for
# every alias in that cohort, "list_projects" included) — the two entries
# cannot coexist under one key regardless of category/dispatch-path
# reasoning, so this is a REAL collision, not a false positive from naming
# alone. Per the dispatch instructions ("STOP if they conflict"): stopped.
# `list_archived` is unaffected (delegates to the EXISTING
# `list_archived_projects` entry below — no new key) and all three WRITE
# ops below use brand-new, collision-free names (verified via
# derive_routing_grammar()/get_action_workflows()/ACTION_REGISTRY grep —
# see Lead's handback for the exact commands run).
#
# Verified WRITE end to end (2026-10-04):
#  - archive_project: PortfolioService.archive_project
#    (portfolio_service.py:269-273) sets is_archived=True on the existing
#    row — an UPDATE, nothing deleted; restore_project is its exact inverse.
#  - restore_project: PortfolioService.restore_project
#    (portfolio_service.py:328-331) sets is_archived=False — the reverse
#    UPDATE.
#  - add_project: ProjectRepository.create (canonical_handlers.py,
#    CanonicalHandlers._handle_add_project) persists ONE new Project row;
#    the no-name/already-asked turns only transition PortfolioOnboardingManager
#    session state (ephemeral conversation state, not a domain-table write —
#    Arch's ruling §2 question 2: EffectClass measures domain state that
#    persists beyond the conversation, so this is still ONE op, WRITE, by
#    its terminal effect).
# `grep -n '\.save(\|\.create(\|\.update(\|\.delete(\|session\.add\|
# session\.commit\|\.persist(\|INSERT'` over each hoisted handler confirms
# no call beyond the ones named above.
#
# ACTION_REGISTRY disposition STAYS CANONICAL (action_registry.py) for all
# three — same verified reasoning as list_repos directly above:
# CanonicalHandlers.can_handle() claims the WHOLE PORTFOLIO category
# unconditionally, so the action rail is never reached for a PORTFOLIO
# intent on the unreplaced dispatch path; these rail entries exist only for
# consult_inversion_live and for `inversion_live.registry_category_for`'s
# #1920 cross-family lookup (which reads ACTION_REGISTRY, never the rail) —
# see the #1920 note on each WorkflowEntry below.
#
# NO flip_group on any of the three (non-READ keys never carry one, per
# WorkflowEntry.__post_init__'s structural guard) — each flips only by its
# own FLIP_WRITE_ALLOWLIST name (workflow_dispatcher.py), never by a wave.
# (list_archived needed no new entry at all — it delegates to the EXISTING
# run_archived_projects_query_workflow, defined earlier in this file.)
async def run_archive_project_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 PORTFOLIO rail entry: dispatches archive_project via
    the action-dispatch rail by calling the EXISTING
    CanonicalHandlers._handle_archive_project directly, never reimplementing
    the archive logic. See the module-level comment above this function for
    the full disposition/effect/ACTION_REGISTRY/collision reasoning (Arch's
    2026-10-04 ruling, section 2).
    """
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_archive_project",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    result = await canonical_handlers._handle_archive_project(intent, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


archive_project_entry = WorkflowEntry(
    entry_point=run_archive_project_workflow,
    effect=EffectClass.WRITE,
    outwardness=Outwardness.PRIVATE,
    description=(
        "Archive (soft-delete) a project by name — reversible via "
        "restore_project (#1595 Phase 3)"
    ),
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_write_allowlist_key="archive_project",
)


async def run_restore_project_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 PORTFOLIO rail entry: dispatches restore_project via
    the action-dispatch rail by calling the EXISTING
    CanonicalHandlers._handle_restore_project directly. Mirrors
    run_archive_project_workflow directly above.
    """
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_restore_project",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    result = await canonical_handlers._handle_restore_project(intent, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


restore_project_entry = WorkflowEntry(
    entry_point=run_restore_project_workflow,
    effect=EffectClass.WRITE,
    outwardness=Outwardness.PRIVATE,
    description=(
        "Restore a previously archived project by name — reversible via "
        "archive_project (#1595 Phase 3)"
    ),
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_write_allowlist_key="restore_project",
)


async def run_add_project_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """#1595 Phase 3 PORTFOLIO rail entry: dispatches add_project via the
    action-dispatch rail by calling the EXISTING
    CanonicalHandlers._handle_add_project directly (#1856's own method —
    no hoist needed, it was already its own method before this unit). That
    method takes ``(original_message, session_id, user_id)``, not
    ``(intent, session_id, user_id)`` like the other canonical adapters in
    this file, so this wrapper extracts ``original_message`` from the
    intent's context the same way every other PORTFOLIO branch does.
    """
    from services.intent.intent_service import IntentProcessingResult

    ctx = context or {}
    intent_service = ctx.get("intent_service")
    intent = ctx.get("intent")
    if intent_service is None or intent is None:
        logger.error(
            "query_dispatch_missing_context",
            handler="_handle_add_project",
            has_intent_service=intent_service is not None,
            has_intent=intent is not None,
        )
        return None
    canonical_handlers = intent_service.canonical_handlers
    original_message = (intent.context or {}).get("original_message", "")
    result = await canonical_handlers._handle_add_project(
        original_message=original_message,
        session_id=session_id,
        user_id=user_id,
    )
    return IntentProcessingResult(
        success=True,
        message=result["message"],
        intent_data=result.get("intent"),
        workflow_id=None,
        requires_clarification=result.get("requires_clarification", False),
    )


add_project_entry = WorkflowEntry(
    entry_point=run_add_project_workflow,
    effect=EffectClass.WRITE,
    outwardness=Outwardness.PRIVATE,
    description=(
        "Create a new project in the user's portfolio, optionally linking a "
        "named GitHub repo in the same utterance; asks once for a name if "
        "the utterance didn't carry one (#1595 Phase 3)"
    ),
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_write_allowlist_key="add_project",
)


# #1124 analysis cohort — the ANALYSIS-category handlers (analyze_commits /
# generate_report / analyze_data) via the standard factory. #1641: 3-arg since
# the repo-question wiring — ``session_id`` threads (pass_session_id) so the
# 'repository not specified' ask can bind via the #846 pending-offer store.
# NOT included: analyze_document (the if-head) — Notion-coupled, deferred to
# its own bite. Aliases mirror the migrated elif branches exactly.
_ANALYSIS_QUERY_COHORT: dict[str, list[str]] = {
    "_handle_analyze_commits": ["analyze_commits", "analyze_code"],
    "_handle_generate_report": ["generate_report", "create_report"],
    "_handle_analyze_data": ["analyze_data", "evaluate_metrics"],
}


def register_default_workflows() -> None:
    """
    Register all default workflow entry points.

    Called during application startup. To add a new workflow:
    1. Write an entry point function above
    2. Add an entry to ``_default_entries`` below

    Idempotent: the container's process-registry init can run more than once in
    a process (the process registry already tolerates this by replacing handlers).
    register_workflow() itself stays strict (raises on duplicate keys, to catch
    genuine wiring bugs), so this orchestrator skips any key already present
    rather than re-registering. A bare double-call is therefore a safe no-op.
    """
    # #1124 cohort 1: document update — direct action-dispatch workflow.
    # All three classifier aliases share one entry point; action_triggered lets
    # the intent_service action-dispatch rail pick them up (vs offer-only
    # workflows like meeting, which stay action_triggered=False).
    # effect: WRITE — _handle_update_document_notion appends content to a Notion
    # page (notion_router.append_blocks, intent_service.py ~L3409). Recoverable
    # (page history), so WRITE not DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — appending to a doc teammates can
    # read is CXO's named non-example: nobody is handed anything right now.
    document_update_entry = WorkflowEntry(
        entry_point=run_update_document_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Document update via slot-filling (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1124 cohort 1 migration #3: changes-query — dispatch migration. The four
    # classifier aliases (verified live as stable) share one entry point.
    # effect: READ — _handle_changes_query reads GitHub activity for a time
    # window and formats it; no mutating router calls anywhere in its body.
    # flip_group (#1667/#1595 wave 2, 2026-09-25): read_temporal. "What
    # changed SINCE X" parses a user-supplied time expression
    # (_parse_time_expression, days-as-int, called out in this entry point's
    # own docstring as a bounded-but-real temporal parser) — exactly the
    # read_temporal class. Held out of wave 1 because time faces were
    # unowned (kickoff §2.2 puts temporal last among queries); #1887
    # (2026-09-24) gave the product one timezone resolver, which is the
    # thing that changed. Effect confirmed still READ (unchanged from
    # above) before grouping — flip_group is unconstructible on a non-READ
    # entry.
    changes_query_entry = WorkflowEntry(
        entry_point=run_changes_query_workflow,
        effect=EffectClass.READ,
        description="What-changed-since query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_group="read_temporal",
    )

    # #1124 Phase 4 step 3: issue-mutation cohort (CLOSE / REOPEN / COMMENT verbs).
    # Each handler reused unchanged; all classifier aliases share one entry point.
    # effect: DESTRUCTIVE (#1190, PM ruling decisions.log 2026-08-10 ~10:55) —
    # _handle_close_issue_query calls
    # github_router.update_issue(issue_number, state="closed") (~L4264).
    # The old rationale ("reversible via reopen, so WRITE") classified by
    # RECOVERABILITY; the ruling classifies by BLAST RADIUS: closing an issue
    # removes it from every open-state board, query, and sprint view at once
    # (the 2026-07 auto-close incident closed a live Beta Blocker from a
    # commit message). needs_confirm derives True → the #1190 confirmation
    # gate defers execution to an explicit yes/no turn.
    # outwardness: PRIVATE (#1509 axis) — PPM's stress-tested boundary case,
    # SETTLED 2026-08-15, do not re-litigate: a close creates/sends no
    # content, so it is not a communication act; its board-wide visibility is
    # exactly what the DESTRUCTIVE effect tier (#1190 blast-radius ruling)
    # already covers. The two axes are jointly exhaustive over reasons for
    # care, not redundant nets over the same actions.
    close_issue_entry = WorkflowEntry(
        entry_point=run_close_issue_workflow,
        effect=EffectClass.DESTRUCTIVE,
        outwardness=Outwardness.PRIVATE,
        description="Close-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    # #1411: update_issue onto the rail (was elif-only surface-4, registry/rail-invisible
    # → mode-4 reachability gap for every update request). Reuses the fully-implemented
    # _handle_update_issue (intent, workflow_id, user_id) via the standard factory. The
    # legacy elif is REMOVED (migration completion): the rail is the single dispatch
    # surface — B3 Stage-0 referent resolution emits update_issue onto this same key.
    # effect: WRITE — _handle_update_issue calls github_router.update_issue with
    # title/body/label fields (~L7594). Prior values recoverable via GitHub edit
    # history, so WRITE not DESTRUCTIVE.
    # #1411 clarify-first (2026-08-13): session_id threaded too — the unmapped
    # status-value ask binds via the #846 pending-offer store, which is
    # session-keyed. Handler signature is (intent, workflow_id, session_id,
    # user_id), the _handle_create_issue shape.
    update_issue_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point(
            "_handle_update_issue", pass_session_id=True, pass_user_id=True
        ),
        effect=EffectClass.WRITE,
        # outwardness: PRIVATE (#1509 axis) — editing an issue's
        # title/body/labels is repo-content editing (CXO's named
        # non-example family): no content lands in front of anyone as a
        # direct, immediate consequence.
        outwardness=Outwardness.PRIVATE,
        description="Update-issue via action dispatch (#1411)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    # #1412: create_issue onto the rail (same mode-4 gap as #1411; the live primary
    # write path). _handle_create_issue takes (intent, workflow_id, session_id, user_id),
    # so BOTH pass_session_id + pass_user_id. Elif stays as an additive backstop.
    # effect: WRITE — _handle_create_issue calls github_router.create_issue
    # (~L7392): creates a new GitHub issue. Additive, so WRITE not DESTRUCTIVE.
    create_issue_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point(
            "_handle_create_issue", pass_session_id=True, pass_user_id=True
        ),
        effect=EffectClass.WRITE,
        # outwardness: OUTWARD (#1509 axis) — filing an issue IS a
        # communication act: it lands in front of the team (boards, watchers,
        # notifications) as a direct, immediate consequence. This is the
        # Jake-incident action class — the reason the axis exists.
        outwardness=Outwardness.OUTWARD,
        description="Create-issue via action dispatch (#1412)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    # effect: DESTRUCTIVE (#1190, PM ruling decisions.log 2026-08-10 ~10:55) —
    # _handle_reopen_issue_query calls
    # github_router.update_issue(issue_number, state="open") (~L4475).
    # Same blast-radius rationale as close (a reopen resurrects an issue onto
    # every open-state surface — sprint boards, counts, portfolio reviews —
    # in one stroke); recoverability was the old WRITE rationale and is
    # retired. needs_confirm derives True → #1190 confirmation gate.
    # outwardness: PRIVATE (#1509 axis) — same settled boundary case as
    # close above (PPM 2026-08-15): not a communication act; the effect
    # axis already covers its visibility.
    reopen_issue_entry = WorkflowEntry(
        entry_point=run_reopen_issue_workflow,
        effect=EffectClass.DESTRUCTIVE,
        outwardness=Outwardness.PRIVATE,
        description="Reopen-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    # effect: WRITE — _handle_comment_issue_query calls
    # github_router.add_comment(issue_number, comment_body) (~L4597). Additive.
    # outwardness: OUTWARD (#1509 axis) — posting a comment is the axis's
    # defining communication act: content lands in front of everyone
    # watching the issue as a direct, immediate consequence, however easy
    # the underlying write is to delete.
    comment_issue_entry = WorkflowEntry(
        entry_point=run_comment_issue_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.OUTWARD,
        description="Comment-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1124 cohort 1: prioritization — strategy-category handler, 2-arg
    # (intent, workflow_id), reused unchanged via the parameterized factory.
    # effect: READ — the ruling's own cautionary example: `prioritization`
    # SOUNDS like a bulk-write and writes NOTHING. _handle_prioritization
    # scores/ranks items entirely in memory (_calculate_*_scores /
    # _rank_items_by_score) and returns the ranking as a message. No router,
    # DB, or session writes anywhere in its body.
    prioritization_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_prioritization"),
        effect=EffectClass.READ,
        description="Prioritization via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        # flip_group (#1667/#1595 wave 3, 2026-09-25): read_strategic. Was
        # deliberately ungrouped through wave 1 — it ranks in memory and
        # writes nothing (see the effect note above), so it was already
        # flip-SAFE; it simply wasn't one of wave 1's three classes, and
        # `prioritize` is the ruling's own cautionary example of a name that
        # SOUNDS like a bulk write. It joins read_strategic now (wave 3, the
        # plan/priority/pattern/content class) rather than staying an
        # unaddressable one-op-only reach — effect re-confirmed READ before
        # grouping.
        flip_group="read_strategic",
    )

    # #1124: content generation — synthesis-category handler, 2-arg, reused unchanged.
    # effect: READ — despite "generate": _handle_generate_content routes to
    # _generate_status_report / _generate_readme_section / _generate_issue_template,
    # all of which READ repo metrics and return generated TEXT in the result
    # message. Nothing is written to GitHub, Notion, disk, or DB.
    generate_content_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_generate_content"),
        effect=EffectClass.READ,
        description="Content generation via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        # flip_group (#1667/#1595 wave 3, 2026-09-25): read_strategic. Was
        # deliberately excluded from read_synthesis in wave 1 — it generates
        # prose (status report / README section / issue template) and writes
        # nothing, so it looked like a summarize sibling, but read_synthesis
        # is the SUMMARIZE family specifically (PM's named parity area, per
        # kickoff §2.2 item 3), and admitting a generation op there would
        # quietly have redefined that group as "anything whose output is
        # prose". read_strategic is the reviewed extension this was held for:
        # generated content over the user's own material, alongside
        # planning/prioritization/pattern-learning — effect re-confirmed
        # READ before grouping. PA's issue/commit summarize gap remains
        # read_synthesis's own, unaffected by this.
        flip_group="read_strategic",
    )

    # RECONNECT #1327 gap 1: conversational "set my default repo to owner/name".
    # 2-arg (intent, workflow_id) handler, reused via the standard factory. Routed
    # via the action-dispatch rail (action_triggered) — NOT a hand-coded elif branch.
    # effect: WRITE — _handle_set_default_repo persists the preference to the
    # DB: ConnectorConfigService(session).set_default_repo(user_id, full_name)
    # (~L4847). Overwritable, so WRITE not DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — writes the user's OWN preference
    # row; nobody else witnesses anything.
    # #1595 unit 3c (2026-09-27, for #1606's set-default-repo half): the
    # third named write on the inversion flip, via the same #1677 allowlist
    # mechanism create_todo/create_reminder/delete_todo used — not a relaxed
    # effect check, not a flip_group (no wave sweeps a write in). Arch's
    # three conditions RE-RUN today, not cited from #1327's original ruling:
    #   1. registered — get_action_workflows()["set_default_repo"] exists,
    #      action_triggered=True (this entry). No alias family: ActionMapper
    #      has no set_default_repo entry to canonicalize (this op is reached
    #      via the pre-classifier's SET_DEFAULT_REPO_PATTERNS, which emits
    #      the literal action string "set_default_repo" directly — see
    #      pre_classifier.py ~L1379-1393 — and via the LLM classifier /
    #      inversion router, both of which target the same registry
    #      canonical). ACTION_REGISTRY files it as
    #      ("QUERY", "set_default_repo") (action_registry.py:150) and
    #      derive_routing_grammar() emits "set_default_repo" as the (only,
    #      alias-free) canonical for this rail key. So the allowlist key
    #      below is "set_default_repo" — matches both the registry and rail
    #      canonical; there is no alias to distinguish it from.
    #   2. effect correct BY BEHAVIOR — _handle_set_default_repo
    #      (services/intent/intent_service.py ~L7305-7406) parses an
    #      owner/name token from the message, then calls (line ~7375)
    #      `ConnectorConfigService(session).set_default_repo(_user_id,
    #      full_name)`, which itself (services/connectors/config_service.py
    #      ~L52-61) reads the owner's github config blob, sets
    #      `config[DEFAULT_REPO_KEY] = value` (overwriting any prior value
    #      while "preserving other keys" per its own docstring), and upserts
    #      the blob back. One key in a JSONB blob is replaced; nothing is
    #      deleted anywhere in the call chain, and the prior value is not
    #      lost in the DESTRUCTIVE sense — the user can set it back with the
    #      same command. WRITE, never DESTRUCTIVE — same overwrite-preference
    #      shape as set_timezone (also WRITE, PRIVATE, unallowlisted-but-READ-
    #      guard-irrelevant since it's never been on this list).
    #   3. reaches consent — needs_consent derives True (WRITE >= WRITE) and
    #      the SAME entry-agnostic rail block create_todo/create_reminder/
    #      delete_todo use (intent_service.py's `_dispatch_action_rail`,
    #      ~L15717-15794) awaits consent_gate.evaluate_consent with THIS
    #      entry's effect + outwardness before dispatch — it already ran
    #      identically for set_default_repo before this change (#1327
    #      registered it on the rail in the first place); the create_todo/
    #      create_reminder/delete_todo consent spies exercise the SAME code
    #      path under the flip and are mirrored here in
    #      test_inversion_write_allowlist_set_default_repo_1606.py.
    # ⚠️ Unlike its three siblings, this entry's ACTION_REGISTRY category is
    # QUERY, not EXECUTION — so naming the raw category token `QUERY` (not a
    # read_* wave) sweeps this write in too. `QUERY` is flip-1's own original
    # unit and by far the broadest category on the rail (most READ query
    # ops live there), so this consequence is worth stating plainly rather
    # than leaving as an inference: an operator flipping `QUERY` is flipping
    # a write, exactly as flipping `EXECUTION` is for the other three named
    # writes. No flip_group here either, for the same reason.
    set_default_repo_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_set_default_repo"),
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Set-default-repo via action dispatch (#1327)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_write_allowlist_key="set_default_repo",
    )

    # #1560: create_reminder onto the rail (the structural half of the #1517
    # capability-gaslighting incident). Its only dispatch was the legacy
    # `elif mapped_action == "create_reminder"` inside _handle_execution_intent —
    # reachable ONLY under category EXECUTION, so a correct create_reminder
    # emission under any other category (TEMPORAL, GUIDANCE, ...) floored, and
    # the floor improvised a capability denial. The rail check in process_intent
    # dispatches by intent.action BEFORE category routing, making dispatch
    # category-independent. Entry point: run_todo_query_workflow, the existing
    # execution-delegation adapter — the rail reaches the SAME handler chain the
    # elif fronts (ActionMapper → todo_handlers.handle_create_reminder); no
    # duplicated logic. The elif stays (additive backstop, #1412 precedent; it is
    # not a ratchet-counted site — the ratchet counts `if/elif intent.action in [`).
    # effect: WRITE — handle_create_reminder persists a reminder row via
    # todo_service.create_todo (todo_handlers.py ~L624). Additive + recoverable
    # (a todo row the user can delete), so WRITE not DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — a reminder/todo row is the ratified
    # example of a private write (the user's own list; no communication act).
    # #1595 unit 3 (2026-09-25, for #1559): the second named write on the
    # inversion flip, via the same #1677 allowlist mechanism create_todo used
    # — not a relaxed effect check, not a flip_group (no wave sweeps a write
    # in). Arch's three conditions RE-RUN today, not cited from #1560/#1685:
    #   1. registered — get_action_workflows()["create_reminder"] exists,
    #      action_triggered=True (this entry). Alias family enumerated from
    #      ActionMapper (action_mapper.py:89-91): create_reminder /
    #      set_reminder / add_reminder, all canonicalizing to
    #      "create_reminder" — the same name ACTION_REGISTRY files it under
    #      (EXECUTION, action_registry.py:199) and the same name
    #      derive_routing_grammar() emits as the canonical (rail-first
    #      collapse — the grammar-derivation module's own docstring names
    #      create_reminder explicitly as a case it must NOT entry_point-
    #      collapse with the todo READ keys). So the allowlist key below is
    #      "create_reminder" — matches the registry canonical, not an alias.
    #   2. effect correct BY BEHAVIOR — handle_create_reminder
    #      (todo_handlers.py:530-656) extracts task text and a parsed time,
    #      then (line 624) calls
    #      `self.todo_service.create_todo(user_id=user_id, text=text,
    #      priority="medium", reminder_date=reminder_dt, due_date=reminder_dt)`
    #      — persists exactly one row and deletes nothing anywhere in the
    #      function (the two honest-ask early returns, missing task / missing
    #      time, persist nothing at all). WRITE, not DESTRUCTIVE, not READ.
    #      Read from the handler body, not this docstring or #1560's.
    #   3. reaches consent — needs_consent derives True (WRITE >= WRITE) and
    #      intent_service.py's rail block (process_intent, ~L2894-2937) awaits
    #      consent_gate.evaluate_consent with THIS entry's effect +
    #      outwardness before dispatch. That block is entry-agnostic — it
    #      reads `_rail_entry.needs_consent`/`.effect`/`.outwardness` off
    #      whichever entry `intent.action` resolved to, so it already ran
    #      identically for create_reminder before this change (#1560
    #      registered it on the rail in the first place); the create_todo spy
    #      in test_inversion_write_allowlist_1677.py exercises the SAME code
    #      path under the flip and is mirrored here for create_reminder in
    #      test_inversion_write_allowlist_create_reminder_1559.py.
    # No flip_group: create_reminder carries registry category EXECUTION, so
    # (as with create_todo) flipping that category sweeps this write in too
    # — the allowlist bounds which writes, never which surface.
    create_reminder_entry = WorkflowEntry(
        entry_point=run_todo_query_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Create-reminder via action dispatch (#1560)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_write_allowlist_key="create_reminder",
    )

    # #1685: create_todo onto the rail — #1666's exact gap on the CREATE side,
    # found by Arch (2026-08-25) while checking a claim rather than trusting
    # it. create_todo was absent from this dict entirely, so
    # `intent.action in _action_workflows` was FALSE at the #1124 rail check:
    # it fell to the legacy `elif mapped_action == "create_todo"` and reached
    # todo_handlers.handle_create_todo, which makes ZERO consent_gate calls.
    # That is not "a WRITE the matrix correctly waves through" — it is
    # UNREGISTERED: not covered because nothing evaluated it. The elif is
    # REMOVED in the same commit (migration completion, #1411/#1666
    # precedent); run_create_todo_workflow carries its exact body.
    # effect: WRITE — handle_create_todo persists a row via
    # todo_service.create_todo (todo_handlers.py ~L368). Additive and
    # recoverable (the user can delete the todo they just made), so WRITE,
    # never DESTRUCTIVE — the same derivation the create_reminder sibling
    # (#1560) carries for the same call into the same service.
    # outwardness: PRIVATE (#1509 axis) — a todo row on the user's own list;
    # no communication act, nobody else witnesses it (the ratified worked
    # example of a private write).
    # Consequence, stated so it is never inferred: needs_consent derives True
    # (WRITE >= WRITE), so the gate now RUNS on create turns. It does not add
    # ceremony to them — PRIVATE x WRITE x execute framing is PROCEED, and
    # "add/create a todo …" is verb-initial imperative, which
    # classify_framing reads as EXECUTE. Evaluation, not ask.
    # #1677 note: this registration is also the prerequisite for the
    # individually-flipped-WRITE option there — flip-1 selects which ROUTER
    # feeds this rail, and an unregistered op never reaches the rail at all.
    # #1677 (PM chose option (d), 2026-08-28): the FIRST and only named WRITE
    # the inversion flip may route. Not a flip_group — no wave sweeps a write
    # in; it flips only when a flag token names it (`create_todo`) or names
    # its registry category (`EXECUTION`). Arch's three conditions were
    # RE-RUN on 2026-08-28, not cited from the 08-25 ruling:
    #   1. registered — get_action_workflows()["create_todo"] exists,
    #      action_triggered=True (this entry, landed by #1685);
    #   2. effect correct BY BEHAVIOR — todo_handlers.handle_create_todo
    #      (~L350) calls todo_service.create_todo(user_id, text, priority),
    #      which persists one row and deletes nothing: WRITE, not
    #      DESTRUCTIVE, not READ. Read from the handler body, not this
    #      docstring or #1685's;
    #   3. reaches consent — needs_consent derives True (WRITE >= WRITE) and
    #      intent_service.py's rail block awaits consent_gate.evaluate_consent
    #      with THIS entry's effect + outwardness before dispatching
    #      (asserted at that seam by test_create_todo_rail_1685.py's spy, and
    #      re-asserted under the flip in test_inversion_write_allowlist_1677).
    # Why the flip is the fix for #1677: the misroute is the LLM classifier
    # drawing create_ticket for "add todo …" (1/3–2/3 of samples). The
    # inversion's constrained router picks from the derived grammar instead,
    # so the todo-create shape stops depending on that draw.
    create_todo_entry = WorkflowEntry(
        entry_point=run_create_todo_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Create-todo via action dispatch (#1685)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_write_allowlist_key="create_todo",
    )

    # #1666: delete_todo onto the rail — the consent-gate coverage gap Arch
    # found during the #1663 investigation. Unregistered, delete_todo never
    # reached the #1124 rail check, fell to the legacy elif chain, and
    # DELETED IMMEDIATELY with no confirm — while its DESTRUCTIVE tier was
    # implicitly assumed enforced (#1663's own worked example). The elif is
    # REMOVED in the same commit (migration completion, #1411 precedent) —
    # this entry point carries its exact body (run_delete_todo_workflow:
    # principal coercion, the #1605 clear-family seam, handle_delete_todo).
    # effect: DESTRUCTIVE — todo_handlers.handle_delete_todo calls
    # todo_service.delete_todo: the row is GONE, no recovery path, and the
    # blast radius is the user's own data destroyed on a misparse (the
    # position-based "todo N" resolution makes silent wrong-target deletion
    # a real failure mode — exactly what confirming WHAT protects against).
    # needs_confirm derives True → the #1190 gate arms at the rail via the
    # ASYNC delete-todo builder (destructive_confirm.build_todo_delete_
    # confirmation), which binds the real todo text into the ask.
    # outwardness: PRIVATE (#1509 axis) — the user's own todo list; deleting
    # a row is not a communication act (same settled boundary reasoning as
    # close/reopen: the effect axis already covers everything worth fearing).
    #
    # #1595 unit 3b (2026-09-25, for #1606): the FIRST DESTRUCTIVE entry on
    # the #1677 named-write allowlist — Arch's Q1 floor ruling, 2026-09-25:
    # "#1677's 'WRITE' was never a categorical ceiling — extend the
    # allowlist to a DESTRUCTIVE op, individually verified, same as
    # create_todo/create_reminder were." This is the operation the LIVE
    # constrained router actually draws for #1606's corpus phrasing
    # ("please clear the reminders except for 'Review the PR'" →
    # `delete_todo` @0.9; "delete my hydrate reminder" → `delete_todo` @0.9
    # — 2026-09-25 shadow score) — the corpus row this unit closes. Arch's
    # three conditions RE-RUN today, not cited from #1666's ruling:
    #   1. registered — get_action_workflows()["delete_todo"] exists,
    #      action_triggered=True (this entry). Alias family enumerated from
    #      ActionMapper (action_mapper.py:98-107): delete_todo / remove_todo
    #      / cancel_todo / delete_reminder / remove_reminder /
    #      cancel_reminder, all canonicalizing to "delete_todo" — the same
    #      name ACTION_REGISTRY files it under (EXECUTION,
    #      action_registry.py:202/390) and derive_routing_grammar() emits
    #      as canonical. The allowlist key below is "delete_todo" — matches
    #      the registry canonical, not an alias.
    #   2. effect correct BY BEHAVIOR — todo_handlers.handle_delete_todo
    #      calls `self.todo_service.delete_todo(todo_id=…, user_id=…)` on
    #      BOTH its confirmed-binding leg (todo_handlers.py ~L964) and its
    #      legacy positional leg (~L1002): the row is GONE, no recovery
    #      path anywhere in the function. DESTRUCTIVE, never WRITE or READ.
    #   3. reaches consent AND confirm — needs_consent derives True
    #      (DESTRUCTIVE >= WRITE) and needs_confirm ALSO derives True
    #      (== DESTRUCTIVE); the SAME entry-agnostic #1190 gate
    #      (intent_service.py process_intent, ~L2900-2990) evaluates it and
    #      builds the confirm via build_todo_delete_confirmation, whichever
    #      router produced the Intent — inversion_live.consult_inversion_
    #      live REPLACES the classifier draw for the turn (one `intent`
    #      variable flows into this same rail block), it never opens a
    #      second dispatch path.
    #   Arch's ONE ADDITIONAL build-time condition for a DESTRUCTIVE flip
    #      (not asked of create_todo/create_reminder, both WRITE): confirm
    #      that the rendered confirm prompt pulls its identifying detail
    #      from the SAME slot-extraction path the legacy dispatch uses —
    #      not a differently-shaped inversion-specific confirm that could
    #      drop the identifying detail the user needs to catch a misparse.
    #      build_todo_delete_confirmation reads `intent.context.get(
    #      "original_message")` or falls back to `intent.original_message`
    #      (destructive_confirm.py ~L508-512) — both the legacy classifier
    #      and consult_inversion_live set `original_message=message` (the
    #      raw user text) on the Intent they return, so the SAME title-
    #      resolution (_named_delete_target → resolve_named_todo_target
    #      against the owner-scoped list) runs regardless of provenance.
    #      Proven, not assumed: two tests with the SAME assertion and
    #      DIFFERENT Intent provenance (legacy-classified vs.
    #      inversion-consulted), comparing the rendered confirm strings for
    #      equality — tests/…/test_inversion_write_allowlist_delete_todo_
    #      1606.py, TestConfirmProvenanceParity.
    # No flip_group: delete_todo carries registry category EXECUTION, so
    # (as with create_todo/create_reminder) flipping that category sweeps
    # this write in too — the allowlist bounds which writes, never which
    # surface.
    delete_todo_entry = WorkflowEntry(
        entry_point=run_delete_todo_workflow,
        effect=EffectClass.DESTRUCTIVE,
        outwardness=Outwardness.PRIVATE,
        # Router-facing (the catalog is derived from this text, 2026-10-01):
        # "clear / delete / remove / cancel" todos or reminders — one, several,
        # or all-except-named ones. Without the verbs named, the Haiku-class
        # router read "clear the reminders except X" as a LISTING 3/3.
        description=(
            "Delete, clear, remove or cancel todos or reminders — one by name, several, "
            "or all except the ones named; a destructive ask, never a listing (#1666)"
        ),
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_write_allowlist_key="delete_todo",
    )

    # #1595 Phase 3 (2026-10-04, for Arch's 2026-10-03 ruling §4): complete_todo
    # onto the rail — the op was EXECUTION/COMPLETE with NO entry (Arch's
    # memo), so it never reached the #1124 rail or the #1509 consent check at
    # all; it fell straight to the ``elif mapped_action == "complete_todo"``
    # chain, ungated. The elif is REMOVED in the same commit (migration
    # completion, #1666/#1685 precedent) — this entry point carries its exact
    # body (run_complete_todo_workflow: principal coercion, the #1605
    # clear-family seam with candidate effect WRITE, handle_complete_todo).
    #
    # effect: WRITE, never DESTRUCTIVE — Arch's handler-read test (§4):
    # "if completing removes the item from the active list irrecoverably,
    # it's DESTRUCTIVE... if it's a reversible status flip, it's WRITE."
    # ``todo_handlers.handle_complete_todo`` (todo_handlers.py:1102) calls
    # ``self.todo_service.complete_todo(todo_id=…, user_id=…)`` —
    # ``TodoManagementService.complete_todo`` (todo_management_service.py:240)
    # → ``TodoRepository.complete_todo`` (todo_repository.py:330-354), which
    # sets ``status=COMPLETED``, ``completed=True``, ``completed_at=now()`` —
    # an UPDATE on the existing row, nothing deleted. The row stays selectable
    # by ``list_todos(include_completed=True)`` (the ``list_completed_todos``
    # action, action_mapper.py:85) and ``TodoRepository.reopen_todo``
    # (todo_repository.py:356-378) / ``TodoManagementService.reopen_todo``
    # (todo_management_service.py:272) reverse every one of those same three
    # fields back to pending. Reversible status flip → WRITE.
    # ⚠️ Noted, not blocking: ``reopen_todo`` exists at the service/repo layer
    # but is NOT wired to any chat action today (no "reopen_todo" hit anywhere
    # in services/intent_service/ or services/intent/ — grep-verified) — a
    # user cannot currently say "reopen todo 3" and have it fire. That is a
    # chat-affordance gap, not a handler-behavior question: Arch's test asks
    # what completing DOES to the row (a status flip vs. a deletion), not
    # whether a reopen command is exposed, and the data-layer answer is
    # unambiguous. Separate discovered-work candidate, not this unit's scope.
    # needs_consent derives True (WRITE) → the SAME entry-agnostic rail block
    # create_todo/create_reminder/delete_todo use (intent_service.py
    # _dispatch_action_rail, ~L15901-15916) evaluates it via
    # consent_gate.evaluate_consent (PRIVATE x WRITE x execute framing =
    # PROCEED — every natural completion phrasing is verb-initial imperative).
    # outwardness: PRIVATE (#1509 axis) — the user's own todo list; completing
    # a row is not a communication act (same boundary reasoning as
    # create_todo/delete_todo).
    # No flip_group — complete_todo carries registry category EXECUTION
    # (action_registry.py:210), so (as with create_todo/create_reminder/
    # delete_todo) flipping that category would sweep this write in too; this
    # unit does NOT flip it (no live-category change, no flag/env edit) —
    # only the allowlist entry below exists so a future flip of EXECUTION
    # wave is representable, per #1677's structural-not-config framing.
    #
    # #1677 named-WRITE allowlist, all three conditions RE-RUN today (not
    # cited from create_todo's/delete_todo's ruling):
    #   1. registered — get_action_workflows()["complete_todo"] exists,
    #      action_triggered=True (this entry). Alias family (ActionMapper,
    #      action_mapper.py:93-96): complete_todo / finish_todo /
    #      mark_complete / mark_done, all canonicalizing to "complete_todo" —
    #      the same name ACTION_REGISTRY files it under (EXECUTION,
    #      action_registry.py:210/437). The allowlist key below is
    #      "complete_todo" — the registry canonical, not an alias.
    #   2. effect correct BY BEHAVIOR — see the WRITE paragraph above; read
    #      from todo_handlers.py / todo_management_service.py /
    #      todo_repository.py, not from a docstring or a prior reviewer.
    #   3. reaches consent — needs_consent derives True (WRITE) and the
    #      rail's consent block actually evaluates it (see above); WRITE
    #      never derives needs_confirm (== DESTRUCTIVE only), so this entry
    #      takes no #1190 confirm arm — correct, nothing it does needs one.
    #
    # #1920 cross-family carrier-release note (inversion_live.py ~804-830):
    # complete_todo's registry category is EXECUTION — the SAME family as
    # "the reminder carriers" the cross-family release names explicitly in
    # its own docstring. A same-family write declines release
    # ("same_family_write" reason) exactly like delete_todo already does; an
    # armed reminder/todo carrier therefore still RE-ASKS rather than
    # releasing for a completion phrase. Registering this entry does not
    # change that outcome — before this commit the decline reason was
    # "not_rail_dispatchable" (no entry existed at all); after, it is
    # "same_family_write" — the carrier still never releases either way,
    # only the logged decline reason changes.
    complete_todo_entry = WorkflowEntry(
        entry_point=run_complete_todo_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description=(
            "Mark an existing todo or reminder as done — a reversible status flip "
            "(reopen reverses it), never a deletion (#1595 Phase 3)"
        ),
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        flip_write_allowlist_key="complete_todo",
    )

    # #1570: archived-projects LIST query (the #1560 pattern). Self-contained
    # entry point (needs only user_id — no intent/intent_service context), so
    # requires_context stays empty. See run_archived_projects_query_workflow's
    # docstring for the incident + moratorium disposition.
    # effect: READ — owner-scoped SELECT of archived project rows
    # (PortfolioService.list_archived_projects); no writes anywhere.
    archived_projects_entry = WorkflowEntry(
        entry_point=run_archived_projects_query_workflow,
        effect=EffectClass.READ,
        description="Archived-projects list query via action dispatch (#1570)",
        action_triggered=True,
        # flip_group (#1667): read_status — an owner-scoped listing, and one of
        # the ops #1667 names as having no ACTION_REGISTRY category (so before
        # this field it was unaddressable by every possible flag value).
        flip_group="read_status",
    )

    # #1624: chat summarize of an uploaded document — the #1187-deferred
    # `document` branch, finished by pointing chat at the SAME code path the
    # REST endpoint uses (document_handlers.handle_summarize_document →
    # DocumentAnalyzer). See run_summarize_document_workflow's docstring for
    # the 15-month forensics trace + the honesty contract.
    # effect: READ — owner-scoped SELECT of the uploaded-file row + a
    # read-only DocumentAnalyzer.analyze over its stored bytes; no row is
    # written anywhere on the path (document_handlers.py:67-110, 179-224).
    # outwardness: PRIVATE (#1509 axis) — a summary rendered back to the
    # asking user in their own chat; no communication act, nobody else
    # witnesses it (declared explicitly even though READ defaults PRIVATE,
    # per the #1624 build directive).
    summarize_document_entry = WorkflowEntry(
        entry_point=run_summarize_document_workflow,
        effect=EffectClass.READ,
        outwardness=Outwardness.PRIVATE,
        description=(
            "Summarize a document the user uploaded (resolves 'the document' "
            "to their file, then the same DocumentAnalyzer path as the REST "
            "summarize endpoint)"
        ),
        requires_context=["intent"],
        action_triggered=True,
        # flip_group (#1667): read_synthesis — THE summarize family, and
        # currently its only member. PA's issue/commit summarize shapes (the
        # 08-18 crack: they still ride the floor with no operation) join this
        # group when they are built, which is exactly the kickoff's §2.2 item 3.
        # The group deliberately stays the summarize family and nothing else:
        # generate_content / strategic_planning also emit prose and are NOT
        # here, because "generates prose" is not the property being flipped.
        flip_group="read_synthesis",
    )

    # RECONNECT #1327 build #2: conversational "what's my default repo" — the read
    # counterpart. Same 2-arg (intent, workflow_id) factory + action-dispatch rail.
    # effect: READ — _handle_get_default_repo reads the same preference key the
    # set handler writes; its own docstring names it "the READ counterpart".
    get_default_repo_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_get_default_repo"),
        effect=EffectClass.READ,
        description="Get-default-repo via action dispatch (#1327)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
        # flip_group (#1667): read_status — the IDENTITY half of the wave-1
        # class ("what's my default repo?"): reading back the user's own stored
        # setting. Its WRITE counterpart (set_default_repo, right above) can
        # never carry a group — __post_init__ rejects it — which is the pairing
        # that makes the READ-only invariant concrete rather than nominal.
        flip_group="read_status",
    )

    # #1876: conversational "set my timezone to Helsinki" — UserPreferenceManager
    # .set_reminder_timezone (#1574's store) had ZERO callers anywhere (no Settings
    # page, no API route, no chat action), so every clock face (#1576) rendered on
    # DEFAULT_USER_TIMEZONE for everyone. This is the chat-action leg; the Settings
    # page + PUT /api/v1/preferences/timezone are the other two.
    # effect: WRITE — _handle_set_timezone persists via
    # UserPreferenceManager.set_reminder_timezone (write-through to
    # users.preferences["upm"], #1574). Additive/recoverable (the user can
    # re-set it any time), never DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — a reminder-timezone preference is the
    # user's own setting; nobody else is handed anything, same derivation as
    # set_default_repo (#1327) directly above.
    set_timezone_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_set_timezone"),
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Set-timezone via action dispatch (#1876)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1333 (Arch-ruled 2026-06-30): the former per-action unwired-write registration
    # (a hand-maintained `UNWIRED_WRITE_ACTIONS` list fanned onto the rail) is RETIRED.
    # The honest-decline is now DERIVED by construction: any unwired EXECUTION action
    # reaches `_handle_execution_intent`'s else-branch, which deterministically declines
    # and never routes to the floor (#1331 confabulation vector). No list to maintain →
    # no drift surface (a novel unwired action declines automatically). Curated decline
    # COPY still lives in `unwired_writes.UNWIRED_WRITE_DECLINES`; the trigger is derived.
    _default_entries: dict[str, WorkflowEntry] = {
        # effect: READ — despite the "Schedule a Meeting" name, this workflow
        # only runs a slot-filling CONVERSATION: start_meeting_workflow calls
        # manager.start_filling, and _complete_session (slot_filling_manager)
        # returns the filled slots with a "done" message — no calendar event or
        # any other durable write is created anywhere on the path (verified
        # 2026-08-09; grep for schedule_meeting consumers finds only lens
        # inference). ⚠️ If a real calendar write ever lands at completion,
        # this entry MUST flip to WRITE in the same commit.
        "meeting": WorkflowEntry(
            entry_point=start_meeting_workflow,
            effect=EffectClass.READ,
            description="Meeting scheduling via slot-filling",
            requires_context=["trigger_message"],
        ),
        # #1190: the confirmed-deferred-action executor. Offer-acceptance
        # ONLY (action_triggered=False — the classifier/rail can never emit
        # it; an accidental key/action collision must not fire a deferred
        # write). effect: DESTRUCTIVE — the CEILING of what dispatching it
        # can perform: it executes the deferred action with its stored
        # parameters. #1509 reuses this same carrier + entry for accepted
        # WRITE-tier consent checks (deliberately — one acceptance path, no
        # parallel gate), so the deferred action may be WRITE or DESTRUCTIVE;
        # the declaration stays at the ceiling per the ordered-enum contract.
        # It is not itself consent/confirm-gated: the gate lives at the rail
        # seam, which this entry is structurally excluded from, and the
        # consent/confirmation turn HAS already happened when this dispatches.
        # outwardness: PRIVATE (#1509 axis) — a carrier, not an action: the
        # deferred action's OWN entry carries its outwardness, and the
        # consent/disclosure turn has already happened at the rail seam when
        # this dispatches (structurally excluded from the rail, like its
        # effect note above).
        "confirm_pending_action": WorkflowEntry(
            entry_point=run_confirm_pending_action_workflow,
            effect=EffectClass.DESTRUCTIVE,
            outwardness=Outwardness.PRIVATE,
            description="Execute a confirmed pending destructive action (#1190)",
            requires_context=["pending_action", "intent_service"],
        ),
        # #1510 (inferred half, PM ruling via Exec 2026-08-13): store a
        # user-verified inference on the read-back's accepted turn.
        # Offer-acceptance ONLY (action_triggered=False — the classifier/rail
        # can never emit it). effect: WRITE (explicit + defaultless per
        # #1557/Arch 2026-08-09) — acceptance writes the verified value into
        # users.preferences JSONB (the set_default_repo precedent: a durable
        # per-user preference write, mutating but not destructive).
        # outwardness: PRIVATE (#1509 axis) — writes the user's own
        # verified-inference store; no communication act.
        "verify_inference": WorkflowEntry(
            entry_point=run_verify_inference_workflow,
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            description="Store a user-verified inference (#1510 read-back acceptance)",
            requires_context=["pending_action"],
        ),
        # #1591: accepted standup-interview invitation → start the EXISTING
        # #585 interview. Offer-acceptance ONLY (action_triggered=False — the
        # deterministic claim + interview token already route classified
        # standup intents; an accidental action collision must not start a
        # conversation). effect: WRITE (explicit + defaultless per #1557,
        # classified by READING the handler: _start_standup_conversation →
        # StandupConversationHandler.start_conversation → manager
        # .create_conversation → repo.add — a durable conversation row is
        # created; mutating, not destructive).
        # outwardness: PRIVATE (#1509 axis) — creates the user's own
        # conversation row; nothing lands in front of anyone else.
        "standup_interview": WorkflowEntry(
            entry_point=run_standup_interview_workflow,
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            description="Start the #585 standup interview from an accepted invitation (#1591)",
            requires_context=["pending_action", "intent_service"],
        ),
        # #1651: accepted standup closing offer → complete the BOUND
        # overdue todo. Offer-acceptance ONLY (action_triggered=False — the
        # classifier/rail can never emit it; an accidental action collision
        # must not fire a deferred write). effect: WRITE (explicit +
        # defaultless per #1557, classified by READING the handler:
        # TodoManagementService.complete_todo flips the row's completed flag —
        # mutating, recoverable, not destructive; the #1605 batch-complete
        # precedent). The acceptance turn dispatches on the todo id BOUND at
        # offer time — never a re-parse of the user's phrasing (the #1651
        # failure mode was title-matching 'overdue').
        # outwardness: PRIVATE (#1509 axis) — completes the user's own todo
        # row; no communication act.
        "standup_complete_todo": WorkflowEntry(
            entry_point=run_standup_complete_todo_workflow,
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            description="Complete the bound overdue todo from an accepted standup offer (#1651)",
            requires_context=["pending_action", "intent_service"],
        ),
        # #1605: reminder-clear verb disambiguation (CXO/PPM joint design,
        # signed off 2026-08-13). Three offer-seam-only entries (all
        # action_triggered=False — the classifier/rail can never emit them;
        # the #1190/verify_inference pattern).
        # effect: READ — a bare "yes" against the variant-1 either/or
        # question re-asks and re-arms the offer; nothing is written on this
        # path (the writes happen on an ANSWERED turn, handled kind-
        # specifically at the offer seam).
        "clarify_reminder_clear_verb": WorkflowEntry(
            entry_point=run_clarify_reminder_clear_verb_workflow,
            effect=EffectClass.READ,
            description="Re-ask the #1605 clear-verb either/or on a bare affirmative",
            requires_context=["pending_action", "intent_service"],
        ),
        # effect: READ — a bare "yes" after the variant-2 disclosure points
        # at the working correction phrase and re-arms the window; no write.
        "reminder_clear_correction": WorkflowEntry(
            entry_point=run_reminder_clear_correction_workflow,
            effect=EffectClass.READ,
            description="Hold the #1605 variant-2 correction window on a bare affirmative",
            requires_context=["pending_action", "intent_service"],
        ),
        # effect: DESTRUCTIVE (explicit + defaultless per #1557) — deletes
        # the todo rows resolved at offer time, by id, owner-scoped (#1532).
        # Reachable ONLY via run_confirm_pending_action_workflow's re-dispatch
        # of an explicitly-confirmed "yes" (the REAL #1190 gate) — the stored
        # 'clear'=delete preference changes the MAPPING, never the consent
        # tier (consent matrix: DESTRUCTIVE -> CONFIRM in every cell).
        # outwardness: PRIVATE (#1509 axis) — deletes the user's own
        # reminder/task rows; no communication act.
        "clear_reminders_delete": WorkflowEntry(
            entry_point=run_clear_reminders_delete_workflow,
            effect=EffectClass.DESTRUCTIVE,
            outwardness=Outwardness.PRIVATE,
            description="Execute a #1190-confirmed #1605 batch reminder/todo delete",
            requires_context=["intent", "intent_service"],
        ),
        # #1906: the "which one do you mean?" clarify (the named-target
        # UNMATCHED branch) — previously the one unarmed ask in this module.
        # Offer-seam-only (action_triggered=False — the classifier/rail can
        # never emit it). effect: READ — a bare "yes" against "tell me
        # which one you mean" re-asks and re-arms; the REAL bind + act
        # happens on an ANSWERED turn (ordinal / name / status word),
        # handled kind-specifically at the offer seam
        # (reminder_clear._handle_pick_target_turn), which re-enters the
        # SAME post-resolution flow a single matched name would have taken.
        "reminder_clear_pick_target": WorkflowEntry(
            entry_point=run_reminder_clear_pick_target_workflow,
            effect=EffectClass.READ,
            description="Re-ask the #1906 which-one-do-you-mean clarify on a bare affirmative",
            requires_context=["pending_action", "intent_service"],
        ),
        # #1648: offer-seam-only landing for the reminder time question (the
        # carrier armed by handle_create_reminder's honest time-clarify ask).
        # effect: READ — a bare "yes" against "when should I remind you?"
        # re-asks and re-arms; the REAL write happens on an ANSWERED turn,
        # handled kind-specifically at the offer seam
        # (todo_handlers.handle_reminder_time_turn). action_triggered=False:
        # the classifier/rail can never emit it (the #1605 clarify precedent).
        "clarify_reminder_time": WorkflowEntry(
            entry_point=run_clarify_reminder_time_workflow,
            effect=EffectClass.READ,
            description="Re-ask the #1648 reminder time question on a bare affirmative",
            requires_context=["pending_action", "intent_service"],
        ),
        # #1654: offer-seam-only landing for the reminder TASK question (the
        # carrier armed by handle_create_reminder's honest no-task clarify —
        # #1648's class one question earlier). effect: READ — a bare "yes"
        # against "what should I remind you about?" re-asks and re-arms; the
        # REAL write happens on an ANSWERED turn, handled kind-specifically
        # at the offer seam (todo_handlers.handle_reminder_task_turn).
        # action_triggered=False: the classifier/rail can never emit it (the
        # #1605/#1648 clarify precedent).
        "clarify_reminder_task": WorkflowEntry(
            entry_point=run_clarify_reminder_task_workflow,
            effect=EffectClass.READ,
            description="Re-ask the #1654 reminder task question on a bare affirmative",
            requires_context=["pending_action", "intent_service"],
        ),
        "update_document": document_update_entry,
        "edit_document": document_update_entry,
        "update_document_query": document_update_entry,
        "changes_query": changes_query_entry,
        "what_changed": changes_query_entry,
        "show_changes": changes_query_entry,
        "changes_since": changes_query_entry,
        # #1595 Phase 3 (Arch's 2026-10-01 ruling): get_current_time via
        # action dispatch, flip_group read_temporal. No alias family — the
        # pre-classifier's TEMPORAL_PATTERNS list and the LLM classifier both
        # emit this exact action name (action_registry.py ACTION_EXAMPLES).
        "get_current_time": get_current_time_entry,
        # read_floor (#1595 Phase 3): FLOOR ops the rail now reaches, explicit membership.
        **_read_floor_entries(),
        # read_floor_2 (#1595 Phase 3 wave 2): a SECOND, separate group of FLOOR
        # rail adapters — not a widening of read_floor, which is already live.
        **_read_floor_2_entries(),
        # read_canonical (#1595 Phase 3, Arch's ruling 2026-10-03 section 3):
        # READ rail adapters for two CANONICAL-disposition ops that mutate
        # nothing — explain_suggestion, get_contextual_guidance.
        **_read_canonical_entries(),
        # read_portfolio (#1595 Phase 3, Arch's ruling 2026-10-03 section 2;
        # widened 2026-10-04 ruling section 1): the LIST half of
        # manage_repos (list_repos) PLUS the READ fourth of
        # manage_portfolio's own split (search_projects) — two READ rail
        # adapters sharing one flip_group, wrapping
        # CanonicalHandlers._handle_list_repos /
        # _handle_search_projects respectively. manage_repos's link/unlink
        # are separate WRITE/DESTRUCTIVE tasks, not registered here.
        "list_repos": list_repos_entry,
        "search_projects": search_projects_entry,
        # #1595 Phase 3 (Arch's ruling 2026-10-04 section 2): the WRITE
        # thirds of manage_portfolio's split — archive_project /
        # restore_project / add_project. `list_projects` (the ACTIVE-list
        # READ) is deliberately NOT re-homed here — Arch's 2026-10-04
        # ruling §1 keeps it on the EXISTING QUERY-category rail key (see
        # the module comment directly above archive_project_entry's
        # definition); only `search_projects` (immediately above) is new.
        "archive_project": archive_project_entry,
        "restore_project": restore_project_entry,
        "add_project": add_project_entry,
        # #1124 step 3: issue-mutation cohort (aliases mirror the migrated elif branches).
        "close_issue": close_issue_entry,
        "close_issue_query": close_issue_entry,
        "reopen_issue": reopen_issue_entry,
        "reopen_issue_query": reopen_issue_entry,
        "comment_issue": comment_issue_entry,
        "add_comment": comment_issue_entry,
        "comment_issue_query": comment_issue_entry,
        # #1411: update_issue + its action_mapper aliases (the raw names the classifier
        # emits: update_github_issue/update_ticket/modify_issue → update_issue).
        "update_issue": update_issue_entry,
        "update_github_issue": update_issue_entry,
        "update_ticket": update_issue_entry,
        "modify_issue": update_issue_entry,
        # #1412: create_issue + its 6 action_mapper aliases.
        "create_issue": create_issue_entry,
        "create_github_issue": create_issue_entry,
        "create_item": create_issue_entry,
        "create_ticket": create_issue_entry,
        "make_github_issue": create_issue_entry,
        "new_github_issue": create_issue_entry,
        # #1124 cohort 1: prioritization (strategy category).
        "prioritize": prioritization_entry,
        "set_priorities": prioritization_entry,
        # #1124: content generation (synthesis category).
        "generate_content": generate_content_entry,
        "create_content": generate_content_entry,
        # #1560: create_reminder + its ActionMapper raw-emission aliases
        # (set_reminder / add_reminder → create_reminder, #284/#1426). Canonical
        # key first: wired_chat_actions() names each unique entry by its
        # first-registered key.
        "create_reminder": create_reminder_entry,
        "set_reminder": create_reminder_entry,
        "add_reminder": create_reminder_entry,
        # #1685: create_todo + its ActionMapper raw-emission aliases
        # (add_todo / new_todo → create_todo, #284). Enumerated from
        # ACTION_MAPPING, not assumed to mirror the delete family's shape.
        # Canonical key first: wired_chat_actions() names each unique entry
        # by its first-registered key.
        "create_todo": create_todo_entry,
        "add_todo": create_todo_entry,
        "new_todo": create_todo_entry,
        # #1666: delete_todo + its ActionMapper raw-emission aliases
        # (remove_todo / cancel_todo → delete_todo, #284). Canonical key
        # first: wired_chat_actions() names each unique entry by its
        # first-registered key.
        "delete_todo": delete_todo_entry,
        "remove_todo": delete_todo_entry,
        "cancel_todo": delete_todo_entry,
        # 1527 (v70 live, 2026-09-08): the classifier's reminder-NOUN raw
        # emissions for the same delete ask. PM's "delete my hydrate reminder"
        # emitted EXECUTION/delete_reminder (3/3 live-classifier runs, conf
        # 0.9-0.95); unregistered, it fell past the rail to the #1333 generic
        # unwired-write decline — a false "still on the way" for a wired,
        # confirm-gated capability. Same alias discipline as the create
        # family's add_reminder (#1426: census-observed LLM emission).
        # destructive_confirm._DELETE_TODO_FAMILY carries the same three so
        # the title-bound confirm (not the generic offer) arms on this leg.
        "delete_reminder": delete_todo_entry,
        "remove_reminder": delete_todo_entry,
        "cancel_reminder": delete_todo_entry,
        # #1595 Phase 3: complete_todo + its ActionMapper raw-emission aliases
        # (finish_todo / mark_complete / mark_done → complete_todo,
        # action_mapper.py:93-96). Canonical key first: wired_chat_actions()
        # names each unique entry by its first-registered key.
        "complete_todo": complete_todo_entry,
        "finish_todo": complete_todo_entry,
        "mark_complete": complete_todo_entry,
        "mark_done": complete_todo_entry,
        # RECONNECT #1327 gap 1: set-default-repo (QUERY category, pre-classifier action).
        "set_default_repo": set_default_repo_entry,
        # RECONNECT #1327 build #2: get-default-repo (read counterpart).
        "get_default_repo": get_default_repo_entry,
        # #1876: set-timezone (QUERY category, pre-classifier reachable only via
        # the rail — no pre_classifier.py pattern; the LLM classifier's own
        # emission is the reachability path, per the 2026-08-29 corpus-deposit
        # ruling).
        "set_timezone": set_timezone_entry,
        # #1570: archived-projects list — canonical key first (wired_chat_actions
        # names each unique entry by its first-registered key), then the mode-4
        # defense aliases for LLM paraphrase emissions.
        "list_archived_projects": archived_projects_entry,
        "show_archived_projects": archived_projects_entry,
        "archived_projects_query": archived_projects_entry,
        "list_archived": archived_projects_entry,
        # #1624: uploaded-document summarize — canonical key first (it is the
        # registry canonical, the verb-shim target, AND classifier.py's
        # action-normalization target for bare `summarize` emissions), then
        # mode-4 defense aliases for LLM paraphrase emissions.
        "summarize_document": summarize_document_entry,
        "summarize_file": summarize_document_entry,
        "summarize_upload": summarize_document_entry,
        "summarize_uploaded_file": summarize_document_entry,
    }

    # #1124 step 3 cohort 2: GitHub read-query cohort — one shared entry point per
    # handler (built by the factory), fanned out to that handler's classifier aliases.
    # effect: READ for every handler in this cohort — each of the nine
    # (_handle_shipped_this_week / _handle_stale_prs / _handle_review_issue_query
    # / _handle_list_{issues,prs,milestones,releases,labels,branches}_query)
    # fetches GitHub data via the router and formats it; none contains a
    # mutating call (verified per-handler 2026-08-09). A handler that starts
    # writing must move OUT of this cohort and declare its own effect.
    # flip_group (#1667): per-handler, from _READ_QUERY_FLIP_GROUPS above —
    # eight listings in read_status, review_issue in read_referent. A handler
    # this cohort gains later with no entry in that map registers UNGROUPED
    # (safe direction: no wave flip can address it; `--audit` names it).
    for handler_attr, aliases in _READ_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(
                handler_attr,
                # #1762 (epic 6): the six listing handlers take session_id so
                # a capped list can arm its remainder. See
                # _READ_QUERY_SESSION_THREADED above for why the other three
                # stay on the 2-arg shape.
                pass_session_id=handler_attr in _READ_QUERY_SESSION_THREADED,
            ),
            effect=EffectClass.READ,
            description=_READ_QUERY_DESCRIPTIONS.get(
                handler_attr, f"{handler_attr} via action dispatch (#1124)"
            ),
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group=_READ_QUERY_FLIP_GROUPS.get(handler_attr),
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 calendar cohort — 3-arg (intent, workflow_id, user_id), user-scoped factory.
    # effect: READ for all three calendar handlers — meeting_time /
    # recurring_meetings / week_calendar each analyze the user's calendar and
    # answer; no event creation or modification (verified per-handler 2026-08-09).
    # flip_group (#1667/#1595 wave 2, 2026-09-25): read_temporal for all three,
    # from _CALENDAR_QUERY_FLIP_GROUPS above — every calendar op answers over a
    # TIME WINDOW ("this week", "how much time", "recurring"), the paradigm
    # read_temporal case. Previously ungrouped (kickoff §2.2 put temporal last,
    # pending the #1572 clock work); #1887 (2026-09-24) gave the product one
    # timezone resolver, which is what changed.
    for handler_attr, aliases in _CALENDAR_QUERY_COHORT.items():
        description = _CALENDAR_QUERY_DESCRIPTIONS.get(
            handler_attr, f"{handler_attr} via action dispatch (#1124)"
        )
        entry = WorkflowEntry(
            entry_point=_make_user_scoped_query_dispatch_entry_point(handler_attr),
            effect=EffectClass.READ,
            description=description,
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group=_CALENDAR_QUERY_FLIP_GROUPS.get(handler_attr),
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 analysis cohort — standard factory; #1641: session_id threaded
    # (pass_session_id) so the repository ask can bind (see cohort comment).
    # effect: READ for all three analysis handlers — analyze_commits and
    # analyze_data read repo activity/metrics; generate_report (despite the
    # name) reads recent activity and returns the formatted report as the
    # response message, writing nowhere (verified per-handler 2026-08-09).
    # flip_group (#1667): read_referent for all three — this IS the analysis
    # family the kickoff names for wave 2, and the referent is real rather than
    # nominal: #1641 threads session_id through this cohort precisely so the
    # "which repository?" ask can bind. Flipping these is what exercises the
    # snapshot's referent fields against handlers that need one.
    for handler_attr, aliases in _ANALYSIS_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(handler_attr, pass_session_id=True),
            effect=EffectClass.READ,
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group="read_referent",
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 QUERY-category cohort — the remaining `_handle_query_intent` elif
    # handlers, reused unchanged, with per-handler arity threaded via the factory
    # flags (session_id and/or user_id). `todos` is special — it delegates to the
    # EXECUTION handler via run_todo_query_workflow. Aliases mirror the elif branches.
    def _qentry(entry_point, description, effect, flip_group=None):
        # `effect` is deliberately REQUIRED here too (no default): the helper
        # must not become the defaulted back door around WorkflowEntry's
        # defaultless field (Arch ruling 2026-08-09) — every call site below
        # declares what its handler does in the world, with evidence.
        # `flip_group` (#1667) mirrors WorkflowEntry's own default: optional,
        # None = unaddressable by any wave flip (the safe direction). Every
        # call site below states its assignment — or its non-assignment — with
        # the reasoning in the comment beside it.
        return WorkflowEntry(
            entry_point=entry_point,
            effect=effect,
            description=f"{description} (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
            flip_group=flip_group,
        )

    _query_cohort: list[tuple[WorkflowEntry, list[str]]] = [
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_local_git_status_query"),
                "local-git-status via action dispatch",
                # effect: READ — runs read-only local git status inspection.
                EffectClass.READ,
                # flip_group: read_status — "what's my local git status" is the
                # literal status class; no referent, no time expression.
                "read_status",
            ),
            ["local_git_status_query", "local_git_status"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_search_documents_notion", pass_session_id=True
                ),
                "search-documents (Notion) via action dispatch",
                # effect: READ — Notion search only; no page mutation calls.
                EffectClass.READ,
                # flip_group: read_status — BORDERLINE, called listing. A search
                # returns a LIST of hits for a query string; it resolves no
                # referent (nothing is "the document" yet) and parses no time
                # expression, so it sits in the zero-armed-state listing class
                # rather than read_referent. The one wave-1 op whose data source
                # is a connector rather than GitHub/local state; if the Notion
                # connector's absence turns out to change the failure shape, this
                # is the assignment to revisit first.
                "read_status",
            ),
            ["search_documents", "find_documents", "search_notion"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_productivity_query", pass_session_id=True
                ),
                "productivity query via action dispatch",
                # effect: READ — aggregates activity metrics; no writes.
                EffectClass.READ,
                # flip_group: read_referent — BORDERLINE. It reads like a status
                # query ("how productive was I this week?") but it is built as an
                # ANALYSIS: same _make_query_dispatch_entry_point(pass_session_id)
                # shape as the analysis cohort, same repo-scoped aggregation, and
                # the live LLM's own paraphrase for it is `analyze_productivity`.
                # Grouped with the analyses it behaves like, not the listings it
                # sounds like.
                "read_referent",
            ),
            # #1283 probe (2026-07-08): the registry CANONICAL was missing from its
            # own handler's alias list (mode-2), and the live LLM emitted
            # analyze_productivity past all four aliases (mode-4).
            [
                "productivity",
                "my_productivity",
                "weekly_metrics",
                "accomplishments",
                "productivity_query",
                "analyze_productivity",
            ],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_session_activity_query", pass_session_id=True
                ),
                # #1595 D1 (Arch/CXO/PPM 2026-10-03): the handler is owner- AND
                # this-session-scoped by construction (ADR-078 D3); the router
                # only knows that scope if the description says it. A
                # prior-session ask ("what did we discuss in our last session")
                # is MEMORY / the floor, never this op.
                "What was created or done in the CURRENT session only — 'what "
                "did we create this session', 'what did I work on today' — never "
                "earlier or previous sessions (#1394 / ADR-078 B4)",
                # effect: READ — recalls what this session created; pure read.
                EffectClass.READ,
                # flip_group: read_status — BORDERLINE, and the call turns on a
                # direction: this op READS OUT the session ledger the snapshot's
                # referent fields are built FROM. It consumes no referent of its
                # own ("what did we create this session?" names nothing), so it
                # is a listing of session state, not a referent resolution.
                "read_status",
            ),
            ["session_activity_query", "what_did_we_create", "session_recall"],
        ),
        (
            _qentry(
                # #1511: pass_session_id too — the interview-token branch inside
                # _handle_standup_query needs the session to key the interactive
                # flow; the report path still ignores it.
                _make_query_dispatch_entry_point(
                    "_handle_standup_query", pass_session_id=True, pass_user_id=True
                ),
                "standup query via action dispatch",
                # effect: READ — assembles standup summary from existing data;
                # the #1511 interview-token branch starts the existing guided
                # capture flow (same effect the /standup command already has).
                EffectClass.READ,
                # flip_group: read_status — the status op #1667 names first in
                # its own title. ⚠️ Note for the flip operator, not a reason to
                # withhold the group: the #1511 interview-token branch inside
                # this handler can START a guided capture. That is handler
                # behavior identical on both routing paths (the rail dispatches
                # the same key either way), and the consult never runs on an
                # ARMED turn at all — but it is why this op deserves live
                # telemetry attention before the rest of read_status.
                "read_status",
            ),
            ["show_standup", "get_standup"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_projects_query", pass_user_id=True),
                "projects query via action dispatch",
                # effect: READ — lists the user's projects; no writes.
                EffectClass.READ,
                # flip_group: read_status — a plain owner-scoped listing; the
                # second op named in #1667's coverage gap.
                "read_status",
            ),
            ["list_projects", "show_projects"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_attention_query", pass_session_id=True, pass_user_id=True
                ),
                # #1595 Phase 3 (2026-10-01, CXO/PPM ruling): this is the URGENCY
                # aggregate — what needs action soon — NOT an ownership listing.
                # The served router was taking "what's assigned to me" / "what am
                # I working on" here @0.85; those are floor questions (no op
                # computes "what I own"). The description now says what it is.
                "What needs my attention or action SOON — urgent, overdue, due "
                "today, blocked, at risk — ranked by urgency; NOT a listing of "
                "what is assigned to me, what I own, or what I am working on "
                "(#1595)",
                # effect: READ — surfaces items needing attention; pure read.
                EffectClass.READ,
                # flip_group: read_status — "what needs my attention?" is a
                # state summary over the user's own items; no referent, no
                # user-supplied window.
                "read_status",
            ),
            ["attention_query", "needs_attention", "what_needs_attention", "attention_items"],
        ),
        (
            _qentry(
                run_todo_query_workflow,
                "todo list/next query via action dispatch",
                # effect: READ — delegates to _handle_execution_intent, but the
                # ONLY actions registered on this entry (list_todos_query /
                # list_completed_todos / next_todo_query) map to list_todos /
                # next_todo — todo READS. The handler's write branches
                # (complete_todo / delete_todo / create_issue) are unreachable
                # from these rail keys; if a write alias is ever added here,
                # it needs its own entry with its own effect.
                EffectClass.READ,
                # flip_group: read_status — todo LIST/next reads. The same
                # caveat the effect note carries applies doubly here: a write
                # alias added to this entry would be both a mis-declared effect
                # AND a flippable write, which __post_init__ would then reject
                # at construction. The group is safe exactly as long as the
                # effect declaration is honest.
                "read_status",
            ),
            ["list_todos_query", "list_completed_todos", "next_todo_query"],
        ),
        # #1521: reminder LIST query — "what reminders do I have?" The
        # pre-classifier emits QUERY/list_reminders_query (canonical); the
        # extra aliases are mode-4 defense for LLM paraphrase emissions on
        # phrasings the pre-classifier doesn't claim. 4-arg handler
        # (intent, workflow_id, session_id, user_id) — session for logging
        # parity, user for the owner-scoped todo read.
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_list_reminders_query", pass_session_id=True, pass_user_id=True
                ),
                "reminder list query via action dispatch (#1521)",
                # effect: READ — owner-scoped reminder/todo read; no writes.
                EffectClass.READ,
                # flip_group: read_status — BORDERLINE against the kickoff's
                # "TEMPORAL/reminder parsing LAST" ordering (§2.2 item 4). That
                # ordering is about PARSING a time expression, which this op
                # does not do: it is an owner-scoped list read with no time
                # argument. It is also already flippable today via its registry
                # category (QUERY), so the group adds no reachability it didn't
                # have — it only lets a wave name it deliberately.
                "read_status",
            ),
            ["list_reminders_query", "list_reminders", "show_reminders", "get_reminders"],
        ),
    ]
    for entry, aliases in _query_cohort:
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 final if-heads — the last category-router if-heads (analysis / strategy /
    # learning), migrated onto the rail so every category router collapses to its
    # floor fallback. Handlers reused unchanged. analyze_document is 3-arg (session_id);
    # strategic_planning + learn_pattern are 2-arg.
    _final_ifheads: list[tuple[WorkflowEntry, list[str]]] = [
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_analyze_document_notion", pass_session_id=True
                ),
                "analyze-document (Notion) via action dispatch",
                # effect: READ — fetches and analyzes a Notion document; unlike
                # its update sibling, it never calls append_blocks/update_page.
                EffectClass.READ,
                # flip_group: read_referent — BORDERLINE against read_synthesis
                # (its output is generated prose about a document). Grouped by
                # what it must RESOLVE, not what it emits: "analyze that doc"
                # only means anything once a specific Notion page is bound, and
                # that binding is the referent machinery. read_synthesis stays
                # exactly the summarize family the decision named.
                "read_referent",
            ),
            ["analyze_document", "analyze_file"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_strategic_planning"),
                "strategic-planning via action dispatch",
                # effect: READ — despite "create_plan": _handle_strategic_planning
                # builds an in-memory plan dict (_create_issue_resolution_plan)
                # and returns it as the message; nothing is persisted.
                EffectClass.READ,
                # flip_group (#1667/#1595 wave 3, 2026-09-25): read_strategic.
                # Was deliberately ungrouped through wave 1 — planning was not
                # one of wave 1's three classes (status/listing/identity,
                # referent+analysis, summarize), and stretching one of those
                # groups to absorb it would have made the group name stop
                # meaning what it says. read_strategic is that reviewed
                # fourth class: a plan produced over the user's own material,
                # nothing written anywhere — effect re-confirmed READ before
                # grouping.
                "read_strategic",
            ),
            ["strategic_planning", "create_plan"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_learn_pattern"),
                "learn-pattern via action dispatch",
                # effect: READ — despite "learn": _handle_learn_pattern fetches
                # historical data and computes patterns in memory
                # (_learn_*_patterns are pure); no pattern store is written.
                EffectClass.READ,
                # flip_group (#1667/#1595 wave 3, 2026-09-25): read_strategic.
                # Was deliberately ungrouped through wave 1, same reasoning as
                # strategic_planning above: the LEARNING class was not a
                # wave-1 class, and it is an "analysis" only in the loose
                # sense — grouping it read_referent would have put a
                # no-referent op into the group whose whole purpose is
                # exercising referent resolution. It joins read_strategic now:
                # a pattern produced over the user's own material, nothing
                # written anywhere — effect re-confirmed READ before grouping.
                "read_strategic",
            ),
            ["learn_pattern", "detect_pattern"],
        ),
    ]
    for entry, aliases in _final_ifheads:
        for alias in aliases:
            _default_entries[alias] = entry

    # #1893: skip against the SAME dict register_workflow() raises on, read at
    # call time through the module — not through a name bound at import. Tests
    # patch `workflow_dispatcher.get_registered_workflows` to return {} while
    # this module may be imported lazily (the #1632 path); a name bound during
    # such a patch stayed the mock forever, "already" read as empty, and the
    # strict register_workflow raised on the second call. Ordering-dependent,
    # file-only failure; green in the full run by accident.
    already = _workflow_dispatcher.WORKFLOW_REGISTRY
    newly_registered: list[str] = []
    for workflow_type, entry in _default_entries.items():
        if workflow_type in already:
            continue
        register_workflow(workflow_type, entry)
        newly_registered.append(workflow_type)

    logger.info(
        "default_workflows_registered",
        count=len(newly_registered),
        registered=newly_registered,
        skipped_already_present=[k for k in _default_entries if k not in newly_registered],
    )
