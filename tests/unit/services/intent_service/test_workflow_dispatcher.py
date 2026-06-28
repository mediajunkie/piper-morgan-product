"""
Tests for the workflow dispatcher (ADR-059).

Verifies:
- Registry-based dispatch replaces switch statements
- Unknown workflow types return None (caller routes to floor)
- Registered workflows dispatch correctly
- Validation catches bad entries
- Meeting workflow entry point works
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.workflow_dispatcher import (
    WORKFLOW_REGISTRY,
    WorkflowEntry,
    dispatch_workflow,
    register_workflow,
    validate_registry,
)


@pytest.fixture(autouse=True)
def clean_registry():
    """Reset the workflow registry before each test."""
    saved = dict(WORKFLOW_REGISTRY)
    WORKFLOW_REGISTRY.clear()
    yield
    WORKFLOW_REGISTRY.clear()
    WORKFLOW_REGISTRY.update(saved)


class TestWorkflowRegistry:
    """Tests for workflow registration."""

    def test_register_workflow(self):
        """Can register a workflow entry."""
        entry = WorkflowEntry(
            entry_point=AsyncMock(),
            description="Test workflow",
        )
        register_workflow("test_type", entry)
        assert "test_type" in WORKFLOW_REGISTRY
        assert WORKFLOW_REGISTRY["test_type"].description == "Test workflow"

    def test_duplicate_registration_raises(self):
        """Cannot register the same workflow type twice."""
        entry = WorkflowEntry(entry_point=AsyncMock(), description="First")
        register_workflow("dupe", entry)

        with pytest.raises(ValueError, match="already registered"):
            register_workflow("dupe", WorkflowEntry(entry_point=AsyncMock(), description="Second"))

    def test_get_registered_workflows(self):
        """get_registered_workflows returns a copy."""
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        register_workflow("test", WorkflowEntry(entry_point=AsyncMock(), description="Test"))
        result = get_registered_workflows()
        assert "test" in result
        # Mutating the copy doesn't affect the real registry
        result.pop("test")
        assert "test" in WORKFLOW_REGISTRY


class TestDispatchWorkflow:
    """Tests for the dispatch_workflow function."""

    @pytest.mark.asyncio
    async def test_unknown_type_returns_none(self):
        """Unknown workflow types return None for floor routing."""
        result = await dispatch_workflow(
            workflow_type="nonexistent",
            session_id="sess-1",
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_dispatch_calls_entry_point(self):
        """Dispatches to the registered entry point."""
        mock_handler = AsyncMock(return_value={"message": "Started!"})
        register_workflow(
            "test_workflow",
            WorkflowEntry(entry_point=mock_handler, description="Test"),
        )

        result = await dispatch_workflow(
            workflow_type="test_workflow",
            session_id="sess-1",
            user_id="user-1",
            context={"key": "value"},
        )

        assert result == {"message": "Started!"}
        mock_handler.assert_called_once_with(
            session_id="sess-1",
            user_id="user-1",
            context={"key": "value"},
        )

    @pytest.mark.asyncio
    async def test_dispatch_with_resume_point(self):
        """Resume uses resume_point when available."""
        mock_start = AsyncMock(return_value={"message": "Fresh start"})
        mock_resume = AsyncMock(return_value={"message": "Resumed!"})
        register_workflow(
            "resumable",
            WorkflowEntry(
                entry_point=mock_start,
                resume_point=mock_resume,
                description="Resumable",
            ),
        )

        result = await dispatch_workflow(
            workflow_type="resumable",
            session_id="sess-1",
            resume=True,
        )

        assert result == {"message": "Resumed!"}
        mock_resume.assert_called_once()
        mock_start.assert_not_called()

    @pytest.mark.asyncio
    async def test_dispatch_resume_fallback_to_entry(self):
        """Resume falls back to entry_point when no resume_point."""
        mock_start = AsyncMock(return_value={"message": "Fresh start"})
        register_workflow(
            "no_resume",
            WorkflowEntry(entry_point=mock_start, description="No resume"),
        )

        result = await dispatch_workflow(
            workflow_type="no_resume",
            session_id="sess-1",
            resume=True,
        )

        assert result == {"message": "Fresh start"}
        mock_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_dispatch_error_returns_none(self):
        """Entry point errors are caught and return None."""
        mock_handler = AsyncMock(side_effect=RuntimeError("boom"))
        register_workflow(
            "broken",
            WorkflowEntry(entry_point=mock_handler, description="Broken"),
        )

        result = await dispatch_workflow(
            workflow_type="broken",
            session_id="sess-1",
        )

        assert result is None


class TestValidateRegistry:
    """Tests for registry validation."""

    def test_valid_registry(self):
        """Valid registry produces no errors."""
        register_workflow(
            "valid",
            WorkflowEntry(entry_point=AsyncMock(), description="Valid"),
        )
        errors = validate_registry()
        assert errors == []

    def test_non_callable_entry_point(self):
        """Non-callable entry_point is caught."""
        WORKFLOW_REGISTRY["bad"] = WorkflowEntry(
            entry_point="not_a_function",  # type: ignore
            description="Bad entry",
        )
        errors = validate_registry()
        assert len(errors) == 1
        assert "not callable" in errors[0]

    def test_non_callable_resume_point(self):
        """Non-callable resume_point is caught."""
        WORKFLOW_REGISTRY["bad_resume"] = WorkflowEntry(
            entry_point=AsyncMock(),
            resume_point=42,  # type: ignore
            description="Bad resume",
        )
        errors = validate_registry()
        assert len(errors) == 1
        assert "resume_point" in errors[0]


class TestMeetingWorkflowEntry:
    """Tests for the meeting workflow entry point."""

    @pytest.mark.asyncio
    async def test_meeting_workflow_starts_slot_filling(self):
        """Meeting workflow starts slot filling via the adapter."""
        import sys

        mock_slot_response = MagicMock()
        mock_slot_response.message = "When would you like to meet?"
        mock_slot_response.filled_slots = {}
        mock_slot_response.template_name = "meeting"

        mock_manager = MagicMock()
        mock_manager.start_filling = AsyncMock(return_value=mock_slot_response)

        mock_adapter_instance = MagicMock()
        mock_adapter_instance.manager = mock_manager

        mock_wos_instance = MagicMock()
        mock_wos_instance.format_acceptance.return_value = "Great, let's set that up!"

        # Patch WorkflowOfferService which is lazily imported
        with patch(
            "services.intent_service.soft_invocation.WorkflowOfferService",
            return_value=mock_wos_instance,
        ):
            from services.intent_service.workflow_entries import start_meeting_workflow

            result = await start_meeting_workflow(
                session_id="sess-1",
                user_id="user-1",
                context={
                    "trigger_message": "get the team together",
                    "active_lens": "people",
                    "formality_baseline": 0.6,
                    "slot_filling_adapter": mock_adapter_instance,
                },
            )

        assert "Great, let's set that up!" in result["message"]
        assert "When would you like to meet?" in result["message"]
        assert result["intent_data"]["action"] == "meeting"
        assert result["intent_data"]["context"]["slot_filling_active"] is True


class TestDefaultWorkflowRegistration:
    """Tests for register_default_workflows."""

    def test_registers_meeting_workflow(self):
        """register_default_workflows registers the meeting workflow."""
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        assert "meeting" in WORKFLOW_REGISTRY
        assert WORKFLOW_REGISTRY["meeting"].description == "Meeting scheduling via slot-filling"

    def test_double_registration_is_idempotent(self):
        """#1124: register_default_workflows is safe to call twice — the
        container's process-registry init can run more than once per process, so
        the second call is a no-op rather than a ValueError. (register_workflow
        itself stays strict — see TestWorkflowRegistry.test_duplicate_registration_raises.)
        """
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        before = dict(WORKFLOW_REGISTRY)

        register_default_workflows()  # must not raise
        assert dict(WORKFLOW_REGISTRY) == before

    def test_registers_document_update_aliases_action_triggered(self):
        """#1124: all three update_document aliases register as action-triggered;
        the offer-only meeting workflow stays non-action-triggered."""
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        for alias in ("update_document", "edit_document", "update_document_query"):
            assert alias in WORKFLOW_REGISTRY, f"{alias} not registered"
            assert WORKFLOW_REGISTRY[alias].action_triggered is True

        # #1124 migration #3: changes_query family also action-triggered
        for alias in ("changes_query", "what_changed", "show_changes", "changes_since"):
            assert alias in WORKFLOW_REGISTRY, f"{alias} not registered"
            assert WORKFLOW_REGISTRY[alias].action_triggered is True

        # meeting is offer-triggered only — must NOT be action-dispatchable
        assert WORKFLOW_REGISTRY["meeting"].action_triggered is False


class TestActionWorkflows:
    """#1124: the action-dispatch rail's registry filter."""

    def test_workflow_entry_defaults_to_not_action_triggered(self):
        """Backward-compatible default: existing entries are offer-only."""
        entry = WorkflowEntry(entry_point=AsyncMock(), description="x")
        assert entry.action_triggered is False

    def test_get_action_workflows_filters_to_action_triggered_only(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows

        register_workflow(
            "offer_only",
            WorkflowEntry(entry_point=AsyncMock(), description="offer"),
        )
        register_workflow(
            "by_action",
            WorkflowEntry(entry_point=AsyncMock(), description="action", action_triggered=True),
        )

        action_workflows = get_action_workflows()
        assert "by_action" in action_workflows
        assert "offer_only" not in action_workflows


class TestUpdateDocumentWorkflowEntry:
    """#1124: the document-update action-dispatch entry point."""

    @pytest.mark.asyncio
    async def test_invokes_handler_with_intent_and_returns_result(self):
        """Reuses the existing instance handler unchanged, passing the classified
        intent / workflow_id / session_id through context."""
        from services.intent_service.workflow_entries import run_update_document_workflow

        sentinel_result = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_update_document_notion = AsyncMock(return_value=sentinel_result)
        mock_intent = MagicMock(action="update_document")

        result = await run_update_document_workflow(
            session_id="sess-9",
            user_id="user-9",
            context={
                "intent": mock_intent,
                "workflow_id": None,
                "intent_service": mock_service,
            },
        )

        assert result is sentinel_result
        mock_service._handle_update_document_notion.assert_awaited_once_with(
            mock_intent, None, "sess-9"
        )

    @pytest.mark.asyncio
    async def test_missing_context_returns_none_for_floor_fallback(self):
        """Wiring error (no intent / no service) returns None so the dispatcher
        routes to the conversational floor rather than crashing."""
        from services.intent_service.workflow_entries import run_update_document_workflow

        assert await run_update_document_workflow(session_id="s", context={}) is None
        assert (
            await run_update_document_workflow(session_id="s", context={"intent": MagicMock()})
            is None
        )


class TestChangesQueryWorkflowEntry:
    """#1124 cohort-1 migration #3: the changes-query action-dispatch entry point
    (dispatch migration — reuses _handle_changes_query unchanged)."""

    @pytest.mark.asyncio
    async def test_invokes_handler_with_session_id_and_returns_result(self):
        from services.intent_service.workflow_entries import run_changes_query_workflow

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_changes_query = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="changes_query")

        result = await run_changes_query_workflow(
            session_id="sess-7",
            user_id="user-7",
            context={"intent": mock_intent, "workflow_id": None, "intent_service": mock_service},
        )

        assert result is sentinel
        mock_service._handle_changes_query.assert_awaited_once_with(mock_intent, None, "sess-7")

    @pytest.mark.asyncio
    async def test_missing_context_returns_none(self):
        from services.intent_service.workflow_entries import run_changes_query_workflow

        assert await run_changes_query_workflow(session_id="s", context={}) is None


