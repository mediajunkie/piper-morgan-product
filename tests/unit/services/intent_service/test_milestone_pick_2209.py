"""#2209 — an armed milestone pick whose reply names no listed milestone gets CXO's no-match line,
not the conversational floor (Arch's shape, decisions.log 2026-10-29 20:29; seam 20:42; amended 20:55).

The served bug (PA, alpha 48df90eb72): "what are my github milestones?" listed one milestone, "Beta launch",
and armed the pick; "MVP" matched no title, fell out of the pick, routed ``query/get_information`` and the
floor answered about "Beta launch" as if it were what was asked for.

The shape under test:

* the pop seam (``handle_milestone_pick_turn``) still returns None on no match, and sets a TURN-LOCAL marker
  (a per-session dict on the service: set at the pop seam, cleared at the top of ``_process_intent_internal``
  and in ``process_intent``'s finally, consumed on first use);
* the turn routes normally. A dispatched op runs as today and the marker drops;
* the two NON-DISPATCH floor doors (``_handle_floor_with_context``, ``_handle_unknown_intent``) consult the
  marker at their head, before any context assembly or model call: CXO's line from the stored titles, no
  GitHub read, no write, the same titles re-armed ONCE;
* the ethics denial door and the guidance door do not consult it.

Layer honesty (m-43): the real ``IntentService.process_intent`` with an EXPLOSIVE LLM; the classifier's
verdict is stubbed (the LLM chooses it live); the floor's model is stubbed at ``ConversationalFloor.respond``
and context assembly at ``ContextAssembler.gather_context``. No served text is claimed here.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service import milestone_pick as mp
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversational_floor import FloorResponse
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
FLOOR_RESPOND = "services.intent_service.conversational_floor.ConversationalFloor.respond"
GATHER = "services.intent_service.context_assembler.ContextAssembler.gather_context"

_USER = "22092209-2209-4209-8209-000000002209"
_REPO = "dinp-machine/piper-test-activity"
_ARM_ASK = "what are my github milestones?"
FLOOR_TEXT = "FLOOR: The Beta launch milestone has 4 open issues."
LINE_ONE = (
    "I don't see a milestone by that name. Your open milestones: Beta launch. Say one of those."
)


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


@pytest.fixture
def floor():
    """The floor's model, stubbed; context assembly stubbed. Records every call."""
    respond = AsyncMock(return_value=FloorResponse(message=FLOOR_TEXT))
    with patch(FLOOR_RESPOND, new=respond), patch(GATHER, new=AsyncMock(return_value={})):
        yield respond


@pytest.fixture
def github():
    """Every GitHub read and write the pick could reach, explosive."""

    def boom(what):
        return AsyncMock(side_effect=AssertionError(f"GitHub {what} awaited"))

    reads = {
        "get_open_issues": boom("get_open_issues"),
        "list_milestones_via_mcp": boom("list_milestones_via_mcp"),
        "create_issue": boom("create_issue"),
        "update_issue": boom("update_issue"),
    }
    with (
        patch(f"{ROUTER}.get_open_issues", new=reads["get_open_issues"]),
        patch(f"{ROUTER}.list_milestones_via_mcp", new=reads["list_milestones_via_mcp"]),
        patch(f"{ROUTER}.create_issue", new=reads["create_issue"]),
        patch(f"{ROUTER}.update_issue", new=reads["update_issue"]),
    ):
        yield reads


def _arm(service, sid, titles=("Beta launch",), principal=_USER):
    assert mp.arm_milestone_pick(
        session_id=sid,
        principal=principal,
        offer_service=service.workflow_offer_service,
        titles=list(titles),
        repository=_REPO,
        original_message=_ARM_ASK,
    )


def _verdict(service, category, action, message, confidence=0.9):
    service.intent_classifier.classify = AsyncMock(
        return_value=Intent(
            category=category,
            action=action,
            confidence=confidence,
            original_message=message,
            context={"original_message": message},
        )
    )


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


def _marker(service, sid):
    return service._milestone_pick_no_match.get(sid)


