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
from tests.utils.made_up_credentials import GOOD_OPENAI_KEY, joined, openai_key


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
        unrecognized_key = GOOD_OPENAI_KEY

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

        Quick-check path: the key's digest is in self.known_test_key_digests. The list
        holds digests, not keys (issue 2397), so this adds a made-up key's digest to it.
        """
        known_test_key = openai_key("on the detector's list for this test")
        detector.known_test_key_digests = detector.known_test_key_digests | {
            KeyLeakDetector._digest(known_test_key)
        }

        result = await detector.check_key_leaked(known_test_key)

        assert result.leaked is True
        assert result.severity == "critical"
        assert result.confidence >= 0.9
        assert result.source == "Known test key database"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("placeholder", ("your-api-key-here", "Test-API-Key", "DEMO-KEY-123"))
    async def test_a_placeholder_on_the_shipped_list_is_critical(self, detector, placeholder):
        """The shipped list, untouched: a placeholder is caught in any letter case."""
        result = await detector.check_key_leaked(placeholder)

        assert result.leaked is True
        assert result.source == "Known test key database"
        assert result.confidence == 1.0

    def test_the_shipped_list_holds_digests_and_no_key(self, detector):
        """Issue 2397: every entry is a SHA-256 hex digest, so the source file holds no
        credential-shaped value, and the six published examples are still listed."""
        digests = detector.known_test_key_digests
        assert all(len(d) == 64 and set(d) <= set("0123456789abcdef") for d in digests)
        assert len(digests) == 6 + 5  # published example keys + placeholders

    def test_the_digest_ignores_letter_case(self):
        assert KeyLeakDetector._digest("AbC") == KeyLeakDetector._digest("abc")
        assert KeyLeakDetector._digest("abc") != KeyLeakDetector._digest("abd")

    @pytest.mark.asyncio
    async def test_check_key_leaked_returns_critical_for_weak_pattern(self, detector):
        """Keys containing weak patterns must continue to be flagged critical.

        Quick-check path: any pattern in self.weak_patterns appears in the key.
        Uses '1234567890' which is one of the canonical weak patterns.
        """
        weak_pattern_key = joined("sk", "-", "real1234567890morestuffafterthat")

        result = await detector.check_key_leaked(weak_pattern_key)

        assert result.leaked is True
        assert result.severity == "critical"
        assert result.confidence >= 0.9
        assert result.source == "Weak pattern detection"
