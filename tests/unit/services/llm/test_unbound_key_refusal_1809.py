"""#1809 — an UNBOUND LLM call refuses instead of silently spending the server's key.

THE DEFECT (#1809, step 3 of the #1812 plan). #1807 closed the server-key fallback at the
RESOLVER, and wired the refusal into the two entry points that call it (`/api/v1/intent`,
the five `/api/v1/documents/*` routes). But the mechanism that actually spends the key is
`anthropic_client_for_request` in `_anthropic_complete`, and its ContextVar default meant
"unbound → use the server's configured client". So any path that reached the LLM without
binding — Slack inbound, a future route, a forgotten background job — silently billed the
operator, and nothing failed. Default-open.

PM RULED (2026-09-14, decisions.log ×2, #1812): the server key "is not a real concept and
we don't need to support it in any sense." So the default inverts: **unbound is an ERROR**
(`UnboundLLMKeyError`, an `LLMKeyRequiredError`), never a fallback. The ONE surviving
server-key path is #1807's designated-operator opt-in — expressed as an EXPLICIT `None`
binding produced by `resolve_request_api_key`'s operator rung (both gates held), and even
that binding is re-checked against gate 1 (`PIPER_OPERATOR_SERVER_KEY`) at the chokepoint.
That seam stays until #1812 step 5 removes it.

Red-first evidence (2026-09-18): `TestUnboundIsAnError` run against the pre-fix tree —
`anthropic_client_for_request(SERVER_CLIENT)` with nothing bound RETURNED the server's own
client object (the silent spend), so the `pytest.raises` assertions failed. Output pinned
in the session log (dev/2026/09/18/2026-09-18-1245-prog-code-log.md).

Layer: unit, at the exact function `LLMClient._anthropic_complete` calls — plus one test
driving the REAL `_complete_raw` to prove the refusal is not swallowed into "All
configured LLM providers failed" by the fallback loop's blanket handler.
"""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from services.infrastructure.keychain_service import KeychainService
from services.llm import clients as clients_module
from services.llm.request_key import (
    OPERATOR_SERVER_KEY_ENV,
    LLMKeyRequiredError,
    UnboundLLMKeyError,
    anthropic_client_for_request,
    get_request_api_key,
    request_api_key,
)

SERVER_CLIENT = SimpleNamespace(name="THE-SERVERS-OWN-ANTHROPIC-CLIENT")
USER_KEY = "sk-ant-api03-the-users-own-key-1809"


class _FakeAnthropicResponse:
    content = [SimpleNamespace(text="ok")]
    usage = SimpleNamespace(input_tokens=3, output_tokens=1)


class _RecordingAnthropic:
    """Stands in for `anthropic.Anthropic` at BOTH bind sites (module import in
    clients.py; late import in anthropic_client_for_request) — same discipline as
    the #1814/#1815 suites: an unobserved construction path is exactly the
    server-vs-request credential confusion this family of issues is about."""

    constructed_with: list = []

    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        type(self).constructed_with.append(api_key)
        self.messages = SimpleNamespace(create=lambda **kw: _FakeAnthropicResponse())


@pytest.fixture(autouse=True)
def _clean_world(monkeypatch):
    """No provider env keys, no operator opt-in, recording Anthropic constructor."""
    for var in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "PERPLEXITY_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.delenv(OPERATOR_SERVER_KEY_ENV, raising=False)
    _RecordingAnthropic.constructed_with = []
    monkeypatch.setattr("anthropic.Anthropic", _RecordingAnthropic)
    monkeypatch.setattr(clients_module, "Anthropic", _RecordingAnthropic)
    yield


class TestUnboundIsAnError:
    """The inversion itself: default-open becomes default-closed."""

    @pytest.mark.smoke
    def test_unbound_call_refuses_instead_of_spending_the_server_key(self):
        """THE red-first pin. Pre-fix this RETURNED `SERVER_CLIENT` — the silent
        spend #1809 names: no binding, no resolver, no refusal, operator billed."""
        with pytest.raises(UnboundLLMKeyError):
            anthropic_client_for_request(SERVER_CLIENT)

    def test_the_refusal_is_a_key_required_error(self):
        """Routes/boundaries catch the FAMILY (`LLMKeyRequiredError`) — the new
        member must be a member, or every existing honest-copy handler misses it."""
        with pytest.raises(LLMKeyRequiredError):
            anthropic_client_for_request(SERVER_CLIENT)

    def test_unbound_refuses_even_when_the_server_client_is_none(self):
        """A keyless server must refuse for the same reason a keyed one does —
        returning None here would surface as `RuntimeError: Anthropic client not
        initialized`, blaming server config for the caller's missing binding."""
        with pytest.raises(UnboundLLMKeyError):
            anthropic_client_for_request(None)

    def test_the_refusal_lands_on_the_honest_no_key_copy(self):
        """The #1812 step-2 prerequisite this work waited for: the raise must map to
        CXO's "no key configured" error-table entry (services/ui_messages/
        user_friendly_errors.py), not the generic fallback — converting a silent
        spend into a refusal is only honest if the refusal says the right thing."""
        from services.ui_messages.user_friendly_errors import UserFriendlyErrorService

        with pytest.raises(UnboundLLMKeyError) as exc_info:
            anthropic_client_for_request(SERVER_CLIENT)

        translated = UserFriendlyErrorService().make_user_friendly(exc_info.value)
        assert translated["category"] == "llm_key", translated
        assert "key of your own" in translated["message"]


