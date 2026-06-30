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
    """Action-dispatch entry point for close-issue queries (#1124 step 3, CLOSE)."""
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
    return await intent_service._handle_close_issue_query(intent, workflow_id)


async def run_reopen_issue_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Action-dispatch entry point for reopen-issue queries (#1124 step 3, REOPEN)."""
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
    return await intent_service._handle_reopen_issue_query(intent, workflow_id)


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
    """#1124: todo list/next queries (pre-classifier routes them as QUERY) delegate
    to the EXECUTION handler, which owns the todo handlers — mirrors the migrated
    elif exactly. The workflow object is no longer pre-created (#883/#1094), so None
    is passed (the elif passed the `workflow` param, which the handler reduced to
    `getattr(workflow, 'id', None)` anyway)."""
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


# handler_attr → classifier aliases (mirror the migrated elif branches exactly).
_READ_QUERY_COHORT: dict[str, list[str]] = {
    "_handle_shipped_this_week": [
        "shipped_this_week",
        "what_shipped",
        "show_closed_prs",
        "shipped_query",
    ],
    "_handle_stale_prs": ["stale_prs", "old_prs", "show_stale_prs", "stale_prs_query"],
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


# #1124 analysis cohort — the 2-arg `(intent, workflow_id)` ANALYSIS-category
# handlers (analyze_commits / generate_report / analyze_data), reused unchanged via
# the standard factory. NOT included: analyze_document (the if-head) — it is 3-arg
# (session_id) + Notion-coupled, deferred to its own bite. Aliases mirror the
# migrated elif branches exactly.
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

    # #1124 Phase 4 step 3: issue-mutation cohort (CLOSE / REOPEN / COMMENT verbs).
    # Each handler reused unchanged; all classifier aliases share one entry point.
    close_issue_entry = WorkflowEntry(
        entry_point=run_close_issue_workflow,
        description="Close-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    reopen_issue_entry = WorkflowEntry(
        entry_point=run_reopen_issue_workflow,
        description="Reopen-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )
    comment_issue_entry = WorkflowEntry(
        entry_point=run_comment_issue_workflow,
        description="Comment-issue query via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1124 cohort 1: prioritization — strategy-category handler, 2-arg
    # (intent, workflow_id), reused unchanged via the parameterized factory.
    prioritization_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_prioritization"),
        description="Prioritization via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1124: content generation — synthesis-category handler, 2-arg, reused unchanged.
    generate_content_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_generate_content"),
        description="Content generation via action dispatch (#1124)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # RECONNECT #1327 gap 1: conversational "set my default repo to owner/name".
    # 2-arg (intent, workflow_id) handler, reused via the standard factory. Routed
    # via the action-dispatch rail (action_triggered) — NOT a hand-coded elif branch.
    set_default_repo_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_set_default_repo"),
        description="Set-default-repo via action dispatch (#1327)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # RECONNECT #1327 build #2: conversational "what's my default repo" — the read
    # counterpart. Same 2-arg (intent, workflow_id) factory + action-dispatch rail.
    get_default_repo_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_get_default_repo"),
        description="Get-default-repo via action dispatch (#1327)",
        requires_context=["intent", "intent_service"],
        action_triggered=True,
    )

    # #1331 TRUST: honest-degrade unwired WRITE actions. The LLM classifier can emit
    # write actions (e.g. create_milestone) with NO real handler; left alone they
    # fall to the floor, which CONFABULATES "created ✓" without writing anything.
    # Each unwired write registers an action-triggered entry routing to
    # _handle_unwired_write (2-arg, standard factory) so the action-dispatch rail
    # intercepts it BEFORE the floor and returns an honest decline. The covered set
    # is the single source of truth in services.intent_service.unwired_writes.
    # NOTE: honest-degrade FLOOR only — performs NO write (#1322 Q3 owns real writes).
    unwired_write_entry = WorkflowEntry(
        entry_point=_make_query_dispatch_entry_point("_handle_unwired_write"),
        description="Honest-degrade unwired write via action dispatch (#1331)",
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
        # #1124 step 3: issue-mutation cohort (aliases mirror the migrated elif branches).
        "close_issue": close_issue_entry,
        "close_issue_query": close_issue_entry,
        "reopen_issue": reopen_issue_entry,
        "reopen_issue_query": reopen_issue_entry,
        "comment_issue": comment_issue_entry,
        "add_comment": comment_issue_entry,
        "comment_issue_query": comment_issue_entry,
        # #1124 cohort 1: prioritization (strategy category).
        "prioritize": prioritization_entry,
        "set_priorities": prioritization_entry,
        # #1124: content generation (synthesis category).
        "generate_content": generate_content_entry,
        "create_content": generate_content_entry,
        # RECONNECT #1327 gap 1: set-default-repo (QUERY category, pre-classifier action).
        "set_default_repo": set_default_repo_entry,
        # RECONNECT #1327 build #2: get-default-repo (read counterpart).
        "get_default_repo": get_default_repo_entry,
    }

    # #1331: fan the honest-degrade entry over every recognized-but-unwired WRITE
    # action (create_milestone, create_release, …). Keyed on the classifier's
    # free-form action string so the rail (`intent.action in get_action_workflows()`)
    # intercepts before the floor. Source of truth: unwired_writes.UNWIRED_WRITE_ACTIONS.
    from services.intent_service.unwired_writes import UNWIRED_WRITE_ACTIONS

    for _unwired_action in UNWIRED_WRITE_ACTIONS:
        _default_entries[_unwired_action] = unwired_write_entry

    # #1124 step 3 cohort 2: GitHub read-query cohort — one shared entry point per
    # handler (built by the factory), fanned out to that handler's classifier aliases.
    for handler_attr, aliases in _READ_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(handler_attr),
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 calendar cohort — 3-arg (intent, workflow_id, user_id), user-scoped factory.
    for handler_attr, aliases in _CALENDAR_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_user_scoped_query_dispatch_entry_point(handler_attr),
            description=f"{handler_attr} via action dispatch (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )
        for alias in aliases:
            _default_entries[alias] = entry

    # #1124 analysis cohort — 2-arg (intent, workflow_id), standard factory.
    for handler_attr, aliases in _ANALYSIS_QUERY_COHORT.items():
        entry = WorkflowEntry(
            entry_point=_make_query_dispatch_entry_point(handler_attr),
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
    def _qentry(entry_point, description):
        return WorkflowEntry(
            entry_point=entry_point,
            description=f"{description} (#1124)",
            requires_context=["intent", "intent_service"],
            action_triggered=True,
        )

    _query_cohort: list[tuple[WorkflowEntry, list[str]]] = [
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_local_git_status_query"),
                "local-git-status via action dispatch",
            ),
            ["local_git_status_query", "local_git_status"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_search_documents_notion", pass_session_id=True
                ),
                "search-documents (Notion) via action dispatch",
            ),
            ["search_documents", "find_documents", "search_notion"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_productivity_query", pass_session_id=True
                ),
                "productivity query via action dispatch",
            ),
            ["productivity", "my_productivity", "weekly_metrics", "accomplishments"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_standup_query", pass_user_id=True),
                "standup query via action dispatch",
            ),
            ["show_standup", "get_standup"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_projects_query", pass_user_id=True),
                "projects query via action dispatch",
            ),
            ["list_projects", "show_projects"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point(
                    "_handle_attention_query", pass_session_id=True, pass_user_id=True
                ),
                "attention query via action dispatch",
            ),
            ["attention_query", "needs_attention", "what_needs_attention", "attention_items"],
        ),
        (
            _qentry(run_todo_query_workflow, "todo list/next query via action dispatch"),
            ["list_todos_query", "list_completed_todos", "next_todo_query"],
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
            ),
            ["analyze_document", "analyze_file"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_strategic_planning"),
                "strategic-planning via action dispatch",
            ),
            ["strategic_planning", "create_plan"],
        ),
        (
            _qentry(
                _make_query_dispatch_entry_point("_handle_learn_pattern"),
                "learn-pattern via action dispatch",
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
