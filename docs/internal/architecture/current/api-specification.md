# Piper Morgan 1.0 - API Design Specification

## Overview

This document defines the API contracts for Piper Morgan, including REST endpoints, WebSocket events, request/response formats, and error handling patterns. The API follows RESTful principles with a focus on clarity and consistency.

## Base Configuration

### API Version

- Base URL: `http://localhost:8001/api/v1`
- Version: 1.0
- Format: JSON

### Authentication

- **Development**: API key in environment variables
- **Production**: Bearer token authentication (planned)
- **Headers**:
  ```
  Authorization: Bearer <token>
  Content-Type: application/json
  ```

## REST Endpoints

### 1. Intent Processing

#### POST `/api/v1/intent`

Process natural language input and execute appropriate action.

**Request:**

```json
{
  "message": "Create a bug ticket for the mobile login crash",
  "session_id": "optional-session-uuid",
  "context": {
    "project_id": "optional-explicit-project-id"
  }
}
```

**Response (Command - Workflow Created):**

```json
{
  "status": "success",
  "intent": {
    "id": "intent-uuid",
    "category": "execution",
    "action": "create_github_issue",
    "confidence": 0.95,
    "context": {
      "project_id": "proj-123",
      "project_name": "Mobile App",
      "repository": "org/mobile-app",
      "original_message": "Create a bug ticket for the mobile login crash"
    }
  },
  "workflow": {
    "id": "workflow-uuid",
    "type": "create_ticket",
    "status": "pending"
  },
  "response": "I'll create a GitHub issue for the mobile login crash. This will be added to the Mobile App repository.",
  "needs_project_confirmation": false
}
```

**Response (Query - Direct Data):**

```json
{
  "status": "success",
  "intent": {
    "id": "intent-uuid",
    "category": "query",
    "action": "list_projects",
    "confidence": 0.98
  },
  "data": {
    "projects": [
      {
        "id": "proj-123",
        "name": "Mobile App",
        "description": "iOS and Android applications",
        "is_default": false,
        "integrations": {
          "github": {
            "repository": "org/mobile-app",
            "enabled": true
          }
        }
      },
      {
        "id": "proj-456",
        "name": "Web Platform",
        "description": "Main web application",
        "is_default": true,
        "integrations": {
          "github": {
            "repository": "org/web-platform",
            "enabled": true
          },
          "jira": {
            "project": "WEB",
            "enabled": true
          }
        }
      }
    ]
  },
  "response": "You have 2 active projects: Mobile App and Web Platform (default)."
}
```

**Response (Clarification Needed):**

```json
{
  "status": "clarification_needed",
  "intent": {
    "id": "intent-uuid",
    "category": "execution",
    "action": "create_ticket",
    "confidence": 0.65
  },
  "clarification": {
    "type": "ambiguous_project",
    "message": "I found multiple projects that could match. Which project should I create the ticket in?",
    "options": [
      {
        "id": "proj-123",
        "name": "Mobile App",
        "description": "iOS and Android applications"
      },
      {
        "id": "proj-789",
        "name": "Mobile Web",
        "description": "Responsive web version"
      }
    ]
  },
  "response": "I need clarification about which project to use. You mentioned 'mobile' which could refer to either the Mobile App or Mobile Web project."
}
```

### 2. Workflow Management

#### GET `/api/v1/workflows/{workflow_id}`

Get workflow status and details.

**Response:**

```json
{
  "id": "workflow-uuid",
  "type": "create_ticket",
  "status": "completed",
  "created_at": "2025-06-19T10:30:00Z",
  "completed_at": "2025-06-19T10:30:15Z",
  "tasks": [
    {
      "id": "task-1",
      "type": "analyze_request",
      "status": "completed",
      "started_at": "2025-06-19T10:30:01Z",
      "completed_at": "2025-06-19T10:30:05Z"
    },
    {
      "id": "task-2",
      "type": "github_create_issue",
      "status": "completed",
      "started_at": "2025-06-19T10:30:06Z",
      "completed_at": "2025-06-19T10:30:15Z",
      "output": {
        "issue_number": 123,
        "issue_url": "https://github.com/org/mobile-app/issues/123",
        "repository": "org/mobile-app"
      }
    }
  ],
  "result": {
    "success": true,
    "message": "Created issue #123 in mobile-app repository",
    "data": {
      "issue_url": "https://github.com/org/mobile-app/issues/123",
      "issue_number": 123,
      "repository": "org/mobile-app"
    }
  }
}
```

