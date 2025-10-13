# Prompt for Cursor Agent: GREAT-4C Phase 2 - Error Handling

## Context

Phase 1 complete: Spatial intelligence integrated into all 5 handlers.

**Next priority**: Add robust error handling for service failures and missing data.

## Session Log

Create new: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Add graceful error handling to canonical handlers so service failures (calendar unavailable, PIPER.md missing) provide helpful fallback responses instead of crashes.

---

## Phase 2: Error Handling Implementation

### Step 1: Identify Error Scenarios

Current handlers can fail when:

1. **Calendar service unavailable** (_handle_temporal_query)
   - Network timeout
   - API credentials invalid
   - Service down

2. **PIPER.md missing or unreadable** (_handle_status_query, _handle_priority_query, _handle_guidance_query)
   - File not found
   - Parse errors
   - Empty/invalid format

3. **User context unavailable** (all handlers)
   - Session expired
   - User not found
   - Config load failure

### Step 2: Add Error Handling to Calendar Integration

Edit: `services/intent_service/canonical_handlers.py`

Find `_handle_temporal_query` and wrap calendar calls:

```python
async def _handle_temporal_query(self, intent: Intent, session_id: str) -> Dict:
    """Handle temporal queries with error handling."""
    from services.configuration.piper_config_loader import piper_config_loader

    # Basic date/time (always works)
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    standup_config = piper_config_loader.load_standup_config()
    timezone = standup_config["timing"]["timezone"]
    timezone_short = timezone.split("/")[-1].replace("_", " ")
    current_time = datetime.now().strftime(f"%I:%M %p {timezone_short}")

    message = f"Today is {current_date} at {current_time}."
    calendar_context = {}

    # Try to enhance with calendar data
    try:
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        calendar_adapter = CalendarIntegrationRouter()
        events_result = await calendar_adapter.get_events_for_temporal_query()

        if events_result and "events" in events_result:
            # Format calendar data
            calendar_context = self._format_calendar_events(events_result["events"])
            message += f"\n\n{calendar_context['summary']}"

    except Exception as e:
        # Calendar unavailable - log but continue
        logger.warning(f"Calendar service unavailable: {e}")
        message += "\n\nNote: I couldn't access your calendar right now. The calendar service may be unavailable."

    # Spatial intelligence handling (existing)
    # ... rest of handler

    return {
        "message": message,
        "calendar_available": bool(calendar_context),
        "fallback_used": not calendar_context,
        # ... rest of response
    }
```

### Step 3: Add Error Handling to PIPER.md Access

Wrap PIPER.md access in try-except blocks:

```python
async def _handle_status_query(self, intent: Intent, session_id: str) -> Dict:
    """Handle status queries with error handling."""

    # Try to get user context
    try:
        user_context = await user_context_service.get_user_context(session_id)
    except Exception as e:
        logger.error(f"Failed to load user context: {e}")
        return {
            "message": "I'm having trouble accessing your configuration right now. "
                       "Your PIPER.md file may be missing or unreadable. "
                       "Would you like help setting it up?",
            "error": "config_unavailable",
            "action_required": "setup_piper_config",
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_status",
                "confidence": 1.0
            }
        }

    # Check if we have project data
    if not user_context.projects:
        return {
            "message": "You don't have any active projects configured in your PIPER.md yet. "
                       "Would you like me to help you set up your project portfolio?",
            "action_required": "configure_projects",
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_status",
                "confidence": 1.0
            }
        }

    # Normal handling (existing spatial logic)
    # ...
```

Apply similar pattern to:
- `_handle_priority_query` (handle missing priorities)
- `_handle_guidance_query` (handle config errors)

### Step 4: Add User Context Fallbacks

For handlers that depend on user context:

```python
async def _handle_guidance_query(self, intent: Intent, session_id: str) -> Dict:
    """Handle guidance queries with fallbacks."""

    current_time = datetime.now()
    current_hour = current_time.hour

    # Try to get user context for personalization
    user_context = None
    try:
        user_context = await user_context_service.get_user_context(session_id)
    except Exception as e:
        logger.warning(f"Using generic guidance, user context unavailable: {e}")

    # Time-based guidance (works without user context)
    if 6 <= current_hour < 9:
        if user_context and user_context.organization:
            focus = f"Morning development work - perfect time for deep focus on {user_context.organization} priorities."
        else:
            focus = "Morning development work - perfect time for deep focus and complex problem-solving."
    elif 9 <= current_hour < 14:
        if user_context and user_context.organization:
            focus = f"Collaboration time - good for coordinating with your {user_context.organization} team."
        else:
            focus = "Collaboration time - good for meetings and team coordination."
    # ... continue with fallback guidance for all time periods

    # Return with fallback indicator
    return {
        "message": focus,
        "personalized": bool(user_context),
        "fallback_guidance": not user_context,
        # ...
    }
```

### Step 5: Create Error Handling Tests

Create: `tests/intent/test_handler_error_handling.py`

