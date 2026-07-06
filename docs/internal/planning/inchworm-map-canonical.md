# Inchworm Map — Canonical Record

**Owner**: PM (xian)
**Captured**: 2026-07-05/06, pasted in during the sprint-history recovery effort
**Status**: DURABLE — this is PM's own contemporaneous planning record, kept personally (Apple Notes, then Bike outliner) in parallel to GitHub issue tracking. Per PA's June 28 session log, this map was already used once as "the most authoritative sprint-to-task source" to resolve the hardest ambiguous sprint assignments — this file exists so it never has to be re-pasted from memory again.

**How to read this**: multiple snapshots in chronological order, each showing the state of the plan as of that date (✅ done, ➡️ in progress/current, ❌ abandoned/failed, 🐛 current focus, 🔝 deferred, 🛑 stopped/blocked, ‼️ stop-everything). The most recent, most complete snapshot (last in this file) supersedes earlier ones for overall structure — PM kept it in a Bike outliner and pasted it in a code block, so its indentation survived intact and its hierarchy can be trusted precisely. Earlier snapshots lost indentation on paste but retain phase-level detail (sub-phase names, specific failure points) that got compressed into single checkmarks by the time of the final rollup.

**Important caveat for anyone using this to assign GitHub Sprint field values**: this map's own naming (especially "M0" through "M7" in the "MVP - march to beta" section near the end) reflects PM's *original* planning conception, not necessarily the *current* GitHub Sprint field option names. Cross-reference against the actual sprint-restructuring history before applying labels literally — e.g. this map's "M6 - MVP Future" has been confirmed retired (PA, 2026-06-28); this map's "M4 - MVP Document Revolution" content (DOCS-STOPGAP, etc.) was folded into what's now the live "M3 - Artifact Persistence" option. For the Alpha-era portion (A1 through A31, T1/T2, S1/S2, Q1, B1, the MUX cluster V1/X1/V2/Interact/Implement) the map's names generally do match the live GitHub Sprint field options directly.

---

## Snapshot: Oct 9, version 2.2.3 (indentation lost on paste)

```
Daily Execution Checklist
Before starting work:
1. What step am I on?
2. Is previous step 100% complete?
3. Will this help GitHub issue creation work?
4. Am I finishing or starting?
If starting when not finished: STOP

Success Validation
Each refactor validated by:
- GitHub issue creation works end-to-end
- No regressions in working features
- Tests prevent future breaks
- Documentation update

Alpha
1. The Great Refactor
2. Complete the build of CORE
   1. Prep for A1 (Docs: roadmap review, omnibus log 10/8, TODO list; Token efficiency: Serena MCP, handoff briefing)
   2. A1: Critical Infrastructure
      - INFR-DATA #113 (1d) Database migration
      - CORE-TEST-CACHE #216 (30m) Quick warm-up
      - INFR-DATA #145 (1d) Fix Slack asyncio bug
      - CORE-LLM-CONFIG #217 (1-2d) API keys -- first attempt (investigation, env vars, Cursor cross-validate FAILED)
        then ARCH ISSUE DISCOVERED -- new gameplan: Phase 0 Investigation, Phase 1 LLM Domain Service Creation,
        Phase 2 Consumer Migration to ServiceRegistry, Phase 3 Testing/Deprecation, Phase 1 Core infra,
        Phase 1.5 keychain (sub-phases A/B/C -- Migration CLI 1hr->4min), Phase 2 Multi-provider (selection config,
        tests, ProviderSelector service, tests, env config, client code, startup validation, Cursor cross-validate),
        Phase 3 Key setup/tooling, Phase 4 Documentation, Phase Z verification evidence + commit (#215, #145 too)
        + push w/ PM approval, Chief Architect check-in
      - CORE-INTENT-ENHANCE #212 (4-6h) Better classification
   3. CORE-CRAFT: CRAFT-GAP (GAP-1)
   4. A2: Notion & Errors -- CORE-NOTN #142 (5h) API connectivity, CORE-NOTN #136 (1d) remove hardcoding,
      CORE-NOTN #165 (1d) DB API upgrade, CORE-INT #109 (5h) legacy deprecation verification,
      MVP-ERROR-STANDARDS (1-2d) standardize errors
   5. A3: Core Activation -- CORE-MCP-MIGRATION #198 (2d) MCP, CORE-ETHICS-ACTIVATE #197 (1d) ethics middleware,
      CORE-KNOW #99 (1d) connect knowledge graph, CORE-KNOW-BOUNDARY #226
   6. A4: Standup Epic -- OPS-STAND #159 (1d) sprint model foundation, OPS-STAND #162 (1d) multi-modal generation,
      OPS-STAND #160 (2d) interactive assistant transformation, OPS-STAND #161 (1d) Slack reminder integration
   7. A5: Learning System -- CORE-LEARN-A (2-3d) infra foundation, CORE-LEARN-B (2-3d) pattern recognition,
      CORE-LEARN-C (2-3d) preference learning, CORE-LEARN-D (3-4d) workflow optimization
   8. Sprint 6: Learning Polish & Onboarding -- CORE-LEARN-E (3-4d) intelligent automation, CORE-LEARN-F (2d)
      integration & polish, CORE-ALPHA-USERS (2-3d) onboarding infra, CORE-USERS-PROD, CORE-USERS-API,
      CORE-USERS-JWT
   9. Sprint 7: Testing & Buffer -- e2e workflow testing, doc updates, alpha deployment prep, discovery buffer
3. Start Piper education
   1. Configuration check (distinguish universal-baseline Piper learning vs. proprietary per-customer teaching)
   2. Self-knowledge: Ethics, Spatial intelligence, Growth mindset, Systematic kindness
   3. Flywheel Methodology
   4. Domain knowledge about Product Management (basic sprint cadences; advanced things Christian wants to teach)
   5. Domain knowledge about clients/partners/project owners
   6. Domain knowledge about projects
   7. User patterns and preferences
   8. Command optimization suggestions
   9. Workflow improvements
   10. Conversational inferences (free form?)
4. Start alpha testing on 0.1
5. Pause (document progress, assess status/remaining path to MVP, revise roadmap)
6. Complete build of MVP
7. Start beta testing on 0.9
8. Launch 1.0

Note appended: "1. Piper learning: What specifically should Piper learn first"
```

