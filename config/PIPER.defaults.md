# PIPER.defaults.md - Product Configuration

**Version**: 1.0.0
**Purpose**: Default product configuration for Piper Morgan AI Assistant
**Status**: Product defaults - do not modify

---

## 🤖 **System Defaults**

**Product Name**: Piper Morgan AI Assistant
**Version**: Production-ready MCP Consumer
**Performance Target**: <150ms response time
**Architecture**: MCP (Model Context Protocol) integration with GitHub

**Core Features**:
- Real-time GitHub integration
- Conversational AI with memory
- Daily standup automation
- Pattern-based development assistance
- Documentation management
- Issue tracking and project management

---

## 🏗️ **Technical Configuration**

**Default File Structure**:
- `config/PIPER.user.md` - User-specific configuration (gitignored)
- `config/PIPER.defaults.md` - Product defaults (this file)
- `config/README.md` - Configuration documentation

**System Patterns**:
- Excellence Flywheel methodology (Verify First, Evidence Required)
- GitHub-first tracking for project management
- Dual-agent coordination for complex tasks
- Complete bookending and documentation

**Performance Specifications**:
- Current achievement: 36.43ms response time
- Target: <150ms for all queries
- Infrastructure: 15,457+ lines of MCP foundation code
- Production code: 2,480+ lines of validated implementation

---

## 📊 **Default Templates**

**Daily Routines Template**:
- Morning: Daily standup with Piper Morgan
- Mid-morning: Development focus time
- Afternoon: UX and improvement work
- Evening: Documentation and handoff preparation

**Priority Structure Template**:
1. Primary project focus (70% allocation)
2. Secondary AI development (25% allocation)
3. Maintenance and knowledge management (5% allocation)

**Knowledge Sources Structure**:
- Pattern Index: `docs/internal/architecture/patterns/`
- Architecture Guides: `docs/internal/architecture/current/`
- User Guides: `docs/public/user-guides/`
- Session Logs: `dev/YYYY/MM/DD/` (dated working documents)

---

## 🔧 **System Configuration Notes**

**How User Configuration Works**:
1. Copy `PIPER.user.md.example` to `PIPER.user.md`
2. Customize user-specific sections (name, role, priorities, etc.)
3. System automatically loads user config, falling back to defaults
4. User config is gitignored for privacy and separation

**Configuration Priority**:
1. User configuration (`PIPER.user.md`) - highest priority
2. Product defaults (this file) - fallback values
3. System defaults - hard-coded minimums

**Hot-Reload**: Configuration changes take effect immediately without restart.

**Version Control**: Product defaults are versioned. User configs are gitignored.

---

## 📝 **Default Response Patterns**

**System Identity**: "I'm Piper Morgan, your AI assistant for product management and development work."

**Default Context Injection**: Product configuration is automatically included in system prompts for consistent behavior.

**Fallback Behavior**: When user configuration is missing, system uses these defaults to maintain functionality.

---

**Status**: Active Product Configuration ✅
**Maintained by**: Piper Morgan Development Team
**Do not modify**: This file contains product defaults only
