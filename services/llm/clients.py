"""
LLM Client implementations
Handles connections to Anthropic and OpenAI

Uses LLMConfigService for secure key management and validation.
"""

from typing import Any, Dict, Optional

import openai
import structlog
from anthropic import Anthropic

from services.config.llm_config_service import LLMConfigService

from .config import MODEL_CONFIGS, LLMModel, LLMProvider

logger = structlog.get_logger()


class LLMClient:
    """Base LLM client with common interface"""

    def __init__(self):
        self.anthropic_client = None
        self.openai_client = None
        self._config_service = LLMConfigService()
        self._init_clients()

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
                openai.api_key = openai_key
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            except ValueError as e:
                logger.warning(f"OpenAI client initialization skipped: {e}")
        else:
            logger.warning("No OPENAI_API_KEY configured")

    async def complete(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Get completion for a specific task type with automatic fallback

        Args:
            task_type: Type of task (intent_classification, reasoning, etc)
            prompt: The prompt to send
            context: Optional context to include

        Returns:
            The LLM's response
        """
        config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
        primary_provider = config["provider"]

        # Try primary provider first
        try:
            if primary_provider == LLMProvider.ANTHROPIC:
                return await self._anthropic_complete(prompt, config, response_format)
            elif primary_provider == LLMProvider.OPENAI:
                return await self._openai_complete(prompt, config, response_format)
            else:
                raise ValueError(f"Unknown provider: {primary_provider}")
        except Exception as e:
            # Log the primary provider failure
            logger.warning(f"Primary provider {primary_provider.value} failed: {str(e)}")

            # Determine fallback provider
            fallback_provider = (
                LLMProvider.OPENAI
                if primary_provider == LLMProvider.ANTHROPIC
                else LLMProvider.ANTHROPIC
            )
            fallback_config = {**config, "provider": fallback_provider}

            # Adjust model for fallback provider
            if fallback_provider == LLMProvider.OPENAI:
                fallback_config["model"] = LLMModel.GPT4
            else:
                fallback_config["model"] = LLMModel.CLAUDE_SONNET

            logger.info(f"Falling back to {fallback_provider.value}")

            try:
                if fallback_provider == LLMProvider.ANTHROPIC:
                    return await self._anthropic_complete(prompt, fallback_config, response_format)
                else:
                    return await self._openai_complete(prompt, fallback_config, response_format)
            except Exception as fallback_error:
                logger.error(
                    f"Fallback provider {fallback_provider.value} also failed: {str(fallback_error)}"
                )
                raise RuntimeError(
                    f"Both LLM providers failed. Primary: {str(e)}, Fallback: {str(fallback_error)}"
                )

    async def _anthropic_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Get completion from Anthropic"""
        if not self.anthropic_client:
            raise RuntimeError("Anthropic client not initialized")

        # Note: Anthropic doesn't support response_format like OpenAI
        # JSON mode must be handled via prompt engineering
        response = self.anthropic_client.messages.create(
            model=config["model"].value,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            messages=[{"role": "user", "content": prompt}],
        )
        # Log approximate tokens/cost
        logger.info(
            "llm_usage",
            provider="anthropic",
            tokens_sent=len(prompt) // 4,
            tokens_received=len(response.content[0].text) // 4,
        )
        return response.content[0].text

    async def _openai_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Get completion from OpenAI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")

        # Prepare request parameters
        request_params = {
            "model": config["model"].value,
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"],
            "messages": [{"role": "user", "content": prompt}],
        }

        # Add response_format if provided (for JSON mode)
        if response_format:
            request_params["response_format"] = response_format

        response = self.openai_client.chat.completions.create(**request_params)
        # Log approximate tokens/cost
        logger.info(
            "llm_usage",
            provider="openai",
            tokens_sent=len(prompt) // 4,
            tokens_received=len(response.choices[0].message.content) // 4,
        )
        return response.choices[0].message.content


# Global client instance
llm_client = LLMClient()
