"""#2266 (Arch 2026-11-04 12:46, "either way"): the Settings GitHub endpoints answer for
the SIGNED-IN account only. An account with nothing stored (no binding, no token) reads
not connected, gets no repository list, and starts a connect bound to its own id, even
when the deployment carries an env token and an env handle. The leak report of 11-04 was
GitHub's own consent screen; these pins keep Piper's side provably per-account.
"""

from __future__ import annotations

import contextlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.database.models import ConnectorBinding
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter
from web.api.routes import settings_integrations as si

pytestmark = pytest.mark.asyncio

ACCOUNT_B = "bbbbbbbb-2266-4b00-9e00-00000000000b"


def _claims(sub: str = ACCOUNT_B):
    c = MagicMock()
    c.sub = sub
    c.user_email = "b@example.invalid"
    return c


@pytest_asyncio.fixture
async def empty_db(monkeypatch):
    """A binding table with NO rows for account B, and no token on either PAT leg; the
    deployment env carries an operator token and handle that must never be read."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    monkeypatch.setattr(
        "services.database.session_factory.AsyncSessionFactory.session_scope",
        staticmethod(_scope),
    )
    monkeypatch.setattr(
        GitHubMCPSpatialAdapter, "account_pat", staticmethod(AsyncMock(return_value=None))
    )
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_operator_token_never_read")
    monkeypatch.setenv("PIPER_GITHUB_HANDLE", "mediajunkie")
    # alpha's branch: on a hosted deployment the system env token is the host's account,
    # never the caller's (#2151); a local install may still read it, by design.
    monkeypatch.setenv("FLY_APP_NAME", "piper-morgan")
    yield maker
    await engine.dispose()


class TestAnAccountWithNothingStored:
    async def test_oauth_status_reads_not_connected(self, empty_db):
        res = await si.github_oauth_status(current_user=_claims())
        assert res == {"connected": False, "stale": False, "serving": None, "status": None}

    async def test_repositories_are_refused_not_listed(self, empty_db):
        with pytest.raises(HTTPException) as e:
            await si.get_github_repositories(current_user=_claims())
        assert e.value.status_code in (401, 502)
        assert "mediajunkie" not in str(e.value.detail)

    async def test_connect_binds_the_state_to_the_signed_in_account(self, empty_db):
        handler = MagicMock()
        handler.generate_authorization_url = MagicMock(
            return_value=("https://github.com/login/oauth/authorize?state=s", "s")
        )
        with patch(
            "services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler", return_value=handler
        ):
            res = await si.connect_github(current_user=_claims())
        handler.generate_authorization_url.assert_called_once_with(user_id=ACCOUNT_B)
        assert res["auth_url"].startswith("https://github.com/login/oauth/authorize")

    async def test_settings_status_carries_no_operator_identity(self, empty_db):
        with (
            patch(
                "services.integrations.integration_status_service.IntegrationStatusService.get_status",
                new=AsyncMock(return_value={"configured": False, "via": None}),
            ),
            patch(
                "services.integrations.github.token_validator.verify_github_token",
                new=AsyncMock(
                    side_effect=AssertionError(
                        "the operator's env token was validated for account B"
                    )
                ),
            ),
        ):
            res = await si.get_github_settings(current_user=_claims())
        assert res == {"configured": False, "valid": False, "username": None, "error": None}
