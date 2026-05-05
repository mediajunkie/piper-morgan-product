"""Unit tests for GitHub adapter list_labels + list_branches + get_repository_info (Issue #1040)."""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter


@pytest.fixture
def adapter() -> GitHubMCPSpatialAdapter:
    a = GitHubMCPSpatialAdapter()
    a._call_github_api = AsyncMock()
    return a


class TestListLabels:
    """Adapter list_labels — Issue #1040."""

    async def test_returns_normalized_labels(self, adapter):
        adapter._call_github_api.return_value = [
            {
                "name": "bug",
                "color": "d73a4a",
                "description": "Something isn't working",
                "url": "https://api.github.com/repos/o/r/labels/bug",
            },
            {
                "name": "enhancement",
                "color": "a2eeef",
                "description": None,
                "url": "https://api.github.com/repos/o/r/labels/enhancement",
            },
        ]
        result = await adapter.list_labels("r", "o")
        assert len(result) == 2
        assert result[0]["name"] == "bug"
        assert result[0]["color"] == "d73a4a"
        assert result[1]["description"] == ""  # None → empty string
        adapter._call_github_api.assert_awaited_once_with(
            "repos/o/r/labels", {"per_page": 100}
        )

    async def test_empty_response(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.list_labels("r", "o") == []

    async def test_exception_returns_empty_list(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("boom")
        assert await adapter.list_labels("r", "o") == []

    async def test_required_args_no_defaults(self, adapter):
        with pytest.raises(TypeError):
            await adapter.list_labels()  # type: ignore[call-arg]
        with pytest.raises(TypeError):
            await adapter.list_labels("r")  # type: ignore[call-arg]


class TestListBranches:
    """Adapter list_branches — Issue #1040."""

    async def test_returns_normalized_branches(self, adapter):
        adapter._call_github_api.return_value = [
            {
                "name": "main",
                "protected": True,
                "commit": {"sha": "abc123"},
            },
            {
                "name": "claude/feature-x",
                "protected": False,
                "commit": {"sha": "def456"},
            },
        ]
        result = await adapter.list_branches("r", "o")
        assert len(result) == 2
        assert result[0]["name"] == "main"
        assert result[0]["protected"] is True
        assert result[0]["commit_sha"] == "abc123"
        assert result[1]["protected"] is False

    async def test_handles_missing_commit(self, adapter):
        adapter._call_github_api.return_value = [
            {"name": "stale", "protected": False, "commit": None}
        ]
        result = await adapter.list_branches("r", "o")
        assert result[0]["commit_sha"] == ""

    async def test_empty_response(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.list_branches("r", "o") == []

    async def test_exception_returns_empty_list(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("boom")
        assert await adapter.list_branches("r", "o") == []

    async def test_required_args_no_defaults(self, adapter):
        with pytest.raises(TypeError):
            await adapter.list_branches()  # type: ignore[call-arg]


class TestGetRepositoryInfo:
    """Adapter get_repository_info (used to identify default_branch) — Issue #1040."""

    async def test_returns_default_branch(self, adapter):
        adapter._call_github_api.return_value = {
            "name": "myrepo",
            "full_name": "octocat/myrepo",
            "default_branch": "main",
            "html_url": "https://github.com/octocat/myrepo",
        }
        result = await adapter.get_repository_info("myrepo", "octocat")
        assert result is not None
        assert result["default_branch"] == "main"
        assert result["full_name"] == "octocat/myrepo"

    async def test_none_response(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.get_repository_info("r", "o") is None

    async def test_exception_returns_none(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("boom")
        assert await adapter.get_repository_info("r", "o") is None


class TestEndpointPaths:
    """Per #1042: endpoint paths use {owner}/{repo} from required args."""

    async def test_labels_endpoint_uses_args(self, adapter):
        adapter._call_github_api.return_value = []
        await adapter.list_labels("special-repo", "octocat")
        endpoint = adapter._call_github_api.call_args.args[0]
        assert "octocat/special-repo" in endpoint
        assert "mediajunkie" not in endpoint
        assert "piper-morgan" not in endpoint

    async def test_branches_endpoint_uses_args(self, adapter):
        adapter._call_github_api.return_value = []
        await adapter.list_branches("special-repo", "octocat")
        endpoint = adapter._call_github_api.call_args.args[0]
        assert "octocat/special-repo" in endpoint
        assert "mediajunkie" not in endpoint
