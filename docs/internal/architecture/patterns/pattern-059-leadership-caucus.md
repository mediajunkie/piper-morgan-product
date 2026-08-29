# Pattern-059: Leadership Caucus

## Status

**Emerging** | Proven in MUX Track V1 (January 19, 2026)

## Context

Complex, cross-cutting work often requires input from multiple advisor domains before execution can begin. Traditional approaches have limitations:

- **Sequential handoffs** (cascade): Slow, context lost between steps, downstream advisors can't influence upstream decisions
- **Async mailboxes alone**: Good for ongoing communication but can create alignment lag for time-sensitive decisions
- **Ad-hoc collaboration**: Works but inconsistent, decisions may not be captured

The Leadership Caucus addresses the need for **synchronous multi-advisor alignment** before complex work begins, complementing async coordination patterns.

## Pattern Description

**Core Concept**: A facilitated, synchronous discussion where multiple advisors contribute domain perspectives to a cross-cutting decision, with the PM as facilitator capturing decisions as they emerge.

**Key Elements**:
- **Facilitator (PM)**: Frames the question, captures decisions, resolves disputes
- **Multiple advisors**: Contribute from their domain expertise (CXO, Architect, PPM, etc.)
- **Lead Dev** (if implementation follows): Confirms execution path
- **Real-time decision capture**: Decisions documented as they're made, not reconstructed later

**How It Works**:
1. PM identifies cross-cutting work requiring multi-domain alignment
2. PM convenes relevant advisors (not necessarily all—just those relevant)
3. Structured discussion produces captured decisions
4. Lead Dev confirms implementation approach
5. Execution proceeds with alignment already achieved

## Implementation

### Trigger Conditions

Use a Leadership Caucus when:

- Work spans multiple advisor domains (e.g., design + architecture + product)
- Transitioning from vision to implementation on significant features
- Architectural or design decisions have multiple valid approaches
- PM believes upfront alignment will accelerate execution
- Mailbox async exchange would create unacceptable delay

### Participants

| Role | Presence | Purpose |
|------|----------|---------|
| PM | Required (facilitator) | Frame question, capture decisions, resolve disputes |
| Relevant advisors | 2+ recommended | Contribute domain perspective |
| Lead Dev | If implementation follows | Confirm implementation path |

**Note**: Full advisor complement is optional—invite those relevant to the decision.

### Facilitation Protocol

```
1. FRAME    - PM states the question and provides context
2. CONTRIBUTE - Each advisor shares perspective from their domain
3. CAPTURE  - PM documents decisions explicitly as they emerge
4. RESOLVE  - Disagreements addressed in session (not deferred)
5. CONFIRM  - Lead Dev acknowledges implementation path
```

### Outputs

- **Decisions documented** (can be informal—omnibus log captures)
- **Implementation assignment** (who does what)
- **Open questions flagged** for follow-up (if any)

## Usage Guidelines

### When to Use

- Cross-cutting work spanning multiple advisor domains
- Vision → Implementation transitions (like MUX V1)
- Significant architectural or design decisions with multiple stakeholders
- PM believes upfront alignment will accelerate execution
- Time-sensitive decisions where async would create delay

### When NOT to Use

- Single-domain decisions (use direct consultation or mailbox)
- Simple, well-understood work with clear ownership
- Decisions that don't benefit from multiple perspectives
- When async exchange is sufficient and time permits

### Best Practices

- Keep it focused: Clear question, relevant participants only
- Capture decisions in real-time, not after the fact
- Resolve disagreements in session—don't defer
- PM facilitates but doesn't dominate; advisors contribute expertise
- Lead Dev presence ensures implementation feasibility is considered

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correction |
|--------------|----------------|------------|
| Caucus for single-domain decisions | Overkill; wastes advisor time | Use direct consultation or mailbox |
| Skipping caucus for cross-cutting work | Creates alignment debt; execution slows | Call the caucus upfront |
| No facilitator | Discussion meanders, decisions unclear | PM always facilitates |
| Deferring disagreements | Kicks the can; alignment incomplete | Resolve in session |
| Full advisor complement always | Not all decisions need everyone | Invite only relevant advisors |
| Design by committee | Advisors contribute, they don't vote | PM facilitates and decides |

## Examples in Codebase

### Primary Usage

**MUX Track V1 (January 19, 2026)**:
- **Question**: How to move MUX from vision to implementation?
- **Participants**: CXO (design philosophy), PPM (product guidance), Chief Architect (technical direction), Lead Dev (execution), PM (facilitation)
- **Outcome**: MUX P1 delivered in 15 minutes with 101 tests
- **Reference**: `docs/omnibus-logs/2026-01-19-omnibus-log.md`

### Pattern Origin

Identified by HOSR during Jan 16-22 workstream review as "Leadership Cascade," renamed to "Leadership Caucus" by PM to emphasize iterative deliberation over sequential handoff.

## Related Patterns

### Complements

- [Pattern-049: Audit Cascade](pattern-049-audit-cascade.md) - Caucus creates alignment *before* work; Audit Cascade verifies *after* work
- Mailbox System - Async (mailboxes) + sync (caucus) = complete coordination toolkit

### Comparison

| Pattern | Purpose | Timing | Participants |
|---------|---------|--------|--------------|
| Audit Cascade (049) | Verify work at phase boundaries | After work | Single agent audits |
| Mailbox System | Async cross-role communication | Any time | 1:1 or 1:many |
| **Leadership Caucus (059)** | Sync multi-advisor alignment | Before complex work | PM + multiple advisors |

### Differentiation: Pattern-059 vs Pattern-029

Pattern-059 and [Pattern-029: Multi-Agent Coordination](pattern-029-multi-agent-coordination.md) both involve multiple agents but serve different purposes:

| Dimension | Pattern-059 (Leadership Caucus) | Pattern-029 (Multi-Agent Coordination) |
|-----------|---------------------------------|----------------------------------------|
| **Domain** | Leadership alignment | Technical execution |
| **Purpose** | Align on cross-cutting decisions before work begins | Coordinate parallel implementation work |
| **Participants** | Advisory agents (CXO, Architect, PPM) + PM | Coding agents (Backend, Frontend, Analyst) |
| **Timing** | Before execution | During execution |
| **Output** | Decisions, assignments, implementation direction | Code, tests, validated changes |
| **Coordination** | Facilitated discussion, real-time decision capture | Cross-validation, handoffs, parallel phases |

**In practice**: A Leadership Caucus (059) produces the decision and assignment that triggers a Multi-Agent Coordination (029) deployment. They are sequential, not competing — one decides *what* and *how*; the other *executes*.

### Alternatives

- **Direct consultation**: For single-domain decisions
- **Mailbox exchange**: For async alignment when time permits
- **Sequential handoff**: When domains are truly independent (rare for complex work)

## References

### Documentation

- Original identification: HOSR workstream review memo (January 24, 2026)
- CIO formalization recommendation: `mailboxes/exec/read/memo-cio-leadership-caucus-response-2026-01-26.md`
- PM request for formalization: `mailboxes/cio/read/memo-cio-leadership-caucus-2026-01-26.md`

### Usage Analysis

- Current usage count: 1 documented instance (MUX V1)
- First documented: January 19, 2026 (identified), January 26, 2026 (formalized)
- Maintenance status: Emerging

---

_Pattern created: January 26, 2026_
_Origin: MUX Track V1 coordination success_
_Formalized per CIO recommendation_
