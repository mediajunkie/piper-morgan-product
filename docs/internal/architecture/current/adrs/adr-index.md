# Architectural Decision Records (ADR) Index

**Last Updated**: 2026-05-16 (ADR-061 + ADR-062 + ADR-063 + ADR-064 entries added; full index reconciliation pending)
**Total ADRs**: 67 (000-064, excluding field-mapping-report and this index)
**Status**: Active

## Overview

This index provides a complete catalog of all Architectural Decision Records (ADRs) in the Piper Morgan system. ADRs document important architectural decisions, their context, rationale, and consequences.

## ADR Catalog

### Foundation & Core Platform

- [ADR-000: Meta-Platform](adr-000-meta-platform.md) - Core platform architecture foundation
- [ADR-045: Object Model - "Entities Experience Moments in Places"](adr-045-object-model.md) - Foundational grammar for Piper's consciousness ("Entities experience Moments in Places")
- [ADR-046: Moment Type Agent Architecture](adr-046-moment-type-agent-architecture.md) - Typed input decomposition and specialized agent routing for coordination

### Integration & Communication

- [ADR-001: MCP Integration](adr-001-mcp-integration.md) - Model Control Protocol integration
- [ADR-002: Claude Code Integration](adr-002-claude-code-integration.md) - Claude Code agent integration
- [ADR-013: MCP + Spatial Intelligence Integration Pattern](adr-013-mcp-spatial-integration-pattern.md) - Spatial intelligence integration

### Service Enhancement & Features

- [ADR-003: Intent Classifier Enhancement](adr-003-intent-classifier-enhancement.md) - Intent classification improvements
- [ADR-004: Action Humanizer Integration](adr-004-action-humanizer-integration.md) - Human-readable action formatting
- [ADR-014: Attribution First](adr-014-attribution-first.md) - Attribution-based architecture
- [ADR-015: Wild Claim](adr-015-wild-claim.md) - Wild claim handling approach
- [ADR-016: Ambiguity Driven](adr-016-ambiguity-driven.md) - Ambiguity-driven design decisions

### Data & Repository Management

- [ADR-005: Eliminate Dual Repository Implementations](adr-005-eliminate-dual-repository-implementations.md) - Repository pattern standardization
- [ADR-006: Standardize Async Session Management](adr-006-standardize-async-session-management.md) - Session management patterns
- [ADR-025: Unified Session Management Architecture](adr-025-unified-session-management.md) - Comprehensive session management
- [ADR-041: Domain Primitives - Item and List Refactoring](adr-041-domain-primitives-refactoring.md) - Polymorphic inheritance with Item/List as universal primitives
- [ADR-055: Object Model Implementation](adr-055-object-model-implementation.md) - Core Grammar & Lens Infrastructure for the object model

### Infrastructure & Operations

