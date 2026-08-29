# CORE-PREF-QUEST: Structured Preference Questionnaire

**Sprint**: A7 (Polish & Buffer)
**Priority**: Medium
**Effort**: 45 minutes
**Impact**: High (enables personalization)

---

## Problem

Alpha users need a way to set their personality preferences for how Piper Morgan communicates and behaves. Currently there's no mechanism for users to express their preferences, forcing Piper to use default settings that may not match user expectations.

---

## Proposed Solution

Implement a **simple structured questionnaire** that asks users a series of multiple-choice questions about their preferences, then stores the results in the `alpha_users.preferences` JSONB column.

### Key Features

1. **CLI Command**: `python main.py preferences` or similar
2. **Structured Questions**: Multiple-choice format for reliability
3. **JSONB Storage**: Store in existing `alpha_users.preferences` column
4. **Progressive Questions**: Ask one at a time, not all at once

---

## Implementation Approach

### Core Preference Dimensions

Ask users about **5 key dimensions**:

1. **Communication Style**
   - Question: "How do you prefer Piper Morgan to communicate?"
   - Options: `concise`, `balanced`, `detailed`

2. **Work Style**
   - Question: "What's your typical work style?"
   - Options: `structured`, `flexible`, `exploratory`

3. **Decision-Making Style**
   - Question: "How do you prefer to make decisions?"
   - Options: `data-driven`, `intuitive`, `collaborative`

4. **Learning Preference**
   - Question: "How do you prefer to learn new things?"
   - Options: `examples`, `explanations`, `exploration`

5. **Feedback Style**
   - Question: "What level of feedback do you prefer?"
   - Options: `minimal`, `moderate`, `detailed`

---

## Technical Specification

### CLI Flow

```python
# python main.py preferences

async def run_preference_questionnaire(user_id: str):
    """Run structured preference questionnaire"""

    print("\n=== Piper Morgan Preference Setup ===")
    print("Let's customize how Piper works for you.\n")

    preferences = {}

    # Communication Style
    print("1/5: Communication Style")
    print("How do you prefer Piper Morgan to communicate?")
    print("  1) Concise - Brief, to-the-point responses")
    print("  2) Balanced - Mix of detail and brevity")
    print("  3) Detailed - Comprehensive explanations")
    response = input("Your choice (1-3): ")
    preferences['communication_style'] = parse_choice(response,
        ['concise', 'balanced', 'detailed'])

    # Work Style
    print("\n2/5: Work Style")
    print("What's your typical work style?")
    print("  1) Structured - Clear plans and schedules")
    print("  2) Flexible - Adaptable to changing needs")
    print("  3) Exploratory - Creative and experimental")
    response = input("Your choice (1-3): ")
    preferences['work_style'] = parse_choice(response,
        ['structured', 'flexible', 'exploratory'])

    # Decision-Making Style
    print("\n3/5: Decision-Making Style")
    print("How do you prefer to make decisions?")
    print("  1) Data-driven - Based on facts and metrics")
    print("  2) Intuitive - Based on experience and gut feel")
    print("  3) Collaborative - Based on team input")
    response = input("Your choice (1-3): ")
    preferences['decision_making'] = parse_choice(response,
        ['data-driven', 'intuitive', 'collaborative'])

    # Learning Preference
    print("\n4/5: Learning Preference")
    print("How do you prefer to learn new things?")
    print("  1) Examples - Show me how it's done")
    print("  2) Explanations - Tell me why it works")
    print("  3) Exploration - Let me try it myself")
    response = input("Your choice (1-3): ")
    preferences['learning_style'] = parse_choice(response,
        ['examples', 'explanations', 'exploration'])

    # Feedback Style
    print("\n5/5: Feedback Style")
    print("What level of feedback do you prefer?")
    print("  1) Minimal - Only essential updates")
    print("  2) Moderate - Key milestones and issues")
    print("  3) Detailed - Comprehensive progress reports")
    response = input("Your choice (1-3): ")
    preferences['feedback_level'] = parse_choice(response,
        ['minimal', 'moderate', 'detailed'])

    # Store in database
    await store_user_preferences(user_id, preferences)

    print("\n✅ Preferences saved!")
    print(f"You can update these anytime with: python main.py preferences")
```

---

### Database Storage

Store in existing `alpha_users.preferences` JSONB column:

```json
{
  "communication_style": "balanced",
  "work_style": "flexible",
  "decision_making": "data-driven",
  "learning_style": "examples",
  "feedback_level": "moderate",
  "configured_at": "2025-10-23T15:50:00Z"
}
```

---

### Helper Functions

