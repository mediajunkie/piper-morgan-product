# AUTH-PASSWORD-CHANGE - Implement Password Change Endpoint + Integration Test

**Priority**: P2 (Security Feature)
**Labels**: `auth`, `security`, `api`, `testing`, `technical-debt`
**Milestone**: Beta or MVP
**Related**: #292 (Integration Tests), #281 (JWT Auth)
**Created From**: Technical debt identified during #292

---

## Problem Statement

**Missing Functionality**: Users cannot change their passwords after account creation.

**Security Requirement**: When users change passwords, old tokens should be invalidated to prevent unauthorized access with compromised credentials.

**Origin**: During #292 (Auth Integration Tests), Test 5 (Password Change Invalidation) could not be implemented because `/auth/change-password` endpoint doesn't exist yet.

---

## Goal

Implement complete password change functionality:
1. **API Endpoint**: `/auth/change-password`
2. **Token Invalidation**: Revoke existing tokens on password change
3. **Integration Test**: Verify token invalidation works

---

## Required Functionality

### API Endpoint

**Endpoint**: `POST /auth/change-password`

**Request**:
```json
{
  "current_password": "oldpass123",
  "new_password": "newpass456",
  "new_password_confirm": "newpass456"
}
```

**Headers**:
```
Authorization: Bearer {current_valid_token}
```

**Response** (Success):
```json
{
  "success": true,
  "message": "Password changed successfully. Please log in with your new password."
}
```

**Response** (Errors):
- `400`: New password doesn't meet requirements
- `400`: Passwords don't match
- `401`: Current password incorrect
- `401`: Token invalid/expired

### Password Requirements

**Minimum Security**:
- At least 8 characters
- Contains uppercase letter
- Contains lowercase letter
- Contains number
- Contains special character

**Validation Messages**:
- Clear error messages for each requirement
- Don't reveal whether username exists (timing-safe)

### Token Invalidation

**Behavior**: When password changes successfully:
1. Add current token to blacklist
2. Add all other user tokens to blacklist (if tracking multiple sessions)
3. User must log in again with new password
4. Old tokens return 401 Unauthorized

**Implementation Options**:

**Option A**: Simple (Recommended for MVP)
```python
async def change_password(user_id: UUID, new_password_hash: str):
    # Change password
    user.password_hash = new_password_hash
    await session.commit()

    # Blacklist current token (from Authorization header)
    await TokenBlacklist.add(current_token, user_id, reason="password_change")
```

**Option B**: Complete (For Enterprise)
```python
async def change_password(user_id: UUID, new_password_hash: str):
    # Change password
    user.password_hash = new_password_hash

    # Blacklist ALL user tokens (multi-device security)
    tokens = await Token.get_all_for_user(user_id)
    for token in tokens:
        await TokenBlacklist.add(token.id, user_id, reason="password_change")

    await session.commit()
```

---

## Integration Test

**Add to**: `tests/integration/auth/test_auth_integration.py`

```python
@pytest.mark.integration
async def test_password_change_invalidates_tokens(real_client, integration_db):
    """
    Verify password change invalidates existing tokens.

    This test was deferred from Issue #292 because the password change
    endpoint didn't exist yet. Now it can be implemented.
    """
    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create user and login
    user_id = await create_test_user(
        integration_db,
        username=f"pwchangeuser_{unique_id}",
        password="OldPass123!"
    )

    login_data = {
        "username": f"pwchangeuser_{unique_id}",
        "password": "OldPass123!"
    }
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    old_token = response.json()["token"]

    # Verify old token works
    headers = {"Authorization": f"Bearer {old_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200, "Old token should work before password change"

    # Change password
    change_data = {
        "current_password": "OldPass123!",
        "new_password": "NewPass456!",
        "new_password_confirm": "NewPass456!"
    }
    response = await real_client.post(
        "/auth/change-password",
        json=change_data,
        headers=headers
    )
    assert response.status_code == 200, f"Password change failed: {response.text}"

    # Old token should NO LONGER work
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 401, \
        "Old token should be invalidated after password change"

    # Verify token is blacklisted in database
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await integration_db.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) > 0, "Token should be blacklisted"

    # Any blacklist entry with reason 'password_change' confirms it worked
    reasons = [entry.reason for entry in blacklist_entries]
    assert "password_change" in reasons, \
        f"Expected 'password_change' reason, got: {reasons}"

    # Login with NEW password should work
    login_data["password"] = "NewPass456!"
    response = await real_client.post("/auth/login", json=login_data)
    assert response.status_code == 200, "Login with new password should work"
    new_token = response.json()["token"]

    # New token should work
    headers = {"Authorization": f"Bearer {new_token}"}
    response = await real_client.get("/auth/me", headers=headers)
    assert response.status_code == 200, "New token should work"
    assert response.json()["username"] == f"pwchangeuser_{unique_id}"
```

---

## Implementation Plan

### Phase 1: Password Validation (30 minutes)

**Create**: `services/auth/password_validator.py`

```python
from typing import Optional
import re

class PasswordValidator:
    """Validates password requirements"""

    MIN_LENGTH = 8

    @classmethod
    def validate(cls, password: str) -> tuple[bool, Optional[str]]:
        """Returns (is_valid, error_message)"""

        if len(password) < cls.MIN_LENGTH:
            return False, f"Password must be at least {cls.MIN_LENGTH} characters"

        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"

        return True, None
```

### Phase 2: Service Layer (45 minutes)

**Update**: `services/auth/auth_service.py`

