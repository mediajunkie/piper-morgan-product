# Cross-Feature Integration Guide

**Status**: ✅ **ACTIVE** - Morning Standup + Issue Intelligence integration operational
**Created**: August 24, 2025
**Last Updated**: August 24, 2025

## 🎯 Overview

This guide documents how Piper Morgan features integrate via canonical query patterns, best practices for cross-feature development, and troubleshooting integration issues.

## 🏗️ Integration Architecture

### Canonical Query Pattern

All feature integrations use the shared CanonicalHandlers infrastructure:

```python
# Base pattern for all integrated features
from services.intent_service.canonical_handlers import CanonicalHandlers

class FeatureWorkflow:
    def __init__(self, canonical_handlers: Optional[CanonicalHandlers] = None):
        self.canonical_handlers = canonical_handlers

    async def canonical_query_integration(self, query: str, user_id: str) -> Dict[str, Any]:
        """Standard integration interface for cross-feature communication"""
        # Feature-specific integration logic
        pass
```

### Integration Layers

1. **Canonical Layer**: Shared query processing and response formatting
2. **Feature Layer**: Specific business logic and data processing
3. **Integration Layer**: Cross-feature communication and context sharing
4. **Presentation Layer**: Unified output formatting and error handling

## 📊 Current Integrations

### Morning Standup + Issue Intelligence

**Status**: ✅ **ACTIVE** since August 24, 2025

#### Integration Flow

```mermaid
graph LR
    A[Morning Standup CLI] --> B[MorningStandupWorkflow]
    B --> C[generate_with_issues]
    C --> D[IssueIntelligenceCanonicalQueryEngine]
    D --> E[CanonicalHandlers]
    E --> F[Issue Priority Analysis]
    F --> G[Integrated Standup Result]
```

#### Technical Implementation

```python
# Morning Standup integration method
async def generate_with_issues(self, user_id: str) -> StandupResult:
    # Get base standup
    base_standup = await self.generate_standup(user_id)

    # Add issue context via canonical query
    try:
        if hasattr(self, 'canonical_handlers') and self.canonical_handlers:
            issue_engine = IssueIntelligenceCanonicalQueryEngine(
                user_id=user_id,
                canonical_handlers=self.canonical_handlers
            )

            # Create intent for issue intelligence
            intent = Intent(
                user_id=user_id,
                text="what needs attention",
                category=IntentCategory.PROJECT_MANAGEMENT,
                confidence_score=1.0
            )

            # Get enhanced results
            enhanced_result = await issue_engine.enhance_canonical_query(intent, f"session_{user_id}")

            # Integrate issue priorities into standup
            if enhanced_result and enhanced_result.issue_intelligence.get("priority_issues"):
                issue_priorities = enhanced_result.issue_intelligence["priority_issues"][:3]
                for issue in issue_priorities:
                    base_standup.today_priorities.append(f"🎯 Issue #{issue.get('number')}: {issue.get('title')}")

    except Exception as e:
        # Graceful degradation
        base_standup.today_priorities.append(f"⚠️ Issue priorities unavailable: {str(e)[:50]}...")

    return base_standup
```

#### CLI Integration

```bash
# Usage examples
python cli/commands/standup.py --with-issues    # Integrated output
python cli/commands/standup.py                  # Standard output
```

## 🔧 Integration Best Practices

### 1. Canonical Pattern Compliance

**Required Elements**:
- Extend or use CanonicalHandlers
- Implement standard integration methods
- Follow async/await patterns
- Provide graceful degradation

```python
# Standard integration interface
async def canonical_query_integration(self, query: str, user_id: str) -> Dict[str, Any]:
    """
    Standard method all integrable features should implement

    Returns:
        Dict with standardized keys: context, source, integration_time_ms, error (optional)
    """
    pass
```

### 2. Error Handling Strategy

**Graceful Degradation Pattern**:

```python
try:
    # Attempt integration
    integrated_result = await other_feature.canonical_query_integration(query, user_id)
    # Use integrated result
except Exception as e:
    # Log error but continue with base functionality
    logger.warning(f"Integration failed: {e}")
    # Provide user-friendly fallback
    fallback_message = f"⚠️ {feature_name} unavailable: {str(e)[:50]}..."
```

### 3. Performance Considerations

**Integration Performance Targets**:
- Integration overhead: <200ms
- Total feature time: Maintain original performance targets
- Timeout handling: 5-second maximum integration wait
- Fallback speed: <50ms for graceful degradation

### 4. Testing Strategy

**Integration Testing Layers**:

