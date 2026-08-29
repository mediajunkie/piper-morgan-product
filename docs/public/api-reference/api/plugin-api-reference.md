# Plugin API Reference

**Version**: 1.0.0
**Last Updated**: October 4, 2025
**Status**: Complete

---

## Overview

Complete API reference for the Piper Morgan plugin system. This document covers the `PiperPlugin` interface, `PluginRegistry` API, configuration patterns, and common usage examples.

**Quick Links**:
- [PiperPlugin Interface](#piperplugin-interface) - Core plugin methods
- [PluginMetadata](#pluginmetadata) - Plugin metadata structure
- [PluginRegistry API](#pluginregistry-api) - Registry methods
- [Configuration](#configuration) - Plugin configuration in PIPER.user.md
- [Examples](#examples) - Complete code examples
- [Error Handling](#error-handling) - Error patterns and recovery

---

## PiperPlugin Interface

The `PiperPlugin` abstract base class defines the contract all plugins must implement. Located in `services/plugins/plugin_interface.py`.

### Core Methods

All plugins must implement these 6 methods:

#### `get_metadata() -> PluginMetadata`

Returns plugin metadata including identity, version, capabilities, and dependencies.

**Returns:**
- `PluginMetadata`: Object containing plugin information

**Required Fields:**
- `name` (str): Unique plugin identifier (e.g., "slack", "github")
- `version` (str): Semantic version (e.g., "1.0.0")
- `description` (str): Human-readable description
- `author` (str): Plugin author/team name
- `capabilities` (List[str]): Feature list (see capabilities below)
- `dependencies` (List[str]): Required plugin names

**Capabilities** (common values):
- `"routes"` - Plugin provides HTTP routes
- `"webhooks"` - Plugin handles webhook callbacks
- `"spatial"` - Plugin uses spatial intelligence (see ADR-038)
- `"mcp"` - Plugin uses Model Context Protocol
- `"background"` - Plugin runs background tasks

**Example:**
```python
def get_metadata(self) -> PluginMetadata:
    return PluginMetadata(
        name="slack",
        version="1.0.0",
        description="Slack integration with spatial intelligence",
        author="Piper Team",
        capabilities=["routes", "webhooks", "spatial"],
        dependencies=[]
    )
```

**Contract Requirements** (validated by `tests/plugins/contract/test_plugin_interface_contract.py`):
- Must return `PluginMetadata` instance
- All required fields must be non-empty strings
- `capabilities` must be a list (can be empty)
- `version` must follow semantic versioning (X.Y.Z format with numeric parts)

---

#### `get_router() -> Optional[APIRouter]`

Provides FastAPI router for HTTP endpoints. Return `None` if plugin has no HTTP routes.

**Returns:**
- `Optional[APIRouter]`: FastAPI router with plugin routes, or `None`

**Router Requirements** (validated by contract tests):
- Router must have a `prefix` defined
- Prefix must start with "/"
- Router must have at least one route defined (if returned)

**Example:**
```python
def get_router(self) -> Optional[APIRouter]:
    router = APIRouter(prefix="/api/v1/slack", tags=["slack"])

    @router.get("/health")
    async def health_check():
        return {"status": "healthy", "plugin": "slack"}

    @router.post("/webhook")
    async def handle_webhook(request: Request):
        # Process webhook
        return {"status": "received"}

    return router
```

**For plugins without routes:**
```python
def get_router(self) -> Optional[APIRouter]:
    return None  # Plugin has no HTTP endpoints
```

---

#### `is_configured() -> bool`

Checks if plugin is properly configured with all required settings.

**Returns:**
- `bool`: `True` if configured, `False` otherwise

**Performance Requirement** (validated by contract tests):
- Must complete in <1ms (typically checks config object, doesn't do I/O)

**Example:**
```python
def is_configured(self) -> bool:
    config = self.config_service.get_config()
    return all([
        config.api_token is not None,
        config.workspace_id is not None,
        config.validate()  # Validation method
    ])
```

**Consistency Requirement**:
- Return value must match `status['configured']` from `get_status()`

---

#### `async initialize() -> None`

Initializes plugin resources during application startup. Called after all plugins are registered.

**Returns:**
- `None`

**Raises:**
- `Exception`: If initialization fails (logged but doesn't stop other plugins)

**Use Cases:**
- Initialize API connections
- Allocate resources
- Start background tasks
- Validate configuration
- Authenticate with external services

**Idempotency Requirement** (validated by contract tests):
- Must be idempotent (can be called multiple times safely)
- Second call should not error or duplicate resources

**Example:**
```python
async def initialize(self) -> None:
    """Initialize Slack plugin."""
    metadata = self.get_metadata()
    self.logger.info(f"Initializing {metadata.name} plugin")

    # Only initialize if configured
    if not self.is_configured():
        self.logger.warning(f"{metadata.name} plugin not configured, skipping init")
        return

    try:
        # Initialize connections
        await self.router.adapter.authenticate()
        self.logger.info(f"{metadata.name} plugin initialized successfully")
    except Exception as e:
        self.logger.error(f"Failed to initialize {metadata.name}: {e}")
        raise
```

---

#### `async shutdown() -> None`

Cleans up plugin resources during application shutdown.

**Returns:**
- `None`

**Important:**
- Should NOT raise exceptions (log errors instead)
- Should be idempotent (safe to call multiple times)

**Use Cases:**
- Close API connections
- Release resources
- Stop background tasks
- Save state
- Cancel pending operations

**Idempotency Requirement** (validated by contract tests):
- Must be idempotent (can be called multiple times safely)
- Multiple calls should not error

**Example:**
```python
async def shutdown(self) -> None:
    """Shutdown Slack plugin gracefully."""
    metadata = self.get_metadata()
    self.logger.info(f"Shutting down {metadata.name} plugin")

    try:
        # Cleanup resources
        if hasattr(self.router, 'adapter'):
            await self.router.adapter.disconnect()

        # Cancel background tasks
        if hasattr(self, '_background_task'):
            self._background_task.cancel()

        self.logger.info(f"{metadata.name} plugin shutdown complete")
    except Exception as e:
        # Log but don't raise during shutdown
        self.logger.error(f"Error during {metadata.name} shutdown: {e}")
```

---

#### `get_status() -> Dict[str, Any]`

Returns plugin health and status information for monitoring.

**Returns:**
- `Dict[str, Any]`: Status dictionary

**Required Fields** (validated by contract tests):
- `configured` (bool): Must match `is_configured()` return value

**Recommended Fields:**
- `name` (str): Plugin name
- `version` (str): Plugin version
- `active` (bool): Whether plugin is active
- `connections` (dict): Connection status
- `metrics` (dict): Performance metrics
- `errors` (list): Recent errors

**Example:**
```python
def get_status(self) -> Dict[str, Any]:
    metadata = self.get_metadata()
    configured = self.is_configured()

    status = {
        "name": metadata.name,
        "version": metadata.version,
        "configured": configured,
        "active": True,
        "router": {
            "prefix": self.router.router.prefix if configured else None,
            "routes": len(self.router.router.routes) if configured else 0
        }
    }

    # Add spatial status if plugin has spatial capabilities
    if "spatial" in metadata.capabilities and configured:
        status["spatial"] = {
            "enabled": True,
            "adapter": "SlackSpatialAdapter"
        }

    return status
```

---

## PluginMetadata

Dataclass containing plugin metadata. Located in `services/plugins/plugin_interface.py`.

### Fields

```python
@dataclass
class PluginMetadata:
    # Required fields
    name: str               # Unique plugin identifier
    version: str            # Semantic version (X.Y.Z)
    description: str        # Human-readable description
    author: str             # Plugin author/team

    # Optional fields with defaults
    capabilities: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
```

### Example

```python
metadata = PluginMetadata(
    name="github",
    version="1.0.0",
    description="GitHub integration with issue tracking",
    author="Piper Team",
    capabilities=["routes", "webhooks"],
    dependencies=[]  # No dependencies on other plugins
)
```

---

## PluginRegistry API

The `PluginRegistry` class manages plugin registration, lifecycle, and discovery. Singleton pattern ensures global registry instance.

**Location**: `services/plugins/plugin_registry.py`

**Access**: `from services.plugins import get_plugin_registry`

### Core Methods

#### `get_plugin_registry() -> PluginRegistry`

Returns the global singleton plugin registry instance.

**Returns:**
- `PluginRegistry`: Global registry instance

**Example:**
```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()
```

---

#### `register(plugin: PiperPlugin) -> None`

Registers a plugin with the registry.

**Parameters:**
- `plugin` (PiperPlugin): Plugin instance to register

**Raises:**
- `TypeError`: If plugin doesn't implement `PiperPlugin` interface
- `ValueError`: If plugin name already registered

**Example:**
```python
from services.plugins import get_plugin_registry
from my_plugin import MyPlugin

registry = get_plugin_registry()
plugin = MyPlugin()
registry.register(plugin)
```

**Auto-Registration Pattern**:
Plugins typically auto-register when their module is imported:

```python
# In plugin file (e.g., slack_plugin.py)
from services.plugins import get_plugin_registry

# Auto-register on import
registry = get_plugin_registry()
registry.register(SlackPlugin())
```

---

#### `unregister(plugin_name: str) -> bool`

Unregisters a plugin by name.

**Parameters:**
- `plugin_name` (str): Name of plugin to unregister

**Returns:**
- `bool`: `True` if unregistered, `False` if not found

**Example:**
```python
registry = get_plugin_registry()
success = registry.unregister("slack")
if success:
    print("Slack plugin unregistered")
```

---

#### `get_plugin(name: str) -> Optional[PiperPlugin]`

Gets a plugin by name.

**Parameters:**
- `name` (str): Plugin name

**Returns:**
- `Optional[PiperPlugin]`: Plugin instance or `None` if not found

**Example:**
```python
registry = get_plugin_registry()
slack_plugin = registry.get_plugin("slack")

if slack_plugin:
    status = slack_plugin.get_status()
    print(f"Slack status: {status}")
else:
    print("Slack plugin not found")
```

---

#### `list_plugins() -> List[str]`

Lists all registered plugin names.

**Returns:**
- `List[str]`: List of plugin names (alphabetically sorted)

**Example:**
```python
registry = get_plugin_registry()
plugins = registry.list_plugins()
print(f"Registered plugins: {', '.join(plugins)}")
# Output: "Registered plugins: calendar, github, notion, slack"
```

---

#### `get_all_plugins() -> Dict[str, PiperPlugin]`

Gets all registered plugins.

**Returns:**
- `Dict[str, PiperPlugin]`: Copy of plugins dictionary

**Example:**
```python
registry = get_plugin_registry()
all_plugins = registry.get_all_plugins()

for name, plugin in all_plugins.items():
    metadata = plugin.get_metadata()
    print(f"{name}: v{metadata.version} - {metadata.description}")
```

---

#### `get_plugin_count() -> int`

Gets count of registered plugins.

**Returns:**
- `int`: Number of registered plugins

**Example:**
```python
registry = get_plugin_registry()
count = registry.get_plugin_count()
print(f"Total plugins: {count}")
```

---

#### `async initialize_all() -> Dict[str, bool]`

Initializes all registered plugins. Continues even if some fail.

**Returns:**
- `Dict[str, bool]`: Map of plugin name to success status

**Example:**
```python
registry = get_plugin_registry()
results = await registry.initialize_all()

for name, success in results.items():
    if success:
        print(f"✅ {name} initialized")
    else:
        print(f"❌ {name} failed to initialize")
```

---

#### `async shutdown_all() -> Dict[str, bool]`

Shuts down all registered plugins. Continues even if some fail.

**Returns:**
- `Dict[str, bool]`: Map of plugin name to success status

**Example:**
```python
registry = get_plugin_registry()
results = await registry.shutdown_all()

for name, success in results.items():
    status = "✅" if success else "❌"
    print(f"{status} {name} shutdown")
```

---

#### `discover_plugins() -> Dict[str, str]`

Discovers all available plugins in the integrations directory.

**Returns:**
- `Dict[str, str]`: Map of plugin name to module path

**Example:**
```python
registry = get_plugin_registry()
available = registry.discover_plugins()

print(f"Discovered {len(available)} plugins:")
for name, path in available.items():
    print(f"  {name}: {path}")
```

---

#### `load_enabled_plugins() -> Dict[str, bool]`

Loads all enabled plugins based on configuration.

**Returns:**
- `Dict[str, bool]`: Map of plugin name to load success status

**Example:**
```python
registry = get_plugin_registry()
results = registry.load_enabled_plugins()

print(f"Loaded {sum(results.values())}/{len(results)} plugins")
```

---

## Configuration

### Plugin Configuration in PIPER.user.md

Plugins are configured via YAML blocks in `config/PIPER.user.md`.

#### Basic Configuration

```yaml
```plugins
enabled:
  - github
  - slack
  - notion
  - calendar
disabled:
  - demo
```
```

#### With Settings

```yaml
```plugins
enabled:
  - github
  - slack

settings:
  github:
    feature_flags:
      - spatial_intelligence
  slack:
    workspace_id: "T012345"
```
```

### Environment Variables

Each plugin typically requires specific environment variables:

**GitHub**:
```bash
GITHUB_TOKEN=ghp_xxxxx
GITHUB_APP_ID=123456
```

**Slack**:
```bash
SLACK_BOT_TOKEN=xoxb-xxxxx
SLACK_SIGNING_SECRET=xxxxx
```

**Notion**:
```bash
NOTION_API_KEY=secret_xxxxx
```

**Calendar**:
```bash
GOOGLE_CALENDAR_CREDENTIALS=/path/to/credentials.json
```

---

## Examples

### Creating a New Plugin

Complete example of a minimal plugin:

```python
# File: services/integrations/weather/weather_plugin.py

from typing import Any, Dict, Optional
from fastapi import APIRouter
from services.plugins import get_plugin_registry
from services.plugins.plugin_interface import PiperPlugin, PluginMetadata
from .weather_integration_router import WeatherIntegrationRouter
from .config_service import WeatherConfigService


class WeatherPlugin(PiperPlugin):
    """Weather integration plugin."""

    def __init__(self):
        """Initialize Weather plugin."""
        self.config_service = WeatherConfigService()
        self.router = WeatherIntegrationRouter(self.config_service)
        self.logger = logging.getLogger(__name__)

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        return PluginMetadata(
            name="weather",
            version="1.0.0",
            description="Weather data integration",
            author="Piper Team",
            capabilities=["routes"],
            dependencies=[]
        )

    def get_router(self) -> Optional[APIRouter]:
        """Return FastAPI router."""
        return self.router.router

    def is_configured(self) -> bool:
        """Check if plugin is configured."""
        config = self.config_service.get_config()
        return config.api_key is not None

    async def initialize(self) -> None:
        """Initialize plugin resources."""
        metadata = self.get_metadata()
        self.logger.info(f"Initializing {metadata.name} plugin")

        if not self.is_configured():
            self.logger.warning(f"{metadata.name} not configured")
            return

        # Initialize API connection
        await self.router.initialize()
        self.logger.info(f"{metadata.name} initialized successfully")

    async def shutdown(self) -> None:
        """Cleanup plugin resources."""
        metadata = self.get_metadata()
        self.logger.info(f"Shutting down {metadata.name}")

        try:
            await self.router.cleanup()
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Return plugin status."""
        metadata = self.get_metadata()
        configured = self.is_configured()

        return {
            "name": metadata.name,
            "version": metadata.version,
            "configured": configured,
            "active": True,
            "router": {
                "prefix": "/api/v1/weather",
                "routes": 3
            }
        }


# Auto-register plugin
registry = get_plugin_registry()
registry.register(WeatherPlugin())
```

### Testing a Plugin

Contract tests automatically run against all plugins:

```python
# File: tests/plugins/contract/test_plugin_interface_contract.py

import pytest
from services.plugins.plugin_interface import PiperPlugin, PluginMetadata

@pytest.mark.contract
class TestPluginInterfaceContract:
    """Contract tests run automatically for all plugins."""

    def test_plugin_implements_interface(self, plugin_instance):
        """Every plugin must implement PiperPlugin."""
        assert isinstance(plugin_instance, PiperPlugin)

    def test_metadata_version_format(self, plugin_instance):
        """Version must follow semver (X.Y.Z)."""
        metadata = plugin_instance.get_metadata()
        parts = metadata.version.split('.')
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit()
```

Plugin-specific tests:

```python
# File: services/integrations/weather/tests/test_weather_plugin.py

import pytest
from ..weather_plugin import WeatherPlugin

class TestWeatherPlugin:
    """Weather plugin specific tests."""

    def test_weather_plugin_creation(self):
        """Test plugin can be created."""
        plugin = WeatherPlugin()
        assert plugin is not None

    def test_weather_metadata(self):
        """Test plugin metadata."""
        plugin = WeatherPlugin()
        metadata = plugin.get_metadata()

        assert metadata.name == "weather"
        assert metadata.version == "1.0.0"
        assert "routes" in metadata.capabilities

    @pytest.mark.asyncio
    async def test_lifecycle(self):
        """Test initialize/shutdown lifecycle."""
        plugin = WeatherPlugin()

        await plugin.initialize()
        status = plugin.get_status()
        assert status["active"] is True

        await plugin.shutdown()
```

### Using Plugins in Application

In FastAPI application startup:

```python
# File: web/app.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from services.plugins import get_plugin_registry

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    registry = get_plugin_registry()

    # Discover and load plugins
    available = registry.discover_plugins()
    print(f"Discovered {len(available)} plugins")

    results = registry.load_enabled_plugins()
    print(f"Loaded {sum(results.values())} plugins")

    # Initialize all plugins
    init_results = await registry.initialize_all()
    for name, success in init_results.items():
        if success:
            print(f"✅ {name} initialized")

    # Mount plugin routers
    for name in registry.list_plugins():
        plugin = registry.get_plugin(name)
        router = plugin.get_router()
        if router:
            app.include_router(router)
            print(f"Mounted {name} routes")

    yield  # Application runs

    # Shutdown plugins
    shutdown_results = await registry.shutdown_all()
    for name, success in shutdown_results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name} shutdown")

app = FastAPI(lifespan=lifespan)
```

---

## Error Handling

### Registration Errors

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

try:
    registry.register(my_plugin)
except TypeError as e:
    # Plugin doesn't implement PiperPlugin
    print(f"Invalid plugin: {e}")
except ValueError as e:
    # Plugin name already registered
    print(f"Duplicate plugin: {e}")
```

### Initialization Errors

```python
registry = get_plugin_registry()
results = await registry.initialize_all()

# Check for failures
failed = [name for name, success in results.items() if not success]
if failed:
    print(f"Failed to initialize: {', '.join(failed)}")
    # Application continues with remaining plugins
```

### Graceful Degradation

```python
def get_plugin_or_fallback(name: str) -> PiperPlugin:
    """Get plugin with fallback."""
    registry = get_plugin_registry()
    plugin = registry.get_plugin(name)

    if not plugin:
        print(f"Warning: {name} plugin not available")
        return None

    if not plugin.is_configured():
        print(f"Warning: {name} plugin not configured")
        return None

    return plugin

# Use with fallback
slack = get_plugin_or_fallback("slack")
if slack:
    status = slack.get_status()
else:
    # Handle absence gracefully
    status = {"configured": False, "active": False}
```

---

## Performance Characteristics

Based on benchmark results from `scripts/benchmarks/`:

| Operation | Target | Actual | Margin |
|-----------|--------|--------|--------|
| Plugin overhead | < 0.05 ms | 0.000041 ms | 120× better |
| Startup (all plugins) | < 2000 ms | 295.23 ms | 6.8× faster |
| Memory per plugin | < 50 MB | 9.08 MB | 5.5× better |
| Concurrent status checks | < 100 ms | 0.11 ms | 909× faster |

**Key Insights**:
- Plugin wrapper pattern is essentially free (0.041μs overhead)
- Startup dominated by config parsing, not plugin overhead
- Memory efficient (9MB per plugin average)
- Fully concurrent-safe (all plugins can be queried simultaneously)

---

## See Also

- **[Plugin Development Guide](../../../guides/plugin-development-guide.md)** - Step-by-step tutorial
- **[Pattern-031: Plugin Wrapper](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/patterns/pattern-031-plugin-wrapper.md)** - Architecture pattern
- **[ADR-034: Plugin Architecture](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-034-plugin-architecture.md)** - Implementation record
- **[Plugin Quick Reference](../../../guides/plugin-quick-reference.md)** - Cheat sheet
- **[Demo Plugin](https://github.com/mediajunkie/piper-morgan-product/tree/main/services/integrations/demo)** - Example implementation

---

**Questions or Issues?** See `docs/guides/plugin-development-guide.md` or check existing plugins in `services/integrations/`.
