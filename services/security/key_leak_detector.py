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
    """Result of leak detection check"""

    leaked: bool
    source: Optional[str] = None
    severity: str = "ok"  # 'ok', 'warning', 'critical'
    recommendation: Optional[str] = None
    confidence: float = 1.0  # 0.0 to 1.0


class KeyLeakDetector:
    """Detects if API keys have been leaked or compromised"""

    def __init__(self):
        """Initialize leak detector"""
        self.known_test_keys = self._load_known_test_keys()
        self.weak_patterns = self._load_weak_patterns()

    def _load_known_test_keys(self) -> set:
        """Load known test/example keys that should never be used"""
        # Common test keys and examples from documentation
        test_keys = {
            # OpenAI examples
            "sk-1234567890abcdef1234567890abcdef1234567890abcdef",
            "sk-proj-1234567890abcdef1234567890abcdef1234567890abcdef",
            "sk-test1234567890abcdef1234567890abcdef1234567890",
            # Anthropic examples
            "sk-ant-api03-1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            # GitHub examples
            "ghp_1234567890abcdef1234567890abcdef12345678",
            "gho_1234567890abcdef1234567890abcdef12345678",
            # Common placeholder patterns
            "your-api-key-here",
            "replace-with-your-key",
            "example-api-key",
            "test-api-key",
            "demo-key-123",
        }

        return {key.lower() for key in test_keys}

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

            # TODO(#932): Implement actual HIBP integration
            # Returns false safe result until implemented — tracked as security issue
            return LeakCheckResult(
                leaked=False,
                source=None,
                severity="ok",
                recommendation=None,
                confidence=0.8,  # Lower confidence without full check
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
        if api_key.lower() in self.known_test_keys:
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
