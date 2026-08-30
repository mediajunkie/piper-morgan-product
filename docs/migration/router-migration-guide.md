# Router Migration Guide

**Purpose**: Step-by-step guide for migrating services from direct adapter imports to router pattern
**Status**: Active (CORE-QUERY-1 Phase 6)
**Last Updated**: 2025-09-29

## Quick Reference

### Calendar Integration

```python
# ❌ OLD: Direct Import
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

calendar = GoogleCalendarMCPAdapter()
events = await calendar.get_events()

# ✅ NEW: Router Pattern
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

calendar = CalendarIntegrationRouter()
events = await calendar.get_events()  # Same method call
```

**Feature Flags**:
- `USE_SPATIAL_CALENDAR` - Enable spatial intelligence (default: true)
- `ALLOW_LEGACY_CALENDAR` - Allow legacy fallback (default: false)

### Notion Integration

```python
# ❌ OLD: Direct Import
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

notion = NotionMCPAdapter()
database = await notion.get_database(db_id)

# ✅ NEW: Router Pattern
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

notion = NotionIntegrationRouter()
database = await notion.get_database(db_id)  # Same method call
```

**Feature Flags**:
- `USE_SPATIAL_NOTION` - Enable spatial intelligence (default: true)
- `ALLOW_LEGACY_NOTION` - Allow legacy fallback (default: false)

### Slack Integration

```python
# ❌ OLD: Direct Import (Dual Component)
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.slack_client import SlackClient

spatial = SlackSpatialAdapter()
client = SlackClient(config_service)

# Spatial operations
spatial_event = await spatial.create_spatial_event_from_slack(...)

# Client operations
await client.send_message(channel, text)

# ✅ NEW: Router Pattern (Unified Access)
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

slack = SlackIntegrationRouter(config_service)

# Spatial adapter access
spatial = slack.get_spatial_adapter()
spatial_event = await spatial.create_spatial_event_from_slack(...)

# Client methods available directly on router
await slack.send_message(channel, text)
```

**Feature Flags**:
- `USE_SPATIAL_SLACK` - Enable spatial intelligence (default: true)
- `ALLOW_LEGACY_SLACK` - Allow legacy fallback (default: false)

**Note**: Slack router requires `config_service` parameter for client initialization.

## Migration Process

### Step 1: Verify Current Usage

Identify all direct adapter imports in your service:

```bash
# Find Calendar direct imports
grep -r "GoogleCalendarMCPAdapter" services/your_service/

# Find Notion direct imports
grep -r "NotionMCPAdapter" services/your_service/

# Find Slack direct imports
grep -r "SlackSpatialAdapter\|SlackClient" services/your_service/
```

### Step 2: Create Backup

Always create a backup before migration:

```bash
cp services/your_service/your_file.py services/your_service/your_file.py.backup
```

### Step 3: Update Imports

Replace direct adapter imports with router imports:

**Calendar**:
```python
# Replace this:
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

# With this:
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
```

**Notion**:
```python
# Replace this:
from services.integrations.mcp.notion_adapter import NotionMCPAdapter

# With this:
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
```

**Slack**:
```python
# Replace this:
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.slack_client import SlackClient

# With this:
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
```

### Step 4: Update Instantiation

Replace adapter instantiation with router instantiation:

**Calendar**:
```python
# Replace this:
self.calendar = GoogleCalendarMCPAdapter()

# With this:
self.calendar = CalendarIntegrationRouter()
```

**Notion**:
```python
# Replace this:
self.notion = NotionMCPAdapter()

# With this:
self.notion = NotionIntegrationRouter()
```

**Slack** (requires config_service):
```python
# Replace this:
self.spatial = SlackSpatialAdapter()
self.client = SlackClient(config_service)

# With this:
self.slack = SlackIntegrationRouter(config_service)
# Access spatial: self.slack.get_spatial_adapter()
# Client methods: self.slack.send_message(), etc.
```

