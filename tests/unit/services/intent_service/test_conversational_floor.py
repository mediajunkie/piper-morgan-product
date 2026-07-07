"""
Tests for Conversational Floor (#907 MUX-LLM-FLOOR)

The conversational floor replaces dead-end deflections with contextual LLM
responses when no structured handler matches. Tests verify:

1. Floor produces conversational responses (not deflections)
2. Floor uses Piper's voice and personality
3. Floor incorporates available context
4. Floor does NOT take actions or call integrations
5. Floor routes through ethics pipeline (upstream, already cleared)
6. Structured handlers still take priority
7. Instrumentation logs floor hits

TDD: Tests written first, implementation follows.
"""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
    FloorContext,
    FloorResponse,
)

# ---- FloorContext Tests ----


class TestFloorContext:
    """FloorContext captures everything the floor needs to generate a response."""

    def test_floor_context_creation(self):
        ctx = FloorContext(
            user_message="Can you help me manage coding agents?",
            session_id="session-123",
        )
        assert ctx.user_message == "Can you help me manage coding agents?"
        assert ctx.session_id == "session-123"
        assert ctx.user_id is None
        assert ctx.conversation_history == []
        assert ctx.trust_stage is None
        assert ctx.formality_baseline is None

    def test_floor_context_with_full_context(self):
        ctx = FloorContext(
            user_message="What risks should I be aware of?",
            session_id="session-456",
            user_id="user-789",
            conversation_history=[
                {"role": "user", "content": "Tell me about the project"},
                {"role": "assistant", "content": "Your project has 3 active features..."},
            ],
            trust_stage="ESTABLISHED",
            formality_baseline=0.7,
            intent_category="UNKNOWN",
            intent_action="unknown",
            intent_confidence=0.3,
        )
        assert ctx.user_id == "user-789"
        assert len(ctx.conversation_history) == 2
        assert ctx.trust_stage == "ESTABLISHED"
        assert ctx.formality_baseline == 0.7
        assert ctx.intent_category == "UNKNOWN"

    def test_floor_context_builds_conversation_prompt(self):
        """Context should format conversation history for the LLM."""
        ctx = FloorContext(
            user_message="What about today?",
            session_id="s1",
            conversation_history=[
                {"role": "user", "content": "How's the project going?"},
                {"role": "assistant", "content": "Things are progressing well."},
            ],
        )
        prompt = ctx.format_conversation_history()
        assert "How's the project going?" in prompt
        assert "Things are progressing well." in prompt


# ---- FloorResponse Tests ----


class TestFloorResponse:
    """FloorResponse wraps the LLM output with metadata."""

    def test_floor_response_creation(self):
        resp = FloorResponse(
            message="Let me think about that with you...",
            floor_hit=True,
            original_category="UNKNOWN",
        )
        assert resp.message == "Let me think about that with you..."
        assert resp.floor_hit is True
        assert resp.original_category == "UNKNOWN"

    def test_floor_response_has_instrumentation_data(self):
        resp = FloorResponse(
            message="That's a great question about prioritization...",
            floor_hit=True,
            original_category="UNKNOWN",
            original_action="unknown",
            confidence=0.3,
        )
        log_data = resp.to_log_dict()
        assert log_data["floor_hit"] is True
        assert log_data["original_category"] == "UNKNOWN"
        assert log_data["confidence"] == 0.3
        assert "timestamp" in log_data


# ---- ConversationalFloor Tests ----


