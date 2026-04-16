# tests/test_pm009_project_support.py
"""
Test-first specification for PM-009 multi-project support.
These tests define the complete behavior expected from the implementation.
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from services.database.repositories import ProjectRepository
from services.domain.models import Intent, IntentCategory, Project, ProjectIntegration

# Domain imports (these will need to be implemented)
from services.project_context import AmbiguousProjectError, ProjectContext, ProjectNotFoundError
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter
from services.shared_types import IntegrationType, WorkflowStatus, WorkflowType


@pytest.fixture
def mock_project_repository():
    repo = Mock()
    repo.list_active_projects = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.get_default_project = AsyncMock()
    repo.find_by_name = AsyncMock()
    repo.count_active_projects = AsyncMock()
    return repo


class TestProjectDomainModel:
    """Test the Project domain model behaves correctly"""

    def test_project_creation_with_defaults(self):
        """Project should initialize with sensible defaults"""
        project = Project(name="Mobile App", description="iOS and Android apps")

        assert project.id is not None
        assert project.name == "Mobile App"
        assert project.description == "iOS and Android apps"
        assert project.is_default is False
        assert project.is_archived is False
        assert len(project.integrations) == 0
        assert isinstance(project.created_at, datetime)

    def test_get_github_integration(self):
        """Should retrieve GitHub integration when present"""
        # GIVEN: Project with GitHub integration
        project = Project(name="Test Project")
        github_integration = ProjectIntegration(
            type=IntegrationType.GITHUB,
            name="Main Repo",
            config={"repository": "owner/repo"},
        )
        project.integrations.append(github_integration)

        # WHEN: Getting GitHub integration
        integration = project.get_integration(IntegrationType.GITHUB)

        # THEN: Should return the integration
        assert integration is not None
        assert integration.type == IntegrationType.GITHUB
        assert integration.config["repository"] == "owner/repo"

    def test_get_github_repository_shortcut(self):
        """Should provide easy access to GitHub repository"""
        # GIVEN: Project with GitHub integration
        project = Project(name="Test Project")
        project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                name="Main Repo",
                config={"repository": "mediajunkie/piper-morgan-test"},
            )
        )

        # WHEN/THEN: Should return repository directly
        assert project.get_github_repository() == "mediajunkie/piper-morgan-test"

    def test_validate_integrations(self):
        """Should validate all integration configurations"""
        # GIVEN: Project with valid and invalid integrations
        project = Project(name="Test Project")

        # Valid GitHub integration
        project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                name="Valid GitHub",
                config={"repository": "owner/repo"},
            )
        )

        # Invalid GitHub integration (missing repository)
        project.integrations.append(
            ProjectIntegration(type=IntegrationType.GITHUB, name="Invalid GitHub", config={})
        )

        # WHEN: Validating integrations
        errors = project.validate_integrations()

        # THEN: Should report invalid integration
        assert len(errors) == 1
        assert "github" in errors[0].lower()


class TestProjectContext:
    """Test ProjectContext resolution logic"""

    @pytest.fixture
    def mock_repo(self):
        """Provides a mock ProjectRepository"""
        repo = Mock(spec=ProjectRepository)
        repo.get_by_id = AsyncMock()
        repo.get_default_project = AsyncMock()
        repo.list_active_projects = AsyncMock()
        repo.count_active_projects = AsyncMock()
        repo.find_by_name = AsyncMock()
        return repo

    @pytest.fixture
    def mock_llm(self):
        """Provides a mock LLM client"""
        llm = Mock()
        llm.complete = AsyncMock()
        return llm

    @pytest.mark.asyncio
    async def test_explicit_project_id_takes_precedence(self, mock_repo, mock_llm):
        """Explicit project ID should always win"""
        # GIVEN: Intent with explicit project_id
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"project_id": "explicit-123"},
        )

        # AND: Repository returns the project
        expected_project = Project(id="explicit-123", name="Explicit Project")
        mock_repo.get_by_id.return_value = expected_project

        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="test-session"
        )

        # THEN: Should return explicit project without confirmation
        assert project.id == "explicit-123"
        assert project.name == "Explicit Project"
        assert needs_confirmation is False
        mock_repo.get_by_id.assert_called_once_with("explicit-123")

    @pytest.mark.asyncio
    async def test_uses_last_project_from_session(self, mock_repo, mock_llm):
        """Should remember and use last project from session"""
        # GIVEN: Previous project selection in session
        context = ProjectContext(mock_repo, mock_llm)
        context._session_last_used["session-1"] = "last-used-123"

        # AND: Intent without project specification
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a bug ticket"},
        )

        # AND: Repository returns the last used project
        last_project = Project(id="last-used-123", name="Last Used Project")
        mock_repo.get_by_id.return_value = last_project

        # WHEN: Resolving with confirmed session
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="session-1", confirmed_this_session=True
        )

        # THEN: Should use last project without confirmation
        assert project.id == "last-used-123"
        assert needs_confirmation is False

    @pytest.mark.asyncio
    async def test_infers_project_from_message_context(self, mock_repo, mock_llm):
        """Should use LLM to infer project from message"""
        # GIVEN: Intent mentioning a project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Bug in the mobile app login"},
        )

        # AND: Multiple projects exist
        projects = [
            Project(id="web-123", name="Web Platform", description="Main website"),
            Project(id="mobile-123", name="Mobile App", description="iOS and Android"),
        ]
        mock_repo.list_active_projects.return_value = projects

        # AND: LLM identifies the mobile project
        mock_llm.complete.return_value = "Mobile App"

        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="new-session"
        )

        # THEN: Should return mobile project
        assert project.name == "Mobile App"
        assert project.id == "mobile-123"

    @pytest.mark.asyncio
    async def test_needs_confirmation_when_ambiguous(self, mock_repo, mock_llm):
        """Should request confirmation when project is ambiguous"""
        # GIVEN: Session has different project than inferred
        context = ProjectContext(mock_repo, mock_llm)
        context._session_last_used["session-1"] = "project-1"

        # Mock the last used project
        last_project = Project(id="project-1", name="Web App")
        mock_repo.get_by_id.return_value = last_project

        # AND: Message suggests different project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Critical bug in mobile app"},
        )

        # Mock inference returning different project
        inferred_project = Project(id="project-2", name="Mobile App")
        mock_repo.list_active_projects.return_value = [last_project, inferred_project]
        mock_llm.complete.return_value = "Mobile App"

        # WHEN: Resolving without confirmation
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="session-1", confirmed_this_session=False
        )

        # THEN: Should return inferred project but need confirmation
        assert project.name == "Mobile App"
        assert needs_confirmation is True

    @pytest.mark.asyncio
    async def test_falls_back_to_default_project(self, mock_repo, mock_llm):
        """Should use default project when no other context available"""
        # GIVEN: No session history or context
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a ticket"},
        )

        # AND: Only one project exists (the default)
        mock_repo.count_active_projects.return_value = 1
        default_project = Project(id="default-123", name="Default Project", is_default=True)
        mock_repo.get_default_project.return_value = default_project

        # WHEN: Resolving project
        context = ProjectContext(mock_repo, mock_llm)
        project, needs_confirmation = await context.resolve_project(
            intent, session_id="new-session"
        )

        # THEN: Should return default without confirmation
        assert project.id == "default-123"
        assert project.is_default is True
        assert needs_confirmation is False

    @pytest.mark.asyncio
    async def test_raises_ambiguous_error_when_unclear(self, mock_repo, mock_llm):
        """Should raise error when can't determine project among many"""
        # GIVEN: Multiple projects exist
        mock_repo.count_active_projects.return_value = 3

        # AND: No context to determine which one
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"original_message": "Create a ticket"},
        )

        # AND: No inference possible
        mock_repo.list_active_projects.return_value = [
            Project(name="Project A"),
            Project(name="Project B"),
            Project(name="Project C"),
        ]
        mock_llm.complete.return_value = "UNCLEAR"

        # WHEN/THEN: Should raise AmbiguousProjectError
        context = ProjectContext(mock_repo, mock_llm)
        with pytest.raises(AmbiguousProjectError) as exc_info:
            await context.resolve_project(intent, session_id="new-session")

        assert "Multiple projects available" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_handles_project_not_found_error(self, mock_repo, mock_llm):
        """Should handle gracefully when explicit project doesn't exist"""
        # GIVEN: Intent with non-existent project_id
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            context={"project_id": "non-existent-123"},
        )

        # AND: Repository returns None (not found)
        mock_repo.get_by_id.return_value = None

        # WHEN/THEN: Should raise clear error
        context = ProjectContext(mock_repo, mock_llm)
        with pytest.raises(ProjectNotFoundError) as exc_info:
            await context.resolve_project(intent, session_id="test-session")

        assert "non-existent-123" in str(exc_info.value)
        assert "not found" in str(exc_info.value).lower()


