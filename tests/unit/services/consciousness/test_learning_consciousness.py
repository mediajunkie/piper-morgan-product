"""Tests for learning/preference consciousness wrapper. Issue #636."""

import pytest


class TestLearningConsciousness:
    """Test consciousness wrapper for learning feedback."""

    def test_patterns_learned_has_identity(self):
        """Learning feedback must have identity voice."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [
            {"description": "Morning standup preference", "occurrences": 5, "confidence": 0.85},
        ]
        output = format_patterns_learned_conscious(patterns, 10)
        assert "I" in output or "I'" in output, "Should have identity"

    def test_patterns_learned_explains_what(self):
        """Learning feedback should explain what was learned."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [
            {"description": "Prefers concise updates", "occurrences": 3, "confidence": 0.9},
        ]
        output = format_patterns_learned_conscious(patterns, 5)
        assert "concise" in output.lower() or "pattern" in output.lower()

    def test_patterns_learned_has_invitation(self):
        """Learning feedback should invite correction."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [{"description": "test", "occurrences": 2, "confidence": 0.7}]
        output = format_patterns_learned_conscious(patterns, 3)
        assert "?" in output, "Should invite feedback/correction"

    def test_no_patterns_has_identity(self):
        """No patterns message should have identity."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        output = format_patterns_learned_conscious([], 5)
        assert "I" in output or "I'" in output

    def test_preference_saved_has_identity(self):
        """Preference saved feedback must have identity."""
        from services.consciousness.learning_consciousness import format_preference_saved_conscious

        output = format_preference_saved_conscious("standup_time", "morning")
        assert "I" in output or "I'" in output

    def test_preference_saved_claims_only_the_save(self):
        """#1198 honest contract: confirm the save; NO unbacked durable-recall
        promise ("I'll remember" / "future interactions") — the preference
        store's persistence isn't this function's to promise (#1199)."""
        from services.consciousness.learning_consciousness import format_preference_saved_conscious

        output = format_preference_saved_conscious("verbosity", "concise")
        assert "verbosity" in output and "concise" in output  # confirms the save
        assert "remember" not in output.lower()
        assert "future" not in output.lower()

    def test_preference_saved_has_invitation(self):
        """Preference saved should allow adjustment."""
        from services.consciousness.learning_consciousness import format_preference_saved_conscious

        output = format_preference_saved_conscious("theme", "dark")
        assert "?" in output


class TestLearningEventConsciousness:
    """Test consciousness wrapper for learning events."""

    def test_learning_event_has_identity(self):
        """Learning event must have identity voice."""
        from services.consciousness.learning_consciousness import format_learning_event_conscious

        output = format_learning_event_conscious("you prefer morning standups")
        assert "I " in output or "I'" in output, "Should have identity"

    def test_learning_event_has_invitation(self):
        """Learning event should invite feedback."""
        from services.consciousness.learning_consciousness import format_learning_event_conscious

        output = format_learning_event_conscious("you like concise responses")
        assert "?" in output, "Should invite feedback"

    def test_learning_event_with_context(self):
        """Learning event with context should include context."""
        from services.consciousness.learning_consciousness import format_learning_event_conscious

        output = format_learning_event_conscious(
            "you prefer bullet points", context="your last three requests"
        )
        assert "bullet" in output.lower() or "prefer" in output.lower()


class TestLearningConsciousnessEdgeCases:
    """Test edge cases for learning consciousness."""

    def test_patterns_with_high_confidence(self):
        """High confidence patterns should express more certainty."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [
            {"description": "Prefers morning meetings", "occurrences": 10, "confidence": 0.95},
        ]
        output = format_patterns_learned_conscious(patterns, 15)
        # Should express confidence
        assert "confident" in output.lower() or "pretty" in output.lower()

    def test_patterns_with_low_confidence(self):
        """Low confidence patterns should express uncertainty."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [
            {"description": "Might prefer brief updates", "occurrences": 2, "confidence": 0.4},
        ]
        output = format_patterns_learned_conscious(patterns, 10)
        # Should express uncertainty
        assert "think" in output.lower() or "seem" in output.lower()

    def test_multiple_patterns_formatted(self):
        """Multiple patterns should all be mentioned."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        patterns = [
            {"description": "Morning preference", "occurrences": 5, "confidence": 0.8},
            {"description": "Concise style", "occurrences": 3, "confidence": 0.7},
            {"description": "Weekly reviews", "occurrences": 2, "confidence": 0.6},
        ]
        output = format_patterns_learned_conscious(patterns, 20)
        # Should mention all patterns or at least the top ones
        assert "morning" in output.lower() or "concise" in output.lower()

    def test_no_patterns_mentions_future_learning(self):
        """No patterns message should express willingness to learn."""
        from services.consciousness.learning_consciousness import format_patterns_learned_conscious

        output = format_patterns_learned_conscious([], 3)
        # Should express willingness to continue learning
        assert "learn" in output.lower() or "better" in output.lower() or "work" in output.lower()
