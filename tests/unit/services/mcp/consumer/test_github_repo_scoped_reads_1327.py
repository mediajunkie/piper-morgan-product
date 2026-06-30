"""#1327 gap 2 — GitHub OAuth-connector repo-scoped reads (branches/releases/issue #N).

The repo-scoped counterparts to #1322's user-wide `list_open_issues`/`list_open_prs`. Each
reads via the per-user OAuth connector (binding + grant → the github-mcp-server tool) AFTER
resolving the target repo through `resolve_repo()`. Repo-scoped reads REQUIRE a repo, so on
`UnresolvedRepoError` they honest-degrade with REPO_UNRESOLVED ("which repo?") — never
silent-empty, never get-all (#1231 / #1327 doc-of-record).

github-mcp-server tools used (authoritative, official README):
  branches → `list_branches`(owner, repo) · releases → `list_releases`(owner, repo) ·
  single issue → `issue_read`(owner, repo, issue_number, method="get").
  Milestones AND labels have NO list MCP tool → stay native (not tested here). github-mcp-server
  exposes only `get_label` (ONE label by name), not a list-labels tool; the gap-2 `list_label`
  cutover returned `unknown tool` live and was reverted.

TDD vs FastMCP fixtures (no live github-mcp-server needed); `resolve_repo` is monkeypatched.
"""

from __future__ import annotations

import contextlib
import json

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.shared.memory import create_connected_server_and_client_session  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.integrations.github.repo_resolver import (  # noqa: E402
    ResolvedRepo,
    UnresolvedRepoError,
)
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import DegradationReason  # noqa: E402
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_RESOLVED = ResolvedRepo(owner="octo", name="hello", source="user_default")

