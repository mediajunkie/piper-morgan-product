"""
Slack Configuration Service
Implements ADR-010 Configuration Access Patterns for Slack integration components.

Provides centralized configuration management for Slack operations including:
- Authentication and token management
- API rate limiting and retry configuration
- Feature flags for Slack integrations
- Environment-specific settings
"""

import logging
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from services.infrastructure.config.feature_flags import FeatureFlags

logger = logging.getLogger(__name__)


class SlackEnvironment(Enum):
    """Slack environment types"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class SlackConfig:
    """Slack configuration settings"""

    # Authentication
    bot_token: str = ""
    # #1338: user token (xoxp-) for USER-only Web API methods (e.g. search.messages,
    # which a bot token cannot call). User-scoped, persisted as the `slack_user`
    # keychain key after OAuth. Empty when the user hasn't granted user scopes.
    user_token: str = ""
    app_token: str = ""
    signing_secret: str = ""

    # API Configuration
    api_base_url: str = "https://slack.com/api"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Rate Limiting
    requests_per_minute: int = 50
    burst_limit: int = 10

    # Feature Flags
    enable_webhooks: bool = True
    enable_socket_mode: bool = False
    enable_spatial_mapping: bool = True

    # Environment
    environment: SlackEnvironment = SlackEnvironment.DEVELOPMENT

    # OAuth Settings
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""

    # Webhook Configuration
    webhook_url: str = ""
    default_channel: str = ""

    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.bot_token:
            return False
        if self.enable_webhooks and not self.webhook_url:
            return False
        return True


class SlackConfigService:
    """
    Slack configuration service following ADR-010 patterns.

    Issue #734: Updated for multi-tenancy isolation.
    All user-scoped methods now require user_id parameter.
    """

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        # Per-user config cache (keyed by user_id)
        self._config_cache: Dict[str, SlackConfig] = {}

    def get_config(self, user_id: str) -> SlackConfig:
        """
        Get Slack configuration with environment variable loading.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            SlackConfig object with user-scoped credentials

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")

        if user_id not in self._config_cache:
            self._config_cache[user_id] = self._load_config(user_id)
        return self._config_cache[user_id]

    def _load_from_user_config(self) -> Dict[str, Any]:
        """
        Load Slack configuration from PIPER.user.md.

        Parses YAML blocks from the markdown file and extracts the slack section.
        Follows the same pattern as Calendar and Notion config loading.

        Returns:
            Dict with Slack configuration, or empty dict if not found/invalid
        """
        try:
            user_config_path = Path("config/PIPER.user.md")
            if not user_config_path.exists():
                logger.debug("PIPER.user.md not found")
                return {}

            # Read the markdown file
            content = user_config_path.read_text()

            # Find the Slack Integration section
            # Look for heading pattern: ## Slack Integration or ## slack:
            slack_section_match = re.search(
                r"##\s+\U0001F4AC\s+Slack Integration(.*?)(?=##\s+|$)", content, re.DOTALL
            )

            if not slack_section_match:
                # Try alternate pattern: slack: followed by YAML block
                slack_section_match = re.search(
                    r"slack:\s*```yaml(.*?)```", content, re.DOTALL | re.IGNORECASE
                )
                if not slack_section_match:
                    logger.debug("No slack: section found in PIPER.user.md")
                    return {}

                # Extract YAML content directly
                yaml_content = slack_section_match.group(1).strip()
                config_data = yaml.safe_load(yaml_content)
                logger.info(
                    f"Loaded Slack config from PIPER.user.md: {list(config_data.keys()) if config_data else []}"
                )
                return config_data or {}

            section_content = slack_section_match.group(1)

            # Extract YAML from markdown code blocks
            yaml_match = re.search(r"```yaml.*?```", section_content, re.DOTALL)
            if not yaml_match:
                logger.debug("No YAML block found in slack section")
                return {}

            # Extract YAML content by removing markdown markers
            full_yaml_block = yaml_match.group(0)
            yaml_content = full_yaml_block.replace("```yaml", "").replace("```", "").strip()
            config_data = yaml.safe_load(yaml_content)

            if config_data and "slack" in config_data:
                logger.info(
                    f"Loaded Slack config from PIPER.user.md: {list(config_data['slack'].keys())}"
                )
                return config_data["slack"]

            logger.info(
                f"Loaded Slack config from PIPER.user.md: {list(config_data.keys()) if config_data else []}"
            )
            return config_data or {}

        except Exception as e:
            # Log error but don't crash - graceful fallback
            logger.error(f"Error loading Slack config from PIPER.user.md: {e}")
            return {}

    def _load_config(self, user_id: str) -> SlackConfig:
        """
        Load configuration with 4-layer priority: env vars > user config > keychain > defaults.

        Priority order:
        1. Environment variables (highest)
        2. PIPER.user.md configuration (middle)
        3. OS Keychain with user-scoping (secure storage, Issue #575/#734)
        4. Hardcoded defaults (lowest)

        Args:
            user_id: User identifier for scoping credentials

        Issue #734: Keychain lookups now scoped by user_id.
        """
        from services.infrastructure.keychain_service import KeychainService

        # Load user configuration from PIPER.user.md
        user_config = self._load_from_user_config()

        # Extract subsections (with empty dict fallback)
        auth_config = user_config.get("authentication", {})
        api_config = user_config.get("api", {})
        behavior_config = user_config.get("behavior", {})
        features_config = user_config.get("features", {})
        oauth_config = user_config.get("oauth", {})

        # Issue #575/#576/#734: Check keychain for credentials with user-scoping
        keychain = KeychainService()
        # User-scoped token (per ADR-058)
        keychain_bot_token = keychain.get_api_key("slack_bot", username=user_id) or ""
        # #1338: user token (xoxp-) for USER-only methods (search.messages), user-scoped
        keychain_user_token = keychain.get_api_key("slack_user", username=user_id) or ""
        # App credentials (shared, no user scoping)
        keychain_client_id = keychain.get_api_key("slack_client_id") or ""
        keychain_client_secret = keychain.get_api_key("slack_client_secret") or ""

        # 4-layer priority: env > user config > keychain > default
        # bot_token is user-scoped
        bot_token = (
            os.getenv("SLACK_BOT_TOKEN") or auth_config.get("bot_token") or keychain_bot_token or ""
        )
        # user_token is user-scoped (same 4-layer priority as bot_token) — #1338
        user_token = (
            os.getenv("SLACK_USER_TOKEN")
            or auth_config.get("user_token")
            or keychain_user_token
            or ""
        )
        # client_id/secret are app credentials (shared)
        client_id = (
            os.getenv("SLACK_CLIENT_ID")
            or oauth_config.get("client_id")
            or keychain_client_id
            or ""
        )
        client_secret = (
            os.getenv("SLACK_CLIENT_SECRET")
            or oauth_config.get("client_secret")
            or keychain_client_secret
            or ""
        )

        return SlackConfig(
            # Authentication (4-layer priority for bot_token, user-scoped)
            bot_token=bot_token,
            user_token=user_token,  # #1338: USER-only methods (search.messages)
            app_token=os.getenv("SLACK_APP_TOKEN", auth_config.get("app_token", "")),
            signing_secret=os.getenv("SLACK_SIGNING_SECRET", auth_config.get("signing_secret", "")),
            # API Configuration
            api_base_url=os.getenv(
                "SLACK_API_BASE_URL", api_config.get("base_url", "https://slack.com/api")
            ),
            timeout_seconds=int(
                os.getenv("SLACK_TIMEOUT_SECONDS", str(api_config.get("timeout_seconds", 30)))
            ),
            max_retries=int(os.getenv("SLACK_MAX_RETRIES", str(api_config.get("max_retries", 3)))),
            # Rate Limiting
            requests_per_minute=int(
                os.getenv(
                    "SLACK_RATE_LIMIT_RPM", str(behavior_config.get("rate_limit_per_minute", 50))
                )
            ),
            burst_limit=int(
                os.getenv("SLACK_BURST_LIMIT", str(behavior_config.get("burst_limit", 10)))
            ),
            # Feature Flags (prefer user config over feature flags service)
            enable_webhooks=features_config.get(
                "enable_webhooks", self.feature_flags.is_enabled("slack_webhooks")
            ),
            enable_socket_mode=features_config.get(
                "enable_socket_mode", self.feature_flags.is_enabled("slack_socket_mode")
            ),
            enable_spatial_mapping=features_config.get(
                "enable_spatial_mapping", self.feature_flags.is_enabled("slack_spatial_mapping")
            ),
            # Environment
            environment=SlackEnvironment(
                os.getenv("SLACK_ENVIRONMENT", api_config.get("environment", "development"))
            ),
            # OAuth Settings (4-layer priority, app credentials)
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.getenv("SLACK_REDIRECT_URI", oauth_config.get("redirect_uri", "")),
            # Webhook Configuration
            webhook_url=os.getenv("SLACK_WEBHOOK_URL", behavior_config.get("webhook_url", "")),
            default_channel=os.getenv(
                "SLACK_DEFAULT_CHANNEL", behavior_config.get("default_channel", "")
            ),
        )

    def is_configured(self, user_id: str) -> bool:
        """
        Check if Slack is properly configured for the given user.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            True if Slack is properly configured

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        config = self.get_config(user_id)
        return config.validate()

    def get_environment(self, user_id: str) -> SlackEnvironment:
        """
        Get current Slack environment.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            SlackEnvironment enum value

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        return self.get_config(user_id).environment

    def is_production(self, user_id: str) -> bool:
        """
        Check if running in production environment.

        Args:
            user_id: User identifier for scoping credentials (required)

        Returns:
            True if in production environment

        Raises:
            ValueError: If user_id is None or empty

        Issue #734: Added user_id parameter for multi-tenancy isolation.
        """
        if not user_id:
            raise ValueError("user_id is required")
        return self.get_environment(user_id) == SlackEnvironment.PRODUCTION

    def clear_cache(self, user_id: Optional[str] = None) -> None:
        """
        Clear configuration cache.

        Args:
            user_id: If provided, clear only that user's cache.
                     If None, clear entire cache.

        Issue #734: Added for multi-tenancy support.
        """
        if user_id:
            self._config_cache.pop(user_id, None)
        else:
            self._config_cache.clear()
