"""
Tests for Key Storage Validation Integration

Tests verify that:
1. Invalid format keys are rejected before storage
2. Weak keys are rejected before storage
3. Leaked/test keys are rejected before storage
4. Valid keys are stored successfully
5. Clear error messages are provided for each validation failure
6. Validation happens before keychain storage
7. Error messages specify the failure reason

Issue #268 CORE-KEYS-STORAGE-VALIDATION
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select

from services.config.llm_config_service import ValidationResult as LLMValidationResult
from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.api_key_validator import APIKeyValidator, ValidationReport
from services.security.key_leak_detector import LeakCheckResult
from services.security.key_strength_analyzer import KeyStrength
from services.security.provider_key_validator import ValidationResult
from services.security.user_api_key_service import UserAPIKeyService
from tests.conftest import TEST_USER_ID

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_user(request):
    """Provide a test user ID for validation tests"""
    # Use unique ID based on test name and timestamp
    import time

    test_name = request.node.name
    timestamp = str(int(time.time() * 1000000))[-8:]  # Last 8 digits for uniqueness
    user_id = uuid4()  # Issue #262 - UUID instead of string
    username = f"test_key_{test_name[:15]}_{timestamp}"  # Limit to keep it reasonable
    return User(
        id=user_id,
        username=username,
        email=f"test_{timestamp}@example.com",
        is_active=True,
    )


@pytest.fixture
def mock_keychain():
    """Mock keychain service for testing"""
    keychain = MagicMock()
    keychain._storage = {}

    def store_key(provider, api_key, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        keychain._storage[key_name] = api_key

    keychain.store_api_key = MagicMock(side_effect=store_key)
    return keychain


@pytest.fixture
def mock_llm_config():
    """Mock LLM config service"""
    mock = MagicMock()
    mock.validate_api_key = AsyncMock(return_value=True)
    # #1718: store_user_key now calls validate_api_key_detailed (the FULL
    # ValidationResult) instead of the bare-bool validate_api_key. Both are
    # mocked so this fixture stays a faithful double of the real service
    # regardless of which method production code calls.
    mock.validate_api_key_detailed = AsyncMock(
        return_value=LLMValidationResult(provider="openai", is_valid=True)
    )
    return mock


# ============================================================================
# TEST SCENARIO 1: INVALID FORMAT
# ============================================================================


@pytest.mark.asyncio
async def test_invalid_format_key_rejected(test_user, mock_keychain, mock_llm_config):
    """
    Test that keys with invalid format are rejected before storage.

    Format validation checks provider-specific key prefixes.
    Example: OpenAI keys must start with 'sk-'
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Use invalid format key (wrong prefix for OpenAI)
        invalid_key = "invalid-key-12345"

        # Attempt to store should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=invalid_key,
                validate=False,  # Skip provider validation
            )

        # Verify error message is specific about format
        error_message = str(exc_info.value)
        assert "format" in error_message.lower(), f"Error should mention format: {error_message}"
        assert (
            "validation failed" in error_message.lower()
        ), f"Error should mention validation: {error_message}"

        # Verify keychain.store_api_key was NOT called
        mock_keychain.store_api_key.assert_not_called()

        print(f"✓ Invalid format rejected with message: {error_message}")


# ============================================================================
# TEST SCENARIO 2: WEAK KEY (LOW ENTROPY)
# ============================================================================


