# ADR-052: Standardize on Tool-Based MCP Implementation

**Status**: Accepted
**Date**: October 17, 2025
**Deciders**: Chief Architect, Lead Developer
**GitHub Issue**: #198 (CORE-MCP-MIGRATION)

---

## Context

Note: was initially numbered ADR-037 but not added to the ADRs directory, so its number was reused. It was added to the collection on Tue Jan 13 2026 and given #052.

During Phase -1 discovery of Sprint A3 MCP migration (#198), we discovered two competing MCP implementation patterns across our integrations:

### Tool-Based MCP (GitHub, Calendar)
- Direct tool definitions in integration routers
- Tools registered with orchestration layer
- Simpler architecture, no separate servers
- 90-95% complete implementations

### Server-Based MCP (Notion)
- Separate MCP servers with protocol handlers
- More complex architecture with additional abstraction layers
- Requires server lifecycle management
- 60% complete implementation

**Discovery Evidence**:
```
Service    | Pattern      | Completion | Complexity
-----------|--------------|------------|------------
Calendar   | Tool-based   | 95%        | Low
GitHub     | Tool-based   | 90%        | Low
Notion     | Server-based | 60%        | High
Slack      | Basic        | 40%        | TBD
```

**Key Findings**:
1. Tool-based implementations are simpler and more complete
2. Server-based implementation adds architectural complexity without clear benefit
3. Calendar (tool-based) is our most mature implementation
4. No technical advantage identified for server-based approach in our use case

---

## Decision

**We will standardize on tool-based MCP implementation across all integrations.**

This means:
1. **Tool-based MCP is our canonical pattern**
2. **Server-based implementations must migrate to tool-based**
3. **All future integrations must use tool-based approach**
4. **Calendar integration serves as reference implementation**

---

## Rationale

### Technical Simplicity
- Tool-based requires fewer architectural layers
- Direct tool registration with orchestration engine
- Simpler debugging and maintenance
- Proven pattern in our two most complete integrations

### Implementation Evidence
- **Calendar**: 95% complete using tool-based (only config loading needed)
- **GitHub**: 90% complete using tool-based (only wiring needed)
- **Notion**: 60% complete using server-based (architecture incomplete)

This completion pattern strongly suggests tool-based is the natural fit for our architecture.

### Consistency
- Single pattern easier to understand and maintain
- New developers learn one approach
- Testing patterns unified across integrations
- Documentation simpler

### Performance
- Tool-based has less overhead (no server abstraction)
- Direct orchestration access to tools
- Simpler call paths

### Maintainability
- Fewer moving parts (no separate servers)
- No server lifecycle management needed
- Easier to debug (fewer layers)

---

## Consequences

### Positive

**Immediate Benefits**:
- Clear pattern for completing Calendar (95%→100%)
- Clear pattern for completing GitHub (90%→100%)
- Clear pattern for completing Slack (40%→100%)
- Single reference implementation (Calendar)

**Long-term Benefits**:
- Architectural consistency across all integrations
- Simplified onboarding for new developers
- Reduced maintenance burden
- Clear pattern for future integrations
- Easier testing and debugging

### Negative

**Migration Required**:
- Notion must migrate from server-based to tool-based
- Migration effort: 3-4 hours estimated
- Risk of regression during migration
- Need migration guide for future reference

**Sunk Cost**:
- Server-based Notion implementation (60% complete) must be replaced
- Previous architectural decisions superseded
- Some code will be discarded

### Mitigation Strategies

**For Notion Migration**:
1. Use Calendar as reference implementation
2. Extract existing tool definitions from server
3. Create comprehensive tests before migration
4. Maintain backward compatibility during transition
5. Document migration pattern for future use

**For Future Integrations**:
1. Calendar serves as canonical reference
2. Clear documentation of tool-based pattern
3. Template for new integrations
4. Testing patterns established

---

## Implementation Plan

### Phase 0.5: ADR Creation (30 minutes)
- ✅ Document this architectural decision
- ✅ Update ADR index
- ✅ Communicate to team

### Phase 1: Complete Tool-Based Implementations (3-4 hours)
1. **Calendar** (95%→100%): Add configuration loading
2. **GitHub** (90%→100%): Complete integration wiring
3. **Document Pattern**: Create reference documentation

### Phase 2: Migrate Server-Based to Tool-Based (3-4 hours)
1. **Notion** (60%→100%): Migrate from server to tools
2. **Create Migration Guide**: Document conversion pattern
3. **Test Thoroughly**: Ensure no functionality loss

### Phase 3: Complete Remaining Integration (2-3 hours)
1. **Slack** (40%→100%): Implement using tool-based pattern
2. **Final Testing**: Validate all integrations
3. **Documentation**: Update architecture docs

**Total Effort**: 8-10 hours (Sprint A3 achievable)

---

## Related Decisions

### Supersedes
- Any previous decisions favoring server-based MCP
- Notion server-based implementation approach

### References
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) - Spatial intelligence patterns (three valid approaches: Granular, Embedded, Delegated MCP)
- [ADR-034: Plugin Architecture](adr-034-plugin-architecture.md) - Plugin pattern compatible with tool-based MCP

### Terminology Clarification

**Tool-based MCP** (this ADR) determines the *protocol architecture* - how we communicate with external services via MCP protocol.

**Delegated MCP Pattern** (ADR-038) is the *spatial intelligence approach* that builds on tool-based MCP - how we add 8-dimensional spatial context to MCP integrations.

Calendar uses both: it implements tool-based MCP (per this ADR) with the Delegated MCP spatial pattern (per ADR-038).

### Future Impact
- All future MCP integrations must follow tool-based pattern
- Migration guide serves as template for any server→tool conversions
- Calendar becomes canonical reference implementation

---

## Validation Criteria

This decision is validated when:

1. ✅ All four integrations use tool-based pattern
2. ✅ Calendar serves as documented reference implementation
3. ✅ Notion successfully migrated with no functionality loss
4. ✅ Migration guide created for future use
5. ✅ All integrations tested with real operations
6. ✅ Pattern documentation updated
7. ✅ Team trained on tool-based approach

---

## Notes

### Discovery Process
This decision emerged from systematic Phase -1 investigation following Inchworm Protocol. The evidence was clear: tool-based implementations were more complete and simpler. This is a "following the evidence" decision, not a theoretical preference.

### 75% Pattern
The Notion server-based implementation at 60% completion is another instance of our recurring "75% pattern" - systems that are mostly built but incomplete. The tool-based pattern's higher completion rate (90-95%) suggests it's the natural architectural fit.

### Time Lord Philosophy
This decision prioritizes quality and consistency over preserving incomplete work. The 3-4 hour migration cost for Notion is small compared to long-term maintenance benefits of a unified pattern.

---

**Decision Status**: ✅ **ACCEPTED**
**Implementation Status**: 🚧 In Progress (Sprint A3)
**Review Date**: After Sprint A3 completion

---

**Document Created**: October 17, 2025, 1:50 PM PT
**Last Updated**: January 13, 2026 (reference update: ADR-013 → ADR-038)
**Author**: Lead Developer (with Chief Architect guidance)
