"""#1329: GitHub Integration-Health follows the OAuth connector binding, not the
legacy native PAT.

After the #1322 chat-reads cutover, an expired/dead native PAT must not make the
Integration Health page report GitHub as "unknown"/"failed" while the OAuth connector
is bound and serving the chat reads. These tests pin the precedence:
  - BOUND connector  -> "healthy" (regardless of native PAT state)
  - not bound        -> falls through to the legacy native config/health path
"""

from unittest.mock import AsyncMock, patch

import pytest

from web.api.routes import integrations

_META = {"display_name": "GitHub", "configure_url": "/settings/github"}


@pytest.mark.asyncio
async def test_github_health_healthy_when_oauth_bound():
    """A BOUND OAuth connector → GitHub reads healthy even with a dead native PAT."""
    with patch.object(integrations, "_github_oauth_bound", new=AsyncMock(return_value=True)):
        status = await integrations._check_integration_health("github", _META, user_id="u1")
    assert status.status == "healthy"
    assert "OAuth" in status.status_message


@pytest.mark.asyncio
async def test_github_health_falls_through_when_not_oauth_bound():
    """No OAuth binding → the legacy native config path still governs (here: not_configured)."""
    with patch.object(
        integrations, "_github_oauth_bound", new=AsyncMock(return_value=False)
    ), patch.object(
        integrations,
        "_get_integration_config_status",
        new=AsyncMock(return_value="not_configured"),
    ):
        status = await integrations._check_integration_health("github", _META, user_id="u1")
    assert status.status == "not_configured"


@pytest.mark.asyncio
async def test_non_github_integration_unaffected_by_oauth_shortcircuit():
    """The OAuth short-circuit is GitHub-only — other integrations keep native behavior."""
    bound = AsyncMock(return_value=True)
    with patch.object(integrations, "_github_oauth_bound", new=bound), patch.object(
        integrations,
        "_get_integration_config_status",
        new=AsyncMock(return_value="not_configured"),
    ):
        status = await integrations._check_integration_health(
            "slack", {"display_name": "Slack"}, user_id="u1"
        )
    assert status.status == "not_configured"
    bound.assert_not_called()
