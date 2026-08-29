# ADR-002: Claude Code Integration

**Date**: July 6, 2025
**Status**: Accepted
**Deciders**: Principal Architect, Chief of Staff, CTO, PM
**Last Modified**: July 8, 2025 (Sprint Zero findings added)

## Context

Current development workflow using Opus + Cursor Agent requires approximately 80% coordination overhead - the PM spends 4 hours coordinating for every 1 hour of implementation. This is unsustainable for a single-developer project with ambitious scope.

Claude Code promises:

- Complete implementation traces
- Self-directed task completion
- Architectural rule enforcement
- Reduced context switching

### Sprint Zero Validation (July 7-8, 2025)

PM-011 debugging sessions served as unintentional validation exercise:

- **4 hours** spent debugging 7 integration issues
- **75% time savings** projected (2 hours → 30 minutes)
- **20-25 copy/paste cycles** between Claude and Cursor Agent
- **15+ context switches** causing architectural drift
- Multiple violations of established patterns due to lost context

## Decision

We will pilot Claude Code as a replacement for Cursor Agent in our development workflow, with a phased adoption approach based on measured efficiency gains.

Based on Sprint Zero findings, we are accelerating the timeline to begin integration immediately rather than waiting for Week 2.

## Consequences

### Positive

- Potential 50%+ reduction in coordination overhead (80% → 40%)
- More time for architectural thinking and design
- Complete implementation traces improve learning
- Automated pattern enforcement via `.claude-code-rules`
- Better debugging through full execution visibility
- **Force multiplier across all workstreams** (not a new workstream)

### Negative

- Risk of reduced code understanding without proper review
- New tool learning curve (mitigated by phased approach)
- Potential over-reliance on automation
- Cost of context switch if pilot fails

### Neutral

- Requires disciplined code review practices
- Changes daily development rhythm
- New documentation requirements for workflows

## Implementation Plan (Accelerated)

### Week 0 (July 7-8) ✅

- Documented current pain points through PM-011 debugging
- Validated 80% coordination overhead claim
- Confirmed 75% potential time savings

### This Week (July 8-12)

- Request Claude Code access immediately
- Setup environment and `.claude-code-rules`
- Test on document summarization bug
- Make go/no-go decision by Friday

### Next Week (Full Adoption if approved)

- Transition all development to Claude Code
- Maintain Cursor Agent knowledge for fallback
- Daily efficiency tracking against Sprint Zero baseline

### Following Week

- Use Claude Code for MCP implementation
- Compound benefits of both improvements

## Sprint Zero Evidence

The PM-011 debugging sessions provided empirical validation:

| Metric             | Current Tools | Claude Code (Projected) | Improvement |
| ------------------ | ------------- | ----------------------- | ----------- |
| Debug Simple Bug   | 15 min        | 1 min                   | 93%         |
| Trace Data Flow    | 30 min        | 5 min                   | 83%         |
| Fix Integration    | 45 min        | 10 min                  | 78%         |
| Full Debug Session | 2 hours       | 30 min                  | 75%         |

Key findings:

- Every component boundary hid integration issues
- Lost context led to guessing methods that didn't exist
- Architectural principles abandoned during "the chase"
- Past code became unrecognizable without context

## Success Criteria

**Proceed to full adoption if ALL met:**

1. 50%+ reduction in coordination time
2. Architectural patterns maintained in generated code
3. Developer can explain all generated code
4. Tests pass without manual fixing
5. No increase in bug rate

## Failure Criteria

**Revert to Cursor Agent if ANY occur:**

1. Architectural violations increase
2. Developer cannot explain generated code
3. Debugging time increases rather than decreases
4. Critical bugs traced to generated code
5. Coordination overhead reduction < 25%

## Risk Mitigation

1. **Mandatory Code Walkthroughs**: Every Claude Code session ends with developer explaining what was built
2. **Incremental Adoption**: Start with low-risk tasks
3. **Metrics Tracking**: Daily measurement of efficiency and quality
4. **Fallback Plan**: Cursor Agent remains available throughout pilot
5. **Learning Enforcement**: No commits without understanding

## Alternatives Considered

1. **Status Quo (Opus + Cursor)**: Rejected due to unsustainable coordination overhead
2. **Hire Additional Developer**: Rejected due to $0 budget constraint
3. **Reduce Project Scope**: Rejected as it abandons the vision
4. **Different AI Tool**: No other tool offers complete traces

## Related Decisions

- ADR-001: MCP Integration (scheduled for Week 4+)
- Architectural patterns in pattern-catalog.md
- Development workflows in chat-protocols.md

## Review Schedule

- Week 2 End: Pilot assessment and go/no-go decision
- Week 3 End: Full adoption assessment
- Monthly: Ongoing efficiency tracking

---

_"The best tool is the one that lets you focus on the problem, not the process."_

---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
