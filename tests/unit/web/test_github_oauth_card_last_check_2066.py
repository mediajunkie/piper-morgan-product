"""#2066: the OAuth-leg GitHub card carries last_check once a real check is recorded.

Web's served round on d741214b6c: an OAuth-connected account's card had ``last_check: null``
after a passed Test, so the #2045 time line never rendered. The card builder (#2031) returned
the OAuth leg without the health monitor's timestamp; it now carries it the way the generic
path does, and never the startup UNKNOWN stamp (#2044).
"""

from __future__ import annotations

import time
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes import integrations as integrations_routes


def _oauth_credential():
    return SimpleNamespace(leg="oauth", stale_oauth_reason=None)


def _store(*principals):
    """#2071: the Test result is per principal; record a GitHub pass for each one named."""
    store = PrincipalTestResultStore()
    for principal in principals:
        store.record_test_result(principal, "github", ok=True)
    return store


METADATA = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}


@pytest.mark.asyncio
async def test_oauth_card_carries_last_check_after_a_recorded_check():
    started = time.time()
    with (
        patch.object(
            _adapter_cls(),
            "resolve_credential",
            AsyncMock(return_value=_oauth_credential()),
        ),
        patch.object(
            integrations_routes,
            "_get_test_result_store",
            lambda: _store("user-1"),
        ),
    ):
        card = await integrations_routes._github_card(METADATA, "user-1")
    assert card is not None
    assert card.status == "healthy"
    assert (
        card.status_message
        == "Connected as octocat. Not the right account? Disconnect, then connect again."
    )
    assert card.last_check is not None
    assert card.last_check.startswith("20")  # ISO 8601, UTC
    assert datetime.fromisoformat(card.last_check).timestamp() >= started - 1


@pytest.mark.asyncio
async def test_oauth_card_has_no_last_check_before_any_real_check():
    with (
        patch.object(
            _adapter_cls(), "resolve_credential", AsyncMock(return_value=_oauth_credential())
        ),
        patch.object(
            integrations_routes,
            "_get_test_result_store",
            lambda: _store("someone-else"),  # #2071: another account's Test is not a check
        ),
    ):
        card = await integrations_routes._github_card(METADATA, "user-1")
    assert card is not None
    assert card.status == "connected"  # #2075: no recorded check, no health claim
    assert card.last_check is None


def _adapter_cls():
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return GitHubMCPSpatialAdapter


@pytest.fixture(autouse=True)
def _login_octocat_2279(monkeypatch):
    """#2279: the OAuth card now reads the account's login through its own grant."""
    from unittest.mock import AsyncMock as _AM

    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter as _A

    monkeypatch.setattr(_A, "account_login", _AM(return_value="octocat"))
