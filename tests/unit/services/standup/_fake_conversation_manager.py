"""
Test double for StandupConversationManager — in-memory, no DB.

Mirrors the StandupConversationManager API surface (post-#1052 Phase 2
rewrite) so tests that use the manager as a *dependency* for testing
other classes (StandupConversationHandler, StandupProcessAdapter,
intent-service standup routing) don't need an AsyncSessionFactory or
DB session.

This is explicitly a TEST DOUBLE — never imported from production code.

Production StandupConversationManager
(`services/standup/conversation_manager.py`) is async + repository-backed.
Tests that need to verify production behavior (persistence,
transaction-boundary, etc.) use `StandupConversationRepository` against
in-memory SQLite per the #1052 Phase 1 pattern at
`tests/unit/services/test_standup_conversation_repository_1052.py`, or
the manager-level integration tests at
`tests/unit/services/standup/test_conversation_state.py`.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from services.domain.models import (
    ConversationTurn,
    StandupConversation,
    StandupPartialCapture,
)
from services.shared_types import StandupConversationState
from services.standup.conversation_manager import (
    InvalidStateTransitionError,
    StandupConversationManager,
)


class FakeStandupConversationManager:
    """In-memory test double of StandupConversationManager.

    Implements the same async API as the production manager (post-#1052
    Phase 2) using an in-memory dict. Suitable for tests that depend on
    the manager's surface behavior but don't exercise persistence
    semantics.
    """

    MAX_TURN_HISTORY = StandupConversationManager.MAX_TURN_HISTORY
    VALID_TRANSITIONS = StandupConversationManager.VALID_TRANSITIONS

    def __init__(self) -> None:
        self._conversations: Dict[str, StandupConversation] = {}

    async def create_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> StandupConversation:
        if not user_id:
            raise ValueError("user_id is required for multi-tenancy isolation")
        conv = StandupConversation(
            session_id=session_id,
            user_id=user_id,
            context=initial_context or {},
        )
        self._conversations[conv.id] = conv
        return conv

    async def get_conversation(self, conversation_id: str) -> Optional[StandupConversation]:
        return self._conversations.get(conversation_id)

    async def get_conversation_by_session(
        self, session_id: str, include_suspended: bool = False
    ) -> Optional[StandupConversation]:
        terminal = [
            StandupConversationState.COMPLETE,
            StandupConversationState.ABANDONED,
        ]
        if not include_suspended:
            terminal.append(StandupConversationState.SUSPENDED)
        for conv in reversed(list(self._conversations.values())):
            if conv.session_id == session_id and conv.state not in terminal:
                return conv
        return None

    async def get_conversation_by_user(
        self, user_id: str, include_suspended: bool = False
    ) -> Optional[StandupConversation]:
        terminal = [
            StandupConversationState.COMPLETE,
            StandupConversationState.ABANDONED,
        ]
        if not include_suspended:
            terminal.append(StandupConversationState.SUSPENDED)
        for conv in reversed(list(self._conversations.values())):
            if conv.user_id == user_id and conv.state not in terminal:
                return conv
        return None

    async def get_suspended_for_user(self, user_id: str) -> Optional[StandupConversation]:
        for conv in reversed(list(self._conversations.values())):
            if conv.user_id == user_id and conv.state == StandupConversationState.SUSPENDED:
                return conv
        return None

    async def transition_state(
        self,
        conversation_id: str,
        new_state: StandupConversationState,
    ) -> StandupConversation:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        valid_targets = self.VALID_TRANSITIONS.get(conv.state, [])
        if new_state not in valid_targets:
            raise InvalidStateTransitionError(
                f"Cannot transition from {conv.state.value} to {new_state.value}. "
                f"Valid transitions: {[s.value for s in valid_targets]}"
            )
        conv.previous_state = conv.state
        conv.state = new_state
        conv.updated_at = datetime.now(timezone.utc)
        if new_state == StandupConversationState.COMPLETE:
            conv.completed_at = datetime.now(timezone.utc)
        return conv

    async def add_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        intent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ConversationTurn:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        turn = ConversationTurn(
            conversation_id=conversation_id,
            turn_number=len(conv.turns) + 1,
            user_message=user_message,
            assistant_response=assistant_response,
            intent=intent,
            metadata=metadata or {},
            completed_at=datetime.now(timezone.utc),
        )
        conv.turns.append(turn)
        conv.updated_at = datetime.now(timezone.utc)
        if len(conv.turns) > self.MAX_TURN_HISTORY:
            conv.turns = conv.turns[-self.MAX_TURN_HISTORY :]
        return turn

    async def update_preferences(
        self,
        conversation_id: str,
        preferences: Dict[str, Any],
    ) -> StandupConversation:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        conv.preferences.update(preferences)
        conv.updated_at = datetime.now(timezone.utc)
        return conv

    async def set_standup_content(
        self,
        conversation_id: str,
        content: str,
    ) -> StandupConversation:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        if conv.current_standup:
            conv.standup_versions.append(conv.current_standup)
        conv.current_standup = content
        conv.updated_at = datetime.now(timezone.utc)
        return conv

    async def update_partial_capture(
        self,
        conversation_id: str,
        capture: StandupPartialCapture,
    ) -> StandupConversation:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        conv.partial_capture = capture
        conv.updated_at = datetime.now(timezone.utc)
        return conv

    async def bind_session_id(
        self,
        conversation_id: str,
        session_id: str,
    ) -> StandupConversation:
        conv = self._conversations.get(conversation_id)
        if not conv:
            raise KeyError(f"Conversation not found: {conversation_id}")
        conv.session_id = session_id
        conv.updated_at = datetime.now(timezone.utc)
        return conv

    async def cleanup_expired(self, max_age_minutes: int = 60) -> int:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=max_age_minutes)
        expired = [
            cid
            for cid, c in self._conversations.items()
            if c.updated_at < cutoff and c.state != StandupConversationState.COMPLETE
        ]
        for cid in expired:
            del self._conversations[cid]
        return len(expired)
