---
type: briefing
title: BRIEFING-ESSENTIAL-ARCHITECT
valid_from: "2025-10-19"
last_updated: "2026-09-01"
last_verified: "2026-09-01"
---

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

## Critical vs. Commodity Work in This Role

Per Apr 22–26 leadership migration §6 reflections, surfaced consistently across all seven role retirements (now Proto-Pattern PP-002):

- **Load-bearing**: **cross-project protocol decisions** (Klatch alignment, URI conventions, tool naming — "decisions that will outlive any single sprint" per Architect Apr 25 §8); **ADR synthesis and architectural validation** (reviewing specs against existing work to prevent conflicts); **detection-effectiveness vs. dispatch-ordering analysis** (the Apr 26 #1002 reframe — substring detector brittleness, not routing failure — is canonical example of architectural judgment that no other role could produce).
- **Commodity**: timeline-reconstruction in workstream memos (Architect Apr 25 §4.1: "keep the architectural observations + decisions + what-needs-attention sections; move the day-by-day activity table to whoever owns omnibus synthesis"); ADR formatting housekeeping; routine pattern-catalog maintenance.

The discipline: protect time for cross-project protocol work + architectural validation. Architectural judgment on novel architectural questions is irreplaceable; pattern-catalog upkeep can wait or delegate.

## ⭐ CURRENT LAW (verified 2026-09-01 — supersedes the pattern notes below where they conflict)

**The Architectural Review 2026 (PM+Arch co-led, 08-29→09-01) reset this role's operating surface.**
Read these FIRST; the sections below are historical context:

- **`docs/internal/architecture/ESSENCE.md`** (v1.0.2, PM-RATIFIED) — what Piper IS: seven
  commitments, the for-whom (xian first, definitionally), the NOT-boundary. Current law.
- **`docs/internal/architecture/SYSTEM.md`** — what's actually running (census-derived).
- **`docs/internal/architecture/CONNECTORS.md`** — per-connector transport/grant truth + the
  C4 grant rule + class-aware payload-honesty rules.
- **`reviews/2026-08-architectural-review/reorientation-plan.md`** — the four workstreams, owners,
  dates. **Ratified sequencing: web-chat = MAINTENANCE MODE; all new build → the MCP/BYOC path;
  MCP-path completion = PUBLIC-BETA GATE (milestone #9); legacy-classifier retirement check
  2026-09-30.**
- **`docs/internal/architecture/bets/`** — the scope-bet gate (ratified): crossing a scope
  tripwire needs a PM-ratified one-page Bet Memo first.
- ADR corpus: **demote-don't-retire** — ADRs are append-only history; the index is a DERIVED VIEW
  (`scripts/derive-adr-index.py`); current law lives in the six living core docs.

## Key Patterns (HISTORICAL NOTES — dated caveats added 2026-09-01)
**Router Architecture** (ADR-038):
- Proven abstraction layer for all integrations
- 100% method completeness standard
- Feature flag control for graceful degradation
- Spatial intelligence preservation

**Spatial Intelligence Patterns** *(⚠️ RESCOPED 2026-08-15/16, PM-ruled: the live layer stays
(place_service/Radar, place_detector, github_spatial, home_state); the 11 committed-theory modules
were disposed as superseded prior art. "3 patterns operational" below is the pre-rescope claim.)*:
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
- **Design docs** → docs/internal/architecture/patterns/
- **Current decisions** → See BRIEFING-CURRENT-STATE.md for active issues

## Architectural State
**Proven Patterns**:
- Router abstraction: 100% successful across 4 integrations
- Spatial patterns: Domain-optimized, working simultaneously
- Config validation: Operational, detecting real issues
- Plugin foundation: Solid base for 3B work

**System Capabilities**: *(2026-09-01 — the April list that stood here was two architectural
generations stale; deleted rather than patched.)* **Current truth: `SYSTEM.md`** (entry points,
understanding stack incl. Inversion flip state, module classification with disposal-in-flight
counts, census hazards). Headlines as of this verification: ~69% of 491 modules load-bearing at
census, ~10K LOC disposed since via three fix-or-delete batches; flip-1 live for `read_status` via
fly secrets; the staged full flip is sequenced into PM's next watched round.

**Technical Debt** *(2026-09-01: this list is HISTORICAL — the Leg-B census + Lead's disposal
pipeline (epic #1698) now govern dead/75% code, and the resolved strikethroughs below are kept as
record only. One line-item correction: `intent_service.py` is now ~14.4K lines, not ~10.4K.)*:
- ~~ADR-051 RequestContext migration Phase 2/3 partial adoption (#1015) — intent path adopted RequestContext; all other route/service surfaces still use `current_user.sub` / `user_id: str`; Apr 27 audit recommended completing the migration~~ — ✅ resolved 2026-05-16 as **#1015 Phase 2 Option C** (ratify-with-scope-clarification, Architect-ratified): ADR-051 AMENDED with intent-path-specific scope; RequestContext docstring updated to name the scope + Pattern-072 connection; `require_request_context` orphan dependency in `auth_middleware.py` deleted (Architect's Option 1; was 3rd 12w/Pattern-073 instance); 2 orphan tests in `tests/security/test_request_context_enforcement.py` deleted. RequestContext is now the canonical identity-and-context object for the intent path specifically; other surfaces use FastAPI dependency injection (`current_user: JWTClaims`). Adopting RequestContext beyond intent path is a Pattern-072 recognition-trigger decision (criterion: ≥3 service boundaries with state depending on identity-and-context, not just identity). Net ~+50 lines in docs, ~-80 lines in code/tests.
- ~~OrchestrationEngine + WorkflowFactory partially abandoned post-#883 lazy-workflow; engine.create_workflow_from_intent had zero active callers but the engine reference was held in 5 places (intent_service, container init, webhook_router, 2 slack handlers); WorkflowFactory + dispatcher had 8/14 WorkflowType coverage gap silently failing~~ — ✅ resolved 2026-05-15 PM as **#1094 ENGINE-DELETION** (γ-preserve ratified by Architect): deleted `services/orchestration/engine.py` + `services/orchestration/workflow_factory.py` + `services/integrations/slack/slack_workflow_factory.py` + ~12 engine-direct tests; refactored 5 live-code consumers + ~20 test files to drop the engine kwarg; Slack handlers + intent_service now dispatch EXECUTION intents via task_type registry (Pattern-072 third-consumer trigger fires here — promotion to Proven). Workflow domain model + WorkflowRepository preserved (γ-preserve). Branch `claude/1094-engine-deletion`.
- ~~`services/ethics/boundary_enforcer.py` — held alive by KG service; tracked as #1010~~ — ✅ resolved 2026-05-14 (KG migrated to its own KGBoundaryEnforcer; placeholder methods removed; #1089 KG-PRIVACY-FILTER filed as designed-feature replacement)
- ~~UserHistoryService Layer 3 has no DB backend (#1021)~~ — ✅ resolved 2026-05-14 (DBUserHistoryRepository over extended ConversationDB; migration `a1021userhist`; user-history API surface + adaptive-greetings wiring landed; 32 tests, 11 integration)
- ~~`services/ethics/adaptive_boundaries.py` — alive scaffolding (called from `boundary_enforcer_refactored`; learning loop inert); tracked as #1019~~ — ✅ resolved 2026-05-14 (Path C: deleted 367 LOC + cleaned `boundary_enforcer_refactored.py` + `staging_health.py` + `ethics_metrics.py`; net −543 LOC across 5 files; 111 ethics tests pass; #1004 semantic-detector substrate is structural successor; #1016 is where future learning-loop design will land)
- 🚧 **LLM outputs reach users unfiltered (#1017)** — Phase 2 implementation **merged to main 2026-05-15** (`ba00185a`, branch `claude/1017-output-content-filter`): OutputFilter at decorator chokepoint on `LLMClient.complete()`; profile dispatch via `task_type` registry (10 user_visible / 1 internal / 1 mixed); Tier 1 PII regex (reused SecurityRedactor + added secret-format patterns) + Tier 2 BoundaryEnforcer-on-outputs; CXO-ratified canned phrasing on category violations with regenerate-trigger coupling; hash-only audit envelope (Pattern-064-adjacent invariant) via `log_output_filter_decision()` writing to `ethics_audit_log`; 55 new tests, 0 regressions. **Phase 3 probe set + CI verification gate + ADR-061 amendment** remain (gated on Architect + CXO co-design per CXO Q7 ratification)
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

Full framework: `docs/internal/architecture/adrs/README.md#how-to-read-this-catalog-citation-framework`. Same framework applies to patterns and PDRs.

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
- **Pattern catalog**: `docs/internal/architecture/patterns/` (81 entries, B3-dispositioned 2026-09-01)
- **ADRs**: `docs/internal/architecture/adrs/` (78 files; index is DERIVED — trust Status lines)
- **Navigation**: `docs/NAVIGATION.md` (find anything)

---

*Last Updated / Verified: September 1, 2026 (owner-attested verification per #1712, replacing the
2026-06-19 bulk stamp). WHAT I RE-CHECKED: the current-law banner's every claim (against
ESSENCE/SYSTEM/CONNECTORS/reorientation-plan at HEAD — all authored or ratified within 72h);
spatial rescope status; capability list (replaced with SYSTEM.md pointer); intent_service line
count; ADR/pattern counts (against the derived index + B3 trackers). WHAT I DID NOT RE-CHECK:
the Key Patterns historical notes' fine detail (router/plugin/config-validation claims — dated
May-era, flagged historical rather than re-verified); the Catalog Citation Framework (still sound
in principle; its examples' citation counts not re-run); Methodology Integration section. Prior
footer preserved in git history.)*
