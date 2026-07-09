"""
Workflow Dispatcher — registry-based routing for offer acceptance.

ADR-059: Replaces the if/elif switch in soft offer acceptance with a
registry lookup. New workflow types are added by registering an entry,
not modifying a switch statement.

Design principle (from OpenClaw Gateway pattern): this is dumb plumbing.
Maps workflow_type → entry_point. No business logic in the dispatch layer.
Unknown workflow types route to the conversational floor (safe default).

Issue #922: Fixes dead-end acceptances where workflow types were added
to the offer map but never wired to real handlers.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Coroutine, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class WorkflowEntry:
    """
    Registry entry for a dispatchable workflow.

    Attributes:
        entry_point: Async callable that starts the workflow.
            Signature: (session_id, user_id, context) -> IntentProcessingResult
        resume_point: Optional async callable for resuming a suspended workflow.
            If None, resume falls back to entry_point with existing session context.
        requires_context: List of context keys the workflow expects.
        description: Human-readable description for logging.
        action_triggered: If True, this workflow may be dispatched directly by a
            classified ``intent.action`` (#1124 pre-floor handler migration), in
            addition to / instead of offer-acceptance. Offer-only workflows (e.g.
            ``meeting``) leave this False so the action-dispatch rail never picks
            them up by an accidental key/action collision.
    """

    entry_point: Callable[..., Coroutine[Any, Any, Any]]
    resume_point: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None
    requires_context: list[str] = field(default_factory=list)
    description: str = ""
    action_triggered: bool = False


# ─── Workflow Registry ───────────────────────────────────────────────
# Each entry maps a workflow_type string to its WorkflowEntry.
# To add a new workflow: add an entry here and implement the entry_point.
# The dispatcher handles the routing — no switch statement needed.

WORKFLOW_REGISTRY: Dict[str, WorkflowEntry] = {}


def register_workflow(workflow_type: str, entry: WorkflowEntry) -> None:
    """
    Register a workflow entry point.

    Raises ValueError if workflow_type is already registered
    (prevents silent overwrites).
    """
    if workflow_type in WORKFLOW_REGISTRY:
        raise ValueError(
            f"Workflow type '{workflow_type}' is already registered. "
            f"Existing: {WORKFLOW_REGISTRY[workflow_type].description}"
        )
    WORKFLOW_REGISTRY[workflow_type] = entry
    logger.info(
        "workflow_registered",
        workflow_type=workflow_type,
        description=entry.description,
    )


def get_registered_workflows() -> Dict[str, WorkflowEntry]:
    """Return a copy of the workflow registry for inspection."""
    return dict(WORKFLOW_REGISTRY)


def get_action_workflows() -> Dict[str, WorkflowEntry]:
    """Return only the workflows that may be dispatched by a classified
    ``intent.action`` (#1124). Offer-only workflows (action_triggered=False)
    are excluded so the action-dispatch rail can't pick them up by accident.
    """
    return {k: v for k, v in WORKFLOW_REGISTRY.items() if v.action_triggered}


async def dispatch_workflow(
    workflow_type: str,
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    resume: bool = False,
) -> Optional[Any]:
    """
    Dispatch a workflow by type.

    Args:
        workflow_type: The type of workflow to start (e.g., "meeting").
        session_id: Current session ID.
        user_id: Current user ID.
        context: Additional context (trigger_message, active_lens, etc.).
        resume: If True, use resume_point instead of entry_point.

    Returns:
        IntentProcessingResult from the workflow entry point, or None if
        the workflow type is unknown (caller should route to floor).
    """
    entry = WORKFLOW_REGISTRY.get(workflow_type)

    if entry is None:
        # ADR-059: Unknown workflow type → log as wiring bug, return None.
        # Caller routes to conversational floor.
        logger.warning(
            "workflow_dispatch_unknown_type",
            workflow_type=workflow_type,
            registered_types=list(WORKFLOW_REGISTRY.keys()),
            reason="no_registered_entry_point",
        )
        return None

    # Choose entry point or resume point
    if resume and entry.resume_point is not None:
        handler = entry.resume_point
        logger.info(
            "workflow_dispatch_resume",
            workflow_type=workflow_type,
            description=entry.description,
        )
    else:
        handler = entry.entry_point
        logger.info(
            "workflow_dispatch_start",
            workflow_type=workflow_type,
            description=entry.description,
            resume_fallback=resume and entry.resume_point is None,
        )

    try:
        return await handler(
            session_id=session_id,
            user_id=user_id,
            context=context or {},
        )
    except Exception as e:
        logger.error(
            "workflow_dispatch_error",
            workflow_type=workflow_type,
            error=str(e),
            exc_info=True,
        )
        return None


def validate_registry() -> list[str]:
    """
    Validate that all registered workflows have callable entry points.

    Returns list of error messages (empty = valid).
    Called at startup to catch wiring bugs early.
    """
    errors = []
    for workflow_type, entry in WORKFLOW_REGISTRY.items():
        if not callable(entry.entry_point):
            errors.append(
                f"Workflow '{workflow_type}' entry_point is not callable: {entry.entry_point}"
            )
        if entry.resume_point is not None and not callable(entry.resume_point):
            errors.append(
                f"Workflow '{workflow_type}' resume_point is not callable: {entry.resume_point}"
            )
    return errors


# ---------------------------------------------------------------------------
# #1283 AC-4 (b): near-miss emission normalization — Arch-ratified 2026-07-08.
#
# The live probe proved the LLM emits paraphrase VARIANTS of canonical action
# names that slip past hand-maintained alias lists (run 1: list_stale_prs past
# four stale aliases; analyze_productivity past four productivity aliases;
# run 2: get_pull_requests, a third stale-family variant). This shim is the
# ruled second net UNDER the aliases (additive — never a reason to prune
# them): a conservative prefix-strip that maps an unknown emission to a rail
# key only on an EXACT post-strip match — unambiguous by construction. No
# fuzzy scoring: a wrong confident map is worse than a pass-through (the
# pass-through still lands in category handling, and the structured log line
# feeds the alias/vocabulary loop).
# ---------------------------------------------------------------------------

_NORMALIZE_PREFIXES = ("list_", "get_", "show_", "analyze_", "fetch_", "display_")


def normalize_action(action: str) -> str:
    """Map a near-miss LLM action emission onto its rail key, conservatively.

    Known action (already a rail key) → unchanged. Unknown action whose
    prefix-stripped form IS a rail key → that key (logged). Anything else →
    unchanged (falls through to category routing exactly as before this shim).
    """
    if not action:
        return action
    workflows = get_action_workflows()
    if action in workflows:
        return action
    for prefix in _NORMALIZE_PREFIXES:
        if action.startswith(prefix):
            stripped = action[len(prefix):]
            if stripped in workflows:
                logger.info("action_normalized", emitted=action, rail_key=stripped)
                return stripped
    logger.debug("action_unnormalized", emitted=action)
    return action
