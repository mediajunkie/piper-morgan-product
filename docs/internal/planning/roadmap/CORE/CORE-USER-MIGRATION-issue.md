# CORE-USER-MIGRATION: Alpha to Production User Migration Tool

**Labels**: `enhancement`, `alpha`, `user-management`, `data-migration`
**Milestone**: Alpha
**Estimate**: 2 hours
**Priority**: Medium (High before Alpha ends)

---

## Context

When alpha testing concludes, testers need control over their data. They should be able to:
1. Migrate everything to a production account
2. Keep profile but discard test learning data
3. Abandon alpha account entirely

This prevents the "Netcom problem" where beta testers lose their usernames to their own test accounts.

## Scope

### 1. Migration Options Interface

```python
@dataclass
class MigrationOptions:
    """User choices for alpha data migration"""

    migrate_profile: bool = True  # Username, email, display name
    migrate_preferences: bool = True  # UI preferences, settings
    migrate_learning: bool = False  # Learning patterns (often noisy from testing)
    migrate_history: bool = False  # Conversation history
    create_backup: bool = True  # Archive alpha data regardless
```

### 2. Migration Service

```python
class AlphaMigrationService:
    """Handle alpha to production user migration"""

    async def offer_migration(self, alpha_user_id: str) -> MigrationOffer:
        """
        Present migration options to user
        Returns: MigrationOffer with available choices
        """
        alpha_user = await self.get_alpha_user(alpha_user_id)

        return MigrationOffer(
            username=alpha_user.username,
            data_summary=await self.summarize_user_data(alpha_user_id),
            options=MigrationOptions(),
            expires_at=datetime.now() + timedelta(days=30)
        )

    async def execute_migration(
        self,
        alpha_user_id: str,
        options: MigrationOptions
    ) -> MigrationResult:
        """
        Execute user-selected migration
        """
        # 1. Create production user
        prod_user = await self.create_prod_user(alpha_user_id, options)

        # 2. Migrate selected data
        if options.migrate_preferences:
            await self.migrate_preferences(alpha_user_id, prod_user.id)

        if options.migrate_learning:
            await self.migrate_learning_data(alpha_user_id, prod_user.id)

        if options.migrate_history:
            await self.migrate_history(alpha_user_id, prod_user.id)

        # 3. Create backup archive
        if options.create_backup:
            await self.archive_alpha_data(alpha_user_id)

        # 4. Mark alpha account as migrated
        await self.mark_migrated(alpha_user_id, prod_user.id)

        return MigrationResult(
            success=True,
            prod_user_id=prod_user.id,
            migrated_items=self.get_migrated_summary(options)
        )
```

### 3. CLI Migration Tool

```bash
# For PM to run migrations
piper migrate-user xian-alpha

Migration Options for user 'xian-alpha':
────────────────────────────────────────
Alpha Account Summary:
- Active since: Oct 29, 2025
- Conversations: 47
- Learning patterns: 12
- Preferences set: 8

What would you like to migrate to production?
[x] Profile (username, email)
[x] UI Preferences
[ ] Learning Data (may include test noise)
[ ] Conversation History

Proceed with migration? [y/N]: y

✅ Migration complete!
- Production user 'xian-alpha' created
- Profile migrated
- Preferences migrated
- Alpha data archived to: backups/alpha/xian-alpha-2025-11-15.tar.gz
```

### 4. Web Migration Wizard (Future)

```python
@app.get("/migrate")
async def migration_wizard(user: AlphaUser = Depends(get_current_user)):
    """Web interface for self-service migration"""
    # Return migration options page
    # User selects what to keep
    # Execute migration
    # Provide download of archived data
```

## Acceptance Criteria

- [ ] Migration service with configurable options
- [ ] CLI tool for PM-initiated migration
- [ ] Backup archive created for all migrations
- [ ] Username preserved in production
- [ ] Selected data migrated correctly
- [ ] Alpha account marked as migrated
- [ ] Rollback capability for failed migrations
- [ ] Tests for all migration paths

## Migration Data Handling

### What Migrates Cleanly
- Username, email, display name
- UI preferences (theme, verbosity)
- Basic settings

### What Needs Consideration
- **Learning patterns**: May include test noise
- **Conversation history**: May include test conversations
- **API keys**: Should re-enter for security

### What Doesn't Migrate
- Session tokens (regenerate)
- Temporary cache data
- Error logs from testing
- Test-specific metadata

## Success Metrics

- Users can keep their chosen username
- No data loss for wanted data
- Clean separation of test vs production
- Migration completes in <30 seconds
- Zero corruption of production data

## Future Enhancements

- Web-based self-service migration
- Selective data migration (choose specific patterns)
- Migration preview ("what will this look like?")
- Bulk migration tools for many users

---

**Created**: October 22, 2025
**Author**: Chief Architect
