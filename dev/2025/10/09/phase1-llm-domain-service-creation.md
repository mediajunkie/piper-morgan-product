# Phase 1: LLM Domain Service Creation

**Issue**: #217 - CORE-LLM-CONFIG (Refactoring)
**Phase**: 1 of 3 - Domain Service Creation
**Agent**: Code Agent
**Date**: October 9, 2025, 5:24 PM
**Time Estimate**: 2-3 hours

---

## Mission

Create LLMDomainService and ServiceRegistry following existing domain service patterns. Enable ALL consumers (web, CLI, Slack) to access LLM through proper DDD architecture.

---

## Context from Phase 0

**Critical Discovery**: 11 existing domain services with proven patterns!

**Patterns to Follow**:
- `services/domain/github_domain_service.py` - Structure
- `services/domain/user_preference_manager.py` - Initialization
- `tests/domain/test_user_preference_manager.py` - Test pattern

**Infrastructure Found**:
- main.py line 102: Perfect initialization spot
- 13 active LLM consumers need to be updated
- tests/domain/ ready for new tests

---

## Phase 1 Tasks

### Task 1: Create ServiceRegistry (30 min)

**File**: `services/service_registry.py` (NEW)

**Purpose**: Global registry for domain services (singleton pattern)

**Implementation**:
```python
"""
Service Registry for Domain Services

Global registry pattern enabling dependency injection and
centralized service management across the application.
"""

from typing import Any, Dict, Optional
import structlog

logger = structlog.get_logger(__name__)

class ServiceRegistry:
    """
    Global service registry for domain services.

    Provides centralized access to domain services across
    web, CLI, Slack, and other consumers.

    Usage:
        # Register service at startup
        ServiceRegistry.register("llm", llm_service)

        # Access from any consumer
        llm = ServiceRegistry.get_llm()
    """

    _services: Dict[str, Any] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, name: str, service: Any) -> None:
        """
        Register a domain service

        Args:
            name: Service identifier (e.g., "llm", "github")
            service: Domain service instance

        Raises:
            ValueError: If service already registered
        """
        if name in cls._services:
            raise ValueError(f"Service '{name}' already registered")

        cls._services[name] = service
        logger.info(f"Service registered: {name}", service_type=type(service).__name__)

    @classmethod
    def get(cls, name: str) -> Any:
        """
        Get registered service

        Args:
            name: Service identifier

        Returns:
            Domain service instance

        Raises:
            RuntimeError: If service not registered
        """
        if name not in cls._services:
            raise RuntimeError(
                f"Service '{name}' not registered. "
                f"Available services: {list(cls._services.keys())}"
            )
        return cls._services[name]

    @classmethod
    def get_llm(cls) -> "LLMDomainService":
        """
        Convenience method for LLM service access

        Returns:
            LLMDomainService instance
        """
        return cls.get("llm")

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if service is registered"""
        return name in cls._services

    @classmethod
    def list_services(cls) -> list[str]:
        """Get list of registered service names"""
        return list(cls._services.keys())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered services (for testing)"""
        cls._services.clear()
        cls._initialized = False

    @classmethod
    def mark_initialized(cls) -> None:
        """Mark registry as initialized"""
        cls._initialized = True

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if registry is initialized"""
        return cls._initialized
```

**Acceptance Criteria**:
- [ ] File created at services/service_registry.py
- [ ] All methods implemented
- [ ] Docstrings complete
- [ ] Type hints correct
- [ ] Logging included

---

### Task 2: Create LLMDomainService (60 min)

**File**: `services/domain/llm_domain_service.py` (NEW)

**Follow Pattern**: `services/domain/github_domain_service.py`

