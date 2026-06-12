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


class LLMModel(Enum):
    # Anthropic models
    CLAUDE_OPUS = "claude-opus-4-8"
    CLAUDE_SONNET = "claude-sonnet-4-6"

    # OpenAI models
    GPT4 = "gpt-4o"
    GPT35 = "gpt-4o-mini"

    # Google Gemini models (wired Apr 16 per #950-adjacent provider diversification)
    GEMINI_FLASH = "gemini-2.5-flash"
    GEMINI_PRO = "gemini-2.5-pro"


# Issue #1126 (2026-05-27): Models that don't accept the `temperature` parameter.
# Anthropic deprecated `temperature` for extended-thinking models like
# claude-opus-4-8 — passing it returns HTTP 400 ("temperature is deprecated
# for this model"). LLMClient checks this set at request-build time and
# omits `temperature` from the payload when the target model is listed here.
#
# When adding new models to LLMModel above: if the model accepts temperature,
# do nothing here. If it doesn't, add the model-id string to this set.
MODELS_WITHOUT_TEMPERATURE: set[str] = {
    "claude-opus-4-8",  # Extended-thinking model; temperature deprecated
}


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
    # Issue #1004 Fix B: Semantic boundary detector — JSON classification only.
    # Low temperature for deterministic classification; small max_tokens since
    # output is the SemanticDetectorOutput envelope (~150 tokens worst case).
    "boundary_detection": {
        "model_tier": "default",
        "temperature": 0.2,
        "max_tokens": 400,
    },
    # Issue #1126 (2026-05-27): Slot extraction — JSON extraction of structured
    # slot values from natural-language user messages. Use default-tier model
    # (Sonnet) — the task is structured extraction, not deep reasoning. Low
    # temperature for deterministic output. Previously fell through to
    # "reasoning" default which routed to CLAUDE_OPUS (heavy tier), which
    # doesn't accept temperature, which is why #1121's slot-extraction live
    # smoke failed today.
    "slot_extraction": {
        "model_tier": "default",
        "temperature": 0.2,
        "max_tokens": 800,
    },
}


# Map deprecated model IDs to current equivalents (PA proposal, Lead-approved
# 2026-06-12). Update ONE entry here when Anthropic deprecates a model —
# downstream code/config/env passing a deprecated ID resolves gracefully
# instead of hard-erroring. Resolution logs a warning so stale IDs stay findable.
MODEL_ALIASES: Dict[str, str] = {
    "claude-sonnet-4-20250514": "claude-sonnet-4-6",
    "claude-opus-4-7": "claude-opus-4-8",
}


def resolve_model_alias(model_id: str) -> str:
    """Translate a deprecated model ID to its current equivalent.

    Logs on alias HIT — silent resolution forever is how stale IDs linger
    (#1193 doc/behavior-honesty principle); the warning makes them findable
    without breaking anyone.
    """
    resolved = MODEL_ALIASES.get(model_id, model_id)
    if resolved != model_id:
        import structlog

        structlog.get_logger().warning(
            "model_alias_resolved", from_id=model_id, to_id=resolved
        )
    return resolved


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
