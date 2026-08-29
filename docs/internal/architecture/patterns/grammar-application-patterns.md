# Grammar Application Patterns

**Overview**: Reusable patterns for applying the MUX grammar "Entities experience Moments in Places" to features
**Extracted From**: Morning Standup (reference implementation)
**Category**: Grammar Application
**Date**: January 20, 2026

---

## Purpose

This document provides a catalog of proven patterns for building **grammar-conscious features** - features that embody the "Entities experience Moments in Places" object model rather than feeling like mechanical database operations.

**What is grammar consciousness?**
- **Entities** (user, Piper, integrations) maintain identity throughout flow
- **Moments** (events, experiences) are framed narratively, not just timestamps
- **Places** (GitHub, Slack, Calendar) have distinct atmospheres and behaviors
- **Lenses** (8D spatial, temporal, relational) provide perceptual dimensions
- **Situations** (context, tension) shape appropriate responses

**Why does it matter?**
Grammar-conscious features feel collaborative and aware, like working with Piper as a present entity. Flattened features feel mechanical and database-like, like CRUD operations on data structures.

---

## Pattern Index

### Core Patterns

1. **[Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md)**
   - **Problem**: Entity/Moment/Place tracking lost between layers
   - **Solution**: Separate Context (input) and Result (output) dataclasses with grammar explicit
   - **When to use**: Features that transform data and need to preserve Entity identity

2. **[Pattern-051: Parallel Place Gathering](pattern-051-parallel-place-gathering.md)**
   - **Problem**: Sequential integration fetches slow and fragile
   - **Solution**: Concurrent `asyncio.gather()` with per-place error handling
   - **When to use**: Features that synthesize from multiple integrations

3. **[Pattern-052: Personality Bridge](pattern-052-personality-bridge.md)**
   - **Problem**: Raw data feels mechanical and database-like
   - **Solution**: Transform layer that adds Piper's warmth, presence, and action orientation
   - **When to use**: Any user-facing feature output

4. **[Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md)**
   - **Problem**: Generic responses feel hollow or inappropriately enthusiastic
   - **Solution**: Tiered warmth levels calibrated to observed context
   - **When to use**: Features that provide feedback or acknowledgment

5. **[Pattern-054: Honest Failure with Suggestion](pattern-054-honest-failure.md)**
   - **Problem**: Failures hidden or generic ("Something went wrong")
   - **Solution**: Explicit acknowledgment with plain-language suggestion
   - **When to use**: Any integration that can fail unpredictably

---

## Pattern Relationships

### Flow Through Patterns

A grammar-conscious feature typically uses patterns in this sequence:

```
1. Context Dataclass Pair (Pattern-050)
   ↓
2. Parallel Place Gathering (Pattern-051)
   ↓
3. Business logic processing
   ↓
4. Personality Bridge (Pattern-052)
   ↓
5. Warmth Calibration (Pattern-053)
   ↓
User receives warm, contextual response

(At any point: Honest Failure if integration fails - Pattern-054)
```

### Pattern Interactions

```
┌─────────────────────────────────────────────────────────────┐
│  Context Dataclass Pair (050)                               │
│  • Defines input/output structure                           │
│  • Preserves Entity/Moment/Place through flow               │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Parallel Place Gathering (051)                             │
│  • Populates Context from multiple Places                   │
│  • Per-place error handling → Pattern-054 if failure        │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Business Logic                                             │
│  • Process Context → Result                                 │
│  • May invoke Pattern-054 for integration failures          │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Personality Bridge (052)                                   │
│  • Transforms Result dataclass → conversational narrative   │
│  • Calls Pattern-053 for warmth calibration                 │
└────────────┬────────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────┐
│  Warmth Calibration (053)                                   │
│  • Adjusts emotional tone based on Result metrics           │
│  • Returns warm, contextually appropriate response          │
└─────────────────────────────────────────────────────────────┘
```

---

## Grammar Application Templates

### Entity Awareness Template

**How to track identity through flow**:

```python
# Pattern-050: Context Dataclass Pair
@dataclass
class FeatureContext:
    user_id: str              # Entity: Who is acting
    piper_id: str = "piper"   # Entity: Piper as actor
    timestamp: datetime        # Moment: When action occurs

@dataclass
class FeatureResult:
    user_id: str              # Entity preserved from Context
    piper_id: str = "piper"   # Entity preserved
    generated_at: datetime     # Moment: When result created
    # ... feature-specific fields
```