**Implementation**:
```python
"""
LLM Domain Service

Domain service mediating all LLM access following DDD principles.
Provides clean interface for LLM operations across all consumers.
"""

from typing import Optional, List, Dict, Any
import structlog
from services.config.llm_config_service import LLMConfigService
from services.llm.provider_selector import ProviderSelector

logger = structlog.get_logger(__name__)

class LLMDomainService:
    """
    Domain service for LLM operations

    Mediates all LLM access following Domain-Driven Design principles.
    This is THE ONLY way to access LLM providers in the system.

    Usage:
        # Access via ServiceRegistry
        llm = ServiceRegistry.get_llm()

        # Generate completion
        response = await llm.generate(
            prompt="Hello",
            task_type="general"
        )
    """

    def __init__(
        self,
        config_service: Optional[LLMConfigService] = None,
        provider_selector: Optional[ProviderSelector] = None
    ):
        """
        Initialize LLM domain service

        Args:
            config_service: Optional LLMConfigService for testing
            provider_selector: Optional ProviderSelector for testing
        """
        self._config_service = config_service
        self._provider_selector = provider_selector
        self._clients = {}
        self._initialized = False

    async def initialize(self) -> None:
        """
        Initialize service (called from main.py at startup)

        Validates all providers and initializes clients.
        Must be called before any LLM operations.

        Raises:
            RuntimeError: If initialization fails
        """
        try:
            logger.info("Initializing LLM domain service...")

            # Initialize config service if not provided
            if not self._config_service:
                self._config_service = LLMConfigService()

            # Validate all providers
            logger.info("Validating LLM providers...")
            validation_results = await self._config_service.validate_all_providers()

            # Log validation results
            for provider, result in validation_results.items():
                if result.is_valid:
                    logger.info(f"✅ {provider}: Valid")
                else:
                    logger.warning(f"⚠️ {provider}: {result.error_message}")

            # Count valid providers
            valid_count = sum(1 for r in validation_results.values() if r.is_valid)
            logger.info(f"LLM providers validated: {valid_count}/{len(validation_results)}")

            # Initialize provider selector
            if not self._provider_selector:
                self._provider_selector = ProviderSelector(self._config_service)

            # Initialize clients
            self._initialize_clients()

            self._initialized = True
            logger.info("LLM domain service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize LLM domain service: {e}")
            raise RuntimeError(f"LLM domain service initialization failed: {e}")

    def _initialize_clients(self) -> None:
        """Initialize LLM clients for available providers"""
        try:
            # Import clients here to avoid circular imports
            from services.llm import clients

            available = self._config_service.get_available_providers()

            for provider in available:
                if provider == "openai" and hasattr(clients, "openai_client"):
                    self._clients["openai"] = clients.openai_client
                elif provider == "anthropic" and hasattr(clients, "anthropic_client"):
                    self._clients["anthropic"] = clients.anthropic_client
                elif provider == "gemini" and hasattr(clients, "gemini_client"):
                    self._clients["gemini"] = clients.gemini_client
                elif provider == "perplexity" and hasattr(clients, "perplexity_client"):
                    self._clients["perplexity"] = clients.perplexity_client

            logger.info(f"Initialized {len(self._clients)} LLM clients")

        except Exception as e:
            logger.error(f"Failed to initialize clients: {e}")
            raise

    async def generate(
        self,
        prompt: str,
        task_type: str = "general",
        provider: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate LLM completion

        Domain-level operation for LLM text generation.
        Automatically selects appropriate provider if not specified.

        Args:
            prompt: Input prompt for generation
            task_type: Type of task (general, coding, research)
            provider: Optional specific provider to use
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text response

        Raises:
            RuntimeError: If service not initialized
            ValueError: If no providers available
        """
        if not self._initialized:
            raise RuntimeError(
                "LLMDomainService not initialized. "
                "Call initialize() before using."
            )

        # Select provider
        if not provider:
            provider = self._provider_selector.select_provider(
                task_type=task_type
            )

        logger.info(
            "Generating LLM completion",
            provider=provider,
            task_type=task_type
        )

        # Get client
        client = self._get_client(provider)

        # Generate (implementation depends on actual client interface)
        # This is a placeholder - actual implementation depends on
        # how clients are currently structured
        try:
            # TODO: Update this based on actual client interface
            response = await client.generate(prompt, **kwargs)
            return response
        except Exception as e:
            logger.error(
                f"LLM generation failed",
                provider=provider,
                error=str(e)
            )
            raise

    def _get_client(self, provider: str) -> Any:
        """
        Get initialized client for provider

        Args:
            provider: Provider name

        Returns:
            Client instance

        Raises:
            ValueError: If provider not available
        """
        if provider not in self._clients:
            available = list(self._clients.keys())
            raise ValueError(
                f"Provider '{provider}' not available. "
                f"Available providers: {available}"
            )
        return self._clients[provider]

    def get_available_providers(self) -> List[str]:
        """
        Get list of available providers

        Returns:
            List of provider names
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_available_providers()

    def get_default_provider(self) -> str:
        """
        Get default provider

        Returns:
            Default provider name
        """
        if not self._initialized:
            raise RuntimeError("Service not initialized")

        return self._config_service.get_default_provider()

    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self._initialized
```

