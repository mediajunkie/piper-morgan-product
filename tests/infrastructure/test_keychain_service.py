"""Tests for KeychainService"""

import os
from unittest.mock import Mock, patch

import keyring
import pytest

from services.infrastructure.keychain_service import (
    KeychainEntry,
    KeychainService,
    get_keychain_service,
)


class TestKeychainService:
    """Test keychain service functionality"""

    @pytest.fixture
    def service(self):
        """Create keychain service for testing"""
        return KeychainService(service_name="piper-test")

    @pytest.fixture(autouse=True)
    def cleanup(self, service):
        """Clean up test keys after each test"""
        yield
        # Clean up any test keys
        for provider in ["test-provider", "openai", "anthropic"]:
            try:
                service.delete_api_key(provider)
            except:
                pass

    def test_store_and_retrieve_api_key(self, service):
        """Can store and retrieve API key"""
        service.store_api_key("test-provider", "test-key-123")

        retrieved = service.get_api_key("test-provider")
        assert retrieved == "test-key-123"

    def test_retrieve_nonexistent_key(self, service):
        """Returns None for nonexistent key"""
        result = service.get_api_key("nonexistent-provider")
        assert result is None

    def test_delete_api_key(self, service):
        """Can delete API key"""
        service.store_api_key("test-provider", "test-key")
        assert service.get_api_key("test-provider") == "test-key"

        deleted = service.delete_api_key("test-provider")
        assert deleted is True
        assert service.get_api_key("test-provider") is None

    def test_delete_nonexistent_key(self, service):
        """Deleting nonexistent key returns False"""
        result = service.delete_api_key("nonexistent-provider")
        assert result is False

    def test_store_empty_provider_raises_error(self, service):
        """Empty provider name raises ValueError"""
        with pytest.raises(ValueError, match="Provider name cannot be empty"):
            service.store_api_key("", "test-key")

    def test_store_empty_key_raises_error(self, service):
        """Empty API key raises ValueError"""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            service.store_api_key("test-provider", "")

    def test_list_stored_keys(self, service):
        """Lists providers with stored keys"""
        service.store_api_key("openai", "test-key-1")
        service.store_api_key("anthropic", "test-key-2")

        stored = service.list_stored_keys()
        assert "openai" in stored
        assert "anthropic" in stored

    def test_check_migration_status(self, service):
        """Checks migration status correctly"""
        # Store one key in keychain
        service.store_api_key("openai", "test-key")

        # Control the WHOLE env surface this test asserts on, not just one var —
        # on keyed seats conftest loads real OPENAI/GEMINI keys into the env from
        # the keychain (first bit 2026-08-01 when the Amber keychain was
        # provisioned). The assertions below are about THIS test's env, so the
        # test must clear the vars it asserts absent, not assume a keyless seat.
        env = {k: v for k, v in os.environ.items()
               if k not in ("OPENAI_API_KEY", "GEMINI_API_KEY")}
        env["ANTHROPIC_API_KEY"] = "env-key"
        with patch.dict("os.environ", env, clear=True):
            status = service.check_migration_status(["openai", "anthropic", "gemini"])

        assert status["openai"].exists_in_keychain is True
        assert status["openai"].exists_in_env is False

        assert status["anthropic"].exists_in_keychain is False
        assert status["anthropic"].exists_in_env is True

        assert status["gemini"].exists_in_keychain is False
        assert status["gemini"].exists_in_env is False

    def test_get_keychain_service_singleton(self):
        """Global keychain service is singleton"""
        service1 = get_keychain_service()
        service2 = get_keychain_service()
        assert service1 is service2


class TestKeychainIntegration:
    """Integration tests with actual keychain"""

    def test_real_keychain_roundtrip(self):
        """Can store and retrieve from real macOS keychain"""
        service = KeychainService(service_name="piper-test-integration")

        # Store
        service.store_api_key("integration-test", "secret-key-123")

        # Retrieve
        retrieved = service.get_api_key("integration-test")
        assert retrieved == "secret-key-123"

        # Clean up
        service.delete_api_key("integration-test")
        assert service.get_api_key("integration-test") is None