# Canned github-mcp-server payloads (REST-style JSON arrays, as the tools return them).
_BRANCHES = json.dumps(
    [
        {"name": "main", "protected": True, "commit": {"sha": "abc"}},
        {"name": "feature/x", "protected": False, "commit": {"sha": "def"}},
    ]
)
_RELEASES = json.dumps(
    [
        {"tag_name": "v1.2.0", "name": "1.2.0", "prerelease": False, "published_at": "2026-06-01T0:0:0Z"},
        {"tag_name": "v1.3.0-rc1", "name": "rc", "prerelease": True, "published_at": "2026-06-10T0:0:0Z"},
    ]
)
_ISSUE = json.dumps(
    {
        "number": 42,
        "title": "An issue",
        "state": "open",
        "body": "Body text",
        "labels": [{"name": "bug"}],
        "assignees": [{"login": "octo"}],
        "html_url": "http://x/42",
    }
)


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """In-memory ConnectorBinding store; the github adapter's session_scope points at it."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


@pytest.fixture
def resolves(monkeypatch):
    """resolve_repo → a concrete repo (the happy path)."""

    async def _ok(**kwargs):
        return _RESOLVED

    monkeypatch.setattr(gh_mod, "resolve_repo", _ok)


@pytest.fixture
def unresolved(monkeypatch):
    """resolve_repo → UnresolvedRepoError (no target repo → 'which repo?')."""

    async def _raise(**kwargs):
        raise UnresolvedRepoError("no repo")

    monkeypatch.setattr(gh_mod, "resolve_repo", _raise)


async def _seed(maker, status):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref="http://srv/mcp"
        )
        await s.commit()


def _point_at_fixture(adapter, *, tool, payload, raises=False):
    """Patch _mcp_client_ctx to yield a FastMCP-backed client exposing one named tool."""
    server = FastMCP("github-repo-scoped-fixture")

    # Tools take owner/repo (+ issue args); they ignore inputs and return the canned payload.
    @server.tool(name=tool)
    def _t(owner: str = "", repo: str = "", issue_number: int = 0, method: str = "") -> str:
        return payload

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        if raises:
            raise RuntimeError("server unreachable")
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


# ── Pattern read: branches (established end-to-end first) ──
class TestListBranchesConnector:
    async def test_no_binding_degrades_connect_required(self, sm, resolves):
        res = await GitHubMCPSpatialAdapter().list_branches_connector(_ALPHA)
        assert res.items is None
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED
        assert res.degradation.action_hint  # connect link surfaced (never silent-empty)

    async def test_non_bound_binding_degrades(self, sm, resolves):
        await _seed(sm, "unreachable")
        res = await GitHubMCPSpatialAdapter().list_branches_connector(_ALPHA)
        assert res.items is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_unresolved_repo_degrades_which_repo(self, sm, unresolved):
        # Bound, but no target repo → REPO_UNRESOLVED ("which repo?"), NOT a silent empty / get-all.
        await _seed(sm, "bound")
        res = await GitHubMCPSpatialAdapter().list_branches_connector(_ALPHA)
        assert res.items is None
        assert res.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert "which repo" in res.degradation.user_message.lower()

    async def test_bound_but_server_unreachable_degrades(self, sm, resolves):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._BRANCHES_TOOL, payload=_BRANCHES, raises=True)
        res = await adapter.list_branches_connector(_ALPHA)
        assert res.items is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_bound_returns_parsed_branches(self, sm, resolves):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._BRANCHES_TOOL, payload=_BRANCHES)
        res = await adapter.list_branches_connector(_ALPHA)
        assert res.degradation is None
        assert [b["name"] for b in res.items] == ["main", "feature/x"]
        assert res.items[0]["protected"] is True
        assert res.items[0]["commit_sha"] == "abc"  # normalized from commit.sha
        assert res.resolved_repo == "octo/hello"  # resolved repo surfaced for the handler

    async def test_bound_empty_payload_is_empty_list_not_degrade(self, sm, resolves):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._BRANCHES_TOOL, payload="[]")
        res = await adapter.list_branches_connector(_ALPHA)
        assert res.degradation is None
        assert res.items == []


# Labels: reverted to native (github-mcp-server has no list-labels tool, only get_label for ONE
# label) — no connector class here. Native-labels behavior: test_handlers_labels_branches_1040.py.


class TestListReleasesConnector:
    async def test_bound_returns_parsed_releases(self, sm, resolves):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._RELEASES_TOOL, payload=_RELEASES)
        res = await adapter.list_releases_connector(_ALPHA)
        assert res.degradation is None
        assert [r["tag_name"] for r in res.items] == ["v1.2.0", "v1.3.0-rc1"]
        assert res.items[0]["prerelease"] is False
        assert res.items[1]["prerelease"] is True

    async def test_unresolved_repo_degrades_which_repo(self, sm, unresolved):
        await _seed(sm, "bound")
        res = await GitHubMCPSpatialAdapter().list_releases_connector(_ALPHA)
        assert res.degradation.reason is DegradationReason.REPO_UNRESOLVED


class TestReviewIssueConnector:
    async def test_bound_returns_parsed_issue_via_issue_read(self, sm, resolves):
        # Fixture exposes ONLY issue_read → proves get_issue_connector uses that tool with method=get.
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._ISSUE_READ_TOOL, payload=_ISSUE)
        res = await adapter.get_issue_connector(_ALPHA, issue_number=42)
        assert res.degradation is None
        assert res.item["number"] == 42
        assert res.item["title"] == "An issue"
        assert res.resolved_repo == "octo/hello"

    async def test_unresolved_repo_degrades_which_repo(self, sm, unresolved):
        await _seed(sm, "bound")
        res = await GitHubMCPSpatialAdapter().get_issue_connector(_ALPHA, issue_number=42)
        assert res.item is None
        assert res.degradation.reason is DegradationReason.REPO_UNRESOLVED

    async def test_no_binding_degrades_connect_required(self, sm, resolves):
        res = await GitHubMCPSpatialAdapter().get_issue_connector(_ALPHA, issue_number=42)
        assert res.item is None
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_explicit_repo_passed_to_resolver(self, sm, monkeypatch):
        # "issue #N in owner/name" → explicit repo threaded into resolve_repo.
        await _seed(sm, "bound")
        seen = {}

        async def _capture(**kwargs):
            seen.update(kwargs)
            return _RESOLVED

        monkeypatch.setattr(gh_mod, "resolve_repo", _capture)
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, tool=gh_mod._ISSUE_READ_TOOL, payload=_ISSUE)
        await adapter.get_issue_connector(_ALPHA, issue_number=42, explicit_repo="foo/bar")
        assert seen.get("explicit") == "foo/bar"
