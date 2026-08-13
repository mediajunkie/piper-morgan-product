# Plugin Development Guide

**Last Updated**: October 4, 2025
**Difficulty**: Intermediate
**Time**: 2-3 hours for first integration

## Quick Start

Want to add a new integration to Piper Morgan? This guide walks you through creating a complete integration from scratch.

**What You'll Build**: A weather integration that fetches weather data and exposes it via API

**What You'll Learn**:

- Creating integration routers
- Wrapping routers as plugins
- Adding configuration
- Writing tests
- Registering your plugin

## Prerequisites

Before starting, ensure you have:

- [ ] Piper Morgan development environment set up
- [ ] Familiarity with FastAPI
- [ ] Understanding of Python async/await
- [ ] Read [Pattern-031: Plugin Wrapper](../internal/architecture/current/patterns/pattern-031-plugin-wrapper.md)

## Step 1: Plan Your Integration

### Questions to Answer

1. **What service are you integrating?** (e.g., Weather API, CRM, etc.)
2. **What functionality is needed?** (e.g., fetch data, send webhooks)
3. **What configuration is required?** (e.g., API keys, endpoints)
4. **What capabilities does it provide?** (e.g., routes, webhooks, spatial)

### Example: Weather Integration

```yaml
Service: OpenWeatherMap API
Functionality:
  - Fetch current weather
  - Get forecast
  - Location search
Configuration:
  - API key
  - Default location
Capabilities:
  - routes (API endpoints)
  - spatial (location-based data)
```

## Step 2: Create Directory Structure

```bash
cd services/integrations/
mkdir weather
cd weather
touch __init__.py
touch weather_integration_router.py
touch weather_plugin.py
touch config_service.py
mkdir tests
touch tests/test_weather_plugin.py
```

Your structure should look like:

```
services/integrations/weather/
├── __init__.py
├── weather_integration_router.py
├── weather_plugin.py
├── config_service.py
└── tests/
    └── test_weather_plugin.py
```

## Step 3: Create Config Service

Start with configuration - it's the foundation.

**File**: `services/integrations/weather/config_service.py`

```python
"""Configuration service for Weather integration"""

import os
from typing import Optional


class WeatherConfigService:
    """Manages configuration for Weather integration"""

    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY", "")
        self.default_location = os.getenv("WEATHER_DEFAULT_LOCATION", "San Francisco")
        self.api_endpoint = os.getenv(
            "WEATHER_API_ENDPOINT",
            "https://api.openweathermap.org/data/2.5"
        )

    def is_configured(self) -> bool:
        """Check if integration is properly configured"""
        return bool(self.api_key)

    def get_api_key(self) -> Optional[str]:
        """Get API key"""
        return self.api_key if self.api_key else None

    def get_default_location(self) -> str:
        """Get default location"""
        return self.default_location
```

**Key Points**:

- Use environment variables for sensitive data
- Provide sensible defaults
- Include `is_configured()` method
- Keep it simple

## Step 4: Create Integration Router

Now build your business logic.

**File**: `services/integrations/weather/weather_integration_router.py`

```python
"""Weather integration router - business logic"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
import httpx

from .config_service import WeatherConfigService


class WeatherIntegrationRouter:
    """Handles weather API integration logic"""

    def __init__(self, config_service: WeatherConfigService):
        self.config = config_service
        self.router = APIRouter(
            prefix="/api/integrations/weather",
            tags=["weather"]
        )
        self._setup_routes()

    def _setup_routes(self):
        """Define API routes"""

        @self.router.get("/current")
        async def get_current_weather(
            location: str = Query(default=None)
        ) -> Dict[str, Any]:
            """Get current weather for location"""
            if not self.config.is_configured():
                raise HTTPException(
                    status_code=503,
                    detail="Weather integration not configured"
                )

            loc = location or self.config.get_default_location()

            # Call weather API
            async with httpx.AsyncClient() as client:
                url = f"{self.config.api_endpoint}/weather"
                params = {
                    "q": loc,
                    "appid": self.config.get_api_key(),
                    "units": "metric"
                }

                response = await client.get(url, params=params)
                response.raise_for_status()

                return response.json()

        @self.router.get("/health")
        async def health_check() -> Dict[str, str]:
            """Health check endpoint"""
            is_configured = self.config.is_configured()
            return {
                "status": "ok" if is_configured else "unconfigured",
                "service": "weather"
            }
```

**Key Points**:

- Business logic goes here
- Use dependency injection for config
- Create routes with `@self.router` decorators
- Include health check endpoint
- Handle configuration errors gracefully

## Step 5: Create Plugin Wrapper

Wrap your router in the plugin interface.

**File**: `services/integrations/weather/weather_plugin.py`

```python
"""Weather integration plugin wrapper"""

from services.plugins.plugin_interface import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Dict, Any

from .config_service import WeatherConfigService
from .weather_integration_router import WeatherIntegrationRouter


class WeatherPlugin(PiperPlugin):
    """Plugin wrapper for Weather integration"""

    def __init__(self):
        self.config_service = WeatherConfigService()
        self.router_instance = WeatherIntegrationRouter(self.config_service)

    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata"""
        return PluginMetadata(
            name="weather",
            version="1.0.0",
            description="Weather data integration",
            author="Your Name",
            capabilities=["routes", "spatial"]
        )

    def get_router(self) -> APIRouter:
        """Return FastAPI router"""
        return self.router_instance.router

    def is_configured(self) -> bool:
        """Check if plugin is configured"""
        return self.config_service.is_configured()

    async def initialize(self):
        """Initialize plugin"""
        # Perform any startup tasks
        pass

    async def shutdown(self):
        """Cleanup on shutdown"""
        # Perform any cleanup
        pass

    def get_status(self) -> Dict[str, Any]:
        """Return plugin status"""
        return {
            "configured": self.is_configured(),
            "router_prefix": self.router_instance.router.prefix,
            "routes": len(self.router_instance.router.routes)
        }


# Auto-registration
from services.plugins import get_plugin_registry

_weather_plugin = WeatherPlugin()
get_plugin_registry().register(_weather_plugin)
```

