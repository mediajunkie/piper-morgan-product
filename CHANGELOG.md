# Changelog

All notable changes to the Piper Morgan project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.0.0] - 2026-10-31 — private beta

MVP milestone closed 2026-10-30; first 0.9 release. Full notes:
[docs/releases/RELEASE-NOTES-v0.9.0.0.md](docs/releases/RELEASE-NOTES-v0.9.0.0.md)
The GREAT-3B block below was carried in `[Unreleased]`
since 2025-10-03 and shipped in 0.8.x releases without a label; it stays here as history.

### Added - GREAT-3B (2025-10-03)
- Dynamic plugin discovery system
- Config-based plugin enabling/disabling via PIPER.user.md
- Enhanced plugin loading with detailed status reporting
- Plugin configuration section in user config
- Comprehensive plugin system documentation (PLUGIN-SYSTEM-GUIDE.md)
- 14 new plugin system tests (total: 48)

### Changed - GREAT-3B
- Replaced static plugin imports with dynamic loading in web/app.py
- Enhanced startup logging for plugin system with per-plugin status
- Improved error handling for plugin failures (graceful degradation)
- Updated plugin system README with GREAT-3B enhancements

### Technical - GREAT-3B
- Added `discover_plugins()` method to PluginRegistry
- Added `load_plugin()` method with importlib support
- Added `load_enabled_plugins()` orchestration method
- Added `get_enabled_plugins()` config reader
- Added `_read_plugin_config()` YAML parser for PIPER.user.md
- Enhanced plugin loading with re-registration support for test environments
- Maintained full backwards compatibility (all plugins enabled by default)

## [Previous Releases]

### Added - GREAT-3A (2025-10-02)
- Plugin system foundation with PiperPlugin interface
- PluginRegistry singleton for plugin management
- Auto-registration system for plugins
- Plugin lifecycle management (initialize/shutdown)
- FastAPI router integration for plugins
- 4 plugin implementations: Slack, GitHub, Notion, Calendar
- Comprehensive plugin interface test suite

### Technical - GREAT-3A
- Created `services/plugins/` directory structure
- Implemented `PiperPlugin` abstract base class
- Created `PluginMetadata` dataclass for plugin information
- Built plugin registry with lifecycle management
- Added plugin auto-registration on module import
- Integrated plugin system into web/app.py startup
