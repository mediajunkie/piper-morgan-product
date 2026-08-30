"""
LLM Domain Service

Domain service mediating all LLM access following DDD principles.
Provides clean interface for LLM operations across all consumers.

# #971: Adapters, LLMFactory, ProviderSelector deleted per Architect decision (Apr 14)
"""

from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.config.llm_config_service import LLMConfigService

logger = structlog.get_logger(__name__)


class LLMDomainService:
    """
    Domain service for LLM operations

    Mediates all LLM access following Domain-Driven Design principles.
    This is THE ONLY way to access LLM providers in the system.

    Usage:
        # Access via the service container's registry (services/container/):
        # ServiceInitializer registers the instance under "llm" at startup.
        llm = container._registry.get("llm")

        # Generate completion
        response = await llm.complete(
            task_type="general",
            prompt="Hello"
        )
    """

    def __init__(
        self,
        config_service: Optional[LLMConfigService] = None,
    ):
        """
        Initialize LLM domain service

        Args:
            config_service: Optional LLMConfigService for testing
        """
        self._config_service = config_service
        self._llm_client = None
        self._initialized = False
        # #935 (May 9 2026): _usage_tracker removed. APIUsageTracker was wired
        # in but the call chain was unreachable in production — callers don't
        # pass a session. Cost tracking is a beta-readiness concern that we'll
        # re-design with concrete scope when actually needed.

    async def initialize(self) -> None:
        """
        Initialize service (called from main.py at startup)

        Validates all providers and initializes clients.
        Must be called before any LLM operations.

        Raises:
            RuntimeError: If initialization fails
        """
        try:
            logger.info("Initializing LLM domain service...")

            # Initialize config service if not provided
            if not self._config_service:
                self._config_service = LLMConfigService()

            # Validate all providers
            logger.info("Validating LLM providers...")
            validation_results = await self._config_service.validate_all_providers()

            # Log validation results
            for provider, result in validation_results.items():
                if result.is_valid:
                    logger.info(f"✅ {provider}: Valid")
                else:
                    logger.warning(f"⚠️ {provider}: {result.error_message}")

            # Count valid providers
            valid_count = sum(1 for r in validation_results.values() if r.is_valid)
            logger.info(f"LLM providers validated: {valid_count}/{len(validation_results)}")

            # Initialize LLM client
            self._initialize_client()

            self._initialized = True
            logger.info("LLM domain service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM domain service: {e}")
            raise RuntimeError(f"LLM domain service initialization failed: {e}")

    def _initialize_client(self) -> None:
        """Initialize LLM client"""
        try:
            # Import global llm_client instance
            from services.llm.clients import llm_client

            self._llm_client = llm_client
            logger.info("LLM client initialized")

        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise

    async def complete(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        session: Optional[AsyncSession] = None,
        system: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> str:
        """
        Generate LLM completion

        Domain-level operation for LLM text generation.
        Delegates to underlying LLM client with proper error handling.

        Args:
            task_type: Type of task (intent_classification, reasoning, etc)
            prompt: Input prompt for generation
            context: Optional context to include
            response_format: Optional response format specification
            session: Optional database session for usage logging (Issue #271)
            system: Optional system prompt (Issue #381)
            user_id: Acting principal — threads to per-user provider
                selection (#1415). Optional for legacy callers; without it,
                selection resolves the server/global chain.

        Returns:
            Generated text response

        Raises:
            RuntimeError: If service not initialized
            Exception: If LLM completion fails
        """
        if not self._initialized:
            raise RuntimeError(
                "LLMDomainService not initialized. " "Call initialize() before using."
            )

        logger.info("Generating LLM completion", task_type=task_type)

        try:
            # Delegate to LLM client
            response = await self._llm_client.complete(
                task_type=task_type,
                prompt=prompt,
                context=context,
                response_format=response_format,
                system=system,
                user_id=user_id,  # #1415: identity reaches provider selection
            )

            # #935 (May 9 2026): #271 cost-tracking call removed. The original
            # `if session and context: await self._log_usage(...)` was never
            # reached in production — neither caller (lens_inference.py:275 or
            # slot_extractor.py:50) passed a session. APIUsageTracker deleted.

            return response

        except Exception as e:
            logger.error(f"LLM completion failed", task_type=task_type, error=str(e))
            raise

    def get_available_providers(self) -> List[str]:
        """
        Get list of available providers

        Returns:
            List of provider names
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_available_providers()

    def get_default_provider(self) -> str:
        """
        Get default provider

        Returns:
            Default provider name
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_default_provider()

    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized
