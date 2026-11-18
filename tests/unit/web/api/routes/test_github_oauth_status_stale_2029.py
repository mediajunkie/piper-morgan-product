"""#2029 — Settings → GitHub agrees with the reads and the Test on a revoked grant.

Pins, at the route layer:
- the #2012 Test probe's own 401 marks the binding STALE (so the page agrees right after
  a Test), and its guidance now says Reconnect in one step;
- ``GET /api/v1/settings/integrations/github/oauth-status`` reports ``connected`` /
  ``stale`` / ``serving`` for BOUND, STALE with a working personal token, STALE with a
  rejected personal token, STALE with none, and no binding.

The binding table is a real in-memory SQLite ``connector_bindings`` behind a committing
``session_scope``; the 401 is a real FastMCP tool error (how github-mcp-server reports it).
"""

from __future__ import annotations

import contextlib
from unittest.mock import AsyncMock, MagicMock, patch

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
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    ConnectorStatusState,
    DegradationReason,
    DegradationResponse,
)
from services.mcp.consumer.github_adapter import (  # noqa: E402
    GitHubCredential,
    GitHubMCPSpatialAdapter,
    GitHubReposResult,
)
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402
from web.api.routes import integrations  # noqa: E402
from web.api.routes.settings_integrations import github_oauth_status  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
_401 = "failed to search repositories: GET https://api.github.com/search/repositories: 401 Bad credentials []"


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
            await s.commit()

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", staticmethod(_scope))
    assert gh_mod.AsyncSessionFactory is AsyncSessionFactory
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


def _claims():
    c = MagicMock()
    c.sub = _ALPHA
    return c


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


def _repos_tool_401_ctx():
    server = FastMCP("github-repos-401-fixture")

    @server.tool(name=gh_mod._REPOS_TOOL)
    def _search(query: str = "", perPage: int = 30) -> str:
        raise RuntimeError(_401)

    @contextlib.asynccontextmanager
    async def _ctx(self, binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    return _ctx


class TestTheTestProbeMarksStale:
    async def test_test_button_401_marks_the_binding_stale_and_says_reconnect(self, maker):
        await _seed(maker, ConnectorStatusState.BOUND.value)
        with (
            patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=_oauth())),
            patch.object(GitHubMCPSpatialAdapter, "_mcp_client_ctx", _repos_tool_401_ctx()),
        ):
            result = await integrations._test_github(user_id=_ALPHA)
        # The #2012 reply as landed...
        assert result["success"] is False
        assert result["error_type"] == "stale_token"
        assert result["error"] == "GitHub no longer accepts your connection."
        # ...and the page now agrees: the row is STALE.
        assert await _status(maker) == ConnectorStatusState.STALE.value
        message, fix = integrations._get_error_guidance("github", "stale_token")
        assert message == "GitHub no longer accepts your connection."
        assert fix == "In Settings → Integrations → GitHub, Reconnect with GitHub"
        assert "Disconnect" not in fix


def _core(out):
    """The four fields #2029 pins. #2376 added ``app_connected`` and ``pat_on_file``,
    pinned in test_settings_github_token_form_2376.py."""
    assert set(out) == {"connected", "stale", "serving", "status", "app_connected", "pat_on_file"}
    return {k: out[k] for k in ("connected", "stale", "serving", "status")}


class TestOAuthStatusStates:
    async def test_bound_is_connected_on_oauth_with_no_github_call(self, maker):
        await _seed(maker, ConnectorStatusState.BOUND.value)
        resolve = AsyncMock()
        with patch(f"{_ADAPTER}.resolve_credential", new=resolve):
            out = await github_oauth_status(current_user=_claims())
        assert _core(out) == {
            "connected": True,
            "stale": False,
            "serving": "oauth",
            "status": "bound",
        }
        resolve.assert_not_awaited()

    async def test_stale_with_a_working_personal_token_serves_pat(self, maker):
        await _seed(maker, ConnectorStatusState.STALE.value)
        probe = AsyncMock(return_value=GitHubReposResult(repositories=[{"full_name": "o/r"}]))
        with (
            patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=_pat())),
            patch(f"{_ADAPTER}.search_user_repositories", new=probe),
        ):
            out = await github_oauth_status(current_user=_claims())
        assert _core(out) == {
            "connected": False,
            "stale": True,
            "serving": "pat",
            "status": "stale",
        }
        probe.assert_awaited_once_with(_ALPHA, limit=1)

    async def test_stale_with_a_rejected_personal_token_serves_nothing(self, maker):
        # "Connected via your personal token" only on evidence the token answers.
        await _seed(maker, ConnectorStatusState.STALE.value)
        failed = GitHubReposResult(
            degradation=DegradationResponse(
                reason=DegradationReason.STALE_TOKEN, user_message="re-auth"
            )
        )
        with (
            patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=_pat())),
            patch(f"{_ADAPTER}.search_user_repositories", new=AsyncMock(return_value=failed)),
        ):
            out = await github_oauth_status(current_user=_claims())
        assert _core(out) == {"connected": False, "stale": True, "serving": None, "status": "stale"}

    async def test_stale_without_a_personal_token_serves_nothing_and_never_probes(self, maker):
        await _seed(maker, ConnectorStatusState.STALE.value)
        degraded = DegradationResponse(reason=DegradationReason.STALE_TOKEN, user_message="x")
        probe = AsyncMock()
        with (
            patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=degraded)),
            patch(f"{_ADAPTER}.search_user_repositories", new=probe),
        ):
            out = await github_oauth_status(current_user=_claims())
        assert _core(out) == {"connected": False, "stale": True, "serving": None, "status": "stale"}
        probe.assert_not_awaited()

    async def test_no_binding_is_neither(self, maker):
        out = await github_oauth_status(current_user=_claims())
        assert _core(out) == {"connected": False, "stale": False, "serving": None, "status": None}

    async def test_a_read_401_then_status_then_regrant_round_trip(self, maker):
        # The whole story on one row: BOUND → a read's 401 → page says stale →
        # the OAuth callback's persist → page says connected again.
        from services.mcp.consumer.github_oauth_handler import persist_github_connection

        await _seed(maker, ConnectorStatusState.BOUND.value)
        adapter = GitHubMCPSpatialAdapter()
        with (
            patch.object(adapter, "resolve_credential", AsyncMock(return_value=_oauth())),
            patch.object(GitHubMCPSpatialAdapter, "_mcp_client_ctx", _repos_tool_401_ctx()),
        ):
            await adapter.search_user_repositories(_ALPHA, limit=1)
        none = DegradationResponse(reason=DegradationReason.STALE_TOKEN, user_message="x")
        with patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=none)):
            mid = await github_oauth_status(current_user=_claims())
        assert (mid["connected"], mid["stale"]) == (False, True)

        async with maker() as s:
            await persist_github_connection(s, _ALPHA, "gho_new", grant_store=AsyncMock())
            await s.commit()
        after = await github_oauth_status(current_user=_claims())
        assert (after["connected"], after["stale"], after["serving"]) == (True, False, "oauth")
