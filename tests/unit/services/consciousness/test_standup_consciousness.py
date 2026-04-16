"""
Tests for Standup Consciousness Wrapper.

Part of Issue #632: Consciousness Integration for Morning Standup.
TDD approach: tests written FIRST, then implementation.

Tests validate that standup output meets MVC (Minimum Viable Consciousness) requirements:
1. Identity Voice - has "I" statement
2. Epistemic Humility - has uncertainty/hedge
3. Dialogue Opening - has invitation
4. Source Transparency - has attribution
"""

import pytest

from services.consciousness.validation import (
    MVCResult,
    has_attribution,
    has_identity,
    has_invitation,
    has_uncertainty,
    validate_mvc,
)


class TestFormatStandupGreetingConscious:
    """Tests for format_standup_greeting_conscious function."""

    def test_greeting_has_identity(self):
        """Greeting contains identity voice (I statement)."""
        from services.consciousness.standup_consciousness import format_standup_greeting_conscious

        result = format_standup_greeting_conscious(["GitHub", "conversations"])
        assert has_identity(result), f"Missing identity voice in: {result}"

    def test_greeting_has_source_attribution(self):
        """Greeting contains source attribution."""
        from services.consciousness.standup_consciousness import format_standup_greeting_conscious

        result = format_standup_greeting_conscious(["GitHub", "Calendar"])
        assert has_attribution(result), f"Missing source attribution in: {result}"

    def test_greeting_mentions_sources(self):
        """Greeting mentions the actual sources provided."""
        from services.consciousness.standup_consciousness import format_standup_greeting_conscious

        result = format_standup_greeting_conscious(["GitHub", "Calendar"])
        # Should mention at least one source
        assert (
            "GitHub" in result or "Calendar" in result or "your" in result.lower()
        ), f"Sources not mentioned in: {result}"


class TestFormatAccomplishmentsConscious:
    """Tests for format_accomplishments_conscious function."""

    def test_accomplishments_has_identity(self):
        """Accomplishments section contains identity voice."""
        from services.consciousness.standup_consciousness import format_accomplishments_conscious

        result = format_accomplishments_conscious(["Fixed bug #123", "Added feature"])
        assert has_identity(result), f"Missing identity voice in: {result}"

    def test_accomplishments_adds_context(self):
        """Accomplishments section adds contextual framing."""
        from services.consciousness.standup_consciousness import format_accomplishments_conscious

        accomplishments = ["Fixed bug #123", "Added feature"]
        result = format_accomplishments_conscious(accomplishments)
        # Should contain the accomplishments in some form
        assert (
            "Fixed" in result or "bug" in result or "feature" in result
        ), f"Accomplishments not reflected in: {result}"

    def test_accomplishments_empty_list_handled(self):
        """Empty accomplishments list returns graceful message."""
        from services.consciousness.standup_consciousness import format_accomplishments_conscious

        result = format_accomplishments_conscious([])
        assert has_identity(result), f"Missing identity voice in empty case: {result}"


class TestFormatPrioritiesConscious:
    """Tests for format_priorities_conscious function."""

    def test_priorities_has_identity(self):
        """Priorities section contains identity voice."""
        from services.consciousness.standup_consciousness import format_priorities_conscious

        result = format_priorities_conscious(["Continue work", "Review feedback"])
        assert has_identity(result), f"Missing identity voice in: {result}"

    def test_priorities_has_reasoning(self):
        """Priorities section shows reasoning or epistemic humility."""
        from services.consciousness.standup_consciousness import format_priorities_conscious

        result = format_priorities_conscious(["Continue work", "Review feedback"])
        # Should have either uncertainty language or invitation
        has_epistemic = has_uncertainty(result) or has_invitation(result)
        assert has_epistemic, f"Missing reasoning/epistemic humility in: {result}"


class TestFormatBlockersConscious:
    """Tests for format_blockers_conscious function."""

    def test_blockers_has_epistemic_humility(self):
        """Blockers section shows epistemic humility when no blockers."""
        from services.consciousness.standup_consciousness import format_blockers_conscious

        result = format_blockers_conscious([])
        # Should show uncertainty about absence of blockers
        has_epistemic = has_identity(result) and (
            has_uncertainty(result) or "didn't" in result.lower()
        )
        assert has_epistemic, f"Missing epistemic humility for no blockers: {result}"

    def test_blockers_with_items(self):
        """Blockers section properly formats actual blockers."""
        from services.consciousness.standup_consciousness import format_blockers_conscious

        blockers = ["Waiting on API access", "Need design review"]
        result = format_blockers_conscious(blockers)
        assert has_identity(result), f"Missing identity voice in: {result}"
        # Should mention the blocker content
        assert (
            "API" in result or "access" in result or "waiting" in result.lower()
        ), f"Blockers not reflected in: {result}"


