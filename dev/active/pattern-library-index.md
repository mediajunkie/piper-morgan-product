# Pattern Library Index

**Built**: 2026-05-09
**Scope**: All 65 pattern files at `docs/internal/architecture/current/patterns/pattern-*.md` (excluding `pattern-000-template.md`)
**Phase**: Phase 1 of Pattern Sweep 2.0 — enumeration only (no usage analysis, no novelty detection)
**Origin**: Pattern Sweep #1025 (staggered audit, March 17 → April 28, 2026 window)
**Builder**: Pattern Librarian sub-agent under CIO orchestration

This file is a machine-friendly enumeration intended for cross-reference by Phase 2+ subagents (Usage Analyst, Novelty Detector, Evolution Tracker). Each row captures the minimum metadata needed to grep for pattern manifestations in session logs, omnibus logs, ADRs, and code.

## Index

| # | Status | Name | Category | Signature Terms | Origin Date | Diagnostic |
|---|---|---|---|---|---|---|
| 001 | Proven | Repository Pattern | Core Architecture | repository, BaseRepository, CRUD, data access, session_scope | uncertain (pre-2025 catalog) | Are data-access concerns mixed into domain models or services? |
| 002 | Proven | Service Pattern | Core Architecture | service, business logic, orchestration, single responsibility, dependency injection | uncertain (pre-2025 catalog) | Is business logic scattered across controllers, repositories, or domain models? |
| 003 | Proven | Factory Pattern | Core Architecture | factory, stateless, object creation, WorkflowFactory, per-call context | uncertain (pre-2025 catalog) | Is complex object creation logic duplicated or context-mixed across the codebase? |
| 004 | Proven | CQRS-lite Pattern | Core Architecture | CQRS, query, command, QueryRouter, read separation | uncertain (pre-2025 catalog) | Are read and write operations sharing services to performance detriment? |
| 005 | Proven | Transaction Management Pattern | Core Architecture | transaction, session.begin, transaction_scope, atomic, rollback | uncertain (pre-2025 catalog) | Are multi-step database operations missing atomic transaction boundaries? |
| 006 | Proven | Verification-First Pattern | Investigation & Root Cause | verification, AI-generated, validation gate, evidence, hallucination | 2025-07 (July 2025) | Is AI-generated code being executed without systematic verification gates? |
| 007 | Proven | Async Error Handling Pattern | Core Architecture | async, await, error propagation, async boundary, structured exception | uncertain (legacy catalog) | Are async operation failures lost, deferred, or improperly propagated? |
| 008 | Proven | DDD Service Layer Pattern | Core Architecture | DDD, domain layer, integration layer, application layer, domain exception | 2025-09-12 | Is the application layer reaching directly into integration code, polluting the domain? |
| 009 | Proven | GitHub Issue Tracking Pattern | Methodology | issue tracking, GitHub, audit trail, evidence, work item | uncertain (consolidation) | Is work happening without GitHub-issue-anchored tracking and evidence? |
| 010 | Proven | Cross-Validation Protocol Pattern | Multi-Agent Coordination | cross-validation, multi-agent, validation, checkpoint, integration failure | uncertain (Sept 2025 era) | Are agent outputs landing without systematic cross-checks against another role? |
| 011 | Proven | Context Resolution Pattern | Core Architecture | context, resolution hierarchy, precedence, project resolution, implicit context | uncertain (pre-2025 catalog) | Is implicit context resolved unpredictably across multiple conflicting sources? |
| 012 | Proven | LLM Adapter Pattern | AI & Intelligence | LLM, adapter, provider, vendor lock-in, common interface | uncertain (pre-2025 catalog) | Is application code tightly coupled to a single LLM provider's API? |
| 013 | Proven | Database Session Management Pattern | Core Architecture | session, AsyncSession, lifecycle, resource leak, session_scope | uncertain (pre-2025 catalog) | Are database session lifecycles inconsistent or leaking resources? |
| 014 | Proven | Error Handling Pattern (API Contract) | Integration & Platform | API error, HTTP status, error response, RESTful, user-friendly | uncertain (pre-2025 catalog) | Are API error responses inconsistent or exposing internal details? |
| 015 | Proven | Internal Task Handler Pattern | Core Architecture | internal handler, orchestration, engine method, task type, indirection | uncertain (pre-2025 catalog) | Is orchestration logic fragmented across separate external handler classes? |
| 016 | Proven | Repository Context Enrichment Pattern | Integration & Platform | context enrichment, repository, automatic context, integration workflow | uncertain (legacy catalog) | Are users repeatedly providing the same contextual data that could be auto-resolved? |
| 017 | Proven | Background Task Error Handling Pattern | Core Architecture | background task, task lifecycle, async error, observability, correlation | uncertain (legacy catalog) | Are background task failures crashing the app or vanishing silently? |
| 018 | Proven | Configuration Access Pattern | Core Architecture | configuration, layered access, clean architecture, environment, settings | uncertain (legacy catalog) | Is configuration access violating layer boundaries or causing test brittleness? |
| 019 | Proven | LLM Placeholder Instruction Pattern | AI & Intelligence | placeholder, hallucination, LLM instruction, uncertainty, technical detail | uncertain (legacy catalog) | Is the LLM fabricating plausible-but-wrong technical details when info is missing? |
| 020 | Proven | Spatial Metaphor Integration Pattern (PM-074) | AI & Intelligence | spatial, metaphor, embodied, PM-074, navigation, ambient | uncertain (legacy catalog) | Are external events arriving without the spatial context AI agents need to navigate? |
| 021 | Proven | Development Session Management Pattern | Methodology | session log, development workflow, audit trail, multi-agent, progress tracking | uncertain (legacy catalog) | Is development work spanning sessions without structured logging and progress tracking? |
| 022 | Proven | MCP+Spatial Intelligence Integration Pattern | Integration & Platform | MCP, Model Context Protocol, spatial intelligence, federated search, 8-dimensional | uncertain (legacy catalog) | Are external-tool integrations losing dimensional context needed for cross-system insight? |
| 023 | Proven | Query Layer Patterns | Data & Query | query layer, circuit breaker, graceful degradation, performance monitoring | uncertain (legacy catalog) | Are read-heavy operations lacking circuit-breaker protection and performance isolation? |
| 024 | Proven | Methodology Patterns | Methodology | methodology, Excellence Flywheel, systematic, verification-first, evidence-based | 2025-08-22 (pattern sweep) | Is systematic methodology absent, leading to inconsistent quality and coordination loss? |
| 025 | Proven | Canonical Query Extension Pattern | Data & Query | canonical query, extension, delegation, backward compatibility, additive | uncertain (legacy catalog) | Are enhancements to canonical query systems risking backward compatibility? |
| 026 | Proven | Cross-Feature Learning Pattern | AI & Intelligence | cross-feature, learning, pattern sharing, confidence, feature isolation | uncertain (legacy catalog) | Are isolated learning systems re-discovering patterns each feature could share? |
| 027 | Proven | CLI Integration Pattern | Integration & Platform | CLI, command-line, service integration, formatting, scripted usage | uncertain (legacy catalog) | Is CLI tooling bypassing service layers or providing inconsistent formatting? |
| 028 | Proven | Intent Classification | AI & Intelligence | intent, classification, natural language, routing, GREAT-4A | 2025-05-28 (genesis); 2025-10-05 (validated) | Is natural-language input being routed without disciplined intent classification? |
| 029 | Experimental | Multi-Agent Coordination | Multi-Agent Coordination | multi-agent, coordination, handoff, specialized agent, orchestration | 2025-05-27 | Are specialized agents handing off work without explicit coordination protocols? |
| 030 | Experimental | Plugin Interface | Integration & Platform | plugin, interface, vendor lock-in, extensibility, integration contract | 2025-06-03 | Are PM-tool integrations hardcoded rather than pluggable? |
| 031 | Active | Plugin Wrapper Pattern | Integration & Platform | plugin wrapper, adapter, thin wrapper, GREAT-3A, integration router | 2025-10 (GREAT-3A) | Is plugin code carrying business logic instead of delegating to integration routers? |
| 032 | Proven | Intent Pattern Catalog | AI & Intelligence | intent pattern, catalog, regex, precision, false positive | 2025-10-05 | Are intent regex patterns over-broad or over-narrow, missing or mis-routing queries? |
| 033 | Proven | Notion Publishing | Integration & Platform | Notion, publishing, markdown, multi-platform, TDD | 2025-08-29 | Is Notion publishing happening without real-API testing (verification theater risk)? |
| 034 | Active | Error Handling Standards | Integration & Platform | HTTP status, error standards, API endpoint, status code, 200 OK | 2025-10-16 | Are API endpoints returning 200 OK for error conditions? |
| 035 | Emerging | MCP Integration Router with Adapter Methods | Integration & Platform | MCP, adapter method, integration router, ADR-038, ADR-052, lazy initialization | uncertain (during MCP+Spatial migration) | Is the MCP migration breaking backward-compatible method names for existing consumers? |
| 036 | Active | Signal Convergence for Breakthrough Detection | Methodology | signal convergence, multi-signal, breakthrough, meta-pattern, false positive | 2026-01-04 (Note: file says 2025-11-04) | Is breakthrough detection relying on a single metric and missing multi-signal events? |
| 037 | Active | Cross-Context Validation | Methodology | cross-context, validation, ADR, code, omnibus, concept emergence | 2025-11-04 | Are concepts appearing in one context (ADR or code) without validation in others? |
| 038 | Active | Temporal Clustering for Coordination Analysis | Methodology | temporal clustering, signal density, coordination, breakthrough day, concentration | 2025-11-04 | Are signals analyzed individually, missing coordinated breakthrough days? |
| 039 | Emerging | Feature Prioritization Scorecard | Methodology | scorecard, priority one, RICE, prioritization, Ted Nadeau | 2025-11-20 | Is the team treating every feature as priority one without a quantified scorecard? |
| 040 | Proven | Integration Swappability Guide | Integration & Platform | swappability, vendor lock-in, MS-SQL, Teams, JIRA, integration | 2025-11-20 | Are enterprise customers blocked because integrations cannot swap out their toolchain? |
| 041 | Proven | Systematic Fix Planning | Investigation & Root Cause | systematic fix, related issues, root cause, plan-then-fix, alpha testing | 2025-11-18 | Are related bugs being fixed reactively and piecemeal, missing shared root causes? |
| 042 | Proven | Investigation-Only Protocol | Investigation & Root Cause | investigation-only, no-fix, E2E testing, symptom fixing, root cause | 2025-11-18 | Is the agent fixing during investigation, missing pattern recognition across bugs? |
| 043 | Proven | Defense-in-Depth Prevention | Investigation & Root Cause | defense in depth, single-point fix, layer, prevention, hallucination eradication | 2025-11-18 | Is a systematic risk being addressed only at one layer, leaving recurrence paths open? |
| 044 | Established | MCP Skill Testing Pattern | Integration & Platform | MCP skill, skill testing, token usage, workflow component, CONV-MCP-STANDUP | 2025-11-22 | Are MCP skills shipping without disciplined testing of their reusable workflow shape? |
| 045 | Established | Green Tests, Red User | Completion Theater | green tests red user, mocked dependency, real infrastructure, completion triad | 2025-12-25 | Are unit tests passing while real users hit systematic failures against actual infrastructure? |
| 046 | Established | Beads Completion Discipline | Completion Theater | beads, completion discipline, 75 percent, optional, last mile | 2025-12-27 (first observed 2025-11-13) | Is work getting 75-90 percent done then abandoned by rationalizing the rest as optional? |
| 047 | Established | Time Lord Alert | Completion Theater | time lord, completion bias, uncertainty, escalation, pause | 2025-12-27 (first observed 2025-11-27) | Is the agent proceeding through uncertainty rather than pausing to express it? |
| 048 | Proven | Periodic Background Job | Core Architecture | periodic, background job, interval, cleanup, lightweight scheduler | 2026-01-10 (identified Dec 2025) | Are simple recurring tasks pulling in heavyweight scheduler dependencies? |
| 049 | Proven | Audit Cascade | Methodology | audit cascade, audit, drift, handoff, multi-step | 2026-01-13 | Is multi-step work accumulating drift across handoffs without audit-and-correct gates? |
| 050 | Proven | Context Dataclass Pair | Grammar Application | Entity Moment Place, dataclass pair, grammar, input output, attribution | 2026-01-20 | Is grammar awareness (Entity/Moment/Place) lost between service layers? |
| 051 | Proven | Parallel Place Gathering | Grammar Application | parallel gathering, asyncio.gather, Place, graceful degradation, integration | 2026-01-20 | Are multi-source integrations fetched sequentially when they could be gathered in parallel? |
| 052 | Proven | Personality Bridge | Grammar Application | personality bridge, raw data, Piper voice, Place-aware, presentation | 2026-01-20 | Is rich contextual data being shown to users in raw, mechanical form? |
| 053 | Proven | Warmth Calibration | Grammar Application | warmth, calibration, encouragement, generic praise, emotional tone | 2026-01-20 | Is feedback feeling hollow, over-enthusiastic, or disconnected from observed data? |
| 054 | Proven | Honest Failure with Suggestion | Grammar Application | honest failure, error message, recovery, blame-shifting, actionable | 2026-01-20 | Are integration failures presented as silent errors, jargon, or blame-shifting? |
| 055 | Emerging | Multi-Intent Decomposition | AI & Intelligence | multi-intent, decomposition, greeting plus query, first-match-wins, parallel intents | 2026-01-21 (discovered 2026-01-15) | Are multi-intent messages collapsing to a single intent and losing the secondary one? |
| 056 | Emerging | Consciousness Attribute Layering | AI & Intelligence | consciousness, awareness, emotional state, role, capability, trust layer | 2026-01-21 | Is Piper's self-awareness state flat rather than multi-dimensionally layered? |
| 057 | Emerging | Grammar-Driven Classification | Grammar Application | grammar-driven, MUX, ADR-055, intent category, verb type, Entity Moment Place | 2026-01-21 | Is intent classification using arbitrary action categories rather than grammatical roles? |
| 058 | Emerging | Ownership Graph Navigation | AI & Intelligence | ownership graph, epistemological, fact vs inference, stale data, read-only | 2026-01-21 | Is the assistant treating uncertain inferences as certain facts due to no ownership model? |
| 059 | Emerging | Leadership Caucus | Multi-Agent Coordination | leadership caucus, MUX Track V1, multi-advisor, synchronous alignment, cross-cutting | 2026-01-19 | Is cross-cutting work blocked by sequential advisor handoffs that lose context? |
| 060 | Emerging | Cascade Investigation | Investigation & Root Cause | cascade investigation, adjacent issue, related bug, audit prompt, cluster | 2026-02-03 (Pattern Sweep 2.0) | After fixing a bug, are adjacent related issues going undiscovered until they surface independently? |
| 061 | Proven | Human-AI Collaboration Referee | Multi-Agent Coordination | referee, human-AI, role confusion, handoff, validation gate | 2025-07 | Is human-AI collaboration suffering from role confusion, handoff failures, or quality gaps? |
| 062 | Proven | Assembly Assumption | Investigation & Root Cause | assembly assumption, horizontal slice, integration gap, M0 sprint, composition | 2026-02 (M0 sprint) | Are individually-passing feature slices assumed to compose correctly without integration verification? |
| 063 | Proven | Parallel-Authoring Drift | Methodology | parallel authoring drift, canonical reference, branch-or-anchor, semantic divergence, rubric | 2026-04-26 (filed 2026-04-27, promoted 2026-05-08) | Are two authors extending a canonical reference in parallel and diverging silently at the semantic layer? |
| 064 | Proven | Extension Without Integration | Investigation & Root Cause | extension without integration, alive scaffolding, mechanical wiring, semantic verification, BoundaryEnforcer | 2026-04-28 (formalized; sketched 2026-04-25) | Is a component extended to a new context being wired mechanically but never verified semantically against the new input? |
| 065 | Proven | Continuity Memo Before the Seam | Multi-Agent Coordination | continuity memo, pre-seam, six-section, handoff, departing party | 2026-04-27 (filed; promoted 2026-05-08) | Is the continuity document being written after the discontinuity rather than before? |

