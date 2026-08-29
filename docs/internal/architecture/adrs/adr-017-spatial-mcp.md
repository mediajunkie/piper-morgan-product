# ADR-017: Spatial-MCP Refactoring

**Status**: Implemented
**Date**: August 17, 2025 (Documenting August 12, 2025 decision)
**Decision Makers**: PM, Lead Developer, Chief Architect
**Classification**: Architectural Refactoring

## Context

During the MCP Monday sprint (August 11, 2025), we successfully implemented Model Context Protocol federation for tool interoperability. Simultaneously, we had developed an 8-dimensional spatial intelligence system for understanding PM workflows in context.

Initially, these were separate systems:
- **MCP Federation**: Tool connectivity and protocol standardization
- **Spatial Intelligence**: Contextual understanding across 8 dimensions

On Tuesday (August 12, 2025), while implementing PM-033b, we discovered these parallel systems were solving related problems:
- MCP provided the **communication layer**
- Spatial intelligence provided the **understanding layer**

The revelation: Spatial intelligence shouldn't compete with MCP—it should enhance it. Every MCP tool could benefit from spatial context, and spatial analysis needs tool data from MCP.

### The 8 Dimensions of Spatial Intelligence

1. **HIERARCHY**: Organizational structure (epic → story → task)
2. **TEMPORAL**: Time relationships (deadlines, sequences, dependencies)
3. **PRIORITY**: Urgency and importance mapping
4. **COLLABORATIVE**: Team interactions and handoffs
5. **FLOW**: Process and workflow states
6. **QUANTITATIVE**: Metrics and measurements
7. **CAUSAL**: Cause-effect relationships
8. **CONTEXTUAL**: Environmental factors

### The Integration Opportunity

We realized that spatial intelligence could be exposed as MCP services, allowing:
- Any MCP tool to query spatial context
- Spatial analysis to consume any MCP tool's data
- Unified architecture instead of parallel systems

## Decision

We will refactor spatial intelligence to operate as MCP services, making every spatial dimension queryable through the MCP protocol while allowing spatial analysis to consume data from any MCP-connected tool.

### Architectural Pattern

**Before (Parallel Systems)**:
```
┌─────────────┐     ┌──────────────────┐
│     MCP     │     │     Spatial      │
│  Federation │     │  Intelligence    │
└─────────────┘     └──────────────────┘
      ↓                     ↓
┌─────────────┐     ┌──────────────────┐
│    Tools    │     │    Analysis      │
└─────────────┘     └──────────────────┘
```

**After (Unified Architecture)**:
```
┌─────────────────────────────────────┐
│         MCP + Spatial Layer         │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Spatial MCP Services       │  │
│  │  ┌────────┐  ┌────────┐     │  │
│  │  │Hierarchy│  │Temporal│ ... │  │
│  │  └────────┘  └────────┘     │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │   Tool MCP Services          │  │
│  │  ┌────────┐  ┌────────┐     │  │
│  │  │ GitHub │  │ Notion │ ... │  │
│  │  └────────┘  └────────┘     │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Implementation Approach

```python
class SpatialMCPService(MCPService):
    """Spatial intelligence exposed as MCP services"""

    @mcp_method("spatial.analyze")
    async def analyze_spatial_context(self, entity_id: str, dimensions: List[str]):
        """Analyze entity across requested spatial dimensions"""
        results = {}
        for dimension in dimensions:
            analyzer = self.get_analyzer(dimension)
            results[dimension] = await analyzer.analyze(entity_id)
        return results

    @mcp_method("spatial.hierarchy.traverse")
    async def traverse_hierarchy(self, start_id: str, direction: str = "up"):
        """Navigate organizational hierarchy"""
        return await self.hierarchy_analyzer.traverse(start_id, direction)

    @mcp_method("spatial.temporal.timeline")
    async def get_timeline(self, entity_ids: List[str]):
        """Generate temporal timeline for entities"""
        return await self.temporal_analyzer.create_timeline(entity_ids)
```

### Migration Path

**Phase 1: Parallel Operation** (Implemented)
- Both systems run simultaneously
- No breaking changes
- Gradual migration of consumers

**Phase 2: MCP Service Wrapper** (Implemented)
- Spatial intelligence exposed via MCP
- Tools begin consuming spatial services
- Bidirectional data flow established

**Phase 3: Full Integration** (Current)
- Spatial-native MCP implementation
- Deprecated standalone spatial system
- All spatial queries through MCP

## Consequences

### Positive

1. **Architectural Simplification**: One system instead of two
2. **Universal Spatial Context**: Any MCP tool gets spatial intelligence
3. **Bidirectional Enhancement**: Tools provide data, spatial provides context
4. **Protocol Standardization**: Spatial queries follow MCP standards
5. **Performance Achievement**: Sub-1ms federated search with spatial context
   *[Confidence: Low - Likely from mocked tests per ADR-015]*

### Negative

1. **Refactoring Effort**: 2 days to merge systems
   *[Actual: Completed in 4 hours on August 12]*
2. **Protocol Overhead**: MCP adds ~10ms latency
   *[Measured: Actually negligible in practice]*
3. **Deprecation Management**: Existing spatial API consumers need migration

### Neutral

1. **Architectural Pattern**: Becomes reference for future consolidations
2. **Documentation Updates**: All spatial docs need MCP context
3. **Testing Expansion**: Spatial tests must include MCP protocol

## Implementation Evidence

From PM-033b session log (August 12, 2025):
```
**Historic Performance Achievement**:
- Federated Search: <1ms average (target: <150ms)
- Spatial Context: 0.10ms average (target: <50ms)
- Implementation Speed: 19 minutes total execution
```
*Note: Performance claims need verification per ADR-015*

The implementation created `GitHubSpatialIntelligence` with full 8-dimensional analysis integrated into the MCP federation, validated through comprehensive test scenarios.

## Alternatives Considered

### Alternative 1: Keep Systems Separate
**Description**: Maintain parallel spatial and MCP systems
**Rejected Because**: Duplicate maintenance, missed integration opportunities

### Alternative 2: Spatial-First Architecture
**Description**: Make MCP subordinate to spatial intelligence
**Rejected Because**: Violates protocol standards, limits interoperability

### Alternative 3: Gradual Feature Migration
**Description**: Move one dimension at a time to MCP
**Rejected Because**: Extends transition period, confuses consumers

## References and Influences

- **Model Context Protocol Specification**: Standard for tool interoperability
- **Embodied Cognition Theory**: Spatial reasoning in AI systems
- **Domain-Driven Design**: Bounded contexts and integration patterns
- **Our Discovery**: "MCP+Spatial as competitive advantage" (August 12, 2025)

## Related ADRs

- ADR-001: MCP Integration (foundation for federation)
- ADR-013: MCP+Spatial Integration Pattern (documents the result)
- ADR-016: Ambiguity-Driven Architecture (uses spatial context for routing)
- ADR-000: Meta-Platform Vision (spatial intelligence as differentiator)

## Notes

This refactoring exemplifies emergent architecture—we didn't plan to merge these systems, but their natural affinity became obvious during implementation. The speed of refactoring (4 hours vs. 2-day estimate) validated the architectural fit.

The pattern established here—exposing domain intelligence as MCP services—becomes reusable for future capabilities. Any specialized intelligence we develop can be MCP-native from the start.

Success metrics:
- 100% of spatial queries routed through MCP
- Zero degradation in spatial analysis quality
- 90% reduction in code duplication
- Spatial context available to all MCP tools
