"""
Tests for Issue #911 Phase 1: GUIDANCE floor routing with context assembly.

Verifies that GUIDANCE intents route through the conversational floor with
assembled domain context instead of through canonical template handlers.
"""

from dataclasses import asdict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.conversational_floor import ConversationalFloor, FloorContext


class TestFloorContextDomainContext:
    """Verify FloorContext accepts and stores domain_context."""

    def test_domain_context_defaults_to_none(self):
        ctx = FloorContext(user_message="test", session_id="s1")
        assert ctx.domain_context is None

    def test_domain_context_accepts_dict(self):
        domain = {"current_time": "3:00 PM", "projects": {"Klatch": {"open_issues_count": 5}}}
        ctx = FloorContext(
            user_message="test",
            session_id="s1",
            domain_context=domain,
        )
        assert ctx.domain_context == domain
        assert ctx.domain_context["current_time"] == "3:00 PM"


class TestFormatDomainContext:
    """Verify _format_domain_context renders structured data as facts."""

    def setup_method(self):
        self.floor = ConversationalFloor(llm_client=MagicMock())

    def test_empty_context_returns_empty_string(self):
        result = self.floor._format_domain_context({})
        assert result == ""

    def test_current_time_rendered(self):
        result = self.floor._format_domain_context({"current_time": "3:00 PM"})
        assert "Current time: 3:00 PM" in result

    def test_calendar_next_meeting(self):
        result = self.floor._format_domain_context(
            {
                "calendar": {
                    "next_meeting": {"title": "Sprint Review", "start": "4:00 PM"},
                }
            }
        )
        assert 'Next meeting: "Sprint Review" at 4:00 PM' in result

    def test_calendar_free_block(self):
        result = self.floor._format_domain_context(
            {
                "calendar": {
                    "next_free_block": {"start": "2:00 PM", "duration_minutes": 60},
                }
            }
        )
        assert "Next free block: 2:00 PM" in result
        assert "60 minutes" in result

    def test_projects_with_issues(self):
        result = self.floor._format_domain_context(
            {
                "projects": {
                    "Klatch": {"open_issues_count": 12, "has_github": True},
                    "Piper": {"open_issues_count": 5, "has_github": True},
                }
            }
        )
        assert '"Klatch": 12 open issues' in result
        assert '"Piper": 5 open issues' in result

    def test_projects_as_list(self):
        """When projects are just names without metadata."""
        result = self.floor._format_domain_context({"projects": ["Klatch", "Piper"]})
        assert '"Klatch": tracked' in result
        assert '"Piper": tracked' in result

    def test_priorities_rendered(self):
        result = self.floor._format_domain_context(
            {
                "priorities": {
                    "user_priorities": ["Ship v2", "Onboard beta users"],
                    "urgent_items": 3,
                }
            }
        )
        assert "Ship v2" in result
        assert "Onboard beta users" in result
        # #2458 (CXO's words): the count line says what it counts.
        assert "Open issues marked high priority: 3" in result

    def test_full_context_all_sections(self):
        result = self.floor._format_domain_context(
            {
                "current_time": "3:00 PM",
                "calendar": {"next_meeting": {"title": "Standup", "start": "3:30 PM"}},
                "projects": {"MyApp": {"open_issues_count": 7}},
                "priorities": {"user_priorities": ["Launch"], "urgent_items": 1},
            }
        )
        assert "Current time: 3:00 PM" in result
        assert "Standup" in result
        assert '"MyApp": 7 open issues' in result
        assert "Launch" in result

    def test_context_wrapped_in_brackets(self):
        result = self.floor._format_domain_context({"current_time": "3:00 PM"})
        assert result.startswith("[Available context")
        assert result.endswith("]")


class TestBuildPromptDomainContext:
    """Verify _build_prompt includes domain context and adjusts routing notes."""

    def setup_method(self):
        self.floor = ConversationalFloor(llm_client=MagicMock())

    def test_domain_context_included_in_prompt(self):
        ctx = FloorContext(
            user_message="What should I focus on?",
            session_id="s1",
            intent_category="GUIDANCE",
            domain_context={"current_time": "3:00 PM"},
        )
        prompt = self.floor._build_prompt(ctx)
        assert "Current time: 3:00 PM" in prompt
        assert "What should I focus on?" in prompt

    def test_guidance_no_handler_unavailable_note(self):
        """GUIDANCE is a floor-native category — no 'handler unavailable' note."""
        ctx = FloorContext(
            user_message="What should I focus on?",
            session_id="s1",
            intent_category="GUIDANCE",
            intent_action="focus_recommendation",
        )
        prompt = self.floor._build_prompt(ctx)
        assert "no specialized handler" not in prompt

    def test_unknown_no_handler_unavailable_note(self):
        """UNKNOWN is also floor-native."""
        ctx = FloorContext(
            user_message="Tell me about agile",
            session_id="s1",
            intent_category="UNKNOWN",
        )
        prompt = self.floor._build_prompt(ctx)
        assert "no specialized handler" not in prompt

    def test_other_category_gets_handler_note(self):
        """Non-floor-native categories still get the routing context note."""
        ctx = FloorContext(
            user_message="something",
            session_id="s1",
            intent_category="STRATEGY",
            intent_action="discuss",
        )
        prompt = self.floor._build_prompt(ctx)
        # Context note mentions the category and encourages engagement
        assert "STRATEGY" in prompt
        assert "Engage" in prompt

    def test_domain_context_before_user_message(self):
        """Domain context should appear before the user's message."""
        ctx = FloorContext(
            user_message="What should I focus on?",
            session_id="s1",
            domain_context={"current_time": "3:00 PM"},
        )
        prompt = self.floor._build_prompt(ctx)
        time_pos = prompt.index("3:00 PM")
        msg_pos = prompt.index("What should I focus on?")
        assert time_pos < msg_pos


class TestGuidanceFloorRoutingDispatch:
    """Verify GUIDANCE intents route to floor, not canonical handler."""

    def test_guidance_setup_request_detected(self):
        """Setup requests should still use canonical handler."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)
        intent = MagicMock()
        intent.original_message = "Help me set up my projects"
        result = handlers._detect_setup_request(intent)
        assert result == "projects"

    def test_non_setup_guidance_not_detected_as_setup(self):
        """Regular guidance should NOT be detected as setup."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)
        intent = MagicMock()
        intent.original_message = "What should I focus on today?"
        result = handlers._detect_setup_request(intent)
        assert result is None

    def test_agent_coordination_not_detected_as_setup(self):
        """Conversational queries should NOT be detected as setup."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers.__new__(CanonicalHandlers)
        intent = MagicMock()
        intent.original_message = "Can you help me coordinate AI agents on a project?"
        result = handlers._detect_setup_request(intent)
        assert result is None