class TestConversationalFloor:
    """Core floor behavior: LLM call with context, not deflection."""

    @pytest.fixture
    def mock_llm(self):
        llm = AsyncMock()
        llm.complete = AsyncMock(
            return_value="That's a great question! Let me think through this with you. "
            "Managing coding agents involves coordination, task decomposition, "
            "and clear acceptance criteria. What kind of coding work are they doing?"
        )
        return llm

    @pytest.fixture
    def floor(self, mock_llm):
        return ConversationalFloor(llm_client=mock_llm)

    @pytest.mark.asyncio
    async def test_floor_returns_llm_response_not_deflection(self, floor):
        """The whole point: no more 'I don't have that capability yet'."""
        ctx = FloorContext(
            user_message="Can you help me manage the agents working on a coding assignment?",
            session_id="s1",
        )
        response = await floor.respond(ctx)

        assert response.floor_hit is True
        assert "I don't have that capability" not in response.message
        assert "I'm not sure what you're asking" not in response.message
        assert len(response.message) > 20  # Substantive response

    @pytest.mark.asyncio
    async def test_floor_calls_llm_with_system_prompt(self, floor, mock_llm):
        """Floor must use Piper's system prompt + floor addendum."""
        ctx = FloorContext(
            user_message="What's the best way to run a retrospective?",
            session_id="s1",
        )
        await floor.respond(ctx)

        # Verify LLM was called
        mock_llm.complete.assert_called_once()
        call_kwargs = mock_llm.complete.call_args
        # System prompt should include the floor addendum
        assert "system" in call_kwargs.kwargs or len(call_kwargs.args) > 3
        system_arg = call_kwargs.kwargs.get("system", "")
        assert "conversational" in system_arg.lower() or "colleague" in system_arg.lower()

    @pytest.mark.asyncio
    async def test_floor_includes_conversation_history(self, floor, mock_llm):
        """Floor should pass conversation history to the LLM for context."""
        ctx = FloorContext(
            user_message="What about the frontend?",
            session_id="s1",
            conversation_history=[
                {"role": "user", "content": "Tell me about the project architecture"},
                {"role": "assistant", "content": "The backend uses FastAPI with PostgreSQL..."},
            ],
        )
        await floor.respond(ctx)

        call_kwargs = mock_llm.complete.call_args
        prompt = call_kwargs.kwargs.get(
            "prompt", call_kwargs.args[1] if len(call_kwargs.args) > 1 else ""
        )
        assert "project architecture" in prompt or "FastAPI" in prompt

    @pytest.mark.asyncio
    async def test_floor_does_not_promise_actions(self, floor):
        """Floor system prompt must instruct LLM not to promise actions."""
        prompt_lower = FLOOR_SYSTEM_PROMPT_ADDENDUM.lower()
        # Verify the addendum contains constraints against self-introduction
        assert "do not" in prompt_lower or "don't" in prompt_lower
        # Prompt should prohibit capability listing or self-introduction
        assert "capabilities" in prompt_lower or "introduce" in prompt_lower

    @pytest.mark.asyncio
    async def test_floor_handles_llm_failure_gracefully(self, floor, mock_llm):
        """If LLM call fails, floor should return a graceful fallback."""
        mock_llm.complete.side_effect = Exception("API timeout")

        ctx = FloorContext(
            user_message="Help me think through prioritization",
            session_id="s1",
        )
        response = await floor.respond(ctx)

        # Should still return something useful, not crash
        assert response.message is not None
        assert len(response.message) > 0
        assert response.floor_hit is True
        # The fallback should be honest, not the old deflection
        assert "I don't have that capability" not in response.message

    @pytest.mark.asyncio
    async def test_floor_passes_task_type_conversation(self, floor, mock_llm):
        """Floor should use 'conversation' task type for appropriate model selection."""
        ctx = FloorContext(
            user_message="What's a good framework for stakeholder mapping?",
            session_id="s1",
        )
        await floor.respond(ctx)

        call_kwargs = mock_llm.complete.call_args
        assert call_kwargs.kwargs.get("task_type") == "conversation"

    @pytest.mark.asyncio
    async def test_floor_response_includes_instrumentation(self, floor):
        """Floor responses must include data for instrumentation."""
        ctx = FloorContext(
            user_message="How do I manage scope creep?",
            session_id="s1",
            intent_category="UNKNOWN",
            intent_action="unknown",
            intent_confidence=0.25,
        )
        response = await floor.respond(ctx)
        log_data = response.to_log_dict()

        assert log_data["floor_hit"] is True
        assert log_data["original_category"] == "UNKNOWN"
        assert "user_message" in log_data

    @pytest.mark.asyncio
    async def test_floor_with_formality_baseline(self, floor, mock_llm):
        """Floor should incorporate formality/warmth into the system prompt."""
        ctx = FloorContext(
            user_message="yo what's good with the sprint",
            session_id="s1",
            formality_baseline=0.9,  # Very warm/casual
        )
        await floor.respond(ctx)

        call_kwargs = mock_llm.complete.call_args
        system_arg = call_kwargs.kwargs.get("system", "")
        # System prompt should mention warmth or formality calibration
        assert (
            "warm" in system_arg.lower()
            or "casual" in system_arg.lower()
            or "formality" in system_arg.lower()
        )


