# Phase 4: STRATEGY Handler - _handle_strategic_planning

**Date**: October 11, 2025, 4:02 PM  
**Agent**: Code Agent  
**Duration**: Estimated 45-60 minutes  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 4 (STRATEGY Handlers - First Handler)

---

## Mission

Implement `_handle_strategic_planning` handler with genuine strategic planning functionality, establishing the STRATEGY category pattern. This is the **first STRATEGY handler** and will set the pattern for strategic operations.

**Context**: Three categories complete (EXECUTION, ANALYSIS, SYNTHESIS) with A+ quality gate rating. Now we establish the STRATEGY pattern, which focuses on planning, decision-making, and recommendations.

**PM Priority**: Thoroughness and accuracy over speed.

**Available Time**: 90 minutes total for both STRATEGY handlers

---

## Success Criteria

- [ ] `_handle_strategic_planning` creates real strategic plans (not placeholders)
- [ ] Plans are actually generated with actionable steps
- [ ] Tests demonstrate actual planning functionality
- [ ] Pattern follows established approach (validation, service, response, error handling)
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual strategic plans with examples
- [ ] Quality maintained at A+ level

---

## Understanding STRATEGY vs Previous Categories

**Critical Distinctions**:

**EXECUTION** (complete):
- **Does**: Creates/updates resources
- **Example**: Create GitHub issue, update issue

**ANALYSIS** (complete):
- **Reads**: Existing data
- **Analyzes**: Patterns, metrics, trends
- **Example**: Analyze commits, generate report

**SYNTHESIS** (complete):
- **Creates**: New content/documents
- **Example**: Generate content, summarize

**STRATEGY** (starting now):
- **Plans**: Future actions
- **Recommends**: Best courses of action
- **Decides**: Priorities and approaches
- **Example**: Create project plan, prioritize tasks

**Key Difference**: STRATEGY looks forward (planning), while ANALYSIS looks backward (understanding)

---

## Phase 4 Structure

### Part 1: Study Strategic Planning Requirements (15 min)

#### Step 1.1: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_strategic_planning` (line 856 per original reconciliation, may have shifted)

**Use Serena to find current location**:
```
Search for _handle_strategic_planning in services/intent/intent_service.py
```

**Current placeholder** (approximately):
```python
async def _handle_strategic_planning(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STRATEGIC_PLANNING intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': 'Strategic planning handler ready. Implementation in progress.'
    }
```

**Critical Questions**:
1. What can be planned strategically?
   - Project roadmaps?
   - Sprint/iteration planning?
   - Feature development plans?
   - Issue resolution strategies?
   - Resource allocation?

2. What inputs are needed?
   - Goal/objective (required)
   - Timeframe (sprint, quarter, year)?
   - Resources available?
   - Constraints?
   - Current state/context?

3. What should the plan contain?
   - Goals and objectives
   - Action items/steps
   - Timeline/milestones
   - Dependencies
   - Success criteria
   - Risk assessment?

4. How is the plan generated?
   - Template-based (for common plans)?
   - LLM-based (for custom strategic thinking)?
   - Data-driven (using ANALYSIS results)?
   - Combination?

**STOP if requirements are unclear** - Report to PM for clarification

#### Step 1.2: Review Available Infrastructure

**Check for existing planning capabilities**:

```bash
# Search for planning utilities
grep -r "plan\|strategy\|roadmap" services/ --include="*.py" | grep -i "def\|class"

# Check for LLM integration (for strategic thinking)
# We know TextAnalyzer exists from Phase 3B - can it help here?

# Check for project management integrations
find services/integrations -name "*project*" -o -name "*plan*"
```

**Determine approach**:
- Can we leverage LLM for strategic thinking (like summarization)?
- Do we need templates for common planning scenarios?
- Can we use ANALYSIS data (Phase 2C) to inform plans?

---

### Part 2: Define Planning Types and Strategy (20 min)

#### Step 2.1: Choose Supported Planning Types

**Start with 2-3 plan types that are**:
- Useful for PM/development teams
- Implementable with available tools
- Good examples of STRATEGY category

**Example planning types** (choose 2-3):

1. **Sprint Planning**
   - Input: Issues, velocity, sprint duration
   - Output: Sprint plan with prioritized issues
   - Method: Analyze backlog + recommend priorities

2. **Feature Roadmap**
   - Input: Feature requests, dependencies, timeline
   - Output: Phased feature roadmap
   - Method: Dependency analysis + timeline mapping

3. **Issue Resolution Strategy**
   - Input: Issue details, similar past issues
   - Output: Step-by-step resolution approach
   - Method: Pattern matching + best practices

4. **Project Kickoff Plan**
   - Input: Project goals, constraints, team size
   - Output: Initial project plan with phases
   - Method: Template + customization

