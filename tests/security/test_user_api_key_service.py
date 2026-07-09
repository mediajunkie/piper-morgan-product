"""
Tests for UserAPIKeyService - Multi-User API Key Isolation

Tests verify that:
1. Different users can store keys for the same provider
2. Keys are isolated per user (user A can't access user B's keys)
3. Store/retrieve/delete operations work correctly per user
4. Key validation works per user
5. List operations show only user-specific keys

Issue #228 CORE-USERS-API Phase 1E
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

# Test fixtures
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService


@pytest.fixture
def test_users(request):
    """Create test user objects for isolation testing with unique IDs per test"""
    import time

    test_name = request.node.name
    timestamp = str(int(time.time() * 1000000))[-8:]  # Last 8 digits for uniqueness
    user_a = User(
        id=str(
            uuid4()
        ),  # #262: users.id is UUID — string ids fail the column type (pre-existing fixture bug)
        username=f"{test_name}_a_{timestamp}",
        email=f"user_a_{timestamp}@example.com",
        is_active=True,
    )
    user_b = User(
        id=str(
            uuid4()
        ),  # #262: users.id is UUID — string ids fail the column type (pre-existing fixture bug)
        username=f"{test_name}_b_{timestamp}",
        email=f"user_b_{timestamp}@example.com",
        is_active=True,
    )
    return user_a, user_b


@pytest.fixture
def mock_keychain():
    """Mock keychain service for testing"""
    keychain = MagicMock()
    keychain._storage = {}  # In-memory storage for testing

    def store_key(provider, api_key, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        keychain._storage[key_name] = api_key

    def get_key(provider, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        return keychain._storage.get(key_name)

    def delete_key(provider, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        if key_name in keychain._storage:
            del keychain._storage[key_name]

    keychain.store_api_key = MagicMock(side_effect=store_key)
    keychain.get_api_key = MagicMock(side_effect=get_key)
    keychain.delete_api_key = MagicMock(side_effect=delete_key)

    return keychain


@pytest.mark.asyncio
async def test_multi_user_key_isolation(test_users, mock_keychain):
    """
    Test that different users can store keys for the same provider
    without interfering with each other.

    Issue #228 CORE-USERS-API - Multi-user key isolation
    """
    user_a, user_b = test_users

    # Create service with mock keychain (skip validation)
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create users in database
        session.add(user_a)
        session.add(user_b)
        await session.commit()  # Flush to ensure IDs are available

        # Valid test keys (proper format and length for OpenAI)
        key_a_value = "sk-" + "a" * 48  # Valid OpenAI format and length
        key_b_value = "sk-" + "b" * 48  # Valid OpenAI format and length

        # Mock BOTH validator and llm_config
        with (
            patch.object(service._validator, "validate_api_key") as mock_validator,
            patch.object(service._llm_config, "validate_api_key", return_value=True),
        ):
            # Mock validator to allow these keys
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-a...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # User A stores OpenAI key
            key_a = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=key_a_value,
                validate=False,  # Skip provider validation for speed
            )

            # Update mock for user B
            mock_validator.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-b...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # User B stores OpenAI key (same provider, different key!)
            key_b = await service.store_user_key(
                session=session,
                user_id=user_b.id,
                provider="openai",
                api_key=key_b_value,
                validate=False,  # Skip provider validation for speed
            )

        # Verify both keys stored in database
        assert key_a is not None
        assert key_b is not None
        assert key_a.user_id == user_a.id
        assert key_b.user_id == user_b.id
        assert key_a.provider == "openai"
        assert key_b.provider == "openai"

        # Verify keys stored in keychain with different references
        assert key_a.key_reference == f"piper_{user_a.id}_openai"
        assert key_b.key_reference == f"piper_{user_b.id}_openai"

        # Retrieve user A's key - should get user A's key only
        retrieved_key_a = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="openai"
        )
        assert retrieved_key_a == key_a_value

        # Retrieve user B's key - should get user B's key only
        retrieved_key_b = await service.retrieve_user_key(
            session=session, user_id=user_b.id, provider="openai"
        )
        assert retrieved_key_b == key_b_value

        # Verify keychain was called with correct username parameter
        mock_keychain.get_api_key.assert_any_call("openai", username=user_a.id)
        mock_keychain.get_api_key.assert_any_call("openai", username=user_b.id)

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_delete_user_key_isolation(test_users, mock_keychain):
    """
    Test that deleting user A's key doesn't affect user B's key
    for the same provider.

    Issue #228 CORE-USERS-API - Delete isolation
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create users in database
        session.add(user_a)
        session.add(user_b)
        await session.commit()

        # Use valid key formats that pass validation
        key_a_value = "sk-" + "a" * 48
        key_b_value = "sk-" + "b" * 48

        # Mock validator to allow these keys
        with patch.object(service._validator, "validate_api_key") as mock_validator:
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="anthropic",
                api_key_preview="sk-a...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="anthropic"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # Store keys for both users
            await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="anthropic",
                api_key=key_a_value,
                validate=False,
            )

            await service.store_user_key(
                session=session,
                user_id=user_b.id,
                provider="anthropic",
                api_key=key_b_value,
                validate=False,
            )

        # Delete user A's key
        deleted = await service.delete_user_key(
            session=session, user_id=user_a.id, provider="anthropic"
        )
        assert deleted is True

        # Verify user A's key is gone
        key_a = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="anthropic"
        )
        assert key_a is None

        # Verify user B's key still exists
        key_b = await service.retrieve_user_key(
            session=session, user_id=user_b.id, provider="anthropic"
        )
        assert key_b == key_b_value

        # Cleanup
        await service.delete_user_key(session, user_b.id, "anthropic")


