# Phase 1: Pattern Establishment - _handle_update_issue

**Date**: October 11, 2025, 10:09 AM  
**Agent**: Code Agent  
**Duration**: 3-4 hours estimated  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 1 (EXECUTION Handlers)

---

## Mission

Implement `_handle_update_issue` handler with genuine functionality, establishing the pattern that will be used for all remaining handlers. This is the **most critical phase** - we get this right, and the other 7 handlers follow the same pattern.

**Context**: `_handle_create_issue` already works perfectly. We copy its pattern and adapt for updating issues.

---

## Success Criteria

- [ ] `_handle_update_issue` makes real GitHub API calls
- [ ] Issues are actually updated (not just returning `success=True`)
- [ ] Tests demonstrate actual GitHub integration
- [ ] Pattern is documented for future handlers
- [ ] Zero "requires_clarification" responses
- [ ] Evidence shows actual API calls and updated issues

---

## Phase 1 Structure

### Part 1: Study the Working Pattern (30 min)

**File**: `services/intent/intent_service.py`  
**Working handler**: `_handle_create_issue` (already implemented)

#### Step 1.1: Analyze Working Implementation

Read `_handle_create_issue` carefully and document:

1. **Parameter extraction pattern**:
```python
# How does it get params?
# How does it validate?
# What error handling?
```

2. **Service integration pattern**:
```python
# How does it get GitHubDomainService?
# How does it call the service?
# What does it pass?
```

3. **Response construction pattern**:
```python
# What does it return on success?
# What does it return on error?
# What data structure?
```

4. **Error handling pattern**:
```python
# Try/except structure?
# Logging approach?
# Error response format?
```

#### Step 1.2: Document the Pattern

Create: `dev/2025/10/11/handler-implementation-pattern.md`

