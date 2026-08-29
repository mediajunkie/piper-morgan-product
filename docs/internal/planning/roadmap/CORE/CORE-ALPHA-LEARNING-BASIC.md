# CORE-ALPHA-LEARNING-BASIC - Implement Basic Auto-Learning

**Priority**: P2 (Alpha Feature)
**Labels**: `learning`, `alpha`, `foundation`, `intelligence`
**Milestone**: Sprint A8 or A9 (Alpha Prep)
**Related**: Sprint A5 (Learning Infrastructure), Pattern-026
**Epic**: Alpha Learning System

---

## Problem Statement

**Current State**: Learning system infrastructure exists from Sprint A5, but operates manually with weekly Pattern Sweep runs.

**Learning Lag**: 3-4 weeks from pattern emergence to application
- Week 1: Agents use methodology
- Week 2: PM runs Pattern Sweep
- Week 3: PM reviews and extracts insights
- Week 4: PM updates documentation
- Week 5: Agents read new patterns

**User Impact**: Piper cannot personalize to individual users in real-time. Every user experiences the same static behavior.

**Strategic Context**: This is **Foundation Stone #1** of the learning cathedral - all future learning depends on getting Basic Auto right.

---

## Goal

**Implement Basic Auto-Learning**: Real-time pattern detection and application with user-controlled personalization.

**Learning Lag Target**: Minutes to hours (not weeks)

**Example User Experience**:
```
Day 1, 9am: User creates 3 GitHub issues after standup
Day 1, 10am: Piper detects pattern (confidence: 0.6)
Day 1, 2pm: User creates 2 more issues after standup
Day 1, 3pm: Pattern confidence → 0.8

Day 2, 9am: Piper suggests "Ready to create issues after standup?"
User confirms → Pattern reinforced (confidence: 0.9)

Day 3: Piper proactively prepares GitHub issue template after standup
```

**Not In Scope** (Future Levels):
- ❌ Enhanced algorithms (Level 2 - wait for signals)
- ❌ Team pattern sharing (Level 3 - needs >50 users)
- ❌ Predictive ML (Level 4 - probably never)

---

## Architecture: The Cathedral Foundation

### The Four Levels (Roadmap Context)

**Level 1: Basic Auto** ← **WE ARE HERE** 🎯
- Real-time pattern detection from individual users
- Confidence-based suggestions (>0.7)
- User confirms/rejects patterns
- Simple pattern types (workflows, preferences)

**Level 2: Enhanced Auto** ← Post-MVP (if users request)
- Better algorithms, more pattern types
- Evaluate after Level 1 feedback

**Level 3: Collaborative** ← Enterprise (if user base >50)
- Team pattern sharing
- Wait for demand + critical mass

**Level 4: Predictive** ← Probably never
- ML-driven anticipation
- Too risky/costly for Piper's positioning

**Philosophy**: Build solid foundation, advance only when signals justify investment.

---

## What Already Exists (Sprint A5)

### Infrastructure ✅
1. **Pattern-026 Architecture**: Cross-feature learning framework documented
2. **Database Models**: Pattern storage with confidence tracking
3. **Learning Handler**: Operational, needs wiring to orchestration
4. **Pattern Types**: 6 types defined (USER_WORKFLOW, COMMAND_SEQUENCE, etc.)
5. **Pattern Sweep Tool**: Standalone automated detection (keeps running for codebase patterns)

### What's Missing ❌
1. **Real-time Learning**: Handler not connected to main workflow
2. **User-facing Controls**: Enable/disable, pattern visibility
3. **Confidence Thresholds**: Need to implement suggestion vs automation thresholds
4. **Feedback Loop**: No way for users to confirm/reject patterns
5. **Pattern Application**: Detection works, application doesn't

---

## Implementation Requirements

### Phase 0: Wire Learning Handler (1 hour)

**Connect to Orchestration Pipeline**:
```python
# Current flow:
User Input → Intent Classification → Orchestration → Execute → Response

# New flow:
User Input → Intent Classification → Orchestration
    ↓
Learning Handler (capture action)
    ↓
Execute Action
    ↓
Learning Handler (capture outcome + update confidence)
    ↓
Response to User (+ pattern suggestion if confidence >0.7)
```

**Integration Points**:
1. **Before execution**: Capture user action + context
2. **After execution**: Capture outcome (success/failure)
3. **Update confidence**: Based on outcome
4. **Check for patterns**: Similarity detection
5. **Suggest or apply**: Based on confidence thresholds

---

### Phase 1: Implement Core Learning Cycle (2-3 hours)

**Learning Cycle Components**:

