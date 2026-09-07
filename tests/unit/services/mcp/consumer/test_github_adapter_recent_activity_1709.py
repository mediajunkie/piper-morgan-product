"""#1709 — GitHubMCPSpatialAdapter.get_recent_activity, the layer below the #1646 pins.

Layer named (m-43): these tests mock the adapter's REST transport helper
``_call_github_api`` (the same seam every sibling adapter suite mocks —
#1039/#1040/#969 idiom), so everything from the operation's signature down to
endpoint construction, window filtering, and item shaping is REAL; only the
HTTP round-trip is not. The repo-resolution path additionally patches
``resolve_repo`` at the adapter's import site.

The return-shape assertions here are the CONSUMERS' navigations verbatim:
- analyze_commits / _format_commit_report: ``commit.commit.author.name``,
  ``commit.commit.author.date``, ``commit.commit.message``
- _analyze_contributor_stats: ``item["author"]`` as a flat string on
  commits, PRs, and issues
- _handle_temporal_last_activity (#504): ``created_at``/``updated_at`` +
  ``title``/``message`` on every item
- the #1646 fixtures' four-key shape: commits / prs / issues_created /
  issues_closed
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.github.repo_resolver import UnresolvedRepoError
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

FOUR_KEYS = {"commits", "prs", "issues_created", "issues_closed"}
EMPTY = {"commits": [], "prs": [], "issues_created": [], "issues_closed": []}


def _iso(days_ago: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _commit(sha="abc123", name="Ada", date=None, message="fix: the thing\n\nbody", login="ada-gh"):
    return {
        "sha": sha,
        "html_url": f"https://github.com/o/r/commit/{sha}",
        "commit": {"message": message, "author": {"name": name, "date": date or _iso(1)}},
        "author": {"login": login},
    }


def _issue(number, *, created, closed=None, login="ada-gh", pr=False, title="An item"):
    item = {
        "number": number,
        "title": title,
        "state": "closed" if closed else "open",
        "created_at": created,
        "updated_at": closed or created,
        "closed_at": closed,
        "html_url": f"https://github.com/o/r/issues/{number}",
        "user": {"login": login},
    }
    if pr:
        item["pull_request"] = {"url": f"https://api.github.com/repos/o/r/pulls/{number}"}
    return item


@pytest.fixture
def adapter() -> GitHubMCPSpatialAdapter:
    a = GitHubMCPSpatialAdapter()
    a._call_github_api = AsyncMock(return_value=[])
    return a


class TestEndpointsAndScoping:
    """The resolved repository reaches the wire — the layer-below half of #1646's pin."""

    async def test_explicit_repository_scopes_both_endpoints(self, adapter):
        await adapter.get_recent_activity(7, repository="octocat/hello-world")
        endpoints = [c.args[0] for c in adapter._call_github_api.await_args_list]
        assert endpoints == [
            "repos/octocat/hello-world/commits",
            "repos/octocat/hello-world/issues",
        ]

    async def test_days_window_becomes_the_since_param(self, adapter):
        await adapter.get_recent_activity(30, repository="o/r")
        for call in adapter._call_github_api.await_args_list:
            since = call.args[1]["since"]
            # since ≈ now - 30d (parseable, within an hour of the target)
            parsed = datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            target = datetime.now(timezone.utc) - timedelta(days=30)
            assert abs((parsed - target).total_seconds()) < 3600
        issues_call = adapter._call_github_api.await_args_list[1]
        assert issues_call.args[1]["state"] == "all"

    async def test_none_repository_resolves_via_resolve_repo(self, adapter):
        from services.integrations.github.repo_resolver import ResolvedRepo

        resolved = ResolvedRepo(owner="envowner", name="envrepo", source="env_var")
        with patch(
            "services.mcp.consumer.github_adapter.resolve_repo",
            new=AsyncMock(return_value=resolved),
        ):
            result = await adapter.get_recent_activity(7)
        endpoints = [c.args[0] for c in adapter._call_github_api.await_args_list]
        assert endpoints[0] == "repos/envowner/envrepo/commits"
        assert set(result.keys()) == FOUR_KEYS

    async def test_none_repository_unresolvable_returns_empty_shape_no_fetch(self, adapter):
        with patch(
            "services.mcp.consumer.github_adapter.resolve_repo",
            new=AsyncMock(side_effect=UnresolvedRepoError()),
        ):
            result = await adapter.get_recent_activity(7)
        assert result == EMPTY
        adapter._call_github_api.assert_not_awaited()

    async def test_bare_repo_name_without_owner_returns_empty_shape_no_fetch(self, adapter):
        result = await adapter.get_recent_activity(7, repository="just-a-name")
        assert result == EMPTY
        adapter._call_github_api.assert_not_awaited()


