"""#1591 declaration path (PM live verdict 2026-08-13 3:26–3:29 PM, PARTIAL).

The built preference loop passed live; the path INTO it from a direct
declaration didn't exist. PM's turn ``use the standup interview format by
default from now on`` fell to the floor, which improvised an unstored promise
("Noted for this conversation…") that broke two turns later — fabricated
capability + broken commitment in one turn.

The fix (sanctioned shape, per the issue's own comment): ONLY the
standup-token phrasings, riding the already-claiming standup surface as an
in-handler branch (#1431 pattern; no new pre-classifier patterns, no claim
widening under the moratorium). A declaration turn stores the mode via the
verified-inference rail as a DECLARED value (source=user_declared,
confidence 1.0 — the highest-confidence signal there is; store +
confirmation copy, never a read-back question), and the confirmation
teaches a switch-back phrase that genuinely ROUTES (#1571): 'back to my
standup report' carries the 'my standup' cue ``_is_standup_query`` claims,
so it resolves deterministically — and the same declaration branch acts on
it (stores the report default back).

Reachability honesty (m-43, flagged for Lead): PM's exact phrasing carries
the bare 'standup' token, which NO deterministic surface claims (the
pre-classifier's bare-standup pattern was removed for temporal false
positives; ``_is_standup_query`` needs its cue list). It reaches this branch
when any surface emits a standup action for it (live, the LLM lane) — the
deterministic-reachability gap is exactly the #1595 corpus material the
issue names, and the tokenless phrasing is a corpus row too. The e2e class
therefore pins the 'my standup'-cued declaration forms end-to-end with an
explosive LLM, and pins PM's exact phrasing at the handler seam.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import standup_preferences as sp
from services.intent_service import verified_inference as vi
from services.intent_service.classifier import IntentClassifier
from services.shared_types import IntentCategory

# PM's verbatim declaration turn (2026-08-13, live FAIL 2).
PM_DECLARATION = "use the standup interview format by default from now on"
# The tokenless live FAIL 1 — a #1595 corpus row, deliberately NOT claimed.
PM_TOKENLESS = "use the interview from now on"
# The taught switch-back phrase (routes via the 'my standup' cue).
TAUGHT_SWITCH_BACK = "back to my standup report"
# A declaration form that ALSO routes deterministically ('my standup' cue).
ROUTABLE_DECLARATION = "use the interview format for my standup from now on"

_USER = "3f7b8a52-1591-4b00-9e00-000000001591"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — declaration turns in this class "
            "must resolve deterministically"
        )


@pytest.fixture(autouse=True)
def _clean_transient_state():
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()
    yield
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double at the ONE persistence seam."""
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
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _standup_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.STATUS,
        action="get_standup",
        original_message=message,
        confidence=1.0,
    )


def _summary(empty: bool = False):
    summary = MagicMock()
    summary.is_empty.return_value = empty
    summary.to_prose.return_value = "Here's your derived standup."
    summary.to_dict.return_value = {"sections": []}
    return summary


def _stored_mode(mem_prefs):
    return (mem_prefs[_USER].get(vi.VERIFIED_INFERENCES_PREF_KEY) or {}).get(sp.STANDUP_MODE_KEY)


# ---------------------------------------------------------------------------
# Detection unit
# ---------------------------------------------------------------------------


class TestDeclarationDetection:
    def test_pm_exact_phrasing_declares_interview(self):
        assert sp.detect_standup_mode_declaration(PM_DECLARATION) == sp.MODE_INTERVIEW

    def test_taught_switch_back_declares_report(self):
        assert sp.detect_standup_mode_declaration(TAUGHT_SWITCH_BACK) == sp.MODE_REPORT

    def test_routable_declaration_form_declares_interview(self):
        assert sp.detect_standup_mode_declaration(ROUTABLE_DECLARATION) == sp.MODE_INTERVIEW

    def test_tokenless_phrasing_is_not_claimed(self):
        """'use the interview from now on' has no standup token — it is a
        #1595 corpus row, and this detector must not claim it (moratorium)."""
        assert sp.detect_standup_mode_declaration(PM_TOKENLESS) is None

    def test_one_off_asks_carry_no_durativity_and_are_untouched(self):
        assert sp.detect_standup_mode_declaration("my standup interview") is None
        assert sp.detect_standup_mode_declaration("give me my standup report") is None

    def test_ambiguous_both_directions_is_no_declaration(self):
        assert (
            sp.detect_standup_mode_declaration(
                "use the standup interview instead of the quick report from now on"
            )
            is None
        )

    def test_directionless_durative_standup_mention_is_no_declaration(self):
        assert sp.detect_standup_mode_declaration("do my standup daily from now on") is None

    def test_working_mode_surface_does_not_steal_pm_phrasing(self):
        """The #1510 declaration surface runs ABOVE routing — it must return
        None for PM's standup declaration or the turn would never reach the
        standup handler at all."""
        from services.intent_service.collaboration_gate import detect_mode_declaration

        assert detect_mode_declaration(PM_DECLARATION) is None
        assert detect_mode_declaration(TAUGHT_SWITCH_BACK) is None


# ---------------------------------------------------------------------------
# Handler seam — PM's exact phrasing (reachability: see module docstring)
# ---------------------------------------------------------------------------


