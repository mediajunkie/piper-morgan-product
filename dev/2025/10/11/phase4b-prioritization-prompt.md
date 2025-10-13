# Phase 4B: STRATEGY Handler - _handle_prioritization (Final STRATEGY Handler)

**Date**: October 11, 2025, 4:40 PM  
**Agent**: Code Agent  
**Duration**: Estimated 45-60 minutes  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 4 (STRATEGY Handlers - Final Handler)

---

## Mission

Implement `_handle_prioritization` handler with genuine prioritization functionality, completing the STRATEGY category. This is the **final STRATEGY handler** and will establish the pattern for ranking, ordering, and priority decisions.

**Context**: Phase 4 established STRATEGY pattern with planning. Now we apply that pattern to prioritization - helping users decide what's most important.

**PM Priority**: Thoroughness and accuracy over speed.

**Progress**: 8/10 handlers complete (80%), this completes STRATEGY at 90%

---

## Success Criteria

- [ ] `_handle_prioritization` creates real priority rankings (not placeholders)
- [ ] Items are actually prioritized with clear reasoning
- [ ] Tests demonstrate actual prioritization functionality
- [ ] Pattern follows Phase 4 STRATEGY approach
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual prioritization with examples
- [ ] Quality maintained at A+ level

---

## Understanding Prioritization vs Planning

**Phase 4 (_handle_strategic_planning)**:
- **Creates**: Multi-phase plans
- **Output**: Structured roadmaps with tasks
- **Focus**: How to execute

**Phase 4B (_handle_prioritization)**:
- **Ranks**: Items by importance/urgency
- **Output**: Ordered list with priority scores
- **Focus**: What to do first

**Both are STRATEGY** because they guide future decisions

---

## Phase 4B Structure

### Part 1: Study Prioritization Requirements (15 min)

#### Step 1.1: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_prioritization` (line 890 per original reconciliation, may have shifted after Phase 4)

**Use Serena to find current location**:
```
Search for _handle_prioritization in services/intent/intent_service.py
```

**Current placeholder** (approximately):
```python
async def _handle_prioritization(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle PRIORITIZATION intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Prioritization handler ready. Implementation in progress.'
    }
```

**Critical Questions**:
1. What can be prioritized?
   - Issues/tasks?
   - Features/requirements?
   - Pull requests for review?
   - Technical debt items?
   - Projects?

2. What inputs are needed?
   - Items to prioritize (required)
   - Prioritization criteria (urgency, impact, effort)?
   - Context (project goals, deadlines)?
   - Current priorities?

