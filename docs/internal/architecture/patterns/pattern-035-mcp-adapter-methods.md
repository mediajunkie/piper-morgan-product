# Pattern-035: MCP Integration Router with Adapter Methods

## Status

**Proven** — demonstrated in GitHub integration (promoted 2026-06-17 per stale-pattern triage; instance confirmed)

## Context

During MCP+Spatial migration (see ADR-038 for current spatial patterns, ADR-052 for tool-based MCP standardization), integration routers need to provide backward-compatible interfaces while delegating to new MCP spatial adapters. This creates a challenge:

- Existing feature-layer consumers expect stable method names (e.g., `get_recent_issues()`, `get_issue()`)
- New MCP spatial adapters use different method names (e.g., `list_github_issues_direct()`, `get_github_issue_direct()`)
- Migration must be non-breaking for existing code
- Need to support both lazy initialization and async token configuration

### When This Pattern Applies

- During dual implementation phases of MCP migrations
- When modernizing integrations without breaking existing consumers
- When adding MCP+Spatial capabilities to legacy integration code
- When routers need async initialization for API tokens or configuration

## Pattern Description

Add thin adapter methods to integration routers that:

1. Provide stable, consumer-facing interface
2. Delegate to MCP+Spatial adapters internally
3. Support lazy initialization for async operations
4. Translate parameter names/formats between interfaces
5. Maintain backward compatibility during migration

### Core Concept

**Interface Stability via Delegation** - Router provides unchanging public interface while implementation evolves to use MCP protocol and spatial intelligence.

**Lazy Initialization** - Router initializes async resources (like API tokens) on first use rather than during construction, using double-check locking pattern.

## Implementation

### Structure

```
GitHubIntegrationRouter (stable interface)
    ├── __init__() - sync initialization
    ├── initialize() - async initialization (idempotent)
    ├── get_recent_issues() - adapter method → list_github_issues_direct()
    ├── get_issue() - adapter method → get_github_issue_direct()
    ├── get_open_issues() - adapter method → get_recent_issues()
    └── _mcp_adapter: GitHubMCPSpatialAdapter
            ├── list_github_issues_direct() - MCP implementation
            ├── get_github_issue_direct() - MCP implementation
            └── configure_github_api() - async token setup
```

### Code Example

```python
# File: services/integrations/github/github_integration_router.py

class GitHubIntegrationRouter:
    """
    Integration router for GitHub operations.
    Provides stable interface while delegating to MCP+Spatial implementation.

    ARCHITECTURAL PATTERN (ADR-038 Delegated MCP Pattern, ADR-052 Tool-Based MCP):
    - Consumers call router methods (get_recent_issues, etc.)
    - Router delegates to MCP+Spatial adapter
    - Adapter provides 8-dimensional spatial context
    - Adapter handles MCP protocol and circuit breakers
    """

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """Initialize router with sync operations only."""
        self.config_service = config_service or GitHubConfigService()
        self.mcp_adapter = GitHubMCPSpatialAdapter()

        # Lazy initialization tracking
        self._initialized = False
        self._initialization_lock = None  # Created in async context

    async def initialize(self):
        """
        Initialize the router asynchronously (idempotent).

        Uses double-check locking pattern to ensure:
        - Only one initialization occurs
        - Thread-safe in async context
        - Safe to call multiple times
        """
        # Skip if already initialized
        if self._initialized:
            return

        # Create lock if needed (first async call)
        if self._initialization_lock is None:
            import asyncio
            self._initialization_lock = asyncio.Lock()

        # Double-check pattern
        async with self._initialization_lock:
            if self._initialized:
                return

            # Configure MCP adapter with authentication
            token = self.config_service.get_authentication_token()
            if token:
                await self.mcp_adapter.configure_github_api(token)

            self._initialized = True

    async def get_recent_issues(
        self,
        repo: str = None,
        limit: int = 10,
        state: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        Get recent issues (adapter method).

        ADAPTER METHOD: Delegates to MCP spatial adapter.
        Uses lazy initialization to ensure token loaded.
        """
        # Lazy initialization
        if not self._initialized:
            await self.initialize()

        # Delegate to MCP adapter (different method name)
        return await self.mcp_adapter.list_github_issues_direct(
            repository=repo,
            limit=limit,
            state=state
        )

    async def get_issue(
        self,
        issue_number: int,
        repo: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get single issue by number (adapter method).

        ADAPTER METHOD: Delegates to MCP spatial adapter.
        Uses lazy initialization to ensure token loaded.
        """
        # Lazy initialization
        if not self._initialized:
            await self.initialize()

        # Delegate to MCP adapter (different method name + parameter format)
        return await self.mcp_adapter.get_github_issue_direct(
            issue_number=str(issue_number),  # MCP expects string
            repository=repo
        )

    async def get_open_issues(
        self,
        repo: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get open issues (adapter method).

        ADAPTER METHOD: Delegates to another adapter method.
        """
        return await self.get_recent_issues(
            repo=repo,
            limit=limit,
            state="open"
        )
```

## Usage Guidelines

### When to Use

- ✅ During MCP+Spatial migrations (dual implementation phase)
- ✅ When existing consumers depend on stable method signatures
- ✅ When adding spatial intelligence to existing integrations
- ✅ When async initialization is needed (API tokens, configuration)
- ✅ When MCP adapter uses different method names than legacy interface

### When NOT to Use

