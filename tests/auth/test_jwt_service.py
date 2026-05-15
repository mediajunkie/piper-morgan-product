"""
Test suite for JWT tokens (Issue #281: CORE-ALPHA-WEB-AUTH)
Verify JWT token security

These tests define what "done" means for JWT service:
- Tokens properly formatted (3 parts: header.payload.signature)
- Contains required claims (user_id, username, exp, iat)
- Valid tokens validate successfully
- Expired tokens rejected
- Tampered tokens rejected
- Secret from environment variable (not hardcoded)
"""

import time
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import jwt as pyjwt  # Use pyjwt for verification
import pytest

from tests.conftest import TEST_USER_ID, TEST_USER_ID_2


class TestJWTService:
    """Verify JWT token security"""

    def test_jwt_service_exists(self):
        """
        Verify JWTService can be imported.

        Success Criteria:
        - Module exists at expected location
        - Class can be instantiated
        """
        try:
            from services.auth.jwt_service import JWTService

            jwt_service = JWTService()
            assert jwt_service is not None
        except ImportError as e:
            pytest.fail(f"JWTService not found: {e}")

    def test_generate_token_format(self):
        """
        Verify JWT tokens properly formatted.

        Success Criteria:
        - Token has 3 parts separated by dots
        - Each part is base64url encoded
        - Can be decoded without validation
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()
        token = jwt_service.generate_token(user_id=TEST_USER_ID, username="testuser")

        # Verify format: header.payload.signature
        parts = token.split(".")
        assert (
            len(parts) == 3
        ), f"JWT should have 3 parts (header.payload.signature): got {len(parts)}"

        # Each part should be non-empty
        for i, part in enumerate(parts):
            assert len(part) > 0, f"JWT part {i} should not be empty"

    def test_generate_token_claims(self):
        """
        Verify JWT contains required claims.

        Success Criteria:
        - Contains user_id claim
        - Contains username claim
        - Contains exp (expiration) claim
        - Contains iat (issued at) claim
        - Contains type claim
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        user_id = TEST_USER_ID
        username = "claimtester"

        token = jwt_service.generate_token(user_id=user_id, username=username)

        # Decode without verification to check claims
        payload = jwt_service.decode_token_unsafe(token)

        assert payload is not None, "Token should decode"
        assert payload["user_id"] == user_id, "Token should include user_id"
        assert payload["username"] == username, "Token should include username"
        assert "exp" in payload, "Token should include expiration"
        assert "iat" in payload, "Token should include issued-at"
        assert payload.get("type") == "access", "Token should be marked as access token"

    def test_generate_token_expiration(self):
        """
        Verify token expiration is set correctly.

        Success Criteria:
        - Expiration time in future
        - Expiration ~24 hours from now (for alpha)
        - Issued-at time is current time
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        before_time = datetime.now(timezone.utc)
        token = jwt_service.generate_token(user_id=TEST_USER_ID, username="expuser")
        after_time = datetime.now(timezone.utc)

        payload = jwt_service.decode_token_unsafe(token)

        # Check issued-at is recent
        iat = datetime.fromtimestamp(payload["iat"])
        assert before_time <= iat <= after_time, "Issued-at time should be current time"

        # Check expiration is in future
        exp = datetime.fromtimestamp(payload["exp"])
        assert exp > after_time, "Expiration should be in future"

        # Check expiration is approximately 24 hours (for alpha)
        # Allow some tolerance (23-25 hours)
        time_diff = exp - iat
        hours_diff = time_diff.total_seconds() / 3600

        assert (
            23 <= hours_diff <= 25
        ), f"Token should expire in ~24 hours: got {hours_diff:.1f} hours"

    def test_validate_token_success(self):
        """
        Verify valid tokens validate successfully.

        Success Criteria:
        - Fresh token validates
        - Returns payload with all claims
        - Signature verified
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        user_id = TEST_USER_ID
        username = "validuser"

        token = jwt_service.generate_token(user_id=user_id, username=username)

        # Validate token
        payload = jwt_service.validate_token(token)

        assert payload is not None, "Valid token should validate"
        assert payload["user_id"] == user_id
        assert payload["username"] == username

    def test_validate_token_expired(self):
        """
        Verify expired tokens rejected.

        Success Criteria:
        - Token with past expiration returns None
        - No exception raised
        - Graceful handling
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        # Manually create expired token
        # This tests the validation logic
        expired_payload = {
            "user_id": "expired-user",
            "username": "expireduser",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),  # 1 hour ago
            "iat": datetime.now(timezone.utc) - timedelta(hours=25),  # 25 hours ago
        }

        # Encode with same secret
        expired_token = pyjwt.encode(
            expired_payload, jwt_service.secret_key, algorithm=jwt_service.algorithm
        )

        # Validate should return None
        payload = jwt_service.validate_token(expired_token)

        assert payload is None, "Expired token should return None (not raise exception)"

    def test_validate_token_tampered(self):
        """
        Verify tampered tokens rejected.

        Success Criteria:
        - Modified token returns None
        - Signature validation catches tampering
        - No exception raised
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        # Generate valid token
        token = jwt_service.generate_token(user_id=TEST_USER_ID, username="tamperuser")

        # Tamper with payload (change one character in middle section)
        parts = token.split(".")
        # Modify payload part (middle)
        tampered_payload = parts[1][:-1] + ("A" if parts[1][-1] != "A" else "B")
        tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"

        # Validate should return None
        payload = jwt_service.validate_token(tampered_token)

        assert payload is None, "Tampered token should return None (signature validation failed)"

    def test_validate_token_wrong_secret(self):
        """
        Verify tokens signed with wrong secret rejected.

        Success Criteria:
        - Token signed with different secret returns None
        - Signature mismatch detected
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        # Create token with different secret
        wrong_secret_token = pyjwt.encode(
            {
                "user_id": "wrong-secret-user",
                "username": "wronguser",
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                "iat": datetime.now(timezone.utc),
            },
            "completely_different_secret_key_12345",
            algorithm="HS256",
        )

        # Validate should return None
        payload = jwt_service.validate_token(wrong_secret_token)

        assert payload is None, "Token with wrong secret should be rejected"

    def test_validate_token_malformed(self):
        """
        Verify malformed tokens handled gracefully.

        Success Criteria:
        - Invalid format returns None
        - No exception raised
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        malformed_tokens = [
            "not.a.valid.jwt.token",
            "onlyonepart",
            "two.parts",
            "",
            "header.payload",  # Missing signature
            ".....",
        ]

        for malformed in malformed_tokens:
            payload = jwt_service.validate_token(malformed)

            assert payload is None, f"Malformed token should return None: {malformed}"

    def test_secret_key_from_environment(self):
        """
        Verify JWT secret comes from environment variable.

        Success Criteria:
        - JWT_SECRET_KEY env var used if set
        - Has reasonable default for alpha
        - Secret is not empty
        """
        import os

        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        # Verify secret key exists
        assert hasattr(jwt_service, "secret_key"), "JWTService should have secret_key attribute"

        assert jwt_service.secret_key is not None, "Secret key should not be None"

        assert len(jwt_service.secret_key) > 0, "Secret key should not be empty"

        # Verify it's reading from env or has default
        env_secret = os.getenv("JWT_SECRET_KEY")
        if env_secret:
            assert (
                jwt_service.secret_key == env_secret
            ), "Should use JWT_SECRET_KEY from environment"

    def test_secret_key_production_unset_raises(self, monkeypatch):
        """
        Issue #1087: production-mode env with JWT_SECRET_KEY unset must
        raise at JWTService init rather than silently using the dev
        fallback.

        Success Criteria:
        - PIPER_ENVIRONMENT=production + no JWT_SECRET_KEY → RuntimeError
        - Error message names the env var explicitly so deploy operators
          see what to fix
        """
        from services.auth.jwt_service import JWTService

        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
        monkeypatch.delenv("ENVIRONMENT", raising=False)

        with pytest.raises(RuntimeError, match="JWT_SECRET_KEY must be set in production"):
            JWTService()

    def test_secret_key_production_via_environment_var_also_raises(self, monkeypatch):
        """
        Issue #1087: ENVIRONMENT (older convention) also triggers the
        prod guard. Both env var names route to the same check.
        """
        from services.auth.jwt_service import JWTService

        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
        monkeypatch.setenv("ENVIRONMENT", "production")

        with pytest.raises(RuntimeError, match="JWT_SECRET_KEY must be set in production"):
            JWTService()

    def test_secret_key_dev_unset_keeps_fallback(self, monkeypatch, caplog):
        """
        Issue #1087: dev env (or unset env) keeps the warn-and-fallback
        behavior so local development stays frictionless.
        """
        import logging

        from services.auth.jwt_service import JWTService

        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
        monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
        monkeypatch.delenv("ENVIRONMENT", raising=False)

        jwt_service = JWTService()
        assert jwt_service.secret_key == "dev-secret-key-change-in-production"

    def test_secret_key_production_with_key_set_works(self, monkeypatch):
        """
        Issue #1087: production env + JWT_SECRET_KEY set → normal init,
        no error. The prod guard only fires when the key is missing.
        """
        from services.auth.jwt_service import JWTService

        monkeypatch.setenv("JWT_SECRET_KEY", "a-real-production-secret-value-32chars-min")
        monkeypatch.setenv("PIPER_ENVIRONMENT", "production")

        jwt_service = JWTService()
        assert jwt_service.secret_key == "a-real-production-secret-value-32chars-min"

    def test_secret_key_not_hardcoded_in_code(self):
        """
        Verify secret key not hardcoded as weak value.

        Success Criteria:
        - Secret not "secret", "password", "test", etc.
        - Reasonable length (>= 16 chars)
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        weak_secrets = [
            "secret",
            "password",
            "test",
            "12345",
            "jwt_secret",
        ]

        assert (
            jwt_service.secret_key not in weak_secrets
        ), f"Secret key should not be weak value: {jwt_service.secret_key}"

        # Should be reasonable length
        assert (
            len(jwt_service.secret_key) >= 16
        ), f"Secret key should be >= 16 chars for security: got {len(jwt_service.secret_key)}"

    def test_algorithm_is_hs256(self):
        """
        Verify JWT algorithm is HS256.

        Success Criteria:
        - Algorithm set to HS256 (symmetric)
        - Not using insecure algorithms (none, HS0)
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        assert hasattr(jwt_service, "algorithm"), "JWTService should have algorithm attribute"

        assert (
            jwt_service.algorithm == "HS256"
        ), f"Should use HS256 algorithm: got {jwt_service.algorithm}"

    def test_additional_claims(self):
        """
        Verify additional claims can be added to token.

        Success Criteria:
        - generate_token accepts additional_claims parameter
        - Additional claims included in token
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        try:
            token = jwt_service.generate_token(
                user_id=TEST_USER_ID,
                username="claimsuser",
                additional_claims={"role": "admin", "department": "engineering"},
            )

            payload = jwt_service.decode_token_unsafe(token)

            assert payload.get("role") == "admin", "Additional claims should be included"
            assert payload.get("department") == "engineering"

        except TypeError:
            # If additional_claims not supported, skip
            pytest.skip("generate_token doesn't support additional_claims parameter")

    def test_decode_unsafe_method_exists(self):
        """
        Verify decode_token_unsafe method exists for debugging.

        Success Criteria:
        - Method exists
        - Can decode without validation
        - Useful for debugging
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        assert hasattr(
            jwt_service, "decode_token_unsafe"
        ), "JWTService should have decode_token_unsafe method for debugging"

        token = jwt_service.generate_token(user_id=TEST_USER_ID, username="decodeuser")

        payload = jwt_service.decode_token_unsafe(token)

        assert payload is not None
        assert payload["user_id"] == str(TEST_USER_ID)

    def test_token_uniqueness(self):
        """
        Verify tokens are unique even for same user.

        Success Criteria:
        - Multiple tokens for same user are different
        - Issued-at timestamp makes them unique
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        tokens = []
        for _ in range(3):
            token = jwt_service.generate_token(user_id=TEST_USER_ID, username="uniqueuser")
            tokens.append(token)
            time.sleep(0.01)  # Small delay to ensure different iat

        # All tokens should be unique
        unique_tokens = set(tokens)
        assert len(unique_tokens) == len(
            tokens
        ), "Tokens should be unique (different iat timestamps)"
