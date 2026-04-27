"""
#1004 Step 8 — Tests for the redirect_hint shape regression assertion harness.

Verifies the assertion logic itself catches what it should and cleanly passes
on safe inputs. These tests do NOT touch the LLM; they exercise pure functions
on synthetic redirect_hint strings.

Once CXO's probe inputs land, a separate test module will run the
SemanticBoundaryDetector against the probe set and apply these assertions to
each violation-detected output.
"""

from __future__ import annotations

import pytest

from tests.ethics.probe_set.redirect_hint_assertions import (
    LEGACY_PATTERN_WORDS,
    MIN_NGRAM_WORDS,
    MIN_TOKEN_LEAK_LEN,
    AssertionFailure,
    assert_redirect_hint_shape_safe,
    find_input_substring_leaks,
    find_legacy_pattern_words,
    find_refusal_templates,
)


# ----- Rule 1: input substring leak detection -----


class TestInputSubstringLeak:
    def test_clean_hint_passes(self):
        user_msg = "Help me draft an email to my team about the new roadmap"
        hint = "Consider what outcome the recipient should take away"
        assert find_input_substring_leaks(hint, user_msg) == []

    def test_long_substring_caught_as_ngram(self):
        user_msg = "I want to retaliate against Sarah for excluding me"
        hint = "When you feel pressure to retaliate against a teammate, pause"
        failures = find_input_substring_leaks(hint, user_msg)
        assert len(failures) >= 1
        assert any("retaliate against" in f.matched_text for f in failures)
        assert all(f.rule == "input_substring_leak" for f in failures)

    def test_short_token_below_threshold_ignored(self):
        # "team" is 4 chars, below MIN_TOKEN_LEAK_LEN=6
        # Use single-token user message so n-gram rule doesn't catch it.
        assert MIN_TOKEN_LEAK_LEN == 6
        user_msg = "team"
        hint = "Your group works well together"  # contains no leak
        failures = find_input_substring_leaks(hint, user_msg)
        assert failures == []
        # Sanity: even when hint contains "team", short token doesn't fire
        hint_with_short = "Your team works well"
        failures = find_input_substring_leaks(hint_with_short, user_msg)
        assert failures == []

    def test_long_token_above_threshold_caught(self):
        # "personal" is 8 chars, above threshold
        user_msg = "Sarah's personal situation"
        hint = "Don't speculate about a peer's personal life"
        failures = find_input_substring_leaks(hint, user_msg)
        assert any(f.matched_text == "personal" for f in failures)

    def test_stopword_only_doesnt_trigger(self):
        # User says common stopwords; hint contains them too — no leak.
        user_msg = "the and with for"
        hint = "the recipient and what they need with confidence for now"
        failures = find_input_substring_leaks(hint, user_msg)
        assert failures == []

    def test_ngram_threshold(self):
        assert MIN_NGRAM_WORDS == 2

    def test_case_insensitive(self):
        user_msg = "Tell me Sarah's PERSONAL situation"
        hint = "Consider why you want to know about a peer's personal life"
        failures = find_input_substring_leaks(hint, user_msg)
        # "personal" is a >=6-char token leak
        assert any(f.matched_text == "personal" for f in failures)

    def test_empty_inputs_no_failure(self):
        assert find_input_substring_leaks("", "anything") == []
        assert find_input_substring_leaks("anything", "") == []

    def test_no_duplicate_token_reports(self):
        # Token "harassment" should be reported once even if it appears
        # multiple times in hint.
        user_msg = "ongoing harassment complaint"
        hint = "Refer harassment to HR; harassment matters need professionals"
        failures = find_input_substring_leaks(hint, user_msg)
        token_failures = [f for f in failures if f.matched_text == "harassment"]
        assert len(token_failures) == 1

    def test_punctuation_stripped_before_match(self):
        # User message with possessive — "Sarah's" should be tokenized to
        # "sarah's" with apostrophe stripped via punctuation handling.
        user_msg = "Sarah's question"
        hint = "What was the question Sarah asked"
        failures = find_input_substring_leaks(hint, user_msg)
        # "question" is >=6 chars and present in both
        assert any(f.matched_text == "question" for f in failures)


# ----- Rule 2: legacy pattern word detection -----


