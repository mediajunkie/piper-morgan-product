    # ADR-057: CommandRegistry - Unified Command Discovery and Routing

**Status**: APPROVED (Phase 3 Implementation In Progress)
**Issue**: #551 ARCH-COMMANDS
**Date**: 2026-01-22
**Decision Makers**: Lead Developer, Chief Architect, PM

---

## Context

### Problem Statement

Commands in Piper Morgan are scattered across 6 registration points with no single source of truth:

| Interface | Commands | Registration Location |
|-----------|----------|----------------------|
| CLI (argparse) | 6 | `main.py` |
| CLI (Click) | 23+ | `cli/commands/*.py` |
| Web Chat Patterns | 541+ → ~20 intents | `services/intent_service/pre_classifier.py` |
| Slack Commands | 2 | `services/integrations/slack/webhook_router.py` |
| URL Routes | 202 | `web/api/routes/*.py` |
| Action Registry | 1+ | `services/actions/action_registry.py` |

### Impact

1. **Parity Gaps**: Same capability available in Web Chat but not Slack (calendar, priorities)
2. **Help Generation**: `/piper help` hardcoded, doesn't reflect actual capabilities
3. **Discoverability**: No single place to query "what can Piper do?"
4. **Maintenance**: Adding a command requires changes in multiple locations
5. **Testing**: No unified way to verify command coverage across interfaces

### Inventory Findings (Phase 1)

From `docs/internal/architecture/current/command-inventory.md`:

- **CLI**: 29 commands (framework inconsistency: argparse + Click)
- **Web Chat**: 541+ patterns → 17 groups → 6 canonical handlers + 14 QUERY handlers
- **Slack**: 2 slash commands (/piper, /standup)
- **URL Routes**: 202 endpoints across 25 modules

**Key Gap Categories**:
- A: True Gaps (should exist) - /calendar and /todo in Slack
- B: Inconsistencies (need standardization) - argparse vs Click
- C: Intentional Differences (documented) - issues CLI-only, admin URL-only

---

## Decision

### Design a CommandRegistry with the following properties:

1. **Central Definition**: Commands defined once with interface metadata
2. **Interface Adapters**: Each interface queries registry for its commands
3. **Dynamic Discovery**: Help and capabilities generated from registry
4. **Incremental Adoption**: Existing handlers remain, registry wraps them

### Architecture

```
                         ┌─────────────────────┐
                         │   CommandRegistry   │
                         │   (Single Source)   │
                         └─────────┬───────────┘
                                   │
       ┌───────────────┬───────────┼───────────┬───────────────┐
       │               │           │           │               │
       ▼               ▼           ▼           ▼               ▼
 ┌───────────┐  ┌───────────┐ ┌─────────┐ ┌─────────┐  ┌───────────┐
 │ CLI       │  │ Web Chat  │ │ Slack   │ │ URL     │  │ Discovery │
 │ Adapter   │  │ Adapter   │ │ Adapter │ │ Adapter │  │ Handler   │
 └───────────┘  └───────────┘ └─────────┘ └─────────┘  └───────────┘
```

---

## Schema Design

### CommandDefinition

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from enum import Enum

class CommandInterface(Enum):
    """Interfaces where a command can be exposed"""
    CLI = "cli"
    WEB_CHAT = "web_chat"
    SLACK = "slack"
    URL = "url"
    ALL = "all"  # Exposed on all interfaces

class CommandCategory(Enum):
    """Functional categories for command organization"""
    CALENDAR = "calendar"
    TODOS = "todos"
    PROJECTS = "projects"
    GITHUB = "github"
    STANDUP = "standup"
    SETTINGS = "settings"
    HELP = "help"
    ADMIN = "admin"

@dataclass
class InterfaceConfig:
    """Configuration for a specific interface"""
    enabled: bool = True
    aliases: List[str] = field(default_factory=list)
    description_override: Optional[str] = None
    requires_auth: bool = True
    # Interface-specific options
    slack_response_type: str = "ephemeral"  # or "in_channel"
    cli_group: Optional[str] = None  # Click group name
    url_method: str = "GET"  # HTTP method
    url_path: Optional[str] = None  # Route path override

