"""#1966 / ADR-081 D1: one read of an account's own GitHub PAT.

``GitHubMCPSpatialAdapter.account_pat`` reads both PAT legs in the resolver's order
(the at-rest row, then the user-scoped keychain), and ``resolve_credential`` uses it. So
every surface that needs the raw token (the router's REST session, the issue-summary
fetch, Settings' validity check, repo validation, the status line) finds exactly the
token the resolver finds. Before, those read the keychain only and missed a PAT saved
only at rest.

LAYER: unit (the legs stubbed) plus a source scan.
DENOMINATOR: account_pat's five outcomes; the router's per-user init; the Settings card
on a failed read; every module under services/ and web/.
"""

import ast
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter as _A

ROOT = Path(__file__).resolve().parents[4]
_USER = "5a2c9d10-1966-4b00-9e00-00000000cccc"


def _failed(*a, **k):
    raise GitHubReadFailed("the stored GitHub token couldn't be read", None, detail="store_failed")


def _legs(at_rest, keychain):
    def _mk(v, is_async):
        if v is _failed:
            return AsyncMock(side_effect=_failed) if is_async else MagicMock(side_effect=_failed)
        return AsyncMock(return_value=v) if is_async else MagicMock(return_value=v)

    return (
        patch.object(_A, "_user_pat_at_rest", _mk(at_rest, True)),
        patch.object(_A, "_user_pat", _mk(keychain, False)),
    )


@pytest.mark.asyncio
class TestAccountPat:
    @pytest.mark.parametrize(
        "at_rest, keychain, expected",
        [
            ("fake-token-row", None, "fake-token-row"),
            (None, "fake-token-kc", "fake-token-kc"),
            (_failed, "fake-token-kc", "fake-token-kc"),  # either leg's token serves
            (None, None, None),  # both legs ran and found nothing
        ],
    )
    async def test_either_leg_serves_and_absence_is_none(self, at_rest, keychain, expected):
        a, k = _legs(at_rest, keychain)
        with a, k:
            assert await _A.account_pat(_USER) == expected

    @pytest.mark.parametrize("at_rest, keychain", [(_failed, None), (None, _failed)])
    async def test_a_failed_leg_with_no_token_raises(self, at_rest, keychain):
        a, k = _legs(at_rest, keychain)
        with a, k, pytest.raises(GitHubReadFailed):
            await _A.account_pat(_USER)

    async def test_the_router_configures_rest_with_the_accounts_pat(self):
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        router = GitHubIntegrationRouter()
        router.mcp_adapter = MagicMock()
        router.mcp_adapter.configure_github_api = AsyncMock()
        router.spatial_github = None
        with patch.object(_A, "account_pat", AsyncMock(return_value="fake-token-row")) as pat:
            await router.initialize(user_id=_USER)
        pat.assert_awaited_once_with(_USER)
        router.mcp_adapter.configure_github_api.assert_awaited_once_with("fake-token-row")


def _calls(tree, names):
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            name = getattr(n.func, "attr", getattr(n.func, "id", None))
            if name in names:
                yield n


def test_only_the_adapter_reads_the_pat_legs():
    offenders = []
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "services/mcp/consumer/github_adapter.py":
                continue
            tree = ast.parse(path.read_text())
            for n in _calls(tree, {"_user_pat", "_user_pat_at_rest"}):
                offenders.append(f"{rel}:{n.lineno}")
    assert not offenders, "PAT legs read outside account_pat (#1966): " + "; ".join(offenders)


def test_the_keychain_leg_is_read_only_in_user_pat():
    """Arch 10-25: read_user_token (the keychain leg alone) is referenced only by
    _user_pat; _list_repos_native_pat read it directly and missed a PAT saved at rest."""
    offenders = []
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "services/integrations/github/config_service.py":
                continue
            tree = ast.parse(path.read_text())
            for fn in ast.walk(tree):
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if rel == "services/mcp/consumer/github_adapter.py" and fn.name == "_user_pat":
                    continue
                for n in ast.walk(fn):
                    if isinstance(n, ast.Attribute) and n.attr == "read_user_token":
                        offenders.append(f"{rel}:{n.lineno}")
    assert not offenders, "keychain-only PAT read (#1966): " + "; ".join(sorted(set(offenders)))


