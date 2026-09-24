"""#1870 (follow-up 1 of 3 from #1718) — gemini/perplexity validators treated
ANY non-2xx as AUTH_ERROR, unlike the #1718 fix already applied to
`_validate_openai`/`_validate_anthropic`. Same fix here: 401/403 -> AUTH_ERROR,
everything else -> VALIDATION_ERROR, with the provider's response body included
via `_safe_response_body` (previously neither branch attached a body at all for
these two providers).

LAYER (m-43): pure-unit on the provider HTTP call (httpx mocked, no network)
through `validate_api_key_detailed()`. DENOMINATOR: both providers named in the
issue (gemini, perplexity) x the outcomes each has REAL, evidence-backed
envelopes for.

Envelope provenance — LIVE-VERIFIED 2026-09-24 (not documentation, not
invented; direct unauthenticated `curl` against the real endpoints this
service calls):

  - Gemini (`generativelanguage.googleapis.com/v1/models`, GET, key as query
    param): a malformed/fake key returns HTTP 400 with
    `{"error":{"code":400,"message":"API key not valid. Please pass a valid
    API key.","status":"INVALID_ARGUMENT","details":[{"reason":
    "API_KEY_INVALID", ...}]}}` — NOT 401/403. A request with NO key at all
    returns HTTP 403 `{"error":{"code":403,"message":"Method doesn't allow
    unregistered callers (callers without established identity)....",
    "status":"PERMISSION_DENIED"}}`.
  - Perplexity (`api.perplexity.ai/chat/completions`, POST): a malformed/fake
    key returns HTTP 401 `{"error":{"message":"Invalid API key provided. You
    can find your API key at https://console.perplexity.ai.",
    "type":"invalid_api_key","code":401}}`.

No real quota/billing-exhausted envelope was found or reproducible for either
provider without spending real money on a depleted-credit account:
  - Gemini's only documented 429 `quota_exceeded`/`rate_limit_exceeded` shape
    (ai.google.dev/gemini-api/docs/api-errors, fetched 2026-09-24) is
    EXPLICITLY scoped to the newer "Interactions API" surface, not the classic
    `v1/models` endpoint this service calls — reusing it here would be
    conflating two different API surfaces' error envelopes, not evidence.
  - Perplexity's docs have no documented quota/credit-exhaustion shape; a
    Perplexity community-forum report (not verified here) suggests an
    out-of-credits account may ALSO return 401 (the same status as a bad key)
    rather than a distinct status — see the code comment on
    `_validate_perplexity`'s AUTH_ERROR branch for the full caveat.
Per the task's own instruction ("if you can't find a real quota envelope...
test 401 + a generic 400 only — don't invent a provider's JSON"): this file
tests the live-verified 401/403/400 cases plus one generic/unparseable 5xx for
the VALIDATION_ERROR fallback bucket. No quota-shaped body is fabricated.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.config.llm_config_service import LLMConfigService, humanize_validation_result

INVALID_KEY_SENTENCE = "The language-model API key on your account isn't valid."


def _mock_async_client(status_code, text="", reason_phrase="", method="get", raise_exc=None):
    """An httpx.AsyncClient() replacement — no network hit. `text`/`reason_phrase`
    are real strings (not MagicMocks) since the service code slices/reads them."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.reason_phrase = reason_phrase

    client = MagicMock()
    call = AsyncMock(side_effect=raise_exc) if raise_exc else AsyncMock(return_value=resp)
    setattr(client, method, call)

    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=None)
    return MagicMock(return_value=cm)


@pytest.fixture
def service():
    with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
        mock_keychain_class.return_value.get_api_key.return_value = None
        return LLMConfigService()


# ---------------------------------------------------------------------------
# Gemini — live-verified envelopes (2026-09-24)
# ---------------------------------------------------------------------------


