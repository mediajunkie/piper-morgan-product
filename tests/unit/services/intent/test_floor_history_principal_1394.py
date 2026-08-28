"""#1394 session-continuity gap — prior turns must reach the floor's context
on the AUTHENTICATED chat path.

Root cause being guarded: the in-memory conversation registry is keyed by
``f"{user_id or 'anonymous'}:{session_id}"`` (#817). The outer process_intent
seam records every turn under the AUTHENTICATED key, but a family of category
fall-through paths dropped ``user_id`` on their way to the floor —
``_handle_generic_query`` (QUERY), the ANALYSIS/SYNTHESIS/STRATEGY/LEARNING
fall-throughs, and the soft-offer unknown-workflow path — so
``build_recent_history(session_id, None)`` read the EMPTY ``anonymous:`` context
and the floor prompt carried no prior turns. Same split-brain for the #852
contextual-offer pair (write at the canonical seam / read at turn start), which
used the anonymous key while #953 persistence and the floor flags used the
authenticated key.

Why no existing test caught it: every pipeline-level test drove these paths
with ``user_id=None``, where the anonymous keys coincide. The live chat path is
always authenticated (alpha + beta identically) — the probe's shape didn't
match the live shape.

These tests assert on the ACTUAL FloorContext handed to ConversationalFloor
(captured via respond()), not on a mock's return value.
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import conversational_floor as cf
from services.intent_service.conversation_context import (
    clear_context,
    get_or_create_context,
)
from services.shared_types import IntentCategory

PRIOR_USER_MSG = "let's call the new initiative Project CoVa"
PRIOR_ASSISTANT_MSG = "Noted — Project CoVa it is."


def _fresh_ids():
    return str(uuid4()), str(uuid4())


def _seed_authenticated_history(session_id: str, user_id: str, current_message: str):
    """Reproduce what the outer process_intent seam does on the chat path:
    a completed prior turn + the in-flight turn, recorded under the
    AUTHENTICATED registry key."""
    ctx = get_or_create_context(session_id, user_id=user_id)
    prior = ctx.add_turn(message=PRIOR_USER_MSG)
    prior.response = PRIOR_ASSISTANT_MSG
    ctx.add_turn(message=current_message)  # in-flight (response None)
    return ctx


def _svc():
    """Bare service — floor fall-through paths only need the logger."""
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    return svc


@pytest.fixture
def captured_floor(monkeypatch):
    """Capture every FloorContext the floor is asked to respond to."""
    captured = []

    async def fake_respond(self, ctx):
        captured.append(ctx)
        return cf.FloorResponse(message="(stubbed floor answer)")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", fake_respond)
    return captured


def _intent(category, action, message, user_id=None):
    intent = Intent(
        category=category,
        action=action,
        confidence=0.8,
        original_message=message,
    )
    # process_intent stamps the principal onto intent.context (#490/#1252)
    # BEFORE category routing — the fall-through paths can always recover it.
    intent.context = {"user_id": user_id} if user_id else {}
    return intent


def _assert_history_reaches_floor(captured):
    assert captured, "floor was never reached"
    history = captured[-1].conversation_history
    assert {
        "role": "user",
        "content": PRIOR_USER_MSG,
    } in history, f"prior turn missing from floor history: {history!r}"
    assert {"role": "assistant", "content": PRIOR_ASSISTANT_MSG} in history
    # and the prompt the LLM would actually see carries it (m-43: right layer)
    prompt = cf.ConversationalFloor()._build_prompt(captured[-1])
    assert "Project CoVa" in prompt


class TestQueryFallthroughHistory:
    """PM's Exhibit B shape: authenticated QUERY with no specialized handler
    floors via _handle_query_intent → _handle_generic_query."""

    @pytest.mark.asyncio
    async def test_generic_query_floor_sees_authenticated_history(self, captured_floor):
        session_id, user_id = _fresh_ids()
        message = "what do you know about the CoVa project?"
        _seed_authenticated_history(session_id, user_id, message)

        intent = _intent(IntentCategory.QUERY, "project_info_query_unrailed", message, user_id)
        result = await _svc()._handle_query_intent(intent, None, session_id, user_id)

        assert result.success
        _assert_history_reaches_floor(captured_floor)
        clear_context(session_id, user_id)

    @pytest.mark.asyncio
    async def test_floor_continuation_flags_land_on_authenticated_context(self, captured_floor):
        """The #913 floor tag must land on the SAME context the outer seam
        reads next turn — the authenticated one, not anonymous."""
        session_id, user_id = _fresh_ids()
        message = "what do you know about the CoVa project?"
        _seed_authenticated_history(session_id, user_id, message)

        intent = _intent(IntentCategory.QUERY, "project_info_query_unrailed", message, user_id)
        await _svc()._handle_query_intent(intent, None, session_id, user_id)

        assert get_or_create_context(session_id, user_id=user_id).last_response_was_floor
        assert not get_or_create_context(session_id).last_response_was_floor
        clear_context(session_id, user_id)
        clear_context(session_id)


class TestCategoryFallthroughHistory:
    """The ANALYSIS/SYNTHESIS/STRATEGY/LEARNING fall-throughs never received a
    user_id parameter at all — they must recover the principal from the intent
    (the sanctioned _principal_from_intent read) before flooring."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "handler_name,category,action",
        [
            ("_handle_analysis_intent", IntentCategory.ANALYSIS, "analyze_vibes_unrailed"),
            ("_handle_synthesis_intent", IntentCategory.SYNTHESIS, "brainstorm_unrailed"),
            ("_handle_strategy_intent", IntentCategory.STRATEGY, "ponder_strategy_unrailed"),
            ("_handle_learning_intent", IntentCategory.LEARNING, "reflect_unrailed"),
        ],
    )
    async def test_fallthrough_floor_sees_authenticated_history(
        self, captured_floor, handler_name, category, action
    ):
        session_id, user_id = _fresh_ids()
        message = "keep going with what we discussed"
        _seed_authenticated_history(session_id, user_id, message)

        intent = _intent(category, action, message, user_id)
        result = await getattr(_svc(), handler_name)(intent, None, session_id)

        assert result.success
        _assert_history_reaches_floor(captured_floor)
        clear_context(session_id, user_id)

    @pytest.mark.asyncio
    async def test_unknown_intent_recovers_principal_from_intent_context(self, captured_floor):
        """Direct guard on the shared floor entry: user_id param absent but the
        principal stamped on the intent → history still reaches the floor."""
        session_id, user_id = _fresh_ids()
        message = "and what about the thing from before?"
        _seed_authenticated_history(session_id, user_id, message)

        intent = _intent(IntentCategory.UNKNOWN, "unknown", message, user_id)
        result = await _svc()._handle_unknown_intent(intent, None, session_id)

        assert result.success
        _assert_history_reaches_floor(captured_floor)
        clear_context(session_id, user_id)

    @pytest.mark.asyncio
    async def test_no_principal_anywhere_still_works_with_empty_history(self, captured_floor):
        """Genuinely anonymous call (no param, no stamp): unchanged behavior —
        floor responds, history is whatever the anonymous context holds."""
        session_id, _ = _fresh_ids()
        intent = _intent(IntentCategory.UNKNOWN, "unknown", "hello there")
        result = await _svc()._handle_unknown_intent(intent, None, session_id)
        assert result.success
        assert captured_floor[-1].conversation_history == []
        clear_context(session_id)


