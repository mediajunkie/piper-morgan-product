# ADR-053: Trust Computation Architecture

**Status**: ACCEPTED
**Date**: 2026-01-13
**Accepted**: 2026-01-23
**Authors**: Chief Architect
**Deciders**: PM, CXO, PPM
**References**: PDR-002 (Conversational Glue), PDR-001 (FTUX), Ethics-First Architecture

---

## Context

### Problem Statement

PDR-002 establishes a Trust Gradient Model governing Piper's proactivity: users progress through four trust stages (New → Building → Established → Trusted) based on interaction history. The product requirements are defined; this ADR specifies the architectural implementation.

**Requirements from PDR-002**:
- Trust must be computed, stored, and queryable
- Trust is invisible to users but effects are noticeable
- Trust is discussable when users ask ("Why did you do that without asking?")
- Trust affects proactivity decisions throughout the system

### Design Constraints

From PDR-002 and CXO guidance:

1. **Invisible computation, visible effects**: No "Trust Level: Established" display
2. **Discussable on request**: Piper can explain trust-based behavior when asked
3. **Mirrors human relationships**: Incremental building, rapid loss possible
4. **"Thoughtful colleague" test**: Remember work context, not casual asides

### Current State

No trust computation infrastructure exists. Proactivity is currently hardcoded or absent. The preference learning system (standup domain) provides a pattern for interaction-based learning but doesn't track trust.

---

## Decision

### Core Model: UserTrustProfile

```python
# services/domain/models.py

class TrustStage(IntEnum):
    """Trust stages per PDR-002"""
    NEW = 1           # Respond to queries; no unsolicited help
    BUILDING = 2      # Offer related capabilities after task completion
    ESTABLISHED = 3   # Proactive suggestions based on observed context
    TRUSTED = 4       # Anticipate needs; "I'll do X unless you stop me"

@dataclass
class TrustEvent:
    """Individual interaction that affects trust"""
    event_id: UUID
    timestamp: datetime
    outcome: Literal["successful", "neutral", "negative"]
    context: str  # Brief description for discussability
    stage_at_time: TrustStage

@dataclass
class UserTrustProfile:
    """Persisted trust state for a user"""
    user_id: UUID
    current_stage: TrustStage

    # Counters for stage progression
    successful_count: int = 0
    neutral_count: int = 0
    negative_count: int = 0
    consecutive_negative: int = 0

    # History for discussability (bounded, not infinite)
    recent_events: List[TrustEvent] = field(default_factory=list)
    max_recent_events: int = 50

    # Stage progression tracking
    stage_history: List[Tuple[datetime, TrustStage, str]] = field(default_factory=list)
    highest_stage_achieved: TrustStage = TrustStage.NEW

    # Timestamps
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_interaction_at: datetime = field(default_factory=datetime.utcnow)
    last_stage_change_at: Optional[datetime] = None
```

### Stage Transition Logic

