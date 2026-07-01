"""
Unit tests for Conversations API Routes
Issue #583: Auto-load conversation history on page refresh

Tests verify that the backend correctly returns BOTH user_message AND assistant_response
fields in conversation turns. This proves the backend works - the bug is in the frontend
JavaScript that doesn't auto-load conversation history on page refresh.

Critical Schema Note:
The database uses a PAIRED TURN MODEL:
- Table conversation_turns has columns: user_message, assistant_response, turn_number, conversation_id
- NOT a role column with separate rows for user/assistant
- Both messages are stored in the SAME row
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain import models as domain
from web.api.routes.conversations import ConversationTurnResponse, get_conversation_turns


class TestGetConversationTurns:
    """Tests for GET /api/v1/conversations/{conversation_id}/turns

    Issue #583: These tests verify the API contract for conversation turn retrieval.
    The backend must return both user_message AND assistant_response for each turn.
    """

    @pytest.fixture
    def mock_current_user(self):
        """Create a mock current user (JWTClaims)."""
        user = MagicMock()
        user.sub = str(uuid4())
        user.username = "testuser"
        return user

    @pytest.fixture
    def mock_conversation(self, mock_current_user):
        """Create a mock conversation owned by the current user."""
        conv = MagicMock()
        conv.id = str(uuid4())
        conv.user_id = mock_current_user.sub
        conv.title = "Test Conversation"
        return conv

    @pytest.mark.asyncio
    async def test_returns_both_user_message_and_assistant_response_issue_583(
        self, mock_current_user, mock_conversation
    ):
        """
        Issue #583: Verify API returns turns with BOTH user_message AND assistant_response.

        This test proves the backend contract is correct - each turn must contain
        both the user's message and the assistant's response. The bug in #583
        is that the frontend doesn't auto-load this data on page refresh.
        """
        # Setup: Create domain turns with both messages populated
        test_turns = [
            domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=mock_conversation.id,
                turn_number=1,
                user_message="Hello Piper!",
                assistant_response="Hello! How can I help you today?",
                created_at=datetime.now(),
            ),
            domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=mock_conversation.id,
                turn_number=2,
                user_message="What's on my calendar?",
                assistant_response="You have a standup meeting at 10am.",
                created_at=datetime.now(),
            ),
        ]

        # Mock the repository
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_conversation)
        mock_repo.get_conversation_turns = AsyncMock(return_value=test_turns)

        # Act: Call the endpoint
        result = await get_conversation_turns(
            conversation_id=mock_conversation.id,
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        # Assert: Response contains both fields for each turn
        assert len(result) == 2

        # First turn
        assert result[0].user_message == "Hello Piper!"
        assert result[0].assistant_response == "Hello! How can I help you today?"
        assert result[0].turn_number == 1

        # Second turn
        assert result[1].user_message == "What's on my calendar?"
        assert result[1].assistant_response == "You have a standup meeting at 10am."
        assert result[1].turn_number == 2

    @pytest.mark.asyncio
    async def test_requests_most_recent_window_issue_1235(
        self, mock_current_user, mock_conversation
    ):
        """#1235: the /turns restore endpoint must fetch the NEWEST `limit` turns, not the
        oldest — a >limit conversation should show where the user left off, not turns
        1..limit. Asserts the endpoint passes most_recent=True (the #1223 machinery)."""
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_conversation)
        mock_repo.get_conversation_turns = AsyncMock(return_value=[])

        await get_conversation_turns(
            conversation_id=mock_conversation.id,
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        mock_repo.get_conversation_turns.assert_awaited_once_with(
            mock_conversation.id, limit=50, most_recent=True
        )

    @pytest.mark.asyncio
    async def test_returns_empty_list_for_new_conversation_no_turns_issue_583(
        self, mock_current_user, mock_conversation
    ):
        """
        Issue #583: Verify API returns empty list for conversation with no turns.

        This is a valid state - when a user creates a new conversation but hasn't
        sent any messages yet.
        """
        # Setup: Mock empty turns
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_conversation)
        mock_repo.get_conversation_turns = AsyncMock(return_value=[])

        # Act
        result = await get_conversation_turns(
            conversation_id=mock_conversation.id,
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_response_model_includes_required_fields_issue_583(
        self, mock_current_user, mock_conversation
    ):
        """
        Issue #583: Verify ConversationTurnResponse includes all required fields.

        The response model must include:
        - id: unique turn identifier
        - turn_number: sequential order
        - user_message: what the user said
        - assistant_response: what Piper replied
        - created_at: timestamp
        """
        test_turn = domain.ConversationTurn(
            id="turn-123",
            conversation_id=mock_conversation.id,
            turn_number=1,
            user_message="Test user message",
            assistant_response="Test assistant response",
            created_at=datetime(2026, 1, 13, 9, 0, 0),
        )

        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=mock_conversation)
        mock_repo.get_conversation_turns = AsyncMock(return_value=[test_turn])

        result = await get_conversation_turns(
            conversation_id=mock_conversation.id,
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        assert len(result) == 1
        turn_response = result[0]

        # Verify response model structure
        assert isinstance(turn_response, ConversationTurnResponse)
        assert turn_response.id == "turn-123"
        assert turn_response.turn_number == 1
        assert turn_response.user_message == "Test user message"
        assert turn_response.assistant_response == "Test assistant response"
        assert turn_response.created_at == "2026-01-13T09:00:00"

    @pytest.mark.asyncio
    async def test_returns_empty_for_unauthorized_conversation_issue_583(self, mock_current_user):
        """
        Issue #583: Verify API returns empty for conversations user doesn't own.

        Security: Users should not be able to access other users' conversations.
        """
        # Setup: Conversation owned by different user
        other_user_conversation = MagicMock()
        other_user_conversation.id = str(uuid4())
        other_user_conversation.user_id = str(uuid4())  # Different user

        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=other_user_conversation)

        # Act
        result = await get_conversation_turns(
            conversation_id=other_user_conversation.id,
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        # Assert: Returns empty, not an error (security: don't leak existence)
        assert result == []

    @pytest.mark.asyncio
    async def test_returns_empty_for_nonexistent_conversation_issue_583(self, mock_current_user):
        """
        Issue #583: Verify API returns empty for nonexistent conversations.

        Security: Returns empty instead of 404 to avoid leaking existence.
        """
        mock_repo = MagicMock()
        mock_repo.get_by_id = AsyncMock(return_value=None)

        result = await get_conversation_turns(
            conversation_id="nonexistent-id",
            limit=50,
            current_user=mock_current_user,
            conv_repo=mock_repo,
        )

        assert result == []


class TestConversationTurnResponseModel:
    """Tests for ConversationTurnResponse Pydantic model.

    Issue #583: Verify the response model correctly represents the paired turn model.
    """

    def test_model_has_both_message_fields(self):
        """Issue #583: Response model must have both user_message and assistant_response."""
        response = ConversationTurnResponse(
            id="test-id",
            turn_number=1,
            user_message="User says hello",
            assistant_response="Assistant responds",
            created_at="2026-01-13T09:00:00",
        )

        assert response.user_message == "User says hello"
        assert response.assistant_response == "Assistant responds"

    def test_model_validates_required_fields(self):
        """Issue #583: Response model validates all required fields."""
        # This should succeed - all required fields provided
        response = ConversationTurnResponse(
            id="test-id",
            turn_number=1,
            user_message="",  # Empty is valid
            assistant_response="",  # Empty is valid
            created_at="",  # Empty is valid
        )

        assert response.id == "test-id"
        assert response.turn_number == 1
