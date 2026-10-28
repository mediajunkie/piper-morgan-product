"""#2076: the plain focus and standup replies say GitHub can't be read when it needs
reconnecting (a source that cannot be read is never shown as an empty one).

CXO's ruling (ADR-080 / #2033: code adds the fact, never the model). Served on alpha
with an OAuth-only account whose grant was revoked (binding STALE, no PAT):

- "what should I focus on today?" answered "**Today:** Nothing due today and nothing
  overdue. ..." and named no GitHub;
- "give me my standup" answered "... no observed activity in your connected tools. ..."
  and called the source that needs reconnecting a "connected tool".

Pins, stale vs bound:

1. Focus (``_handle_attention_query``, #1985's "**Today:**" shape): stale → the reply
   OPENS with the exact sentence, then the bound reply byte for byte; bound → unchanged.
2. Standup empty state (``_handle_standup_query``): stale → the exact invitation text,
   which is also the stored offer's question (#1665 / #1652); the standalone variant
   (sessionless / declined) leads with the same sentence; never "connected tools".
   Bound → the existing texts, quoted. Detection: the summary's own degraded record
   (the GitHub read failed ``stale_token``) first, the status service otherwise.
3. Standup interview re-entry (``StandupConversationHandler._generate_standup``, the
   quick bypass with nothing captured): stale → the sentence, then the one question.

The binding state is patched the way ``test_stale_binding_renderers_2072`` does; the
fixtures are the #1985 (b) and #1591 ones, imported, not copied.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

import services.integrations.integration_status_service as iss_mod
from services.domain.models import StandupSummary
from services.intent.intent_service import FOCUS_GITHUB_NEEDS_RECONNECTING_LEAD
from services.intent_service import standup_preferences as sp
from services.intent_service import verified_inference as vi
from services.shared_types import StandupConversationState
from services.standup.conversation_handler import StandupConversationHandler
from tests.unit.services.intent_service.test_contextual_query_handlers import (
    TestAttentionReplyShape1985b as _Shape1985b,
)
from tests.unit.services.intent_service.test_contextual_query_handlers import (  # noqa: F401
    intent_service,
)
from tests.unit.services.intent_service.test_standup_preference_capture_1591 import (  # noqa: F401
    _USER,
    _clean_transient_state,
    _pending,
    _standup_intent,
    mem_prefs,
    service,
)
from tests.unit.services.standup._fake_conversation_manager import (
    FakeStandupConversationManager,
)

# CXO's copy, verbatim (#2076).
FOCUS_SENTENCE = (
    "I can't read your GitHub right now (it needs reconnecting), so this leaves out "
    "your issues and pull requests."
)
STANDUP_STALE = (
    "I can't read your GitHub right now (it needs reconnecting), so I have no activity "
    "from it. Want to do a quick guided standup interview instead? (yes/no)"
)
STANDUP_SENTENCE = (
    "I can't read your GitHub right now (it needs reconnecting), so I have no activity " "from it."
)

# The bound (healthy) texts, quoted as they stood before #2076.
FOCUS_BOUND_EMPTY = (
    "**Today:**\n"
    "Nothing due today and nothing overdue.\n"
    "Nothing from your flagged todos, upcoming meetings or stale projects either."
)
STANDUP_BOUND_INVITE = (
    "I don't have anything to build your standup from yet — no observed activity in "
    "your connected tools. Want to do a quick guided standup interview instead? You "
    "tell me what happened and what's ahead, and I'll put it together. (yes/no)"
)
STANDUP_BOUND_STANDALONE = (
    "I don't have anything to build your standup from yet — no observed activity in "
    "your connected tools. Say 'my standup interview' any time to capture one "
    "interactively."
)
REENTRY_BOUND = (
    "I don't have anything to build your standup from — no observed activity and "
    "nothing captured yet, and I won't invent one. Let's capture it: what did you work "
    "on yesterday?"
)

_STALE_GITHUB_DETAIL = {
    "label": "your GitHub work items",
    "reason": "stale_token",
    "connector": "GitHub",
}


def _binding(state):
    """Patch only the binding state (#2072's idiom)."""
    return patch.object(iss_mod, "github_oauth_binding_state", new=AsyncMock(return_value=state))


def test_copy_constants_are_cxos_text():
    assert FOCUS_GITHUB_NEEDS_RECONNECTING_LEAD == FOCUS_SENTENCE
    assert sp.INVITE_EMPTY_LEAD_GITHUB_STALE == STANDUP_STALE
    assert sp.GITHUB_NEEDS_RECONNECTING_NO_ACTIVITY == STANDUP_SENTENCE
    # The bound lead is byte-identical to its pre-#2076 text.
    assert sp.INVITE_EMPTY_LEAD == STANDUP_BOUND_INVITE
    assert sp.EMPTY_STANDALONE == STANDUP_BOUND_STANDALONE
    # One yes/no question, last.
    assert STANDUP_STALE.count("?") == 1 and STANDUP_STALE.endswith("(yes/no)")
    for text in (FOCUS_SENTENCE, STANDUP_STALE, sp.EMPTY_STANDALONE_GITHUB_STALE):
        assert "connected tools" not in text
        assert "Settings" not in text  # no reconnect pointer in these sentences (CXO 3)


@pytest.mark.parametrize("state", ["stale", "unreachable"])
@pytest.mark.asyncio
async def test_helper_agrees_with_needs_reconnecting_of_get_status(state):
    """``github_needs_reconnecting`` is ``needs_reconnecting(get_status(...))`` without
    the credential probes: same answer for every binding state."""
    for s in (state, "bound", None):
        with (
            _binding(s),
            patch.object(
                iss_mod, "get_config_status", new=AsyncMock(return_value=("configured", "env"))
            ),
        ):
            status = await iss_mod.IntegrationStatusService().get_status(_USER, "github")
            assert await iss_mod.github_needs_reconnecting(_USER) is iss_mod.needs_reconnecting(
                status
            )
    assert await iss_mod.github_needs_reconnecting(None) is False


# ---------------------------------------------------------------------------
# 1. Focus ("**Today:**")
# ---------------------------------------------------------------------------


class TestFocusReplyDisclosesStaleGitHub2076:
    _shape = _Shape1985b()

    async def _focus(self, intent_service, state, due_today=(), overdue=()):
        with _binding(state) as bstate:
            result = await self._shape._run(intent_service, due_today, overdue)
        return result, bstate

    @pytest.mark.asyncio
    async def test_bound_reply_is_unchanged(self, intent_service):
        result, _ = await self._focus(intent_service, "bound")
        assert result.message == FOCUS_BOUND_EMPTY

    @pytest.mark.asyncio
    async def test_no_binding_reply_is_unchanged(self, intent_service):
        result, _ = await self._focus(intent_service, None)
        assert result.message == FOCUS_BOUND_EMPTY

    @pytest.mark.parametrize("state", ["stale", "unreachable"])
    @pytest.mark.asyncio
    async def test_stale_opens_with_the_sentence_then_the_bound_reply(self, intent_service, state):
        result, bstate = await self._focus(intent_service, state)
        assert result.message == f"{FOCUS_SENTENCE}\n\n{FOCUS_BOUND_EMPTY}"
        assert result.message.startswith(FOCUS_SENTENCE)
        # Asked for the principal, not the session.
        bstate.assert_awaited_with(_Shape1985b.USER)

    @pytest.mark.asyncio
    async def test_stale_over_a_non_empty_list_is_the_same_reply_after_the_sentence(
        self, intent_service
    ):
        from datetime import datetime, timedelta, timezone

        late = _Shape1985b._Todo(
            "revise the pr", due_date=datetime.now(timezone.utc) - timedelta(days=2)
        )
        bound, _ = await self._focus(intent_service, "bound", overdue=[late])
        stale, _ = await self._focus(intent_service, "stale", overdue=[late])
        assert FOCUS_SENTENCE not in bound.message
        assert stale.message == f"{FOCUS_SENTENCE}\n\n{bound.message}"


# ---------------------------------------------------------------------------
# 2. Standup empty state
# ---------------------------------------------------------------------------


async def _standup_turn(service, sid, summary, state):
    with (
        patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=summary),
        ),
        _binding(state) as bstate,
    ):
        result = await service._handle_standup_query(
            _standup_intent(), "wf-2076", session_id=sid, user_id=_USER
        )
    return result, bstate