class TestDeclarationAtHandlerSeam:
    pytestmark = pytest.mark.asyncio

    async def _turn(self, service, message, user_id=_USER, sid="sess-1591-decl"):
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_summary()),
        ):
            return await service._handle_standup_query(
                _standup_intent(message), "wf-1591", session_id=sid, user_id=user_id
            )

    async def test_pm_declaration_stores_declared_value_and_confirms(self, service, mem_prefs):
        result = await self._turn(service, PM_DECLARATION)
        assert result.success is True
        assert result.message == sp.declaration_confirmation(sp.MODE_INTERVIEW, True)
        assert "back to my standup report" in result.message  # taught phrase
        record = _stored_mode(mem_prefs)
        assert record is not None
        assert record["value"] == sp.MODE_INTERVIEW
        assert record["source"] == vi.SOURCE_USER_DECLARED
        assert record["confidence_at_verification"] == 1.0

    async def test_declaration_does_not_start_the_interview(self, service):
        """Ordering pin: the declaration contains the interview token — the
        token branch below it must NOT fire (store + confirm, no flow start,
        no read-back question)."""
        service._start_standup_conversation = AsyncMock()
        result = await self._turn(service, PM_DECLARATION)
        service._start_standup_conversation.assert_not_called()
        assert "(yes/no)" not in result.message  # not a read-back

    async def test_next_generic_ask_honors_the_declared_interview(self, service, mem_prefs):
        """PM's live expectation: after the declaration, the next standup ask
        goes straight to the interview — stored, not re-inferred."""
        await self._turn(service, PM_DECLARATION)
        service._start_standup_conversation = AsyncMock(return_value="INTERVIEW")
        result = await self._turn(service, "give me my standup")
        service._start_standup_conversation.assert_awaited_once()
        assert result == "INTERVIEW"

    async def test_switch_back_declaration_flips_the_store(self, service, mem_prefs):
        """The taught phrase acts: 'back to my standup report' re-declares the
        report default over the stored interview value."""
        await self._turn(service, PM_DECLARATION)
        result = await self._turn(service, TAUGHT_SWITCH_BACK)
        assert result.message == sp.declaration_confirmation(sp.MODE_REPORT, True)
        assert _stored_mode(mem_prefs)["value"] == sp.MODE_REPORT
        # And the generic ask now renders the report (no interview dispatch).
        service._start_standup_conversation = AsyncMock()
        report = await self._turn(service, "give me my standup")
        service._start_standup_conversation.assert_not_called()
        assert "Here's your derived standup." in report.message

    async def test_anonymous_declaration_is_honest_not_fabricated(self, service, mem_prefs):
        """No signed-in user → no store to write. The reply says so instead
        of promising (the floor's fabricated promise is the bug this path
        replaces) — and teaches only phrases that route."""
        result = await self._turn(service, PM_DECLARATION, user_id=None)
        assert result.message == sp.DECLARATION_NO_USER_MESSAGE
        assert mem_prefs[_USER] == {}

    async def test_failed_persistence_is_visible(self, service, monkeypatch):
        """persisted=False must be visible (no confabulated durable change)."""
        from services.intent_service import collaboration_gate

        async def _save_fails(user_id, key, value):
            return False

        monkeypatch.setattr(collaboration_gate, "_save_preference", _save_fails)
        result = await self._turn(service, PM_DECLARATION)
        assert "couldn't save that preference" in result.message


# ---------------------------------------------------------------------------
# End-to-end — the routable declaration forms through the REAL process_intent
# ---------------------------------------------------------------------------


class TestEndToEndRoutableDeclarations:
    pytestmark = pytest.mark.asyncio

    async def _e2e(self, service, message, sid):
        with patch(
            "services.standup.assembler.build_user_standup_summary",
            new=AsyncMock(return_value=_summary()),
        ):
            return await service.process_intent(message=message, session_id=sid, user_id=_USER)

    async def test_routable_declaration_deterministic_end_to_end(self, service, mem_prefs):
        """A 'my standup'-cued declaration resolves with the LLM structurally
        unreachable: _is_standup_query claims it, the in-handler branch
        stores the declared interview default and confirms."""
        result = await self._e2e(service, ROUTABLE_DECLARATION, "e2e-1591-decl")
        assert result.message == sp.declaration_confirmation(sp.MODE_INTERVIEW, True)
        assert _stored_mode(mem_prefs)["value"] == sp.MODE_INTERVIEW
        assert _stored_mode(mem_prefs)["source"] == vi.SOURCE_USER_DECLARED

    async def test_taught_switch_back_routes_end_to_end(self, service, mem_prefs):
        """#1571's rule made real: the phrase the confirmation copy teaches
        is driven through the REAL process_intent with an explosive LLM and
        both ROUTES and ACTS (declares the report default)."""
        await self._e2e(service, ROUTABLE_DECLARATION, "e2e-1591-back")
        result = await self._e2e(service, TAUGHT_SWITCH_BACK, "e2e-1591-back")
        assert result.message == sp.declaration_confirmation(sp.MODE_REPORT, True)
        assert _stored_mode(mem_prefs)["value"] == sp.MODE_REPORT

    async def test_stored_declaration_redirects_the_generic_ask_end_to_end(
        self, service, mem_prefs
    ):
        """The full PM loop, deterministic: declare → confirmed → 'give me my
        standup' goes straight to the interview (stored, not re-inferred)."""
        await self._e2e(service, ROUTABLE_DECLARATION, "e2e-1591-loop")
        from services.intent.intent_service import IntentProcessingResult

        service._start_standup_conversation = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="INTERVIEW STARTED", intent_data={}
            )
        )
        result = await self._e2e(service, "give me my standup", "e2e-1591-loop")
        service._start_standup_conversation.assert_awaited_once()
        assert "INTERVIEW STARTED" in result.message
