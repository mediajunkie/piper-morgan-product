"""
Adapters for existing process managers to implement GuidedProcess protocol.

These adapters wrap the existing PortfolioOnboardingManager and
StandupConversationManager to work with the ProcessRegistry.

ADR-049: Two-Tier Intent Architecture
Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
Issue #888: Escape commands, timeout, suspend/resume
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import structlog

from services.process.registry import GuidedProcess, ProcessCheckResult, ProcessType, SuspendedInfo
from services.shared_types import IntentCategory
from services.utils.datetime_utils import ensure_utc

logger = structlog.get_logger(__name__)

# Issue #888: Timeout durations per PPM binding direction (2026-03-13)
ONBOARDING_TIMEOUT_MINUTES = 30
STANDUP_TIMEOUT_MINUTES = 15


class OnboardingProcessAdapter:
    """
    Adapter wrapping PortfolioOnboardingManager for ProcessRegistry.

    Implements GuidedProcess protocol by delegating to the existing
    singleton manager and handler.
    """

    def __init__(self):
        self._manager = None
        self._handler = None

    def _get_components(self):
        """Lazy-load components to avoid circular imports."""
        if self._manager is None:
            from services.conversation.conversation_handler import _get_onboarding_components

            self._manager, self._handler = _get_onboarding_components()
        return self._manager, self._handler

    @property
    def process_type(self) -> ProcessType:
        return ProcessType.ONBOARDING

    def _get_session(self, user_id: Optional[str], session_id: Optional[str]):
        """Look up an onboarding session by user_id or session_id."""
        manager, _ = self._get_components()

        session = None
        if user_id:
            session = manager.get_session_by_user(user_id)
        if not session and session_id:
            session = manager.get_session_by_session_id(session_id)
        return session

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """
        Check if there's an active onboarding session.

        Issue #888: Arch guidance — enumerate non-active states explicitly.
        OFFERED and SUSPENDED are NOT active (registry should not route to them).
        Also checks timeout: sessions inactive > 30min auto-suspend.
        """
        from services.shared_types import PortfolioOnboardingState

        session = self._get_session(user_id, session_id)

        if not session:
            return False

        # Issue #888: Enumerate non-active states explicitly per Arch guidance.
        # Don't rely on "not terminal" — be explicit about what IS active.
        NON_ACTIVE_STATES = (
            PortfolioOnboardingState.COMPLETE,
            PortfolioOnboardingState.DECLINED,
            PortfolioOnboardingState.OFFERED,
            PortfolioOnboardingState.SUSPENDED,
        )
        if session.state in NON_ACTIVE_STATES:
            return False

        # Issue #888: Timeout auto-suspend — onboarding 30min per PPM direction
        if (
            hasattr(session, "updated_at")
            and session.updated_at
            and isinstance(session.updated_at, datetime)
        ):
            # #1079: updated_at is tz-aware (UTC) from the DB; use tz-aware now
            elapsed = datetime.now(timezone.utc) - session.updated_at
            if elapsed > timedelta(minutes=ONBOARDING_TIMEOUT_MINUTES):
                logger.info(
                    "Onboarding session timed out, auto-suspending",
                    session_id=session.id,
                    user_id=user_id,
                    elapsed_minutes=elapsed.total_seconds() / 60,
                )
                manager, _ = self._get_components()
                try:
                    manager.transition_state(session.id, PortfolioOnboardingState.SUSPENDED)
                except Exception as e:
                    logger.warning(
                        "Error auto-suspending timed-out onboarding",
                        error=str(e),
                    )
                return False

        return True

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """Handle a message in active onboarding session."""
        manager, handler = self._get_components()

        session = self._get_session(user_id, session_id)
        if not session:
            return ProcessCheckResult.not_handled()

        # Handle the turn
        response = handler.handle_turn(session.id, message)

        # Issue #728: Include captured_projects in context for persistence
        # IntentService._check_active_guided_process() looks for this
        # to persist projects when onboarding completes
        context = {
            "onboarding_id": session.id,
            "state": response.state.value,
            "bypassed_classification": True,
            "guided_process": ProcessType.ONBOARDING.value,
        }

        # Add captured_projects when onboarding completes
        if response.is_complete and response.captured_projects:
            context["captured_projects"] = response.captured_projects

        intent_data = {
            "category": IntentCategory.GUIDANCE.value,
            "action": "portfolio_onboarding",
            "confidence": 1.0,
            "context": context,
        }

        return ProcessCheckResult.handled_by(
            process_type=ProcessType.ONBOARDING,
            response_message=response.message,
            intent_data=intent_data,
        )

    async def suspend(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Suspend the active onboarding session.

        Issue #888: Transitions session to SUSPENDED state, preserving
        all captured project data for later resumption.
        """
        from services.shared_types import PortfolioOnboardingState

        session = self._get_session(user_id, session_id)
        if not session:
            logger.warning(
                "Cannot suspend onboarding — no session found",
                user_id=user_id,
                session_id=session_id,
            )
            return

        manager, _ = self._get_components()
        try:
            manager.transition_state(session.id, PortfolioOnboardingState.SUSPENDED)
            logger.info(
                "Onboarding session suspended",
                session_id=session.id,
                user_id=user_id,
                previous_state=session.previous_state.value if session.previous_state else None,
            )
        except Exception as e:
            logger.warning(
                "Error suspending onboarding session",
                session_id=session.id,
                error=str(e),
            )

    async def close(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Close the active onboarding session for good (#1529).

        Exit/refusal semantics: transition to DECLINED (terminal) so the
        flow doesn't re-offer itself. Distinct from suspend(), which
        preserves state for resumption.
        """
        from services.shared_types import PortfolioOnboardingState

        session = self._get_session(user_id, session_id)
        if not session:
            logger.warning(
                "Cannot close onboarding — no session found",
                user_id=user_id,
                session_id=session_id,
            )
            return

        manager, _ = self._get_components()
        try:
            manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)
            logger.info(
                "Onboarding session closed (escape exit/refusal)",
                session_id=session.id,
                user_id=user_id,
            )
        except Exception as e:
            logger.warning(
                "Error closing onboarding session",
                session_id=session.id,
                error=str(e),
            )

    async def has_suspended_session(
        self,
        user_id: Optional[str],
    ) -> Optional[SuspendedInfo]:
        """
        Check if this user has a suspended onboarding session.

        Issue #888: Arch guidance — handler checks its own state machine.
        Returns SuspendedInfo if found, None otherwise.
        """
        from services.shared_types import PortfolioOnboardingState

        if not user_id:
            return None

        manager, _ = self._get_components()
        session = manager.get_session_by_user(user_id)

        if not session:
            return None

        if session.state == PortfolioOnboardingState.SUSPENDED:
            return SuspendedInfo(
                process_type=ProcessType.ONBOARDING,
                suspended_at=session.updated_at if hasattr(session, "updated_at") else None,
                description="Portfolio onboarding was paused. You can pick it up anytime.",
            )

        return None


class StandupProcessAdapter:
    """
    Adapter wrapping StandupConversationManager for ProcessRegistry.

    Implements GuidedProcess protocol by delegating to the existing
    singleton manager and handler.

    Issue #888: Added suspend(), has_suspended_session(), timeout.
    """

    def __init__(self):
        self._manager = None
        self._handler = None

    def _get_components(self):
        """Lazy-load components to avoid circular imports."""
        if self._manager is None:
            from services.conversation.conversation_handler import _get_standup_components

            self._manager, self._handler = _get_standup_components()
        return self._manager, self._handler

    async def _get_conversation(self, user_id: Optional[str], session_id: Optional[str]):
        """Look up a standup conversation by session_id (primary) or user_id."""
        manager, _ = self._get_components()

        conversation = None
        if session_id:
            conversation = await manager.get_conversation_by_session(session_id)
        return conversation

    @property
    def process_type(self) -> ProcessType:
        return ProcessType.STANDUP

    async def check_active(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """
        Check if there's an active standup conversation.

        Issue #888: Enumerate non-active states explicitly. SUSPENDED is not active.
        Also checks timeout: sessions inactive > 15min auto-suspend — but ONLY in
        the completion tail since #1623 (see below).

        #1623 (PM live 2026-08-15, mid-gathering theft): the timeout here is
        evaluated LAZILY — there is no background reaper, so it fires INSIDE the
        processing of the user's next turn. Mid-gathering, that next turn is by
        construction the ANSWER to the flow's open question ("What's planned for
        today?" → PM's plans answer). The old unconditional timeout silently
        auto-suspended the flow and let that answer fall through to the LLM
        classifier, where an unrelated surface claimed it (PM's plans answer ate
        a files-family canned denial; the blockers answer got the temporal
        surface). Measured: every content-dependent surface above the process
        claim passes these turns; this lazy ejection was the only thief.

        The rule now: a MID-GATHERING flow (open question pending) HOLDS its
        turns regardless of think-time — the user leaves via the #888/#1529
        escape tiers or #899 off-topic, which run every turn and are the
        deliberate exceptions. The timeout auto-suspend applies only in the
        completion tail (REFINING/FINALIZING), where the work is delivered and
        going idle should stop claiming the session (#1617 releases off-tail
        turns there anyway). Trade-off, flagged for review: a mid-gathering flow
        abandoned in a still-open session no longer times out — its turns are
        claimable until an escape/off-topic tier fires. Scoping limits the blast
        radius: the conversation is keyed to its session, so a fresh session
        never meets the stale flow.
        """
        from services.shared_types import StandupConversationState

        conversation = await self._get_conversation(user_id, session_id)

        if not conversation:
            return False

        # Issue #888: Enumerate non-active states explicitly per Arch guidance
        NON_ACTIVE_STATES = (
            StandupConversationState.COMPLETE,
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,
        )
        if conversation.state in NON_ACTIVE_STATES:
            return False

        # Issue #888 timeout auto-suspend, #1623-gated to the completion tail:
        # mid-gathering, an elapsed clock must never eject the in-flight answer.
        in_tail = conversation.state in (
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,
        )
        if (
            in_tail
            and hasattr(conversation, "updated_at")
            and conversation.updated_at
            and isinstance(conversation.updated_at, datetime)
        ):
            # #1079: updated_at is tz-aware (UTC) from the DB; use tz-aware now.
            # ensure_utc coerces a tz-naive updated_at (e.g. an in-memory
            # conversation not yet round-tripped through the timestamptz column)
            # so the subtraction never raises naive-vs-aware TypeError.
            elapsed = datetime.now(timezone.utc) - ensure_utc(conversation.updated_at)
            if elapsed > timedelta(minutes=STANDUP_TIMEOUT_MINUTES):
                logger.info(
                    "Standup conversation timed out, auto-suspending",
                    conversation_id=conversation.id,
                    user_id=user_id,
                    elapsed_minutes=elapsed.total_seconds() / 60,
                )
                manager, _ = self._get_components()
                try:
                    await manager.transition_state(
                        conversation.id, StandupConversationState.SUSPENDED
                    )
                except Exception as e:
                    logger.warning(
                        "Error auto-suspending timed-out standup",
                        error=str(e),
                    )
                return False

        return True

    async def handle_message(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
        message: str,
    ) -> ProcessCheckResult:
        """Handle a message in active standup conversation."""
        manager, handler = self._get_components()

        conversation = await self._get_conversation(user_id, session_id)
        if not conversation:
            return ProcessCheckResult.not_handled()

        # Handle the turn (standup handler is async)
        response = await handler.handle_turn(conversation, message)

        intent_data = {
            "category": IntentCategory.EXECUTION.value,
            "action": "standup_conversation_turn",
            "confidence": 1.0,
            "context": {
                "conversation_id": conversation.id,
                "state": response.state.value,
                "bypassed_classification": True,
                "guided_process": ProcessType.STANDUP.value,
            },
        }

        return ProcessCheckResult.handled_by(
            process_type=ProcessType.STANDUP,
            response_message=response.message,
            intent_data=intent_data,
        )

    async def suspend(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Suspend the active standup conversation.

        Issue #888: Transitions conversation to SUSPENDED state, preserving
        partial standup content for later resumption.
        """
        from services.shared_types import StandupConversationState

        conversation = await self._get_conversation(user_id, session_id)
        if not conversation:
            logger.warning(
                "Cannot suspend standup — no conversation found",
                user_id=user_id,
                session_id=session_id,
            )
            return

        manager, _ = self._get_components()
        try:
            await manager.transition_state(conversation.id, StandupConversationState.SUSPENDED)
            logger.info(
                "Standup conversation suspended",
                conversation_id=conversation.id,
                user_id=user_id,
                previous_state=(
                    conversation.previous_state.value if conversation.previous_state else None
                ),
            )
        except Exception as e:
            logger.warning(
                "Error suspending standup conversation",
                conversation_id=conversation.id,
                error=str(e),
            )

    async def in_completion_tail(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> bool:
        """#1617: True when the conversation is in a post-summary tail state —
        the standup content has been rendered and delivered (REFINING is
        entered exactly when the summary renders; FINALIZING is the legacy
        'share or save?' tail). An off-tail turn here can only be a command
        the user wants answered, never interview material."""
        from services.shared_types import StandupConversationState

        conversation = await self._get_conversation(user_id, session_id)
        if not conversation:
            return False
        return conversation.state in (
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,
        )

    async def release(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """#1617: end a DELIVERED standup for good — completion-tail release.

        The summary was rendered and stands; the honest terminal state is
        COMPLETE (the work happened — distinct from close()'s ABANDONED for
        exits/refusals). Falls back to ABANDONED if the COMPLETE transition
        is invalid from the current state. Both are terminal: no further
        claiming, no resume re-offer.
        """
        from services.shared_types import StandupConversationState

        conversation = await self._get_conversation(user_id, session_id)
        if not conversation:
            logger.warning(
                "Cannot release standup — no conversation found",
                user_id=user_id,
                session_id=session_id,
            )
            return

        manager, _ = self._get_components()
        try:
            await manager.transition_state(conversation.id, StandupConversationState.COMPLETE)
            logger.info(
                "Standup conversation released (completion-tail, #1617)",
                conversation_id=conversation.id,
                user_id=user_id,
            )
        except Exception:
            try:
                await manager.transition_state(conversation.id, StandupConversationState.ABANDONED)
            except Exception as e:
                logger.warning(
                    "Error releasing standup conversation",
                    conversation_id=conversation.id,
                    error=str(e),
                )

    async def close(
        self,
        user_id: Optional[str],
        session_id: Optional[str],
    ) -> None:
        """
        Close the active standup conversation for good (#1529).

        Exit/refusal semantics: transition to ABANDONED, a terminal state,
        so the flow neither claims further turns nor re-offers itself at the
        next greeting (the resume-nag loop). Distinct from suspend(), which
        preserves the conversation for resumption.
        """
        from services.shared_types import StandupConversationState

        conversation = await self._get_conversation(user_id, session_id)
        if not conversation:
            logger.warning(
                "Cannot close standup — no conversation found",
                user_id=user_id,
                session_id=session_id,
            )
            return

        manager, _ = self._get_components()
        try:
            await manager.transition_state(conversation.id, StandupConversationState.ABANDONED)
            logger.info(
                "Standup conversation closed (escape exit/refusal)",
                conversation_id=conversation.id,
                user_id=user_id,
            )
        except Exception as e:
            logger.warning(
                "Error closing standup conversation",
                conversation_id=conversation.id,
                error=str(e),
            )

    async def has_suspended_session(
        self,
        user_id: Optional[str],
    ) -> Optional[SuspendedInfo]:
        """
        Check if this user has a suspended standup conversation.

        Issue #888: Surface resume offers when a user has a paused standup.

        Issue #1052 Phase 2: Queries the durable repository via the manager
        rather than iterating an in-memory dict.
        """
        if not user_id:
            return None

        manager, _ = self._get_components()
        suspended = await manager.get_suspended_for_user(user_id)
        if suspended is None:
            return None

        return SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=(suspended.updated_at if hasattr(suspended, "updated_at") else None),
            description="Your standup was paused. Want to pick it up?",
        )


def register_default_processes() -> None:
    """
    Register the default guided process adapters.

    Called during application startup to register onboarding and
    standup processes with the registry.
    """
    from services.process.registry import get_process_registry

    registry = get_process_registry()

    # Register adapters for existing process managers
    # ADR-059: Onboarding disabled — put on ice until workflow dispatcher is in place
    # registry.register(OnboardingProcessAdapter())
    registry.register(StandupProcessAdapter())

    logger.info(
        "Registered default guided processes",
        types=[t.value for t in registry.registered_types],
    )
