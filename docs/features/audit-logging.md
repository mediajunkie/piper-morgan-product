# Audit Logging System

**Issue**: #249 CORE-AUDIT-LOGGING
**Status**: Production Ready
**Version**: 1.0.0

## Overview

The Piper Morgan audit logging system provides comprehensive tracking of security-sensitive operations for compliance, debugging, and security monitoring. Every authentication event, API key operation, and security event is recorded with full context for accountability and forensics.

## Table of Contents

- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Architecture](#architecture)
- [Query Examples](#query-examples)
- [Security Considerations](#security-considerations)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Basic Usage

```python
from services.security.audit_logger import audit_logger, Action, EventType, Severity
from services.database.session_factory import AsyncSessionFactory

async def example():
    async with AsyncSessionFactory.session_scope() as session:
        # Log an authentication event
        await audit_logger.log_auth_event(
            action=Action.LOGIN,
            status="success",
            message="User logged in successfully",
            session=session,
            user_id="user123",
            session_id="session456",
            details={"method": "password", "username": "john"},
            audit_context={
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0...",
                "request_id": "req_789",
                "request_path": "/api/v1/auth/login",
            }
        )
        await session.commit()
```

### In API Routes

```python
from fastapi import Request

def build_audit_context(request: Request) -> Dict[str, Any]:
    """Extract audit context from FastAPI request"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.headers.get("x-request-id"),
        "request_path": str(request.url.path),
    }

@router.post("/logout")
async def logout(request: Request, current_user: JWTClaims = Depends(get_current_user)):
    audit_context = build_audit_context(request)

    async with AsyncSessionFactory.session_scope() as session:
        await jwt_service.revoke_token(
            token=token,
            reason="logout",
            user_id=current_user.user_id,
            session=session,
            audit_context=audit_context,
        )
        await session.commit()
```

## Core Concepts

### Event Types

The system tracks five categories of events:

| Event Type | Description | Use Cases |
|------------|-------------|-----------|
| `auth` | Authentication events | Login, logout, token operations |
| `api_key` | API key operations | Store, retrieve, delete, rotate keys |
| `data` | Data modifications | Create, update, delete records |
| `system` | System events | Configuration changes, maintenance |
| `security` | Security events | Suspicious activity, rate limits |

### Actions

Each event type has specific actions:

**Authentication Actions**:
- `login` - Successful login
- `logout` - User logout
- `login_failed` - Failed login attempt
- `token_issued` - New token generated
- `token_revoked` - Token invalidated
- `token_refreshed` - Token refreshed

**API Key Actions**:
- `key_stored` - Key added or updated
- `key_retrieved` - Key accessed
- `key_deleted` - Key removed
- `key_rotated` - Key rotated to new value
- `key_validated` - Key validated with provider

**Security Actions**:
- `permission_denied` - Access denied
- `suspicious_activity` - Anomalous behavior detected
- `rate_limit_exceeded` - Rate limit hit

### Severity Levels

| Severity | Use Case | Examples |
|----------|----------|----------|
| `info` | Normal operations | Successful login, key stored |
| `warning` | Potential issues | Failed login, invalid key |
| `error` | Errors needing attention | Storage failures, validation errors |
| `critical` | Critical security events | Multiple failed attempts, suspicious activity |

### Audit Context

Every audit log should include request context for forensics:

```python
audit_context = {
    "ip_address": "192.168.1.100",      # Client IP address
    "user_agent": "Mozilla/5.0...",      # Browser/client identifier
    "request_id": "req_abc123",          # Unique request ID for tracing
    "request_path": "/api/v1/auth/login" # API endpoint accessed
}
```

### Change Tracking

For modifications, capture before/after state:

```python
await audit_logger.log_api_key_event(
    action=Action.KEY_ROTATED,
    provider="openai",
    status="success",
    message="API key rotated",
    session=session,
    user_id=user_id,
    old_value={"keychain_ref": "old_ref", "rotated_at": "2025-10-21T10:00:00Z"},
    new_value={"keychain_ref": "new_ref", "validated": True},
    details={"zero_downtime": True},
    audit_context=audit_context,
)
```

## API Reference

### audit_logger.log_event()

Core method for logging any audit event.

**Signature**:
```python
async def log_event(
    self,
    event_type: str,          # EventType constant
    action: str,              # Action constant
    status: str,              # "success", "failed", "error", "detected"
    severity: str,            # Severity constant
    message: str,             # Human-readable description
    session: AsyncSession,    # Database session (required)
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    old_value: Optional[Dict[str, Any]] = None,
    new_value: Optional[Dict[str, Any]] = None,
    audit_context: Optional[Dict[str, Any]] = None,
) -> AuditLog
```

**Example**:
```python
log = await audit_logger.log_event(
    event_type=EventType.SECURITY,
    action=Action.SUSPICIOUS_ACTIVITY,
    status="detected",
    severity=Severity.CRITICAL,
    message="Multiple failed login attempts from same IP",
    session=session,
    user_id="user123",
    details={
        "failed_attempts": 5,
        "time_window": "5_minutes",
        "ip_addresses": ["192.168.1.1", "192.168.1.2"],
    },
    audit_context=audit_context,
)
```

### audit_logger.log_auth_event()

Convenience method for authentication events.

**Signature**:
```python
async def log_auth_event(
    self,
    action: str,              # Action.LOGIN, Action.LOGOUT, etc.
    status: str,              # "success" or "failed"
    message: str,
    session: AsyncSession,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    audit_context: Optional[Dict[str, Any]] = None,
) -> AuditLog
```

**Example - Successful Login**:
```python
await audit_logger.log_auth_event(
    action=Action.LOGIN,
    status="success",
    message="User logged in successfully",
    session=session,
    user_id="user123",
    session_id="session456",
    details={"username": "john", "method": "password"},
    audit_context=audit_context,
)
```

**Example - Failed Login**:
```python
await audit_logger.log_auth_event(
    action=Action.LOGIN_FAILED,
    status="failed",
    message="Invalid credentials",
    session=session,
    user_id=None,  # No user_id for failed attempts
    details={"username": "john", "reason": "invalid_password"},
    audit_context=audit_context,
)
```

### audit_logger.log_api_key_event()

Convenience method for API key operations.

**Signature**:
```python
async def log_api_key_event(
    self,
    action: str,              # Action.KEY_STORED, Action.KEY_ROTATED, etc.
    provider: str,            # "openai", "anthropic", etc.
    status: str,              # "success" or "failed"
    message: str,
    session: AsyncSession,
    user_id: str,
    details: Optional[Dict[str, Any]] = None,
    old_value: Optional[Dict[str, Any]] = None,
    new_value: Optional[Dict[str, Any]] = None,
    audit_context: Optional[Dict[str, Any]] = None,
) -> AuditLog
```

**Example - Store Key**:
```python
await audit_logger.log_api_key_event(
    action=Action.KEY_STORED,
    provider="openai",
    status="success",
    message="API key stored successfully",
    session=session,
    user_id="user123",
    details={"keychain_ref": "piper_user123_openai", "validated": True},
    audit_context=audit_context,
)
```

**Example - Rotate Key**:
```python
await audit_logger.log_api_key_event(
    action=Action.KEY_ROTATED,
    provider="anthropic",
    status="success",
    message="API key rotated successfully",
    session=session,
    user_id="user123",
    old_value={"keychain_ref": "old_ref", "rotated_at": "2025-10-21T10:00:00Z"},
    new_value={"keychain_ref": "new_ref", "validated": True},
    details={"zero_downtime": True},
    audit_context=audit_context,
)
```

### audit_logger.log_security_event()

Convenience method for security events.

**Signature**:
```python
async def log_security_event(
    self,
    action: str,              # Action.PERMISSION_DENIED, etc.
    severity: str,            # Severity constant
    message: str,
    session: AsyncSession,
    user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    audit_context: Optional[Dict[str, Any]] = None,
) -> AuditLog
```

**Example - Rate Limit**:
```python
await audit_logger.log_security_event(
    action=Action.RATE_LIMIT_EXCEEDED,
    severity=Severity.WARNING,
    message="User exceeded rate limit",
    session=session,
    user_id="user123",
    details={"limit": 100, "actual": 150, "window": "1_hour"},
    audit_context=audit_context,
)
```

## Architecture

### Database Schema

The `audit_logs` table structure:

```sql
CREATE TABLE audit_logs (
    -- Identity
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    session_id VARCHAR(255),

    -- Event classification
    event_type VARCHAR(50) NOT NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(255),

    -- Event details
    status VARCHAR(20) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    details JSON,

    -- Request context
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    request_id VARCHAR(255),
    request_path VARCHAR(500),

    -- Change tracking
    old_value JSON,
    new_value JSON,

    -- Timestamps
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Indexes

Nine strategic indexes for query performance:

1. `idx_audit_user_date` - User's audit trail by date
2. `idx_audit_event_type` - Filter by event type
3. `idx_audit_action` - Filter by specific action
4. `idx_audit_resource` - Query specific resources
5. `idx_audit_severity` - Critical/error queries
6. `idx_audit_status` - Success/failure analysis
7. `idx_audit_ip` - Track activity by IP
8. `idx_audit_session` - Session-based queries
9. `idx_audit_request` - Request tracing

### Integration Points

```
┌─────────────────────────────────────────────────────────┐
│                   Audit Logging System                   │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌─────▼──────┐
    │ JWT Service  │ │  API Keys   │ │  Security  │
    │              │ │  Service    │ │  Events    │
    ├──────────────┤ ├─────────────┤ ├────────────┤
    │ • Revoke     │ │ • Store     │ │ • Rate     │
    │ • Refresh    │ │ • Delete    │ │   Limit    │
    │ • Validate   │ │ • Rotate    │ │ • Anomaly  │
    └──────────────┘ └─────────────┘ └────────────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                    ┌───────▼────────┐
                    │  AuditLog      │
                    │  Database      │
                    │  (PostgreSQL)  │
                    └────────────────┘
```

### Service Flow

```
1. API Route receives request
   ↓
2. Extract audit_context from Request
   ↓
3. Call service method (JWT, API Key, etc.)
   ↓
4. Service performs operation
   ↓
5. Service calls audit_logger with session
   ↓
6. audit_logger creates AuditLog record
   ↓
7. Session commits (operation + audit log)
   ↓
8. Both succeed or both rollback (transactional)
```

## Query Examples

### Query User's Recent Activity

```python
from sqlalchemy import select
from services.database.models import AuditLog

async with AsyncSessionFactory.session_scope() as session:
    result = await session.execute(
        select(AuditLog)
        .where(AuditLog.user_id == "user123")
        .order_by(AuditLog.created_at.desc())
        .limit(50)
    )
    recent_logs = result.scalars().all()

    for log in recent_logs:
        print(f"{log.event_type}.{log.action}: {log.message}")
```

### Query Failed Login Attempts

```python
result = await session.execute(
    select(AuditLog)
    .where(
        AuditLog.event_type == EventType.AUTH,
        AuditLog.action == Action.LOGIN_FAILED,
        AuditLog.created_at >= datetime.now(timezone.utc) - timedelta(hours=24)
    )
    .order_by(AuditLog.created_at.desc())
)
failed_logins = result.scalars().all()

# Group by IP address
from collections import defaultdict
by_ip = defaultdict(int)
for log in failed_logins:
    by_ip[log.ip_address] += 1

# Find IPs with multiple failures
suspicious_ips = {ip: count for ip, count in by_ip.items() if count >= 5}
```

### Query API Key Operations

```python
result = await session.execute(
    select(AuditLog)
    .where(
        AuditLog.event_type == EventType.API_KEY,
        AuditLog.user_id == "user123",
        AuditLog.resource_id == "openai"  # Specific provider
    )
    .order_by(AuditLog.created_at.desc())
)
key_operations = result.scalars().all()

for log in key_operations:
    print(f"{log.action} at {log.created_at}: {log.message}")
    if log.old_value and log.new_value:
        print(f"  Old: {log.old_value}")
        print(f"  New: {log.new_value}")
```

### Query Critical Security Events

```python
result = await session.execute(
    select(AuditLog)
    .where(
        AuditLog.severity == Severity.CRITICAL,
        AuditLog.created_at >= datetime.now(timezone.utc) - timedelta(days=7)
    )
    .order_by(AuditLog.created_at.desc())
)
critical_events = result.scalars().all()

# Send alerts for critical events
for event in critical_events:
    alert_security_team(event)
```

### Query by Request ID (Trace Full Request)

```python
result = await session.execute(
    select(AuditLog)
    .where(AuditLog.request_id == "req_abc123")
    .order_by(AuditLog.created_at)
)
request_trail = result.scalars().all()

print(f"Full audit trail for request req_abc123:")
for log in request_trail:
    print(f"  {log.created_at}: {log.event_type}.{log.action}")
```

### Query by Session ID (Multi-Request Workflow)

```python
result = await session.execute(
    select(AuditLog)
    .where(AuditLog.session_id == "session456")
    .order_by(AuditLog.created_at)
)
session_logs = result.scalars().all()

print(f"All operations in session session456:")
for log in session_logs:
    print(f"  {log.action}: {log.message}")
```

### Generate Security Report

```python
from datetime import datetime, timedelta, timezone

# Get statistics for last 24 hours
since = datetime.now(timezone.utc) - timedelta(hours=24)

# Total events
result = await session.execute(
    select(func.count(AuditLog.id))
    .where(AuditLog.created_at >= since)
)
total_events = result.scalar()

# Events by type
result = await session.execute(
    select(AuditLog.event_type, func.count(AuditLog.id))
    .where(AuditLog.created_at >= since)
    .group_by(AuditLog.event_type)
)
events_by_type = dict(result.all())

# Events by severity
result = await session.execute(
    select(AuditLog.severity, func.count(AuditLog.id))
    .where(AuditLog.created_at >= since)
    .group_by(AuditLog.severity)
)
events_by_severity = dict(result.all())

print(f"Security Report (Last 24 Hours)")
print(f"Total Events: {total_events}")
print(f"By Type: {events_by_type}")
print(f"By Severity: {events_by_severity}")
```

## Security Considerations

### 1. Sensitive Data Protection

**DO NOT log sensitive data in audit logs**:

```python
# ❌ BAD - Logs sensitive data
await audit_logger.log_api_key_event(
    action=Action.KEY_STORED,
    provider="openai",
    details={"api_key": "sk-actual-key-12345"},  # NEVER DO THIS
    ...
)

# ✅ GOOD - Logs metadata only
await audit_logger.log_api_key_event(
    action=Action.KEY_STORED,
    provider="openai",
    details={"keychain_ref": "piper_user_openai", "validated": True},
    ...
)
```

**Never log**:
- Passwords (plain text or hashed)
- API keys or tokens
- Personal identifiable information (PII) beyond user_id
- Credit card numbers
- Social security numbers

### 2. Access Control

Audit logs should be read-only for most users:

```python
# Only admins should query audit logs
if not current_user.is_admin:
    raise HTTPException(status_code=403, detail="Insufficient permissions")

# Users can only see their own logs
result = await session.execute(
    select(AuditLog).where(AuditLog.user_id == current_user.user_id)
)
```

### 3. Retention Policy

Implement retention policies to manage database growth:

```python
# Example: Delete logs older than 90 days
async def cleanup_old_logs():
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=90)

    async with AsyncSessionFactory.session_scope() as session:
        # Archive to cold storage first (optional)
        result = await session.execute(
            select(AuditLog).where(AuditLog.created_at < cutoff_date)
        )
        old_logs = result.scalars().all()

        # Export to S3/archive
        await archive_logs(old_logs)

        # Then delete from database
        await session.execute(
            delete(AuditLog).where(AuditLog.created_at < cutoff_date)
        )
        await session.commit()
```

### 4. Audit Log Integrity

Audit logs should be tamper-evident:

```python
# Consider adding checksums or signatures
import hashlib
import json

def compute_log_checksum(log: AuditLog) -> str:
    """Compute checksum for audit log integrity"""
    data = {
        "event_type": log.event_type,
        "action": log.action,
        "user_id": log.user_id,
        "created_at": log.created_at.isoformat(),
        "message": log.message,
    }
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
```

### 5. Rate Limiting

Prevent audit log spam:

```python
# Check if too many similar events in short time
recent_similar = await session.execute(
    select(func.count(AuditLog.id))
    .where(
        AuditLog.user_id == user_id,
        AuditLog.event_type == event_type,
        AuditLog.action == action,
        AuditLog.created_at >= datetime.now(timezone.utc) - timedelta(minutes=1)
    )
)

if recent_similar.scalar() > 100:  # More than 100 similar events in 1 minute
    logger.warning("Potential audit log spam detected", user_id=user_id)
    # Consider rate limiting or alerting
```

## Best Practices

### 1. Always Use Audit Context

```python
# ✅ GOOD - Full context
audit_context = build_audit_context(request)
await service.operation(session=session, audit_context=audit_context)

# ❌ BAD - Missing context
await service.operation(session=session, audit_context=None)
```

### 2. Use Appropriate Severity Levels

```python
# ✅ GOOD - Correct severity
await audit_logger.log_auth_event(
    action=Action.LOGIN_FAILED,
    status="failed",
    severity=Severity.WARNING,  # Failed login is warning
    ...
)

# ❌ BAD - Wrong severity
await audit_logger.log_auth_event(
    action=Action.LOGIN,
    status="success",
    severity=Severity.CRITICAL,  # Normal login should be INFO
    ...
)
```

### 3. Provide Meaningful Messages

```python
# ✅ GOOD - Clear, actionable message
message = f"User {username} exceeded rate limit: {actual_requests} requests in {window}"

# ❌ BAD - Vague message
message = "Error occurred"
```

### 4. Use Structured Details

```python
# ✅ GOOD - Structured data for querying
details = {
    "failed_attempts": 5,
    "time_window": "5_minutes",
    "ip_addresses": ["192.168.1.1", "192.168.1.2"],
    "user_agent": "Mozilla/5.0...",
}

# ❌ BAD - Unstructured string
details = {"info": "5 failed attempts from 192.168.1.1 in 5 minutes"}
```

### 5. Track Changes with old_value/new_value

```python
# ✅ GOOD - Clear before/after state
await audit_logger.log_api_key_event(
    action=Action.KEY_ROTATED,
    provider="openai",
    old_value={"keychain_ref": "old_ref", "rotated_at": "2025-10-21T10:00:00Z"},
    new_value={"keychain_ref": "new_ref", "validated": True},
    ...
)

# ❌ BAD - No change tracking
await audit_logger.log_api_key_event(
    action=Action.KEY_ROTATED,
    provider="openai",
    details={"rotated": True},  # Lost change details
    ...
)
```

### 6. Commit Audit Logs Transactionally

```python
# ✅ GOOD - Atomic operation + audit
async with AsyncSessionFactory.session_scope() as session:
    # Perform operation
    result = await service.store_key(session=session, ...)

    # Log audit event
    await audit_logger.log_api_key_event(session=session, ...)

    # Single commit for both
    await session.commit()

# ❌ BAD - Separate commits (can get out of sync)
await service.store_key(...)  # Commits internally
await audit_logger.log_api_key_event(...)  # Separate commit
```

### 7. Monitor Critical Events

Set up alerting for critical events:

```python
# Example monitoring query (run periodically)
async def check_critical_events():
    since = datetime.now(timezone.utc) - timedelta(minutes=5)

    result = await session.execute(
        select(AuditLog)
        .where(
            AuditLog.severity == Severity.CRITICAL,
            AuditLog.created_at >= since
        )
    )
    critical_events = result.scalars().all()

    if critical_events:
        # Send alerts
        for event in critical_events:
            await alert_security_team(
                subject=f"CRITICAL: {event.action}",
                body=f"Message: {event.message}\nDetails: {event.details}",
                user_id=event.user_id,
                ip_address=event.ip_address,
            )
```

## Troubleshooting

### Issue: Audit logs not appearing

**Check**:
1. Is `session` parameter provided to service method?
2. Is `session.commit()` called after the operation?
3. Are there any database errors in logs?

```python
# Debug: Check if audit_logger is being called
import structlog
logger = structlog.get_logger(__name__)

logger.info("About to log audit event", user_id=user_id, action=action)
await audit_logger.log_auth_event(...)
logger.info("Audit event logged successfully")
```

### Issue: Missing audit_context fields

**Check**:
1. Is `build_audit_context(request)` called?
2. Are headers present in the request?
3. Is `request.client` available (may be None in tests)?

```python
# Debug: Log audit context
audit_context = build_audit_context(request)
logger.debug("Audit context", **audit_context)
```

### Issue: Performance degradation

**Check**:
1. Are indexes being used? Run `EXPLAIN ANALYZE` on queries
2. Is retention policy in place to limit table growth?
3. Are queries filtering on indexed columns?

```python
# Check query performance
from sqlalchemy import text

async with session.begin():
    result = await session.execute(
        text("""
            EXPLAIN ANALYZE
            SELECT * FROM audit_logs
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 50
        """),
        {"user_id": "user123"}
    )
    print(result.fetchall())
```

### Issue: Duplicate audit logs

**Check**:
1. Is operation being retried?
2. Is `session.commit()` being called multiple times?
3. Are there duplicate event handlers?

```python
# Fix: Use idempotency keys
await audit_logger.log_event(
    ...,
    details={"idempotency_key": f"{user_id}_{action}_{timestamp}"},
)
```

### Issue: Audit logs for failed operations

Audit logs should be created even when operations fail:

```python
# ✅ GOOD - Log both success and failure
try:
    result = await service.store_key(...)
    await audit_logger.log_api_key_event(
        action=Action.KEY_STORED,
        status="success",
        ...
    )
except ValueError as e:
    await audit_logger.log_api_key_event(
        action=Action.KEY_STORED,
        status="failed",
        severity=Severity.ERROR,
        message=f"Failed to store key: {e}",
        ...
    )
    raise
finally:
    await session.commit()  # Commit audit log even if operation failed
```

## Related Documentation

- Authentication System *(proposed; doc TBD)*
- API Key Management *(proposed; doc TBD)*
- Security Best Practices *(proposed; doc TBD)*
- Database Schema *(proposed; doc TBD)*

## Support

For issues or questions:
- GitHub Issues: [#249 CORE-AUDIT-LOGGING](https://github.com/your-org/piper-morgan/issues/249)
- Security concerns: security@your-org.com
- Documentation updates: Submit PR to `docs/features/audit-logging.md`

---

**Last Updated**: October 22, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅
