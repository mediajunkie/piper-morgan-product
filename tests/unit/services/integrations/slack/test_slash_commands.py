"""
Tests for Slack Slash Commands.

Issue #520: Canonical Queries #49, #50
- Query #49: /standup - Generate daily standup
- Query #50: /piper help - Show available commands and capabilities
Issue #1429: /standup Yesterday/Today wired to real todo services

Test categories:
1. Routing tests - verify command routing logic
2. Handler tests - verify handler behavior
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.integrations.slack.webhook_router import SlackWebhookRouter


def _todo(text, completed=False, completed_at=None, priority="medium"):
    """Minimal domain-Todo stand-in with the fields /standup reads."""
    return SimpleNamespace(
        text=text, completed=completed, completed_at=completed_at, priority=priority
    )


class TestSlashCommandRouting:
    """Test slash command routing logic.

    Issue #521 learning: Routing tests verify the full path
    from _process_slash_command → appropriate handler.
    """

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_piper_help_routes_correctly(self, router):
        """Verify /piper help routes to help handler."""
        result = await router._process_slash_command(
            {
                "command": "/piper",
                "text": "help",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "response_type" in result
        # Issue #628: Grammar-conscious help uses warm intro
        text = result.get("text", "")
        assert "Piper" in text
        assert "help" in text.lower()

    @pytest.mark.asyncio
    async def test_piper_empty_routes_to_help(self, router):
        """Verify /piper with no text routes to help."""
        result = await router._process_slash_command(
            {
                "command": "/piper",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "response_type" in result
        # Issue #628: Grammar-conscious help uses warm intro
        assert "Piper" in result.get("text", "")

    @pytest.mark.asyncio
    async def test_standup_routes_correctly(self, router):
        """Verify /standup routes to standup handler."""
        result = await router._process_slash_command(
            {
                "command": "/standup",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert result["response_type"] == "in_channel"

    @pytest.mark.asyncio
    async def test_unknown_command_returns_help_hint(self, router):
        """Verify unknown command suggests /piper help."""
        result = await router._process_slash_command(
            {
                "command": "/unknown",
                "text": "",
                "user_id": "U123",
                "channel_id": "C456",
            }
        )
        assert "Unknown command" in result.get("text", "")
        assert "/piper help" in result.get("text", "")


class TestPiperHelpCommand:
    """Test /piper help command handler."""

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_help_includes_available_commands(self, router):
        """Test help lists available commands."""
        result = await router._handle_piper_command("help", "U123", "C456")
        assert "/piper help" in result.get("text", "")
        assert "/standup" in result.get("text", "")

    @pytest.mark.asyncio
    async def test_help_includes_capabilities(self, router):
        """Test help shows capabilities."""
        result = await router._handle_piper_command("help", "U123", "C456")
        # Issue #551: Now uses CommandRegistry - shows category-based commands
        # Issue #628: Grammar-conscious help text
        text = result.get("text", "")
        # Should show commands by category (Discovery, Identity, etc.)
        assert "Piper" in text  # Should mention Piper
        assert "help" in text.lower()  # Should show help info

    @pytest.mark.asyncio
    async def test_help_is_ephemeral(self, router):
        """Test help response is ephemeral (only visible to user)."""
        result = await router._handle_piper_command("help", "U123", "C456")
        assert result["response_type"] == "ephemeral"

    @pytest.mark.asyncio
    async def test_unknown_subcommand_suggests_help(self, router):
        """Test unknown subcommand suggests /piper help."""
        result = await router._handle_piper_command("foobar", "U123", "C456")
        # Issue #628: Grammar-conscious error message
        text = result.get("text", "")
        assert "don't recognize" in text or "foobar" in text
        assert "/piper help" in text


class TestStandupCommand:
    """Test /standup command handler."""

    @pytest.fixture
    def router(self):
        """Create SlackWebhookRouter instance for testing."""
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_standup_has_three_sections(self, router):
        """Test standup includes yesterday, today, blockers."""
        result = await router._handle_standup_command("U123", "C456")
        text = result.get("text", "")
        assert "Yesterday" in text
        assert "Today" in text
        assert "Blockers" in text

    @pytest.mark.asyncio
    async def test_standup_is_public(self, router):
        """Test standup uses in_channel response (visible to team)."""
        result = await router._handle_standup_command("U123", "C456")
        assert result["response_type"] == "in_channel"

    @pytest.mark.asyncio
    async def test_standup_handles_empty_data_gracefully(self, router):
        """Test standup handles no data without errors.

        Issue #1429: uses a resolvable (UUID) principal so the empty copy is
        honest — we actually looked and found nothing.
        """
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=[])
            result = await router._handle_standup_command(str(uuid4()), "C456")
        # Should still return valid structure with defaults
        text = result.get("text", "")
        assert "Yesterday" in text
        assert "Today" in text
        # Should show placeholder when no data
        assert "No completed items" in text or "No high-priority" in text or "None" in text

    @pytest.mark.asyncio
    async def test_standup_handles_errors_gracefully(self, router):
        """Test standup returns ephemeral on error.

        Issue #1429: the user_id must be a resolvable (UUID) principal so the
        data-source helper is actually invoked (unresolvable Slack IDs
        short-circuit to honest not-linked copy without calling it).
        """
        # Mock _get_completed_since_yesterday to throw
        with patch.object(
            router, "_get_completed_since_yesterday", side_effect=Exception("Test error")
        ):
            result = await router._handle_standup_command(str(uuid4()), "C456")
            assert result["response_type"] == "ephemeral"
            assert "Unable to generate standup" in result.get("text", "")


class TestStandupDataWiring1429:
    """Issue #1429: /standup Yesterday/Today sections wired to real todo services.

    Previously `_get_completed_since_yesterday` / `_get_today_priorities` always
    returned `[]` (placeholder TODOs), so every standup said "No completed items
    recorded" regardless of actual work — the F2 affirmative-false shape.
    (`_get_blockers` returning [] is ratified product behavior #692 — untouched.)
    """

    @pytest.fixture
    def router(self):
        return SlackWebhookRouter()

    @pytest.mark.asyncio
    async def test_completed_todos_since_yesterday_render(self, router):
        """A user with todos completed yesterday sees them under *Yesterday:*."""
        now = datetime.now(timezone.utc)
        todos = [
            _todo("Ship the report", completed=True, completed_at=now - timedelta(hours=20)),
            _todo("Old chore", completed=True, completed_at=now - timedelta(days=5)),
            _todo("Still pending", completed=False),
        ]
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=todos)
            result = await router._handle_standup_command(str(uuid4()), "C456")

        text = result.get("text", "")
        assert result["response_type"] == "in_channel"
        assert "Ship the report" in text
        # Completed long before yesterday must NOT render as yesterday's work
        assert "Old chore" not in text
        # And the affirmative-false empty copy must be gone
        assert "No completed items recorded" not in text

    @pytest.mark.asyncio
    async def test_today_shows_high_priority_pending_todos(self, router):
        """Pending urgent/high todos render under *Today:*, urgent first."""
        todos = [
            _todo("Low-key cleanup", priority="low"),
            _todo("Fix prod bug", priority="urgent"),
            _todo("Review design doc", priority="high"),
            _todo("Medium thing", priority="medium"),
        ]
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=todos)
            result = await router._handle_standup_command(str(uuid4()), "C456")

        text = result.get("text", "")
        assert "Fix prod bug" in text
        assert "Review design doc" in text
        assert "Low-key cleanup" not in text
        assert "Medium thing" not in text
        # Urgent outranks high
        assert text.index("Fix prod bug") < text.index("Review design doc")

    @pytest.mark.asyncio
    async def test_unlinked_slack_user_gets_honest_copy(self, router):
        """A raw Slack workspace ID ("U…") has no todo principal — the sections
        must say so honestly, never claim "No completed items recorded" when we
        did not look."""
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=[])
            result = await router._handle_standup_command("U123ABC", "C456")
            # We never looked, so the todo service must not have been queried
            mock_svc.return_value.list_todos.assert_not_awaited()

        text = result.get("text", "")
        assert "No completed items recorded" not in text
        assert "No high-priority items scheduled" not in text
        assert "isn't linked" in text
        # Sections still render, and blockers behavior (#692) is untouched
        assert "Yesterday" in text
        assert "Today" in text
        assert "Blockers" in text
        assert "None" in text

    @pytest.mark.asyncio
    async def test_lookup_failure_says_couldnt_check_not_empty_claim(self, router):
        """A failed lookup renders "couldn't check" copy (#1425 shape), never
        the affirmative-false "No completed items recorded"."""
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(side_effect=Exception("db down"))
            result = await router._handle_standup_command(str(uuid4()), "C456")

        text = result.get("text", "")
        assert "No completed items recorded" not in text
        assert "No high-priority items scheduled" not in text
        assert "couldn't check" in text

    @pytest.mark.asyncio
    async def test_blockers_section_still_ratified_empty(self, router):
        """#692: _get_blockers stays a ratified [] — Blockers renders "None"."""
        assert await router._get_blockers() == []
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=[])
            result = await router._handle_standup_command(str(uuid4()), "C456")
        assert "*Blockers:*" in result.get("text", "")
        assert "None" in result.get("text", "")
