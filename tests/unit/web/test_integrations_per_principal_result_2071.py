"""#2071 (Arch-ruled shape, Gate class 2): the Integrations Test result is keyed by
(principal, integration). One account's Test never sets the status, error text or check
time another account sees, on the card or in chat.

Two accounts, two JWTs, one app (TestClient). Account A presses Test and fails; B's card
for that integration stays the unchecked card and ``IntegrationStatusService.get_status``
for B has ``healthy=None``. B's own pass does not show on A's card, and A's card keeps
A's failure with A's error sentence. ``_recorded_check_iso`` (the GitHub OAuth card's
time, #2066) for B stays None after A's GitHub Test.

Layers: the real Test route (POST) and health route (GET) through the app's TestClient,
the provider's own test function patched to fail or pass (no network); the status
service read with the real per-principal store. Not a browser, not a served host.
"""

from __future__ import annotations

import uuid
from typing import Dict
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.integrations import integration_status_service as iss_mod
from services.integrations.integration_status_service import IntegrationStatusService
from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes import integrations
from web.app import app

HEALTH = "/api/v1/integrations/health"
A_ERROR = "Token expired or revoked for a-private-workspace. Please reconnect."
UNCHECKED = {
    "status": "connected",
    "status_message": "Connected",
    "status_detail": "Not checked yet. Press Test.",
}
# The generic (non-GitHub) card path; GitHub's PAT leg reaches it too.
PROVIDERS = [k for k in integrations.INTEGRATION_REGISTRY if k != "github"]


def _client(email: str):
    user_id = uuid.uuid4()
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=user_id, user_email=email, scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c, str(user_id)


@pytest.fixture
def accounts():
    a, a_id = _client("a2071@example.com")
    b, b_id = _client("b2071@example.com")
    return {"a": a, "a_id": a_id, "b": b, "b_id": b_id}


@pytest.fixture
def store():
    """A fresh store per test, shared by the route and the status service like the
    process singleton is."""
    s = PrincipalTestResultStore()
    with (
        patch.object(integrations, "_get_test_result_store", return_value=s),
        patch.object(iss_mod, "get_test_result_store", return_value=s),
        patch.object(
            integrations, "_get_integration_config_status", new=AsyncMock(return_value="configured")
        ),
        patch.object(integrations, "_github_card", new=AsyncMock(return_value=None)),
    ):
        yield s


def _press_test(client, provider: str, ok: bool, error: str = A_ERROR) -> Dict:
    outcome = {"success": True} if ok else {"success": False, "error": error}
    with patch.object(integrations, "_test_integration", new=AsyncMock(return_value=outcome)):
        r = client.post(f"/api/v1/integrations/test/{provider}")
    assert r.status_code == 200, r.text
    assert r.json()["success"] is ok
    return r.json()


def _card(client, provider: str) -> Dict:
    r = client.get(HEALTH)
    assert r.status_code == 200, r.text
    (card,) = [c for c in r.json()["integrations"] if c["name"] == provider]
    return card


async def _chat_status(user_id: str, provider: str) -> Dict:
    with patch.object(
        iss_mod, "get_config_status", new=AsyncMock(return_value=("configured", "keychain"))
    ):
        return await IntegrationStatusService().get_status(user_id, provider)


@pytest.mark.parametrize("provider", PROVIDERS)
@pytest.mark.asyncio
async def test_a_failure_leaves_b_unchecked_on_the_card_and_in_chat(accounts, store, provider):
    _press_test(accounts["a"], provider, ok=False)

    b_card = _card(accounts["b"], provider)
    for key, want in UNCHECKED.items():
        assert b_card[key] == want, (provider, b_card)
    assert b_card["last_check"] is None and b_card["error"] is None
    assert "a-private-workspace" not in str(b_card)

    b_chat = await _chat_status(accounts["b_id"], provider)
    assert b_chat["healthy"] is None and b_chat["last_check"] is None

    # A sees A's own failure, in A's words, and chat says so for A.
    a_card = _card(accounts["a"], provider)
    assert a_card["status"] == "failed"
    assert a_card["status_message"] == A_ERROR
    assert a_card["error"] == A_ERROR
    assert a_card["last_check"] is not None
    a_chat = await _chat_status(accounts["a_id"], provider)
    assert a_chat["healthy"] is False and a_chat["last_check"] is not None


@pytest.mark.parametrize("provider", PROVIDERS)
@pytest.mark.asyncio
async def test_b_success_does_not_show_on_a_card(accounts, store, provider):
    _press_test(accounts["a"], provider, ok=False)
    _press_test(accounts["b"], provider, ok=True)

    a_card = _card(accounts["a"], provider)
    assert a_card["status"] == "failed", a_card
    assert a_card["status_message"] == A_ERROR
    assert (await _chat_status(accounts["a_id"], provider))["healthy"] is False

    b_card = _card(accounts["b"], provider)
    assert b_card["status"] == "healthy" and b_card["status_message"] == "Healthy"
    assert b_card["error"] is None
    assert (await _chat_status(accounts["b_id"], provider))["healthy"] is True


@pytest.mark.asyncio
async def test_failures_do_not_accumulate_across_accounts_and_success_resets(accounts, store):
    """Counts were host-wide (over 3 DEGRADED, over 10 FAILED, never reset)."""
    for _ in range(12):
        _press_test(accounts["a"], "calendar", ok=False)
    assert store.get_test_result(accounts["a_id"], "calendar").error_count == 12
    assert store.get_test_result(accounts["b_id"], "calendar") is None
    _press_test(accounts["b"], "calendar", ok=False, error="B's own sentence.")
    assert store.get_test_result(accounts["b_id"], "calendar").error_count == 1
    assert _card(accounts["b"], "calendar")["status_message"] == "B's own sentence."
    _press_test(accounts["a"], "calendar", ok=True)
    assert store.get_test_result(accounts["a_id"], "calendar").error_count == 0


def test_github_recorded_check_for_b_is_none_after_a_github_test(accounts, store):
    """#2066's OAuth-card time reads the viewer's own result only."""
    _press_test(accounts["a"], "github", ok=True)
    assert integrations._recorded_check_iso(accounts["a_id"], "github") is not None
    assert integrations._recorded_check_iso(accounts["b_id"], "github") is None
    _press_test(accounts["a"], "github", ok=False)
    assert integrations._recorded_check_iso(accounts["b_id"], "github") is None


def test_raw_exception_text_from_a_test_reaches_no_card(accounts, store):
    """#2151 (Arch 10-24 12:32): a Test that raised is a check that couldn't run, so
    nothing is recorded: A's exception text reaches neither A's card nor B's (it used to
    be recorded under A only)."""
    with patch.object(
        integrations,
        "_test_integration",
        new=AsyncMock(side_effect=RuntimeError("database a-private-workspace not found")),
    ):
        r = accounts["a"].post("/api/v1/integrations/test/notion")
    assert r.status_code == 200 and r.json()["success"] is False
    assert "a-private-workspace" not in r.text
    for who in ("a", "b"):
        card = _card(accounts[who], "notion")
        assert "a-private-workspace" not in str(card)
    assert _card(accounts["b"], "notion")["status_detail"] == UNCHECKED["status_detail"]


def test_no_principal_records_nothing_and_reads_nothing():
    s = PrincipalTestResultStore()
    assert s.record_test_result(None, "slack", ok=False, error="x") is None
    assert s.record_test_result("", "slack", ok=True) is None
    assert s.get_test_result(None, "slack") is None
    s.record_test_result("u1", "slack", ok=True)
    assert s.get_test_result(None, "slack") is None
    assert s.get_test_result("u2", "slack") is None
