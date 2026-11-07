"""#2311: the #1855 seam's widened lead (Arch 11-06 16:10; PPM 16:24 build now).

The floor's own narration before a dash, of any length, then an offer opener, with
nothing armed: 'Deleting "urgent task" and "review prs" — want me to go ahead?' on beta
7ffd460640. It is never armed (condition 3) and is rewritten in CXO's words (16:21,
amended 16:45), the shape chosen as copy only (Arch 16:22, 16:41):

- shape 2, a predicate with no object of its own (bare, or only that / it / this,
  optionally "up" / "now"): the lead is dropped, ``Nothing has been done yet. Tell me
  what you'd like as a direct request.``, UNLESS this turn failed a read, when the lead
  may be the true failure report and is kept;
- shape 1, anything else: the lead stays as its own sentence and only the offer is
  replaced, ``{lead}. If you'd like me to {predicate}, ask me directly.``

The census rows are the 11 unique, cleanly split sentences of Lead's 16:20 census over
337 served-transcript and control files (5,379 questions, 0 false positives).
"""

import pytest

from services.intent_service.unarmed_offer import (
    NOTHING_DONE_BARE,
    detect_offer_questions,
    enforce_armed_offers,
    is_shape_two_predicate,
)

_GRAB = "I don't have your projects pulled up right now"
_JUST_NOW = "I don't have your projects pulled up just now"

# (sentence, expected rewrite)
_CENSUS = [
    (
        f"{_GRAB} — want me to grab both your active projects and the archived list in one shot?",
        f"{_GRAB}. If you'd like me to grab both your active projects and the archived list "
        "in one shot, ask me directly.",
    ),
    (
        f"{_GRAB} — want me to grab both your active projects and archived list in one shot?",
        f"{_GRAB}. If you'd like me to grab both your active projects and archived list "
        "in one shot, ask me directly.",
    ),
    (
        f"{_GRAB} — want me to grab both the active project list and the archived list in "
        "one shot?",
        f"{_GRAB}. If you'd like me to grab both the active project list and the archived "
        "list in one shot, ask me directly.",
    ),
    ("I can pull up your archived projects — want me to run that now?", NOTHING_DONE_BARE),
    (
        f"{_GRAB} — want me to grab both the active project list and the archived one?",
        f"{_GRAB}. If you'd like me to grab both the active project list and the archived "
        "one, ask me directly.",
    ),
    (
        f"{_JUST_NOW} — want me to grab both the active list and the archived list in one shot?",
        f"{_JUST_NOW}. If you'd like me to grab both the active list and the archived list "
        "in one shot, ask me directly.",
    ),
    (
        "I'm not seeing any projects pulled up for this account right now — want me to try "
        "fetching that list again?",
        "I'm not seeing any projects pulled up for this account right now. If you'd like me "
        "to try fetching that list again, ask me directly.",
    ),
    (
        "I'll need to pull up your archived projects — want me to run that query now?",
        "I'll need to pull up your archived projects. If you'd like me to run that query "
        "now, ask me directly.",
    ),
    ("For the archived projects list — want me to pull that now?", NOTHING_DONE_BARE),
    ("As for the archived projects list — want me to pull that up now?", NOTHING_DONE_BARE),
    ('Deleting "urgent task" and "review prs" — want me to go ahead?', NOTHING_DONE_BARE),
]


@pytest.mark.parametrize("sentence,expected", _CENSUS)
def test_each_census_sentence_is_widened_and_rewrites_to_its_shape(sentence, expected):
    [offer] = detect_offer_questions(sentence)
    assert offer.widened is True
    out, rewrites = enforce_armed_offers(sentence)
    assert rewrites == 1
    assert out == expected
    assert "?" not in out


def test_the_delete_narration_loses_its_lead():
    out, _ = enforce_armed_offers('Deleting "urgent task" and "review prs" — want me to go ahead?')
    assert out == "Nothing has been done yet. Tell me what you'd like as a direct request."
    assert "Deleting" not in out


@pytest.mark.parametrize(
    "predicate",
    [
        "go ahead",
        "Go ahead",
        "go on",
        "go for it",
        "proceed",
        "do it",
        "do that",
        "do this",
        "run that",
        "run that now",
        "run it now",
        "pull it up",
        "pull that up now",
        "fetch it",
        "grab that",
        "try that",
    ],
)
def test_shape_two_predicates(predicate):
    assert is_shape_two_predicate(predicate)


@pytest.mark.parametrize(
    "predicate",
    ["run that query now", "check again", "try again", "grab both your active projects"],
)
def test_shape_one_predicates(predicate):
    assert not is_shape_two_predicate(predicate)


# CXO 16:45: when this turn failed a read, the lead is never dropped.
@pytest.mark.parametrize(
    "sentence,expected",
    [
        (
            "I wasn't able to pull up your reminders just now — want me to try again?",
            "I wasn't able to pull up your reminders just now. If you'd like me to try "
            "again, ask me directly.",
        ),
        (
            "I couldn't pull up that list just now — want me to check again?",
            "I couldn't pull up that list just now. If you'd like me to check again, "
            "ask me directly.",
        ),
        (
            "I couldn't pull that up just now — want me to run that now?",
            "I couldn't pull that up just now. If you'd like me to run that now, "
            "ask me directly.",
        ),
    ],
)
def test_a_failed_read_keeps_its_lead(sentence, expected):
    assert enforce_armed_offers(sentence, read_failed=True) == (expected, 1)


def test_without_a_failed_read_a_shape_two_lead_is_dropped():
    out, _ = enforce_armed_offers("I couldn't pull that up just now — want me to run that now?")
    assert out == NOTHING_DONE_BARE


def test_which_two_should_i_delete_is_unchanged():
    """No offer opener: ADR-083's to fix (#2310), not this seam's."""
    sentence = 'Which two should I delete — "urgent task" and "review prs"?'
    assert detect_offer_questions(sentence) == []
    assert enforce_armed_offers(sentence) == (sentence, 0)


def test_the_short_lead_keeps_its_present_rewrite():
    """The 1-3 word lead (#2080) is not the widened form; its rewrite is unchanged."""
    [offer] = detect_offer_questions("Got it — want me to go ahead?")
    assert offer.widened is False
    out, _ = enforce_armed_offers("Got it — want me to go ahead?")
    assert out == "If you'd like me to go ahead, just tell me directly."


def test_a_spaced_hyphen_is_a_dash():
    [offer] = detect_offer_questions("I set up the follow-up list - want me to add the rest?")
    assert offer.widened is True
    assert offer.lead == "I set up the follow-up list"


def test_a_widened_offer_is_never_armed():
    """Condition 3: the widened form arms nothing, even an add-project offer the
    narrow form's tier 1 could bind (the #1855 layer-2 PM fixture's offer)."""
    armed = []
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
    assert out.startswith("I found the repo you mentioned a moment ago. If you'd like me to add")


def test_something_already_armed_passes_through():
    text = 'Deleting "urgent task" — want me to go ahead?'
    assert enforce_armed_offers(text, armed_offer="workflow_offer") == (text, 0)
