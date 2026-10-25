"""
Unit tests for Repository API endpoints.
Issue #866: Repository as first-class domain entity.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTClaims
from services.domain.models import Project, ProjectRepositoryLink, Repository
from services.infrastructure.github_repo_validator import RepoValidationResult

pytestmark = pytest.mark.unit


USER_ID = str(uuid4())
MOCK_CLAIMS = JWTClaims(
    sub=USER_ID,
    exp=9999999999,
    iat=1000000000,
    iss="piper-morgan",
    aud="piper-morgan-api",
    jti=str(uuid4()),
    user_id=UUID(USER_ID),
    user_email="test@example.com",
    username="testuser",
    scopes=["user"],
    token_type="access",
)


def _make_app(
    repo_repo_mock=None,
    project_repo_mock=None,
):
    """Create a test app with mocked dependencies."""
    from web.api.routes.repositories import router

    app = FastAPI()
    app.include_router(router)

    # Override auth
    from services.auth.auth_middleware import get_current_user

    app.dependency_overrides[get_current_user] = lambda: MOCK_CLAIMS

    # Override repo repository
    if repo_repo_mock:
        from web.api.dependencies import get_repository_repository

        app.dependency_overrides[get_repository_repository] = lambda: repo_repo_mock

    # Override project repository
    if project_repo_mock:
        from web.api.dependencies import get_project_repository

        app.dependency_overrides[get_project_repository] = lambda: project_repo_mock

    return TestClient(app)


class TestCreateRepository:
    """Tests for POST /api/v1/repositories."""

    def test_create_success(self):
        repo_repo = MagicMock()
        repo_repo.get_by_full_name = AsyncMock(return_value=None)
        repo_repo.create_repository = AsyncMock(
            return_value=Repository(
                id="repo-1",
                owner_id=USER_ID,
                provider="github",
                full_name="owner/my-repo",
                display_name="my-repo",
                url="https://github.com/owner/my-repo",
            )
        )
        client = _make_app(repo_repo_mock=repo_repo)

        with patch(
            "web.api.routes.repositories.validate_github_repo_for_account",
            new_callable=AsyncMock,
            return_value=RepoValidationResult(validated=False, exists=False, accessible=False),
        ):
            resp = client.post(
                "/api/v1/repositories",
                json={"full_name": "owner/my-repo"},
            )
        assert resp.status_code == 201
        data = resp.json()
        assert data["full_name"] == "owner/my-repo"
        assert data["provider"] == "github"
        repo_repo.create_repository.assert_called_once()

    def test_create_invalid_full_name(self):
        repo_repo = MagicMock()
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.post(
            "/api/v1/repositories",
            json={"full_name": "no-slash"},
        )
        assert resp.status_code == 400
        assert "owner/repo" in resp.json()["detail"]

    def test_create_invalid_provider(self):
        repo_repo = MagicMock()
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.post(
            "/api/v1/repositories",
            json={"full_name": "owner/repo", "provider": "svn"},
        )
        assert resp.status_code == 400
        assert "Invalid provider" in resp.json()["detail"]

    def test_create_duplicate_409(self):
        repo_repo = MagicMock()
        repo_repo.get_by_full_name = AsyncMock(return_value=Repository(full_name="owner/repo"))
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.post(
            "/api/v1/repositories",
            json={"full_name": "owner/repo"},
        )
        assert resp.status_code == 409

    def test_create_with_validation_success(self):
        """Issue #867: Metadata populated when GitHub API validates."""
        repo_repo = MagicMock()
        repo_repo.get_by_full_name = AsyncMock(return_value=None)
        repo_repo.create_repository = AsyncMock(
            return_value=Repository(
                id="repo-1",
                owner_id=USER_ID,
                provider="github",
                full_name="owner/my-repo",
                description="A cool repo",
                language="Python",
                visibility="public",
                default_branch="main",
            )
        )
        client = _make_app(repo_repo_mock=repo_repo)

        with patch(
            "web.api.routes.repositories.validate_github_repo_for_account",
            new_callable=AsyncMock,
            return_value=RepoValidationResult(
                validated=True,
                exists=True,
                accessible=True,
                description="A cool repo",
                language="Python",
                visibility="public",
                default_branch="main",
            ),
        ):
            resp = client.post(
                "/api/v1/repositories",
                json={"full_name": "owner/my-repo"},
            )
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == "A cool repo"
        assert data["language"] == "Python"
        assert "validation_warning" not in data

    def test_create_with_validation_not_found_still_creates(self):
        """Issue #867: Repo created even if GitHub API returns 404; warning included."""
        repo_repo = MagicMock()
        repo_repo.get_by_full_name = AsyncMock(return_value=None)
        repo_repo.create_repository = AsyncMock(
            return_value=Repository(
                id="repo-1",
                owner_id=USER_ID,
                provider="github",
                full_name="owner/typo-repo",
            )
        )
        client = _make_app(repo_repo_mock=repo_repo)

        with patch(
            "web.api.routes.repositories.validate_github_repo_for_account",
            new_callable=AsyncMock,
            return_value=RepoValidationResult(
                validated=True,
                exists=False,
                accessible=False,
                error="Repository 'owner/typo-repo' not found on GitHub",
            ),
        ):
            resp = client.post(
                "/api/v1/repositories",
                json={"full_name": "owner/typo-repo"},
            )
        assert resp.status_code == 201
        data = resp.json()
        assert "validation_warning" in data
        assert "not found" in data["validation_warning"]
        repo_repo.create_repository.assert_called_once()

    def test_create_without_token_skips_validation(self):
        """Issue #867: No token → validation skipped, repo created normally."""
        repo_repo = MagicMock()
        repo_repo.get_by_full_name = AsyncMock(return_value=None)
        repo_repo.create_repository = AsyncMock(
            return_value=Repository(
                id="repo-1",
                owner_id=USER_ID,
                provider="github",
                full_name="owner/my-repo",
            )
        )
        client = _make_app(repo_repo_mock=repo_repo)

        with patch(
            "web.api.routes.repositories.validate_github_repo_for_account",
            new_callable=AsyncMock,
            return_value=RepoValidationResult(validated=False, exists=False, accessible=False),
        ):
            resp = client.post(
                "/api/v1/repositories",
                json={"full_name": "owner/my-repo"},
            )
        assert resp.status_code == 201
        assert "validation_warning" not in resp.json()
        repo_repo.create_repository.assert_called_once()


