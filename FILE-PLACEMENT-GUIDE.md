# File Placement Guide

**Purpose**: Prevent root directory clutter by establishing clear placement rules
**Created**: October 5, 2025
**Authority**: PM decision - no files in root without permission

---

## 🚫 Root Directory Rules

**CRITICAL**: No new files may be placed in the project root without explicit PM permission.

### Files That Belong in Root
- Core startup scripts: `main.py`, `start-piper.sh`, `stop-piper.sh`
- Essential project docs: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CLAUDE.md`
- Core configuration: `.env.example`, `.gitignore`, `Makefile`, `pyproject.toml`
- Container config: `docker-compose.yml`, `Dockerfile`
- Package files: `package.json`, `tsconfig.json` (for web components)
- PM convenience scripts: `ba.sh` (marked with "do not move" comment)

### Pending Chief Architect Review
- `credentials.json`, `token.json` (Google OAuth - may move to config/)
- `methodology/` directory (Python implementation code - may move to services/)

---

## 📁 Where Files Should Go

### Development & Testing
- **Test scripts** → `tests/` or appropriate subdirectory
- **Test fixtures/data** → `tests/fixtures/`
- **Development scripts** → `scripts/`
- **Development logs** → `logs/` or `dev/YYYY/MM/DD/`
- **Coverage reports** → `dev/YYYY/MM/DD/` with date
- **Temporary test files** → `tests/` or `/tmp/`

### Documentation (Per NAVIGATION.md Structure)
- **ADRs** → `docs/internal/architecture/adrs/`
- **Planning docs** → `docs/internal/planning/current/`
- **Session logs** → `dev/YYYY/MM/DD/` or `docs/internal/development/session-logs/`
- **Omnibus logs** → `docs/omnibus-logs/`
- **Methodology docs** → `docs/internal/development/methodology-core/`
- **Decision logs** → `docs/internal/architecture/decisions/`
- **Pattern docs** → `docs/internal/architecture/patterns/`

### Configuration & Credentials
- **User config** → `config/` (PIPER.user.md, etc.)
- **Environment files** → Root only if essential, otherwise `config/`
- **OAuth/API credentials** → Under Chief Architect review (currently root)
- **Settings files** → `.claude/` for Claude-specific, `config/` for project

### Code & Services
- **Service code** → `services/` with appropriate subdirectory
- **Integration code** → `services/integrations/`
- **Plugin code** → `services/integrations/*/[name]_plugin.py`
- **Web/API code** → `web/`
- **CLI commands** → `cli/commands/`
- **Shared utilities** → `shared/` or `tools/`

### Data & Archives
- **Analysis data** → `dev/analysis/` or dated subdirectory
- **Archived files** → `archive/`
- **Deprecated files** → `trash/` (for temporary holding before deletion)
- **Historical data** → `archive/` or `data/archive/`
- **Upload storage** → `archive/uploads/` (not root)

### Assets & Resources
- **Images/logos** → `docs/assets/` or `public/assets/`
- **Templates** → `templates/`
- **Static web assets** → `web/assets/` or `public/`

---

## 🎯 Quick Decision Tree

When adding a new file, ask:

1. **Is this a test file?** → `tests/`
2. **Is this a script?** → `scripts/`
3. **Is this documentation?** → `docs/` (follow NAVIGATION.md structure)
4. **Is this configuration?** → `config/` (unless core project config)
5. **Is this service code?** → `services/`
6. **Is this temporary?** → `/tmp/` or `tests/`
7. **Is this a log/output?** → `logs/` or `dev/YYYY/MM/DD/`
8. **Is this historical?** → `archive/`
9. **Still unsure?** → Ask PM or Chief Architect

---

## 🛠️ Agent Instructions

### For Development Agents
- Create test files in `tests/`, not root
- Place working documents in `dev/` with appropriate date structure
- Use `/tmp/` for truly temporary files that don't need persistence
- Never create new files in root without explicit permission

### For Documentation Agents
- Follow NAVIGATION.md structure strictly
- Session logs go in `dev/YYYY/MM/DD/` or `docs/internal/development/session-logs/`
- Omnibus logs go in `docs/omnibus-logs/`
- Always check existing structure before creating new directories

### For All Agents
- When in doubt, propose location and ask for confirmation
- Check this guide before placing any new file
- If a file type isn't covered here, ask before creating

---

## 📋 Recent Cleanup Reference

On October 5, 2025, we moved 45+ files out of root:
- Scripts moved to `scripts/`
- Test files moved to `tests/`
- Logs moved to `logs/`
- Historical data moved to `archive/`
- Outdated files moved to `trash/`

This cleanup demonstrates the proper placement for common file types.

---

*Last Updated: October 5, 2025*
*Next Review: When Chief Architect resolves pending items*
