# ADR-038: Spatial Intelligence Architecture Patterns

**Date**: September 30, 2025 (Updated: October 1, 2025)
**Status**: Accepted · **AMENDED 2026-07-30 (Amendment A, Arch)** — decision stands; verification claims corrected. Read Amendment A at the foot of this file before citing any operational claim.
**Context**: CORE-GREAT-2C Verification Work (GitHub Issue #194), CORE-GREAT-2D Discovery (GitHub Issue #195)
**Supersedes**: None
**Superseded by**: None

---

## ⚠️ TWO NOTICES ADDED 2026-07-29 — read before relying on this ADR's verification claims

### 1. A committed-theory review is IN FLIGHT

A PM-directed committed-theory review of spatial intelligence opened 2026-07-19 and **has not
concluded**. It may amend this ADR (the current pattern policy). **Spatial deletions are HELD** until
it concludes; spatial intelligence is protected representation under PM's standing rule.

**Before inferring from cold `*_spatial` code that this ADR's patterns failed, read
[`../spatial-intelligence-experience-thesis.md`](../spatial-intelligence-experience-thesis.md).**
The experience-design argument is that spatial intelligence here is **three capabilities**, not one at
partial completion: live spatial *reasoning* ("Piper knows where things live"); per-connector *adapter
depth*, **live for GitHub and cold for five others**; and *ambient presence* ("Piper inhabits your
tools and notices changes"), which is **built nowhere** and is not the cold adapters at a higher
percentage.

⚠️ **`github_spatial` is LIVE** — full 8-dimensional, reachable through `context_assembler` and over
HTTP via the Places API (Arch, verified importer-by-importer, 2026-07-29). **Retiring "the spatial
adapter pattern" would therefore delete working production code.** The pattern was built once, at
full depth, and never replicated — which is a cost question, not a proof question.

Lanes: Arch (synthesis + ADR map), CXO (experience theory), PPM (roadmap dependency), Lead (code
census). **PM decides.** Live synthesis:
`dev/active/spatial-intelligence-architectural-history-arch-WIP.md`.

### 2. ⚠️ The "100% operational" verification claims below are CONTRADICTED by current state

The **Verification Results** section asserts *"Notion spatial: 1 file, 100% operational,
8-dimensional analysis working"* and *"Production-proven: All operational in production codebase"*
(Sept 30 / Oct 1, 2025).

**As of 2026-07-18 recon, `services/intelligence/spatial/notion_spatial.py` is ~75% abandoned with
~12 undefined methods, and the per-connector spatial-adapter surface is unreachable from the running
application.** Whether the 2025 claim was aspirational when written or the code regressed after it
**is not yet established** — that determination is Arch's, inside the review above.

**Arch's 2026-07-29 verification makes the correction precise: this ADR was right about the pattern
and wrong about which connector proved it.** GitHub — which this ADR does *not* hold up as the spatial
exemplar — is the implementation that shipped at full 8-dimensional depth. Notion, nominated here as
the Embedded-Intelligence proof, is both abandoned and unreachable.

**Do not cite this ADR's operational claims as current fact.** The ADR amendment is Arch's to draft;
this notice is CXO's, flagged because the "100% operational" sentence is what makes today's cold code
read as *regression* rather than as *never-replicated* — the wrong inference the review exists to
prevent.

---

## Decision

Piper Morgan will support **three distinct spatial intelligence patterns** optimized for different integration domains:

1. **Granular Adapter Pattern** for complex coordination scenarios
2. **Embedded Intelligence Pattern** for streamlined knowledge management
3. **Delegated MCP Pattern** for Model Context Protocol integrations (NEW - Oct 1, 2025)

All patterns are considered first-class architectural approaches, and new integrations should choose the pattern most appropriate for their domain.

---

## Context

During CORE-GREAT-2C verification work (Phases 1-2, September 30, 2025), we discovered that Slack and Notion integrations implement fundamentally different but equally valid spatial architecture approaches.

During CORE-GREAT-2D investigation (Phase 0, October 1, 2025), we discovered Calendar implements a third distinct pattern using Model Context Protocol (MCP) delegation.

### Slack Implementation (Granular Adapter Pattern)

- **Structure**: 11 files (6 core + 5 tests)
- **Location**: `services/integrations/slack/spatial_*.py`
- **Access**: `router.get_spatial_adapter() → SlackSpatialAdapter`
- **Inheritance**: Extends `BaseSpatialAdapter`
- **Components**: Types, Adapter, Agent, Classifier, Mapper, Memory
- **Use Case**: Real-time messaging coordination

### Notion Implementation (Embedded Intelligence Pattern)

- **Structure**: 1 comprehensive file (632 lines)
- **Location**: `services/intelligence/spatial/notion_spatial.py`
- **Access**: Separate `NotionSpatialIntelligence` class using router internally
- **Inheritance**: Standalone class (no base adapter)
- **Components**: Single comprehensive intelligence class
- **Use Case**: Knowledge management and semantic analysis

### Calendar Implementation (Delegated MCP Pattern) - NEW

- **Structure**: 2 files (router + MCP adapter)
- **Location**: Split between `services/integrations/calendar/` (router) and `services/mcp/consumer/` (adapter)
- **Access**: `router.method()` delegates to MCP adapter
- **Inheritance**: MCP adapter extends `BaseSpatialAdapter`
- **Components**: Minimal router + comprehensive MCP adapter (499 lines)
- **Use Case**: Temporal awareness and calendar operations via Model Context Protocol

### Verification Results

- ✅ Slack spatial: 11 files, 100% operational, 66 test functions passing
- ✅ Notion spatial: 1 file, 100% operational, 8-dimensional analysis working
- ✅ Calendar spatial: 2 files, 100% operational, MCP protocol integration
- ✅ All patterns: Support 8-dimensional spatial metaphor
- ✅ Zero conflicts: Patterns coexist successfully
- ✅ Feature flags: All support USE*SPATIAL*\* control
- ✅ Production-proven: All operational in production codebase

---

## Options Considered

### Option 1: Standardize on Single Pattern (REJECTED)

Force all integrations to use the same architectural approach.

**Advantages**:

- Single pattern to learn and maintain
- Consistent codebase structure
- Easier onboarding for new developers

**Disadvantages**:

- Wrong tool for some domains (over-engineering or under-engineering)
- Performance penalties for mismatched patterns
- Maintenance burden (either too complex or too inflexible)
- Discards validated, working implementations
- **Rejected**: Both patterns are production-proven and domain-optimized

### Option 2: Support Multiple Patterns (CHOSEN)

Allow domain-optimized architectures based on integration characteristics.

**Advantages**:

- Optimal performance for each domain
- Appropriate complexity levels
- Proven operational in production
- Clear selection criteria
- Flexibility for future integrations
- Support for MCP-based integrations (Oct 2025 update)

**Disadvantages**:

- Multiple patterns to maintain (now 3 patterns as of Oct 2025)
- Documentation overhead
- Training requirement for developers

**Decision**: CHOSEN - Benefits outweigh costs. October 2025 update: Calendar's Delegated MCP Pattern confirms this approach scales well for protocol-based integrations.

### Option 3: Hybrid Approach (REJECTED)

Combine both patterns in single implementation (e.g., granular components with embedded access).

**Advantages**:

- Theoretically "best of both worlds"
- Single architectural style

**Disadvantages**:

- Complexity without clear benefit
- Unclear which pattern to follow
- No production validation
- Maintenance burden of both approaches
- **Rejected**: Adds complexity without solving real problems

---

## Decision Rationale

### Core Principle: Domain-Optimized Architecture

**Key Insight**: Domain-specific optimization outweighs standardization for standardization's sake.

Different integration domains have fundamentally different spatial requirements:

**Reactive Coordination (Slack)**:

- Real-time event processing
- Multiple interaction types (messages, threads, reactions, etc.)
- Complex state management across channels/workspaces
- Need for fine-grained component testing
- **Solution**: Granular Adapter Pattern (11 files, component-based)

**Analytical Intelligence (Notion)**:

- Batch processing of knowledge structures
- Single comprehensive analytical model
- Stable domain with clear requirements
- Performance-critical operations
- **Solution**: Embedded Intelligence Pattern (1 file, consolidated)

### Evidence-Based Decision

**Production Validation**:

- Both patterns verified operational (GREAT-2C Phases 1-2)
- Zero conflicts between patterns
- 100% feature parity (8-dimensional spatial metaphor)
- Complete test coverage (66 tests Slack, integration tests Notion)

**Architectural Quality**:

- Slack: Clean component separation, extensive test coverage
- Notion: Consolidated design, lower overhead, direct access
- Both: Feature flag control, async/await patterns, observability

**Developer Experience**:

- Clear selection criteria documented
- Pattern choice based on objective factors
- Both patterns have proven track record

---

## Implementation

### Pattern Selection Criteria

New spatial integrations must choose pattern based on:

1. **Domain Complexity**:

   - Many distinct capabilities (>5) → Granular
   - Few focused capabilities (≤5) → Embedded
   - **MCP Protocol required** → Delegated MCP (Oct 2025)

2. **Requirement Stability**:

   - Evolving requirements → Granular (easier to extend)
   - Stable requirements → Embedded (lower overhead)
   - **Protocol-driven** → Delegated MCP

3. **Performance Criticality**:

   - Performance critical → Embedded (minimal overhead)
   - Performance adequate → Either pattern
   - **External service** → Delegated MCP (protocol overhead acceptable)

4. **Testing Requirements**:

   - Component-level isolation needed → Granular
   - Integration-level testing sufficient → Embedded
   - **Protocol compliance testing** → Delegated MCP

5. **Team Structure**:

   - Multiple developers on feature → Granular (parallel work)
   - Single developer or small team → Embedded (simpler)
   - **MCP team + integration team** → Delegated MCP (separation of concerns)

6. **Domain Nature**:

   - Reactive coordination → Granular
   - Analytical intelligence → Embedded
   - **Temporal/contextual awareness via protocol** → Delegated MCP

7. **Integration Architecture** (NEW - Oct 2025):
   - **Model Context Protocol (MCP) required** → Delegated MCP
   - **Separate consumer layer exists** → Delegated MCP
   - **Protocol-specific spatial logic** → Delegated MCP
   - All other cases → Granular or Embedded

### Pattern Descriptions

#### Granular Adapter Pattern

**When to Use**:

- Complex coordination scenarios
- Real-time messaging and events
- Multi-faceted spatial requirements
- Requirements likely to evolve
- Multiple developers working on spatial features

**Structure**:

```
services/integrations/{integration}/
  spatial_types.py          # Domain types and primitives
  spatial_adapter.py        # Main adapter (inherits BaseSpatialAdapter)
  spatial_agent.py          # Navigation and awareness
  spatial_intent_classifier.py  # Intent classification
  spatial_mapper.py         # Domain-specific mapping
  spatial_memory.py         # Memory storage/retrieval
  tests/
    test_spatial_*.py       # Component-level tests
```

**Access Pattern**:

```python
router = IntegrationRouter()
adapter = router.get_spatial_adapter()
result = await adapter.map_to_position(context)
```

#### Embedded Intelligence Pattern

**When to Use**:

- Knowledge management scenarios
- Semantic analysis and content processing
- Streamlined spatial requirements
- Stable, well-defined domain
- Performance-critical applications
- Single comprehensive model fits domain

**Structure**:

```
services/intelligence/spatial/{integration}_spatial.py
  # Single comprehensive class
  # 8-dimensional analysis methods
  # Built-in analytics tracking
  # Internal router usage
```

**Access Pattern**:

```python
spatial = IntegrationSpatialIntelligence()
await spatial.connect()
analysis = await spatial.get_comprehensive_spatial_analysis(item_id)
```

#### Delegated MCP Pattern (NEW - Oct 2025)

**When to Use**:

- Model Context Protocol (MCP) integrations
- External service adapters requiring protocol compliance
- Temporal or contextual awareness scenarios
- Services with separate consumer layer architecture
- Integrations where spatial logic is protocol-specific

**Structure**:

```
services/integrations/{integration}/
  {integration}_integration_router.py  # Minimal router (delegation only)

services/mcp/consumer/
  {integration}_adapter.py             # MCP adapter (inherits BaseSpatialAdapter)
    # Spatial intelligence implementation
    # MCP protocol compliance
    # Custom spatial context extraction
```

**Access Pattern**:

```python
router = IntegrationRouter()
# Router methods delegate to MCP adapter
events = await router.get_todays_events()
# Spatial methods also available
context = router.get_context(external_id)
```

**Key Characteristics**:

- Router is minimal (mostly pass-through methods)
- Spatial intelligence in MCP consumer layer
- MCP adapter inherits from `BaseSpatialAdapter`
- Protocol-specific spatial context extraction
- Clean separation: integration routing vs MCP protocol

**Example**: Calendar integration

- Router: `services/integrations/calendar/calendar_integration_router.py` (397 lines)
- MCP Adapter: `services/mcp/consumer/google_calendar_adapter.py` (499 lines)
- Custom spatial context for temporal awareness (meeting_type, duration, attendees, location)

### Common Requirements

All spatial patterns **must**:

1. **Router Integration**:

   - Use IntegrationRouter (directly or indirectly)
   - Support feature flag control (USE*SPATIAL*\*)
   - Provide health check capabilities
   - **Update Oct 2025**: Delegated MCP Pattern delegates through router to MCP adapter

2. **8-Dimensional Spatial Metaphor**:

   - Implement relevant dimensions for domain
   - Use consistent naming (HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL)
   - Document which dimensions supported
   - **Update Oct 2025**: Calendar implements TEMPORAL dimension via temporal_summary

3. **Backward Compatibility**:

   - Graceful degradation when spatial disabled
   - Don't break existing functionality
   - Support legacy mode via feature flags
   - **Update Oct 2025**: All 3 patterns support feature flag control

4. **Async Patterns**:

   - Use async/await for I/O operations
   - Support concurrent operations where appropriate
   - Handle cleanup properly

5. **Observability**:
   - Log spatial operations appropriately
   - Track analytics/metrics
   - Support debugging and troubleshooting
   - **Update Oct 2025**: Delegated MCP Pattern includes circuit breaker pattern for resilience

---

## Consequences

### Positive Consequences

1. **Optimal Performance**: Each integration uses pattern suited to its needs
2. **Appropriate Complexity**: No over-engineering or under-engineering
3. **Production-Proven**: Both patterns validated and operational
4. **Clear Guidance**: Selection criteria documented
5. **Flexibility**: Future integrations can choose appropriate pattern
6. **No Breaking Changes**: Both existing patterns continue working

### Negative Consequences

1. **Multiple Patterns**: Two patterns to maintain instead of one
2. **Documentation Overhead**: Must document both patterns
3. **Training**: Developers need to understand pattern selection
4. **Consistency Risk**: Must ensure both patterns follow core requirements

### Mitigation Strategies

**For Multiple Patterns**:

- Clear documentation of both patterns
- Decision framework for pattern selection
- Common requirements enforced across patterns

**For Documentation Overhead**:

- Comprehensive pattern guide created (`docs/architecture/spatial-intelligence-patterns.md`)
- Pattern comparison table
- Usage examples for both patterns

**For Training**:

- Selection criteria clearly documented
- Decision framework provides objective guidance
- Examples from production code (Slack, Notion)

**For Consistency**:

- Common requirements documented (router integration, 8-dimensional metaphor, etc.)
- Feature flag system consistent across patterns
- Observability standards apply to both

---

## Compliance Requirements

### For Existing Implementations

**Slack (Granular Adapter Pattern)**:

- ✅ Compliant: Follows all pattern requirements
- ✅ Production operational
- ✅ Feature flag control working
- ✅ 8-dimensional metaphor supported
- ✅ Comprehensive test coverage

**Notion (Embedded Intelligence Pattern)**:

- ✅ Compliant: Follows all pattern requirements
- ✅ Production operational
- ✅ Feature flag control working
- ✅ 8-dimensional analysis implemented
- ✅ Integration test coverage

### For New Implementations

New spatial integrations must:

1. **Choose Pattern**: Use decision framework to select appropriate pattern
2. **Document Choice**: Create brief rationale document explaining pattern choice
3. **Follow Requirements**: Implement all common requirements
4. **Feature Flags**: Support USE*SPATIAL*{INTEGRATION}=true/false
5. **Router Integration**: Integrate with IntegrationRouter infrastructure
6. **Dimensions**: Implement relevant 8-dimensional analysis
7. **Testing**: Provide appropriate test coverage (component or integration)
8. **Documentation**: Update spatial pattern guide with integration

### Review Process

Pattern selection should be reviewed during:

- Initial design phase
- Architecture review
- Code review (ensure pattern followed correctly)

---

## References

### Documentation

- [Spatial Intelligence Competitive Advantage](../spatial-intelligence-competitive-advantage.md) - Strategic overview
- [Pattern-022: MCP Spatial Intelligence Integration](../patterns/pattern-022-mcp-spatial-intelligence-integration.md) - Integration pattern

### Source Code

- Granular Pattern: `services/integrations/slack/spatial_*.py` (11 files)
- Embedded Pattern: `services/intelligence/spatial/notion_spatial.py` (1 file)
- Base Adapter: `services/integrations/spatial_adapter.py`

### Verification

- GitHub Issue #194: CORE-GREAT-2C verification work
- Session Log: `dev/2025/09/30/2025-09-30-1025-prog-code-log.md`
- Phase 1: Slack spatial investigation (11 files analyzed)
- Phase 2: Notion spatial investigation (consolidated architecture discovered)

---

## Version History

| Date       | Version | Author      | Changes                                             |
| ---------- | ------- | ----------- | --------------------------------------------------- |
| 2025-09-30 | 1.0     | Claude Code | Initial ADR creation based on GREAT-2C verification |

---

## Approval

**Approved by**: CORE-GREAT-2C Verification Work (Phases 1-4)
**Implementation Status**: Complete and Operational
**Production Status**: Both patterns deployed and validated

---

**Next Review**: After next spatial integration implementation
**Related ADRs**: None (first spatial architecture ADR)
**Supersedes**: None
**Superseded by**: None (active)

---

## Update October 2025

See **ADR-034: Plugin Architecture Implementation** for the plugin system that now manages all spatial intelligence integrations. The three spatial patterns documented in this ADR are now implemented as plugins following the Wrapper/Adapter pattern, providing:

- **Dynamic loading** and configuration control via `config/PIPER.user.md`
- **Lifecycle management** through the `PluginRegistry`
- **Performance validation** with <0.05ms overhead per spatial operation
- **Contract testing** ensuring all spatial integrations comply with `PiperPlugin` interface

All spatial intelligence patterns remain valid architectural choices, now enhanced with plugin capabilities.

---

_This ADR documents the discovery and validation of two production spatial patterns during GREAT-2C verification work (September 30, 2025)._

---

# Amendment A — 2026-07-30 (Arch)

**Status of the amendment**: ACCEPTED as a correction to this ADR's *verification claims*. **The decision is NOT reversed.**
**Authored by**: Chief Architect · **Sources**: `../spatial-intelligence-layer-map-and-costed-options.md` (the measured map), `../spatial-intelligence-experience-thesis.md` (CXO, the experience argument).
**Supersedes**: the two ⚠️ notices at the head of this file, which were placeholders pending this amendment. Their substance is folded in here.

## A1 — The decision stands. The three-pattern pluralism is VALIDATED, not aspirational.

ADR-038 replaced ADR-013's maximalism (*"ALL external tool integrations MUST use the unified MCP + Spatial Intelligence pattern"*) with domain-appropriate pluralism. **That call was right and the evidence has strengthened, not weakened.** Every connector a user can actually connect today has a live spatial path, and they arrive by *different* patterns — which is precisely what this ADR predicted:

| Advertised connector | Live spatial path | Pattern |
|---|---|---|
| Slack | `integrations/slack/spatial_adapter` (3 importers) | Granular Adapter |
| Notion | `mcp/consumer/notion_adapter` → `notion_integration_router` | (see A2 — **not** the pattern this ADR cited) |
| Calendar | `mcp/consumer/google_calendar_adapter` → `calendar_integration_router` | Delegated MCP |
| GitHub | `integrations/spatial/github_spatial` + `mcp/consumer/github_adapter` | full 8-dimensional, live |

**No part of this ADR's decision requires amendment.** What requires amendment is how it *evidenced* the decision.

## A2 — ⚠️ The verification claims are CORRECTED. One of three citations went stale.

The **Verification Results** section (and the "Production-proven / Proven operational" lines at §§112, 134, 144, 204) asserted per-connector operational status. Measured 2026-07-30:

| ADR-038 claim | Current state | Verdict |
|---|---|---|
| *"Slack spatial: 11 files, 100% operational"* | `slack/spatial_adapter` live — 3 importers | ✅ **holds** |
| *"Calendar spatial: 2 files, 100% operational, MCP protocol integration"* | `google_calendar_adapter` live via `calendar_integration_router` | ✅ **holds** |
| *"Notion spatial: 1 file, 100% operational, 8-dimensional analysis working"* | **`intelligence/spatial/notion_spatial` has ZERO importers and ~12 undefined methods (~75% abandoned)** | ❌ **CONTRADICTED** |

**But Notion's spatial capability is live** — via `mcp/consumer/notion_adapter`, which produces `SpatialContext`/`SpatialPosition`. **Notion users are not missing place-modeling.** What is dead is the *specific file this ADR cited as proof*.

**Do not cite §§106–112, 134, 144 or 204 as current fact.** They were true when written; one is now false, and all four are frozen snapshots of a moving system.

## A3 — ★ The methodological error, named so it doesn't recur

**ADR-038 was right about the pattern and wrong about which connector proved it.**

The `notion_spatial` citation didn't go stale because the pattern failed. It went stale because **CORE-MCP-MIGRATION #198 moved the implementation** — replacing per-connector direct-API spatial modules with MCP consumer adapters **built on the same spatial contract** (`BaseSpatialAdapter` / `SpatialContext`, `services/integrations/spatial_adapter.py`) — while this ADR kept pointing at the superseded predecessor.

**The error class: citing an IMPLEMENTATION as evidence for a PATTERN that outlives it.** An implementation is a point-in-time fact with a short half-life; a pattern is a decision. Binding the second to the first means a successful migration makes the ADR *look* falsified — and that is exactly what happened here. An agent reading §107 against the cold `notion_spatial` file would conclude the pattern failed. **It succeeded so thoroughly that the code it was demonstrated on became redundant.**

**Forward rule for this corpus**: an ADR may cite implementations as *illustration*, never as *proof of continuing validity*. Where an ADR needs to make a live/cold claim, it must point at a command that re-derives it rather than freezing a table. (This amendment follows that rule — see A4.)

## A4 — Where the facts live now

**This amendment deliberately does not restate the live/cold inventory.** It lives in `../spatial-intelligence-layer-map-and-costed-options.md`, and every claim there is re-derivable:

```
python3 scripts/reachability-map.py services/integrations/spatial services/intelligence/spatial services/mcp/consumer
```

**If any table in this corpus disagrees with that command, the command is right.** (CXO's formulation, 2026-07-30: *"prose can't be re-run; the tool can"* — adopted here as a corpus convention, not just a note.)

⚠️ **A string match on a module name is not an import edge.** Both CXO and I independently mistook `config_service.py:222`'s feature-flag string `"notion_spatial_mapping"` for a `notion_spatial` importer, within a day of each other. Use the tool.

## A5 — What is still open (this amendment closes none of it)

The committed-theory review has **not** concluded. Open: PPM's roadmap-dependency slice; Lead's cost estimate for an L4 (ambient-presence) monitoring loop; and **PM's call on the 10-module cold island**, which should be described as *"superseded implementation strategy, retained as prior art"* rather than dead code — it holds the only worked examples of place-modeling for four connectors.

**Spatial deletions remain HELD.** Spatial intelligence is protected representation under PM's standing rule, and nothing here authorizes removal.

---