class TestBoundKeyStillWorks:
    """#1162/#1185/#1814 no-regress: the inversion changes only the UNBOUND arm."""

    def test_bound_user_key_builds_a_fresh_client_keyed_to_it(self):
        with request_api_key(USER_KEY):
            client = anthropic_client_for_request(SERVER_CLIENT)
        assert client is not SERVER_CLIENT
        assert client.api_key == USER_KEY
        assert _RecordingAnthropic.constructed_with == [USER_KEY]

    def test_the_binding_does_not_outlive_the_request(self):
        """The no-residue property (reset-in-finally), stated in its inverted form:
        after the request, the context is not "server key" — it is REFUSAL."""
        with request_api_key(USER_KEY):
            assert get_request_api_key() == USER_KEY
        assert get_request_api_key() is None
        with pytest.raises(UnboundLLMKeyError):
            anthropic_client_for_request(SERVER_CLIENT)


class TestOperatorOptInSeamSurvives:
    """#1807's designated-operator path — the ONE server-key seam, until #1812 step 5.

    The operator rung of `resolve_request_api_key` (both gates held) returns None; the
    route binds that None EXPLICITLY. Explicit None is now distinguishable from unbound,
    and it re-checks gate 1 at the chokepoint — so code that binds None WITHOUT the
    operator opt-in (i.e. without having gone through the resolver's double gate,
    which checks gate 1 first) still refuses.
    """

    def test_explicit_none_with_opt_in_uses_the_server_client(self, monkeypatch):
        monkeypatch.setenv(OPERATOR_SERVER_KEY_ENV, "1")
        with request_api_key(None):
            assert anthropic_client_for_request(SERVER_CLIENT) is SERVER_CLIENT

    def test_explicit_none_without_opt_in_refuses(self):
        """Binding None cannot be used to smuggle the server key past #1807's gate 1:
        the resolver can only produce a None binding when `is_designated_operator`
        held, and that checker requires the env opt-in first. A bare
        `request_api_key(None)` from anywhere else refuses at the chokepoint."""
        with request_api_key(None):
            with pytest.raises(UnboundLLMKeyError):
                anthropic_client_for_request(SERVER_CLIENT)

    def test_opt_in_alone_does_not_authorize_an_unbound_call(self, monkeypatch):
        """Gate 1 without gate 2 is not authorization: an UNBOUND call refuses even
        with the env flag on, because unbound means `is_designated_operator` (gate 2)
        was never consulted — only the resolver's explicit None binding attests both
        gates were checked."""
        monkeypatch.setenv(OPERATOR_SERVER_KEY_ENV, "1")
        with pytest.raises(UnboundLLMKeyError):
            anthropic_client_for_request(SERVER_CLIENT)


class TestRefusalIsNotSwallowedByTheFallbackLoop:
    """`_complete_raw`'s blanket handlers must let the refusal OUT (#1815 Gap 2's
    principle at the call layer): pre-fix shape would have been `RuntimeError: All
    configured LLM providers failed` — a refusal relabeled as an outage, serving
    try-again copy for a condition retrying cannot fix."""

    @pytest.mark.asyncio
    async def test_unbound_complete_raises_the_refusal_not_all_providers_failed(self, monkeypatch):
        keychain = Mock(spec=KeychainService)
        # Server owns an Anthropic key: anthropic is configured + selected primary,
        # so the call genuinely reaches `_anthropic_complete` — where the chokepoint
        # refuses because NOTHING WAS BOUND. The server key existing is precisely
        # what made the old default spend it.
        keychain.get_api_key.side_effect = (
            lambda name, username=None, **kw: "sk-the-operators-anthropic-key"
            if name == "anthropic" and username is None
            else None
        )
        monkeypatch.setenv("PIPER_DEFAULT_PROVIDER", "anthropic")
        from services.config.llm_config_service import LLMConfigService

        monkeypatch.setattr(
            clients_module,
            "LLMConfigService",
            lambda *a, **kw: LLMConfigService(keychain_service=keychain),
        )

        llm = clients_module.LLMClient()
        assert llm.anthropic_client is not None, "precondition: server client exists"

        with pytest.raises(LLMKeyRequiredError):
            await llm.complete(task_type="conversation", prompt="hi")

        # The server's client object was constructed at init (request-blind, #1814) —
        # but no completion was ever created on it.
        assert _RecordingAnthropic.constructed_with == ["sk-the-operators-anthropic-key"]
