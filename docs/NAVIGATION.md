# Internal Documentation Navigation Hub

**Purpose**: Internal development team navigation for restructured documentation
**Audience**: Agents, developers, architects, and internal contributors
**Public Documentation**: See [README.md](README.md) for pmorgan.tech public site

**Last Updated**: July 14, 2026
**Status**: ✅ **Complete Internal Navigation System** - Role-based access for development teams

---

> **Note**: This navigation serves **internal development workflows**. For public project information, getting started guides, and user documentation, visit the main [README.md](README.md) which powers the pmorgan.tech website.

---

## 🚀 Quick Start by Role

### Essential Briefings (Start Here)

- [Lead Developer](briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md) - 2.5K tokens
- [Chief Architect](briefing/BRIEFING-ESSENTIAL-ARCHITECT.md) - 2.5K tokens
- [Chief of Staff](briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md) - 2.5K tokens
- [CXO](briefing/BRIEFING-ESSENTIAL-CXO.md) - 2.5K tokens
- [CIO](briefing/BRIEFING-ESSENTIAL-CIO.md) - 2.5K tokens
- [PPM](briefing/BRIEFING-ESSENTIAL-PPM.md) - 2.5K tokens
- [HOST](briefing/BRIEFING-ESSENTIAL-HOST.md) - 2.5K tokens
- [Communications](briefing/BRIEFING-ESSENTIAL-COMMS.md) - 2.5K tokens
- [Documentation](briefing/BRIEFING-ESSENTIAL-DOCS.md) - 2.5K tokens
- [Coding Agent](briefing/BRIEFING-ESSENTIAL-AGENT.md) - 2K tokens

### Progressive Loading

Each essential briefing includes triggers for loading detailed documentation as needed.

---

## 🧭 Quick Navigation by Role

### 👨‍💼 Product Managers

