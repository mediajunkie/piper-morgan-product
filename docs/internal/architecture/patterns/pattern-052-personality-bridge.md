# Pattern-052: Personality Bridge

**Status**: Proven
**Category**: Grammar Application
**First Documented**: January 20, 2026
**Ratified**: January 20, 2026 (Grammar Implementation)

---

## Problem Statement

Features generate rich contextual data (GitHub activity, calendar events, task status), but presenting this raw data to users feels mechanical and database-like. Common challenges:

- Technical data structures ("commits": [], "issues": {}) shown to users
- No emotional intelligence or warmth in responses
- Piper's personality inconsistent or absent
- Same data presented identically regardless of Place (Slack vs email vs CLI)
- No Entity awareness (who is asking affects presentation)

This creates features that feel like tools rather than collaborative experiences with Piper as a present, helpful entity.

---

## Solution

Implement a **Personality Bridge** that transforms raw data into warm, conversational narrative:

1. **Separation layer** - Bridge class isolates personality from business logic
2. **Entity awareness** - Presentation adapts to who is receiving
3. **Place atmosphere** - Format and tone adapt to where (Slack, email, web)
4. **Warmth calibration** - Emotional tone matches context (see Pattern-053)
5. **Action orientation** - Piper suggests next steps, not just reports

---

## Pattern Description

A **Personality Bridge** is a transformation layer that converts feature output (data) into user-facing narrative (experience). The pattern emphasizes:

- **Separation of concerns**: Business logic generates data; bridge adds personality
- **Consistent voice**: Piper's personality applied uniformly across features
- **Place-aware formatting**: Same data feels different in different Places
- **Entity respect**: Language adapts to user's relationship with Piper
- **Moment framing**: Data presented as experiences, not facts

### Key Characteristics

1. **Bridge class structure**:
   - Input: Raw feature data (Result dataclass)
   - Output: Conversational format (string or structured response)
   - Methods: `adapt_for_[place]()`, `apply_personality()`

2. **Transformation layers**:
   - **Structure** - Convert dicts/lists to prose
   - **Voice** - Add Piper's warmth and presence
   - **Format** - Adapt to Place (emoji for Slack, formal for email)
   - **Action** - Suggest next steps, not just inform

3. **Personality dimensions**:
   - **Warmth** - Encouragement, celebration, empathy
   - **Presence** - "I noticed", "I found", "I see" (Piper is present)
   - **Action orientation** - "You might want to...", "Consider..."
   - **Honesty** - Admit limitations, don't hide failures

---

## Implementation

### Structure

```python
from typing import Dict, Any
from services.personality.personality_profile import PersonalityProfile

class [Feature]ToChatBridge:
    """
    Transform [feature] data into conversational format.

    Separates business logic from presentation personality.
    """

    def adapt_for_chat(self, raw_data: Dict[str, Any]) -> str:
        """
        Convert raw feature data to conversational format.

        Args:
            raw_data: Feature Result dataclass as dict

        Returns:
            Conversational narrative suitable for chat interface
        """
        # Convert structure to prose
        sections = []

        if raw_data.get("findings"):
            sections.append(self._format_findings(raw_data["findings"]))

        if raw_data.get("suggestions"):
            sections.append(self._format_suggestions(raw_data["suggestions"]))

        return "\n\n".join(sections)

    def apply_personality(
        self,
        content: str,
        profile: PersonalityProfile,
        context: Dict[str, Any]
    ) -> str:
        """
        Apply personality preferences to content.

        Args:
            content: Base conversational content
            profile: User's personality preferences
            context: Additional context (accomplishment level, urgency, etc.)

        Returns:
            Content enhanced with personality dimensions
        """
        # Add warmth based on context (see Pattern-053: Warmth Calibration)
        enhanced = self._enhance_with_warmth(content, context)

        # Add action orientation if appropriate
        if context.get("suggest_actions"):
            enhanced = self._add_action_suggestions(enhanced, context)

        # Add presence language ("I noticed", "I found")
        enhanced = self._add_presence(enhanced)

        return enhanced

    def _format_findings(self, findings: List[str]) -> str:
        """Format findings with Piper's voice."""
        if not findings:
            return ""

        # Add presence and warmth
        intro = "Here's what I found:"
        items = [f"• {finding}" for finding in findings]

        return f"{intro}\n" + "\n".join(items)

    def _add_presence(self, content: str) -> str:
        """Add Piper's presence to content."""
        # Transform passive voice to active Piper voice
        # "5 items were found" → "I found 5 items"
        # "Activity was detected" → "I noticed activity"
        return content  # Implementation details
```

