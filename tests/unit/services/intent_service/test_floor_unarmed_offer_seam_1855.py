"""#1855 — the floor never ASKS what it hasn't ARMED.

PM live, 2026-09-23, twice: the floor composed *"Want me to add 'One Job' with
the Design-in-Product/one-job repo to your projects now?"*, PM answered
*"Yes, please."*, and nothing was armed — so the bare affirmative had nothing to
bind to and the honest no-result fallback fired. The acceptance predicate's
exactly-armed rule (#1694 (b)) is the correct half; the OFFER was the lie.

Layer 1 (this file): enforcement at the floor's single output seam. The floor's
LLM prose is the one producer of offers that touches neither arming rail, so an
offer-shaped question it composes is rewritten into an imperative suggestion and
logged for #1595's corpus lane. Layer 2 (real arming) is deliberately not here.

Layer honesty (m-43): the ``respond()``-level tests drive ``ConversationalFloor``
with a STUBBED LLM client and a static system-prompt base. They measure the
RENDERER SEAM — what reaches user copy given a model output — not a live model,
not the full dispatch chain. The detector tests are pure functions.
"""

import re
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.acceptance import AcceptanceVerdict, evaluate_acceptance
from services.intent_service.conversation_context import LastOffer
from services.intent_service.conversational_floor import ConversationalFloor, FloorContext
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.unarmed_offer import (
    ADD_PROJECT_IMPERATIVE,
    detect_offer_questions,
    enforce_armed_offers,
    rewrite_offer_sentence,
)
from services.shared_types import EffectClass

# PM's verbatim transcript turn (issue #1855).
PM_OFFER = "Want me to add 'One Job' with the Design-in-Product/one-job repo to your projects now?"
PM_REPLY = "I found the repo. " + PM_OFFER
PM_EXPECTED_COMMAND = "add project One Job with repo Design-in-Product/one-job"


# ---------------------------------------------------------------------------
# (a) The detector
# ---------------------------------------------------------------------------


class TestOfferQuestionDetector:
    """Narrow, anchored, literal — the `TestUnarmedAskSiteRatchet` discipline."""

    @pytest.mark.parametrize(
        "sentence",
        [
            "Want me to file that issue?",
            "Would you like me to file that issue?",
            "Should I file that issue?",
            "Shall I file that issue?",
            # Case and whitespace are not the discriminator.
            "want me to   file that issue?",
            "SHOULD I file that issue?",
            PM_OFFER,
        ],
    )
    def test_every_phrasing_in_the_family_matches(self, sentence):
        found = detect_offer_questions(sentence)
        assert len(found) == 1, f"family member not detected: {sentence!r}"
        assert found[0].sentence == sentence

    @pytest.mark.parametrize(
        "sentence",
        [
            # Imperative suggestions — the form the rewrite PRODUCES. If these
            # matched, the enforcement would chew its own output.
            "To do that, say: add project One Job with repo owner/name.",
            "Say the word and I'll pull the rest.",
            "Add project One Job with repo Design-in-Product/one-job.",
            # Non-offer questions.
            "What's the repo?",
            "Which project did you mean?",
            "Did that work?",
            "How would you like to handle it?",
            # Offer vocabulary WITHOUT the question — a statement, not an ask.
            "Want me to know: I can add projects.",
            "I should file that issue.",
            # Offer vocabulary not at a sentence start (deliberately uncovered;
            # narrowness is the ratified design, not an oversight).
            "Let me know if you want me to file that issue.",
            # Empty / trivial.
            "",
            "?",
        ],
    )
    def test_non_offers_do_not_match(self, sentence):
        assert detect_offer_questions(sentence) == []

    def test_finds_the_offer_inside_a_longer_reply(self):
        found = detect_offer_questions(PM_REPLY)
        assert len(found) == 1
        assert found[0].sentence == PM_OFFER
        assert found[0].predicate.startswith("add 'One Job'")
        assert PM_REPLY[found[0].start : found[0].end] == PM_OFFER

    def test_finds_multiple_offers(self):
        text = "Should I file it? I can also tag it. Want me to add the label?"
        found = detect_offer_questions(text)
        assert [f.sentence for f in found] == [
            "Should I file it?",
            "Want me to add the label?",
        ]

    def test_markdown_bullet_lead_does_not_hide_an_offer(self):
        found = detect_offer_questions("Options:\n- Want me to file that issue?\n")
        assert len(found) == 1
        assert found[0].sentence == "Want me to file that issue?"

    def test_dot_inside_a_token_does_not_saw_the_sentence(self):
        """`docs/README.md` must not split the sentence before its `?`."""
        found = detect_offer_questions("Want me to open docs/README.md for you?")
        assert len(found) == 1