**Note on Client Interface**: The `generate()` method includes a TODO comment because we need to check how clients.py currently structures its client interface. Update this based on actual implementation.

**Acceptance Criteria**:
- [ ] File created at services/domain/llm_domain_service.py
- [ ] Follows github_domain_service.py pattern
- [ ] All methods implemented
- [ ] Initialization working
- [ ] Error handling robust
- [ ] Logging comprehensive

---

### Task 3: Initialize in main.py (15 min)

**File**: `main.py` (MODIFY at line 102)

**Add Service Initialization**:
```python
# Around line 102 (current placeholder location)

async def initialize_domain_services():
    """Initialize domain services at application startup"""
    from services.domain.llm_domain_service import LLMDomainService
    from services.service_registry import ServiceRegistry

    try:
        logger.info("Initializing domain services...")

        # Initialize LLM service
        llm_service = LLMDomainService()
        await llm_service.initialize()

        # Register in global registry
        ServiceRegistry.register("llm", llm_service)

        # Mark registry as initialized
        ServiceRegistry.mark_initialized()

        logger.info("Domain services initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize domain services: {e}")
        raise

# Then call this in main startup
def main():
    # ... existing code ...

    # Initialize domain services
    asyncio.run(initialize_domain_services())

    # ... rest of startup ...
```

**Follow Pattern**: Look at how ConfigValidator is initialized in main.py

**Acceptance Criteria**:
- [ ] Initialization function added
- [ ] Called at appropriate point in startup
- [ ] Error handling matches existing patterns
- [ ] Logging consistent with main.py style

---

### Task 4: Create Domain Tests (30 min)

**File**: `tests/domain/test_llm_domain_service.py` (NEW)

**Follow Pattern**: `tests/domain/test_user_preference_manager.py`

**Test Structure**:
```python
"""Tests for LLMDomainService"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from services.domain.llm_domain_service import LLMDomainService
from services.service_registry import ServiceRegistry

class TestLLMDomainService:
    """Test LLM domain service"""

    @pytest.fixture
    def mock_config_service(self):
        """Mock LLMConfigService"""
        mock = Mock()
        mock.get_available_providers.return_value = ["openai", "gemini"]
        mock.get_default_provider.return_value = "openai"
        mock.validate_all_providers = AsyncMock(return_value={
            "openai": Mock(is_valid=True),
            "gemini": Mock(is_valid=True)
        })
        return mock

    @pytest.fixture
    def mock_provider_selector(self):
        """Mock ProviderSelector"""
        mock = Mock()
        mock.select_provider.return_value = "openai"
        return mock

    @pytest.fixture
    async def llm_service(self, mock_config_service, mock_provider_selector):
        """Create LLMDomainService for testing"""
        service = LLMDomainService(
            config_service=mock_config_service,
            provider_selector=mock_provider_selector
        )
        # Mock client initialization
        service._clients = {"openai": Mock(), "gemini": Mock()}
        await service.initialize()
        return service

    async def test_initialization(self, mock_config_service, mock_provider_selector):
        """Service initializes correctly"""
        service = LLMDomainService(
            config_service=mock_config_service,
            provider_selector=mock_provider_selector
        )

        assert not service.is_initialized()

        # Mock client initialization
        service._clients = {"openai": Mock()}
        await service.initialize()

        assert service.is_initialized()
        mock_config_service.validate_all_providers.assert_called_once()

    async def test_generate_with_default_provider(self, llm_service):
        """Generate uses default provider when not specified"""
        # Mock client generate
        llm_service._clients["openai"].generate = AsyncMock(return_value="response")

        result = await llm_service.generate("test prompt")

        assert result == "response"
        llm_service._clients["openai"].generate.assert_called_once()

    async def test_generate_with_specific_provider(self, llm_service):
        """Generate uses specified provider"""
        llm_service._clients["gemini"].generate = AsyncMock(return_value="response")

        result = await llm_service.generate("test prompt", provider="gemini")

        assert result == "response"

    async def test_generate_before_initialization(self):
        """Generate raises error if not initialized"""
        service = LLMDomainService()

        with pytest.raises(RuntimeError, match="not initialized"):
            await service.generate("test")

    async def test_get_available_providers(self, llm_service, mock_config_service):
        """Returns available providers"""
        providers = llm_service.get_available_providers()
        assert providers == ["openai", "gemini"]

    async def test_invalid_provider(self, llm_service):
        """Raises error for invalid provider"""
        with pytest.raises(ValueError, match="not available"):
            await llm_service.generate("test", provider="invalid")


class TestServiceRegistry:
    """Test ServiceRegistry"""

    def setup_method(self):
        """Clear registry before each test"""
        ServiceRegistry.clear()

    def test_register_service(self):
        """Can register service"""
        mock_service = Mock()
        ServiceRegistry.register("test", mock_service)

        assert ServiceRegistry.is_registered("test")
        assert ServiceRegistry.get("test") == mock_service

    def test_get_unregistered_service(self):
        """Raises error for unregistered service"""
        with pytest.raises(RuntimeError, match="not registered"):
            ServiceRegistry.get("nonexistent")

    def test_register_duplicate(self):
        """Raises error for duplicate registration"""
        ServiceRegistry.register("test", Mock())

        with pytest.raises(ValueError, match="already registered"):
            ServiceRegistry.register("test", Mock())

    def test_list_services(self):
        """Lists registered services"""
        ServiceRegistry.register("svc1", Mock())
        ServiceRegistry.register("svc2", Mock())

        services = ServiceRegistry.list_services()
        assert "svc1" in services
        assert "svc2" in services

    def test_get_llm_convenience(self):
        """Convenience method for LLM access"""
        mock_llm = Mock()
        ServiceRegistry.register("llm", mock_llm)

        assert ServiceRegistry.get_llm() == mock_llm
```

