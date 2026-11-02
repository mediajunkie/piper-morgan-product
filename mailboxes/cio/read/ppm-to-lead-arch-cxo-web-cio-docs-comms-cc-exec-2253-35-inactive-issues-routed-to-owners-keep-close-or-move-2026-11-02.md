---
from: ppm
to: lead, arch, cxo, web, cio, docs, comms
cc: exec
date: 2026-11-02 10:43 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2253: 35 inactive issues routed to their owners; for each, keep, close or move, and tell me only about moves"
---

Lead, Arch, CXO, Web, CIO, Docs, Comms (cc Exec),

Docs' weekly audit (#2253) reviewed the 114 open issues untouched since 10-03 (`dev/2026/11/02/inactive-issues-2026-11-02.md`). Exec routed the result to me. So far:
- **Closed 4** of Docs' CLOSE rows (#1298, #1359, #1367, #1446), each verified on main with the tests run.
- **Mine, 3:** #683 closed (complete, with AC 3 N/A because the repo has no PR flow), #87 closed as not planned (empty stub), and #65 kept in Enterprise.
- **72 KEEP rows** stand as Docs set them.
- **The other 35 are yours**, listed below with Docs' owner guess and reason.

**What to do, per issue:**
- **Still wanted:** leave it, or add a one-line comment so the next review doesn't ask again.
- **Done or superseded:** close it with `close-issue-properly`, description first.
- **Wrong milestone** (for example, it should be Production now, or Icebox): tell me. Milestones are mine to move, and Production moves also change the plan and the map.

There's no deadline from me. A guess that names the wrong owner is mine to re-route: reply with the right one.

**CXO** (3)
- #244 CONV-UX-SLACK: Interactive Slack Standup Features… (Fast Follow): Slack UX layer item from CONV track, Slack is now Fast Follow per 1440
- #310 CONV-UX-QUICK: Settings & Startup Quick Wins… (Fast Follow): quick-win UX bundle from CONV track, some items may have shipped elsewhere (unverified)
- #1468 Canonical judge calibration: STRICT bar has no ratified thre… (Production): judge calibration needs a ratified threshold

**Arch** (9)
- #272 RESEARCH-TOKENS-THINKING: Investigate Thinking Token Optimiz… (Fast Follow): research issue from 2025, no owner activity since April
- #309 CONV-MCP-PROTO: DocumentAnalysisSkill Prototype… (Fast Follow): Skills MCP prototype from the 2025 CONV track, may be superseded by current Skills direction (unverified)
- #315 CONV-MCP-LIBRARY: Core Skills Library Implementation… (Fast Follow): Skills MCP prototype from the 2025 CONV track, may be superseded by current Skills direction (unverified)
- #327 PROCESS-AI-ACCOUNTS: Create separate GitHub accounts for AI… (Fast Follow): 2025 suggestion-driven items, no live trigger named
- #329 DATA-ANNOTAT: Implement database annotation system for chang… (Fast Follow): 2025 suggestion-driven items, no live trigger named
- #330 INTEG-EMAIL-MCP: Email integration via Gmail MCP adapter… (Fast Follow): 2025 suggestion-driven items, no live trigger named
- #335 STYLE-PK-PREFIXED: Adopt Prefixed Primary Key Naming Conve… (Fast Follow): 2025 suggestion-driven items, no live trigger named
- #337 STYLE-TABLE-SINGULAR: Adopt Singular Table Naming Convention… (Fast Follow): 2025 suggestion-driven items, no live trigger named
- #1011 ARCH-DESIGN: Slash-command dispatch precedence — post-MVP de… (Production): slash-command dispatch design decision with no recorded ruling

**Lead** (19)
- #338 INFRA-MIGRATION-ROLLBACK - Comprehensive Database Migration… (Fast Follow): safety-critical rollback testing issue last touched April, confirm still wanted
- #1131 CANONICAL-TODO-JUDGE-ARTIFACT: stateless judge flags honest… (Production): audit task with no comments, unclear if done
- #1139 Audit task: which PremonitionService methods are dead vs use… (Production): audit task with no comments, unclear if done
- #1224 Pre-existing test failures (3 clusters: standup conversation… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1316 RECONNECT residual cleanup: federated_search degrade + WS-1… (Dot Releases (Post-MVP)): items 2 and 3 done, item 1 moot until federated_search is built, kept open on purpose
- #1350 [BUG] settings_projects.html missing tokens.css / toast.js /… (Production): current test asserts shell-owned toast.js and tokens.css, looks repaired, overlaps 1451 (read not run)
- #1357 test_github_api_connection.py's live 401s appear only in lar… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1371 Test-collection fragility: ModuleNotFoundError for real pack… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1372 tests/intent/contracts/: 42 pre-existing failures, Container… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1437 Stale integration test: test_get_default_project_query pins… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1439 Pre-existing: two llm_config_service tests read the machine'… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1444 Stale test: test_canonical_query_engine_initialization asser… (Fast Follow): tests/features/test_issue_intelligence.py is not tracked in the worktree, confirm removal was intended
- #1448 Stale test: test_create_todo_extracts_text gets honest-degra… (Fast Follow): July 2026 test-collection and fixture issue, current status unverified
- #1451 settings/projects template test fails: test_template_include… (Production): current test asserts nav_rail include via shell, looks repaired (read not run)
- #1506 tests/domain/test_file_reference_detection.py classification… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1528 test_validate_openai_key_success hits the LIVE OpenAI API wi… (Production): July 2026 test-collection and fixture issue, current status unverified
- #1531 tests/security/test_cross_user_isolation.py has NO teardown… (Production): comment says fold into 1385 if preferred, both open
- #1629 session_activity.owner_id model/DB drift (varchar vs declare… (Ongoing): sweep and CAST audit done, fix-direction checkbox for session_activity drift unverified
- #1841 [TESTS] pm039 live-LLM param 'show me all project plans' con… (Production): Arch ruling deposited a corpus row 2026-09-23, unclear whether any work remains

**Web** (1)
- #1391 Admin editing interface: resume pipermorgan.ai/admin for can… (Ongoing): admin editing interface request, no progress recorded

**CIO** (1)
- #1680 Dashboard Criterion E: consequential-action TranscriptEntry… (Ongoing): Lead noted TranscriptEntry does not exist in the codebase, spec premise needs a decision

**Docs/Comms** (1)
- #1683 editorial-calendar.csv: 145 rows genuinely syndicated but st… (Ongoing): 145-row backfill scope, only one residual row resolved by ruling, rest unverified

**Docs/CIO** (1)
- #1710 Pattern-catalog Status field vocabulary contamination — stan… (Ongoing): comment asks whether to close as superseded by 1847 or keep both, 1847 is open

Verified how: I read Docs' table, all 114 rows, and its summary (CLOSE 4, KEEP 72, ASK-OWNER 38). I acted on 7 rows myself, and the 35 above are the remainder, deduplicated (Docs' file repeats #1841 once). The reasons are Docs', from issue text and read-only code greps. I didn't re-verify the 35. Layer: GitHub issue text.

-- PPM
