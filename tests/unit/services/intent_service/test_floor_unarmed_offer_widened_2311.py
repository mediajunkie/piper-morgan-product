"""#2311: the #1855 seam's widened lead (Arch 11-06 16:10; PPM 16:24 build now).

The floor's own narration before a dash, of any length, then an offer opener, with
nothing armed: 'Deleting "urgent task" and "review prs" — want me to go ahead?' on beta
7ffd460640. The sentence is rewritten whole in CXO's words (16:21), the shape chosen
from Arch's closed list of bare predicates (16:22), and it is never armed (condition 3).

The census rows are the 11 unique, cleanly split sentences of Lead's 16:20 census over
337 served-transcript and control files (5,379 questions, 0 false positives).
"""

import pytest

from services.intent_service.unarmed_offer import (
    NOTHING_DONE_BARE,
    detect_offer_questions,
    enforce_armed_offers,
)

_CENSUS = [
    "I don't have your projects pulled up right now — want me to grab both your active "
    "projects and the archived list in one shot?",
    "I don't have your projects pulled up right now — want me to grab both your active "
    "projects and archived list in one shot?",
    "I don't have your projects pulled up right now — want me to grab both the active "
    "project list and the archived list in one shot?",
    "I can pull up your archived projects — want me to run that now?",
    "I don't have your projects pulled up right now — want me to grab both the active "
    "project list and the archived one?",
    "I don't have your projects pulled up just now — want me to grab both the active list "
    "and the archived list in one shot?",
    "I'm not seeing any projects pulled up for this account right now — want me to try "
    "fetching that list again?",
    "I'll need to pull up your archived projects — want me to run that query now?",
    "For the archived projects list — want me to pull that now?",
    "As for the archived projects list — want me to pull that up now?",
    'Deleting "urgent task" and "review prs" — want me to go ahead?',
]

_WITH_OBJECT_PREFIX = "Nothing has been done yet. If you'd like me to "


@pytest.mark.parametrize("sentence", _CENSUS)
def test_each_census_sentence_is_detected_as_widened(sentence):
    [offer] = detect_offer_questions(sentence)
    assert offer.widened is True


@pytest.mark.parametrize("sentence", _CENSUS)
def test_each_census_sentence_rewrites_to_one_shape_without_its_lead_or_a_question(sentence):
    out, rewrites = enforce_armed_offers(sentence)
    assert rewrites == 1
    assert "?" not in out
    lead = sentence.split("—", 1)[0].strip()
    assert lead not in out
    assert out == NOTHING_DONE_BARE or (
        out.startswith(_WITH_OBJECT_PREFIX) and out.endswith(", ask me directly.")
    )


def test_the_delete_narration_gets_the_bare_shape():
    out, _ = enforce_armed_offers('Deleting "urgent task" and "review prs" — want me to go ahead?')
    assert out == "Nothing has been done yet. Tell me what you'd like as a direct request."
    assert "Deleting" not in out


def test_a_predicate_with_an_object_keeps_it():
    out, _ = enforce_armed_offers("For the archived projects list — want me to pull that now?")
    assert out == "Nothing has been done yet. If you'd like me to pull that now, ask me directly."


@pytest.mark.parametrize("predicate", ["go ahead", "do that", "do it", "proceed", "Go ahead"])
def test_the_closed_list_of_bare_predicates(predicate):
    out, _ = enforce_armed_offers(f"Here is the plan — want me to {predicate}?")
    assert out == NOTHING_DONE_BARE


def test_which_two_should_i_delete_is_unchanged():
    """No offer opener: ADR-083's to fix, not this seam's."""
    sentence = 'Which two should I delete — "urgent task" and "review prs"?'
    assert detect_offer_questions(sentence) == []
    assert enforce_armed_offers(sentence) == (sentence, 0)


def test_the_short_lead_keeps_its_present_rewrite():
    """The 1-3 word lead (#2080) is not the widened form; its rewrite is unchanged."""
    [offer] = detect_offer_questions("Got it — want me to go ahead?")
    assert offer.widened is False
    out, _ = enforce_armed_offers("Got it — want me to go ahead?")
    assert out == "If you'd like me to go ahead, just tell me directly."


def test_a_hyphen_inside_a_word_is_not_a_dash():
    assert detect_offer_questions("I can add the follow-up list want me to do it?") == []


def test_a_spaced_hyphen_is_a_dash():
    [offer] = detect_offer_questions("I set up the follow-up list - want me to add the rest?")
    assert offer.widened is True


def test_a_widened_offer_is_never_armed():
    """Condition 3: the widened form arms nothing, even an add-project offer the
    narrow form's tier 1 could bind."""
    armed = []
    # The #1855 layer-2 PM fixture's offer (which the narrow form arms), behind a long lead.
    text = (
        "I found the repo you mentioned a moment ago — want me to add 'One Job' with the "
        "Design-in-Product/one-job repo to your projects now?"
    )
    out, rewrites = enforce_armed_offers(
        text,
        arm_offer=lambda record: armed.append(record) or True,
        user_text="add One Job with repo Design-in-Product/one-job",
    )
    assert armed == []
    assert rewrites == 1
    assert out.startswith("Nothing has been done yet.")


def test_something_already_armed_passes_through():
    text = 'Deleting "urgent task" — want me to go ahead?'
    assert enforce_armed_offers(text, armed_offer="workflow_offer") == (text, 0)