class TestIssueMutationWorkflowEntries1124:
    """#1124 Phase 4 step 3: the CLOSE/REOPEN/COMMENT issue-mutation cohort
    action-dispatch entry points (dispatch migration — handlers reused unchanged,
    called as (intent, workflow_id), no session_id)."""

    @pytest.mark.asyncio
    async def test_close_invokes_handler_and_returns_result(self):
        from services.intent_service.workflow_entries import run_close_issue_workflow

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_close_issue_query = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="close_issue_query")

        result = await run_close_issue_workflow(
            session_id="sess-c",
            user_id="user-c",
            context={"intent": mock_intent, "workflow_id": "wf-c", "intent_service": mock_service},
        )

        assert result is sentinel
        mock_service._handle_close_issue_query.assert_awaited_once_with(mock_intent, "wf-c")

    @pytest.mark.asyncio
    async def test_reopen_invokes_handler_and_returns_result(self):
        from services.intent_service.workflow_entries import run_reopen_issue_workflow

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_reopen_issue_query = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="reopen_issue_query")

        result = await run_reopen_issue_workflow(
            session_id="sess-r",
            context={"intent": mock_intent, "workflow_id": None, "intent_service": mock_service},
        )

        assert result is sentinel
        mock_service._handle_reopen_issue_query.assert_awaited_once_with(mock_intent, None)

    @pytest.mark.asyncio
    async def test_comment_invokes_handler_and_returns_result(self):
        from services.intent_service.workflow_entries import run_comment_issue_workflow

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_comment_issue_query = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="comment_issue_query")

        result = await run_comment_issue_workflow(
            session_id="sess-m",
            context={"intent": mock_intent, "workflow_id": None, "intent_service": mock_service},
        )

        assert result is sentinel
        # #1122: the entry point threads session_id for antecedent history
        mock_service._handle_comment_issue_query.assert_awaited_once_with(
            mock_intent, None, session_id="sess-m"
        )

    @pytest.mark.asyncio
    async def test_missing_context_returns_none_for_floor_fallback(self):
        from services.intent_service.workflow_entries import (
            run_close_issue_workflow,
            run_comment_issue_workflow,
            run_reopen_issue_workflow,
        )

        assert await run_close_issue_workflow(session_id="s", context={}) is None
        assert await run_reopen_issue_workflow(session_id="s", context={}) is None
        assert await run_comment_issue_workflow(session_id="s", context={}) is None

    def test_cohort_registered_as_action_triggered(self):
        """register_default_workflows wires all cohort aliases into the
        action-dispatch rail (action_triggered=True)."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        action_workflows = get_action_workflows()
        for alias in (
            "close_issue",
            "close_issue_query",
            "reopen_issue",
            "reopen_issue_query",
            "comment_issue",
            "add_comment",
            "comment_issue_query",
        ):
            assert alias in action_workflows, f"{alias} not registered as action-triggered"


class TestReadQueryCohortWorkflowEntries1124:
    """#1124 Phase 4 step 3 cohort 2: the GitHub read-query cohort migrated via the
    parameterized entry-point factory (all handlers share (intent, workflow_id))."""

    @pytest.mark.asyncio
    async def test_factory_entry_dispatches_to_named_handler(self):
        from services.intent_service.workflow_entries import (
            _make_query_dispatch_entry_point,
        )

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_shipped_this_week = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="shipped_query")

        entry = _make_query_dispatch_entry_point("_handle_shipped_this_week")
        result = await entry(
            session_id="sess-s",
            context={"intent": mock_intent, "workflow_id": "wf-s", "intent_service": mock_service},
        )

        assert result is sentinel
        mock_service._handle_shipped_this_week.assert_awaited_once_with(mock_intent, "wf-s")

    @pytest.mark.asyncio
    async def test_factory_entry_missing_context_returns_none(self):
        from services.intent_service.workflow_entries import (
            _make_query_dispatch_entry_point,
        )

        entry = _make_query_dispatch_entry_point("_handle_stale_prs")
        assert await entry(session_id="s", context={}) is None

    def test_all_cohort_handlers_exist_on_intent_service(self):
        """Closes the getattr blind spot: every registered handler_attr must be a
        real IntentService method (a MagicMock-based test would silently pass a typo)."""
        from services.intent.intent_service import IntentService
        from services.intent_service.workflow_entries import _READ_QUERY_COHORT

        missing = [h for h in _READ_QUERY_COHORT if not hasattr(IntentService, h)]
        assert not missing, f"handler_attr(s) not on IntentService: {missing}"

    def test_cohort_aliases_registered_as_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import (
            _READ_QUERY_COHORT,
            register_default_workflows,
        )

        register_default_workflows()
        action_workflows = get_action_workflows()
        for aliases in _READ_QUERY_COHORT.values():
            for alias in aliases:
                assert alias in action_workflows, f"{alias} not registered as action-triggered"


class TestCalendarQueryCohortWorkflowEntries1124:
    """#1124 calendar cohort: meeting_time / recurring_meetings / week_calendar
    migrated via the user-scoped factory (all share (intent, workflow_id, user_id))."""

    @pytest.mark.asyncio
    async def test_user_scoped_factory_threads_user_id_to_handler(self):
        from services.intent_service.workflow_entries import (
            _make_user_scoped_query_dispatch_entry_point,
        )

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_meeting_time_query = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="meeting_time")

        entry = _make_user_scoped_query_dispatch_entry_point("_handle_meeting_time_query")
        result = await entry(
            session_id="sess-s",
            user_id="user-42",
            context={"intent": mock_intent, "workflow_id": "wf-s", "intent_service": mock_service},
        )

        assert result is sentinel
        # user_id is threaded through as the 3rd positional arg (the #586 requirement).
        mock_service._handle_meeting_time_query.assert_awaited_once_with(
            mock_intent, "wf-s", "user-42"
        )

    @pytest.mark.asyncio
    async def test_user_scoped_factory_missing_context_returns_none(self):
        from services.intent_service.workflow_entries import (
            _make_user_scoped_query_dispatch_entry_point,
        )

        entry = _make_user_scoped_query_dispatch_entry_point("_handle_week_calendar_query")
        assert await entry(session_id="s", user_id="u", context={}) is None

    def test_all_calendar_handlers_exist_on_intent_service(self):
        """getattr blind-spot guard for the calendar cohort handler names."""
        from services.intent.intent_service import IntentService
        from services.intent_service.workflow_entries import _CALENDAR_QUERY_COHORT

        missing = [h for h in _CALENDAR_QUERY_COHORT if not hasattr(IntentService, h)]
        assert not missing, f"handler_attr(s) not on IntentService: {missing}"

    def test_calendar_aliases_registered_as_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import (
            _CALENDAR_QUERY_COHORT,
            register_default_workflows,
        )

        register_default_workflows()
        action_workflows = get_action_workflows()
        for aliases in _CALENDAR_QUERY_COHORT.values():
            for alias in aliases:
                assert alias in action_workflows, f"{alias} not registered as action-triggered"


class TestPrioritizationWorkflowEntry1124:
    """#1124 cohort 1: prioritization migrated onto the rail (2-arg factory)."""

    def test_prioritize_aliases_registered_as_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        action_workflows = get_action_workflows()
        for alias in ("prioritize", "set_priorities"):
            assert alias in action_workflows, f"{alias} not registered as action-triggered"

    def test_prioritization_handler_exists_on_intent_service(self):
        from services.intent.intent_service import IntentService

        assert hasattr(IntentService, "_handle_prioritization")


