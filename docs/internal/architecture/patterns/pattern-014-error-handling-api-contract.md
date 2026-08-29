# Pattern-014: Error Handling Pattern (API Contract)

## Status

**Proven**

## Context

Web APIs need consistent, actionable error responses that follow RESTful principles and give users clear guidance on resolution. Without systematic error handling, applications provide inconsistent error formats, expose internal implementation details, and frustrate users with unhelpful error messages. The Error Handling Pattern addresses:

- What challenges does this solve? Provides consistent, user-friendly error responses with clear resolution guidance
- When should this pattern be considered? When building APIs that need professional error handling and user experience
- What are the typical scenarios where this applies? REST APIs, user-facing applications, service integrations, validation errors

## Pattern Description

The Error Handling Pattern creates centralized error handling that converts domain exceptions into consistent API responses with both technical details for debugging and user-friendly messages for resolution guidance.

Core concept:

- Centralized error handler maps exceptions to responses
- Consistent error response contract across all endpoints
- User-friendly messages with actionable guidance
- Proper HTTP status codes for different error types

## Implementation

### Centralized Error Handler

```python
from fastapi import JSONResponse
from typing import Dict, Type

class APIErrorHandler:
    """Centralized error handling for consistent responses"""

    ERROR_MESSAGES = {
        ProjectNotFoundError: "I couldn't find that project. Try 'list projects' to see available options.",
        AmbiguousProjectError: "Multiple projects match your request. Please be more specific.",
        GitHubAPIError: "GitHub is temporarily unavailable. Please try again in a few moments.",
        InsufficientContextError: "I need more information to complete this task. {details}"
    }

    @staticmethod
    def handle_error(error: Exception) -> JSONResponse:
        """Convert exceptions to user-friendly API responses"""
        if isinstance(error, ProjectNotFoundError):
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "error": {
                        "code": "PROJECT_NOT_FOUND",
                        "message": "The specified project does not exist",
                        "user_message": APIErrorHandler.ERROR_MESSAGES[ProjectNotFoundError],
                        "details": {"project_id": error.project_id}
                    }
                }
            )
        elif isinstance(error, ValidationError):
            return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": str(error),
                        "field": getattr(error, 'field', None)
                    }
                }
            )
        else:
            # Generic error with safe message
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                        "user_message": "Something went wrong. Please try again or contact support."
                    }
                }
            )
```

### API Endpoint Integration

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/api/v1/intent")
async def process_intent(request: IntentRequest):
    try:
        result = await intent_service.process(request)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return APIErrorHandler.handle_error(e)

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    try:
        project = await project_service.get_by_id(project_id)
        return {"status": "success", "data": project}
    except Exception as e:
        return APIErrorHandler.handle_error(e)
```

### Domain Exception Classes

```python
class DomainException(Exception):
    """Base class for domain-specific exceptions"""

    def __init__(self, message: str, details: Dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class ProjectNotFoundError(DomainException):
    """Raised when project cannot be found"""

    def __init__(self, project_id: str):
        self.project_id = project_id
        super().__init__(f"Project {project_id} not found", {"project_id": project_id})

class AmbiguousProjectError(DomainException):
    """Raised when multiple projects match criteria"""

    def __init__(self, criteria: str, matches: List[str]):
        self.criteria = criteria
        self.matches = matches
        super().__init__(f"Multiple projects match '{criteria}'", {
            "criteria": criteria,
            "matches": matches
        })

class ValidationError(DomainException):
    """Raised for business rule validation failures"""

    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(message, {"field": field})
```

## Usage Guidelines

### Error Response Contract

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Technical error message",
    "user_message": "User-friendly guidance",
    "field": "field_name (if applicable)",
    "details": {
      /* optional context */
    }
  }
}
```

### Status Code Guidelines

| Code | Usage               | Example                                        |
| ---- | ------------------- | ---------------------------------------------- |
| 200  | Success             | Request completed successfully                 |
| 400  | Bad Request         | Invalid JSON format or missing required fields |
| 404  | Not Found           | Project, workflow, or resource doesn't exist   |
| 422  | Validation Error    | Valid format but business rules violated       |
| 429  | Rate Limited        | Too many requests from client                  |
| 500  | Server Error        | Unexpected internal error                      |
| 502  | Service Unavailable | External service (GitHub, Claude) unavailable  |

### User Message Guidelines

- **Actionable**: Tell users what they can do to resolve the issue
- **Contextual**: Reference the specific situation (project names, etc.)
- **Helpful**: Suggest alternatives or next steps
- **Consistent**: Use the same tone and terminology across errors

### Error Handling Best Practices

- Always include both technical and user-friendly messages
- Log technical details separately for debugging
- Never expose internal implementation details
- Provide recovery suggestions when possible
- Use appropriate HTTP status codes consistently

## Benefits

- Consistent error experience across all API endpoints
- User-friendly messages with actionable guidance
- Proper separation of technical and user concerns
- Easier debugging with structured error information
- Professional API contract compliance

## Trade-offs

- Additional abstraction layer for error handling
- Need to maintain error message consistency
- Potential information hiding for debugging
- Overhead of centralized error mapping

## Anti-patterns to Avoid

- ❌ Generic "Something went wrong" without guidance
- ❌ Exposing stack traces or internal errors to users
- ❌ Inconsistent error formats across endpoints
- ❌ Wrong HTTP status codes for error types
- ❌ Technical jargon in user-facing messages

## Related Patterns

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Domain exceptions from repository layer
- [Pattern-002: Service Pattern](pattern-002-service.md) - Service layer error handling
- [Pattern-018: Configuration Access Pattern](pattern-018-configuration-access.md) - Configuration error handling

## References

- **Implementation**: Centralized error handling in FastAPI applications
- **Usage Example**: Domain exceptions, HTTP status codes, user message guidance
- **Related ADR**: Error handling framework, API design principles

## Migration Notes

_Consolidated from:_

- `pattern-catalog.md#14-error-handling-pattern-api-contract` - Complete API error handling implementation
- `archive/PATTERN-INDEX-legacy.md#error-handling-pattern` - Graceful degradation with specific error types
- Codebase analysis - Domain exception handling and HTTP response patterns
