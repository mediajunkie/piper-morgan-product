"""Tests for #693 WIRE-MCP-STANDUP — placeholder helpers wired to UserPreferenceManager.

Covers the three previously-returning-None helpers:
- ``_get_user_slack_workspace`` → wraps SLACK_DEFAULT_CHANNEL pref in dict
- ``_get_user_github_repo`` → delegates to ``get_default_repo`` (#1042)
- ``_get_user_notion_database`` → delegates to ``get_notion_database``
- ``_parse_user_id_for_prefs`` → defensive UUID parsing

Note: this issue narrowly wires the 3 placeholders. The downstream secondary
actions (post-to-slack, create-issues, sync-to-notion) have additional
defects that surface only when these gates open — those are tracked as
separate discovered-work issues and NOT in scope here.
"""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.integrations.mcp.skills.standup_workflow_skill import (
    StandupWorkflowSkill,
)


@contextmanager
def _patched_skill_deps():
    """Patch all the skill's heavy dependencies for in-process instantiation.

    Mirrors the fixture pattern in
    ``tests/unit/integrations/mcp/test_standup_workflow_skill.py`` so the
    skill can be constructed without touching the real domain services.

    #1289: MorningStandupWorkflow / StandupOrchestrationService /
    SessionPersistenceManager are no longer imported by the skill; patches removed.
    """
    module = "services.integrations.mcp.skills.standup_workflow_skill"
    with (
        patch(f"{module}.GitHubDomainService"),
        patch(f"{module}.SlackDomainService"),
        patch(f"{module}.UserPreferenceManager"),
        patch(f"{module}.NotionDomainService"),
    ):
        yield


def _make_skill_with_mock_prefs():
    """Construct a StandupWorkflowSkill with the preference_manager mocked.

    Returns: (skill, mock_pref_manager) — direct access for assertions.
    The full dependency chain is patched at construction time; we then
    swap in a clean MagicMock for the preference manager so per-test
    AsyncMock returns are explicit.
    """
    with _patched_skill_deps():
        skill = StandupWorkflowSkill()
    mock_prefs = MagicMock()
    mock_prefs.get_slack_default_channel = AsyncMock(return_value=None)
    mock_prefs.get_default_repo = AsyncMock(return_value=None)
    mock_prefs.get_notion_database = AsyncMock(return_value=None)
    # Skill reads through self.workflow.preference_manager
    skill.workflow.preference_manager = mock_prefs
    return skill, mock_prefs


# -------------------------------------------------------------------
# _get_user_slack_workspace
# -------------------------------------------------------------------


class TestGetUserSlackWorkspace:
    @pytest.mark.asyncio
    async def test_returns_dict_when_channel_pref_set(self):
        """Channel set → ``{"default_channel": "#standups"}`` shape."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_slack_default_channel.return_value = "#standups"

        result = await skill._get_user_slack_workspace(str(uuid4()))

        assert result == {"default_channel": "#standups"}

    @pytest.mark.asyncio
    async def test_returns_none_when_channel_pref_unset(self):
        """Channel pref is None → helper returns None (gates skill skip)."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_slack_default_channel.return_value = None

        result = await skill._get_user_slack_workspace(str(uuid4()))

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_channel_pref_empty_string(self):
        """Empty-string channel (shouldn't be settable but defensive) → None."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_slack_default_channel.return_value = ""

        result = await skill._get_user_slack_workspace(str(uuid4()))

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_user_id_not_uuid(self):
        """Bogus user_id → None without touching preference manager."""
        skill, mock_prefs = _make_skill_with_mock_prefs()

        result = await skill._get_user_slack_workspace("not-a-uuid")

        assert result is None
        mock_prefs.get_slack_default_channel.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_passes_parsed_uuid_to_pref_manager(self):
        """user_id string is parsed to UUID before passing to pref manager."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_slack_default_channel.return_value = "#anywhere"
        uid = uuid4()

        await skill._get_user_slack_workspace(str(uid))

        mock_prefs.get_slack_default_channel.assert_awaited_once_with(uid)


# -------------------------------------------------------------------
# _get_user_github_repo
# -------------------------------------------------------------------


class TestGetUserGitHubRepo:
    @pytest.mark.asyncio
    async def test_returns_default_repo_when_set(self):
        """Default repo set → returned as-is (no shape transformation)."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_default_repo.return_value = "test-org/test-repo"

        result = await skill._get_user_github_repo(str(uuid4()))

        assert result == "test-org/test-repo"

    @pytest.mark.asyncio
    async def test_returns_none_when_default_repo_unset(self):
        """Default repo None → None (skill skips create-issues branch)."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_default_repo.return_value = None

        result = await skill._get_user_github_repo(str(uuid4()))

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_user_id_not_uuid(self):
        """Bogus user_id → None without touching preference manager."""
        skill, mock_prefs = _make_skill_with_mock_prefs()

        result = await skill._get_user_github_repo("not-a-uuid")

        assert result is None
        mock_prefs.get_default_repo.assert_not_awaited()


# -------------------------------------------------------------------
# _get_user_notion_database
# -------------------------------------------------------------------


