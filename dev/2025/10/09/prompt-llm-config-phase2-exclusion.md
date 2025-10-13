# Phase 2 Implementation: Provider Exclusion & Selection Logic

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 2 of 4
**Agent**: Code Agent
**Estimated Time**: 2-3 hours
**Date**: October 9, 2025, 1:58 PM

---

## Mission

Implement provider exclusion and selection logic to stop burning Anthropic credits during development. Enable configuration-driven provider selection with intelligent fallbacks.

---

## Context from Phase 0 & Phase 1

**Current State**:
- ✅ LLMConfigService implemented with 4 providers validated
- ✅ All providers working (OpenAI, Anthropic, Gemini, Perplexity)
- ❌ 87.5% of LLM tasks use Anthropic (burning credits)
- ❌ No provider selection logic (hardcoded provider usage)

**Goal**:
- Exclude Anthropic during development
- Use OpenAI as primary provider
- Implement fallback chain
- Make it configurable per environment

---

## Phase 2 Goals

1. **Provider Exclusion**: Ability to exclude providers (e.g., exclude Anthropic)
2. **Default Provider**: Configure which provider to use by default
3. **Fallback Chain**: If primary fails, try next provider
4. **Environment-Aware**: Development vs production configurations
5. **Provider Selection**: Centralized logic for choosing provider

---

## Implementation Approach

### Part A: Configuration Schema (30 minutes)
### Part B: Provider Selection Service (60 minutes)
### Part C: Integration & Testing (30-60 minutes)

---

## Part A: Configuration Schema (30 minutes)

### A.1: Add Configuration to LLMConfigService

**File**: `services/config/llm_config_service.py`

Add provider selection configuration:

```python
from typing import List, Optional
from enum import Enum

class Environment(Enum):
    """Deployment environment"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LLMConfigService:
    def __init__(self):
        self._load_provider_configs()
        self._load_selection_config()  # New

    def _load_selection_config(self) -> None:
        """Load provider selection configuration from environment"""

        # Current environment
        self._environment = Environment(
            os.getenv("PIPER_ENVIRONMENT", "development")
        )

        # Excluded providers (comma-separated list)
        excluded = os.getenv("PIPER_EXCLUDED_PROVIDERS", "")
        self._excluded_providers = [
            p.strip() for p in excluded.split(",") if p.strip()
        ]

        # Default provider
        self._default_provider = os.getenv(
            "PIPER_DEFAULT_PROVIDER",
            "openai"  # Safe default
        )

        # Fallback chain (comma-separated, in priority order)
        fallback = os.getenv(
            "PIPER_FALLBACK_PROVIDERS",
            "openai,gemini,anthropic,perplexity"  # Default order
        )
        self._fallback_chain = [
            p.strip() for p in fallback.split(",") if p.strip()
        ]

    def get_available_providers(self) -> List[str]:
        """
        Return list of providers that are:
        1. Configured (have valid API keys)
        2. Not excluded
        3. Available in current environment
        """
        configured = self.get_configured_providers()

        # Filter out excluded providers
        available = [
            provider for provider in configured
            if provider not in self._excluded_providers
        ]

        return available

    def get_default_provider(self) -> str:
        """
        Get the default provider to use

        Returns the configured default if available,
        otherwise first available provider

        Raises:
            ValueError: If no providers available
        """
        available = self.get_available_providers()

        if not available:
            raise ValueError(
                "No LLM providers available. Check configuration."
            )

        # Use default if it's available
        if self._default_provider in available:
            return self._default_provider

        # Otherwise use first available
        return available[0]

    def get_provider_with_fallback(
        self,
        preferred: Optional[str] = None
    ) -> str:
        """
        Get provider with fallback logic

        Args:
            preferred: Preferred provider (optional)

        Returns:
            Provider name to use

        Logic:
        1. If preferred specified and available, use it
        2. Otherwise use default provider
        3. If default not available, use first in fallback chain
        """
        available = self.get_available_providers()

        if not available:
            raise ValueError("No LLM providers available")

        # Try preferred provider first
        if preferred and preferred in available:
            return preferred

        # Try default provider
        if self._default_provider in available:
            return self._default_provider

        # Try fallback chain in order
        for provider in self._fallback_chain:
            if provider in available:
                return provider

        # Last resort: first available
        return available[0]

    def is_provider_excluded(self, provider: str) -> bool:
        """Check if provider is excluded"""
        return provider in self._excluded_providers

    def get_environment(self) -> Environment:
        """Get current environment"""
        return self._environment
```

### A.2: Add Tests for Selection Logic

**File**: `tests/config/test_llm_config_service.py`

Add new test class:

