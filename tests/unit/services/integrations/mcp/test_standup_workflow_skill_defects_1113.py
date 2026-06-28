"""Tests for #1113 StandupWorkflowSkill 4-defect cleanup.

Covers four defects surfaced when #693 wired the placeholder gates open:

1. Instantiation: ``SessionPersistenceManager()`` previously raised TypeError
   for missing ``preference_manager``. Now reuses one shared
   UserPreferenceManager across workflow + session persistence.

2. ``_process_github_items`` previously called ``create_issue(repo=...)``;
   GitHubDomainService.create_issue accepts ``repo_name=`` (fixed in #1112).

3. ``_update_notion`` previously referenced ``self._notion_service`` which
   was never initialized; now NotionDomainService is instantiated in
   ``__init__`` AND the call uses ``parent_id=`` to match the real signature.

4. Dead close-issue loop removed: ``_extract_completed_items`` always
   returned ``[]`` and called nonexistent ``close_issue_by_title``.
"""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest


SKILL_MODULE = "services.integrations.mcp.skills.standup_workflow_skill"


@contextmanager
def _patched_skill_deps():
    """Patch all the skill's heavy dependencies for in-process instantiation.

    #1289: MorningStandupWorkflow / StandupOrchestrationService /
    SessionPersistenceManager are no longer imported by the skill; patches removed.
    """
    with (
        patch(f"{SKILL_MODULE}.GitHubDomainService"),
        patch(f"{SKILL_MODULE}.SlackDomainService"),
        patch(f"{SKILL_MODULE}.NotionDomainService"),
        patch(f"{SKILL_MODULE}.UserPreferenceManager"),
    ):
        yield


def _make_skill():
    """Construct a StandupWorkflowSkill with all heavy deps patched."""
    from services.integrations.mcp.skills.standup_workflow_skill import (
        StandupWorkflowSkill,
    )

    with _patched_skill_deps():
        return StandupWorkflowSkill()


# -------------------------------------------------------------------
# Defect 1 — Instantiation: SessionPersistenceManager needs preference_manager
# -------------------------------------------------------------------


class TestDefect1Instantiation:
    """Skill construction is clean after #1289 swap.

    #1289 retired MorningStandupWorkflow + StandupOrchestrationService +
    SessionPersistenceManager from the skill. The old defect was a TypeError
    because SessionPersistenceManager needed preference_manager; the fix was
    sharing one UserPreferenceManager. #1289 goes further: these three classes
    are no longer imported, so the TypeError can never recur.
    """

    def test_skill_instantiates_without_error(self):
        """Construction with only domain services patched must not raise."""
        from services.integrations.mcp.skills.standup_workflow_skill import (
            StandupWorkflowSkill,
        )

        with (
            patch(f"{SKILL_MODULE}.GitHubDomainService"),
            patch(f"{SKILL_MODULE}.SlackDomainService"),
            patch(f"{SKILL_MODULE}.NotionDomainService"),
        ):
            # UserPreferenceManager NOT patched — exercises real wiring in _WorkflowShim.
            skill = StandupWorkflowSkill()

        # Skill exists, all expected services initialized
        assert skill.workflow is not None
        assert skill.workflow.preference_manager is not None
        assert skill.github_service is not None
        assert skill.slack_service is not None
        assert skill._notion_service is not None
        # orchestration is gone (#1289)
        assert not hasattr(skill, "orchestration")

    def test_workflow_shim_holds_preference_manager(self):
        """The _WorkflowShim wraps a UserPreferenceManager so preference helpers work."""
        from services.integrations.mcp.skills.standup_workflow_skill import (
            StandupWorkflowSkill,
            _WorkflowShim,
        )

        with (
            patch(f"{SKILL_MODULE}.GitHubDomainService"),
            patch(f"{SKILL_MODULE}.SlackDomainService"),
            patch(f"{SKILL_MODULE}.NotionDomainService"),
            patch(f"{SKILL_MODULE}.UserPreferenceManager") as MockPrefMgr,
        ):
            pref_instance = MagicMock()
            MockPrefMgr.return_value = pref_instance

            skill = StandupWorkflowSkill()

        # _WorkflowShim stores the pref instance; helpers read through .preference_manager
        assert isinstance(skill.workflow, _WorkflowShim)
        assert skill.workflow.preference_manager is pref_instance


# -------------------------------------------------------------------
# Defect 2 — _process_github_items uses repo_name= kwarg
# -------------------------------------------------------------------


class TestDefect2CreateIssueKwarg:
    """Verify create_issue is called with repo_name= not repo=."""

    @pytest.mark.asyncio
    async def test_create_issue_called_with_repo_name_kwarg(self):
        """When action items resolve, create_issue receives repo_name=."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="test-org/test-repo")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 42, "html_url": "https://example.com/42"}
        )

        standup = {
            "today_priorities": ["Deploy feature"],
            "blockers": [],
            "generated_at": "2026-05-24",
            "user_id": str(uuid4()),
        }

        result = await skill._process_github_items(user_id=str(uuid4()), standup=standup)

        assert result["success"] is True
        assert result["issues_created"] == 1
        skill.github_service.create_issue.assert_awaited_once()
        # Verify it was a kwarg (not positional) call with the right name
        kwargs = skill.github_service.create_issue.await_args.kwargs
        assert kwargs.get("repo_name") == "test-org/test-repo"
        assert "repo" not in kwargs  # The OLD broken kwarg must NOT appear

    @pytest.mark.asyncio
    async def test_no_repo_returns_failure_envelope(self):
        """When _get_user_github_repo returns None, no create_issue call made."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value=None)
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock()

        standup = {"today_priorities": ["x"], "blockers": [], "generated_at": "now"}
        result = await skill._process_github_items(str(uuid4()), standup)

        assert result["success"] is False
        assert "No GitHub repo configured" in result["message"]
        skill.github_service.create_issue.assert_not_awaited()


