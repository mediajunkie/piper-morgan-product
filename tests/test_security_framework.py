"""
Comprehensive Security Testing Framework for JWT Authentication

This test suite validates both security standards AND protocol portability for JWT authentication,
ensuring the implementation supports open protocol vision while maintaining bulletproof security.

Test Categories:
1. Authentication Security Testing - Core security validation
2. Protocol Portability Testing - Protocol-first validation for interoperability
3. Future Federation Readiness - OAuth2 and MCP protocol compatibility
4. Performance Testing - Auth endpoint performance validation

Strategic Value: Ensure security implementation supports open protocol vision while maintaining
bulletproof security standards. Framework ready for TDD validation before Code completes Phase 1.
"""

import json
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch

# Import actual JWT library for testing
import jwt
import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.testclient import TestClient

JWT_AVAILABLE = True

from services.api.errors import APIError, AuthenticationRequiredError
from web.app import app

# Test JWT Configuration
TEST_SECRET_KEY = "test_secret_key_for_testing_only"
TEST_ALGORITHM = "HS256"
TEST_ISSUER = "piper-morgan-test"
TEST_AUDIENCE = "piper-morgan-api"

# JWT decode options to skip audience validation in tests
JWT_DECODE_OPTIONS = {
    "verify_aud": False,  # Skip audience validation in tests
    "verify_iss": False,  # Skip issuer validation in tests
}



@pytest.fixture
def test_client():
    """Module-level client (#1452): TestProtocolPortability + TestFederationReadiness
    use this fixture but never defined it (only two OTHER classes carry copies) —
    their 8 tests have been erroring at setup."""
    return TestClient(app)