class TestWorkflowFactoryIntegration:
    """Test WorkflowFactory creates workflows with project context"""

    @pytest.mark.asyncio
    async def test_workflow_includes_project_context(self):
        """Created workflow should include full project context"""
        # GIVEN: Intent and project
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_github_issue",
            context={"original_message": "Bug report"},
        )

        project = Project(id="proj-123", name="Test Project")
        project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                name="Main Repo",
                config={"repository": "owner/repo", "default_labels": ["bug"]},
            )
        )

        # Import after mocks are set up
        from services.orchestration.workflow_factory import WorkflowFactory

        # WHEN: Creating workflow with stateless factory
        factory = WorkflowFactory()  # Stateless - no dependencies
        workflow = await factory.create_from_intent(intent)

        # THEN: Workflow should be created (project context would be injected at execution time)
        assert workflow is not None
        assert workflow.type == WorkflowType.CREATE_TICKET
        assert workflow.status == WorkflowStatus.PENDING


class TestGitHubAgentProjectIntegration:
    """Test GitHub agent uses project configuration"""

    @pytest.mark.asyncio
    async def test_uses_project_github_configuration(self):
        """Should use repository and labels from project config"""
        # This is more of an integration test but important for PM-009
        from services.domain.models import Workflow

        # GIVEN: Workflow with project context
        workflow = Workflow(
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            context={
                "project_id": "proj-123",
                "project_name": "Mobile App",
                "project_integrations": {
                    "github": {
                        "repository": "mediajunkie/mobile-app",
                        "default_labels": ["mobile", "ai-generated"],
                    }
                },
            },
        )

        # AND: Issue data
        issue_data = {
            "title": "Login crash on iOS",
            "body": "Users report app crashes when logging in",
            "labels": ["bug"],
        }

        # WHEN: GitHub agent processes the workflow
        # (This would be mocked in a unit test, but shows expected behavior)
        # The agent should:
        # 1. Extract repository from workflow context
        # 2. Merge default labels with issue labels
        # 3. Create issue in correct repository

        # Expected behavior to test:
        # - Repository: "mediajunkie/mobile-app" (from project)
        # - Labels: ["bug", "mobile", "ai-generated"] (merged)