3. What prioritization methods?
   - Impact vs Effort matrix?
   - RICE framework (Reach, Impact, Confidence, Effort)?
   - MoSCoW (Must, Should, Could, Won't)?
   - Urgency/Importance (Eisenhower)?
   - Simple scoring?

4. What should the output contain?
   - Ranked list of items
   - Priority score/level for each
   - Reasoning for ranking
   - Recommendations

**STOP if requirements are unclear** - Report to PM for clarification

#### Step 1.2: Determine Prioritization Approach

**Consider approaches**:

**Option 1: Issue Prioritization** (Recommended)
- Input: List of GitHub issues
- Criteria: Impact, urgency, effort
- Output: Ranked issues with scores
- Method: Weighted scoring

**Option 2: Feature Prioritization**
- Input: Feature requests
- Criteria: RICE framework
- Output: Ranked features
- Method: RICE calculation

**Option 3: Task Prioritization**
- Input: Tasks/work items
- Criteria: Eisenhower matrix
- Output: Quadrant assignment + ranking
- Method: Urgency/Importance scoring

**Choose 2-3 prioritization types** that complement planning from Phase 4

---

### Part 2: Define Prioritization Strategy (20 min)

#### Step 2.1: Choose Supported Prioritization Types

**Recommended types**:

1. **Issue Prioritization** (GitHub issues)
   - Criteria: Impact (1-10), Urgency (1-10), Effort (1-10)
   - Scoring: `priority = (impact * urgency) / effort`
   - Output: Ranked issues with priority scores

2. **Feature Prioritization** (RICE)
   - Criteria: Reach, Impact, Confidence, Effort
   - Scoring: `RICE = (reach * impact * confidence) / effort`
   - Output: RICE scores and ranking

3. **Task Prioritization** (Eisenhower)
   - Criteria: Urgency (high/low), Importance (high/low)
   - Quadrants: Do First, Schedule, Delegate, Eliminate
   - Output: Quadrant assignment + action recommendations

#### Step 2.2: Design Prioritization Approach

**For each type**:

```markdown
## Prioritization Type: Issue Prioritization

### Input Parameters
- prioritization_type: "issues"
- items: [list of issue numbers or issue data]
- criteria: {
    'impact': 'weight' (default: 1.0),
    'urgency': 'weight' (default: 1.0),
    'effort': 'weight' (default: 1.0)
  }

### Scoring Method
For each issue:
1. Assess impact (1-10): How many users affected? How critical?
2. Assess urgency (1-10): How soon must this be addressed?
3. Assess effort (1-10): How complex to implement? (lower is easier)
4. Calculate: priority_score = (impact * urgency) / effort

### Output Structure
```python
{
    'success': True,
    'prioritization_type': 'issues',
    'prioritized_items': [
        {
            'rank': 1,
            'item': 'Issue #123: Critical bug in authentication',
            'priority_score': 45.0,
            'scores': {
                'impact': 9,
                'urgency': 10,
                'effort': 2
            },
            'reasoning': 'High impact and urgency, low effort - top priority'
        },
        # ... more items
    ],
    'recommendations': [
        'Focus on top 3 items first',
        'Re-evaluate priorities weekly'
    ]
}
```
```

---

### Part 3: Write Comprehensive Tests (TDD) (20 min)

**File**: `tests/intent/test_strategy_handlers.py` (add to existing)

```python
class TestHandlePrioritization:
    """Comprehensive tests for _handle_prioritization handler"""
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService"""
        service = IntentService()
        return service
    
    @pytest.mark.asyncio
    async def test_prioritization_handler_exists(self, intent_service):
        """Verify handler exists and is not placeholder"""
        result = await intent_service._handle_prioritization(
            query="prioritize these issues",
            params={
                'prioritization_type': 'issues',
                'items': ['Issue 1', 'Issue 2']
            }
        )
        
        assert 'requires_clarification' not in result or result.get('requires_clarification') is False
    
    @pytest.mark.asyncio
    async def test_prioritization_missing_type(self, intent_service):
        """Test error when prioritization_type missing"""
        result = await intent_service._handle_prioritization(
            query="prioritize",
            params={'items': ['Item 1']}
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'prioritization_type' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_prioritization_missing_items(self, intent_service):
        """Test error when items missing"""
        result = await intent_service._handle_prioritization(
            query="prioritize",
            params={'prioritization_type': 'issues'}
        )
        
        assert result['success'] is False
        assert 'error' in result
        assert 'items' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_prioritization_issues_success(self, intent_service):
        """Test successful issue prioritization"""
        items = [
            {'title': 'Critical bug', 'impact': 9, 'urgency': 10, 'effort': 2},
            {'title': 'Nice feature', 'impact': 5, 'urgency': 3, 'effort': 8},
            {'title': 'Important fix', 'impact': 8, 'urgency': 7, 'effort': 3}
        ]
        
        result = await intent_service._handle_prioritization(
            query="prioritize these issues",
            params={
                'prioritization_type': 'issues',
                'items': items
            }
        )
        
        assert result['success'] is True
        assert 'prioritized_items' in result
        
        prioritized = result['prioritized_items']
        assert len(prioritized) == 3
        
        # Verify ranking (first should be highest priority)
        assert prioritized[0]['rank'] == 1
        assert 'priority_score' in prioritized[0]
        
        # Verify scores are calculated
        assert 'scores' in prioritized[0]
    
    @pytest.mark.asyncio
    async def test_prioritization_ranking_order(self, intent_service):
        """Test that items are actually ranked by priority"""
        items = [
            {'title': 'Low priority', 'impact': 2, 'urgency': 2, 'effort': 8},
            {'title': 'High priority', 'impact': 10, 'urgency': 10, 'effort': 1},
            {'title': 'Medium priority', 'impact': 5, 'urgency': 5, 'effort': 5}
        ]
        
        result = await intent_service._handle_prioritization(
            query="prioritize",
            params={
                'prioritization_type': 'issues',
                'items': items
            }
        )
        
        assert result['success'] is True
        prioritized = result['prioritized_items']
        
        # High priority should be rank 1
        assert prioritized[0]['item']['title'] == 'High priority'
        assert prioritized[0]['rank'] == 1
        
        # Low priority should be last
        assert prioritized[-1]['item']['title'] == 'Low priority'
```

**Run tests - verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_strategy_handlers.py::TestHandlePrioritization -v
```

---

### Part 4: Implement Handler (30-40 min)

**File**: `services/intent/intent_service.py`

```python
async def _handle_prioritization(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle PRIORITIZATION intent - FULLY IMPLEMENTED
    
    Prioritizes items (issues, features, tasks) based on various criteria
    to help determine what should be worked on first.
    
    Supported prioritization_types:
        - 'issues': Prioritize GitHub issues by impact/urgency/effort
        - 'features': Prioritize features using RICE framework
        - 'tasks': Prioritize tasks using Eisenhower matrix
    
    Args:
        query: Natural language query describing prioritization request
        params: Dictionary containing:
            - prioritization_type (required): Type of prioritization
            - items (required): List of items to prioritize
            - criteria (optional): Custom criteria/weights
    
    Returns:
        Dictionary containing:
            - success: Boolean
            - prioritization_type: Type used
            - prioritized_items: Ranked list with scores
            - recommendations: Strategic recommendations
            - error: Error message (if failed)
    """
    try:
        # 1. VALIDATION
        prioritization_type = params.get('prioritization_type')
        if not prioritization_type:
            logger.warning("Prioritization type missing")
            return {
                'success': False,
                'error': 'prioritization_type parameter is required. Supported: issues, features, tasks'
            }
        
        items = params.get('items')
        if not items:
            logger.warning("Items missing for prioritization")
            return {
                'success': False,
                'error': 'items parameter is required (list of items to prioritize)'
            }
        
        if not isinstance(items, list) or len(items) == 0:
            return {
                'success': False,
                'error': 'items must be a non-empty list'
            }
        
        # Normalize type
        prioritization_type = prioritization_type.lower().strip()
        
        # Validate type
        supported_types = ['issues', 'features', 'tasks']
        if prioritization_type not in supported_types:
            return {
                'success': False,
                'error': f'Unsupported type "{prioritization_type}". Supported: {", ".join(supported_types)}'
            }
        
        criteria = params.get('criteria', {})
        
        # 2. PRIORITIZE based on type
        if prioritization_type == 'issues':
            prioritized = self._prioritize_issues(items, criteria)
        elif prioritization_type == 'features':
            prioritized = self._prioritize_features_rice(items, criteria)
        elif prioritization_type == 'tasks':
            prioritized = self._prioritize_tasks_eisenhower(items, criteria)
        else:
            raise ValueError(f"Unhandled type: {prioritization_type}")
        
        # 3. GENERATE RECOMMENDATIONS
        recommendations = self._generate_prioritization_recommendations(
            prioritized, prioritization_type
        )
        
        # 4. RETURN SUCCESS
        logger.info(f"Successfully prioritized {len(items)} {prioritization_type}")
        return {
            'success': True,
            'prioritization_type': prioritization_type,
            'total_items': len(items),
            'prioritized_items': prioritized,
            'recommendations': recommendations
        }
        
    except Exception as e:
        logger.error(f"Failed to prioritize: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to prioritize: {str(e)}'
        }
```

**Helper 1: Issue prioritization**
```python
def _prioritize_issues(
    self,
    items: List[Dict[str, Any]],
    criteria: Dict[str, float]
) -> List[Dict[str, Any]]:
    """Prioritize issues by impact/urgency/effort"""
    
    # Default weights
    impact_weight = criteria.get('impact', 1.0)
    urgency_weight = criteria.get('urgency', 1.0)
    effort_weight = criteria.get('effort', 1.0)
    
    scored_items = []
    
    for item in items:
        # Extract or estimate scores
        if isinstance(item, dict):
            title = item.get('title', item.get('name', str(item)))
            impact = item.get('impact', 5)  # Default mid-range
            urgency = item.get('urgency', 5)
            effort = item.get('effort', 5)
        else:
            title = str(item)
            # Estimate from title keywords
            impact = self._estimate_impact_from_title(title)
            urgency = self._estimate_urgency_from_title(title)
            effort = self._estimate_effort_from_title(title)
        
        # Calculate priority score
        # Higher score = higher priority
        # Formula: (impact * urgency) / effort
        priority_score = (
            (impact * impact_weight) * (urgency * urgency_weight)
        ) / max(effort * effort_weight, 1)  # Avoid division by zero
        
        scored_items.append({
            'item': item,
            'priority_score': round(priority_score, 2),
            'scores': {
                'impact': impact,
                'urgency': urgency,
                'effort': effort
            },
            'reasoning': self._generate_priority_reasoning(
                impact, urgency, effort, priority_score
            )
        })
    
    # Sort by priority score (descending)
    scored_items.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Add ranks
    for rank, item in enumerate(scored_items, 1):
        item['rank'] = rank
    
    return scored_items

def _estimate_impact_from_title(self, title: str) -> int:
    """Estimate impact from title keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['critical', 'security', 'crash', 'data loss']):
        return 10
    elif any(word in title_lower for word in ['important', 'bug', 'error', 'broken']):
        return 8
    elif any(word in title_lower for word in ['feature', 'enhancement', 'improve']):
        return 6
    else:
        return 5  # Default

def _estimate_urgency_from_title(self, title: str) -> int:
    """Estimate urgency from title keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['urgent', 'asap', 'blocking', 'critical']):
        return 10
    elif any(word in title_lower for word in ['soon', 'high priority']):
        return 8
    elif any(word in title_lower for word in ['when possible', 'nice to have']):
        return 3
    else:
        return 5  # Default

def _estimate_effort_from_title(self, title: str) -> int:
    """Estimate effort from title keywords"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['refactor', 'rewrite', 'major']):
        return 9
    elif any(word in title_lower for word in ['complex', 'difficult']):
        return 7
    elif any(word in title_lower for word in ['quick', 'simple', 'typo', 'minor']):
        return 2
    else:
        return 5  # Default

def _generate_priority_reasoning(
    self,
    impact: int,
    urgency: int,
    effort: int,
    priority_score: float
) -> str:
    """Generate human-readable reasoning for priority"""
    
    impact_level = 'high' if impact >= 7 else 'medium' if impact >= 4 else 'low'
    urgency_level = 'high' if urgency >= 7 else 'medium' if urgency >= 4 else 'low'
    effort_level = 'high' if effort >= 7 else 'medium' if effort >= 4 else 'low'
    
    return f"{impact_level.capitalize()} impact, {urgency_level} urgency, {effort_level} effort"
```

**Helper 2: Recommendations**
```python
def _generate_prioritization_recommendations(
    self,
    prioritized_items: List[Dict[str, Any]],
    prioritization_type: str
) -> List[str]:
    """Generate recommendations based on prioritization"""
    
    recommendations = []
    
    if not prioritized_items:
        return ['No items to prioritize']
    
    # Top item recommendation
    top_item = prioritized_items[0]
    recommendations.append(
        f"Start with rank #1: highest priority item"
    )
    
    # Quick wins
    if prioritization_type == 'issues':
        quick_wins = [
            item for item in prioritized_items
            if item['scores']['effort'] <= 3 and item['priority_score'] > 10
        ]
        if quick_wins:
            recommendations.append(
                f"Consider {len(quick_wins)} quick win(s) with high impact and low effort"
            )
    
    # Focus recommendations
    if len(prioritized_items) > 5:
        recommendations.append(
            "Focus on top 3-5 items to maintain momentum"
        )
    
    # Re-evaluation
    recommendations.append(
        "Re-evaluate priorities weekly as context changes"
    )
    
    return recommendations
```

---

### Part 5: Run Tests (10 min)

```bash
pytest tests/intent/test_strategy_handlers.py::TestHandlePrioritization -v -s
# All tests should pass
```

---

### Part 6: Evidence Collection (10 min)

**Create**:
1. `dev/2025/10/11/phase4b-test-results.txt`
2. `dev/2025/10/11/phase4b-sample-prioritizations.md`
3. `dev/2025/10/11/phase4b-completion-report.md`
4. `dev/2025/10/11/STRATEGY-category-complete.md`

---

## Completion Criteria

- [ ] Tests passing (6+ tests)
- [ ] Real prioritization working
- [ ] Items ranked correctly
- [ ] No placeholders
- [ ] Quality maintained
- [ ] Evidence collected
- [ ] STRATEGY category 100% complete

---

*Phase 4B prompt created: October 11, 2025, 4:40 PM*  
*Final STRATEGY handler - completes category*  
*Target: 90% total completion (9/10 handlers)*