@pytest.mark.asyncio
async def test_list_user_keys_isolation(test_users, mock_keychain):
    """
    Test that list_user_keys only returns keys for the specified user.

    Issue #228 CORE-USERS-API - List isolation
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create users in database
        session.add(user_a)
        session.add(user_b)
        await session.commit()

        # Mock validator
        with patch.object(service._validator, "validate_api_key") as mock_validator:
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-x...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # User A stores 2 keys
            await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key="sk-" + "a" * 48,
                validate=False,
            )
            await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="anthropic",
                api_key="sk-" + "a" * 48,
                validate=False,
            )

            # User B stores 1 key
            await service.store_user_key(
                session=session,
                user_id=user_b.id,
                provider="openai",
                api_key="sk-" + "b" * 48,
                validate=False,
            )

        # List user A's keys - should see 2 keys
        keys_a = await service.list_user_keys(session=session, user_id=user_a.id, active_only=True)
        assert len(keys_a) == 2
        providers_a = {key["provider"] for key in keys_a}
        assert providers_a == {"openai", "anthropic"}

        # List user B's keys - should see 1 key
        keys_b = await service.list_user_keys(session=session, user_id=user_b.id, active_only=True)
        assert len(keys_b) == 1
        assert keys_b[0]["provider"] == "openai"

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_a.id, "anthropic")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_store_user_key_update_existing(test_users, mock_keychain):
    """
    Test that storing a key for an existing (user_id, provider) updates
    the record rather than creating a duplicate.

    Issue #228 CORE-USERS-API - Update behavior
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user in database
        session.add(user_a)
        await session.commit()

        # Mock validator
        with patch.object(service._validator, "validate_api_key") as mock_validator:
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-x...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # Store initial key
            key1 = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key="sk-" + "a" * 48,
                validate=False,
            )
            initial_id = key1.id

            # Store new key (should update, not create new)
            key2 = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key="sk-" + "b" * 48,
                validate=False,
            )

        # Verify same record updated (same ID)
        assert key2.id == initial_id

        # Verify only one record exists
        result = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_a.id, UserAPIKey.provider == "openai"
            )
        )
        all_keys = result.scalars().all()
        assert len(all_keys) == 1

        # Verify new key retrieved (should be the second key stored)
        retrieved_key = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="openai"
        )
        assert retrieved_key == "sk-" + "b" * 48

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")


