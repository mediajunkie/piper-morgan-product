# Pattern Index

_Consolidated from pattern-catalog.md and PATTERN-INDEX.md_
_Format: ADR-style numbered patterns_

**Total Patterns**: 33 patterns (001-033) + template (000)

## Pattern Categories

### Core Architecture Patterns

_Foundational patterns for system architecture and infrastructure_

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access encapsulation
- [Pattern-002: Service Pattern](pattern-002-service.md) - Business logic organization
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Object creation abstraction
- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Command/query separation
- [Pattern-005: Transaction Management](pattern-005-transaction-management.md) - Data consistency
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Error propagation
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain organization
- [Pattern-014: Error Handling API Contract](pattern-014-error-handling-api-contract.md) - API error contracts
- [Pattern-015: Internal Task Handler](pattern-015-internal-task-handler.md) - Task processing patterns
- [Pattern-017: Background Task Error Handling](pattern-017-background-task-error-handling.md) - Async error management

### Data & Query Patterns

_Data access, session management, and query abstraction patterns_

- [Pattern-013: Session Management](pattern-013-session-management.md) - Database session handling
- [Pattern-016: Repository Context Enrichment](pattern-016-repository-context-enrichment.md) - Context-aware data access
- [Pattern-023: Query Layer Patterns](pattern-023-query-layer-patterns.md) - Query abstraction layers
- [Pattern-025: Canonical Query Extension](pattern-025-canonical-query-extension.md) - Query extension patterns
- [Pattern-026: Cross-Feature Learning](pattern-026-cross-feature-learning.md) - Feature learning integration

### AI & Intelligence Patterns

_AI coordination, spatial intelligence, and language model integration patterns_

- [Pattern-012: LLM Adapter](pattern-012-llm-adapter.md) - Language model integration
- [Pattern-019: LLM Placeholder Instruction](pattern-019-llm-placeholder-instruction.md) - AI instruction patterns
- [Pattern-020: Spatial Metaphor Integration](pattern-020-spatial-metaphor-integration.md) - Spatial AI context
- [Pattern-022: MCP+Spatial Intelligence Integration](pattern-022-mcp-spatial-intelligence-integration.md) - MCP spatial patterns
- [Pattern-028: Intent Classification](pattern-028-intent-classification.md) - Natural language intent routing
- [Pattern-029: Multi-Agent Coordination](pattern-029-multi-agent-coordination.md) - Specialized agent orchestration
- [Pattern-032: Intent Pattern Catalog](pattern-032-intent-pattern-catalog.md) - Regex pattern management for intent classification
  - 44 total patterns across TEMPORAL (17), STATUS (14), PRIORITY (13)
  - 92% canonical query coverage achieved (Phase 3 expansion)

### Integration & Platform Patterns

_External system integration, plugin architecture, and platform connectivity patterns_

- [Pattern-018: Configuration Access](pattern-018-configuration-access.md) - Configuration management
- [Pattern-027: CLI Integration](pattern-027-cli-integration.md) - Command-line interface patterns
- [Pattern-030: Plugin Interface](pattern-030-plugin-interface.md) - Extensible integration architecture
- [Pattern-031: Plugin Wrapper](pattern-031-plugin-wrapper.md) - Adapter pattern for integration routers
- [Pattern-033: Notion Publishing](pattern-033-notion-publishing.md) - Knowledge management publishing

### Development & Process Patterns

_Development methodology, quality assurance, and workflow management patterns_

- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Methodology approach
- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md) - Process management
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Quality assurance
- [Pattern-011: Context Resolution](pattern-011-context-resolution.md) - Implicit context resolution
- [Pattern-021: Development Session Management](pattern-021-development-session-management.md) - Dev workflow sessions
- [Pattern-024: Methodology Patterns](pattern-024-methodology-patterns.md) - Development methodology patterns

## Pattern Development

### Creating New Patterns

See [pattern-000-template.md](pattern-000-template.md) for the standard template when creating new patterns.

### Pattern Status Levels

- **Proven**: Established patterns with extensive usage
- **Emerging**: New patterns with initial validation
- **Experimental**: Patterns under active development
- **Deprecated**: Legacy patterns being phased out

## Navigation

- **[Main Documentation](../README.md)** - Return to main docs
- **[Architecture Overview](../architecture/README.md)** - System architecture documentation
- **[Development Guides](../development/README.md)** - Developer resources

## Legacy References

- Original catalog: [../architecture/pattern-catalog.md](../architecture/pattern-catalog.md)
- Previous index: [archive/PATTERN-INDEX-legacy.md](archive/PATTERN-INDEX-legacy.md)

---

_Last updated: October 5, 2025_
_All 32 patterns now included with logical categorization_
