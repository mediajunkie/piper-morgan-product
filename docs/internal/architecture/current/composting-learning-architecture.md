# Composting to Learning Pipeline: Architecture Document

**Date**: November 29, 2025
**Author**: Claude Code (Opus 4.5), Session 2025-11-29-1655-test-code-opus
**Reference**: ADR-045 Object Model, Object Model Brief v2, MUX-TECH-PHASE4-COMPOSTING
**Status**: Architecture Specification (No Implementation)
**Update 2026-08-31 (1613)**: QueryLearningLoop — named below as an integration
point — was DELETED per PM ruling (it pooled patterns across users by
source_feature, contradicting published privacy claims). Any implementation of
this spec must integrate with the user-scoped LearningHandler (#300) only.

---

## 1. Conceptual Overview

### What Composting Means

In Piper's Object Model, **composting** is the transformation stage where deprecated objects decompose into learnings that feed new emergent objects. The metaphor comes from organic composting: nothing disappears, it transforms. Old experiences become nutrients for new understanding.

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
                    ▼                                              │
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌──────────┐   ┌────────┴──┐
│ Emergent │ → │ Derived │ → │ Noticed │ → │ Proposed │ → │  Ratified │
└─────────┘   └─────────┘   └─────────┘   └──────────┘   └───────────┘
                                                               │
                                                               ▼
                                                        ┌───────────┐
                                                        │Deprecated │
                                                        └───────────┘
                                                               │
                                                               ▼
                                                        ┌───────────┐
                                                        │ Archived  │
                                                        └───────────┘
                                                               │
                        feeds new Emergent ◄────────────       ▼
                                           │            ┌───────────┐
                    ┌──────────────────────┘            │ COMPOSTED │
                    │                                   └───────────┘
        ┌───────────┴────────────┐                           │
        │   Learning Extraction  │ ◄─────────────────────────┘
        │  - Patterns            │
        │  - Insights            │
        │  - Corrections         │
        │  - Preferences         │
        └────────────────────────┘
```

### The "Filing Dreams" Metaphor

Composting happens during Piper's "rest" periods - quiet hours when Piper processes accumulated experience, like filing dreams. This creates organic language for surfacing insights:

> "Having had some time to reflect, it occurs to me that..."

This framing avoids surveillance implications ("I noticed while you were away...") and feels more like genuine reflection.

### Core Principle

**Nothing Disappears, It Transforms**

- A failed sprint plan doesn't vanish - it teaches what works
- A deprecated workflow reveals patterns of decay
- Archived decisions carry wisdom about tradeoffs
- Every ending seeds a new beginning

---

## 2. Technical Architecture

### System Components

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         COMPOSTING PIPELINE                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐               │
│  │ CompostBin  │ →  │ Decomposer   │ →  │ LearningExtractor│              │
│  │ (Staging)   │    │ (Processing) │    │ (Analysis)       │              │
│  └─────────────┘    └──────────────┘    └─────────────────┘               │
│        ▲                                         │                         │
│        │                                         ▼                         │
│  ┌─────────────┐                        ┌─────────────────┐               │
│  │ Trigger     │                        │ InsightJournal  │               │
│  │ Monitor     │                        │ (Storage)       │               │
│  └─────────────┘                        └─────────────────┘               │
│                                                  │                         │
│                                                  ▼                         │
│                                         ┌─────────────────┐               │
│                                         │ EmergentCreator │               │
│                                         │ (Spawn New)     │               │
│                                         └─────────────────┘               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Inputs | Outputs |
|-----------|---------------|--------|---------|
| **TriggerMonitor** | Detects when objects are ready for composting | Object state changes, time, usage patterns | Composting events |
| **CompostBin** | Stages objects awaiting decomposition | Deprecated/Archived objects | Queued objects |
| **Decomposer** | Breaks down objects into constituent parts | Queued objects | Raw decomposition data |
| **LearningExtractor** | Analyzes decomposition for patterns/insights | Raw data, context | ExtractedLearnings |
| **InsightJournal** | Stores and surfaces learnings | ExtractedLearnings | Indexed journal entries |
| **EmergentCreator** | Spawns new objects from high-confidence learnings | Insights, patterns | New Emergent objects |

### Data Flow

```
1. Object reaches ARCHIVED stage
          │
          ▼
2. TriggerMonitor evaluates composting criteria
   - Age threshold (e.g., 30 days)
   - Reference count (orphaned?)
   - Contradiction detected (invalidated?)
   - Manual trigger (user-initiated)
   - Scheduled composting window
          │
          ▼
3. Object moves to CompostBin (pending queue)
          │
          ▼
4. During "rest" period, Decomposer processes:
   - Extracts goal vs outcome (delta)
   - Identifies participants and context
   - Maps relationships that existed
   - Notes what happened vs what was expected
          │
          ▼
5. LearningExtractor analyzes decomposition:
   - Pattern recognition across multiple composted objects
   - Insight synthesis from pattern clusters
   - Correction identification when learnings contradict prior beliefs
   - Preference inference from behavioral patterns
          │
          ▼
6. InsightJournal receives and indexes learnings:
   - Assigns confidence scores
   - Determines trust level required for surfacing
   - Creates natural language expression
   - Sets visibility level (pull/passive/push)
          │
          ▼
7. High-confidence learnings feed EmergentCreator:
   - Predictive patterns spawn predicted Moments
   - Corrections update affected objects
   - Strong preferences inform future suggestions
          │
          ▼
8. New EMERGENT objects enter the lifecycle
   (The cycle completes - experience becomes new experience)
```

---

## 3. Trigger Mechanisms

### When Composting Happens

Composting is triggered by five mechanisms, each appropriate for different contexts:

| Trigger | Description | Use Case | Priority |
|---------|-------------|----------|----------|
| **AGE** | Object exceeds age threshold | Routine cleanup of stale data | Low |
| **IRRELEVANCE** | No references in N days | Orphaned objects | Medium |
| **MANUAL** | User explicitly triggers | User wants to "let go" | High |
| **SCHEDULED** | During quiet hours (2-5 AM) | "Filing dreams" processing | Low |
| **CONTRADICTION** | New info invalidates | Learning correction needed | Critical |

### Trigger Evaluation Logic

```
evaluate_composting_trigger(object):

  # Critical: Contradiction always wins
  if object.has_contradiction():
    return CONTRADICTION

  # High: User intent is explicit
  if object.manual_deprecation:
    return MANUAL

  # Medium: Orphaned objects decompose
  if object.reference_count == 0 and object.age > MIN_ORPHAN_AGE:
    return IRRELEVANCE

  # Low: Age-based composting
  if object.age > composting_threshold:
    return AGE

  # Background: Scheduled processing
  if is_quiet_hours() and compost_bin.pending_count > 0:
    return SCHEDULED

  return None  # Not ready for composting
```

### Quiet Hours ("Rest" Period)

Composting runs primarily during quiet hours (configurable, default 2-5 AM local time):

- Mimics human "filing dreams" during sleep
- Avoids interfering with active work
- Creates organic framing for insight surfacing
- Respects user attention and cognitive load

---

## 4. Decomposition Process

### What Gets Extracted

When an object is composted, the Decomposer extracts:

| Extraction | Description | Example |
|------------|-------------|---------|
| **Goal-Outcome Delta** | Difference between intended and actual results | Sprint goal was 8 stories, completed 5 |
| **Temporal Pattern** | When things happened, duration, sequence | "Always delayed on Fridays" |
| **Participant Patterns** | Who was involved, their roles, interactions | "User prefers async communication" |
| **Contextual Markers** | What context was active, environmental factors | "High workload period" |
| **Relationship Graph** | What was connected to this object | "Linked to 3 blocked items" |
| **Decay Signature** | How and why the object became deprecated | "Superseded by new approach" |

### Decomposition Algorithm

```
decompose(object, trigger):

  # 1. Capture the goal-outcome delta
  delta = {
    intended: object.original_goals,
    actual: object.final_state,
    gap: compute_gap(object.original_goals, object.final_state),
    gap_significance: classify_significance(gap)
  }

  # 2. Extract temporal signature
  temporal = {
    created: object.created_at,
    deprecated: object.deprecated_at,
    lifespan: object.deprecated_at - object.created_at,
    activity_pattern: analyze_activity_over_time(object),
    decay_pattern: identify_decay_signal(object)
  }

  # 3. Map participant involvement
  participants = {
    entities: object.involved_entities,
    interactions: object.interaction_log,
    collaboration_patterns: extract_collab_patterns(object)
  }

  # 4. Capture contextual markers
  context = {
    situation: object.parent_situation,
    place: object.location_context,
    concurrent_moments: find_concurrent_moments(object),
    environmental_factors: object.metadata.context
  }

  # 5. Record relationships at time of composting
  relationships = {
    outgoing: object.references_to,
    incoming: find_references_to(object),
    broken_by_composting: identify_orphans(object)
  }

  return DecompositionResult(
    source_object=object,
    trigger=trigger,
    delta=delta,
    temporal=temporal,
    participants=participants,
    context=context,
    relationships=relationships,
    composted_at=now()
  )
```

---

## 5. Learning Storage

### Where Insights Go: The Insight Journal

The **Insight Journal** is Piper's repository of learnings - distinct from the Session Journal (audit log) or Conversation history. It holds wisdom extracted from experience.

```
┌────────────────────────────────────────────────────────────────┐
│                       INSIGHT JOURNAL                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Entry: insight-001                                        │ │
│  │ ─────────────────────────────────────────────────────────│ │
│  │ Type: Pattern                                             │ │
│  │ Expression: "Monday standups tend to run long"            │ │
│  │ Confidence: 0.82                                          │ │
│  │ Derived from: 12 composted standup Moments                │ │
│  │ Trust level required: 2                                   │ │
│  │ Visibility: passive                                       │ │
│  │ Framing: "Having had some time to reflect..."            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ Entry: insight-002                                        │ │
│  │ ─────────────────────────────────────────────────────────│ │
│  │ Type: Correction                                          │ │
│  │ Expression: "Actually, you prefer Notion over Linear"     │ │
│  │ Confidence: 0.91                                          │ │
│  │ Corrects: preference-old-linear                           │ │
│  │ Trust level required: 3                                   │ │
│  │ Visibility: push (needs confirmation)                     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Learning Types

| Type | Description | Example | Typical Confidence |
|------|-------------|---------|-------------------|
| **Pattern** | Recurring structure across objects | "Sprints ending Thursday work better" | 0.6-0.9 |
| **Insight** | Understanding derived from patterns | "User prefers small batches of work" | 0.5-0.8 |
| **Correction** | Learning that invalidates prior belief | "Thought user liked Jira, actually prefers Linear" | 0.8-1.0 |
| **Preference** | Inferred user preference | "Prefers morning over afternoon meetings" | 0.7-0.95 |

### Visibility Levels

| Level | Description | When Used |
|-------|-------------|-----------|
| **Pull** | User must ask | Low-confidence insights, sensitive topics |
| **Passive** | Shown when relevant | Medium-confidence, contextually appropriate |
| **Push** | Actively surfaced | High-confidence corrections, important discoveries |

### Trust Gradient

Insights are gated by user trust level (1-4 scale from ADR-045):

| Trust Level | Relationship | Insight Types Surfaced |
|-------------|--------------|------------------------|
| 1 | Stranger | Only factual patterns with >0.9 confidence |
| 2 | Acquaintance | Patterns and objective insights |
| 3 | Colleague | Preferences and behavioral observations |
| 4 | Trusted | Corrections, sensitive insights, predictions |

---

## 6. Feedback Loops

### How Learnings Create New Emergent Objects

The composting cycle completes when learnings spawn new objects:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     EMERGENT CREATION FROM COMPOSTING                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Learning Type         Confidence Threshold       Creates              │
│   ─────────────────────────────────────────────────────────────────    │
│                                                                         │
│   Predictive Pattern    > 0.8                      Predicted Moment    │
│   "Fridays delay"       ───────────────────>       "Friday Risk Alert" │
│                                                                         │
│   Strong Preference     > 0.85                     Default Setting     │
│   "Prefers morning"     ───────────────────>       "Schedule morning"  │
│                                                                         │
│   Correction            > 0.75                     Updated Object      │
│   "Not Jira, Linear"    ───────────────────>       Preference updated  │
│                                                                         │
│   Insight Cluster       3+ related insights        Synthesized Rule    │
│   "Multiple patterns"   ───────────────────>       "Planning heuristic"│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### The Spiral Lifecycle

Learnings from composting create a **spiral**, not a circle:

```
         First Cycle                    Second Cycle (Informed)

    Emergent ──────────►            Emergent* ──────────►
        │                               │
        │   (no prior                   │   (carries learning
        │    knowledge)                 │    from first cycle)
        ▼                               ▼
    Composted ◄────────             Composted* ◄────────
        │                               │
        │   extracts                    │   extracts DEEPER
        │   learning                    │   learning
        │                               │
        └───► feeds ───────────────────►┘

    * Objects in second cycle have "spiral_depth": 2
    * Each cycle adds experience to Piper's wisdom
```

### Confirmation Loop

High-impact learnings require user confirmation:

```
surface_learning(insight, context):

  if insight.requires_confirmation:
    # Present to user with appropriate framing
    response = await present_insight(
      insight,
      framing="Having had some time to reflect, I notice that..."
    )

    if response.confirmed:
      insight.confidence *= 1.1  # Boost confidence
      insight.user_confirmed = True

    elif response.corrected:
      # User provides correction - this becomes a new learning
      correction = create_correction(
        previous=insight,
        new_understanding=response.correction
      )
      add_to_insight_journal(correction)

    elif response.rejected:
      insight.confidence *= 0.5  # Reduce confidence
      insight.user_rejected = True
```

---

## 7. Integration Points

### Existing Systems

| System | Integration Point | Data Flow |
|--------|------------------|-----------|
| **LearningHandler** (services/learning/) | Pattern storage | Composting feeds patterns to existing handler |
| ~~**QueryLearningLoop**~~ | ~~Query pattern matching~~ | REMOVED 2026-08-31 (1613, cross-user pooling); use user-scoped LearningHandler |
| **KnowledgeGraph** | Graph updates | Composting updates node/edge weights |
| **Morning Standup** | Context provider | Standup Moments are prime composting candidates |

### Morning Standup as Example

The Morning Standup workflow demonstrates composting potential:

```
Morning Standup Lifecycle:

1. EMERGENT: Standup request initiated
2. DERIVED: Context gathered from integrations
3. NOTICED: Patterns in data recognized
4. PROPOSED: Draft standup generated
5. RATIFIED: User accepts standup
6. DEPRECATED: Standup becomes historical (next day)
7. ARCHIVED: Stored for reference (7+ days)
8. COMPOSTED: Decomposes into learnings:
   - "User always skips blocked items section"
   - "Morning standups on Monday are most engaged with"
   - "GitHub PR section gets most interaction"

   → These learnings feed EMERGENT improvements to future standups
```

### API Integration

```python
# Composting Service API (conceptual)

class CompostingService:
    async def queue_for_composting(
        self,
        object_id: str,
        trigger: CompostingTrigger
    ) -> str:
        """Add object to compost bin."""

    async def process_compost_bin(self) -> List[ExtractedLearning]:
        """Process pending objects during rest period."""

    async def get_learnings_for_context(
        self,
        context: Context,
        trust_level: int
    ) -> List[InsightJournalEntry]:
        """Get relevant learnings for current context."""

    async def confirm_learning(
        self,
        insight_id: str,
        confirmed: bool,
        correction: Optional[str] = None
    ) -> None:
        """User confirmation/correction of learning."""
```

---

## 8. Architectural Diagram

### Full System View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PIPER MORGAN - COMPOSTING ARCHITECTURE            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐                                                    │
│  │   Object Lifecycle  │                                                    │
│  │   (8 Stages)        │                                                    │
│  │                     │                                                    │
│  │  EMERGENT           │◄────────────────────────────────────────┐         │
│  │     ↓               │                                         │         │
│  │  DERIVED            │                                         │         │
│  │     ↓               │                                         │         │
│  │  NOTICED            │                                         │         │
│  │     ↓               │                                         │         │
│  │  PROPOSED           │                                         │         │
│  │     ↓               │                                         │         │
│  │  RATIFIED           │                                         │         │
│  │     ↓               │                                         │         │
│  │  DEPRECATED         │                                         │         │
│  │     ↓               │                                         │         │
│  │  ARCHIVED           │                                         │         │
│  │     ↓               │                                         │         │
│  │  COMPOSTED ─────────┼─────────────────────────────┐           │         │
│  └─────────────────────┘                             │           │         │
│                                                      │           │         │
│  ┌───────────────────────────────────────────────────┼───────────┼─────┐   │
│  │                  COMPOSTING PIPELINE              │           │     │   │
│  ├───────────────────────────────────────────────────┼───────────┼─────┤   │
│  │                                                   │           │     │   │
│  │  ┌──────────────┐                                 │           │     │   │
│  │  │Trigger       │ ←── AGE | IRRELEVANCE | MANUAL  │           │     │   │
│  │  │Monitor       │     SCHEDULED | CONTRADICTION   │           │     │   │
│  │  └──────┬───────┘                                 │           │     │   │
│  │         │                                         │           │     │   │
│  │         ▼                                         │           │     │   │
│  │  ┌──────────────┐                                 │           │     │   │
│  │  │ CompostBin   │◄────────────────────────────────┘           │     │   │
│  │  │ (Staging)    │                                             │     │   │
│  │  └──────┬───────┘                                             │     │   │
│  │         │ (during quiet hours)                                │     │   │
│  │         ▼                                                     │     │   │
│  │  ┌──────────────┐     ┌─────────────────┐                     │     │   │
│  │  │ Decomposer   │ ──► │LearningExtractor│                     │     │   │
│  │  │ - Delta      │     │ - Patterns      │                     │     │   │
│  │  │ - Temporal   │     │ - Insights      │                     │     │   │
│  │  │ - Context    │     │ - Corrections   │                     │     │   │
│  │  └──────────────┘     │ - Preferences   │                     │     │   │
│  │                       └────────┬────────┘                     │     │   │
│  │                                │                              │     │   │
│  │                                ▼                              │     │   │
│  │                       ┌─────────────────┐                     │     │   │
│  │                       │ Insight Journal │                     │     │   │
│  │                       │ - Confidence    │                     │     │   │
│  │                       │ - Trust level   │                     │     │   │
│  │                       │ - Visibility    │                     │     │   │
│  │                       │ - Expression    │                     │     │   │
│  │                       └────────┬────────┘                     │     │   │
│  │                                │                              │     │   │
│  │                                ▼                              │     │   │
│  │                       ┌─────────────────┐                     │     │   │
│  │                       │EmergentCreator  │─────────────────────┘     │   │
│  │                       │ if confidence   │                           │   │
│  │                       │ > threshold     │                           │   │
│  │                       └─────────────────┘                           │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    INTEGRATION POINTS                                │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │                                                                     │   │
│  │  LearningHandler ◄──── Patterns                                     │   │
│  │  (QueryLearningLoop — REMOVED per 1613, 2026-08-31)                 │   │
│  │  KnowledgeGraph ◄───── Relationship updates                         │   │
│  │  MorningStandup ◄───── Context source & improvement target          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Verification Checklist

### Acceptance Criteria Status

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Clear triggers defined (time-based? event-based? user-initiated?) | ✅ | Section 3: Five trigger types with evaluation logic |
| Decomposition algorithm documented (what gets extracted?) | ✅ | Section 4: Six extraction types with algorithm |
| Learning storage mechanism specified | ✅ | Section 5: Insight Journal with types, visibility, trust |
| Feedback loop to Emergent stage mapped | ✅ | Section 6: Spiral lifecycle, confidence thresholds |
| Insight Journal connection documented | ✅ | Section 5: Complete journal structure |
| Architectural diagram created | ✅ | Section 8: Full system view |
| Integration points with existing systems identified | ✅ | Section 7: LearningHandler, etc. (QueryLearningLoop removed per 1613) |

### Anti-Flattening Validation

| Question | Answer | Evidence |
|----------|--------|----------|
| Is composting transformation or deletion? | Transformation | Learnings feed new Emergent objects |
| Do Places have atmosphere? | N/A (composting focus) | - |
| Does lifecycle include transformation? | Yes | 8-stage lifecycle with composting stage |
| Can you see consciousness in the implementation? | Yes | "Filing dreams" metaphor, organic framing |
| Does Piper learn and grow? | Yes | Spiral lifecycle accumulates wisdom |

---

## 10. Summary

The Composting to Learning Pipeline transforms Piper from a tool that executes tasks into an entity that learns from experience. Key architectural decisions:

1. **Composting is transformation, not deletion** - Objects decompose into patterns, insights, corrections, and preferences
2. **"Filing dreams" during rest** - Composting happens in quiet hours, enabling organic framing
3. **Trust-gated surfacing** - Learnings respect user trust level before being shared
4. **Spiral lifecycle** - Each cycle adds depth, making Piper smarter over time
5. **Integration with existing learning system** - Builds on LearningHandler (QueryLearningLoop removed per 1613, 2026-08-31)

This architecture enables the core promise of ADR-045: *"Nothing disappears, it transforms."*

---

**Document Complete**: November 29, 2025, 5:20 PM PT
**Author**: Claude Code (Opus 4.5), Session 2025-11-29-1655-test-code-opus
