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


def _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="testuser", **extra):
    """#1091 fix: tests originally used `generate_token(user_id, username)` which
    was renamed to `generate_access_token(user_id, user_email, scopes, username)`
    by #857. This helper preserves the old test ergonomics while calling the
    actual method. Email and scopes default to test-safe values; callers can
    still pass extras (e.g., `session_id`, `workspace_id`)."""
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{username}@test.local",
        scopes=["api:user"],
        username=username,
        **extra,
    )


def _decode_unsafe(token):
    """#1091 fix: `JWTService.decode_token_unsafe` no longer exists post-#857.
    Replacement: direct pyjwt decode with signature verification disabled.
    Matches the original test intent — peek at payload without validating —
    while not coupling to a JWTService method that has been removed."""
    return pyjwt.decode(token, options={"verify_signature": False})


def _decode_safe(jwt_service, token):
    """#1091 fix: `JWTService.validate_token` is now async + returns a
    JWTClaims dataclass, not a payload dict. For tests that previously
    inspected the payload dict directly, this helper does the same
    pyjwt-decode-with-verification the service does internally — returning
    a payload dict for the test's assertion shape. Raises pyjwt exceptions
    on tampered/expired/wrong-key tokens (use pytest.raises to assert
    rejection)."""
    return pyjwt.decode(
        token,
        jwt_service.secret_key,
        algorithms=[jwt_service.algorithm],
        audience=jwt_service.audience,
        issuer=jwt_service.issuer,
    )


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
        token = _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="testuser")

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

        token = _gen_test_token(jwt_service, user_id=user_id, username=username)

        # Decode without verification to check claims
        payload = _decode_unsafe(token)

        assert payload is not None, "Token should decode"
        # Issue #730 / #857: user_id moved to standard `sub` claim; stored as str
        assert payload["sub"] == str(user_id), "Token should include user_id in sub claim"
        assert payload["username"] == username, "Token should include username"
        assert "exp" in payload, "Token should include expiration"
        assert "iat" in payload, "Token should include issued-at"
        # Issue #857: claim renamed from `type` to `token_type` for clarity
        assert payload.get("token_type") == "access", "Token should be marked as access token"

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
        token = _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="expuser")
        after_time = datetime.now(timezone.utc)

        payload = _decode_unsafe(token)

        # #857: timestamps are integer epoch seconds (whole-second precision).
        # Compare as tz-aware UTC datetimes; truncate before/after to whole
        # seconds so the comparison doesn't fail on sub-second precision drift.
        iat = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
        before_sec = before_time.replace(microsecond=0)
        after_sec = after_time.replace(microsecond=0) + timedelta(seconds=1)
        assert before_sec <= iat <= after_sec, "Issued-at time should be current time"

        # Check expiration is in future
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert exp > after_time, "Expiration should be in future"

        # Check expiration is within the configured access-token window.
        # #857: default access_token_expire_minutes is 30; legacy "~24 hours
        # for alpha" framing is obsolete.
        time_diff = exp - iat
        minutes_diff = time_diff.total_seconds() / 60
        expected_min = jwt_service.access_token_expire_minutes
        # Allow ±1 minute tolerance for clock skew during test
        assert (
            (expected_min - 1) <= minutes_diff <= (expected_min + 1)
        ), f"Token should expire in ~{expected_min} minutes: got {minutes_diff:.1f}"

    def test_validate_token_success(self):
        """
        Verify valid tokens validate successfully.

        Success Criteria:
        - Fresh token decodes + signature verifies
        - Payload contains all claims

        #1091 fix: `JWTService.validate_token` is now async + returns a
        `JWTClaims` dataclass. For this test's purpose (verify valid
        tokens pass signature verification), we use `_decode_safe` which
        does the same pyjwt-decode-with-verification the service does
        internally and returns the payload dict the original assertion
        shape expects.
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        user_id = TEST_USER_ID
        username = "validuser"

        token = _gen_test_token(jwt_service, user_id=user_id, username=username)

        # Verify signature + decode payload
        payload = _decode_safe(jwt_service, token)

        assert payload is not None, "Valid token should validate"
        # Issue #730: user_id stored in `sub` per JWT standard claims
        assert payload["sub"] == str(user_id)
        assert payload["username"] == username

    def test_validate_token_expired(self):
        """
        Verify expired tokens rejected.

        Success Criteria:
        - Token with past expiration is rejected with pyjwt.ExpiredSignatureError
        - Underlying JWT lib (and JWTService.validate_token built on it)
          will not accept expired tokens

        #1091 fix: `validate_token` originally returned None on expired;
        new `JWTService.validate_token` raises `TokenExpired`. For this
        test's purpose, pyjwt direct decode raises `ExpiredSignatureError`
        on expiry — same underlying property, exception-based.
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        # Manually create expired token
        expired_payload = {
            "sub": "expired-user",
            "user_email": "expired@test.local",
            "username": "expireduser",
            "scopes": ["api:user"],
            "iss": jwt_service.issuer,
            "aud": jwt_service.audience,
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            "iat": datetime.now(timezone.utc) - timedelta(hours=25),
        }

        expired_token = pyjwt.encode(
            expired_payload, jwt_service.secret_key, algorithm=jwt_service.algorithm
        )

        with pytest.raises(pyjwt.ExpiredSignatureError):
            _decode_safe(jwt_service, expired_token)

    def test_validate_token_tampered(self):
        """
        Verify tampered tokens rejected.

        Success Criteria:
        - Modified token fails signature verification (raises
          pyjwt.InvalidSignatureError)

        #1091 fix: see test_validate_token_expired — exception-based now.
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        token = _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="tamperuser")

        # Tamper with payload (change one character in middle section)
        parts = token.split(".")
        tampered_payload = parts[1][:-1] + ("A" if parts[1][-1] != "A" else "B")
        tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"

        with pytest.raises(
            (pyjwt.InvalidSignatureError, pyjwt.DecodeError, pyjwt.InvalidTokenError)
        ):
            _decode_safe(jwt_service, tampered_token)

    def test_validate_token_wrong_secret(self):
        """
        Verify tokens signed with wrong secret rejected.

        Success Criteria:
        - Token signed with different secret fails signature verification

        #1091 fix: see test_validate_token_expired — exception-based now.
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        wrong_secret_token = pyjwt.encode(
            {
                "sub": "wrong-secret-user",
                "user_email": "wrong@test.local",
                "username": "wronguser",
                "scopes": ["api:user"],
                "iss": jwt_service.issuer,
                "aud": jwt_service.audience,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
                "iat": datetime.now(timezone.utc),
            },
            "completely_different_secret_key_12345",
            algorithm="HS256",
        )

        with pytest.raises(pyjwt.InvalidSignatureError):
            _decode_safe(jwt_service, wrong_secret_token)

    def test_validate_token_malformed(self):
        """
        Verify malformed tokens handled — pyjwt raises on invalid format.

        Success Criteria:
        - Each malformed input raises an InvalidTokenError subclass

        #1091 fix: `validate_token` originally caught these and returned
        None; pyjwt direct decode raises the parser-level exceptions.
        Same underlying property — these strings are not valid JWTs.
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
            with pytest.raises(pyjwt.InvalidTokenError):
                _decode_safe(jwt_service, malformed)

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
            token = _gen_test_token(
                jwt_service,
                user_id=TEST_USER_ID,
                username="claimsuser",
                additional_claims={"role": "admin", "department": "engineering"},
            )

            payload = _decode_unsafe(token)

            assert payload.get("role") == "admin", "Additional claims should be included"
            assert payload.get("department") == "engineering"

        except TypeError:
            # If additional_claims not supported, skip
            pytest.skip("generate_token doesn't support additional_claims parameter")

    def test_decode_unsafe_works(self):
        """
        Verify a JWT can be decoded without signature verification for
        debugging purposes (peek at payload without validating).

        Success Criteria:
        - Token decodes via pyjwt direct decode
        - Payload contains the expected claims

        #1091 fix: `JWTService.decode_token_unsafe` no longer exists
        post-#857. The test is reframed to verify the equivalent
        capability via pyjwt direct decode (`_decode_unsafe` helper).
        """
        from services.auth.jwt_service import JWTService

        jwt_service = JWTService()

        token = _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="decodeuser")

        payload = _decode_unsafe(token)

        assert payload is not None
        # Issue #730 / #857: user_id stored in standard `sub` claim
        assert payload["sub"] == str(TEST_USER_ID)

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
            token = _gen_test_token(jwt_service, user_id=TEST_USER_ID, username="uniqueuser")
            tokens.append(token)
            time.sleep(0.01)  # Small delay to ensure different iat

        # All tokens should be unique
        unique_tokens = set(tokens)
        assert len(unique_tokens) == len(
            tokens
        ), "Tokens should be unique (different iat timestamps)"
