# PPM Standing Items — Task List (duty-cycle Task Loop source)

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "task list" per v0.6 architectural decision 1 (reframed standing-items tracker; no new doc). Task Loop drains this in priority order until all blocked-or-empty.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

---

## Active lane work (priority order)

| # | Item | Priority | Status | Unblocked? | Notes |
|---|---|---|---|---|---|
| 1 | **#1128 ROADMAP-REFRESH** | medium | **in-progress** | **partial** | roadmap.md stale. delta-assessment (5/28) → v17 draft (5/30, `00cee8d47`, distributed `15f8a05ae`) → **v18 draft (6/2, `roadmap-v18-draft-2026-06-02.md`): PA §M5/BYOC review ABSORBED** (Daedalus referent explicit; Outcomes date corrected; PoC PASSED-5/19 sharpened; Janus meta-coordinator line). **CIO §Methodology review ABSORBED 6/3** (corpus 29→37, patterns 62→74, methodology-as-operational-capability prose). **Both section reviews now in (PA + CIO) → v18 READY FOR PM RATIFICATION** (escalated to attention doc 6/3). Comms external-language frame = parallel polish (v18.1-able), not gating internal canonical. Next: PM ratifies → Docs swap → canonical `roadmap.md`. (Optional: re-render HTML on ratification.) |
| 2 | **#967 Backlog Deep Review — Surviving Edges** | low | open | YES | backlog tracking. PPM domain. PM-approved triage lane. |
| 3 | **PDR-005 v0.5 → v1.0 path** | medium | **v0.6 — EC-2 folded** | partial | EC-2 flag-back (6/3) → Arch + CXO both qualifier-needed → PPM synthesized → CXO confirmed faithful ("take it to PM"). **FOLDED into `PDR-005-...-v0.6-2026-06-03.md`** (6/3): EC-2 platform-affordance-bounded qualifier + paired AC-1 surface-presence-detection mechanism + Q7 per-host-claim-map note + open-q 11 RESOLVED. **Remaining v1.0 gates**: (1) **Comms external-language frame** — nudged 6/3 as "the last input before v1.0→PM"; (2) PM ratification (after Comms frame). Lead Dev integration read = non-gating example-refinement (welcomed). CT v2.5 sub-dim deferrable to v1.1. **Next PPM action**: on Comms frame landing, fold it + take PDR-005 v1.0 to PM. |
| 4 | **EC-2 platform-affordance-bounded qualifier cohort flag-back** | low | **RESOLVED 6/3** | done → folded into #3 | flag-back sent 6/3 AM → Arch + CXO replied same morning, both qualifier-needed with genuine examples → PPM synthesized + re-circulated (see #3). Disposition closed; remaining EC-2 work (fold qualifier into PDR-005 after Lead's read) tracked under #3 PDR-005 path. |
| 7 | **HOST Agent 360 v0.3 fielding** | low | open | YES | HOST request 6/3: complete post-migration 360 (`dev/active/agent-360-questionnaire-v0_3.md`); answer §8 PPM-specific + §7 diff-vs-v0.2-baseline + §10 duty-cycle-adopter module. Respond to `mailboxes/host/inbox/` filename `agent-360-response-ppm-code-opus-2026-06-0X.md`. **Backstop ~Jun 10** (Time Lord, not pacing). Substantial; fold into a focused cycle before Jun 10. |
| 5 | **Multi-Agent API characterization** | low | open | unclear | per CIO May 18 Outcomes disposition; may have reassigned with the May 24 Outcomes lane reassignment to PA+CIO. Needs clarification before advancing. |
| 6 | **#683 Layer A — interface-verification DoD** | medium | **INTEGRATED (6/2)** | done (PPM scope) | **PPM Layer A integration COMPLETE 6/2**: canonical DoD doc `docs/internal/development/interface-verification-dod-layer-a.md` (promoted CIO draft) + Sub-Epic Gating Protocol item 5 in `m2-structure.md` + Class B note on Review Gates norm in `roadmap.md`. Placement = Class B (sub-epic gate) requirement per PM ratification 5/30. **Remaining for full #683 close (not PPM-Layer-A)**: Lead Dev operational-check recipe + CXO methodology-30 grounding-review + Layer B (CXO experience-DoD — **drafted fresh by CXO 2026-06-02**, `done-criteria-layer-b-experience-2026-06-02.md` `833871245`; A+B co-review before canonical landing) + literal PR-review-checklist AC + service-type-interface matrix AC. Do NOT close #683 yet. **Corrected-premise note (CXO flag 6/2):** the May 28 PPM memo `memo-ppm-to-cxo-...683-parallel-pairing-confirmed-2026-05-28.md` confabulated two artifact refs (a "Layer B as drafted" + an in-reply-to CXO memo) — both never existed; CXO never drafted Layer B until 6/2. My Layer A was correctly queued-on-CIO-draft; there was simply no Layer B to pair against yet. DoD doc corrected; CXO acked. |

## Next task (queued for next session)

~~**#1128 v17 roadmap draft**~~ — **COMPLETE May 30** (`roadmap-v17-draft-2026-05-30.md` commit `00cee8d47`; distributed `15f8a05ae`).

**Primary next tasks** (queued for new worktree-cycle session post-migration):

1. **v17 → v18 absorbing PA §M5 review** (May 31, `71220bbfe`):
   - Daedalus referent: revise to "context-package format to be negotiated with Daedalus (Klatch's lead engineer); on hold while Klatch is paused" (PM clarified Daedalus = Klatch lead engineer)
   - Outcomes "~May 30 findings" stale → real sequence: CIO methodology-34 synthesis Day 28-29 → PA Outcomes smoke-test scope-memo + execution
   - §M5 line 127: undersells gated PASSED 5/19 sub-pass 4.a (local plugin install + skill-invoke via `--plugin-dir`; predecessor-pattern study not PDR-005 competitor) — fold concrete result
   - §Autonomous Operations: add one line on DinP Janus meta-coordinator contrast (cycle architecture generalizing across structurally-different agents, not just uniform cohort)
   - Still waiting on CIO §Methodology review (no movement since distribution May 30)

2. **Ship #045 workstream review** (Wed Jun 3 drop-dead) — PPM lane: PDR-005 ratification path / Roadmap v17 work + sign-off discipline learning / M2g closure tail / MUX/UI Phase 2 build coordination / standing-items tracker discipline / Q6/Q7 ADR sequencing

3. **#683 Layer A integration** (PM-ratified Class B requirement May 30; CIO DoD draft `dev/active/dod-layer-a-interface-verification-DRAFT-cio-2026-05-28.md` ready) — write Review Gates 5-class taxonomy addition + M2d-style completion-criteria entry. methodology-30 strengthened by Architect's May 30 `_fallback_classify` production-orphan catch.

## Blocked / waiting-on-external

| Item | Blocked on |
|---|---|
| PDR-005 v1.0 ratification | PM final gate + Comms external frame + EC-2 flag-back |
| Multi-Agent characterization | clarification whether PPM-lane or PA+CIO-lane post-May-24-reassignment |

## Done (recent, for context)

- Ship #044 PPM workstream review (filed May 24)
- PDR-005 v0.5 (CXO §experience absorbed, May 19)
- HOST 360 item 1.3 BYOC vehicle clarification (closed both sides May 24)
- Surface 2 + Surface 4 sufficient-signals to Lead Dev (May 18)

---

*Duty-cycle Task Loop reads this top-to-bottom; advances unblocked items smallest-scope-first per v0.6.3 idle-advance discipline.*
