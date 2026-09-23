"""#1718 — key-validation reasons are coarse.

`services/config/llm_config_service.py::validate_api_key()` computed a specific
`ValidationResult` (`_validate_anthropic`/`_validate_openai` distinguish a rejected
credential (401/403, AUTH_ERROR) from a valid-but-rejected key, e.g. no credits/billing
(VALIDATION_ERROR)) and then collapsed it to a bare bool — discarding the cause before
it reached `services/security/user_api_key_service.py::store_user_key`/`validate_user_key`
or any route above them.

Fix: `validate_api_key_detailed()` returns the full `ValidationResult`;
`humanize_validation_result()` routes it through the SAME translator the runtime chat
path already uses (`services/ui_messages/user_friendly_errors.py`), so a save-time
no-credits failure gets the identical honest sentence a runtime chat failure already
gets. `validate_api_key()` stays a thin bool wrapper — no existing bool-consuming
caller changes behavior.

LAYER (m-43): pure-unit on the provider HTTP call (httpx mocked, no network) through
`validate_api_key_detailed()` and `humanize_validation_result()`, plus the
`validate_api_key()` back-compat wrapper. DENOMINATOR: both providers named in the
issue (openai, anthropic) x three outcomes (200 valid / 401 rejected-credential /
credits-exhausted body), using each provider's REAL error-envelope shape (verified
against dev/active/probes/probe_b_gpt_2026-08-30.json for OpenAI's
`insufficient_quota`/`credit_balance_exhausted` shape, and the Anthropic API's
documented `authentication_error` / "credit balance is too low" shapes).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.config.llm_config_service import (
    LLMConfigService,
    ValidationResult,
    humanize_validation_result,
)

INVALID_KEY_SENTENCE = "The language-model API key on your account isn't valid."
QUOTA_SENTENCE = (
    "I can't reach a language model — the API key on your account is out of "
    "quota (or its billing needs attention)."
)


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
# (a) service level: each provider x {401 rejected-credential, 400 no-credits,
#     200 valid} using the provider's REAL error-envelope shape.
# ---------------------------------------------------------------------------


class TestOpenAIValidationDetailed:
    @pytest.mark.asyncio
    async def test_200_is_valid(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="get")):
            result = await service.validate_api_key_detailed("openai", "sk-real-key")
        assert result.is_valid is True
        assert humanize_validation_result(result) == ""

    @pytest.mark.asyncio
    async def test_401_rejected_credential_yields_invalid_key_sentence(self, service):
        body = (
            '{"error": {"message": "Incorrect API key provided", '
            '"type": "invalid_request_error", "param": null, "code": "invalid_api_key"}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(401, text=body, reason_phrase="Unauthorized", method="get"),
        ):
            result = await service.validate_api_key_detailed("openai", "sk-bad")
        assert result.is_valid is False
        assert result.error_code == "AUTH_ERROR"
        assert humanize_validation_result(result) == INVALID_KEY_SENTENCE

    @pytest.mark.asyncio
    async def test_429_no_credits_body_yields_quota_sentence(self, service):
        """#1718's real trigger, OpenAI shape (dev/active/probes/probe_b_gpt_2026-08-30.json):
        insufficient_quota/credit_balance_exhausted arrives as HTTP 429, NOT 401 — this
        was previously mislabeled AUTH_ERROR (any non-200 was AUTH_ERROR for OpenAI)."""
        body = (
            "{'error': {'message': 'You have no credits remaining. Add credits to "
            "continue using the API at https://platform.openai.com/settings/organization/"
            "billing/.', 'type': 'insufficient_quota', 'param': None, "
            "'code': 'credit_balance_exhausted'}}"
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(429, text=body, reason_phrase="Too Many Requests", method="get"),
        ):
            result = await service.validate_api_key_detailed("openai", "sk-no-credit")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"
        assert humanize_validation_result(result) == QUOTA_SENTENCE

    @pytest.mark.asyncio
    async def test_400_no_credits_body_also_yields_quota_sentence(self, service):
        """Per the task's stubbed-400 shape (issue's own framing) — also correctly
        bucketed even though 400 isn't AUTH_ERROR (401/403 only) nor is it the real
        429 status observed live: any non-200/401/403 goes through VALIDATION_ERROR."""
        body = '{"error": {"message": "quota exceeded", "type": "insufficient_quota"}}'
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(400, text=body, reason_phrase="Bad Request", method="get"),
        ):
            result = await service.validate_api_key_detailed("openai", "sk-no-credit-400")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"
        assert humanize_validation_result(result) == QUOTA_SENTENCE


class TestAnthropicValidationDetailed:
    @pytest.mark.asyncio
    async def test_200_is_valid(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="post")):
            result = await service.validate_api_key_detailed("anthropic", "sk-ant-real")
        assert result.is_valid is True
        assert humanize_validation_result(result) == ""

    @pytest.mark.asyncio
    async def test_401_rejected_credential_yields_invalid_key_sentence(self, service):
        body = (
            '{"type":"error","error":{"type":"authentication_error","message":"invalid x-api-key"}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(401, text=body, method="post"),
        ):
            result = await service.validate_api_key_detailed("anthropic", "sk-ant-bad")
        assert result.is_valid is False
        assert result.error_code == "AUTH_ERROR"
        assert humanize_validation_result(result) == INVALID_KEY_SENTENCE

    @pytest.mark.asyncio
    async def test_400_no_credits_body_yields_quota_sentence(self, service):
        """The issue's own real-world trigger: a valid, correctly-formatted key
        hitting a $0-credit account — Anthropic's real phrasing ('credit balance
        is too low'), not OpenAI's 'insufficient_quota' token."""
        body = (
            '{"type":"error","error":{"type":"invalid_request_error","message":'
            '"Your credit balance is too low to access the Claude API. Please go to '
            'Plans \\u0026 Billing to upgrade or purchase credits."}}'
        )
        with patch(
            "httpx.AsyncClient",
            _mock_async_client(400, text=body, reason_phrase="Bad Request", method="post"),
        ):
            result = await service.validate_api_key_detailed("anthropic", "sk-ant-no-credit")
        assert result.is_valid is False
        assert result.error_code == "VALIDATION_ERROR"
        assert humanize_validation_result(result) == QUOTA_SENTENCE


# ---------------------------------------------------------------------------
# validate_api_key() back-compat: bool-only callers see no behavior change.
# ---------------------------------------------------------------------------


class TestValidateApiKeyBackCompat:
    @pytest.mark.asyncio
    async def test_valid_key_returns_true(self, service):
        with patch("httpx.AsyncClient", _mock_async_client(200, method="get")):
            assert await service.validate_api_key("openai", "sk-real-key") is True

    @pytest.mark.asyncio
    async def test_invalid_key_returns_false(self, service):
        with patch(
            "httpx.AsyncClient", _mock_async_client(401, reason_phrase="Unauthorized", method="get")
        ):
            assert await service.validate_api_key("openai", "sk-bad") is False

    @pytest.mark.asyncio
    async def test_unknown_provider_returns_false(self, service):
        assert await service.validate_api_key("not-a-real-provider", "x") is False


# ---------------------------------------------------------------------------
# humanize_validation_result: never invents copy for causes it can't classify.
# ---------------------------------------------------------------------------


class TestHumanizeValidationResultFallback:
    def test_network_error_passes_through_raw_message(self):
        result = ValidationResult(
            provider="anthropic",
            is_valid=False,
            error_code="NETWORK_ERROR",
            error_message="Network error: Connection timeout",
        )
        assert humanize_validation_result(result) == "Network error: Connection timeout"

    def test_unrecognized_validation_error_passes_through_raw_message(self):
        result = ValidationResult(
            provider="anthropic",
            is_valid=False,
            error_code="VALIDATION_ERROR",
            error_message="Validation failed: 500 Internal Server Error",
        )
        assert humanize_validation_result(result) == "Validation failed: 500 Internal Server Error"

    def test_valid_result_returns_empty_string(self):
        result = ValidationResult(provider="anthropic", is_valid=True)
        assert humanize_validation_result(result) == ""
