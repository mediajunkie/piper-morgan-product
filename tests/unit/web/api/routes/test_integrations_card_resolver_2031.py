"""#2031: the Integrations page's GitHub card derives from the one credential resolver
(ADR-070 B4; Arch issuecomment-6203985153). CXO's words (memo 2026-10-15, #2031 card
words, and the #2029 token-serving title/subtitle), verbatim.

One fixture per resolver outcome → the card (status, title, subtitle, icon, which
buttons). The resolver and the one-read probe are stubbed; no DB, no GitHub, no LLM.
A stale binding never renders "Not configured".
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult
from web.api.routes import integrations

_META = integrations.INTEGRATION_REGISTRY["github"]
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"

OAUTH = GitHubCredential(owner_id="u1", mcp_server_ref="github", token=None, leg="oauth")
PAT_STALE = GitHubCredential(
    owner_id="u1",
    mcp_server_ref="github",
    token="tok",
    leg="pat",
    stale_oauth_reason=DegradationReason.STALE_TOKEN,
)
PAT_ONLY = GitHubCredential(owner_id="u1", mcp_server_ref="github", token="tok", leg="pat")
# An UNBOUND row (the user pressed Disconnect) carries CONNECT_REQUIRED, not a stale grant.
PAT_AFTER_DISCONNECT = GitHubCredential(
    owner_id="u1",
    mcp_server_ref="github",
    token="tok",
    leg="pat",
    stale_oauth_reason=DegradationReason.CONNECT_REQUIRED,
)
STALE_NOTHING = DegradationResponse(
    reason=DegradationReason.STALE_TOKEN,
    user_message="Your GitHub connection needs re-authorizing.",
)
NOTHING = DegradationResponse(
    reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub to continue."
)
PROBE_OK = GitHubReposResult(repositories=[{"full_name": "o/r"}])
PROBE_REJECTED = GitHubReposResult(
    repositories=[],
    degradation=DegradationResponse(reason=DegradationReason.STALE_TOKEN, user_message="rejected"),
)


async def _card(credential, probe=PROBE_OK):
    probe_mock = AsyncMock(return_value=probe)
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=credential)),
        patch(f"{_ADAPTER}.search_user_repositories", new=probe_mock),
        patch.object(
            integrations,
            "_get_integration_config_status",
            new=AsyncMock(side_effect=AssertionError("GitHub must not use the config check")),
        ),
    ):
        status = await integrations._check_integration_health("github", _META, user_id="u1")
    return status, probe_mock


@pytest.mark.asyncio
async def test_oauth_serving_is_connected():
    status, probe = await _card(OAUTH)
    assert (
        status.status == "connected"
    )  # #2075: a bound grant with no recorded check claims no health
    assert status.status_message == "Connected with your GitHub account."
    assert (
        status.status_icon is None and status.status_detail == "Not checked yet. Press Test."
    )  # #2187: no record -> unchecked line
    assert status.can_test is True and status.show_test is True
    assert status.action is None
    probe.assert_not_awaited()  # a healthy page load makes no GitHub call


@pytest.mark.asyncio
async def test_pat_serving_with_stale_grant_is_the_warning_token_state():
    status, probe = await _card(PAT_STALE)
    assert status.status == "degraded"
    assert status.status_icon == "⚠️"
    assert status.status_message == "Connected via your personal token"
    assert (
        status.status_detail
        == "Your GitHub connection needs re-authorizing, so I'm not using it right now."
    )
    assert status.can_test is True and status.show_test is True
    assert status.action == "reconnect"  # #2053 (CXO): Reconnect in every stale state
    probe.assert_awaited_once()


@pytest.mark.asyncio
async def test_nothing_serving_with_stale_grant_needs_reconnecting():
    status, probe = await _card(STALE_NOTHING)
    assert status.status == "degraded"
    assert status.status_icon == "⚠️"
    assert status.status_message == "Needs reconnecting"
    assert status.status_detail == "GitHub no longer accepts your connection."
    assert status.show_test is False and status.can_test is False
    assert status.action == "reconnect"
    assert status.configure_url == "/settings/integrations/github"
    probe.assert_not_awaited()


@pytest.mark.asyncio
async def test_stale_grant_and_a_token_github_also_refuses_needs_reconnecting():
    """Same evidence rule as #2029's page: the token state shows only when the token
    answers a read; a refused token leaves nothing serving."""
    status, probe = await _card(PAT_STALE, probe=PROBE_REJECTED)
    assert status.status_message == "Needs reconnecting"
    assert status.action == "reconnect" and status.show_test is False
    probe.assert_awaited_once()


@pytest.mark.asyncio
async def test_nothing_at_all_is_not_configured():
    status, _ = await _card(NOTHING)
    assert status.status == "not_configured"
    assert status.status_message == "Not configured"
    assert status.can_test is False
    assert status.action is None and status.status_icon is None


@pytest.mark.asyncio
@pytest.mark.parametrize("credential", [STALE_NOTHING, PAT_STALE])
async def test_a_stale_binding_never_renders_not_configured(credential):
    for probe in (PROBE_OK, PROBE_REJECTED):
        status, _ = await _card(credential, probe=probe)
        assert status.status != "not_configured"
        assert status.status_message != "Not configured"


@pytest.mark.asyncio
@pytest.mark.parametrize("credential", [PAT_ONLY, PAT_AFTER_DISCONNECT])
async def test_own_token_without_a_stale_grant_keeps_the_configured_path(credential):
    """Outside the four states: the user's own token with no stale grant (including
    after Disconnect, whose UNBOUND row maps to CONNECT_REQUIRED) is configured, and the
    cached Test result / unchecked-card path governs as before. No re-authorize line."""
    with patch.object(integrations, "_get_test_result_store") as store:
        store.return_value.get_test_result.return_value = None
        status, probe = await _card(credential)
    # #2044 (CXO): the configured-but-unchecked card reads "Connected" with the
    # "Not checked yet. Press Test." line; "unknown" never reaches a configured card.
    assert status.status == "connected"
    assert status.status_message == "Connected"
    assert status.status_detail == "Not checked yet. Press Test."
    assert status.can_test is True and status.show_test is True
    assert status.status_icon is None and status.action is None  # no re-authorize glyph/action
    probe.assert_not_awaited()


@pytest.mark.asyncio
async def test_no_user_is_not_configured_without_a_resolver_call():
    resolve = AsyncMock()
    with patch(f"{_ADAPTER}.resolve_credential", new=resolve):
        status = await integrations._check_integration_health("github", _META, user_id=None)
    assert status.status == "not_configured"
    resolve.assert_not_called()


def test_no_mcp_connector_in_the_route_strings():
    import inspect

    assert "mcp connector" not in inspect.getsource(integrations).lower()
    assert not hasattr(integrations, "_github_oauth_bound")
