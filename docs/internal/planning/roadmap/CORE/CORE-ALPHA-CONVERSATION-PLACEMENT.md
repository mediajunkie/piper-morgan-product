# CORE-ALPHA-CONVERSATION-PLACEMENT - Fix Handler Architecture

**Priority**: P2 IMPORTANT
**Labels**: `architecture`, `technical-debt`, `patterns`
**Milestone**: Sprint A8 Phase 4
**Estimated Effort**: 2 hours

#### Problem
CONVERSATION handler is architecturally misplaced at line 199, after orchestration check but before workflow routing. Should be with other canonical handlers.

#### Current Location (Wrong)
```python
# Line 199 - Wrong place, wrong pattern
if intent.category.value == "conversation":
    return await self._handle_conversation_intent(intent, session_id)
```

#### Target Location (Correct)
```python
# Lines 123-136 - With other canonical handlers
if intent.category == IntentCategory.CONVERSATION:
    return await self._handle_conversation_intent(intent, session_id)
```

#### Solution
1. Move handler to canonical section
2. Use enum comparison (not string)
3. Remove line 199
4. Add integration tests
5. Verify performance

#### Acceptance Criteria
- [ ] Handler in canonical section
- [ ] Uses enum comparison
- [ ] Old location removed
- [ ] Tests pass
- [ ] Performance verified (<100ms)
