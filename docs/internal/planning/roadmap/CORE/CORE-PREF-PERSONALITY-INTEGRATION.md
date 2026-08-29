# CORE-PREF-PERSONALITY-INTEGRATION: Connect Preferences to PersonalityProfile System

**Sprint**: TBD (A8 or MVP)
**Priority**: Medium
**Effort**: 30-45 minutes
**Impact**: Medium (personalization enhancement)

---

## Problem

Issue #267 (CORE-PREF-QUEST) created a structured questionnaire that captures user preferences in the `alpha_users.preferences` JSONB column:

```json
{
  "communication_style": "balanced",
  "work_style": "flexible",
  "decision_making": "data-driven",
  "learning_style": "examples",
  "feedback_level": "moderate"
}
```

However, these preferences are **not yet connected** to Piper Morgan's existing `PersonalityProfile` system. Currently:
- Preferences are collected but not used
- PersonalityProfile reads from PIPER.user.md only
- No runtime application of user preferences
- No integration between the two systems

**Result**: Users set preferences but see no behavior change in Piper Morgan.

---

## Proposed Solution

Integrate the preference questionnaire system with the existing `PersonalityProfile` system so that:
1. Preferences from database take precedence over defaults
2. Runtime overrides still work (PIPER.user.md)
3. Piper's responses reflect user preferences
4. Clear priority order: Runtime > Database > Defaults

---

## Current PersonalityProfile System

### Existing Implementation

```python
# models/personality/personality_profile.py

class PersonalityProfile:
    """User's personality preferences for interaction style"""

    def __init__(self):
        self.communication_style = "balanced"  # Default
        self.work_style = "flexible"           # Default
        # ... other defaults

    @classmethod
    def from_config(cls, config_path: str) -> "PersonalityProfile":
        """Load from PIPER.user.md"""
        # Reads from markdown config file
        ...
```

**Current Source**: Only reads from `config/PIPER.user.md`

**Missing**: Database preferences integration

---

## Enhanced Implementation

### 1. Multi-Source PersonalityProfile Loading

```python
class PersonalityProfile:
    """User's personality preferences for interaction style"""

    @classmethod
    async def for_user(cls, user_id: str) -> "PersonalityProfile":
        """
        Load personality profile with proper priority order:
        1. Runtime overrides (PIPER.user.md) - highest priority
        2. Database preferences (from questionnaire)
        3. System defaults - lowest priority
        """
        profile = cls()

        # Step 1: Load defaults (already set in __init__)

        # Step 2: Load from database preferences
        db_prefs = await cls._load_from_database(user_id)
        if db_prefs:
            profile._apply_preferences(db_prefs)

        # Step 3: Load runtime overrides from config
        config_prefs = cls._load_from_config()
        if config_prefs:
            profile._apply_preferences(config_prefs)

        return profile

    @staticmethod
    async def _load_from_database(user_id: str) -> dict | None:
        """Load preferences from alpha_users.preferences JSONB"""
        from services.user.user_service import UserService

        user_service = UserService()
        user = await user_service.get_user(user_id)

        if user and hasattr(user, 'preferences'):
            return user.preferences

        return None

    def _apply_preferences(self, prefs: dict):
        """Apply preference dict to profile"""
        if 'communication_style' in prefs:
            self.communication_style = prefs['communication_style']

        if 'work_style' in prefs:
            self.work_style = prefs['work_style']

        if 'decision_making' in prefs:
            self.decision_making = prefs['decision_making']

        if 'learning_style' in prefs:
            self.learning_style = prefs['learning_style']

        if 'feedback_level' in prefs:
            self.feedback_level = prefs['feedback_level']
```

---

### 2. Integration with Response Generation

```python
# services/orchestration/orchestration_engine.py

class OrchestrationEngine:

    async def process_request(
        self,
        user_id: str,
        user_input: str
    ) -> OrchestrationResult:
        """Process user request with personality-aware responses"""

        # Load user's personality profile
        personality = await PersonalityProfile.for_user(user_id)

        # Apply to response generation
        response = await self._generate_response(
            user_input,
            personality=personality
        )

        # Apply preferences to formatting
        formatted_response = self._apply_personality_formatting(
            response,
            personality
        )

        return formatted_response

    def _apply_personality_formatting(
        self,
        response: str,
        personality: PersonalityProfile
    ) -> str:
        """Format response based on personality preferences"""

        # Communication style
        if personality.communication_style == "concise":
            response = self._make_concise(response)
        elif personality.communication_style == "detailed":
            response = self._add_detail(response)
        # "balanced" uses default formatting

        # Feedback level
        if personality.feedback_level == "minimal":
            response = self._remove_progress_updates(response)
        elif personality.feedback_level == "detailed":
            response = self._add_progress_updates(response)

        return response
```

---

### 3. Priority Order Enforcement

```python
class PersonalityProfile:

    def get_effective_value(self, preference_key: str) -> str:
        """
        Get effective preference value with clear priority order

        Priority:
        1. Runtime override (PIPER.user.md)
        2. Database preference (questionnaire)
        3. System default
        """
        # Check runtime override
        runtime_value = self._runtime_overrides.get(preference_key)
        if runtime_value is not None:
            return runtime_value

        # Check database preference
        db_value = self._db_preferences.get(preference_key)
        if db_value is not None:
            return db_value

        # Fall back to default
        return self._defaults[preference_key]
```

---

