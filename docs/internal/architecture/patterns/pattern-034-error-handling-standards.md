# Error Handling Standards

**Status**: ✅ Active
**Applies To**: All API endpoints
**Effective**: October 16, 2025
**Related Issue**: #215 (CORE-ERROR-STANDARDS)
**Pattern Number**: 034 (next in sequence)

---

## Overview

All API endpoints MUST return appropriate HTTP status codes for errors. The response body format remains consistent for backward compatibility.

**Core Principle**: HTTP status codes MUST accurately reflect the outcome of the request. Never return 200 OK for error conditions.

---

## HTTP Status Code Standards

### 200 OK ✅ Success Only

**Use For**: Successful operations only

**Response Format**:
```json
{
    "status": "success",
    "data": { ... }
}
```

**Never use 200 for errors** - this violates REST principles and breaks HTTP client error handling.

---

### 400 Bad Request

**Use For**: Malformed request syntax

**Examples**:
- Invalid JSON syntax
- Missing required headers
- Malformed URL parameters
- Wrong content-type

**Response Format**:
```json
{
    "status": "error",
    "code": "BAD_REQUEST",
    "message": "Request syntax is malformed",
    "details": {
        "issue": "Invalid JSON: unexpected token at line 5"
    }
}
```

**Implementation**:
```python
from web.utils.error_responses import bad_request_error

return bad_request_error(
    "Invalid JSON",
    {"issue": "Syntax error at line 5"}
)
```

---

### 422 Unprocessable Entity

**Use For**: Syntactically valid but semantically invalid

**Examples**:
- Empty required fields
- Invalid field values
- Business rule violations
- Type mismatches

**Response Format**:
```json
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
        "field": "intent",
        "issue": "Cannot be empty"
    }
}
```

**Implementation**:
```python
from web.utils.error_responses import validation_error

if not data.get("intent"):
    return validation_error(
        "Required field missing",
        {"field": "intent", "issue": "Cannot be empty"}
    )
```

---

### 404 Not Found

**Use For**: Resource doesn't exist

**Examples**:
- Workflow ID not found
- User ID not found
- Unknown endpoint

**Response Format**:
```json
{
    "status": "error",
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {
        "resource": "workflow",
        "id": "12345"
    }
}
```

**Implementation**:
```python
from web.utils.error_responses import not_found_error

return not_found_error(
    "Workflow not found",
    {"resource": "workflow", "id": workflow_id}
)
```

---

### 500 Internal Server Error

**Use For**: Unexpected server errors

**Examples**:
- Unhandled exceptions
- Service failures
- Database errors
- Service unavailable

**Response Format**:
```json
{
    "status": "error",
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "details": {
        "error_id": "uuid-for-log-correlation"
    }
}
```

**Implementation**:
```python
from web.utils.error_responses import internal_error
import logging

logger = logging.getLogger(__name__)

try:
    # operation
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return internal_error()  # Never expose details to client
```

**CRITICAL**: Never expose stack traces or internal details in 500 errors.

---

### 502 Bad Gateway / 503 Service Unavailable

**Use For**: Backend/upstream service issues

**502 Bad Gateway**:
- Invalid response from upstream server
- Backend returned error

**503 Service Unavailable**:
- Backend temporarily down
- Maintenance mode
- Rate limiting

**Implementation**:
```python
try:
    response = await http_client.get(backend_url)
except Exception as e:
    logger.error(f"Backend unavailable: {e}")
    return internal_error("Backend service unavailable")
```

---

## Error Codes Enumeration

Location: `web/utils/error_responses.py`

```python
from enum import Enum

class ErrorCode(str, Enum):
    """Standard error codes for API responses."""
    BAD_REQUEST = "BAD_REQUEST"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
```

**Extensibility**: Add new codes as needed for specific error types.

---

## Implementation Guidelines

### 1. Using Error Utilities

**Always use utility functions** from `web/utils/error_responses.py`:

```python
from web.utils.error_responses import (
    bad_request_error,
    validation_error,
    not_found_error,
    internal_error
)

@app.post("/api/v1/endpoint")
async def endpoint(request: Request):
    try:
        data = await request.json()

        # Validation
        if not data.get("required_field"):
            return validation_error(
                "Required field missing",
                {"field": "required_field", "issue": "Cannot be empty"}
            )

        # Process...
        result = process_data(data)
        return {"status": "success", "data": result}

    except ValueError as e:
        # Bad input
        return validation_error(str(e))
    except Exception as e:
        # Unexpected error
        logger.error(f"Endpoint error: {e}", exc_info=True)
        return internal_error()
```

### 2. Logging Errors

**Always log errors** with appropriate level:

```python
import logging
logger = logging.getLogger(__name__)

# Validation errors: INFO or WARNING
logger.warning(f"Validation failed: {field}")

# Internal errors: ERROR with stack trace
logger.error(f"Unexpected error: {e}", exc_info=True)
```

### 3. Error Response Consistency

All error responses MUST include:
- `status`: Always "error"
- `code`: Error code from ErrorCode enum
- `message`: User-friendly message
- `details`: Optional additional information (dict)

### 4. Sanitizing Error Details

