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
