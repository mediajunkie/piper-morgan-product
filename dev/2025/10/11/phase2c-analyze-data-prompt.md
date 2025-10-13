# Phase 2C: ANALYSIS Handler - _handle_analyze_data (Last ANALYSIS Handler)

**Date**: October 11, 2025, 12:58 PM  
**Agent**: Code Agent  
**Duration**: Estimated 1-2 hours (take time needed for quality)  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 2 (ANALYSIS Handlers - Final Handler)

---

## Mission

Implement `_handle_analyze_data` handler with genuine data analysis functionality, completing the ANALYSIS category. This is the **last ANALYSIS handler** and must maintain the same thoroughness and quality as previous implementations.

**Context**: Phases 2 and 2B established ANALYSIS patterns. This handler completes the category at 100%.

**PM Priority**: **Thoroughness and accuracy over speed.** Take the time needed to get this right.

---

## Success Criteria

- [ ] `_handle_analyze_data` performs real data analysis
- [ ] Data is actually analyzed (not just returning `success=True`)
- [ ] Tests demonstrate actual data analysis functionality
- [ ] Pattern follows established ANALYSIS approach (Phases 2 & 2B)
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual analysis with concrete examples
- [ ] **Quality maintained** - thoroughness is paramount

---

## Phase 2C Structure

### Part 1: Study Established ANALYSIS Pattern (30 min)

**Don't rush this part - understand the pattern thoroughly**

#### Step 1.1: Review Both ANALYSIS Handlers

**Compare**:
1. `_handle_analyze_commits` (Phase 2) - line 652
2. `_handle_generate_report` (Phase 2B) - line 749

**Document**:
- What parameters do they accept?
- How do they validate inputs?
- What services do they use?
- What response structure do they return?
- How do they handle errors?
- What makes them ANALYSIS vs EXECUTION?

#### Step 1.2: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_analyze_data` (line 722 per reconciliation)

**Current placeholder** (approximately):
```python
async def _handle_analyze_data(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ANALYZE_DATA intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Data analysis handler ready for {data_type} analysis'
    }
```

**Critical Questions** (answer thoroughly):
1. What type of data should this analyze? (metrics, logs, statistics, trends?)
2. Where does the data come from? (GitHub stats, Slack activity, Notion pages?)
3. What analysis should be performed? (aggregation, trends, patterns, anomalies?)
4. What should the output look like? (summary stats, visualizations, insights?)
5. How is this different from `analyze_commits`? (broader scope? different data source?)

**STOP if requirements are unclear** - Report to PM for clarification before proceeding

---

### Part 2: Define Data Analysis Scope (45 min)

**Be thorough here - this determines implementation quality**

#### Step 2.1: Determine Data Sources

**Investigate available data sources**:

```bash
# Check what data sources we have access to
grep -r "get_.*data\|fetch_.*data\|retrieve_.*data" services/integrations/ --include="*.py"

# Check for analytics/metrics services
find services -name "*metric*" -o -name "*analytic*" -o -name "*stat*"

# Review GitHub service capabilities
grep -n "class GitHubDomainService" services/integrations/github_domain_service.py -A 100

# Check for any data analysis utilities
find services -name "*analysis*" -type f
```

**Document findings**:
```markdown
## Available Data Sources

### GitHub Data
- Issues (count, status, labels, timeline)
- Pull requests (status, reviews, merge time)
- Commits (frequency, authors, patterns) ← Already used in Phase 2
- Repository stats (stars, forks, contributors)

### Slack Data (if configured)
- Message volume
- Channel activity
- User participation

### Notion Data (if configured)
- Page counts
- Update frequency
- Content statistics

### Other Sources
- [List any other sources found]
```

#### Step 2.2: Define Analysis Types

**What kinds of analysis are meaningful?**

Example analysis types:
1. **Aggregation**: Sum, count, average over time periods
2. **Trends**: Identify increasing/decreasing patterns
3. **Comparison**: Compare metrics across time periods or entities
4. **Distribution**: Show how data is distributed
5. **Anomalies**: Identify outliers or unusual patterns

**Choose 2-3 analysis types that**:
- Use available data sources
- Provide valuable insights
- Are implementable with current infrastructure
- Follow ANALYSIS category patterns

#### Step 2.3: Design Response Structure

**Based on chosen analysis types, design response**:

