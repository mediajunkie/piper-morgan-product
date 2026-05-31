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

**#1128 v17 roadmap draft** — delta-assessment COMPLETE (Fire-0; `roadmap-v17-refresh-delta-assessment-2026-05-28.md`, 8 deltas). Next unit: draft roadmap v17 in dev/active from the assessment, preserving v16.0 structure, with executive-summary through-line flagged `[PM EYE]` per v16 precedent (strategic-framing emphasis is PM's call). Then Docs-swap + CEO ratification. Best done in a PM-present or worktree-live session (CEO-authority artifact + through-line judgment).

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
