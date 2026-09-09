"""#1739 [MVP] — THE acceptance contract: one predicate, every armed seam.

PM's 2026-09-09 round (Exec's convergence memo): three failures in one
session were ONE contract failing in opposite directions — a question fired
a state change (#1617) while a bare "yes" did nothing (#1694) and prose
asides fired (#1631/#1650). PM: "we're not patching via whack-a-mole, but
capturing patterns."

Pinned here:
1. the predicate itself (``acceptance.evaluate_acceptance``) — verdicts,
   the two-axis strictness (Arch's ratified EffectClass law + CXO's binding
   correction that Outwardness is the second half of the same gate), the
   question-shape guard, the prose floor, taught vocabulary, and the
   NAMED_OBJECT input-adequacy refusal (Arch condition (a) with teeth);
2. the compatibility alias ``detect_confirm_response`` (absorbed, not
   paralleled — #1650's suite pins its unchanged vocabulary; here we pin
   the one thing the contract ADDS to it: question-forms never accept);
3. the adopted generic-offer-seam READ tier end-to-end (the #1411/#1650
   test idiom — real ``process_intent``, explosive LLM boundary): a state
   question RE-ARMS the offer (the arm survives) and a decline still
   cancels honestly.

The standup REFINING seam's pins — including PM's verbatim "are we done
with that standup?" — live with that seam's suite
(tests/unit/services/standup/test_conversation_handler.py,
TestRefiningAcceptanceContract1739). The adoption ratchet lives in
tests/test_architecture_enforcement.py::TestAcceptanceContractRatchet.

Layer honesty (m-43): classes 1–2 pin the shared predicate (unit); class 3
drives the REAL IntentService offer seam with the LLM boundary explosive.
"""

import pytest

from services.intent.intent_service import IntentProcessingError, IntentService
from services.intent_service.acceptance import (
    LEGACY_UNTHREADED,
    AcceptanceTier,
    AcceptanceVerdict,
    acceptance_tier,
    declared_axes_for_workflow,
    evaluate_acceptance,
    is_state_question,
)
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import (
    detect_confirm_response,
    detect_offer_response,
)
from services.shared_types import EffectClass, Outwardness

_USER = "3f7b8a52-1739-4b00-9e00-000000001739"  # valid UUID: survives principal parsing

# PM's verbatim failing turns from the 2026-09-09 live round (Exec's memo).
PM_STANDUP_QUESTION = "are we done with that standup?"
PM_BARE_YES = "yes"

# PM's 2026-08-18 aside, verbatim (the #1650 incident — the aside that fired
# an armed delete off the greedy "^please\\s" row).
PM_ASIDE_1650 = (
    "please note that I'll need to figure out later why you thought I "
    "wanted you to delete a project."
)

_AN_ASK = "Want me to mark that overdue todo done? (yes/no)"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1739 offer-seam turns must "
            "resolve deterministically"
        )


# ---------------------------------------------------------------------------
# 1. The predicate (unit)
# ---------------------------------------------------------------------------


class TestTwoAxisStrictness:
    """CXO's binding structural correction: the ask scales on TWO ratified
    axes (decide_consent's own two), so the acceptance must too — an
    effect-only predicate would give "shall I post this comment on the
    issue?" exactly the acceptance bar of "shall I update your todo's
    title?"."""

    @pytest.mark.parametrize(
        "effect,outwardness,tier",
        [
            (EffectClass.READ, Outwardness.PRIVATE, AcceptanceTier.LOW_CEREMONY),
            (EffectClass.READ, Outwardness.OUTWARD, AcceptanceTier.LOW_CEREMONY),
            (EffectClass.WRITE, Outwardness.PRIVATE, AcceptanceTier.LOW_CEREMONY),
            # THE corrected cell: an outward WRITE accepts at the
            # DESTRUCTIVE-tier bar (socially irreversible the instant it
            # lands — the entire reason the axis exists).
            (EffectClass.WRITE, Outwardness.OUTWARD, AcceptanceTier.NAMED_OBJECT),
            (EffectClass.DESTRUCTIVE, Outwardness.PRIVATE, AcceptanceTier.NAMED_OBJECT),
            (EffectClass.DESTRUCTIVE, Outwardness.OUTWARD, AcceptanceTier.NAMED_OBJECT),
        ],
    )
    def test_tier_matrix(self, effect, outwardness, tier):
        assert acceptance_tier(effect, outwardness) == tier

    def test_undeclared_effect_gets_the_strict_bar(self):
        """The safe direction: an undeclared seam can never get a WEAKER bar
        than a declared one."""
        assert acceptance_tier(None, None) == AcceptanceTier.NAMED_OBJECT

    def test_outward_write_takes_the_strict_vocabulary(self):
        """ "yes, that's right" is an accept to the generic rows (pinned in
        #1650's suite) — at OUTWARD WRITE it must NOT accept; only the crisp
        full-message forms do."""
        loose = evaluate_acceptance(
            "yes, that's right",
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            armed_question=_AN_ASK,
        )
        strict = evaluate_acceptance(
            "yes, that's right",
            effect=EffectClass.WRITE,
            outwardness=Outwardness.OUTWARD,
            armed_question=_AN_ASK,
        )
        assert loose is AcceptanceVerdict.ACCEPT
        assert strict is AcceptanceVerdict.PASS
        # The crisp form accepts at BOTH bars (#1694's direction: a bare
        # affirmative against an exactly-armed offer is a yes).
        assert (
            evaluate_acceptance(
                PM_BARE_YES,
                effect=EffectClass.WRITE,
                outwardness=Outwardness.OUTWARD,
                armed_question=_AN_ASK,
            )
            is AcceptanceVerdict.ACCEPT
        )


