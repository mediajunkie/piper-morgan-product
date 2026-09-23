"""
Tests for Gemini's place in LLMClient after #1812 steps 5–6.

HISTORY. This file used to pin Gemini SERVING mechanics (client init,
system_instruction, #988 JSON mode) under the designated-operator binding — the
only credential Gemini could ever spend, because `google.generativeai` configures
credentials process-globally and so has no safe per-request client path (#1819).
#1812 step 5 deleted the operator seam, which deleted Gemini's only spend path;
step 6 amputated `_init_clients` (no server clients exist to initialize). The
serving code and these tests went with it — git has both. Resurrect them only
alongside a SAFE per-request Gemini credential path, which the SDK does not offer.

What remains true, and pinned here: the dispatch table still routes GEMINI (so a
future leg needs no router change), the leg refuses honestly (the refusal pins
live in test_provider_request_key_1819.py), and the model config stays coherent.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------
# The leg is a pure, honest refusal (summary pin; full set in the 1819 file)
# ---------------------------------------------------------------------


class TestGeminiLegRefuses:
    @pytest.mark.asyncio
    async def test_gemini_complete_refuses_unbound(self):
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider
        from services.llm.request_key import UnboundLLMKeyError

        client = LLMClient.__new__(LLMClient)
        client._output_filter = None
        config = {
            "provider": LLMProvider.GEMINI,
            "model": LLMModel.GEMINI_FLASH,
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        with pytest.raises(UnboundLLMKeyError):
            await client._gemini_complete(prompt="hi", config=config, system=None)


# ---------------------------------------------------------------------
# Dispatch routing (unchanged by #1812 — a future safe leg slots back in here)
# ---------------------------------------------------------------------


class TestCallProviderDispatch:
    @pytest.mark.asyncio
    async def test_call_provider_routes_gemini(self):
        """_call_provider dispatches GEMINI to _gemini_complete."""
        from services.llm.clients import LLMClient
        from services.llm.config import LLMModel, LLMProvider

        with patch("services.llm.clients.LLMConfigService") as mock_config_cls:
            mock_config_cls.return_value = MagicMock()
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