**Acceptance Criteria**:
- [ ] Test file created
- [ ] Tests for initialization
- [ ] Tests for generate method
- [ ] Tests for error conditions
- [ ] Tests for ServiceRegistry
- [ ] All tests passing

---

### Task 5: Remove Web Layer LLM Validation (15 min)

**File**: `web/app.py` (MODIFY)

**Remove** the startup validation that was added in Phase 1 Part C (around lines 80-122).

**Why**: Validation now happens in main.py via LLMDomainService initialization.

**Acceptance Criteria**:
- [ ] LLM validation removed from web/app.py
- [ ] No LLM initialization in web layer
- [ ] Server still starts correctly

---

## Testing Strategy

### After Each Task
```bash
# After Task 1 (ServiceRegistry)
python -c "from services.service_registry import ServiceRegistry; print('✅ Import works')"

# After Task 2 (LLMDomainService)
python -c "from services.domain.llm_domain_service import LLMDomainService; print('✅ Import works')"

# After Task 3 (main.py)
python main.py
# Should see: "Initializing domain services..."
# Should see: "LLM providers validated..."

# After Task 4 (Tests)
pytest tests/domain/test_llm_domain_service.py -v

# After Task 5 (cleanup)
pytest tests/ -v
# All 43+ tests should still pass
```

---

## Success Criteria

### Functional
- [ ] ServiceRegistry working
- [ ] LLMDomainService initializes at startup
- [ ] Validation happens during initialization
- [ ] All new tests passing (15-20 tests)
- [ ] All existing tests still passing (43+)
- [ ] Server starts successfully

### Architectural
- [ ] Follows existing domain service patterns
- [ ] Proper dependency injection
- [ ] Clean error handling
- [ ] Comprehensive logging
- [ ] No web layer initialization

### Evidence Required
- [ ] Terminal output showing successful initialization
- [ ] Test results (all passing)
- [ ] Server startup logs
- [ ] grep showing no LLM init in web/app.py

---

## STOP Conditions

- If existing patterns don't match expectations
- If client interface is unclear
- If main.py startup pattern is different than expected
- If tests break in unexpected ways

**If STOP: Document findings and escalate**

---

## Time Breakdown

| Task | Description | Estimate |
|------|-------------|----------|
| 1 | ServiceRegistry | 30 min |
| 2 | LLMDomainService | 60 min |
| 3 | main.py integration | 15 min |
| 4 | Domain tests | 30 min |
| 5 | Web cleanup | 15 min |

**Total**: 2.5 hours (estimate 2-3 hours with testing)

---

## Important Notes

1. **Follow existing patterns** - We have 11 domain services to learn from
2. **Check client interface** - Update generate() method based on actual clients.py
3. **Preserve existing logic** - Keep all LLMConfigService and ProviderSelector logic
4. **Test continuously** - After each task, verify it works

---

**After Phase 1 completes, we'll update consumers in Phase 2.**

---

*Phase 1 implementation - October 9, 2025, 5:24 PM*
