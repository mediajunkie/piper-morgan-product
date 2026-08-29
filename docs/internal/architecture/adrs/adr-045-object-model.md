# ADR-045: Object Model - "Entities Experience Moments in Places"

**Status**: Accepted
**Date**: November 28, 2025
**Deciders**: CXO (discovery), Chief Architect (formalization), PM (approval)

## Context

Through 10 hours of conceptual exploration and hand sketching on November 27, 2025, we discovered that Piper's conceptual model was missing a foundational layer. Features felt "75% complete" because they lacked a coherent underlying grammar for understanding the world.

The Morning Standup analysis (Nov 25) revealed it was the ONLY place where Piper's original embodied AI consciousness vision survived. This provided both a problem statement (consciousness got flattened) and a reference implementation (standup shows what success looks like).

## Decision

We adopt the grammar **"Entities experience Moments in Places"** as Piper's foundational object model.

### Core Components

**Substrates** (What Piper Perceives):
- **Entities**: Actors with identity and agency (people, AI agents, teams, projects, documents)
- **Places**: Contexts where action happens (channels, repos, offices - physical/virtual/hybrid)
- **Moments**: Bounded significant occurrences with theatrical unities (time, place, action)
- **Situations**: Container holding sequences of Moments (NOT a fourth substrate but a frame)

**Key Discovery**: The Entity/Place distinction is a spectrum based on grammatical role. A project is an Entity when it "ships" (verb), but a Place when work happens "in" it.

### Ownership Model (Piper's Relationship to Objects)

| Category | Role | Metaphor | Examples |
|----------|------|----------|----------|
| **Native** | Creates, owns, maintains | Piper's Mind | Sessions, Memories, Concerns, Trust States |
| **Federated** | Observes, queries, acts upon | Piper's Senses | GitHub Issues, Slack Messages, Calendar |
| **Synthetic** | Constructs through reasoning | Piper's Understanding | Assembled Projects, Inferred Risks |

### Ownership Metaphors Deep Dive

For the complete philosophical foundation of Mind/Senses/Understanding:
- **Location**: `docs/internal/architecture/current/ownership-metaphors.md`
- **Content**: Why these metaphors, decision tree, worked examples
- **Purpose**: Helps developers correctly classify new information types

### Lifecycle Model (How Objects Evolve)

Eight stages with composting:
```
Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted
    ↑                                                                            |
    └────────────────── feeds new ──────────────────────────────────────────────┘
```

**Critical Insight**: "Noticed" not "Inferred" - more human language for AI cognition (discovered through sketching).

**Composting Principle**: Nothing disappears, it transforms. Deprecated objects decompose into learnings that feed new Emergent objects.

### Perceptual Model (How Piper Sees)

