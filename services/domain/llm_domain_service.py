"""
LLM Domain Service

Domain service mediating all LLM access following DDD principles.
Provides clean interface for LLM operations across all consumers.

# #971: Adapters, LLMFactory, ProviderSelector deleted per Architect decision (Apr 14)
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.analytics.api_usage_tracker import APIUsageTracker
from services.config.llm_config_service import LLMConfigService

logger = structlog.get_logger(__name__)


class LLMDomainService:
    """
    Domain service for LLM operations

    Mediates all LLM access following Domain-Driven Design principles.
    This is THE ONLY way to access LLM providers in the system.

    Usage:
        # Access via ServiceRegistry
        llm = ServiceRegistry.get_llm()

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
        self._usage_tracker = APIUsageTracker()  # Issue #271: Cost tracking

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
            )

            # Issue #271: Log usage if session available
            if session and context:
                await self._log_usage(
                    session=session,
                    task_type=task_type,
                    prompt=prompt,
                    response_text=response,
                    context=context,
                )

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

    async def _log_usage(
        self,
        session: AsyncSession,
        task_type: str,
        prompt: str,
        response_text: str,
        context: Dict[str, Any],
    ) -> None:
        """
        Log LLM API usage for cost tracking (Issue #271)

        Non-blocking: Errors in logging don't interrupt the response.

        Args:
            session: Database session for logging
            task_type: Type of task completed
            prompt: Input prompt sent to LLM
            response_text: Response received from LLM
            context: Context dictionary with user_id, provider, model info
        """
        try:
            # Extract context information
            user_id = context.get("user_id", "unknown")
            conversation_id = context.get("conversation_id")
            feature = context.get("feature", task_type)
            request_id = context.get("request_id")

            # Determine provider and model from context or config
            provider = context.get("provider", "anthropic")
            model = context.get("model", "claude-3-sonnet")

            # Prepare request/response data for logging
            request_data = {
                "conversation_id": conversation_id,
                "feature": feature,
                "request_id": request_id,
                "task_type": task_type,
                "prompt_length": len(prompt),
            }

            response_data = {
                "response_time_ms": context.get("response_time_ms"),
                "response_length": len(response_text),
                "usage": {
                    # Approximate token counts (will be replaced with actual counts when LLMClient returns them)
                    "prompt_tokens": len(prompt) // 4,
                    "completion_tokens": len(response_text) // 4,
                    "total_tokens": (len(prompt) + len(response_text)) // 4,
                },
            }

            # Log the API call
            await self._usage_tracker.log_api_call(
                session=session,
                user_id=user_id,
                provider=provider,
                model=model,
                request_data=request_data,
                response_data=response_data,
            )

            logger.debug(f"Usage logged for {user_id}: {provider}/{model}")

        except Exception as e:
            # Non-blocking: Log error but don't interrupt request
            logger.warning(f"Failed to log usage: {e}")