def test_no_user_scoped_token_read_outside_the_config_service():
    """get_authentication_token / aget_authentication_token take only the literal "system"
    outside the config service; a user's token comes from account_pat."""
    offenders = []
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "services/integrations/github/config_service.py":
                continue
            tree = ast.parse(path.read_text())
            for n in _calls(tree, {"get_authentication_token", "aget_authentication_token"}):
                args = list(n.args) + [k.value for k in n.keywords]
                if not (
                    len(args) == 1
                    and isinstance(args[0], ast.Constant)
                    and args[0].value == "system"
                ):
                    offenders.append(f"{rel}:{n.lineno}")
    assert not offenders, "user-scoped GitHub token read (#1966): " + "; ".join(offenders)


@pytest.mark.asyncio
class TestSettingsCardReadsTheAccountPat:
    async def _card(self, pat):
        from web.api.routes import settings_integrations as si

        with (
            patch(
                "services.integrations.integration_status_service.IntegrationStatusService"
                ".get_status",
                new=AsyncMock(return_value={"configured": True, "check_failed": False}),
            ),
            patch.object(_A, "account_pat", pat),
            patch(
                "services.integrations.github.token_validator.verify_github_token",
                new=AsyncMock(return_value={"authenticated": True, "username": "me"}),
            ) as verify,
        ):
            return await si.get_github_settings(current_user=MagicMock(sub=_USER)), verify

    async def test_a_pat_saved_only_at_rest_is_validated(self):
        out, verify = await self._card(AsyncMock(return_value="fake-token-row"))
        verify.assert_awaited_once_with("fake-token-row")
        assert out["valid"] is True and out["username"] == "me"

    async def test_a_failed_read_is_couldnt_check_never_valid(self):
        from web.api.routes.settings_integrations import _github_check_failed

        out, verify = await self._card(AsyncMock(side_effect=_failed))
        verify.assert_not_awaited()
        assert out == _github_check_failed()


class _Resp:
    status = 200

    async def json(self):
        return [{"id": 1, "name": "r", "full_name": "me/r"}]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _Session:
    def __init__(self):
        self.headers = None

    def get(self, url, headers=None, params=None):
        self.headers = headers
        return _Resp()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


@pytest.mark.asyncio
class TestRepoListReadsTheAccountPat:
    """Arch 10-25: the PAT-only repo list read the keychain alone, so a PAT saved only at
    rest got 401 "GitHub not connected" while the resolver said connected."""

    async def _list(self, pat):
        from web.api.routes import settings_integrations as si

        session = _Session()
        with (
            patch.object(_A, "account_pat", pat),
            patch("aiohttp.ClientSession", return_value=session),
        ):
            return await si._list_repos_native_pat(_USER), session

    async def test_a_pat_saved_only_at_rest_lists_repos(self):
        pat = AsyncMock(return_value="fake-token-row")
        repos, session = await self._list(pat)
        pat.assert_awaited_once_with(_USER)
        assert session.headers["Authorization"] == "Bearer fake-token-row"
        assert repos[0]["full_name"] == "me/r"

    async def test_no_pat_is_not_connected(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc:
            await self._list(AsyncMock(return_value=None))
        assert exc.value.status_code == 401

    async def test_a_failed_read_is_couldnt_read_not_not_connected(self):
        from web.api.routes.settings_integrations import GITHUB_TOKEN_READ_FAILED_MESSAGE

        with pytest.raises(Exception) as exc:
            await self._list(AsyncMock(side_effect=_failed))
        assert exc.value.status_code == 503
        assert exc.value.detail == GITHUB_TOKEN_READ_FAILED_MESSAGE
