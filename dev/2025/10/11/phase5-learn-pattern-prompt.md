# Phase 5: LEARNING Handler - _handle_learn_pattern (FINAL HANDLER!)

**Date**: October 11, 2025, 5:03 PM  
**Agent**: Code Agent  
**Duration**: Estimated 45-60 minutes  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 5 (LEARNING Handler - **FINAL HANDLER**)

---

## Mission

Implement `_handle_learn_pattern` handler with genuine pattern learning functionality, completing the LEARNING category and **achieving 100% GAP-1 completion**. This is the **FINAL handler** in the GREAT-4D implementation.

**Context**: Nine handlers complete across four categories (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY) with A+ quality. This final LEARNING handler completes the vision.

**PM Priority**: Thoroughness and accuracy over speed - finish strong!

**Progress**: 9/10 handlers complete (90%), this achieves 100% completion! 🎯

---

## Success Criteria

- [ ] `_handle_learn_pattern` learns and recognizes patterns (not placeholder)
- [ ] Patterns are actually identified and stored
- [ ] Tests demonstrate actual learning functionality
- [ ] Pattern follows established approach
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual pattern learning with examples
- [ ] Quality maintained at A+ level
- [ ] **GAP-1 COMPLETE** - All 10 handlers implemented! 🎉

---

## Understanding LEARNING vs Previous Categories

**Critical Distinctions**:

**EXECUTION** (complete):
- **Does**: Creates/updates resources now
- **Example**: Create issue, update issue

**ANALYSIS** (complete):
- **Reads**: Past data and analyzes
- **Example**: Analyze commits, generate report

**SYNTHESIS** (complete):
- **Creates**: New content/documents
- **Example**: Generate content, summarize

**STRATEGY** (complete):
- **Plans**: Future actions and decisions
- **Example**: Strategic planning, prioritization

**LEARNING** (final):
- **Learns**: From patterns and experience
- **Adapts**: Improves over time
- **Recognizes**: Recurring patterns
- **Example**: Learn from past issues, recognize similar patterns

**Key Difference**: LEARNING looks across time to identify patterns and improve

---

## Phase 5 Structure

### Part 1: Study Pattern Learning Requirements (15 min)

#### Step 1.1: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_learn_pattern` (line 924 per original reconciliation, may have shifted significantly)

**Use Serena to find current location**:
```
Search for _handle_learn_pattern in services/intent/intent_service.py
```

**Current placeholder** (approximately):
```python
async def _handle_learn_pattern(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle LEARN_PATTERN intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Pattern learning handler ready. Implementation in progress.'
    }
```

**Critical Questions**:
1. What patterns can be learned?
   - Issue patterns (common bugs, resolutions)?
   - Code patterns (common approaches)?
   - Workflow patterns (successful processes)?
   - User patterns (common questions)?

2. What inputs are needed?
   - Pattern source (past issues, commits, interactions)?
   - Pattern type (what to learn)?
   - Time range (how far back)?
   - Minimum occurrences (threshold)?

3. How are patterns learned?
   - Similarity detection (text/semantic)?
   - Frequency analysis?
   - Template extraction?
   - Classification?

4. What should the output contain?
   - Identified patterns
   - Pattern frequency/confidence
   - Examples of pattern
   - Recommendations based on pattern

**STOP if requirements are unclear** - Report to PM for clarification

#### Step 1.2: Determine Learning Approach

**Consider approaches**:

**Option 1: Issue Pattern Learning** (Recommended)
- Input: Past GitHub issues
- Method: Identify similar issues, extract common patterns
- Output: Pattern definitions with examples
- Use case: "Learn from past authentication bugs"

**Option 2: Resolution Pattern Learning**
- Input: Resolved issues with solutions
- Method: Map problem types to solution approaches
- Output: Problem-solution pattern library
- Use case: "What's the typical fix for database errors?"

**Option 3: Workflow Pattern Learning**
- Input: Successful project histories
- Method: Extract common successful workflows
- Output: Best practice patterns
- Use case: "Learn from successful feature launches"

**Recommended**: Start with **Issue Pattern Learning** (practical, demonstrable)

---

### Part 2: Define Learning Strategy (20 min)

#### Step 2.1: Choose Pattern Learning Types

**Recommended types** (choose 2-3):

