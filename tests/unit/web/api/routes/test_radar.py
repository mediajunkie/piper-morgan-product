"""#1236 — /api/v1/radar route. Tests the real wiring (route → _build_feed →
ConversationEntitySource → RadarFeed → response), mocking only the external
UserHistoryService (per the #490 wiring-test lesson — don't mock internals).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from services.integrations.github.repo_resolver import read_user_github_handle
from services.radar import WorkItemEntitySource
from services.radar.feed_factory import (  # #1269: source wiring moved here (shared w/ standup)
    WorkItemProvider,
    filter_issues_by_assignee,
)
from web.api.routes.radar import _build_feed, get_radar


def _summary(cid, title, last_activity, turns=2):
    return SimpleNamespace(
        conversation_id=cid,
        title=title,
        last_activity=last_activity,
        turn_count=turns,
        topics=[],
        preview="...",
        is_private=False,
    )


class _FakeHistoryService:
    def __init__(self, conversations):
        self._conversations = conversations

    async def get_history(self, user_id, page, page_size, include_private):
        return SimpleNamespace(
            conversations=self._conversations,
            total_count=len(self._conversations),
            page=page,
            page_size=page_size,
            has_more=False,
        )


_USER = SimpleNamespace(sub="user-1")


async def test_radar_populated_is_attention_first_and_observed():
    now = datetime.now(timezone.utc)
    older = now - timedelta(days=400)
    svc = _FakeHistoryService([_summary("c1", "old chat", older), _summary("c2", "new chat", now)])
    view = await get_radar(current_user=_USER, service=svc)

    assert view.state == "populated"
    # attention-first: most-recent last_activity at the top
    assert [e.title for e in view.entities] == ["new chat", "old chat"]
    assert all(e.entity_type == "Conversation" for e in view.entities)
    assert all(e.provenance == "observed" for e in view.entities)
    assert view.entities[0].ref == "c2"


async def test_radar_empty_returns_one_example():
    view = await get_radar(current_user=_USER, service=_FakeHistoryService([]))
    assert view.state == "empty"
    assert len(view.entities) == 1
    assert view.entities[0].provenance == "example"


async def test_radar_lifecycle_derived_from_recency():
    now = datetime.now(timezone.utc)
    svc = _FakeHistoryService([_summary("c1", "fresh", now)])
    view = await get_radar(current_user=_USER, service=svc)
    assert view.entities[0].lifecycle_state == "active"  # recent → active


# --- #1239: WorkItem source registration + graceful-empty contract ---


def test_workitem_source_registered_in_feed():
    """#1239: the live feed wires a WorkItemEntitySource alongside the others."""
    feed = _build_feed(_FakeHistoryService([]))
    assert any(isinstance(s, WorkItemEntitySource) for s in feed._sources)


async def test_workitem_provider_returns_empty_when_github_unavailable(monkeypatch):
    """A GitHub hiccup must NEVER blank Radar — the provider degrades to [] (and
    RadarFeed's per-source isolation is the second guard). #1239 beta path.
    (#1547: gate patched configured=True so the hiccup path is actually reached.)"""
    from unittest.mock import AsyncMock, patch

    import services.integrations.github.github_integration_router as ghmod

    class _BoomRouter:
        def __init__(self, *a, **k):
            raise RuntimeError("github down")

    monkeypatch.setattr(ghmod, "GitHubIntegrationRouter", _BoomRouter)
    with patch(
        "services.integrations.integration_status_service."
        "IntegrationStatusService.is_configured",
        new=AsyncMock(return_value=True),
    ):
        assert await WorkItemProvider().list_for_user("user-1") == []


# --- #6: scope work items to "assigned to me" via the configured GitHub handle ---


def _issue(num, assignees):
    return {"number": num, "title": f"#{num}", "state": "open", "assignees": assignees}


class TestWorkItemAssigneeFilter:
    def test_no_handle_returns_all(self):
        """Opt-in: with no handle configured, all open issues show (prior behavior)."""
        issues = [_issue(1, ["alice"]), _issue(2, [])]
        assert filter_issues_by_assignee(issues, None) == issues
        assert filter_issues_by_assignee(issues, "") == issues

    def test_handle_filters_to_assigned(self):
        """With a handle, only issues assigned to it survive ('what's on my plate')."""
        issues = [_issue(1, ["alice", "bob"]), _issue(2, ["carol"]), _issue(3, [])]
        assert [i["number"] for i in filter_issues_by_assignee(issues, "bob")] == [1]

    def test_handle_is_case_insensitive(self):
        assert len(filter_issues_by_assignee([_issue(1, ["MediaJunkie"])], "mediajunkie")) == 1

    def test_empty_or_missing_assignees(self):
        assert filter_issues_by_assignee(None, "bob") == []
        assert filter_issues_by_assignee([{"number": 9}], "bob") == []  # no assignees key

    async def test_handle_reader_env_fallback(self, monkeypatch):
        """No DB config entry + env set → the env handle (single-user beta config).

        WS-1 P4: the handle reader is now async + DB-backed (connector_configs is the SOLE
        store). Patch the DB read to an empty config so the env fallback is the only source.
        """
        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "octocat")
        with patch(
            "services.connectors.config_service.ConnectorConfigService.get_config",
            new=AsyncMock(return_value={}),
        ):
            assert await read_user_github_handle("no-such-user-uuid") == "octocat"

    async def test_handle_reader_none_when_unset(self, monkeypatch):
        """No DB config entry + no env → None → callers apply no filter (show all)."""
        monkeypatch.delenv("PIPER_GITHUB_HANDLE", raising=False)
        with patch(
            "services.connectors.config_service.ConnectorConfigService.get_config",
            new=AsyncMock(return_value={}),
        ):
            assert await read_user_github_handle("no-such-user-uuid") is None

    async def test_handle_reader_db_value_used(self, monkeypatch):
        """WS-1 P4: a ``github_username`` in the DB config is returned (and beats the env var)."""
        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "envhandle")
        with patch(
            "services.connectors.config_service.ConnectorConfigService.get_config",
            new=AsyncMock(return_value={"github_username": "dbhandle"}),
        ):
            assert await read_user_github_handle(uuid4()) == "dbhandle"