### Step 5: Update Method Calls (Usually Unchanged)

In most cases, method calls remain identical due to transparent delegation:

```python
# Calendar - No changes needed
events = await self.calendar.get_events()
summary = await self.calendar.get_temporal_summary()

# Notion - No changes needed
database = await self.notion.get_database(db_id)
page = await self.notion.create_page(parent_id, properties)

# Slack - Client methods unchanged
await self.slack.send_message(channel, text)
channels = await self.slack.list_channels()

# Slack - Spatial adapter requires accessor
spatial = self.slack.get_spatial_adapter()
event = await spatial.create_spatial_event_from_slack(...)
```

### Step 6: Test Migration

Verify the migrated service works correctly:

```bash
# Import test
PYTHONPATH=. python3 -c "from services.your_service.your_file import YourClass"

# Instantiation test
PYTHONPATH=. python3 -c "
from services.your_service.your_file import YourClass
obj = YourClass()
print('✅ Service instantiates correctly')
"

# Run relevant unit tests
pytest tests/your_service/test_your_file.py -v
```

### Step 7: Verify No Direct Imports Remain

Use the automated checker:

```bash
python scripts/check_direct_imports.py services/your_service/your_file.py
```

Expected output:
```
✅ No direct adapter imports detected (1 files checked)
```

### Step 8: Commit Changes

Commit with evidence of successful migration:

```bash
git add services/your_service/your_file.py
git commit -m "Migrate your_service to [Integration]Router pattern

- Import: [OldAdapter] → [NewRouter]
- Instantiation updated
- Method calls preserved (transparent delegation)
- Testing: Service imports successfully
- Verification: No direct imports remain

CORE-QUERY-1 service migration"
```

## Completed Migrations

### Calendar Services (Phase 4A)

1. **canonical_handlers.py**
   - Location: `services/intent_service/canonical_handlers.py`
   - Usage: Temporal data for time-related queries
   - Migration: Line 112-114
   - Commit: 52a4ba39

2. **morning_standup.py**
   - Location: `services/features/morning_standup.py`
   - Usage: Calendar context for morning standup generation
   - Migration: 2 locations (lines 414, 558)
   - Commit: 52a4ba39

### Notion Services (Phase 4B)

1. **notion_domain_service.py**
   - Location: `services/domain/notion_domain_service.py`
   - Usage: Domain service mediating Notion operations
   - Migration: Lines 14, 36
   - Commit: 750b4357

2. **publisher.py**
   - Location: `services/publishing/publisher.py`
   - Usage: Publishing content to Notion
   - Migration: Line 10, 19
   - Commit: 750b4357

3. **notion_spatial.py** — *deleted 2026-08-29 (spatial cold-island disposal; it had migrated
   to the router but was itself never wired into the live app)*
   - Location: was `services/intelligence/spatial/notion_spatial.py`
   - Usage: Notion spatial intelligence with 8-dimensional analysis
   - Migration: Lines 19, 87
   - Commit: 750b4357

### Slack Services (Phase 4C)

1. **webhook_router.py**
   - Location: `services/integrations/slack/webhook_router.py`
   - Usage: Slack webhook handling with spatial mapping
   - Migration: Lines 37, 56-65, 67-90
   - Special: Dual-component migration (spatial + client)
   - Commit: 894f01e1

## Common Patterns

### Pattern 1: Single Integration in __init__

```python
class MyService:
    def __init__(self):
        # OLD
        self.calendar = GoogleCalendarMCPAdapter()

        # NEW
        self.calendar = CalendarIntegrationRouter()
```

### Pattern 2: Conditional Integration

```python
class MyService:
    def __init__(self, use_calendar: bool = True):
        # OLD
        if use_calendar:
            self.calendar = GoogleCalendarMCPAdapter()

        # NEW
        if use_calendar:
            self.calendar = CalendarIntegrationRouter()
```

### Pattern 3: Lazy Initialization

