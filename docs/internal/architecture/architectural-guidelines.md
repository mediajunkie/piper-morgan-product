# Architectural Guidelines - Piper Morgan

This document outlines architectural principles, antipatterns to avoid, and the architecture-first approach for Piper Morgan development.

## Architecture-First Approach

Before implementing features:

1. **Consult documentation first** - Architecture patterns may already exist
2. **Verify against domain models** - All features must align with domain
3. **Check architectural layers** - Ensure changes respect boundaries
4. **Look for existing examples** - Grep for similar implementations
5. **Stop when patching** - Multiple quick fixes signal architectural work needed

### Layer Verification Commands

```bash
# Check domain models
cat services/domain/models.py

# Verify shared types
cat services/shared_types.py

# Check architectural patterns
grep -r "pattern_name" services/

# Find similar implementations
grep -r "similar_functionality" services/
```

## Excellence Flywheel Methodology

**MANDATORY**: All development work must follow the Excellence Flywheel methodology for systematic quality and velocity.

### Core Principles

1. **Systematic Verification First** - Verify requirements and existing state before implementation
2. **TDD Requirements** - Write tests FIRST, then implementation
3. **Agent Coordination** - Coordinate parallel work systematically
4. **Quality Vigilance** - Maintain high standards throughout

### Excellence Flywheel Process

#### Phase 1: Systematic Verification

- **Verify Requirements**: Understand exactly what needs to be built
- **Check Existing State**: What's already implemented and working
- **Identify Dependencies**: What other components are affected
- **Plan Architecture**: How the new feature fits into existing patterns

#### Phase 2: Test-Driven Development

- **Write Failing Tests**: Define expected behavior before implementation
- **Implement Minimum Viable**: Code that makes tests pass
- **Refactor**: Improve code quality while maintaining functionality
- **Verify Integration**: Ensure new code works with existing systems

#### Phase 3: Quality Assurance

- **Code Review**: Self-review against architectural guidelines
- **Integration Testing**: Verify component interactions
- **Performance Validation**: Ensure acceptable response times
- **Documentation Update**: Update relevant documentation

### Excellence Flywheel Benefits

- **Quality creates velocity creates quality** - Systematic approaches create self-reinforcing productivity cycles
- **Foundation-first approach** - Enables impossible speed with perfect quality
- **Compound learning** - Each implementation builds knowledge for accelerated future work
- **Risk mitigation** - Systematic verification prevents costly mistakes

### Excellence Flywheel Integration

- **Session Logs**: Every session must document Excellence Flywheel application
- **Code Reviews**: Verify Excellence Flywheel methodology was followed
- **Documentation**: Update architectural guidelines with new patterns discovered
- **Knowledge Preservation**: Document successful patterns for future sessions

For detailed methodology, see [Excellence Flywheel Documentation](../development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md).

## Common Antipatterns to Catch

### Development Antipatterns

❌ **Assuming methods exist without checking**

- Always verify method signatures before calling
- Use `grep` or direct file inspection

❌ **Galloping ahead without verification**

- Follow VERIFY → UNDERSTAND → IMPLEMENT → VALIDATE
- One step at a time, wait for confirmation

❌ **Modifying domain models to fix tests**

- Tests should reflect domain reality
- Fix tests, not domain models

❌ **Creating Path objects when strings expected**

- Check expected parameter types
- Use `str()` conversion when needed

❌ **Assuming import paths without verification**

- Verify actual file locations
- Check existing import patterns

### Domain Model Antipatterns

❌ **Fighting the intent classifier**

- Work with its preferences
- Understand its categorization logic

❌ **Creating enums outside shared_types.py**

- All enums belong in `services/shared_types.py`
- Maintain single source of truth

❌ **Assuming single data access pattern**

- Check for tier differences
- Verify repository patterns

### Architecture Antipatterns

❌ **Patching without understanding**

- Stop and design when fixes accumulate
- Address root causes, not symptoms

❌ **Skipping architecture review**

- Always check docs first
- Understand existing patterns

❌ **Mixing concerns across layers**

- Keep domain logic in domain services
- UI logic stays in presentation layer
- Infrastructure concerns in infrastructure layer

## Layer Boundaries

### Domain Layer

- **Location**: `services/domain/`
- **Responsibilities**: Core business logic, domain models
- **Dependencies**: None (depends on nothing)
- **Rules**: Pure business logic only

### Application Layer

- **Location**: `services/queries/`, `services/orchestration/`
- **Responsibilities**: Use cases, workflows, queries
- **Dependencies**: Domain layer only
- **Rules**: Coordinates domain objects

### Infrastructure Layer

- **Location**: `services/database/`, `services/integrations/`
- **Responsibilities**: External systems, persistence
- **Dependencies**: Domain and application layers
- **Rules**: Implements interfaces defined in domain

### Presentation Layer

- **Location**: `main.py`, `web/`
- **Responsibilities**: API endpoints, UI
- **Dependencies**: Application layer
- **Rules**: Minimal logic, delegate to application services

## Architectural Checks

### Before Adding New Code

```bash
# 1. Check if pattern already exists
grep -r "similar_functionality" services/

# 2. Verify domain model alignment
cat services/domain/models.py | grep -A 10 "relevant_model"

# 3. Check layer boundaries
# Domain depends on nothing
# Application depends on domain only
# Infrastructure can depend on domain and application
# Presentation depends on application only

# 4. Verify shared types usage
grep -r "enum_name" services/shared_types.py
```

### Red Flags That Require Architectural Review

1. **Multiple quick fixes** in same area
2. **Circular dependencies** between layers
3. **Domain logic** in presentation layer
4. **Direct database access** bypassing repositories
5. **Hardcoded values** that should be configuration
6. **Duplicate code** across services
7. **Complex conditionals** that should be polymorphic

## Best Practices

### Domain-Driven Design

- **Models drive everything** - Start with domain models
- **Ubiquitous language** - Use domain terms consistently
- **Bounded contexts** - Keep related concepts together
- **Aggregates** - Ensure consistency boundaries

### Testing Strategy

- **Test domain logic** thoroughly
- **Mock external dependencies** in unit tests
- **Integration tests** for workflows
- **End-to-end tests** for user scenarios

### Documentation

- **ADRs** for significant architectural decisions
- **Session logs** for development context
- **Code comments** for complex business rules
- **README updates** for new patterns

## When to Stop and Redesign

### Signals That Architecture Work Is Needed

1. **Patch upon patch** - Multiple fixes in same area
2. **Copy-paste code** - Similar logic in multiple places
3. **Long parameter lists** - Objects need better encapsulation
4. **Nested conditionals** - Complex logic needs abstraction
5. **Violation of single responsibility** - Classes doing too much
6. **Tight coupling** - Changes requiring updates in multiple places

### Redesign Process

1. **Document current state** - What's working, what's not
2. **Identify core problem** - Root cause, not symptoms
3. **Propose solution** - With clear benefits
4. **Create migration plan** - Step-by-step transformation
5. **Implement incrementally** - Small, safe changes
6. **Verify improvements** - Measure before/after

## Architecture Review Checklist

Before merging any significant change:

- [ ] Domain models remain pure (no external dependencies)
- [ ] Layer boundaries respected
- [ ] Shared types used for all enums
- [ ] Existing patterns followed
- [ ] Tests cover new functionality
- [ ] Documentation updated
- [ ] Session log reflects architectural decisions

---

_Last Updated: July 28, 2025_

## Revision Log

- **July 28, 2025**: Added Excellence Flywheel Methodology section with core principles, process phases, benefits, and integration guidelines
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
