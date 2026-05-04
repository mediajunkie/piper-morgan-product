# BRIEFING-CURRENT-STATE.md - Where We Are Right Now

> **For current system state** (intent categories, plugins, patterns, architecture):
> **Use Serena symbolic queries instead of reading this file.**
> See `CLAUDE.md` "Live System State" section for query patterns.
> **This file focuses on sprint/epic position and methodology context.**

---

## STATUS BANNER

**Current Position**: 4.4.3 — **M2 Sprint Active** (M2a/b/c COMPLETE; #992 + Phase F SHIPPED; #1018 audit_transparency durability shipped; M2d in gameplan-prep)
**Version**: v0.8.6 (pyproject.toml source of truth)
**Last Updated**: May 4, 2026
**Current Focus**: **M2d gameplan + audit-cascade pass** (per CEO May 3 direction). M2d issue restructure complete May 2 — 4 new issues filed (#1030/#1031/#1032/#1033), 3 reframed (#707/#714/#703), #869 relocated to M2e. Conceptual-integrity gate added to M2d completion. **#1018 audit_transparency durability Phase 2 SHIPPED May 2** (commit `fc79de31`); cluster regressions #1006/#1007/#1008 closed together. **Phase F flag-flip MERGED Apr 30** (commit `deecc816`); #992 ETHICS-ACTIVATE closed completing the multi-step arc. **ADR-061 v1.0 RATIFIED** (CEO verbal approval May 4; Architect committed v1.0 Apr 30 with Lead Dev review fixes folded). Mid-week mini-shai-hulud IoC scan run (clean across 16 dimensions; security note filed). Calibration reframe accepted: alpha-catch-22 named (no users → no calibration possible); three-phase split (simulation harness → beta-traffic refinement → stable) folded into ADR-061 v1.0.
**Sprint Structure**: M2a (baseline, DONE) → M2b (testing + cleanup, DONE) → M2c (floor consciousness + voice, DONE; tail in flight) → M2d (MUX Lifecycle, gameplan-prep) → M2e (Integrations) → M2f (Security + Infrastructure)
**Key Docs**: Vision V2.3 (`docs/internal/planning/current/vision.md`), Roadmap v15.0 — note: canonical file `docs/internal/planning/roadmap/roadmap.md` still v14.3; restructured content at `dev/active/roadmap-restructure-proposal-2026-04-08.md` is operating canonical pending PPM update memo
**Migration State**: **All 7 leadership roles on Code** (HOST Apr 22, CIO + Comms Apr 23, CXO + PPM Apr 25, Architect Apr 26 AM, Exec Apr 26 PM). Migration arc complete.

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
        ✅ M1: Foundation — CLOSED Apr 11 (4/4 gates passed; #922 carried to M2)
        🎯 M2: Conscious Floor + Action Handlers ← ACTIVE (M2a/b/c DONE; M2d/e next)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## Recent Progress

### Apr 30 – May 2 (Phase F MERGED + #1018 Phase 2 SHIPPED + M2d restructure)
- **Apr 30**: **Phase F flag-flip MERGED to main** (commit `deecc816`); `ENABLE_ETHICS_ENFORCEMENT=true` live; **#992 ETHICS-ACTIVATE closed** completing the multi-step ethics-enforcement arc (Phases A→F). **#948 orphan-task fix** closed (post-cancellation hygiene baseline for scheduler jobs). **Mini-Shai-Hulud IoC scan** run across 16 dimensions (local repo + GitHub account); all clean — false-positive sweep, not a compromise. Security note filed at `dev/2026/04/30/security-note-mini-shai-hulud-ioc-scan-2026-04-30.md`. **Calibration alpha-catch-22 named** (no users in alpha → no calibration possible from within alpha); resolved via three-phase reframe: Phase A simulation harness (Gemma-generated traffic) → Phase B beta-traffic refinement → Phase C stable. Lead Dev memo to Architect + PPM; Architect folded reframe into ADR-061 v1.0 same day. **#1018 Phase 1 design ratified** by Architect (Q1 flat repository, Q2 per-call session_scope transaction-boundary, Q3 adaptive_boundaries deferred to #1019 Path C remove-not-retarget).
- **May 2**: **#1018 Phase 2 SHIPPED + cluster closed** (single merge `fc79de31` to main). 8 production files + 14 new unit tests + 8 existing tests rewritten. PostgreSQL-backed `ethics_audit_log` table replaces in-memory `audit_logs` list; `EthicsAuditRepository` (flat in `services/database/repositories.py`); `AsyncSessionFactory.session_scope()` per call isolates audit-write failures from request transaction; SecurityRedactor extended with phone patterns (3-3-4 + (NNN) NNN-NNNN); `EthicsAuditCleanupJob` with post-#948 cancellation hygiene; lifespan wiring via `EthicsAuditCleanupPhase`. **Cluster regression targets all closed**: #1006 datetime offset (TIMESTAMPTZ throughout), #1007 PII redaction (phone patterns added), #1008 await-on-list (test mock fixed; production code already correct). 17/17 audit-transparency tests pass on changed surface. **M2d audit-cascade run** against 4 issues (#703/#707/#714/#869) per CEO direction with MUX-flattening watch. Audit gate did NOT pass on first read; surfaced 3 conceptual-drift risks. Findings filed at `dev/2026/05/02/m2d-audit-cascade-findings.md`. **M2d restructure executed**: 4 new issues filed — **#1030 MUX-INSIGHT-PULL** (P2 MVP, all trust stages, user-initiated), **#1031 MUX-INSIGHT-PASSIVE** (P2 MVP, Insight Journal navigation), **#1032 MUX-INSIGHT-PUSH** (P3 MVP, Stage 3+ trust gate, longer-pole), **#1033 MUX-COMPOSTED-EXPERIENCE** (P2 MVP, sibling to #703, "filing dreams" framing). #707 reframed as tracking parent for the 3 children. #714 rewritten with staleness-spec-first scope and "Lists are non-lifecycle" decision folded. #703 cross-referenced to #1033. #869 relocated to M2e. `m2-structure.md` updated with new conceptual-integrity gate clause. **4 issues closed today** (#1018, #1006, #1007, #1008); **4 issues filed**; **3 issues reframed**.

### Apr 27–28 (#1004 SHIP + Phase F decision pending + Methodology-24/25 filed)
- **Apr 27**: **#1004 SHIPPED end-to-end in a single Lead Dev session** — Step 8 (probe set + calibration) and Step 9 (ship at v0.2 production) completed Monday. Phase C run-2 with prompt v0.2 + probe deltas hit 18/20 PASS, all CXO success criteria met. **112/112 PASS across the full ethics enforcement suite.** **#1002 and #1003 both closed** with full evidence per close-issue-properly skill. **Phase F flag-flip conditions all met per PPM v4** (Architect scoping ✓, #1002 + #1003 close ✓, flag-matters diagnostic ✓, probe set + two calibration rounds ✓). Lead Dev recommendation: defer flag-flip pending ADR-061 (Architect drafting); **decision now sits with PM/PA** (memo `2322907a`). **Methodology-24 (Branch-or-Anchor)** and **Methodology-25 (Workstream Review Cadence)** filed by CIO. **CT v2.3** embeds Branch-or-Anchor rule directly in rubric. **Pattern-063 (Parallel-Authoring Drift)** PM concurrence landed (PA memo `6d1c7062`). CIO filed audit B1–B6 Flywheel downstream sweep memo to Docs; audit S1 (canonical-term drift) + audit S3 (Klatch AAXT scaffolded probing); Lead Dev audit-A3 disposition: retire. PA scoping ask to Lead Dev re `merge-keeper-sweep.sh` + `deliver-mail (b)` — branch-discipline implementation continuing. HOST acknowledging 360-synthesis replies from PPM/CXO/Comms/CIO; CIO migration-experience confer resurrected. Chief of Staff completed OpenLaws Bet 1 Q5 + Q2 (CoS-vantage independent answer) per Janus relay convention.
- **Apr 28**: Cross-pollination brief: #1004 ships; MCP live. Klatch first live MCP stdio integration test (27/27 PASS via official TypeScript SDK over `StdioClientTransport`); same transport path Claude Code/Desktop would use. Round-trip gap findings scoped (3 gaps; transferable to PM Phase 3.5 / L5 portability design decisions already in flight).

### Apr 22–26 (Chat→Code Migration Wave + #992 Phase E + Publishing)

- **Apr 22**: HOST migrates Chat→Code (singleton). Migration checklist (4-phase) + 6-section handoff template + Agent 360 v0.2 baseline established. Apr 16 omnibus drift discovered + remediated. Step 2.5 Cross-Reference Gate added to create-omnibus skill. Session-start hook fixed (3 hardcoded Lead Dev assumptions removed). #998 Compose UI v1 plan ratified.
- **Apr 23**: **CIO + Comms both migrate** (pair). Lead Dev autonomous backlog triage closes #990, audits #997, posts #982 status. Compose UI Phase 1 (#998) ships (`6b129edd`). Gemma harness role settled: generator tier (routine offload — intent classification, slot filling, relevance, routing) NOT judge tier. PA Gap 2 sharpened (Gemma-family for secondary review pending Lead Dev viability check). Apr 22 omnibus shipped via Step 2.5 gate (first use catches real drift). #992 Phases A-D merged to main.
- **Apr 24**: Comms's first full Code day produces 6 narrative beats for May editorial calendar + 8 weekend insight pairs + voice/tone-guide misfile rescue + 2 insight drafts (Verify the Paraphrase, Six Issues Before Dinner). Exec batch-drafts 6 migration artifacts for Arch/PPM/CXO (bilateral-vs-triangular coordination distinction). Docs publishes The Gate (3-week-old stash conflict resolved mid-pipeline). Apr 23 + 24 omnibi shipped.
- **Apr 25**: **CXO + PPM both migrate** (dual). Lead Dev runs #992 Phase E on fresh port-8002 server (Path B); 3 scenarios captured. **Scenario 1 floor-bypass-by-pre-classifier finding**: pre-classifier matched "blocking my PRs" → `list_prs_query` handler before ethics floor evaluated. Filed as **#1002 P0** (Phase F flag-flip blocker pending Architect scoping). **#997 closed** via Option A (`b17c4aba`); follow-ups #999/#1000/#1001 filed. **Colleague Test v2.0** committed by CXO Code (reconstructed from handoff spec; predecessor's Apr 19 Chat draft never committed — Finding A added to migration Phase 1 checklist). **Multi-Wave Investigation** published (3 surfaces: blog, LinkedIn, Medium). PA autonomous 5-memo batch under PM "Go!" (90 minutes). Apr 22 omnibus deeper amendment + Apr 23 + 24 + 25 omnibi shipped (5 syntheses across the day).
- **Apr 26**: Scenario 1 r2 re-run (rephrased) — floor reached as GUIDANCE intent, not boundary trigger; new finding (audit-shape question for PPM/CXO scoring). PPM finding-response memo with 4 decisions; #1002 Architect scoping memo routed. CXO branch merged to main (`23f585f8`) with manifest conflict resolution. CXO briefing post-migration corrections applied (priority/path updates, Code-era environment, CXO↔Comms↔Docs triangle, operational disciplines covering ethics-decline voice / floor quality monitoring / verification-before-assertion / calibration through use). Branch-discipline review thread opened (CXO proposal to PA following PPM worktree-vs-main path-confusion incident). Architect + Exec migrations remaining.

### Apr 15–22 (M2 Completion + CIO Audit + Ship #039)
- **Apr 15**: M2b complete. Test suite stabilized at 6,242 after deletions brought count down from 6,309.
- **Apr 16**: **Highest-velocity day to date.** M2c complete. #950 Floor Prompt (Five Pillars + Grammar + anti-flattening) designed, drafted, approved, implemented, measured in a single day — quality 65.6% → 72.1%. #964 Ethics voice guidance delivered (CXO direction, BoundaryEnforcer activation pending FP validation). #971 executed per Architect (10 files deleted, llm_domain_service.py -160 lines). Ruff migration (#981). PDR-004 correction chain: CXO spotted "patience over performance" paraphrase error; Docs added canonical-term verification to omnibus skill; Comms flagged affected posts. 28 commits Lead Dev + 4-agent coordination chain. Apr 16 omnibus logged HIGH-COMPLEXITY: COORDINATION.
- **Apr 17**: IAC conference in Philadelphia — "Ethics as Information Architecture" delivered. CIO methodology audit delivered: 12 recommendations, 8 formulations of Excellence Flywheel across 9 months discovered, zero canonical document citations in 128 session logs.
- **Apr 18**: Docs published "Thirteen Mailboxes" (insight). publish-to-blog skill v0.7 (YAML frontmatter + heading convention).
- **Apr 19**: Docs published "Sibling Intelligence" (insight). Apr 16 omnibus synthesized. Session-log maintenance hook added (PostToolUse Bash reminder every 15 calls if log >30min stale). CLAUDE.md strengthened with "Session Log Maintenance (NON-NEGOTIABLE)" section.
- **Apr 20**: Rest day (PM at family visit).
- **Apr 21**: Docs published "Four Roles, Ninety Minutes" (narrative — #717 product concept via 4-role coordination chain). Weekly docs audit #996 run: 3 broken methodology-core links fixed in pattern-049, BRIEFING + roadmap flagged stale, 14 issues without milestone flagged, 86 services/ files with mock_/fallback flagged for sweep, patterns/README line-6 count inconsistency flagged.
- **Apr 22**: Session-start hook fixed (3 hardcoded Lead Dev assumptions removed — session log search, mailbox check, role identity). Weekly Ship #039 "The Voice Takes Shape" published to LinkedIn + blog. publish-to-blog skill v0.8 (explicit blog-content.json schema + preserve non-metadata HTML comments). Two website bugs filed: mediajunkie/piper-morgan-website#17 (dedup fails on prefix-extended Medium slugs — Archaeological Debugging duplicate), #18 (alt text dropped from medium-posts.json for blog-first posts, accessibility regression). Four Roles content schema fixed (bare string → dict). patterns/README.md count corrected (62 patterns + template, not 63). **Omnibus drift discovered + remediated**: Apr 16 omnibus was synthesized Apr 19 from incomplete source set (PPM/CIO/HOST 4/16 logs not downloaded, Arch 4/16 partial). Discovery triggered by Apr 17-21 catch-up walkthrough. Four missing/richer source logs integrated; Apr 16 omnibus amended (sessions 6 → 9, surfacing CIO Flywheel reformulation decisions + PPM pathological-tagging memo + HOST 12-role assessment). Apr 17/18/19/21 omnibus synthesized (Apr 20 dark-day). create-omnibus skill updated with source-log cross-reference gate (Step 2.5) to prevent recurrence. **Chat-to-Code migration decided** (Apr 21 Exec session): all Chat-based roles migrate to Code/Cowork starting today; sequence HOST + CIO first, then memo-writers, then CoS last with handoff.

### Apr 14 (M2 Sprint Acceleration — Lead Dev Ships Testing Track)
- **Lead Dev ships 6 issues in single session**: #960/#961 (context contract audit + UNKNOWN enrichment), #963 (911 lines dead code removed, 26 methods from canonical_handlers.py), #927 (E2E task lifecycle 9/9 pass), #928 (canonical conversation suite — 61 queries, two-tier), #929 (AAXT golden scenarios — 5 multi-turn tests), #930 (CI integration — GitHub Actions for all three test tiers). Entire M2b testing track complete.
- **M2 structure document** created at `docs/internal/planning/m2-structure.md` — all 6 sub-epics with gating criteria
- **PA**: 5 cross-pollination routing memos delivered. Managed Agents assessment written. MUX lifecycle issues revised (6 issues). #979 Haiku 3 retirement filed (Apr 19 deadline). Memory Stores API documented — path-based model maps to our file-based memory. Check-in cadence agreed.
- **Architect**: Session (log in dev/2026/04/14/)
- **Comms**: Session (log in dev/2026/04/14/)

### Apr 11-13 (M1 Closure + Vision V2.3 + Roadmap v15.0 + M2 Kickoff)
- **Apr 11**: **M1 GATE #926 CLOSED** at 7/9 PASS. Floor fabrication guardrail added ("NEVER fabricate user data unless in context"). Three M2 issues filed (#960-962). **Vision V2.3 adopted** — leadership review complete (PPM ✓ CXO ✓ CIO ✓ Architect ✓). **Roadmap v15.0 adopted** — M2-M5 restructured around differentiator stack. 3 new issues filed (#964, #966, #967). 2 issues closed with replacements (#312→#966, #241→#964). **Lead Dev M2 go-ahead memo** delivered. PA read all 6 leadership workstream reviews.
- **Apr 12**: M2 canonical retest baseline established (95.1% routing, 65.6% quality). **Janus memory research synthesis** (20+ systems, 6-dimension taxonomy). 5 memory architecture issues filed (#972-976). Dreaming concept provenance brief created by Docs.
- **Apr 13**: Lead Dev completes **floor inversion trilogy** (#925 STATUS/PRIORITY migration). Canonical retest run 3: 93.4% routing, 62.3% quality, stable. Docs 15-day session wrap. Comms session. #965 temporal floor migration.

### Apr 8-10 (Strategic Pivot + Sprint Planning)
- **Apr 8**: **Vision V2.2** — "Bring Your Own Chat" added. MCPB feasibility confirmed. Roadmap restructure proposal drafted (v14.3→v15.0). 3 CONV-FEAT decisions: #100→M2 context shape, #101→M2 context shape, #103→deferred Horizon 2. 10 new issues filed (#950-959). Leadership review memos sent to PPM, CXO, Architect.
- **Apr 9**: Dispatch comms gap identified (4 missed messages). Haiku 3 retirement verified (3 files need updates). Session log discipline memo relayed to PO via Dispatch. Check-in flow design produced.
- **Apr 10**: **HIGH-COMPLEXITY: COORDINATION** — 9 sessions, 8 roles. M1 UAT Round 4 (PM + Lead Dev + CXO). PA created 10 new issues. 6 leadership workstream reviews delivered. PPM + CXO + CIO + Architect all reviewed Vision V2.1 + roadmap restructure.

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

**Pattern Catalog**: 62 patterns (001-062) + template (000), across 8 families
- Completion Theater (045-049) - quality discipline
- Investigation & Root Cause (006, 041-043, 060) - debugging methodology
- Grammar Application (050-058) - consciousness, ownership, warmth
- Multi-Agent Coordination (029, 059, 010, 021, 037) - orchestration
- Core Architecture, Data & Query, AI & Intelligence, Integration & Platform

**ADRs**: 63 architectural decision records (ADR-059 through ADR-060 newest, plus adr-039 appendix removed)

**Skills**: 13+ skills
- create-session-log, check-mailbox, close-issue-properly, audit-cascade, discovered-work-capture
- create-omnibus, deliver-mail, publish-to-blog (v0.8 — Apr 22), narrative-verification
- update-calendar, cleanup-dev-active, update-current-state (new Apr 7)

---

## What's Next: M1 Completion → M2

### M1 — CLOSED (April 11, 2026)

**M1 closed after 4 UAT rounds (trajectory 0/9 → 0/9 → 5/9 → 7/9).** Gate 1 final: 7/9 passed, 1 marginal (memory tone), 1 known carry-forward (#922 affirmation handling, assigned to M2). All four gates passed. M1 ran 33 days (Mar 10 – Apr 11), expansion factor ~2x.

**Historical M1 gate record:**

**M1 Tier Status**:
- **Tier 1** (Architecture): ✅ Complete
- **Tier 2** (Quality): ✅ Complete
- **Tier 3** (Capabilities): ✅ Complete
- **Tier 4** (PM-led): ✅ Complete (#706 closed Mar 24, #375 folded into #926 Gate 1, #717 closed Mar 23)

**Gate Status** (all closed Apr 11):
- **Gate 1** (Conversation Quality): ✅ 7/9 PASSED Apr 10 (Round 4); #922 memory-tone carry-forward to M2
- **Gate 2** (Task Lifecycle): ✅ PASSED Apr 10 (Round 4)
- **Gate 3** (Architectural Integrity): ✅ 4/5 verified Mar 24 (G3.5 covered by #927/#929 completed Apr 14)
- **Gate 4** (Bug Debt + Test Health): ✅ 3/3 verified (test suite stabilized at 6,242 after Apr 15 cleanup)

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
| M1 | MVP Foundation | ✅ COMPLETE (Apr 11) |
| M2 | MVP Activation | M2a/b/c DONE; M2d in gameplan-prep; M2e/f to follow |
| M3-M6 | Advanced Features | Backlog |
| DIST | Distribution | 0% (after M6) |

---

## Open Items by Priority

### Pending PM Decision
- **ADR-061 v1.0 RATIFIED** — CEO verbal approval May 4. Architect committed v1.0 Apr 30 with Lead Dev review fixes folded + calibration reframe (alpha-catch-22 → three-phase split) integrated. ADR file status block update flagged to Architect.

### Ready for Action
- **M2d gameplans + audit-cascades** (per CEO May 3 direction): #703 (tracking + COMPOSTED cross-ref), #714 (staleness-spec-first reframe), #1030 PULL, #1031 PASSIVE, #1032 PUSH (longer-pole, phase-0 design), #1033 COMPOSTED-EXPERIENCE. Issue gate now passable post-restructure.
- **M2e gameplans** (after M2d): #790 Trust-gated calendar, #864 Pre-classifier patterns, #900 Standup 3-part, #869 Project config IA (relocated from M2d May 2).
- **PreCompact hook** (Docs Apr 29 go-ahead, task #86): backlog.
- **#925** Floor inversion Phase 3-4 (carried).
- **#922** affirmation handling (carried from M1 to M2).

### Planning/Strategy
- **Cross-project comms gap escalation** (tracker item 17): exec to escalate to Architect this week per predecessor handoff §6 force-decide.
- **Migration checklist v1.1**: HOST drafting per Apr 22 commitment; folds Phase 3 first-week findings.
- **Codification of handoff-review pattern**: methodology debt named in predecessor handoff §6; first-month task; six review memos as source material.
- **Branch-discipline aggregation → formal policy**: PA aggregating responses; PPM hosting synthesis-into-formal-policy step.
- **360 Round 2 cohort confer**: HOST acking syntheses; CIO migration-experience confer resurrected.

### Deferred
- #557 WebSocket (deferred to M2 per Architect)
- #482 KMS (deferred to M2)
- Mobile PoC (paused)
- DIST epic (#828 and children — after M6)

---

## Metrics Snapshot (May 4, 2026)

### Quality
- **Pattern Count**: 63 patterns (001-063, with Pattern-063 Parallel-Authoring Drift PM-ratified Apr 27) + template (000)
- **ADR Count**: 64 (through ADR-061, RATIFIED May 4)
- **PDR Count**: 6 (001-004, 101)
- **Methodology Count**: 26 (Methodology-24 Branch-or-Anchor + Methodology-25 Workstream Review Cadence filed Apr 27 by CIO)
- **Colleague Test rubric**: v2.3 (embeds Branch-or-Anchor rule directly in rubric, Apr 27)
- **Skill Count**: 13+
- **Test Suite**: 112/112 PASS across full ethics enforcement suite as of #1004 Apr 27 ship; broader project test count pending re-measure
- **Omnibus Logs**: continuous through Apr 26; Apr 27 + 28 pending in normal Docs cadence
- **Blog Posts**: ~292 + Apr 26 publish (Verify the Paraphrase) — full count pending re-measure
- **Documentation Files**: ~1,282 .md files (not re-measured this week)
- **Python LOC**: ~419K (not re-measured this week)

### Quality (retest baseline)
- Run 1 (Apr 11): routing 41%, quality 59% — first honest post-M1 baseline
- Run 2 (Apr 12): routing 95.1%, quality 65.6% — after #965 + #968 methodology fixes
- Run 3 (Apr 16): quality 72.1% — after #950 Five Pillars + grammar in floor prompt

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

**Roadmap**: `docs/internal/planning/roadmap/roadmap.md` (v15.0 adopted Apr 11; may need refresh — last git update Apr 11)
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

*Last Updated: May 4, 2026*
*Source: Lead Dev session logs 2026-04-30, 2026-05-02, 2026-05-03, recent commits `fc79de31` (#1018 Phase 2 + cluster #1006/#1007/#1008), `deecc816` (Phase F flag-flip), `d1c54dda` (M2d restructure), `0b88e932` (M2d audit-cascade findings), Architect ADR-061 v1.0 commit Apr 30, security note `dev/2026/04/30/security-note-mini-shai-hulud-ioc-scan-2026-04-30.md`, M2d audit findings `dev/2026/05/02/m2d-audit-cascade-findings.md`, m2-structure.md update May 2, xpoll brief May 3.*
