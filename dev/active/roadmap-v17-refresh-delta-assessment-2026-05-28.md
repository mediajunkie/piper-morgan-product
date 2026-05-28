# Roadmap v16.0 → v17 Refresh — Delta Assessment (#1128)

**Author**: PPM (duty-cycle Fire-0 Task Loop)
**Date**: 2026-05-28
**Purpose**: scope the v17 roadmap refresh by cataloging the May 10 → May 28 deltas roadmap.md (currently v16.0, 18 days stale) must capture. First step of #1128 ROADMAP-REFRESH; v17 draft follows from this assessment.
**Swap precedent**: per v15→v16 (May 10) — PPM drafts v17 in dev/active → Docs swaps into canonical roadmap.md after CEO ratification.

---

## What v16.0 (May 10) says vs. what's now true

### Deltas to capture in v17

**1. BYOC: "active discovery" → PDR-005 v0.5 with full decision-rule + architecture + experience sections**
- v16.0: "BYOC distribution model now in active discovery — PDR-005 scoping outline distributed May 4; eventual ADR slot TBD"
- Now: PDR-005 v0.5 (May 19) — all decision-rule sections complete; Architect §architecture fill-in (AC-1→AC-4); CXO §experience fill-in (EC-1→EC-5 + identity coherence framework); companion ADRs Q6/Q7 queued in Architect's lane; ADR altitude resolved (PDR foundational, ADRs implementation — HOST 360 item 1.3 closed). v1.0 path: cohort flag-back on EC-2 + Comms external frame + PM ratification.

**2. V2 Autonomous Duty Cycle — entirely new since v16.0**
- Not in v16.0 at all.
- Now: V1 Duty Cycle designed (CIO) → retired (PM May 21 pivot) → V2/v0.6.x design ratified → Phase D cohort rollout (all 10 roles adopting; PPM final-wave May 28). Major methodology/operations addition. cron-bind-to-IDLE + drain-until-IDLE + 0th-step + idle-advance semantics.

**3. MUX/UI cohort + Phase 2 build — new since v16.0**
- Not in v16.0.
- Now: MUX/UI 7-surface cohort scoping (Round 1 + Round 2 CEO-ratified May 16); integration pick GitHub+Calendar+Notion (Slack deferred); ADR-062/063/064 landed; Phase 2.1 (Surfaces 1+7) + 2.2 (Surfaces 2+4, PPM-signal-unblocked) + 2.3 (Surface 6) build lanes; offer-first cluster MUX docs (2/4/7) at v0.2 voice-pass lock.

**4. Anthropic platform-laps reframe — new strategic frame**
- Not in v16.0.
- Now: Anthropic shipped Outcomes (May 6) / Dreams / Multi-Agent / Webhooks; PM "platform laps you = value-chain climbing" reframe; CIO platform-productization disposition (May 18); PA-leads + CIO-co-author Outcomes investigation (started May 25); "Platform Lapped Us, We Climbed" Ship spine candidate.

**5. Methodology corpus: 5+ landings → 34+ entries**
- v16.0: "5+ landings since Apr 26"
- Now: methodology-29 (Pattern Formation via Successful Imitation) through methodology-34 (Cohort-Discipline as Moat candidate); Pattern-070 (Cleanup-Job) / 071 (audit-as-attack-surface) / 073 (Documentation-Asserted-Behavior Drift, promoted Emerging→Proven). doc-sync-sweep skill. methodology-to-runtime latency now sub-daily.

**6. M2 progression: M2f gated → M2g closure tail**
- v16.0: "M2f gated on canonical-retest baseline (met May 9)"
- Now: M2f closed; M2g closure tail in progress; #1089 KG-Privacy-Filter Phase 0 (PM-ratified ship-now May 20); MEM-* cluster work.

**7. Ships #043 + #044 published/in-flight**
- v16.0: through Ship #042 era.
- Now: Ship #043 published (May 20, "What Was Working Got Written Down" era + fab-catch recovery arc); Ship #044 workstream-review cycle in flight (May 15-21 window; six memos including PPM filed May 24).

**8. Colleague Test v2.4 + UI Lifecycle Rubric progression**
- v16.0: "Colleague Test v2.0 → v2.4 (in flight)"
- Now: CT v2.4 in use; CT v2.5 identity-coherence sub-dimension proposed (PDR-005 EC work); rubric recalibration cycle.

---

## v17 structure recommendation

Keep v16.0's structure (Executive Summary + Current Position + MVP Sprint Status + Roadmap Refresh Cadence). Update:

- **Executive Summary**: lead with the platform-laps-value-chain-climbing strategic frame + PDR-005-near-ratification + V2 Duty Cycle as the operational-autonomy milestone
- **Current Position**: M2f closed → M2g tail; MUX/UI Phase 2 build in flight; PDR-005 v0.5→v1.0 path
- **MVP Sprint Status**: M2g + MUX/UI surfaces + BYOC 1.0 scope (the 5 1.0-required surfaces + 3 integrations)
- **New section: Autonomous Operations** (V2 Duty Cycle — the cohort-wide operational-autonomy capability)
- **Refresh cadence**: retain hybrid (trigger-based + workstream-review-line-item + chesterton's-fence weekly docs audit); note the duty-cycle idle-advance now also surfaces roadmap staleness

---

## Status + next step

- **Delta-assessment**: COMPLETE (this doc) — Fire-0 Task Loop forward-progress on #1128
- **v17 draft**: NEXT (next fire or dedicated effort) — draft roadmap v17 in dev/active from this assessment, then Docs swap + CEO ratification per v15→v16 precedent
- **#1128 status**: in-progress (assessment done; draft pending) — updated in `ppm-standing-items.md`

---

*#1128 ROADMAP-REFRESH delta-assessment | PPM duty-cycle Fire-0 | 2026-05-28*
