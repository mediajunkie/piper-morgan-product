"""Tests for #1092 OrchestrationEngine dispatcher cleanup.

Verifies:
- ANALYZE_REQUEST still routes through _analyze_request_task
- Unhandled task types raise ValueError with the #1092-shaped error message
  (not a vague \"Unknown task type\" string)
- The deleted handlers (_extract_requirements_task, _identify_dependencies_task,
  _generate_documentation_task, _execute_github_action_task) no longer exist
- The previously-broken TaskType references (GENERATE_DOCUMENTATION,
  EXECUTE_GITHUB_ACTION) are no longer in the dispatcher
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent, IntentCategory, Task, Workflow
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import (
    TaskStatus,
    TaskType,
    WorkflowStatus,
    WorkflowType,
)


def _make_engine() -> OrchestrationEngine:
    """Build engine with a mock LLMClient so we don't need the ServiceContainer."""
    mock_llm = MagicMock()
    engine = OrchestrationEngine(llm_client=mock_llm)
    engine.intent_enricher = MagicMock()
    return engine


def _make_workflow(task_type: TaskType) -> Workflow:
    """Construct a one-task workflow with the given task type."""
    task = Task(
        id="task-1",
        type=task_type,
        status=TaskStatus.PENDING,
        input_data={},
        output_data={},
    )
    workflow = Workflow(
        id="wf-1",
        type=WorkflowType.CREATE_TICKET,
        status=WorkflowStatus.PENDING,
        tasks=[task],
        context={
            "intent": {
                "category": IntentCategory.EXECUTION,
                "action": "create_issue",
                "original_message": "create an issue",
            },
            "session_id": "test-session",
        },
    )
    return workflow


class TestAnalyzeRequestStillWorks:
    """The one remaining dispatcher branch must continue to route correctly."""

    @pytest.mark.asyncio
    async def test_analyze_request_routes_through_handler(self):
        engine = _make_engine()
        workflow = _make_workflow(TaskType.ANALYZE_REQUEST)
        task = workflow.tasks[0]

        # Mock the intent enricher to return a sane enriched intent.
        enriched = MagicMock()
        enriched.context = {
            "requirements": ["req1"],
            "complexity": "low",
            "estimated_effort": "1h",
        }
        engine.intent_enricher.enrich = AsyncMock(return_value=enriched)

        result = await engine._execute_task(task, workflow)

        assert result.status == TaskStatus.COMPLETED
        assert result.output_data["complexity"] == "low"
        assert result.output_data["estimated_effort"] == "1h"
        engine.intent_enricher.enrich.assert_awaited_once()


class TestUnhandledTaskTypesRaiseExplicit:
    """The 8 workflow_factory-created task types that this dispatcher doesn't
    handle must fail through to the new #1092-shaped ValueError, not the prior
    AttributeError on a non-existent enum attribute."""

    @pytest.mark.parametrize(
        "task_type",
        [
            TaskType.EXTRACT_WORK_ITEM,
            TaskType.GENERATE_GITHUB_ISSUE_CONTENT,
            TaskType.GITHUB_CREATE_ISSUE,
            TaskType.ANALYZE_GITHUB_ISSUE,
            TaskType.ANALYZE_FILE,
            TaskType.SUMMARIZE,
            TaskType.LIST_PROJECTS,
            TaskType.CREATE_WORK_ITEM,
        ],
    )
    @pytest.mark.asyncio
    async def test_unhandled_task_type_marks_task_failed_with_clear_error(
        self, task_type
    ):
        """All 8 unhandled-but-factory-created task types fall through to the
        explicit error branch. Task status = FAILED; error message names the
        dispatcher gap so operators can see the architectural reality."""
        engine = _make_engine()
        workflow = _make_workflow(task_type)
        task = workflow.tasks[0]

        result = await engine._execute_task(task, workflow)

        assert result.status == TaskStatus.FAILED
        assert "OrchestrationEngine dispatcher has no handler" in result.error_message
        assert "#1092" in result.error_message  # operator-discoverable reference


class TestDeletedHandlersGone:
    """The four dead handler methods removed by #1092 must not be reintroduced."""

    def test_extract_requirements_handler_removed(self):
        engine = _make_engine()
        assert not hasattr(engine, "_extract_requirements_task")

    def test_identify_dependencies_handler_removed(self):
        engine = _make_engine()
        assert not hasattr(engine, "_identify_dependencies_task")

    def test_generate_documentation_handler_removed(self):
        engine = _make_engine()
        assert not hasattr(engine, "_generate_documentation_task")

    def test_execute_github_action_handler_removed(self):
        engine = _make_engine()
        assert not hasattr(engine, "_execute_github_action_task")


class TestBrokenTaskTypeReferencesGone:
    """The two broken `TaskType.X` references (Bug 1, Bug 2) must remain absent."""

    def test_generate_documentation_enum_still_missing(self):
        """Verify TaskType enum doesn't have GENERATE_DOCUMENTATION (the
        non-existent attribute that caused Bug 1). If a future change adds
        it, this test will pass — but at that point the dispatcher should
        also gain a handler for it."""
        assert not hasattr(TaskType, "GENERATE_DOCUMENTATION")

    def test_execute_github_action_enum_still_missing(self):
        """Similar to above for Bug 2 — TaskType.EXECUTE_GITHUB_ACTION."""
        assert not hasattr(TaskType, "EXECUTE_GITHUB_ACTION")