5. **Technical Debt Strategy**
   - Input: Code analysis, priorities
   - Output: Debt reduction plan
   - Method: Risk assessment + prioritization

**Choose 2-3 types** that are practical and demonstrable

#### Step 2.2: Design Strategic Planning Approach

**For each chosen type, define**:

```markdown
## Plan Type: [Name]

### Input Parameters
- planning_type: "[type_name]"
- goal: [description of goal]
- timeframe: [duration/deadline]
- context: [optional context/constraints]
- [other type-specific params]

### Planning Method
- [ ] Template-based (structured plan format)
- [ ] LLM-assisted (strategic thinking/recommendations)
- [ ] Data-driven (uses ANALYSIS results)
- [ ] Combination

### Output Structure
```python
{
    'success': True,
    'planning_type': '[type_name]',
    'plan': {
        'goal': '[stated goal]',
        'timeframe': '[timeframe]',
        'phases': [
            {
                'phase': 1,
                'name': '[phase name]',
                'duration': '[duration]',
                'tasks': [
                    {'task': '[task description]', 'priority': 'high/medium/low'},
                    # ...
                ]
            },
            # ... more phases
        ],
        'milestones': [
            {'milestone': '[name]', 'target_date': '[date]'},
            # ...
        ],
        'dependencies': [
            {'task': '[task]', 'depends_on': '[other task]'},
            # ...
        ],
        'success_criteria': [
            '[criterion 1]',
            '[criterion 2]'
        ]
    },
    'recommendations': [
        '[recommendation 1]',
        '[recommendation 2]'
    ]
}
```

### Quality Checks
- [ ] Plan has actionable steps
- [ ] Steps are in logical order
- [ ] Timeframes are realistic
- [ ] Dependencies identified
- [ ] Success criteria clear
```

---

### Part 3: Write Comprehensive Tests (TDD) (20 min)

**File**: `tests/intent/test_strategy_handlers.py` (NEW FILE)

#### Step 3.1: Test Structure

```python
import pytest
from datetime import datetime, timedelta
from services.intent.intent_service import IntentService

class TestHandleStrategicPlanning:
    """Comprehensive tests for _handle_strategic_planning handler
    
    STRATEGY handlers create plans and recommendations for future actions.
    Tests verify that plans are actionable, realistic, and well-structured.
    """
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with required services"""
        service = IntentService()
        return service
```

#### Step 3.2: Write Thorough Unit Tests

**Test 1: Handler exists and is not placeholder**
```python
@pytest.mark.asyncio
async def test_strategic_planning_handler_exists(self, intent_service):
    """Verify handler exists and is not a placeholder"""
    result = await intent_service._handle_strategic_planning(
        query="create a sprint plan",
        params={
            'planning_type': 'sprint',
            'goal': 'Complete authentication features',
            'timeframe': '2_weeks'
        }
    )
    
    # Should not have placeholder response
    assert 'requires_clarification' not in result or result.get('requires_clarification') is False
```

**Test 2: Missing planning_type parameter**
```python
@pytest.mark.asyncio
async def test_strategic_planning_missing_type(self, intent_service):
    """Test error when planning_type missing"""
    result = await intent_service._handle_strategic_planning(
        query="create a plan",
        params={'goal': 'Some goal'}  # Missing planning_type
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'planning_type' in result['error'].lower()
```

**Test 3: Successful plan generation**
```python
@pytest.mark.asyncio
async def test_strategic_planning_success(self, intent_service):
    """Test successful strategic plan generation"""
    result = await intent_service._handle_strategic_planning(
        query="create a sprint plan for authentication work",
        params={
            'planning_type': 'sprint',
            'goal': 'Complete OAuth integration',
            'timeframe': '2_weeks'
        }
    )
    
    assert result['success'] is True
    assert 'plan' in result
    
    plan = result['plan']
    # Verify plan structure
    assert 'goal' in plan
    assert 'timeframe' in plan
    assert 'phases' in plan or 'tasks' in plan
    
    # Verify plan has actionable content
    if 'phases' in plan:
        assert len(plan['phases']) > 0
        assert 'tasks' in plan['phases'][0]
    elif 'tasks' in plan:
        assert len(plan['tasks']) > 0
```

**Test 4: Plan contains recommendations**
```python
@pytest.mark.asyncio
async def test_strategic_planning_recommendations(self, intent_service):
    """Test that plans include strategic recommendations"""
    result = await intent_service._handle_strategic_planning(
        query="plan a feature rollout",
        params={
            'planning_type': 'feature_rollout',
            'goal': 'Deploy new dashboard safely',
            'timeframe': '1_month'
        }
    )
    
    assert result['success'] is True
    # Recommendations should be present
    assert 'recommendations' in result or 'next_steps' in result
```