```python
"""Test graceful error handling in handlers."""
import pytest
from unittest.mock import patch, AsyncMock
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.classifier import Intent

@pytest.fixture
def handlers():
    return CanonicalHandlers()

@pytest.mark.asyncio
async def test_temporal_query_calendar_unavailable(handlers):
    """Temporal query should work even if calendar fails."""

    # Mock calendar service to fail
    with patch('services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter') as mock_calendar:
        mock_calendar.return_value.get_events_for_temporal_query = AsyncMock(
            side_effect=Exception("Calendar service unavailable")
        )

        intent = Intent(
            text="What day is it?",
            category="TEMPORAL",
            action="provide_date",
            confidence=1.0
        )

        response = await handlers._handle_temporal_query(intent, "test_session")

        # Should still return date/time
        assert "Today is" in response["message"]
        assert response["fallback_used"] is True
        assert "calendar" in response["message"].lower()

@pytest.mark.asyncio
async def test_status_query_missing_config(handlers):
    """Status query should handle missing PIPER.md gracefully."""

    # Mock user context service to fail
    with patch('services.user_context_service.user_context_service.get_user_context') as mock_context:
        mock_context.side_effect = FileNotFoundError("PIPER.md not found")

        intent = Intent(
            text="What am I working on?",
            category="STATUS",
            action="provide_status",
            confidence=1.0
        )

        response = await handlers._handle_status_query(intent, "test_session")

        # Should provide helpful error message
        assert "configuration" in response["message"].lower()
        assert "setup" in response["message"].lower()
        assert response["error"] == "config_unavailable"
        assert response["action_required"] == "setup_piper_config"

@pytest.mark.asyncio
async def test_priority_query_empty_priorities(handlers):
    """Priority query should handle empty priorities list."""

    # Mock user context with no priorities
    from services.user_context_service import UserContext
    empty_context = UserContext(
        user_id="test_user",
        projects=[],
        priorities=[]
    )

    with patch('services.user_context_service.user_context_service.get_user_context') as mock_context:
        mock_context.return_value = empty_context

        intent = Intent(
            text="What's my top priority?",
            category="PRIORITY",
            action="provide_priority",
            confidence=1.0
        )

        response = await handlers._handle_priority_query(intent, "test_session")

        # Should provide helpful message
        assert "configure" in response["message"].lower() or "set up" in response["message"].lower()
        assert response.get("action_required") == "configure_priorities"

@pytest.mark.asyncio
async def test_guidance_without_user_context(handlers):
    """Guidance should work with generic advice if context unavailable."""

    # Mock context to fail
    with patch('services.user_context_service.user_context_service.get_user_context') as mock_context:
        mock_context.side_effect = Exception("Context unavailable")

        intent = Intent(
            text="What should I focus on?",
            category="GUIDANCE",
            action="provide_guidance",
            confidence=1.0
        )

        response = await handlers._handle_guidance_query(intent, "test_session")

        # Should still provide guidance (time-based)
        assert len(response["message"]) > 20
        assert response["fallback_guidance"] is True
        assert response["personalized"] is False
```

Run tests:
```bash
pytest tests/intent/test_handler_error_handling.py -v
```

### Step 6: Document Error Handling

Create: `dev/2025/10/06/error-handling-implementation.md`

```markdown
# Error Handling Implementation

## Overview
Canonical handlers now gracefully handle service failures and missing data.

## Error Scenarios Handled

### 1. Calendar Service Unavailable
**Handler**: _handle_temporal_query
**Fallback**: Return date/time without calendar events
**User message**: "Note: I couldn't access your calendar right now."

### 2. PIPER.md Missing
**Handlers**: _handle_status_query, _handle_priority_query, _handle_guidance_query
**Fallback**: Offer to help set up configuration
**User message**: "Your PIPER.md file may be missing. Would you like help setting it up?"

### 3. User Context Unavailable
**Handlers**: All handlers
**Fallback**: Provide generic responses without personalization
**User message**: Varies by handler, generally helpful without user-specific data

## Response Format

Handlers return additional fields when errors occur:

```python
{
    "message": "User-friendly error message with helpful guidance",
    "fallback_used": True,  # Indicates fallback mode
    "error": "config_unavailable",  # Error type
    "action_required": "setup_piper_config",  # Next step
    "personalized": False  # Context availability indicator
}
```

## Testing

All error scenarios tested in `tests/intent/test_handler_error_handling.py`:
- ✅ Calendar service failures
- ✅ Missing PIPER.md
- ✅ Empty configuration
- ✅ User context unavailable

## User Experience

Before: Handler crashes, user sees error
After: Handler degrades gracefully, user gets helpful guidance
```

---

## Success Criteria

- [ ] Calendar failures handled gracefully
- [ ] Missing PIPER.md handled with helpful message
- [ ] Empty config handled appropriately
- [ ] User context failures don't crash handlers
- [ ] All error tests passing
- [ ] Documentation complete
- [ ] Session log updated

---

## Evidence Format

```bash
$ pytest tests/intent/test_handler_error_handling.py -v
test_temporal_query_calendar_unavailable PASSED
test_status_query_missing_config PASSED
test_priority_query_empty_priorities PASSED
test_guidance_without_user_context PASSED

=================== 4 passed in 0.89s ===================
```

---

**Effort**: Medium (~30-45 minutes)
**Priority**: MEDIUM (UX improvement)
**Complexity**: Moderate (error paths + testing)
