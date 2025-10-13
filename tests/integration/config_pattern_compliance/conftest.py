"""
Pytest fixtures for config pattern compliance tests
"""

import importlib
import inspect
from pathlib import Path
from typing import Any, Optional, Type

import pytest


@pytest.fixture
def integration_names():
    """List of integrations to test for compliance"""
    return ["slack", "notion", "github", "calendar"]


@pytest.fixture
def config_service_path():
    """Base path for config services"""
    return Path("services/integrations")


@pytest.fixture
def integration_config_service():
    """Factory fixture to get config service for integration"""

    def _get_config_service(integration_name: str) -> Optional[Type]:
        try:
            module_path = f"services.integrations.{integration_name}.config_service"
            module = importlib.import_module(module_path)

            # Look for {Name}ConfigService class with special handling for GitHub
            if integration_name == "github":
                class_name = "GitHubConfigService"  # Special case for GitHub
            else:
                class_name = f"{integration_name.title()}ConfigService"
            return getattr(module, class_name, None)
        except ImportError:
            return None

    return _get_config_service


@pytest.fixture
def integration_router():
    """Factory fixture to get router for integration"""

    def _get_router(integration_name: str) -> Optional[Type]:
        try:
            module_path = (
                f"services.integrations.{integration_name}.{integration_name}_integration_router"
            )
            module = importlib.import_module(module_path)

            # Look for {Name}IntegrationRouter class with special handling for GitHub
            if integration_name == "github":
                class_name = "GitHubIntegrationRouter"  # Special case for GitHub
            else:
                class_name = f"{integration_name.title()}IntegrationRouter"
            return getattr(module, class_name, None)
        except ImportError:
            return None

    return _get_router


@pytest.fixture
def method_checker():
    """Utility to check if class has required methods"""

    def _check_method(cls: Type, method_name: str) -> bool:
        return hasattr(cls, method_name) and callable(getattr(cls, method_name))

    return _check_method


@pytest.fixture
def signature_inspector():
    """Utility to inspect method signatures"""

    def _get_signature(cls: Type, method_name: str):
        if hasattr(cls, method_name):
            method = getattr(cls, method_name)
            return inspect.signature(method)
        return None

    return _get_signature