```python
# Unit tests for integration methods
@pytest.mark.asyncio
async def test_feature_integration():
    feature = FeatureWorkflow(canonical_handlers=mock_handlers)
    result = await feature.canonical_query_integration("test query", "user_id")
    assert "context" in result
    assert "integration_time_ms" in result

# Integration tests for end-to-end functionality
@pytest.mark.integration
async def test_cross_feature_integration():
    # Test actual feature integration
    standup = MorningStandupWorkflow(canonical_handlers=real_handlers)
    result = await standup.generate_with_issues("test_user")
    assert len(result.today_priorities) > 0
```

## 🚀 Adding New Integrations

### Step 1: Canonical Compliance

Ensure your feature follows canonical patterns:

```python
class NewFeatureWorkflow:
    def __init__(self, canonical_handlers: Optional[CanonicalHandlers] = None):
        self.canonical_handlers = canonical_handlers

    async def canonical_query_integration(self, query: str, user_id: str) -> Dict[str, Any]:
        """Implement standard integration interface"""
        return {
            "context": feature_specific_context,
            "source": "new_feature_canonical",
            "integration_time_ms": processing_time,
        }
```

### Step 2: Integration Points

Identify where your feature should integrate:

- **CLI Commands**: Add flags and options for integration
- **Other Features**: Implement bidirectional integration where valuable
- **Canonical Handlers**: Register integration capabilities

### Step 3: Documentation

Document your integration:

- Add section to this integration guide
- Update feature-specific documentation
- Create usage examples and troubleshooting guides

### Step 4: Testing

Implement comprehensive testing:

- Unit tests for integration methods
- Integration tests for cross-feature functionality
- CLI tests for user-facing integration options

## 🛠️ Troubleshooting Integration Issues

### Common Integration Problems

**1. Initialization Errors**

```bash
# Error: Missing required arguments in integration
# Solution: Ensure proper dependency injection
canonical_handlers = CanonicalHandlers()
feature = FeatureWorkflow(canonical_handlers=canonical_handlers)
```

**2. Timeout Issues**

```python
# Add timeout handling to integration calls
async def safe_integration_call(feature, query, user_id):
    try:
        return await asyncio.wait_for(
            feature.canonical_query_integration(query, user_id),
            timeout=5.0  # 5-second timeout
        )
    except asyncio.TimeoutError:
        return {"error": "Integration timeout", "source": "timeout_handler"}
```

**3. Context Conflicts**

```python
# Ensure context isolation between features
integration_context = {
    "user_id": user_id,
    "session_id": f"integration_{timestamp}",
    "source_feature": self.__class__.__name__
}
```

### Debugging Integration Issues

```bash
# Test feature isolation
python -c "from services.features.feature_name import FeatureWorkflow; print('Import successful')"

# Test integration method availability
python -c "
feature = FeatureWorkflow()
print('Has integration method:', hasattr(feature, 'canonical_query_integration'))
"

# Test CLI integration flags
python path/to/cli.py --help | grep integration-flag
```

### Performance Debugging

```python
# Add timing to integration calls
import time

start_time = time.time()
result = await feature.canonical_query_integration(query, user_id)
integration_time = (time.time() - start_time) * 1000

if integration_time > 200:  # 200ms threshold
    logger.warning(f"Slow integration: {integration_time}ms")
```

## 📈 Future Integration Opportunities

### Planned Integrations

1. **FTUX Wizard + Morning Standup**: New user onboarding integration
2. **Issue Intelligence + FTUX**: Intelligent setup based on issue patterns
3. **Session Persistence + All Features**: Universal context sharing

### Integration Roadmap

- **Q4 2025**: Complete Morning Standup + Issue Intelligence optimization
- **Q1 2026**: FTUX Wizard integration across all features
- **Q2 2026**: Advanced cross-feature learning and pattern sharing

## 📚 Reference Documentation

### Related Documentation

- [Canonical Queries Architecture](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/canonical-queries-architecture.md)
- [Morning Standup User Guide](morning-standup.md)
- [Issue Intelligence User Guide](issue-intelligence.md)
- [API Reference](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/current/api-reference.md)

### Code Examples

- `services/features/morning_standup.py`: Integration implementation example
- `cli/commands/standup.py`: CLI integration example
- `tests/features/test_quick_integration.py`: Integration testing example

---

**Status**: ✅ **ACTIVE GUIDE** - Morning Standup + Issue Intelligence integration operational
**Next Integration**: FTUX Wizard cross-feature integration
**Methodology**: Canonical query pattern with graceful degradation
**Support**: Comprehensive testing and error handling frameworks available
