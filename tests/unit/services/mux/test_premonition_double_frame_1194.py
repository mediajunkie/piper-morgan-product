"""#1194: frame_insight_for_surfacing must not double-frame.

`expression` is already a first-person frame (composting_models factories build it
as "It occurs to me that {description}" etc.). Surfacing wraps content in ANOTHER
frame, so it must wrap the BARE description (or a frame-stripped expression), never
the pre-framed expression — else "...it occurs to me that It occurs to me that ...".
"""

from unittest.mock import MagicMock

from services.mux.premonition import _strip_leading_frame, frame_insight_for_surfacing


def _insight(*, description="", expression="", learning_type="general", requires_attention=False):
    learning = MagicMock()
    learning.description = description
    learning.expression = expression
    learning.learning_type = learning_type
    learning.requires_attention = requires_attention
    insight = MagicMock()
    insight.learning = learning
    return insight


class TestStripLeadingFrame:
    def test_strips_it_occurs_to_me_that(self):
        assert _strip_leading_frame("It occurs to me that X happened") == "X happened"

    def test_strips_pattern_frame(self):
        assert _strip_leading_frame("I've noticed a pattern: Y") == "Y"

    def test_case_insensitive(self):
        assert _strip_leading_frame("it occurs to me that z") == "z"

    def test_leaves_unframed_text_untouched(self):
        assert _strip_leading_frame("Just a plain fact") == "Just a plain fact"

    def test_empty(self):
        assert _strip_leading_frame("") == ""


class TestNoDoubleFrame:
    def test_prefers_bare_description_over_framed_expression(self):
        # description is bare; expression is pre-framed. Must wrap description.
        ins = _insight(
            description="the migration completed cleanly",
            expression="It occurs to me that the migration completed cleanly",
        )
        out = frame_insight_for_surfacing(ins).lower()
        assert "it occurs to me that it occurs to me" not in out
        assert "the migration completed cleanly" in out

    def test_falls_back_to_stripped_expression_when_no_description(self):
        ins = _insight(description="", expression="It occurs to me that the api was flaky")
        out = frame_insight_for_surfacing(ins).lower()
        assert "it occurs to me that it occurs to me" not in out
        assert "the api was flaky" in out
