"""#1570 (b) — context assembly must be floor-ENTRY-independent, not just
category-independent (#1566 one level up).

PM live 2026-08-10: "what todos are pending?" (multiple pending rows in the
store) floored with ZERO user data. Mechanism, verified by direct execution:
the pre-classifier does not claim the phrasing (pre_classify → None), the
LLM's paraphrase emission misses the rail's todo-read keys (mode 4), and
category routing lands in `_handle_generic_query` → `_handle_unknown_intent`
— the one floor entry that NEVER called ContextAssembler. Its
`domain_context` parameter defaulted to None and nothing gathered, so the
floor honestly reported seeing no todos while the store had rows. The
bound-offer projects turn converges on the same entry (pending-offer
dispatch returning None → `_handle_unknown_intent`).

Principal threading is NOT the hole here: #1394's recovery already threads
user_id on this path (asserted below) — the missing gather is.

Layer honesty (m-43): these tests drive `_handle_unknown_intent` /
`_handle_generic_query` directly with the assembler's gather mocked,
asserting on the FloorContext actually handed to ConversationalFloor. The
gather internals (which keys each category yields) are #1566's tests; the
seam here is "does this floor entry gather at all, and does what it gathers
reach the floor".
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import conversational_floor as cf
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversation_context import clear_context
from services.shared_types import IntentCategory

PENDING_TODOS = [
    {"text": "follow up with the beta testers", "deadline_proximity": "due_today"},
    {"text": "draft the sprint review", "deadline_proximity": "none"},
]


def _svc():
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    return svc


def _intent(category, action, message, user_id=None):
    intent = Intent(
        category=category,
        action=action,
        confidence=0.8,
        original_message=message,
    )
    intent.context = {"user_id": user_id} if user_id else {}
    return intent


@pytest.fixture
def captured_floor(monkeypatch):
    captured = []

    async def fake_respond(self, ctx):
        captured.append(ctx)
        return cf.FloorResponse(message="(stubbed floor answer)")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", fake_respond)
    return captured


@pytest.fixture
def gather_spy(monkeypatch):
    """Stub ContextAssembler.gather_context (the real one reaches DB/GitHub)
    and record every call's (category, user_id)."""
    calls = []

    async def fake_gather(
        self, intent_category, user_id=None, session_id=None, intent_action=None
    ):
        calls.append({"category": intent_category, "user_id": user_id})
        return {"pending_todos": list(PENDING_TODOS), "pending_todo_count": 2}

    monkeypatch.setattr(ContextAssembler, "gather_context", fake_gather)
    monkeypatch.setattr(
        ContextAssembler, "get_last_provenance", lambda self: {"pending_todos": {"source": "stub"}}
    )
    return calls


class TestUnknownIntentFloorEntryGathersContext:
    """The shared floor entry must gather domain context when the caller
    supplied none — under a NON-None principal (PM's authenticated shape)."""

    @pytest.mark.asyncio
    async def test_pending_todos_reach_floor_for_generic_query(
        self, captured_floor, gather_spy
    ):
        """PM's sentence shape: unrailed QUERY emission → generic → floor.
        RED before #1570: domain_context arrived as None (no gather ever ran)."""
        session_id, user_id = str(uuid4()), str(uuid4())
        intent = _intent(
            IntentCategory.QUERY,
            "list_pending_todos_unrailed",  # mode-4 paraphrase past the rail
            "what todos are pending?",
            user_id,
        )
        result = await _svc()._handle_query_intent(intent, None, session_id, user_id)

        assert result.success
        assert captured_floor, "floor was never reached"
        ctx = captured_floor[-1]
        assert ctx.domain_context, (
            "floor received NO domain context on the generic-query entry — "
            "the #1570 empty-data mechanism"
        )
        assert ctx.domain_context.get("pending_todos") == PENDING_TODOS
        # principal threading verdict: gather ran under the AUTHENTICATED key
        assert gather_spy and gather_spy[-1]["user_id"] == user_id
        clear_context(session_id, user_id)

    @pytest.mark.asyncio
    async def test_offer_fallback_floor_entry_gathers_too(
        self, captured_floor, gather_spy
    ):
        """The bound-offer acceptance fallback (#1570 projects lane) is a
        direct `_handle_unknown_intent` call with an UNKNOWN-category intent
        and an explicit user_id — it must gather as well."""
        session_id, user_id = str(uuid4()), str(uuid4())
        intent = _intent(IntentCategory.UNKNOWN, "status_check", "yes please", user_id)
        result = await _svc()._handle_unknown_intent(
            intent, None, session_id, user_id=user_id
        )

        assert result.success
        ctx = captured_floor[-1]
        assert ctx.domain_context and ctx.domain_context.get("pending_todos") == PENDING_TODOS
        assert gather_spy[-1]["user_id"] == user_id
        clear_context(session_id, user_id)

    @pytest.mark.asyncio
    async def test_provenance_threads_alongside_gathered_context(
        self, captured_floor, gather_spy
    ):
        """#1030 R4 parity with _handle_floor_with_context: when this entry
        gathers, the provenance map rides with it."""
        session_id, user_id = str(uuid4()), str(uuid4())
        intent = _intent(IntentCategory.UNKNOWN, "unknown", "what's pending?", user_id)
        await _svc()._handle_unknown_intent(intent, None, session_id, user_id=user_id)

        ctx = captured_floor[-1]
        assert ctx.domain_context_provenance == {"pending_todos": {"source": "stub"}}
        clear_context(session_id, user_id)


class TestCallerCuratedContextIsPreserved:
    """#1187 summarize passes a curated domain_context — the gather must not
    replace it (the caller knows what the floor should reason over)."""

    @pytest.mark.asyncio
    async def test_supplied_domain_context_passes_through_without_gather(
        self, captured_floor, gather_spy
    ):
        session_id, user_id = str(uuid4()), str(uuid4())
        curated = {"summary_source": {"content": "issue body to summarize"}}
        intent = _intent(IntentCategory.UNKNOWN, "summarize", "summarize #42", user_id)
        await _svc()._handle_unknown_intent(
            intent, None, session_id, user_id=user_id, domain_context=curated
        )

        ctx = captured_floor[-1]
        assert ctx.domain_context == curated
        assert not gather_spy, "curated context must not trigger a second gather"
        clear_context(session_id, user_id)


class TestGatherFailureNeverKillsTheFloor:
    @pytest.mark.asyncio
    async def test_gather_exception_degrades_to_contextless_floor(
        self, captured_floor, monkeypatch
    ):
        monkeypatch.setattr(
            ContextAssembler,
            "gather_context",
            AsyncMock(side_effect=RuntimeError("db down")),
        )
        session_id, user_id = str(uuid4()), str(uuid4())
        intent = _intent(IntentCategory.UNKNOWN, "unknown", "hello?", user_id)
        result = await _svc()._handle_unknown_intent(
            intent, None, session_id, user_id=user_id
        )
        assert result.success, "a gather failure must never take down the floor reply"
        assert captured_floor[-1].domain_context is None
        clear_context(session_id, user_id)
