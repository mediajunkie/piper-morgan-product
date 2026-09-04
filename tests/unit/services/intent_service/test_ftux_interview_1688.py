"""#1688 — FTUX empty-state interview (Leg D increment 1, cold-start
reflection), web-chat half.

The sibling gap to #1536: the rich case demonstrates with real data; the
EMPTY case (cold user, zero connected sources) met an ordinary greeting. Per
the FTUX model the interview OWNS the empty moment (same rule that
suppresses the #1635 Radar placeholder on empty).

Copy is CXO's v0.2 spec VERBATIM
(docs/internal/design/ftux-mcp-first-turn-copy-2026-09-02.md §3a) with ONE
scope cut ruled by PPM 2026-09-03: the `why_asking` string promised
cross-session recall (increment 6, #1705, unbuilt) and is CUT ENTIRELY —
not reworded, not softened. These tests pin the literals (grep-able
copy-drift protection, the #1635 pattern) AND pin the promise language as
ABSENT from every rendered surface.

Binding: the interview arms a #846 pending-offer record (the #1654 carrier
idiom — no new message-parsing regex; the extraction ratchet is frozen);
the answer binds WHOLE at the offer seam into session-scoped
ConversationContext and is used WITHIN-SESSION only (assembler → floor
domain context). Declines, bare exits, and pre-classifier-claimed commands
release unbound.

Layer honesty (m-43): greeting tests assert the FINAL user-facing message
(deterministic path); floor tests assert the prompt block handed to the LLM
(the composed reply is LLM work, not measured here); seam tests assert the
handler contract + context binding.
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversation_context import (
    ConversationContext,
    get_or_create_context,
)
from services.intent_service.conversational_floor import ConversationalFloor
from services.intent_service.first_contact import (
    FTUX_INTERVIEW_OPENING_LINE,
    FTUX_INTERVIEW_QUESTION,
    FTUX_INTERVIEW_QUESTION_KIND,
    FTUX_INTERVIEW_WORKFLOW,
    build_ftux_interview_offer,
    ftux_interview_greeting,
    handle_ftux_interview_turn,
    is_cold_user,
    render_ftux_interview,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

# The promise-language pin (PPM ruling 2026-09-03): the cut `why_asking`
# string's distinctive phrases must be ABSENT from every rendered surface.
# Checked case-insensitively; "hold on to" covers the spaced variant.
PROMISE_PHRASES = ("bring it back", "next time", "hold onto", "hold on to")


def _assert_no_promise_language(text: str):
    low = (text or "").lower()
    for phrase in PROMISE_PHRASES:
        assert phrase not in low, f"promise language {phrase!r} in: {text!r}"


def _fresh_session(user_id=None, first_message="hello"):
    """A brand-new conversation with only the in-flight turn (#1122)."""
    session_id = str(uuid4())
    conv_ctx = get_or_create_context(session_id, user_id=user_id)
    conv_ctx.add_turn(message=first_message)
    return session_id


def _warm_session(user_id=None):
    session_id = str(uuid4())
    conv_ctx = get_or_create_context(session_id, user_id=user_id)
    conv_ctx.add_turn(message="hello")
    conv_ctx.turns[-1].response = "Hi!"
    conv_ctx.add_turn(message="second message")
    return session_id


def _status_all(configured_map):
    """Patch IntegrationStatusService.get_all to a fixed status map."""
    inst = MagicMock()
    inst.get_all = AsyncMock(return_value={k: {"configured": v} for k, v in configured_map.items()})
    inst.is_configured = AsyncMock(side_effect=lambda uid, iid: configured_map.get(iid, False))
    return patch(
        "services.integrations.integration_status_service.IntegrationStatusService",
        return_value=inst,
    )


COLD = {"github": False, "google_calendar": False, "slack": False, "notion": False}
WARM_GH = {**COLD, "github": True}


# ---------------------------------------------------------------------------
# Copy pins — CXO v0.2 verbatim, minus why_asking (PPM cut)
# ---------------------------------------------------------------------------


class TestCopyPins:
    def test_opening_line_verbatim_v02(self):
        assert FTUX_INTERVIEW_OPENING_LINE == (
            "I don't have anything of yours in front of me yet — nothing's connected."
        )

    def test_question_verbatim_v02(self):
        assert FTUX_INTERVIEW_QUESTION == ("What's the thing most on your mind at work right now?")

    def test_render_is_the_two_strings_and_nothing_else(self):
        assert render_ftux_interview() == (
            f"{FTUX_INTERVIEW_OPENING_LINE}\n\n{FTUX_INTERVIEW_QUESTION}"
        )

    def test_no_promise_language_on_any_rendered_surface(self):
        """The why_asking cut, enforced: no string a user (or the floor's
        LLM) can see carries the recall promise. Covers the rendered
        interview, every string in the offer record, and the floor guidance
        for a bound answer."""
        _assert_no_promise_language(render_ftux_interview())
        offer = build_ftux_interview_offer(str(uuid4()))

        def walk(value):
            if isinstance(value, str):
                _assert_no_promise_language(value)
            elif isinstance(value, dict):
                for v in value.values():
                    walk(v)

        walk(offer)
        floor_block = ConversationalFloor()._format_domain_context(
            {"ftux_interview_answer": "the beta launch"}
        )
        _assert_no_promise_language(floor_block)

    def test_no_saved_or_remembered_claims_in_deterministic_copy(self):
        """#1648 action-claims contract: the deterministic strings never
        claim anything was saved or remembered (nothing is)."""
        offer = build_ftux_interview_offer(str(uuid4()))
        for text in (render_ftux_interview(), offer["decline_message"]):
            low = text.lower()
            assert "saved" not in low and "remember" not in low


# ---------------------------------------------------------------------------
# Cold detection — "nothing's connected" must be literally true
# ---------------------------------------------------------------------------


class TestIsColdUser:
    @pytest.mark.asyncio
    async def test_zero_configured_integrations_is_cold(self):
        with _status_all(COLD):
            assert await is_cold_user(str(uuid4())) is True

    @pytest.mark.asyncio
    async def test_any_configured_integration_is_not_cold(self):
        with _status_all(WARM_GH):
            assert await is_cold_user(str(uuid4())) is False

    @pytest.mark.asyncio
    async def test_no_principal_is_not_cold(self):
        """Fail-closed: an unidentified principal gets no interview."""
        assert await is_cold_user(None) is False

    @pytest.mark.asyncio
    async def test_status_error_is_not_cold(self):
        """Fail-closed: a broken probe must never yield a false
        "nothing's connected" over an account that may be connected."""
        inst = MagicMock()
        inst.get_all = AsyncMock(side_effect=RuntimeError("boom"))
        with patch(
            "services.integrations.integration_status_service.IntegrationStatusService",
            return_value=inst,
        ):
            assert await is_cold_user(str(uuid4())) is False


# ---------------------------------------------------------------------------
# The greeting seam — interview iff first exchange AND cold
# ---------------------------------------------------------------------------


class TestFtuxInterviewGreeting:
    @pytest.mark.asyncio
    async def test_cold_first_exchange_gets_interview_with_armed_offer(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        with _status_all(COLD):
            result = await ftux_interview_greeting(session_id, user_id)
        assert result is not None
        assert result["message"] == render_ftux_interview()
        offer = result["offer"]
        assert offer["workflow_type"] == FTUX_INTERVIEW_WORKFLOW
        assert offer["pending_action"]["kind"] == FTUX_INTERVIEW_QUESTION_KIND
        assert offer["pending_action"]["user_id"] == user_id
        # #1665: the stored question is the ask verbatim as rendered
        assert offer["question"] == FTUX_INTERVIEW_QUESTION

    @pytest.mark.asyncio
    async def test_non_cold_user_does_not_get_interview(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        with _status_all(WARM_GH):
            assert await ftux_interview_greeting(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_warm_conversation_does_not_get_interview(self):
        user_id = str(uuid4())
        session_id = _warm_session(user_id)
        with _status_all(COLD):
            assert await ftux_interview_greeting(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_no_user_id_does_not_get_interview(self):
        session_id = _fresh_session()
        with _status_all(COLD):
            assert await ftux_interview_greeting(session_id, None) is None


class TestGreetingHandler:
    @pytest.mark.asyncio
    async def test_cold_greeting_is_the_interview_and_carries_the_offer(self):
        """The interview OWNS the empty moment: the reply is CXO's copy with
        no competing canned question, and the #846 carrier rides the result
        for the canonical seam to arm."""
        from services.conversation.conversation_handler import ConversationHandler
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
            original_message="hello",
            context={"user_id": user_id},
        )
        with _status_all(COLD):
            result = await ConversationHandler()._respond_to_greeting(
                intent, session_id, user_id=user_id
            )
        assert result["message"] == render_ftux_interview()
        assert "work on today" not in result["message"]  # no competing question
        assert result["ftux_interview_offer"]["pending_action"]["kind"] == (
            FTUX_INTERVIEW_QUESTION_KIND
        )
        # The one-slot store protection flag (#1605): a soft offer must not
        # clobber the just-armed question.
        assert result["intent"]["ftux_interview_question_pending"] is True

    @pytest.mark.asyncio
    async def test_non_cold_greeting_unchanged(self):
        from services.conversation.conversation_handler import ConversationHandler
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
            original_message="hello",
            context={"user_id": user_id},
        )
        handler = ConversationHandler()
        with (
            _status_all(WARM_GH),
            patch.object(handler, "_get_calendar_summary", AsyncMock(return_value=None)),
            patch(
                "services.intent_service.first_contact.first_contact_demo_block",
                AsyncMock(return_value=""),
            ),
        ):
            result = await handler._respond_to_greeting(intent, session_id, user_id=user_id)
        assert "ftux_interview_offer" not in result
        assert result["message"] != render_ftux_interview()


# ---------------------------------------------------------------------------
# The offer seam — binding semantics (#1654 carrier idiom)
# ---------------------------------------------------------------------------


def _intent_service_mock():
    svc = MagicMock()
    svc.workflow_offer_service = MagicMock()
    return svc


def _ctx_answer(session_id, user_id):
    return get_or_create_context(session_id, user_id=user_id).ftux_interview_answer


class TestHandleFtuxInterviewTurn:
    @pytest.mark.asyncio
    async def test_substantive_answer_binds_and_routes_to_floor(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        offer = build_ftux_interview_offer(user_id)
        turn = await handle_ftux_interview_turn(
            offer,
            "our beta launch keeps slipping",
            session_id=session_id,
            user_id=user_id,
            intent_service=_intent_service_mock(),
        )
        assert turn is not None and turn.get("route_to_floor") is True
        assert turn["intent_data"]["ftux_interview_answer_bound"] is True
        assert _ctx_answer(session_id, user_id) == "our beta launch keeps slipping"

    @pytest.mark.asyncio
    async def test_decline_releases_unbound(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        offer = build_ftux_interview_offer(user_id)
        turn = await handle_ftux_interview_turn(
            offer,
            "no thanks",
            session_id=session_id,
            user_id=user_id,
            intent_service=_intent_service_mock(),
        )
        assert turn is None  # generic flow → honest decline via decline_message
        assert _ctx_answer(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_bare_exit_releases_unbound(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        offer = build_ftux_interview_offer(user_id)
        turn = await handle_ftux_interview_turn(
            offer,
            "cancel",
            session_id=session_id,
            user_id=user_id,
            intent_service=_intent_service_mock(),
        )
        assert turn is None
        assert _ctx_answer(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_preclassifier_claimed_command_releases_unbound(self):
        """A deterministic product command is not an answer — release it to
        route normally (the #1654 discriminator, same granularity)."""
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        offer = build_ftux_interview_offer(user_id)
        turn = await handle_ftux_interview_turn(
            offer,
            "list my reminders",
            session_id=session_id,
            user_id=user_id,
            intent_service=_intent_service_mock(),
        )
        assert turn is None
        assert _ctx_answer(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_bare_accept_reasks_verbatim_and_rearms(self):
        """A bare "yes" doesn't answer an open question — the honest re-ask
        (#1648 direction 2), question verbatim, offer re-armed."""
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        offer = build_ftux_interview_offer(user_id)
        svc = _intent_service_mock()
        turn = await handle_ftux_interview_turn(
            offer, "yes", session_id=session_id, user_id=user_id, intent_service=svc
        )
        assert turn is not None
        assert turn["message"] == FTUX_INTERVIEW_QUESTION
        assert turn["intent_data"]["ftux_interview_question_pending"] is True
        svc.workflow_offer_service.set_pending_offer.assert_called_once()
        rearmed = svc.workflow_offer_service.set_pending_offer.call_args[0][1]
        assert rearmed["pending_action"]["kind"] == FTUX_INTERVIEW_QUESTION_KIND
        assert _ctx_answer(session_id, user_id) is None

    @pytest.mark.asyncio
    async def test_principal_mismatch_releases_unbound(self):
        asker = str(uuid4())
        other = str(uuid4())
        session_id = _fresh_session(other)
        offer = build_ftux_interview_offer(asker)
        turn = await handle_ftux_interview_turn(
            offer,
            "our beta launch keeps slipping",
            session_id=session_id,
            user_id=other,
            intent_service=_intent_service_mock(),
        )
        assert turn is None
        assert _ctx_answer(session_id, other) is None

    @pytest.mark.asyncio
    async def test_empty_message_releases(self):
        user_id = str(uuid4())
        session_id = _fresh_session(user_id)
        turn = await handle_ftux_interview_turn(
            build_ftux_interview_offer(user_id),
            "   ",
            session_id=session_id,
            user_id=user_id,
            intent_service=_intent_service_mock(),
        )
        assert turn is None


# ---------------------------------------------------------------------------
# Within-session use — assembler + floor surfaces the bound answer
# ---------------------------------------------------------------------------

_CATEGORY_GATHERERS = [
    "_gather_identity_context",
    "_gather_trust_context",
    "_gather_insight_pull_context",
    "_gather_memory_context",
    "_gather_temporal_context",
    "_gather_status_priority_context",
]


def _quiet_gatherers():
    patchers = [
        patch.object(ContextAssembler, name, AsyncMock(return_value={}))
        for name in _CATEGORY_GATHERERS
    ]
    patchers.append(
        patch.object(ContextAssembler, "_gather_reminder_context", AsyncMock(return_value={}))
    )
    patchers.append(
        patch(
            "services.intent_service.context_assembler._current_time_for_user",
            AsyncMock(return_value=None),
        )
    )
    return patchers


class TestWithinSessionUse:
    @pytest.mark.asyncio
    async def test_bound_answer_reaches_floor_domain_context(self):
        user_id = str(uuid4())
        session_id = _warm_session(user_id)  # later in the session
        get_or_create_context(
            session_id, user_id=user_id
        ).ftux_interview_answer = "our beta launch keeps slipping"
        patchers = _quiet_gatherers()
        for p in patchers:
            p.start()
        try:
            with _status_all(COLD):
                context = await ContextAssembler().gather_context(
                    "UNKNOWN", user_id=user_id, session_id=session_id
                )
        finally:
            for p in patchers:
                p.stop()
        assert context.get("ftux_interview_answer") == "our beta launch keeps slipping"

    def test_floor_guidance_carries_answer_and_no_persistence_claims(self):
        block = ConversationalFloor()._format_domain_context(
            {"ftux_interview_answer": "our beta launch keeps slipping"}
        )
        assert "our beta launch keeps slipping" in block
        # The within-session rule is stated (never claim storage, never
        # promise future-session recall)…
        assert "never claim" in block.lower()
        assert "future session" in block.lower()
        # …without re-teaching the cut promise vocabulary (#1570)
        _assert_no_promise_language(block)
        # #1655 discipline: no incident seed strings in the guidance
        for seed in ("I don't see any todos", "creating that now", "Reminder set for"):
            assert seed not in block

    def test_no_answer_renders_nothing(self):
        assert ConversationalFloor()._format_domain_context({}) == ""


# ---------------------------------------------------------------------------
# Session-scoped persistence (#953 slice) — within-session, never cross-
# ---------------------------------------------------------------------------


class TestPersistableStateRoundTrip:
    def test_round_trip(self):
        ctx = ConversationContext()
        ctx.ftux_interview_answer = "our beta launch keeps slipping"
        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.apply_persisted_state(state)
        assert restored.ftux_interview_answer == "our beta launch keeps slipping"

    def test_legacy_state_without_key_leaves_default(self):
        ctx = ConversationContext()
        ctx.apply_persisted_state({"lens_stack": []})
        assert ctx.ftux_interview_answer is None


# ---------------------------------------------------------------------------
# Wiring pins — the seam dispatch + clobber protection exist in the chain
# (grep-able drift protection; behavior is pinned handler-level above)
# ---------------------------------------------------------------------------


class TestSeamWiringPins:
    def _src(self):
        import services.intent.intent_service as m

        with open(m.__file__) as f:
            return f.read()

    def test_kind_dispatch_and_pending_flag_wired(self):
        src = self._src()
        assert '"ftux_interview_question"' in src  # kind branch + abandon name
        assert '"ftux_interview_question_pending"' in src  # _pending_flags entry

    def test_canonical_seam_arms_the_offer(self):
        src = self._src()
        assert 'canonical_result.get("ftux_interview_offer")' in src
