"""#1511 MVP slice — pure disambiguation: "two standups wear one name."

The interactive standup interview (#585, StandupConversationHandler) exists and
works, but is unaddressable from chat: the derived report (#1269/#1289,
StandupAssembler via _handle_standup_query) claims all standup phrasings, and
the only route to the interview is the literal ``/standup`` command.

The sanctioned shape (#1431 pattern, routing moratorium): a token branch INSIDE
the already-claiming handler — when the standup claim fires AND the message
carries an explicit interview token (``\\binterview\\b`` or ``\\binteractive\\b``),
dispatch the EXISTING interview flow instead of the report. No pre-classifier
pattern changes, no prompt changes, no behavior change to either mode.

Layer honesty (m-43): these tests exercise the deterministic claim
(_is_standup_query → _handle_standup_query) and the action-dispatch rail entry
(show_standup/get_standup → same handler). The bare phrase "standup interview"
is NOT deterministically claimed (no _is_standup_query cue matches, by design —
widening the claim is a routing change and off-limits under the moratorium); it
reaches the branch only if the LLM classifier yields show_standup/get_standup.
The copy therefore teaches a phrase the deterministic claim DOES cover:
"my standup interview".

Escape pin: the standup-hijack history (#1529) makes escape regression the one
to fear — a branch-entered interview must honor the same escape tiers as a
/standup-entered one. Pinned at the registry seam with the REAL
StandupProcessAdapter + REAL StandupConversationHandler over the fake manager.
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory

REPORT_TEACHING_LINE = "Want the guided version instead? Say 'my standup interview'."
# #1591 updated the taught report phrase: the generic 'give me my standup' now
# honors a stored standup_mode=interview preference (redirects to the
# interview), so the interview's escape line must carry the explicit report
# token to stay a working escape. Still claimed by the 'my standup' cue.
INTERVIEW_TEACHING_LINE = "Want the quick report instead? Say 'my standup report'."


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """IntentService with heavy deps patched out (mirrors cohort handler tests)."""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


@pytest.fixture(autouse=True)
def _clean_1591_transient_state():
    """#1591 wired preference capture into the handler these tests drive; its
    transient module state (mode tally, session decline memory) must not leak
    between tests."""
    from services.intent_service import standup_preferences as sp
    from services.intent_service import verified_inference as vi

    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()
    yield
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()


@pytest.fixture(autouse=True)
def _no_stored_standup_mode(monkeypatch):
    """Pin the rail's store read to a miss at its persistence seam — these
    #1511 tests assert the NO-stored-preference behavior; the real seam would
    try the DB. (#1591's own tests exercise the stored paths.)"""

    async def _load(user_id):
        return {}

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)


def _standup_intent(message: str, action: str = "get_standup") -> Intent:
    return Intent(
        category=IntentCategory.STATUS,
        action=action,
        original_message=message,
        confidence=1.0,
    )


def _fake_summary():
    summary = MagicMock()
    # #1591: the handler now branches on is_empty() (PPM's empty-case rule);
    # these tests exercise the WITH-data report shape.
    summary.is_empty.return_value = False
    summary.to_prose.return_value = "Here's your derived standup."
    summary.to_dict.return_value = {"sections": []}
    return summary


# ---------------------------------------------------------------------------
# 1. The token branch — interview token dispatches the EXISTING interview flow
# ---------------------------------------------------------------------------


class TestInterviewTokenBranch:
    @pytest.mark.asyncio
    async def test_interview_token_dispatches_interactive_flow(self, intent_service):
        """FAILING-FIRST core: 'my standup interview' (claimed by
        _is_standup_query via the 'my standup' cue) must enter the interview,
        not the report."""
        sentinel = IntentProcessingResult(
            success=True,
            message="interview started",
            intent_data={"category": "execution", "action": "standup_started", "confidence": 1.0},
        )
        intent_service._start_standup_conversation = AsyncMock(return_value=sentinel)
        with patch("services.standup.assembler.build_user_standup_summary") as assembler:
            result = await intent_service._handle_standup_query(
                _standup_intent("my standup interview"),
                "wf-1",
                session_id="sess-1",
                user_id="user-1",
            )
        intent_service._start_standup_conversation.assert_awaited_once_with("user-1", "sess-1")
        assembler.assert_not_called()  # the report never fires
        assert result is sentinel

    @pytest.mark.asyncio
    async def test_interactive_token_dispatches_interactive_flow(self, intent_service):
        """'interactive' is the second sanctioned token; rail-shaped intent
        (show_standup from the LLM classifier) reaches the same branch."""
        sentinel = IntentProcessingResult(
            success=True,
            message="interview started",
            intent_data={"category": "execution", "action": "standup_started", "confidence": 1.0},
        )
        intent_service._start_standup_conversation = AsyncMock(return_value=sentinel)
        with patch("services.standup.assembler.build_user_standup_summary") as assembler:
            result = await intent_service._handle_standup_query(
                _standup_intent("interactive standup", action="show_standup"),
                "wf-2",
                session_id="sess-2",
                user_id="user-2",
            )
        intent_service._start_standup_conversation.assert_awaited_once_with("user-2", "sess-2")
        assembler.assert_not_called()
        assert result is sentinel

    @pytest.mark.asyncio
    async def test_token_requires_word_boundary(self, intent_service):
        """'interviewing candidates for standup notes' style substrings must not
        misfire — but a bounded token anywhere in a claimed phrasing does."""
        intent_service._start_standup_conversation = AsyncMock()
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_fake_summary()),
        ):
            await intent_service._handle_standup_query(
                _standup_intent("my standup about the interviewer role"),
                "wf-3",
                session_id="sess-3",
                user_id="user-3",
            )
        # "interviewer" is not \binterview\b — report fires, no interview dispatch
        intent_service._start_standup_conversation.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_session_id_falls_through_to_report(self, intent_service):
        """Honest deterministic fallback: without a session there is no
        conversation to key the interview to — serve the report (whose teaching
        line still names the interview)."""
        intent_service._start_standup_conversation = AsyncMock()
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_fake_summary()),
        ):
            result = await intent_service._handle_standup_query(
                _standup_intent("my standup interview"),
                "wf-4",
                session_id=None,
                user_id="user-4",
            )
        intent_service._start_standup_conversation.assert_not_called()
        assert result.success is True
        assert "Good morning!" in result.message