```python
class TestProviderSelection:
    """Test provider selection and exclusion logic"""

    def test_exclude_provider(self):
        """Excluded provider not in available list"""
        with patch.dict(os.environ, {"PIPER_EXCLUDED_PROVIDERS": "anthropic"}):
            service = LLMConfigService()
            available = service.get_available_providers()
            assert "anthropic" not in available

    def test_exclude_multiple_providers(self):
        """Multiple excluded providers filtered out"""
        with patch.dict(os.environ, {
            "PIPER_EXCLUDED_PROVIDERS": "anthropic,gemini"
        }):
            service = LLMConfigService()
            available = service.get_available_providers()
            assert "anthropic" not in available
            assert "gemini" not in available

    def test_default_provider_selection(self):
        """Default provider is returned if available"""
        with patch.dict(os.environ, {"PIPER_DEFAULT_PROVIDER": "openai"}):
            service = LLMConfigService()
            default = service.get_default_provider()
            assert default == "openai"

    def test_default_provider_excluded_uses_fallback(self):
        """If default excluded, uses fallback"""
        with patch.dict(os.environ, {
            "PIPER_DEFAULT_PROVIDER": "anthropic",
            "PIPER_EXCLUDED_PROVIDERS": "anthropic",
            "PIPER_FALLBACK_PROVIDERS": "openai,gemini"
        }):
            service = LLMConfigService()
            provider = service.get_provider_with_fallback()
            assert provider in ["openai", "gemini"]
            assert provider != "anthropic"

    def test_preferred_provider_override(self):
        """Preferred provider overrides default"""
        service = LLMConfigService()
        provider = service.get_provider_with_fallback(preferred="gemini")
        assert provider == "gemini"

    def test_is_provider_excluded(self):
        """Can check if provider is excluded"""
        with patch.dict(os.environ, {"PIPER_EXCLUDED_PROVIDERS": "anthropic"}):
            service = LLMConfigService()
            assert service.is_provider_excluded("anthropic") is True
            assert service.is_provider_excluded("openai") is False
```

Run tests to ensure RED (not implemented yet):
```bash
python -m pytest tests/config/test_llm_config_service.py::TestProviderSelection -v
```

---

## Part B: Provider Selection Service (60 minutes)

### B.1: Create Provider Selection Service

**File**: `services/llm/provider_selector.py` (new file)

```python
"""
LLM Provider Selection Service

Handles intelligent provider selection with fallbacks,
exclusions, and environment-aware routing.
"""

from typing import Optional, List
import structlog
from services.config.llm_config_service import LLMConfigService

logger = structlog.get_logger(__name__)

class ProviderSelector:
    """
    Service for selecting appropriate LLM provider

    Usage:
        selector = ProviderSelector()
        provider = selector.select_provider(task_type="general")
    """

    def __init__(self, config_service: Optional[LLMConfigService] = None):
        """Initialize with config service"""
        self._config = config_service or LLMConfigService()

    def select_provider(
        self,
        task_type: Optional[str] = None,
        preferred: Optional[str] = None
    ) -> str:
        """
        Select appropriate provider for task

        Args:
            task_type: Type of task (general, coding, research)
            preferred: Explicitly preferred provider

        Returns:
            Provider name to use
        """

        # If preferred specified and available, use it
        if preferred:
            if self._is_available(preferred):
                logger.debug(f"Using preferred provider: {preferred}")
                return preferred
            else:
                logger.warning(
                    f"Preferred provider {preferred} not available, "
                    f"falling back"
                )

        # Task-specific routing
        if task_type:
            provider = self._select_for_task(task_type)
            if provider:
                return provider

        # Use default with fallback
        provider = self._config.get_provider_with_fallback(preferred)
        logger.debug(f"Selected provider: {provider}")
        return provider

    def _select_for_task(self, task_type: str) -> Optional[str]:
        """
        Select provider based on task type

        Task-specific preferences (cost-optimized):
        - general: OpenAI (cheap, reliable)
        - coding: OpenAI (good at code)
        - research: Gemini (good for search/research)
        """

        task_preferences = {
            "general": ["openai", "gemini", "anthropic"],
            "coding": ["openai", "anthropic", "gemini"],
            "research": ["gemini", "perplexity", "openai"],
        }

        preferences = task_preferences.get(task_type, [])
        available = self._config.get_available_providers()

        # Return first preferred provider that's available
        for provider in preferences:
            if provider in available:
                logger.debug(
                    f"Task {task_type}: selected {provider}"
                )
                return provider

        return None

    def _is_available(self, provider: str) -> bool:
        """Check if provider is available"""
        available = self._config.get_available_providers()
        return provider in available

    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return self._config.get_available_providers()
```

### B.2: Add Tests for Provider Selector

**File**: `tests/llm/test_provider_selector.py` (new file)

