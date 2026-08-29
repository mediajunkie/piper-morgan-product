# MCP Skill Testing Pattern

**Status**: Established
**Date**: November 22, 2025
**Related Issues**: #303 (CONV-MCP-STANDUP)

## Overview

Testing pattern for MCP Skills (reusable workflow components that handle specific tasks with minimal token usage).

## Test Structure

### 1. Fixture Setup

All skill tests use a `skill` fixture that mocks external dependencies:

```python
@pytest.fixture
def skill():
    """Create skill instance with mocked dependencies"""
    with (
        patch("services.integrations.mcp.skills.standup_workflow_skill.MorningStandupWorkflow"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.StandupOrchestrationService"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.GitHubDomainService"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.SlackDomainService"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.UserPreferenceManager"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.SessionPersistenceManager"),
    ):
        return StandupWorkflowSkill()
```

**Key Points**:
- Mock all external domain services
- Mock preference/session managers to avoid initialization side effects
- Returns a fully isolated skill instance ready for testing

### 2. Test Organization

Tests are organized into semantic classes covering major functionality areas:

- **TestSkillValidation**: Parameter validation logic
- **TestSkillExecution**: Main execute method behavior
- **TestFormatting**: Output formatting methods
- **TestIntegration**: Multi-system integration points
- **TestErrorHandling**: Error cases and graceful degradation

### 3. Common Test Patterns

#### Testing Async Methods

```python
@pytest.mark.asyncio
async def test_execute_success(self, skill, sample_standup):
    """Test successful execution"""
    skill.workflow = AsyncMock()
    skill.workflow.generate_standup = AsyncMock(return_value=sample_standup)

    result = await skill.execute({"user_id": "test"})

    assert result["success"] is True
    skill.workflow.generate_standup.assert_called_once()
```

Use `AsyncMock` for async method mocking, `@pytest.mark.asyncio` decorator for async test functions.

#### Testing Error Handling & Degradation

```python
@pytest.mark.asyncio
async def test_partial_failure_continues(self, skill, sample_standup):
    """One system failure shouldn't stop entire workflow"""
    skill.workflow = AsyncMock()
    skill._post_to_slack = AsyncMock(side_effect=Exception("API error"))
    skill._process_github = AsyncMock(return_value={"success": True})

    result = await skill.execute({"user_id": "test", "include_slack": True, "include_github": True})

    assert result["success"] is True  # Overall success despite Slack failure
    assert "github" in result["posted_to"]
    assert "slack" not in result["posted_to"]
```

Test graceful degradation where partial failures don't crash the entire skill.

#### Testing Format Methods

```python
def test_format_multiple_formats(self, skill, sample_standup):
    """Support multiple output formats"""
    markdown = skill._format_standup(sample_standup, format_type="markdown")
    plain = skill._format_standup(sample_standup, format_type="plain")
    json_out = skill._format_standup(sample_standup, format_type="json")

    assert markdown["format"] == "markdown"
    assert plain["format"] == "plain"
    assert json_out == sample_standup  # JSON returns raw data
```

Test multiple output format paths independently.

### 4. Sample Data Fixture

Use a `sample_standup` fixture with realistic data structure:

```python
@pytest.fixture
def sample_standup():
    """Sample standup data"""
    return {
        "user_id": str(uuid4()),
        "generated_at": datetime.now().isoformat(),
        "generation_time_ms": 1500,
        "yesterday_accomplishments": [...],
        "today_priorities": [...],
        "blockers": [...],
        "github_activity": {...},
        "time_saved_minutes": 18,
    }
```

## Coverage Goals

- Parameter validation: 100% of validation rules
- Main execution path: Success and failure scenarios
- Output formatting: All supported format types
- Multi-system integration: Success and partial failure
- Error handling: Graceful degradation verification
- Token estimation: Consistency checks

## Implementation Example

See: `tests/unit/integrations/mcp/test_standup_workflow_skill.py` (22 tests)

## Related Patterns

- **Base Skill Pattern**: `pattern-mcp-skill-base.md`
- **Integration Testing**: For multi-system workflows, use integration tests with real services
- **Async Testing**: Standard pytest-asyncio patterns with proper mock setup
