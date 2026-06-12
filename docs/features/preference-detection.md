# Preference Detection System

## Overview

The Preference Detection System allows users to naturally express personality preferences through conversation. Instead of editing configuration files, users can say things like "I'd like more detailed explanations" or "Keep responses brief and professional," and the system automatically detects, suggests, and applies these preferences.

**Status**: ✅ Production Ready (Phase 2 Implementation + Phase 3 Testing Complete)

---

## Features

### Automatic Detection
The system continuously analyzes user messages for preference signals across **4 personality dimensions**:

| Dimension | Examples | Range |
|-----------|----------|-------|
| **Warmth** | "be more friendly", "casual tone", "professional" | 0.0 (cold) to 1.0 (warm) |
| **Confidence** | "show confidence scores", "hide uncertainty" | NUMERIC, CONTEXTUAL |
| **Action** | "give me next steps", "just analyze", "let's execute" | LOW, MEDIUM, HIGH |
| **Technical** | "more detail", "explain simply", "algorithms" | SIMPLIFIED, BALANCED, DETAILED |

### Intelligent Filtering
Detected preferences are automatically filtered by confidence:
- **≥ 0.9 + explicit source**: Auto-apply silently (user explicitly stated preference)
- **0.4 - 0.89**: Suggest to user for confirmation
- **< 0.4**: Don't display (too uncertain)

### User Confirmation
When preferences are suggested:
1. **Clear messaging**: "I noticed you prefer detailed technical explanations. Should I update your settings?"
2. **Easy confirmation**: Accept or dismiss with single click
3. **Immediate effect**: Applied preferences take effect immediately

### Session Management
- Preference suggestions stored in session (30-minute TTL)
- Users can accept, reject, or ignore suggestions
- No preferences applied without explicit user action (except high-confidence auto-applies)

### Learning Integration
- Confirmed preferences logged to learning system
- Pattern becomes part of user's learned preferences
- System improves detection over time

---

## How It Works

### Detection Flow

```
User Message
    ↓
ConversationAnalyzer.analyze_message()
    ├─ Language pattern matching (warm words, technical keywords, etc.)
    ├─ Behavioral signal analysis
    ├─ Explicit feedback parsing
    ↓
Confidence scoring (0.0 - 1.0)
    ├─ VERY_HIGH (≥0.9): Auto-apply
    ├─ HIGH (0.7-0.89): Suggest with confidence
    ├─ MEDIUM (0.4-0.69): Suggest
    └─ LOW (<0.4): Filtered out
    ↓
Session storage (30-min TTL)
    ├─ Suggested hints (await user confirmation)
    └─ Auto-apply hints (silent application)
    ↓
API response includes preference suggestions
    ↓
Frontend displays suggestions to user
    ↓
User confirms/rejects
    ↓
PreferenceDetectionHandler.confirm_preference()
    ├─ Store in UserPreferenceManager (persistent)
    ├─ Update PersonalityProfile
    ├─ Log to learning system
    └─ Apply to all future responses
```

### Detection Methods

The system uses multiple detection approaches:

1. **Language Patterns** (Primary)
   - Warm words: "love", "appreciate", "friendly", "casual"
   - Technical words: "algorithm", "architecture", "code", "implementation"
   - Professional words: "efficient", "concise", "rigorous"
   - Action words: "execute", "implement", "build", "immediately"

2. **Behavioral Signals**
   - User asks follow-up questions about topics
   - User requests additional detail or simplification
   - User adjusts complexity/formality mid-conversation

3. **Explicit Feedback**
   - "You were too technical" / "not technical enough"
   - "That was too formal" / "I'd like you to be friendlier"
   - Direct preference statements

4. **Response Analysis**
   - User satisfaction signals (tone, follow-up questions)
   - Request adjustments ("Can you simplify that?")
   - Pattern consistency checks

---

## API Reference

### Accept Preference Suggestion

```http
POST /api/v1/preferences/hints/{hint_id}/accept
```

**Parameters**:
- `hint_id` (path): ID of the preference hint to accept
- `session_id` (header/body): Current session ID

