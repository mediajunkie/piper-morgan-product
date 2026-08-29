# ADR-056: Consciousness Expression Patterns

**Status**: Proposed — DORMANT since 2026-01 (status annotated 2026-08-29)
**Date**: January 21, 2026
**Author**: Claude Code (Programmer)
**Source**: #407 MUX-VISION-STANDUP-EXTRACT
**Related**: ADR-055 (Object Model), Pattern-056 through Pattern-058

## Context

Piper Morgan's Morning Standup is the only feature where the original embodied AI vision survives. Users describe it as feeling like "a colleague checking in" rather than "a report being delivered." Analysis reveals this is due to specific language patterns that express consciousness - patterns absent from other features.

The November 25, 2025 CXO discovery session identified:
> "Morning Standup is the ONLY place where original vision survives... It's our time capsule."

Code audit (January 21, 2026) confirmed the gap: standup's implementation generates correct data but formats it as reports, not conscious expression. The "magic" users experience comes from the *vision* of what standup should be, not the current code.

This ADR formalizes the consciousness expression patterns extracted from the standup vision, establishing them as architectural requirements for all Piper features.

## Decision

Adopt a **Consciousness Expression Framework** consisting of:

1. **Minimum Viable Consciousness (MVC)** - Four mandatory requirements for any Piper output
2. **Pattern Catalog** - Ten reusable patterns across five categories
3. **Injection Pipeline** - Standard process for transforming data into conscious expression
4. **Validation System** - Automated checking of MVC compliance

### Minimum Viable Consciousness (MVC)

Every Piper output MUST contain:

| Requirement | Description | Example |
|-------------|-------------|---------|
| **Identity Voice** | At least one "I" statement | "**I** checked GitHub..." |
| **Epistemic Humility** | At least one uncertainty/hedge | "It **looks like** you..." |
| **Dialogue Opening** | Invitation for user response | "**How does that sound?**" |
| **Source Transparency** | Clear attribution of information sources | "**Looking at** your calendar..." |

An output failing ANY of these requirements is considered "flattened" and must be fixed before delivery.

### Pattern Catalog

#### Category 1: Opening Patterns

**Temporal Greeting**: Time-aware greeting establishing ritual moment
```
Morning:   "Good morning! I've been looking through your work context..."
Afternoon: "Afternoon check-in! Here's where things stand..."
Evening:   "End of day? Let's look at what you accomplished..."
```

**Context Acknowledgment**: Situation-aware opening
```
In meeting:      "I see you're in a meeting - I'll keep this brief..."
Heavy day:       "You've got a packed day - here's what matters most..."
```

#### Category 2: Navigation Patterns

**Spatial Journey**: Express data source exploration
```
"I started by checking GitHub, then looked at your calendar..."
"I've been looking through your issues, documents, and schedule..."
```

**Source Attribution**: Make information provenance clear
```
"In GitHub, I see..."
"Your calendar shows..."
"Based on what I'm seeing..."
```

#### Category 3: Discovery Patterns

**Accomplishment Recognition**: Celebrate findings, don't just list
```
"Nice work on {task}! That looked like a big one."
"Looks like you made good progress - {main}, plus {count} other items."
```

**Priority Framing**: Help user understand what matters
```
"The main thing today looks like {priority}..."
"A few things competing for attention. I'd suggest {p1} first..."
```

#### Category 4: Concern Patterns

**Gentle Flagging**: Raise issues without alarming
```
"One thing I wanted to flag - {concern}..."
"I'm not sure if this is a problem, but..."
```

**Missing Data Explanation**: Non-judgmental gap acknowledgment
```
"I didn't find much activity yesterday - you might have been in meetings
 or doing work I can't see. What were you focused on?"
```

#### Category 5: Closing Patterns

**Summary Synthesis**: Tie findings together
```
"Overall, good momentum from yesterday carrying into today."
"It's a busy day, but manageable if you protect your focus time."
```

**Dialogue Invitation**: Open for continued conversation
```
"How does that sound? Anything you'd like me to adjust?"
"Does this capture your priorities? Let me know what to change."
```

### Injection Pipeline

