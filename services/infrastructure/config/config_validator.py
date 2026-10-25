"""
Configuration Validator Service

Centralized configuration validation for all integration services.
Validates required configurations at startup to fail fast with clear error messages.

Architecture: CORE-GREAT-2D Configuration Validation
"""

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class ServiceStatus(Enum):
    """Configuration validation status"""

    VALID = "valid"
    MISSING = "missing"
    INVALID = "invalid"
    OPTIONAL = "optional"


@dataclass
class ValidationResult:
    """Result of configuration validation"""

    service: str
    status: ServiceStatus
    message: str
    recovery_suggestion: Optional[str] = None
    config_checked: List[str] = None

    def __post_init__(self):
        if self.config_checked is None:
            self.config_checked = []


class ConfigValidator:
    """
    Validates configuration for all integration services.

    Provides:
    - Centralized validation logic
    - Clear error messages
    - Recovery suggestions
    - Graceful degradation for optional services
    """

    def __init__(self):
        """Initialize configuration validator"""
        self.results: Dict[str, ValidationResult] = {}

    def validate_all(self) -> Dict[str, ValidationResult]:
        """
        Validate all service configurations.

        Returns:
            Dict[str, ValidationResult]: Validation results for each service
        """
        self.results = {
            "github": self._validate_github(),
            "slack": self._validate_slack(),
            "notion": self._validate_notion(),
            "calendar": self._validate_calendar(),
        }
        return self.results

    def _validate_github(self) -> ValidationResult:
        """
        Validate GitHub service configuration.

        Required: GITHUB_TOKEN (a local install's deployment token)
        """
        from services.infrastructure.deployment import is_hosted_deployment
        from services.integrations.github.config_service import GitHubConfigService

        if is_hosted_deployment():
            # ADR-081 D2: GitHub connects per account on a hosted deploy; nothing to report
            # missing here.
            return ValidationResult(
                service="github",
                status=ServiceStatus.OPTIONAL,
                message="GitHub connects per account on this deployment",
                config_checked=[],
            )
        token = GitHubConfigService().get_authentication_token("system")

        if not token:
            return ValidationResult(
                service="github",
                status=ServiceStatus.MISSING,
                message="GitHub token not configured",
                recovery_suggestion=(
                    "Set GITHUB_TOKEN environment variable with a valid GitHub personal access token. "
                    "Create token at: https://github.com/settings/tokens"
                ),
                config_checked=["GITHUB_TOKEN"],
            )

        # Basic validation - token should start with expected prefix
        if not (token.startswith("ghp_") or token.startswith("github_pat_")):
            return ValidationResult(
                service="github",
                status=ServiceStatus.INVALID,
                message="GitHub token appears invalid (wrong format)",
                recovery_suggestion=(
                    "GitHub personal access tokens should start with 'ghp_' or 'github_pat_'. "
                    "Verify token at: https://github.com/settings/tokens"
                ),
                config_checked=["GITHUB_TOKEN"],
            )

        return ValidationResult(
            service="github",
            status=ServiceStatus.VALID,
            message="GitHub configuration valid",
            config_checked=["GITHUB_TOKEN"],
        )

    def _validate_slack(self) -> ValidationResult:
        """
        Validate Slack service configuration.

        Required: SLACK_BOT_TOKEN, SLACK_APP_TOKEN, SLACK_SIGNING_SECRET
        """
        bot_token = os.getenv("SLACK_BOT_TOKEN")
        app_token = os.getenv("SLACK_APP_TOKEN")
        signing_secret = os.getenv("SLACK_SIGNING_SECRET")

        config_checked = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_SIGNING_SECRET"]

        # Check all required tokens
        missing = []
        if not bot_token:
            missing.append("SLACK_BOT_TOKEN")
        if not app_token:
            missing.append("SLACK_APP_TOKEN")
        if not signing_secret:
            missing.append("SLACK_SIGNING_SECRET")

        if missing:
            return ValidationResult(
                service="slack",
                status=ServiceStatus.MISSING,
                message=f"Slack configuration incomplete: {', '.join(missing)} not set",
                recovery_suggestion=(
                    f"Set missing environment variables: {', '.join(missing)}. "
                    "Get credentials from: https://api.slack.com/apps → Your App → OAuth & Permissions / Basic Information"
                ),
                config_checked=config_checked,
            )

        # Validate token formats
        if not bot_token.startswith("xoxb-"):
            return ValidationResult(
                service="slack",
                status=ServiceStatus.INVALID,
                message="SLACK_BOT_TOKEN appears invalid (should start with 'xoxb-')",
                recovery_suggestion="Verify bot token from https://api.slack.com/apps → Your App → OAuth & Permissions",
                config_checked=config_checked,
            )

        if not app_token.startswith("xapp-"):
            return ValidationResult(
                service="slack",
                status=ServiceStatus.INVALID,
                message="SLACK_APP_TOKEN appears invalid (should start with 'xapp-')",
                recovery_suggestion="Verify app token from https://api.slack.com/apps → Your App → Basic Information",
                config_checked=config_checked,
            )

        return ValidationResult(
            service="slack",
            status=ServiceStatus.VALID,
            message="Slack configuration valid",
            config_checked=config_checked,
        )

    def _validate_notion(self) -> ValidationResult:
        """
        Validate Notion service configuration.

        Required: NOTION_API_KEY
        """
        api_key = os.getenv("NOTION_API_KEY")

        if not api_key:
            return ValidationResult(
                service="notion",
                status=ServiceStatus.MISSING,
                message="Notion API key not configured",
                recovery_suggestion=(
                    "Set NOTION_API_KEY environment variable. "
                    "Create integration at: https://www.notion.so/my-integrations"
                ),
                config_checked=["NOTION_API_KEY"],
            )

        # Notion API keys start with "secret_"
        if not api_key.startswith("secret_"):
            return ValidationResult(
                service="notion",
                status=ServiceStatus.INVALID,
                message="Notion API key appears invalid (should start with 'secret_')",
                recovery_suggestion="Verify API key from https://www.notion.so/my-integrations",
                config_checked=["NOTION_API_KEY"],
            )

        return ValidationResult(
            service="notion",
            status=ServiceStatus.VALID,
            message="Notion configuration valid",
            config_checked=["NOTION_API_KEY"],
        )

    def _validate_calendar(self) -> ValidationResult:
        """
        Validate Google Calendar service configuration.

        Required: GOOGLE_CLIENT_SECRETS_FILE (credentials.json)
        Optional: GOOGLE_TOKEN_FILE (token.json) - created after first OAuth
        """
        client_secrets = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
        token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")

        config_checked = ["GOOGLE_CLIENT_SECRETS_FILE", "GOOGLE_TOKEN_FILE"]

        # Check if client secrets file exists
        if not Path(client_secrets).exists():
            return ValidationResult(
                service="calendar",
                status=ServiceStatus.MISSING,
                message=f"Google Calendar credentials file not found: {client_secrets}",
                recovery_suggestion=(
                    f"1. Create Google Cloud project at: https://console.cloud.google.com\n"
                    f"2. Enable Google Calendar API\n"
                    f"3. Create OAuth 2.0 credentials (Desktop app)\n"
                    f"4. Download credentials and save as: {client_secrets}\n"
                    f"5. Set GOOGLE_CLIENT_SECRETS_FILE={client_secrets} if not using default"
                ),
                config_checked=config_checked,
            )

        # Token file is optional (created on first OAuth)
        # Just note if it doesn't exist yet
        if not Path(token_file).exists():
            return ValidationResult(
                service="calendar",
                status=ServiceStatus.OPTIONAL,
                message=f"Google Calendar authenticated (credentials found, token will be created on first OAuth)",
                recovery_suggestion=(
                    f"Token file {token_file} will be created automatically on first authentication. "
                    "No action needed unless OAuth flow fails."
                ),
                config_checked=config_checked,
            )

        return ValidationResult(
            service="calendar",
            status=ServiceStatus.VALID,
            message="Google Calendar configuration valid",
            config_checked=config_checked,
        )

    def is_all_valid(self) -> bool:
        """
        Check if all required configurations are valid.

        Returns:
            bool: True if all services are valid or optional, False if any missing/invalid
        """
        if not self.results:
            self.validate_all()

        for result in self.results.values():
            if result.status in (ServiceStatus.MISSING, ServiceStatus.INVALID):
                return False

        return True

    def get_invalid_services(self) -> List[ValidationResult]:
        """
        Get list of services with invalid or missing configuration.

        Returns:
            List[ValidationResult]: Services that need attention
        """
        if not self.results:
            self.validate_all()

        return [
            result
            for result in self.results.values()
            if result.status in (ServiceStatus.MISSING, ServiceStatus.INVALID)
        ]

    def get_summary(self) -> Dict[str, any]:
        """
        Get validation summary for all services.

        Returns:
            Dict: Summary of validation results
        """
        if not self.results:
            self.validate_all()

        return {
            "all_valid": self.is_all_valid(),
            "services": {
                service: {
                    "status": result.status.value,
                    "message": result.message,
                    "recovery_suggestion": result.recovery_suggestion,
                    "config_checked": result.config_checked,
                }
                for service, result in self.results.items()
            },
            "valid_count": sum(1 for r in self.results.values() if r.status == ServiceStatus.VALID),
            "optional_count": sum(
                1 for r in self.results.values() if r.status == ServiceStatus.OPTIONAL
            ),
            "invalid_count": sum(
                1
                for r in self.results.values()
                if r.status in (ServiceStatus.MISSING, ServiceStatus.INVALID)
            ),
        }

    def print_summary(self):
        """Print validation summary to console"""
        if not self.results:
            self.validate_all()

        print("\n" + "=" * 60)
        print("CONFIGURATION VALIDATION SUMMARY")
        print("=" * 60)

        for service, result in self.results.items():
            status_icon = {
                ServiceStatus.VALID: "✅",
                ServiceStatus.OPTIONAL: "⚠️",
                ServiceStatus.MISSING: "❌",
                ServiceStatus.INVALID: "❌",
            }[result.status]

            print(f"\n{status_icon} {service.upper()}: {result.status.value}")
            print(f"   {result.message}")

            if result.recovery_suggestion:
                print(f"\n   Recovery:")
                for line in result.recovery_suggestion.split("\n"):
                    print(f"   {line}")

        print("\n" + "=" * 60)
        print(
            f"Valid: {sum(1 for r in self.results.values() if r.status == ServiceStatus.VALID)} | "
            f"Optional: {sum(1 for r in self.results.values() if r.status == ServiceStatus.OPTIONAL)} | "
            f"Invalid: {sum(1 for r in self.results.values() if r.status in (ServiceStatus.MISSING, ServiceStatus.INVALID))}"
        )
        print("=" * 60 + "\n")


# Convenience function for quick validation
def validate_configuration(print_results: bool = True) -> bool:
    """
    Validate all service configurations.

    Args:
        print_results: Whether to print validation summary

    Returns:
        bool: True if all configurations valid, False otherwise
    """
    validator = ConfigValidator()
    validator.validate_all()

    if print_results:
        validator.print_summary()

    return validator.is_all_valid()
