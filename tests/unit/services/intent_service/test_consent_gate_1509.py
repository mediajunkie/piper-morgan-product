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
from services.shared_types import EffectClass, IntentCategory, Outwardness

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
    """decide_consent across the FULL matrix: 2 outwardness x 3 effects x
    3 framings x 2 modes = 36 cells; all 36 asserted below (m-44: this
    parametrize IS the denominator — if an outwardness, framing, mode, or
    effect value is added, the completeness test underneath fails until the
    matrix here grows). The PRIVATE half is the pre-axis 18-cell matrix,
    cell-for-cell unchanged (the #1509 outwardness ratification's
    "PRIVATE behavior fully unchanged" regression pin)."""

    CELLS = [
        # (outwardness, effect, framing, mode, expected)
        # ── PRIVATE half: today's 18 cells, unchanged ─────────────────────
        # READ: never consent territory — 6 cells, all PROCEED.
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        # WRITE: compose always collaborates (executing a request for drafting
        # HELP is the Jake failure), execute framing IS consent, ambiguity is
        # decided by the declared mode — 6 cells.
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        # DESTRUCTIVE: CONFIRM in every cell — framing and mode never weaken
        # the #1190 tier (execute-mode users still confirm) — 6 cells.
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.PRIVATE, EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        # ── OUTWARD half (#1509 axis, ratified 2026-08-15) ────────────────
        # READ: PROCEED — an outward READ is unrepresentable by the scope
        # boundary (a communication act writes by definition); the cells
        # exist because the type space contains them — 6 cells.
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.READ, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED),
        # WRITE: collaborate/ambiguous cells check exactly as today; wherever
        # the DECLARED trust mode proceeds, it proceeds WITH the disclosure
        # (CXO's mechanism ruling: say it out loud, never a second
        # DESTRUCTIVE, never a silent pass) — 6 cells.
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.PROCEED),
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED_WITH_DISCLOSURE),
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.COLLABORATE),
        (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.PROCEED_WITH_DISCLOSURE),
        # DESTRUCTIVE: CONFIRM in every cell — outwardness never substitutes
        # for, weakens, or doubles the #1190 tier — 6 cells.
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_COMPOSE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_EXECUTE, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.COLLABORATE, cg.ConsentDecision.CONFIRM),
        (Outwardness.OUTWARD, EffectClass.DESTRUCTIVE, FRAMING_AMBIGUOUS, WorkingMode.EXECUTE, cg.ConsentDecision.CONFIRM),
    ]

    @pytest.mark.parametrize("outwardness,effect,framing,mode,expected", CELLS)
    def test_cell(self, outwardness, effect, framing, mode, expected):
        assert (
            cg.decide_consent(effect, framing, mode, outwardness=outwardness)
            is expected
        )

    def test_matrix_is_complete(self):
        """The denominator guard: the CELLS table covers the whole space.
        A new Outwardness value, EffectClass tier, framing verdict, or
        WorkingMode fails here until its cells are ruled and added."""
        framings = {FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS}
        covered = {(o, e, f, m) for o, e, f, m, _ in self.CELLS}
        full = {
            (o, e, f, m)
            for o in Outwardness
            for e in EffectClass
            for f in framings
            for m in WorkingMode
        }
        assert covered == full, (
            f"matrix drift: {len(covered)}/{len(full)} cells covered — "
            "every new axis/tier/framing/mode value needs its cells ruled here"
        )

    def test_private_default_reproduces_the_private_column(self):
        """The defaulted parameter IS the PRIVATE column: calling without
        outwardness (every pre-axis caller) answers identically to passing
        PRIVATE explicitly — the regression pin that makes the default safe."""
        framings = (FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS)
        for e in EffectClass:
            for f in framings:
                for m in WorkingMode:
                    assert cg.decide_consent(e, f, m) is cg.decide_consent(
                        e, f, m, outwardness=Outwardness.PRIVATE
                    )

    def test_mode_consulting_cells_are_exactly_the_ruled_three(self):
        """The 'mode-tied, not per-verb' property, extended for the axis:
        the cells where the two modes disagree are EXACTLY (1) PRIVATE
        WRITE x AMBIGUOUS (the original graduation cell), (2) OUTWARD
        WRITE x AMBIGUOUS, and (3) OUTWARD WRITE x EXECUTE framing (the
        disclosure hangs on the declared mode). Everywhere else the modes
        agree."""
        framings = (FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS)
        disagreeing = {
            (o, e, f)
            for o in Outwardness
            for e in EffectClass
            for f in framings
            if cg.decide_consent(e, f, WorkingMode.COLLABORATE, outwardness=o)
            is not cg.decide_consent(e, f, WorkingMode.EXECUTE, outwardness=o)
        }
        assert disagreeing == {
            (Outwardness.PRIVATE, EffectClass.WRITE, FRAMING_AMBIGUOUS),
            (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_AMBIGUOUS),
            (Outwardness.OUTWARD, EffectClass.WRITE, FRAMING_EXECUTE),
        }


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

        def _poisoned(effect, framing, mode, outwardness=Outwardness.PRIVATE):
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
# 2b. The outwardness axis (#1509, ratified PM + CXO + PPM 2026-08-15)
# ---------------------------------------------------------------------------


