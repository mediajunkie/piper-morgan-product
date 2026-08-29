# ADR-001: MCP Integration Pilot

**Date**: July 3, 2025
**Status**: Accepted
**Deciders**: Principal Architect, Chief of Staff

## Context

Piper Morgan needs to integrate with an expanding ecosystem of PM tools beyond GitHub and Jira. Building custom integrations for each tool is not scalable with single developer bandwidth.

## Decision

We will implement Model Context Protocol (MCP) support in a phased approach, starting with Piper as an MCP consumer.

## Consequences

### Positive

- Standardized integration pattern for new tools
- Access to community-built MCP servers
- Reduced maintenance burden
- Enhanced knowledge federation capabilities

### Negative

- Dependency on emerging standard
- Initial learning curve
- Additional abstraction layer

### Neutral

- Requires adapter pattern to maintain backward compatibility
- 6-8 week implementation timeline

## Implementation Plan

1. Phase 1: MCP Consumer (4-6 weeks)
2. Phase 2: Hybrid Integration (2-3 weeks)
3. Phase 3: MCP Provider (Future/Maybe)

Start date: After PM-011 closure (Week 4+)

---

## Update October 2025

See **ADR-034: Plugin Architecture Implementation** for how MCP integrations are now managed as plugins. The Calendar integration implements the "Delegated MCP Pattern" documented in ADR-038, where MCP adapters are wrapped as plugins for unified lifecycle management and configuration control.

---

_Last Updated: July 09, 2025_

## Revision Log

- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
