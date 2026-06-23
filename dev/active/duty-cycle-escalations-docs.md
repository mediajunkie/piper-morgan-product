# Docs Duty Cycle — Escalations / Attention Doc

**Purpose**: items requiring PM attention per v0.6 Duty Cycle (reframed escalations = attention doc, per Architectural Decision 2).

**Owner**: Documentation Management (Docs)
**Created**: 2026-05-27 12:05 PT at v0.6 cycle adoption

---

## Active escalations (for PM)

- **✅ RESOLVED 2026-06-02 — Docs duty cycle RESUMED in the `claude/docs-cycle` worktree (Model A); cron `d0724f4a` at `:17` (session-only, 7-day expiry).** The documented resume condition (operator relaunch in a worktree) is met — this session runs in the worktree, cwd anchors here, mail via the main-worktree bridge. PM-directed resume after the Jun 2 BYOC publish + workDate audit. Original vacate context retained below for history.

- **⚠️ SUPERSEDED 2026-06-21** — Docs now runs the duty cycle under the **Option B ephemeral worktree** model (canonical since 2026-06-12), cron armed (`9eb97927`, `17 3,10,13,16,19,22`). The "not re-registering / loop pauses by design" framing below is fully obsolete — the worktree-cycle mechanism landed and Docs cycles normally. Retained for history only; **not an active escalation.** Original (now-historical) note:
- **~~Docs on-main cron VACATED per ratified "do not register on main" (2026-05-28 ~14:50 PT)~~** — Following PM's morning ratification (Rule-2→Model-A + Q1 worktree-as-cycle-default) and the cohort convergence (CIO won't re-register, Exec vacated, HOST STOPped, PA never registered), Docs is **not re-registering the on-main cron.** The autonomous loop pauses here by design. **To resume autonomous cycling: relaunch Docs in a `claude/docs-cycle` worktree** once Lead+Arch land the worktree-cycle mechanism (v0.7 item 1, in design) + the overnight never-recreate-gap (item 4, open) resolves — a cron can't self-migrate to a worktree (operator relaunch required). Until then Docs runs **manual-session-open + PM-engaged**. No work is stranded; today's mail is drained and committed (`ee9ddcbeb`).

- **~~#972 MEM-TEMPORAL — 2 design questions~~ RESOLVED 2026-05-30** (PM directives): Q1 = "add a YAML block" (already shipped via May 28 briefing pilot `b40876b87`); Q2 = "drop them— I never asked for that" (memos dropped from scope; spec narrows to standing reference docs only). Spec updated to v0.3. ≥3-examples AC substantially satisfied (17 briefings already carry `valid_from` from the pilot). Remaining: decide session-log-instructions disposition (recommend same as memos by point-in-time logic; flagged in spec), continue YAML-frontmatter upgrade across other standing-doc classes (ADRs/patterns/methodology/serena already queued in standing-items). Closing this attention-doc item; remaining work tracked in standing-items.

## Process observations (for cycle methodology + CIO research)

- **2026-05-27**: Adopting v0.6 cycle as workhorse-tier per PM 8:51 AM PDT directive. Cron offset `:17`. [RESOLVED: launched 12:24 PT job 42a9ed72; cron-id rotated 3x through day to fc464e79.]
- **2026-05-27 Fire 8**: v0.6.3 forward-progress judgment — declined to autonomously edit BRIEFING-CURRENT-STATE (high-blast-radius cohort doc) on a late-evening fire; instead surfaced the #972 clarification blocker above. Holistic-not-tactical: not all "unblocked low-priority work" is appropriate for unsupervised fires — blast-radius is a filter alongside scope.

---

*This file is escalations-as-attention-doc per v0.6 architectural decision 2. Append during cycle fires when items need PM-attention surfacing.*

## Forward-looking (PM observation 2026-06-02 ~19:1x PT) — omnibus-gating is temporary-by-design

PM: *"Once all the agents are on a duty cycle, the STOP day part should handle this kind of routine log closeout before you START the next day and then WORK on the new omnibus."*

**Confirmed**: `docs/operations/duty-cycle design/procedures/stop.md` Step 2 already mandates each agent's own day-close (wrap entry + commit + push). No procedure gap.

**The dependency to make explicit**: Docs's omnibus-at-START depends on the *whole cohort's* STOP-at-EOD having run the prior night — not just Docs's own. So the omnibus-synthesis-gating friction we hit for May 30 / May 31 / June 1 (PM manually checking in to close each agent's log before clearing the day) is a **temporary state**, not a standing process. It resolves when:
1. **All agents are on the cycle** (off-cycle agents — Comms/PPM/Web/HOST during the June migration — don't run STOP, so their logs need manual closeout); AND
2. **The overnight-continuity gap (item-4) is closed** (sessions ending before the 11pm STOP fires → logs trail off → retroactive next-day closes; the failure mode behind most of the trailing-off logs).

**Docs action when full adoption lands**: the omnibus can move from "wait for PM to clear each day" → "synthesize yesterday's omnibus at START by default" (logs already finalized by the cohort's STOP). Until then, the PM-clearance gate stays (it's the safety net while adoption + overnight-reliability are incomplete). Worth a flag to CIO (duty-cycle-design lane) to note the cohort-STOP→Docs-omnibus dependency in the v0.7+ design so it's a tracked adoption-completion criterion.

## June 2 self-closeout test RESULT (2026-06-03 ~07:30) — partial pass

PM ran the test: do agents self-close June 2 via STOP without reminders? **Result: ~half.**
- **Self-closed cleanly**: Lead, Docs, CIO, PPM, Exec (+ Comms ran its closing ritual).
- **Did NOT** (trailed off, no STOP/wrap): PA (triage list), Web (recommendation "surface to PM"), HOST (2206 — `<!-- append Fire entries below -->`, successor just set up), Architect (plan-only, paused), CXO (1730 — "fill at wrap" never filled).
- **Pattern**: established full-day cycles self-close; **evening migration-successor sessions + paused/recommendation-trailing roles do not.** Confirms the item-4 overnight-continuity gap + a successor-session-handoff gap.
- **Consequence for omnibus**: June 2 omnibus HELD until PM closes the 5 trailing logs (biggest day of the stretch — 11 roles, ~197 commits; drift-risk too high to synthesize over unclosed logs). PM closing them 6/3 AM (HOST + CXO done; PA/Web/Arch next).
- **For the overnight-continuity/STOP fix (CIO/Lead lane)**: the self-closeout reliability gap is specifically at successor-session-handoff + paused-role boundaries, not the steady-state cycle.
