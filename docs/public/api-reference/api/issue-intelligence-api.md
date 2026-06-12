# Issue Intelligence API Documentation

**Complete API reference for Issue Intelligence canonical query classes**
**Updated**: August 24, 2025
**Status**: Production-Ready API Documentation

This document provides comprehensive API documentation for the Issue Intelligence feature, including canonical query classes, data models, and integration patterns.

---

## Overview

The Issue Intelligence API extends Piper Morgan's canonical query system with GitHub issue analysis capabilities. It provides AI-powered issue prioritization, pattern discovery, and cross-feature learning while maintaining backward compatibility with existing systems.

### Key Features

- **Canonical Query Extension**: Enhances existing queries with GitHub issue intelligence
- **AI-Powered Triage**: Intelligent issue prioritization with confidence scoring
- **Pattern Learning**: Cross-feature pattern discovery and sharing
- **Graceful Degradation**: Maintains functionality when external services unavailable
- **Performance Tracking**: Built-in enhancement time monitoring

---

## Core Classes

### IssueIntelligenceCanonicalQueryEngine

Main engine class that extends canonical query functionality with GitHub issue intelligence.

#### Constructor

```python
def __init__(
    self,
    github_integration: Any,
    canonical_handlers: CanonicalHandlers,
    session_manager: Any,
    user_id: str = "xian"
)
```

**Parameters**:
- `github_integration`: GitHub API integration service
- `canonical_handlers`: Existing canonical query handlers (delegation target)
- `session_manager`: Session management service
- `user_id`: User identifier for personalized intelligence

#### Methods

##### `enhance_canonical_query(intent: Intent, session_id: str) -> IssueIntelligenceResult`

Enhance canonical query responses with GitHub issue intelligence.

**Parameters**:
- `intent`: Intent object from canonical query system
- `session_id`: Unique session identifier

**Returns**: `IssueIntelligenceResult` with enhanced response and intelligence data

**Example**:
```python
engine = IssueIntelligenceCanonicalQueryEngine(
    github_integration=github_service,
    canonical_handlers=canonical_handlers,
    session_manager=session_service
)

result = await engine.enhance_canonical_query(
    intent=Intent(
        category=IntentCategory.PRIORITY,
        action="get_top_priority",
        confidence=0.95,
        original_message="What's my top priority?"
    ),
    session_id="session_123"
)

# Access enhanced result
print(result.enhanced_message)  # Enhanced with issue context
print(result.original_response)  # Preserved original response
print(result.issue_intelligence)  # Additional GitHub data
```

##### `create_issue_intelligence_context(priority_level: str = "top") -> IssueIntelligenceContext`

Create issue intelligence context for priority-based queries.

**Parameters**:
- `priority_level`: Priority filter ("top", "high", "all")

**Returns**: `IssueIntelligenceContext` with relevant issue data

**Example**:
```python
context = await engine.create_issue_intelligence_context("high")

print(f"Priority issues: {len(context.priority_issues)}")
print(f"Open issues: {context.open_issues_count}")
print(f"Assignee context: {context.assignee_context}")
```

---

## Data Models

### IssueIntelligenceResult

Enhanced result object that preserves original canonical responses while adding issue intelligence.

#### Fields

```python
@dataclass
class IssueIntelligenceResult:
    original_response: Dict[str, Any]      # From CanonicalHandlers
    enhanced_message: str                  # With additional context
    issue_intelligence: Dict[str, Any]     # Enhancement data
    context_source: str = "github_integration"
    enhancement_time_ms: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
```

**Field Descriptions**:
- `original_response`: Complete original response from canonical handlers
- `enhanced_message`: Message enhanced with issue intelligence context
- `issue_intelligence`: Additional GitHub issue data and analysis
- `context_source`: Source of enhancement data (always "github_integration")
- `enhancement_time_ms`: Time taken for enhancement in milliseconds
- `created_at`: Timestamp when result was created

#### Example Response Structure

```json
{
    "original_response": {
        "message": "Your top priority today is completing the authentication redesign.",
        "intent": {
            "category": "PRIORITY",
            "action": "provide_top_priority",
            "confidence": 1.0
        },
        "requires_clarification": false
    },
    "enhanced_message": "Your top priority today is completing the authentication redesign.\n\n**Recent GitHub Activity:**\n🔴 #128: PM-122 FTUX Wizard Implementation\n🟢 #127: PM-121 Canonical Query Integration\n\n*1 open issues need attention*",
    "issue_intelligence": {
        "recent_issues": [
            {
                "number": 128,
                "title": "PM-122: FTUX Wizard Implementation",
                "state": "open",
                "labels": ["enhancement"]
            },
            {
                "number": 127,
                "title": "PM-121: Canonical Query Integration",
                "state": "closed",
                "labels": ["enhancement", "query"]
            }
        ],
        "open_issues_count": 1,
        "closed_issues_count": 1
    },
    "context_source": "github_integration",
    "enhancement_time_ms": 45,
    "created_at": "2025-08-24T17:30:00Z"
}
```

