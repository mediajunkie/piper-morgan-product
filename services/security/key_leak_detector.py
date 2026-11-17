"""
API Key Leak Detection Service

Checks if API keys appear in public leak databases or have been compromised.
Provides security warnings and recommendations for leaked keys.

Issue #252 CORE-KEYS-STRENGTH-VALIDATION
"""

import hashlib
import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LeakCheckResult:
    """Result of leak detection check.

    severity values:
      'ok'       — checked, no leak found
      'unknown'  — leak DB lookup not performed (no real lookup wired yet, #932)
      'warning'  — checked, low-confidence concern
      'critical' — checked, leak confirmed

    confidence: 0.0 means "no actual check was performed" (treat result as
    informational only); >0.0 means "we did check and this is our certainty."
    """

    leaked: bool
    source: Optional[str] = None
    severity: str = "ok"  # 'ok' | 'unknown' | 'warning' | 'critical'
    recommendation: Optional[str] = None
    confidence: float = 1.0  # 0.0 to 1.0; 0.0 = check not performed


class KeyLeakDetector:
    """Detects if API keys have been leaked or compromised"""

    def __init__(self):
        """Initialize leak detector"""
        self.known_test_key_digests = self._load_known_test_key_digests()
        self.weak_patterns = self._load_weak_patterns()

    @staticmethod
    def _digest(api_key: str) -> str:
        """SHA-256 of the lower-cased key: the form the deny-list is stored and compared in."""
        return hashlib.sha256(api_key.lower().encode("utf-8")).hexdigest()

    def _load_known_test_key_digests(self) -> set:
        """Digests of known test/example keys that should never be used.

        Issue 2397 (Arch 2026-11-16): the published example keys are stored as the SHA-256
        of their lower-cased value, never as the value, so this public file holds no
        credential-shaped run. A candidate key is compared by its digest. To add a
        published example, add its digest (``KeyLeakDetector._digest(value)``), not the value.
        """
        published_example_digests = {
            # OpenAI examples
            "e6e9657b0d9e20bb956d81de6d96f927f8b4a76882c775b22bd5b02e8d6c590e",
            "e8b4b69691671955fee34570ab0f96790ad922c82552fe6b135390db7f7ff407",
            "9f44dd4c53ab8c4b1af9ed29347262caebc58430668ad2b53dffa530bb3ea142",
            # Anthropic examples
            "2edfb8210a24a60391737d6e294f7a869714fee473d587f113ff7562f5434c77",
            # GitHub examples
            "bf0316155996e95e18790be9064962d84ab4a6befce3d9563cf5b78d6226a2cb",
            "a7bc1cd9e096b298c96501b8d2ce13219cde43275fdbd4fc0259539a94c5bf6c",
        }
        # Common placeholder patterns: not credential-shaped, kept readable.
        placeholders = {
            "your-api-key-here",
            "replace-with-your-key",
            "example-api-key",
            "test-api-key",
            "demo-key-123",
        }
        return published_example_digests | {self._digest(key) for key in placeholders}

    def _load_weak_patterns(self) -> List[str]:
        """Load patterns that indicate weak or test keys"""
        return [
            r"test",
            r"demo",
            r"example",
            r"sample",
            r"placeholder",
            r"your-key",
            r"replace",
            r"1234567890",
            r"abcdefgh",
            r"qwertyui",
        ]

    async def check_key_leaked(self, api_key: str, provider: str = None) -> LeakCheckResult:
        """
        Check if API key appears in public leak databases

        Args:
            api_key: API key to check
            provider: Optional provider context

        Returns:
            LeakCheckResult with detection details
        """
        try:
            # Quick checks first (no network required)
            quick_result = self._quick_leak_checks(api_key, provider)
            if quick_result.leaked:
                return quick_result

            # #932 (May 9 PM disposition: Option C honest unknown): no real
            # leak-DB lookup is wired yet. We return "unknown" rather than
            # "safe" so the validator's overall_valid doesn't depend on a
            # check we didn't perform. The local _quick_leak_checks above
            # still catch test keys, weak patterns, and obvious fakes —
            # those return leaked=True with high confidence as before.
            #
            # When a real leak-detection service is selected (HIBP, GitHub
            # secret scanning, curated hash DB, etc.), file a new issue with
            # concrete scope and replace this branch.
            return LeakCheckResult(
                leaked=False,
                source=None,
                severity="unknown",
                recommendation=(
                    "Leak-DB lookup not yet implemented; key passes local "
                    "quick-checks (test key / weak pattern / obvious fake) only."
                ),
                confidence=0.0,  # 0.0 = check not performed
            )

        except Exception as e:
            logger.error(f"Error checking key leak status: {e}")
            return LeakCheckResult(
                leaked=False,
                source=None,
                severity="warning",
                recommendation="Could not verify leak status",
                confidence=0.0,
            )

    def _quick_leak_checks(self, api_key: str, provider: str = None) -> LeakCheckResult:
        """Perform quick local checks for known issues"""

        # Check against known test keys
        if self._digest(api_key) in self.known_test_key_digests:
            return LeakCheckResult(
                leaked=True,
                source="Known test key database",
                severity="critical",
                recommendation="This is a known test/example key. Generate a new key from your provider.",
                confidence=1.0,
            )

        # Check for weak patterns
        api_key_lower = api_key.lower()
        for pattern in self.weak_patterns:
            if pattern in api_key_lower:
                return LeakCheckResult(
                    leaked=True,
                    source="Weak pattern detection",
                    severity="critical",
                    recommendation=f"Key contains weak pattern '{pattern}'. Generate a proper API key.",
                    confidence=0.9,
                )

        # Check for obviously fake keys
        if self._is_obviously_fake(api_key):
            return LeakCheckResult(
                leaked=True,
                source="Fake key detection",
                severity="critical",
                recommendation="This appears to be a placeholder or fake key. Use a real API key.",
                confidence=0.95,
            )

        return LeakCheckResult(leaked=False)

    def _is_obviously_fake(self, api_key: str) -> bool:
        """Check if key is obviously fake or placeholder"""

        # Check for repeated characters
        if len(set(api_key)) < len(api_key) * 0.3:  # Less than 30% unique chars
            return True

        # Check for sequential patterns
        sequences = ["0123456789", "abcdefghij", "ABCDEFGHIJ"]
        for seq in sequences:
            if any(seq[i : i + 5] in api_key for i in range(len(seq) - 4)):
                return True

        # Check for keyboard patterns
        keyboard_patterns = ["qwerty", "asdfgh", "zxcvbn"]
        api_key_lower = api_key.lower()
        for pattern in keyboard_patterns:
            if pattern in api_key_lower:
                return True

        return False

    def _hash_key_for_lookup(self, api_key: str) -> str:
        """Create one-way hash for secure leak database lookup"""
        # Use SHA-256 for one-way hashing
        return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

    async def check_multiple_keys(
        self, keys: List[tuple[str, str]]
    ) -> List[tuple[str, LeakCheckResult]]:
        """
        Check multiple keys for leaks

        Args:
            keys: List of (provider, api_key) tuples

        Returns:
            List of (provider, LeakCheckResult) tuples
        """
        results = []

        for provider, api_key in keys:
            result = await self.check_key_leaked(api_key, provider)
            results.append((provider, result))

        return results

    def get_security_recommendations(self, leak_results: List[LeakCheckResult]) -> List[str]:
        """Generate security recommendations based on leak check results"""
        recommendations = []

        critical_leaks = [r for r in leak_results if r.leaked and r.severity == "critical"]
        warning_leaks = [r for r in leak_results if r.leaked and r.severity == "warning"]

        if critical_leaks:
            recommendations.append(
                "🚨 CRITICAL: Some keys are compromised and must be rotated immediately"
            )
            for leak in critical_leaks:
                if leak.recommendation:
                    recommendations.append(f"  • {leak.recommendation}")

        if warning_leaks:
            recommendations.append("⚠️  WARNING: Some keys may be at risk")
            for leak in warning_leaks:
                if leak.recommendation:
                    recommendations.append(f"  • {leak.recommendation}")

        if not critical_leaks and not warning_leaks:
            recommendations.append("✅ No known leaks detected")

        # General security recommendations
        recommendations.extend(
            [
                "💡 Best practices:",
                "  • Rotate keys regularly (every 90 days)",
                "  • Never commit keys to version control",
                "  • Use environment variables or secure key management",
                "  • Monitor key usage for unusual activity",
            ]
        )

        return recommendations
