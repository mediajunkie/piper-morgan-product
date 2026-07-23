"""Tests for LLMDomainService"""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.container.service_registry import ServiceRegistry
from services.domain.llm_domain_service import LLMDomainService


class TestLLMDomainService:
    """Test LLM domain service"""

    @pytest.fixture
    def mock_config_service(self):
        """Mock LLMConfigService"""
        mock = Mock()
        mock.get_available_providers.return_value = ["openai", "gemini"]
        mock.get_configured_providers.return_value = ["openai", "gemini"]
        mock.get_default_provider.return_value = "openai"
        mock.get_api_key.return_value = "test-key"
        mock.validate_all_providers = AsyncMock(
            return_value={"openai": Mock(is_valid=True), "gemini": Mock(is_valid=True)}
        )
        return mock

    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM client"""
        mock = Mock()
        mock.complete = AsyncMock(return_value="test response")
        return mock

    async def test_initialization(self, mock_config_service, mock_llm_client):
        """Service initializes correctly"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(config_service=mock_config_service)

            assert not service.is_initialized()

            await service.initialize()

            assert service.is_initialized()
            mock_config_service.validate_all_providers.assert_called_once()

    async def test_complete_with_task_type(self, mock_config_service, mock_llm_client):
        """Complete uses task_type parameter"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(config_service=mock_config_service)
            await service.initialize()

            result = await service.complete(task_type="test_task", prompt="test prompt")

            assert result == "test response"
            # #1452: the pass-through gained system/user_id (per-user LLM rail)
            mock_llm_client.complete.assert_called_once_with(
                task_type="test_task",
                prompt="test prompt",
                context=None,
                response_format=None,
                system=None,
                user_id=None,
            )

    async def test_complete_with_context(self, mock_config_service, mock_llm_client):
        """Complete passes context to client"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(config_service=mock_config_service)
            await service.initialize()

            context = {"key": "value"}
            result = await service.complete(
                task_type="test_task", prompt="test prompt", context=context
            )

            assert result == "test response"
            mock_llm_client.complete.assert_called_once_with(
                task_type="test_task",
                prompt="test prompt",
                context=context,
                response_format=None,
                system=None,
                user_id=None,
            )

    async def test_complete_before_initialization(self):
        """Complete raises error if not initialized"""
        service = LLMDomainService()

        with pytest.raises(RuntimeError, match="not initialized"):
            await service.complete("test_task", "test")

    async def test_get_available_providers(self, mock_config_service, mock_llm_client):
        """Returns available providers"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(config_service=mock_config_service)
            await service.initialize()

            providers = service.get_available_providers()
            assert providers == ["openai", "gemini"]

    async def test_get_default_provider(self, mock_config_service, mock_llm_client):
        """Returns default provider"""
        with patch("services.llm.clients.llm_client", mock_llm_client):
            service = LLMDomainService(config_service=mock_config_service)
            await service.initialize()

            provider = service.get_default_provider()
            assert provider == "openai"

    async def test_get_providers_before_initialization(self):
        """Get providers raises error if not initialized"""
        service = LLMDomainService()

        with pytest.raises(RuntimeError, match="not initialized"):
            service.get_available_providers()

    async def test_complete_error_handling(self, mock_config_service):
        """Complete propagates errors from client"""
        error_client = Mock()
        error_client.complete = AsyncMock(side_effect=ValueError("Client error"))

        with patch("services.llm.clients.llm_client", error_client):
            service = LLMDomainService(config_service=mock_config_service)
            await service.initialize()

            with pytest.raises(ValueError, match="Client error"):
                await service.complete("test_task", "test")


class TestServiceRegistry:
    """Test ServiceRegistry (Phase 1.6: Updated to instance-based API)"""

    @pytest.fixture
    def registry(self):
        """Create fresh registry for each test"""
        reg = ServiceRegistry()
        yield reg
        reg.clear()

    def test_register_service(self, registry):
        """Can register service"""
        mock_service = Mock()
        registry.register("test", mock_service)

        assert registry.has("test")
        assert registry.get("test") == mock_service

    def test_get_unregistered_service(self, registry):
        """Raises error for unregistered service"""
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_register_allows_overwrite(self, registry):
        """Registry allows overwriting services (Phase 1.6 behavior)"""
        service1 = Mock()
        service2 = Mock()

        registry.register("test", service1)
        assert registry.get("test") == service1

        # New registry allows overwriting
        registry.register("test", service2)
        assert registry.get("test") == service2

    def test_list_services(self, registry):
        """Lists registered services"""
        registry.register("svc1", Mock())
        registry.register("svc2", Mock())

        services = registry.list_services()
        assert "svc1" in services
        assert "svc2" in services

    def test_clear_registry(self, registry):
        """Clear removes all services"""
        registry.register("test", Mock())
        assert registry.has("test")

        registry.clear()
        assert not registry.has("test")
