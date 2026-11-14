"""#2368 (Arch's ruling, 2026-11-13 15:14): setup's `default_llm_provider` is validated.

`complete_setup` appends the value to `authorized_llm_providers` (the #946 consent
list) and stores it as the person's default. It was a free string: a direct call with
"gemini", or anything else, was accepted and stored. The consent list is permission
data, so it never holds an unvalidated string. The request model now accepts nothing,
or a provider a reply can be served on (`PER_REQUEST_CLIENT_PROVIDERS`), and refuses
the rest before `complete_setup` runs. CXO's words (15:23): "gemini" gets the #2367
sentence, which names Gemini; any other value gets its own sentence.

Layers: the model directly, and the route through the app's TestClient with a signed-in
cookie (the refusal is FastAPI's 422, and nothing is opened or stored).
"""

from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from services.auth.container import AuthContainer
from services.llm.config import LLMProvider
from services.llm.request_key import PER_REQUEST_CLIENT_PROVIDERS
from web.api.routes import setup as setup_routes
from web.api.routes.setup import SetupCompleteRequest
from web.app import app

GEMINI_WORDS = "Piper doesn't use Google (Gemini) keys yet. Anthropic and OpenAI keys work."
OTHER_WORDS = "That isn't a provider Piper uses. Anthropic and OpenAI keys work."
REFUSED = [
    ("gemini", GEMINI_WORDS),
    ("not-a-provider", OTHER_WORDS),
    ("", OTHER_WORDS),
    ("OpenAI", OTHER_WORDS),
    ("anthropic ", OTHER_WORDS),
    ("Gemini", OTHER_WORDS),
]


@pytest.mark.parametrize("value,words", REFUSED)
def test_the_model_refuses_a_provider_that_cannot_serve(value, words):
    with pytest.raises(ValidationError) as exc:
        SetupCompleteRequest(default_llm_provider=value)
    text = str(exc.value)
    assert words in text
    other = OTHER_WORDS if words is GEMINI_WORDS else GEMINI_WORDS
    assert other not in text


@pytest.mark.parametrize("value", [None, "anthropic", "openai"])
def test_the_model_accepts_nothing_or_a_provider_that_can_serve(value):
    assert SetupCompleteRequest(default_llm_provider=value).default_llm_provider == value


def test_the_accepted_set_is_the_one_list_of_providers_that_can_serve():
    """No second list: every LLMProvider value is accepted exactly when it is in
    PER_REQUEST_CLIENT_PROVIDERS."""
    for provider in LLMProvider:
        if provider.value in PER_REQUEST_CLIENT_PROVIDERS:
            SetupCompleteRequest(default_llm_provider=provider.value)
        else:
            with pytest.raises(ValidationError):
                SetupCompleteRequest(default_llm_provider=provider.value)


@pytest.fixture(scope="module")
def client():
    return TestClient(app, follow_redirects=False)


def _token() -> str:
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2368@example.com", scopes=["user"]
    )


@pytest.mark.parametrize("value,words", [("gemini", GEMINI_WORDS), ("not-a-provider", OTHER_WORDS)])
def test_the_route_refuses_before_anything_is_stored(client, value, words):
    """Arch's pin: 'gemini' and an arbitrary string are each refused with nothing stored,
    even when the same request carries a key."""
    client.cookies.set("auth_token", _token())
    try:
        with patch.object(setup_routes, "AsyncSessionFactory") as factory:
            r = client.post(
                "/api/v1/setup/complete",
                json={"default_llm_provider": value, "anthropic_key": "not-a-real-key"},
            )
    finally:
        client.cookies.delete("auth_token")
    assert r.status_code == 422
    assert words in r.text
    factory.session_scope_fresh.assert_not_called()
    factory.session_scope.assert_not_called()
