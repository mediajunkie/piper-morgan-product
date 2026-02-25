# Internal Documentation Navigation Hub

**Purpose**: Internal development team navigation for restructured documentation
**Audience**: Agents, developers, architects, and internal contributors
**Public Documentation**: See [README.md](README.md) for pmorgan.tech public site

**Last Updated**: January 20, 2026
**Status**: ✅ **Complete Internal Navigation System** - Role-based access for development teams

---

> **Note**: This navigation serves **internal development workflows**. For public project information, getting started guides, and user documentation, visit the main [README.md](README.md) which powers the pmorgan.tech website.

---

## 🚀 Quick Start by Role

### Essential Briefings (Start Here)

- [Lead Developer](../knowledge/BRIEFING-ESSENTIAL-LEAD-DEV.md) - 2.5K tokens
- [Chief Architect](../knowledge/BRIEFING-ESSENTIAL-ARCHITECT.md) - 2.5K tokens
- [Chief of Staff](../knowledge/BRIEFING-ESSENTIAL-CHIEF-STAFF.md) - 2.5K tokens
- [Communications](../knowledge/BRIEFING-ESSENTIAL-COMMS.md) - 2.5K tokens
- [Coding Agent](../knowledge/BRIEFING-ESSENTIAL-AGENT.md) - 2K tokens
- [LLM Support](../knowledge/BRIEFING-ESSENTIAL-LLM.md) - 1K tokens

### Progressive Loading

Each essential briefing includes triggers for loading detailed documentation as needed.

---

## 🧭 Quick Navigation by Role

### 👨‍💼 Product Managers

- **[PR/FAQ (Working Backwards)](internal/design/piper-morgan-prfaq.md)** - Customer-centric product narrative for alignment and stakeholder reviews
- **[Current Planning](internal/planning/current/)** - Active planning cycles and roadmaps
- **[Issue Tracking](internal/planning/current/issues.csv)** - Current PM issue status
- **[Roadmap](internal/planning/roadmap/)** - Strategic planning and milestones
- **[Backlog Management](internal/planning/current/)** - Priority management and organization
- **[Suggestions (pre-issue)](../suggestions/README.md)** - Ideas and change requests before they become issues ([SUGGESTIONS_ted.md](../suggestions/SUGGESTIONS_ted.md))

### 🏗️ Architects

- **[Architecture Hub](internal/architecture/current/)** - Current architectural decisions
- **[Domain Models](internal/architecture/current/models/)** - Hub-and-spoke model documentation
- **[ADRs](internal/architecture/current/adrs/)** - Architectural Decision Records
- **[Patterns](internal/architecture/current/patterns/)** - Established architectural patterns
- **[Technical Evolution](internal/architecture/evolution/)** - Architecture development history
- **[Canonical Queries](internal/architecture/current/canonical-queries.md)** - Reference list of canonical query types (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)
  - See also: [ADR-039 Investigation Appendix](internal/architecture/current/adrs/adr-039-appendix-investigation.md) for routing analysis
  - Test matrix: To be created (validation coverage for all 25 canonical query patterns)

### 🧠 MUX Object Model (Grammar & Consciousness)

The MUX track establishes Piper's unified object model: **"Entities experience Moments in Places"**

**Core Philosophy**:
- **[ADR-045 Object Model](internal/architecture/current/adrs/adr-045-object-model.md)** - Canonical grammar definition (ACCEPTED)
- **[Consciousness Philosophy](internal/architecture/current/consciousness-philosophy.md)** - WHY Piper has a soul (Five Pillars)
- **[Ownership Metaphors](internal/architecture/current/ownership-metaphors.md)** - Mind/Senses/Understanding philosophy

**Implementation Reference**:
- **[ADR-055 Implementation](internal/architecture/current/adrs/adr-055-object-model-implementation.md)** - Technical implementation spec
- **[Grammar Compliance Audit](internal/architecture/current/grammar-compliance-audit.md)** - 16 features assessed for compliance
- **[Feature Object Model Map](internal/architecture/current/feature-object-model-map.md)** - Feature-to-grammar mappings with canonical queries

**Patterns** (in `patterns/`):
- **[Grammar Application Patterns](internal/architecture/current/patterns/grammar-application-patterns.md)** - Index of 5 MUX patterns
- pattern-050: Context/Dataclass Pair
- pattern-051: Parallel Place Gathering
- pattern-052: Personality Bridge
- pattern-053: Warmth Calibration
- pattern-054: Honest Failure

