"""#1509 TRUST-CONSENT — the unified consent gate (consent half of the one feature).

The four-lens ruling (jake-ftux-four-lens-synthesis-2026-07-31 §2, CXO's
pairing): HOST's consent gate makes the action safe AFTER intent forms;
capability legibility (test_capability_legibility_1509.py) makes it
discoverable WHILE intent forms. Ship together; one feature.

What these tests pin:
- ONE decision function (``consent_gate.decide_consent``) across the full
  EffectClass x framing x WorkingMode matrix — every cell asserted, with the
  denominator stated (the #1555 lesson: one decision, one implementation).
- The #1190 confirm tier and the #1510 collaborate tier are PROJECTIONS of
  that matrix, not parallel gates: ``gate_holds`` delegates to it, the rail's
  CONFIRM branch takes its verdict from it.
- The named boundary condition (#1509 AC-1) is effect-DERIVED: membership is
  the declared WorkflowEntry.effect, never a hand list of actions.
- The generalized gate does not confiscate imperatives: the extended
  execute-verb framing keeps every imperative WRITE phrasing executing.

Layer honesty (m-43): the end-to-end class drives the REAL
``IntentService.process_intent`` (the #1190/#1510 idiom), mocked ONLY at the
LLM boundary (explosive), the classification boundary where a deterministic
route to an ambiguous-framed WRITE action does not exist (stated per test),
and the persistence seam (the house in-memory users.preferences double).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import consent_gate as cg
from services.intent_service.classifier import IntentClassifier
from services.intent_service.collaboration_gate import (
    DRAFT_COLLABORATION_ACTIONS,
    FRAMING_AMBIGUOUS,
    FRAMING_COMPOSE,
    FRAMING_EXECUTE,
    WORKING_MODE_PREF_KEY,
    WorkingMode,
    classify_framing,
    detect_mode_declaration,
    gate_holds,
)
from services.intent_service.destructive_confirm import CONFIRM_PENDING_ACTION_WORKFLOW
from services.intent_service.verified_inference import (
    VerificationDecision,
    VerificationMetaMode,
)
from services.shared_types import EffectClass, IntentCategory

_USER = "3f7b8a52-1509-4b00-9e00-000000001509"

# An update-issue request with AMBIGUOUS framing: no verb-initial imperative,
# no compose marker. Ambiguity is the cell the declared mode decides.
AMBIGUOUS_UPDATE = "the title of issue #108 ought to say Q3 roadmap"
JAKE = "help me write a ticket about the login timeout on mobile"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM (house idiom)."""

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


# ---------------------------------------------------------------------------
# 1. THE decision matrix — every cell, denominator stated
# ---------------------------------------------------------------------------