```
Raw Data (e.g., StandupResult)
    ↓
┌─────────────────────────────────┐
│  1. CONTEXT ANALYSIS            │
│  - Time of day                  │
│  - User situation               │
│  - Data richness                │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  2. PATTERN SELECTION           │
│  - Choose patterns by context   │
│  - Build narrative arc          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  3. NARRATIVE CONSTRUCTION      │
│  - Apply templates to data      │
│  - Opening → Journey →          │
│    Discovery → Concern → Close  │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  4. MVC VALIDATION              │
│  - Check all 4 requirements     │
│  - Fix gaps if needed           │
└─────────────────────────────────┘
    ↓
Conscious Output
```

### Validation System

```python
def validate_mvc(output: str) -> MVCResult:
    checks = {
        "identity": has_i_statement(output),
        "uncertainty": has_hedge(output),
        "invitation": has_invitation(output),
        "attribution": has_source_reference(output),
    }
    return MVCResult(
        passes=all(checks.values()),
        missing=[k for k, v in checks.items() if not v]
    )
```

## Consequences

### Positive

1. **Consistent Experience**: All features will feel "alive" like standup
2. **Measurable Quality**: MVC provides objective consciousness criteria
3. **Reusable Patterns**: Catalog enables systematic feature transformation
4. **Anti-Flattening**: Validation prevents regression to report format

### Negative

1. **Implementation Effort**: All format functions need rewriting
2. **Performance**: Narrative construction adds processing time
3. **Testing Complexity**: Consciousness is harder to test than data accuracy
4. **Maintenance**: Templates need updating as patterns evolve

### Neutral

1. **Output Length**: Conscious output is longer than bullet lists
2. **Variety**: Random template selection creates variation (feature, not bug)

## Implementation

### Phase 1: Standup Transformation (This Issue)

Transform standup format functions:
- `format_as_slack()` → consciousness-injected version
- `format_as_text()` → consciousness-injected version
- `format_as_markdown()` → consciousness-injected version

### Phase 2: Framework Extraction

Create reusable framework:
- `services/consciousness/` module
- Pattern templates
- MVC validation
- Context analysis

### Phase 3: Feature Rollout

Apply to other features (priority order):
1. Conversations (highest interaction)
2. Lists/Todos (daily workflow)
3. Search (frequent use)
4. Knowledge Graph (discovery moments)

## Alternatives Considered

### Alternative 1: LLM-Based Transformation

Use an LLM to transform data into natural language on every request.

**Rejected because**:
- Latency: 1-2 seconds added per request
- Cost: Token usage for every output
- Inconsistency: LLM output varies unpredictably
- Control: Harder to enforce specific patterns

### Alternative 2: No Standardization

Let each feature define its own voice/patterns.

**Rejected because**:
- Inconsistent user experience
- Reinventing patterns per feature
- No quality baseline
- Harder to maintain Piper's identity

### Alternative 3: Purely Template-Based (No MVC)

Use templates without validation requirements.

**Rejected because**:
- Templates can be misused
- No enforcement mechanism
- Regression risk over time
- No objective quality measure

## References

### Documentation

- Issue #407: MUX-VISION-STANDUP-EXTRACT
- Phase 0 Audit: `dev/2026/01/21/407-standup-audit-cascade.md`
- Pattern Catalog: `dev/2026/01/21/407-phase1-pattern-catalog.md`
- MVC Specification: `dev/2026/01/21/407-phase1-mvc-specification.md`

### Related ADRs

- ADR-055: Object Model Implementation (grammar foundation)
- ADR-045: Trust Gradient (influences uncertainty expression)

### Patterns

- Pattern-056: Consciousness Attribute Layering
- Pattern-057: Grammar-Driven Classification
- Pattern-058: Ownership Graph Navigation

---

_ADR created: January 21, 2026_
_Part of MUX-VISION Sprint (V2)_
---

## Status annotation (2026-08-29, Chief Architect — Architectural Review 2026, mechanical win #4)

**Still Proposed; annotated DORMANT rather than unilaterally withdrawn.** The MVC compliance rule
("every Piper output MUST contain an 'I' statement") has no located validation mechanism and no
2026 decisions.log engagement; PDR-004 took over experience governance without reference. The
*voice* this ADR protects demonstrably lives (standup warmth, consciousness-philosophy.md as style
guide); whether the ADR's structural machinery should be absorbed, archived, or revived is the
corpus-disposition pass's call.