class TestStandupEmptyStateDisclosesStaleGitHub2076:
    @pytest.mark.asyncio
    async def test_stale_from_the_summarys_degraded_record(self, service):
        """The served shape: the GitHub read failed STALE_TOKEN (b1fbfa3da1), recorded on
        the summary. That record answers; the status service is not asked."""
        summary = StandupSummary(
            degraded_sources=["your GitHub work items"], degraded_details=[_STALE_GITHUB_DETAIL]
        )
        result, bstate = await _standup_turn(service, "s-2076-a", summary, None)
        assert result.message == STANDUP_STALE
        assert "connected tools" not in result.message
        offer = _pending(service, "s-2076-a")
        assert offer["question"] == STANDUP_STALE  # #1665: the stored ask is what was shown
        assert offer["decline_message"] == sp.INVITE_DECLINE_MESSAGE_NO_REPORT  # #2020
        assert result.intent_data["standup_interview_invitation_pending"] is True  # #1652
        bstate.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_stale_from_the_status_service_when_the_summary_has_no_record(self, service):
        result, bstate = await _standup_turn(service, "s-2076-b", StandupSummary(), "stale")
        assert result.message == STANDUP_STALE
        assert _pending(service, "s-2076-b")["question"] == STANDUP_STALE
        bstate.assert_awaited_with(_USER)

    @pytest.mark.asyncio
    async def test_bound_keeps_the_existing_invitation(self, service):
        result, _ = await _standup_turn(service, "s-2076-c", StandupSummary(), "bound")
        assert result.message == STANDUP_BOUND_INVITE
        assert _pending(service, "s-2076-c")["question"] == STANDUP_BOUND_INVITE

    @pytest.mark.asyncio
    async def test_github_failed_another_way_is_not_called_reconnecting(self, service):
        """An unreachable read with a healthy binding is not "needs reconnecting".
        #2182: nor is it "no observed activity"; the #1889 line says the read failed."""
        summary = StandupSummary(
            degraded_sources=["your GitHub work items"],
            degraded_details=[{**_STALE_GITHUB_DETAIL, "reason": "unreachable"}],
        )
        result, _ = await _standup_turn(service, "s-2076-d", summary, "bound")
        assert result.message.startswith("I couldn't reach your GitHub work items just now.")
        assert "reconnecting" not in result.message
        assert "no observed activity" not in result.message

    @pytest.mark.asyncio
    async def test_sessionless_stale_keeps_the_standalone_shape_with_the_sentence(self, service):
        result, _ = await _standup_turn(service, None, StandupSummary(), "stale")
        assert result.message == (
            f"{STANDUP_SENTENCE} Say 'my standup interview' any time to capture one "
            "interactively."
        )
        assert "connected tools" not in result.message
        assert "?" not in result.message

    @pytest.mark.asyncio
    async def test_sessionless_bound_keeps_the_existing_standalone(self, service):
        result, _ = await _standup_turn(service, None, StandupSummary(), "bound")
        assert result.message == STANDUP_BOUND_STANDALONE

    @pytest.mark.asyncio
    async def test_declined_stale_is_standalone_and_names_github(self, service):
        sid = "s-2076-e"
        vi.mark_declined(sid, sp.STANDUP_MODE_KEY)
        result, _ = await _standup_turn(service, sid, StandupSummary(), "stale")
        assert result.message == sp.EMPTY_STANDALONE_GITHUB_STALE
        assert result.message.startswith(STANDUP_SENTENCE)
        assert _pending(service, sid) is None


# ---------------------------------------------------------------------------
# 3. Standup interview re-entry (quick bypass, nothing captured)
# ---------------------------------------------------------------------------


class TestStandupReentryDisclosesStaleGitHub2076:
    async def _quick(self, state):
        handler = StandupConversationHandler(conversation_manager=FakeStandupConversationManager())
        conversation = await handler.manager.create_conversation("s-2076-q", _USER)
        with _binding(state):
            return await handler.handle_turn(conversation, "quick standup")

    @pytest.mark.asyncio
    async def test_stale_names_github_then_the_one_question(self):
        response = await self._quick("stale")
        assert response.message == (
            f"{STANDUP_SENTENCE} Let's capture it: what did you work on yesterday?"
        )
        assert response.message.count("?") == 1
        assert response.state == StandupConversationState.GATHERING_YESTERDAY

    @pytest.mark.asyncio
    async def test_bound_keeps_the_existing_reentry(self):
        response = await self._quick("bound")
        assert response.message == REENTRY_BOUND
        assert response.state == StandupConversationState.GATHERING_YESTERDAY
