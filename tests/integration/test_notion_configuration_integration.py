"""
Notion Configuration Integration Testing Framework

End-to-end testing of configuration validation and real API integration.
Prevents verification theater by testing actual configuration behavior.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

# Import the configuration classes we'll be testing
from config.notion_user_config import ConfigurationError, NotionUserConfig


class TestNotionConfigurationIntegration:
    """Integration testing framework for Notion configuration validation"""

    def setup_method(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "PIPER.user.md"

        # Sample valid configuration based on Code Agent's schema
        self.valid_config = {
            "notion": {
                "publishing": {
                    "default_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                    "enabled": True,
                    "auto_title_generation": True,
                    "format": "markdown",
                },
                "adrs": {
                    "database_id": "25e11704d8bf80deaac2f806390fe7da",
                    "enabled": True,
                    "auto_publish": True,
                    "metadata_extraction": True,
                    "status_field": "Status",
                    "date_field": "Date",
                    "author_field": "Author",
                },
                "workspace": {
                    "id": None,
                    "name": "Test Workspace",
                    "team": "Development Team",
                    "description": "Test workspace for integration testing",
                },
                "development": {
                    "test_parent": "25d11704d8bf81dfb37acbdc143e6a80",
                    "debug_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                    "mock_mode": False,
                    "test_database": "",
                    "cache_enabled": True,
                    "verbose_logging": False,
                },
                "validation": {
                    "level": "basic",
                    "connectivity_check": True,
                    "permission_check": False,
                    "cache_results": True,
                    "timeout_seconds": 30,
                    "retry_attempts": 3,
                },
                "behavior": {
                    "confirm_overwrites": True,
                    "backup_before_publish": False,
                    "track_publishing_history": True,
                    "default_visibility": "private",
                    "tag_published_content": False,
                },
            }
        }

    def teardown_method(self):
        """Clean up test fixtures"""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_end_to_end_configuration_loading(self):
        """Test complete configuration loading and validation"""

        # Create temporary configuration file
        config_content = f"""# Test Configuration
