# Calendar Integration Guide

## Overview
Complete guide for Calendar integration using the Delegated Model Context Protocol (MCP) Pattern with Google Calendar API.

## Architecture
The Calendar integration uses a **Delegated MCP Pattern** where:
- **Router**: `services/integrations/calendar/calendar_integration_router.py`
- **MCP Adapter**: `services/mcp/consumer/google_calendar_adapter.py`
- **Pattern**: Spatial intelligence delegated to MCP service

## Quick Start

### 1. Configuration
Follow the [Calendar Setup Guide](../configuration/calendar-setup.md) for environment configuration.

### 2. Basic Usage
```python
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

router = CalendarIntegrationRouter()

# Get today's events
events = await router.get_todays_events()

# Get current meeting
current = await router.get_current_meeting()

# Get next meeting
next_meeting = await router.get_next_meeting()
```

### 3. Spatial Context
```python
# Calendar integration provides spatial context through MCP
spatial_context = await router.get_spatial_context()
```

## Testing
See [Calendar Tests Documentation](../testing/calendar-tests.md) for comprehensive test coverage.

## Troubleshooting
See [Calendar Troubleshooting Guide](../troubleshooting/calendar-issues.md) for common issues.

## Related Documentation
- [Architecture Decision Record (ADR) 038: Spatial Intelligence Patterns](../internal/architecture/current/adrs/adr-038-spatial-intelligence-patterns.md)
- MCP Integration Guide *(proposed; doc TBD)*
