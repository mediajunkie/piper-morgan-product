# Distribution Sprint — Epic and Issue Specifications

**Sprint**: DIST — Distribution Packaging
**Milestone**: Post-MVP (after M6 Security Hardening)
**Labels**: `distribution`, `packaging`, `infrastructure`
**Total Effort**: 5-8 weeks (Phase 1: 2-3 weeks, Phase 2: 3-5 weeks)
**Reference**: Architect/PPM distribution consensus (Feb 20, 2026)

---

## Epic: DIST — Distribution Packaging

**Title**: EPIC: DIST — Distribution Packaging (MCP-Native + Desktop)

### Description

Package Piper Morgan for distribution beyond source-based alpha testing. Two phases:

1. **MCP-Native**: Publish Piper as an MCP server package that integrates with Claude Desktop, VS Code, and other MCP clients
2. **Desktop Download**: Self-contained desktop application with local database and auto-updates

**Strategic rationale**: MCP-native first positions us for the emerging pattern of fluid UI surfaces while being the lightest path to broader distribution. Desktop follows for users who want a standalone experience.

**Vision**: Users can run Piper without cloning a repo or managing Python environments.

### Success Criteria

- [ ] Piper installable via `npm install` or `pip install`
- [ ] Works with Claude Desktop out of the box
- [ ] Desktop app runs on macOS, Windows, Linux
- [ ] Auto-updates without user intervention
- [ ] First-run experience handles API key setup
- [ ] No PostgreSQL required (SQLite for desktop)

### Child Issues

**Phase 1 — MCP-Native**:
- [ ] DIST-MCP-PACKAGE
- [ ] DIST-MCP-DOCS
- [ ] DIST-MCP-REGISTRY
- [ ] DIST-MCP-TEST

**Phase 2 — Desktop**:
- [ ] DIST-SQLITE
- [ ] DIST-WRAPPER
- [ ] DIST-UPDATE
- [ ] DIST-INSTALLER
- [ ] DIST-FIRST-RUN

---

## Phase 1: MCP-Native (2-3 weeks)

### DIST-MCP-PACKAGE

**Title**: DIST-MCP-PACKAGE: Package Piper as MCP server

**Type**: Feature
**Priority**: P0
**Effort**: 3-5 days
**Labels**: `distribution`, `mcp`, `packaging`

#### Description

Create installable packages (npm and/or pip) that allow users to run Piper as an MCP server.

**Current state**: Piper's MCP server works but requires source checkout and manual setup.

**Target state**: `pip install piper-morgan` or `npx piper-morgan` starts a working MCP server.

#### Requirements

1. **Package structure**
   - Determine primary package format (pip vs npm vs both)
   - Entry point that starts MCP server
   - Bundled dependencies (no separate install steps)

2. **Configuration**
   - Environment variable support for API keys
   - Config file discovery (~/.piper/config.yml or similar)
   - Sensible defaults for MCP-only mode

3. **MCP-only mode**
   - Skip web UI components
   - Minimal dependencies for MCP operation
   - Fast startup time

#### Acceptance Criteria

- [ ] Package published to test registry (TestPyPI or npm --dry-run)
- [ ] `pip install piper-morgan && piper-morgan serve` starts MCP server
- [ ] Server responds to MCP protocol handshake
- [ ] API key configurable via environment variable
- [ ] Startup time < 5 seconds
- [ ] Package size reasonable (< 50MB)

#### Technical Notes

- Consider `pyproject.toml` with optional dependency groups
- May need to stub/skip PostgreSQL in MCP-only mode
- Existing MCP server code is in `services/mcp/`

---

### DIST-MCP-DOCS

**Title**: DIST-MCP-DOCS: Integration documentation for MCP clients

**Type**: Documentation
**Priority**: P0
**Effort**: 2-3 days
**Labels**: `distribution`, `mcp`, `documentation`
**Depends on**: DIST-MCP-PACKAGE

#### Description

Create user-facing documentation for integrating Piper with MCP clients.

#### Requirements

1. **Quick start guide**
   - Installation (one command)
   - Configuration (API keys)
   - Adding to Claude Desktop config
   - First conversation

2. **Client-specific guides**
   - Claude Desktop (primary)
   - VS Code with Continue/similar
   - Generic MCP client setup

3. **Troubleshooting**
   - Common errors and fixes
   - Log locations
   - How to report issues

4. **Feature reference**
   - Available tools
   - What Piper can do via MCP
   - Limitations vs full web UI

#### Acceptance Criteria

- [ ] README in package with quick start
- [ ] Dedicated docs page on pipermorgan.ai
- [ ] Claude Desktop config example (copy-paste ready)
- [ ] Troubleshooting covers top 5 expected issues
- [ ] Screenshots/GIFs showing working integration

