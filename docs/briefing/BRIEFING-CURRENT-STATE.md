# BRIEFING-CURRENT-STATE.md - Where We Are Right Now

> **For current system state** (intent categories, plugins, patterns, architecture):
> **Use Serena symbolic queries instead of reading this file.**
> See `CLAUDE.md` "Live System State" section for query patterns.
> **This file focuses on sprint/epic position and methodology context.**

---

## STATUS BANNER

**Current Position**: 4.4.2 - M1 Sprint Active (Foundation) — Gate Re-Test Phase
**Version**: v0.8.6 (pyproject.toml source of truth)
**Last Updated**: April 7, 2026
**Current Focus**: M1 gate re-test — UAT round 1 failed Apr 3 (0/7 Gate 1), all 5 findings fixed Apr 4-5, ready for re-test
**Next Phase**: M1 gate re-test → M1 closure → M2 (MVP Activation)

---

## Inchworm Position

```
1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.4)
4. 🎯 Complete build of MVP
   4.1. ✅ B1 - Beta Enablers (v0.8.3.1, v0.8.3.2) - COMPLETE Jan 11
   4.2. ✅ A20 - Alpha Testing round 2 (v0.8.4.x) - COMPLETE Jan 18
   4.3. ✅ MUX: Modeled User Experience - COMPLETE Jan 27
   4.4. 🎯 MVP: Minimum Valuable Product (M0-M6) ← CURRENT
        ✅ M0: Conversational Glue — COMPLETE (v0.8.6, shipped Mar 4)
        🎯 M1: Foundation — GATE VERIFICATION (all issues closed, Gates 3-4 verified)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Recent Progress

### Apr 3-7 (M1 Gate UAT Round 1 + Remediation)
- **Apr 3**: **M1 Gate UAT Round 1 — NOT PASSED.** PM + CXO ran 7 of 9 Gate 1 queries and 1 of 5 Gate 2 scenarios on fresh account. 0/7 passed Colleague Test (4 auto-fails). 5 findings documented: (1) floor LLM not reaching user — hardcoded Anthropic provider failing silently, (2) canned template masks all failures, (3) handler pre-flight checks missing, (4) todo completion broken (Pattern-045: 23 tests pass, user can't complete), (5) input parsing too rigid. 2 issues filed: #939 (avatar cosmetic), #940 (LLM config blocker).
- **Apr 4**: **Lead Dev resolves #940 (M1 blocker).** Removed hardcoded provider assignments, introduced provider-agnostic `model_tier` system with `resolve_model()`. Setup UI redesigned: provider dropdown + single key input. Conversational floor now classifies LLM errors (auth/transient/no-provider). 6,303 tests passing. Inbox cleared (5 items). 3 stale branches deleted. Docs published "Silent Failures" insight. PA drafted Piper Open briefing docs for OpenLaws.us sibling project.
- **Apr 5**: **Lead Dev completes ALL 5 UAT findings** in 22 minutes. Todo parsing: regex now accepts articles ("Add a todo"). Completion text extraction fixed. #939 avatar: orphaned container fix. #943 pre-flight checks: GitHub config validation before API calls. **M1 gate ready for re-test.** Docs published "The Mismatch Category." Agent activity rollup produced (Mar 20–Apr 5: 77 sessions, 12 roles). PA ran dev/active cleanup (24→16).
- **Apr 6**: Rest day. No sessions.
- **Apr 7**: Docs catch-up (omnibus logs Apr 4-6, audit #944). PA orientation. Lead Dev + CXO re-test planned.

### Mar 29–Apr 2 (Infrastructure Migration + PA Operational + Publishing Pipeline)
- **Mar 29**: Docs blog infrastructure (269→275 posts, dedup fix, Medium demoted).
- **Mar 30**: **HIGH-COMPLEXITY day** (18 sessions, 12 roles). All agents migrated to new account (xian@designinproduct.com on faoilean). PA first-ever operational session. Blog: 5-era model, 275 posts fully self-hosted. #937 audit closed. Ship #036 drafted.
- **Mar 31**: Docs triage (50→7 files), CXO briefing refreshed, CIO methodology innovations doc, mail delivery, blog publish "Are We Doing It Backwards?", branch check hook installed.
- **Apr 1**: PA Day 3 — CLAUDE.md identity fix (hardcoded Lead Dev → role routing table). CIO endorsed RFC-001 with 3 amendments. Docs built Shipping News section on pipermorgan.ai (orange visual identity, /shipping-news route). Ship #036 published. Quarterly maintenance template updated (#938).
- **Apr 2**: PA backlog audit (119 issues, 89 in MVP milestone). Roadmap refresh prep drafted. Docs published "The Floor That Wasn't", HOST rename completed, #938: 12/15 items done. Session cut short by usage limit.

### Mar 24-28 (M1 Gate Verification + First Blog-Canonical Publish)
- **Mar 24**: **4-agent EXECUTION day**. Lead Dev closes #706 (Objects & Views Discovery — 3 formal deliverables) and verifies Gates 3+4. Gate 3: 4/5 architectural integrity criteria pass (G3.5 deferred to #927/#929). Gate 4: 6,310 tests passing, 0 failures. #375 folded into #926 Gate 1. Comms identifies 6-act blog narrative arc (Mar 13-22) from 10 omnibus logs, drafts Acts 1-2. CXO formalizes product header response (Option A, visible header). Docs: TODO triage (107 analyzed, 5 issues filed #932-#936, #746 reopened), Dispatch retro eval approved.
- **Mar 25**: Day off (PM at day job).
- **Mar 26**: Brief Docs session — 26 untracked files committed, CXO header response routed, Mar 24 omnibus synthesized. Session cut short by Anthropic service disruption.
- **Mar 27**: Day off (service disruptions).
- **Mar 28**: **Recovery + milestone day**. PPM confirms all 5 #717 decisions final (Lead Dev fully unblocked). CIO completes PA (Piper Alpha) Phase 0 — briefing v0.2 + onboarding prompt ready for launch. Docs recovers 4-day gap (omnibus logs, session logs, mail, stash recovery). **First blog-canonical publish**: "Discovery is the Bottleneck" published to pipermorgan.ai → Medium → LinkedIn. Editorial calendar: 15 entries updated/added, altText/caption columns added. 12 new content pieces in pipeline (5 narratives, 7 insights).

### Mar 22-23 (M1 Tier 3 Complete + Product Concept)
- **Mar 22**: **M1 Tier 3 complete** — 4 capability issues closed in single Lead Dev session (#902 GitHub close/reopen, #903 reminders, #904 todo completion, #883 lazy workflow deferral). 76 new tests, 1325 total passing. Gate #926 filed. CXO + PPM independently reviewed gate criteria (fresh-account testing, Colleague Test rubric, 9 smoke queries). E2E + AAXT testing proposal written, 4 issues filed (#927-#930). **PDR-004 Experience Philosophy** ratified. Docs: agent-log CSV migration (877 sessions indexed), Ship process guide v1.1, publishing workflow one-pager.
- **Mar 23**: **#717 Product concept closed** — 4-role coordination chain (Architect validates schema, CXO recommends nav Option B, PPM revises to both-models approach, Lead consolidates and writes product-concept-model.md). Weekly docs audit: NAVIGATION.md refreshed, 5 indexes corrected, 2 broken links fixed. dev/active/ cleaned (deliverables filed to docs/).

### Mar 17-21 (Documentation + Automation)
- **Mar 17**: Briefing architecture repaired (8/12 files fixed — root cause: hardcoded counts instead of CURRENT-STATE refs). Publish-to-blog skill battle-tested (v0.2). Medium repatriation completed: 268/268 posts (100%) local. #922 conversation continuity bug filed.
- **Mar 18**: dev/active/ sort completed (80→12 files). Blog image matching: 134/168 posts matched (87% coverage). Memo delivery (7 memos + CIO questionnaire to 8 inboxes).
- **Mar 19**: **All 9 agent roles active** (first time). ADR-059 (Workflow Dispatcher) drafted, reviewed, approved, and implemented in one morning. ADR-060 (Floor-First Routing) created. Mailbox v3 built and validated same-day. Agent 360 questionnaire: 9/9 response rate. Blog pipeline: 269/269 posts with imageSlug (100%).
- **Mar 20**: 3 parallel sessions. Lead Dev M1 capability audits (#923 filed + closed, #924 filed + closed). Docs created `/create-omnibus` skill. Blog image localization: 175/269 (65%) — CDN rate-limited at 22 requests.
- **Mar 21**: Omnibus automation pilot (Dispatch v3→v4 eval loop). Retro omnibus eval completed (5 historical dates). Blog images: 269/269 localized (100%, 0 CDN). CoS proposals 2 & 3 applied.

### Mar 12-16 (M1 Sprint Execution)
- **Mar 12**: M1 kickoff. #884 canonical retest: impl pass rate 53.7%→81.1% via wiring fixes alone. Klatch AX testing piloted (ETA role). Chief of Staff chat retired (34 days).
- **Mar 13**: **Highest-activity day** — 12 sessions, 10 roles. Workflow hijack design sprint (CXO→PPM→Architect→impl in one day). #888/#889 closed. #886 contextual fallbacks. Lead Dev: 7 issues closed, 80+ new tests.
- **Mar 14**: "Are we doing it backwards?" roundtable. 4 leadership roles independently converged on identical diagnosis (layer inversion). LLM floor implemented same-day. E2E test infrastructure created (#352). Todo completion lifecycle (#904).
- **Mar 15**: Floor inversion investigation — PM testing revealed handlers catch messages before floor. Phase 1 GUIDANCE routing implemented. Comms 2-month chat retired. CIO methodology audit (10 recommendations).
- **Mar 16**: "Extend without verifying" systemic pattern discovered via PM QA. Action Registry (34 pairs) created. Leadership floor synthesis cycle. Editorial calendar unified (304 rows). 9 issues closed.

### Mar 10-11 (M1 Planning)
- **Mar 10**: M0 retrospective (7→27 issues, 3.9x expansion). M1 scope refined: #557 WebSocket deferred M2, #482 KMS deferred M2. Spec pipeline formalized.
- **Mar 11**: M1 sequenced into 4 phases. #715 promoted to M1. 4 issues created (#883-#886).

### Mar 3-9 (Post-M0 Consolidation)
- **Mar 4**: M0 gate #779 + GLUE epic #762 closed. v0.8.6 released (56-commit merge)
- **Mar 5-7**: Recovery period
- **Mar 8-9**: Ship #033, GitHub wiki (14 pages), dev/active/ cleaned

---

## SYSTEM CAPABILITY

> **Use Serena for live state**: `mcp__serena__find_symbol`, `mcp__serena__list_dir`

### Current Capabilities (March 2026)

**Intent Classification**: 19 categories
```python
# From services/shared_types.py IntentCategory enum
EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING,
QUERY, CONVERSATION, IDENTITY, DISCOVERY, TEMPORAL, STATUS, PRIORITY,
GUIDANCE, TRUST, MEMORY, PORTFOLIO, UNKNOWN
```

**Active Integrations**: 7 plugins
- Slack (OAuth from Settings)
- GitHub (PAT configuration)
- Notion (API key in setup wizard)
- Google Calendar (OAuth from Settings)
- MCP (Model Context Protocol)
- Spatial (spatial intelligence)
- Demo (reference implementation)

**Architecture (M1 changes)**:
- **Floor-First Routing** (ADR-060): LLM conversational floor is default; canonical handlers handle actions. "Piper is always at least as good as a well-prompted LLM with context."
- **Workflow Dispatcher** (ADR-059): Registry-based dispatch replaces 3 competing offer/acceptance systems. Onboarding disabled (Gall's Law).
- **Action Registry**: 34 (category, action) pairs cataloged with `ActionDisposition` enum (CANONICAL, FLOOR, HANDLER, WORKFLOW)

**Pattern Catalog**: 63 patterns (001-062) across 8 families
- Completion Theater (045-049) - quality discipline
- Investigation & Root Cause (006, 041-043, 060) - debugging methodology
- Grammar Application (050-058) - consciousness, ownership, warmth
- Multi-Agent Coordination (029, 059, 010, 021, 037) - orchestration
- Core Architecture, Data & Query, AI & Intelligence, Integration & Platform

**ADRs**: 63 architectural decision records (ADR-059 through ADR-060 newest, plus adr-039 appendix removed)

**Skills**: 12 skills
- create-session-log, check-mailbox, close-issue-properly, audit-cascade, discovered-work-capture
- create-omnibus, deliver-mail, publish-to-blog (v0.5), narrative-verification
- update-calendar (new Apr 1), cleanup-dev-active (new Mar 30)

---

## What's Next: M1 Completion → M2

### M1 — GATE VERIFICATION PHASE

**All M1 issues closed.** Gates 3-4 verified. Gates 1-2 await PM manual testing.

**M1 Tier Status**:
- **Tier 1** (Architecture): ✅ Complete
- **Tier 2** (Quality): ✅ Complete
- **Tier 3** (Capabilities): ✅ Complete
- **Tier 4** (PM-led): ✅ Complete (#706 closed Mar 24, #375 folded into #926 Gate 1, #717 closed Mar 23)

**Gate Status**:
- **Gate 1** (Conversation Quality): ❌ FAILED Apr 3 (0/7 passed) → fixes applied Apr 4-5 → 🔲 RE-TEST PENDING
- **Gate 2** (Task Lifecycle): ❌ FAILED Apr 3 (1/5 attempted, todo completion broken) → fixes applied Apr 5 → 🔲 RE-TEST PENDING
- **Gate 3** (Architectural Integrity): ✅ 4/5 verified Mar 24 (G3.5 deferred to #927/#929)
- **Gate 4** (Bug Debt + Test Health): ✅ 3/3 verified (6,303 tests passing after Apr 5 fixes)

**UAT Round 1 Findings (all resolved)**:
| Finding | Severity | Fix | Commit |
|---------|----------|-----|--------|
| 1. Floor LLM not reaching user | BLOCKING | Provider-agnostic config (#940) | c2bdb772 |
| 2. Canned template masks failures | BLOCKING | Differentiated error messages | c2bdb772 |
| 3. Handler pre-flight checks | MODERATE | GitHub config check (#943) | d2ef354f |
| 4. Todo completion broken | BLOCKING | Completion text extraction fix | ff895d75 |
| 5. Input parsing too rigid | MODERATE | Accept articles in regex | ff895d75 |

**Remaining for M1 closure** (1 session):
- #926 Sprint Completion Gate — PM + CXO re-test (14 scenarios, all fixes applied)

**Other open issues** (not M1-gated):
- #925 Floor inversion Phase 3-4 (STATUS/PRIORITY floor-first)
- #921 Framework upgrade (FastAPI/Starlette/httpx)
- #927-#930 E2E + AAXT testing track (filed Mar 22)
- #932-#936 Security + infrastructure (from TODO triage Mar 24)
- #939 Avatar positioning (cosmetic, fixed)
- #940 LLM config (FIXED Apr 4)
- #942 Pre-existing workflows table test failure
- #943 Handler pre-flight checks (FIXED Apr 5)
- #944 Weekly docs audit (Apr 7)
- #945 todo_management.py TODO triage

### MVP Milestones Overview

| Milestone | Focus | Status |
|-----------|-------|--------|
| M0 | Conversational Glue | ✅ COMPLETE (v0.8.6) |
| M1 | MVP Foundation | ~98% (all issues closed, Gates 1-2 manual testing remains) |
| M2 | MVP Activation | 4% |
| M3-M6 | Advanced Features | Backlog |
| DIST | Distribution | 0% (after M6) |

---

## Open Items by Priority

### Ready for Action
- #926 M1 Sprint Completion Gate — **RE-TEST** (all 5 findings fixed, PM + CXO re-test)
- #925 Floor inversion Phase 3-4

### Planning/Strategy
- **Piper Alpha (PA)**: Day 8, fully operational. Backlog audit complete (119 issues). Roadmap refresh prep awaiting PM review.
- **Piper Open (PO)**: Briefing docs drafted for OpenLaws.us sibling project (Apr 4). Lighter process, no research mandate.
- **Publishing workflow**: Blog-first pipeline smooth (6 posts published Mar 28–Apr 5). Shipping News section live. 23 unpublished drafts indexed. 8 posts scheduled through Apr 19.
- IA Conference talk (April 17, Philadelphia) — 16-slide deck drafted
- E2E + AAXT testing: 4 issues filed (#927-#930), proposal written
- Content pipeline: 3 building narrative acts (Apr 8, 10, 15) + 5 insights scheduled (Apr 5-19)

### Deferred
- #557 WebSocket (deferred to M2 per Architect)
- #482 KMS (deferred to M2)
- Mobile PoC (paused)
- DIST epic (#828 and children — after M6)

---

## Metrics Snapshot (April 7, 2026)

### Quality
- **Pattern Count**: 63 (001-062)
- **ADR Count**: 63 (through ADR-060)
- **PDR Count**: 6 (001-004, 101)
- **Methodology Count**: 23 (00-22) + M1-INNOVATIONS doc
- **Skill Count**: 12
- **Test Suite**: 6,303 passing (after Apr 4-5 fixes)
- **Omnibus Logs**: Through Apr 6 (continuous daily coverage)
- **Agent Sessions**: 77 sessions Mar 20–Apr 5 across 12 roles
- **Blog Posts**: 280 (6 blog-first canonical publishes since Mar 28)
- **Documentation Files**: 1,237 .md files
- **Python LOC**: ~419K

### Infrastructure (current)
- **Mailbox v3**: 11-role infrastructure (HOST renamed from HOSR Apr 2)
- **Blog Pipeline**: 280 posts, `/publish-to-blog` skill v0.5, draft metadata convention (comment blocks)
- **Shipping News**: Dedicated section at pipermorgan.ai/shipping-news (Apr 1), orange visual identity
- **Editorial Calendar**: 320+ entries, 8 posts scheduled through Apr 19
- **PA (Piper Alpha)**: Day 8, fully operational. Backlog audit, roadmap prep, daily reports to Dispatch.
- **Piper Open**: Briefing docs drafted for OpenLaws.us (Apr 4)

### Version History (Recent)
| Version | Date | Milestone |
|---------|------|-----------|
| v0.8.6 | Mar 4, 2026 | M0 Conversational Glue, 27 issues |
| v0.8.5.3 | Feb 11, 2026 | Windows compat, setup UX, 14 issues |
| v0.8.5.2 | Feb 6, 2026 | Alpha bug fixes, timezone alignment |
| v0.8.5.1 | Feb 1, 2026 | Timezone cascade fixes |
| v0.8.5 | Jan 27, 2026 | MUX-IMPLEMENT complete |

---

## Alpha Testing Focus

### What's Stable
- Setup wizard (GUI and CLI)
- Login/authentication
- Chat interface with 19 intent categories
- Conversational floor (LLM with assembled context for unmatched queries)
- Lists, todos, projects, files CRUD
- Integration Settings (Slack, Calendar, GitHub, Notion)
- Trust-appropriate proactivity
- Workflow escape commands and timeout

### What Changed (M1)
- Floor-first routing: unmatched queries get LLM conversational response instead of "I can't do that"
- Onboarding wizard disabled (Gall's Law — was hijacking sessions)
- Contextual fallback messages for unimplemented capabilities
- Action Registry gates which intents trigger handlers vs floor

### Known Issues
- #925 STATUS/PRIORITY still routed to canonical handlers instead of floor (Phase 3-4)
- #927-#930 E2E + AAXT testing track (filed, not yet started)

---

## Key Documents

**Roadmap**: `docs/internal/planning/roadmap/roadmap.md` (v14.3)
**Patterns**: `docs/internal/architecture/current/patterns/` (63 patterns)
**ADRs**: `docs/internal/architecture/current/adrs/` (63 ADRs, newest: ADR-059, ADR-060)
**PDRs**: `docs/internal/product/pdr/` (6 PDRs, newest: PDR-004 Experience Philosophy)
**Skills**: `.claude/skills/` (9 skills)
**Omnibus Logs**: `docs/omnibus-logs/` (continuous through Mar 28)
**Mailbox Directory**: `mailboxes/DIRECTORY.md`
**Publishing Workflow**: `docs/internal/planning/comms/publishing-workflow-target.md`
**Wiki**: `https://github.com/mediajunkie/piper-morgan-product/wiki`
**CITATIONS**: `docs/references/CITATIONS.md` (updated Mar 3)
**Glossary**: `knowledge/piper-morgan-glossary-v1.1.md`

---

*Last Updated: April 7, 2026*
*Source: Omnibus logs Mar 10–Apr 6, GitHub issue list, session logs, weekly audit #944*
