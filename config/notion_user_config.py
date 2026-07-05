"""
Notion User Configuration Loader
Extends existing PIPER.user.md structure with Notion-specific settings.
Implements fail-fast validation with actionable error messages.
"""

import os
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class ValidationLevel(Enum):
    """Configuration validation levels"""

    BASIC = "basic"  # Format validation + environment check
    ENHANCED = "enhanced"  # Basic + API connectivity test
    FULL = "full"  # Enhanced + permission verification


@dataclass
class ValidationResult:
    """Result of configuration validation"""

    level: ValidationLevel
    format_valid: bool
    environment_valid: bool
    connectivity_tested: bool = False
    connectivity_result: Optional[bool] = None
    permission_checked: bool = False
    permission_result: Optional[Dict[str, bool]] = None
    errors: List[str] = None
    warnings: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

    def is_valid(self) -> bool:
        """Check if configuration is valid for its validation level"""
        if not self.format_valid or not self.environment_valid:
            return False

        if self.level in [ValidationLevel.ENHANCED, ValidationLevel.FULL]:
            if self.connectivity_tested and self.connectivity_result is False:
                return False

        if self.level == ValidationLevel.FULL:
            if (
                self.permission_checked
                and self.permission_result
                and not all(self.permission_result.values())
            ):
                return False

        return True


class ConfigurationError(Exception):
    """Clear, actionable configuration errors with resolution steps"""

    def __init__(self, message: str, resolution_steps: List[str], field_path: str = None):
        self.field_path = field_path
        self.resolution_steps = resolution_steps

        formatted_message = f"{message}"
        if field_path:
            formatted_message = f"Configuration error in '{field_path}': {message}"

        formatted_message += f"\n\nResolution steps:\n"
        for i, step in enumerate(resolution_steps, 1):
            formatted_message += f"{i}. {step}\n"

        super().__init__(formatted_message)


