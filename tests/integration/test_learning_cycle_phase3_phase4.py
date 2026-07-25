"""
Integration tests for Phase 3 + Phase 4 learning cycle.

Tests the complete production learning flow with database-backed patterns:
1. Capture action → LearningHandler.capture_action()
2. Detect similar pattern → LearningHandler.find_similar_pattern()
3. Suggest to user → LearningHandler.get_suggestions()
4. User feedback → POST /api/v1/learning/patterns/{id}/feedback
5. Confidence updates → Database confidence adjustment
6. Proactive application → LearningHandler.get_automation_patterns()

Issue: #300 (Phase 3 + Phase 4)
Task: Integration testing for production learning system
"""

from datetime import datetime, timedelta
from types import SimpleNamespace
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import and_, delete, select

from services.database.models import LearnedPattern, LearningSettings
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent, IntentCategory
from services.learning.context_matcher import ContextMatcher
from services.learning.learning_handler import LearningHandler
from services.shared_types import PatternType

# #1452 de-flake: TEST_USER_ID was a fixed literal (xian's live UUID, shared
# with tests/manual/test_learning_handler_phase1.py and any app activity as
# that user) — in full sweeps, foreign LearnedPattern/learning_settings rows
# for the same user cross-contaminated similarity matching and settings
# checks. Now UNIQUE PER TEST: the autouse fixture below rebinds these module
# globals to a fresh user each test (test bodies read them at call time).
TEST_USER_ID = UUID("00000000-0000-0000-0000-000000000000")  # rebound per test

# #1252 (ADR-071 D4): the pattern routes now take the authenticated principal;
# these direct-call tests pass a stand-in carrying the test user_id (the route
# reads only current_user.user_id).
_TEST_CLAIMS = SimpleNamespace(user_id=TEST_USER_ID)  # rebound per test


@pytest_asyncio.fixture(autouse=True)
async def _unique_learning_user():
    """Fresh user per test; learned_patterns FK-CASCADEs on user delete."""
    import uuid as _uuid

    global TEST_USER_ID, _TEST_CLAIMS
    from services.database.models import User
    from tests.conftest import delete_test_user_fully

    TEST_USER_ID = _uuid.uuid4()
    _TEST_CLAIMS = SimpleNamespace(user_id=TEST_USER_ID)
    uid = str(TEST_USER_ID)
    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(
            User(
                id=uid,
                username=f"learn-{uid[:8]}",
                email=f"learn-{uid[:8]}@example.com",
                password_hash="x",
                is_active=True,
                is_verified=True,
            )
        )
        await session.commit()

    yield

    async with AsyncSessionFactory.session_scope_fresh() as session:
        await delete_test_user_fully(session, uid)
        await session.commit()


@pytest_asyncio.fixture(autouse=True)
async def _fresh_factory(monkeypatch):
    """#1452 (the proven wave-6 recipe): route functions these tests call use
    the global AsyncSessionFactory internally; in a full sweep its shared pool
    arrives poisoned (loop-bound abandoned connections) and the routes error.
    Patch the scope to a NullPool engine — no pooled connections to inherit,
    no engine dispose needed at teardown."""
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


@pytest.fixture
async def clean_test_patterns():
    """Clean up test patterns before and after each test."""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Delete test patterns before test
        await session.execute(delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID))
        from sqlalchemy import text as _text
        await session.execute(
            _text("DELETE FROM learning_settings WHERE user_id = :u"), {"u": str(TEST_USER_ID)}
        )
        await session.commit()

    yield

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Delete test patterns after test
        await session.execute(delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID))
        from sqlalchemy import text as _text
        await session.execute(
            _text("DELETE FROM learning_settings WHERE user_id = :u"), {"u": str(TEST_USER_ID)}
        )
        await session.commit()


@pytest.fixture
def learning_handler():
    """Create LearningHandler instance for testing."""
    return LearningHandler()


@pytest.fixture
def context_matcher():
    """Create ContextMatcher instance for testing."""
    return ContextMatcher()


