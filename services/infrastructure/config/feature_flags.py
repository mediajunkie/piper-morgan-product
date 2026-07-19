"""
Feature Flags Utility for Infrastructure Layer

This utility provides clean access to infrastructure-level feature flags and runtime
detection capabilities while maintaining separation from application configuration.

Use this for:
- Infrastructure toggles (MCP_ENABLED, USE_CONNECTION_POOL)
- Runtime capability detection
- Emergency overrides and circuit breakers
- Development and debugging flags

For application-level configuration, use ConfigService instead.

Architecture Decision: ADR-010 Configuration Access Patterns
"""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


class FeatureFlags:
    """
    Static utility for infrastructure-level feature flag access.

    This class handles environment variable access for infrastructure concerns
    while keeping application logic clean. Use ConfigService for business logic
    configuration.

    Examples:
        # ✅ Infrastructure feature detection
        if FeatureFlags.is_mcp_content_search_enabled():
            return await self._enhanced_mcp_search(query)

        # ✅ Runtime capability check
        pool_size = FeatureFlags.get_max_connection_pool_size()

        # ✅ Debug mode for infrastructure logging
        if FeatureFlags.is_debug_mode_enabled():
            logger.debug("Infrastructure debug info")
    """

    # GitHub integration feature flags (PM-033b-deprecation)
    @staticmethod
    def should_use_spatial_github() -> bool:
        """
        Check if spatial GitHub integration should be used as primary.

        Read by GitHubIntegrationRouter to determine whether to use
        GitHubSpatialIntelligence (8-dimensional spatial analysis) or fall back
        to legacy GitHub integration. (Originally also read by QueryRouter,
        deleted 2026-07-19 — #1436 Family-3.)

        Environment Variable: USE_SPATIAL_GITHUB
        Default: True (spatial is the new default)
        """
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_GITHUB", True)

    @staticmethod
    def is_legacy_github_allowed() -> bool:
        """
        Check if legacy GitHub integration is still allowed as fallback.

        Used during deprecation period to maintain backward compatibility.
        Disabled by default in Week 3 of deprecation timeline.

        Environment Variable: ALLOW_LEGACY_GITHUB
        Default: False (Week 3+: legacy disabled by default)
        """
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_GITHUB", False)

    @staticmethod
    def should_warn_github_deprecation() -> bool:
        """
        Check if deprecation warnings should be shown for legacy GitHub usage.

        Used to alert users when legacy GitHub integration is being used
        during the deprecation period (Week 2+).

        Environment Variable: GITHUB_DEPRECATION_WARNINGS
        Default: True (enabled from Week 2 onward)
        """
        return FeatureFlags._get_boolean_flag("GITHUB_DEPRECATION_WARNINGS", True)

    # Calendar integration feature flags (CORE-QUERY-1)
    @staticmethod
    def should_use_spatial_calendar() -> bool:
        """
        Check if spatial Calendar integration should be used as primary.

        Used by CalendarIntegrationRouter to determine whether to use
        GoogleCalendarMCPAdapter (spatial intelligence) or legacy calendar.

        Environment Variable: USE_SPATIAL_CALENDAR
        Default: True (spatial is the default)
        """
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_CALENDAR", True)

    @staticmethod
    def is_legacy_calendar_allowed() -> bool:
        """
        Check if legacy Calendar integration is allowed as fallback.

        Used during migration period to maintain backward compatibility.

        Environment Variable: ALLOW_LEGACY_CALENDAR
        Default: False (no legacy calendar implementation exists yet)
        """
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_CALENDAR", False)

    # Notion integration feature flags (CORE-QUERY-1)
    @staticmethod
    def should_use_spatial_notion() -> bool:
        """
        Check if spatial Notion integration should be used as primary.

        Used by NotionIntegrationRouter to determine whether to use
        NotionMCPAdapter (spatial intelligence) or legacy notion.

        Environment Variable: USE_SPATIAL_NOTION
        Default: True (spatial is the default)
        """
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_NOTION", True)

    @staticmethod
    def is_legacy_notion_allowed() -> bool:
        """
        Check if legacy Notion integration is allowed as fallback.

        Used during migration period to maintain backward compatibility.

        Environment Variable: ALLOW_LEGACY_NOTION
        Default: False (no legacy notion implementation exists yet)
        """
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_NOTION", False)

    # Slack integration feature flags (CORE-QUERY-1)
    @staticmethod
    def should_use_spatial_slack() -> bool:
        """
        Check if spatial Slack integration should be used as primary.

        Used by SlackIntegrationRouter to determine whether to use
        SlackSpatialAdapter (spatial intelligence) or legacy slack.

        Environment Variable: USE_SPATIAL_SLACK
        Default: True (spatial is the default)
        """
        return FeatureFlags._get_boolean_flag("USE_SPATIAL_SLACK", True)

    @staticmethod
    def is_legacy_slack_allowed() -> bool:
        """
        Check if legacy Slack integration is allowed as fallback.

        Used during migration period to maintain backward compatibility.

        Environment Variable: ALLOW_LEGACY_SLACK
        Default: False (no legacy slack implementation exists yet)
        """
        return FeatureFlags._get_boolean_flag("ALLOW_LEGACY_SLACK", False)

    # MCP-related feature flags
    @staticmethod
    def is_mcp_content_search_enabled() -> bool:
        """
        Check if MCP content search is enabled.

        Used by FileRepository and other components that need to detect
        MCP infrastructure availability for enhanced search capabilities.

        Environment Variable: ENABLE_MCP_FILE_SEARCH
        Default: False
        """
        return FeatureFlags._get_boolean_flag("ENABLE_MCP_FILE_SEARCH", False)

    @staticmethod
    def is_mcp_connection_pooling_enabled() -> bool:
        """
        Check if MCP connection pooling is enabled.

        Used by MCPResourceManager to determine whether to use connection
        pooling infrastructure or direct connections.

        Environment Variable: USE_MCP_POOL
        Default: False
        """
        return FeatureFlags._get_boolean_flag("USE_MCP_POOL", False)

    @staticmethod
    def get_mcp_server_url() -> str:
        """
        Get MCP server URL for infrastructure connections.

        This is infrastructure-level configuration for the MCP server endpoint.
        Application-level MCP configuration should use ConfigService.

        Environment Variable: MCP_SERVER_URL
        Default: stdio://./scripts/mcp_file_server.py
        """
        return os.getenv("MCP_SERVER_URL", "stdio://./scripts/mcp_file_server.py")

    # General infrastructure flags
    @staticmethod
    def is_debug_mode_enabled() -> bool:
        """
        Check if debug mode is enabled for infrastructure components.

        Used for enhanced logging, debug endpoints, and development features
        that should not be enabled in production.

        Environment Variable: DEBUG
        Default: False
        """
        return FeatureFlags._get_boolean_flag("DEBUG", False)

    @staticmethod
    def is_development_mode() -> bool:
        """
        Check if running in development mode.

        Used to enable development-specific features like auto-reload,
        detailed error messages, and development endpoints.

        Environment Variable: DEVELOPMENT_MODE
        Default: False
        """
        return FeatureFlags._get_boolean_flag("DEVELOPMENT_MODE", False)

    # Connection and performance flags
    @staticmethod
    def get_max_connection_pool_size() -> int:
        """
        Get maximum connection pool size for infrastructure connections.

        Used by connection pool implementations to determine maximum
        concurrent connections to external services.

        Environment Variable: MAX_CONNECTION_POOL_SIZE
        Default: 5
        """
        return FeatureFlags._get_int_flag("MAX_CONNECTION_POOL_SIZE", 5)

    @staticmethod
    def get_connection_timeout_seconds() -> float:
        """
        Get connection timeout for infrastructure connections.

        Used by HTTP clients, database connections, and other infrastructure
        components for timeout configuration.

        Environment Variable: CONNECTION_TIMEOUT_SECONDS
        Default: 5.0
        """
        return FeatureFlags._get_float_flag("CONNECTION_TIMEOUT_SECONDS", 5.0)

    # Testing and quality assurance flags
    @staticmethod
    def is_test_mode() -> bool:
        """
        Check if running in test mode.

        Used to enable test-specific behavior, mock services, and
        testing utilities that should not run in production.

        Environment Variable: TEST_MODE
        Default: False
        """
        return FeatureFlags._get_boolean_flag("TEST_MODE", False)

    # Emergency and operational flags
    @staticmethod
    def is_circuit_breaker_enabled() -> bool:
        """
        Check if circuit breakers are enabled for external service calls.

        Used to enable/disable circuit breaker protection for resilience
        against external service failures.

        Environment Variable: ENABLE_CIRCUIT_BREAKERS
        Default: True (safety-first default)
        """
        return FeatureFlags._get_boolean_flag("ENABLE_CIRCUIT_BREAKERS", True)

    @staticmethod
    def is_emergency_mode() -> bool:
        """
        Check if system is in emergency mode.

        Used to disable non-essential features and reduce system load
        during incidents or maintenance windows.

        Environment Variable: EMERGENCY_MODE
        Default: False
        """
        return FeatureFlags._get_boolean_flag("EMERGENCY_MODE", False)

    @staticmethod
    def is_enabled(flag_name: str, default: bool = False) -> bool:
        """
        Generic method to check if any feature flag is enabled.

        Used by integrations that need dynamic feature flag checking.
        For known flags, prefer the specific methods above.

        Args:
            flag_name: Environment variable name or feature name
            default: Default value if flag not found

        Returns:
            Boolean value of the feature flag
        """
        # Map common feature names to environment variables
        feature_env_map = {
            "slack_webhooks": "ENABLE_SLACK_WEBHOOKS",
            "slack_socket_mode": "ENABLE_SLACK_SOCKET_MODE",
            "slack_spatial_mapping": "ENABLE_SLACK_SPATIAL_MAPPING",
        }

        # Use mapped environment variable if available, otherwise use flag_name directly
        env_var = feature_env_map.get(flag_name, flag_name)
        return FeatureFlags._get_boolean_flag(env_var, default)

    # Internal utility methods
    @staticmethod
    def _get_boolean_flag(flag_name: str, default: bool = False) -> bool:
        """
        Internal: Get boolean environment variable with safe parsing.

        Supports multiple boolean representations: true/false, 1/0, yes/no, on/off

        Args:
            flag_name: Environment variable name
            default: Default value if variable not set or invalid

        Returns:
            Boolean value of environment variable
        """
        try:
            value = os.getenv(flag_name, str(default)).lower().strip()
            return value in ("true", "1", "yes", "on", "enabled")
        except Exception as e:
            logger.warning(f"Error parsing boolean flag {flag_name}: {e}, using default {default}")
            return default

    @staticmethod
    def _get_int_flag(flag_name: str, default: int) -> int:
        """
        Internal: Get integer environment variable with safe parsing.

        Args:
            flag_name: Environment variable name
            default: Default value if variable not set or invalid

        Returns:
            Integer value of environment variable
        """
        try:
            value = os.getenv(flag_name, str(default))
            return int(value)
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid integer value for {flag_name}: {e}, using default {default}")
            return default

    @staticmethod
    def _get_float_flag(flag_name: str, default: float) -> float:
        """
        Internal: Get float environment variable with safe parsing.

        Args:
            flag_name: Environment variable name
            default: Default value if variable not set or invalid

        Returns:
            Float value of environment variable
        """
        try:
            value = os.getenv(flag_name, str(default))
            return float(value)
        except (ValueError, TypeError) as e:
            logger.warning(f"Invalid float value for {flag_name}: {e}, using default {default}")
            return default

    # Utility methods for common patterns
    @classmethod
    def get_all_enabled_features(cls) -> dict:
        """
        Get dictionary of all currently enabled feature flags.

        Useful for debugging, monitoring, and configuration validation.

        Returns:
            Dictionary mapping feature names to their current values
        """
        features = {}

        # GitHub integration features
        features["spatial_github"] = cls.should_use_spatial_github()
        features["legacy_github_allowed"] = cls.is_legacy_github_allowed()
        features["github_deprecation_warnings"] = cls.should_warn_github_deprecation()

        # MCP features
        features["mcp_content_search"] = cls.is_mcp_content_search_enabled()
        features["mcp_connection_pooling"] = cls.is_mcp_connection_pooling_enabled()

        # General infrastructure
        features["debug_mode"] = cls.is_debug_mode_enabled()
        features["development_mode"] = cls.is_development_mode()
        features["test_mode"] = cls.is_test_mode()

        # Operational
        features["circuit_breakers"] = cls.is_circuit_breaker_enabled()
        features["emergency_mode"] = cls.is_emergency_mode()

        return {k: v for k, v in features.items() if v}

    @classmethod
    def validate_configuration(cls) -> list[str]:
        """
        Validate current feature flag configuration for common issues.

        Returns:
            List of configuration warnings or issues found
        """
        warnings = []

        # Check for conflicting configurations
        if cls.is_emergency_mode() and cls.is_debug_mode_enabled():
            warnings.append("DEBUG mode enabled during EMERGENCY_MODE - may impact performance")

        if cls.is_mcp_content_search_enabled() and not cls.is_mcp_connection_pooling_enabled():
            warnings.append(
                "MCP content search enabled without connection pooling - may impact performance"
            )

        if cls.is_development_mode() and cls.is_circuit_breaker_enabled():
            warnings.append(
                "Circuit breakers enabled in development mode - may hide integration issues"
            )

        # Check for production safety
        if not cls.is_circuit_breaker_enabled() and not cls.is_test_mode():
            warnings.append(
                "Circuit breakers disabled in non-test environment - may impact resilience"
            )

        return warnings


