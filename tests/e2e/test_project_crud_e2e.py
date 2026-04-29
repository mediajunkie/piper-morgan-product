"""
E2E: Project CRUD verification.

Tests the project management journey: login, create project, list projects,
verify persistence. Uses real database — no mocking.

Issue: #352 TEST-SMOKE-E2E
"""

import pytest
from sqlalchemy import text


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_create_and_list_project(e2e_client, e2e_test_user, e2e_db_session):
    """Create a project via API, then verify it appears in project list."""
    user_id, username, password = e2e_test_user

    # Login
    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200
    cookies = login_response.cookies

    # Create project
    create_response = await e2e_client.post(
        "/api/v1/projects",
        json={"name": "E2E Test Project", "description": "Created by E2E test"},
        cookies=cookies,
    )

    assert create_response.status_code == 200, f"Create failed: {create_response.text}"
    created = create_response.json()
    assert created["name"] == "E2E Test Project"
    project_id = created["id"]

    # List projects — should include our new project
    list_response = await e2e_client.get("/api/v1/projects", cookies=cookies)

    assert list_response.status_code == 200
    data = list_response.json()
    assert data["count"] >= 1

    project_names = [p["name"] for p in data["projects"]]
    assert "E2E Test Project" in project_names

    # Cleanup: delete project from database
    await e2e_db_session.execute(
        text("DELETE FROM projects WHERE id = :pid"),
        {"pid": project_id},
    )
    await e2e_db_session.commit()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_new_user_has_no_projects(e2e_client, e2e_test_user):
    """Freshly created user has 0 projects."""
    _, username, password = e2e_test_user

    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    cookies = login_response.cookies

    response = await e2e_client.get("/api/v1/projects", cookies=cookies)

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["projects"] == []


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_create_project_requires_name(e2e_client, e2e_test_user):
    """Creating a project without a name returns 400."""
    _, username, password = e2e_test_user

    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    cookies = login_response.cookies

    response = await e2e_client.post(
        "/api/v1/projects",
        json={"name": "", "description": "Missing name"},
        cookies=cookies,
    )

    assert response.status_code == 400


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_create_project_requires_auth(e2e_client):
    """Creating a project without auth returns 401."""
    response = await e2e_client.post(
        "/api/v1/projects",
        json={"name": "Unauthorized Project"},
    )

    assert response.status_code == 401
