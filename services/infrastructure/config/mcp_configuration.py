"""
Centralized Configuration Service for MCP Settings
Production-ready configuration management with type safety and hot reload capability.
"""

import json
import logging
import os
import threading
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or cannot be loaded."""

    pass


@dataclass
class ConfigurationChangeEvent:
    """Event triggered when configuration changes."""

    key: str
    old_value: Any
    new_value: Any
    timestamp: float


@dataclass
class MCPConfiguration:
    """Type-safe configuration for all MCP settings."""

    # Feature Flags
    mcp_enabled: bool = False
    pool_enabled: bool = False
    debug_enabled: bool = False

    # Connection Pool Settings
    max_connections: int = 5
    connection_timeout: float = 5.0
    circuit_breaker_threshold: int = 5
    circuit_breaker_timeout: int = 60

    # Content Extraction Settings
    max_content_length: int = 50000
    snippet_length: int = 200
    max_keywords: int = 20

    # API Keys (optional, can be None)

    def __post_init__(self):
        """Validate configuration values."""
        if self.max_connections <= 0:
            raise ValueError("max_connections must be greater than 0")

        if self.connection_timeout <= 0:
            raise ValueError("connection_timeout must be greater than 0")

        if self.circuit_breaker_threshold <= 0:
            raise ValueError("circuit_breaker_threshold must be greater than 0")

        if self.circuit_breaker_timeout <= 0:
            raise ValueError("circuit_breaker_timeout must be greater than 0")

        if self.max_content_length <= 0:
            raise ValueError("max_content_length must be greater than 0")

        if self.snippet_length <= 0:
            raise ValueError("snippet_length must be greater than 0")

        if self.max_keywords <= 0:
            raise ValueError("max_keywords must be greater than 0")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert configuration to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class MCPConfigurationService:
    """
    Centralized configuration service for all MCP settings.

    Features:
    - Type-safe configuration with validation
    - Hot reload from environment variables
    - Configuration change notifications
    - File-based configuration loading
    - Thread-safe access
    """

    def __init__(self):
        """Initialize configuration service with defaults."""
        self._config = MCPConfiguration()
        self._config_lock = threading.RLock()
        self._change_listeners: List[Callable[[ConfigurationChangeEvent], None]] = []

        # Environment variable mappings
        self._env_mappings = {
            "ENABLE_MCP_FILE_SEARCH": ("mcp_enabled", self._parse_bool),
            "USE_MCP_POOL": ("pool_enabled", self._parse_bool),
            "APP_DEBUG": ("debug_enabled", self._parse_bool),
            "MCP_MAX_CONNECTIONS": ("max_connections", self._parse_int),
            "MCP_CONNECTION_TIMEOUT": ("connection_timeout", self._parse_float),
            "MCP_CIRCUIT_BREAKER_THRESHOLD": ("circuit_breaker_threshold", self._parse_int),
            "MCP_CIRCUIT_BREAKER_TIMEOUT": ("circuit_breaker_timeout", self._parse_int),
            "MCP_MAX_CONTENT_LENGTH": ("max_content_length", self._parse_int),
            "MCP_SNIPPET_LENGTH": ("snippet_length", self._parse_int),
            "MCP_MAX_KEYWORDS": ("max_keywords", self._parse_int),
        }

        logger.info("MCPConfigurationService initialized with defaults")

    def get_config(self) -> MCPConfiguration:
        """Get current configuration (thread-safe, cached access)."""
        with self._config_lock:
            return self._config

    def reload_from_environment(self) -> None:
        """Reload configuration from environment variables."""
        errors = []
        changes = []

        with self._config_lock:
            old_config = self._config
            new_values = {}

            # Process each environment variable
            for env_var, (attr_name, parser) in self._env_mappings.items():
                env_value = os.getenv(env_var)
                if env_value is not None:
                    try:
                        parsed_value = parser(env_value)
                        new_values[attr_name] = parsed_value

                        # Track changes
                        old_value = getattr(old_config, attr_name)
                        if old_value != parsed_value:
                            changes.append((attr_name, old_value, parsed_value))

                    except (ValueError, TypeError) as e:
                        errors.append(f"{env_var}: {str(e)}")

            # If there were parsing errors, raise them
            if errors:
                raise ConfigurationError(f"Configuration validation failed: {'; '.join(errors)}")

            # Create new configuration with updated values
            config_dict = self._config.to_dict()
            config_dict.update(new_values)

            try:
                new_config = MCPConfiguration(**config_dict)
                self._config = new_config

                # Notify listeners of changes
                import time

                timestamp = time.time()
                for attr_name, old_value, new_value in changes:
                    event = ConfigurationChangeEvent(
                        key=attr_name, old_value=old_value, new_value=new_value, timestamp=timestamp
                    )
                    self._notify_change_listeners(event)

                if changes:
                    logger.info(f"Configuration reloaded with {len(changes)} changes")

            except (ValueError, TypeError) as e:
                raise ConfigurationError(f"Configuration validation failed: {str(e)}")

    def load_from_file(self, file_path: Union[str, Path]) -> None:
        """Load configuration from JSON file."""
        file_path = Path(file_path)

        if not file_path.exists():
            raise ConfigurationError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            # Flatten nested configuration if needed
            flattened = self._flatten_config_dict(data)

            with self._config_lock:
                old_config = self._config
                config_dict = old_config.to_dict()
                config_dict.update(flattened)

                new_config = MCPConfiguration(**config_dict)

                # Track changes
                changes = []
                import time

                timestamp = time.time()
                for key, new_value in flattened.items():
                    old_value = getattr(old_config, key)
                    if old_value != new_value:
                        changes.append(
                            ConfigurationChangeEvent(
                                key=key,
                                old_value=old_value,
                                new_value=new_value,
                                timestamp=timestamp,
                            )
                        )

                self._config = new_config

                # Notify listeners
                for event in changes:
                    self._notify_change_listeners(event)

                logger.info(f"Configuration loaded from file: {file_path}")

        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise ConfigurationError(f"Failed to load configuration from {file_path}: {str(e)}")

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        with self._config_lock:
            old_config = self._config
            default_config = MCPConfiguration()

            # Track changes
            changes = []
            import time

            timestamp = time.time()

            for key in default_config.to_dict().keys():
                old_value = getattr(old_config, key)
                new_value = getattr(default_config, key)
                if old_value != new_value:
                    changes.append(
                        ConfigurationChangeEvent(
                            key=key, old_value=old_value, new_value=new_value, timestamp=timestamp
                        )
                    )

            self._config = default_config

            # Notify listeners
            for event in changes:
                self._notify_change_listeners(event)

            logger.info("Configuration reset to defaults")

    def subscribe_to_changes(self, listener: Callable[[ConfigurationChangeEvent], None]) -> None:
        """Subscribe to configuration change notifications."""
        with self._config_lock:
            self._change_listeners.append(listener)

    def unsubscribe_from_changes(
        self, listener: Callable[[ConfigurationChangeEvent], None]
    ) -> None:
        """Unsubscribe from configuration change notifications."""
        with self._config_lock:
            if listener in self._change_listeners:
                self._change_listeners.remove(listener)

    def _notify_change_listeners(self, event: ConfigurationChangeEvent) -> None:
        """Notify all change listeners of a configuration change."""
        for listener in self._change_listeners:
            try:
                listener(event)
            except Exception as e:
                logger.warning(f"Configuration change listener failed: {e}")

    def _flatten_config_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Flatten nested configuration dictionary."""
        flattened = {}

        # Handle nested structure like {"mcp": {"enabled": true}}
        if "mcp" in data:
            mcp_config = data["mcp"]
            if "enabled" in mcp_config:
                flattened["mcp_enabled"] = mcp_config["enabled"]
            if "pool_enabled" in mcp_config:
                flattened["pool_enabled"] = mcp_config["pool_enabled"]
            if "max_connections" in mcp_config:
                flattened["max_connections"] = mcp_config["max_connections"]
            if "connection_timeout" in mcp_config:
                flattened["connection_timeout"] = mcp_config["connection_timeout"]

        if "features" in data:
            features_config = data["features"]
            if "file_search_enabled" in features_config:
                flattened["mcp_enabled"] = features_config["file_search_enabled"]
            if "enhanced_ranking" in features_config:
                # Map to some configuration if needed
                pass

        # Also handle flat structure
        for key, value in data.items():
            if key not in ["mcp", "features"] and hasattr(MCPConfiguration, key):
                flattened[key] = value

        return flattened

    @staticmethod
    def _parse_bool(value: str) -> bool:
        """Parse string to boolean with comprehensive true/false recognition."""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value = value.lower().strip()
            if value in ("true", "1", "yes", "on", "enabled"):
                return True
            elif value in ("false", "0", "no", "off", "disabled", ""):
                return False

        raise ValueError(f"Cannot parse '{value}' as boolean")

    @staticmethod
    def _parse_int(value: str) -> int:
        """Parse string to integer with validation."""
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot parse '{value}' as integer: {e}")

    @staticmethod
    def _parse_float(value: str) -> float:
        """Parse string to float with validation."""
        try:
            return float(value)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot parse '{value}' as float: {e}")


# Global singleton instance
_config_service_instance: Optional[MCPConfigurationService] = None
_instance_lock = threading.Lock()


def get_config_service() -> MCPConfigurationService:
    """Get global configuration service instance (singleton)."""
    global _config_service_instance

    if _config_service_instance is None:
        with _instance_lock:
            if _config_service_instance is None:
                _config_service_instance = MCPConfigurationService()
                # Load from environment by default
                try:
                    _config_service_instance.reload_from_environment()
                except ConfigurationError as e:
                    logger.warning(f"Failed to load configuration from environment: {e}")

    return _config_service_instance


def get_config() -> MCPConfiguration:
    """Convenience function to get current configuration."""
    return get_config_service().get_config()
