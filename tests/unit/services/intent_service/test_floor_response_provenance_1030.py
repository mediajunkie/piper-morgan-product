"""
Tests for Issue #1030 R4 Step 4: FloorContext + FloorResponse provenance.

Covers:
- FloorContext.domain_context_provenance default None
- FloorResponse.provenance default empty dict
- _build_response_provenance: copies keys present in BOTH domain_context AND
  domain_context_provenance; honest empty-state when either is missing
- to_log_dict includes provenance_keys + provenance_size
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
    FloorResponse,
)


def _floor():
    f = ConversationalFloor(llm_client=MagicMock())
    f._push_session_state = {}
    return f


class TestFloorContextProvenanceField:
    def test_default_provenance_is_none(self):
        ctx = FloorContext(user_message="hi", session_id="s")
        assert ctx.domain_context_provenance is None

    def test_can_set_provenance(self):
        prov = {"calendar": {"source": "GoogleCalendar"}}
        ctx = FloorContext(user_message="hi", session_id="s", domain_context_provenance=prov)
        assert ctx.domain_context_provenance == prov


class TestFloorResponseProvenanceField:
    def test_default_provenance_is_empty_dict(self):
        r = FloorResponse(message="ok")
        assert r.provenance == {}

    def test_to_log_dict_includes_provenance_metadata(self):
        r = FloorResponse(
            message="ok",
            provenance={"calendar": {"source": "GoogleCalendar"}, "todos": {"source": "TodoMgr"}},
        )
        log = r.to_log_dict()
        assert "provenance_keys" in log
        assert set(log["provenance_keys"]) == {"calendar", "todos"}
        assert log["provenance_size"] == 2

    def test_to_log_dict_with_empty_provenance(self):
        r = FloorResponse(message="ok")
        log = r.to_log_dict()
        assert log["provenance_keys"] == []
        assert log["provenance_size"] == 0


class TestBuildResponseProvenance:
    """_build_response_provenance copies the intersection of domain_context
    keys and domain_context_provenance keys — honest 'what was available AND
    sourced' subset."""

    def test_intersection_of_keys_captured(self):
        floor = _floor()
        ctx = FloorContext(
            user_message="hi",
            session_id="s",
            domain_context={"calendar": {}, "todos": [], "current_time": "10:00 AM"},
            domain_context_provenance={
                "calendar": {"source": "GoogleCalendar"},
                "todos": {"source": "TodoMgr"},
                # current_time has no provenance entry (intentional — always-available)
                "blocked_items": {"source": "GitHub"},  # in provenance but not in context
            },
        )
        prov = floor._build_response_provenance(ctx)
        assert "calendar" in prov
        assert "todos" in prov
        assert "current_time" not in prov  # no provenance available
        assert "blocked_items" not in prov  # was not in domain_context

    def test_empty_when_no_domain_context(self):
        floor = _floor()
        ctx = FloorContext(user_message="hi", session_id="s")
        assert floor._build_response_provenance(ctx) == {}

    def test_empty_when_no_provenance_passed(self):
        floor = _floor()
        ctx = FloorContext(user_message="hi", session_id="s", domain_context={"calendar": {}})
        assert floor._build_response_provenance(ctx) == {}

    def test_empty_when_no_overlap(self):
        floor = _floor()
        ctx = FloorContext(
            user_message="hi",
            session_id="s",
            domain_context={"current_time": "10:00 AM"},
            domain_context_provenance={"calendar": {"source": "GoogleCalendar"}},
        )
        assert floor._build_response_provenance(ctx) == {}


class TestRespondPopulatesFloorResponseProvenance:
    """respond() must wire the helper into both success and exception paths."""

    @pytest.mark.asyncio
    async def test_success_path_populates_provenance(self):
        floor = _floor()
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(return_value="LLM response")
        ctx = FloorContext(
            user_message="What about my todos?",
            session_id="s-test",
            user_id="u-test",
            intent_category="STATUS",
            intent_action="get_project_status",
            domain_context={"pending_todos": [{"text": "T1"}]},
            domain_context_provenance={
                "pending_todos": {"source": "TodoMgr", "fetch_timestamp": "now"}
            },
        )
        result = await floor.respond(ctx)
        assert "pending_todos" in result.provenance
        assert result.provenance["pending_todos"]["source"] == "TodoMgr"

    @pytest.mark.asyncio
    async def test_exception_path_still_populates_provenance(self):
        """Even on LLM error, provenance survives for downstream tracking."""
        floor = _floor()
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(side_effect=RuntimeError("simulated"))
        ctx = FloorContext(
            user_message="hello",
            session_id="s-test",
            user_id="u-test",
            domain_context={"current_time": "10:00 AM", "calendar": {}},
            domain_context_provenance={"calendar": {"source": "GoogleCalendar"}},
        )
        result = await floor.respond(ctx)
        # Provenance still has calendar (it was in both dicts)
        assert "calendar" in result.provenance