class TestListRepositories:
    """Tests for GET /api/v1/repositories."""

    def test_list_success(self):
        repo_repo = MagicMock()
        repo_repo.list_by_owner = AsyncMock(
            return_value=[
                Repository(id="r1", full_name="owner/repo-a"),
                Repository(id="r2", full_name="owner/repo-b"),
            ]
        )
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.get("/api/v1/repositories")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["repositories"]) == 2

    def test_list_with_provider_filter(self):
        repo_repo = MagicMock()
        repo_repo.list_by_owner = AsyncMock(return_value=[])
        client = _make_app(repo_repo_mock=repo_repo)

        client.get("/api/v1/repositories?provider=gitlab")
        repo_repo.list_by_owner.assert_called_once_with(owner_id=USER_ID, provider="gitlab")


class TestGetRepository:
    """Tests for GET /api/v1/repositories/{repo_id}."""

    def test_get_success(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.get("/api/v1/repositories/r1")
        assert resp.status_code == 200
        assert resp.json()["full_name"] == "owner/repo"

    def test_get_not_found(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=None)
        client = _make_app(repo_repo_mock=repo_repo)

        resp = client.get("/api/v1/repositories/nonexistent")
        assert resp.status_code == 404


class TestLinkRepository:
    """Tests for POST /api/v1/repositories/{repo_id}/projects/{project_id}."""

    def test_link_success(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        repo_repo.get_project_links = AsyncMock(return_value=[])
        repo_repo.link_to_project = AsyncMock(
            return_value=ProjectRepositoryLink(
                id="link-1",
                project_id="p1",
                repository_id="r1",
                linked_by=USER_ID,
            )
        )
        project_repo = MagicMock()
        project_repo.get_by_id = AsyncMock(return_value=Project(id="p1", name="My Project"))
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.post("/api/v1/repositories/r1/projects/p1")
        assert resp.status_code == 201
        assert resp.json()["project_id"] == "p1"
        assert resp.json()["repository_id"] == "r1"

    def test_link_already_linked_409(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        repo_repo.get_project_links = AsyncMock(
            return_value=[
                ProjectRepositoryLink(project_id="p1", repository_id="r1"),
            ]
        )
        project_repo = MagicMock()
        project_repo.get_by_id = AsyncMock(return_value=Project(id="p1", name="My Project"))
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.post("/api/v1/repositories/r1/projects/p1")
        assert resp.status_code == 409

    def test_link_repo_not_found(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=None)
        project_repo = MagicMock()
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.post("/api/v1/repositories/bad/projects/p1")
        assert resp.status_code == 404

    def test_link_project_not_found(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        project_repo = MagicMock()
        project_repo.get_by_id = AsyncMock(return_value=None)
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.post("/api/v1/repositories/r1/projects/bad")
        assert resp.status_code == 404


class TestUnlinkRepository:
    """Tests for DELETE /api/v1/repositories/{repo_id}/projects/{project_id}."""

    def test_unlink_success(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        repo_repo.unlink_from_project = AsyncMock(return_value=True)
        project_repo = MagicMock()
        project_repo.get_by_id = AsyncMock(return_value=Project(id="p1", name="My Project"))
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.delete("/api/v1/repositories/r1/projects/p1")
        assert resp.status_code == 200

    def test_unlink_not_found(self):
        repo_repo = MagicMock()
        repo_repo.get_by_id = AsyncMock(return_value=Repository(id="r1", full_name="owner/repo"))
        repo_repo.unlink_from_project = AsyncMock(return_value=False)
        project_repo = MagicMock()
        project_repo.get_by_id = AsyncMock(return_value=Project(id="p1", name="My Project"))
        client = _make_app(repo_repo_mock=repo_repo, project_repo_mock=project_repo)

        resp = client.delete("/api/v1/repositories/r1/projects/p1")
        assert resp.status_code == 404
