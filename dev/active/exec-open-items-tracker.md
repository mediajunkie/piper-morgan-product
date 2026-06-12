# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: **2026-06-12 ~10:10 AM PT** (new-Exec / DinP first duty-cycle fire — **full reconciliation after a 15-day gap** May 28 → Jun 12; the tracker was anchored to a Ship #044 / duty-cycle-v0.7 worldview now well past). Prior: 2026-05-28 (old-Exec, v0.6.1+v0.7 snapshot).

---

## Reconciliation context (Jun 12)

The May 28 → Jun 12 window moved a lot: M2 CLOSED Jun 3; M3 active; v0.8.7 production cut + BYOC hosted alpha live; Ship #045 + #046 published; PDR-005 BYOC v1.0 ratified Jun 5; duty cycle evolved v0.7 → windowed-exemplar + Option-B ephemeral-worktree; methodology catalog grew (m-40/41/42); the account re-migration wave (PA → Exec → Lead/CIO). Disposition applied below. **One item dropped** (Item 9 PDR-004, per its own prior escalation). Owner-lane items I can't verify from Exec's vantage are marked **status-check-owed** rather than given a fabricated status.

---

## Active Items

| # | Item | Owner | Opened | Status | Notes |
|---|------|-------|--------|--------|-------|
| 1 | **Ship #047 workstream review (Jun 5–11)** | exec (synthesize) | Jun 12 (kickoffs distributed) | **ACTIVE — 4 of 6 lenses in** (arch, cxo, cio, comms; held in exec/inbox as the collecting set). Pending: **PPM, HOST**. | Backstop Tue Jun 16 EOD (floor, not target); publish Wed Jun 17 AM. Source-set-state pacing: draft when complete; escalate source-owners if missing as backstop nears (not near yet). First cohort cycle under the corrected procedural-deadline framing — 4 same-week lenses suggests it's working. |
| 2 | **Migration instruction-gaps diagnostic + m-41 instance #2** | exec (filed) → CIO + Arch (ratify) | Jun 12 | Diagnostic filed to CIO (cc PA); **CIO promoted Finding 1 to an m-41 Proven-gate candidate** (variant-preservation trap = 2nd structurally-different instance), pending PM ratification + Arch co-author concurrence. PA compare-your-run ask pending. Doc-cleanup (canonical cron template; windowed-STOP skill rule; carry-forward register-split) queued by CIO. | The cross-pressure produced a reusable fix. Memory pin filed (`feedback_honor_durable_instructions_under_cross_pressure`). |
| 3 | **Routines watchdog build decision** | PM (gate) | standing (surfaced CIO Jun 7) | **Newly load-bearing.** Gap-C dormancy is the dominant cron-halt mechanism (CIO research Jun 11; funding-trigger criterion MET). Fresh data point: Exec's own cron died Jun 12 ~06:50→08:25 pre-first-fire. ~$70/mo external watchdog is the cure. | On PM's plate. The session-cron self-heal only fires if the session gets a turn — a fully-dormant session can't self-wake. |
| 4 | **Role-portfolio framework + pilot + v0.2 refinement** | PM (ratify) | Jun 11 | At PM ratification gate (filed Jun 11 eve + HOST pilot `ROLE-PORTFOLIO-HOST.md`). PM heads-down on OpenLaws this week — no rush. | Post-ratification sequencing: HOST pilot authored → cohort self-authors → HOST reviews vs 5 rules → Exec coordinates draft→ratify. |
| 5 | **BYO-colleague synthesis — 3 questions** | PM (answer) | Jun 9 | At PM's plate (filed Jun 9 STOP). Q1 M5 loop-defensibility gate; Q2 ratify ADR-068-only; Q3 HOST guest-framing external-vs-internal. | PPM lens + 6-lens convergence (composition-not-greenfield). Not blocking; awaits PM bandwidth. |
| 6 | **Duty cycle — windowed + Option B** | CIO (design) + cohort (adopt) | evolved from v0.7 | **LIVE, evolved.** Windowed-exemplar cron (no overnight 22:00–06:00 no-op fires; PA Day-7 ratified) + **Option-B ephemeral-worktree is canonical** (CIO confirmed 6/12; dedicated `claude/*-cycle` = older Model A, not required). Windowed-STOP rule (PM 6/12: "next fire is next day → STOP this fire"). | Exec cron `5dd30533` (windowed `:32`). CIO patching skill for windowed-STOP + thin-vs-middleweight prompt + canonical-template windowing within a few fires. |
| 7 | **Cohort-attention-rollup** | exec (maintains) | standing | Last compiled Jun 10 (`exec-cohort-attention-rollup-2026-06-10.html`). Refresh on PM request or when cohort PM-decision items accumulate enough to warrant a single-glance board. | Skill `cohort-attention-rollup` (Exec-owned, handed off from PA Jun 6). Lead Dev's attention-doc phantom-fix mechanism (Jun 10) should make the next compile clean. |
| 8 | **Owner-lane carries (status-check-owed; not exec-blocking)** | HOST / CIO / Docs / Lead | various | **HOST**: 360 R2 + handoff-review codification (Jun 8 re-benchmark passed — status-check-owed). **CIO**: Outcomes lane + methodology catalog m-34/40/41/42 (catalog clearly growing; specific item states owed). **PM+HOST**: alpha→beta closure (alpha live; beta gated on M3+). **Docs/Lead**: cross-poll-brief-as-session-start-hook, bash cwd-drift hook, two stale unowned branches, Apr 27 omnibus-reframing supersession. | Consolidated from old items 2–5, 8, 10–15. None exec-fixable; surfacing so they don't sit silent. Owners hold the status. |

