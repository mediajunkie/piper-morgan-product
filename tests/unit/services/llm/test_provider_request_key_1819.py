"""#1819 — the per-request key path is PER-PROVIDER, and every completion leg refuses unbound.

#1809 inverted the Anthropic chokepoint; this closes the remaining half of the class:
`_openai_complete` / `_gemini_complete` read the server's own long-lived clients with no
per-request path at all, so any user turn that provider selection routed there was billed
to a product-owned credential — the concept PM ruled out (#1812, decisions.log 2026-09-14
×2).

RED evidence (pre-fix tree, 2026-09-18 probe):
    nothing bound; _openai_complete returned: served-by-server-key
    server client was spent (silent spend): True
    nothing bound; _gemini_complete returned: served-by-server-gemini-config

Now: `request_spend_key(provider)` is the one spend decision every leg shares — bound key
for THAT provider → spend it (fresh per-request client, never stored on self, #1814);
anything else → ``UnboundLLMKeyError``. A key bound for one provider is never spendable
on another (#1815's constraint, enforced at the chokepoint).

#1812 step 5 (2026-09-21): the operator ``None``-binding arm this file used to pin is
DELETED with the seam (str-or-raise now); its staying-deleted contract lives in
test_operator_seam_retired_1812.py. The ``client.openai_client``-style attributes some
tests still set are DECOYS — production `LLMClient` no longer has server clients at all
(step 6 amputated `_init_clients`); the decoys pin that nothing resurrects an
attribute-read spend path without these assertions catching it.
"""

from unittest.mock import MagicMock, patch

import pytest

from services.llm.clients import LLMClient
from services.llm.config import LLMModel, LLMProvider
from services.llm.request_key import (
    UnboundLLMKeyError,
    get_request_api_key,
    request_api_key,
    request_spend_key,
)

USER_OPENAI_KEY = "sk-user-openai-TEST"
USER_ANTHROPIC_KEY = "sk-ant-user-TEST"


def _bare_client() -> LLMClient:
    """LLMClient without __init__ (no config-service construction). Tests that want a
    server-client DECOY set the attribute themselves — production has none (#1812)."""
    client = LLMClient.__new__(LLMClient)
    client._output_filter = None
    return client


def _openai_config() -> dict:
    return {
        "provider": LLMProvider.OPENAI,
        "model": list(LLMModel)[0],
        "max_tokens": 16,
        "temperature": 0.0,
    }


def _gemini_config() -> dict:
    return {
        "provider": LLMProvider.GEMINI,
        "model": list(LLMModel)[0],
        "max_tokens": 16,
        "temperature": 0.0,
    }


def _server_openai_client() -> MagicMock:
    server = MagicMock(name="THE-SERVERS-OWN-OPENAI-CLIENT")
    resp = MagicMock()
    resp.choices = [MagicMock(message=MagicMock(content="served"))]
    resp.usage = MagicMock(prompt_tokens=1, completion_tokens=1)
    server.chat.completions.create.return_value = resp
    return server


# ---------------------------------------------------------------------------
# request_spend_key — the shared chokepoint decision
# ---------------------------------------------------------------------------


class TestRequestSpendKey:
    def test_unbound_refuses_for_every_provider(self):
        for provider in ("anthropic", "openai", "gemini"):
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key(provider)

    def test_a_key_bound_for_one_provider_is_not_spendable_on_another(self):
        """#1815's constraint at the chokepoint: cross-provider spend never happens."""
        with request_api_key(USER_ANTHROPIC_KEY):  # str form → anthropic by construction
            assert request_spend_key("anthropic") == USER_ANTHROPIC_KEY
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key("openai")
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key("gemini")

    def test_mapping_binding_carries_each_provider_to_its_own_leg(self):
        with request_api_key({"anthropic": USER_ANTHROPIC_KEY, "openai": USER_OPENAI_KEY}):
            assert request_spend_key("anthropic") == USER_ANTHROPIC_KEY
            assert request_spend_key("openai") == USER_OPENAI_KEY
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key("gemini")

    def test_empty_mapping_binds_nothing_spendable(self):
        """'No usable keys' refuses at spend — it must never collapse into any
        authorized form; that conflation (unbound == server-key) was #1809's bug,
        and #1812 step 5 removed the operator form it could have collapsed into."""
        with request_api_key({}):
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key("anthropic")
            with pytest.raises(UnboundLLMKeyError):
                request_spend_key("openai")

    def test_mapping_binding_resets_after_the_block(self):
        with request_api_key({"openai": USER_OPENAI_KEY}):
            assert get_request_api_key("openai") == USER_OPENAI_KEY
        assert get_request_api_key("openai") is None
        with pytest.raises(UnboundLLMKeyError):
            request_spend_key("openai")


# ---------------------------------------------------------------------------
# _openai_complete — the OpenAI leg refuses unbound, spends the user's own key bound
# ---------------------------------------------------------------------------


