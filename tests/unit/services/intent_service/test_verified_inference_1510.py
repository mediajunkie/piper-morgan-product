"""#1510 (inferred half) — the shared verified-inference preference mechanism.

PM ruling (relayed by Exec 2026-08-13, recorded on #1510): low trust-gradient
inference → read back for verification; once verified → STORED, not
re-inferred; meta-feedback about the verification process ("stop asking me
every time", "don't make assumptions") is a DISTINCT steering signal with its
own handling.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` (the #1190/#1411 idiom), mocked ONLY at the
LLM boundary (explosive — every verification turn must resolve
deterministically at the pending-offer seam) and the PERSISTENCE seam
(``collaboration_gate._load_preferences`` / ``_save_preference`` replaced by
an in-memory users.preferences double — the real-Postgres half lives in
``tests/integration/test_verified_inference_persistence_1510.py``).
"""

import pytest

from services.intent.intent_service import IntentService
from services.intent_service import verified_inference as vi
from services.intent_service.classifier import IntentClassifier
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_verify_inference_workflow,
)
from services.personality.preference_detection import (
    AUTO_APPLY_THRESHOLD,
    SUGGESTION_THRESHOLD,
)
from services.shared_types import EffectClass

_USER = "3f7b8a52-1510-4b00-9e00-000000001510"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically (the pending-offer seam runs
    before classification)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1510 verification turns must "
            "resolve deterministically at the pending-offer seam"
        )


@pytest.fixture(autouse=True)
def _clean_session_declines():
    vi._SESSION_DECLINES.clear()
    yield
    vi._SESSION_DECLINES.clear()


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double patched at the ONE persistence seam
    (collaboration_gate) — verified_inference imports the seam at call time,
    so patching the module attributes covers every path."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if str(user_id) not in store:
            return False  # mirrors the real seam: absent user row → False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


# ---------------------------------------------------------------------------
# The confidence gate (EXTENDS preference_detection's — one scoring system)
# ---------------------------------------------------------------------------


class TestDecisionGate:
    def test_thresholds_are_preference_detections(self):
        """The ruling's shape: extend the existing confidence_score gate, no
        parallel scoring system. The mechanism's cuts ARE the hoisted
        preference_detection constants."""
        assert AUTO_APPLY_THRESHOLD == 0.9
        assert SUGGESTION_THRESHOLD == 0.4

    def test_high_confidence_no_read_back(self):
        """Required AC: high-confidence → no read-back."""
        assert vi.decide(0.95) is vi.VerificationDecision.AUTO_APPLY
        assert vi.decide(AUTO_APPLY_THRESHOLD) is vi.VerificationDecision.AUTO_APPLY

    def test_low_confidence_reads_back(self):
        """Required AC: low-confidence → read-back (the ruled behavior)."""
        assert vi.decide(0.6) is vi.VerificationDecision.READ_BACK
        assert vi.decide(SUGGESTION_THRESHOLD) is vi.VerificationDecision.READ_BACK

    def test_below_suggestion_floor_discards_in_every_mode(self):
        """Too weak to surface at all (is_ready_for_suggestion's floor) —
        mode-independent: the floor is a property of the inference, not of
        the process preference."""
        for mode in vi.VerificationMetaMode:
            assert vi.decide(0.39, mode) is vi.VerificationDecision.DISCARD

    def test_trust_mode_auto_applies_low_confidence(self):
        """Required AC (second half): after "stop asking me every time",
        subsequent low-confidence inferences auto-apply."""
        assert (
            vi.decide(0.5, vi.VerificationMetaMode.TRUST_INFERENCES)
            is vi.VerificationDecision.AUTO_APPLY
        )

    def test_always_ask_mode_reads_back_even_high_confidence(self):
        assert (
            vi.decide(0.95, vi.VerificationMetaMode.ALWAYS_ASK)
            is vi.VerificationDecision.READ_BACK
        )

    def test_is_low_confidence_resurrected_trigger(self):
        assert vi.is_low_confidence(0.89) is True
        assert vi.is_low_confidence(0.9) is False

    def test_standup_preference_delegates_to_shared_gate(self):
        """#1591's consumer hook: the resurrected
        UserStandupPreference.is_low_confidence() asks THIS gate, not a
        second threshold."""
        from services.standup.preference_models import UserStandupPreference

        low = UserStandupPreference(user_id=_USER, key="format", value="brief", confidence=0.7)
        high = UserStandupPreference(user_id=_USER, key="format", value="brief", confidence=0.95)
        assert low.is_low_confidence() is True
        assert high.is_low_confidence() is False


