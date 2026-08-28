"""
Tests for UserAPIKeyService — Active-Validation Path (Issue #933)

Verifies that the security-validation pipeline runs end-to-end on
store_user_key() after #933 re-enabled it. The earlier bypass
(`skip_validation = True`) was removed in commit 7462e6b2; these tests
lock in the integration with #932 (honest-unknown leak semantics) so
that:

  1. Format-invalid keys are rejected (ValueError).
  2. Low-entropy / strength-failing keys are rejected (ValueError).
  3. Known test keys from KeyLeakDetector._load_known_test_keys() are
     blocked by the leak quick-check (high confidence → blocking).
  4. Keys that pass format + strength + slip past the leak quick-check
     hit the #932 "unknown" branch (confidence=0.0) and STILL store
     successfully — the load-bearing assertion that the #932 + #933
     integration works as intended.
  5. Validation failures don't produce success-path side effects
     (no keychain write, no KEY_STORED audit log entry).

Issue #933: SEC: API key validation re-enabled
Issue #932: leak-check honest unknown (Option C)
Issue #228: CORE-USERS-API Phase 1C — original feature
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_user(request):
    """Create a test User with a real UUID (matches DB schema).

    Uses uuid4 + per-test-name suffix for isolation across the suite.
    Test-name prefix in username/email for log readability.
    """
    import time

    test_name = request.node.name
    timestamp = str(int(time.time() * 1000000))[-8:]
    return User(
        id=uuid4(),
        username=f"t_{test_name[:20]}_{timestamp}",
        email=f"t_{timestamp}@example.com",
        is_active=True,
    )


@pytest.fixture
def mock_keychain():
    """Mock keychain service to verify store_api_key call sites."""
    keychain = MagicMock()
    keychain._storage = {}

    def store_key(provider, api_key, username=None):
        key_name = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
        keychain._storage[key_name] = api_key

    keychain.store_api_key = MagicMock(side_effect=store_key)
    keychain.get_api_key = MagicMock(return_value=None)
    keychain.delete_api_key = MagicMock(return_value=None)
    return keychain


@pytest.fixture
def mock_llm_config():
    """Mock provider-API validator (separate from the security validator).

    `validate=False` is passed in tests below to avoid this path entirely;
    fixture exists so service._llm_config can be safely overridden.
    """
    mock = MagicMock()
    mock.validate_api_key = AsyncMock(return_value=True)
    return mock


# ============================================================================
# TEST 1: FORMAT VALIDATION (real validator, no mocks)
# ============================================================================


@pytest.mark.asyncio
async def test_store_user_key_validates_format(test_user, mock_keychain, mock_llm_config):
    """A key with invalid format → ValueError raised before keychain write.

    #933: the format check is the first gate. We pass a string that does
    NOT match any provider's prefix pattern (no `sk-`, no `ghp_`) — the
    real APIKeyValidator + ProviderKeyValidator should reject it.

    The exception must fire BEFORE keychain.store_api_key is called.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Invalid format: no provider prefix, just a raw string
        invalid_key = "not-a-valid-format-12345"

        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=invalid_key,
                validate=False,
            )

        error_message = str(exc_info.value)
        # Error should mention format failure
        assert (
            "format" in error_message.lower()
        ), f"Expected format-failure message, got: {error_message}"
        assert (
            "validation failed" in error_message.lower()
        ), f"Expected validation-failed wording, got: {error_message}"

        # Critical: keychain should NOT have been called
        mock_keychain.store_api_key.assert_not_called()


# ============================================================================
# TEST 2: STRENGTH VALIDATION (real validator, no mocks)
# ============================================================================


