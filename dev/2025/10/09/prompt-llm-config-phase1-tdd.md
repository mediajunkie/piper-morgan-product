# Phase 1 Implementation: LLMConfigService with Validation (TDD)

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 1 of 4
**Agent**: Code Agent
**Approach**: Test-Driven Development
**Estimated Time**: 3-4 hours
**Date**: October 9, 2025, 12:26 PM

---

## Mission

Build LLMConfigService that loads and validates LLM API keys from environment variables. Use TDD approach: write tests first, then implement.

---

## Context from Phase 0

**Current State**:
- Keys stored in plaintext `.env` file
- No validation at startup (late runtime errors)
- 87.5% of tasks use Anthropic (burning credits)
- Clean singleton architecture (easy to update)

**Available Keys** (in `.env`):
- `ANTHROPIC_API_KEY` ✅
- `OPENAI_API_KEY` ✅
- `GEMINI_API_KEY` ✅
- `PERPLEXITY_API_KEY` ✅

---

## Phase 1 Goals

1. **LLMConfigService**: Central service for LLM configuration
2. **Validation**: Test each key at startup with real API call
3. **Clear Errors**: Tell user exactly what's wrong
4. **Foundation**: Enable Phase 2 (provider exclusion)

---

## Implementation Approach: TDD

### Part A: Write Tests First (45 minutes)
### Part B: Implement Service (2 hours)
### Part C: Integration (45 minutes)

---

## Part A: Write Tests First (TDD)

**File**: `tests/config/test_llm_config_service.py`

### Test Suite Structure

```python
"""
Tests for LLMConfigService - Written BEFORE implementation (TDD)
"""
import pytest
import os
from unittest.mock import patch, MagicMock
from services.config.llm_config_service import LLMConfigService, ProviderConfig

class TestLLMConfigServiceInit:
    """Test service initialization"""

    def test_service_loads_from_environment(self):
        """Service loads all available keys from environment"""
        # Test will pass when service reads from os.environ
        pass

    def test_service_handles_missing_env_vars(self):
        """Service handles missing environment variables gracefully"""
        # Test will pass when service doesn't crash on missing keys
        pass

class TestProviderValidation:
    """Test individual provider validation"""

    @pytest.mark.asyncio
    async def test_validate_openai_key_success(self):
        """Valid OpenAI key passes validation"""
        # Make real API call to validate key
        pass

    @pytest.mark.asyncio
    async def test_validate_openai_key_invalid(self):
        """Invalid OpenAI key fails validation with clear error"""
        pass

    @pytest.mark.asyncio
    async def test_validate_anthropic_key_success(self):
        """Valid Anthropic key passes validation"""
        pass

    @pytest.mark.asyncio
    async def test_validate_gemini_key_success(self):
        """Valid Gemini key passes validation"""
        pass

    @pytest.mark.asyncio
    async def test_validate_perplexity_key_success(self):
        """Valid Perplexity key passes validation"""
        pass

class TestProviderConfiguration:
    """Test provider configuration loading"""

    def test_get_configured_providers(self):
        """Returns list of providers with valid keys"""
        pass

    def test_get_provider_config(self):
        """Returns config for specific provider"""
        pass

    def test_get_missing_provider_raises_error(self):
        """Requesting unconfigured provider raises clear error"""
        pass

class TestStartupValidation:
    """Test startup validation behavior"""

    @pytest.mark.asyncio
    async def test_validate_all_configured_providers(self):
        """Validates all configured providers at startup"""
        pass

    @pytest.mark.asyncio
    async def test_validation_failure_provides_clear_error(self):
        """Failed validation gives actionable error message"""
        pass

    @pytest.mark.asyncio
    async def test_validation_handles_network_errors(self):
        """Network errors during validation handled gracefully"""
        pass

class TestErrorMessages:
    """Test error message quality"""

    def test_missing_key_error_message(self):
        """Missing key error tells user exactly what to do"""
        # Should say: "OPENAI_API_KEY not found in environment. Add to .env file."
        pass

    def test_invalid_key_error_message(self):
        """Invalid key error is clear and actionable"""
        # Should say: "OPENAI_API_KEY is invalid. Received 401 Unauthorized."
        pass
```

### Test Implementation Instructions

**Write actual test code** for each test above. Tests should:
1. **Use real API calls** for validation (not mocks) - We want to know keys actually work
2. **Use mocks for error cases** - Don't need real failed API calls
3. **Have clear assertions** - Specific expected behavior
4. **Be independent** - Each test stands alone

