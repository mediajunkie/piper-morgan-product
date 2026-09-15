"""#1814 — a signed-in BYOC user's OWN stored key must actually be used for a routed turn.

THE DEFECT. Provider SELECTION became principal-aware in #946/#1415:
``get_configured_providers(user_id)`` and ``get_default_provider(user_id)`` both take the
acting principal. Credential RESOLUTION never did — ``LLMConfigService.get_api_key(provider)``
read only the server's bare, unprefixed keychain slot and an env fallback, and the module
contained zero references to ``UserAPIKeyService``. That asymmetry was invisible while
``/setup/complete`` ALSO wrote the caller's key into the global slot as a side effect.
#1810 correctly removed that write ("the server key is not a real concept"), and with the
global slot empty the gate started returning ``[]`` for every user — including one whose
key was stored, and whose key the route had ALREADY resolved and bound for that very
request. ``_complete_raw`` raised ``RuntimeError("No LLM providers configured. Add an API
key in Settings.")`` and the floor rendered ``FLOOR_FALLBACK_NO_PROVIDER``. The gate refused
on behalf of a consumer (``_anthropic_complete`` → ``anthropic_client_for_request``) that
would have succeeded: the correctly-wired BYOC path sat one frame below the gate that never
looked at it.

LAYER (m-43). These are not ``LLMConfigService`` unit tests, and deliberately so — the
defect was not that the resolver returned a wrong value, it was that TWO layers disagreed
about whether a key existed. Proving the fix therefore requires both layers in one call
stack. So: the REAL ``/api/v1/intent`` route through a real ASGI ``TestClient``, a real
HS256 ``JWTService``, the real ``get_current_user_optional`` dependency, the real
``resolve_request_api_key`` → ``request_api_key(...)`` binding, and then — where the 1807
suite stops — a REAL ``LLMClient`` constructed INSIDE the request (as intent_service /
conversational_floor / semantic_boundary_detector all do lazily) running its REAL
availability gate and its REAL provider dispatch. The only stub below the route is
``anthropic.Anthropic`` itself, so no network call leaves the box; the key that reaches its
constructor is the observable, because that constructor argument IS what gets billed.

The failure assertion is likewise not a hand-copied string: it runs the production
``_classify_llm_error`` over the raised exception and compares against the production
``FLOOR_FALLBACK_NO_PROVIDER`` constant, which is what makes this test the pin for the
symptom the alpha tester actually saw rather than for a paraphrase of it.

DENOMINATOR. Five callers covered at the route, all post-#1810 (no global slot, no env
key anywhere): (1) signed-in with a STORED key — the defect, and the one the invite walks a
tester into; (2) signed-in with a BYOC HEADER key (#1162); (3) signed-in and KEYLESS —
must still be refused (#1807 no-regress), and must not be rescued by anything added here;
(4) fully anonymous — must still be refused (#1320 no-regress); (5) the cross-request
containment property: a key bound during one request must not survive into a
long-lived client for the next caller.
NOT covered here: a live billable Anthropic call (no real key in CI — the constructor
argument is the honest stopping point), the non-Anthropic providers (the per-request
ContextVar is Anthropic-only by construction — see ``REQUEST_KEY_PROVIDER``), and the
Slack/MCP entry points, which do not route through ``/intent``.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.config.llm_config_service import LLMConfigService
from services.infrastructure.keychain_service import KeychainService
from services.intent_service.conversational_floor import (
    FLOOR_FALLBACK_NO_PROVIDER,
    _classify_llm_error,
)
from services.llm import clients as clients_module
from services.llm.request_key import get_request_api_key
from web.api.routes.intent import router as intent_router

SECRET = "test-secret-1814-not-a-real-key"

STORED_USER_KEY = "sk-ant-api03-the-users-own-stored-key-1814"
HEADER_USER_KEY = "sk-ant-api03-the-users-own-header-key-1814"

# Every provider env var that could smuggle a server key into this test, neutralising it.
_PROVIDER_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "PERPLEXITY_API_KEY",
)


class _FakeAnthropicResponse:
    """Shape `_anthropic_complete` actually reads: `.content[0].text` and `.usage`."""

    content = [SimpleNamespace(text="Here's what I can help with.")]
    usage = SimpleNamespace(input_tokens=11, output_tokens=7)


class _RecordingAnthropic:
    """Stands in for `anthropic.Anthropic`. Records the api_key it was constructed with —
    the argument that decides WHOSE account the call is billed to — and never goes out."""

    constructed_with: list = []

    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        type(self).constructed_with.append(api_key)
        self.messages = SimpleNamespace(create=lambda **kw: _FakeAnthropicResponse())


@pytest.fixture(autouse=True)
def _post_1810_world(monkeypatch):
    """Post-#1810 reality: no global/server key ANYWHERE.

    The bare keychain slot is empty (that is exactly what #1810's removed write used to
    populate) and every provider env var is unset, so nothing but the caller's own key
    can possibly satisfy the gate. Without this the test could pass on a developer
    machine that happens to have a key and prove nothing.
    """
    for var in _PROVIDER_ENV_VARS:
        monkeypatch.delenv(var, raising=False)

    empty_keychain = Mock(spec=KeychainService)
    empty_keychain.get_api_key.return_value = None

    # The REAL LLMConfigService, through its existing injection seam — the class under
    # test is not replaced, only its credential store is emptied.
    monkeypatch.setattr(
        clients_module,
        "LLMConfigService",
        lambda *a, **kw: LLMConfigService(keychain_service=empty_keychain),
    )
    _RecordingAnthropic.constructed_with = []
    monkeypatch.setattr("anthropic.Anthropic", _RecordingAnthropic)
    yield


def _intent_result(message: str) -> SimpleNamespace:
    return SimpleNamespace(
        message=message,
        intent_data={},
        workflow_id=None,
        requires_clarification=False,
        clarification_type=None,
        suggestions=[],
        preferences={},
        error=None,
        error_type=None,
        async_work_started=False,
    )


class _FloorRoutedTurn:
    """Stands where IntentService stands and does what a floor-routed turn does: builds an
    LLMClient inside the request and calls `complete()`. Everything it exercises below that
    — the availability gate, provider selection, provider dispatch — is production code.

    On failure it reproduces the floor's own degradation (`_classify_llm_error` →
    `FLOOR_FALLBACK_NO_PROVIDER`), so the test observes the user-visible symptom, not just
    an exception type.
    """

    def __init__(self) -> None:
        self.calls = 0
        self.answer = None
        self.raised = None
        self.key_bound_at_llm_time = None

    async def process_intent(self, **kwargs):
        self.calls += 1
        self.key_bound_at_llm_time = get_request_api_key()
        client = clients_module.LLMClient()
        try:
            self.answer = await client.complete(
                task_type="reasoning",
                prompt="What can you do?",
                user_id=kwargs.get("user_id"),
            )
        except Exception as exc:
            self.raised = exc
            fallback = {
                "no_provider": FLOOR_FALLBACK_NO_PROVIDER,
            }.get(_classify_llm_error(exc), "transient")
            return _intent_result(fallback)
        return _intent_result(self.answer)


@contextlib.asynccontextmanager
async def _fake_session_scope():
    yield object()


@contextlib.contextmanager
def _stored_key(value):
    """Point the route's DB-backed stored-key fetcher at `value` without a database.
    Resolution, binding and refusal all still run for real."""
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            lambda *a, **k: _fake_session_scope(),
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            AsyncMock(return_value=value),
        ),
    ):
        yield


def _client() -> tuple[TestClient, JWTService, _FloorRoutedTurn]:
    app = FastAPI()
    app.include_router(intent_router)
    jwt_service = JWTService(secret_key=SECRET)
    turn = _FloorRoutedTurn()
    app.state.jwt_service = jwt_service
    app.state.intent_service = turn
    return TestClient(app, raise_server_exceptions=False), jwt_service, turn


def _token(jwt_service: JWTService) -> str:
    user_id = uuid.uuid4()
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


def _post(client: TestClient, headers: dict) -> dict:
    # session_id "default_session" deliberately skips the conversation auto-create block,
    # which is unrelated to key resolution and would need a real database.
    response = client.post(
        "/api/v1/intent",
        json={"message": "What can you do?", "session_id": "default_session"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()


class TestSignedInUsersOwnKeyIsActuallyUsed:
    """The #1814 property: a key we told the user to configure must reach the LLM call."""

    @pytest.mark.smoke
    def test_stored_per_user_key_is_used_for_a_floor_routed_turn(self):
        """THE red-first pin, and the exact path the alpha invite instructs a tester into.

        Pre-fix this raised `RuntimeError("No LLM providers configured. Add an API key in
        Settings.")` inside `_complete_raw` — before `_anthropic_complete` ran — and the
        floor rendered FLOOR_FALLBACK_NO_PROVIDER to a user whose key was sitting right
        there, resolved and bound.
        """
        client, jwt_service, turn = _client()
        token = _token(jwt_service)

        with _stored_key(STORED_USER_KEY):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert turn.calls == 1
        assert turn.key_bound_at_llm_time == STORED_USER_KEY, (
            "the route must bind the user's resolved key for the request — if this "
            "fails the defect is upstream of #1814, in #1807's resolution"
        )
        assert turn.raised is None, f"the routed turn still failed: {turn.raised!r}"
        assert body["message"] != FLOOR_FALLBACK_NO_PROVIDER, (
            "a signed-in user with their own stored key was told no provider is "
            "configured — this is #1814"
        )
        # The observable that matters: the call was billed to the USER'S key.
        assert _RecordingAnthropic.constructed_with == [STORED_USER_KEY]
        assert body["message"] == "Here's what I can help with."

    @pytest.mark.smoke
    def test_byoc_header_key_is_used_for_a_floor_routed_turn_1162(self):
        """#1162's Desktop path has the same gate above it, so it had the same wall."""
        client, jwt_service, turn = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(
                client,
                {"Authorization": f"Bearer {token}", "X-User-Api-Key": HEADER_USER_KEY},
            )

        assert turn.raised is None, f"the routed turn still failed: {turn.raised!r}"
        assert body["message"] != FLOOR_FALLBACK_NO_PROVIDER
        assert _RecordingAnthropic.constructed_with == [HEADER_USER_KEY]

    def test_the_gate_and_the_consumer_now_agree(self):
        """The root cause stated as a property, at the layer it lives on: for the same
        principal, in the same request, "is a provider available?" and "which key will
        the Anthropic call use?" must not contradict each other. Two layers disagreeing
        is what #1814 WAS; a value being wrong is not."""
        from services.llm.request_key import anthropic_client_for_request, request_api_key

        empty_keychain = Mock(spec=KeychainService)
        empty_keychain.get_api_key.return_value = None
        config = LLMConfigService(keychain_service=empty_keychain)
        user_id = str(uuid.uuid4())

        # No request bound: nothing is available and no key is invented. (Fix must not
        # manufacture a provider out of thin air.)
        assert config.get_api_key("anthropic") is None
        assert config.get_configured_providers(user_id) == []

        with request_api_key(STORED_USER_KEY):
            assert config.get_configured_providers(user_id) == ["anthropic"]
            assert config.get_default_provider(user_id) == "anthropic"
            assert config.get_api_key("anthropic") == STORED_USER_KEY
            # ...and the consumer resolves to a client keyed to the SAME credential.
            assert anthropic_client_for_request(None).api_key == STORED_USER_KEY

        # The binding does not outlive the request (ContextVar reset in `finally`).
        assert config.get_api_key("anthropic") is None
        assert config.get_configured_providers(user_id) == []