**Test 5: Multiple planning types**
```python
@pytest.mark.asyncio
async def test_strategic_planning_different_types(self, intent_service):
    """Test different planning types"""
    types = [
        ('sprint', {'goal': 'Complete features', 'timeframe': '2_weeks'}),
        ('feature_roadmap', {'goal': 'Plan Q1 features', 'timeframe': '3_months'}),
    ]
    
    for planning_type, params in types:
        params['planning_type'] = planning_type
        result = await intent_service._handle_strategic_planning(
            query=f"create {planning_type} plan",
            params=params
        )
        
        assert result['success'] is True, f"Failed for {planning_type}"
        assert 'plan' in result
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_strategy_handlers.py::TestHandleStrategicPlanning -v
# Should fail - handler is still placeholder
```

---

### Part 4: Implement Handler (30-40 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_strategic_planning` (find current line with Serena)

#### Step 4.1: Implementation Structure

```python
async def _handle_strategic_planning(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STRATEGIC_PLANNING intent - FULLY IMPLEMENTED
    
    Creates strategic plans for projects, sprints, features, and other initiatives.
    This is a STRATEGY operation that plans future actions and provides recommendations.
    
    Supported planning_types:
        - 'sprint': Sprint/iteration planning
        - 'feature_roadmap': Feature development roadmap
        - 'issue_resolution': Strategic approach to resolve issues
        - [Add other supported types]
    
    Args:
        query: Natural language query describing planning request
        params: Dictionary containing:
            - planning_type (required): Type of plan to create
            - goal (required): Primary goal/objective
            - timeframe (optional): Duration/deadline for plan
            - context (optional): Additional context or constraints
            - [Type-specific parameters]
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if planning succeeded
            - planning_type: Type of plan created
            - plan: The strategic plan with phases/tasks/milestones
            - recommendations: Strategic recommendations
            - error: Error message (if success is False)
    """
    try:
        # 1. VALIDATION
        planning_type = params.get('planning_type')
        if not planning_type:
            logger.warning("Planning type missing for strategic planning")
            return {
                'success': False,
                'error': 'planning_type parameter is required. Supported types: sprint, feature_roadmap, issue_resolution'
            }
        
        goal = params.get('goal')
        if not goal:
            logger.warning("Goal missing for strategic planning")
            return {
                'success': False,
                'error': 'goal parameter is required to create a strategic plan'
            }
        
        # Normalize planning_type
        planning_type = planning_type.lower().strip()
        
        # Validate planning_type is supported
        supported_types = ['sprint', 'feature_roadmap', 'issue_resolution']
        if planning_type not in supported_types:
            logger.warning(f"Unsupported planning type: {planning_type}")
            return {
                'success': False,
                'error': f'Planning type "{planning_type}" is not supported. Supported types: {", ".join(supported_types)}'
            }
        
        # Get optional parameters
        timeframe = params.get('timeframe', 'not_specified')
        context = params.get('context', '')
        
        # 2. CREATE PLAN based on type
        if planning_type == 'sprint':
            plan = await self._create_sprint_plan(goal, timeframe, context)
        elif planning_type == 'feature_roadmap':
            plan = await self._create_feature_roadmap(goal, timeframe, context)
        elif planning_type == 'issue_resolution':
            plan = await self._create_issue_resolution_plan(goal, context)
        else:
            raise ValueError(f"Unhandled planning type: {planning_type}")
        
        # 3. GENERATE RECOMMENDATIONS
        recommendations = self._generate_strategic_recommendations(plan, planning_type)
        
        # 4. RETURN SUCCESS
        logger.info(f"Successfully created {planning_type} plan for goal: {goal}")
        return {
            'success': True,
            'planning_type': planning_type,
            'goal': goal,
            'timeframe': timeframe,
            'plan': plan,
            'recommendations': recommendations
        }
        
    except Exception as e:
        # 5. HANDLE ERRORS
        logger.error(f"Failed to create strategic plan: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to create strategic plan: {str(e)}'
        }
```

#### Step 4.2: Implement Planning Methods

