"""
E2E: Authentication flow verification.

Tests the complete auth journey: login, token usage, and rejection of bad credentials.
Uses real database and real auth middleware — no mocking.

Issue: #352 TEST-SMOKE-E2E
"""

import pytest


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_login_returns_token_and_cookie(e2e_client, e2e_test_user):
    """Successful login returns JWT token in body and sets auth cookie."""
    _, username, password = e2e_test_user

    response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user_id" in data
    assert data["username"] == username

    # Auth cookie should be set
    assert "auth_token" in response.cookies


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_login_rejects_bad_password(e2e_client, e2e_test_user):
    """Login with wrong password returns 401."""
    _, username, _ = e2e_test_user

    response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "wrongpassword"},
    )

    assert response.status_code == 401


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_login_rejects_nonexistent_user(e2e_client):
    """Login with nonexistent user returns 401."""
    response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent_user_xyz", "password": "anypass"},
    )

    assert response.status_code == 401


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_authenticated_endpoint_with_cookie(e2e_client, e2e_test_user):
    """Authenticated endpoint works with auth cookie from login."""
    _, username, password = e2e_test_user

    # Login to get cookie
    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    cookies = login_response.cookies

    # Use cookie to access protected endpoint
    response = await e2e_client.get("/api/v1/projects", cookies=cookies)

    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert "count" in data


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_authenticated_endpoint_with_bearer_token(e2e_client, e2e_test_user):
    """Authenticated endpoint works with Bearer token from login."""
    _, username, password = e2e_test_user

    # Login to get token
    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    token = login_response.json()["token"]

    # Use Bearer token to access protected endpoint
    response = await e2e_client.get(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "projects" in data


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_protected_endpoint_rejects_unauthenticated(e2e_client):
    """Protected endpoint returns 401 without auth."""
    response = await e2e_client.get("/api/v1/projects")

    assert response.status_code == 401
