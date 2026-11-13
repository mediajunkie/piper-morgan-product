"""#2367 (CXO's words, 2026-11-13): a Gemini key can't be saved through the keys API.

No reply can be served on a Gemini key (#1819). The keys page stopped offering one in
#2366; a direct API save that returned success would give the same wrong belief and
could leave an account whose only key Piper can't use. So store and rotate refuse with
a plain 400 and CXO's sentence, and store nothing. A key stored earlier is untouched:
still listed, still removable.

LAYER: the real route functions through FastAPI's TestClient, the service mocked.
DENOMINATOR: store and rotate refused for gemini; store for anthropic and openai
unchanged; list and delete for an existing gemini row unchanged.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims

REFUSAL = "Piper doesn't use Google (Gemini) keys yet. Anthropic and OpenAI keys work."


def _current_user() -> JWTClaims:
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub="test-user-2367",
        exp=9999999999,
        iat=1234567890,
        jti="test-jti-2367",
        user_id=UUID("00000000-0000-0000-0000-000000002367"),
        user_email="test-2367@example.com",
        username="test2367",
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
        "created_at": "2026-10-01T00:00:00",
        "rotated_at": None,
    }


@pytest.fixture
def client():
    from web.api.routes.api_keys import get_user_api_key_service, router

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = _current_user
    service = MagicMock()
    service.list_user_keys = AsyncMock(return_value=[_row("gemini"), _row("openai")])
    for name in ("store_user_key", "delete_user_key", "validate_user_key", "rotate_user_key"):
        setattr(service, name, AsyncMock())
    app.dependency_overrides[get_user_api_key_service] = lambda: service
    with patch(
        "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
        side_effect=lambda: _fake_session_scope(),
    ):
        yield TestClient(app), service


def test_a_gemini_save_is_refused_in_cxos_words_and_stores_nothing(client):
    c, service = client
    res = c.post("/api/v1/keys/store", json={"provider": "gemini", "api_key": "not-a-real-key"})
    assert res.status_code == 400
    assert res.json()["detail"] == REFUSAL
    service.store_user_key.assert_not_called()


def test_a_gemini_rotate_is_refused_the_same_way(client):
    c, service = client
    res = c.post("/api/v1/keys/gemini/rotate", json={"new_api_key": "not-a-real-key"})
    assert res.status_code == 400
    assert res.json()["detail"] == REFUSAL
    service.rotate_user_key.assert_not_called()


@pytest.mark.parametrize("provider", ["anthropic", "openai"])
def test_anthropic_and_openai_saves_still_reach_the_service(client, provider):
    c, service = client
    c.post("/api/v1/keys/store", json={"provider": provider, "api_key": "not-a-real-key"})
    service.store_user_key.assert_called_once()
    assert service.store_user_key.call_args.kwargs["provider"] == provider


def test_a_stored_gemini_key_is_still_listed(client):
    c, _ = client
    res = c.get("/api/v1/keys/list")
    assert res.status_code == 200, res.text
    assert sorted(k["provider"] for k in res.json()) == ["gemini", "openai"]


def test_a_stored_gemini_key_can_still_be_removed(client):
    c, service = client
    service.delete_user_key.return_value = True
    res = c.delete("/api/v1/keys/gemini")
    assert res.status_code == 200, res.text
    service.delete_user_key.assert_called_once()


def test_the_refused_set_is_derived_from_the_one_list_of_providers_that_can_serve():
    """Arch's mechanism (14:38): no second hand-written list. Today the set is Gemini."""
    from services.llm.config import LLMProvider
    from services.llm.request_key import PER_REQUEST_CLIENT_PROVIDERS
    from web.api.routes import api_keys

    every = {p.value for p in LLMProvider}
    assert api_keys.UNSERVED_LLM_PROVIDERS == every - PER_REQUEST_CLIENT_PROVIDERS
    assert api_keys.UNSERVED_LLM_PROVIDERS == frozenset({"gemini"})
    assert api_keys.PROVIDER_NOT_USED_YET == REFUSAL
    assert "#" not in REFUSAL and "alpha" not in REFUSAL.lower()


def _unserved():
    from services.llm.config import LLMProvider
    from services.llm.request_key import PER_REQUEST_CLIENT_PROVIDERS

    return sorted({p.value for p in LLMProvider} - PER_REQUEST_CLIENT_PROVIDERS)


@pytest.mark.parametrize("provider", _unserved())
def test_store_refuses_and_remove_accepts_every_provider_that_cannot_serve(client, provider):
    """Arch's pin: each LLMProvider value outside PER_REQUEST_CLIENT_PROVIDERS."""
    c, service = client
    res = c.post("/api/v1/keys/store", json={"provider": provider, "api_key": "not-a-real-key"})
    assert res.status_code == 400
    assert res.json()["detail"] == REFUSAL
    service.store_user_key.assert_not_called()
    service.delete_user_key.return_value = True
    assert c.delete(f"/api/v1/keys/{provider}").status_code == 200


def test_the_words_name_gemini_so_the_set_must_stay_gemini_only_until_reworded():
    """CXO's sentence names Google (Gemini). If another unserved provider is ever added
    to LLMProvider, this fails and the words need CXO before the refusal covers it."""
    assert _unserved() == ["gemini"]