## Configuration Management

### Example PIPER.user.md Override

```yaml
# config/PIPER.user.md

personality:
  # Runtime overrides (highest priority)
  communication_style: detailed  # Override database preference
  # Other preferences use database values
```

**Priority**:
1. ✅ `communication_style: detailed` from config (runtime override)
2. ✅ `work_style: flexible` from database (questionnaire)
3. ✅ Other preferences from database or defaults

---

## User Experience

### Before Integration
```bash
$ python main.py preferences
# User sets preferences...
✅ Preferences saved!

$ python main.py
Piper: [Uses default personality - preferences ignored]
```

### After Integration
```bash
$ python main.py preferences
# User sets communication_style: concise
✅ Preferences saved!

$ python main.py
Piper: ✅ Done. Files updated. [Concise response!]

# VS user who chose "detailed":
Piper: ✅ Task completed successfully! I've updated the following files:
       - main.py (added new CLI command)
       - services/user/user_service.py (added preference loading)
       The changes are ready for testing. [Detailed response!]
```

---

## Testing

### Unit Tests

```python
async def test_personality_loads_from_database():
    """Test personality profile loads from database"""
    # Create user with preferences
    user_id = await create_test_user(preferences={
        'communication_style': 'concise',
        'work_style': 'structured'
    })

    # Load personality
    profile = await PersonalityProfile.for_user(user_id)

    # Verify database preferences applied
    assert profile.communication_style == 'concise'
    assert profile.work_style == 'structured'

async def test_runtime_override_precedence():
    """Test runtime overrides take precedence over database"""
    # User has database preference
    user_id = await create_test_user(preferences={
        'communication_style': 'concise'
    })

    # But PIPER.user.md has override
    set_config_override('communication_style', 'detailed')

    # Load personality
    profile = await PersonalityProfile.for_user(user_id)

    # Runtime override wins
    assert profile.communication_style == 'detailed'

async def test_defaults_when_no_preferences():
    """Test defaults used when no preferences set"""
    user_id = await create_test_user(preferences={})

    profile = await PersonalityProfile.for_user(user_id)

    # Uses defaults
    assert profile.communication_style == 'balanced'
    assert profile.work_style == 'flexible'
```

### Integration Tests

```python
async def test_response_reflects_preferences():
    """Test responses change based on user preferences"""
    # User 1: Concise
    user1 = await create_test_user(preferences={
        'communication_style': 'concise'
    })
    response1 = await orchestrator.process("List files", user1)
    assert len(response1) < 100  # Short response

    # User 2: Detailed
    user2 = await create_test_user(preferences={
        'communication_style': 'detailed'
    })
    response2 = await orchestrator.process("List files", user2)
    assert len(response2) > 200  # Long response
```

---

## Acceptance Criteria

### Functional Requirements
- [ ] PersonalityProfile loads from database preferences
- [ ] Priority order enforced (Runtime > Database > Default)
- [ ] PIPER.user.md overrides still work
- [ ] Response generation uses personality preferences
- [ ] Communication style affects response length/detail
- [ ] Feedback level affects progress updates

### User Experience
- [ ] Preferences from questionnaire immediately applied
- [ ] Clear documentation of priority order
- [ ] Users can see which preferences are active
- [ ] Status command shows current personality settings

### Testing Requirements
- [ ] Unit tests for multi-source loading
- [ ] Unit tests for priority order
- [ ] Integration tests for response formatting
- [ ] Edge case handling (missing preferences, invalid values)

---

## Migration Notes

### Backward Compatibility

**Existing users (PIPER.user.md only)**:
- No change - config continues to work
- Can optionally run questionnaire
- Config overrides questionnaire

**New users (questionnaire)**:
- Set preferences via questionnaire
- Stored in database
- Applied automatically

**Power users (both)**:
- Questionnaire sets base preferences
- Config file overrides specific preferences
- Best of both worlds

---

## Performance Considerations

### Database Load
- Load preferences once per session
- Cache in PersonalityProfile instance
- Refresh only when preferences change

### Response Time Impact
- Preference loading: <10ms
- Response formatting: <5ms
- Total overhead: <15ms (negligible)

---

## Documentation Requirements

### User Documentation
- How preferences affect Piper's behavior
- Examples of concise vs detailed responses
- How to override via PIPER.user.md
- Priority order explanation

### Developer Documentation
- PersonalityProfile.for_user() usage
- Adding new preference dimensions
- Response formatting patterns
- Testing personality-aware features

---

## Related Issues

- **#267: CORE-PREF-QUEST** - Created the questionnaire system
- **#259: CORE-USER-ALPHA-TABLE** - Created alpha_users.preferences column
- **CORE-LEARN** (Sprint A5) - Learning system that will eventually inform preferences

---

## Future Enhancements

### Phase 2
- Automatic preference learning from user behavior
- A/B testing different response styles
- Preference effectiveness analytics

### Phase 3 (MVP)
- Team preference templates
- Role-based preference defaults
- Adaptive preferences (change based on context)

---

## Success Metrics

- User-reported satisfaction with response style
- Preference configuration rate (% of users who set preferences)
- Override usage (% using PIPER.user.md overrides)
- Response time unchanged (<15ms overhead)

---

**Sprint**: TBD
**Milestone**: TBD (A8 or MVP)
**Labels**: enhancement, personalization, integration, preferences
**Estimated Effort**: 30-45 minutes