---

### DIST-MCP-REGISTRY

**Title**: DIST-MCP-REGISTRY: Publish to package registries

**Type**: Infrastructure
**Priority**: P1
**Effort**: 1-2 days
**Labels**: `distribution`, `mcp`, `infrastructure`
**Depends on**: DIST-MCP-DOCS

#### Description

Publish Piper to public package registries and any MCP-specific marketplaces.

#### Requirements

1. **PyPI publication**
   - Account setup
   - Package metadata (description, keywords, classifiers)
   - Release workflow (GitHub Actions)

2. **MCP registry** (if exists)
   - Research current MCP tool discovery mechanisms
   - Submit to any official/community registries

3. **Versioning**
   - Semantic versioning aligned with main releases
   - Changelog in package

#### Acceptance Criteria

- [ ] `pip install piper-morgan` works from PyPI
- [ ] Package page shows correct metadata
- [ ] GitHub Actions workflow for releases
- [ ] Listed in MCP registry/directory (if applicable)

---

### DIST-MCP-TEST

**Title**: DIST-MCP-TEST: Integration testing with MCP clients

**Type**: Testing
**Priority**: P1
**Effort**: 2-3 days
**Labels**: `distribution`, `mcp`, `testing`
**Depends on**: DIST-MCP-PACKAGE

#### Description

Verify Piper works correctly with target MCP clients.

#### Requirements

1. **Claude Desktop testing**
   - Fresh install flow
   - All tools register correctly
   - Conversation flows work
   - Error handling (API key missing, etc.)

2. **VS Code testing**
   - Integration with MCP-compatible extensions
   - Tool invocation works

3. **Automated smoke tests**
   - CI workflow that tests MCP handshake
   - Tool registration verification

#### Acceptance Criteria

- [ ] Manual test checklist for Claude Desktop (10+ scenarios)
- [ ] Manual test checklist for VS Code (5+ scenarios)
- [ ] CI smoke test for MCP protocol compliance
- [ ] Known issues documented

---

## Phase 2: Desktop Download (3-5 weeks)

### DIST-SQLITE

**Title**: DIST-SQLITE: SQLite adapter for repositories

**Type**: Feature
**Priority**: P0
**Effort**: 5-8 days
**Labels**: `distribution`, `desktop`, `database`

#### Description

Create SQLite backend for all repositories, enabling Piper to run without PostgreSQL.

**Current state**: All repositories assume PostgreSQL with asyncpg.

**Target state**: Repository layer supports both PostgreSQL and SQLite via configuration.

#### Requirements

1. **Repository abstraction**
   - Verify current repository interfaces are DB-agnostic
   - Create SQLite implementations where needed
   - Factory pattern for backend selection

2. **SQLite-specific handling**
   - Async SQLite (aiosqlite)
   - Schema migrations for SQLite
   - JSON field handling (SQLite vs JSONB)
   - DateTime handling differences

3. **Configuration**
   - `DATABASE_TYPE=sqlite|postgresql` environment variable
   - SQLite file location configurable
   - Default: `~/.piper/piper.db`

4. **Data migration** (optional, P2)
   - Export from PostgreSQL
   - Import to SQLite
   - For users transitioning

#### Acceptance Criteria

- [ ] All repositories work with SQLite backend
- [ ] Existing tests pass with SQLite
- [ ] New tests for SQLite-specific edge cases
- [ ] Schema migrations work for SQLite
- [ ] Performance acceptable (< 2x PostgreSQL for common operations)

#### Technical Notes

- May need to handle `JSONB` → `JSON` text
- `timestamptz` → SQLite datetime handling
- Consider SQLAlchemy for unified interface

---

### DIST-WRAPPER

**Title**: DIST-WRAPPER: Desktop application wrapper

**Type**: Feature
**Priority**: P0
**Effort**: 5-8 days
**Labels**: `distribution`, `desktop`, `packaging`
**Depends on**: DIST-SQLITE

#### Description

Create desktop application wrapper using Electron or Tauri.

#### Requirements

1. **Framework selection**
   - Evaluate Electron vs Tauri
   - Tauri preferred (smaller, Rust-based) if feasible
   - Decision documented in ADR

2. **Application structure**
   - Bundles Python runtime (or uses system Python?)
   - Starts backend server on launch
   - Opens web UI in application window
   - System tray presence (optional)

3. **Platform support**
   - macOS (Intel + Apple Silicon)
   - Windows (x64)
   - Linux (x64, AppImage or .deb)

