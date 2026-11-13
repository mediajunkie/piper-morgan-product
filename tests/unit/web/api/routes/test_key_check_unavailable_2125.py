"""#2125, Arch's ruling (2026-10-22): a timeout, a network fault or a bug of ours during
the key check is not a verdict on the key. The validator carries its own code, the key is
left unjudged, one fixed line reaches the page, and the cause stays in the log. The same
fault on /setup/complete and keychain-check renders no exception text. The encryptor is
probed at startup and /health reads the credential store."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.config import llm_config_service as llm_mod
from services.config.llm_config_service import (
    KEY_CHECK_UNAVAILABLE,
    KEY_CHECK_UNAVAILABLE_MESSAGE,
    KeyCheckUnavailable,
    LLMConfigService,
    ValidationResult,
    humanize_validation_result,
)
from services.security.field_encryption import FieldEncryptionService, KeyStoreConfigError
from services.security.user_api_key_service import UserAPIKeyService
from web.api.routes.setup import (
    KEY_CHECK_COULD_NOT_RUN_MESSAGE,
    SERVER_CANNOT_STORE_KEYS_MESSAGE,
    SETUP_COULD_NOT_FINISH_MESSAGE,
    ApiKeyValidateRequest,
    check_keychain,
    validate_api_key,
)

STAGING_ERROR = "master_key must be 32 bytes (AES-256); got 48 bytes"


def _scope():
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=MagicMock())
    scope.__aexit__ = AsyncMock(return_value=False)
    return scope


# --- the validator -------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_validator_fault_is_the_unavailable_code_not_a_verdict():
    svc = LLMConfigService(keychain_service=MagicMock())
    with patch.object(
        LLMConfigService, "_validate_anthropic", new=AsyncMock(side_effect=TimeoutError("slow"))
    ):
        result = await svc.validate_api_key_detailed("anthropic", "sk-ant-not-real")
    assert result.is_valid is False
    assert result.error_code == KEY_CHECK_UNAVAILABLE
    assert result.error_message == KEY_CHECK_UNAVAILABLE_MESSAGE
    assert "slow" not in (result.error_message or "")
    assert "Validation error" not in (result.error_message or "")


def test_the_humanizer_passes_the_fixed_line_through_for_the_unavailable_code():
    result = ValidationResult(
        provider="openai",
        is_valid=False,
        error_message=KEY_CHECK_UNAVAILABLE_MESSAGE,
        error_code=KEY_CHECK_UNAVAILABLE,
    )
    assert humanize_validation_result(result) == KEY_CHECK_UNAVAILABLE_MESSAGE


def test_no_validator_site_renders_the_exception_any_more():
    import inspect

    src = inspect.getsource(llm_mod)
    assert 'error_message=f"Validation error' not in src
    assert 'error_code="NETWORK_ERROR"' not in src


# --- the key service -----------------------------------------------------------------


def _service_with_validator(side_effect=None, result=None) -> UserAPIKeyService:
    svc = UserAPIKeyService(field_encryption_service=FieldEncryptionService(b"k" * 32))
    # the key-shape validator is not under test here; a fake key must reach the provider check
    report = MagicMock(
        format_valid=True, strength_acceptable=True, leak_safe=True, security_level="test"
    )
    svc._validator = MagicMock()
    svc._validator.validate_api_key = AsyncMock(return_value=report)
    llm = MagicMock()
    if side_effect is not None:
        llm.validate_api_key_detailed = AsyncMock(side_effect=side_effect)
    else:
        llm.validate_api_key_detailed = AsyncMock(return_value=result)
    svc._llm_config = llm
    return svc


@pytest.mark.asyncio
async def test_the_key_service_raises_the_typed_error_for_an_unrun_check_not_a_value_error():
    unavailable = ValidationResult(
        provider="anthropic",
        is_valid=False,
        error_message=KEY_CHECK_UNAVAILABLE_MESSAGE,
        error_code=KEY_CHECK_UNAVAILABLE,
    )
    svc = _service_with_validator(result=unavailable)
    with pytest.raises(KeyCheckUnavailable) as ei:
        await svc.store_user_key(
            user_id="validation-only",
            provider="anthropic",
            api_key="sk-ant-api03-not-a-real-key-but-long-enough-to-pass-the-shape-check-0000",
            session=MagicMock(),
            validate=True,
            store=False,
        )
    assert not isinstance(ei.value, ValueError)


@pytest.mark.asyncio
async def test_a_validator_that_raises_is_the_typed_error_too():
    svc = _service_with_validator(side_effect=TimeoutError("slow"))
    with pytest.raises(KeyCheckUnavailable):
        await svc.store_user_key(
            user_id="validation-only",
            provider="anthropic",
            api_key="sk-ant-api03-not-a-real-key-but-long-enough-to-pass-the-shape-check-0000",
            session=MagicMock(),
            validate=True,
            store=False,
        )


# --- the routes ----------------------------------------------------------------------


@pytest.mark.asyncio
async def test_validate_key_says_the_check_could_not_run_when_the_validator_times_out():
    """Arch's pin (1): a validator raising TimeoutError -> the fixed line, not valid=False
    with the exception text."""
    svc = _service_with_validator(side_effect=TimeoutError("slow"))
    with (
        patch("web.api.routes.setup.UserAPIKeyService", return_value=svc),
        patch(
            "web.api.routes.setup.AsyncSessionFactory.session_scope_fresh", return_value=_scope()
        ),
    ):
        response = await validate_api_key(
            ApiKeyValidateRequest(
                provider="anthropic",
                api_key="sk-ant-api03-not-a-real-key-but-long-enough-to-pass-the-shape-check-0000",
            )
        )
    assert response.valid is False
    assert response.message == KEY_CHECK_COULD_NOT_RUN_MESSAGE
    assert "slow" not in response.message and "Timeout" not in response.message


@pytest.mark.asyncio
async def test_validate_key_re_raises_a_key_store_error_from_inside_the_store_call():
    """Arch's point (4): KeyStoreConfigError is a ValueError by type; raised inside the
    store call it must still reach the server-fault branch, never render the parameter."""
    service = MagicMock()
    service.store_user_key = AsyncMock(side_effect=KeyStoreConfigError(STAGING_ERROR))
    with (
        patch("web.api.routes.setup.UserAPIKeyService", return_value=service),
        patch(
            "web.api.routes.setup.AsyncSessionFactory.session_scope_fresh", return_value=_scope()
        ),
    ):
        response = await validate_api_key(
            ApiKeyValidateRequest(provider="anthropic", api_key="sk-ant-test-not-real")
        )
    assert response.message == SERVER_CANNOT_STORE_KEYS_MESSAGE
    assert "master_key" not in response.message


@pytest.mark.asyncio
async def test_keychain_check_renders_no_exception_text():
    broken = MagicMock()
    broken.get_api_key.side_effect = RuntimeError("keyring-internal-detail")
    with patch("services.infrastructure.keychain_service.KeychainService", return_value=broken):
        response = await check_keychain("anthropic")
    assert response.exists is False
    assert response.message == KEY_CHECK_COULD_NOT_RUN_MESSAGE
    assert "keyring-internal-detail" not in response.message


@pytest.mark.asyncio
async def test_setup_complete_with_the_staging_error_names_no_parameter():
    """Arch's pin (3)."""
    from web.api.routes.setup import SetupCompleteRequest, complete_setup

    with (
        patch(
            "web.api.routes.setup.UserAPIKeyService", side_effect=KeyStoreConfigError(STAGING_ERROR)
        ),
        patch("web.api.routes.setup._setup_principal", return_value="user-1"),
    ):
        with pytest.raises(HTTPException) as ei:
            await complete_setup(SetupCompleteRequest(), current_user=None)
    assert ei.value.status_code == 503
    assert ei.value.detail == SERVER_CANNOT_STORE_KEYS_MESSAGE
    assert "master_key" not in ei.value.detail and "48 bytes" not in ei.value.detail
    with (
        patch("web.api.routes.setup.UserAPIKeyService", side_effect=RuntimeError("boom-internal")),
        patch("web.api.routes.setup._setup_principal", return_value="user-1"),
    ):
        with pytest.raises(HTTPException) as ei2:
            await complete_setup(SetupCompleteRequest(), current_user=None)
    assert ei2.value.detail == SETUP_COULD_NOT_FINISH_MESSAGE
    assert "boom-internal" not in ei2.value.detail


def test_no_setup_route_renders_an_exception_to_the_page():
    """Arch 10-22 10:07 / CXO: no page prints str(e). The one allowed str(e) in a reply is
    the provider's own refusal of a key (validate-key's inner ValueError)."""
    import re
    from pathlib import Path

    src = Path("web/api/routes/setup.py").read_text()
    renders = [
        ln.strip()
        for ln in src.splitlines()
        if re.search(r"(detail|message)=f?\".*\{str\(e\)\}", ln)
    ]
    assert renders == [], renders


def test_the_keychain_no_store_message_carries_the_type_not_the_cause():
    from pathlib import Path

    src = Path("services/infrastructure/keychain_service.py").read_text()
    # #2353 reworded the sentence; the rule is the same: the type, never the cause.
    assert "unavailable ({type(e).__name__})" in src
    assert "unavailable ({e})" not in src and "unavailable ({str(e)})" not in src