```markdown
# Handler Implementation Pattern

Based on `_handle_create_issue` (working implementation)

## Pattern Structure

### 1. Method Signature
```python
async def _handle_X(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """[Description] - FULLY IMPLEMENTED"""
```

### 2. Parameter Extraction & Validation
[Copy actual pattern from _handle_create_issue]

### 3. Service Integration
[Copy actual pattern from _handle_create_issue]

### 4. API Call
[Copy actual pattern from _handle_create_issue]

### 5. Success Response
[Copy actual pattern from _handle_create_issue]

### 6. Error Handling
[Copy actual pattern from _handle_create_issue]

## Key Principles
- [List principles observed in working code]

## Anti-Patterns to Avoid
- Never return `success=True` without doing work
- Never return `requires_clarification=True` as placeholder
- Always log errors
- Always use try/except
```

**Deliverable**: Pattern document for reference

---

### Part 2: Write Tests First (TDD) (45 min)

**File**: `tests/intent/test_intent_handlers.py` (or new file if needed)

#### Step 2.1: Create Test Structure

```python
import pytest
from services.intent.intent_service import IntentService
from services.integrations.github_domain_service import GitHubDomainService

class TestHandleUpdateIssue:
    """Tests for _handle_update_issue handler"""
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with real GitHubDomainService"""
        # Copy fixture pattern from test_handle_create_issue if it exists
        service = IntentService()
        # Ensure GitHubDomainService is registered
        return service
    
    # Tests go here
```

#### Step 2.2: Write Unit Tests

**Test 1: Successful update**
```python
@pytest.mark.asyncio
async def test_handle_update_issue_success(self, intent_service):
    """Test successful issue update"""
    result = await intent_service._handle_update_issue(
        query="update issue 123 with title 'Updated Title'",
        params={
            'issue_number': 123,
            'title': 'Updated Title',
            'body': 'Updated body text'
        }
    )
    
    assert result['success'] is True
    assert 'requires_clarification' not in result  # No placeholder!
    assert 'issue_number' in result
    assert result['issue_number'] == 123
```

**Test 2: Missing issue number**
```python
@pytest.mark.asyncio
async def test_handle_update_issue_missing_number(self, intent_service):
    """Test error when issue number missing"""
    result = await intent_service._handle_update_issue(
        query="update issue",
        params={'title': 'New Title'}  # No issue_number
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'issue number' in result['error'].lower()
```

**Test 3: Invalid issue number**
```python
@pytest.mark.asyncio
async def test_handle_update_issue_invalid_number(self, intent_service):
    """Test error when issue doesn't exist"""
    result = await intent_service._handle_update_issue(
        query="update issue 999999",
        params={'issue_number': 999999, 'title': 'Test'}
    )
    
    assert result['success'] is False
    assert 'error' in result
```

#### Step 2.3: Write Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_handle_update_issue_real_github(self, intent_service):
    """Test with real GitHub API - creates then updates issue"""
    
    # Step 1: Create a test issue first
    create_result = await intent_service._handle_create_issue(
        query="create test issue",
        params={
            'title': 'Test Issue for Update',
            'body': 'Original body'
        }
    )
    assert create_result['success'] is True
    issue_number = create_result['issue_number']
    
    try:
        # Step 2: Update the issue
        update_result = await intent_service._handle_update_issue(
            query=f"update issue {issue_number}",
            params={
                'issue_number': issue_number,
                'title': 'UPDATED: Test Issue',
                'body': 'Updated body text'
            }
        )
        
        # Verify update succeeded
        assert update_result['success'] is True
        assert 'requires_clarification' not in update_result
        assert update_result['issue_number'] == issue_number
        
        # Step 3: Verify issue was actually updated on GitHub
        github_service = intent_service.service_registry.get('github')
        updated_issue = await github_service.get_issue(issue_number)
        assert updated_issue.title == 'UPDATED: Test Issue'
        assert updated_issue.body == 'Updated body text'
        
    finally:
        # Cleanup: Close the test issue
        github_service = intent_service.service_registry.get('github')
        await github_service.update_issue(
            issue_number=issue_number,
            state='closed'
        )
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_intent_handlers.py::TestHandleUpdateIssue -v
# Should fail because _handle_update_issue is still placeholder
```

**Deliverable**: Failing tests that specify exact behavior

---

### Part 3: Implement Handler (90 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_update_issue` (currently lines 495-516)

#### Step 3.1: Replace Placeholder

**Current placeholder** (approximately):
```python
async def _handle_update_issue(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle UPDATE_ISSUE intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Issue update requires clarification'
    }
```

**Replace with real implementation** following the pattern from Part 1:

```python
async def _handle_update_issue(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle UPDATE_ISSUE intent - FULLY IMPLEMENTED"""
    try:
        # 1. Extract and validate parameters
        issue_number = params.get('issue_number')
        if not issue_number:
            logger.warning("Issue number missing for update")
            return {
                'success': False,
                'error': 'Issue number is required for updates'
            }
        
        # Get optional update fields
        title = params.get('title')
        body = params.get('body')
        state = params.get('state')  # 'open' or 'closed'
        labels = params.get('labels')
        
        # Ensure at least one field to update
        if not any([title, body, state, labels]):
            logger.warning("No fields to update provided")
            return {
                'success': False,
                'error': 'At least one field to update must be provided'
            }
        
        # 2. Get GitHub service
        github_service = self.service_registry.get('github')
        if not github_service:
            logger.error("GitHub service not available")
            return {
                'success': False,
                'error': 'GitHub service not configured'
            }
        
        # 3. Call GitHub API to update issue
        updated_issue = await github_service.update_issue(
            issue_number=issue_number,
            title=title,
            body=body,
            state=state,
            labels=labels
        )
        
        # 4. Return success with updated issue data
        logger.info(f"Successfully updated issue #{issue_number}")
        return {
            'success': True,
            'issue_number': updated_issue.number,
            'title': updated_issue.title,
            'state': updated_issue.state,
            'updated_at': updated_issue.updated_at.isoformat() if hasattr(updated_issue.updated_at, 'isoformat') else str(updated_issue.updated_at),
            'html_url': updated_issue.html_url
        }
        
    except Exception as e:
        # 5. Handle errors
        logger.error(f"Failed to update issue: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to update issue: {str(e)}'
        }
```

**Key Requirements**:
- Follow exact pattern from `_handle_create_issue`
- Remove ALL placeholder markers (`IMPLEMENTATION IN PROGRESS`, `requires_clarification`)
- Add comprehensive logging
- Handle all error cases
- Return real data from GitHub API

#### Step 3.2: Verify GitHubDomainService Has update_issue Method

```python
# Check if update_issue exists in GitHubDomainService
grep -n "def update_issue" services/integrations/github_domain_service.py
```

**If method doesn't exist**, you need to add it:

```python
# In GitHubDomainService
async def update_issue(
    self,
    issue_number: int,
    title: Optional[str] = None,
    body: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[List[str]] = None
) -> Issue:
    """Update an existing GitHub issue"""
    # Implementation here using GitHub API
    # PATCH /repos/{owner}/{repo}/issues/{number}
```

**STOP if this is complex** - report to PM before implementing service method.

---

### Part 4: Run Tests (Green Phase) (30 min)

#### Step 4.1: Run Unit Tests

```bash
pytest tests/intent/test_intent_handlers.py::TestHandleUpdateIssue -v

# Expected: All unit tests pass ✅
```

#### Step 4.2: Run Integration Test

```bash
pytest tests/intent/test_intent_handlers.py::TestHandleUpdateIssue::test_handle_update_issue_real_github -v --log-cli-level=INFO

# Expected:
# 1. Test creates issue
# 2. Test updates issue  
# 3. Test verifies update on GitHub
# 4. Test cleans up
# ALL PASS ✅
```

#### Step 4.3: Manual Verification

```bash
# Start Piper Morgan
python main.py

# In another terminal, test the handler
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "update issue 123 with title Updated Title"}'

# Check logs for:
# - Real API call to GitHub
# - Success response
# - No "requires_clarification"
```

**Capture all terminal output for evidence**

---

### Part 5: Evidence Collection (30 min)

#### Required Evidence

**1. Test Results**
```bash
# Run full test suite
pytest tests/intent/test_intent_handlers.py -v > dev/2025/10/11/phase1-test-results.txt

# Capture output showing:
# - All tests pass
# - Integration test shows real GitHub interaction
```

**2. API Call Logs**
```bash
# Show actual GitHub API calls
tail -f logs/app.log | grep -E "github|update_issue"

# Should show:
# - PATCH request to GitHub
# - Issue number
# - Updated fields
# - Success response
```

**3. GitHub Verification**
- Screenshot or log showing issue was actually updated
- GitHub issue URL before and after update
- Timestamp of update

**4. Code Comparison**
Create: `dev/2025/10/11/phase1-pattern-comparison.md`

```markdown
# Pattern Comparison: Create vs Update

## _handle_create_issue (Working)
```python
[Copy relevant parts]
```

## _handle_update_issue (New Implementation)
```python
[Copy relevant parts]
```

## Pattern Consistency
- ✅ Same parameter extraction approach
- ✅ Same service integration approach
- ✅ Same error handling approach
- ✅ Same response structure
- ✅ Same logging approach

## Differences (Expected)
- Different GitHub API endpoint (POST vs PATCH)
- Different required parameters
- Different validation logic
```

---

## Phase 1 Completion Criteria

- [ ] Tests written (TDD red phase)
- [ ] Implementation complete (following pattern)
- [ ] Tests passing (TDD green phase)
- [ ] Integration test shows real GitHub updates
- [ ] No placeholder responses (`requires_clarification` removed)
- [ ] Evidence collected (tests, logs, GitHub verification)
- [ ] Pattern documented for future handlers
- [ ] Code reviewed against working handler pattern

---

## STOP Conditions

**STOP and report to PM if**:
- `update_issue` method doesn't exist in GitHubDomainService
- GitHub authentication fails
- Pattern from `_handle_create_issue` is unclear or complex
- Tests reveal architectural issues
- Implementation takes >4 hours

---

## Deliverables

1. **Pattern Documentation**: `dev/2025/10/11/handler-implementation-pattern.md`
2. **Tests**: Updated `tests/intent/test_intent_handlers.py`
3. **Implementation**: Updated `services/intent/intent_service.py`
4. **Test Results**: `dev/2025/10/11/phase1-test-results.txt`
5. **Pattern Comparison**: `dev/2025/10/11/phase1-pattern-comparison.md`
6. **Evidence**: Logs, screenshots, GitHub URLs

---

## After Phase 1

**Report to PM**:
1. Implementation complete with evidence
2. Pattern established and documented
3. Lessons learned
4. Estimate for remaining EXECUTION handler
5. Ready for Phase 2 authorization

**Do NOT proceed to Phase 2 without PM authorization**

---

*Phase 1 prompt created: October 11, 2025, 10:09 AM*  
*Agent: Code Agent*  
*Duration: 3-4 hours*  
*Pattern establishment - most critical phase*
