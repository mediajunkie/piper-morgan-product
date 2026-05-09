"""
Tests for KeyLeakDetector — honest "unknown" semantics (#932).

Phase 3 of the #932 audit-cascade gameplan: lock in that
KeyLeakDetector.check_key_leaked() returns honest "unknown" results when no
real leak-DB lookup has been performed, while preserving the existing
quick-check behavior for known test keys and weak patterns.

PM Disposition (2026-05-09): Option C — honest "unknown" semantics.
Audit-cascade reference: dev/2026/05/09/932-issue-audit.md
Gameplan reference: dev/2026/05/09/932-gameplan.md
"""

import pytest

from services.security.key_leak_detector import KeyLeakDetector, LeakCheckResult


class TestKeyLeakDetectorHonestUnknown:
    """Tests for honest 'unknown' semantics introduced in #932."""

    @pytest.fixture
    def detector(self):
        """KeyLeakDetector instance for testing."""
        return KeyLeakDetector()

    @pytest.mark.asyncio
    async def test_check_key_leaked_returns_unknown_for_unrecognized_key(self, detector):
        """A key that passes all quick-checks should return 'unknown', not 'ok'.

        This is the load-bearing assertion for the honest-semantics fix:
        when we haven't actually performed a leak-DB lookup, we must NOT
        claim the key is safe. We must report we didn't check.
        """
        # Realistic-looking key with high entropy, mixed case, no test/weak
        # patterns, no sequential or keyboard runs. Designed to slip past all
        # _quick_leak_checks branches.
        unrecognized_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        result = await detector.check_key_leaked(unrecognized_key)

        assert isinstance(result, LeakCheckResult)
        assert result.leaked is False
        assert result.severity == "unknown"
        assert result.confidence == 0.0
        assert result.recommendation is not None
        assert "not yet implemented" in result.recommendation.lower()

    @pytest.mark.asyncio
    async def test_check_key_leaked_returns_critical_for_known_test_key(self, detector):
        """Known test keys must continue to be flagged critical (existing behavior preserved).

        Quick-check path: api_key.lower() in self.known_test_keys.
        """
        # From _load_known_test_keys()
        known_test_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"

        result = await detector.check_key_leaked(known_test_key)

        assert result.leaked is True
        assert result.severity == "critical"
        assert result.confidence >= 0.9
        assert result.source == "Known test key database"

    @pytest.mark.asyncio
    async def test_check_key_leaked_returns_critical_for_weak_pattern(self, detector):
        """Keys containing weak patterns must continue to be flagged critical.

        Quick-check path: any pattern in self.weak_patterns appears in the key.
        Uses '1234567890' which is one of the canonical weak patterns.
        """
        weak_pattern_key = "sk-real1234567890morestuffafterthat"

        result = await detector.check_key_leaked(weak_pattern_key)

        assert result.leaked is True
        assert result.severity == "critical"
        assert result.confidence >= 0.9
        assert result.source == "Weak pattern detection"