class TestConversationalFloorSystemPrompt:
    """The floor system prompt is critical — it defines Piper's conversational identity."""

    def test_addendum_establishes_pm_colleague_identity(self):
        """Piper should present as a PM colleague, not a tool."""
        prompt = FLOOR_SYSTEM_PROMPT_ADDENDUM
        # Should mention PM or product management context
        assert any(term in prompt.lower() for term in ["product", "pm", "colleague"])

    def test_addendum_includes_no_actions_constraint(self):
        """Must explicitly state: reason conversationally, don't promise actions."""
        prompt = FLOOR_SYSTEM_PROMPT_ADDENDUM.lower()
        # Prompt should prohibit capability listing or self-introduction
        assert "do not" in prompt or "don't" in prompt
        assert "capabilities" in prompt or "introduce" in prompt

    def test_addendum_encourages_collaborative_thinking(self):
        """Should frame responses as thinking-with, not answering-at."""
        prompt = FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert any(
            term in prompt.lower()
            for term in ["think", "collaborate", "together", "explore", "work through"]
        )

    def test_addendum_is_honest_about_limitations(self):
        """Piper should be honest about what it can and can't do."""
        prompt = FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert any(
            term in prompt.lower()
            for term in ["honest", "transparent", "don't know", "not sure", "learn"]
        )

    def test_addendum_does_not_apologize(self):
        """Should NOT apologize or suggest 'What can you do?'"""
        prompt = FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "what can you do" not in prompt.lower()
        assert "sorry" not in prompt.lower()

    def test_addendum_answers_orientation_queries_1293(self):
        """#1293: the capabilities prohibition carries an 'unless asked' carve-out, so the
        floor answers orientation questions directly instead of deflecting. (Canonical Q4
        'How do I get help?' was a 6/9 marginal that deflected to 'what are you working
        on?'.) The behavioral test is the Tier-2 canonical judge (Q4-Identity); this cheap
        guard keeps the carve-out from silent revert in CI, where the Tier-2 judge does not run."""
        # normalize whitespace — the prompt's source line-wrapping is incidental (the LLM
        # collapses it; a phrase like "what are you working on" can wrap mid-source-line)
        prompt = " ".join(FLOOR_SYSTEM_PROMPT_ADDENDUM.lower().split())
        assert "orientation question" in prompt
        assert "how do i get help" in prompt
        # the prompt must name the deflection failure mode it has to avoid
        assert "what are you working on" in prompt


class TestConversationalFloorForUnhandledExecution:
    """Floor should also handle unhandled EXECUTION actions (Path B)."""

    @pytest.fixture
    def mock_llm(self):
        llm = AsyncMock()
        llm.complete = AsyncMock(
            return_value="I can't create calendar events directly yet, but let me help you "
            "think through the meeting. What's the purpose and who needs to be there?"
        )
        return llm

    @pytest.fixture
    def floor(self, mock_llm):
        return ConversationalFloor(llm_client=mock_llm)

    @pytest.mark.asyncio
    async def test_floor_handles_unimplemented_execution(self, floor):
        """For unhandled EXECUTION, floor should engage while being honest."""
        ctx = FloorContext(
            user_message="Schedule a meeting with the design team",
            session_id="s1",
            intent_category="EXECUTION",
            intent_action="schedule_meeting",
            intent_confidence=0.85,
        )
        response = await floor.respond(ctx)

        assert response.floor_hit is True
        assert response.original_category == "EXECUTION"
        assert len(response.message) > 20

    @pytest.mark.asyncio
    async def test_floor_preserves_known_capability_awareness(self, floor, mock_llm):
        """When the floor knows a capability is coming, it should say so honestly."""
        ctx = FloorContext(
            user_message="Set a reminder for tomorrow",
            session_id="s1",
            intent_category="EXECUTION",
            intent_action="set_reminder",
        )
        await floor.respond(ctx)

        # The prompt should include info about what Piper CAN do
        call_kwargs = mock_llm.complete.call_args
        prompt = call_kwargs.kwargs.get("prompt", "")
        # Should mention what Piper can currently help with
        assert "todo" in prompt.lower() or "capability" in prompt.lower() or len(prompt) > 50


