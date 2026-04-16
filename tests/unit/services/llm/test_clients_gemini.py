"""
Tests for Gemini integration in LLMClient.

Scope: verify Gemini is a real primary/fallback provider, not a stub.
Paired with config changes in services/llm/config.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------
# Client initialization
# ---------------------------------------------------------------------


class TestGeminiClientInit:
    def test_gemini_client_initialized_when_configured(self):
        """LLMClient initializes a gemini_client when the config service reports gemini configured."""
        from services.llm.clients import LLMClient

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["gemini"]
            mock_config.get_api_key.return_value = "test-gemini-key"

            with patch("google.generativeai.configure") as mock_configure:
                client = LLMClient()

        assert (
            client.gemini_client is not None
        ), "Gemini client should be initialized when configured"
        mock_configure.assert_called_with(api_key="test-gemini-key")

    def test_gemini_client_none_when_not_configured(self):
        """LLMClient leaves gemini_client as None when gemini is absent from configured providers."""
        from services.llm.clients import LLMClient

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["anthropic"]
            mock_config.get_api_key.return_value = "test-anthropic-key"

            client = LLMClient()

        assert client.gemini_client is None

    def test_providers_initialized_includes_gemini(self):
        """providers_initialized returns True when only Gemini is configured."""
        from services.llm.clients import LLMClient

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["gemini"]
            mock_config.get_api_key.return_value = "test-gemini-key"

            with patch("google.generativeai.configure"):
                client = LLMClient()

        assert client.providers_initialized is True


# ---------------------------------------------------------------------
# Gemini completion
# ---------------------------------------------------------------------


class TestGeminiComplete:
    @pytest.mark.asyncio
    async def test_gemini_complete_success(self):
        """_gemini_complete returns text from the response."""
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["gemini"]
            mock_config.get_api_key.return_value = "test-key"

            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel") as mock_model_cls:
                    mock_response = MagicMock()
                    mock_response.text = "I'm Piper."
                    mock_response.usage_metadata = MagicMock(
                        prompt_token_count=42, candidates_token_count=8
                    )

                    mock_model = mock_model_cls.return_value
                    mock_model.generate_content_async = AsyncMock(return_value=mock_response)

                    client = LLMClient()
                    # Mark gemini_client as truthy so the method proceeds
                    client.gemini_client = True

                    config = {
                        "provider": LLMProvider.GEMINI,
                        "model": LLMModel.GEMINI_FLASH,
                        "max_tokens": 1000,
                        "temperature": 0.7,
                    }
                    result = await client._gemini_complete(
                        prompt="who are you?",
                        config=config,
                        system=None,
                    )

        assert result == "I'm Piper."

    @pytest.mark.asyncio
    async def test_gemini_complete_with_system_prompt(self):
        """System prompt is passed as system_instruction to GenerativeModel."""
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["gemini"]
            mock_config.get_api_key.return_value = "test-key"

            with patch("google.generativeai.configure"):
                with patch("google.generativeai.GenerativeModel") as mock_model_cls:
                    mock_response = MagicMock()
                    mock_response.text = "ok"
                    mock_response.usage_metadata = MagicMock(
                        prompt_token_count=1, candidates_token_count=1
                    )
                    mock_model_cls.return_value.generate_content_async = AsyncMock(
                        return_value=mock_response
                    )

                    client = LLMClient()
                    client.gemini_client = True

                    config = {
                        "provider": LLMProvider.GEMINI,
                        "model": LLMModel.GEMINI_FLASH,
                        "max_tokens": 1000,
                        "temperature": 0.7,
                    }
                    await client._gemini_complete(
                        prompt="hi",
                        config=config,
                        system="You are Piper.",
                    )

        # Verify GenerativeModel was constructed with system_instruction
        call_args = mock_model_cls.call_args
        assert call_args.kwargs.get("system_instruction") == "You are Piper." or (
            len(call_args.args) > 1 and call_args.args[1] == "You are Piper."
        ), f"Expected system_instruction='You are Piper.' in {call_args}"

    @pytest.mark.asyncio
    async def test_gemini_complete_raises_when_not_initialized(self):
        """Unconfigured Gemini raises RuntimeError instead of crashing obscurely."""
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["anthropic"]
            mock_config.get_api_key.return_value = "test-key"

            client = LLMClient()
            # gemini_client should be None
            assert client.gemini_client is None

            config = {
                "provider": LLMProvider.GEMINI,
                "model": LLMModel.GEMINI_FLASH,
                "max_tokens": 1000,
                "temperature": 0.7,
            }

            with pytest.raises(RuntimeError, match="Gemini client not initialized"):
                await client._gemini_complete(prompt="hi", config=config, system=None)


# ---------------------------------------------------------------------
# Dispatch routing
# ---------------------------------------------------------------------


class TestCallProviderDispatch:
    @pytest.mark.asyncio
    async def test_call_provider_routes_gemini(self):
        """_call_provider dispatches GEMINI to _gemini_complete."""
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config = mock_config_cls.return_value
            mock_config.get_configured_providers.return_value = ["gemini"]
            mock_config.get_api_key.return_value = "test-key"

            with patch("google.generativeai.configure"):
                client = LLMClient()

        config = {
            "provider": LLMProvider.GEMINI,
            "model": LLMModel.GEMINI_FLASH,
            "max_tokens": 1000,
            "temperature": 0.7,
        }

        with patch.object(
            client, "_gemini_complete", AsyncMock(return_value="gemini-response")
        ) as mock_gemini:
            result = await client._call_provider(
                LLMProvider.GEMINI, "prompt", config, None, None, None
            )

        assert result == "gemini-response"
        mock_gemini.assert_called_once()


# ---------------------------------------------------------------------
# Config (LLMModel + PROVIDER_MODELS)
# ---------------------------------------------------------------------


class TestGeminiConfig:
    def test_gemini_models_defined(self):
        """LLMModel enum includes Gemini model identifiers."""
        from services.llm.config import LLMModel

        assert hasattr(LLMModel, "GEMINI_FLASH"), "LLMModel.GEMINI_FLASH should be defined"
        assert hasattr(LLMModel, "GEMINI_PRO"), "LLMModel.GEMINI_PRO should be defined"

    def test_provider_models_has_gemini(self):
        """PROVIDER_MODELS includes gemini entries for default + heavy tiers."""
        from services.llm.config import PROVIDER_MODELS, LLMModel

        assert "gemini" in PROVIDER_MODELS
        assert PROVIDER_MODELS["gemini"]["default"] == LLMModel.GEMINI_FLASH
        assert PROVIDER_MODELS["gemini"]["heavy"] == LLMModel.GEMINI_PRO

    def test_resolve_model_for_gemini(self):
        """resolve_model returns the right Gemini model for a task type."""
        from services.llm.config import LLMModel, LLMProvider, resolve_model

        result = resolve_model(LLMProvider.GEMINI, "conversation")
        assert result == LLMModel.GEMINI_FLASH  # default tier

        result = resolve_model(LLMProvider.GEMINI, "reasoning")
        assert result == LLMModel.GEMINI_PRO  # heavy tier