**Helper 1: Sprint planning**
```python
async def _create_sprint_plan(
    self,
    goal: str,
    timeframe: str,
    context: str
) -> Dict[str, Any]:
    """Create a sprint plan with phases and tasks"""
    
    # Parse timeframe
    duration_days = self._parse_timeframe_to_days(timeframe)
    
    # Create structured plan
    plan = {
        'goal': goal,
        'duration': f"{duration_days} days",
        'phases': [
            {
                'phase': 1,
                'name': 'Planning & Setup',
                'duration': '1-2 days',
                'tasks': [
                    {'task': 'Refine requirements', 'priority': 'high'},
                    {'task': 'Set up development environment', 'priority': 'high'},
                    {'task': 'Create task breakdown', 'priority': 'medium'}
                ]
            },
            {
                'phase': 2,
                'name': 'Implementation',
                'duration': f'{duration_days - 4} days',
                'tasks': [
                    {'task': f'Implement core functionality for: {goal}', 'priority': 'high'},
                    {'task': 'Write unit tests', 'priority': 'high'},
                    {'task': 'Code review and refinement', 'priority': 'medium'}
                ]
            },
            {
                'phase': 3,
                'name': 'Testing & Deployment',
                'duration': '2-3 days',
                'tasks': [
                    {'task': 'Integration testing', 'priority': 'high'},
                    {'task': 'Documentation', 'priority': 'medium'},
                    {'task': 'Deploy to staging', 'priority': 'high'},
                    {'task': 'Production deployment', 'priority': 'high'}
                ]
            }
        ],
        'success_criteria': [
            f'{goal} is fully implemented',
            'All tests passing',
            'Documentation complete',
            'Successfully deployed to production'
        ]
    }
    
    return plan

def _parse_timeframe_to_days(self, timeframe: str) -> int:
    """Parse timeframe string to days"""
    timeframe_lower = timeframe.lower()
    
    if 'week' in timeframe_lower:
        weeks = int(''.join(filter(str.isdigit, timeframe_lower)) or '2')
        return weeks * 7
    elif 'day' in timeframe_lower:
        return int(''.join(filter(str.isdigit, timeframe_lower)) or '14')
    elif 'month' in timeframe_lower:
        months = int(''.join(filter(str.isdigit, timeframe_lower)) or '1')
        return months * 30
    else:
        return 14  # Default 2 weeks
```

**Helper 2: Feature roadmap**
```python
async def _create_feature_roadmap(
    self,
    goal: str,
    timeframe: str,
    context: str
) -> Dict[str, Any]:
    """Create a feature development roadmap"""
    
    duration_days = self._parse_timeframe_to_days(timeframe)
    num_phases = max(2, duration_days // 30)  # One phase per month roughly
    
    plan = {
        'goal': goal,
        'duration': timeframe,
        'phases': []
    }
    
    # Generate phases based on typical feature development
    phase_templates = [
        ('Research & Planning', ['Market research', 'User interviews', 'Feature specification']),
        ('MVP Development', ['Core feature implementation', 'Basic UI', 'Initial testing']),
        ('Enhancement', ['Advanced features', 'Polish UI/UX', 'Performance optimization']),
        ('Launch Preparation', ['Beta testing', 'Documentation', 'Marketing materials', 'Deployment']),
    ]
    
    for i in range(min(num_phases, len(phase_templates))):
        phase_name, default_tasks = phase_templates[i]
        plan['phases'].append({
            'phase': i + 1,
            'name': phase_name,
            'tasks': [{'task': task, 'priority': 'medium'} for task in default_tasks]
        })
    
    plan['milestones'] = [
        {'milestone': 'MVP Complete', 'target_date': 'Month 1'},
        {'milestone': 'Beta Release', 'target_date': 'Month 2'},
        {'milestone': 'Public Launch', 'target_date': f'Month {num_phases}'}
    ]
    
    return plan
```

**Helper 3: Recommendations**
```python
def _generate_strategic_recommendations(
    self,
    plan: Dict[str, Any],
    planning_type: str
) -> List[str]:
    """Generate strategic recommendations based on plan"""
    
    recommendations = []
    
    if planning_type == 'sprint':
        recommendations.extend([
            'Start with highest priority tasks first',
            'Schedule daily stand-ups for team alignment',
            'Reserve buffer time for unexpected issues',
            'Conduct sprint retrospective at the end'
        ])
    elif planning_type == 'feature_roadmap':
        recommendations.extend([
            'Validate assumptions with user research early',
            'Build MVP first, then iterate based on feedback',
            'Maintain regular communication with stakeholders',
            'Plan for technical debt reduction alongside features'
        ])
    elif planning_type == 'issue_resolution':
        recommendations.extend([
            'Investigate root cause before implementing fix',
            'Write tests to prevent regression',
            'Document solution for future reference'
        ])
    
    # Add general recommendations
    recommendations.append('Track progress regularly and adjust plan as needed')
    
    return recommendations
```

---

### Part 5: Run Tests (10 min)

```bash
pytest tests/intent/test_strategy_handlers.py::TestHandleStrategicPlanning -v -s
# All tests should pass
```

---

### Part 6: Evidence Collection (10 min)

**Create**:
1. `dev/2025/10/11/phase4-test-results.txt`
2. `dev/2025/10/11/phase4-sample-plans.md`
3. `dev/2025/10/11/phase4-completion-report.md`

---

## Completion Criteria

- [ ] Tests passing
- [ ] Real plans generated
- [ ] No placeholders
- [ ] Quality maintained
- [ ] Evidence collected

---

*Phase 4 prompt created: October 11, 2025, 4:02 PM*  
*First STRATEGY handler - establishes planning pattern*  
*Time available: 90 minutes for both STRATEGY handlers*
