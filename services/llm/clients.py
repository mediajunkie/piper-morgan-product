"""
LLM Client implementations
Handles connections to Anthropic, OpenAI, and Gemini.

Uses LLMConfigService for secure key management and validation.
"""

from typing import Any, Dict, Optional

import structlog
from anthropic import Anthropic
from openai import OpenAI

from services.analytics.api_usage_tracker import APIUsageTracker
from services.config.llm_config_service import LLMConfigService

from .config import MODEL_CONFIGS, PROVIDER_MODELS, LLMModel, LLMProvider, resolve_model

logger = structlog.get_logger()

# Fallback preference order — tried in sequence if the primary provider fails.
# Anthropic first (project default), Gemini second (added Apr 16), OpenAI last.
_FALLBACK_ORDER = [LLMProvider.ANTHROPIC, LLMProvider.GEMINI, LLMProvider.OPENAI]


class LLMClient:
    """Base LLM client with common interface"""

    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        self.gemini_client = (
            None  # Gemini uses a per-call GenerativeModel; this flag tracks "configured"
        )
        self._config_service = LLMConfigService()
        self.usage_tracker = APIUsageTracker()
        self._init_clients()

    @property
    def providers_initialized(self) -> bool:
        """Check if at least one LLM provider is initialized and available"""
        return (
            self.anthropic_client is not None
            or self.openai_client is not None
            or self.gemini_client is not None
        )

    def _init_clients(self):
        """Initialize API clients using LLMConfigService"""
        # Get configured providers from config service
        configured_providers = self._config_service.get_configured_providers()

        # Anthropic
        if "anthropic" in configured_providers:
            try:
                anthropic_key = self._config_service.get_api_key("anthropic")
                self.anthropic_client = Anthropic(api_key=anthropic_key)
                logger.info("Anthropic client initialized")
            except ValueError as e:
                logger.warning(f"Anthropic client initialization skipped: {e}")
        else:
            logger.warning("No ANTHROPIC_API_KEY configured")

        # OpenAI
        if "openai" in configured_providers:
            try:
                openai_key = self._config_service.get_api_key("openai")
                self.openai_client = OpenAI(api_key=openai_key)
                logger.info("OpenAI client initialized")
            except ValueError as e:
                logger.warning(f"OpenAI client initialization skipped: {e}")
        else:
            logger.warning("No OPENAI_API_KEY configured")

        # Gemini (added Apr 16, #950-adjacent)
        if "gemini" in configured_providers:
            try:
                import google.generativeai as genai

                gemini_key = self._config_service.get_api_key("gemini")
                genai.configure(api_key=gemini_key)
                # Gemini uses a per-call GenerativeModel rather than a stateless client.
                # We set this flag to True to signal "configured"; actual model instances
                # are constructed inside _gemini_complete as needed (cheap, supports
                # per-call system_instruction).
                self.gemini_client = True
                logger.info("Gemini client initialized")
            except (ValueError, ImportError) as e:
                logger.warning(f"Gemini client initialization skipped: {e}")
        else:
            logger.warning("No GEMINI_API_KEY configured")

    async def complete(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """
        Get completion for a specific task type with automatic fallback

        Args:
            task_type: Type of task (intent_classification, reasoning, etc)
            prompt: The prompt to send
            context: Optional context to include
            response_format: Optional response format (for JSON mode)
            system: Optional system prompt

        Returns:
            The LLM's response
        """
        task_config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])

        # Resolve primary provider: user's setup choice first (#946)
        try:
            # Check user's explicit setup choice stored in keychain
            from services.infrastructure.keychain_service import KeychainService

            user_choice = KeychainService().get_api_key("default_llm_provider")
            if user_choice:
                primary_provider = LLMProvider(user_choice)
            else:
                default_provider_name = self._config_service.get_default_provider()
                primary_provider = LLMProvider(default_provider_name)
        except (ValueError, Exception):
            # Fall back to whichever client is initialized
            if self.anthropic_client:
                primary_provider = LLMProvider.ANTHROPIC
            elif self.gemini_client:
                primary_provider = LLMProvider.GEMINI
            elif self.openai_client:
                primary_provider = LLMProvider.OPENAI
            else:
                raise RuntimeError("No LLM providers configured. Add an API key in Settings.")

        # Build runtime config with correct model for this provider
        config = {
            **task_config,
            "provider": primary_provider,
            "model": resolve_model(primary_provider, task_type),
        }

        # Try primary provider first
        try:
            return await self._call_provider(
                primary_provider, prompt, config, response_format, context, system
            )
        except Exception as e:
            logger.warning(
                "llm_primary_failed",
                provider=primary_provider.value,
                task_type=task_type,
                error=str(e),
            )

            # Try each other configured provider in the fallback order (Apr 16: Gemini added)
            fallback_errors: list[str] = [f"{primary_provider.value}: {e}"]
            for fallback_provider in _FALLBACK_ORDER:
                if fallback_provider == primary_provider:
                    continue
                if not self._is_provider_configured(fallback_provider):
                    continue

                fallback_config = {
                    **task_config,
                    "provider": fallback_provider,
                    "model": resolve_model(fallback_provider, task_type),
                }

                logger.info(f"Falling back to {fallback_provider.value}")

                try:
                    return await self._call_provider(
                        fallback_provider,
                        prompt,
                        fallback_config,
                        response_format,
                        context,
                        system,
                    )
                except Exception as fallback_error:
                    logger.warning(
                        f"Fallback provider {fallback_provider.value} failed: {fallback_error}"
                    )
                    fallback_errors.append(f"{fallback_provider.value}: {fallback_error}")
                    continue

            # No fallback succeeded
            logger.error(f"All LLM providers failed: {fallback_errors}")
            raise RuntimeError(
                f"All configured LLM providers failed. Details: {'; '.join(fallback_errors)}"
            )

    def _is_provider_configured(self, provider: LLMProvider) -> bool:
        """Return True if the given provider has a live client / configured flag."""
        if provider == LLMProvider.ANTHROPIC:
            return self.anthropic_client is not None
        if provider == LLMProvider.OPENAI:
            return self.openai_client is not None
        if provider == LLMProvider.GEMINI:
            return bool(self.gemini_client)
        return False

    async def _call_provider(
        self,
        provider: LLMProvider,
        prompt: str,
        config: Dict[str, Any],
        response_format=None,
        context=None,
        system=None,
    ) -> str:
        """Route to the appropriate provider's completion method."""
        if provider == LLMProvider.ANTHROPIC:
            return await self._anthropic_complete(prompt, config, response_format, context, system)
        elif provider == LLMProvider.OPENAI:
            return await self._openai_complete(prompt, config, response_format, context, system)
        elif provider == LLMProvider.GEMINI:
            return await self._gemini_complete(prompt, config, response_format, context, system)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _anthropic_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from Anthropic"""
        if not self.anthropic_client:
            raise RuntimeError("Anthropic client not initialized")

        # Build request parameters
        request_params = {
            "model": config["model"].value,
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
            "messages": [{"role": "user", "content": prompt}],
        }

        # Add system prompt if provided
        if system:
            request_params["system"] = system

        # Note: Anthropic doesn't support response_format like OpenAI
        # JSON mode must be handled via prompt engineering
        response = self.anthropic_client.messages.create(**request_params)

        # Extract actual token counts from response
        prompt_tokens = (
            response.usage.input_tokens if hasattr(response, "usage") else len(prompt) // 4
        )
        completion_tokens = (
            response.usage.output_tokens
            if hasattr(response, "usage")
            else len(response.content[0].text) // 4
        )

        # Log usage - non-blocking
        try:
            # Note: We don't have DB session here in synchronous context
            # Usage tracking will need to be handled at a higher level with DB session
            logger.info(
                "llm_usage",
                provider="anthropic",
                model=config["model"].value,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.content[0].text

    async def _openai_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from OpenAI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")

        # Build messages list
        messages = []

        # Add system message if provided
        if system:
            messages.append({"role": "system", "content": system})

        # Add user message
        messages.append({"role": "user", "content": prompt})

        # Prepare request parameters
        request_params = {
            "model": config["model"].value,
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
            "messages": messages,
        }

        # Add response_format if provided (for JSON mode)
        if response_format:
            request_params["response_format"] = response_format

        response = self.openai_client.chat.completions.create(**request_params)

        # Extract actual token counts from response
        prompt_tokens = (
            response.usage.prompt_tokens if hasattr(response, "usage") else len(prompt) // 4
        )
        completion_tokens = (
            response.usage.completion_tokens
            if hasattr(response, "usage")
            else len(response.choices[0].message.content) // 4
        )

        # Log usage - non-blocking
        try:
            # Note: We don't have DB session here in synchronous context
            # Usage tracking will need to be handled at a higher level with DB session
            logger.info(
                "llm_usage",
                provider="openai",
                model=config["model"].value,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.choices[0].message.content

    async def _gemini_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from Google Gemini.

        Constructs a per-call GenerativeModel so that system_instruction can vary
        per request (Gemini 1.5+ sets system_instruction at model-init time rather
        than per-call). Object creation is cheap relative to the HTTP round trip.

        response_format handling (#988): when the caller passes
        {"type": "json_object"} (matching OpenAI's convention), Gemini's
        response_mime_type is set to 'application/json' so the model returns
        structured JSON rather than prose. Without this, Gemini often returns
        natural-language text where the classifier expects JSON, causing
        downstream ValueError on parse.
        """
        if not self.gemini_client:
            raise RuntimeError("Gemini client not initialized")

        import google.generativeai as genai

        model_name = config["model"].value
        model_kwargs: Dict[str, Any] = {"model_name": model_name}
        if system:
            model_kwargs["system_instruction"] = system

        model = genai.GenerativeModel(**model_kwargs)

        # #988: translate OpenAI-convention response_format to Gemini's native flag
        gen_config_kwargs: Dict[str, Any] = {
            "max_output_tokens": config["max_tokens"],
            "temperature": config["temperature"],
        }
        if response_format and response_format.get("type") == "json_object":
            gen_config_kwargs["response_mime_type"] = "application/json"

        generation_config = genai.types.GenerationConfig(**gen_config_kwargs)

        response = await model.generate_content_async(
            prompt,
            generation_config=generation_config,
        )

        # Extract token counts from usage_metadata if available
        try:
            prompt_tokens = response.usage_metadata.prompt_token_count
            completion_tokens = response.usage_metadata.candidates_token_count
        except AttributeError:
            prompt_tokens = len(prompt) // 4
            completion_tokens = len(response.text) // 4 if hasattr(response, "text") else 0

        try:
            logger.info(
                "llm_usage",
                provider="gemini",
                model=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.text


# Global client instance
llm_client = LLMClient()
