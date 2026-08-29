# CORE-USER-ID-MIGRATION: Migrate users.id from VARCHAR to UUID

**Labels**: `technical-debt`, `database`, `migration`, `pre-mvp`
**Milestone**: MVP (Before May 2026)
**Priority**: High (must complete before MVP launch)
**Estimate**: Large (2-3 days with testing)
**Blocked By**: Sprint A7 complete
**Created During**: Sprint A7 (Issue #259 decision)

---

## Context

During Sprint A7 (Issue #259), we decided to keep `users.id` as VARCHAR(255) for Alpha launch to avoid risky data migration. However, UUID is industry standard and required for MVP scale.

**Current State**:
- `users.id`: VARCHAR(255) (human-readable IDs like "xian")
- `alpha_users.id`: UUID (proper format)
- **Type inconsistency**: Makes cross-table references awkward
- **Scale limitation**: VARCHAR less suitable for distributed systems

**Decision Context** (from Issue #259 discussion, Oct 23 2025):
> PM approved VARCHAR for Alpha with two caveats:
> 1. No production users yet (just PM + test artifacts)
> 2. **MUST create GitHub issue for UUID migration BEFORE MVP milestone**

---

## Why This Matters for MVP

**Problems with VARCHAR**:
- ❌ Not industry standard (confuses developers)
- ❌ Predictable IDs easier to enumerate (security)
- ❌ Harder to merge data from different systems
- ❌ Type inconsistency with alpha_users
- ❌ Less suitable for federation/distribution

**Benefits of UUID**:
- ✅ Industry standard (expected by developers)
- ✅ Globally unique (no collision risk)
- ✅ Non-sequential (harder to enumerate)
- ✅ Cross-system friendly (merging/syncing)
- ✅ Type consistency across all tables
- ✅ Future-proof for distributed systems

---

## Scope

### 1. Pre-Migration Analysis

**Data Audit**:
```sql
-- Count users affected
SELECT COUNT(*) as total_users FROM users;

-- Find non-UUID format IDs
SELECT id, username, email
FROM users
WHERE id !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$';

-- Find all foreign key references
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND ccu.table_name = 'users'
  AND ccu.column_name = 'id';
```

**Expected FK Tables**:
- conversations (user_id)
- user_api_keys (user_id)
- audit_logs (user_id)
- token_blacklist (user_id)
- feedback (user_id)
- personality_profiles (user_id)
- alpha_users (prod_user_id)

---

### 2. Migration Strategy

**Approach**: Zero-downtime migration with temporary dual-key column

**Steps**:

**Phase 1: Add UUID Column**
```sql
-- Add new UUID column (nullable initially)
ALTER TABLE users ADD COLUMN id_uuid UUID;

-- Generate UUIDs for existing users
UPDATE users SET id_uuid = gen_random_uuid();

-- Make UUID column NOT NULL
ALTER TABLE users ALTER COLUMN id_uuid SET NOT NULL;

-- Create unique index
CREATE UNIQUE INDEX idx_users_id_uuid ON users(id_uuid);
```

**Phase 2: Update Foreign Key Tables**
```sql
-- For each FK table, add temporary UUID column
-- Example for conversations:
ALTER TABLE conversations ADD COLUMN user_id_uuid UUID;

-- Populate UUID FK from users.id → users.id_uuid
UPDATE conversations c
SET user_id_uuid = u.id_uuid
FROM users u
WHERE c.user_id = u.id;

-- Verify all FKs populated
SELECT COUNT(*) FROM conversations WHERE user_id_uuid IS NULL;
-- Should be 0

-- Repeat for: user_api_keys, audit_logs, token_blacklist,
-- feedback, personality_profiles, alpha_users.prod_user_id
```

**Phase 3: Switch Primary Key**
```sql
-- Drop old FK constraints
ALTER TABLE conversations DROP CONSTRAINT conversations_user_id_fkey;
-- Repeat for all FK tables

-- Drop old PK on users.id
ALTER TABLE users DROP CONSTRAINT users_pkey;

-- Rename columns
ALTER TABLE users RENAME COLUMN id TO id_old;
ALTER TABLE users RENAME COLUMN id_uuid TO id;

-- Add new PK on users.id (now UUID)
ALTER TABLE users ADD PRIMARY KEY (id);

-- Update FK tables
ALTER TABLE conversations RENAME COLUMN user_id TO user_id_old;
ALTER TABLE conversations RENAME COLUMN user_id_uuid TO user_id;
-- Repeat for all FK tables

-- Recreate FK constraints
ALTER TABLE conversations
ADD CONSTRAINT conversations_user_id_fkey
FOREIGN KEY (user_id) REFERENCES users(id);
-- Repeat for all FK tables
```

**Phase 4: Cleanup**
```sql
-- Drop old VARCHAR columns (after verifying everything works)
ALTER TABLE users DROP COLUMN id_old;
ALTER TABLE conversations DROP COLUMN user_id_old;
-- Repeat for all FK tables
```

---

### 3. Data Preservation

**Critical**: Maintain user identity mapping

```sql
-- Create migration audit table
CREATE TABLE user_id_migration_audit (
    old_id VARCHAR(255) NOT NULL,
    new_id UUID NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    migrated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (old_id, new_id)
);

-- Populate during migration
INSERT INTO user_id_migration_audit (old_id, new_id, username, email)
SELECT id_old, id, username, email FROM users;
```

---

### 4. Application Code Updates

**Services to Update**:
```python
# services/auth/user_service.py
# - Update type hints: user_id: str → user_id: UUID
# - Update queries to use UUID type
# - Update serialization/deserialization

# models/user.py
# - Change id field type to UUID
from sqlalchemy.dialects.postgresql import UUID
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

# All services that reference user_id:
# - auth/
# - conversation/
# - knowledge/
# - feedback/
# Update type hints and UUID handling
```

---

### 5. Testing Strategy

**Test Phases**:

**Phase 1: Staging Migration**
```bash
# 1. Backup production database
pg_dump -U piper -d piper_morgan > backup_pre_uuid_migration.sql

# 2. Restore to staging
psql -U piper -d piper_morgan_staging < backup_pre_uuid_migration.sql

# 3. Run migration on staging
alembic upgrade head

# 4. Verify data integrity
pytest tests/integration/test_uuid_migration.py -v

# 5. Load test staging
# Simulate production load for 24 hours
```

**Phase 2: Production Migration**
```bash
# 1. Announce maintenance window (4-hour window)
# 2. Backup production
# 3. Run migration
# 4. Verify
# 5. Monitor for 48 hours
```

**Critical Tests**:
```python
def test_user_lookup_by_uuid():
    """Verify user lookup works with UUID"""
    user = user_service.get_user_by_id(uuid_value)
    assert user is not None

def test_foreign_key_integrity():
    """Verify all FKs reference correct UUID"""
    # Check conversations
    orphaned = db.query(Conversation).filter(
        ~exists().where(User.id == Conversation.user_id)
    ).count()
    assert orphaned == 0

def test_api_backwards_compatibility():
    """Verify API still works (if needed)"""
    # If API exposed VARCHAR IDs, ensure graceful handling
    pass

def test_migration_audit_complete():
    """Verify audit table has all users"""
    user_count = db.query(User).count()
    audit_count = db.query(UserIdMigrationAudit).count()
    assert user_count == audit_count
```

---

## Acceptance Criteria

- [ ] Pre-migration analysis complete (data audit, FK mapping)
- [ ] Migration script created and tested in staging
- [ ] All foreign key tables updated to UUID
- [ ] Primary key switched from VARCHAR to UUID
- [ ] Application code updated (type hints, queries)
- [ ] Migration audit table populated
- [ ] All tests passing (unit, integration, e2e)
- [ ] Staging migration successful (24-hour monitoring)
- [ ] Production migration successful (zero data loss)
- [ ] Rollback plan tested and documented
- [ ] Post-migration monitoring (48 hours)

---

## Risks & Mitigation

**Risk 1: Data Loss**
- **Mitigation**: Full backup before migration, audit table for tracing
- **Rollback**: Restore from backup if issues detected

**Risk 2: FK Constraint Violations**
- **Mitigation**: Verify FK population before dropping old columns
- **Detection**: Test queries for orphaned records

**Risk 3: Application Downtime**
- **Mitigation**: Dual-column approach allows zero-downtime migration
- **Fallback**: Keep old columns until verified working

**Risk 4: Performance Degradation**
- **Mitigation**: UUID indexes created, query plans reviewed
- **Monitoring**: Performance testing in staging first

**Risk 5: Alpha User Data**
- **Mitigation**: Alpha users run own instances (data isolated)
- **Communication**: Notify alpha users of migration timeline

---

## Timeline

**Target**: Complete before MVP milestone (May 2026)

**Recommended Schedule**:
- **Feb 2026**: Analysis phase (1 week)
- **Feb 2026**: Development & staging testing (1 week)
- **Mar 2026**: Production migration (1 day + monitoring)
- **Mar 2026**: Verification & cleanup (1 week)

**Buffer**: 2 months before MVP for any issues

---

## Dependencies

**Blocked By**:
- Sprint A7 complete (alpha_users table created)
- Alpha Wave 2 launch successful (users in system)

**Blocks**:
- Federation features (require UUID for cross-system identity)
- Advanced multi-tenancy (UUID required)
- Distributed deployment (UUID for global uniqueness)

---

## References

- **Issue #259**: Created alpha_users with UUID (established pattern)
- **Sprint A7 Discussion**: PM approved VARCHAR→UUID migration path
- **Chief Architect Guidance**: "Lightweight for alpha, proper for MVP"
- **PostgreSQL UUID Best Practices**: https://www.postgresql.org/docs/current/datatype-uuid.html

---

## Notes

**Why We Waited**:
- Alpha needed speed → VARCHAR was faster
- No real users yet → Safe to migrate before MVP
- Type inconsistency acceptable short-term

**Why We Must Do This**:
- MVP has real users → Need proper patterns
- Scale requirements → UUID better for growth
- Developer expectations → UUID is standard
- Future features → UUID required for federation

---

**Created**: October 23, 2025 (Sprint A7)
**Target**: March 2026 (Before MVP)
**Complexity**: High (touches all FK tables)
**Impact**: High (affects all user references)
**Priority**: Must complete before MVP launch
