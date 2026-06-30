"""#1331 (systemic): the conversational floor must forbid claiming unverified
action-success / resource-existence — the hole beyond action-coverage. In UAT the floor
confabulated "the test milestone is sitting there" by trusting a prior fake "✓" still in
the conversation history. These guards pin the floor-contract rule so it can't regress.
(Behavioral verification is a live chat test; this is the prompt-contract regression guard.)
"""

import re

from services.intent_service.conversational_floor import FLOOR_SYSTEM_PROMPT_ADDENDUM

# Normalize whitespace — the prompt is line-wrapped, so phrases span newlines+indent.
_NORM = re.sub(r"\s+", " ", FLOOR_SYSTEM_PROMPT_ADDENDUM).lower()


def test_floor_forbids_unverified_action_success():
    p = _NORM
    assert "verified it this turn" in p, "floor must require this-turn verification for action claims"
    assert (
        "past claim of success is not proof" in p
    ), "floor must distrust prior '✓' claims in history (the milestone-confabulation vector)"
    assert "never simulate" in p, "floor must forbid simulating/pre-announcing success"


def test_floor_still_forbids_data_fabrication():
    # the pre-existing data-fabrication rule must remain alongside the new action rule
    assert "never fabricate user data" in FLOOR_SYSTEM_PROMPT_ADDENDUM.lower()