@pytest.mark.asyncio
async def test_validate_user_key_per_user(test_users, mock_keychain):
    """
    Test that key validation works per user.

    Issue #228 CORE-USERS-API - Validation per user
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create users in database
        session.add(user_a)
        session.add(user_b)
        await session.commit()

        # Mock validator for storage
        with patch.object(service._validator, "validate_api_key") as mock_validator:
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-x...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # Store keys for both users (skip initial validation)
            key_a_value = "sk-" + "a" * 48
            key_b_value = "sk-" + "b" * 48

            await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=key_a_value,
                validate=False,
            )

            await service.store_user_key(
                session=session,
                user_id=user_b.id,
                provider="openai",
                api_key=key_b_value,
                validate=False,
            )

        # Mock validation - user A's key is valid, user B's is invalid
        async def mock_validate(provider, api_key):
            if api_key == key_a_value:
                return True
            return False

        with patch.object(service._llm_config, "validate_api_key", side_effect=mock_validate):
            # Validate user A's key
            is_valid_a = await service.validate_user_key(
                session=session, user_id=user_a.id, provider="openai"
            )
            assert is_valid_a is True

            # Validate user B's key
            is_valid_b = await service.validate_user_key(
                session=session, user_id=user_b.id, provider="openai"
            )
            assert is_valid_b is False

        # Verify validation status in database
        result_a = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_a.id, UserAPIKey.provider == "openai"
            )
        )
        key_a = result_a.scalar_one()
        assert key_a.is_validated is True
        assert key_a.last_validated_at is not None

        result_b = await session.execute(
            select(UserAPIKey).where(
                UserAPIKey.user_id == user_b.id, UserAPIKey.provider == "openai"
            )
        )
        key_b = result_b.scalar_one()
        assert key_b.is_validated is False

        # Cleanup
        await service.delete_user_key(session, user_a.id, "openai")
        await service.delete_user_key(session, user_b.id, "openai")


@pytest.mark.asyncio
async def test_keychain_reference_format(test_users, mock_keychain):
    """
    Test that keychain references follow the correct format:
    piper_{user_id}_{provider}

    Issue #228 CORE-USERS-API - Reference format
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user in database
        session.add(user_a)
        await session.commit()

        # Mock validator
        with patch.object(service._validator, "validate_api_key") as mock_validator:
            from services.security.api_key_validator import ValidationReport
            from services.security.key_leak_detector import LeakCheckResult
            from services.security.key_strength_analyzer import KeyStrength
            from services.security.provider_key_validator import ValidationResult

            mock_validator.return_value = ValidationReport(
                provider="github",
                api_key_preview="ghp-...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="github"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.9,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.9,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=True,
                security_level="high",
                recommendations=[],
                warnings=[],
            )

            # Store key for user A
            github_key = "ghp_" + "a" * 36
            key = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="github",
                api_key=github_key,
                validate=False,
            )

        # Verify reference format
        expected_reference = f"piper_{user_a.id}_github"
        assert key.key_reference == expected_reference

        # Verify keychain was called with correct username
        mock_keychain.store_api_key.assert_called_with("github", github_key, username=user_a.id)

        # Cleanup
        await service.delete_user_key(session, user_a.id, "github")


@pytest.mark.asyncio
async def test_retrieve_nonexistent_key_returns_none(test_users, mock_keychain):
    """
    Test that retrieving a non-existent key returns None without error.

    Issue #228 CORE-USERS-API - Error handling
    """
    user_a, user_b = test_users
    service = UserAPIKeyService(keychain_service=mock_keychain)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Try to retrieve key that doesn't exist
        key = await service.retrieve_user_key(
            session=session, user_id=user_a.id, provider="nonexistent"
        )

        assert key is None


# ---------------------------------------------------------------------------
# #358 Phase 2 — encrypted-at-rest user-secret store (the #1185 enabler)
# ---------------------------------------------------------------------------


def _all_pass_report(provider: str, preview: str):
    """Minimal all-pass ValidationReport (mirrors test_multi_user_key_isolation)."""
    from services.security.api_key_validator import ValidationReport
    from services.security.key_leak_detector import LeakCheckResult
    from services.security.key_strength_analyzer import KeyStrength
    from services.security.provider_key_validator import ValidationResult

    return ValidationReport(
        provider=provider,
        api_key_preview=preview,
        format_valid=True,
        format_result=ValidationResult(valid=True, message="ok", provider=provider),
        strength_acceptable=True,
        strength_result=KeyStrength(
            length_score=1.0,
            entropy_score=0.9,
            character_diversity_score=1.0,
            pattern_score=0.9,
            overall_score=0.9,
            recommendations=[],
            security_level="strong",
        ),
        leak_safe=True,
        leak_result=LeakCheckResult(leaked=False, source=None),
        overall_valid=True,
        security_level="high",
        recommendations=[],
        warnings=[],
    )


@pytest.mark.asyncio
async def test_secret_encrypted_at_rest_and_round_trips(test_users, mock_keychain):
    """#358: with an encryptor configured, store writes an encrypted_secret (NOT the
    plaintext) and retrieve returns the original by decrypting it."""
    from services.security.field_encryption import FieldEncryptionService

    user_a, _ = test_users
    enc = FieldEncryptionService(b"K" * 32)
    service = UserAPIKeyService(keychain_service=mock_keychain, field_encryption_service=enc)
    key_value = "sk-" + "a" * 48

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user_a)
        await session.commit()
        with patch.object(
            service._validator,
            "validate_api_key",
            return_value=_all_pass_report("openai", "sk-a..."),
        ):
            row = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=key_value,
                validate=False,
            )
        # at-rest: a non-null encrypted_secret that is NOT the plaintext
        assert row.encrypted_secret
        assert key_value not in row.encrypted_secret
        # retrieve decrypts back to the original
        assert await service.retrieve_user_key(session, user_a.id, "openai") == key_value


