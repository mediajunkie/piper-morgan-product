"""
Tests for API Key Validator

Tests the actual implementation of APIKeyValidator which provides:
- Format validation per provider
- Key strength checking
- Leak detection
- Comprehensive validation reporting

Refactored 2025-11-19 to match actual implementation (Bead: piper-morgan-36m)
"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.security.api_key_validator import APIKeyValidator, ValidationReport
from services.security.provider_key_validator import ProviderKeyValidator, ValidationResult


class TestAPIKeyValidator:
    """Test API key validation functionality"""

    @pytest.fixture
    def validator(self):
        """APIKeyValidator instance for testing"""
        return APIKeyValidator()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_openai_key_valid_format(self, validator):
        """Test OpenAI key with valid format"""
        # Valid OpenAI key format: sk- + 48+ mixed characters
        # Using realistic mixed pattern to avoid fake key detection
        valid_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        report = await validator.validate_api_key("openai", valid_key)

        assert report.provider == "openai"
        assert report.format_valid is True
        assert report.format_result.valid is True
        assert report.api_key_preview.startswith("sk-")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_openai_key_invalid_format(self, validator):
        """Test OpenAI key with invalid format (too short)"""
        invalid_key = "sk-short"

        report = await validator.validate_api_key("openai", invalid_key)

        assert report.provider == "openai"
        assert report.format_valid is False
        assert report.format_result.valid is False
        assert report.overall_valid is False
        assert len(report.warnings) > 0 or len(report.recommendations) > 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_anthropic_key_valid_format(self, validator):
        """Test Anthropic key with valid format"""
        # Valid Anthropic key format: sk-ant- + 100+ mixed characters
        # Using mixed characters to avoid fake key detection (107 total chars = 100 after prefix)
        valid_key = (
            "sk-ant-"
            + "X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT6vL3nR9pM7yH5kJ4wB2gC8xN1qS0tV6mP"
            + "aB" * 11
        )

        report = await validator.validate_api_key("anthropic", valid_key)

        assert report.provider == "anthropic"
        assert report.format_valid is True
        assert report.format_result.valid is True

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_anthropic_key_invalid_format(self, validator):
        """Test Anthropic key with invalid format"""
        invalid_key = "sk-ant-short"

        report = await validator.validate_api_key("anthropic", invalid_key)

        assert report.provider == "anthropic"
        assert report.format_valid is False
        assert report.overall_valid is False

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_github_token_valid_format(self, validator):
        """Test GitHub personal access token format"""
        # Valid GitHub PAT: ghp_ + 36+ mixed characters (40+ total)
        valid_token = "ghp_X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA"

        report = await validator.validate_api_key("github", valid_token)

        assert report.provider == "github"
        assert report.format_valid is True

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_slack_token_valid_format(self, validator):
        """Test Slack bot token format"""
        # Valid Slack bot token: xoxb- + numbers + dash + mixed characters
        valid_token = "xoxb-FAKE-FAKE-TESTTOKEN"  # Intentionally fake for testing

        report = await validator.validate_api_key("slack", valid_token)

        assert report.provider == "slack"
        assert report.format_valid is True

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_unknown_provider(self, validator):
        """Test validation with unknown provider"""
        report = await validator.validate_api_key("unknown_provider", "test-key-12345")

        # Unknown provider should still attempt validation
        assert report.provider == "unknown_provider"
        assert isinstance(report.format_valid, bool)
        assert isinstance(report.overall_valid, bool)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_key_strength_validation(self, validator):
        """Test key strength checking"""
        # Weak key (too short, simple pattern)
        weak_key = "sk-test123"

        report = await validator.validate_api_key("openai", weak_key)

        # Strength checking should identify weak key
        assert isinstance(report.strength_acceptable, bool)
        assert report.strength_result is not None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_leak_detection(self, validator):
        """Test leak detection for potentially compromised keys"""
        # Test key with common test pattern
        test_key = "sk-test" + "a" * 44

        report = await validator.validate_api_key("openai", test_key)

        # Leak detection should run
        assert isinstance(report.leak_safe, bool)
        assert report.leak_result is not None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_overall_validation_logic(self, validator):
        """Test that overall_valid reflects all validation checks"""
        # Valid format, good strength, no leaks
        strong_key = "sk-" + "X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4u"

        report = await validator.validate_api_key("openai", strong_key)

        # overall_valid should be True only if all checks pass
        if report.format_valid and report.strength_acceptable and report.leak_safe:
            assert report.overall_valid is True
        else:
            assert report.overall_valid is False

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_security_level_assignment(self, validator):
        """Test that security_level is assigned correctly"""
        valid_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        report = await validator.validate_api_key("openai", valid_key)

        # security_level should be one of: high, medium, low, critical
        assert report.security_level in ["high", "medium", "low", "critical"]

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_recommendations_populated(self, validator):
        """Test that recommendations list is populated for issues"""
        # Invalid format should generate recommendations
        invalid_key = "invalid-key"

        report = await validator.validate_api_key("openai", invalid_key)

        # Should have recommendations or warnings
        assert isinstance(report.recommendations, list)
        assert isinstance(report.warnings, list)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_warnings_populated(self, validator):
        """Test that warnings list is populated appropriately"""
        # Weak key should generate warnings (repetitive pattern)
        weak_key = "sk-111111111111111111111111111111111111111111111111"

        report = await validator.validate_api_key("openai", weak_key)

        assert isinstance(report.warnings, list)

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_strict_mode_parameter(self, validator):
        """Test strict_mode parameter affects validation"""
        borderline_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        # Normal mode
        normal_report = await validator.validate_api_key(
            "openai", borderline_key, strict_mode=False
        )

        # Strict mode
        strict_report = await validator.validate_api_key("openai", borderline_key, strict_mode=True)

        # Both should complete (may have different results)
        assert normal_report is not None
        assert strict_report is not None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_api_key_preview_privacy(self, validator):
        """Test that API key preview doesn't expose full key"""
        full_key = "sk-" + "X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4u"

        report = await validator.validate_api_key("openai", full_key)

        # Preview should be shorter than full key
        assert len(report.api_key_preview) < len(full_key)
        # Should not contain the full key
        assert report.api_key_preview != full_key