```python
{
    'success': True,
    'data_type': 'repository_metrics',  # or other type
    'analysis_period': {
        'start': '2024-10-01',
        'end': '2024-10-11'
    },
    'metrics': {
        'total_issues': 150,
        'open_issues': 23,
        'closed_issues': 127,
        'avg_close_time_days': 3.5,
        # ... other relevant metrics
    },
    'trends': {
        'issue_creation': 'increasing',
        'close_rate': 'stable',
        # ... other trends
    },
    'insights': [
        'Issue creation rate increased 15% this week',
        'Average close time improved from 4.2 to 3.5 days',
        # ... other insights
    ],
    'raw_data': [
        # Sample of underlying data if useful
    ]
}
```

**Document your design thoroughly** before implementing

---

### Part 3: Write Comprehensive Tests (TDD) (45 min)

**Take time to write thorough tests - they define expected behavior**

**File**: `tests/intent/test_execution_analysis_handlers.py`

#### Step 3.1: Test Structure

```python
class TestHandleAnalyzeData:
    """Comprehensive tests for _handle_analyze_data handler
    
    This handler should analyze data from various sources and provide
    meaningful insights through aggregation, trends, and comparisons.
    """
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with required services"""
        service = IntentService()
        return service
```

#### Step 3.2: Write Thorough Unit Tests

**Test 1: Successful data analysis with all fields**
```python
@pytest.mark.asyncio
async def test_handle_analyze_data_complete_success(self, intent_service):
    """Test successful data analysis with all expected fields"""
    result = await intent_service._handle_analyze_data(
        query="analyze repository metrics for piper-morgan",
        params={
            'data_type': 'repository_metrics',
            'repository': 'piper-morgan',
            'period': 'last_week'
        }
    )
    
    # Verify no placeholder response
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify structure completeness
    assert 'data_type' in result
    assert 'metrics' in result
    assert isinstance(result['metrics'], dict)
    assert len(result['metrics']) > 0
    
    # Verify analysis quality
    if 'trends' in result:
        assert isinstance(result['trends'], dict)
    if 'insights' in result:
        assert isinstance(result['insights'], list)
```

**Test 2: Missing required parameters**
```python
@pytest.mark.asyncio
async def test_handle_analyze_data_missing_data_type(self, intent_service):
    """Test error when data_type parameter missing"""
    result = await intent_service._handle_analyze_data(
        query="analyze data",
        params={}  # Missing required params
    )
    
    assert result['success'] is False
    assert 'error' in result
    # Error message should be helpful
    assert 'data_type' in result['error'].lower() or 'required' in result['error'].lower()
```

**Test 3: Unsupported data type**
```python
@pytest.mark.asyncio
async def test_handle_analyze_data_unsupported_type(self, intent_service):
    """Test handling of unsupported data type"""
    result = await intent_service._handle_analyze_data(
        query="analyze xyz data",
        params={
            'data_type': 'unsupported_type',
            'repository': 'piper-morgan'
        }
    )
    
    # Should either:
    # 1. Return error explaining unsupported type, OR
    # 2. Handle gracefully with limited analysis
    assert 'success' in result
    if result['success'] is False:
        assert 'error' in result
        assert 'unsupported' in result['error'].lower() or 'not available' in result['error'].lower()
```

**Test 4: Empty data scenario**
```python
@pytest.mark.asyncio
async def test_handle_analyze_data_no_data_found(self, intent_service):
    """Test when no data available for analysis"""
    result = await intent_service._handle_analyze_data(
        query="analyze data for nonexistent repository",
        params={
            'data_type': 'repository_metrics',
            'repository': 'nonexistent-repo-xyz-12345'
        }
    )
    
    # Should handle gracefully
    assert result['success'] is True  # Not an error, just no data
    assert 'message' in result or 'metrics' in result
    # Should indicate no data found
```

**Test 5: Multiple data types**
```python
@pytest.mark.asyncio
async def test_handle_analyze_data_multiple_types(self, intent_service):
    """Test analysis of multiple data types simultaneously"""
    result = await intent_service._handle_analyze_data(
        query="analyze all data for piper-morgan",
        params={
            'data_type': ['repository_metrics', 'commit_stats'],
            'repository': 'piper-morgan'
        }
    )
    
    # Should handle multiple types or return clear guidance
    assert 'success' in result
```

