"""
Process Registry for Guided Processes.

ADR-049: Two-Tier Intent Architecture

A Guided Process is a multi-turn conversation where Piper maintains control
until completion or exit. Examples: onboarding, standup, planning, feedback.

The Process Registry tracks active guided processes per session and checks
them BEFORE intent classification to prevent derailment.

Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
Issue #687: ADR-049 Implementation
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, runtime_checkable

import structlog

logger = structlog.get_logger(__name__)


# Issue #888, #889: Escape commands recognized at registry level.
# PPM binding direction (2026-03-13): These bypass workflow handlers entirely.
# Arch guidance: Exact match on stripped+lowercased full message. Use frozenset.
ESCAPE_COMMANDS: frozenset = frozenset(
    {
        "cancel",
        "exit",
        "stop",
        "skip",
        "quit",
        "never mind",
    }
)


class ProcessType(str, Enum):
    """
    Types of guided processes.

    Current (MVP):
    - ONBOARDING: Portfolio setup for new users
    - STANDUP: Interactive standup creation
    - SLOT_FILLING: Natural multi-turn slot collection (#765)

    Future (Advanced Layer):
    - PLANNING: Structured planning sessions
    - FEEDBACK: User feedback collection
    - CLARIFICATION: Pending question resolution
    """

    ONBOARDING = "onboarding"
    STANDUP = "standup"
    SLOT_FILLING = "slot_filling"  # Issue #765 GLUE-SLOTFILL
    # Future types (Advanced Layer - see #698, #699, #700)
    PLANNING = "planning"
    FEEDBACK = "feedback"
    CLARIFICATION = "clarification"


@dataclass
class SuspendedInfo:
    """
    Lightweight info about a suspended workflow session.

    Issue #888: Arch guidance — registry discovers suspended sessions
    via has_suspended_session(), handlers own the semantics.
    """

    process_type: ProcessType
    suspended_at: Optional[datetime] = None
    description: str = ""


@dataclass
class ProcessCheckResult:
    """
    Result of checking for an active guided process.

    If handled is True, the message was handled by a guided process
    and classification should be bypassed.
    """

    handled: bool
    process_type: Optional[ProcessType] = None
    response_message: Optional[str] = None
    intent_data: Optional[Dict[str, Any]] = None
    escaped: bool = False  # True when user used an escape command

    @classmethod
    def not_handled(cls) -> "ProcessCheckResult":
        """No active process claimed the message."""
        return cls(handled=False)

    @classmethod
    def handled_by(
        cls,
        process_type: ProcessType,
        response_message: str,
        intent_data: Dict[str, Any],
    ) -> "ProcessCheckResult":
        """Message was handled by a guided process."""
        return cls(
            handled=True,
            process_type=process_type,
            response_message=response_message,
            intent_data=intent_data,
        )

    @classmethod
    def off_topic_pause(
        cls,
        process_type: ProcessType,
        pause_message: str,
    ) -> "ProcessCheckResult":
        """
        Process was paused because user sent an off-topic message.

        Issue #899: Layer C escape. Unlike escaped_from(), this returns
        handled=False so normal intent processing can answer the user's
        actual question. The pause_message is prepended by IntentService.
        """
        return cls(
            handled=False,  # Let intent processing handle the actual question
            escaped=True,
            process_type=process_type,
            response_message=pause_message,
            intent_data={
                "category": "guidance",
                "action": "off_topic_pause",
                "confidence": 1.0,
                "context": {
                    "paused_process": process_type.value,
                    "bypassed_classification": False,  # Intent processing continues
                    "off_topic_detected": True,
                },
            },
        )

    @classmethod
    def escaped_from(
        cls,
        process_type: ProcessType,
        response_message: str,
    ) -> "ProcessCheckResult":
        """User escaped from an active guided process via escape command."""
        return cls(
            handled=True,
            escaped=True,
            process_type=process_type,
            response_message=response_message,
            intent_data={
                "category": "guidance",
                "action": "workflow_escaped",
                "confidence": 1.0,
                "context": {
                    "escaped_process": process_type.value,
                    "bypassed_classification": True,
                },
            },
        )


@runtime_checkable
class GuidedProcess(Protocol):
    """
    Protocol for guided process handlers.

    Each guided process type implements this protocol to integrate
    with the process registry.

    Issue #888: Added suspend() and has_suspended_session() per
    PPM direction and Arch guidance (2026-03-13).
    """

    @property
    def process_type(self) -> ProcessType:
        """The type of this guided process."""
        ...

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """
        Check if there's an active session for this user/session.

        Returns True if an active (non-terminal) session exists.
        """
        ...

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """
        Handle a message in the context of an active session.

        Only called if check_active returned True.
        Returns ProcessCheckResult with handled=True and response.
        """
        ...

    async def suspend(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Suspend the active session, preserving state for later resumption.

        Issue #888: Called by ProcessRegistry when user issues an escape
        command. Transitions session to SUSPENDED state. Handler owns
        the semantics of what "suspended" means for its workflow.
        """
        ...

    async def has_suspended_session(
        self,
        user_id: Optional[str],
    ) -> Optional[SuspendedInfo]:
        """
        Check if this user has a suspended session.

        Issue #888: Arch guidance — registry discovers suspended sessions
        by iterating handlers. Each handler checks its own state machine.

        Returns SuspendedInfo if a suspended session exists, None otherwise.
        """
        ...


class ProcessRegistry:
    """
    Registry of guided process handlers.

    Maintains the list of registered processes and checks them in
    priority order when processing a message.

    Design principle: Check processes in a defined priority order.
    First match wins. If no process claims the message, proceed
    with normal intent classification.
    """

    # Singleton instance
    _instance: Optional["ProcessRegistry"] = None

    def __init__(self):
        # Process handlers in priority order
        self._handlers: List[GuidedProcess] = []
        # Priority order for checking (lower = higher priority)
        self._priority_order: Dict[ProcessType, int] = {
            ProcessType.ONBOARDING: 10,  # Highest priority
            ProcessType.STANDUP: 20,
            ProcessType.SLOT_FILLING: 25,  # Issue #765 — after standup, before clarification
            ProcessType.CLARIFICATION: 30,
            ProcessType.PLANNING: 40,
            ProcessType.FEEDBACK: 50,
        }
        logger.info("ProcessRegistry initialized")

    @classmethod
    def get_instance(cls) -> "ProcessRegistry":
        """Get singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset singleton (for testing)."""
        cls._instance = None

    def register(self, handler: GuidedProcess) -> None:
        """
        Register a guided process handler.

        Handlers are automatically sorted by priority order.
        """
        if not isinstance(handler, GuidedProcess):
            raise TypeError(f"Handler must implement GuidedProcess protocol: {handler}")

        # Check for duplicate registration
        for existing in self._handlers:
            if existing.process_type == handler.process_type:
                logger.warning(
                    "Replacing existing handler for process type",
                    process_type=handler.process_type.value,
                )
                self._handlers.remove(existing)
                break

        self._handlers.append(handler)

        # Sort by priority
        self._handlers.sort(key=lambda h: self._priority_order.get(h.process_type, 100))

        logger.info(
            "Registered guided process handler",
            process_type=handler.process_type.value,
            priority=self._priority_order.get(handler.process_type, 100),
        )

    def unregister(self, process_type: ProcessType) -> bool:
        """
        Unregister a handler by process type.

        Returns True if a handler was removed.
        """
        for handler in self._handlers:
            if handler.process_type == process_type:
                self._handlers.remove(handler)
                logger.info(
                    "Unregistered guided process handler",
                    process_type=process_type.value,
                )
                return True
        return False

    def _check_off_topic(self, message: str, process_type: ProcessType):
        """
        Check if a message is off-topic for the active process.

        Issue #899: Layer C escape — conservative off-topic detection.
        Returns OffTopicResult if detection ran, None if module unavailable.
        """
        try:
            from services.process.off_topic import OffTopicResult, detect_off_topic

            return detect_off_topic(message, process_type)
        except Exception as e:
            logger.warning(
                "Off-topic detection failed, allowing message through",
                error=str(e),
            )
            return None

    def _is_escape_command(self, message: str) -> bool:
        """
        Check if a message is an escape command.

        Issue #888: PPM binding direction — exact match on stripped+lowercased
        full message. No regex, no substring. "cancel" escapes, but
        "cancel my standup" does NOT.

        Arch guidance (2026-03-13): Use frozenset for O(1) lookup.
        """
        normalized = message.strip().lower()
        return normalized in ESCAPE_COMMANDS

    async def _close_process(
        self,
        handler: GuidedProcess,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """Close a flow for good (exit/refusal — #1529).

        Prefers the handler's `close()` (terminal state: no resume re-offer,
        which is the nag loop #1529 documents) and falls back to `suspend()`
        for handlers that don't implement it. Duck-typed on purpose so the
        GuidedProcess protocol doesn't force a migration.
        """
        closer = getattr(handler, "close", None)
        try:
            if closer is not None:
                await closer(user_id, session_id)
            else:
                await handler.suspend(user_id, session_id)
        except Exception as close_err:
            logger.warning(
                "Error closing process after escape",
                process_type=handler.process_type.value,
                error=str(close_err),
            )

    async def _handle_escape_signal(
        self,
        handler: GuidedProcess,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> Optional[ProcessCheckResult]:
        """Issue #1529: universal escape check for an active guided flow.

        Runs the flow-generic escape detection (exit / refusal / off-intent)
        and, when a signal fires, closes or pauses the flow and returns the
        appropriate ProcessCheckResult. Returns None when the message should
        proceed to the flow's handler. Detection failures never trap the user
        IN the flow silently — they log and return None (the pre-existing
        #888 exact-match escape above remains the guaranteed hatch).
        """
        try:
            from services.process.escape import (
                check_escape,
                format_exit_message,
                format_refusal_prefix,
            )

            signal = check_escape(message, handler.process_type)
        except Exception as e:
            logger.warning(
                "Escape check failed, message proceeds to flow handler",
                process_type=handler.process_type.value,
                error=str(e),
            )
            return None

        if signal is None:
            return None

        logger.info(
            "Guided-process escape detected",
            process_type=handler.process_type.value,
            kind=signal.kind,
            matched=signal.matched[:80],
            has_residual=signal.residual is not None,
            user_id=user_id,
            session_id=session_id,
        )

        if signal.kind == "exit":
            await self._close_process(handler, user_id, session_id)
            return ProcessCheckResult.escaped_from(
                process_type=handler.process_type,
                response_message=format_exit_message(handler.process_type),
            )

        if signal.kind == "refusal":
            await self._close_process(handler, user_id, session_id)
            if signal.residual:
                # Refusal + an actual request ("… restore CoVa"): exit the
                # flow and let normal intent processing answer the request,
                # with the honest exit copy prepended (off_topic_pause shape).
                return ProcessCheckResult.off_topic_pause(
                    process_type=handler.process_type,
                    pause_message=format_refusal_prefix(handler.process_type),
                )
            return ProcessCheckResult.escaped_from(
                process_type=handler.process_type,
                response_message=format_exit_message(handler.process_type),
            )

        # off_intent — Option A UX (#899): pause (resumable) + answer.
        try:
            await handler.suspend(user_id, session_id)
        except Exception as suspend_err:
            logger.warning(
                "Error suspending process after off-intent escape",
                process_type=handler.process_type.value,
                error=str(suspend_err),
            )
        from services.process.off_topic import format_off_topic_pause_message

        return ProcessCheckResult.off_topic_pause(
            process_type=handler.process_type,
            pause_message=format_off_topic_pause_message(handler.process_type),
        )

    async def check_suspended_processes(
        self,
        user_id: Optional[str],
    ) -> Optional[SuspendedInfo]:
        """
        Check all handlers for a suspended session belonging to user_id.

        Issue #888: Arch guidance — registry is a "dumb aggregator."
        Iterates handlers, each checks its own state machine. First
        suspended session found wins (priority order).

        Returns SuspendedInfo if a suspended session exists, None otherwise.
        """
        if not user_id:
            return None

        for handler in self._handlers:
            try:
                suspended = await handler.has_suspended_session(user_id)
                if suspended is not None:
                    logger.info(
                        "Found suspended session",
                        process_type=suspended.process_type.value,
                        user_id=user_id,
                    )
                    return suspended
            except Exception as e:
                logger.warning(
                    "Error checking suspended session",
                    process_type=handler.process_type.value,
                    error=str(e),
                )
                continue

        return None

    async def check_active_processes(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """
        Check all registered processes for an active session.

        Issue #888: Escape commands are checked BEFORE routing to handler.
        PPM binding direction: "recognized by the ProcessRegistry directly,
        not passed to the workflow handler for interpretation."

        Checks in priority order. First process that has an active
        session and can handle the message wins.

        Args:
            user_id: Authenticated user ID (may be None)
            session_id: Session identifier
            message: User's message

        Returns:
            ProcessCheckResult - handled=True if a process claimed the message
        """
        for handler in self._handlers:
            try:
                # First check if there's an active session
                is_active = await handler.check_active(user_id, session_id)

                if is_active:
                    logger.debug(
                        "Found active guided process",
                        process_type=handler.process_type.value,
                        user_id=user_id,
                        session_id=session_id,
                    )

                    # Issue #888: Check for escape commands BEFORE routing to handler.
                    # This is the guaranteed escape hatch — no handler can break it.
                    if self._is_escape_command(message):
                        logger.info(
                            "Escape command intercepted by registry",
                            process_type=handler.process_type.value,
                            escape_command=message.strip().lower(),
                            user_id=user_id,
                            session_id=session_id,
                        )
                        # Suspend the session (handler owns semantics)
                        try:
                            await handler.suspend(user_id, session_id)
                        except Exception as suspend_err:
                            logger.warning(
                                "Error suspending process after escape",
                                process_type=handler.process_type.value,
                                error=str(suspend_err),
                            )
                        return ProcessCheckResult.escaped_from(
                            process_type=handler.process_type,
                            response_message=(
                                f"No problem — I've paused {handler.process_type.value}. "
                                "We can pick it up anytime."
                            ),
                        )

                    # Issue #1529: universal escape check (FLOW-ESCAPE) — exits,
                    # refusals, and cross-domain actions are consumed HERE,
                    # deterministically, before the flow can transcribe them and
                    # before any classifier sees them.
                    escape_result = await self._handle_escape_signal(
                        handler, user_id, session_id, message
                    )
                    if escape_result is not None:
                        return escape_result

                    # Issue #899: Layer C — off-topic detection.
                    # Check if the message is clearly unrelated to the active process.
                    # Conservative: only clear non-sequiturs trigger auto-pause.
                    off_topic_result = self._check_off_topic(message, handler.process_type)
                    if off_topic_result is not None and off_topic_result.is_off_topic:
                        logger.info(
                            "Off-topic message detected during guided process",
                            process_type=handler.process_type.value,
                            pattern=off_topic_result.matched_pattern,
                            user_id=user_id,
                            session_id=session_id,
                        )
                        # Option A UX: auto-pause + let normal intent processing answer
                        try:
                            await handler.suspend(user_id, session_id)
                        except Exception as suspend_err:
                            logger.warning(
                                "Error suspending process after off-topic detection",
                                process_type=handler.process_type.value,
                                error=str(suspend_err),
                            )

                        from services.process.off_topic import format_off_topic_pause_message

                        pause_msg = format_off_topic_pause_message(handler.process_type)
                        return ProcessCheckResult.off_topic_pause(
                            process_type=handler.process_type,
                            pause_message=pause_msg,
                        )

                    # Let the handler process the message
                    result = await handler.handle_message(user_id, session_id, message)

                    if result.handled:
                        logger.info(
                            "Message handled by guided process",
                            process_type=handler.process_type.value,
                            user_id=user_id,
                            session_id=session_id,
                        )
                        return result

            except Exception as e:
                logger.warning(
                    "Error checking guided process",
                    process_type=handler.process_type.value,
                    error=str(e),
                )
                # Continue to next handler
                continue

        return ProcessCheckResult.not_handled()

    @property
    def registered_types(self) -> List[ProcessType]:
        """List of currently registered process types."""
        return [h.process_type for h in self._handlers]


# Convenience function for getting the singleton
def get_process_registry() -> ProcessRegistry:
    """Get the singleton process registry instance."""
    return ProcessRegistry.get_instance()