**Developer Guides** (in `development/`):
- **[Grammar Transformation Guide](internal/development/grammar-transformation-guide.md)** - HOW to transform features
- **[Grammar Onboarding Checklist](internal/development/grammar-onboarding-checklist.md)** - Developer onboarding
- **[MUX Implementation Guide](internal/development/mux-implementation-guide.md)** - Technical implementation
- **[MUX Experience Tests](internal/development/mux-experience-tests.md)** - Consciousness test criteria

### 👨‍💻 Developers

- **[Development Tools](internal/development/tools/)** - Setup guides and development workflows
- **[Active Work](internal/development/active/)** - Current development status
- **[Methodology](internal/development/methodology-core/)** - Development methodologies (20 core patterns)
- **[Methodology Index](internal/development/methodology-core/INDEX.md)** - Comprehensive methodology navigation
- **[Gameplan Template](internal/development/methodology-core/gameplan-template.md)** - Issue implementation gameplan template (v9.3)
- **[Testing Procedures](internal/development/testing/)** - E2E bug protocol, testing guides, and procedures
- **[Session Templates](internal/development/tools/session-log-templates/)** - Session documentation

### 🚀 DevOps / Release Engineering

- **[CI/CD Smoke Test Runbook](internal/operations/ci-cd-smoke-test-runbook.md)** - Smoke test suite deployment and operations guide
- **[Deployment Operations](internal/operations/deployment/)** - Production deployment procedures
- **[Legacy Runbooks](internal/operations/legacy-operations/)** - Archived operational procedures

### 📚 Researchers & Historians

- **[Session Logs Archive](../dev/2025/)** - Chronological development history (dev/2025/MM/DD/ structure)
- **[Omnibus Logs](omnibus-logs/)** - Weekly/monthly session consolidations (100+ logs)
- **[Development Logs](internal/development/active/)** - Active development work and status files

### 👥 External Users

- **[Getting Started](public/getting-started/)** - Public onboarding materials
- **[API Reference](public/api-reference/)** - Public API documentation
- **[User Guides](public/user-guides/)** - End-user documentation

### 🧪 Alpha Testers

- **[Alpha Quickstart](ALPHA_QUICKSTART.md)** - Quick 2-5 minute setup guide
- **[Alpha Testing Guide](ALPHA_TESTING_GUIDE.md)** - Comprehensive testing guide
- **[Alpha Known Issues](ALPHA_KNOWN_ISSUES.md)** - Current bugs and feature status
- **[Alpha Agreement](ALPHA_AGREEMENT_v2.md)** - Legal terms and conditions
- **[Email Templates](operations/alpha-onboarding/email-template.md)** - Internal onboarding communications
- **[Setup Screenshots](assets/images/alpha-onboarding/)** - GUI setup wizard screenshots (5 images for documentation)

---

## 📁 Documentation Architecture

### 🔓 Public Documentation (`public/`)

**External-facing content for users and developers**

- Getting started guides and tutorials
- API documentation and references
- User manuals and help content

### 🔒 Internal Documentation (`internal/`)

**Working documents for active development**

#### Development (`internal/development/`)

```
├── active/                    # Current work by status
│   ├── in-progress/          # Active development
│   ├── pending-review/       # Files needing review
│   └── ready-for-integration/ # Completed work
├── methodology-core/         # 20 development methodologies (see INDEX.md)
├── tools/                    # Development tools and guides
└── planning/                 # Current planning cycles
```

#### Architecture (`internal/architecture/`)

```
├── current/                   # Active architectural decisions
│   ├── models/               # Hub-and-spoke model docs (39 models)
│   ├── adrs/                 # Current ADRs
│   ├── patterns/             # Established patterns
│   └── [core-specs]          # API, technical specifications
├── evolution/                # Architectural evolution tracking
└── decisions/                # Decision logs and rationale
```

## Architecture Patterns

- [Pattern-031: Plugin Wrapper](internal/architecture/current/patterns/pattern-031-plugin-wrapper.md) - Adapter pattern for integration routers

## Developer Guides

