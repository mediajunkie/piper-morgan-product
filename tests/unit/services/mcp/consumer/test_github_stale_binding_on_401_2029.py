"""#2029 — GitHub's 401 on the OAuth leg marks the binding STALE; a re-grant restores BOUND.

Before this, nothing on main wrote STALE to a binding, so a revoked grant stayed BOUND
forever: the reads (#1965) and the Test (#2012) said "reconnect" while Settings → GitHub
(``oauth-status``, BOUND-only) still said Connected and hid the Connect button. Now the
adapter's one degrade rail (``_degrade_for_exc``) writes STALE when the leaf is GitHub's
401 on the OAuth leg, so every status surface reads the same stored state.

Real round-trips: a FastMCP fixture whose tool raises (how github-mcp-server produces
``isError`` on a 401), and an in-memory SQLite ``connector_bindings`` table behind a
committing ``session_scope`` (the production contract, #1193).
"""

from __future__ import annotations

import contextlib
from unittest.mock import AsyncMock, patch

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
from services.mcp.consumer.connector import (  # noqa: E402
    ConnectorStatusState,
    DegradationReason,
)
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubCredential,
    GitHubMCPSpatialAdapter,
)
from services.mcp.consumer.github_oauth_handler import persist_github_connection  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_401 = "failed to search repositories: GET https://api.github.com/search/repositories: 401 Bad credentials []"
_502 = "failed to search repositories: GET https://api.github.com/search/repositories: 502 Bad Gateway []"


async def _fake_grant(owner_id):
    return "gho_test_grant_2266"


@pytest_asyncio.fixture
async def maker(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with sm() as s:
            yield s
            await s.commit()  # the #1193 contract: commit on clean exit

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    # #2266: the resolver reads the OAuth grant strictly; this fixture stores none, so
    # the seam answers with a fake bearer (the connect itself is faked below).
    monkeypatch.setattr(gh_mod.GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(_fake_grant))
    yield sm
    await engine.dispose()


async def _seed(sm, status: str) -> None:
    async with sm() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref="github"
        )
        await s.commit()


async def _status(sm):
    async with sm() as s:
        row = await ConnectorBindingRepository(s).get(_ALPHA, "github")
    return None if row is None else row.status


def _oauth():
    return GitHubCredential(owner_id=_ALPHA, mcp_server_ref="github", token=None, leg="oauth")


def _pat():
    return GitHubCredential(
        owner_id=_ALPHA,
        mcp_server_ref="github",
        token="ghp_x",
        leg="pat",
        stale_oauth_reason=DegradationReason.STALE_TOKEN,
    )


