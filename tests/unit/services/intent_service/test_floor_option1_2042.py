"""#2042 option 1: the floor prompt no longer compels an observation.

Arch's 10-29 diagnosis (#2042): the floor's unasked "Also..." asides and its
invented issue→milestone relations came from the prompt itself. Every reply
had to "exhibit" five pillars ("no response should structurally lack any of
them"), one of which was Prediction, so a turn about something else still
had to carry an observation; and the Time pillar asked for "lived time, not
clock time", which told the model to turn a raw timestamp into "yesterday".

Option 1 (ordered first by PPM and CXO; words CXO's, 10-29 20:48 and 10-31
21:32; build spec Arch's on #2042, 10-31):
1. the compulsory-pillars sentence and the Prediction bullet are replaced by
   CXO's observation paragraph, verbatim;
2. the Time bullet is replaced by CXO's wording, which drops the instruction
   to convert and keeps the three example phrases as examples of HANDED words;
3. no existing ban is loosened (the other floor-prompt pins stay as they are).

These pins hold the text. The behaviour is measured served (Arch's
preregistered row-3 replay and one row-2 run, judged by CXO), not here.
"""

import re

from services.intent_service.conversational_floor import FLOOR_SYSTEM_PROMPT_ADDENDUM

_NORM = re.sub(r"\s+", " ", FLOOR_SYSTEM_PROMPT_ADDENDUM)
_LOWER = _NORM.lower()

# CXO's words, 10-29 20:48 (#2042 comment), whitespace-normalised.
CXO_OBSERVATION_PARAGRAPH = (
    "add an observation only when something in the context bears on what the "
    "person asked and you can point to where it came from in this turn's data. "
    "When nothing does, answer and stop. A reply with no observation is "
    "complete. Never state how two records relate (which milestone an issue "
    "belongs to, what an issue is linked to) unless that relation is in the "
    "data you were given. Never turn a timestamp into a relative time such as "
    '"yesterday". Use the time as given, or leave it out.'
)

# CXO's words, 10-31 21:32 memo, whitespace-normalised.
CXO_TIME_BULLET = (
    "- Time: lived time, in the user's own terms. Use the time words your "
    'context already gives you ("earlier today", "since Tuesday", "when you '
    'pushed that PR"). Never work a time out from a timestamp, and never state '
    "a clock time, a date or an interval you were not handed. If you have no "
    "time word, say nothing about when."
)


def _time_bullet() -> str:
    """The Time bullet alone: from '- Time:' to the next voice bullet."""
    start = _NORM.index("- Time:")
    end = _NORM.index("- Space:", start)
    return _NORM[start:end].strip()


class TestObservationParagraph:
    def test_cxo_paragraph_is_present_verbatim(self):
        assert CXO_OBSERVATION_PARAGRAPH in _NORM

    def test_the_compulsion_is_gone(self):
        assert "structurally lack" not in _LOWER
        assert "no response should" not in _LOWER
        assert "every response should exhibit" not in _LOWER

    def test_prediction_is_no_longer_a_pillar(self):
        assert "- prediction:" not in _LOWER
        assert "observation, not telemetry" not in _LOWER
        assert "why it might deserve attention" not in _LOWER

    def test_a_reply_with_no_observation_is_complete(self):
        assert "a reply with no observation is complete" in _LOWER

    def test_relations_need_data(self):
        assert "never state how two records relate" in _LOWER
        assert "which milestone an issue belongs to" in _LOWER

    def test_the_paragraph_appears_once(self):
        assert _NORM.count("A reply with no observation is complete") == 1


class TestTimeBullet:
    def test_cxo_time_bullet_is_present_verbatim(self):
        assert CXO_TIME_BULLET in _NORM

    def test_three_example_phrases_survive_as_handed_words(self):
        bullet = _time_bullet()
        for phrase in ('"earlier today"', '"since Tuesday"', '"when you pushed that PR"'):
            assert phrase in bullet, phrase
        assert "your context already gives you" in bullet

    def test_no_instruction_to_convert_or_compute(self):
        """CXO's pin: the bullet carries no instruction to convert or compute.

        The only arithmetic verb left is inside a prohibition ("Never work a
        time out from a timestamp"); the old "lived time, not clock time"
        contrast, which asked for the conversion, is gone.
        """
        bullet = _time_bullet().lower()
        assert "not clock time" not in bullet
        assert "convert" not in bullet
        assert "compute" not in bullet
        assert "calculate" not in bullet
        assert "time has rhythm" not in bullet
        # "work a time out" appears only as the thing never to do.
        for m in re.finditer(r"work a time out", bullet):
            assert bullet[max(0, m.start() - 6) : m.start()].strip().endswith("never"), bullet

    def test_no_unhanded_clock_time_date_or_interval(self):
        bullet = _time_bullet().lower()
        assert "never state a clock time, a date or an interval you were not handed" in bullet
        assert "if you have no time word, say nothing about when" in bullet

    def test_the_two_time_rules_agree(self):
        """Arch's conflict (10-31): the Time bullet and the observation
        paragraph must not pull opposite ways. Both now say: the time as
        handed, or nothing."""
        assert "use the time as given, or leave it out" in _LOWER
        assert "say nothing about when" in _LOWER
        assert "lived time, not clock time" not in _LOWER


class TestNothingLoosened:
    """The other four voice bullets, the Grammar paragraph and every CRITICAL
    section stay; option 1 removes a compulsion, it does not loosen a ban."""

    def test_four_voice_bullets_remain(self):
        for head in ("- Identity:", "- Time:", "- Space:", "- Agency:"):
            assert head in _NORM, head

    def test_grammar_paragraph_remains(self):
        assert "Grammar — frame observations as entities experiencing moments in places" in _NORM

    def test_grammar_paragraph_takes_a_moment_only_from_handed_time_words(self):
        """CXO 07:16 / Arch 07:16-07:18 (11-01): the Grammar paragraph was a third
        place asking for a time ("how long it has been waiting or when it last
        moved"); with ISO-only slices the model could meet it only by working a
        duration out. CXO's one parenthetical ties the moment to handed words.
        Pin (CXO's): the clause is present, and the telemetry-register sentence
        still stands."""
        start = _NORM.index("Grammar — frame observations")
        end = _NORM.index("Use the context you have.", start)
        grammar = _NORM[start:end]
        assert (
            "how long it has been waiting or when it last moved (only in the time words "
            "your context already gives you), and where it lives" in grammar
        )
        assert "Telemetry register" in grammar and "is not grammatical" in grammar
        assert "Only prose is a colleague speaking" in grammar

    def test_critical_sections_remain(self):
        assert "CRITICAL — Never fabricate user data" in _NORM
        assert "CRITICAL — Never claim an action happened" in _NORM

    def test_voice_heading_remains_without_the_compulsion(self):
        assert "Voice constraints:" in _NORM
