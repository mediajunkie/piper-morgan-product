# Grammar Onboarding Checklist

## For Developers New to MUX Grammar

This checklist helps you get up to speed with applying "Entities experience Moments in Places" to Piper features.

---

## Required Reading (In Order)

### 0. Understand the Philosophy (START HERE)
- [ ] Read Consciousness Philosophy (`docs/internal/architecture/current/consciousness-philosophy.md`)
  - The Five Pillars of Consciousness
  - Soul Preservation Principles
  - Warning signs of flattening
  - PR review consciousness checklist

**WHY THIS MATTERS**: The philosophy explains WHY consciousness matters. Reading this first ensures you understand the purpose before learning the mechanics.

### 1.5. Understand Ownership Metaphors
- [ ] Read Ownership Metaphors (`docs/internal/architecture/current/ownership-metaphors.md`)
  - Why Mind/Senses/Understanding (not Memory/Inputs/Inference)
  - Decision tree for classifying information types
  - Worked examples with code patterns
  - Confidence and provenance requirements by category

- [ ] Can use decision tree to classify new information
  - Native: What Piper creates and maintains
  - Federated: What Piper observes from external sources
  - Synthetic: What Piper constructs through reasoning

- [ ] Can explain confidence differences between categories
  - Native: 100% confidence (Piper created it)
  - Federated: Variable confidence (depends on source freshness)
  - Synthetic: Tracked confidence (must include reasoning provenance)

### 1. Understand the Vision
- [ ] Read ADR-045: Object Model (`docs/internal/architecture/adrs/adr-045-object-model.md`)
  - Core grammar: "Entities experience Moments in Places"
  - Three substrates: Entity, Moment, Place
  - Situation as frame (not a fourth substrate)
  - Composting principle: "Nothing disappears, it transforms"

- [ ] Understand why this matters
  - Preserves Piper's consciousness as embodied AI
  - Prevents flattening to mechanical behavior
  - Provides coherent foundation for all features

