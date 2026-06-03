# Piper Morgan Roadmap v18.0 (DRAFT)

**Date**: June 2, 2026 (CIO §Methodology absorbed 2026-06-03)
**Author**: PPM, with leadership review (PA — §M5/BYOC + skunkworks **ABSORBED v18**; CIO — §Methodology **ABSORBED v18 (6/3)**; CXO — §Differentiator stack EC framework; Architect — §Architectural commitments AC framework; Lead Dev — §M2g + Phase 2 build; Comms — external-language frame pending)
**Status**: DRAFT — **both section reviews absorbed (PA §M5/BYOC + CIO §Methodology); substantively complete and READY FOR PM RATIFICATION** → Docs swap into canonical `roadmap.md`. Comms external-language frame is a parallel polish input (external-facing language) that can fold at ratification or as v18.1; not gating the internal canonical. Per v15→v16 precedent.
**Supersedes**: v17.0-draft (May 30, 2026, `00cee8d47` — the version PA reviewed against); v16.0 (May 10, 2026) to be archived at `docs/internal/planning/historical/roadmap-v16.0-2026-05-10.md` per the v15.0 archive pattern
**v18 changelog**: (a) PA §M5/BYOC review absorbed — Daedalus referent made explicit (Klatch's lead engineer; on hold while Klatch paused); Outcomes "~May 30 findings" target corrected to the CIO-synthesis-gated sequence; §M5 PoC result sharpened (sub-pass 4.a gated PASSED 5/19); Janus meta-coordinator line added to §Autonomous Operations. (b) **CIO §Methodology review absorbed (6/3)** — corpus extended methodology-29→37 (m-32 Postel-for-Headers, m-33 Session-Type-Git-Scope, m-34 Cohort-Discipline-as-Moat FILED, m-35 Asymmetric-Discipline, m-36 Mechanism-Beats-Vigilance, m-37 Coverage-Audit-Gate); Pattern catalog reconciled 62→74; methodology-as-operational-capability prose.

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
- **CT v2.4 in use; CT v2.5 identity-coherence sub-dimension proposed** (PDR-005 EC work); UI Lifecycle Verification Rubric v0.1 operational
- **Per-surface sufficient-signals as coordination primitive** — Phase 2.2 unblocked via two separate "Surface 2 unblocked" + "Surface 4 unblocked" PPM-to-Lead-Dev memos (May 18); composite signal declined; per-surface signals match Lead Dev's sub-phase model

---

## Current Position

M2 mid-sprint with M2g closure tail in flight. MUX/UI Phase 2 build operational on three lanes (2.1 Surfaces 1+7 unblocked NOW; 2.2 Surfaces 2+4 PPM-signal-unblocked; 2.3 Surface 6 anytime after 2.1). PDR-005 v0.5 → v1.0 path open. V2 Duty Cycle operational across 7+ cohort agents.

Differentiator stack pillars 1-2 (Context Methodology + Conscious Floor) operational at the floor; #992 ETHICS-ACTIVATE arc closed Apr 30; ADR-061 v1.0 ratified May 4. Pillar 3 (Artifact Persistence) and Pillar 4 (Trust + Learning) remain M3/M4 territory; M3 scope sharpening continues at M2 closure.

---

## The Differentiator Stack (Vision V2.3 — Stable)

Four differentiators that, together, make Piper a colleague rather than a chatbot wrapper:

1. **Context Methodology** — Five-layer model operationalized as practiced discipline
2. **Conscious Floor** — LLM responses embodying grammar, Five Pillars, anti-flattening + Investment-pillar extension (#950 v0.1 May)
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with composting lifecycle (M3 territory)
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value (M4 territory)

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

#### M2g 🎯 CLOSURE TAIL IN PROGRESS
M2g-A + M2g-B shipped during v16→v17 interval. Ongoing: MEM-* cluster work; demand-gated cluster dispositions. #1089 KG-Privacy-Filter Phase 0 (PM-ratified ship-now May 20). Issue list at PPM tracker `dev/active/ppm-standing-items.md`.

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

### M3 — Artifact Persistence
Theme + scope unchanged from v16.0. Post-MVP candidates surface as M3 territory. Composting data model designed in M3; composting engine deferred to M4.

### M4 — Trust + Learning
Theme + scope unchanged from v16.0. Trust graduation MVP must be credible first step toward full model.

### M5 — Distribution + Polish

*(PA §M5/BYOC review absorbed into v18 — PA endorsed §M5 structure + the PDR-005-supersedes-PoC boundary + the Klatch-pause framing; corrections folded below.)*

PDR-005 v0.5 carries the foundational BYOC decisions:
- **Core decision rule (b)** — primary MCP + thin bespoke UI for 1.0-required MUX surfaces; (c) asymptotic-target
- **Mechanism set** — persona-template parameterization + MCP-server packaging alongside FastAPI + RequestContext-based auth abstraction + audit envelope `host_id` field + context-package format **to be negotiated with Daedalus (Klatch's lead engineer); on hold while Klatch is paused**
- **3-criterion "must be UI" test** for downstream ADR application
- **Variance hierarchy**: zero tolerance for capability claims + ethics commitments; ≤5% tone via CT v2.4; ≤10% structural for context-coordination

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
- CT v2.4 in use (C=0 disambiguation per CXO May 10 memo, `context_requirement` query tagging)
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
- **Launch-in-worktree (Model A)** — agents launch Claude Code inside `claude/{role}-cycle` worktree; satisfies "do not register on main" by construction
- **Idle-advance** — at (0,0) Decision Table, advance unblocked low-priority work before pronouncing IDLE
- **Three per-agent docs** — standing-items tracker (task list) + cycle log (per-fire chronology) + escalations doc (attention surface for PM)

**Adoption status** (cohort-agent-status.md tracker):
- **Cycling**: CIO, Docs, Arch, Lead, Exec, HOST, PA (7 agents)
- **Cleared to launch via v0.7.0**: PPM, CXO, Comms, Web (4 agents; PM will engage)

**Cohort-Discipline as Moat (methodology-34 candidate)**: the cycle is itself the operationalization of cohort-discipline as a competitive moat — what the Anthropic Multi-Agent productization doesn't reach (the cohort's institutional culture, roles, mailbox protocol, methodology corpus) is what stays DIY at higher altitude.

---

## Distribution Strategy: Bring Your Own Chat (PDR-005 v0.5 near-canonical)

Build sequence (Gall's Law) — unchanged from v15.0:
1. MCP server — standalone, stdio transport
2. MCPB packaging — Claude Desktop bundle
3. Claude Project template — persona/instructions for hybrid
4. MCP Apps — interactive HTML for artifact canvas

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
| **M2** | Conscious Floor + Action Handlers | 🎯 LATE-SPRINT (M2a/b/c/d-MVP/e/f closed; M2g closure tail in progress; MUX/UI Phase 2 build operational) |
| **M3** | Artifact Persistence | — (post-MVP candidates surfacing; composting data model designed in M3) |
| **M4** | Trust + Learning | — (#1032 Push-insight trust-gating is first concrete touch surface) |
| **M5** | Distribution + Polish | 🎯 PDR-005 v0.5 near-canonical (v1.0 ratification path open); MUX/UI Phase 2 build feeds 1.0 scope |

---

## Timeline (Inchworm, Not Calendar — Sequence Statements, Not Deadlines)

**These are sequence statements. We are time lords. Each phase complete before the next begins.**

### Recent (May 2026)

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

### Estimated forward sequence

- M2g closure tail + MUX/UI Phase 2 build completion (~13-18 working days)
- PDR-005 v0.5 → v1.0 ratification (cohort flag-back on EC-2 + Comms external frame + PM ratification)
- Companion BYOC ADRs Q6 + Q7 land in Architect's lane post-PDR-005-v1.0
- PPM + CXO + Comms + Web duty-cycle adoption via v0.7.0 launch-in-worktree (PM-engaged)
- Outcomes investigation: CIO methodology-34 synthesis (Day 28-29) → PA Outcomes smoke-test scope-memo + execution follows
- Ship #044 publication (Wed May 27 or Thu May 28 target; spine candidate "Platform Lapped Us, We Climbed")
- M3 (Artifact Persistence): scope sharpening at M2g closure
- Beta via MCPB → v1.0

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

- **v17.0 (May 30, 2026)**: Major refresh covering May 10 → May 30 substantive deltas. PDR-005 v0.3 → v0.5 (BYOC near-canonical; Architect AC + CXO EC fill-ins absorbed). MUX/UI Round 2 CEO-ratified; Phase 2 build operational on three lanes; ADR-062/063/064 landed. V2 Duty Cycle shipped (v0.6 → v0.7.0; 7+ agents cycling; PPM+CXO+Comms+Web cleared to adopt via launch-in-worktree). Platform-laps strategic reframe + Anthropic Outcomes investigation lane (PA-leads + CIO-co-author). Methodology corpus expanded substantially (methodology-27→34; Pattern-067→073). M2f closed; M2g closure tail. Ships #043 + #044. New §Autonomous Operations + §Platform-Laps Strategic Frame sections.
- **v16.0 (May 10, 2026)**: Major refresh covering Apr 11 → May 10 deltas. M2 sub-epic restructure; #992 ETHICS-ACTIVATE arc closed; methodology corpus expansion; BYOC PDR-005 discovery thread; all-leadership Code migration arc; new roadmap-refresh cadence. (To be archived at `docs/internal/planning/historical/roadmap-v16.0-2026-05-10.md`.)
- **v15.0 (April 11, 2026)**: Major restructure post-M1 closure. (Archived.)
- **v14.3 (March 10, 2026)**: M0 marked complete, M1 cherry-picking. (Archived.)
- Earlier versions: see archived historical roadmaps.

---

*v17.0 DRAFT — PPM 2026-05-30. Cohort section review (PA §M5/BYOC + CIO §Methodology) pending; CEO ratification gates Docs swap into canonical `roadmap.md`. Per v15→v16 precedent.*