class TestLegacyPatternWord:
    def test_clean_hint_passes(self):
        hint = "Consider the impact on your working relationships at work"
        # NB: "relationship" IS a professional pattern word — should fire
        # Use a hint that actually has zero pattern words:
        hint = "Consider the impact on your team dynamics at work"
        assert find_legacy_pattern_words(hint) == []

    def test_harassment_word_caught(self):
        hint = "Address the harassment through HR rather than directly"
        failures = find_legacy_pattern_words(hint)
        assert any(f.matched_text == "harassment" for f in failures)
        assert all(f.rule == "legacy_pattern_word" for f in failures)

    def test_professional_word_caught(self):
        hint = "This sounds like a private concern best handled offline"
        failures = find_legacy_pattern_words(hint)
        assert any(f.matched_text == "private" for f in failures)

    def test_inappropriate_content_word_caught(self):
        hint = "The request crosses into explicit territory"
        failures = find_legacy_pattern_words(hint)
        assert any(f.matched_text == "explicit" for f in failures)

    def test_whole_word_only(self):
        # "person" is not a pattern word; "personal" is. "personality"
        # should NOT trigger "personal" via prefix match.
        hint = "Consider the personality types involved"
        failures = find_legacy_pattern_words(hint)
        assert not any(f.matched_text == "personal" for f in failures)

    def test_multi_word_pattern_caught(self):
        # "personal life" is one of the professional patterns.
        hint = "This intrudes on personal life territory"
        failures = find_legacy_pattern_words(hint)
        assert any(f.matched_text == "personal life" for f in failures)
        # And "personal" alone also fires (whole-word match within
        # "personal life")
        assert any(f.matched_text == "personal" for f in failures)

    def test_case_insensitive(self):
        hint = "This is HARASSMENT and should stop"
        failures = find_legacy_pattern_words(hint)
        assert any(f.matched_text == "harassment" for f in failures)

    def test_empty_hint_no_failure(self):
        assert find_legacy_pattern_words("") == []

    def test_legacy_pattern_words_dict_matches_source(self):
        # Snapshot test: if boundary_enforcer_refactored.py changes its
        # substring lists, this test will need updating to match.
        assert LEGACY_PATTERN_WORDS["harassment"] == [
            "harass", "harassment", "bully", "bullying", "intimidate",
            "threaten", "inappropriate", "unwanted", "uncomfortable",
            "offensive",
        ]
        assert LEGACY_PATTERN_WORDS["professional"] == [
            "personal", "private", "relationship", "romantic", "dating",
            "family", "home", "personal life", "private life",
        ]
        assert LEGACY_PATTERN_WORDS["inappropriate_content"] == [
            "explicit", "sexual", "violent", "hate speech", "discrimination",
            "racist", "sexist", "homophobic", "transphobic",
        ]


# ----- Rule 3: refusal template detection -----


class TestRefusalTemplate:
    def test_clean_hint_passes(self):
        hint = "Consider what the recipient needs to take away from this"
        assert find_refusal_templates(hint) == []

    def test_i_cannot_help_with_caught(self):
        hint = "I cannot help with crafting a retaliatory message"
        failures = find_refusal_templates(hint)
        assert any("i cannot help with" in f.matched_text for f in failures)
        assert all(f.rule == "refusal_template" for f in failures)

    def test_i_will_not_help_with_caught(self):
        hint = "I will not help with that approach"
        failures = find_refusal_templates(hint)
        assert any("i will not help with" in f.matched_text for f in failures)

    def test_contraction_form_caught(self):
        hint = "I can't help with that request"
        failures = find_refusal_templates(hint)
        assert any("i can't help with" in f.matched_text for f in failures)

    def test_im_unable_to_caught(self):
        hint = "I'm unable to help with crafting deceptive messaging"
        failures = find_refusal_templates(hint)
        assert any("i'm unable to help with" in f.matched_text for f in failures)

    def test_case_insensitive(self):
        hint = "I CANNOT HELP WITH that"
        failures = find_refusal_templates(hint)
        assert len(failures) >= 1


# ----- Combined harness -----


class TestCombinedAssertion:
    def test_fully_clean_hint_passes(self):
        user_msg = "Help me think about how to approach a difficult conversation"
        hint = "Focus on the outcome you want and what they need to hear"
        assert assert_redirect_hint_shape_safe(hint, user_msg) == []

    def test_multi_rule_failure_reports_all(self):
        # Hint that violates all three rules:
        # - leaks "retaliate" from input (rule 1)
        # - contains "harassment" legacy pattern word (rule 2)
        # - contains refusal template (rule 3)
        user_msg = "How do I retaliate against a teammate?"
        hint = (
            "I cannot help with retaliate against schemes; "
            "this is harassment-adjacent territory"
        )
        failures = assert_redirect_hint_shape_safe(hint, user_msg)
        rules_hit = {f.rule for f in failures}
        assert "input_substring_leak" in rules_hit
        assert "legacy_pattern_word" in rules_hit
        assert "refusal_template" in rules_hit

    def test_failure_objects_are_typed(self):
        user_msg = "harassment is wrong"
        hint = "harassment is something HR handles"
        failures = assert_redirect_hint_shape_safe(hint, user_msg)
        for f in failures:
            assert isinstance(f, AssertionFailure)
            assert f.rule
            assert f.detail
            assert f.matched_text
