"""
TDD Tests for Centralized MCP Configuration Service
RED Phase: Comprehensive test suite for production-ready configuration management
"""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest

# Import will fail initially (RED phase)
try:
    from services.infrastructure.config.mcp_configuration import (
        ConfigurationChangeEvent,
        ConfigurationError,
        MCPConfiguration,
        MCPConfigurationService,
    )

    CONFIG_SERVICE_AVAILABLE = True
except ImportError:
    CONFIG_SERVICE_AVAILABLE = False


@pytest.mark.skipif(
    not CONFIG_SERVICE_AVAILABLE, reason="Configuration service not implemented yet"
)
class TestMCPConfigurationService:
    """Test centralized configuration service."""

    @pytest.fixture
    def config_service(self):
        """Create configuration service with clean state."""
        service = MCPConfigurationService()
        yield service
        # Cleanup any changes
        service.reset_to_defaults()

    @pytest.fixture
    def temp_config_file(self):
        """Create temporary configuration file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            config_data = {
                "mcp": {
                    "enabled": True,
                    "pool_enabled": True,
                    "max_connections": 10,
                    "connection_timeout": 30.0,
                },
                "features": {"file_search_enabled": True, "enhanced_ranking": True},
            }
            import json

            json.dump(config_data, f)
            temp_path = f.name

        yield temp_path

        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    def test_configuration_service_initialization(self, config_service):
        """Test that configuration service initializes with defaults."""
        # Should initialize successfully
        assert config_service is not None

        # Should have default configuration
        config = config_service.get_config()
        assert isinstance(config, MCPConfiguration)

        # Should have sensible defaults
        assert isinstance(config.mcp_enabled, bool)
        assert isinstance(config.pool_enabled, bool)
        assert isinstance(config.max_connections, int)
        assert config.max_connections > 0

    def test_configuration_loading_from_environment(self, config_service):
        """Test loading configuration from environment variables."""
        # RED: This should fail until we implement environment loading
        with patch.dict(
            os.environ,
            {
                "ENABLE_MCP_FILE_SEARCH": "true",
                "USE_MCP_POOL": "true",
                "MCP_MAX_CONNECTIONS": "15",
                "MCP_CONNECTION_TIMEOUT": "45.5",
            },
        ):
            config_service.reload_from_environment()
            config = config_service.get_config()

            assert config.mcp_enabled == True
            assert config.pool_enabled == True
            assert config.max_connections == 15
            assert config.connection_timeout == 45.5

    def test_configuration_default_values_when_not_set(self, config_service):
        """Test that defaults are used when environment variables are not set."""
        with patch.dict(os.environ, {}, clear=True):
            config_service.reload_from_environment()
            config = config_service.get_config()

            # Should use defaults for missing values
            assert isinstance(config.mcp_enabled, bool)
            assert isinstance(config.pool_enabled, bool)
            assert isinstance(config.max_connections, int)
            assert config.max_connections > 0
            assert config.connection_timeout > 0

    def test_boolean_type_validation(self, config_service):
        """Test type validation for boolean configuration values."""
        # Valid boolean values
        valid_boolean_values = ["true", "TRUE", "True", "1", "yes", "on"]
        for value in valid_boolean_values:
            with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": value}):
                config_service.reload_from_environment()
                config = config_service.get_config()
                assert config.mcp_enabled == True, f"Failed for value: {value}"

        # False boolean values
        false_boolean_values = ["false", "FALSE", "False", "0", "no", "off", ""]
        for value in false_boolean_values:
            with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": value}):
                config_service.reload_from_environment()
                config = config_service.get_config()
                assert config.mcp_enabled == False, f"Failed for value: {value}"

    def test_integer_type_validation(self, config_service):
        """Test type validation for integer configuration values."""
        # Valid integer
        with patch.dict(os.environ, {"MCP_MAX_CONNECTIONS": "25"}):
            config_service.reload_from_environment()
            config = config_service.get_config()
            assert config.max_connections == 25

        # Invalid integer should raise error or use default
        with patch.dict(os.environ, {"MCP_MAX_CONNECTIONS": "not_a_number"}):
            with pytest.raises(ConfigurationError):
                config_service.reload_from_environment()

    def test_float_type_validation(self, config_service):
        """Test type validation for float configuration values."""
        # Valid float
        with patch.dict(os.environ, {"MCP_CONNECTION_TIMEOUT": "12.5"}):
            config_service.reload_from_environment()
            config = config_service.get_config()
            assert config.connection_timeout == 12.5

        # Invalid float should raise error
        with patch.dict(os.environ, {"MCP_CONNECTION_TIMEOUT": "invalid_float"}):
            with pytest.raises(ConfigurationError):
                config_service.reload_from_environment()

    def test_configuration_validation_ranges(self, config_service):
        """Test that configuration values are validated within acceptable ranges."""
        # Max connections must be positive
        with patch.dict(os.environ, {"MCP_MAX_CONNECTIONS": "0"}):
            with pytest.raises(ConfigurationError):
                config_service.reload_from_environment()

        with patch.dict(os.environ, {"MCP_MAX_CONNECTIONS": "-5"}):
            with pytest.raises(ConfigurationError):
                config_service.reload_from_environment()

        # Connection timeout must be positive
        with patch.dict(os.environ, {"MCP_CONNECTION_TIMEOUT": "0"}):
            with pytest.raises(ConfigurationError):
                config_service.reload_from_environment()

    def test_hot_reload_capability(self, config_service):
        """Test that configuration can be reloaded without restart."""
        # RED: This should fail until hot reload is implemented

        # Initial state
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false"}):
            config_service.reload_from_environment()
            assert config_service.get_config().mcp_enabled == False

        # Change environment and reload
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
            config_service.reload_from_environment()
            assert config_service.get_config().mcp_enabled == True

        # Should be able to reload multiple times
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false"}):
            config_service.reload_from_environment()
            assert config_service.get_config().mcp_enabled == False

    def test_configuration_change_notifications(self, config_service):
        """Test that configuration changes trigger notifications."""
        # RED: This should fail until change notifications are implemented

        changes_received = []

        def on_config_change(event: ConfigurationChangeEvent):
            changes_received.append(event)

        # Subscribe to changes
        config_service.subscribe_to_changes(on_config_change)

        # Make a change
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
            config_service.reload_from_environment()

        # Should have received notification
        assert len(changes_received) > 0
        event = changes_received[0]
        assert event.key == "mcp_enabled"
        assert event.new_value == True

    def test_configuration_from_file(self, config_service, temp_config_file):
        """Test loading configuration from JSON file."""
        # RED: This should fail until file loading is implemented

        config_service.load_from_file(temp_config_file)
        config = config_service.get_config()

        # Should load values from file
        assert config.mcp_enabled == True
        assert config.pool_enabled == True
        assert config.max_connections == 10
        assert config.connection_timeout == 30.0

    def test_configuration_precedence(self, config_service, temp_config_file):
        """Test that environment variables override file configuration."""
        # Load from file first
        config_service.load_from_file(temp_config_file)

        # Override with environment
        with patch.dict(os.environ, {"USE_MCP_POOL": "false"}):
            config_service.reload_from_environment()
            config = config_service.get_config()

            # Environment should override file
            assert config.pool_enabled == False  # From environment
            assert config.max_connections == 10  # From file (not overridden)

    def test_invalid_configuration_handling(self, config_service):
        """Test graceful handling of invalid configuration."""
        # Multiple invalid values
        with patch.dict(
            os.environ,
            {
                "MCP_MAX_CONNECTIONS": "invalid",
                "MCP_CONNECTION_TIMEOUT": "also_invalid",
                "ENABLE_MCP_FILE_SEARCH": "maybe",  # This should default to False
            },
        ):
            # Should raise ConfigurationError with details
            with pytest.raises(ConfigurationError) as exc_info:
                config_service.reload_from_environment()

            # Error should contain details about what failed
            error_message = str(exc_info.value)
            assert "MCP_MAX_CONNECTIONS" in error_message
            assert "MCP_CONNECTION_TIMEOUT" in error_message

    def test_configuration_reset_to_defaults(self, config_service):
        """Test resetting configuration to defaults."""
        # Change configuration
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
            config_service.reload_from_environment()
            assert config_service.get_config().mcp_enabled == True

        # Reset to defaults
        config_service.reset_to_defaults()
        default_config = config_service.get_config()

        # Should be back to defaults
        assert isinstance(default_config.mcp_enabled, bool)
        # Default should be False for feature flags
        assert default_config.mcp_enabled == False

    def test_configuration_serialization(self, config_service):
        """Test that configuration can be serialized for debugging."""
        config = config_service.get_config()

        # Should be able to convert to dict
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "mcp_enabled" in config_dict
        assert "pool_enabled" in config_dict

        # Should be able to convert to JSON
        config_json = config.to_json()
        assert isinstance(config_json, str)

        # Should be valid JSON
        import json

        parsed = json.loads(config_json)
        assert isinstance(parsed, dict)

    def test_configuration_environment_variable_names(self, config_service):
        """Test that all expected environment variable names are supported."""
        expected_env_vars = [
            "ENABLE_MCP_FILE_SEARCH",
            "USE_MCP_POOL",
            "MCP_MAX_CONNECTIONS",
            "MCP_CONNECTION_TIMEOUT",
            "MCP_CIRCUIT_BREAKER_THRESHOLD",
            "MCP_CIRCUIT_BREAKER_TIMEOUT",
            "ANTHROPIC_API_KEY",
            "OPENAI_API_KEY",
            "APP_DEBUG",
        ]

        # Each environment variable should be recognized
        for env_var in expected_env_vars:
            with patch.dict(os.environ, {env_var: "test_value"}):
                # Should not raise "unknown environment variable" error
                try:
                    config_service.reload_from_environment()
                except ConfigurationError as e:
                    # Error should be about invalid value, not unknown variable
                    assert "unknown" not in str(e).lower()
                except Exception:
                    # Other exceptions are fine (type conversion, etc.)
                    pass


@pytest.mark.skipif(
    not CONFIG_SERVICE_AVAILABLE, reason="Configuration service not implemented yet"
)
class TestMCPConfiguration:
    """Test the configuration data class."""

    def test_mcp_configuration_creation(self):
        """Test creating MCPConfiguration with all parameters."""
        config = MCPConfiguration(
            mcp_enabled=True,
            pool_enabled=True,
            max_connections=15,
            connection_timeout=30.0,
            circuit_breaker_threshold=5,
            circuit_breaker_timeout=60,
            anthropic_api_key="test_key",
            openai_api_key="test_key_2",
            debug_enabled=True,
        )

        assert config.mcp_enabled == True
        assert config.pool_enabled == True
        assert config.max_connections == 15
        assert config.connection_timeout == 30.0

    def test_mcp_configuration_validation(self):
        """Test that MCPConfiguration validates its inputs."""
        # Invalid max_connections
        with pytest.raises(ValueError):
            MCPConfiguration(max_connections=0)

        with pytest.raises(ValueError):
            MCPConfiguration(max_connections=-5)

        # Invalid connection_timeout
        with pytest.raises(ValueError):
            MCPConfiguration(connection_timeout=0)

        with pytest.raises(ValueError):
            MCPConfiguration(connection_timeout=-1.0)

    def test_mcp_configuration_defaults(self):
        """Test that MCPConfiguration has sensible defaults."""
        config = MCPConfiguration()

        # Feature flags should default to False for safety
        assert config.mcp_enabled == False
        assert config.pool_enabled == False
        assert config.debug_enabled == False

        # Performance settings should have reasonable defaults
        assert config.max_connections > 0
        assert config.connection_timeout > 0
        assert config.circuit_breaker_threshold > 0
        assert config.circuit_breaker_timeout > 0


@pytest.mark.skipif(CONFIG_SERVICE_AVAILABLE, reason="Only run when config service is missing")
class TestConfigurationServiceMissing:
    """Test behavior when configuration service is not available."""

    def test_import_error_graceful_handling(self):
        """Test that missing configuration service is handled gracefully."""
        # This test only runs when CONFIG_SERVICE_AVAILABLE is False
        assert not CONFIG_SERVICE_AVAILABLE

        # Attempting to import should fail cleanly
        with pytest.raises(ImportError):
            from services.infrastructure.config.mcp_configuration import MCPConfigurationService


class TestConfigurationIntegration:
    """Integration tests for configuration with existing services."""


    def test_file_repository_uses_configuration_service(self):
        """Test that FileRepository uses centralized configuration."""
        # RED: This should fail until we integrate the services

        if not CONFIG_SERVICE_AVAILABLE:
            pytest.skip("Configuration service not available")

        import inspect

        from services.repositories.file_repository import FileRepository

        # Should use configuration service instead of direct os.getenv
        source_lines = inspect.getsource(FileRepository).split("\n")
        getenv_lines = [line for line in source_lines if "os.getenv" in line]
        assert (
            len(getenv_lines) == 0
        ), f"FileRepository should use configuration service. Found os.getenv in: {getenv_lines}"


class TestConfigurationPerformance:
    """Test configuration service performance."""

    @pytest.mark.skipif(
        not CONFIG_SERVICE_AVAILABLE, reason="Configuration service not implemented yet"
    )
    def test_configuration_access_performance(self):
        """Test that configuration access is fast for hot paths."""
        service = MCPConfigurationService()

        # Configuration access should be very fast (cached)
        start_time = time.time()
        for _ in range(1000):
            config = service.get_config()
            _ = config.mcp_enabled
            _ = config.pool_enabled
        duration = time.time() - start_time

        # 1000 config accesses should take less than 10ms
        assert duration < 0.01, f"Configuration access too slow: {duration:.4f}s for 1000 accesses"

    @pytest.mark.skipif(
        not CONFIG_SERVICE_AVAILABLE, reason="Configuration service not implemented yet"
    )
    def test_configuration_reload_performance(self):
        """Test that configuration reload is reasonably fast."""
        service = MCPConfigurationService()

        # Reload should be fast enough for hot reload
        start_time = time.time()
        for _ in range(10):
            service.reload_from_environment()
        duration = time.time() - start_time

        # 10 reloads should take less than 100ms
        assert duration < 0.1, f"Configuration reload too slow: {duration:.4f}s for 10 reloads"