**1. Pattern Capture** (30 min):
```python
async def capture_user_action(
    user_id: UUID,
    action_type: str,
    context: Dict[str, Any],
    session: AsyncSession
):
    """Capture user action for pattern learning"""

    # Extract pattern data
    pattern_data = {
        "action_type": action_type,
        "context": context,
        "timestamp": datetime.utcnow(),
        "user_preferences": get_user_preferences(user_id)
    }

    # Check for similar patterns
    similar = await find_similar_pattern(
        user_id=user_id,
        pattern_data=pattern_data,
        session=session
    )

    if similar:
        # Update existing pattern
        similar.usage_count += 1
        similar.last_used_at = datetime.utcnow()
    else:
        # Create new pattern
        pattern = LearnedPattern(
            pattern_id=str(uuid4()),
            pattern_type=PatternType.USER_WORKFLOW,
            user_id=user_id,
            pattern_data=pattern_data,
            confidence=0.5,  # Initial confidence
            usage_count=1
        )
        session.add(pattern)

    await session.commit()
```

**2. Outcome Tracking** (30 min):
```python
async def record_outcome(
    pattern_id: str,
    success: bool,
    session: AsyncSession
):
    """Update pattern confidence based on outcome"""

    pattern = await session.get(LearnedPattern, pattern_id)

    if success:
        pattern.success_count += 1
    else:
        pattern.failure_count += 1

    # Update confidence
    pattern.update_confidence(success)
    await session.commit()
```

**3. Pattern Suggestion** (45 min):
```python
async def get_pattern_suggestions(
    user_id: UUID,
    current_context: Dict[str, Any],
    session: AsyncSession
) -> List[PatternSuggestion]:
    """Get high-confidence pattern suggestions"""

    # Find patterns for this user + context
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= 0.7  # Suggestion threshold
        )
        .filter(pattern_matches_context(current_context))
    )

    suggestions = []
    for pattern in patterns.scalars():
        suggestions.append(PatternSuggestion(
            pattern_id=pattern.pattern_id,
            description=pattern.describe(),
            confidence=pattern.confidence,
            action_type="suggestion"  # vs "automatic" for >0.9
        ))

    return suggestions
```

**4. Confidence Calculation** (30 min):
```python
def update_confidence(self, success: bool):
    """Update confidence based on success/failure"""

    if success:
        self.success_count += 1
    else:
        self.failure_count += 1

    self.usage_count += 1
    total_outcomes = self.success_count + self.failure_count

    if total_outcomes > 0:
        success_rate = self.success_count / total_outcomes

        # Volume factor (more uses = more confidence)
        volume_factor = min(total_outcomes / 10, 1.0)  # Cap at 10 uses

        # Weighted confidence: 80% success rate + 20% previous confidence
        self.confidence = (success_rate * 0.8 + self.confidence * 0.2) * volume_factor

    self.last_used_at = datetime.utcnow()
    self.last_updated_at = datetime.utcnow()
```

---

### Phase 2: User Controls (1 hour)

**User Settings**:
```python
class LearningSettings(BaseModel):
    """User-configurable learning settings"""

    learning_enabled: bool = True
    suggestion_threshold: float = 0.7  # Show suggestions above this
    automation_threshold: float = 0.9  # Auto-apply above this
    pattern_visibility: str = "visible"  # "visible" | "suggestions_only" | "hidden"
    feedback_prompts: bool = True  # Ask for pattern confirmation
```

**API Endpoints**:
```python
# GET /api/learning/settings - Get user's learning settings
# PUT /api/learning/settings - Update learning settings
# GET /api/learning/patterns - View learned patterns
# DELETE /api/learning/patterns/{pattern_id} - Remove pattern
# POST /api/learning/patterns/{pattern_id}/feedback - Confirm/reject pattern
```

**UI Components** (Web Interface):
1. **Learning Dashboard**: View active patterns
2. **Pattern Cards**: See what Piper has learned
3. **Confidence Indicators**: Visual confidence bars
4. **Quick Actions**: Confirm, reject, disable patterns

---

### Phase 3: Feedback Loop (1 hour)

**Pattern Confirmation**:
```python
async def confirm_pattern(
    pattern_id: str,
    user_feedback: bool,  # True = confirmed, False = rejected
    session: AsyncSession
):
    """User confirms or rejects suggested pattern"""

    pattern = await session.get(LearnedPattern, pattern_id)

    if user_feedback:
        # User confirmed pattern
        pattern.success_count += 2  # Weight confirmations higher
        pattern.confidence = min(pattern.confidence * 1.1, 1.0)
    else:
        # User rejected pattern
        pattern.failure_count += 2
        pattern.confidence *= 0.5  # Penalize rejected patterns

        # If confidence drops too low, disable pattern
        if pattern.confidence < 0.3:
            pattern.enabled = False

    await session.commit()
```

