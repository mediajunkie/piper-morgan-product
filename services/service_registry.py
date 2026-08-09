"""
Service Registry for Domain Services

Global registry pattern enabling dependency injection and
centralized service management across the application.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional

import structlog

if TYPE_CHECKING:
    # #1436: resolve the "LLMDomainService" forward ref for type checkers
    # (runtime import stays lazy — registry must not depend on domain services).
    from services.domain.llm_domain_service import LLMDomainService

logger = structlog.get_logger(__name__)


class ServiceRegistry:
    """
    Global service registry for domain services.

    Provides centralized access to domain services across
    web, CLI, Slack, and other consumers.

    Usage:
        # Register service at startup
        ServiceRegistry.register("llm", llm_service)

        # Access from any consumer
        llm = ServiceRegistry.get_llm()
    """

    _services: Dict[str, Any] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """
        Register a domain service

        Args:
            name: Service identifier (e.g., "llm", "github")
            service: Domain service instance

        Raises:
            ValueError: If service already registered
        """
        if name in cls._services:
            raise ValueError(f"Service '{name}' already registered")

        cls._services[name] = service
        logger.info(f"Service registered: {name}", service_type=type(service).__name__)

    @classmethod
    def get(cls, name: str) -> Any:
        """
        Get registered service

        Args:
            name: Service identifier

        Returns:
            Domain service instance

        Raises:
            RuntimeError: If service not registered
        """
        if name not in cls._services:
            raise RuntimeError(
                f"Service '{name}' not registered. "
                f"Available services: {list(cls._services.keys())}"
            )
        return cls._services[name]

    @classmethod
    def get_llm(cls) -> "LLMDomainService":
        """
        Convenience method for LLM service access

        Returns:
            LLMDomainService instance
        """
        return cls.get("llm")

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if service is registered"""
        return name in cls._services

    @classmethod
    def list_services(cls) -> list[str]:
        """Get list of registered service names"""
        return list(cls._services.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered services (for testing)"""
        cls._services.clear()
        cls._initialized = False

    @classmethod
    def mark_initialized(cls) -> None:
        """Mark registry as initialized"""
        cls._initialized = True

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if registry is initialized"""
        return cls._initialized