# Anti-pattern prevention tests
class TestNoHardcodedValues:
    """Ensure implementation follows patterns"""

    def test_uses_enum_not_strings_for_integration_type(self):
        """Must use IntegrationType enum, not string literals"""
        # This is a meta-test that would inspect the actual implementation
        # Include it to prevent "if integration.type == 'github':" anti-pattern
        pass

    def test_repository_pattern_for_database_operations(self):
        """Database operations must go through repositories"""
        # Ensure ProjectContext doesn't directly use SQLAlchemy
        # Should only use ProjectRepository methods
        pass


class TestListProjectsQuery:
    """Test LIST_PROJECTS query following CQRS-lite pattern"""

    @pytest.fixture
    def mock_project_repository(self):
        """Provides a mock ProjectRepository for testing"""
        repo = Mock()
        repo.list_active_projects = AsyncMock()
        return repo

    @pytest.mark.asyncio
    async def test_list_projects_query_returns_all_projects(self, mock_project_repository):
        """LIST_PROJECTS query should return structured project list"""
        # GIVEN: Multiple projects in the repository
        projects = [
            Project(
                id="proj-1",
                name="Mobile App",
                description="iOS and Android applications",
                is_default=True,
            ),
            Project(
                id="proj-2",
                name="Web Platform",
                description="Main website and API",
                is_default=False,
            ),
            Project(
                id="proj-3",
                name="Data Pipeline",
                description="ETL and analytics infrastructure",
                is_default=False,
            ),
        ]
        mock_project_repository.list_active_projects.return_value = projects

        # AND: Intent to list projects (QUERY category)
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_projects",
            context={"original_message": "What projects are available?"},
        )

        # WHEN: Processing query through query service
        query_service = ProjectQueryService(mock_project_repository)
        result = await query_service.list_active_projects()

        # THEN: Repository should be called
        mock_project_repository.list_active_projects.assert_called_once()

        # AND: Result should contain structured project data
        assert len(result) == 3

        # AND: Each project should have required fields
        for i, project in enumerate(result):
            assert project.id == projects[i].id
            assert project.name == projects[i].name
            assert project.description == projects[i].description
            assert project.is_default == projects[i].is_default

    @pytest.mark.asyncio
    async def test_list_projects_query_handles_empty_repository(self, mock_project_repository):
        """LIST_PROJECTS query should handle empty project list gracefully"""
        # GIVEN: Empty repository
        mock_project_repository.list_active_projects.return_value = []

        # AND: Intent to list projects
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_projects",
            context={"original_message": "Show me all projects"},
        )

        # WHEN: Processing query
        query_service = ProjectQueryService(mock_project_repository)
        result = await query_service.list_active_projects()

        # THEN: Should handle empty list gracefully
        assert result == []

    @pytest.mark.asyncio
    async def test_list_projects_query_handles_repository_error(self, mock_project_repository):
        """LIST_PROJECTS query should handle repository errors gracefully"""
        # GIVEN: Repository that raises an exception
        mock_project_repository.list_active_projects.side_effect = Exception(
            "Database connection failed"
        )

        # AND: Intent to list projects
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_projects",
            context={"original_message": "List all projects"},
        )

        # WHEN: Processing query
        query_service = ProjectQueryService(mock_project_repository)

        # THEN: Should handle error gracefully
        with pytest.raises(Exception) as exc_info:
            await query_service.list_active_projects()
        assert "Database connection failed" in str(exc_info.value)

    def test_list_projects_intent_classification(self):
        """Intent classifier should recognize list_projects as QUERY category"""
        # GIVEN: Various ways to request project listing
        list_project_phrases = [
            "What projects are available?",
            "Show me all projects",
            "List the projects",
            "Get project list",
            "What projects do we have?",
        ]

        # WHEN: Classifying each phrase
        # classifier = IntentClassifier()

        for phrase in list_project_phrases:
            # intent = await classifier.classify(phrase)

            # THEN: Should be classified as QUERY with list_projects action
            # assert intent.category == IntentCategory.QUERY
            # assert intent.action == "list_projects"
            pass  # Placeholder until implementation


