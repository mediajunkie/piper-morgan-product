# Pattern-053: Warmth Calibration

**Status**: Proven
**Category**: Grammar Application
**First Documented**: January 20, 2026
**Ratified**: January 20, 2026 (Grammar Implementation)

---

## Problem Statement

Piper needs to provide feedback and encouragement that feels authentic and appropriate to the situation. Common challenges:

- Generic praise feels hollow ("Good job!" for everything)
- Over-enthusiasm seems insincere (celebrating trivial actions)
- Under-enthusiasm feels cold (no recognition of significant achievements)
- No calibration to context (morning vs late night, high vs low accomplishment)
- Emotional tone disconnected from observed data

This creates responses that feel robotic or inappropriately enthusiastic, damaging user trust and engagement.

---

## Solution

Implement **Warmth Calibration** where emotional tone is dynamically adjusted based on observed context:

1. **Warmth levels** - Tiered responses from high celebration to neutral acknowledgment
2. **Context-driven selection** - Choose level based on accomplishment, urgency, time-of-day
3. **Authentic language** - Each level feels genuine, not forced
4. **Graceful degradation** - Low warmth = factual, not cold
5. **Consistent mapping** - Same heuristics across features

---

## Pattern Description

**Warmth Calibration** is an adaptive tone selection pattern that matches Piper's emotional expression to observed context. The pattern emphasizes:

- **Quantified warmth**: Numeric levels (0.0 to 1.0) map to tone categories
- **Context heuristics**: Clear rules for calculating warmth level
- **Tiered responses**: 4-5 tiers from high warmth to neutral
- **Authentic language**: Each tier sounds natural, not algorithmic
- **Perceptual basis**: Warmth reflects what Piper observes, not arbitrary

### Key Characteristics

1. **Warmth level calculation**:
   - Based on observable metrics (accomplishments, activity, progress)
   - Returns float 0.0 to 1.0 (or int for tier selection)
   - Transparent heuristics (user could understand the logic)

2. **Tiered language sets**:
   - High warmth (0.8+): Celebration, excitement
   - Medium-high (0.6-0.8): Encouragement, recognition
   - Medium (0.4-0.6): Acknowledgment, support
   - Low (0.2-0.4): Factual, neutral
   - Minimal (0.0-0.2): Pure information

3. **Context dimensions**:
   - **Accomplishment level**: How much was achieved?
   - **Urgency**: How pressing is the situation?
   - **Time-of-day**: Morning optimism vs late night pragmatism
   - **Streak/momentum**: Consistent progress vs sporadic activity

4. **Language authenticity**:
   - High warmth uses exclamation points and emoji
   - Medium warmth uses affirming language
   - Low warmth stays factual and supportive

---

## Implementation

### Structure

```python
from typing import Dict, List

class WarmthCalibrator:
    """Calibrate emotional warmth based on observed context."""

    # Define warmth tiers with authentic language
    WARMTH_TIERS = {
        0.8: {
            "prefixes": ["Outstanding work!", "Incredible progress!", "Fantastic achievement!"],
            "emoji": ["🎉", "⭐", "🚀"],
            "tone": "celebration"
        },
        0.6: {
            "prefixes": ["Great job!", "Nice work!", "Well done!"],
            "emoji": ["✨", "👏", "💪"],
            "tone": "encouragement"
        },
        0.4: {
            "prefixes": ["Good progress!", "Moving forward!", "Making headway!"],
            "emoji": ["✓", "→", "📈"],
            "tone": "acknowledgment"
        },
        0.2: {
            "prefixes": ["Progress made:", "Continuing work on:", "Working through:"],
            "emoji": [],
            "tone": "factual"
        }
    }

    def calculate_warmth_level(self, context: Dict) -> float:
        """
        Calculate warmth level from observable context.

        Args:
            context: Dict with metrics like:
                - accomplishments_count: int
                - blockers_count: int
                - activity_level: float (0.0-1.0)
                - time_of_day: str ("morning", "afternoon", "evening")

        Returns:
            Warmth level 0.0 to 1.0
        """
        accomplishments = context.get("accomplishments_count", 0)
        blockers = context.get("blockers_count", 0)
        activity = context.get("activity_level", 0.0)
        time_of_day = context.get("time_of_day", "afternoon")

        # Base warmth from accomplishments
        if accomplishments >= 5:
            base_warmth = 0.9
        elif accomplishments >= 3:
            base_warmth = 0.7
        elif accomplishments >= 1:
            base_warmth = 0.5
        else:
            base_warmth = 0.3

        # Adjust for blockers (reduce warmth if challenges present)
        if blockers > 2:
            base_warmth *= 0.8
        elif blockers > 0:
            base_warmth *= 0.9

        # Adjust for time of day (morning = more optimistic)
        if time_of_day == "morning":
            base_warmth *= 1.1
        elif time_of_day == "evening":
            base_warmth *= 0.9

        # Clamp to valid range
        return max(0.0, min(1.0, base_warmth))

    def select_warmth_tier(self, warmth_level: float) -> Dict:
        """
        Select language tier for warmth level.

        Args:
            warmth_level: Float 0.0 to 1.0

        Returns:
            Dict with prefixes, emoji, tone for selected tier
        """
        # Find highest tier that warmth_level meets
        for threshold in sorted(self.WARMTH_TIERS.keys(), reverse=True):
            if warmth_level >= threshold:
                return self.WARMTH_TIERS[threshold]

        # Default to lowest tier
        return self.WARMTH_TIERS[0.2]

    def apply_warmth(self, content: str, warmth_level: float) -> str:
        """
        Apply warmth to content based on level.

        Args:
            content: Base content to enhance
            warmth_level: Float 0.0 to 1.0

        Returns:
            Content with warmth applied
        """
        tier = self.select_warmth_tier(warmth_level)

        # Select random prefix from tier
        import random
        prefix = random.choice(tier["prefixes"]) if tier["prefixes"] else ""

        # Add emoji if tier includes it
        emoji = random.choice(tier["emoji"]) if tier["emoji"] else ""

        # Combine
        if prefix and emoji:
            return f"{prefix} {emoji}\n\n{content}"
        elif prefix:
            return f"{prefix}\n\n{content}"
        else:
            return content
```

