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
    CLAUDE_OPUS = "claude-3-opus-20240229"
    CLAUDE_SONNET = "claude-sonnet-4-20250514"

    # OpenAI models
    GPT4 = "gpt-4-turbo-preview"
    GPT35 = "gpt-3.5-turbo"


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