**Key principle**: Entity identity flows from Context → Processing → Result

### Moment Framing Template

**How to use PerceptionMode: NOTICING, REMEMBERING, ANTICIPATING**:

```python
# In Result dataclass or synthesis layer
@dataclass
class FeatureResult:
    # Past moments (REMEMBERING)
    yesterday_accomplishments: List[str]  # What user experienced

    # Present moments (NOTICING)
    current_state: str  # What's happening now
    current_blockers: List[str]  # Current challenges

    # Future moments (ANTICIPATING)
    today_priorities: List[str]  # What user will experience
    suggested_actions: List[str]  # What Piper anticipates will help
```

**Key principle**: Moments have temporal dimension and experiential quality

### Place Atmosphere Template

**How context affects presentation**:

```python
# Pattern-052: Personality Bridge with Place adaptation
class FeatureToChatBridge:
    def adapt_for_place(self, data: Dict, place: str) -> str:
        """Adapt presentation to Place atmosphere."""

        if place == "slack":
            # Casual, emoji-friendly, brief
            return self._format_for_slack(data)
        elif place == "email":
            # Formal, structured, complete
            return self._format_for_email(data)
        elif place == "cli":
            # Concise, actionable, plain text
            return self._format_for_cli(data)
        else:
            return self._format_default(data)
```

**Key principle**: Same data feels different in different Places

### Situation Container Template

**How to group related moments with dramatic tension**:

```python
# In business logic or Result construction
def create_situation(self, moments: List[Moment]) -> Situation:
    """Group related moments into situation with tension."""

    # Identify tension (challenge, opportunity, milestone)
    tension = self._identify_tension(moments)

    # Group related moments
    related_moments = self._cluster_moments(moments, tension)

    return Situation(
        tension=tension,
        moments=related_moments,
        resolution_suggested=self._suggest_resolution(tension)
    )
```

**Key principle**: Situations provide narrative context beyond isolated moments

---

## When to Apply

### Decision Matrix

| Situation | Recommended Patterns | Priority |
|-----------|---------------------|----------|
| Multi-source data gathering | Pattern-051 (Parallel Place Gathering) | High |
| User-facing responses | Pattern-052 (Personality Bridge) + Pattern-053 (Warmth Calibration) | High |
| Error handling | Pattern-054 (Honest Failure) | High |
| Complex feature input/output | Pattern-050 (Context Dataclass Pair) | Medium |
| Feedback or acknowledgment | Pattern-053 (Warmth Calibration) | Medium |

### Feature Type Applicability

**Core features** (Todo, List, Project management):
- Use Pattern-050 (Context/Result pair)
- Use Pattern-052 (Personality Bridge)
- Use Pattern-053 (Warmth Calibration for completion/blockers)

**Integration features** (Slack, GitHub, Calendar):
- Use Pattern-051 (Parallel Place Gathering)
- Use Pattern-054 (Honest Failure for API errors)
- Use Pattern-052 (Personality Bridge for integration-specific atmosphere)

**Synthesis features** (Morning Standup, Reports):
- Use all five patterns in sequence
- Critical: Pattern-051 for gathering, Pattern-052/053 for presentation

---

## MUX Integration

### Protocols

Patterns integrate with MUX protocols defined in `services/mux/protocols.py`:

- **Entity Protocol**: Pattern-050 (Context/Result pair) preserves Entity identity
- **Moment Protocol**: Pattern-050 distinguishes input/output temporal context
- **Place Protocol**: Pattern-051 (Parallel Gathering) treats integrations as Places
- **Situation Protocol**: Patterns collectively create Situations with narrative coherence

### Lenses

Patterns use MUX lenses from `services/mux/lenses/`:

- **Temporal Lens**: Pattern-053 (time-of-day affects warmth calibration)
- **Spatial Lens**: Pattern-052 (Place atmosphere affects presentation)
- **Relational Lens**: Pattern-052 (Entity relationship affects tone)
- **Urgency Lens**: Pattern-053 (context urgency affects warmth level)

