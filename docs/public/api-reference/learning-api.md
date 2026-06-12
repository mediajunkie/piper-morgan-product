# Learning System API Reference

**Version**: 1.3
**Base URL**: `/api/v1/learning`
**Issues**: #221 (CORE-LEARN-A), #222 (CORE-LEARN-B), #223 (CORE-LEARN-C), #224 (CORE-LEARN-D)
**Status**: Production Ready ✅

---

## Overview

The Learning API provides endpoints for managing learned patterns, submitting feedback, and accessing learning analytics. The system learns from query patterns across features (CLI, Web, Slack) to optimize future operations.

**Key Features:**
- Pattern learning and retrieval
- Feedback submission for continuous improvement
- Cross-feature knowledge sharing
- Learning analytics and statistics
- User preference management

**Privacy Note:** The system learns from metadata and patterns only. No personally identifiable information (PII) is stored in learned patterns.

---

## Authentication

All endpoints require JWT authentication via the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

See Authentication API *(proposed; doc TBD)* for token generation.

---

## Pattern Types

The system supports 8 pattern types for comprehensive learning across different domains:

**Core Patterns** (Issue #221):
- **`query_pattern`** - User query optimization and intent learning
- **`response_pattern`** - Response format and content preferences
- **`workflow_pattern`** - Command sequence and workflow learning
- **`integration_pattern`** - Tool and service integration patterns
- **`user_preference_pattern`** - User-specific behavior patterns

**Extended Patterns** (Issue #222 - CORE-LEARN-B):
- **`temporal_pattern`** - Time-based trends and recurring patterns
- **`communication_pattern`** - Communication style and format preferences
- **`error_pattern`** - Error detection and recovery patterns

Each pattern type uses the same confidence scoring, feedback, and analytics infrastructure.

---

## Preference Learning

**Issue**: #223 (CORE-LEARN-C)

The system learns user preferences both **explicitly** (stated) and **implicitly** (inferred from behavior patterns).

### How It Works

1. **Pattern Detection**: User behavior creates patterns through repeated actions
2. **Confidence Building**: Patterns gain confidence as they're observed multiple times
3. **Automatic Application**: High-confidence patterns (≥ 0.7) automatically become explicit preferences
4. **Hierarchical Storage**: Preferences follow Session > User > Global precedence

### Explicit vs Implicit Preferences

**Explicit Preferences**:
- Directly stated by user through configuration or commands
- Set via API endpoints or preference management
- Take precedence over learned preferences

**Implicit Preferences**:
- Derived from `USER_PREFERENCE_PATTERN` observations
- Automatically applied when confidence ≥ 0.7
- Converted to explicit preferences in UserPreferenceManager

**Example Flow**:
```
User Action (15x): Chooses "concise" response format
    ↓
Pattern Detected: USER_PREFERENCE_PATTERN (confidence: 0.85)
    ↓
Auto-Applied: preference "response_format" = "concise"
    ↓
Future Interactions: Automatically use concise format
```

### Confidence Threshold

Only high-confidence patterns become preferences:
- **Confidence ≥ 0.7**: Pattern applied as explicit preference
- **Confidence < 0.7**: Pattern observed but not applied
- **Rationale**: Prevents false positives from limited observations

### Conflict Resolution

When preferences conflict, hierarchy determines precedence:

1. **Session > User > Global**: More specific scopes win
2. **Explicit > Implicit**: Stated preferences override learned patterns
3. **Recent > Historical**: Newer preferences override older (via versioning)

**Example**:
```python
# User explicitly sets preference
POST /api/v1/preferences
{"key": "format", "value": "json", "user_id": "user123"}

# System learns different preference from behavior
# Pattern: "format" = "markdown" (confidence: 0.8)

# Result: Explicit preference ("json") takes precedence
```

### Privacy & Safety

- **Confidence Gating**: Only high-confidence patterns (≥ 0.7) applied
- **JSON Validation**: Prevents PII leakage through serialization checks
- **TTL Expiration**: Session preferences auto-expire
- **Scope Isolation**: User/session/global separation prevents cross-contamination

### Integration with Pattern System

**Learning Flow**:
```python
# 1. Pattern is learned through QueryLearningLoop
pattern_id = await learning_loop.learn_pattern(
    pattern_type=PatternType.USER_PREFERENCE_PATTERN,
    source_feature="user_interaction",
    pattern_data={
        "preference_key": "response_style",
        "preference_value": "concise"
    },
    initial_confidence=0.85
)

# 2. Pattern is automatically applied to preferences
success, result, confidence = await learning_loop.apply_pattern(
    pattern_id=pattern_id,
    context={"user_id": "user123"}
)

# 3. Preference is now available for all features
style = await preference_manager.get_preference(
    key="response_style",
    user_id="user123"
)
# Returns: "concise"
```

### Supported Preference Categories

**Reminder Preferences** (Sprint A4):
- `standup_reminder_enabled`, `standup_reminder_time`
- `standup_reminder_timezone`, `standup_reminder_days`

**Learning Preferences** (CORE-LEARN-A):
- `learning_enabled`, `learning_min_confidence`, `learning_features`

**Custom Preferences**:
- Any preference learned through USER_PREFERENCE_PATTERN
- Stored with same validation and hierarchy as specialized preferences

---

## Workflow Optimization

**Issue**: #224 (CORE-LEARN-D - Sprint A5 Finale)

The system provides workflow optimization through A/B testing via the Chain-of-Draft experiment system. This enables automatic identification of workflow improvements and creation of reusable templates.

### How It Works

1. **Experiment Execution**: Chain-of-Draft runs 2-draft A/B tests on workflows
2. **Quality Assessment**: Multi-factor scoring (performance, success rate, task decomposition)
3. **Pattern Learning**: Workflows with ≥5% improvement automatically become learned patterns
4. **Template Creation**: High-confidence patterns (≥0.8) can be converted to reusable templates

### A/B Testing Framework

**Chain-of-Draft Capabilities**:
- **2-Draft Experiments**: Execute workflow twice with slight variations
- **Quality Scoring**: Weighted assessment (performance 30%, success 30%, decomposition 20%, distribution 20%)
- **Improvement Detection**: Identifies performance, accuracy, completeness, efficiency, and clarity improvements
- **Learning Insights**: Automatic recommendations for workflow optimization

**Optimization Metrics**:
- **Time to Completion**: Total experiment time and per-draft execution time
- **Quality Score**: 0.0-1.0 weighted score (POOR < 0.5, ACCEPTABLE 0.5-0.7, GOOD 0.7-0.9, EXCELLENT ≥0.9)
- **Success Rate**: Percentage of successful subtask completions
- **Improvement Percentage**: Quality improvement from Draft 1 to Draft 2

### Running Workflow Experiments

**Python API**:
```python
from services.learning.query_learning_loop import QueryLearningLoop
from services.domain.models import Intent
from services.shared_types import IntentCategory

# Create intent for workflow to optimize
intent = Intent(
    category=IntentCategory.EXECUTION,
    action="implement_rest_api",
    original_message="Implement REST API with auth and validation",
    confidence=0.95
)

# Run optimization experiment
learning_loop = QueryLearningLoop()
result = await learning_loop.optimize_workflow_via_experiments(
    intent=intent,
    context={"user_id": "user123"}
)

# Check results
if result["success"]:
    optimization = result["optimization"]
    print(f"Best Quality: {optimization['best_draft_quality']}")
    print(f"Improvement: {optimization['improvement_percentage']}%")
    print(f"Insights: {optimization['learning_insights']}")

    if optimization.get("pattern_learned"):
        print(f"Pattern ID: {optimization['learned_pattern_id']}")
```

**Response Structure**:
```json
{
  "success": true,
  "experiment_id": "exp_intent_12345_1729442890123",
  "optimization": {
    "best_draft_quality": 0.88,
    "improvement_percentage": 12.5,
    "improvement_types": ["performance", "accuracy"],
    "learning_insights": [
      "Draft 2 showed 12.5% quality improvement",
      "Significant performance improvement: 75ms faster"
    ],
    "recommendations": [
      "Continue with context variation approaches"
    ],
    "total_experiment_time_ms": 1850,
    "pattern_learned": true,
    "learned_pattern_id": "workflow_pattern_chain_of_draft_optimization_20251020_142500"
  }
}
```

### Creating Workflow Templates

High-confidence workflow patterns (≥0.8) can be converted to reusable templates for similar workflows.

**Python API**:
```python
# Create template from learned pattern
template_result = await learning_loop.create_workflow_template_from_pattern(
    pattern_id="workflow_pattern_chain_of_draft_optimization_20251020_142500",
    template_name="rest_api_optimization_template"
)

if template_result["success"]:
    template = template_result["template"]
    print(f"Template: {template['template_name']}")
    print(f"Confidence: {template['confidence']}")
    print(f"Expected Quality: {template['expected_quality']}")
    print(f"Steps: {len(template['steps'])}")
```

**Template Structure**:
```json
{
  "success": true,
  "template": {
    "template_name": "rest_api_optimization_template",
    "template_id": "wf_template_1729442950000",
    "based_on_pattern": "workflow_pattern_chain_of_draft_optimization_20251020_142500",
    "confidence": 0.85,
    "steps": [
      {
        "step_number": 1,
        "description_template": "Parse user requirements and define API schema",
        "agent_preference": "CODE",
        "parameters": []
      },
      {
        "step_number": 2,
        "description_template": "Implement API endpoints with validation",
        "agent_preference": "CODE",
        "parameters": []
      },
      {
        "step_number": 3,
        "description_template": "Add authentication and authorization layer",
        "agent_preference": "CURSOR",
        "parameters": []
      }
    ],
    "expected_quality": 0.88,
    "expected_time_ms": 1200,
    "created_at": "2025-10-20T14:25:50.000000",
    "usage_count": 0
  },
  "template_pattern_id": "workflow_pattern_workflow_templates_20251020_142551",
  "message": "Template 'rest_api_optimization_template' created from pattern workflow_pattern_chain_of_draft_optimization_20251020_142500"
}
```

### Template Requirements

**Minimum Confidence**: Templates can only be created from patterns with confidence ≥ 0.8
**Pattern Learning**: Workflows must show ≥5% improvement to be learned as patterns
**Pattern Type**: Only WORKFLOW_PATTERN types support template creation

**Error Handling**:
```python
# Low confidence pattern (< 0.8)
result = await learning_loop.create_workflow_template_from_pattern(
    pattern_id="low_confidence_pattern",
    template_name="will_fail"
)
# Returns: {"success": false, "error": "Pattern confidence 0.6 below 0.8 threshold"}

# Pattern not found
result = await learning_loop.create_workflow_template_from_pattern(
    pattern_id="nonexistent",
    template_name="will_fail"
)
# Returns: {"success": false, "error": "Pattern nonexistent not found"}
```

### Integration with Learning System

**Automatic Pattern Learning**:
- Experiments with ≥5% improvement automatically learn WORKFLOW_PATTERN
- Pattern confidence based on improvement percentage (capped at 0.95)
- Pattern includes workflow steps, quality score, execution time, and insights

**Cross-Feature Knowledge**:
- Workflow patterns can be shared via CrossFeatureKnowledgeService
- Templates enable knowledge transfer across different features
- Optimization insights inform future workflow decisions

### Use Cases

1. **Multi-Agent Coordination**: Optimize task decomposition and agent assignment
2. **REST API Development**: Learn optimal implementation workflows
3. **Database Refactoring**: Capture proven refactoring sequences
4. **Testing Workflows**: Optimize test creation and execution patterns
5. **Code Review Processes**: Learn efficient review and feedback cycles

### Dashboard Integration

Workflow optimization metrics are available through the analytics endpoint:

```python
# Get learning analytics
analytics = await learning_loop.get_learning_stats()

# Workflow-specific metrics
workflow_patterns = [p for p in analytics["patterns_by_type"]["workflow_pattern"]]
avg_quality = sum(p["quality_score"] for p in workflow_patterns) / len(workflow_patterns)
avg_improvement = sum(p["pattern_data"]["improvement_achieved"] for p in workflow_patterns) / len(workflow_patterns)
```

---

## Pattern Management

### Get Patterns

Retrieve learned patterns with optional filtering.

**Endpoint:** `GET /api/v1/learning/patterns`

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source_feature` | string | No | null | Filter by source feature name |
| `min_confidence` | float | No | 0.5 | Minimum confidence threshold (0.0-1.0) |

**Response:**
```json
{
  "patterns": [
    {
      "pattern_id": "query_pattern_QUERY_20251020_120000",
      "pattern_type": "query_pattern",
      "source_feature": "orchestration_QUERY",
      "confidence": 0.85,
      "usage_count": 15,
      "success_rate": 0.93
    }
  ],
  "count": 1
}
```

**Example:**
```bash
curl -X GET "http://localhost:8001/api/v1/learning/patterns?source_feature=QUERY&min_confidence=0.7" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Error Responses:**
- `500` - Internal error retrieving patterns

---

### Learn Pattern

Record a new pattern from successful operations.

**Endpoint:** `POST /api/v1/learning/patterns`

**Request Body:**
```json
{
  "pattern_type": "query_pattern",
  "source_feature": "orchestration_QUERY",
  "pattern_data": {
    "query": "search for project management tools",
    "action": "search_projects",
    "entity": "project"
  },
  "initial_confidence": 0.8,
  "metadata": {
    "timestamp": "2025-10-20T12:00:00Z",
    "success": true
  }
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pattern_type` | string | Yes | Pattern type: `query_pattern`, `response_pattern`, `workflow_pattern`, `integration_pattern`, `user_preference_pattern`, `temporal_pattern`, `communication_pattern`, `error_pattern` |
| `source_feature` | string | Yes | Feature that generated the pattern |
| `pattern_data` | object | Yes | The actual pattern data |
| `initial_confidence` | float | No | Starting confidence (0.0-1.0, default: 0.5) |
| `metadata` | object | No | Additional metadata |

**Response:**
```json
{
  "status": "pattern_learned",
  "pattern_id": "query_pattern_orchestration_QUERY_20251020_120143",
  "confidence": 0.8
}
```

**Error Responses:**
- `400` - Invalid pattern type or data
- `500` - Internal error learning pattern

**Example:**
```bash
curl -X POST "http://localhost:8001/api/v1/learning/patterns" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pattern_type": "query_pattern",
    "source_feature": "user_query",
    "pattern_data": {"query": "find recent issues"},
    "initial_confidence": 0.7
  }'
```

---

### Apply Pattern

Apply a learned pattern to a new context.

**Endpoint:** `POST /api/v1/learning/patterns/apply`

**Request Body:**
```json
{
  "pattern_id": "query_pattern_QUERY_20251020_120000",
  "context": {
    "entity": "project",
    "user_id": "user_123"
  }
}
```

**Response:**
```json
{
  "status": "pattern_applied",
  "pattern_id": "query_pattern_QUERY_20251020_120000",
  "result": {
    "success": true,
    "optimized_query": "search projects"
  },
  "confidence": 0.87
}
```

**Error Responses:**
- `404` - Pattern not found or failed to apply
- `400` - Invalid application context
- `500` - Internal error applying pattern

---

## Feedback System

### Submit Feedback

Provide feedback on pattern effectiveness.

**Endpoint:** `POST /api/v1/learning/feedback`

**Request Body:**
```json
{
  "pattern_id": "query_pattern_QUERY_20251020_120000",
  "success": true,
  "feedback": "Pattern worked perfectly for project search",
  "context": {
    "execution_time_ms": 250,
    "result_count": 15
  }
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pattern_id` | string | Yes | Pattern identifier |
| `success` | boolean | Yes | Was pattern application successful? |
| `feedback` | string | No | Optional feedback text |
| `context` | object | No | Additional context |

**Response:**
```json
{
  "status": "feedback_recorded",
  "pattern_id": "query_pattern_QUERY_20251020_120000",
  "success": true
}
```

**Note:** Success feedback increases pattern confidence, failure feedback decreases it.

**Error Responses:**
- `404` - Pattern not found
- `400` - Invalid feedback data
- `500` - Internal error recording feedback

---

## Analytics

### Get Learning Analytics

Retrieve learning system statistics and analytics.

**Endpoint:** `GET /api/v1/learning/analytics`

**Response:**
```json
{
  "total_patterns": 127,
  "patterns_by_feature": {
    "orchestration_QUERY": 45,
    "orchestration_CREATE_TICKET": 32,
    "user_query": 50
  },
  "pattern_type_distribution": {
    "query_pattern": 95,
    "workflow_pattern": 32
  },
  "average_confidence": 0.78,
  "total_feedback": 234,
  "recent_patterns_24h": 12,
  "recent_feedback_24h": 28
}
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `total_patterns` | integer | Total learned patterns |
| `patterns_by_feature` | object | Breakdown by source feature |
| `pattern_type_distribution` | object | Breakdown by pattern type |
| `average_confidence` | float | Average confidence across all patterns |
| `total_feedback` | integer | Total feedback submissions |
| `recent_patterns_24h` | integer | Patterns created in last 24 hours |
| `recent_feedback_24h` | integer | Feedback submitted in last 24 hours |

**Error Responses:**
- `500` - Internal error retrieving analytics

---

## Cross-Feature Knowledge

### Get Shared Knowledge

Retrieve knowledge shared across features.

**Endpoint:** `GET /api/v1/learning/knowledge/shared`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_feature` | string | No | Filter by source feature |
| `target_feature` | string | No | Filter by target feature |

**Response:**
```json
{
  "knowledge": [],
  "count": 0,
  "note": "Cross-feature knowledge service requires database integration (Phase 2)"
}
```

**Status:** Not yet implemented (requires database integration in Phase 2)

---

### Share Knowledge

Share knowledge between features.

**Endpoint:** `POST /api/v1/learning/knowledge/share`

**Request Body:**
```json
{
  "source_feature": "issue_intelligence",
  "target_feature": "morning_standup",
  "knowledge_type": "pattern_optimization",
  "content": {
    "optimization": "batch similar queries"
  }
}
```

**Response:**
```json
{
  "detail": "Cross-feature knowledge service requires database integration (Phase 2)",
  "error_id": "SERVICE_NOT_AVAILABLE"
}
```

**Status:** Not yet implemented (requires database integration in Phase 2)

---

### Get Knowledge Statistics

Retrieve cross-feature knowledge sharing statistics.

**Endpoint:** `GET /api/v1/learning/knowledge/stats`

**Response:**
```json
{
  "total_shared": 0,
  "by_feature": {},
  "success_rate": 0.0,
  "avg_confidence": 0.0,
  "note": "Cross-feature knowledge service requires database integration (Phase 2)"
}
```

**Status:** Not yet implemented (requires database integration in Phase 2)

---

## Health Check

### System Health

Check learning system health status.

**Endpoint:** `GET /api/v1/learning/health`

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "learning_loop": "available",
    "cross_feature_knowledge": "pending_phase_2"
  },
  "note": "Cross-feature knowledge requires database integration (Phase 2)"
}
```

**Service Status Values:**
- `available` - Service is operational
- `pending_phase_2` - Service requires database integration
- `unavailable` - Service is not operational

---

## User Preferences

Users can control learning behavior through preferences. See User Preferences API *(proposed; doc TBD)* for full reference.

### Learning Preference Keys

| Preference Key | Type | Default | Description |
|----------------|------|---------|-------------|
| `learning_enabled` | boolean | `true` | Enable/disable pattern learning |
| `learning_min_confidence` | float | `0.5` | Minimum confidence for pattern application (0.0-1.0) |
| `learning_features` | array | `[]` | List of features enabled for learning |

**Example - Get Learning Preferences:**
```bash
curl -X GET "http://localhost:8001/api/v1/preferences/learning_enabled?user_id=user_123" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Example - Set Minimum Confidence:**
```bash
curl -X POST "http://localhost:8001/api/v1/preferences/learning_min_confidence" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "value": 0.7
  }'
```

