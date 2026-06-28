"""#1322 P1 — GitHub OAuth-connector issue fetch (the chat-cutover read primitive).

`GitHubMCPSpatialAdapter.list_open_issues(user_id)` reads the user's open issues over the
per-user OAuth connector (binding + grant → `search_issues`), honest-degrade throughout
(#1231 — never a silent empty). This is the primitive the chat handlers
(`_handle_list_issues_query` + siblings) cut over to, replacing the native shared-PAT path.
TDD vs a FastMCP `search_issues` fixture (no live github-mcp-server needed); the live
round-trip was de-risked separately (179 real issues).
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
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import DegradationReason  # noqa: E402
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"

# A canned github-mcp-server search_issues payload (the real shape: total_count + items[]).
_PAYLOAD = json.dumps(
    {
        "total_count": 2,
        "items": [
            {"number": 42, "title": "First open issue", "labels": [{"name": "bug"}]},
            {"number": 43, "title": "Second open issue", "labels": []},
        ],
    }
)
_EMPTY = json.dumps({"total_count": 0, "items": []})


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


async def _seed(maker, status):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref="http://srv/mcp"
        )
        await s.commit()


def _point_at_fixture(adapter, *, payload=_PAYLOAD, raises=False, tool=None):
    """Patch _mcp_client_ctx to yield a FastMCP-backed client exposing the given search tool."""
    server = FastMCP("github-search-fixture")

    @server.tool(name=tool or gh_mod._ISSUES_TOOL)
    def search(query: str) -> str:
        return payload

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        if raises:
            raise RuntimeError("server unreachable")
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestListOpenIssuesDegradeRail:
    async def test_no_binding_degrades_connect_required(self, sm):
        res = await GitHubMCPSpatialAdapter().list_open_issues(_ALPHA)
        assert res.issues is None
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED
        assert res.degradation.action_hint  # connect link surfaced (never silent-empty)

    async def test_non_bound_binding_degrades(self, sm):
        await _seed(sm, "unreachable")
        res = await GitHubMCPSpatialAdapter().list_open_issues(_ALPHA)
        assert res.issues is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_bound_but_server_unreachable_degrades(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, raises=True)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.issues is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE


class TestListOpenIssuesHit:
    async def test_bound_returns_parsed_issues(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.degradation is None
        assert [i["number"] for i in res.issues] == [42, 43]
        assert res.issues[0]["title"] == "First open issue"
        assert res.total == 2  # total_count from the payload

    async def test_total_reflects_search_total_count_not_page(self, sm):
        # search_issues returns a PAGE of items but a far larger total_count — the count
        # must be total_count (179), not len(page) (2). Regression guard for the 30-vs-179 bug.
        paged = json.dumps(
            {
                "total_count": 179,
                "items": [
                    {"number": 1, "title": "a", "labels": []},
                    {"number": 2, "title": "b", "labels": []},
                ],
            }
        )
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, payload=paged)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.total == 179  # the TRUE count
        assert len(res.issues) == 2  # ...but only a page of items

    async def test_bound_respects_limit(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter)
        res = await adapter.list_open_issues(_ALPHA, limit=1)
        assert len(res.issues) == 1

    async def test_bound_empty_payload_is_empty_list_not_degrade(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, payload=_EMPTY)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.degradation is None
        assert res.issues == []
        assert res.total == 0


class TestListOpenPRs:
    """#1322 P3 — list_open_prs shares the rail but targets search_pull_requests."""

    async def test_bound_returns_parsed_prs_via_pr_tool(self, sm):
        # Fixture exposes ONLY search_pull_requests → proves list_open_prs uses the PR tool
        # (if it called search_issues it would miss and return []).
        pr_payload = json.dumps(
            {
                "total_count": 2,
                "items": [
                    {"number": 5, "title": "My PR", "html_url": "http://x/5", "labels": []},
                    {"number": 6, "title": "Another PR", "html_url": "http://x/6", "labels": []},
                ],
            }
        )
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, payload=pr_payload, tool=gh_mod._PRS_TOOL)
        res = await adapter.list_open_prs(_ALPHA)
        assert res.degradation is None
        assert [i["number"] for i in res.issues] == [5, 6]
        assert res.total == 2

    async def test_no_binding_degrades_connect_required(self, sm):
        res = await GitHubMCPSpatialAdapter().list_open_prs(_ALPHA)
        assert res.issues is None
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED
