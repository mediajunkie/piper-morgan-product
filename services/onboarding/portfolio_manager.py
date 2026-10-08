"""
Issue #490: Portfolio onboarding state management service.

Epic: FTUX (First Time User Experience)

Provides state machine management for portfolio onboarding conversations,
following the pattern established by StandupConversationManager (Epic #242).

Simpler than standup - focused on project capture in a few turns.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import ConversationTurn, PortfolioOnboardingSession
from services.shared_types import PortfolioOnboardingState

logger = structlog.get_logger()


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    pass


class PortfolioOnboardingManager:
    """
    Issue #490: Manages portfolio onboarding conversation state and transitions.

    Provides:
    - Session lifecycle (create, get, complete)
    - State machine validation
    - Turn recording
    - Project capture storage
    - Session-scoped persistence (in-memory initially)

    Follows StandupConversationManager pattern from Epic #242.
    """

    # Memory optimization - limit turn history
    MAX_TURN_HISTORY = 20  # Onboarding typically completes in 3-5 turns

    # Valid state transitions - defines the state machine
    # Issue #888: Added OFFERED (pre-activation) and SUSPENDED (escape/timeout) states
    VALID_TRANSITIONS: Dict[PortfolioOnboardingState, List[PortfolioOnboardingState]] = {
        PortfolioOnboardingState.OFFERED: [
            PortfolioOnboardingState.INITIATED,  # User accepted the offer
            PortfolioOnboardingState.DECLINED,  # User said no thanks
        ],
        PortfolioOnboardingState.INITIATED: [
            PortfolioOnboardingState.OFFERED,  # Issue #888: the greeting offer flow transitioned here immediately
            PortfolioOnboardingState.GATHERING_PROJECTS,  # User said yes
            PortfolioOnboardingState.DECLINED,  # User said no thanks
            PortfolioOnboardingState.SUSPENDED,  # Escape command or timeout
        ],
        PortfolioOnboardingState.GATHERING_PROJECTS: [
            PortfolioOnboardingState.GATHERING_PROJECTS,  # More projects to add
            PortfolioOnboardingState.CONFIRMING,  # User done adding projects
            PortfolioOnboardingState.DECLINED,  # User changed mind
            PortfolioOnboardingState.SUSPENDED,  # Escape command or timeout
        ],
        PortfolioOnboardingState.CONFIRMING: [
            PortfolioOnboardingState.GATHERING_PROJECTS,  # User wants to add more
            PortfolioOnboardingState.GATHERING_REPOS,  # Proceed to repo linking (#863)
            PortfolioOnboardingState.COMPLETE,  # User confirmed, save projects
            PortfolioOnboardingState.DECLINED,  # User cancelled
            PortfolioOnboardingState.SUSPENDED,  # Escape command or timeout
        ],
        PortfolioOnboardingState.GATHERING_REPOS: [
            PortfolioOnboardingState.GATHERING_REPOS,  # Next project's repo
            PortfolioOnboardingState.COMPLETE,  # All done / skip all
            PortfolioOnboardingState.SUSPENDED,  # Escape command or timeout
        ],
        PortfolioOnboardingState.SUSPENDED: [
            PortfolioOnboardingState.INITIATED,  # User accepted resume offer
            PortfolioOnboardingState.DECLINED,  # User declined to resume
        ],
        PortfolioOnboardingState.COMPLETE: [],  # Terminal state
        PortfolioOnboardingState.DECLINED: [],  # Terminal state
    }

    def __init__(self) -> None:
        """Initialize with in-memory session storage."""
        self._sessions: Dict[str, PortfolioOnboardingSession] = {}

    def create_session(
        self,
        session_id: str,
        user_id: str,
    ) -> PortfolioOnboardingSession:
        """
        Create a new portfolio onboarding session.

        Args:
            session_id: Session identifier
            user_id: User identifier (required for multi-tenancy isolation)

        Returns:
            New PortfolioOnboardingSession instance

        Raises:
            ValueError: If user_id is None or empty
        """
        # Issue #734: Validate user_id for multi-tenancy isolation
        if not user_id:
            raise ValueError("user_id is required for multi-tenancy isolation")

        session = PortfolioOnboardingSession(
            session_id=session_id,
            user_id=user_id,
        )

        self._sessions[session.id] = session

        # Issue #490 INVESTIGATION: Trace session creation
        print(
            f"[PortfolioManager] Session CREATED: id={session.id}, user_id={user_id}, session_id={session_id}"
        )
        print(f"[PortfolioManager] Manager id={id(self)}, total sessions={len(self._sessions)}")

        logger.info(
            "portfolio_onboarding_session_created",
            onboarding_id=session.id,
            session_id=session_id,
            user_id=user_id,
        )

        return session

    def get_session(self, onboarding_id: str) -> Optional[PortfolioOnboardingSession]:
        """Retrieve a session by ID."""
        return self._sessions.get(onboarding_id)

    def get_session_by_user(self, user_id: str) -> Optional[PortfolioOnboardingSession]:
        """
        Retrieve active onboarding session for a user.

        Returns the most recent non-terminal session for the user.
        """
        # Issue #490 INVESTIGATION: Trace lookup with manager ID for singleton verification
        print(
            f"[PortfolioManager] get_session_by_user called, manager id={id(self)}, user_id={user_id}"
        )
        print(
            f"[PortfolioManager] Current sessions: {[(s.id, s.user_id, s.state.value) for s in self._sessions.values()]}"
        )

        for session in reversed(list(self._sessions.values())):
            if session.user_id == user_id and session.state not in [
                PortfolioOnboardingState.COMPLETE,
                PortfolioOnboardingState.DECLINED,
            ]:
                print(f"[PortfolioManager] Found session {session.id} for user {user_id}")
                return session
        print(f"[PortfolioManager] No active session found for user {user_id}")
        return None

    def get_session_by_session_id(self, session_id: str) -> Optional[PortfolioOnboardingSession]:
        """
        Retrieve active onboarding session by HTTP session ID.

        Issue #490: Fallback lookup when user_id is not available.
        Returns the most recent non-terminal session for the session_id.
        """
        for session in reversed(list(self._sessions.values())):
            if session.session_id == session_id and session.state not in [
                PortfolioOnboardingState.COMPLETE,
                PortfolioOnboardingState.DECLINED,
            ]:
                return session
        return None

    def transition_state(
        self,
        onboarding_id: str,
        new_state: PortfolioOnboardingState,
    ) -> PortfolioOnboardingSession:
        """
        Transition session to a new state.

        Args:
            onboarding_id: Session to transition
            new_state: Target state

        Returns:
            Updated session

        Raises:
            InvalidStateTransitionError: If transition is not valid
            KeyError: If session not found
        """
        session = self._sessions.get(onboarding_id)
        if not session:
            raise KeyError(f"Onboarding session not found: {onboarding_id}")

        current_state = session.state
        valid_targets = self.VALID_TRANSITIONS.get(current_state, [])

        if new_state not in valid_targets:
            raise InvalidStateTransitionError(
                f"Cannot transition from {current_state.value} to {new_state.value}. "
                f"Valid transitions: {[s.value for s in valid_targets]}"
            )

        session.previous_state = current_state
        session.state = new_state
        session.updated_at = datetime.now()

        if new_state == PortfolioOnboardingState.COMPLETE:
            session.completed_at = datetime.now()
            duration_seconds = (session.completed_at - session.created_at).total_seconds()
            logger.info(
                "portfolio_onboarding_completed",
                onboarding_id=onboarding_id,
                total_turns=len(session.turns),
                duration_seconds=round(duration_seconds, 2),
                projects_captured=len(session.captured_projects),
            )
        elif new_state == PortfolioOnboardingState.DECLINED:
            duration_seconds = (datetime.now() - session.created_at).total_seconds()
            logger.info(
                "portfolio_onboarding_declined",
                onboarding_id=onboarding_id,
                turns_before_decline=len(session.turns),
                duration_seconds=round(duration_seconds, 2),
                last_state=current_state.value,
            )

        logger.info(
            "portfolio_onboarding_state_changed",
            onboarding_id=onboarding_id,
            from_state=current_state.value,
            to_state=new_state.value,
        )

        return session

    def add_turn(
        self,
        onboarding_id: str,
        user_message: str,
        assistant_response: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        """
        Record a conversation turn.

        Args:
            onboarding_id: Session to add turn to
            user_message: User's input
            assistant_response: Piper's response
            metadata: Additional metadata

        Returns:
            Created ConversationTurn

        Raises:
            KeyError: If session not found
        """
        session = self._sessions.get(onboarding_id)
        if not session:
            raise KeyError(f"Onboarding session not found: {onboarding_id}")

        turn = ConversationTurn(
            conversation_id=onboarding_id,
            turn_number=len(session.turns) + 1,
            user_message=user_message,
            assistant_response=assistant_response,
            metadata=metadata or {},
            completed_at=datetime.now(),
        )

        session.turns.append(turn)
        session.updated_at = datetime.now()

        # Memory optimization - trim old turns if exceeding limit
        if len(session.turns) > self.MAX_TURN_HISTORY:
            session.turns = session.turns[-self.MAX_TURN_HISTORY :]
            logger.debug(
                "portfolio_onboarding_turns_trimmed",
                onboarding_id=onboarding_id,
                kept_turns=self.MAX_TURN_HISTORY,
            )

        logger.debug(
            "portfolio_onboarding_turn_added",
            onboarding_id=onboarding_id,
            turn_number=turn.turn_number,
        )

        return turn

    def add_project(
        self,
        onboarding_id: str,
        project_data: Dict[str, Any],
    ) -> PortfolioOnboardingSession:
        """
        Add a captured project to the session.

        Args:
            onboarding_id: Session to update
            project_data: Project info dict (name, description, etc.)

        Returns:
            Updated session

        Raises:
            KeyError: If session not found
        """
        session = self._sessions.get(onboarding_id)
        if not session:
            raise KeyError(f"Onboarding session not found: {onboarding_id}")

        session.captured_projects.append(project_data)
        session.updated_at = datetime.now()

        logger.info(
            "portfolio_onboarding_project_added",
            onboarding_id=onboarding_id,
            project_name=project_data.get("name", "unnamed"),
            total_projects=len(session.captured_projects),
        )

        return session

    def get_captured_projects(self, onboarding_id: str) -> List[Dict[str, Any]]:
        """
        Get all captured projects for a session.

        Args:
            onboarding_id: Session ID

        Returns:
            List of captured project dicts

        Raises:
            KeyError: If session not found
        """
        session = self._sessions.get(onboarding_id)
        if not session:
            raise KeyError(f"Onboarding session not found: {onboarding_id}")

        return session.captured_projects

    def cleanup_expired(self, max_age_minutes: int = 30) -> int:
        """
        Remove expired/abandoned sessions.

        Args:
            max_age_minutes: Maximum age in minutes before cleanup

        Returns:
            Count of removed sessions
        """
        now = datetime.now()
        expired_ids = []

        for session_id, session in self._sessions.items():
            age_minutes = (now - session.updated_at).total_seconds() / 60
            if age_minutes > max_age_minutes and session.state not in [
                PortfolioOnboardingState.COMPLETE
            ]:
                expired_ids.append(session_id)

        for session_id in expired_ids:
            del self._sessions[session_id]
            logger.info("portfolio_onboarding_expired", onboarding_id=session_id)

        return len(expired_ids)