class TestQuestionFormsNeverAccept:
    """Contract axis (a): interrogative shape is a state query, not consent
    (CXO: a DIFFERENT SPEECH ACT, not a failed acceptance)."""

    @pytest.mark.parametrize(
        "question",
        [
            PM_STANDUP_QUESTION,  # PM verbatim, no affirmative token, no "?" needed
            "are we done with that standup",  # opener-shape without the "?"
            "done?",
            "yes?",
            "sure?",
            "is it saved?",
            "did that work?",
            "what's the sixth one?",
            "yes, what happened?",  # accept-prefixed question — the greedy-row steal
            "sure, why not?",
        ],
    )
    @pytest.mark.parametrize(
        "effect,outwardness",
        [
            (EffectClass.READ, Outwardness.PRIVATE),
            (EffectClass.WRITE, Outwardness.PRIVATE),
            (EffectClass.WRITE, Outwardness.OUTWARD),
            (EffectClass.DESTRUCTIVE, Outwardness.PRIVATE),
        ],
    )
    def test_questions_are_state_questions_at_every_tier(self, question, effect, outwardness):
        verdict = evaluate_acceptance(
            question,
            effect=effect,
            outwardness=outwardness,
            armed_question=_AN_ASK,
            taught_accepts=("done", "looks good"),
        )
        assert verdict is AcceptanceVerdict.STATE_QUESTION, question

    def test_question_shape_detector(self):
        assert is_state_question(PM_STANDUP_QUESTION)
        assert is_state_question("are we done with that standup")
        assert not is_state_question("do it")  # imperative opener, no "?"
        assert not is_state_question("go ahead and do it")
        assert not is_state_question("no, don't")
        assert not is_state_question("looks good")


class TestBareAffirmativesAcceptArmedOffers:
    """Contract axis (b) — #1694's failure direction: 'yes', the least
    ambiguous acceptance available, did nothing."""

    @pytest.mark.parametrize("affirmative", ["yes", "y", "yes please", "go ahead", "ok"])
    def test_bare_affirmatives_accept_at_both_tiers(self, affirmative):
        for effect in (EffectClass.READ, EffectClass.DESTRUCTIVE):
            assert (
                evaluate_acceptance(
                    affirmative,
                    effect=effect,
                    armed_question=_AN_ASK,
                )
                is AcceptanceVerdict.ACCEPT
            )

    def test_named_object_tier_refuses_accept_without_an_armed_ask(self):
        """Arch condition (a), mechanical: a predicate fed None returns
        judgment, not confidence — an accept against an arm site that stored
        no rendered ask is refused at the strict tier (CXO's user-facing
        twin: if Piper cannot quote the acceptance back into a true
        sentence, the offer was not specific enough to be accepted)."""
        assert (
            evaluate_acceptance(
                "yes",
                effect=EffectClass.DESTRUCTIVE,
                armed_question=None,
            )
            is AcceptanceVerdict.PASS
        )
        # The LOW tier still accepts (READ offers are cheap + reversible —
        # Arch condition (b)'s reason for adopting them first).
        assert (
            evaluate_acceptance(
                "yes",
                effect=EffectClass.READ,
                armed_question=None,
            )
            is AcceptanceVerdict.ACCEPT
        )
        # And a decline is never blocked by adequacy — declining only cancels.
        assert (
            evaluate_acceptance(
                "no thanks",
                effect=EffectClass.DESTRUCTIVE,
                armed_question=None,
            )
            is AcceptanceVerdict.DECLINE
        )


