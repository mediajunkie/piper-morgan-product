"""Unit tests for GitHub adapter list_milestones + list_releases (Issue #1039)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter


@pytest.fixture
def adapter() -> GitHubMCPSpatialAdapter:
    a = GitHubMCPSpatialAdapter()
    # Patch _call_github_api to avoid real network calls
    a._call_github_api = AsyncMock()
    return a


class TestListMilestones:
    """Adapter list_milestones — Issue #1039."""

    async def test_returns_normalized_milestones(self, adapter):
        adapter._call_github_api.return_value = [
            {
                "title": "v1.0",
                "number": 1,
                "state": "open",
                "due_on": "2026-06-01T00:00:00Z",
                "open_issues": 5,
                "closed_issues": 10,
                "html_url": "https://github.com/o/r/milestone/1",
                "description": "First major release",
            },
            {
                "title": "v0.9",
                "number": 2,
                "state": "open",
                "due_on": None,
                "open_issues": 3,
                "closed_issues": 0,
                "html_url": "https://github.com/o/r/milestone/2",
                "description": None,
            },
        ]
        result = await adapter.list_milestones("myrepo", "myorg")
        assert len(result) == 2
        assert result[0]["title"] == "v1.0"
        assert result[0]["open_issues"] == 5
        assert result[1]["description"] == ""  # None → empty string
        adapter._call_github_api.assert_awaited_once_with(
            "repos/myorg/myrepo/milestones",
            {"state": "open", "per_page": 100},
        )

    async def test_state_kwarg_threaded(self, adapter):
        adapter._call_github_api.return_value = []
        await adapter.list_milestones("r", "o", state="closed")
        adapter._call_github_api.assert_awaited_once_with(
            "repos/o/r/milestones",
            {"state": "closed", "per_page": 100},
        )

    async def test_empty_response_returns_empty_list(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.list_milestones("r", "o") == []

    async def test_exception_returns_empty_list(self, adapter):
        adapter._call_github_api.side_effect = Exception("api boom")
        assert await adapter.list_milestones("r", "o") == []

    async def test_required_args_no_defaults(self, adapter):
        # Cannot call without repo + owner — TypeError on missing positional args
        with pytest.raises(TypeError):
            await adapter.list_milestones()  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            await adapter.list_milestones("r")  # type: ignore[call-arg]


class TestListReleases:
    """Adapter list_releases — Issue #1039."""

    async def test_returns_normalized_releases(self, adapter):
        adapter._call_github_api.return_value = [
            {
                "tag_name": "v1.0.0",
                "name": "First Major Release",
                "published_at": "2026-05-01T12:00:00Z",
                "prerelease": False,
                "draft": False,
                "html_url": "https://github.com/o/r/releases/v1.0.0",
                "body": "Release notes here",
            },
            {
                "tag_name": "v1.1.0-beta",
                "name": None,  # name absence falls back to tag_name
                "published_at": "2026-05-04T08:00:00Z",
                "prerelease": True,
                "draft": False,
                "html_url": "https://github.com/o/r/releases/v1.1.0-beta",
                "body": None,
            },
        ]
        result = await adapter.list_releases("r", "o")
        assert len(result) == 2
        assert result[0]["tag_name"] == "v1.0.0"
        assert result[0]["prerelease"] is False
        assert result[1]["name"] == "v1.1.0-beta"  # fell back to tag_name
        assert result[1]["prerelease"] is True
        assert result[1]["body"] == ""  # None → empty string

    async def test_body_truncation(self, adapter):
        long_body = "x" * 1000
        adapter._call_github_api.return_value = [
            {
                "tag_name": "v1.0",
                "name": "v1.0",
                "published_at": "2026-05-01T12:00:00Z",
                "prerelease": False,
                "draft": False,
                "html_url": "u",
                "body": long_body,
            }
        ]
        result = await adapter.list_releases("r", "o")
        assert len(result[0]["body"]) == 503  # 500 + "..."
        assert result[0]["body"].endswith("...")

    async def test_empty_response(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.list_releases("r", "o") == []

    async def test_exception_returns_empty_list(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("boom")
        assert await adapter.list_releases("r", "o") == []

    async def test_required_args_no_defaults(self, adapter):
        with pytest.raises(TypeError):
            await adapter.list_releases()  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            await adapter.list_releases("r")  # type: ignore[call-arg]


class TestEndpointPaths:
    """Per #1042: endpoint paths use {owner}/{repo} from required args, no
    hardcoded mediajunkie/piper-morgan-product."""

    async def test_milestones_endpoint_uses_args(self, adapter):
        adapter._call_github_api.return_value = []
        await adapter.list_milestones("special-repo", "octocat")
        endpoint = adapter._call_github_api.call_args.args[0]
        assert "octocat/special-repo" in endpoint
        assert "mediajunkie" not in endpoint
        assert "piper-morgan" not in endpoint

    async def test_releases_endpoint_uses_args(self, adapter):
        adapter._call_github_api.return_value = []
        await adapter.list_releases("special-repo", "octocat")
        endpoint = adapter._call_github_api.call_args.args[0]
        assert "octocat/special-repo" in endpoint
        assert "mediajunkie" not in endpoint
        assert "piper-morgan" not in endpoint
