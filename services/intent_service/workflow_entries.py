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

from services.intent_service.workflow_dispatcher import (
    WorkflowEntry,
    get_registered_workflows,
    register_workflow,
)

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

    return await intent_service._handle_update_document_notion(
        intent, workflow_id, session_id
    )


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
    document_update_entry = WorkflowEntry(
        entry_point=run_update_document_workflow,
        description="Document update via slot-filling (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1124 cohort 1 migration #3: changes-query — dispatch migration. The four
    # classifier aliases (verified live as stable) share one entry point.
    changes_query_entry = WorkflowEntry(
        entry_point=run_changes_query_workflow,
        description="What-changed-since query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    _default_entries: dict[str, WorkflowEntry] = {
        "meeting": WorkflowEntry(
            entry_point=start_meeting_workflow,
            description="Meeting scheduling via slot-filling",
            requires_context=["trigger_message"],
        ),
        "update_document": document_update_entry,
        "edit_document": document_update_entry,
        "update_document_query": document_update_entry,
        "changes_query": changes_query_entry,
        "what_changed": changes_query_entry,
        "show_changes": changes_query_entry,
        "changes_since": changes_query_entry,
    }

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
