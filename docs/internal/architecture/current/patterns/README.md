# Pattern Index

_Consolidated from pattern-catalog.md and PATTERN-INDEX.md_
_Format: ADR-style numbered patterns_

**Total Patterns**: 74 patterns (001-074), plus a template (000). Recent additions (2026-05-09 → 2026-05-24); all are now integrated into the category index below (this highlights box is a recent-filing snapshot, not the authoritative list):
- **Pattern-066 (Stacked Silent Failures)** Emerging — filed 2026-05-09 (CIO Pattern Sweep #1025 Phase 2C TRUE EMERGENCE finding)
- **Pattern-067 (Issue-Body Reality Mismatch)** Emerging — filed 2026-05-09 (Lead Dev; 3-of-5 evidence from M2f Group A+B dead-code dispositions same day)
- **Pattern-068 (Silent State Mutation in Shared Working Tree)** Emerging — filed 2026-05-11 (CIO; parent meta-pattern over P-13 branch-drift + P-15 residue-drift + P-16 index-drift + P-17 working-tree-path-fragmentation)
- **Pattern-069 (Coarse Triggers Causing False-Positive Triage Cost)** Emerging — filed 2026-05-11 (CIO; hook-design meta-pattern from PreCompact-hook two-incident thread)
- **Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene)** Emerging — filed 2026-05-15 (Architect; three-instance convergence May 2–5 across #1018 audit cleanup / #1035 composting / #1052 standup; Anthropic Dreams Type 1 consolidation as prospective Proven trigger; CIO co-signs methodology sidecar 12o "Pattern Formation via Successful Imitation")
- **Pattern-071 (Audit Logs as Attack Surface)** Emerging — filed 2026-05-15 (Lead Dev; sibling shape of Pattern-064 "Alive Scaffolding" — compliance-shaped scaffolding that actively amplifies leaks vs. passive scaffolding that does nothing; reference implementation #1017 `OutputFilterDecision` hash-only invariant + write-time guard; promotion to Proven contingent on 4-6 week cohort exposure surfacing no required exception path)
- **Pattern-072 (Registries that Grow into Architectural Shapes)** **Proven** — filed Emerging 2026-05-15 (Lead Dev); promoted to **Proven** 2026-05-16 (CIO) after #1094 ENGINE-DELETION close-out landed Slack handler dispatch as the fourth behavior-deciding consumer of the `task_type` registry, with all four formalization-discipline invariants intact. First sub-day Emerging-to-Proven promotion in the catalog (~6 hours between recognition trigger and Proven trigger).
- **Pattern-073 (Documentation-Asserted-Behavior Drift)** **Proven** (promoted 2026-05-18) — filed 2026-05-16 (Lead Dev; CIO methodology cosign). Six independent reference instances in ≤48 hours across five narrative-artifact layers (methodology docs / code docstrings / templated user-facing copy / orphan dependency / test fixture vs. classification / incomplete pattern translation). Pattern-064-adjacent sibling at the narrative layer: where Pattern-064 names code-that-looks-live-but-does-nothing, Pattern-073 names narrative-that-asserts-a-contract-the-code-doesn't-honor. Operational recognition discipline: `doc-sync-sweep` v0.1 skill at `.claude/skills/doc-sync-sweep/`. Promotion-to-Proven contingent on one more independent instance within 14 days + skill operating cleanly on a fresh-fix flow by an agent who didn't draft it.
- **Pattern-074 (Visibility Loss After Premature Retirement)** Emerging — filed 2026-05-24 (CIO per Comms seed memo `memo-comms-to-cio-cc-host-pa-pm-pattern-of-visibility-loss-lapses-plus-guards-2026-05-24.md`). Two reference instances logged within a single day (both Comms-side, May 24, 2026). Needs ≥1 more independent cross-role instance to graduate Emerging → Proven.

CIO carries the catalog-management authority; full index updates per category live below.

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
- [Pattern-064: Extension Without Integration](pattern-064-extension-without-integration.md) - Scaffolding that extends a surface without wiring into live behavior ("Alive Scaffolding") (Proven)
- [Pattern-071: Audit Logs as Attack Surface](pattern-071-audit-logs-as-attack-surface.md) - Compliance-shaped logging that amplifies leaks; write-time guard + hash-only invariant (Emerging)
- [Pattern-072: Registries that Grow into Architectural Shapes](pattern-072-registries-that-grow-into-architectural-shapes.md) - Registries accreting behavior-deciding consumers harden into architectural structures (Proven)

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
  - 44 total **intent-classification regex patterns** across TEMPORAL (17), STATUS (14), PRIORITY (13) — these belong to Pattern-032's intent-routing catalog, NOT the architecture-pattern catalog (see **Total Patterns** at the top of this file for the architecture-pattern count). Distinct count, distinct domain.
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
- [Pattern-070: Cleanup-Job-with-Cancellation-Hygiene](pattern-070-cleanup-job-with-cancellation-hygiene.md) - Cleanup/cancellation jobs need hygiene to avoid orphaned or double-processed state (Emerging)

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
- [Pattern-062: Assembly Assumption](pattern-062-assembly-assumption.md) - Multi-role convergence on shared artifacts (COORDINATION PATTERN; Methodology-Elevated → Flywheel Practice 5)
- [Pattern-063: Parallel-Authoring Drift](pattern-063-parallel-authoring-drift.md) - Two agents extend the same canonical reference concurrently, producing divergent versions (Proven; META-PATTERN)
- [Pattern-065: Continuity Memo Before the Seam](pattern-065-continuity-memo-before-the-seam.md) - Write the handoff/continuity memo before the discontinuity, not after (Proven; META-PATTERN)
- [Pattern-066: Stacked Silent Failures](pattern-066-stacked-silent-failures.md) - N layers each with a silent-failure mode compound into an undetected cascade (Emerging)
- [Pattern-067: Issue-Body Reality Mismatch](pattern-067-issue-body-reality-mismatch.md) - Issue body/checkbox state drifts from implementation reality (Emerging)
- [Pattern-068: Silent State Mutation in Shared Working Tree](pattern-068-silent-state-mutation-shared-working-tree.md) - Concurrent agents silently mutate shared git working-tree state (parent meta-pattern over branch/index/residue/path drift) (Emerging)
- [Pattern-069: Coarse Triggers Causing False-Positive Triage Cost](pattern-069-coarse-triggers-false-positive-triage-cost.md) - Hook/trigger granularity too coarse generates false-positive triage load (Emerging)
- [Pattern-073: Documentation-Asserted-Behavior Drift](pattern-073-documentation-asserted-behavior-drift.md) - Documentation asserts a contract the code no longer honors (Proven)
- [Pattern-074: Visibility Loss After Premature Retirement](pattern-074-visibility-loss-after-premature-retirement.md) - Retiring a tracker/surface before its function is replaced loses visibility (Emerging)

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
- **Methodology-Elevated**: A Proven pattern whose underlying principle has graduated *out* of the pattern catalog and into the methodology corpus as a named principle or practice. The pattern entry remains as the catalog record of origin; the methodology entry becomes the canonical, actively-cited form. This is a promotion, not a deprecation — it marks a diagnostic vocabulary item maturing into a standing principle the cohort applies by default. **Exemplar**: Pattern-062 (Assembly Assumption) → Excellence Flywheel v2.0 Practice 5 ("Audit the Composition"). **Retroactive candidates**: Pattern-045 (Green Tests, Red User), Pattern-049 (Audit Cascade) — both diagnostic-vocabulary patterns that now function as standing methodology principles. (Term coined in the Pattern Sweep 2.0 report, 2026-05-09; formalized 2026-05-28 per PM ratification. Recognition criterion: the pattern's principle appears as a named entry/practice in `docs/internal/development/methodology-core/` or the Excellence Flywheel, and the methodology form is the one the cohort cites.)

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
- **[Architecture Overview](../architecture.md)** - System architecture documentation
- **[Development Guides](../../../development/README.md)** - Developer resources

## Legacy References

- Original catalog: `pattern-catalog.md` (consolidated into this README; file removed)
- Previous index: [archive/PATTERN-INDEX-legacy.md](archive/PATTERN-INDEX-legacy.md)

---

_Last updated: 2026-07-08 (Docs audit — added Pattern-074 to recent-additions list; footer count corrected)_
_Total: 74 patterns (001-074) plus template (000). Previous footer noted 62 (as of 2026-03-03, when pattern-061 was last addition tracked here)._
