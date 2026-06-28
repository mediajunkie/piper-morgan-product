"""
Enhanced API Key Validator

Comprehensive API key validation including format validation, strength analysis,
leak detection, and security recommendations. Integrates all validation components.

Issue #252 CORE-KEYS-STRENGTH-VALIDATION
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from services.security.key_leak_detector import KeyLeakDetector, LeakCheckResult
from services.security.key_strength_analyzer import KeyStrength, KeyStrengthAnalyzer
from services.security.provider_key_validator import ProviderKeyValidator, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ValidationReport:
    """Comprehensive validation report for an API key"""

    provider: str
    api_key_preview: str  # First 8 chars + "..."

    # Validation results
    format_valid: bool
    format_result: ValidationResult

    strength_acceptable: bool
    strength_result: KeyStrength

    leak_safe: bool
    leak_result: LeakCheckResult

    # Overall assessment
    overall_valid: bool
    security_level: str  # 'high', 'medium', 'low', 'critical'
    recommendations: List[str]
    warnings: List[str]

    def __post_init__(self):
        """Ensure lists are initialized"""
        if self.recommendations is None:
            self.recommendations = []
        if self.warnings is None:
            self.warnings = []


class APIKeyValidator:
    """Enhanced API key validator with comprehensive security checks"""

    def __init__(self):
        """Initialize validator with all components"""
        self.format_validator = ProviderKeyValidator()
        self.strength_analyzer = KeyStrengthAnalyzer()
        self.leak_detector = KeyLeakDetector()

    async def validate_api_key(
        self, provider: str, api_key: str, strict_mode: bool = False
    ) -> ValidationReport:
        """
        Perform comprehensive API key validation

        Args:
            provider: Provider name (openai, anthropic, github, etc.)
            api_key: API key to validate
            strict_mode: If True, require strong keys and no warnings

        Returns:
            ValidationReport with comprehensive analysis
        """
        try:
            # Create preview (first 8 chars + "...")
            preview = f"{api_key[:8]}..." if len(api_key) > 8 else api_key

            # 1. Format validation (fast)
            format_result = self.format_validator.validate_format(provider, api_key)
            format_valid = format_result.valid

            # 2. Strength analysis (fast)
            strength_result = self.strength_analyzer.analyze_key_strength(api_key, provider)
            strength_acceptable, _ = self.strength_analyzer.is_key_acceptable(
                strength_result, allow_medium=not strict_mode
            )

            # 3. Leak detection (potentially slow)
            leak_result = await self.leak_detector.check_key_leaked(api_key, provider)
            leak_safe = not leak_result.leaked

            # 4. Overall assessment
            # #932: when leak check wasn't actually performed (confidence=0.0,
            # severity=='unknown'), treat leak_safe as informational rather
            # than blocking. We don't fail a key for a check we didn't do.
            # When the check WAS performed (e.g., local quick-checks found a
            # weak pattern or known test key, returning confidence>=0.9),
            # leak_safe still gates as before.
            leak_check_performed = leak_result.confidence > 0.0
            overall_valid = (
                format_valid
                and strength_acceptable
                and (leak_safe if leak_check_performed else True)
            )

            # 5. Determine security level
            security_level = self._determine_security_level(
                format_result, strength_result, leak_result
            )

            # 6. Generate recommendations and warnings
            recommendations = self._generate_recommendations(
                format_result, strength_result, leak_result, strict_mode
            )
            warnings = self._generate_warnings(format_result, strength_result, leak_result)

            return ValidationReport(
                provider=provider,
                api_key_preview=preview,
                format_valid=format_valid,
                format_result=format_result,
                strength_acceptable=strength_acceptable,
                strength_result=strength_result,
                leak_safe=leak_safe,
                leak_result=leak_result,
                overall_valid=overall_valid,
                security_level=security_level,
                recommendations=recommendations,
                warnings=warnings,
            )

        except Exception as e:
            logger.error(f"Error validating API key for {provider}: {e}")
            return self._create_error_report(provider, api_key, str(e))

    def _determine_security_level(
        self,
        format_result: ValidationResult,
        strength_result: KeyStrength,
        leak_result: LeakCheckResult,
    ) -> str:
        """Determine overall security level"""

        # Critical issues
        if leak_result.leaked and leak_result.severity == "critical":
            return "critical"

        if not format_result.valid:
            return "critical"

        # High security
        if (
            strength_result.security_level == "strong"
            and not leak_result.leaked
            and not format_result.warnings
        ):
            return "high"

        # Medium security
        if strength_result.security_level in ["strong", "medium"] and not leak_result.leaked:
            return "medium"

        # Low security
        return "low"

    def _generate_recommendations(
        self,
        format_result: ValidationResult,
        strength_result: KeyStrength,
        leak_result: LeakCheckResult,
        strict_mode: bool,
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Format issues
        if not format_result.valid:
            recommendations.append(f"❌ Format: {format_result.message}")
            provider_info = self.format_validator.get_provider_info(format_result.provider)
            if provider_info:
                recommendations.append(f"   Expected: {provider_info['description']}")

        # Strength issues
        if strength_result.security_level == "weak":
            recommendations.append("❌ Strength: Key is too weak for secure use")
            recommendations.extend([f"   • {rec}" for rec in strength_result.recommendations])
        elif strength_result.security_level == "medium" and strict_mode:
            recommendations.append("⚠️  Strength: Key acceptable but not optimal for strict mode")
            recommendations.extend([f"   • {rec}" for rec in strength_result.recommendations])

        # Leak issues
        if leak_result.leaked:
            icon = "🚨" if leak_result.severity == "critical" else "⚠️"
            recommendations.append(f"{icon} Security: {leak_result.recommendation}")

        # Positive feedback
        if not recommendations:
            recommendations.append("✅ Key passes all security checks")
            recommendations.append(f"   Security level: {strength_result.security_level}")

        return recommendations

    def _generate_warnings(
        self,
        format_result: ValidationResult,
        strength_result: KeyStrength,
        leak_result: LeakCheckResult,
    ) -> List[str]:
        """Generate warnings for potential issues"""
        warnings = []

        # Format warnings
        warnings.extend(format_result.warnings)

        # Strength warnings
        if strength_result.security_level == "medium":
            warnings.append("Key strength is medium - consider using a stronger key")

        # Leak warnings
        if leak_result.severity == "warning":
            warnings.append(f"Leak check: {leak_result.recommendation}")

        # Confidence warnings
        if leak_result.confidence < 0.8:
            warnings.append("Leak detection confidence is low - manual verification recommended")

        return warnings

    def _create_error_report(self, provider: str, api_key: str, error: str) -> ValidationReport:
        """Create error report when validation fails"""
        preview = f"{api_key[:8]}..." if len(api_key) > 8 else api_key

        return ValidationReport(
            provider=provider,
            api_key_preview=preview,
            format_valid=False,
            format_result=ValidationResult(False, f"Validation error: {error}", provider),
            strength_acceptable=False,
            strength_result=KeyStrength(0, 0, 0, 0, 0, [f"Error: {error}"], "unknown"),
            leak_safe=False,
            leak_result=LeakCheckResult(False, None, "warning", f"Could not check: {error}", 0.0),
            overall_valid=False,
            security_level="critical",
            recommendations=[f"❌ Validation failed: {error}"],
            warnings=["Manual verification required"],
        )

    async def validate_multiple_keys(
        self, keys: List[Tuple[str, str]], strict_mode: bool = False
    ) -> List[ValidationReport]:
        """
        Validate multiple API keys

        Args:
            keys: List of (provider, api_key) tuples
            strict_mode: If True, require strong keys

        Returns:
            List of ValidationReport objects
        """
        reports = []

        for provider, api_key in keys:
            report = await self.validate_api_key(provider, api_key, strict_mode)
            reports.append(report)

        return reports

    def get_validation_summary(self, reports: List[ValidationReport]) -> Dict:
        """Generate summary of validation results"""
        total = len(reports)
        valid = sum(1 for r in reports if r.overall_valid)

        security_levels = {}
        for report in reports:
            level = report.security_level
            security_levels[level] = security_levels.get(level, 0) + 1

        issues = []
        for report in reports:
            if not report.overall_valid:
                issues.append(
                    f"{report.provider}: {report.recommendations[0] if report.recommendations else 'Validation failed'}"
                )

        return {
            "total_keys": total,
            "valid_keys": valid,
            "invalid_keys": total - valid,
            "security_levels": security_levels,
            "issues": issues,
            "overall_status": "secure" if valid == total else "needs_attention",
        }

    def format_validation_report(self, report: ValidationReport) -> str:
        """Format validation report for display"""
        lines = []

        # Header
        lines.append(f"🔑 {report.provider.upper()} Key Validation")
        lines.append(f"Key: {report.api_key_preview}")
        lines.append(f"Security Level: {report.security_level.upper()}")
        lines.append("")

        # Results
        format_icon = "✅" if report.format_valid else "❌"
        lines.append(f"{format_icon} Format: {report.format_result.message}")

        strength_icon = "✅" if report.strength_acceptable else "❌"
        lines.append(
            f"{strength_icon} Strength: {report.strength_result.security_level} ({report.strength_result.overall_score:.0%})"
        )

        leak_icon = "✅" if report.leak_safe else "❌"
        leak_msg = (
            "No leaks detected"
            if report.leak_safe
            else f"Leak detected: {report.leak_result.source}"
        )
        lines.append(f"{leak_icon} Security: {leak_msg}")
        lines.append("")

        # Recommendations
        if report.recommendations:
            lines.append("Recommendations:")
            lines.extend(report.recommendations)
            lines.append("")

        # Warnings
        if report.warnings:
            lines.append("Warnings:")
            for warning in report.warnings:
                lines.append(f"⚠️  {warning}")

        return "\n".join(lines)
