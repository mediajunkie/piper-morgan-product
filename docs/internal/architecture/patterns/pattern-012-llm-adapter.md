# Pattern-012: LLM Adapter Pattern

## Status

**Proven**

## Context

Applications using Large Language Models face vendor lock-in and switching costs when tightly coupled to specific LLM providers. Different providers have varying APIs, capabilities, and pricing models, making it difficult to switch or compare providers. The LLM Adapter Pattern addresses:

- What challenges does this solve? Abstracts LLM provider differences behind a common interface to enable provider switching
- When should this pattern be considered? When building applications that need flexibility in LLM provider selection
- What are the typical scenarios where this applies? Multi-provider support, A/B testing, fallback mechanisms, cost optimization

## Pattern Description

The LLM Adapter Pattern creates a common interface for all LLM providers, allowing applications to switch between providers without code changes and enabling capabilities like fallback, cost optimization, and performance comparison.

Core concept:
- Common interface abstracts provider differences
- Provider-specific adapters handle implementation details
- Factory pattern creates appropriate adapters
- Configuration-driven provider selection

## Implementation

### Core Adapter Interface

```python
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any

class LLMAdapter(ABC):
    """Common interface for all LLM providers"""

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        """Generate text completion"""
        pass

    @abstractmethod
    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        """Classify text into categories with confidence"""
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        pass

    @abstractmethod
    def supports_streaming(self) -> bool:
        """Check if provider supports streaming responses"""
        pass

    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """Get model capabilities and limits"""
        pass
```

### Provider-Specific Implementations

```python
class ClaudeAdapter(LLMAdapter):
    """Claude-specific implementation"""

    def __init__(self, api_key: str, model: str = "claude-3-opus"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def complete(self, prompt: str, **kwargs) -> str:
        response = await self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.content[0].text

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        prompt = f"""
        Classify this text into one of these categories: {', '.join(categories)}
        Text: {text}

        Return format: category_name:confidence_score
        """
        response = await self.complete(prompt)
        parts = response.split(':')
        return parts[0].strip(), float(parts[1].strip())

    async def embed(self, text: str) -> List[float]:
        # Claude doesn't provide embeddings, use alternative or raise NotImplementedError
        raise NotImplementedError("Claude doesn't support embeddings")

    def supports_streaming(self) -> bool:
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "anthropic",
            "model": self.model,
            "max_tokens": 100000,
            "supports_streaming": True,
            "supports_embeddings": False
        }

class OpenAIAdapter(LLMAdapter):
    """OpenAI-specific implementation"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def complete(self, prompt: str, **kwargs) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000),
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.choices[0].message.content

    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        # Similar implementation with OpenAI format
        pass

    async def embed(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    def supports_streaming(self) -> bool:
        return True

    async def get_model_info(self) -> Dict[str, Any]:
        return {
            "provider": "openai",
            "model": self.model,
            "max_tokens": 8192,
            "supports_streaming": True,
            "supports_embeddings": True
        }
```

### Adapter Factory

```python
class LLMFactory:
    """Creates appropriate adapter based on configuration"""

    _adapters: Dict[str, type] = {
        "claude": ClaudeAdapter,
        "openai": OpenAIAdapter,
        "local": LocalLLMAdapter,
        "azure": AzureOpenAIAdapter
    }

    @classmethod
    def create(cls, provider: str, **kwargs) -> LLMAdapter:
        """Create adapter for specified provider"""
        if provider not in cls._adapters:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls._adapters.keys())}")

        adapter_class = cls._adapters[provider]
        return adapter_class(**kwargs)

    @classmethod
    def register_adapter(cls, provider: str, adapter_class: type):
        """Register custom adapter"""
        cls._adapters[provider] = adapter_class

    @classmethod
    def list_providers(cls) -> List[str]:
        """List available providers"""
        return list(cls._adapters.keys())
```

### Multi-Provider Manager

```python
class LLMManager:
    """Manages multiple providers with fallback and load balancing"""

    def __init__(self, config: Dict[str, Dict]):
        self.adapters = {}
        self.primary_provider = None
        self.fallback_providers = []

        for provider, provider_config in config.items():
            adapter = LLMFactory.create(provider, **provider_config)
            self.adapters[provider] = adapter

            if provider_config.get("primary", False):
                self.primary_provider = provider
            if provider_config.get("fallback", False):
                self.fallback_providers.append(provider)

    async def complete(self, prompt: str, **kwargs) -> str:
        """Try primary provider, fallback on failure"""
        providers_to_try = [self.primary_provider] + self.fallback_providers

        for provider in providers_to_try:
            try:
                adapter = self.adapters[provider]
                return await adapter.complete(prompt, **kwargs)
            except Exception as e:
                logger.warning(f"Provider {provider} failed: {e}")
                continue

        raise LLMProviderError("All providers failed")

    async def compare_providers(self, prompt: str) -> Dict[str, str]:
        """Compare responses from all providers"""
        results = {}
        for provider, adapter in self.adapters.items():
            try:
                response = await adapter.complete(prompt)
                results[provider] = response
            except Exception as e:
                results[provider] = f"Error: {e}"
        return results
```

## Usage Guidelines

### Interface Design
- Define provider-agnostic interfaces that capture common capabilities
- Handle provider-specific features through optional methods or capability flags
- Use async interfaces for all operations to support various client patterns
- Include error handling and capability detection in interface

### Configuration Management
- Use configuration files or environment variables for provider selection
- Support runtime provider switching for testing and fallback
- Include provider-specific settings (models, tokens, endpoints)
- Validate configuration at startup

### Error Handling
- Implement graceful fallback between providers
- Log provider failures for monitoring and debugging
- Handle rate limiting and quota exhaustion
- Distinguish between temporary and permanent failures

## Benefits

- Provider independence and reduced vendor lock-in
- Easy A/B testing and performance comparison
- Fallback mechanisms for reliability
- Cost optimization through provider switching
- Simplified provider migration

## Trade-offs

- Additional abstraction layer complexity
- Lowest common denominator of features
- Potential performance overhead
- Need to maintain multiple provider credentials

## Anti-patterns to Avoid

- ❌ Exposing provider-specific features in common interface
- ❌ Tight coupling to specific provider APIs
- ❌ No fallback mechanisms for provider failures
- ❌ Ignoring provider-specific capabilities and limits

## Related Patterns

- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Factory creates appropriate adapters
- [Pattern-018: Configuration Access Pattern](pattern-018-configuration-access.md) - Provider configuration management
- [Pattern-014: Error Handling Pattern](pattern-014-error-handling-api-contract.md) - Provider error handling

## References

- **Implementation**: LLM provider abstraction layers
- **Usage Example**: Claude, OpenAI, local model adapters
- **Related Concepts**: Provider abstraction, API gateway pattern

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#12-adapter-pattern-for-llm-providers` - Complete implementation with factory and multi-provider management
- Codebase analysis - Provider abstraction patterns and configuration management