---

## Disposition applied this reconciliation (Jun 12)

- **DROPPED — Item 9 (PDR-004 Medium/LinkedIn corrections)**: was flagged May 28 at 38 days zero-movement with an explicit "drop to tracked-not-prioritized if still unmoved" escalation. Now ~57 days. **Executing that escalation: dropped from active rotation** (tracked-not-prioritized; low-priority external-comms fix, PM+Docs lane if ever revived).
- **CLOSED — Ship #044 / #045 / #046 workstream reviews**: all published ("What Survives" → "The Substrate Pivoted" → "The Substrate Delivered"). Ship #047 (Item 1) is the current cycle.
- **CLOSED — BYOC PDR-005 discovery thread** (old item 7): **v1.0 RATIFIED Jun 5** (foundational PDR); hosted alpha live. Downstream ADR-065/066/068 work is Architect-lane.
- **EVOLVED — Duty Cycle v0.6→v0.7** (old item 6): superseded by Item 6 above (windowed + Option-B current state).

## Archived audit trail

Prior reconciliation's "Closed This Cycle (May 10 → May 24)" list + discipline-mechanism-artifacts inventory preserved in git history (`exec-open-items-tracker.md` @ commit prior to 2026-06-12). Condensed here to keep the active surface readable; recover via `git log -p` if an audit needs the May-era detail.

---

## Standing checks (next reconciliation)

- **BRIEFING-CURRENT-STATE.md** freshness — Jun 10 (within 7-day window as of Jun 12; trails the Jun 11–12 work). Docs lane.
- **XPOLL brief** — current.md fresh (Jun 12). PA/cross lane.
- **dev/active/ cleanup** — skill threshold ~15 files; dev/active is well over (cohort cycle-logs + deltas + trackers). Cross-role cleanup-coordination candidate (a solo exec sweep would violate commit-only-own-files); flagged in attention doc.
- **Ship #047 source-set** — monitor for PPM + HOST lenses each fire; escalate source-owners if missing as Tue Jun 16 backstop nears.

---

*Maintained by: Chief of Staff, Executive Office (exec-code-opus, Code/DinP instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
