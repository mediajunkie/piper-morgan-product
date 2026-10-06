"""
Unit tests for project creation in setup wizard.
Issue #860: Setup wizard project-repo linking step.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

pytestmark = pytest.mark.unit


class TestSetupProjectCreation:
    """Tests for POST /setup/projects endpoint."""

    @pytest.mark.asyncio
    async def test_create_project_success(self):
        """Should create a project with owner_id from setup."""
        from web.api.routes.setup import SetupProjectRequest, create_setup_project

        user_id = str(uuid4())
        project_id = str(uuid4())

        mock_project = MagicMock()
        mock_project.id = project_id

        with patch("web.api.routes.setup.AsyncSessionFactory") as MockFactory:
            mock_session = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
            mock_ctx.__aexit__ = AsyncMock(return_value=None)
            MockFactory.session_scope_fresh.return_value = mock_ctx

            with patch("services.database.repositories.ProjectRepository") as MockProjectRepo:
                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_project)
                MockProjectRepo.return_value = mock_repo

                req = SetupProjectRequest(
                    user_id=user_id,
                    project_name="My App",
                )

                result = await create_setup_project(req)

        assert result.success is True
        assert result.project_id == project_id
        assert "My App" in result.message
        mock_repo.create.assert_called_once()
        call_kwargs = mock_repo.create.call_args[1]
        assert call_kwargs["name"] == "My App"
        assert call_kwargs["owner_id"] == user_id

    @pytest.mark.asyncio
    async def test_create_project_with_github_repo(self):
        """Should create project, Repository entity and link — and NOT the legacy
        GitHub ProjectIntegration the #866 dual-write used to add (retired #1945,
        Arch GO 2026-10-05: nothing reads it; the panel showed it twice)."""
        from services.domain.models import Repository as DomainRepo
        from web.api.routes.setup import SetupProjectRequest, create_setup_project

        user_id = str(uuid4())
        project_id = str(uuid4())
        repo_id = str(uuid4())

        mock_project = MagicMock()
        mock_project.id = project_id

        mock_repo_entity = DomainRepo(
            id=repo_id,
            owner_id=user_id,
            provider="github",
            full_name="owner/backend-api",
        )

        with patch("web.api.routes.setup.AsyncSessionFactory") as MockFactory:
            mock_session = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
            mock_ctx.__aexit__ = AsyncMock(return_value=None)
            MockFactory.session_scope_fresh.return_value = mock_ctx

            with (
                patch("services.database.repositories.ProjectRepository") as MockProjectRepo,
                patch("services.database.repositories.ProjectIntegrationRepository") as MockIntRepo,
                patch("services.database.repositories.RepositoryRepository") as MockRepoRepo,
            ):
                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_project)
                MockProjectRepo.return_value = mock_repo

                mock_int_repo = MagicMock()
                mock_int_repo.create = AsyncMock()
                MockIntRepo.return_value = mock_int_repo

                mock_repo_repo = MagicMock()
                mock_repo_repo.create_repository = AsyncMock(return_value=mock_repo_entity)
                mock_repo_repo.link_to_project = AsyncMock()
                MockRepoRepo.return_value = mock_repo_repo

                req = SetupProjectRequest(
                    user_id=user_id,
                    project_name="Backend",
                    github_repo="owner/backend-api",
                )

                result = await create_setup_project(req)

        assert result.success is True

        # Verify NEW Repository entity was created (#866)
        mock_repo_repo.create_repository.assert_called_once()
        created_repo = mock_repo_repo.create_repository.call_args[0][0]
        assert created_repo.full_name == "owner/backend-api"
        assert created_repo.provider == "github"
        assert created_repo.owner_id == user_id

        # Verify NEW link was created (#866)
        mock_repo_repo.link_to_project.assert_called_once()
        link_kwargs = mock_repo_repo.link_to_project.call_args[1]
        assert link_kwargs["repository_id"] == repo_id
        assert link_kwargs["project_id"] == project_id
        assert link_kwargs["is_primary"] is True

        # #1945: the legacy GitHub integration is NOT written any more — one
        # row per real thing. (The mock stays in place so a reintroduced
        # dual-write fails here rather than silently re-creating the mirror.)
        mock_int_repo.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_project_empty_name_fails(self):
        """Should reject empty project name."""
        from fastapi import HTTPException

        from web.api.routes.setup import SetupProjectRequest, create_setup_project

        req = SetupProjectRequest(
            user_id=str(uuid4()),
            project_name="  ",
        )

        with pytest.raises(HTTPException) as exc_info:
            await create_setup_project(req)
        assert exc_info.value.status_code == 400
        assert "name is required" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_create_project_invalid_repo_format(self):
        """Should reject repo without slash."""
        from fastapi import HTTPException

        from web.api.routes.setup import SetupProjectRequest, create_setup_project

        user_id = str(uuid4())
        project_id = str(uuid4())

        mock_project = MagicMock()
        mock_project.id = project_id

        with patch("web.api.routes.setup.AsyncSessionFactory") as MockFactory:
            mock_session = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
            mock_ctx.__aexit__ = AsyncMock(return_value=None)
            MockFactory.session_scope_fresh.return_value = mock_ctx

            with patch("services.database.repositories.ProjectRepository") as MockProjectRepo:
                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_project)
                MockProjectRepo.return_value = mock_repo

                req = SetupProjectRequest(
                    user_id=user_id,
                    project_name="My App",
                    github_repo="no-slash-here",
                )

                with pytest.raises(HTTPException) as exc_info:
                    await create_setup_project(req)
                assert exc_info.value.status_code == 400
                assert "owner/repo" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_create_project_without_repo(self):
        """Should create project without GitHub repo when not provided."""
        from web.api.routes.setup import SetupProjectRequest, create_setup_project

        user_id = str(uuid4())
        project_id = str(uuid4())

        mock_project = MagicMock()
        mock_project.id = project_id

        with patch("web.api.routes.setup.AsyncSessionFactory") as MockFactory:
            mock_session = AsyncMock()
            mock_ctx = AsyncMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_session)
            mock_ctx.__aexit__ = AsyncMock(return_value=None)
            MockFactory.session_scope_fresh.return_value = mock_ctx

            with (
                patch("services.database.repositories.ProjectRepository") as MockProjectRepo,
                patch("services.database.repositories.ProjectIntegrationRepository") as MockIntRepo,
            ):
                mock_repo = MagicMock()
                mock_repo.create = AsyncMock(return_value=mock_project)
                MockProjectRepo.return_value = mock_repo

                mock_int_repo = MagicMock()
                MockIntRepo.return_value = mock_int_repo

                req = SetupProjectRequest(
                    user_id=user_id,
                    project_name="No Repo Project",
                )

                result = await create_setup_project(req)

        assert result.success is True
        # Integration repo should NOT have been called
        mock_int_repo.create.assert_not_called()


class TestSetupProjectHTMLStep:
    """Tests for setup wizard project step HTML structure."""

    def test_setup_html_has_projects_step(self):
        """Verify setup.html includes the Projects step."""
        with open("templates/setup.html") as f:
            html = f.read()

        assert 'id="step-4"' in html
        assert "Your Projects" in html
        assert "setup-project-name" in html
        assert "setup-github-repo" in html
        assert "add-project-btn" in html
        assert "skip-projects-btn" in html

    def test_setup_html_has_five_steps(self):
        """Verify progress bar has 5 steps after #860."""
        with open("templates/setup.html") as f:
            html = f.read()

        assert 'data-step="5"' in html
        assert "5. Complete" in html
        assert "4. Projects" in html

    def test_complete_step_renumbered_to_5(self):
        """Verify Complete step is now step-5."""
        with open("templates/setup.html") as f:
            html = f.read()

        assert 'id="step-5"' in html
        assert "Setup Complete" in html