def _unique_action_entries():
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return get_action_workflows()


class TestOutwardnessAxis:
    """The second consent dimension: who else witnesses the action —
    membership pins (the CXO scope boundary applied to the live registry),
    lookup contract, and the doctrine properties the ratification made
    binding."""

    # CXO's scope boundary, applied: OUTWARD = the action IS a communication
    # act (files an issue, posts a comment — content lands in front of others
    # as a direct, immediate consequence). Conservative start per the
    # ratification: sends (Slack/email) would join here when such rail
    # actions exist (#1481 Slack hold is separate and stays).
    EXPECTED_OUTWARD_KEYS = {
        # create family (the Jake-incident action class):
        "create_issue",
        "create_github_issue",
        "create_item",
        "create_ticket",
        "make_github_issue",
        "new_github_issue",
        # comment family:
        "comment_issue",
        "add_comment",
        "comment_issue_query",
    }

    def test_outward_membership_is_exactly_the_communication_acts(self):
        """The whole-registry pin (m-44 denominator: EVERY action-triggered
        key classified, not a sample): the OUTWARD set is exactly the filed-
        issue + posted-comment families. A key drifting in here means the
        broad reading ("touches data someone could later see") is creeping —
        the reading CXO ruled out because it stops the dimension
        discriminating."""
        workflows = _unique_action_entries()
        outward = {
            key
            for key, entry in workflows.items()
            if entry.outwardness == Outwardness.OUTWARD
        }
        assert outward == self.EXPECTED_OUTWARD_KEYS
        # Denominator: the classification covered a real registry.
        assert len(workflows) >= 30

    def test_shared_state_writes_stay_private(self):
        """CXO's named non-examples, pinned: editing repo content, todos/
        reminders, own-preference writes are PRIVATE — nobody is being
        handed something right now."""
        workflows = _unique_action_entries()
        for key in ("update_issue", "update_document", "create_reminder", "set_default_repo"):
            assert workflows[key].outwardness == Outwardness.PRIVATE, key

    def test_ppm_boundary_case_close_reopen_destructive_and_private(self):
        """PPM's stress-tested boundary case, SETTLED — do not re-litigate:
        close/reopen stay DESTRUCTIVE (#1190 blast-radius) and are NOT
        reclassified OUTWARD; the effect axis already covers them. The two
        axes are jointly exhaustive over reasons for care, not redundant
        nets over the same actions."""
        workflows = _unique_action_entries()
        for key in ("close_issue", "reopen_issue"):
            assert workflows[key].effect == EffectClass.DESTRUCTIVE, key
            assert workflows[key].outwardness == Outwardness.PRIVATE, key

    def test_outwardness_lookup_reads_the_declared_registry_value(self):
        assert cg.outwardness_for_action("comment_issue") == Outwardness.OUTWARD
        assert cg.outwardness_for_action("create_ticket") == Outwardness.OUTWARD
        assert cg.outwardness_for_action("update_issue") == Outwardness.PRIVATE
        assert cg.outwardness_for_action("close_issue") == Outwardness.PRIVATE
        assert cg.outwardness_for_action("no_such_action") is None
        assert cg.outwardness_for_action(None) is None
        assert cg.outwardness_for_action("") is None

    # ── Doctrine (standing, inviolable — the ratification restated them) ──

    _STRENGTH = {
        cg.ConsentDecision.PROCEED: 0,
        cg.ConsentDecision.PROCEED_WITH_DISCLOSURE: 1,
        cg.ConsentDecision.COLLABORATE: 2,
        cg.ConsentDecision.CONFIRM: 3,
    }

    def test_doctrine_outward_is_never_weaker_than_private(self):
        """Across ALL 18 (effect, framing, mode) cells: the OUTWARD verdict
        is at least as careful as the PRIVATE verdict — the axis only ever
        ADDS care (disclosure), never removes any."""
        framings = (FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS)
        for e in EffectClass:
            for f in framings:
                for m in WorkingMode:
                    private = cg.decide_consent(e, f, m, outwardness=Outwardness.PRIVATE)
                    outward = cg.decide_consent(e, f, m, outwardness=Outwardness.OUTWARD)
                    assert self._STRENGTH[outward] >= self._STRENGTH[private], (
                        e, f, m, private, outward,
                    )

    def test_doctrine_destructive_confirms_in_every_outwardness_cell(self):
        """DESTRUCTIVE always confirms — outwardness (like framing and mode)
        never weakens the #1190 tier, and never doubles it either (the
        verdict is CONFIRM, not some outward-flavored second gate)."""
        framings = (FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS)
        for o in Outwardness:
            for f in framings:
                for m in WorkingMode:
                    assert (
                        cg.decide_consent(EffectClass.DESTRUCTIVE, f, m, outwardness=o)
                        is cg.ConsentDecision.CONFIRM
                    )

    def test_doctrine_no_mode_weakens_a_confirm_or_compose_tier(self):
        """Consent tier is never weakened by mode: any cell that CONFIRMs
        under the default mode CONFIRMs under the declared trust mode, and
        compose-framed writes COLLABORATE in both modes, in both outwardness
        columns (the declared mode graduates only the ruled ambiguity/
        disclosure cells, pinned exhaustively in the matrix class)."""
        framings = (FRAMING_COMPOSE, FRAMING_EXECUTE, FRAMING_AMBIGUOUS)
        for o in Outwardness:
            for e in EffectClass:
                for f in framings:
                    default_mode = cg.decide_consent(e, f, WorkingMode.COLLABORATE, outwardness=o)
                    trust_mode = cg.decide_consent(e, f, WorkingMode.EXECUTE, outwardness=o)
                    if default_mode is cg.ConsentDecision.CONFIRM:
                        assert trust_mode is cg.ConsentDecision.CONFIRM, (o, e, f)
            assert (
                cg.decide_consent(EffectClass.WRITE, FRAMING_COMPOSE, WorkingMode.EXECUTE, outwardness=o)
                is cg.ConsentDecision.COLLABORATE
            )

    # ── The disclosure line (what + to whom) ──────────────────────────────

    def test_disclosure_line_states_what_and_to_whom(self):
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue",
            confidence=0.85,
            original_message="issue #5 could use a note that the fix shipped",
            context={"original_message": "issue #5 could use a note that the fix shipped"},
        )
        line = cg.build_outward_disclosure(intent)
        assert "I'm about to comment issue #5" in line  # the WHAT
        assert "in front of other people" in line  # the TO WHOM
        assert "(yes/no)" not in line  # a disclosure, never a gate

    def test_disclosure_line_renders_repo_when_context_carries_one(self):
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue",
            confidence=0.85,
            original_message="issue #5 could use a note that the fix shipped",
            context={
                "original_message": "issue #5 could use a note that the fix shipped",
                "repository": "octo/widgets",
            },
        )
        assert "comment issue #5 in octo/widgets" in cg.build_outward_disclosure(intent)


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
        # Draft surface, not the generic consent check.
        assert result.intent_data.get("consent_check_pending") is None
        # #1571 (updated pin): the draft turn now ARMS the drafted-issue
        # binding — "file it as is" next turn files THIS draft. The property
        # this line used to pin ("the follow-up imperative routes as its own
        # explicitly-framed turn") still holds: an explicit imperative is
        # off-intent to the binding, and the pop abandons it before the turn
        # routes normally (pinned in test_drafted_issue_1571.py).
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == "drafted_issue"

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


