"""#1650 [MVP] — CONFIRM kinds accept only anchored, crisp, full-message
affirmatives.

PM live 2026-08-18: with a delete-correction confirm armed ("delete this
reminder instead? yes/no"), PM typed an ASIDE — "please note that I'll need
to figure out later why you thought I wanted you to delete a project." —
and the delete FIRED off the greedy "^please\\s" accept row. One line,
~95 chars: under the #1631 prose floor, so the shape override never
triggered. Class: one-label-two-objects (an aside wearing an accept
prefix).

The fix: every offer dispatching the #1190 pending-action carrier
(``CONFIRM_PENDING_ACTION_WORKFLOW`` — destructive close/reopen confirms,
consent checks, reminder-clear delete confirms, drafted-issue file
confirms, repo-question default binds) consults the STRICT
``detect_confirm_response`` at its accept seam: the whole message must be
crisp affirmative vocabulary. Everything else falls to each kind's
documented off-intent rule (#1190: the pop already cancelled the action —
nothing can fire — and normal processing answers the turn; kinds that
document a re-ask re-ask). Declines are unchanged (the crisp decline set
was never the greedy hazard). Generic (non-confirm) offers keep #1631
behavior byte-for-byte.

Layer honesty (m-43): the unit classes pin the shared detector and the
correction-claim anchoring; the end-to-end class drives the REAL
``IntentService.process_intent`` (the #1411-test idiom), mocked only at
the LLM boundary (explosive) and the GitHub-router boundary (explosive
wherever nothing should fire).
"""

from unittest.mock import AsyncMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingError, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import (
    PROSE_LENGTH_FLOOR,
    detect_confirm_response,
    detect_offer_response,
)
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1650-4b00-9e00-000000001650"  # valid UUID: survives principal parsing

# PM's exact aside, verbatim from the live transcript (one line, ~95 chars —
# under the #1631 floor, which is the whole point of this issue).
PM_ASIDE = (
    "please note that I'll need to figure out later why you thought I "
    "wanted you to delete a project."
)


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1650 turns must resolve "
            "deterministically"
        )


# ---------------------------------------------------------------------------
# 1. The strict detector (unit)
# ---------------------------------------------------------------------------


class TestConfirmAcceptVocabulary:
    def test_pm_aside_is_not_an_accept(self):
        """THE incident shape: single-line, under the floor, greedy-row
        prefix — the generic detector calls it an accept; the confirm
        detector must not."""
        assert len(PM_ASIDE) < PROSE_LENGTH_FLOOR and "\n" not in PM_ASIDE
        assert detect_offer_response(PM_ASIDE) == "accept"  # the bug's fuel
        assert detect_confirm_response(PM_ASIDE) is None

    @pytest.mark.parametrize(
        "message",
        [
            # the #1650 vocabulary, register kept from ACCEPT_PATTERNS row 1
            "yes",
            "y",
            "yes please",
            "yep",
            "yup",
            "do it",
            "confirm",
            "go ahead",
            # crisp combinations and politeness tails
            "Yes, please!",
            "yes, do it",
            "sure, go ahead",
            "go ahead and do it",
            "okay",
            "sure",
            "yes thanks",
            "sounds good",
            "let's do it",
            "please do",
        ],
    )
    def test_crisp_affirmatives_accept(self, message):
        assert detect_confirm_response(message) == "accept"

    @pytest.mark.parametrize(
        "message",
        [
            # near-accepts: greedy-row shapes that are NOT full-message
            # affirmatives — the one-label-two-objects class
            "yes, but hold on",
            "sure, whatever you think",
            "please hold on a sec",
            "please note that we should wait",
            "yes and delete everything else too",
            "go ahead with the other one",
            "yes we should discuss this first",
            PM_ASIDE,
        ],
    )
    def test_near_accepts_are_not_accepts(self, message):
        """Each of these IS an accept to the generic rows (that's what makes
        them hazards) and must be None to the confirm detector."""
        assert detect_offer_response(message) == "accept"
        assert detect_confirm_response(message) is None

    @pytest.mark.parametrize(
        "message",
        ["no", "nope", "no thanks", "not now", "never mind", "no, don't", "nah"],
    )
    def test_declines_unchanged(self, message):
        """The crisp decline set stays as-is — declining only cancels."""
        assert detect_confirm_response(message) == "decline"
        assert detect_offer_response(message) == "decline"

    def test_prose_shapes_stay_none(self):
        """#1631's floor still applies above the crisp check — long or
        multi-line turns are never confirm responses either."""
        assert detect_confirm_response("yes " * 80) is None
        assert detect_confirm_response("yes\nplease") is None

    def test_generic_detector_untouched(self):
        """#1650 must not change generic (non-confirm) offer behavior: the
        greedy prefix rows still accept short turns for soft offers."""
        assert detect_offer_response("yes, that's right") == "accept"
        assert detect_offer_response("sure, let's try that") == "accept"