@dataclass
class CommandDefinition:
    """Central definition of a command across all interfaces"""

    # Identity
    name: str  # Canonical name (e.g., "calendar_today")
    display_name: str  # Human-readable (e.g., "Today's Calendar")
    description: str  # What it does
    category: CommandCategory

    # Interface Exposure
    interfaces: Dict[CommandInterface, InterfaceConfig] = field(default_factory=dict)

    # Handler Reference (existing handlers continue to work)
    handler_module: str  # e.g., "services.intent_service.canonical_handlers"
    handler_name: str  # e.g., "_handle_temporal_query"

    # Discovery Metadata
    examples: List[str] = field(default_factory=list)  # Example invocations
    keywords: List[str] = field(default_factory=list)  # Search terms
    help_text: Optional[str] = None  # Detailed help

    # Execution Metadata
    requires_integration: Optional[str] = None  # e.g., "calendar", "github"
    execution_type: str = "query"  # "query", "mutation", "action"

    def is_available_on(self, interface: CommandInterface) -> bool:
        """Check if command is available on given interface"""
        if CommandInterface.ALL in self.interfaces:
            return self.interfaces[CommandInterface.ALL].enabled
        return interface in self.interfaces and self.interfaces[interface].enabled

    def get_interface_config(self, interface: CommandInterface) -> Optional[InterfaceConfig]:
        """Get configuration for specific interface"""
        if CommandInterface.ALL in self.interfaces:
            return self.interfaces[CommandInterface.ALL]
        return self.interfaces.get(interface)
```

### CommandRegistry

```python
from typing import Dict, List, Optional, Callable
import logging

class CommandRegistry:
    """Central registry for all Piper commands"""

    _commands: Dict[str, CommandDefinition] = {}
    _by_category: Dict[CommandCategory, List[str]] = {}
    _by_interface: Dict[CommandInterface, List[str]] = {}
    _initialized: bool = False

    @classmethod
    def register(cls, command: CommandDefinition) -> None:
        """Register a command definition"""
        cls._commands[command.name] = command

        # Index by category
        if command.category not in cls._by_category:
            cls._by_category[command.category] = []
        cls._by_category[command.category].append(command.name)

        # Index by interface
        for interface in command.interfaces:
            if interface not in cls._by_interface:
                cls._by_interface[interface] = []
            cls._by_interface[interface].append(command.name)

    @classmethod
    def get_command(cls, name: str) -> Optional[CommandDefinition]:
        """Get a command by canonical name"""
        return cls._commands.get(name)

    @classmethod
    def list_commands(cls,
                      interface: Optional[CommandInterface] = None,
                      category: Optional[CommandCategory] = None) -> List[CommandDefinition]:
        """List commands, optionally filtered"""
        commands = list(cls._commands.values())

        if interface:
            commands = [c for c in commands if c.is_available_on(interface)]
        if category:
            commands = [c for c in commands if c.category == category]

        return commands

    @classmethod
    def get_help(cls, interface: CommandInterface) -> str:
        """Generate help text for an interface"""
        commands = cls.list_commands(interface=interface)

        # Group by category
        by_category: Dict[CommandCategory, List[CommandDefinition]] = {}
        for cmd in commands:
            if cmd.category not in by_category:
                by_category[cmd.category] = []
            by_category[cmd.category].append(cmd)

        # Format help
        lines = ["**Available Commands**\n"]
        for category, cmds in sorted(by_category.items(), key=lambda x: x[0].value):
            lines.append(f"\n**{category.value.title()}**")
            for cmd in cmds:
                config = cmd.get_interface_config(interface)
                desc = config.description_override if config and config.description_override else cmd.description
                lines.append(f"  • {cmd.display_name}: {desc}")

        return "\n".join(lines)

    @classmethod
    def find_by_keyword(cls, keyword: str, interface: Optional[CommandInterface] = None) -> List[CommandDefinition]:
        """Find commands matching a keyword"""
        keyword_lower = keyword.lower()
        matches = []

        for cmd in cls.list_commands(interface=interface):
            if (keyword_lower in cmd.name.lower() or
                keyword_lower in cmd.display_name.lower() or
                any(keyword_lower in kw.lower() for kw in cmd.keywords)):
                matches.append(cmd)

        return matches
