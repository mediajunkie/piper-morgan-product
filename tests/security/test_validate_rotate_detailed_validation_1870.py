"""#1870 (follow-up 2 of 3 from #1718) — UserAPIKeyService.validate_user_key()
and rotate_user_key() still consumed the bare bool from
LLMConfigService.validate_api_key(); the specific cause (rejected credential
vs. no credits/billing) never reached either caller. Route both through
validate_api_key_detailed() (same #1718 pattern `store_user_key` already uses).

Return-shape discipline (kept deliberately bool-compatible where a caller
already treats the return as one):
  - `validate_user_key()` KEEPS returning a bare `bool` — grepped callers:
      * web/api/routes/api_keys.py:331 (`POST /keys/{provider}/validate`)
      * cli/commands/keys.py:219
      * scripts/status_checker.py:114
    all three do `is_valid = await service.validate_user_key(...)` and use
    only truthiness — none inspect a richer return, so changing the return
    type would be a breaking API change none of them expect. The honest
    reason is exposed the SAME way `store_user_key` exposes it instead: a
    transient (non-persisted) `.validation_message` attribute set on the
    `UserAPIKey` record this method already fetches/updates in the same
    session. Reliably visible only to a caller that ALREADY holds a live
    Python reference to that same row (SQLAlchemy's identity map holds
    objects by weak reference, so a caller who instead re-queries fresh
    afterward, holding nothing in between, may get a newly-hydrated instance
    without the attribute — confirmed empirically, see the service method's
    own docstring) — None when valid.
  - `rotate_user_key()` already returned the `UserAPIKey` record (not a bool),
    so no compatibility concern there; it now RAISES `ValueError(<honest
    message>)` on a rejected new key instead of the old flat "New API key
    validation failed for {provider}" — mirrors `store_user_key(store=False)`.
    The transient `.validation_message` attribute is also set on the returned
    record for parity (always None at return, since a failure raises before
    that point — kept so future callers inspecting the record see the same
    shape store_user_key's callers do).

LAYER (m-43): service level — `service._llm_config` replaced with a MagicMock
whose `validate_api_key_detailed` is an AsyncMock (no httpx/network; the HTTP-
envelope-level coverage lives in tests/config/test_llm_key_validation_reasons_
{1718,1870}.py). DENOMINATOR: both methods x {valid, rejected-credential,
no-credits/quota} where applicable, plus the back-compat bool-return check for
`validate_user_key` and the existing-callers-unaffected note above.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.config.llm_config_service import ValidationResult
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

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
        username=f"t1870_{timestamp}",
        email=f"t1870_{timestamp}@example.com",
        is_active=True,
    )


@pytest.fixture
def mock_keychain():
    keychain = MagicMock()
    keychain._storage = {}

    def store_key(provider, api_key, username=None):
        keychain._storage[f"{username}_{provider}_api_key"] = api_key

    def get_key(provider, username=None):
        return keychain._storage.get(f"{username}_{provider}_api_key")

    keychain.store_api_key = MagicMock(side_effect=store_key)
    keychain.get_api_key = MagicMock(side_effect=get_key)
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


# ---------------------------------------------------------------------------
# validate_user_key(): bool-compat return + transient .validation_message
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_validate_user_key_valid_returns_true_no_message(test_user, mock_keychain):
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=ValidationResult(provider="anthropic", is_valid=True)
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        stored = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )
        # #1870: hold a live reference to the SAME row `validate_user_key` will
        # annotate — SQLAlchemy's identity map holds session objects by WEAK
        # reference, so a caller who instead re-queries fresh AFTER the call
        # with nothing held in between may get a newly-hydrated instance
        # without the transient attribute (confirmed empirically). `stored`
        # (the record `store_user_key` returned) IS that same row.

        is_valid = await service.validate_user_key(
            session=session, user_id=str(test_user.id), provider="anthropic"
        )
        assert is_valid is True
        assert isinstance(is_valid, bool)  # #1870: bool-compat, not a richer object
        assert stored.is_validated is True
        assert stored.validation_message is None


@pytest.mark.asyncio
async def test_validate_user_key_quota_failure_carries_honest_message(test_user, mock_keychain):
    """The literal #1870 fix: previously this call site collapsed a no-credits
    failure to a bare `False`, indistinguishable from a rejected key."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_quota_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        stored = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )

        is_valid = await service.validate_user_key(
            session=session, user_id=str(test_user.id), provider="anthropic"
        )
        assert is_valid is False
        assert stored.is_validated is False
        assert stored.validation_message == QUOTA_SENTENCE


@pytest.mark.asyncio
async def test_validate_user_key_rejected_credential_differs_from_quota(test_user, mock_keychain):
    """The whole point: quota and rejected-credential must not collapse to the
    same message (or, pre-#1870, to the same bare False)."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_auth_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        stored = await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )

        is_valid = await service.validate_user_key(
            session=session, user_id=str(test_user.id), provider="anthropic"
        )
        assert is_valid is False
        assert stored.validation_message == INVALID_KEY_SENTENCE
        assert stored.validation_message != QUOTA_SENTENCE


@pytest.mark.asyncio
async def test_validate_user_key_no_key_found_returns_false_unaffected(test_user, mock_keychain):
    """Pre-existing early-return path (no stored key) — #1870 must not touch it."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock()

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()

        is_valid = await service.validate_user_key(
            session=session, user_id=str(test_user.id), provider="anthropic"
        )
        assert is_valid is False
    service._llm_config.validate_api_key_detailed.assert_not_called()


# ---------------------------------------------------------------------------
# rotate_user_key(): honest ValueError on rejected new key
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rotate_user_key_quota_failure_raises_with_honest_message(test_user, mock_keychain):
    """Previously: `raise ValueError(f"New API key validation failed for {provider}")`
    for EVERY cause — #1870 makes the exception message the honest one."""
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_quota_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )

        with pytest.raises(ValueError) as exc_info:
            await service.rotate_user_key(
                session=session,
                user_id=str(test_user.id),
                provider="anthropic",
                new_api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVnewnocred",
                validate=True,
            )

    assert str(exc_info.value) == QUOTA_SENTENCE


@pytest.mark.asyncio
async def test_rotate_user_key_rejected_credential_message_differs_from_quota(
    test_user, mock_keychain
):
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=_auth_result("anthropic")
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )

        with pytest.raises(ValueError) as exc_info:
            await service.rotate_user_key(
                session=session,
                user_id=str(test_user.id),
                provider="anthropic",
                new_api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVnewbadkey",
                validate=True,
            )

    assert str(exc_info.value) == INVALID_KEY_SENTENCE
    assert str(exc_info.value) != QUOTA_SENTENCE


@pytest.mark.asyncio
async def test_rotate_user_key_valid_succeeds_with_no_message(test_user, mock_keychain):
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = MagicMock()
    service._llm_config.validate_api_key_detailed = AsyncMock(
        return_value=ValidationResult(provider="anthropic", is_valid=True)
    )

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(test_user)
        await session.commit()
        await service.store_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVoriginal",
            validate=False,
        )

        rotated = await service.rotate_user_key(
            session=session,
            user_id=str(test_user.id),
            provider="anthropic",
            new_api_key="sk-ant-aqEfYiVg7G5linYsUuCCmyecyA7tEnjFuxAxD8cd3MRbcXnBSOZXBVzvyUaLuoV9sSYBlc5oo8Eravj8tNfnQFyXEFWQyY56veWIGGPdPyICeVnewgoodkey",
            validate=True,
        )

    assert rotated.is_validated is True
    assert rotated.validation_message is None
