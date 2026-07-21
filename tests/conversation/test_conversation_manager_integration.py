"""
PM-034 Phase 3 Integration Tests: ConversationManager End-to-End Validation
Tests the complete conversation context and anaphoric resolution pipeline
Target: <150ms additional latency, 90% resolution accuracy
"""

import asyncio
import time
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy import delete, select

from services.cache.redis_factory import RedisFactory
from services.conversation.conversation_manager import ConversationManager
from services.conversation.reference_resolver import ResolvedReference
from services.database.models import ConversationDB, ConversationTurnDB
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import ConversationTurn

# #1208: a fixed, recognizable user_id so save_conversation_turn's parent
# conversation row is actually created. ensure_conversation_exists (issue #840)
# refuses to create a conversation without a user_id, so the turn INSERT then
# fails the FK constraint and the anaphora/resolution path reads zero turns.
# user_id is a plain String column (no FK) — any UUID works, no user seeding.
# The autouse cleanup fixture removes all rows under this id after each test.
TEST_USER_ID = "11111111-1111-1111-1111-111111111111"


class TestConversationManagerIntegration:
    """Test ConversationManager integration with QueryRouter and Redis"""

    @pytest.fixture
    async def mock_redis_client(self):
        """Mock Redis client for testing"""
        mock_client = AsyncMock()
        mock_client.ping = AsyncMock(return_value=True)
        mock_client.get = AsyncMock(return_value=None)
        mock_client.setex = AsyncMock(return_value=True)
        mock_client.close = AsyncMock()
        return mock_client

    @pytest.fixture
    def conversation_manager(self, mock_redis_client):
        """ConversationManager with mocked Redis"""
        return ConversationManager(
            redis_client=mock_redis_client, context_window_size=10, cache_ttl=300
        )

    @pytest_asyncio.fixture(autouse=True)
    async def _fresh_factory(self, monkeypatch):
        """#1452: bind this file's DB access to a fresh per-test engine. The
        manager's internals use the global AsyncSessionFactory, whose shared
        pool arrives poisoned (loop-bound abandoned connections) in full
        sweeps — asyncpg 'another operation is in progress' at setup. Patching
        the scope here immunizes the tests without touching the live path
        (switching the manager itself to fresh engines is a latency tradeoff
        for Arch, not a test fix)."""
        import contextlib

        from sqlalchemy.ext.asyncio import AsyncSession as _AS
        from sqlalchemy.ext.asyncio import create_async_engine as _cae
        from sqlalchemy.orm import sessionmaker as _sm

        import services.database.session_factory as _sf

        engine = _cae(
            "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
        )
        maker = _sm(engine, class_=_AS, expire_on_commit=False)

        @contextlib.asynccontextmanager
        async def _scope():
            async with maker() as s:
                yield s
                await s.commit()

        monkeypatch.setattr(_sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
        yield
        await engine.dispose()

    @pytest_asyncio.fixture(autouse=True)
    async def _cleanup_test_conversations(self):
        """#1208: remove every row created under TEST_USER_ID after each test so
        these real-DB integration tests don't accumulate orphan conversations in
        the dev database."""
        yield
        async with AsyncSessionFactory.session_scope() as session:
            conv_ids = (
                (
                    await session.execute(
                        select(ConversationDB.id).where(ConversationDB.user_id == TEST_USER_ID)
                    )
                )
                .scalars()
                .all()
            )
            if conv_ids:
                await session.execute(
                    delete(ConversationTurnDB).where(
                        ConversationTurnDB.conversation_id.in_(conv_ids)
                    )
                )
                await session.execute(
                    delete(ConversationDB).where(ConversationDB.user_id == TEST_USER_ID)
                )
                await session.commit()

    async def test_conversation_context_creation(self, conversation_manager):
        """Test basic conversation context creation and management"""
        conversation_id = "test_conv_001"

        # Save initial turn
        turn = await conversation_manager.save_conversation_turn(
            conversation_id=conversation_id,
            user_message="Create GitHub issue for login bug",
            assistant_response="I created GitHub issue #85 for the login bug.",
            entities=["#85"],
            user_id=TEST_USER_ID,
        )

        assert turn.conversation_id == conversation_id
        assert turn.turn_number == 1
        assert "GitHub issue #85" in turn.assistant_response

    async def test_anaphoric_reference_resolution_performance(self, conversation_manager):
        """Test reference resolution performance meets <150ms target"""
        conversation_id = "test_conv_002"

        # Set up conversation context with GitHub issue
        await conversation_manager.save_conversation_turn(
            conversation_id=conversation_id,
            user_message="Create GitHub issue for login bug",
            assistant_response="I created GitHub issue #85 for the login bug.",
            entities=["#85"],
            user_id=TEST_USER_ID,
        )

        # Test reference resolution with performance timing
        start_time = time.time()
        resolved_message, references = await conversation_manager.resolve_references_in_message(
            "Show me that issue again", conversation_id
        )
        end_time = time.time()

        resolution_time_ms = (end_time - start_time) * 1000

        # Performance assertion: <150ms target
        assert (
            resolution_time_ms < 150
        ), f"Resolution took {resolution_time_ms:.2f}ms, exceeds 150ms target"

        # Functionality assertions
        assert "GitHub issue #85" in resolved_message
        assert len(references) > 0
        assert references[0].entity_type == "github_issue"
        assert references[0].confidence > 0.7

    async def test_conversation_window_management(self, conversation_manager):
        """Test 10-turn context window is properly maintained (#1223: DB fallback
        now returns the most-recent N, not the oldest N)."""
        conversation_id = "test_conv_004"

        # Create 15 turns (exceeds 10-turn window)
        for i in range(15):
            await conversation_manager.save_conversation_turn(
                conversation_id=conversation_id,
                user_message=f"Message {i+1}",
                assistant_response=f"Response {i+1}",
                entities=[f"entity_{i+1}"],
                user_id=TEST_USER_ID,
            )

        # Get recent turns (#1207: manager returns domain turn lists)
        recent_turns = await conversation_manager.get_recent_turns(conversation_id, limit=10)

        # Verify the most-recent 10 turns are kept (#1208: with user_id the
        # parent conversation persists, so recent_turns is now non-empty —
        # assert it rather than guarding, restoring real window coverage).
        assert recent_turns, "expected persisted turns for the window test"
        assert len(recent_turns) <= 10
        # Should have the most-recent 10 (turns 6-15), chronological
        assert recent_turns[-1].user_message == "Message 15"
        assert recent_turns[0].user_message == "Message 6"

    async def test_redis_circuit_breaker(self, conversation_manager):
        """Test Redis circuit breaker functionality"""
        # Force Redis failures
        conversation_manager.redis_client.get = AsyncMock(
            side_effect=Exception("Redis connection failed")
        )

        conversation_id = "test_conv_005"

        # Should gracefully degrade to database-only (#1207: list API)
        turns = await conversation_manager.get_recent_turns(conversation_id)

        # Should not crash, gracefully returns a (possibly empty) list
        assert isinstance(turns, list)

        # Circuit breaker should be activated after threshold failures
        for _ in range(conversation_manager.circuit_breaker_threshold + 1):
            await conversation_manager._get_from_cache(conversation_id)

        assert conversation_manager.redis_circuit_open

    async def test_conversation_manager_stats(self, conversation_manager):
        """Test ConversationManager statistics and health monitoring"""
        stats = await conversation_manager.get_manager_stats()

        assert stats["conversation_manager"] == "active"
        assert stats["context_window_size"] == 10
        assert stats["cache_ttl"] == 300
        assert "components" in stats
        assert stats["components"]["reference_resolver"] is True

    @pytest.mark.performance
    async def test_concurrent_conversation_performance(self, conversation_manager):
        """Test performance under concurrent conversation loads"""

        async def single_conversation_flow(conv_id: str):
            """Single conversation flow for concurrency testing"""
            await conversation_manager.save_conversation_turn(
                conversation_id=conv_id,
                user_message="Create issue",
                assistant_response=f"Created issue #{conv_id[-3:]}",
                entities=[f"#{conv_id[-3:]}"],
                user_id=TEST_USER_ID,
            )

            resolved_message, references = await conversation_manager.resolve_references_in_message(
                "Show me that issue", conv_id
            )

            return resolved_message, references

        # Run 10 concurrent conversations
        start_time = time.time()
        tasks = [single_conversation_flow(f"conv_{i:03d}") for i in range(10)]
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        total_time_ms = (end_time - start_time) * 1000
        avg_time_per_conversation = total_time_ms / 10

        # Performance assertion: average <150ms per conversation under load
        assert (
            avg_time_per_conversation < 150
        ), f"Average time {avg_time_per_conversation:.2f}ms exceeds 150ms target"

        # Verify all conversations completed successfully
        assert len(results) == 10
        for resolved_message, references in results:
            assert "issue #" in resolved_message.lower()
            assert len(references) > 0


class TestRecentTurnsWindow:
    """#1207: the windowing concept lives in the manager's read/cache paths
    now (the manager-local ConversationContext aggregate was eliminated —
    the domain Conversation + turn lists express it)."""

    @pytest.mark.asyncio
    async def test_cache_write_trims_to_window(self):
        """_save_to_cache keeps at most context_window_size turns"""
        mock_client = AsyncMock()
        stored = {}

        async def _setex(key, ttl, value):
            stored[key] = value

        mock_client.setex = AsyncMock(side_effect=_setex)
        manager = ConversationManager(redis_client=mock_client, context_window_size=10)

        turns = [
            ConversationTurn(
                id=f"turn_{i}",
                conversation_id="test_001",
                turn_number=i + 1,
                user_message=f"Message {i+1}",
                assistant_response=f"Response {i+1}",
                entities=[],
                created_at=datetime.now(),
            )
            for i in range(15)  # Exceeds 10-turn window
        ]
        await manager._save_to_cache("test_001", turns)

        import json as _json

        cached = _json.loads(stored["conversation_turns:test_001"])
        assert len(cached["turns"]) == 10
        assert cached["turns"][-1]["user_message"] == "Message 15"

    @pytest.mark.asyncio
    async def test_get_recent_turns_respects_limit(self):
        """get_recent_turns slices the window to the requested limit"""
        manager = ConversationManager(redis_client=None)
        many = [
            ConversationTurn(
                id=f"turn_{i}",
                conversation_id="test_002",
                turn_number=i + 1,
                user_message=f"Message {i+1}",
                assistant_response=f"Response {i+1}",
                entities=[],
                created_at=datetime.now(),
            )
            for i in range(8)
        ]

        async def _fake_db(conversation_id):
            return many

        manager._get_from_database = _fake_db
        recent = await manager.get_recent_turns("test_002", limit=5)
        assert len(recent) == 5
        assert recent[-1].user_message == "Message 8"
