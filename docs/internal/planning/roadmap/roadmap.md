# Piper Morgan Roadmap v18.7

**Date**: July 16, 2026 (v18.7 fold: #1394 architecture COMPLETE + Production 1.0 connector gate defined + Finish-the-Unfinished sprint ratified — reconstructed by PPM after a ~22hr session gap during which PM made these calls in-conversation with Lead; body narrative otherwise per v18.6 July 12, 2026)
**Author**: PPM, with leadership review (PA — §M5/BYOC + skunkworks **ABSORBED v18**; CIO — §Methodology **ABSORBED v18 (6/3)**; CXO — §Differentiator stack EC framework; Architect — §Architectural commitments AC framework; Lead Dev — §M2g + Phase 2 build; Comms — external-language frame pending)
**Status**: Active. **PM-ratified June 3, 2026** (relay via PA). **v18.1 sprint-board fold June 15, 2026** (PPM). **v18.2 fold June 28, 2026** (PPM): RECONNECT WS-1 closed Jun 22 + WS-2 active; three M3-followon sprints (M3-Quality/Health/Security) added; beta moved Aug 1 + production Oct 30; ADRs 070/071/072 landed; entity-model spec delivered; #1237 CLOSED. v18.1 archived at `docs/internal/planning/historical/roadmap-v18.1-2026-06-15.md`. **v18.3 fold July 3, 2026** (PPM): RECONNECT WS-2 buildable scope DRAINED Jul 1; #1343 CLOSED (v0.8.9.1 Jul 2); #1344 PM-gated (HOST); M3-Quality is active cohort priority; #1331 floor confabulation hardening landed. **v18.4 fold July 4, 2026 (PPM)**: Beta Blockers sprint introduced (hard gates only; no theme; 12 confirmed gates); MVP milestone = beta gate — beta ships when MVP milestone is complete, not on a calendar date; Aug 1 target removed as unrealistic; RECONNECT connector status corrected (connectors work via PAT/keychain fallback, PM-verified; full ADR-070 migration is Production milestone work); milestone dates updated from GitHub (Fast Follow Nov 19 2026, Dot Releases Feb 2 2027, Enterprise Jul 4 2027). **v18.5 fold July 5, 2026 (PPM)**: full sprint-by-sprint backlog triage complete (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT — every open issue reviewed and dispositioned); GitHub-write-capability forensic investigation resolved (writes are real/wired, not unwired as first assumed; #1220's scope expanded to cover a real write-path credential gap); Beta Blockers sprint grew from 12→22 issues, now organized into 7 epics with recommended sequencing in the new canonical **[beta-blockers.md](../beta-blockers.md)** document; Aug 1 dropped entirely (not just marked TBD) — no fixed beta date until Lead Dev's bottom-up estimate against the stabilized 22-issue list. See `beta-blockers.md` (path-to-beta canonical) and sprint-order.md (full sprint sequencing). **v18.6 fold July 12, 2026 (PPM)**: the 8 PROD-* Production sprints referenced above were never actually documented as applied -- this fold closes that gap. They were created and 71 issues triaged into them July 5, 2026, in the *same PPM session* that triggered the project-wide Sprint-field wipe (the `updateProjectV2Field` full-replace mutation used to add the 8 new options detached all 1175 items' existing Sprint values -- full incident account in that session's log, `dev/2026/07/05/2026-07-05-0000-ppm-code-sonnet-log.md`). The wipe's recovery ran 2026-07-05 through 2026-07-12 (canonical record: `sprint-recovery-decisions-log.md`) and is now fully complete -- every issue that had a Sprint value before the wipe has one again. Separately, 20 more Production-milestone issues (created Jul 3-12, arrived after the big Jul 4-5 triage sweep) were triaged into the existing PROD-* structure this same fold: 10 -> PROD-TECHDEBT, 6 -> PROD-RECONNECT, 2 -> PROD-DESIGN, 1 -> PROD-INFRA, 1 -> PROD-TRUST. 2 more (#1358, #1374) were flagged as process/tooling work that likely belongs on the Ongoing milestone (FLYWHEEL sprint) rather than Production -- held for PM's call rather than force-fit.
**Supersedes**: v18.1 (June 15, 2026, archived); v17.0-draft (May 30, 2026, `00cee8d47`); v16.0 (May 10, 2026)
**v18.7 changelog** (July 16, 2026, PPM — reconstructing PM+Lead's in-conversation decisions from a ~22hr PPM session gap, Gap-C cron death): (jj) **#1394 architecture COMPLETE.** B4 (session-activity ledger) and B3 (referent resolution — "change the title" deterministically resolves the antecedent issue and emits `update_issue` directly, no classifier round-trip) both built and Arch-ratified. The cross-turn continuity gap open since Jul 12 is closed pending only a D5 live-behavioral-probe confirmation (gated to the next canonical-retest cycle, not beta-blocking). Along the way, #1411 and #1412 (the `update_issue`/`create_issue` elif-only dispatch reachability gaps Arch's B3 review surfaced) were both built and ratified same-window, closing the reachability-lint blind spot for the two live-write paths. (kk) **Production 1.0 GATE defined** (PM, in-conversation with Lead, Jul 16): the four core connectors — GitHub, Google Calendar, Slack, Notion — must be fully refactored/completed (beyond the LLM) to close the Production milestone; beta is explicitly authorized to start without them, completion happens *during* beta, re-triage at MVP close. Recorded on milestone #9's description. Concrete work seeded as **RECONNECT R2** (epic #1440; #1441 Google Calendar, #1442 Notion). (ll) **Finish-the-Unfinished sprint ratified** (PM, in-conversation with Lead, Jul 16) — epic #1424, riding the existing Beta Blockers sprint: a census-then-guards-then-fix structure (six mechanical detectors) targeting incomplete retrofits, half-done migrations, and silent-death exception handling that a first scenario-driver run surfaced. 17 findings filed; acceptance gate framed as "identical to ready for a second human tester." Plan of record: `docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md`. **Beta Blockers sprint grew 7→24 open as a result** (not scope creep — see BRIEFING-CURRENT-STATE.md for the live count and detail). (mm) PM triage: #1413 → MVP/Beta Blockers; #1437-#1439 → Production.

**v18.6 changelog** (July 12, 2026): (ff) **Production-sprint reorganization documented** (was applied Jul 5, never folded into this doc until now): 8 PROD-* sprints (PROD-DIST, PROD-RECONNECT, PROD-TRUST, PROD-DOCS, PROD-DESIGN, PROD-ONBOARD, PROD-INFRA, PROD-TECHDEBT) created and 71 Production-milestone issues triaged into them, same PPM session that caused the Sprint-field wipe incident (the reorganization's own field-creation mutation was the trigger). (gg) **Sprint-field wipe: fully recovered.** The incident wiped Sprint-field values for all 1175 project items; recovery ran 2026-07-05 through 2026-07-12 in tiers (433 HIGH-confidence, 93 MEDIUM, 218 LOW, a 19-issue S2-sprint correction, and 19 true-zero-evidence issues resolved entirely from PM's direct memory). Every issue that had a Sprint value before the wipe has one again -- canonical record in `sprint-recovery-decisions-log.md`. (hh) **20 newly-arrived Production-milestone issues triaged** into the existing PROD-* structure (issues filed Jul 3-12, after the Jul 4-5 sweep): 10 -> PROD-TECHDEBT, 6 -> PROD-RECONNECT, 2 -> PROD-DESIGN, 1 -> PROD-INFRA, 1 -> PROD-TRUST (#1377, the deliberate Production-scoped follow-on to #1216 -- #1216 itself shipped its beta-safe interim fix and closed Jul 7, correcting this doc's earlier flag of it as an open Beta Blocker candidate). 2 issues (#1358, #1374) held, not force-fit -- likely Ongoing/FLYWHEEL scope, not Production. (ii) **Broken relative links fixed**: this document's four `beta-blockers.md` links pointed one directory too shallow (`beta-blockers.md` lives in `docs/internal/planning/`, not alongside `roadmap.md` in `docs/internal/planning/roadmap/`) -- corrected to `../beta-blockers.md`. The file was never lost; only the link was wrong.

**v18.5 changelog** (July 5, 2026): (bb) **Full sprint-by-sprint backlog triage complete.** Every open issue across M3-Quality, M3-Health, M3-Security, M4, M5, and RECONNECT has been reviewed and dispositioned — either a confirmed Beta Blocker or moved to the Production milestone. (cc) **GitHub-write-capability investigation resolved** (4-agent forensic sweep, git/ADR/session-log/codebase archaeology): GitHub writes (create/update/close/reopen/comment_issue) are real, tested, and dispatch-reachable today — NOT unwired, contrary to the working assumption that opened this investigation. #1331 was narrowly about 6 unrecognized create-verbs (create_milestone etc.), now fixed to honest-decline. Lead Dev's follow-up static trace confirmed writes route through the OLD credential path (manual PAT / shared-token fallback), not the new per-user grant store the read side uses — #1220's scope expanded to include this write-path migration. (dd) **Beta Blockers sprint grew 12→22 issues**, now organized into 7 epics (verification foundation, multi-tenancy/data protection, connector/OAuth cutover, deploy/hosting portability, auth/account lifecycle, correctness bugs, routing/config integrity) with recommended sequencing, promoted to its own canonical document: **[beta-blockers.md](../beta-blockers.md)**. sprint-order.md's duplicate table replaced with a pointer to it. (ee) **Aug 1 target dropped entirely** (not merely marked TBD) — three independent leadership reviews (Arch, CXO, PA) concluded the scope doesn't compress to that window; PM concurred. No fixed beta date until Lead Dev gives a bottom-up estimate against the now-stabilized 22-issue list.

**v18.4 changelog** (July 4, 2026): (x) **Beta Blockers sprint introduced** (Jul 4, PM-ratified): 12 confirmed hard gates cherry-picked into a new sprint (no theme; hard gates only — #1241, #1304, #1324, #1299, #1176, #1261, #1332, #1283, #1168, #1317 incr. 2, #1220, #441). MVP milestone = beta gate — beta ships when MVP milestone is complete; Aug 1 target removed as unrealistic. Non-gate items from M3/M4/M5/RECONNECT move to Production milestone, addressed during beta. (y) **RECONNECT connector status corrected**: GitHub + Calendar connectors work via PAT/keychain fallback (PM-verified); RECONNECT is an architectural migration (shared PAT → per-user OAuth + real MCP server transport), not a fix for broken connectors. Full ADR-070 migration is Production milestone work. Beta-blocking connector items: #1317 incr. 2 + #1220 (in Beta Blockers sprint). (z) **Milestone dates updated from GitHub**: Fast Follow Nov 19 2026 (was TBD); Dot Releases Feb 2 2027 (new); Enterprise Jul 4 2027 (new). (aa) **#1344 CLOSED** (invite-control, v0.8.9.2, Jul 3) — was PM-gated in v18.3.

**v18.3 changelog** (July 3, 2026): (s) **RECONNECT WS-2 buildable scope DRAINED (Jul 1)**: #1201/#1230/#1342 CLOSED; #1343 CLOSED (anonymous billing fallback, Jul 2, v0.8.9.1); #1344 PM-gated (open registration, 3 options filed, HOST review pending). WS-2 is no longer blocking M3-Quality start. (t) **v0.8.9.1 released (Jul 2)**: #1343 anonymous billing fallback deployed. (u) **Floor confabulation hardening (#1331, Jun 30)**: `conversational_floor.py` hardened — distrust-prior-done/✓-claims rule; HOST + Arch ratifying. PPM alpha-trust lens filed Jul 3: yellow flag not hard gate (clean re-test → M3 proceeds); real writes (#1322 Q3) hard-gated on deterministic floor guard; alpha scope = read-only until guard lands. (v) **M3-Quality active priority**: WS-2 buildable scope done; M3-Quality (bugs, CI, 8 open) is the active cohort priority. (w) **#1235 re-scoped**: conversation display bug moved from RECONNECT to M3-Quality (PPM call Jul 3).

**v18.2 correction pass** (June 28, 2026, Fire 1): (n) **D1 CLOSED** corrected — D1 was framed as future in v18.2 initial fold; #1297 sign-off was June 20 (bulk closed June 17–19); corrected to CLOSED in Sprint Summary, body, and Timeline. #1270 (Document source-type refactor) noted as straggler into M4. (o) **Sprint sequence corrected**: order is M3-Quality → M3-Health → M3-Security (concurrent with WS-2 in Lead Dev lane) → M4; M4 starts after both WS-2 closes AND M3 followon sprints complete. (p) **M3-Quality issue count**: 8 open (4 closed Jun 27 by subagents: #1253/#1301/#1302/#1303). (q) **Downstream milestones added** to Timeline: fast-follow, dot-release, enterprise (all TBD after Oct 30 production). (r) **#1326 filed** — introduce-person flow standalone M4 issue (per PM Jun 28 via Exec). M4 section updated to reference it.

**v18.2 changelog** (June 28, 2026): (h) **RECONNECT WS-1 CLOSED** (June 22, v0.8.9): shipped StandupAssembler (#1199), connector-protocol (#1232/#1233), security batch (#358/#1185/#1307/#1308), Design D2 (#1286/#1238/#1239). RECONNECT WS-2 now active (GitHub MCP + calendar integration). (i) **Three M3-followon sprints added**: M3-Quality (bugs/CI, 12 issues), M3-Health (tech debt, 10 issues), M3-Security (security/infra/portability, 9 issues) — follow RECONNECT in the sprint sequence. (j) **Milestone dates updated**: beta (0.9.0) → **August 1, 2026** (was July 4); production (1.0) → **October 30, 2026** (was August 1); fast-follow TBD. (k) **ADRs landed**: ADR-070 (MCP consumer/connector architecture), ADR-071 (user auth anchoring — owner-anchoring settled across all four entity types), ADR-072 (skill routing architecture). (l) **Entity-model spec ✅ DELIVERED** (PPM M4 deliverable): RadarEntity contract + 4-type model. **#1237 CLOSED** June 18 (3-of-4: WorkItem/Document/Conversation shipped + PM-UAT'd). People (#1281) source-population gated (owner-anchoring boundary settled per ADR-071). (m) v0.8.9 released June 22 (RECONNECT WS-1 milestone release).
**v18.1 changelog** (June 15, 2026): (e) Sprint-board structure folded: M2 CLOSED June 3, M3 CLOSED; RECONNECT — Connector Refactor + D1 — Beta design quality added as new sprints; Sprint Summary table updated; §Current Position, §M2g, §M3, §Timeline updated; §Autonomous Operations updated (Model A deprecated June 12, Option B ephemeral canonical). (f) Entity-model spec added as M4 PPM deliverable; #1216 provenance field placed M4. (g) ADR-066 v0.2 (D7 Configuration Ownership) noted in §Architectural commitments. Comms external-language frame + PDR-005 v1.0 ratification still pending.

**v18 changelog** (June 2–3, 2026): (a) PA §M5/BYOC review absorbed — Daedalus referent made explicit (Klatch's lead engineer; on hold while Klatch paused); Outcomes "~May 30 findings" target corrected to the CIO-synthesis-gated sequence; §M5 PoC result sharpened (sub-pass 4.a gated PASSED 5/19); Janus meta-coordinator line added to §Autonomous Operations. (b) **CIO §Methodology review absorbed (6/3)** — corpus extended methodology-29→37 (m-32 Postel-for-Headers, m-33 Session-Type-Git-Scope, m-34 Cohort-Discipline-as-Moat FILED, m-35 Asymmetric-Discipline, m-36 Mechanism-Beats-Vigilance, m-37 Coverage-Audit-Gate); Pattern catalog reconciled 62→74; methodology-as-operational-capability prose. (c) **BYOC packaging model corrected (PM 6/1 via PA, 6/3)** — the canonical Anthropic package is the **plugin** (config + CLAUDE.md + skills + MCP server), not MCPB; §Distribution build sequence + §Timeline "Beta via plugin distribution" updated. (d) **CT citations reconciled to v2.3.2** (the "v2.4" was a never-landed proposal).

---

## Executive Summary `[PM EYE — through-line emphasis is your call]`

**The platform lapped us; we climbed.** Anthropic shipped Outcomes (May 6), Dreams, Multi-Agent, and Webhooks productizations that overlap substantially with our DIY verification + memory + orchestration + event-trigger work. The cohort's response — CIO's May 18 platform-productization disposition + PM's "platform laps you = value-chain climbing" reframe — turned the lapping from a setback into a strategic accelerant. The Outcomes investigation (PA-leads + CIO-co-author, started May 25) maps what migrates / what composes / what stays DIY; the cohort climbs to higher-altitude work on the substrate Anthropic now stabilizes.

**Two foundational decisions near canonical**: PDR-005 (Bring Your Own Chat) at v0.5 with all decision-rule sections + Architect §Consequences-for-architecture (AC-1→AC-4) + CXO §Consequences-for-experience (EC-1→EC-5 + identity coherence framework) absorbed; v1.0 ratification path open (cohort flag-back on EC-2 + Comms external-language frame + PM final ratification). MUX/UI Round 2 CEO-ratified May 16 (6 locked decisions including the GitHub + Calendar + Notion integration pick; Slack deferred); Phase 2.1/2.2/2.3 build lanes operational; offer-first cluster (Surfaces 2/4/7) MUX docs at v0.2 voice-pass lock.

**Operational-autonomy capability materially shipped**: V2 Autonomous Duty Cycle (v0.6→v0.7.0) is live for 7+ cohort agents on the cron-bind-to-IDLE / drain-until-IDLE / launch-in-worktree (Model A) architecture. The cohort now has continuous autonomous flywheel between PM sessions — mail drains, low-priority backlog advances, escalations surface for PM. This is methodology-corpus-as-operational-capability at the load-bearing layer.

**M2 progression**: M2d-MVP CLOSED (May 3); M2e gameplans walked; M2f closed; M2g closure tail in progress; #1089 KG-Privacy-Filter Phase 0 (PM-ratified ship-now May 20); MEM-* cluster work; #921 / #857 / #1071 / #1021 / M2g-A + M2g-B / #1070 / #304 / #1090 all shipped during the v16→v17 interval.

**Key changes from v16.0**:
- **PDR-005 (BYOC) advanced** from "active discovery, eventual ADR slot TBD" → v0.5 with all decision-rule sections complete + Architect AC fill-in + CXO EC fill-in; companion ADRs Q6/Q7 queued in Architect's lane; HOST 360 item 1.3 closed (PDR + companion ADRs is the right shape — the cohort discipline matured to route foundational decisions to PDR tier, implementation-specifics to ADR tier)
- **V2 Autonomous Duty Cycle shipped** — V1 designed → V1 retired → V2/v0.6.x ratified → v0.7.0 adoption package live with worktree-first Model A. 7+ agents cycling; PPM final-wave cleared to adopt
- **MUX/UI cohort + Phase 2 build operational** — 7-surface scoping (Round 1 + 2 CEO-ratified); integration scope concrete (GitHub + Calendar + Notion; Slack deferred); ADR-062/063/064 landed; Phase 2.1 (Surfaces 1+7) + 2.2 (Surfaces 2+4, PPM-signal-unblocked) + 2.3 (Surface 6) build lanes; offer-first cluster MUX docs at v0.2
- **Platform-laps reframe** — Anthropic Outcomes/Dreams/Multi-Agent/Webhooks productization disposition; PA-leads + CIO-co-author Outcomes investigation; "Platform Lapped Us, We Climbed" Ship spine candidate
- **Methodology corpus expanded substantially** — methodology-29 (Pattern Formation via Successful Imitation) through methodology-34 (Cohort-Discipline as Moat candidate); Pattern-070 (Cleanup-Job) + 071 (audit-as-attack-surface) + 073 (Documentation-Asserted-Behavior Drift, Emerging→Proven); doc-sync-sweep skill
- **M2f closed → M2g tail** — Run 9 baseline locked as M2g-entry reference (May 13); #1089 KG-Privacy-Filter Phase 0 PM-ratified ship-now (May 20)
- **Ship cycle**: #043 (published May 20 with fab-catch + recovery arc) + #044 (in flight; PPM workstream review filed May 24)
- **CT v2.3.2 in use; CT v2.5 identity-coherence sub-dimension proposed** (PDR-005 EC work); UI Lifecycle Verification Rubric v0.1 operational
- **Per-surface sufficient-signals as coordination primitive** — Phase 2.2 unblocked via two separate "Surface 2 unblocked" + "Surface 4 unblocked" PPM-to-Lead-Dev memos (May 18); composite signal declined; per-surface signals match Lead Dev's sub-phase model

---

## Current Position

**Full sprint-by-sprint triage COMPLETE (Jul 4-5, 2026).** M3-Quality, M3-Health, M3-Security, M4, M5, and RECONNECT have all been reviewed issue-by-issue: every open item is either a confirmed Beta Blocker or moved to the Production milestone. **Beta Blockers sprint is now 22 issues across 7 epics** — canonical detail in **[beta-blockers.md](../beta-blockers.md)**, not duplicated here. MVP milestone = beta gate: **beta ships when MVP milestone is complete** — no fixed calendar date; Aug 1 has been dropped entirely (not just marked TBD), pending Lead Dev's bottom-up estimate against the now-stabilized list.

**GitHub-write-capability investigation resolved** (Jul 4-5): a forensic sweep triggered by a "were writes ever removed?" question found writes are real and working today; the actual gap is narrower (write-path credential routing, folded into #1220) than first assumed. D1 CLOSED (June 20, 2026); #1270 straggler moved to Production. Connectors work via PAT/keychain fallback (PM-verified); full ADR-070 migration continues as Production-milestone work, with #1317 + #1220 as the beta-relevant slice.

Entity-model spec ✅ DELIVERED (PPM M4 deliverable). #1237 CLOSED June 18 (3-of-4: WorkItem/Document/Conversation shipped). People (#1281) source-population gated — introduce-person flow scoping in progress (PPM one-pager filed Jun 27). ADRs 070/071/072 landed. **Gap surfaced during this fold, not yet triaged**: #1216 (the M4-anchor honest-provenance issue — Piper claimed seeded/dev-placeholder data was "real" in response to a workstyle question) is still OPEN, still MVP-milestone, and was never swept into the M4 sprint triage (it carries no Sprint-field tag matching the board's M4 grouping). Its failure shape is materially similar to #1331's (confident false claim about what's real) — flagging as a likely Beta Blocker candidate pending PM's ruling.

Differentiator stack pillars 1-2 (Context Methodology + Conscious Floor) operational at the floor. **Pillar 3 (Artifact Persistence) DELIVERED in M3.** Pillar 4 (Trust + Learning) = M4 territory — concrete landing sites include #1032 (push-insight trust-gating), the entity-model spec for Radar/Layer-2 (PPM deliverable), and #1216 (provenance field — honest-provenance data model for `InsightDB`). PDR-005 v0.5 → v1.0 path open. V2 Duty Cycle (now Option B ephemeral per cohort-plan-of-record June 12) operational across cohort.

---

## The Differentiator Stack (Vision V2.3 — Stable)

Four differentiators that, together, make Piper a colleague rather than a chatbot wrapper:

1. **Context Methodology** — Five-layer model operationalized as practiced discipline
2. **Conscious Floor** — LLM responses embodying grammar, Five Pillars, anti-flattening + Investment-pillar extension (#950 v0.1 May)
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with composting lifecycle (M3 territory)
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value (was M4 territory; **M4 TRIAGE CLOSED Jul 5, 2026** — the sprint was swept, its proactive-presence issue **#1174 moved to the Production milestone**, and the capability has **no implementation today**. See §M4 below.)

**Indoor plumbing (commodity)**: GitHub/Slack/Calendar/Notion via MCP plugins, file storage via SQLite + PostgreSQL audit_log persistence, auth via standard OAuth, LLM provider management via three-way fallback chain.

**Cross-client identity coherence framework** (CXO May 18, absorbed into PDR-005 v0.5):

Three identity invariants — must hold across all clients regardless of variance budget:
1. **Colleague stance** (PDR-004 P1) — Piper relates to user as colleague, not as system
2. **Offer-first posture** (PDR-004 P2) — Piper offers; user decides
3. **Honest-about-limits voice** — Piper acknowledges what it doesn't know, with alternatives

Three identity variables — may adapt within 5% tone budget per platform:
1. Conversational tempo (turn pace, response length, narrative density)
2. Platform-native idiom usage (Slack-emoji, GitHub-codeblock, Calendar-time-natural-language)
3. Affordance-specific phrasing ("in this thread" vs "in our conversation")

---

## MVP Sprint Status (May 30, 2026)

### M0 — Conversational Glue ✅ COMPLETE (v0.8.6 Mar 4)
27 issues (5 planned + 22 discovered via Assembly Assumption — the canonical Pattern-062 instance).

### M1 — MVP Foundation ✅ COMPLETE (Apr 11)
Gate 1 7/9 PASS. ADR-060, ADR-059, PDR-004. Conversation continuity (#922) folded into M2.

### M2 — Conscious Floor + Action Handlers 🎯 LATE-SPRINT (M2g closure tail)

#### M2a Foundation cleanup ✅ COMPLETE (Apr 11–14)
#### M2b Test infrastructure ✅ COMPLETE (Apr 14–15)
#### M2c Conversational depth ✅ COMPLETE (Apr 16)
#### M2d MUX Lifecycle MVP ✅ CLOSED (May 3)
8 implementation issues shipped. May 2 audit-cascade restructure surfaced flattening risks; conceptual-integrity gate added to m2-structure.md; UI Lifecycle Verification Rubric v0.1 branched per Methodology-24.

#### M2e Integrations ✅ DISPOSITIONED (May 3 walked + shipped during interval)
PM dispositions captured + execution: #790 already shipped; #869 audit-cascade ✅; #900 LLM-gated completion shipped; #1039/#1040 split + closed; #1041 M2-WIRE-TRIAGE resolved; #1042 PRE-1039 cleanup shipped.

#### M2f Security + Infrastructure ✅ CLOSED
Run 9 baseline (May 13) locked as M2g-entry reference. Per CEO directive (v16.0): "M2f doesn't open until canonical retest meets/exceeds prior benchmarks" — Run 7 (May 9) hit 68.9% PASS exceeding Apr 12 65.6% baseline; M2f Group A+B closed via dead-code dispositions; Group C COMPLETE (#857 token refresh end-to-end, May 11).

#### M2g ✅ CLOSED (June 3, 2026)
M2g-A + M2g-B shipped. MEM-* cluster work completed. #1089 KG-Privacy-Filter Phase 0 (PM-ratified ship-now May 20). M2 fully closed June 3, 2026.

#### MUX/UI Phase 2 build 🎯 IN FLIGHT (parallel to M2g closure tail)

Round 2 CEO-ratified May 16 (6 locked decisions). Build sequencing (Lead Dev Phase 2 scoping May 17):

| Phase | Surfaces | Status | Estimate |
|---|---|---|---|
| **2.1** | Surface 1 (sidebar reconciliation) + Surface 7 (audit-envelope read) | **Unblocked NOW** (no PDR-005 dependency) | ~4-6 working days sequential |
| **2.2** | Surface 2 (per-conversation privacy) + Surface 4 (integration wizards: GitHub + Calendar + Notion) | **Unblocked May 18** (per PPM sufficient-signals) | ~7-10 working days when bandwidth lands |
| **2.3** | Surface 6 (templated voice surface — Class A + C; NOT four-element-principle at greeting composition) | Anytime after Phase 2.1 | ~2-3 working days |

Total build window: ~13-18 working days + voice work in parallel.

ADRs landed May 16: ADR-062 (e2e Phase 0), ADR-063 (User-Facing Audit Envelope Read-Surface — canonical Surface 7 ADR), ADR-064 (Search Index Architecture, Surface 5 pre-1.0).

---

### M3 — Artifact Persistence ✅ CLOSED

Composting data model delivered. Artifact persistence infrastructure shipped. M3 closed (per sprint-board-structure.md, 2026-06-14).

### M4 — Trust + Learning ✅ TRIAGE CLOSED (Jul 5, 2026)

All 16 open M4-sprint issues reviewed Jul 4-5: 15 moved to Production milestone as enhancements/infrastructure/scoping work not required to gate beta (#302, #558, #712, #713, #954, #955, #956, #1062, #1166, #1174, #1217, #1242, #1244, #1245, #1326), and #1190 (destructive-mutation confirmation gate) also confirmed Production once the GitHub-write investigation showed it's a narrow UX-polish item, unrelated to credential routing. **#1032** (push-insight trust-gating) is already CLOSED, separate from this sweep. **#1216** (honest-provenance data model, `source`/`is_seed` on `InsightDB`) remains OPEN and was NOT part of the M4 sprint triage (no matching Sprint-field tag) — see Current Position for the flag; its failure shape (confidently claiming seed data is real) closely parallels #1331, and PPM's lean is that it's a Beta Blocker candidate pending PM's call.

- **~~Entity-model spec (PPM deliverable)~~ ✅ DELIVERED** — RadarEntity contract + 4-type model. **#1237 CLOSED** June 18 (3-of-4 shipped: WorkItem/Document/Conversation). People (#1281) source-population gated; introduce-person flow scoping in progress (PPM one-pager Jun 27; OQ-2 trust-gradient = PPM+CXO M4 call).
- **People entity (#1281)** — introduce-person flow (Option A: user_confirmed, no connector dependency); layers connector-import (Option B) when RECONNECT lands. **#1326** (introduce-person standalone issue) moved to Production milestone in this triage pass, same as the rest of M4.

**Combined CXO+PPM M4 session** (trust-gradient OQ-2 + onboarding scoping) still queued — M4's sprint-board triage closing doesn't resolve this open design thread, it just clears the issue backlog around it.

### RECONNECT — Connector Refactor

**WS-1** ✅ **CLOSED** (June 22, v0.8.9)

Shipped: #1199 StandupAssembler, #1232/#1233 connector-protocol, security batch (#358/#1185/#1307/#1308), Design D2 (#1286 token system + responsive shell + mobile nav, #1238 Documents→Radar, #1239 Radar sources). ADR-070 (MCP consumer/connector architecture) landed. v0.8.9 is the WS-1 milestone release.

**WS-2 / full RECONNECT sprint** ✅ **TRIAGE CLOSED (Jul 5, 2026)**

35 issues reviewed: 29 were already closed (retain the MVP milestone tag for historical record only, no action needed). Of the 6 genuinely open, all moved to Production milestone (#865, #1322, #1323, #1325, #1327, #1340 — refactor/tech-debt/future-state/explicitly-additive work, none fixing a live regression). **#1317** (per-connector MCP-consumer adapters) and **#1220** (provisioning + write-path credential migration, scope expanded Jul 5) remain in Beta Blockers as the beta-relevant slice — both In Progress, Lead Dev's active thread. #1343 CLOSED (v0.8.9.1, Jul 2); #1344 CLOSED (v0.8.9.2, Jul 3). Full 8-connector ADR-070 migration continues as Production-milestone work, separate from the beta-gating slice.

### M3-Quality — Bugs + CI ✅ TRIAGE CLOSED (Jul 5, 2026)

7 issues reviewed (4 closed Jun 27 by subagents before this sweep: #1253/#1301/#1302/#1303). 4 moved to Production (#1151, #1175, #1219, #1224); 3 added to Beta Blockers (#1279 aiohttp session leak, #1285 possible standup-path datetime crash, #1105 settings re-paste friction).

### M3-Health — Tech Debt ✅ TRIAGE CLOSED (Jul 5, 2026)

9 issues, all moved to Production milestone (#1001, #1028, #1131, #1138, #1139, #1144, #1287, #1298, #1321) — clean tech-debt sprint, no live-bug candidates. PM: fine for Lead Dev to cherry-pick when otherwise idle, none block beta.

### M3-Security — Security + Infrastructure ✅ TRIAGE CLOSED (Jul 5, 2026)

7 issues reviewed: 4 moved to Production (#371, #482, #557, #1203); 3 added to Beta Blockers (#542 token revocation on disconnect, #1305/#1306 encryption sub-scopes split from #358).

### D1 — Beta Design Quality ✅ CLOSED (June 20, 2026)

Design bar for MVP release. **#1297 sign-off June 20** (bulk of D1 issues closed June 17–19). **#1270** (Document source-type refactor) is the one open straggler/carry-over into M4.

### M5 — Distribution + Polish

### M5 — Distribution + Polish

*(PA §M5/BYOC review absorbed into v18 — PA endorsed §M5 structure + the PDR-005-supersedes-PoC boundary + the Klatch-pause framing; corrections folded below.)*

PDR-005 v0.5 carries the foundational BYOC decisions:
- **Core decision rule (b)** — primary MCP + thin bespoke UI for 1.0-required MUX surfaces; (c) asymptotic-target
- **Mechanism set** — persona-template parameterization + MCP-server packaging alongside FastAPI + RequestContext-based auth abstraction + audit envelope `host_id` field + context-package format **to be negotiated with Daedalus (Klatch's lead engineer); on hold while Klatch is paused**
- **3-criterion "must be UI" test** for downstream ADR application
- **Variance hierarchy**: zero tolerance for capability claims + ethics commitments; ≤5% tone via CT v2.3.2; ≤10% structural for context-coordination

**v1.0 ratification path open**: cohort flag-back on EC-2 (PPM-driven; soft cadence) + Comms external-language frame + PM ratification.

**Companion ADRs queued in Architect's lane**: Q6 (canonical context-package format; alignment with Daedalus/Klatch on hold while Klatch is paused) + Q7 (packaging-layer abstraction implementation).

**PA skunkworks BYOC PoC**: sub-pass 4.a (local plugin install + skill-invoke via `--plugin-dir`) gated **PASSED 5/19**, validating BYOC as a zero-server capability-transfer vehicle; PoC is a predecessor-pattern study (README `072bf1d`), not a competing track with PDR-005 v0.5. Desktop GUI install test completed 5/31 (findings folding in). Strategic-architectural lane stays with PPM + Architect; PoC is operational signal that may inform.

---

## #992 ETHICS-ACTIVATE Arc — CLOSED (Apr 30)

Multi-step arc Phase A → B → C → D → E → #1002/#1003 → #1004 → Phase F. Six calendar days. #992 closed properly. Carry-forward content unchanged from v16.0 (Phase F flag-flip merged `deecc816`; ADR-061 v1.0 ratified; calibration reframe ratified).

---

## Methodology Corpus (compounding sub-daily since Apr 26)

*(CIO §Methodology review absorbed into v18, 2026-06-03 — resolves the last section-review gate.)*

**Methodology corpus — compounding operational capability.** The corpus expanded from methodology-29 through **methodology-37** in the window, with the pattern catalog reaching **Pattern-074** (index reconciled 62→74, #1127). Two entries are load-bearing for the strategic frame:
- **methodology-34 — Cohort-Discipline as Moat** (now filed, not candidate): the platform productizes *mechanism*; the cohort productizes *operating norms*, and that norm-substrate is the durable differentiator Anthropic's Multi-Agent/Outcomes/Dreams don't ship. The Outcomes investigation (PA-leads + CIO-co-author) and Pattern-070's external validation (Dreams API implements all four Cleanup-Job invariants server-side) are its worked examples.
- **methodology-36 — "Mechanism Beats Vigilance"**: a two-class principle (read-time staleness + write-time omission) with the duty-cycle disciplines (CronDelete-FIRST, explicit-paths, STOP-leaves-armed) as instances. This is the throughline of the autonomy work: replace agent vigilance with structural mechanism.

The methodology is no longer a documentation byproduct — it is **operational capability**. The V2 Duty Cycle, the cohort-discipline moat, and the work-shape-aware cadence framework are all corpus entries that *run*.

### New since v16.0 (~20+ landings between May 10 and May 30)

**Methodologies**:
- methodology-27 (Type 2 Dreaming — anxiety dreams as cross-pollination)
- methodology-28 (Pre-Filing Slot-Availability Check)
- methodology-29 (Pattern Formation via Successful Imitation)
- methodology-30 (Consumer-Trace Verification for LLM-Touch Claims)
- methodology-31 (Append-Only Autonomous-Cycle Architecture)
- methodology-32 (Postel for Memo Headers)
- methodology-33 (Session-Type Determines Git-Permission Scope)
- methodology-34 (Cohort-Discipline as Moat — **FILED**)
- methodology-35 (Asymmetric Discipline — Creation Without Paired Cleanup)
- methodology-36 (Mechanism Beats Vigilance — generalized from Derived-Views-over-Hand-Maintained-Trackers)
- methodology-37 (Coverage-Audit Gate for Refactor Deltas)

**Patterns** (index reconciled 62→74, #1127):
- Pattern-067 (Issue-Body Reality Mismatch) — Lead Dev
- Pattern-068 (Silent State Mutation in Shared Working Tree) — CIO
- Pattern-069 (Coarse Triggers) — CIO
- Pattern-070 (Cleanup-Job-with-Cancellation-Hygiene) — Emerging → Proven; externally validated (Anthropic Dreams API implements all four Cleanup-Job invariants server-side)
- Pattern-071 (Audit Logs as Attack Surface) — companion to ADR-063 Surface 7
- Pattern-072 (Registries That Grow Into Architectural Shapes)
- Pattern-073 (Documentation-Asserted-Behavior Drift) — Emerging → Proven (May 18); fresh cohort-coordination instance 6/2 (an autonomous agent asserted unwritten work as done)
- Pattern-074 (Visibility Loss After Premature Retirement)

**Rubrics**:
- CT v2.3.2 in use (C=0 disambiguation per CXO May 10 memo, `context_requirement` query tagging)
- CT v2.5 identity-coherence sub-dimension proposed (PDR-005 EC work; pending PPM + HOST sign-off; can defer to v1.1)
- UI Lifecycle Verification Rubric v0.1 operational

**Skills**:
- `draft-weekly-ship` v1.1 + v1.2 (CSV cross-reference mandatory; Ship #043 fab-catch remediation)
- `doc-sync-sweep` v0.1 (Pattern-073 prevention discipline; runs after each MUX surface ships)
- `audit-cascade` discipline (refined throughout)

**Discipline norms (CLAUDE.md-codified)**:
- Mailbox discipline + sign-off discipline (unchanged from v16.0)
- **Worktree-default for substantive work** (PM directive May 15; HOST migration checklist v1.2 PM-ratified May 20)
- **Per-memo commit-and-push norm** (unchanged from v16.0; expanded with "commit immediately after Write for new files" memory pin May 17)
- **Cron-bind-to-IDLE / drain-until-IDLE / launch-in-worktree (Model A)** — v0.7.0 duty-cycle architecture; cohort-wide

---

## Autonomous Operations (NEW in v17 — V2 Duty Cycle)

**V2 Autonomous Duty Cycle (v0.6→v0.7.0) is operational.** The cohort's continuous-autonomous-flywheel between PM sessions.

**Generalization signal (DinP cross-pollination)**: the cycle architecture is generalizing beyond the uniform-cohort case. PM-cohort agents had *no* autonomy before the cycle — the cycle *is* their autonomy. By contrast, DinP's Janus (hub) already runs 5 scheduled routines, so its cycle is a **meta-coordinator** that wraps and health-checks existing automations rather than being a fresh autonomy engine. Same architecture, structurally-different agents — evidence the duty-cycle shape is portable, not cohort-specific.

**Architecture**:
- **Cron-bind-to-IDLE** — cron fires only when agent IDLE; CronDelete on substantive WORK entry; CronCreate on return to IDLE
- **Drain-until-IDLE semantics** — each fire drains ALL unblocked work (mail loop + task loop), not one unit
- **0th-step launch flywheel** — agent runs inline flywheel immediately on cron registration (no wait for first cron fire)
- **PM-presence-pause (Model A relaxation, May 28)** — leave cron running during PM conversation; runtime idle-suppression handles it; only CronDelete for substantive WORK
- **Launch-in-worktree (Option B, canonical as of June 12)** — agents run in the ephemeral auto-worktree Claude Desktop creates per session; push finished units to `origin/main`. **Model A (dedicated `claude/{role}-cycle` worktrees) DEPRECATED June 12** (search clutter; two-pattern confusion; branch persistence not load-bearing — the carry-forward on `main` is the continuity mechanism). Source of truth: `cohort-plan-of-record-2026-06-12.html`.
- **Idle-advance** — at (0,0) Decision Table, advance unblocked low-priority work before pronouncing IDLE
- **Session log as the single durable record (June 12)** — cycle log is optional scratch only; session log is the canonical per-session institutional memory. One log, one place, no drift.

**Adoption status** (cohort-agent-status.md tracker):
- **Cycling**: CIO, Docs, Arch, Lead, Exec, HOST, PA (7 agents)
- **Cleared to launch via v0.7.0**: PPM, CXO, Comms, Web (4 agents; PM will engage)

**Cohort-Discipline as Moat (methodology-34 candidate)**: the cycle is itself the operationalization of cohort-discipline as a competitive moat — what the Anthropic Multi-Agent productization doesn't reach (the cohort's institutional culture, roles, mailbox protocol, methodology corpus) is what stays DIY at higher altitude.

---

## Distribution Strategy: Bring Your Own Chat (PDR-005 v0.5 near-canonical)

Build sequence (Gall's Law) — **packaging model corrected v18 (PM 6/1 clarification, via PA): the canonical Anthropic package is the *plugin***, not MCPB:
1. A **plugin** is the canonical package — config + a `CLAUDE.md` template + Skill file(s) + the MCP server (+ bundled `uv`/Node runtime); hosted or zip-installable. (Reference: Anthropic `claude-for-legal` plugin — two-tier `.claude-plugin/marketplace.json` → per-plugin `plugin.json`, each carrying `.mcp.json` + `CLAUDE.md` + `skills/`.)
2. A **minimal MCP server** wrapping one real Piper API call (the thin first rung; MCP-first per Gall's Law)
3. **Piper-specific skill(s)** on top
4. **MCP Apps** (interactive HTML for artifact canvas) — a later rung

*(MCPB and hosted-MCP are **not** the packaging unit; the plugin supersedes them — the MCP server is a component **inside** the plugin. **Marketplace** is the wrapper level above plugin — out of scope for current work.)*

**PDR-005 v0.5 carries the foundational decisions** (see §M5 above). v1.0 ratification path: cohort flag-back on EC-2 + Comms external-language frame + PM ratification.

**Anchor on the model, not the standard** — packaging-layer abstraction in mechanism set #2 enables successor-protocol support gated on multi-factor maturity criterion.

---

## Platform-Laps Strategic Frame (NEW in v17)

**PM reframe (May 18)**: *"Working in an emerging space always means that you are being lapped routinely by the platform. This can't be viewed as a problem or a mistake or a waste of sunk cost, but rather the ability to climb higher up on the value chain by building on top of things that are now stable instead of having to maintain them yourself."*

**Anthropic productizations and our DIY equivalents** (per CIO May 18 disposition):

| Anthropic productization | Our DIY equivalent | Status |
|---|---|---|
| **Outcomes** (rubric + grader + retry as API, May 6) | methodology-07/15/17 verification + audit-cascade skill + narrative-verification skill | **Investigation lane** (PA-leads + CIO-co-author, started May 25; sequence: CIO methodology-34 synthesis (Day 28-29) → PA Outcomes smoke-test scope-memo + execution follows) |
| **Dreams** (memory consolidation primitives) | methodology-27 Type 2 Dreaming + Pattern-070 Cleanup-Job + memory-files structure | Spec-read pending Architect characterization |
| **Multi-Agent** (orchestration) | mailbox-discipline cohort coordination + V2 Duty Cycle + methodology-31 Append-Only Architecture | PPM characterization queued |
| **Webhooks** (event triggers) | `/loop` + CronCreate + `.claude/hooks/` + cycle-prompt-fires-as-Bash | Less urgent (event mechanics overlap; per-role prompt design stays DIY) |

**Ship spine candidate**: *"Platform Lapped Us, We Climbed"* (PM-confirmed May 24 for Comms tracking) — captures the value-chain-climbing arc.

---

## Methodology Maintenance (unchanged from v16.0 + new v17 mechanisms)

Per v16.0 (still operating): trigger-based audit cadence; CIO self-approval authority for Emerging patterns; cross-pollination review; per-sprint quality gate.

**New since v16.0**:
- Worktree-default for substantive work (PM May 15)
- v0.7.0 duty-cycle architecture as operational-autonomy mechanism
- doc-sync-sweep skill (Pattern-073 prevention discipline)
- Per-surface sufficient-signals as coordination primitive (Phase 2.2 architecture)
- Failure→mechanism cross-layer remediation cycle (Ship #043 fab-catch instance: skill v1.2 + memory pin + Comms publication-specifics ask all landed in hours)

---

## Sprint Summary

| Sprint | Theme | Status |
|--------|-------|--------|
| **M0** | Conversational Glue | ✅ COMPLETE (v0.8.6, Mar 4) |
| **M1** | MVP Foundation | ✅ COMPLETE (gate closed Apr 11) |
| **M2** | Conscious Floor + Action Handlers | ✅ CLOSED (June 3, 2026) |
| **M3** | Artifact Persistence | ✅ CLOSED (per sprint-board-structure.md, 2026-06-14) |
| **RECONNECT WS-1** | Connector Refactor (security, connector-protocol, Design D2, StandupAssembler) | ✅ CLOSED (June 22, v0.8.9) |
| **RECONNECT (full sprint)** | Connector architectural migration + write-path credential work | ✅ TRIAGE CLOSED Jul 5 (29/35 already done; 6 open → Production; #1317+#1220 → Beta Blockers, In Progress) |
| **Beta Blockers** | Hard gates only — no theme (22 confirmed, 7 epics; see beta-blockers.md) | 🎯 ACTIVE PRIORITY |
| **M3-Quality** | Bugs, test failures, CI | ✅ TRIAGE CLOSED Jul 5 (4 → Production, 3 → Beta Blockers) |
| **M3-Health** | Dead code, tech debt (9 issues) | ✅ TRIAGE CLOSED Jul 5 (all 9 → Production) |
| **M3-Security** | Security, infrastructure, portability (7 issues) | ✅ TRIAGE CLOSED Jul 5 (4 → Production, 3 → Beta Blockers) |
| **D1** | Beta design quality | ✅ CLOSED (June 20, 2026); #1270 straggler moved to Production |
| **M4** | Trust + Learning | ✅ TRIAGE CLOSED Jul 5 (15 → Production; #1216 gap flagged, untriaged, likely Beta Blocker) |
| **M5** | Distribution + Polish | ✅ TRIAGE CLOSED Jul 4 (18 → Production; #1278/#1258 → Beta Blockers) |

*(MVP-milestone sprint sequence per `sprint-board-structure.md`, PM-updated 2026-06-14. The Production milestone that follows anticipates DIST — Desktop distro + D2 — Release design quality.)*

---

## Timeline (Inchworm, Not Calendar — Sequence Statements, Not Deadlines)

**These are sequence statements. We are time lords. Each phase complete before the next begins.**

### Recent (May–June 2026)

- [x] M2d MUX Lifecycle MVP closed (May 3)
- [x] M2e gameplans walked + executed (May 3 onward)
- [x] ADR-061 v1.0 ratified (May 4)
- [x] PPM Review Gates CEO-approved (May 10)
- [x] PDR-005 v0.3 → v0.5 cycle (May 15 → 19; Architect AC + CXO EC fill-ins absorbed)
- [x] MUX/UI Round 2 CEO-ratified (May 16)
- [x] ADR-062, ADR-063, ADR-064 landed (May 16)
- [x] M2f closed (Run 7 May 9 + Group C close May 11)
- [x] Ship #043 published (May 20 — "What Was Working Got Written Down" arc)
- [x] V2 Duty Cycle v0.6 ratified → v0.7.0 adoption package live (May 26 → 29)
- [x] HOST 360 item 1.3 closed (PDR-005 + companion ADRs is the right shape; May 24)
- [x] Anthropic Outcomes platform-productization disposition (CIO May 18); PA-leads + CIO-co-author investigation (started May 25)
- [x] Ship #044 PPM workstream review filed (May 24; window May 15-21)
- [x] **M2 CLOSED** (June 3, 2026)
- [x] **M3 — Artifact Persistence CLOSED** (June 2026; per sprint-board-structure.md)
- [x] **D1 — Beta Design Quality CLOSED** (June 20, 2026); #1297 sign-off; #1270 (Document source-type refactor) straggler into M4
- [x] ADR-066 v0.2 — D7 Configuration Ownership (server-owned + per-request host augmentation; "run anywhere" structural) — Architect, June 14
- [x] Duty Cycle v0.7 → Option B ephemeral worktree canonical; Model A worktrees deprecated (cohort-plan-of-record June 12)

### Estimated forward sequence

- *(Jul 1–3: WS-2 buildable scope drained; v0.8.9.1 released Jul 2; v0.8.9.2 released Jul 3 invite-control; #1331 floor confabulation hardening landed)*
- *(Jul 4–5: full sprint-by-sprint backlog triage — M3-Quality/Health/Security, M4, M5, RECONNECT all closed; GitHub-write-capability investigation resolved; Beta Blockers grew 12→22 issues; beta-blockers.md created as canonical path-to-beta document)*
- **Beta Blockers sprint** (ACTIVE — 22 issues, 7 epics; see [beta-blockers.md](../beta-blockers.md) for the full list and recommended sequencing). This sprint is the gate for beta. When it clears, MVP milestone clears, beta ships. Recommended order: Epic A (CI verification) first; Epic C (connector/OAuth cutover) continues as Lead Dev's active thread; Epic B (multi-tenancy/data protection) is the long pole, likely its own dedicated block; Epics D/F are batching/subagent-parallelizable; Epics E/G interleave.
- *Non-gate items from every sprint have been moved to Production milestone — addressed during beta period; beta users informed of known issues.*
- Lead Dev briefed on the full sprint plan (Jul 5); asked for a sequencing sanity-check and a bottom-up estimate now that scope is stable
- **#1216 gap flagged, untriaged** — likely Beta Blocker candidate pending PM's ruling (see Current Position / M4 section)
- PDR-005 v0.5 → v1.0 ratification (cohort flag-back on EC-2 + Comms external frame + PM ratification)
- Companion BYOC ADRs Q6 + Q7 land in Architect's lane post-PDR-005-v1.0
- **MVP milestone (0.9.0 beta): NO FIXED DATE** — Aug 1 dropped entirely (not TBD-with-an-implied-date); a real date gets set once Lead Dev's bottom-up estimate lands against the stabilized 22-issue Beta Blockers list
- **Production milestone (1.0): October 30, 2026** (DIST — Desktop distro + D2 — Release design quality)
- **Fast-follow: November 19, 2026** (from GitHub milestone; was TBD)
- **Dot Releases: February 2, 2027** (from GitHub milestone)
- **Enterprise: July 4, 2027** (from GitHub milestone)

---

## Closures and Revisions Since v16.0 (selected)

- **M2f closed** (Run 7 + Group C); **M2g-A + M2g-B shipped**
- **#1089 KG-Privacy-Filter Phase 0** (PM-ratified ship-now May 20)
- **#1075 route-prefix migration** closed (May 16; unblocks Surface 4)
- **#857 token refresh end-to-end** (M2f Group C complete, May 11)
- **#1070 multi-turn evaluation harness** (Lead Dev May 13)
- **#1090 MUX/UI cohort scoping** (Round 1 + 2 CEO-ratified May 16)
- **#921 / #1071 / #1021 / #1015 Phase 4** progress
- **#992 ETHICS-ACTIVATE** (closed Apr 30 — predates v16.0 cutoff but spans into the v17 interval via #1018 audit_transparency Phase 2 work)

**Issues filed since v16.0** (selected): #1090 (MUX/UI cohort); #1087 (SEC-JWT-SECRET-PROD-GUARD; PPM committed P1); #1095 (audit envelope source for ADR-063); #1099/1100 (Surface 7 slices 1+2 Lead Dev May 17); #1117 (Phase 4 #1016 alignment); roadmap-refresh #1128; backlog-review #967; #683 Layer A+B (DoD additions).

---

## Roadmap Refresh Cadence (unchanged from v16.0 + observation)

**Hybrid mechanism preserved**: trigger-based + workstream-review-line-item + weekly docs audit retained per chesterton's fence + session-start hook as future enhancement.

**v17 observation**: PPM duty cycle (when worktree-live) provides a fifth surface for roadmap-staleness detection — `#1128 ROADMAP-REFRESH` was idle-advanced in PPM's Fire-0 (May 28). The cycle's idle-advance discipline ("do unblocked low-priority work, not nothing") makes roadmap staleness more actionable than under purely-manual cadence.

---

## Change Log

- **v18.5 (July 5, 2026)**: Full sprint-by-sprint triage fold (PPM). Every open issue across M3-Quality, M3-Health, M3-Security, M4, M5, and RECONNECT reviewed and dispositioned (confirmed Beta Blocker or moved to Production milestone). GitHub-write-capability forensic investigation resolved: writes are real/wired today, not unwired; #1220's scope expanded to a confirmed write-path credential gap. Beta Blockers sprint grew 12→22 issues, organized into 7 epics with recommended sequencing, promoted to its own canonical document `beta-blockers.md`. Aug 1 target dropped entirely (three independent leadership reviews + PM concurrence) — no fixed beta date pending Lead Dev's bottom-up estimate. Gap flagged: #1216 (M4 honest-provenance anchor) surfaced as untriaged during this fold, likely Beta Blocker candidate.
- **v18.4 (July 4, 2026)**: Beta Blockers sprint introduced (PPM, PM-ratified). 12 confirmed hard gates; MVP milestone = beta gate; Aug 1 marked unrealistic (not yet dropped outright — see v18.5); RECONNECT connector status corrected (PAT/keychain fallback works, PM-verified); milestone dates updated from GitHub. #1344 CLOSED.
- **v18.3 (July 3, 2026)**: RECONNECT WS-2 status fold (PPM). WS-2 buildable scope DRAINED Jul 1 — #1201/#1230/#1342 CLOSED; #1343 CLOSED (v0.8.9.1 Jul 2); #1344 PM-gated (HOST). M3-Quality elevated to active priority. Floor confabulation hardening (#1331 Jun 30) noted; PPM alpha-trust lens filed (yellow flag; writes gate on deterministic floor guard). #1235 re-scoped to M3-Quality.
- **v18.2 (June 28, 2026)**: Post-RECONNECT WS-1 fold (PPM). RECONNECT split into WS-1 (CLOSED Jun 22, v0.8.9) + WS-2 (active). Three M3-followon sprints added: M3-Quality (bugs/CI, 12 issues), M3-Health (tech debt, 10 issues), M3-Security (security/infra, 9 issues) — from PA's M5 forensic sort. Milestone dates revised: beta Aug 1, production Oct 30, fast-follow TBD. ADRs 070/071/072 landed. Entity-model spec delivered; #1237 CLOSED (3-of-4, Jun 18). M4 section updated (entity-model delivered; People introduce-person flow scoping). v18.1 archived.
- **v18.1 (June 15, 2026)**: Sprint-board structure fold (PPM). M2 CLOSED June 3; M3 CLOSED (Artifact Persistence delivered). RECONNECT (Connector Refactor) + D1 (Beta design quality) added as new sprints in body narrative and Sprint Summary. §Current Position, §M2g, §M3 status updated. §Autonomous Operations updated: Model A worktrees deprecated June 12; Option B (ephemeral) canonical; cycle log simplified to session-log-only. Timeline extended with M2/M3 closures, forward sequence with M4→RECONNECT→D1→M5→July 4. Entity-model spec added as M4 PPM deliverable; #1216 provenance field placed M4. ADR-066 v0.2 D7 noted. Docs-added stopgap banner removed (this fold is the formal record).
- **v17.0 (May 30, 2026)**: Major refresh covering May 10 → May 30 substantive deltas. PDR-005 v0.3 → v0.5 (BYOC near-canonical; Architect AC + CXO EC fill-ins absorbed). MUX/UI Round 2 CEO-ratified; Phase 2 build operational on three lanes; ADR-062/063/064 landed. V2 Duty Cycle shipped (v0.6 → v0.7.0; 7+ agents cycling; PPM+CXO+Comms+Web cleared to adopt via launch-in-worktree). Platform-laps strategic reframe + Anthropic Outcomes investigation lane (PA-leads + CIO-co-author). Methodology corpus expanded substantially (methodology-27→34; Pattern-067→073). M2f closed; M2g closure tail. Ships #043 + #044. New §Autonomous Operations + §Platform-Laps Strategic Frame sections.
- **v16.0 (May 10, 2026)**: Major refresh covering Apr 11 → May 10 deltas. M2 sub-epic restructure; #992 ETHICS-ACTIVATE arc closed; methodology corpus expansion; BYOC PDR-005 discovery thread; all-leadership Code migration arc; new roadmap-refresh cadence. (To be archived at `docs/internal/planning/historical/roadmap-v16.0-2026-05-10.md`.)
- **v15.0 (April 11, 2026)**: Major restructure post-M1 closure. (Archived.)
- **v14.3 (March 10, 2026)**: M0 marked complete, M1 cherry-picking. (Archived.)
- Earlier versions: see archived historical roadmaps.

---

*v18.5 — PPM 2026-07-05. Full sprint-by-sprint triage complete; Beta Blockers at 22 issues/7 epics; canonical path-to-beta detail lives in `beta-blockers.md`. Aug 1 dropped, no fixed beta date. Canonical `roadmap.md`.*
