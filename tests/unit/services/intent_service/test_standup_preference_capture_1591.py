"""#1591 (Production/PUB half) — standup preference capture + interview
invitation, wired onto the #1510 verified-inference rail as a CONSUMER.

The governing spec (issue #1591 + comments), each pinned by a named test:

- CXO property 1 — report first and complete   → TestCxoPropertyOneReportFirst
- CXO property 2 — invitation after, cheap to
  decline                                      → TestCxoPropertyTwoInvitationAfterCheapDecline
- CXO property 3 — declining changes nothing
  else                                         → TestCxoPropertyThreeDecliningChangesNothing
- PPM's empty rule — nothing to demonstrate →
  fail honestly, invitation IS the first move  → TestPpmEmptyExceptionInvitationFirst
- Accept → the EXISTING #585 interview starts  → TestAcceptStartsInterview
- Low-confidence signal → the RAIL's read-back
  is armed; yes stores source=user_verified    → TestLowConfidenceReadBack
- Stored preference → honored without
  re-inference (one store, the rail's)         → TestStoredPreferenceHonored
- High confidence → rail auto-apply semantics  → TestAutoApplySemantics
- The invitation workflow entry (#1557 pin)    → TestStandupInterviewWorkflowEntry

Layer honesty (m-43): handler-level tests drive the REAL
``IntentService._handle_standup_query`` (the #1511 idiom — assembler patched
at its import seam, is_empty explicit); end-to-end classes drive the REAL
``process_intent`` mocked ONLY at the LLM boundary (explosive — every
accept/decline turn must resolve deterministically at the pending-offer seam,
which is also the #1529 ordering pin: the offer is consumed before any
classification or resume check could see the turn) and at the persistence
seam (in-memory users.preferences double; the real-Postgres half lives in
``tests/integration/test_standup_preference_capture_1591.py``).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service import standup_preferences as sp
from services.intent_service import verified_inference as vi
from services.intent_service.classifier import IntentClassifier
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1591-4b00-9e00-000000001591"

TEACHING_LINE = "Want the guided version instead? Say 'my standup interview'."
PROSE = "Here's your derived standup."


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM (forbidden on
    offer turns — the #1510/#1529 determinism pin)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1591 offer turns must resolve "
            "deterministically at the pending-offer seam"
        )


@pytest.fixture(autouse=True)
def _clean_transient_state():
    """The tally and the session decline memory are process-lifetime module
    state (transient evidence, not preference stores) — never shared between
    tests."""
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()
    yield
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double at the ONE persistence seam
    (collaboration_gate) — the rail imports the seam at call time, so
    patching the module attributes covers every path (the #1510 idiom)."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if str(user_id) not in store:
            return False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


@pytest.fixture
def service(mem_prefs):
    """IntentService with heavy deps patched out and an explosive LLM — used
    both for direct handler calls and REAL process_intent turns. The workflow
    registry is populated up front (idempotent — in production the container
    init does this; the acceptance seam dispatches from it)."""
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _standup_intent(message: str = "give me my standup") -> Intent:
    return Intent(
        category=IntentCategory.STATUS,
        action="get_standup",
        original_message=message,
        confidence=1.0,
    )


def _summary(empty: bool = False):
    summary = MagicMock()
    summary.is_empty.return_value = empty
    summary.to_prose.return_value = PROSE
    summary.to_dict.return_value = {"sections": []}
    return summary


async def _report_turn(service, sid, user_id=_USER, message="give me my standup", empty=False):
    """One handler turn with the assembler patched at its import seam."""
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary(empty=empty)),
    ):
        return await service._handle_standup_query(
            _standup_intent(message), "wf-1591", session_id=sid, user_id=user_id
        )


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


# ---------------------------------------------------------------------------
# CXO property 1 — report first and complete
# ---------------------------------------------------------------------------


class TestCxoPropertyOneReportFirst:
    pytestmark = pytest.mark.asyncio

    async def test_report_renders_first_complete_and_unconditional(self, service):
        """CXO's binary predicate: 'did any user-visible prompt precede the
        report's content?' — must be no. The complete prose renders before
        any ask, and the full standup_data payload rides the result."""
        result = await _report_turn(service, "sess-p1")
        assert result.success is True
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert result.intent_data["context"]["standup_data"] == {"sections": []}

    async def test_invitation_comes_after_the_complete_report(self, service):
        """Property 1 + 2 ordering, pinned positionally: the invitation text
        appears strictly AFTER the report prose — never before, never
        instead, never as a precondition."""
        result = await _report_turn(service, "sess-p1b")
        assert sp.INVITE_AFTER_REPORT in result.message
        assert result.message.index(PROSE) < result.message.index(sp.INVITE_AFTER_REPORT)


# ---------------------------------------------------------------------------
# CXO property 2 — invitation after, and cheap to decline
# ---------------------------------------------------------------------------


class TestCxoPropertyTwoInvitationAfterCheapDecline:
    pytestmark = pytest.mark.asyncio

    async def test_invitation_arms_the_offer_in_the_shared_carrier(self, service):
        """The invitation binds via the SAME #846 pending-offer store the
        rail's read-back uses (#1529 ordering — offer beats resume-check —
        holds by construction; no second offer mechanism)."""
        await _report_turn(service, "sess-p2")
        offer = _pending(service, "sess-p2")
        assert offer is not None
        assert offer["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW
        assert offer["pending_action"]["kind"] == sp.INVITE_KIND
        assert offer["pending_action"]["user_id"] == _USER

    async def test_decline_is_one_cheap_turn_no_interview_no_store(self, service, mem_prefs):
        """'no' through the REAL process_intent: one turn, the offer's own
        decline message, no interview started, nothing written anywhere."""
        sid = "sess-p2-no"
        service._start_standup_conversation = AsyncMock()
        await _report_turn(service, sid)
        result = await service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert result.success is True
        assert result.message == sp.INVITE_DECLINE_MESSAGE
        service._start_standup_conversation.assert_not_called()
        assert mem_prefs[_USER] == {}  # declining stores NOTHING


# ---------------------------------------------------------------------------
# CXO property 3 — declining changes nothing else
# ---------------------------------------------------------------------------


class TestCxoPropertyThreeDecliningChangesNothing:
    pytestmark = pytest.mark.asyncio

    async def test_report_after_decline_is_identical_and_not_reasked(self, service):
        """'If saying no makes tomorrow's report terser, thinner, or
        differently ordered, the next decline is no longer free.' The
        post-decline report's PROSE is byte-identical; only the trailing ask
        is gone (plain teaching line), and no offer is re-armed this
        session."""
        sid = "sess-p3"
        before = await _report_turn(service, sid)
        await service.process_intent(message="no", session_id=sid, user_id=_USER)
        after = await _report_turn(service, sid)
        # The report itself: unconditional, byte-identical prose.
        report_before = before.message.split("\n\n")[0]
        report_after = after.message.split("\n\n")[0]
        assert report_before == report_after == f"Good morning! {PROSE}"
        assert after.intent_data["context"]["standup_data"] == {"sections": []}
        # Not re-asked: no armed offer; discoverability line only.
        assert _pending(service, sid) is None
        assert TEACHING_LINE in after.message
        assert sp.INVITE_AFTER_REPORT not in after.message

    async def test_decline_is_session_scoped_not_punitive(self, service):
        """A decline suppresses re-asking THIS session only — the honest
        interim is 'a repeated invitation that is cheap to decline', not a
        remembered local preference (which would be a second store)."""
        vi.mark_declined("sess-p3-old", sp.INVITE_DECLINE_KEY)
        await _report_turn(service, "sess-p3-new")
        assert _pending(service, "sess-p3-new") is not None

    async def test_ignoring_the_invitation_changes_nothing_either(self, service):
        """Off-intent is not a 'no': the offer is dropped (popped, nothing
        fires) but NOT marked declined — a later report may honestly invite
        again."""
        sid = "sess-p3-ignore"
        await _report_turn(service, sid)
        assert _pending(service, sid) is not None
        # The pop-on-next-turn is the seam's job; here we pin the state rule:
        assert vi.was_declined(sid, sp.INVITE_DECLINE_KEY) is False


# ---------------------------------------------------------------------------
# PPM's empty-case rule — a different rule taking over, not an exception
# ---------------------------------------------------------------------------


class TestPpmEmptyExceptionInvitationFirst:
    pytestmark = pytest.mark.asyncio

    async def test_empty_fails_honestly_and_leads_with_the_invitation(self, service):
        """'An empty report is a null result wearing a report's format.'
        The empty turn does NOT demonstrate-then-ask: no report dress
        (no 'Good morning!' + prose shape), a plain statement that there is
        nothing, and the invitation IS the first move — armed in the same
        carrier."""
        result = await _report_turn(service, "sess-empty", empty=True)
        assert result.success is True
        assert result.message == sp.INVITE_EMPTY_LEAD
        assert result.message.startswith("I don't have anything to build your standup from")
        assert "Good morning!" not in result.message
        assert result.intent_data["context"]["empty"] is True
        offer = _pending(service, "sess-empty")
        assert offer is not None
        assert offer["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW

    async def test_discriminator_is_whether_the_read_produced_anything(self, service):
        """PPM's table, both rows: there IS data → demonstrate then ask
        (invitation after); there is NONE → fail honestly and offer
        (invitation first)."""
        with_data = await _report_turn(service, "sess-disc-a")
        empty = await _report_turn(service, "sess-disc-b", empty=True)
        assert with_data.message.index(PROSE) < with_data.message.index(
            sp.INVITE_AFTER_REPORT
        )
        assert empty.message == sp.INVITE_EMPTY_LEAD  # the ask leads

    async def test_empty_records_no_mode_choice_and_infers_nothing(self, service):
        """An empty render demonstrates nothing — it is not evidence the user
        chose the report mode, so repetition of empties never manufactures a
        read-back."""
        await _report_turn(service, "sess-empty-2", empty=True)
        await _report_turn(service, "sess-empty-2", empty=True)
        assert sp.infer_mode_signal(_USER) is None
        offer = _pending(service, "sess-empty-2")
        assert offer is not None and offer["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW

    async def test_empty_after_decline_stands_alone_without_nag(self, service):
        """Declined this session → the honest empty statement stands alone
        (teaching line for discoverability, no armed offer)."""
        sid = "sess-empty-3"
        vi.mark_declined(sid, sp.INVITE_DECLINE_KEY)
        result = await _report_turn(service, sid, empty=True)
        assert _pending(service, sid) is None
        assert "I don't have anything to build your standup from" in result.message
        assert "my standup interview" in result.message  # door stays visible


# ---------------------------------------------------------------------------
# Accept → the EXISTING #585 interview starts
# ---------------------------------------------------------------------------


class TestAcceptStartsInterview:
    pytestmark = pytest.mark.asyncio

    def _sentinel(self):
        return IntentProcessingResult(
            success=True,
            message="interview started",
            intent_data={"category": "execution", "action": "standup_started"},
        )

    async def test_yes_after_report_starts_the_existing_interview(self, service):
        """'yes' through the REAL process_intent dispatches the registered
        standup_interview workflow, which calls the SAME
        _start_standup_conversation the /standup command uses — one
        interview, three doors."""
        sid = "sess-accept"
        service._start_standup_conversation = AsyncMock(return_value=self._sentinel())
        await _report_turn(service, sid)
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.success is True
        assert result.message == "interview started"
        service._start_standup_conversation.assert_awaited_once_with(_USER, sid)
        assert _pending(service, sid) is None  # consumed, one-turn offer

    async def test_yes_on_the_empty_lead_starts_the_interview(self, service):
        """PPM's empty form is the same offer in the same carrier — accepting
        it starts the interview identically."""
        sid = "sess-accept-empty"
        service._start_standup_conversation = AsyncMock(return_value=self._sentinel())
        await _report_turn(service, sid, empty=True)
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.message == "interview started"
        service._start_standup_conversation.assert_awaited_once_with(_USER, sid)


# ---------------------------------------------------------------------------
# Low-confidence signal → the rail's read-back
# ---------------------------------------------------------------------------


class TestLowConfidenceReadBack:
    pytestmark = pytest.mark.asyncio

    async def test_repeated_report_choice_arms_the_rail_read_back(self, service):
        """Two served reports = a repeated mode choice = a low-confidence
        signal (0.55 < AUTO_APPLY_THRESHOLD) → the RAIL's read-back is armed
        through build_read_back_offer, after the complete report."""
        sid = "sess-rb"
        await _report_turn(service, sid)
        service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        result = await _report_turn(service, sid)
        offer = _pending(service, sid)
        assert offer is not None
        assert offer["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
        pa = offer["pending_action"]
        assert pa["kind"] == vi.VERIFY_INFERENCE_KIND
        assert pa["inference_key"] == sp.STANDUP_MODE_KEY
        assert pa["inference_value"] == sp.MODE_REPORT
        assert pa["confidence"] == pytest.approx(0.55)
        # The question rides AFTER the complete report (property 1 holds for
        # the read-back exactly as for the invitation).
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert sp.MODE_DESCRIPTIONS[sp.MODE_REPORT] in result.message
        assert result.message.index(PROSE) < result.message.index("Did I get that right?")

    async def test_interview_token_use_feeds_the_signal(self, service):
        """The issue's own example signal: repeated interview-token choices →
        the read-back proposes the INTERVIEW as the usual mode."""
        sentinel = IntentProcessingResult(
            success=True, message="interview started", intent_data={"action": "standup_started"}
        )
        service._start_standup_conversation = AsyncMock(return_value=sentinel)
        sid = "sess-rb-int"
        await _report_turn(service, sid, message="my standup interview")
        await _report_turn(service, sid, message="my standup interview")
        service._start_standup_conversation.reset_mock()
        await _report_turn(service, sid, message="give me my standup")
        offer = _pending(service, sid)
        assert offer is not None
        assert offer["pending_action"]["inference_value"] == sp.MODE_INTERVIEW
        # The report itself still rendered (the inference did not hijack an
        # explicit report request at read-back confidence).
        service._start_standup_conversation.assert_not_called()

    async def test_read_back_yes_stores_user_verified_then_honored(self, service, mem_prefs):
        """The full #1510 loop as #1591's consumer: yes → stored with
        source=user_verified; the NEXT report turn reads the store, re-infers
        nothing, and asks nothing (settled)."""
        sid = "sess-rb-yes"
        await _report_turn(service, sid)
        service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        await _report_turn(service, sid)
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.intent_data["verified"] is True
        stored = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY][sp.STANDUP_MODE_KEY]
        assert stored["value"] == sp.MODE_REPORT
        assert stored["source"] == vi.SOURCE_USER_VERIFIED
        # Settled: no read-back, no invitation, plain teaching line.
        after = await _report_turn(service, sid)
        assert _pending(service, sid) is None
        assert TEACHING_LINE in after.message

    async def test_read_back_no_is_not_reasked_same_session(self, service, mem_prefs):
        """Declining the read-back stores nothing, and the symmetric anti-nag
        rule quiets ALL standup asks for the session — the very next report
        does not come back with a different question (a decline buys quiet,
        not a rephrased ask)."""
        sid = "sess-rb-no"
        await _report_turn(service, sid)
        service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        await _report_turn(service, sid)
        await service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        assert vi.was_declined(sid, sp.STANDUP_MODE_KEY) is True
        after = await _report_turn(service, sid)
        assert _pending(service, sid) is None  # nothing re-armed, either ask
        assert TEACHING_LINE in after.message
        assert sp.MODE_DESCRIPTIONS[sp.MODE_REPORT] not in after.message


# ---------------------------------------------------------------------------
# Stored preference → honored without re-inference
# ---------------------------------------------------------------------------


class TestStoredPreferenceHonored:
    pytestmark = pytest.mark.asyncio

    async def test_stored_interview_redirects_generic_ask_without_reinference(
        self, service, mem_prefs
    ):
        """'Once verified, it's stored — not re-inferred each time': a stored
        standup_mode=interview redirects the GENERIC ask to the interview;
        the assembler never runs, nothing is inferred, nothing is asked."""
        await vi.store_verified_inference(
            _USER, sp.STANDUP_MODE_KEY, sp.MODE_INTERVIEW, confidence=0.55
        )
        sentinel = IntentProcessingResult(
            success=True, message="interview started", intent_data={"action": "standup_started"}
        )
        service._start_standup_conversation = AsyncMock(return_value=sentinel)
        with patch("services.standup.assembler.build_user_standup_summary") as assembler:
            result = await service._handle_standup_query(
                _standup_intent("give me my standup"),
                "wf-1591",
                session_id="sess-stored",
                user_id=_USER,
            )
        assert result is sentinel
        assembler.assert_not_called()  # honored, not re-derived/re-inferred
        service._start_standup_conversation.assert_awaited_once_with(_USER, "sess-stored")
        assert sp.infer_mode_signal(_USER) is None  # no evidence even recorded
        assert _pending(service, "sess-stored") is None

    async def test_stored_report_preference_settles_the_question(self, service, mem_prefs):
        """A stored report preference renders the report with NO invitation
        and NO read-back — the capture question is answered; only the
        discoverability line remains (PPM: visible + trivially revisable)."""
        await vi.store_verified_inference(
            _USER, sp.STANDUP_MODE_KEY, sp.MODE_REPORT, confidence=0.55
        )
        sid = "sess-stored-rep"
        result = await _report_turn(service, sid)
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert _pending(service, sid) is None
        assert TEACHING_LINE in result.message
        assert sp.INVITE_AFTER_REPORT not in result.message

    async def test_explicit_report_token_beats_stored_interview(self, service, mem_prefs):
        """The escape hatch: 'my standup report' reaches the report even with
        a stored interview preference — the taught escape phrase from the
        interview's opening cannot loop back into the interview."""
        await vi.store_verified_inference(
            _USER, sp.STANDUP_MODE_KEY, sp.MODE_INTERVIEW, confidence=0.55
        )
        service._start_standup_conversation = AsyncMock()
        result = await _report_turn(service, "sess-escape", message="my standup report")
        service._start_standup_conversation.assert_not_called()
        assert result.message.startswith(f"Good morning! {PROSE}")

    @pytest.mark.asyncio
    async def test_taught_escape_phrase_is_deterministically_claimed(self):
        """'my standup report' must route without the LLM classifier — the
        'my standup' cue claims it; the report token keeps it out of both the
        interview branch and the stored-interview redirect."""
        assert IntentService._is_standup_query("my standup report")

    async def test_stored_interview_without_session_falls_through_to_report(
        self, service, mem_prefs
    ):
        """No session → no conversation to key the interview to; the honest
        deterministic fallback is the report (same rule as the #1511 token
        branch)."""
        await vi.store_verified_inference(
            _USER, sp.STANDUP_MODE_KEY, sp.MODE_INTERVIEW, confidence=0.55
        )
        service._start_standup_conversation = AsyncMock()
        result = await _report_turn(service, None)
        service._start_standup_conversation.assert_not_called()
        assert result.message.startswith(f"Good morning! {PROSE}")