class TestAnalysisQueryCohortWorkflowEntries1124:
    """#1124 analysis cohort: analyze_commits / generate_report / analyze_data
    migrated via the standard 2-arg factory (analyze_document, the if-head, stays —
    it is 3-arg session_id + Notion-coupled)."""

    @pytest.mark.asyncio
    async def test_factory_entry_dispatches_to_named_handler(self):
        from services.intent_service.workflow_entries import (
            _make_query_dispatch_entry_point,
        )

        sentinel = MagicMock(name="IntentProcessingResult")
        mock_service = MagicMock()
        mock_service._handle_analyze_commits = AsyncMock(return_value=sentinel)
        mock_intent = MagicMock(action="analyze_commits")

        entry = _make_query_dispatch_entry_point("_handle_analyze_commits")
        result = await entry(
            session_id="sess-s",
            context={"intent": mock_intent, "workflow_id": "wf-s", "intent_service": mock_service},
        )

        assert result is sentinel
        mock_service._handle_analyze_commits.assert_awaited_once_with(mock_intent, "wf-s")

    def test_all_analysis_handlers_exist_on_intent_service(self):
        """getattr blind-spot guard for the analysis cohort handler names."""
        from services.intent.intent_service import IntentService
        from services.intent_service.workflow_entries import _ANALYSIS_QUERY_COHORT

        missing = [h for h in _ANALYSIS_QUERY_COHORT if not hasattr(IntentService, h)]
        assert not missing, f"handler_attr(s) not on IntentService: {missing}"

    def test_analysis_aliases_registered_as_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import (
            _ANALYSIS_QUERY_COHORT,
            register_default_workflows,
        )

        register_default_workflows()
        action_workflows = get_action_workflows()
        for aliases in _ANALYSIS_QUERY_COHORT.values():
            for alias in aliases:
                assert alias in action_workflows, f"{alias} not registered as action-triggered"


class TestGenerateContentWorkflowEntry1124:
    """#1124 synthesis migration: generate_content/create_content onto the rail
    (the dead summarize elif was deleted per #1158 — summaries floor)."""

    def test_generate_content_aliases_registered_as_action_triggered(self):
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        action_workflows = get_action_workflows()
        for alias in ("generate_content", "create_content"):
            assert alias in action_workflows, f"{alias} not registered as action-triggered"

    def test_generate_content_handler_exists_on_intent_service(self):
        from services.intent.intent_service import IntentService

        assert hasattr(IntentService, "_handle_generate_content")
