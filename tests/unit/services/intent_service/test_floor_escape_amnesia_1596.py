"""#1596 — floor amnesia after a guided-flow escape (split out of #1529).

PM's 2026-08-08 hostage transcript ended: "User escaped only via 'none' →
floor (which then had amnesia)". #1529 fixed the escape itself; this pins
what the floor KNOWS when it catches the fall-through.

DIAGNOSIS (verify-first, 2026-09-12, driven e2e through the real
process_intent — see the session log for the probe transcripts):

- The HISTORY half of the filed amnesia was already fixed by #1394
  (acf26bbec, 2026-08-08): prior turns reach the floor on the authenticated
  path, including through the escape arrangement. No test drove that e2e
  through a real escape until now — pinned GREEN here so it stays fixed.
- Two halves were still RED on 2026-09-12, both fixed with this file:

  1. THE FLOOR'S READ (wrong-empty): the classifier rewrites vague /
     low-confidence turns to CONVERSATION/clarification_needed — exactly
     where post-escape fragments like PM's verbatim 'none' land — and
     ContextAssembler.gather_context had a deliberate `pass` for
     CONVERSATION ("minimal context for greetings", a rationale keyed to a
     caller that no longer exists: pure greetings take the canned canonical
     lane and never reach the assembler). Those turns floored with
     domain_context ≈ {current_time}: no todos, no projects, no GitHub —
     while the structurally identical UNKNOWN fall-through got the #960
     baseline. CONVERSATION now falls into the #960 else-branch.

  2. THE ESCAPE'S STATE HANDOFF: on the escape turn itself, the exit
     acknowledgment (off_topic_prefix) is glued onto the reply AFTER the
     floor composes, and the current turn is excluded from history — so the
     floor composed with the flow's open question visible and nothing
     saying the flow closed. It could re-open the interview the user just
     escaped, contradicting the prepended exit copy.
     _check_active_guided_process now also returns WHICH flow the
     fall-through left; the classification seam stamps it onto
     intent.context["guided_flow_escape"]; the floor doors merge it into
     domain_context; _format_domain_context renders a rule-stating
     directive (#1655-clean: no sample reply sentences).

Acceptance-contract note (#1739): this change arms nothing and consumes
nothing — no acceptance detection is added, evaluate_acceptance is not
involved, and the escape/pop interplay (§5a/§5b arm survival) is untouched.
The stamped note is turn-scoped by construction (a per-turn local, stamped
onto the freshly classified intent), pinned below.
"""

import json
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from services.intent_service import conversational_floor as cf
from services.intent_service.context_assembler import ContextAssembler
from services.process.registry import ProcessRegistry, ProcessType
from services.shared_types import StandupConversationState

# A refusal naming the flow + a residual no deterministic surface claims
# (probed: pre_classify → None, detect_multiple_intents → no claim), so the
# fall-through takes the REAL vague-rewrite lane the way PM's 'none' did.
ESCAPE_WITH_VAGUE_RESIDUAL = (
    "i am not doing the standup right now. what was that thing you mentioned"
)
POST_ESCAPE_FRAGMENT = "none"  # PM's verbatim amnesia beat

_USER = "3f7b8a52-1596-4b00-9e00-000000001596"
_SESSION = "sess-1596-amnesia"

_BASELINE_SENTINEL = {"sentinel_1596": True, "pending_todos": [{"text": "sentinel row"}]}


async def _fake_baseline_gather(self, user_id=None):
    """Stands in for _gather_status_priority_context: proves WHICH branch of
    gather_context consulted the #960 baseline gatherer (layer note, m-43:
    these tests pin the consult, not the gatherer's own DB/GitHub reads)."""
    return dict(_BASELINE_SENTINEL)


# ---------------------------------------------------------------------------
# Unit: the floor's read — CONVERSATION gathers the #960 baseline
# ---------------------------------------------------------------------------


class TestConversationCategoryGathersBaseline:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "action",
        ["clarification_needed", "chitchat", "farewell", "greeting", None],
    )
    async def test_conversation_consults_the_960_baseline(self, monkeypatch, action):
        """RED pre-fix: the CONVERSATION `pass` branch skipped the baseline
        gather entirely, so a clarification turn floored with
        domain_context ≈ {current_time}."""
        monkeypatch.setattr(
            ContextAssembler, "_gather_status_priority_context", _fake_baseline_gather
        )
        ctx = await ContextAssembler().gather_context(
            intent_category="CONVERSATION",
            user_id=_USER,
            session_id=_SESSION,
            intent_action=action,
        )
        assert ctx.get("sentinel_1596") is True, (
            f"CONVERSATION/{action} floor turn skipped the #960 baseline gather "
            f"— the wrong-empty half of the #1596 amnesia. Keys: {list(ctx)}"
        )

    async def test_unknown_baseline_unchanged(self, monkeypatch):
        """Control: UNKNOWN keeps the #960 behavior it always had."""
        monkeypatch.setattr(
            ContextAssembler, "_gather_status_priority_context", _fake_baseline_gather
        )
        ctx = await ContextAssembler().gather_context(
            intent_category="UNKNOWN", user_id=_USER, session_id=_SESSION
        )
        assert ctx.get("sentinel_1596") is True


