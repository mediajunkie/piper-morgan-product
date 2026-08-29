# ADR-047: Async Event Loop Awareness for Database Connections

**Date**: December 3, 2025
**Status**: Draft (Pending Chief Architect Review)
**Deciders**: Chief Architect, Development Team
**Related**: ADR-006 (Standardize Async Session Management), Issue #442, Issue #453

## Context

### The Problem Discovered

During alpha testing of the setup wizard (Issue #442), users encountered `InterfaceError: cannot perform operation: another operation is in progress` and `Future attached to a different loop` errors. These errors only manifested in specific runtime conditions:

1. Application started via CLI (`python main.py setup`)
2. CLI wizard initialized database connection in Event Loop A
3. HTTP endpoints received requests in Event Loop B (uvicorn's loop)
4. Database sessions bound to Loop A failed when used in Loop B

### Root Cause Analysis

Python's `asyncio.run()` creates a **new event loop** each time it's called. When our application:

1. Initializes the global `db` singleton during startup (Event Loop A)
2. Runs the CLI setup wizard with `asyncio.run(run_setup_wizard())` (creates Event Loop B)
3. The global `db.engine` remains bound to Event Loop A
4. Any database operation in Event Loop B fails with event loop mismatch errors

This is particularly insidious because:
- The code looks correct - it uses `session_scope()` properly
- Tests may pass if they run in a single event loop context
- Errors only appear in specific multi-loop runtime configurations
- Error messages don't clearly indicate the cause is event loop mismatch

### Pattern Not Covered by ADR-006

ADR-006 established `AsyncSessionFactory.session_scope()` as the standard pattern, but assumed all database operations would occur within a single event loop context. This assumption breaks in:

- CLI commands that spawn separate async contexts
- Background workers with their own event loops
- Test scenarios with pytest-asyncio's loop isolation
- Multi-process deployments sharing database configuration

## Decision

### Introduce Event Loop-Aware Session Scope Pattern

Add `session_scope_fresh()` to `AsyncSessionFactory` as the safe pattern for code that may run in a different event loop than application startup.

```python
class AsyncSessionFactory:
    @staticmethod
    @asynccontextmanager
    async def session_scope():
        """Standard pattern - uses global db singleton.

        Use when: Code runs in the same event loop as app startup.
        Examples: HTTP request handlers, background tasks started during startup.
        """
        session = await db.get_session()
        try:
            yield session
        finally:
            await session.close()

    @staticmethod
    @asynccontextmanager
    async def session_scope_fresh():
        """Fresh engine pattern - creates new engine per request.

        Use when: Code may run in a different event loop than app startup.
        Examples: CLI wizards, setup endpoints, test fixtures.

        Trade-off: Slightly higher overhead (new engine creation) for
        guaranteed event loop safety.
        """
        engine = create_async_engine(
            _get_database_url(),
            pool_size=1,
            max_overflow=0,
        )
        session_factory = async_sessionmaker(engine)
        session = session_factory()
        try:
            yield session
        finally:
            await session.close()
            await engine.dispose()
```

### Decision Criteria: When to Use Each Pattern

| Scenario | Pattern | Rationale |
|----------|---------|-----------|
| HTTP request handlers | `session_scope()` | Same event loop as uvicorn startup |
| Background tasks via FastAPI | `session_scope()` | Same event loop as application |
| CLI commands with `asyncio.run()` | `session_scope_fresh()` | New event loop context |
| Setup wizard endpoints | `session_scope_fresh()` | May be called before/after CLI |
| Test fixtures | `session_scope_fresh()` | pytest-asyncio creates isolated loops |
| Worker processes | `session_scope_fresh()` | Separate process = separate loop |

### Detection Heuristic

When reviewing code, look for these patterns that suggest `session_scope_fresh()` is needed:

1. **`asyncio.run()` anywhere in the call chain** - Creates new event loop
2. **Code in `cli/` directory** - Often invoked separately from main app
3. **Endpoints marked for "setup" or "initialization"** - May run before normal startup
4. **Code that checks "is database initialized?"** - Chicken-and-egg scenarios
5. **Multiprocessing or subprocess usage** - Separate process = separate loop

## Consequences

### Positive

- **Eliminates cryptic event loop errors** - Clear pattern for multi-loop scenarios
- **Maintains performance for common case** - `session_scope()` still uses efficient pooling
- **Self-documenting code** - Method name indicates awareness of loop context
- **Testable pattern** - Fresh engines are easier to isolate in tests

### Negative

- **Cognitive overhead** - Developers must choose between two patterns
- **Slight performance cost** - `session_scope_fresh()` creates/disposes engines per request
- **Pattern proliferation** - Third session pattern after ADR-006's consolidation

### Neutral

- **Documentation requirement** - Must document when to use each pattern
- **Code review checklist** - Reviewers should verify correct pattern choice

## Implementation Checklist

### Immediate (Issue #442 Fix - Completed)

- [x] Add `session_scope_fresh()` to `AsyncSessionFactory`
- [x] Update `setup_wizard.py` to use `session_scope_fresh()` (16 call sites)
- [x] Document Issue #442 root cause and fix

### Audit Required (Issue #453 - Pending)

- [ ] Audit all `session_scope()` usage for event loop safety
- [ ] Identify CLI commands needing `session_scope_fresh()`
- [ ] Review test fixtures for correct pattern usage
- [ ] Create lint rule or code review checklist

### Future Considerations

- Consider a runtime detection mechanism that warns when session is used in wrong loop
- Evaluate if pool-per-loop pattern is feasible for performance optimization
- Document pattern in developer onboarding materials

## Risk Mitigation

### Risk: Developers Choose Wrong Pattern

**Mitigation**:
- Default to `session_scope()` - it's correct for 90% of cases
- Document clear decision criteria in this ADR
- Add to code review checklist
- Consider lint rule for CLI code paths

### Risk: Performance Degradation

**Mitigation**:
- `session_scope_fresh()` only used in setup/initialization paths
- These paths are infrequent (once per session, not per request)
- Monitor if pattern spreads to hot paths inappropriately

## Pattern Catalog Integration

### Session Management Pattern (Extended from ADR-006)

**Standard Pattern** - `session_scope()`:
- ✅ Use for HTTP request handlers
- ✅ Use for background tasks started with application
- ✅ Uses connection pooling efficiently
- ❌ NOT safe if `asyncio.run()` in call chain

**Fresh Engine Pattern** - `session_scope_fresh()`:
- ✅ Use for CLI commands
- ✅ Use for setup/initialization endpoints
- ✅ Use for test fixtures
- ✅ Safe across event loop boundaries
- ⚠️ Higher overhead - don't use in hot paths

## Lessons Learned

### What Would Have Helped

1. **Earlier awareness** - This ADR documents what we wish we'd known before Issue #442
2. **Detection patterns** - The heuristics above would have caught this during code review
3. **Test coverage gap** - Unit tests in single-loop context don't catch multi-loop issues
4. **Error message improvement** - `InterfaceError: another operation is in progress` doesn't suggest event loop issues

### Key Insight

The async ecosystem's "works in isolation, fails in integration" pattern is a fundamental challenge. Global singletons that bind to event loops at initialization time are a hidden coupling that breaks when runtime context changes.

---

**Draft Date**: December 3, 2025
**Submitted For Review**: Chief Architect
**Risk Level**: Low (extends existing pattern, doesn't replace it)
**Business Impact**: None (transparent to users, improves reliability)