- [Plugin Development Guide](guides/plugin-development-guide.md) - Step-by-step tutorial for adding integrations
- [Plugin Versioning Policy](guides/plugin-versioning-policy.md) - Semantic versioning guidelines for plugins
- [Plugin Quick Reference](guides/plugin-quick-reference.md) - Cheat sheet for common tasks
- [Intent Classification Guide](guides/intent-classification-guide.md) - Universal intent enforcement developer guide
- [User Context Service](guides/user-context-service.md) - Multi-user context architecture guide
- [Canonical Handlers Architecture](guides/canonical-handlers-architecture.md) - Handler design and capabilities
- [EXECUTION/ANALYSIS Handlers](guides/execution-analysis-handlers.md) - Intent routing to domain services
- [Preference Detection Guide](guides/preference-detection-guide.md) - Developer integration guide for preference detection
- [CLI Publish Command](guides/cli-publish-command.md) - Publish markdown files to various platforms

## Examples

- [Demo Plugin](../services/integrations/demo/) - Complete example integration to copy and adapt

#### Planning (`internal/planning/`)

```
├── current/                  # Active planning cycle
│   ├── data/                 # Planning data and analysis
│   ├── draft-issues/         # Issue development
│   ├── editorial/            # Content planning
│   └── integration/          # Integration planning
├── roadmap/                  # Long-term strategic planning
└── historical/               # Previous planning cycles
```

### 📚 Knowledge Base (`knowledge/`)

**Staging area for claude.ai project knowledge**

Files optimized for RAG search in the claude.ai project knowledge base:

- **BRIEFING-\*** files use prefix for context in flat namespace
- **Symlinked canonical sources** from docs/briefing/ (zero duplication)
- **Workflow**: Update files in docs/briefing/ → automatically syncs to knowledge/ → PM updates claude.ai

```
knowledge/
├── BRIEFING-CURRENT-STATE.md        → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-LEAD-DEV.md   → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-ARCHITECT.md  → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-AGENT.md      → Symlink to docs/briefing/
├── BRIEFING-ESSENTIAL-*.md          → Symlinks to docs/briefing/
├── CLAUDE.md                        # Agent entry point
├── serena-briefing-queries.md       # Live system state queries
└── README.md                        # Knowledge base workflow guide
```

**See**: `knowledge/README.md` for complete workflow documentation

### 📦 Archives & Historical Content

**Historical preservation and archaeological research**

#### Session Logs (`dev/YYYY/MM/DD/`)

Working documents and session logs are stored in date-stamped directories:
```
dev/
├── 2025/                     # Historical year
│   └── MM/DD/               # Date-stamped directories
├── 2026/                     # Current year
│   └── MM/DD/               # Date-stamped directories
└── active/                   # Current working documents
```

#### Omnibus Logs (`docs/omnibus-logs/`)

Weekly/monthly session consolidations - 100+ consolidated logs for historical research.

#### ADRs & Decisions

- **Active ADRs**: `docs/internal/architecture/current/adrs/` (48+ decisions)
- **Patterns**: `docs/internal/architecture/current/patterns/` (33 patterns)

### 🎨 Assets (`assets/` and `docs/assets/`)

**Binary files and multimedia content with size management**

#### Root Assets (`assets/`)
```
├── images/                   # Organized by purpose
│   ├── architecture/         # System diagrams
│   ├── screenshots/          # Development captures
│   └── blog/                 # Blog content (186+ files)
├── diagrams/                 # Source and generated
│   ├── source/               # Editable formats
│   └── generated/            # PNG/SVG outputs
└── documents/                # Templates and exports
    ├── templates/            # Document boilerplates
    └── exports/              # Generated documentation
```

#### Documentation Assets (`docs/assets/`)
```
└── images/                   # Documentation images
    └── alpha-onboarding/     # GUI setup wizard screenshots (5 images)
```
**Note**: `docs/assets/` is for documentation-embedded images (alpha guides, user docs). Root `assets/` is for general project assets.

---

## 🔍 Finding What You Need

### By Work Type

- **Current Tasks**: `internal/development/active/` or `dev/active/`
- **Strategic Planning**: `internal/planning/current/`
- **Technical Decisions**: `internal/architecture/current/`
- **Historical Research**: `dev/YYYY/MM/DD/` and `omnibus-logs/`
- **Asset Management**: `assets/` with inventory and guidelines

### By Time Period

