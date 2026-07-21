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
        """#1452 redo: bind this file's DB access to a per-test NullPool engine.
        The global factory's shared pool carries loop-bound connections
        abandoned by earlier sweep tests (asyncpg 'another operation is in
        progress'); NullPool holds NO connections — each operation opens and
        closes its own within the current loop, and dispose() in a mismatched
        finalizer loop is a no-op (the first redo's pooled engine died exactly
        there in CI). Live-path unchanged (the manager-on-fresh-scopes latency
        question stays with Arch)."""
        import contextlib

        from sqlalchemy.ext.asyncio import AsyncSession as _AS
        from sqlalchemy.ext.asyncio import create_async_engine as _cae
        from sqlalchemy.orm import sessionmaker as _sm
        from sqlalchemy.pool import NullPool as _NP

        import services.database.session_factory as _sf

        engine = _cae(
            "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan",
            poolclass=_NP,
        )
        maker = _sm(engine, class_=_AS, expire_on_commit=False)

        @contextlib.asynccontextmanager
        async def _scope():
            async with maker() as s:
                yield s
                await s.commit()

        monkeypatch.setattr(_sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
        yield

    @pytest.fixture(autouse=True)
    def _cleanup_test_conversations(self):
        """#1208 cleanup, SYNC edition (#1452): the async version's teardown ran
        during pytest-asyncio 0.21.1 cross-loop finalization and collided with
        in-flight connection work ('another operation is in progress'). A sync
        engine can't interleave with the event loop at all — immune by
        construction. Deletes every row created under TEST_USER_ID."""
        yield
        from sqlalchemy import create_engine, text as _text

        eng = create_engine(
            "postgresql+psycopg2://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
        )
        try:
            with eng.begin() as conn:
                ids = [
                    r[0]
                    for r in conn.execute(
                        _text("SELECT id FROM conversations WHERE user_id = :u"),
                        {"u": TEST_USER_ID},
                    )
                ]
                if ids:
                    conn.execute(
                        _text("DELETE FROM conversation_turns WHERE conversation_id = ANY(:ids)"),
                        {"ids": ids},
                    )
                    conn.execute(
                        _text("DELETE FROM conversations WHERE user_id = :u"), {"u": TEST_USER_ID}
                    )
        finally:
            eng.dispose()

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