**Response**:
```json
{
  "success": true,
  "action": "accepted",
  "dimension": "warmth_level",
  "previous_value": 0.5,
  "new_value": 0.8,
  "message": "Preference updated! Your warmth_level setting is now 0.8"
}
```

### Dismiss Preference Suggestion

```http
POST /api/v1/preferences/hints/{hint_id}/dismiss
```

**Parameters**:
- `hint_id` (path): ID of the preference hint to dismiss
- `session_id` (header/body): Current session ID

**Response**:
```json
{
  "success": true,
  "action": "dismissed",
  "hint_id": "hint_1_abc123"
}
```

### Get Personality Profile

```http
GET /api/v1/preferences/profile
```

**Response**:
```json
{
  "warmth_level": 0.8,
  "confidence_style": "contextual",
  "action_orientation": "high",
  "technical_depth": "detailed",
  "last_updated": "2025-11-22T16:30:00Z"
}
```

### Get Preference Statistics

```http
GET /api/v1/preferences/stats
```

**Response**:
```json
{
  "total_preferences_detected": 15,
  "total_preferences_applied": 8,
  "last_preference_update": "2025-11-22T16:30:00Z",
  "by_dimension": {
    "warmth_level": {"detected": 4, "applied": 3},
    "confidence_style": {"detected": 3, "applied": 2},
    "action_orientation": {"detected": 5, "applied": 2},
    "technical_depth": {"detected": 3, "applied": 1}
  }
}
```

### Health Check

```http
GET /api/v1/preferences/health
```

**Response**:
```json
{
  "status": "healthy",
  "components": {
    "analyzer": "healthy",
    "storage": "healthy",
    "learning_integration": "healthy"
  }
}
```

---

## Configuration

### Confidence Thresholds

Edit in `services/personality/preference_detection.py`:

```python
# Suggestion threshold (what gets shown to user)
SUGGESTION_THRESHOLD = 0.4

# Auto-apply threshold (applies without user confirmation)
AUTO_APPLY_THRESHOLD = 0.9

# Session hint TTL (how long suggestions stay available)
SESSION_HINT_TTL_MINUTES = 30
```

### Detection Patterns

Customize word sets in `services/personality/conversation_analyzer.py`:

```python
class ConversationAnalyzer:
    WARM_WORDS = {"love", "appreciate", "friendly", ...}
    PROFESSIONAL_WORDS = {"efficient", "concise", ...}
    TECHNICAL_WORDS = {"algorithm", "architecture", ...}
    ACTION_WORDS = {"execute", "build", ...}
```

### Personality Dimensions

Configure default values in `services/personality/personality_profile.py`:

```python
@dataclass
class PersonalityProfile:
    warmth_level: float = 0.5  # Default: neutral
    confidence_style: ConfidenceDisplayStyle = CONTEXTUAL
    action_orientation: ActionLevel = MEDIUM
    technical_depth: TechnicalPreference = BALANCED
```

---

## Frontend Integration

### HTML Component

The preference suggestion component is available in `templates/components/preference_suggestion.html`:

```html
<div class="preference-suggestion" id="pref_{{ hint.id }}">
  <div class="suggestion-header">
    <span class="dimension-icon">{{ icon }}</span>
    <span class="dimension-label">{{ hint.dimension }}</span>
    <div class="confidence-bar">
      <div class="confidence-fill" style="width: {{ confidence * 100 }}%"></div>
    </div>
  </div>

  <div class="suggestion-body">
    <p class="explanation">{{ hint.explanation }}</p>
    <div class="suggestion-actions">
      <button onclick="acceptPreference('{{ hint.id }}')">Accept</button>
      <button onclick="dismissPreference('{{ hint.id }}')">Dismiss</button>
    </div>
  </div>
</div>
```

### JavaScript Handlers

Use functions from `static/js/preferences.js`:

```javascript
// Accept a preference suggestion
await acceptPreference(hintId);

// Dismiss a preference suggestion
await dismissPreference(hintId);

// Get current session ID
const sessionId = getCurrentSessionId();

// Show notification
showToast("Preference updated!", "success");

// Log preference event
logEvent("preference_accepted", {dimension, value});
```

