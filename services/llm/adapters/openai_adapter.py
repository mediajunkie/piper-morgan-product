"""
OpenAI LLM Adapter

Wraps OpenAI SDK in Pattern-012 compliant interface for vendor-agnostic access.
Uses native OpenAI Python SDK for GPT models.

Pattern-012: LLM Adapter Pattern
See: docs/internal/architecture/current/patterns/pattern-012-llm-adapter.md
"""

from typing import List, Tuple, AsyncIterator, Dict, Any
import structlog
from openai import AsyncOpenAI

from .base import LLMAdapter, LLMResponse

logger = structlog.get_logger()


class OpenAIAdapter(LLMAdapter):
    """
    Adapter for OpenAI models (GPT-4, GPT-3.5).

    Provides Pattern-012 compliant interface on top of the OpenAI SDK.
    Supports GPT-4, GPT-4 Turbo, and GPT-3.5 Turbo models.

    Supported models:
        - gpt-4o (GPT-4 Turbo, 128K context)
        - gpt-4-1106-preview (GPT-4 Turbo with vision)
        - gpt-4 (Standard GPT-4, 8K context)
        - gpt-4-32k (GPT-4 with 32K context)
        - gpt-3.5-turbo (GPT-3.5 Turbo, 16K context)
        - gpt-3.5-turbo-16k (GPT-3.5 with 16K context)

    Features:
        - Streaming support
        - Function/tool calling
        - JSON mode (structured output)
        - Vision capabilities (GPT-4V models)
        - Up to 128K token context (Turbo models)

    Example:
        adapter = OpenAIAdapter(
            api_key="sk-...",
            model="gpt-4o"
        )
        response = await adapter.complete("Explain quantum computing")
        print(response.content)
    """

    def __init__(self, api_key: str, model: str = "gpt-4o", **kwargs):
        """
        Initialize OpenAI adapter.

        Args:
            api_key: OpenAI API key (starts with sk-)
            model: GPT model identifier
            **kwargs: Additional config (timeout, max_retries, organization, etc.)

        Raises:
            ValueError: If API key or model is invalid
        """
        super().__init__(api_key, model, **kwargs)

        # Initialize OpenAI async client
        self._client = AsyncOpenAI(
            api_key=api_key,
            timeout=kwargs.get("timeout", 60.0),
            max_retries=kwargs.get("max_retries", 2),
            organization=kwargs.get("organization"),
        )

        logger.info(
            "openai_adapter_initialized",
            model=model,
            timeout=kwargs.get("timeout", 60.0),
        )

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate completion using GPT.

        Args:
            prompt: Input prompt
            **kwargs:
                max_tokens: Max tokens to generate (default: 1000)
                temperature: Sampling temperature 0.0-2.0 (default: 0.7)
                top_p: Nucleus sampling (default: None)
                stop: List of stop sequences (default: None)
                response_format: {"type": "json_object"} for JSON mode
                frequency_penalty: -2.0 to 2.0 (default: 0)
                presence_penalty: -2.0 to 2.0 (default: 0)

        Returns:
            LLMResponse with completion

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            # Build messages
            messages = [{"role": "user", "content": prompt}]

            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
            }

            # Add optional parameters
            if kwargs.get("top_p") is not None:
                request_params["top_p"] = kwargs["top_p"]
            if kwargs.get("stop"):
                request_params["stop"] = kwargs["stop"]
            if kwargs.get("response_format"):
                request_params["response_format"] = kwargs["response_format"]
            if kwargs.get("frequency_penalty") is not None:
                request_params["frequency_penalty"] = kwargs["frequency_penalty"]
            if kwargs.get("presence_penalty") is not None:
                request_params["presence_penalty"] = kwargs["presence_penalty"]

            logger.debug("openai_api_request", model=self.model, prompt_length=len(prompt))

            # Make API call
            response = await self._client.chat.completions.create(**request_params)

            # Log usage
            logger.info(
                "openai_completion",
                model=self.model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                finish_reason=response.choices[0].finish_reason,
            )

            # Convert to standardized format
            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=self.model,
                provider="openai",
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "response_id": response.id,
                    "model_version": response.model,
                    "system_fingerprint": response.system_fingerprint,
                },
            )

        except Exception as e:
            logger.error("openai_completion_failed", error=str(e), model=self.model)
            raise RuntimeError(f"OpenAI API call failed: {str(e)}") from e

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """
        Classify text using GPT with confidence score.

        Args:
            text: Text to classify
            categories: List of possible categories

        Returns:
            Tuple of (category_name, confidence_score)

        Raises:
            ValueError: If text or categories empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        if not categories:
            raise ValueError("Categories list cannot be empty")

        prompt = f"""Classify the following text into exactly one of these categories: {', '.join(categories)}

