"""#1327 gap 3 — GitHub OAuth-connector repo listing (Settings repo-config dropdown cutover).

`GitHubMCPSpatialAdapter.search_user_repositories(user_id)` lists the user's OWN repos over
the per-user OAuth connector (binding + grant -> `search_repositories` with the user-wide
`user:@me` query), honest-degrade throughout (#1231 — never a silent empty). This is the
read primitive the Settings `GET /github/repositories` dropdown cuts over to, replacing the
native shared-PAT path (`api.github.com/user/repos`).

TDD vs a FastMCP `search_repositories` fixture (no live github-mcp-server needed); the live
round-trip was de-risked separately (18 real repos via `user:@me`, payload shape
`{total_count, incomplete_results, items[]}` — same shape as search_issues).
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

# A canned github-mcp-server search_repositories payload (the real LIVE shape:
# total_count + incomplete_results + items[], each item with the repo dict fields).
_PAYLOAD = json.dumps(
    {
        "total_count": 2,
        "incomplete_results": False,
        "items": [
            {
                "id": 123,
                "name": "piper-morgan-product",
                "full_name": "mediajunkie/piper-morgan-product",
                "description": "Piper Morgan AI Assistant",
                "private": False,
                "fork": False,
            },
            {
                "id": 456,
                "name": "other-project",
                "full_name": "mediajunkie/other-project",
                "description": None,  # null description -> "" (mirror native)
                "private": True,
                "fork": False,
            },
        ],
    }
)
_EMPTY = json.dumps({"total_count": 0, "incomplete_results": False, "items": []})


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


def _point_at_fixture(adapter, *, payload=_PAYLOAD, raises=False, capture=None):
    """Patch _mcp_client_ctx to yield a FastMCP-backed client exposing search_repositories.

    If ``capture`` (a dict) is given, the tool records the query it was called with so a test
    can assert the user-wide `user:@me` query was used.
    """
    server = FastMCP("github-repos-fixture")

    @server.tool(name=gh_mod._REPOS_TOOL)
    def search_repositories(query: str) -> str:
        if capture is not None:
            capture["query"] = query
        return payload

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        if raises:
            raise RuntimeError("server unreachable")
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestSearchUserRepositoriesDegradeRail:
    async def test_no_binding_degrades_connect_required(self, sm):
        res = await GitHubMCPSpatialAdapter().search_user_repositories(_ALPHA)
        assert res.repositories is None
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED
        assert res.degradation.action_hint  # connect link surfaced (never silent-empty)

    async def test_non_bound_binding_degrades(self, sm):
        await _seed(sm, "unreachable")
        res = await GitHubMCPSpatialAdapter().search_user_repositories(_ALPHA)
        assert res.repositories is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_bound_but_server_unreachable_degrades(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, raises=True)
        res = await adapter.search_user_repositories(_ALPHA)
        assert res.repositories is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE


class TestSearchUserRepositoriesHit:
    async def test_bound_returns_parsed_repos(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter)
        res = await adapter.search_user_repositories(_ALPHA)
        assert res.degradation is None
        assert [r["full_name"] for r in res.repositories] == [
            "mediajunkie/piper-morgan-product",
            "mediajunkie/other-project",
        ]
        first = res.repositories[0]
        assert first["id"] == 123
        assert first["name"] == "piper-morgan-product"
        assert first["description"] == "Piper Morgan AI Assistant"

    async def test_null_description_normalized_to_empty_string(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter)
        res = await adapter.search_user_repositories(_ALPHA)
        # second item had description: None -> "" (mirror the native dropdown behavior)
        assert res.repositories[1]["description"] == ""

    async def test_uses_user_at_me_query(self, sm):
        """The dropdown must list the USER's OWN repos -> the user-wide `user:@me` query."""
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        cap = {}
        _point_at_fixture(adapter, capture=cap)
        await adapter.search_user_repositories(_ALPHA)
        assert cap["query"] == gh_mod._MY_REPOS_QUERY
        assert "user:@me" in cap["query"]

    async def test_bound_respects_limit(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter)
        res = await adapter.search_user_repositories(_ALPHA, limit=1)
        assert len(res.repositories) == 1

    async def test_bound_empty_payload_is_empty_list_not_degrade(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, payload=_EMPTY)
        res = await adapter.search_user_repositories(_ALPHA)
        assert res.degradation is None
        assert res.repositories == []
