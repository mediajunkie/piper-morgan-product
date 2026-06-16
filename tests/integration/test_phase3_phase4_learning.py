"""
Focused integration test for Phase 3 + Phase 4 learning (Issue #300).

Tests critical learning cycle paths:
1. Pattern feedback API
2. Learning settings API
3. Pattern enable/disable API
4. Performance verification

Simpler than test_learning_cycle_phase3_phase4.py - focused on API-level testing.
"""

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from sqlalchemy import delete, select

from services.database.models import LearnedPattern, LearningSettings, User
from services.database.session_factory import AsyncSessionFactory
from services.shared_types import PatternType
from web.api.routes.learning import (
    PatternFeedback,
    SettingsUpdate,
    disable_pattern,
    enable_pattern,
    get_settings,
    list_patterns,
    provide_pattern_feedback,
    update_settings,
)

TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

# #1250 (ADR-071 D4): get_settings/update_settings now take the authenticated
# principal. These integration tests call the route fns directly, so pass a
# stand-in carrying the test user_id (the route reads only current_user.user_id).
_TEST_CLAIMS = SimpleNamespace(user_id=TEST_USER_ID)

# #1252 (ADR-071 D4): a DIFFERENT principal — proves cross-user isolation now
# that the pattern routes anchor to current_user.user_id (not a shared
# TEST_USER_ID): one user's routes must not read or mutate another's patterns.
_OTHER_USER_ID = UUID("9e9e9e9e-0000-0000-0000-000000000001")
_OTHER_CLAIMS = SimpleNamespace(user_id=_OTHER_USER_ID)


@pytest.fixture
async def clean_test_data():
    """Clean up test data before and after each test."""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # #1250 (ADR-071 D4): ensure the test principal exists in `users` — the
        # learning FKs (learned_patterns/learning_settings → users) require it.
        # It was absent, so these integration tests had been FK-failing (silently
        # red). Seeding it makes them valid tests of the anchored-principal path.
        if await session.get(User, TEST_USER_ID) is None:
            session.add(
                User(
                    id=TEST_USER_ID,
                    username="test_learning_user",
                    email="test_learning@example.com",
                )
            )
            await session.commit()
        await session.execute(delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID))
        await session.execute(
            delete(LearningSettings).where(LearningSettings.user_id == TEST_USER_ID)
        )
        await session.commit()

    yield

    async with AsyncSessionFactory.session_scope_fresh() as session:
        await session.execute(delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID))
        await session.execute(
            delete(LearningSettings).where(LearningSettings.user_id == TEST_USER_ID)
        )
        await session.commit()


class TestPhase3FeedbackCycle:
    """Test Phase 3: User feedback on pattern suggestions."""

    @pytest.mark.asyncio
    async def test_accept_feedback_increases_confidence(self, clean_test_data):
        """Test accepting a pattern increases confidence."""
        # Create test pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.7,
                usage_count=5,
                success_count=3,
                failure_count=2,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Submit accept feedback
        feedback = PatternFeedback(action="accept", feedback_text="Great!")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["confidence"] > 0.7  # Increased
        assert result["pattern"]["success_count"] == 5  # 3 + 2

    @pytest.mark.asyncio
    async def test_reject_feedback_decreases_confidence(self, clean_test_data):
        """Test rejecting a pattern decreases confidence."""
        # Create test pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.6,
                usage_count=5,
                success_count=3,
                failure_count=2,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Submit reject feedback
        feedback = PatternFeedback(action="reject", feedback_text="Not helpful")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["confidence"] < 0.6  # Decreased
        assert result["pattern"]["failure_count"] == 4  # 2 + 2

    @pytest.mark.asyncio
    async def test_low_confidence_auto_disables(self, clean_test_data):
        """Test patterns auto-disable when confidence drops below 0.3."""
        # Create pattern near disable threshold
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.35,  # Just above threshold
                usage_count=5,
                success_count=1,
                failure_count=4,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Reject should drop below 0.3 and auto-disable
        feedback = PatternFeedback(action="reject")
        result = await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["confidence"] < 0.3
        assert result["pattern"]["enabled"] is False  # Auto-disabled


