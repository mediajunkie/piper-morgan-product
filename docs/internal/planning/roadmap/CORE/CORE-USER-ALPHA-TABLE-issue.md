# CORE-USER-ALPHA-TABLE: Create Alpha Users Table

**Labels**: `enhancement`, `alpha`, `database`, `user-management`
**Milestone**: Alpha
**Estimate**: 2 hours
**Priority**: High

---

## Context

Alpha testers need isolated accounts separate from future production users. Test data and learning patterns should not contaminate production. Users who beta test should not lose their preferred usernames when production launches (the Netcom problem).

## Current State

- Single `users` table for all users
- No distinction between test and production accounts
- Learning data mixed across all users
- No migration path planned

## Scope

### 1. Create alpha_users Table

```sql
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Alpha-specific fields
    alpha_wave INTEGER DEFAULT 2,  -- Wave 1 was internal, Wave 2 is first external
    test_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    test_end_date TIMESTAMP,
    migrated_to_prod BOOLEAN DEFAULT FALSE,
    migration_date TIMESTAMP,
    prod_user_id UUID REFERENCES users(id),

    -- Preferences (JSON for flexibility during alpha)
    preferences JSONB DEFAULT '{}',
    learning_data JSONB DEFAULT '{}',

    -- Metadata
    notes TEXT,  -- For PM notes about tester
    feedback_count INTEGER DEFAULT 0,
    last_active TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_alpha_users_username ON alpha_users(username);
CREATE INDEX idx_alpha_users_email ON alpha_users(email);
CREATE INDEX idx_alpha_users_wave ON alpha_users(alpha_wave);
```

### 2. Update Authentication to Check Both Tables

```python
class AlphaUserService:
    async def authenticate(self, username: str) -> Optional[User]:
        # Check alpha_users first
        alpha_user = await self.get_alpha_user(username)
        if alpha_user:
            return self.alpha_to_user_model(alpha_user)

        # Fall back to production users
        return await self.get_prod_user(username)
```

### 3. Separate Learning Storage

```python
class AlphaLearningStorage:
    """Isolated learning storage for alpha users"""

    def get_storage_path(self, user_id: str, is_alpha: bool):
        if is_alpha:
            return f"data/alpha/learning/{user_id}/"
        return f"data/prod/learning/{user_id}/"
```

## Acceptance Criteria

- [ ] alpha_users table created with migration
- [ ] Authentication checks both tables
- [ ] Learning data isolated per table
- [ ] Preferences isolated per table
- [ ] Alpha users can log in normally
- [ ] Production users (if any) unaffected
- [ ] Tests verify isolation

## Benefits

- **Clean separation**: Test data doesn't contaminate production
- **Username protection**: Alpha testers keep their usernames
- **Learning isolation**: Test patterns don't affect production learning
- **Easy cleanup**: Can truncate alpha_users after testing
- **Migration flexibility**: Users choose what to keep

## Implementation Notes

- Start with PostgreSQL implementation (from Sprint A6)
- Use Alembic migration for schema
- Keep alpha_users schema flexible (JSONB for rapid iteration)
- Production users table can be more strict later

## Testing

- Unit tests for dual-table authentication
- Integration tests for data isolation
- Migration tests (even though not used yet)
- Performance tests with both tables

## Future Work

This issue creates the table. CORE-USER-MIGRATION will handle the migration tool.

---

**Created**: October 22, 2025
**Author**: Chief Architect
