# PPM Standing Items — Task List (duty-cycle Task Loop source)

**Role**: Principal Product Manager (PPM)
**Purpose**: the duty-cycle "task list" per v0.6 architectural decision 1 (reframed standing-items tracker; no new doc). Task Loop drains this in priority order until all blocked-or-empty.
**Created**: 2026-05-28 (duty-cycle adoption, final wave)

---

## Active lane work (priority order)

| # | Item | Priority | Status | Unblocked? | Notes |
|---|---|---|---|---|---|
| 1 | **#1128 ROADMAP-REFRESH** | medium | **in-progress** | **partial** | roadmap.md 20 days stale. **Fire-0 (May 28): delta-assessment COMPLETE**. **May 30: v17 draft COMPLETE** (`roadmap-v17-draft-2026-05-30.md`, ~290 lines, commit `00cee8d47`). Distributed to cohort (`15f8a05ae`). **Now blocked on**: PA §M5/BYOC review + CIO §Methodology review + Comms external-language frame (PDR-005 carry) + PM ratification → Docs swap. |
| 2 | **#967 Backlog Deep Review — Surviving Edges** | low | open | YES | backlog tracking. PPM domain. PM-approved triage lane. |
| 3 | **PDR-005 v0.5 → v1.0 path** | medium | in flight | partial | gated on: cohort flag-back on EC-2 + Comms external-language frame + PM ratification. CT v2.5 sub-dimension deferrable to v1.1. |
| 4 | **EC-2 platform-affordance-bounded qualifier cohort flag-back** | low | open | YES | PPM-driven surfacing before v1.0 ratification. |
| 5 | **Multi-Agent API characterization** | low | open | unclear | per CIO May 18 Outcomes disposition; may have reassigned with the May 24 Outcomes lane reassignment to PA+CIO. Needs clarification before advancing. |
| 6 | **#683 Layer A — interface-verification DoD** | medium | queued | **blocked** | accepted May 28 (PPM integration owner). methodology-30 Consumer-Trace as completion gate; lands in Review Gates taxonomy + M2d-criteria-style completion-gate entry. **Blocked on CIO methodology-30-grounded draft** (standing-items 8d) landing first; then PPM integrates. |

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