- [ADR-007: Staging Environment Architecture](adr-007-staging-environment-architecture.md) - Staging environment design
- [ADR-008: MCP Connection Pooling Production](adr-008-mcp-connection-pooling-production.md) - Connection pooling strategy
- [ADR-009: Health Monitoring System](adr-009-health-monitoring-system.md) - System health monitoring
- [ADR-010: Configuration Patterns](adr-010-configuration-patterns.md) - Configuration management
- [ADR-012: Protocol Ready JWT Authentication](adr-012-protocol-ready-jwt-authentication.md) - Authentication architecture
- [ADR-027: Configuration Architecture: User vs. System Separation](adr-027-configuration-architecture-user-vs-system-separation.md) - Configuration architecture (may partly supersede ADR-010?)
- [ADR-040: Local Database Per Environment](adr-040-local-database-per-environment.md) - CODE ≠ DATA architecture (git-managed code, PostgreSQL per environment data)
- [ADR-044: Lightweight RBAC vs Traditional](adr-044-lightweight-rbac-vs-traditional.md) - Security architecture for role-based access control
- [ADR-057: CommandRegistry](adr-057-command-registry.md) - Unified command discovery and routing
- [ADR-058: Multi-Tenancy Isolation](adr-058-multi-tenancy-isolation.md) - Multi-tenancy isolation architecture
- [ADR-059: Workflow Dispatcher & Offer Consolidation](adr-059-workflow-dispatcher-offer-consolidation.md) - Unified dispatch replacing per-handler workflow management
- [ADR-060: Floor-First Routing](adr-060-floor-first-routing.md) - Invert routing: floor handles everything, handlers prove specificity
- [ADR-061: LLM-Touch Boundary Enforcement](adr-061-llm-touch-boundary-enforcement.md) - Two-layer detection (literal-trigger + semantic) with floor as de-facto ethics layer; four-element principle (permissive input / schema validation / safe-fallback / audit envelope); v1.1 output-side companion per #1017
- [ADR-062: Project-Scope End-to-End Suite](adr-062-project-scope-e2e-suite.md) - Generalizing ADR-061 simulation harness; four-layer architecture (probe registry / harness orchestration / disagreement table / reporting+CI) + five-phase sequence (Phase 0 scoping → cross-host gated by BYOC ship); Phase 1+ trigger-gated
- [ADR-063: User-Facing Audit Envelope Read Surface](adr-063-user-facing-audit-envelope-read-surface.md) - ADR-061 READ-side companion; four-element READ-side principle (user-visible field set / schema validation / safe-fallback / JWT-bound access control); codifies #1095 Pattern-071 first fix as architecture; Surface 7 paired with MUX doc (CXO + Comms lane)
- [ADR-064: Project-Scope Search Index Architecture](adr-064-project-scope-search-index-architecture.md) - Pre-1.0 Architect-lane commitment for Surface 5 (post-1.0); layered Postgres FTS + ChromaDB storage; per-surface IndexDeclaration registry (Pattern-072 4th application); query-time access control; BYOC forward-compatible

### Testing & Quality Assurance

- [ADR-011: Test Infrastructure Hanging Fixes](adr-011-test-infrastructure-hanging-fixes.md) - Test infrastructure reliability
- [ADR-023: Test Infrastructure Activation](adr-023-test-infrastructure-activation.md) - Test activation patterns

### Spatial Intelligence & Advanced Features

- [ADR-013: MCP + Spatial Intelligence Integration Pattern](adr-013-mcp-spatial-integration-pattern.md) - Spatial intelligence integration
- [ADR-017: Spatial MCP](adr-017-spatial-mcp.md) - Spatial MCP implementation
- [ADR-018: Server Functionality](adr-018-server-functionality.md) - Server capability architecture
- [ADR-019: Orchestration Commitment](adr-019-orchestration-commitment.md) - Orchestration strategy
- [ADR-020: Protocol Investment](adr-020-protocol-investment.md) - Protocol investment decisions
- [ADR-021: Multi Federation](adr-021-multi-federation.md) - Multi-federation architecture
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) - Two validated spatial patterns (Granular Adapter, Embedded Intelligence)
- [ADR-042: Mobile Strategy - Progressive Enhancement](adr-042-mobile-strategy-progressive-enhancement.md) - Mobile development strategy
- [ADR-056: Consciousness Expression Patterns](adr-056-consciousness-expression-patterns.md) - Consciousness expression patterns for entity awareness

### Core Patterns & Workflows

- [ADR-043: Application-Layer Stored Procedures](adr-043-application-layer-stored-procedures.md) - Multi-step workflow composition at application layer instead of database layer

### Experimentation & Innovation

- [ADR-022: Autonomy Experimentation](adr-022-autonomy-experimentation.md) - Autonomous system experiments
- [ADR-024: Persistent Context Architecture](adr-024-persistent-context-architecture.md) - Context persistence design

### External Integrations

- [ADR-026: Notion Client Migration](adr-026-notion-client-migration.md) - Migration to official Notion client library

### Methodological Architecture

- [ADR-028: Three-Tier Verification Pyramid](adr-028-verification-pyramid.md) - Foundational framework for all agent coordination, requiring systematic evidence at each level before proceeding

## ADR Status Summary

- **Total**: 61 ADRs (000-058)
- **Accepted**: ~55 ADRs
- **Proposed/Draft**: ~6 ADRs
- **Superseded**: 0 ADRs
- **Deprecated**: 0 ADRs