# ---------------------------------------------------------------------------
# High confidence → the rail's auto-apply semantics
# ---------------------------------------------------------------------------


class TestAutoApplySemantics:
    pytestmark = pytest.mark.asyncio

    async def test_sustained_repetition_auto_applies_without_read_back(
        self, service, mem_prefs
    ):
        """5 report choices → confidence 0.95 ≥ AUTO_APPLY_THRESHOLD → the
        rail says apply, don't ask: no read-back, no invitation nag, and
        (DEFAULT meta mode) NO store write — only VERIFIED values are stored,
        and this one was never read back."""
        sid = "sess-auto"
        for _ in range(4):
            await _report_turn(service, sid)
            service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        result = await _report_turn(service, sid)
        assert _pending(service, sid) is None
        assert TEACHING_LINE in result.message
        assert sp.INVITE_AFTER_REPORT not in result.message
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]

    async def test_trust_meta_mode_applies_and_stores_meta_auto(self, service, mem_prefs):
        """Under 'stop asking me every time' (TRUST_INFERENCES), a
        low-confidence signal auto-applies AND is stored with the rail's
        meta_auto provenance — the #1509-legible 'applied under a stop-asking
        preference' record, not a fabricated user_verified."""
        await vi.set_meta_mode(_USER, vi.VerificationMetaMode.TRUST_INFERENCES)
        sid = "sess-auto-trust"
        await _report_turn(service, sid)
        service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        await _report_turn(service, sid)
        stored = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY][sp.STANDUP_MODE_KEY]
        assert stored["value"] == sp.MODE_REPORT
        assert stored["source"] == vi.SOURCE_META_AUTO
        assert _pending(service, sid) is None  # applied, not asked

    async def test_auto_apply_interview_dispatches_the_interview(self, service, mem_prefs):
        """A ≥0.9-confidence INTERVIEW signal on a generic ask auto-applies
        by dispatching the interview (the applied value IS the mode)."""
        for _ in range(5):
            sp.record_mode_choice(_USER, sp.MODE_INTERVIEW)
        sentinel = IntentProcessingResult(
            success=True, message="interview started", intent_data={"action": "standup_started"}
        )
        service._start_standup_conversation = AsyncMock(return_value=sentinel)
        result = await _report_turn(service, "sess-auto-int")
        assert result is sentinel
        service._start_standup_conversation.assert_awaited_once_with(_USER, "sess-auto-int")
        # DEFAULT meta mode: applied, not stored (never verified).
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]


