"""#1648 — the floor ACTION-CLAIMS CONTRACT, prompt-layer pins.

PM live 2026-08-18 (v58): in one session the floor roleplayed a full issue
filing ("Filed in test-piper-morgan. The issue is in there now." — zero
writes, verified against GitHub) and a reminder save ("Reminder set for 3pm
today." — no row, no 📅 line). The never-fabricate guidance constrained DATA
claims; nothing constrained the floor from claiming ACTIONS.

These pins cover the prompt half of the fix (layer honesty, m-43: this file
tests prompt CONTENT — the behavioral halves live in
test_action_fabrication_1648.py, which drives the real process_intent):

1. The action-claims contract is present: the floor must never state an
   action was performed; actions run only via dispatched handlers that
   compose their own confirmations; implied-but-unperformable actions get
   honesty plus a pointer at what would work.
2. The #1544 root cause is not reintroduced: the guidance states rules and
   contains NO example reply strings. The old section's own examples were
   the seeds — its "On it — creating that now…" is the near-verbatim shape
   of the live "On it — setting a reminder for 3pm today", and the #1517
   section's parenthetical example carried the exact "Reminder set for 3pm"
   shape of instance 2's fabrication.
"""

import re

from services.intent_service.conversational_floor import FLOOR_SYSTEM_PROMPT_ADDENDUM

_NORM = re.sub(r"\s+", " ", FLOOR_SYSTEM_PROMPT_ADDENDUM).lower()


def _action_claims_section() -> str:
    """The action-claims section (from its CRITICAL header to the next)."""
    start = FLOOR_SYSTEM_PROMPT_ADDENDUM.index(
        "CRITICAL — Never claim an action happened"
    )
    end = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL", start + 10)
    return FLOOR_SYSTEM_PROMPT_ADDENDUM[start:end]


class TestActionClaimsContractPresent:
    def test_contract_named_and_stated(self):
        section = re.sub(r"\s+", " ", _action_claims_section()).lower()
        assert "action-claims contract" in section
        # The structural rule: the floor only composes; rails act.
        assert "composing this reply is the only thing you are doing" in section
        assert "composes its own confirmation" in section
        assert "no action you can truthfully confirm" in section

    def test_no_meta_offer_roleplay(self):
        """Instance 2's shape — a soft offer to 'confirm'/'go ahead' with an
        action the floor cannot dispatch — must be named and forbidden."""
        section = re.sub(r"\s+", " ", _action_claims_section()).lower()
        assert "never role-play" in section
        assert "go ahead" in section
        assert "fabricated action claim" in section

    def test_honest_pointer_at_what_would_work(self):
        section = re.sub(r"\s+", " ", _action_claims_section()).lower()
        assert "say so directly and honestly" in section
        assert "one plain line" in section

    def test_1331_pins_survive_the_rewrite(self):
        """The pre-existing #1331 pins must keep holding on the new text."""
        assert "verified it this turn" in _NORM
        assert "past claim of success is not proof" in _NORM
        assert "never simulate" in _NORM
        assert "never fabricate user data" in _NORM

    def test_1517_retraction_rules_survive(self):
        assert "never retract" in _NORM
        assert "fabricated retraction" in _NORM


class TestNoExampleReplyStrings:
    """#1544's root cause: the model assembles replies from the prompt's own
    example sentences verbatim. The action guidance states rules only."""

    def test_old_seed_strings_are_gone(self):
        # The pre-announce example — near-verbatim shape of the live
        # "On it — setting a reminder for 3pm today" fabrication.
        assert "On it" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "creating that now" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        # The capability-denial example sentence.
        assert "I can't create milestones" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        # The offer-to-check example sentence.
        assert "want me to look up" not in FLOOR_SYSTEM_PROMPT_ADDENDUM

    def test_1517_example_confirmation_string_is_gone(self):
        # The retraction section's parenthetical example WAS an action
        # confirmation string — the exact "Reminder set for 3pm" shape PM
        # saw fabricated live.
        assert "Reminder set" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "I should have been upfront" not in FLOOR_SYSTEM_PROMPT_ADDENDUM

    def test_transcript_shapes_not_in_prompt(self):
        # Neither live fabrication can be prompt-seeded.
        assert "Filed in" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "Filed!" not in FLOOR_SYSTEM_PROMPT_ADDENDUM

    def test_action_section_has_no_quoted_reply_sentences(self):
        """Structural: no quote-delimited first-person sample sentence in the
        action-claims section (quoted vocabulary fragments like
        "done / created / ✓" are fine — they describe history content, not a
        reply to imitate)."""
        section = _action_claims_section()
        assert not re.search(
            r'["“]\s*(?:I\b|On it|Filed|Reminder|Created|Saved|Done\b)',
            section,
        ), section

    def test_own_words_instruction_present(self):
        section = re.sub(r"\s+", " ", _action_claims_section()).lower()
        assert "never copy phrasing from these instructions" in section