@pytest.mark.asyncio
async def test_retrieve_falls_back_to_keychain_without_encrypted_secret(test_users, mock_keychain):
    """A legacy / pre-migration row has no encrypted_secret → retrieve uses the keychain."""
    from services.security.field_encryption import FieldEncryptionService

    user_a, _ = test_users
    enc = FieldEncryptionService(b"K" * 32)
    service = UserAPIKeyService(keychain_service=mock_keychain, field_encryption_service=enc)
    value = "sk-" + "c" * 48

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user_a)
        await session.commit()
        with patch.object(
            service._validator,
            "validate_api_key",
            return_value=_all_pass_report("openai", "sk-c..."),
        ):
            row = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=value,
                validate=False,
            )
        # simulate a legacy/pre-migration row: clear the encrypted column (keychain keeps it)
        row.encrypted_secret = None
        await session.commit()
        # retrieve must fall back to the keychain
        assert await service.retrieve_user_key(session, user_a.id, "openai") == value


class _RaisingKeychain:
    """Simulates the hosted-Linux container: python-keyring has no backend, so
    every keychain op raises (#1382 — live alpha evidence 2026-07-08)."""

    def store_api_key(self, provider, api_key, username=None):
        raise RuntimeError("No recommended backend was available.")

    def get_api_key(self, provider, username=None):
        raise RuntimeError("No recommended backend was available.")

    def delete_api_key(self, provider, username=None):
        raise RuntimeError("No recommended backend was available.")


@pytest.mark.asyncio
async def test_store_survives_keychain_failure_with_encryptor(test_users):
    """#1382: on hosted (keychain dead, encryptor present) the wizard key save must
    SUCCEED via the encrypted-DB store — this exact case failed live on alpha."""
    from services.security.field_encryption import FieldEncryptionService

    user_a, _ = test_users
    enc = FieldEncryptionService(b"K" * 32)
    service = UserAPIKeyService(
        keychain_service=_RaisingKeychain(), field_encryption_service=enc
    )
    key_value = "sk-" + "b" * 48

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user_a)
        await session.commit()
        with patch.object(
            service._validator,
            "validate_api_key",
            return_value=_all_pass_report("openai", "sk-b..."),
        ):
            row = await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=key_value,
                validate=False,
            )
        assert row.encrypted_secret and key_value not in row.encrypted_secret
        # retrieve prefers encrypted_secret — the dead keychain is never consulted
        assert await service.retrieve_user_key(session, user_a.id, "openai") == key_value


@pytest.mark.asyncio
async def test_store_keychain_failure_fatal_without_encryptor(test_users):
    """#1382 boundary: keychain-only mode (no encryptor) keeps failure FATAL —
    nothing else would hold the key."""
    user_a, _ = test_users
    service = UserAPIKeyService(keychain_service=_RaisingKeychain())
    service._encryptor = None  # force local keychain-only mode deterministically

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user_a)
        await session.commit()
        with patch.object(
            service._validator,
            "validate_api_key",
            return_value=_all_pass_report("openai", "sk-c..."),
        ):
            with pytest.raises(ValueError, match="Keychain storage failed"):
                await service.store_user_key(
                    session=session,
                    user_id=user_a.id,
                    provider="openai",
                    api_key="sk-" + "c" * 48,
                    validate=False,
                )


@pytest.mark.asyncio
async def test_rotate_refreshes_encrypted_secret(test_users, mock_keychain):
    """#1382 (companion bug): rotation must refresh encrypted_secret — the read path
    prefers the encrypted column, so a stale one would serve the OLD key forever."""
    from services.security.field_encryption import FieldEncryptionService

    user_a, _ = test_users
    enc = FieldEncryptionService(b"K" * 32)
    service = UserAPIKeyService(keychain_service=mock_keychain, field_encryption_service=enc)
    old_key = "sk-" + "d" * 48
    new_key = "sk-" + "e" * 48

    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user_a)
        await session.commit()
        with patch.object(
            service._validator,
            "validate_api_key",
            return_value=_all_pass_report("openai", "sk-..."),
        ):
            await service.store_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                api_key=old_key,
                validate=False,
            )
            await service.rotate_user_key(
                session=session,
                user_id=user_a.id,
                provider="openai",
                new_api_key=new_key,
                validate=False,
            )
        # pre-fix this returned old_key (stale ciphertext preferred by the read path)
        assert await service.retrieve_user_key(session, user_a.id, "openai") == new_key