class TestConsentDecisionMatrix:
    """decide_consent across the FULL matrix: 3 effects x 3 framings x
    2 modes = 18 cells; all 18 asserted below (m-44: this parametrize IS the
    denominator — if a framing, mode, or effect value is added, the
    completeness test underneath fails until the matrix here grows)."""

    CELLS = [
        # (effect, framing, mode, expected)
        # READ: never consent territory — 6 cells, all PROCEED.
        (EffectClass.READ, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (EffectClass.READ, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (EffectClass.READ, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (EffectClass.READ, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        # WRITE: compose always collaborates (executing a request for drafting
        # HELP is the Jake failure), execute framing IS consent, ambiguity is
        # decided by the declared mode — 6 cells.
        (EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.COLLABORATE),
        (EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        # DESTRUCTIVE: CONFIRM in every cell — framing and mode never weaken
        # the #1190 tier (execute-mode users still confirm) — 6 cells.
        (EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
    ]

    @pytest.mark.parametrize("effect,framing,mode,expected", CELLS)
    def test_cell(self, effect, framing, mode, expected):
        assert cg.decide_consent(effect, framing, mode) is expected

    def test_matrix_is_complete(self):
        """The denominator guard: the CELLS table covers the whole space.
        A new EffectClass tier, framing verdict, or WorkingMode fails here
        until its cells are ruled and added."""
        framings = {FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS}
        covered = {(e, f, m) for e, f, m, _ in self.CELLS}
        full = {
            (e, f, m)
            for e in EffectClass
            for f in framings
            for m in WorkingMode
        }
        assert covered == full, (
            f"matrix drift: {len(covered)}/{len(full)} cells covered — "
            "every new tier/framing/mode value needs its cells ruled here"
        )

    def test_only_one_cell_family_consults_the_mode(self):
        """The 'mode-tied, not per-verb' property: for every cell OUTSIDE
        WRITE x AMBIGUOUS, the two modes agree — the declared mode decides
        exactly the ambiguous-write cell."""
        framings = {FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS}
        for e in EffectClass:
            for f in framings:
                if e == EffectClass.WRITE and f == FRAMING_AMBIGUOUS:
                    continue
                assert cg.decide_consent(e, f, WorkingMode.COLLABORATE) is cg.decide_consent(
                    e, f, WorkingMode.EXECUTE
                )


# ---------------------------------------------------------------------------
# 2. The boundary condition is effect-DERIVED (AC-1: named, not per-call-site)
# ---------------------------------------------------------------------------


class TestEffectDerivedBoundary:
    def test_effect_lookup_reads_the_declared_registry_effect(self):
        assert cg.effect_for_action("list_issues_query") == EffectClass.READ
        assert cg.effect_for_action("create_ticket") == EffectClass.WRITE
        assert cg.effect_for_action("update_issue") == EffectClass.WRITE
        assert cg.effect_for_action("close_issue") == EffectClass.DESTRUCTIVE

    def test_unknown_action_has_no_effect_hence_no_derivation(self):
        assert cg.effect_for_action("no_such_action") is None
        assert cg.effect_for_action(None) is None
        assert cg.effect_for_action("") is None

    @pytest.mark.asyncio
    async def test_gate_holds_is_a_projection_of_the_unified_decision(self, monkeypatch):
        """#1555 proof obligation: gate_holds consults decide_consent — the
        collaborate tier has no second implementation. Poisoning the one
        function changes gate_holds' answer."""
        calls = {}

        def _poisoned(effect, framing, mode):
            calls["hit"] = (effect, framing)
            return cg.ConsentDecision.PROCEED  # inverted verdict on purpose

        monkeypatch.setattr(cg, "decide_consent", _poisoned)
        # Compose-framed create would hold under the real decision; with the
        # decision poisoned to PROCEED, gate_holds must follow it.
        assert await gate_holds("create_ticket", JAKE, _USER) is False
        assert calls["hit"][0] == EffectClass.WRITE

    @pytest.mark.asyncio
    async def test_gate_holds_now_covers_every_write_entry_not_a_hand_list(self):
        """The derivation swap the old GATED_WRITE_ACTIONS comment tracked:
        a WRITE rail action OUTSIDE the create family (update_issue) holds on
        compose framing — membership is the declared effect."""
        assert await gate_holds("update_issue", "help me update the ticket wording", _USER) is True

    @pytest.mark.asyncio
    async def test_destructive_actions_are_the_confirm_tiers_not_this_ones(self):
        """DESTRUCTIVE never collaborates here — decide_consent says CONFIRM
        and the #1190 rail gate owns that turn."""
        assert await gate_holds("close_issue", "help me close issue #9", _USER) is False

    def test_draft_collaboration_set_is_copy_selection_only(self):
        """The renamed set still names exactly the create family — and the
        semantics contract lives in its name: copy-surface selection, not
        gate membership (gate membership is the declared effect above)."""
        assert DRAFT_COLLABORATION_ACTIONS == frozenset(
            {
                "create_issue",
                "create_github_issue",
                "create_item",
                "create_ticket",
                "make_github_issue",
                "new_github_issue",
            }
        )


# ---------------------------------------------------------------------------
# 3. Framing generalization — imperatives across ALL write families
# ---------------------------------------------------------------------------


class TestFramingGeneralization:
    @pytest.mark.parametrize(
        "message",
        [
            # the phrasings the deterministic surfaces actually route (#1411/
            # B3/#1560/#1327) — every one must stay an un-gated imperative:
            "change the title of issue #108 to test new regressions",
            "change the title to Foo",
            "update the roadmap doc with the Q3 dates",
            "remind me at 3pm tomorrow to review the PR",
            "set my default repo to owner/name",
            "use owner/name as my default repo",
            "comment on issue #5 saying the fix shipped",
            "add a label to it",
            "please modify issue #12's title",
        ],
    )
    def test_imperative_write_phrasings_are_execute(self, message):
        assert classify_framing(message) == FRAMING_EXECUTE

    def test_verb_initial_imperative_with_compose_noun_is_execute(self):
        """The ordering fix: 'draft' as a NOUN inside a verb-initial
        imperative no longer reads compose — the anchored execute check
        runs first."""
        assert classify_framing("add the draft notes to the meeting doc") == FRAMING_EXECUTE

    @pytest.mark.parametrize(
        "message",
        [
            JAKE,
            "help me draft an issue for the checkout bug",
            "let's write a ticket about the flaky tests",
            "draft a ticket about slow dashboards",
            "can we update the roadmap together",
        ],
    )
    def test_compose_phrasings_survive_the_reorder(self, message):
        assert classify_framing(message) == FRAMING_COMPOSE

    @pytest.mark.parametrize(
        "message",
        [AMBIGUOUS_UPDATE, "I need a ticket for the login bug", ""],
    )
    def test_ambiguous_stays_ambiguous(self, message):
        assert classify_framing(message) == FRAMING_AMBIGUOUS


# ---------------------------------------------------------------------------
# 4. The consent-check offer (generic WRITE tier) — #1190 carrier reuse
# ---------------------------------------------------------------------------


def _update_intent(message=AMBIGUOUS_UPDATE):
    return Intent(
        category=IntentCategory.QUERY,
        action="update_issue",
        confidence=0.85,
        original_message=message,
        context={"original_message": message},
    )


class TestConsentCheckOffer:
    def test_offer_reuses_the_1190_carrier_and_acceptance_path(self):
        """No parallel store, no parallel acceptance: the check IS a
        confirm_pending_action offer — 'yes' re-dispatches the ORIGINAL
        intent through the existing entry point."""
        offer = cg.build_consent_check_offer(_update_intent(), EffectClass.WRITE)
        assert offer.offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        pa = offer.offer["pending_action"]
        assert pa["action"] == "update_issue"
        assert pa["intent"].original_message == AMBIGUOUS_UPDATE
        assert pa["kind"] == cg.CONSENT_CHECK_KIND

    def test_check_is_legible_names_action_effect_and_asks(self):
        """#1509 AC-5: the transcript shows a check happened — the copy names
        the action in plain words, states its effect tier (derived), and asks
        one clear question."""
        from services.intent_service.capability_legibility import describe_effect

        offer = cg.build_consent_check_offer(_update_intent(), EffectClass.WRITE)
        assert "update issue #108" in offer.question
        assert describe_effect(EffectClass.WRITE) in offer.question
        assert "(yes/no)" in offer.question

    def test_decline_copy_is_honest_cancel(self):
        offer = cg.build_consent_check_offer(_update_intent(), EffectClass.WRITE)
        assert "won't update issue #108" in offer.offer["decline_message"]
        assert "Nothing has been changed" in offer.offer["decline_message"]

    def test_taught_graduation_phrase_actually_routes(self):
        """#1571: never teach a phrase that doesn't route. The check copy
        teaches exactly one phrase, and the #1510 declaration surface catches
        it deterministically (layer: the deterministic declaration detector,
        which runs before any routing — the surface the phrase targets)."""
        offer = cg.build_consent_check_offer(_update_intent(), EffectClass.WRITE)
        taught = "just do things directly from now on"
        assert taught in offer.question
        assert detect_mode_declaration(taught) is WorkingMode.EXECUTE


# ---------------------------------------------------------------------------
# 5. PM 2026-08-13 ruling — effect-weighted verb-interpretation ask
# ---------------------------------------------------------------------------


class TestVerbInterpretation:
    """decide_verb_interpretation across the FULL space: 3 effects x 3 meta
    modes x 3 confidence bands (below suggestion floor / low / high) =
    27 cells, all asserted (denominator stated per m-44). Bands: 0.3 < 0.4
    (floor), 0.6 in [0.4, 0.9), 0.95 >= 0.9."""

    LOW, MID, HIGH = 0.3, 0.6, 0.95
    D = VerificationDecision
    M = VerificationMetaMode

    CELLS = [
        # Below the suggestion floor: DISCARD regardless (9 cells).
        *[
            (e, m, 0.3, VerificationDecision.DISCARD)
            for e in EffectClass
            for m in VerificationMetaMode
        ],
        # READ candidate: best-effort permitted ("wrong list != lost data")
        # unless the user explicitly said don't-assume (6 cells).
        (EffectClass.READ, M.DEFAULT, MID, D.AUTO_APPLY),
        (EffectClass.READ, M.DEFAULT, HIGH, D.AUTO_APPLY),
        (EffectClass.READ, M.TRUST_INFERENCES, MID, D.AUTO_APPLY),
        (EffectClass.READ, M.TRUST_INFERENCES, HIGH, D.AUTO_APPLY),
        (EffectClass.READ, M.ALWAYS_ASK, MID, D.READ_BACK),
        (EffectClass.READ, M.ALWAYS_ASK, HIGH, D.READ_BACK),
        # WRITE candidate: exactly the rail's ruled behavior (6 cells).
        (EffectClass.WRITE, M.DEFAULT, MID, D.READ_BACK),
        (EffectClass.WRITE, M.DEFAULT, HIGH, D.AUTO_APPLY),
        (EffectClass.WRITE, M.TRUST_INFERENCES, MID, D.AUTO_APPLY),
        (EffectClass.WRITE, M.TRUST_INFERENCES, HIGH, D.AUTO_APPLY),
        (EffectClass.WRITE, M.ALWAYS_ASK, MID, D.READ_BACK),
        (EffectClass.WRITE, M.ALWAYS_ASK, HIGH, D.READ_BACK),
        # DESTRUCTIVE candidate: a low-confidence destructive mapping always
        # asks — even "stop asking me" never lowers it (6 cells).
        (EffectClass.DESTRUCTIVE, M.DEFAULT, MID, D.READ_BACK),
        (EffectClass.DESTRUCTIVE, M.DEFAULT, HIGH, D.AUTO_APPLY),
        (EffectClass.DESTRUCTIVE, M.TRUST_INFERENCES, MID, D.READ_BACK),
        (EffectClass.DESTRUCTIVE, M.TRUST_INFERENCES, HIGH, D.AUTO_APPLY),
        (EffectClass.DESTRUCTIVE, M.ALWAYS_ASK, MID, D.READ_BACK),
        (EffectClass.DESTRUCTIVE, M.ALWAYS_ASK, HIGH, D.READ_BACK),
    ]

    @pytest.mark.parametrize("effect,meta,confidence,expected", CELLS)
    def test_cell(self, effect, meta, confidence, expected):
        assert cg.decide_verb_interpretation(confidence, effect, meta) is expected

    def test_space_is_complete(self):
        covered = {(e, m, c) for e, m, c, _ in self.CELLS}
        full = {
            (e, m, c)
            for e in EffectClass
            for m in VerificationMetaMode
            for c in (self.LOW, self.MID, self.HIGH)
        }
        assert covered == full

    def test_pm_ruling_headline_cell(self):
        """PM's own example shape ('clear my reminders'): an ambiguous verb
        whose candidate mapping is DESTRUCTIVE asks, never maps-by-decree —
        even for a user who said 'stop asking me every time'."""
        assert (
            cg.decide_verb_interpretation(
                0.6, EffectClass.DESTRUCTIVE, VerificationMetaMode.TRUST_INFERENCES
            )
            is VerificationDecision.READ_BACK
        )


# ---------------------------------------------------------------------------
# 6. End-to-end through the REAL process_intent
# ---------------------------------------------------------------------------


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


@pytest.fixture
def mem_prefs(monkeypatch):
    """House in-memory users.preferences double at the ONE persistence seam."""
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


def _stub_classifier(service, intent):
    """Classification-boundary stub, used ONLY where no deterministic surface
    emits the needed (action, framing) pair — stated per test (m-43). The
    LLM stays explosive underneath; this pins the post-classification rail."""
    multi = SimpleNamespace(
        is_multi_intent=False,
        intents=[intent],
        primary_intent=intent,
        has_greeting=False,
        has_substantive_intent=True,
        secondary_intents=[],
    )
    service.intent_classifier.classify_multiple = AsyncMock(return_value=multi)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestEndToEndConsentCheck:
    pytestmark = pytest.mark.asyncio

    async def test_ambiguous_write_is_held_with_a_legible_check(
        self, live_service, mem_prefs
    ):
        """An ambiguous-framed WRITE rail action does NOT execute on the turn
        it was classified: the handler is explosive, one check question comes
        back, the pending action is stored in the EXISTING #846 store.
        (Classifier stubbed: every deterministic WRITE surface is
        imperative-shaped by construction, so an ambiguous emission only
        arises from the LLM lane.)"""
        sid = "e2e-1509-hold"
        _stub_classifier(live_service, _update_intent())

        async def _explosive_handler(*a, **k):
            raise AssertionError("update handler reached — consent gate must hold")

        live_service._handle_update_issue = _explosive_handler

        result = await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("consent_check_pending") is True
        assert result.intent_data.get("consent_effect") == "write"
        assert result.requires_clarification is True
        assert "(yes/no)" in result.message
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["action"] == "update_issue"

    async def test_yes_executes_the_original_intent_unreclassified(
        self, live_service, mem_prefs
    ):
        from services.intent.intent_service import IntentProcessingResult

        sid = "e2e-1509-yes"
        _stub_classifier(live_service, _update_intent())
        holder = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Updated issue #108", intent_data={}
            )
        )
        live_service._handle_update_issue = holder

        await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        holder.assert_not_awaited()
        # The "yes" turn must not re-classify (the stub would be consulted
        # again — make it explosive instead).
        live_service.intent_classifier.classify_multiple = AsyncMock(
            side_effect=AssertionError("'yes' was re-classified")
        )
        result = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        holder.assert_awaited_once()
        dispatched_intent = holder.await_args.args[0]
        assert dispatched_intent.original_message == AMBIGUOUS_UPDATE
        assert "Updated issue #108" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_no_cancels_honestly_and_nothing_fires(
        self, live_service, mem_prefs
    ):
        sid = "e2e-1509-no"
        _stub_classifier(live_service, _update_intent())

        async def _explosive_handler(*a, **k):
            raise AssertionError("declined consent must never execute")

        live_service._handle_update_issue = _explosive_handler
        await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert "won't update issue #108" in result.message
        assert "Nothing has been changed" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_execute_mode_user_proceeds_on_the_same_ambiguity(
        self, live_service, mem_prefs
    ):
        """The declared working model decides the ambiguous cell: the same
        message from an execute-mode user dispatches directly (CXO decline
        property inverse: graduation is a declared setting, not friction)."""
        from services.intent.intent_service import IntentProcessingResult

        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        sid = "e2e-1509-execmode"
        _stub_classifier(live_service, _update_intent())
        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Updated issue #108", intent_data={}
            )
        )
        live_service._handle_update_issue = handler
        result = await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        handler.assert_awaited_once()
        assert _pending_offers(live_service).get(sid) is None
        assert "Updated issue #108" in result.message

    async def test_imperative_phrasing_never_checks_deterministic_route(
        self, live_service, mem_prefs
    ):
        """Zero-friction pin on the REAL deterministic route (no classifier
        stub): the #1411 explicit-issue-update sentence resolves at Stage 0
        and executes without a consent turn — the gate confiscates ambiguity,
        not imperatives."""
        from services.intent.intent_service import IntentProcessingResult

        sid = "e2e-1509-imperative"
        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Updated issue #108", intent_data={}
            )
        )
        live_service._handle_update_issue = handler
        await live_service.process_intent(
            message="change the title of issue #108 to test new regressions",
            session_id=sid,
            user_id=_USER,
        )
        handler.assert_awaited_once()
        assert _pending_offers(live_service).get(sid) is None

    async def test_jake_replay_through_the_rail_renders_draft_collaboration(
        self, live_service, mem_prefs, monkeypatch
    ):
        """#1509 AC-3 at the rail layer: the Jake shape classified as
        create_ticket falls through to the create handler's DRAFT copy (the
        richer #1510 surface — copy-surface selection, not a second gate),
        and no GitHub write fires (explosive router)."""
        sid = "e2e-1509-jake"
        jake_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.95,
            original_message=JAKE,
            context={"original_message": JAKE},
        )
        _stub_classifier(live_service, jake_intent)

        from services.integrations.github import github_integration_router as gh_mod

        class _ExplosiveRouter:
            def __init__(self, *a, **k):
                pass

            async def initialize(self, *a, **k):
                return None

            async def is_available(self):
                return True

            def __getattr__(self, name):
                raise AssertionError(f"GitHub router touched ({name}) on the Jake replay")

        monkeypatch.setattr(gh_mod, "GitHubIntegrationRouter", _ExplosiveRouter)

        result = await live_service.process_intent(
            message=JAKE, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("collaboration_gate") is True
        assert result.requires_clarification is True
        assert "login timeout on mobile" in result.message
        # Draft surface, not the generic check — and nothing pending: the
        # follow-up imperative routes as its own explicitly-framed turn.
        assert result.intent_data.get("consent_check_pending") is None
        assert _pending_offers(live_service).get(sid) is None

    async def test_destructive_confirm_tier_unchanged_through_unified_gate(
        self, live_service, mem_prefs
    ):
        """#1190 regression pin THROUGH the refactored seam: 'close issue
        #108' (real deterministic route) still defers with the yes/no
        confirmation — CONFIRM now arrives via decide_consent."""
        sid = "e2e-1509-destructive"
        result = await live_service.process_intent(
            message="close issue #108", session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert "(yes/no)" in result.message
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
