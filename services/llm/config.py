"""
LLM Configuration
Central place for model selection and settings
"""

from enum import Enum
from typing import Any, Dict


class LLMProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"


class LLMModel(Enum):
    # Anthropic models
    CLAUDE_OPUS = "claude-sonnet-4-20250514"  # Use Sonnet 4 as "heavy" tier until Opus 4 available
    CLAUDE_SONNET = "claude-sonnet-4-20250514"

    # OpenAI models
    GPT4 = "gpt-4o"
    GPT35 = "gpt-4o-mini"

    # Google Gemini models (wired Apr 16 per #950-adjacent provider diversification)
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"


# Per-provider model preferences for each task type.
# The provider is NOT specified here — it's determined at runtime from user config.
# Issue #940: Removed hardcoded provider assignments that caused UAT failures
# when the pinned provider was unavailable.
PROVIDER_MODELS: Dict[str, Dict[str, LLMModel]] = {
    "anthropic": {
        "default": LLMModel.CLAUDE_SONNET,
        "heavy": LLMModel.CLAUDE_OPUS,
    },
    "openai": {
        "default": LLMModel.GPT4,
        "heavy": LLMModel.GPT4,
    },
    "gemini": {
        "default": LLMModel.GEMINI_FLASH,
        "heavy": LLMModel.GEMINI_PRO,
    },
}

# Task configurations — provider-agnostic.
# "model_tier" selects from PROVIDER_MODELS: "default" or "heavy".
MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "intent_classification": {
        "model_tier": "default",
        "temperature": 0.3,
        "max_tokens": 500,
    },
    "reasoning": {
        "model_tier": "heavy",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    "code_generation": {
        "model_tier": "default",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
    "github_content_generation": {
        "model_tier": "heavy",
        "temperature": 0.7,
        "max_tokens": 3000,
    },
    # Issue #907: Conversational floor — contextual LLM responses for unmatched queries
    "conversation": {
        "model_tier": "default",
        "temperature": 0.7,
        "max_tokens": 1000,
    },
}


def resolve_model(provider: LLMProvider, task_type: str) -> LLMModel:
    """Resolve the appropriate model for a provider + task type combination."""
    config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
    tier = config.get("model_tier", "default")
    provider_models = PROVIDER_MODELS.get(provider.value, PROVIDER_MODELS["openai"])
    return provider_models.get(tier, provider_models["default"])


def get_default_model_for_provider(provider_name: str) -> str:
    """Get the default model ID string for a provider.

    #947: Single source of truth for model defaults, used by both LLMClient
    (via resolve_model) and LLMDomainService adapter initialization.
    Eliminates hardcoded model strings that drift out of sync.
    """
    provider_models = PROVIDER_MODELS.get(provider_name, PROVIDER_MODELS.get("openai", {}))
    model_enum = provider_models.get("default")
    if model_enum and hasattr(model_enum, "value"):
        return model_enum.value
    return "gpt-4o"  # safe fallback