@pytest.mark.asyncio
async def test_store_user_key_validates_strength(test_user, mock_keychain, mock_llm_config):
    """A low-entropy key (all repeated chars) → ValueError, no keychain write.

    #933: strength is the second gate after format. A key that has the
    correct `sk-` prefix but is built from a single repeated character
    has near-zero entropy and should be rejected by KeyStrengthAnalyzer.

    Note: this key may also trip the leak quick-check's
    `_is_obviously_fake` (repeated-character heuristic). Both paths
    raise ValueError pre-keychain; the test asserts the rejection
    happened, not which gate fired first.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Valid OpenAI prefix but pathologically low entropy
        weak_key = "sk-" + "a" * 40

        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=weak_key,
                validate=False,
            )

        error_message = str(exc_info.value)
        # Error wording should reference weakness, entropy, or leak/breach
        # (depending on which gate caught it — both are blocking).
        msg_lower = error_message.lower()
        assert any(
            w in msg_lower for w in ("weak", "entropy", "breach", "leak")
        ), f"Expected strength/leak-failure message, got: {error_message}"
        # Keychain should not have been called
        mock_keychain.store_api_key.assert_not_called()


# ============================================================================
# TEST 3: KNOWN TEST KEY BLOCKED BY LEAK QUICK-CHECK
# ============================================================================


@pytest.mark.asyncio
async def test_store_user_key_blocks_known_test_key(test_user, mock_keychain, mock_llm_config):
    """A known test key from _load_known_test_keys() → blocked with high confidence.

    #932 + #933: the leak quick-check fires with confidence=1.0 for keys
    in the known-test-keys set. That confidence>0.0 means leak_safe
    DOES gate overall_valid (per #932's honest-unknown logic).

    Uses `sk-1234567890abcdef1234567890abcdef1234567890abcdef` from
    KeyLeakDetector._load_known_test_keys() — guaranteed to be on the
    blocklist.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # This is in the known-test-keys set (see key_leak_detector.py)
        known_test_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"

        with pytest.raises(ValueError) as exc_info:
            await service.store_user_key(
                session=session,
                user_id=test_user.id,
                provider="openai",
                api_key=known_test_key,
                validate=False,
            )

        error_message = str(exc_info.value)
        # Should mention breach/leak (the leak-quick-check fired)
        # OR weak pattern (1234567890 also matches a weak pattern,
        # whichever the quick-check catches first).
        msg_lower = error_message.lower()
        assert any(
            w in msg_lower for w in ("breach", "leak", "weak", "test")
        ), f"Expected leak/test-key-failure message, got: {error_message}"

        # Keychain should not have been called
        mock_keychain.store_api_key.assert_not_called()


# ============================================================================
# TEST 4: LOAD-BEARING — UNKNOWN-LEAK PATH PASSES (the #932 + #933 integration)
# ============================================================================


@pytest.mark.asyncio
async def test_store_user_key_passes_unknown_leak_with_valid_format_strength(
    test_user, mock_keychain, mock_llm_config
):
    """Valid format + sufficient strength + leak=unknown (#932) → key STORES.

    LOAD-BEARING for the #932 + #933 integration. This test locks in
    that:
      - format check passes (valid `sk-` prefix + 47 chars)
      - strength check passes (high entropy, no repeats, no patterns)
      - leak quick-check passes (not in known-test-keys, no weak
        patterns, not obviously-fake)
      - the leak detector falls through to the #932 honest-unknown
        branch (confidence=0.0, severity='unknown')
      - APIKeyValidator's `leak_check_performed = leak_result.confidence
        > 0.0` is False, so leak_safe is NOT a gate → overall_valid=True
      - the key is stored successfully (mock_keychain.store_api_key
        called, DB record created)

    If anyone breaks the #932 honest-unknown logic (e.g., flips leak_safe
    back to a hard gate without a real lookup), this test fails: the
    overall_valid would be False and the store would raise ValueError.

    Fixture key: `sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT`
    (used in #932's tests/unit/services/security/test_api_key_validator.py
    as the canonical "passes all checks" key.)
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Create the user in the DB so the foreign-key constraint passes
        session.add(test_user)
        await session.commit()

        # Canonical "passes all real-validator checks" key from #932 suite
        good_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        # Pass user_id as string — the user_id DB column coerces to UUID
        # while the created_by String(255) column needs a string. The
        # production code currently passes user_id straight through to
        # both, so a string input works for both columns.
        user_id_str = str(test_user.id)

        # No mocks on the validator — we want the REAL validator to run
        # so this test exercises the full #932 + #933 integration.
        result = await service.store_user_key(
            session=session,
            user_id=user_id_str,
            provider="openai",
            api_key=good_key,
            validate=False,  # skip provider-API check (network)
        )

        # Storage succeeded — UserAPIKey record returned
        assert result is not None, (
            "Expected store_user_key to return a UserAPIKey record "
            "(format+strength passed, leak=unknown should NOT block per #932)"
        )
        assert str(result.user_id) == user_id_str
        assert result.provider == "openai"
        assert result.is_active is True

        # Keychain WAS called (validation passed)
        mock_keychain.store_api_key.assert_called_once()
        call_args = mock_keychain.store_api_key.call_args
        assert call_args[0][0] == "openai"
        assert call_args[0][1] == good_key


# ============================================================================
# TEST 5: VALIDATION FAILURE PRODUCES NO SUCCESS-PATH SIDE EFFECTS
# ============================================================================


@pytest.mark.asyncio
async def test_store_user_key_audit_logs_validation_failure(
    test_user, mock_keychain, mock_llm_config
):
    """On validation failure, KEY_VALIDATION_FAILED audit event fires; KEY_STORED does not.

    #1071: when the validator rejects a key, store_user_key now emits an
    audit-log entry recording the failure (security-relevant event) BEFORE
    raising ValueError. The audit entry captures provider, key_preview
    (first 8 chars), failure_reason, and failed_checks — NEVER the full
    key value. The non-blocking try/except ensures audit-log failures
    don't prevent the primary ValueError signal.

    Originally filed #933: previous behavior pinned that NO KEY_STORED
    success log fired on failure. #1071 added the FAILURE event without
    changing that absence-of-success-event guarantee — both invariants
    must hold.
    """
    service = UserAPIKeyService(keychain_service=mock_keychain)
    service._llm_config = mock_llm_config

    async with AsyncSessionFactory.session_scope_fresh() as session:
        invalid_key = "not-a-valid-format-12345"

        # Patch the audit_logger to observe call activity
        with patch("services.security.user_api_key_service.audit_logger") as mock_audit_logger:
            mock_audit_logger.log_api_key_event = AsyncMock()

            with pytest.raises(ValueError):
                await service.store_user_key(
                    session=session,
                    user_id=test_user.id,
                    provider="openai",
                    api_key=invalid_key,
                    validate=False,
                )

            # The success-path audit event must NOT fire on failure.
            # Specifically: no log_api_key_event(action="key_stored",
            # status="success", ...) call should have been made.
            success_calls = [
                call
                for call in mock_audit_logger.log_api_key_event.call_args_list
                if call.kwargs.get("action") == "key_stored"
                and call.kwargs.get("status") == "success"
            ]
            assert len(success_calls) == 0, (
                f"Expected no KEY_STORED success audit on validation failure, "
                f"got: {success_calls}"
            )

            # #1071: the failure-path audit event MUST fire (security-relevant event).
            # Exactly one log_api_key_event(action="key_validation_failed",
            # status="failed", ...) call should have been made, with provider,
            # key_preview, failure_reason, and failed_checks captured in details.
            failure_calls = [
                call
                for call in mock_audit_logger.log_api_key_event.call_args_list
                if call.kwargs.get("action") == "key_validation_failed"
                and call.kwargs.get("status") == "failed"
            ]
            assert len(failure_calls) == 1, (
                f"Expected exactly one KEY_VALIDATION_FAILED audit on failure, "
                f"got {len(failure_calls)} calls"
            )

            failure_call = failure_calls[0]
            assert failure_call.kwargs["provider"] == "openai"
            assert failure_call.kwargs["user_id"] == test_user.id
            details = failure_call.kwargs["details"]
            assert "key_preview" in details
            assert "failure_reason" in details
            assert "failed_checks" in details
            # PII protection: full key value must NEVER appear in audit details.
            assert invalid_key not in str(
                details
            ), f"Full key value leaked into audit details: {details}"
            # key_preview is first 8 chars + "..." (or "<too_short>" if key < 9 chars)
            assert details["key_preview"] in (f"{invalid_key[:8]}...", "<too_short>")

        # And of course the keychain wasn't touched either
        mock_keychain.store_api_key.assert_not_called()