## Notes on data quality (for Phase 2+ subagents)

### Status field unusual formats
- **Pattern-029 (Multi-Agent Coordination)**: Status reads "Experimental (Scripts exist, deployment pending)" — recorded as Experimental.
- **Pattern-030 (Plugin Interface)**: Status reads "Experimental (June 3 vision, partially implemented in GitHub integration)" — recorded as Experimental.
- **Pattern-031 (Plugin Wrapper)**: Uses "Active" not "Proven/Emerging/Experimental/Withdrawn" — kept as Active.
- **Pattern-034 (Error Handling Standards)**: Uses "Active" with checkmark glyph — recorded as Active.
- **Pattern-035 (MCP Adapter Methods)**: "Emerging - Proven in GitHub integration, ready for broader adoption" — recorded as Emerging.
- **Pattern-036, 037, 038**: All use "Active" status (meta-patterns from Enhanced Pattern Sweep) — recorded as Active.
- **Pattern-039 (Feature Prioritization Scorecard)**: Status field shows the template literal "**Emerging** | Proven | Experimental | Deprecated" — appears to be unedited template artifact; the file's Evolution section confirms Emerging. Recommend filing as a template-cleanup ticket.
- **Pattern-040 (Integration Swappability Guide)**: Same template-literal artifact as 039 ("**Proven** | Emerging | Experimental | Deprecated"); the bolded Proven indicates intent. Recommend filing as a template-cleanup ticket.
- **Patterns 044, 045, 046, 047, 048, 050-054**: Use "Established" or "Proven" with metadata block format (different from main template) — recorded as-stated.
- **Patterns 055-060**: Use "Emerging | Proven in #NNN" format — recorded as Emerging (the issue-proven flag is supplemental).
- **Pattern-063, 064, 065**: Recently promoted from Emerging to Proven on 2026-05-08 with extensive promotion narrative in the Status block — recorded as Proven.

