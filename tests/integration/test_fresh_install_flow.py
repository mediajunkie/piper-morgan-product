"""
State Transition Tests: Fresh Install Flow

Tests the complete journey from empty database to first authenticated use.
This catches temporal/ordering bugs that steady-state tests miss.

Issue #485: FK violations during setup wizard - root cause was that tests
always pre-created users, so the "fresh install" flow was never tested.

These tests use the fresh_database fixture which clears all user data,
simulating a brand new installation where no users exist yet.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.security.user_api_key_service import UserAPIKeyService


@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_api_key_validation_no_database_writes(fresh_database, transition_state):
    """
    API key validation with store=False should NOT create any database records.

    This is the core test for Issue #485 - the bug was that validation was
    creating UserAPIKey records even though it was supposed to be validation-only.

    Regression test: If this fails, the FK violation bug has regressed.
    """
    await transition_state.capture_before(fresh_database)

    service = UserAPIKeyService()

    # Mock the LLM config validation to return True (simulates valid key)
    with patch.object(service._llm_config, "validate_api_key", new=AsyncMock(return_value=True)):
        # Call with store=False - should validate but not store anything
        result = await service.store_user_key(
            session=fresh_database,
            user_id="validation-only",  # This would fail FK constraint if stored
            provider="openai",
            api_key="sk-tQ7xR2mV9pL4wN8bK3fJ6hD1gS5aZ0yE",
            validate=True,
            store=False,  # The key fix from Issue #485
        )

    # Result should be None when store=False
    assert result is None, "store=False should return None, not a UserAPIKey record"

    await transition_state.capture_after(fresh_database)

    # No database records should have been created
    transition_state.assert_no_new_records("user_api_keys", "audit_logs")


@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_api_key_validation_fails_on_invalid_key(fresh_database):
    """
    API key validation with store=False should raise ValueError on invalid key.

    When store=False, validation failures should raise an exception so the
    caller knows the key is invalid.
    """
    service = UserAPIKeyService()

    # Mock the LLM config validation to return False (simulates invalid key)
    with patch.object(service._llm_config, "validate_api_key", new=AsyncMock(return_value=False)):
        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=fresh_database,
                user_id="validation-only",
                provider="anthropic",
                api_key="invalid-key",
                validate=True,
                store=False,
            )

    assert "validation failed" in str(exc_info.value).lower()


@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_store_user_key_with_store_true_requires_existing_user(fresh_database):
    """
    Storing a key with store=True on a fresh database should fail FK constraint.

    This test verifies the FK constraint is working as expected - if we try to
    store a key for a non-existent user, it should fail with an integrity error.

    This is the expected behavior that was triggering the bug before #485 fix.
    """
    from uuid import uuid4

    from sqlalchemy.exc import IntegrityError

    service = UserAPIKeyService()

    # Generate a valid UUID that doesn't exist in the database
    nonexistent_user_id = str(uuid4())

    # Mock keychain to avoid actual keychain operations
    with (
        patch.object(service._keychain, "store_api_key"),
        patch.object(service._llm_config, "validate_api_key", new=AsyncMock(return_value=True)),
    ):
        with pytest.raises(IntegrityError):
            # This should fail because no user exists with this ID
            await service.store_user_key(
                session=fresh_database,
                user_id=nonexistent_user_id,
                provider="openai",
                api_key="sk-tQ7xR2mV9pL4wN8bK3fJ6hD1gS5aZ0yE",
                validate=True,
                store=True,  # Actually try to store - should fail FK
            )


@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_store_user_key_succeeds_after_user_created(fresh_database, transition_state):
    """
    Storing a key should succeed after user is created (correct flow).

    This tests the happy path: first create user, then store key.
    This is the correct order that avoids FK violations.
    """
    from uuid import uuid4

    from services.database.models import User

    await transition_state.capture_before(fresh_database)

    # Step 1: Create user first (this is the correct order)
    user_id = str(uuid4())
    user = User(
        id=user_id,
        username="test_user",
        email="test@example.com",
        password_hash="test_hash",
    )
    fresh_database.add(user)
    await fresh_database.commit()

    # Step 2: Now store key for existing user
    service = UserAPIKeyService()

    with (
        patch.object(service._keychain, "store_api_key"),
        patch.object(service._llm_config, "validate_api_key", new=AsyncMock(return_value=True)),
    ):
        result = await service.store_user_key(
            session=fresh_database,
            user_id=user_id,
            provider="openai",
            api_key="sk-tQ7xR2mV9pL4wN8bK3fJ6hD1gS5aZ0yE",
            validate=True,
            store=True,
        )

    # Should succeed and return a UserAPIKey
    assert result is not None
    assert result.user_id == user_id
    assert result.provider == "openai"

    await transition_state.capture_after(fresh_database)

    # Should have created exactly 1 user and 1 user_api_key
    transition_state.assert_new_records("users", count=1)
    transition_state.assert_new_records("user_api_keys", count=1)
