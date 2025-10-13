# Phase 2: ANALYSIS Handler - _handle_analyze_commits

**Date**: October 11, 2025, 11:25 AM  
**Agent**: Code Agent  
**Duration**: 3-4 hours estimated  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 2 (ANALYSIS Handlers - First Handler)

---

## Mission

Implement `_handle_analyze_commits` handler with genuine Git analysis functionality, following the established pattern from Phase 1. This is the **first ANALYSIS handler** and will establish the pattern for the remaining two ANALYSIS handlers.

**Context**: Phase 1 established the implementation pattern with EXECUTION handlers. Now we apply that pattern to ANALYSIS category, starting with commit analysis.

---

## Success Criteria

- [ ] `_handle_analyze_commits` performs real Git commit analysis
- [ ] Commits are actually analyzed (not just returning `success=True`)
- [ ] Tests demonstrate actual Git integration
- [ ] Pattern follows Phase 1 (validation, service call, error handling)
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual analysis of commits

---

## Phase 2 Structure

### Part 1: Study the Pattern (30 min)

**Reference**: `dev/2025/10/11/handler-implementation-pattern.md` (from Phase 1)

#### Step 1.1: Review Established Pattern

The Phase 1 pattern document contains:
1. Method signature structure
2. Parameter extraction & validation
3. Service integration approach
4. API call pattern
5. Success response structure
6. Error handling pattern

**Review this document carefully** - it's your implementation guide.

#### Step 1.2: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_analyze_commits` (line 652 per reconciliation)

**Current placeholder** (approximately):
```python
async def _handle_analyze_commits(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ANALYZE_COMMITS intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': f'Commit analysis handler is ready for {repository} ({timeframe})'
    }
```

**Document what needs to change**:
- What parameters does it expect? (repository, timeframe, author?, branch?)
- What should it actually do? (analyze commits, extract patterns, return insights)
- What service does it need? (GitHubDomainService? GitService? New service?)

---

### Part 2: Determine Service Requirements (30 min)

#### Step 2.1: Check for Existing Git Analysis Service

```bash
# Search for Git-related services
find services/integrations -name "*git*" -type f

# Check GitHubDomainService capabilities
grep -n "def.*commit" services/integrations/github_domain_service.py

# Check for any Git analysis utilities
find services -name "*analysis*" -type f
grep -r "analyze.*commit" services/ --include="*.py"
```

**Questions to answer**:
1. Does GitHubDomainService have commit analysis methods?
2. Is there a separate Git analysis service?
3. Do we need to add methods to existing service?
4. Is there utility code we can leverage?

#### Step 2.2: Define Required Service Interface

Based on what you find, define what the service needs to provide:

```python
# Example: What we need from the service
class GitAnalysisService:
    async def get_commits(
        self,
        repository: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        author: Optional[str] = None,
        branch: Optional[str] = None
    ) -> List[Commit]:
        """Get commits matching criteria"""
        pass
    
    async def analyze_commit_patterns(
        self,
        commits: List[Commit]
    ) -> Dict[str, Any]:
        """Analyze commits for patterns, frequency, etc."""
        pass
```

**STOP if service doesn't exist and would require >1 hour to create**  
Report to PM - this might need architectural decision.

---

### Part 3: Write Tests First (TDD) (45 min)

**File**: `tests/intent/test_execution_analysis_handlers.py` (or create new test file)

#### Step 3.1: Create Test Class

```python
import pytest
from datetime import datetime, timedelta
from services.intent.intent_service import IntentService

class TestAnalysisHandlers:
    """Tests for ANALYSIS handlers"""
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with required services"""
        service = IntentService()
        # Ensure required services are registered
        return service
    
    # Tests go here
```

#### Step 3.2: Write Unit Tests

**Test 1: Successful commit analysis**
```python
@pytest.mark.asyncio
async def test_handle_analyze_commits_success(self, intent_service):
    """Test successful commit analysis"""
    result = await intent_service._handle_analyze_commits(
        query="analyze commits in piper-morgan from last week",
        params={
            'repository': 'piper-morgan',
            'timeframe': 'last_week',
            'since': (datetime.now() - timedelta(days=7)).isoformat()
        }
    )
    
    assert result['success'] is True
    assert 'requires_clarification' not in result  # No placeholder!
    assert 'commits' in result or 'analysis' in result
    assert 'commit_count' in result
```

**Test 2: Missing repository parameter**
```python
@pytest.mark.asyncio
async def test_handle_analyze_commits_missing_repository(self, intent_service):
    """Test error when repository missing"""
    result = await intent_service._handle_analyze_commits(
        query="analyze commits from last week",
        params={'timeframe': 'last_week'}  # No repository
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'repository' in result['error'].lower()
```

**Test 3: Invalid timeframe**
```python
@pytest.mark.asyncio
async def test_handle_analyze_commits_invalid_timeframe(self, intent_service):
    """Test handling of invalid timeframe"""
    result = await intent_service._handle_analyze_commits(
        query="analyze commits in piper-morgan",
        params={
            'repository': 'piper-morgan',
            'timeframe': 'invalid_time'
        }
    )
    
    # Should either validate timeframe or proceed with default
    assert 'success' in result
```

