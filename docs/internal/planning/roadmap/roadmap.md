# Piper Morgan Roadmap v16.0

**Date**: May 10, 2026
**Author**: PPM, with leadership review (PA, CXO, CIO, Architect, Lead Developer)
**Status**: Active. Adopted May 10, 2026 (CEO ratified). M2 sub-epics M2a/b/c/d-MVP closed; M2e dispositions walked; M2f gated on canonical-retest baseline (met May 9).
**Supersedes**: v15.0 (April 11, 2026) — archived at `docs/internal/planning/historical/roadmap-v15.0-2026-04-11.md`

---

## Executive Summary

**M2 sub-epics M2a/b/c/d-MVP all CLOSED**; M2e gameplans walked May 3 with PM dispositions captured; M2f preceded by canonical-retest baseline gate (Run 5 May 9, 68.3% quality with v2.4-pending recalibration). **#992 ETHICS-ACTIVATE arc CLOSED end-to-end** (Phase A → Phase F flag-flip merged Apr 30 `deecc816`); **ADR-061 v1.0 ratified** May 4 (CEO verbal). **All seven leadership roles + Lead Dev now on Code** (migration arc complete Apr 26); post-migration parallel-velocity payoff demonstrated through April → May.

**Methodology-corpus compounding at sub-week cadence since Apr 26**: Methodology-24 (Branch-or-Anchor), Methodology-25 (Workstream Review Cadence), Pattern-063 (Parallel-Authoring Drift, Emerging), Pattern-064 (Extension Without Integration, Emerging), Pattern-065 (TBD candidate per CIO sweep), Colleague Test v2.0 → v2.4 (in flight), branched UI Lifecycle Verification Rubric v0.1, PPM Review Gates (5-class review surface, CEO-approved May 10), mailbox-discipline + sign-off discipline norms hook-enforced in CLAUDE.md. **Methodology-to-runtime latency now hours-to-days, not weeks**.

**BYOC distribution model now in active discovery** — PDR-005 scoping outline distributed May 4 to PA + Architect + CXO; eventual ADR slot TBD when Architect files (paired-document approach per PDR-001/ADR-060 precedent). HOST 360 cohort surfacing identified BYOC as "the strongest decision-debt signal in the cohort" — discovery thread responds to the surfacing.

