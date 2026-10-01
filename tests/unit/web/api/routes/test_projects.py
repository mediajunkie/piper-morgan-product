"""
Tests for projects API routes.

Issue #672: MUX-WIRE-PROJECTS-PAGE - Ensures /projects endpoint
falls back to user preferences when projects table is empty.
"""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@dataclass
class MockJWTClaims:
    """Minimal JWT claims mock for testing."""

    sub: str
    user_id: str = None
    user_email: str = "test@example.com"

    def __post_init__(self):
        if self.user_id is None:
            self.user_id = self.sub


class TestProjectsListRoute:
    """Tests for GET /api/v1/projects endpoint."""

    @pytest.fixture
    def mock_current_user(self):
        """Create mock JWT claims for authenticated user."""
        user_id = str(uuid4())
        return MockJWTClaims(sub=user_id)

    @pytest.fixture
    def mock_project(self, mock_current_user):
        """Create a mock project domain object."""
        project = MagicMock()
        project.id = str(uuid4())
        project.name = "Test Project"
        project.description = "A test project"
        project.owner_id = mock_current_user.sub
        project.created_at = None
        return project

    @pytest.fixture
    def mock_project_repo(self):
        """Create a mock project repository."""
        repo = MagicMock()
        repo.list_active_projects = AsyncMock(return_value=[])
        return repo

    @pytest.mark.smoke
    def test_list_projects_from_database(self, mock_current_user, mock_project, mock_project_repo):
        """Test that projects are returned from database when available."""
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Configure mock to return a project
        mock_project_repo.list_active_projects = AsyncMock(return_value=[mock_project])

        # Create test app with mocked dependencies
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["projects"][0]["name"] == "Test Project"
        assert data["source"] == "database"

    @pytest.mark.smoke
    def test_list_projects_fallback_to_preferences(self, mock_current_user, mock_project_repo):
        """Test that projects fall back to user preferences when DB is empty - Issue #672."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock empty database
        mock_project_repo.list_active_projects = AsyncMock(return_value=[])

        # Mock user context with projects from preferences
        mock_user_context = MagicMock()
        mock_user_context.projects = ["Project A", "Project B", "Project C"]

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert data["source"] == "preferences"
        # Check project names
        names = [p["name"] for p in data["projects"]]
        assert "Project A" in names
        assert "Project B" in names
        assert "Project C" in names

    @pytest.mark.smoke
    def test_list_projects_empty_when_no_fallback(self, mock_current_user, mock_project_repo):
        """Test that empty list is returned when both DB and preferences are empty."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock empty database
        mock_project_repo.list_active_projects = AsyncMock(return_value=[])

        # Mock user context with no projects
        mock_user_context = MagicMock()
        mock_user_context.projects = []

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["projects"] == []
        # source is "database" because we didn't convert any preferences
        assert data["source"] == "database"

    @pytest.mark.smoke
    def test_database_projects_take_precedence(
        self, mock_current_user, mock_project, mock_project_repo
    ):
        """Test that database projects are used over preferences when both exist."""
        from unittest.mock import patch

        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        # Mock database with project
        mock_project_repo.list_active_projects = AsyncMock(return_value=[mock_project])

        # Mock user context with different projects (should be ignored)
        mock_user_context = MagicMock()
        mock_user_context.projects = ["Preference Project"]

        # Create test app
        app = FastAPI()
        app.include_router(router)

        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo

        client = TestClient(app)

        with patch(
            "services.user_context_service.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            response = client.get("/api/v1/projects")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["source"] == "database"
        assert data["projects"][0]["name"] == "Test Project"


class TestDeleteProjectRoute1912:
    """Tests for DELETE /api/v1/projects/{project_id} (Issue #1912).

    #1912: PM clicked Remove in the UI and got a success toast over a
    no-op — the TEMPLATE never called this route at all (the fetch was
    commented out). These tests pin the ROUTE layer: it already does the
    right thing (owner-scoped hard delete, honest 404/500), so the fix
    is template-side; this class guards against the route regressing
    while the template is wired up to actually call it.
    """

    @pytest.fixture
    def mock_current_user(self):
        user_id = str(uuid4())
        return MockJWTClaims(sub=user_id)

    @pytest.fixture
    def mock_project(self, mock_current_user):
        project = MagicMock()
        project.id = str(uuid4())
        project.name = "One Job"
        project.owner_id = mock_current_user.sub
        return project

    @pytest.fixture
    def mock_project_repo(self, mock_project):
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_project)
        repo.delete = AsyncMock(return_value=True)
        return repo

    @pytest.fixture
    def app_and_client(self, mock_current_user, mock_project_repo):
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_repository
        from web.api.routes.projects import router

        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo
        client = TestClient(app)
        return app, client

    @pytest.mark.smoke
    def test_delete_success_returns_deleted_status_and_project_id(
        self, app_and_client, mock_project, mock_project_repo
    ):
        """The honest-success shape the template must check the BODY
        for — not status code alone (#1912)."""
        _, client = app_and_client

        response = client.delete(f"/api/v1/projects/{mock_project.id}")

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "deleted"
        assert body["project_id"] == mock_project.id
        mock_project_repo.delete.assert_awaited_once_with(mock_project.id)

    def test_delete_is_owner_scoped(
        self, app_and_client, mock_project, mock_project_repo, mock_current_user
    ):
        """get_by_id must be called with the caller's owner_id — a
        mismatched owner must not be able to delete another user's
        project."""
        _, client = app_and_client

        client.delete(f"/api/v1/projects/{mock_project.id}")

        mock_project_repo.get_by_id.assert_awaited_once_with(
            mock_project.id, owner_id=mock_current_user.sub
        )

    def test_delete_not_found_or_not_owned_is_404_and_does_not_delete(
        self, app_and_client, mock_project_repo
    ):
        """Project missing, already gone, or owned by someone else —
        all look identical from this repo call (get_by_id returns
        None) and must 404, never silently succeed."""
        mock_project_repo.get_by_id = AsyncMock(return_value=None)
        _, client = app_and_client

        response = client.delete(f"/api/v1/projects/{uuid4()}")

        assert response.status_code == 404
        mock_project_repo.delete.assert_not_called()

    def test_delete_repo_failure_returns_500_not_a_silent_success(
        self, app_and_client, mock_project, mock_project_repo
    ):
        """If the delete itself raises, the route must surface a real
        error — never a 200 the template could mistake for success."""
        mock_project_repo.delete = AsyncMock(side_effect=RuntimeError("db exploded"))
        _, client = app_and_client

        response = client.delete(f"/api/v1/projects/{mock_project.id}")

        assert response.status_code == 500