### Example from Morning Standup

**File**: `services/personality/standup_bridge.py:21-31`

```python
class StandupToChatBridge:
    def __init__(self):
        # Define accomplishment-based warmth tiers
        self.accomplishment_prefixes = {
            0.8: ["Outstanding work!", "Incredible progress!", "Fantastic achievement!"],
            0.6: ["Great job!", "Nice work!", "Well done!"],
            0.4: ["Good progress!", "Moving forward!", "Making headway!"],
            0.2: ["Progress made:", "Continuing work on:", "Working through:"],
        }
```

**File**: `services/personality/standup_bridge.py:211-231`

```python
def _calculate_accomplishment_level(self, standup_data: Dict[str, Any]) -> float:
    """
    Calculate accomplishment level (0.0 to 1.0) from standup data.

    Uses observable metrics:
    - Number of yesterday's accomplishments
    - GitHub activity (commits, PRs)
    - Blockers (reduce score if present)

    Returns float suitable for warmth calibration.
    """
    accomplishments = standup_data.get("yesterday_accomplishments", [])
    blockers = standup_data.get("blockers", [])
    github_activity = standup_data.get("github_activity", {})

    # Base score from accomplishments
    base_score = min(len(accomplishments) / 5.0, 1.0)  # 5+ accomplishments = 1.0

    # Boost from GitHub activity
    commits = len(github_activity.get("commits", []))
    if commits > 0:
        base_score += 0.2

    # Reduce for blockers
    if len(blockers) > 2:
        base_score *= 0.7

    return min(base_score, 1.0)
```

**File**: `services/personality/standup_bridge.py:233-245`

```python
def _get_accomplishment_prefix(self, accomplishment_level: float) -> str:
    """
    Select warmth prefix based on accomplishment level.

    Args:
        accomplishment_level: Float 0.0 to 1.0

    Returns:
        Appropriate warmth prefix for level
    """
    import random

    # Find highest threshold met
    for threshold in sorted(self.accomplishment_prefixes.keys(), reverse=True):
        if accomplishment_level >= threshold:
            return random.choice(self.accomplishment_prefixes[threshold])

    # Default to neutral
    return "Here's your standup:"
```

**Evidence of calibration in action**:

High accomplishment (0.9):
```
Outstanding work! 🎉

• Completed 7 tasks
• Merged 3 PRs
• Resolved blocker
```

Medium accomplishment (0.5):
```
Good progress!

• Completed 2 tasks
• Made progress on feature
```

Low accomplishment (0.2):
```
Progress made:

• Started investigation
• No blockers currently
```

Zero accomplishment (0.0):
```
Here's your standup:

• No recent activity detected
• Ready to start fresh today
```

**Note the authentic tone shift**: High warmth feels celebratory, medium feels supportive, low stays factual. Each level is appropriate to context.

---

## Consequences

### Benefits

- **Authentic tone**: Warmth matches observed context, feels genuine
- **User trust**: Appropriate celebration builds credibility (vs over-enthusiasm)
- **Emotional intelligence**: Piper demonstrates perception and awareness
- **Consistent calibration**: Same heuristics across features
- **Testable**: Warmth calculation is deterministic and transparent
- **Explainable**: User could understand why Piper chose that tone

