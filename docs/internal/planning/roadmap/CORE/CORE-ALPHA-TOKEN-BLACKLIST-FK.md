# CORE-ALPHA-TOKEN-BLACKLIST-FK - Re-add Token Blacklist Foreign Key Constraint

**Priority**: P2 (Technical Debt - Important)
**Labels**: `technical-debt`, `database`, `blocked`, `post-alpha`
**Milestone**: Post-#263 (UUID Migration)
**Blocked By**: #263 (UUID Migration)
**Related**: #281 (JWT Auth - where constraint was dropped)

---

## Problem Statement

During #281 implementation, we temporarily dropped the foreign key constraint on `token_blacklist.user_id` to enable alpha testing. This constraint MUST be re-added after the UUID migration (#263) is complete to maintain database integrity.

**Current State** ⚠️:
```sql
-- Constraint dropped in #281
ALTER TABLE token_blacklist DROP CONSTRAINT IF EXISTS token_blacklist_user_id_fkey;

-- user_id column exists but has no FK enforcement
token_blacklist.user_id → (no constraint) → alpha_users.id
```

**Why This Matters**:
- ❌ No referential integrity (orphaned blacklist entries possible)
- ❌ Can't rely on CASCADE deletes
- ❌ Database doesn't enforce user existence
- ❌ Potential for data corruption

---

## Root Cause

