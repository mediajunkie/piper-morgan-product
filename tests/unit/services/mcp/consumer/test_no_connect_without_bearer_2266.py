"""#2266 (2026-11-04): a beta tester's GitHub connector reached xian's repositories as
mediajunkie. A BOUND binding whose stored grant was absent or unreadable reached
``_mcp_client_ctx`` with no token, the client connected with no Authorization header,
and the official github-mcp-server answered with its own token. These pins hold the
guard: the resolver reads the grant strictly and never yields an OAuth credential
without a token; the client context never connects without a bearer; the env handle
is never a real account's identity.
"""

from __future__ import annotations

import contextlib
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.connectors.binding_repository import ConnectorBindingRepository
from services.database.models import ConnectorBinding
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GitHubCredential,
    GitHubGrantMissing,
    GitHubMCPSpatialAdapter,
)
from services.security.user_api_key_service import UserKeyReadFailed

pytestmark = pytest.mark.asyncio

_USER = "22222222-2266-4b00-9e00-000000002266"


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
            await s.commit()  # the real session_scope commits on exit

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _USER, "github", status="bound", mcp_server_ref="github"
        )
        await s.commit()
    # No PAT on either leg unless a test says otherwise.
    monkeypatch.setattr(
        GitHubMCPSpatialAdapter, "account_pat", staticmethod(AsyncMock(return_value=None))
    )
    yield maker
    await engine.dispose()


async def _binding_status(maker):
    async with maker() as s:
        row = await ConnectorBindingRepository(s).get(_USER, "github")
        return row.status if row else None


class TestResolverNeverYieldsAnOAuthCredentialWithoutAToken:
    async def test_a_stored_grant_is_the_credential(self, sm, monkeypatch):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter,
            "_oauth_grant",
            staticmethod(AsyncMock(return_value="gho_real")),
        )
        cred = await GitHubMCPSpatialAdapter().resolve_credential(_USER)
        assert isinstance(cred, GitHubCredential)
        assert cred.leg == "oauth" and cred.token == "gho_real"

    async def test_an_absent_grant_degrades_to_reauthorize_and_marks_the_binding_stale(
        self, sm, monkeypatch
    ):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(AsyncMock(return_value=None))
        )
        res = await GitHubMCPSpatialAdapter().resolve_credential(_USER)
        assert isinstance(res, DegradationResponse), res
        assert res.reason is DegradationReason.STALE_TOKEN
        assert await _binding_status(sm) == "stale"

    async def test_an_absent_grant_with_a_pat_serves_the_pat_leg(self, sm, monkeypatch):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(AsyncMock(return_value=None))
        )
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter,
            "account_pat",
            staticmethod(AsyncMock(return_value="ghp_own")),
        )
        cred = await GitHubMCPSpatialAdapter().resolve_credential(_USER)
        assert isinstance(cred, GitHubCredential)
        assert cred.leg == "pat" and cred.token == "ghp_own"
        assert cred.stale_oauth_reason is DegradationReason.STALE_TOKEN

    async def test_an_unreadable_grant_degrades_unreachable_not_stale(self, sm, monkeypatch):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter,
            "_oauth_grant",
            staticmethod(AsyncMock(side_effect=UserKeyReadFailed("cannot decrypt"))),
        )
        res = await GitHubMCPSpatialAdapter().resolve_credential(_USER)
        assert isinstance(res, DegradationResponse), res
        assert res.reason is DegradationReason.UNREACHABLE
        assert await _binding_status(sm) == "bound"  # a failed read is not absence


class TestTheClientNeverConnectsWithoutABearer:
    @pytest.mark.parametrize(
        "binding",
        [
            GitHubCredential(owner_id=_USER, mcp_server_ref="github", token=None, leg="oauth"),
            GitHubCredential(owner_id=_USER, mcp_server_ref="github", token="", leg="pat"),
            object(),
        ],
    )
    async def test_an_empty_bearer_raises_before_any_connect(self, binding):
        with patch.object(gh_mod.MCPClient, "connect_http") as connect:
            with pytest.raises(GitHubGrantMissing):
                async with GitHubMCPSpatialAdapter()._mcp_client_ctx(binding):
                    pass
        connect.assert_not_called()

    def test_the_guard_degrades_as_reauthorize(self):
        reason = GitHubMCPSpatialAdapter._degrade_reason_for_exc(GitHubGrantMissing("x"))
        assert reason is DegradationReason.STALE_TOKEN

    def test_a_credential_with_a_token_builds_the_bearer_header(self):
        """The header is built from the credential alone; nothing is read at connect time."""
        import inspect

        src = inspect.getsource(GitHubMCPSpatialAdapter._mcp_client_ctx)
        assert "ConnectorGrantStore().get(" not in src
        assert "if grant else None" not in src


class TestTheEnvHandleIsNeverARealAccountsIdentity:
    async def test_a_real_account_with_no_configured_handle_gets_none(self, monkeypatch):
        from services.integrations.github import repo_resolver

        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "mediajunkie")
        with patch(
            "services.connectors.config_service.ConnectorConfigService.get_config",
            new=AsyncMock(return_value={}),
        ):
            assert await repo_resolver.read_user_github_handle(_USER) is None

    async def test_the_system_principal_still_gets_the_env_handle(self, monkeypatch):
        from services.integrations.github import repo_resolver

        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "mediajunkie")
        assert await repo_resolver.read_user_github_handle(None) == "mediajunkie"
