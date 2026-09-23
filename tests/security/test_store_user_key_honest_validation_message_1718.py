"""#1718 — UserAPIKeyService.store_user_key carries the SPECIFIC validation-failure
reason instead of collapsing it to a bare bool.

Mirrors the fixture pattern in test_user_api_key_service_validation.py (#933): real
DB session, real format/strength/leak validator (the canonical
"passes all real-validator checks" key from the #932 suite), `service._llm_config`
overridden so the PROVIDER-API check is deterministic and network-free.

Two call shapes exercised (both go through UserAPIKeyService, not LLMConfigService
directly — that's covered in tests/config/test_llm_key_validation_reasons_1718.py):
  - store=False (validation-only, the setup-wizard's /validate-key route): the
    ValueError raised on failure carries the honest sentence, not the old flat
    "API key validation failed for {provider}".
  - store=True (Settings -> LLM API Keys' /keys/store route, #485's "keep the
    entered key even if unvalidated" behavior): the record IS still stored, and
    carries a transient `.validation_message` with the honest sentence for the
    route to surface — behavior unchanged, message honesty is the fix.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.config.llm_config_service import ValidationResult
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

# Canonical "passes format+strength+leak-unknown" OpenAI-shaped key from the
# #932/#933 suite.
GOOD_FORMAT_KEY = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

# Anthropic requires its own "sk-ant-" prefix + 100+ chars (provider_key_validator.py);
# generated once with `secrets`, verified to pass format+strength+leak-unknown.
GOOD_FORMAT_ANTHROPIC_KEY = (
    "sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Er"
    "av78tNfnQFyXEFWQyY56veWIGGPdPyICeV"
)

QUOTA_SENTENCE = (
    "I can't reach a language model — the API key on your account is out of "
    "quota (or its billing needs attention)."
)
INVALID_KEY_SENTENCE = "The language-model API key on your account isn't valid."


@pytest.fixture
def test_user(request):
    import time
    from uuid import uuid4

    from services.database.models import User

    timestamp = str(int(time.time() * 1000000))[-8:]
    return User(
        id=uuid4(),
        username=f"t1718_{timestamp}",
        email=f"t1718_{timestamp}@example.com",
        is_active=True,
    )


@pytest.fixture
def mock_keychain():
    keychain = MagicMock()
    keychain._storage = {}

    def store_key(provider, api_key, username=None):
        keychain._storage[f"{username}_{provider}_api_key"] = api_key

    keychain.store_api_key = MagicMock(side_effect=store_key)
    keychain.get_api_key = MagicMock(return_value=None)
    keychain.delete_api_key = MagicMock(return_value=None)
    return keychain


def _quota_result(provider: str) -> ValidationResult:
    return ValidationResult(
        provider=provider,
        is_valid=False,
        error_code="VALIDATION_ERROR",
        error_message=(
            'Validation failed: 400 Bad Request {"type":"error","error":'
            '{"type":"invalid_request_error","message":"Your credit balance '
            'is too low to access the Claude API."}}'
        ),
    )


def _auth_result(provider: str) -> ValidationResult:
    return ValidationResult(
        provider=provider,
        is_valid=False,
        error_code="AUTH_ERROR",
        error_message=(
            'Invalid API key: 401 Unauthorized {"type":"error","error":'
            '{"type":"authentication_error","message":"invalid x-api-key"}}'
        ),
    )


@pytest.mark.asyncio
async def test_store_true_quota_failure_stores_key_with_honest_message(test_user, mock_keychain):
    """#485: the key is kept even though provider validation failed. #1718: the
    returned record's transient .validation_message carries the QUOTA sentence,
    not silence and not a generic failure string."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_quota_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()

        result = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key=GOOD_FORMAT_ANTHROPIC_KEY,
            validate=True,
            store=True,
        )

    assert result is not None, "#485: key must still be stored despite failed validation"
    assert result.is_validated is False
    assert result.validation_message == QUOTA_SENTENCE
    mock_keychain.store_api_key.assert_called_once()


@pytest.mark.asyncio
async def test_store_false_rejected_credential_raises_with_honest_message(test_user, mock_keychain):
    """The setup-wizard's /validate-key route (store=False, validation-only):
    the ValueError's message IS the honest sentence — this is the literal fix
    for the "flat invalid" bug #1718 filed against."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(return_value=_auth_result("openai"))

    async with AsyncSessionFactory.session_scope_fresh() as session:
        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=session,
                user_id="validation-only",
                provider="openai",
                api_key=GOOD_FORMAT_KEY,
                validate=True,
                store=False,
            )

    assert str(exc_info.value) == INVALID_KEY_SENTENCE
    mock_keychain.store_api_key.assert_not_called()


@pytest.mark.asyncio
async def test_store_true_quota_failure_message_differs_from_auth_failure_message(
    test_user, mock_keychain
):
    """The whole point of #1718: the two causes must not collapse to the same
    sentence. Same fixture shape as the quota test above, AUTH_ERROR instead."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_auth_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()

        result = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key=GOOD_FORMAT_ANTHROPIC_KEY,
            validate=True,
            store=True,
        )

    assert result.validation_message == INVALID_KEY_SENTENCE
    assert result.validation_message != QUOTA_SENTENCE


@pytest.mark.asyncio
async def test_valid_key_carries_no_validation_message(test_user, mock_keychain):
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=ValidationResult(provider="anthropic", is_valid=True)
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()

        result = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key=GOOD_FORMAT_ANTHROPIC_KEY,
            validate=True,
            store=True,
        )

    assert result.is_validated is True
    assert result.validation_message is None
