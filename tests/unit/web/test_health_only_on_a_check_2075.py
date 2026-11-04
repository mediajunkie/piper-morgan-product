"""#2075 (CXO's ruling): the Integrations headline claims health only for connected
integrations with a recorded check for THIS account. A bound OAuth grant nobody has
tested is "connected" (the #2044 unchecked status), the headline reads "Connected, not
yet tested" and the count line counts checks ("0 of 1 checked"). After a Test it reads
"All Systems Healthy | 1 of 1 connected integrations working". The card line stays
"Connected as octocat. Not the right account? Disconnect, then connect again." The PAT leg is unchanged.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

import web.api.routes.integrations as integ
from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes.integrations import IntegrationStatus, summarize_integrations

_PRINCIPAL = "user-2075"


def _oauth_credential():
    return SimpleNamespace(leg="oauth", stale_oauth_reason=None)


METADATA = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}


def _adapter_cls():
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return GitHubMCPSpatialAdapter


async def _oauth_card(store: PrincipalTestResultStore):
    with (
        patch.object(
            _adapter_cls(), "resolve_credential", AsyncMock(return_value=_oauth_credential())
        ),
        patch.object(integ, "_get_test_result_store", lambda: store),
    ):
        return await integ._github_card(METADATA, _PRINCIPAL)


@pytest.mark.asyncio
async def test_bound_grant_with_no_recorded_check_is_connected_not_healthy():
    card = await _oauth_card(PrincipalTestResultStore())
    assert card is not None
    assert card.status == "connected"
    assert (
        card.status_message
        == "Connected as octocat. Not the right account? Disconnect, then connect again."
    )
    assert card.last_check is None


@pytest.mark.asyncio
async def test_bound_grant_with_a_passing_check_is_healthy():
    store = PrincipalTestResultStore()
    store.record_test_result(_PRINCIPAL, "github", True)
    card = await _oauth_card(store)
    assert card is not None
    assert card.status == "healthy"
    assert (
        card.status_message
        == "Connected as octocat. Not the right account? Disconnect, then connect again."
    )
    assert card.last_check is not None


@pytest.mark.asyncio
async def test_bound_grant_with_a_failing_check_is_failed():
    store = PrincipalTestResultStore()
    store.record_test_result(_PRINCIPAL, "github", False, error="GitHub said no")
    card = await _oauth_card(store)
    assert card is not None
    assert card.status == "failed"
    assert card.error == "GitHub said no"


@pytest.mark.asyncio
async def test_another_accounts_check_does_not_make_this_card_healthy():
    store = PrincipalTestResultStore()
    store.record_test_result("someone-else", "github", True)
    card = await _oauth_card(store)
    assert card is not None
    assert card.status == "connected"


def _card(status: str) -> IntegrationStatus:
    return IntegrationStatus(
        name="github",
        display_name="GitHub",
        status=status,
        status_message="Connected as octocat. Not the right account? Disconnect, then connect again.",
        can_test=True,
    )


def test_headline_before_any_check_counts_checks_not_health():
    overall, headline, summary, working, connected = summarize_integrations([_card("connected")])
    assert (overall, headline) == ("unknown", "Connected, not yet tested")
    assert summary == "0 of 1 checked"
    assert (working, connected) == (0, 1)


def test_headline_after_a_passing_check_is_all_systems_healthy():
    overall, headline, summary, working, connected = summarize_integrations([_card("healthy")])
    assert (overall, headline) == ("healthy", "All Systems Healthy")
    assert summary == "1 of 1 connected integrations working"


def test_count_line_with_one_checked_and_one_not():
    cards = [_card("healthy"), _card("connected")]
    _, headline, summary, *_ = summarize_integrations(cards)
    assert headline == "Connected, not yet tested"
    assert summary == "1 of 2 checked"


def _named(name: str, status: str) -> IntegrationStatus:
    return IntegrationStatus(
        name=name, display_name=name.title(), status=status, status_message="", can_test=True
    )


def test_failure_branch_counts_checked_only_and_names_the_untested():
    # CXO ruling 2026-10-17 (xian's A1 sitting): GitHub needs reconnecting, Calendar
    # connected and untested. Never "0 of 2 connected integrations working".
    cards = [_named("github", "failed"), _named("calendar", "connected")]
    overall, headline, summary, working, connected = summarize_integrations(cards)
    assert (overall, headline) == ("degraded", "Needs attention")
    assert summary == "0 of 1 checked integrations working, 1 not yet tested"
    assert (working, connected) == (0, 2)


def test_failure_branch_with_nothing_untested_has_no_tail():
    cards = [_named("github", "failed"), _named("calendar", "healthy")]
    _, headline, summary, *_ = summarize_integrations(cards)
    assert headline == "Needs attention"
    assert summary == "1 of 2 checked integrations working"


def test_after_reconnect_with_both_untested_counts_zero_checked():
    # The second half of CXO's acceptance: never "1 of 2 ... working" with both untested.
    cards = [_named("github", "connected"), _named("calendar", "connected")]
    overall, headline, summary, *_ = summarize_integrations(cards)
    assert (overall, headline) == ("unknown", "Connected, not yet tested")
    assert summary == "0 of 2 checked"


def test_multiple_issues_branch_uses_the_same_count_shape():
    cards = [_named("github", "failed"), _named("slack", "failed"), _named("calendar", "connected")]
    overall, headline, summary, *_ = summarize_integrations(cards)
    assert (overall, headline) == ("unhealthy", "Multiple Issues")
    assert summary == "0 of 2 checked integrations working, 1 not yet tested"


@pytest.fixture(autouse=True)
def _login_octocat_2279(monkeypatch):
    """#2279: the OAuth card now reads the account's login through its own grant."""
    from unittest.mock import AsyncMock as _AM

    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter as _A

    monkeypatch.setattr(_A, "account_login", _AM(return_value="octocat"))