class TestAsidesNeitherAcceptNorSteal:
    """Contract axis (c): the #1631 shape floor and the #1650 crisp rule,
    composed in the predicate."""

    def test_pm_1650_aside_never_accepts_at_the_strict_tier(self):
        """PM's aside must never fire anything at the NAMED_OBJECT bar —
        DESTRUCTIVE (any outwardness) and OUTWARD WRITE."""
        for effect, outwardness in (
            (EffectClass.DESTRUCTIVE, Outwardness.PRIVATE),
            (EffectClass.DESTRUCTIVE, Outwardness.OUTWARD),
            (EffectClass.WRITE, Outwardness.OUTWARD),
        ):
            verdict = evaluate_acceptance(
                PM_ASIDE_1650,
                effect=effect,
                outwardness=outwardness,
                armed_question=_AN_ASK,
            )
            assert verdict is AcceptanceVerdict.PASS

    def test_low_tier_keeps_the_generic_vocabulary_including_its_greedy_residue(self):
        """HONEST RESIDUE PIN (not an endorsement): the LOW_CEREMONY tier is
        CXO's COLLABORATE bar and carries the generic vocabulary as-is —
        including the greedy prefix rows #1631 audited. PM's aside therefore
        still reads as an accept at LOW tier, exactly as the legacy generic
        detector reads it. Every seam ADOPTED at LOW tier this lane is
        EffectClass.READ (cheap + reversible — Arch condition (b));
        tightening the LOW vocabulary before any WRITE-PRIVATE seam adopts
        is CXO-owned vocabulary work tracked on #1739. If this pin breaks
        because the vocabulary was tightened deliberately, update it WITH
        that decision's citation."""
        verdict = evaluate_acceptance(
            PM_ASIDE_1650,
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            armed_question=_AN_ASK,
        )
        assert verdict is AcceptanceVerdict.ACCEPT
        assert detect_offer_response(PM_ASIDE_1650) == "accept"  # parity with legacy

    def test_prose_shapes_pass(self):
        long_turn = "yes " * 80
        assert (
            evaluate_acceptance(
                long_turn,
                effect=EffectClass.READ,
                armed_question=_AN_ASK,
            )
            is AcceptanceVerdict.PASS
        )
        assert (
            evaluate_acceptance(
                "yes\nplease",
                effect=EffectClass.READ,
                armed_question=_AN_ASK,
            )
            is AcceptanceVerdict.PASS
        )


class TestTaughtVocabulary:
    """Seam-taught closing phrases: full-message only, LOW tier only."""

    def test_taught_phrase_accepts_full_message_only(self):
        kwargs = dict(
            effect=EffectClass.READ,
            armed_question=_AN_ASK,
            taught_accepts=("looks good", "done"),
        )
        assert evaluate_acceptance("Looks good", **kwargs) is AcceptanceVerdict.ACCEPT
        assert evaluate_acceptance("done.", **kwargs) is AcceptanceVerdict.ACCEPT
        # Containing ≠ being: the #1617 substring failure must not return.
        assert (
            evaluate_acceptance("add that the demo went good", **kwargs) is AcceptanceVerdict.PASS
        )

    def test_taught_vocabulary_never_loosens_the_strict_tier(self):
        assert (
            evaluate_acceptance(
                "looks good",
                effect=EffectClass.DESTRUCTIVE,
                armed_question=_AN_ASK,
                taught_accepts=("looks good",),
            )
            is AcceptanceVerdict.PASS
        )


# ---------------------------------------------------------------------------
# 2. The absorbed alias (unit)
# ---------------------------------------------------------------------------


