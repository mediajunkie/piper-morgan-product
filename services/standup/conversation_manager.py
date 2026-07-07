"""
Issue #552: Standup conversation state management service.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Provides state machine management for interactive standup conversations,
including state transitions, turn recording, and preference tracking.

Issue #556 Phase 4: Enhanced with structured performance logging.

Issue #1052 Phase 2 (May 5, 2026): Manager rewritten to delegate to
`StandupConversationRepository` (durable PostgreSQL persistence) rather
than holding state in an in-memory dict. All methods are async; each
opens its own session via `AsyncSessionFactory.session_scope()`,
mirroring the #1018/#1035 transaction-boundary pattern. Required for
#900 Phase 4 (resume-after-restart).
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import (
    ConversationTurn,
    StandupConversation,
    StandupPartialCapture,
)
from services.shared_types import StandupConversationState
from services.utils.datetime_utils import ensure_utc

logger = structlog.get_logger()


class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""

    pass


class StandupConversationManager:
    """
    Issue #552: Manages standup conversation state and transitions.

    Per #1052 Phase 2 (May 5, 2026), the manager is stateless — all
    persistence flows through `StandupConversationRepository`. Each
    public method opens its own session via
    `AsyncSessionFactory.session_scope()` and delegates to the
    repository. Transaction-boundary is per-call so a manager-write
    failure doesn't cascade into the caller's transaction (mirrors
    #1018 Q2 ratification).

    Provides:
    - Conversation lifecycle (create, get, complete)
    - State machine validation (in-memory class data; not persisted state)
    - Turn recording
    - Durable persistence via the repository
    """

    # Issue #556: Memory optimization - limit turn history to prevent unbounded growth
    MAX_TURN_HISTORY = 50  # Typical standups complete in 5-10 turns

    # Valid state transitions - defines the state machine
    # Issue #888: Added SUSPENDED state (escape command or timeout)
    # Issue #900 Phase 1: Added GATHERING_YESTERDAY/TODAY/BLOCKERS 3-part flow.
    # INITIATED can route to either the legacy GATHERING_PREFERENCES path or
    # the new GATHERING_YESTERDAY path; the handler picks based on flow.
    VALID_TRANSITIONS: Dict[StandupConversationState, List[StandupConversationState]] = {
        StandupConversationState.INITIATED: [
            StandupConversationState.GATHERING_PREFERENCES,  # Legacy preference flow
            StandupConversationState.GATHERING_YESTERDAY,  # #900 3-part flow entry
            StandupConversationState.GENERATING,  # Skip preferences if user wants quick standup
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.GATHERING_PREFERENCES: [
            StandupConversationState.GENERATING,
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.GATHERING_YESTERDAY: [
            StandupConversationState.GATHERING_TODAY,  # Normal advance
            StandupConversationState.GENERATING,  # Early-completion signal (e.g., "skip rest")
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.GATHERING_TODAY: [
            StandupConversationState.GATHERING_BLOCKERS,  # Normal advance
            StandupConversationState.GENERATING,  # Early-completion signal
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.GATHERING_BLOCKERS: [
            StandupConversationState.GENERATING,  # All 3 parts captured → generate
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.GENERATING: [
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,  # Skip refinement if user accepts
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.REFINING: [
            StandupConversationState.GENERATING,  # Re-generate with new preferences
            StandupConversationState.FINALIZING,
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.FINALIZING: [
            StandupConversationState.COMPLETE,
            StandupConversationState.REFINING,  # User wants more changes
            StandupConversationState.ABANDONED,
            StandupConversationState.SUSPENDED,  # Escape command or timeout
        ],
        StandupConversationState.SUSPENDED: [
            StandupConversationState.INITIATED,  # Legacy resume path (re-enter via _handle_initiated)
            # #900 Phase 4: Direct resume back into the 3-part collection
            # at the part the user left off in. Avoids the round-trip
            # through INITIATED that would discard partial_capture context.
            StandupConversationState.GATHERING_YESTERDAY,
            StandupConversationState.GATHERING_TODAY,
            StandupConversationState.GATHERING_BLOCKERS,
            StandupConversationState.ABANDONED,  # User declined to resume
        ],
        StandupConversationState.COMPLETE: [],  # Terminal state
        StandupConversationState.ABANDONED: [],  # Terminal state
    }

    def __init__(self) -> None:
        """No-arg constructor preserved for callers that defaulted it."""
        pass

    @staticmethod
    def _session_scope():
        """Open a fresh transactional session for one manager operation.

        Imported lazily so that services/standup doesn't depend on
        services/database at module-load time.

        Issue #1079 (2026-05-16): switched from `session_scope()` to
        `transaction_scope()`. The former opens a session WITHOUT a
        commit on success (only rolls back on exception, closes on
        exit) — so writes via `repo.add()` only flush, are never
        committed, and disappear at session close. The repo's docstring
        ("Caller owns the transaction. ... session_scope() handles
        commit.") asserts the commit-on-success behavior that
        `session_scope()` does not actually provide. `transaction_scope()`
        uses `session.begin()` which commits on success and rolls back
        on exception — matching the docstring's stated contract.
        Read-only methods still work under transaction_scope (commits an
        empty transaction; small overhead is acceptable).
        """
        from services.database.session_factory import AsyncSessionFactory

        return AsyncSessionFactory.transaction_scope()

    @staticmethod
    def _new_repo(session):
        """Construct a StandupConversationRepository over the given session."""
        from services.database.repositories import StandupConversationRepository

        return StandupConversationRepository(session)

    async def create_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> StandupConversation:
        """
        Create a new standup conversation.

        Args:
            session_id: Session identifier
            user_id: User identifier (required for multi-tenancy isolation)
            initial_context: Optional initial context (e.g., from integrations)

        Returns:
            New StandupConversation instance

        Raises:
            ValueError: If user_id is None or empty
        """
        # Issue #734: Validate user_id for multi-tenancy isolation
        if not user_id:
            raise ValueError("user_id is required for multi-tenancy isolation")

        conversation = StandupConversation(
            session_id=session_id,
            user_id=user_id,
            context=initial_context or {},
        )

        async with self._session_scope() as session:
            repo = self._new_repo(session)
            await repo.add(conversation)

        logger.info(
            "standup_conversation_created",
            conversation_id=conversation.id,
            session_id=session_id,
            user_id=user_id,
        )

        return conversation

    async def get_conversation(self, conversation_id: str) -> Optional[StandupConversation]:
        """Retrieve a conversation by ID."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.get_by_id(conversation_id)

    async def get_conversation_by_session(
        self, session_id: str, include_suspended: bool = False
    ) -> Optional[StandupConversation]:
        """
        Retrieve active conversation for a session.

        Returns the most recent non-terminal conversation for the session.

        Issue #889: SUSPENDED is excluded by default (it's non-active from the
        registry's perspective). Pass include_suspended=True when you need to
        find a suspended conversation for resume offers.
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conv = await repo.get_by_session_id(session_id)

        if conv is None:
            return None
        if conv.state in (
            StandupConversationState.COMPLETE,
            StandupConversationState.ABANDONED,
        ):
            return None
        if not include_suspended and conv.state == StandupConversationState.SUSPENDED:
            return None
        return conv

    async def get_conversation_by_user(
        self, user_id: str, include_suspended: bool = False
    ) -> Optional[StandupConversation]:
        """
        Retrieve active conversation for a user.

        Issue #734: Primary lookup method for multi-tenancy isolation.
        Returns the most recent non-terminal conversation for the user.

        Issue #889: SUSPENDED is excluded by default. Pass include_suspended=True
        when you need to find a suspended conversation for resume offers.
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            active = await repo.get_active_for_user(user_id)

        # Repository excludes COMPLETE/ABANDONED already; filter SUSPENDED here.
        for conv in active:
            if not include_suspended and conv.state == StandupConversationState.SUSPENDED:
                continue
            return conv
        return None

    async def get_suspended_for_user(self, user_id: str) -> Optional[StandupConversation]:
        """
        Find the most-recent SUSPENDED conversation for a user, if any.

        Issue #888: Used by `has_suspended_session()` to surface resume
        offers. Returns the newest suspended conversation across all of the
        user's sessions; None if there is none.
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            active = await repo.get_active_for_user(user_id)

        for conv in active:
            if conv.state == StandupConversationState.SUSPENDED:
                return conv
        return None

    async def transition_state(
        self,
        conversation_id: str,
        new_state: StandupConversationState,
    ) -> StandupConversation:
        """
        Transition conversation to a new state.

        Args:
            conversation_id: Conversation to transition
            new_state: Target state

        Returns:
            Updated conversation

        Raises:
            InvalidStateTransitionError: If transition is not valid
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            current_state = conversation.state
            valid_targets = self.VALID_TRANSITIONS.get(current_state, [])

            if new_state not in valid_targets:
                raise InvalidStateTransitionError(
                    f"Cannot transition from {current_state.value} to {new_state.value}. "
                    f"Valid transitions: {[s.value for s in valid_targets]}"
                )

            conversation.previous_state = current_state
            conversation.state = new_state
            # #1079: tz-aware to match DB-issued created_at (offset-aware UTC).
            # Naive datetime here propagated through updated_at and broke the
            # StandupProcessAdapter.check_active timeout-elapsed math, making
            # the registry fail to recognize the active session on Turn 2.
            conversation.updated_at = datetime.now(timezone.utc)

            if new_state == StandupConversationState.COMPLETE:
                conversation.completed_at = datetime.now(timezone.utc)

            await repo.update(conversation)

        if new_state == StandupConversationState.COMPLETE:
            # #1079: coerce both operands to tz-aware UTC. created_at can come
            # back tz-naive from a backend that drops tzinfo (e.g. SQLite in
            # tests; defensive for any pre-round-trip object), while completed_at
            # was just set tz-aware — subtracting the two raw would TypeError.
            duration_seconds = (
                ensure_utc(conversation.completed_at) - ensure_utc(conversation.created_at)
            ).total_seconds()
            logger.info(
                "standup_conversation_completed",
                conversation_id=conversation_id,
                total_turns=len(conversation.turns),
                duration_seconds=round(duration_seconds, 2),
                has_standup_content=conversation.current_standup is not None,
                versions_created=(
                    len(conversation.standup_versions) + 1 if conversation.current_standup else 0
                ),
            )
        elif new_state == StandupConversationState.ABANDONED:
            # #1079: created_at may be tz-naive (see COMPLETE branch above).
            duration_seconds = (
                datetime.now(timezone.utc) - ensure_utc(conversation.created_at)
            ).total_seconds()
            logger.info(
                "standup_conversation_abandoned",
                conversation_id=conversation_id,
                turns_before_abandon=len(conversation.turns),
                duration_seconds=round(duration_seconds, 2),
                last_state=current_state.value,
            )

        logger.info(
            "standup_conversation_state_changed",
            conversation_id=conversation_id,
            from_state=current_state.value,
            to_state=new_state.value,
        )

        return conversation

    async def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        intent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        """
        Record a conversation turn.

        Args:
            conversation_id: Conversation to add turn to
            user_message: User's input
            assistant_response: Piper's response
            intent: Classified intent for this turn
            metadata: Additional metadata

        Returns:
            Created ConversationTurn

        Raises:
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            turn = ConversationTurn(
                conversation_id=conversation_id,
                turn_number=len(conversation.turns) + 1,
                user_message=user_message,
                assistant_response=assistant_response,
                intent=intent,
                metadata=metadata or {},
                completed_at=datetime.now(timezone.utc),
            )

            conversation.turns.append(turn)
            conversation.updated_at = datetime.now(timezone.utc)  # #1285: tz-aware, matching the #1079 fix + the DateTime(timezone=True) column

            # Issue #556: Memory optimization - trim old turns if exceeding limit
            trimmed = False
            if len(conversation.turns) > self.MAX_TURN_HISTORY:
                conversation.turns = conversation.turns[-self.MAX_TURN_HISTORY :]
                trimmed = True

            await repo.update(conversation)

        if trimmed:
            logger.debug(
                "standup_conversation_turns_trimmed",
                conversation_id=conversation_id,
                kept_turns=self.MAX_TURN_HISTORY,
            )

        logger.debug(
            "standup_conversation_turn_added",
            conversation_id=conversation_id,
            turn_number=turn.turn_number,
        )

        return turn

    async def update_preferences(
        self,
        conversation_id: str,
        preferences: Dict[str, Any],
    ) -> StandupConversation:
        """
        Update conversation preferences.

        Args:
            conversation_id: Conversation to update
            preferences: Preference dict to merge

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            conversation.preferences.update(preferences)
            conversation.updated_at = datetime.now(timezone.utc)  # #1285: tz-aware, matching the #1079 fix + the DateTime(timezone=True) column
            await repo.update(conversation)

        return conversation

    async def set_standup_content(
        self,
        conversation_id: str,
        content: str,
    ) -> StandupConversation:
        """
        Set/update the current standup content.

        Keeps version history for refinement tracking.

        Args:
            conversation_id: Conversation to update
            content: New standup content

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            # Save previous version if exists
            if conversation.current_standup:
                conversation.standup_versions.append(conversation.current_standup)

            conversation.current_standup = content
            conversation.updated_at = datetime.now(timezone.utc)  # #1285: tz-aware, matching the #1079 fix + the DateTime(timezone=True) column
            await repo.update(conversation)

        return conversation

    async def bind_session_id(
        self,
        conversation_id: str,
        session_id: str,
    ) -> StandupConversation:
        """
        Rebind a conversation to a new session_id.

        Used when resuming a SUSPENDED conversation in a new session
        (Issue #889) — the adapter routes by session_id, so the resumed
        conversation must be visible from the current session.

        Args:
            conversation_id: Conversation to rebind
            session_id: New session identifier

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            conversation.session_id = session_id
            conversation.updated_at = datetime.now(timezone.utc)  # #1285: tz-aware, matching the #1079 fix + the DateTime(timezone=True) column
            await repo.update(conversation)

        return conversation

    async def update_partial_capture(
        self,
        conversation_id: str,
        capture: StandupPartialCapture,
    ) -> StandupConversation:
        """
        Replace the conversation's 3-part `partial_capture` (Issue #900 Phase 2).

        Args:
            conversation_id: Conversation to update
            capture: New StandupPartialCapture (full replace, not merge)

        Returns:
            Updated conversation

        Raises:
            KeyError: If conversation not found
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            conversation = await repo.get_by_id(conversation_id)
            if not conversation:
                raise KeyError(f"Conversation not found: {conversation_id}")

            conversation.partial_capture = capture
            conversation.updated_at = datetime.now(timezone.utc)  # #1285: tz-aware, matching the #1079 fix + the DateTime(timezone=True) column
            await repo.update(conversation)

        return conversation

    async def cleanup_expired(self, max_age_minutes: int = 60) -> int:
        """
        Remove abandoned/expired conversations.

        Args:
            max_age_minutes: Maximum age in minutes before cleanup

        Returns:
            Count of removed conversations
        """
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            removed = await repo.delete_stale(max_age_minutes)

        if removed:
            logger.info(
                "standup_conversation_expired_cleanup",
                removed_count=removed,
                max_age_minutes=max_age_minutes,
            )

        return removed