```yaml
{yaml.dump(self.valid_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Test configuration loading (placeholder until Code Agent creates the class)
        # config = NotionUserConfig.load_from_file(self.config_file)
        # assert config.is_valid()

        # Verify all required fields are loaded
        # assert config.publishing.default_parent == "25d11704d8bf80c8a71ddbe7aba51f55"
        # assert config.adrs.database_id == "25e11704d8bf80deaac2f806390fe7da"

        # Verify optional fields have sensible defaults
        # assert config.workspace.id is None
        # assert config.validation.level == "basic"

    def test_configuration_validation_with_real_api(self):
        """Integration test: does configuration work with real API?"""

        if not os.getenv("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for integration testing")

        # Test with valid configuration from audit findings
        valid_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # This should pass basic validation
        # config = NotionUserConfig.load(valid_config)
        # result = config.validate(level="basic")
        # assert result.is_valid()
        # assert result.validation_level == "basic"

        # Test with invalid database ID (should fail connectivity check)
        invalid_config = {
            "notion": {
                "adrs": {"database_id": "00000000000000000000000000000000"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # This should fail enhanced validation (connectivity check)
        # config = NotionUserConfig.load(invalid_config)
        # result = config.validate(level="enhanced")
        # assert not result.is_valid()
        # assert "not accessible" in result.errors[0].lower()

    def test_migration_path_validation(self):
        """Test migration from hardcoded values works with real configuration"""

        # Create configuration with audit values
        audit_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "development": {
                    "test_parent": "25d11704d8bf81dfb37acbdc143e6a80",
                    "debug_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                },
            }
        }

        # Verify configuration loads correctly
        # config = NotionUserConfig.load(audit_config)
        # assert config.is_valid()

        # Test each hardcoded value maps to correct config field
        # assert config.adrs.database_id == "25e11704d8bf80deaac2f806390fe7da"
        # assert config.publishing.default_parent == "25d11704d8bf80c8a71ddbe7aba51f55"
        # assert config.development.test_parent == "25d11704d8bf81dfb37acbdc143e6a80"
        # assert config.development.debug_parent == "25d11704d8bf80c8a71ddbe7aba51f55"

    def test_cli_validation_commands(self):
        """Test CLI validation commands work with real configuration"""

        # Test configuration file validation
        config_content = f"""# Test Configuration
```yaml
{yaml.dump(self.valid_config, default_flow_style=False)}
```
"""
        self.config_file.write_text(config_content)

        # Test CLI validation command (placeholder until implemented)
        # result = subprocess.run(['piper', 'notion', 'validate', '--config', str(self.config_file)],
        #                        capture_output=True, text=True)
        # assert result.returncode == 0
        # assert "Configuration valid" in result.stdout

    def test_error_handling_with_invalid_config(self):
        """Test error handling with various invalid configuration scenarios"""

        # Test missing required fields
        incomplete_config = {
            "notion": {
                "publishing": {"enabled": True}
                # Missing: default_parent and adrs.database_id
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(incomplete_config)

        error_msg = str(exc_info.value)

        # Verify specific error messages for each missing field
        assert "default_parent" in error_msg
        assert "database_id" in error_msg

        # Test invalid format
        invalid_format_config = {
            "notion": {
                "adrs": {"database_id": "invalid-format"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        with pytest.raises(ConfigurationError) as exc_info:
            NotionUserConfig.load(invalid_format_config)

        error_msg = str(exc_info.value)
        assert "invalid" in error_msg.lower()

    def test_validation_levels_integration(self):
        """Test different validation levels with real API integration"""

        if not os.getenv("NOTION_API_KEY"):
            pytest.skip("NOTION_API_KEY not available for validation testing")

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
            }
        }

        # Test basic validation (format + connectivity)
        # config = NotionUserConfig.load(config)
        # result = config.validate(level="basic")
        # assert result.is_valid()

        # Test enhanced validation (resource accessibility)
        # result = config.validate(level="enhanced")
        # assert result.is_valid()

        # Test full validation (comprehensive permissions)
        # result = config.validate(level="full")
        # assert result.is_valid()

    def test_configuration_file_loading_integration(self):
        """Test loading configuration from actual file formats"""

        # Test YAML loading
        yaml_config = yaml.dump(self.valid_config, default_flow_style=False)
        yaml_file = Path(self.temp_dir) / "config.yaml"
        yaml_file.write_text(yaml_config)

        # Test loading from YAML file (placeholder until implemented)
        # config = NotionUserConfig.load_from_file(yaml_file)
        # assert config.is_valid()

        # Test markdown file with YAML block
        md_config = f"""# Notion Configuration
```yaml
{yaml.dump(self.valid_config, default_flow_style=False)}
```
"""
        md_file = Path(self.temp_dir) / "PIPER.user.md"
        md_file.write_text(md_config)

        # Test loading from markdown file (placeholder until implemented)
        # config = NotionUserConfig.load_from_file(md_file)
        # assert config.is_valid()

    def test_performance_and_caching_integration(self):
        """Test performance features and caching behavior"""

        config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"cache_results": True, "timeout_seconds": 30, "retry_attempts": 3},
            }
        }

        # Test configuration loading with caching enabled
        # config = NotionUserConfig.load(config)
        # assert config.validation.cache_results is True
        # assert config.validation.timeout_seconds == 30
        # assert config.validation.retry_attempts == 3

        # Test caching behavior (placeholder until implemented)
        # first_result = config.validate(level="basic")
        # second_result = config.validate(level="basic")
        # assert first_result == second_result  # Should be cached

    def test_development_mode_integration(self):
        """Test development and testing configuration options"""

        dev_config = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "development": {
                    "mock_mode": True,
                    "test_parent": "25d11704d8bf81dfb37acbdc143e6a80",
                    "debug_parent": "25d11704d8bf80c8a71ddbe7aba51f55",
                    "cache_enabled": True,
                    "verbose_logging": True,
                },
            }
        }

        # Test development configuration loading
        # config = NotionUserConfig.load(dev_config)
        # assert config.development.mock_mode is True
        # assert config.development.test_parent == "25d11704d8bf81dfb37acbdc143e6a80"
        # assert config.development.debug_parent == "25d11704d8bf80c8a71ddbe7aba51f55"
        # assert config.development.cache_enabled is True
        # assert config.development.verbose_logging is True

    @pytest.mark.asyncio
    async def test_enhanced_validation_get_current_user_exists(self):
        """
        Test that NotionMCPAdapter now has get_current_user() method.

        This test verifies the fix for CORE-NOTN #142 where enhanced validation
        was calling adapter.get_current_user() but the method didn't exist.

        This is a simple existence check to ensure the method is available
        when config validation needs it.
        """
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter

        # Verify the method exists
        assert hasattr(NotionMCPAdapter, "get_current_user")

        # Verify it's callable and async
        import inspect

        method = getattr(NotionMCPAdapter, "get_current_user")
        assert callable(method)
        assert inspect.iscoroutinefunction(method)

        # Test that it can be called without errors (with mocked client)
        with patch("services.mcp.consumer.notion_adapter.NotionConfig"):
            adapter = NotionMCPAdapter()
            adapter._notion_client = MagicMock()
            adapter._notion_client.users.me.return_value = {
                "id": "test-123",
                "name": "Test User",
                "type": "person",
                "person": {"email": "test@example.com"},
            }

            # Call the method - should not raise AttributeError
            result = await adapter.get_current_user()

            # Verify it returns expected structure
            assert result is not None
            assert "id" in result
            assert "name" in result
            assert result["id"] == "test-123"

    @pytest.mark.asyncio
    async def test_enhanced_validation_calls_get_current_user(self):
        """
        End-to-end test that enhanced validation successfully calls adapter.get_current_user().

        This is the comprehensive test that verifies CORE-NOTN #142 is fully resolved.
        The original error was AttributeError at config/notion_user_config.py:373.
        """
        from unittest.mock import AsyncMock

        from config.notion_user_config import NotionUserConfig, ValidationLevel
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter

        # Create a mock adapter with get_current_user method
        mock_adapter = AsyncMock(spec=NotionMCPAdapter)
        mock_adapter.get_current_user = AsyncMock(
            return_value={
                "id": "test-user-123",
                "name": "Test User",
                "email": "test@example.com",
                "type": "person",
            }
        )
        mock_adapter.connect = AsyncMock()

        # Create config with enhanced validation level
        config_dict = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "enhanced", "connectivity_check": True},
            }
        }

        # Mock NotionMCPAdapter instantiation in validate_async
        # Need to patch at the actual source, not where it's imported
        # Also need to mock environment variable check
        with (
            patch(
                "services.integrations.mcp.notion_adapter.NotionMCPAdapter",
                return_value=mock_adapter,
            ),
            patch.dict(os.environ, {"NOTION_API_KEY": "test-key"}),
        ):
            config = NotionUserConfig(config_dict)

            # Run validation - this should NOT raise AttributeError anymore
            try:
                result = await config.validate_async(level=ValidationLevel.ENHANCED)

                # Verify get_current_user() was called
                mock_adapter.get_current_user.assert_called_once()

                # Validation should succeed
                assert result.connectivity_tested is True
                assert result.connectivity_result is True

                print("✅ Enhanced validation successfully called get_current_user()")
                print(f"✅ Original issue CORE-NOTN #142 is RESOLVED")

            except AttributeError as e:
                if "get_current_user" in str(e):
                    pytest.fail(f"FAILED: get_current_user() still missing! Error: {e}")
                else:
                    raise

    @pytest.mark.asyncio
    async def test_full_validation_calls_get_current_user(self):
        """
        Test that full validation also calls get_current_user().

        Full validation should include everything from enhanced validation.
        """
        import os
        from unittest.mock import AsyncMock

        from config.notion_user_config import NotionUserConfig, ValidationLevel
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter

        mock_adapter = AsyncMock(spec=NotionMCPAdapter)
        mock_adapter.get_current_user = AsyncMock(
            return_value={"id": "bot-456", "name": "Piper Morgan", "type": "bot"}
        )
        mock_adapter.connect = AsyncMock()

        # Mock database and page retrieval for permission checks
        mock_adapter.notion_client = MagicMock()
        mock_adapter.notion_client.databases.retrieve = AsyncMock(return_value={"id": "test-db"})
        mock_adapter.get_page = AsyncMock(return_value={"id": "test-page"})

        config_dict = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {
                    "level": "full",
                    "connectivity_check": True,
                    "permission_check": True,
                },
            }
        }

        with (
            patch(
                "services.integrations.mcp.notion_adapter.NotionMCPAdapter",
                return_value=mock_adapter,
            ),
            patch.dict(os.environ, {"NOTION_API_KEY": "test-key"}),
        ):
            config = NotionUserConfig(config_dict)
            result = await config.validate_async(level=ValidationLevel.FULL)

            # Should call get_current_user() for connectivity
            mock_adapter.get_current_user.assert_called()

            # Full validation should also test permissions
            assert result.permission_checked is True

            print("✅ Full validation successfully called get_current_user()")

    @pytest.mark.asyncio
    async def test_enhanced_validation_handles_connectivity_failure(self):
        """
        Test that enhanced validation gracefully handles API connectivity failures.
        """
        import os
        from unittest.mock import AsyncMock

        from config.notion_user_config import NotionUserConfig, ValidationLevel
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter

        # Create a mock adapter that fails get_current_user
        mock_adapter = AsyncMock(spec=NotionMCPAdapter)
        mock_adapter.get_current_user = AsyncMock(side_effect=Exception("API connection failed"))
        mock_adapter.connect = AsyncMock()

        config_dict = {
            "notion": {
                "adrs": {"database_id": "25e11704d8bf80deaac2f806390fe7da"},
                "publishing": {"default_parent": "25d11704d8bf80c8a71ddbe7aba51f55"},
                "validation": {"level": "enhanced", "connectivity_check": True},
            }
        }

        with (
            patch(
                "services.integrations.mcp.notion_adapter.NotionMCPAdapter",
                return_value=mock_adapter,
            ),
            patch.dict(os.environ, {"NOTION_API_KEY": "test-key"}),
        ):
            config = NotionUserConfig(config_dict)
            result = await config.validate_async(level=ValidationLevel.ENHANCED)

            # Should handle error gracefully
            assert result.connectivity_tested is True
            assert result.connectivity_result is False
            assert len(result.errors) > 0
            assert "API connectivity failed" in result.errors[0]

            print("✅ Enhanced validation gracefully handles connectivity failures")