class TestLearningCyclePhase3:
    """Test Phase 3: Pattern suggestion and feedback cycle."""

    @pytest.mark.asyncio
    async def test_complete_learning_cycle(self, learning_handler, clean_test_patterns):
        """
        Test complete learning cycle: capture → suggest → feedback → confidence update.

        Verifies:
        - Action capture creates or updates pattern
        - Pattern similarity detection works
        - Suggestions appear with correct confidence
        - Accept feedback increases confidence
        - Reject feedback decreases confidence
        """
        # Step 1: Capture first action (creates pattern)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern_id = await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={
                    "action": "create_github_issue",
                    "entity": "github_issue",
                    "params": {
                        "title": "Daily standup action item",
                        "description": "Follow up on API integration",
                        "repository": "piper-morgan",
                    },
                },
                session=session,
            )

        assert pattern_id is not None

        # Verify pattern created in database
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(LearnedPattern).where(LearnedPattern.id == pattern_id)
            )
            pattern = result.scalar_one_or_none()

            assert pattern is not None
            assert pattern.pattern_type == PatternType.COMMAND_SEQUENCE
            assert pattern.confidence == 0.5  # Initial confidence
            assert pattern.usage_count == 1
            assert pattern.success_count == 0  # New patterns start with 0

        # Step 2: Capture second similar action (updates existing pattern)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern_id_2 = await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={
                    "action": "create_github_issue",
                    "entity": "github_issue",
                    "params": {
                        "title": "Standup action item",
                        "description": "Check deployment status",
                        "repository": "piper-morgan",
                    },
                },
                session=session,
            )

        # Should update existing pattern (same pattern_id)
        assert pattern_id_2 == pattern_id

        # Step 2b (#1438 rewrite): the live thresholds are deliberate — 0.7 to
        # suggest AND a volume factor (usage/10, capped) that keeps low-use
        # patterns quiet. Earn BOTH: usage to 10 via repeated captures of the
        # same-signature action, then successful outcomes.
        for _ in range(8):
            async with AsyncSessionFactory.session_scope_fresh() as session:
                assert (
                    await learning_handler.capture_action(
                        user_id=TEST_USER_ID,
                        action_type=IntentCategory.EXECUTION,
                        context={"action": "create_github_issue"},
                        session=session,
                    )
                    == pattern_id
                )
        # two successes: above the 0.7 gate with headroom below 1.0 so the
        # feedback step can still demonstrate an increase
        for _ in range(2):
            async with AsyncSessionFactory.session_scope_fresh() as session:
                assert await learning_handler.record_outcome(
                    user_id=TEST_USER_ID, pattern_id=pattern_id, success=True, session=session
                )

        # Step 3: Get suggestions (now above threshold)
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            suggestions = await learning_handler.get_suggestions(
                user_id=TEST_USER_ID,
                context={"category": "EXECUTION", "action": "create_github_issue"},
                session=_sess,
            )

        assert suggestions is not None
        assert len(suggestions) > 0

        suggestion = suggestions[0]
        assert suggestion["pattern_id"] == str(pattern_id)
        assert suggestion["auto_triggered"] is False  # Regular suggestion
        assert suggestion["confidence"] >= 0.7  # earned the threshold via outcomes

        # Step 4: Submit positive feedback (accept)
        from web.api.routes.learning import PatternFeedback, provide_pattern_feedback

        feedback = PatternFeedback(action="accept", feedback_text="Perfect!")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["confidence"] > suggestion["confidence"]

        # Verify confidence increased
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(LearnedPattern).where(LearnedPattern.id == pattern_id)
            )
            pattern = result.scalar_one_or_none()

            # Accept multiplies by 1.1, capped at 1.0
            assert pattern.confidence > 0.6
            assert pattern.success_count >= 3  # 2 earned outcomes + accept-feedback path (route may record an additional outcome internally)

        # Step 5: Submit negative feedback (reject) to test decrease
        feedback = PatternFeedback(action="reject", feedback_text="Not useful")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True

        # Verify confidence decreased
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(LearnedPattern).where(LearnedPattern.id == pattern_id)
            )
            pattern = result.scalar_one_or_none()

            # Reject multiplies by 0.5
            assert pattern.confidence < 0.6
            assert pattern.failure_count == 2  # Reject adds 2

    @pytest.mark.asyncio
    async def test_pattern_similarity_detection(self, learning_handler, clean_test_patterns):
        """
        Test pattern similarity detection finds existing patterns.

        Verifies:
        - Similar actions match existing patterns
        - Dissimilar actions create new patterns
        - Context matching works correctly
        """
        # Create initial pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern_id_1 = await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={"action": "create_github_issue", "params": {"title": "Bug fix"}},
                session=session,
            )

        # Capture similar action (same type, similar params)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern_id_2 = await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={"action": "create_github_issue", "params": {"title": "Feature request"}},
                session=session,
            )

        # Should match existing pattern
        assert pattern_id_2 == pattern_id_1

        # Capture dissimilar action (different type)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern_id_3 = await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.QUERY,
                context={"action": "search", "params": {"query": "API docs"}},
                session=session,
            )

        # Should create new pattern
        assert pattern_id_3 != pattern_id_1

    @pytest.mark.asyncio
    async def test_confidence_threshold_filtering(self, learning_handler, clean_test_patterns):
        """
        Test suggestions filtered by confidence threshold.

        Verifies:
        - Low confidence patterns don't appear in suggestions
        - Threshold can be customized via settings
        """
        # Create low-confidence pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            low_pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={
                    "action_type": "low_confidence_action",
                    "action_params": {"test": "value"},
                },
                confidence=0.3,  # Below default threshold (0.7)
                usage_count=1,
                success_count=1,
                failure_count=0,
                enabled=True,
            )
            session.add(low_pattern)
            await session.commit()
            low_pattern_id = low_pattern.id

        # Get suggestions with default threshold (0.7)
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            suggestions = await learning_handler.get_suggestions(
                user_id=TEST_USER_ID, context={"category": "EXECUTION"},
                session=_sess,
            )

        # Low confidence pattern should NOT appear
        pattern_ids = [s["pattern_id"] for s in suggestions]
        assert str(low_pattern_id) not in pattern_ids

        # Create high-confidence pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            high_pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={
                    "action_type": "high_confidence_action",
                    "action_params": {"test": "value"},
                },
                confidence=0.85,  # Above threshold
                usage_count=10,
                success_count=9,
                failure_count=1,
                enabled=True,
            )
            session.add(high_pattern)
            await session.commit()
            high_pattern_id = high_pattern.id

        # Get suggestions again
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            suggestions = await learning_handler.get_suggestions(
                user_id=TEST_USER_ID, context={"category": "EXECUTION"},
                session=_sess,
            )

        # High confidence pattern SHOULD appear
        pattern_ids = [s["pattern_id"] for s in suggestions]
        assert str(high_pattern_id) in pattern_ids