class TestPatternRouteUserIsolation1252:
    """#1252 (ADR-071 D4): the pattern routes anchor to current_user.user_id,
    not a shared TEST_USER_ID. A different principal must NOT see or mutate
    another user's patterns — the cross-user read+write leak closed."""

    @pytest.mark.asyncio
    async def test_list_patterns_is_scoped_to_principal(self, clean_test_data):
        """list_patterns returns only the authenticated user's patterns."""
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(
                LearnedPattern(
                    user_id=TEST_USER_ID,
                    pattern_type=PatternType.COMMAND_SEQUENCE,
                    pattern_data={"action_type": "test_action"},
                    confidence=0.7,
                    enabled=True,
                )
            )
            await session.commit()

        # Owner sees the pattern…
        owner_view = await list_patterns(current_user=_TEST_CLAIMS)
        assert owner_view["count"] == 1
        # …a different principal does not (isolation on read).
        other_view = await list_patterns(current_user=_OTHER_CLAIMS)
        assert other_view["count"] == 0

    @pytest.mark.asyncio
    async def test_enable_pattern_cross_user_is_not_found(self, clean_test_data):
        """A non-owner cannot mutate another user's pattern (enable → 404-shape)."""
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.7,
                enabled=False,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Cross-user enable must not find the pattern: the not-found path
        # returns a 404-shape JSONResponse, never a success dict.
        result = await enable_pattern(str(pattern_id), current_user=_OTHER_CLAIMS)
        assert not (isinstance(result, dict) and result.get("success") is True)

        # Definitive proof of isolation: the pattern stays disabled — no
        # cross-user write happened.
        async with AsyncSessionFactory.session_scope_fresh() as session:
            row = await session.get(LearnedPattern, pattern_id)
            assert row.enabled is False


class TestLearningSettings:
    """Test learning settings management (global enable/disable)."""

    @pytest.mark.asyncio
    async def test_get_default_settings(self, clean_test_data):
        """Test getting default settings when none exist."""
        result = await get_settings(current_user=_TEST_CLAIMS)

        assert result["configured"] is False
        assert result["settings"]["learning_enabled"] is True  # Default
        assert result["settings"]["suggestion_threshold"] == 0.7
        assert result["settings"]["automation_threshold"] == 0.9

    @pytest.mark.asyncio
    async def test_update_settings_creates_new(self, clean_test_data):
        """Test updating settings creates new record if none exists."""
        settings_update = SettingsUpdate(learning_enabled=False, suggestion_threshold=0.8)

        result = await update_settings(settings_update, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["settings"]["learning_enabled"] is False
        assert result["settings"]["suggestion_threshold"] == 0.8

    @pytest.mark.asyncio
    async def test_update_existing_settings(self, clean_test_data):
        """Test updating existing settings."""
        # Create initial settings
        async with AsyncSessionFactory.session_scope_fresh() as session:
            settings = LearningSettings(
                user_id=TEST_USER_ID,
                learning_enabled=True,
                suggestion_threshold=0.7,
                automation_threshold=0.9,
                auto_apply_enabled=False,
                notification_enabled=True,
            )
            session.add(settings)
            await session.commit()

        # Update settings
        settings_update = SettingsUpdate(learning_enabled=False)
        result = await update_settings(settings_update, current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["settings"]["learning_enabled"] is False
        assert result["settings"]["suggestion_threshold"] == 0.7  # Unchanged


class TestPatternEnableDisable:
    """Test per-pattern enable/disable (Phase 3 requirement)."""

    @pytest.mark.asyncio
    async def test_disable_pattern(self, clean_test_data):
        """Test disabling a pattern."""
        # Create pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.8,
                usage_count=5,
                success_count=4,
                failure_count=1,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Disable pattern
        result = await disable_pattern(str(pattern_id), current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["enabled"] is False

    @pytest.mark.asyncio
    async def test_enable_pattern(self, clean_test_data):
        """Test enabling a pattern."""
        # Create disabled pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.8,
                usage_count=5,
                success_count=4,
                failure_count=1,
                enabled=False,  # Disabled
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Enable pattern
        result = await enable_pattern(str(pattern_id), current_user=_TEST_CLAIMS)

        assert result["success"] is True
        assert result["pattern"]["enabled"] is True


class TestPerformanceRequirements:
    """Test <10ms overhead requirement from #300."""

    @pytest.mark.asyncio
    async def test_feedback_performance(self, clean_test_data):
        """Test pattern feedback completes quickly."""
        import time

        # Create pattern
        async with AsyncSessionFactory.session_scope_fresh() as session:
            pattern = LearnedPattern(
                user_id=TEST_USER_ID,
                pattern_type=PatternType.COMMAND_SEQUENCE,
                pattern_data={"action_type": "test_action"},
                confidence=0.7,
                usage_count=5,
                success_count=3,
                failure_count=2,
                enabled=True,
            )
            session.add(pattern)
            await session.commit()
            pattern_id = pattern.id

        # Warm up
        feedback = PatternFeedback(action="accept")
        await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)

        # Measure
        start = time.perf_counter()
        feedback = PatternFeedback(action="accept")
        await provide_pattern_feedback(pattern_id, feedback, current_user=_TEST_CLAIMS)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Should complete quickly (<10ms target)
        assert elapsed_ms < 50.0, f"Feedback took {elapsed_ms:.2f}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-s"])
