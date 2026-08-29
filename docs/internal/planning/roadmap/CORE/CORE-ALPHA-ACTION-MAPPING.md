# CORE-ALPHA-ACTION-MAPPING - Fix Action Name Coordination

**Priority**: P1 CRITICAL
**Labels**: `bug`, `integration`, `classifier`
**Milestone**: Sprint A8 Phase 3
**Estimated Effort**: 2 hours

#### Problem
Intent classifier generates action names that don't match handler method names:
- Classifier: `create_github_issue`
- Handler: `_handle_create_issue`
- Result: "No handler for action" error

#### Solution
Create ActionMapper class to translate classifier output to handler names:

```python
class ActionMapper:
    ACTION_MAPPING = {
        "create_github_issue": "create_issue",
        "list_github_issues": "list_issues",
        "create_notion_page": "create_page",
        # etc.
    }
```

#### Implementation Steps
1. Create action_mapper.py
2. Define comprehensive mappings
3. Integrate into intent_service.py
4. Log unmapped actions
5. Test with common queries
6. Document mapping patterns

#### Acceptance Criteria
- [ ] ActionMapper class created
- [ ] All known actions mapped
- [ ] Unknown actions logged
- [ ] Friendly fallback for unmapped
- [ ] Integration tests pass
- [ ] Documentation updated
