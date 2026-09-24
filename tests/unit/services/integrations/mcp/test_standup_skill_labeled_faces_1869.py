"""Tests for #1869 — StandupWorkflowSkill's two raw-ISO-in-user-face defects.

``services/integrations/mcp/skills/standup_workflow_skill.py`` rendered the raw
ISO ``generated_at`` straight into two user-visible surfaces:

1. ``_text_version`` / ``_format_for_slack`` (via ``_post_to_slack``) — the
   Slack fallback text (~line 461 pre-fix).
2. ``_format_github_issue_body`` (via ``_process_github_items``) — the GitHub
   issue body's ``**Date**:`` line (~line 499 pre-fix).

Ruling (decisions.log, 2026-09-23 14:39, #1869): the zone source for these
faces is the #1574 preference store via ``user_timezone_name(user_id)`` — NOT
Slack's ``users.info.tz``. When no user resolves, fall back to UTC and label
it "UTC". Both sites must render a *labeled* face (date + time + zone
abbreviation) on the user's clock, never the raw ISO string.

``user_timezone_name`` is patched at the skill module's own import seam
(``from services.utils.datetime_utils import ... user_timezone_name`` in
standup_workflow_skill.py) rather than at its defining module, per the
skill's actual import binding.
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.slack_domain_service import SlackDomainService

SKILL_MODULE = "services.integrations.mcp.skills.standup_workflow_skill"

# A fixed UTC instant with no DST ambiguity in either zone under test:
# 2026-01-15T00:00:00+00:00 == 2026-01-15 09:00 AM JST (Tokyo is UTC+9, no DST).
GENERATED_AT_UTC_ISO = "2026-01-15T00:00:00+00:00"

# The ISO "T" date/time separator pattern — must never survive into a
# rendered face (distinct from the "T" inside a zone abbreviation like "JST").
_ISO_T_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


def _assert_no_raw_iso(text: str) -> None:
    assert GENERATED_AT_UTC_ISO not in text
    assert "+00:00" not in text
    assert not _ISO_T_PATTERN.search(text)


@contextmanager
def _patched_skill_deps():
    with (
        patch(f"{SKILL_MODULE}.GitHubDomainService"),
        patch(f"{SKILL_MODULE}.SlackDomainService"),
        patch(f"{SKILL_MODULE}.NotionDomainService"),
        patch(f"{SKILL_MODULE}.UserPreferenceManager"),
    ):
        yield


def _make_skill():
    from services.integrations.mcp.skills.standup_workflow_skill import (
        StandupWorkflowSkill,
    )

    with _patched_skill_deps():
        return StandupWorkflowSkill()


def _standup(generated_at) -> dict:
    return {
        "yesterday_accomplishments": ["Shipped X"],
        "today_priorities": ["Ship Y"],
        "blockers": [],
        "generated_at": generated_at,
        "user_id": str(uuid4()),
    }


# ---------------------------------------------------------------------------
# Site 1 — Slack fallback text (_text_version via _post_to_slack)
# ---------------------------------------------------------------------------


class TestSlackFallbackTextLabeledFace:
    @pytest.mark.asyncio
    async def test_post_to_slack_renders_tokyo_face_not_raw_iso(self):
        """A Tokyo user's Slack fallback text carries a JST-labeled face."""
        skill = _make_skill()
        skill._get_user_slack_workspace = AsyncMock(return_value={"default_channel": "#standups"})
        # #1871: spec=SlackDomainService catches drift if post_message stops
        # existing on the real class (m-43 — was a bare MagicMock()).
        skill.slack_service = MagicMock(spec=SlackDomainService)
        skill.slack_service.post_message = AsyncMock(
            return_value={"success": True, "channel": "#standups", "ts": "123.456"}
        )

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="Asia/Tokyo")):
            result = await skill._post_to_slack(
                user_id=str(uuid4()), standup=_standup(GENERATED_AT_UTC_ISO)
            )

        assert result["success"] is True
        skill.slack_service.post_message.assert_awaited_once()
        text = skill.slack_service.post_message.await_args.kwargs["message"]

        assert "JST" in text
        assert "9:00 AM" in text
        _assert_no_raw_iso(text)

    @pytest.mark.asyncio
    async def test_post_to_slack_renders_utc_label_for_unknown_user(self):
        """When no user resolves, the face falls back to UTC and says 'UTC'."""
        skill = _make_skill()
        skill._get_user_slack_workspace = AsyncMock(return_value={"default_channel": "#standups"})
        # #1871: spec=SlackDomainService catches drift if post_message stops
        # existing on the real class (m-43 — was a bare MagicMock()).
        skill.slack_service = MagicMock(spec=SlackDomainService)
        skill.slack_service.post_message = AsyncMock(
            return_value={"success": True, "channel": "#standups", "ts": "123.456"}
        )

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="UTC")):
            result = await skill._post_to_slack(
                user_id=str(uuid4()), standup=_standup(GENERATED_AT_UTC_ISO)
            )

        assert result["success"] is True
        text = skill.slack_service.post_message.await_args.kwargs["message"]

        assert "UTC" in text
        _assert_no_raw_iso(text)

    @pytest.mark.asyncio
    async def test_post_to_slack_missing_generated_at_omits_timestamp_honestly(self):
        """Missing generated_at never prints a raw fallback string like 'Today'
        borrowed from the old default — it omits the timestamp entirely."""
        skill = _make_skill()
        skill._get_user_slack_workspace = AsyncMock(return_value={"default_channel": "#standups"})
        # #1871: spec=SlackDomainService catches drift if post_message stops
        # existing on the real class (m-43 — was a bare MagicMock()).
        skill.slack_service = MagicMock(spec=SlackDomainService)
        skill.slack_service.post_message = AsyncMock(
            return_value={"success": True, "channel": "#standups", "ts": "123.456"}
        )
        standup = _standup(None)

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="Asia/Tokyo")):
            await skill._post_to_slack(user_id=str(uuid4()), standup=standup)

        text = skill.slack_service.post_message.await_args.kwargs["message"]
        assert text == "Daily Standup"


