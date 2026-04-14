"""
Tests for Issue #911 Phase 2: Action Gate and Context Assembler.

Tests that the Action Gate correctly routes intents to either the canonical
handler (for operations the LLM cannot perform) or the conversational floor
(for everything else, with assembled context).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.shared_types import IntentCategory as IC

# ---- Helpers ----


def _make_intent(category: IC, action: str = "default", message: str = "") -> Intent:
    """Create a minimal Intent for testing."""
    return Intent(
        category=category,
        action=action,
        confidence=0.9,
        original_message=message,
        context={"original_message": message},
    )


def _get_intent_service():
    """Create an IntentService instance with mocked dependencies."""
    from services.intent.intent_service import IntentService

    with patch("services.intent.intent_service.OrchestrationEngine"):
        svc = IntentService.__new__(IntentService)
        svc.logger = MagicMock()
        svc.canonical_handlers = MagicMock()
        # #963: Wire up only the detection methods still used by the action gate.
        # _detect_health_check_request, _detect_differentiation_request, and
        # _detect_help_request were deleted (dead code — _is_adjacent_identity removed).
        from services.intent_service.canonical_handlers import CanonicalHandlers

        real_handlers = CanonicalHandlers()
        svc.canonical_handlers._detect_setup_request = real_handlers._detect_setup_request
        return svc


# ---- TestActionGate ----


class TestActionGate:
    """Test _requires_canonical_handler() and _should_route_to_floor() routing decisions."""

    def setup_method(self):
        self.svc = _get_intent_service()

    # -- Categories that ALWAYS require canonical handler --

    def test_portfolio_requires_canonical(self):
        intent = _make_intent(IC.PORTFOLIO, "add_project", "add project X")
        assert self.svc._requires_canonical_handler(intent) is True

    def test_execution_requires_canonical(self):
        intent = _make_intent(IC.EXECUTION, "create_issue", "create an issue")
        assert self.svc._requires_canonical_handler(intent) is True

    # -- TEMPORAL: date/time is canonical, conversational queries go to floor (#965) --

    def test_temporal_date_requires_canonical(self):
        """Q6: 'What day is it?' stays canonical (deterministic fast-path)."""
        for action in ("get_current_time", "provide_date", "get_date"):
            intent = _make_intent(IC.TEMPORAL, action, "what day is it")
            assert self.svc._requires_canonical_handler(intent) is True, f"action={action} should be canonical"

    def test_temporal_agenda_does_not_require_canonical(self):
        """Q8: 'What's on the agenda for today?' should route to floor."""
        intent = _make_intent(IC.TEMPORAL, "provide_agenda", "What's on the agenda for today?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_temporal_retrospective_does_not_require_canonical(self):
        """Q7: 'What did we accomplish yesterday?' should route to floor."""
        intent = _make_intent(IC.TEMPORAL, "provide_retrospective", "What did we accomplish yesterday?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_temporal_last_activity_does_not_require_canonical(self):
        """Q9: 'When was the last time we worked on this?' should route to floor."""
        intent = _make_intent(IC.TEMPORAL, "provide_last_activity", "When was the last time we worked on this?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_temporal_duration_does_not_require_canonical(self):
        """Q10: 'How long have we been working on this project?' should route to floor."""
        intent = _make_intent(IC.TEMPORAL, "provide_project_duration", "How long have we been working on this project?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_temporal_conversational_without_known_action_goes_to_floor(self):
        """Temporal queries with conversational keywords route to floor regardless of action."""
        intent = _make_intent(IC.TEMPORAL, "something_else", "what did we accomplish yesterday")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- STATUS: migrated to floor (#925 Phase 3) --

    def test_status_does_not_require_canonical(self):
        """#925: STATUS queries route to floor with project context."""
        intent = _make_intent(IC.STATUS, "get_project_status", "what am I working on")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- PRIORITY: migrated to floor (#925 Phase 3) --

    def test_priority_does_not_require_canonical(self):
        """#925: PRIORITY queries route to floor with priority context."""
        intent = _make_intent(IC.PRIORITY, "get_top_priority", "what should I focus on")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- CONVERSATION: greeting is canonical, others are floor --

    def test_conversation_greeting_requires_canonical(self):
        intent = _make_intent(IC.CONVERSATION, "greeting", "hello")
        assert self.svc._requires_canonical_handler(intent) is True

    def test_conversation_chitchat_does_not_require_canonical(self):
        intent = _make_intent(IC.CONVERSATION, "chitchat", "nice weather today")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_conversation_farewell_does_not_require_canonical(self):
        intent = _make_intent(IC.CONVERSATION, "farewell", "goodbye")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_conversation_thanks_does_not_require_canonical(self):
        intent = _make_intent(IC.CONVERSATION, "thanks", "thank you")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- IDENTITY: all identity goes to floor (Apr 8 decision) --
    # UAT showed canned templates scoring 1/3; floor scores 7+.

    def test_identity_core_does_not_require_canonical(self):
        """Apr 8: All identity queries now route to floor, not canonical templates."""
        intent = _make_intent(IC.IDENTITY, "provide_identity", "Who are you?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_identity_health_check_does_not_require_canonical(self):
        intent = _make_intent(IC.IDENTITY, "provide_identity", "Are you working properly?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_identity_differentiation_does_not_require_canonical(self):
        intent = _make_intent(
            IC.IDENTITY, "provide_identity", "What makes you different from ChatGPT?"
        )
        assert self.svc._requires_canonical_handler(intent) is False

    def test_identity_help_does_not_require_canonical(self):
        intent = _make_intent(IC.IDENTITY, "provide_identity", "How do I get started?")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- GUIDANCE: setup is canonical, everything else is floor --

    def test_guidance_general_does_not_require_canonical(self):
        intent = _make_intent(IC.GUIDANCE, "focus_guidance", "What should I work on?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_guidance_setup_requires_canonical(self):
        intent = _make_intent(IC.GUIDANCE, "setup_guidance", "Help me set up my projects")
        assert self.svc._requires_canonical_handler(intent) is True

    # -- Categories that ALWAYS go to floor --

    def test_discovery_does_not_require_canonical(self):
        intent = _make_intent(IC.DISCOVERY, "provide_capabilities", "What can you do?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_trust_does_not_require_canonical(self):
        intent = _make_intent(IC.TRUST, "trust_explanation", "How well do you know me?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_memory_does_not_require_canonical(self):
        intent = _make_intent(IC.MEMORY, "history_query", "What do you remember?")
        assert self.svc._requires_canonical_handler(intent) is False

    def test_unknown_does_not_require_canonical(self):
        intent = _make_intent(IC.UNKNOWN, "unknown", "purple monkey dishwasher")
        assert self.svc._requires_canonical_handler(intent) is False

    # -- _should_route_to_floor integration tests --

    def test_should_route_guidance_to_floor(self):
        intent = _make_intent(IC.GUIDANCE, "focus_guidance", "What should I work on?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_not_route_guidance_setup_to_floor(self):
        intent = _make_intent(IC.GUIDANCE, "setup_guidance", "Help me set up my projects")
        assert self.svc._should_route_to_floor(intent) is False

    def test_should_route_discovery_to_floor(self):
        intent = _make_intent(IC.DISCOVERY, "provide_capabilities", "What can you do?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_trust_to_floor(self):
        intent = _make_intent(IC.TRUST, "trust_explanation", "How well do you know me?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_memory_to_floor(self):
        intent = _make_intent(IC.MEMORY, "history_query", "What do you remember?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_conversation_chitchat_to_floor(self):
        intent = _make_intent(IC.CONVERSATION, "chitchat", "Nice weather")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_not_route_conversation_greeting_to_floor(self):
        intent = _make_intent(IC.CONVERSATION, "greeting", "hello")
        assert self.svc._should_route_to_floor(intent) is False

    def test_should_route_unknown_to_floor(self):
        intent = _make_intent(IC.UNKNOWN, "unknown", "purple monkey dishwasher")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_identity_health_check_to_floor(self):
        intent = _make_intent(IC.IDENTITY, "provide_identity", "Are you working properly?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_identity_core_to_floor(self):
        """Apr 8: All identity queries now route to floor."""
        intent = _make_intent(IC.IDENTITY, "provide_identity", "Who are you?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_temporal_non_date_to_floor(self):
        """#965: Conversational temporal queries (agenda, retrospective, etc.) route to floor."""
        intent = _make_intent(IC.TEMPORAL, "provide_agenda", "What's on the agenda?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_not_route_temporal_date_to_floor(self):
        """#965: Pure date/time stays canonical, not floor."""
        intent = _make_intent(IC.TEMPORAL, "get_current_time", "What day is it?")
        assert self.svc._should_route_to_floor(intent) is False

    def test_should_route_status_to_floor(self):
        """#925: STATUS queries route to floor with project context."""
        intent = _make_intent(IC.STATUS, "get_project_status", "What am I working on?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_route_priority_to_floor(self):
        """#925: PRIORITY queries route to floor with priority context."""
        intent = _make_intent(IC.PRIORITY, "get_top_priority", "What should I focus on?")
        assert self.svc._should_route_to_floor(intent) is True

    def test_should_not_route_portfolio_to_floor(self):
        """PORTFOLIO is not in floor-routed categories, should not route to floor."""
        intent = _make_intent(IC.PORTFOLIO, "add_project", "add project")
        assert self.svc._should_route_to_floor(intent) is False

    def test_should_not_route_execution_to_floor(self):
        """EXECUTION is not in floor-routed categories."""
        intent = _make_intent(IC.EXECUTION, "create_issue", "create issue")
        assert self.svc._should_route_to_floor(intent) is False


# ---- TestContextAssembler ----


class TestContextAssembler:
    """Test ContextAssembler gathers correct data for each category."""

    @pytest.mark.asyncio
    async def test_gather_always_returns_current_time(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler.gather_context("CONVERSATION")
        assert "current_time" in result

    @pytest.mark.asyncio
    async def test_gather_identity_returns_capabilities(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        with patch("services.plugins.get_plugin_registry") as mock_reg:
            mock_reg.return_value.get_status_all.return_value = {
                "github": {"configured": True, "active": True},
            }
            result = await assembler.gather_context("IDENTITY")

        assert "capabilities" in result
        assert isinstance(result["capabilities"], list)
        # #923: Capabilities are now registry-derived, not hardcoded
        assert "conversational PM guidance" in result["capabilities"]

    @pytest.mark.asyncio
    async def test_gather_identity_returns_integrations(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        with patch("services.plugins.get_plugin_registry") as mock_reg:
            mock_reg.return_value.get_status_all.return_value = {
                "github": {"configured": True, "active": True},
                "slack": {"configured": False, "active": False},
            }
            result = await assembler.gather_context("DISCOVERY")

        assert "integrations" in result
        assert isinstance(result["integrations"], list)
        assert len(result["integrations"]) == 2

    @pytest.mark.asyncio
    async def test_gather_trust_without_user_id(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler.gather_context("TRUST", user_id=None)

        assert "trust_profile" in result
        assert result["trust_profile"]["stage"] == "unknown"

    @pytest.mark.asyncio
    async def test_gather_trust_with_user_id_db_error(self):
        """Trust gathering should be graceful on database errors."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_sf:
            mock_sf.session_scope.side_effect = Exception("DB connection failed")
            result = await assembler.gather_context(
                "TRUST", user_id="550e8400-e29b-41d4-a716-446655440000"
            )

        assert "trust_profile" in result
        assert result["trust_profile"]["stage"] == "unknown"

    @pytest.mark.asyncio
    async def test_gather_memory_returns_history_summary(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        mock_turn = MagicMock()
        mock_turn.message = "What should I focus on today?"
        mock_turn.response = "Let me check your priorities."
        mock_ctx = MagicMock()
        mock_ctx.turns = [mock_turn]

        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=mock_ctx,
        ):
            result = await assembler.gather_context("MEMORY", session_id="test-session")

        assert "conversation_history_summary" in result
        summary = result["conversation_history_summary"]
        assert summary["turn_count"] == 1
        assert len(summary["recent_topics"]) == 1

    @pytest.mark.asyncio
    async def test_gather_graceful_on_total_failure(self):
        """Even if everything fails, gather_context returns a dict with current_time."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        # Patch the category-specific gatherer to raise
        with patch.object(assembler, "_gather_identity_context", side_effect=Exception("boom")):
            result = await assembler.gather_context("IDENTITY")

        assert isinstance(result, dict)
        assert "current_time" in result

    @pytest.mark.asyncio
    async def test_gather_conversation_minimal_context(self):
        """CONVERSATION chitchat should return minimal context (just current_time)."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        result = await assembler.gather_context("CONVERSATION")

        assert "current_time" in result
        # Should not have extra keys beyond current_time
        assert "capabilities" not in result
        assert "trust_profile" not in result


# ---- TestFormatDomainContext ----


class TestFormatDomainContext:
    """Test that _format_domain_context handles new context keys from ContextAssembler."""

    def _get_floor(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        return ConversationalFloor(llm_client=MagicMock())

    def test_format_capabilities(self):
        floor = self._get_floor()
        ctx = {"capabilities": ["issue tracking", "strategic planning"]}
        result = floor._format_domain_context(ctx)
        assert "issue tracking" in result
        assert "strategic planning" in result

    def test_format_integrations(self):
        floor = self._get_floor()
        ctx = {
            "integrations": [
                {"name": "github", "status": "active"},
                {"name": "slack", "status": "inactive"},
            ]
        }
        result = floor._format_domain_context(ctx)
        assert "github" in result
        assert "slack" not in result  # Only active integrations shown

    def test_format_trust_profile(self):
        floor = self._get_floor()
        ctx = {
            "trust_profile": {
                "stage": "established",
                "interaction_count": 42,
            }
        }
        result = floor._format_domain_context(ctx)
        assert "established" in result
        assert "42" in result

    def test_format_conversation_history_summary(self):
        floor = self._get_floor()
        ctx = {
            "conversation_history_summary": {
                "turn_count": 5,
                "recent_topics": ["sprint planning", "bug triage"],
            }
        }
        result = floor._format_domain_context(ctx)
        assert "5" in result
        assert "sprint planning" in result

    def test_format_empty_context_returns_empty_string(self):
        floor = self._get_floor()
        result = floor._format_domain_context({})
        assert result == ""


# ---- TestFloorNativeCategories ----


class TestFloorNativeCategories:
    """Test that _FLOOR_NATIVE_CATEGORIES is correctly expanded."""

    def test_floor_native_categories_includes_phase2(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        cats = ConversationalFloor._FLOOR_NATIVE_CATEGORIES
        assert "UNKNOWN" in cats
        assert "GUIDANCE" in cats
        assert "IDENTITY" in cats
        assert "DISCOVERY" in cats
        assert "TRUST" in cats
        assert "MEMORY" in cats
        assert "CONVERSATION" in cats


# ---- TestContinuationRate ----


class TestContinuationRate:
    """Test continuation rate instrumentation (#913)."""

    def test_conversation_context_has_floor_tracking_fields(self):
        """ConversationContext should have fields for floor tracking."""
        from services.intent_service.conversation_context import ConversationContext

        ctx = ConversationContext()
        assert ctx.last_response_was_floor is False
        assert ctx.last_floor_category is None

    def test_floor_tracking_fields_are_settable(self):
        """Floor tracking fields should be settable."""
        from services.intent_service.conversation_context import ConversationContext

        ctx = ConversationContext()
        ctx.last_response_was_floor = True
        ctx.last_floor_category = "IDENTITY"
        assert ctx.last_response_was_floor is True
        assert ctx.last_floor_category == "IDENTITY"

    def test_floor_tracking_resets(self):
        """Floor tracking should be resettable for after logging."""
        from services.intent_service.conversation_context import ConversationContext

        ctx = ConversationContext()
        ctx.last_response_was_floor = True
        ctx.last_floor_category = "DISCOVERY"

        # Simulate what process_intent does after logging continuation
        ctx.last_response_was_floor = False
        ctx.last_floor_category = None
        assert ctx.last_response_was_floor is False
        assert ctx.last_floor_category is None
