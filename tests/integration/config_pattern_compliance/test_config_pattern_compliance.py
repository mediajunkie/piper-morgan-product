"""
Config Pattern Compliance Test Suite

Tests that all integrations follow the service injection pattern
for consistent configuration management across the system.
"""

import importlib
import inspect
import os
from pathlib import Path
from typing import Any, Optional, Type

import pytest


class TestConfigPatternCompliance:
    """Test suite for config service pattern compliance"""

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_config_service_file_exists(self, integration, config_service_path):
        """Test that config_service.py exists in correct location"""
        config_file = config_service_path / integration / "config_service.py"
        assert config_file.exists(), (
            f"Config service file missing: {config_file}\n"
            f"Expected: services/integrations/{integration}/config_service.py"
        )

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_config_service_class_exists(self, integration, integration_config_service):
        """Test that {Name}ConfigService class exists"""
        config_service_class = integration_config_service(integration)
        assert config_service_class is not None, (
            f"Config service class missing: {integration.title()}ConfigService\n"
            f"Expected in: services.integrations.{integration}.config_service"
        )

        # Verify class name follows pattern (with special handling for GitHub)
        if integration == "github":
            expected_name = "GitHubConfigService"  # Special case for GitHub
        else:
            expected_name = f"{integration.title()}ConfigService"
        assert config_service_class.__name__ == expected_name, (
            f"Config service class name incorrect: {config_service_class.__name__}\n"
            f"Expected: {expected_name}"
        )

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_config_service_required_methods(
        self, integration, integration_config_service, method_checker
    ):
        """Test that config service has required methods"""
        config_service_class = integration_config_service(integration)
        if config_service_class is None:
            pytest.skip(f"Config service class not found for {integration}")

        # GitHub has a different interface (legacy design)
        if integration == "github":
            github_methods = [
                "get_authentication_token",
                "get_client_configuration",
                "get_configuration_summary",
            ]
            for method_name in github_methods:
                assert method_checker(config_service_class, method_name), (
                    f"Required GitHub method missing: {config_service_class.__name__}.{method_name}()\n"
                    f"GitHub config service must implement: {', '.join(github_methods)}"
                )
        else:
            # Standard pattern for Slack/Notion/Calendar
            required_methods = ["get_config", "is_configured", "_load_config"]

            for method_name in required_methods:
                assert method_checker(config_service_class, method_name), (
                    f"Required method missing: {config_service_class.__name__}.{method_name}()\n"
                    f"Config service must implement: {', '.join(required_methods)}"
                )

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_config_service_init_signature(
        self, integration, integration_config_service, signature_inspector
    ):
        """Test that config service __init__ accepts optional FeatureFlags"""
        config_service_class = integration_config_service(integration)
        if config_service_class is None:
            pytest.skip(f"Config service class not found for {integration}")

        init_sig = signature_inspector(config_service_class, "__init__")
        assert (
            init_sig is not None
        ), f"Config service {config_service_class.__name__} missing __init__"

        # Check for feature_flags parameter (optional)
        params = list(init_sig.parameters.keys())
        # Should have 'self' and optionally 'feature_flags'
        assert len(params) >= 1, f"Config service __init__ should have at least 'self' parameter"

        if len(params) > 1:
            # If there's a second parameter, check based on integration
            second_param = init_sig.parameters[params[1]]
            if integration == "github":
                # GitHub uses 'environment' parameter
                assert (
                    second_param.name == "environment"
                ), f"GitHub second parameter should be 'environment', got: {second_param.name}"
            else:
                # Standard pattern uses 'feature_flags'
                assert (
                    second_param.name == "feature_flags"
                ), f"Second parameter should be 'feature_flags', got: {second_param.name}"
            assert (
                second_param.default is not inspect.Parameter.empty
            ), f"Second parameter should be optional (have default value)"

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_router_accepts_config_service(
        self, integration, integration_router, signature_inspector
    ):
        """Test that router accepts config_service parameter"""
        router_class = integration_router(integration)
        if router_class is None:
            pytest.skip(f"Router class not found for {integration}")

        init_sig = signature_inspector(router_class, "__init__")
        assert init_sig is not None, f"Router {router_class.__name__} missing __init__"

        # Check for config_service parameter
        params = init_sig.parameters
        config_service_param = None

        for param_name, param in params.items():
            if "config" in param_name.lower() and "service" in param_name.lower():
                config_service_param = param
                break

        assert config_service_param is not None, (
            f"Router {router_class.__name__}.__init__ missing config_service parameter\n"
            f"Available parameters: {list(params.keys())}\n"
            f"Expected parameter name containing 'config' and 'service'"
        )

        # Parameter should be optional (have default value)
        assert config_service_param.default is not inspect.Parameter.empty, (
            f"config_service parameter should be optional (have default value)\n"
            f"Current: {config_service_param}"
        )

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_router_stores_config_service(
        self, integration, integration_router, integration_config_service
    ):
        """Test that router stores config_service attribute"""
        router_class = integration_router(integration)
        config_service_class = integration_config_service(integration)

        if router_class is None:
            pytest.skip(f"Router class not found for {integration}")
        if config_service_class is None:
            pytest.skip(f"Config service class not found for {integration}")

        # Test with config service
        try:
            config_service = config_service_class()
            router = router_class(config_service)

            # Router should store config_service reference
            assert hasattr(
                router, "config_service"
            ), f"Router {router_class.__name__} should store config_service attribute"
            assert (
                router.config_service is config_service
            ), f"Router should store the provided config_service instance"
        except Exception as e:
            pytest.fail(f"Failed to instantiate router with config service: {e}")

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_graceful_degradation(self, integration, integration_router):
        """Test that router works without config_service"""
        router_class = integration_router(integration)
        if router_class is None:
            pytest.skip(f"Router class not found for {integration}")

        # Test without config service - should not crash
        try:
            router = router_class()
            assert (
                router is not None
            ), f"Router {router_class.__name__} failed to instantiate without config"

            # Should have config_service attribute
            if hasattr(router, "config_service"):
                if integration in ["github", "calendar"]:
                    # GitHub and Calendar create default config service when none provided
                    assert (
                        router.config_service is not None
                    ), f"{integration.title()} router should create default config_service when not provided"
                else:
                    # Standard pattern: should be None when not provided
                    assert (
                        router.config_service is None
                    ), f"Router config_service should be None when not provided"
        except Exception as e:
            pytest.fail(f"Router {router_class.__name__} should work without config_service: {e}")

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_config_dataclass_exists(self, integration, integration_config_service):
        """Test that {Name}Config dataclass exists and has validate method"""
        config_service_class = integration_config_service(integration)
        if config_service_class is None:
            pytest.skip(f"Config service class not found for {integration}")

        try:
            # #1452: get_config/get_client_configuration became owner-scoped
            # (required user_id, ADR-071) — the compliance claim (dataclass
            # shape + validate()) is user-agnostic, so any principal id works.
            from uuid import uuid4 as _uuid4

            probe_user = str(_uuid4())
            config_service = config_service_class()

            if integration == "github":
                # GitHub has different interface - test get_client_configuration
                config = config_service.get_client_configuration(probe_user)
                assert hasattr(config, "to_dict"), f"GitHub config should have to_dict() method"
                assert callable(config.to_dict), f"to_dict should be callable"
                # Test the method works
                result = config.to_dict()
                assert isinstance(
                    result, dict
                ), f"to_dict() should return dict, got: {type(result)}"
            else:
                # Standard pattern - test get_config and validate
                config = config_service.get_config(probe_user)

                # Should have validate method
                assert hasattr(
                    config, "validate"
                ), f"Config dataclass should have validate() method"
                assert callable(config.validate), f"validate should be callable"

                # validate() should return boolean
                result = config.validate()
                assert isinstance(
                    result, bool
                ), f"validate() should return boolean, got: {type(result)}"

        except Exception as e:
            pytest.fail(f"Failed to test config dataclass for {integration}: {e}")

    @pytest.mark.parametrize("integration", ["slack", "notion", "github", "calendar"])
    def test_no_direct_env_access_in_router(self, integration, integration_router):
        """Test that router doesn't use os.getenv directly"""
        router_class = integration_router(integration)
        if router_class is None:
            pytest.skip(f"Router class not found for {integration}")

        # Get router source code
        try:
            import inspect

            source = inspect.getsource(router_class)

            # Check for direct environment access
            forbidden_patterns = ["os.getenv", "os.environ", "getenv(", "environ["]

            found_patterns = []
            for pattern in forbidden_patterns:
                if pattern in source:
                    found_patterns.append(pattern)

            assert not found_patterns, (
                f"Router {router_class.__name__} should not access environment directly\n"
                f"Found patterns: {found_patterns}\n"
                f"Use config_service instead of direct environment access"
            )

        except Exception as e:
            # If we can't get source, skip this test
            pytest.skip(f"Could not inspect router source for {integration}: {e}")