#### GET `/api/v1/workflows`

List recent workflows.

**Query Parameters:**

- `limit` (default: 20, max: 100)
- `offset` (default: 0)
- `status` (optional: pending, running, completed, failed)

**Response:**

```json
{
  "workflows": [
    {
      "id": "workflow-uuid-1",
      "type": "create_ticket",
      "status": "completed",
      "created_at": "2025-06-19T10:30:00Z",
      "summary": "Created GitHub issue #123"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### 3. Project Management

#### GET `/api/v1/projects`

List all active projects.

**Response:**

```json
{
  "projects": [
    {
      "id": "proj-123",
      "name": "Mobile App",
      "description": "iOS and Android applications",
      "is_default": false,
      "is_archived": false,
      "integrations": {
        "github": {
          "repository": "org/mobile-app",
          "enabled": true
        }
      },
      "created_at": "2025-01-15T09:00:00Z"
    }
  ],
  "total": 3
}
```

#### GET `/api/v1/projects/{project_id}`

Get specific project details.

**Response:**

```json
{
  "id": "proj-123",
  "name": "Mobile App",
  "description": "iOS and Android applications",
  "vision": "Best-in-class mobile experience",
  "strategy": "Focus on user engagement and performance",
  "is_default": false,
  "is_archived": false,
  "integrations": {
    "github": {
      "repository": "org/mobile-app",
      "default_labels": ["mobile", "app"],
      "enabled": true
    }
  },
  "metrics": {
    "active_features": 12,
    "open_work_items": 34,
    "stakeholders": 8
  },
  "created_at": "2025-01-15T09:00:00Z",
  "updated_at": "2025-06-18T14:22:00Z"
}
```

### 4. Knowledge Base

#### POST `/api/v1/knowledge/upload`

Upload documents to knowledge base.

**Request (multipart/form-data):**

```
file: <binary data>
metadata: {
  "title": "Q2 Product Strategy",
  "type": "strategy_document",
  "tags": ["strategy", "q2", "roadmap"]
}
```

**Response:**

```json
{
  "status": "success",
  "document": {
    "id": "doc-uuid",
    "filename": "q2-strategy.pdf",
    "title": "Q2 Product Strategy",
    "size_bytes": 2048576,
    "chunks_created": 42,
    "processing_time_ms": 3500
  },
  "message": "Document successfully ingested into knowledge base"
}
```

#### POST `/api/v1/knowledge/search`

Search knowledge base.

**Request:**

```json
{
  "query": "mobile app performance metrics",
  "limit": 5,
  "filters": {
    "type": "strategy_document",
    "date_range": {
      "start": "2025-01-01",
      "end": "2025-06-30"
    }
  }
}
```

**Response:**

```json
{
  "results": [
    {
      "document_id": "doc-123",
      "title": "Mobile Performance KPIs",
      "excerpt": "...app launch time should be under 2 seconds...",
      "relevance_score": 0.89,
      "metadata": {
        "type": "metrics_document",
        "created_at": "2025-03-15T10:00:00Z"
      }
    }
  ],
  "total_results": 3,
  "query_time_ms": 125
}
```

### 5. Analytics & Reporting

#### GET `/api/v1/analytics/usage`

Get system usage analytics.

**Query Parameters:**

- `period` (day, week, month)
- `start_date` (ISO date)
- `end_date` (ISO date)

**Response:**

```json
{
  "period": "week",
  "start_date": "2025-06-12",
  "end_date": "2025-06-19",
  "metrics": {
    "total_intents": 234,
    "successful_workflows": 198,
    "failed_workflows": 12,
    "average_response_time_ms": 2150,
    "most_common_actions": [
      {
        "action": "create_ticket",
        "count": 89
      },
      {
        "action": "list_projects",
        "count": 56
      }
    ],
    "user_satisfaction": 4.3
  }
}
```

## WebSocket API

### Connection

```
ws://localhost:8001/ws
```

### Authentication

Send auth message after connection:

```json
{
  "type": "auth",
  "token": "your-auth-token"
}
```

### Event Types

#### Workflow Updates

```json
{
  "type": "workflow.task_started",
  "timestamp": "2025-06-19T10:30:01Z",
  "data": {
    "workflow_id": "workflow-uuid",
    "task_id": "task-uuid",
    "task_type": "analyze_request"
  }
}
```

```json
{
  "type": "workflow.task_completed",
  "timestamp": "2025-06-19T10:30:05Z",
  "data": {
    "workflow_id": "workflow-uuid",
    "task_id": "task-uuid",
    "task_type": "analyze_request",
    "result": {
      "success": true
    }
  }
}
```

```json
{
  "type": "workflow.completed",
  "timestamp": "2025-06-19T10:30:15Z",
  "data": {
    "workflow_id": "workflow-uuid",
    "status": "completed",
    "result": {
      "success": true,
      "message": "Created issue #123",
      "issue_url": "https://github.com/org/repo/issues/123"
    }
  }
}
```

#### System Events

```json
{
  "type": "system.knowledge_update",
  "timestamp": "2025-06-19T11:00:00Z",
  "data": {
    "documents_added": 3,
    "total_documents": 156
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "error": {
    "code": "PROJECT_NOT_FOUND",
    "message": "The specified project does not exist",
    "details": {
      "project_id": "invalid-id"
    },
    "user_message": "I couldn't find that project. Try 'list projects' to see available options."
  },
  "request_id": "req-uuid"
}
```

### Error Codes

| Code                           | HTTP Status | Description                           |
| ------------------------------ | ----------- | ------------------------------------- |
| `INVALID_REQUEST`              | 400         | Request validation failed             |
| `UNAUTHORIZED`                 | 401         | Missing or invalid authentication     |
| `FORBIDDEN`                    | 403         | Insufficient permissions              |
| `NOT_FOUND`                    | 404         | Resource not found                    |
| `PROJECT_NOT_FOUND`            | 404         | Specified project doesn't exist       |
| `WORKFLOW_NOT_FOUND`           | 404         | Specified workflow doesn't exist      |
| `AMBIGUOUS_REQUEST`            | 400         | Request needs clarification           |
| `INTENT_CLASSIFICATION_FAILED` | 500         | Could not classify intent             |
| `EXTERNAL_SERVICE_ERROR`       | 502         | GitHub/Jira/etc API error             |
| `GITHUB_RATE_LIMITED`          | 429         | GitHub API rate limit exceeded        |
| `GITHUB_REPO_NOT_FOUND`        | 404         | Specified GitHub repository not found |
| `GITHUB_ISSUE_CREATION_FAILED` | 502         | Failed to create GitHub issue         |
| `RATE_LIMITED`                 | 429         | Too many requests                     |
| `INTERNAL_ERROR`               | 500         | Unexpected server error               |

### Rate Limiting

**Headers:**

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1623456789
```

**Rate Limit Exceeded Response:**

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMITED",
    "message": "Rate limit exceeded",
    "retry_after_seconds": 300
  }
}
```

## Pagination

Standard pagination for list endpoints:

**Request Parameters:**

- `limit` - Number of items (default: 20, max: 100)
- `offset` - Starting position (default: 0)
- `sort` - Sort field (varies by endpoint)
- `order` - Sort order (asc/desc)

**Response Format:**

```json
{
  "data": [...],
  "pagination": {
    "total": 156,
    "limit": 20,
    "offset": 40,
    "has_more": true
  }
}
```

## Content Types

### Request Content Types

- `application/json` - Default for all endpoints
- `multipart/form-data` - File uploads only

### Response Content Types

- `application/json` - All responses

## API Versioning

- Version included in URL path: `/api/v1/`
- Breaking changes require new version
- Deprecation notices via headers:
  ```
  X-API-Deprecation-Date: 2025-12-31
  X-API-Deprecation-Info: Use /api/v2/intent instead
  ```

## Health Check

#### GET `/health/`

Basic health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-07-30T10:00:00Z",
  "environment": "staging"
}
```

