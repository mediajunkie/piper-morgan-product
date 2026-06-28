"""
Test suite for /api/v1/auth/refresh endpoint (Issue #857)

Verifies seamless token-refresh behavior:
- Refresh succeeds with a valid refresh-token cookie (returns new access token
  + rotates the refresh-token cookie)
- 401 with no refresh cookie
- 401 + cookies cleared with an invalid refresh token
- Refresh-token rotation: new refresh-cookie value differs from input
- /login issues both auth_token and refresh_token cookies with the documented
  cookie flags (httponly, samesite=lax, max-age=604800 for refresh)

Issue #857: INFRA token refresh mechanism for seamless session continuity.
"""

from contextlib import asynccontextmanager

import httpx
import pytest


class TestRefreshEndpoint:
    """Verify /api/v1/auth/refresh endpoint behavior (Issue #857)"""

    @pytest.mark.asyncio
    async def test_refresh_endpoint_succeeds_with_valid_refresh_token(
        self, async_client, db_session
    ):
        """
        Verify refresh succeeds and rotates tokens with a valid refresh cookie (#857).

        Success Criteria:
        - POST /api/v1/auth/refresh with valid refresh_token cookie returns 200
        - Response body includes a new `token` (access token)
        - Response sets new auth_token AND new refresh_token cookies
        - The new refresh-token cookie value differs from the input refresh token
        """
        from uuid import uuid4

        from sqlalchemy import delete as sql_delete

        from services.auth.jwt_service import JWTService
        from services.auth.password_service import PasswordService
        from services.database.models import User

        # Clean up any existing test user
        await db_session.execute(
            sql_delete(User).where(User.email == "refresh_success@example.com")
        )
        await db_session.commit()

        # Create test user (so the user_id in the refresh token corresponds to a real user)
        ps = PasswordService()
        test_user = User(
            username="refresh_success_user",
            email="refresh_success@example.com",
            password_hash=ps.hash_password("refresh_success_password_123"),
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        try:
            # Generate a valid refresh token directly via JWTService (no /login round-trip needed)
            jwt_service = JWTService()
            refresh_token = jwt_service.generate_refresh_token(
                user_id=test_user.id,
                user_email=test_user.email,
                username=test_user.username,
            )

            # Set the cookie on the async client and POST to /refresh
            async_client.cookies.set("refresh_token", refresh_token)
            response = await async_client.post("/api/v1/auth/refresh")

            assert response.status_code == 200, f"Refresh should succeed: {response.text}"

            data = response.json()
            assert "token" in data, "Response should include new access token"
            assert data["token"], "Access token should be non-empty"

            # Both cookies should be set on the response
            assert "auth_token" in response.cookies, "Response should set new auth_token cookie"
            assert (
                "refresh_token" in response.cookies
            ), "Response should set new refresh_token cookie"

            # Rotation: new refresh-token value differs from input
            assert (
                response.cookies["refresh_token"] != refresh_token
            ), "New refresh token should differ from input (rotation per #857 AC)"

        finally:
            async_client.cookies.clear()
            await db_session.execute(
                sql_delete(User).where(User.email == "refresh_success@example.com")
            )
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_refresh_endpoint_fails_with_no_refresh_token(self, async_client):
        """
        Verify refresh returns 401 when no refresh_token cookie is present (#857).

        Success Criteria:
        - POST /api/v1/auth/refresh with no cookie returns 401
        - Response includes a 401-shaped error body (the friendly-error handler from
          Issue #283 reshapes `{detail: ...}` → `{message: ...}` for end users; we
          accept either since the body schema is owned by the friendly-error layer)
        """
        # Ensure no refresh_token cookie is present
        async_client.cookies.clear()

        response = await async_client.post("/api/v1/auth/refresh")

        assert (
            response.status_code == 401
        ), f"Refresh with no cookie should return 401: {response.text}"

        error = response.json()
        # Accept either the raw {detail} shape OR the friendly {message} shape
        # (the #283 HTTPException handler reshapes 401s to {message} for end users).
        body_text = (error.get("detail") or error.get("message") or "").lower()
        assert body_text, f"401 body should include a detail or message field: {error!r}"

    @pytest.mark.asyncio
    async def test_refresh_endpoint_fails_with_invalid_refresh_token(self, async_client):
        """
        Verify refresh returns 401 for an invalid refresh token AND clears
        both auth cookies (#857 + #1078).

        Success Criteria:
        - POST /api/v1/auth/refresh with cookie set to "not-a-jwt" returns 401
        - 401 body present (detail or message shape)
        - Set-Cookie headers clear BOTH auth_token AND refresh_token

        #1078 closure: the refresh endpoint raises HTTPExceptionWithCookieClear
        with `clear_cookies=["auth_token", "refresh_token"]`. The #283
        friendly-error handler in web/app.py honors this subclass and applies
        delete_cookie to the rebuilt JSONResponse, so Set-Cookie headers
        actually reach the client.
        """
        async_client.cookies.clear()
        async_client.cookies.set("refresh_token", "not-a-jwt")

        try:
            response = await async_client.post("/api/v1/auth/refresh")

            assert (
                response.status_code == 401
            ), f"Invalid refresh token should return 401: {response.text}"

            error = response.json()
            body_text = (error.get("detail") or error.get("message") or "").lower()
            assert body_text, f"401 body should include detail or message: {error!r}"

            # #1078: Set-Cookie headers must clear both auth_token + refresh_token
            set_cookie_headers = [
                v.decode() if isinstance(v, bytes) else v
                for k, v in response.headers.raw
                if k.lower() == b"set-cookie"
            ]
            assert any(
                "auth_token=" in h for h in set_cookie_headers
            ), f"auth_token Set-Cookie missing on 401. Headers: {set_cookie_headers!r}"
            assert any(
                "refresh_token=" in h for h in set_cookie_headers
            ), f"refresh_token Set-Cookie missing on 401. Headers: {set_cookie_headers!r}"
            # Cookie-clearing semantics: delete_cookie sets Max-Age=0 (or empty value)
            for cookie_name in ("auth_token", "refresh_token"):
                matching = [h for h in set_cookie_headers if h.startswith(f"{cookie_name}=")]
                assert matching, f"{cookie_name} clear header missing"
                # delete_cookie emits Max-Age=0
                assert any("Max-Age=0" in h or "expires=" in h.lower() for h in matching), (
                    f"{cookie_name} should be cleared (Max-Age=0 or expires-past). "
                    f"Got: {matching!r}"
                )
        finally:
            async_client.cookies.clear()

    @pytest.mark.asyncio
    async def test_refresh_endpoint_rotates_refresh_token(self, async_client, db_session):
        """
        Verify refresh token rotation: new refresh cookie value differs from input (#857).

        Load-bearing for the rotation acceptance criterion. Even when the access token
        is regenerated, the refresh token MUST also be regenerated on every successful
        refresh so that a stolen refresh token has a single-use window.

        Success Criteria:
        - New refresh_token cookie value DIFFERS from the input refresh token
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.jwt_service import JWTService
        from services.auth.password_service import PasswordService
        from services.database.models import User

        await db_session.execute(sql_delete(User).where(User.email == "refresh_rotate@example.com"))
        await db_session.commit()

        ps = PasswordService()
        test_user = User(
            username="refresh_rotate_user",
            email="refresh_rotate@example.com",
            password_hash=ps.hash_password("refresh_rotate_password_123"),
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        try:
            jwt_service = JWTService()
            input_refresh_token = jwt_service.generate_refresh_token(
                user_id=test_user.id,
                user_email=test_user.email,
                username=test_user.username,
            )

            async_client.cookies.set("refresh_token", input_refresh_token)
            response = await async_client.post("/api/v1/auth/refresh")

            assert (
                response.status_code == 200
            ), f"Refresh should succeed for rotation check: {response.text}"

            new_refresh_token = response.cookies.get("refresh_token")
            assert new_refresh_token is not None, "Response must set new refresh_token cookie"
            assert (
                new_refresh_token != input_refresh_token
            ), "Rotation AC: new refresh-cookie value MUST differ from input refresh token"

        finally:
            async_client.cookies.clear()
            await db_session.execute(
                sql_delete(User).where(User.email == "refresh_rotate@example.com")
            )
            await db_session.commit()

    @pytest.mark.asyncio
    async def test_login_now_issues_refresh_token_cookie(self, async_client, db_session):
        """
        Verify /api/v1/auth/login now issues a refresh_token cookie alongside auth_token (#857).

        Success Criteria:
        - POST /api/v1/auth/login with valid creds sets refresh_token cookie
        - refresh_token cookie has httponly=true, samesite=lax, max-age=604800 (7 days)
        - auth_token cookie still set (existing behavior preserved)
        """
        from sqlalchemy import delete as sql_delete

        from services.auth.password_service import PasswordService
        from services.database.models import User

        await db_session.execute(sql_delete(User).where(User.email == "refresh_login@example.com"))
        await db_session.commit()

        ps = PasswordService()
        test_password = "refresh_login_password_123"
        test_user = User(
            username="refresh_login_user",
            email="refresh_login@example.com",
            password_hash=ps.hash_password(test_password),
        )
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        try:
            async_client.cookies.clear()
            response = await async_client.post(
                "/api/v1/auth/login",
                data={"username": "refresh_login_user", "password": test_password},
            )

            assert response.status_code == 200, f"Login should succeed: {response.text}"

            # Both cookies must be present
            assert (
                "auth_token" in response.cookies
            ), "Login should still set auth_token cookie (preserved behavior)"
            assert (
                "refresh_token" in response.cookies
            ), "Login should now set refresh_token cookie (#857)"

            # Verify refresh_token cookie flags by inspecting Set-Cookie headers
            set_cookie_headers = (
                response.headers.get_list("set-cookie")
                if hasattr(response.headers, "get_list")
                else [v.decode() for k, v in response.headers.raw if k.lower() == b"set-cookie"]
            )
            if set_cookie_headers and isinstance(set_cookie_headers[0], tuple):
                set_cookie_strs = [v.decode() for k, v in set_cookie_headers]
            else:
                set_cookie_strs = list(set_cookie_headers)

            # Find the refresh_token Set-Cookie line
            refresh_header = next(
                (h for h in set_cookie_strs if h.lower().startswith("refresh_token=")),
                None,
            )
            assert (
                refresh_header is not None
            ), f"refresh_token Set-Cookie header missing. Headers: {set_cookie_strs!r}"

            refresh_header_lower = refresh_header.lower()
            assert (
                "httponly" in refresh_header_lower
            ), f"refresh_token cookie should be HttpOnly: {refresh_header!r}"
            assert (
                "samesite=lax" in refresh_header_lower
            ), f"refresh_token cookie should have SameSite=Lax: {refresh_header!r}"
            assert (
                "max-age=604800" in refresh_header_lower
            ), f"refresh_token cookie should have Max-Age=604800 (7 days): {refresh_header!r}"

        finally:
            async_client.cookies.clear()
            await db_session.execute(
                sql_delete(User).where(User.email == "refresh_login@example.com")
            )
            await db_session.commit()


# Test fixtures
# Mirrors tests/auth/test_auth_endpoints.py — async client + db_session override
# (Issue #281 / #921 pattern: AsyncClient + ASGITransport + overridden db.get_session).


@pytest.fixture
async def async_client(db_session):
    """
    Provide async HTTP client for testing FastAPI endpoints (#857).

    Overrides global db.get_session() to use the test session so all DB operations
    happen in the same event loop. Mirrors the fixture in test_auth_endpoints.py.
    """
    from services.database.connection import db
    from web.app import app

    original_get_session = db.get_session

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
        db.get_session = original_get_session
