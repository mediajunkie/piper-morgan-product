"""Tests for `services.ethics.privacy_types` — #1089 Phase 0 increment 1.

Verifies the PrivacyLevel + FilterReason enum contracts the rest of the
KG-Privacy-Filter implementation depends on:

- Both enums are string-valued (JSON-serializable + comparable to literals)
- PrivacyLevel.STANDARD is the canonical default
- All ratified values present (matches the #1089 design substrate)
- No surprise renames / typos that would break downstream wiring
"""

from services.ethics.privacy_types import FilterReason, PrivacyLevel


class TestPrivacyLevel:
    """PrivacyLevel enum contract — the three ratified levels and their string values."""

    def test_three_levels_exist(self):
        """Ratified levels: public, standard, strict (HOST Q2 reply)."""
        assert PrivacyLevel.PUBLIC.value == "public"
        assert PrivacyLevel.STANDARD.value == "standard"
        assert PrivacyLevel.STRICT.value == "strict"

    def test_exactly_three_members(self):
        """No accidental extra levels — three-level semantics are the design."""
        assert len(list(PrivacyLevel)) == 3

    def test_string_comparison_works(self):
        """str-mixin lets callers pass literal strings interchangeably."""
        assert PrivacyLevel.STANDARD == "standard"
        assert PrivacyLevel.PUBLIC == "public"
        assert PrivacyLevel.STRICT == "strict"

    def test_membership_check_via_value(self):
        """Lookup by string value (for deserializing from API / config / DB)."""
        assert PrivacyLevel("public") is PrivacyLevel.PUBLIC
        assert PrivacyLevel("standard") is PrivacyLevel.STANDARD
        assert PrivacyLevel("strict") is PrivacyLevel.STRICT

    def test_distinct_values(self):
        """Each member has a distinct value — no aliasing surprises."""
        values = [level.value for level in PrivacyLevel]
        assert len(set(values)) == len(values)


class TestFilterReason:
    """FilterReason enum contract — category-not-content audit discipline."""

    def test_ratified_reasons_exist(self):
        """HOST Q2-ratified initial set: harassment / inappropriate / principle-violation."""
        assert FilterReason.HARASSMENT_PATTERN_MATCHED.value == "harassment_pattern_matched"
        assert FilterReason.INAPPROPRIATE_CONTENT_MATCHED.value == "inappropriate_content_matched"
        assert FilterReason.BOUNDARY_PRINCIPLE_VIOLATION.value == "boundary_principle_violation"

    def test_initial_set_has_three_members(self):
        """Three-reason initial set per HOST Q2; future expansion adds members."""
        assert len(list(FilterReason)) == 3

    def test_string_comparison_works(self):
        """str-mixin parity with PrivacyLevel — audit-log payloads can use either."""
        assert FilterReason.HARASSMENT_PATTERN_MATCHED == "harassment_pattern_matched"

    def test_membership_check_via_value(self):
        """Lookup from audit-log entries serialized as plain strings."""
        assert FilterReason("harassment_pattern_matched") is FilterReason.HARASSMENT_PATTERN_MATCHED
        assert FilterReason("inappropriate_content_matched") is FilterReason.INAPPROPRIATE_CONTENT_MATCHED
        assert FilterReason("boundary_principle_violation") is FilterReason.BOUNDARY_PRINCIPLE_VIOLATION

    def test_distinct_values(self):
        """No accidental duplicate string values across reason members."""
        values = [reason.value for reason in FilterReason]
        assert len(set(values)) == len(values)


class TestModuleSurface:
    """Module-level export contract — downstream files import these two names."""

    def test_public_exports(self):
        """`__all__` lists exactly the two enum classes."""
        from services.ethics import privacy_types

        assert set(privacy_types.__all__) == {"PrivacyLevel", "FilterReason"}