class TestContextualOfferUserScoped:
    """#852 offer pair (write at canonical seam, read at next turn start) must
    live on the AUTHENTICATED context — the same one #953 persists and the
    outer seam hydrates. Driven through the real process_intent pipeline."""

    def _pipeline_service(self, canonical_result):
        classifier = MagicMock()

        def _multi(message, context=None, user_id=None, session_id=None):
            from services.intent_service.pre_classifier import MultiIntentResult

            intent = Intent(
                category=IntentCategory.PORTFOLIO,
                action="portfolio_help",
                confidence=1.0,
                original_message=message,
            )
            mr = MultiIntentResult(
                intents=[intent], original_message=message, is_multi_intent=False
            )
            return mr

        classifier.classify_multiple = AsyncMock(side_effect=_multi)
        classifier.classify = AsyncMock()

        svc = IntentService(intent_classifier=classifier)
        svc.canonical_handlers = MagicMock()
        svc.canonical_handlers.can_handle = MagicMock(return_value=True)
        svc.canonical_handlers.handle = AsyncMock(return_value=canonical_result)
        # keep the pipeline hermetic — no guided processes, no resume offers
        svc._check_active_guided_process = AsyncMock(return_value=(None, None))
        svc._check_pending_resume_offer = AsyncMock(return_value=None)
        return svc, classifier

    @pytest.fixture(autouse=True)
    def _no_db(self, monkeypatch):
        """Force every best-effort DB block (formality/trust/learning/#953)
        onto its fallback path so the test is hermetic."""
        from contextlib import asynccontextmanager

        from services.database import session_factory as sf

        @asynccontextmanager
        async def _raise():
            raise RuntimeError("no db in unit test")
            yield  # pragma: no cover

        monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", _raise)
        monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope_fresh", _raise)

        import services.intent.intent_service as isvc

        monkeypatch.setattr(
            isvc.PersonalityProfile,
            "load_with_preferences",
            AsyncMock(side_effect=RuntimeError("no db in unit test")),
        )

    @pytest.mark.asyncio
    async def test_offer_hint_stored_on_authenticated_context(self):
        session_id, user_id = _fresh_ids()
        svc, _ = self._pipeline_service(
            {
                "message": "Would you like me to explain project context?",
                "intent": {"category": "portfolio", "action": "portfolio_help"},
                "requires_clarification": False,
                "offer_hint": {
                    "continuation_hint": "explain how project context works",
                    "offer_text": "Would you like me to explain project context?",
                },
            }
        )

        await svc.process_intent(
            message="how do I set up projects?", session_id=session_id, user_id=user_id
        )

        user_ctx = get_or_create_context(session_id, user_id=user_id)
        assert user_ctx.last_offer is not None, (
            "offer_hint landed on the anonymous context — the authenticated "
            "read next turn (and #953 persistence) will never see it"
        )
        assert user_ctx.last_offer.continuation_hint == "explain how project context works"
        assert get_or_create_context(session_id).last_offer is None
        clear_context(session_id, user_id)
        clear_context(session_id)

    @pytest.mark.asyncio
    async def test_yes_after_offer_consumes_hint_from_authenticated_context(self):
        from services.intent_service.conversation_context import LastOffer

        session_id, user_id = _fresh_ids()
        user_ctx = get_or_create_context(session_id, user_id=user_id)
        user_ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="explain how project context works",
        )

        svc, classifier = self._pipeline_service(
            {
                "message": "Sure — project context works like this.",
                "intent": {"category": "portfolio", "action": "portfolio_help"},
                "requires_clarification": False,
            }
        )

        await svc.process_intent(message="yes", session_id=session_id, user_id=user_id)

        call_kwargs = classifier.classify_multiple.call_args.kwargs
        passed_context = call_kwargs.get("context") or {}
        assert (
            passed_context.get("contextual_continuation_hint")
            == "explain how project context works"
        ), "authenticated last_offer was not consumed at turn start"
        # one-turn memory: cleared after the read
        assert get_or_create_context(session_id, user_id=user_id).last_offer is None
        clear_context(session_id, user_id)
        clear_context(session_id)
