# Inactive open issues (updatedAt before 2026-10-03), review of 2026-11-02

Source: gh issue list --state open (362 open at run time, not 363), filtered by updatedAt before 2026-10-03 gives 114. Bodies (first 40 lines) and last comments read via gh issue view. Code checks were read-only greps in the docs worktree at f7599ac649. No tests were run (no pytest in that environment), so test-state claims are marked read not run.

| # | title (short) | milestone | recommendation | one-line reason |
|---|---|---|---|---|
| 1298 | Remove dead templates/components/navigation.html + retire it | Production | CLOSE | Template file gone (deleted in commit 741c531918, chore 1522) and the dead-code test file tests/unit/templates/test_navigation.py is absent in the docs worktree at f7599ac649 |
| 1359 | cli/commands/notion.py: self.adapter referenced 10x but neve | Production | CLOSE | cli/commands/notion.py docstring says self.adapter was fixed to the live path (read in worktree, tests not run) |
| 1367 | test_execution_intent_no_placeholder fails: mocks .classify  | Production | CLOSE | Test now mocks classify_multiple per its own #1452 docstring (read not run) |
| 1446 | Stale test: test_security_framework TestFederationReadiness  | Fast Follow | CLOSE | tests/test_security_framework.py now defines the test_client fixture (#1452 repair, read not run) |
| 57 | FEAT-MEET: Transcript Analysis & Visualization | Enterprise | KEEP | Enterprise backlog feature, deferred by design |
| 58 | FEAT-DASH: Analytics Dashboard Integration | Enterprise | KEEP | Enterprise backlog feature, deferred by design |
| 66 | FEAT-PREDICT: Predictive Project Analytics | Enterprise | KEEP | Enterprise backlog feature, deferred by design |
| 103 | CONV-FEAT-PRIOR: Priority Calculation Engine | Fast Follow | KEEP | Deferred to Fast Follow by recorded 2026-04-08 decision |
| 104 | CONV-FEAT-ALLOC: Time Allocation Analysis | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 106 | CONV-FEAT-STRAT: Strategic Recommendations | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 159 | FEAT-STAND-MODEL: Sprint Model & Team Coordination | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 213 | MVP-QUALITY-ENHANCE: Enterprise Infrastructure & Advanced Mo | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 243 | MVP-STAND-MODES-UI: Advanced Multi-Modal UI Controls | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 251 | ENT-KEYS-TEAM-SHARING: Team API Key Sharing (Enterprise) | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 299 | AUTH-CONCURRENT-SESSIONS: Add Concurrent Session Handling Te | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 321 | DATA-AUDIT-FIELDS: Standardize audit fields across all domai | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 326 | ARCH-MULT-ORG: Design multi-organization (multi-tenant) supp | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 328 | OBSERV-CENTRAL: Implement centralized logging, metrics, and  | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 364 | SLACK-MULTI-WORKSPACE: Support attention across multiple wor | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 373 | INFRA-OAUTH-MULTI: Implement Multi-OAuth Installation Infras | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 374 | Enhancement: Semantic classification for preference detectio | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 546 | TECH-DEBT: Support alternate issue providers (Jira, Linear,  | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 568 | MUX-CORE-PORTFOLIO-ACROSS: Cross-channel portfolio sharing | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 650 | FUTURE-CONSCIOUSNESS: Settings Reset confirmation pattern | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 686 | MUX-LIFECYCLE-ANIMATIONS: Add transition animations for life | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 688 | POST-MVP: ADR-050 Conversation Graph Phase 1-3 Implementatio | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 698 | ADVANCED: Guided Process - Planning Sessions | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 699 | ADVANCED: Guided Process - Feedback Sessions | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 700 | ADVANCED: Guided Process - Pending Clarification Handling | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 702 | MUX-LIFECYCLE-NOTIFICATIONS: Backend notification queue for  | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 716 | MUX-FEATURES-VIEW: Create Features View with Lifecycle | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 760 | TECH-DEBT: Add slack_workspaces table for proper team_id → u | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 828 | EPIC: DIST — Distribution Packaging (MCP-Native + Desktop) | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 833 | DIST-SQLITE: SQLite adapter for repositories | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 834 | DIST-WRAPPER: Desktop application wrapper | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 835 | DIST-UPDATE: Auto-update mechanism | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 836 | DIST-INSTALLER: Platform installers | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 837 | DIST-FIRST-RUN: First-run experience | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1045 | POST-MVP: Project Detail Activity tab — design + content | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1062 | CORE-LEARN-PHASE-3: Learning infrastructure phase 3 (broken  | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1154 | POST-MVP: Unified admin/dev console — consolidate scattered  | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1164 | HISTORY-PRIVACY-TOGGLE-STUB: slide-out 'Start private sessio | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 1175 | SOURCE-TYPE-SLOT-LOCATION: revisit intent.context vs intent. | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1179 | LEARNING-CONSOLIDATION-EXPIRY: dedup + expire composted lear | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1181 | BEING-GOOD-INVITED-WATCH: 'let me know if X' standing-watch  | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1203 | KeyAuditService query/report surfaces unwired — deferred to  | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1257 | [REFACTOR] P7 cutover: migrate user_id→owner_id reads + drop | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1281 | People entity source (PeopleEntitySource) — post-beta | Dot Releases (Post-MVP) | KEEP | Open in live Dot Releases (Post-MVP) milestone, scope still stated and no superseding issue found |
| 1295 | BYOC-DIST: MCP-only scenario — skills discovery hint in ask_ | Ongoing | KEEP | Open in live Ongoing milestone, scope still stated and no superseding issue found |
| 1323 | RECONNECT tech-debt: extract BindingBackedConnector mixin (d | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1336 | [placeholder] Expand/refactor canonical-query regression for | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1345 | Route all LLM-billing paths through one fail-closed wrapper  | Production | KEEP | Arch-ratified durable deferral, 1343 closed |
| 1349 | [BUG] test_github_place_has_name asserts repo name in Place. | Production | KEEP | Test still asserts repo name in Place.name at line 73, still stale |
| 1361 | Notion: repoint legacy services/integrations/mcp/notion_adap | Production | KEEP | Legacy shim services/integrations/mcp/notion_adapter.py still exists in worktree |
| 1362 | Notion adapter: rate-limiting tests reference removed _call_ | Production | KEEP | Test already skipped with reason citing 1362, cleanup still open |
| 1363 | test_publish_creates_actual_notion_page: hardcoded fallback  | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1376 | Follow-up to #1279: ~23 more fresh-GitHubIntegrationRouter s | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1379 | Config hygiene follow-ups from #1324 audit (post-beta) | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1385 | tests/security cross-file fixture contamination: full-suite  | Production | KEEP | Open fixture-contamination family, 1531 depends on it |
| 1407 | Day-part greeting sweep: remaining surfaces still compute fr | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1443 | Stale integration test: test_create_tables_from_scratch expe | Fast Follow | KEEP | Test still lists todo_lists at line 77 of test_fresh_database_setup.py |
| 1479 | Flaky (order-dependent): test_github_query_handlers TestComm | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1481 | Socket-mode DM/mention path binds EVERY Slack sender to the  | Fast Follow | KEEP | Arch comment 2026-10-01 gives build shape, live bug |
| 1487 | renderInboundStatus lives inside a Jinja template — the bran | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1494 | ADR-059 blanket skip on test_portfolio_service.py also disab | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1497 | Slack settings page is three generations of config stacked w | Fast Follow | KEEP | Moved to Fast Follow 2026-08-27, Slack descoped per open 1440 |
| 1500 | Slack DMs with file attachments (and edits) are silently ign | Fast Follow | KEEP | Moved to Fast Follow 2026-08-27, Slack descoped per open 1440 |
| 1503 | No API path to clear or rotate slack_app_token (overwrite-on | Fast Follow | KEEP | Moved to Fast Follow 2026-08-27, Slack descoped per open 1440 |
| 1561 | ProjectQueryService by-id reads remain owner-unscoped + Proj | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1619 | Registry: four mutations filed under the read-only QUERY cat | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1634 | User-facing data-retention settings (Enterprise) — PM ratifi | Enterprise | KEEP | Open in live Enterprise milestone, scope still stated and no superseding issue found |
| 1673 | AUDIT: held-state parity — equip Piper (the agent) with the  | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 1686 | Slack users.info.tz capture — deferred half of #1572, sequen | Fast Follow | KEEP | Open in live Fast Follow milestone, scope still stated and no superseding issue found |
| 1834 | Governance: mechanical check for 'people'/'person' used to d | Ongoing | KEEP | Build-item 1 done, build-item 2 (internal reports) still open per comment |
| 1847 | docs: pattern frontmatter status field needs real fix, not j | Ongoing | KEEP | Open, 15 of 74 patterns carry status Unknown per body |
| 1854 | [TESTS/LLM] Live canonical accuracy under bar — identity 92% | Production | KEEP | Open in live Production milestone, scope still stated and no superseding issue found |
| 65 | FEAT-VISION: Visual Content Analysis Pipeline | Enterprise | ASK-OWNER | PPM: later comment notes an existing browser extension covers the UI annotation part |
| 87 | FEAT-GRAPH: Visual knowledge graph interface | Enterprise | ASK-OWNER | PPM: body is empty, no scope recorded |
| 244 | CONV-UX-SLACK: Interactive Slack Standup Features | Fast Follow | ASK-OWNER | CXO: Slack UX layer item from CONV track, Slack is now Fast Follow per 1440 |
| 272 | RESEARCH-TOKENS-THINKING: Investigate Thinking Token Optimiz | Fast Follow | ASK-OWNER | Arch: research issue from 2025, no owner activity since April |
| 309 | CONV-MCP-PROTO: DocumentAnalysisSkill Prototype | Fast Follow | ASK-OWNER | Arch: Skills MCP prototype from the 2025 CONV track, may be superseded by current Skills direction (unverified) |
| 310 | CONV-UX-QUICK: Settings & Startup Quick Wins | Fast Follow | ASK-OWNER | CXO: quick-win UX bundle from CONV track, some items may have shipped elsewhere (unverified) |
| 315 | CONV-MCP-LIBRARY: Core Skills Library Implementation | Fast Follow | ASK-OWNER | Arch: Skills MCP prototype from the 2025 CONV track, may be superseded by current Skills direction (unverified) |
| 327 | PROCESS-AI-ACCOUNTS: Create separate GitHub accounts for AI  | Fast Follow | ASK-OWNER | Arch: 2025 suggestion-driven items, no live trigger named |
| 329 | DATA-ANNOTAT: Implement database annotation system for chang | Fast Follow | ASK-OWNER | Arch: 2025 suggestion-driven items, no live trigger named |
| 330 | INTEG-EMAIL-MCP: Email integration via Gmail MCP adapter | Fast Follow | ASK-OWNER | Arch: 2025 suggestion-driven items, no live trigger named |
| 335 | # STYLE-PK-PREFIXED: Adopt Prefixed Primary Key Naming Conve | Fast Follow | ASK-OWNER | Arch: 2025 suggestion-driven items, no live trigger named |
| 337 | STYLE-TABLE-SINGULAR: Adopt Singular Table Naming Convention | Fast Follow | ASK-OWNER | Arch: 2025 suggestion-driven items, no live trigger named |
| 338 | INFRA-MIGRATION-ROLLBACK - Comprehensive Database Migration  | Fast Follow | ASK-OWNER | Lead: safety-critical rollback testing issue last touched April, confirm still wanted |
| 683 | MUX-WIRE-DOD: Update Definition of Done to require interface | Ongoing | ASK-OWNER | PPM: all 3 ACs checked, only a Lead operational-check recipe refinement remains |
| 1011 | ARCH-DESIGN: Slash-command dispatch precedence — post-MVP de | Production | ASK-OWNER | Arch: slash-command dispatch design decision with no recorded ruling |
| 1131 | CANONICAL-TODO-JUDGE-ARTIFACT: stateless judge flags honest  | Production | ASK-OWNER | Lead: audit task with no comments, unclear if done |
| 1139 | Audit task: which PremonitionService methods are dead vs use | Production | ASK-OWNER | Lead: audit task with no comments, unclear if done |
| 1224 | Pre-existing test failures (3 clusters: standup conversation | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1316 | RECONNECT residual cleanup: federated_search degrade + WS-1  | Dot Releases (Post-MVP) | ASK-OWNER | Lead: items 2 and 3 done, item 1 moot until federated_search is built, kept open on purpose |
| 1350 | [BUG] settings_projects.html missing tokens.css / toast.js / | Production | ASK-OWNER | Lead: current test asserts shell-owned toast.js and tokens.css, looks repaired, overlaps 1451 (read not run) |
| 1357 | test_github_api_connection.py's live 401s appear only in lar | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1371 | Test-collection fragility: ModuleNotFoundError for real pack | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1372 | tests/intent/contracts/: 42 pre-existing failures, Container | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1391 | Admin editing interface: resume pipermorgan.ai/admin for can | Ongoing | ASK-OWNER | Web: admin editing interface request, no progress recorded |
| 1437 | Stale integration test: test_get_default_project_query pins  | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1439 | Pre-existing: two llm_config_service tests read the machine' | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1444 | Stale test: test_canonical_query_engine_initialization asser | Fast Follow | ASK-OWNER | Lead: tests/features/test_issue_intelligence.py is not tracked in the worktree, confirm removal was intended |
| 1448 | Stale test: test_create_todo_extracts_text gets honest-degra | Fast Follow | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1451 | settings/projects template test fails: test_template_include | Production | ASK-OWNER | Lead: current test asserts nav_rail include via shell, looks repaired (read not run) |
| 1468 | Canonical judge calibration: STRICT bar has no ratified thre | Production | ASK-OWNER | CXO: judge calibration needs a ratified threshold |
| 1506 | tests/domain/test_file_reference_detection.py classification | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1528 | test_validate_openai_key_success hits the LIVE OpenAI API wi | Production | ASK-OWNER | Lead: July 2026 test-collection and fixture issue, current status unverified |
| 1531 | tests/security/test_cross_user_isolation.py has NO teardown  | Production | ASK-OWNER | Lead: comment says fold into 1385 if preferred, both open |
| 1629 | session_activity.owner_id model/DB drift (varchar vs declare | Ongoing | ASK-OWNER | Lead: sweep and CAST audit done, fix-direction checkbox for session_activity drift unverified |
| 1680 | Dashboard Criterion E: consequential-action TranscriptEntry  | Ongoing | ASK-OWNER | CIO: Lead noted TranscriptEntry does not exist in the codebase, spec premise needs a decision |
| 1683 | editorial-calendar.csv: 145 rows genuinely syndicated but st | Ongoing | ASK-OWNER | Docs/Comms: 145-row backfill scope, only one residual row resolved by ruling, rest unverified |
| 1710 | Pattern-catalog Status field vocabulary contamination — stan | Ongoing | ASK-OWNER | Docs/CIO: comment asks whether to close as superseded by 1847 or keep both, 1847 is open |
| 1841 | [TESTS] pm039 live-LLM param 'show me all project plans' con | Production | ASK-OWNER | Lead: Arch ruling deposited a corpus row 2026-09-23, unclear whether any work remains |

## Summary
- Total reviewed: 114 of 114
- CLOSE: 4 of 114
- KEEP: 72 of 114
- ASK-OWNER: 38 of 114
- Icebox milestone: 0 of the 114 are in Icebox (8 of the 362 open issues are in Icebox, all updated since 2026-10-03). Milestones among the 114: Fast Follow 44, Production 40, Enterprise 14, Ongoing 9, Dot Releases 7.
- KEEP rows are a default for items in live milestones with no concrete evidence of completion. Reasons for those rows were not individually verified beyond reading the issue text.
- No outside person is named. Several 2025 issues credit an outside advisor as source, referred to here only as outside suggestion.