# ---------------------------------------------------------------------------
# 2. Canary — the report mode is UNCHANGED for non-token phrasings
# ---------------------------------------------------------------------------


class TestReportCanary:
    @pytest.mark.asyncio
    async def test_plain_standup_query_still_reports(self, intent_service):
        intent_service._start_standup_conversation = AsyncMock()
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_fake_summary()),
        ) as assembler:
            result = await intent_service._handle_standup_query(
                _standup_intent("give me my standup"),
                "wf-5",
                session_id="sess-5",
                user_id="user-5",
            )
        assembler.assert_awaited_once_with("user-5")
        intent_service._start_standup_conversation.assert_not_called()
        assert result.success is True
        assert result.message.startswith("Good morning!")
        assert "Here's your derived standup." in result.message
        assert result.intent_data["context"]["standup_data"] == {"sections": []}

    def test_deterministic_claim_unchanged(self):
        """_is_standup_query is untouched (moratorium): the taught phrase is
        claimed via the existing 'my standup' cue; the bare phrase is NOT
        claimed (it rides the LLM rail only) — documented, not widened."""
        assert IntentService._is_standup_query("my standup interview")
        assert IntentService._is_standup_query("give me my standup")
        assert not IntentService._is_standup_query("standup interview")
        assert not IntentService._is_standup_query("/standup")


# ---------------------------------------------------------------------------
# 3. Copy — each mode names the other, once, deterministically
# ---------------------------------------------------------------------------


class TestDisambiguationCopy:
    @pytest.mark.asyncio
    async def test_report_teaches_interview_exists_once(self, intent_service):
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_fake_summary()),
        ):
            result = await intent_service._handle_standup_query(
                _standup_intent("give me my standup"),
                "wf-6",
                session_id="sess-6",
                user_id="user-6",
            )
        assert result.message.count(REPORT_TEACHING_LINE) == 1

    @pytest.mark.asyncio
    async def test_report_error_path_has_no_teaching_line(self, intent_service):
        """The teaching line rides the successful report only — an error
        message teaching a second mode would be noise (#1423 honesty intact)."""
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            side_effect=RuntimeError("assembler exploded"),
        ):
            result = await intent_service._handle_standup_query(
                _standup_intent("give me my standup"),
                "wf-7",
                session_id="sess-7",
                user_id="user-7",
            )
        assert result.success is False
        assert REPORT_TEACHING_LINE not in result.message

    @pytest.mark.asyncio
    async def test_interview_opening_names_report(self, intent_service):
        """The interview's opening (new conversation) carries the reciprocal
        teaching line — for BOTH entries (/standup and the token branch), since
        both go through _start_standup_conversation."""
        fake_manager = MagicMock()
        fake_manager.get_conversation_by_session = AsyncMock(return_value=None)
        fake_handler = MagicMock()
        opening = MagicMock()
        opening.message = "Good morning! Ready for your standup?"
        opening.state = MagicMock(value="initiated")
        opening.requires_input = True
        opening.suggestions = ["Yes, let's do it"]
        fake_handler.start_conversation = AsyncMock(return_value=opening)
        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(fake_manager, fake_handler),
        ):
            result = await intent_service._start_standup_conversation("user-8", "sess-8")
        assert result.success is True
        assert result.message.startswith("Good morning! Ready for your standup?")
        assert result.message.count(INTERVIEW_TEACHING_LINE) == 1

    @pytest.mark.asyncio
    async def test_in_progress_offer_has_no_teaching_line(self, intent_service):
        """Only the OPENING teaches; the continue-or-restart offer for an
        already-active conversation is unchanged."""
        from services.shared_types import StandupConversationState

        existing = MagicMock()
        existing.id = "conv-1"
        existing.state = StandupConversationState.GATHERING_PREFERENCES
        fake_manager = MagicMock()
        fake_manager.get_conversation_by_session = AsyncMock(return_value=existing)
        fake_handler = MagicMock()
        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(fake_manager, fake_handler),
        ):
            result = await intent_service._start_standup_conversation("user-9", "sess-9")
        assert INTERVIEW_TEACHING_LINE not in result.message


