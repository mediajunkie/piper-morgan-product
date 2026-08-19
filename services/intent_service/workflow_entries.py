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

from services.intent_service.reminder_clear import (
    run_clarify_reminder_clear_verb_workflow,
    run_clear_reminders_delete_workflow,
    run_reminder_clear_correction_workflow,
)
from services.intent_service.standup_todo_offer import (
    run_standup_complete_todo_workflow,
)
from services.intent_service.todo_handlers import (
    run_clarify_reminder_time_workflow,
)
from services.intent_service.workflow_dispatcher import (
    WorkflowEntry,
    get_registered_workflows,
    register_workflow,
)
from services.shared_types import EffectClass, Outwardness

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
    active_lens = ctx.get("active_lens")
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
        active_lens=active_lens,
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
                "active_lens": active_lens,
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
    result = await intent_service._start_standup_conversation(effective_user, session_id)
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
        logger.error(
            "archived_projects_query_failed", error=str(e), user_id=user_id
        )
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
        names = [p.name for p in projects[:5]]
        noun = "project" if len(projects) == 1 else "projects"
        message = f"You have {len(projects)} archived {noun}:\n\n" + "\n".join(
            f"- {name}" for name in names
        )
        if len(projects) > 5:
            message += f"\n\n...and {len(projects) - 5} more."
        message += '\n\nSay "restore <name>" to bring one back.'
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
        if ("issue" in msg_lower and _re.search(r"#?\d+", msg_lower)) or (
            "commit" in msg_lower
        ):
            return None  # issue/commit summarize that mis-landed here

    if not user_id:
        return _result(
            "I can summarize a document you've uploaded, but I need to know who "
            "you are first — try signing in.",
            reason="no_user_id",
        )

    # ── Resolve "the document" → file_id (owner-scoped) ───────────────────
    try:
        from types import SimpleNamespace

        from services.database.session_factory import AsyncSessionFactory
        from services.file_context.exceptions import AmbiguousFileReferenceError
        from services.file_context.file_resolver import FileResolver
        from services.repositories.file_repository import FileRepository

        # FileResolver reads intent.action + intent.context["original_message"];
        # hand it a detached view so intent.context is never mutated (the
        # process_intent convention).
        resolver_view = SimpleNamespace(
            action="summarize_document",
            context={"original_message": message},
        )

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
            f"Here's my summary of {summarized['filename']}:\n\n"
            f"{summarized['summary']}",
            extra={
                "file_id": summarized["file_id"],
                "filename": summarized["filename"],
                "summary_format": summarized["format"],
                "resolution_confidence": resolution_confidence,
            },
        )
    except Exception as e:  # silent-ok: error-logged with context and returns success=False — honest degrade, never fake success (#1425)
        logger.error(
            "summarize_document_workflow_failed", error=str(e), user_id=user_id
        )
        return _result(
            "I had trouble reading that document just now. You can try again "
            "in a moment.",
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
    changes_query_entry = WorkflowEntry(
        entry_point=run_changes_query_workflow,
        effect=EffectClass.READ,
        description="What-changed-since query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
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
    )

    # RECONNECT #1327 gap 1: conversational "set my default repo to owner/name".
    # 2-arg (intent, workflow_id) handler, reused via the standard factory. Routed
    # via the action-dispatch rail (action_triggered) — NOT a hand-coded elif branch.
    # effect: WRITE — _handle_set_default_repo persists the preference to the
    # DB: ConnectorConfigService(session).set_default_repo(user_id, full_name)
    # (~L4847). Overwritable, so WRITE not DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — writes the user's OWN preference
    # row; nobody else witnesses anything.
    set_default_repo_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_set_default_repo"),
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Set-default-repo via action dispatch (#1327)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
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
    # todo_service.create_todo (todo_handlers.py ~L229). Additive + recoverable
    # (a todo row the user can delete), so WRITE not DESTRUCTIVE.
    # outwardness: PRIVATE (#1509 axis) — a reminder/todo row is the ratified
    # example of a private write (the user's own list; no communication act).
    create_reminder_entry = WorkflowEntry(
        entry_point=run_todo_query_workflow,
        effect=EffectClass.WRITE,
        outwardness=Outwardness.PRIVATE,
        description="Create-reminder via action dispatch (#1560)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
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
    delete_todo_entry = WorkflowEntry(
        entry_point=run_delete_todo_workflow,
        effect=EffectClass.DESTRUCTIVE,
        outwardness=Outwardness.PRIVATE,
        description="Delete-todo via action dispatch (#1666)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
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
        "update_document": document_update_entry,
        "edit_document": document_update_entry,
        "update_document_query": document_update_entry,
        "changes_query": changes_query_entry,
        "what_changed": changes_query_entry,
        "show_changes": changes_query_entry,
        "changes_since": changes_query_entry,
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
        # #1666: delete_todo + its ActionMapper raw-emission aliases
        # (remove_todo / cancel_todo → delete_todo, #284). Canonical key
        # first: wired_chat_actions() names each unique entry by its
        # first-registered key.
        "delete_todo": delete_todo_entry,
        "remove_todo": delete_todo_entry,
        "cancel_todo": delete_todo_entry,
        # RECONNECT #1327 gap 1: set-default-repo (QUERY category, pre-classifier action).
        "set_default_repo": set_default_repo_entry,
        # RECONNECT #1327 build #2: get-default-repo (read counterpart).
        "get_default_repo": get_default_repo_entry,
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
    for handler_attr, aliases in _READ_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(handler_attr),
            effect=EffectClass.READ,
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 calendar cohort — 3-arg (intent, workflow_id, user_id), user-scoped factory.
    # effect: READ for all three calendar handlers — meeting_time /
    # recurring_meetings / week_calendar each analyze the user's calendar and
    # answer; no event creation or modification (verified per-handler 2026-08-09).
    for handler_attr, aliases in _CALENDAR_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_user_scoped_query_dispatch_entry_point(handler_attr),
            effect=EffectClass.READ,
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 analysis cohort — standard factory; #1641: session_id threaded
    # (pass_session_id) so the repository ask can bind (see cohort comment).
    # effect: READ for all three analysis handlers — analyze_commits and
    # analyze_data read repo activity/metrics; generate_report (despite the
    # name) reads recent activity and returns the formatted report as the
    # response message, writing nowhere (verified per-handler 2026-08-09).
    for handler_attr, aliases in _ANALYSIS_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(
                handler_attr, pass_session_id=True
            ),
            effect=EffectClass.READ,
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 QUERY-category cohort — the remaining `_handle_query_intent` elif
    # handlers, reused unchanged, with per-handler arity threaded via the factory
    # flags (session_id and/or user_id). `todos` is special — it delegates to the
    # EXECUTION handler via run_todo_query_workflow. Aliases mirror the elif branches.
    def _qentry(entry_point, description, effect):
        # `effect` is deliberately REQUIRED here too (no default): the helper
        # must not become the defaulted back door around WorkflowEntry's
        # defaultless field (Arch ruling 2026-08-09) — every call site below
        # declares what its handler does in the world, with evidence.
        return WorkflowEntry(
            entry_point=entry_point,
            effect=effect,
            description=f"{description} (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )

    _query_cohort: list[tuple[WorkflowEntry, list[str]]] = [
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_local_git_status_query"),
                "local-git-status via action dispatch",
                # effect: READ — runs read-only local git status inspection.
                EffectClass.READ,
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
                "session-activity recall (#1394 / ADR-078 B4) via action dispatch",
                # effect: READ — recalls what this session created; pure read.
                EffectClass.READ,
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
            ),
            ["show_standup", "get_standup"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_projects_query", pass_user_id=True),
                "projects query via action dispatch",
                # effect: READ — lists the user's projects; no writes.
                EffectClass.READ,
            ),
            ["list_projects", "show_projects"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_attention_query", pass_session_id=True, pass_user_id=True
                ),
                "attention query via action dispatch",
                # effect: READ — surfaces items needing attention; pure read.
                EffectClass.READ,
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
            ),
            ["learn_pattern", "detect_pattern"],
        ),
    ]
    for entry, aliases in _final_ifheads:
        for alias in aliases:
            _default_entries[alias] = entry

    already = get_registered_workflows()
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
