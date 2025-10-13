# MVP-ERROR-STANDARDS: Standardize Error Handling Across All Endpoints

## Context
During GREAT-5 validation, inconsistent error handling patterns were discovered. Currently, invalid requests return 200 with error JSON instead of proper HTTP status codes. This works but isn't REST-compliant.

## Current State
- Invalid JSON to intent endpoint: Returns 200 with `{"status":"error", "error":"..."}`
- Some endpoints: Return 422 for validation errors
- Others: Return 400 for bad requests
- No consistent pattern across the system

## Scope

### 1. Define Error Standards
Establish clear standards for all error types:
- **200**: Success only (with success JSON)
- **400**: Bad request (malformed syntax)
- **422**: Validation error (syntactically correct but semantically invalid)
- **404**: Resource not found
- **500**: Server error (with graceful degradation)

### 2. Audit All Endpoints
Find all error responses across:
- Intent endpoints
- API endpoints
- Health checks
- Admin endpoints
- Plugin endpoints

### 3. Standardize Responses
Update all endpoints to follow standards:
```python
# Standard error response format
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "User-friendly message",
    "details": {
        "field": "specific_field",
        "issue": "specific_problem"
    }
}
```

### 4. Update Tests
Fix tests expecting old behavior:
- Update status code expectations
- Verify error response format
- Ensure graceful degradation (no 500 crashes)

## Acceptance Criteria
- [ ] Error standards documented in ADR or pattern
- [ ] All endpoints audited and listed
- [ ] All endpoints follow standards
- [ ] Tests updated for new behavior
- [ ] No 500 errors leak stack traces
- [ ] Client documentation updated

## Success Validation
```bash
# Test various error conditions
curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"invalid": "json structure"}'
# Should return 422, not 200

# Verify all endpoints
python scripts/test_error_standards.py
# All endpoints return correct status codes

# Check for stack trace leaks
python scripts/security_check.py
# No internal details in error responses
```

## Time Estimate
1-2 days

## Priority
Medium - Important for API consumers but not blocking alpha

## Notes
- Keep backward compatibility where possible
- Document breaking changes clearly
- Consider versioning if significant changes
- Production cache and functionality work perfectly - this is just standardization

---

**Trigger**: Implement before first external API consumer