# Convenience functions for common patterns
def is_feature_enabled(feature_name: str) -> bool:
    """
    Convenience function to check if a feature is enabled.

    Maps common feature names to their specific flag methods for easier usage.

    Args:
        feature_name: Human-readable feature name

    Returns:
        Whether the feature is enabled

    Example:
        if is_feature_enabled("mcp_search"):
            # Enhanced search logic
            pass
    """
    feature_map = {
        "mcp_search": FeatureFlags.is_mcp_content_search_enabled,
        "mcp_pool": FeatureFlags.is_mcp_connection_pooling_enabled,
        "debug": FeatureFlags.is_debug_mode_enabled,
        "development": FeatureFlags.is_development_mode,
        "test": FeatureFlags.is_test_mode,
        "circuit_breakers": FeatureFlags.is_circuit_breaker_enabled,
        "emergency": FeatureFlags.is_emergency_mode,
    }

    if feature_name in feature_map:
        return feature_map[feature_name]()
    else:
        logger.warning(f"Unknown feature name: {feature_name}")
        return False


def get_infrastructure_config() -> dict:
    """
    Get complete infrastructure configuration for monitoring and debugging.

    Returns:
        Dictionary containing all infrastructure configuration values
    """
    return {
        "features": FeatureFlags.get_all_enabled_features(),
        "connection_pool_size": FeatureFlags.get_max_connection_pool_size(),
        "connection_timeout": FeatureFlags.get_connection_timeout_seconds(),
        "mcp_server_url": FeatureFlags.get_mcp_server_url(),
        "configuration_warnings": FeatureFlags.validate_configuration(),
    }
