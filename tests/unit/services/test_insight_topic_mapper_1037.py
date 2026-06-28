"""Tests for the Insight Journal topic mapper (#1037 — MUX-INSIGHT-TOPIC-MAPPING).

Covers the derive_topic_from_tags() function + the un-hiding of topic tabs
in the insights.html template + integration into the insights API payload.

Per Pattern-073 discipline: the mapper returns None (uncategorized) rather
than guessing a topic; the UI treats None as "All-only visibility."
"""

from pathlib import Path

import pytest

from services.mux.insight_topic_mapper import (
    KNOWN_TOPICS,
    derive_topic_from_tags,
)


# Direct mapping tests ---------------------------------------------------


@pytest.mark.parametrize(
    "tags,expected",
    [
        # work-patterns
        (["workflow", "morning"], "work-patterns"),
        (["habit"], "work-patterns"),
        (["coding pattern"], "work-patterns"),
        # projects
        (["project alpha"], "projects"),
        (["milestone q3"], "projects"),
        (["feature delivery"], "projects"),
        # preferences
        (["voice preference"], "preferences"),
        (["preferred tone"], "preferences"),
        (["style note"], "preferences"),
        # relationships
        (["team dynamics"], "relationships"),
        (["user feedback"], "relationships"),
        (["stakeholder ask"], "relationships"),
        # scheduling
        (["calendar conflict"], "scheduling"),
        (["meeting cadence"], "scheduling"),
        (["deadline pressure"], "scheduling"),
    ],
)
def test_mapper_routes_keyword_tags_correctly(tags, expected) -> None:
    """Each known keyword routes to the right topic category."""
    assert derive_topic_from_tags(tags) == expected


def test_uncategorized_tags_return_none() -> None:
    """Tags that don't match any topic return None (Pattern-073 discipline)."""
    assert derive_topic_from_tags(["coding", "implementation"]) is None
    assert derive_topic_from_tags(["random", "uncategorized"]) is None


def test_empty_inputs_return_none() -> None:
    """None, [], and [""] all return None."""
    assert derive_topic_from_tags(None) is None
    assert derive_topic_from_tags([]) is None
    assert derive_topic_from_tags([""]) is None
    assert derive_topic_from_tags(["", None]) is None  # type: ignore[list-item]


def test_case_insensitive_matching() -> None:
    """Matching is case-insensitive on the tag side."""
    assert derive_topic_from_tags(["CALENDAR"]) == "scheduling"
    assert derive_topic_from_tags(["Workflow"]) == "work-patterns"
    assert derive_topic_from_tags(["PROJECT"]) == "projects"


def test_first_match_wins_in_declaration_order() -> None:
    """When tags map to multiple categories, the first declared topic wins."""
    # work-patterns declared before scheduling; tag matches both
    assert derive_topic_from_tags(["workflow scheduling"]) == "work-patterns"
    # projects declared before relationships
    assert derive_topic_from_tags(["project team"]) == "projects"


def test_substring_match_on_tag() -> None:
    """Keywords match as substrings of tags, not whole-word."""
    assert derive_topic_from_tags(["my-calendar-week"]) == "scheduling"


def test_known_topics_matches_template_data_topic() -> None:
    """KNOWN_TOPICS tuple matches the data-topic values in the template."""
    expected = {
        "work-patterns",
        "projects",
        "preferences",
        "relationships",
        "scheduling",
    }
    assert set(KNOWN_TOPICS) == expected


# Template un-hiding -----------------------------------------------------


def test_template_topic_tabs_are_visible() -> None:
    """All 5 topic tabs are present in the template (no longer commented out)."""
    html = Path("templates/insights.html").read_text()
    for topic_id in KNOWN_TOPICS:
        marker = f'data-topic="{topic_id}"'
        assert marker in html, f"Topic tab for {topic_id!r} must be visible in the template"


def test_template_no_longer_marks_topic_tabs_as_withheld() -> None:
    """The {# Withheld... #} jinja comment block is gone."""
    html = Path("templates/insights.html").read_text()
    assert (
        "Withheld until #1037" not in html
    ), "The withheld-tabs comment must be removed; #1037 has shipped"


# API integration --------------------------------------------------------


def test_payload_serializer_includes_topic_derived_from_tags() -> None:
    """_insight_to_payload uses derive_topic_from_tags on learning.topic_tags."""
    from unittest.mock import MagicMock

    from web.api.routes.insights import _insight_to_payload

    insight = MagicMock()
    insight.id = "i1"
    insight.created_at = None
    insight.user_response = None
    insight.user_correction = None

    learning = MagicMock()
    learning.expression = "test"
    learning.description = ""
    learning.confidence = 0.8
    learning.topic_tags = ["calendar", "deadline"]
    insight.learning = learning

    payload = _insight_to_payload(insight)
    assert payload["topic"] == "scheduling"


def test_payload_serializer_returns_none_topic_for_unmapped_tags() -> None:
    """Unmapped tags surface as topic=None in the payload."""
    from unittest.mock import MagicMock

    from web.api.routes.insights import _insight_to_payload

    insight = MagicMock()
    insight.id = "i1"
    insight.created_at = None
    insight.user_response = None
    insight.user_correction = None

    learning = MagicMock()
    learning.expression = "test"
    learning.description = ""
    learning.confidence = 0.8
    learning.topic_tags = ["something-random"]
    insight.learning = learning

    payload = _insight_to_payload(insight)
    assert payload["topic"] is None


def test_payload_serializer_handles_missing_learning() -> None:
    """Insight with no learning still serializes without crash; topic=None."""
    from unittest.mock import MagicMock

    from web.api.routes.insights import _insight_to_payload

    insight = MagicMock()
    insight.id = "i1"
    insight.created_at = None
    insight.user_response = None
    insight.user_correction = None
    insight.learning = None

    payload = _insight_to_payload(insight)
    assert payload["topic"] is None
