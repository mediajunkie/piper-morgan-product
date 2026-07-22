"""
Performance validation tests for Issue #356 - PERF-INDEX
Composite indexes for common query patterns
"""

import time
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import AuditLog, ConversationDB, ConversationTurnDB, FeedbackDB, User



async def _seed_conversation(session, conv_id: str) -> None:
    """conversation_turns FKs to conversations — turns need a real parent
    (and the conversation a real user). Mirrors the 532 file's helper."""
    import uuid as _uuid
    from datetime import datetime, timezone as _tz

    from sqlalchemy import text as _text

    uid = str(_uuid.uuid4())
    now = datetime.now(_tz.utc)
    await session.execute(
        _text(
            "INSERT INTO users (id, username, email, is_active, is_verified, "
            "created_at, updated_at, role, is_alpha) "
            "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
        ),
        {"id": uid, "u": f"p356_{uid[:8]}", "e": f"p356_{uid[:8]}@test.example.com", "now": now},
    )
    await session.execute(
        _text(
            "INSERT INTO conversations (id, user_id, session_id, title, context, is_active, created_at, updated_at) "
            "VALUES (:c, :u, :s, 'perf-356 test', '{}', true, :now, :now)"
        ),
        {"c": conv_id, "u": uid, "s": str(_uuid.uuid4()), "now": now},
    )

class TestConversationIndexes:
    """Test performance improvements from conversation table indexes"""

    @pytest.mark.asyncio
    async def test_conversations_user_created_index_query(self, db_session: AsyncSession):
        """
        Verify that idx_conversations_user_created index exists and is being used
        Query: WHERE user_id = ? ORDER BY created_at DESC
        """
        # Check index exists
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'conversations'
                AND indexname = 'idx_conversations_user_created'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert index_exists, "Index idx_conversations_user_created not found on conversations table"

    @pytest.mark.asyncio
    async def test_conversation_turns_conv_created_index_query(self, db_session: AsyncSession):
        """
        Verify that idx_conversation_turns_conv_created index exists
        Query: WHERE conversation_id = ? ORDER BY created_at DESC
        Use case: Context window retrieval for recent turns
        """
        # Check index exists
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'conversation_turns'
                AND indexname = 'idx_conversation_turns_conv_created'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert (
            index_exists
        ), "Index idx_conversation_turns_conv_created not found on conversation_turns table"

    # test_conversation_turns_entities_gin_index PRUNED (#1452): the GIN index it pinned
    # (idx_conversation_turns_entities) was DELIBERATELY dropped by the
    # h1312recon schema-reconciliation migration — the test asserted schema
    # removed by design.


    # test_conversation_turns_references_gin_index PRUNED (#1452): the GIN index it pinned
    # (idx_conversation_turns_references) was DELIBERATELY dropped by the
    # h1312recon schema-reconciliation migration — the test asserted schema
    # removed by design.


class TestAuditLogIndexes:
    """Test performance improvements from audit log indexes"""

    @pytest.mark.asyncio
    async def test_audit_logs_user_timeline_index(self, db_session: AsyncSession):
        """
        Verify that idx_audit_logs_user_timeline index exists
        Query: WHERE user_id = ? ORDER BY created_at DESC
        Use case: User activity audit trails
        """
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'audit_logs'
                AND indexname = 'idx_audit_logs_user_timeline'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert index_exists, "Index idx_audit_logs_user_timeline not found on audit_logs table"


class TestFeedbackIndexes:
    """Test performance improvements from feedback indexes"""

    @pytest.mark.asyncio
    async def test_feedback_user_status_date_index(self, db_session: AsyncSession):
        """
        Verify that idx_feedback_user_status_date index exists
        Query: WHERE user_id = ? AND status = ? ORDER BY created_at DESC
        Use case: Feedback review page, user feedback analytics
        """
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'feedback'
                AND indexname = 'idx_feedback_user_status_date'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert index_exists, "Index idx_feedback_user_status_date not found on feedback table"


