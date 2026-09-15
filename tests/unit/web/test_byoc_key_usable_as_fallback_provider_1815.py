"""#1815 Gap 1 — a BYOC user's own key must be usable as a FALLBACK provider, not only as primary.

THE DEFECT (the residual #1814 left behind). #1814 made credential RESOLUTION
request-aware: ``LLMConfigService.get_api_key`` gained a Priority 0 that reads the same
``request_key`` ContextVar ``anthropic_client_for_request`` reads, so the availability gate
and the Anthropic consumer stopped disagreeing about whether a key exists. That repaired the
**primary**-provider path.

The cross-provider fallback loop was not on that path. ``_complete_raw`` gates each candidate
on ``self._is_provider_configured(provider)``, which for Anthropic was literally
``self.anthropic_client is not None`` — the **server's** long-lived singleton, which #1810
correctly stopped populating on any deployment that owns no global key. So the same
"server-owned artifact as the proxy for *is this provider available*" shape survived one
frame lower down: a BYOC user's key satisfied the gate above ``_call_provider`` but could
never satisfy the gate inside the fallback loop. Their working key was skipped in silence and
they were handed the generic "having trouble, try again" copy.

WHY IT IS NOT HYPOTHETICAL. It needs only a second provider ahead of Anthropic in selection,
which is the DEFAULT: ``PIPER_DEFAULT_PROVIDER`` defaults to ``"openai"``
(``llm_config_service.py`` ``_load_selection_config``). A mixed instance — operator's OpenAI
key configured server-side, tester BYOCs their own Anthropic key — resolves primary=openai,
and the moment OpenAI has a bad minute the tester is told the system is broken while the key
we instructed them to configure sits one ``continue`` statement away.

LAYER (m-43). Route-driven, mirroring the #1814 suite, because the property is a
disagreement BETWEEN layers and cannot be observed inside either one: the real
``/api/v1/intent`` route, a real ``JWTService``, the real ``resolve_request_api_key`` →
``request_api_key(...)`` binding, a REAL ``LLMClient`` built inside the request, its REAL
availability gate, its REAL provider selection and its REAL fallback loop. The only things
stubbed are the two vendor SDK constructors, so nothing leaves the box — and the observable
is the ``api_key`` the Anthropic constructor receives, because that argument IS what decides
whose account is billed.

DENOMINATOR. Four properties over the fallback path, all in a post-#1810 world (no global
keychain slot, no provider env var):
  (1) primary=openai fails → Anthropic fallback runs on the USER'S key, and the answer is
      the user's, not the floor's degradation copy;
  (2) the gate and the consumer agree about Anthropic at the fallback frame, in both the
      bound and unbound directions (the root-cause property, stated directly);
  (3) providers with NO per-request path (OpenAI, Gemini) are NOT reported available off the
      back of a request key — an Anthropic key must never make OpenAI look callable;
  (4) no-regress containment (mirrors #1814's pin, in the world this change creates): the
      server singleton still never captures a request-scoped key, even now that the
      availability ANSWER for that same request is True.
NOT covered here: a live billable call to either vendor (the constructor argument is the
honest stopping point in CI); Gap 2 of #1815 (the #1415 consent fail-closed degradation),
which is a consent-semantics decision and is deliberately untouched by this file.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.infrastructure.keychain_service import KeychainService
from services.intent_service.conversational_floor import (
    FLOOR_FALLBACK_NO_PROVIDER,
    FLOOR_FALLBACK_TRANSIENT,
    _classify_llm_error,
)
from services.llm import clients as clients_module
from services.llm.config import LLMProvider
from services.llm.request_key import (
    anthropic_client_for_request,
    get_request_api_key,
    request_api_key,
)
from web.api.routes.intent import router as intent_router

SECRET = "test-secret-1815-not-a-real-key"

# The tester's own key — the one the alpha invite tells them to paste into Settings.
STORED_USER_KEY = "sk-ant-api03-the-users-own-stored-key-1815"
# The operator's OpenAI key. This is the ONLY server-owned credential in this world, and it
# is what makes openai the resolved PRIMARY provider — i.e. what puts Anthropic in the
# fallback position where #1815 Gap 1 lives.
SERVER_OPENAI_KEY = "sk-the-operators-own-openai-key-1815"

_PROVIDER_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY",
    "GEMINI_API_KEY",
    "PERPLEXITY_API_KEY",
)

# What the primary provider does in this scenario. Deliberately a plain upstream blip, not an
# auth error: `_classify_llm_error` must read it as "transient", so the pre-fix user-visible
# symptom is the generic try-again copy rather than anything that hints at credentials.
OPENAI_OUTAGE = "openai upstream returned 503 service_unavailable"


class _FakeAnthropicResponse:
    """The shape `_anthropic_complete` actually reads: `.content[0].text` and `.usage`."""

    content = [SimpleNamespace(text="Here's what I can help with.")]
    usage = SimpleNamespace(input_tokens=11, output_tokens=7)


class _RecordingAnthropic:
    """Stands in for `anthropic.Anthropic`, recording every api_key it is constructed with.

    Patched at BOTH names deliberately: `clients.py` binds `Anthropic` at module import
    (used by `_init_clients`, the singleton path) while `anthropic_client_for_request`
    late-imports `anthropic.Anthropic` (the per-request path). Recording only one of them
    would leave the other able to construct a real client unobserved, which is precisely
    the confusion between server-owned and request-owned credentials this issue is about.
    """

    constructed_with: list = []

    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        type(self).constructed_with.append(api_key)
        self.messages = SimpleNamespace(create=lambda **kw: _FakeAnthropicResponse())


class _FailingOpenAI:
    """The operator's OpenAI client, constructed fine and failing at CALL time.

    Failing at call time rather than construction time is the point: OpenAI must be
    genuinely *configured* (so it wins primary selection and the fallback loop is actually
    entered), and must then fail the way a real upstream does.
    """

    constructed_with: list = []

    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        type(self).constructed_with.append(api_key)

        def _create(**kw):
            raise RuntimeError(OPENAI_OUTAGE)

        self.chat = SimpleNamespace(completions=SimpleNamespace(create=_create))


def _mixed_instance_keychain() -> Mock:
    """A post-#1810 keychain holding the operator's OpenAI key and NOTHING else.

    Critically it also returns None for the #1415 selection slots
    (``default_llm_provider`` / ``authorized_llm_providers``, per-user and global), so
    provider selection runs its real legacy path — consent list absent means
    all-configured is authorized — and the default falls through to the env default. That
    keeps this test about the fallback GATE and not about consent configuration.
    """
    keychain = Mock(spec=KeychainService)

    def _get(name, username=None, **kwargs):
        if name == "openai" and username is None:
            return SERVER_OPENAI_KEY
        return None

    keychain.get_api_key.side_effect = _get
    return keychain


@pytest.fixture(autouse=True)
def _mixed_byoc_instance(monkeypatch):
    """The world: operator owns an OpenAI key; the tester owns an Anthropic key; the server
    owns no Anthropic key at all (that is what #1810 removed)."""
    for var in _PROVIDER_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    # Explicit rather than relying on the default, so this test states the condition it
    # depends on instead of inheriting it silently from the environment.
    monkeypatch.setenv("PIPER_DEFAULT_PROVIDER", "openai")

    keychain = _mixed_instance_keychain()
    monkeypatch.setattr(clients_module, "LLMConfigService", lambda *a, **kw: _real_config(keychain))

    _RecordingAnthropic.constructed_with = []
    _FailingOpenAI.constructed_with = []
    monkeypatch.setattr("anthropic.Anthropic", _RecordingAnthropic)
    monkeypatch.setattr(clients_module, "Anthropic", _RecordingAnthropic)
    monkeypatch.setattr(clients_module, "OpenAI", _FailingOpenAI)
    yield


def _real_config(keychain):
    """The REAL LLMConfigService through its existing injection seam — only the credential
    store is emptied, the class under test is never replaced."""
    from services.config.llm_config_service import LLMConfigService

    return LLMConfigService(keychain_service=keychain)


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
    LLMClient inside the request and calls `complete()`. Everything below that — the
    availability gate, provider selection, the fallback loop, provider dispatch — is
    production code. On failure it reproduces the floor's own degradation so the test
    observes the user-visible symptom rather than an exception type."""

    def __init__(self) -> None:
        self.calls = 0
        self.answer = None
        self.raised = None
        self.key_bound_at_llm_time = None
        self.served: dict = {}

    async def process_intent(self, **kwargs):
        self.calls += 1
        self.key_bound_at_llm_time = get_request_api_key()
        client = clients_module.LLMClient()
        try:
            self.answer = await client.complete(
                task_type="reasoning",
                prompt="What can you do?",
                user_id=kwargs.get("user_id"),
                served=self.served,
            )
        except Exception as exc:
            self.raised = exc
            fallback = {
                "no_provider": FLOOR_FALLBACK_NO_PROVIDER,
                "transient": FLOOR_FALLBACK_TRANSIENT,
            }.get(_classify_llm_error(exc), FLOOR_FALLBACK_TRANSIENT)
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


class TestByocKeyIsUsableAsAFallbackProvider:
    """#1815 Gap 1: availability at the fallback frame must mean "this REQUEST can call it"."""

    @pytest.mark.smoke
    def test_primary_provider_failure_falls_back_to_the_users_own_anthropic_key(self):
        """THE red-first pin.

        Pre-fix: the fallback loop hit ``_is_provider_configured(ANTHROPIC)``, read the
        server's ``anthropic_client`` (``None`` post-#1810), skipped the one provider that
        could actually have served this request, and raised ``RuntimeError("All configured
        LLM providers failed...")`` — which the floor renders as the generic transient
        copy. The user's own working key was never consulted and no Anthropic client was
        ever constructed.
        """
        client, jwt_service, turn = _client()
        token = _token(jwt_service)

        with _stored_key(STORED_USER_KEY):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert turn.calls == 1
        assert turn.key_bound_at_llm_time == STORED_USER_KEY, (
            "the route must bind the user's resolved key for the request — if this fails "
            "the defect is upstream of #1815, in #1807's resolution or #1814's gate"
        )
        # The primary really did run and really did fail — otherwise this test would pass
        # without ever entering the fallback loop it exists to cover.
        assert _FailingOpenAI.constructed_with == [SERVER_OPENAI_KEY]

        assert turn.raised is None, (
            f"the routed turn failed instead of falling back: {turn.raised!r} — the "
            "fallback loop skipped Anthropic despite a usable per-request key (#1815 Gap 1)"
        )
        assert body["message"] != FLOOR_FALLBACK_TRANSIENT, (
            "a BYOC user with a working key was told the system is having trouble, because "
            "the fallback gate asked whether the SERVER could call Anthropic (#1815 Gap 1)"
        )
        assert body["message"] != FLOOR_FALLBACK_NO_PROVIDER
        assert body["message"] == "Here's what I can help with."

        # The observable that matters: the fallback call was billed to the USER'S key,
        # and to exactly one client built for this request.
        assert _RecordingAnthropic.constructed_with == [STORED_USER_KEY]
        # #1676/#1620: a cross-provider fallback changes the serving provider — it must say so.
        assert turn.served.get("provider") == "anthropic"

    def test_the_fallback_gate_and_the_anthropic_consumer_agree(self):
        """The root cause stated as a property, at the frame it lives on.

        ``_is_provider_configured`` is the fallback loop's gate; ``anthropic_client_for_
        request`` is what ``_anthropic_complete`` actually calls. For the same request
        these two must never contradict each other — two layers disagreeing about whether
        a credential exists is what #1814 WAS, and the fallback loop is where it survived.
        """
        llm = clients_module.LLMClient()

        # No request bound: the server owns no Anthropic key, so Anthropic is genuinely
        # unavailable and nothing is invented.
        assert llm._is_provider_configured(LLMProvider.ANTHROPIC) is False
        assert anthropic_client_for_request(llm.anthropic_client) is None

        with request_api_key(STORED_USER_KEY):
            assert llm._is_provider_configured(LLMProvider.ANTHROPIC) is True
            consumer_client = anthropic_client_for_request(llm.anthropic_client)
            assert consumer_client is not None
            assert consumer_client.api_key == STORED_USER_KEY

        # And the agreement holds in the other direction too: the binding does not outlive
        # the request, so neither does the availability answer.
        assert llm._is_provider_configured(LLMProvider.ANTHROPIC) is False
        assert anthropic_client_for_request(llm.anthropic_client) is None

    def test_a_request_key_never_makes_a_provider_without_a_per_request_path_look_available(
        self,
    ):
        """The constraint #1815 states explicitly, pinned so a later refactor cannot lose it.

        The per-request key is an ANTHROPIC key by construction (``REQUEST_KEY_PROVIDER``),
        and ``_anthropic_complete`` is its only consumer. OpenAI and Gemini have no
        per-request path at all: ``_openai_complete`` and ``_gemini_complete`` read the
        server's client/flag and nothing else. Reporting them available off the back of a
        request key would send the fallback loop into a provider that is guaranteed to
        raise — trading a silent skip for a guaranteed failure, which is not a fix.
        """
        llm = clients_module.LLMClient()
        # Gemini is unconfigured server-side in this world; OpenAI IS configured, so its
        # answer must be True for the server's OWN reason and not because of the user key.
        assert llm.gemini_client in (None, False)

        with request_api_key(STORED_USER_KEY):
            assert llm._is_provider_configured(LLMProvider.GEMINI) is False, (
                "an Anthropic request key made Gemini look callable — `_gemini_complete` "
                "has no per-request path and would raise"
            )
            assert llm._is_provider_configured(LLMProvider.OPENAI) is True
            assert llm.openai_client is not None, (
                "OpenAI must read True because the SERVER holds an OpenAI key, not because "
                "a request bound an Anthropic one"
            )


class TestNoServerOwnedKeyIsReintroduced:
    """#1807 / #1320 / #1814 no-regress, in the world this change creates.

    #1815 makes the fallback gate answer True for a request-scoped key. The one thing that
    must NOT follow is the singleton learning that key — this is the containment property
    #1814 guarded with ``include_request_key=False``, re-asserted at the point where the
    availability ANSWER has now flipped to True.
    """

    def test_server_singleton_never_captures_a_request_scoped_key_even_when_available(self):
        """Mirrors ``test_server_singleton_client_never_captures_a_request_scoped_key``
        (#1814), with the assertion that actually distinguishes the two fixes: availability
        is True *and* the singleton is still empty. If a future change satisfies the gate by
        populating ``self.anthropic_client`` from the ContextVar, this fails — and that
        change would spend one user's key on the NEXT caller, because ``LLMClient()`` is
        constructed lazily inside requests in several services and then reused.
        """
        with request_api_key(STORED_USER_KEY):
            llm = clients_module.LLMClient()

            assert (
                llm._is_provider_configured(LLMProvider.ANTHROPIC) is True
            ), "precondition: this test is only meaningful while the gate says available"
            assert llm.anthropic_client is None, (
                "the server's singleton Anthropic client captured a request-scoped user "
                "key — it would be reused for the next caller"
            )
            assert _RecordingAnthropic.constructed_with == [], (
                "_init_clients constructed an Anthropic client from a key the server does "
                "not own"
            )

        # A client constructed with a key bound is still clean once the request ends.
        assert llm.anthropic_client is None
        assert llm._is_provider_configured(LLMProvider.ANTHROPIC) is False

    def test_a_keyless_caller_gets_no_anthropic_fallback_from_anywhere(self):
        """The refusal boundary #1807/#1320 draw must not be softened by this change: with
        no request key bound there is no Anthropic availability to be had, so a keyless
        caller cannot be rescued into the operator's balance by the fallback loop either."""
        llm = clients_module.LLMClient()

        assert get_request_api_key() is None
        assert llm._is_provider_configured(LLMProvider.ANTHROPIC) is False
        assert llm.anthropic_client is None
        assert _RecordingAnthropic.constructed_with == []