## Snapshot: version 2.0, "Doc sweep / Pattern sweep" (indentation lost on paste)

Near-identical structure to Oct 9 above but earlier/less complete: A1 through A5 unchanged in content; adds under CORE-LLM-CONFIG a note "Stop use of Anthropic for Piper (use OpenAI, get other keys too!)"; Learning System sub-items show stray numbering artifacts ("Pattern recognition 20.", "Preference learning 21." -- outliner renumbering artifacts, not real issue numbers). Sprint 6/7 content matches Oct 9 snapshot.

## Snapshot: Oct 7, version 1.1.5.4 (indentation lost on paste)

```
1. The Great Refactor
   1. Refactors and fixes: GREAT-1 Orchestration Core (done), GREAT-2 Integration Cleanup (done),
      GREAT-3 Plugin Architecture (done), GREAT-4 Intent Universal (done), GREAT-5 Validation Suite
      (Phase 0 Current state assessment -> Phase 1 Zero-tolerance regression suite [Phase 1.5 Fix
      IntentService Test Fixtures] -> Phase 2 Performance benchmarks -> Phase 3 Integration tests for
      critical flows -> Phase 4 CI/CD quality gates -> Phase Z Validation & Documentation)
   2. Address validation gaps (incl. issues documented that day and the day before)
2. Complete the build of CORE
   1. $$$ ALL STOP -- Review Anthropic subscription (why did high Max acct lock out Opus? make sure
      Claude Code uses the API; make sure personal Claude uses personal account), Review Cursor usage/billing
   2. Address validation gaps
3. Complete the build of CORE

[Session note: "I'll continue with the existing session log and start GREAT-5 Phase 2: Performance
Benchmarks & Gates. Let me update the session log to note we're continuing after a break and then create
the performance benchmark suite." 5:03 -- "Cursor was getting daydreaming running a big test"]
```

A second, slightly earlier pass on the same date shows GREAT-5 as still 🐛 in-progress with a Chief-Architect-review sub-branch (radically simplify; give details conversationally/on-demand per a PM guide; remove time estimates, add infrastructure-verification section to templates; document Session Review Format in the Lead-Dev briefing doc, in knowledge + backed up locally; roadmap review/update; update current state; revise Pattern Sweep) -- this review checklist recurs verbatim across several snapshots as a standing methodology-improvement backlog, not sprint-specific work.

## Snapshot: Oct 6/7 (indentation lost on paste)

Shows GREAT-4 (Intent Universal) mid-flight with its full sub-epic breakdown: GREAT-4A through 4F, each
with phase-level detail (e.g. GREAT-4E "Validation & Documentation" ran twice -- a first attempt with
Phases -1 through Z, then GREAT-4E-2 repeating Phases 0 through Z after gaps were found). GREAT-4F
"Classifier Accuracy & Canonical Pattern Formalization" phases: -1 Current State Verification, 0 ADR
Documentation, 1 QUERY fallback implementation, 2 Classifier prompt enhancement, 3 Classification Accuracy
Testing, 4 Fix Permissive Tests, Z Validation and Metrics, then Chief Arch review (same standing
methodology checklist as above). Multiple earlier passes on nearby dates show GREAT-4B/4C/4D in progress
with granular phase tracking (e.g. GREAT-4D Phase 1 "EXECUTION handler implementation" marked 🐛 at one
point, fully done by a later pass the same window) and a recurring note "BRIEFING TOOK 50% - need to
simplify" flagging a real methodology pain point during this period.

## Snapshot: "ALL STOP (Sept 1X)" -- architectural review kickoff (indentation lost on paste)

```
1. ALL STOP -- Architectural review (15 issues; examine one real complete workflow [plumb github
   make-issue end to end, sequence diagram]; make a plan [dependency order, document what each refactor
   entails, completion criteria, linear execution sequence])
   Document decisions: gather 9/19 working docs, update roadmap.md with CORE-GREAT epic, create GitHub
   issues per REFACTOR epic, write ADRs for major architectural decisions, define briefing content for
   new LLM chats (standards to enforce; project instructions for claude.ai/CLAUDE.md/.cursor; project docs
   PROJECT.md/METHODOLOGY.md/CURRENT-STATE.md/role docs ARCHITECT.md,LEAD-DEV.md,PROGRAMMER.md; prompts),
   place docs in project and knowledge
2. The Great Refactor
   Standards to enforce: strict domain model separation, MCP + spatial intelligence, Flywheel methodology,
   strict separation of user config layer
   Refactors and fixes:
     REFACTOR-1: Orchestration Core (2wk) -- QueryRouter integration (PM-034), initialize
       OrchestrationEngine properly, remove workarounds/TODOs, test GitHub issue creation e2e, lock w/
       comprehensive tests
     REFACTOR-2: Integration Cleanup (1wk) -- complete GitHub service refactor, single pattern through
       orchestration, config cross-validation, fix bad doc links, enforce methodology in all agents
     REFACTOR-3: Plugin Architecture (2wk) -- plugin interface, extract GitHub/Slack/Notion to plugins,
       test all integrations
     REFACTOR-4: Intent Universal (1wk) -- mandatory intent classification, remove bypass routes, test
       every user flow, document intent patterns
     REFACTOR-5: Validation Suite (1wk) -- address validation gaps, integration test suite, performance
       benchmarks, staging deployment, monitoring setup
   Address validation gaps
3. Complete the build of CORE
4. Start Piper education
5. Start alpha testing on 0.1
6. Complete build of MVP
7. Start beta testing on 0.9
8. Launch 1.0
```