---

## Error Handling

All endpoints follow standard error response format:

```json
{
  "detail": "Error message describing what went wrong",
  "error_id": "ERROR_CODE_IDENTIFIER"
}
```

### Common Error Codes

| Error Code | HTTP Status | Description |
|------------|-------------|-------------|
| `PATTERN_RETRIEVAL_ERROR` | 500 | Failed to retrieve patterns |
| `INVALID_PATTERN_TYPE` | 400 | Invalid pattern type provided |
| `INVALID_PATTERN_DATA` | 400 | Invalid pattern data structure |
| `PATTERN_LEARNING_ERROR` | 500 | Failed to learn pattern |
| `PATTERN_NOT_FOUND` | 404 | Pattern ID not found |
| `INVALID_PATTERN_APPLICATION` | 400 | Invalid pattern application context |
| `PATTERN_APPLICATION_ERROR` | 500 | Failed to apply pattern |
| `INVALID_FEEDBACK_DATA` | 400 | Invalid feedback structure |
| `FEEDBACK_RECORDING_ERROR` | 500 | Failed to record feedback |
| `ANALYTICS_RETRIEVAL_ERROR` | 500 | Failed to retrieve analytics |
| `SERVICE_NOT_AVAILABLE` | 400 | Service requires Phase 2 database integration |

