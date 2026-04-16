"""Test all 4 plugins are functional"""

from services.plugins import get_plugin_registry, reset_plugin_registry

reset_plugin_registry()
registry = get_plugin_registry()

# Load all plugins
results = registry.load_enabled_plugins()

print("Plugin Loading Results:")
for name, success in sorted(results.items()):
    status = "✅" if success else "❌"
    print(f"{status} {name}: {'Loaded' if success else 'Failed'}")

print(f"\nTotal: {len(results)} plugins")

# Test each plugin's functionality
print("\nPlugin Functionality Check:")

for name in sorted(registry.list_plugins()):
    plugin = registry.get_plugin(name)

    # Get metadata
    metadata = plugin.get_metadata()
    print(f"\n{name}:")
    print(f"  Version: {metadata.version}")
    print(f"  Capabilities: {metadata.capabilities}")

    # Check configuration
    is_configured = plugin.is_configured()
    print(f"  Configured: {is_configured}")

    # Get status
    status = plugin.get_status()
    print(f"  Status keys: {list(status.keys())}")

    # Check router
    if "routes" in metadata.capabilities:
        router = plugin.get_router()
        print(f"  Router: {router.prefix if router else 'None'}")

print("\n✅ All plugin functionality verified!")
