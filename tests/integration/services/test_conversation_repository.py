"""Integration tests for ConversationRepository - Issue #563

Tests the actual database persistence of conversation turns.
"""

from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.models import ConversationDB, ConversationTurnDB
from services.database.repositories import ConversationRepository
from services.domain import models as domain

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def db_session():
    """Fresh per-test engine (#1452 wave 2). The global AsyncSessionFactory's
    shared pool accumulates loop-bound connections abandoned by earlier tests
    in a full sweep — asyncpg 'another operation is in progress' at setup —
    so these fixtures never borrow from it (the B15 house pattern)."""
    engine = create_async_engine(_DB_URL)
    maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def test_conversation(db_session):
    """Create a test conversation in the database."""
    conversation_id = str(uuid4())
    user_id = str(uuid4())

    conversation = ConversationDB(
        id=conversation_id,
        user_id=user_id,
        session_id=str(uuid4()),
        title="Test Conversation",
        context={},
        is_active=True,
    )

    db_session.add(conversation)
    await db_session.commit()

    yield conversation

    # Cleanup - turns will cascade delete
    await db_session.delete(conversation)
    await db_session.commit()


class TestConversationRepository:
    """Tests for ConversationRepository methods."""

    @pytest.mark.asyncio
    async def test_save_turn_creates_new_turn(self, db_session, test_conversation):
        """Test that save_turn creates a new turn in the database."""
        repo = ConversationRepository(db_session)

        turn = domain.ConversationTurn(
            id=str(uuid4()),
            conversation_id=test_conversation.id,
            turn_number=1,
            user_message="Hello Piper!",
            assistant_response="Hello! How can I help you today?",
            intent="greeting",
            entities=["user"],
            references={},
            context_used={},
            metadata={"source": "test"},
            processing_time=150.5,
            created_at=datetime.now(),
            completed_at=datetime.now(),
        )

        await repo.save_turn(turn)

        # Verify it was saved
        saved = await db_session.get(ConversationTurnDB, turn.id)
        assert saved is not None
        assert saved.user_message == "Hello Piper!"
        assert saved.assistant_response == "Hello! How can I help you today?"
        assert saved.turn_number == 1

    @pytest.mark.asyncio
    async def test_save_turn_updates_existing_turn(self, db_session, test_conversation):
        """Test that save_turn updates an existing turn (upsert behavior)."""
        repo = ConversationRepository(db_session)
        turn_id = str(uuid4())

        # Create initial turn
        turn = domain.ConversationTurn(
            id=turn_id,
            conversation_id=test_conversation.id,
            turn_number=1,
            user_message="Initial message",
            assistant_response="",  # Empty response initially
        )
        await repo.save_turn(turn)

        # Update with response
        turn.assistant_response = "Here is the response"
        turn.completed_at = datetime.now()
        await repo.save_turn(turn)

        # Verify update
        saved = await db_session.get(ConversationTurnDB, turn_id)
        assert saved.assistant_response == "Here is the response"
        assert saved.completed_at is not None

    @pytest.mark.asyncio
    async def test_get_conversation_turns_returns_ordered_turns(
        self, db_session, test_conversation
    ):
        """Test that get_conversation_turns returns turns in order."""
        repo = ConversationRepository(db_session)

        # Create multiple turns out of order
        for i in [3, 1, 2]:
            turn = domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=test_conversation.id,
                turn_number=i,
                user_message=f"Message {i}",
                assistant_response=f"Response {i}",
            )
            await repo.save_turn(turn)

        # Fetch and verify order
        turns = await repo.get_conversation_turns(test_conversation.id)

        assert len(turns) == 3
        assert turns[0].turn_number == 1
        assert turns[1].turn_number == 2
        assert turns[2].turn_number == 3
        assert turns[0].user_message == "Message 1"
        assert turns[0].assistant_response == "Response 1"

    @pytest.mark.asyncio
    async def test_get_conversation_turns_respects_limit(self, db_session, test_conversation):
        """Test that get_conversation_turns respects the limit parameter."""
        repo = ConversationRepository(db_session)

        # Create 5 turns
        for i in range(1, 6):
            turn = domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=test_conversation.id,
                turn_number=i,
                user_message=f"Message {i}",
                assistant_response=f"Response {i}",
            )
            await repo.save_turn(turn)

        # Fetch with limit
        turns = await repo.get_conversation_turns(test_conversation.id, limit=3)

        assert len(turns) == 3
        assert turns[0].turn_number == 1  # Returns first 3 in order

    @pytest.mark.asyncio
    async def test_get_conversation_turns_most_recent(self, db_session, test_conversation):
        """#1223: most_recent=True returns the NEWEST `limit` turns, chronologically."""
        repo = ConversationRepository(db_session)

        # Create 5 turns
        for i in range(1, 6):
            turn = domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=test_conversation.id,
                turn_number=i,
                user_message=f"Message {i}",
                assistant_response=f"Response {i}",
            )
            await repo.save_turn(turn)

        # most_recent=True with limit=3 -> turns 3,4,5 (newest), chronological order
        turns = await repo.get_conversation_turns(test_conversation.id, limit=3, most_recent=True)
        assert len(turns) == 3
        assert turns[0].turn_number == 3  # oldest-of-the-newest first
        assert turns[-1].turn_number == 5  # most-recent last (chronological)

        # Regression guard: default (oldest-N) behavior is unchanged
        default_turns = await repo.get_conversation_turns(test_conversation.id, limit=3)
        assert default_turns[0].turn_number == 1
        assert default_turns[-1].turn_number == 3

    @pytest.mark.asyncio
    async def test_get_conversation_turns_returns_empty_for_nonexistent(self, db_session):
        """Test that get_conversation_turns returns empty list for nonexistent conversation."""
        repo = ConversationRepository(db_session)

        turns = await repo.get_conversation_turns("nonexistent-conversation-id")

        assert turns == []

    @pytest.mark.asyncio
    async def test_get_next_turn_number_returns_one_for_empty(self, db_session, test_conversation):
        """Test that get_next_turn_number returns 1 for conversation with no turns."""
        repo = ConversationRepository(db_session)

        next_num = await repo.get_next_turn_number(test_conversation.id)

        assert next_num == 1

    @pytest.mark.asyncio
    async def test_get_next_turn_number_returns_correct_sequence(
        self, db_session, test_conversation
    ):
        """Test that get_next_turn_number returns max + 1."""
        repo = ConversationRepository(db_session)

        # Create some turns
        for i in [1, 2, 5]:  # Non-sequential to test max logic
            turn = domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=test_conversation.id,
                turn_number=i,
                user_message=f"Message {i}",
                assistant_response=f"Response {i}",
            )
            await repo.save_turn(turn)

        next_num = await repo.get_next_turn_number(test_conversation.id)

        assert next_num == 6  # max(1,2,5) + 1