---

## Usage Patterns

### Pattern Learning Flow

1. **Learn from Success:**
   ```javascript
   // After successful query
   POST /api/v1/learning/patterns
   {
     "pattern_type": "query_pattern",
     "source_feature": "user_search",
     "pattern_data": {"query": "find active projects"},
     "initial_confidence": 0.7
   }
   ```

2. **Retrieve Relevant Patterns:**
   ```javascript
   // Before similar operation
   GET /api/v1/learning/patterns?source_feature=user_search&min_confidence=0.7
   ```

3. **Apply Pattern:**
   ```javascript
   // Use learned optimization
   POST /api/v1/learning/patterns/apply
   {
     "pattern_id": "query_pattern_user_search_20251020_120000",
     "context": {"current_query": "show active projects"}
   }
   ```

4. **Provide Feedback:**
   ```javascript
   // After pattern application
   POST /api/v1/learning/feedback
   {
     "pattern_id": "query_pattern_user_search_20251020_120000",
     "success": true,
     "feedback": "Improved query speed by 40%"
   }
   ```

### Monitoring Learning Effectiveness

```javascript
// Regular analytics checks
GET /api/v1/learning/analytics

// Response analysis
{
  "total_patterns": 150,
  "average_confidence": 0.82,  // Good: trending up
  "total_feedback": 300,        // Active: 2:1 feedback ratio
  "recent_patterns_24h": 15     // Healthy: consistent learning
}
```