#### Step 3.3: Write Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_handle_analyze_data_real_analysis(self, intent_service):
    """Test with real data analysis - comprehensive integration test"""
    
    result = await intent_service._handle_analyze_data(
        query="analyze repository metrics for piper-morgan from last month",
        params={
            'data_type': 'repository_metrics',
            'repository': 'piper-morgan',
            'since': (datetime.now() - timedelta(days=30)).isoformat()
        }
    )
    
    # Verify success
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify we got real analysis
    assert 'metrics' in result
    metrics = result['metrics']
    
    # Verify metrics are meaningful (not just empty/default values)
    assert len(metrics) > 0
    
    # Verify data types are correct
    for key, value in metrics.items():
        assert isinstance(value, (int, float, str, bool, list, dict)), \
            f"Metric {key} has unexpected type: {type(value)}"
    
    # Log results for manual review
    import json
    logger.info(f"Real analysis results: {json.dumps(result, indent=2, default=str)}")
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestHandleAnalyzeData -v
# Should fail - handler is still placeholder
```

**Document test strategy**:
Create `dev/2025/10/11/phase2c-test-strategy.md` explaining:
- What each test validates
- Why these scenarios matter
- What edge cases are covered
- What quality standards are enforced

---

### Part 4: Implement Handler Thoroughly (60-90 min)

**Take the time needed to implement this properly**

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_analyze_data` (currently line 722)

#### Step 4.1: Implementation Structure

**Follow the established pattern, but be thorough**:

```python
async def _handle_analyze_data(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle ANALYZE_DATA intent - FULLY IMPLEMENTED
    
    Analyzes data from various sources (GitHub, Slack, Notion) to provide
    insights through metrics, trends, and patterns.
    
    Supported data_types:
        - 'repository_metrics': GitHub repository statistics
        - 'commit_stats': Commit patterns and frequency
        - 'issue_stats': Issue creation, resolution, and trends
        - [Add other supported types]
    
    Args:
        query: Natural language query describing analysis request
        params: Dictionary containing:
            - data_type (required): Type of data to analyze
            - repository (optional): Repository name for GitHub data
            - since (optional): Start date for analysis period
            - until (optional): End date for analysis period
            - [Other relevant parameters]
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if analysis succeeded
            - data_type: Type of data analyzed
            - metrics: Dictionary of calculated metrics
            - trends: Dictionary of identified trends (if applicable)
            - insights: List of human-readable insights (if applicable)
            - error: Error message (if success is False)
    """
    try:
        # 1. VALIDATION - Be thorough
        data_type = params.get('data_type')
        if not data_type:
            logger.warning("Data type missing for data analysis")
            return {
                'success': False,
                'error': 'data_type parameter is required. Supported types: repository_metrics, commit_stats, issue_stats'
            }
        
        # Normalize data_type to list for consistent handling
        if isinstance(data_type, str):
            data_types = [data_type]
        else:
            data_types = data_type if isinstance(data_type, list) else [str(data_type)]
        
        # Get time period parameters
        repository = params.get('repository')
        since_str = params.get('since')
        until_str = params.get('until')
        period = params.get('period', 'last_week')
        
        # Parse dates
        since = datetime.fromisoformat(since_str) if since_str else None
        until = datetime.fromisoformat(until_str) if until_str else None
        
        # Apply default period if not specified
        if not since:
            if period == 'last_week':
                since = datetime.now() - timedelta(days=7)
            elif period == 'last_month':
                since = datetime.now() - timedelta(days=30)
            elif period == 'last_year':
                since = datetime.now() - timedelta(days=365)
            else:
                since = datetime.now() - timedelta(days=7)  # Default
        
        # 2. GET REQUIRED SERVICES
        github_service = self.service_registry.get('github')
        if not github_service:
            logger.error("GitHub service not available for data analysis")
            return {
                'success': False,
                'error': 'GitHub service not configured'
            }
        
        # 3. ANALYZE EACH DATA TYPE
        all_metrics = {}
        all_trends = {}
        all_insights = []
        
        for dt in data_types:
            if dt == 'repository_metrics':
                metrics = await self._analyze_repository_metrics(
                    github_service, repository, since, until
                )
                all_metrics.update(metrics)
                
            elif dt == 'commit_stats':
                metrics = await self._analyze_commit_stats(
                    github_service, repository, since, until
                )
                all_metrics.update(metrics)
                
            elif dt == 'issue_stats':
                metrics = await self._analyze_issue_stats(
                    github_service, repository, since, until
                )
                all_metrics.update(metrics)
                
            else:
                logger.warning(f"Unsupported data type: {dt}")
                all_insights.append(f"Data type '{dt}' is not yet supported")
        
        # 4. GENERATE INSIGHTS (if we have metrics)
        if all_metrics:
            insights = self._generate_insights(all_metrics, since, until)
            all_insights.extend(insights)
        
        # 5. RETURN COMPREHENSIVE RESULTS
        logger.info(f"Analyzed {len(data_types)} data types with {len(all_metrics)} metrics")
        return {
            'success': True,
            'data_types': data_types,
            'analysis_period': {
                'since': since.isoformat() if since else None,
                'until': until.isoformat() if until else None
            },
            'metrics': all_metrics,
            'trends': all_trends if all_trends else None,
            'insights': all_insights if all_insights else None,
            'metric_count': len(all_metrics)
        }
        
    except Exception as e:
        # 6. HANDLE ERRORS
        logger.error(f"Failed to analyze data: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to analyze data: {str(e)}'
        }
```