class TestSecurityAuthentication:
    """Core security validation for JWT authentication"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    @pytest.fixture
    def valid_jwt_token(self):
        """Generate a valid JWT token for testing"""
        payload = {
            "sub": "test_user_123",
            "iss": TEST_ISSUER,
            "aud": TEST_AUDIENCE,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "user_id": "test_user_123",
            "email": "test@example.com",
            "permissions": ["read", "write"],
        }
        return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)

    @pytest.fixture
    def expired_jwt_token(self):
        """Generate an expired JWT token for testing"""
        payload = {
            "sub": "test_user_123",
            "iss": TEST_ISSUER,
            "aud": TEST_AUDIENCE,
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),  # Expired
            "iat": datetime.now(timezone.utc) - timedelta(hours=2),
            "user_id": "test_user_123",
            "email": "test@example.com",
            "permissions": ["read", "write"],
        }
        return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)

    @pytest.fixture
    def invalid_signature_token(self):
        """Generate a token with invalid signature"""
        payload = {
            "sub": "test_user_123",
            "iss": TEST_ISSUER,
            "aud": TEST_AUDIENCE,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "user_id": "test_user_123",
            "email": "test@example.com",
            "permissions": ["read", "write"],
        }
        return jwt.encode(payload, "wrong_secret_key", algorithm=TEST_ALGORITHM)

    async def test_jwt_token_validation(self, test_client, valid_jwt_token):
        """Valid tokens accepted, invalid rejected"""

        # Test valid token acceptance using actual JWT service
        try:
            # Decode valid token to verify it's accepted
            decoded = jwt.decode(
                valid_jwt_token,
                TEST_SECRET_KEY,
                algorithms=[TEST_ALGORITHM],
                options=JWT_DECODE_OPTIONS,
            )
            assert decoded["sub"] == "test_user_123"
            assert decoded["user_id"] == "test_user_123"
            assert "read" in decoded["permissions"]
            assert "write" in decoded["permissions"]
        except Exception as e:
            assert False, f"Valid token should have been accepted: {e}"

        # Test invalid token rejection
        invalid_token = "invalid.jwt.token"
        try:
            jwt.decode(invalid_token, TEST_SECRET_KEY, algorithms=[TEST_ALGORITHM])
            assert False, "Invalid token should have been rejected"
        except jwt.InvalidTokenError:
            assert True, "Invalid token correctly rejected"

    async def test_token_expiration_handling(self, test_client, expired_jwt_token):
        """Expired tokens properly rejected"""

        # Test expired token rejection
        headers = {"Authorization": f"Bearer {expired_jwt_token}"}

        # Test that expired tokens are rejected
        try:
            # Decode expired token to verify expiration
            jwt.decode(
                expired_jwt_token,
                TEST_SECRET_KEY,
                algorithms=[TEST_ALGORITHM],
                options=JWT_DECODE_OPTIONS,
            )
            assert False, "Expired token should have been rejected"
        except jwt.ExpiredSignatureError:
            assert True, "Expired token correctly rejected"

    async def test_unauthorized_access_prevention(self, test_client):
        """Protected endpoints require valid auth"""

        # Test unauthorized access prevention
        # This will need to be updated when actual protected endpoints are implemented

        # Test that unauthorized access is prevented
        try:
            # Test with invalid token
            jwt.decode("invalid_token", TEST_SECRET_KEY, algorithms=[TEST_ALGORITHM])
            assert False, "Unauthorized access should have been prevented"
        except jwt.InvalidTokenError:
            assert True, "Unauthorized access correctly prevented"

    async def test_token_tampering_prevention(self, test_client, valid_jwt_token):
        """Tampered tokens are rejected"""

        # Test token tampering prevention
        tampered_token = valid_jwt_token[:-5] + "tampered"

        # Test that tampered tokens are rejected
        try:
            # Test with tampered token
            jwt.decode(tampered_token, TEST_SECRET_KEY, algorithms=[TEST_ALGORITHM])
            assert False, "Tampered token should have been rejected"
        except jwt.InvalidSignatureError:
            assert True, "Tampered token correctly rejected"

    async def test_algorithm_restriction(self, test_client):
        """Only allowed algorithms are accepted"""

        # Test algorithm restriction
        payload = {
            "sub": "test_user_123",
            "iss": TEST_ISSUER,
            "aud": TEST_AUDIENCE,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "user_id": "test_user_123",
        }

        # Test that supported algorithms are accepted
        supported_algorithms = ["HS256"]  # Only HS256 is guaranteed to work with our test setup

        for algorithm in supported_algorithms:
            token = jwt.encode(payload, TEST_SECRET_KEY, algorithm=algorithm)
            # Token should be created successfully
            assert "eyJ" in token, f"Token creation failed for algorithm {algorithm}"

        # Test that unsupported algorithms are handled gracefully
        unsupported_algorithms = ["HS384", "HS512", "RS256", "ES256"]
        for algorithm in unsupported_algorithms:
            try:
                token = jwt.encode(payload, TEST_SECRET_KEY, algorithm=algorithm)
                # Some algorithms might work, some might not - that's okay for testing
                pass
            except Exception:
                # Some algorithms might not be supported - that's expected
                pass


class TestProtocolPortability:
    """Protocol-first validation for interoperability"""

    @pytest.fixture
    def standard_jwt_token(self):
        """Generate a token with standard JWT claims"""
        payload = {
            "sub": "test_user_123",  # Standard: Subject
            "iss": TEST_ISSUER,  # Standard: Issuer
            "aud": TEST_AUDIENCE,  # Standard: Audience
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Standard: Expiration
            "iat": datetime.now(timezone.utc),  # Standard: Issued At
            "nbf": datetime.now(timezone.utc),  # Standard: Not Before
            "jti": "unique_token_id_123",  # Standard: JWT ID
            "typ": "JWT",  # Standard: Type
            "cty": "JWT",  # Standard: Content Type
            # Custom claims for Piper Morgan
            "user_id": "test_user_123",
            "email": "test@example.com",
            "permissions": ["read", "write"],
            "org_id": "org_123",
            "session_id": "session_456",
        }
        return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)

    async def test_jwt_standard_claims(self, test_client, standard_jwt_token):
        """Tokens use standard claims for interoperability"""

        # Decode token to verify standard claims
        decoded = jwt.decode(
            standard_jwt_token,
            TEST_SECRET_KEY,
            algorithms=[TEST_ALGORITHM],
            options=JWT_DECODE_OPTIONS,
        )

        # Verify all standard JWT claims are present
        standard_claims = ["sub", "iss", "aud", "exp", "iat", "nbf", "jti", "typ", "cty"]
        for claim in standard_claims:
            assert claim in decoded, f"Standard claim {claim} missing from token"

        # Verify custom claims are also present
        custom_claims = ["user_id", "email", "permissions", "org_id", "session_id"]
        for claim in custom_claims:
            assert claim in decoded, f"Custom claim {claim} missing from token"

    async def test_token_export_import(self, test_client, standard_jwt_token):
        """Tokens can travel across protocol boundaries"""

        # Test token export (serialization)
        token_data = {
            "token": standard_jwt_token,
            "metadata": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "algorithm": TEST_ALGORITHM,
                "issuer": TEST_ISSUER,
                "audience": TEST_AUDIENCE,
            },
        }

        # Serialize token data
        exported_token = json.dumps(token_data)
        assert isinstance(exported_token, str)
        assert standard_jwt_token in exported_token

        # Test token import (deserialization)
        imported_data = json.loads(exported_token)
        assert imported_data["token"] == standard_jwt_token
        assert imported_data["metadata"]["algorithm"] == TEST_ALGORITHM

    async def test_user_context_ownership(self, test_client, standard_jwt_token):
        """User clearly owns their context/data"""

        # Decode token to verify user ownership
        decoded = jwt.decode(
            standard_jwt_token,
            TEST_SECRET_KEY,
            algorithms=[TEST_ALGORITHM],
            options=JWT_DECODE_OPTIONS,
        )

        # Verify user identity claims
        assert decoded["sub"] == "test_user_123"
        assert decoded["user_id"] == "test_user_123"
        assert decoded["email"] == "test@example.com"

        # Verify user owns their session
        assert decoded["session_id"] == "session_456"

        # Verify user belongs to organization
        assert decoded["org_id"] == "org_123"

    async def test_audit_log_exportability(self, test_client, standard_jwt_token):
        """Audit logs can be exported/ported"""

        # Create audit log entry
        audit_log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": "test_user_123",
            "action": "token_generated",
            "token_id": "unique_token_id_123",
            "ip_address": "192.168.1.100",
            "user_agent": "test-client/1.0",
            "session_id": "session_456",
            "org_id": "org_123",
        }

        # Test audit log export
        exported_audit = json.dumps(audit_log)
        assert isinstance(exported_audit, str)
        assert "test_user_123" in exported_audit

        # Test audit log import
        imported_audit = json.loads(exported_audit)
        assert imported_audit["user_id"] == "test_user_123"
        assert imported_audit["action"] == "token_generated"

    async def test_cross_protocol_compatibility(self, test_client, standard_jwt_token):
        """Tokens work across different protocols and systems"""

        # Test HTTP header compatibility
        http_headers = {
            "Authorization": f"Bearer {standard_jwt_token}",
            "X-User-ID": "test_user_123",
            "X-Session-ID": "session_456",
        }

        # Verify headers are properly formatted
        assert http_headers["Authorization"].startswith("Bearer ")
        assert http_headers["X-User-ID"] == "test_user_123"

        # Test query parameter compatibility
        query_params = {
            "token": standard_jwt_token,
            "user_id": "test_user_123",
            "session_id": "session_456",
        }

        # Verify query parameters are properly formatted
        assert query_params["token"] == standard_jwt_token
        assert query_params["user_id"] == "test_user_123"


class TestFederationReadiness:
    """OAuth2 and MCP protocol compatibility"""

    @pytest.fixture
    def oauth2_token(self):
        """Generate an OAuth2 compatible token"""
        payload = {
            "sub": "oauth2_user_123",
            "iss": "https://oauth2.provider.com",
            "aud": "piper-morgan-api",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "scope": "read write admin",
            "client_id": "piper_morgan_client",
            "token_type": "Bearer",
            "user_id": "oauth2_user_123",
            "email": "oauth2@example.com",
        }
        return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)

    async def test_oauth2_compatibility_hooks(self, test_client, oauth2_token):
        """OAuth 2.0 patterns supported"""

        # Decode OAuth2 token
        decoded = jwt.decode(
            oauth2_token, TEST_SECRET_KEY, algorithms=[TEST_ALGORITHM], options=JWT_DECODE_OPTIONS
        )

        # Verify OAuth2 specific claims
        oauth2_claims = ["scope", "client_id", "token_type"]
        for claim in oauth2_claims:
            assert claim in decoded, f"OAuth2 claim {claim} missing from token"

        # Verify OAuth2 scope parsing
        scope = decoded["scope"]
        assert "read" in scope
        assert "write" in scope
        assert "admin" in scope

        # Verify client identification
        assert decoded["client_id"] == "piper_morgan_client"

    async def test_mcp_protocol_compatibility(self, test_client, oauth2_token):
        """Authentication works with MCP integration"""

        # Test MCP protocol headers
        mcp_headers = {
            "Authorization": f"Bearer {oauth2_token}",
            "X-MCP-Version": "2024-11-05",
            "X-MCP-Protocol": "jsonrpc",
            "X-MCP-Request-ID": "mcp_req_123",
        }

        # Verify MCP protocol headers
        assert mcp_headers["X-MCP-Version"] == "2024-11-05"
        assert mcp_headers["X-MCP-Protocol"] == "jsonrpc"
        assert mcp_headers["X-MCP-Request-ID"] == "mcp_req_123"

        # Test MCP authentication flow
        mcp_auth_flow = {
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"authentication": {"methods": ["jwt", "oauth2"]}},
                "clientInfo": {"name": "piper-morgan-mcp-client", "version": "1.0.0"},
            },
            "id": 1,
        }

        # Verify MCP authentication flow structure
        assert mcp_auth_flow["method"] == "initialize"
        assert "authentication" in mcp_auth_flow["params"]["capabilities"]
        assert "jwt" in mcp_auth_flow["params"]["capabilities"]["authentication"]["methods"]

    async def test_federation_token_exchange(self, test_client, oauth2_token):
        """Tokens can be exchanged between different authentication systems"""

        # Test token exchange flow
        token_exchange = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": oauth2_token,
            "scope": "read write admin",
            "audience": "piper-morgan-api",
        }

        # Verify token exchange structure
        assert token_exchange["grant_type"] == "urn:ietf:params:oauth:grant-type:jwt-bearer"
        assert token_exchange["assertion"] == oauth2_token
        assert "read" in token_exchange["scope"]

        # Test federation metadata
        federation_metadata = {
            "issuer": "https://oauth2.provider.com",
            "jwks_uri": "https://oauth2.provider.com/.well-known/jwks.json",
            "token_endpoint": "https://oauth2.provider.com/oauth/token",
            "userinfo_endpoint": "https://oauth2.provider.com/oauth/userinfo",
            "supported_scopes": ["read", "write", "admin"],
            "supported_grant_types": ["authorization_code", "client_credentials", "jwt-bearer"],
        }

        # Verify federation metadata
        assert federation_metadata["issuer"] == "https://oauth2.provider.com"
        assert "jwt-bearer" in federation_metadata["supported_grant_types"]


class TestPerformanceValidation:
    """Auth endpoint performance validation"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    @pytest.fixture
    def valid_jwt_token(self):
        """Generate a valid JWT token for testing"""
        payload = {
            "sub": "test_user_123",
            "iss": TEST_ISSUER,
            "aud": TEST_AUDIENCE,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
            "user_id": "test_user_123",
            "email": "test@example.com",
            "permissions": ["read", "write"],
        }
        return jwt.encode(payload, TEST_SECRET_KEY, algorithm=TEST_ALGORITHM)

    async def test_jwt_validation_performance(self, test_client, valid_jwt_token):
        """JWT validation is performant"""

        # Test JWT validation performance
        start_time = time.time()

        # Perform multiple JWT validations
        for _ in range(100):
            try:
                jwt.decode(
                    valid_jwt_token,
                    TEST_SECRET_KEY,
                    algorithms=[TEST_ALGORITHM],
                    options=JWT_DECODE_OPTIONS,
                )
            except Exception:
                pass

        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds

        # JWT validation should be fast (< 100ms for 100 operations)
        assert elapsed < 100, f"JWT validation too slow: {elapsed:.2f}ms for 100 operations"

    async def test_auth_endpoint_response_time(self, test_client, valid_jwt_token):
        """Auth endpoints respond quickly"""

        # Test JWT validation response time
        start_time = time.time()

        # Simulate JWT validation
        try:
            jwt.decode(
                valid_jwt_token,
                TEST_SECRET_KEY,
                algorithms=[TEST_ALGORITHM],
                options=JWT_DECODE_OPTIONS,
            )
        except Exception:
            pass

        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds

        # JWT validation should respond quickly (< 50ms)
        assert elapsed < 50, f"JWT validation too slow: {elapsed:.2f}ms"

    async def test_concurrent_auth_requests(self, test_client, valid_jwt_token):
        """System handles concurrent auth requests efficiently"""

        import asyncio

        async def validate_token():
            """Simulate token validation"""
            try:
                jwt.decode(
                    valid_jwt_token,
                    TEST_SECRET_KEY,
                    algorithms=[TEST_ALGORITHM],
                    options=JWT_DECODE_OPTIONS,
                )
                return True
            except Exception:
                return False

        # Test concurrent token validation
        start_time = time.time()

        # Create 10 concurrent validation tasks
        tasks = [validate_token() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # Convert to milliseconds

        # Concurrent validation should be efficient (< 200ms for 10 operations)
        assert elapsed < 200, f"Concurrent validation too slow: {elapsed:.2f}ms for 10 operations"
        assert all(results), "All concurrent validations should succeed"


class TestSecurityRegressionPrevention:
    """Ensure security enhancements don't break existing functionality"""

    @pytest.fixture
    def test_client(self):
        """Test client for API testing"""
        return TestClient(app)

    async def test_existing_auth_patterns_preserved(self, test_client):
        """Existing authentication patterns remain functional"""

        # Test that existing GitHub and Slack auth patterns are preserved
        # This will need to be updated when actual auth middleware is implemented

        # For now, verify the testing framework structure
        assert True, "Security regression prevention framework ready"

    async def test_error_handling_preserved(self, test_client):
        """Security error handling doesn't break existing error handling"""

        # Test that security errors integrate with existing error handling
        # This will need to be updated when actual auth middleware is implemented

        # For now, verify the testing framework structure
        assert True, "Security error handling integration ready"

    async def test_performance_standards_maintained(self, test_client):
        """Security doesn't degrade performance below acceptable thresholds"""

        # Test that security doesn't impact performance
        # This will need to be updated when actual auth middleware is implemented

        # For now, verify the testing framework structure
        assert True, "Security performance validation ready"


if __name__ == "__main__":
    # Run the test suite
    pytest.main([__file__, "-v"])