class NotionUserConfig:
    """User-specific Notion configuration with fail-fast validation"""

    # Notion ID format validation pattern
    NOTION_ID_PATTERN = re.compile(r"^25[a-f0-9]{30}$")

    def __init__(self, config_dict: Dict[str, Any]):
        self.raw_config = config_dict
        self.notion_config = config_dict.get("notion", {})
        self.validation_results = {}

        # Parse configuration sections (format-first validation)
        self._parse_all_fields()
        self._validate_required_fields_present()

    def _parse_all_fields(self):
        """Parse all configuration fields and validate formats (format-first approach)"""
        # Parse all fields first
        self.adrs_database_id = self.notion_config.get("adrs", {}).get("database_id")
        self.publishing_default_parent = self.notion_config.get("publishing", {}).get(
            "default_parent"
        )

        # Development settings
        dev_config = self.notion_config.get("development", {})
        self.development_test_parent = dev_config.get("test_parent", "")
        self.development_debug_parent = dev_config.get("debug_parent", "")
        self.development_mock_mode = dev_config.get("mock_mode", False)

        # Validation settings
        validation_config = self.notion_config.get("validation", {})
        level_str = validation_config.get("level", "basic")
        self.validation_level = ValidationLevel(level_str)
        self.validation_connectivity_check = validation_config.get("connectivity_check", True)
        self.validation_permission_check = validation_config.get("permission_check", False)

        # Publishing settings
        publishing_config = self.notion_config.get("publishing", {})
        self.publishing_enabled = publishing_config.get("enabled", True)
        self.publishing_format = publishing_config.get("format", "markdown")

        # ADR settings
        adrs_config = self.notion_config.get("adrs", {})
        self.adrs_enabled = adrs_config.get("enabled", True)
        self.adrs_auto_publish = adrs_config.get("auto_publish", True)

        # VALIDATE FORMATS FIRST (better user experience)
        self._validate_all_formats()

    def _validate_all_formats(self):
        """Validate format of all fields with Notion IDs (format-first approach)"""
        format_errors = []

        # Validate ADR database ID format if present and not empty
        if (
            self.adrs_database_id
            and self.adrs_database_id.strip()
            and not self.NOTION_ID_PATTERN.match(self.adrs_database_id)
        ):
            format_errors.append(("adrs.database_id", self.adrs_database_id))

        # Validate publishing default parent format if present and not empty
        if (
            self.publishing_default_parent
            and self.publishing_default_parent.strip()
            and not self.NOTION_ID_PATTERN.match(self.publishing_default_parent)
        ):
            format_errors.append(("publishing.default_parent", self.publishing_default_parent))

        # Validate development test parent format if present and not empty
        if (
            self.development_test_parent
            and self.development_test_parent.strip()
            and not self.NOTION_ID_PATTERN.match(self.development_test_parent)
        ):
            format_errors.append(("development.test_parent", self.development_test_parent))

        # Validate development debug parent format if present and not empty
        if (
            self.development_debug_parent
            and self.development_debug_parent.strip()
            and not self.NOTION_ID_PATTERN.match(self.development_debug_parent)
        ):
            format_errors.append(("development.debug_parent", self.development_debug_parent))

        if format_errors:
            field_info = ", ".join([f"{field}='{value}'" for field, value in format_errors])
            raise ConfigurationError(
                f"Invalid Notion ID format: {field_info}",
                [
                    "Notion IDs must be 32-character hexadecimal strings starting with '25'",
                    "Pattern: 25[a-f0-9]{30}",
                    "Example: 25e11704d8bf80deaac2f806390fe7da",
                    "Run 'piper notion list-pages' or 'piper notion list-databases' to get valid IDs",
                ],
            )

    def _validate_required_fields_present(self):
        """Check that required fields are present (after format validation)"""
        missing_fields = []

        # Only check for missing if field is None or empty string
        if not self.adrs_database_id or self.adrs_database_id == "":
            missing_fields.append(
                (
                    "adrs.database_id",
                    [
                        "Add 'notion.adrs.database_id' to config/PIPER.user.md",
                        "Run 'piper notion list-databases' to find your database ID",
                        "Run 'piper notion setup' for guided configuration",
                    ],
                )
            )

        if not self.publishing_default_parent or self.publishing_default_parent == "":
            missing_fields.append(
                (
                    "publishing.default_parent",
                    [
                        "Add 'notion.publishing.default_parent' to config/PIPER.user.md",
                        "Run 'piper notion list-pages' to find your parent page ID",
                        "Use 'piper notion create-parent' to create a new parent page",
                    ],
                )
            )

        if missing_fields:
            all_resolution_steps = []
            field_names = []

            for field_name, resolution_steps in missing_fields:
                field_names.append(field_name)
                all_resolution_steps.extend(resolution_steps)

            raise ConfigurationError(
                f"Missing required Notion configuration field(s): {', '.join(field_names)}",
                all_resolution_steps,
            )

    @classmethod
    def load(cls, config_dict: Dict[str, Any]) -> "NotionUserConfig":
        """Load configuration from dictionary with validation"""
        instance = cls(config_dict)

        return instance

    @classmethod
    def load_from_user_config(cls, config_path: Optional[Path] = None) -> "NotionUserConfig":
        """Load from PIPER.user.md file with structured error handling"""
        if config_path is None:
            config_path = Path("config/PIPER.user.md")

        if not config_path.exists():
            raise ConfigurationError(
                f"User configuration file not found: {config_path}",
                [
                    f"Copy the template: cp config/PIPER.user.md.example {config_path}",
                    f"Edit {config_path} and add your Notion configuration",
                    "Run 'piper notion setup' for guided configuration",
                ],
            )

        try:
            content = config_path.read_text()

            # Extract YAML section from markdown
            yaml_match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
            if not yaml_match:
                raise ConfigurationError(
                    "No YAML configuration section found in user config",
                    [
                        f"Add a YAML section to {config_path}",
                        'Use the format: ```yaml\\nnotion:\\n  adrs:\\n    database_id: "your_id"\\n```',
                        "Run 'piper notion setup' for guided configuration",
                    ],
                )

            yaml_content = yaml_match.group(1)
            config_dict = yaml.safe_load(yaml_content)

            return cls.load(config_dict)

        except yaml.YAMLError as e:
            raise ConfigurationError(
                f"Invalid YAML syntax in configuration: {e}",
                [
                    "Check YAML syntax in your configuration section",
                    "Ensure proper indentation (spaces, not tabs)",
                    "Use an online YAML validator to check syntax",
                ],
            )

    def get_database_id(self, database_type: str) -> str:
        """Get database ID with fail-fast error handling"""
        if database_type == "adrs":
            if not self.adrs_database_id:
                raise ConfigurationError(
                    "ADR database ID not configured",
                    [
                        "Add 'notion.adrs.database_id' to config/PIPER.user.md",
                        "Run 'piper notion list-databases' to find your database ID",
                        "Run 'piper notion setup' for guided configuration",
                    ],
                )
            return self.adrs_database_id
        else:
            raise ConfigurationError(
                f"Unknown database type: '{database_type}'",
                [
                    "Valid database types: 'adrs'",
                    "Check your configuration usage",
                    "Refer to configuration schema documentation",
                ],
            )

    def get_parent_id(self, context: str = "default") -> str:
        """Get parent ID with context-aware selection"""
        if context == "default":
            if not self.publishing_default_parent:
                raise ConfigurationError(
                    "Default parent page ID not configured",
                    [
                        "Add 'notion.publishing.default_parent' to config/PIPER.user.md",
                        "Run 'piper notion list-pages' to find your parent page ID",
                        "Use 'piper notion create-parent' to create a new parent page",
                    ],
                )
            return self.publishing_default_parent
        elif context == "test":
            if not self.development_test_parent:
                raise ConfigurationError(
                    "Test parent page ID not configured",
                    [
                        "Add 'notion.development.test_parent' to config/PIPER.user.md",
                        "This is optional for development/testing scenarios",
                        "Use default parent if test parent not needed",
                    ],
                )
            return self.development_test_parent
        else:
            raise ConfigurationError(
                f"Unknown parent context: '{context}'",
                [
                    "Valid contexts: 'default', 'test'",
                    "Check your configuration usage",
                    "Refer to configuration schema documentation",
                ],
            )

    def validate(self, level: Optional[ValidationLevel] = None) -> ValidationResult:
        """Synchronous validation (basic level only)"""
        validation_level = level or self.validation_level

        # Basic validation: format + environment
        format_valid = True
        try:
            self._validate_all_formats()
        except ConfigurationError:
            format_valid = False

        environment_valid = bool(os.environ.get("NOTION_API_KEY"))

        return ValidationResult(
            level=validation_level,
            format_valid=format_valid,
            environment_valid=environment_valid,
            connectivity_tested=False,
            errors=[] if format_valid and environment_valid else ["Basic validation failed"],
        )

    async def validate_async(self, level: Optional[ValidationLevel] = None) -> ValidationResult:
        """Asynchronous validation supporting all levels"""
        validation_level = level or self.validation_level

        # Start with basic validation
        result = self.validate(validation_level)

        if not result.format_valid or not result.environment_valid:
            return result

        # Enhanced validation: API connectivity
        if validation_level in [ValidationLevel.ENHANCED, ValidationLevel.FULL]:
            if self.validation_connectivity_check:
                try:
                    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

                    adapter = NotionMCPAdapter()
                    await adapter.connect_with_token()

                    # Test connectivity by getting user info
                    user_info = await adapter.get_current_user()
                    result.connectivity_tested = True
                    result.connectivity_result = bool(user_info)

                except Exception as e:
                    result.connectivity_tested = True
                    result.connectivity_result = False
                    result.errors.append(f"API connectivity failed: {e}")

        # Full validation: Permission checking
        if validation_level == ValidationLevel.FULL and result.connectivity_result:
            if self.validation_permission_check:
                try:
                    # Check database access permissions
                    permission_results = {}

                    if self.adrs_database_id:
                        database = await adapter.notion_client.databases.retrieve(
                            database_id=self.adrs_database_id
                        )
                        permission_results["adrs_database"] = bool(database)

                    if self.publishing_default_parent:
                        page = await adapter.get_page(self.publishing_default_parent)
                        permission_results["default_parent"] = bool(page)

                    result.permission_checked = True
                    result.permission_result = permission_results

                except Exception as e:
                    result.permission_checked = True
                    result.permission_result = {}
                    result.errors.append(f"Permission check failed: {e}")

        return result

    def is_valid_format(self) -> bool:
        """Quick format validation check"""
        try:
            self._validate_all_formats()
            return True
        except ConfigurationError:
            return False

    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary for display"""
        return {
            "adrs_database_id": (
                self.adrs_database_id[:8] + "..." if self.adrs_database_id else None
            ),
            "publishing_default_parent": (
                self.publishing_default_parent[:8] + "..."
                if self.publishing_default_parent
                else None
            ),
            "validation_level": self.validation_level.value,
            "development_mode": self.development_mock_mode,
            "publishing_enabled": self.publishing_enabled,
            "adrs_enabled": self.adrs_enabled,
        }
