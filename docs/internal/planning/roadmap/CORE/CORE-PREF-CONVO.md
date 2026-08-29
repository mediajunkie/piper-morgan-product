# CORE-PREF-CONVO: Conversational Personality Preference Gathering

## Overview

**Epic**: User Preferences & Personalization
**Component**: Personality Profile System
**Priority**: Medium (Enhancement)
**Complexity**: Medium

## Problem Statement

The personality preference system currently supports:
- ✅ **Explicit Configuration**: Users can set preferences in `PIPER.user.md`
- ✅ **Context Discernment**: Automatic adaptation based on intent confidence
- ⚠️ **Conversational Gathering**: Infrastructure exists but lacks UI integration

Users should be able to naturally express personality preferences through conversation rather than editing YAML configuration files.

## Current State

**Infrastructure Already Exists**:
- `PatternType.USER_PREFERENCE_PATTERN` in learning system
- `_apply_user_preference_pattern()` method for converting implicit → explicit preferences
- UserPreferenceManager integration ready
- Confidence thresholds and pattern application logic implemented

**Missing**: Conversational UI and natural language preference extraction.

## Proposed Solution

### Phase 1: Natural Language Preference Detection
- Detect preference expressions in conversation:
  - "I prefer more detailed explanations"
  - "Keep responses brief and professional"
  - "Show me confidence scores"
  - "Don't be so formal with me"

### Phase 2: Confirmation & Application
- Confirm detected preferences with user:
  - "I noticed you prefer detailed technical explanations. Should I update your personality settings?"
- Apply confirmed preferences to PersonalityProfile
- Show before/after personality configuration

### Phase 3: Learning Integration
- Learn from user corrections and feedback
- Improve preference detection accuracy over time
- Suggest personality adjustments based on usage patterns

## Technical Implementation

### Conversation Analysis
```python
# New service: services/personality/conversation_analyzer.py
class ConversationAnalyzer:
    async def detect_personality_preferences(self, conversation_text: str) -> List[PreferenceHint]:
        # Analyze conversation for preference indicators
        # Return structured preference suggestions
```

### Preference Confirmation
```python
# Enhanced: services/personality/preference_manager.py
class PersonalityPreferenceManager:
    async def suggest_preference_update(self, user_id: str, detected_preferences: List[PreferenceHint]):
        # Generate confirmation message
        # Handle user approval/rejection
        # Apply approved preferences
```

### Integration Points
- **Intent Service**: Detect preference-related intents
- **Learning System**: Use existing USER_PREFERENCE_PATTERN infrastructure
- **Response Enhancer**: Apply learned preferences immediately
- **UserPreferenceManager**: Store confirmed preferences

## Acceptance Criteria

### Core Functionality
- [ ] Detect personality preferences from natural conversation
- [ ] Confirm detected preferences with user before applying
- [ ] Update PersonalityProfile based on confirmed preferences
- [ ] Show personality changes in user-friendly format

### User Experience
- [ ] Non-intrusive preference detection (no constant prompting)
- [ ] Clear confirmation messages with examples
- [ ] Easy approval/rejection of suggestions
- [ ] Immediate application of approved preferences

### Technical Requirements
- [ ] Integrate with existing learning infrastructure
- [ ] Maintain PIPER.user.md override priority
- [ ] Support all 4 personality dimensions (warmth, confidence, action, technical)
- [ ] Include confidence scoring for preference detection

### Quality Gates
- [ ] Unit tests for conversation analysis
- [ ] Integration tests with PersonalityProfile system
- [ ] User acceptance testing for natural interaction
- [ ] Performance testing (< 100ms preference detection)

## Examples

### Conversation Flow
```
User: "Can you give me more detailed technical information? I'm a developer."

Piper: "I noticed you prefer detailed technical explanations. Should I update your personality settings to 'technical_depth: detailed' and 'confidence_style: high'?"

User: "Yes, that sounds good."

Piper: "Great! I've updated your preferences. You'll now get more detailed technical responses with higher confidence indicators. You can always adjust these in your PIPER.user.md file."
```

### Preference Patterns
- **Warmth Level**: "be more friendly", "keep it professional", "casual tone"
- **Confidence Style**: "show me the confidence", "hide uncertainty", "be more humble"
- **Action Orientation**: "give me next steps", "just the facts", "what should I do"
- **Technical Depth**: "explain simply", "full technical details", "balanced approach"

## Dependencies

### Existing Infrastructure (Ready)
- ✅ PersonalityProfile domain model
- ✅ USER_PREFERENCE_PATTERN learning system
- ✅ UserPreferenceManager integration
- ✅ PIPER.user.md override system

### New Components (Need Implementation)
- ❌ Conversation analysis for preference detection
- ❌ Natural language → preference mapping
- ❌ Confirmation UI/UX flow
- ❌ Integration with chat interface

## Effort Estimate

**Total**: 8-12 hours

**Breakdown**:
- Conversation analysis: 4-5 hours
- Preference confirmation flow: 2-3 hours
- Integration & testing: 2-4 hours

## Success Metrics

- Users can set personality preferences through natural conversation
- 80%+ accuracy in preference detection
- 90%+ user satisfaction with confirmation flow
- Seamless integration with existing explicit configuration

## Future Enhancements

- Multi-turn preference refinement conversations
- Preference learning from user corrections
- Contextual preference suggestions based on task type
- Integration with Piper Education for onboarding new users

---

**Related Issues**: #228 (User Model), Learning System Epic
**Milestone**: Alpha
**Labels**: enhancement, component: ai, component: ui