# ---------------------------------------------------------------------------
# 2. The correction window's claim is anchored (unit)
# ---------------------------------------------------------------------------


class TestCorrectionClaimAnchoring:
    """#1650's second layer: reminder_clear's correction window used an
    unanchored \\bdelete\\b — PM's aside *mentions* deleting and would claim
    the correction (arming a live delete confirm one crisp 'yes' from data
    loss)."""

    @pytest.mark.parametrize(
        "message",
        [
            "I meant delete",  # the #1605 pinned phrase
            "delete them",
            "delete",
            "no, delete them",
            "actually delete those",
            "oops, I meant delete",
            "yes, delete them",
            "wait, delete them instead",
            "please delete them",
            "remove them",
            "get rid of them",
            "I wanted you to delete them",
        ],
    )
    def test_crisp_corrections_still_claim(self, message):
        from services.intent_service.reminder_clear import (
            _CORRECTION_CLAIM_RE,
            _NEGATED_DELETE_RE,
        )

        assert _CORRECTION_CLAIM_RE.match(message)
        assert not _NEGATED_DELETE_RE.search(message)

    @pytest.mark.parametrize(
        "message",
        [
            PM_ASIDE,
            "why did you delete that?",
            "the delete button is broken",
            "please note that deleting is bad",
            "don't delete them",
        ],
    )
    def test_asides_and_negations_do_not_claim(self, message):
        from services.intent_service.reminder_clear import (
            _CORRECTION_CLAIM_RE,
            _NEGATED_DELETE_RE,
        )

        claimed = bool(_CORRECTION_CLAIM_RE.match(message)) and not (
            _NEGATED_DELETE_RE.search(message)
        )
        assert not claimed

    @pytest.mark.asyncio
    async def test_correction_turn_falls_through_on_the_aside(self):
        """Through the real turn handler: the aside returns None (off-intent
        fall-through — the pop drops the window; nothing is armed)."""
        from services.intent_service.reminder_clear import (
            CLEAR_CORRECTION_KIND,
            handle_reminder_clear_turn,
        )

        class _ExplosiveOfferService:
            def set_pending_offer(self, *a, **k):
                raise AssertionError(
                    "correction window armed a confirm off the aside"
                )

        class _Svc:
            workflow_offer_service = _ExplosiveOfferService()

        pending_offer = {
            "pending_action": {
                "kind": CLEAR_CORRECTION_KIND,
                "user_id": _USER,
                "clear_verb": "clear",
                "clear_noun": "reminder",
                "clear_target_ids": ["a"],
                "clear_target_texts": ["ship the memo"],
                "original_message": "clear my reminder",
            },
        }
        result = await handle_reminder_clear_turn(
            pending_offer,
            PM_ASIDE,
            session_id="sess-1650-corr",
            user_id=_USER,
            intent_service=_Svc(),
        )
        assert result is None


# ---------------------------------------------------------------------------
# 3. End-to-end: the armed destructive confirm (the #1190 tier, real
#    process_intent — the #1411-test idiom)
# ---------------------------------------------------------------------------