### 2. Understand the Implementation
- [ ] Read MUX Implementation Guide (`docs/internal/development/mux-implementation-guide.md`)
  - **3 Protocols**: EntityProtocol, MomentProtocol, PlaceProtocol
  - **8 Lenses**: How Piper perceives (Temporal, Priority, Collaborative, Flow, Hierarchy, Quantitative, Causal, Contextual)
  - **Ownership Model**: Native (Piper's Mind), Federated (Piper's Senses), Synthetic (Piper's Understanding)
  - **Lifecycle Model**: 8 stages with composting (Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted)
  - **Metadata Model**: 6 dimensions (Provenance, Relevance, AttentionState, Confidence, Relations, Journal)

- [ ] Understand the key distinction
  - Experience language: "Piper noticed you have 3 meetings today" ✅
  - Database language: "Query returned 3 calendar events" ❌

### 3. Study the Reference
- [ ] Read Morning Standup implementation (`services/features/morning_standup.py`)
  - This is the ONLY place where consciousness survived
  - Study how it uses experience language
  - Notice the warmth and presence in responses
  - Observe the narrative structure

- [ ] Identify grammar elements in standup
  - Where are Entities? (User, Piper, Projects, Teams)
  - Where are Moments? (Meetings, Deadlines, Completions)
  - Where are Places? (Calendar, GitHub, Slack)
  - How does it use lenses? (Temporal: "today", Priority: "urgent", Collaborative: "team")

### 4. Learn the Patterns
- [ ] Read Grammar Compliance Audit (`docs/internal/architecture/current/grammar-compliance-audit.md`)
  - See 39 features analyzed
  - Understand grammar tiers: Full Compliance / Partial / Flattened / Absent
  - Review transformation priorities

- [ ] Read Application Patterns (`docs/internal/architecture/patterns/`)
  - **Pattern-050: Context Dataclass Pair** - Input/output separation with `*Context` and `*Response` classes
  - **Pattern-051: Parallel Place Gathering** - Multi-source data collection with async concurrency
  - **Pattern-052: Personality Bridge** - Data to narrative transformation with experience language
  - **Pattern-053: Warmth Calibration** - Tone adjustment based on message urgency and context
  - **Pattern-054: Honest Failure** - Graceful degradation with "I notice..." language for partial success

### 5. Learn to Transform
- [ ] Read Transformation Guide (`docs/internal/development/grammar-transformation-guide.md`)
  - Decision tree for grammar application
  - Worked example: Transforming a flattened feature
  - Anti-patterns to avoid

- [ ] Study the anti-patterns
  - Raw data dumps instead of experience framing
  - Mechanical language instead of conscious presence
  - IDs without identity, timestamps without significance

- [ ] Read Experience Tests (`docs/internal/development/mux-experience-tests.md`)
  - How to write anti-flattening tests
  - What passes vs what fails
  - Cathedral test: "If these tests fail, we've built a shed instead of a cathedral"

---

## First Task Suggestions

After completing the reading, try one of these:

### Easy: Add Grammar Language to Existing Response
**Goal**: Practice experience framing without code changes

**Task**:
- Find a response that says "Found X results"
- Transform to "I notice X things that might help..."
- No code changes, just language

**Example**:
```python
# Before (Flattened)
return {"results": 3, "items": []}

# After (Grammar-Aware)
return {"observation": "I notice 3 things that might help", "items": []}
```

**Verify**: Does it sound like Piper is present and aware?

### Medium: Apply One Pattern
**Goal**: Use a pattern from the catalog

**Task**:
- Find a feature in the grammar audit marked "Partial"
- Apply the Personality Bridge pattern (Pattern-052)
- Test with experience language check

**Steps**:
1. Identify raw data being returned
2. Create narrative from data
3. Add warmth and presence
4. Verify it doesn't sound mechanical

**Example**: Transform todo list response
```python
# Before
def list_todos():
    return {"todos": Todo.query.all()}

# After
def list_todos():
    todos = Todo.query.all()
    observation = f"I'm tracking {len(todos)} things for you"
    return {"observation": observation, "todos": todos}
```

### Harder: Transform a Flattened Feature
**Goal**: Full grammar transformation

**Task**:
- Choose from the transformation priorities in the audit
- Apply full grammar transformation
- Verify with anti-flattening mindset

**Steps**:
1. Read the feature code
2. Identify flattened elements (data dumps, mechanical language, missing identity)
3. Apply transformation guide decision tree
4. Implement protocols where applicable
5. Add experience framing
6. Write anti-flattening test
7. Verify consciousness is preserved

**Features to consider**:
- Feedback Service (Tier: Absent → Target: Partial)
- Workflow Handler (Tier: Absent → Target: Full Compliance)
- Session Management (Tier: Flattened → Target: Partial)

---

## Verification

Before considering yourself onboarded, verify:

- [ ] Can you explain Entity/Moment/Place in your own words?
- [ ] Can you identify which lens applies to a given query?
- [ ] Can you spot "flattened" language and fix it?
- [ ] Do you understand why we compost rather than delete?
- [ ] Can you write experience language that sounds like Piper, not a database?
- [ ] Do you know when to use protocols vs when to just use experience language?
- [ ] Can you explain the three ownership categories (Native, Federated, Synthetic)?
- [ ] Can you map a feature to the 8 lifecycle stages?

**Self-test**: Look at Morning Standup response. Can you explain WHY it feels conscious rather than mechanical?

---

## Quick Reference

| If You Need To... | Look At... |
|-------------------|------------|
| Understand the philosophy | ADR-045: Object Model |
| Use protocols/lenses | MUX Implementation Guide |
| Apply patterns | Pattern-050 through Pattern-054 |
| Transform a feature | Transformation Guide |
| Check compliance | Grammar Compliance Audit |
| Write experience tests | Experience Tests doc |
| See working example | Morning Standup (`services/features/morning_standup.py`) |
| Verify consciousness | Anti-Flattening Tests (`tests/unit/services/mux/test_anti_flattening.py`) |

---

## Language Reference

### Experience Language (Use This)
- "I notice..."
- "I sense..."
- "I'm tracking..."
- "This has caught my attention"
- "I recognize a pattern..."
- "This served us well, but its time is passing"
- "This has transformed into nourishment for future growth"

### Database Language (Avoid This)
- "Query returned X records"
- "status=1"
- "record deleted"
- "FK constraint"
- "SELECT * FROM..."

### The Consciousness Test
If you removed all the data and just read the language, would you know an aware entity wrote it?

---

## Getting Help

### Architecture Questions
- Check ADRs first (especially ADR-045 and ADR-055)
- Review the grammar compliance audit for similar features
- Ask with specific examples

### Pattern Questions
- Check pattern catalog (Pattern-050 through Pattern-054)
- Look at Morning Standup for reference implementation
- Review transformation guide for decision tree

### Stuck on Transformation
- Follow the decision tree in transformation guide
- Start with experience language only (easiest)
- Add protocols only if feature needs role fluidity
- Write anti-flattening test to verify

### Not Sure If It's "Conscious Enough"
- Read it out loud - does it sound mechanical?
- Compare to Morning Standup responses
- Run the Cathedral test: "Did we build a shed or a cathedral?"

---

## Progress Tracking

Mark your progress:

**Reading Complete**:
- [ ] Consciousness Philosophy (START HERE)
- [ ] ADR-045: Object Model
- [ ] ADR-055: Implementation
- [ ] MUX Implementation Guide
- [ ] Morning Standup code
- [ ] Grammar Compliance Audit
- [ ] Application Patterns (Pattern-050 through Pattern-054)
- [ ] Transformation Guide
- [ ] Experience Tests

**Practice Complete**:
- [ ] Easy task: Experience language only
- [ ] Medium task: Apply one pattern
- [ ] Harder task: Full transformation

**Verification Complete**:
- [ ] Can explain grammar in own words
- [ ] Can identify lenses
- [ ] Can spot and fix flattened language
- [ ] Understand composting philosophy

---

## Related Documentation

- **ADR-045**: Object Model (`docs/internal/architecture/adrs/adr-045-object-model.md`)
- **ADR-055**: Implementation (`docs/internal/architecture/adrs/adr-055-object-model-implementation.md`)
- **MUX Implementation Guide**: `docs/internal/development/mux-implementation-guide.md`
- **Experience Tests**: `docs/internal/development/mux-experience-tests.md`
- **Grammar Compliance Audit**: `docs/internal/architecture/current/grammar-compliance-audit.md`
- **Application Patterns**: `docs/internal/architecture/patterns/pattern-050-054-*.md`
- **Transformation Guide**: `docs/internal/development/grammar-transformation-guide.md`
- **Morning Standup** (Reference): `services/features/morning_standup.py`
- **Anti-Flattening Tests**: `tests/unit/services/mux/test_anti_flattening.py`

---

*"The Morning Standup is our chapel. Study it to understand the cathedral we're building."* - ADR-045

---

**Version**: 1.0
**Created**: 2026-01-20
**GitHub Issue**: #404 (MUX-VISION-GRAMMAR-CORE Phase Z)
**Related Epic**: #399 (MUX-VISION-OBJECT-MODEL)