def _spy_handlers(service):
    """The pick's own reads, as the service holds them: never awaited on a no-match."""
    issues = AsyncMock(side_effect=AssertionError("issues read awaited"))
    milestones = AsyncMock(side_effect=AssertionError("milestones read awaited"))
    service._handle_list_issues_query = issues
    service._handle_list_milestones_query = milestones
    return issues, milestones


# ---------------------------------------------------------------------------
# The line itself
# ---------------------------------------------------------------------------


class TestTheLine:
    def test_one_title(self):
        assert mp.no_match_line(["Beta launch"], _REPO) == LINE_ONE

    def test_several_titles_comma_separated_in_listed_order(self):
        assert mp.no_match_line(["MVP", "Production", "Beta launch"], _REPO) == (
            "I don't see a milestone by that name. Your open milestones: "
            "MVP, Production, Beta launch. Say one of those."
        )

    def test_no_open_milestones_names_the_repo(self):
        assert mp.no_match_line([], _REPO) == f"I don't see any open milestones in {_REPO}."

    def test_the_line_never_echoes_the_message(self):
        """CXO's unquoted form (Arch 20:55): the user's words are not repeated back."""
        assert "MVP" not in mp.no_match_line(["Beta launch"], _REPO)

    def test_no_milestones_form_answers_and_arms_nothing(self, service):
        sid = "s2209-none"
        mp.set_no_match_marker(
            service,
            sid,
            {"pick_titles": [], "repository": _REPO, "original_message": _ARM_ASK},
            _USER,
            "MVP",
        )
        result = service._milestone_pick_no_match_result(sid)
        assert result.message == f"I don't see any open milestones in {_REPO}."
        assert result.intent_data[mp.PICK_PENDING_FLAG] is False
        assert result.requires_clarification is False
        assert _pending(service, sid) is None
        assert _marker(service, sid) is None