## ADR Guidelines

### Creating New ADRs

1. Use next sequential number (next: ADR-059)
2. Follow naming convention: `adr-XXX-descriptive-title.md`
3. Include required sections: Status, Date, Context, Decision, Consequences
4. Update this index when adding new ADRs

### ADR Lifecycle

- **Proposed**: Initial draft, under review
- **Accepted**: Decision approved and implemented
- **Superseded**: Replaced by newer ADR
- **Deprecated**: No longer applicable

## Recent Changes

- **March 3, 2026**: Docs audit — added ADR-042, ADR-044, ADR-055, ADR-056, ADR-057, ADR-058 to catalog (existed as files but missing from index). Total now 61.
- **January 13, 2026**: Added ADR-053 (Trust Computation Architecture), ADR-054 (Cross-Session Memory Architecture) - Trust gradient and memory persistence from PDR-002; Updated ADR-052 (Tool-Based MCP Standardization)
- **January 13, 2026**: Added ADR-050 (Conversation-as-Graph Model), ADR-051 (Unified User Session Context) - Multi-party conversation modeling and user context unification
- **January 9, 2026**: Added ADR-049 (Conversational State and Hierarchical Intent) - Multi-turn conversation architecture from FTUX-PORTFOLIO
- **January 4, 2026**: Added ADR-048 (ServiceContainer Lifecycle Management) - Singleton pattern and lifecycle management from ARCH-FIX-SINGLETON
- **December 3, 2025**: Added ADR-047 (Async Event Loop Awareness) - Database connection event loop handling from setup wizard debugging
- **October 17, 2025**: Added ADR-052 (Tool-Based MCP Standardization) - MCP implementation standardization from CORE-MCP-MIGRATION
- **November 30, 2025**: Added ADR-046 (Micro-Format Agent Architecture) - Typed input decomposition and specialized agent routing for coordination; emerges from Ted Nadeau's advisor mailbox insights
- **November 29, 2025**: Added ADR-045 (Object Model - "Entities Experience Moments in Places") - Foundational conceptual grammar establishing how Piper perceives the world through Entities, Places, Moments, and Situations - Total was 46 ADRs (000-045)
- **November 24, 2025**: Added ADR-044 (Lightweight RBAC vs Traditional) - Security architecture decision for role-based access control
- **November 22, 2025**: Added ADR-043 (Application-Layer Stored Procedures) - Documents Piper's stored procedure pattern at application layer (orchestration, workflows, intent handlers) - Total was 43 ADRs (000-043)
- **November 4, 2025**: Added ADR-041 (Domain Primitives - Item and List Refactoring) - Polymorphic inheritance with Item/List as universal primitives - Total was 42 ADRs (000-041)
- **November 4, 2025**: Added ADR-040 (Local Database Per Environment) - CODE ≠ DATA architecture for Sprint A8 P0 blockers
- **October 13, 2025**: Updated index with ADR-037, ADR-038, ADR-039 (PROOF-8 audit) - Total was 42 ADRs
- **October 7, 2025**: Added ADR-039 (Canonical Handler Fast-Path Pattern) - Dual-path intent architecture from GREAT-4
- **October 2-4, 2025**: Updated ADR-034 (Plugin Architecture) with implementation verification (GREAT-3)
- **September 30, 2025**: Added ADR-038 (Spatial Intelligence Architecture Patterns) - Three validated spatial patterns from GREAT-2
- **September 22, 2025**: Added ADR-037 (Test-Driven Locking Strategy) and ADR-036 (QueryRouter Resurrection) from GREAT-1

## Related Documentation