# ---------------------------------------------------------------------------
# The rewrite rule
# ---------------------------------------------------------------------------


class TestRewriteRule:
    def test_pm_fixture_binds_the_real_command(self):
        found = detect_offer_questions(PM_OFFER)
        assert rewrite_offer_sentence(found[0].predicate) == (
            f"To do that, say: {PM_EXPECTED_COMMAND}."
        )

    def test_unquoted_name_degrades_to_the_bracket_template_not_a_guess(self):
        """No quoted name → we do not invent one; the app's own template stands."""
        found = detect_offer_questions("Want me to add that project for you?")
        out = rewrite_offer_sentence(found[0].predicate)
        assert out == f"To do that, say: {ADD_PROJECT_IMPERATIVE}."

    def test_uncatalogued_action_names_the_action_and_asks_nothing(self):
        found = detect_offer_questions("Should I dig into the release notes?")
        out = rewrite_offer_sentence(found[0].predicate)
        assert out == "If you'd like me to dig into the release notes, just tell me directly."
        assert "?" not in out

    def test_no_tier_ever_produces_a_yes_no_question(self):
        for sentence in (
            PM_OFFER,
            "Want me to add that project for you?",
            "Should I dig into the release notes?",
        ):
            found = detect_offer_questions(sentence)
            out = rewrite_offer_sentence(found[0].predicate)
            assert detect_offer_questions(out) == [], out
            assert out.strip(), "a rewrite is never a bare deletion"

    def test_bracket_template_matches_1856s_canonical_copy_byte_for_byte(self):
        """Drift between the two copies of the one-liner must be loud."""
        from services.intent_service.canonical_handlers import CanonicalHandlers

        assert ADD_PROJECT_IMPERATIVE == CanonicalHandlers._ADD_PROJECT_IMPERATIVE

    def test_suggested_command_round_trips_through_the_real_1856_extractor(self):
        """We never suggest a phrasing the real extractor cannot parse (#1108)."""
        from services.onboarding.portfolio_service import extract_add_project_slots

        slots = extract_add_project_slots(PM_EXPECTED_COMMAND)
        assert slots == {"name": "One Job", "repo": "Design-in-Product/one-job"}


# ---------------------------------------------------------------------------
# enforce_armed_offers — the armed/unarmed decision
# ---------------------------------------------------------------------------


class TestEnforcementGate:
    def test_unarmed_offer_is_rewritten(self):
        out, n = enforce_armed_offers(PM_REPLY, armed_offer=None)
        assert n == 1
        assert PM_OFFER not in out
        assert f"To do that, say: {PM_EXPECTED_COMMAND}." in out
        assert out.startswith("I found the repo. ")

    @pytest.mark.parametrize("rail", ["workflow_offer", "last_offer", "interview_offer"])
    def test_armed_offer_passes_through_byte_for_byte(self, rail):
        out, n = enforce_armed_offers(PM_REPLY, armed_offer=rail)
        assert (out, n) == (PM_REPLY, 0)

    def test_text_without_offers_is_untouched(self):
        text = "Your todo list has no pending items. What's the repo?"
        assert enforce_armed_offers(text, armed_offer=None) == (text, 0)

    def test_empty_text_safe(self):
        assert enforce_armed_offers("", armed_offer=None) == ("", 0)

    def test_every_rewrite_is_logged_with_the_original_sentence(self):
        """#1595's corpus lane must see each instance, not the rewrite only."""
        from structlog.testing import capture_logs

        with capture_logs() as events:
            enforce_armed_offers(PM_REPLY, armed_offer=None, session_id="s1855")

        rewrites = [e for e in events if e.get("event") == "floor_unarmed_offer_rewritten"]
        assert len(rewrites) == 1
        assert rewrites[0]["original_sentence"] == PM_OFFER
        assert rewrites[0]["session_id"] == "s1855"
        assert PM_EXPECTED_COMMAND in rewrites[0]["rewritten_sentence"]


# ---------------------------------------------------------------------------
# (b) The seam — respond()
# ---------------------------------------------------------------------------


def _floor_returning(text):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(
        llm_client=llm,
        system_prompt_base="You are Piper Morgan (test base).",
    )