Text to classify:
{text}

Respond with ONLY this format (no other text):
category_name:confidence_score

Where confidence_score is a number between 0.0 and 1.0.
Example: bug_report:0.92"""

        try:
            response = await self.complete(prompt, max_tokens=50, temperature=0.0)
            parts = response.content.strip().split(":")

            if len(parts) != 2:
                logger.warning(
                    "openai_classification_parse_failed",
                    response=response.content,
                    expected_format="category:score",
                )
                return categories[0], 0.1

            category = parts[0].strip()
            try:
                confidence = float(parts[1].strip())
                confidence = max(0.0, min(1.0, confidence))
            except ValueError:
                logger.warning("openai_confidence_parse_failed", confidence_str=parts[1])
                confidence = 0.5

            # Validate category
            if category not in categories:
                logger.warning(
                    "openai_invalid_category", category=category, valid_categories=categories
                )
                category = categories[0]
                confidence = 0.3

            return category, confidence

        except Exception as e:
            logger.error("openai_classification_failed", error=str(e))
            return categories[0], 0.0

    async def stream_complete(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """
        Stream completion from GPT in real-time.

        Args:
            prompt: Input prompt
            **kwargs: Same as complete() method

        Yields:
            Text chunks as they arrive

        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        try:
            messages = [{"role": "user", "content": prompt}]

            request_params = {
                "model": self.model,
                "messages": messages,
                "max_tokens": kwargs.get("max_tokens", 1000),
                "temperature": kwargs.get("temperature", 0.7),
                "stream": True,  # Enable streaming
            }

            # Add optional parameters
            if kwargs.get("top_p") is not None:
                request_params["top_p"] = kwargs["top_p"]
            if kwargs.get("stop"):
                request_params["stop"] = kwargs["stop"]

            logger.debug("openai_stream_request", model=self.model)

            # Stream the response
            stream = await self._client.chat.completions.create(**request_params)

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            logger.info("openai_stream_complete", model=self.model)

        except Exception as e:
            logger.error("openai_stream_failed", error=str(e))
            raise RuntimeError(f"OpenAI streaming failed: {str(e)}") from e

    def supports_streaming(self) -> bool:
        """OpenAI supports streaming responses."""
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        """
        Get GPT model capabilities.

        Returns:
            Dict with model metadata
        """
        # Determine capabilities based on model name
        model_lower = self.model.lower()

        if "gpt-4-turbo" in model_lower or "gpt-4-1106" in model_lower:
            max_tokens = 128000
            tier = "turbo"
            supports_vision = "vision" in model_lower or "1106" in model_lower
        elif "gpt-4-32k" in model_lower:
            max_tokens = 32000
            tier = "extended"
            supports_vision = False
        elif "gpt-4" in model_lower:
            max_tokens = 8192
            tier = "standard"
            supports_vision = False
        elif "gpt-3.5-turbo-16k" in model_lower:
            max_tokens = 16000
            tier = "extended"
            supports_vision = False
        elif "gpt-3.5" in model_lower:
            max_tokens = 16000  # Updated default for gpt-3.5-turbo
            tier = "turbo"
            supports_vision = False
        else:
            max_tokens = 8192
            tier = "unknown"
            supports_vision = False

        return {
            "provider": "openai",
            "model": self.model,
            "max_tokens": max_tokens,
            "supports_streaming": True,
            "supports_vision": supports_vision,
            "supports_function_calling": True,  # All GPT models support functions
            "supports_json_mode": True,  # JSON mode available
            "tier": tier,
            "context_window": max_tokens,
        }

    async def health_check(self) -> bool:
        """
        Verify OpenAI API connectivity.

        Returns:
            True if API is accessible
        """
        try:
            response = await self.complete("test", max_tokens=5, temperature=0.0)
            return len(response.content) > 0
        except Exception as e:
            logger.warning("openai_health_check_failed", error=str(e))
            return False