# ---------------------------------------------------------------------------
# Meta-feedback detection (the DISTINCT channel)
# ---------------------------------------------------------------------------


class TestMetaFeedbackDetection:
    @pytest.mark.parametrize(
        "message",
        [
            "stop asking me every time",
            "Stop asking!",
            "don't ask, just do it",
            "quit asking me about this",
            "no need to check with me",
            "just go with it",
        ],
    )
    def test_trust_phrasings(self, message):
        assert vi.detect_meta_feedback(message) is vi.VerificationMetaMode.TRUST_INFERENCES

    @pytest.mark.parametrize(
        "message",
        [
            "don't make assumptions",
            "stop assuming things about my workflow",
            "please always check with me",
            "ask me every time",
            "no assumptions please",
        ],
    )
    def test_always_ask_phrasings(self, message):
        assert vi.detect_meta_feedback(message) is vi.VerificationMetaMode.ALWAYS_ASK

    @pytest.mark.parametrize(
        "message",
        ["yes", "no", "yes that's right", "close issue #108", "what about standups?", ""],
    )
    def test_non_meta_messages(self, message):
        assert vi.detect_meta_feedback(message) is None

    def test_mode_declaration_surface_does_not_claim_meta_phrasings(self):
        """The #1510 DECLARED surface (durative-marker working-mode
        declarations) and this meta channel stay distinct: the canonical meta
        phrasings carry no durative marker, so detect_mode_declaration must
        not intercept them upstream of the pending-offer seam."""
        from services.intent_service.collaboration_gate import detect_mode_declaration

        assert detect_mode_declaration("stop asking me every time") is None
        assert detect_mode_declaration("don't make assumptions") is None


# ---------------------------------------------------------------------------
# Read-back offer building (the #846/#1190 carrier — no parallel store)
# ---------------------------------------------------------------------------


