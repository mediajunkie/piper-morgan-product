"""#2125: a server that cannot store keys says so; it never blames the key or prints
the parameter (Web on staging, 2026-10-21: "Validation error: master_key must be 32
bytes (AES-256); got 48 bytes" rendered in red under a correct key)."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.security.field_encryption import FieldEncryptionService, KeyStoreConfigError
from web.api.routes.setup import (
    KEY_CHECK_COULD_NOT_RUN_MESSAGE,
    SERVER_CANNOT_STORE_KEYS_MESSAGE,
    ApiKeyValidateRequest,
    KeychainUseRequest,
    use_keychain,
    validate_api_key,
)

STAGING_ERROR = "master_key must be 32 bytes (AES-256); got 48 bytes"


def test_a_wrong_length_master_key_is_a_typed_config_error_and_still_a_value_error():
    with pytest.raises(KeyStoreConfigError) as ei:
        FieldEncryptionService(b"x" * 48)
    assert isinstance(ei.value, ValueError)
    assert str(ei.value) == STAGING_ERROR


@pytest.mark.asyncio
async def test_an_unusable_key_store_blames_the_server_not_the_key():
    with patch(
        "web.api.routes.setup.UserAPIKeyService",
        side_effect=KeyStoreConfigError(STAGING_ERROR),
    ):
        response = await validate_api_key(
            ApiKeyValidateRequest(provider="anthropic", api_key="sk-ant-test-not-real")
        )
    assert response.valid is False
    assert response.message == SERVER_CANNOT_STORE_KEYS_MESSAGE
    for leak in ("master_key", "48 bytes", "AES", "Validation error"):
        assert leak not in response.message


@pytest.mark.asyncio
async def test_an_unexpected_failure_renders_no_exception_text():
    with patch(
        "web.api.routes.setup.UserAPIKeyService",
        side_effect=RuntimeError("boom-internal-detail"),
    ):
        response = await validate_api_key(
            ApiKeyValidateRequest(provider="openai", api_key="sk-test-not-real")
        )
    assert response.valid is False
    assert response.message == KEY_CHECK_COULD_NOT_RUN_MESSAGE
    assert "boom-internal-detail" not in response.message


@pytest.mark.asyncio
async def test_a_key_the_provider_refuses_still_gets_the_providers_reason():
    """Unchanged: a ValueError from the validation itself is the person's to read."""
    service = MagicMock()
    service.store_user_key = AsyncMock(
        side_effect=ValueError("API key validation failed: 401 Unauthorized")
    )
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=MagicMock())
    scope.__aexit__ = AsyncMock(return_value=False)
    with (
        patch("web.api.routes.setup.UserAPIKeyService", return_value=service),
        patch(
            "web.api.routes.setup.AsyncSessionFactory.session_scope_fresh",
            return_value=scope,
        ),
    ):
        response = await validate_api_key(
            ApiKeyValidateRequest(provider="anthropic", api_key="sk-ant-test-not-real")
        )
    assert response.valid is False
    assert response.message == "API key validation failed: 401 Unauthorized"


@pytest.mark.asyncio
async def test_use_keychain_names_no_model_and_renders_no_exception_text():
    """#2117's rule in the sibling route: the keychain path reached no model, so its
    line names none (it said "(claude-3.5)" from a constant table). And a failure
    renders the fixed line, not the exception."""
    keychain = MagicMock()
    keychain.get_api_key.return_value = "sk-ant-from-keychain-not-real"
    with patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain):
        response = await use_keychain(KeychainUseRequest(provider="anthropic"))
    assert response.success is True
    assert response.message == "Using the Anthropic key you already saved."  # CXO: display name
    for model_word in ("claude", "gpt", "gemini-pro", "3.5"):
        assert model_word not in response.message
    broken = MagicMock()
    broken.get_api_key.side_effect = RuntimeError("keyring-internal-detail")
    with patch("services.infrastructure.keychain_service.KeychainService", return_value=broken):
        response = await use_keychain(KeychainUseRequest(provider="anthropic"))
    assert response.success is False
    assert response.message == KEY_CHECK_COULD_NOT_RUN_MESSAGE
    assert "keyring-internal-detail" not in response.message


def test_the_server_side_line_claims_no_action_it_does_not_take():
    """CXO 10-22 07:02: the route only logs; it must not say anyone 'has been told'."""
    assert "has been told" not in SERVER_CANNOT_STORE_KEYS_MESSAGE
    assert "please tell us" in SERVER_CANNOT_STORE_KEYS_MESSAGE
    assert SERVER_CANNOT_STORE_KEYS_MESSAGE == (
        "The server can't store keys right now, so no key can be saved. Your key isn't the "
        "problem. This is on our side, so please tell us."
    )