### IssueIntelligenceContext

Context object containing GitHub issue intelligence data for analysis.

#### Fields

```python
@dataclass
class IssueIntelligenceContext:
    user_id: str
    priority_level: str
    priority_issues: List[Dict[str, Any]] = field(default_factory=list)
    open_issues_count: int = 0
    closed_issues_count: int = 0
    assignee_context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
```

**Field Descriptions**:
- `user_id`: Identifier for the user requesting intelligence
- `priority_level`: Priority filter applied ("top", "high", "all")
- `priority_issues`: List of issues matching priority criteria
- `open_issues_count`: Count of open issues in context
- `closed_issues_count`: Count of closed issues in context
- `assignee_context`: Dictionary mapping assignees to their issues
- `created_at`: Timestamp when context was created

#### Example Context Structure

```json
{
    "user_id": "xian",
    "priority_level": "top",
    "priority_issues": [
        {
            "number": 128,
            "title": "PM-122: FTUX Wizard Implementation",
            "state": "open",
            "labels": ["enhancement", "P1-high"],
            "assignee": {
                "login": "mediajunkie",
                "name": "Xian"
            },
            "created_at": "2025-08-24T00:08:05Z"
        }
    ],
    "open_issues_count": 1,
    "closed_issues_count": 5,
    "assignee_context": {
        "mediajunkie": [
            {
                "number": 128,
                "title": "PM-122: FTUX Wizard Implementation"
            }
        ]
    },
    "created_at": "2025-08-24T17:30:00Z"
}
```

---

## Integration Patterns

### Basic Integration

Integrate Issue Intelligence with existing canonical query handlers:

```python
# Initialize dependencies
github_integration = GitHubAgent()
canonical_handlers = CanonicalHandlers(session_manager)
session_manager = SessionManager()

# Create Issue Intelligence engine
issue_engine = IssueIntelligenceCanonicalQueryEngine(
    github_integration=github_integration,
    canonical_handlers=canonical_handlers,
    session_manager=session_manager,
    user_id="your_user_id"
)

# Process enhanced queries
async def handle_priority_query(message: str, session_id: str):
    # Create intent (your existing logic)
    intent = Intent(
        category=IntentCategory.PRIORITY,
        action="get_top_priority",
        confidence=0.95,
        original_message=message
    )

    # Get enhanced response
    result = await issue_engine.enhance_canonical_query(intent, session_id)

    # Use enhanced message with issue context
    return result.enhanced_message
```

### CLI Integration

Integrate with command-line interfaces:

```python
from cli.commands.issues import IssuesCommand

async def cli_workflow():
    # Initialize CLI command
    issues_cmd = IssuesCommand()

    # Execute triage with learning
    triage_result = await issues_cmd.triage_issues(limit=10)

    # Execute status overview
    status_result = await issues_cmd.get_issue_status()

    # Discover learned patterns
    patterns_result = await issues_cmd.discover_patterns()

    return {
        "triage": triage_result,
        "status": status_result,
        "patterns": patterns_result
    }
```

### Learning System Integration

Integrate with cross-feature learning:

```python
from services.learning import get_learning_loop

async def learning_integration():
    # Get learning loop
    learning_loop = await get_learning_loop()

    # Learn from triage decision
    await learning_loop.learn_pattern(
        pattern_type=PatternType.WORKFLOW_PATTERN,
        source_feature="issue_intelligence",
        pattern_data={
            "issue_title_keywords": ["authentication", "login", "security"],
            "priority_assigned": "high",
            "labels": ["P1-high", "security"],
            "pattern_category": "triage_decision"
        },
        initial_confidence=0.7,
        metadata={"category": "triage", "priority": "high"}
    )

    # Get patterns for issue intelligence
    patterns = await learning_loop.get_patterns_for_feature(
        "issue_intelligence",
        pattern_type=PatternType.WORKFLOW_PATTERN,
        min_confidence=0.5
    )

    return patterns
```

---

## Performance Considerations

### Enhancement Time Tracking

All Issue Intelligence operations include performance tracking:

```python
# Enhancement time is automatically tracked
result = await engine.enhance_canonical_query(intent, session_id)

# Access performance data
print(f"Enhancement took: {result.enhancement_time_ms}ms")

# Target performance: <300ms for enhancement
if result.enhancement_time_ms > 300:
    logger.warning(f"Slow enhancement: {result.enhancement_time_ms}ms")
```

### Graceful Degradation

Issue Intelligence fails gracefully when external services are unavailable:

