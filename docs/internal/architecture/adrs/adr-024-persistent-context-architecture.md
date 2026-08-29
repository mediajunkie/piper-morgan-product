# ADR-024: Persistent Context Foundation Architecture

## Status
Superseded by ADR-075 (status corrected 2026-08-29 — see Status correction at end of file)

## Context
MVP features require user preferences and session context persistence. The current system has in-memory session management with TTL cleanup, but lacks persistent storage for user preferences and long-term context retention across conversations and system restarts.

## Decision
Implement hierarchical preference system using JSON storage with existing database patterns. Leverage existing JSON context fields in Intent, Workflow, and FeedbackDB models to store user preferences and session context without requiring schema migrations.

## Consequences

### Positive
- **<500ms preference operations** for responsive user experience
- **Foundation for all MVP features** with consistent architecture
- **Scalable to 1000+ concurrent users** with existing infrastructure
- **No schema migrations required** - leverages existing JSON fields
- **Hierarchical preference system** (global → user → session) for flexibility

### Negative
- **JSON field complexity** - no built-in schema validation
- **Query performance** on JSON fields may be slower than structured fields
- **Data consistency** challenges with flexible JSON structure

### Neutral
- **Storage overhead** minimal for preference data
- **Migration complexity** low - no database schema changes

## Implementation Details

### Architecture Components
```python
# UserPreferenceManager (400+ lines)
class UserPreferenceManager:
    async def get_preference(self, key: str, user_id: str = None,
                           session_id: str = None, default: Any = None) -> Any
    async def set_preference(self, key: str, value: Any, user_id: str = None,
                           session_id: str = None) -> bool
    async def merge_preferences(self, user_id: str, session_id: str) -> Dict[str, Any]

# SessionPersistenceManager (500+ lines)
class SessionPersistenceManager:
    async def persist_session(self, session: ConversationSession) -> bool
    async def restore_session(self, session_id: str) -> ConversationSession
    async def cleanup_expired_sessions(self) -> int

# PreferenceAPI (600+ lines)
class PreferenceAPI:
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool
    async def get_session_context(self, session_id: str) -> Dict[str, Any]
```

### Database Integration
- **Existing JSON Fields**: Intent.context, Workflow.context, FeedbackDB.context
- **Session Tracking**: session_id indexing for efficient queries
- **Preference Storage**: User-specific preferences in context JSON
- **Performance**: <500ms operations with existing database infrastructure

### Preference Hierarchy
1. **Global Defaults**: System-wide preference defaults
2. **User Preferences**: User-specific customizations
3. **Session Context**: Temporary session-specific overrides
4. **Conflict Resolution**: Session preferences override user preferences

## Performance Requirements
- **Preference Retrieval**: <100ms
- **Context Persistence**: <500ms
- **Concurrent Users**: Support 1000+ simultaneous users
- **Response Time**: <500ms for all preference operations

## Test Coverage
- **100% TDD methodology** with comprehensive test suites
- **Standalone tests** for database-free validation
- **Performance tests** for latency requirements
- **Load tests** for concurrent user scenarios

## Related Decisions
- **ADR-012**: Unified Session Management - Extends existing session infrastructure
- **Excellence Flywheel**: Systematic verification of performance requirements
- **Multi-Agent Coordinator**: Foundation for user preference coordination

## References
- [Persistent Context Research](../../development/active/pending-review/PERSISTENT_CONTEXT_RESEARCH.md)
- User Preference Manager (see codebase)
- Session Persistence (see codebase)
- Preference API Endpoints (see codebase)

---

**Date**: August 20, 2025
**Author**: Cursor Agent
**Reviewers**: Chief Architect, Lead Developer
---

## Status correction (2026-08-29, Chief Architect — Architectural Review 2026, mechanical win #4)

**Status corrected → Superseded by ADR-075.** The JSON-field preference persistence this ADR
established was functionally replaced by ADR-075's owner-scoped personalization store; no
supersession was recorded at the time — this note closes that gap.