Short map from the same era: "1. Fix response layer, 2. ALL STOP Architectural review, 3. The Great
Refactor, 4. Testing Validation, 5. Complete build of CORE, 6. Piper education, 7. alpha 0.1, 8. MVP,
9. beta 0.9, 10. Launch 1.0" -- and a fuller pre-ALL-STOP pass showing "Fix web UI" (fix intent layer
[done], fix response layer [in progress]) still active before the architectural review was called.

## Snapshot: Chief of Staff chat resumption + near-term inchworm plan (earliest captured, indentation lost)

Covers: finishing a Track/Epic Review with retrospective architectural insights; a documentation catch-up
pass (doc sweep, pattern sweep, ADR catch-up covering Intent Classification / Multi-Agent Coordination /
Plugin Interface patterns, then ADR-031 through ADR-034; new daily-omnibus-session-log concept documented;
project knowledge updated); planning (full architectural walkthrough, roadmap revision, a running
plan-tracking document -- the direct ancestor of this inchworm map itself); then the near-term plan: fix
web UI -> ALL STOP -> The Great Refactor (TBD) -> Complete build of CORE (Plug-in epic PLUG: align with
spatial intelligence model, build plugin interface, build first plugin, refactor GitHub/Notion/Slack to
plugin level; add intent classification; complete standup integration incl. fixing response layer and
regression-testing greet/chitchat/github/upload/summarize/analyze/piper-help/slack/notion/calendar/standup)
-> Piper learning (same 10-item list as later snapshots) -> alpha 0.1 (Dave Feldman named as first alpha
tester) -> MVP feature checklist (chitchat, github integration, knowledge, integrations, morning standup)
-> beta 0.9 -> pause/revise -> continue.

---

## Final, most complete snapshot (Bike outliner, code-block paste -- indentation preserved, treat as authoritative structure)

