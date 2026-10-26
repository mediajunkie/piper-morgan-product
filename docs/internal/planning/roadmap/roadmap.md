# Piper Morgan Roadmap v19.1

**Date**: October 26, 2026 (v19.1: the Current Position re-fold after the Production map rulings, ESSENCE v1.1 and the ratified promise register; v19.0 of October 10 is archived whole at `../historical/roadmap-v19.0-2026-10-26.md`)
**Author**: PPM. Section owners as in v18: PA (BYOC / skunkworks), CIO (Methodology), CXO (Differentiator stack), Architect (architectural commitments), Lead Dev (build), Comms (external language).
**Status**: Active. Canonical `roadmap.md`. **The v18.10 document is archived whole** at `../historical/roadmap-v18.10-2026-10-10.md` (v18.1 through v18.10 changelogs, the Beta Blockers / 22-issue narrative, the 07-16 Current Position). Nothing was deleted; sections below that predate this fold are kept in place under an explicit "historical" banner so a reader cannot mistake May or July state for current state.
**Supersedes**: v19.0 (October 10, 2026); the v18 line (v18.0 through v18.10); v17.0 (May 30, 2026); v16.0 (May 10, 2026).

**How to read this document.** The **gate, the dates and the audience model** are current as of 2026-10-26 and live in *Current Position*, *Sprint Summary* and *Timeline* below. They are **pointers to canonical sources**, not copies: the gate rules are `../beta-gate-standard.md`, the audience model is `../release-model.md`, live counts are `scripts/sprint-truth.py`, orientation is `docs/briefing/BRIEFING-CURRENT-STATE.md`. Where this document and one of those disagree, **that source wins**. Sections marked `[HISTORICAL]` are frozen at the date in their banner (May 30 or July 16) and are retained for provenance only.

