"""
Plugin Registry for Piper Integration Plugins

Manages plugin registration, lifecycle, and discovery.
Singleton pattern ensures global registry instance.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from .plugin_interface import PiperPlugin, PluginMetadata

# 1690: the demo template plugin mounts live example routes
# (/api/v1/integrations/demo/*) and must NOT ship in a default deployment.
# It is excluded from the no-config "enable everything" default unless this
# env var opts in (dev/demo walkthroughs), or config/PIPER.user.md lists it
# explicitly under plugins.enabled (an explicit choice is always honored).
DEMO_PLUGIN_ENV = "PIPER_DEMO_PLUGIN"


def demo_plugin_opted_in() -> bool:
    """True when the operator explicitly opted in to the demo template plugin."""
    return os.getenv(DEMO_PLUGIN_ENV, "").strip().lower() in {"1", "true", "yes"}


class PluginRegistry:
    """
    Manages plugin registration, lifecycle, and discovery.

    Singleton registry that all plugins register with at startup.
    Provides plugin lookup, health checks, and lifecycle management.

    Usage:
        registry = get_plugin_registry()
        registry.register(my_plugin)
        await registry.initialize_all()
        routers = registry.get_routers()
    """

    def __init__(self):
        """Initialize empty registry"""
        self._plugins: Dict[str, PiperPlugin] = {}
        self._initialized: bool = False
        self.logger = logging.getLogger(__name__)

    def register(self, plugin: PiperPlugin) -> None:
        """
        Register a plugin with the registry.

        Args:
            plugin: Plugin instance to register

        Raises:
            ValueError: If plugin name already registered
            TypeError: If plugin doesn't implement PiperPlugin
        """
        if not isinstance(plugin, PiperPlugin):
            raise TypeError(f"Plugin must implement PiperPlugin interface")

        metadata = plugin.get_metadata()

        if metadata.name in self._plugins:
            raise ValueError(f"Plugin '{metadata.name}' already registered")

        self._plugins[metadata.name] = plugin
        self.logger.info(
            f"Registered plugin: {metadata.name} v{metadata.version}",
            extra={
                "plugin_name": metadata.name,
                "plugin_version": metadata.version,
                "capabilities": metadata.capabilities,
            },
        )

    def unregister(self, plugin_name: str) -> bool:
        """
        Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            bool: True if unregistered, False if not found
        """
        if plugin_name in self._plugins:
            del self._plugins[plugin_name]
            self.logger.info(f"Unregistered plugin: {plugin_name}")
            return True
        return False

    def get_plugin(self, name: str) -> Optional[PiperPlugin]:
        """
        Get plugin by name.

        Args:
            name: Plugin name

        Returns:
            Optional[PiperPlugin]: Plugin instance or None if not found
        """
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """
        List all registered plugin names.

        Returns:
            List[str]: List of plugin names
        """
        return list(self._plugins.keys())

    def get_all_plugins(self) -> Dict[str, PiperPlugin]:
        """
        Get all registered plugins.

        Returns:
            Dict[str, PiperPlugin]: Copy of plugins dictionary
        """
        return self._plugins.copy()

    def get_plugin_count(self) -> int:
        """
        Get count of registered plugins.

        Returns:
            int: Number of registered plugins
        """
        return len(self._plugins)

    async def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all registered plugins.

        Calls initialize() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.initialize()
                self.logger.info(f"Initialized plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to initialize plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )
                results[name] = False

        self._initialized = True
        return results

    async def shutdown_all(self) -> Dict[str, bool]:
        """
        Shutdown all registered plugins.

        Calls shutdown() on each plugin. Continues even if some fail.

        Returns:
            Dict[str, bool]: Map of plugin name to success status
        """
        results = {}

        for name, plugin in self._plugins.items():
            try:
                await plugin.shutdown()
                self.logger.info(f"Shutdown plugin: {name}")
                results[name] = True
            except Exception as e:
                self.logger.error(
                    f"Failed to shutdown plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )
                results[name] = False

        self._initialized = False
        return results

    def get_routers(self) -> List[APIRouter]:
        """
        Get all plugin routers for mounting.

        Returns:
            List[APIRouter]: List of routers from plugins that provide them
        """
        routers = []

        for name, plugin in self._plugins.items():
            try:
                router = plugin.get_router()
                if router is not None:
                    routers.append(router)
                    self.logger.debug(f"Added router from plugin: {name}")
            except Exception as e:
                self.logger.error(
                    f"Failed to get router from plugin: {name}",
                    extra={"error": str(e), "plugin_name": name},
                )

        return routers

    def get_status_all(self) -> Dict[str, Dict]:
        """
        Get status of all plugins.

        Returns:
            Dict[str, Dict]: Map of plugin name to status dict
        """
        status = {}

        for name, plugin in self._plugins.items():
            try:
                plugin_status = plugin.get_status()
                status[name] = plugin_status
            except Exception as e:
                status[name] = {"error": str(e), "status": "error"}

        return status

    def get_plugins_with_capability(self, capability: str) -> List[PiperPlugin]:
        """
        Get all plugins with a specific capability.

        Args:
            capability: Capability to filter by (e.g., "routes", "webhooks")

        Returns:
            List[PiperPlugin]: Plugins with the specified capability
        """
        plugins = []

        for plugin in self._plugins.values():
            metadata = plugin.get_metadata()
            if capability in metadata.capabilities:
                plugins.append(plugin)

        return plugins

    def is_initialized(self) -> bool:
        """
        Check if registry has been initialized.

        Returns:
            bool: True if initialize_all() has been called
        """
        return self._initialized

    def discover_plugins(self) -> Dict[str, str]:
        """
        Discover available plugins by scanning integrations directory.

        Scans services/integrations/*/ for *_plugin.py files and returns
        a mapping of plugin names to their module paths.

        Returns:
            Dict[str, str]: Map of plugin name to module path
            Example: {
                "slack": "services.integrations.slack.slack_plugin",
                "github": "services.integrations.github.github_plugin"
            }

        Note:
            - Only discovers plugins, does not load them
            - Ignores files that don't match *_plugin.py pattern
            - Returns empty dict if integrations directory not found
        """
        from pathlib import Path

        plugins = {}
        base_path = Path("services/integrations")

        if not base_path.exists():
            self.logger.warning(f"Integrations directory not found: {base_path}")
            return plugins

        # Scan each subdirectory in integrations
        for integration_dir in base_path.iterdir():
            if not integration_dir.is_dir():
                continue

            # Look for *_plugin.py files
            for plugin_file in integration_dir.glob("*_plugin.py"):
                # Extract plugin name from filename
                # Example: slack_plugin.py -> slack
                plugin_name = plugin_file.stem.replace("_plugin", "")

                # Build module path
                # Example: services.integrations.slack.slack_plugin
                module_path = f"services.integrations.{integration_dir.name}.{plugin_file.stem}"

                plugins[plugin_name] = module_path
                self.logger.debug(
                    f"Discovered plugin: {plugin_name} at {module_path}",
                    extra={"plugin_name": plugin_name, "module_path": module_path},
                )

        self.logger.info(
            f"Discovery complete: found {len(plugins)} plugin(s)",
            extra={"plugin_count": len(plugins), "plugins": list(plugins.keys())},
        )

        return plugins

    def load_plugin(self, name: str, module_path: str) -> bool:
        """
        Dynamically load and register a plugin.

        Uses importlib to import the plugin module, which triggers
        auto-registration via the module's _plugin instance.

        Args:
            name: Plugin name (e.g., "slack")
            module_path: Full module path (e.g., "services.integrations.slack.slack_plugin")

        Returns:
            bool: True if loaded successfully, False otherwise

        Note:
            - Import triggers auto-registration (plugin registers itself)
            - Plugin must already be registered after import
            - Handles import errors gracefully
        """
        import importlib

        try:
            # Check if plugin is already loaded
            if name in self._plugins:
                self.logger.info(f"Plugin {name} already loaded", extra={"plugin_name": name})
                return True

            self.logger.info(
                f"Loading plugin: {name}", extra={"plugin_name": name, "module_path": module_path}
            )

            # Import the module - this triggers auto-registration
            # Note: If module is already in sys.modules, this won't re-execute the module code
            module = importlib.import_module(module_path)

            # Handle case where module was already imported but plugin not registered
            # This can happen if the registry was reset after the module was imported
            import sys

            if module_path in sys.modules and name not in self._plugins:
                # Module exists but plugin not registered - try to get the plugin instance
                if hasattr(module, f"_{name}_plugin"):
                    plugin_instance = getattr(module, f"_{name}_plugin")
                    self.register(plugin_instance)
                    self.logger.info(f"Re-registered existing plugin: {name}")
                else:
                    self.logger.warning(
                        f"Module {module_path} imported but no plugin instance found"
                    )

            # Verify plugin was registered
            if name not in self._plugins:
                self.logger.error(
                    f"Plugin {name} failed to register after import. Registry has: {list(self._plugins.keys())}",
                    extra={
                        "plugin_name": name,
                        "module_path": module_path,
                        "registered_plugins": list(self._plugins.keys()),
                    },
                )
                return False

            self.logger.info(f"Successfully loaded plugin: {name}", extra={"plugin_name": name})
            return True

        except ImportError as e:
            self.logger.error(
                f"Failed to import plugin {name}: {e}",
                extra={"plugin_name": name, "module_path": module_path, "error": str(e)},
            )
            return False
        except Exception as e:
            self.logger.error(
                f"Unexpected error loading plugin {name}: {e}",
                extra={"plugin_name": name, "module_path": module_path, "error": str(e)},
            )
            return False

    def _read_plugin_config(self) -> Dict[str, Any]:
        """
        Read plugin configuration from PIPER.user.md.

        Extracts YAML block from Plugin Configuration section.

        Returns:
            Dict containing plugin config, or empty dict if not found

        Default Behavior:
            - If config file missing: return empty dict
            - If plugin section missing: return empty dict
            - If YAML invalid: log error, return empty dict
        """
        from pathlib import Path
        from typing import Any

        import yaml

        config_path = Path("config/PIPER.user.md")

        if not config_path.exists():
            self.logger.warning("Config file not found: config/PIPER.user.md")
            return {}

        try:
            content = config_path.read_text()

            # Find Plugin Configuration section
            if "## " not in content or "Plugin Configuration" not in content:
                self.logger.debug("No Plugin Configuration section found")
                return {}

            # Extract YAML block after Plugin Configuration header
            lines = content.split("\n")
            in_plugin_section = False
            in_yaml_block = False
            yaml_lines = []

            for line in lines:
                if "Plugin Configuration" in line and line.strip().startswith("##"):
                    in_plugin_section = True
                    continue

                if in_plugin_section:
                    # End of section if we hit another ## header
                    if line.startswith("## ") and "Plugin Configuration" not in line:
                        break

                    # Start of YAML block
                    if "```yaml" in line:
                        in_yaml_block = True
                        continue

                    # End of YAML block
                    if in_yaml_block and "```" in line:
                        break

                    # Collect YAML lines
                    if in_yaml_block:
                        yaml_lines.append(line)

            if not yaml_lines:
                self.logger.debug("No YAML block found in Plugin Configuration")
                return {}

            # Parse YAML
            yaml_content = "\n".join(yaml_lines)
            config = yaml.safe_load(yaml_content)

            self.logger.info("Loaded plugin configuration", extra={"config": config})
            return config or {}

        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in plugin configuration: {e}", extra={"error": str(e)})
            return {}
        except Exception as e:
            self.logger.error(f"Error reading plugin configuration: {e}", extra={"error": str(e)})
            return {}

    def get_enabled_plugins(self) -> List[str]:
        """
        Get list of enabled plugins from configuration.

        Returns:
            List of enabled plugin names

        Default Behavior:
            - If no config: return all discovered plugins (backwards compatible)
              EXCEPT the demo template plugin, which requires explicit opt-in
              via PIPER_DEMO_PLUGIN=1 or a plugins.enabled listing (#1690)
            - If config exists but no enabled list: same as no config
            - If empty enabled list: return empty list (all plugins disabled)
        """
        config = self._read_plugin_config()

        # Get enabled list from config
        if "plugins" in config and "enabled" in config["plugins"]:
            enabled = config["plugins"]["enabled"]
            self.logger.info(
                f"Enabled plugins from config: {enabled}",
                extra={"enabled_plugins": enabled},
            )
            return enabled if enabled is not None else []

        # Default: all discovered plugins enabled — except the demo template
        # plugin, which must not mount live routes in a default deployment
        # (1690). Opt in with PIPER_DEMO_PLUGIN=1 or list it explicitly under
        # plugins.enabled in config/PIPER.user.md.
        available = self.discover_plugins()
        all_plugins = list(available.keys())

        if "demo" in all_plugins and not demo_plugin_opted_in():
            all_plugins.remove("demo")
            self.logger.info(
                "Demo plugin excluded from default-enabled set "
                f"(set {DEMO_PLUGIN_ENV}=1 to enable)",
                extra={"excluded_plugin": "demo"},
            )

        self.logger.info(
            f"No config found, enabling all discovered plugins: {all_plugins}",
            extra={"enabled_plugins": all_plugins},
        )
        return all_plugins

    def load_enabled_plugins(self) -> Dict[str, bool]:
        """
        Discover and load only enabled plugins.

        Combines discovery, config reading, and selective loading.

        Returns:
            Dict mapping plugin name to load success status

        Process:
            1. Discover available plugins
            2. Read enabled list from config
            3. Load only enabled plugins
            4. Log results
        """
        # Discover what's available
        available = self.discover_plugins()

        if not available:
            self.logger.warning("No plugins discovered")
            return {}

        # Get enabled list
        enabled = self.get_enabled_plugins()

        # Load enabled plugins
        results = {}
        for plugin_name in enabled:
            if plugin_name not in available:
                self.logger.warning(
                    f"Enabled plugin not found: {plugin_name}",
                    extra={
                        "plugin_name": plugin_name,
                        "available": list(available.keys()),
                    },
                )
                results[plugin_name] = False
                continue

            module_path = available[plugin_name]
            success = self.load_plugin(plugin_name, module_path)
            results[plugin_name] = success

        # Log summary
        success_count = sum(1 for success in results.values() if success)
        self.logger.info(
            f"Plugin loading complete: {success_count}/{len(results)} successful",
            extra={"results": results},
        )

        return results


# Global registry instance (singleton)
_registry: Optional[PluginRegistry] = None


def get_plugin_registry() -> PluginRegistry:
    """
    Get the global plugin registry (singleton).

    Returns:
        PluginRegistry: Global registry instance
    """
    global _registry
    if _registry is None:
        _registry = PluginRegistry()
    return _registry


def reset_plugin_registry() -> None:
    """
    Reset the global plugin registry.

    Used primarily for testing. Creates a fresh registry instance.
    """
    global _registry
    _registry = PluginRegistry()