class TestGetUserNotionDatabase:
    @pytest.mark.asyncio
    async def test_returns_database_id_when_set(self):
        """Notion DB ID set → returned as-is."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_notion_database.return_value = "abc123-def456-789xyz"

        result = await skill._get_user_notion_database(str(uuid4()))

        assert result == "abc123-def456-789xyz"

    @pytest.mark.asyncio
    async def test_returns_none_when_db_unset(self):
        """Notion DB unset → None (skill skips Notion update)."""
        skill, mock_prefs = _make_skill_with_mock_prefs()
        mock_prefs.get_notion_database.return_value = None

        result = await skill._get_user_notion_database(str(uuid4()))

        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_when_user_id_not_uuid(self):
        """Bogus user_id → None without touching preference manager."""
        skill, mock_prefs = _make_skill_with_mock_prefs()

        result = await skill._get_user_notion_database("not-a-uuid")

        assert result is None
        mock_prefs.get_notion_database.assert_not_awaited()


# -------------------------------------------------------------------
# _parse_user_id_for_prefs
# -------------------------------------------------------------------


class TestParseUserIdForPrefs:
    """The static UUID-parsing helper."""

    def test_valid_uuid_string_parses(self):
        uid = uuid4()
        result = StandupWorkflowSkill._parse_user_id_for_prefs(str(uid))
        assert result == uid

    def test_uuid_object_passes_through(self):
        """UUID objects (as str()) parse back to the same UUID."""
        uid = uuid4()
        result = StandupWorkflowSkill._parse_user_id_for_prefs(uid)
        assert result == uid

    @pytest.mark.parametrize("bad_input", ["not-a-uuid", "", None, "12345", 42])
    def test_invalid_inputs_return_none(self, bad_input):
        result = StandupWorkflowSkill._parse_user_id_for_prefs(bad_input)
        assert result is None


# -------------------------------------------------------------------
# UserPreferenceManager — new typed accessors (round-trip + validation)
# -------------------------------------------------------------------


class TestSlackDefaultChannelAccessors:
    """Issue #693 added get/set_slack_default_channel to UserPreferenceManager."""

    @pytest.mark.asyncio
    async def test_round_trip_set_and_get(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        # Use mocked storage to avoid touching real DB
        manager.set_preference = AsyncMock()
        manager.get_preference = AsyncMock(return_value="#standups")

        uid = uuid4()
        await manager.set_slack_default_channel(uid, "#standups")
        result = await manager.get_slack_default_channel(uid)

        assert result == "#standups"
        manager.set_preference.assert_awaited_once()
        manager.get_preference.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_set_none_clears_preference(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        await manager.set_slack_default_channel(uuid4(), None)
        # Verify None is stored (not rejected)
        manager.set_preference.assert_awaited_once()
        args, kwargs = manager.set_preference.call_args
        assert args[1] is None  # The value argument

    @pytest.mark.asyncio
    async def test_set_non_string_raises_type_error(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        with pytest.raises(TypeError, match="expected str or None"):
            await manager.set_slack_default_channel(uuid4(), 42)
        manager.set_preference.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_set_empty_string_raises_value_error(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        with pytest.raises(ValueError, match="cannot be empty"):
            await manager.set_slack_default_channel(uuid4(), "")
        manager.set_preference.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_set_whitespace_only_raises_value_error(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        with pytest.raises(ValueError, match="cannot be empty"):
            await manager.set_slack_default_channel(uuid4(), "   ")
        manager.set_preference.assert_not_awaited()


class TestNotionDatabaseAccessors:
    """Issue #693 added get/set_notion_database to UserPreferenceManager."""

    @pytest.mark.asyncio
    async def test_round_trip_set_and_get(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()
        manager.get_preference = AsyncMock(return_value="db-id-123")

        uid = uuid4()
        await manager.set_notion_database(uid, "db-id-123")
        result = await manager.get_notion_database(uid)

        assert result == "db-id-123"
        manager.set_preference.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_set_none_clears_preference(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        await manager.set_notion_database(uuid4(), None)
        manager.set_preference.assert_awaited_once()
        args, kwargs = manager.set_preference.call_args
        assert args[1] is None

    @pytest.mark.asyncio
    async def test_set_non_string_raises_type_error(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        with pytest.raises(TypeError, match="expected str or None"):
            await manager.set_notion_database(uuid4(), ["not", "a", "string"])
        manager.set_preference.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_set_empty_string_raises_value_error(self):
        from services.domain.user_preference_manager import UserPreferenceManager

        manager = UserPreferenceManager()
        manager.set_preference = AsyncMock()

        with pytest.raises(ValueError, match="cannot be empty"):
            await manager.set_notion_database(uuid4(), "")
        manager.set_preference.assert_not_awaited()


# -------------------------------------------------------------------
# Preference key constants exist (sanity check)
# -------------------------------------------------------------------


class TestPreferenceKeyConstants:
    def test_slack_default_channel_key_is_stable(self):
        from services.domain.user_preference_manager import SLACK_DEFAULT_CHANNEL

        assert SLACK_DEFAULT_CHANNEL == "slack_default_channel"

    def test_notion_database_key_is_stable(self):
        from services.domain.user_preference_manager import NOTION_DATABASE

        assert NOTION_DATABASE == "notion_database"