# ---------------------------------------------------------------------------
# Arch's eight pins
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestArmedNoMatch:
    async def test_pin1_mvp_via_the_unknown_intent_door_gets_the_line_reads_nothing_rearms(
        self, service, floor, github
    ):
        """PA's served turn: armed on ["Beta launch"], "MVP" routes query/get_information, which floors
        through _handle_generic_query -> _handle_unknown_intent. The line answers; the floor's model is
        never called; nothing is read or written; the same titles are re-armed."""
        sid = "s2209-pin1"
        _arm(service, sid)
        issues, milestones = _spy_handlers(service)
        _verdict(service, IntentCategory.QUERY, "get_information", "MVP")
        result = await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        assert result.message == LINE_ONE
        floor.assert_not_awaited()
        issues.assert_not_awaited()
        milestones.assert_not_awaited()
        for m in github.values():
            m.assert_not_awaited()
        rec = _pending(service, sid)
        assert rec["pending_action"]["kind"] == mp.MILESTONE_PICK_KIND
        assert rec["pending_action"]["pick_titles"] == ["Beta launch"]
        assert rec["pending_action"]["repository"] == _REPO
        assert rec["pending_action"]["user_id"] == _USER
        assert rec["pending_action"][mp.REARMED_FLAG] is True
        assert rec["question"] == LINE_ONE
        assert _marker(service, sid) is None

    async def test_pin1b_the_floor_with_context_door_gets_the_line_too(
        self, service, floor, github
    ):
        """The other non-dispatch door: a CONVERSATION landing floors through _handle_floor_with_context."""
        sid = "s2209-pin1b"
        _arm(service, sid, titles=("MVP", "Production"))
        _verdict(service, IntentCategory.CONVERSATION, "chitchat", "the alpha one")
        result = await service.process_intent(
            message="the alpha one", session_id=sid, user_id=_USER
        )
        assert result.message == (
            "I don't see a milestone by that name. Your open milestones: MVP, Production. "
            "Say one of those."
        )
        floor.assert_not_awaited()
        assert _pending(service, sid)["pending_action"]["pick_titles"] == ["MVP", "Production"]

    async def test_pin1c_a_second_caller_of_the_unknown_intent_door_is_covered_by_construction(
        self, service, floor, github
    ):
        """The ANALYSIS fall-through (_handle_analysis_intent -> _handle_unknown_intent): no branch of its
        own, the head of the door covers it."""
        sid = "s2209-pin1c"
        _arm(service, sid)
        _verdict(service, IntentCategory.ANALYSIS, "analyze_something_unrailed", "MVP")
        result = await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        assert result.message == LINE_ONE
        floor.assert_not_awaited()

    async def test_pin2_a_dispatching_request_runs_and_the_marker_drops(
        self, service, floor, github
    ):
        sid = "s2209-pin2"
        _arm(service, sid)
        _verdict(service, IntentCategory.TEMPORAL, "get_current_time", "what time is it", 1.0)
        result = await service.process_intent(
            message="what time is it", session_id=sid, user_id=_USER
        )
        assert "milestone" not in result.message
        assert result.intent_data.get("milestone_pick_no_match") is None
        floor.assert_not_awaited()
        assert _marker(service, sid) is None
        # Whatever the pending store holds is today's behaviour (#1739: a question-form turn keeps the
        # arm silently); the no-match line re-armed nothing.
        rec = _pending(service, sid)
        assert rec is None or not rec["pending_action"].get(mp.REARMED_FLAG)

    async def test_pin3_an_exact_title_binds_as_today(self, service, floor, github):
        sid = "s2209-pin3"
        _arm(service, sid)
        service._handle_list_issues_query = AsyncMock(
            return_value=IntentProcessingResult(
                success=True,
                message=f'You have **4 open issues** in {_REPO} in milestone "Beta launch".',
                intent_data={},
            )
        )
        result = await service.process_intent(message="Beta launch", session_id=sid, user_id=_USER)
        assert result.message.startswith("You have **4 open issues**")
        intent = service._handle_list_issues_query.await_args.args[0]
        assert intent.context["list_scope_milestone"] == "Beta launch"
        assert _marker(service, sid) is None
        floor.assert_not_awaited()

    @pytest.mark.parametrize("turn_user", [None, "33333333-3333-4333-8333-333333333333"])
    async def test_pin4_no_or_mismatched_principal_keeps_todays_decline(
        self, service, floor, github, turn_user
    ):
        """No marker is set when the principal check declines (13:04): the pick says nothing and the
        turn reaches the floor as today."""
        sid = f"s2209-pin4-{turn_user}"
        _arm(service, sid)
        rec = _pending(service, sid)
        assert await mp.handle_milestone_pick_turn(rec, "MVP", sid, turn_user, service) is None
        assert _marker(service, sid) is None
        # End to end with a mismatched principal: the floor answers, no line.
        if turn_user is not None:
            _verdict(service, IntentCategory.CONVERSATION, "chitchat", "MVP")
            result = await service.process_intent(message="MVP", session_id=sid, user_id=turn_user)
            assert result.message.startswith("FLOOR:")
            assert "don't see a milestone" not in result.message
            floor.assert_awaited()

    async def test_pin5_the_rearm_happens_once(self, service, floor, github):
        sid = "s2209-pin5"
        _arm(service, sid)
        _verdict(service, IntentCategory.QUERY, "get_information", "MVP")
        first = await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        assert first.message == LINE_ONE
        _verdict(service, IntentCategory.QUERY, "get_information", "MVP please")
        second = await service.process_intent(message="MVP please", session_id=sid, user_id=_USER)
        assert "don't see a milestone" not in second.message
        assert second.message.startswith("FLOOR:")
        floor.assert_awaited_once()
        assert _pending(service, sid) is None  # no second re-arm
        assert _marker(service, sid) is None

    async def test_pin5b_after_the_line_an_exact_title_still_binds(self, service, floor, github):
        sid = "s2209-pin5b"
        _arm(service, sid)
        _verdict(service, IntentCategory.QUERY, "get_information", "MVP")
        await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        service._handle_list_issues_query = AsyncMock(
            return_value=IntentProcessingResult(success=True, message="ISSUES", intent_data={})
        )
        result = await service.process_intent(message="Beta launch", session_id=sid, user_id=_USER)
        assert result.message == "ISSUES"
        assert (
            service._handle_list_issues_query.await_args.args[0].context["list_scope_milestone"]
            == "Beta launch"
        )

    async def test_pin7_the_ethics_denial_door_outranks_the_pick(self, service, floor, github):
        from services.ethics.boundary_enforcer_refactored import BoundaryDecision, BoundaryType

        sid = "s2209-pin7"
        _arm(service, sid)
        decision = BoundaryDecision(
            violation_detected=True,
            boundary_type=BoundaryType.HARASSMENT,
            explanation="test",
            audit_data={"decision_id": "bd_2209"},
            session_id=sid,
            redirect_context="redirect",
        )
        floor.return_value = FloorResponse(message="DECLINE: not one I'll help with.")
        with (
            patch.dict("os.environ", {"ENABLE_ETHICS_ENFORCEMENT": "true"}),
            patch(
                "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
                new=AsyncMock(return_value=decision),
            ),
        ):
            result = await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        assert result.message.startswith("DECLINE:")
        assert "don't see a milestone" not in result.message
        floor.assert_awaited_once()
        assert floor.await_args.args[0].denial_mode is True
        assert _marker(service, sid) is None  # discarded by the turn-end clear
        assert _pending(service, sid) is None  # not re-armed

    async def test_pin8_the_guidance_door_does_not_consult_the_marker(self, service, floor, github):
        """``_handle_guidance_via_floor`` is driven directly: a marker present for the session is neither
        used nor consumed there (the turn-end clear discards it)."""
        sid = "s2209-pin8"
        mp.set_no_match_marker(
            service,
            sid,
            {"pick_titles": ["Beta launch"], "repository": _REPO, "original_message": _ARM_ASK},
            _USER,
            "MVP",
        )
        intent = Intent(
            category=IntentCategory.GUIDANCE,
            action="get_guidance",
            confidence=0.9,
            original_message="how should I plan this week?",
            context={"original_message": "how should I plan this week?", "user_id": _USER},
        )
        with patch.object(service, "_assemble_guidance_context", new=AsyncMock(return_value={})):
            result = await service._handle_guidance_via_floor(intent, sid, user_id=_USER)
        assert result.message.startswith("FLOOR:")
        floor.assert_awaited_once()
        assert _marker(service, sid) is not None
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# The marker never leaks; un-armed turns are unchanged
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTurnLocal:
    async def test_marker_is_cleared_even_when_the_turn_raises(self, service, floor, github):
        sid = "s2209-raise"
        _arm(service, sid)
        service.intent_classifier.classify = AsyncMock(side_effect=RuntimeError("boom"))
        try:
            await service.process_intent(message="MVP", session_id=sid, user_id=_USER)
        except Exception:  # noqa: BLE001 - the turn's own error handling is not under test
            pass
        assert _marker(service, sid) is None

    async def test_a_stale_marker_is_cleared_at_turn_start(self, service, floor, github):
        sid = "s2209-stale"
        mp.set_no_match_marker(
            service,
            sid,
            {"pick_titles": ["Beta launch"], "repository": _REPO, "original_message": _ARM_ASK},
            _USER,
            "MVP",
        )
        _verdict(service, IntentCategory.QUERY, "get_information", "MVP")
        result = await service._process_intent_internal(
            message="MVP", session_id=sid, user_id=_USER
        )
        assert result.message.startswith("FLOOR:")
        floor.assert_awaited_once()

    @pytest.mark.parametrize("door", ["_handle_floor_with_context", "_handle_unknown_intent"])
    async def test_unarmed_door_call_is_unchanged(self, service, floor, door):
        """Byte-identity pin: with no marker the head returns to the existing path; the floor receives
        the same FloorContext it would without the branch, and the reply is the floor's."""
        sid = f"s2209-unarmed-{door}"
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="chitchat",
            confidence=0.9,
            original_message="MVP",
            context={"original_message": "MVP", "user_id": _USER},
        )
        if door == "_handle_floor_with_context":
            result = await service._handle_floor_with_context(intent, sid, user_id=_USER)
        else:
            result = await service._handle_unknown_intent(intent, None, sid, user_id=_USER)
        assert result.message == FLOOR_TEXT
        floor.assert_awaited_once()
        ctx = floor.await_args.args[0]
        assert ctx.user_message == "MVP"
        assert ctx.session_id == sid
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# Pin 6: the per-element floor door (multi-intent rule 2 kept)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestMultiIntentPerElementDoor:
    """The per-element caller of ``_handle_floor_with_context`` (in
    ``_maybe_dispatch_multi_intent_inversion``). The marker is set directly here: on the turn the
    pick pops, the live consult skips with ``armed_pending_offer_popped`` and publishes no split or
    plan stand-down, so this path declines on that turn (see ``test_the_popped_turn_never_reaches_it``).
    The head of the method covers this caller by construction; this pins what it does if it ever runs
    with a marker: the line once, armed once, later elements deferred and named (#1595 rule 2)."""

    _MSG = "is there anything you can tell me, what else can you do, and what are my todos"

    def _plan(self, monkeypatch):
        from services.intent_service import inversion_router as ir
        from services.intent_service.inversion_router import RoutingDecision

        ops = [
            {
                "operation": "get_capabilities",
                "args": {},
                "confidence": 0.85,
                "rationale": "asks what Piper can tell",
            },
            {
                "operation": "get_capabilities",
                "args": {},
                "confidence": 0.85,
                "rationale": "asks what else Piper can do",
            },
            {
                "operation": "list_todos_query",
                "args": {},
                "confidence": 0.95,
                "rationale": "list todos",
            },
        ]

        async def _route(utterance, session_state=None, **kwargs):
            if utterance == self._MSG:
                return RoutingDecision(outcome="plan", operations=list(ops))
            return RoutingDecision(outcome="none", operation=None, confidence=None)

        monkeypatch.setattr(ir, "route", _route)
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")

    async def test_pin6_line_once_armed_once_later_elements_deferred_and_named(
        self, service, floor, github, monkeypatch
    ):
        self._plan(monkeypatch)
        sid = "s2209-pin6"
        real_multi = service._maybe_dispatch_multi_intent_inversion

        async def _multi_with_marker(*a, **k):
            # The marker as the pop seam would have left it, inside the turn (a marker set before
            # the turn is cleared at the top of _process_intent_internal).
            mp.set_no_match_marker(
                service,
                sid,
                {"pick_titles": ["Beta launch"], "repository": _REPO, "original_message": _ARM_ASK},
                _USER,
                "MVP",
            )
            return await real_multi(*a, **k)

        monkeypatch.setattr(service, "_maybe_dispatch_multi_intent_inversion", _multi_with_marker)
        sets = []
        real_set = service.workflow_offer_service.set_pending_offer

        def _counting_set(session_id, offer, user_id=None):
            sets.append(offer)
            return real_set(session_id, offer, user_id=user_id)

        monkeypatch.setattr(service.workflow_offer_service, "set_pending_offer", _counting_set)
        result = await service.process_intent(message=self._MSG, session_id=sid, user_id=_USER)
        assert result.intent_data.get("multi_intent_inversion") is True
        assert result.message.count("I don't see a milestone by that name.") == 1
        assert [o["pending_action"]["kind"] for o in sets] == [mp.MILESTONE_PICK_KIND]
        assert "I haven't touched" in result.message
        assert "what else Piper can do" in result.message
        floor.assert_not_awaited()
        assert _marker(service, sid) is None

    async def test_the_popped_turn_never_reaches_it(self, service, floor, github, monkeypatch):
        """On the turn the armed pick pops, the multi-intent inversion path does not run (the consult's
        armed guard): the line still answers once, through the main path's door."""
        self._plan(monkeypatch)
        sid = "s2209-pin6-armed"
        _arm(service, sid)
        returned = []
        real_multi = service._maybe_dispatch_multi_intent_inversion

        async def _multi(*a, **k):
            out = await real_multi(*a, **k)
            returned.append(out)
            return out

        monkeypatch.setattr(service, "_maybe_dispatch_multi_intent_inversion", _multi)
        _verdict(service, IntentCategory.QUERY, "get_information", self._MSG)
        result = await service.process_intent(message=self._MSG, session_id=sid, user_id=_USER)
        assert result.message.count("I don't see a milestone by that name.") == 1
        assert result.intent_data.get("multi_intent_inversion") is None
        assert all(out is None for out in returned)  # the path declined (or never ran)
        assert _pending(service, sid)["pending_action"][mp.REARMED_FLAG] is True