```

---

## Interface Adapters

### Slack Adapter (Example)

```python
class SlackCommandAdapter:
    """Adapts CommandRegistry for Slack slash commands"""

    @staticmethod
    def get_slash_commands() -> Dict[str, Callable]:
        """Get all Slack slash commands from registry"""
        commands = CommandRegistry.list_commands(interface=CommandInterface.SLACK)

        slash_commands = {}
        for cmd in commands:
            config = cmd.get_interface_config(CommandInterface.SLACK)
            if config and config.enabled:
                # Primary command
                slash_commands[f"/{cmd.name}"] = SlackCommandAdapter._create_handler(cmd)
                # Aliases
                for alias in config.aliases:
                    slash_commands[f"/{alias}"] = SlackCommandAdapter._create_handler(cmd)

        return slash_commands

    @staticmethod
    def _create_handler(cmd: CommandDefinition):
        """Create Slack handler wrapper for command"""
        async def handler(payload: dict) -> dict:
            # Load actual handler
            module = importlib.import_module(cmd.handler_module)
            handler_fn = getattr(module, cmd.handler_name)

            # Execute
            result = await handler_fn(payload)

            # Format for Slack
            config = cmd.get_interface_config(CommandInterface.SLACK)
            return {
                "response_type": config.slack_response_type if config else "ephemeral",
                "text": result.get("message", str(result))
            }
        return handler

    @staticmethod
    def build_help_response() -> dict:
        """Build Slack-formatted help response"""
        help_text = CommandRegistry.get_help(CommandInterface.SLACK)
        return {
            "response_type": "ephemeral",
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": help_text}
                }
            ]
        }
```

---

## Migration Strategy

### Phase 1: Registry Infrastructure (This ADR)
- Create `CommandRegistry` class
- Create `CommandDefinition` dataclass
- Create interface adapter base classes
- No behavioral changes

### Phase 2: Standup Command Migration (Proof of Concept)
- Register `/standup` in CommandRegistry
- Update Slack adapter to query registry
- Verify help generation works
- Document migration pattern

### Phase 3: Gap Closure
- Register calendar commands with Slack interface config
- Register todo commands with Slack interface config
- Generate `/piper help` from registry

### Phase 4: Full Migration
- Migrate remaining commands to registry
- Deprecate hardcoded command lists
- Enable interface parity by default

---

## Consequences

### Positive

1. **Single Source of Truth**: One place to define and discover commands
2. **Automatic Help**: Help generated from registry, always accurate
3. **Interface Parity**: Easy to enable command on new interface
4. **Testing**: Can verify all commands registered and routed
5. **Discovery**: DISCOVERY intent can query registry directly

### Negative

1. **Abstraction Overhead**: Additional layer between intent and handler
2. **Migration Effort**: Existing commands need registration
3. **Learning Curve**: Team must understand registry pattern

### Neutral

1. **Existing Handlers**: Continue to work unchanged
2. **Performance**: Registry is in-memory, negligible overhead
3. **Flexibility**: Can still have interface-specific behavior via config

---

## Relationship to Existing Registries

| Registry | Purpose | Relationship |
|----------|---------|--------------|
| PluginRegistry | Integration lifecycle | CommandRegistry may query for available integrations |
| ActionRegistry | Mutation execution | Commands may reference actions for mutations |
| ServiceContainer | Service lifecycle | CommandRegistry handlers access services |

**Integration**: CommandRegistry complements rather than replaces these. Commands may:
- Check `PluginRegistry.get_enabled_plugins()` for availability
- Dispatch to `ActionRegistry.execute()` for mutations
- Get services via `ServiceContainer.get_service()`

---

## Example Registration

```python
# services/commands/command_definitions.py

