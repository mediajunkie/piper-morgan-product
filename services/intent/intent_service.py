"""
Intent Service - Business Logic for Intent Processing

Extracts business logic from web/app.py /api/v1/intent route.
Handles intent classification, orchestration coordination, and response formatting.

Phase 2B: Service layer extraction for clean architecture
Phase 2B (Issue #197): Ethics enforcement integration at universal entry point
"""

import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import structlog
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.consciousness.files_consciousness import (
    format_files_conscious,
    format_projects_conscious,
)
from services.consciousness.learning_consciousness import format_patterns_learned_conscious
from services.consciousness.search_consciousness import (
    format_no_results_conscious,
    format_search_error_conscious,
    format_search_results_conscious,
)
from services.conversation.conversation_handler import ConversationHandler
from services.conversation.conversation_manager import ConversationManager
from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent, RequestContext
from services.ethics.boundary_enforcer_refactored import boundary_enforcer_refactored
from services.intent_service import classifier
from services.intent_service.action_mapper import ActionMapper
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import (
    build_recent_history,
    get_or_create_context,
)
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.intent_service.soft_invocation import (
    SoftInvocationDetector,
    WorkflowOfferService,
    detect_offer_response,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.knowledge.conversation_integration import ConversationKnowledgeGraphIntegration
from services.learning.learning_handler import LearningHandler
from services.personality.personality_profile import PersonalityProfile
from services.process import ProcessCheckResult, ProcessType, get_process_registry
from services.repositories.user_trust_profile_repository import UserTrustProfileRepository
from services.shared_types import IntentCategory, TrustStage
from services.slot_filling.slot_filling_adapter import SlotFillingProcessAdapter
from services.slot_filling.slot_template import MEETING_TEMPLATE
from services.trust.trust_computation_service import TrustComputationService
from services.ui_messages.user_friendly_errors import UserFriendlyErrorService


@dataclass
class IntentProcessingResult:
    """
    Result from intent processing.

    Contains all data needed by HTTP route to format response.
    Separates business logic result from HTTP concerns.
    """

    success: bool
    message: str
    intent_data: Dict[str, Any]
    workflow_id: Optional[str] = None
    # Issue #878: Handlers that start real async/background work set this to True.
    # The route layer strips workflow_id unless this is True, preventing the frontend
    # from polling a workflow that will never progress. See ADR note in intent.py.
    async_work_started: bool = False
    requires_clarification: bool = False
    clarification_type: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    implemented: bool = True  # CORE-CRAFT-GAP: Track actual implementation vs placeholders
    suggestions: Optional[List[Dict[str, Any]]] = (
        None  # Phase 3: Pattern suggestions  # CORE-CRAFT-GAP: Track actual implementation vs placeholders
    )
    preferences: Optional[Dict[str, Any]] = None  # Issue #248: Preference detection results
    # Issue #595: Multi-intent support
    multi_intent_greeting: bool = (
        False  # True if greeting was detected alongside substantive intent
    )
    secondary_intents: Optional[List[Dict[str, Any]]] = None  # Other intents detected
    # Issue #764: Multi-substantive intent orchestration
    multi_intent_orchestrated: bool = (
        False  # True if multiple substantive intents were orchestrated
    )
    # Issue #767: Soft workflow invocation
    pending_offer: Optional[Dict[str, Any]] = None  # Active soft offer awaiting response


class IntentProcessingError(Exception):
    """Raised when intent processing fails"""

    pass


def _autonomous_execution_enabled() -> bool:
    """#1195: master flag for autonomous (read-only) auto-execution of
    high-confidence learned patterns. Default OFF; set
    ``AUTONOMOUS_EXECUTION_ENABLED=true`` (alpha) to activate.

    Read at call time (not import) so it can be toggled without a restart in
    tests. Note this is only the *gate to offer* a pattern to the executor —
    every actual execution is still gated by
    ``AutonomousExecutor.execute_with_safety`` AND the read-only allow-list
    below."""
    import os

    return os.getenv("AUTONOMOUS_EXECUTION_ENABLED", "false").strip().lower() == "true"


# #1195: explicit deny-by-default read-only allow-list for autonomous execution.
# The ActionClassifier's keyword SAFE check is necessary but NOT sufficient: the
# "_query" suffix on mutating actions (comment_issue_query, close_issue_query,
# reopen_issue_query) matches the SAFE "query" keyword via substring, so the
# classifier alone green-lights state-changing actions (#1210). This list is the
# OUTER gate — only genuinely read-only action_types are ever offered to
# execute_with_safety; the classifier remains the inner gate (defense-in-depth).
# Expanding the autonomous-executable set (incl. mutating-with-undo) is #1209.
_AUTOEXEC_READONLY_ALLOWLIST = frozenset(
    {
        "list_issues_query",
        "list_issues",
        "list_prs_query",
        "list_prs",
        "list_pull_requests",
        "list_milestones_query",
        "list_milestones",
        "list_releases_query",
        "list_releases",
        "list_labels_query",
        "list_labels",
        "list_branches_query",
        "list_branches",
        "list_projects",
        "list_todos_query",
        "list_completed_todos",
        "next_todo_query",
        "get_issue",
        "get_standup",
        "local_git_status_query",
        "attention_query",
        "shipped_this_week",
        "shipped_query",
    }
)


def _principal_from_intent(intent) -> Optional[str]:
    """The single sanctioned read of the request principal from an intent.

    The principal (a ``users.id`` string) is stamped onto ``intent.context``
    at the host boundary in ``IntentService.process_intent`` (when a ``user_id``
    is supplied). Downstream handlers read it through THIS accessor rather than
    re-deriving ``_principal_from_intent(intent)`` at
    each site — that scattered ternary was the ADR-071 D5 degradation
    anti-pattern (the principal silently becoming ``None`` → unscoped reads),
    now consolidated to one place and enforced by
    ``scripts/principal_threading_lint.py``.

    Returns ``None`` for genuinely principal-less calls (system/internal
    invocations that ``process_intent`` received without a ``user_id``).
    Tightening this to a *required* principal threaded end-to-end is the deeper
    ADR-071 D4 follow-on; this consolidation is the first, behaviour-preserving
    step (#1252). NOTE: keep this accessor free of the ``... if ... else None``
    ternary so the D5 lint stays satisfied — it is the sanctioned path.
    """
    context = intent.context or {}
    return context.get("user_id")


class IntentService:
    """
    Service for processing user intents.

    Handles intent classification, orchestration coordination, and response formatting.
    Decouples business logic from HTTP route handlers.

    Architecture:
        - Direct dispatch via task_type registry (#1094, Pattern-072)
        - Handles Tier 1 conversation bypass (Phase 3D)
        - Routes QUERY intents appropriately
        - Preserves Phase 3C placeholders

    Phase 2B: Extracted from web/app.py lines 327-551 (225 lines)
    """

    # Issue #907: Generic fallback text constant for comparison.
    # When _get_contextual_fallback returns this exact text, the conversational
    # floor takes over instead.
    _GENERIC_FALLBACK_TEXT = (
        "I don't have that capability yet, but I'm learning! "
        "Try asking 'What can you do?' to see what I can help with, "
        "or let me know if there's something else I can assist with."
    )

    def __init__(
        self,
        intent_classifier: Optional = None,
        conversation_handler: Optional[ConversationHandler] = None,
        conversation_manager: Optional[ConversationManager] = None,
    ):
        """
        Initialize service with dependencies.

        Args:
            intent_classifier: Optional classifier for intent detection
            conversation_handler: Optional handler for conversation intents
            conversation_manager: Optional manager for conversation persistence (Issue #563)
        """
        self.intent_classifier = intent_classifier or classifier
        self.conversation_handler = conversation_handler
        self.conversation_manager = conversation_manager  # Issue #563: Conversation persistence
        self.canonical_handlers = CanonicalHandlers()
        self.intent_orchestrator = IntentOrchestrator(
            canonical_handlers=self.canonical_handlers
        )  # Issue #764: Multi-substantive orchestration
        self.soft_invocation_detector = SoftInvocationDetector()  # Issue #767
        self.workflow_offer_service = WorkflowOfferService()  # Issue #767
        # Issue #825: Register slot filling with process registry
        self.slot_filling_adapter = SlotFillingProcessAdapter()
        try:
            registry = get_process_registry()
            registry.register(self.slot_filling_adapter)
        except Exception:
            pass  # Graceful — slot filling optional
        self.kg_integration = ConversationKnowledgeGraphIntegration()  # Issue #99 CORE-KNOW
        self.todo_handlers = TodoIntentHandlers()  # Issue #285: Todo chat integration
        self.learning_handler = LearningHandler()  # Issue #300: Basic Auto-Learning
        self._friendly_errors = (
            UserFriendlyErrorService()
        )  # Issue #876: Conversational error messages
        self.logger = structlog.get_logger()

    def _apply_soft_offer(
        self,
        result: "IntentProcessingResult",
        message: str,
        session_id: str,
        current_turn: int = 0,
        trust_stage: Optional[TrustStage] = None,
        user_id: Optional[str] = None,
        formality_baseline: Optional[float] = None,
    ) -> "IntentProcessingResult":
        """
        Issue #767: Check for soft invocation opportunity and append offer.

        Called after intent processing to potentially add a soft workflow offer
        to the response. Respects ProactivityGate throttling.

        Args:
            result: The intent processing result to potentially modify
            message: Original user message
            session_id: Current session ID
            current_turn: Current conversation turn number
            trust_stage: User's resolved trust stage (Issue #826).
                None falls back to BUILDING for backward compatibility.

        Returns:
            Modified result with offer appended, or original result unchanged
        """
        if not result.success:
            return result

        try:
            # Issue #820: Read current lens from conversation context
            # Classifier already extracts and stores lens during classify_multiple()
            current_lens = None
            try:
                conv_context = get_or_create_context(session_id, user_id=user_id)
                current_lens = conv_context.current_lens
            except (ValueError, KeyError):
                pass  # Non-UUID session_id or missing context — proceed without lens

            detection = self.soft_invocation_detector.detect(
                message, active_lens=current_lens, formality_baseline=formality_baseline
            )
            if not detection.has_offer:
                return result

            # Issue #826: Use resolved trust stage from caller, default to BUILDING
            if trust_stage is None:
                trust_stage = TrustStage.BUILDING
            suggestions_count = 0  # TODO: Track across session

            allowed, reason = self.workflow_offer_service.should_offer(
                trust_stage=trust_stage,
                session_id=session_id,
                current_turn=current_turn,
                suggestions_this_session=suggestions_count,
                user_id=user_id,
            )

            if not allowed:
                self.logger.debug(
                    "soft_offer_throttled",
                    reason=reason,
                    workflow_type=detection.offer.workflow_type,
                )
                return result

            # Append offer to response
            result.message = self.workflow_offer_service.format_offer(
                detection.offer, result.message
            )
            result.pending_offer = {
                "workflow_type": detection.offer.workflow_type,
                "offer_message": detection.offer.offer_message,
                "decline_message": detection.offer.decline_message,
                "active_lens": current_lens,  # Issue #820: Include lens context
                "trigger_message": message,  # Issue #825: For slot extraction
            }

            # Record offer for throttling and store as pending (#817: user-scoped)
            self.workflow_offer_service.record_offer(session_id, current_turn, user_id=user_id)
            # Issue #824: Store pending offer for accept/decline on next turn
            self.workflow_offer_service.set_pending_offer(
                session_id, result.pending_offer, user_id=user_id
            )

            self.logger.info(
                "soft_offer_added",
                workflow_type=detection.offer.workflow_type,
                session_id=session_id,
                active_lens=current_lens,  # Issue #820: Log lens context
            )

        except Exception as e:
            self.logger.warning(f"Soft invocation check failed: {e}")
            # Graceful degradation — return original result

        return result

    async def _save_conversation_turn(
        self,
        session_id: str,
        user_message: str,
        assistant_response: str,
        entities: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        provenance: Optional[dict] = None,
        context_state: Optional[dict] = None,
    ) -> None:
        """
        Save conversation turn via ConversationManager (Issue #563).

        Follows DDD pattern: IntentService coordinates, ConversationManager persists.
        Fails silently to avoid blocking the response - persistence is best-effort.

        Args:
            session_id: Session/conversation identifier
            user_message: The user's original message
            assistant_response: Piper's response
            entities: Optional extracted entities
            user_id: Optional user ID for conversation ownership
            provenance: Issue #1030 R4 — provenance dict to persist into
                turn_metadata['provenance'] for cross-session lookup (PM Q1
                GUARANTEED).
        """
        if not self.conversation_manager:
            self.logger.debug("ConversationManager not available - skipping turn persistence")
            return

        try:
            await self.conversation_manager.save_conversation_turn(
                conversation_id=session_id,
                user_message=user_message,
                assistant_response=assistant_response,
                entities=entities,
                user_id=user_id,
                provenance=provenance,
                context_state=context_state,
            )
            self.logger.debug(
                "Conversation turn saved",
                session_id=session_id,
                message_preview=user_message[:50] if user_message else None,
            )
        except Exception as e:
            # Don't fail the response if persistence fails
            self.logger.warning(
                "Failed to save conversation turn",
                session_id=session_id,
                error=str(e),
            )

    async def process_intent(
        self,
        message: str,
        session_id: str = "default_session",
        user_id: str = None,
        ctx: Optional[RequestContext] = None,
    ) -> IntentProcessingResult:
        """
        Process user intent and return formatted response.

        Issue #563: Wraps _process_intent_internal to save conversation turns.
        ADR-051 Phase 3: Accepts RequestContext for unified identity handling.

        Args:
            message: The user's intent text
            session_id: Session identifier (deprecated - use ctx.conversation_id)
            user_id: Optional user ID (deprecated - use ctx.user_id)
            ctx: RequestContext with unified identity (preferred)

        Returns:
            IntentProcessingResult with results
        """
        # ADR-051: Extract from context when available, fallback to old params
        effective_user_id = str(ctx.user_id) if ctx else user_id
        effective_session_id = str(ctx.conversation_id) if ctx else session_id

        # Issue #913: Continuation rate instrumentation
        # Check if the previous response in this session was a floor hit
        try:
            conv_ctx = get_or_create_context(effective_session_id, user_id=effective_user_id)
            # #953: hydrate persisted Layer-4 state (lens_stack + last_offer + floor
            # flags) once per in-memory context, on first touch in this async path —
            # so a resumed session restores its lens/offer/floor state (restart/refresh).
            # Flag set before the await → once-only, no per-turn retry; best-effort.
            if not conv_ctx._hydrated:
                conv_ctx._hydrated = True
                if self.conversation_manager:
                    try:
                        _persisted = await self.conversation_manager.load_context_state(
                            effective_session_id
                        )
                        if _persisted:
                            conv_ctx.apply_persisted_state(_persisted)
                    except Exception:
                        pass  # best-effort hydration — never block the turn
            # #1122: backfill the in-memory turn window from persisted turns
            # whenever it's empty (server restart, 30-min prune, resumed
            # conversation) — the registry is process-local but the DB has
            # every completed turn. Checked per-turn (not once-only like the
            # Layer-4 flag) because pruning can empty the window mid-lifetime.
            if not conv_ctx.turns and message:
                from services.intent_service.conversation_context import (
                    hydrate_turns_from_db,
                )

                await hydrate_turns_from_db(
                    conv_ctx, self.conversation_manager, effective_session_id
                )
            # #1122: record the in-flight turn for EVERY path, not just the
            # one floor site that called add_turn (R4 fix). Before this, turns
            # routed to canonical/structured handlers were never recorded
            # in-memory, so follow-up antecedents ("the doc", "that one") had
            # no prior turn to bind against, and the #922 response-write below
            # could overwrite an OLDER turn's response. Guard: skip only a
            # same-message turn still awaiting its response (double-submit);
            # a completed identical message (e.g. "yes" twice) records anew.
            if message and (
                not conv_ctx.turns
                or conv_ctx.turns[-1].message != message
                or conv_ctx.turns[-1].response is not None
            ):
                conv_ctx.add_turn(message=message)
            if conv_ctx.last_response_was_floor:
                self.logger.info(
                    "floor_continuation_detected",
                    session_id=effective_session_id,
                    user_id=effective_user_id,
                    previous_floor_category=conv_ctx.last_floor_category,
                    continuation=True,
                )
                # Reset the flag — we've logged the continuation
                conv_ctx.last_response_was_floor = False
                conv_ctx.last_floor_category = None
        except Exception:
            pass  # Best-effort instrumentation, never block processing

        # Process the intent
        result = await self._process_intent_internal(
            message=message,
            session_id=effective_session_id,
            user_id=effective_user_id,
            ctx=ctx,
        )

        # Issue #563: Save conversation turn after processing (best-effort)
        # Only save successful responses with actual content
        if result.success and result.message:
            # Issue #1030 R4 Step 11: extract provenance from in-memory
            # sidecar for the just-completed turn so it persists to DB for
            # cross-session lookup (PM Q1 GUARANTEED disposition).
            turn_provenance_for_db = None
            context_state_for_db = None
            try:
                # #1122: do NOT re-import get_or_create_context here — a
                # function-local import makes the name local for the WHOLE
                # function, so the #913/#953 block above raised
                # UnboundLocalError on its first reference and silently
                # no-op'd via its except-pass (dead since this import landed).
                conv_ctx = get_or_create_context(effective_session_id, user_id=effective_user_id)
                if conv_ctx.turns:
                    latest_turn = conv_ctx.turns[-1]
                    turn_provenance_for_db = conv_ctx.turn_provenance.get(latest_turn.id)
                # #953: capture the Layer-4 context slice (lens_stack + last_offer +
                # floor flags) to persist alongside the turn so it survives restart/refresh.
                context_state_for_db = conv_ctx.to_persistable_state()
            except Exception:
                pass  # Best-effort; persistence proceeds without provenance/context

            await self._save_conversation_turn(
                session_id=effective_session_id,
                user_message=message,
                assistant_response=result.message,
                user_id=effective_user_id,
                provenance=turn_provenance_for_db,
                context_state=context_state_for_db,
            )

            # #922: Store response in the in-memory ConversationContext so the floor
            # has Piper's replies for conversational continuity (e.g., "OK" after a plan)
            # (#1122: no local re-import — see scoping note in the provenance block above)
            try:
                conv_ctx = get_or_create_context(effective_session_id, user_id=effective_user_id)
                if conv_ctx.turns:
                    conv_ctx.turns[-1].response = result.message
            except Exception:
                pass  # Best-effort — don't block response delivery

        return result

    async def _maybe_autoexecute_automation_patterns(
        self,
        automation_patterns: list,
        session_id: str,
        user_id: Optional[str],
    ) -> list:
        """#1195: flag-gated autonomous execution of high-confidence learned
        patterns. Wires the previously-orphaned ``AutonomousExecutor`` into the
        pattern-application path (the ``auto_triggered`` flag was set but never
        acted on). ALL safety gates live in ``execute_with_safety``; this only
        decides which patterns to *offer* it and how to run the predicted action.

        Safety envelope (defense-in-depth — TWO gates, both required):
          1. OUTER: the action_type must be on ``_AUTOEXEC_READONLY_ALLOWLIST``
             (deny-by-default). This is the load-bearing gate: the classifier's
             keyword SAFE check is NOT sufficient on its own — "_query"-suffixed
             mutating actions (comment_issue_query / close_issue_query /
             reopen_issue_query) match the SAFE "query" keyword (#1210), so
             trusting the classifier alone would auto-execute state changes.
          2. INNER: ``execute_with_safety`` (emergency-stop + classify + SAFE +
             confidence >= 0.9 + never-destructive + audit + rollback).
        Both gates must pass, so this can ONLY ever auto-run a vetted *read* —
        never auto-create/comment/close/delete. Mutating auto-execution + the
        rollback UX is the fleshing-out increment (#1209); the user-facing
        proactive surface is #1174. This minimal wire's observable outputs are
        the execution + audit trail + a structured log; no user surfacing yet.

        No-op unless the flag is on AND a SAFE >= 0.9 pattern matched context.
        Returns the executed patterns (for tests + the future #1174 surface).
        """
        if not _autonomous_execution_enabled() or not automation_patterns or not user_id:
            return []
        try:
            from uuid import UUID as _UUID

            from services.automation.autonomous_executor import get_autonomous_executor
            from services.intent_service.workflow_dispatcher import dispatch_workflow
        except Exception:  # pragma: no cover - import safety
            return []

        try:
            uid = _UUID(user_id) if isinstance(user_id, str) else user_id
        except (ValueError, TypeError):
            return []

        # Workflows are registered at container init; an unregistered type makes
        # dispatch_workflow return None (safe no-op), so no defensive re-register.
        executor = get_autonomous_executor()
        executed: list = []
        for pattern in automation_patterns:
            pattern_data = pattern.get("pattern_data") or {}
            action_type = pattern_data.get("action_type")
            if not action_type:
                continue
            # OUTER GATE (#1195/#1210): read-only allow-list, deny-by-default.
            if action_type not in _AUTOEXEC_READONLY_ALLOWLIST:
                continue
            confidence = float(pattern.get("confidence", 0.0) or 0.0)

            # action_handler: run the predicted action through the SAME dispatch
            # rail a manual request uses. dispatch_workflow returns None for an
            # unregistered type (safe no-op). Bound to read-only by the SAFE gate
            # inside execute_with_safety, so this never mutates state.
            async def _handler(_at=action_type, _ctx=(pattern_data.get("context") or {})):
                return await dispatch_workflow(
                    workflow_type=_at,
                    session_id=session_id,
                    user_id=str(uid),
                    context={"autonomous": True, **_ctx},
                )

            try:
                exec_result = await executor.execute_with_safety(
                    action_type=action_type,
                    action_handler=_handler,
                    confidence=confidence,
                    user_id=uid,
                    context={
                        "pattern_id": pattern.get("pattern_id"),
                        "source": "automation_pattern",
                    },
                )
                if exec_result.executed:
                    executed.append(
                        {
                            "pattern_id": pattern.get("pattern_id"),
                            "action_type": action_type,
                            "confidence": confidence,
                            "auto_executed": True,
                            "result_preview": str(exec_result.result)[:200],
                        }
                    )
                    self.logger.info(
                        "autonomous_pattern_executed",
                        action_type=action_type,
                        confidence=confidence,
                        pattern_id=pattern.get("pattern_id"),
                        safety_level=exec_result.safety_level,
                    )
            except Exception as e:
                self.logger.warning(f"Autonomous execution attempt failed for {action_type}: {e}")
        return executed

    def _observe_action_verb(self, intent, message: str) -> None:
        """#1124 Phase 3: emit a canonicalization-backlog signal for any classified
        action with no registered Verb.

        Observability ONLY — does NOT change routing. Per the Architect ruling
        (2026-06-07), enforce-floor ("unknown verb -> floor") waits for Phase 4,
        because the verb vocab (ACTION_TO_VERB) does not yet cover the ~40+
        category-routed/LLM-classifier actions, which Phase 4 retires. This
        structured stream IS the work-list Phase 4 builds against (which verbs to
        add / prompts to canonicalize) and the artifact its canonical-retest gate
        is evaluated with (did would-floor actions disappear post-Phase-4?).

        Filterable by `signal="canonicalization_backlog"`. Never raises — an
        observability failure must not break classification.
        """
        try:
            from services.intent_service.action_registry import get_verb

            if get_verb(intent.action) is None:
                self.logger.info(
                    "action_verb_unregistered",
                    signal="canonicalization_backlog",  # #1124 Phase 4 consumes this
                    action=intent.action,
                    category=intent.category.value if intent.category else None,
                    sample=(message or "")[:80],
                )
        except Exception as e:  # pragma: no cover - defensive
            self.logger.debug("action_verb_observe_failed", error=str(e))

    async def _process_intent_internal(
        self,
        message: str,
        session_id: str = "default_session",
        user_id: str = None,
        ctx: Optional[RequestContext] = None,
    ) -> IntentProcessingResult:
        """
        Internal intent processing logic.

        ADR-051 Phase 3: Accepts RequestContext for unified identity handling.
        ctx is optional during migration; when present, user_id/session_id are
        already extracted from it by process_intent().

        Handles:
        - Ethics boundary enforcement (Issue #197 - Phase 2B)
        - Tier 1 conversation bypass (Phase 3D)
        - Intent classification
        - Workflow creation with timeout protection
        - QUERY intent routing (standup, projects, generic)
        - Error handling

        Args:
            message: The user's intent text
            session_id: Session identifier
            user_id: Optional user ID from authenticated request (Issue #490)

        Returns:
            IntentProcessingResult with results

        Raises:
            IntentProcessingError: If processing fails
        """
        try:
            # Issue #899: Off-topic pause message prefix (set by guided process check)
            off_topic_prefix = None

            # Issue #838: Load formality baseline from PersonalityProfile
            # Must load early — needed by pending offer handling and soft offer detection.
            formality_baseline = None
            if user_id:
                try:
                    from services.personality.formality import DEFAULT_WARMTH

                    profile = await PersonalityProfile.load_with_preferences(user_id)
                    formality_baseline = profile.warmth_level
                    self.logger.debug(
                        "formality_baseline_loaded",
                        user_id=user_id,
                        formality_baseline=formality_baseline,
                    )
                except Exception as e:
                    self.logger.warning(f"Formality baseline load failed: {e}")
                    formality_baseline = DEFAULT_WARMTH

            # ADR-059: Unified offer acceptance via workflow dispatcher.
            # Single detection point for all offer types — no parallel paths.
            # Must run before classification — "yes please" is a response to an offer,
            # not a new intent to classify.
            pending_offer = self.workflow_offer_service.get_and_clear_pending_offer(
                session_id, user_id=user_id
            )
            if pending_offer:
                response_type = detect_offer_response(message)
                if response_type == "accept":
                    workflow_type = pending_offer["workflow_type"]

                    # ADR-059: Dispatch through workflow registry instead of switch
                    from services.intent_service.workflow_dispatcher import dispatch_workflow

                    dispatch_context = {
                        "trigger_message": pending_offer.get("trigger_message", ""),
                        "active_lens": pending_offer.get("active_lens"),
                        "formality_baseline": formality_baseline,
                        "slot_filling_adapter": self.slot_filling_adapter,
                    }

                    result = await dispatch_workflow(
                        workflow_type=workflow_type,
                        session_id=session_id,
                        user_id=user_id,
                        context=dispatch_context,
                    )

                    if result is not None:
                        # Dispatcher returned a result — build the response
                        self.logger.info(
                            "soft_offer_accepted_via_dispatcher",
                            workflow_type=workflow_type,
                            session_id=session_id,
                        )
                        return IntentProcessingResult(
                            success=True,
                            message=result["message"],
                            intent_data=result.get(
                                "intent_data",
                                {
                                    "category": "soft_offer_accepted",
                                    "action": workflow_type,
                                },
                            ),
                        )
                    else:
                        # Unknown workflow type — route to floor with context
                        self.logger.info(
                            "soft_offer_accepted_unknown_workflow_to_floor",
                            workflow_type=workflow_type,
                            session_id=session_id,
                        )
                        return await self._handle_unknown_intent(
                            Intent(
                                category=IntentCategory.UNKNOWN,
                                action=workflow_type,
                                confidence=0.5,
                                original_message=message,
                            ),
                            None,
                            session_id,
                        )

                elif response_type == "decline":
                    decline_msg = pending_offer.get(
                        "decline_message",
                        "No worries, just let me know if you change your mind.",
                    )
                    self.logger.info(
                        "soft_offer_declined",
                        workflow_type=pending_offer["workflow_type"],
                        session_id=session_id,
                    )
                    return IntentProcessingResult(
                        success=True,
                        message=decline_msg,
                        intent_data={
                            "category": "soft_offer_declined",
                            "action": pending_offer["workflow_type"],
                        },
                    )
                # Neither accept nor decline — user moved on. Continue normal processing.

            # Issue #852: Contextual offer continuation
            # If the user was offered something contextual (not a workflow) on the
            # previous turn, check if they're accepting it with a bare affirmative.
            # One-turn memory: always clear, regardless of user response.
            contextual_continuation_hint = None
            if session_id:
                from services.intent_service.conversation_context import get_or_create_context

                try:
                    _conv_ctx = get_or_create_context(session_id)
                except (ValueError, KeyError):
                    _conv_ctx = None  # Non-UUID session_id — skip offer tracking
                if _conv_ctx and _conv_ctx.last_offer:
                    last_offer = _conv_ctx.last_offer
                    _conv_ctx.last_offer = None  # One-turn memory: always clear

                    response_type = detect_offer_response(message)
                    if response_type == "accept":
                        contextual_continuation_hint = last_offer.continuation_hint
                        self.logger.info(
                            "contextual_offer_accepted",
                            continuation_hint=contextual_continuation_hint,
                            session_id=session_id,
                        )
                    else:
                        self.logger.debug(
                            "contextual_offer_expired",
                            offer_hint=last_offer.continuation_hint,
                            user_response_type=response_type,
                            session_id=session_id,
                        )

            # Issue #826: Resolve trust stage from real computation service
            # Pre-fetch here so _apply_soft_offer() receives resolved domain data
            resolved_trust_stage = None
            if user_id:
                try:
                    async with AsyncSessionFactory.session_scope() as db_session:
                        trust_repo = UserTrustProfileRepository(db_session)
                        trust_service = TrustComputationService(trust_repo)
                        resolved_trust_stage = await trust_service.get_trust_stage(UUID(user_id))
                    self.logger.debug(
                        "trust_stage_resolved",
                        user_id=user_id,
                        trust_stage=resolved_trust_stage.name if resolved_trust_stage else None,
                    )
                except Exception as e:
                    self.logger.warning(f"Trust stage resolution failed: {e}")
                    # Fallback: _apply_soft_offer will use BUILDING default

            # ADR-049: Active guided processes take priority over classification
            # Domain invariant: Once a user enters a guided process (onboarding, standup, etc.),
            # ALL their messages belong to that process until completion/exit.
            # This check MUST run before any classification.
            guided_process_result, off_topic_prefix = await self._check_active_guided_process(
                user_id=user_id,
                session_id=session_id,
                message=message,
            )
            if guided_process_result:
                return guided_process_result

            # ADR-059: Onboarding offer check disabled — onboarding on ice.
            # Was: _check_pending_onboarding_offer() at pipeline position 2.
            # Will be replaced by workflow dispatcher (ADR-059 Phase C).

            # Issue #889: Check for pending resume offer (SUSPENDED state).
            # If user was offered to resume a suspended session, catch their response.
            if user_id and session_id:
                pending_resume_result = await self._check_pending_resume_offer(
                    user_id=user_id,
                    session_id=session_id,
                    message=message,
                )
                if pending_resume_result:
                    return pending_resume_result

            # Issue #585: Check for /standup command BEFORE classification
            # This routes the explicit command to the interactive handler
            # Note: This starts a NEW standup, not checking an active one (registry handles that)
            if message.strip().lower() == "/standup":
                self.logger.info(
                    "Standup command detected - starting interactive flow",
                    user_id=user_id,
                    session_id=session_id,
                )
                return await self._start_standup_conversation(user_id, session_id)

            # Issue #1269: a standup QUERY ("give me my standup", "what's my standup") →
            # the DERIVED on-demand standup (StandupAssembler over the live entity catalog),
            # routed deterministically BEFORE classification. The LLM classifier conflates
            # these with get_project_status (verified: "give me my standup" → get_project_status,
            # conf 1.0), so they never reached _handle_standup_query and Piper improvised a
            # fabricated standup. The interactive `/standup` capture flow is separate (above).
            if self._is_standup_query(message):
                self.logger.info(
                    "Standup query detected - routing to derived on-demand standup (#1269)",
                    user_id=user_id,
                    session_id=session_id,
                )
                standup_intent = Intent(
                    category=IntentCategory.STATUS,
                    action="get_standup",
                    original_message=message,
                    confidence=1.0,
                )
                return await self._handle_standup_query(standup_intent, standup_intent.id, user_id)

            # Issue #197 Phase 2B: Ethics enforcement at universal entry point
            # Check ENABLE_ETHICS_ENFORCEMENT environment variable (default: False for gradual rollout)
            ethics_enabled = os.getenv("ENABLE_ETHICS_ENFORCEMENT", "false").lower() == "true"

            if ethics_enabled:
                self.logger.info("Ethics enforcement enabled - checking boundaries")
                ethics_decision = await boundary_enforcer_refactored.enforce_boundaries(
                    message=message,
                    session_id=session_id,
                    context={
                        "source": "intent_service",
                        "timestamp": datetime.now(timezone.utc),
                    },
                )

                if ethics_decision.violation_detected:
                    self.logger.warning(
                        f"Ethics violation detected: {ethics_decision.boundary_type} - {ethics_decision.explanation}"
                    )

                    # #992 ETHICS-ACTIVATE Phase C: Route the decline through the
                    # conversational floor so Piper composes a voice-appropriate
                    # response instead of emitting a system-error string.
                    # CXO guidance: "the enforcer detects, but Piper speaks."
                    # The raw `explanation` stays audit-only (in intent_data);
                    # only the enforcer's neutral `redirect_context` hint reaches
                    # the floor LLM via FloorContext.
                    from services.intent_service.conversational_floor import (
                        ConversationalFloor,
                        FloorContext,
                    )

                    # Build recent history for continuity in the decline voice
                    # (#1122: shared builder; excludes the in-flight turn)
                    history: List[Dict[str, str]] = build_recent_history(session_id, user_id)

                    floor_ctx = FloorContext(
                        user_message=message,
                        session_id=session_id,
                        user_id=user_id,
                        conversation_history=history,
                        denial_mode=True,
                        denial_category=ethics_decision.boundary_type,
                        redirect_context=ethics_decision.redirect_context,
                    )
                    floor = ConversationalFloor()
                    floor_response = await floor.respond(floor_ctx)

                    # success=True (not False) so downstream conversation flow
                    # treats the decline as a normal turn rather than an error —
                    # the ethics boundary was enforced; the request just doesn't
                    # proceed to intent classification. `ethics_triggered` flag
                    # in intent_data preserves the audit signal for metrics/telemetry.
                    return IntentProcessingResult(
                        success=True,
                        message=floor_response.message,
                        intent_data={
                            "ethics_triggered": True,
                            "boundary_type": ethics_decision.boundary_type,
                            "violation_detected": True,
                            "audit_data": ethics_decision.audit_data,
                            # Legacy name kept for any consumers that read this flag
                            "blocked_by_ethics": True,
                            # Raw explanation preserved for audit, NEVER user-routed
                            "audit_explanation": ethics_decision.explanation,
                        },
                    )

                self.logger.info("Ethics check passed - proceeding with intent processing")

            # Issue #99 CORE-KNOW Phase 2: Knowledge Graph context enhancement
            # Check ENABLE_KNOWLEDGE_GRAPH environment variable (default: False for gradual rollout)
            kg_enabled = os.getenv("ENABLE_KNOWLEDGE_GRAPH", "false").lower() == "true"
            conversation_context = {}

            if kg_enabled:
                try:
                    self.logger.info("Knowledge Graph enhancement enabled - enriching context")
                    conversation_context = await self.kg_integration.enhance_conversation_context(
                        message=message,
                        session_id=session_id,
                        base_context={
                            "source": "intent_service",
                            "timestamp": datetime.now(timezone.utc),
                        },
                    )
                    self.logger.info(
                        "Knowledge Graph context enhancement successful",
                        extra={
                            "kg_concepts": len(
                                conversation_context.get("knowledge_graph", {}).get("concepts", [])
                            ),
                            "kg_patterns": len(
                                conversation_context.get("knowledge_graph", {}).get("patterns", [])
                            ),
                            "kg_entities": len(
                                conversation_context.get("knowledge_graph", {}).get("entities", [])
                            ),
                        },
                    )
                except Exception as e:
                    # Graceful degradation - log error but continue
                    self.logger.error(f"Knowledge Graph enhancement failed: {e}", exc_info=True)
                    conversation_context = {}

            # Issue #595: Multi-intent classification
            # Use classify_multiple to detect all intents in message
            self.logger.info(f"Processing intent: {message}")
            # Issue #852: Pass contextual continuation hint to classifier
            classification_context = (
                {"contextual_continuation_hint": contextual_continuation_hint}
                if contextual_continuation_hint
                else None
            )
            multi_result = await self.intent_classifier.classify_multiple(
                message, context=classification_context
            )

            # Issue #764: Multi-substantive intent orchestration
            # Count substantive (non-conversational) intents
            substantive_count = sum(
                1 for i in multi_result.intents if i.category != IntentCategory.CONVERSATION
            )

            if multi_result.is_multi_intent and substantive_count >= 2:
                # Issue #764: Route to orchestrator for multi-substantive intents
                self.logger.info(
                    "multi_intent_orchestrating",
                    intent_count=len(multi_result.intents),
                    substantive_count=substantive_count,
                    has_greeting=multi_result.has_greeting,
                )
                try:
                    plan = self.intent_orchestrator.create_plan(multi_result)
                    orchestrated = await self.intent_orchestrator.execute_plan(
                        plan, session_id, user_id
                    )
                    orchestrated_result = IntentProcessingResult(
                        success=len(orchestrated.successful_results) > 0,
                        message=orchestrated.aggregated_message,
                        intent_data=orchestrated.primary_intent_data,
                        multi_intent_greeting=orchestrated.greeting_prefix,
                        multi_intent_orchestrated=True,
                        secondary_intents=[
                            {"category": r.intent.category.value, "action": r.intent.action}
                            for r in orchestrated.results[1:]
                        ],
                    )
                    # Issue #819: Apply soft invocation to orchestrated responses
                    return self._apply_soft_offer(
                        orchestrated_result,
                        message,
                        session_id,
                        trust_stage=resolved_trust_stage,
                        user_id=user_id,
                        formality_baseline=formality_baseline,
                    )
                except Exception as e:
                    # Graceful fallback: process primary intent only
                    self.logger.warning(
                        "multi_intent_orchestration_failed",
                        error=str(e),
                        fallback="primary_only",
                    )
                    intent = multi_result.primary_intent
                    if intent is None:
                        intent = await self.intent_classifier.classify(message)

            elif (
                multi_result.is_multi_intent
                and multi_result.has_greeting
                and multi_result.has_substantive_intent
            ):
                # Issue #595: Handle greeting + single substantive intent
                self.logger.info(
                    "multi_intent_handling",
                    intent_count=len(multi_result.intents),
                    has_greeting=True,
                    primary_category=(
                        multi_result.primary_intent.category.value
                        if multi_result.primary_intent
                        else None
                    ),
                )
                # Use primary intent (substantive) for main processing
                # The greeting will be handled via multi_intent context
                intent = multi_result.primary_intent
                # Mark that we detected a greeting so response can include acknowledgment
                if intent.context is None:
                    intent.context = {}
                intent.context["multi_intent_greeting"] = True
                intent.context["secondary_intents"] = [
                    {"category": i.category.value, "action": i.action}
                    for i in multi_result.secondary_intents
                ]
            else:
                # Single intent or all-conversational - use primary
                intent = multi_result.primary_intent
                if intent is None:
                    # No intents detected - fall back to standard classification
                    intent = await self.intent_classifier.classify(message)

            self.logger.info(f"Intent classified as: {intent.category} - {intent.action}")

            # Issue #490: Add user_id to intent context for downstream handlers
            # This enables features like portfolio onboarding that need user context
            self.logger.info(
                "intent_service_user_id_trace",
                user_id_param=user_id,
                intent_category=intent.category.value if intent.category else None,
                intent_action=intent.action,
            )

            # #1124 Phase 3: verb-boundary observability (Arch ruling 2026-06-07).
            self._observe_action_verb(intent, message)

            if user_id:
                if intent.context is None:
                    intent.context = {}
                intent.context["user_id"] = user_id
                self.logger.info(f"Added user_id to intent context: {user_id}")

            # Issue #248: Extract preference detection results from intent
            # Preferences are attached by IntentProcessingHooks during classification
            preferences = getattr(intent, "preferences", None)

            # Issue #300 Phase 1: Learning Handler - Capture Action
            # Store pattern_id for outcome recording
            pattern_id = None
            # Issue #490: Use authenticated user_id if available, otherwise skip learning
            learning_user_id = UUID(user_id) if user_id else None
            try:
                if learning_user_id:
                    async with AsyncSessionFactory.session_scope() as db_session:
                        # Issue #485: Check if user exists before capturing patterns
                        # During fresh install, user may not exist yet - skip learning in that case
                        user_result = await db_session.execute(
                            select(User.id).where(User.id == str(learning_user_id))
                        )
                        user_exists = user_result.scalar_one_or_none() is not None

                        if not user_exists:
                            self.logger.info(
                                "Learning Handler: Skipping capture - user not found",
                                user_id=str(learning_user_id),
                            )
                        else:
                            pattern_id = await self.learning_handler.capture_action(
                                user_id=learning_user_id,
                                action_type=intent.category,
                                context={"intent": intent.action, "message": message[:100]},
                                session=db_session,
                            )

                            self.logger.info(
                                "Learning Handler: Action captured",
                                pattern_id=str(pattern_id) if pattern_id else None,
                                action_type=intent.category.value,
                            )
            except Exception as e:
                self.logger.error(f"Learning Handler: Capture failed: {e}")
                # Continue processing even if learning fails

            # Issue #300 Phase 3: Get pattern suggestions
            # Issue #490: Only fetch suggestions if we have an authenticated user
            suggestions = None
            try:
                if learning_user_id:
                    async with AsyncSessionFactory.session_scope() as db_session:
                        suggestions = await self.learning_handler.get_suggestions(
                            user_id=learning_user_id,
                            context={"intent": intent.action, "message": message[:100]},
                            session=db_session,
                        )

                        self.logger.info(
                            "Learning Handler: Suggestions retrieved",
                            suggestion_count=len(suggestions) if suggestions else 0,
                        )
            except Exception as e:
                self.logger.error(f"Learning Handler: Get suggestions failed: {e}")
                # Continue processing even if suggestions fail
                suggestions = None

            # Issue #300 Phase 4: Get proactive automation patterns
            # Issue #490: Only fetch patterns if we have an authenticated user
            automation_patterns = []
            try:
                if learning_user_id:
                    async with AsyncSessionFactory.session_scope() as db_session:
                        # Build context for matching
                        current_context = {
                            "intent": intent.category.value.upper(),  # Match against category (EXECUTION, QUERY, etc.)
                            "message": message[:100],
                            # Note: Don't pass None values - context matcher expects strings or missing keys
                        }

                        patterns = await self.learning_handler.get_automation_patterns(
                            user_id=learning_user_id,
                            context=current_context,
                            min_confidence=0.9,
                            limit=3,
                            session=db_session,
                        )

                        # Convert LearnedPattern objects to suggestion format with auto_triggered flag
                        for pattern in patterns:
                            automation_patterns.append(
                                {
                                    "pattern_id": str(pattern.id),
                                    "confidence": round(pattern.confidence, 2),
                                    "pattern_type": pattern.pattern_type.value,
                                    "pattern_data": pattern.pattern_data,
                                    "usage_count": pattern.usage_count,
                                    "auto_triggered": True,  # Mark as proactive
                                }
                            )

                        self.logger.info(
                            "Learning Handler: Automation patterns retrieved",
                            pattern_count=len(automation_patterns),
                        )
            except Exception as e:
                self.logger.error(f"Learning Handler: Get automation patterns failed: {e}")
                # Continue processing even if automation patterns fail
                automation_patterns = []

            # Combine regular suggestions with automation patterns (Bug #86n: deduplicate)
            if suggestions is None:
                suggestions = []

            # Deduplicate by pattern_id, preferring automation_patterns (auto_triggered=True)
            seen_pattern_ids = set()
            all_suggestions = []

            # Add automation patterns first (higher priority)
            for pattern in automation_patterns:
                pattern_id = pattern.get("pattern_id")
                if pattern_id and pattern_id not in seen_pattern_ids:
                    all_suggestions.append(pattern)
                    seen_pattern_ids.add(pattern_id)

            # Add regular suggestions only if not already seen
            for suggestion in suggestions:
                pattern_id = suggestion.get("pattern_id")
                if pattern_id and pattern_id not in seen_pattern_ids:
                    all_suggestions.append(suggestion)
                    seen_pattern_ids.add(pattern_id)

            self.logger.debug(
                f"Suggestion deduplication: {len(automation_patterns)} auto + {len(suggestions)} regular → {len(all_suggestions)} unique"
            )

            # Issue #1195: flag-gated autonomous execution of the high-confidence
            # automation patterns. Read-only by construction (see the method's
            # docstring); no-op unless AUTONOMOUS_EXECUTION_ENABLED=true and a
            # SAFE >= 0.9 pattern matched. Side effects only (execution + audit +
            # log); user-facing surfacing = #1174, mutating + rollback = #1209.
            await self._maybe_autoexecute_automation_patterns(
                automation_patterns, session_id, user_id
            )

            # Issue #911 Phase 2: Action Gate — decides BEFORE execution whether
            # the canonical handler is needed or the floor should handle it.
            #
            # Architecture:
            #   Classifier → Action Gate
            #     ├── Operation LLM cannot perform? → Canonical/Workflow Handler
            #     ├── Pre-classifier high-confidence + deterministic? → Fast-path canonical
            #     └── Everything else → Context Assembler → Floor
            if self._should_route_to_floor(intent):
                # Floor with context assembly
                result = await self._handle_floor_with_context(
                    intent,
                    session_id,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                    trust_stage=resolved_trust_stage,
                )
                result.suggestions = all_suggestions
                result.preferences = preferences
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # Issue #286: Handle canonical intents (PORTFOLIO, EXECUTION, STATUS, etc.)
            # Issue #911 Phase 2: Only reaches here for categories that passed through
            # the Action Gate (_requires_canonical_handler returned True).
            if self.canonical_handlers.can_handle(intent):
                # Issue #582: Pass user_id to enable database project lookup
                canonical_result = await self.canonical_handlers.handle(intent, session_id, user_id)

                # Issue #907: Safety net — detect generic template responses from canonical
                # handlers and fall back to floor on generic response.
                # Note: As of #925 (Apr 13), STATUS/PRIORITY/TEMPORAL are floor-routed.
                # Remaining canonical: TEMPORAL-date, GUIDANCE-setup, PORTFOLIO, CONVERSATION-greeting.
                # Issue #908: Now checks structural flag first, then signature fallback.
                response_message = canonical_result["message"]
                if self._is_generic_canonical_response(canonical_result, response_message):
                    self.logger.info(
                        "canonical_generic_detected_routing_to_floor",
                        category=intent.category.value,
                        action=intent.action,
                        original_message=intent.original_message,
                    )
                    result = await self._handle_unknown_intent(
                        intent,
                        None,
                        session_id,
                        user_id=user_id,
                        formality_baseline=formality_baseline,
                        trust_stage=resolved_trust_stage,
                    )
                    result.suggestions = all_suggestions
                    result.preferences = preferences
                    return self._apply_soft_offer(
                        result,
                        message,
                        session_id,
                        trust_stage=resolved_trust_stage,
                        user_id=user_id,
                        formality_baseline=formality_baseline,
                    )

                # Issue #595: Add greeting prefix if multi-intent with greeting detected
                multi_intent_greeting = (
                    intent.context.get("multi_intent_greeting", False) if intent.context else False
                )
                if multi_intent_greeting:
                    # Prepend friendly greeting acknowledgment to substantive response
                    response_message = f"Hi there! {response_message}"
                    self.logger.info(
                        "multi_intent_greeting_added",
                        original_length=len(canonical_result["message"]),
                    )

                # Issue #846: Register embedded offers as pending offers
                # When canonical handlers return responses with "Would you like..." questions,
                # register them so user's "yes"/"no" response gets matched correctly.
                if canonical_result.get("action_required"):
                    _action_to_workflow = {
                        "configure_priorities": "priority_check",
                        "configure_projects": "project_setup",
                        "setup_piper_config": "setup",
                    }
                    _wf_type = _action_to_workflow.get(
                        canonical_result["action_required"],
                        canonical_result["action_required"],
                    )
                    self.workflow_offer_service.set_pending_offer(
                        session_id,
                        {
                            "workflow_type": _wf_type,
                            "action_required": canonical_result["action_required"],
                        },
                        user_id=user_id,
                    )

                # Issue #852: Track contextual offer for continuation detection
                # Complements action_required (line 864) — different storage, same location.
                # action_required → WorkflowOfferService (triggers workflows)
                # offer_hint → ConversationContext.last_offer (gives LLM context)
                offer_hint = canonical_result.get("offer_hint")
                if offer_hint and session_id:
                    from services.intent_service.conversation_context import (
                        LastOffer,
                        get_or_create_context,
                    )

                    try:
                        conv_ctx = get_or_create_context(session_id)
                    except (ValueError, KeyError):
                        conv_ctx = None  # Non-UUID session_id — skip offer tracking
                    if conv_ctx:
                        conv_ctx.last_offer = LastOffer(
                            offer_type="contextual",
                            continuation_hint=offer_hint["continuation_hint"],
                            offer_text=offer_hint.get("offer_text", ""),
                        )
                        self.logger.info(
                            "contextual_offer_tracked",
                            continuation_hint=offer_hint["continuation_hint"],
                            session_id=session_id,
                        )

                canonical_response = IntentProcessingResult(
                    success=True,
                    message=response_message,
                    intent_data=canonical_result["intent"],
                    requires_clarification=canonical_result.get("requires_clarification", False),
                    suggestions=all_suggestions,
                    preferences=preferences,  # Issue #248: Attach preference detection results
                    # Issue #595: Multi-intent tracking
                    multi_intent_greeting=multi_intent_greeting,
                    secondary_intents=(
                        intent.context.get("secondary_intents") if intent.context else None
                    ),
                )
                # Issue #767: Check for soft invocation opportunity
                return self._apply_soft_offer(
                    canonical_response,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # Issue #883 + #1094: workflows are no longer pre-created. Handlers
            # that previously consumed workflow_id pass None through harmlessly.
            workflow = None
            workflow_id = None  # For fallback error path

            # ── #1124 action-dispatch rail (ADR-059) ─────────────────────────
            # If the classified action maps to a registered action-triggered
            # workflow, dispatch it through the workflow registry instead of a
            # hand-coded `elif intent.action in [...]` chain below. This is the
            # shared rail that lets pre-floor handlers migrate off the switch one
            # at a time. A None return (unknown type / handler error) falls
            # through to normal category routing — the safe default.
            from services.intent_service.workflow_dispatcher import (
                dispatch_workflow,
                get_action_workflows,
            )

            if intent.action in get_action_workflows():
                dispatched = await dispatch_workflow(
                    workflow_type=intent.action,
                    session_id=session_id,
                    user_id=user_id,
                    context={
                        "intent": intent,
                        "workflow_id": workflow_id,
                        "intent_service": self,
                    },
                )
                if dispatched is not None:
                    dispatched.suggestions = all_suggestions
                    # Issue #248: Attach preference detection results
                    dispatched.preferences = preferences
                    # Issue #844: Apply soft invocation to all handler paths
                    return self._apply_soft_offer(
                        dispatched,
                        message,
                        session_id,
                        trust_stage=resolved_trust_stage,
                        user_id=user_id,
                        formality_baseline=formality_baseline,
                    )

            # Handle QUERY intents with domain services
            # Issue #586: Pass user_id for timezone-aware calendar queries
            if intent.category.value.upper() == "QUERY":
                result = await self._handle_query_intent(intent, workflow, session_id, user_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 1: Handle EXECUTION intents with domain services
            if intent.category.value.upper() == "EXECUTION":
                result = await self._handle_execution_intent(intent, workflow, session_id, user_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 2: Handle ANALYSIS intents with domain services
            if intent.category.value.upper() == "ANALYSIS":
                result = await self._handle_analysis_intent(intent, workflow, session_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 4: Handle SYNTHESIS intents
            if intent.category.value.upper() == "SYNTHESIS":
                result = await self._handle_synthesis_intent(intent, workflow, session_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 5: Handle STRATEGY intents
            if intent.category.value.upper() == "STRATEGY":
                result = await self._handle_strategy_intent(intent, workflow, session_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 6: Handle LEARNING intents
            if intent.category.value.upper() == "LEARNING":
                result = await self._handle_learning_intent(intent, workflow, session_id)
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # GREAT-4D Phase 7: Handle UNKNOWN intents via conversational floor (#907)
            if intent.category.value.upper() == "UNKNOWN":
                result = await self._handle_unknown_intent(
                    intent,
                    workflow,
                    session_id,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                    trust_stage=resolved_trust_stage,
                )
                result.suggestions = all_suggestions
                result.preferences = preferences  # Issue #248: Attach preference detection results
                # Issue #844: Apply soft invocation to all handler paths
                return self._apply_soft_offer(
                    result,
                    message,
                    session_id,
                    trust_stage=resolved_trust_stage,
                    user_id=user_id,
                    formality_baseline=formality_baseline,
                )

            # Fallback for truly unhandled categories (should never reach here)
            result = IntentProcessingResult(
                success=False,
                message=f"Unhandled intent category: {intent.category.value}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow_id,
                error=f"No handler for category: {intent.category.value}",
                error_type="UnhandledCategoryError",
                suggestions=suggestions,
                preferences=preferences,  # Issue #248: Attach preference detection results
            )

            # Issue #300 Phase 1: Learning Handler - Record Outcome
            # Issue #490: Only record outcome if we have an authenticated user
            if pattern_id and learning_user_id:
                try:
                    async with AsyncSessionFactory.session_scope() as db_session:
                        success = await self.learning_handler.record_outcome(
                            user_id=learning_user_id,
                            pattern_id=pattern_id,
                            success=result.success,
                            session=db_session,
                        )

                        self.logger.info(
                            "Learning Handler: Outcome recorded",
                            pattern_id=str(pattern_id),
                            success=result.success,
                            outcome_recorded=success,
                        )
                except Exception as e:
                    self.logger.error(f"Learning Handler: Outcome recording failed: {e}")

            # Issue #899: Prepend off-topic pause message if process was auto-paused
            if off_topic_prefix and result.message:
                result = IntentProcessingResult(
                    success=result.success,
                    message=f"{off_topic_prefix}\n\n{result.message}",
                    intent_data=result.intent_data,
                    workflow_id=result.workflow_id,
                    requires_clarification=result.requires_clarification,
                )

            return result

        except Exception as e:
            self.logger.error(f"Intent processing error: {e}")
            raise IntentProcessingError(f"Intent processing failed: {str(e)}")

    async def _check_active_guided_process(
        self, user_id: str, session_id: str, message: str
    ) -> tuple[Optional[IntentProcessingResult], Optional[str]]:
        """
        ADR-049: Check for active guided processes before intent classification.

        Uses the ProcessRegistry to check all registered guided processes
        in priority order. First active process that claims the message wins.

        Guided processes include: onboarding, standup, planning, feedback, etc.

        Issue #899: Returns a tuple of (result, off_topic_prefix). When off-topic
        detection triggers, result is None (proceed with normal processing) and
        off_topic_prefix contains the pause message to prepend to the response.

        Args:
            user_id: Authenticated user ID
            session_id: Session identifier
            message: User's message

        Returns:
            Tuple of (IntentProcessingResult or None, off_topic_prefix or None)
        """
        try:
            registry = get_process_registry()
            result = await registry.check_active_processes(user_id, session_id, message)

            # Issue #899: Off-topic pause — process was suspended but message
            # should go through normal intent processing
            if not result.handled and result.escaped and result.response_message:
                self.logger.info(
                    "Off-topic detected, process paused, continuing to intent processing",
                    process_type=result.process_type.value if result.process_type else None,
                    user_id=user_id,
                )
                return None, result.response_message

            if result.handled:
                self.logger.info(
                    "Message handled by guided process",
                    process_type=result.process_type.value if result.process_type else None,
                    user_id=user_id,
                    session_id=session_id,
                )

                # ADR-059: Onboarding completion check removed (onboarding on ice).
                # Was: persist captured projects when onboarding completes.

                return (
                    IntentProcessingResult(
                        success=True,
                        message=result.response_message or "",
                        intent_data=result.intent_data,
                        workflow_id=None,
                        requires_clarification=False,
                    ),
                    None,
                )

            return None, None

        except Exception as e:
            self.logger.warning(f"Could not check active guided processes: {e}")
            return None, None

    async def _check_pending_onboarding_offer(
        self, user_id: str, message: str
    ) -> Optional[IntentProcessingResult]:
        """
        Issue #888: Check for pending onboarding offer (OFFERED state).

        After the offer-first activation model, the user may have been
        offered onboarding on the previous turn. If they respond, we
        need to route that response to handle_offer_response() before
        normal classification runs.

        Returns IntentProcessingResult if the offer was handled, None otherwise.
        """
        try:
            from services.conversation.conversation_handler import _get_onboarding_components
            from services.shared_types import PortfolioOnboardingState

            manager, handler = _get_onboarding_components()
            session = manager.get_session_by_user(user_id)

            if not session or session.state != PortfolioOnboardingState.OFFERED:
                return None

            self.logger.info(
                "Checking pending onboarding offer response",
                user_id=user_id,
                session_id=session.id,
            )

            response = handler.handle_offer_response(session.id, message)

            if response is None:
                # Implicit decline — user ignored the offer
                # Return None so message goes through normal classification
                return None

            return IntentProcessingResult(
                success=True,
                message=response.message,
                intent_data={
                    "category": "guidance",
                    "action": "portfolio_onboarding",
                    "confidence": 1.0,
                    "context": {
                        "onboarding_id": session.id,
                        "state": response.state.value,
                    },
                },
                workflow_id=None,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.warning(f"Could not check pending onboarding offer: {e}")
            return None

    async def _check_pending_resume_offer(
        self, user_id: str, session_id: str, message: str
    ) -> Optional[IntentProcessingResult]:
        """
        Issue #889: Check if user is responding to a suspended session resume offer.

        After _check_suspended_session_reentry() offers to resume a suspended
        session, the user's next message may be accepting or declining.
        This method catches those responses before normal classification.

        Accept signals: "yes", "continue", "resume", "sure", "ok", "pick it up"
        Decline signals: "no", "fresh", "start over", "new", "nah", "skip"
        Anything else: Not a response to the offer, proceed with normal classification.

        Returns IntentProcessingResult if the offer was handled, None otherwise.
        """
        try:
            registry = get_process_registry()
            suspended = await registry.check_suspended_processes(user_id)

            if suspended is None:
                return None

            # Determine if user is responding to resume offer
            msg_lower = message.strip().lower()

            # Accept signals
            accept_signals = frozenset(
                {
                    "yes",
                    "yeah",
                    "yep",
                    "sure",
                    "ok",
                    "okay",
                    "continue",
                    "resume",
                    "pick it up",
                    "let's continue",
                    "yes please",
                    "y",
                    "yea",
                }
            )
            # Decline signals
            decline_signals = frozenset(
                {
                    "no",
                    "nah",
                    "nope",
                    "fresh",
                    "start over",
                    "start fresh",
                    "new",
                    "skip",
                    "no thanks",
                    "n",
                }
            )

            if msg_lower in accept_signals:
                # Resume the suspended session
                self.logger.info(
                    "User accepted resume offer",
                    user_id=user_id,
                    process_type=suspended.process_type.value,
                )

                if suspended.process_type == ProcessType.STANDUP:
                    return await self._resume_suspended_standup(user_id, session_id)
                # ADR-059: Onboarding resume disabled (onboarding on ice)

            elif msg_lower in decline_signals:
                # Abandon the suspended session
                self.logger.info(
                    "User declined resume offer",
                    user_id=user_id,
                    process_type=suspended.process_type.value,
                )

                if suspended.process_type == ProcessType.STANDUP:
                    return await self._abandon_suspended_standup(user_id)
                # ADR-059: Onboarding abandon disabled (onboarding on ice)

            # Not a response to the resume offer — let normal classification handle it.
            # The suspended session stays as-is for next greeting re-entry.
            return None

        except Exception as e:
            self.logger.warning(f"Could not check pending resume offer: {e}")
            return None

    async def _resume_suspended_standup(
        self, user_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Issue #889: Resume a suspended standup conversation.

        Transitions SUSPENDED → INITIATED so the ProcessRegistry will route
        subsequent messages to the standup handler.
        """
        from services.conversation.conversation_handler import _get_standup_components
        from services.shared_types import StandupConversationState
        from services.standup.conversation_handler import (
            _RESUME_PROMPTS,
            _format_capture_replay,
            _next_uncaptured_part_state,
        )

        manager, handler = _get_standup_components()

        # Find the suspended conversation for this user
        conv = await manager.get_conversation_by_user(user_id, include_suspended=True)

        if not conv or conv.state != StandupConversationState.SUSPENDED:
            return IntentProcessingResult(
                success=True,
                message="I couldn't find the paused standup. Want to start a fresh one with /standup?",
                intent_data={
                    "category": "guidance",
                    "action": "suspended_session_resume_failed",
                    "confidence": 1.0,
                    "context": {"user_id": user_id},
                },
                workflow_id=None,
                requires_clarification=False,
            )

        # #900 Phase 4: Resume protocol. Two paths:
        # - 3-part flow with partial capture → land directly at the next
        #   uncaptured part, replay what was captured, ask the next question.
        # - Legacy flow (no partial capture, has current_standup) →
        #   continue at INITIATED with the existing refinement message.
        partial = conv.partial_capture
        previous_state = conv.previous_state
        in_three_part_flow = previous_state in (
            StandupConversationState.GATHERING_YESTERDAY,
            StandupConversationState.GATHERING_TODAY,
            StandupConversationState.GATHERING_BLOCKERS,
        )

        if in_three_part_flow and partial is not None:
            next_state = _next_uncaptured_part_state(partial)
            await manager.transition_state(conv.id, next_state)
            conv = await manager.bind_session_id(conv.id, session_id)

            replay = _format_capture_replay(partial)
            prompt = _RESUME_PROMPTS[next_state]
            if replay:
                resume_msg = (
                    f"Picking back up — here's what you'd already captured:\n\n"
                    f"{replay}\n\n{prompt}"
                )
            else:
                resume_msg = f"Picking back up. {prompt}"

            return IntentProcessingResult(
                success=True,
                message=resume_msg,
                intent_data={
                    "category": "execution",
                    "action": "standup_conversation_resumed",
                    "confidence": 1.0,
                    "context": {
                        "conversation_id": conv.id,
                        "state": conv.state.value,
                        "resumed": True,
                        "resume_part": next_state.value,
                        "guided_process": ProcessType.STANDUP.value,
                    },
                },
                workflow_id=None,
                requires_clarification=False,
            )

        # Legacy resume path (pre-#900 flow): SUSPENDED → INITIATED
        await manager.transition_state(conv.id, StandupConversationState.INITIATED)
        conv = await manager.bind_session_id(conv.id, session_id)

        resume_msg = "Great, let's pick up where we left off! "
        if conv.current_standup:
            resume_msg += (
                f"Here's what we had so far:\n\n{conv.current_standup}\n\n"
                "Would you like to continue refining this, or start fresh?"
            )
        else:
            resume_msg += "What would you like to include in your standup today?"

        return IntentProcessingResult(
            success=True,
            message=resume_msg,
            intent_data={
                "category": "execution",
                "action": "standup_conversation_resumed",
                "confidence": 1.0,
                "context": {
                    "conversation_id": conv.id,
                    "state": conv.state.value,
                    "resumed": True,
                    "guided_process": ProcessType.STANDUP.value,
                },
            },
            workflow_id=None,
            requires_clarification=False,
        )

    async def _abandon_suspended_standup(self, user_id: str) -> IntentProcessingResult:
        """
        Issue #889: Abandon a suspended standup conversation.

        User declined to resume. Transition SUSPENDED → ABANDONED.
        """
        from services.conversation.conversation_handler import _get_standup_components
        from services.shared_types import StandupConversationState

        manager, _ = _get_standup_components()
        conv = await manager.get_conversation_by_user(user_id, include_suspended=True)

        if conv and conv.state == StandupConversationState.SUSPENDED:
            await manager.transition_state(conv.id, StandupConversationState.ABANDONED)

        return IntentProcessingResult(
            success=True,
            message="No problem! The paused standup has been cleared. Just say /standup when you're ready for a new one.",
            intent_data={
                "category": "guidance",
                "action": "suspended_session_declined",
                "confidence": 1.0,
                "context": {
                    "user_id": user_id,
                    "process_type": ProcessType.STANDUP.value,
                },
            },
            workflow_id=None,
            requires_clarification=False,
        )

    async def _resume_suspended_onboarding(
        self, user_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Issue #889: Resume a suspended onboarding session.

        Transitions SUSPENDED → INITIATED so the ProcessRegistry will route
        subsequent messages to the onboarding handler.
        """
        from services.conversation.conversation_handler import _get_onboarding_components
        from services.shared_types import PortfolioOnboardingState

        manager, handler = _get_onboarding_components()
        session = manager.get_session_by_user(user_id)

        if not session or session.state != PortfolioOnboardingState.SUSPENDED:
            return IntentProcessingResult(
                success=True,
                message="I couldn't find the paused setup. Want to start fresh? Just say 'help me set up'.",
                intent_data={
                    "category": "guidance",
                    "action": "suspended_session_resume_failed",
                    "confidence": 1.0,
                    "context": {"user_id": user_id},
                },
                workflow_id=None,
                requires_clarification=False,
            )

        # Transition back to INITIATED
        manager.transition_state(session.id, PortfolioOnboardingState.INITIATED)

        resume_msg = "Great, let's continue setting up your workspace! Tell me about your projects."

        return IntentProcessingResult(
            success=True,
            message=resume_msg,
            intent_data={
                "category": "guidance",
                "action": "portfolio_onboarding_resumed",
                "confidence": 1.0,
                "context": {
                    "onboarding_id": session.id,
                    "state": session.state.value,
                    "resumed": True,
                    "guided_process": ProcessType.ONBOARDING.value,
                },
            },
            workflow_id=None,
            requires_clarification=False,
        )

    async def _abandon_suspended_onboarding(self, user_id: str) -> IntentProcessingResult:
        """
        Issue #889: Abandon a suspended onboarding session.

        User declined to resume. Transition SUSPENDED → DECLINED.
        """
        from services.conversation.conversation_handler import _get_onboarding_components
        from services.shared_types import PortfolioOnboardingState

        manager, _ = _get_onboarding_components()
        session = manager.get_session_by_user(user_id)

        if session and session.state == PortfolioOnboardingState.SUSPENDED:
            manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)

        return IntentProcessingResult(
            success=True,
            message="No problem! You can set up your workspace anytime by saying 'help me set up'.",
            intent_data={
                "category": "guidance",
                "action": "suspended_session_declined",
                "confidence": 1.0,
                "context": {
                    "user_id": user_id,
                    "process_type": ProcessType.ONBOARDING.value,
                },
            },
            workflow_id=None,
            requires_clarification=False,
        )

    async def _check_active_onboarding(
        self, user_id: str, session_id: str, message: str
    ) -> Optional[IntentProcessingResult]:
        """
        Issue #490/#560: Check for active onboarding session and route message directly.

        Active conversational processes (like onboarding) take priority over intent
        classification. This prevents guided conversations from being derailed by
        messages that happen to match other intent patterns.

        Design principle: Once the user agrees to participate in a guided process,
        Piper should maintain control of the conversation until:
        - The process completes successfully
        - The user explicitly declines/exits
        - The session times out

        Args:
            user_id: Authenticated user ID
            session_id: Session identifier
            message: User's message

        Returns:
            IntentProcessingResult if active onboarding handled the message,
            None if no active onboarding (proceed with normal classification)
        """
        try:
            from services.conversation.conversation_handler import _get_onboarding_components
            from services.shared_types import IntentCategory, PortfolioOnboardingState

            # Issue #490: Use the SAME singleton manager as conversation_handler
            # Creating a new PortfolioOnboardingManager() would lose session state!
            manager, handler = _get_onboarding_components()

            # Issue #490: Check for active session by user_id (preferred) or session_id (fallback)
            # This ensures onboarding works even when user is not authenticated
            session = None
            if user_id:
                session = manager.get_session_by_user(user_id)
            if not session and session_id:
                session = manager.get_session_by_session_id(session_id)

            if not session:
                return None

            # Check if session is in a terminal state
            if session.state in (
                PortfolioOnboardingState.COMPLETE,
                PortfolioOnboardingState.DECLINED,
            ):
                return None

            # Active onboarding session exists - route message directly to handler
            self.logger.info(
                "Routing to active onboarding session",
                user_id=user_id,
                onboarding_id=session.id,
                state=session.state.value,
            )

            response = handler.handle_turn(session.id, message)

            # If onboarding completed, persist the projects
            if response.is_complete and response.state == PortfolioOnboardingState.COMPLETE:
                await self._persist_onboarding_projects(user_id, response.captured_projects)

            return IntentProcessingResult(
                success=True,
                message=response.message,
                intent_data={
                    "category": IntentCategory.GUIDANCE.value,
                    "action": "portfolio_onboarding",
                    "confidence": 1.0,
                    "context": {
                        "onboarding_id": session.id,
                        "state": response.state.value,
                        "bypassed_classification": True,  # Indicates we skipped intent classification
                    },
                },
                workflow_id=None,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.warning(f"Could not check active onboarding: {e}")
            return None

    async def _check_active_standup(
        self, user_id: str, session_id: str, message: str
    ) -> Optional[IntentProcessingResult]:
        """
        Issue #585: Check for active standup conversation and route message directly.

        DEPRECATED (Issue #889): This method is superseded by the ProcessRegistry
        (ADR-049) which handles all guided process routing via
        _check_active_guided_process(). Retained for backward compatibility with
        tests in test_standup_routing_585.py that verify its existence.

        The ProcessRegistry + StandupProcessAdapter now handle:
        - Active session detection (check_active)
        - Message routing (handle_message)
        - Escape command interception (#888)
        - Timeout auto-suspend (#888)
        """
        try:
            from services.conversation.conversation_handler import _get_standup_components
            from services.shared_types import IntentCategory, StandupConversationState

            manager, handler = _get_standup_components()

            conversation = None
            if session_id:
                conversation = await manager.get_conversation_by_session(session_id)

            if not conversation:
                return None

            if conversation.state in (
                StandupConversationState.COMPLETE,
                StandupConversationState.ABANDONED,
                StandupConversationState.SUSPENDED,
            ):
                return None

            self.logger.info(
                "Legacy _check_active_standup routing to active standup",
                user_id=user_id,
                conversation_id=conversation.id,
                state=conversation.state.value,
            )

            response = await handler.handle_turn(conversation, message)

            return IntentProcessingResult(
                success=True,
                message=response.message,
                intent_data={
                    "category": IntentCategory.EXECUTION.value,
                    "action": "standup_conversation_turn",
                    "confidence": 1.0,
                    "context": {
                        "conversation_id": conversation.id,
                        "state": response.state.value,
                        "bypassed_classification": True,
                    },
                },
                workflow_id=None,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.warning(f"Could not check active standup: {e}")
            return None

    async def _start_standup_conversation(
        self, user_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Issue #585: Start a new interactive standup conversation.

        This method is called when the user sends /standup command.
        It creates a new conversation via StandupConversationHandler.

        Args:
            user_id: Authenticated user ID
            session_id: Session identifier

        Returns:
            IntentProcessingResult with the initial conversation greeting
        """
        try:
            from services.conversation.conversation_handler import _get_standup_components
            from services.shared_types import IntentCategory, StandupConversationState

            manager, handler = _get_standup_components()

            # Check for existing active conversation
            existing = await manager.get_conversation_by_session(session_id) if session_id else None
            if existing and existing.state not in (
                StandupConversationState.COMPLETE,
                StandupConversationState.ABANDONED,
            ):
                # Active session exists - offer to continue or restart
                response_msg = (
                    "You have a standup conversation in progress. "
                    "Would you like to continue where you left off, or start fresh?\n"
                    "Reply 'continue' or 'restart'."
                )
                return IntentProcessingResult(
                    success=True,
                    message=response_msg,
                    intent_data={
                        "category": IntentCategory.EXECUTION.value,
                        "action": "standup_session_exists",
                        "confidence": 1.0,
                        "context": {
                            "conversation_id": existing.id,
                            "state": existing.state.value,
                        },
                    },
                    workflow_id=None,
                    requires_clarification=False,
                )

            # Start new standup conversation
            response = await handler.start_conversation(
                session_id=session_id,
                user_id=user_id,
            )

            self.logger.info(
                "Started interactive standup conversation",
                user_id=user_id,
                session_id=session_id,
                state=response.state.value,
            )

            return IntentProcessingResult(
                success=True,
                message=response.message,
                intent_data={
                    "category": IntentCategory.EXECUTION.value,
                    "action": "standup_started",
                    "confidence": 1.0,
                    "context": {
                        "state": response.state.value,
                        "requires_input": response.requires_input,
                        "suggestions": response.suggestions,
                    },
                },
                workflow_id=None,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to start standup conversation: {e}")
            return IntentProcessingResult(
                success=False,
                message="Unable to start standup conversation. Please try again.",
                intent_data={
                    "category": "EXECUTION",
                    "action": "standup_error",
                    "confidence": 1.0,
                },
                error=str(e),
                error_type="StandupConversationError",
            )

    async def _persist_onboarding_projects(self, user_id: str, captured_projects: list) -> None:
        """
        Issue #490: Persist captured projects from onboarding to database.

        Called when onboarding completes successfully.
        """
        if not captured_projects:
            return

        try:
            from services.database.repositories import ProjectRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as db_session:
                project_repo = ProjectRepository(db_session)
                for project_info in captured_projects:
                    await project_repo.create(
                        name=project_info.get("name", "Unnamed Project"),
                        description=project_info.get("description", ""),
                        owner_id=user_id,
                        is_default=project_info.get("is_default", False),
                    )
                await db_session.commit()

            self.logger.info(
                "Onboarding projects persisted",
                user_id=user_id,
                project_count=len(captured_projects),
            )

            # Issue #838: Persist onboarding formality baseline to user preferences
            # Currently warmth_level defaults to 0.8 (warm) during onboarding.
            # When a formality selection step is added, this wiring will carry
            # the user's chosen tier through to PersonalityProfile.
            try:
                from services.personality.formality import ONBOARDING_TIER_TO_WARMTH

                async with AsyncSessionFactory.session_scope() as pref_session:
                    user_result = await pref_session.execute(select(User).where(User.id == user_id))
                    user = user_result.scalar_one_or_none()
                    if user:
                        prefs = user.preferences or {}
                        # Default onboarding warmth = 0.8 → "warm" tier → "detailed" communication
                        prefs["communication_style"] = prefs.get("communication_style", "detailed")
                        user.preferences = prefs
                        await pref_session.commit()
                        self.logger.info(
                            "onboarding_formality_persisted",
                            user_id=user_id,
                            communication_style=prefs["communication_style"],
                        )
            except Exception as pref_err:
                self.logger.warning(f"Formality persistence failed: {pref_err}")

        except Exception as e:
            self.logger.error(f"Failed to persist onboarding projects: {e}")
            # Don't raise - onboarding message was still delivered

    async def _handle_query_intent(
        self, intent: Intent, workflow, session_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle QUERY category intents (standup, projects, generic).

        Routes to appropriate domain service based on intent action.
        Issue #516: Added document search routing to Notion
        Issue #586: Added user_id parameter for timezone-aware calendar queries
        Issue #883: workflow may be None (lazy creation)
        """
        self.logger.info(f"Processing QUERY intent: {intent.action}")
        # Issue #883: Extract workflow_id safely (None when no async work needed)
        workflow_id = getattr(workflow, "id", None)

        # #1124: the entire QUERY-category dispatch chain now routes through the
        # action-dispatch rail in process_intent (workflow registry), NOT a hand-coded
        # elif chain. Migrated cohorts (handlers all reused UNCHANGED by their
        # registered entry points in workflow_entries.py):
        #   • update_document → run_update_document_workflow
        #   • issue-mutation (close/reopen/comment) → run_{close,reopen,comment}_issue_workflow
        #   • GitHub read-query (shipped/stale_prs/review_issue/list_*) → _READ_QUERY_COHORT
        #   • calendar (meeting_time/recurring_meetings/week_calendar) → _CALENDAR_QUERY_COHORT
        #   • changes_query → run_changes_query_workflow
        #   • this QUERY cohort (search_documents/local_git_status/productivity/attention/
        #     todos/standup/list_projects) → _query_cohort (per-handler arity via factory flags;
        #     todos delegates to the EXECUTION handler via run_todo_query_workflow)
        # The rail short-circuits before this routing; anything without a rail entry
        # falls through to the generic query handler (which itself floors the unknown case).
        return await self._handle_generic_query(intent, workflow_id, session_id)

    @staticmethod
    def _is_standup_query(message: str) -> bool:
        """#1269: detect a request for the on-demand DERIVED standup ("give me my standup",
        "what's my standup", "show my standup") so it routes to the StandupAssembler rather
        than the LLM classifier (which conflates standup with get_project_status — verified
        2026-06-18). Deterministic + unit-testable. Does NOT match the interactive `/standup`
        command (handled separately) or incidental mentions ("how do I run a standup meeting")."""
        m = " ".join(message.strip().lower().rstrip("?!.").split())
        if "standup" not in m or m.startswith("/"):
            return False
        cues = (
            "my standup",  # give me / show / what's / see / get … my standup
            "standup please",
            "today's standup",
            "todays standup",
            "standup for today",
            "give me the standup",
            "show me the standup",
            "me the standup",
        )
        return any(cue in m for cue in cues)

    async def _handle_standup_query(
        self, intent: Intent, workflow_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """Handle show_standup/get_standup query actions — the on-demand standup DERIVED
        over the live entity catalog (#1269: StandupAssembler reading the same Radar
        EntitySources + calendar), replacing the hollow source:"fallback" path. This is the
        QUERY/on-demand surface; the interactive ``/standup`` capture flow
        (StandupConversationHandler, #585) is a separate path and is untouched.

        Scopes to the authenticated ``user_id`` (``current_user.sub`` — the SAME identity
        Radar uses), threaded via the dispatch rail's ``pass_user_id=True``. NOT the
        session_id — the standup is the user's, not the session's. Anonymous (``user_id``
        None) → the sources degrade to an honest empty summary.
        """
        try:
            from services.standup.assembler import build_user_standup_summary

            summary = await build_user_standup_summary(user_id)

            return IntentProcessingResult(
                success=True,
                message=f"Good morning! {summary.to_prose()}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {"standup_data": summary.to_dict()},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )
        except Exception as e:
            self.logger.error(f"Standup generation error: {e}")
            return IntentProcessingResult(
                success=True,  # Still success, just degraded
                message="Unable to generate standup at this time. Please try again later.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

    async def _handle_projects_query(
        self, intent: Intent, workflow_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle list_projects/show_projects query actions.

        Issue #1102 (Pattern-073 data-substitution fix): replaced hardcoded
        fake-project list with a real PortfolioService.list_active_projects
        query, mirroring the canonical PORTFOLIO handler at
        services/intent_service/canonical_handlers.py:3972. Falls back to an
        honest no-projects-yet message when the user has no active projects
        or when user_id is unavailable (rather than asserting fake data).

        Phase 3C history: Issue #635 CONSCIOUSNESS-TRANSFORM Files/Projects
        introduced the consciousness wrapper; the underlying data path was
        left as hardcoded scaffolding until this issue.
        """
        # No user_id → can't query their portfolio. Honest fallback.
        if not user_id:
            return IntentProcessingResult(
                success=True,
                message=(
                    "I can show you your projects, but I need to know who you are first. "
                    "Try signing in, or use the portfolio surface for the list."
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {"reason": "no_user_id"},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

        from services.database.repositories import ProjectRepository
        from services.onboarding.portfolio_service import PortfolioService

        try:
            async with AsyncSessionFactory.session_scope() as session:
                project_repo = ProjectRepository(session)
                portfolio_service = PortfolioService(project_repo)
                projects = await portfolio_service.list_active_projects(user_id=user_id)
        except Exception as e:
            self.logger.error(f"Failed to list projects for user {user_id}: {e}")
            return IntentProcessingResult(
                success=False,
                message=(
                    "I had trouble loading your projects right now. "
                    "You can try again in a moment."
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {"error": str(e)},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

        # Transform domain Project objects → dicts for format_projects_conscious.
        project_dicts = [{"name": p.name, "active": not p.is_archived} for p in projects]

        return IntentProcessingResult(
            success=True,
            message=format_projects_conscious(project_dicts),
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "context": {"project_count": len(projects)},
            },
            workflow_id=workflow_id,
            requires_clarification=False,
            clarification_type=None,
        )

    async def _handle_generic_query(
        self, intent: Intent, workflow_id: str, session_id: str = None
    ) -> IntentProcessingResult:
        """
        Handle generic QUERY intents that have no specialized handler.

        Issue #915: Routes to conversational floor instead of returning
        a dev stub ("Query processed successfully: {action}").
        The floor can discuss the topic conversationally with context.
        """
        self.logger.info(
            "query_action_routing_to_floor",
            action=intent.action,
            reason="no_specialized_handler",
        )
        return await self._handle_unknown_intent(
            intent,
            None,
            session_id or "default_session",
        )

    async def _handle_search_documents_notion(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle document search via Notion integration.

        Issue #516: Canonical Query #20 - "Search for X in our documents"
        Uses NotionIntegrationRouter.search_notion() to search workspace.

        Args:
            intent: The classified intent with search query in context
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with search results or graceful fallback
        """
        self.logger.info(f"Processing document search via Notion: {intent.action}")

        try:
            # Import NotionIntegrationRouter
            from services.integrations.notion.notion_integration_router import (
                NotionIntegrationRouter,
            )

            # Initialize router
            notion_router = NotionIntegrationRouter()

            # Check if Notion is configured
            if not notion_router.is_configured():
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to help search your documents, but Notion isn't configured yet. "
                        "To enable document search, please add your NOTION_API_KEY to your environment "
                        "or configure it in PIPER.user.md. Once configured, I can search your entire "
                        "Notion workspace for you!"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Extract search query from intent context
            search_query = intent.context.get("search_query") or intent.context.get(
                "original_message", ""
            )

            # Connect and search
            await notion_router.connect()
            results = await notion_router.search_notion(
                query=search_query,
                filter_type="page",  # Search pages (documents)
                page_size=10,
            )

            # Format results
            if not results:
                return IntentProcessingResult(
                    success=True,
                    message=format_no_results_conscious(search_query),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "search_query": search_query,
                        "result_count": 0,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                )

            # Build response with result summaries
            result_summaries = []
            for item in results[:5]:  # Top 5 results
                title = "Untitled"
                if "properties" in item:
                    title_prop = item["properties"].get("title", {})
                    if "title" in title_prop and len(title_prop["title"]) > 0:
                        title = title_prop["title"][0].get("text", {}).get("content", "Untitled")
                    elif "Name" in item["properties"]:
                        name_prop = item["properties"]["Name"]
                        if "title" in name_prop and len(name_prop["title"]) > 0:
                            title = name_prop["title"][0].get("text", {}).get("content", "Untitled")

                result_summaries.append(
                    {
                        "title": title,
                        "id": item.get("id", ""),
                        "url": item.get("url", ""),
                        "last_edited": item.get("last_edited_time", ""),
                    }
                )

            # Format message with consciousness wrapper (Issue #634)
            return IntentProcessingResult(
                success=True,
                message=format_search_results_conscious(
                    search_query, result_summaries, "your Notion workspace"
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "search_query": search_query,
                    "result_count": len(results),
                    "results": result_summaries,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Notion document search error: {e}")
            return IntentProcessingResult(
                success=False,
                message=format_search_error_conscious(str(e)),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="NotionSearchError",
            )

    async def _handle_analyze_document_notion(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle document analysis via Notion integration.

        Issue #515: Canonical Query #17 - "Analyze this document"
        Uses NotionIntegrationRouter to fetch and analyze Notion page content.

        Args:
            intent: The classified intent with document reference in context
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with analysis or graceful fallback
        """
        self.logger.info(f"Processing document analysis via Notion: {intent.action}")

        try:
            # Import NotionIntegrationRouter
            from services.integrations.notion.notion_integration_router import (
                NotionIntegrationRouter,
            )

            # Initialize router
            notion_router = NotionIntegrationRouter()

            # Check if Notion is configured
            if not notion_router.is_configured():
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to analyze your document, but Notion isn't configured yet. "
                        "To enable document analysis, please add your NOTION_API_KEY to your environment "
                        "or configure it in PIPER.user.md. Alternatively, you can upload a file directly "
                        "and I'll analyze that instead!"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Extract document reference from intent context
            document_id = intent.context.get("document_id") or intent.context.get("page_id")
            document_title = intent.context.get("document_title") or intent.context.get("filename")

            # If no specific document, search for one based on message
            if not document_id:
                search_query = intent.context.get("original_message", "")
                await notion_router.connect()
                results = await notion_router.search_notion(query=search_query, page_size=1)

                if results:
                    document_id = results[0].get("id")
                    # Extract title from search result
                    if "properties" in results[0]:
                        title_prop = results[0]["properties"].get("title", {})
                        if "title" in title_prop and len(title_prop["title"]) > 0:
                            document_title = (
                                title_prop["title"][0].get("text", {}).get("content", "Untitled")
                            )
                else:
                    return IntentProcessingResult(
                        success=True,
                        message=(
                            "I couldn't find a specific document to analyze. Please specify which "
                            "document you'd like me to analyze, or try searching with 'search for X "
                            "in documents' first."
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=True,
                        clarification_type="document_selection",
                    )

            # Fetch document content
            await notion_router.connect()
            page_data = await notion_router.get_page(document_id)
            blocks = await notion_router.get_page_blocks(document_id)

            if not page_data:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unable to retrieve document '{document_title or document_id}'",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    error="Document not found",
                    error_type="NotionDocumentError",
                )

            # Extract text content from blocks
            text_content = []
            for block in blocks:
                block_type = block.get("type", "")
                if block_type in [
                    "paragraph",
                    "heading_1",
                    "heading_2",
                    "heading_3",
                    "bulleted_list_item",
                    "numbered_list_item",
                ]:
                    rich_text = block.get(block_type, {}).get("rich_text", [])
                    for text_obj in rich_text:
                        text_content.append(text_obj.get("plain_text", ""))

            full_content = "\n".join(text_content)

            # Simple analysis summary
            word_count = len(full_content.split())
            char_count = len(full_content)
            paragraph_count = len([p for p in text_content if p.strip()])

            # Build analysis response
            title = page_data.get("title", document_title or "Untitled")
            last_edited = page_data.get("last_edited_time", "Unknown")

            message = f"""**Document Analysis: {title}**

**Overview:**
- Word count: {word_count:,}
- Character count: {char_count:,}
- Sections: {paragraph_count}
- Last edited: {last_edited}

**Content Preview:**
{full_content[:500]}{'...' if len(full_content) > 500 else ''}

**URL:** {page_data.get('url', 'N/A')}
"""

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "document_id": document_id,
                    "document_title": title,
                    "word_count": word_count,
                    "paragraph_count": paragraph_count,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Notion document analysis error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="analyzing that document",
                error_type="NotionAnalysisError",
            )

    async def _handle_update_document_notion(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle document update via Notion integration.

        Issue #522: Canonical Query #40 - "Update the X document"
        Uses NotionIntegrationRouter.search_notion() to find document by name,
        then update_page() to modify it.

        Flow:
        1. Extract document name and update content from query
        2. Search for document by name
        3. Handle ambiguity (0 matches, 1 match, multiple matches)
        4. Update document properties
        5. Return confirmation

        Args:
            intent: The classified intent with document name in context
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with update confirmation or clarification request
        """
        self.logger.info(f"Processing document update via Notion: {intent.action}")

        try:
            # Import NotionIntegrationRouter
            from services.integrations.notion.notion_integration_router import (
                NotionIntegrationRouter,
            )

            # Initialize router
            notion_router = NotionIntegrationRouter()

            # Check if Notion is configured
            if not notion_router.is_configured():
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to help update your document, but Notion isn't configured yet. "
                        "To enable document updates, please add your NOTION_API_KEY to your environment "
                        "or configure it in PIPER.user.md. Once configured, I can update documents "
                        "in your Notion workspace!"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Issue #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING (2026-05-27):
            # Use LLM-driven slot extraction (extract_slots) instead of the
            # legacy regex-based _parse_document_update_query. The regex hit
            # Pattern-045 — narrow canonical phrasings worked, natural language
            # flunked. The LLM extractor uses DOCUMENT_UPDATE_TEMPLATE's
            # extraction_hints to recover doc_name + content from arbitrary
            # phrasings (with/without parens, colons, antecedents, etc.).
            original_message = intent.context.get("original_message", "")

            # Lazy-init LLM client (same pattern used elsewhere in this file
            # for test-mockability)
            if not hasattr(self, "llm_client") or self.llm_client is None:
                from services.llm.clients import LLMClient

                self.llm_client = LLMClient()

            from services.slot_filling.slot_extractor import extract_slots
            from services.slot_filling.slot_template import DOCUMENT_UPDATE_TEMPLATE

            # #1122 option B: pass conversation history so the extractor can
            # resolve antecedent phrases ("the doc", "that one") against
            # entities from prior turns. Shared builder (#1122 floor fix):
            # the in-flight turn is excluded by response-is-None, not list
            # position — the old `turns[:-1]` here dropped the latest PRIOR
            # turn whenever the current turn wasn't yet recorded, which was
            # every time on this path before the outer-seam recording.
            # session_id comes from the HANDLER PARAMETER — intent.context
            # never carried a session_id, so the original option-B lookup
            # (`intent.context.get("session_id")`) was always None and the
            # extractor never saw history on the live path.
            _ictx = intent.context or {}
            conversation_history = build_recent_history(
                session_id,
                _ictx.get("user_id"),
                max_turns=8,
            )

            extracted = await extract_slots(
                message=original_message,
                template=DOCUMENT_UPDATE_TEMPLATE,
                llm_service=self.llm_client,
                conversation_history=conversation_history or None,
            )
            doc_name = extracted.get("doc_name")
            update_content = extracted.get("content")

            if not doc_name:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I need to know which document to update. Please specify the document name, "
                        "for example: 'Update the Project Plan document with the new deadline'"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="document_name",
                )

            # Connect and search for the document
            await notion_router.connect()
            results = await notion_router.search_notion(
                query=doc_name,
                filter_type="page",
                page_size=5,
            )

            # Handle search results
            if not results:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        f"No document found matching '{doc_name}'. Please try a different name or "
                        f"use 'search for X in documents' to find the right document."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "search_query": doc_name,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="document_not_found",
                )

            # Extract matching document(s)
            matches = []
            for item in results:
                title = "Untitled"
                if "properties" in item:
                    title_prop = item["properties"].get("title", {})
                    if "title" in title_prop and len(title_prop["title"]) > 0:
                        title = title_prop["title"][0].get("text", {}).get("content", "Untitled")
                    elif "Name" in item["properties"]:
                        name_prop = item["properties"]["Name"]
                        if "title" in name_prop and len(name_prop["title"]) > 0:
                            title = name_prop["title"][0].get("text", {}).get("content", "Untitled")

                matches.append(
                    {
                        "id": item.get("id", ""),
                        "title": title,
                        "url": item.get("url", ""),
                    }
                )

            # If multiple matches, ask for clarification
            if len(matches) > 1:
                match_list = "\n".join(
                    [f"{i+1}. **{m['title']}**" for i, m in enumerate(matches[:5])]
                )
                return IntentProcessingResult(
                    success=True,
                    message=(
                        f"Found {len(matches)} documents matching '{doc_name}':\n\n{match_list}\n\n"
                        f"Please specify which one you want to update."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "search_query": doc_name,
                        "matches": matches,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="multiple_matches",
                )

            # Single match - proceed with update
            target_doc = matches[0]
            page_id = target_doc["id"]
            doc_title = target_doc["title"]

            # Build update properties
            # Note: Notion property update format depends on page schema
            # For now, we'll update a "Description" or "Notes" property if it exists
            # or create a simple update confirmation

            if update_content:
                try:
                    # Issue #1080: Build a paragraph block from update_content and
                    # append to the page. Previously this called update_page with
                    # empty properties (a no-op) and asserted success — Pattern-073
                    # Instance 12 at the user-facing handler layer. Now uses
                    # append_blocks for actual "update doc with new content"
                    # semantics per Notion's data model (page = properties +
                    # child content blocks).
                    paragraph_block = {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": update_content},
                                }
                            ]
                        },
                    }
                    append_result = await notion_router.append_blocks(
                        page_id=page_id, blocks=[paragraph_block]
                    )

                    if append_result is None:
                        # Append failed — report honestly rather than claiming success
                        return IntentProcessingResult(
                            success=False,
                            message=(
                                f"I found **{doc_title}** but couldn't append the "
                                f"content. The Notion API call returned no result — "
                                f"the integration may not have write access to this "
                                f"specific page, or there may be a transient API issue. "
                                f"You can try again, or open the document directly: "
                                f"[View in Notion]({target_doc['url']})"
                            ),
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "document_id": page_id,
                                "document_title": doc_title,
                                "update_content": update_content,
                                "error": "append_blocks_returned_none",
                            },
                            workflow_id=workflow_id,
                            requires_clarification=False,
                            clarification_type=None,
                        )

                    return IntentProcessingResult(
                        success=True,
                        message=(
                            f"✓ Appended to **{doc_title}**\n\n"
                            f"Added paragraph: {update_content[:100]}{'...' if len(update_content) > 100 else ''}\n\n"
                            f"[View in Notion]({target_doc['url']})"
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                            "document_id": page_id,
                            "document_title": doc_title,
                            "update_content": update_content,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=False,
                    )

                except Exception as update_error:
                    self.logger.warning(f"Update failed: {update_error}")
                    # Fall through to confirmation without actual update
                    pass

            # Return confirmation (document found but update content may be incomplete)
            return IntentProcessingResult(
                success=True,
                message=(
                    f"Found **{doc_title}** ready for update.\n\n"
                    f"[View in Notion]({target_doc['url']})\n\n"
                    f"To update, please specify what you'd like to change, e.g.:\n"
                    f"'Update {doc_title} with the new deadline of January 15'"
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "document_id": page_id,
                    "document_title": doc_title,
                },
                workflow_id=workflow_id,
                requires_clarification=update_content is None,
                clarification_type="update_content" if update_content is None else None,
            )

        except Exception as e:
            self.logger.error(f"Notion document update error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="updating that document",
                error_type="NotionUpdateError",
            )

    # _parse_document_update_query removed 2026-05-27 per #1121
    # MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING. The 5-pattern regex helper was
    # Pattern-045 — it passed against canonical phrasings ("Update X document
    # with Y") and flunked natural language (parentheses, colons, "by adding
    # ... to it", antecedents). Replaced with LLM-driven extract_slots()
    # invocation in _handle_update_document_notion using the
    # DOCUMENT_UPDATE_TEMPLATE in services/slot_filling/slot_template.py.
    # See #1124 PRE-FLOOR-HANDLER-AUDIT for the broader migration roadmap;
    # this is the first cohort-1 migration.

    async def _handle_shipped_this_week(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "What did we ship this week?" query.

        Issue #518: Canonical Query #41 - GitHub Cluster
        Returns closed issues/PRs from the past 7 days as a release summary.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with shipped items or graceful fallback
        """
        self.logger.info(f"Processing shipped this week query: {intent.action}")

        try:
            # Import GitHubIntegrationRouter
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            # Initialize router (Issue #891: pass user_id for token lookup)
            github_router = GitHubIntegrationRouter()
            _user_id = _principal_from_intent(intent)
            await github_router.initialize(user_id=_user_id)

            # Check if GitHub is configured
            if not github_router.config_service.is_configured(_user_id or "system"):
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to show you what was shipped, but GitHub isn't configured yet. "
                        "To enable GitHub integration, please add your GITHUB_TOKEN to your environment "
                        "or configure it in PIPER.user.md. Once configured, I can track closed issues and PRs!"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Get closed issues from the past 7 days
            from datetime import datetime, timedelta, timezone

            closed_items = await github_router.get_closed_issues(limit=50)

            # Filter to past 7 days
            now = datetime.now(timezone.utc)
            week_ago = now - timedelta(days=7)

            recent_closed = []
            for item in closed_items:
                closed_at_str = item.get("closed_at")
                if closed_at_str:
                    closed_at = datetime.fromisoformat(closed_at_str.replace("Z", "+00:00"))
                    if closed_at >= week_ago:
                        recent_closed.append(item)

            # Format response.
            # #1096 (Pattern-073): verification-bounded phrasing — report
            # what was actually checked (the get_closed_issues window) rather
            # than asserting an unverifiable global ("no issues were closed").
            if not recent_closed:
                total_checked = len(closed_items)
                if total_checked == 0:
                    message = (
                        "No closed issues or PRs returned from GitHub. "
                        "This could mean none exist in the recent window, or "
                        "there's a configuration or auth issue worth checking."
                    )
                else:
                    message = (
                        f"No closures in the past 7 days among the "
                        f"{total_checked} most-recent closed items I checked."
                    )
            else:
                lines = [f"**Shipped This Week** ({len(recent_closed)} items):\n"]
                for item in recent_closed:
                    number = item.get("number", "?")
                    title = item.get("title", "Untitled")
                    url = item.get("html_url", "")
                    is_pr = bool(item.get("pull_request"))
                    item_type = "PR" if is_pr else "Issue"
                    lines.append(f"- {item_type} #{number}: {title}")
                    if url:
                        lines.append(f"  {url}")

                message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "shipped_count": len(recent_closed),
                    "items": recent_closed,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub shipped query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="fetching what was shipped this week",
                error_type="GitHubShippedQueryError",
            )

    async def _handle_stale_prs(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
        """
        Handle "Show me stale PRs" query.

        Issue #518: Canonical Query #42 - GitHub Cluster
        Returns open PRs older than 7 days with age and title.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with stale PRs or graceful fallback
        """
        self.logger.info(f"Processing stale PRs query: {intent.action}")

        try:
            from datetime import datetime, timedelta, timezone

            _user_id = _principal_from_intent(intent)

            # RECONNECT (#1322 P3): prefer the OAuth connector (search_pull_requests, author:@me);
            # native-PAT fallback only when not OAuth-connected; honest-degrade otherwise (#1231).
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = (
                await GitHubMCPSpatialAdapter().list_open_prs(_user_id, limit=100)
                if _user_id
                else None
            )
            if connector_result is not None and connector_result.issues is not None:
                # search_pull_requests already returns PRs (no pull_request-field filter needed).
                pr_items = connector_result.issues
            elif connector_result is not None and (
                connector_result.degradation.reason is not DegradationReason.CONNECT_REQUIRED
            ):
                # Connected but degraded → honest message, never a silent PAT fallback (#1231).
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                )
            else:
                # No principal, OR not OAuth-connected (CONNECT_REQUIRED) → native-PAT fallback.
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                await github_router.initialize(user_id=_user_id)
                if not github_router.config_service.is_configured(_user_id or "system"):
                    return IntentProcessingResult(
                        success=True,
                        message=(
                            "I'd love to show you stale PRs, but GitHub isn't connected yet. "
                            "Connect GitHub in Settings → Integrations to track your open PRs."
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=False,
                        implemented=False,  # Graceful degradation
                    )
                # Native path mixes issues + PRs → filter to PRs via the pull_request field.
                open_items = await github_router.get_open_issues(limit=100)
                pr_items = [item for item in open_items if item.get("pull_request")]

            # Filter to PRs older than 7 days
            now = datetime.now(timezone.utc)
            stale_threshold = now - timedelta(days=7)

            stale_prs = []
            for item in pr_items:
                created_at_str = item.get("created_at")
                if created_at_str:
                    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                    if created_at <= stale_threshold:
                        age_days = (now - created_at).days
                        item["age_days"] = age_days
                        stale_prs.append(item)

            # Sort by age (oldest first)
            stale_prs.sort(key=lambda x: x.get("age_days", 0), reverse=True)

            # Format response.
            # #1096 (Pattern-073 instance): the empty-result branch must
            # report what was actually verified, not assert a stronger claim.
            # `open_items` came from `get_open_issues(limit=100)` — if the API
            # returned zero, that could mean "no open PRs" OR "scope/auth issue"
            # OR "transient failure swallowed silently". Either way, we only
            # know we checked up to 100 items + none of them were PRs older
            # than 7 days. The prior wording ("All open PRs are less than
            # 7 days old") asserted more than the handler verified.
            if not stale_prs:
                # Pattern-073: report what was actually checked (the PR set), not a stronger claim.
                checked_count = len(pr_items)
                if checked_count == 0:
                    message = (
                        "No open PRs returned from GitHub. This could mean you have none "
                        "open, or there's a connection/auth issue worth checking."
                    )
                else:
                    message = (
                        f"No stale PRs among the {checked_count} open PR(s) I checked. "
                        f"(Older PRs may exist beyond the 100-item scan limit.)"
                    )
            else:
                lines = [f"**Stale PRs** ({len(stale_prs)} found):\n"]
                for pr in stale_prs:
                    number = pr.get("number", "?")
                    title = pr.get("title", "Untitled")
                    url = pr.get("html_url", "")
                    age_days = pr.get("age_days", 0)
                    lines.append(f"- PR #{number} ({age_days} days old): {title}")
                    if url:
                        lines.append(f"  {url}")

                message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "stale_count": len(stale_prs),
                    "items": stale_prs,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub stale PRs query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="checking for stale pull requests",
                error_type="GitHubStalePRsQueryError",
            )

    async def _handle_review_issue_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "Review issue #X" / "Show me issue #X" query.

        Issue #519: Canonical Query #60 - GitHub Issue Operations
        Fetches and displays details for a specific GitHub issue.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with issue details or error
        """
        self.logger.info(f"Processing review issue query: {intent.action}")

        try:
            import re

            _user_id = _principal_from_intent(intent)

            # Parse issue number FIRST (graceful ask if missing — no connector call wasted).
            original_message = intent.context.get("original_message", "")
            match = re.search(r"#?(\d+)", original_message)

            if not match:
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find an issue number in your request. Please specify an issue number (e.g., 'show me issue #123').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                )

            issue_number = int(match.group(1))

            # Optional explicit repo from "issue #N in owner/name" → threaded into resolve_repo.
            explicit_repo = None
            repo_match = re.search(r"\bin\s+([\w.\-]+/[\w.\-]+)", original_message)
            if repo_match:
                explicit_repo = repo_match.group(1)

            # RECONNECT (#1327 gap 2): connector-first (issue_read method=get, repo via
            # resolve_repo); native-PAT fallback only when not OAuth-connected; honest-degrade
            # otherwise (REPO_UNRESOLVED "which repo?" / UNREACHABLE) — never silent PAT (#1231).
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = await GitHubMCPSpatialAdapter().get_issue_connector(
                _user_id, issue_number=issue_number, explicit_repo=explicit_repo
            )
            if connector_result.item is not None:
                issue = connector_result.item
            elif (
                connector_result.degradation
                and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
            ):
                # Not connected via OAuth → transitional native-PAT fallback (#1042 path).
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                await github_router.initialize(user_id=_user_id)
                if not github_router.config_service.is_configured(_user_id or "system"):
                    return IntentProcessingResult(
                        success=True,
                        message=(
                            "I'd love to show you issue details, but GitHub isn't configured yet. "
                            "To enable GitHub integration, please add your GITHUB_TOKEN to your "
                            "environment or configure it in PIPER.user.md."
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=False,
                        implemented=False,  # Graceful degradation
                    )
                # Fetch issue details (Issue #1042: router resolves repo internally)
                issue = await github_router.get_issue(issue_number)
            else:
                # Connected but degraded (REPO_UNRESOLVED "which repo?" / UNREACHABLE) → honest.
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "degraded": connector_result.degradation.reason.value,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=(
                        connector_result.degradation.reason
                        is DegradationReason.REPO_UNRESOLVED
                    ),
                )

            # #969: Guard against None (API returns None if issue not found or not configured)
            if issue is None:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        f"I couldn't find issue #{issue_number} — it may not exist in this "
                        f"repository, or GitHub may not be fully connected. You can check "
                        f"the issue directly or verify your GitHub configuration in Settings."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                )

            # Format issue details. Labels/assignees may be dicts (raw GitHub API) OR plain
            # strings (the normalized native get_github_issue_direct shape + the #1327 connector
            # parser) — tolerate both so neither path crashes (was dict-only → crashed on the
            # normalized string shape).
            title = issue.get("title", "Untitled")
            state = issue.get("state", "unknown")
            labels = issue.get("labels", [])
            label_names = (
                [(lbl.get("name", "") if isinstance(lbl, dict) else lbl) for lbl in labels]
                if isinstance(labels, list)
                else []
            )
            body = issue.get("body", "No description") or "No description"
            body_preview = body[:200] + "..." if len(body) > 200 else body
            assignees = issue.get("assignees", [])
            assignee_names = (
                [(a.get("login", "") if isinstance(a, dict) else a) for a in assignees]
                if isinstance(assignees, list)
                else []
            )
            url = issue.get("html_url", "")

            lines = [
                f"**Issue #{issue_number}: {title}**\n",
                f"**State:** {state}",
            ]

            if label_names:
                lines.append(f"**Labels:** {', '.join(label_names)}")

            if assignee_names:
                lines.append(f"**Assignees:** {', '.join(assignee_names)}")

            lines.append(f"\n**Description:**\n{body_preview}")

            if url:
                lines.append(f"\n**URL:** {url}")

            message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue_number,
                    "issue": issue,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub review issue query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="reviewing that issue",
                error_type="GitHubReviewIssueQueryError",
            )

    @staticmethod
    def _extract_search_terms(message: str, action: str) -> str:
        """
        Extract search terms from a close/reopen message by stripping command words.

        Args:
            message: The original user message
            action: 'close' or 'reopen'

        Returns:
            Cleaned search string for fuzzy matching against issue titles
        """
        import re as _re

        text = message.lower().strip()
        # Strip common command words and filler
        strip_words = [
            "close",
            "reopen",
            "re-open",
            "issue",
            "the",
            "that",
            "this",
            "please",
            "can",
            "you",
            "a",
            "an",
            "my",
            "our",
            "it",
        ]
        for word in strip_words:
            text = _re.sub(rf"\b{word}\b", "", text)
        # Collapse whitespace
        text = _re.sub(r"\s+", " ", text).strip()
        return text

    @staticmethod
    def _score_issue_match(search_terms: str, issue_title: str) -> int:
        """
        Score how well search terms match an issue title using word overlap.

        Returns count of matching words (0 means no match).
        """
        if not search_terms or not issue_title:
            return 0
        search_words = set(search_terms.lower().split())
        title_words = set(issue_title.lower().split())
        return len(search_words & title_words)

    async def _fuzzy_find_issues(
        self,
        github_router,
        search_terms: str,
        state: str,
        limit: int = 50,
    ) -> list:
        """
        Find issues matching search terms by fuzzy title matching.

        Args:
            github_router: Initialized GitHubIntegrationRouter
            search_terms: Cleaned search string
            state: 'open' or 'closed' — which issues to search
            limit: Max issues to fetch from API

        Returns:
            List of (score, issue_dict) tuples sorted by score descending
        """
        try:
            if state == "open":
                issues = await github_router.get_open_issues(limit=limit)
            else:
                issues = await github_router.get_closed_issues(limit=limit)
        except Exception as e:
            self.logger.warning(f"Failed to fetch issues for fuzzy match: {e}")
            return []

        scored = []
        for issue in issues:
            title = issue.get("title", "")
            score = self._score_issue_match(search_terms, title)
            if score > 0:
                scored.append((score, issue))

        # Sort by score descending, then by issue number descending (most recent)
        scored.sort(key=lambda x: (x[0], x[1].get("number", 0)), reverse=True)
        return scored

    async def _handle_close_issue_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "Close issue #X" query.

        Issue #519: Canonical Query #45 - GitHub Issue Operations
        Closes a specific GitHub issue.
        Issue #902: Fuzzy match by description when no issue number given.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with confirmation or error
        """
        self.logger.info(f"Processing close issue query: {intent.action}")

        try:
            # Import GitHubIntegrationRouter
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            # Initialize router (Issue #891: pass user_id for token lookup)
            github_router = GitHubIntegrationRouter()
            _user_id = _principal_from_intent(intent)
            await github_router.initialize(user_id=_user_id)

            # Check if GitHub is configured
            if not github_router.config_service.is_configured(_user_id or "system"):
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to close issues for you, but GitHub isn't configured yet. "
                        "To enable GitHub integration, please add your GITHUB_TOKEN to your environment "
                        "or configure it in PIPER.user.md."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Parse issue number from message
            import re

            original_message = intent.context.get("original_message", "")
            match = re.search(r"#?(\d+)", original_message)

            if not match:
                # Issue #902: Fuzzy match by description
                search_terms = self._extract_search_terms(original_message, "close")
                if search_terms:
                    matches = await self._fuzzy_find_issues(
                        github_router, search_terms, state="open"
                    )
                    if len(matches) == 1:
                        score, issue = matches[0]
                        num = issue.get("number")
                        title = issue.get("title", "")
                        return IntentProcessingResult(
                            success=False,
                            message=f"Did you mean issue #{num}: {title}? Say 'close issue #{num}' to confirm.",
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "matched_issue_number": num,
                                "matched_issue_title": title,
                            },
                            workflow_id=workflow_id,
                            requires_clarification=True,
                        )
                    elif len(matches) > 1:
                        lines = ["I found a few issues that might match:"]
                        for _score, issue in matches[:5]:
                            lines.append(f"- #{issue.get('number')}: {issue.get('title', '')}")
                        lines.append("\nWhich one would you like to close?")
                        return IntentProcessingResult(
                            success=False,
                            message="\n".join(lines),
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "matched_issues": [
                                    {"number": i.get("number"), "title": i.get("title", "")}
                                    for _s, i in matches[:5]
                                ],
                            },
                            workflow_id=workflow_id,
                            requires_clarification=True,
                        )

                # No search terms or no matches
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find any issues matching your description. Please specify an issue number (e.g., 'close issue #123').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                )

            issue_number = int(match.group(1))

            # Issue #902: Check if this is a confirmed close (user already saw
            # the issue and confirmed). Pattern: "yes, close #123" or "confirm close #123"
            confirmed = bool(
                re.search(
                    r"\b(yes|confirm|confirmed|sure|go ahead|do it)\b",
                    original_message.lower(),
                )
            )

            if not confirmed:
                # First request: fetch issue details and ask for confirmation
                # (Issue #1042: router resolves repo internally)
                try:
                    issue_details = await github_router.get_issue(issue_number)
                    title = issue_details.get("title", f"Issue #{issue_number}")
                    state = issue_details.get("state", "unknown")

                    if state == "closed":
                        return IntentProcessingResult(
                            success=True,
                            message=f"Issue #{issue_number}: {title} is already closed.",
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "issue_number": issue_number,
                                "already_closed": True,
                            },
                            workflow_id=workflow_id,
                            requires_clarification=False,
                        )

                    return IntentProcessingResult(
                        success=True,
                        message=(
                            f"Are you sure you want to close issue #{issue_number}: "
                            f"**{title}**?\n\n"
                            f"Say 'yes, close #{issue_number}' to confirm."
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                            "issue_number": issue_number,
                            "pending_confirmation": True,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=True,
                    )
                except Exception as fetch_err:
                    self.logger.warning(
                        f"Could not fetch issue #{issue_number} for confirmation: {fetch_err}"
                    )
                    # Fall through to close without preview if fetch fails

            # Confirmed close (or fallback if fetch failed)
            # (Issue #1042: router resolves repo internally)
            updated_issue = await github_router.update_issue(issue_number, state="closed")

            # Get issue title for success message
            title = updated_issue.get("title", f"Issue #{issue_number}")
            url = updated_issue.get("html_url", "")

            message_lines = [
                f"Closed issue #{issue_number}: {title}",
            ]

            if url:
                message_lines.append(f"{url}")

            message = "\n".join(message_lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue_number,
                    "issue": updated_issue,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub close issue query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="closing that issue",
                error_type="GitHubCloseIssueQueryError",
            )

    async def _handle_reopen_issue_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "Reopen issue #X" query.

        Issue #902: Mirror of close issue handler with state="open".

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with confirmation or error
        """
        self.logger.info(f"Processing reopen issue query: {intent.action}")

        try:
            # Import GitHubIntegrationRouter
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            # Initialize router (Issue #891: pass user_id for token lookup)
            github_router = GitHubIntegrationRouter()
            _user_id = _principal_from_intent(intent)
            await github_router.initialize(user_id=_user_id)

            # Check if GitHub is configured
            if not github_router.config_service.is_configured(_user_id or "system"):
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to reopen issues for you, but GitHub isn't configured yet. "
                        "To enable GitHub integration, please add your GITHUB_TOKEN to your environment "
                        "or configure it in PIPER.user.md."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Parse issue number from message
            import re

            original_message = intent.context.get("original_message", "")
            match = re.search(r"#?(\d+)", original_message)

            if not match:
                # Issue #902: Fuzzy match by description
                search_terms = self._extract_search_terms(original_message, "reopen")
                if search_terms:
                    matches = await self._fuzzy_find_issues(
                        github_router, search_terms, state="closed"
                    )
                    if len(matches) == 1:
                        score, issue = matches[0]
                        num = issue.get("number")
                        title = issue.get("title", "")
                        return IntentProcessingResult(
                            success=False,
                            message=f"Did you mean issue #{num}: {title}? Say 'reopen issue #{num}' to confirm.",
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "matched_issue_number": num,
                                "matched_issue_title": title,
                            },
                            workflow_id=workflow_id,
                            requires_clarification=True,
                        )
                    elif len(matches) > 1:
                        lines = ["I found a few issues that might match:"]
                        for _score, issue in matches[:5]:
                            lines.append(f"- #{issue.get('number')}: {issue.get('title', '')}")
                        lines.append("\nWhich one would you like to reopen?")
                        return IntentProcessingResult(
                            success=False,
                            message="\n".join(lines),
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "matched_issues": [
                                    {"number": i.get("number"), "title": i.get("title", "")}
                                    for _s, i in matches[:5]
                                ],
                            },
                            workflow_id=workflow_id,
                            requires_clarification=True,
                        )

                # No search terms or no matches
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find any issues matching your description. Please specify an issue number (e.g., 'reopen issue #123').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                )

            issue_number = int(match.group(1))

            # Issue #902: Confirmation UX (mirrors close handler)
            confirmed = bool(
                re.search(
                    r"\b(yes|confirm|confirmed|sure|go ahead|do it)\b",
                    original_message.lower(),
                )
            )

            if not confirmed:
                # (Issue #1042: router resolves repo internally)
                try:
                    issue_details = await github_router.get_issue(issue_number)
                    title = issue_details.get("title", f"Issue #{issue_number}")
                    state = issue_details.get("state", "unknown")

                    if state == "open":
                        return IntentProcessingResult(
                            success=True,
                            message=f"Issue #{issue_number}: {title} is already open.",
                            intent_data={
                                "category": intent.category.value,
                                "action": intent.action,
                                "confidence": intent.confidence,
                                "issue_number": issue_number,
                                "already_open": True,
                            },
                            workflow_id=workflow_id,
                            requires_clarification=False,
                        )

                    return IntentProcessingResult(
                        success=True,
                        message=(
                            f"Reopen issue #{issue_number}: **{title}**?\n\n"
                            f"Say 'yes, reopen #{issue_number}' to confirm."
                        ),
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "confidence": intent.confidence,
                            "issue_number": issue_number,
                            "pending_confirmation": True,
                        },
                        workflow_id=workflow_id,
                        requires_clarification=True,
                    )
                except Exception as fetch_err:
                    self.logger.warning(
                        f"Could not fetch issue #{issue_number} for confirmation: {fetch_err}"
                    )

            # Confirmed reopen (or fallback if fetch failed)
            # (Issue #1042: router resolves repo internally)
            updated_issue = await github_router.update_issue(issue_number, state="open")

            # Get issue title for success message
            title = updated_issue.get("title", f"Issue #{issue_number}")
            url = updated_issue.get("html_url", "")

            message_lines = [
                f"Reopened issue #{issue_number}: {title}",
            ]

            if url:
                message_lines.append(f"{url}")

            message = "\n".join(message_lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue_number,
                    "issue": updated_issue,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub reopen issue query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="reopening that issue",
                error_type="GitHubReopenIssueQueryError",
            )

    async def _handle_comment_issue_query(
        self, intent: Intent, workflow_id: str, session_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle "Comment on issue #X saying..." query.

        Issue #519: Canonical Query #59 - GitHub Issue Operations
        Adds a comment to a specific GitHub issue.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID

        Returns:
            IntentProcessingResult with confirmation or error
        """
        self.logger.info(f"Processing comment issue query: {intent.action}")

        try:
            # Import GitHubIntegrationRouter
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            # Initialize router (Issue #891: pass user_id for token lookup)
            github_router = GitHubIntegrationRouter()
            _user_id = _principal_from_intent(intent)
            await github_router.initialize(user_id=_user_id)

            # Check if GitHub is configured
            if not github_router.config_service.is_configured(_user_id or "system"):
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I'd love to add comments to issues for you, but GitHub isn't configured yet. "
                        "To enable GitHub integration, please add your GITHUB_TOKEN to your environment "
                        "or configure it in PIPER.user.md."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Issue #1124 Phase 2: LLM-driven slot extraction (extract_slots) replaces
            # the brittle hand-regex (`re.search(r"#?(\d+)")` + the `comment_patterns`
            # list) that hit Pattern-045 — narrow canonical phrasings worked, natural
            # language flunked. COMMENT_ISSUE_TEMPLATE recovers issue_number +
            # comment_text from arbitrary phrasings.
            import re

            original_message = intent.context.get("original_message", "")

            # Lazy-init LLM client (test-mockable; same pattern as update_document #1121).
            if not hasattr(self, "llm_client") or self.llm_client is None:
                from services.llm.clients import LLMClient

                self.llm_client = LLMClient()

            from services.slot_filling.slot_extractor import extract_slots
            from services.slot_filling.slot_template import COMMENT_ISSUE_TEMPLATE

            # #1122: pass conversation history so the extractor can resolve antecedents
            # ("that issue", "it") against entities from prior turns. Uses the
            # shared builder (the DRY follow-on this comment used to promise).
            # session_id is the threaded handler param — intent.context never
            # carried one (same live-wiring gap as update_document).
            _ictx = intent.context or {}
            conversation_history = build_recent_history(
                session_id,
                _ictx.get("user_id"),
                max_turns=8,
            )

            extracted = await extract_slots(
                message=original_message,
                template=COMMENT_ISSUE_TEMPLATE,
                llm_service=self.llm_client,
                conversation_history=conversation_history or None,
            )

            # issue_number arrives as an ENTITY string — pull the digits.
            issue_number = None
            _raw_issue = extracted.get("issue_number")
            if _raw_issue is not None:
                _digits = re.search(r"\d+", str(_raw_issue))
                if _digits:
                    issue_number = int(_digits.group(0))

            if issue_number is None:
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find an issue number in your request. Please specify an issue number (e.g., 'comment on issue #123 saying...').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                )

            comment_body = extracted.get("comment_text")
            if comment_body:
                comment_body = comment_body.strip()

            if not comment_body:
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find the comment text. Please specify what you'd like to say (e.g., 'comment on issue #123 saying this looks great').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                )

            # Add the comment (Issue #1042: router resolves repo internally)
            comment_result = await github_router.add_comment(issue_number, comment_body)

            # Format confirmation message
            comment_preview = comment_body[:50] + "..." if len(comment_body) > 50 else comment_body

            message_lines = [
                f"Successfully added comment to issue #{issue_number}",
                f"Comment: {comment_preview}",
            ]

            if comment_result and comment_result.get("html_url"):
                message_lines.append(f"{comment_result.get('html_url')}")

            message = "\n".join(message_lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue_number,
                    "comment_body": comment_body,
                    "comment": comment_result,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"GitHub comment issue query error: {e}")
            # #1159: a repo-resolution failure is a graceful "which repo?" case,
            # not an opaque crash. Detect it and ask, instead of rendering the
            # generic "something unexpected happened" via _make_error_result.
            if "no repo could be resolved" in str(e).lower():
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I can add that comment, but I couldn't tell which repository "
                        "the issue is in. Tell me the repo (for example, "
                        '"comment on owner/repo#123 saying ...") or set a default '
                        "repository, and I'll post it."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="adding a comment to that issue",
                error_type="GitHubCommentIssueQueryError",
            )

    async def _handle_list_issues_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "How many open issues?" and similar issue listing queries.

        Issue #845: Routes issue queries to GitHub issue data instead of
        falling through to project status.
        """
        self.logger.info("Processing list issues query")

        try:
            _user_id = _principal_from_intent(intent)

            # RECONNECT (#1322): prefer the per-user OAuth connector (binding + grant →
            # search_issues, user-wide assignee:@me). Fall back to the native PAT ONLY when
            # the user hasn't connected GitHub via OAuth yet (CONNECT_REQUIRED) — the
            # layer-then-migrate transition (D6 retires the PAT path). If they ARE connected
            # but the connector is degraded (server unreachable / re-auth), degrade honestly
            # (#1231) rather than masking the real connection state with a silent PAT fallback.
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = await GitHubMCPSpatialAdapter().list_open_issues(
                _user_id, limit=50
            )
            if connector_result.issues is not None:
                issues = connector_result.issues
                total_count = (
                    connector_result.total
                    if connector_result.total is not None
                    else len(issues)
                )
            elif (
                connector_result.degradation
                and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
            ):
                # Not connected via OAuth → transitional native-PAT fallback (#1042 path).
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                await github_router.initialize(user_id=_user_id)
                issues = await github_router.get_open_issues(limit=50)
                total_count = len(issues)  # native path returns the full list, not a page
            else:
                # Connected but degraded → honest message, never a silent PAT fallback (#1231).
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": "query",
                        "action": "list_issues_query",
                        "context": {"degraded": connector_result.degradation.reason.value},
                    },
                )

            if issues:
                # total_count is the TRUE match count (search_issues total_count); `issues` is
                # only a page (e.g. 30 of 179) — count by total_count, show a few recent (#1322).
                message = (
                    f"You have **{total_count} open issue{'s' if total_count != 1 else ''}**."
                )
                message += "\n\nHere are the most recent:"
                for issue in issues[:5]:
                    title = issue.get("title", "Untitled")
                    number = issue.get("number", "?")
                    labels = ", ".join(
                        label.get("name", "") for label in issue.get("labels", [])
                    )
                    label_str = f" ({labels})" if labels else ""
                    message += f"\n- **#{number}**: {title}{label_str}"

                if total_count > 5:
                    message += f"\n\n...and {total_count - 5} more."
            else:
                message = "You don't have any open issues right now."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_issues_query",
                    "context": {
                        "issue_count": total_count if issues else 0,
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list issues: {e}")
            return IntentProcessingResult(
                success=True,
                message="I wasn't able to fetch your issues right now. Please try again in a moment.",
                intent_data={
                    "category": "query",
                    "action": "list_issues_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_set_default_repo(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle conversational "set my default repo to owner/name" (RECONNECT #1327).

        The conversational counterpart to the GUI default-repo setting. Persists the
        repo as THIS user's default in the DB-backed ``connector_configs`` store
        (ADR-070 D4) — the SAME key ``repo_resolver.resolve_repo`` reads at path 3
        (``_resolve_from_user_default``), so the value round-trips into every
        repo-resolving handler.

        Setting the default is a PREFERENCE, independent of the GitHub OAuth binding:
        it must work whether or not GitHub is connected (the value is consumed later by
        ``resolve_repo``), so this handler does NOT construct a GitHub router/connector
        and does NOT gate on connection state.

        Validation mirrors the close/reopen handlers' issue-number parse: the
        ``owner/name`` token is parsed out of ``original_message`` and validated with
        ``parse_full_name``. A bad shape yields a graceful chat nudge — never an
        exception.
        """
        import re

        self.logger.info("Processing set-default-repo query")

        from services.integrations.github.repo_resolver import parse_full_name

        original_message = intent.context.get("original_message", "")
        _user_id = _principal_from_intent(intent)

        _GRACEFUL_BAD_SHAPE = (
            "That doesn't look like an `owner/name` repo — try e.g. "
            "`set my default repo to mediajunkie/piper-morgan-product`."
        )

        def _bad_shape_result() -> IntentProcessingResult:
            return IntentProcessingResult(
                success=True,
                message=_GRACEFUL_BAD_SHAPE,
                intent_data={
                    "category": "query",
                    "action": "set_default_repo",
                    "context": {"error": "invalid_repo_shape"},
                },
                workflow_id=workflow_id,
                requires_clarification=True,
            )

        # Find a candidate owner/name token in the message, then validate it strictly
        # with parse_full_name (the same validator resolve_repo trusts). The candidate
        # regex is permissive; parse_full_name is the authority on shape.
        candidate_match = re.search(r"[\w.\-]+/[\w.\-]+", original_message)
        if not candidate_match:
            return _bad_shape_result()

        candidate = candidate_match.group(0)
        try:
            owner, name = parse_full_name(candidate)
        except ValueError:
            return _bad_shape_result()

        full_name = f"{owner}/{name}"

        try:
            from services.connectors.config_service import ConnectorConfigService
            from services.database.session_factory import AsyncSessionFactory

            # session_scope() commits on clean exit (#1193), and set_default_repo
            # flushes-not-commits (caller owns the txn) — so the write persists here.
            async with AsyncSessionFactory.session_scope() as session:
                await ConnectorConfigService(session).set_default_repo(_user_id, full_name)

            return IntentProcessingResult(
                success=True,
                message=(
                    f"Done — your default repo is now **{full_name}**. "
                    "I'll use it whenever you don't name a repo explicitly."
                ),
                intent_data={
                    "category": "query",
                    "action": "set_default_repo",
                    "context": {"default_repo": full_name},
                },
                workflow_id=workflow_id,
            )
        except Exception as e:
            self.logger.error(f"Failed to set default repo: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to save your default repo just now. "
                    "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "set_default_repo",
                    "context": {"error": str(e)},
                },
                workflow_id=workflow_id,
            )

    async def _handle_get_default_repo(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle conversational "what's my default repo?" (RECONNECT #1327 build #2).

        The READ counterpart to ``_handle_set_default_repo``. PM UAT (2026-06-30):
        asked "what is my default repo again?", Piper floored honestly ("I don't have
        it in the context I have") — correct per the no-guess floor rule, but unhelpful,
        because the default IS persisted in the DB-backed ``connector_configs`` store
        (ADR-070 D4). This handler reads it via ``ConnectorConfigService.get_default_repo``
        — the SAME key the set handler writes and ``repo_resolver.resolve_repo`` reads at
        path 3 (``_resolve_from_user_default``) — and reports it.

        Reading the default is a PREFERENCE read, independent of the GitHub OAuth
        binding: it must work whether or not GitHub is connected (the value is a stored
        string), so this handler does NOT construct a GitHub router/connector and does
        NOT gate on connection state. When no default is set it returns a graceful,
        helpful nudge telling the user how to set one — never an exception.
        """
        self.logger.info("Processing get-default-repo query")

        _user_id = _principal_from_intent(intent)

        try:
            from services.connectors.config_service import ConnectorConfigService
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                repo = await ConnectorConfigService(session).get_default_repo(_user_id)

            if repo:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        f"Your default repo is **{repo}**. "
                        "I use it whenever you don't name a repo explicitly."
                    ),
                    intent_data={
                        "category": "query",
                        "action": "get_default_repo",
                        "context": {"default_repo": repo},
                    },
                    workflow_id=workflow_id,
                )

            return IntentProcessingResult(
                success=True,
                message=(
                    "You haven't set a default repo yet — tell me "
                    "`set my default repo to owner/name` "
                    "(e.g. `mediajunkie/piper-morgan-product`) and I'll remember it."
                ),
                intent_data={
                    "category": "query",
                    "action": "get_default_repo",
                    "context": {"default_repo": None},
                },
                workflow_id=workflow_id,
            )
        except Exception as e:
            self.logger.error(f"Failed to get default repo: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to look up your default repo just now. "
                    "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "get_default_repo",
                    "context": {"error": str(e)},
                },
                workflow_id=workflow_id,
            )

    async def _handle_unwired_write(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Honest-degrade handler for recognized-but-unwired WRITE actions (#1331).

        The trust fix: the LLM classifier can emit write actions (e.g.
        ``create_milestone``) for which NO real handler exists. Left alone, such an
        action falls through to the conversational floor (the LLM), which
        CONFABULATES a success message ("Milestone created ✓") even though no write
        ever happened. This handler is wired onto the ADR-059 / #1124
        action-dispatch rail (via ``services.intent_service.unwired_writes`` →
        ``workflow_entries``) so the action is intercepted BEFORE the floor — and
        answered with a brief, honest decline instead.

        SCOPE: honest-degrade FLOOR only. This performs NO write — it constructs no
        GitHub router/connector/service and mutates nothing. Real connector-backed
        writes are #1322 Q3. The decline names the capability, says it's not
        available *yet*, and points to the GitHub alternative (per #1331 tone:
        honest, brief, not over-apologetic). It NEVER fabricates success.

        Returns ``success=True`` (graceful — this is an expected, well-formed
        decline, not an error/422), with ``intent_data.unwired_write = True`` for
        analytics + audit.
        """
        from services.intent_service.unwired_writes import get_unwired_write_decline

        action = intent.action or "unknown"
        self.logger.info(
            "unwired_write_honest_degrade",
            action=action,
            reason="no_real_handler_decline_instead_of_confabulate",
        )

        return IntentProcessingResult(
            success=True,
            message=get_unwired_write_decline(action),
            intent_data={
                "category": (intent.category.value if intent.category else "execution"),
                "action": action,
                "unwired_write": True,
                "confidence": getattr(intent, "confidence", None),
            },
            workflow_id=workflow_id,
        )

    async def _handle_list_prs_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle "Show my PRs" and similar PR listing queries.

        Issue #851: Routes PR listing queries to GitHub PR data instead of
        falling through to the LLM classifier.
        """
        self.logger.info("Processing list PRs query")

        try:
            _user_id = _principal_from_intent(intent)

            # RECONNECT (#1322 P3): prefer the OAuth connector (search_pull_requests, author:@me).
            # Native-PAT fallback only when not OAuth-connected; honest-degrade otherwise (#1231).
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = await GitHubMCPSpatialAdapter().list_open_prs(_user_id, limit=50)
            if connector_result.issues is not None:
                prs = connector_result.issues
                pr_count = (
                    connector_result.total
                    if connector_result.total is not None
                    else len(prs)
                )
            elif (
                connector_result.degradation
                and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
            ):
                # Not connected via OAuth → transitional native-PAT fallback (#851 path).
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                await github_router.initialize(user_id=_user_id)
                if not github_router.config_service.is_configured(_user_id or "system"):
                    return IntentProcessingResult(
                        success=True,
                        message=(
                            "I'd love to show you your pull requests, but GitHub isn't connected "
                            "yet. Connect GitHub in Settings → Integrations to see your PRs."
                        ),
                        intent_data={
                            "category": "query",
                            "action": "list_prs_query",
                            "context": {"configured": False},
                        },
                    )
                # Native path mixes issues + PRs → filter to PRs via the pull_request field.
                open_items = await github_router.get_open_issues(limit=100)
                prs = [item for item in open_items if item.get("pull_request")]
                pr_count = len(prs)
            else:
                # Connected but degraded → honest message, never a silent PAT fallback (#1231).
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": "query",
                        "action": "list_prs_query",
                        "context": {"degraded": connector_result.degradation.reason.value},
                    },
                )

            if prs:
                message = f"You have **{pr_count} open PR{'s' if pr_count != 1 else ''}**."
                message += "\n\nHere are the most recent:"
                for pr in prs[:5]:
                    title = pr.get("title", "Untitled")
                    number = pr.get("number", "?")
                    url = pr.get("html_url", "")
                    message += f"\n- **#{number}**: {title}"
                    if url:
                        message += f"\n  {url}"

                if pr_count > 5:
                    message += f"\n\n...and {pr_count - 5} more."
            else:
                message = "You don't have any open pull requests right now."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_prs_query",
                    "context": {
                        "pr_count": pr_count,
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list PRs: {e}")
            return IntentProcessingResult(
                success=True,
                message="I wasn't able to fetch your pull requests right now. Please try again in a moment.",
                intent_data={
                    "category": "query",
                    "action": "list_prs_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_list_milestones_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle 'Show milestones' and similar queries (Issue #1039).

        Routes milestone listing through the GitHub integration router which
        resolves the repo via repo_resolver (#1042). Default state is "open"
        (state-filter UX deferred to #1051).
        """
        self.logger.info("Processing list milestones query")
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github_router = GitHubIntegrationRouter()
            milestones = await github_router.list_milestones_via_mcp()

            if milestones:
                count = len(milestones)
                message = f"You have **{count} open milestone" f"{'s' if count != 1 else ''}**."
                if count > 0:
                    # Sort by due_on (None last); show top 5
                    sorted_ms = sorted(
                        milestones,
                        key=lambda m: (m.get("due_on") is None, m.get("due_on") or ""),
                    )
                    message += "\n\nUpcoming:"
                    for m in sorted_ms[:5]:
                        title = m.get("title", "Untitled")
                        due_raw = m.get("due_on")
                        due = due_raw.split("T")[0] if due_raw else "no due date"
                        open_count = m.get("open_issues", 0)
                        suffix = f" ({open_count} open issue" f"{'s' if open_count != 1 else ''})"
                        message += f"\n- **{title}** — due {due}{suffix}"
                    if count > 5:
                        message += f"\n\n...and {count - 5} more."
            else:
                message = "You don't have any open milestones right now."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_milestones_query",
                    "context": {
                        "milestone_count": len(milestones) if milestones else 0,
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list milestones: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to fetch milestones right now. " "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "list_milestones_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_list_releases_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle 'Recent releases' / 'What version are we on?' (Issue #1039).

        Routes release listing through the GitHub integration router which
        resolves the repo via repo_resolver (#1042). Returns all releases;
        prerelease flag shown inline (prerelease-only filter UX deferred
        to #1051). Q5 disposition: "What version are we on?" infers latest
        non-prerelease at the top of the response.
        """
        self.logger.info("Processing list releases query")
        try:
            _user_id = _principal_from_intent(intent)

            # RECONNECT (#1327 gap 2): connector-first (list_releases, repo via resolve_repo);
            # native-PAT fallback only when not OAuth-connected; honest-degrade otherwise (#1231).
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = await GitHubMCPSpatialAdapter().list_releases_connector(_user_id)
            if connector_result.items is not None:
                releases = connector_result.items
            elif (
                connector_result.degradation
                and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
            ):
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                releases = await github_router.list_releases_via_mcp()
            else:
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": "query",
                        "action": "list_releases_query",
                        "context": {"degraded": connector_result.degradation.reason.value},
                    },
                )

            if releases:
                count = len(releases)
                # Sort by published_at descending (most recent first); None last
                sorted_releases = sorted(
                    releases,
                    key=lambda r: r.get("published_at") or "",
                    reverse=True,
                )
                # Q5 disposition: surface latest non-prerelease as headline
                latest_stable = next(
                    (r for r in sorted_releases if not r.get("prerelease")),
                    None,
                )
                if latest_stable:
                    tag = latest_stable.get("tag_name", "")
                    name = latest_stable.get("name") or tag
                    message = f"Current version: **{tag}** ({name})."
                else:
                    message = (
                        f"You have **{count} release{'s' if count != 1 else ''}**, "
                        "all pre-releases."
                    )
                # Show top 5 recent (regardless of stable/prerelease)
                message += "\n\nRecent releases:"
                for r in sorted_releases[:5]:
                    tag = r.get("tag_name", "")
                    name = r.get("name") or tag
                    pub_raw = r.get("published_at")
                    pub = pub_raw.split("T")[0] if pub_raw else "unpublished"
                    flag = " (pre-release)" if r.get("prerelease") else ""
                    message += f"\n- **{tag}**{flag} — {name} ({pub})"
                if count > 5:
                    message += f"\n\n...and {count - 5} more."
            else:
                message = "You don't have any releases yet."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_releases_query",
                    "context": {
                        "release_count": len(releases) if releases else 0,
                        "latest_version": (
                            next(
                                (r.get("tag_name") for r in releases if not r.get("prerelease")),
                                None,
                            )
                            if releases
                            else None
                        ),
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list releases: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to fetch releases right now. " "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "list_releases_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_list_labels_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle 'What labels do we use?' / 'Show issue labels' (Issue #1040).

        Routes label listing through the GitHub integration router which
        resolves the repo via repo_resolver (#1042). Plain-text presentation
        per Q3 disposition; visual swatches deferred to CXO copy review (#1043).

        NATIVE path (NOT the OAuth connector): github-mcp-server has NO list-labels tool —
        only ``get_label`` (fetch ONE label by name). The #1327 gap-2 cutover to a
        ``list_label`` connector tool was reverted (live, ``list_label`` returned
        ``unknown tool`` → labels degraded UNREACHABLE for OAuth users). Labels therefore
        stays native, exactly like milestones (also no github-mcp-server tool).
        """
        self.logger.info("Processing list labels query")
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github_router = GitHubIntegrationRouter()
            labels = await github_router.list_labels_via_mcp()

            if labels:
                count = len(labels)
                message = f"You have **{count} label{'s' if count != 1 else ''}**."
                # Sort alphabetically for stable presentation
                sorted_labels = sorted(labels, key=lambda lbl: lbl.get("name", ""))
                message += "\n"
                for lbl in sorted_labels[:20]:
                    name = lbl.get("name", "")
                    desc = lbl.get("description") or ""
                    desc_suffix = f" — {desc}" if desc else ""
                    message += f"\n- **{name}**{desc_suffix}"
                if count > 20:
                    message += f"\n\n...and {count - 20} more."
            else:
                message = "I don't see any labels for this repository."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_labels_query",
                    "context": {
                        "label_count": len(labels) if labels else 0,
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list labels: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to fetch labels right now. " "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "list_labels_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_list_branches_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle 'Active branches' / 'Show feature branches' (Issue #1040).

        Returns ALL branches (per Q5 disposition: "all non-default") with
        default-branch first. The colloquial "feature branches" query also
        routes here — handler treats it as a synonym for "all non-default".
        Filter syntax (e.g., claude/* patterns) deferred to post-MVP.
        Local-git "what branch are we on?" tracked by #1044.
        """
        self.logger.info("Processing list branches query")
        try:
            _user_id = _principal_from_intent(intent)

            # RECONNECT (#1327 gap 2): prefer the per-user OAuth connector (binding + grant →
            # list_branches), resolving the repo via resolve_repo(). Fall back to the native PAT
            # ONLY when not OAuth-connected (CONNECT_REQUIRED). REPO_UNRESOLVED → "which repo?";
            # any other degrade → honest message — never a silent PAT fallback (#1231).
            from services.mcp.consumer.connector import DegradationReason
            from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

            connector_result = await GitHubMCPSpatialAdapter().list_branches_connector(_user_id)
            if connector_result.items is not None:
                branches = connector_result.items
                # The connector tool returns branches only; default-branch identification is a
                # separate repo-info read (native path enriches it). Connector path omits it for
                # now — render without the "(default: …)" annotation, never fabricate one.
                default_branch = ""
            elif (
                connector_result.degradation
                and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
            ):
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                github_router = GitHubIntegrationRouter()
                payload = await github_router.list_branches_via_mcp()
                branches = payload.get("branches", [])
                default_branch = payload.get("default_branch", "") or ""
            else:
                # Connected but degraded (REPO_UNRESOLVED "which repo?" / UNREACHABLE / stale) →
                # honest message, never a silent PAT fallback (#1231).
                return IntentProcessingResult(
                    success=True,
                    message=connector_result.degradation.user_message,
                    intent_data={
                        "category": "query",
                        "action": "list_branches_query",
                        "context": {"degraded": connector_result.degradation.reason.value},
                    },
                )

            if branches:
                count = len(branches)

                # Sort: default branch first (if found), then alphabetical
                def _sort_key(b):
                    name = b.get("name", "")
                    return (0 if name == default_branch else 1, name)

                sorted_branches = sorted(branches, key=_sort_key)
                message = f"You have **{count} branch{'es' if count != 1 else ''}**"
                if default_branch:
                    message += f" (default: `{default_branch}`)."
                else:
                    message += "."
                message += "\n"
                for b in sorted_branches[:20]:
                    name = b.get("name", "")
                    flags = []
                    if name == default_branch:
                        flags.append("default")
                    if b.get("protected"):
                        flags.append("protected")
                    flag_suffix = f" ({', '.join(flags)})" if flags else ""
                    message += f"\n- **{name}**{flag_suffix}"
                if count > 20:
                    message += f"\n\n...and {count - 20} more."
            else:
                message = "I don't see any branches for this repository."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "list_branches_query",
                    "context": {
                        "branch_count": len(branches) if branches else 0,
                        "default_branch": default_branch or None,
                    },
                },
            )

        except Exception as e:
            self.logger.error(f"Failed to list branches: {e}")
            return IntentProcessingResult(
                success=True,
                message=(
                    "I wasn't able to fetch branches right now. " "Please try again in a moment."
                ),
                intent_data={
                    "category": "query",
                    "action": "list_branches_query",
                    "context": {"error": str(e)},
                },
            )

    async def _handle_local_git_status_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle local-git status queries (Issue #1044).

        Returns the server's working-tree state: current branch, dirty/clean,
        ahead/behind from upstream. Distinct from #1040 list_branches_query
        which targets GitHub-remote branches via REST.

        Per Pattern-073 discipline: returns verification-bounded observations.
        Errors (not a git repo, GitPython missing) surface as structured
        states with honest messaging rather than fake-OK assertions.
        """
        self.logger.info("Processing local-git status query")
        from services.integrations.local_git import LocalGitInspector

        status = LocalGitInspector().get_status()

        if status.error:
            message = (
                f"I couldn't read the local git state: {status.error}. "
                "This query inspects the server's working directory; if "
                "you're running Piper in a non-git environment, that's "
                "expected."
            )
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": "query",
                    "action": "local_git_status_query",
                    "context": {"error": status.error},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

        parts = [f"You're on **`{status.current_branch}`**"]

        if status.upstream:
            parts.append(f"tracking `{status.upstream}`")

        # Working-tree state — verification-bounded phrasing
        if status.is_clean is True:
            parts.append("with a clean working tree")
        elif status.is_clean is False:
            uncommitted_str = (
                f"{status.uncommitted_files_count} uncommitted file(s)"
                if status.uncommitted_files_count is not None
                else "uncommitted changes"
            )
            untracked_str = ""
            if status.untracked_files_count and status.untracked_files_count > 0:
                untracked_str = f" + {status.untracked_files_count} untracked"
            parts.append(f"with {uncommitted_str}{untracked_str}")
        # else: is_clean is None — we couldn't determine; omit the claim

        message = ", ".join(parts) + "."

        # Ahead/behind on a second line if available
        if status.commits_ahead is not None and status.commits_behind is not None:
            if status.commits_ahead > 0 or status.commits_behind > 0:
                ab_parts = []
                if status.commits_ahead > 0:
                    ab_parts.append(f"{status.commits_ahead} ahead")
                if status.commits_behind > 0:
                    ab_parts.append(f"{status.commits_behind} behind")
                message += f"\n\n📊 {' / '.join(ab_parts)} from `{status.upstream}`."
            else:
                message += f"\n\nIn sync with `{status.upstream}`."

        return IntentProcessingResult(
            success=True,
            message=message,
            intent_data={
                "category": "query",
                "action": "local_git_status_query",
                "context": {
                    "current_branch": status.current_branch,
                    "is_clean": status.is_clean,
                    "uncommitted": status.uncommitted_files_count,
                    "untracked": status.untracked_files_count,
                    "ahead": status.commits_ahead,
                    "behind": status.commits_behind,
                    "upstream": status.upstream,
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
            clarification_type=None,
        )

    async def _handle_meeting_time_query(
        self, intent: Intent, workflow_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle "How much time in meetings?" query.

        Issue #518: Canonical Query #34 - Calendar Cluster
        Issue #586: Added user_id for timezone-aware queries
        Issue #588: Added support for tomorrow/this week/next week via temporal parsing
        Returns total meeting duration for the requested date range.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            user_id: Optional user ID for timezone-aware queries

        Returns:
            IntentProcessingResult with meeting time summary or graceful fallback
        """
        self.logger.info(f"Processing meeting time query: {intent.action}")

        try:
            # Use CalendarIntegrationRouter (CORE-QUERY-1 pattern)
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Issue #588: Parse temporal modifiers (today, tomorrow, this week, etc.)
            from services.intent_service.temporal_utils import parse_relative_date

            # Initialize router with user_id for timezone awareness (Issue #586)
            calendar_router = CalendarIntegrationRouter(user_id=user_id)

            # Check if calendar is configured by attempting authentication
            is_configured = await calendar_router.authenticate()

            if not is_configured:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "Google Calendar isn't connected yet, so I can't see your meetings. "
                        'Ask me "how do I connect Google Calendar?" and I\'ll walk you through it — '
                        "once it's connected I can analyze your meeting time."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Issue #588: Parse date range from original message
            # Note: original_message may be in intent.original_message OR intent.context["original_message"]
            original_message = intent.original_message or intent.context.get("original_message", "")
            start_date, end_date, date_label = parse_relative_date(original_message)

            # Get events for the requested date range
            events = await calendar_router.get_events_in_range(start_date, end_date)

            # Filter to meetings only (exclude all-day events)
            meetings = [e for e in events if not e.get("is_all_day", False)]

            # Issue #588: Use date_label in response (today, tomorrow, this week, etc.)
            date_label_title = date_label.title()  # "today" -> "Today"

            if not meetings:
                message = f"You have no meetings scheduled for {date_label}."
                total_minutes = 0
                meeting_count = 0
            else:
                # Calculate total meeting time
                total_minutes = sum(e.get("duration_minutes", 0) for e in meetings)
                meeting_count = len(meetings)

                # Format time summary
                hours = total_minutes // 60
                minutes = total_minutes % 60

                if hours > 0 and minutes > 0:
                    time_str = f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
                elif hours > 0:
                    time_str = f"{hours} hour{'s' if hours != 1 else ''}"
                else:
                    time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"

                message = f"**Meeting Time {date_label_title}**: {time_str} across {meeting_count} meeting{'s' if meeting_count != 1 else ''}\n\n"

                # Add meeting list
                message += "Meetings:\n"
                for meeting in meetings:
                    summary = meeting.get("summary", "Untitled")
                    duration = meeting.get("duration_minutes", 0)
                    message += f"- {summary} ({duration} min)\n"

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "total_minutes": total_minutes,
                    "meeting_count": meeting_count,
                    "meetings": meetings,
                },
                # Issue #588: Direct response - no workflow polling needed
                workflow_id=None,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Calendar meeting time query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="looking up meeting times",
                error_type="CalendarMeetingTimeQueryError",
            )

    async def _handle_recurring_meetings_query(
        self, intent: Intent, workflow_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle "Review my recurring meetings" query.

        Issue #518: Canonical Query #35 - Calendar Cluster
        Issue #586: Added user_id for timezone-aware queries
        Returns list of recurring meetings with frequency and time commitment.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            user_id: Optional user ID for timezone-aware queries

        Returns:
            IntentProcessingResult with recurring meetings or graceful fallback
        """
        self.logger.info(f"Processing recurring meetings query: {intent.action}")

        try:
            # Use CalendarIntegrationRouter (CORE-QUERY-1 pattern)
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Initialize router with user_id for timezone awareness (Issue #586)
            calendar_router = CalendarIntegrationRouter(user_id=user_id)

            # Check if calendar is configured by attempting authentication
            is_configured = await calendar_router.authenticate()

            if not is_configured:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "Google Calendar isn't connected yet, so I can't see your recurring meetings. "
                        'Ask me "how do I connect Google Calendar?" and I\'ll walk you through it — '
                        "once it's connected I can review what's recurring and how often."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Get recurring meetings via router (Issue #518 fix - CORE-QUERY-1 pattern)
            recurring_meetings = await calendar_router.get_recurring_events(days_ahead=30)

            if not recurring_meetings:
                # #1096 (Pattern-073): the calendar API returned no events;
                # we can only attest to "none found in the queried window".
                message = (
                    "I didn't find any recurring meetings in the calendar "
                    "events I checked for the next 30 days."
                )
            else:
                message = f"**Recurring Meetings** ({len(recurring_meetings)} found):\n\n"

                for meeting in recurring_meetings:
                    summary = meeting["summary"]
                    frequency = meeting["frequency"]
                    duration = meeting["duration_minutes"]
                    message += f"- {summary}\n"
                    message += f"  Frequency: {frequency}\n"
                    if duration > 0:
                        message += f"  Duration: {duration} min per occurrence\n"
                    message += "\n"

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "recurring_count": len(recurring_meetings),
                    "meetings": recurring_meetings,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Calendar recurring meetings query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="checking recurring meetings",
                error_type="CalendarRecurringMeetingsQueryError",
            )

    async def _handle_week_calendar_query(
        self, intent: Intent, workflow_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle "What's my week look like?" query.

        Issue #518: Canonical Query #61 - Calendar Cluster
        Issue #586: Added user_id for timezone-aware queries
        Returns calendar view for the current week (next 7 days).

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            user_id: Optional user ID for timezone-aware queries

        Returns:
            IntentProcessingResult with week calendar view or graceful fallback
        """
        self.logger.info(f"Processing week calendar query: {intent.action}")

        try:
            # Use CalendarIntegrationRouter (CORE-QUERY-1 pattern)
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Initialize router with user_id for timezone awareness (Issue #586)
            calendar_router = CalendarIntegrationRouter(user_id=user_id)

            # Check if calendar is configured by attempting authentication
            is_configured = await calendar_router.authenticate()

            if not is_configured:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "Google Calendar isn't connected yet, so I can't show your week. "
                        'Ask me "how do I connect Google Calendar?" and I\'ll walk you through it — '
                        "once it's connected I can lay out what's on your schedule."
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                    implemented=False,  # Graceful degradation
                )

            # Get events for the next 7 days via router (Issue #518 fix - CORE-QUERY-1 pattern)
            from datetime import datetime, timedelta, timezone

            now = datetime.now(timezone.utc)
            end_date = now + timedelta(days=7)
            events = await calendar_router.get_events_in_range(now, end_date)

            # Process and group events by day
            events_by_day = {}
            for event in events:
                # Get date (not time) from start_time
                start_time = datetime.fromisoformat(event["start_time"])
                date_key = start_time.strftime("%Y-%m-%d")
                day_name = start_time.strftime("%A, %B %d")

                if date_key not in events_by_day:
                    events_by_day[date_key] = {"day_name": day_name, "events": []}

                events_by_day[date_key]["events"].append(event)

            # Format response
            if not events_by_day:
                # #1096 (Pattern-073): the calendar API returned zero events;
                # avoid asserting a stronger claim than the data verified.
                message = (
                    "I didn't find any events in the calendar for the next "
                    "7 days. (If this seems wrong, check that calendar "
                    "permissions cover the expected scope.)"
                )
            else:
                message = "**Your Week Ahead**:\n\n"

                # Sort by date
                sorted_days = sorted(events_by_day.items())

                for date_key, day_data in sorted_days:
                    day_name = day_data["day_name"]
                    day_events = day_data["events"]
                    meeting_count = len([e for e in day_events if not e.get("is_all_day", False)])
                    total_time = sum(
                        e.get("duration_minutes", 0)
                        for e in day_events
                        if not e.get("is_all_day", False)
                    )

                    message += f"**{day_name}** ({meeting_count} meetings, {total_time} min)\n"

                    for event in day_events:
                        summary = event.get("summary", "Untitled")
                        if event.get("is_all_day"):
                            message += f"  - {summary} (All day)\n"
                        else:
                            # Format time
                            start_time = datetime.fromisoformat(event["start_time"])
                            time_str = start_time.strftime("%I:%M %p")
                            duration = event.get("duration_minutes", 0)
                            message += f"  - {time_str}: {summary} ({duration} min)\n"

                    message += "\n"

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "days_count": len(events_by_day),
                    "events_by_day": events_by_day,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Calendar week query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="pulling up your week's calendar",
                error_type="CalendarWeekQueryError",
            )

    async def _handle_productivity_query(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle "What's my productivity this week?" query.

        Issue #518: Canonical Query #51 - Productivity Cluster
        Aggregates metrics from todos and optionally GitHub issues.

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with productivity metrics summary
        """
        self.logger.info(f"Processing productivity query: {intent.action}")

        try:
            from datetime import datetime, timedelta, timezone

            from services.repositories.todo_repository import TodoRepository

            # Get todo completion stats for the past 7 days
            async with AsyncSessionFactory.session_scope() as session:
                todo_repo = TodoRepository(session)
                todo_stats = await todo_repo.get_completion_stats(owner_id=session_id, days=7)

            # Try to get GitHub stats if configured
            github_stats = None
            try:
                from services.integrations.github.github_integration_router import (
                    GitHubIntegrationRouter,
                )

                # Issue #891: pass user_id for token lookup
                github_router = GitHubIntegrationRouter()
                _user_id = _principal_from_intent(intent)
                await github_router.initialize(user_id=_user_id)

                if github_router.config_service.is_configured(_user_id or "system"):
                    # Get closed issues from past 7 days
                    closed_items = await github_router.get_closed_issues(limit=100)

                    now = datetime.now(timezone.utc)
                    week_ago = now - timedelta(days=7)

                    recent_closed = []
                    for item in closed_items:
                        closed_at_str = item.get("closed_at")
                        if closed_at_str:
                            closed_at = datetime.fromisoformat(closed_at_str.replace("Z", "+00:00"))
                            if closed_at >= week_ago:
                                recent_closed.append(item)

                    github_stats = {
                        "issues_closed": len(recent_closed),
                        "items": recent_closed,
                    }

            except Exception as gh_error:
                self.logger.warning(f"GitHub productivity metrics unavailable: {gh_error}")
                # Continue without GitHub stats

            # Format productivity summary
            lines = ["**Productivity Summary (Past 7 Days)**\n"]

            # Todo metrics
            lines.append("**Tasks:**")
            lines.append(f"- Completed: {todo_stats['completed']}")
            lines.append(f"- Created: {todo_stats['total_created']}")
            lines.append(f"- Active: {todo_stats['active']}")
            if todo_stats["total_created"] > 0:
                completion_rate = todo_stats["completion_rate"]
                lines.append(f"- Completion Rate: {completion_rate:.1f}%")

            # GitHub metrics (if available)
            if github_stats:
                lines.append("\n**GitHub:**")
                lines.append(f"- Issues/PRs Closed: {github_stats['issues_closed']}")

            # Overall assessment
            lines.append("\n**Assessment:**")
            total_completed = todo_stats["completed"] + (
                github_stats["issues_closed"] if github_stats else 0
            )

            if total_completed == 0:
                lines.append(
                    "No completed items this week. Consider setting some achievable goals!"
                )
            elif total_completed < 5:
                lines.append(
                    f"Light week with {total_completed} items completed. Keep building momentum!"
                )
            elif total_completed < 15:
                lines.append(
                    f"Solid progress with {total_completed} items completed. You're making steady headway!"
                )
            else:
                lines.append(
                    f"Highly productive week with {total_completed} items completed. Excellent work!"
                )

            message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "todo_stats": todo_stats,
                    "github_stats": github_stats,
                    "total_completed": total_completed,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Productivity query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="analyzing productivity",
                error_type="ProductivityQueryError",
            )

    async def _handle_changes_query(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle "What changed since X?" query.

        Issue #521: Canonical Query #29 - Contextual Intelligence
        Parses time expressions and aggregates activity from:
        - AuditLog table (user actions)
        - Entity timestamps (todos, projects, files)

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with activity summary grouped by type
        """
        self.logger.info(f"Processing changes query: {intent.action}")

        try:
            from datetime import datetime, timedelta, timezone

            from services.repositories.todo_repository import TodoRepository

            # Parse time expression from intent context
            original_message = intent.context.get("original_message", "").lower()

            # Parse time range
            time_range_days = self._parse_time_expression(original_message)

            now = datetime.now(timezone.utc)
            since_time = now - timedelta(days=time_range_days)

            # 1. Get audit log activity
            audit_activity = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    from services.database.models import AuditLog

                    result = await session.execute(
                        select(AuditLog)
                        .where(
                            and_(AuditLog.user_id == session_id, AuditLog.created_at >= since_time)
                        )
                        .order_by(AuditLog.created_at.desc())
                        .limit(50)
                    )
                    audit_logs = result.scalars().all()

                    for log in audit_logs:
                        audit_activity.append(
                            {
                                "type": "audit",
                                "action": log.action,
                                "event_type": log.event_type,
                                "message": log.message,
                                "timestamp": log.created_at.isoformat(),
                            }
                        )
            except Exception as audit_error:
                self.logger.warning(f"Failed to fetch audit logs: {audit_error}")

            # 2. Get todo activity (created/updated/completed)
            todo_activity = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    todo_repo = TodoRepository(session)
                    from services.database.models import TodoDB

                    # Query for todos created or updated since time range
                    result = await session.execute(
                        select(TodoDB)
                        .where(
                            and_(
                                TodoDB.owner_id == session_id,
                                or_(
                                    TodoDB.created_at >= since_time,
                                    TodoDB.updated_at >= since_time,
                                    TodoDB.completed_at >= since_time,
                                ),
                            )
                        )
                        .order_by(TodoDB.updated_at.desc())
                        .limit(50)
                    )
                    todos = result.scalars().all()

                    for todo in todos:
                        # Determine activity type
                        if todo.completed_at and todo.completed_at >= since_time:
                            activity_type = "completed"
                            timestamp = todo.completed_at
                        elif todo.updated_at >= since_time and todo.created_at < since_time:
                            activity_type = "updated"
                            timestamp = todo.updated_at
                        else:
                            activity_type = "created"
                            timestamp = todo.created_at

                        todo_activity.append(
                            {
                                "type": "todo",
                                "activity": activity_type,
                                "text": todo.text,
                                "priority": todo.priority,
                                "timestamp": timestamp.isoformat() if timestamp else None,
                            }
                        )
            except Exception as todo_error:
                self.logger.warning(f"Failed to fetch todo activity: {todo_error}")

            # 3. Get project activity (created/updated)
            project_activity = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    from services.database.models import ProjectDB

                    result = await session.execute(
                        select(ProjectDB)
                        .where(
                            and_(
                                ProjectDB.owner_id == session_id,
                                or_(
                                    ProjectDB.created_at >= since_time,
                                    ProjectDB.updated_at >= since_time,
                                ),
                            )
                        )
                        .order_by(ProjectDB.updated_at.desc())
                        .limit(20)
                    )
                    projects = result.scalars().all()

                    for project in projects:
                        activity_type = "created" if project.created_at >= since_time else "updated"
                        project_activity.append(
                            {
                                "type": "project",
                                "activity": activity_type,
                                "name": project.name,
                                "timestamp": (
                                    project.updated_at.isoformat() if project.updated_at else None
                                ),
                            }
                        )
            except Exception as project_error:
                self.logger.warning(f"Failed to fetch project activity: {project_error}")

            # Format response
            time_desc = self._format_time_range(time_range_days)
            total_activities = len(audit_activity) + len(todo_activity) + len(project_activity)

            if total_activities == 0:
                message = f"No activity detected {time_desc}."
            else:
                lines = [f"**Activity Summary {time_desc}** ({total_activities} items)\n"]

                # Group and format by type
                if todo_activity:
                    lines.append(f"**Tasks** ({len(todo_activity)}):")
                    # Group by activity type
                    created = [t for t in todo_activity if t["activity"] == "created"]
                    updated = [t for t in todo_activity if t["activity"] == "updated"]
                    completed = [t for t in todo_activity if t["activity"] == "completed"]

                    if created:
                        lines.append(f"  Created: {len(created)}")
                        for item in created[:3]:  # Show first 3
                            lines.append(f"    - {item['text']}")
                    if updated:
                        lines.append(f"  Updated: {len(updated)}")
                    if completed:
                        lines.append(f"  Completed: {len(completed)}")
                        for item in completed[:3]:
                            lines.append(f"    - {item['text']}")
                    lines.append("")

                if project_activity:
                    lines.append(f"**Projects** ({len(project_activity)}):")
                    for proj in project_activity[:5]:
                        lines.append(f"  - {proj['activity'].capitalize()}: {proj['name']}")
                    lines.append("")

                if audit_activity:
                    lines.append(f"**Actions** ({len(audit_activity)}):")
                    # Group by event type
                    event_counts = {}
                    for event in audit_activity:
                        event_type = event.get("event_type", "unknown")
                        event_counts[event_type] = event_counts.get(event_type, 0) + 1

                    for event_type, count in sorted(
                        event_counts.items(), key=lambda x: x[1], reverse=True
                    )[:5]:
                        lines.append(f"  - {event_type}: {count}")

                message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "time_range_days": time_range_days,
                    "total_activities": total_activities,
                    "todo_activity": todo_activity,
                    "project_activity": project_activity,
                    "audit_activity": audit_activity,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Changes query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="looking at recent changes",
                error_type="ChangesQueryError",
            )

    async def _handle_attention_query(
        self, intent: Intent, workflow_id: str, session_id: str, user_id: Optional[str] = None
    ) -> IntentProcessingResult:
        """
        Handle "What needs my attention?" query.

        Issue #521: Canonical Query #30 - Contextual Intelligence
        Aggregates attention items from:
        - High-priority todos
        - Overdue items
        - Calendar urgency (upcoming meetings)
        - Stale projects

        Args:
            intent: The classified intent
            workflow_id: Current workflow ID
            session_id: User session ID

        Returns:
            IntentProcessingResult with prioritized attention list
        """
        self.logger.info(f"Processing attention query: {intent.action}")

        try:
            from datetime import datetime, timedelta, timezone

            from services.repositories.todo_repository import TodoRepository

            now = datetime.now(timezone.utc)
            attention_items = []

            # 1. High-priority todos
            high_priority_todos = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    todo_repo = TodoRepository(session)
                    from services.database.models import TodoDB

                    result = await session.execute(
                        select(TodoDB)
                        .where(
                            and_(
                                TodoDB.owner_id == session_id,
                                TodoDB.completed == False,
                                TodoDB.priority.in_(["urgent", "high"]),
                            )
                        )
                        .order_by(TodoDB.priority.desc())
                        .limit(10)
                    )
                    todos = result.scalars().all()

                    for todo in todos:
                        high_priority_todos.append(
                            {
                                "type": "high_priority_todo",
                                "text": todo.text,
                                "priority": todo.priority,
                                "urgency": "urgent" if todo.priority == "urgent" else "high",
                            }
                        )
                        attention_items.append(
                            {
                                "category": "Priority",
                                "item": todo.text,
                                "urgency": "urgent" if todo.priority == "urgent" else "high",
                                "icon": "🔴" if todo.priority == "urgent" else "🟠",
                            }
                        )
            except Exception as priority_error:
                self.logger.warning(f"Failed to fetch priority todos: {priority_error}")

            # 2. Overdue todos
            overdue_todos = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    from services.database.models import TodoDB

                    result = await session.execute(
                        select(TodoDB)
                        .where(
                            and_(
                                TodoDB.owner_id == session_id,
                                TodoDB.completed == False,
                                TodoDB.due_date.isnot(None),
                                TodoDB.due_date < now,
                            )
                        )
                        .order_by(TodoDB.due_date.asc())
                        .limit(10)
                    )
                    todos = result.scalars().all()

                    for todo in todos:
                        days_overdue = (now - todo.due_date).days if todo.due_date else 0
                        overdue_todos.append(
                            {
                                "type": "overdue_todo",
                                "text": todo.text,
                                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                                "days_overdue": days_overdue,
                            }
                        )
                        attention_items.append(
                            {
                                "category": "Overdue",
                                "item": todo.text,
                                "urgency": "urgent" if days_overdue > 7 else "high",
                                "icon": "⏰",
                                "detail": f"{days_overdue} days overdue",
                            }
                        )
            except Exception as overdue_error:
                self.logger.warning(f"Failed to fetch overdue todos: {overdue_error}")

            # 3. Calendar urgency (upcoming meetings in next 2 hours)
            # Issue #518 fix - Use CalendarIntegrationRouter (CORE-QUERY-1 pattern)
            upcoming_meetings = []
            try:
                from services.integrations.calendar.calendar_integration_router import (
                    CalendarIntegrationRouter,
                )

                # Issue #849: Thread user_id for user-scoped calendar auth
                calendar_router = CalendarIntegrationRouter(user_id=user_id)
                is_configured = await calendar_router.authenticate()

                if is_configured:
                    events = await calendar_router.get_todays_events()
                    two_hours_from_now = now + timedelta(hours=2)

                    for event in events:
                        if not event.get("is_all_day", False):
                            start_time_str = event.get("start_time")
                            if start_time_str:
                                try:
                                    start_time = datetime.fromisoformat(
                                        start_time_str.replace("Z", "+00:00")
                                    )
                                    if now <= start_time <= two_hours_from_now:
                                        minutes_until = int((start_time - now).total_seconds() / 60)
                                        upcoming_meetings.append(
                                            {
                                                "type": "upcoming_meeting",
                                                "summary": event.get("summary", "Untitled"),
                                                "start_time": start_time_str,
                                                "minutes_until": minutes_until,
                                            }
                                        )
                                        attention_items.append(
                                            {
                                                "category": "Upcoming",
                                                "item": event.get("summary", "Untitled"),
                                                "urgency": "medium",
                                                "icon": "📅",
                                                "detail": f"in {minutes_until} min",
                                            }
                                        )
                                except Exception as parse_error:
                                    self.logger.warning(
                                        f"Failed to parse event time: {parse_error}"
                                    )
            except Exception as calendar_error:
                self.logger.warning(f"Calendar urgency check unavailable: {calendar_error}")

            # 4. Stale projects (no activity in 7+ days)
            stale_projects = []
            try:
                async with AsyncSessionFactory.session_scope() as session:
                    from services.database.models import ProjectDB

                    week_ago = now - timedelta(days=7)
                    result = await session.execute(
                        select(ProjectDB)
                        .where(
                            and_(
                                ProjectDB.owner_id == session_id,
                                ProjectDB.is_archived == False,
                                ProjectDB.updated_at < week_ago,
                            )
                        )
                        .order_by(ProjectDB.updated_at.asc())
                        .limit(5)
                    )
                    projects = result.scalars().all()

                    for project in projects:
                        days_stale = (now - project.updated_at).days if project.updated_at else 0
                        stale_projects.append(
                            {
                                "type": "stale_project",
                                "name": project.name,
                                "last_updated": (
                                    project.updated_at.isoformat() if project.updated_at else None
                                ),
                                "days_stale": days_stale,
                            }
                        )
                        attention_items.append(
                            {
                                "category": "Stale",
                                "item": project.name,
                                "urgency": "low",
                                "icon": "💤",
                                "detail": f"{days_stale} days inactive",
                            }
                        )
            except Exception as stale_error:
                self.logger.warning(f"Failed to fetch stale projects: {stale_error}")

            # Format response
            if not attention_items:
                # Issue #1069: source-transparent empty-state. The previous
                # wording ("Everything looks good!") asserted a positive state
                # without naming what was checked — scored as fabrication-shaped
                # in Colleague Test rubric (Q30 R=1 C=0 T=1 across Runs 4-7).
                # Naming the surfaces and acknowledging the limits keeps the
                # claim honest and invites follow-up.
                message = (
                    "I don't see anything urgent across your high-priority todos, "
                    "overdue items, upcoming meetings, or stale projects. "
                    "There may be other signals I haven't checked — let me know if "
                    "there's a specific area you want me to look at."
                )
            else:
                lines = [f"**Items Needing Attention** ({len(attention_items)})\n"]

                # Sort by urgency (urgent > high > medium > low)
                urgency_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
                sorted_items = sorted(
                    attention_items, key=lambda x: urgency_order.get(x["urgency"], 4)
                )

                # Group by category
                current_category = None
                for item in sorted_items:
                    if item["category"] != current_category:
                        current_category = item["category"]
                        lines.append(f"\n**{current_category}:**")

                    detail_str = f" ({item['detail']})" if "detail" in item else ""
                    lines.append(f"{item['icon']} {item['item']}{detail_str}")

                message = "\n".join(lines)

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "total_attention_items": len(attention_items),
                    "high_priority_todos": high_priority_todos,
                    "overdue_todos": overdue_todos,
                    "upcoming_meetings": upcoming_meetings,
                    "stale_projects": stale_projects,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Attention query error: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="finding items that need attention",
                error_type="AttentionQueryError",
            )

    def _parse_time_expression(self, message: str) -> int:
        """
        Parse time expression from natural language to days.

        Examples:
            "since yesterday" -> 1
            "since Monday" -> ~days since last Monday
            "in the last hour" -> 0 (partial day)
            "since last week" -> 7

        Args:
            message: Natural language message

        Returns:
            Number of days in the time range
        """
        message_lower = message.lower()

        # Yesterday
        if "yesterday" in message_lower:
            return 1

        # Hours
        if "hour" in message_lower:
            if "last hour" in message_lower or "past hour" in message_lower:
                return 0  # Partial day
            # Extract number of hours
            import re

            match = re.search(r"(\d+)\s*hours?", message_lower)
            if match:
                hours = int(match.group(1))
                return max(0, hours // 24)  # Convert to days
            return 0

        # Days
        if "day" in message_lower:
            import re

            match = re.search(r"(\d+)\s*days?", message_lower)
            if match:
                return int(match.group(1))
            if "last day" in message_lower or "past day" in message_lower:
                return 1
            return 1

        # Week
        if "week" in message_lower:
            if "last week" in message_lower or "past week" in message_lower:
                return 7
            import re

            match = re.search(r"(\d+)\s*weeks?", message_lower)
            if match:
                return int(match.group(1)) * 7
            return 7

        # Month
        if "month" in message_lower:
            import re

            match = re.search(r"(\d+)\s*months?", message_lower)
            if match:
                return int(match.group(1)) * 30
            return 30

        # Day of week (Monday, Tuesday, etc.)
        days_of_week = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        for day in days_of_week:
            if day in message_lower:
                # Calculate days since that day
                from datetime import datetime

                today = datetime.now()
                target_day = days_of_week.index(day)
                current_day = today.weekday()

                if current_day >= target_day:
                    days_ago = current_day - target_day
                else:
                    days_ago = 7 - (target_day - current_day)

                return max(1, days_ago)

        # Default to 1 day if can't parse
        return 1

    def _format_time_range(self, days: int) -> str:
        """
        Format time range as human-readable string.

        Args:
            days: Number of days

        Returns:
            Formatted string like "since yesterday", "in the past 7 days"
        """
        if days == 0:
            return "in the past hour"
        elif days == 1:
            return "since yesterday"
        elif days == 7:
            return "in the past week"
        elif days == 30:
            return "in the past month"
        else:
            return f"in the past {days} days"

    async def _handle_execution_intent(
        self, intent: Intent, workflow, session_id: str, user_id: str = None
    ) -> IntentProcessingResult:
        """
        Handle EXECUTION category intents.

        Routes to appropriate domain service based on intent action.
        Follows QUERY pattern for consistency.

        GREAT-4D Phase 1: Replaces Phase 3C placeholder.
        Issue #284: Added ActionMapper to handle classifier/handler name mismatches.
        Issue #744: Added user_id parameter for todo operations (multi-tenancy).
        Issue #883: workflow may be None (lazy creation).
        """
        self.logger.info(f"Processing EXECUTION intent: {intent.action}")
        # Issue #883: Extract workflow_id safely
        workflow_id = getattr(workflow, "id", None)

        # Issue #284: Map classifier action to handler method name
        mapped_action = ActionMapper.map_action(intent.action)
        self.logger.debug(f"Action routing: '{intent.action}' -> '{mapped_action}'")

        # Route based on mapped action
        if mapped_action in ["create_issue", "create_ticket"]:
            return await self._handle_create_issue(intent, workflow_id, session_id, user_id=user_id)

        elif mapped_action in ["update_issue", "update_ticket"]:
            return await self._handle_update_issue(intent, workflow_id, user_id=user_id)

        # Issue #285: Todo operations routing
        # Issue #744: Convert user_id string to UUID for multi-tenancy support
        elif mapped_action == "create_todo":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to manage todos. Please log in and try again.",
                    intent_data={"category": intent.category.value, "action": intent.action},
                    workflow_id=workflow_id,
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_create_todo(
                intent, session_id, user_id=todo_user_id
            )
            # Issue #748: Don't return workflow_id for synchronous operations
            # The frontend polls workflow_id, but todo ops are already complete
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        # Issue #903: Reminder creation
        elif mapped_action == "create_reminder":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to set reminders. Please log in and try again.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_create_reminder(
                intent, session_id, user_id=todo_user_id
            )
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        elif mapped_action == "list_todos":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to show your todos. Please log in and try again.",
                    intent_data={"category": intent.category.value, "action": intent.action},
                    workflow_id=workflow_id,
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_list_todos(
                intent, session_id, user_id=todo_user_id
            )
            # Issue #748: Don't return workflow_id for synchronous operations
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        elif mapped_action == "next_todo":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to show your next todo. Please log in and try again.",
                    intent_data={"category": intent.category.value, "action": intent.action},
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_next_todo(
                intent, session_id, user_id=todo_user_id
            )
            # Issue #748: Don't return workflow_id for synchronous operations
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        elif mapped_action == "complete_todo":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to complete todos. Please log in and try again.",
                    intent_data={"category": intent.category.value, "action": intent.action},
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_complete_todo(
                intent, session_id, user_id=todo_user_id
            )
            # Issue #748: Don't return workflow_id for synchronous operations
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        elif mapped_action == "delete_todo":
            todo_user_id = UUID(user_id) if user_id else None
            if not todo_user_id:
                return IntentProcessingResult(
                    success=False,
                    message="I need you to be logged in to delete todos. Please log in and try again.",
                    intent_data={"category": intent.category.value, "action": intent.action},
                    error="User not authenticated",
                    error_type="AuthenticationRequired",
                )
            message = await self.todo_handlers.handle_delete_todo(
                intent, session_id, user_id=todo_user_id
            )
            # Issue #748: Don't return workflow_id for synchronous operations
            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
            )

        else:
            # Issue #489: Graceful degradation for unhandled EXECUTION actions
            # Issue #886: Contextual fallback copy (CXO guidance)
            # Issue #907: Route generic fallback through conversational floor
            self.logger.info(
                f"Unhandled EXECUTION action: {mapped_action} (original: {intent.action}) - checking contextual fallback"
            )

            # Try specific contextual fallback first (#886 — these are genuinely
            # useful "I can't do X but I can do Y" responses)
            specific_fallback = self._get_contextual_fallback(
                mapped_action=mapped_action,
                original_message=intent.original_message,
            )

            # #1333 (Arch-ruled 2026-06-30): an EXECUTION action that reaches this branch
            # has NO registered handler (not in the rail's get_action_workflows AND not
            # mapped by ActionMapper above) — it is, BY CONSTRUCTION, unwired. It must
            # DETERMINISTICALLY honest-decline. It must NEVER route to the conversational
            # floor, which — being a helpful LLM — confabulates a success ("done ✓") for
            # an action that never ran (the #1331 trust-breaker PM hit). This DERIVES the
            # decline from "reached this branch" — no hand-maintained action list (the
            # former unwired_writes.UNWIRED_WRITE_ACTIONS registration is retired; the
            # branch itself is the signal — Arch's derive-don't-list contract). Curated
            # per-action copy still wins; otherwise a curated/generic honest decline.
            if specific_fallback == self._GENERIC_FALLBACK_TEXT:
                from services.intent_service.unwired_writes import get_unwired_write_decline

                fallback_message = get_unwired_write_decline(intent.action)
                self.logger.info(
                    "unwired_execution_honest_degrade_1333",
                    action=intent.action,
                    mapped_action=mapped_action,
                )
            else:
                fallback_message = specific_fallback

            return IntentProcessingResult(
                success=True,  # honest decline, not an error (avoid 422)
                message=fallback_message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "mapped_action": mapped_action,
                    "confidence": intent.confidence,
                    "unhandled": True,  # Flag for analytics
                    # #1333: unwired EXECUTION now honest-declines deterministically;
                    # it NEVER reaches the floor (floor_hit retired for this path).
                    "unwired_action": True,
                },
                # Issue #878: No handler ran — don't set workflow_id or frontend will poll and timeout
                workflow_id=None,
                requires_clarification=False,
                error=None,  # No error - graceful degradation
                error_type=None,
            )

    def _get_contextual_fallback(self, mapped_action: str, original_message: str) -> str:
        """
        Issue #886: Return contextual fallback copy for not-implemented capabilities.

        Instead of a generic "I don't have that capability yet" message, return
        a colleague-level response that acknowledges what the user asked, explains
        the limitation, and suggests a concrete next step using existing capabilities.

        Copy authored by CXO (memo-cxo-contextual-fallbacks-2026-03-13).
        """
        msg_lower = original_message.lower().strip() if original_message else ""

        # Issue #886: Contextual fallback lookup.
        # Match on keywords in the original message to select the right copy.
        # Order: most specific patterns first, generic fallback last.

        # Scheduling: "schedule a meeting", "set up a meeting"
        if any(
            kw in msg_lower for kw in ["schedule a meeting", "set up a meeting", "book a meeting"]
        ):
            return (
                "I can't create calendar events yet — that's coming soon. "
                "Want me to create a GitHub issue to track this meeting topic, "
                "or draft an agenda you can paste into your calendar invite?"
            )

        # Reminders: "remind me"
        if "remind me" in msg_lower or "set a reminder" in msg_lower:
            return (
                "I can't set reminders yet, but I can add a todo for that "
                "so it shows up in your task list. Want me to do that?"
            )

        # Document creation: "create a doc", "create a document"
        if any(kw in msg_lower for kw in ["create a doc", "create a document", "make a doc"]):
            return (
                "I can't create documents yet. If you'd like to capture something "
                "from our conversation, I can summarize the key points so you can "
                "copy them into a doc."
            )

        # Batch issue creation: "create issues from", "action items"
        if any(
            kw in msg_lower
            for kw in [
                "create issues from",
                "action items",
                "batch create",
                "issues from this meeting",
            ]
        ):
            return (
                "I can't batch-create issues from a meeting yet, but I can create "
                "them one at a time. Want to walk through the action items? "
                "Just tell me the first one."
            )

        # Close issues — redirect to the working QUERY handler
        if "close" in msg_lower and ("issue" in msg_lower or "completed" in msg_lower):
            return (
                "I can close issues! Just tell me the issue number, like "
                "'close issue #123'. Which issue would you like to close?"
            )

        # Reopen issues — redirect to the working QUERY handler
        if "reopen" in msg_lower and "issue" in msg_lower:
            return (
                "I can reopen issues! Just tell me the issue number, like "
                "'reopen issue #123'. Which issue would you like to reopen?"
            )

        # Post to Slack: "post" + ("channel" or "slack" or "team")
        if "post" in msg_lower and any(kw in msg_lower for kw in ["channel", "slack", "team"]):
            return (
                "I can't post to Slack channels yet. I can help you draft the "
                "message though — then you can paste it into the channel. "
                "Want me to format an update?"
            )

        # Complete todo: removed — #904 implemented todo completion.
        # This fallback was factually wrong. Todo completion is now handled
        # by the pre-classifier and todo_handlers.

        # Upload file: "upload" + ("file" or "knowledge")
        if "upload" in msg_lower and any(kw in msg_lower for kw in ["file", "knowledge"]):
            return (
                "I can't accept file uploads yet. If you paste the content here, "
                "I can analyze it — or you can add files directly to Notion and "
                "I'll be able to search them."
            )

        # Generic fallback (Issue #489 original)
        # Issue #907: Now a class constant so the caller can detect it
        # and route through the conversational floor instead.
        return self._GENERIC_FALLBACK_TEXT

    async def _handle_create_issue(
        self, intent: Intent, workflow_id: str, session_id: str, user_id: str = None
    ) -> IntentProcessingResult:
        """
        Handle create_issue/create_ticket action.

        Creates GitHub issue using domain service.

        GREAT-4D Phase 1: First EXECUTION handler implementation.
        Issue #494: Added better defaults from PIPER.md config.
        Issue #943: Added pre-flight check for GitHub configuration.
        """
        # Issue #943: Pre-flight check — verify GitHub is configured
        # Simplified: just check for GITHUB_TOKEN before attempting any API call
        import os

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            # Also check keychain
            try:
                from services.infrastructure.keychain_service import KeychainService

                github_token = KeychainService().get_api_key("github")
            except Exception:
                pass

        if not github_token:
            return IntentProcessingResult(
                success=True,
                message=(
                    "GitHub isn't connected yet. To create issues, you'll need to add a "
                    "GITHUB_TOKEN to your environment or configure it in Settings. "
                    "Once that's set up, I can create and manage GitHub issues for you!"
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        try:
            from services.configuration.piper_config_loader import piper_config_loader
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Issue #494: Load GitHub config for defaults
            github_config = piper_config_loader.load_github_config()

            # Extract issue details from intent
            title = intent.context.get("title") or f"Issue: {intent.original_message[:50]}"
            description = intent.context.get("description") or intent.original_message
            repository = intent.context.get("repository") or intent.context.get("repo")

            # Issue #494: Fall back to default repository from config
            if not repository:
                repository = github_config.default_repository
                self.logger.info(
                    f"Using default repository from config: {repository}",
                    extra={"repository": repository, "session_id": session_id},
                )

            # Issue #1212: graceful degradation. If no repo was named in the
            # request AND no valid default is configured, `repository` is empty /
            # not "owner/repo" — calling create_issue with it raises "Repository
            # must be in 'owner/repo' format", which UserFriendlyErrorService has
            # no pattern for, so it surfaced the generic "Something unexpected
            # happened" (Q16). Degrade honestly + actionably instead, like the
            # missing-token pre-flight above.
            if not repository or "/" not in repository:
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I couldn't tell which repository to create the issue in. "
                        "Set a default repository in Settings → GitHub, or tell me "
                        'which one — e.g. "create an issue in owner/repo about testing."'
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                )

            # Issue #494: Use default labels from config if none specified
            labels = intent.context.get("labels")
            if not labels and github_config.default_labels:
                labels = github_config.default_labels

            # Create issue
            issue = await github_service.create_issue(
                repo_name=repository,
                title=title,
                body=description,
                labels=labels or [],
                assignees=intent.context.get("assignees", []),
            )

            # Issue #494: Include repository info in success message
            repo_short = repository.split("/")[-1] if "/" in repository else repository
            return IntentProcessingResult(
                success=True,
                message=f"Created issue #{issue.get('number')} in {repo_short}: {issue.get('title')}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue.get("number"),
                    "issue_url": issue.get("html_url"),
                    "repository": repository,
                    "used_default_repo": not intent.context.get(
                        "repository"
                    ),  # Issue #494: Track if default was used
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to create issue: {e}")
            error_str = str(e).lower()
            # #943: Detect configuration issues and give actionable message
            if any(
                term in error_str
                for term in [
                    "not configured",
                    "no response",
                    "unauthorized",
                    "401",
                    "403",
                    "bad credentials",
                    "token",
                    "authentication",
                    "api session",
                ]
            ):
                return IntentProcessingResult(
                    success=True,
                    message=(
                        "I wasn't able to create that GitHub issue — it looks like GitHub "
                        "isn't fully connected yet. Check that your GITHUB_TOKEN is set and valid "
                        "in your environment or Settings. Once that's sorted, I can create and "
                        "manage issues for you!"
                    ),
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=False,
                )
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="creating a new issue",
                error_type="GitHubError",
            )

    async def _handle_update_issue(
        self, intent: Intent, workflow_id: str, user_id: str = None
    ) -> IntentProcessingResult:
        """
        Handle update_issue/update_ticket action.

        Updates existing GitHub issue using domain service.

        GREAT-4D Phase 1: FULLY IMPLEMENTED
        Issue #943: Added pre-flight check for GitHub configuration.
        """
        # Issue #943: Pre-flight check — verify GitHub is configured
        import os

        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            try:
                from services.infrastructure.keychain_service import KeychainService

                github_token = KeychainService().get_api_key("github")
            except Exception:
                pass

        if not github_token:
            return IntentProcessingResult(
                success=True,
                message=(
                    "GitHub isn't connected yet. To update issues, you'll need to add a "
                    "GITHUB_TOKEN to your environment or configure it in Settings. "
                    "Once that's set up, I can manage GitHub issues for you!"
                ),
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        try:
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Extract parameters from intent
            issue_number = intent.context.get("issue_number")
            repository = intent.context.get("repository") or intent.context.get("repo")
            title = intent.context.get("title")
            body = intent.context.get("body") or intent.context.get("description")
            state = intent.context.get("state")
            labels = intent.context.get("labels")
            assignees = intent.context.get("assignees")

            # Issue #1066: Fall back to parsing #N from original_message if LLM
            # extraction didn't populate issue_number. Matches the pattern
            # already used by _handle_review_issue_query (line 3181) and the
            # other GitHub mutation handlers.
            if not issue_number:
                import re as _re

                original_message = intent.original_message or intent.context.get(
                    "original_message", ""
                )
                _m = _re.search(r"#?(\d+)", original_message)
                if _m:
                    issue_number = int(_m.group(1))

            # Validate required parameters
            if not issue_number:
                return IntentProcessingResult(
                    success=False,
                    message="I couldn't find an issue number in your request. Please specify an issue number (e.g., 'update issue #123').",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="issue_number_required",
                )

            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot update issue: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Ensure at least one field to update is provided
            if not any([title, body, state, labels, assignees]):
                return IntentProcessingResult(
                    success=False,
                    message="Cannot update issue: no fields to update specified. Please provide at least one field to update (title, body, state, labels, or assignees).",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="update_fields_required",
                )

            # Update issue
            updated_issue = await github_service.update_issue(
                repo_name=repository,
                issue_number=issue_number,
                title=title,
                body=body,
                state=state,
                labels=labels,
                assignees=assignees,
            )

            return IntentProcessingResult(
                success=True,
                message=f"Updated issue #{updated_issue.get('number')}: {updated_issue.get('title')}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": updated_issue.get("number"),
                    "title": updated_issue.get("title"),
                    "state": updated_issue.get("state"),
                    "issue_url": updated_issue.get("html_url"),
                    "repository": repository,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to update issue: {e}")
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="updating that issue",
                error_type="GitHubError",
            )

    async def _handle_analysis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle ANALYSIS category intents.

        Routes to appropriate analysis service based on intent action.
        Follows EXECUTION/QUERY pattern for consistency.

        GREAT-4D Phase 2: Replaces Phase 3C placeholder.
        Issue #515: Added analyze_document routing to Notion
        Issue #883: workflow may be None (lazy creation).
        """
        self.logger.info(f"Processing ANALYSIS intent: {intent.action}")
        # Issue #883: Extract workflow_id safely
        workflow_id = getattr(workflow, "id", None)

        # #1124: the ANALYSIS-category dispatch is fully migrated onto the
        # action-dispatch rail (analyze_document/analyze_file → final-if-heads;
        # analyze_commits/generate_report/analyze_data → _ANALYSIS_QUERY_COHORT, in
        # workflow_entries.py). The rail short-circuits before this routing; handlers
        # reused unchanged. Anything without a rail entry floors here (#916: route to
        # the conversational floor, not a dev stub).
        self.logger.info(
            "analysis_action_routing_to_floor",
            action=intent.action,
            reason="no_specialized_handler",
        )
        return await self._handle_unknown_intent(intent, None, session_id)

    async def _handle_analyze_commits(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle commit analysis requests.

        Analyzes Git commits from specified repository and timeframe.

        GREAT-4D Phase 2: First ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot analyze commits: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)  # Default to 7 days
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service
            github_service = GitHubDomainService()

            # Get recent activity (includes commits)
            self.logger.info(f"Fetching commits for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Extract commits from activity
            commits = activity.get("commits", [])
            commit_count = len(commits)

            # Analyze commits
            authors = {}
            messages = []
            for commit in commits:
                # Extract author info
                author_info = commit.get("commit", {}).get("author", {})
                author_name = author_info.get("name", "Unknown")
                authors[author_name] = authors.get(author_name, 0) + 1

                # Extract message
                message = commit.get("commit", {}).get("message", "").split("\n")[0][:100]
                messages.append(message)

            # Build response message
            if commit_count == 0:
                # #1096 (Pattern-073): "No commits found" is verification-bounded
                # phrasing already (named the repo + timeframe explicitly). Keep
                # the phrasing but flag the audit visit for awareness.
                message = f"No commits found in {repository} over the {timeframe}."
            else:
                author_summary = ", ".join([f"{name} ({count})" for name, count in authors.items()])
                message = f"Analyzed {commit_count} commit{'s' if commit_count != 1 else ''} in {repository} over the {timeframe}. Authors: {author_summary}"

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "repository": repository,
                    "commit_count": commit_count,
                    "timeframe": timeframe,
                    "days": days,
                    "authors": authors,
                    "recent_messages": messages[:5],  # First 5 commit messages
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze commits: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="analyzing commits",
                error_type="AnalysisError",
            )

    async def _handle_generate_report(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle report generation requests.

        Generates markdown reports based on repository activity data.

        GREAT-4D Phase 2B: Second ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")
            report_type = intent.context.get("report_type", "commit_analysis")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot generate report: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)  # Default to 7 days
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service
            github_service = GitHubDomainService()

            # Get recent activity (includes commits, PRs, issues)
            self.logger.info(f"Generating {report_type} report for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Generate report based on type
            if report_type == "commit_analysis":
                report_content = self._format_commit_report(
                    repository=repository, activity=activity, timeframe=timeframe, days=days
                )
            else:
                # Default to commit analysis for unknown types
                report_content = self._format_commit_report(
                    repository=repository, activity=activity, timeframe=timeframe, days=days
                )

            # Build response message
            commits = activity.get("commits", [])
            commit_count = len(commits)
            message = f"Generated {report_type} report for {repository} with {commit_count} commit{'s' if commit_count != 1 else ''} from {timeframe}."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "repository": repository,
                    "report_type": report_type,
                    "timeframe": timeframe,
                    "days": days,
                    "commit_count": commit_count,
                    "content": report_content,
                    "format": "markdown",
                    "generated_at": datetime.now().isoformat(),
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="generating that report",
                error_type="ReportError",
            )

    def _format_commit_report(
        self, repository: str, activity: Dict[str, Any], timeframe: str, days: int
    ) -> str:
        """
        Format commit analysis as markdown report.

        Helper method for _handle_generate_report.
        """
        # Extract data
        commits = activity.get("commits", [])
        commit_count = len(commits)

        # Analyze authors
        authors = {}
        for commit in commits:
            author_info = commit.get("commit", {}).get("author", {})
            author_name = author_info.get("name", "Unknown")
            authors[author_name] = authors.get(author_name, 0) + 1

        # Build markdown report
        report = f"# Commit Analysis Report\n\n"
        report += f"**Repository**: {repository}\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Period**: {timeframe} ({days} days)\n\n"

        report += f"## Summary\n\n"
        report += f"- **Total Commits**: {commit_count}\n"
        report += f"- **Contributors**: {len(authors)}\n\n"

        if authors:
            report += f"## Contributors\n\n"
            for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
                report += f"- **{author}**: {count} commit{'s' if count != 1 else ''}\n"
            report += "\n"

        if commits:
            report += f"## Recent Commits\n\n"
            for commit in commits[:10]:  # First 10
                msg = commit.get("commit", {}).get("message", "No message").split("\n")[0]
                author_info = commit.get("commit", {}).get("author", {})
                author_name = author_info.get("name", "Unknown")
                date_str = author_info.get("date", "Unknown date")
                report += f"- **{msg[:80]}** by {author_name} on {date_str}\n"

        return report

    async def _handle_analyze_data(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle general data analysis requests.

        Analyzes repository data and returns structured insights based on data_type.
        Supports: repository_metrics, activity_trends, contributor_stats

        GREAT-4D Phase 2C: Third ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")
            data_type = intent.context.get("data_type", "repository_metrics")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot analyze data: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Validate data_type
            supported_types = ["repository_metrics", "activity_trends", "contributor_stats"]
            if data_type not in supported_types:
                return IntentProcessingResult(
                    success=False,
                    message=f"Cannot analyze data: unsupported data type '{data_type}'. Supported types: {', '.join(supported_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "data_type": data_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_data_type",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service and fetch data
            github_service = GitHubDomainService()
            self.logger.info(f"Analyzing {data_type} for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Route to appropriate analysis helper
            if data_type == "repository_metrics":
                result_data = self._analyze_repository_metrics(
                    activity, repository, days, timeframe, intent
                )
            elif data_type == "activity_trends":
                result_data = self._analyze_activity_trends(
                    activity, repository, days, timeframe, intent
                )
            elif data_type == "contributor_stats":
                result_data = self._analyze_contributor_stats(
                    activity, repository, days, timeframe, intent
                )

            # Return success
            return IntentProcessingResult(
                success=True,
                message=result_data["message"],
                intent_data=result_data["intent_data"],
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze data: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="analyzing data",
                error_type="AnalysisError",
            )

    def _analyze_repository_metrics(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze repository metrics from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        # Extract counts
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        commit_count = len(commits)
        pr_count = len(prs)
        issues_created_count = len(issues_created)
        issues_closed_count = len(issues_closed)
        total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

        # Calculate distribution percentages
        distribution = {}
        if total_activity > 0:
            distribution = {
                "commits": round((commit_count / total_activity) * 100, 1),
                "prs": round((pr_count / total_activity) * 100, 1),
                "issues_created": round((issues_created_count / total_activity) * 100, 1),
                "issues_closed": round((issues_closed_count / total_activity) * 100, 1),
            }

        # Build message
        message = f"Analyzed repository metrics for {repository} over {timeframe}: {total_activity} total activities ({commit_count} commits, {pr_count} PRs, {issues_created_count} issues created, {issues_closed_count} issues closed)"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "repository_metrics",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_activity_count": total_activity,
                "commits_count": commit_count,
                "prs_count": pr_count,
                "issues_created_count": issues_created_count,
                "issues_closed_count": issues_closed_count,
                "activity_distribution": distribution,
            },
        }

        return {"message": message, "intent_data": intent_data}

    def _analyze_activity_trends(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze activity trends from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        # Extract counts
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        commit_count = len(commits)
        pr_count = len(prs)
        issues_created_count = len(issues_created)
        issues_closed_count = len(issues_closed)
        total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

        # Analyze trends
        trends = {}
        insights = []

        # Most active type
        activity_types = {
            "commits": commit_count,
            "prs": pr_count,
            "issues_created": issues_created_count,
            "issues_closed": issues_closed_count,
        }
        most_active = max(activity_types, key=activity_types.get) if total_activity > 0 else "none"
        trends["most_active_type"] = most_active

        # Issue closure rate
        total_issue_activity = issues_created_count + issues_closed_count
        if total_issue_activity > 0:
            closure_rate = (issues_closed_count / total_issue_activity) * 100
            trends["issue_closure_rate"] = round(closure_rate, 1)
            insights.append(f"Issue closure rate: {round(closure_rate, 1)}%")

        # Commit velocity
        if days > 0:
            commit_velocity = commit_count / days
            trends["commit_velocity"] = f"{round(commit_velocity, 1)} commits/day"
            insights.append(f"Commit velocity: {round(commit_velocity, 1)} commits/day")

        # PR activity
        if pr_count > 0:
            trends["pr_activity"] = f"{pr_count} PRs updated"
            insights.append(f"Active PR development ({pr_count} PRs)")

        # Most active insight
        if total_activity > 0:
            insights.insert(
                0, f"Most active in {most_active} ({activity_types[most_active]} total)"
            )

        # Build message
        message = f"Analyzed activity trends for {repository} over {timeframe}: {total_activity} total activities, most active in {most_active}"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "activity_trends",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_activity_count": total_activity,
                "commits_count": commit_count,
                "prs_count": pr_count,
                "issues_created_count": issues_created_count,
                "issues_closed_count": issues_closed_count,
            },
            "trends": trends,
            "insights": insights,
        }

        return {"message": message, "intent_data": intent_data}

    def _analyze_contributor_stats(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze contributor statistics from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        # Analyze commit authors
        commit_authors = {}
        for commit in commits:
            # Try to get author from commit data structure
            author = commit.get("author", "Unknown")
            # Handle nested author structure
            if isinstance(author, dict):
                author = author.get("name", "Unknown")
            # Also try commit.commit.author.name
            if author == "Unknown":
                commit_data = commit.get("commit", {})
                author_info = commit_data.get("author", {})
                author = author_info.get("name", "Unknown")
            commit_authors[author] = commit_authors.get(author, 0) + 1

        # Analyze PR authors
        pr_authors = {}
        for pr in prs:
            author = pr.get("author", "Unknown")
            pr_authors[author] = pr_authors.get(author, 0) + 1

        # Analyze issue authors (created and closed)
        issue_authors = {}
        for issue in issues_created + issues_closed:
            author = issue.get("author", "Unknown")
            issue_authors[author] = issue_authors.get(author, 0) + 1

        # Get unique contributors
        all_contributors = set()
        all_contributors.update(commit_authors.keys())
        all_contributors.update(pr_authors.keys())
        all_contributors.update(issue_authors.keys())

        # Build insights
        insights = []
        total_contributors = len(all_contributors)
        insights.append(
            f"{total_contributors} total contributor{'s' if total_contributors != 1 else ''} across all activities"
        )

        if commit_authors:
            top_committer = max(commit_authors, key=commit_authors.get)
            insights.append(
                f"{top_committer} is most active committer ({commit_authors[top_committer]} commits)"
            )

        if len(all_contributors) > 1:
            insights.append("Collaboration across commits, PRs, and issues")

        # Build message
        message = f"Analyzed contributor stats for {repository} over {timeframe}: {total_contributors} total contributor{'s' if total_contributors != 1 else ''}"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "contributor_stats",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_contributors": total_contributors,
                "commit_authors": len(commit_authors),
                "pr_authors": len(pr_authors),
                "issue_authors": len(issue_authors),
            },
            "contributors": {"commits": commit_authors, "prs": pr_authors, "issues": issue_authors},
            "insights": insights,
        }

        return {"message": message, "intent_data": intent_data}

    async def _handle_synthesis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle SYNTHESIS category intents.

        Routes to appropriate synthesis service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.
        Issue #883: workflow may be None (lazy creation).

        GREAT-4D Phase 4: Completes intent handler coverage.
        """
        self.logger.info(f"Processing SYNTHESIS intent: {intent.action}")
        # Issue #883: Extract workflow_id safely
        workflow_id = getattr(workflow, "id", None)

        # #1124: `generate_content` / `create_content` MIGRATED to the action-dispatch
        # rail (generate_content_entry in workflow_entries.py); `_handle_generate_content`
        # reused unchanged. The `summarize` / `create_summary` dispatch was DELETED:
        # per #1158 (SUMMARIZE-TAXONOMY) summaries always floor — the verb shim no longer
        # produces the legacy `summarize` action, and removing this branch floors it even
        # if a free-form `summarize` action is ever emitted directly. All synthesis
        # actions without a rail entry route to the conversational floor (the safe default).
        #
        # #1187 fetch-augmentation: for a `summarize` request whose source the floor
        # can't reach (github_issue / commit_range), fetch the content first and inject
        # it via domain_context so the floor summarizes the SOURCE — not just
        # acknowledge it can't reach it. `_fetch_summary_source_content` returns None
        # for floor-direct (text/conversation) / deferred (document) / fetch-failure, so
        # this is a cheap no-op for every non-summarize-of-source synthesis intent.
        summary_dc = None
        fetched = await self._fetch_summary_source_content(intent, workflow_id)
        if fetched:
            _content, _meta = fetched
            summary_dc = {"summary_source": {"content": _content, "metadata": _meta or {}}}
        return await self._handle_unknown_intent(
            intent, workflow, session_id, domain_context=summary_dc
        )

    async def _handle_generate_content(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle content generation requests - SYNTHESIS category.

        Creates new content artifacts (status reports, README sections, issue templates).
        Unlike ANALYSIS handlers that read/analyze data, SYNTHESIS handlers create new content.

        Supported content types:
        - status_report: Generate markdown status report from repository metrics
        - readme_section: Generate README.md section (installation, usage, etc.)
        - issue_template: Generate GitHub issue template (bug_report, feature_request)
        """
        try:
            import time

            start_time = time.time()

            # 1. Validate content_type (required parameter)
            content_type = intent.context.get("content_type")
            if not content_type:
                return IntentProcessingResult(
                    success=False,
                    message="Content type is required for content generation.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="content_type_required",
                )

            # 2. Validate content_type is supported
            valid_types = ["status_report", "readme_section", "issue_template"]
            if content_type not in valid_types:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unsupported content type: {content_type}. Valid types: {', '.join(valid_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "content_type": content_type,
                        "valid_types": valid_types,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_content_type",
                )

            # 3. Route to appropriate helper method
            if content_type == "status_report":
                result = await self._generate_status_report(intent, workflow_id)
            elif content_type == "readme_section":
                result = await self._generate_readme_section(intent, workflow_id)
            elif content_type == "issue_template":
                result = await self._generate_issue_template(intent, workflow_id)

            # 4. Add generation timing to metadata
            generation_time_ms = int((time.time() - start_time) * 1000)
            result.intent_data["generation_time_ms"] = generation_time_ms

            return result

        except Exception as e:
            self.logger.error(f"Failed to generate content: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="generating content",
                error_type="SynthesisError",
            )

    async def _generate_status_report(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate status report from repository metrics.

        Leverages Phase 2C _handle_analyze_data to get repository metrics,
        then applies markdown template to create formatted status report.

        Parameters:
        - repository (optional): Repository to analyze (e.g., "org/repo")
        - days (optional): Days to analyze (default: 7, range: 1-90)
        - data_type (optional): Analysis type (default: "repository_metrics")
          - "repository_metrics": Activity counts and distribution
          - "activity_trends": Trends, velocity, insights
          - "contributor_stats": Contributor analysis
        """
        from datetime import datetime

        # 1. Extract and validate parameters
        repository = intent.context.get("repository")
        if not repository:
            # Try to get from user config or default
            repository = self._get_default_repository()
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Repository is required for status report generation.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "content_type": "status_report",
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

        # Validate and normalize days parameter
        days = intent.context.get("days", 7)
        if not isinstance(days, int) or days < 1 or days > 90:
            days = 7  # Default to 7 days

        # Validate data_type
        data_type = intent.context.get("data_type", "repository_metrics")
        valid_types = ["repository_metrics", "activity_trends", "contributor_stats"]
        if data_type not in valid_types:
            data_type = "repository_metrics"  # Default

        # Get custom title or use default
        title = intent.context.get("title")
        if not title:
            title = f"Status Report: {repository}"

        # 2. Call Phase 2C _handle_analyze_data to get repository metrics
        analysis_intent = Intent(
            original_message=f"analyze data for {repository}",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=1.0,
            context={
                "repository": repository,
                "days": days,
                "data_type": data_type,
            },
        )

        analysis_result = await self._handle_analyze_data(analysis_intent, workflow_id)

        if not analysis_result.success:
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze repository: {analysis_result.message}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "status_report",
                    "repository": repository,
                },
                workflow_id=workflow_id,
                error=analysis_result.error,
                error_type="AnalysisFailed",
            )

        # 3. Extract data from analysis result
        metrics = analysis_result.intent_data.get("metrics", {})
        trends = analysis_result.intent_data.get("trends", {})
        insights = analysis_result.intent_data.get("insights", [])
        contributors = analysis_result.intent_data.get("contributors", {})

        # 4. Apply appropriate template based on data_type
        if data_type == "repository_metrics":
            content = self._apply_repository_metrics_template(title, repository, days, metrics)
        elif data_type == "activity_trends":
            content = self._apply_activity_trends_template(
                title, repository, days, metrics, trends, insights
            )
        elif data_type == "contributor_stats":
            content = self._apply_contributor_stats_template(
                title, repository, days, metrics, contributors, insights
            )

        # 5. Validate content quality
        if not content or len(content) < 100:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "status_report",
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result with generated content
        return IntentProcessingResult(
            success=True,
            message=f"Generated {data_type} status report for {repository}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "status_report",
                "repository": repository,
                "days": days,
                "data_type": data_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "title": title,
                    "generated_at": datetime.now().isoformat(),
                    "total_activity": metrics.get("total_activity_count", 0),
                    "data_source": data_type,
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _get_default_repository(self) -> str:
        """Get default repository from user config or return None."""
        # This could be enhanced to read from user config
        # For now, return None to require explicit repository
        return None

    def _apply_repository_metrics_template(
        self, title: str, repository: str, days: int, metrics: dict
    ) -> str:
        """Apply repository metrics template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total = metrics.get("total_activity_count", 0)
        commits = metrics.get("commits_count", 0)
        prs = metrics.get("prs_count", 0)
        issues_created = metrics.get("issues_created_count", 0)
        issues_closed = metrics.get("issues_closed_count", 0)

        distribution = metrics.get("activity_distribution", {})
        commits_pct = distribution.get("commits", 0)
        prs_pct = distribution.get("prs", 0)
        issues_created_pct = distribution.get("issues_created", 0)
        issues_closed_pct = distribution.get("issues_closed", 0)

        # Generate ASCII bar chart
        bar_chart = self._generate_ascii_bar_chart(distribution)

        # Determine activity level
        if total > 50:
            activity_level = "high"
        elif total > 20:
            activity_level = "moderate"
        else:
            activity_level = "low"

        # Generate issue activity summary
        if issues_closed > 0:
            issue_summary = f"{issues_created} issues created and {issues_closed} closed"
        elif issues_created > 0:
            issue_summary = f"{issues_created} issues created"
        else:
            issue_summary = "no issue activity"

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Activity Overview

- **Total Activity**: {total} events
- **Commits**: {commits} ({commits_pct:.1f}%)
- **Pull Requests**: {prs} ({prs_pct:.1f}%)
- **Issues Created**: {issues_created} ({issues_created_pct:.1f}%)
- **Issues Closed**: {issues_closed} ({issues_closed_pct:.1f}%)

---

## Activity Distribution

{bar_chart}

---

## Summary

Repository shows {activity_level} activity with {commits} commits, {prs} pull requests, and {issue_summary}.

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _apply_activity_trends_template(
        self, title: str, repository: str, days: int, metrics: dict, trends: dict, insights: list
    ) -> str:
        """Apply activity trends template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total = metrics.get("total_activity_count", 0)
        commits = metrics.get("commits_count", 0)
        prs = metrics.get("prs_count", 0)
        issues_created = metrics.get("issues_created_count", 0)
        issues_closed = metrics.get("issues_closed_count", 0)

        # Extract trends
        most_active_type = trends.get("most_active_type", "N/A")
        issue_closure_rate = trends.get("issue_closure_rate", 0)
        commit_velocity = trends.get("commit_velocity", "N/A")
        pr_activity = trends.get("pr_activity", "N/A")

        # Format insights list
        insights_text = (
            "\n".join(f"- {insight}" for insight in insights)
            if insights
            else "- No insights available"
        )

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Activity Metrics

- **Total Activity**: {total} events
- **Commits**: {commits}
- **Pull Requests**: {prs}
- **Issues Created**: {issues_created}
- **Issues Closed**: {issues_closed}

---

## Trends

- **Most Active Type**: {most_active_type}
- **Issue Closure Rate**: {issue_closure_rate}%
- **Commit Velocity**: {commit_velocity}
- **PR Activity**: {pr_activity}

---

## Insights

{insights_text}

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _apply_contributor_stats_template(
        self,
        title: str,
        repository: str,
        days: int,
        metrics: dict,
        contributors: dict,
        insights: list,
    ) -> str:
        """Apply contributor stats template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total_contributors = metrics.get("total_contributors", 0)
        commit_authors = metrics.get("commit_authors", 0)
        pr_authors = metrics.get("pr_authors", 0)
        issue_authors = metrics.get("issue_authors", 0)

        # Generate leaderboards
        commits_leaderboard = self._generate_leaderboard(contributors.get("commits", {}))
        prs_leaderboard = self._generate_leaderboard(contributors.get("prs", {}))
        issues_leaderboard = self._generate_leaderboard(contributors.get("issues", {}))

        # Format insights list
        insights_text = (
            "\n".join(f"- {insight}" for insight in insights)
            if insights
            else "- No insights available"
        )

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Contributor Overview

- **Total Contributors**: {total_contributors}
- **Commit Authors**: {commit_authors}
- **PR Authors**: {pr_authors}
- **Issue Authors**: {issue_authors}

---

## Top Contributors

### Commits
{commits_leaderboard}

### Pull Requests
{prs_leaderboard}

### Issues
{issues_leaderboard}

---

## Insights

{insights_text}

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _generate_ascii_bar_chart(self, distribution: dict) -> str:
        """Generate simple ASCII bar chart from distribution data."""
        if not distribution:
            return "No distribution data available"

        lines = []
        max_bar_width = 40

        for label, percent in distribution.items():
            bar_width = int((percent / 100) * max_bar_width)
            bar = "█" * bar_width
            lines.append(f"{label:20s} │{bar} {percent:.1f}%")

        return "\n".join(lines)

    def _generate_leaderboard(self, contributor_dict: dict) -> str:
        """Generate leaderboard text from contributor dictionary."""
        if not contributor_dict:
            return "- No data available"

        # Sort by count (descending)
        sorted_contributors = sorted(contributor_dict.items(), key=lambda x: x[1], reverse=True)

        lines = []
        for i, (name, count) in enumerate(sorted_contributors[:10], 1):  # Top 10
            lines.append(f"{i}. **{name}**: {count}")

        return "\n".join(lines)

    async def _generate_readme_section(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate README.md section.

        Creates standard README sections with language-specific templates.

        Parameters:
        - section_type (required): Type of section to generate
          - "installation": Installation instructions
          - "usage": Usage examples
          - "contributing": Contributing guidelines
          - "testing": Testing instructions
        - language (optional): Primary language (default: "python")
        - repository (optional): Repository name for examples
        - title (optional): Custom section title
        """
        from datetime import datetime

        # 1. Validate section_type (required)
        section_type = intent.context.get("section_type")
        if not section_type:
            return IntentProcessingResult(
                success=False,
                message="Section type is required for README generation.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="section_type_required",
            )

        # 2. Validate section_type is supported
        valid_sections = ["installation", "usage", "contributing", "testing"]
        if section_type not in valid_sections:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported section type: {section_type}. Valid types: {', '.join(valid_sections)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                    "section_type": section_type,
                    "valid_types": valid_sections,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="unsupported_section_type",
            )

        # 3. Extract optional parameters
        repository = intent.context.get("repository")
        language = intent.context.get("language", "python")
        title = intent.context.get("title", section_type.capitalize())

        # Parse repository into org/repo if provided
        org, repo = None, None
        if repository:
            parts = repository.split("/")
            if len(parts) == 2:
                org, repo = parts

        # 4. Generate content based on section_type
        if section_type == "installation":
            content = self._generate_installation_section(title, language, org, repo)
        elif section_type == "usage":
            content = self._generate_usage_section(title, language, repo)
        elif section_type == "contributing":
            content = self._generate_contributing_section(title, repo)
        elif section_type == "testing":
            content = self._generate_testing_section(title, language, repo)

        # 5. Validate content quality
        if not content or len(content) < 50:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                    "section_type": section_type,
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result
        return IntentProcessingResult(
            success=True,
            message=f"Generated {section_type} section for README",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "readme_section",
                "section_type": section_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "title": title,
                    "language": language,
                    "repository": repository,
                    "generated_at": datetime.now().isoformat(),
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _generate_installation_section(
        self, title: str, language: str, org: str = None, repo: str = None
    ) -> str:
        """Generate installation section based on language."""

        if language.lower() in ["javascript", "typescript", "js", "ts"]:
            return self._generate_installation_javascript(title, org, repo)
        else:  # Default to Python
            return self._generate_installation_python(title, org, repo)

    def _generate_installation_python(self, title: str, org: str = None, repo: str = None) -> str:
        """Generate Python installation section."""
        repo_url = (
            f"https://github.com/{org}/{repo}.git"
            if org and repo
            else "https://github.com/ORG/REPO.git"
        )
        repo_name = repo if repo else "repo"
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Prerequisites

- Python 3.9 or higher
- pip or poetry
- Git

### Quick Start

```bash
# Clone the repository
git clone {repo_url}
cd {repo_name}

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Verification

```bash
# Run tests
python -m pytest tests/

# Check installation
python -c "import {package_name}; print({package_name}.__version__)"
```

### Troubleshooting

If you encounter issues:

- Ensure Python 3.9+ is installed: `python --version`
- Update pip: `pip install --upgrade pip`
- Check dependencies: `pip check`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

*For detailed installation instructions, see [INSTALL.md](INSTALL.md)*
"""

    def _generate_installation_javascript(
        self, title: str, org: str = None, repo: str = None
    ) -> str:
        """Generate JavaScript/TypeScript installation section."""
        repo_url = (
            f"https://github.com/{org}/{repo}.git"
            if org and repo
            else "https://github.com/ORG/REPO.git"
        )
        repo_name = repo if repo else "repo"

        return f"""## {title}

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn or pnpm
- Git

### Quick Start

```bash
# Clone the repository
git clone {repo_url}
cd {repo_name}

# Install dependencies
npm install
# or: yarn install
# or: pnpm install
```

### Verification

```bash
# Run tests
npm test

# Build the project
npm run build

# Check installation
npm list
```

### Troubleshooting

If you encounter issues:

- Ensure Node.js 18+ is installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

*For detailed installation instructions, see [INSTALL.md](INSTALL.md)*
"""

    def _generate_usage_section(self, title: str, language: str, repo: str = None) -> str:
        """Generate usage section based on language."""

        if language.lower() in ["javascript", "typescript", "js", "ts"]:
            return self._generate_usage_javascript(title, repo)
        else:  # Default to Python
            return self._generate_usage_python(title, repo)

    def _generate_usage_python(self, title: str, repo: str = None) -> str:
        """Generate Python usage section."""
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Basic Usage

```python
from {package_name} import Client

# Initialize
client = Client()

# Basic operation
result = client.process("input data")
print(result)
```

### Common Use Cases

#### Use Case 1: Simple Processing

```python
# Process a single item
result = client.process_item(item)
```

#### Use Case 2: Batch Processing

```python
# Process multiple items
results = client.process_batch(items)
for result in results:
    print(result)
```

#### Use Case 3: Async Processing

```python
import asyncio

async def main():
    async with Client() as client:
        result = await client.process_async("data")
        print(result)

asyncio.run(main())
```

### Configuration

Create a configuration file:

```python
# config.py
config = {{
    "option1": "value1",
    "option2": "value2"
}}
```

Use configuration:

```python
from config import config

client = Client(config=config)
```

### Examples

See [examples/](examples/) directory for complete examples:

- [examples/basic.py](examples/basic.py) - Basic usage
- [examples/advanced.py](examples/advanced.py) - Advanced features
- [examples/async.py](examples/async.py) - Async operations

---

*For more examples, see [examples/](examples/)*
"""

    def _generate_usage_javascript(self, title: str, repo: str = None) -> str:
        """Generate JavaScript usage section."""
        package_name = repo if repo else "package-name"

        return f"""## {title}

### Basic Usage

```javascript
const {{ Client }} = require('{package_name}');

// Initialize
const client = new Client();

// Basic operation
const result = client.process('input data');
console.log(result);
```

### Common Use Cases

#### Use Case 1: Simple Processing

```javascript
// Process a single item
const result = client.processItem(item);
```

#### Use Case 2: Batch Processing

```javascript
// Process multiple items
const results = client.processBatch(items);
results.forEach(result => console.log(result));
```

#### Use Case 3: Async/Await

```javascript
async function main() {{
    const result = await client.processAsync('data');
    console.log(result);
}}

main();
```

### Configuration

Create a configuration file:

```javascript
// config.js
module.exports = {{
    option1: 'value1',
    option2: 'value2'
}};
```

Use configuration:

```javascript
const config = require('./config');
const client = new Client(config);
```

### Examples

See [examples/](examples/) directory for complete examples:

- [examples/basic.js](examples/basic.js) - Basic usage
- [examples/advanced.js](examples/advanced.js) - Advanced features
- [examples/async.js](examples/async.js) - Async operations

---

*For more examples, see [examples/](examples/)*
"""

    def _generate_contributing_section(self, title: str, repo: str = None) -> str:
        """Generate contributing section."""
        repo_name = repo if repo else "repo"
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

We welcome contributions! Here's how to get started.

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/{repo_name}.git
   cd {repo_name}
   ```
3. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```
4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes in the feature branch
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass: `pytest`
5. Run linting: `flake8 .` and `black .`

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Keep functions focused and under 50 lines
- Maximum line length: 100 characters

### Testing

- Write unit tests for all new code
- Maintain or improve code coverage (target: 80%+)
- Run full test suite before submitting: `pytest tests/`
- Run coverage check: `pytest --cov={package_name} tests/`

### Submitting Changes

1. Commit your changes:
   ```bash
   git commit -m "feat: add new feature"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/)

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request:
   - Describe your changes
   - Link any related issues
   - Add screenshots if UI changes
   - Wait for review and address feedback

---

*See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines*
"""

    def _generate_testing_section(self, title: str, language: str, repo: str = None) -> str:
        """Generate testing section based on language."""
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_module.py
```

Run specific test:
```bash
pytest tests/test_module.py::test_function
```

Run with coverage:
```bash
pytest --cov={package_name} --cov-report=html tests/
```

Run with verbose output:
```bash
pytest -v
```

### Test Structure

```
tests/
├── unit/               # Unit tests
│   ├── test_core.py
│   └── test_utils.py
├── integration/        # Integration tests
│   └── test_workflow.py
├── fixtures/           # Test fixtures and data
│   └── sample_data.json
└── conftest.py        # Shared fixtures
```

### Writing Tests

Use pytest fixtures for setup:

```python
import pytest
from {package_name} import Client

@pytest.fixture
def client():
    return Client()

def test_basic_functionality(client):
    result = client.process("test input")
    assert result is not None
    assert "expected" in result
```

### Coverage

Current coverage: **85%** (target: 80%+)

View coverage report:
```bash
pytest --cov={package_name} --cov-report=html tests/
open htmlcov/index.html
```

---

*See [tests/README.md](tests/README.md) for detailed testing guide*
"""

    async def _generate_issue_template(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate GitHub issue template.

        Creates YAML-formatted issue templates for .github/ISSUE_TEMPLATE/ directory.

        Parameters:
        - template_type (required): Type of template to generate
          - "bug_report": Bug report template
          - "feature_request": Feature request template
          - "custom": Custom template (requires additional context)
        - labels (optional): Default labels to apply
        - repository (optional): Repository name for context
        """
        from datetime import datetime

        # 1. Validate template_type (required)
        template_type = intent.context.get("template_type")
        if not template_type:
            return IntentProcessingResult(
                success=False,
                message="Template type is required for issue template generation.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="template_type_required",
            )

        # 2. Validate template_type is supported
        valid_types = ["bug_report", "feature_request", "custom"]
        if template_type not in valid_types:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported template type: {template_type}. Valid types: {', '.join(valid_types)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                    "template_type": template_type,
                    "valid_types": valid_types,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="unsupported_template_type",
            )

        # 3. Extract optional parameters
        repository = intent.context.get("repository")
        labels = intent.context.get("labels")

        # Set default labels based on template type
        if not labels:
            if template_type == "bug_report":
                labels = ["bug", "needs-triage"]
            elif template_type == "feature_request":
                labels = ["enhancement", "needs-triage"]
            else:
                labels = ["needs-triage"]

        # 4. Generate content based on template_type
        if template_type == "bug_report":
            content = self._generate_bug_report_template(labels)
            filename = "bug_report.yml"
        elif template_type == "feature_request":
            content = self._generate_feature_request_template(labels)
            filename = "feature_request.yml"
        elif template_type == "custom":
            content = self._generate_custom_template(intent.context, labels)
            filename = "custom_template.yml"

        # 5. Validate content quality
        if not content or len(content) < 50:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                    "template_type": template_type,
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result
        return IntentProcessingResult(
            success=True,
            message=f"Generated {template_type} issue template",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "issue_template",
                "template_type": template_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "filename": filename,
                    "labels": labels,
                    "repository": repository,
                    "generated_at": datetime.now().isoformat(),
                    "installation_path": f".github/ISSUE_TEMPLATE/{filename}",
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _generate_bug_report_template(self, labels: list) -> str:
        """Generate bug report issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        return f"""---
name: Bug Report
about: Report a bug to help us improve
title: "[BUG] "
labels: [{labels_yaml}]
assignees: []
---

## Description

A clear and concise description of the bug.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior

A clear description of what you expected to happen.

## Actual Behavior

A clear description of what actually happened.

## Screenshots

If applicable, add screenshots to help explain the problem.

## Environment

- **OS**: [e.g., macOS 14.0, Windows 11, Ubuntu 22.04]
- **Browser** (if applicable): [e.g., Chrome 120, Safari 17]
- **Version**: [e.g., 1.0.0]
- **Python Version** (if applicable): [e.g., 3.9.6]

## Additional Context

Add any other context about the problem here.

## Possible Solution

If you have suggestions on how to fix the bug, please describe them here.
"""

    def _generate_feature_request_template(self, labels: list) -> str:
        """Generate feature request issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        return f"""---
name: Feature Request
about: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: [{labels_yaml}]
assignees: []
---

## Feature Description

A clear and concise description of the feature you'd like to see.

## Problem Statement

Describe the problem this feature would solve. Why is this feature needed?

## Proposed Solution

Describe your proposed solution. How would you like this feature to work?

## Alternatives Considered

Have you considered any alternative solutions? If so, describe them here.

## Use Cases

Describe specific use cases where this feature would be valuable:

1. Use case 1...
2. Use case 2...
3. Use case 3...

## Additional Context

Add any other context, mockups, or examples about the feature request here.

## Acceptance Criteria

What would need to be true for this feature to be considered complete?

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Priority

How important is this feature to you?

- [ ] Critical - Blocking my work
- [ ] High - Significantly improves my workflow
- [ ] Medium - Nice to have
- [ ] Low - Minor improvement
"""

    def _generate_custom_template(self, context: dict, labels: list) -> str:
        """Generate custom issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        # Extract custom parameters or use defaults
        custom_name = context.get("custom_name", "Custom Issue")
        custom_description = context.get("custom_description", "Custom issue template")
        custom_title_prefix = context.get("custom_title_prefix", "")

        return f"""---
name: {custom_name}
about: {custom_description}
title: "{custom_title_prefix}"
labels: [{labels_yaml}]
assignees: []
---

## Description

Please provide a detailed description.

## Context

Add any relevant context or background information.

## Checklist

- [ ] I have read the contributing guidelines
- [ ] I have searched existing issues
- [ ] I have provided all requested information

## Additional Information

Add any additional information here.
"""

    async def _handle_summarize(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
        """
        Handle summarization requests — DORMANT (off the dispatch path post-#1158).

        SUMMARIZE-TAXONOMY (#1158, resolved 2026-06-09): per PPM's product ruling, a
        summary's output is ALWAYS conversational (floor-rendered). The canonical
        `summarize` verb is therefore deliberately NOT shimmed to the `summarize`
        action (see `_VERB_SOURCE_TO_ACTION` in action_registry.py), so this handler
        is no longer reached — summary requests fall through the SYNTHESIS elif to the
        conversational floor. This method is retained (not deleted) because its
        fetch helpers (`_fetch_issue_content` / `_fetch_commit_content`) are the
        seed for the deferred fetch-augmentation pipeline (SUMMARIZE-FETCH-AUGMENTATION
        follow-on): fetch source content the floor can't reach, then hand to the floor
        to render. There is no second (structured) output renderer to build.

        Fetch capability of THIS handler (narrower than the classifier's source_type
        vocabulary, which is {text, conversation, github_issue, commit_range, document}):
            - 'github_issue': Summarize GitHub issue and comments
            - 'commit_range': Summarize commits from a time period
            - 'text': Summarize provided text content
        ('conversation' is floor-direct; 'document' retrieval is part of the deferred
        fetch-augmentation work.)
        """
        try:
            # 1. VALIDATION
            source_type = intent.context.get("source_type")

            if not source_type:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot summarize: source type not specified. Please specify 'github_issue', 'commit_range', or 'text'.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="source_type_required",
                )

            # Validate source_type
            valid_sources = ["github_issue", "commit_range", "text"]
            if source_type not in valid_sources:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unknown source type '{source_type}'. Supported types: {', '.join(valid_sources)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "requested_source_type": source_type,
                    },
                    workflow_id=workflow_id,
                    error=f"Unknown source type: {source_type}",
                    error_type="ValidationError",
                )

            # 2. FETCH CONTENT based on source_type
            try:
                if source_type == "github_issue":
                    content, source_metadata = await self._fetch_issue_content(intent.context)
                elif source_type == "commit_range":
                    content, source_metadata = await self._fetch_commit_content(
                        intent.context, workflow_id
                    )
                elif source_type == "text":
                    content, source_metadata = self._extract_text_content(intent.context)

                # Check for empty content
                if not content or len(content.strip()) < 50:
                    return IntentProcessingResult(
                        success=False,
                        message=f"Content too short to summarize (< 50 characters). Please provide more content.",
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "source_type": source_type,
                        },
                        workflow_id=workflow_id,
                        error="Content too short",
                        error_type="ValidationError",
                    )

            except ValueError as e:
                # Parameter validation errors
                return self._make_error_result(
                    intent=intent,
                    workflow_id=workflow_id,
                    error=e,
                    context="creating that summary",
                    error_type="ValidationError",
                )

            # 3. SUMMARIZE with LLM
            length = intent.context.get("length", "moderate")

            doc_summary = await self._summarize_with_llm(
                content=content, source_type=source_type, length=length, **source_metadata
            )

            # 4. FORMAT summary
            format_type = intent.context.get("format", "bullet_points")
            formatted_summary = self._format_summary(doc_summary, format_type)

            # 5. CALCULATE metrics
            original_length = len(content)
            summary_length = len(formatted_summary)
            compression_ratio = summary_length / original_length if original_length > 0 else 0.0

            # 6. BUILD response
            return IntentProcessingResult(
                success=True,
                message=f"Summarized {source_type} successfully ({original_length} → {summary_length} chars, {compression_ratio:.1%} compression)",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    # Summary content
                    "summary": formatted_summary,
                    "summary_format": format_type,
                    "summary_length": summary_length,
                    # Metrics
                    "original_length": original_length,
                    "compression_ratio": compression_ratio,
                    # Structured data
                    "title": doc_summary.title,
                    "document_type": doc_summary.document_type,
                    "key_findings": doc_summary.key_findings,
                    # Source info
                    "source_type": source_type,
                    "source_metadata": source_metadata,
                    # Timing
                    "summarized_at": datetime.now().isoformat(),
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to summarize: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="creating that summary",
                error_type="SynthesisError",
            )

    async def _fetch_summary_source_content(
        self, intent: Intent, workflow_id: Optional[str] = None
    ) -> Optional[Tuple[str, Dict[str, Any]]]:
        """#1187 fetch-augmentation core: for a `summarize` request whose source the
        floor can't reach (github_issue / commit_range), fetch the source content so
        the floor can render the summary from it. Returns `(content, metadata)` or
        `None` when there is nothing to fetch (text / conversation are floor-direct;
        document retrieval is a deferred path).

        Reuses the `_handle_summarize` fetch helpers (`_fetch_issue_content` does its
        own #1187 Gap-1 issue-number extraction from the raw message, since the
        classifier tags source_type but does not slot the number). This is the
        *fetch* half of #1158's "output always floor, source branches" ruling; the
        floor-injection + rendering is wired separately (see the #1187 wiring
        design). Pure dispatcher: no LLM, no formatting, no side effects.
        """
        # Enrich a COPY of the context: the classifier puts the raw message on
        # `intent.original_message` (the model field), but the fetch helpers read
        # `context["original_message"]` to parse the `#N`. Never mutate intent.context.
        context = dict(intent.context or {})
        context.setdefault("original_message", getattr(intent, "original_message", "") or "")
        source_type = context.get("source_type")

        # #1187 robustness: the full classification pipeline (learned-pattern / KG
        # enrichment for a known user) can emit a COLLAPSED action
        # ("summarize_github_issue") and omit the source_type slot — even though the
        # #1158 prompt asks for verb + source_type. Infer the source from the
        # action / message so the fetch still fires. (Fresh/standalone
        # classification sets source_type cleanly; this covers the enriched path.)
        if not source_type:
            import re as _re

            action = (getattr(intent, "action", "") or "").lower()
            msg = (context.get("original_message", "") or "").lower()
            summarize_ish = any(v in msg for v in ("summarize", "summary", "tl;dr", "recap"))
            if "github_issue" in action or "summarize_github_issue" in action:
                source_type = "github_issue"
            elif "github" in msg and "issue" in msg and _re.search(r"#?\d+", msg) and summarize_ish:
                source_type = "github_issue"
            if source_type:
                context["source_type"] = source_type

        try:
            if source_type == "github_issue":
                return await self._fetch_issue_content(context)
            if source_type == "commit_range":
                return await self._fetch_commit_content(context, workflow_id)
            # text / conversation → the floor already has it (floor-direct).
            # document → deferred (Notion/uploaded-file retrieval); not yet wired.
            return None
        except Exception as e:
            # Fetch failure is graceful: return None → the floor degrades to the
            # honest "I couldn't pull that — want me to try again?" rather than crashing.
            self.logger.warning(
                "summary_source_fetch_failed",
                source_type=source_type,
                error=str(e),
            )
            return None

    async def _fetch_issue_content(self, context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Fetch and format GitHub issue content for summarization.

        #1187 Gap 1: the classifier tags ``source_type=github_issue`` but does NOT
        slot the issue number, so the number is parsed here from the raw message
        (``#1124`` / ``issue 1124``). Repository resolution follows the live
        ``github_router`` path (Issue #1042): the router resolves owner/repo from
        its default-repo config when not given explicitly, so a bare
        "summarize github issue #1124" works without the user naming the repo.

        Args:
            context: Intent context. Accepts ``issue_url`` OR ``issue_number`` OR a
                raw ``original_message`` to parse a ``#N`` from. ``repository``
                ("owner/repo") is optional — the router default-repo fills it in.

        Returns:
            Tuple of (content_string, metadata_dict)

        Raises:
            ValueError: no issue number found, GitHub not configured, or the issue
                couldn't be fetched. Callers (``_fetch_summary_source_content``)
                degrade these to None so the floor responds gracefully.
        """
        import re
        from uuid import UUID

        from services.integrations.github.config_service import GitHubConfigService
        from services.integrations.github.issue_fetch import fetch_issue_with_comments
        from services.integrations.github.repo_resolver import (
            UnresolvedRepoError,
            resolve_repo,
        )

        # Extract parameters
        issue_url = context.get("issue_url")
        repository = context.get("repository")
        issue_number = context.get("issue_number")
        include_comments = context.get("include_comments", True)
        max_comments = context.get("max_comments", 10)
        user_id = context.get("user_id")

        # Resolve the issue number: explicit slot > issue_url > parse from message.
        if issue_url:
            match = re.match(r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)", issue_url)
            if not match:
                raise ValueError(f"Invalid issue URL format: {issue_url}")
            _o, _r, num = match.groups()
            repository = f"{_o}/{_r}"
            issue_number = int(num)
        elif not issue_number:
            # #1187 Gap 1: the classifier tags source_type=github_issue but does
            # not slot the number — parse it from the raw message.
            match = re.search(r"#?(\d+)", context.get("original_message", ""))
            if not match:
                raise ValueError("No issue number found in summarize request")
            issue_number = int(match.group(1))

        # Resolve the repository: explicit ("owner/repo") > user/project default.
        # #1192 slice (a): resolve_repo reads the persistent UI default-repo store,
        # so designating a default repo in the settings page reaches this path.
        if not (repository and "/" in repository):
            try:
                _uid = UUID(user_id) if user_id and user_id != "system" else None
            except (ValueError, TypeError):
                _uid = None
            try:
                repository = (await resolve_repo(user_id=_uid)).full_name
            except UnresolvedRepoError:
                raise ValueError(
                    "No repository resolved — connect GitHub and set a default "
                    "repository, or name the repo in your request"
                )

        # Resolve the token (keychain-first for a connected user; #1192 Blocker 1 —
        # a connected PAT wins over a stale global env token).
        token = GitHubConfigService().get_authentication_token(user_id or "system")
        if not token:
            raise ValueError("GitHub is not configured")

        owner, repo = repository.split("/", 1)

        # #1187 Option C: fetch the raw issue + comment thread directly via the
        # GitHub REST API. The MCP adapter returns a lossy transformed dict (no
        # comments, description-not-body) — a faithful summary needs the full body
        # AND the discussion, so we fetch the raw shape the formatter expects.
        try:
            issue = await fetch_issue_with_comments(
                owner,
                repo,
                issue_number,
                token,
                max_comments=(max_comments if include_comments else 0),
            )
            if not issue:
                raise ValueError(
                    f"Issue #{issue_number} in {repository} could not be fetched "
                    "(not found, no access, or token invalid)"
                )

            # Extract fields
            title = issue.get("title", "Untitled")
            body = issue.get("body", "")
            state = issue.get("state", "unknown")
            created_at = issue.get("created_at", "")

            # Handle author - could be nested dict
            author_data = issue.get("user") or issue.get("author", {})
            if isinstance(author_data, dict):
                author = author_data.get("login", "unknown")
            else:
                author = str(author_data)

            # Build content markdown
            content_parts = [
                f"# GitHub Issue Summary Request\n",
                f"**Issue**: #{issue_number} - {title}",
                f"**Repository**: {repository}",
                f"**Status**: {state}",
                f"**Created**: {created_at}",
                f"**Author**: {author}\n",
                f"## Issue Body\n",
                body or "(No description provided)",
            ]

            # Add comments if requested
            comment_count = 0
            if include_comments:
                comments = issue.get("comments", [])
                if isinstance(comments, list):
                    comment_count = len(comments)
                    if comment_count > 0:
                        content_parts.append(
                            f"\n## Comments ({comment_count} total, showing {min(comment_count, max_comments)})\n"
                        )
                        for i, comment in enumerate(comments[:max_comments], 1):
                            comment_author_data = comment.get("user") or comment.get("author", {})
                            if isinstance(comment_author_data, dict):
                                comment_author = comment_author_data.get("login", "unknown")
                            else:
                                comment_author = str(comment_author_data)
                            comment_body = comment.get("body", "")
                            comment_date = comment.get("created_at", "")
                            content_parts.append(
                                f"### Comment {i} by {comment_author} ({comment_date})\n"
                            )
                            content_parts.append(comment_body)
                            content_parts.append("")  # Blank line

            content = "\n".join(content_parts)

            # Build metadata
            metadata = {
                "issue_url": f"https://github.com/{repository}/issues/{issue_number}",
                "issue_number": issue_number,
                "repository": repository,
                "issue_state": state,
                "comment_count": comment_count,
                "comments_included": min(comment_count, max_comments) if include_comments else 0,
                "author": author,
                "created_at": created_at,
            }

            return content, metadata

        except Exception as e:
            self.logger.error(f"Failed to fetch issue content: {e}", exc_info=True)
            raise Exception(f"Failed to fetch GitHub issue: {str(e)}")

    async def _fetch_commit_content(
        self, context: Dict[str, Any], workflow_id: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Fetch and format commit data for summarization.

        Integrates with Phase 2C _handle_analyze_commits.

        Args:
            context: Intent context containing repository and timeframe params
            workflow_id: Current workflow ID

        Returns:
            Tuple of (content_string, metadata_dict)
        """
        # Extract parameters
        repository = context.get("repository")
        if not repository:
            raise ValueError("repository is required for commit_range summarization")

        days = context.get("days", 7)
        timeframe = context.get("timeframe", f"last {days} days")
        categorize = context.get("categorize", True)

        # Build intent for Phase 2C
        from services.domain.models import Intent as DomainIntent

        commit_intent = DomainIntent(
            original_message=f"analyze commits for {repository}",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=1.0,
            context={
                "repository": repository,
                "days": days,
            },
        )

        # Call Phase 2C handler
        commit_result = await self._handle_analyze_commits(commit_intent, workflow_id)

        if not commit_result.success:
            raise Exception(f"Failed to fetch commits: {commit_result.message}")

        # Extract commit data
        commit_count = commit_result.intent_data.get("commit_count", 0)
        commits = commit_result.intent_data.get("recent_messages", [])
        authors = commit_result.intent_data.get("authors", {})

        # Build content
        content_parts = [
            f"# Commit Summary Request\n",
            f"**Repository**: {repository}",
            f"**Timeframe**: {timeframe}",
            f"**Total Commits**: {commit_count}",
            f"**Authors**: {', '.join([f'{name} ({count})' for name, count in authors.items()])}\n",
        ]

        # Categorize commits if requested
        if categorize and commits:
            categories = self._categorize_commits(commits)

            # Add categorized commits
            for category, cat_commits in categories.items():
                if cat_commits:
                    category_title = category.capitalize() if category != "other" else "Other"
                    content_parts.append(f"## {category_title} ({len(cat_commits)} commits)\n")
                    for commit in cat_commits:
                        content_parts.append(f"- {commit}")
                    content_parts.append("")  # Blank line
        else:
            # Non-categorized list
            content_parts.append(f"## Commits (chronological)\n")
            for i, commit in enumerate(commits, 1):
                content_parts.append(f"{i}. {commit}")

        content = "\n".join(content_parts)

        # Build metadata
        metadata = {
            "repository": repository,
            "commit_count": commit_count,
            "timeframe": timeframe,
            "days": days,
            "authors": authors,
        }

        if categorize:
            categories = self._categorize_commits(commits)
            category_counts = {cat: len(msgs) for cat, msgs in categories.items()}
            metadata["categories"] = category_counts

        return content, metadata

    def _extract_text_content(self, context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Extract and validate text content for summarization.

        Args:
            context: Intent context containing content text

        Returns:
            Tuple of (content_string, metadata_dict)
        """
        # Extract content
        content = context.get("content")
        if not content:
            raise ValueError("content is required for text summarization")

        if not isinstance(content, str):
            raise ValueError("content must be a string")

        # Validate minimum length
        if len(content.strip()) < 50:
            raise ValueError("content is too short to summarize (minimum 50 characters)")

        # Truncate if too long (with warning)
        MAX_LENGTH = 10000
        if len(content) > MAX_LENGTH:
            self.logger.warning(
                f"Content exceeds maximum length ({len(content)} > {MAX_LENGTH}), truncating"
            )
            content = content[:MAX_LENGTH]

        # Extract optional params
        title = context.get("title", "Document")
        document_type = context.get("document_type", "Text")

        # Build formatted content
        formatted_content = f"""# Text Summary Request

**Title**: {title}
**Document Type**: {document_type}
**Length**: {len(content)} characters

## Content

{content}"""

        # Build metadata
        metadata = {
            "title": title,
            "document_type": document_type,
            "original_length": len(content),
            "provided_by": "user",
        }

        return formatted_content, metadata

    async def _summarize_with_llm(
        self, content: str, source_type: str, length: str = "moderate", **kwargs
    ):
        """
        Summarize content using LLM with structured JSON output.

        Args:
            content: Formatted content to summarize
            source_type: Type of source
            length: Desired summary length
            **kwargs: Additional metadata

        Returns:
            DocumentSummary object with structured summary
        """
        # Initialize LLM client if needed (for test mocking)
        if not hasattr(self, "llm_client") or self.llm_client is None:
            from services.llm.clients import LLMClient

            self.llm_client = LLMClient()

        # Build length guidance
        length_guidance = {
            "brief": "Provide 2-3 key points only.",
            "moderate": "Provide 5-7 key points covering main topics.",
            "detailed": "Provide 10+ key points with comprehensive coverage.",
        }.get(length, "Provide 5-7 key points covering main topics.")

        # Build source-specific guidance
        source_guidance = {
            "github_issue": "Focus on the issue description, key discussion points, and proposed solutions.",
            "commit_range": "Focus on categorizing changes by type (features, fixes, chores) and identifying key contributors.",
            "text": "Focus on extracting the main themes and important details.",
        }.get(source_type, "Focus on the key themes and important details.")

        # Truncate content to avoid token limits (like TextAnalyzer does)
        truncated_content = content[:3000]

        # Build prompt
        prompt = f"""Please summarize the following content.

{source_guidance}
{length_guidance}

Return a JSON object with this exact structure:
{{
    "title": "Brief title for the summary",
    "document_type": "{source_type}",
    "key_findings": ["Finding 1", "Finding 2", "Finding 3", ...],
    "sections": []
}}

Content to summarize:

{truncated_content}"""

        # Call LLM with JSON mode
        try:
            json_response = await self.llm_client.complete(
                task_type="summarize", prompt=prompt, response_format={"type": "json_object"}
            )

            # Parse JSON response
            summary_data = json.loads(json_response)

            # Create DocumentSummary-like object
            from services.analysis.summary_parser import DocumentSummary

            doc_summary = DocumentSummary(
                title=summary_data.get("title", "Summary"),
                document_type=summary_data.get("document_type", source_type),
                key_findings=summary_data.get("key_findings", []),
                sections=summary_data.get("sections", []),
            )

            return doc_summary

        except Exception as e:
            self.logger.error(f"LLM summarization failed: {e}", exc_info=True)
            raise Exception(f"Failed to generate summary: {str(e)}")

    def _format_summary(self, doc_summary, format_type: str = "bullet_points") -> str:
        """
        Format DocumentSummary into requested output format.

        Args:
            doc_summary: Structured summary from LLM
            format_type: Output format (bullet_points, paragraph, executive_summary)

        Returns:
            Formatted summary string
        """
        if format_type == "paragraph":
            # Convert to narrative paragraph
            sentences = []
            sentences.append(f"This document discusses {doc_summary.title}.")
            sentences.extend(doc_summary.key_findings)
            return " ".join(sentences)

        elif format_type == "executive_summary":
            # Build executive summary structure
            parts = [
                f"# Executive Summary: {doc_summary.title}\n",
                f"## Overview\n",
            ]

            if doc_summary.key_findings:
                parts.append(doc_summary.key_findings[0])
                parts.append("\n## Key Points\n")
                for finding in doc_summary.key_findings[1:]:
                    parts.append(f"- {finding}")

            if doc_summary.sections:
                parts.append("\n## Details\n")
                for section in doc_summary.sections:
                    if isinstance(section, dict):
                        title = section.get("title", "")
                        points = section.get("points", [])
                        parts.append(f"### {title}\n")
                        for point in points:
                            parts.append(f"- {point}")

            return "\n".join(parts)

        else:
            # Default to bullet_points - use to_markdown if available
            if hasattr(doc_summary, "to_markdown"):
                return doc_summary.to_markdown()
            else:
                # Fallback: build markdown manually
                parts = [f"## Summary: {doc_summary.title}\n"]
                if doc_summary.key_findings:
                    parts.append("### Key Findings\n")
                    for finding in doc_summary.key_findings:
                        parts.append(f"- {finding}")
                return "\n".join(parts)

    def _categorize_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """
        Categorize commit messages by conventional commit type.

        Args:
            commits: List of commit messages

        Returns:
            Dict mapping category to list of commit messages
        """
        if not commits:
            return {}

        # Define categories
        CATEGORIES = {
            "feat": "Features",
            "fix": "Bug Fixes",
            "docs": "Documentation",
            "chore": "Chores",
            "refactor": "Refactoring",
            "test": "Tests",
            "style": "Style",
            "perf": "Performance",
            "ci": "CI/CD",
        }

        # Initialize categories dict
        categories = {cat: [] for cat in CATEGORIES.keys()}
        categories["other"] = []

        # Categorize each commit
        for commit in commits:
            categorized = False
            for cat in CATEGORIES.keys():
                # Check if commit starts with category prefix
                if commit.startswith(f"{cat}:") or commit.startswith(f"{cat}("):
                    categories[cat].append(commit)
                    categorized = True
                    break

            if not categorized:
                categories["other"].append(commit)

        # Remove empty categories
        return {cat: msgs for cat, msgs in categories.items() if msgs}

    async def _handle_strategy_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle STRATEGY category intents.

        Routes to appropriate strategy service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 5: Completes intent handler coverage.
        Issue #883: workflow may be None (lazy creation).
        """
        self.logger.info(f"Processing STRATEGY intent: {intent.action}")
        # Issue #883: Extract workflow_id safely
        workflow_id = getattr(workflow, "id", None)

        # #1124: STRATEGY-category dispatch fully migrated onto the action-dispatch
        # rail (strategic_planning/create_plan → final-if-heads; prioritize/set_priorities
        # → prioritization_entry, in workflow_entries.py). The rail short-circuits before
        # this routing; handlers reused unchanged. Anything without a rail entry floors
        # here (#878: conversational response only, no dev stub).
        return await self._handle_unknown_intent(intent, workflow, session_id)

    async def _handle_strategic_planning(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle strategic planning requests - FULLY IMPLEMENTED.

        Creates strategic plans for projects, sprints, features, and issue resolution.
        This is a STRATEGY operation that plans future actions and provides recommendations.

        Supported planning_types:
            - 'sprint': Sprint/iteration planning with 3-phase structure
            - 'feature_roadmap': Feature development roadmap with 4-phase structure
            - 'issue_resolution': Strategic issue resolution with 4-phase structure

        Intent Context Parameters:
            - planning_type (required): Type of plan to create
            - goal (required): Primary goal/objective for the plan
            - timeframe (optional): Duration/deadline (default: type-specific)
            - context (optional): Additional context or constraints

        Returns:
            IntentProcessingResult with plan, recommendations, and metadata
        """
        try:
            # 1. VALIDATION - Check planning_type
            planning_type = intent.context.get("planning_type")
            if not planning_type:
                self.logger.warning("Planning type missing for strategic planning")
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create plan: planning type not specified. Supported types: sprint, feature_roadmap, issue_resolution",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="planning_type_required",
                )

            # Validate goal
            goal = intent.context.get("goal")
            if not goal:
                self.logger.warning("Goal missing for strategic planning")
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create plan: goal not specified. Please provide the objective or goal for this plan.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "planning_type": planning_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="goal_required",
                )

            # Normalize planning_type
            planning_type = planning_type.lower().strip()

            # Validate planning_type is supported
            supported_types = ["sprint", "feature_roadmap", "issue_resolution"]
            if planning_type not in supported_types:
                self.logger.warning(f"Unsupported planning type: {planning_type}")
                return IntentProcessingResult(
                    success=False,
                    message=f"Planning type '{planning_type}' is not supported. Supported types: {', '.join(supported_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "planning_type": planning_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_planning_type",
                )

            # Get optional parameters
            timeframe = intent.context.get("timeframe", "not_specified")
            context = intent.context.get("context", "")

            # 2. CREATE PLAN based on type
            if planning_type == "sprint":
                plan = self._create_sprint_plan(goal, timeframe, context)
            elif planning_type == "feature_roadmap":
                plan = self._create_feature_roadmap(goal, timeframe, context)
            elif planning_type == "issue_resolution":
                plan = self._create_issue_resolution_plan(goal, context)
            else:
                # This should never happen due to validation above
                raise ValueError(f"Unhandled planning type: {planning_type}")

            # 3. GENERATE RECOMMENDATIONS
            recommendations = self._generate_strategic_recommendations(plan, planning_type)

            # 4. BUILD RESPONSE
            self.logger.info(f"Successfully created {planning_type} plan for goal: {goal}")
            return IntentProcessingResult(
                success=True,
                message=f"Successfully created {planning_type} plan: {goal}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "planning_type": planning_type,
                    "goal": goal,
                    "timeframe": timeframe,
                    "plan": plan,
                    "recommendations": recommendations,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            # 5. ERROR HANDLING
            self.logger.error(f"Failed to create strategic plan: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="working on strategic planning",
                error_type="StrategyError",
            )

    def _create_sprint_plan(self, goal: str, timeframe: str, context: str) -> Dict[str, Any]:
        """
        Create a sprint plan with 3-phase structure (Planning, Implementation, Testing).

        Args:
            goal: Sprint goal/objective
            timeframe: Duration (e.g., '2_weeks', '1_week', '3_weeks')
            context: Additional context or constraints

        Returns:
            Dictionary containing sprint plan with phases, tasks, and success criteria
        """
        # Parse timeframe to days
        duration_days = self._parse_timeframe_to_days(timeframe)

        # Create structured 3-phase plan
        plan = {
            "goal": goal,
            "duration": f"{duration_days} days",
            "phases": [
                {
                    "phase": 1,
                    "name": "Planning & Setup",
                    "duration": "1-2 days",
                    "tasks": [
                        {"task": f"Refine requirements for: {goal}", "priority": "high"},
                        {
                            "task": "Set up development environment and dependencies",
                            "priority": "high",
                        },
                        {
                            "task": "Create detailed task breakdown and estimates",
                            "priority": "medium",
                        },
                        {
                            "task": "Identify potential risks and mitigation strategies",
                            "priority": "medium",
                        },
                    ],
                },
                {
                    "phase": 2,
                    "name": "Implementation",
                    "duration": f"{max(duration_days - 4, 5)} days",
                    "tasks": [
                        {"task": f"Implement core functionality for: {goal}", "priority": "high"},
                        {
                            "task": "Write comprehensive unit tests for all components",
                            "priority": "high",
                        },
                        {"task": "Conduct code review and address feedback", "priority": "high"},
                        {"task": "Refactor and optimize implementation", "priority": "medium"},
                        {"task": "Document code and API interfaces", "priority": "medium"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Testing & Deployment",
                    "duration": "2-3 days",
                    "tasks": [
                        {"task": "Run integration tests with existing system", "priority": "high"},
                        {
                            "task": "Perform manual QA testing and edge case validation",
                            "priority": "high",
                        },
                        {"task": "Complete user documentation and guides", "priority": "medium"},
                        {
                            "task": "Deploy to staging environment for validation",
                            "priority": "high",
                        },
                        {"task": "Production deployment with monitoring", "priority": "high"},
                    ],
                },
            ],
            "success_criteria": [
                f"{goal} is fully implemented and tested",
                "All tests passing (unit, integration, manual QA)",
                "Code reviewed and documented",
                "Successfully deployed to production with monitoring enabled",
            ],
        }

        return plan

    def _create_feature_roadmap(self, goal: str, timeframe: str, context: str) -> Dict[str, Any]:
        """
        Create a feature development roadmap with 4-phase structure.

        Args:
            goal: Feature goal/objective
            timeframe: Duration (e.g., '3_months', '1_month', '6_months')
            context: Additional context or constraints

        Returns:
            Dictionary containing feature roadmap with phases, milestones, and dependencies
        """
        # Parse timeframe
        duration_days = self._parse_timeframe_to_days(timeframe)
        num_months = max(1, duration_days // 30)

        # Create structured 4-phase roadmap
        plan = {
            "goal": goal,
            "duration": f"{num_months} month{'s' if num_months != 1 else ''}",
            "phases": [
                {
                    "phase": 1,
                    "name": "Research & Planning",
                    "duration": "2-3 weeks",
                    "tasks": [
                        {
                            "task": "Conduct user interviews and gather requirements",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze competitor solutions and market research",
                            "priority": "medium",
                        },
                        {"task": f"Define key features and scope for: {goal}", "priority": "high"},
                        {"task": "Create technical specification document", "priority": "high"},
                        {"task": "Design mockups and user flows", "priority": "medium"},
                    ],
                },
                {
                    "phase": 2,
                    "name": "MVP Development",
                    "duration": "4-6 weeks",
                    "tasks": [
                        {"task": "Implement core feature functionality", "priority": "high"},
                        {
                            "task": "Build basic user interface with essential workflows",
                            "priority": "high",
                        },
                        {"task": "Create data models and backend services", "priority": "high"},
                        {"task": "Write unit and integration tests", "priority": "high"},
                        {"task": "Internal alpha testing with team", "priority": "high"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Enhancement & Polish",
                    "duration": "3-4 weeks",
                    "tasks": [
                        {
                            "task": "Add advanced features based on MVP feedback",
                            "priority": "medium",
                        },
                        {"task": "Implement performance optimizations", "priority": "high"},
                        {
                            "task": "Polish UI/UX based on alpha testing feedback",
                            "priority": "high",
                        },
                        {
                            "task": "Enhance error handling and edge case coverage",
                            "priority": "medium",
                        },
                        {"task": "Complete comprehensive documentation", "priority": "medium"},
                    ],
                },
                {
                    "phase": 4,
                    "name": "Launch Preparation",
                    "duration": "1-2 weeks",
                    "tasks": [
                        {"task": "Beta testing with external users", "priority": "high"},
                        {
                            "task": "Fix critical bugs and issues from beta feedback",
                            "priority": "high",
                        },
                        {
                            "task": "Create marketing materials and announcements",
                            "priority": "medium",
                        },
                        {"task": "Staged rollout (10% → 50% → 100% of users)", "priority": "high"},
                        {
                            "task": "Monitor performance and user adoption metrics",
                            "priority": "high",
                        },
                    ],
                },
            ],
            "milestones": [
                {
                    "milestone": "Research Complete & Specs Finalized",
                    "target_date": f"Week {min(3, duration_days // 7)}",
                },
                {
                    "milestone": "MVP Released to Alpha Testers",
                    "target_date": f"Week {min(8, duration_days // 7 - 4)}",
                },
                {
                    "milestone": "Beta Release with Full Features",
                    "target_date": f"Week {min(11, duration_days // 7 - 2)}",
                },
                {"milestone": "Public Launch to All Users", "target_date": f"End of {timeframe}"},
            ],
            "dependencies": [
                "User research must complete before MVP design",
                "Alpha testing must pass before enhancement phase",
                "Beta testing must complete before public launch",
            ],
        }

        return plan

    def _create_issue_resolution_plan(self, goal: str, context: str) -> Dict[str, Any]:
        """
        Create an issue resolution plan with 4-phase structure.

        Args:
            goal: Issue description
            context: Issue details, attempted solutions, symptoms

        Returns:
            Dictionary containing issue resolution plan with phases and success criteria
        """
        # Create structured 4-phase resolution plan
        plan = {
            "goal": f"Resolve: {goal}",
            "phases": [
                {
                    "phase": 1,
                    "name": "Investigation",
                    "tasks": [
                        {
                            "task": "Reproduce issue in development/staging environment",
                            "priority": "high",
                        },
                        {
                            "task": "Gather logs, error messages, and stack traces",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze system behavior under issue conditions",
                            "priority": "high",
                        },
                        {"task": "Profile performance and resource usage", "priority": "medium"},
                        {"task": "Review related code and recent changes", "priority": "medium"},
                    ],
                },
                {
                    "phase": 2,
                    "name": "Root Cause Analysis",
                    "tasks": [
                        {
                            "task": "Identify specific code or configuration causing issue",
                            "priority": "high",
                        },
                        {
                            "task": "Determine if issue is code, infrastructure, or data-related",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze dependencies and interactions between components",
                            "priority": "medium",
                        },
                        {
                            "task": "Check for similar historical issues and solutions",
                            "priority": "medium",
                        },
                        {"task": "Document findings and root cause hypothesis", "priority": "high"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Solution Implementation",
                    "tasks": [
                        {"task": "Design fix addressing root cause", "priority": "high"},
                        {
                            "task": "Implement solution with appropriate error handling",
                            "priority": "high",
                        },
                        {
                            "task": "Write regression tests to prevent reoccurrence",
                            "priority": "high",
                        },
                        {
                            "task": "Add monitoring and alerting for issue detection",
                            "priority": "medium",
                        },
                        {"task": "Code review and validation of fix", "priority": "high"},
                    ],
                },
                {
                    "phase": 4,
                    "name": "Verification & Documentation",
                    "tasks": [
                        {"task": "Test fix in staging environment", "priority": "high"},
                        {
                            "task": "Verify issue no longer occurs under original conditions",
                            "priority": "high",
                        },
                        {"task": "Deploy to production with monitoring", "priority": "high"},
                        {"task": "Monitor for 1-2 weeks to confirm resolution", "priority": "high"},
                        {
                            "task": "Document root cause and solution for team knowledge base",
                            "priority": "medium",
                        },
                    ],
                },
            ],
            "success_criteria": [
                f"{goal} is resolved and verified",
                "Issue does not reoccur in production",
                "Regression tests added to prevent future occurrence",
                "Solution documented for team reference",
            ],
        }

        return plan

    def _generate_strategic_recommendations(
        self, plan: Dict[str, Any], planning_type: str
    ) -> List[str]:
        """
        Generate strategic recommendations based on plan type.

        Args:
            plan: The generated plan structure
            planning_type: Type of plan ('sprint', 'feature_roadmap', 'issue_resolution')

        Returns:
            List of strategic recommendations (4-6 recommendations)
        """
        recommendations = []

        if planning_type == "sprint":
            recommendations.extend(
                [
                    "Start with highest priority tasks first to deliver value early",
                    "Schedule daily stand-ups for team alignment and blocker removal",
                    "Reserve 10-20% buffer time for unexpected issues and technical debt",
                    "Conduct sprint retrospective at the end to capture learnings",
                ]
            )
        elif planning_type == "feature_roadmap":
            recommendations.extend(
                [
                    "Validate assumptions with user research early to avoid costly pivots",
                    "Build MVP first (Phase 2), then iterate based on real user feedback",
                    "Maintain regular communication with stakeholders throughout development",
                    "Plan for technical debt reduction alongside new feature work",
                    "Use feature flags for gradual rollout to minimize risk",
                ]
            )
        elif planning_type == "issue_resolution":
            recommendations.extend(
                [
                    "Investigate root cause systematically before implementing fixes",
                    "Use profiling and monitoring tools to gather evidence",
                    "Write regression tests to prevent the issue from recurring",
                    "Document the solution clearly for future team reference",
                ]
            )

        # Add general recommendation for all types
        recommendations.append(
            "Track progress regularly and adjust plan as needed based on actual progress"
        )

        return recommendations

    def _parse_timeframe_to_days(self, timeframe: str) -> int:
        """
        Parse timeframe string to number of days.

        Args:
            timeframe: String like '2_weeks', '1_month', '14_days', 'not_specified'

        Returns:
            Integer number of days

        Examples:
            '2_weeks' → 14
            '1_month' → 30
            '3_months' → 90
            '7_days' → 7
            'not_specified' → 14 (default 2 weeks)
        """
        timeframe_lower = timeframe.lower().strip()

        # Extract numeric portion
        import re

        numbers = re.findall(r"\d+", timeframe_lower)
        number = int(numbers[0]) if numbers else 1

        # Check for time unit
        if "week" in timeframe_lower:
            return number * 7
        elif "month" in timeframe_lower:
            return number * 30
        elif "day" in timeframe_lower:
            return number
        else:
            # Default to 2 weeks if unparseable
            return 14

    async def _handle_prioritization(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle prioritization requests.

        Supports three prioritization types:
        1. issues: Impact/Urgency/Effort scoring
        2. features: RICE framework (Reach/Impact/Confidence/Effort)
        3. tasks: Eisenhower matrix (Urgent/Important quadrants)

        Args:
            intent: Intent object with prioritization context
            workflow_id: Workflow identifier

        Returns:
            IntentProcessingResult with prioritized items
        """
        try:
            # Phase 1: Validate request
            validation_result = self._validate_prioritization_request(intent)
            if validation_result:
                return validation_result

            # Phase 2: Extract items and type
            prioritization_type = intent.context.get("prioritization_type")
            items = self._extract_prioritization_items(intent)

            self.logger.info(f"Prioritizing {len(items)} items using {prioritization_type} method")

            # Phase 3: Calculate scores based on type
            if prioritization_type == "issues":
                scored_items = self._calculate_issue_priority_scores(items)
            elif prioritization_type == "features":
                scored_items = self._calculate_rice_scores(items)
            elif prioritization_type == "tasks":
                scored_items = self._calculate_eisenhower_quadrants(items)
            else:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unsupported prioritization type: {prioritization_type}. Supported types: issues, features, tasks.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "prioritization_type": prioritization_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_prioritization_type",
                    error=f"Unsupported prioritization type: {prioritization_type}",
                    error_type="ValidationError",
                )

            # Phase 4: Rank and format response
            ranked_items = self._rank_items_by_score(scored_items)
            recommendations = self._generate_prioritization_recommendations(
                ranked_items, prioritization_type
            )
            response_message = self._format_prioritization_response(
                ranked_items, prioritization_type
            )

            self.logger.info(f"Prioritization completed: {len(ranked_items)} items ranked")

            return IntentProcessingResult(
                success=True,
                message=response_message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                    "total_items": len(ranked_items),
                    "prioritized_items": ranked_items,
                    "recommendations": recommendations,
                },
                workflow_id=workflow_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to prioritize: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="prioritizing items",
                error_type="StrategyError",
            )

    def _validate_prioritization_request(self, intent: Intent) -> Optional[IntentProcessingResult]:
        """Validate prioritization request has required fields.

        Args:
            intent: Intent object to validate

        Returns:
            IntentProcessingResult if validation fails, None if valid
        """
        # Check for prioritization_type
        prioritization_type = intent.context.get("prioritization_type")
        if not prioritization_type:
            return IntentProcessingResult(
                success=False,
                message="Prioritization type is required. Please specify: issues, features, or tasks.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="prioritization_type_required",
            )

        # Check for items
        items = intent.context.get("items")
        if items is None:
            return IntentProcessingResult(
                success=False,
                message="Items list is required for prioritization.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="items_required",
            )

        # Check items not empty
        if not isinstance(items, list) or len(items) == 0:
            return IntentProcessingResult(
                success=False,
                message="Items list cannot be empty.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                    "item_count": 0,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="items_empty",
            )

        return None  # Validation passed

    def _extract_prioritization_items(self, intent: Intent) -> List[Dict[str, Any]]:
        """Extract and normalize items from intent context.

        Args:
            intent: Intent with items in context

        Returns:
            List of item dictionaries
        """
        items = intent.context.get("items", [])

        # Normalize items to dicts if they're strings
        normalized_items = []
        for item in items:
            if isinstance(item, str):
                normalized_items.append({"title": item})
            elif isinstance(item, dict):
                normalized_items.append(item)
            else:
                self.logger.warning(f"Skipping invalid item type: {type(item)}")

        return normalized_items

    def _calculate_issue_priority_scores(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate priority scores for issues using impact/urgency/effort.

        Formula: priority_score = (impact * urgency) / effort

        Args:
            items: List of issue dictionaries

        Returns:
            Items with priority_score added
        """
        scored_items = []

        for item in items:
            # Get explicit scores or estimate from keywords
            impact = item.get("impact")
            urgency = item.get("urgency")
            effort = item.get("effort")

            # Estimate missing scores from title/description
            if impact is None or urgency is None or effort is None:
                title = item.get("title", "")
                description = item.get("description", "")
                text = f"{title} {description}".lower()

                estimated = self._estimate_scores_from_keywords(text)
                impact = impact or estimated["impact"]
                urgency = urgency or estimated["urgency"]
                effort = effort or estimated["effort"]

            # Calculate priority score
            # Avoid division by zero
            effort = max(effort, 0.1)
            priority_score = (impact * urgency) / effort

            scored_items.append(
                {
                    **item,
                    "impact": impact,
                    "urgency": urgency,
                    "effort": effort,
                    "priority_score": priority_score,
                }
            )

        return scored_items

    def _calculate_rice_scores(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate RICE scores for features.

        Formula: RICE_score = (reach * impact * confidence) / effort

        Args:
            items: List of feature dictionaries

        Returns:
            Items with rice_score added
        """
        scored_items = []

        for item in items:
            # Get RICE components (with defaults)
            reach = item.get("reach", 100)  # Default: 100 users
            impact = item.get("impact", 1.0)  # Default: 1.0 (moderate)
            confidence = item.get("confidence", 0.8)  # Default: 80%
            effort = item.get("effort", 1.0)  # Default: 1 person-month

            # Calculate RICE score
            effort = max(effort, 0.1)  # Avoid division by zero
            rice_score = (reach * impact * confidence) / effort

            scored_items.append(
                {
                    **item,
                    "reach": reach,
                    "impact": impact,
                    "confidence": confidence,
                    "effort": effort,
                    "rice_score": rice_score,
                    "priority_score": rice_score,  # Alias for consistent ranking
                }
            )

        return scored_items

    def _calculate_eisenhower_quadrants(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify tasks into Eisenhower matrix quadrants.

        Quadrants:
        - Q1 (urgent + important): Do First
        - Q2 (not urgent + important): Schedule
        - Q3 (urgent + not important): Delegate
        - Q4 (not urgent + not important): Eliminate

        Args:
            items: List of task dictionaries

        Returns:
            Items with quadrant and priority_score added
        """
        scored_items = []

        # Quadrant priority mapping (for ranking)
        quadrant_priority = {
            "Q1": 100,  # Do First
            "Q2": 75,  # Schedule
            "Q3": 50,  # Delegate
            "Q4": 25,  # Eliminate
        }

        for item in items:
            # Get urgency/importance or estimate from keywords
            urgency = item.get("urgency")
            importance = item.get("importance")

            # Estimate from title/description if missing
            if urgency is None or importance is None:
                title = item.get("title", "")
                description = item.get("description", "")
                text = f"{title} {description}".lower()

                estimated = self._estimate_scores_from_keywords(text)
                urgency = urgency or estimated["urgency"]
                importance = importance or estimated["impact"]  # Use impact as importance

            # Determine quadrant (using median split at 5.5)
            is_urgent = urgency > 5.5
            is_important = importance > 5.5

            if is_urgent and is_important:
                quadrant = "Q1"
                quadrant_label = "Do First"
            elif not is_urgent and is_important:
                quadrant = "Q2"
                quadrant_label = "Schedule"
            elif is_urgent and not is_important:
                quadrant = "Q3"
                quadrant_label = "Delegate"
            else:  # not urgent and not important
                quadrant = "Q4"
                quadrant_label = "Eliminate"

            scored_items.append(
                {
                    **item,
                    "urgency": urgency,
                    "importance": importance,
                    "quadrant": quadrant,
                    "quadrant_label": quadrant_label,
                    "priority_score": quadrant_priority[quadrant],
                }
            )

        return scored_items

    def _estimate_scores_from_keywords(self, text: str) -> Dict[str, float]:
        """Estimate impact/urgency/effort scores from text keywords.

        Args:
            text: Lowercase text to analyze

        Returns:
            Dict with estimated impact, urgency, effort scores (1-10)
        """
        # Impact keywords
        high_impact = ["critical", "severe", "major", "essential", "vital"]
        medium_impact = ["important", "significant", "moderate"]
        low_impact = ["minor", "trivial", "small", "cosmetic"]

        # Urgency keywords
        high_urgency = ["urgent", "asap", "immediate", "now", "emergency"]
        medium_urgency = ["soon", "timely", "prompt"]
        low_urgency = ["later", "eventually", "someday", "future"]

        # Effort keywords
        low_effort = ["quick", "easy", "simple", "trivial", "fast"]
        medium_effort = ["moderate", "medium", "average"]
        high_effort = ["complex", "difficult", "hard", "slow", "large"]

        # Estimate impact (default: 5)
        impact = 5.0
        if any(keyword in text for keyword in high_impact):
            impact = 9.0
        elif any(keyword in text for keyword in medium_impact):
            impact = 6.0
        elif any(keyword in text for keyword in low_impact):
            impact = 3.0

        # Estimate urgency (default: 5)
        urgency = 5.0
        if any(keyword in text for keyword in high_urgency):
            urgency = 9.0
        elif any(keyword in text for keyword in medium_urgency):
            urgency = 6.0
        elif any(keyword in text for keyword in low_urgency):
            urgency = 3.0

        # Estimate effort (default: 5)
        effort = 5.0
        if any(keyword in text for keyword in high_effort):
            effort = 8.0
        elif any(keyword in text for keyword in medium_effort):
            effort = 5.0
        elif any(keyword in text for keyword in low_effort):
            effort = 2.0

        return {
            "impact": impact,
            "urgency": urgency,
            "effort": effort,
        }

    def _rank_items_by_score(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort items by priority_score and assign ranks with proper structure.

        Args:
            items: List of items with priority_score and other fields

        Returns:
            Sorted items with structure:
            {
                "rank": 1,
                "priority_score": 45.0,
                "item": {...original item...},
                "scores": {...extracted scores...},
                "reasoning": "..."
            }
        """
        # Sort by priority_score descending (highest first)
        sorted_items = sorted(items, key=lambda x: x.get("priority_score", 0), reverse=True)

        result = []
        for i, item in enumerate(sorted_items, start=1):
            priority_score = item.get("priority_score", 0)

            # Extract scores based on what fields are present
            scores = {}
            if "impact" in item:
                scores["impact"] = item["impact"]
            if "urgency" in item:
                scores["urgency"] = item["urgency"]
            if "effort" in item:
                scores["effort"] = item["effort"]
            if "reach" in item:
                scores["reach"] = item["reach"]
            if "confidence" in item:
                scores["confidence"] = item["confidence"]
            if "importance" in item:
                scores["importance"] = item["importance"]

            # Create original item (without internal scoring fields)
            original_item = {
                k: v
                for k, v in item.items()
                if k
                not in [
                    "priority_score",
                    "impact",
                    "urgency",
                    "effort",
                    "reach",
                    "confidence",
                    "importance",
                    "quadrant",
                    "quadrant_label",
                    "rice_score",
                ]
            }

            # Generate reasoning
            reasoning = self._generate_prioritization_reasoning(item, priority_score)

            # Build structured result
            structured_item = {
                "rank": i,
                "priority_score": priority_score,
                "item": original_item,
                "scores": scores,
                "reasoning": reasoning,
            }

            # Add quadrant info for Eisenhower matrix
            if "quadrant" in item:
                structured_item["quadrant"] = item["quadrant"]
                structured_item["quadrant_label"] = item.get("quadrant_label", "")

            result.append(structured_item)

        return result

    def _generate_prioritization_reasoning(
        self, item: Dict[str, Any], priority_score: float
    ) -> str:
        """Generate reasoning explanation for prioritization.

        Args:
            item: Item with scoring fields
            priority_score: Calculated priority score

        Returns:
            Human-readable reasoning string
        """
        title = item.get("title", "Item")

        # Issues prioritization reasoning
        if "impact" in item and "urgency" in item and "effort" in item:
            impact = item["impact"]
            urgency = item["urgency"]
            effort = item["effort"]

            return (
                f"{title} has high priority (score: {priority_score:.1f}) due to "
                f"impact={impact}, urgency={urgency}, and effort={effort}. "
                f"Formula: (impact × urgency) / effort = ({impact} × {urgency}) / {effort}"
            )

        # RICE framework reasoning
        elif "reach" in item and "confidence" in item:
            reach = item["reach"]
            impact = item.get("impact", 1.0)
            confidence = item["confidence"]
            effort = item.get("effort", 1.0)

            return (
                f"{title} scores {priority_score:.1f} using RICE framework: "
                f"reach={reach}, impact={impact}, confidence={confidence:.0%}, effort={effort}. "
                f"Formula: (reach × impact × confidence) / effort"
            )

        # Eisenhower matrix reasoning
        elif "quadrant" in item:
            quadrant = item["quadrant"]
            quadrant_label = item.get("quadrant_label", "")
            urgency = item.get("urgency", 5)
            importance = item.get("importance", 5)

            return (
                f"{title} falls in {quadrant} ({quadrant_label}) with "
                f"urgency={urgency}, importance={importance}. "
                f"This quadrant has priority score {priority_score:.0f}."
            )

        # Generic fallback
        else:
            return f"{title} has priority score of {priority_score:.1f}"

    def _generate_prioritization_recommendations(
        self, ranked_items: List[Dict[str, Any]], prioritization_type: str
    ) -> List[str]:
        """Generate recommendations based on prioritization results.

        Args:
            ranked_items: Ranked items with scores
            prioritization_type: Type of prioritization

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not ranked_items:
            return ["No items to prioritize."]

        # Get top and bottom items
        top_item = ranked_items[0]

        if prioritization_type == "issues":
            # Issues recommendations
            recommendations.append(
                f"Start with rank 1: {top_item['item'].get('title', 'Top item')} "
                f"(priority score: {top_item['priority_score']:.1f})"
            )

            # Check for low-effort high-impact items
            quick_wins = [
                item
                for item in ranked_items
                if item["scores"].get("effort", 10) <= 3 and item["rank"] <= 5
            ]
            if quick_wins:
                recommendations.append(
                    f"Found {len(quick_wins)} quick win(s) in top 5 (low effort, high priority)"
                )

            # Warn about low-priority items
            if len(ranked_items) > 5:
                low_priority = ranked_items[-1]
                recommendations.append(
                    f"Consider deferring rank {low_priority['rank']}: "
                    f"{low_priority['item'].get('title', 'Last item')} "
                    f"(score: {low_priority['priority_score']:.1f})"
                )

        elif prioritization_type == "features":
            # RICE recommendations
            recommendations.append(
                f"Highest RICE score: {top_item['item'].get('title', 'Top feature')} "
                f"({top_item['priority_score']:.1f})"
            )

            # Check confidence levels
            low_confidence = [
                item for item in ranked_items[:3] if item["scores"].get("confidence", 1.0) < 0.5
            ]
            if low_confidence:
                recommendations.append(
                    f"Warning: {len(low_confidence)} top-ranked feature(s) have low confidence (<50%). "
                    "Consider validating assumptions."
                )

        elif prioritization_type == "tasks":
            # Eisenhower recommendations
            q1_items = [item for item in ranked_items if item.get("quadrant") == "Q1"]
            q2_items = [item for item in ranked_items if item.get("quadrant") == "Q2"]
            q3_items = [item for item in ranked_items if item.get("quadrant") == "Q3"]
            q4_items = [item for item in ranked_items if item.get("quadrant") == "Q4"]

            if q1_items:
                recommendations.append(
                    f"Do First (Q1): {len(q1_items)} urgent and important task(s)"
                )
            if q2_items:
                recommendations.append(
                    f"Schedule (Q2): {len(q2_items)} important but not urgent task(s)"
                )
            if q3_items:
                recommendations.append(
                    f"Delegate (Q3): {len(q3_items)} urgent but less important task(s)"
                )
            if q4_items:
                recommendations.append(
                    f"Eliminate (Q4): {len(q4_items)} low-priority task(s) to eliminate"
                )

        return recommendations

    def _format_prioritization_response(
        self, ranked_items: List[Dict[str, Any]], prioritization_type: str
    ) -> str:
        """Format human-readable response message.

        Args:
            ranked_items: List of ranked items
            prioritization_type: Type of prioritization used

        Returns:
            Formatted message string
        """
        if not ranked_items:
            return "No items to prioritize."

        count = len(ranked_items)

        # Get top 3 items for preview
        top_items = ranked_items[:3]
        preview = []

        for item in top_items:
            title = item.get("title", "Untitled")
            rank = item.get("rank", 0)
            score = item.get("priority_score", 0)

            if prioritization_type == "issues":
                preview.append(f"{rank}. {title} (score: {score:.2f})")
            elif prioritization_type == "features":
                preview.append(f"{rank}. {title} (RICE: {score:.2f})")
            elif prioritization_type == "tasks":
                quadrant = item.get("quadrant_label", "Unknown")
                preview.append(f"{rank}. {title} ({quadrant})")

        preview_text = "\n".join(preview)

        return (
            f"Prioritized {count} items using {prioritization_type} method:\n\n"
            f"{preview_text}\n\n"
            f"See intent_data.prioritized_items for complete ranking."
        )

    async def _handle_learning_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle LEARNING category intents.

        Routes to appropriate learning service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 6: Completes intent handler coverage.
        Issue #883: workflow may be None (lazy creation).
        """
        self.logger.info(f"Processing LEARNING intent: {intent.action}")
        # Issue #883: Extract workflow_id safely
        workflow_id = getattr(workflow, "id", None)

        # #1124: LEARNING-category dispatch migrated onto the action-dispatch rail
        # (learn_pattern/detect_pattern → final-if-heads in workflow_entries.py;
        # _handle_learn_pattern reused unchanged). The rail short-circuits before this
        # routing; anything without a rail entry floors here (conversational response).
        return await self._handle_unknown_intent(intent, workflow, session_id)

    async def _handle_learn_pattern(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle pattern learning requests.

        Learns patterns from historical data to identify recurring themes,
        similar issues, and common approaches. Helps recognize patterns
        and improve future decision-making.

        Supported pattern_types:
            - 'issue_similarity': Find similar issues and common patterns
            - 'resolution_patterns': Learn solution approaches for problems
            - 'tag_patterns': Learn tag/classification patterns

        Args:
            intent: Intent object with pattern learning context
            workflow_id: Workflow identifier

        Returns:
            IntentProcessingResult with learned patterns
        """
        try:
            # Phase 1: Validate request
            validation_result = self._validate_learning_request(intent)
            if validation_result:
                return validation_result

            # Phase 2: Fetch historical data
            self.logger.info("Fetching historical data for pattern learning")
            historical_data = await self._fetch_learning_data(intent)

            if not historical_data or len(historical_data) == 0:
                self.logger.info("No historical data found for pattern learning")
                return IntentProcessingResult(
                    success=True,
                    message="No historical data available for pattern learning.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "pattern_type": intent.context.get("pattern_type"),
                        "total_items_analyzed": 0,
                        "patterns_count": 0,
                        "patterns_found": [],
                    },
                    workflow_id=workflow_id,
                )

            # Phase 3: Learn patterns based on type
            pattern_type = intent.context.get("pattern_type")
            search_query = intent.context.get("query", "")
            min_occurrences = intent.context.get("min_occurrences", 2)

            if pattern_type == "issue_similarity":
                patterns = self._learn_issue_similarity_patterns(
                    historical_data, search_query, min_occurrences
                )
            elif pattern_type == "resolution_patterns":
                patterns = self._learn_resolution_patterns(historical_data, min_occurrences)
            elif pattern_type == "tag_patterns":
                patterns = self._learn_tag_patterns(historical_data, min_occurrences)
            else:
                # Should not reach here due to validation
                raise ValueError(f"Unhandled pattern type: {pattern_type}")

            # Phase 4: Format and return
            response_message = self._format_learning_response(patterns, len(historical_data))

            self.logger.info(f"Learned {len(patterns)} patterns from {len(historical_data)} items")

            return IntentProcessingResult(
                success=True,
                message=response_message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                    "total_items_analyzed": len(historical_data),
                    "patterns_count": len(patterns),
                    "patterns_found": patterns,
                },
                workflow_id=workflow_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to learn pattern: {e}", exc_info=True)
            return self._make_error_result(
                intent=intent,
                workflow_id=workflow_id,
                error=e,
                context="learning patterns",
                error_type="LearningError",
            )

    def _validate_learning_request(self, intent: Intent) -> Optional[IntentProcessingResult]:
        """Validate pattern learning request has required fields.

        Args:
            intent: Intent object to validate

        Returns:
            IntentProcessingResult if validation fails, None if valid
        """
        # Check for pattern_type
        pattern_type = intent.context.get("pattern_type")
        if not pattern_type:
            return IntentProcessingResult(
                success=False,
                message="Pattern type is required. Supported: issue_similarity, resolution_patterns, tag_patterns.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="pattern_type_required",
            )

        # Check for source
        source = intent.context.get("source")
        if not source:
            return IntentProcessingResult(
                success=False,
                message="Source is required (e.g., github_issues).",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="source_required",
            )

        # Validate pattern_type
        supported_types = ["issue_similarity", "resolution_patterns", "tag_patterns"]
        if pattern_type not in supported_types:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported pattern type: {pattern_type}. Supported: {', '.join(supported_types)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                },
                workflow_id=None,
                requires_clarification=True,
                clarification_type="unsupported_pattern_type",
            )

        return None  # Validation passed

    async def _fetch_learning_data(self, intent: Intent) -> List[Dict[str, Any]]:
        """Fetch historical data for pattern learning.

        Args:
            intent: Intent with source and query parameters

        Returns:
            List of historical data items
        """
        source = intent.context.get("source")
        search_query = intent.context.get("query", "")

        if source == "github_issues":
            # Issue #1042: was calling nonexistent GitHubDomainService.list_issues
            # with repository="piper-morgan" literal; refactored to use the
            # GitHubIntegrationRouter (self-resolves the repo internally).
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github_router = GitHubIntegrationRouter()

            try:
                # Fetch recent issues
                issues = await github_router.get_recent_issues(limit=100)

                # Filter by search query if provided
                if search_query:
                    query_lower = search_query.lower()
                    issues = [
                        issue
                        for issue in issues
                        if query_lower in (issue.title or "").lower()
                        or query_lower in (issue.body or "").lower()
                    ]

                # Convert to standard format
                return [
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "body": issue.body,
                        "labels": [label.name for label in (issue.labels or [])],
                        "state": issue.state,
                    }
                    for issue in issues
                ]

            except Exception as e:
                self.logger.error(f"Failed to fetch GitHub issues: {e}")
                return []

        # Future: Add support for other sources
        return []

    def _learn_issue_similarity_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        search_query: str,
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn patterns from similar issues using keyword clustering.

        Args:
            historical_data: List of issue dictionaries
            search_query: Optional query string (for context)
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of identified pattern dictionaries
        """
        if len(historical_data) < min_occurrences:
            return []

        # Extract keywords and group issues
        keyword_groups = {}
        stop_words = {
            "the",
            "a",
            "an",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "is",
            "are",
            "be",
            "by",
        }

        for item in historical_data:
            title = item.get("title", "").lower()
            words = title.split()

            # Filter significant keywords
            keywords = [w for w in words if len(w) > 3 and w not in stop_words]

            for keyword in keywords:
                keyword_groups.setdefault(keyword, []).append(item)

        # Create patterns from groups with enough occurrences
        patterns = []

        for keyword, items in keyword_groups.items():
            if len(items) >= min_occurrences:
                # Calculate confidence
                confidence = min(len(items) / 10, 1.0)  # Scale to 1.0

                # Extract common labels
                all_labels = []
                for item in items:
                    all_labels.extend(item.get("labels", []))

                # Count label occurrences
                label_counts = {}
                for label in all_labels:
                    label_counts[label] = label_counts.get(label, 0) + 1

                # Keep labels appearing in 30%+ of items
                common_labels = [
                    label for label, count in label_counts.items() if count >= len(items) * 0.3
                ]

                # Generate recommendations
                recommendations = self._generate_pattern_recommendations(
                    keyword, common_labels, len(items)
                )

                # Create pattern
                pattern = {
                    "pattern_id": f"keyword_{keyword}",
                    "description": f"Issues related to '{keyword}'",
                    "keyword": keyword,
                    "confidence": confidence,
                    "occurrences": len(items),
                    "common_labels": common_labels,
                    "examples": [
                        {"number": item["number"], "title": item["title"]}
                        for item in items[:5]  # First 5 examples
                    ],
                    "recommended_actions": recommendations,
                }

                patterns.append(pattern)

        # Sort by occurrences (most common first)
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)

        # Return top 10 patterns
        return patterns[:10]

    def _learn_resolution_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn solution patterns from resolved issues.

        Args:
            historical_data: List of issue dictionaries
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of resolution pattern dictionaries
        """
        # Filter to closed issues only
        closed_issues = [item for item in historical_data if item.get("state") == "closed"]

        if len(closed_issues) < min_occurrences:
            return []

        # Group by common resolution labels
        resolution_groups = {}

        for item in closed_issues:
            labels = item.get("labels", [])
            for label in labels:
                if label.lower() in ["fixed", "resolved", "completed", "duplicate", "wontfix"]:
                    resolution_groups.setdefault(label, []).append(item)

        # Create patterns
        patterns = []
        for resolution_type, items in resolution_groups.items():
            if len(items) >= min_occurrences:
                patterns.append(
                    {
                        "pattern_id": f"resolution_{resolution_type}",
                        "description": f"Issues resolved as '{resolution_type}'",
                        "resolution_type": resolution_type,
                        "confidence": min(len(items) / 5, 1.0),
                        "occurrences": len(items),
                        "examples": [
                            {"number": item["number"], "title": item["title"]} for item in items[:3]
                        ],
                        "recommended_actions": [
                            f"Review {len(items)} similar resolutions of type '{resolution_type}'"
                        ],
                    }
                )

        return patterns

    def _learn_tag_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn tag/label patterns from historical issues.

        Args:
            historical_data: List of issue dictionaries
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of tag pattern dictionaries
        """
        if len(historical_data) < min_occurrences:
            return []

        # Analyze label co-occurrence
        label_pairs = {}

        for item in historical_data:
            labels = sorted(item.get("labels", []))
            if len(labels) >= 2:
                # Create pairs
                for i in range(len(labels)):
                    for j in range(i + 1, len(labels)):
                        pair = (labels[i], labels[j])
                        label_pairs[pair] = label_pairs.get(pair, 0) + 1

        # Create patterns from frequent pairs
        patterns = []
        for (label1, label2), count in label_pairs.items():
            if count >= min_occurrences:
                patterns.append(
                    {
                        "pattern_id": f"tags_{label1}_{label2}",
                        "description": f"Labels '{label1}' and '{label2}' often appear together",
                        "label_pair": [label1, label2],
                        "confidence": min(count / 10, 1.0),
                        "occurrences": count,
                        "recommended_actions": [
                            f"When applying '{label1}', consider also applying '{label2}'"
                        ],
                    }
                )

        # Sort by occurrences
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)

        return patterns[:10]

    def _generate_pattern_recommendations(
        self, keyword: str, common_labels: List[str], occurrences: int
    ) -> List[str]:
        """Generate actionable recommendations for a pattern.

        Args:
            keyword: The keyword defining the pattern
            common_labels: Labels commonly associated with the pattern
            occurrences: Number of times pattern occurred

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Always recommend reviewing similar issues
        recommendations.append(f"Review {occurrences} similar past issues with '{keyword}'")

        # Recommend common labels if available
        if common_labels:
            recommendations.append(f"Consider applying labels: {', '.join(common_labels[:3])}")

        # Add frequency-based recommendations
        if occurrences >= 5:
            recommendations.append(
                f"High frequency pattern ({occurrences} occurrences) - consider root cause analysis"
            )

        # Add keyword-specific recommendations
        if keyword in ["bug", "error", "issue", "problem", "fail", "crash"]:
            recommendations.append(
                "Investigate if a systemic fix can address multiple related issues"
            )
        elif keyword in ["performance", "slow", "timeout", "latency"]:
            recommendations.append("Consider performance monitoring and profiling tools")
        elif keyword in ["security", "auth", "authentication", "authorization"]:
            recommendations.append("Review security best practices and recent CVEs")

        return recommendations

    def _format_learning_response(self, patterns: List[Dict[str, Any]], total_analyzed: int) -> str:
        """Format human-readable response message with consciousness.

        Issue #636: Now uses consciousness wrapper for identity voice.

        Args:
            patterns: List of identified patterns
            total_analyzed: Total number of items analyzed

        Returns:
            Formatted message string with consciousness
        """
        return format_patterns_learned_conscious(patterns, total_analyzed)

    # Issue #907: Known generic template signatures from canonical handlers.
    # When a handler returns one of these, the response doesn't actually address
    # the user's query — route to the conversational floor instead.
    # Issue #908: This signature list is now a FALLBACK. Handlers should set
    # is_generic_response=True in their return dict. Signatures catch handlers
    # that haven't been updated yet.
    _GENERIC_CANONICAL_SIGNATURES = [
        # GUIDANCE handler: standard priority template
        "Based on your current priorities and the time of day:",
        # GUIDANCE handler: granular variant
        "Here's comprehensive guidance for your focus:",
        # GUIDANCE consolidated variants (time-based generic)
        "Focus: Deep work",
        "Focus: Team coordination",
        "Focus: Task execution",
        "Focus: Wrap-up and handoff",
        "Focus: Strategic planning",
    ]

    def _is_generic_canonical_response(self, canonical_result: dict, response_message: str) -> bool:
        """
        Issue #907: Detect generic template responses from canonical handlers.
        Issue #908: Check structural flag first, fall back to signature matching.

        Handlers that have been updated set is_generic_response=True in their
        return dict. For handlers not yet updated, we fall back to substring
        matching against known template signatures.

        Args:
            canonical_result: The full dict returned by the canonical handler
            response_message: The "message" field from the handler result

        Returns:
            True if the response is generic (either flagged or signature-matched)
        """
        # Issue #908 Phase 1: Check structural flag first
        if canonical_result.get("is_generic_response", False):
            return True

        # Issue #907 fallback: Signature matching for handlers not yet updated
        if not response_message:
            return False
        if any(sig in response_message for sig in self._GENERIC_CANONICAL_SIGNATURES):
            self.logger.info(
                "generic_response_signature_fallback",
                message_prefix=response_message[:80],
                note="Handler should set is_generic_response=True instead",
            )
            return True

        return False

    # ---- Issue #911 Phase 2: Action Gate ----

    def _requires_canonical_handler(self, intent: Intent) -> bool:
        """
        Issue #911 Phase 2: Determine if an intent requires a canonical handler
        (an operation the LLM cannot perform on its own).

        Returns True ONLY for intents that need side effects, database writes,
        or deterministic fast-path responses.
        """
        category = intent.category.value.upper()

        # PORTFOLIO: all operations (add/delete/archive/restore) — always canonical
        if category == "PORTFOLIO":
            return True

        # EXECUTION: all operations (create issue, manage todos, etc.) — always canonical
        if category == "EXECUTION":
            return True

        # CONVERSATION with action="greeting": has onboarding/calendar side effects
        # Greeting stays canonical until floor has calendar context integration
        if category == "CONVERSATION" and intent.action == "greeting":
            return True

        # TEMPORAL: pure date/time queries stay canonical (deterministic, sub-ms).
        # Conversational temporal queries (agenda, retrospective, last activity,
        # project duration) migrate to floor for contextual LLM responses (#965).
        # Decision rationale: M1 canonical retest showed Q7-Q10 scoring 1/9
        # (Context=0) — the canonical handlers return templates without real data.
        #
        # Note: The pre-classifier assigns get_current_time to ALL temporal queries
        # including conversational ones. We use message keywords to distinguish.
        if category == "TEMPORAL":
            import re

            msg = (
                intent.original_message
                or (intent.context.get("original_message", "") if intent.context else "")
            ).lower()
            # Conversational temporal keywords → floor
            _TEMPORAL_FLOOR_KEYWORDS = re.compile(
                r"yesterday|accomplish|agenda|schedule|last time|how long|"
                r"duration|worked on|retrospective|done today|did we|"
                r"been working|last.*activity|week look|recurring"
            )
            if msg and _TEMPORAL_FLOOR_KEYWORDS.search(msg):
                return False  # Conversational → floor
            # Pure date/time query → canonical
            return True

        # STATUS: migrated to floor (#925 Phase 3, Apr 13).
        # Canonical handlers returned templates that passed via safety-net → floor
        # roundtrip. Direct floor routing eliminates the roundtrip.
        # M1 retest: Q11-14 already scored 9/9 via floor.
        if category == "STATUS":
            return False

        # PRIORITY: migrated to floor (#925 Phase 3, Apr 13).
        # Same rationale as STATUS. M1 retest: Q21 scored 9/9 via floor.
        if category == "PRIORITY":
            return False

        # IDENTITY: ALL identity queries now go to floor (Apr 8 decision).
        # The floor generates much better responses than canned templates.
        # Previous behavior: core identity → canonical template, adjacent → floor.
        # New behavior: all identity → floor with context.
        # Decision rationale: UAT Round 2 showed canned "I'm Piper Morgan..."
        # template scoring 1/3 on Colleague Test. Floor scores 7+.
        if category == "IDENTITY":
            return False

        # GUIDANCE setup requests: canonical (triggers setup workflow)
        if category == "GUIDANCE":
            setup_topic = self.canonical_handlers._detect_setup_request(intent)
            if setup_topic:
                return True
            return False

        return False

    # _is_adjacent_identity removed (#963) — all IDENTITY routes to floor since Apr 8.
    # Detection methods it called (_detect_health_check_request, etc.) also removed.

    def _should_route_to_floor(self, intent: Intent) -> bool:
        """
        Issue #911 Phase 2: Determine if an intent should go to the conversational
        floor with context assembly.

        This is the inverse of _requires_canonical_handler, but only for categories
        that have been migrated to the Action Gate pattern. Categories not yet migrated
        fall through to the existing can_handle() → handle() path.
        """
        category = intent.category.value.upper()

        # Categories fully migrated to Action Gate floor routing:
        _FLOOR_ROUTED_CATEGORIES = {
            "GUIDANCE",  # Phase 1: already floor-routed
            "IDENTITY",  # Phase 2: all identity → floor (Apr 8)
            "DISCOVERY",  # Phase 2: capabilities context → floor
            "TRUST",  # Phase 2: trust data context → floor
            "MEMORY",  # Phase 2: history context → floor
            "CONVERSATION",  # Phase 2: chitchat/farewell/thanks → floor
            "TEMPORAL",  # Phase 3: non-date temporal → floor (#965)
            "STATUS",  # Phase 3: project status → floor (#925)
            "PRIORITY",  # Phase 3: priority queries → floor (#925)
            "UNKNOWN",  # Already floor-routed since #907
        }

        if category not in _FLOOR_ROUTED_CATEGORIES:
            return False

        # If the Action Gate says canonical is required, don't route to floor
        if self._requires_canonical_handler(intent):
            return False

        return True

    async def _handle_floor_with_context(
        self,
        intent: Intent,
        session_id: str,
        user_id: str = None,
        formality_baseline: float = None,
        trust_stage=None,
    ) -> IntentProcessingResult:
        """
        Issue #911 Phase 2: Route intent through the conversational floor
        with category-specific context assembly.

        Uses ContextAssembler to gather structured data, then creates
        FloorContext and calls ConversationalFloor.respond().
        """
        category = intent.category.value.upper()

        self.logger.info(
            "action_gate_routing_to_floor",
            category=category,
            action=intent.action,
            original_message=intent.original_message,
        )

        from services.intent_service.context_assembler import ContextAssembler
        from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

        # Issue #1030 R4: provenance starts None; only the standard
        # ContextAssembler path populates it (GUIDANCE uses a different
        # _assemble_guidance_context pathway with no provenance attribution yet).
        domain_context_provenance: Optional[Dict[str, Dict[str, Any]]] = None

        # For GUIDANCE, use the existing specialized context assembler
        if category == "GUIDANCE":
            domain_context = await self._assemble_guidance_context(intent, session_id, user_id)
        else:
            # Use the new ContextAssembler for other categories
            assembler = ContextAssembler()
            # Issue #1030: pass intent_action so MEMORY/pull_insights gets
            # InsightRepository enrichment distinct from MEMORY/get_memory.
            intent_action = getattr(intent, "action", None) if intent else None
            domain_context = await assembler.gather_context(
                intent_category=category,
                user_id=user_id,
                session_id=session_id,
                intent_action=intent_action,
            )
            # Issue #1030 R4: capture per-gatherer provenance map to pass to floor
            domain_context_provenance = assembler.get_last_provenance()

        # Gather conversation history (#1122: shared builder, excludes in-flight turn)
        history = build_recent_history(session_id, user_id)

        floor_ctx = FloorContext(
            user_message=intent.original_message
            or (intent.context.get("original_message", "") if intent.context else ""),
            session_id=session_id,
            user_id=user_id,
            conversation_history=history,
            trust_stage=trust_stage.value if trust_stage else None,
            formality_baseline=formality_baseline,
            intent_category=category,
            intent_action=intent.action,
            intent_confidence=intent.confidence,
            domain_context=domain_context,
            # Issue #1030 R4: pass per-gatherer provenance for floor to copy
            # into FloorResponse.provenance (which we'll then write to the
            # turn_provenance sidecar below).
            domain_context_provenance=domain_context_provenance,
        )

        floor = ConversationalFloor()
        response = await floor.respond(floor_ctx)

        # Issue #913: Tag session for continuation rate tracking
        try:
            conv_ctx = get_or_create_context(session_id, user_id=user_id)
            conv_ctx.last_response_was_floor = True
            conv_ctx.last_floor_category = category

            # Issue #1030 R4 bug fix 2026-06-02: intent_service calls
            # IntentClassifier.classify() (basic), not classify_conscious(), so
            # the in-memory conv_ctx.add_turn() side effect never fires for
            # pre-classifier-routed intents (which is ~most of them). Without
            # a turn, Step 6's `if conv_ctx.turns:` was always False → write
            # never happened. Add the turn explicitly here for the current
            # floor-routed message so the sidecar has somewhere to land.
            user_msg = intent.original_message or (
                intent.context.get("original_message", "") if intent.context else ""
            )
            # #1122: the outer process_intent now records the in-flight turn for
            # every path, so this site normally just annotates it with the
            # classified intent (the provenance write below needs a turn either
            # way). Add only if the in-flight record is absent (direct internal
            # calls, tests) — and never add an empty message.
            if conv_ctx.turns and conv_ctx.turns[-1].response is None:
                if conv_ctx.turns[-1].intent is None:
                    conv_ctx.turns[-1].intent = intent
            elif user_msg and (not conv_ctx.turns or conv_ctx.turns[-1].message != user_msg):
                conv_ctx.add_turn(message=user_msg, intent=intent)

            # Issue #1030 R4: write per-turn provenance to the sidecar so future
            # "why did you suggest that?" lookups can ground their citation.
            if conv_ctx.turns:
                latest_turn = conv_ctx.turns[-1]
                # Phase 1: write floor response provenance (may be empty for
                # floor calls without domain_context like ethics-decline)
                turn_prov = dict(response.provenance) if response.provenance else {}

                # Phase 2 (R6 mitigation): merge push payload provenance if a
                # push was appended this turn. Floor stashes it in session
                # state since it doesn't have a handle to ConversationContext.
                push_state = (
                    floor._push_session_state.get(session_id)
                    if hasattr(floor, "_push_session_state")
                    else None
                )
                if push_state and "last_push_provenance" in push_state:
                    turn_prov["push_insight"] = push_state["last_push_provenance"]
                    # Consume the stash so it doesn't bleed into the next turn
                    del push_state["last_push_provenance"]

                if turn_prov:
                    conv_ctx.turn_provenance[latest_turn.id] = turn_prov
        except Exception:
            pass  # Best-effort instrumentation + provenance

        return IntentProcessingResult(
            success=True,
            message=response.message,
            intent_data={
                "category": category,
                "action": intent.action,
                "confidence": intent.confidence,
                "original_message": intent.original_message,
                "floor_hit": True,  # Issue #911: Instrumentation
                "context_keys": list(domain_context.keys()),
            },
            workflow_id=None,  # No workflow — conversational response
            requires_clarification=False,
        )

    async def _assemble_guidance_context(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict[str, Any]:
        """
        Issue #911: Assemble domain context for GUIDANCE intents routed to the floor.

        Reuses the canonical handler's data-gathering methods but skips the
        template formatting. The floor LLM gets the raw facts and decides
        how to use them in its response.
        """
        from datetime import datetime

        context = {}
        current_time = datetime.now()
        context["current_time"] = current_time.strftime("%I:%M %p")

        handlers = self.canonical_handlers

        # User context (projects, priorities)
        user_context = None
        try:
            from services.user_context_service import user_context_service

            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception:
            pass

        # Calendar context
        try:
            calendar_context = await handlers._get_calendar_context(user_id=user_id)
            if calendar_context:
                context["calendar"] = calendar_context
        except Exception:
            pass

        # Project metadata
        projects = user_context.projects if user_context else []
        if projects:
            try:
                project_metadata = await handlers._get_project_metadata(projects)
                if project_metadata:
                    context["projects"] = project_metadata
                else:
                    context["projects"] = projects  # At least list the names
            except Exception:
                context["projects"] = projects

        # Priority metadata
        try:
            priority_metadata = await handlers._get_priority_metadata(user_id=user_id)
            if priority_metadata:
                context["priorities"] = {
                    "user_priorities": (user_context.priorities if user_context else []),
                    "urgent_items": len(priority_metadata.get("high_priority_issues", [])),
                    "total_open_issues": priority_metadata.get("total_open_issues", 0),
                }
            elif user_context and user_context.priorities:
                context["priorities"] = {
                    "user_priorities": user_context.priorities,
                    "urgent_items": 0,
                }
        except Exception:
            pass

        return context

    async def _handle_guidance_via_floor(
        self,
        intent: Intent,
        session_id: str,
        user_id: str = None,
        formality_baseline: float = None,
        trust_stage=None,
    ) -> IntentProcessingResult:
        """
        Issue #911 Phase 1: Route GUIDANCE intents through the conversational floor
        with assembled domain context instead of template responses.

        The floor gets calendar, projects, and priorities as factual context,
        then generates a response that actually addresses the user's question.
        """
        self.logger.info(
            "guidance_routed_to_floor",
            action=intent.action,
            original_message=intent.original_message,
        )

        from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

        # Assemble domain context (calendar, projects, priorities)
        domain_context = await self._assemble_guidance_context(intent, session_id, user_id)

        # Gather conversation history (#1122: shared builder, excludes in-flight turn)
        history = build_recent_history(session_id, user_id)

        floor_ctx = FloorContext(
            user_message=intent.original_message
            or (intent.context.get("original_message", "") if intent.context else ""),
            session_id=session_id,
            user_id=user_id,
            conversation_history=history,
            trust_stage=trust_stage.value if trust_stage else None,
            formality_baseline=formality_baseline,
            intent_category="GUIDANCE",
            intent_action=intent.action,
            intent_confidence=intent.confidence,
            domain_context=domain_context,
        )

        floor = ConversationalFloor()
        response = await floor.respond(floor_ctx)

        # Issue #913: Tag session for continuation rate tracking
        try:
            conv_ctx_tag = get_or_create_context(session_id, user_id=user_id)
            conv_ctx_tag.last_response_was_floor = True
            conv_ctx_tag.last_floor_category = "GUIDANCE"
        except Exception:
            pass  # Best-effort instrumentation

        return IntentProcessingResult(
            success=True,
            message=response.message,
            intent_data={
                "category": "GUIDANCE",
                "action": intent.action,
                "confidence": intent.confidence,
                "original_message": intent.original_message,
                "floor_hit": True,  # Issue #911: Instrumentation
                "context_keys": list(domain_context.keys()),
            },
            workflow_id=None,  # No workflow — conversational response
            requires_clarification=False,
        )

    async def _handle_unknown_intent(
        self,
        intent: Intent,
        workflow,
        session_id: str,
        user_id: str = None,
        formality_baseline: float = None,
        trust_stage=None,
        domain_context: Optional[Dict[str, Any]] = None,
    ) -> IntentProcessingResult:
        """
        Handle UNKNOWN category intents via conversational floor.

        Issue #907: Instead of a dead-end deflection, engage conversationally
        using the LLM with Piper's full context. The floor thinks WITH the user
        rather than telling them "I can't do that."

        GREAT-4D Phase 7: Completes intent handler coverage.
        """
        self.logger.info(f"Processing UNKNOWN intent via conversational floor: {intent.action}")

        # Issue #907: Build floor context from available state
        from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

        # Gather conversation history (#1122: shared builder, excludes in-flight turn)
        history = build_recent_history(session_id, user_id)

        floor_ctx = FloorContext(
            user_message=intent.original_message
            or (intent.context.get("original_message", "") if intent.context else ""),
            session_id=session_id,
            user_id=user_id,
            conversation_history=history,
            trust_stage=trust_stage.value if trust_stage else None,
            formality_baseline=formality_baseline,
            intent_category="UNKNOWN",
            intent_action=intent.action,
            intent_confidence=intent.confidence,
            # #1187: optional fetched source content for the floor to summarize.
            domain_context=domain_context,
        )

        floor = ConversationalFloor()
        response = await floor.respond(floor_ctx)

        # Issue #913: Tag session for continuation rate tracking
        try:
            conv_ctx_tag = get_or_create_context(session_id, user_id=user_id)
            conv_ctx_tag.last_response_was_floor = True
            conv_ctx_tag.last_floor_category = "UNKNOWN"
        except Exception:
            pass  # Best-effort instrumentation

        return IntentProcessingResult(
            success=True,
            message=response.message,
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "original_message": intent.original_message,
                "floor_hit": True,  # Issue #907: Instrumentation flag
            },
            workflow_id=None,  # No workflow — conversational response
            requires_clarification=False,
        )

    def _make_error_result(
        self,
        intent: "Intent",
        workflow_id: str,
        error: Exception,
        context: str,
        error_type: str = "InternalError",
    ) -> IntentProcessingResult:
        """Create conversational error result using UserFriendlyErrorService.

        Issue #876: Raw exception text should never reach users. This method
        converts technical errors into conversational messages while preserving
        the raw error in the `error` field for logging/debugging.
        """
        conversational_message = self._friendly_errors.get_conversational_error(
            error, context=context
        )
        return IntentProcessingResult(
            success=False,
            message=conversational_message,
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": getattr(intent, "confidence", 0.0),
            },
            workflow_id=workflow_id,
            error=str(error),
            error_type=error_type,
        )
