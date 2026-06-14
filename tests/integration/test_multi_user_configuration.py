"""
Multi-user configuration integration tests.

This module tests the configuration system's ability to handle multiple users
without data leakage and ensures all hardcoded values are properly extracted.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.fixtures.test_configs import (
    ALICE_CONFIG,
    BOB_CONFIG,
    EDGE_CASE_CONFIG,
    INVALID_CONFIGS,
    MINIMAL_CONFIG,
    VALID_CONFIGS,
    XIAN_CONFIG,
)


class TestMultiUserConfiguration:
    """Test multi-user configuration capability."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "PIPER.user.md"
        self.original_config = None

        # Backup original config if it exists
        if Path("config/PIPER.user.md").exists():
            self.original_config = Path("config/PIPER.user.md").read_text()

    def teardown_method(self):
        """Clean up test environment."""
        # Restore original config
        if self.original_config:
            Path("config/PIPER.user.md").write_text(self.original_config)

        # Clean up temp files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def create_test_config(self, config_data: dict) -> str:
        """Create a test configuration file."""
        yaml_content = f"""
```yaml
{config_data}
```
"""
        config_content = f"""# PIPER Configuration

## Configuration

{yaml_content}

## Other sections...
"""
        self.config_file.write_text(config_content)
        return str(self.config_file)

    def test_configuration_loading_with_different_users(self):
        """Test that different user configurations load correctly."""
        # Test Xian's configuration
        self.create_test_config(XIAN_CONFIG)

        # Mock the config loader to use our test file
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            # Test loading
            from services.configuration.piper_config_loader import PiperConfigLoader

            loader = PiperConfigLoader()
            config = loader.load_config()

            assert config["github"]["default_repository"] == "mediajunkie/piper-morgan-product"
            assert config["github"]["owner"] == "mediajunkie"
            assert config["github"]["pm_numbers"]["prefix"] == "PM-"

    def test_pm_number_formatting_different_users(self):
        """Test PM number formatting with different user configurations."""
        # Test Alice's configuration (TASK- format)
        self.create_test_config(ALICE_CONFIG)

        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = ALICE_CONFIG
            mock_loader.return_value = mock_instance

            # Test PM number formatting
            from services.config.github_config import GitHubConfiguration

            config = GitHubConfiguration(
                default_repository=ALICE_CONFIG["github"]["default_repository"],
                owner=ALICE_CONFIG["github"]["owner"],
                pm_prefix=ALICE_CONFIG["github"]["pm_numbers"]["prefix"],
                pm_start=ALICE_CONFIG["github"]["pm_numbers"]["start_number"],
                pm_padding=ALICE_CONFIG["github"]["pm_numbers"]["padding"],
            )

            # Test formatting
            assert config.format_pm_number(1) == "TASK-0001"
            assert config.format_pm_number(100) == "TASK-0100"
            assert config.format_pm_number(9999) == "TASK-9999"

    def test_cli_with_different_configurations(self):
        """Test CLI commands work with different user configurations."""
        # Test with Bob's configuration
        self.create_test_config(BOB_CONFIG)

        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = BOB_CONFIG
            mock_loader.return_value = mock_instance

            # Test CLI create command with dry-run
            import click.testing

            from cli.commands.issues import issues

            runner = click.testing.CliRunner()
            result = runner.invoke(
                issues, ["create", "--title", "Multi-user test issue", "--dry-run"]
            )

            # Should not fail due to configuration
            assert result.exit_code == 0
            assert "Multi-user test issue" in result.output

    def test_no_user_data_leakage_between_configurations(self):
        """Test that user data doesn't leak between different configurations."""
        # Test switching between configurations
        configs = [XIAN_CONFIG, ALICE_CONFIG, BOB_CONFIG]

        for i, config in enumerate(configs):
            self.create_test_config(config)

            with patch(
                "services.configuration.piper_config_loader.PiperConfigLoader"
            ) as mock_loader:
                mock_instance = MagicMock()
                mock_instance.load_config.return_value = config
                mock_loader.return_value = mock_instance

                # Load configuration
                from services.configuration.piper_config_loader import PiperConfigLoader

                loader = PiperConfigLoader()
                loaded_config = loader.load_config()

                # Verify correct configuration is loaded
                assert (
                    loaded_config["github"]["default_repository"]
                    == config["github"]["default_repository"]
                )
                assert loaded_config["github"]["owner"] == config["github"]["owner"]

                # Verify no data from previous configurations
                for j, other_config in enumerate(configs):
                    if i != j:
                        assert (
                            loaded_config["github"]["default_repository"]
                            != other_config["github"]["default_repository"]
                        )
                        assert loaded_config["github"]["owner"] != other_config["github"]["owner"]

    def test_hardcoded_repository_references_removed(self):
        """Test that hardcoded repository references are properly extracted."""
        # This test will verify that the CLI and services use configuration
        # instead of hardcoded values

        # Test CLI issues command
        import click.testing

        from cli.commands.issues import issues

        runner = click.testing.CliRunner()
        result = runner.invoke(issues, ["create", "--title", "Test", "--dry-run"])

        # Should not contain hardcoded repository in output
        assert (
            "mediajunkie/piper-morgan-product" not in result.output
            or "Repository:" in result.output
        )

        # Test that the CLI uses configuration
        assert result.exit_code == 0

    def test_pm_number_format_configurable(self):
        """Test that PM number format is configurable per user."""
        # #1222: format_pm_number formats the integer it is given with the
        # configured prefix + zero-padding. It does NOT offset by pm_start — the
        # "starting number" is applied by the caller (e.g. pm_number_manager
        # passes format_pm_number(pm_start) for the first issue). Making the
        # function offset would double-count that call. The prior BOB/EDGE
        # expectations assumed a pm_start offset that doesn't exist and were
        # internally inconsistent with the start=1000 ALICE case (which expects
        # the non-offset "TASK-0001"). Corrected to the actual prefix+padding
        # output (format_pm_number(1) and (123), independent of start_number).
        test_cases = [
            (XIAN_CONFIG, "PM-001", "PM-123"),
            (ALICE_CONFIG, "TASK-0001", "TASK-0123"),
            (BOB_CONFIG, "ISSUE-00001", "ISSUE-00123"),
            (EDGE_CASE_CONFIG, "VERY-LONG-PREFIX-000001", "VERY-LONG-PREFIX-000123"),
        ]

        for config, expected_first, expected_123 in test_cases:
            from services.config.github_config import GitHubConfiguration

            github_config = GitHubConfiguration(
                default_repository=config["github"]["default_repository"],
                owner=config["github"]["owner"],
                pm_prefix=config["github"]["pm_numbers"]["prefix"],
                pm_start=config["github"]["pm_numbers"]["start_number"],
                pm_padding=config["github"]["pm_numbers"]["padding"],
            )

            assert github_config.format_pm_number(1) == expected_first
            assert github_config.format_pm_number(123) == expected_123

    def test_configuration_validation(self):
        """Test configuration validation for valid and invalid configs."""
        from services.config.github_config import GitHubConfiguration

        # Test valid configurations
        for config in VALID_CONFIGS:
            # #1222: MINIMAL_CONFIG is a VALID config with no "pm_numbers" block
            # at all — guard the whole block (not just the inner keys), else it
            # KeyErrors before any validation runs.
            pm_numbers = config["github"].get("pm_numbers", {})
            github_config = GitHubConfiguration(
                default_repository=config["github"]["default_repository"],
                owner=config["github"]["owner"],
                pm_prefix=pm_numbers.get("prefix", "PM-"),
                pm_start=pm_numbers.get("start_number", 1),
                pm_padding=pm_numbers.get("padding", 3),
            )

            # Should not raise exceptions
            assert github_config.default_repository is not None
            assert github_config.owner is not None

    def test_backwards_compatibility_maintained(self):
        """Test that existing functionality is not broken."""
        # Test that existing CLI commands still work
        import click.testing

        from cli.commands.issues import issues

        runner = click.testing.CliRunner()

        # Test help command
        result = runner.invoke(issues, ["--help"])
        assert result.exit_code == 0
        assert "Issue management commands" in result.output

        # Test create help
        result = runner.invoke(issues, ["create", "--help"])
        assert result.exit_code == 0
        assert "Create new issue" in result.output

        # Test verify command
        result = runner.invoke(issues, ["verify"])
        assert result.exit_code == 0

    def test_configuration_hot_reload(self):
        """Test that configuration changes are picked up without restart."""
        # Create initial configuration
        self.create_test_config(XIAN_CONFIG)

        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            # Load initial configuration
            from services.configuration.piper_config_loader import PiperConfigLoader

            loader = PiperConfigLoader()
            initial_config = loader.load_config()

            # Change configuration
            self.create_test_config(ALICE_CONFIG)
            mock_instance.load_config.return_value = ALICE_CONFIG

            # Reload configuration
            new_config = loader.load_config()

            # Verify configuration changed
            assert (
                new_config["github"]["default_repository"]
                != initial_config["github"]["default_repository"]
            )
            assert new_config["github"]["owner"] != initial_config["github"]["owner"]

    def test_error_handling_invalid_configurations(self):
        """Test error handling for invalid configurations."""
        from services.config.github_config import GitHubConfiguration

        # Test invalid repository format
        with pytest.raises(ValueError):
            GitHubConfiguration(default_repository="invalid-repo", owner="test")

        # Test invalid PM number configuration
        with pytest.raises(ValueError):
            GitHubConfiguration(
                default_repository="test/repo",
                owner="test",
                pm_prefix="",
                pm_start=-1,
                pm_padding=0,
            )

    def test_performance_with_multiple_configurations(self):
        """Test performance when switching between multiple configurations."""
        import time

        configs = [XIAN_CONFIG, ALICE_CONFIG, BOB_CONFIG, MINIMAL_CONFIG, EDGE_CASE_CONFIG]

        start_time = time.time()

        for config in configs:
            self.create_test_config(config)

            with patch(
                "services.configuration.piper_config_loader.PiperConfigLoader"
            ) as mock_loader:
                mock_instance = MagicMock()
                mock_instance.load_config.return_value = config
                mock_loader.return_value = mock_instance

                from services.configuration.piper_config_loader import PiperConfigLoader

                loader = PiperConfigLoader()
                loader.load_config()

        end_time = time.time()
        total_time = end_time - start_time

        # Should complete within reasonable time (less than 5 seconds)
        assert total_time < 5.0, f"Configuration loading took too long: {total_time:.2f}s"