1. **Issue Patterns** (Similar issue identification)
   - Input: Issue description or keywords
   - Method: Find similar past issues
   - Output: Pattern with similar issues and common themes

2. **Resolution Patterns** (Solution patterns)
   - Input: Problem description
   - Method: Find similar problems and their solutions
   - Output: Common resolution approaches

3. **Tag/Label Patterns** (Classification patterns)
   - Input: Issue content
   - Method: Learn common tag patterns
   - Output: Suggested tags based on pattern

#### Step 2.2: Design Pattern Learning Approach

```markdown
## Learning Type: Issue Pattern Learning

### Input Parameters
- pattern_type: "issue_similarity"
- source: "github_issues"
- query: [description of what to learn]
- timeframe: [how far back to look] (optional)
- min_occurrences: [minimum pattern frequency] (optional, default: 2)

### Learning Method
1. Fetch relevant historical data (past issues)
2. Extract features (keywords, labels, structure)
3. Find similarities (text similarity, semantic similarity)
4. Group similar items (clustering)
5. Identify patterns (common themes, approaches)
6. Calculate confidence (based on frequency)

### Output Structure
```python
{
    'success': True,
    'pattern_type': 'issue_similarity',
    'patterns_found': [
        {
            'pattern_id': 'auth_timeout_issues',
            'description': 'Authentication timeout errors',
            'confidence': 0.85,
            'occurrences': 12,
            'common_themes': [
                'Session timeout',
                'Token expiration',
                'Network latency'
            ],
            'examples': [
                {'issue': '#123', 'title': 'User logged out unexpectedly'},
                {'issue': '#145', 'title': 'Session timeout too short'},
                # ... more examples
            ],
            'recommended_actions': [
                'Check session configuration',
                'Review token expiration settings',
                'Add token refresh mechanism'
            ]
        },
        # ... more patterns
    ],
    'total_items_analyzed': 150,
    'patterns_count': 3
}
```

### Quality Checks
- [ ] Pattern has multiple examples (not singleton)
- [ ] Confidence score is reasonable
- [ ] Common themes are meaningful
- [ ] Recommendations are actionable
```

---

### Part 3: Write Comprehensive Tests (TDD) (20 min)

**File**: `tests/intent/test_learning_handlers.py` (NEW FILE)

```python
import pytest
from datetime import datetime, timedelta
from services.intent.intent_service import IntentService

class TestHandleLearnPattern:
    """Comprehensive tests for _handle_learn_pattern handler
    
    LEARNING handlers identify patterns from historical data
    to improve future decision-making and recognize similarities.
    """
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService"""
        service = IntentService()
        return service
    
    @pytest.mark.asyncio
    async def test_learn_pattern_handler_exists(self, intent_service):
        """Verify handler exists and is not placeholder"""
        result = await intent_service._handle_learn_pattern(
            query="learn from authentication issues",
            params={
                'pattern_type': 'issue_similarity',
                'source': 'github_issues',
                'query': 'authentication errors'
            }
        )
        
        assert 'requires_clarification' not in result or result.get('requires_clarification') is False
    
    @pytest.mark.asyncio
    async def test_learn_pattern_missing_type(self, intent_service):
        """Test error when pattern_type missing"""
        result = await intent_service._handle_learn_pattern(
            query="learn from issues",
            params={'source': 'github_issues'}
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'pattern_type' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_learn_pattern_missing_source(self, intent_service):
        """Test error when source missing"""
        result = await intent_service._handle_learn_pattern(
            query="learn patterns",
            params={'pattern_type': 'issue_similarity'}
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'source' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_learn_pattern_unknown_type(self, intent_service):
        """Test error for unsupported pattern type"""
        result = await intent_service._handle_learn_pattern(
            query="learn quantum patterns",
            params={
                'pattern_type': 'quantum_entanglement',
                'source': 'github_issues'
            }
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'unsupported' in result['error'].lower() or 'not supported' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_learn_pattern_issue_similarity_success(self, intent_service):
        """Test successful issue pattern learning"""
        result = await intent_service._handle_learn_pattern(
            query="learn from authentication issues",
            params={
                'pattern_type': 'issue_similarity',
                'source': 'github_issues',
                'query': 'authentication',
                'timeframe': '6_months'
            }
        )
        
        assert result['success'] is True
        assert 'patterns_found' in result
        
        # Should find at least some patterns (or indicate none found)
        patterns = result['patterns_found']
        assert isinstance(patterns, list)
        
        # If patterns found, verify structure
        if len(patterns) > 0:
            pattern = patterns[0]
            assert 'pattern_id' in pattern or 'description' in pattern
            assert 'confidence' in pattern or 'occurrences' in pattern
    
    @pytest.mark.asyncio
    async def test_learn_pattern_with_examples(self, intent_service):
        """Test that patterns include examples"""
        result = await intent_service._handle_learn_pattern(
            query="learn bug patterns",
            params={
                'pattern_type': 'issue_similarity',
                'source': 'github_issues',
                'query': 'bug'
            }
        )
        
        assert result['success'] is True
        
        if result.get('patterns_found') and len(result['patterns_found']) > 0:
            pattern = result['patterns_found'][0]
            # Should have examples or at least metadata
            assert 'examples' in pattern or 'occurrences' in pattern
    
    @pytest.mark.asyncio
    async def test_learn_pattern_no_placeholder(self, intent_service):
        """Verify no placeholder response"""
        result = await intent_service._handle_learn_pattern(
            query="learn from issues",
            params={
                'pattern_type': 'issue_similarity',
                'source': 'github_issues',
                'query': 'test'
            }
        )
        
        # Should not have requires_clarification as True
        assert result.get('requires_clarification') is not True
        
        # Should have either success or error
        assert 'success' in result
```