**Example of a complete test**:
```python
@pytest.mark.asyncio
async def test_validate_openai_key_success(self):
    """Valid OpenAI key passes validation"""
    service = LLMConfigService()

    # This should make a real API call to OpenAI
    result = await service.validate_provider("openai")

    assert result.is_valid is True
    assert result.provider == "openai"
    assert result.error_message is None
```

**Run tests after writing** (they should all fail - RED phase):
```bash
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py -v
# Expected: All tests FAIL (service doesn't exist yet)
```

---

## Part B: Implement LLMConfigService (2 hours)

**File**: `services/config/llm_config_service.py`

### Service Architecture

```python
"""
LLM Configuration Service - Secure key management and validation

Responsibilities:
- Load API keys from environment variables
- Validate keys with real API calls
- Provide clear error messages
- Foundation for provider selection/exclusion
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import os
import asyncio
from enum import Enum

@dataclass
class ValidationResult:
    """Result of provider key validation"""
    provider: str
    is_valid: bool
    error_message: Optional[str] = None
    error_code: Optional[str] = None

@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider"""
    name: str
    env_var: str
    api_key: Optional[str]
    validation_endpoint: str
    required: bool = False

class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    PERPLEXITY = "perplexity"

class LLMConfigService:
    """
    Central service for LLM configuration management

    Usage:
        service = LLMConfigService()
        await service.validate_all_providers()

        # Get provider API key
        openai_key = service.get_api_key("openai")
    """

    def __init__(self):
        """Initialize service and load configuration from environment"""
        self._load_provider_configs()

    def _load_provider_configs(self) -> None:
        """Load provider configurations from environment variables"""
        # Define provider configurations
        self._providers: Dict[str, ProviderConfig] = {
            "openai": ProviderConfig(
                name="openai",
                env_var="OPENAI_API_KEY",
                api_key=os.getenv("OPENAI_API_KEY"),
                validation_endpoint="https://api.openai.com/v1/models",
                required=True,  # OpenAI is required
            ),
            "anthropic": ProviderConfig(
                name="anthropic",
                env_var="ANTHROPIC_API_KEY",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                validation_endpoint="https://api.anthropic.com/v1/messages",
                required=False,
            ),
            "gemini": ProviderConfig(
                name="gemini",
                env_var="GEMINI_API_KEY",
                api_key=os.getenv("GEMINI_API_KEY"),
                validation_endpoint="https://generativelanguage.googleapis.com/v1/models",
                required=False,
            ),
            "perplexity": ProviderConfig(
                name="perplexity",
                env_var="PERPLEXITY_API_KEY",
                api_key=os.getenv("PERPLEXITY_API_KEY"),
                validation_endpoint="https://api.perplexity.ai/chat/completions",
                required=False,
            ),
        }

    def get_configured_providers(self) -> List[str]:
        """Return list of providers with API keys configured"""
        return [
            name for name, config in self._providers.items()
            if config.api_key is not None
        ]

    def get_api_key(self, provider: str) -> str:
        """
        Get API key for provider

        Raises:
            ValueError: If provider not configured
        """
        if provider not in self._providers:
            raise ValueError(f"Unknown provider: {provider}")

        config = self._providers[provider]
        if config.api_key is None:
            raise ValueError(
                f"{config.env_var} not found in environment. "
                f"Add to .env file or set environment variable."
            )

        return config.api_key

    async def validate_provider(self, provider: str) -> ValidationResult:
        """
        Validate provider API key with real API call

        Makes lightweight API call to verify key works.
        """
        if provider not in self._providers:
            return ValidationResult(
                provider=provider,
                is_valid=False,
                error_message=f"Unknown provider: {provider}",
            )

        config = self._providers[provider]

        if config.api_key is None:
            return ValidationResult(
                provider=provider,
                is_valid=False,
                error_message=f"{config.env_var} not set in environment",
            )

        # Validate with provider-specific logic
        if provider == "openai":
            return await self._validate_openai(config)
        elif provider == "anthropic":
            return await self._validate_anthropic(config)
        elif provider == "gemini":
            return await self._validate_gemini(config)
        elif provider == "perplexity":
            return await self._validate_perplexity(config)

        return ValidationResult(
            provider=provider,
            is_valid=False,
            error_message=f"No validation implemented for {provider}",
        )

    async def _validate_openai(self, config: ProviderConfig) -> ValidationResult:
        """Validate OpenAI API key"""
        # TODO: Implement OpenAI validation
        # Make GET request to https://api.openai.com/v1/models
        # Check for 200 OK or 401 Unauthorized
        pass

    async def _validate_anthropic(self, config: ProviderConfig) -> ValidationResult:
        """Validate Anthropic API key"""
        # TODO: Implement Anthropic validation
        pass

    async def _validate_gemini(self, config: ProviderConfig) -> ValidationResult:
        """Validate Gemini API key"""
        # TODO: Implement Gemini validation
        pass

    async def _validate_perplexity(self, config: ProviderConfig) -> ValidationResult:
        """Validate Perplexity API key"""
        # TODO: Implement Perplexity validation
        pass

    async def validate_all_providers(self) -> Dict[str, ValidationResult]:
        """
        Validate all configured providers

        Returns dict of provider -> ValidationResult
        Logs results and raises if required provider fails
        """
        configured = self.get_configured_providers()

        # Validate all providers concurrently
        tasks = [
            self.validate_provider(provider)
            for provider in configured
        ]
        results = await asyncio.gather(*tasks)

        # Create results dict
        validation_results = {
            result.provider: result
            for result in results
        }

        # Log results
        for provider, result in validation_results.items():
            if result.is_valid:
                print(f"✅ {provider}: Valid")
            else:
                print(f"❌ {provider}: {result.error_message}")

        # Check required providers
        for provider, config in self._providers.items():
            if config.required and provider in validation_results:
                result = validation_results[provider]
                if not result.is_valid:
                    raise ValueError(
                        f"Required provider {provider} validation failed: "
                        f"{result.error_message}"
                    )

        return validation_results
```