- [Architecture Overview](../architecture.md)
- [Domain Models Index](../models/domain-models-index.md)
- [Pattern Catalog](../patterns/README.md)
- [Technical Specifications](../technical-spec.md)
- [ADR-029: Domain Service Mediation Architecture](adr-029-domain-service-mediation-architecture.md) - Complete domain service mediation for external system access
- [ADR-030: Configuration Service Centralization](adr-030-configuration-service-centralization.md) - Centralized configuration management through PortConfigurationService
- [ADR-031: MVP Redefinition](adr-031-mvp-redefinition.md) - Core vs Feature MVP distinction for strategic development
- [ADR-032: Intent Classification Universal Entry](adr-032-intent-classification-universal-entry.md) - Intent classification as universal conversation entry point
- [ADR-033: Multi-Agent Deployment](adr-033-multi-agent-deployment.md) - Multi-agent coordination scripts deployment strategy
- [ADR-034: Plugin Architecture](adr-034-plugin-architecture.md) - Extensible plugin architecture for PM tool integration
- [ADR-035: Inchworm Protocol](adr-035-inchworm-protocol.md) - Sequential execution methodology
- [ADR-036: QueryRouter Resurrection Strategy](adr-036-queryrouter-resurrection.md) - Complete and reenable QueryRouter
- [ADR-037: Test-Driven Locking Strategy](adr-037-test-driven-locking.md) - Lock critical infrastructure with tests
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) - Three validated spatial patterns (Granular, Embedded, Delegated MCP)
- [ADR-039: Canonical Handler Fast-Path Pattern](adr-039-canonical-handler-pattern.md) - Dual-path architecture for intent classification
- [ADR-040: Local Database Per Environment](adr-040-local-database-per-environment.md) - CODE ≠ DATA architecture (git-managed code, PostgreSQL per environment data)
- [ADR-043: Application-Layer Stored Procedures](adr-043-application-layer-stored-procedures.md) - Application-layer workflow composition pattern through OrchestrationEngine, WorkflowFactory, and IntentService (supports ADR-019)
- [ADR-047: Async Event Loop Awareness](adr-047-async-event-loop-awareness.md) - Database connection event loop handling for CLI/HTTP contexts
- [ADR-048: ServiceContainer Lifecycle Management](adr-048-service-container-lifecycle.md) - Singleton pattern and lazy initialization for service container
- [ADR-049: Conversational State and Hierarchical Intent](adr-049-conversational-state-hierarchical-intent.md) - Multi-turn conversation architecture
- [ADR-050: Conversation-as-Graph Model](adr-050-conversation-as-graph-model.md) - Multi-party, multi-agent conversational modeling
- [ADR-051: Unified User Session Context](adr-051-unified-user-session-context.md) - Unifying user_id and session_id patterns
- [ADR-052: Tool-Based MCP Standardization](adr-052-tool-based-mcp-standardization.md) - Standardize on tool-based MCP implementation
- [ADR-053: Trust Computation Architecture](adr-053-trust-computation-architecture.md) - Trust gradient model implementation from PDR-002
- [ADR-054: Cross-Session Memory Architecture](adr-054-cross-session-memory-architecture.md) - Three-layer context persistence model from PDR-002
- [ADR-071: User-Auth Anchoring Pattern for Content Stores](adr-071-user-auth-anchoring-pattern.md) - Canonical principal-anchoring (owner_id FK canonical; user_id string deprecated; none forbidden); principal threaded from the host boundary (D4); from the #1241 audit. Companion to ADR-058 at content altitude.
- [ADR-072: Skill-Routing Architecture — Fluid Model with Defense-in-Depth](adr-072-skill-routing-architecture.md) - Five decisions (D1–D5) for routing PM skills across native path (Claude Desktop/Code) vs plugin path (MCP); fluid model with defense-in-depth; D5 ratified 2026-06-17 with CXO + HOST trust-lens (gate Piper-initiated, never user-reaching-for-own; HOST consequential-action carve-out; transparency-when-gated). Related: ADR-059 (PIPER.md accuracy), ADR-070 (Connector Architecture).
- [ADR-073: No Destructive Git in PM's Main Checkout Working Tree](adr-073-no-destructive-git-in-pm-main-checkout.md) - Operational hard-rule (PM-approved 2026-06-27); never destructive git (`checkout -- .` / `reset --hard` / `stash`) in PM's live workspace — agents commit from their own worktree, MANIFEST noise cleared by surgical path only. Structurally enforced (CLAUDE.md callout + #1259 push-to-ref + check-branch hook). From the 6/21 data-loss incident; m-41 case.
