"""
Issue #585: TDD tests for standup routing gap.

These tests document and prove that `/standup` currently routes to the wrong handler.

Epic #242 built StandupConversationHandler for interactive standups, but it was
never wired into intent routing. This test file:

1. FAILING TESTS (4): Prove the gap exists - routing goes to wrong handler
2. PASSING TESTS (4): Prove infrastructure exists - classes can be imported/instantiated

The failing tests use pytest.fail() with descriptive messages to document WHY they fail,
making it clear what needs to be fixed in Phase 2 (implementation).

Reference:
- Current behavior: /standup → IntentService._handle_standup_query() → StandupOrchestrationService (one-shot)
- Target behavior: /standup → StandupConversationHandler.start_conversation() → interactive flow

Issue #1053 (May 7, 2026): These tests intentionally verify the production
StandupConversationManager class via isinstance checks (TestStandupSingletonGap585)
and DI compatibility (test_handler_can_receive_manager_dependency). They do not
call manager methods that require a DB session, so they pass Postgres-down sanity
without needing the FakeStandupConversationManager.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ============================================================================
# PART 1: FAILING TESTS - Prove the routing gap exists
# ============================================================================


class TestStandupRoutingGap585:
    """
    Tests that MUST FAIL with current code.

    These tests prove Issue #585: /standup routes to STATUS handler
    (StandupOrchestrationService) instead of interactive standup flow
    (StandupConversationHandler).

    Each test uses pytest.fail() to document exactly what's missing.
    When Phase 2 implementation is complete, these will be replaced
    with actual assertions.
    """

    @pytest.mark.asyncio
    async def test_standup_command_should_start_interactive_flow(self):
        """
        FIXED (Issue #585): /standup invokes StandupConversationHandler.start_conversation().

        Implementation: _process_intent_internal() checks for "/standup" command
        BEFORE classification and routes to _start_standup_conversation() which
        uses StandupConversationHandler.

        This test verifies the fix is in place.
        """
        import inspect

        from services.intent.intent_service import IntentService

        # Verify IntentService has the _start_standup_conversation method
        service = IntentService()
        assert hasattr(
            service, "_start_standup_conversation"
        ), "IntentService should have _start_standup_conversation method"

        # Verify _process_intent_internal checks for /standup command
        source = inspect.getsource(IntentService._process_intent_internal)
        assert (
            '"/standup"' in source or "'/standup'" in source
        ), "_process_intent_internal should check for /standup command"
        assert (
            "_start_standup_conversation" in source
        ), "_process_intent_internal should call _start_standup_conversation"

    @pytest.mark.asyncio
    async def test_standup_handler_should_be_invoked_not_orchestration_service(self):
        """
        FIXED (Issue #585): StandupConversationHandler is now invoked via _start_standup_conversation.

        The /standup command now routes to _start_standup_conversation() which uses
        StandupConversationHandler. The old _handle_standup_query() is bypassed for
        explicit /standup commands.

        Note: _handle_standup_query() still exists for QUERY intents like "what's my standup"
        but /standup command goes through the new interactive path.
        """
        import inspect

        from services.intent.intent_service import IntentService

        # Verify _start_standup_conversation uses StandupConversationHandler
        source = inspect.getsource(IntentService._start_standup_conversation)

        # It should import from conversation_handler (via _get_standup_components)
        assert (
            "_get_standup_components" in source
        ), "_start_standup_conversation should use _get_standup_components"

        # It should call start_conversation
        assert (
            "start_conversation" in source
        ), "_start_standup_conversation should call handler.start_conversation"

    @pytest.mark.asyncio
    async def test_active_session_should_be_checked_before_classification(self):
        """
        FIXED (Issue #585): Active standup sessions are intercepted before classification.

        Implementation: _process_intent_internal() calls _check_active_guided_process()
        which uses the ProcessRegistry (ADR-049) to check all registered guided processes
        including standup. The StandupProcessAdapter wraps StandupConversationManager.

        Updated for ADR-049: Two-Tier Intent Architecture.
        """
        import inspect

        from services.intent.intent_service import IntentService

        # Get the source of _process_intent_internal
        internal_source = inspect.getsource(IntentService._process_intent_internal)

        # ADR-049: Now uses unified _check_active_guided_process which checks all
        # registered processes including standup via ProcessRegistry
        has_session_check = (
            "_check_active_guided_process" in internal_source
            or "_check_active_standup" in internal_source  # Legacy check still present
        )

        assert (
            has_session_check
        ), "_process_intent_internal should check for active guided processes (ADR-049)"

        # Verify unified check method exists (ADR-049 pattern)
        assert hasattr(
            IntentService, "_check_active_guided_process"
        ), "IntentService should have _check_active_guided_process method (ADR-049)"

        # Verify ProcessRegistry is used
        check_source = inspect.getsource(IntentService._check_active_guided_process)
        assert (
            "get_process_registry" in check_source or "ProcessRegistry" in check_source
        ), "_check_active_guided_process should use ProcessRegistry"

        # Legacy _check_active_standup still exists for backward compatibility
        assert hasattr(
            IntentService, "_check_active_standup"
        ), "IntentService should still have _check_active_standup method"

        legacy_source = inspect.getsource(IntentService._check_active_standup)
        assert (
            "get_conversation_by_session" in legacy_source
        ), "_check_active_standup should use get_conversation_by_session"
        assert "handle_turn" in legacy_source, "_check_active_standup should route to handle_turn"

    @pytest.mark.asyncio
    async def test_standup_session_should_continue_across_turns(self):
        """
        FIXED (Issue #585): Standup conversations continue across turns.

        Flow:
        1. User: "/standup" → _start_standup_conversation() → INITIATED state
        2. User: "I finished the auth work" → _check_active_standup() → handle_turn() → GATHERING state
        3. User: "Make it shorter" → _check_active_standup() → handle_turn() → REFINING state
        4. User: "Looks good" → _check_active_standup() → handle_turn() → COMPLETED state

        Session continuity is provided by:
        - Module-level singleton: _get_standup_components() returns same manager
        - Manager tracks sessions: get_conversation_by_session()
        - Active check in process flow: _check_active_standup() runs before classification
        """
        import inspect

        from services.conversation.conversation_handler import _get_standup_components
        from services.intent.intent_service import IntentService

        # Verify singleton pattern exists for state persistence
        manager1, handler1 = _get_standup_components()
        manager2, handler2 = _get_standup_components()

        assert manager1 is manager2, "Manager should be singleton - same instance across calls"
        assert handler1 is handler2, "Handler should be singleton - same instance across calls"

        # Verify IntentService has the session continuity mechanism
        class_source = inspect.getsource(IntentService)

        # Check for _check_active_standup which provides session continuity
        has_session_continuity = (
            "_check_active_standup" in class_source and "_get_standup_components" in class_source
        )

        assert has_session_continuity, (
            "IntentService should have _check_active_standup using _get_standup_components "
            "for session continuity across turns"
        )


# ============================================================================
# PART 2: PASSING TESTS - Prove the infrastructure exists
# ============================================================================


class TestStandupInfrastructureExists585:
    """
    Tests that MUST PASS with current code.

    These tests prove the infrastructure for Issue #585 EXISTS:
    - StandupConversationHandler can be imported
    - StandupConversationManager can be imported
    - Both can be instantiated
    - Key methods exist

    If these fail, the infrastructure from Epic #242 is broken and we have
    a bigger problem than routing.
    """

    def test_conversation_handler_can_be_imported(self):
        """
        PASSING: StandupConversationHandler exists and can be imported.

        This proves Epic #242 delivered the handler class.
        """
        from services.standup.conversation_handler import StandupConversationHandler

        assert StandupConversationHandler is not None
        assert callable(StandupConversationHandler)

    def test_conversation_manager_can_be_imported(self):
        """
        PASSING: StandupConversationManager exists and can be imported.

        This proves Epic #242 delivered the session management class.
        """
        from services.standup.conversation_manager import StandupConversationManager

        assert StandupConversationManager is not None
        assert callable(StandupConversationManager)

    def test_handler_can_be_instantiated(self):
        """
        PASSING: StandupConversationHandler can be instantiated.

        This proves the class has a working constructor.
        """
        from services.standup.conversation_handler import StandupConversationHandler

        handler = StandupConversationHandler()
        assert handler is not None

    def test_handler_has_required_methods(self):
        """
        PASSING: StandupConversationHandler has the methods needed for routing.

        Required methods:
        - start_conversation: Begin interactive flow (for /standup command)
        - handle_turn: Process subsequent messages (for session continuity)
        """
        from services.standup.conversation_handler import StandupConversationHandler

        handler = StandupConversationHandler()

        # Check required methods exist
        assert hasattr(handler, "start_conversation"), "Missing start_conversation method"
        assert hasattr(handler, "handle_turn"), "Missing handle_turn method"

        # Check they're callable
        assert callable(handler.start_conversation), "start_conversation not callable"
        assert callable(handler.handle_turn), "handle_turn not callable"


class TestStandupSingletonGap585:
    """
    Tests for singleton/service-level integration (FIXED - Issue #585).

    These tests verify IntentService has the necessary infrastructure
    to integrate with StandupConversationHandler via the singleton pattern.
    """

    def test_intent_service_uses_standup_components_singleton(self):
        """
        FIXED (Issue #585): IntentService uses _get_standup_components singleton.

        Implementation uses the same pattern as portfolio onboarding:
        - Singleton defined in conversation_handler.py
        - Imported via _get_standup_components function
        - Ensures state persistence across requests
        """
        import inspect

        from services.intent.intent_service import IntentService

        source = inspect.getsource(IntentService)

        # The fix: Uses _get_standup_components from conversation_handler
        has_components_import = "_get_standup_components" in source

        assert (
            has_components_import
        ), "IntentService should use _get_standup_components for standup handler access"

    def test_singleton_provides_manager_and_handler(self):
        """
        FIXED (Issue #585): Singleton provides both manager and handler.

        The _get_standup_components() function returns a tuple of
        (StandupConversationManager, StandupConversationHandler) that
        are used for session management and conversation handling.
        """
        from services.conversation.conversation_handler import _get_standup_components

        manager, handler = _get_standup_components()

        # Verify types
        from services.standup.conversation_handler import StandupConversationHandler
        from services.standup.conversation_manager import StandupConversationManager

        assert isinstance(
            manager, StandupConversationManager
        ), "First component should be StandupConversationManager"
        assert isinstance(
            handler, StandupConversationHandler
        ), "Second component should be StandupConversationHandler"

    def test_standup_orchestration_still_available_for_queries(self):
        """
        FIXED (Issue #585): _handle_standup_query still exists for QUERY intents.

        The /standup command uses interactive handler, but QUERY intents like
        "what's my standup status" can still use the orchestration service.
        Both paths are available.
        """
        import inspect

        from services.intent.intent_service import IntentService

        # _handle_standup_query still exists for QUERY intent fallback
        assert hasattr(
            IntentService, "_handle_standup_query"
        ), "_handle_standup_query should still exist for QUERY intents"

        # Verify the new methods also exist
        assert hasattr(
            IntentService, "_start_standup_conversation"
        ), "_start_standup_conversation should exist for /standup command"
        assert hasattr(
            IntentService, "_check_active_standup"
        ), "_check_active_standup should exist for session continuity"

    def test_handler_can_receive_manager_dependency(self):
        """
        PASSING: StandupConversationHandler can receive a manager via DI.

        This proves the handler supports dependency injection for the manager,
        which will be needed when wiring into IntentService.
        """
        from services.standup.conversation_handler import StandupConversationHandler
        from services.standup.conversation_manager import StandupConversationManager

        # Create manager
        manager = StandupConversationManager()

        # Handler accepts conversation_manager as constructor argument
        handler = StandupConversationHandler(conversation_manager=manager)

        # Verify manager is set
        assert handler.manager is manager