```
Piper Morgan Inchworm Map
✅ The GREAT Refactor
✅ CORE functionality
	✅A1: Critical Infrastructure
		✅Prep for A1
			✅Docs
				✅Roadmap review
				✅Omnibus log for 10/8
				✅List of TODOs
			✅Token efficiency
				✅Install Serena MCP
				✅Use handoff for efficient briefing
		✅ INFR-DATA #113 (1d) - Database migration (fixed in doc cleanup 10/8)
		✅CORE-TEST-CACHE #216 (30 mangos) - Quick warm-up
		✅INFR-DATA #145 (1 diga) - Fix Slack asyncio bug
		✅CORE-LLM-CONFIG #217 (1-2d) - API keys (blocks everything)
			❌First attempt
				✅Phase 0: Investigation
				✅Phase 1: Environmental variables
				❌Cursor to cross-validate
			✅ARCH ISSUE DISCOVERED -NEW GAMEPLAN
				✅Phase 0: Investigation
				✅Phase 1: LLM Domain Service Creation
				✅Phase 2: Consumer Migration to ServiceRegistry
				✅Phase 3: Testing and Deprecation Warnings
			✅Phase 1: Core infrastructure
				Phase 5.1: keychain
					✅Sub-phase A
					✅Sub-phase B
					✅Sub-Phase C: Migration CLI (1 hour => 4 min).
				✅Phase 2: Multi-provider
					✅Add selection config to LLMConfigService
					✅Write tests for selection logic
					✅Create ProviderSelector service
					✅Write tests for ProviderSelector
					✅Update environment configuration
					✅Update client code to use selection
					✅Update startup validation
					✅Cursor to cross-validate
				✅Phase 3: Key setup / setup tooling
				✅Phase 4: Documentation
				✅Phase Z: Provide verification evidence for acceptance criteria, commit code (#215 and #145 as well), push with PM approval
				✅Chief Architect check-in
		✅Cursor Serena codebase investigation => CRAFT (Craft Pride) epic before A2
		✅CORE-INTENT-ENHANCE #212 (4-6 hurons) - Better classification
			Phase 0: Investigation
			✅Phase 1: IDENTITY enhancement
			✅Phase 2: GUIDANCE enhancement
			✅Phase 3: Pre-Classifier Pattern Expansion
			✅Phase 4: Validation
			✅Phase Z: Documentation and issue closer
			✅Chief Architect review
				✅#212 and A1
				✅Serena briefing model
				✅Planning CORE-CRAFT
	✅CORE-CRAFT
		✅CRAFT-GAP
			✅CRAFT-GAP-1: Phase -1 recon through Phase 5 LEARNING handlers (EXECUTION/ANALYSIS/SYNTHESIS/
			  STRATEGY/LEARNING handler phases, each w/ study-requirements/define-strategy/TDD-tests/
			  implement/run-tests/evidence sub-parts), Phase Z docs+commit+push, retro w/ Lead Dev, review
			  w/ Chief Architect + plan GAP-2
			✅CRAFT-GAP 2: Phase -1 recon, Phase 0 test validation (bypass prevention tests across CLI/
			  Slack-event-handler/Slack-plugin, 16 bypass tests, interface validation, contract tests, cache
			  perf tests), Phase 1 runtime validation, Phase 2 evidence collection, bonus fixes (2yr-stale
			  libraries modernized, 3 production bugs fixed, CI/CD enforcement activated)
			✅FOUNDATION cleanup: fix failing GH Actions workflows, fix router pattern violations, fix CI
			  tests workflow (prevent-direct-adapter-imports hook), document LLM architecture state
			✅CRAFT-GAP-3: accuracy analysis, pre-classifier enhancement, LLM classifier enhancement, docs
			  & validation, close CRAFT-GAP, report to Chief Architect, plan CORE-CRAFT-PROOF
		✅CRAFT-PROOF: Stage 1 discovery, Stage 2 documentation (8 numbered proofs), Stage 3 precision
		  (remaining proofs), close with evidence, Chief Architect review -> plan CRAFT-VALID
		✅CRAFT-VALID: recon, VALID-1 Serena, VALID-2
		✅Architect review: CORE-CRAFT retro, roadmap review (Alpha epics + MVP roadmap updates), gameplan
		  for A2
	✅A2: Notion & Errors
		✅ Issue 1: CORE-NOTN-API #142 (5h) - API connectivity fix
		✅ Issue 2: CORE-NOTN-USER #136 (1d) - Remove hardcoding
		✅Issue 3: CORE-NOTN-UP #165 (Phase 1) - Database API upgrade
		✅Issue 4: CORE-INT #109 (5h) - Legacy deprecation verification
		✅Issue 5: CORE-ERROR-STANDARDS #215 (1-2d) - Standardize errors
		✅Architect check-in: review #215 and A2, gameplan for A3
		➡️Process check: update briefing docs (current-format update, refactor to single-source-of-truth),
		  🐛automate updating current-state after each session
	✅A3: Core Activation
		✅CORE-MCP-MIGRATION #198 - Model Context Protocol (Calendar/GitHub/Notion/Slack integration phases)
		✅CORE-ETHICS-ACTIVATE #197 - Ethics middleware (BoundaryEnforcer refactor, IntentService integration,
		  multi-channel validation, docs, Slack gap fix)
		✅CORE-KNOW #99 - Connect knowledge graph (integration architecture/implementation/testing,
		  CORE-KNOW-BOUNDARY #226 sub-phase, docs)
		✅CORE-NOTN-UP #165 - Database API upgrade (DB ops, integration testing, docs)
	✅A4: Standup Epic
		✅Phase 0: Discovery and assessment
		✅Phase 1: CORE-STAND-FOUND (#119) -- bug fix, test verification across 5 generation modes incl.
		  GitHubIntegrationRouter adapter-method fixes
		✅Phase 2: CORE-STAND-MODES-API (#162) - Surface multi-modal generation (API design, service
		  integration, authentication integration incl. JWT bug fix, OpenAPI docs, error handling, unit +
		  integration testing)
		✅Phase 3: CORE-STAND-SLACK-REMIND (#161) - Slack reminder integration (job implementation,
		  preference extension, testing/reliability incl. ReminderMessageFormatter, integration testing)
		✅ Phase 4: CORE-STAND (#120) - Integration and documentation
	✅A5: Learning System
		✅CORE-LEARN-A: Infrastructure foundation (discovery, API layer, application integration, user
		  preferences, testing & integration)
		✅CORE-LEARN-B: Pattern recognition (3 new pattern types: TEMPORAL/COMMUNICATION/ERROR)
		✅CORE-LEARN-C: Preference learning (apply_preference_pattern, QueryLearningLoop wiring)
		✅CORE-LEARN-D: Workflow optimization (Chain-of-Draft experiments, workflow templates)
		✅ CORE-LEARN-E: Intelligent automation (ActionClassifier, EmergencyStop, AuditTrail,
		  PredictiveAssistant, AutonomousExecutor, UserApprovalSystem)
		✅CORE-LEARN-F: Integration & polish (use controls, Learning Dashboard UI w/ 7 cards, integration
		  testing)
	✅ A6: User Onboarding
		✅ CORE-LLM-SUPPORT: LLMAdapter interface + Claude/OpenAI/Gemini/Perplexity adapters + LLMFactory
		✅CORE-USERS-JWT: TokenBlacklist class + DB model + JWT service + logout integration + tests
		✅CORE-USERS-PROD
		✅CORE-USERS-API: UserAPIKey model/service, KeychainService multi-user support, key rotation,
		  API endpoints, docs
		✅ CORE-AUDIT-LOGGING: AuditLog model + migration + AuditLogger service + JWT/API-key audit
		  integration + tests + docs
		✅ CORE-USERS-ONBOARD: setup wizard, status checker, README + troubleshooting docs, PM manual testing
	✅A7: Polish and Buffer
		✅ Critical fixes: CORE-KNOW-BOUNDARY-COMPLETE, CORE-AUTH-CONTAINER
		✅ CORE-USER: CORE-USER-ALPHA-TABLE, CORE-USER-MIGRATION, CORE-USER-XIAN, tech-debt issues created
		✅Lead Dev fugue state improv group: CORE-UX-RESPONSE-HUMANIZATION, CORE-UX-ERROR-MESSAGING,
		  CORE-UX-LOADING-STATES, CORE-UX-CONVERSATION-CONTEXT
		✅CORE-UX: CORE-UX-QUIET, CORE-UX-STATUS-USER, CORE-UX-BROWSER
		✅CORE-KEYS: CORE-KEYS-ROTATION-REMINDERS, CORE-KEYS-STRENGTH-VALIDATION, CORE-KEYS-COST-ANALYTICS
		✅CORE-PREF-CONVO
	✅A8: Alpha prep
		✅Planning: Chief Architect review, Chief of Staff review (work streams, weekly ship, alpha
		  planning, ideas incl. email to Sam Zimmerman re ethics infra, Haiku 4.5 experiment setup, smoke
		  test debugging, bot-checker prep, draft alpha phase 4/5 docs), revise A8 plan w/ Chief Arch
		✅Phase 1: Critical Integrations: TEST-SMOKE-HOOKS, CORE-KEYS-STORAGE-VALIDATION,
		  CORE-PREF-PERSONALITY-INTEGRATON, CORE-KEYS-COST-TRACKING, CORE-KNOW-ENHANCE
		✅Phase 2: End-to-end workflow testing
			✅Investigation, Phase 2.1 automated testing against MVP, Phase 2.2 User Journey Testing
			  (alpha deployment prep, welcome email/onboarding checklist, Alpha User Day 1 walkthrough:
			  setup wizard/API keys/preferences/first conversation/upload doc/create GH issue)
			✅Phase 2.2.5 - fix blocker issues from initial testing:
				✅P0 blockers: CORE-ALPHA-DATA-LEAK #280, CORE-ALPHA-FILE-UPLOAD #282,
				  CORE-ALPHA-WEB-AUTH #281, CORE-ALPHA-DOC-PROCESSING #290 (added from #282)
				✅P1 critical: CORE-ALPHA-ERROR-MESSAGES, CORE-ALPHA-TODO-INCOMPLETE
				  (-> CORE-ALPHA-TODO-PERSISTENCE, phases 1-Z), CORE-ALPHA-ACTION-MAPPING
				  (-> CORE-ALPHA-ACTIONMAPPER-CLEANUP), pattern sweep update, resume e2e testing
				✅P2 important: CORE-ALPHA-CONVERSATION-PLACEMENT, CORE-ALPHA-TEMPORAL-BUGS,
				  CORE-ALPHA-TOKEN-BLACKLIST-FK, CORE-USER-ID-MIGRATION, documentation updates
				  (Alpha Tester Guide, Known Issues, Quick start, Agreement, Email template)
				✅P3 misc: CORE-ALPHA-SETUP-PASSWORD, CORE-ALPHA-LEARNING-INVESTIGATION,
				  CORE-ALPHA-MIGRATION-PROTOCOL, CORE-ALPHA-AUTH-INTEGRATION-TESTS,
				  CORE-ALPHA-LEARNING-BASIC (#300)
✅ ALPHA foundation
	✅Initial alpha testing - 0.8.0
		✅T1 (Test Repair)
			✅ P0 - critical: TEST-PHANTOM-SPATIAL, TEST-INFRA-ENUM, TEST-DISCIPLINE-KNOWN, TEST-SMOKE-HOOK
			✅ P1 - urgent: TEST-DISCIPLINE-CATEGORIES, TEST-INFRA-CONTAINER, TEST-DISCIPLINE-HOOK,
			  SLACK-SPATIAL
		✅Q1 (Quick Wins): DEV-VSCODE-SETUP, DEV-OS-DETECT, ARCH-FIX-WRAPPER, BUG-TEST-SECURITY,
		  UX-DESIGN-TOKENS
		✅S1 (Security Foundation): DEV-PYTHON-311, BUILD-WINDOWS-CLONE, PERF-INDEX,
		  SEC-RBAC (Phase -1 through Z incl. Role/Permission/RolePermission/UserRole models, owner_id
		  columns, seed data, DB-JSON-INDEX, AuthorizationService, permission decorators/middleware,
		  4-phase comprehensive testing + security scan, final bookending/security sign-off)
		✅A9 (Final Alpha Prep): front-end permission awareness, Alpha onboarding docs review/update,
		  clean branch + push 0.8.1 to production
	✅ Alpha onboarding/auth testing - 0.8.1, 0.8.1.1-3, 0.8.2
		✅ A10 - Alpha Testing: session_scope audit, ALPHA-ONBOARD-FLAG, CORE-AUTH-CLI-KEYS,
		  BUG-SETUP-KEYS-REINSTALL, ALPHA-ONBOARD-DETECT, ALPHA-BUG-DASHBOARD-UI, CORE-UX-AUTH,
		  SETUP-WIZARD-HYGIENE, ALPHA-ONBOARD-UX, ALPHA-SETUP-UI, BUG-DB-CONCURRENCY, ALPHA-UX-LOGO,
		  BUG-UX-DISTRACTION, ALPHA-UX-BUG (base.css), ALPHA-UX (suppress browser auto-open),
		  INFRA-DB-442, BUG-P0 (chat submit/create 401), BUG-P1 (standup errors, endpoint mismatch),
		  P0 (component integration gap), FLY-COORD-TREES-1, P0 (API contract mismatch), DI provider
		  pattern incomplete, UX menu restructure
		✅ A11 - Alpha Polish: CORE-UX-ERROR-QUAL, ALPHA-UX-ENHANCE, ALPHA-SETUP-TEST, setup-wizard
		  function-extraction refactor, ALPHA-SETUP-CLI (Gemini key)
		✅ T2 - Test Polish: TEST-PHANTOM-VALIDATOR (44 phantom tests), TEST-SMOKE-STATIC,
		  TEST-INFRA-FIXTURES (53 tests), TEST-SMOKE-RELY, TEST-PHANTOM-AUDIT, TEST Infrastructure
		  Repair Super Epic, pytest collection error investigation, P3 Test Reliability Issues
	✅ A12 - Alpha Setup evolution - 0.8.3
		✅ test_intent_enricher schema-mismatch bug, BUG-P0 unhandled EXECUTION actions 422,
		  TEST-FIX bypass_prevention 401, ALPHA-SETUP-VERIFY (health dashboard), ALPHA-SETUP-NOTION,
		  Integration-Test-button MCP-vs-OAuth bug, Notion/GitHub stuck-integration recovery paths,
		  ALPHA-SETUP-CALENDAR, ALPHA-SETUP-SLACK, ALPHA-SETUP-MANAGE, ALPHA-SETTINGS-INTEGRATIONS,
		  ARCH-SCHEMA-VALID, ARCH-FIX-SINGLETON, FTUX-TESTPLAN, FLY-MAINT-CLEANUP
	✅Sprint Mu (ur-MVP work): CORE-CONFIG-PIPER, DOCUMENTATION-STORED-PROCS, BUG-TEST-CONFIG,
	  BUG-HEALTH-UTC, INFR-DATA (repository pattern), INFR-MAINT-REFACTOR, CONV-MCP-MEASURE, UX-POLISH
	  (7 features), MVP-UX-QUICK (5 wins), CONV-UX-NAV, UX-TRANCHE3, TEST-SMOKE-BUG-BUS,
	  AUTH-PASSWORD-CHANGE, CONV-MCP-STANDUP, CONV-LEARN-PREF, INFR-CONFIG-PERF
🐛Complete build of MVP
	✅ B1 - Beta Enablers - 0.8.3.1, 2: FTUX-PIPER-INTRO, FTUX-EMPTY-STATES, FTUX-POST-SETUP,
	  FTUX-QUICK-2, FTUX-QUICK-3, FTUX-CHAT-BRIDGE #550, FTUX-CONCIERGE, CONV-UX-GREET,
	  CONV-MCP-STANDUP-INTERACTIVE (STANDUP-CONV-STATE/FLOW, STANDUP-CHAT-WIDGET, STANDUP-LEARNING,
	  STANDUP-PERF), SLACK-ATTENTION-DECAY, FTUX-PORTFOLIO, TEST-GAP, echo/echolalia bug, CONV-UX-PERSIST
	  (CONV-PERSIST-1/2/3/4), CORE-SETTING-DISCONNECT, CORE-SETTINGS-INTEGRATION (ENHANCE-SETTINGS
	  Slack-channel/calendar-sync/Notion-workspace/GitHub-repo prefs; ENHANCE Notion/GitHub/Calendar/
	  OAuth credential config in UI), conversation-history-panel-switch bug
	✅Alpha testing round 2 - 0.8.4
		✅ A20 - Alpha Testing round 2 - 0.8.4, .1, .2: chat-input-ignores-selection bug, standup
		  no-projects bug, calendar timezone-aware queries, replies-not-persisting bug, /standup
		  routing bug, TECH-DEBT user_id/session_id docs, markdown-rendering regression,
		  ARCH-TEMPORAL-GAPS, UX-AUTO-TITLE, UX-SUPPRESS-NULLS, UX-REMOVE-REDUNDANT, test fixture
		  bugs (x2), FLY-RUN-RESTART, UX-EDITABLE-TITLES #604, setup-wizard-continue-button
		  regression, migration 44f5cd40b495 bug, fresh-install routing bug, setup-access-for-new-
		  registration #608, fresh-db-migration-bypass #609, FLY-HOOKS-CLEANUP #610
		✅A21 - Alpha testing round 2.1 - 0.8.4.3: BUG-ALPHA-DOCKER, BUG-ALPHA-RACE, BUG-ALPHA-TOAST
	✅MUX: Modeled User Experience (Super epic #398)
		✅MUX-V1: Vision, Conceptual architecture formalization #401: VISION-OBJECT-MODEL #399
		  (Phase P0 through PZ, incl. #612-#618), MUX-VISION-GRAMMAR-CORE #404, MUX-VISION-CONSCIOUSNESS
		  #400, MUX-VISION-METAPHORS #405, MUX-VISION-FEATURE-MAP #406, MUX-GATE-1 #531
		✅MUX-TECH - X1 - Architectural model implementation: MUX-TECH-PHASE1-GRAMMAR #432,
		  MUX-TECH-PHASE2-ENTITY #433, MUX-TECH-PHASE3-OWNERSHIP #434, MUX-INTENT-MULTI, MUX-GATE-2
		✅MUX-V2: Integration Mapping: MUX-VISION-FEATURE-MAP, MUX-VISION-STANDUP-EXTRACT,
		  MUX-VISION-CONSCIOUS (CONSCIOUSNESS-TRANSFORM x9: Standup/Loading/Error/CLI/Search/Files/
		  Learning/Settings/HTML, plus smaller confirmations-standardization items), MUX-VISION-GRAMMAR
		  (GRAMMAR-TRANSFORM x9: Conversation/Intent/Slack/GitHub/Personality/Calendar/Feedback/
		  Onboarding/Etc-long-tail), MUX-VISION-MULTICHAT (MUX-MULTICHAT-PHASE0 x3: ADR-050 status,
		  schema design x2), MUX-VISION-LIFECYCLE-SPEC, MUX-VISION-LEARN, MUX-GATE-3, MUX-LISTS - L1 -
		  List Management (MUX-VISION-LIST-TODO, MUX-VISION-LIST-MGMT)
		✅ MUX-INTERACT: Interaction Design: ARCH-COMMANDS, MUX-INTERACT-DISCOVERY,
		  MUX-INTERACT-TRUST-LEVELS (TRUST-LEVELS-1/2/3), MUX-INTERACT-RECOGNITION,
		  MUX-INTERACT-INTENT-BRIDGE, MUX-INTERACT-CANONICAL-ENHANCE, MUX-INTERACT-DELEGATION,
		  MUX-INTERACT-WORKSPACE (WORKSPACE-DETECTION/NAVIGATION/ISOLATION/MEMORY incl.
		  MEM-ADR054-P1/P2/P3/P4), MUX-TECH deferred (MUX-TECH-LISTS, MUX-TECH-PHASE4-COMPOSTING incl.
		  COMPOSTING-MODELS/BIN/PIPELINE/SCHEDULE), MUX-INTERACT-PREMONITION, MUX-INTERACT-ATTENTION,
		  MUX-INTERACT-MOMENT-UI, MUX-FTUX-CONVERSE, MUX-INTERACT-PORTFOLIO-DEL,
		  MUX-INTERACT-CONV-SEARCH, MUX-WIRE (MUX-WIRE-DISCOVERY/PROJECTS-PAGE/TRUST/MEMORY/PORTFOLIO/
		  WORKFLOW-MSG), MUX-GATE-4
		✅MUX-IMPLEMENT: UI Polish
			✅P1 - Navigation Breakthrough: MUX-NAV-HOME, MUX-NAV-UTILITY, MUX-NAV-PALETTE, MUX-NAV-PLACES
			✅P2 - Document Management: MUX-IMPLEMENT-DOCS-ACCESS, MUX-IMPLEMENT-LIFECYCLE,
			  MUX-IMPLEMENT-COMPOST
			✅ P3 - Cross-Channel Unity: MUX-IMPLEMENT-MEMORY-SYNC, MUX-IMPLEMENT-CONSISTENT,
			  MUX-IMPLEMENT-CONVERSE-MODEL, MUX-LIFECYCLE-OBJECTS (glossary update, MUX-LIFECYCLE-UI-A,
			  MUX-LIFECYCLE-UI-TODOS, MUX-LIFECYCLE-UI-PROJECTS, MUX-WORKITEMS-VIEW,
			  MUX-PROJECT-DETAIL-VIEW, lifecycle_state-columns-missing bug)
			✅P4 - Accessibility & Polish: MUX-IMPLEMENT-THEME-CONSISTENCY, MUX-IMPLEMENT-ARIA,
			  MUX-IMPLEMENT-CONTRAST-TESTS, "MVP: Minimum Valuable Product" marker
	✅ Alpha testing round 3 - end-to-end - 0.8.5
		✅Sprint A30 - setup: BUG-ALPHA-DOCKER, BUG-ALPHA-RACE, BUG-ALPHA-TOAST, race-condition
		  first-load, missing stylesheet, first-time-user routing, logout bug, LLM-keys-per-user-
		  retrieval bug, chat-refresh regression, sidebar regression, autofill bug, portfolio-onboarding
		  save bug, history-button bug, username-display bug, conversations-not-persisting fix,
		  history-button trust-gate fix, projects-not-saving debug, SEC-MULTITENANCY,
		  FINISH-HISTORY-SIDEBAR, projects-unique-constraint bug (multi-tenancy), portfolio-onboarding
		  routing bug
		✅ Sprint A31 - workflows: entity-extraction-regex bug, _store_classification bug, LLM-tests-
		  keychain-loading, test_pm039_patterns bug, todo-intent-handler empty-message bug,
		  todo-handler user_id bug, [TECH-DEBT] auth context injection, TECH-DEBT schema-drift
		  datetime, todo-workflow-polling bug, knowledge-graph-entity-query bug,
		  [#747-A/B/C/D/E/F] datetime_utils work, TEST-FIX file_resolver/file_scoring/
		  plugins_functional, TECH-DEBT #734 multi-tenancy migration, AUDIT timezone handling,
		  TokenBlacklist timezone bug, setup-completion timezone bug, AUDIT schema drift,
		  Slack-credentials-save bug, schema-drift false positive, Notion-API-key-prefix bug,
		  Notion-keychain-option bug, Notion-validate-button styling, PATTERN-SWEEP 2025-12-24 to
		  2026-02-04, FTUX-overlay bug, history-sidebar 404 bug, Notion-plugin-crash bug, #734 test
		  update, knowledge_nodes schema drift, calendar-plugin-crash bug, conversation-sidebar bug,
		  Invalid-Date bug, calendar "no meetings" bug, [SETUP] uvloop Windows, [DB] migration
		  70847a6596f3 bug, [SETUP] CRLF bug, [DB] schema-validation 6 mismatches, [SETUP]
		  account-creation error, [DOCS] docker-compose syntax, [DOCS] quick-start time estimate,
		  [DOCS] setup paths, [DOCS] venv clarification, [SETUP] localhost-vs-127.0.0.1, [DOCS]
		  pip-upgrade step, [SETUP] smoke-test script, [DOCS] postgres-browsing instructions, [UX]
		  error-message interpretation, [SETUP] alpha-setup.bat bug, [CI] Windows test matrix,
		  [SETUP] Windows smoke-test script
🐛MVP - march to beta - 0.8.6
	✅ M0 - Conversational Glue - EPIC: GLUE - Conversational Glue Implementation: GLUE-HISTORY-DIFF,
	  GLUE-FOLLOWUP, GLUE-MULTI, GLUE-SLOT, GLUE-PROJ, GLUE-SOFT (incl. GLUE-SOFTINVOKE), UX
	  GitHub-connection-to-projects (FEAT #859/#860/#861/#862/#863), misc bugs (TrustStage hardcoded,
	  conversation-not-appearing, 90+ failing tests, REFACTOR Repository-as-entity, flaky
	  test_verbosity_gradient, planning/workflow-status/issue-soft-invocation raw-error bugs, SYSTEMIC
	  #385 business-errors-to-422, TECH-DEBT 56 raw error messages, extraneous workflow polling,
	  GitHubIntegrationRouter assignees param, calendar-credential 401, SEC-KEYCHAIN audit),
	  M0-GLUE Sprint Completion Gate
	🐛 M1 - MVP Foundation: Frontloaded work (CONV-MCP-MEASURE, BUG-HEALTH-UTC, BUG-TEST-CONFIG,
	  UX-POLISH, MVP-UX-QUICK, UX-TRANCHE3, INFR-DATA, CORE-CONFIG-PIPER, CONV-UX-NAV,
	  DOCUMENTATION-STORED-PROCS, INFR-MAINT-REFACTOR); re-test canonical queries; MVP-MUX
	  (MUX-LIFECYCLE-UI-B, MUX-OBJECTS-VIEWS, MUX-PRODUCT-MODELING); ARCH WebSocket Infrastructure;
	  CONV-UX-QUICK Settings & Startup Quick Wins; MVP-TEST (TEST-SMOKE epic incl.
	  ✅TEST-SMOKE-BUG-BUS/TEST-SMOKE-E2E/TEST-SMOKE-CI, QA manual testing, INFR-TEST, POST-TEST-E2E,
	  TEST-QUALITY, BUG-TEST-ASYNC, TEST-INFRA attention-sim, TEST-FIX response_handler_observability);
	  MVP-SEC (✅BUG-AUTH settings_integrations/intent_service hardcoded user_id, SEC token-revocation-
	  on-disconnect, EPIC SEC-RBAC Phases 4-5, EPIC Slack-Integration-TDD-Gaps, SEC-KMS-INTEGRATION);
	  CORE-LEARN-PHASE-3
	M2 - MVP Activation 0.8.6.5: MVP-MUX (MUX-WIRE-DOD, WIRE-BOUNDARY/CANONICAL/SLACK/STANDUP/
	  GITHUB-LLM/GITHUB-CMD, MUX-LIFECYCLE-UI, MUX-INSIGHT-SURFACING, MUX-LISTS-LIFECYCLE-UI,
	  MUX-HOME-CONVERSATIONS-LIFECYCLE); MVP-INFRA (INFRA-TIMESERIES, EPIC Infrastructure OAuth/
	  Learning/TimeSeries/Conversation, INFR-TEST); EPIC Slack-Integration-TDD-Gaps;
	  CONV-INFR-NOTN Activate Existing Notion Integration
	M3 - MVP Skills - 0.8.6.8: INFR-AGENT Multi-Agent Coordinator Operational Deployment,
	  CONV-UX-DESIGN Unified Design System & Token Migration, CONV-MCP-LIBRARY Core Skills Library,
	  CANONICAL-#9 (CONV-FEAT-PRIOR Priority Calculation Engine), CANONICAL-#10 (focus guidance
	  synthesis), MVP-MUX (MUX-LIFECYCLE-UI-A, MUX-FEATURES-VIEW), MVP-PIPER-SKILLS (CONV-MCP-PROTO
	  DocumentAnalysisSkill Prototype, basic PM skills?), SLACK-MEMORY persist spatial patterns
	M4 - MVP Document Revolution 0.8.7: CONV-MCP-DOCS Unified Document Processing via Skills,
	  CONV-UX-DOCS File Browser & Document Management UI, DOCS-STOPGAP Basic Artifact Persistence,
	  MUX-DOCUMENT-VIEWER, MUX-DOCUMENTS-LIFECYCLE-UI
	M5 - MVP Polish 0.8.7.5: FLY-VERIFY Three-Tier Verification Pyramid (FLY-VERIFY-HAND,
	  FLY-VERIFY-CONFIG), CONV-UX-SLACK Interactive Slack Standup Features, RESEARCH-TOKENS-THINKING,
	  INFRA-MIGRATION-ROLLBACK, CORE-UX-AUTH-PHASE2 Registration/Password-Reset/Security-Polish,
	  FLY-COORD-TREES Git Worktrees for Multi-Agent Coordination, CORE-LEARN-PHASE-3
	M6 - MVP Future 0.8.8: CORE-ETHICS-TUNE, MUX-STANDUP-CONVERSE, MUX-CORE-PORTFOLIO-ACROSS,
	  CONV-FEAT-PROJ, CONV-FEAT-TIME, CONV-FEAT-ALLOC, COMPOSTING-HYBRID-TRIGGER, FLY-COORD-TREES-2,
	  TECH-DEBT alternate issue providers, CORE-KEYS-ROTATION-WORKFLOW, SEC-KMS-INTEGRATION,
	  🛑 SEC-ENCRYPT-ATREST
	M7 - MVP Distro 0.8.9 - EPIC: DIST — Distribution Packaging (MCP-Native + Desktop):
	  DIST-MCP-PACKAGE, DIST-MCP-DOCS, DIST-MCP-REGISTRY, DIST-MCP-TEST, DIST-SQLITE, DIST-WRAPPER,
	  DIST-UPDATE, DIST-INSTALLER, DIST-FIRST-RUN, "Needs gate"
Start BETA testing on 0.9: Hosted version, Auto-installer, Enhancements backlog, Launch blocker
  verification
Launch 1.0
Fast-Follow: MUX-LIFECYCLE-ANIMATIONS
Post-MVP: DEFERRED-#427 (ADR-050 Conversation Graph Phase 1-3), CONV-FEAT-STRAT
Open source project milestone
Enterprise milestone
```

---

## PM's own summary of the Sept 20 - Oct 27 window (context, not a sprint list)

> From September 20 to October 27, we completed: GREAT-1 Orchestration Core, GREAT-2 Integration Cleanup,
> GREAT-3 Plugin Architecture, GREAT-4 Intent Universal (7 sub-epics!), GREAT-5 Validation Suite.
> Result: Complete architectural transformation with zero technical debt, 602K req/sec performance,
> 200+ tests, production-ready quality.
> Sprint A1 Beginning — Starting with CORE-TEST-CACHE #216 as warm-up, then progressing through
> critical infrastructure.