```python
async def change_password(
    user_id: UUID,
    current_password: str,
    new_password: str,
    current_token: str,
    session: AsyncSession
) -> dict:
    """
    Change user password and invalidate tokens.

    Returns:
        {"success": True} or raises exception

    Raises:
        ValueError: Invalid current password or new password doesn't meet requirements
    """
    # Get user
    user = await session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    # Verify current password
    if not bcrypt.checkpw(
        current_password.encode(),
        user.password_hash.encode()
    ):
        raise ValueError("Current password is incorrect")

    # Validate new password
    is_valid, error = PasswordValidator.validate(new_password)
    if not is_valid:
        raise ValueError(error)

    # Hash new password
    new_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt(rounds=12)
    ).decode()

    # Update password
    user.password_hash = new_hash

    # Blacklist current token
    await TokenBlacklist.add(
        session,
        token_id=current_token,
        user_id=user_id,
        reason="password_change"
    )

    await session.commit()

    return {"success": True}
```

### Phase 3: API Endpoint (30 minutes)

**Update**: `web/api/routes/auth.py`

```python
@router.post("/change-password")
async def change_password(
    data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token_from_header)
):
    """
    Change user password.

    Invalidates current token. User must log in again with new password.
    """
    try:
        # Verify passwords match
        if data.new_password != data.new_password_confirm:
            raise HTTPException(
                status_code=400,
                detail="New passwords do not match"
            )

        # Change password (validates and blacklists token)
        await auth_service.change_password(
            user_id=current_user.id,
            current_password=data.current_password,
            new_password=data.new_password,
            current_token=token,
            session=db
        )

        return {
            "success": True,
            "message": "Password changed successfully. Please log in with your new password."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400 if "requirement" in str(e) else 401,
            detail=str(e)
        )
```

**Pydantic Model**:
```python
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    new_password_confirm: str
```

### Phase 4: Integration Test (30 minutes)

**Add test** to `tests/integration/auth/test_auth_integration.py` (see above)

### Phase 5: Documentation (15 minutes)

**Update**: `docs/api/auth-api.md`

Add password change endpoint documentation with:
- Endpoint details
- Request/response examples
- Error codes
- Security notes

---

## Security Considerations

### Timing Attacks

**Problem**: Response timing could reveal whether password is correct

**Solution**: Use constant-time comparison for password checking (bcrypt handles this)

### Brute Force Protection

**Recommendation**: Add rate limiting to password change endpoint (separate issue)

**For MVP**: Document as known limitation

### Multi-Device Security

**MVP Approach**: Invalidate only current token (simple)

**Enterprise Approach**: Invalidate all user tokens (requires token tracking)

---

## Acceptance Criteria

### Functionality
- [ ] `/auth/change-password` endpoint implemented
- [ ] Password validation (8+ chars, upper, lower, number, special)
- [ ] Current password verification
- [ ] New password hashing with bcrypt (12 rounds)
- [ ] Token invalidation on password change

### Testing
- [ ] Integration test: `test_password_change_invalidates_tokens` passing
- [ ] Test verifies old token stops working
- [ ] Test verifies new password enables login
- [ ] Test checks blacklist entry with "password_change" reason

### Security
- [ ] Constant-time password comparison
- [ ] Clear error messages (don't leak info)
- [ ] Tokens properly blacklisted
- [ ] No way to bypass current password check

### Documentation
- [ ] API endpoint documented
- [ ] Password requirements listed
- [ ] Error responses documented
- [ ] Security notes included

---

## Test Verification

**Run integration test**:
```bash
pytest -m integration -k "password_change" -v

# Expected:
# test_password_change_invalidates_tokens PASSED
```

**Manual test**:
```bash
# 1. Login
curl -X POST http://localhost:8001/auth/login \
  -d '{"username":"testuser","password":"OldPass123!"}'

# Returns: {"token":"..."}

# 2. Change password
curl -X POST http://localhost:8001/auth/change-password \
  -H "Authorization: Bearer {token}" \
  -d '{"current_password":"OldPass123!","new_password":"NewPass456!","new_password_confirm":"NewPass456!"}'

# Returns: {"success":true,"message":"..."}

# 3. Try old token (should fail)
curl http://localhost:8001/auth/me \
  -H "Authorization: Bearer {old_token}"

# Returns: 401 Unauthorized

# 4. Login with new password (should work)
curl -X POST http://localhost:8001/auth/login \
  -d '{"username":"testuser","password":"NewPass456!"}'

# Returns: {"token":"..."}
```

---

## Estimated Effort

**Total**: 2-3 hours

- Phase 1 (Validation): 30 min
- Phase 2 (Service): 45 min
- Phase 3 (API): 30 min
- Phase 4 (Test): 30 min
- Phase 5 (Docs): 15 min

---

## Priority Justification

**P2 (Not P1)** because:
- ✅ Basic auth works without it (users can reset via admin)
- ✅ Not blocking alpha testing
- ✅ Security enhancement, not critical vulnerability

**Should be in Beta/MVP** because:
- 🔒 Standard security feature users expect
- 🔒 Required for production deployment
- 🔒 Simple to implement (2-3 hours)
- 🔒 Integration test infrastructure already exists

---

## Related Documentation

- **Password Security Best Practices**: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **OWASP Password Requirements**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- **bcrypt Documentation**: https://pypi.org/project/bcrypt/

---

**Created From**: Issue #292 scope adjustment
**Milestone**: Beta or MVP
**Priority**: P2 (Security Feature)
**Effort**: 2-3 hours

---

_This issue captures technical debt from #292 where Test 5 (Password Change Invalidation) could not be implemented because the endpoint doesn't exist yet. Infrastructure is ready - just needs endpoint implementation._