@pytest.mark.asyncio
async def test_weak_key_rejected(test_user, mock_keychain, mock_llm_config):
    """
    Test that keys with low entropy are rejected before storage.

    Weak keys have insufficient entropy and are vulnerable to brute force.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Use low-entropy key (repetitive characters)
        weak_key = "sk-" + "a" * 48  # Valid format but weak entropy

        # Mock the validator to indicate weak key
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-aaa...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=False,
                strength_result=KeyStrength(
                    length_score=0.7,
                    entropy_score=0.35,  # 35% entropy (below 70% requirement)
                    character_diversity_score=0.5,
                    pattern_score=0.4,
                    overall_score=0.35,
                    recommendations=["Increase key entropy"],
                    security_level="weak",
                ),
                leak_safe=True,
                leak_result=LeakCheckResult(leaked=False, source=None),
                overall_valid=False,
                security_level="low",
                recommendations=["Increase key entropy"],
                warnings=["Key entropy too low"],
            )

            # Attempt to store should raise ValueError
            with pytest.raises(ValueError) as exc_info:
                await service.store_user_key(
                    session=session,
                    user_id=test_user.id,
                    provider="openai",
                    api_key=weak_key,
                    validate=False,
                )

            # Verify error mentions entropy
            error_message = str(exc_info.value)
            assert (
                "weak" in error_message.lower() or "entropy" in error_message.lower()
            ), f"Error should mention key strength: {error_message}"
            assert (
                "35" in error_message or "35%" in error_message
            ), f"Error should show entropy percentage: {error_message}"

            # Verify keychain was not called
            mock_keychain.store_api_key.assert_not_called()

            print(f"✓ Weak key rejected with message: {error_message}")


# ============================================================================
# TEST SCENARIO 3: LEAKED/TEST KEY
# ============================================================================


@pytest.mark.asyncio
async def test_leaked_key_rejected(test_user, mock_keychain, mock_llm_config):
    """
    Test that keys found in breach databases are rejected before storage.

    Test keys and demo keys are detected to prevent accidental storage.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Use a test/demo key pattern
        test_key = "sk-test-demo-key-12345"

        # Mock the validator to indicate leaked key
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-test...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.95,
                    character_diversity_score=1.0,
                    pattern_score=0.9,
                    overall_score=0.95,
                    recommendations=[],
                    security_level="strong",
                ),
                leak_safe=False,  # Key found in breach database
                leak_result=LeakCheckResult(leaked=True, source="test_pattern"),
                overall_valid=False,
                security_level="critical",
                recommendations=["Rotate this key immediately"],
                warnings=["Key found in breach database"],
            )

            # Attempt to store should raise ValueError
            with pytest.raises(ValueError) as exc_info:
                await service.store_user_key(
                    session=session,
                    user_id=test_user.id,
                    provider="openai",
                    api_key=test_key,
                    validate=False,
                )

            # Verify error mentions breach/leak
            error_message = str(exc_info.value)
            assert (
                "breach" in error_message.lower() or "leak" in error_message.lower()
            ), f"Error should mention breach/leak: {error_message}"
            assert (
                "test_pattern" in error_message
            ), f"Error should identify breach source: {error_message}"

            # Verify keychain was not called
            mock_keychain.store_api_key.assert_not_called()

            print(f"✓ Leaked key rejected with message: {error_message}")


# ============================================================================
# TEST SCENARIO 4: VALID KEY STORED SUCCESSFULLY
# ============================================================================