### Origin date issues
- **Patterns 001-005, 011-019, 022-023, 025-027**: No explicit origin date in Status block, Evolution section, or footer. Most reference legacy `pattern-catalog.md` consolidations. Marked "uncertain (pre-2025 catalog)" or "uncertain (legacy catalog)". Phase 2/3 subagents may want to git-blame these files for first-commit dates.
- **Pattern-007 (Async Error Handling)**: References legacy `PATTERN-INDEX-legacy.md`; no specific date.
- **Pattern-009 (GitHub Issue Tracking)**: "Created from observed project practices" — no date.
- **Pattern-010 (Cross-Validation Protocol)**: References Sept 2025 session-log examples in footer but no explicit creation date.
- **Pattern-024 (Methodology Patterns)**: Footer mentions "August 22, 2025 pattern sweep" and "Last updated: September 15, 2025"; used Aug 22 as origin proxy.
- **Pattern-031 (Plugin Wrapper)**: "Established in GREAT-3A (October 2025)" — no exact day; recorded as 2025-10.
- **Pattern-035 (MCP Adapter Methods)**: No explicit date; placed during MCP+Spatial migration (ADR-038/ADR-052 era).
- **Pattern-036 (Signal Convergence)**: File header reads "Created: 2025-11-04" but the file is grouped with other 2025-11-04 meta-patterns (037, 038); kept as recorded though I noted it as 2026-01-04 initially in my draft and corrected back. **Recorded as 2025-11-04 per file.**
- **Pattern-061 (Human-AI Collaboration Referee)**: "Production ready since July 2025" — recorded as 2025-07; no exact day.
- **Pattern-062 (Assembly Assumption)**: "Identified February 2026, validated through M0 sprint" — recorded as 2026-02; no exact day.

