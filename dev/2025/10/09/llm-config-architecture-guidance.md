# Architectural Guidance: LLM Configuration Refactoring

**Date**: October 9, 2025, 5:00 PM
**Issue**: #217 - CORE-LLM-CONFIG
**Status**: Architecture violation identified, refactoring required
**Priority**: High - Blocking proper implementation

---

## Executive Summary

The LLM configuration was incorrectly placed in the web layer. It needs to be refactored into a proper domain service pattern that all consumers (web, CLI, Slack) can access.

---

## The Architecture Violation

### What Was Built (Wrong)
```
web/app.py → LLMConfigService → Providers
(Web Only!)
```

### What Should Be Built (Correct)
```
main.py → LLMDomainService → LLMConfigService → Providers
           ↑                    ↑
    All consumers use    Infrastructure layer
    domain service
```

---

## Correct Architecture Design

### Layer Structure

```
APPLICATION LAYER (Consumers)
├── web/app.py           - Web application
├── cli/commands.py      - CLI commands
├── slack/bot.py         - Slack bot
└── workers/tasks.py     - Background tasks
         ↓
    DOMAIN LAYER (Business Logic)
├── services/domain/llm_domain_service.py
         ↓
    INFRASTRUCTURE LAYER (External Systems)
├── services/config/llm_config_service.py
├── services/llm/provider_selector.py
└── services/llm/clients.py
```

### Component Responsibilities

#### 1. LLMDomainService (NEW - Domain Layer)
```python
# services/domain/llm_domain_service.py
class LLMDomainService:
    """
    Domain service mediating all LLM access.
    This is THE ONLY way to access LLMs in the system.
    """

    def __init__(self):
        self._config_service = None
        self._provider_selector = None
        self._clients = {}
        self._initialized = False

    async def initialize(self):
        """Initialize on application startup"""
        self._config_service = LLMConfigService()
        await self._config_service.validate_all_keys()
        self._provider_selector = ProviderSelector(self._config_service)
        self._initialize_clients()
        self._initialized = True

    async def generate(
        self,
        prompt: str,
        task_type: str = "general",
        provider: Optional[str] = None
    ) -> str:
        """Generate LLM response - THE domain operation"""
        if not self._initialized:
            raise RuntimeError("LLMDomainService not initialized")

        # Select provider if not specified
        if not provider:
            provider = self._provider_selector.select(task_type)

        # Get client and generate
        client = self._get_client(provider)
        return await client.generate(prompt)
```

#### 2. Application Bootstrap (main.py)
```python
# main.py
from services.domain.llm_domain_service import LLMDomainService
from services.service_registry import ServiceRegistry

async def initialize_services():
    """Initialize all domain services at startup"""

    # Initialize LLM service
    llm_service = LLMDomainService()
    await llm_service.initialize()

    # Register for global access
    ServiceRegistry.register("llm", llm_service)

    # Initialize other domain services...

def main():
    # Initialize services ONCE at startup
    asyncio.run(initialize_services())

    # Then start application (web, CLI, Slack, etc.)
    start_application()
```

#### 3. Service Registry Pattern
```python
# services/service_registry.py
class ServiceRegistry:
    """Global registry for domain services"""
    _services = {}

    @classmethod
    def register(cls, name: str, service: Any):
        cls._services[name] = service

    @classmethod
    def get(cls, name: str) -> Any:
        if name not in cls._services:
            raise RuntimeError(f"Service {name} not registered")
        return cls._services[name]

    @classmethod
    def get_llm(cls) -> LLMDomainService:
        """Convenience method for LLM access"""
        return cls.get("llm")
```

#### 4. Consumer Access Pattern
```python
# ANY consumer (web, CLI, Slack)
from services.service_registry import ServiceRegistry

async def any_function_needing_llm():
    llm_service = ServiceRegistry.get_llm()
    response = await llm_service.generate(
        prompt="Hello",
        task_type="greeting"
    )
```

---

## Refactoring Plan

### Phase 1: Create Domain Service (1 hour)
1. Create `services/domain/llm_domain_service.py`
2. Move provider selection logic into domain service
3. Create service registry pattern
4. Add initialization to main.py

### Phase 2: Refactor Consumers (30 minutes)
1. Remove LLM validation from web/app.py
2. Update all consumers to use ServiceRegistry
3. Update tests to use domain service

### Phase 3: Verify Architecture (30 minutes)
1. Verify all layers follow DDD
2. Ensure no direct infrastructure access
3. Test all consumers can access LLM

---

## Key Decisions

### Q1: Where Does Initialization Belong?
**Answer**: `main.py` or application bootstrap, NOT web layer

### Q2: Should We Use Domain Service Pattern?
**Answer**: YES - LLMDomainService mediates all LLM access

### Q3: How Do Services Access LLM?
**Answer**: Through ServiceRegistry.get_llm()

### Q4: Where Does Provider Selection Belong?
**Answer**: Inside LLMDomainService (domain logic)

### Q5: Should Phase 1.5 (Keychain) Wait?
**Answer**: YES - Fix architecture first, then add keychain

---

## Migration Strategy

### Keep What Works
- LLMConfigService logic (just move initialization)
- Provider selection logic (move to domain)
- API validation logic (move to domain)

### Fix What's Wrong
- Remove from web/app.py
- Add domain service layer
- Add service registry
- Update all consumers

### Testing Strategy
```bash
# After refactoring, verify:
pytest tests/domain/test_llm_domain_service.py
pytest tests/integration/test_llm_access.py

# Verify CLI can access:
python -m cli.test_llm_access

# Verify Slack can access:
python -m slack.test_llm_access
```

---

## Process Improvements

### What Went Wrong
1. **No architectural gameplan** - Jumped to implementation
2. **Web-centric thinking** - Forgot about other consumers
3. **Missed DDD patterns** - Didn't review ADR-029/Pattern-008

### Future Prevention
1. **Always start with architecture** for infrastructure changes
2. **Review relevant ADRs/Patterns** before implementation
3. **Consider ALL consumers** not just web
4. **Use Phase 0 verification** of architectural approach

---

## Immediate Action Items

1. **STOP Phase 1.5** - Don't add keychain to wrong architecture
2. **Create LLMDomainService** - Follow pattern above
3. **Refactor initialization** - Move to main.py
4. **Update consumers** - Use ServiceRegistry
5. **Verify architecture** - All tests pass
6. **THEN proceed to Phase 1.5** - Add keychain to correct layer

---

## Success Criteria

- [ ] LLMDomainService created and working
- [ ] Initialization moved to main.py
- [ ] Web app uses ServiceRegistry
- [ ] CLI can access LLM service
- [ ] Slack can access LLM service
- [ ] All 43+ tests still passing
- [ ] Architecture follows DDD patterns

---

**Recommendation**: Take 2-3 hours to refactor properly now rather than accumulating technical debt. This is foundational infrastructure that everything else will build on.

---

*Chief Architect - October 9, 2025, 5:00 PM*