@pytest.mark.asyncio
async def test_valid_key_stored_successfully(test_user, mock_keychain, mock_llm_config):
    """
    Test that keys passing all validation checks are stored successfully.

    Valid keys should:
    - Pass format validation
    - Have sufficient entropy
    - Not be in breach database
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    # Create test user in database first
    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create user
        user = User(
            id=test_user.id,
            username=test_user.username,
            email=test_user.email,
            is_active=True,
        )
        session.add(user)
        await session.commit()

        # Use a valid-looking key
        valid_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz"

        # Mock the validator to indicate valid key
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-proj-...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.87,
                    character_diversity_score=1.0,
                    pattern_score=0.85,
                    overall_score=0.87,
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

            # Store should succeed
            result = await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=valid_key,
                validate=False,
            )

            # Verify result is a UserAPIKey record
            assert result is not None
            assert result.user_id == test_user.id
            assert result.provider == "openai"
            assert result.is_active is True

            # Verify keychain.store_api_key was called
            mock_keychain.store_api_key.assert_called_once()
            call_args = mock_keychain.store_api_key.call_args
            assert call_args[0][0] == "openai"  # provider
            assert call_args[0][1] == valid_key  # api_key

            # Verify record exists in database
            db_result = await session.execute(
                select(UserAPIKey).where(
                    (UserAPIKey.user_id == test_user.id) & (UserAPIKey.provider == "openai")
                )
            )
            db_key = db_result.scalar_one_or_none()
            assert db_key is not None
            assert db_key.is_active is True

            print("✓ Valid key stored successfully")


# ============================================================================
# TEST SCENARIO 5: VALIDATION ERRORS DON'T BREAK EXISTING TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_validation_integration_with_mock_llm_config(
    test_user, mock_keychain, mock_llm_config
):
    """
    Test that validation integration works correctly with mocked dependencies.

    This verifies that new validation code doesn't break existing patterns.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    # Create user in database first
    async with AsyncSessionFactory.session_scope_fresh() as session:
        user = User(
            id=test_user.id,
            username=test_user.username,
            email=test_user.email,
            is_active=True,
        )
        session.add(user)
        await session.commit()

        valid_key = "sk-proj-abcdef1234567890abcdef1234567890"

        # Patch validator to allow this test
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.return_value = ValidationReport(
                provider="openai",
                api_key_preview="sk-proj-...",
                format_valid=True,
                format_result=ValidationResult(
                    valid=True, message="Valid format", provider="openai"
                ),
                strength_acceptable=True,
                strength_result=KeyStrength(
                    length_score=1.0,
                    entropy_score=0.88,
                    character_diversity_score=1.0,
                    pattern_score=0.87,
                    overall_score=0.88,
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

            # Provider validation should be called with validate=True
            result = await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=valid_key,
                validate=True,  # Should call provider validation
            )

            # Both validators should be called. #1718: production now calls
            # validate_api_key_detailed (the FULL ValidationResult), not the
            # bare-bool validate_api_key — assert the method actually invoked.
            mock_validate.assert_called_once_with("openai", valid_key)
            mock_llm_config.validate_api_key_detailed.assert_called_once_with("openai", valid_key)

            assert result.is_validated is True
            print("✓ Validation integration works with existing code")


# ============================================================================
# TEST SCENARIO 6: MULTIPLE VALIDATION FAILURES
# ============================================================================


@pytest.mark.asyncio
async def test_multiple_validation_failures_reported(test_user, mock_keychain, mock_llm_config):
    """
    Test that multiple validation failures are all reported in error message.

    If a key fails multiple validation checks, user should see all issues.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        bad_key = "invalid_format_and_weak"

        # Mock validator to indicate multiple failures
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.return_value = ValidationReport(
                provider="openai",
                api_key_preview="invalid-...",
                format_valid=False,
                format_result=ValidationResult(
                    valid=False, message="Must start with sk-", provider="openai"
                ),
                strength_acceptable=False,
                strength_result=KeyStrength(
                    length_score=0.3,
                    entropy_score=0.20,
                    character_diversity_score=0.2,
                    pattern_score=0.1,
                    overall_score=0.20,
                    recommendations=["Use a proper API key"],
                    security_level="weak",
                ),
                leak_safe=False,
                leak_result=LeakCheckResult(leaked=True, source="common_test_patterns"),
                overall_valid=False,
                security_level="critical",
                recommendations=["Use a proper API key"],
                warnings=["Multiple security issues"],
            )

            # Attempt to store
            with pytest.raises(ValueError) as exc_info:
                await service.store_user_key(
                    session=session,
                    user_id=test_user.id,
                    provider="openai",
                    api_key=bad_key,
                    validate=False,
                )

            # Error message should mention all failures
            error_message = str(exc_info.value)
            print(f"✓ Multiple failures reported: {error_message}")

            # Should mention at least format and leak
            assert "format" in error_message.lower() or "sk-" in error_message
            assert "breach" in error_message.lower() or "leak" in error_message.lower()


# ============================================================================
# TEST SCENARIO 7: VALIDATION EXCEPTION HANDLING
# ============================================================================


@pytest.mark.asyncio
async def test_validation_exception_handling(test_user, mock_keychain, mock_llm_config):
    """
    Test that exceptions from validator are handled gracefully.

    If validation code raises unexpected exceptions, they should be caught
    and converted to clear error messages.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        test_key = "sk-12345"

        # Mock validator to raise an exception
        with patch.object(service._validator, "validate_api_key") as mock_validate:
            mock_validate.side_effect = Exception("Validator crashed!")

            # Should convert to ValueError
            with pytest.raises(ValueError) as exc_info:
                await service.store_user_key(
                    session=session,
                    user_id=test_user.id,
                    provider="openai",
                    api_key=test_key,
                    validate=False,
                )

            error_message = str(exc_info.value)
            assert "Failed to validate API key" in error_message
            print(f"✓ Validation exception handled: {error_message}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