class TestGenericCanonicalResponseDetection:
    """Issue #907/#908: Detect when canonical handlers return generic template responses."""

    def _make_service(self):
        """Create a minimal IntentService for detection method testing."""
        from services.intent.intent_service import IntentService

        service = IntentService.__new__(IntentService)
        # Provide a logger for the signature fallback logging
        import structlog

        service.logger = structlog.get_logger()
        return service

    # --- Issue #908: Structural flag detection ---

    def test_detects_generic_via_flag(self):
        """Handlers that set is_generic_response=True should be detected."""
        service = self._make_service()
        result = {
            "message": "Some response text",
            "is_generic_response": True,
        }
        assert service._is_generic_canonical_response(result, result["message"]) is True

    def test_flag_false_does_not_trigger(self):
        """Explicit is_generic_response=False should not trigger detection."""
        service = self._make_service()
        result = {
            "message": "Your project Piper Morgan has 3 open issues.",
            "is_generic_response": False,
        }
        assert service._is_generic_canonical_response(result, result["message"]) is False

    def test_missing_flag_does_not_trigger(self):
        """Results without the flag should not trigger flag detection."""
        service = self._make_service()
        result = {
            "message": "Your project Piper Morgan has 3 open issues.",
        }
        assert service._is_generic_canonical_response(result, result["message"]) is False

    def test_status_no_projects_flagged(self):
        """STATUS handler with no projects returns is_generic_response=True."""
        result = {
            "message": "You don't have any active projects configured yet. "
            "You can tell me about your projects anytime and I'll help you track them.",
            "is_generic_response": True,
        }
        service = self._make_service()
        assert service._is_generic_canonical_response(result, result["message"]) is True

    def test_priority_no_data_flagged(self):
        """PRIORITY handler with no priorities returns is_generic_response=True."""
        result = {
            "message": "You don't have any priorities configured in your PIPER.md yet. "
            "Would you like me to help you set up your priority list?",
            "is_generic_response": True,
        }
        service = self._make_service()
        assert service._is_generic_canonical_response(result, result["message"]) is True

    def test_config_error_flagged(self):
        """Config error responses should be detected as generic."""
        result = {
            "message": "I'm having trouble accessing your configuration right now. "
            "Your PIPER.md file may be missing or unreadable. "
            "Would you like help setting it up?",
            "is_generic_response": True,
            "error": "config_unavailable",
        }
        service = self._make_service()
        assert service._is_generic_canonical_response(result, result["message"]) is True

    def test_handler_fallback_flagged(self):
        """The handle() method's unknown-category fallback is generic."""
        result = {
            "message": "I'm here to help with your questions!",
            "is_generic_response": True,
        }
        service = self._make_service()
        assert service._is_generic_canonical_response(result, result["message"]) is True

    # --- Issue #907: Signature fallback detection (backward compat) ---

    def test_detects_generic_guidance_via_signature_fallback(self):
        """The GUIDANCE handler's generic priority template should be detected via signature."""
        service = self._make_service()
        generic_msg = (
            "Based on your current priorities and the time of day:\n"
            "**Right Now**: Flexible time - consider strategic planning.\n"
            "**Today's Key Focus**: your key priorities"
        )
        result = {"message": generic_msg}  # No flag — tests fallback path
        assert service._is_generic_canonical_response(result, generic_msg) is True

    def test_does_not_flag_specific_responses(self):
        """Specific, useful canonical responses should NOT be caught."""
        service = self._make_service()
        specific_msg = "I'm Piper Morgan, an AI product management assistant."
        result = {"message": specific_msg}
        assert service._is_generic_canonical_response(result, specific_msg) is False

    def test_does_not_flag_empty_or_none(self):
        """Empty/None responses should not crash."""
        service = self._make_service()
        assert service._is_generic_canonical_response({"message": ""}, "") is False
        assert service._is_generic_canonical_response({"message": None}, None) is False

    def test_flag_takes_priority_over_signature(self):
        """If flag is True, we don't even need to check signatures."""
        service = self._make_service()
        # Message doesn't match any signature, but flag is set
        result = {
            "message": "Some completely novel template text.",
            "is_generic_response": True,
        }
        assert service._is_generic_canonical_response(result, result["message"]) is True


# ---- #992 ETHICS-ACTIVATE Phase B Tests ----


class TestFloorContextDenialMode:
    """FloorContext accepts denial-mode fields from intent_service after
    BoundaryEnforcer flags a violation (#992 Phase B)."""

    def test_denial_fields_default_off(self):
        """Default construction → denial mode off, no category, no redirect."""
        ctx = FloorContext(user_message="hello", session_id="s1")
        assert ctx.denial_mode is False
        assert ctx.denial_category is None
        assert ctx.redirect_context is None

    def test_denial_fields_accept_values(self):
        """Denial fields can be set via constructor kwargs."""
        ctx = FloorContext(
            user_message="offending message",
            session_id="s1",
            denial_mode=True,
            denial_category="harassment",
            redirect_context="Steer toward constructive work.",
        )
        assert ctx.denial_mode is True
        assert ctx.denial_category == "harassment"
        assert ctx.redirect_context == "Steer toward constructive work."