#### GET `/health/liveness`

Kubernetes-style liveness probe.

**Response:**

```json
{
  "status": "alive",
  "timestamp": "2025-07-30T10:00:00Z"
}
```

#### GET `/health/readiness`

Kubernetes-style readiness probe with database connectivity check.

**Response (Ready):**

```json
{
  "status": "ready",
  "timestamp": "2025-07-30T10:00:00Z"
}
```

**Response (Not Ready):**

HTTP 503 Service Unavailable

```json
{
  "detail": "Not ready: Database connection failed"
}
```

#### GET `/health/comprehensive`

Comprehensive health check for all system components.

**Response (Healthy):**

```json
{
  "overall_status": "healthy",
  "timestamp": "2025-07-30T10:00:00Z",
  "environment": "staging",
  "version": "PM-038-staging",
  "components": {
    "database": {
      "status": "healthy",
      "response_time_ms": 12.5,
      "total_connections": 5,
      "active_connections": 2,
      "table_count": 15,
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 8.3,
      "connected_clients": 3,
      "used_memory_human": "2.5M",
      "redis_version": "7.0.0",
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "chromadb": {
      "status": "healthy",
      "response_time_ms": 45.2,
      "heartbeat": {"nanosecond heartbeat": 1690789200123456789},
      "collection_count": 2,
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "mcp_integration": {
      "status": "healthy",
      "total_response_time_ms": 320.5,
      "tests": {
        "resource_count": 5,
        "search_response_time_ms": 250.2,
        "search_results_count": 12,
        "connection_stats": {"using_pool": true},
        "performance_target_met": true
      },
      "pm038_features": {
        "connection_pooling": true,
        "content_search": true,
        "performance_target": "< 500ms",
        "actual_performance": "250.2ms"
      },
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "slack_integration": {
      "status": "healthy",
      "checks": {
        "slack_token_configured": true,
        "slack_api_reachable": true,
        "workspace_info": {
          "team": "Piper Morgan Dev",
          "user": "piper-bot",
          "team_id": "T1234567890"
        },
        "active_background_tasks": 3,
        "task_success_rate": 0.95,
        "stuck_pipelines_count": 0,
        "has_stuck_pipelines": false,
        "meets_slack_timeout": true
      },
      "metrics": {
        "api_response_time_ms": 125.3,
        "recent_success_rate": 0.92,
        "recent_pipeline_count": 8,
        "successful_pipelines": 7,
        "failed_pipelines": 1,
        "avg_processing_time_ms": 1850.5,
        "total_tasks_created": 45,
        "failed_tasks": 2
      },
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "system_resources": {
      "status": "healthy",
      "cpu_percent": 35.2,
      "memory_percent": 45.8,
      "disk_percent": 22.1,
      "memory_available_gb": 8.5,
      "disk_free_gb": 45.2,
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "api_endpoints": {
      "status": "healthy",
      "total_response_time_ms": 1250.8,
      "healthy_endpoints": "4/4",
      "endpoints": {
        "/api/v1/intent": {
          "status_code": 200,
          "response_time_ms": 450.2,
          "healthy": true
        },
        "/api/v1/files/search": {
          "status_code": 200,
          "response_time_ms": 320.5,
          "healthy": true
        },
        "/health/liveness": {
          "status_code": 200,
          "response_time_ms": 15.3,
          "healthy": true
        },
        "/health/readiness": {
          "status_code": 200,
          "response_time_ms": 25.8,
          "healthy": true
        }
      },
      "timestamp": "2025-07-30T10:00:00Z"
    },
    "external_services": {
      "status": "degraded",
      "reachable_services": "2/3",
      "services": {
        "anthropic": {
          "status_code": 200,
          "response_time_ms": 890.2,
          "reachable": true
        },
        "openai": {
          "status_code": 200,
          "response_time_ms": 1250.8,
          "reachable": true
        },
        "github": {
          "status_code": 0,
          "response_time_ms": 0,
          "reachable": false,
          "error": "Connection timeout"
        }
      },
      "timestamp": "2025-07-30T10:00:00Z"
    }
  },
  "summary": {
    "total_components": 8,
    "healthy_components": 7,
    "degraded_components": 1,
    "unhealthy_components": 0,
    "health_percentage": 87.5
  }
}
```

