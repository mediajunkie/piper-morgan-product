"""#1329: GitHub Integration-Health follows the OAuth connector, not the legacy native PAT.

After the #1322 chat-reads cutover, an expired/dead native PAT must not make the
Integration Health page report GitHub as "unknown"/"failed" while the OAuth connector
is serving the chat reads.

#2031 (ADR-070 B4): the card now derives from the one credential resolver
(``resolve_credential``), not from the binding row's BOUND status, so these pins stub
the resolver. The four card states are pinned in
``test_integrations_card_resolver_2031.py``.
  - OAuth leg serving -> "healthy" (regardless of native PAT state)
  - nothing serving, no stale grant -> "not_configured"
"""

from unittest.mock import AsyncMock, patch

import pytest

from web.api.routes import integrations

_META = {"display_name": "GitHub", "configure_url": "/settings/github"}
_RESOLVE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential"


@pytest.mark.asyncio
async def test_github_health_healthy_when_oauth_leg_serves():
    """The resolver's OAuth leg → GitHub reads healthy even with a dead native PAT."""
    from services.mcp.consumer.github_adapter import GitHubCredential

    credential = GitHubCredential(owner_id="u1", mcp_server_ref="github", token=None, leg="oauth")
    with patch(_RESOLVE, new=AsyncMock(return_value=credential)):
        status = await integrations._check_integration_health("github", _META, user_id="u1")
    assert (
        status.status == "connected"
    )  # #2075: a bound grant with no recorded check claims no health
    assert (
        status.status_message
        == "Connected as octocat. Not the right account? Disconnect, then connect again."
    )


@pytest.mark.asyncio
async def test_github_health_not_configured_when_nothing_serves():
    """No binding and no token (CONNECT_REQUIRED) → not_configured, from the resolver."""
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse

    degraded = DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub to continue."
    )
    with patch(_RESOLVE, new=AsyncMock(return_value=degraded)):
        status = await integrations._check_integration_health("github", _META, user_id="u1")
    assert status.status == "not_configured"


@pytest.mark.asyncio
async def test_non_github_integration_does_not_consult_the_github_resolver():
    """The resolver path is GitHub-only — other integrations keep native behavior."""
    resolve = AsyncMock()
    with (
        patch(_RESOLVE, new=resolve),
        patch.object(
            integrations,
            "_get_integration_config_status",
            new=AsyncMock(return_value="not_configured"),
        ),
    ):
        status = await integrations._check_integration_health(
            "slack", {"display_name": "Slack"}, user_id="u1"
        )
    assert status.status == "not_configured"
    resolve.assert_not_called()


@pytest.mark.asyncio
async def test_github_test_button_succeeds_when_oauth_bound():
    """The Integration-Health 'Test' button reports success via the connector when BOUND,
    without probing the (possibly dead) native PAT — keeps it consistent with the health row."""
    # #2012: the Test no longer selects a leg by row presence; the resolver picks it and one
    # real read follows. A live OAuth credential whose probe answers is the pass case.
    from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult

    credential = GitHubCredential(owner_id="u1", mcp_server_ref="github", token=None, leg="oauth")
    probe = AsyncMock(return_value=GitHubReposResult(repositories=[{"full_name": "o/r"}]))
    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            new=AsyncMock(return_value=credential),
        ),
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.search_user_repositories",
            new=probe,
        ),
    ):
        result = await integrations._test_github(user_id="u1")
    assert result["success"] is True
    assert "GitHub connection" in result.get("message", "")
    probe.assert_awaited_once()


@pytest.fixture(autouse=True)
def _login_octocat_2279(monkeypatch):
    """#2279: the OAuth card now reads the account's login through its own grant."""
    from unittest.mock import AsyncMock as _AM

    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter as _A

    monkeypatch.setattr(_A, "account_login", _AM(return_value="octocat"))
