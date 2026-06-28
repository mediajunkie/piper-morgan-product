"""
#1033 — COMPOSTED state experience-phrase regression test.

Per `lifecycle-experience-guide.md`:
> COMPOSTED — Experience Phrase: "I learned that..."

This is the most distinctive MUX surface (filing-dreams metaphor); the
phrase is load-bearing for the user-facing voice. A future change that
flattens this phrase to a technical label or different framing would
silently erode the MUX vocabulary.

This test asserts the canonical phrase is preserved verbatim in
`LifecycleState.COMPOSTED.experience_phrase`.

Also tests that all 8 stages have non-empty experience phrases (catches
accidental removal of any phrase).
"""

import pytest

from services.mux.lifecycle import LifecycleState


class TestCompostedExperiencePhrase:
    def test_composted_experience_phrase_canonical(self):
        """The canonical phrase per lifecycle-experience-guide.md."""
        assert LifecycleState.COMPOSTED.experience_phrase == "I learned that..."

    def test_composted_phrase_not_empty(self):
        """Defensive — would catch accidental empty/None return."""
        phrase = LifecycleState.COMPOSTED.experience_phrase
        assert phrase
        assert isinstance(phrase, str)

    def test_composted_phrase_is_first_person_reflection(self):
        """Per D3 spec § Reflection Openers: composting language uses
        first-person reflection ('I learned'), NOT analysis or surveillance
        framing ('I detected', 'I monitored', 'My analysis')."""
        phrase = LifecycleState.COMPOSTED.experience_phrase.lower()
        forbidden_starts = [
            "i detected",
            "i monitored",
            "i observed",
            "i tracked",
            "my analysis",
            "based on",
            "after analyzing",
        ]
        for forbidden in forbidden_starts:
            assert not phrase.startswith(
                forbidden
            ), f"COMPOSTED phrase should not start with surveillance framing: {phrase!r}"


class TestAllStagesHaveExperiencePhrases:
    """Defensive — every stage must have a non-empty experience phrase.
    The phrase is part of the user-facing voice; missing one would silently
    degrade UX wherever the phrase is rendered.
    """

    @pytest.mark.parametrize("stage", list(LifecycleState))
    def test_each_stage_has_phrase(self, stage):
        phrase = stage.experience_phrase
        assert phrase, f"Stage {stage.name} has no experience phrase"
        assert isinstance(phrase, str)
        assert phrase.strip(), f"Stage {stage.name} has whitespace-only phrase"

    def test_all_phrases_unique(self):
        """No two stages should share an experience phrase — that would
        make the lifecycle UI ambiguous in narrative output."""
        phrases = [stage.experience_phrase for stage in LifecycleState]
        assert len(phrases) == len(
            set(phrases)
        ), f"Duplicate experience phrases across stages: {phrases}"