#### Step 4.2: Implement Helper Methods

**Be thorough - these do the actual analysis work**:

```python
async def _analyze_repository_metrics(
    self,
    github_service,
    repository: str,
    since: datetime,
    until: datetime
) -> Dict[str, Any]:
    """Analyze repository-level metrics
    
    Returns metrics like:
        - Issue counts (total, open, closed)
        - PR counts (total, merged, pending)
        - Contributor count
        - Star/fork growth
    """
    # Implementation here - be thorough
    # Use existing service methods
    # Calculate meaningful metrics
    pass

async def _analyze_commit_stats(
    self,
    github_service,
    repository: str,
    since: datetime,
    until: datetime
) -> Dict[str, Any]:
    """Analyze commit statistics
    
    Returns metrics like:
        - Commit frequency
        - Active contributors
        - Code churn
        - Commit patterns by day/time
    """
    # Can leverage get_recent_activity from Phase 2
    pass

async def _analyze_issue_stats(
    self,
    github_service,
    repository: str,
    since: datetime,
    until: datetime
) -> Dict[str, Any]:
    """Analyze issue statistics
    
    Returns metrics like:
        - Creation rate
        - Resolution rate
        - Average time to close
        - Label distribution
    """
    # Implementation here
    pass

def _generate_insights(
    self,
    metrics: Dict[str, Any],
    since: datetime,
    until: datetime
) -> List[str]:
    """Generate human-readable insights from metrics
    
    Looks for:
        - Significant changes
        - Trends
        - Anomalies
        - Comparisons to baselines
    """
    insights = []
    
    # Example insight generation
    if 'commit_count' in metrics:
        count = metrics['commit_count']
        days = (until - since).days if until else 7
        avg_per_day = count / days if days > 0 else 0
        insights.append(f"Average of {avg_per_day:.1f} commits per day")
    
    # Add more insight logic
    
    return insights
```

**Implementation Quality Checklist**:
- [ ] All validation thorough (not just happy path)
- [ ] Error messages helpful and specific
- [ ] Logging comprehensive (info, warning, error levels)
- [ ] Edge cases handled (no data, invalid params, service failures)
- [ ] Response structure consistent with Phase 2/2B
- [ ] Helper methods are focused and testable
- [ ] Code is readable and well-commented
- [ ] No placeholder markers remain

---

### Part 5: Run Tests Thoroughly (30 min)

**Don't rush testing - verify quality**

#### Step 5.1: Unit Test Pass

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestHandleAnalyzeData -v -s

# Verify:
# - All tests pass ✅
# - No unexpected warnings
# - Log output looks correct
# - Error messages are helpful
```

#### Step 5.2: Integration Test Pass

```bash
pytest tests/intent/test_execution_analysis_handlers.py::TestHandleAnalyzeData::test_handle_analyze_data_real_analysis -v -s --log-cli-level=INFO

# Review:
# - Real data is analyzed
# - Metrics are meaningful
# - Response structure is correct
# - No placeholder artifacts
```

#### Step 5.3: Manual Testing

```bash
# Start Piper Morgan
python main.py

# Test various scenarios manually
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "analyze repository metrics for piper-morgan"}'

# Verify in logs:
# - Real API calls made
# - Data fetched and analyzed
# - Meaningful results returned
# - No errors or warnings
```

**Test multiple scenarios**:
1. Valid request with all parameters
2. Minimal request (only required params)
3. Invalid data_type
4. Missing required parameters
5. Repository that doesn't exist

**Document all test results** - thoroughness matters

---

### Part 6: Comprehensive Evidence Collection (30 min)

**Create thorough documentation of implementation**

#### Required Deliverables

**1. Test Results** (`dev/2025/10/11/phase2c-test-results.txt`)
- Full pytest output
- All tests passing
- Log output from integration test
- Manual test results

**2. Implementation Analysis** (`dev/2025/10/11/phase2c-implementation-analysis.md`)
```markdown
# Phase 2C Implementation Analysis

## Data Types Supported
[List all supported data types with descriptions]

## Analysis Capabilities
[Describe what analyses are performed]

## Helper Methods
[Document each helper method and its purpose]

