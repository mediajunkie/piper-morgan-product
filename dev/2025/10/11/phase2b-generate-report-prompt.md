# Phase 2B: ANALYSIS Handler - _handle_generate_report

**Date**: October 11, 2025, 11:44 AM  
**Agent**: Code Agent  
**Duration**: 1-2 hours estimated (based on Phase 2 velocity)  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 2 (ANALYSIS Handlers - Second Handler)

---

## Mission

Implement `_handle_generate_report` handler with genuine report generation functionality, following the established pattern from Phases 1 and 2. This is the **second ANALYSIS handler** (2/3).

**Context**: Phase 2 showed 95% velocity improvement by following the pattern. Continue that momentum with report generation.

---

## Success Criteria

- [ ] `_handle_generate_report` generates real reports
- [ ] Reports are actually created (not just returning `success=True`)
- [ ] Tests demonstrate actual report generation
- [ ] Pattern follows Phase 1 & 2 (validation, service call, error handling)
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual generated reports

---

## Phase 2B Structure

### Part 1: Study the Pattern (15 min)

**Reference**: 
- `dev/2025/10/11/handler-implementation-pattern.md` (Phase 1)
- `dev/2025/10/11/phase2-pattern-comparison.md` (Phase 2)

#### Step 1.1: Review Established Pattern

You've now implemented:
1. `_handle_create_issue` (EXECUTION) - creates resources
2. `_handle_update_issue` (EXECUTION) - updates resources
3. `_handle_analyze_commits` (ANALYSIS) - analyzes data

All follow the same pattern. Continue that pattern here.

#### Step 1.2: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_generate_report` (line 692 per reconciliation)

**Current placeholder** (approximately):
```python
async def _handle_generate_report(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GENERATE_REPORT intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Report generation handler is ready but needs reporting service integration'
    }
```

**Questions**:
- What type of reports? (commit report, project status, analysis summary?)
- What parameters? (report_type, data_source, timeframe, format?)
- What output format? (markdown, JSON, HTML?)

---

### Part 2: Determine Service Requirements (20 min)

#### Step 2.1: Check for Reporting Service

```bash
# Search for reporting/report services
find services -name "*report*" -type f
grep -r "report" services/integrations/ --include="*.py"

# Check what we used in Phase 2
grep -n "get_recent_activity" services/intent/intent_service.py
```

**Strategy Options**:

**Option A: Reuse Existing Services**
- Use `get_recent_activity()` like Phase 2
- Format the data as a report
- No new service needed (FAST)

**Option B: Create Simple Report Formatter**
- Create utility function to format data
- Keep it simple (markdown or JSON)
- ~20-30 min work

**Option C: Full Reporting Service**
- Create new `ReportingService`
- Complex, requires architecture
- >30 min work (STOP condition)

**Recommendation**: Try Option A first (reuse), fall back to Option B if needed.

#### Step 2.2: Define Report Structure

Based on analysis, define what a report should contain:

```python
# Example report structure
{
    'success': True,
    'report_type': 'commit_analysis',
    'title': 'Commit Analysis Report for piper-morgan',
    'generated_at': '2025-10-11T11:44:00',
    'summary': {
        'total_commits': 45,
        'authors': {'Alice': 30, 'Bob': 15},
        'timeframe': {'since': '...', 'until': '...'}
    },
    'content': '# Report Title\n\n## Summary\n...',  # Markdown format
    'format': 'markdown'
}
```

---

### Part 3: Write Tests First (TDD) (30 min)

**File**: `tests/intent/test_execution_analysis_handlers.py`

#### Step 3.1: Add Tests to Existing TestAnalysisHandlers Class