**Run tests - verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_learning_handlers.py::TestHandleLearnPattern -v
```

---

### Part 4: Implement Handler (30-40 min)

**File**: `services/intent/intent_service.py`

```python
async def _handle_learn_pattern(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle LEARN_PATTERN intent - FULLY IMPLEMENTED
    
    Learns patterns from historical data to identify recurring themes,
    similar issues, and common approaches. Helps recognize patterns
    and improve future decision-making.
    
    Supported pattern_types:
        - 'issue_similarity': Find similar issues and common patterns
        - 'resolution_patterns': Learn solution approaches for problems
        - 'tag_patterns': Learn tag/classification patterns
    
    Args:
        query: Natural language query describing what to learn
        params: Dictionary containing:
            - pattern_type (required): Type of pattern to learn
            - source (required): Data source (github_issues, commits, etc.)
            - query (optional): Specific query/keywords for pattern learning
            - timeframe (optional): How far back to analyze
            - min_occurrences (optional): Minimum pattern frequency
    
    Returns:
        Dictionary containing:
            - success: Boolean
            - pattern_type: Type of pattern learned
            - patterns_found: List of identified patterns
            - total_items_analyzed: Number of items analyzed
            - patterns_count: Number of patterns identified
            - error: Error message (if failed)
    """
    try:
        # 1. VALIDATION
        pattern_type = params.get('pattern_type')
        if not pattern_type:
            logger.warning("Pattern type missing for learning")
            return {
                'success': False,
                'error': 'pattern_type parameter is required. Supported: issue_similarity, resolution_patterns, tag_patterns'
            }
        
        source = params.get('source')
        if not source:
            logger.warning("Source missing for pattern learning")
            return {
                'success': False,
                'error': 'source parameter is required (e.g., github_issues)'
            }
        
        # Normalize
        pattern_type = pattern_type.lower().strip()
        source = source.lower().strip()
        
        # Validate type
        supported_types = ['issue_similarity', 'resolution_patterns', 'tag_patterns']
        if pattern_type not in supported_types:
            return {
                'success': False,
                'error': f'Unsupported pattern_type "{pattern_type}". Supported: {", ".join(supported_types)}'
            }
        
        # Get optional parameters
        search_query = params.get('query', '')
        timeframe = params.get('timeframe', '6_months')
        min_occurrences = params.get('min_occurrences', 2)
        
        # 2. FETCH HISTORICAL DATA
        historical_data = await self._fetch_learning_data(
            source, search_query, timeframe
        )
        
        if not historical_data or len(historical_data) == 0:
            logger.info(f"No historical data found for pattern learning: {search_query}")
            return {
                'success': True,
                'pattern_type': pattern_type,
                'patterns_found': [],
                'total_items_analyzed': 0,
                'patterns_count': 0,
                'message': 'No historical data available for pattern learning'
            }
        
        # 3. LEARN PATTERNS based on type
        if pattern_type == 'issue_similarity':
            patterns = self._learn_issue_similarity_patterns(
                historical_data, search_query, min_occurrences
            )
        elif pattern_type == 'resolution_patterns':
            patterns = self._learn_resolution_patterns(
                historical_data, min_occurrences
            )
        elif pattern_type == 'tag_patterns':
            patterns = self._learn_tag_patterns(
                historical_data, min_occurrences
            )
        else:
            raise ValueError(f"Unhandled pattern type: {pattern_type}")
        
        # 4. RETURN SUCCESS
        logger.info(
            f"Learned {len(patterns)} patterns from {len(historical_data)} items"
        )
        return {
            'success': True,
            'pattern_type': pattern_type,
            'patterns_found': patterns,
            'total_items_analyzed': len(historical_data),
            'patterns_count': len(patterns)
        }
        
    except Exception as e:
        logger.error(f"Failed to learn pattern: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to learn pattern: {str(e)}'
        }
```

**Helper 1: Fetch learning data**
```python
async def _fetch_learning_data(
    self,
    source: str,
    search_query: str,
    timeframe: str
) -> List[Dict[str, Any]]:
    """Fetch historical data for pattern learning"""
    
    if source == 'github_issues':
        # Use existing analyze_commits infrastructure from Phase 2
        # Or fetch issues directly via GitHub service
        github_service = self.service_registry.get('github')
        if not github_service:
            logger.warning("GitHub service not available for pattern learning")
            return []
        
        try:
            # Fetch recent issues
            # This is simplified - in production might use search/query
            issues = await github_service.list_issues(
                repository='piper-morgan',
                state='all',
                limit=100
            )
            
            # Filter by query if provided
            if search_query:
                query_lower = search_query.lower()
                issues = [
                    issue for issue in issues
                    if query_lower in (issue.title or '').lower()
                    or query_lower in (issue.body or '').lower()
                ]
            
            return [
                {
                    'number': issue.number,
                    'title': issue.title,
                    'body': issue.body,
                    'labels': [label.name for label in (issue.labels or [])],
                    'state': issue.state
                }
                for issue in issues
            ]
            
        except Exception as e:
            logger.error(f"Failed to fetch GitHub issues: {e}")
            return []
    
    return []
```

**Helper 2: Learn issue similarity patterns**
```python
def _learn_issue_similarity_patterns(
    self,
    historical_data: List[Dict[str, Any]],
    search_query: str,
    min_occurrences: int
) -> List[Dict[str, Any]]:
    """Learn patterns from similar issues"""
    
    if len(historical_data) < min_occurrences:
        return []
    
    # Group issues by similarity (simplified - in production use NLP)
    # For now, group by common keywords in titles
    
    patterns = []
    
    # Extract common keywords
    keyword_groups = {}
    
    for item in historical_data:
        title = item.get('title', '').lower()
        words = title.split()
        
        # Find significant words (not common stop words)
        stop_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        
        for keyword in keywords:
            keyword_groups.setdefault(keyword, []).append(item)
    
    # Create patterns from groups with enough occurrences
    for keyword, items in keyword_groups.items():
        if len(items) >= min_occurrences:
            # Extract common labels
            all_labels = []
            for item in items:
                all_labels.extend(item.get('labels', []))
            
            label_counts = {}
            for label in all_labels:
                label_counts[label] = label_counts.get(label, 0) + 1
            
            common_labels = [
                label for label, count in label_counts.items()
                if count >= len(items) * 0.3  # In 30%+ of items
            ]
            
            patterns.append({
                'pattern_id': f"keyword_{keyword}",
                'description': f"Issues related to '{keyword}'",
                'keyword': keyword,
                'confidence': min(len(items) / 10, 1.0),  # Scale to 1.0
                'occurrences': len(items),
                'common_labels': common_labels,
                'examples': [
                    {'number': item['number'], 'title': item['title']}
                    for item in items[:5]  # First 5 examples
                ],
                'recommended_actions': [
                    f"Review similar past issues with '{keyword}'",
                    f"Consider common labels: {', '.join(common_labels)}" if common_labels else "No common labels found"
                ]
            })
    
    # Sort by occurrences
    patterns.sort(key=lambda x: x['occurrences'], reverse=True)
    
    return patterns[:10]  # Top 10 patterns
```

**Helper 3: Generate pattern ID**
```python
def _generate_pattern_id(self, description: str) -> str:
    """Generate unique pattern ID from description"""
    import hashlib
    
    # Create short hash
    desc_hash = hashlib.md5(description.encode()).hexdigest()[:8]
    
    # Create readable ID
    words = description.lower().split()[:3]
    readable = '_'.join(words)
    
    return f"{readable}_{desc_hash}"
```

---

### Part 5: Run Tests (10 min)

```bash
pytest tests/intent/test_learning_handlers.py::TestHandleLearnPattern -v -s

# All tests should pass
# Verify pattern learning actually works with real data
```

---

### Part 6: Evidence Collection & GAP-1 COMPLETION (15 min)

**Create Final Documentation**:

1. **Phase 5 Completion**:
   - `dev/2025/10/11/phase5-test-results.txt`
   - `dev/2025/10/11/phase5-sample-patterns.md`
   - `dev/2025/10/11/phase5-completion-report.md`

2. **LEARNING Category Complete**:
   - `dev/2025/10/11/LEARNING-category-complete.md`

3. **GAP-1 COMPLETE**:
   - `dev/2025/10/11/GAP-1-COMPLETE.md` 🎉
   - Summary of all 10 handlers
   - Overall statistics
   - Quality verification
   - Next steps

**GAP-1 Completion Template**:
```markdown
# GAP-1 COMPLETE - All 10 GREAT-4D Handlers Implemented! 🎉

**Date**: October 11, 2025
**Status**: ✅ 100% COMPLETE
**Duration**: [X hours] over 1 day

## Achievement Summary

**10/10 handlers implemented** (100%)

### EXECUTION (2/2) ✅
1. _handle_create_issue - Already working
2. _handle_update_issue - Phase 1

### ANALYSIS (3/3) ✅
1. _handle_analyze_commits - Phase 2
2. _handle_generate_report - Phase 2B
3. _handle_analyze_data - Phase 2C

### SYNTHESIS (2/2) ✅
1. _handle_generate_content - Phase 3
2. _handle_summarize - Phase 3B

### STRATEGY (2/2) ✅
1. _handle_strategic_planning - Phase 4
2. _handle_prioritization - Phase 4B

### LEARNING (1/1) ✅
1. _handle_learn_pattern - Phase 5

## Quality Metrics

- **Total Tests**: [X] tests across all handlers
- **Test Pass Rate**: 100%
- **Quality Gate Rating**: A+
- **Zero Placeholders**: All sophisticated placeholders eliminated
- **Documentation**: [Y] comprehensive documents

## Statistics

- **Total Lines of Code**: ~[X] lines
- **Helper Methods**: ~[Y] methods
- **Test Coverage**: Comprehensive
- **Categories Complete**: 5/5 (100%)

## What This Enables

With all 10 GREAT-4D handlers complete, Piper Morgan can now:
- Execute actions (create/update resources)
- Analyze data (commits, patterns, metrics)
- Synthesize content (generate, summarize)
- Plan strategy (roadmaps, priorities)
- Learn patterns (recognize, improve)

## Next Steps

1. Integration testing across all handlers
2. Deploy to staging
3. User acceptance testing
4. Production deployment
5. Monitor and iterate

---

*GAP-1 completed: [DATE]*
*All 10 handlers production-ready!* 🎉
```

---

## Completion Criteria

- [ ] Tests passing (7+ tests)
- [ ] Real pattern learning working
- [ ] Patterns identified from data
- [ ] No placeholders
- [ ] Quality maintained
- [ ] Evidence collected
- [ ] LEARNING category 100% complete
- [ ] **GAP-1 100% COMPLETE** 🎉

---

## Victory Lap Checklist

After Phase 5 completes:

- [ ] All 10 handlers verified complete
- [ ] Run full test suite (all categories)
- [ ] Create GAP-1 completion document
- [ ] Commit all changes
- [ ] Update CORE-CRAFT-GAP issue on GitHub
- [ ] Celebrate! 🎉

---

*Phase 5 prompt created: October 11, 2025, 5:03 PM*  
*FINAL handler - achieves 100% GAP-1 completion*  
*The home stretch!* 🏁