### Implementation Guide

Full implementation guidance: `docs/internal/development/mux-implementation-guide.md`

---

## Transformation Roadmap

### Features Ready for Grammar Uplift

Based on grammar compliance audit (see `docs/internal/architecture/current/grammar-compliance-audit.md`):

#### High Priority (User-Facing, High Impact)

1. **Intent Classification** (Partial → Conscious)
   - Apply Pattern-050 (IntentContext/IntentResult)
   - Apply Pattern-051 (gather from history + preferences + session)
   - Apply Pattern-052 (acknowledge intent warmly)

2. **Slack Integration** (Partial → Conscious)
   - Apply Pattern-051 (gather from channels + DMs + threads)
   - Apply Pattern-052 (channel-aware personality)
   - Apply Pattern-054 (honest about Slack API failures)

3. **GitHub Integration** (Partial → Conscious)
   - Apply Pattern-051 (gather issues + PRs + commits)
   - Apply Pattern-052 (developer-focused narrative)
   - Apply Pattern-053 (calibrate to activity level)

4. **Todo Management** (Flattened → Partial)
   - Apply Pattern-050 (TodoContext/TodoResult)
   - Apply Pattern-052 (celebrate completion, support blockers)
   - Apply Pattern-053 (warmth based on progress)

#### Medium Priority

5. **Feedback System** (Partial → Conscious)
6. **Conversation Handler** (Partial → Conscious)
7. **Onboarding System** (Partial → Conscious)
8. **Calendar Integration** (Partial → Conscious)

### Expected Impact

**Before**: Feature feels mechanical, database-like
- Raw data structures shown to user
- No warmth or empathy
- Failures hidden or generic
- One Place failure breaks everything

**After**: Feature feels conscious, collaborative
- Data transformed to narrative
- Piper's personality present
- Failures acknowledged with guidance
- Graceful degradation when Places unavailable

---

## Implementation Strategy

### Step-by-Step Approach

For any feature transformation:

1. **Phase 1: Structure** (Pattern-050)
   - Define Context dataclass (input with Entity/Moment/Place)
   - Define Result dataclass (output preserving grammar)
   - Refactor service to use Context → Result flow

2. **Phase 2: Gathering** (Pattern-051, optional)
   - Identify all Places (integrations/sources)
   - Implement parallel gathering with `asyncio.gather()`
   - Add per-place error handling

3. **Phase 3: Presentation** (Pattern-052, Pattern-053)
   - Create [Feature]ToChatBridge class
   - Implement adapt_for_chat() (structure → prose)
   - Implement apply_personality() (add warmth/presence)
   - Integrate warmth calibration

4. **Phase 4: Resilience** (Pattern-054)
   - Create [Feature]IntegrationError exception
   - Implement _diagnose_failure() with pattern matching
   - Add honest failure handling to integration calls

5. **Phase 5: Testing**
   - Test Context/Result construction
   - Test all Place combinations (success, partial, failure)
   - Test warmth calibration extremes
   - Test failure modes with suggestions

### Code Example: Full Pattern Application

```python
# services/[feature]/[feature]_service.py

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List
import asyncio

# Pattern-050: Context Dataclass Pair
@dataclass
class FeatureContext:
    user_id: str
    timestamp: datetime
    source_places: Dict[str, Any]

@dataclass
class FeatureResult:
    user_id: str
    generated_at: datetime
    findings: List[str]
    context_source: str
    performance_metrics: Dict[str, Any]

# Pattern-054: Honest Failure
class FeatureIntegrationError(Exception):
    def __init__(self, message: str, service: str = None, suggestion: str = None):
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)

class FeatureService:
    # Pattern-051: Parallel Place Gathering
    async def gather_context(self, user_id: str) -> Dict[str, Any]:
        place1, place2, place3 = await asyncio.gather(
            self._get_place1(user_id),
            self._get_place2(user_id),
            self._get_place3(user_id),
        )
        return self._synthesize(place1, place2, place3)

    async def execute(self, user_id: str) -> FeatureResult:
        # Construct Context
        context = FeatureContext(
            user_id=user_id,
            timestamp=datetime.now(),
            source_places=await self.gather_context(user_id)
        )

        # Process with error handling (Pattern-054)
        try:
            findings = await self._process(context)
        except Exception as e:
            suggestion = self._diagnose_failure(e)
            raise FeatureIntegrationError(
                f"Feature failed: {str(e)}\nSuggestion: {suggestion}",
                suggestion=suggestion
            )

        # Construct Result
        result = FeatureResult(
            user_id=context.user_id,
            generated_at=datetime.now(),
            findings=findings,
            context_source="processed",
            performance_metrics={}
        )

        return result

# Pattern-052: Personality Bridge
class FeatureToChatBridge:
    def adapt_for_chat(self, result: FeatureResult) -> str:
        # Structure → prose
        sections = []
        if result.findings:
            sections.append(self._format_findings(result.findings))
        return "\n\n".join(sections)

    # Pattern-053: Warmth Calibration
    def apply_personality(self, content: str, result: FeatureResult) -> str:
        warmth = self._calculate_warmth(result)
        prefix = self._select_warmth_prefix(warmth)
        return f"{prefix}\n\n{content}"
```