def _explosive_router(monkeypatch, allow_update=False):
    from services.integrations.github.github_integration_router import (
        GitHubIntegrationRouter,
    )

    async def _noop_init(self, user_id=None):
        return None

    async def _available(self):
        return True

    async def _explosive_get_issue(self, *a, **k):
        raise AssertionError("github_router.get_issue called")

    monkeypatch.setattr(GitHubIntegrationRouter, "initialize", _noop_init)
    monkeypatch.setattr(GitHubIntegrationRouter, "is_available", _available)
    monkeypatch.setattr(GitHubIntegrationRouter, "get_issue", _explosive_get_issue)

    if allow_update:
        update_mock = AsyncMock(
            return_value={
                "title": "Test issue",
                "html_url": "https://github.com/x/y/issues/108",
            }
        )
        monkeypatch.setattr(GitHubIntegrationRouter, "update_issue", update_mock)
        return update_mock

    async def _explosive_update(self, *a, **k):
        raise AssertionError(
            "github_router.update_issue FIRED — a destructive mutation "
            "executed without a crisp confirmed yes (#1650 gate breach)"
        )

    monkeypatch.setattr(GitHubIntegrationRouter, "update_issue", _explosive_update)
    return None


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestDestructiveConfirmCrispEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_pm_aside_never_fires_the_armed_confirm(
        self, live_service, monkeypatch
    ):
        """THE acceptance pin: PM's exact aside against an armed close
        confirm. RED pre-fix: the greedy "^please\\s" row read it as YES and
        update_issue fired. GREEN: neither accept nor decline claims it —
        the documented #1190 off-intent rule applies (the pop cancelled the
        action, nothing can fire, and the turn falls to normal processing —
        here the explosive LLM boundary, proving no offer seam claimed it)."""
        update_mock = _explosive_router(monkeypatch, allow_update=True)
        sid = "e2e-1650-aside"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        try:
            result = await live_service.process_intent(
                message=PM_ASIDE, session_id=sid, user_id=_USER
            )
            # However the turn resolves downstream, it is never the decline
            # copy — declining was not what PM said either.
            assert "won't close issue #108" not in result.message
        except IntentProcessingError as exc:
            assert (
                "LLM boundary touched" in str(exc)
                or "INTENT_CLASSIFICATION_FAILED" in str(exc)
            ), str(exc)
        update_mock.assert_not_awaited()  # nothing fired
        assert _pending_offers(live_service).get(sid) is None  # popped

    @pytest.mark.parametrize(
        "affirmative", ["yes", "yes please", "go ahead", "do it", "confirm", "y"]
    )
    async def test_crisp_yes_forms_still_fire(
        self, live_service, monkeypatch, affirmative
    ):
        _explosive_router(monkeypatch, allow_update=False)
        sid = f"e2e-1650-yes-{affirmative.replace(' ', '-')}"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        update_mock = _explosive_router(monkeypatch, allow_update=True)
        result = await live_service.process_intent(
            message=affirmative, session_id=sid, user_id=_USER
        )
        update_mock.assert_awaited_once_with(108, state="closed")
        assert "Closed issue #108" in result.message

    @pytest.mark.parametrize("negative", ["no", "no thanks", "cancel"])
    async def test_crisp_no_forms_still_cancel(
        self, live_service, monkeypatch, negative
    ):
        _explosive_router(monkeypatch, allow_update=False)
        sid = f"e2e-1650-no-{negative.replace(' ', '-')}"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message=negative, session_id=sid, user_id=_USER
        )
        assert "won't close issue #108" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_short_near_accept_neither_fires_nor_declines(
        self, live_service, monkeypatch
    ):
        """A short single-line turn the generic rows would claim ("sure,
        whatever you think") — well under the #1631 floor, so only the
        #1650 crisp rule protects it."""
        near_accept = "sure, whatever you think"
        assert detect_offer_response(near_accept) == "accept"
        update_mock = _explosive_router(monkeypatch, allow_update=True)
        sid = "e2e-1650-nearaccept"
        await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        try:
            result = await live_service.process_intent(
                message=near_accept, session_id=sid, user_id=_USER
            )
            assert "won't close issue #108" not in result.message
        except IntentProcessingError as exc:
            assert (
                "LLM boundary touched" in str(exc)
                or "INTENT_CLASSIFICATION_FAILED" in str(exc)
            ), str(exc)
        update_mock.assert_not_awaited()
        assert _pending_offers(live_service).get(sid) is None