class TestProjectIntegrationEndpoints859:
    """Tests for project integration CRUD endpoints (Issue #859)."""

    @pytest.fixture
    def mock_current_user(self):
        user_id = str(uuid4())
        return MockJWTClaims(sub=user_id)

    @pytest.fixture
    def mock_project(self, mock_current_user):
        project = MagicMock()
        project.id = str(uuid4())
        project.name = "Test Project"
        project.owner_id = mock_current_user.sub
        return project

    @pytest.fixture
    def mock_project_repo(self, mock_project):
        repo = MagicMock()
        repo.get_by_id = AsyncMock(return_value=mock_project)
        return repo

    @pytest.fixture
    def mock_integration(self, mock_project):
        """Create a mock integration DB object (BaseRepository.get_by_id returns DB model)."""
        from services.shared_types import IntegrationType

        integration = MagicMock()
        integration.id = str(uuid4())
        integration.project_id = mock_project.id
        integration.type = IntegrationType.GITHUB
        integration.name = "Main Repository"
        integration.config = {"repository": "owner/repo"}
        integration.is_active = True
        integration.created_at = None
        # to_domain() returns a domain object
        domain_obj = MagicMock()
        domain_obj.id = integration.id
        domain_obj.type = IntegrationType.GITHUB
        domain_obj.name = "Main Repository"
        domain_obj.config = {"repository": "owner/repo"}
        domain_obj.is_active = True
        domain_obj.created_at = None
        integration.to_domain.return_value = domain_obj
        return integration

    @pytest.fixture
    def mock_integration_repo(self):
        repo = MagicMock()
        repo.list_by_project = AsyncMock(return_value=[])
        repo.get_by_project_and_type = AsyncMock(return_value=None)
        repo.get_by_id = AsyncMock(return_value=None)
        repo.create = AsyncMock()
        repo.update = AsyncMock()
        repo.delete = AsyncMock(return_value=True)
        return repo

    @pytest.fixture
    def app_and_client(self, mock_current_user, mock_project_repo, mock_integration_repo):
        from services.auth.auth_middleware import get_current_user
        from web.api.dependencies import get_project_integration_repository, get_project_repository
        from web.api.routes.projects import router

        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_current_user] = lambda: mock_current_user
        app.dependency_overrides[get_project_repository] = lambda: mock_project_repo
        app.dependency_overrides[get_project_integration_repository] = lambda: mock_integration_repo
        client = TestClient(app)
        return app, client

    # --- LIST ---

    def test_list_integrations_empty(self, app_and_client, mock_project):
        _, client = app_and_client
        response = client.get(f"/api/v1/projects/{mock_project.id}/integrations")
        assert response.status_code == 200
        data = response.json()
        assert data["project_id"] == mock_project.id
        assert data["integrations"] == []

    def test_list_integrations_with_results(
        self, app_and_client, mock_project, mock_integration_repo
    ):
        from services.shared_types import IntegrationType

        domain_integration = MagicMock()
        domain_integration.id = str(uuid4())
        domain_integration.type = IntegrationType.GITHUB
        domain_integration.name = "Main Repo"
        domain_integration.config = {"repository": "owner/repo"}
        domain_integration.is_active = True
        domain_integration.created_at = None
        mock_integration_repo.list_by_project = AsyncMock(return_value=[domain_integration])

        _, client = app_and_client
        response = client.get(f"/api/v1/projects/{mock_project.id}/integrations")
        assert response.status_code == 200
        data = response.json()
        assert len(data["integrations"]) == 1
        assert data["integrations"][0]["type"] == "github"
        assert data["integrations"][0]["name"] == "Main Repo"

    def test_list_integrations_project_not_found(self, app_and_client, mock_project_repo):
        mock_project_repo.get_by_id = AsyncMock(return_value=None)
        _, client = app_and_client
        response = client.get(f"/api/v1/projects/{uuid4()}/integrations")
        assert response.status_code == 404

    # --- CREATE ---

    def test_create_integration_success(self, app_and_client, mock_project, mock_integration_repo):
        created = MagicMock()
        created.id = str(uuid4())
        created.created_at = None
        mock_integration_repo.create = AsyncMock(return_value=created)

        _, client = app_and_client
        response = client.post(
            f"/api/v1/projects/{mock_project.id}/integrations",
            json={"type": "github", "name": "Main Repo", "config": {"repository": "owner/repo"}},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "github"
        assert data["name"] == "Main Repo"
        assert data["config"] == {"repository": "owner/repo"}

    def test_create_integration_invalid_type(self, app_and_client, mock_project):
        _, client = app_and_client
        response = client.post(
            f"/api/v1/projects/{mock_project.id}/integrations",
            json={"type": "invalid", "name": "Bad", "config": {}},
        )
        assert response.status_code == 400
        assert "Invalid integration type" in response.json()["detail"]

    def test_create_integration_invalid_config(self, app_and_client, mock_project):
        _, client = app_and_client
        response = client.post(
            f"/api/v1/projects/{mock_project.id}/integrations",
            json={"type": "github", "name": "No Repo Key", "config": {"wrong": "key"}},
        )
        assert response.status_code == 400
        assert "Invalid config" in response.json()["detail"]

    def test_create_integration_duplicate_type(
        self, app_and_client, mock_project, mock_integration_repo
    ):
        mock_integration_repo.get_by_project_and_type = AsyncMock(return_value=MagicMock())
        _, client = app_and_client
        response = client.post(
            f"/api/v1/projects/{mock_project.id}/integrations",
            json={"type": "github", "name": "Dup", "config": {"repository": "owner/repo"}},
        )
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_create_integration_project_not_found(self, app_and_client, mock_project_repo):
        mock_project_repo.get_by_id = AsyncMock(return_value=None)
        _, client = app_and_client
        response = client.post(
            f"/api/v1/projects/{uuid4()}/integrations",
            json={"type": "github", "name": "X", "config": {"repository": "o/r"}},
        )
        assert response.status_code == 404

    # --- GET ---

    def test_get_integration_success(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        _, client = app_and_client
        response = client.get(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_integration.id
        assert data["type"] == "github"

    def test_get_integration_not_found(self, app_and_client, mock_project):
        _, client = app_and_client
        response = client.get(f"/api/v1/projects/{mock_project.id}/integrations/{uuid4()}")
        assert response.status_code == 404

    def test_get_integration_wrong_project(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        """Integration exists but belongs to different project."""
        mock_integration.project_id = str(uuid4())  # Different project
        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        _, client = app_and_client
        response = client.get(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}"
        )
        assert response.status_code == 404

    # --- UPDATE ---

    def test_update_integration_name(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        from services.shared_types import IntegrationType

        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        updated = MagicMock()
        updated.id = mock_integration.id
        updated.type = IntegrationType.GITHUB
        updated.name = "Renamed Repo"
        updated.config = {"repository": "owner/repo"}
        updated.is_active = True
        updated.created_at = None
        mock_integration_repo.update = AsyncMock(return_value=updated)

        _, client = app_and_client
        response = client.put(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}",
            json={"name": "Renamed Repo"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Renamed Repo"

    def test_update_integration_invalid_config(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        _, client = app_and_client
        response = client.put(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}",
            json={"config": {"wrong": "key"}},
        )
        assert response.status_code == 400
        assert "Invalid config" in response.json()["detail"]

    def test_update_integration_empty_body(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        _, client = app_and_client
        response = client.put(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}",
            json={},
        )
        assert response.status_code == 400
        assert "No fields to update" in response.json()["detail"]

    # --- DELETE ---

    def test_delete_integration_success(
        self, app_and_client, mock_project, mock_integration, mock_integration_repo
    ):
        mock_integration_repo.get_by_id = AsyncMock(return_value=mock_integration)
        _, client = app_and_client
        response = client.delete(
            f"/api/v1/projects/{mock_project.id}/integrations/{mock_integration.id}"
        )
        assert response.status_code == 200
        assert response.json()["deleted"] is True

    def test_delete_integration_not_found(self, app_and_client, mock_project):
        _, client = app_and_client
        response = client.delete(f"/api/v1/projects/{mock_project.id}/integrations/{uuid4()}")
        assert response.status_code == 404

    # --- OWNERSHIP VERIFICATION ---

    def test_all_endpoints_verify_project_ownership(self, app_and_client, mock_project_repo):
        """All integration endpoints should return 404 when project not owned by user."""
        mock_project_repo.get_by_id = AsyncMock(return_value=None)
        _, client = app_and_client
        fake_pid = str(uuid4())
        fake_iid = str(uuid4())

        assert client.get(f"/api/v1/projects/{fake_pid}/integrations").status_code == 404
        assert (
            client.post(
                f"/api/v1/projects/{fake_pid}/integrations",
                json={"type": "github", "name": "X", "config": {"repository": "o/r"}},
            ).status_code
            == 404
        )
        assert client.get(f"/api/v1/projects/{fake_pid}/integrations/{fake_iid}").status_code == 404
        assert (
            client.put(
                f"/api/v1/projects/{fake_pid}/integrations/{fake_iid}",
                json={"name": "X"},
            ).status_code
            == 404
        )
        assert (
            client.delete(f"/api/v1/projects/{fake_pid}/integrations/{fake_iid}").status_code == 404
        )
