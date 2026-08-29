# Pattern Family Index

_Patterns organized by how they work together, not just what they're about._

**Purpose**: The category index (README.md) organizes patterns by topic. This index organizes them by *family* — patterns that reinforce each other and work best when applied together.

**Usage**: When starting work, identify which families apply. Apply patterns in family units, not individually.

---

## Tier 1: Established Families

_Proven pattern groups with documented co-occurrence and reinforcing effects._

### Completion Theater Family

**Patterns**: 045, 046, 047, 049
**Lead Pattern**: [Pattern-045: Green Tests, Red User](pattern-045-green-tests-red-user.md) ← Start here (diagnostic)
**Health**: Excellent
**Use when**: Multi-phase work, closing issues, preventing premature completion

| Pattern | Role in Family |
|---------|----------------|
| 045: Green Tests, Red User | Diagnoses the gap (tests pass, users fail) |
| 046: Beads Completion Discipline | Enforces 100% completion criteria |
| 047: Time Lord Alert | Enables pause when uncertain |
| 049: Audit Cascade | Verifies at every phase boundary |

**Quick reference**: 045 diagnoses → 046 enforces → 047 enables pause → 049 audits

---

### Investigation & Root Cause Family

**Patterns**: 006, 041, 042, 043, 060
**Lead Pattern**: [Pattern-006: Verification-First](pattern-006-verification-first.md) ← Start here (foundation)
**Health**: Excellent
**Use when**: Bug fixing, incident response, security investigation, any problem-solving

| Pattern | Role in Family |
|---------|----------------|
| 006: Verification-First | Foundation — verify before acting |
| 042: Investigation-Only Protocol | Investigate without fixing (restraint) |
| 060: Cascade Investigation | Audit category when fixing (breadth) |
| 041: Systematic Fix Planning | Plan multi-issue resolution |
| 043: Defense-in-Depth Prevention | Prevent recurrence after fix |

**Quick reference**: 006 verifies → 042 investigates → 060 cascades → 041 plans → 043 prevents

---

### Grammar Application Family

**Patterns**: 050, 051, 052, 053, 054, 055, 056, 057, 058
**Lead Pattern**: [Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md) ← Start here (structural foundation)
**Health**: Strong
**Use when**: New feature development, UX work, intent classification

| Pattern | Role in Family |
|---------|----------------|
| 050: Context Dataclass Pair | Structural foundation for grammar awareness |
| 051: Parallel Place Gathering | Synthesize from multiple integrations |
| 052: Personality Bridge | Transform data into Piper's voice |
| 053: Warmth Calibration | Calibrate emotional tone |
| 054: Honest Failure with Suggestion | Handle failures gracefully |
| 055: Multi-Intent Decomposition | Handle multiple intents |
| 056: Consciousness Attribute Layering | Layer consciousness through processing |
| 057: Grammar-Driven Classification | Use grammar for intent routing |
| 058: Ownership Graph Navigation | Navigate object relationships |

**Quick reference**: Apply all 9 for "Conscious" rating on features. Features adopting partial set achieve lower ratings.

---

## Tier 2: Emerging Families

_Pattern groups with initial evidence but not yet proven across multiple contexts._

### Multi-Agent Coordination Family

**Patterns**: 010, 021, 029, 037, 059
**Lead Pattern**: [Pattern-059: Leadership Caucus](pattern-059-leadership-caucus.md) ← Start here for decisions; [Pattern-029](pattern-029-multi-agent-coordination.md) for execution
**Health**: Medium
**Use when**: Cross-domain decisions, parallel agent work, multi-advisor alignment

| Pattern | Role in Family |
|---------|----------------|
| 059: Leadership Caucus | Sync multi-advisor alignment (before work) |
| 029: Multi-Agent Coordination | Technical agent coordination (during work) |
| 010: Cross-Validation Protocol | Agents verify each other's outputs |
| 021: Development Session Management | Session handoffs and continuity |
| 037: Cross-Context Validation | Validate concepts across contexts |

**Quick reference**: 059 decides → 029 executes → 010 validates. Use 021 for session continuity, 037 for concept validation.

**Note**: Pattern-059 (leadership alignment) and Pattern-029 (technical execution) are complementary, not competing. See differentiation sections in each pattern.

---

### Analysis & Discovery Family

**Patterns**: 036, 037, 038, 039
**Lead Pattern**: [Pattern-036: Signal Convergence](pattern-036-signal-convergence.md) ← Start here (meta-pattern)
**Health**: Experimental
**Use when**: System analysis, pattern detection, feature prioritization

| Pattern | Role in Family |
|---------|----------------|
| 036: Signal Convergence | Detect breakthroughs via multi-analyzer signals |
| 037: Cross-Context Validation | Validate concepts across contexts |
| 038: Temporal Clustering | Analyze coordination via time grouping |
| 039: Feature Prioritization Scorecard | Quantified feature prioritization |

**Quick reference**: Second-order methodology — patterns about detecting patterns. Use when analyzing system behavior or prioritizing work.

---

## Tier 3: Unaffiliated Patterns

_Patterns not yet assigned to a family. May join existing families or form new ones._

### Architecture & Data Patterns

**Patterns**: 001-008, 013-017, 023, 025, 026, 034, 035, 040, 048
**Health**: Unknown — **HEALTH CHECK PENDING** (Lead Dev, before Feb 17)

Core system architecture, data access, and infrastructure patterns. These may be "invisible through success" (Meta-Pattern 3) or drifting. The Feb 17 code archaeology will determine:
- Which patterns are fully internalized (mature)
- Which patterns need reinforcement (drifting)
- Whether sub-families are warranted

**Pending**: Do not split into sub-families until health check results are available.

---

### Integration & Platform Patterns

**Patterns**: 018, 027, 030, 031, 033, 035, 044

Plugin architecture and external system integration. Includes MCP adapter patterns and plugin interface standards.

---

### AI & Intelligence Patterns

**Patterns**: 012, 019, 020, 022, 028, 032

LLM integration, spatial intelligence, and intent classification infrastructure.

---

### Standalone Process Patterns

**Patterns**: 009, 011, 024

Process and methodology patterns that don't naturally cluster with others:
- 009: GitHub Issue Tracking
- 011: Context Resolution
- 024: Methodology Patterns

---

## Using This Index

### At Session Start

Note which families apply to your work:

```markdown
**Active pattern families this session**: [Completion Theater, Investigation]
```

### In Gameplans

Include a checklist:

```markdown
## Applicable Pattern Families
- [ ] Completion Theater (multi-phase work)
- [ ] Investigation (bug-related work)
- [ ] Grammar Application (feature development)
- [ ] Multi-Agent Coordination (cross-domain decisions)
```

### When Unsure

1. Start with the **lead pattern** for the relevant family
2. The lead pattern will reference others in the family
3. Apply the family as a unit, not individual patterns in isolation

---

## Maintenance

- **During pattern sweeps**: Review family assignments, tier classifications, health status
- **New patterns**: Start as unaffiliated; assign to family during next sweep
- **Proto-patterns**: See [PROTO-PATTERNS.md](PROTO-PATTERNS.md) for candidates not yet formalized

---

_Created: February 5, 2026_
_Per CIO approval (memo-cio-to-docs-deliverables-approved-2026-02-05)_
_Related: [README.md](README.md) (category index), [META-PATTERNS.md](META-PATTERNS.md) (meta-patterns)_