class TestReadBackOffer:
    def test_offer_carries_the_documented_shape(self):
        offer = vi.build_read_back_offer(
            _USER,
            "standup_format",
            "brief",
            "that you want brief standups",
            confidence=0.6,
            session_id="sess-1",
        )
        assert offer is not None
        assert "that you want brief standups" in offer.question
        assert "(yes/no)" in offer.question
        record = offer.offer
        assert record["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
        pa = record["pending_action"]
        assert pa["kind"] == vi.VERIFY_INFERENCE_KIND
        assert pa["user_id"] == _USER
        assert pa["inference_key"] == "standup_format"
        assert pa["inference_value"] == "brief"
        assert pa["confidence"] == 0.6
        assert "won't assume" in record["decline_message"]

    def test_declined_key_is_not_reoffered_same_session(self):
        """Required AC: declined → not re-asked in the same session (the
        mechanism enforces it; consumers can't nag by accident)."""
        vi.mark_declined("sess-1", "standup_format")
        assert (
            vi.build_read_back_offer(
                _USER, "standup_format", "brief", "that you want brief standups",
                session_id="sess-1",
            )
            is None
        )

    def test_decline_memory_is_session_scoped(self):
        vi.mark_declined("sess-1", "standup_format")
        assert (
            vi.build_read_back_offer(
                _USER, "standup_format", "brief", "that you want brief standups",
                session_id="sess-2",
            )
            is not None
        )

    def test_registered_offer_only_write_entry(self):
        """The workflow entry: registered, WRITE (explicit + defaultless per
        #1557), and rail-unreachable (action_triggered=False) — a classifier
        emission can never store a preference."""
        register_default_workflows()
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        entry = WORKFLOW_REGISTRY[vi.VERIFY_INFERENCE_WORKFLOW]
        assert entry.effect == EffectClass.WRITE
        assert entry.needs_consent is True  # #1509's derivation, ready for its consumer
        assert vi.VERIFY_INFERENCE_WORKFLOW not in get_action_workflows()


# ---------------------------------------------------------------------------
# Acceptance entry point (unit)
# ---------------------------------------------------------------------------


class TestVerifyInferenceEntryPoint:
    pytestmark = pytest.mark.asyncio

    async def test_accept_stores_with_user_verified_provenance(self, mem_prefs):
        offer = vi.build_read_back_offer(
            _USER, "standup_format", "brief", "that you want brief standups", confidence=0.6
        )
        result = await run_verify_inference_workflow(
            session_id="s",
            user_id=_USER,
            context={"pending_action": offer.offer["pending_action"]},
        )
        assert result["intent_data"]["verified"] is True
        assert result["intent_data"]["persisted"] is True
        stored = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY]["standup_format"]
        assert stored["value"] == "brief"
        assert stored["source"] == vi.SOURCE_USER_VERIFIED
        assert stored["confidence_at_verification"] == 0.6
        assert stored["verified_at"]  # provenance timestamp present

    async def test_stored_value_is_read_back_not_reinferred(self, mem_prefs):
        """Required AC: verified → stored; the second turn READS THE STORE
        (get_verified_inference hit) instead of re-inferring."""
        offer = vi.build_read_back_offer(
            _USER, "standup_format", "brief", "that you want brief standups", confidence=0.6
        )
        await run_verify_inference_workflow(
            session_id="s", user_id=_USER,
            context={"pending_action": offer.offer["pending_action"]},
        )
        record = await vi.get_verified_inference(_USER, "standup_format")
        assert record is not None and record["value"] == "brief"

    async def test_persistence_failure_is_honest(self, mem_prefs):
        mem_prefs.pop(_USER)  # no user row → seam returns False
        offer = vi.build_read_back_offer(
            _USER, "standup_format", "brief", "that you want brief standups"
        )
        result = await run_verify_inference_workflow(
            session_id="s", user_id=_USER,
            context={"pending_action": offer.offer["pending_action"]},
        )
        assert result["intent_data"]["persisted"] is False
        assert "couldn't save" in result["message"]

    async def test_principal_mismatch_never_writes(self, mem_prefs):
        """#1532: the offer was built for user A; the accepting turn is user
        B — nothing lands in either store."""
        offer = vi.build_read_back_offer(
            _USER, "standup_format", "brief", "that you want brief standups"
        )
        other = "9f7b8a52-1532-4b00-9e00-000000001532"
        mem_prefs[other] = {}
        result = await run_verify_inference_workflow(
            session_id="s", user_id=other,
            context={"pending_action": offer.offer["pending_action"]},
        )
        assert result["intent_data"].get("principal_mismatch") is True
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[other]
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]

    async def test_foreign_or_missing_payload_returns_none(self):
        assert await run_verify_inference_workflow(session_id="s", context={}) is None
        assert (
            await run_verify_inference_workflow(
                session_id="s",
                context={"pending_action": {"action": "close_issue", "kind": None}},
            )
            is None
        )


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent (#1190/#1411 idiom)
# ---------------------------------------------------------------------------


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _arm_read_back(service, sid, key="standup_format", value="brief",
                   description="that you want brief standups", confidence=0.6):
    """Simulate the consumer's move (the consumers themselves are #1591/#1509
    scope): build the read-back and store it in the EXISTING #846 pending-offer
    store, exactly as a consumer would."""
    offer = vi.build_read_back_offer(
        _USER, key, value, description, confidence=confidence, session_id=sid
    )
    assert offer is not None
    service.workflow_offer_service.set_pending_offer(sid, offer.offer, user_id=_USER)
    return offer


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestEndToEndVerificationTurn:
    pytestmark = pytest.mark.asyncio

    async def test_yes_stores_the_inference(self, live_service, mem_prefs):
        sid = "e2e-1510-yes"
        _arm_read_back(live_service, sid)
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.success is True
        assert result.intent_data["verified"] is True
        stored = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY]["standup_format"]
        assert stored["value"] == "brief"
        assert stored["source"] == vi.SOURCE_USER_VERIFIED
        assert _pending_offers(live_service).get(sid) is None  # consumed

    async def test_no_discards_without_storing_and_without_reask(
        self, live_service, mem_prefs
    ):
        """Required AC: declined → not stored, not re-asked same session."""
        sid = "e2e-1510-no"
        _arm_read_back(live_service, sid)
        result = await live_service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "won't assume" in result.message
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        # The mechanism refuses to rebuild the same read-back this session:
        assert (
            vi.build_read_back_offer(
                _USER, "standup_format", "brief", "that you want brief standups",
                session_id=sid,
            )
            is None
        )

    async def test_stop_asking_me_every_time_full_meta_flow(
        self, live_service, mem_prefs
    ):
        """Required AC (verbatim scenario): meta-feedback on a verification
        turn → (a) the meta-preference is VISIBLE IN THE STORE under its own
        key, (b) subsequent low-confidence inferences auto-apply, (c) the
        current inference is applied (meta_auto provenance — "stop asking"
        while being asked means "go with it")."""
        sid = "e2e-1510-meta"
        _arm_read_back(live_service, sid)
        result = await live_service.process_intent(
            message="stop asking me every time", session_id=sid, user_id=_USER
        )
        assert result.intent_data["meta_mode"] == "trust_inferences"
        # (a) distinct signal, own key, visible in the store:
        meta = mem_prefs[_USER][vi.VERIFICATION_META_PREF_KEY]
        assert meta["mode"] == "trust_inferences"
        assert vi.VERIFICATION_META_PREF_KEY != vi.VERIFIED_INFERENCES_PREF_KEY
        # (b) subsequent low-confidence inferences auto-apply:
        mode = await vi.get_meta_mode(_USER)
        assert vi.decide(0.5, mode) is vi.VerificationDecision.AUTO_APPLY
        # (c) the current inference rode along, with distinct provenance:
        stored = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY]["standup_format"]
        assert stored["source"] == vi.SOURCE_META_AUTO

    async def test_no_stop_asking_declines_current_but_sets_meta(
        self, live_service, mem_prefs
    ):
        """Co-occurrence: "no, stop asking me every time" = decline THIS
        inference AND steer the process — the two signals are handled as the
        two signals they are."""
        sid = "e2e-1510-meta-no"
        _arm_read_back(live_service, sid)
        await live_service.process_intent(
            message="no, stop asking me every time", session_id=sid, user_id=_USER
        )
        assert mem_prefs[_USER][vi.VERIFICATION_META_PREF_KEY]["mode"] == "trust_inferences"
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        assert vi.was_declined(sid, "standup_format") is True

    async def test_dont_make_assumptions_raises_the_gate(
        self, live_service, mem_prefs
    ):
        sid = "e2e-1510-meta-ask"
        _arm_read_back(live_service, sid)
        result = await live_service.process_intent(
            message="don't make assumptions", session_id=sid, user_id=_USER
        )
        assert result.intent_data["meta_mode"] == "always_ask"
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        mode = await vi.get_meta_mode(_USER)
        assert vi.decide(0.95, mode) is vi.VerificationDecision.READ_BACK

    async def test_bare_cancel_declines_via_exit_tier(self, live_service, mem_prefs):
        """The #1529 exit tier rides the shared pending_action carrier: a bare
        'cancel' on a verification turn declines honestly (nothing stored,
        session decline memo set)."""
        sid = "e2e-1510-cancel"
        _arm_read_back(live_service, sid)
        result = await live_service.process_intent(
            message="cancel", session_id=sid, user_id=_USER
        )
        assert "won't assume" in result.message
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        assert vi.was_declined(sid, "standup_format") is True
