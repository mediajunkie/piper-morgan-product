"""
LLM Domain Service

Domain service mediating all LLM access following DDD principles.
Provides clean interface for LLM operations across all consumers.
"""

from decimal import Decimal
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from services.analytics.api_usage_tracker import APIUsageTracker
from services.config.llm_config_service import LLMConfigService
from services.llm.adapters import LLMAdapter, LLMFactory, LLMResponse
from services.llm.config import LLMProvider
from services.llm.provider_selector import ProviderSelector

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
        provider_selector: Optional[ProviderSelector] = None,
    ):
        """
        Initialize LLM domain service

        Args:
            config_service: Optional LLMConfigService for testing
            provider_selector: Optional ProviderSelector for testing
        """
        self._config_service = config_service
        self._provider_selector = provider_selector
        self._llm_client = None
        self._adapters: Dict[LLMProvider, LLMAdapter] = {}  # Pattern-012 adapters
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

            # Initialize provider selector
            if not self._provider_selector:
                self._provider_selector = ProviderSelector(self._config_service)

            # Initialize LLM client (legacy)
            self._initialize_client()

            # Initialize Pattern-012 adapters
            self._initialize_adapters()

            self._initialized = True
            logger.info("LLM domain service initialized successfully")
            logger.info(f"Adapters available: {list(self._adapters.keys())}")

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

    def _initialize_adapters(self) -> None:
        """
        Initialize Pattern-012 adapters for all configured providers.

        Creates adapter instances for each provider that has valid configuration.
        Adapters are cached in self._adapters for reuse.
        """
        logger.info("Initializing Pattern-012 LLM adapters...")

        # Get all configured providers
        configured_providers = self._config_service.get_configured_providers()

        # Map provider names to enums
        provider_map = {
            "anthropic": LLMProvider.ANTHROPIC,
            "openai": LLMProvider.OPENAI,
            "gemini": LLMProvider.GEMINI,
            "perplexity": LLMProvider.PERPLEXITY,
        }

        adapter_count = 0

        for provider_name in configured_providers:
            if provider_name not in provider_map:
                logger.warning(
                    f"Provider {provider_name} not supported in adapter pattern, skipping"
                )
                continue

            provider_enum = provider_map[provider_name]

            try:
                # Get API key and default model for provider
                api_key = self._config_service.get_api_key(provider_name)

                # #947: Get default model from unified config (single source of truth)
                from services.llm.config import get_default_model_for_provider

                model = get_default_model_for_provider(provider_name)

                # Create adapter using factory
                adapter = LLMFactory.create(provider=provider_enum, api_key=api_key, model=model)

                self._adapters[provider_enum] = adapter
                adapter_count += 1

                logger.info(
                    "adapter_initialized",
                    provider=provider_name,
                    model=model,
                    adapter_type=adapter.__class__.__name__,
                )

            except Exception as e:
                logger.warning(f"Failed to initialize {provider_name} adapter: {e}")

        logger.info(
            f"Pattern-012 adapters initialized: {adapter_count}/{len(configured_providers)}"
        )

    async def complete_with_adapter(
        self, provider: LLMProvider, prompt: str, **kwargs
    ) -> LLMResponse:
        """
        Generate completion using specific adapter (Pattern-012).

        This is the NEW Pattern-012 interface for direct provider access.
        Provides more control than task_type-based routing.

        Args:
            provider: Which provider to use (ANTHROPIC, OPENAI, GEMINI, PERPLEXITY)
            prompt: Input prompt
            **kwargs: Provider-specific options (max_tokens, temperature, etc.)

        Returns:
            LLMResponse with standardized format

        Raises:
            RuntimeError: If service not initialized
            ValueError: If provider not configured

        Example:
            # Use Claude
            response = await llm.complete_with_adapter(
                provider=LLMProvider.ANTHROPIC,
                prompt="Explain quantum computing",
                max_tokens=500,
                temperature=0.7
            )

            # Use Gemini
            response = await llm.complete_with_adapter(
                provider=LLMProvider.GEMINI,
                prompt="Summarize this document",
                max_tokens=200
            )
        """
        if not self._initialized:
            raise RuntimeError("LLMDomainService not initialized. Call initialize() first.")

        if provider not in self._adapters:
            available = ", ".join(p.value for p in self._adapters.keys())
            raise ValueError(
                f"Provider {provider.value} not configured. " f"Available: {available}"
            )

        adapter = self._adapters[provider]

        logger.info(
            "adapter_completion_requested",
            provider=provider.value,
            adapter_type=adapter.__class__.__name__,
            prompt_length=len(prompt),
        )

        try:
            response = await adapter.complete(prompt, **kwargs)

            logger.info(
                "adapter_completion_success",
                provider=provider.value,
                response_length=len(response.content),
                tokens=response.usage.get("total_tokens", 0),
            )

            return response

        except Exception as e:
            logger.error(
                "adapter_completion_failed",
                provider=provider.value,
                error=str(e),
            )
            raise

    def get_adapter(self, provider: LLMProvider) -> Optional[LLMAdapter]:
        """
        Get adapter instance for provider.

        Useful for advanced operations like streaming or classification.

        Args:
            provider: Provider enum

        Returns:
            LLMAdapter instance or None if not configured

        Example:
            adapter = llm.get_adapter(LLMProvider.ANTHROPIC)
            if adapter:
                async for chunk in adapter.stream_complete("Tell a story"):
                    print(chunk, end='')
        """
        return self._adapters.get(provider)

    def list_adapters(self) -> List[LLMProvider]:
        """
        List available adapters.

        Returns:
            List of configured provider enums
        """
        return list(self._adapters.keys())

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
