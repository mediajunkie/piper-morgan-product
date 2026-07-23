"""Comprehensive tests for EXECUTION and ANALYSIS handlers - GREAT-4D"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService
from services.intent_service.pre_classifier import MultiIntentResult


def _stub_classifier(mock_classifier, intent):
    """#1452 fixture-rot repair: process_intent now awaits classify_multiple
    (the #595 multi-intent rail) before any classify fallback — a bare
    MagicMock there raised "can't be used in 'await' expression". Stub both
    surfaces with the same single intent."""
    mock_classifier.classify = AsyncMock(return_value=intent)
    mock_classifier.classify_multiple = AsyncMock(
        return_value=MultiIntentResult(
            intents=[intent],
            original_message=intent.original_message,
            is_multi_intent=False,
        )
    )


class TestExecutionHandlers:
    """Test EXECUTION intent handlers."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_engine.handle_execution_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-123"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService()

    @pytest.mark.asyncio
    async def test_create_issue_handler_exists(self, intent_service):
        """Verify create_issue handler exists and is callable."""
        assert hasattr(intent_service, "_handle_create_issue")
        assert callable(intent_service._handle_create_issue)

    @pytest.mark.asyncio
    async def test_execution_intent_no_placeholder(self, intent_service):
        """Verify EXECUTION intents don't return placeholder messages."""
        intent = Intent(
            original_message="create an issue about testing",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"title": "Test issue", "repository": "test-repo"},
        )

        # Mock classifier to return this intent
        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "create an issue about testing", session_id="test"
            )

            # Should NOT contain placeholder messages
            assert "Phase 3" not in result.message
            assert "full orchestration workflow" not in result.message
            assert "placeholder" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_create_issue_uses_user_scoped_default_repo_1366(self, intent_service):
        """#1366 Component A: when no repository is named in the request, the
        fallback default repo must come from the per-user get_user_default_repo
        resolver, not piper_config_loader.load_github_config().default_repository
        — on a shared instance the unscoped file read would hand every user PM's
        own default repo."""
        from uuid import UUID

        user_id = "12345678-1234-5678-1234-567812345678"
        intent = Intent(
            original_message="create an issue about testing",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            # Deliberately no "repository"/"repo" key — forces the default-repo fallback.
            context={"title": "Test issue"},
        )

        # #1220/#1382 (2026-07-09): the write now goes through the ROUTER
        # (connector-first, #1322-guarded) — mocks repointed from the legacy
        # GitHubDomainService to GitHubIntegrationRouter.
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize", new=AsyncMock()
        ), patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter.is_available", new=AsyncMock(return_value=True)
        ), patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter.create_issue",
            new=AsyncMock(return_value={"number": 42, "title": "Test issue"}),
        ) as mock_create, patch(
            "services.integrations.github.repo_resolver.get_user_default_repo",
            new_callable=AsyncMock,
        ) as mock_get_default_repo, patch(
            "services.configuration.piper_config_loader.piper_config_loader"
        ) as mock_config_loader:
            mock_get_default_repo.return_value = "scoped-owner/scoped-repo"
            mock_config_loader.load_github_config.return_value = MagicMock(
                default_labels=None
            )

            result = await intent_service._handle_create_issue(
                intent, workflow_id="wf-1", session_id="test", user_id=user_id
            )

            mock_get_default_repo.assert_awaited_once_with(UUID(user_id))
            assert result.success is True
            mock_create.assert_awaited_once()
            kwargs = mock_create.await_args.kwargs
            assert kwargs["owner"] == "scoped-owner"
            assert kwargs["repo_name"] == "scoped-repo"

    @pytest.mark.asyncio
    async def test_create_issue_attempts_execution(self, intent_service):
        """Verify create_issue handler attempts to execute."""
        intent = Intent(
            original_message="create an issue",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"title": "Test issue", "repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            result = await intent_service.process_intent("create an issue", session_id="test")

            # Should attempt execution (success or error, not placeholder)
            assert result.success is not None
            assert result.message is not None
            assert len(result.message) > 0

    @pytest.mark.asyncio
    async def test_update_issue_handler_exists(self, intent_service):
        """Verify update_issue handler exists."""
        assert hasattr(intent_service, "_handle_update_issue")
        assert callable(intent_service._handle_update_issue)

    @pytest.mark.asyncio
    async def test_update_issue_missing_issue_number(self, intent_service):
        """Test update_issue returns error when issue_number is missing."""
        intent = Intent(
            original_message="update issue with new title",
            category=IntentCategory.EXECUTION,
            action="update_issue",
            confidence=0.95,
            context={"title": "Updated Title", "repository": "test-repo"},
            # Missing issue_number
        )

        result = await intent_service._handle_update_issue(
            intent=intent, workflow_id="test-workflow-123"
        )

        # Should fail validation
        assert result.success is False
        assert "issue number" in result.message.lower() or "issue_number" in result.message.lower()
        assert result.requires_clarification is True  # Validation errors require clarification
        assert result.clarification_type == "issue_number_required"

    @pytest.mark.asyncio
    async def test_update_issue_extracts_issue_number_from_message(self, intent_service):
        """Issue #1066: When LLM extraction doesn't populate issue_number, fall back
        to parsing #N from the original message — matches the pattern used by
        review_issue / close_issue / comment_issue handlers."""
        intent = Intent(
            original_message="Update issue #123",
            category=IntentCategory.EXECUTION,
            action="update_issue",
            confidence=0.95,
            context={"title": "Updated Title", "repository": "test-repo"},
            # No issue_number in context — should be extracted from #123 in message
        )

        result = await intent_service._handle_update_issue(
            intent=intent, workflow_id="test-workflow-1066"
        )

        # The "issue_number_required" path should NOT fire because #123 was extracted.
        # We don't care about the success/failure of the actual GitHub call here —
        # only that it got past the issue_number validation.
        if result.requires_clarification and result.clarification_type == "issue_number_required":
            pytest.fail(
                f"Handler bailed at issue_number validation despite #123 in message. "
                f"Message: {result.message}"
            )

    @pytest.mark.asyncio
    async def test_update_issue_missing_repository(self, intent_service):
        """Test update_issue returns error when repository is missing."""
        intent = Intent(
            original_message="update issue 123",
            category=IntentCategory.EXECUTION,
            action="update_issue",
            confidence=0.95,
            context={"issue_number": 123, "title": "Updated Title"},
            # Missing repository
        )

        result = await intent_service._handle_update_issue(
            intent=intent, workflow_id="test-workflow-123"
        )

        # Should fail validation
        assert result.success is False
        assert "repository" in result.message.lower()
        assert result.requires_clarification is True  # Validation errors require clarification
        assert result.clarification_type == "repository_required"

    @pytest.mark.asyncio
    async def test_update_issue_no_placeholder_message(self, intent_service):
        """Verify update_issue doesn't return placeholder message after implementation."""
        intent = Intent(
            original_message="update issue 123",
            category=IntentCategory.EXECUTION,
            action="update_issue",
            confidence=0.95,
            context={"issue_number": 123, "title": "Updated Title", "repository": "test-repo"},
        )

        result = await intent_service._handle_update_issue(
            intent=intent, workflow_id="test-workflow-123"
        )

        # Should NOT contain placeholder messages (will fail until implemented)
        if result.success:
            assert "implementation in progress" not in result.message.lower()
            assert "placeholder" not in result.message.lower()
            assert (
                "requires_clarification" not in result.message.lower()
                or result.requires_clarification is False
            )

    @pytest.mark.asyncio
    @patch("services.integrations.github.github_integration_router.GitHubIntegrationRouter.update_issue", new_callable=AsyncMock)
    @patch("services.integrations.github.github_integration_router.GitHubIntegrationRouter.is_available", new_callable=AsyncMock)
    @patch("services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize", new_callable=AsyncMock)
    async def test_update_issue_success_with_mock(
        self, _mock_init, mock_available, mock_update, intent_service
    ):
        """Test successful issue update through the guarded ROUTER (#1220/#1382 —
        mocks repointed from the legacy GitHubDomainService)."""
        mock_available.return_value = True
        mock_update.return_value = {
            "number": 123,
            "title": "Updated Title",
            "state": "open",
            "html_url": "https://github.com/test-org/test-repo/issues/123",
            "updated_at": "2025-10-11T10:30:00Z",
        }

        intent = Intent(
            original_message="update issue 123 with new title",
            category=IntentCategory.EXECUTION,
            action="update_issue",
            confidence=0.95,
            context={
                "issue_number": 123,
                "repository": "test-org/test-repo",
                "title": "Updated Title",
                "body": "Updated description",
            },
        )

        result = await intent_service._handle_update_issue(
            intent=intent, workflow_id="test-workflow-123"
        )

        # Should succeed (will fail until implemented)
        assert result.success is True
        assert result.requires_clarification is False
        assert "updated" in result.message.lower() or "issue" in result.message.lower()
        assert result.intent_data.get("issue_number") == 123

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_update_issue_real_github_integration(self, intent_service):
        """
        Integration test: Create real issue, update it, verify on GitHub, cleanup.

        Requires:
        - GitHub token in .env
        - PIPER_TEST_REPO environment variable set
        """
        import os

        # Skip if no GitHub token or test repo configured
        test_repo = os.getenv("PIPER_TEST_REPO")
        if not test_repo:
            pytest.skip("PIPER_TEST_REPO not configured for integration test")

        # Step 1: Create test issue
        create_intent = Intent(
            original_message="create test issue for update test",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={
                "title": "Test Issue for Update Integration",
                "description": "Original description - will be updated",
                "repository": test_repo,
                "labels": ["test"],
            },
        )

        create_result = await intent_service._handle_create_issue(
            intent=create_intent, workflow_id="test-workflow-integration", session_id="test"
        )

        # Verify issue was created
        assert create_result.success is True
        issue_number = create_result.intent_data.get("issue_number")
        assert issue_number is not None

        try:
            # Step 2: Update the issue
            update_intent = Intent(
                original_message=f"update issue {issue_number}",
                category=IntentCategory.EXECUTION,
                action="update_issue",
                confidence=0.95,
                context={
                    "issue_number": issue_number,
                    "repository": test_repo,
                    "title": "UPDATED: Test Issue",
                    "body": "Updated description - integration test",
                    "labels": ["test", "updated"],
                },
            )

            update_result = await intent_service._handle_update_issue(
                intent=update_intent, workflow_id="test-workflow-integration"
            )

            # Verify update succeeded
            assert update_result.success is True
            assert update_result.requires_clarification is False
            assert update_result.intent_data.get("issue_number") == issue_number
            assert "updated" in update_result.message.lower()

            # Step 3: Verify issue was actually updated on GitHub
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            updated_issue = await github_service.get_issue(test_repo, issue_number)
            assert updated_issue is not None
            assert "UPDATED: Test Issue" in updated_issue.get("title", "")
            assert "Updated description" in updated_issue.get("body", "")

        finally:
            # Step 4: Cleanup - close the test issue
            try:
                from services.domain.github_domain_service import GitHubDomainService

                github_service = GitHubDomainService()
                await github_service.update_issue(
                    repo_name=test_repo, issue_number=issue_number, state="closed"
                )
            except Exception as cleanup_error:
                # Don't fail test if cleanup fails
                print(f"Warning: Failed to cleanup test issue #{issue_number}: {cleanup_error}")

    @pytest.mark.asyncio
    async def test_generic_execution_routes_to_orchestration(self, intent_service):
        """Verify generic EXECUTION actions route to orchestration."""
        intent = Intent(
            original_message="execute something",
            category=IntentCategory.EXECUTION,
            action="unknown_action",
            confidence=0.85,
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            result = await intent_service.process_intent("execute something", session_id="test")

            # Should route to orchestration, not return placeholder
            assert "Phase 3" not in result.message
            assert result.message is not None


class TestAnalysisHandlers:
    """Test ANALYSIS intent handlers."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_engine.handle_analysis_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-456"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService()

    @pytest.mark.asyncio
    async def test_analysis_intent_no_placeholder(self, intent_service):
        """Verify ANALYSIS intents don't return placeholder messages."""
        intent = Intent(
            original_message="analyze the commits",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            result = await intent_service.process_intent("analyze the commits", session_id="test")

            # Should NOT contain placeholder messages
            assert "Phase 3" not in result.message
            assert "full orchestration workflow" not in result.message
            assert "placeholder" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_analyze_commits_handler_exists(self, intent_service):
        """Verify analyze_commits handler exists and is callable."""
        assert hasattr(intent_service, "_handle_analyze_commits")
        assert callable(intent_service._handle_analyze_commits)

    @pytest.mark.asyncio
    async def test_analyze_commits_missing_repository(self, intent_service):
        """Test analyze_commits returns error when repository is missing."""
        intent = Intent(
            original_message="analyze commits from last week",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"timeframe": "last_week"},
            # Missing repository
        )

        result = await intent_service._handle_analyze_commits(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should fail validation
        assert result.success is False
        assert "repository" in result.message.lower()
        assert result.requires_clarification is True
        assert result.clarification_type == "repository_required"

    @pytest.mark.asyncio
    async def test_analyze_commits_no_placeholder_message(self, intent_service):
        """Verify analyze_commits doesn't return placeholder message after implementation."""
        intent = Intent(
            original_message="analyze commits in test-repo",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-org/test-repo", "timeframe": "last_week"},
        )

        result = await intent_service._handle_analyze_commits(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should NOT contain placeholder messages
        if result.success:
            assert "implementation in progress" not in result.message.lower()
            assert "placeholder" not in result.message.lower()
            assert "handler is ready" not in result.message.lower()
            # Should NOT have requires_clarification=True for successful analysis
            assert result.requires_clarification is False

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_analyze_commits_success_with_mock(self, mock_github_service, intent_service):
        """Test successful commit analysis with mocked GitHubDomainService."""
        # Mock the GitHub service and its internal _github_agent
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity to return commits
        mock_agent.get_recent_activity = AsyncMock(
            return_value={
                "commits": [
                    {
                        "sha": "abc123",
                        "commit": {
                            "message": "Test commit 1",
                            "author": {"name": "Alice", "date": "2025-10-11T10:00:00Z"},
                        },
                        "author": {"login": "alice"},
                    },
                    {
                        "sha": "def456",
                        "commit": {
                            "message": "Test commit 2",
                            "author": {"name": "Bob", "date": "2025-10-11T11:00:00Z"},
                        },
                        "author": {"login": "bob"},
                    },
                ],
                "pulls": [],
                "issues": [],
            }
        )

        intent = Intent(
            original_message="analyze commits in test-repo from last week",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-org/test-repo", "timeframe": "last_week", "days": 7},
        )

        result = await intent_service._handle_analyze_commits(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain analysis data
        assert "commit" in result.message.lower() or "analyzed" in result.message.lower()
        assert "commit_count" in result.intent_data
        assert result.intent_data["commit_count"] == 2

        # Should have repository in response
        assert result.intent_data.get("repository") == "test-org/test-repo"

    @pytest.mark.asyncio
    async def test_generate_report_handler_exists(self, intent_service):
        """Verify generate_report handler exists."""
        assert hasattr(intent_service, "_handle_generate_report")
        assert callable(intent_service._handle_generate_report)

    @pytest.mark.asyncio
    async def test_generate_report_missing_repository(self, intent_service):
        """Test generate_report returns error when repository is missing."""
        intent = Intent(
            original_message="generate commit report",
            category=IntentCategory.ANALYSIS,
            action="generate_report",
            confidence=0.90,
            context={"report_type": "commit_analysis"},
            # Missing repository
        )

        result = await intent_service._handle_generate_report(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should fail validation
        assert result.success is False
        assert "repository" in result.message.lower()
        assert result.requires_clarification is True
        assert result.clarification_type == "repository_required"

    @pytest.mark.asyncio
    async def test_generate_report_no_placeholder_message(self, intent_service):
        """Verify generate_report doesn't return placeholder message after implementation."""
        intent = Intent(
            original_message="generate report for test-repo",
            category=IntentCategory.ANALYSIS,
            action="generate_report",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                "report_type": "commit_analysis",
                "timeframe": "last_week",
            },
        )

        result = await intent_service._handle_generate_report(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should NOT contain placeholder messages
        if result.success:
            assert "implementation in progress" not in result.message.lower()
            assert "placeholder" not in result.message.lower()
            assert "needs reporting service" not in result.message.lower()
            assert result.requires_clarification is False

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_generate_report_success_with_mock(self, mock_github_service, intent_service):
        """Test successful report generation with mocked GitHubDomainService."""
        # Mock the GitHub service and its internal _github_agent
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity to return commits
        mock_agent.get_recent_activity = AsyncMock(
            return_value={
                "commits": [
                    {
                        "sha": "abc123",
                        "commit": {
                            "message": "feat: add new feature",
                            "author": {"name": "Alice", "date": "2025-10-11T10:00:00Z"},
                        },
                        "author": {"login": "alice"},
                    },
                    {
                        "sha": "def456",
                        "commit": {
                            "message": "fix: bug fix",
                            "author": {"name": "Bob", "date": "2025-10-11T11:00:00Z"},
                        },
                        "author": {"login": "bob"},
                    },
                ],
                "pulls": [],
                "issues": [],
            }
        )

        intent = Intent(
            original_message="generate commit report for test-repo",
            category=IntentCategory.ANALYSIS,
            action="generate_report",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                "report_type": "commit_analysis",
                "days": 7,
            },
        )

        result = await intent_service._handle_generate_report(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain report data
        assert "report" in result.message.lower() or "generated" in result.message.lower()
        assert "report_type" in result.intent_data
        assert result.intent_data["report_type"] == "commit_analysis"

        # Should have repository in response
        assert result.intent_data.get("repository") == "test-org/test-repo"

        # Should have report content
        assert "content" in result.intent_data or "summary" in result.intent_data

    @pytest.mark.asyncio
    async def test_analyze_data_handler_exists(self, intent_service):
        """Verify analyze_data handler exists."""
        assert hasattr(intent_service, "_handle_analyze_data")
        assert callable(intent_service._handle_analyze_data)

    @pytest.mark.asyncio
    async def test_analyze_data_missing_repository(self, intent_service):
        """Test analyze_data returns error when repository is missing."""
        intent = Intent(
            original_message="analyze data",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={"data_type": "repository_metrics"},
            # Missing repository
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should fail validation
        assert result.success is False
        assert "repository" in result.message.lower()
        assert result.requires_clarification is True
        assert result.clarification_type == "repository_required"

    @pytest.mark.asyncio
    async def test_analyze_data_unknown_data_type(self, intent_service):
        """Test analyze_data returns error for unknown data_type."""
        intent = Intent(
            original_message="analyze data with unknown type",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={"repository": "test-org/test-repo", "data_type": "unknown_type"},
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should fail validation
        assert result.success is False
        assert "unsupported" in result.message.lower() or "unknown" in result.message.lower()
        assert "data type" in result.message.lower() or "data_type" in result.message.lower()
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_data_type"

    @pytest.mark.asyncio
    async def test_analyze_data_no_placeholder_message(self, intent_service):
        """Verify analyze_data doesn't return placeholder message after implementation."""
        intent = Intent(
            original_message="analyze repository metrics",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={"repository": "test-org/test-repo", "data_type": "repository_metrics"},
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should NOT contain placeholder messages
        if result.success:
            assert "implementation in progress" not in result.message.lower()
            assert "placeholder" not in result.message.lower()
            assert "handler is ready" not in result.message.lower()
            assert "handler ready" not in result.message.lower()
            # Should NOT have requires_clarification=True for successful analysis
            assert result.requires_clarification is False

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_analyze_data_repository_metrics_success(
        self, mock_github_service, intent_service
    ):
        """Test successful repository_metrics analysis with mocked GitHubDomainService."""
        # Mock the GitHub service and its internal _github_agent
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity to return comprehensive activity data
        mock_agent.get_recent_activity = AsyncMock(
            return_value={
                "commits": [
                    {
                        "sha": "abc123",
                        "commit": {"message": "Commit 1", "author": {"name": "Alice"}},
                    },
                    {"sha": "def456", "commit": {"message": "Commit 2", "author": {"name": "Bob"}}},
                    {
                        "sha": "ghi789",
                        "commit": {"message": "Commit 3", "author": {"name": "Alice"}},
                    },
                ],
                "prs": [
                    {"number": 1, "title": "PR 1", "author": "alice"},
                    {"number": 2, "title": "PR 2", "author": "bob"},
                ],
                "issues_created": [
                    {"number": 10, "title": "Issue 10", "author": "charlie"},
                ],
                "issues_closed": [
                    {"number": 11, "title": "Issue 11", "author": "alice"},
                    {"number": 12, "title": "Issue 12", "author": "bob"},
                ],
            }
        )

        intent = Intent(
            original_message="analyze repository metrics",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                "data_type": "repository_metrics",
                "days": 7,
            },
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain metrics
        assert "metrics" in result.intent_data
        metrics = result.intent_data["metrics"]

        # Verify counts
        assert metrics["commits_count"] == 3
        assert metrics["prs_count"] == 2
        assert metrics["issues_created_count"] == 1
        assert metrics["issues_closed_count"] == 2
        assert metrics["total_activity_count"] == 8  # 3 + 2 + 1 + 2

        # Verify distribution is present
        assert "activity_distribution" in metrics
        assert "commits" in metrics["activity_distribution"]
        assert "prs" in metrics["activity_distribution"]

        # Verify metadata
        assert result.intent_data.get("repository") == "test-org/test-repo"
        assert result.intent_data.get("data_type") == "repository_metrics"
        assert result.intent_data.get("days") == 7

        # Message should mention analysis
        assert "analyzed" in result.message.lower() or "metrics" in result.message.lower()

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_analyze_data_activity_trends_success(self, mock_github_service, intent_service):
        """Test successful activity_trends analysis with mocked GitHubDomainService."""
        # Mock the GitHub service and its internal _github_agent
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity
        mock_agent.get_recent_activity = AsyncMock(
            return_value={
                "commits": [
                    {
                        "sha": f"commit{i}",
                        "commit": {"message": f"Commit {i}", "author": {"name": "Alice"}},
                    }
                    for i in range(10)  # 10 commits
                ],
                "prs": [
                    {"number": 1, "title": "PR 1", "author": "alice"},
                ],
                "issues_created": [
                    {"number": 10, "title": "Issue 10", "author": "bob"},
                    {"number": 11, "title": "Issue 11", "author": "bob"},
                ],
                "issues_closed": [
                    {"number": 12, "title": "Issue 12", "author": "alice"},
                ],
            }
        )

        intent = Intent(
            original_message="analyze activity trends",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={"repository": "test-org/test-repo", "data_type": "activity_trends", "days": 7},
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain metrics and trends
        assert "metrics" in result.intent_data
        assert "trends" in result.intent_data

        trends = result.intent_data["trends"]

        # Verify trends analysis
        assert "most_active_type" in trends
        assert trends["most_active_type"] == "commits"  # 10 commits is most

        # Should have insights
        assert "insights" in result.intent_data
        assert len(result.intent_data["insights"]) > 0

        # Verify metadata
        assert result.intent_data.get("data_type") == "activity_trends"

        # Message should mention trends or activity
        assert "trends" in result.message.lower() or "activity" in result.message.lower()

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_analyze_data_contributor_stats_success(
        self, mock_github_service, intent_service
    ):
        """Test successful contributor_stats analysis with mocked GitHubDomainService."""
        # Mock the GitHub service and its internal _github_agent
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity with multiple contributors
        mock_agent.get_recent_activity = AsyncMock(
            return_value={
                "commits": [
                    {
                        "sha": "abc1",
                        "commit": {"message": "C1", "author": {"name": "Alice"}},
                        "author": {"login": "alice"},
                    },
                    {
                        "sha": "abc2",
                        "commit": {"message": "C2", "author": {"name": "Alice"}},
                        "author": {"login": "alice"},
                    },
                    {
                        "sha": "abc3",
                        "commit": {"message": "C3", "author": {"name": "Bob"}},
                        "author": {"login": "bob"},
                    },
                ],
                "prs": [
                    {"number": 1, "title": "PR 1", "author": "alice"},
                    {"number": 2, "title": "PR 2", "author": "charlie"},
                ],
                "issues_created": [
                    {"number": 10, "title": "Issue 10", "author": "bob"},
                ],
                "issues_closed": [],
            }
        )

        intent = Intent(
            original_message="analyze contributor stats",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                "data_type": "contributor_stats",
                "days": 7,
            },
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain metrics and contributors
        assert "metrics" in result.intent_data
        assert "contributors" in result.intent_data

        metrics = result.intent_data["metrics"]
        contributors = result.intent_data["contributors"]

        # Verify contributor metrics
        assert "total_contributors" in metrics
        assert metrics["total_contributors"] >= 3  # Alice, Bob, Charlie

        # Verify contributors breakdown
        assert "commits" in contributors
        assert contributors["commits"]["Alice"] == 2
        assert contributors["commits"]["Bob"] == 1

        # Should have insights
        assert "insights" in result.intent_data
        assert len(result.intent_data["insights"]) > 0

        # Verify metadata
        assert result.intent_data.get("data_type") == "contributor_stats"

        # Message should mention contributors or stats
        assert "contributor" in result.message.lower() or "stats" in result.message.lower()

    @pytest.mark.asyncio
    @patch("services.domain.github_domain_service.GitHubDomainService")
    async def test_analyze_data_empty_activity_graceful(self, mock_github_service, intent_service):
        """Test analyze_data handles empty activity data gracefully."""
        # Mock the GitHub service with empty data
        mock_service_instance = mock_github_service.return_value
        mock_agent = Mock()
        mock_service_instance._github_agent = mock_agent

        # Mock get_recent_activity with no activity
        mock_agent.get_recent_activity = AsyncMock(
            return_value={"commits": [], "prs": [], "issues_created": [], "issues_closed": []}
        )

        intent = Intent(
            original_message="analyze repository metrics",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                "data_type": "repository_metrics",
                "days": 7,
            },
        )

        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should succeed even with empty data
        assert result.success is True
        assert result.requires_clarification is False

        # Should have zero counts
        assert "metrics" in result.intent_data
        metrics = result.intent_data["metrics"]
        assert metrics["total_activity_count"] == 0
        assert metrics["commits_count"] == 0
        assert metrics["prs_count"] == 0

        # Should not crash or raise exceptions

    @pytest.mark.asyncio
    async def test_analyze_data_defaults_to_repository_metrics(self, intent_service):
        """Test analyze_data defaults to repository_metrics when data_type not specified."""
        intent = Intent(
            original_message="analyze data for repo",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=0.90,
            context={
                "repository": "test-org/test-repo",
                # data_type not specified - should default to repository_metrics
            },
        )

        # Don't need full mock - just verify it routes correctly without error
        result = await intent_service._handle_analyze_data(
            intent=intent, workflow_id="test-workflow-456"
        )

        # Should attempt to analyze (may succeed or fail depending on service availability)
        # But should not fail validation
        assert result is not None

        # If it succeeded, should use default data_type
        if result.success:
            assert result.intent_data.get("data_type") == "repository_metrics"

    @pytest.mark.asyncio
    async def test_generic_analysis_routes_to_orchestration(self, intent_service):
        """Verify generic ANALYSIS actions route to orchestration."""
        intent = Intent(
            original_message="analyze something",
            category=IntentCategory.ANALYSIS,
            action="unknown_analysis",
            confidence=0.85,
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            result = await intent_service.process_intent("analyze something", session_id="test")

            # Should route to orchestration, not return placeholder
            assert "Phase 3" not in result.message
            assert result.message is not None


class TestHandlerIntegration:
    """Test handler integration and routing."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "test-workflow-789"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService()

    @pytest.mark.asyncio
    async def test_execution_routing_exists(self, intent_service):
        """Verify main routing handles EXECUTION category."""
        # Check that _handle_execution_intent exists
        assert hasattr(intent_service, "_handle_execution_intent")

    @pytest.mark.asyncio
    async def test_analysis_routing_exists(self, intent_service):
        """Verify main routing handles ANALYSIS category."""
        # Check that _handle_analysis_intent exists
        assert hasattr(intent_service, "_handle_analysis_intent")

    @pytest.mark.asyncio
    async def test_no_generic_intent_fallback(self, intent_service):
        """Verify old _handle_generic_intent placeholder is removed."""
        # The old placeholder method should not exist or should not be called
        # for EXECUTION/ANALYSIS

        # If method exists, it should not be used for EXECUTION/ANALYSIS
        if hasattr(intent_service, "_handle_generic_intent"):
            # Check it's not called in main routing
            import inspect

            source = inspect.getsource(intent_service.process_intent)

            # Should have specific handlers for EXECUTION/ANALYSIS
            assert "_handle_execution_intent" in source or "EXECUTION" in source
            assert "_handle_analysis_intent" in source or "ANALYSIS" in source

    @pytest.mark.asyncio
    async def test_execution_handler_routing_works(self, intent_service):
        """Test that EXECUTION intents properly route to execution handler."""
        intent = Intent(
            original_message="create issue",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.95,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            # Should not raise exception and should return result
            result = await intent_service.process_intent("create issue", session_id="test")
            assert result is not None
            assert hasattr(result, "success")
            assert hasattr(result, "message")

    @pytest.mark.asyncio
    async def test_analysis_handler_routing_works(self, intent_service):
        """Test that ANALYSIS intents properly route to analysis handler."""
        intent = Intent(
            original_message="analyze commits",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.90,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _stub_classifier(mock_classifier, intent)

            # Should not raise exception and should return result
            result = await intent_service.process_intent("analyze commits", session_id="test")
            assert result is not None
            assert hasattr(result, "success")
            assert hasattr(result, "message")