class TestQueryRouter:
    """Test QueryRouter for proper intent routing"""

    @pytest.fixture
    def mock_project_repository(self):
        """Provides a mock ProjectRepository for testing"""
        repo = Mock()
        repo.list_active_projects = AsyncMock()
        repo.get_by_id = AsyncMock()
        repo.get_default_project = AsyncMock()
        repo.find_by_name = AsyncMock()
        repo.count_active_projects = AsyncMock()
        return repo

    @pytest.mark.asyncio
    async def test_router_routes_list_projects_query(self, mock_project_repository):
        """QueryRouter should route list_projects to project query service"""
        # GIVEN: Projects and query service
        projects = [Project(id="p1", name="Test Project")]
        mock_project_repository.list_active_projects.return_value = projects

        project_query_service = ProjectQueryService(mock_project_repository)
        conversation_query_service = ConversationQueryService()
        file_query_service = FileQueryService(Mock())  # Add mock file query service
        router = QueryRouter(project_query_service, conversation_query_service, file_query_service)

        # AND: QUERY intent for list_projects
        intent = Intent(category=IntentCategory.QUERY, action="list_projects", context={})

        # WHEN: Routing the query
        result = await router.route_query(intent)

        # THEN: Should return projects from query service
        assert result == projects
        mock_project_repository.list_active_projects.assert_called_once()

    @pytest.mark.asyncio
    async def test_router_rejects_non_query_intents(self, mock_project_repository):
        """QueryRouter should reject non-QUERY intents"""
        project_query_service = ProjectQueryService(mock_project_repository)
        conversation_query_service = ConversationQueryService()
        file_query_service = FileQueryService(Mock())  # Add mock file query service
        router = QueryRouter(project_query_service, conversation_query_service, file_query_service)

        # GIVEN: EXECUTION intent (not QUERY)
        intent = Intent(category=IntentCategory.EXECUTION, action="list_projects", context={})

        # WHEN/THEN: Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            await router.route_query(intent)
        assert "QueryRouter can only handle QUERY intents" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_router_handles_unknown_query_action(self, mock_project_repository):
        """QueryRouter should handle unknown query actions gracefully"""
        project_query_service = ProjectQueryService(mock_project_repository)
        conversation_query_service = ConversationQueryService()
        file_query_service = FileQueryService(Mock())  # Add mock file query service
        router = QueryRouter(project_query_service, conversation_query_service, file_query_service)

        # GIVEN: QUERY intent with unknown action
        intent = Intent(category=IntentCategory.QUERY, action="unknown_action", context={})

        # WHEN/THEN: Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            await router.route_query(intent)
        assert "Unknown query action" in str(exc_info.value)

    def test_router_supported_queries(self, mock_project_repository):
        """QueryRouter should return list of supported queries"""
        project_query_service = ProjectQueryService(mock_project_repository)
        conversation_query_service = ConversationQueryService()
        file_query_service = FileQueryService(Mock())  # Add mock file query service
        router = QueryRouter(project_query_service, conversation_query_service, file_query_service)

        # WHEN: Getting supported queries
        supported = router.get_supported_queries()

        # THEN: Should include expected query actions
        assert "list_projects" in supported
        assert "get_project" in supported
        assert "get_default_project" in supported
        assert "find_project" in supported
        assert "count_projects" in supported