- **[Current Planning](internal/planning/current/)** - Active planning cycles and roadmaps
- **[Issue Tracking](internal/planning/current/issues.csv)** - Current PM issue status
- **[Roadmap](internal/planning/roadmap/)** - Strategic planning and milestones
- **[Sprint Board Structure](internal/planning/sprint-board-structure.md)** - How milestones, sprints, and board Status are organized (xian's conventions) — **read before any board operations**
- **[Beta Blockers](internal/planning/beta-blockers.md)** - Canonical source of truth for what remains before beta release (22 issues, 7 epics, recommended sequencing) — living document, updated as issues are triaged in/out
- **[Sprint Order](internal/planning/sprint-order.md)** - Canonical sprint sequence across the full board
- **[Backlog Management](internal/planning/current/)** - Priority management and organization
- **Product Design & Strategy** (`internal/design/`):
  - [Piper Morgan by Analogy](internal/design/piper-morgan-by-analogy.md) — Positioning: same domain as Jira, different paradigm (Colleague vs Tool)
  - [Piper Morgan PR/FAQ](internal/design/piper-morgan-prfaq.md) — Working Backwards product narrative (press release + FAQ)
  - [Questions for Technical System Architect](internal/design/questions-for-technical-system-architect.md) — Architecture review discussion guide
- **[Suggestions](../suggestions/)** - Pre-issue ideas and change requests (promote to issues when triaged)

### 🏗️ Architects

- **[Architecture Hub](internal/architecture/current/)** - Current architectural decisions
- **[Domain Models](internal/architecture/current/models/)** - Hub-and-spoke model documentation
- **[ADRs](internal/architecture/current/adrs/)** - Architectural Decision Records (63)
- **[Patterns](internal/architecture/current/patterns/)** - Established architectural patterns (63)
- **[Pattern Families](internal/architecture/current/patterns/PATTERN-FAMILIES.md)** - 8 pattern families index
- **[Five-Layer Context Mapping](internal/architecture/current/five-layer-context-mapping.md)** - How PM injects context at each layer (agent team + product), with gap analysis
- **[Technical Evolution](internal/architecture/evolution/)** - Architecture development history
- **[Canonical Queries](internal/architecture/current/canonical-queries.md)** - Reference list of canonical query types (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)
  - Test matrix: To be created (validation coverage for all 25 canonical query patterns)
- **Product Design Records (PDRs)** (`internal/product/pdr/`):
  - [PDR-001: FTUX as First Recognition](internal/product/pdr/PDR-001-ftux-as-first-recognition-v3.md)
  - [PDR-002: Conversational Glue](internal/product/pdr/PDR-002-conversational-glue.md)
  - [PDR-002 Appendix: Layer 2 Vision](internal/product/pdr/PDR-002-appendix-layer-2-vision.md)
  - [PDR-003: Entity Concept Model](internal/product/pdr/PDR-003-entity-concept-model.md) — Product, Project, Repository relationships (APPROVED Mar 8, 2026)
  - [PDR-004: Experience Philosophy](internal/product/pdr/PDR-004-experience-philosophy.md) — Four principles governing Piper's experience design (Mar 22, 2026)
  - [PDR-101: Multi-Entity Conversation](internal/product/pdr/PDR-101-multi-entity-conversation.md)

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
- **[Methodology](internal/development/methodology-core/)** - Development methodologies (43 methodology docs, methodology-00 through -42)
- **[Methodology Index](internal/development/methodology-core/INDEX.md)** - Comprehensive methodology navigation
- **[Weekly Ship Process Guide](internal/development/weekly-ship-process-guide.md)** - Ship production process (v1.1)
- **[Colleague Test (operational v2.1)](internal/testing/colleague-test-rubric.md)** - Canonical scoring rubric (R/C/T 0-3, ≥7/9 pass, decline-path Tone=0 auto-fail)
- **[Colleague Test (conceptual)](internal/development/colleague-test.md)** - Philosophy, when-to-apply, worked PM examples
- **[Agent 360: Session-Start Overhead](internal/development/agent-360-finding-session-start-overhead-2026-03-21.md)** - HOST finding on briefing staleness (originally filed as HOSR before Mar 30 rename)
- **[Gameplan Template](internal/development/methodology-core/gameplan-template.md)** - Issue implementation gameplan template (v9.3)
- **[Sprint Gate Template](internal/development/sprint-gate-template-v1.md)** - Sprint completion gate checklist template (v1)
- **[Testing Procedures](internal/development/testing/)** - E2E bug protocol, testing guides, and procedures
- **[Session Templates](internal/development/tools/session-log-templates/)** - Session documentation

### 🚀 DevOps / Release Engineering

- **[CI/CD Smoke Test Runbook](internal/operations/ci-cd-smoke-test-runbook.md)** - Smoke test suite deployment and operations guide
- **[Deployment Operations](internal/operations/deployment/)** - Production deployment procedures
- **[Legacy Runbooks](internal/operations/legacy-operations/)** - Archived operational procedures

### 📚 Researchers & Historians

- **[Session Logs Archive](../dev/2025/)** - Chronological development history (dev/2025/MM/DD/ structure)
- **[Agent Activity Log](internal/operations/agent-activity-log.csv)** - Per-session index: date, role, slug, environment (code/web), model, log filename. Cross-project consumable (Janus sibling project)
- **[Omnibus Logs](omnibus-logs/)** - Daily session consolidations (288 logs through Mar 22, 2026)
- **[Retro Omnibus Evaluations](omnibus-logs/retro/)** - Dispatch automation pilot iterations and evaluations
- **[Cross-Pollination Briefs](briefs/cross-pollination/)** - Inter-project intelligence (Klatch ↔ Piper Morgan)
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
- **[Collaborator Profile Template](operations/alpha-onboarding/human-collaborator-profile-template.md)** - Template for creating new collaborator profiles
- **[Setup Screenshots](assets/images/alpha-onboarding/)** - GUI setup wizard screenshots (5 images for documentation)

---

## 📁 Documentation Architecture

### 🔓 Public Documentation (`public/`)

**External-facing content for users and developers**

- Getting started guides and tutorials
- API documentation and references
- User manuals and help content

#### Communications (`public/comms/`)

Blog posts and the content pipeline live here:

```
docs/public/comms/
└── drafts/               # All blog post drafts (pre-publish)
    ├── {slug}.md         # PM's working copy — canonical for publish
    ├── draft-{slug}.md   # Comms draft (may be superseded by PM's copy)
    ├── stashed-{slug}.md # Indefinitely deferred — not scheduled, not abandoned
    └── {slug}.png        # Post image (gitignored; must be force-added or moved manually)
```

**Draft lifecycle:**
1. **Active draft** — in progress; may have PM's voice-pass edits
2. **Ready to publish** — template audit passed, PM voice pass done; signal goes to Docs
3. **Published** — `publish-post.js` run, calendar updated; draft stays in `drafts/` for reference
4. **Stashed** (`stashed-{slug}.md`) — no current publish date; deferred but not deleted

**`stashed-` prefix convention** (PM-ratified 2026-07-14): rename a draft to `stashed-{slug}.md` when it has no scheduled publish date and no active work. This signals "deferred, not abandoned" to any agent. When PM is ready to resume, rename back to `{slug}.md` and add to the editorial calendar. Do not delete stashed drafts without PM direction.

**Publishing tools:**
- `scripts/publish-post.js` (always dry-run first)
- `docs/internal/planning/comms/editorial-calendar.csv` — source of truth for schedule and status
- `docs/internal/planning/comms/content-publishing-run-of-show.md` — full multi-agent publish sequence

**Downloadable resources / skills** (embedded in blog posts as `/resources/{filename}` links):
- Live in the WEBSITE repo at `piper-morgan-website/public/resources/` (served at `pipermorgan.ai/resources/`)
- Use a root-relative link in the draft: `[Label](/resources/{filename})`
- Copy the file to the website repo before running publish-post.js; commit alongside the post

### 🔒 Internal Documentation (`internal/`)

**Working documents for active development**

#### Development (`internal/development/`)

```
├── active/                    # Current work by status
│   ├── in-progress/          # Active development
│   ├── pending-review/       # Files needing review
│   └── ready-for-integration/ # Completed work
├── methodology-core/         # 43 development methodologies (see INDEX.md)
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
├── conversational-glue/      # M0 sprint planning docs (NEW Feb 2026)
│   ├── gap-analysis.md       # Gap analysis
│   ├── design-spec.md        # Design specification
│   └── implementation-guide.md # Implementation guide
├── comms/                    # Communications planning
│   ├── editorial-calendar.csv # Publication tracker
│   ├── xian-voice-tone-guide.md # PM's voice/tone guide — REQUIRED READING before drafting
│   ├── blog-post-template.md # YAML frontmatter + structure for new posts
│   ├── blog-first-publish-checklist.md # Pre-publish checklist (legacy PM-centric; superseded below)
│   ├── content-publishing-run-of-show.md # Multi-agent 7-step publish sequence (Comms→PM→Docs→Dispatch)
│   └── publishing-workflow-target.md # Blog-first target state
├── audits/                   # Planning audits (NEW Feb 2026)
├── mobile-skunkworks/        # Mobile PoC planning
├── roadmap/                  # Long-term strategic planning
└── historical/               # Previous planning cycles
```

### 📚 Knowledge Base (`knowledge/`)

**Files that exist in claude.ai project knowledge but have no other home in the repository**

This folder contains files that are useful in the claude.ai web project knowledge base but don't belong elsewhere in the docs/ hierarchy. Examples:
- Templates (gameplan-template.md, agent-prompt-template.md)
- Glossaries and reference materials
- Claude.ai-specific instructions (CLAUDE.ai-project-instructions-v5.0.md)

**Note**: BRIEFING-* files now live canonically in `docs/briefing/` (not symlinked). The roadmap lives in `docs/internal/planning/roadmap/roadmap.md`.

```
knowledge/
├── gameplan-template.md             # Gameplan template
├── agent-prompt-template.md         # Agent prompt template
├── piper-morgan-glossary-v1.1.md    # Project glossary
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

- **Active ADRs**: `docs/internal/architecture/current/adrs/` (63 decisions)
- **Patterns**: `docs/internal/architecture/current/patterns/` (63 patterns)
- **PDRs**: `docs/internal/product/pdr/` (6 product design records)

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
- **ADRs**: `internal/architecture/current/adrs/` (61 decisions)

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
- **[ADRs](internal/architecture/current/adrs/)** - Architectural decision records (63)
- **[Patterns Catalog](internal/architecture/current/patterns/)** - Implementation patterns (63)
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
