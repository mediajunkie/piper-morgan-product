"""#1485 — global credential writes require admin authority, not mere authentication.

Three routes in web/api/routes/settings_integrations.py write GLOBAL (app-wide,
unscoped) credentials from a per-user settings surface:

  - POST /slack/app-token        → keychain `slack_app_token` (no username scope)
  - POST /slack/app-credentials  → slack client_id/client_secret (IntegrationConfigService:
                                   "server-wide configuration, NOT per-user")
  - POST /calendar/app-credentials → google client_id/client_secret (same service)

Audit predicate (issue AC, m-44 family): every `KeychainService.store_api_key` call
WITHOUT a `username=` kwarg + every `IntegrationConfigService.store_*` call reachable
from this router. Per-user writes (calendar refresh token under `google_calendar_{user_id}`,
`github_token` with `username=current_user.sub`) are out of scope and NOT gated.

The authorization mechanism is the codebase's existing privileged-user concept:
the `users.is_admin` DB column (#357 SEC-RBAC), checked live via the new
`require_admin` dependency (services/auth/auth_middleware.py).

Per the issue AC, the load-bearing tests here exercise an AUTHENTICATED NON-ADMIN
caller through the real dependency graph (TestClient + dependency_overrides on
get_current_user only — require_admin itself runs for real, with the one-line DB
read patched at its boundary) and assert refusal WITHOUT a write. A suite whose
non-admin caller never reaches the route would pass vacuously.

Also pins: the #1484 contract is not weakened — flag-unset still 409s before any
write for an admin, and a non-admin is refused before any write regardless of flag.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user, require_admin
from web.api.routes.settings_integrations import router

ADMIN_ID = uuid4()
NON_ADMIN_ID = uuid4()


def _claims(user_id):
    claims = MagicMock()
    claims.user_id = user_id
    claims.sub = str(user_id)
    return claims


def _client(user_id) -> TestClient:
    """App with the real router; only authentication is overridden.

    require_admin is NOT overridden — the admin check itself is under test.
    """
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: _claims(user_id)
    return TestClient(app, raise_server_exceptions=False)


def _patch_is_admin():
    """Patch the DB read at its boundary: ADMIN_ID is admin, everyone else is not."""

    async def fake(user_id):
        return str(user_id) == str(ADMIN_ID)

    return patch("services.auth.auth_middleware._user_is_admin", side_effect=fake)


# ---- POST /slack/app-token (the #1485 headline write) ----


def test_non_admin_app_token_write_refused_403_and_no_keychain_write(monkeypatch):
    """The issue's core AC: an authenticated NON-admin must be refused, and the
    global keychain write must never happen."""
    monkeypatch.setenv("PIPER_SLACK_INBOUND_ENABLED", "true")
    stored = []
    with (
        _patch_is_admin(),
        patch("services.infrastructure.keychain_service.KeychainService") as KC,
    ):
        KC.return_value.store_api_key = lambda *a, **k: stored.append(a)
        resp = _client(NON_ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-token",
            json={"app_token": "xapp-1-nonadmin-attempt"},
        )
    assert resp.status_code == 403
    # Honest refusal: says why, and that nothing was saved (CXO refusal contract).
    detail = resp.json().get("detail", "")
    assert "admin" in detail.lower()
    assert not stored, "a refused non-admin call must NEVER reach the keychain write"


def test_non_admin_refused_without_write_even_when_flag_unset(monkeypatch):
    """Authz refusal precedes the #1484 feature gate; either way NOTHING is written."""
    monkeypatch.delenv("PIPER_SLACK_INBOUND_ENABLED", raising=False)
    stored = []
    with (
        _patch_is_admin(),
        patch("services.infrastructure.keychain_service.KeychainService") as KC,
    ):
        KC.return_value.store_api_key = lambda *a, **k: stored.append(a)
        resp = _client(NON_ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-token",
            json={"app_token": "xapp-1-nonadmin-attempt"},
        )
    assert resp.status_code in (403, 409)
    assert not stored