```python
class TestAnalysisHandlers:
    """Tests for ANALYSIS handlers"""
    
    # ... existing tests for analyze_commits ...
    
    # New tests for generate_report
    
    @pytest.mark.asyncio
    async def test_handle_generate_report_success(self, intent_service):
        """Test successful report generation"""
        result = await intent_service._handle_generate_report(
            query="generate report for piper-morgan commits",
            params={
                'report_type': 'commit_analysis',
                'repository': 'piper-morgan',
                'timeframe': 'last_week'
            }
        )
        
        assert result['success'] is True
        assert 'requires_clarification' not in result  # No placeholder!
        assert 'report_type' in result
        assert 'content' in result or 'summary' in result
        assert 'generated_at' in result
    
    @pytest.mark.asyncio
    async def test_handle_generate_report_missing_type(self, intent_service):
        """Test error when report type missing"""
        result = await intent_service._handle_generate_report(
            query="generate report",
            params={'repository': 'piper-morgan'}  # No report_type
        )
        
        # Should either use default report_type or return error
        assert 'success' in result
    
    @pytest.mark.asyncio
    async def test_handle_generate_report_missing_repository(self, intent_service):
        """Test error when repository missing"""
        result = await intent_service._handle_generate_report(
            query="generate commit report",
            params={'report_type': 'commit_analysis'}  # No repository
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'repository' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_handle_generate_report_unknown_type(self, intent_service):
        """Test handling of unknown report type"""
        result = await intent_service._handle_generate_report(
            query="generate magic report",
            params={
                'report_type': 'unknown_type',
                'repository': 'piper-morgan'
            }
        )
        
        # Should either use default or return error
        assert 'success' in result
```

#### Step 3.2: Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_handle_generate_report_real_data(self, intent_service):
    """Test report generation with real repository data"""
    
    result = await intent_service._handle_generate_report(
        query="generate commit analysis report for piper-morgan",
        params={
            'report_type': 'commit_analysis',
            'repository': 'piper-morgan',
            'since': (datetime.now() - timedelta(days=30)).isoformat()
        }
    )
    
    # Verify report generated
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify report has content
    assert 'content' in result or 'summary' in result
    assert result.get('report_type') == 'commit_analysis'
    
    # Verify report has data
    if 'content' in result:
        assert len(result['content']) > 100  # Should be substantial
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers -k "generate_report" -v
# Should fail because _handle_generate_report is still placeholder
```

---

### Part 4: Implement Handler (45 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_generate_report` (currently line 692)

#### Step 4.1: Replace Placeholder with Real Implementation

**Strategy**: Reuse `get_recent_activity()` and format as report

```python
async def _handle_generate_report(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GENERATE_REPORT intent - FULLY IMPLEMENTED"""
    try:
        # 1. Extract and validate parameters
        report_type = params.get('report_type', 'commit_analysis')
        repository = params.get('repository')
        
        if not repository:
            logger.warning("Repository missing for report generation")
            return {
                'success': False,
                'error': 'Repository name is required for report generation'
            }
        
        # Get time parameters
        since_str = params.get('since')
        until_str = params.get('until')
        timeframe = params.get('timeframe', 'last_week')
        
        # Parse datetime strings if provided
        since = datetime.fromisoformat(since_str) if since_str else None
        until = datetime.fromisoformat(until_str) if until_str else None
        
        # Apply default timeframe
        if not since:
            if timeframe == 'last_week':
                since = datetime.now() - timedelta(days=7)
            elif timeframe == 'last_month':
                since = datetime.now() - timedelta(days=30)
            else:
                since = datetime.now() - timedelta(days=7)
        
        # 2. Get GitHub service
        github_service = self.service_registry.get('github')
        if not github_service:
            logger.error("GitHub service not available for report generation")
            return {
                'success': False,
                'error': 'GitHub service not configured'
            }
        
        # 3. Fetch data for report (reuse from Phase 2)
        activity = await github_service.get_recent_activity(
            repo=repository,
            since=since,
            until=until
        )
        
        # 4. Generate report based on type
        if report_type == 'commit_analysis':
            report_content = self._format_commit_report(
                repository=repository,
                activity=activity,
                since=since,
                until=until
            )
        else:
            # Default to commit analysis
            report_content = self._format_commit_report(
                repository=repository,
                activity=activity,
                since=since,
                until=until
            )
        
        # 5. Return success with report
        logger.info(f"Generated {report_type} report for {repository}")
        return {
            'success': True,
            'report_type': report_type,
            'repository': repository,
            'generated_at': datetime.now().isoformat(),
            'timeframe': {
                'since': since.isoformat() if since else None,
                'until': until.isoformat() if until else None
            },
            'content': report_content,
            'format': 'markdown'
        }
        
    except Exception as e:
        # 6. Handle errors
        logger.error(f"Failed to generate report: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to generate report: {str(e)}'
        }

def _format_commit_report(
    self,
    repository: str,
    activity: Dict[str, Any],
    since: datetime,
    until: Optional[datetime]
) -> str:
    """Format commit analysis as markdown report"""
    
    # Extract data
    commits = activity.get('commits', [])
    commit_count = len(commits)
    
    # Analyze authors
    authors = {}
    for commit in commits:
        author = commit.get('author', 'Unknown')
        authors[author] = authors.get(author, 0) + 1
    
    # Build markdown report
    report = f"# Commit Analysis Report\n\n"
    report += f"**Repository**: {repository}\n"
    report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Period**: {since.strftime('%Y-%m-%d')} to "
    report += f"{until.strftime('%Y-%m-%d') if until else 'present'}\n\n"
    
    report += f"## Summary\n\n"
    report += f"- **Total Commits**: {commit_count}\n"
    report += f"- **Contributors**: {len(authors)}\n\n"
    
    if authors:
        report += f"## Contributors\n\n"
        for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{author}**: {count} commits\n"
        report += "\n"
    
    if commits:
        report += f"## Recent Commits\n\n"
        for commit in commits[:10]:  # First 10
            msg = commit.get('message', 'No message')
            author = commit.get('author', 'Unknown')
            date = commit.get('date', 'Unknown date')
            report += f"- **{msg[:80]}** by {author} on {date}\n"
    
    return report
```