```python
class TrustComputationService:
    """Computes and manages user trust levels"""

    # Thresholds from PDR-002 (calibration values)
    STAGE_1_TO_2_THRESHOLD = 10   # successful interactions
    STAGE_2_TO_3_THRESHOLD = 50   # successful + pattern recognition evidence
    STAGE_3_TO_4_REQUIRES_EXPLICIT = True  # explicit user comfort signal

    CONSECUTIVE_NEGATIVE_DROP = 3  # consecutive negatives to drop stage
    INACTIVITY_DAYS_DROP = 90      # days of inactivity to drop stage
    MINIMUM_STAGE_FLOOR = TrustStage.BUILDING  # never below Stage 2 once earned

    async def record_interaction(
        self,
        user_id: UUID,
        outcome: Literal["successful", "neutral", "negative"],
        context: str
    ) -> TrustStage:
        """Record interaction outcome and compute new trust stage"""

        profile = await self.repository.get_or_create(user_id)

        # Record the event
        event = TrustEvent(
            event_id=uuid4(),
            timestamp=datetime.utcnow(),
            outcome=outcome,
            context=context,
            stage_at_time=profile.current_stage
        )
        profile.recent_events.append(event)
        profile.recent_events = profile.recent_events[-profile.max_recent_events:]

        # Update counters
        profile.last_interaction_at = datetime.utcnow()
        if outcome == "successful":
            profile.successful_count += 1
            profile.consecutive_negative = 0
        elif outcome == "negative":
            profile.negative_count += 1
            profile.consecutive_negative += 1
        else:
            profile.neutral_count += 1
            profile.consecutive_negative = 0

        # Compute stage changes
        new_stage = self._compute_stage(profile)

        if new_stage != profile.current_stage:
            profile.stage_history.append((
                datetime.utcnow(),
                new_stage,
                f"{'Progressed' if new_stage > profile.current_stage else 'Regressed'}: {context}"
            ))
            profile.last_stage_change_at = datetime.utcnow()
            profile.current_stage = new_stage

            if new_stage > profile.highest_stage_achieved:
                profile.highest_stage_achieved = new_stage

        await self.repository.save(profile)
        return new_stage

    def _compute_stage(self, profile: UserTrustProfile) -> TrustStage:
        """Pure computation of trust stage from profile state"""

        current = profile.current_stage

        # Check for regression first
        if profile.consecutive_negative >= self.CONSECUTIVE_NEGATIVE_DROP:
            # Drop one stage, but respect floor
            new_stage = max(TrustStage(current - 1), self._get_floor(profile))
            return new_stage

        # Check for progression
        if current == TrustStage.NEW:
            if profile.successful_count >= self.STAGE_1_TO_2_THRESHOLD:
                return TrustStage.BUILDING

        elif current == TrustStage.BUILDING:
            if profile.successful_count >= self.STAGE_2_TO_3_THRESHOLD:
                # TODO: Add pattern recognition evidence check
                return TrustStage.ESTABLISHED

        elif current == TrustStage.ESTABLISHED:
            # Stage 3→4 requires explicit user signal
            # This is handled separately via explicit_trust_upgrade()
            pass

        return current

    def _get_floor(self, profile: UserTrustProfile) -> TrustStage:
        """Determine minimum stage (never below Stage 2 once earned)"""
        if profile.highest_stage_achieved >= TrustStage.BUILDING:
            return TrustStage.BUILDING
        return TrustStage.NEW

    async def check_inactivity_regression(self, user_id: UUID) -> Optional[TrustStage]:
        """Check and apply inactivity-based regression (called by background job)"""

        profile = await self.repository.get(user_id)
        if not profile:
            return None

        days_inactive = (datetime.utcnow() - profile.last_interaction_at).days

        if days_inactive >= self.INACTIVITY_DAYS_DROP:
            if profile.current_stage > self._get_floor(profile):
                new_stage = TrustStage(profile.current_stage - 1)
                new_stage = max(new_stage, self._get_floor(profile))

                profile.stage_history.append((
                    datetime.utcnow(),
                    new_stage,
                    f"Inactivity regression ({days_inactive} days)"
                ))
                profile.current_stage = new_stage
                profile.last_stage_change_at = datetime.utcnow()

                await self.repository.save(profile)
                return new_stage

        return profile.current_stage

    async def handle_explicit_complaint(self, user_id: UUID, complaint: str) -> TrustStage:
        """Handle explicit user complaint about proactivity - immediate Stage 2"""

        profile = await self.repository.get_or_create(user_id)

        if profile.current_stage > TrustStage.BUILDING:
            profile.stage_history.append((
                datetime.utcnow(),
                TrustStage.BUILDING,
                f"Explicit complaint: {complaint[:100]}"
            ))
            profile.current_stage = TrustStage.BUILDING
            profile.last_stage_change_at = datetime.utcnow()

            await self.repository.save(profile)

        return TrustStage.BUILDING

    async def explicit_trust_upgrade(self, user_id: UUID, signal: str) -> TrustStage:
        """Handle explicit user comfort signal for Stage 3→4 progression"""

        profile = await self.repository.get_or_create(user_id)

        if profile.current_stage == TrustStage.ESTABLISHED:
            profile.stage_history.append((
                datetime.utcnow(),
                TrustStage.TRUSTED,
                f"Explicit trust signal: {signal[:100]}"
            ))
            profile.current_stage = TrustStage.TRUSTED
            profile.highest_stage_achieved = TrustStage.TRUSTED
            profile.last_stage_change_at = datetime.utcnow()

            await self.repository.save(profile)
            return TrustStage.TRUSTED

        return profile.current_stage
```