from services.commands.registry import CommandRegistry, CommandDefinition, CommandInterface, InterfaceConfig, CommandCategory

# Standup command - available everywhere
STANDUP_COMMAND = CommandDefinition(
    name="standup",
    display_name="Daily Standup",
    description="Generate your daily standup report",
    category=CommandCategory.STANDUP,
    interfaces={
        CommandInterface.ALL: InterfaceConfig(
            enabled=True,
            aliases=["standup", "daily"],
            slack_response_type="in_channel",
            cli_group="standup",
            url_path="/api/v1/standup/generate"
        )
    },
    handler_module="services.standup.standup_service",
    handler_name="generate_standup",
    examples=["show standup", "/standup", "what's my standup?"],
    keywords=["standup", "daily", "yesterday", "today", "blockers"],
    requires_integration=None,  # No external integration required
    execution_type="query"
)

# Calendar today - not yet on Slack (gap to close)
CALENDAR_TODAY_COMMAND = CommandDefinition(
    name="calendar_today",
    display_name="Today's Calendar",
    description="Show your meetings for today",
    category=CommandCategory.CALENDAR,
    interfaces={
        CommandInterface.WEB_CHAT: InterfaceConfig(enabled=True),
        CommandInterface.CLI: InterfaceConfig(enabled=True, cli_group="cal"),
        CommandInterface.SLACK: InterfaceConfig(enabled=False),  # Gap: #551 Phase 3 will enable
        CommandInterface.URL: InterfaceConfig(enabled=True, url_path="/api/v1/calendar/today")
    },
    handler_module="services.intent_service.canonical_handlers",
    handler_name="_handle_temporal_query",
    examples=["what meetings do I have today?", "cal today", "show calendar"],
    keywords=["calendar", "meetings", "today", "schedule"],
    requires_integration="calendar",
    execution_type="query"
)

def register_all():
    """Register all command definitions"""
    CommandRegistry.register(STANDUP_COMMAND)
    CommandRegistry.register(CALENDAR_TODAY_COMMAND)
    # ... more commands
```

---

## Open Questions

### Resolved by This ADR

1. **In-memory vs persisted?** → In-memory (registered at startup)
2. **How to handle auth per interface?** → InterfaceConfig.requires_auth
3. **Versioning strategy?** → Not needed initially; commands registered at startup

### Deferred to Implementation

1. **Pattern matching integration**: How does pre_classifier.py query CommandRegistry?
2. **CLI framework**: Does registry influence argparse→Click migration?
3. **Hot reload**: Can commands be added without restart?

---

## Decision

**PROPOSED** - Awaiting PM review before implementation.

### Implementation Plan

1. **Phase 3.1**: Create `services/commands/registry.py` with core classes
2. **Phase 3.2**: Create `services/commands/definitions.py` with initial commands
3. **Phase 3.3**: Create interface adapters (start with Slack)
4. **Phase 3.4**: Migrate `/standup` as proof of concept
5. **Phase 3.5**: Generate `/piper help` from registry
6. **Phase 4**: Close gaps (calendar, todo on Slack)

### Files to Create

```
services/commands/
├── __init__.py
├── registry.py           # CommandRegistry class
├── definitions.py        # CommandDefinition dataclass
├── adapters/
│   ├── __init__.py
│   ├── base.py          # BaseAdapter interface
│   ├── slack_adapter.py
│   ├── cli_adapter.py
│   └── webchat_adapter.py
└── commands/
    ├── __init__.py
    ├── standup.py       # STANDUP_COMMAND
    ├── calendar.py      # CALENDAR_* commands
    └── todos.py         # TODO_* commands
```

---

## References

- Issue #551: ARCH-COMMANDS - Command Parity Across Interfaces
- `docs/internal/architecture/current/command-inventory.md`: Phase 1 inventory
- `services/plugins/plugin_registry.py`: Existing registry pattern
- `services/actions/action_registry.py`: Existing action pattern
- `services/container/service_container.py`: Service lifecycle pattern

---

*ADR-057 created: 2026-01-22*
*Phase 2 of Issue #551 ARCH-COMMANDS*