4. **Development workflow**
   - Hot reload for development
   - Debug mode with dev tools

#### Acceptance Criteria

- [ ] Application launches on all 3 platforms
- [ ] Web UI accessible in app window
- [ ] Backend starts automatically
- [ ] Clean shutdown (no orphan processes)
- [ ] Application icon and branding

---

### DIST-UPDATE

**Title**: DIST-UPDATE: Auto-update mechanism

**Type**: Feature
**Priority**: P1
**Effort**: 3-5 days
**Labels**: `distribution`, `desktop`, `infrastructure`
**Depends on**: DIST-WRAPPER

#### Description

Implement automatic updates for the desktop application.

#### Requirements

1. **Update checking**
   - Check for updates on startup (configurable)
   - Check periodically while running
   - Respect user preference to disable

2. **Update flow**
   - Download in background
   - Notify user when ready
   - Apply on next restart (or offer immediate restart)
   - Rollback if update fails

3. **Update server**
   - Host releases (GitHub Releases or dedicated)
   - Signed updates for security
   - Delta updates if feasible (reduce download size)

#### Acceptance Criteria

- [ ] App detects when update is available
- [ ] User can install update with one click
- [ ] Update applies cleanly without data loss
- [ ] User can disable auto-update
- [ ] Rollback works if update corrupts

---

### DIST-INSTALLER

**Title**: DIST-INSTALLER: Platform installers

**Type**: Feature
**Priority**: P1
**Effort**: 3-5 days
**Labels**: `distribution`, `desktop`, `packaging`
**Depends on**: DIST-WRAPPER

#### Description

Create native installers for each platform.

#### Requirements

1. **macOS**
   - DMG with drag-to-Applications
   - Code signing (Apple Developer account)
   - Notarization for Gatekeeper

2. **Windows**
   - MSI or NSIS installer
   - Code signing (certificate)
   - Start menu integration

3. **Linux**
   - AppImage (universal)
   - Optional: .deb for Debian/Ubuntu
   - Desktop entry file

4. **CI/CD**
   - GitHub Actions builds installers
   - Artifacts attached to releases

#### Acceptance Criteria

- [ ] macOS: Signed, notarized DMG
- [ ] Windows: Signed installer, clean install/uninstall
- [ ] Linux: AppImage runs on major distros
- [ ] All installers < 150MB
- [ ] CI workflow produces all installers on release

---

### DIST-FIRST-RUN

**Title**: DIST-FIRST-RUN: First-run experience

**Type**: Feature
**Priority**: P1
**Effort**: 2-3 days
**Labels**: `distribution`, `desktop`, `ux`
**Depends on**: DIST-WRAPPER

#### Description

Create a smooth first-run experience for new desktop users.

#### Requirements

1. **API key setup**
   - Prompt for Anthropic API key
   - Link to get API key if needed
   - Validate key before proceeding
   - Secure storage (system keychain)

2. **Optional integrations**
   - GitHub token (if using GitHub features)
   - Slack token (if using Slack features)
   - Skip option for each

3. **Initial configuration**
   - Choose data directory (default ~/.piper)
   - Optional: Import from existing installation

4. **Welcome flow**
   - Brief tour of capabilities
   - First conversation prompt
   - Link to documentation

#### Acceptance Criteria

- [ ] New user can go from install to first conversation in < 3 minutes
- [ ] API key stored securely (not in plain text)
- [ ] Can skip optional integrations
- [ ] Clear error messages for invalid keys
- [ ] Welcome flow is skippable

---

## Sprint Sequencing

**Recommended placement**: After M6 (MVP Security Hardening)

```
M0 ✅ → M1 → M2 → M3 → M4 → M5 → M6 → DIST-Phase1 → DIST-Phase2 → Beta
```

**Dependencies within DIST**:

```
Phase 1 (MCP-Native):
DIST-MCP-PACKAGE → DIST-MCP-DOCS → DIST-MCP-REGISTRY
                → DIST-MCP-TEST

Phase 2 (Desktop):
DIST-SQLITE → DIST-WRAPPER → DIST-UPDATE
                           → DIST-INSTALLER
                           → DIST-FIRST-RUN
```

---

## Open Questions

1. **Package name**: `piper-morgan`? `pipermorgan`? Check availability on PyPI/npm.

2. **Electron vs Tauri**: Needs investigation. Tauri is lighter but may have Python bundling challenges.

3. **Python bundling**: Bundle Python runtime (larger, more reliable) or require system Python (smaller, potential version issues)?

4. **Signing certificates**: Need Apple Developer account ($99/year) and Windows code signing cert (~$200-400/year).

---

*Ready for GitHub issue creation and roadmap placement.*