### Proactivity Decision Integration

```python
class ProactivityGate:
    """Determines what proactive behaviors are allowed based on trust"""

    def can_offer_capability_hints(self, stage: TrustStage) -> bool:
        """Stage 2+: Offer related capabilities after task completion"""
        return stage >= TrustStage.BUILDING

    def can_proactive_suggest(self, stage: TrustStage) -> bool:
        """Stage 3+: Proactive suggestions based on context"""
        return stage >= TrustStage.ESTABLISHED

    def can_act_without_asking(self, stage: TrustStage) -> bool:
        """Stage 4: 'I'll do X unless you stop me'"""
        return stage >= TrustStage.TRUSTED

    def get_proactivity_config(self, stage: TrustStage) -> Dict[str, Any]:
        """Get full proactivity configuration for a trust stage"""
        return {
            "stage": stage,
            "can_hint": self.can_offer_capability_hints(stage),
            "can_suggest": self.can_proactive_suggest(stage),
            "can_act": self.can_act_without_asking(stage),
            "max_suggestions_per_session": {
                TrustStage.NEW: 0,
                TrustStage.BUILDING: 1,
                TrustStage.ESTABLISHED: 2,
                TrustStage.TRUSTED: 3,
            }.get(stage, 0),
            "explanation_level": {
                TrustStage.NEW: "high",      # Explain everything
                TrustStage.BUILDING: "medium",
                TrustStage.ESTABLISHED: "low",
                TrustStage.TRUSTED: "minimal",  # User trusts, less explanation needed
            }.get(stage, "high"),
        }
```

### Discussability: Explaining Trust Decisions

```python
class TrustExplainer:
    """Generates natural language explanations of trust-based behavior"""

    async def explain_proactive_action(
        self,
        user_id: UUID,
        action_taken: str
    ) -> str:
        """When user asks 'Why did you do that without asking?'"""

        profile = await self.trust_service.get_profile(user_id)

        if profile.current_stage >= TrustStage.ESTABLISHED:
            recent_successes = len([
                e for e in profile.recent_events[-20:]
                if e.outcome == "successful"
            ])

            return (
                f"Based on our history together—you've found my suggestions helpful "
                f"about {recent_successes} times recently—I thought this was something "
                f"you'd want me to handle. Should I check first next time?"
            )

        return (
            "I should have asked first. I'll be more careful about checking "
            "before taking action. What would you prefer I do?"
        )

    async def explain_trust_level(self, user_id: UUID) -> str:
        """When user explicitly asks about trust (rare, but supported)"""

        profile = await self.trust_service.get_profile(user_id)

        stage_descriptions = {
            TrustStage.NEW: (
                "We're still getting to know each other. I'll wait for you to ask "
                "before offering suggestions, so I can learn what's helpful to you."
            ),
            TrustStage.BUILDING: (
                "We've been working together for a bit. I'll occasionally mention "
                "related things I can help with, but I'll always ask before acting."
            ),
            TrustStage.ESTABLISHED: (
                "We have a good working relationship. I'll proactively point out "
                "things I notice that might need your attention, but I'll still "
                "check before doing anything significant."
            ),
            TrustStage.TRUSTED: (
                "You've given me latitude to handle routine things. I'll take care "
                "of what I can and let you know what I did. Just tell me if you'd "
                "prefer I check first on anything."
            ),
        }

        return stage_descriptions.get(profile.current_stage, stage_descriptions[TrustStage.NEW])
```