**Key Requirements**:
- Follow Phase 1 & 2 pattern exactly
- Remove ALL placeholder markers
- Reuse existing services (avoid new service creation)
- Add helper method `_format_commit_report()` for clean code
- Return actual report content

---

### Part 5: Run Tests (Green Phase) (15 min)

#### Step 5.1: Run Unit Tests

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers -k "generate_report" -v

# Expected: All unit tests pass ✅
```

#### Step 5.2: Run Integration Test

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestAnalysisHandlers::test_handle_generate_report_real_data -v --log-cli-level=INFO

# Expected: Real report generated with actual data ✅
```

#### Step 5.3: Manual Verification

```bash
# Test the handler
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "generate commit report for piper-morgan from last week"}'

# Check response contains actual markdown report
```

---

### Part 6: Evidence Collection (15 min)

#### Required Evidence

**1. Test Results**
```bash
pytest tests/intent/ -k "generate_report" -v > dev/2025/10/11/phase2b-test-results.txt
```

**2. Sample Report Output**
Save an actual generated report to `dev/2025/10/11/phase2b-sample-report.md`

**3. Pattern Verification**
Add to `dev/2025/10/11/phase2-pattern-comparison.md`:

```markdown
## _handle_generate_report (ANALYSIS - Phase 2B)

### Pattern Match
- ✅ Validation (report_type, repository)
- ✅ Service integration (get_recent_activity)
- ✅ Data processing (_format_commit_report helper)
- ✅ Error handling
- ✅ Logging
- ✅ No placeholders

### Implementation Notes
- Reused get_recent_activity() from Phase 2
- Added helper method for report formatting
- Markdown format for readability
- Follows exact same pattern as analyze_commits
```

---

## Phase 2B Completion Criteria

- [ ] Tests written (TDD red phase)
- [ ] Implementation complete (following pattern)
- [ ] Tests passing (TDD green phase)
- [ ] Integration test shows real report generation
- [ ] No placeholder responses
- [ ] Evidence collected (tests, sample report)
- [ ] Pattern consistency verified

---

## STOP Conditions

**STOP and report to PM if**:
- Report generation requires complex new service (>30 min)
- Report format requirements unclear
- Pattern doesn't apply well
- Implementation takes >2 hours

---

## Deliverables

1. **Implementation**: Updated `services/intent/intent_service.py`
2. **Helper Method**: `_format_commit_report()` added
3. **Tests**: Updated `tests/intent/test_execution_analysis_handlers.py`
4. **Test Results**: `dev/2025/10/11/phase2b-test-results.txt`
5. **Sample Report**: `dev/2025/10/11/phase2b-sample-report.md`
6. **Evidence**: Updated pattern comparison document

---

## After Phase 2B

**Report to PM**:
1. Implementation complete with evidence
2. ANALYSIS 2/3 complete (67%)
3. One ANALYSIS handler remaining (`_handle_analyze_data`)
4. Ready for Phase 2C authorization

**Progress Update**:
- GREAT-4D handlers: 4/10 complete (40%)
- ANALYSIS: 2/3 complete (67%)
- Remaining: 6 handlers

---

## Expected Velocity

**Based on Phase 2 results**:
- Estimated: 1-2 hours
- Likely actual: 10-30 minutes (if pattern holds)
- Pattern is established, services exist, momentum is high

---

*Phase 2B prompt created: October 11, 2025, 11:44 AM*  
*Agent: Code Agent*  
*Duration: 1-2 hours estimated*  
*Second ANALYSIS handler - continuing the momentum*