### Trade-offs

- **Complexity**: Requires calculating warmth level from context
- **Tuning**: Thresholds (0.8, 0.6, 0.4) may need adjustment based on usage
- **Language maintenance**: Multiple tiers require more copywriting
- **Subjectivity**: "Appropriate warmth" is subjective (preferences may vary)

---

## Related Patterns

### Complements

- **[Pattern-052: Personality Bridge](pattern-052-personality-bridge.md)** - Bridge uses warmth calibration
- **[Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md)** - Result data feeds calibration
- **[Pattern-054: Honest Failure](pattern-054-honest-failure.md)** - Calibrate warmth in failure states

### Alternatives

- **Fixed tone** - Simpler but less adaptive
- **LLM-generated tone** - More flexible but less predictable
- **User preference** - Let users set warmth level manually

### Dependencies

- **Observable metrics** - Need quantifiable context (accomplishments, activity)
- **Language tiers** - Pre-defined authentic phrases per level

---

## Usage Guidelines

### When to Use

✅ **Use Warmth Calibration when:**

- Feature provides feedback or acknowledgment
- Context varies significantly (high vs low accomplishment)
- Want to demonstrate emotional intelligence
- Consistent tone across features matters
- Have observable metrics to calculate warmth from

### When NOT to Use

❌ **Don't use when:**

- **Informational only**: Pure data display (no feedback needed)
- **User-generated content**: Don't add warmth to user's own words
- **Error messages**: Use honest failure pattern instead
- **API responses**: Machine-to-machine (no emotional dimension)

### Best Practices

1. **Calculate from observables**: Use metrics user can see (accomplishments, activity)
2. **Define 4-5 tiers**: Too few = abrupt shifts, too many = hard to distinguish
3. **Authentic language per tier**: Each tier should sound natural
4. **Test extremes**: Verify 0.0 (none) and 1.0 (max) feel appropriate
5. **Avoid over-enthusiasm**: High warmth should celebrate, not exaggerate
6. **Graceful low warmth**: Factual ≠ cold or disappointed
7. **Document heuristics**: Make warmth calculation transparent
8. **Tune thresholds**: Adjust based on user feedback and usage patterns
9. **Consistent across features**: Same accomplishment level → same warmth
10. **Consider time-of-day**: Morning optimism, evening pragmatism

---

## Examples in Codebase

### Primary Usage

- `services/personality/standup_bridge.py` - Accomplishment-based warmth calibration (reference)

### Applicable To (from audit)

**High Priority** (should adopt pattern):
- Intent Classification - Calibrate acknowledgment warmth to confidence level
- Todo Management - Celebrate completion warmly, acknowledge blockers supportively
- Slack Integration - Adjust tone based on channel activity level
- GitHub Integration - Calibrate based on PR/issue/commit volume

**Medium Priority**:
- Feedback System - Warm gratitude for detailed feedback, neutral for brief
- Onboarding - High warmth for first successes, medium for progress
- Conversation Handler - Adjust across conversation based on user engagement

---

## Implementation Checklist

- [ ] Define warmth tiers (typically 4-5 levels)
- [ ] Create authentic language for each tier
- [ ] Implement `calculate_warmth_level()` from observable context
- [ ] Implement `select_warmth_tier()` to map level to language
- [ ] Implement `apply_warmth()` to enhance content
- [ ] Test with high accomplishment context (expect 0.8+)
- [ ] Test with medium accomplishment (expect 0.4-0.6)
- [ ] Test with low/no accomplishment (expect 0.0-0.2)
- [ ] Test with blockers (expect reduced warmth)
- [ ] Verify authenticity of each tier's language
- [ ] Document warmth calculation heuristics
- [ ] Add time-of-day adjustment if relevant

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **Morning Standup Warmth Calibration** (reference implementation)
   - Location: `services/personality/standup_bridge.py`
   - Status: Production, daily use
   - Tiers: 4 levels (0.8, 0.6, 0.4, 0.2)
   - Context: Accomplishment count, GitHub activity, blockers
   - Result: Tone feels appropriate and authentic

**P0 Analysis Evidence**:
- Pattern identified as "Pattern D: Warmth Calibration"
- Enables standup to feel empathetic and perceptive
- Accomplishment prefixes calibrated to observed activity level

**User Feedback**:
- High warmth celebrations feel earned, not hollow
- Low warmth factual tone doesn't feel cold or judgmental
- Calibration demonstrates Piper's awareness of user's activity

---

_Pattern Identified: January 19, 2026 (P0 Morning Standup Analysis)_
_Ratified: January 20, 2026_
_Category: Grammar Application_