class TestReturnShapeMatchesConsumers:
    async def test_commit_items_carry_the_nested_and_flat_shapes(self, adapter):
        adapter._call_github_api.side_effect = [
            [_commit(name="Ada", message="feat: ship it\n\ndetails", login="ada-gh")],
            [],
        ]
        result = await adapter.get_recent_activity(7, repository="o/r")
        assert set(result.keys()) == FOUR_KEYS
        (c,) = result["commits"]
        # analyze_commits / _format_commit_report navigation:
        assert c["commit"]["author"]["name"] == "Ada"
        assert c["commit"]["message"].startswith("feat: ship it")
        assert c["commit"]["author"]["date"]
        # contributor-stats navigation (flat string author):
        assert c["author"] == "ada-gh"
        # temporal last-activity navigation (sortable timestamp + message):
        assert c["created_at"] and c["message"] == "feat: ship it"

    async def test_commit_without_linked_user_falls_back_to_commit_author_name(self, adapter):
        raw = _commit(name="Ada Lovelace")
        raw["author"] = None  # commits by unlinked emails have author: null
        adapter._call_github_api.side_effect = [[raw], []]
        result = await adapter.get_recent_activity(7, repository="o/r")
        assert result["commits"][0]["author"] == "Ada Lovelace"

    async def test_prs_and_issues_classified_and_carry_flat_author(self, adapter):
        adapter._call_github_api.side_effect = [
            [],
            [
                _issue(1, created=_iso(2), pr=True, login="pr-author"),
                _issue(2, created=_iso(3), login="issue-author"),  # created in window
                _issue(3, created=_iso(40), closed=_iso(1)),  # closed in window only
                _issue(4, created=_iso(40)),  # merely updated — neither list
            ],
        ]
        result = await adapter.get_recent_activity(7, repository="o/r")
        assert [p["number"] for p in result["prs"]] == [1]
        assert result["prs"][0]["author"] == "pr-author"
        assert [i["number"] for i in result["issues_created"]] == [2]
        assert result["issues_created"][0]["author"] == "issue-author"
        assert [i["number"] for i in result["issues_closed"]] == [3]

    async def test_issue_created_and_closed_in_window_appears_in_both(self, adapter):
        adapter._call_github_api.side_effect = [
            [],
            [_issue(9, created=_iso(2), closed=_iso(1))],
        ]
        result = await adapter.get_recent_activity(7, repository="o/r")
        assert [i["number"] for i in result["issues_created"]] == [9]
        assert [i["number"] for i in result["issues_closed"]] == [9]

    async def test_issue_items_carry_temporal_navigation_fields(self, adapter):
        adapter._call_github_api.side_effect = [[], [_issue(5, created=_iso(1), title="Fix login")]]
        result = await adapter.get_recent_activity(7, repository="o/r")
        (i,) = result["issues_created"]
        assert i["title"] == "Fix login"
        assert i["created_at"] and i["updated_at"]


class TestFailureIsTheEmptyShape:
    """House shape for this seam (#969/#1039 siblings): empty, never None, never raise."""

    async def test_api_none_responses_yield_empty_shape(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.get_recent_activity(7, repository="o/r") == EMPTY

    async def test_api_exception_yields_empty_shape(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("api boom")
        assert await adapter.get_recent_activity(7, repository="o/r") == EMPTY