class TestDenialModeSystemPrompt:
    """In denial mode, _get_system_prompt swaps the main addendum for the
    denial addendum so Piper composes the decline in voice."""

    def _make_floor(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        return ConversationalFloor(
            llm_client=AsyncMock(),
            system_prompt_base="You are Piper Morgan.",
        )

    @pytest.mark.asyncio
    async def test_non_denial_mode_uses_main_addendum(self):
        from services.intent_service.conversational_floor import (
            FLOOR_SYSTEM_PROMPT_ADDENDUM,
        )

        floor = self._make_floor()
        ctx = FloorContext(user_message="hi", session_id="s1")
        prompt = await floor._get_system_prompt(ctx)
        # Main addendum present
        assert "Think through the problem with them" in prompt
        assert FLOOR_SYSTEM_PROMPT_ADDENDUM[:60] in prompt

    @pytest.mark.asyncio
    async def test_denial_mode_swaps_in_denial_addendum(self):
        from services.intent_service.conversational_floor import (
            FLOOR_DENIAL_ADDENDUM,
            FLOOR_SYSTEM_PROMPT_ADDENDUM,
        )

        floor = self._make_floor()
        ctx = FloorContext(
            user_message="x",
            session_id="s1",
            denial_mode=True,
            denial_category="harassment",
            redirect_context="hint",
        )
        prompt = await floor._get_system_prompt(ctx)
        # Denial addendum present
        assert FLOOR_DENIAL_ADDENDUM[:60] in prompt
        # Main addendum NOT present (swap, not augment)
        assert "Think through the problem with them" not in prompt

    def test_denial_addendum_prohibits_system_speak(self):
        """The denial voice guide must explicitly prohibit system-error language."""
        from services.intent_service.conversational_floor import FLOOR_DENIAL_ADDENDUM

        lower = FLOOR_DENIAL_ADDENDUM.lower()
        # Voice: first-person colleague, not system emitter
        assert "first person" in lower
        # Explicit prohibitions against system-speak
        assert "blocked" in lower
        assert "violation" in lower
        assert "policy" in lower

    def test_denial_addendum_warns_against_quoting_hint_back(self):
        """The LLM must use the redirect hint, not parrot it at the user."""
        from services.intent_service.conversational_floor import FLOOR_DENIAL_ADDENDUM

        # Explicit instruction not to quote the redirect context back
        assert "do not quote it back" in FLOOR_DENIAL_ADDENDUM.lower()


class TestDenialModePromptComposition:
    """In denial mode, _build_prompt injects the [Redirect context] block
    and suppresses the generic intent_category context note."""

    def _make_floor(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        return ConversationalFloor(
            llm_client=AsyncMock(),
            system_prompt_base="You are Piper Morgan.",
        )

    def test_denial_mode_injects_redirect_context_block(self):
        floor = self._make_floor()
        ctx = FloorContext(
            user_message="offensive thing",
            session_id="s1",
            denial_mode=True,
            denial_category="harassment",
            redirect_context="Steer toward constructive work.",
        )
        prompt = floor._build_prompt(ctx)
        assert "[Redirect context:" in prompt
        assert "Steer toward constructive work." in prompt

    def test_denial_mode_suppresses_intent_category_block(self):
        """In denial mode, the generic 'relates to X' context note is suppressed
        — the redirect block replaces it."""
        floor = self._make_floor()
        ctx = FloorContext(
            user_message="offensive thing",
            session_id="s1",
            denial_mode=True,
            denial_category="harassment",
            redirect_context="Steer toward constructive work.",
            intent_category="ACTION",  # not in _FLOOR_NATIVE_CATEGORIES
        )
        prompt = floor._build_prompt(ctx)
        assert "[Redirect context:" in prompt
        assert "relates to 'ACTION'" not in prompt

    def test_denial_mode_without_redirect_context_omits_block(self):
        """If enforcer returned no redirect_context (unknown category), don't
        inject an empty block — let the LLM rely on the addendum alone."""
        floor = self._make_floor()
        ctx = FloorContext(
            user_message="x",
            session_id="s1",
            denial_mode=True,
            denial_category="unknown",
            redirect_context=None,
        )
        prompt = floor._build_prompt(ctx)
        assert "[Redirect context:" not in prompt

    def test_non_denial_mode_preserves_intent_category_block(self):
        """Regression guard: non-denial flow still shows intent context note
        for non-floor-native categories."""
        floor = self._make_floor()
        ctx = FloorContext(
            user_message="create an issue",
            session_id="s1",
            intent_category="ACTION",
        )
        prompt = floor._build_prompt(ctx)
        assert "relates to 'ACTION'" in prompt
        assert "[Redirect context:" not in prompt