# ---------------------------------------------------------------------------
# 7. End-to-end — the outwardness axis at the rail (#1509, 2026-08-15)
# ---------------------------------------------------------------------------

# An outward request with AMBIGUOUS framing: not verb-initial imperative, no
# compose marker — the cell the declared mode decides, on a communication act.
AMBIGUOUS_COMMENT = "issue #5 could use a note that the fix shipped"
IMPERATIVE_COMMENT = "comment on issue #5 saying the fix shipped"
DISCLOSURE_MARKER = "Heads up — I'm about to"


def _comment_intent(message=AMBIGUOUS_COMMENT):
    return Intent(
        category=IntentCategory.QUERY,
        action="comment_issue",
        confidence=0.9,
        original_message=message,
        context={"original_message": message},
    )


class TestEndToEndOutwardness:
    pytestmark = pytest.mark.asyncio

    async def test_outward_ambiguous_under_trust_mode_executes_with_disclosure(
        self, live_service, mem_prefs
    ):
        """THE headline cell (OUTWARD x WRITE x ambiguous x declared trust
        mode): the comment posts THIS turn — no hold, no yes/no — and the
        reply leads with the disclosure line stating what and to whom, ahead
        of the handler's own result. (Classifier stubbed: ambiguous-framed
        emissions only arise from the LLM lane, per the class-6 convention.)"""
        from services.intent.intent_service import IntentProcessingResult

        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        sid = "e2e-1509-outward-trust"
        _stub_classifier(live_service, _comment_intent())
        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Comment added to issue #5.", intent_data={}
            )
        )
        live_service._handle_comment_issue_query = handler

        result = await live_service.process_intent(
            message=AMBIGUOUS_COMMENT, session_id=sid, user_id=_USER
        )
        handler.assert_awaited_once()
        assert _pending_offers(live_service).get(sid) is None
        assert result.message.startswith(DISCLOSURE_MARKER)
        assert "I'm about to comment issue #5" in result.message
        assert "in front of other people" in result.message
        # The handler's own result still follows the disclosure.
        assert "Comment added to issue #5." in result.message
        # Transcript legibility flags (#1509 AC-5).
        assert result.intent_data.get("consent_disclosure") is True
        assert result.intent_data.get("consent_outwardness") == "outward"

    async def test_outward_ambiguous_under_default_mode_same_ask_as_today(
        self, live_service, mem_prefs
    ):
        """OUTWARD x WRITE x ambiguous x collaborate mode: exactly today's
        consent check — held turn, yes/no question, pending offer in the
        #846 store, handler untouched. The axis added a disclosure to trust
        mode; it changed NOTHING about the default mode's ask."""
        sid = "e2e-1509-outward-default"
        _stub_classifier(live_service, _comment_intent())

        async def _explosive_handler(*a, **k):
            raise AssertionError("outward ambiguous write must hold under default mode")

        live_service._handle_comment_issue_query = _explosive_handler

        result = await live_service.process_intent(
            message=AMBIGUOUS_COMMENT, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("consent_check_pending") is True
        assert "(yes/no)" in result.message
        assert DISCLOSURE_MARKER not in result.message
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["action"] == "comment_issue"

    async def test_outward_imperative_under_trust_mode_discloses(
        self, live_service, mem_prefs
    ):
        """OUTWARD x WRITE x execute framing x declared trust mode: proceeds
        (the imperative is consent — nothing is held) WITH the disclosure —
        CXO's 'under a declared TRUST mode, it still states what it's about
        to do and to whom' covers every outward write proceeding in trust
        mode; disclosure is not confirmation, so nothing re-confirms."""
        from services.intent.intent_service import IntentProcessingResult

        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        sid = "e2e-1509-outward-imp-trust"
        _stub_classifier(live_service, _comment_intent(IMPERATIVE_COMMENT))
        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Comment added to issue #5.", intent_data={}
            )
        )
        live_service._handle_comment_issue_query = handler

        result = await live_service.process_intent(
            message=IMPERATIVE_COMMENT, session_id=sid, user_id=_USER
        )
        handler.assert_awaited_once()
        assert _pending_offers(live_service).get(sid) is None
        assert DISCLOSURE_MARKER in result.message
        assert result.intent_data.get("consent_disclosure") is True

    async def test_outward_imperative_under_default_mode_executes_plain(
        self, live_service, mem_prefs
    ):
        """OUTWARD x WRITE x execute framing x collaborate mode: same as
        today — the imperative executes with no check AND no disclosure (the
        user themselves said the act out loud this turn; the disclosure
        discipline attaches to the declared trust mode)."""
        from services.intent.intent_service import IntentProcessingResult

        sid = "e2e-1509-outward-imp-default"
        _stub_classifier(live_service, _comment_intent(IMPERATIVE_COMMENT))
        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Comment added to issue #5.", intent_data={}
            )
        )
        live_service._handle_comment_issue_query = handler

        result = await live_service.process_intent(
            message=IMPERATIVE_COMMENT, session_id=sid, user_id=_USER
        )
        handler.assert_awaited_once()
        assert _pending_offers(live_service).get(sid) is None
        assert DISCLOSURE_MARKER not in result.message
        assert result.intent_data.get("consent_disclosure") is None

    async def test_private_write_under_trust_mode_never_discloses(
        self, live_service, mem_prefs
    ):
        """PRIVATE regression pin: the same trust-mode ambiguous cell on a
        PRIVATE write (update_issue — repo-content editing, CXO's named
        non-example) proceeds exactly as before the axis: no check, no
        disclosure, no flags."""
        from services.intent.intent_service import IntentProcessingResult

        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        sid = "e2e-1509-private-trust"
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
        assert DISCLOSURE_MARKER not in result.message
        assert result.intent_data.get("consent_disclosure") is None
        assert result.intent_data.get("consent_outwardness") is None

    async def test_decline_memory_never_lowers_the_gate(
        self, live_service, mem_prefs
    ):
        """Standing doctrine, restated by the ratification: declining a
        consent check never suppresses the NEXT check — the identical
        outward-ambiguous request is checked again in full (consent is
        per-action-instance; decline memory suppresses preference re-asks,
        never safety gates)."""
        sid = "e2e-1509-decline-rearm"
        _stub_classifier(live_service, _comment_intent())

        async def _explosive_handler(*a, **k):
            raise AssertionError("declined-then-repeated request must never execute unchecked")

        live_service._handle_comment_issue_query = _explosive_handler

        first = await live_service.process_intent(
            message=AMBIGUOUS_COMMENT, session_id=sid, user_id=_USER
        )
        assert first.intent_data.get("consent_check_pending") is True
        declined = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert "Nothing has been changed" in declined.message
        assert _pending_offers(live_service).get(sid) is None
        # The identical request again: checked again, not remembered-declined
        # into silence, and NOT executed.
        _stub_classifier(live_service, _comment_intent())
        second = await live_service.process_intent(
            message=AMBIGUOUS_COMMENT, session_id=sid, user_id=_USER
        )
        assert second.intent_data.get("consent_check_pending") is True
        assert _pending_offers(live_service).get(sid) is not None