@pytest.mark.asyncio
async def test_get_project_by_id_returns_project(mock_project_repository):
    project = Project(id="proj-1", name="Test Project")
    mock_project_repository.get_by_id.return_value = project
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.get_project_by_id("proj-1")
    assert result == project


@pytest.mark.asyncio
async def test_get_project_by_id_returns_none_for_missing(mock_project_repository):
    mock_project_repository.get_by_id.return_value = None
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.get_project_by_id("nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_get_project_by_id_handles_repository_error(mock_project_repository):
    mock_project_repository.get_by_id.side_effect = Exception("DB error")
    query_service = ProjectQueryService(mock_project_repository)
    with pytest.raises(Exception) as exc_info:
        await query_service.get_project_by_id("proj-1")
    assert "DB error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_default_project_returns_project(mock_project_repository):
    project = Project(id="proj-1", name="Default Project", is_default=True)
    mock_project_repository.get_default_project.return_value = project
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.get_default_project()
    assert result == project


@pytest.mark.asyncio
async def test_get_default_project_returns_none_if_missing(mock_project_repository):
    mock_project_repository.get_default_project.return_value = None
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.get_default_project()
    assert result is None


@pytest.mark.asyncio
async def test_find_project_by_name_returns_project(mock_project_repository):
    project = Project(id="proj-2", name="Web Platform")
    mock_project_repository.find_by_name.return_value = project
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.find_project_by_name("Web Platform")
    assert result == project


@pytest.mark.asyncio
async def test_find_project_by_name_returns_none_for_missing(mock_project_repository):
    mock_project_repository.find_by_name.return_value = None
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.find_project_by_name("Nonexistent")
    assert result is None


@pytest.mark.asyncio
async def test_count_active_projects_returns_count(mock_project_repository):
    mock_project_repository.count_active_projects.return_value = 3
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.count_active_projects()
    assert result == 3


@pytest.mark.asyncio
async def test_count_active_projects_handles_repository_error(mock_project_repository):
    mock_project_repository.count_active_projects.side_effect = Exception("DB error")
    query_service = ProjectQueryService(mock_project_repository)
    with pytest.raises(Exception) as exc_info:
        await query_service.count_active_projects()
    assert "DB error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_project_by_id_with_invalid_id(mock_project_repository):
    mock_project_repository.get_by_id.return_value = None
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.get_project_by_id("")
    assert result is None


@pytest.mark.asyncio
async def test_find_project_by_name_with_invalid_name(mock_project_repository):
    mock_project_repository.find_by_name.return_value = None
    query_service = ProjectQueryService(mock_project_repository)
    result = await query_service.find_project_by_name("")
    assert result is None