**Response (Unhealthy):**

HTTP 503 Service Unavailable - Returns same structure with failed components.

#### GET `/health/mcp`

Dedicated MCP (Model Context Protocol) health check.

**Response:**

```json
{
  "status": "healthy",
  "total_response_time_ms": 320.5,
  "tests": {
    "resource_count": 5,
    "search_response_time_ms": 250.2,
    "search_results_count": 12,
    "connection_stats": {"using_pool": true},
    "performance_target_met": true
  },
  "pm038_features": {
    "connection_pooling": true,
    "content_search": true,
    "performance_target": "< 500ms",
    "actual_performance": "250.2ms"
  },
  "timestamp": "2025-07-30T10:00:00Z"
}
```

#### GET `/health/slack`

Dedicated Slack integration health check with pipeline monitoring.

**Response:**

```json
{
  "status": "healthy",
  "checks": {
    "slack_token_configured": true,
    "slack_api_reachable": true,
    "workspace_info": {
      "team": "Piper Morgan Dev",
      "user": "piper-bot",
      "team_id": "T1234567890"
    },
    "active_background_tasks": 3,
    "task_success_rate": 0.95,
    "stuck_pipelines_count": 0,
    "has_stuck_pipelines": false,
    "meets_slack_timeout": true
  },
  "metrics": {
    "api_response_time_ms": 125.3,
    "recent_success_rate": 0.92,
    "recent_pipeline_count": 8,
    "successful_pipelines": 7,
    "failed_pipelines": 1,
    "avg_processing_time_ms": 1850.5,
    "total_tasks_created": 45,
    "failed_tasks": 2
  },
  "timestamp": "2025-07-30T10:00:00Z"
}
```

