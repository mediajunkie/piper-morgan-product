# Pattern Index

_Consolidated from pattern-catalog.md and PATTERN-INDEX.md_
_Format: ADR-style numbered patterns_

**Total Patterns**: 66 patterns (001-066), plus a template (000). Pattern-066 (Stacked Silent Failures) Emerging-filed 2026-05-09 per Pattern Sweep #1025 Phase 2C TRUE EMERGENCE finding.

> **How to read this catalog**: A code-side citation count alone does not determine whether a pattern is load-bearing. Many foundational patterns (Repository, Service, Factory) are followed implicitly throughout the codebase but rarely cited by name in code. Diagnostic-vocabulary patterns (e.g., Pattern-062 Assembly Assumption) are used in conversation and review work, not in code annotations. See the **[ADR catalog citation framework](../adrs/README.md#how-to-read-this-catalog-citation-framework)** for the full status taxonomy (Load-bearing-interface / Load-bearing-decision / Internalized / Archival / Genuinely decorative). Same framework applies here.

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
- [Pattern-034: Error Handling Standards](pattern-034-error-handling-standards.md) - REST-compliant HTTP status codes and error responses

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
- [Pattern-035: MCP Adapter Methods](pattern-035-mcp-adapter-methods.md) - Backward-compatible MCP migration pattern (ADR-013 Phase 2)
- [Pattern-040: Integration Swappability Guide](pattern-040-integration-swappability-guide.md) - Router pattern for pluggable provider implementations

### Infrastructure & Scheduling Patterns

_Background job execution, periodic tasks, and infrastructure coordination patterns_

- [Pattern-048: Periodic Background Job](pattern-048-periodic-background-job.md) - Lightweight asyncio-based periodic task execution with responsive shutdown

### Development & Process Patterns

_Development methodology, quality assurance, and workflow management patterns_

- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Methodology approach
- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md) - Process management
- [Pattern-010: Cross-Validation Protocol](pattern-010-cross-validation-protocol.md) - Quality assurance
- [Pattern-011: Context Resolution](pattern-011-context-resolution.md) - Implicit context resolution
- [Pattern-021: Development Session Management](pattern-021-development-session-management.md) - Dev workflow sessions
- [Pattern-024: Methodology Patterns](pattern-024-methodology-patterns.md) - Development methodology patterns
- [Pattern-036: Signal Convergence](pattern-036-signal-convergence.md) - Multi-analyzer breakthrough detection (META-PATTERN)
- [Pattern-037: Cross-Context Validation](pattern-037-cross-context-validation.md) - Concept validation across contexts (META-PATTERN)
- [Pattern-038: Temporal Clustering](pattern-038-temporal-clustering.md) - Coordination analysis via temporal grouping (META-PATTERN)
- [Pattern-039: Feature Prioritization Scorecard](pattern-039-feature-prioritization-scorecard.md) - Quantified feature prioritization framework
- [Pattern-041: Systematic Fix Planning](pattern-041-systematic-fix-planning.md) - Phase-based approach to multi-issue resolution
- [Pattern-042: Investigation-Only Protocol](pattern-042-investigation-only-protocol.md) - Separation of bug investigation from fixing
- [Pattern-043: Defense-in-Depth Prevention](pattern-043-defense-in-depth-prevention.md) - Multi-layer protection against discovered vulnerabilities
- [Pattern-044: MCP Skill Testing](pattern-044-mcp-skill-testing.md) - Testing patterns for MCP skill development
- [Pattern-045: Green Tests, Red User](pattern-045-green-tests-red-user.md) - Anti-pattern: tests pass but users fail (COMPLETION DISCIPLINE TRIAD)
- [Pattern-046: Beads Completion Discipline](pattern-046-beads-completion-discipline.md) - Systematic completion enforcement using `bd` CLI (COMPLETION DISCIPLINE TRIAD)
- [Pattern-047: Time Lord Alert](pattern-047-time-lord-alert.md) - Uncertainty signaling for AI agents (COMPLETION DISCIPLINE TRIAD)
- [Pattern-049: Audit Cascade](pattern-049-audit-cascade.md) - Institutionalized skepticism at every handoff point (VELOCITY PATTERN)
- [Pattern-059: Leadership Caucus](pattern-059-leadership-caucus.md) - Facilitated multi-advisor alignment for cross-cutting decisions (COORDINATION PATTERN)
- [Pattern-060: Cascade Investigation](pattern-060-cascade-investigation.md) - Treat every bug fix as a trigger for category-wide audit (INVESTIGATION PATTERN)
- [Pattern-061: Human-AI Collaboration Referee](pattern-061-human-ai-collaboration-referee.md) - Structured facilitation for human-AI decision processes (COORDINATION PATTERN)
- [Pattern-062: Assembly Assumption](pattern-062-assembly-assumption.md) - Multi-role convergence on shared artifacts (COORDINATION PATTERN)

