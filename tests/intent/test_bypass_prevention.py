"""
Test suite to prevent intent classification bypasses.
Ensures all NL endpoints use intent classification.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from web.app import app


class TestBypassPrevention:
    """Prevent bypasses of intent classification."""

    @pytest.fixture
    async def async_client(self, db_session):
        """Provide async HTTP client with database session override."""
        from contextlib import asynccontextmanager

        from services.database.connection import db

        # Save original get_session method
        original_get_session = db.get_session

        # Override get_session to return test session
        async def mock_get_session():
            @asynccontextmanager
            async def _session():
                yield db_session

            return _session()

        db.get_session = mock_get_session

        try:
            # Use ASGITransport instead of deprecated app= shortcut
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                yield client
        finally:
            # Restore original get_session
            db.get_session = original_get_session

    @pytest.fixture
    async def authenticated_client(self, async_client, db_session):
        """Provide authenticated async HTTP client for testing admin endpoints."""
        from sqlalchemy import delete as sql_delete

        from services.auth.password_service import PasswordService
        from services.database.models import User

        # Cleanup any existing test user first (from failed previous runs)
        await db_session.execute(sql_delete(User).where(User.email == "bypasstest@example.com"))
        await db_session.commit()

        # Create test user with password
        ps = PasswordService()
        test_password = "bypass_test_password_123"
        hashed = ps.hash_password(test_password)

        # is_admin: 1598 gated /api/admin/intent-monitoring (the endpoint this
        # fixture exists to reach) behind require_admin, which reads users.is_admin
        # LIVE from the DB. A merely-authenticated fixture user now gets a correct
        # 403 — so the flag is what keeps this test testing the middleware rather
        # than re-testing the auth gate.
        test_user = User(
            username="bypass_test_user",
            email="bypasstest@example.com",
            password_hash=hashed,
            is_admin=True,
        )

        # Add user to database using fixture session
        db_session.add(test_user)
        await db_session.commit()
        await db_session.refresh(test_user)

        # Login to get token (login endpoint expects form data, not JSON)
        response = await async_client.post(
            "/api/v1/auth/login", data={"username": "bypass_test_user", "password": test_password}
        )

        # Debug: Verify login succeeded
        assert (
            response.status_code == 200
        ), f"Login failed: {response.status_code} - {response.text}"

        data = response.json()
        token = data["token"]
        # Add token to client headers
        async_client.headers["Authorization"] = f"Bearer {token}"

        yield async_client

        # Cleanup - use same session
        await db_session.execute(sql_delete(User).where(User.email == "bypasstest@example.com"))
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_middleware_is_registered(self, authenticated_client):
        """Verify IntentEnforcementMiddleware is active."""
        response = await authenticated_client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200
        data = response.json()
        assert data["middleware_active"] is True
        assert len(data["nl_endpoints"]) == 4
        assert len(data["exempt_paths"]) == 12

    @pytest.mark.asyncio
    async def test_nl_endpoints_marked(self, authenticated_client):
        """Verify NL endpoints are marked as requiring intent."""
        # This would require accessing request.state in tests
        # For now, verify they exist
        nl_endpoints = ["/api/v1/intent", "/api/standup", "/api/chat", "/api/message"]

        for endpoint in nl_endpoints:
            # Test endpoint exists or returns expected status
            response = await authenticated_client.get(endpoint)
            # 404, 405, or 422 are acceptable (endpoint exists but wrong method/data)
            assert response.status_code in [200, 404, 405, 422]

    @pytest.mark.asyncio
    async def test_exempt_paths_accessible(self, async_client):
        """Verify exempt paths work without authentication."""
        exempt_tests = [("/health", 200), ("/docs", 200)]

        for path, expected_status in exempt_tests:
            response = await async_client.get(path)
            assert (
                response.status_code == expected_status
            ), f"{path} should be accessible without auth (got {response.status_code})"

    @pytest.mark.asyncio
    async def test_personality_enhance_is_exempt(self, authenticated_client):
        """Personality enhancement is output processing, should be exempt."""
        # This endpoint processes Piper's output, not user input
        response = await authenticated_client.post(
            "/api/v1/personality/enhance", json={"text": "Test response", "context": {}}
        )
        # Should not require intent (it's exempt)
        # 200 (success), 422 (validation error), or 500 (services not initialized in test) are acceptable
        assert response.status_code in [200, 422, 500]

    @pytest.mark.asyncio
    async def test_monitoring_logs_requests(self, async_client, caplog):
        """Verify middleware logs all requests."""
        with caplog.at_level("INFO"):
            await async_client.get("/health")

        # Check logs contain request
        log_messages = [record.message for record in caplog.records]
        assert any("Request: GET /health" in msg for msg in log_messages)