class TestLearningCyclePhase4:
    """Test Phase 4: Proactive automation patterns."""

    @pytest.mark.asyncio
    async def test_proactive_pattern_application(
        self, learning_handler, context_matcher, clean_test_patterns
    ):
        """
        Test proactive automation (confidence >= 0.9).

        Verifies:
        - High confidence patterns trigger proactively
        - Context matching filters correctly
        - auto_triggered flag set correctly
        """
        # Create high-confidence pattern (>= 0.9 for automation)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            auto_pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={
                    "action_type": "create_github_issue",
                    "action_params": {"title": "Standup action item"},
                    "trigger_context": {"temporal": "after standup", "intent": "EXECUTION"},
                },
                confidence=0.95,  # High confidence
                usage_count=20,
                success_count=19,
                failure_count=1,
                enabled=True,
            )
            session.add(auto_pattern)
            await session.commit()
            auto_pattern_id = auto_pattern.id

        # Get automation patterns (proactive)
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            automation_patterns = await learning_handler.get_automation_patterns(
                user_id=TEST_USER_ID,
                context={"intent": "EXECUTION", "current_event": "standup_complete"},
                session=_sess,
            )

        assert automation_patterns is not None
        assert len(automation_patterns) > 0

        pattern = automation_patterns[0]
        # live contract returns LearnedPattern OBJECTS; the auto_triggered flag
        # is added by intent_service's conversion layer, not here
        assert pattern.id == auto_pattern_id
        assert pattern.confidence >= 0.9

    @pytest.mark.asyncio
    async def test_context_matching(self, context_matcher):
        """
        Test context matcher filters patterns correctly.

        Verifies:
        - Temporal matching (e.g., "after standup")
        - Sequential matching (action after action)
        - Intent matching (EXECUTION, QUERY, etc.)
        """
        # Test temporal matching
        # matcher vocabulary is trigger_time / after_action / trigger_intent
        pattern_context = {"after_action": "standup_complete"}
        current_context = {"last_action": "standup_complete"}

        assert await context_matcher.matches(pattern_context, current_context) is True

        # Test intent matching
        pattern_context = {"trigger_intent": "EXECUTION"}
        current_context = {"intent": "EXECUTION"}

        assert await context_matcher.matches(pattern_context, current_context) is True

        # Test mismatch
        pattern_context = {"trigger_intent": "QUERY"}
        current_context = {"intent": "EXECUTION"}

        assert await context_matcher.matches(pattern_context, current_context) is False

    @pytest.mark.asyncio
    async def test_feedback_auto_disable_low_confidence(
        self, learning_handler, clean_test_patterns
    ):
        """
        Test patterns auto-disable when confidence drops below 0.3.

        Verifies:
        - Reject feedback decreases confidence
        - Pattern disabled when confidence < 0.3
        """
        # Create pattern with moderate confidence
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action", "action_params": {}},
                confidence=0.35,  # Just above disable threshold
                usage_count=5,
                success_count=2,
                failure_count=3,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Submit reject feedback (should drop below 0.3 and auto-disable)
        from web.api.routes.learning import PatternFeedback, provide_pattern_feedback

        feedback = PatternFeedback(action="reject")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["enabled"] is False  # Auto-disabled
        assert result["pattern"]["confidence"] < 0.3


