# ADR-048: ServiceContainer Lifecycle Management

**Status:** Accepted
**Date:** 2026-01-04
**Issue:** [#322 ARCH-FIX-SINGLETON](https://github.com/mediajunkie/piper-morgan-product/issues/322)
**Author:** Lead Developer (Claude Code Opus)
**Approver:** PM (xian)

## Context

The ServiceContainer class used a singleton pattern (`__new__` override with `_instance` class variable) to ensure a single instance across the application. While this simplified service access, it blocked horizontal scaling:

- Multiple uvicorn workers could not function independently
- Kubernetes horizontal pod autoscaling was not possible
- Load balancer distribution across instances was blocked
- Cloud-native deployment patterns were incompatible

### Current State (Before)

```python
class ServiceContainer:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Problems:**
1. Singleton is per-process, but each uvicorn worker is a separate process
2. Workers cannot have independent service registries
3. Tests require `ServiceContainer.reset()` classmethod to clean up state
4. Implicit global state makes testing and reasoning difficult

## Decision

**Adopt application-scoped container lifecycle managed by FastAPI lifespan.**

The container will be:
- Created once during application startup (`web/startup.py`)
- Stored in `app.state.service_container`
- Accessed via FastAPI dependency injection (`get_container()`)
- Destroyed during application shutdown

### Rejected Alternatives

**Option 1: Per-Request Container**
- Create new container for each request
- Initialize all services per request
- Destroy after request completes

*Rejected because:*
- High overhead (service initialization is expensive)
- Inconsistent state within same request across different handlers
- Better suited for multi-tenant SaaS (not our current requirement)
- Can migrate to this later if multi-tenancy is needed

**Option 2: Keep Singleton**
- Maintain current pattern
- Accept single-worker deployment limitation

*Rejected because:*
- Blocks all horizontal scaling
- Architectural debt accumulates as codebase grows
- Modern cloud deployment requires multi-instance support

## Implementation

### Phase 1: Dependency Injection Helper

```python
# web/api/dependencies.py
def get_container(request: Request) -> ServiceContainer:
    """Get ServiceContainer from application state."""
    if not hasattr(request.app.state, "service_container"):
        raise HTTPException(status_code=503, detail="Container not initialized")
    return request.app.state.service_container
```

### Phase 2: Remove Singleton Pattern

```python
class ServiceContainer:
    """Application-scoped container (NOT a singleton)."""

    def __init__(self):
        self._registry = ServiceRegistry()
        self._initialized = False

    # No __new__ override
    # No _instance class variable
```

### Phase 3: Access Pattern

Routes use FastAPI dependency injection:

```python
from fastapi import Depends
from web.api.dependencies import get_container

@router.get("/example")
async def example(container: ServiceContainer = Depends(get_container)):
    service = container.get_service("my_service")
```

Services receive container via constructor:

```python
class MyService:
    def __init__(self, container: ServiceContainer):
        self.llm = container.get_service("llm")
```

## Consequences

### Positive

1. **Horizontal Scaling**: Multiple uvicorn workers function independently
2. **Testability**: No global state; tests create fresh containers
3. **Explicit Dependencies**: Container access is visible in function signatures
4. **Cloud-Native**: Compatible with Kubernetes, Docker Swarm, etc.

### Negative

1. **Migration Effort**: 9 production files + 15+ test files need updates
2. **Longer Function Signatures**: Routes need `Depends(get_container)`
3. **Breaking Change**: Services must receive container explicitly

### Neutral

1. **Memory**: Each worker has its own container (same as before with singleton per process)
2. **Startup Time**: Unchanged (initialization happens once per worker)

## Testing Implications

### Before (Singleton)
```python
def test_something():
    container = ServiceContainer()  # Gets singleton
    try:
        # test code
    finally:
        ServiceContainer.reset()  # Must reset global state
```

### After (Application-Scoped)
```python
def test_something():
    container = ServiceContainer()  # Creates new instance
    await container.initialize()
    # test code
    # No reset needed - container goes out of scope
```

## Migration Path

1. Create `get_container()` DI helper (backward compatible)
2. Migrate production callers to use DI
3. Remove singleton pattern from ServiceContainer
4. Update tests to create fresh containers
5. Verify multi-worker deployment

## Validation Criteria

- [ ] Multi-worker startup shows 4 separate "Creating ServiceContainer" logs
- [ ] No shared state between workers
- [ ] All existing tests pass
- [ ] 6 validation scenarios pass (see Issue #322)

## Related Decisions

- ADR-047: Async Event Loop Awareness (session management)
- Issue #469: Database session factory patterns
- Issue #484: Schema validation on startup

---

*Accepted by PM: 2026-01-04 (implicit in Phase -1 gameplan approval)*