---

## Privacy & Security

**What We Learn:**
- Query patterns and optimizations
- Workflow sequences and frequencies
- Response patterns for common tasks
- User preference patterns

**What We DON'T Learn:**
- Personally identifiable information (PII)
- Message contents beyond structure
- User credentials or tokens
- Private project data

**Data Retention:**
- Patterns are stored indefinitely for continuous improvement
- Feedback is retained for pattern confidence calculation
- Users can request pattern deletion via preference settings

**Access Control:**
- All endpoints require JWT authentication
- Users can only access their own patterns
- Admin users can access aggregated analytics

---

## Rate Limiting

| Endpoint Type | Rate Limit | Window |
|---------------|------------|--------|
| Pattern Retrieval | 100 requests | 1 minute |
| Pattern Learning | 50 requests | 1 minute |
| Feedback Submission | 100 requests | 1 minute |
| Analytics | 20 requests | 1 minute |

Exceeding rate limits returns `429 Too Many Requests`.

---

## Changelog

### Version 1.3 (October 20, 2025)
- **CORE-LEARN-D**: Workflow Optimization System (Sprint A5 Finale)
- Wired Chain-of-Draft experiment system as workflow optimizer
- Added `optimize_workflow_via_experiments()` method for A/B testing
- Added `create_workflow_template_from_pattern()` for template creation
- Automatic pattern learning from workflows with ≥5% improvement
- Template creation from high-confidence patterns (≥0.8)
- Quality assessment: multi-factor scoring (performance, success, decomposition, distribution)
- Created 5 integration tests for workflow optimization
- Added comprehensive Workflow Optimization documentation section
- All existing functionality preserved (backward compatible)
- 96% leverage ratio (3,579 lines existing / 150 lines new)