**Test 4: Empty commit results**
```python
@pytest.mark.asyncio
async def test_handle_analyze_commits_no_commits(self, intent_service):
    """Test when no commits found in timeframe"""
    result = await intent_service._handle_analyze_commits(
        query="analyze commits",
        params={
            'repository': 'piper-morgan',
            'since': '2020-01-01T00:00:00',
            'until': '2020-01-02T00:00:00'  # Unlikely to have commits
        }
    )
    
    assert result['success'] is True
    assert result.get('commit_count', 0) == 0
    assert 'message' in result  # Should inform user no commits found
```

#### Step 3.3: Write Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_handle_analyze_commits_real_repository(self, intent_service):
    """Test with real repository analysis"""
    
    # Use actual piper-morgan repository
    result = await intent_service._handle_analyze_commits(
        query="analyze commits in piper-morgan from last month",
        params={
            'repository': 'piper-morgan',
            'since': (datetime.now() - timedelta(days=30)).isoformat()
        }
    )
    
    # Verify analysis succeeded
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify we got actual data
    assert 'commit_count' in result
    assert result['commit_count'] >= 0
    
    # Verify analysis includes useful information
    # (What exactly depends on what the analysis provides)
    assert 'commits' in result or 'summary' in result or 'analysis' in result
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers -v
# Should fail because _handle_analyze_commits is still placeholder
```

---

### Part 4: Implement Handler (90 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_analyze_commits` (currently line 652)

#### Step 4.1: Replace Placeholder with Real Implementation

Follow the Phase 1 pattern exactly:

```python
async def _handle_analyze_commits(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ANALYZE_COMMITS intent - FULLY IMPLEMENTED"""
    try:
        # 1. Extract and validate parameters
        repository = params.get('repository')
        if not repository:
            logger.warning("Repository missing for commit analysis")
            return {
                'success': False,
                'error': 'Repository name is required for commit analysis'
            }
        
        # Get time parameters (with defaults)
        since_str = params.get('since')
        until_str = params.get('until')
        timeframe = params.get('timeframe', 'last_week')
        author = params.get('author')
        branch = params.get('branch', 'main')
        
        # Parse datetime strings if provided
        since = datetime.fromisoformat(since_str) if since_str else None
        until = datetime.fromisoformat(until_str) if until_str else None
        
        # Apply default timeframe if not specified
        if not since:
            if timeframe == 'last_week':
                since = datetime.now() - timedelta(days=7)
            elif timeframe == 'last_month':
                since = datetime.now() - timedelta(days=30)
            elif timeframe == 'last_year':
                since = datetime.now() - timedelta(days=365)
            else:
                since = datetime.now() - timedelta(days=7)  # Default
        
        # 2. Get Git/GitHub service
        github_service = self.service_registry.get('github')
        if not github_service:
            logger.error("GitHub service not available for commit analysis")
            return {
                'success': False,
                'error': 'GitHub service not configured'
            }
        
        # 3. Fetch commits
        # NOTE: You'll need to check what method exists in GitHubDomainService
        # It might be get_commits(), list_commits(), or you may need to add it
        commits = await github_service.get_commits(
            repository=repository,
            since=since,
            until=until,
            author=author,
            branch=branch
        )
        
        # 4. Analyze commits
        commit_count = len(commits)
        
        # Basic analysis (expand based on requirements)
        authors = {}
        for commit in commits:
            author_name = commit.author.name if hasattr(commit, 'author') else 'Unknown'
            authors[author_name] = authors.get(author_name, 0) + 1
        
        # 5. Return success with analysis
        logger.info(f"Analyzed {commit_count} commits in {repository}")
        return {
            'success': True,
            'repository': repository,
            'commit_count': commit_count,
            'timeframe': {
                'since': since.isoformat() if since else None,
                'until': until.isoformat() if until else None
            },
            'authors': authors,
            'commits': [
                {
                    'sha': c.sha,
                    'message': c.commit.message if hasattr(c.commit, 'message') else str(c),
                    'author': c.author.name if hasattr(c, 'author') else 'Unknown',
                    'date': c.commit.author.date.isoformat() if hasattr(c.commit, 'author') else None
                }
                for c in commits[:10]  # First 10 commits
            ] if commits else []
        }
        
    except Exception as e:
        # 6. Handle errors
        logger.error(f"Failed to analyze commits: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to analyze commits: {str(e)}'
        }
```

**Key Requirements**:
- Follow Phase 1 pattern (validation → service → response → error handling)
- Remove ALL placeholder markers
- Add comprehensive logging
- Handle missing/invalid parameters gracefully
- Return real analysis data

#### Step 4.2: Verify or Add Service Methods

**Check if `get_commits()` exists**:
```bash
grep -n "def get_commits\|def list_commits" services/integrations/github_domain_service.py
```

