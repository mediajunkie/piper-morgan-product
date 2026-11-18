"""#2012 — the Integration Health "Test" for GitHub is ONE probe through the resolver.

A BOUND binding row survives a revoked or expired grant, so "bound → success" told the user
GitHub worked while every read failed (xian, alpha, 2026-10-14). Now ``_test_github`` lets
``resolve_credential`` pick the leg exactly as the reads do, makes one real authenticated
read (``search_user_repositories``, limit 1), names the serving leg (CXO's lines) and maps a
degrade to an ``error_type`` the registry's guidance knows. A missing user is not-configured,
never a global-key fallback (Arch, Amendment B).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult
from web.api.routes import integrations

pytestmark = pytest.mark.asyncio

_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"


def _degraded(reason: DegradationReason, message: str) -> DegradationResponse:
    return DegradationResponse(reason=reason, user_message=message, action_hint=None)


def _oauth_credential(stale=None) -> GitHubCredential:
    return GitHubCredential(
        owner_id="u1", mcp_server_ref="github", token=None, leg="oauth", stale_oauth_reason=stale
    )


def _pat_credential(stale=None) -> GitHubCredential:
    return GitHubCredential(
        owner_id="u1", mcp_server_ref="github", token="ghp_x", leg="pat", stale_oauth_reason=stale
    )


def _patched(credential, probe_result):
    resolve = AsyncMock(return_value=credential)
    probe = AsyncMock(return_value=probe_result)
    ctx = (
        patch(f"{_ADAPTER}.resolve_credential", new=resolve),
        patch(f"{_ADAPTER}.search_user_repositories", new=probe),
    )
    return ctx, resolve, probe


async def test_revoked_grant_fails_the_test_with_a_reconnect_fix():
    ctx, resolve, probe = _patched(
        _oauth_credential(),
        GitHubReposResult(degradation=_degraded(DegradationReason.STALE_TOKEN, "re-auth")),
    )
    with ctx[0], ctx[1]:
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is False
    assert result["error_type"] == "stale_token"
    resolve.assert_awaited_once_with("u1")
    probe.assert_awaited_once()
    message, fix = integrations._get_error_guidance("github", result["error_type"])
    assert message == "GitHub no longer accepts your connection."  # CXO 2026-11-18
    assert "Reconnect with GitHub" in fix  # #2029: one step, no Disconnect first


async def test_live_oauth_grant_passes_and_names_the_connection():
    ctx, _resolve, probe = _patched(
        _oauth_credential(), GitHubReposResult(repositories=[{"full_name": "o/r"}])
    )
    with ctx[0], ctx[1]:
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is True
    assert result["message"] == "GitHub is working, using your GitHub connection."
    assert result["leg"] == "oauth"
    assert result["stale_oauth_reason"] is None
    probe.assert_awaited_once()


async def test_pat_only_user_passes_on_their_own_token():
    # Arch's condition: a PAT-only user (no binding) must not read "not connected" from Test
    # while the reads work on their token. The resolver serves the PAT leg; Test reports it.
    ctx, _resolve, _probe = _patched(
        _pat_credential(), GitHubReposResult(repositories=[{"full_name": "o/r"}])
    )
    with ctx[0], ctx[1]:
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is True
    assert result["message"] == "GitHub is working, using your personal token."
    assert result["leg"] == "pat"


async def test_stale_oauth_with_working_pat_says_so():
    # B3: never a plain green when only the fallback leg works.
    ctx, _resolve, _probe = _patched(
        _pat_credential(stale=DegradationReason.STALE_TOKEN),
        GitHubReposResult(repositories=[{"full_name": "o/r"}]),
    )
    with ctx[0], ctx[1]:
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is True
    assert result["message"] == (
        "GitHub is working, using your personal token. "
        "GitHub no longer accepts your connection, so I'm not using it right now."
    )
    assert result["stale_oauth_reason"] == "stale_token"


async def test_no_credential_at_all_is_connect_required_without_a_probe():
    resolve = AsyncMock(return_value=_degraded(DegradationReason.CONNECT_REQUIRED, "connect"))
    probe = AsyncMock()
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=resolve),
        patch(f"{_ADAPTER}.search_user_repositories", new=probe),
    ):
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is False
    assert result["error_type"] == "connect_required"
    probe.assert_not_awaited()


async def test_server_down_reads_unreachable_not_connected():
    ctx, _resolve, _probe = _patched(
        _oauth_credential(),
        GitHubReposResult(degradation=_degraded(DegradationReason.UNREACHABLE, "down")),
    )
    with ctx[0], ctx[1]:
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is False
    assert result["error_type"] == "unreachable"


async def test_missing_user_is_not_configured_and_never_resolves_a_global_key():
    resolve = AsyncMock()
    with patch(f"{_ADAPTER}.resolve_credential", new=resolve):
        result = await integrations._test_github(user_id=None)
    assert result["success"] is False
    assert result["error_type"] == "not_configured"
    resolve.assert_not_awaited()
