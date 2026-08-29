# ADR-025: Unified Session Management Architecture

**Status:** Accepted
**Date:** 2025-08-07
**Context:** PM-034 Foundation Repair - Database Integration Architecture
**Decision Maker:** Lead Developer (Code Agent)
**Stakeholders:** Chief Architect, Infrastructure Team

## Summary

Unify database session management across Piper Morgan services by standardizing on AsyncSessionFactory pattern and eliminating competing session creation approaches that cause transaction conflicts and integration failures.

## Context

### Problem Statement

Root cause analysis revealed critical database integration failures:

1. **Two Competing Patterns:**

   - Modern: `AsyncSessionFactory.session_scope()`
   - Legacy: `RepositoryFactory` + `db.get_session()`

2. **Transaction Boundary Conflicts:**

   ```python
   # services/database/repositories.py:49-115
   if self.session.in_transaction():
       # Already in transaction, just add the entity
   else:
       # Start new transaction - CREATES NESTED CONFLICTS
       async with self.session.begin():
   ```

3. **Integration Health Impact:**
   - Database Connection: 0% reliability (failing component)
   - Session leaks causing connection pool exhaustion
   - Silent transaction failures in concurrent operations

### Current State Analysis

**Files with AsyncSessionFactory (Modern Pattern):**

- `services/database/session_factory.py` - Core implementation
- `services/intent_service/llm_classifier_factory.py`
- `services/repositories/todo_repository.py`
- `services/orchestration/engine.py`
- `services/api/health/staging_health.py`

**Files with Legacy Patterns:**

- `services/database/repositories.py` - BaseRepository (594 lines)
- `services/database/connection.py` - Global `db` instance

## Decision

### Primary Decision

**Adopt AsyncSessionFactory as the single database session management pattern** across all Piper Morgan services.

### Architectural Standards

1. **Session Creation:**

   ```python
   # STANDARD PATTERN (Required)
   async with AsyncSessionFactory.session_scope() as session:
       repository = SomeRepository(session)
       await repository.operation()
       # Automatic commit and cleanup
   ```

2. **Repository Pattern Update:**

   ```python
   # ELIMINATE transaction detection logic
   # SIMPLIFY to single-responsibility operations
   async def create(self, **kwargs) -> Any:
       entity = self.model(**kwargs)
       self.session.add(entity)
       await self.session.flush()
       return entity
   ```

3. **Service Integration:**
   ```python
   # STANDARD SERVICE PATTERN
   class UnifiedService:
       async def perform_operation(self, data):
           async with AsyncSessionFactory.session_scope() as session:
               repository = SomeRepository(session)
               return await repository.operation(data)
   ```

## Consequences

### Positive Outcomes

1. **Elimination of Session Conflicts:**

   - Single session creation pattern
   - No nested transaction boundary issues
   - Predictable resource lifecycle management

2. **Simplified Repository Pattern:**

   - Remove complex transaction detection logic
   - Single responsibility for each repository method
   - Clear separation between business logic and transaction management

3. **Improved Integration Reliability:**

   - Database connection component becomes reliable
   - Foundation for Phase 3 ConversationManager implementation
   - Enables PM-034 parallel execution architecture

4. **Developer Experience:**
   - Consistent patterns across all services
   - Reduced cognitive load
   - Clear migration path from legacy code

### Migration Requirements

1. **Immediate Actions:**

   - Update BaseRepository to remove transaction detection
   - Migrate RepositoryFactory usage to AsyncSessionFactory
   - Deprecate `db.get_session()` global pattern

2. **Service Updates Required:**

   - All services using BaseRepository must wrap operations in session_scope()
   - Remove direct session creation outside AsyncSessionFactory
   - Update test fixtures to use unified patterns

3. **Testing Strategy:**
   - Verify all integration tests pass with unified session management
   - Confirm no session leaks under concurrent load
   - Validate transaction isolation in complex workflows

## Implementation Plan

### Phase 1: Core Pattern Implementation

- [ ] Update BaseRepository to eliminate transaction detection
- [ ] Create UnifiedSessionManager wrapper for complex operations
- [ ] Update core services to use session_scope() consistently

### Phase 2: Service Migration

- [ ] Migrate all RepositoryFactory usage
- [ ] Update OrchestrationEngine session handling
- [ ] Verify QueryRouter integration compatibility

### Phase 3: Validation & Cleanup

- [ ] Remove deprecated db.get_session() patterns
- [ ] Update documentation and examples
- [ ] Confirm 100% reliability of database connection component

## Risks and Mitigation

### Risk 1: Service Disruption During Migration

**Mitigation:** Incremental migration with backward compatibility during transition

### Risk 2: Performance Impact of Session Scope Changes

**Mitigation:** Performance testing at each migration step, optimization if needed

### Risk 3: Complex Services with Multiple Repository Operations

**Mitigation:** UnifiedSessionManager for services requiring transaction coordination

## Success Criteria

1. **Technical Metrics:**

   - Database Connection component: 0% → 100% reliability
   - Zero session leaks in integration tests
   - All services using single session creation pattern

2. **Integration Health:**

   - Foundation stable for PM-034 Phase 3 implementation
   - ConversationManager can rely on consistent session management
   - Slack integration stability improved through reliable database layer

3. **Code Quality:**
   - Elimination of competing session patterns
   - Simplified repository transaction logic
   - Clear service-to-database interaction patterns

## References

- PM-034 Phase 1: Conversation Foundation
- PM-034 Phase 2: Anaphoric Reference Resolution
- PM-034 Phase 3: Integration Architecture (blocked pending this ADR)
- Root Cause Analysis: Integration Architecture Failures (2025-08-07)

## Related Decisions

- ADR-010: MCP Integration Architecture (async patterns)
- Future ADR-008: Circuit Breaker Integration Patterns
- Future ADR-009: Slack Integration Simplification

---

**Implementation Priority:** P0 - Foundational (blocks PM-034 Phase 3)
**Estimated Effort:** 3-5 points
**Dependencies:** None
**Follow-up ADRs:** Circuit breaker patterns, Slack integration simplification