**The Problem** (#281 discovery):
1. `token_blacklist` table had FK to `users.id`
2. Alpha testing uses `alpha_users` table (different table)
3. Foreign key violation prevented logout from working
4. Temporary fix: Drop constraint for alpha

**Original Error**:
```
insert or update on table "token_blacklist" violates foreign key constraint
"token_blacklist_user_id_fkey"
DETAIL: Key (user_id)=(3f4593ae-5bc9-468d-b08d-8c4c02a5b963) is not present in table "users".
```

**Why We Couldn't Fix Properly in #281**:
- Issue #263 (UUID migration) not complete
- `users` vs `alpha_users` table split unresolved
- Needed auth working for alpha testing
- Proper fix requires resolving table architecture

---

## What Needs to Happen

### Prerequisite: Issue #263 Must Be Complete

**After #263 resolves the table architecture**, then:

### Option A: If UUID Migration Merges Tables
```sql
-- If #263 merges alpha_users → users
ALTER TABLE token_blacklist
  ADD CONSTRAINT token_blacklist_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE;
```

### Option B: If Alpha Users Stay Separate
```sql
-- If #263 keeps alpha_users separate
ALTER TABLE token_blacklist
  ADD CONSTRAINT token_blacklist_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES alpha_users(id)
  ON DELETE CASCADE;
```

### Additionally: Re-enable Model Relationships

In `services/database/models.py`, currently commented out:

```python
class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    # CURRENTLY DISABLED (re-enable after FK restored):
    # user = relationship("User", back_populates="blacklisted_tokens")
    # session = relationship("Session", back_populates="blacklisted_tokens")
```

**Re-enable these** once FK constraint is back in place.

---

## Implementation Plan

### Phase 1: Verify Prerequisites (10 min)
```bash
# 1. Verify #263 is complete
git log --oneline | grep "#263"

# 2. Check current table structure
psql -U piper -d piper_morgan -c "\d alpha_users"
psql -U piper -d piper_morgan -c "\d users"
psql -U piper -d piper_morgan -c "\d token_blacklist"

# 3. Determine which table to reference
# Based on #263 outcome
```

### Phase 2: Check for Orphaned Records (15 min)
```sql
-- Find any blacklist entries with invalid user_ids
SELECT tb.id, tb.user_id, tb.token_id, tb.expires_at
FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL;

-- If any found, decide:
-- Option A: Delete orphaned entries
-- Option B: Investigate why they exist
```

### Phase 3: Add Foreign Key Constraint (5 min)
```sql
-- Choose correct table based on #263 outcome
ALTER TABLE token_blacklist
  ADD CONSTRAINT token_blacklist_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES alpha_users(id)  -- or users(id)
  ON DELETE CASCADE;

-- Verify constraint added
\d token_blacklist
```

### Phase 4: Re-enable Model Relationships (10 min)
```python
# In services/database/models.py

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    # Re-enable:
    user = relationship("AlphaUser", back_populates="blacklisted_tokens")  # or "User"
    session = relationship("Session", back_populates="blacklisted_tokens")

# In AlphaUser (or User) model:
class AlphaUser(Base):  # or User
    # Re-enable:
    blacklisted_tokens = relationship("TokenBlacklist", back_populates="user")
```

### Phase 5: Test Cascade Behavior (15 min)
```python
# Test that deleting user cascades to blacklist
async def test_user_deletion_cascades_blacklist():
    # Create user
    # Create token and blacklist it
    # Delete user
    # Verify blacklist entry deleted
```

---

## Acceptance Criteria

### Database Integrity
- [ ] Foreign key constraint exists on `token_blacklist.user_id`
- [ ] Constraint references correct table (users or alpha_users)
- [ ] ON DELETE CASCADE behavior works
- [ ] No orphaned blacklist entries exist

### Model Relationships
- [ ] `TokenBlacklist.user` relationship re-enabled
- [ ] `TokenBlacklist.session` relationship re-enabled
- [ ] `AlphaUser.blacklisted_tokens` relationship re-enabled (or User)
- [ ] ORM navigation works: `user.blacklisted_tokens`

### Testing
- [ ] Test user deletion cascades to blacklist
- [ ] Test session deletion cascades to blacklist
- [ ] Test can't create blacklist entry for non-existent user
- [ ] All auth tests still pass (15/15)

### Documentation
- [ ] Migration script documented
- [ ] Decision about table reference documented
- [ ] Any orphaned records investigation documented

---

## Risk Assessment

### Low Risk ✅
- Adding FK constraint is straightforward
- Database operation is quick (milliseconds)
- Can roll back if issues

### Medium Risk ⚠️
- If orphaned records exist, need to handle
- Must coordinate with #263 timing
- Downtime if production (not issue for alpha)

### Mitigation
- Check for orphaned records BEFORE adding constraint
- Add constraint in transaction (can rollback)
- Test in development first
- Have rollback plan ready

---

## Testing Plan

### Pre-Addition Tests
```sql
-- Verify no orphaned records
SELECT COUNT(*) FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL;
-- Expected: 0
```

### Post-Addition Tests
```python
# Test 1: Can't create blacklist for non-existent user
async def test_blacklist_invalid_user():
    with pytest.raises(IntegrityError):
        await TokenBlacklist.add(
            token_id="fake",
            user_id="00000000-0000-0000-0000-000000000000",  # doesn't exist
            expires_at=datetime.utcnow()
        )

# Test 2: Deleting user cascades
async def test_user_deletion_cascades():
    user = await create_test_user()
    token = await create_token(user.id)
    await TokenBlacklist.add(token.id, user.id, expires_at=...)

    await db.delete(user)
    await db.commit()

    # Verify blacklist entry deleted
    entry = await TokenBlacklist.get(token.id)
    assert entry is None
```

### Integration Test
```bash
# Full auth flow still works
curl -X POST /auth/login -d '{"username": "xian", "password": "test"}'
TOKEN=$(...)
curl -X POST /auth/logout -H "Authorization: Bearer $TOKEN"
curl -X GET /auth/me -H "Authorization: Bearer $TOKEN"
# Expected: 401 Unauthorized
```

---

## Documentation Updates

### Files to Update
1. `services/database/models.py` - Re-enable relationships
2. `dev/active/CRITICAL-token-blacklist-foreign-key-issue.md` - Mark resolved
3. Migration script - Document the ALTER TABLE command
4. ADR or decision log - Document table choice rationale

---

## Timeline

**Dependencies**:
- ⏳ Waiting for #263 (UUID Migration) to complete
- Cannot proceed until table architecture resolved

**Estimated Effort**: 1 hour (after #263)
- Prerequisites: 10 min
- Orphaned records: 15 min
- Add constraint: 5 min
- Re-enable relationships: 10 min
- Testing: 15 min
- Documentation: 5 min

**Do NOT implement** until #263 is marked complete.

---

## Success Metrics

### Database Health
- Zero orphaned blacklist entries
- FK constraint enforced
- Cascade deletes working

### Code Quality
- Model relationships working
- ORM navigation functional
- No circular import issues

### Testing
- All existing tests pass
- New cascade tests pass
- Integration tests pass

---

## Evidence Required

**Before claiming complete**:
```sql
-- 1. Show constraint exists
\d token_blacklist
-- Expected: See FK constraint listed

-- 2. Show no orphans
SELECT COUNT(*) FROM token_blacklist tb
LEFT JOIN alpha_users au ON tb.user_id = au.id
WHERE au.id IS NULL;
-- Expected: 0

-- 3. Show cascade works
-- Delete test user with blacklisted token
-- Verify blacklist entry deleted
```

```python
# 4. Show tests pass
pytest tests/auth/test_auth_endpoints.py -v
# Expected: 15/15 passing

pytest tests/database/test_token_blacklist_cascade.py -v
# Expected: New tests passing
```

---

## Related Issues

- **#263**: UUID Migration (BLOCKS this issue)
- **#281**: JWT Auth (where constraint was dropped)
- **#282**: File Upload (depends on auth)

---

**DO NOT START** until #263 is complete and table architecture is resolved.

**Priority**: P2 - Important technical debt, but not blocking alpha testing.

**When Ready**: Ping @xian to confirm #263 complete and get go-ahead.

---

*This issue documents technical debt created in #281 for the sake of unblocking alpha testing. The constraint MUST be restored before production to maintain database integrity.*