### Implementation Instructions

1. **Complete the TODO sections** in validation methods
2. **Use httpx or requests** for API calls
3. **Handle errors gracefully** (network, timeouts, auth failures)
4. **Log clearly** what's happening
5. **Make tests pass** (GREEN phase)

**Provider-specific validation hints**:
- **OpenAI**: GET `/v1/models` with Authorization header
- **Anthropic**: POST `/v1/messages` with minimal request
- **Gemini**: GET `/v1/models` with API key param
- **Perplexity**: POST `/chat/completions` with minimal request

**Run tests during development**:
```bash
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py -v
# Watch tests turn from RED → GREEN
```

---

## Part C: Integration (45 minutes)

### Update Client Initialization

**File**: `services/llm/clients.py` (or wherever clients are initialized)

**Changes needed**:
1. Import `LLMConfigService`
2. Use service to get API keys instead of direct env vars
3. Add startup validation call

**Example update**:
```python
# Before
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# After
from services.config.llm_config_service import LLMConfigService

config_service = LLMConfigService()
openai_client = OpenAI(api_key=config_service.get_api_key("openai"))
```

### Add Startup Validation

**File**: `main.py`

Add validation call at startup:
```python
from services.config.llm_config_service import LLMConfigService

@app.on_event("startup")
async def validate_llm_configuration():
    """Validate LLM API keys at startup"""
    config_service = LLMConfigService()
    await config_service.validate_all_providers()
```

---

## Acceptance Criteria

- [ ] `LLMConfigService` class implemented
- [ ] All tests pass (GREEN)
- [ ] Each provider has validation logic
- [ ] Startup validation works
- [ ] Clear error messages for missing/invalid keys
- [ ] Client initialization updated to use service
- [ ] No plaintext keys in code (only in `.env`)

---

## Testing Validation

```bash
# Run all LLM config tests
PYTHONPATH=. python -m pytest tests/config/test_llm_config_service.py -v

# Start server (should validate at startup)
PYTHONPATH=. python main.py
# Expected: See validation messages for each provider

# Test with invalid key (temporarily break one)
# Expected: Clear error message, server refuses to start
```

---

## STOP Conditions

- If API validation is too complex for any provider
- If real API calls in tests are problematic
- If startup validation blocks development workflow
- If error messages aren't clear enough

Document and escalate if any STOP condition hit.

---

## Subagent Usage

**Use subagents for**:
- Writing provider-specific validation logic (4 subagents, one per provider)
- Writing test suites (can parallelize)
- Updating client initialization code (separate concern)

**Example subagent task**:
```
Subagent Task: Implement OpenAI validation
- Function: _validate_openai()
- Make GET request to https://api.openai.com/v1/models
- Check for 200 (valid) or 401 (invalid)
- Return ValidationResult with clear error messages
- Handle network errors gracefully
```

---

## Time Breakdown

- **Part A** (Tests): 45 minutes
- **Part B** (Service): 2 hours
  - Core service: 45 min
  - Validation logic (4 providers): 60 min
  - Error handling: 15 min
- **Part C** (Integration): 45 minutes
  - Update clients: 30 min
  - Startup validation: 15 min

**Total**: 3-4 hours

---

**TDD Red → Green → Refactor cycle. Take time to do it right.**