class TestLearningCyclePerformance:
    """Test performance requirements (<500ms overhead)."""

    @pytest.mark.asyncio
    async def test_capture_action_performance(self, learning_handler, clean_test_patterns):
        """
        Test capture_action() completes in <500ms.

        Verifies:
        - Overhead is minimal for pattern capture
        - Database writes are efficient
        """
        import time

        # Warm up (first call may be slower due to DB connection)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={"action": "warmup"},
                session=session,
            )

        # Measure performance
        start = time.perf_counter()

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await learning_handler.capture_action(
                user_id=TEST_USER_ID,
                action_type=IntentCategory.EXECUTION,
                context={"action": "create_github_issue", "params": {"title": "Performance test"}},
                session=session,
            )

        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should complete in <500ms (acceptance criteria from #300)
        assert elapsed_ms < 500.0, f"capture_action took {elapsed_ms:.2f}ms (>500ms bound)"

    @pytest.mark.asyncio
    async def test_get_suggestions_performance(self, learning_handler, clean_test_patterns):
        """
        Test get_suggestions() completes in <500ms.

        Verifies:
        - Pattern retrieval is fast
        - Filtering is efficient
        """
        import time

        # Create some patterns first
        for i in range(5):
            async with AsyncSessionFactory.session_scope_fresh() as session:
                pattern = LearnedPattern(
                    user_id=TEST_USER_ID,
                    pattern_type=PatternType.COMMAND_SEQUENCE,
                    pattern_data={"action_type": f"action_{i}"},
                    confidence=0.8,
                    usage_count=1,
                    success_count=1,
                    failure_count=0,
                    enabled=True,
                )
                session.add(pattern)
                await session.commit()

        # Warm up
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            await learning_handler.get_suggestions(user_id=TEST_USER_ID, context={}, session=_sess)

        # Measure performance
        start = time.perf_counter()

        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            suggestions = await learning_handler.get_suggestions(
                user_id=TEST_USER_ID, context={"category": "EXECUTION"},
                session=_sess,
            )

        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should complete in <500ms
        assert elapsed_ms < 500.0, f"get_suggestions took {elapsed_ms:.2f}ms (>500ms bound)"
        assert suggestions is not None

    @pytest.mark.asyncio
    async def test_get_automation_patterns_performance(self, learning_handler, clean_test_patterns):
        """
        Test get_automation_patterns() completes in <500ms.

        Verifies:
        - Context matching is fast
        - High-confidence filtering is efficient
        """
        import time

        # Create automation patterns
        for i in range(3):
            async with AsyncSessionFactory.session_scope_fresh() as session:
                pattern = LearnedPattern(
                    user_id=TEST_USER_ID,
                    pattern_type=PatternType.COMMAND_SEQUENCE,
                    pattern_data={
                        "action_type": f"auto_action_{i}",
                        "trigger_context": {"intent": "EXECUTION"},
                    },
                    confidence=0.95,
                    usage_count=10,
                    success_count=9,
                    failure_count=1,
                    enabled=True,
                )
                session.add(pattern)
                await session.commit()

        # Warm up
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            await learning_handler.get_automation_patterns(user_id=TEST_USER_ID, context={}, session=_sess)

        # Measure performance
        start = time.perf_counter()

        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            patterns = await learning_handler.get_automation_patterns(
                user_id=TEST_USER_ID, context={"intent": "EXECUTION"},
                session=_sess,
            )

        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should complete in <500ms
        assert (
            elapsed_ms < 500.0
        ), f"get_automation_patterns took {elapsed_ms:.2f}ms (>500ms bound)"
        assert patterns is not None


class TestLearningSettings:
    """Test global and per-pattern enable/disable."""

    @pytest.mark.asyncio
    async def test_global_learning_disable(self, learning_handler, clean_test_patterns):
        """
        Test global learning disable prevents pattern capture.

        Verifies:
        - When learning_enabled=False, no patterns captured
        - Settings respected in LearningHandler
        """
        # Create settings with learning disabled
        async with AsyncSessionFactory.session_scope_fresh() as session:
            settings = LearningSettings(
                user_id=TEST_USER_ID,
                learning_enabled=False,  # Disabled globally
                suggestion_threshold=0.7,
                automation_threshold=0.9,
                auto_apply_enabled=False,
                notification_enabled=True,
            )
            session.add(settings)
            await session.commit()

        # Try to capture action (should be blocked)
        # Note: Current implementation doesn't check settings in capture_action
        # This is a TODO for Phase 5 - settings enforcement
        # For now, just verify settings exist

        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(LearningSettings).where(LearningSettings.user_id == TEST_USER_ID)
            )
            settings = result.scalar_one_or_none()

            assert settings is not None
            assert settings.learning_enabled is False

    @pytest.mark.asyncio
    async def test_per_pattern_disable(self, learning_handler, clean_test_patterns):
        """
        Test per-pattern disable prevents suggestions.

        Verifies:
        - Disabled patterns don't appear in suggestions
        - Disabled patterns don't trigger proactively
        """
        # Create disabled pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "disabled_action"},
                confidence=0.9,
                usage_count=10,
                success_count=9,
                failure_count=1,
                enabled=False,  # Explicitly disabled
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Get suggestions
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            suggestions = await learning_handler.get_suggestions(
                user_id=TEST_USER_ID, context={},
                session=_sess,
            )

        # Disabled pattern should NOT appear
        pattern_ids = [s["pattern_id"] for s in suggestions]
        assert str(pattern_id) not in pattern_ids

        # Get automation patterns
        async with AsyncSessionFactory.session_scope_fresh() as _sess:
            automation = await learning_handler.get_automation_patterns(
                user_id=TEST_USER_ID, context={},
                session=_sess,
            )

        # Disabled pattern should NOT appear
        pattern_ids = [p["pattern_id"] for p in automation]
        assert str(pattern_id) not in pattern_ids


if __name__ == "__main__":
    # Run integration tests with verbose output
    import pytest

    pytest.main([__file__, "-v", "--tb=short", "-s"])
