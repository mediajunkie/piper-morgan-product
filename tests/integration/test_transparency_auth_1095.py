"""Auth-gate tests for #1095 (transparency endpoints user-binding + admin checks).

Verifies that the transparency router (wired in #1075) now enforces:
- audit-log + audit-summary: JWT user must own the session_id per ConversationDB
  (or have is_admin=True). Cross-user access returns 403.
- stats + cleanup + health: require is_admin=True. Without it, 403.
- Without any JWT, all endpoints return 401 (auth middleware).

Tests mock AsyncSessionFactory in the transparency module rather than
exercising the real DB — focused on the auth-gate logic, not the
audit_transparency persistence (covered by #1018 tests).

Pattern-071 (Audit Logs as Attack Surface) concrete fix coverage.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from tests.conftest import TEST_USER_ID, TEST_USER_ID_2


@pytest.fixture
def client():
    from web.app import app

    return TestClient(app)


@pytest.fixture
def jwt_svc():
    """Local JWTService instance for minting test tokens."""
    return JWTService()


def _mint_token(jwt_svc, user_id=TEST_USER_ID, username="testuser", **extra):
    """Mint a JWT for the given user. Mirrors tests/auth/test_jwt_service.py helper."""
    return jwt_svc.generate_access_token(
        user_id=user_id,
        user_email=f"{username}@test.local",
        scopes=["api:user"],
        username=username,
        **extra,
    )


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _mock_session_lookup(owner_user_id):
    """Patch AsyncSessionFactory in transparency module to return a session
    owned by `owner_user_id`. Returns the patcher (use as context manager)."""
    # Build a mock ConversationDB row with .user_id = owner_user_id
    mock_conv = MagicMock()
    mock_conv.user_id = str(owner_user_id)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_conv

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)

    patcher = patch("services.api.transparency.AsyncSessionFactory")
    return patcher, mock_ctx


def _mock_session_not_found():
    """Patch session factory to return no session for the lookup (session doesn't exist)."""
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_session = AsyncMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
    mock_ctx.__aexit__ = AsyncMock(return_value=None)

    patcher = patch("services.api.transparency.AsyncSessionFactory")
    return patcher, mock_ctx


class TestUserScopedEndpoints:
    """audit-log + audit-summary: require session ownership."""

    def test_audit_log_403_when_not_owner(self, client, jwt_svc):
        """User A's JWT cannot retrieve user B's session audit log."""
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        # Session is owned by user 2; requester is user 1
        patcher, mock_ctx = _mock_session_lookup(TEST_USER_ID_2)
        with patcher as MockFactory:
            MockFactory.session_scope_fresh.return_value = mock_ctx
            response = client.get(
                "/api/v1/transparency/audit-log/some-session-id",
                headers=_auth(token),
            )
        assert response.status_code == 403, (
            f"Cross-user access must be blocked; got {response.status_code} "
            f"body={response.json() if response.content else 'empty'}"
        )

    def test_audit_summary_403_when_not_owner(self, client, jwt_svc):
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        patcher, mock_ctx = _mock_session_lookup(TEST_USER_ID_2)
        with patcher as MockFactory:
            MockFactory.session_scope_fresh.return_value = mock_ctx
            response = client.get(
                "/api/v1/transparency/audit-summary/some-session-id",
                headers=_auth(token),
            )
        assert response.status_code == 403

    def test_audit_log_403_when_session_not_found(self, client, jwt_svc):
        """Non-existent session returns 403 (uniform — don't leak existence)."""
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        patcher, mock_ctx = _mock_session_not_found()
        with patcher as MockFactory:
            MockFactory.session_scope_fresh.return_value = mock_ctx
            response = client.get(
                "/api/v1/transparency/audit-log/nonexistent-session",
                headers=_auth(token),
            )
        # Uniform 403 (Pattern-071 — don't differentiate from "not yours")
        assert response.status_code == 403


class TestAdminScopedEndpoints:
    """stats + cleanup + health: require is_admin=True."""

    def test_stats_403_without_admin(self, client, jwt_svc):
        """Non-admin user gets 403 on stats endpoint."""
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        response = client.get(
            "/api/v1/transparency/stats", headers=_auth(token)
        )
        assert response.status_code == 403, (
            f"Non-admin should get 403; got {response.status_code}"
        )

    def test_cleanup_403_without_admin(self, client, jwt_svc):
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        response = client.post(
            "/api/v1/transparency/cleanup", headers=_auth(token)
        )
        assert response.status_code == 403

    def test_health_403_without_admin(self, client, jwt_svc):
        token = _mint_token(jwt_svc, user_id=TEST_USER_ID)
        response = client.get(
            "/api/v1/transparency/health", headers=_auth(token)
        )
        assert response.status_code == 403


class TestUnauthenticated:
    """All endpoints reject unauthenticated requests at the auth middleware."""

    def test_audit_log_401_without_jwt(self, client):
        response = client.get("/api/v1/transparency/audit-log/x")
        assert response.status_code == 401

    def test_audit_summary_401_without_jwt(self, client):
        response = client.get("/api/v1/transparency/audit-summary/x")
        assert response.status_code == 401

    def test_stats_401_without_jwt(self, client):
        response = client.get("/api/v1/transparency/stats")
        assert response.status_code == 401

    def test_cleanup_401_without_jwt(self, client):
        response = client.post("/api/v1/transparency/cleanup")
        assert response.status_code == 401

    def test_health_401_without_jwt(self, client):
        response = client.get("/api/v1/transparency/health")
        assert response.status_code == 401