# ---------------------------------------------------------------------------
# 4. Threading — both claiming rails hand the branch a session_id
# ---------------------------------------------------------------------------


class TestSessionThreading:
    def test_deterministic_claim_site_threads_session_id(self):
        """The #1269 pre-classification claim passes session_id through to the
        handler (source-level pin, same style as the #585 routing tests)."""
        import inspect

        source = inspect.getsource(IntentService._process_intent_internal)
        call = re.search(r"_handle_standup_query\((.*?)\)", source, re.DOTALL)
        assert call, "deterministic claim site must dispatch _handle_standup_query"
        assert "session_id" in call.group(1), (
            "the deterministic standup claim must thread session_id so the "
            "interview branch can key the conversation"
        )

    @pytest.mark.asyncio
    async def test_rail_entry_threads_session_and_user(self):
        """The show_standup/get_standup dispatch-rail entry point calls the
        handler as (intent, workflow_id, session_id, user_id)."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        workflows = get_action_workflows()
        assert "show_standup" in workflows and "get_standup" in workflows
        entry = workflows["show_standup"]
        fake_service = MagicMock()
        fake_service._handle_standup_query = AsyncMock(return_value="ok")
        intent = _standup_intent("standup interview", action="show_standup")
        ctx = {"intent_service": fake_service, "intent": intent, "workflow_id": "wf-10"}
        out = await entry.entry_point("sess-10", "user-10", ctx)
        assert out == "ok"
        fake_service._handle_standup_query.assert_awaited_once_with(
            intent, "wf-10", "sess-10", "user-10"
        )


# ---------------------------------------------------------------------------
# 5. Escape pin (#1529) — a branch-entered interview honors the escape tiers
# ---------------------------------------------------------------------------


@pytest.fixture
def real_interview_components():
    """REAL StandupConversationHandler over the in-memory fake manager —
    the same objects serve both the entry (via the token branch) and the
    registry adapter, exactly as the production singletons do."""
    from services.standup.conversation_handler import StandupConversationHandler
    from tests.unit.services.standup._fake_conversation_manager import (
        FakeStandupConversationManager,
    )

    manager = FakeStandupConversationManager()
    handler = StandupConversationHandler(conversation_manager=manager)
    return manager, handler


class TestBranchEnteredInterviewEscape:
    async def _enter_via_branch(self, intent_service, components, session_id, user_id):
        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=components,
        ):
            return await intent_service._handle_standup_query(
                _standup_intent("my standup interview"),
                "wf-esc",
                session_id=session_id,
                user_id=user_id,
            )

    @pytest.mark.asyncio
    async def test_exit_tier_end_standup_closes_branch_entered_interview(
        self, intent_service, real_interview_components
    ):
        """Enter via the token branch, then 'end standup' at the registry seam:
        consumed deterministically, flow CLOSED, never transcribed (#1529)."""
        from services.process.adapters import StandupProcessAdapter
        from services.process.registry import ProcessRegistry
        from services.shared_types import StandupConversationState

        manager, handler = real_interview_components
        result = await self._enter_via_branch(
            intent_service, (manager, handler), "sess-esc-1", "user-esc-1"
        )
        assert result.success is True
        assert result.intent_data["action"] == "standup_started"
        conversation = await manager.get_conversation_by_session("sess-esc-1")
        assert conversation is not None, "branch entry must create the session-keyed conversation"

        adapter = StandupProcessAdapter()
        adapter._manager, adapter._handler = manager, handler
        registry = ProcessRegistry()
        registry.register(adapter)

        escape = await registry.check_active_processes("user-esc-1", "sess-esc-1", "end standup")
        assert escape.handled is True
        assert escape.escaped is True
        closed = await manager.get_conversation(conversation.id)
        assert closed.state == StandupConversationState.ABANDONED
        # Terminal: the flow no longer claims subsequent turns
        assert await adapter.check_active("user-esc-1", "sess-esc-1") is False

    @pytest.mark.asyncio
    async def test_refusal_tier_honored_from_branch_entered_interview(
        self, intent_service, real_interview_components
    ):
        """PM's verbatim refusal shape (#1529) exits a branch-entered interview
        instead of being transcribed as a standup answer."""
        from services.process.adapters import StandupProcessAdapter
        from services.process.registry import ProcessRegistry

        manager, handler = real_interview_components
        await self._enter_via_branch(
            intent_service, (manager, handler), "sess-esc-2", "user-esc-2"
        )
        adapter = StandupProcessAdapter()
        adapter._manager, adapter._handler = manager, handler
        registry = ProcessRegistry()
        registry.register(adapter)

        escape = await registry.check_active_processes(
            "user-esc-2", "sess-esc-2", "i am not doing the standup right now"
        )
        assert escape.escaped is True
        assert await adapter.check_active("user-esc-2", "sess-esc-2") is False
