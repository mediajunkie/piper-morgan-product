# Pattern-030: Plugin Interface

## Status
**Emerging** — partially implemented (GitHub integration + the piper-morgan plugin surface); refreshed 2026-06-17 (was "Experimental, June 3 vision")

## Context
To avoid vendor lock-in and enable extensibility across PM tools, Piper Morgan needs a plugin architecture where integrations (GitHub, Jira, Notion, Slack) are pluggable components rather than hardcoded dependencies. This pattern defines the interface contract for plugins.

## Pattern

### Core Plugin Interface
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class PiperPlugin(ABC):
    """
    Base interface for all Piper Morgan plugins.
    Domain concepts drive the interface, not tool specifics.
    """

    @abstractmethod
    async def get_items(self) -> List[WorkItem]:
        """Get all work items from this source"""
        pass

    @abstractmethod
    async def create_item(self, item: WorkItem) -> WorkItem:
        """Create a new work item"""
        pass

    @abstractmethod
    async def update_item(self, item_id: str, updates: Dict[str, Any]) -> WorkItem:
        """Update existing work item"""
        pass

    @abstractmethod
    async def get_team_members(self) -> List[TeamMember]:
        """Get team members from this source"""
        pass

    @abstractmethod
    async def sync_knowledge(self) -> KnowledgeBase:
        """Sync knowledge/documentation from this source"""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> PluginCapabilities:
        """Declare what this plugin can do"""
        pass
```

### Domain-First Design
```python
# PM domain concepts, not tool-specific
class WorkItem:
    """Universal work item that maps to issues/tickets/tasks"""
    id: str
    title: str
    description: str
    status: WorkItemStatus
    assignee: Optional[TeamMember]
    labels: List[str]

    @classmethod
    def from_github_issue(cls, issue: GitHubIssue) -> 'WorkItem':
        """Adapt GitHub issue to domain model"""
        pass

    @classmethod
    def from_jira_ticket(cls, ticket: JiraTicket) -> 'WorkItem':
        """Adapt Jira ticket to domain model"""
        pass

class PluginCapabilities:
    """Declare what a plugin can do"""
    can_create_items: bool = True
    can_update_items: bool = True
    can_sync_knowledge: bool = False
    supports_webhooks: bool = False
    supports_comments: bool = True
```

### Plugin Registration and Discovery
```python
class PluginRegistry:
    """
    Manages available plugins and their lifecycle.
    """

    def __init__(self):
        self.plugins: Dict[str, PiperPlugin] = {}
        self.primary_source: Optional[str] = None

    def register(self, name: str, plugin: PiperPlugin):
        """Register a new plugin"""
        self.plugins[name] = plugin

    def discover(self):
        """Auto-discover plugins in plugins/ directory"""
        plugin_dir = Path("plugins")
        for plugin_path in plugin_dir.glob("*/plugin.py"):
            # Dynamic import and registration
            pass

    async def broadcast_event(self, event: Event):
        """Send events to all interested plugins"""
        for plugin in self.plugins.values():
            if plugin.capabilities.supports_events:
                await plugin.handle_event(event)
```

### Spatial Intelligence Integration
```python
class SpatialPlugin(PiperPlugin):
    """
    Leverage MCP spatial intelligence patterns already in codebase.
    """

    def __init__(self, mcp_service: MCPService):
        self.mcp = mcp_service

    async def query_spatial(self, query: str) -> List[WorkItem]:
        """
        Use MCP's spatial query capabilities to find relevant items
        across multiple connected services.
        """
        results = await self.mcp.spatial_search(query)
        return [self.adapt_to_work_item(r) for r in results]
```

### Event-Driven Learning
```python
class PluginEventBus:
    """
    Every plugin interaction is a learning opportunity.
    June 3 vision: event-driven core.
    """

    async def emit(self, event: PluginEvent):
        """Emit event for learning and other plugins"""
        # Store for learning
        await self.learning_service.record_event(event)

        # Notify other plugins
        await self.registry.broadcast_event(event)

        # Update patterns
        if event.is_pattern_relevant:
            await self.pattern_service.analyze(event)
```

## Benefits
- **Vendor independence**: Not locked to any PM tool
- **Infinite extensibility**: New tools easily added as plugins
- **Domain-driven**: PM concepts drive design, not tool quirks
- **Learning from all sources**: Every plugin feeds learning system
- **Spatial intelligence**: MCP patterns enable cross-tool queries

## Trade-offs
- **Abstraction complexity**: Mapping different tools to common model
- **Feature parity**: Lowest common denominator risk
- **Testing burden**: Each plugin needs comprehensive tests
- **Maintenance overhead**: Plugin API versioning challenges

## Implementation Strategy

### Phase 1: Extract GitHub as Plugin (Week 1)
```python
# Current: Hardcoded GitHub integration
# Target: GitHubPlugin implementing PiperPlugin interface

class GitHubPlugin(PiperPlugin):
    """Extract existing GitHub integration to plugin"""
    # Move existing code behind interface
```

### Phase 2: Plugin Registry (Week 2)
- Implement discovery mechanism
- Add configuration for plugin selection
- Create plugin lifecycle management

### Phase 3: Second Plugin (Week 3)
- Implement Notion or Slack as second plugin
- Prove interface works across different tools
- Refine based on learnings

## Example Configuration
```yaml
# config/plugins.yaml
plugins:
  github:
    enabled: true
    primary: true
    config:
      token: ${GITHUB_TOKEN}
      org: "mediajunkie"

  notion:
    enabled: true
    config:
      token: ${NOTION_TOKEN}
      workspace: "product-management"

  slack:
    enabled: true
    config:
      token: ${SLACK_TOKEN}
      channel: "#product"
```

## Related Patterns
- [Pattern-028: Intent Classification](pattern-028-intent-classification.md)
- [Pattern-029: Multi-Agent Coordination](pattern-029-multi-agent-coordination.md)
- [Pattern-009: GitHub Issue Tracking](pattern-009-github-issue-tracking.md)

## References
- Original vision: June 3, 2025 (Clean slate, plugin from day one)
- Current implementation: services/integrations/github/ (to be extracted)
- MCP patterns: services/mcp/ (spatial intelligence foundation)
- Related issues: Multiple integration issues across tracks
