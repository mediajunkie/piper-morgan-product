"""#1718 — POST /api/v1/keys/store surfaces the SPECIFIC validation-failure reason.

Settings -> LLM API Keys (templates/settings_llm_keys.html) posts here. Before this
fix, a key that failed provider validation was stored anyway (validate=True,
store=True keeps the entered key rather than discard it — #485) but the response
always said the flat "stored successfully", discarding WHY validation failed.

This pins the route contract: when store_user_key's provider-validation attaches a
`.validation_message` (UserAPIKeyService.store_user_key, #1718), the route puts that
SPECIFIC sentence in StoreKeyResponse.message instead of the generic success line —
and the sentence is the SAME one the runtime chat path already uses
(services/ui_messages/user_friendly_errors.py), not new copy.

LAYER (m-43): the real route function (not a curl 200) through FastAPI's TestClient
with get_current_user/get_user_api_key_service dependency-overridden and the DB
session mocked to a no-op context manager — store_user_key itself is mocked so the
test is about the ROUTE's message-selection contract, not the service internals
(covered separately in tests/config/test_llm_key_validation_reasons_1718.py and
tests/security/test_user_api_key_service*.py). DENOMINATOR: quota bucket, invalid-key
bucket, the already-passing case, and the validate=False no-claim case.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims

QUOTA_SENTENCE = (
    "I can't reach a language model — the API key on your account is out of "
    "quota (or its billing needs attention)."
)
INVALID_KEY_SENTENCE = "The language-model API key on your account isn't valid."


def _current_user() -> JWTClaims:
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub="test-user-1718",
        exp=9999999999,
        iat=1234567890,
        jti="test-jti-1718",
        user_id=UUID("00000000-0000-0000-0000-000000000099"),
        user_email="test-1718@example.com",
        username="test1718",
        scopes=["read", "write"],
        token_type="access",
    )


def _fake_session_scope():
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


def _client(stored_key):
    from web.api.routes.api_keys import get_user_api_key_service, router

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = _current_user

    mock_service = MagicMock()
    mock_service.store_user_key = AsyncMock(return_value=stored_key)
    app.dependency_overrides[get_user_api_key_service] = lambda: mock_service

    return TestClient(app), mock_service


def _stored_key(is_validated: bool, validation_message=None):
    key = MagicMock()
    key.is_validated = is_validated
    key.validation_message = validation_message
    return key


class TestStoreKeyHonestMessage:
    def test_quota_failure_message_is_the_quota_sentence_not_flat_invalid(self):
        key = _stored_key(is_validated=False, validation_message=QUOTA_SENTENCE)
        client, mock_service = _client(key)
        with patch(
            "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
            lambda: _fake_session_scope(),
        ):
            resp = client.post(
                "/api/v1/keys/store",
                json={"provider": "anthropic", "api_key": "sk-ant-no-credit"},
            )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["is_validated"] is False
        assert body["message"] == QUOTA_SENTENCE
        assert "invalid" not in body["message"].lower()

    def test_rejected_credential_message_is_the_invalid_key_sentence(self):
        key = _stored_key(is_validated=False, validation_message=INVALID_KEY_SENTENCE)
        client, mock_service = _client(key)
        with patch(
            "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
            lambda: _fake_session_scope(),
        ):
            resp = client.post(
                "/api/v1/keys/store",
                json={"provider": "openai", "api_key": "sk-bad"},
            )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["is_validated"] is False
        assert body["message"] == INVALID_KEY_SENTENCE

    def test_valid_key_keeps_the_success_message(self):
        key = _stored_key(is_validated=True, validation_message=None)
        client, mock_service = _client(key)
        with patch(
            "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
            lambda: _fake_session_scope(),
        ):
            resp = client.post(
                "/api/v1/keys/store",
                json={"provider": "anthropic", "api_key": "sk-ant-good"},
            )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["is_validated"] is True
        assert body["message"] == "API key for anthropic stored successfully"

    def test_validate_false_does_not_claim_a_failure_that_never_happened(self):
        """request.validate=False skips provider validation entirely —
        is_validated=False there means "unknown," not "rejected." The route
        must not borrow the failure copy for a check that was never run."""
        key = _stored_key(is_validated=False, validation_message=None)
        client, mock_service = _client(key)
        with patch(
            "web.api.routes.api_keys.AsyncSessionFactory.session_scope",
            lambda: _fake_session_scope(),
        ):
            resp = client.post(
                "/api/v1/keys/store",
                json={"provider": "anthropic", "api_key": "sk-ant-unchecked", "validate": False},
            )
        assert resp.status_code == 201, resp.text
        body = resp.json()
        assert body["is_validated"] is False
        assert body["message"] == "API key for anthropic stored successfully"