## Edge Cases Handled
[List all edge cases and how they're handled]

## Quality Verification
- [ ] All validation comprehensive
- [ ] Error messages helpful
- [ ] Logging appropriate
- [ ] No placeholder markers
- [ ] Pattern consistent with Phase 2/2B
- [ ] Tests comprehensive
- [ ] Documentation complete
```

**3. Sample Analysis Output** (`dev/2025/10/11/phase2c-sample-analysis.json`)
- Save actual output from integration test
- Show real metrics, trends, insights
- Demonstrate quality of analysis

**4. Pattern Comparison** (`dev/2025/10/11/phase2c-pattern-verification.md`)
- Compare with Phase 2 and 2B implementations
- Verify pattern consistency
- Document any necessary deviations

**5. ANALYSIS Category Completion Report** (`dev/2025/10/11/analysis-category-complete.md`)
```markdown
# ANALYSIS Category Completion Report

## Status: 3/3 Handlers Complete (100%) ✅

### Implemented Handlers
1. ✅ _handle_analyze_commits (Phase 2)
2. ✅ _handle_generate_report (Phase 2B)  
3. ✅ _handle_analyze_data (Phase 2C)

### Quality Metrics
- Test coverage: [X%]
- Pattern consistency: [100%]
- Documentation: [Complete/Incomplete]
- Evidence: [Complete/Incomplete]

### Category Characteristics
[Describe what makes ANALYSIS category distinct]

### Lessons Learned
[Key insights from implementing ANALYSIS handlers]

### Ready for Next Category
[Verification that pattern can be applied to SYNTHESIS]
```

---

## Phase 2C Completion Criteria

**Do not mark complete until ALL criteria met**:

- [ ] Tests written and comprehensive (TDD red phase)
- [ ] Helper methods implemented and tested
- [ ] Implementation complete with thorough validation
- [ ] All tests passing (TDD green phase)
- [ ] Integration test shows real, meaningful analysis
- [ ] No placeholder responses anywhere
- [ ] Edge cases handled properly
- [ ] Error messages are helpful and specific
- [ ] Logging is comprehensive
- [ ] Evidence collected and documented
- [ ] Pattern consistency verified
- [ ] ANALYSIS category completion report created
- [ ] Quality review complete

---

## STOP Conditions

**STOP and report to PM if**:
- Requirements for "data analysis" are unclear
- No appropriate data sources available
- Analysis scope is too broad or undefined
- Service methods needed would take >1 hour to create
- Pattern doesn't apply well to data analysis
- Implementation reveals architectural issues
- Testing shows quality concerns
- **Any uncertainty about thoroughness or accuracy**

---

## Quality Reminders

**PM Priority**: Thoroughness and accuracy over speed

**This means**:
- Take time to understand requirements fully
- Don't skip validation or error handling
- Write comprehensive tests
- Document thoroughly
- Verify quality at each step
- If something seems rushed or incomplete, slow down
- Ask for clarification rather than making assumptions

**Speed is secondary to quality** - take 2-3 hours if needed for thoroughness

---

## Deliverables Checklist

- [ ] Updated `services/intent/intent_service.py` with full implementation
- [ ] Helper methods implemented and tested
- [ ] Comprehensive tests in `tests/intent/test_execution_analysis_handlers.py`
- [ ] `dev/2025/10/11/phase2c-test-results.txt`
- [ ] `dev/2025/10/11/phase2c-implementation-analysis.md`
- [ ] `dev/2025/10/11/phase2c-sample-analysis.json`
- [ ] `dev/2025/10/11/phase2c-pattern-verification.md`
- [ ] `dev/2025/10/11/analysis-category-complete.md`
- [ ] Session log updated

---

## After Phase 2C

**Report to PM**:
1. Implementation complete with comprehensive evidence
2. ANALYSIS category 100% complete (3/3 handlers)
3. Quality verification results
4. Thoroughness assessment
5. Ready for SYNTHESIS category (or need review)

**Do NOT proceed to SYNTHESIS without PM authorization**

---

## Progress Tracking

**Before Phase 2C**:
- GREAT-4D handlers: 4/10 complete (40%)
- ANALYSIS: 2/3 complete (67%)

**After Phase 2C**:
- GREAT-4D handlers: 5/10 complete (50%)
- ANALYSIS: 3/3 complete (100%) ✅

**Remaining**:
- SYNTHESIS: 2 handlers
- STRATEGY: 2 handlers
- LEARNING: 1 handler
- **Total**: 5 handlers remaining

---

*Phase 2C prompt created: October 11, 2025, 12:58 PM*  
*Agent: Code Agent*  
*Duration: 1-2 hours (take time needed for quality)*  
*Priority: Thoroughness and accuracy over speed*  
*Final ANALYSIS handler - completes category*