### Version 1.2 (October 20, 2025)
- **CORE-LEARN-C**: Preference Learning System
- Wired USER_PREFERENCE_PATTERN to UserPreferenceManager
- Added `apply_preference_pattern()` for automatic preference application
- Implemented implicit→explicit preference conversion (confidence ≥ 0.7)
- Added preference hierarchy (Session > User > Global)
- Added conflict resolution (Explicit > Implicit > Historical)
- Created 5 integration tests for preference learning
- Added comprehensive Preference Learning documentation section
- All existing functionality preserved (backward compatible)

### Version 1.1 (October 20, 2025)
- **CORE-LEARN-B**: Extended pattern recognition
- Added 3 new pattern types: `temporal_pattern`, `communication_pattern`, `error_pattern`
- 8 total pattern types (60% overachievement vs 5 required)
- Pattern Types documentation section added
- All existing functionality preserved (backward compatible)

### Version 1.0 (October 20, 2025)
- Initial release
- Pattern management endpoints
- Feedback system
- Learning analytics
- User preferences integration
- Cross-feature knowledge placeholders (Phase 2)

---

## Support

**Issues & Bugs:** [GitHub Issues](https://github.com/your-org/piper-morgan/issues)
**Documentation:** [API Reference Index](./index.md)
**Source Code:** `web/api/routes/learning.py`

---

**Generated with [Claude Code](https://claude.com/claude-code)**
**Last Updated:** October 20, 2025
**Status:** Production Ready ✅
