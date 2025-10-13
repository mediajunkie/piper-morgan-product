# CORE-USERS-JWT: Implement Token Blacklist Storage

## Context
JWT tokens need blacklist storage for invalidation support (logout, security revocation). Currently marked as TODO in auth services.

## Current State
```python
# services/auth/jwt_service.py
# TODO: Implement token blacklist storage (Redis or database)
```

## Scope

### 1. Token Blacklist Infrastructure
- Redis-based blacklist storage (preferred for performance)
- Fallback to database if Redis unavailable
- TTL matching token expiration
- Atomic operations for thread safety

### 2. Blacklist Operations
```python
class TokenBlacklist:
    async def add(self, token: str, reason: str, expires_at: datetime):
        """Add token to blacklist with expiration"""

    async def is_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted"""

    async def remove_expired(self):
        """Clean up expired entries (background task)"""
```

### 3. Integration Points
- Logout endpoint adds tokens to blacklist
- Middleware checks blacklist before authorizing
- Admin capability to revoke specific tokens
- Security incident response (bulk revocation)

## Acceptance Criteria
- [ ] Redis blacklist storage implemented
- [ ] Database fallback operational
- [ ] Logout properly blacklists tokens
- [ ] Middleware enforces blacklist
- [ ] Expired tokens auto-cleanup
- [ ] Performance <10ms for blacklist check
- [ ] Tests for all operations

## Technical Details
- Use Redis SET with TTL for O(1) lookups
- Prefix keys: `blacklist:jwt:{token_id}`
- Background task for cleanup (daily)
- Circuit breaker for Redis failures

## Time Estimate
1 day

## Priority
High - Security critical for multi-user Alpha
