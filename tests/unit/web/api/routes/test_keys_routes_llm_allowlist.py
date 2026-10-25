"""Arch's 10-25 ruling (CXO's option (a)): the /api/v1/keys routes serve only the LLM
providers, as an allowlist. user_api_keys also holds connector credentials (the GitHub
PAT at rest as `github`, OAuth grants as `{connector}_mcp_oauth`). Listed on the "LLM
API Keys" page, a Remove there deleted one copy while the connection stayed live.

LAYER: the real route functions through FastAPI's TestClient, the service mocked so the
pins are about what the routes let through. DENOMINATOR: list, plus store, validate,
rotate and delete, each for `github` and `github_mcp_oauth`.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims

REFUSAL = (
    "This page is for AI provider keys only. Connected services like GitHub, "
    "Google Calendar and Notion are managed in Settings → Integrations."
)
CONNECTOR_ROWS = ["github", "github_mcp_oauth"]


def _current_user() -> JWTClaims:
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub="test-user-allowlist",
        exp=9999999999,
        iat=1234567890,
        jti="test-jti-allowlist",
        user_id=UUID("00000000-0000-0000-0000-000000000098"),
        user_email="test-allowlist@example.com",
        username="testallowlist",
        scopes=["read", "write"],
        token_type="access",
    )


def _fake_session_scope():
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


def _row(provider):
    return {
        "provider": provider,
        "is_active": True,
        "is_validated": True,
        "last_validated_at": None,
        "created_at": "2026-10-25T00:00:00",
        "rotated_at": None,
    }


@pytest.fixture
def client():
    from web.api.routes.api_keys import get_user_api_key_service, router

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = _current_user
    service = MagicMock()
    service.list_user_keys = AsyncMock(
        return_value=[
            _row("anthropic"),
            _row("github"),
            _row("github_mcp_oauth"),
            _row("google_calendar_mcp_oauth"),
            _row("openai"),
        ]
    )
    for name in ("store_user_key", "delete_user_key", "validate_user_key", "rotate_user_key"):
        setattr(service, name, AsyncMock())
    app.dependency_overrides[get_user_api_key_service] = lambda: service
    with patch(
        "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
        side_effect=lambda: _fake_session_scope(),
    ):
        yield TestClient(app), service


def test_list_returns_only_llm_providers(client):
    c, _ = client
    res = c.get("/api/v1/keys/list")
    assert res.status_code == 200, res.text
    assert sorted(k["provider"] for k in res.json()) == ["anthropic", "openai"]


def test_list_with_only_connector_rows_is_empty(client):
    """CXO's condition: the page picks its no-keys state after the filter."""
    c, service = client
    service.list_user_keys.return_value = [_row(p) for p in CONNECTOR_ROWS]
    assert c.get("/api/v1/keys/list").json() == []


@pytest.mark.parametrize("provider", CONNECTOR_ROWS)
@pytest.mark.parametrize(
    "method,path,body,service_call",
    [
        ("delete", "/api/v1/keys/{p}", None, "delete_user_key"),
        ("post", "/api/v1/keys/{p}/validate", None, "validate_user_key"),
        (
            "post",
            "/api/v1/keys/{p}/rotate",
            {"new_api_key": "fake-token-rotate"},
            "rotate_user_key",
        ),
        (
            "post",
            "/api/v1/keys/store",
            {"provider": "{p}", "api_key": "fake-token-store"},
            "store_user_key",
        ),
    ],
)
def test_connector_writes_refuse_and_touch_nothing(
    client, provider, method, path, body, service_call
):
    c, service = client
    kwargs = {}
    if body is not None:
        kwargs["json"] = {k: v.replace("{p}", provider) for k, v in body.items()}
    res = getattr(c, method)(path.replace("{p}", provider), **kwargs)
    assert res.status_code == 400
    assert res.json()["detail"] == REFUSAL
    getattr(service, service_call).assert_not_called()


def test_an_llm_provider_still_deletes(client):
    c, service = client
    service.delete_user_key.return_value = True
    res = c.delete("/api/v1/keys/anthropic")
    assert res.status_code == 200, res.text
    service.delete_user_key.assert_awaited_once()


def test_allowlist_is_the_llm_provider_enum():
    from services.llm.config import LLMProvider
    from web.api.routes.api_keys import LLM_KEY_PROVIDERS

    assert LLM_KEY_PROVIDERS == {p.value for p in LLMProvider}
    assert not any(p.endswith("_mcp_oauth") or p == "github" for p in LLM_KEY_PROVIDERS)
