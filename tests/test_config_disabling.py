"""Manual check for config-based plugin disabling.

#1452: this is a hand-run CLI utility (takes the plugin name as argv, prints,
returns bool) that pytest collected because of its former test_ name — it then
failed wanting the CLI arg as a fixture. Renamed so pytest skips it; run it
directly: python tests/test_config_disabling.py <plugin>."""

from services.plugins import get_plugin_registry, reset_plugin_registry


def check_disable_plugin(disabled_plugin: str, expected_count: int = 3):
    """Test disabling a specific plugin via config"""
    reset_plugin_registry()
    registry = get_plugin_registry()
    results = registry.load_enabled_plugins()

    enabled_plugins = list(results.keys())

    print(f"\nTest: Disable '{disabled_plugin}'")
    print(f"Enabled plugins: {enabled_plugins}")
    print(f"Expected count: {expected_count}")
    print(f"Actual count: {len(enabled_plugins)}")

    # Verify disabled plugin is NOT loaded
    if disabled_plugin not in enabled_plugins:
        print(f"✅ '{disabled_plugin}' successfully disabled")
    else:
        print(f"❌ '{disabled_plugin}' was NOT disabled (still loaded)")
        return False

    # Verify expected count
    if len(enabled_plugins) == expected_count:
        print(f"✅ Correct plugin count ({expected_count})")
    else:
        print(f"❌ Wrong plugin count (expected {expected_count}, got {len(enabled_plugins)})")
        return False

    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python test_config_disabling.py <plugin_to_disable>")
        sys.exit(1)

    disabled = sys.argv[1]
    success = check_disable_plugin(disabled)

    sys.exit(0 if success else 1)