### Persistence Layer

```python
# Database model
class UserTrustProfileDB(Base):
    __tablename__ = "user_trust_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)

    current_stage = Column(Integer, default=1)  # TrustStage enum value
    highest_stage_achieved = Column(Integer, default=1)

    successful_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    consecutive_negative = Column(Integer, default=0)

    # JSON fields for complex data
    recent_events = Column(JSON, default=list)
    stage_history = Column(JSON, default=list)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction_at = Column(DateTime, default=datetime.utcnow)
    last_stage_change_at = Column(DateTime, nullable=True)
```

### Integration Points

**1. Intent Processing** - Record interaction outcomes:
```python
# In IntentService after processing
outcome = "successful" if user_acted_on_response else "neutral"
await trust_service.record_interaction(ctx.user_id, outcome, f"Intent: {intent_type}")
```

**2. Proactivity Decisions** - Check trust before suggesting:
```python
# In any proactive feature
trust_profile = await trust_service.get_profile(user_id)
if proactivity_gate.can_proactive_suggest(trust_profile.current_stage):
    # Offer suggestion
```

**3. Background Job** - Inactivity regression check:
```python
# New job: TrustInactivityCheckJob (runs daily)
class TrustInactivityCheckJob:
    async def run(self):
        all_profiles = await trust_repo.get_all_with_interactions()
        for profile in all_profiles:
            await trust_service.check_inactivity_regression(profile.user_id)
```

---

## Alternatives Considered

### Alternative A: User-Controlled Trust Settings
Allow users to set their preferred proactivity level directly.

**Rejected because**: PDR-002 explicitly rejects this. "Users don't know what proactivity level is appropriate until they experience it. Trust-based progression is more natural than preference toggles."

### Alternative B: Session-Only Trust (No Persistence)
Calculate trust fresh each session based on session interactions only.

**Rejected because**: Destroys the "earned over time" nature of trust. Users would never reach Stage 3/4.

### Alternative C: Simple Counter Without Events
Just count successes/failures without storing event history.

**Rejected because**: Eliminates discussability. When users ask "why did you do that?", Piper needs context to explain.

### Alternative D: ML-Based Trust Scoring
Train a model to predict appropriate trust level.

**Rejected because**: Over-engineering. The rule-based thresholds from PDR-002 are clear and auditable. ML would add opacity without clear benefit.

---

## Consequences

### Positive

- **Clear proactivity governance**: Every proactive behavior has explicit trust gate
- **Discussable**: Piper can explain trust-based decisions naturally
- **Mirrors human relationships**: Builds incrementally, can regress, has floor
- **Auditable**: Stage history provides forensic trail
- **Testable**: Pure computation logic is easily unit tested

### Negative

- **Calibration required**: Threshold values (10, 50, etc.) are starting points
- **New infrastructure**: Requires database table, service, background job
- **Integration work**: Every proactive feature needs trust gate integration
- **Outcome classification challenge**: Determining "successful" vs "neutral" isn't always clear

### Neutral

- **Storage overhead**: Minimal (one row per user, bounded event history)
- **Performance**: Trust lookup adds one DB query per request (cacheable)

---

## Implementation Plan

**Phase 1: Core Infrastructure**
- [ ] Create `UserTrustProfileDB` model and migration
- [ ] Implement `TrustComputationService` with stage logic
- [ ] Implement `UserTrustProfileRepository`
- [ ] Unit tests for stage transitions

**Phase 2: Integration**
- [ ] Add trust recording to intent processing pipeline
- [ ] Implement `ProactivityGate` service
- [ ] Add trust checks to existing proactive features (standup hints, etc.)

**Phase 3: Discussability**
- [ ] Implement `TrustExplainer` service
- [ ] Add intent handlers for trust-related questions
- [ ] Integration tests for explanation flows

**Phase 4: Background Processing**
- [ ] Implement `TrustInactivityCheckJob`
- [ ] Add to scheduler startup
- [ ] Monitoring for regression events