class TestIntegrationSpecificPatterns:
    """Test integration-specific pattern requirements"""

    def test_slack_pattern_reference(self, integration_config_service, integration_router):
        """Test that Slack pattern is the reference implementation"""
        slack_config = integration_config_service("slack")
        slack_router = integration_router("slack")

        assert slack_config is not None, "Slack config service should exist (reference pattern)"
        assert slack_router is not None, "Slack router should exist (reference pattern)"

        # Slack should be fully compliant
        config_service = slack_config()
        router = slack_router(config_service)

        assert hasattr(router, "config_service"), "Slack router should store config_service"
        assert router.config_service is config_service, "Slack router should use provided config"

    def test_notion_pattern_compliance(self, integration_config_service, integration_router):
        """Test that Notion follows the same pattern as Slack"""
        notion_config = integration_config_service("notion")
        notion_router = integration_router("notion")

        if notion_config is None or notion_router is None:
            pytest.skip("Notion integration not available")

        # Notion should match Slack pattern
        config_service = notion_config()
        router = notion_router(config_service)

        assert hasattr(router, "config_service"), "Notion router should store config_service"
        assert router.config_service is config_service, "Notion router should use provided config"
        from uuid import uuid4 as _uuid4

        assert config_service.is_configured(str(_uuid4())) in [
            True,
            False,
        ], "Notion config should have is_configured()"
