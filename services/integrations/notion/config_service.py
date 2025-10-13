"""
Notion Configuration Service
Implements ADR-010 Configuration Access Patterns for Notion integration components.

Provides centralized configuration management for Notion operations including:
- Authentication and API key management
- API rate limiting and retry configuration
- Feature flags for Notion integrations
- Environment-specific settings

Note: Replaces static config/notion_config.py with service injection pattern
Legacy file preserved for backward compatibility during migration
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from services.infrastructure.config.feature_flags import FeatureFlags


class NotionEnvironment(Enum):
    """Notion environment types"""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class NotionConfig:
    """Notion configuration settings"""

    # Authentication
    api_key: str = ""
    workspace_id: str = ""

    # API Configuration
    api_base_url: str = "https://api.notion.com/v1"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Rate Limiting
    requests_per_minute: int = 30  # Notion's rate limit

    # Feature Flags
    enable_spatial_mapping: bool = True

    # Environment
    environment: NotionEnvironment = NotionEnvironment.DEVELOPMENT

    def get_api_key(self) -> str:
        """Get API key (interface compatibility with legacy config)"""
        return self.api_key

    def get_workspace_id(self) -> str:
        """Get workspace ID (interface compatibility with legacy config)"""
        return self.workspace_id

    def validate(self) -> bool:
        """Validate configuration settings"""
        return bool(self.api_key)


class NotionConfigService:
    """Notion configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[NotionConfig] = None

    def get_config(self) -> NotionConfig:
        """Get Notion configuration with environment variable loading"""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self) -> NotionConfig:
        """Load configuration from environment variables"""
        return NotionConfig(
            api_key=os.getenv("NOTION_API_KEY", ""),
            workspace_id=os.getenv("NOTION_WORKSPACE_ID", ""),
            api_base_url=os.getenv("NOTION_API_BASE_URL", "https://api.notion.com/v1"),
            timeout_seconds=int(os.getenv("NOTION_TIMEOUT_SECONDS", "30")),
            max_retries=int(os.getenv("NOTION_MAX_RETRIES", "3")),
            requests_per_minute=int(os.getenv("NOTION_RATE_LIMIT_RPM", "30")),
            enable_spatial_mapping=self.feature_flags.is_enabled("notion_spatial_mapping"),
            environment=NotionEnvironment(os.getenv("NOTION_ENVIRONMENT", "development")),
        )

    def is_configured(self) -> bool:
        """Check if Notion is properly configured"""
        config = self.get_config()
        return config.validate()

    def get_environment(self) -> NotionEnvironment:
        """Get current Notion environment"""
        return self.get_config().environment

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get_environment() == NotionEnvironment.PRODUCTION