```python
# Example of graceful degradation
issue_intelligence = {
    "error": "Issue intelligence temporarily unavailable: Service timeout",
    "fallback_mode": True
}

# Original message is returned unchanged when intelligence fails
enhanced_message = original_message  # No modification on failure
```

### Caching and Optimization

- **GitHub API Responses**: Cached for 5 minutes to reduce API calls
- **Pattern Data**: Cached for optimal learning loop performance
- **Context Creation**: Optimized for <100ms typical response time
- **Enhancement Logic**: Parallel processing where possible

---

## Error Handling

### Exception Types

The API handles several types of exceptions gracefully:

#### GitHub API Errors

```python
try:
    result = await engine.enhance_canonical_query(intent, session_id)
except GitHubRateLimitError as e:
    # Handle rate limiting
    logger.warning(f"GitHub rate limit hit: retry after {e.retry_after} minutes")
    # Return original response without enhancement

except GitHubConnectionError as e:
    # Handle connection issues
    logger.error(f"GitHub connection failed: {e}")
    # Fall back to original canonical response
```

#### Learning System Errors

```python
try:
    await learning_loop.learn_pattern(pattern_data)
except LearningServiceError as e:
    # Learning failures don't break core functionality
    logger.warning(f"Pattern learning failed: {e}")
    # Continue with enhanced response
```

### Error Response Structure

When errors occur, the API maintains response structure:

```json
{
    "original_response": {
        // Always preserved even on errors
    },
    "enhanced_message": "original message unchanged",
    "issue_intelligence": {
        "error": "Service temporarily unavailable",
        "fallback_mode": true
    },
    "context_source": "fallback",
    "enhancement_time_ms": 10
}
```

---

## Testing

### Unit Test Examples

Test canonical query enhancement:

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_enhance_canonical_query():
    # Mock dependencies
    mock_github = AsyncMock()
    mock_handlers = AsyncMock()
    mock_session = AsyncMock()

    # Setup mock responses
    mock_handlers.handle.return_value = {
        "message": "Your top priority is authentication work",
        "intent": {"category": "PRIORITY"},
        "requires_clarification": False
    }

    mock_github.get_recent_issues.return_value = [
        {"number": 123, "title": "Auth bug", "state": "open"}
    ]

    # Test enhancement
    engine = IssueIntelligenceCanonicalQueryEngine(
        github_integration=mock_github,
        canonical_handlers=mock_handlers,
        session_manager=mock_session
    )

    result = await engine.enhance_canonical_query(intent, "session_123")

    # Verify enhancement
    assert result.original_response is not None
    assert "Auth bug" in result.enhanced_message
    assert result.issue_intelligence["recent_issues"] is not None
```

### Integration Test Examples

Test CLI integration:

```python
@pytest.mark.asyncio
async def test_cli_integration():
    issues_cmd = IssuesCommand()

    # Test triage command
    result = await issues_cmd.triage_issues(limit=5)

    assert result["triage_complete"] is True
    assert result["issues_analyzed"] >= 0
    assert "high_priority" in result
    assert "medium_priority" in result
    assert "low_priority" in result
```

---

## Migration Guide

### From Legacy Systems

If migrating from older issue management systems:

1. **Preserve Existing Handlers**: Issue Intelligence delegates to existing canonical handlers
2. **Gradual Enhancement**: Enable enhancement on selected query types initially
3. **Monitor Performance**: Track enhancement times and optimize as needed
4. **Validate Learning**: Review learned patterns for accuracy before high-confidence usage

### Configuration Updates

Update your configuration to enable Issue Intelligence:

```python
# Enable GitHub integration
GITHUB_TOKEN = "your_github_token"
GITHUB_REPOSITORY = "owner/repo-name"

# Enable learning system
LEARNING_SYSTEM_ENABLED = True
PATTERN_CONFIDENCE_THRESHOLD = 0.3

# Performance settings
ENHANCEMENT_TIMEOUT_MS = 300
GITHUB_API_CACHE_TTL = 300  # 5 minutes
```

---

## Related Documentation

### Architecture Documentation
- [Canonical Queries Architecture](../development/canonical-queries-architecture.md) - Technical architecture details
- Pattern Catalog *(proposed; doc TBD)* - Implementation patterns and anti-patterns

### User Documentation
- [CLI Commands User Guide](../user-guides/cli-commands.md) - Complete CLI reference
- [Issue Intelligence Features](../features/issue-intelligence.md) - Feature overview and examples

### Development Resources
- [Multi-Agent Integration Guide](../development/MULTI_AGENT_INTEGRATION_GUIDE.md) - Advanced coordination patterns
- [Test Guide](../development/TEST-GUIDE.md) - Testing strategies and examples

---

**Last Updated**: August 24, 2025
**Version**: Issue Intelligence API v1.0
**Status**: Production-Ready API Documentation