# -------------------------------------------------------------------
# Defect 3 — _notion_service initialized + create_page uses parent_id
# -------------------------------------------------------------------


class TestDefect3NotionService:
    """_notion_service exists; create_page called with correct kwargs."""

    def test_notion_service_initialized_in_constructor(self):
        """``self._notion_service`` is an attribute set during __init__."""
        skill = _make_skill()
        assert hasattr(skill, "_notion_service")
        assert skill._notion_service is not None

    @pytest.mark.asyncio
    async def test_update_notion_calls_create_page_with_parent_id(self):
        """create_page receives parent_id (matching NotionDomainService sig),
        not database_id (the old broken kwarg)."""
        skill = _make_skill()
        skill._get_user_notion_database = AsyncMock(return_value="db-abc-123")
        skill._notion_service = MagicMock()
        skill._notion_service.create_page = AsyncMock(return_value={"id": "page-xyz-789"})

        standup = {
            "generated_at": "2026-05-24",
            "summary": "summary text",
            "yesterday_accomplishments": ["a1"],
            "today_priorities": ["p1"],
            "blockers": [],
            "time_saved_minutes": 30,
        }

        result = await skill._update_notion(user_id="u1", standup=standup)

        assert result["success"] is True
        assert result["page_id"] == "page-xyz-789"
        assert result["database_id"] == "db-abc-123"

        skill._notion_service.create_page.assert_awaited_once()
        kwargs = skill._notion_service.create_page.await_args.kwargs
        assert kwargs.get("parent_id") == "db-abc-123"
        assert "database_id" not in kwargs  # OLD broken kwarg must NOT appear
        # Properties payload carries the standup data
        assert kwargs["properties"]["summary"] == "summary text"

    @pytest.mark.asyncio
    async def test_update_notion_handles_none_result_from_domain_service(self):
        """NotionDomainService.create_page returns Optional[Dict] and can be
        None on API failure — handle that branch."""
        skill = _make_skill()
        skill._get_user_notion_database = AsyncMock(return_value="db-abc")
        skill._notion_service = MagicMock()
        skill._notion_service.create_page = AsyncMock(return_value=None)

        result = await skill._update_notion(user_id="u1", standup={})

        assert result["success"] is False
        assert "API error" in result["message"]

    @pytest.mark.asyncio
    async def test_update_notion_no_db_returns_failure_envelope(self):
        """When _get_user_notion_database returns None, no create_page call."""
        skill = _make_skill()
        skill._get_user_notion_database = AsyncMock(return_value=None)
        skill._notion_service = MagicMock()
        skill._notion_service.create_page = AsyncMock()

        result = await skill._update_notion(user_id="u1", standup={})

        assert result["success"] is False
        assert "No Notion database configured" in result["message"]
        skill._notion_service.create_page.assert_not_awaited()


# -------------------------------------------------------------------
# Defect 4 — close-issue loop + _extract_completed_items removed
# -------------------------------------------------------------------


class TestDefect4DeadCloseLoopRemoved:
    """Verify the dead loop is gone and no calls to close_issue_by_title."""

    def test_extract_completed_items_method_removed(self):
        """The placeholder helper no longer exists on the class."""
        from services.integrations.mcp.skills.standup_workflow_skill import (
            StandupWorkflowSkill,
        )

        assert not hasattr(StandupWorkflowSkill, "_extract_completed_items")

    @pytest.mark.asyncio
    async def test_process_github_items_does_not_call_close_issue_by_title(self):
        """Even with successful create_issue calls, no close attempt happens."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="org/repo")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 1, "html_url": "https://x"}
        )
        # If the dead loop returned, it would try to call this — should NEVER be
        # called regardless of what the standup contains.
        skill.github_service.close_issue_by_title = AsyncMock(
            side_effect=AssertionError(
                "close_issue_by_title must not be called — dead loop removed in #1113"
            )
        )

        standup = {
            "today_priorities": ["t1"],
            "blockers": ["b1"],
            "generated_at": "now",
        }
        result = await skill._process_github_items(str(uuid4()), standup)

        assert result["success"] is True
        # issues_closed must be 0 (placeholder removed; no real close happening)
        assert result["issues_closed"] == 0
        skill.github_service.close_issue_by_title.assert_not_awaited()


# -------------------------------------------------------------------
# Combined: existing behavior (issues_closed key) preserved
# -------------------------------------------------------------------


class TestBackwardsCompatibility:
    """The result envelope shape stays the same so existing tests don't break."""

    @pytest.mark.asyncio
    async def test_result_envelope_still_includes_issues_closed_key(self):
        """Even though we deleted the close loop, the result still has the key
        (value: 0). Existing tests in test_standup_workflow_skill.py that
        check ``result["issues_closed"]`` continue to work."""
        skill = _make_skill()
        skill._get_user_github_repo = AsyncMock(return_value="o/r")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(
            return_value={"number": 1, "html_url": "https://x"}
        )

        standup = {"today_priorities": [], "blockers": [], "generated_at": "x"}
        result = await skill._process_github_items(str(uuid4()), standup)

        assert "issues_closed" in result
        assert result["issues_closed"] == 0