- **Today's Work**: Check `dev/active/` for current session logs
- **Recent History**: `dev/2026/01/` (current month)
- **Project History**: `dev/2025/` (historical sessions)
- **Decision Evolution**: `internal/architecture/evolution/`
- **Weekly Insights**: `omnibus-logs/` (100+ consolidated logs)

### By Content Type

- **Documentation**: Start with role-based navigation above
- **Code References**: `internal/architecture/current/models/`
- **Processes**: `internal/development/methodology-core/`
- **Images/Assets**: `assets/` with inventory in README
- **ADRs**: `internal/architecture/current/adrs/` (48+ decisions)

---

## 🔧 Documentation Workflow

### For Daily Work

1. **Check active status** in relevant `internal/` directory
2. **Review methodology** for process guidance
3. **Create session artifacts** in local `dev/YYYY/MM/DD/` structure
4. **Process to archives** for permanent preservation

### For Research & Investigation

1. **Start with yearly index** for time-based research
2. **Use monthly indices** for detailed period investigation
3. **Cross-reference artifacts** with session logs
4. **Follow agent collaboration** patterns and handoffs
5. **Check omnibus logs** for strategic insights

### For New Content Creation

1. **Determine audience** (public, internal, or archive)
2. **Follow asset guidelines** for binary files
3. **Update navigation** as needed for major additions
4. **Maintain cross-references** between related content

---

## 📊 Restructuring Achievement Summary

### Transformation Completed (September 20, 2025)

- **787 files surveyed** across 104 directories
- **6-phase systematic restructuring** with zero data loss
- **Session log consolidation** with archaeological optimization
- **186+ binary files organized** with size management
- **Role-based navigation** for multiple user types

### Key Organizational Improvements

- ✅ **Clear active/historical separation** across all content types
- ✅ **Session-based archaeological research** with chronological navigation
- ✅ **Asset management** with size compliance and inventory tracking
- ✅ **Multi-role navigation** supporting different user needs
- ✅ **Archaeological research enhancement** with cross-referencing

### Performance Metrics

- **Phase 1**: Foundation architecture (15 min vs 30 min planned)
- **Phase 2**: Session log consolidation (20 min vs 45 min planned)
- **Phase 3**: Development restructuring (45 min vs 60 min planned)
- **Phase 4**: Architecture optimization (20 min vs 30 min planned)
- **Phase 5**: Asset organization (25 min vs 30 min planned)
- **Phase 6**: Navigation system (15 min vs 30 min planned)
- **Total**: 2 hours 20 minutes vs 3.5 hours planned

---

## 🚀 Quick Access Links

### Most Frequently Used

- **[Active Development Work](internal/development/active/)** - What's happening now
- **[Working Documents](../dev/active/)** - Current session logs and working docs
- **[Domain Models Hub](internal/architecture/current/models/models-architecture.md)** - Complete model reference
- **[Methodology Core](internal/development/methodology-core/INDEX.md)** - Development patterns and processes

### For New Team Members

- **[Public Getting Started](public/getting-started/)** - External onboarding
- **[Development Tools](internal/development/tools/)** - Developer setup and guides
- **[Architecture Overview](internal/architecture/current/)** - System understanding
- **[Session Logs](../dev/2025/)** - Historical development context

### For Research & Analysis

- **[Omnibus Logs](omnibus-logs/)** - Strategic insights and weekly summaries (100+ logs)
- **[ADRs](internal/architecture/current/adrs/)** - Architectural decision records (48+)
- **[Patterns Catalog](internal/architecture/current/patterns/)** - Implementation patterns (33)
- **[Session Logs](../dev/)** - Historical development sessions by date

---

## 🆘 Help and Support

### Navigation Issues

- **Can't find specific content?** Check role-based quick navigation above
- **Looking for historical material?** Start with `dev/2025/` or `omnibus-logs/`
- **Need methodology guidance?** Review `internal/development/methodology-core/`
- **Asset questions?** Check `assets/README.md` and `assets/INVENTORY.md`

### Contributing to Documentation

- **Follow organization principles** established in restructuring
- **Maintain archaeological research** capability in changes
- **Use asset guidelines** in `assets/README.md`
- **Update navigation** when adding major new sections

---

_Comprehensive navigation system established: September 20, 2025_
_Supporting role-based access to restructured documentation architecture_
