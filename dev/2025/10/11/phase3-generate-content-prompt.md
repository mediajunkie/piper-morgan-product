# Phase 3: SYNTHESIS Handler - _handle_generate_content

**Date**: October 11, 2025, 1:36 PM  
**Agent**: Code Agent  
**Duration**: Estimated 1-2 hours  
**Issue**: GAP-1 (CORE-CRAFT-GAP)  
**Sub-Gameplan**: 3 (SYNTHESIS Handlers - First Handler)

---

## Mission

Implement `_handle_generate_content` handler with genuine content generation functionality, establishing the SYNTHESIS category pattern. This is the **first SYNTHESIS handler** and will set the pattern for content creation operations.

**Context**: EXECUTION and ANALYSIS categories are complete. Now we establish the SYNTHESIS pattern, which focuses on creating/generating new content rather than analyzing existing data.

**PM Priority**: Thoroughness and accuracy over speed.

---

## Success Criteria

- [ ] `_handle_generate_content` generates real content (not placeholders)
- [ ] Content is actually created (not just returning `success=True`)
- [ ] Tests demonstrate actual content generation
- [ ] Pattern follows established approach (validation, service, response, error handling)
- [ ] Zero "requires_clarification" placeholder responses
- [ ] Evidence shows actual generated content with examples
- [ ] Quality maintained throughout

---

## Understanding SYNTHESIS vs ANALYSIS

**Critical Distinction**:

**ANALYSIS** (just completed):
- **Reads** existing data
- **Analyzes** patterns, trends, metrics
- **Returns** insights about what exists

**SYNTHESIS** (starting now):
- **Creates** new content
- **Generates** documents, summaries, reports
- **Returns** newly created artifacts

**This changes**:
- What services we need (content generation, not data fetching)
- What tests look like (verify creation, not analysis)
- What responses contain (created content, not metrics)

---

## Phase 3 Structure

### Part 1: Study Content Generation Requirements (30 min)