# ---------------------------------------------------------------------------
# Site 2 — GitHub issue body (_format_github_issue_body via _process_github_items)
# ---------------------------------------------------------------------------


class TestGithubIssueBodyLabeledFace:
    @pytest.mark.asyncio
    async def test_github_issue_body_renders_tokyo_face_not_raw_iso(self):
        """A Tokyo user's GitHub issue body Date line carries a JST-labeled face."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="test-org/test-repo")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 42, "html_url": "https://example.com/42"}
        )
        standup = _standup(GENERATED_AT_UTC_ISO)

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="Asia/Tokyo")):
            result = await skill._process_github_items(user_id=str(uuid4()), standup=standup)

        assert result["success"] is True
        skill.github_service.create_issue.assert_awaited()
        body = skill.github_service.create_issue.await_args.kwargs["body"]

        assert "JST" in body
        assert "9:00 AM" in body
        _assert_no_raw_iso(body)

    @pytest.mark.asyncio
    async def test_github_issue_body_renders_utc_label_for_unknown_user(self):
        """When no user resolves, the face falls back to UTC and says 'UTC'."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="test-org/test-repo")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 42, "html_url": "https://example.com/42"}
        )
        standup = _standup(GENERATED_AT_UTC_ISO)

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="UTC")):
            result = await skill._process_github_items(user_id=str(uuid4()), standup=standup)

        assert result["success"] is True
        body = skill.github_service.create_issue.await_args.kwargs["body"]

        assert "**Date**: " in body
        assert "UTC" in body
        _assert_no_raw_iso(body)

    @pytest.mark.asyncio
    async def test_github_issue_body_unparseable_generated_at_says_unknown(self):
        """An unparseable generated_at renders an honest 'unknown', never the raw value."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="test-org/test-repo")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 42, "html_url": "https://example.com/42"}
        )
        standup = _standup("not-a-real-timestamp")

        with patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="Asia/Tokyo")):
            await skill._process_github_items(user_id=str(uuid4()), standup=standup)

        body = skill.github_service.create_issue.await_args.kwargs["body"]
        assert "**Date**: unknown" in body
        assert "not-a-real-timestamp" not in body


# ---------------------------------------------------------------------------
# Direct coverage of the shared helper
# ---------------------------------------------------------------------------


class TestLabeledGeneratedAtHelper:
    def test_parses_aware_iso_to_labeled_face(self):
        from services.integrations.mcp.skills.standup_workflow_skill import (
            _labeled_generated_at,
        )

        face = _labeled_generated_at(GENERATED_AT_UTC_ISO, "Asia/Tokyo")
        assert face == "2026-01-15 9:00 AM JST"

    def test_missing_value_returns_none(self):
        from services.integrations.mcp.skills.standup_workflow_skill import (
            _labeled_generated_at,
        )

        assert _labeled_generated_at(None, "Asia/Tokyo") is None
        assert _labeled_generated_at("", "Asia/Tokyo") is None

    def test_unparseable_value_returns_none_not_raw_string(self):
        from services.integrations.mcp.skills.standup_workflow_skill import (
            _labeled_generated_at,
        )

        assert _labeled_generated_at("not-a-real-timestamp", "Asia/Tokyo") is None
