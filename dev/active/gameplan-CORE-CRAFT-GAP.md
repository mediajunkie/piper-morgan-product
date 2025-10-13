# Gameplan: CORE-CRAFT-GAP - Critical Functional Gaps

**Date**: October 10, 2025  
**Epic**: CORE-CRAFT-GAP  
**Context**: Replacing sophisticated placeholders with real implementations  
**Approach**: Iterative - EXECUTION handlers first as model  
**Duration**: 28-41 hours total

## Mission

Replace sophisticated placeholders in GREAT-4D with working implementations. These placeholders return `success=True` but contain "IMPLEMENTATION IN PROGRESS" comments and don't execute actual workflows. 

## Background

Serena audit revealed GREAT-4D is only 30% complete despite passing tests. The architecture is sound but handlers are sophisticated stubs. We'll use an iterative approach: perfect EXECUTION handlers first, then use as model for others.

## Overall Structure

### Three Issues to Address
1. **GAP-1**: Handler implementations (20-30 hours) - PRIMARY FOCUS
2. **GAP-2**: Interface validation (2-3 hours)
3. **GAP-3**: Accuracy polish (6-8 hours)

### Iterative Execution Plan
1. **Sub-Gameplan 1**: EXECUTION handlers (this gameplan)
2. **Sub-Gameplan 2**: ANALYSIS handlers
3. **Sub-Gameplan 3**: SYNTHESIS handlers
4. **Sub-Gameplan 4**: STRATEGY/LEARNING handlers
5. **Consolidation**: GAP-2 and GAP-3

## Phase -1: Reconnaissance with Serena
**Both Agents - 30 minutes**

### Map the Battlefield
```python
# Use Serena to find ALL placeholders
mcp__serena__find_symbol(
    name_regex="handle_.*",
    relative_path="services/",
    include_body=True
)

# Identify "IMPLEMENTATION IN PROGRESS" patterns
mcp__serena__search_project(
    query="IMPLEMENTATION IN PROGRESS OR TODO OR placeholder",
    file_pattern="*.py"
)
```

### Categorize Handlers
- EXECUTION: create/update/delete operations
- ANALYSIS: analyze/investigate operations  
- SYNTHESIS: generate/summarize operations
- STRATEGY: plan/prioritize operations
- LEARNING: learn/adapt operations

### Verify Infrastructure
```bash
# Confirm services are configured
cat .env | grep -E "GITHUB|SLACK|NOTION"
pytest tests/integrations/ -k "test_connection" -v

# Verify handler structure
find services/handlers/ -name "*.py" | head -20
grep -r "class.*Handler" services/ --include="*.py"
```

## Phase 0: Investigation & Planning
**Lead Developer WITH PM - 1 hour**

### Current State Analysis
Use Serena to get exact counts:
- Total handlers with placeholders: ?
- EXECUTION handlers needing work: ?
- Test coverage for handlers: ?
- Integration points per handler: ?

### Testing Strategy Decision
Implement `implemented` flag pattern:
```python
class HandlerResult:
    success: bool
    implemented: bool = True  # False for placeholders
    response: Any
    
# Placeholder returns:
return HandlerResult(
    success=True,
    implemented=False,  # KEY MARKER
    response="Handler not yet implemented"
)
```

### Success Criteria Definition
For EXECUTION handlers specifically:
- [ ] Real API calls to external services
- [ ] Resources actually created/updated
- [ ] Proper error handling
- [ ] Retry logic functional
- [ ] Integration tests with real data

## SUB-GAMEPLAN 1: EXECUTION Handlers

### Phase 1: Pattern Establishment with First Handler
**Code Agent - 2 hours**

#### Select Simplest EXECUTION Handler
Priority order (simplest first):
1. `_handle_create_task` (if exists)
2. `_handle_create_issue` (GitHub)
3. `_handle_create_note` (Notion)

#### Implement Complete Pattern
```python
async def _handle_create_issue(self, params: Dict) -> HandlerResult:
    """Create GitHub issue - FULLY IMPLEMENTED"""
    try:
        # 1. Parameter validation
        title = params.get('title')
        body = params.get('body')
        labels = params.get('labels', [])
        
        if not title:
            return HandlerResult(
                success=False,
                implemented=True,  # Real implementation
                error="Title required"
            )
        
        # 2. Service integration
        github_service = self.service_registry.get('github')
        
        # 3. Actual API call
        issue = await github_service.create_issue(
            title=title,
            body=body,
            labels=labels
        )
        
        # 4. Success response with real data
        return HandlerResult(
            success=True,
            implemented=True,
            response={
                'issue_number': issue.number,
                'issue_url': issue.html_url,
                'created_at': issue.created_at
            }
        )
        
    except Exception as e:
        # 5. Proper error handling
        logger.error(f"Failed to create issue: {e}")
        return HandlerResult(
            success=False,
            implemented=True,
            error=str(e)
        )
```

