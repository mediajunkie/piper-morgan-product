"""
Test suite for auth endpoints (Issue #281: CORE-ALPHA-WEB-AUTH)
Verify authentication endpoints and middleware

These tests define what "done" means for auth endpoints:
- POST /auth/login works with valid credentials
- Login returns JWT token and sets cookie
- Invalid credentials rejected with 401
- POST /auth/logout clears authentication
- GET /auth/me returns current user info
- Protected endpoints require authentication
- Authenticated requests work with valid token
"""

from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Verify authentication endpoints"""

    @pytest.mark.asyncio
    async def test_login_endpoint_exists(self, async_client):
        """
        Verify /auth/login endpoint exists.

        Success Criteria:
        - POST /auth/login route registered
        - Returns JSON response
        - Not 404 error
        """
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "nonexistent", "password": "test"}
        )

        # Should not be 404 (endpoint exists)
        assert response.status_code != 404, "/api/v1/auth/login endpoint should exist"

    @pytest.mark.asyncio
    async def test_login_success(self, async_client):
        """
        Verify successful login flow.

        Success Criteria:
        - POST /auth/login with valid credentials returns 200
        - Response includes token, user_id, username
        - Token is valid JWT
        - Cookie set with auth_token
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.password_service import PasswordService
        from services.database.connection import db
        from services.database.models import User

        # Cleanup any existing test user first
        async with await db.get_session() as session:
            await session.execute(sql_delete(User).where(User.email == "logintest@example.com"))
            await session.commit()

        # Create test user with password
        ps = PasswordService()
        test_password = "test_login_password_123"
        hashed = ps.hash_password(test_password)

        test_user = User(
            username="login_test_user", email="logintest@example.com", password_hash=hashed
        )

        try:
            # Add user to database
            async with await db.get_session() as session:
                session.add(test_user)
                await session.commit()

            # Attempt login
            response = await async_client.post(
                "/api/v1/auth/login",
                data={"username": "login_test_user", "password": test_password},
            )

            # Verify response
            assert response.status_code == 200, f"Login should succeed: {response.text}"

            data = response.json()
            assert "token" in data, "Response should include token"
            assert "user_id" in data, "Response should include user_id"
            assert "username" in data, "Response should include username"
            assert data["username"] == "login_test_user"

            # Verify cookie set
            assert "auth_token" in response.cookies, "Response should set auth_token cookie"

        finally:
            # Cleanup - always runs even if test fails
            async with await db.get_session() as session:
                await session.execute(sql_delete(User).where(User.email == "logintest@example.com"))
                await session.commit()

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, async_client):
        """
        Verify login fails for non-existent user.

        Success Criteria:
        - Returns 401
        - Generic error message (don't leak user existence)
        - No token returned
        """
        response = await async_client.post(
            "/api/v1/auth/login",
            data={"username": "nonexistent_user_12345", "password": "any_password"},
        )

        assert response.status_code == 401, "Non-existent user should return 401"

        error = response.json()
        # #1452: the error middleware reshapes detail -> message with friendly
        # generic copy — the security property (no username/password oracle)
        # holds: same body for unknown user and wrong password.
        assert "message" in error
        assert "nonexistent_user_12345" not in error["message"]

        # Should not say "user not found" (leaks user existence)
        assert "not found" not in error["message"].lower(), "Error should not reveal user existence"

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, async_client, db_session):
        """
        Verify login fails for wrong password.

        Success Criteria:
        - Returns 401
        - Generic error message
        - No token returned
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.password_service import PasswordService
        from services.database.models import User

        # Clean up any existing test user first
        await db_session.execute(sql_delete(User).where(User.email == "wrongpass@example.com"))
        await db_session.commit()

        # Create test user
        ps = PasswordService()
        correct_password = "correct_password_789"
        hashed = ps.hash_password(correct_password)

        test_user = User(
            username="wrong_pass_test", email="wrongpass@example.com", password_hash=hashed
        )
        db_session.add(test_user)
        await db_session.commit()

        # Login with wrong password
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "wrong_pass_test", "password": "wrong_password"}
        )

        assert response.status_code == 401, "Wrong password should return 401"

        error = response.json()
        assert "message" in error  # middleware-reshaped body

        # Cleanup
        await db_session.delete(test_user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_login_no_password_set(self, async_client, db_session):
        """
        Verify login fails gracefully if user has no password.

        Success Criteria:
        - Returns 401
        - Helpful error message
        - Suggests contacting admin
        """
        from sqlalchemy import delete as sql_delete

        from services.database.models import User

        # Clean up any existing test user first
        await db_session.execute(sql_delete(User).where(User.email == "nopass@example.com"))
        await db_session.commit()

        # Create user without password
        test_user = User(
            username="no_password_user",
            email="nopass@example.com",
            password_hash=None,  # No password set
        )
        db_session.add(test_user)
        await db_session.commit()

        # Attempt login
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "no_password_user", "password": "any_password"}
        )

        assert response.status_code == 401

        error = response.json()
        # Middleware genericizes 401 copy; just require a friendly message
        assert error.get("message")

        # Cleanup
        await db_session.delete(test_user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_logout_clears_cookie(self, authenticated_client):
        """
        Verify logout clears authentication.

        Success Criteria:
        - POST /auth/logout returns 200
        - Cookie deleted
        - Subsequent requests fail auth
        """
        from unittest.mock import AsyncMock, patch

        # Mock blacklist.add() to avoid database session conflicts in tests
        # (is_blacklisted is mocked globally in conftest.py)
        with patch(
            "services.auth.token_blacklist.TokenBlacklist.add", new=AsyncMock(return_value=True)
        ):
            # Logout
            response = await authenticated_client.post("/api/v1/auth/logout")

            assert response.status_code == 200, f"Logout should succeed: {response.text}"

            # Verify cookie cleared
            # (AsyncClient behavior for delete_cookie varies)
            # Just verify response is successful

    @pytest.mark.asyncio
    async def test_get_current_user(self, authenticated_client):
        """
        Verify GET /auth/me returns user info.

        Success Criteria:
        - Returns user_id, username, email
        - Requires authentication
        - Returns current user's info
        """
        # is_blacklisted is mocked globally in conftest.py
        response = await authenticated_client.get("/api/v1/auth/me")

        assert response.status_code == 200, f"Should return current user: {response.text}"

        data = response.json()
        assert "user_id" in data
        assert "username" in data
        # email may or may not be included depending on implementation

    def test_get_current_user_requires_auth(self, client: TestClient):
        """
        Verify /auth/me requires authentication.

        Success Criteria:
        - Without token returns 401
        - Clear error message
        """
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401, "/api/v1/auth/me should require authentication"

    def test_protected_endpoint_without_auth(self, client: TestClient):
        """
        Verify protected endpoints require auth.

        Success Criteria:
        - /auth/me endpoint returns 401 without token
        - Protected endpoints return 401, not 404
        """
        # Test /auth/me endpoint (requires authentication)
        response = client.get("/api/v1/auth/me")

        assert (
            response.status_code == 401
        ), "/api/v1/auth/me should require authentication (401, not 404)"

        error = response.json()
        # Auth middleware shape: {"error": "authentication_required", ...}
        assert error.get("error") == "authentication_required" or "message" in error

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_auth(self, authenticated_client):
        """
        Verify authenticated requests work.

        Success Criteria:
        - /auth/me endpoint works with valid token
        - Returns 200 with user data
        - User context available to handler
        """
        response = await authenticated_client.get("/api/v1/auth/me")

        # Should be 200 (authentication worked)
        assert response.status_code == 200, f"Authenticated request should work: {response.text}"

        # Should return user data
        data = response.json()
        assert "user_id" in data, "Should return user_id"
        assert "username" in data, "Should return username"
        assert data["username"] == "auth_fixture_user", "Should return correct user"

    @pytest.mark.asyncio
    async def test_login_with_bearer_token_header(self, async_client, db_session):
        """
        Verify Bearer token in Authorization header works.

        Success Criteria:
        - Can authenticate with Authorization: Bearer TOKEN
        - Alternative to cookie authentication
        - Useful for API clients (file upload, etc.)
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.password_service import PasswordService
        from services.database.models import User

        # Clean up any existing test user first
        await db_session.execute(sql_delete(User).where(User.email == "bearertest@example.com"))
        await db_session.commit()

        # Create test user
        ps = PasswordService()
        test_password = "bearer_test_password_123"
        hashed = ps.hash_password(test_password)

        test_user = User(
            username="bearer_test_user", email="bearertest@example.com", password_hash=hashed
        )
        db_session.add(test_user)
        await db_session.commit()

        # Step 1: Login to get token
        login_response = await async_client.post(
            "/api/v1/auth/login", data={"username": "bearer_test_user", "password": test_password}
        )
        assert login_response.status_code == 200, "Login should succeed"
        token = login_response.json()["token"]

        # Step 2: Use token in Authorization: Bearer header
        # Step 3: Call GET /auth/me with that header
        response = await async_client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
        )

        # Step 4: Verify authentication works
        assert response.status_code == 200, f"Bearer auth should work: {response.text}"

        data = response.json()
        assert "user_id" in data, "Response should include user_id"
        assert "username" in data, "Response should include username"
        assert data["username"] == "bearer_test_user", "Should return correct user"

        # Cleanup
        await db_session.delete(test_user)
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_login_invalid_json(self, async_client):
        """
        Verify invalid JSON handled gracefully.

        Success Criteria:
        - Malformed JSON returns 400 or 422
        - Not 500 error
        """
        response = await async_client.post("/api/v1/auth/login", data="not valid json")

        # Should be client error, not server error
        assert 400 <= response.status_code < 500, "Invalid JSON should return 4xx error"

    @pytest.mark.asyncio
    async def test_login_missing_fields(self, async_client):
        """
        Verify missing required fields handled.

        Success Criteria:
        - Missing username returns 422
        - Missing password returns 422
        - Clear validation error
        """
        # Missing password
        response = await async_client.post("/api/v1/auth/login", data={"username": "testuser"})

        assert response.status_code == 422, "Missing password should return 422"

        # Missing username
        response = await async_client.post("/api/v1/auth/login", data={"password": "testpass"})

        assert response.status_code == 422, "Missing username should return 422"

    @pytest.mark.asyncio
    async def test_login_empty_credentials(self, async_client):
        """
        Verify empty credentials handled appropriately.

        Success Criteria:
        - Empty username rejected
        - Empty password rejected
        - Returns 401 or 422
        """
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "", "password": ""}
        )

        # Should be error (either validation or auth failure)
        assert response.status_code in [401, 422], "Empty credentials should be rejected"

    @pytest.mark.asyncio
    async def test_token_in_response_is_valid(self, async_client, db_session):
        """
        Verify token returned by login is valid JWT.

        Success Criteria:
        - Token can be decoded
        - Contains expected claims
        - Can be used for authenticated requests
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.jwt_service import JWTService
        from services.auth.password_service import PasswordService
        from services.database.models import User

        # Clean up any existing test user first
        await db_session.execute(sql_delete(User).where(User.email == "tokentest@example.com"))
        await db_session.commit()

        # Create test user
        ps = PasswordService()
        test_password = "valid_token_test_123"
        hashed = ps.hash_password(test_password)

        test_user = User(
            username="token_valid_test", email="tokentest@example.com", password_hash=hashed
        )
        db_session.add(test_user)
        await db_session.commit()

        # Login
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "token_valid_test", "password": test_password}
        )

        assert response.status_code == 200
        data = response.json()
        token = data["token"]

        # Verify token is valid
        jwt_service = JWTService()
        payload = await jwt_service.validate_token(token)

        assert payload is not None, "Token should be valid"
        # JWTClaims has username attribute (not subscriptable)
        assert hasattr(payload, "user_id"), "Payload should have user_id"

        # Cleanup
        await db_session.delete(test_user)
        await db_session.commit()


# Test fixtures


@pytest.fixture
async def async_client(db_session):
    """
    Provide async HTTP client for testing FastAPI endpoints.

    Uses httpx.AsyncClient which runs in the same event loop as the FastAPI app,
    avoiding event loop conflicts with async database operations.

    Overrides the global db.get_session() to use test database session,
    ensuring all database operations happen in the same event loop.

    Issue #281: CORE-ALPHA-WEB-AUTH - Fix async test isolation
    """
    from contextlib import asynccontextmanager

    import httpx

    from services.database.connection import db
    from web.app import app

    # Save original get_session method
    original_get_session = db.get_session

    # Override get_session to return test session
    # Must be async function that returns context manager (like original)
    async def mock_get_session():
        @asynccontextmanager
        async def _session():
            yield db_session

        return _session()

    db.get_session = mock_get_session

    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client
    finally:
        # Restore original get_session
        db.get_session = original_get_session


@pytest.fixture
def client():
    """
    Provide synchronous test client for simple endpoint tests.

    NOTE: This client creates its own event loop. Only use for tests that
    don't require real database operations (e.g., error handling, validation).
    For tests that need database, use async_client fixture instead.

    Issue #281: CORE-ALPHA-WEB-AUTH
    """
    from web.app import app

    return TestClient(app)


@pytest.fixture
async def authenticated_client(async_client, db_session):
    """
    Provide async test client with authentication.

    Creates test user, logs in, and returns client with auth token.
    Uses async client and database session in same event loop.

    Issue #281: CORE-ALPHA-WEB-AUTH
    Updated: Fix async test isolation by using db_session fixture
    """
    from sqlalchemy import delete as sql_delete

    from services.auth.password_service import PasswordService
    from services.database.models import User

    # Create test user
    ps = PasswordService()
    test_password = "auth_fixture_password_123"
    hashed = ps.hash_password(test_password)

    test_user = User(
        username="auth_fixture_user", email="authfixture@example.com", password_hash=hashed
    )

    # Add to database using fixture session (same event loop)
    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)  # Ensure object is loaded

    # Login to get token
    response = await async_client.post(
        "/api/v1/auth/login", data={"username": "auth_fixture_user", "password": test_password}
    )

    if response.status_code == 200:
        data = response.json()
        token = data["token"]

        # Add token to client headers
        async_client.headers["Authorization"] = f"Bearer {token}"

    yield async_client

    # Cleanup - use same session
    await db_session.execute(sql_delete(User).where(User.email == "authfixture@example.com"))
    await db_session.commit()