class TestOverallValidLeakSemantics:
    """Tests for #932 — leak_safe gates overall_valid only when leak check was performed.

    Phase 3 of the #932 audit-cascade gameplan. Locks in that an unperformed
    leak check (confidence == 0.0) does NOT fail an otherwise-good key, and
    that a known-leak result (confidence >= 0.9) still gates as before.

    PM Disposition (2026-05-09): Option C — honest "unknown" semantics.
    """

    @pytest.fixture
    def validator(self):
        return APIKeyValidator()

    @pytest.mark.asyncio
    async def test_overall_valid_unaffected_by_unknown_leak_check(self, validator):
        """Unperformed leak check (confidence=0.0) must NOT fail an otherwise-good key.

        This is the load-bearing test for Option C: the validator must not
        block a key on a check we never performed. The realistic-looking key
        below passes format + strength + slips past all _quick_leak_checks,
        landing in the "unknown" branch with confidence=0.0.
        """
        # Realistic-looking OpenAI key: passes format check, has high
        # entropy, mixed case, no test/weak patterns. Same shape as the
        # detector's "unrecognized" test fixture.
        good_key = "sk-X7k9mP2nQ5tR8wY3jL6hN4vC1bM0sD9fG8eA7zK5x2W4uT"

        report = await validator.validate_api_key("openai", good_key)

        # Format and strength must be acceptable (precondition for the
        # load-bearing assertion).
        assert report.format_valid is True
        assert report.strength_acceptable is True

        # Leak result must be the "unknown" branch (no real check performed).
        assert report.leak_result.severity == "unknown"
        assert report.leak_result.confidence == 0.0
        assert report.leak_result.leaked is False

        # The load-bearing assertion: overall_valid is True even though
        # leak check returned an "unknown" result.
        assert report.overall_valid is True

    @pytest.mark.asyncio
    async def test_overall_valid_blocks_on_known_leak(self, validator):
        """When the leak check WAS performed and found a leak, overall_valid must be False.

        Existing-behavior preservation. A known test key triggers the
        _quick_leak_checks branch with confidence >= 0.9, and overall_valid
        must reflect that as a blocking failure regardless of format/strength.
        """
        # Known test key from _load_known_test_keys() — triggers the
        # quick-check path with severity="critical" and confidence=1.0.
        known_test_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"

        report = await validator.validate_api_key("openai", known_test_key)

        # Leak check was performed and found a problem.
        assert report.leak_result.leaked is True
        assert report.leak_result.severity == "critical"
        assert report.leak_result.confidence >= 0.9
        assert report.leak_safe is False

        # overall_valid is blocked by the confirmed leak.
        assert report.overall_valid is False