### Example from Morning Standup

**File**: `services/personality/standup_bridge.py:70-86`

```python
class StandupToChatBridge:
    """Transform standup data to conversational format with personality."""

    def apply_personality_to_standup(
        self, standup_data: Dict[str, Any], profile: PersonalityProfile
    ) -> str:
        """Apply personality preferences to standup content"""

        # First convert to chat format (structure → prose)
        base_content = self.adapt_standup_for_chat(standup_data)

        # Then apply personality enhancements (add warmth, presence, action)
        enhanced_content = self._enhance_with_personality(base_content, profile, standup_data)

        return enhanced_content
```

**File**: `services/personality/standup_bridge.py:88-114`

```python
def adapt_standup_for_chat(self, standup_data: Dict[str, Any]) -> str:
    """Convert standup data structure to conversational format."""

    sections = []

    # Yesterday accomplishments - add presence and warmth
    if standup_data.get("yesterday_accomplishments"):
        accomplishments = standup_data["yesterday_accomplishments"]
        intro = self._get_accomplishment_intro(len(accomplishments))  # Warmth calibration
        sections.append(f"{intro}\n" + "\n".join(f"• {item}" for item in accomplishments))

    # Today priorities - action orientation
    if standup_data.get("today_priorities"):
        priorities = standup_data["today_priorities"]
        sections.append("Today's focus:\n" + "\n".join(f"• {item}" for item in priorities))

    # Blockers - empathy and problem-solving tone
    if standup_data.get("blockers"):
        blockers = standup_data["blockers"]
        # Note: "Current challenges to work through" not "Blockers"
        sections.append("Current challenges to work through:\n" + "\n".join(f"• {item}" for item in blockers))

    return "\n\n".join(sections)
```

**Personality application** (`services/personality/standup_bridge.py:116-155`):

```python
def _enhance_with_personality(
    self, base_content: str, profile: PersonalityProfile, standup_data: Dict[str, Any]
) -> str:
    """Enhance content with personality dimensions."""

    # Warmth calibration based on accomplishment level
    accomplishment_level = self._calculate_accomplishment_level(standup_data)
    warmth_prefix = self._get_accomplishment_prefix(accomplishment_level)

    # Action orientation - suggest next steps
    suggestions = []
    if standup_data.get("github_activity"):
        suggestions.append("Consider reviewing recent PRs")

    # Presence language - "I noticed", "I see", "I found"
    # ... transform passive to active voice

    return f"{warmth_prefix}\n\n{base_content}\n\n{self._format_suggestions(suggestions)}"
```

**Evidence of transformation**:

Before (raw data):
```python
{
    "yesterday_accomplishments": ["Fixed bug #123", "Reviewed PR #456"],
    "blockers": ["Waiting on API key"]
}
```

After (personality bridge):
```
Great progress yesterday! 🎉

• Fixed bug #123
• Reviewed PR #456

Current challenges to work through:
• Waiting on API key

Consider reaching out to the team about that API access.
```

---

## Consequences

### Benefits

- **Consistent personality**: Piper feels the same across all features
- **Warmth and empathy**: Users feel supported, not just informed
- **Separation of concerns**: Business logic stays clean, personality isolated
- **Place adaptation**: Same data feels native to each Place
- **Entity awareness**: Response respects user's relationship with Piper
- **Testability**: Bridge logic testable independently of business logic

### Trade-offs

- **Verbosity**: Bridge code adds LOC (though improves UX significantly)
- **Maintenance**: Personality changes require updating bridge classes
- **Translation overhead**: Additional processing to transform data
- **Consistency risk**: Multiple bridges must maintain consistent voice

---

## Related Patterns

### Complements