### Integrating into Response

Include preference suggestions in the response JSON:

```json
{
  "response": "Here's a detailed technical explanation...",
  "preferences": {
    "hints": [
      {
        "id": "hint_1_abc123",
        "dimension": "technical_depth",
        "detected_value": "detailed",
        "confidence_score": 0.85,
        "explanation": "I detected you prefer detailed technical explanations"
      }
    ],
    "has_suggestions": true,
    "has_auto_applies": false,
    "analysis_summary": "Detected technical depth preference"
  }
}
```

---

## Testing

### Unit Tests (27 tests, 100% passing)
- Data structure validation (PreferenceHint, PreferenceConfirmation)
- Confidence scoring and thresholds
- Language pattern matching
- Session storage and retrieval
- Application logic

**Run**: `pytest tests/unit/services/personality/test_preference_detection.py -v`

### Integration Tests (10 tests, 100% passing)
- Complete e2e detection → confirmation → storage flow
- Multiple preference handling
- Auto-apply high-confidence preferences
- Preference rejection
- Session management
- Error handling

**Run**: `pytest tests/integration/services/personality/test_preference_detection_e2e.py -v`

### Manual Testing (Tracked in #375)
- Real conversation scenarios
- UI suggestion display
- Accept/reject button functionality
- Persistence across sessions

---

## Troubleshooting

### Preferences Not Being Detected

**Cause**: Message confidence below 0.4 threshold
**Solution**:
- Use stronger preference signals (more explicit language)
- Check ConversationAnalyzer word lists include your test words
- Verify `analyze_message()` returns hints (check logs)

### Preferences Not Appearing in Suggestions

**Cause**: High-confidence hints auto-applied instead of suggested
**Solution**:
- Check if confidence score ≥ 0.9 + explicit source (auto-apply threshold)
- Reduce confidence by using less explicit language
- Check session storage (TTL may have expired)

### Confirmed Preferences Not Persisting

**Cause**: Learning system integration issue
**Solution**:
- Verify UserPreferenceManager has user_id in correct format (UUID)
- Check learning system logs for errors
- Verify database connection and permissions

### Slow Preference Detection

**Cause**: ConversationAnalyzer processing large messages
**Solution**:
- Optimize word set sizes (smaller is faster)
- Cache analyzer instance (don't recreate per request)
- Monitor database queries for personality profile loading

---

## Future Enhancements

### Phase 4.1: Contextual Preferences
- Different preferences for different conversation types
- "Be technical when discussing code, casual when chatting"
- Context-aware preference application

### Phase 4.2: Preference Conflicts
- Handle contradictory preferences from same user
- Learning-based conflict resolution
- Preference priority system

### Phase 4.3: Group Preferences
- Learn team/organization preferences
- Apply shared preferences to all team members
- Override individual preferences when needed

### Phase 4.4: Preference Evolution
- Track preference changes over time
- Detect shifting preferences (user wants less detail recently)
- Recommend preference updates based on usage patterns

### Phase 4.5: Privacy & Control
- User dashboard for all preferences
- Preference history and audit log
- Easy reset/clear all preferences
- Data export in user-friendly format

---

## Performance Metrics

| Operation | Time | Notes |
|-----------|------|-------|
| analyze_message() | <50ms | Language pattern matching |
| confirm_preference() | <100ms | DB write + learning log |
| Session storage | <10ms | In-memory storage |
| Full e2e cycle | <500ms | Detection → confirmation → storage |

---

## Related Documentation

- **Integration Guide *(proposed; doc TBD)*** - How to integrate into your application
- **[API Reference](../api/preference-detection-api.md)** - Detailed API documentation
- **Development Guide *(proposed; doc TBD)*** - For developers working on the system
- **User Guide *(proposed; doc TBD)*** - For end users

---

**Last Updated**: November 22, 2025
**Status**: Production Ready ✅
**Issue**: #248 (CONV-LEARN-PREF)
**Tests**: 37/37 passing (100%)