**Key Points**:

- Implements all 6 PiperPlugin methods
- Minimal logic - delegates to router
- Auto-registration at module load
- Version follows semver (1.0.0)

## Step 6: Add Configuration

**File**: `config/PIPER.user.md`

Add your plugin to the enabled list:

````yaml
## 🔌 Plugin Configuration

```yaml
plugins:
  enabled:
    - github
    - slack
    - notion
    - calendar
    - weather  # Your new plugin

  settings:
    weather:
      # Plugin-specific settings if needed
````

Add environment variables to `.env`:

```bash
WEATHER_API_KEY=your_api_key_here
WEATHER_DEFAULT_LOCATION=San Francisco
```

## Step 7: Write Tests

**File**: `services/integrations/weather/tests/test_weather_plugin.py`

```python
"""Tests for Weather plugin"""

import pytest
from services.integrations.weather.weather_plugin import WeatherPlugin


def test_plugin_metadata():
    """Test plugin metadata"""
    plugin = WeatherPlugin()
    metadata = plugin.get_metadata()

    assert metadata.name == "weather"
    assert metadata.version == "1.0.0"
    assert "routes" in metadata.capabilities


def test_plugin_has_router():
    """Test plugin provides router"""
    plugin = WeatherPlugin()
    router = plugin.get_router()

    assert router is not None
    assert router.prefix == "/api/integrations/weather"


@pytest.mark.asyncio
async def test_plugin_lifecycle():
    """Test plugin initialization and shutdown"""
    plugin = WeatherPlugin()

    # Should not raise errors
    await plugin.initialize()
    await plugin.shutdown()


def test_plugin_status():
    """Test plugin status reporting"""
    plugin = WeatherPlugin()
    status = plugin.get_status()

    assert "configured" in status
    assert "router_prefix" in status
```

Run tests:

```bash
PYTHONPATH=. pytest services/integrations/weather/tests/ -v
```

## Step 8: Test Your Integration

Start Piper Morgan:

```bash
python3 main.py
```

Check plugin loaded:

```
🔌 Initializing Plugin System...
  📦 Loaded 5/5 plugin(s)
    ✅ weather
    ...
```

Test endpoints:

```bash
# Health check
curl http://localhost:8001/api/integrations/weather/health

# Get weather
curl "http://localhost:8001/api/integrations/weather/current?location=London"
```

## Example: The Demo Plugin

We've created a complete example plugin you can reference or copy.

**Location**: `services/integrations/demo/`

**Files**:

- `config_service.py` - Configuration template
- `demo_integration_router.py` - Router with 3 endpoints
- `demo_plugin.py` - Plugin wrapper
- `tests/test_demo_plugin.py` - Test suite

**Try it**:

```bash
# Load the demo plugin
python3 main.py
# Visit http://localhost:8001/api/integrations/demo/health

# Run tests
PYTHONPATH=. pytest services/integrations/demo/tests/ -v
```

**What it demonstrates**:

- Health check endpoint pattern
- Echo endpoint (simple functionality)
- Status endpoint (integration details)
- Complete test coverage
- Heavily commented code

**How to use it**:

1. Copy `services/integrations/demo/` to your new integration name
2. Search and replace "demo" with your integration name
3. Modify endpoints and logic for your needs
4. Update tests
5. You're done!

See the demo plugin code for detailed comments explaining each part.

## Common Patterns

### Pattern 1: Async HTTP Requests

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(url)
    return response.json()
```

### Pattern 2: Error Handling

```python
from fastapi import HTTPException

if not self.config.is_configured():
    raise HTTPException(
        status_code=503,
        detail="Integration not configured"
    )
```

### Pattern 3: Configuration Validation

```python
def is_configured(self) -> bool:
    return all([
        self.api_key,
        self.endpoint,
        # other required config
    ])
```

## Troubleshooting

### Plugin Not Loading

**Problem**: Plugin doesn't appear in startup logs

**Solutions**:

1. Check `config/PIPER.user.md` - is plugin in enabled list?
2. Check for syntax errors in plugin file
3. Verify auto-registration code is present
4. Check plugin filename matches pattern `*_plugin.py`

### Configuration Not Working

**Problem**: `is_configured()` returns False

**Solutions**:

1. Check environment variables are set
2. Verify `.env` file loaded
3. Print config values for debugging
4. Check config service initialization

### Routes Not Accessible

**Problem**: 404 errors when accessing routes

**Solutions**:

1. Verify router prefix matches URL
2. Check plugin initialized successfully
3. Confirm router returned by `get_router()`
4. Check FastAPI router mounted

## Next Steps

Once your integration works:

1. **Add More Endpoints**: Expand router with additional routes
2. **Improve Error Handling**: Add retry logic, better errors
3. **Add Tests**: Increase test coverage
4. **Document**: Add docstrings and examples
5. **Share**: Consider contributing back to project

## Related Documentation

- [Pattern-031: Plugin Wrapper](../internal/architecture/current/patterns/pattern-031-plugin-wrapper.md) - Architectural details
- [Plugin System README](../../services/plugins/README.md) - System overview
- Configuration Guide *(proposed; doc TBD)* - Config management

## Getting Help

- Review existing integrations in `services/integrations/`
- Check plugin interface definition in `services/plugins/plugin_interface.py`
- [Open a GitHub issue](https://github.com/mediajunkie/piper-morgan-product/issues/new) with what you tried and what happened

---

_Happy coding! 🚀_