**Never expose**:
- Stack traces
- Internal file paths
- Database schemas
- API keys or credentials
- System configuration details

**Safe to expose**:
- User-provided input (sanitized)
- Field names
- Validation rules
- Public error codes

---

## Migration from 200-with-error Pattern

### Old Pattern (Deprecated)

```python
try:
    result = operation()
    return result
except Exception as e:
    return {"status": "error", "error": str(e)}  # Returns 200!
```

**Problems**:
- Violates REST principles
- Breaks HTTP client error handling
- Confuses monitoring tools
- Makes debugging harder

### New Pattern (Required)

```python
try:
    result = operation()
    return result
except ValueError as e:
    # Semantic/validation error
    return validation_error(str(e))  # Returns 422
except Exception as e:
    # Unexpected error
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return internal_error()  # Returns 500
```

**Benefits**:
- REST-compliant
- HTTP clients handle errors correctly
- Monitoring tools work properly
- Clear error semantics

---

## Backward Compatibility

**Response Format**: ✅ UNCHANGED
- `{"status": "error", ...}` format maintained
- Existing parsers continue to work
- Only HTTP status code changes

**Breaking Change**: ❌ HTTP Status Codes
- Old: Always 200 (even for errors)
- New: Proper codes (422, 500, etc.)

**Impact on Clients**:
- Must check `response.status_code` first
- Most HTTP clients handle this automatically
- Update tests to expect proper status codes

**Migration Guide**:

Old client code:
```python
response = requests.post(url, json=data)
if response.json().get("status") == "error":
    handle_error()
```

New client code (better):
```python
response = requests.post(url, json=data)
if response.status_code != 200:
    handle_error()
elif response.json().get("status") == "error":
    # Defensive check (should not happen with proper implementation)
    handle_error()
```

---

## Testing Requirements

### Unit Tests

Test each error path:

```python
def test_endpoint_validation_error():
    """Test endpoint returns 422 for invalid input."""
    response = client.post("/api/v1/endpoint", json={"invalid": "data"})

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert response.json()["code"] == "VALIDATION_ERROR"
```

### Integration Tests

Test error responses end-to-end:

```python
def test_endpoint_error_format():
    """Test error response format is consistent."""
    response = client.post("/api/v1/endpoint", json={})

    # Check status code
    assert response.status_code in [400, 422, 500]

    # Check required fields
    body = response.json()
    assert "status" in body
    assert body["status"] == "error"
    assert "code" in body
    assert "message" in body
```

---

## Examples by Endpoint Type

### Intent Endpoint

```python
@app.post("/api/v1/intent")
async def process_intent(request: Request):
    try:
        data = await request.json()
        message = data.get("message", "")

        # Validation
        if not message:
            return validation_error(
                "Message required",
                {"field": "message", "issue": "Cannot be empty"}
            )

        # Service unavailable
        if intent_service is None:
            return internal_error("Intent service unavailable")

        # Process
        result = await intent_service.process_intent(message)

        # Service returned error
        if result.error:
            return validation_error(
                result.error,
                {"error_type": result.error_type}
            )

        return {"status": "success", "data": result}

    except Exception as e:
        logger.error(f"Intent processing error: {e}", exc_info=True)
        return internal_error()
```

### Resource Endpoint

```python
@app.get("/api/v1/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    try:
        workflow = await workflow_service.get(workflow_id)

        if not workflow:
            return not_found_error(
                "Workflow not found",
                {"resource": "workflow", "id": workflow_id}
            )

        return {"status": "success", "data": workflow}

    except Exception as e:
        logger.error(f"Workflow retrieval error: {e}", exc_info=True)
        return internal_error()
```

### Proxy Endpoint

```python
@app.get("/api/proxy/external")
async def proxy_endpoint():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            return response.json()
    except httpx.ConnectError:
        logger.error("Backend connection failed")
        return internal_error("Backend service unavailable")
    except Exception as e:
        logger.error(f"Proxy error: {e}", exc_info=True)
        return internal_error()
```

---

## Decision Log

### Why 422 instead of 400 for validation?

**400 Bad Request**: Syntax errors (invalid JSON, missing headers)
**422 Unprocessable Entity**: Semantic errors (empty fields, invalid values)

This distinction helps clients understand whether to:
- Fix request format (400)
- Fix request content (422)

### Why standardize error format?

**Consistency**: All errors follow same structure
**Parsing**: Clients can parse errors uniformly
**Monitoring**: Tools can detect patterns
**Debugging**: Clear error identification

### Why not use FastAPI's built-in validation?

**We will**: For request models
**This handles**: Business logic errors, service errors, unexpected exceptions

Both approaches complement each other.

---

## Related Patterns

- **Pattern 007**: Async Error Handling
- **Pattern 014**: Error Handling API Contract
- **Pattern 017**: Background Task Error Handling

---

## References

- [RFC 7231 - HTTP/1.1 Semantics](https://tools.ietf.org/html/rfc7231)
- [RFC 7807 - Problem Details for HTTP APIs](https://tools.ietf.org/html/rfc7807)
- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)

---

**Document Owner**: Lead Developer
**Last Updated**: October 16, 2025
**Review Date**: Sprint A3
**Status**: Active (Effective October 16, 2025)
