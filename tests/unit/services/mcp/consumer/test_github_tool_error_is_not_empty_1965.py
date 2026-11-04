"""#1965 (OAuth leg) — a github-mcp-server tool ERROR must never read as an empty list.

A revoked or expired OAuth grant makes GitHub answer 401; github-mcp-server returns a
tool result with ``isError: true`` whose content is the error text. The MCP SDK hands
that result back without raising, and until this pin the adapter fed the text to its
tolerant JSON parsers, which returned ``[]``: the Radar/standup work-items read came back
VERIFIED_EMPTY with ``degraded_sources: []`` (the issue's own title). Now ``_tool_text``
raises ``GitHubToolError`` and the call site's degrade rail carries the reason the text
names: 401 → STALE_TOKEN ("re-authorize"), 404 → RESOURCE_NOT_FOUND, else UNREACHABLE.
The FastMCP fixture raises inside the tool, which is exactly how an MCP server produces
``isError`` (a real round-trip, not a mocked result object).
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
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubMCPSpatialAdapter,
    GitHubToolError,
    _reason_for_tool_error,
)
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_401 = "failed to search issues: GET https://api.github.com/search/issues: 401 Bad credentials []"
_404 = "failed to get issue: GET https://api.github.com/repos/o/r/issues/9: 404 Not Found []"
_500 = "failed to search issues: GET https://api.github.com/search/issues: 502 Bad Gateway []"


async def _fake_grant(owner_id):
    return "gho_test_grant_2266"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    # #2266: the resolver reads the OAuth grant strictly; this fixture stores none, so
    # the seam answers with a fake bearer (the connect itself is faked below).
    monkeypatch.setattr(gh_mod.GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(_fake_grant))
    yield maker
    await engine.dispose()


async def _seed_bound(maker):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status="bound", mcp_server_ref="http://srv/mcp"
        )
        await s.commit()


def _point_at_erroring_fixture(adapter, *, error_text, tool=None):
    """A FastMCP server whose search tool RAISES: the SDK turns that into a result with
    ``isError=True`` and the message as text content, as github-mcp-server does on a 401."""
    server = FastMCP("github-search-error-fixture")

    @server.tool(name=tool or gh_mod._ISSUES_TOOL)
    def search(query: str, perPage: int = 30) -> str:
        raise RuntimeError(error_text)

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestToolErrorReason:
    def test_401_is_stale_token(self):
        assert _reason_for_tool_error(_401) is DegradationReason.STALE_TOKEN

    def test_404_is_resource_not_found(self):
        assert _reason_for_tool_error(_404) is DegradationReason.RESOURCE_NOT_FOUND

    def test_other_is_unreachable(self):
        assert _reason_for_tool_error(_500) is DegradationReason.UNREACHABLE
        assert _reason_for_tool_error("") is DegradationReason.UNREACHABLE

    def test_tool_text_raises_on_is_error_and_passes_through_otherwise(self):
        class _Text:
            def __init__(self, text):
                self.text = text

        class _Result:
            def __init__(self, text, is_error):
                self.content = [_Text(text)]
                self.isError = is_error

        with pytest.raises(GitHubToolError) as info:
            GitHubMCPSpatialAdapter._tool_text(_Result(_401, True))
        assert info.value.reason is DegradationReason.STALE_TOKEN
        payload = json.dumps({"total_count": 0, "items": []})
        assert GitHubMCPSpatialAdapter._tool_text(_Result(payload, False)) == payload


class TestRevokedGrantIsNotVerifiedEmpty:
    async def test_401_tool_error_degrades_stale_token(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _point_at_erroring_fixture(adapter, error_text=_401)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.issues is None, "an error payload must never parse as an empty list"
        assert res.degradation is not None
        assert res.degradation.reason is DegradationReason.STALE_TOKEN

    async def test_server_error_tool_error_degrades_unreachable(self, sm):
        await _seed_bound(sm)
        adapter = GitHubMCPSpatialAdapter()
        _point_at_erroring_fixture(adapter, error_text=_500)
        res = await adapter.list_open_issues(_ALPHA)
        assert res.issues is None
        assert res.degradation.reason is DegradationReason.UNREACHABLE
