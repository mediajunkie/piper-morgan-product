"""#1872: the floor's LLM-error classifier doesn't recognize its own production
trigger string. `services/llm/clients.py`'s terminal "every provider failed"
path raised a bare `RuntimeError` whose only machine-readable content was its
rendered message — three distinct causes (zero providers attempted, a
configured provider's credential rejected, a transient connection failure)
all wrapped in ONE string that neither error classifier's substring checks
recognized correctly (`no_provider` keyed on "not configured"/"no llm
provider", neither of which appears in "All configured LLM providers failed.
Details: ..."), so every terminal LLM failure fell to "transient" ("try again
in a moment") in the conversational floor regardless of cause.

Fix, at the producer: `AllProvidersFailed(RuntimeError)` carries the real
per-provider `(provider, reason)` attempts, plus `.no_providers` (honest,
read from `attempts` — never inferred from text) and `.primary_reason` (the
first/primary provider's own failure text). `str(exc)` is kept BYTE-IDENTICAL
to the pre-#1872 message so every existing string-matching consumer (the web
route's degradation extractor, the translator's pattern table, every
pre-#1872 test) keeps working unchanged — pinned here directly against the
message-construction logic, and via the full `_complete_raw` integration path.

The FLOOR-side classification fix (delegating to the shared
`classify_llm_error_text` in `user_friendly_errors.py`, plus the Gemini
invalid-key pattern addition) is pinned in
`test_llm_error_classifier_agreement_1870.py`'s
`TestTypedExceptionResolvesStandoutFinding` — this file covers the PRODUCER
half only: the exception's own shape, and that the real `_complete_raw` call
path raises it with the correct attempts.

LAYER (m-43): the class-shape tests are pure-unit (no network, no LLM call);
the `_complete_raw` tests patch `_call_provider` only — real selection,
fallback-ordering, and consent-filtering logic runs. DENOMINATOR: the
exception's `__init__`/`no_providers`/`primary_reason` properties (3), one
real single-provider failure, one real two-provider (primary + fallback)
failure, and a byte-identical `str()` pin against the exact pre-#1872 format
string.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.llm.clients import AllProvidersFailed
from services.llm.request_key import request_api_key

# ---------------------------------------------------------------------------
# The exception's own shape — no client, no network.
# ---------------------------------------------------------------------------


class TestAllProvidersFailedShape:
    def test_str_is_byte_identical_to_pre_1872_format(self):
        """The producer's promise: consumers that string-match this exact
        message (the web route's `_extract_degradation_message`, the
        translator's `all configured llm providers failed` pattern, every
        pre-#1872 test) keep working unchanged."""
        exc = AllProvidersFailed(
            [("anthropic", "invalid x-api-key"), ("openai", "429 rate limited")]
        )
        assert str(exc) == (
            "All configured LLM providers failed. Details: "
            "anthropic: invalid x-api-key; openai: 429 rate limited"
        )

    def test_str_matches_the_original_single_provider_format(self):
        """The single-attempt case — the shape every existing
        `pytest.raises(RuntimeError, match="All configured LLM providers "
        "failed")` test already exercises."""
        exc = AllProvidersFailed([("openai", "Connection error.")])
        assert str(exc) == "All configured LLM providers failed. Details: openai: Connection error."

    def test_is_a_runtime_error(self):
        """Deliberately NOT `Exception`-only (the issue's own suggestion was
        illustrative, not prescriptive): every existing
        `pytest.raises(RuntimeError, ...)` call site (test_provider_selection
        _1415.py, test_serving_record_1676.py) must keep matching without
        modification."""
        assert isinstance(AllProvidersFailed([("openai", "boom")]), RuntimeError)

    def test_attempts_round_trips_exactly(self):
        attempts = [("anthropic", "reason one"), ("gemini", "reason two")]
        exc = AllProvidersFailed(attempts)
        assert exc.attempts == attempts

    def test_no_providers_true_only_when_attempts_empty(self):
        assert AllProvidersFailed([]).no_providers is True
        assert AllProvidersFailed([("openai", "x")]).no_providers is False

    def test_primary_reason_is_the_first_attempts_reason(self):
        exc = AllProvidersFailed([("anthropic", "first reason"), ("openai", "second reason")])
        assert exc.primary_reason == "first reason"

    def test_primary_reason_is_empty_string_when_no_providers(self):
        """Never raises, never None — an empty string is the honest 'nothing
        to classify' value a consumer can safely pass to a text classifier."""
        assert AllProvidersFailed([]).primary_reason == ""


# ---------------------------------------------------------------------------
# The real producer call path — `LLMClient._complete_raw`.
# ---------------------------------------------------------------------------


def _make_client(config_service):
    from services.llm.clients import LLMClient

    client = LLMClient.__new__(LLMClient)  # skip heavyweight __init__ (builds SDKs)
    client._config_service = config_service
    client._output_filter = None
    client.anthropic_client = object()
    client.openai_client = object()
    client.gemini_client = None
    return client


class _StubConfigService:
    """Single-user stub: one provider is primary, both anthropic+openai are
    authorized (mirrors test_provider_selection_1415.py's harness)."""

    def __init__(self, default_provider="anthropic", authorized=("anthropic", "openai")):
        self._default = default_provider
        self._authorized = list(authorized)

    def get_default_provider(self, user_id=None):
        return self._default

    def get_configured_providers(self, user_id=None):
        return self._authorized


@pytest.fixture(autouse=True)
def _byoc_spend_binding():
    """Same BYOC binding test_provider_selection_1415.py uses: `_is_provider_
    configured` (the fallback loop's gate) reads per-request entitlement —
    without a bound key for a provider, it's skipped as a fallback candidate
    regardless of `get_configured_providers`."""
    with request_api_key({"anthropic": "sk-ant-test", "openai": "sk-oai-test"}):
        yield


class TestComplateRawRaisesTypedException:
    @pytest.mark.asyncio
    async def test_single_provider_failure_carries_one_attempt(self):
        """Only anthropic authorized: primary fails, no fallback candidate —
        `AllProvidersFailed.attempts` has exactly the primary's own attempt,
        and `no_providers` is correctly False (one WAS attempted)."""
        cfg = _StubConfigService(default_provider="anthropic", authorized=["anthropic"])
        client = _make_client(cfg)

        async def fake_call(provider, *a, **k):
            raise RuntimeError("invalid x-api-key")

        with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
            with pytest.raises(AllProvidersFailed) as excinfo:
                await client._complete_raw("conversation", "hi", user_id="u1")

        exc = excinfo.value
        assert exc.attempts == [("anthropic", "invalid x-api-key")]
        assert exc.no_providers is False
        assert exc.primary_reason == "invalid x-api-key"
        assert (
            str(exc) == "All configured LLM providers failed. Details: anthropic: invalid x-api-key"
        )

    @pytest.mark.asyncio
    async def test_primary_plus_fallback_failure_carries_both_attempts_in_order(self):
        """anthropic primary fails, openai fallback also fails — `attempts`
        preserves ORDER (primary first) so `.primary_reason` is genuinely the
        FIRST provider's own reason, not an arbitrary one."""
        cfg = _StubConfigService(default_provider="anthropic", authorized=["anthropic", "openai"])
        client = _make_client(cfg)

        async def fake_call(provider, *a, **k):
            if provider.value == "anthropic":
                raise RuntimeError("Connection error.")
            raise RuntimeError("insufficient_quota: no credits")

        with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
            with pytest.raises(AllProvidersFailed) as excinfo:
                await client._complete_raw("conversation", "hi", user_id="u1")

        exc = excinfo.value
        assert exc.attempts == [
            ("anthropic", "Connection error."),
            ("openai", "insufficient_quota: no credits"),
        ]
        assert exc.primary_reason == "Connection error."
        assert str(exc) == (
            "All configured LLM providers failed. Details: "
            "anthropic: Connection error.; openai: insufficient_quota: no credits"
        )

    @pytest.mark.asyncio
    async def test_floor_classifies_the_real_raised_exception_correctly(self):
        """End-to-end from the real producer to the floor's classifier: the
        exact object `_complete_raw` raises, classified without any
        re-construction, lands in the honest bucket — not 'transient' for
        every cause (the pre-#1872 defect)."""
        from services.intent_service.conversational_floor import _classify_llm_error

        cfg = _StubConfigService(default_provider="anthropic", authorized=["anthropic"])
        client = _make_client(cfg)

        async def fake_call(provider, *a, **k):
            raise RuntimeError("invalid x-api-key")

        with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
            with pytest.raises(AllProvidersFailed) as excinfo:
                await client._complete_raw("conversation", "hi", user_id="u1")

        assert _classify_llm_error(excinfo.value) == "rejected_credential"