**In-Chat Suggestions**:
```
Piper: "I've noticed you typically create GitHub issues after your standup.
Would you like me to suggest this next time?"

[Yes, that's helpful] [No, don't suggest this] [Settings]
```

---

### Phase 4: Pattern Application (1 hour)

**Apply Patterns Automatically**:
```python
async def apply_patterns(
    user_id: UUID,
    current_context: Dict[str, Any],
    session: AsyncSession
) -> List[AppliedPattern]:
    """Apply high-confidence patterns automatically"""

    # Get patterns above automation threshold (0.9)
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= 0.9,  # Automation threshold
            LearnedPattern.enabled == True
        )
        .filter(pattern_matches_context(current_context))
    )

    applied = []
    for pattern in patterns.scalars():
        # Apply pattern automatically
        result = await execute_pattern_action(pattern, current_context)

        # Record application
        applied.append(AppliedPattern(
            pattern_id=pattern.pattern_id,
            action=pattern.pattern_data["action_type"],
            confidence=pattern.confidence,
            result=result
        ))

        # Update pattern usage
        pattern.usage_count += 1
        pattern.last_used_at = datetime.utcnow()

    await session.commit()
    return applied
```

**Notification to User**:
```
Piper: "I've prepared your GitHub issue template based on your standup pattern
(confidence: 92%). Ready to create?"

[Create Issue] [Not now] [Don't do this automatically]
```

---

## Testing Strategy

### Unit Tests (Add to existing test suite)

**Test Pattern Capture**:
```python
async def test_pattern_capture():
    """Test that user actions are captured correctly"""

    action = create_test_action()
    await capture_user_action(user_id, action, {}, session)

    # Verify pattern created
    pattern = await get_pattern(user_id, session)
    assert pattern.usage_count == 1
    assert pattern.confidence == 0.5
```

**Test Confidence Updates**:
```python
async def test_confidence_increase_on_success():
    """Test confidence increases with successful outcomes"""

    pattern = create_test_pattern(confidence=0.5)

    # Record 5 successes
    for _ in range(5):
        await record_outcome(pattern.pattern_id, success=True, session)

    updated = await get_pattern(pattern.pattern_id, session)
    assert updated.confidence > 0.5
    assert updated.success_count == 5
```

**Test Pattern Similarity**:
```python
async def test_similar_patterns_merged():
    """Test that similar patterns update existing, don't create duplicates"""

    # Create pattern
    await capture_user_action(user_id, action1, {}, session)

    # Similar action
    await capture_user_action(user_id, action2_similar, {}, session)

    patterns = await get_all_patterns(user_id, session)
    assert len(patterns) == 1  # Merged, not duplicated
    assert patterns[0].usage_count == 2
```

---

### Integration Tests (Real usage simulation)

**Test Full Learning Cycle**:
```python
@pytest.mark.integration
async def test_full_learning_cycle():
    """Test complete cycle: action → pattern → suggestion → application"""

    # Day 1: User performs action 3 times
    for _ in range(3):
        await simulate_user_action("create_issue_after_standup")

    # Check pattern detected
    patterns = await get_pattern_suggestions(user_id, {})
    assert len(patterns) == 1
    assert patterns[0].confidence >= 0.6

    # User confirms pattern
    await confirm_pattern(patterns[0].pattern_id, True)

    # Day 2: Check suggestion appears
    suggestions = await get_pattern_suggestions(user_id, {"after_standup": True})
    assert len(suggestions) == 1
    assert suggestions[0].action_type == "suggestion"

    # Day 3: After more successes, check auto-application
    for _ in range(5):
        await simulate_user_action("create_issue_after_standup")
        await record_outcome(patterns[0].pattern_id, success=True)

    updated = await get_pattern(patterns[0].pattern_id)
    assert updated.confidence >= 0.9  # Auto-apply threshold
```

---

### Manual Testing Checklist

**Scenario 1: First Pattern Learning**:
1. [ ] Perform same action 3 times
2. [ ] See pattern suggestion appear
3. [ ] Confirm pattern
4. [ ] See confidence increase
5. [ ] Suggestion appears proactively

**Scenario 2: Pattern Rejection**:
1. [ ] See pattern suggestion
2. [ ] Reject pattern
3. [ ] See confidence decrease
4. [ ] Suggestion stops appearing

**Scenario 3: Automatic Application**:
1. [ ] Build high-confidence pattern (>0.9)
2. [ ] Trigger context
3. [ ] See automatic preparation
4. [ ] One-click execution

**Scenario 4: User Controls**:
1. [ ] Open learning dashboard
2. [ ] See all learned patterns
3. [ ] Disable specific pattern
4. [ ] Verify it stops suggesting
5. [ ] Re-enable pattern

