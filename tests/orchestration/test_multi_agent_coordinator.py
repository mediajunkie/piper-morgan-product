"""
Comprehensive unit tests for MultiAgentCoordinator

Tests comprehensive task decomposition, agent selection, performance targets,
error handling, and coordination flows for PM-033d implementation.
"""

import asyncio
import time
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    AgentCapability,
    AgentType,
    CoordinationResult,
    CoordinationStatus,
    MultiAgentCoordinator,
    SubTask,
    TaskComplexity,
    TaskDecomposer,
)
from services.shared_types import IntentCategory, TaskStatus


class TestTaskDecomposer:
    """Test TaskDecomposer functionality"""

    @pytest.fixture
    def decomposer(self):
        """Create a fresh TaskDecomposer instance for each test"""
        return TaskDecomposer()

    @pytest.fixture
    def simple_intent(self):
        """Create a simple intent for testing"""
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.QUERY,
            action="get_status",
            original_message="Get current system status",
            confidence=0.9,
        )

    @pytest.fixture
    def moderate_intent(self):
        """Create a moderate complexity intent.

        #1026 fix (2026-05-16): original message "Implement new API endpoint
        with validation and tests" triggered multiple domain expansions in
        `_identify_required_domains` (testing via "validation"/"tests" +
        integration via "api") which combined with the EXECUTION-category
        default 2 domains ("orchestration", "workflows") landed at >2 domains
        → COMPLEX classification → `_create_complex_subtasks` returned 4
        subtasks (architecture + implementation + tests + integration),
        breaking the moderate-path test.

        Tightened the message to stay at EXECUTION-category default 2 domains
        (no domain-trigger keywords: no "test/validation/verify", no
        "api/integration/slack/github", no "database/repository/schema",
        no "interface/frontend/web/user", no "docs/documentation/guide").
        Keeps the "implement" keyword in the action so `_create_moderate_subtasks`
        fires its Implementation pattern (core + tests = 2 subtasks).

        Test for cross-agent classification is the responsibility of
        `test_analyze_complexity_cross_agent_capabilities` below.
        """
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.EXECUTION,
            action="implement_feature",
            original_message="Implement new feature",
            confidence=0.95,
        )

    @pytest.fixture
    def complex_intent(self):
        """Create a complex intent requiring multi-agent coordination"""
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.EXECUTION,
            action="refactor_architecture",
            original_message="Refactor entire system architecture with microservices migration, database changes, and comprehensive testing",
            confidence=0.98,
        )

    def test_agent_capabilities_initialization(self, decomposer):
        """Test that agent capabilities are properly initialized"""
        capabilities = decomposer.agent_capabilities

        # Verify both agent types are present
        assert AgentType.CODE in capabilities
        assert AgentType.CURSOR in capabilities

        # Verify CODE agent capabilities
        code_agent = capabilities[AgentType.CODE]
        assert isinstance(code_agent, AgentCapability)
        assert code_agent.agent_type == AgentType.CODE
        assert "infrastructure" in code_agent.strengths
        assert "backend_services" in code_agent.strengths
        assert "orchestration" in code_agent.domains
        assert code_agent.performance_rating == 0.95
        assert code_agent.availability is True

        # Verify CURSOR agent capabilities
        cursor_agent = capabilities[AgentType.CURSOR]
        assert isinstance(cursor_agent, AgentCapability)
        assert cursor_agent.agent_type == AgentType.CURSOR
        assert "testing_frameworks" in cursor_agent.strengths
        assert "ui_components" in cursor_agent.strengths
        assert "tests" in cursor_agent.domains
        assert cursor_agent.performance_rating == 0.90
        assert cursor_agent.availability is True

    @pytest.mark.asyncio
    async def test_decompose_simple_task(self, decomposer, simple_intent):
        """Test decomposition of simple task results in single subtask"""
        context = {"user_session": "test_session"}

        subtasks = await decomposer.decompose_task(simple_intent, context)

        # Simple task should result in single subtask
        assert len(subtasks) == 1

        subtask = subtasks[0]
        assert isinstance(subtask, SubTask)
        assert subtask.id == f"{simple_intent.id}_simple"
        assert subtask.title == simple_intent.action
        assert subtask.complexity == TaskComplexity.SIMPLE
        assert subtask.assigned_agent is not None
        assert subtask.status == TaskStatus.PENDING
        assert isinstance(subtask.created_at, datetime)

    @pytest.mark.asyncio
    async def test_decompose_moderate_task(self, decomposer, moderate_intent):
        """Test decomposition of moderate complexity task"""
        context = {"user_session": "test_session"}

        subtasks = await decomposer.decompose_task(moderate_intent, context)

        # Moderate task should result in 2-3 subtasks (core + tests)
        assert len(subtasks) in [
            1,
            2,
            3,
        ]  # Can be 1 if treated as simple, or 2-3 for implementation pattern

        for subtask in subtasks:
            assert isinstance(subtask, SubTask)
            assert subtask.assigned_agent is not None
            assert subtask.status == TaskStatus.PENDING
            assert subtask.estimated_duration_minutes > 0

    @pytest.mark.asyncio
    async def test_decompose_complex_task(self, decomposer, complex_intent):
        """Test decomposition of complex task requiring multi-agent coordination"""
        context = {"user_session": "test_session"}

        subtasks = await decomposer.decompose_task(complex_intent, context)

        # Complex task should result in multiple subtasks (4 in the current pattern)
        assert len(subtasks) >= 3  # At least 3 subtasks for complex coordination

        # Verify task structure follows complex pattern
        subtask_ids = [task.id for task in subtasks]
        assert any("architecture" in task_id for task_id in subtask_ids)
        assert any("implementation" in task_id for task_id in subtask_ids)

        # Verify dependencies are set correctly
        dependency_count = sum(len(task.dependencies) for task in subtasks)
        assert dependency_count > 0  # Complex tasks should have dependencies

    def test_analyze_complexity_simple(self, decomposer, simple_intent):
        """Test complexity analysis for simple tasks"""
        context = {}

        complexity = decomposer._analyze_complexity(simple_intent, context)

        assert complexity == TaskComplexity.SIMPLE

    def test_analyze_complexity_multi_domain(self, decomposer):
        """Test complexity analysis detects multi-domain requirements"""
        # Create intent requiring multiple domains
        intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="implement_full_stack_feature",
            original_message="Implement database schema, backend API, frontend UI, and comprehensive testing documentation",
            confidence=0.95,
        )
        context = {}

        complexity = decomposer._analyze_complexity(intent, context)

        # Should be complex due to multiple domains
        assert complexity == TaskComplexity.COMPLEX

    def test_analyze_complexity_cross_agent_capabilities(self, decomposer):
        """Test complexity analysis detects cross-agent capability requirements"""
        intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="implement_with_testing",
            original_message="Implement infrastructure backend services with comprehensive testing frameworks and UI validation",
            confidence=0.95,
        )
        context = {}

        complexity = decomposer._analyze_complexity(intent, context)

        # Should be complex due to requiring both CODE and CURSOR capabilities
        assert complexity == TaskComplexity.COMPLEX

    def test_identify_required_domains(self, decomposer):
        """Test domain identification from intent"""
        intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="create_database_api",
            original_message="Create database repository with REST API integration",
            confidence=0.95,
        )
        context = {}

        domains = decomposer._identify_required_domains(intent, context)

        # Should identify database and integration domains
        assert "database" in domains or "orchestration" in domains
        assert len(domains) > 0

    def test_identify_required_capabilities(self, decomposer):
        """Test capability identification from intent"""
        intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="test_implementation",
            original_message="Implement testing frameworks with UI validation",
            confidence=0.95,
        )
        context = {}

        capabilities = decomposer._identify_required_capabilities(intent, context)

        # Should identify testing and UI capabilities
        assert "testing_frameworks" in capabilities or "ui_components" in capabilities
        assert len(capabilities) > 0

    def test_estimate_duration(self, decomposer):
        """Test duration estimation"""
        # Simple query intent
        simple_intent = Intent(
            id="test_simple",
            category=IntentCategory.QUERY,
            action="get_info",
            original_message="Get information",
            confidence=0.9,
        )

        # Complex execution intent
        complex_intent = Intent(
            id="test_complex",
            category=IntentCategory.EXECUTION,
            action="implement_create_build_develop_integrate",
            original_message="Implement create build develop integrate optimize",
            confidence=0.95,
        )

        simple_duration = decomposer._estimate_duration(simple_intent, {})
        complex_duration = decomposer._estimate_duration(complex_intent, {})

        # Complex intent should take longer
        assert complex_duration > simple_duration
        assert simple_duration >= 15  # Minimum reasonable duration
        assert complex_duration >= 60  # Complex tasks should be substantial

    def test_select_best_agent_code_capabilities(self, decomposer):
        """Test agent selection for CODE agent capabilities"""
        required_caps = {"infrastructure", "backend_services"}

        selected_agent = decomposer._select_best_agent(required_caps)

        assert selected_agent == AgentType.CODE

    def test_select_best_agent_cursor_capabilities(self, decomposer):
        """Test agent selection for CURSOR agent capabilities"""
        required_caps = {"testing_frameworks", "ui_components"}

        selected_agent = decomposer._select_best_agent(required_caps)

        assert selected_agent == AgentType.CURSOR

    def test_select_best_agent_no_match(self, decomposer):
        """Test agent selection with no clear capability match"""
        required_caps = {"unknown_capability"}

        selected_agent = decomposer._select_best_agent(required_caps)

        # Should default to CODE agent
        assert selected_agent == AgentType.CODE

    @pytest.mark.asyncio
    async def test_create_simple_subtask(self, decomposer, simple_intent):
        """Test creation of simple subtask"""
        context = {}

        subtasks = await decomposer._create_simple_subtask(simple_intent, context)

        assert len(subtasks) == 1
        subtask = subtasks[0]
        assert subtask.id == f"{simple_intent.id}_simple"
        assert subtask.complexity == TaskComplexity.SIMPLE
        assert subtask.assigned_agent is not None

    @pytest.mark.asyncio
    async def test_create_moderate_subtasks_implementation(self, decomposer):
        """Test creation of moderate subtasks for implementation pattern"""
        intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="implement_service",
            original_message="Implement new microservice",
            confidence=0.95,
        )
        context = {}

        subtasks = await decomposer._create_moderate_subtasks(intent, context)

        # Should create core + tests pattern
        assert len(subtasks) >= 1

        if len(subtasks) > 1:
            # Check for implementation pattern
            subtask_ids = [task.id for task in subtasks]
            assert any("core" in task_id for task_id in subtask_ids)

    @pytest.mark.asyncio
    async def test_create_complex_subtasks(self, decomposer, complex_intent):
        """Test creation of complex subtasks with proper dependencies"""
        context = {}

        subtasks = await decomposer._create_complex_subtasks(complex_intent, context)

        # Should create architecture + implementation + integration + validation
        assert len(subtasks) == 4

        subtask_ids = [task.id for task in subtasks]
        assert any("architecture" in task_id for task_id in subtask_ids)
        assert any("core_implementation" in task_id for task_id in subtask_ids)
        assert any("integration" in task_id for task_id in subtask_ids)
        assert any("validation" in task_id for task_id in subtask_ids)

        # Verify dependencies
        for subtask in subtasks:
            if "core_implementation" in subtask.id:
                assert any("architecture" in dep for dep in subtask.dependencies)
            elif "integration" in subtask.id:
                assert any("core_implementation" in dep for dep in subtask.dependencies)
            elif "validation" in subtask.id:
                assert any("integration" in dep for dep in subtask.dependencies)

    @pytest.mark.asyncio
    async def test_decompose_task_error_handling(self, decomposer):
        """Test error handling in task decomposition"""
        # Create invalid intent that might cause errors
        invalid_intent = Intent(
            id="test_intent",
            category=IntentCategory.EXECUTION,
            action="",  # Empty action
            original_message="",  # Empty message
            confidence=0.0,
        )
        context = {}

        # Mock _analyze_complexity to raise an exception
        with patch.object(
            decomposer, "_analyze_complexity", side_effect=Exception("Analysis failed")
        ):
            subtasks = await decomposer.decompose_task(invalid_intent, context)

        # Should return fallback subtask
        assert len(subtasks) == 1
        subtask = subtasks[0]
        assert "fallback" in subtask.id
        assert subtask.assigned_agent == AgentType.CODE
        assert subtask.complexity == TaskComplexity.MODERATE

    def test_performance_analyze_complexity(self, decomposer, complex_intent):
        """Test performance of complexity analysis"""
        context = {}

        start_time = time.time()
        for _ in range(100):  # Run 100 iterations
            decomposer._analyze_complexity(complex_intent, context)
        duration_ms = (time.time() - start_time) * 1000

        # Should complete 100 analyses in reasonable time
        assert duration_ms < 1000  # Less than 1 second for 100 analyses