def test_admin_app_token_write_still_works(monkeypatch):
    """Positive control: the privileged user's write must still succeed — and it
    proves the store mock records writes, so the refusal tests' belts mean something."""
    monkeypatch.setenv("PIPER_SLACK_INBOUND_ENABLED", "true")
    stored = []
    with (
        _patch_is_admin(),
        patch("services.infrastructure.keychain_service.KeychainService") as KC,
        patch(
            "services.integrations.slack.socket_mode_runner.restart_socket_runner",
            AsyncMock(return_value=MagicMock(is_connected=True)),
        ),
    ):
        KC.return_value.store_api_key = lambda *a, **k: stored.append(a)
        resp = _client(ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-token",
            json={"app_token": "xapp-1-admin-save"},
        )
    assert resp.status_code == 200
    assert stored == [("slack_app_token", "xapp-1-admin-save")]
    assert resp.json()["state"] == "listening"


def test_admin_with_flag_unset_still_409_before_write(monkeypatch):
    """#1484 contract not weakened: gate-closed refusal (409, 'wasn't saved')
    still holds for an ADMIN, before any keychain write."""
    monkeypatch.delenv("PIPER_SLACK_INBOUND_ENABLED", raising=False)
    stored = []
    with (
        _patch_is_admin(),
        patch("services.infrastructure.keychain_service.KeychainService") as KC,
    ):
        KC.return_value.store_api_key = lambda *a, **k: stored.append(a)
        resp = _client(ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-token",
            json={"app_token": "xapp-1-admin-save"},
        )
    assert resp.status_code == 409
    assert "wasn't saved" in resp.json()["detail"]
    assert not stored


# ---- the sibling global writes found by the audit ----


def test_non_admin_slack_app_credentials_refused_no_write():
    with (
        _patch_is_admin(),
        patch("services.integrations.integration_config_service.IntegrationConfigService") as ICS,
    ):
        resp = _client(NON_ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-credentials",
            json={"client_id": "123.456", "client_secret": "shhh"},
        )
    assert resp.status_code == 403
    ICS.return_value.store_slack_credentials.assert_not_called()


def test_non_admin_calendar_app_credentials_refused_no_write():
    with (
        _patch_is_admin(),
        patch("services.integrations.integration_config_service.IntegrationConfigService") as ICS,
    ):
        resp = _client(NON_ADMIN_ID).post(
            "/api/v1/settings/integrations/calendar/app-credentials",
            json={"client_id": "abc.apps.googleusercontent.com", "client_secret": "shhh"},
        )
    assert resp.status_code == 403
    ICS.return_value.store_google_credentials.assert_not_called()


def test_admin_slack_app_credentials_write_works():
    with (
        _patch_is_admin(),
        patch("services.integrations.integration_config_service.IntegrationConfigService") as ICS,
    ):
        resp = _client(ADMIN_ID).post(
            "/api/v1/settings/integrations/slack/app-credentials",
            json={"client_id": "123.456", "client_secret": "shhh"},
        )
    assert resp.status_code == 200
    ICS.return_value.store_slack_credentials.assert_called_once_with("123.456", "shhh")


# ---- require_admin itself: fail-closed ----


@pytest.mark.asyncio
async def test_require_admin_fails_closed_on_db_error():
    """A lookup failure must refuse (503), never allow — fail-closed."""
    from fastapi import HTTPException

    with patch(
        "services.auth.auth_middleware._user_is_admin",
        side_effect=RuntimeError("db down"),
    ):
        with pytest.raises(HTTPException) as exc:
            await require_admin(current_user=_claims(ADMIN_ID))
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_require_admin_refuses_non_admin_403():
    from fastapi import HTTPException

    with _patch_is_admin():
        with pytest.raises(HTTPException) as exc:
            await require_admin(current_user=_claims(NON_ADMIN_ID))
    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_require_admin_returns_claims_for_admin():
    with _patch_is_admin():
        claims = await require_admin(current_user=_claims(ADMIN_ID))
    assert str(claims.user_id) == str(ADMIN_ID)