---

## Open Questions — RESOLVED (2026-01-23)

### Q1: Outcome Classification Heuristics
**Resolution**: Define per intent type, starting with clear signals:
- User clicked a provided link → successful
- User ran a suggested command → successful
- User said "thanks" or expressed satisfaction → successful
- User asked follow-up question on same topic → successful (engagement)
- User changed topic without acknowledgment → neutral
- User said "that's not what I wanted" → negative

**Principle**: When uncertain, default to "neutral." The thresholds (10, 50) provide buffer for noise.

### Q2: Stage 3→4 Explicit Signal
**Resolution**: Conversational signals only (no settings toggle). Recognize intent patterns like:
- "Just handle it"
- "Do that automatically next time"
- "I trust you to..."
- "You don't need to ask me about that"

**Note**: Per product philosophy ("settings equals abdication"), we do not add a settings toggle for trust. If future user feedback strongly requests explicit control, this could be revisited as a documented future option—but conversational trust escalation is the primary path.

### Q3: Cross-Device Trust
**Resolution**: Yes, unified per-user. Trust is about the relationship between Piper and the person, not between Piper and a device.

### Q4: Privacy Mode Interaction
**Resolution**: Correctly excluded. Privacy mode means "don't remember"—that contract extends to trust computation. Users opting for privacy mode are explicitly declining relationship-building for that session.

---

## References

- PDR-002: Conversational Glue (v2) - Trust Computation Framework
- PDR-001: First Contact is First Recognition - Trust Stage 1 initialization
- Ethics-First Architecture - Trust gradient foundations
- CXO UX Strategy Synthesis (Nov 26, 2025) - Trust gradient origins
- Pattern-026: Cross-Feature Learning - Related confidence/learning patterns

---

## Implementation Notes (from PPM/CXO Review)

The following refinements should be addressed during implementation:

### Threshold Calibration
The values 10 (Stage 1→2) and 50 (Stage 2→3) are starting points for alpha calibration. Add explicit comments in code noting these will be tuned based on real usage patterns.

**Status**: ⚠️ Code constants exist but calibration note not in comments. See #680.

### Complaint Detection Patterns
For `handle_explicit_complaint`, detect keywords and patterns:
- "stop doing that", "don't", "I didn't ask"
- Negative sentiment + trust-related topic
- Explicit "no" to proactive offer

**Status**: ✅ IMPLEMENTED (#678, 2026-01-25). `handle_explicit_complaint()` method added and wired to TrustIntegration.

### Stage 4→3 Reversibility
Ensure regression path from Stage 4 to Stage 3 exists (not just Stage 4→2 on explicit complaint). User might want less proactivity without full reset. Consecutive negative interactions should step down one stage at a time.

**Status**: ✅ IMPLEMENTED (#679, 2026-01-25). Both consecutive negative step-down and soft regression signals implemented. `handle_soft_regression()` method drops one stage (respects floor). Signal patterns detect "ask me first", "check with me", etc.

### Floor Behavior (Stage 2 Minimum)
Per ADR design, users who have earned Stage 2 should never regress below it. The `highest_stage_achieved` field enables this.

**Status**: ✅ IMPLEMENTED (#677, 2026-01-25). `_get_floor()` helper and `MINIMUM_STAGE_FLOOR` constant added.

### Welcome Back Pattern (CXO)
When serving a user who has regressed due to inactivity, acknowledge once:
> "Good to see you again! It's been a while—I'll ease back into helping proactively as we work together."

Implement as one-time message per regression event, not on every interaction.

### Explanation Availability at Stage 4 (CXO)
The `explanation_level: "minimal"` setting affects *unsolicited* explanation depth only. When a user explicitly asks for explanation (via TrustExplainer), Piper provides full context regardless of trust stage.

**Principle**: Trusted colleagues don't over-explain unprompted, but they answer questions fully when asked.

---

*ADR-053 | ACCEPTED | January 23, 2026*
