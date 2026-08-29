# CORE-USER-XIAN: Migrate xian Superuser to Proper User Structure

**Labels**: `enhancement`, `user-management`, `technical-debt`, `data-migration`
**Milestone**: Alpha
**Estimate**: 1-2 hours
**Priority**: High (Blocking for clean Alpha launch)

---

## Context

The "xian" superuser account predates our current user model and exists outside the proper user structure. This creates confusion and technical debt. We need to:

1. Preserve the historical xian configuration
2. Create proper xian user in production users table
3. Keep separate from xian-alpha test account
4. Clean up legacy references

## Current State

```python
# Current: Hardcoded superuser checks scattered throughout
if username == "xian":
    # Special handling

# Config files with xian-specific settings
config/xian.yaml  # Personal preferences outside user system

# Learning data in non-standard location
data/xian/  # Should be data/users/{user_id}/
```

## Scope

### 1. Audit xian References

```python
class XianMigrationAuditor:
    """Find all hardcoded xian references"""

    async def audit_codebase(self) -> AuditReport:
        references = {
            'config_files': self.find_config_references(),
            'code_checks': self.find_code_references(),
            'data_paths': self.find_data_references(),
            'special_cases': self.find_special_handling()
        }

        return AuditReport(
            total_references=len(references),
            breakdown=references,
            migration_complexity=self.assess_complexity(references)
        )
```

### 2. Create Production xian User

```python
class XianMigration:
    """Migrate xian superuser to proper user structure"""

    async def create_xian_production_user(self):
        """Create proper user entry for xian"""

        # 1. Create user in production users table
        xian_user = User(
            id=uuid.uuid4(),  # New proper UUID
            username="xian",
            email="xian@piper-morgan.com",  # Or actual email
            display_name="Christian Crumlish",
            role="superuser",  # Preserve superuser status
            created_at=datetime(2025, 8, 1),  # Historical create date
            preferences={},  # Will migrate from config
            metadata={
                "migrated_from": "legacy_superuser",
                "migration_date": datetime.now(),
                "original_config_path": "config/xian.yaml"
            }
        )

        await self.user_repository.create(xian_user)
        return xian_user
```

### 3. Migrate Configuration

```python
async def migrate_xian_config(self, new_user_id: str):
    """Migrate xian.yaml to user preferences"""

    # Load legacy config
    legacy_config = self.load_yaml("config/xian.yaml")

    # Transform to user preferences format
    preferences = {
        "llm": legacy_config.get("llm_preferences", {}),
        "ui": legacy_config.get("ui_settings", {}),
        "integrations": legacy_config.get("integrations", {}),
        # ... map all settings
    }

    # Save to user preferences
    await self.preference_manager.set_preferences(
        user_id=new_user_id,
        preferences=preferences
    )

    # Archive legacy config
    shutil.move("config/xian.yaml", "archive/config/xian.yaml.legacy")
```

### 4. Update Code References

```python
class XianReferenceUpdater:
    """Replace hardcoded xian checks with proper user checks"""

    def update_special_cases(self):
        # Before:
        # if username == "xian":
        #     return SuperuserPrivileges()

        # After:
        user = await self.get_user(username)
        if user and user.role == "superuser":
            return SuperuserPrivileges()
```

### 5. Data Migration

```bash
# Migrate data from legacy paths to user structure

# From:
data/xian/preferences.json
data/xian/learning/patterns.json
data/xian/history/

# To:
data/users/{new_user_id}/preferences.json
data/users/{new_user_id}/learning/patterns.json
data/users/{new_user_id}/history/
```

## Acceptance Criteria

- [ ] All hardcoded "xian" references identified
- [ ] Production user created for xian
- [ ] Legacy config migrated to user preferences
- [ ] Data moved to proper user structure
- [ ] Superuser privileges preserved
- [ ] No breaking changes to existing functionality
- [ ] xian can log in with proper user account
- [ ] xian-alpha test account remains separate
- [ ] Legacy files archived (not deleted)
- [ ] Tests verify migration success

## Migration Safety

### Preserve Everything
- Archive all legacy configs
- Keep backup of data before migration
- Log all transformations
- Rollback capability

### Verification Steps
1. Audit finds all references
2. Dry-run migration first
3. Verify data integrity after migration
4. Test superuser privileges work
5. Confirm xian and xian-alpha are separate

## Implementation Order

1. **Audit first** - Find all references
2. **Create user** - Establish proper account
3. **Migrate config** - Move preferences
4. **Update code** - Fix hardcoded checks
5. **Move data** - Relocate to user structure
6. **Test thoroughly** - Verify nothing broke
7. **Archive legacy** - Keep backups

## Benefits

- **Clean architecture**: No more special cases
- **Proper separation**: xian vs xian-alpha distinct
- **Future-proof**: Standard user model for all
- **Reduced tech debt**: Remove hardcoded checks
- **Maintainable**: New developers understand user model

## Notes

This is technical debt cleanup that enables clean Alpha launch. The xian account is essentially "User 0" and should be properly structured before we add User 1 (xian-alpha) and beyond.

Consider this a "graduation" of the xian account from prototype hack to proper architecture.

---

**Created**: October 22, 2025
**Author**: Chief Architect
**Note**: The 30-year journey from Netcom username loss to preventing it for others is complete!