class TestFloorOutputSeam:
    """RED before #1855: respond() returned the model's offer verbatim."""

    @pytest.mark.asyncio
    async def test_unarmed_offer_never_reaches_user_copy(self):
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(
            FloorContext(user_message="what's in Design-in-Product?", session_id="s1855")
        )
        assert PM_OFFER not in resp.message
        assert f"To do that, say: {PM_EXPECTED_COMMAND}." in resp.message

    @pytest.mark.asyncio
    async def test_workflow_offer_armed_passes_untouched(self):
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(
            FloorContext(
                user_message="what's in Design-in-Product?",
                session_id="s1855",
                armed_offer="workflow_offer",
            )
        )
        assert resp.message == PM_REPLY

    @pytest.mark.asyncio
    async def test_standup_interview_offer_armed_passes_untouched(self):
        """The one offer that IS armed today (#1837) keeps its question."""
        interview = "Want me to walk you through your standup instead?"
        floor = _floor_returning(interview)
        resp = await floor.respond(
            FloorContext(
                user_message="standup",
                session_id="s1855",
                armed_offer="interview_offer",
            )
        )
        assert resp.message == interview

    @pytest.mark.asyncio
    async def test_unset_armed_offer_is_fail_safe_not_fail_open(self):
        """A door that states nothing is treated as unarmed, never as armed."""
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(FloorContext(user_message="hi", session_id="s1855"))
        assert PM_OFFER not in resp.message


# ---------------------------------------------------------------------------
# (c) PM's transcript, end to end at the seam
# ---------------------------------------------------------------------------


class TestPMTranscript1855:
    @pytest.mark.asyncio
    async def test_the_offer_becomes_an_imperative_and_yes_has_nothing_to_mis_bind(self):
        """Turn 1 rewritten; turn 2's "Yes, please." finds no offer.

        The honest no-result fallback never fires — not because the predicate
        got cleverer, but because the user was never invited to say yes.
        """
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(FloorContext(user_message="add One Job", session_id="s1855"))

        # BEFORE → AFTER on PM's verbatim sentence.
        assert PM_OFFER in PM_REPLY
        assert PM_OFFER not in resp.message
        assert f"To do that, say: {PM_EXPECTED_COMMAND}." in resp.message

        # The rewritten reply contains no yes/no invitation at all.
        assert detect_offer_questions(resp.message) == []

        # The floor still arms NOTHING — layer 1 does not arm, it stops the
        # floor PROMISING a binding that does not exist. So on turn 2 there is
        # no armed seam to consult the acceptance predicate at all: PM's
        # verbatim "Yes, please." routes normally instead of hitting the honest
        # no-result fallback, because it was never solicited.
        offers = WorkflowOfferService()
        assert offers.peek_pending_offer("s1855") is None

        # And the predicate's exactly-armed rule (#1694 (b)) is unchanged and
        # still correct: at the strict tier a bare affirmative with no stored
        # ask REFUSES rather than guessing an action.
        assert (
            evaluate_acceptance(
                "Yes, please.",
                effect=EffectClass.DESTRUCTIVE,
                armed_question=None,
                taught_accepts=None,
            )
            is not AcceptanceVerdict.ACCEPT
        )


# ---------------------------------------------------------------------------
# LastOffer: the reserved value is deleted, not built (Arch ruling #1855)
# ---------------------------------------------------------------------------


class TestLastOfferReservationDeleted:
    def test_no_reserved_offer_type_remains_in_services(self):
        """Arch's own check, kept as a regression: one authority, not two."""
        import pathlib
        import subprocess

        root = pathlib.Path(__file__).resolve().parents[4]
        hits = subprocess.run(
            ["grep", "-rn", '"actionable"', "services/"],
            cwd=root,
            capture_output=True,
            text=True,
        ).stdout.strip()
        assert hits == "", f"reserved offer_type resurrected:\n{hits}"

    def test_live_offer_types_still_construct(self):
        for offer_type in ("contextual", "process_resume"):
            offer = LastOffer(offer_type=offer_type, continuation_hint="explain more")
            assert offer.offer_type == offer_type

    def test_the_dead_comment_is_gone(self):
        import inspect

        import services.intent_service.conversation_context as cc

        src = inspect.getsource(cc)
        field_line = re.search(r"^\s*offer_type: str.*$", src, re.MULTILINE)
        assert field_line is not None
        assert "reserved for future use" not in field_line.group(0)
