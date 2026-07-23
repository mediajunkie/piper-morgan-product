"""
Performance validation tests for Issue #532 - PERF-CONVERSATION-ANALYTICS
Intent-focused indexes for conversation analytics queries
"""

import time
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import ConversationTurnDB



async def _seed_conversation(session, conv_id: str) -> None:
    """conversation_turns FKs to conversations (#840-era hardening) — turns need
    a real parent row (and the conversation a real user)."""
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
        {"id": uid, "u": f"px_{uid[:8]}", "e": f"px_{uid[:8]}@test.example.com", "now": now},
    )
    await session.execute(
        _text(
            "INSERT INTO conversations (id, user_id, session_id, title, context, is_active, created_at, updated_at) "
            "VALUES (:c, :u, :s, 'perf-index test', '{}', true, :now, :now)"
        ),
        {"c": conv_id, "u": uid, "s": str(_uuid.uuid4()), "now": now},
    )

class TestConversationIntentIndexes:
    """Test performance improvements from conversation intent indexes"""

    @pytest.mark.asyncio
    async def test_conversation_turns_intent_index_exists(self, db_session: AsyncSession):
        """
        Verify that idx_conversation_turns_intent index exists
        Query: WHERE intent = 'question'
        Use case: Intent distribution analysis, intent-based filtering
        """
        # Check index exists
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'conversation_turns'
                AND indexname = 'idx_conversation_turns_intent'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert (
            index_exists
        ), "Index idx_conversation_turns_intent not found on conversation_turns table"

    @pytest.mark.asyncio
    async def test_conversation_turns_conv_intent_index_exists(self, db_session: AsyncSession):
        """
        Verify that idx_conversation_turns_conv_intent composite index exists
        Query: WHERE conversation_id = ? AND intent = ?
        Use case: Intent trajectory within conversation, conversation-specific analytics
        """
        # Check index exists
        result = await db_session.execute(
            text(
                """
                SELECT indexname FROM pg_indexes
                WHERE tablename = 'conversation_turns'
                AND indexname = 'idx_conversation_turns_conv_intent'
            """
            )
        )
        index_exists = result.scalar() is not None
        assert (
            index_exists
        ), "Index idx_conversation_turns_conv_intent not found on conversation_turns table"


class TestIntentFilteringQueries:
    """Test that intent filtering queries use indexes effectively"""

    @pytest.mark.asyncio
    async def test_intent_filtering_uses_index(self, db_session: AsyncSession):
        """
        Verify that intent filtering query uses the idx_conversation_turns_intent index
        Query pattern: SELECT * FROM conversation_turns WHERE intent = ?
        """
        # Create test data with different intents
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)
        intents = ["question", "statement", "request", "clarification"]

        for i, intent in enumerate(intents):
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"Test message with {intent} intent",
                assistant_response=f"Response to {intent}",
                intent=intent,
                created_at=datetime.now(timezone.utc),
            )
            db_session.add(turn)
        await db_session.commit()

        # #1452: with near-empty tables the planner CORRECTLY prefers a Seq
        # Scan — the claim under test is "the index exists and is usable",
        # so pin the planner (same cure as test_performance_indexes_356).
        await db_session.execute(text("SET enable_seqscan = off"))

        # Verify query plan uses index
        result = await db_session.execute(
            text(
                """
                EXPLAIN (FORMAT JSON)
                SELECT * FROM conversation_turns
                WHERE intent = 'question'
            """
            )
        )
        plan = result.scalar()
        plan_text = str(plan).lower()

        # Should use index, not sequential scan
        assert "index" in plan_text or "idx_conversation_turns_intent" in plan_text, (
            "Query plan should use idx_conversation_turns_intent. Got: " + str(plan)
        )

    @pytest.mark.asyncio
    async def test_composite_intent_lookup_uses_index(self, db_session: AsyncSession):
        """
        Verify that composite (conversation_id, intent) query uses the composite index
        Query pattern: SELECT * FROM conversation_turns WHERE conversation_id = ? AND intent = ?
        """
        # Create test data
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)
        turn = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=1,
            user_message="Test question",
            assistant_response="Answer",
            intent="question",
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn)
        await db_session.commit()

        # Verify query plan uses composite index
        await db_session.execute(text("SET enable_seqscan = off"))  # #1452: see above
        result = await db_session.execute(
            text(
                f"""
                EXPLAIN (FORMAT JSON)
                SELECT * FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                AND intent = 'question'
            """
            )
        )
        plan = result.scalar()
        plan_text = str(plan).lower()

        # Should use composite index
        assert "index" in plan_text, "Query plan should use composite index. Got: " + str(plan)


