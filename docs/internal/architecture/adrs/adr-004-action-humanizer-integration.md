# ADR-004: Action Humanizer Integration

## Status

Accepted

## Date

2025-07-13

## Context

Piper Morgan's user-facing messages contained technical action strings (e.g., "investigate_crash") that were exposed directly to users. This created several problems:

1. **Poor User Experience**: Technical jargon confused non-technical users
2. **Inconsistent Messaging**: Different parts of the system formatted actions differently
3. **Maintenance Burden**: Hardcoded message strings scattered throughout codebase
4. **Limited Flexibility**: No easy way to A/B test or improve messaging

## Decision

Implement an Action Humanizer system with the following components:

1. **ActionHumanizer Service**: Converts technical actions to natural language
2. **Caching Layer**: Database-backed cache for performance
3. **TemplateRenderer**: Integrates humanization with message templates
4. **Rule-Based Engine**: Predictable conversions for common patterns
5. **Usage Tracking**: Analytics on which actions are used most

## Rationale

### Why Caching?

- Same actions appear repeatedly (e.g., "create_ticket")
- Database lookup is faster than regeneration
- Enables usage analytics and optimization

### Why Rule-Based?

- Predictable and testable
- No external dependencies
- Fast execution (<1ms)
- Covers 90% of use cases

### Why Templates?

- Centralized message management
- Consistent formatting
- Easy to modify without code changes

## Consequences

### Positive

- **Improved UX**: Natural language instead of technical jargon
- **Performance**: Sub-millisecond response for cached entries
- **Consistency**: Same action always produces same text
- **Analytics**: Usage tracking identifies common actions
- **Maintainability**: Centralized message generation
- **Extensibility**: Easy to add LLM generation later

### Negative

- **Additional Complexity**: New service layer and database table
- **Migration Effort**: Existing messages need template conversion
- **Cache Management**: Need to handle cache invalidation
- **Testing Overhead**: More components to test

### Neutral

- **Database Growth**: One row per unique action (minimal impact)
- **Async Operations**: Humanization is now async throughout
- **Documentation Need**: Patterns must be well-documented

## Implementation Notes

### Phase 1 (Completed)

- Rule-based humanization
- Database caching
- Template integration
- Basic usage tracking

### Phase 2 (Future)

- LLM fallback for unknown patterns
- A/B testing framework
- Internationalization support
- Admin interface for overrides

## References

- Pattern Catalog: Action Humanizer Pattern
- Implementation: `services/ui_messages/action_humanizer.py`
- Tests: `tests/ui_messages/test_action_humanizer.py`