class TestMultiAgentCoordinator:
    """Test MultiAgentCoordinator functionality"""

    @pytest.fixture
    def coordinator(self):
        """Create a fresh MultiAgentCoordinator instance for each test"""
        return MultiAgentCoordinator()

    @pytest.fixture
    def test_intent(self):
        """Create a test intent for coordination"""
        return Intent(
            id=f"intent_{uuid4().hex[:8]}",
            category=IntentCategory.EXECUTION,
            action="test_coordination",
            original_message="Test multi-agent coordination",
            confidence=0.95,
        )

    @pytest.mark.asyncio
    async def test_coordinate_task_success(self, coordinator, test_intent):
        """Test successful task coordination"""
        context = {"user_session": "test_session"}

        result = await coordinator.coordinate_task(test_intent, context)

        assert isinstance(result, CoordinationResult)
        assert result.coordination_id.startswith("coord_")
        assert result.status == CoordinationStatus.ASSIGNED
        assert len(result.subtasks) > 0
        assert result.success_rate == 1.0
        assert result.total_duration_ms >= 0
        assert AgentType.CODE in result.agent_performance
        assert AgentType.CURSOR in result.agent_performance

    @pytest.mark.asyncio
    async def test_coordinate_task_performance_target(self, coordinator, test_intent):
        """Test that coordination meets <1000ms performance target"""
        context = {}

        start_time = time.time()
        result = await coordinator.coordinate_task(test_intent, context)
        actual_duration_ms = (time.time() - start_time) * 1000

        # Verify coordination completed within target
        assert (
            result.total_duration_ms < 1000
        ), f"Coordination took {result.total_duration_ms}ms, target is <1000ms"
        assert actual_duration_ms < 2000  # Allow some overhead for test execution

    @pytest.mark.asyncio
    async def test_coordinate_task_no_context(self, coordinator, test_intent):
        """Test coordination with no context provided"""
        result = await coordinator.coordinate_task(test_intent)

        assert isinstance(result, CoordinationResult)
        assert result.status == CoordinationStatus.ASSIGNED
        assert len(result.subtasks) > 0

    @pytest.mark.asyncio
    async def test_coordinate_task_error_handling(self, coordinator, test_intent):
        """Test coordination error handling"""
        # Mock task decomposer to raise an exception
        with patch.object(
            coordinator.task_decomposer,
            "decompose_task",
            side_effect=Exception("Decomposition failed"),
        ):
            result = await coordinator.coordinate_task(test_intent)

        assert isinstance(result, CoordinationResult)
        assert result.status == CoordinationStatus.FAILED
        assert result.success_rate == 0.0
        assert result.error_details == "Decomposition failed"
        assert len(result.subtasks) == 0

    @pytest.mark.asyncio
    async def test_validate_agent_assignments(self, coordinator):
        """Test agent assignment validation"""
        # Create test subtasks with and without assignments
        subtasks = [
            SubTask(
                id="task_1",
                title="Test Task 1",
                description="Description 1",
                estimated_duration_minutes=30,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["infrastructure"],
                dependencies=[],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_2",
                title="Test Task 2",
                description="Description 2",
                estimated_duration_minutes=45,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["testing_frameworks"],
                dependencies=[],
                assigned_agent=None,  # No assignment
            ),
        ]

        validated_tasks = await coordinator._validate_agent_assignments(subtasks)

        assert len(validated_tasks) == 2
        # First task should keep its assignment
        assert validated_tasks[0].assigned_agent == AgentType.CODE
        # Second task should be auto-assigned based on capabilities
        assert validated_tasks[1].assigned_agent == AgentType.CURSOR

    @pytest.mark.asyncio
    async def test_validate_agent_assignments_suboptimal(self, coordinator):
        """Test validation detects and corrects suboptimal assignments"""
        # Create subtask with suboptimal assignment
        subtasks = [
            SubTask(
                id="task_1",
                title="Test Task 1",
                description="Description 1",
                estimated_duration_minutes=30,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["testing_frameworks"],  # CURSOR capability
                dependencies=[],
                assigned_agent=AgentType.CODE,  # Suboptimal assignment
            ),
        ]

        validated_tasks = await coordinator._validate_agent_assignments(subtasks)

        # Should be reassigned to CURSOR agent
        assert validated_tasks[0].assigned_agent == AgentType.CURSOR

    @pytest.mark.asyncio
    async def test_setup_coordination_protocol(self, coordinator):
        """Test coordination protocol setup"""
        subtasks = [
            SubTask(
                id="task_1",
                title="Architecture",
                description="Design architecture",
                estimated_duration_minutes=60,
                complexity=TaskComplexity.MODERATE,
                required_capabilities=["infrastructure"],
                dependencies=[],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_2",
                title="Implementation",
                description="Implement features",
                estimated_duration_minutes=90,
                complexity=TaskComplexity.MODERATE,
                required_capabilities=["backend_services"],
                dependencies=["task_1"],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_3",
                title="Testing",
                description="Create tests",
                estimated_duration_minutes=45,
                complexity=TaskComplexity.SIMPLE,
                required_capabilities=["testing_frameworks"],
                dependencies=["task_2"],
                assigned_agent=AgentType.CURSOR,
            ),
        ]

        protocol = await coordinator._setup_coordination_protocol(subtasks)

        assert isinstance(protocol, dict)
        assert "coordination_method" in protocol
        assert "dependency_graph" in protocol
        assert "parallel_groups" in protocol
        assert "handoff_protocol" in protocol
        assert "status_reporting" in protocol

        # Verify dependency graph
        dependency_graph = protocol["dependency_graph"]
        assert "task_1" in dependency_graph
        assert "task_2" in dependency_graph
        assert "task_3" in dependency_graph
        assert dependency_graph["task_2"]["dependencies"] == ["task_1"]
        assert dependency_graph["task_3"]["dependencies"] == ["task_2"]

    def test_identify_parallel_groups(self, coordinator):
        """Test identification of parallel execution groups"""
        # Create dependency graph with parallel opportunities
        dependency_graph = {
            "task_1": {
                "dependencies": [],
                "assigned_agent": AgentType.CODE,
                "estimated_duration": 30,
            },
            "task_2": {
                "dependencies": [],
                "assigned_agent": AgentType.CURSOR,
                "estimated_duration": 45,
            },
            "task_3": {
                "dependencies": ["task_1"],
                "assigned_agent": AgentType.CODE,
                "estimated_duration": 60,
            },
        }

        parallel_groups = coordinator._identify_parallel_groups(dependency_graph)

        # task_1 and task_2 can run in parallel
        assert len(parallel_groups) >= 1
        if len(parallel_groups) > 0:
            first_group = parallel_groups[0]
            assert "task_1" in first_group
            assert "task_2" in first_group

    @pytest.mark.asyncio
    async def test_get_coordination_status(self, coordinator, test_intent):
        """Test retrieval of coordination status"""
        # First, create a coordination
        result = await coordinator.coordinate_task(test_intent)
        coordination_id = result.coordination_id

        # Then retrieve status
        status = await coordinator.get_coordination_status(coordination_id)

        assert status is not None
        assert status.coordination_id == coordination_id
        assert isinstance(status, CoordinationResult)

    @pytest.mark.asyncio
    async def test_get_coordination_status_not_found(self, coordinator):
        """Test retrieval of non-existent coordination status"""
        status = await coordinator.get_coordination_status("non_existent_id")

        assert status is None

    @pytest.mark.asyncio
    async def test_get_performance_metrics_empty(self, coordinator):
        """Test performance metrics with no coordinations"""
        metrics = await coordinator.get_performance_metrics()

        assert metrics["total_coordinations"] == 0
        assert metrics["average_latency_ms"] == 0

    @pytest.mark.asyncio
    async def test_get_performance_metrics_with_data(self, coordinator, test_intent):
        """Test performance metrics with coordination data"""
        # Create multiple coordinations
        await coordinator.coordinate_task(test_intent)
        await coordinator.coordinate_task(test_intent)

        metrics = await coordinator.get_performance_metrics()

        assert metrics["total_coordinations"] == 2
        assert metrics["average_latency_ms"] > 0
        assert metrics["success_rate"] == 1.0  # All successful
        assert metrics["performance_target_met"] is True  # Should meet <1000ms target
        assert "agent_utilization" in metrics
        assert "code_agent_tasks" in metrics["agent_utilization"]
        assert "cursor_agent_tasks" in metrics["agent_utilization"]

    @pytest.mark.asyncio
    async def test_concurrent_coordination(self, coordinator):
        """Test concurrent coordination handling"""
        intents = []
        for i in range(5):
            intent = Intent(
                id=f"intent_{i}",
                category=IntentCategory.EXECUTION,
                action=f"test_action_{i}",
                original_message=f"Test coordination {i}",
                confidence=0.95,
            )
            intents.append(intent)

        # Execute coordinations concurrently
        tasks = [coordinator.coordinate_task(intent) for intent in intents]
        results = await asyncio.gather(*tasks)

        # All should succeed
        assert len(results) == 5
        for result in results:
            assert result.status == CoordinationStatus.ASSIGNED
            assert result.success_rate == 1.0

    @pytest.mark.asyncio
    async def test_edge_case_empty_intent_action(self, coordinator):
        """Test coordination with empty intent action"""
        empty_intent = Intent(
            id="test_empty",
            category=IntentCategory.QUERY,
            action="",
            original_message="Empty action test",
            confidence=0.5,
        )

        result = await coordinator.coordinate_task(empty_intent)

        # Should still work, possibly falling back to simple task
        assert isinstance(result, CoordinationResult)
        assert result.status in [CoordinationStatus.ASSIGNED, CoordinationStatus.FAILED]

    @pytest.mark.asyncio
    async def test_edge_case_very_low_confidence(self, coordinator):
        """Test coordination with very low confidence intent"""
        low_confidence_intent = Intent(
            id="test_low_confidence",
            category=IntentCategory.QUERY,
            action="test_action",
            original_message="Low confidence test",
            confidence=0.1,
        )

        result = await coordinator.coordinate_task(low_confidence_intent)

        # Should still work, but might be treated as simpler
        assert isinstance(result, CoordinationResult)
        assert result.coordination_id is not None

    @pytest.mark.asyncio
    async def test_performance_stress_test(self, coordinator):
        """Test coordination performance under stress"""
        # Create 20 rapid coordinations
        intents = []
        for i in range(20):
            intent = Intent(
                id=f"stress_intent_{i}",
                category=IntentCategory.EXECUTION,
                action=f"stress_test_{i}",
                original_message=f"Stress test coordination {i}",
                confidence=0.95,
            )
            intents.append(intent)

        start_time = time.time()

        # Execute all coordinations
        tasks = [coordinator.coordinate_task(intent) for intent in intents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        total_time_ms = (time.time() - start_time) * 1000

        # Verify results
        successful_results = [
            r
            for r in results
            if isinstance(r, CoordinationResult) and r.status == CoordinationStatus.ASSIGNED
        ]
        success_rate = len(successful_results) / len(intents)

        # Performance assertions
        assert success_rate >= 0.8  # At least 80% success under stress
        assert total_time_ms < 10000  # Complete within 10 seconds

        # Individual coordination performance
        if successful_results:
            avg_individual_latency = sum(r.total_duration_ms for r in successful_results) / len(
                successful_results
            )
            assert avg_individual_latency < 2000  # Allow higher latency under stress

    @pytest.mark.asyncio
    async def test_timeout_scenario(self, coordinator, test_intent):
        """Test coordination behavior with simulated timeout"""

        # Mock the decomposer to simulate slow operation
        async def slow_decompose_task(intent, context):
            await asyncio.sleep(0.1)  # Simulate slow operation
            return [
                SubTask(
                    id="timeout_task",
                    title="Timeout Test",
                    description="Test timeout handling",
                    estimated_duration_minutes=30,
                    complexity=TaskComplexity.SIMPLE,
                    required_capabilities=["general"],
                    dependencies=[],
                    assigned_agent=AgentType.CODE,
                )
            ]

        with patch.object(
            coordinator.task_decomposer, "decompose_task", side_effect=slow_decompose_task
        ):
            result = await coordinator.coordinate_task(test_intent)

        # Should still complete successfully
        assert result.status == CoordinationStatus.ASSIGNED
        assert len(result.subtasks) == 1

    async def test_agent_capabilities_initialization_coverage(self, coordinator):
        """Test that _initialize_agent_capabilities is properly tested"""
        decomposer = coordinator.task_decomposer
        capabilities = decomposer.agent_capabilities

        # Verify all agent types have capabilities
        assert AgentType.CODE in capabilities
        assert AgentType.CURSOR in capabilities

        # Verify CODE agent has expected strengths
        code_agent = capabilities[AgentType.CODE]
        assert "infrastructure" in code_agent.strengths
        assert "backend_services" in code_agent.strengths
        assert "orchestration" in code_agent.domains

        # Verify CURSOR agent has expected strengths
        cursor_agent = capabilities[AgentType.CURSOR]
        assert "testing" in cursor_agent.strengths
        assert "ui_development" in cursor_agent.strengths

    async def test_coordination_protocol_edge_cases(self, coordinator):
        """Test _setup_coordination_protocol with various dependency patterns"""
        # Test with circular dependency detection
        subtasks = [
            SubTask(
                id="task_a",
                description="Task A depends on B",
                task_type="implementation",
                estimated_duration=10,
                required_capabilities={"general"},
                dependencies=["task_b"],
                assigned_agent=AgentType.CODE,
            ),
            SubTask(
                id="task_b",
                description="Task B depends on A",
                task_type="implementation",
                estimated_duration=10,
                required_capabilities={"general"},
                dependencies=["task_a"],
                assigned_agent=AgentType.CURSOR,
            ),
        ]

        protocol = await coordinator._setup_coordination_protocol(subtasks)

        # Should handle circular dependencies gracefully
        assert "dependency_graph" in protocol
        assert "parallel_groups" in protocol
        assert protocol["execution_strategy"] in ["sequential", "parallel"]

    async def test_performance_metrics_accuracy(self, coordinator, test_intent):
        """Test get_performance_metrics returns accurate timing data"""
        # Coordinate a task to generate metrics
        start_time = time.time()
        result = await coordinator.coordinate_task(test_intent)
        end_time = time.time()

        # Get performance metrics
        metrics = await coordinator.get_performance_metrics()

        # Verify timing accuracy
        assert "average_coordination_time" in metrics
        assert "total_tasks_coordinated" in metrics
        assert metrics["total_tasks_coordinated"] >= 1

        # Performance assertion: coordination should be fast
        coordination_time = end_time - start_time
        assert coordination_time < 1.0, f"Coordination took {coordination_time}s, should be <1s"

    async def test_large_task_decomposition_performance(self, coordinator):
        """Test performance with large, complex tasks"""
        large_intent = Intent(
            id=f"large_intent_{uuid4().hex[:8]}",
            category=IntentCategory.IMPLEMENTATION,
            action="implement_large_system",
            original_message="""Implement a comprehensive user management system with:
            - User registration and authentication
            - Role-based access control
            - Profile management
            - Account settings
            - Password reset functionality
            - Email verification
            - OAuth integration
            - Audit logging
            - Performance monitoring
            - API documentation
            - Unit tests
            - Integration tests
            - E2E tests
            - Security hardening""",
            confidence=0.95,
        )

        start_time = time.time()
        result = await coordinator.coordinate_task(large_intent)
        end_time = time.time()

        # Performance assertion: even large tasks should coordinate quickly
        coordination_time = end_time - start_time
        assert (
            coordination_time < 5.0
        ), f"Large task coordination took {coordination_time}s, should be <5s"

        # Should decompose into multiple subtasks
        assert result.status == CoordinationStatus.ASSIGNED
        assert len(result.subtasks) >= 3, "Large task should decompose into multiple subtasks"