# ---------------------------------------------------------------------------
# Unit: the renderer — the escape note is a rule-stating context line
# ---------------------------------------------------------------------------


class TestEscapeNoteRendering:
    def test_note_renders_naming_the_flow(self):
        block = cf.ConversationalFloor()._format_domain_context(
            {"guided_flow_escape": {"process_type": "standup"}}
        )
        assert "GUIDED FLOW ENDED THIS TURN" in block
        assert "standup" in block
        # #1655 discipline: a rule, not a sample reply the model could copy.
        assert "do not re-open" in block

    def test_note_tolerates_missing_process_type(self):
        block = cf.ConversationalFloor()._format_domain_context({"guided_flow_escape": {}})
        assert "GUIDED FLOW ENDED THIS TURN" in block
        assert "guided flow" in block

    def test_no_note_no_line(self):
        block = cf.ConversationalFloor()._format_domain_context({"current_time": "09:00 AM"})
        assert "GUIDED FLOW ENDED" not in block


# ---------------------------------------------------------------------------
# End-to-end: the issue's arrangement through the REAL process_intent
# ---------------------------------------------------------------------------


class _LowConfidenceLLM:
    """Whatever reaches the LLM classifier draws a low-confidence unknown —
    which the REAL classifier rewrite turns into CONVERSATION/
    clarification_needed (classifier.py's vague/low-confidence seam), the
    lane PM's post-escape fragments actually took."""

    async def complete(self, **kwargs):
        return json.dumps(
            {
                "category": "unknown",
                "action": "unknown",
                "confidence": 0.2,
                "reasoning": "unclear fragment",
            }
        )


def _fake_components():
    from services.standup.conversation_handler import StandupConversationHandler
    from tests.unit.services.standup._fake_conversation_manager import (
        FakeStandupConversationManager,
    )

    manager = FakeStandupConversationManager()
    handler = StandupConversationHandler(conversation_manager=manager)
    return manager, handler


@pytest.fixture
def captured_floor(monkeypatch):
    captured = []

    async def fake_respond(self, ctx):
        captured.append(ctx)
        return cf.FloorResponse(message="(stubbed floor answer)")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", fake_respond)
    return captured


@pytest.fixture
async def live_service(monkeypatch):
    """Real IntentService + real ProcessRegistry + real StandupProcessAdapter
    + REAL IntentClassifier over a low-confidence LLM (the rewrite lane runs
    for real). Baseline gatherer sentinel-stubbed (layer note above)."""
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows
    from services.process.adapters import StandupProcessAdapter

    register_default_workflows()
    manager, handler = _fake_components()

    adapter = StandupProcessAdapter()
    adapter._manager, adapter._handler = manager, handler

    ProcessRegistry.reset_instance()
    ProcessRegistry.get_instance().register(adapter)

    monkeypatch.setattr(ContextAssembler, "_gather_status_priority_context", _fake_baseline_gather)

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_LowConfidenceLLM())
            service = IntentService(intent_classifier=clf)

    yield service, manager

    ProcessRegistry.reset_instance()