class TestFormatStandupClosingConscious:
    """Tests for format_standup_closing_conscious function."""

    def test_closing_has_dialogue_invitation(self):
        """Closing section invites dialogue."""
        from services.consciousness.standup_consciousness import format_standup_closing_conscious

        metrics = {"generation_time_ms": 1200, "time_saved_minutes": 15}
        result = format_standup_closing_conscious(metrics)
        assert has_invitation(result), f"Missing dialogue invitation in: {result}"

    def test_closing_has_identity(self):
        """Closing section maintains identity voice."""
        from services.consciousness.standup_consciousness import format_standup_closing_conscious

        metrics = {"generation_time_ms": 1200, "time_saved_minutes": 15}
        result = format_standup_closing_conscious(metrics)
        assert has_identity(result), f"Missing identity voice in: {result}"


class TestFormatFullStandupConscious:
    """Tests for format_full_standup_conscious function."""

    def test_full_standup_passes_mvc(self):
        """Full standup output passes all MVC requirements."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub", "conversations"],
            "yesterday_accomplishments": ["Fixed bug", "Added feature"],
            "today_priorities": ["Continue work", "Review feedback"],
            "blockers": [],
            "metrics": {"generation_time_ms": 1200, "time_saved_minutes": 15},
        }

        result = format_full_standup_conscious(standup_data)
        mvc_result = validate_mvc(result)
        assert mvc_result.passes, f"MVC failed: {mvc_result.missing}. Suggestions: {mvc_result.suggestions}. Output: {result}"

    def test_full_standup_has_all_sections(self):
        """Full standup contains all expected sections."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub", "conversations"],
            "yesterday_accomplishments": ["Fixed bug", "Added feature"],
            "today_priorities": ["Continue work", "Review feedback"],
            "blockers": ["Waiting on API access"],
            "metrics": {"generation_time_ms": 1200, "time_saved_minutes": 15},
        }

        result = format_full_standup_conscious(standup_data)

        # Should have greeting, accomplishments, priorities, blockers, and closing
        # Check for reasonable length indicating multiple sections
        assert len(result) > 100, f"Output too short, likely missing sections: {result}"

        # Should contain content from all sections
        assert "I" in result, f"Missing identity voice: {result}"  # Identity from greeting
        assert (
            "?" in result
        ), f"Missing question mark (dialogue invitation): {result}"  # Invitation from closing

    def test_full_standup_with_blockers(self):
        """Full standup properly includes blockers when present."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub"],
            "yesterday_accomplishments": ["Fixed bug"],
            "today_priorities": ["Continue work"],
            "blockers": ["Waiting on API access", "Need design approval"],
            "metrics": {"generation_time_ms": 1200, "time_saved_minutes": 15},
        }

        result = format_full_standup_conscious(standup_data)
        mvc_result = validate_mvc(result)
        assert (
            mvc_result.passes
        ), f"MVC failed with blockers: {mvc_result.missing}. Output: {result}"

    def test_full_standup_empty_accomplishments(self):
        """Full standup handles empty accomplishments gracefully."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub"],
            "yesterday_accomplishments": [],
            "today_priorities": ["Start new work"],
            "blockers": [],
            "metrics": {"generation_time_ms": 1200, "time_saved_minutes": 15},
        }

        result = format_full_standup_conscious(standup_data)
        mvc_result = validate_mvc(result)
        assert (
            mvc_result.passes
        ), f"MVC failed with empty accomplishments: {mvc_result.missing}. Output: {result}"


class TestMVCIntegration:
    """Integration tests verifying MVC compliance across all functions."""

    def test_all_functions_maintain_identity_voice(self):
        """All consciousness functions maintain identity voice."""
        from services.consciousness.standup_consciousness import (
            format_accomplishments_conscious,
            format_blockers_conscious,
            format_priorities_conscious,
            format_standup_closing_conscious,
            format_standup_greeting_conscious,
        )

        greeting = format_standup_greeting_conscious(["GitHub"])
        accomplishments = format_accomplishments_conscious(["Task done"])
        priorities = format_priorities_conscious(["Next task"])
        blockers = format_blockers_conscious([])
        closing = format_standup_closing_conscious({"generation_time_ms": 1000})

        for name, output in [
            ("greeting", greeting),
            ("accomplishments", accomplishments),
            ("priorities", priorities),
            ("blockers", blockers),
            ("closing", closing),
        ]:
            assert has_identity(output), f"{name} missing identity voice: {output}"

    def test_combined_output_passes_mvc(self):
        """Combined output from all functions passes MVC validation."""
        from services.consciousness.standup_consciousness import (
            format_accomplishments_conscious,
            format_blockers_conscious,
            format_priorities_conscious,
            format_standup_closing_conscious,
            format_standup_greeting_conscious,
        )

        combined = "\n\n".join(
            [
                format_standup_greeting_conscious(["GitHub", "Calendar"]),
                format_accomplishments_conscious(["Fixed bug", "Reviewed PR"]),
                format_priorities_conscious(["Continue feature work"]),
                format_blockers_conscious([]),
                format_standup_closing_conscious(
                    {"generation_time_ms": 1200, "time_saved_minutes": 15}
                ),
            ]
        )

        mvc_result = validate_mvc(combined)
        assert mvc_result.passes, f"Combined MVC failed: {mvc_result.missing}. Output: {combined}"