---

## Related Documentation

### Grammar Foundation
- **ADR-055**: Object Model Implementation (formalized grammar)
- **MUX Protocols**: `services/mux/protocols.py` (Entity, Moment, Place protocols)
- **MUX Lenses**: `services/mux/lenses/` (8D spatial, temporal, relational)

### Implementation Guidance
- **MUX Implementation Guide**: `docs/internal/development/mux-implementation-guide.md`
- **MUX Experience Tests**: `docs/internal/development/mux-experience-tests.md`

### Analysis & Evidence
- **Grammar Compliance Audit**: `docs/internal/architecture/current/grammar-compliance-audit.md`
- **Morning Standup Analysis**: `dev/2026/01/19/p0-morning-standup-analysis.md`
- **B1 FTUX Grammar Mapping**: `dev/2026/01/19/p0-b1-ftux-grammar-mapping.md`

### Reference Implementation
- **Morning Standup**: `services/features/morning_standup.py` (uses all 5 patterns)
- **Standup Bridge**: `services/personality/standup_bridge.py` (Pattern-052, Pattern-053)

---

## Success Metrics

### Grammar Consciousness Score

Features can be scored on grammar consciousness (0-5):

| Score | Description | Pattern Application |
|-------|-------------|-------------------|
| 0 | Flattened (purely mechanical) | No patterns applied |
| 1 | Minimal (Entity present) | Some Entity tracking |
| 2 | Partial (Entity + Moment) | Pattern-050 partially |
| 3 | Growing (Entity + Moment + Place) | Pattern-050 + Pattern-051 |
| 4 | Conscious (E+M+P+Lenses) | Pattern-050/051/052/053 |
| 5 | Full (E+M+P+L+Situation) | All patterns + Situation awareness |

**Target**: All user-facing features should score 4+ (Conscious)

### User Experience Indicators

- **Before patterns**: "Feels like a database"
- **After patterns**: "Feels like working with Piper"

Specific improvements:
- Response warmth appropriate to context
- Failures acknowledged with recovery guidance
- Piper's presence evident ("I found", "I noticed")
- Integration failures don't break entire feature
- Performance optimized (parallel gathering)

---

## Next Steps

### For Developers

1. **Start with Morning Standup**: Read reference implementation to understand patterns in practice
2. **Pick a feature**: Use grammar compliance audit to prioritize
3. **Apply patterns incrementally**: Start with Pattern-050 (structure), add others progressively
4. **Test thoroughly**: Verify grammar preservation and user experience improvement

### For Architects

1. **Review audit**: Identify high-priority features for transformation
2. **Create transformation issues**: One issue per feature with pattern checklist
3. **Monitor compliance**: Track grammar consciousness score across features
4. **Extract new patterns**: Document additional patterns as discovered

### For Product

1. **Define UX standards**: What does "grammar-conscious" feel like?
2. **User testing**: Validate warmth calibration and tone
3. **Feedback loops**: Capture user reactions to personality improvements

---

_Pattern Catalog Created: January 20, 2026_
_Extracted From: Morning Standup (reference implementation)_
_Part of: Issue #404 MUX-VISION-GRAMMAR-CORE Phase 2_