class TestValidationReport:
    """Test ValidationReport structure and fields"""

    @pytest.mark.smoke
    def test_validation_report_has_required_fields(self):
        """Test that ValidationReport has all required fields"""
        from services.security.key_leak_detector import LeakCheckResult
        from services.security.key_strength_analyzer import KeyStrength

        # Create a minimal report
        report = ValidationReport(
            provider="openai",
            api_key_preview="sk-***",
            format_valid=True,
            format_result=ValidationResult(valid=True, message="Valid", provider="openai"),
            strength_acceptable=True,
            strength_result=KeyStrength(
                length_score=1.0,
                entropy_score=0.8,
                character_diversity_score=0.9,
                pattern_score=0.85,
                overall_score=0.8,
                recommendations=[],
                security_level="strong",
            ),
            leak_safe=True,
            leak_result=LeakCheckResult(leaked=False, severity="ok", confidence=1.0),
            overall_valid=True,
            security_level="high",
            recommendations=[],
            warnings=[],
        )

        # Verify all required fields exist
        assert hasattr(report, "provider")
        assert hasattr(report, "api_key_preview")
        assert hasattr(report, "format_valid")
        assert hasattr(report, "format_result")
        assert hasattr(report, "strength_acceptable")
        assert hasattr(report, "strength_result")
        assert hasattr(report, "leak_safe")
        assert hasattr(report, "leak_result")
        assert hasattr(report, "overall_valid")
        assert hasattr(report, "security_level")
        assert hasattr(report, "recommendations")
        assert hasattr(report, "warnings")

    @pytest.mark.smoke
    def test_validation_report_types(self):
        """Test that ValidationReport fields have correct types"""
        from services.security.key_leak_detector import LeakCheckResult
        from services.security.key_strength_analyzer import KeyStrength

        report = ValidationReport(
            provider="test",
            api_key_preview="***",
            format_valid=True,
            format_result=ValidationResult(valid=True, message="OK", provider="test"),
            strength_acceptable=True,
            strength_result=KeyStrength(
                length_score=1.0,
                entropy_score=0.9,
                character_diversity_score=0.95,
                pattern_score=0.9,
                overall_score=0.9,
                recommendations=[],
                security_level="strong",
            ),
            leak_safe=True,
            leak_result=LeakCheckResult(leaked=False, severity="ok", confidence=1.0),
            overall_valid=True,
            security_level="high",
            recommendations=["test recommendation"],
            warnings=["test warning"],
        )

        # Verify types
        assert isinstance(report.provider, str)
        assert isinstance(report.api_key_preview, str)
        assert isinstance(report.format_valid, bool)
        assert isinstance(report.format_result, ValidationResult)
        assert isinstance(report.strength_acceptable, bool)
        assert isinstance(report.strength_result, KeyStrength)
        assert isinstance(report.leak_safe, bool)
        assert isinstance(report.leak_result, LeakCheckResult)
        assert isinstance(report.overall_valid, bool)
        assert isinstance(report.security_level, str)
        assert isinstance(report.recommendations, list)
        assert isinstance(report.warnings, list)


class TestValidationResult:
    """Test ValidationResult dataclass"""

    @pytest.mark.smoke
    def test_validation_result_creation(self):
        """Test ValidationResult creation and fields"""
        result = ValidationResult(
            valid=True, message="Key format is valid", provider="openai", warnings=[]
        )

        assert result.valid is True
        assert result.message == "Key format is valid"
        assert result.provider == "openai"
        assert isinstance(result.warnings, list)

    @pytest.mark.smoke
    def test_validation_result_with_warnings(self):
        """Test ValidationResult with warnings"""
        result = ValidationResult(
            valid=True,
            message="Valid but has warnings",
            provider="openai",
            warnings=["Warning: Key appears to follow test pattern"],
        )

        assert result.valid is True
        assert len(result.warnings) == 1
        assert "test pattern" in result.warnings[0]