**Key changes from v15.0**:
- **M2 sub-epic gates operationalized** — M2a/b/c canonical-retest gates closed; M2d/e gates with conceptual-integrity checklist + UI Lifecycle Verification Rubric v0.1 + per-issue 2-of-3 sign-off protocol; M2f gated on canonical retest meeting/exceeding prior benchmarks
- **#992 ETHICS-ACTIVATE multi-step arc** (Phases A–F) shipped end-to-end with #1004 semantic detector + #1018 audit_transparency durability + ADR-061 codification
- **Calibration plan reframed** as three-phase (simulation harness → beta-traffic → stable) per CEO-named alpha catch-22 (Apr 30); simulation-first lands with Phase F flip
- **Methodology corpus expanded substantially** (5+ landings since Apr 26, all responsive to operational findings within hours-to-days)
- **PPM Review Gates** as new standing operating norm (5-class review surface; CC routing convention; fail-soft default with PA proxy)
- **Migration arc complete** — all seven leadership roles + Lead Dev on Code by Apr 26; post-migration parallel velocity demonstrated repeatedly through Apr 27 / Apr 28 / Apr 30 / May 2
- **PDR-005 (BYOC) discovery thread opened** — predecessor-flagged carry-forward fired per PM trigger invocation Apr 27; rate-limited then distributed May 4 (CEO authorized post-Ship-#040 inflection)

---

## Current Position

```
Inchworm Position: 4.4.4 (M2 sub-epics advancing; M2d MVP CLOSED; M2e in detailed gameplan)

1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.5.1)
4. 🎯 Complete build of MVP
   4.1. ✅ B1 - Beta Enablers (v0.8.3.x) - COMPLETE Jan 11
   4.2. ✅ A20 - Alpha Testing round 2 (v0.8.4.x) - COMPLETE Jan 18
   4.3. ✅ MUX: Modeled User Experience - COMPLETE Jan 27
   4.4. 🎯 MVP Sprints (M0 → M5) ← CURRENT
        ✅ M0: Conversational Glue — COMPLETE (v0.8.6, Mar 4)
        ✅ M1: Foundation — COMPLETE (gate closed Apr 11, 7/9 Gate 1 PASS)
        🎯 M2: Conscious Floor + Action Handlers ← MID-SPRINT
            ✅ M2a Foundation cleanup
            ✅ M2b Test infrastructure
            ✅ M2c Conversational depth (72.1% quality, post-#950 iter 2)
            ✅ M2d MUX Lifecycle MVP CLOSED end-of-day May 3
            🎯 M2e Integrations (gameplans walked May 3; #790 already shipped; #869/#900/#1039/#1040 pending)
            ○ M2f Security + Infrastructure (gated on canonical-retest baseline)
        ○ M3: Artifact Persistence (post-MVP-related issues filed during M2 walkthrough surface as M3 candidates; not yet scoped)
        ○ M4: Trust + Learning
        ○ M5: Distribution + Polish (BYOC discovery thread in flight)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## The Differentiator Stack (Vision V2.3 — Stable)

The MVP sprints are organized around four differentiators that, together, make Piper a colleague rather than a chatbot wrapper:

1. **Context Methodology** — Five-layer model operationalized as practiced discipline
2. **Conscious Floor** — LLM responses embodying grammar, Five Pillars, anti-flattening + Investment-pillar extension (#950 v0.1, May)
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with composting lifecycle (M3 territory)
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value (M4 territory)

Indoor plumbing (commodity, not differentiating): GitHub/Slack/Calendar/Notion via MCP plugins, file storage via SQLite + PostgreSQL audit_log persistence, auth via standard OAuth, LLM provider management via three-way fallback chain (Anthropic → Gemini → OpenAI).

---

## MVP Sprint Status (May 10, 2026)

### M0 — Conversational Glue ✅ COMPLETE (v0.8.6 Mar 4)

27 issues (5 planned + 22 discovered via Assembly Assumption — the canonical Pattern-062 instance).

### M1 — MVP Foundation ✅ COMPLETE (Apr 11)

Gate 1 7/9 PASS. ADR-060 (Floor-First Routing), ADR-059 (Workflow Dispatcher), PDR-004 (Experience Philosophy). Conversation continuity (#922) folded into M2.

### M2 — Conscious Floor + Action Handlers 🎯 MID-SPRINT

**Theme**: Make the conscious floor reliable and the action gate clean. Differentiator-stack pillars 1–2 become operational.

#### M2a Foundation cleanup ✅ COMPLETE (Apr 11–14)

10/10 issues closed. Floor inversion complete for all read-only categories. Canonical retest run 3 (Apr 13): 93.4% routing, 62.3% quality.

#### M2b Test infrastructure ✅ COMPLETE (Apr 14–15)

5/5 issues closed. E2E + AAXT + CI integrated. Canonical retest automated.

#### M2c Conversational depth ✅ COMPLETE (Apr 16)

#950 (Five Pillars + grammar + anti-flattening + Identity anchoring), #951 (calendar + deadline context), #964 (ethics verification — surfaced #1002+#1003+#1004). Canonical retest run 5 post-#950 iter 2: **72.1% quality PASS**, 95.1% routing.

#### M2d MUX Lifecycle MVP ✅ CLOSED (end-of-day May 3)

8 implementation issues shipped (#704/#714/#1030/#1031/#1032/#1033 + pre-work #1034/#1035; #1036 closed premise-invalid). May 2 audit-cascade restructure surfaced flattening risks; conceptual-integrity gate added to m2-structure.md; **UI Lifecycle Verification Rubric v0.1 branched per Methodology-24** (May 10) for per-issue gate-close protocol.

#### M2e Integrations 🎯 GAMEPLANS WALKED (May 3)

PM dispositions captured: #790 already shipped; #869 relocated from M2d (audit-cascade ✅); #900 (LLM-gated completion in MVP per Q2, ~14h est); #1039/#1040 (split from #864, #1039 blocked by #1042 PRE-1039 cleanup); #1041 M2-WIRE-TRIAGE (resolves WIRE-* ambiguity that was previously a footnote).

**Followup issues filed during M2e walkthrough**: #1043 POST-MVP en-masse copy review; #1044 FOLLOWUP local-git query handler; #1045 POST-MVP Project Detail Activity tab.

#### M2f Security + Infrastructure (gated)

Per CEO directive: M2f doesn't open until canonical retest meets/exceeds prior benchmarks. Run 5 (May 9) baseline at 68.3% with v2.4-pending recalibration; v2.4 (C=0 disambiguation per CXO May 10 memo) is the durable fix; (b) interim 2-dim auto-fail threshold is in force as the recalibration Lead Dev shipped May 9. M2f opens once Run 5+ meets the M2c 72.1% benchmark.

Items per v15.0 stay; gate methodology is canonical-retest-baseline.

---

### M3 — Artifact Persistence (post-MVP-related candidates surfacing)

Theme + scope unchanged from v15.0. Post-MVP-related issues filed during M2 walkthrough surface as M3 candidates — #1037, #1043, #1045, #1046 (most filed during M2d/M2e walkthroughs) are M3-shaped artifact-persistence-adjacent work to be triaged at M2 closure.

Composting data model designed in M3; composting engine deferred to M4.

---

### M4 — Trust + Learning

Theme + scope unchanged from v15.0.

**Trust graduation MVP must be credible first step toward full model, not throwaway hack** (PM emphasis from v15.0 — still load-bearing). #1032 Push-insight trust-stage gating (Stage 3+) is the first concrete trust-gated UX surface; the trust thresholds it depends on are M4 territory.

---

### M5 — Distribution + Polish

Theme + scope unchanged from v15.0.

**BYOC discovery thread now in flight** (PDR-005 scoping outline distributed May 4 to PA + Architect + CXO):
- PA cross-pollination scan (Klatch / Janus / Vergil / Piper Open) — at PA bandwidth
- Architect feasibility check (most-ambitious-version BYOC; folding into LLM-touch lens #1016 Phase 4 per Architect May 4) — at Architect bandwidth
- CXO experience review (voice portability + identity coherence + boundary handling under BYOC) — first-draft routing within 2-3 weeks per CXO May 10 ack
- PPM drafts PDR-005 after the three above land
- Architect drafts the eventual BYOC ADR (slot TBD when filed; was provisionally "ADR-061" in HOST 360 framing but ADR-061 slot used for LLM-touch boundary enforcement instead)

---

## #992 ETHICS-ACTIVATE Arc — CLOSED (Apr 30)

Multi-step arc Phase A → B → C → D → E → #1002/#1003 → #1004 → Phase F. Six calendar days from initial S1 floor-bypass finding (Apr 25) to Phase F flag-flip merged (Apr 30 `deecc816`). #992 closed properly via skill (8/8 ACs marked + closing comment with full Phase F evidence).

**Key landings**:
- **Phase E gate scoring** (Apr 25-26): PPM 7/8/8 + CXO 9/9/9 = all PASS; convergence on PASS verdict, no PM tiebreak; identified #1002 (pre-classifier shadows ethics floor) + #1003 (harassment vector → GUIDANCE classification, BoundaryEnforcer not engaged)
- **#1004 BoundaryEnforcer semantic detector** shipped end-to-end Apr 27 in single Lead Dev session (Steps 5/6/7 overnight + Steps 8/9 Monday); 112/112 PASS full ethics enforcement suite
- **ADR-061 v1.0 LLM-Touch Boundary Enforcement** ratified May 4 (CEO verbal); two-layer detection architecture (literal-trigger fast-path + semantic detector); audit envelope with detector field, decision_tier, semantic_confidence, fast_path_hit, cache_hit, latency_ms
- **#1018 Phase 2 audit_transparency durability** SHIPPED May 2 (PostgreSQL-backed `ethics_audit_log` + `EthicsAuditRepository`); cluster regressions #1006/#1007/#1008 closed atomically
- **Phase F flag-flip MERGED** Apr 30 `deecc816`; `ENABLE_ETHICS_ENFORCEMENT=true` live in `docker-compose.yml`
- **Calibration reframe** (CEO catch-22 Apr 30): three-phase (simulation harness with Gemma generator → beta-traffic refinement → stable) replaces single-phase wait-for-real-traffic plan; simulation-first ships with the flip

---

## Methodology Corpus (compounding since Apr 26)

Methodology landings since v15.0 — all responsive to operational findings within hours-to-days:

### Patterns

- **Pattern-063 (Parallel-Authoring Drift)** — Emerging, filed Apr 27 (CIO `a5d82e82`). Two parallel-authored artifacts share vocabulary that drifts. Reference instance: Phase E rubric C=Clarity vs CT v2 C=Context Apr 26.
- **Pattern-064 (Extension Without Integration)** — Emerging, filed Apr 28 (Architect `35a1108c`). Sibling to Pattern-062/063; extension-layer manifestation. Reference instance: BoundaryEnforcer #197 substring detector recall gap.
- **Pattern-065 (candidate per CIO Pattern Sweep 2.0 May 9)** — TBD slot allocation; awaiting CIO recommendation.

### Methodologies

- **Methodology-24 (Branch-or-Anchor)** — filed Apr 27 (CIO `3bcd9eed`). When authoring a second rubric/framework/vocabulary that could share terminology with an existing one, explicitly choose to either branch (distinct vocabulary) or anchor (declared strict descendant, no semantic drift allowed). Worked examples to date: CT v2.3 §"How to Extend This Rubric"; UI Lifecycle Verification Rubric v0.1 (May 10 PPM-authored, branched per Architect/Lead/CXO concur).
- **Methodology-25 (Workstream Review Cadence)** — filed Apr 27 (CIO `3bcd9eed`). Fri–Thu most-recent-closed window, naming standard, source discipline (omnibus first as reading-order primary, source logs as authority — May 4 two-senses-of-primary clarification).

### Rubrics

- **Colleague Test v2.x trajectory** — v2.0 Apr 25 (PPM successor reconstruction from predecessor's handoff spec) → v2.1 Apr 26 (Tone-3 anchor sharpening from CXO Phase E countersign) → v2.2 (fresh-account ceiling clarification) → v2.3 Apr 27 (Branch-or-Anchor section embedded in §"How to Extend") → v2.4 (in flight: C=0 disambiguation per CXO May 10 memo, with `context_requirement` query tagging). Quarterly review cadence proposed (PPM concur May 10): joint CXO+PPM full-rubric retro per quarter; per-incident interim bumps continue per Methodology-24.
- **UI Lifecycle Verification Rubric v0.1** — May 10 (PPM-authored, branched from CT v2.3 per Methodology-24). Same dimension shapes (R/C/T 0-3, ≥7/9 PASS, single-dim auto-fail) with explicitly different meanings: R=Recognition (UI surfaces lifecycle state), C=Clarity (experience phrase comprehensible without technical knowledge), T=Tone (rendering carries Piper voice into UI). Provenance: deliberate branch per Methodology-24; CT v2.3 §"How to Extend" cites as canonical worked example.

### Discipline Norms (CLAUDE.md-codified)

- **Mailbox discipline** (Apr 26) — `mailboxes/` writes commit to `main` only; `check-branch.sh` hook enforces; per-memo commit-and-push norm
- **Sign-off discipline** (Apr 28) — three-command checklist before session close; Docs merge-keeper sweep as standing safety net
- **PPM Review Gates** (CEO-approved May 10) — 5-class review surface (PDR-adjacent / sub-epic gate / quality-threshold-affecting / integration-pattern-shifting / user-facing-experience-with-PPM-implications); CC PPM on originating memo or `needs-ppm-review:` prefixed memo to ppm/inbox; PPM acks within one PPM session; fail-soft via PA proxy on >2-session unavailability. **Class B (sub-epic gate) carries the Interface-Verification DoD (Layer A, #683)** — methodology-30 Consumer-Trace required at gate-close for any AC asserting a consumer-relationship (PM-ratified placement May 30; full def `docs/internal/development/interface-verification-dod-layer-a.md`; completion-criteria home `m2-structure.md` §Sub-Epic Gating Protocol item 5).
- **Branch-or-anchor extension discipline** (CT v2.3 §"How to Extend") — apply at every rubric/vocabulary extension point; PPM authored the canonical worked-example-of-violation May 10 (UI rubric initially used CT framing → CXO caught the drift → PPM conceded → branched cleanly with provenance)

---

## Distribution Strategy: Bring Your Own Chat (Discovery in Flight)

**Build sequence (Gall's Law) — unchanged from v15.0**:
1. MCP server — standalone, runs via stdio transport
2. MCPB packaging — bundle for Claude Desktop one-click install
3. Claude Project template — persona/instructions for the hybrid approach
4. MCP Apps — interactive HTML for artifact canvas

**PDR-005 discovery thread opened May 4** (post-Ship-#040 publication inflection point). Six decision-rule questions in scoping outline; tier-placement question (PDR-005 Foundational vs PDR-201 Integration Patterns — PPM lean is foundational, CEO call); paired-document approach with eventual BYOC ADR (slot TBD when Architect files).

**HOST 360 cohort surfacing**: Architect §8.3 + PPM §8.3 independent convergence — "the strongest decision-debt signal in the cohort" (Apr 27).

**Build the server cleanly enough that the packaging layer is swappable** — anchor on the thin-wrapper-to-API model, not on MCP specifically.

---

## Methodology Maintenance (Per CIO + HOST + PPM observation)

Methodology-as-product is an asset only while it's a living practice. The mechanisms that keep it alive (v15.0 list + new since Apr 26):

**Per v15.0 (still operating)**:
- Trigger-based audit cadence (methodology audit within 2 weeks of each sprint gate closure)
- CIO self-approval authority for Emerging patterns
- Cross-pollination review as standing intelligence infrastructure
- Per-sprint quality gate with CXO authority

**New since v15.0**:
- Mailbox discipline + sign-off discipline norms hook-enforced
- Per-memo commit-and-push norm with explicit-paths staging
- Methodology-25 weekly workstream review cadence (Fri–Thu most-recent-closed)
- PPM Review Gates 5-class review surface (CEO-approved May 10)
- CT v2.x quarterly review cadence (proposed May 10, ~mid-July first instance)
- Daily Docs merge-keeper sweep (Apr 28 standing)
- Roadmap freshness via hybrid trigger-based + workstream-review-line-item discipline (this v16 introduces; weekly docs audit retained per chesterton's fence)

These don't appear in the feature roadmap but are required for the differentiator stack to remain credible.

---

## Sprint Summary

| Sprint | Theme | Status |
|--------|-------|--------|
| **M0** | Conversational Glue | ✅ COMPLETE (v0.8.6, Mar 4) |
| **M1** | MVP Foundation | ✅ COMPLETE (gate closed Apr 11) |
| **M2** | Conscious Floor + Action Handlers | 🎯 MID-SPRINT (M2a/b/c/d-MVP closed; M2e gameplan; M2f gated) |
| **M3** | Artifact Persistence | — (post-MVP-related candidates surfacing) |
| **M4** | Trust + Learning | — (#1032 Push-insight trust-gating is first concrete touch surface) |
| **M5** | Distribution + Polish | — (BYOC PDR-005 discovery thread in flight) |

---

## Timeline (Inchworm, Not Calendar — Sequence Statements, Not Deadlines)

**These are sequence statements. We are time lords. Each phase complete before the next begins.**

### Recent (April–May 2026)

- [x] M1 gate closure (Apr 11)
- [x] M2a/b/c sub-epic closures (Apr 14, Apr 15, Apr 16)
- [x] IAC presentation (Apr 17, Philadelphia, "Ethics as Information Architecture")
- [x] All-leadership Code migration arc (Apr 22-26; HOST → CIO + Comms → CXO + PPM → Architect → Exec)
- [x] #992 ETHICS-ACTIVATE arc (Apr 25 → Apr 30; Phase F merged `deecc816`; #992 closed)
- [x] M2d MUX Lifecycle MVP (closed end-of-day May 3)
- [x] M2e gameplans walked (May 3, dispositions captured)
- [x] ADR-061 v1.0 ratified (May 4 CEO verbal)
- [x] Ship #040 publication (Apr 29 "The Methodology Audits Itself")
- [x] PPM Review Gates CEO-approved (May 10)

### Estimated forward sequence

- M2e build (~2-4 weeks given walked gameplans + #790 already shipped)
- M2f open once canonical-retest baseline meets/exceeds 72.1% quality (Run 5 at 68.3% with v2.4-pending recalibration; (b) interim ships first then v2.4 durable fix)
- BYOC PDR-005 drafting (~3-6 weeks: 2-3 weeks for PA/Architect/CXO discovery inputs + 1-2 weeks PPM PDR drafting + 1 week leadership review)
- M3 (Artifact Persistence): scope sharpening at M2 closure
- M4 (Trust + Learning): scope sharpening at M3 closure
- M5 (Distribution + Polish): BYOC PDR + ADR ratification gates the build sequence
- Beta via MCPB → v1.0

---

## Closures and Revisions Since v15.0

- **#992 ETHICS-ACTIVATE** (Apr 30) — multi-step arc closed via Phase F flag-flip
- **#1002, #1003, #1004** (Apr 27) — Phase E findings + semantic detector ship
- **#1018, #1006, #1007, #1008** (May 2) — audit_transparency cluster closed atomically
- **#948 orphan-task fix** (Apr 30)
- **#1012 dead-code sweep** (Apr 28)
- **#1013 /api/v1/ migration** (Apr 28)
- **#1014 AuthMiddleware exclude_paths refactor** (Apr 29)
- **M2d MVP-scope** (May 3): #704/#714/#1030/#1031/#1032/#1033/#1034/#1035 shipped; #1036 closed premise-invalid
- **#864** (May 3) — split into #1039/#1040 (closed by replacement)

**Issues filed since v15.0** (selected — full list in git): #1002, #1003, #1004 (#992 arc); #1005-1008 (audit_transparency cluster); #1011-1019 (Architect Phase 1 lens); #1027-1029 (dead-code follow-ups); #1030-1036 (M2d MUX restructure); #1037-1046 (M2d/M2e walkthrough followups); #1049 (weekly docs audit); #1064 (rubric recalibration trigger).

---

## Roadmap Refresh Cadence (New, per Docs May 4 proposal + chesterton's-fence preservation)

**Hybrid mechanism** (per PPM+CEO May 10):

1. **Trigger-based** — refresh within 2 weeks of any sub-epic closure or major artifact landing (PDR ratification, ADR v1.0 ratification, multi-step arc closure). The natural cadence for product-roadmap deltas.
2. **Workstream-review-line-item** — PPM compiles M2/M3 deltas as part of the workstream memo to Exec; the writeup itself becomes the source for the roadmap edit.
3. **Weekly docs audit retained per chesterton's fence** — Docs's standing weekly audit continues as backstop; surfaces staleness if hybrid mechanism above misses something.
4. **Session-start hook** — future enhancement (lower priority); PPM session-start could show roadmap last-updated days alongside briefing staleness counter. Not gating the hybrid above.

---

## Change Log

- **v16.0 (May 10, 2026)**: Major refresh covering Apr 11 → May 10 substantive deltas. M2 sub-epic restructure (M2a/b/c/d-MVP closed; M2e gameplans walked; M2f gated). #992 ETHICS-ACTIVATE arc closed end-to-end. Methodology corpus expansion (Pattern-063/064/065-candidate, Methodology-24/25, CT v2.x trajectory, UI Lifecycle Verification Rubric, PPM Review Gates, mailbox + sign-off discipline norms). BYOC PDR-005 discovery thread in flight. All-leadership Code migration arc complete. New roadmap-refresh cadence (hybrid + chesterton's-fence retention of weekly docs audit).
- **v15.0 (April 11, 2026)**: Major restructure post-M1 closure. Sprints reorganized around differentiator stack per Vision V2.3. 12 closures, 3 revisions, 10 new issues filed (#950-959), DIST integrated into M5. Leadership reviewed and endorsed (PPM, CXO, CIO, Architect). Build sequence and distribution strategy formalized. (Archived at `docs/internal/planning/historical/roadmap-v15.0-2026-04-11.md`.)
- **v14.3 (March 10, 2026)**: M0 marked complete, M1 cherry-picking documented. (Archived at `docs/internal/planning/historical/roadmap-v14.3-2026-03-10.md`.)
- Earlier versions: see archived historical roadmaps
