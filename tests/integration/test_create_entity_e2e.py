"""
E2E Tests for Entity Create Workflows (Issue #468)

These tests verify the frontend→backend contract for create operations.
They use the same JSON body format as the frontend templates.

TDD: These tests are written FIRST and MUST FAIL against current code.
The bug: Backend expects query params, frontend sends JSON body.

Frontend sends:
    POST /api/v1/lists
    Content-Type: application/json
    {"name": "My List", "description": "Optional"}

Backend expects:
    POST /api/v1/lists?name=My%20List&description=Optional

This mismatch causes 422 errors that surface as "Unknown error" to users.

Run with: pytest tests/integration/test_create_entity_e2e.py -xvs
"""

from uuid import uuid4

import pytest
from httpx import AsyncClient

from services.auth.password_service import PasswordService
from services.database.models import User

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
async def authenticated_client(integration_db, real_client):
    """
    HTTP client with authenticated user via cookie.

    Mimics frontend auth flow:
    1. Create test user
    2. Login to get token
    3. Set auth_token cookie for subsequent requests

    Issue #468: Tests use JSON body (same as frontend)
    """
    unique_id = uuid4().hex[:8]

    # Create test user
    ps = PasswordService()
    test_password = "TestPass123!"
    hashed = ps.hash_password(test_password)

    test_user = User(
        username=f"e2e_create_user_{unique_id}",
        email=f"e2e_create_{unique_id}@example.com",
        password_hash=hashed,
    )

    integration_db.add(test_user)
    await integration_db.commit()
    await integration_db.refresh(test_user)

    # Login to get token (login endpoint uses Form data, not JSON)
    login_response = await real_client.post(
        "/api/v1/auth/login", data={"username": test_user.username, "password": test_password}
    )

    if login_response.status_code != 200:
        pytest.skip(f"Login failed: {login_response.text}")

    token = login_response.json().get("token")

    # Return client with auth header (same as cookie-based auth works via header)
    # The frontend uses cookies, but the middleware accepts both
    real_client.headers["Authorization"] = f"Bearer {token}"

    yield real_client

    # Cleanup happens via transaction rollback in integration_db fixture


# ============================================================================
# Test: List Create with JSON Body
# ============================================================================


@pytest.mark.integration
@pytest.mark.asyncio
class TestListCreateE2E:
    """E2E tests for POST /api/v1/lists with JSON body (Issue #468)"""

    async def test_create_list_with_json_body(self, authenticated_client):
        """
        Frontend sends JSON body - backend must accept it.

        This is the core test for Issue #468. The frontend template sends:
            fetch('/api/v1/lists', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name, description }),
                credentials: 'include'
            });

        Current behavior: 422 Unprocessable Entity (query params expected)
        Expected behavior: 200 OK with created list
        """
        response = await authenticated_client.post(
            "/api/v1/lists", json={"name": "E2E Test List", "description": "Created via JSON body"}
        )

        # This assertion MUST FAIL with current code (proving the bug)
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == "E2E Test List"
        assert data["description"] == "Created via JSON body"
        assert "id" in data
        assert "owner_id" in data

    async def test_create_list_name_only(self, authenticated_client):
        """
        Create list with only name (description optional).

        Frontend allows creating without description.
        """
        response = await authenticated_client.post("/api/v1/lists", json={"name": "Minimal List"})

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == "Minimal List"
        assert "id" in data

    async def test_create_list_appears_in_get(self, authenticated_client):
        """
        Created list must appear in GET /api/v1/lists.

        Verifies the full round-trip: create → list → find created item.
        """
        # Create
        create_response = await authenticated_client.post(
            "/api/v1/lists", json={"name": "Visibility Test List"}
        )

        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        list_id = create_response.json()["id"]

        # Verify in list
        list_response = await authenticated_client.get("/api/v1/lists")
        assert list_response.status_code == 200, f"List failed: {list_response.text}"

        lists = list_response.json().get("lists", [])
        assert any(
            l["id"] == list_id for l in lists
        ), f"Created list {list_id} not found in {lists}"

    async def test_create_list_empty_name_rejected(self, authenticated_client):
        """
        Empty name should return validation error (not 500).

        Frontend validates, but backend should too.
        """
        response = await authenticated_client.post(
            "/api/v1/lists", json={"name": "", "description": "No name provided"}
        )

        # Should get 400 (bad request) or 422 (validation error), not 500
        assert response.status_code in [
            400,
            422,
        ], f"Expected 400 or 422, got {response.status_code}"