- **[Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md)** - Result dataclass is bridge input
- **[Pattern-051: Parallel Place Gathering](pattern-051-parallel-place-gathering.md)** - Bridge presents gathered data
- **[Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md)** - How to adjust warmth dimension
- **[Pattern-054: Honest Failure](pattern-054-honest-failure.md)** - Bridge communicates failures warmly

### Alternatives

- **Template strings** - Simpler but less dynamic
- **LLM generation** - More flexible but slower and less predictable
- **Inline formatting** - Faster but personality mixed with business logic

### Dependencies

- **PersonalityProfile** - `services/personality/personality_profile.py`
- **Result dataclass** - Output from feature (Pattern-050)

---

## Usage Guidelines

### When to Use

✅ **Use Personality Bridge when:**

- Feature output is user-facing (not API-only)
- Raw data feels too technical or mechanical
- Want consistent Piper personality across features
- Different Places need different formatting (Slack vs email)
- Feature data benefits from warmth, empathy, action orientation

### When NOT to Use

❌ **Don't use when:**

- **API endpoints only**: Machine-to-machine (use structured JSON)
- **Pass-through data**: Just proxying external responses
- **Real-time streaming**: Latency critical (bridge adds overhead)
- **Already conversational**: LLM-generated content (avoid double transformation)

### Best Practices

1. **Two-step transformation**: Structure → prose (adapt), then prose → personality (apply)
2. **Use presence language**: "I found", "I noticed", "I see" (Piper is present)
3. **Add warmth based on context**: Celebrate wins, empathize with challenges
4. **Suggest actions**: Don't just inform, guide next steps
5. **Reframe negatives supportively**: "Challenges to work through" not "Blockers"
6. **Adapt to Place**: Emoji for Slack, formal for email, concise for CLI
7. **Test raw and bridged**: Verify both data accuracy and personality quality
8. **Extract common voice**: Reusable phrases in personality constants
9. **Respect Entity boundaries**: Formal vs casual based on user relationship
10. **Don't overdo warmth**: Calibrate appropriately (Pattern-053)

---

## Examples in Codebase

### Primary Usage

- `services/personality/standup_bridge.py` - StandupToChatBridge (reference implementation)

### Applicable To (from audit)

**High Priority** (should adopt pattern):
- Intent Classification - IntentResponseBridge (acknowledge intent warmly)
- Todo Management - TodoResponseBridge (celebrate completion, encourage on blockers)
- Slack Integration - SlackMessageBridge (channel-aware tone)
- GitHub Integration - GitHubActivityBridge (developer-focused narrative)

**Medium Priority**:
- Feedback System - FeedbackAcknowledgmentBridge (gratitude and understanding)
- Conversation Handler - ConversationBridge (consistent personality across all interactions)
- Onboarding - OnboardingGuideBridge (welcoming, encouraging)

---

## Implementation Checklist

- [ ] Create `[Feature]ToChatBridge` class
- [ ] Implement `adapt_for_chat()` method (structure → prose)
- [ ] Implement `apply_personality()` method (add warmth/presence/action)
- [ ] Extract `_format_[section]()` methods for each data type
- [ ] Add presence language ("I found", "I noticed")
- [ ] Integrate warmth calibration (Pattern-053)
- [ ] Add action suggestions where appropriate
- [ ] Test with real feature data
- [ ] Test with edge cases (empty data, errors)
- [ ] Verify personality consistency with other features
- [ ] Document transformation examples in tests

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **Morning Standup Bridge** (reference implementation)
   - Location: `services/personality/standup_bridge.py`
   - Status: Production, daily use
   - Transformation: Raw dict → warm narrative
   - Dimensions: Warmth, presence, action, empathy

**P0 Analysis Evidence**:
- Pattern identified as "Pattern C: Personality Bridge"
- Enables Morning Standup to feel collaborative, not mechanical
- Separates data (morning_standup.py) from presentation (standup_bridge.py)

**Grammar Audit Evidence**:
- Personality bridge identified as missing in 9/16 features
- Features without bridge scored "Flattened" (mechanical)
- Bridge presence correlates with "Conscious" rating

---

_Pattern Identified: January 19, 2026 (P0 Morning Standup Analysis)_
_Ratified: January 20, 2026_
_Category: Grammar Application_