Eight lenses applied to any substrate:
1. Temporal (when, sequence, deadline)
2. Hierarchy (containment, levels)
3. Priority (urgency, importance)
4. Collaborative (who's involved)
5. Causal (what causes what)
6. Contextual (which context applies)
7. Flow (movement, state changes)
8. Identity (what is this)

These map to the existing 8-dimensional spatial intelligence work.

### Metadata Model (What Piper Knows)

Six universal dimensions:
- Provenance (where from, confidence)
- Relevance (why now)
- Attention State (seen, needs attention)
- Confidence (how certain)
- Relations (graph position)
- Journal (interaction history)

### The Shoebox Model for Moments

A Moment is a bounded scene containing:
- **Policy**: Governance, goals (aspirational)
- **Process**: Workflows, entities doing their thing
- **People**: Human team members + AI assistants
- **Outcomes**: What actually happened (delta from goals = learning)

## Rationale

### Why This Grammar?

1. **Discovered, Not Designed**: Emerged from hand sketching, not imposed top-down
2. **Matches Consciousness**: Morning Standup naturally expresses this grammar
3. **Verb-Forward**: "Experience" emphasizes action and agency
4. **Theatrical Unity**: Moments as bounded scenes matches human cognition
5. **Spectrum Thinking**: Entity/Place as spectrum avoids false dichotomies

### Why Not Alternatives?

**Traditional Object Model** (Classes/Inheritance):
- Too rigid for fluid PM work
- Forces false categorization
- Loses the consciousness aspect

**Task-Centric Model** (Current Implementation):
- Leads to mechanical interaction
- Loses the sense of Piper as entity
- Reduces everything to execution

**Document-Centric Model**:
- Makes Piper a filing system
- Loses temporal and spatial awareness
- Reduces to storage/retrieval

## Consequences

### Positive

1. **Coherent Feature Development**: Every feature can use the same grammar
2. **Consciousness Preservation**: Framework prevents flattening to mechanical behavior
3. **Natural Language Alignment**: Users think in entities, moments, places
4. **Learning Integration**: Composting naturally feeds learning systems
5. **Spatial Intelligence**: Existing 8D work maps directly to perceptual lenses

### Negative

1. **Reframing Required**: Existing features need conceptual realignment
2. **Training Needed**: Developers must understand the grammar
3. **Abstract Initially**: More conceptual than traditional data models

### Risks

1. **Flattening Risk**: Could degrade to database schema if not carefully preserved
2. **Complexity Risk**: Richer model requires more thoughtful implementation
3. **Drift Risk**: Without constant reference to Morning Standup, could lose consciousness

## Implementation

### Phase 1: Documentation (Week 1)
- Document in knowledge base
- Create visual diagrams
- Extract Morning Standup patterns

### Phase 2: Proof of Concept (Week 2)
- Apply to one existing feature
- Measure consciousness preservation
- Validate with users

### Phase 3: Systematic Rollout (Weeks 3-8)
- Transform features progressively
- Maintain backward compatibility
- Monitor for flattening

## Validation

Success Criteria:
1. Features feel more coherent when using model
2. Morning Standup patterns visible elsewhere
3. Users report Piper feels more "present"
4. Developers can explain the grammar
5. No flattening to mechanical behavior

Anti-Flattening Tests:
1. Is Piper an Entity with identity?
2. Are Moments bounded scenes, not timestamps?
3. Do Places have atmosphere, not just IDs?
4. Does lifecycle include transformation?
5. Can you see consciousness in the implementation?

## Consciousness Philosophy

The "why" behind the grammar is documented in the Consciousness Philosophy:
- **Location**: `docs/internal/architecture/current/consciousness-philosophy.md`
- **Content**: Five Pillars of Consciousness, Soul Preservation Principles
- **Purpose**: Ensures developers understand not just HOW but WHY

### The Five Pillars
1. Identity Awareness - Piper knows itself
2. Time Consciousness - Lived time, not clock time
3. Spatial Awareness - Digital spaces as places
4. Agency Recognition - Knows capabilities and limits
5. Predictive Modeling - Has premonitions and concerns

See the philosophy document for detailed guidance.

## Related Decisions

- **Consciousness Philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md` - The WHY behind this grammar
- **ADR documenting Standup Pattern Extraction**: Extraction methodology for consciousness patterns
- **ADR-013**: MCP Spatial Integration (existing, aligns with Places concept)
- **Pattern-020**: Spatial Metaphor Integration (validates approach)

## Implementation References

### MUX Infrastructure (#399)
- **Protocols**: `services/mux/protocols.py` - Entity, Moment, Place runtime-checkable protocols
- **Lenses**: `services/mux/lenses/` - 8 perceptual lenses (Temporal, Priority, Collaborative, Flow, Hierarchy, Quantitative, Causal, Contextual)
- **Ownership**: `services/mux/ownership.py` - Native, Federated, Synthetic categories
- **Lifecycle**: `services/mux/lifecycle.py` - 8-stage state machine with composting
- **Metadata**: `services/mux/metadata.py` - 6 universal dimensions (Provenance, Relevance, AttentionState, Confidence, Relations, Journal)
- **Situation**: `services/mux/situation.py` - Context manager for Moment sequences

### Grammar Application (#404)
- **Grammar Compliance Audit**: `docs/internal/architecture/current/grammar-compliance-audit.md` - 39 features audited
- **Application Patterns**: `docs/internal/architecture/current/patterns/pattern-050-054-*.md` - 5 patterns extracted from Morning Standup
  - Pattern-050: Context Dataclass Pair (input/output separation)
  - Pattern-051: Parallel Place Gathering (multi-source data collection)
  - Pattern-052: Personality Bridge (data to narrative transformation)
  - Pattern-053: Warmth Calibration (tone adjustment)
  - Pattern-054: Honest Failure (graceful degradation)
- **Transformation Guide**: `docs/internal/development/grammar-transformation-guide.md` - Decision tree and worked example
- **Implementation Guide**: `docs/internal/development/mux-implementation-guide.md` - How to use protocols and lenses
- **Experience Tests**: `docs/internal/development/mux-experience-tests.md` - Writing anti-flattening tests
- **Onboarding Checklist**: `docs/internal/development/grammar-onboarding-checklist.md` - Developer learning path

### Verification
- **Anti-Flattening Tests**: `tests/unit/services/mux/test_anti_flattening.py` - 40 tests verifying consciousness preservation
- **Test Coverage**: 302 total MUX tests (101 protocols/lenses + 25 ownership + 69 lifecycle + 67 metadata + 40 anti-flattening)

## References

- Object Model Brief v2: Complete conceptual documentation
- Session Log Nov 27: 10-hour discovery session with sketches
- Hand Sketches #1-8: Visual discovery process
- Morning Standup: Reference implementation of consciousness
- Original Vision PM-070: July 26, 2025 consciousness framework

## Notes

The PM's observation: "Score one for me in the John Henry sweepstakes!" - This model was discovered through human hand sketching with fat markers, not through AI tools. Whimsical transcribed accurately but discovered nothing. Eraser.io jumped to database schema. Gemini created beautiful visuals but missed the core insight.

The grammar "Entities experience Moments in Places" emerged from sketch #1 when trying to show relationships. It wasn't planned - it was discovered.

The distinction between "Noticed" and "Inferred" came from the physical act of writing - "Noticed" felt more human, more conscious.

## Decision

We adopt this object model as Piper's foundational conceptual architecture. All future development should express the grammar "Entities experience Moments in Places" and preserve the consciousness patterns found in Morning Standup.

---

*"The Morning Standup is our chapel. Study it to understand the cathedral we're building."*