# ============================================================================
# Test: Todo Create with JSON Body
# ============================================================================


@pytest.mark.integration
@pytest.mark.asyncio
class TestTodoCreateE2E:
    """E2E tests for POST /api/v1/todos with JSON body (Issue #468)"""

    async def test_create_todo_with_json_body(self, authenticated_client):
        """
        Frontend sends JSON body - backend must accept it.

        Template sends:
            fetch('/api/v1/todos', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title, description }),
                credentials: 'include'
            });
        """
        response = await authenticated_client.post(
            "/api/v1/todos", json={"title": "E2E Test Todo", "description": "Created via JSON body"}
        )

        # This assertion MUST FAIL with current code
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["title"] == "E2E Test Todo"
        assert "id" in data

    async def test_create_todo_title_only(self, authenticated_client):
        """Create todo with only title (description optional)."""
        response = await authenticated_client.post("/api/v1/todos", json={"title": "Minimal Todo"})

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["title"] == "Minimal Todo"
        assert "id" in data

    async def test_create_todo_appears_in_get(self, authenticated_client):
        """Created todo must appear in GET /api/v1/todos."""
        # Create
        create_response = await authenticated_client.post(
            "/api/v1/todos", json={"title": "Visibility Test Todo"}
        )

        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        todo_id = create_response.json()["id"]

        # Verify in list
        list_response = await authenticated_client.get("/api/v1/todos")
        assert list_response.status_code == 200, f"List failed: {list_response.text}"

        todos = list_response.json().get("todos", [])
        assert any(t["id"] == todo_id for t in todos), f"Created todo {todo_id} not found"


# ============================================================================
# Test: Project Create with JSON Body
# ============================================================================


@pytest.mark.integration
@pytest.mark.asyncio
class TestProjectCreateE2E:
    """E2E tests for POST /api/v1/projects with JSON body (Issue #468)"""

    async def test_create_project_with_json_body(self, authenticated_client):
        """
        Frontend sends JSON body - backend must accept it.

        Template sends:
            fetch('/api/v1/projects', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name, description }),
                credentials: 'include'
            });
        """
        response = await authenticated_client.post(
            "/api/v1/projects",
            json={"name": "E2E Test Project", "description": "Created via JSON body"},
        )

        # This assertion MUST FAIL with current code
        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == "E2E Test Project"
        assert "id" in data

    async def test_create_project_name_only(self, authenticated_client):
        """Create project with only name (description optional)."""
        response = await authenticated_client.post(
            "/api/v1/projects", json={"name": "Minimal Project"}
        )

        assert (
            response.status_code == 200
        ), f"Expected 200, got {response.status_code}: {response.text}"

        data = response.json()
        assert data["name"] == "Minimal Project"
        assert "id" in data

    async def test_create_project_appears_in_get(self, authenticated_client):
        """Created project must appear in GET /api/v1/projects."""
        # Create
        create_response = await authenticated_client.post(
            "/api/v1/projects", json={"name": "Visibility Test Project"}
        )

        assert create_response.status_code == 200, f"Create failed: {create_response.text}"
        project_id = create_response.json()["id"]

        # Verify in list
        list_response = await authenticated_client.get("/api/v1/projects")
        assert list_response.status_code == 200, f"List failed: {list_response.text}"

        projects = list_response.json().get("projects", [])
        assert any(
            p["id"] == project_id for p in projects
        ), f"Created project {project_id} not found"