#### Create Integration Test
```python
@pytest.mark.integration
async def test_handle_create_issue_real():
    """Test with real GitHub API"""
    handler = ExecutionHandler()
    result = await handler.handle({
        'intent': 'CREATE_ISSUE',
        'params': {
            'title': 'Test Issue',
            'body': 'Test body'
        }
    })
    
    assert result.success
    assert result.implemented  # NOT a placeholder
    assert 'issue_number' in result.response
    assert 'issue_url' in result.response
    
    # Verify issue actually exists
    github = GitHubService()
    issue = await github.get_issue(result.response['issue_number'])
    assert issue.title == 'Test Issue'
```

### Phase 2: Pattern Extension
**Cursor Agent - 3 hours**

Using Code's pattern as model, implement remaining EXECUTION handlers:
- `_handle_update_issue`
- `_handle_close_issue`
- `_handle_create_task`
- `_handle_update_task`
- `_handle_create_note`
- `_handle_delete_*` variants

Key requirements:
- Follow exact pattern from Phase 1
- Real API calls (no mocks)
- Proper error handling
- Integration tests for each

### Phase 3: Validation with Serena
**Both Agents - 1 hour**

#### Serena Verification
```python
# Verify no placeholders remain
mcp__serena__search_project(
    query="IMPLEMENTATION IN PROGRESS",
    file_pattern="*handler*.py"
)

# Count implemented handlers
mcp__serena__find_symbol(
    name_regex="_handle_.*",
    relative_path="services/handlers/execution.py"
)

# Verify implemented flag usage
mcp__serena__search_project(
    query="implemented=False",
    file_pattern="*.py"
)
```

#### Integration Testing
```bash
# Run all handler tests with real services
pytest tests/handlers/test_execution_handlers.py -v --integration

# Verify no placeholder responses
grep -r "implemented=False" services/handlers/ || echo "✓ No placeholders"
```

### Phase 4: Evidence Collection
**Lead Developer - 30 minutes**

#### Required Evidence for EXECUTION
1. **API Call Logs**:
```bash
tail -f logs/api_calls.log | grep -E "GitHub|Slack|Notion"
```

2. **Resource Creation Proof**:
- Screenshot of created GitHub issue
- Slack message confirmation
- Notion page link

3. **Performance Metrics**:
```bash
python scripts/benchmark_handlers.py --type=execution
```

4. **Test Results**:
```bash
pytest tests/handlers/ -v --tb=short > evidence/execution_tests.txt
```

## Phase Z: Sub-Gameplan 1 Completion
**Both Agents - 30 minutes**

### Deliverables Checklist
- [ ] All EXECUTION handlers implemented
- [ ] No placeholders remaining (Serena verified)
- [ ] Integration tests passing with real data
- [ ] Evidence package compiled
- [ ] Pattern documented for next sub-gameplan

### Handoff to Sub-Gameplan 2
Document for ANALYSIS handlers:
- Pattern that worked
- Gotchas discovered
- Service integration approach
- Testing strategy

## Success Criteria for Overall GAP

### GAP-1 Complete When
- [ ] All handler categories implemented (via sub-gameplans)
- [ ] Zero "IMPLEMENTATION IN PROGRESS" in codebase
- [ ] All `implemented=True` 
- [ ] Integration tests with real services
- [ ] Evidence for each handler type

### GAP-2 Complete When
- [ ] CLI interface validated
- [ ] Slack enforcement verified
- [ ] Bypass prevention tested
- [ ] Cache performance confirmed

### GAP-3 Complete When  
- [ ] Post-#212 accuracy issues addressed
- [ ] Edge cases handled
- [ ] Documentation accurate

## STOP Conditions

- If service authentication fails
- If architectural redesign needed
- If performance degrades
- If integration points broken

## Agent Division Strategy

**Model**: Code establishes pattern, Cursor extends

**Sub-Gameplan 1** (EXECUTION):
- Code: First handler + pattern
- Cursor: Remaining handlers
- Both: Validation

**Future Sub-Gameplans**:
- Similar pattern
- May adjust based on learnings

## Timeline

**Sub-Gameplan 1**: 6-7 hours
**Sub-Gameplan 2-4**: ~15-20 hours
**GAP-2**: 2-3 hours
**GAP-3**: 6-8 hours
**Total**: 28-41 hours

"It takes as long as it takes" - Quality over speed

---

*Ready to begin with Sub-Gameplan 1: EXECUTION handlers*