- ❌ For new integrations (use MCP adapter directly)
- ❌ When no existing consumers exist (no backward compatibility needed)
- ❌ After migration complete (consumers should call MCP adapter directly)
- ❌ When performance overhead of delegation is unacceptable

### Best Practices

1. **Idempotent Initialization**: Use double-check locking pattern for async init
2. **Clear Documentation**: Mark adapter methods with `ADAPTER METHOD` comments
3. **Parameter Translation**: Document any parameter format changes (e.g., int → string)
4. **Lazy Init Pattern**: Initialize on first use, not in constructor
5. **Preserve Interface**: Keep existing method signatures unchanged
6. **Test Both Paths**: Verify adapter delegation AND lazy initialization work

### Common Pitfalls

- ⚠️ Forgetting to call `initialize()` in adapter methods (causes token not loaded)
- ⚠️ Using synchronous initialization for async operations
- ⚠️ Not making `initialize()` idempotent (can cause duplicate setup)
- ⚠️ Changing parameter types without documentation
- ⚠️ Not preserving return type compatibility

## Examples in Codebase

### Primary Usage

- `services/integrations/github/github_integration_router.py` - Complete implementation
  - `get_recent_issues()` adapter method (lines 331-349)
  - `get_issue()` adapter method (lines 183-200)
  - `get_open_issues()` adapter method (lines 307-328)
  - `initialize()` idempotent async init (lines 119-156)

### Test Examples

- `tests/features/test_morning_standup.py` - Feature-layer usage
  - Mocks `github_domain_service.get_recent_issues()` which uses adapter
- `tests/integration/test_github_mcp_router_integration.py` - Integration testing
  - Verifies adapter delegation and lazy initialization

## Related Patterns

### Complements

- [Pattern-022: MCP+Spatial Intelligence Integration](pattern-022-mcp-spatial-intelligence-integration.md) - Underlying MCP adapter pattern
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain services call these routers
- [Pattern-031: Plugin Wrapper](pattern-031-plugin-wrapper.md) - Similar adapter approach for plugins

### Related ADRs

- [ADR-038: Spatial Intelligence Architecture Patterns](../adrs/adr-038-spatial-intelligence-patterns.md) - Three valid spatial patterns (Granular, Embedded, Delegated MCP)
- [ADR-052: Tool-Based MCP Standardization](../adrs/adr-052-tool-based-mcp-standardization.md) - Tool-based MCP as canonical protocol approach
- [ADR-029: Domain Service Mediation Architecture](../adrs/adr-029-domain-service-mediation-architecture.md) - How domain services interact with routers

### Alternatives

- **Direct MCP Usage**: For new code with no legacy interface
- **Facade Pattern**: For more complex interface transformations
- **Proxy Pattern**: For adding behavior rather than just delegation

### Dependencies

- Requires MCP spatial adapter implementation
- Depends on config service for authentication
- Assumes async/await support in Python 3.7+

## Migration Strategy

### Phase 1: Legacy Interface (Before)

```python
class GitHubIntegrationRouter:
    def get_recent_issues(self, limit=10):
        # Direct GitHub API calls
        return self._github_client.list_issues(limit=limit)
```

### Phase 2: Adapter Methods (During Migration)

```python
class GitHubIntegrationRouter:
    async def get_recent_issues(self, limit=10):
        # Adapter method delegates to MCP
        return await self.mcp_adapter.list_github_issues_direct(limit=limit)
```

### Phase 3: MCP Only (After Migration)

```python
# Router retired, consumers call MCP adapter directly
mcp_adapter = GitHubMCPSpatialAdapter()
issues = await mcp_adapter.list_github_issues_direct(limit=10)
```

## Benefits

- ✅ **Backward compatibility** - Existing consumers don't need code changes
- ✅ **Progressive migration** - Can migrate routers one at a time
- ✅ **Clean separation** - Interface vs implementation decoupled
- ✅ **Lazy initialization** - Resources loaded only when needed
- ✅ **Testability** - Can test adapter delegation independently
- ✅ **Spatial intelligence** - MCP adapters add 8-dimensional context automatically

## Performance Considerations

- **Delegation Overhead**: Minimal (single async function call)
- **Initialization Cost**: One-time async token setup on first use
- **Memory**: Small (one flag + one lock per router instance)
- **Typical Performance**: <1ms delegation, 800-1000ms for real API calls

## References

### Documentation

- **ADR-038**: Spatial Intelligence Architecture Patterns (current spatial policy)
- **ADR-052**: Tool-Based MCP Standardization (protocol architecture)
- **ADR-029**: Domain Service Mediation Architecture
- **Issue #119**: CORE-STAND-FOUND (Sprint A4 implementation)

### Usage Analysis

- **Current usage**: 1 router (GitHub)
- **Planned migrations**: Calendar, Notion, Slack routers
- **First implemented**: October 19, 2025
- **Maintenance status**: Active (Sprint A4)

### Implementation Evidence

- Session summary: `dev/2025/10/19/integration-fixes-complete.md`
- Verification: Successfully retrieved 100 real GitHub issues
- Performance: 948-1004ms (real API calls vs 1-2ms mock data)

---

_Pattern created: October 19, 2025_
_Sprint: A4 (CORE-STAND-FOUND)_
_Status: Emerging (proven in production)_
_Last Updated: January 13, 2026 (reference updates: ADR-013 → ADR-038, ADR-052)_
