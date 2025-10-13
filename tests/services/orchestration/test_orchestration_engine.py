"""
Test coverage for OrchestrationEngine
Tests the core orchestration logic without external dependencies
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.models import Intent, IntentCategory, Task, UploadedFile, Workflow
from services.orchestration.engine import OrchestrationEngine, TaskResult
from services.shared_types import TaskStatus, TaskType, WorkflowStatus, WorkflowType


class TestOrchestrationEngine:
    """Test OrchestrationEngine core functionality"""

    @pytest.fixture
    def engine(self):
        """Create a fresh OrchestrationEngine instance for each test"""
        return OrchestrationEngine()

    @pytest.fixture
    def mock_intent(self):
        """Create a mock analyze_file intent"""
        return Intent(
            id="test-intent-123",
            category=IntentCategory.ANALYSIS,
            action="analyze_file",
            confidence=0.95,
            context={"file_id": "test-file-123", "filename": "test.csv"},
        )

    @pytest.fixture
    def mock_workflow(self):
        """Create a mock workflow with analyze_file task"""
        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.ANALYZE_FILE,
            status=WorkflowStatus.PENDING,
            context={"file_id": "test-file-123", "filename": "test.csv"},
        )
        task = Task(
            id="test-task-123",
            name="Analyze File",
            type=TaskType.ANALYZE_FILE,
            status=TaskStatus.PENDING,
        )
        workflow.tasks.append(task)
        return workflow

    @pytest.fixture
    def mock_file_metadata(self):
        """Create mock file metadata"""
        return UploadedFile(
            id="test-file-123",
            session_id="test-session",
            filename="test.csv",
            file_type="text/csv",
            file_size=1024,
            storage_path="tests/fixtures/sample_data.csv",
            upload_time=datetime.now(),
        )

    @pytest.mark.asyncio
    async def test_create_workflow_from_intent_success(self, engine, mock_intent):
        """Test successful workflow creation from intent"""
        # Mock the factory to return a workflow
        mock_workflow = Mock(spec=Workflow)
        mock_workflow.id = "test-workflow-123"
        mock_workflow.type = WorkflowType.CREATE_TICKET
        mock_workflow.status = WorkflowStatus.PENDING
        mock_workflow.tasks = []
        mock_workflow.context = {}

        with patch.object(
            engine.factory, "create_from_intent", new_callable=AsyncMock
        ) as mock_factory:
            mock_factory.return_value = mock_workflow

            # Mock database persistence
            with patch.object(
                engine, "_persist_workflow_to_database", new_callable=AsyncMock
            ) as mock_persist:
                result = await engine.create_workflow_from_intent(mock_intent)

        # Verify workflow was created and stored
        assert result is not None
        assert result.id == "test-workflow-123"
        assert engine.workflows["test-workflow-123"] == mock_workflow

        # Verify factory was called
        mock_factory.assert_called_once_with(mock_intent)

        # Verify persistence was called
        mock_persist.assert_called_once_with(mock_workflow)

    @pytest.mark.asyncio
    async def test_create_workflow_from_intent_failure(self, engine, mock_intent):
        """Test workflow creation when factory returns None"""
        with patch.object(
            engine.factory, "create_from_intent", new_callable=AsyncMock
        ) as mock_factory:
            mock_factory.return_value = None

            result = await engine.create_workflow_from_intent(mock_intent)

        # Verify no workflow was created
        assert result is None
        assert len(engine.workflows) == 0

    @pytest.mark.asyncio
    async def test_execute_workflow_not_found(self, engine):
        """Test executing a non-existent workflow"""
        with pytest.raises(ValueError, match="Workflow test-missing not found"):
            await engine.execute_workflow("test-missing")

    @pytest.mark.asyncio
    async def test_analyze_file_success(self, engine, mock_workflow, mock_file_metadata):
        """Test successful file analysis execution"""
        # Mock database pool and file repository
        mock_pool = AsyncMock()
        mock_file_repo = AsyncMock()
        mock_file_repo.get_file_by_id.return_value = mock_file_metadata

        # Create a simple object instead of Mock to avoid configuration issues
        class MockAnalysisResult:
            def __init__(self):
                self.summary = "Test analysis summary"
                self.key_findings = ["Finding 1", "Finding 2"]
                self.metadata = {"row_count": 10}
                self.generated_at = datetime.now()
                self.analysis_type = Mock()
                self.analysis_type.value = "data"

        mock_analysis_result = MockAnalysisResult()

        mock_file_analyzer = AsyncMock()
        mock_file_analyzer.analyze_file.return_value = mock_analysis_result

        # Fix import paths - patch the actual import locations
        with (
            # DatabasePool removed - AsyncSessionFactory pattern now used
            patch(
                "services.repositories.file_repository.FileRepository",
                return_value=mock_file_repo,
            ),
            patch(
                "services.analysis.file_analyzer.FileAnalyzer",
                return_value=mock_file_analyzer,
            ),
            patch("services.analysis.analyzer_factory.AnalyzerFactory", return_value=Mock()),
        ):

            # Get the analyze_file task
            task = mock_workflow.tasks[0]

            # Execute the task
            result = await engine._analyze_file(mock_workflow, task)

        # Verify success
        assert result.success is True
        assert "analysis" in result.output_data
        assert result.output_data["file_id"] == "test-file-123"
        assert result.output_data["filename"] == "test.csv"

        # Verify file repository was called
        mock_file_repo.get_file_by_id.assert_called_once_with("test-file-123")

        # Verify FileAnalyzer was called
        mock_file_analyzer.analyze_file.assert_called_once()

    @pytest.mark.asyncio
    async def test_analyze_file_missing_file_id(self, engine, mock_workflow):
        """Test file analysis with missing file ID in context"""
        # Remove file_id from context
        mock_workflow.context = {}

        task = mock_workflow.tasks[0]
        result = await engine._analyze_file(mock_workflow, task)

        # Verify failure
        assert result.success is False
        assert "No file ID found in workflow context" in result.error

    @pytest.mark.asyncio
    async def test_analyze_file_file_not_found(self, engine, mock_workflow):
        """Test file analysis when file is not found in database"""
        # Mock database pool and file repository
        mock_pool = AsyncMock()
        mock_file_repo = AsyncMock()
        mock_file_repo.get_file_by_id.return_value = None  # File not found

        # Fix import paths
        with (
            # DatabasePool removed - AsyncSessionFactory pattern now used
            patch(
                "services.repositories.file_repository.FileRepository",
                return_value=mock_file_repo,
            ),
        ):

            task = mock_workflow.tasks[0]
            result = await engine._analyze_file(mock_workflow, task)

        # Verify failure
        assert result.success is False
        assert "File not found: test-file-123" in result.error

    @pytest.mark.asyncio
    async def test_analyze_file_analysis_exception(self, engine, mock_workflow, mock_file_metadata):
        """Test file analysis when FileAnalyzer raises an exception"""
        # Mock database pool and file repository
        mock_pool = AsyncMock()
        mock_file_repo = AsyncMock()
        mock_file_repo.get_file_by_id.return_value = mock_file_metadata

        # Mock FileAnalyzer to raise exception
        mock_file_analyzer = AsyncMock()
        mock_file_analyzer.analyze_file.side_effect = Exception("Analysis failed")

        # Fix import paths
        with (
            # DatabasePool removed - AsyncSessionFactory pattern now used
            patch(
                "services.repositories.file_repository.FileRepository",
                return_value=mock_file_repo,
            ),
            patch(
                "services.analysis.file_analyzer.FileAnalyzer",
                return_value=mock_file_analyzer,
            ),
            patch("services.analysis.analyzer_factory.AnalyzerFactory", return_value=Mock()),
        ):

            task = mock_workflow.tasks[0]
            result = await engine._analyze_file(mock_workflow, task)

        # Verify failure
        assert result.success is False
        assert "Analysis error: Analysis failed" in result.error

    @pytest.mark.asyncio
    async def test_task_handler_registration(self, engine):
        """Test that all required task handlers are registered"""
        expected_handlers = [
            TaskType.ANALYZE_REQUEST,
            TaskType.EXTRACT_REQUIREMENTS,
            TaskType.IDENTIFY_DEPENDENCIES,
            TaskType.CREATE_WORK_ITEM,
            TaskType.NOTIFY_STAKEHOLDERS,
            TaskType.ANALYZE_GITHUB_ISSUE,
            TaskType.ANALYZE_FILE,
            TaskType.GITHUB_CREATE_ISSUE,
            TaskType.JIRA_CREATE_TICKET,
            TaskType.SLACK_SEND_MESSAGE,
            TaskType.GENERATE_DOCUMENT,
            TaskType.CREATE_SUMMARY,
        ]

        for task_type in expected_handlers:
            assert task_type in engine.task_handlers
            assert callable(engine.task_handlers[task_type])

    @pytest.mark.asyncio
    async def test_placeholder_handler(self, engine, mock_workflow):
        """Test placeholder handler for unimplemented task types"""
        # Create a task with placeholder type
        task = Task(
            id="test-placeholder-task",
            name="Placeholder Task",
            type=TaskType.GITHUB_CREATE_ISSUE,  # This uses placeholder handler
            status=TaskStatus.PENDING,
        )

        result = await engine._placeholder_handler(mock_workflow, task)

        # Verify placeholder behavior
        assert result.success is True
        assert result.output_data["placeholder"] is True

    @pytest.mark.asyncio
    async def test_workflow_state_transitions(self, engine):
        """Test workflow state transitions through execution using real domain models"""
        from services.domain.models import (
            Task,
            TaskStatus,
            TaskType,
            Workflow,
            WorkflowStatus,
            WorkflowType,
        )

        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            tasks=[
                Task(
                    id="task-1",
                    name="Create Work Item",
                    type=TaskType.CREATE_WORK_ITEM,
                    status=TaskStatus.PENDING,
                )
            ],
            context={},
        )
        engine.workflows[workflow.id] = workflow

        # Simulate execution (mock only the actual task execution)
        def complete_task_side_effect(workflow_obj, task_obj):
            task_obj.status = TaskStatus.COMPLETED
            return None

        with patch.object(engine, "_execute_task", new_callable=AsyncMock) as mock_exec_task:
            mock_exec_task.side_effect = complete_task_side_effect
            result = await engine.execute_workflow(workflow.id)

        # Assert workflow is now complete or in expected state
        assert result is not None
        assert workflow.is_complete() or all(t.status != TaskStatus.PENDING for t in workflow.tasks)

    @pytest.mark.asyncio
    async def test_workflow_error_handling(self, engine):
        """Test workflow error handling and status updates using real domain models"""
        from services.domain.models import (
            Task,
            TaskStatus,
            TaskType,
            Workflow,
            WorkflowStatus,
            WorkflowType,
        )

        workflow = Workflow(
            id="test-workflow-123",
            type=WorkflowType.CREATE_TICKET,
            status=WorkflowStatus.PENDING,
            tasks=[
                Task(
                    id="task-1",
                    name="Create Work Item",
                    type=TaskType.CREATE_WORK_ITEM,
                    status=TaskStatus.PENDING,
                )
            ],
            context={},
        )
        engine.workflows[workflow.id] = workflow

        # Simulate execution failure
        with patch.object(engine, "_execute_task", new_callable=AsyncMock) as mock_exec_task:
            mock_exec_task.side_effect = Exception("Task execution failed")
            with pytest.raises(Exception):
                await engine.execute_workflow(workflow.id)

        # Assert workflow status was updated to failed
        assert workflow.status == WorkflowStatus.FAILED
        assert workflow.error is not None