class TestConfirmAliasAbsorbed:
    """``detect_confirm_response`` is a compatibility alias over the
    predicate. Its #1650 vocabulary is pinned by that issue's own suite;
    here we pin what the contract ADDS: question-forms never accept."""

    @pytest.mark.parametrize("question", [PM_STANDUP_QUESTION, "yes?", "sure?", "did it close?"])
    def test_question_forms_are_none_at_the_confirm_seam(self, question):
        assert detect_confirm_response(question) is None

    def test_crisp_forms_unchanged(self):
        assert detect_confirm_response("yes") == "accept"
        assert detect_confirm_response("no thanks") == "decline"
        assert detect_confirm_response(PM_ASIDE_1650) is None

    def test_legacy_unthreaded_sentinel_still_accepts(self):
        """The alias path predates ask-threading; it must keep #1650
        behavior (the ratchet tracks its callers as unadopted)."""
        assert (
            evaluate_acceptance(
                "yes",
                effect=EffectClass.DESTRUCTIVE,
                armed_question=LEGACY_UNTHREADED,
            )
            is AcceptanceVerdict.ACCEPT
        )

    def test_generic_detector_is_byte_identical_legacy(self):
        """Not-yet-adopted seams keep #1631 behavior unchanged — including
        the greedy prefix rows (the #1650 suite pins this too; restated here
        because the contract's adoption boundary depends on it)."""
        assert detect_offer_response("yes, that's right") == "accept"
        assert detect_offer_response(PM_ASIDE_1650) == "accept"  # the known hazard, unadopted


# ---------------------------------------------------------------------------
# 3. The adopted generic-offer-seam READ tier (end-to-end, real service)
# ---------------------------------------------------------------------------


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


_MEETING_ASK = "I could help set up a meeting. Want me to find a time?"


def _arm_meeting_offer(service, sid):
    """Arm the one registered READ-tier soft offer ("meeting") the way the
    arm site does since 2026-09-09 — rendered ask on the record (#1665)."""
    service.workflow_offer_service.set_pending_offer(
        sid,
        {
            "workflow_type": "meeting",
            "offer_message": _MEETING_ASK,
            "question": _MEETING_ASK,
            "decline_message": "No worries, just let me know if you change your mind.",
            "trigger_message": "we should sync up about the launch",
        },
    )


class TestReadTierOfferSeamEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_read_axes_are_declared(self):
        """The adoption's premise: the registry declares the axes the seam
        threads (never inferred from names — #1557/#1509)."""
        axes = declared_axes_for_workflow("meeting")
        assert axes == (EffectClass.READ, Outwardness.PRIVATE)

    async def test_state_question_rearms_the_offer_and_routes(self, live_service):
        """THE arm-survival pin (CXO: the arm is neither consumed nor
        silently dropped by a state question). A question-form against an
        armed READ offer re-arms it and falls through to normal processing —
        proven by the explosive LLM boundary being reached WITH the offer
        still armed afterward."""
        sid = "e2e-1739-question"
        _arm_meeting_offer(live_service, sid)
        try:
            await live_service.process_intent(
                message="what would that involve?", session_id=sid, user_id=_USER
            )
        except IntentProcessingError as exc:
            assert "LLM boundary touched" in str(exc) or "INTENT_CLASSIFICATION_FAILED" in str(
                exc
            ), str(exc)
        # The arm SURVIVED the pop: re-armed for the next turn.
        assert _pending_offers(live_service).get(sid) is not None
        assert _pending_offers(live_service)[sid]["question"] == _MEETING_ASK

    async def test_greedy_prefixed_question_no_longer_binds_as_accept(self, live_service):
        """Pre-adoption the generic row "^(?:yes|…),\\s" claimed "yes, what
        happened?" as an ACCEPT and dispatched the workflow. Adopted: it is
        a state question — nothing dispatches, the arm survives."""
        sid = "e2e-1739-greedy-question"
        _arm_meeting_offer(live_service, sid)
        try:
            await live_service.process_intent(
                message="yes, what happened?", session_id=sid, user_id=_USER
            )
        except IntentProcessingError as exc:
            assert "LLM boundary touched" in str(exc) or "INTENT_CLASSIFICATION_FAILED" in str(
                exc
            ), str(exc)
        assert _pending_offers(live_service).get(sid) is not None

    async def test_decline_still_cancels_honestly(self, live_service):
        sid = "e2e-1739-decline"
        _arm_meeting_offer(live_service, sid)
        result = await live_service.process_intent(
            message="no thanks", session_id=sid, user_id=_USER
        )
        assert "change your mind" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_bare_yes_still_dispatches(self, live_service):
        """#1694's direction: the bare affirmative must keep working at an
        adopted seam — acceptance dispatches the armed workflow."""
        sid = "e2e-1739-accept"
        _arm_meeting_offer(live_service, sid)
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        # The meeting workflow started (slot-filling conversation) — any
        # non-error reply with the offer consumed proves the dispatch.
        assert result.success
        assert _pending_offers(live_service).get(sid) is None