**v19.1 changelog** (October 26, 2026, PPM; Docs' weekly audit #2180 found this file 14 days untouched). Only *Current Position* is rewritten; every other section is carried. Each line cites its source, and none was re-litigated here:
- (a) **xian's Production map rulings** (decisions.log 2026-10-24 17:28): one production instance, alpha's own Fly app, plus a synthetic-data staging never restored from production; **1.0 = every promise gated 1.0 has a closed issue, and main is green**; public beta opens by waitlist with batch admission; a Readiness lane (#2157 to #2161, Terms-backed) gates public beta.
- (b) **ESSENCE v1.1 ratified** (xian, 2026-10-25 12:40). Commitment 6 becomes complementary surfaces: the web app is the beta surface, and the MCP and plugin surface ships during the beta, its completion gating public beta. This replaces v19.0's "MCP/plugin is not a gate surface". PRD/spec drafting is recorded as after 1.0.
- (c) **The promise register** `docs/internal/product/promises.yaml` was ratified by xian on 2026-10-25 at 14:04. It holds 20 promises (E1-E7, T1-T8, R1-R5), each gated private-beta, public-beta or 1.0. Which issues back a promise is read from `promise:<id>` labels.
- (d) **Production is organized into sprints in closing order:** H (honesty) → D (data boundaries and terms) → PUB → C (connectors) → V (conversation reliability) → E (experience), with T, Doc, Dist, Readiness and Q (health) alongside. The plan is `../production-sprint-proposal-2026-10-23.md`. xian added the three new Sprint options on 10-25.
- (e) **A generated Production map** (`../production-map.html`, from `scripts/generate-production-map.py` over the board snapshot) replaces hand-kept sprint narrative. Every Friday, Exec's synthesis carries its since-last diff.
- (f) **The invitation:** xian ruled on 2026-10-23 at 16:57 that invitations may go once #2132 closes, and that he picks the exact time. #2132 closed served the same evening. The Terms page wording was ruled on 10-25 (Call A1: "What this alpha is").

**Verified how (v19.1).** Method:
- read decisions.log entries 10-23 16:57, 10-24 17:28 and 10-25 14:04 in full;
- read `promises.yaml` in full;
- ran `gh api .../milestones`, `gh issue list --milestone MVP` and `gh issue list --milestone Production` at 2026-10-26 10:3x PDT;
- reconciled the plan doc's Production rows to a fresh board snapshot (203 = 203);
- read alpha `/health` (`69d859ca5f`) as quoted in the briefing at 09:27 and by me at 09:33.

Layer: the decision record, the tracker and served health. Not re-audited: any section other than *Current Position*. Not checked: whether a beta hostname fronts alpha's app.

**v19.0 changelog** (October 10, 2026, PPM). The full fold of #1644's open half. Since v18.7 (July 16) the following changed the shape of this roadmap; each line cites its source and none was re-litigated here:
- (a) **The gate is the open MVP milestone, closed by a frozen-list rule.** Four admission classes tagged at filing (data loss, security, honesty, golden-path), Epic 0 clause, per-surface table, slip rule; PM ratified 2026-10-05 (`../beta-gate-standard.md`). The "Beta Blockers sprint of 22 issues / 7 epics" model (v18.5) and `beta-blockers.md` as the gate are superseded; `beta-blockers.md` keeps its Epics A-G history under a banner. Measured pass 2026-10-05 of 31 open MVP issues (31 of 31 read in full) and PM's rulings 10-06 brought the gate to 14.
- (b) **Dates.** PM reset the milestone dates on 2026-09-06 (decisions.log), and held the beta dates on 2026-10-09 09:46: **design partners Fri 10-23, hard stop Fri 10-30**, both conditional on named unknowns. The slip ledger stands at 4 slips, 0 days moved (as of 10-10). The Wed 10-14 tripwire is a PPM inference, not a date PM named (see *Timeline*).
- (c) **Release model.** `../release-model.md` (2026-08-30): milestone closure gates *audience*, not a calendar date. MVP closure starts invitation-only private beta (v0.9.0, reserved for it); public beta is gated on the front-loaded Production MCP-path cluster; 1.0 needs the Production milestone closed in full. ESSENCE v1.0 (08-30) added the seventh commitment and ratified this reconciliation.
- (d) **Fundamentals first (PM 2026-08-08, after the beta date moved back a month).** Epic 0 (#1595, the Understanding-Layer Inversion spine) is the current epic; its completion tail (Phase 3 deletions, contract-test pins) is gate scope by definition. Arch's standing direction (10-05): *the LLM decides meaning; code decides permission, checks meaning against real data, and shows you before it acts.* Interpretation-layer code retires by ratchet.
- (e) **Hosting and distribution.** Alpha runs on Fly (`piper-morgan`, v0.8.14.0 per the briefing); the droplet is destroyed and `origin/production` deleted (09-22/29). The beta target is `beta.pipermorgan.ai`, hosted web UI required. **MCP/plugin** is released and tested during the beta period, not a gate surface; **BYOC/local** is not ruled as a beta surface (PM 10-05). **Bring-your-own-key: YES** (PM 10-05): Piper provides no LLM service and covers no one's LLM cost. PDR-006 (07-31) made the host-LLM-owns-the-surface consequence explicit for the primary distribution surface.
- (f) **Calendar was deferred from MVP (PM 08-30) with a positioning correction that binds planning**: calendar returns as a *central* capability, not an afterthought; what was parked is the unreachable MCP simulation construction, not the live calendar path standup/briefing uses.
- (g) **Privacy and credentials.** Cross-user preference pooling severed and purged (#1613, 08-31); bearer credentials never travel through this PUBLIC repo (#1845, 09-24); one credential resolver per connector (#1965, 10-08).
- (h) **Cohort operations changed under the old Autonomous Operations section**: the cohort migrated to Amber on 2026-07-25 (Model A stable per-agent worktrees on Amber; Model B remains Desktop's), duty-cycle seats are moving to LaunchAgent cadence, the PM mailbox was retired (10-03), deploys no longer wait on PM approval (09-11). The section below is banner-marked accordingly.

**Verified how (v19.0).** Method: read this document in full; read `../beta-gate-standard.md` (headers, ledger and the 10-10 correction note), `../release-model.md` (header and §2), `docs/briefing/BRIEFING-CURRENT-STATE.md` (last_updated 2026-10-09); scanned `decisions.log` headlines 2026-07-17 → 2026-10-09 and read the dated rulings quoted above in full; ran `scripts/sprint-truth.py` and `scripts/ppm-criteria-line.sh` and `gh api repos/mediajunkie/piper-morgan-product/milestones` on 2026-10-10 ~05:20 PDT. Layer: the tracker, the ledger and the decision record, plus one live GitHub read. Not a probe of the running alpha or of any issue's closing evidence. Denominator: the decisions.log headline scan covered 2026-07-17 → 2026-10-09, not every entry in full; only the dated rulings cited here were read in full; Lead's and Arch's Phase 3 figures are quoted, not re-measured; the v18.x narrative sections below are carried, not re-audited.

---

## Executive Summary `[PM EYE — through-line emphasis is your call]`
> **[HISTORICAL — frozen May 30, 2026]** This summary describes the v17 interval (May 10 to May 30, 2026): the platform-laps reframe, PDR-005 v0.5, the V2 duty cycle, M2g. Retained for provenance; superseded for current state by *Current Position* above and the sources named in the header. Do not quote as current.


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
## Current Position (October 26, 2026)

**The gate.** Beta ships when the **MVP milestone closes**. The milestone is the gate list and nothing else is (`../beta-gate-standard.md`, PM-ratified 2026-10-05).
- The milestone endpoint read **3 open** (#2018, #1595, #1386) and 1,284 closed at 2026-10-26 10:3x PDT. `gh issue list --milestone MVP` agrees.
- No must-close has remained since #2132 closed served on 10-23 at 18:32.
- #2018 and #1595 are named in the invitation's known issues. #1386 is the close-out.
- A closure means a served answer someone can quote, not green tests.

**The invitation and the dates.**
- Invitations go at a time xian picks, any time after #2132 closed (decisions.log 10-23 16:57). xian calls them alpha invitations.
- The Terms page wording was ruled on 10-25 (Call A1), and the letter pieces were readied by Comms and HOST.
- The baseline dates are unchanged in the ledger: **design partners Fri 10-23, hard stop Fri 10-30**. The MVP milestone's `due_on` is also 10-30.
- Slips live in `../beta-gate-standard.md`. Only PM moves a date; PPM proposes none.

**What each gate promises** (`docs/internal/product/promises.yaml`, ratified 10-25):

| Gate | Promises |
|---|---|
| Private beta | E4 ("It never lies, and it degrades honestly") and the eight Terms paragraphs, T1 to T8 |
| Public beta | E6 (surfaces, per ESSENCE v1.1) and the five Readiness items, R1 to R5 (backups and restore, in-product delete, export, support loop, incident notice) |
| 1.0 | E1, E2, E3, E5 and E7 (E7 is gated by the Colleague Test, not by issues) |

- **1.0 is measured by the map's headline:** "N of 5 1.0 promises have a closed issue", with main's CI state. It reads **0 of 5** on 10-26.

**Production** (xian's rulings 10-24 17:28):
- **Sprints in closing order:** H → D → PUB → C → V → E, then T, Doc, Dist, Readiness and Q.
- **Size:** 203 issues open, on both `gh` and the 10-26 board snapshot. The 1.0 cut is the promise register, not the milestone. Non-promise work goes to Ongoing or the non-gating Q lane.
- **Dependencies:** recorded as GitHub's native blocked-by relationship, since 10-25. A backward edge (#1706 in PUB, blocked by #1441 in C) is with Exec as a Sprint question.
- **Public beta** opens by waitlist after the inner circle, and needs the Readiness lane closed and the MCP surface complete (ESSENCE v1.1).
- **The map** is `../production-map.html`, also published as a private artifact Exec carries on xian's rollup.

**Where it runs.**
- Alpha is the Fly app `piper-morgan` and is also the production instance (ruling 1). It served `69d859ca5f` on 10-26, promoted at 07:06 under the standing promotion grant (`docs/internal/operations/alpha-promotion-standing-grant.md`).
- Staging (`piper-morgan-staging`) holds synthetic data only.
- The latest tag is v0.8.14.0, and 0.9.0 is reserved for the beta.
- **Do not cite `origin/production`**: it no longer exists.

**What this section no longer claims** (all true on 10-10, superseded since):
- "14 open in the gate" (now 3).
- The Wed 10-14 tripwire. PM ruled Option 1 plus Option 3 on 10-14; see the ledger.
- "MCP/plugin is not a gate surface": its completion now gates public beta.
- "1.0 needs the Production milestone closed in full": 1.0 is now the promise register.
- "185 open in Production."


Differentiator stack: pillars 1-2 (Context Methodology, Conscious Floor) operate at the floor, pillar 3 (Artifact Persistence) shipped in M3; pillar 4 (Trust-Graduated Experience) is not built and has an open product question (see the stack section). The first-contact criterion (ratified 2026-08-15), the surfaces taxonomy v1.0 (08-21) and the FTUX experience model (08-21) are the design-side anchors for what a tester sees first.

---

## The Differentiator Stack (Vision V2.3 — Stable)

Four differentiators that, together, make Piper a colleague rather than a chatbot wrapper:

1. **Context Methodology** — Five-layer model operationalized as practiced discipline
2. **Conscious Floor** — LLM responses embodying grammar, Five Pillars, anti-flattening + Investment-pillar extension (#950 v0.1 May)
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with composting lifecycle (M3 territory)
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value (was M4 territory; **M4 TRIAGE CLOSED Jul 5, 2026** — the sprint was swept, its proactive-presence issue **#1174 moved to the Production milestone**, and the capability has **no implementation today**. See §M4 below.)
   > 🔴 **This differentiator needs a product decision before it can be built at all** *(PPM, 2026-08-01)*. Three facts that were tracked separately and are one problem:
   > 1. It is **differentiator 4 of 4** in a stack whose own framing is *"four differentiators that, together, make Piper a colleague rather than a chatbot wrapper."*
   > 2. It has **zero implementation** — no monitoring loop, no change detection, no salience judgment, no interruption-ethics surface (Arch, from the import graph).
   > 3. Its **specified mechanism is PDR-002's trust gradient, denominated in interactions** (~10 → Stage 2, ~50 → Stage 3) — which assumes **Piper owns the surface and can count them.**
   >
   > **Under PDR-006 (ratified 2026-07-31) we do not own the surface.** The user is inside Claude or ChatGPT; the host LLM decides when to call us and may invoke several tools in one user turn, or none. **So the denominator PDR-002 specifies does not exist on the primary distribution surface.**
   >
   > ⚠️ **Stated precisely, because the overclaim is tempting**: this is *not* "trust graduation is impossible." Alternative denominators are available — tool invocations, sessions, elapsed days. **But choosing one is a product decision nobody has made**, and until it is made, differentiator #4 is unbuildable *as specified*, not merely unbuilt. **The prior question is: what does "earned" mean when you cannot count the thing trust was denominated in?**
   >
   > **Not a beta blocker** — first contact is Stage 1 however you count, and a cold account starts there. It bites at **stage transitions**. Carried in **#1174**'s discovery scope (CXO owns); recorded against **PDR-002**'s trust-gradient table as an open question. **Material to PM's pending choice among the three #1174 options** — it raises the cost of "fund L4" specifically, since the mechanism would need respecifying first.

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
> **[HISTORICAL — frozen May 30, 2026 (July 5 triage notes)]** The M0-M5 / RECONNECT / D1 sprint narrative below is the May 30 picture with July 4-5 triage notes layered on. The M-sprint model no longer organizes the work: the open MVP milestone is the gate and Production is organized by the PROD-* and `PUB - Public Beta` sprints. The 'beta ships when the Beta Blockers sprint clears' and 'Aug 1 / Oct 30' statements inside this section are superseded. Retained for provenance; superseded for current state by *Current Position* above and the sources named in the header. Do not quote as current.


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

All 16 open M4-sprint issues reviewed Jul 4-5: 15 moved to Production milestone as enhancements/infrastructure/scoping work not required to gate beta (#302, #558, #712, #713, #954, #955, #956, #1062, #1166, #1174, #1217, #1242, #1244, #1245, #1326), and #1190 (destructive-mutation confirmation gate) also confirmed Production once the GitHub-write investigation showed it's a narrow UX-polish item, unrelated to credential routing. **#1032** (push-insight trust-gating) is already CLOSED, separate from this sweep. **#1216** (honest-provenance data model, `source`/`is_seed` on `InsightDB`) — ✅ **CLOSED COMPLETED 2026-07-07, milestone MVP** *(corrected by PPM 2026-08-06)*. ⚠️ **This line claimed for a month that it "remains OPEN" and was a "Beta Blocker candidate pending PM's call."** It was neither by the time anyone read it: landing in MVP means it was treated as beta-gating, so **the call I was waiting on had already been made by action rather than by answer** — and I kept carrying it as PM-gated. Its failure shape (confidently claiming seed data is real) does parallel #1331, and that reading stands. It was correctly NOT part of the M4 sprint triage (no matching Sprint-field tag).

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
> **[HISTORICAL — frozen May 30, 2026]** Written for the v17 interval. Since then: the cohort migrated to Amber (2026-07-25), where Model A (a stable per-agent worktree on `claude/{role}-cycle`) is the current model and Model B (Desktop's ephemeral auto-worktree) applies only on Desktop; the 'Model A DEPRECATED June 12' line below is true only for Desktop. Seats are moving from session cron to LaunchAgent cadence; the fire is a wake, not a time-box (PM 06-15 and 10-08); the PM mailbox was retired (10-03). Current rules: `CLAUDE.md` and `.claude/skills/duty-cycle-tick/SKILL.md`. The adoption-status list below (7 cycling, 4 cleared) is the May count. Retained for provenance; superseded for current state by *Current Position* above and the sources named in the header. Do not quote as current.


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
> **[HISTORICAL — frozen June 3, 2026]** Packaging notes from June 3. Since then: PDR-006 (07-31) and PM's 10-05 rulings (R7, bring-your-own-key) reshape the surface story. MCP/plugin is a post-MVP-close probe, BYOC/local is not ruled as a beta surface, and the hosted web UI is the required beta surface. The plugin-as-package sequence below is PA's build ladder, not a beta commitment. Retained for provenance; superseded for current state by *Current Position* above and the sources named in the header. Do not quote as current.


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
| **Dreams** (memory consolidation primitives) | methodology-27 Type 2 Dreaming + Pattern-070 Cleanup-Job + memory-files structure | **Converged 2026-06-08** (#1166, CXO+PPM+Arch three-way): roadmap YES → discovery-spike (not build) → post-M3 → PDR opens on spike-convergence (PPM-owned). Spec-read is done, not pending — row corrected 2026-09-12. |
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

## Sprint Summary (October 10, 2026)

Completed sprints are carried as history. The **active gate is the open MVP milestone**, not a sprint; PM uses sprints on the project board, one sprint (Beta Blockers) remains in the MVP milestone, and "open in the MVP milestone" equals "open in that sprint" today. The milestone is the accepted source of truth for verification (PM 10-05). Sprint-field changes need PM's explicit word.

| Sprint / milestone | Theme | Status (2026-10-10) |
|--------|-------|--------|
| **M0 / M1 / M2 / M3** | Conversational Glue; MVP Foundation; Conscious Floor + Action Handlers; Artifact Persistence | ✅ CLOSED (Mar 4 / Apr 11 / Jun 3 / Jun 2026) |
| **RECONNECT WS-1 / D1** | Connector refactor foundation; beta design quality | ✅ CLOSED (Jun 22, v0.8.9 / Jun 20) |
| **M3-Quality / M3-Health / M3-Security / M4 / M5 / RECONNECT (rest)** | Backlog sweeps | ✅ TRIAGE CLOSED Jul 4-5 (non-gate items moved to Production) |
| **Beta Blockers (MVP milestone)** | The gate | 🎯 **14 open** (`sprint-truth.py`); frozen-list rule, slip ledger at 4 slips / 0 days |
| **Epic 0 (#1595)** | Understanding-Layer Inversion spine; Phase 3 tail is gate scope | 🎯 ACTIVE; Phase 3 re-measure Mon 10-12 (Lead) |
| **PUB - Public Beta** | Front-loaded Production MCP-path cluster (#1462, #1458, #1509, #1688) | ⏳ Gates *public* beta, begins after MVP closes |
| **PROD-DIST / RECONNECT / TRUST / DOCS / DESIGN / ONBOARD / INFRA / TECHDEBT** | Production sprint structure (Jul 5, v18.6) | ⏳ Production milestone: 185 open, 41 closed |
| **Fast Follow** | Post-Production items (Slack moved here 08-27/28) | ⏳ 49 open, 1 closed |
| **Dot Releases** | Post-MVP point releases | ⏳ 7 open, 1 closed |
| **Enterprise** | Enterprise | ⏳ 14 open, 0 closed |
| **Ongoing** | Process, flywheel and tooling (no gate) | ♻️ 37 open, 143 closed |

*Milestone counts are the GitHub milestone endpoint on 2026-10-10 ~05:20 PDT; the MVP row is from `scripts/sprint-truth.py`. Sprint membership beyond the MVP row was not re-read for this fold. The PROD-* sprint names are from the v18.6 changelog (July 12) and were not re-verified against the board.*


---

## Timeline (Inchworm, Not Calendar — Sequence Statements, Not Deadlines)

**These are sequence statements, plus the dates PM has actually set. We are time lords.** Milestone closure gates audience, not the calendar (`../release-model.md`); the dates below are PM's targets for when the gate is expected to be measured clear.

### Recent (July–October 2026), from `decisions.log` headlines

- [x] Jul 16: Production 1.0 four-connector gate defined; Finish-the-Unfinished sprint ratified (epic #1424)
- [x] Jul 25: cohort moved to Amber (shared memory pool; Model A worktrees on Amber)
- [x] Jul 31: PDR-006 ratified (host-LLM-owns-the-surface distribution consequence)
- [x] Aug 8: beta date moved back a month (PM); fundamentals-first priority ruling; Understanding-Layer Inversion proposal
- [x] Aug 15: first-contact criterion ratified; spatial cold-island disposal
- [x] Aug 21: surfaces taxonomy v1.0; FTUX experience model
- [x] Aug 29: Understanding-Layer Inversion sequencing and Reorientation Plan v1.0 ratified; Epic 0 (#1595) is the current epic
- [x] Aug 30: ESSENCE v1.0 (seventh commitment); release model written; calendar deferred from MVP with a positioning correction; #1688 moved to Production-front
- [x] Aug 31: #1613 cross-user pooling severed and purged
- [x] Sep 6: milestone dates reset by PM (see forward sequence)
- [x] Sep 22-29: Fly cutover, droplet destroyed, `origin/production` deleted
- [x] Oct 5: frozen beta-gate standard ratified; slip rule confirmed; bring-your-own-key YES; R7 per-surface ruling; measured gate pass of 31 of 31 open MVP issues
- [x] Oct 6: PM triage rulings, gate sorted to 14; ADR-080 accepted; `Owner:` line convention (Decision D)
- [x] Oct 8: one credential resolver per connector (#1965 admitted to the gate)
- [x] Oct 9: PM held design partners Fri 10-23 and hard stop Fri 10-30; scoring run approved

### Forward sequence (dates are PM's; ordering is the release model's)

- **Mon 10-12**: Lead's Epic 0 Phase 3 re-measure; PPM files the resolution row in the slip ledger.
- **Wed 10-14**: tripwire check. If the Epic 0 evidence tranche is not done, or the gate list has grown again, PPM brings the choice back to PM the same day via Exec. *(Weekday is PPM's inference from the date 10-14 PPM proposed on 10-04; PM named no day. Corrected from "Tue" on 10-10 after Janus's date check; it was a label error, not a slip.)*
- **Fri 10-23**: design partners (held by PM 10-09), conditional on the unknowns named in `../beta-gate-pass-2026-10-05.md`.
- **Fri 10-30**: hard stop, and the MVP milestone's `due_on`. **MVP closure ends alpha and starts invitation-only private beta (v0.9.0) at beta.pipermorgan.ai; Production-milestone work begins.** Outside users enter after closure, dated by the gate measurement (Spec R1 as Exec recommended, PM 10-05).
- **During beta**: MCP/plugin probe released and tested (PA); the front-loaded PUB cluster proceeds. **Public beta** requires the MCP path complete (#1462, #1458, #1509, #1688).
- **Production milestone, 1.0/GA: Feb 2, 2027** (GitHub `due_on` 2027-02-02; PM's 09-06 message said "2026", which Exec flagged as almost certainly 2027, and GitHub now carries 2027). Needs the milestone closed in full.
- **Fast Follow: May 8, 2027. Dot Releases: Sep 2, 2027.** (GitHub `due_on`, matching PM's 09-06 reset.)
- **Enterprise: Oct 30, 2028** (GitHub `due_on` 2028-10-30; PM's answer 2026-10-12, relayed by Exec: "Enterprise was moved to 2028 as a theoretical possibility. On the current plan we are still doing dot releases through 9/2027 at least and there may never be demand for Enterprise features." The 09-06 decisions.log line reading 2027-10-30 is the error; correction appended to decisions.log).
- PDR-005 v1.0 ratification and the BYOC ADRs (Q6/Q7) remain open from the v17 interval; BYOC/local is not ruled as a beta surface.

### Historical: May-June 2026



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

- **v19.0 (October 10, 2026)**: Full fold of #1644's open half (PPM). v18.10 archived whole at `../historical/roadmap-v18.10-2026-10-10.md`. New header and v19 changelog; *Current Position*, *Sprint Summary* and *Timeline* rewritten against the frozen beta-gate standard, the release model, `sprint-truth.py`, live GitHub milestones and the decisions.log record since July 16; Executive Summary, MVP Sprint Status, Autonomous Operations and Distribution Strategy banner-marked historical (frozen May 30 / June 3 state, not rewritten). Methodology, Platform-Laps and Differentiator sections carried unchanged (differentiator-4 note from 08-01 retained). One discrepancy flagged, not resolved: the Enterprise milestone `due_on`. The v18.6-v18.10 changelog entries lived in the v18 header and are retained verbatim only in the archive; the v18.1-v18.5 entries below are carried as they were.
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

*v19.0 — PPM 2026-10-10. Canonical `roadmap.md`. Gate: the open MVP milestone (`../beta-gate-standard.md`); audience model: `../release-model.md`; live counts: `scripts/sprint-truth.py`. Prior state: `../historical/roadmap-v18.10-2026-10-10.md`.*