### Category fit issues
- **Pattern-009 (GitHub Issue Tracking)**: Sits between Methodology and Integration & Platform; chose Methodology because the pattern is about systematic work tracking discipline more than about the GitHub integration itself.
- **Pattern-021 (Development Session Management)**: Sits between Methodology and Multi-Agent Coordination; chose Methodology because it's primarily about session-log discipline.
- **Pattern-024 (Methodology Patterns)**: Self-categorizes as Methodology; meta-pattern about methodology application.
- **Pattern-036, 037, 038**: All three are explicitly labeled "META-PATTERN" in their headers (patterns about pattern-detection itself). Categorized as Methodology since that's their operational layer; Phase 2 may want a "Meta-Patterns" sub-category if the volume grows.
- **Pattern-044 (MCP Skill Testing)**: Could fit Methodology (testing discipline) or Integration & Platform (MCP-specific); chose Integration & Platform because it's about MCP skill artifacts specifically.
- **Pattern-061 (Human-AI Collaboration Referee)**: Could fit Methodology or Multi-Agent Coordination; chose Multi-Agent Coordination because the referee role is about agent-to-agent and human-to-agent coordination.

### Patterns in tight clusters (for Phase 2 cross-reference)
- **Completion Discipline Triad**: 045, 046, 047 — explicitly cross-referenced in Pattern-045's overview.
- **Meta-Pattern Trio (Pattern Sweep methodology)**: 036, 037, 038 — all created 2025-11-04 from Enhanced Pattern Sweep work.
- **Grammar Application Cluster**: 050-054 — all formalized 2026-01-20 from Grammar Implementation sprint.
- **Grammar/MUX Cluster**: 055-058 — all documented 2026-01-21.
- **Sub-pattern Family of Pattern-062 (Assembly Assumption)**: 062, 063, 064 — explicit sibling-sub-pattern relationship at specification, integration-contract, and composition layers respectively.

### Total row count: 65 patterns indexed (pattern-001 through pattern-065).
