# ADR-020: Protocol Development Investment

**Date**: August 17, 2025
**Status**: Superseded — never executed (status corrected 2026-08-29)
**Deciders**: Principal Architect, Chief Architect, Chief of Staff
**Classification**: Strategic (Long-term Vision)

## Context

MCP has proven successful as our integration layer, but it's a general-purpose protocol not optimized for Product Management workflows. Through implementing PM-033c/d, we've discovered patterns and requirements unique to PM orchestration that aren't adequately expressed in standard MCP.

The phrase "downpayment on our own protocol" emerged during architecture discussions when we realized we're not just consuming protocols—we're learning what a PM-specific protocol needs to enable.

As noted in our strategic sessions: "Good architecture naturally becomes open because clean abstractions are shareable, well-defined boundaries become protocols." Our architecture has reached the maturity where defining our own protocol extensions is both possible and necessary.

## Decision

We will invest in developing PM-specific protocol extensions and, eventually, a standalone PM orchestration protocol, building on MCP's foundation while addressing Product Management's unique requirements.

### Investment Phases

**Phase 1: MCP Extensions** (Current - 3 months)
- Extend MCP with PM-specific capabilities
- Document patterns as protocol proposals
- Contribute back to MCP community
- Build coalition of PM tool makers

**Phase 2: Protocol Specification** (3-6 months)
- Formalize Piper Protocol for PM orchestration
- Define standard PM workflow primitives
- Create reference implementation (Piper itself)
- Open source the specification

**Phase 3: Ecosystem Development** (6-12 months)
- SDK development for multiple languages
- Partner integrations
- Community governance model
- Protocol certification program

### PM-Specific Protocol Requirements

**What MCP Lacks for PM**:

1. **Workflow State Management**
   - Sprint boundaries and transitions
   - Epic/Story/Task hierarchies
   - Cross-tool dependency tracking
   - Approval workflows

2. **PM Semantics**
   - Velocity calculations
   - Burndown projections
   - Risk assessments
   - Stakeholder mappings

3. **Temporal Reasoning**
   - Deadline management
   - Schedule conflict detection
   - Resource allocation over time
   - Historical pattern analysis

4. **Multi-Tool Coordination**
   - GitHub + Jira + Notion + Linear state sync
   - Conflict resolution across tools
   - Authoritative source determination
   - Event propagation patterns

### Protocol Design Principles

```yaml
piper_protocol:
  extends: mcp
  version: 0.1.0

  primitives:
    - workflow_state
    - approval_chain
    - velocity_metric
    - dependency_graph
    - resource_allocation
    - risk_assessment

  patterns:
    - sprint_transition
    - story_decomposition
    - stakeholder_notification
    - metric_aggregation
    - conflict_resolution

  guarantees:
    - eventual_consistency
    - audit_trail
    - rollback_capability
    - privacy_preservation
```

## Consequences

### Positive

1. **Competitive Moat**: First PM-specific protocol becomes industry standard
2. **Ecosystem Leadership**: Define how PM tools interoperate
3. **Open Source Credibility**: Contributing to broader community
4. **Network Effects**: Each adopter increases protocol value
5. **Innovation Catalyst**: Enable new PM tool categories

### Negative

1. **Specification Burden**: Maintaining protocol requires resources
2. **Backward Compatibility**: Must support protocol evolution
3. **Community Management**: Open protocols need governance
4. **Competition Risk**: Others might fork or compete

### Neutral

1. **Standards Process**: Must engage with standards bodies eventually
2. **Documentation Requirements**: Extensive specs and examples needed
3. **Reference Implementation**: Piper becomes the reference
4. **Adoption Timeline**: Years to achieve critical mass

## Alternatives Considered

### Alternative 1: Stick with Pure MCP
**Why Rejected**: MCP is too generic. PM needs would always be second-class, requiring workarounds and custom implementations that fragment the ecosystem.

### Alternative 2: Build Proprietary Protocol
**Why Rejected**: Closed protocols limit adoption. Our architecture philosophy ("good architecture becomes open") demands openness. Network effects require community participation.

### Alternative 3: Wait for Market Leader
**Why Rejected**: No PM protocol leader has emerged. Waiting cedes competitive advantage. Our implementation experience positions us to lead.

## Implementation Strategy

### Near Term (Q3 2025)
1. Document PM patterns discovered during MCP implementation
2. Create `piper-protocol` GitHub repository
3. Write initial specification RFC
4. Build prototype extensions in Piper

### Medium Term (Q4 2025 - Q1 2026)
1. Release v0.1 specification
2. Create reference implementation
3. Develop Python/TypeScript SDKs
4. Partner with 2-3 PM tools for pilot

### Long Term (2026)
1. Form protocol governance committee
2. Submit to relevant standards bodies
3. Build certification program
4. Host first PiperConf for protocol adopters

## Success Metrics

### Technical Metrics
- 10+ PM-specific primitives defined
- 100% of Piper workflows expressible in protocol
- <100ms protocol overhead

### Adoption Metrics
- 5+ tools implementing protocol (Year 1)
- 1000+ GitHub stars on specification
- 3+ language SDKs available

### Strategic Metrics
- Mentioned in industry analyst reports
- Adopted by major PM tool vendor
- Becomes reference in PM tool discussions

## Related Decisions

- **ADR-001**: MCP Integration (foundation we extend)
- **ADR-018**: Server Functionality (protocol provider model)
- **ADR-019**: Orchestration Commitment (patterns to encode)
- **PM-033d**: Enhanced Autonomy (protocol-level capabilities)

## Notes

The investment in protocol development represents a strategic bet that PM tooling will converge on standards, and that the first credible standard will capture significant value. Our unique position—having built deep integrations across multiple PM tools—gives us the experience to define what this protocol needs.

The "downpayment" isn't just code or documentation—it's the commitment to open, shared infrastructure for Product Management. Every pattern we discover, every integration we build, contributes to the protocol specification.

As our architecture discussions revealed: "Bad architecture can never become open because it can't bear the scrutiny." The fact that we're ready to open our patterns as protocol proves our architecture's quality.

## Future Considerations

- **AI-Native Protocol Features**: Encoding LLM-friendly semantics
- **Federation Protocols**: Multi-organization PM coordination
- **Real-time Collaboration**: WebRTC integration for live PM sessions
- **Blockchain Integration**: Immutable audit trails for compliance

---

*"Protocols are how good architecture becomes shared infrastructure. We're not just building Piper—we're defining how PM tools communicate."*
---

## Status correction (2026-08-29, Chief Architect — Architectural Review 2026, mechanical win #4)

**Status corrected Accepted → Superseded (never executed).** No phase of the Piper Protocol plan
(spec, reference implementation, open-sourcing) was ever built; no decision record ever cancelled
it — this note is that record. The distribution question this ADR reached for is answered by
PDR-005/PDR-006 (BYOC + hosted MCP) using the industry's protocol (MCP) rather than an owned one.