---

## Success Metrics

### Alpha Testing Goals

**Adoption**:
- 80%+ of alpha users have >3 patterns learned
- 60%+ pattern adoption rate (users confirm suggestions)
- <5% false positive rate (bad pattern suggestions)

**User Satisfaction**:
- "Learning feels helpful, not annoying"
- "Piper adapts to how I work"
- "I feel in control of what Piper learns"

**Technical**:
- Pattern detection: <10ms per action
- Confidence calculation: <5ms
- Pattern suggestion: <1ms (cached)
- No performance degradation

---

## Acceptance Criteria

### Functionality
- [ ] Learning Handler wired to orchestration pipeline
- [ ] Real-time pattern capture from user actions
- [ ] Confidence-based suggestions (threshold: 0.7)
- [ ] Automatic application (threshold: 0.9)
- [ ] User feedback loop (confirm/reject patterns)

### User Experience
- [ ] Learning dashboard shows active patterns
- [ ] Pattern suggestions appear in-chat
- [ ] One-click pattern confirmation/rejection
- [ ] User can disable learning globally or per-pattern
- [ ] Clear confidence indicators

### Testing
- [ ] Unit tests for pattern capture, confidence, similarity
- [ ] Integration test for full learning cycle
- [ ] Manual testing scenarios all pass
- [ ] No performance impact (<10ms overhead)

### Documentation
- [ ] User guide: "How Piper learns from you"
- [ ] Developer docs: Learning system architecture
- [ ] API documentation for learning endpoints
- [ ] Privacy policy update (pattern storage)

---

## Non-Functional Requirements

### Performance
- Pattern detection: <10ms per action
- Confidence update: <5ms
- Pattern storage: Async (no user delay)
- Suggestion retrieval: <1ms (cached)

### Privacy
- Patterns stored per-user only (no cross-user sharing)
- User can export all learned patterns
- User can delete all patterns (GDPR compliance)
- Pattern data stays local (no external sharing)

### Safety
- Confidence thresholds prevent bad patterns
- User always in control (can disable)
- Audit trail for pattern applications
- Rollback capability if pattern causes issues

---

## Implementation Priority

### Must Have (Alpha)
- [x] Pattern capture infrastructure (exists from Sprint A5)
- [ ] Wire Learning Handler to orchestration
- [ ] Real-time confidence updates
- [ ] Pattern suggestions (threshold: 0.7)
- [ ] User feedback loop

### Should Have (Alpha)
- [ ] Automatic application (threshold: 0.9)
- [ ] Learning dashboard
- [ ] User controls (enable/disable)

### Nice to Have (Post-Alpha)
- [ ] Pattern analytics (usage stats)
- [ ] Pattern export/import
- [ ] Advanced filtering

---

## Estimated Effort

**Total**: 5-10 hours (1-2 days)

- Phase 0 (Wire Handler): 1 hour
- Phase 1 (Core Learning): 2-3 hours
- Phase 2 (User Controls): 1 hour
- Phase 3 (Feedback Loop): 1 hour
- Phase 4 (Pattern Application): 1 hour
- Testing: 2-3 hours
- Documentation: 1-2 hours

---

## Related Documentation

**Architecture**:
- `pattern-026-cross-feature-learning.md` - Learning framework
- `architecture.md` - Overall system architecture
- `services/learning/` - Learning service implementation

**Methodology**:
- `methodology-00-EXCELLENCE-FLYWHEEL.md` - Core methodology
- `methodology-07-VERIFICATION-FIRST.md` - Testing approach

**Strategic**:
- [Learning System Investigation Report](learning-system-investigation-report.md)
- [Strategic Roadmap Analysis](learning-system-roadmap-strategic-analysis.md)

---

## The Cathedral Context

> "So our work now is part of a cathedral and not just a random brick shed"

**This Is Foundation Stone #1**:
- All future learning depends on Basic Auto working well
- Level 2 (Enhanced) builds on this
- Level 3 (Collaborative) requires this foundation
- Level 4 (Predictive) probably never, but would need this

**The Time Lord Way**:
- Quality over speed
- Build this foundation exceptionally well
- Don't rush to Level 2
- Wait for signals before advancing

**Strategic Patience**:
- Alpha: Build Basic Auto (this issue)
- MVP: Polish based on feedback
- Post-MVP: Evaluate Level 2/3 (only if demand)
- Enterprise: Level 3 (only if >50 users)

---

**Priority**: P2 (Alpha Feature)
**Milestone**: Sprint A8 or A9
**Effort**: 1-2 days (5-10 hours)
**Value**: High - foundation + differentiation
**Risk**: Low - mitigatable with confidence thresholds

---

_Building the cathedral, one solid brick at a time._