#### Step 1.1: Analyze Current Placeholder

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_generate_content` (line 788 per reconciliation)

**Current placeholder** (approximately):
```python
async def _handle_generate_content(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GENERATE_CONTENT intent - IMPLEMENTATION IN PROGRESS"""
    return {
        'success': True,
        'requires_clarification': True,
        'message': f'Content generation ready for {content_type}. Implementation in progress.'
    }
```

**Critical Questions**:
1. What types of content should this generate?
   - Documentation (README, API docs)?
   - Reports (status reports, summaries)?
   - Code (templates, boilerplate)?
   - Text (descriptions, explanations)?
   - Other?

2. What inputs are needed?
   - Content type (required)
   - Context/data to base content on?
   - Format preferences (markdown, HTML, plain text)?
   - Length/style preferences?

3. How is content generated?
   - Templates with variable substitution?
   - LLM-based generation (if available)?
   - Rule-based generation?
   - Combination?

4. What should the output contain?
   - The generated content itself
   - Metadata (length, format, generation method)
   - Success/error status
   - Suggestions for improvement?

**STOP if requirements are unclear** - Report to PM for clarification

#### Step 1.2: Review Existing Content Generation

**Check for existing generation capabilities**:

```bash
# Search for content generation utilities
grep -r "generate\|template\|create.*content" services/ --include="*.py" | grep -i "def\|class"

# Check for template files
find . -name "*.template" -o -name "*_template.*"

# Check for any LLM/AI integration
grep -r "openai\|anthropic\|claude\|gpt" services/ --include="*.py"

# Check for markdown/document generation
grep -r "markdown\|document.*gen" services/ --include="*.py"
```

**Document findings**:
- What generation capabilities exist?
- What can be leveraged vs what needs building?
- What's the simplest starting point?

---

### Part 2: Define Content Types and Generation Strategy (45 min)

#### Step 2.1: Choose Supported Content Types

**Start with 2-3 content types that are**:
- Actually useful for Piper Morgan users
- Implementable with available tools/services
- Good examples of SYNTHESIS category

**Example content types** (choose 2-3):

1. **Status Report**
   - Input: repository, time period
   - Generate: Markdown report of activity
   - Uses: Analysis data from Phase 2C
   - Template-based generation

2. **README Section**
   - Input: component name, purpose
   - Generate: README markdown section
   - Uses: Template + parameter substitution
   - Simple and demonstrable

3. **Issue Template**
   - Input: issue type (bug, feature, task)
   - Generate: Formatted issue body
   - Uses: Templates
   - Practical and useful

4. **Documentation Page**
   - Input: component name, API methods
   - Generate: API documentation
   - Uses: Code analysis + templates
   - More complex but valuable

5. **Summary Text**
   - Input: raw data/text
   - Generate: Concise summary
   - Uses: Text processing
   - Overlaps with `_handle_summarize` (Phase 3B)

**Choose wisely**: Pick types that are distinct, useful, and implementable

#### Step 2.2: Design Generation Approach

**For each chosen content type, define**:

```markdown
## Content Type: [Name]

### Input Parameters
- content_type: "[type_name]"
- [param1]: [description]
- [param2]: [description]
- Optional: [optional_params]

### Generation Method
- [ ] Template-based (*.template file + substitution)
- [ ] Rule-based (programmatic generation)
- [ ] Data-driven (uses analysis results)
- [ ] Combination

### Output Structure
```python
{
    'success': True,
    'content_type': '[type_name]',
    'content': '[generated content here]',
    'format': 'markdown',  # or 'html', 'text', etc.
    'metadata': {
        'length': 1234,
        'generated_at': '2024-10-11T13:36:00',
        'generation_method': 'template'
    }
}
```

### Quality Checks
- [ ] Content is not empty
- [ ] Content is properly formatted
- [ ] Content contains expected sections
- [ ] Content is useful/actionable
```

#### Step 2.3: Create Templates if Needed

**If using template-based generation, create templates**:

**Example**: `templates/status_report.md.template`
```markdown
# Status Report: {repository}

**Period**: {start_date} to {end_date}

## Summary
{summary}

## Activity Metrics
- Commits: {commit_count}
- Issues Closed: {issues_closed}
- Pull Requests: {prs_merged}

## Contributors
{contributor_list}

## Recent Highlights
{highlights}

---
*Generated by Piper Morgan on {generated_at}*
```

**Create templates for each content type** you support

---

### Part 3: Write Comprehensive Tests (TDD) (45 min)

**File**: `tests/intent/test_synthesis_handlers.py` (new file)

#### Step 3.1: Test Structure

```python
import pytest
from datetime import datetime
from services.intent.intent_service import IntentService

class TestHandleGenerateContent:
    """Comprehensive tests for _handle_generate_content handler
    
    SYNTHESIS handlers create new content, so tests verify:
    - Content is actually generated (not empty)
    - Content format is correct
    - Content contains expected elements
    - Generation handles various content types
    """
    
    @pytest.fixture
    async def intent_service(self):
        """Create IntentService with required services"""
        service = IntentService()
        return service
```

#### Step 3.2: Write Thorough Unit Tests

**Test 1: Successful content generation**
```python
@pytest.mark.asyncio
async def test_handle_generate_content_success(self, intent_service):
    """Test successful content generation"""
    result = await intent_service._handle_generate_content(
        query="generate a status report for piper-morgan",
        params={
            'content_type': 'status_report',
            'repository': 'piper-morgan',
            'period': 'last_week'
        }
    )
    
    # Verify no placeholder response
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify content was generated
    assert 'content' in result
    assert result['content'] is not None
    assert len(result['content']) > 0
    
    # Verify content quality
    assert isinstance(result['content'], str)
    content = result['content']
    assert 'Status Report' in content or 'status report' in content.lower()
    assert len(content) > 100  # Non-trivial content
```

**Test 2: Missing content_type parameter**
```python
@pytest.mark.asyncio
async def test_handle_generate_content_missing_type(self, intent_service):
    """Test error when content_type missing"""
    result = await intent_service._handle_generate_content(
        query="generate content",
        params={'repository': 'piper-morgan'}  # Missing content_type
    )
    
    assert result['success'] is False
    assert 'error' in result
    assert 'content_type' in result['error'].lower()
```

**Test 3: Unsupported content type**
```python
@pytest.mark.asyncio
async def test_handle_generate_content_unsupported_type(self, intent_service):
    """Test handling of unsupported content type"""
    result = await intent_service._handle_generate_content(
        query="generate quantum physics paper",
        params={
            'content_type': 'quantum_physics_paper',
            'repository': 'piper-morgan'
        }
    )
    
    # Should return clear error about unsupported type
    assert result['success'] is False
    assert 'error' in result
    assert 'unsupported' in result['error'].lower() or 'not supported' in result['error'].lower()
```

**Test 4: Multiple content types**
```python
@pytest.mark.asyncio
async def test_handle_generate_content_multiple_types(self, intent_service):
    """Test generation of different content types"""
    content_types = [
        ('status_report', {'repository': 'piper-morgan', 'period': 'last_week'}),
        ('readme_section', {'component': 'IntentService', 'purpose': 'Intent routing'}),
        ('issue_template', {'issue_type': 'bug'})
    ]
    
    for content_type, params in content_types:
        params['content_type'] = content_type
        result = await intent_service._handle_generate_content(
            query=f"generate {content_type}",
            params=params
        )
        
        # Each type should succeed
        assert result['success'] is True, f"Failed for content_type: {content_type}"
        assert 'content' in result
        assert len(result['content']) > 50  # Meaningful content
```

**Test 5: Content format specification**
```python
@pytest.mark.asyncio
async def test_handle_generate_content_format(self, intent_service):
    """Test content format metadata"""
    result = await intent_service._handle_generate_content(
        query="generate status report",
        params={
            'content_type': 'status_report',
            'repository': 'piper-morgan',
            'format': 'markdown'
        }
    )
    
    assert result['success'] is True
    assert 'format' in result
    assert result['format'] in ['markdown', 'html', 'text', 'plain']
```

#### Step 3.3: Write Integration Test

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_handle_generate_content_real_generation(self, intent_service):
    """Test with real content generation - comprehensive integration"""
    
    result = await intent_service._handle_generate_content(
        query="generate a comprehensive status report for piper-morgan from the last month",
        params={
            'content_type': 'status_report',
            'repository': 'piper-morgan',
            'period': 'last_month'
        }
    )
    
    # Verify success
    assert result['success'] is True
    assert 'requires_clarification' not in result
    
    # Verify content was actually generated
    assert 'content' in result
    content = result['content']
    assert content is not None
    assert len(content) > 200  # Substantial content
    
    # Verify content quality - should contain expected sections
    assert 'Status Report' in content or 'status report' in content.lower()
    assert 'piper-morgan' in content.lower()
    
    # Verify metadata
    if 'metadata' in result:
        metadata = result['metadata']
        assert 'length' in metadata or 'generated_at' in metadata
    
    # Log for manual review
    import json
    logger.info(f"Generated content sample:\n{content[:500]}...")
    logger.info(f"Full result: {json.dumps(result, indent=2, default=str)}")
```

**Run tests to verify they fail** (TDD red phase):
```bash
pytest tests/intent/test_synthesis_handlers.py::TestHandleGenerateContent -v
# Should fail - handler is still placeholder
```

---

### Part 4: Implement Handler Thoroughly (60-90 min)

**File**: `services/intent/intent_service.py`  
**Method**: `_handle_generate_content` (currently line 788)

#### Step 4.1: Implementation Structure

```python
async def _handle_generate_content(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GENERATE_CONTENT intent - FULLY IMPLEMENTED
    
    Generates content based on templates and data. This is a SYNTHESIS operation
    that creates new artifacts rather than analyzing existing data.
    
    Supported content_types:
        - 'status_report': Generate repository status report
        - 'readme_section': Generate README section
        - 'issue_template': Generate issue template
        - [Add other supported types]
    
    Args:
        query: Natural language query describing generation request
        params: Dictionary containing:
            - content_type (required): Type of content to generate
            - [Type-specific parameters]
    
    Returns:
        Dictionary containing:
            - success: Boolean indicating if generation succeeded
            - content: The generated content (if successful)
            - content_type: Type of content generated
            - format: Format of content (markdown, html, text)
            - metadata: Generation metadata
            - error: Error message (if success is False)
    """
    try:
        # 1. VALIDATION
        content_type = params.get('content_type')
        if not content_type:
            logger.warning("Content type missing for content generation")
            return {
                'success': False,
                'error': 'content_type parameter is required. Supported types: status_report, readme_section, issue_template'
            }
        
        # Normalize content_type
        content_type = content_type.lower().strip()
        
        # Validate content_type is supported
        supported_types = ['status_report', 'readme_section', 'issue_template']
        if content_type not in supported_types:
            logger.warning(f"Unsupported content type: {content_type}")
            return {
                'success': False,
                'error': f'Content type "{content_type}" is not supported. Supported types: {", ".join(supported_types)}'
            }
        
        # 2. GENERATE CONTENT based on type
        if content_type == 'status_report':
            content = await self._generate_status_report(params)
        elif content_type == 'readme_section':
            content = await self._generate_readme_section(params)
        elif content_type == 'issue_template':
            content = await self._generate_issue_template(params)
        else:
            # Should not reach here due to validation above
            raise ValueError(f"Unhandled content type: {content_type}")
        
        # 3. VALIDATE generated content
        if not content or len(content.strip()) == 0:
            logger.error(f"Content generation produced empty result for type: {content_type}")
            return {
                'success': False,
                'error': f'Content generation failed to produce output for type: {content_type}'
            }
        
        # 4. RETURN SUCCESS with content
        logger.info(f"Successfully generated {content_type} ({len(content)} characters)")
        return {
            'success': True,
            'content_type': content_type,
            'content': content,
            'format': 'markdown',  # Adjust based on actual format
            'metadata': {
                'length': len(content),
                'generated_at': datetime.now().isoformat(),
                'generation_method': 'template'  # or other method
            }
        }
        
    except Exception as e:
        # 5. HANDLE ERRORS
        logger.error(f"Failed to generate content: {e}", exc_info=True)
        return {
            'success': False,
            'error': f'Failed to generate content: {str(e)}'
        }
```

#### Step 4.2: Implement Generation Methods

**Helper method 1: Generate status report**
```python
async def _generate_status_report(self, params: Dict[str, Any]) -> str:
    """Generate a status report for a repository
    
    Uses analysis data to create a comprehensive status report.
    """
    repository = params.get('repository', 'unknown')
    period = params.get('period', 'last_week')
    
    # Get analysis data (reuse from Phase 2C)
    analysis_result = await self._handle_analyze_data(
        query=f"analyze repository metrics for {repository}",
        params={
            'data_type': 'repository_metrics',
            'repository': repository,
            'period': period
        }
    )
    
    if not analysis_result.get('success'):
        return f"# Status Report: {repository}\n\nUnable to generate report - data analysis failed."
    
    metrics = analysis_result.get('metrics', {})
    
    # Generate report content
    report = f"""# Status Report: {repository}

**Period**: {period}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary

Repository activity for {repository} during the {period} period.

## Activity Metrics

- **Total Activity**: {metrics.get('total_activity', 0)} events
- **Commit Count**: {metrics.get('commit_count', 0)}
- **Issues Activity**: {metrics.get('issue_activity', 0)} events
- **PR Activity**: {metrics.get('pr_activity', 0)} events

## Detailed Statistics

{self._format_metrics_section(metrics)}

## Insights

{self._format_insights(analysis_result.get('insights', []))}

---
*Generated by Piper Morgan*
"""
    
    return report

def _format_metrics_section(self, metrics: Dict[str, Any]) -> str:
    """Format metrics into readable sections"""
    sections = []
    
    for key, value in metrics.items():
        if isinstance(value, (int, float)):
            sections.append(f"- **{key.replace('_', ' ').title()}**: {value}")
    
    return '\n'.join(sections) if sections else '*No detailed metrics available*'

def _format_insights(self, insights: List[str]) -> str:
    """Format insights as bullet points"""
    if not insights:
        return '*No specific insights generated*'
    
    return '\n'.join(f"- {insight}" for insight in insights)
```

**Helper method 2: Generate README section**
```python
async def _generate_readme_section(self, params: Dict[str, Any]) -> str:
    """Generate a README section for a component"""
    component = params.get('component', 'Component')
    purpose = params.get('purpose', 'This component provides functionality')
    
    # Template-based generation
    section = f"""## {component}

### Purpose

{purpose}

### Usage

```python
from services.{component.lower()} import {component}

# Initialize the component
{component.lower()} = {component}()

# Use the component
result = await {component.lower()}.process()
```

### Configuration

[Configuration details go here]

### API Reference

[API documentation goes here]
"""
    
    return section
```

**Helper method 3: Generate issue template**
```python
async def _generate_issue_template(self, params: Dict[str, Any]) -> str:
    """Generate an issue template"""
    issue_type = params.get('issue_type', 'bug')
    
    templates = {
        'bug': """## Bug Report

**Description**
A clear and concise description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
A clear description of what you expected to happen.

**Actual Behavior**
A clear description of what actually happened.

**Environment**
- OS: [e.g., macOS, Linux, Windows]
- Python Version: [e.g., 3.11]
- Piper Morgan Version: [e.g., 0.1.0]

**Additional Context**
Add any other context about the problem here.
""",
        'feature': """## Feature Request

**Description**
A clear and concise description of the feature.

**Use Case**
Describe the problem this feature would solve.

**Proposed Solution**
Describe how you envision this feature working.

**Alternatives Considered**
Describe any alternative solutions you've considered.

**Additional Context**
Add any other context or screenshots about the feature request.
""",
        'task': """## Task

**Description**
A clear description of the task to be completed.

**Acceptance Criteria**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Dependencies**
List any dependencies or blockers.

**Estimated Effort**
[e.g., 2 hours, 1 day]
"""
    }
    
    return templates.get(issue_type, templates['bug'])
```

**Implementation Quality Checklist**:
- [ ] All validation thorough
- [ ] Error messages helpful
- [ ] Logging comprehensive
- [ ] Content generation actually works
- [ ] Generated content is useful
- [ ] Helper methods are focused
- [ ] Code is readable
- [ ] No placeholder markers

---

### Part 5: Run Tests Thoroughly (30 min)

```bash
# Run all SYNTHESIS tests
pytest tests/intent/test_synthesis_handlers.py::TestHandleGenerateContent -v -s

# Verify all pass
# Review generated content in logs
# Confirm quality
```

---

### Part 6: Evidence Collection (30 min)

**Create comprehensive documentation**:

1. **Test Results**: `dev/2025/10/11/phase3-test-results.txt`
2. **Sample Content**: `dev/2025/10/11/phase3-sample-generated-content.md`
3. **Pattern Comparison**: `dev/2025/10/11/phase3-synthesis-pattern.md`
4. **Implementation Summary**: `dev/2025/10/11/phase3-completion-report.md`

---

## Phase 3 Completion Criteria

- [ ] Tests written and comprehensive
- [ ] Implementation complete
- [ ] All tests passing
- [ ] Content actually generated (not empty)
- [ ] No placeholder responses
- [ ] Multiple content types supported
- [ ] Quality maintained
- [ ] Evidence collected

---

## STOP Conditions

- Requirements unclear
- No good approach for content generation
- Pattern doesn't apply
- Quality concerns
- **Any uncertainty about thoroughness**

---

*Phase 3 prompt created: October 11, 2025, 1:36 PM*  
*Agent: Code Agent*  
*First SYNTHESIS handler - establishes content creation pattern*  
*Priority: Thoroughness and accuracy*