#### GET `/health/metrics`

Prometheus-compatible health metrics for monitoring integration.

**Response (text/plain):**

```
piper_health_overall{environment="staging"} 1
piper_health_component{component="database",environment="staging"} 1
piper_health_component{component="redis",environment="staging"} 1
piper_health_component{component="slack_integration",environment="staging"} 1
piper_health_response_time_ms{component="database",environment="staging"} 12.5
piper_health_response_time_ms{component="redis",environment="staging"} 8.3
piper_system_cpu_percent{environment="staging"} 35.2
piper_system_memory_percent{environment="staging"} 45.8
piper_system_disk_percent{environment="staging"} 22.1
```

### Health Status Levels

- **healthy**: All systems operational
- **degraded**: Some performance issues but functional
- **unhealthy**: Critical systems down or failing
- **unknown**: Cannot determine status

## Development Tools

### API Documentation

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`
- OpenAPI Schema: `http://localhost:8001/openapi.json`

### Request Examples

#### cURL

```bash
# Create ticket
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a bug ticket for login issue"}'

# Get workflow status
curl http://localhost:8001/api/v1/workflows/workflow-uuid

# List projects
curl http://localhost:8001/api/v1/projects
```

#### Python

```python
import requests

# Create ticket
response = requests.post(
    "http://localhost:8001/api/v1/intent",
    json={"message": "Create a bug ticket for login issue"}
)

# Get workflow status
workflow = requests.get(
    f"http://localhost:8001/api/v1/workflows/{workflow_id}"
).json()

# Example: Check repository in workflow context
print("Repository:", workflow["tasks"][1]["output"].get("repository"))
```