**If method doesn't exist**, you'll need to add it to GitHubDomainService:

```python
# In GitHubDomainService
async def get_commits(
    self,
    repository: str,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    author: Optional[str] = None,
    branch: str = 'main'
) -> List[Commit]:
    """Get commits from repository matching criteria"""
    # Implementation using GitHub API
    # GET /repos/{owner}/{repo}/commits
    pass
```

**STOP if this is complex** - Report to PM if service work is >30 minutes

---

### Part 5: Run Tests (Green Phase) (30 min)

#### Step 5.1: Run Unit Tests

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers -v

# Expected: All unit tests pass ✅
```

#### Step 5.2: Run Integration Test

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers::test_handle_analyze_commits_real_repository -v --log-cli-level=INFO

# Expected:
# 1. Test fetches real commits from repository
# 2. Test analyzes commits
# 3. Test returns real data
# ALL PASS ✅
```

#### Step 5.3: Manual Verification

```bash
# Start Piper Morgan
python main.py

# In another terminal, test the handler
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "analyze commits in piper-morgan from last week"}'

# Check logs for:
# - Real Git API calls
# - Commit analysis
# - Success response with data
# - No "requires_clarification"
```

**Capture all terminal output for evidence**

---

### Part 6: Evidence Collection (30 min)

#### Required Evidence

**1. Test Results**
```bash
# Run full ANALYSIS test suite
pytest tests/intent/ -k "analyze_commits" -v > dev/2025/10/11/phase2-test-results.txt

# Capture output showing:
# - All tests pass
# - Integration test shows real commit analysis
```

**2. Commit Analysis Logs**
```bash
# Show actual Git/GitHub API calls
tail -f logs/app.log | grep -E "github|commit|analysis"

# Should show:
# - GET request to GitHub for commits
# - Repository and timeframe
# - Commit count
# - Analysis results
```

**3. Analysis Output Sample**
Save a sample of actual analysis output showing:
- Real repository analyzed
- Actual commit count
- Author breakdown
- Commit summaries

**4. Pattern Comparison**
Create: `dev/2025/10/11/phase2-pattern-comparison.md`

```markdown
# Pattern Comparison: EXECUTION vs ANALYSIS

## _handle_update_issue (EXECUTION - Phase 1)
```python
[Copy validation, service call, response structure]
```

## _handle_analyze_commits (ANALYSIS - Phase 2)
```python
[Copy validation, service call, response structure]
```

## Pattern Consistency
- ✅ Same validation approach
- ✅ Same service integration approach
- ✅ Same error handling
- ✅ Same logging approach
- ✅ No placeholder responses

## Differences (Expected)
- EXECUTION: Creates/updates resources
- ANALYSIS: Reads and analyzes data
- Different service methods
- Different response structure (analysis vs confirmation)
```

---

## Phase 2 Completion Criteria

- [ ] Tests written (TDD red phase)
- [ ] Service methods verified or added
- [ ] Implementation complete (following pattern)
- [ ] Tests passing (TDD green phase)
- [ ] Integration test shows real commit analysis
- [ ] No placeholder responses (`requires_clarification` removed)
- [ ] Evidence collected (tests, logs, analysis samples)
- [ ] Pattern consistency verified

---

## STOP Conditions

**STOP and report to PM if**:
- Git service doesn't exist and would require >30 min to create
- GitHub API doesn't support commit analysis
- Analysis requirements are unclear
- Pattern from Phase 1 doesn't apply well
- Implementation takes >4 hours

---

## Deliverables

1. **Implementation**: Updated `services/intent/intent_service.py`
2. **Tests**: Updated or new test file for ANALYSIS handlers
3. **Test Results**: `dev/2025/10/11/phase2-test-results.txt`
4. **Pattern Comparison**: `dev/2025/10/11/phase2-pattern-comparison.md`
5. **Evidence**: Logs, analysis samples, API call records

---

## After Phase 2

**Report to PM**:
1. Implementation complete with evidence
2. ANALYSIS pattern established (1/3 handlers done)
3. Lessons learned vs EXECUTION pattern
4. Estimate for remaining ANALYSIS handlers
5. Ready for next phase authorization

**Do NOT proceed to next handler without PM authorization**

---

## Progress Tracking

**Before Phase 2**:
- GREAT-4D handlers: 2/10 complete (20%)
- ANALYSIS: 0/3 complete

**After Phase 2**:
- GREAT-4D handlers: 3/10 complete (30%)
- ANALYSIS: 1/3 complete (33%)

**Remaining**:
- ANALYSIS: 2 handlers (~7-9 hours)
- SYNTHESIS: 2 handlers (~7-9 hours)
- STRATEGY: 2 handlers (~7-9 hours)
- LEARNING: 1 handler (~5-6 hours)
- **Total**: ~23-37 hours remaining

---

*Phase 2 prompt created: October 11, 2025, 11:25 AM*  
*Agent: Code Agent*  
*Duration: 3-4 hours*  
*First ANALYSIS handler - establishes category pattern*