class TestGeminiValidationDetailed:
    @pytest.mark.asyncio
    async def test_200_is_valid(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="get")):
            result = await service.validate_api_key_detailed("gemini", "AIza-real")
        assert result.is_valid is True
        assert humanize_validation_result(result) == ""

    @pytest.mark.asyncio
    async def test_403_no_key_at_all_yields_auth_error(self, service):
        """Live-verified: an unkeyed request (Gemini treats a missing key as
        'unregistered caller') returns 403 PERMISSION_DENIED — a genuinely
        rejected-credential-shaped case, correctly AUTH_ERROR under the #1718
        pattern (401/403 -> AUTH_ERROR)."""
        body = (
            '{"error":{"code":403,"message":"Method doesn\'t allow unregistered '
            "callers (callers without established identity). Please use API Key "
            'or other form of API consumer identity to call this API.",'
            '"status":"PERMISSION_DENIED"}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(403, text=body, reason_phrase="Forbidden", method="get"),
        ):
            result = await service.validate_api_key_detailed("gemini", "")
        assert result.is_valid is False
        assert result.error_code == "AUTH_ERROR"
        assert "PERMISSION_DENIED" in result.error_message
        assert "403" in result.error_message

    @pytest.mark.asyncio
    async def test_400_malformed_key_is_validation_error_not_auth(self, service):
        """Live-verified: Gemini's REAL invalid-key response is 400
        INVALID_ARGUMENT/API_KEY_INVALID, NOT 401/403 — unlike OpenAI/
        Anthropic. Per the #1718 pattern (401/403 ONLY -> AUTH_ERROR), this
        correctly buckets VALIDATION_ERROR now (pre-#1870 it was mislabeled
        AUTH_ERROR, since the old code treated 400 as auth too). The real
        cause still reaches the caller via the body text.

        NOTE (discovered, reported not fixed — #1870 scope is the AUTH_ERROR/
        VALIDATION_ERROR split, not the translator's regex coverage): neither
        `humanize_validation_result()` nor `user_friendly_errors.py` currently
        recognizes Gemini's actual wording ("API key not valid" / "API_KEY_
        INVALID") — none of the translator's invalid-key patterns
        (`invalid_api_key|incorrect api key|invalid.*x-api-key|
        authentication_error|invalid api key provided`) match it. This means
        Gemini save-time failures fall through to the RAW error_message
        (still an improvement over pre-#1870, which had no body at all) rather
        than the humanized "isn't valid" sentence other providers get.
        """
        body = (
            '{"error":{"code":400,"message":"API key not valid. Please pass a '
            'valid API key.","status":"INVALID_ARGUMENT","details":[{"@type":'
            '"type.googleapis.com/google.rpc.ErrorInfo","reason":'
            '"API_KEY_INVALID","domain":"googleapis.com"}]}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(400, text=body, reason_phrase="Bad Request", method="get"),
        ):
            result = await service.validate_api_key_detailed("gemini", "AIza-fake")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"
        assert "API_KEY_INVALID" in result.error_message
        # Confirmed gap, not silently masked: raw message passes through.
        assert humanize_validation_result(result) != INVALID_KEY_SENTENCE
        assert "API key not valid" in humanize_validation_result(result)

    @pytest.mark.asyncio
    async def test_generic_5xx_is_validation_error(self, service):
        """Generic non-parseable failure — the fallback VALIDATION_ERROR
        bucket, no quota-specific body fabricated."""
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(503, text="", reason_phrase="Service Unavailable", method="get"),
        ):
            result = await service.validate_api_key_detailed("gemini", "AIza-real")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"


# ---------------------------------------------------------------------------
# Perplexity — live-verified envelopes (2026-09-24)
# ---------------------------------------------------------------------------


class TestPerplexityValidationDetailed:
    @pytest.mark.asyncio
    async def test_200_is_valid(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="post")):
            result = await service.validate_api_key_detailed("perplexity", "pplx-real")
        assert result.is_valid is True
        assert humanize_validation_result(result) == ""

    @pytest.mark.asyncio
    async def test_401_rejected_credential_yields_invalid_key_sentence(self, service):
        """Live-verified: a malformed key returns 401 with
        `"type":"invalid_api_key"` — that substring already matches the
        runtime translator's invalid-key pattern, so this provider (unlike
        Gemini) gets the fully humanized sentence."""
        body = (
            '{"error":{"message":"Invalid API key provided. You can find your '
            'API key at https://console.perplexity.ai.","type":"invalid_api_key",'
            '"code":401}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(401, text=body, reason_phrase="Unauthorized", method="post"),
        ):
            result = await service.validate_api_key_detailed("perplexity", "pplx-bad")
        assert result.is_valid is False
        assert result.error_code == "AUTH_ERROR"
        assert humanize_validation_result(result) == INVALID_KEY_SENTENCE

    @pytest.mark.asyncio
    async def test_generic_400_is_validation_error(self, service):
        """The task's own fallback shape when no quota envelope is available:
        a generic 4xx that isn't 401/403 -> VALIDATION_ERROR, no quota body
        fabricated. (Per-#1870-comment caveat: Perplexity is reported by its
        community forum to ALSO return 401 — not this bucket — for an
        out-of-credits account; not independently verified, not fixed here.)"""
        body = '{"error":{"message":"Bad request","type":"invalid_request_error"}}'
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(400, text=body, reason_phrase="Bad Request", method="post"),
        ):
            result = await service.validate_api_key_detailed("perplexity", "pplx-real")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"
        assert "invalid_request_error" in result.error_message


# ---------------------------------------------------------------------------
# validate_api_key() back-compat: bool-only callers see no behavior change.
# ---------------------------------------------------------------------------


class TestValidateApiKeyBackCompatGeminiPerplexity:
    @pytest.mark.asyncio
    async def test_gemini_valid_key_returns_true(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="get")):
            assert await service.validate_api_key("gemini", "AIza-real") is True

    @pytest.mark.asyncio
    async def test_gemini_invalid_key_returns_false(self, service):
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(400, text="", reason_phrase="Bad Request", method="get"),
        ):
            assert await service.validate_api_key("gemini", "AIza-fake") is False

    @pytest.mark.asyncio
    async def test_perplexity_valid_key_returns_true(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="post")):
            assert await service.validate_api_key("perplexity", "pplx-real") is True

    @pytest.mark.asyncio
    async def test_perplexity_invalid_key_returns_false(self, service):
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(401, text="", reason_phrase="Unauthorized", method="post"),
        ):
            assert await service.validate_api_key("perplexity", "pplx-bad") is False
