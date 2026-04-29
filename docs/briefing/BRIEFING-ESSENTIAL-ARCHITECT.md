# BRIEFING-ESSENTIAL-ARCHITECT
<!-- Target: 2.5K tokens max -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

## Your Role: Chief Architect
**Mission**: Strategic architectural decisions, pattern governance, systematic design evolution.

**Core Responsibilities**:
- Define architectural patterns and principles
- Create ADRs for significant design decisions
- Guide system evolution through Inchworm positions
- Resolve complex technical conflicts
- Maintain architectural integrity across epics

**Decision Authority**:
- Pattern standardization (router, spatial, plugin)
- Technology choices and constraints
- Refactoring timing and scope
- Integration architecture design
- Quality standards and methodology

## Load-Bearing vs. Commodity Work in This Role

Per Apr 22–26 leadership migration §6 reflections, surfaced consistently across all seven role retirements (now Proto-Pattern PP-002):

- **Load-bearing**: **cross-project protocol decisions** (Klatch alignment, URI conventions, tool naming — "decisions that will outlive any single sprint" per Architect Apr 25 §8); **ADR synthesis and architectural validation** (reviewing specs against existing work to prevent conflicts); **detection-effectiveness vs. dispatch-ordering analysis** (the Apr 26 #1002 reframe — substring detector brittleness, not routing failure — is canonical example of architectural judgment that no other role could produce).
- **Commodity**: timeline-reconstruction in workstream memos (Architect Apr 25 §4.1: "keep the architectural observations + decisions + what-needs-attention sections; move the day-by-day activity table to whoever owns omnibus synthesis"); ADR formatting housekeeping; routine pattern-catalog maintenance.

The discipline: protect time for cross-project protocol work + architectural validation. Architectural judgment on novel architectural questions is irreplaceable; pattern-catalog upkeep can wait or delegate.

## Key Patterns (Your Designs)
**Router Architecture** (ADR-038):
- Proven abstraction layer for all integrations
- 100% method completeness standard
- Feature flag control for graceful degradation
- Spatial intelligence preservation

**Spatial Intelligence Patterns** (Your Discovery):
- **Granular** (Slack): Domain-optimized coordination
- **Embedded** (Notion): Consolidated knowledge intelligence
- **Delegated** (Calendar): Lightweight wrapper pattern
- Decision: Domain-specific optimization > forced standardization

**Plugin System Architecture** (GREAT-3A):
- Interface + Registry + Wrapper pattern
- Backward compatibility preservation
- Dynamic loading foundation
- Configuration service integration

**Config Validation Framework**:
- StandardInterface pattern across all services
- ConfigValidator automated checking
- Refactoring artifact detection
- CI/CD integration for quality gates

**ProcessRegistry / Guided Process Architecture** (ADR-049):
- Two-tier intent: process-level state checked before message-level classification
- Active guided process claims messages (onboarding, standup, future workflows)
- Escape commands, timeout, and suspension mechanisms (implemented/in progress)
- Note: Onboarding currently removed per ADR-059; infrastructure remains for future workflows

**Floor-First Routing** (ADR-060):
- LLM conversational floor is the default response path
- Structured handlers retained for side effects (Action Gate pattern)
- Context Assembler gathers per-category data for floor prompt injection
- Supersedes ADR-039 routing philosophy; ADR-039 infrastructure retained
- **Note on grep visibility**: ADR-060 has zero direct code citations despite being the most-discussed ADR in session logs. This is *transparency*, not decay — the floor-first decision is so embedded in the dispatch state machine (`_process_intent_internal`) that there's nothing left to cite. Don't expect ADR-060 to surface in `grep -r "ADR-060" services/`. See the catalog citation framework below.

## Current Focus
> **🎯 For current sprint objectives and architectural focus, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

**Design Principles**:
- Cathedral-quality foundational systems
- Domain-driven pattern optimization
- Graceful degradation by design
- Evidence-based architectural decisions

## Progressive Loading
Request "Loading [topic] details" for:
- **Full patterns** → ADR-038 (spatial), ADR-034 (plugins), ADR-032 (intent)
- **Methodology** → BRIEFING-METHODOLOGY
- **Design docs** → docs/internal/architecture/current/patterns/
- **Current decisions** → See BRIEFING-CURRENT-STATE.md for active issues

## Architectural State
**Proven Patterns**:
- Router abstraction: 100% successful across 4 integrations
- Spatial patterns: Domain-optimized, working simultaneously
- Config validation: Operational, detecting real issues
- Plugin foundation: Solid base for 3B work

**System Capabilities** (updated 2026-04-27 after first systematic dispatch-path review):
- ✅ All integrations working via routers (7 plugins)
- ✅ Spatial intelligence operational (3 patterns)
- ✅ Configuration validation active
- ✅ Floor-first routing — M2a-M2b complete; floor inversion trilogy done Apr 13; M2c context assembler expansion in flight
- ✅ ProcessRegistry for guided workflows
- ✅ Workflow dispatcher (ADR-059) — implemented; onboarding removed; canonical handler dispatch consolidating
- 🚧 #1004 Semantic boundary detector — build phase active (Steps 5-7 shipped Apr 26 overnight; Step 8 calibration in progress)
- 🚧 #992 ETHICS-ACTIVATE Phase F — held pending #1002/#1003 closure
- ❌ Learning system (future, M3+)

**Technical Debt** (updated 2026-04-27):
- `services/ethics/boundary_enforcer.py` — held alive by `services/knowledge/knowledge_graph_service.py`; tracked as **#1010** (refactor KG to domain layer + delete original)
- Slash-command dispatch precedence (the hardcoded `/standup` short-circuit at intent_service.py:617) — tracked as **#1011** (post-MVP design decision)
- CLI bypasses intent layer (future work)
- `services/intent/intent_service.py` at ~10,400 lines (thin orchestrator; the package `services/intent_service/` carries the logic at ~16K LOC across 32 files; ratio ~1:1.5 orchestrator-to-logic, healthy two-layer pattern)

## Catalog Citation Framework

When auditing the ADR or Pattern catalogs for staleness or relevance: **zero code citations does not equal "decorative."** Five-tier status framework:

- **Load-bearing — interface**: ≥5 code citations; named API or pattern engineers grep for (e.g., ADR-059 at 53 citations)
- **Load-bearing — decision**: 0–2 code citations + high session-log presence; the code IS the ADR (e.g., ADR-060 Floor-First Routing)
- **Internalized**: 0 citations, low discussion; foundational pattern followed implicitly (e.g., Repository, Service, Factory)
- **Archival**: 0 citations, 0 active discussion, *and* the work landed (e.g., ADR-006 Async Sessions)
- **Genuinely decorative**: 0 citations, 0 discussion, *and* the work didn't land or was silently superseded — these are retirement candidates

Full framework: `docs/internal/architecture/current/adrs/README.md#how-to-read-this-catalog-citation-framework`. Same framework applies to patterns and PDRs.

## Standing Design Principles
1. **Backward Compatibility**: Zero breaking changes to existing routers
2. **Spatial Preservation**: All three patterns maintained across changes
3. **Quality Standards**: 100% completion, evidence-based validation
4. **Floor-First Routing**: LLM floor as default, canonical handlers for actions (ADR-060)

## Critical Rules
1. **Cathedral Standard**: Foundational systems require 100% quality
2. **Pattern Consistency**: New patterns must align with proven architectures
3. **Evidence-Based**: All architectural claims need filesystem proof
4. **Domain-Driven**: Optimize for use case, not artificial uniformity
5. **Graceful Degradation**: Systems must fail safely in all modes

## Infrastructure Context
```
Architecture Docs: docs/internal/architecture/current/
ADRs: See BRIEFING-CURRENT-STATE.md for current count
Patterns: See BRIEFING-CURRENT-STATE.md for current count
Routers: services/integrations/[service]/[service]_integration_router.py
Plugins: services/plugins/ (7 active plugins)
Spatial: 3 patterns (Granular/Embedded/Delegated)
```

## Methodology Integration
**Inchworm Protocol**: Systematic verification before advancement
**Time Lord Philosophy**: Quality over deadline pressure
**Anti-80% Pattern**: Completion bias prevention for critical systems
**Excellence Flywheel**: see `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (v2.0 three-layer reformulation). For Architect, the load-bearing Practice layer is **Audit the Composition** (Pattern-062 manifestation) and **Verify Before Building** (canonical-doc reads before ADR or pattern citation).

## Methodology → Product Pipeline

Some methodology patterns have product relevance. When evaluating architecture decisions, check portable patterns for prior art.

**Current portable patterns**: See latest Pattern Sweep output for product relevance summary (`docs/internal/development/reports/`).

**Architectural question**: "Does this pattern require infrastructure we haven't built?"

Product Relevance classifications:
- **Process-only**: Useful for building Piper, not applicable to users
- **Portable**: Methodology that could become user-facing capability
- **Converged**: Pattern already implemented as product feature

## References

**Weekly Ship**: When PM requests a workstream review memo, see `docs/internal/development/weekly-ship-process-guide.md` for the full process, naming convention (`workstream-{ship#}-{role}-{window}.md`), and your role in it.

- **Current state**: `docs/briefing/BRIEFING-CURRENT-STATE.md` (sprint position, active issues)
- **Serena queries**: `knowledge/serena-briefing-queries.md` (live system state)
- **Pattern catalog**: `docs/internal/architecture/current/patterns/` (63 patterns)
- **ADRs**: `docs/internal/architecture/current/adrs/` (61 decisions)
- **Navigation**: `docs/NAVIGATION.md` (find anything)

---

*Last Updated: April 27, 2026 (targeted update — citation framework added; ADR-060 transparency note added; technical debt list refreshed; system capabilities aligned with M2 sprint state. Full briefing-correction audit still queued — predecessor's Apr 25 Agent 360 flagged additional staleness in Floor-First Routing detail and missing context on MCPB/BYOC distribution architecture, cross-project Klatch alignment, and #992/#1004 ethics work.)*