def _erroring(adapter, error_text: str, *tools: str) -> None:
    """Every named tool RAISES: the SDK returns ``isError`` with the text, as
    github-mcp-server does when GitHub answers 401."""
    server = FastMCP("github-401-fixture")
    for name in tools:

        def _make(n):
            @server.tool(name=n)
            def _tool(query: str = "", perPage: int = 30, owner: str = "", repo: str = "") -> str:
                raise RuntimeError(error_text)

        _make(name)

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestOAuthLeg401MarksStale:
    async def test_repo_search_401_on_oauth_leg_writes_stale(self, maker):
        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        _erroring(adapter, _401, gh_mod._REPOS_TOOL)
        with patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())):
            result = await adapter.search_user_repositories(_ALPHA, limit=1)
        assert result.degradation is not None
        assert result.degradation.reason is DegradationReason.STALE_TOKEN
        assert await _status(maker) == ConnectorStatusState.STALE.value

    async def test_issue_search_401_on_oauth_leg_writes_stale(self, maker):
        # The Radar/standup/chat read (#1965's path) flips the row too, not only Settings.
        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        _erroring(adapter, _401, gh_mod._ISSUES_TOOL)
        with patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())):
            result = await adapter.list_open_issues(_ALPHA)
        assert result.degradation.reason is DegradationReason.STALE_TOKEN
        assert await _status(maker) == ConnectorStatusState.STALE.value

    async def test_issue_probe_401_on_oauth_leg_writes_stale(self, maker):
        # probe_issue_connector (#1959) returns "unknown" rather than a degrade; it marks too.
        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        server = FastMCP("github-issue-401-fixture")

        @server.tool(name=gh_mod._ISSUE_READ_TOOL)
        def _issue_read(owner: str, repo: str, issue_number: int, method: str) -> str:
            raise RuntimeError(_401)

        @contextlib.asynccontextmanager
        async def _ctx(binding):
            async with create_connected_server_and_client_session(server) as session:
                yield MCPClient(session)

        adapter._mcp_client_ctx = _ctx

        class _Repo:
            owner, name, full_name = "o", "r", "o/r"

        with (
            patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())),
            patch.object(adapter, "_resolve_or_degrade", AsyncMock(return_value=_Repo())),
        ):
            state, item, _repo = await adapter.probe_issue_connector(_ALPHA, issue_number=9)
        assert (state, item) == ("unknown", None)
        assert await _status(maker) == ConnectorStatusState.STALE.value

    async def test_a_rejected_personal_token_never_marks_the_grant_stale(self, maker):
        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        _erroring(adapter, _401, gh_mod._REPOS_TOOL)
        with patch.object(adapter, "resolve_credential", AsyncMock(return_value=_pat())):
            result = await adapter.search_user_repositories(_ALPHA, limit=1)
        assert result.degradation.reason is DegradationReason.STALE_TOKEN
        assert await _status(maker) == ConnectorStatusState.BOUND.value

    async def test_an_outage_is_not_a_revoked_grant(self, maker):
        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        _erroring(adapter, _502, gh_mod._REPOS_TOOL)
        with patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())):
            result = await adapter.search_user_repositories(_ALPHA, limit=1)
        assert result.degradation.reason is DegradationReason.UNREACHABLE
        assert await _status(maker) == ConnectorStatusState.BOUND.value

    async def test_only_a_bound_row_is_flipped(self, maker):
        # A Disconnect that raced the read leaves the row UNBOUND; a 401 must not revive it.
        await _seed(maker, ConnectorStatusState.UNBOUND.value)
        flipped = await GitHubMCPSpatialAdapter._mark_oauth_binding_stale(_oauth())
        assert flipped is False
        assert await _status(maker) == ConnectorStatusState.UNBOUND.value

    async def test_no_row_is_a_no_op_and_creates_nothing(self, maker):
        flipped = await GitHubMCPSpatialAdapter._mark_oauth_binding_stale(_oauth())
        assert flipped is False
        assert await _status(maker) is None

    async def test_a_failed_write_still_returns_the_honest_degrade(self, maker, monkeypatch):
        await _seed(maker, ConnectorStatusState.BOUND.value)

        @contextlib.asynccontextmanager
        async def _broken():
            raise RuntimeError("db down")
            yield  # pragma: no cover

        adapter = GitHubMCPSpatialAdapter()
        _erroring(adapter, _401, gh_mod._REPOS_TOOL)
        with patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())):
            monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_broken))
            result = await adapter.search_user_repositories(_ALPHA, limit=1)
        assert result.degradation.reason is DegradationReason.STALE_TOKEN


class TestReGrantRestoresBound:
    async def test_oauth_callback_persist_rebinds_the_same_stale_row(self, maker):
        # CXO's question: Reconnect is one step. The callback's persist upserts the
        # (owner, connector) row in place: STALE → BOUND, same row, no Disconnect first.
        await _seed(maker, ConnectorStatusState.STALE.value)
        async with maker() as s:
            before = (await ConnectorBindingRepository(s).get(_ALPHA, "github")).id
        grant = AsyncMock()
        async with maker() as s:
            await persist_github_connection(s, _ALPHA, "gho_new", grant_store=grant)
            await s.commit()
        async with maker() as s:
            row = await ConnectorBindingRepository(s).get(_ALPHA, "github")
        assert row.status == ConnectorStatusState.BOUND.value
        assert row.id == before
        assert row.mcp_server_ref == "github"
        # The grant is replaced under the OAuth provider key only (the PAT lives elsewhere).
        grant.store.assert_awaited_once()
        assert grant.store.call_args.args[1:] == (_ALPHA, "github", "gho_new")
