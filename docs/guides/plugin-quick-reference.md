# Plugin System Quick Reference

Quick reference for common plugin development tasks.

## File Structure

```
services/integrations/[name]/
├── __init__.py              # Package exports
├── config_service.py        # Configuration (~50 lines)
├── [name]_integration_router.py  # Routes (~100-300 lines)
├── [name]_plugin.py         # Plugin wrapper (~130 lines)
└── tests/
    └── test_[name]_plugin.py     # Tests (~100 lines)
```

## Checklist for New Plugin

- [ ] Create directory structure
- [ ] Implement config service
- [ ] Create router with routes
- [ ] Wrap router as plugin
- [ ] Add auto-registration
- [ ] Write tests (6+ tests)
- [ ] Add to PIPER.user.md
- [ ] Test locally
- [ ] Document in README

## Key Patterns

### Config Service

```python
class MyConfigService:
    def __init__(self):
        self.api_key = os.getenv("MY_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.api_key)
```

### Router

```python
class MyIntegrationRouter:
    def __init__(self, config_service: MyConfigService):
        self.config = config_service
        self.router = APIRouter(prefix="/api/integrations/my")
        self._setup_routes()
```

### Plugin

```python
class MyPlugin(PiperPlugin):
    def __init__(self):
        self.config_service = MyConfigService()
        self.router_instance = MyIntegrationRouter(self.config_service)

    # Implement 6 interface methods...
```

### Auto-Registration

```python
from services.plugins import get_plugin_registry
_my_plugin = MyPlugin()
get_plugin_registry().register(_my_plugin)
```

## Common Commands

```bash
# Run plugin tests
PYTHONPATH=. pytest services/integrations/[name]/tests/ -v

# Run all plugin tests
PYTHONPATH=. pytest tests/plugins/ -v

# Start with your plugin
python3 main.py

# Test plugin endpoint
curl http://localhost:8001/api/integrations/[name]/health
```

## Resources

- [Plugin Development Guide](plugin-development-guide.md) - Full tutorial
- [Demo Plugin](../../services/integrations/demo/) - Complete example
- [Pattern-031: Plugin Wrapper](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/patterns/pattern-031-plugin-wrapper.md) - Architecture
- [Versioning Policy](plugin-versioning-policy.md) - Version management
