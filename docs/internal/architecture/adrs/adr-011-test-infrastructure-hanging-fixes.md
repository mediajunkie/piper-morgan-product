# ADR-011: Test Infrastructure Hanging Fixes

## Status

**Accepted** - 2025-07-30

## Context

During Phase 4 TDD implementation, tests were hanging during teardown due to MCP connection pool issues. The hanging was caused by:

1. **Circular import errors** during MCP module teardown
2. **Logging errors** on closed file handles during shutdown
3. **Timeout during pool shutdown** without proper cleanup
4. **Connection pool configuration** issues in test environment

## Decision

Implement aggressive timeout handling and defensive import strategies to prevent test hanging:

### 1. MCP Connection Pool Timeout Handling

```python
# In conftest.py mcp_infrastructure_reset fixture
try:
    await asyncio.wait_for(pool.shutdown(), timeout=0.1)
except asyncio.TimeoutError:
    # Force shutdown immediately if timeout occurs
    pool._is_shutdown = True
    pool._all_connections.clear()
    pool._available_connections.clear()
    pool._pool_lock = None
```

### 2. Defensive Import Strategies

```python
# Only try to reset MCP if the module exists and can be imported
try:
    from services.infrastructure.mcp.connection_pool import MCPConnectionPool
except ImportError:
    # MCP modules not available, skip cleanup
    pass
```

### 3. Logging Level Management

```python
# Disable logging during shutdown to prevent I/O errors
original_level = logging.getLogger().level
logging.getLogger().setLevel(logging.ERROR)

try:
    # MCP cleanup operations
    pass
finally:
    # Restore logging level
    logging.getLogger().setLevel(original_level)
```

### 4. Database Engine Disposal

```python
# In cleanup_sessions fixture
try:
    from services.database.connection import db
    if db.engine:
        await db.engine.dispose()
except Exception:
    pass  # Ignore disposal errors during cleanup
```

## Consequences

### Positive

- ✅ **Tests no longer hang** during teardown
- ✅ **Infrastructure is stable** for TDD development
- ✅ **Graceful degradation** when MCP modules unavailable
- ✅ **Proper resource cleanup** prevents memory leaks
- ✅ **Fast test execution** with 0.1s timeout

### Negative

- ⚠️ **Aggressive cleanup** may mask underlying issues
- ⚠️ **0.1s timeout** is very short but necessary for test stability
- ⚠️ **Defensive imports** add complexity to test setup

### Risks

- **Masked Issues**: Aggressive cleanup might hide real MCP problems
- **Timeout Sensitivity**: Very short timeout might be too aggressive in some cases
- **Import Complexity**: Defensive imports add cognitive overhead

## Implementation

### Files Modified

- `conftest.py` - MCP infrastructure reset fixture
- `services/database/connection.py` - Pool configuration
- `docs/development/test-strategy.md` - Infrastructure troubleshooting guide

### Configuration

```python
# Database connection pool settings
pool_size=5,           # Multiple connections for concurrent tests
max_overflow=10,       # Allow bursts during peak usage
pool_recycle=3600      # Refresh connections every hour
```

### Monitoring

- Test execution time should be <30 seconds total
- No hanging during teardown
- Clean exit codes from pytest
- No logging errors during shutdown

## Related

- **PM-078**: TDD Implementation Plan
- **ADR-008**: MCP Connection Pooling Production
- **ADR-006**: Standardize Async Session Management

## Notes

This ADR addresses immediate infrastructure stability issues. Future work should investigate root causes of MCP circular imports and implement more robust connection pool management.

The aggressive timeout approach is a pragmatic solution that enables continued development while the underlying architectural issues are addressed.