class TestEscapeTurnFloorKnowsTheEscape:
    """The escape turn itself: refusal + vague residual falls through to the
    floor. The floor must know a flow just ended (RED pre-fix) and carry the
    user-data baseline (RED pre-fix) and the prior turns (GREEN — the #1394
    half, pinned e2e through a real escape for the first time)."""

    pytestmark = pytest.mark.asyncio

    async def _run_escape_turn(self, service, manager):
        from services.intent_service.conversation_context import clear_context

        clear_context(_SESSION, _USER)
        conv = await manager.create_conversation(session_id=_SESSION, user_id=_USER)
        conv.state = StandupConversationState.GATHERING_YESTERDAY
        conv.updated_at = datetime.now(timezone.utc)

        # T0: a REAL flow answer through the real pipeline (records the turn
        # the way the live path does — no hand-seeded history).
        await service.process_intent(
            message="shipped the v53 cut", session_id=_SESSION, user_id=_USER
        )
        assert conv.state == StandupConversationState.GATHERING_TODAY

        # T1: the escape (refusal naming the flow + unclaimed residual).
        result = await service.process_intent(
            message=ESCAPE_WITH_VAGUE_RESIDUAL, session_id=_SESSION, user_id=_USER
        )
        return conv, result

    async def test_escape_still_works_and_prefix_rides(self, live_service, captured_floor):
        from services.process.escape import format_refusal_prefix

        service, manager = live_service
        conv, result = await self._run_escape_turn(service, manager)
        assert conv.state == StandupConversationState.ABANDONED
        assert result.message.startswith(format_refusal_prefix(ProcessType.STANDUP))

    async def test_floor_catches_the_fallthrough_as_clarification(
        self, live_service, captured_floor
    ):
        service, manager = live_service
        await self._run_escape_turn(service, manager)
        assert captured_floor, "the fall-through never reached the floor"
        fc = captured_floor[-1]
        assert fc.user_message == ESCAPE_WITH_VAGUE_RESIDUAL
        assert fc.intent_category == "CONVERSATION"
        assert fc.intent_action == "clarification_needed"

    async def test_floor_gets_the_escape_note(self, live_service, captured_floor):
        """RED pre-fix: nothing told the floor a flow ended this turn."""
        service, manager = live_service
        await self._run_escape_turn(service, manager)
        fc = captured_floor[-1]
        note = (fc.domain_context or {}).get("guided_flow_escape")
        assert note == {"process_type": "standup"}, (
            "the escape's state handoff dropped the flow context — the floor "
            f"composes as if the interview were still open. domain_context "
            f"keys: {list(fc.domain_context or {})}"
        )
        prompt = cf.ConversationalFloor()._build_prompt(fc)
        assert "GUIDED FLOW ENDED THIS TURN" in prompt
        assert "standup" in prompt

    async def test_floor_gets_the_user_data_baseline(self, live_service, captured_floor):
        """RED pre-fix: CONVERSATION floored with ≈{current_time} only."""
        service, manager = live_service
        await self._run_escape_turn(service, manager)
        fc = captured_floor[-1]
        assert (fc.domain_context or {}).get("sentinel_1596") is True

    async def test_history_reaches_the_floor_through_a_real_escape(
        self, live_service, captured_floor
    ):
        """GREEN pin of the #1394 half (fixed 2026-08-08, three days before
        #1596 was filed) — no prior test drove it through a real escape."""
        service, manager = live_service
        await self._run_escape_turn(service, manager)
        fc = captured_floor[-1]
        assert {"role": "user", "content": "shipped the v53 cut"} in fc.conversation_history


class TestPostEscapeFragmentFloor:
    """PM's verbatim amnesia beat: 'none' on the turn AFTER the escape."""

    pytestmark = pytest.mark.asyncio

    async def _run_sequence(self, service, manager):
        from services.intent_service.conversation_context import clear_context

        clear_context(_SESSION, _USER)
        conv = await manager.create_conversation(session_id=_SESSION, user_id=_USER)
        conv.state = StandupConversationState.GATHERING_TODAY
        conv.updated_at = datetime.now(timezone.utc)

        await service.process_intent(
            message=ESCAPE_WITH_VAGUE_RESIDUAL, session_id=_SESSION, user_id=_USER
        )
        result = await service.process_intent(
            message=POST_ESCAPE_FRAGMENT, session_id=_SESSION, user_id=_USER
        )
        return result

    async def test_none_floors_with_the_baseline(self, live_service, captured_floor):
        """RED pre-fix: the wrong-empty half on the verbatim beat."""
        service, manager = live_service
        await self._run_sequence(service, manager)
        fc = captured_floor[-1]
        assert fc.user_message == POST_ESCAPE_FRAGMENT
        assert fc.intent_category == "CONVERSATION"
        assert (fc.domain_context or {}).get("sentinel_1596") is True

    async def test_none_sees_the_escape_exchange_in_history(self, live_service, captured_floor):
        """GREEN pin (#1394 half): the floor's history carries the escape
        exchange, exit copy included."""
        service, manager = live_service
        await self._run_sequence(service, manager)
        fc = captured_floor[-1]
        user_turns = [t["content"] for t in fc.conversation_history if t["role"] == "user"]
        assistant_turns = [
            t["content"] for t in fc.conversation_history if t["role"] == "assistant"
        ]
        assert ESCAPE_WITH_VAGUE_RESIDUAL in user_turns
        assert any("standup" in t.lower() for t in assistant_turns)

    async def test_escape_note_is_turn_scoped_not_sticky(self, live_service, captured_floor):
        """The note names an event of THIS turn; it must not leak onto the
        next turn's floor context (stamped from a per-turn local onto the
        freshly classified intent — pinned so a refactor can't make it
        session-sticky)."""
        service, manager = live_service
        await self._run_sequence(service, manager)
        fc = captured_floor[-1]
        assert fc.user_message == POST_ESCAPE_FRAGMENT
        assert "guided_flow_escape" not in (fc.domain_context or {})