### Grammar Application Patterns

_Patterns for maintaining grammar awareness (Entity/Moment/Place) throughout features_

- [Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md) - Maintain grammar awareness with Context/Result dataclass pairs
- [Pattern-051: Parallel Place Gathering](pattern-051-parallel-place-gathering.md) - Synthesize information from multiple integrations concurrently
- [Pattern-052: Personality Bridge](pattern-052-personality-bridge.md) - Transform contextual data into Piper's authentic voice
- [Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md) - Calibrate emotional tone based on context and relationship
- [Pattern-054: Honest Failure with Suggestion](pattern-054-honest-failure.md) - Handle integration failures with helpful guidance
- [Pattern-055: Multi-Intent Decomposition](pattern-055-multi-intent-decomposition.md) - Detect and handle multiple intents in single messages
- [Pattern-056: Consciousness Attribute Layering](pattern-056-consciousness-attribute-layering.md) - Layer consciousness attributes through processing
- [Pattern-057: Grammar-Driven Classification](pattern-057-grammar-driven-classification.md) - Use grammar structure to guide intent classification
- [Pattern-058: Ownership Graph Navigation](pattern-058-ownership-graph-navigation.md) - Navigate object relationships via ownership semantics

## Pattern Development

### Creating New Patterns

See [pattern-000-template.md](pattern-000-template.md) for the standard template when creating new patterns.

### Pattern Status Levels

- **Proven**: Established patterns with extensive usage
- **Emerging**: New patterns with initial validation
- **Experimental**: Patterns under active development
- **Deprecated**: Legacy patterns being phased out

### Product Relevance Classification

Every pattern should include a Product Relevance classification:

- **Process-only**: Useful for building Piper, not applicable to Piper's users
- **Portable**: Methodology that could become user-facing capability
- **Converged**: Pattern already implemented as product feature

When in doubt, default to "Process-only" — it can be reclassified later.

## Pattern Sweep Process

Pattern Sweeps occur every 6 weeks per the staggered audit calendar.

### Sweep Checklist (Product Relevance)

In addition to standard sweep activities, each sweep should:

- [ ] Review each pattern's Product Relevance classification
- [ ] Flag any "Process-only" patterns that should be reclassified as "Portable"
- [ ] Note any "Portable" patterns ready for product discussion

### Sweep Output Template Addition

Each Pattern Sweep results document should include:

```markdown
## Product Relevance Summary
- Portable patterns awaiting product review: [list]
- Patterns reclassified this sweep: [list]
- Converged patterns (methodology → product): [list]
```

## Related Resources

### Pattern Family Index

The **[Pattern Family Index](PATTERN-FAMILIES.md)** organizes patterns by how they work together. While this index (README.md) groups patterns by *category* (what they're about), the family index groups them by *family* (patterns that reinforce each other). Apply patterns in family units for best results.

### Proto-Pattern Registry

The **[Proto-Pattern Registry](PROTO-PATTERNS.md)** tracks emerging pattern candidates that need additional evidence before formalization. Proto-patterns are evaluated during 6-week pattern sweeps and promoted when they meet the evidence threshold.

### Anti-Pattern Index

The **[Anti-Pattern Index](../anti-pattern-index.md)** provides bidirectional navigation between patterns and their associated anti-patterns:

- **43 anti-patterns** across 5 categories (Grammar, Testing, Architecture, Process, Integration)
- Links from anti-patterns → patterns that address them
- Reverse index: patterns → anti-patterns they prevent
- Updated during 6-week pattern sweeps

Use the anti-pattern index to:
- Understand common pitfalls related to a pattern
- Find patterns that address a known problem
- Discover traps to avoid when implementing a pattern

## Navigation

- **[Main Documentation](../README.md)** - Return to main docs
- **[Anti-Pattern Index](../anti-pattern-index.md)** - Common pitfalls and traps
- **[Architecture Overview](../architecture/README.md)** - System architecture documentation
- **[Development Guides](../development/README.md)** - Developer resources

## Legacy References

- Original catalog: [../architecture/pattern-catalog.md](../architecture/pattern-catalog.md)
- Previous index: [archive/PATTERN-INDEX-legacy.md](archive/PATTERN-INDEX-legacy.md)

---

_Last updated: March 3, 2026_
_Added Human-AI Collaboration Referee (061); total now 62 patterns_