#### JavaScript

```javascript
// Create ticket
const response = await fetch("http://localhost:8001/api/v1/intent", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "Create a bug ticket for login issue" }),
});

// Get workflow status
const workflow = await fetch(
  `http://localhost:8001/api/v1/workflows/${workflowId}`
).then((res) => res.json());
```

---

_Last Updated: June 28, 2025_

## Revision Log

- **June 28, 2025**: Updated API contract for GitHub integration, repository context enrichment, error codes, and health check

## Workflow Context Enrichment

For workflows that require repository context (e.g., GitHub issue creation), the system automatically enriches the context with the repository if available from the project configuration. This enables downstream handlers to create issues in the correct repository without requiring explicit user input.

**Example enriched context:**

```json
{
  "project_id": "proj-123",
  "project_name": "Mobile App",
  "repository": "org/mobile-app",
  "title": "Login fails on iOS",
  "body": "Steps to reproduce...",
  "labels": ["bug", "ios"]
}
```

## UI Response Structure and Feedback (2025)

The Piper Morgan web UI now uses a DDD-compliant, test-driven domain module (`bot-message-renderer.js`) for all bot message rendering and response handling. This ensures:

- Consistent response formatting for all success, error, and progress messages
- Real-time feedback and actionable error messages in the UI
- All UI logic is fully covered by automated tests (TDD)

**Technical Note:**
API responses intended for the UI should provide clear status, message, and error fields. The UI will render these using the unified renderer for a consistent user experience.

### UI Message Services

#### ActionHumanizer Service

Converts technical action strings to natural language with intelligent caching.

- **Purpose**: Transform system action identifiers into user-friendly text
- **Location**: `services/ui_messages/action_humanizer.py`
- **Dependencies**: ActionHumanizationRepository, LLMClient (future)

**Primary Method**:

```python
async def humanize(self, action: str, category: Optional[str] = None) -> str:
    """
    Convert technical action to human-readable format.

    Args:
        action: Technical action string (e.g., "investigate_crash")
        category: Optional intent category for context

    Returns:
        Human-readable string (e.g., "investigate a crash")

    Process:
        1. Check cache for existing humanization
        2. If found, increment usage and return
        3. If not found, apply rule-based conversion
        4. Cache result for future use
    """
```

**Rule-Based Patterns**:

- `verb_noun` → `verb a/an noun` (e.g., create_ticket → create a ticket)
- `verb_compound` → `verb compound` (e.g., analyze_performance → analyze performance)
- Handles articles (a/an) based on noun
- Recognizes common abbreviations (github → GitHub, api → API)

#### TemplateRenderer Service (REMOVED 2026-08-29, #1638)

`services/ui_messages/templates.py` and `personality_templates.py` were deleted per Arch's
2026-08-28 DISPOSE ruling: the `TemplateRenderer` family had zero production callers — its
integration point was `main.py`'s pre-2025-10 chat handler, and the successor rendering path
never picked it up. Recoverable from git history. `ActionHumanizer` (below) remains.

#### Integration with Workflows

Workflow responses now include humanized acknowledgment messages:

```json
{
  "success": true,
  "workflow_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "I'll investigate the crash you reported. Let me analyze this for you.",
  "data": {
    "workflow_type": "GENERATE_REPORT",
    "status": "RUNNING",
    "tasks": [...]
  }
}
```

**Message Generation Flow** (historical — this flow ran through `main.py`'s pre-2025-10 chat
handler and the now-removed TemplateRenderer; current rendering happens in the
`IntentService`/workflow-dispatcher path):

1. Workflow returns technical response
2. Response sent to user with natural language

## PM-039 Canonical Action for Document/File Search

- All document/file search actions (find_documents, search_files, etc.) are normalized to 'search_documents'.
- This unification ensures robust, maintainable, and unified handling of all search intents.
- Supported patterns and typo tolerance are documented in tests/test_intent_coverage_pm039.py.
