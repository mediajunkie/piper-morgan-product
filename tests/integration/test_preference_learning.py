"""
Integration tests for preference learning system.

Tests the flow from pattern detection → implicit preference → explicit preference,
all through the user-scoped UserPreferenceManager.

Issue: #223 (CORE-LEARN-C)

1613: the QueryLearningLoop fixture and its two pooled-store tests were removed
with the pooled store itself (PM ruling 2026-08-31).
"""

from datetime import datetime

import pytest

from services.domain.user_preference_manager import UserPreferenceManager


class TestPreferenceLearning:
    """Test preference learning from patterns."""

    @pytest.fixture
    async def preference_manager(self):
        """Create UserPreferenceManager instance."""
        manager = UserPreferenceManager()
        yield manager
        # Cleanup after test
        try:
            await manager.clear_session_preferences("test_user", "test_session")
        except:
            pass  # Ignore cleanup errors

    @pytest.mark.asyncio
    async def test_pattern_to_preference_flow(self, preference_manager):
        """
        Test complete flow: User behavior → Pattern → Preference.

        Simulates:
        1. User consistently chooses concise responses
        2. System learns USER_PREFERENCE_PATTERN
        3. Pattern is applied as explicit preference
        4. Preference is retrievable and affects behavior
        """
        # Create a high-confidence user preference pattern
        pattern_dict = {
            "confidence": 0.85,  # High confidence
            "pattern_data": {
                "preference_key": "response_style",
                "preference_value": "concise",
                "observations": 15,
                "description": "User consistently prefers concise responses",
            },
            "pattern_type": "user_preference_pattern",
            "pattern_id": "test_pattern_001",
        }

        # Apply pattern to preferences
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern_dict, user_id="test_user"
        )

        assert success is True

        # Verify preference was set
        response_style = await preference_manager.get_preference(
            key="response_style", user_id="test_user"
        )

        assert response_style == "concise"

    @pytest.mark.asyncio
    async def test_low_confidence_pattern_ignored(self, preference_manager):
        """
        Test that low-confidence patterns don't become preferences.

        Only patterns with confidence >= 0.7 should be applied.
        """
        # Create a low-confidence pattern
        pattern_dict = {
            "confidence": 0.45,  # Low confidence
            "pattern_data": {
                "preference_key": "detail_level",
                "preference_value": "detailed",
                "observations": 5,
                "description": "User might prefer detailed responses",
            },
            "pattern_type": "user_preference_pattern",
            "pattern_id": "test_pattern_002",
        }

        # Attempt to apply pattern
        success = await preference_manager.apply_preference_pattern(
            pattern=pattern_dict, user_id="test_user"
        )

        # Should be rejected due to low confidence
        assert success is False

        # Verify preference was NOT set
        detail_level = await preference_manager.get_preference(
            key="detail_level", user_id="test_user"
        )

        assert detail_level is None  # Should be None (not set)

    @pytest.mark.asyncio
    async def test_preference_hierarchy_preserved(self, preference_manager):
        """
        Test that pattern-derived preferences respect hierarchy.

        Session preferences should override user preferences.
        """
        # Set user-level preference from pattern
        user_pattern = {
            "confidence": 0.8,
            "pattern_data": {"preference_key": "format", "preference_value": "markdown"},
            "pattern_type": "user_preference_pattern",
            "pattern_id": "test_pattern_003",
        }

        await preference_manager.apply_preference_pattern(
            pattern=user_pattern, user_id="test_user", scope="user"
        )

        # Set session-level preference from pattern
        session_pattern = {
            "confidence": 0.75,
            "pattern_data": {"preference_key": "format", "preference_value": "json"},
            "pattern_type": "user_preference_pattern",
            "pattern_id": "test_pattern_004",
        }

        await preference_manager.apply_preference_pattern(
            pattern=session_pattern, user_id="test_user", session_id="test_session", scope="session"
        )

        # Session preference should override user preference
        format_pref = await preference_manager.get_preference(
            key="format", user_id="test_user", session_id="test_session"
        )

        assert format_pref == "json"  # Session value, not user value

        # Without session, should get user preference
        format_pref_no_session = await preference_manager.get_preference(
            key="format", user_id="test_user"
        )

        assert format_pref_no_session == "markdown"  # User value

    @pytest.mark.asyncio
    async def test_invalid_pattern_data(self, preference_manager):
        """
        Test error handling with invalid pattern data.

        Missing preference_key or preference_value should fail gracefully.
        """
        # Pattern missing preference_value
        invalid_pattern = {
            "confidence": 0.9,
            "pattern_data": {
                "preference_key": "test_key"
                # Missing preference_value!
            },
            "pattern_type": "user_preference_pattern",
            "pattern_id": "invalid_pattern_001",
        }

        success = await preference_manager.apply_preference_pattern(
            pattern=invalid_pattern, user_id="test_user"
        )

        # Should return False, not raise exception
        assert success is False

        # Pattern missing preference_key
        invalid_pattern2 = {
            "confidence": 0.9,
            "pattern_data": {
                "preference_value": "test_value"
                # Missing preference_key!
            },
            "pattern_type": "user_preference_pattern",
            "pattern_id": "invalid_pattern_002",
        }

        success2 = await preference_manager.apply_preference_pattern(
            pattern=invalid_pattern2, user_id="test_user"
        )

        # Should return False, not raise exception
        assert success2 is False


if __name__ == "__main__":
    # Run integration tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