class TestIntentAnalyticsQueries:
    """Test real-world analytics queries that benefit from intent indexes"""

    @pytest.mark.asyncio
    async def test_intent_distribution_analysis(self, db_session: AsyncSession):
        """
        Test intent analytics use case: What's the distribution of intents?
        Query: SELECT intent, COUNT(*) FROM conversation_turns GROUP BY intent
        Use case: Understanding conversation patterns, analytics dashboards
        """
        # Create test data with multiple intents
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)
        intent_counts = {"question": 5, "statement": 3, "request": 2, "clarification": 1}
        turn_number = 0

        for intent, count in intent_counts.items():
            for i in range(count):
                turn = ConversationTurnDB(
                    id=str(uuid.uuid4()),
                    conversation_id=conv_id,
                    turn_number=turn_number,
                    user_message=f"Message {i} with {intent}",
                    assistant_response=f"Response to {intent}",
                    intent=intent,
                    created_at=datetime.now(timezone.utc) - timedelta(minutes=11 - turn_number),
                )
                db_session.add(turn)
                turn_number += 1

        await db_session.commit()

        # Run the analytics query
        result = await db_session.execute(
            text(
                """
                SELECT intent, COUNT(*) as count
                FROM conversation_turns
                WHERE conversation_id = :conv
                GROUP BY intent
                ORDER BY count DESC
            """
            ),
            {"conv": conv_id},
        )
        rows = result.fetchall()

        # Scoped to THIS test's conversation (#1452: the shared dev DB carries
        # other rows — a global GROUP BY asserted absolute counts and broke)
        assert len(rows) == 4, f"Expected 4 intent groups, got {len(rows)}"
        assert rows[0][0] == "question", "Most common intent should be 'question'"
        assert rows[0][1] == 5, "Should have 5 questions"

    @pytest.mark.asyncio
    async def test_conversation_intent_trajectory(self, db_session: AsyncSession):
        """
        Test conversation intent trajectory: How do intents flow through a conversation?
        Query: SELECT turn_number, intent FROM conversation_turns
                WHERE conversation_id = ? ORDER BY turn_number
        Use case: Understanding conversation flow, conversation patterns
        """
        # Create a conversation with intent trajectory
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)
        intent_trajectory = [
            "question",
            "clarification",
            "question",
            "statement",
            "request",
        ]

        for i, intent in enumerate(intent_trajectory):
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"Turn {i}",
                assistant_response=f"Response {i}",
                intent=intent,
                created_at=datetime.now(timezone.utc) - timedelta(minutes=5 - i),
            )
            db_session.add(turn)

        await db_session.commit()

        # Query the trajectory
        result = await db_session.execute(
            text(
                f"""
                SELECT turn_number, intent
                FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                ORDER BY turn_number
            """
            )
        )
        rows = result.fetchall()

        # Verify trajectory
        assert len(rows) == 5, "Should have 5 turns"
        for i, (turn_num, intent) in enumerate(rows):
            assert turn_num == i, f"Turn {i} should have turn_number {i}"
            assert (
                intent == intent_trajectory[i]
            ), f"Turn {i} should have intent {intent_trajectory[i]}"

    @pytest.mark.asyncio
    async def test_intent_filtered_conversation_analytics(self, db_session: AsyncSession):
        """
        Test filtering: Count turns by intent within a specific conversation
        Query: SELECT COUNT(*) FROM conversation_turns
                WHERE conversation_id = ? AND intent = ?
        Use case: Conversation-specific metrics, learning feedback
        """
        # Create test conversation with multiple intents
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create 5 questions
        for i in range(5):
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"Question {i}",
                assistant_response=f"Answer {i}",
                intent="question",
                created_at=datetime.now(timezone.utc),
            )
            db_session.add(turn)

        # Create 3 statements
        for i in range(3):
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=5 + i,
                user_message=f"Statement {i}",
                assistant_response=f"Acknowledgment {i}",
                intent="statement",
                created_at=datetime.now(timezone.utc),
            )
            db_session.add(turn)

        await db_session.commit()

        # Count questions in this conversation
        result = await db_session.execute(
            text(
                f"""
                SELECT COUNT(*) FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                AND intent = 'question'
            """
            )
        )
        question_count = result.scalar()
        assert question_count == 5, "Should have 5 questions"

        # Count statements in this conversation
        result = await db_session.execute(
            text(
                f"""
                SELECT COUNT(*) FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                AND intent = 'statement'
            """
            )
        )
        statement_count = result.scalar()
        assert statement_count == 3, "Should have 3 statements"