```python
def parse_choice(input_str: str, options: list[str]) -> str:
    """Parse user input (1-3) to option value"""
    try:
        choice = int(input_str.strip())
        if 1 <= choice <= len(options):
            return options[choice - 1]
    except ValueError:
        pass

    # Default to middle option if invalid input
    return options[len(options) // 2]

async def store_user_preferences(user_id: str, preferences: dict):
    """Store preferences in alpha_users.preferences JSONB column"""
    from datetime import datetime

    preferences['configured_at'] = datetime.utcnow().isoformat()

    async with AsyncSessionFactory() as session:
        await session.execute(
            text("""
                UPDATE alpha_users
                SET preferences = :prefs
                WHERE id = :user_id
            """),
            {"prefs": preferences, "user_id": user_id}
        )
        await session.commit()
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] CLI command launches preference questionnaire
- [ ] All 5 preference dimensions are asked
- [ ] Multiple-choice format (1-3) for each question
- [ ] Invalid input defaults to middle option (graceful)
- [ ] Preferences stored in `alpha_users.preferences` JSONB
- [ ] Timestamp added to preferences automatically
- [ ] Confirmation message shown after save

### User Experience
- [ ] Clear question text for each dimension
- [ ] Helpful descriptions for each option
- [ ] Progress indicator (1/5, 2/5, etc.)
- [ ] Can be re-run to update preferences
- [ ] Takes <2 minutes to complete

### Technical Requirements
- [ ] Uses existing `alpha_users` table
- [ ] JSONB storage for flexibility
- [ ] Async database operations
- [ ] Error handling for database failures
- [ ] Tests for preference storage

---

## Testing Plan

### Unit Tests
```python
def test_parse_choice_valid():
    """Test valid choice parsing"""
    assert parse_choice("1", ["a", "b", "c"]) == "a"
    assert parse_choice("2", ["a", "b", "c"]) == "b"
    assert parse_choice("3", ["a", "b", "c"]) == "c"

def test_parse_choice_invalid():
    """Test invalid input defaults to middle option"""
    assert parse_choice("4", ["a", "b", "c"]) == "b"
    assert parse_choice("abc", ["a", "b", "c"]) == "b"
    assert parse_choice("", ["a", "b", "c"]) == "b"

async def test_store_preferences():
    """Test preference storage in database"""
    # Create test user
    # Store preferences
    # Verify JSONB storage
    # Verify timestamp added
```

### Integration Tests
```python
async def test_preference_questionnaire_flow():
    """Test full questionnaire flow"""
    # Simulate user input
    # Run questionnaire
    # Verify all preferences stored
    # Verify can be re-run

async def test_preferences_retrieval():
    """Test preferences can be retrieved"""
    # Store preferences
    # Retrieve from database
    # Verify all fields present
```

---

## Future Enhancements

**For MVP** (now in MVP-PREF-CONVO):
- Natural language preference detection
- Automatic preference learning from behavior
- Contextual preference adjustments
- Rich preference profiles

**For Beta**:
- Web UI for preference configuration
- Preference presets (e.g., "Developer", "PM", "Designer")
- Team preference templates

---

## Implementation Notes

### Why Structured Questionnaire for Alpha?

1. **Reliability**: Multiple-choice is more reliable than NLP
2. **Speed**: Faster to implement and test
3. **Clear Intent**: Users know exactly what they're setting
4. **Foundation**: Provides data structure for future NLP features
5. **Testability**: Easy to write comprehensive tests

### Integration with PersonalityProfile

The stored preferences should integrate with existing `PersonalityProfile` system:
- Read from `alpha_users.preferences` JSONB
- Apply to response generation
- Allow runtime overrides via PIPER.user.md
- Priority: Runtime > Database > Defaults

---

## Related Issues

- **MVP-PREF-CONVO** (#248): Advanced NLP-based preference detection (deferred to MVP)
- **CORE-USER-ALPHA-TABLE** (#259): Created the alpha_users table with preferences column
- **CORE-LEARN** (Sprint A5): Learning system that will eventually use these preferences

---

## Files to Modify/Create

### New Files
- `scripts/preferences_questionnaire.py` - CLI questionnaire implementation
- `tests/scripts/test_preferences_questionnaire.py` - Unit tests

### Modified Files
- `main.py` - Add `preferences` command
- `services/user/user_service.py` - Add preference retrieval methods (if needed)

---

## Effort Estimate

**Total**: 45 minutes

**Breakdown**:
- CLI questionnaire implementation: 20 min
- Database integration: 10 min
- Testing: 10 min
- Documentation: 5 min

---

## Success Metrics

- Alpha users can set preferences in <2 minutes
- Preferences stored successfully in JSONB
- Preferences can be updated by re-running command
- 100% test coverage for preference logic

---

**Sprint**: A7
**Milestone**: Alpha
**Labels**: enhancement, ux, user-preferences, alpha