# ---------------------------------------------------------------------------
# The invitation's workflow entry (#1557 pin, mirrors verify_inference's)
# ---------------------------------------------------------------------------


class TestStandupInterviewWorkflowEntry:
    def test_registered_offer_only_write_entry(self):
        """Registered, WRITE (explicit + defaultless per #1557 — starting the
        #585 interview durably creates a conversation row via repo.add), and
        rail-unreachable (action_triggered=False): a classifier emission can
        never start a conversation."""
        from services.intent_service.workflow_dispatcher import (
            WORKFLOW_REGISTRY,
            get_action_workflows,
        )
        from services.intent_service.workflow_entries import register_default_workflows
        from services.shared_types import EffectClass

        register_default_workflows()
        entry = WORKFLOW_REGISTRY[sp.STANDUP_INTERVIEW_WORKFLOW]
        assert entry.effect == EffectClass.WRITE
        assert "pending_action" in entry.requires_context
        assert "intent_service" in entry.requires_context
        assert sp.STANDUP_INTERVIEW_WORKFLOW not in get_action_workflows()

    @pytest.mark.asyncio
    async def test_principal_mismatch_never_starts_a_conversation(self):
        """#1532: the invitation was offered to user A; the accepting turn is
        user B — no conversation starts for either."""
        from services.intent_service.workflow_entries import (
            run_standup_interview_workflow,
        )

        fake_service = MagicMock()
        fake_service._start_standup_conversation = AsyncMock()
        result = await run_standup_interview_workflow(
            session_id="s",
            user_id="9f7b8a52-1532-4b00-9e00-000000001532",
            context={
                "intent_service": fake_service,
                "pending_action": {"kind": sp.INVITE_KIND, "user_id": _USER},
            },
        )
        assert result["intent_data"]["principal_mismatch"] is True
        fake_service._start_standup_conversation.assert_not_called()

    @pytest.mark.asyncio
    async def test_foreign_or_missing_payload_returns_none(self):
        """An accidental workflow_type collision without our payload marker
        must fall to the floor, not start a conversation."""
        from services.intent_service.workflow_entries import (
            run_standup_interview_workflow,
        )

        assert (
            await run_standup_interview_workflow(session_id="s", context={}) is None
        )
        fake_service = MagicMock()
        fake_service._start_standup_conversation = AsyncMock()
        assert (
            await run_standup_interview_workflow(
                session_id="s",
                user_id=_USER,
                context={
                    "intent_service": fake_service,
                    "pending_action": {"kind": "something_else"},
                },
            )
            is None
        )
        fake_service._start_standup_conversation.assert_not_called()