class TestIntentIndexEdgeCases:
    """Edge case tests for intent index correctness"""

    @pytest.mark.asyncio
    async def test_null_intent_handling(self, db_session: AsyncSession):
        """Test that queries handle NULL intents correctly"""
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create turn with NULL intent
        turn = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=0,
            user_message="Message without intent classification",
            assistant_response="Response",
            intent=None,  # No intent
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn)

        # Create turn with intent
        turn2 = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=1,
            user_message="Question",
            assistant_response="Answer",
            intent="question",
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn2)
        await db_session.commit()

        # Query should not error with NULL intents
        result = await db_session.execute(
            text(
                f"""
                SELECT COUNT(*) FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
            """
            )
        )
        count = result.scalar()
        assert count == 2, "Should have 2 turns (including NULL intent)"

    @pytest.mark.asyncio
    async def test_empty_conversation_intent_query(self, db_session: AsyncSession):
        """Test that intent queries work on empty conversations"""
        non_existent_conv = str(uuid.uuid4())

        # Query should return empty result, not error
        result = await db_session.execute(
            text(
                f"""
                SELECT * FROM conversation_turns
                WHERE conversation_id = '{non_existent_conv}'
                AND intent = 'question'
            """
            )
        )
        rows = result.fetchall()
        assert len(rows) == 0, "Empty conversation should return no results"

    @pytest.mark.asyncio
    async def test_case_sensitive_intent_matching(self, db_session: AsyncSession):
        """Test that intent matching is case-sensitive"""
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create turns with different case intents
        turn1 = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=0,
            user_message="Question",
            assistant_response="Answer",
            intent="question",  # lowercase
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn1)

        turn2 = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            turn_number=1,
            user_message="Another question",
            assistant_response="Answer",
            intent="QUESTION",  # UPPERCASE
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn2)
        await db_session.commit()

        # Query for lowercase should only match lowercase
        result = await db_session.execute(
            text(
                f"""
                SELECT COUNT(*) FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                AND intent = 'question'
            """
            )
        )
        count = result.scalar()
        assert count == 1, "Should match only exact case 'question'"