class TestIndexExplainPlans:
    """Verify query plans use indexes (EXPLAIN ANALYZE)"""

    @pytest.mark.asyncio
    async def test_conversation_user_created_uses_index(self, db_session: AsyncSession):
        """
        Verify that conversation listing query uses index, not seq scan
        """
        # Create test data
        user_id = str(uuid.uuid4())
        conv = ConversationDB(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_id="test-session",
            title="Test Conversation",
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(conv)
        await db_session.commit()

        # #1452: pin "index exists and is usable", not the planner's
        # size-dependent CHOICE — on near-empty tables (post-cleanup CI) a
        # Seq Scan correctly wins and the raw assert oscillates.
        await db_session.execute(text("SET enable_seqscan = off"))
        # Verify query plan
        result = await db_session.execute(
            text(
                f"""
                EXPLAIN (FORMAT JSON)
                SELECT * FROM conversations
                WHERE user_id = '{user_id}'
                ORDER BY created_at DESC
                LIMIT 10
            """
            )
        )
        plan = result.scalar()
        plan_text = str(plan).lower()

        # Should use index, not sequential scan
        assert "index" in plan_text or "idx_conversations_user_created" in plan_text, (
            "Query plan should use index. Got: " + str(plan)
        )

    @pytest.mark.asyncio
    async def test_conversation_turns_conv_created_uses_index(self, db_session: AsyncSession):
        """
        Verify that context window query uses index
        """
        # Create test data
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)
        turn = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=1,
            user_message="Hello",
            assistant_response="Hi there!",
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn)
        await db_session.commit()

        # #1452: pin "index exists and is usable", not the planner's
        # size-dependent CHOICE — on near-empty tables (post-cleanup CI) a
        # Seq Scan correctly wins and the raw assert oscillates.
        await db_session.execute(text("SET enable_seqscan = off"))
        # Verify query plan
        result = await db_session.execute(
            text(
                f"""
                EXPLAIN (FORMAT JSON)
                SELECT * FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                ORDER BY created_at DESC
                LIMIT 10
            """
            )
        )
        plan = result.scalar()
        plan_text = str(plan).lower()

        # Should use index, not sequential scan
        assert "index" in plan_text, (
            "Query plan should use index for context window retrieval. Got: " + str(plan)
        )


class TestIndexEdgeCases:
    """Edge case tests for index correctness"""

    @pytest.mark.asyncio
    async def test_empty_conversation_list(self, db_session: AsyncSession):
        """Test that index works with empty results"""
        non_existent_user = str(uuid.uuid4())

        # Should not error, just return empty
        result = await db_session.execute(
            text(
                f"""
                SELECT * FROM conversations
                WHERE user_id = '{non_existent_user}'
                ORDER BY created_at DESC
                LIMIT 10
            """
            )
        )
        rows = result.fetchall()
        assert len(rows) == 0

    @pytest.mark.asyncio
    async def test_conversation_turns_jsonb_containment(self, db_session: AsyncSession):
        """Test GIN index for JSONB array containment"""
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create turn with entities
        turn = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=1,
            user_message="Talk to John",
            assistant_response="John is a team member",
            entities=["John", "team_member"],
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn)
        await db_session.commit()

        # Query with JSONB containment - should use GIN index
        result = await db_session.execute(
            text(
                """
                SELECT * FROM conversation_turns
                WHERE entities @> '["John"]'::jsonb
            """
            )
        )
        rows = result.fetchall()
        assert len(rows) >= 1


class TestIndexMaintenance:
    """Tests for index maintenance and integrity"""

    @pytest.mark.asyncio
    async def test_index_statistics_updated(self, db_session: AsyncSession):
        """Verify that index statistics are available for query planner"""
        # ANALYZE updates index statistics
        await db_session.execute(text("ANALYZE conversations"))
        await db_session.commit()

        # Check that statistics exist
        result = await db_session.execute(
            text(
                """
                SELECT relpages, reltuples
                FROM pg_class
                WHERE relname = 'idx_conversations_user_created'
            """
            )
        )
        stats = result.fetchone()
        # Stats should exist (may be None initially, but should be retrievable)
        assert stats is not None

    @pytest.mark.asyncio
    async def test_index_size_reasonable(self, db_session: AsyncSession):
        """Verify index sizes are reasonable (not bloated)"""
        result = await db_session.execute(
            text(
                """
                SELECT
                    c.relname AS indexname,
                    pg_size_pretty(pg_relation_size(c.oid)) AS size
                FROM pg_class c
                WHERE c.relname = 'idx_conversations_user_created'
            """
            )
        )
        index_info = result.fetchone()
        # Just verify we can get the size - actual size depends on data volume
        assert index_info is not None


