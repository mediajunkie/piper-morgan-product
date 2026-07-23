"""
Tests for Preference Questionnaire

Tests the structured questionnaire for collecting user preferences.

Issue #267 CORE-PREF-QUEST
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from scripts.preferences_questionnaire import (
    get_current_user_id,
    get_existing_preferences,
    parse_choice,
    run_preference_questionnaire,
    store_user_preferences,
)


class TestParseChoice:
    """Test choice parsing functionality"""

    def test_parse_choice_valid(self):
        """Test valid choice parsing"""
        options = ["concise", "balanced", "detailed"]

        assert parse_choice("1", options) == "concise"
        assert parse_choice("2", options) == "balanced"
        assert parse_choice("3", options) == "detailed"

    def test_parse_choice_invalid_number(self):
        """Test invalid numbers default to middle option"""
        options = ["concise", "balanced", "detailed"]

        # Out of range
        assert parse_choice("0", options) == "balanced"
        assert parse_choice("4", options) == "balanced"
        assert parse_choice("10", options) == "balanced"

    def test_parse_choice_invalid_input(self):
        """Test invalid input defaults to middle option"""
        options = ["concise", "balanced", "detailed"]

        # Non-numeric
        assert parse_choice("abc", options) == "balanced"
        assert parse_choice("", options) == "balanced"
        assert parse_choice("  ", options) == "balanced"
        assert parse_choice("1.5", options) == "balanced"

    def test_parse_choice_different_lengths(self):
        """Test with different option list lengths"""
        # 2 options - middle is index 1
        two_options = ["a", "b"]
        assert parse_choice("invalid", two_options) == "b"

        # 4 options - middle is index 2
        four_options = ["a", "b", "c", "d"]
        assert parse_choice("invalid", four_options) == "c"

        # 5 options - middle is index 2
        five_options = ["a", "b", "c", "d", "e"]
        assert parse_choice("invalid", five_options) == "c"


class TestStoreUserPreferences:
    """Test preference storage functionality"""

    @pytest.mark.asyncio
    async def test_store_preferences_success(self):
        """Test successful preference storage"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"
        preferences = {"communication_style": "balanced", "work_style": "flexible"}

        # Mock database operations
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = ("550e8400-e29b-41d4-a716-446655440099",)  # User exists
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await store_user_preferences(user_id, preferences)

            assert result is True
            assert "configured_at" in preferences

            # Verify database calls
            assert mock_session.execute.call_count == 2  # Check user exists + update

    @pytest.mark.asyncio
    async def test_store_preferences_user_not_found(self):
        """Test handling when user doesn't exist"""
        user_id = "nonexistent-user"
        preferences = {"communication_style": "balanced"}

        # Mock database operations - user not found
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None  # User doesn't exist
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await store_user_preferences(user_id, preferences)

            assert result is False

    @pytest.mark.asyncio
    async def test_store_preferences_database_error(self):
        """Test handling database errors"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"
        preferences = {"communication_style": "balanced"}

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.side_effect = Exception("Database error")

            result = await store_user_preferences(user_id, preferences)

            assert result is False


class TestGetCurrentUserId:
    """Test user ID retrieval functionality"""

    @pytest.mark.asyncio
    async def test_get_current_user_id_success(self):
        """Test successful user ID retrieval"""
        expected_user_id = "550e8400-e29b-41d4-a716-446655440099"

        # Mock database operations
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (expected_user_id,)
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await get_current_user_id()

            assert result == expected_user_id

    @pytest.mark.asyncio
    async def test_get_current_user_id_no_users(self):
        """Test handling when no users exist"""
        # Mock database operations - no users
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await get_current_user_id()

            assert result is None


class TestGetExistingPreferences:
    """Test existing preference retrieval"""

    @pytest.mark.asyncio
    async def test_get_existing_preferences_success(self):
        """Test successful preference retrieval"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"
        expected_prefs = {
            "communication_style": "balanced",
            "work_style": "flexible",
            "configured_at": "2025-10-23T16:00:00Z",
        }

        # Mock database operations
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (expected_prefs,)
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await get_existing_preferences(user_id)

            assert result == expected_prefs

    @pytest.mark.asyncio
    async def test_get_existing_preferences_none(self):
        """Test handling when no preferences exist"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"

        # Mock database operations - no preferences
        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.fetchone.return_value = (None,)  # NULL preferences
        mock_session.execute.return_value = mock_result

        with patch("scripts.preferences_questionnaire.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.return_value.__aenter__.return_value = mock_session

            result = await get_existing_preferences(user_id)

            assert result == {}


class TestRunPreferenceQuestionnaire:
    """Test full questionnaire flow"""

    @pytest.mark.asyncio
    async def test_questionnaire_full_flow(self):
        """Test complete questionnaire flow with valid inputs"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"

        # Mock user inputs (1, 2, 3, 1, 2 for the 5 questions)
        mock_inputs = ["1", "2", "3", "1", "2"]

        with (
            patch("builtins.input", side_effect=mock_inputs),
            patch("scripts.preferences_questionnaire.get_existing_preferences", return_value={}),
            patch("scripts.preferences_questionnaire.store_user_preferences", return_value=True),
            patch("builtins.print"),
        ):  # Suppress print output
            result = await run_preference_questionnaire(user_id)

            assert result is True

    @pytest.mark.asyncio
    async def test_questionnaire_update_existing(self):
        """Test updating existing preferences"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"
        existing_prefs = {
            "communication_style": "detailed",
            "configured_at": "2025-10-23T15:00:00Z",
        }

        # Mock user inputs: "y" to update, then answers
        mock_inputs = ["y", "1", "2", "3", "1", "2"]

        with (
            patch("builtins.input", side_effect=mock_inputs),
            patch(
                "scripts.preferences_questionnaire.get_existing_preferences",
                return_value=existing_prefs,
            ),
            patch("scripts.preferences_questionnaire.store_user_preferences", return_value=True),
            patch("builtins.print"),
        ):
            result = await run_preference_questionnaire(user_id)

            assert result is True

    @pytest.mark.asyncio
    async def test_questionnaire_skip_update(self):
        """Test skipping update of existing preferences"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"
        existing_prefs = {
            "communication_style": "detailed",
            "configured_at": "2025-10-23T15:00:00Z",
        }

        # Mock user input: "n" to skip update
        mock_inputs = ["n"]

        with (
            patch("builtins.input", side_effect=mock_inputs),
            patch(
                "scripts.preferences_questionnaire.get_existing_preferences",
                return_value=existing_prefs,
            ),
            patch("builtins.print"),
        ):
            result = await run_preference_questionnaire(user_id)

            assert result is True

    @pytest.mark.asyncio
    async def test_questionnaire_storage_failure(self):
        """Test handling storage failure"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"

        # Mock user inputs
        mock_inputs = ["1", "2", "3", "1", "2"]

        with (
            patch("builtins.input", side_effect=mock_inputs),
            patch("scripts.preferences_questionnaire.get_existing_preferences", return_value={}),
            patch("scripts.preferences_questionnaire.store_user_preferences", return_value=False),
            patch("builtins.print"),
        ):
            result = await run_preference_questionnaire(user_id)

            assert result is False

    @pytest.mark.asyncio
    async def test_questionnaire_keyboard_interrupt(self):
        """Test handling keyboard interrupt (Ctrl+C)"""
        user_id = "550e8400-e29b-41d4-a716-446655440099"

        with (
            patch("builtins.input", side_effect=KeyboardInterrupt),
            patch("scripts.preferences_questionnaire.get_existing_preferences", return_value={}),
            patch("builtins.print"),
        ):
            result = await run_preference_questionnaire(user_id)

            assert result is False


class TestPreferenceValues:
    """Test that all preference values are correctly mapped"""

    def test_all_preference_dimensions(self):
        """Test that all 5 preference dimensions have correct options"""

        # Communication Style
        comm_options = ["concise", "balanced", "detailed"]
        assert parse_choice("1", comm_options) == "concise"
        assert parse_choice("2", comm_options) == "balanced"
        assert parse_choice("3", comm_options) == "detailed"

        # Work Style
        work_options = ["structured", "flexible", "exploratory"]
        assert parse_choice("1", work_options) == "structured"
        assert parse_choice("2", work_options) == "flexible"
        assert parse_choice("3", work_options) == "exploratory"

        # Decision Making
        decision_options = ["data-driven", "intuitive", "collaborative"]
        assert parse_choice("1", decision_options) == "data-driven"
        assert parse_choice("2", decision_options) == "intuitive"
        assert parse_choice("3", decision_options) == "collaborative"

        # Learning Style
        learning_options = ["examples", "explanations", "exploration"]
        assert parse_choice("1", learning_options) == "examples"
        assert parse_choice("2", learning_options) == "explanations"
        assert parse_choice("3", learning_options) == "exploration"

        # Feedback Level
        feedback_options = ["minimal", "moderate", "detailed"]
        assert parse_choice("1", feedback_options) == "minimal"
        assert parse_choice("2", feedback_options) == "moderate"
        assert parse_choice("3", feedback_options) == "detailed"
