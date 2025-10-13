# Gameplan: GREAT-4C - Handler Architecture Fixes (REVISED)

**Date**: October 5, 2025
**Epic**: GREAT-4C (Third sub-epic of GREAT-4)
**Context**: 5 canonical handlers exist with architectural issues
**Priority**: Hardcoded user context is blocking for multi-user

## Mission

Fix critical architectural issues in the 5 canonical handlers, particularly removing hardcoded single-user assumptions that will break with multiple users.

## Background from Investigation

- 5 canonical handlers exist (not 219)
- Hardcoded "VA/Kind Systems" context (single-user hack)
- Basic PIPER.md parsing (works but could be better)
- Spatial intelligence patterns not integrated
- Missing error handling for service failures
- No caching for PIPER.md reads

## Phase -1: Verify Current State
**Lead Developer - ALWAYS DO FIRST**

```bash
# Check for hardcoded user references
grep -r "VA\|Kind Systems" services/intent_service/ --include="*.py"

# Check spatial intelligence usage
grep -r "spatial" services/intent_service/ --include="*.py"

# Check PIPER.md access patterns
grep -r "PIPER\.md\|PIPER\.user\.md" services/ --include="*.py"

# Check error handling
grep -r "try\|except" services/intent_service/canonical_handlers.py
```

Document findings in `dev/2025/10/05/handler-architecture-audit.md`

## Phase 0: User Context Fix (CRITICAL)
**Both Agents - High priority**

### Remove Hardcoded Context
Find and fix:
```python
# BEFORE (hardcoded single user):
if "VA" in text or "Kind Systems" in text:
    context = "user_specific_data"

# AFTER (multi-user capable):
user_context = await get_user_context(session_id)
if user_context.organization in text:
    context = user_context.data
```

### Implement User Context Service
```python
# services/user_context_service.py
class UserContextService:
    async def get_user_context(self, session_id: str):
        """Get user-specific context from session."""
        # Get user from session
        # Load user preferences
        # Return context object
```

## Phase 1: Spatial Intelligence Integration
**Code Agent - Medium priority**

### Check ADR Requirements
Review spatial intelligence ADRs to understand required patterns.

### Integrate Spatial Context
```python
# In canonical_handlers.py
async def _handle_status_query(self, intent, session_id):
    # Get spatial context
    spatial_context = intent.spatial_context

    # Use appropriate spatial pattern
    if spatial_context.pattern == "GRANULAR":
        # Detailed status
    elif spatial_context.pattern == "EMBEDDED":
        # Consolidated status
```

## Phase 2: Error Handling
**Cursor Agent - Medium priority**

### Add Graceful Degradation
```python
async def _handle_temporal_query(self, intent, session_id):
    try:
        calendar_data = await self.calendar_service.get_events()
        return format_calendar_response(calendar_data)
    except CalendarServiceError as e:
        logger.error(f"Calendar service failed: {e}")
        return {
            "response": "I couldn't access your calendar right now. "
                       "The calendar service seems to be unavailable.",
            "fallback": True,
            "error": str(e)
        }
```

### Handle Missing PIPER.md
```python
try:
    config = await load_piper_config()
except FileNotFoundError:
    return {
        "response": "Your PIPER configuration hasn't been set up yet. "
                   "Would you like me to help you create one?",
        "action_required": "setup_piper_config"
    }
```

## Phase 3: PIPER.md Caching
**Code Agent - Medium priority**

### Implement Config Cache
```python
class PiperConfigCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 300  # 5 minutes

    async def get_config(self, user_id: str):
        if user_id in self.cache:
            entry = self.cache[user_id]
            if time.time() < entry['expires']:
                return entry['config']

        # Load from file
        config = await self._load_from_file(user_id)
        self.cache[user_id] = {
            'config': config,
            'expires': time.time() + self.ttl
        }
        return config
```

## Phase 4: Create Enhancement Issue
**Lead Developer - Quick task**

### PIPER.md Parsing Enhancement Issue
Create GitHub issue:
```markdown
# Enhanced PIPER.md Parsing

## Current State
Basic line-by-line parsing of PIPER.md

## Desired State
Structured parsing with:
- Section recognition
- Key-value extraction
- Nested configuration support
- Schema validation

## Acceptance Criteria
- [ ] Parse PIPER.md into structured object
- [ ] Validate against schema
- [ ] Support nested configurations
- [ ] Backward compatible with simple format
```

## Phase Z: Testing & Documentation
**Both Agents**

### Test Multi-User Support
```python
async def test_multiple_users():
    """Ensure no hardcoded user assumptions."""
    user1_response = await handle_query("status", "user1_session")
    user2_response = await handle_query("status", "user2_session")

    assert "VA" not in user2_response  # User2 shouldn't see User1's context
```

### Update Documentation
- Document user context service
- Update handler patterns
- Note caching strategy

## Success Criteria

- [ ] Hardcoded user context removed
- [ ] Multi-user capable
- [ ] Spatial intelligence integrated
- [ ] Error handling robust
- [ ] PIPER.md cached
- [ ] Enhancement issue created
- [ ] All tests passing

## Priority Order

1. **CRITICAL**: Remove hardcoded context (blocks alpha)
2. **HIGH**: Spatial intelligence (architectural compliance)
3. **MEDIUM**: Error handling (user experience)
4. **MEDIUM**: Caching (performance)
5. **DEFER**: PIPER.md parsing (captured in issue)

## Time Estimate
2-3 hours for items 1-4

---

*Ready to fix architectural issues before they become problems!*