class TestConversationRepositoryRoundTrip:
    """Test complete save/load roundtrip - the core fix for Issue #563."""

    @pytest.mark.asyncio
    async def test_full_roundtrip_preserves_all_fields(self, db_session, test_conversation):
        """Test that save and load preserves all ConversationTurn fields."""
        repo = ConversationRepository(db_session)

        original = domain.ConversationTurn(
            id=str(uuid4()),
            conversation_id=test_conversation.id,
            turn_number=1,
            user_message="What's the weather today?",
            assistant_response="I don't have access to weather data, but I can help with other things!",
            intent="query",
            entities=["weather", "today"],
            references={"topic": "weather"},
            context_used={"previous_turn": None},
            metadata={"channel": "web", "client_version": "1.0"},
            processing_time=234.5,
            created_at=datetime.now(),
            completed_at=datetime.now(),
        )

        # Save
        await repo.save_turn(original)

        # Load
        turns = await repo.get_conversation_turns(test_conversation.id)

        assert len(turns) == 1
        loaded = turns[0]

        # Verify all fields preserved
        assert loaded.id == original.id
        assert loaded.conversation_id == original.conversation_id
        assert loaded.turn_number == original.turn_number
        assert loaded.user_message == original.user_message
        assert loaded.assistant_response == original.assistant_response
        assert loaded.intent == original.intent
        assert loaded.entities == original.entities
        assert loaded.references == original.references
        assert loaded.context_used == original.context_used
        assert loaded.metadata == original.metadata
        assert loaded.processing_time == original.processing_time

    @pytest.mark.asyncio
    async def test_both_user_and_assistant_messages_persist(self, db_session, test_conversation):
        """Critical test for Issue #563: Both sides of conversation must persist."""
        repo = ConversationRepository(db_session)

        # Simulate a multi-turn conversation
        turns_data = [
            ("Hello!", "Hi there! How can I help?"),
            ("What's my next meeting?", "You have a standup at 10am."),
            ("Thanks!", "You're welcome! Anything else?"),
        ]

        for i, (user_msg, assistant_msg) in enumerate(turns_data, 1):
            turn = domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=test_conversation.id,
                turn_number=i,
                user_message=user_msg,
                assistant_response=assistant_msg,
            )
            await repo.save_turn(turn)

        # Simulate page refresh - load all turns
        loaded_turns = await repo.get_conversation_turns(test_conversation.id)

        assert len(loaded_turns) == 3

        # Verify BOTH user messages AND assistant responses are present
        for i, turn in enumerate(loaded_turns):
            expected_user, expected_assistant = turns_data[i]
            assert turn.user_message == expected_user, f"Turn {i+1} user message missing"
            assert (
                turn.assistant_response == expected_assistant
            ), f"Turn {i+1} assistant response missing - THIS WAS THE BUG"