```python
class MyService:
    def __init__(self):
        self._calendar = None

    async def get_calendar_data(self):
        # OLD
        if not self._calendar:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
            self._calendar = GoogleCalendarMCPAdapter()

        # NEW
        if not self._calendar:
            from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
            self._calendar = CalendarIntegrationRouter()

        return await self._calendar.get_events()
```

### Pattern 4: Dependency Injection

```python
class MyService:
    # OLD
    def __init__(self, calendar: GoogleCalendarMCPAdapter = None):
        self.calendar = calendar or GoogleCalendarMCPAdapter()

    # NEW
    def __init__(self, calendar: CalendarIntegrationRouter = None):
        self.calendar = calendar or CalendarIntegrationRouter()
```

### Pattern 5: Slack Dual-Component

```python
class MySlackService:
    def __init__(self, config_service):
        # OLD
        self.spatial = SlackSpatialAdapter()
        self.client = SlackClient(config_service)

        # Spatial operations
        await self.spatial.create_spatial_event_from_slack(...)

        # Client operations
        await self.client.send_message(channel, text)

    # NEW
    def __init__(self, config_service):
        self.slack = SlackIntegrationRouter(config_service)

        # Spatial operations via accessor
        spatial = self.slack.get_spatial_adapter()
        await spatial.create_spatial_event_from_slack(...)

        # Client operations directly on router
        await self.slack.send_message(channel, text)
```

## Troubleshooting

### Issue: Import Error After Migration

**Symptom**:
```
ImportError: cannot import name 'CalendarIntegrationRouter' from 'services.integrations.calendar'
```

**Solution**:
Verify the router file exists and is in the correct location:
```bash
ls -la services/integrations/calendar/calendar_integration_router.py
```

### Issue: Method Not Found

**Symptom**:
```
AttributeError: 'CalendarIntegrationRouter' object has no attribute 'some_method'
```

**Solution**:
The router might be missing a method. Verify router completeness:
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

router = CalendarIntegrationRouter()
adapter = GoogleCalendarMCPAdapter()

router_methods = set(m for m in dir(router) if not m.startswith('_'))
adapter_methods = set(m for m in dir(adapter) if not m.startswith('_'))

missing = adapter_methods - router_methods
if missing:
    print(f"Missing methods: {missing}")
```

### Issue: Integration Not Available

**Symptom**:
```
RuntimeError: No calendar integration available for get_events
```

**Solution**:
Feature flags are disabling all integration modes. Enable at least one:
```bash
export USE_SPATIAL_CALENDAR=true
```

### Issue: Pre-Commit Hook Failure

**Symptom**:
```
❌ ARCHITECTURAL VIOLATIONS DETECTED
services/your_service/your_file.py:42: Prohibited direct adapter import
```

**Solution**:
Complete the migration by replacing the direct import with the router import.

## Testing Checklist

After migration, verify:

- [ ] Service imports successfully
- [ ] Service instantiates without errors
- [ ] All method calls work as before
- [ ] No direct adapter imports remain
- [ ] Pre-commit hook passes
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Feature flags control integration correctly

## Getting Help

If you encounter issues during migration:

1. **Check this guide** for common patterns and troubleshooting
2. **Review completed migrations** in the codebase for examples
3. **Run the automated checker**: `python scripts/check_direct_imports.py`
4. **Consult router patterns documentation**: `docs/architecture/router-patterns.md`
5. **Check session logs**: `dev/2025/09/29/2025-09-29-1022-prog-code-log.md`

## Related Documentation

- Router Patterns *(proposed; doc TBD)* - Architecture overview
- [Feature Flags](../../services/infrastructure/config/feature_flags.py) - Feature flag implementation
- [Session Log](../../dev/2025/09/29/2025-09-29-1022-prog-code-log.md) - Detailed migration history

---

**Version**: 1.0
**Last Updated**: 2025-09-29
**Maintained By**: Architecture Team