```python
"""Tests for ProviderSelector"""

import pytest
from unittest.mock import Mock, patch
from services.llm.provider_selector import ProviderSelector
from services.config.llm_config_service import LLMConfigService

class TestProviderSelector:
    """Test provider selection logic"""

    def test_select_with_preferred_provider(self):
        """Preferred provider is used if available"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai", "gemini"]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(preferred="gemini")

        assert provider == "gemini"

    def test_select_with_unavailable_preferred_provider(self):
        """Falls back if preferred not available"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = ["openai"]
        mock_config.get_provider_with_fallback.return_value = "openai"

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(preferred="anthropic")

        assert provider == "openai"

    def test_select_for_general_task(self):
        """General tasks use OpenAI (cheap)"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = [
            "openai", "gemini", "anthropic"
        ]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="general")

        assert provider == "openai"

    def test_select_for_research_task(self):
        """Research tasks prefer Gemini/Perplexity"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = [
            "gemini", "perplexity", "openai"
        ]

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider(task_type="research")

        assert provider in ["gemini", "perplexity"]

    def test_select_excludes_anthropic_in_dev(self):
        """Anthropic excluded during development"""
        mock_config = Mock(spec=LLMConfigService)
        mock_config.get_available_providers.return_value = [
            "openai", "gemini"  # Anthropic excluded
        ]
        mock_config.get_provider_with_fallback.return_value = "openai"

        selector = ProviderSelector(mock_config)
        provider = selector.select_provider()

        assert provider != "anthropic"
```

---

## Part C: Integration & Testing (30-60 minutes)

### C.1: Update Environment Configuration

**File**: `.env`

Add PM's development configuration:

```bash
# Environment
PIPER_ENVIRONMENT=development

# Provider Exclusion (exclude Anthropic during dev)
PIPER_EXCLUDED_PROVIDERS=anthropic

# Default Provider (use OpenAI as primary)
PIPER_DEFAULT_PROVIDER=openai

# Fallback Chain (priority order)
PIPER_FALLBACK_PROVIDERS=openai,gemini,perplexity
```

### C.2: Update Client Code to Use Provider Selection

**File**: `services/llm/clients.py`

Update to use provider selection:

```python
from services.llm.provider_selector import ProviderSelector

# Global selector
_provider_selector = ProviderSelector()

def get_llm_client(
    task_type: Optional[str] = None,
    preferred: Optional[str] = None
):
    """
    Get appropriate LLM client for task

    Args:
        task_type: Type of task (general, coding, research)
        preferred: Explicitly preferred provider

    Returns:
        Configured LLM client
    """
    provider = _provider_selector.select_provider(
        task_type=task_type,
        preferred=preferred
    )

    # Return appropriate client based on provider
    if provider == "openai":
        return openai_client
    elif provider == "anthropic":
        return anthropic_client
    elif provider == "gemini":
        return gemini_client
    elif provider == "perplexity":
        return perplexity_client
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

### C.3: Update Startup Validation

**File**: `web/app.py`

Update startup validation to show exclusions:

```python
@app.on_event("startup")
async def validate_llm_configuration():
    """Validate LLM API keys at startup"""
    logger.info("Validating LLM configuration...")

    config_service = LLMConfigService()

    # Show environment
    env = config_service.get_environment()
    logger.info(f"Environment: {env.value}")

    # Show exclusions
    all_configured = config_service.get_configured_providers()
    available = config_service.get_available_providers()
    excluded = set(all_configured) - set(available)

    if excluded:
        logger.info(f"Excluded providers: {', '.join(excluded)}")

    # Show default
    default = config_service.get_default_provider()
    logger.info(f"Default provider: {default}")

    # Validate
    results = await config_service.validate_all_providers()
    # ... rest of validation ...
```

---

## Acceptance Criteria

- [ ] Provider exclusion configuration working
- [ ] Default provider configuration working
- [ ] Fallback chain implemented
- [ ] ProviderSelector service implemented
- [ ] All new tests passing
- [ ] Startup shows exclusion status
- [ ] PM's .env configured to exclude Anthropic
- [ ] OpenAI used as primary provider
- [ ] Anthropic NOT used during development

---

## Testing Validation

```bash
# Run all config tests
python -m pytest tests/config/test_llm_config_service.py -v

# Run provider selector tests
python -m pytest tests/llm/test_provider_selector.py -v

# Start server and check logs
python main.py
# Expected logs:
# Environment: development
# Excluded providers: anthropic
# Default provider: openai
# ✅ openai: Valid
# ⚠️ anthropic: Excluded
```

---

## Success Metrics

After Phase 2:
- ✅ Anthropic credit burn stopped
- ✅ Development uses OpenAI (cheaper)
- ✅ Configurable provider selection
- ✅ Intelligent fallbacks
- ✅ All tests passing

---

## Time Breakdown

- Part A (Config): 30 minutes
- Part B (Selector): 60 minutes
- Part C (Integration): 30-60 minutes
**Total**: 2-3 hours

---

**This stops the credit burn and gives us intelligent provider routing!**