class TestNoServerOwnedKeyIsReintroduced:
    """#1807 / #1320 no-regress. #1814 makes the gate see MORE keys; the one thing it must
    never make it see is a key the product owns. Keyless still refuses, honestly."""

    @pytest.mark.smoke
    def test_signed_in_keyless_user_is_still_refused_and_never_reaches_the_llm(self):
        client, jwt_service, turn = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert body["error_type"] == "user_key_required"
        assert turn.calls == 0, "refusal must happen before IntentService/the LLM"
        assert _RecordingAnthropic.constructed_with == [], (
            "a keyless caller caused an Anthropic client to be constructed — something "
            "supplied a key that is not theirs"
        )
        msg = body["message"].lower()
        assert "llm key" in msg or "api key" in msg, body["message"]
        assert "sign in" not in msg, "they ARE signed in"
        assert (
            body["message"] != FLOOR_FALLBACK_NO_PROVIDER
        ), "the honest #1807 refusal must not degrade into the vaguer floor copy"

    def test_anonymous_caller_is_still_refused_1320(self):
        client, _, turn = _client()

        with _stored_key(None):
            body = _post(client, {})

        assert body["error_type"] == "anonymous_key_required"
        assert turn.calls == 0
        assert _RecordingAnthropic.constructed_with == []
        assert "sign in" in body["message"].lower()

    def test_server_singleton_client_never_captures_a_request_scoped_key(self):
        """Containment, and the reason `include_request_key=False` exists.

        `LLMClient()` is constructed lazily INSIDE a request in several services. If
        `_init_clients` read the request-scoped key, one user's credential would be baked
        into a long-lived object and spent by the NEXT caller — a cross-user credential
        leak introduced by the fix for a functionality bug. The per-request key must reach
        Anthropic only via `anthropic_client_for_request`, which builds a fresh client.
        """
        from services.llm.request_key import request_api_key

        with request_api_key(STORED_USER_KEY):
            client = clients_module.LLMClient()
            assert client.anthropic_client is None, (
                "the server's singleton Anthropic client captured a request-scoped user "
                "key — it would be reused for the next caller"
            )
            assert client.openai_client is None
            assert not client.gemini_client

        assert _RecordingAnthropic.constructed_with == [], (
            "_init_clients constructed an Anthropic client from a key the server does " "not own"
        )