class TestOpenAILegInversion:
    @pytest.mark.asyncio
    async def test_unbound_refuses_even_when_the_server_client_exists(self):
        """THE #1819 pin (red on the pre-fix tree: 'served-by-server-key', spent=True)."""
        client = _bare_client()
        server = _server_openai_client()
        client.openai_client = server

        with pytest.raises(UnboundLLMKeyError):
            await client._openai_complete(prompt="hi", config=_openai_config())
        assert not server.chat.completions.create.called, (
            "the server's own OpenAI client was spent on an unbound request — "
            "the exact silent spend #1819 closes"
        )

    @pytest.mark.asyncio
    async def test_bound_openai_key_builds_a_fresh_client_keyed_to_it(self):
        client = _bare_client()
        server = _server_openai_client()
        client.openai_client = server

        fresh = _server_openai_client()
        fresh.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="served-by-user-key"))
        ]
        with patch("services.llm.clients.OpenAI", return_value=fresh) as openai_cls:
            with request_api_key({"openai": USER_OPENAI_KEY}):
                out = await client._openai_complete(prompt="hi", config=_openai_config())

        assert out == "served-by-user-key"
        openai_cls.assert_called_once_with(api_key=USER_OPENAI_KEY)
        assert not server.chat.completions.create.called
        # containment (#1814): the fresh client is never stored on the singleton
        assert client.openai_client is server

    @pytest.mark.asyncio
    async def test_an_anthropic_binding_does_not_make_the_openai_leg_spend(self):
        client = _bare_client()
        server = _server_openai_client()
        client.openai_client = server

        with request_api_key(USER_ANTHROPIC_KEY):
            with pytest.raises(UnboundLLMKeyError):
                await client._openai_complete(prompt="hi", config=_openai_config())
        assert not server.chat.completions.create.called


# ---------------------------------------------------------------------------
# _gemini_complete — refuses unbound; refuses a bound key honestly (no per-request path)
# ---------------------------------------------------------------------------


class TestGeminiLegInversion:
    @pytest.mark.asyncio
    async def test_unbound_refuses_even_when_gemini_is_configured(self):
        """Red on the pre-fix tree: returned 'served-by-server-gemini-config'."""
        client = _bare_client()
        client.gemini_client = True
        with pytest.raises(UnboundLLMKeyError):
            await client._gemini_complete(prompt="hi", config=_gemini_config())

    @pytest.mark.asyncio
    async def test_a_bound_gemini_key_is_refused_not_spent_cross_request(self):
        """google.generativeai credentials are process-global (genai.configure): honoring
        a per-request Gemini key would risk serving request A under request B's key.
        The leg refuses HONESTLY instead of building unsafe plumbing (#1819)."""
        client = _bare_client()
        client.gemini_client = True
        with request_api_key({"gemini": "sk-gemini-user"}):
            with pytest.raises(UnboundLLMKeyError, match="no per-request client path"):
                await client._gemini_complete(prompt="hi", config=_gemini_config())


# ---------------------------------------------------------------------------
# availability gate + config-service step 0 agree with the chokepoints (#1814/#1815 shape)
# ---------------------------------------------------------------------------


class TestAvailabilityAgreesWithTheChokepoint:
    def test_bound_openai_key_makes_openai_available_on_this_request(self):
        client = _bare_client()
        assert client._is_provider_configured(LLMProvider.OPENAI) is False
        with request_api_key({"openai": USER_OPENAI_KEY}):
            assert client._is_provider_configured(LLMProvider.OPENAI) is True
        assert client._is_provider_configured(LLMProvider.OPENAI) is False

    def test_a_server_client_alone_is_no_longer_availability(self):
        """The inversion at the gate: unbound, the OpenAI leg would refuse — so a
        server client's mere existence must read unavailable, or the fallback loop
        is routed into a guaranteed refusal (the trap #1815's docstring named)."""
        client = _bare_client()
        client.openai_client = _server_openai_client()
        client.anthropic_client = object()
        client.gemini_client = True
        for provider in (LLMProvider.ANTHROPIC, LLMProvider.OPENAI, LLMProvider.GEMINI):
            assert client._is_provider_configured(provider) is False

    def test_a_bound_gemini_key_never_reads_available(self):
        """No per-request Gemini client path exists — reporting True would route the
        loop into the leg's honest refusal."""
        client = _bare_client()
        client.gemini_client = True
        with request_api_key({"gemini": "sk-gemini-user"}):
            assert client._is_provider_configured(LLMProvider.GEMINI) is False

    def test_config_service_step_0_serves_each_provider_its_own_bound_key(self):
        from services.config.llm_config_service import LLMConfigService

        svc = LLMConfigService()
        with request_api_key({"anthropic": USER_ANTHROPIC_KEY, "openai": USER_OPENAI_KEY}):
            assert svc.get_api_key("anthropic") == USER_ANTHROPIC_KEY
            assert svc.get_api_key("openai") == USER_OPENAI_KEY
            # and request-blind reads (the #1814 singleton constructor) still skip it
            assert svc.get_api_key("openai", include_request_key=False) != USER_OPENAI_KEY