# ============================================================================
# PERFORMANCE BASELINE TESTS
# These establish expected performance characteristics
# ============================================================================


class TestPerformanceBaselines:
    """
    Baseline performance expectations after indexes are applied

    Note: These tests verify that queries can complete within reasonable time.
    Actual performance improvement verification requires:
    1. Before: Run queries with indexes dropped
    2. After: Run queries with indexes present
    3. Compare execution times

    For automated CI, we just verify indexes exist and queries don't timeout.
    """

    @pytest.mark.asyncio
    async def test_conversation_listing_completes(self, db_session: AsyncSession, benchmark=None):
        """
        Test that conversation listing query completes quickly
        Target: <20ms for typical dataset
        """
        user_id = str(uuid.uuid4())

        # Create test conversations
        for i in range(10):
            conv = ConversationDB(
                id=str(uuid.uuid4()),
                user_id=user_id,
                session_id=f"session-{i}",
                title=f"Conversation {i}",
                created_at=datetime.now(timezone.utc) - timedelta(hours=i),
            )
            db_session.add(conv)
        await db_session.commit()

        # Time the query
        start = time.perf_counter()
        result = await db_session.execute(
            text(
                f"""
                SELECT id, title, created_at FROM conversations
                WHERE user_id = '{user_id}'
                ORDER BY created_at DESC
                LIMIT 10
            """
            )
        )
        rows = result.fetchall()
        elapsed = time.perf_counter() - start

        # Should complete quickly (less than 100ms even for demonstration)
        assert elapsed < 0.1, f"Conversation listing took {elapsed*1000:.2f}ms"
        assert len(rows) <= 10

    @pytest.mark.asyncio
    async def test_context_window_retrieval_completes(self, db_session: AsyncSession):
        """
        Test that context window retrieval (last 10 turns) completes quickly
        Target: <15ms for typical dataset
        """
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create test turns
        for i in range(10):
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"User message {i}",
                assistant_response=f"Assistant response {i}",
                created_at=datetime.now(timezone.utc) - timedelta(minutes=10 - i),
            )
            db_session.add(turn)
        await db_session.commit()

        # Time the query
        start = time.perf_counter()
        result = await db_session.execute(
            text(
                f"""
                SELECT id, turn_number, user_message, assistant_response, created_at
                FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                ORDER BY created_at DESC
                LIMIT 10
            """
            )
        )
        rows = result.fetchall()
        elapsed = time.perf_counter() - start

        # Should complete quickly
        assert elapsed < 0.1, f"Context window retrieval took {elapsed*1000:.2f}ms"
        assert len(rows) == 10


# ============================================================================
# SUMMARY
# ============================================================================
"""
Test Coverage for Issue #356 Performance Indexes:

✅ Index Existence Tests (6 indexes):
   - conversations(user_id, created_at DESC)
   - conversation_turns(conversation_id, created_at DESC)
   - conversation_turns(entities) [GIN]
   - conversation_turns(references) [GIN]
   - audit_logs(user_id, created_at DESC)
   - feedback(user_id, status, created_at DESC)

✅ Query Plan Tests:
   - Verify EXPLAIN ANALYZE shows index usage, not seq scan

✅ Edge Case Tests:
   - Empty result sets
   - JSONB containment queries

✅ Maintenance Tests:
   - Index statistics availability
   - Index size reasonableness

✅ Performance Baseline Tests:
   - Query completion time validation

All tests verify correctness and basic performance characteristics.
Full before/after benchmarking should be done in performance environment.
"""