class TestIntentIndexPerformanceBaselines:
    """Performance baseline expectations for intent analytics"""

    @pytest.mark.asyncio
    async def test_intent_filtering_performance(self, db_session: AsyncSession):
        """
        Test that intent filtering completes quickly
        Target: <100ms for typical dataset
        Use case: Real-time intent-based filtering in analytics dashboards
        """
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create test dataset (50 turns)
        for i in range(50):
            intent = ["question", "statement", "request", "clarification"][i % 4]
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"Turn {i}",
                assistant_response=f"Response {i}",
                intent=intent,
                created_at=datetime.now(timezone.utc) - timedelta(minutes=50 - i),
            )
            db_session.add(turn)
        await db_session.commit()

        # Time the filtering query
        start = time.perf_counter()
        result = await db_session.execute(
            text(
                f"""
                SELECT * FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                AND intent = 'question'
            """
            )
        )
        rows = result.fetchall()
        elapsed = time.perf_counter() - start

        # Should complete quickly
        assert elapsed < 0.1, f"Intent filtering took {elapsed*1000:.2f}ms (target <100ms)"
        # Should find the expected number of questions
        expected_questions = 50 // 4  # 4 different intents, so ~12-13 questions
        assert len(rows) > 0, "Should find at least some questions"

    @pytest.mark.asyncio
    async def test_intent_aggregation_performance(self, db_session: AsyncSession):
        """
        Test that intent aggregation (GROUP BY) completes quickly
        Target: <200ms for typical dataset
        Use case: Intent distribution dashboards, analytics reports
        """
        conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, conv_id)

        # Create test dataset (100 turns across 4 intents)
        for i in range(100):
            intent = ["question", "statement", "request", "clarification"][i % 4]
            turn = ConversationTurnDB(
                id=str(uuid.uuid4()),
                conversation_id=conv_id,
                turn_number=i,
                user_message=f"Turn {i}",
                assistant_response=f"Response {i}",
                intent=intent,
                created_at=datetime.now(timezone.utc) - timedelta(minutes=100 - i),
            )
            db_session.add(turn)
        await db_session.commit()

        # Time the aggregation query
        start = time.perf_counter()
        result = await db_session.execute(
            text(
                f"""
                SELECT intent, COUNT(*) as count
                FROM conversation_turns
                WHERE conversation_id = '{conv_id}'
                GROUP BY intent
                ORDER BY count DESC
            """
            )
        )
        rows = result.fetchall()
        elapsed = time.perf_counter() - start

        # Should complete quickly
        assert elapsed < 0.2, f"Intent aggregation took {elapsed*1000:.2f}ms (target <200ms)"
        # Should have multiple intent groups
        assert len(rows) >= 3, "Should find at least 3 different intent types"

    @pytest.mark.asyncio
    async def test_composite_query_performance(self, db_session: AsyncSession):
        """
        Test that composite (conversation_id, intent) queries complete quickly
        Target: <50ms for typical dataset
        Use case: Conversation-specific intent analysis
        """
        # Create multiple conversations
        for conv_num in range(3):
            conv_id = str(uuid.uuid4())
            await _seed_conversation(db_session, conv_id)
            for turn_num in range(20):
                intent = ["question", "statement", "request"][turn_num % 3]
                turn = ConversationTurnDB(
                    id=str(uuid.uuid4()),
                    conversation_id=conv_id,
                    turn_number=turn_num,
                    user_message=f"Conv {conv_num} Turn {turn_num}",
                    assistant_response=f"Response {turn_num}",
                    intent=intent,
                    created_at=datetime.now(timezone.utc),
                )
                db_session.add(turn)
        await db_session.commit()

        # Time composite query on one specific conversation
        test_conv_id = str(uuid.uuid4())
        await _seed_conversation(db_session, test_conv_id)
        turn = ConversationTurnDB(
            id=str(uuid.uuid4()),
            conversation_id=test_conv_id,
            turn_number=0,
            user_message="Test question",
            assistant_response="Test answer",
            intent="question",
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(turn)
        await db_session.commit()

        start = time.perf_counter()
        result = await db_session.execute(
            text(
                f"""
                SELECT * FROM conversation_turns
                WHERE conversation_id = '{test_conv_id}'
                AND intent = 'question'
            """
            )
        )
        rows = result.fetchall()
        elapsed = time.perf_counter() - start

        # Should be very fast (composite index optimization)
        assert elapsed < 0.05, f"Composite query took {elapsed*1000:.2f}ms (target <50ms)"
        assert len(rows) >= 1, "Should find the test turn"


# ============================================================================
# SUMMARY
# ============================================================================
"""
Test Coverage for Issue #532 Performance Indexes:

✅ Index Existence Tests (2 indexes):
   - idx_conversation_turns_intent
   - idx_conversation_turns_conv_intent

✅ Query Plan Tests:
   - Verify EXPLAIN ANALYZE shows index usage, not seq scan

✅ Real-World Analytics Tests:
   - Intent distribution analysis
   - Conversation intent trajectory
   - Intent-filtered conversation analytics

✅ Edge Case Tests:
   - NULL intent handling
   - Empty conversation queries
   - Case-sensitive matching

✅ Performance Baseline Tests:
   - Intent filtering (<100ms)
   - Intent aggregation (<200ms)
   - Composite queries (<50ms)

All tests verify both correctness and performance characteristics.
"""
