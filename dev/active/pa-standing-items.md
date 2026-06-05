# PA Standing Items Tracker

**Purpose**: Track PA-domain items that are pending PM input, blocked on external action, or queued for PA execution but not yet started. Persistent surface so items don't get lost to transcript / PM memory / PA context window.

**Origin**: Created 2026-05-27 at duty cycle v0.6.2 adoption Day 0 per CIO's suggested-path step 2 (reuse existing or create). PA hadn't previously maintained a standing-items tracker; created new at adoption.

**Duty Cycle role (v0.6 design ratified)**: This file IS the canonical **Task List** (Doc 2 of the three per-agent duty-cycle docs). Per the formalizing-not-proliferating principle, no parallel "task list" doc is created. Tasks added during Mail Loop step 4 land here. Task Loop reads from here. PM-injected tasks (the load-bearing (0, 1) decision-table row) also land here.

**Update cadence**: append-only ledger with status updates in-place. PA updates at session-start (review carryforward) and after each substantive session (capture new items + close completed ones). Distinct from `exec-open-items-tracker.md` (exec-owned, project-wide) — this is PA-owned, methodology-and-product-management scope.

---

## How to Read This

| Status | Meaning |
|---|---|
| **Pending PM** | Awaiting PM decision, concurrence, or approval |
| **Pending external** | Awaiting other-role action (CIO, Lead Dev, Docs, etc.) |
| **PA-queued** | Bandwidth-gated PA work; ready to execute when scheduled |
| **Watch** | Standing observation surface; trigger-bound |
| **Active** | Currently in flight |
| **Resolved** | Closed; preserved for one cycle then removed |

---

## Active Standing Items

### Pending PM input

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Skunkworks writeup → final PM signoff → fan-out** | 2026-05-21 (writeup reconstructed 5/30) | **Writeup at `dev/active/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`**. ✅ Cowork-test package findings folded (5/31; runtime/fs mismatch + payoff-ceiling + moat); ✅ all 3 `[verify]` resolved/dispositioned; ✅ PM observations folded (value=light-but-POV-implied; runtime-bug=expected-not-crisis; forward=thin-full-stack-PoC proposal). **Remaining: final PM signoff → fan-out.** Fan-out spine = forcing-function + ratification ask (not just learnings). Ted/Dan tester check = PM-owned + nonblocking (not a gate). |
| 1b | **Thin full-stack PoC — next skunkworks experiment** (PM proposal) | 2026-05-31 | PM proposes next experiment: minimal MCP hitting real PM API + minimal PM/assistance skills (down payment) + minimal plugin orchestration; modeled on PM's OpenLaws plugin. Needs **leadership ratification** (single-purpose, all-layers, NOT overbuilt) + **roadmap/strategy alignment** (don't front-run architecture). Coordination: keep it a predecessor-study feeding PDR-005 + Arch Q6/Q7. PA to surface in fan-out + tee up roadmap synthesis. |
| 2 | **Outcomes smoke test scope + start** | 2026-05-27 | PM approved 2026-05-27 ~2:30 PT. Execute after CIO methodology-34 synthesis lands (Day 28-29 per CIO commit). PA proposes to draft scope-memo to PM at that point. |

### Pending external action

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work tiered "buried" bar concur** — Lead Dev | 2026-05-27 | Tiered bar proposed in disposition memo: P:crit 3d/3d → P:low 21d/14d. Lead may flag-back if mechanically heavier than flat 14d/7d default. First sweep starts Fri 5/29 with flat default; tiered refinement after Lead concur. |
| 2 | **Memory pin draft on discovered-work discipline** — PA-or-Lead-Dev co-author | 2026-05-27 | PA offered to draft solo or co-author with Lead. Awaiting Lead's preference. Provisional name: `feedback_discovered_work_doesnt_get_lost.md`. |
| 3 | **MEM-975 cohort rollout PA slot (Week 2)** — Lead Dev | 2026-05-27 | PA in Week 2 (Days 8-12 post-launch); structured N=5 measurement Lead drives. Aligns with v0.6.1 stabilization ~May 31. |
| 4 | **check-branch.sh fix for Model-A mailbox-on-branch** — Lead Dev | 2026-05-28 | Memo `7670c2f3e` sent. Hook hard-blocks mailbox commits on cycle branch (no push-to-ref bypass); v0.7 template's per-fire-push mail path doesn't work. Until fixed, PA mail rides main-worktree bridge. **CIO concurs Option-1 (amend hook); template corrected `a5517ee02`.** Awaiting Lead Dev fix-choice (Lead owns the hook). |
| 5 | ~~**Roadmap v17 §M5/BYOC review** — PPM~~ → **RESOLVED 5/31** (see Resolved R4) | 2026-05-29 | Draft landed `00cee8d47`; PA review delivered to PPM `0448f8e7d`. |

### PA-queued

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work weekly sweep** — Friday-to-Thursday cadence | 2026-05-27 | **Ran Fri 6/5: 126 open; 8 unassigned (all low/no-pri — 3 are PA's own new #1145/#1150/#1151); 0 high/crit unassigned = HEALTHY** (vs 6/2's 1). Stale-but-high (>14d): 5, all ASSIGNED + known roadmap — flag for PM glance: **#358 SEC-ENCRYPT-ATREST (critical, 5/17)** + **#321 DATA-AUDIT-FIELDS (high, Nov, very old)**; CONV-FEAT #103/104/106 = unscheduled M3/M5 backlog (not neglect). Assigned #1145 to mediajunkie. Flat 14d bar = 101 (mostly parked backlog → tiered-bar still wanted). Next: Fri 6/12. |
| 2 | ~~**Roadmap v17 §M5/BYOC review** — PPM-requested~~ → **RESOLVED 5/31** (see Resolved R4) | 2026-05-31 | Review delivered. Verdict: §M5 sound; 2 corrections (Daedalus referent gap, stale Outcomes target) + 2 sharpenings. Review at `dev/active/pa-v17-m5-review-for-ppm-2026-05-31.md`. |
| 2 | **methodology-34 refresh review** — Day 28-29 when CIO lands | 2026-05-27 | PA welcome as Day-3/4 review feedback per CIO follow-up memo. |
| 3 | **Skunkworks sub-pass 4.b dispatch** (insight-journal-flat-file) | 2026-05-21 | Pending writeup fan-out + PM signoff. PA-queued behind item 1 above. |
| 4 | ~~**HOST Agent-360 v0.3 response**~~ → **DONE 6/3** | 2026-06-03 | Delivered to HOST inbox (`6e8fb106a`), cc PM. Answered §1/2/5/6/7/8(PA)/9/10(observer + V2-live bonus). Candid friction: bridge-overhead, check-branch.sh fix unshipped, deferred-logging near-miss, hourly-cron-wrong-for-bursty-lane, BYOC-not-in-M5-issues. Fielding memo → read. Synthesis ~Jun 12. |
| 5 | **Cron-shape experiment (PA lane)** — STARTED 6/3 | 2026-06-03 | **Switched hourly → every-3-hours `42 */3 * * *`** (cron `4c3be3e3`) under CIO 6/2 standing authorization, after 5 consecutive no-op hourly fires in a ~6h PM-idle stretch. Logged in `cron-shape-experiments.md` (PA row). Revert-to-hourly when substantive backlog surfaces (skunkworks/audit go). Surfaced to PM for revert/adjust. Memo CIO with results (~Day-7). Watch: PA-actionable mail sitting >3hr. |

### Newly-surfaced (6/3 eve)

| # | Item | Filed | Notes |
|---|---|---|---|
| A | **PDR-005 line ~376 "MCPB hybrid" stale ref** | 2026-06-03 | Same packaging-model issue as the v18 fix; PPM flagged + left it (broader-distribution scope). Correct when PDR-005 → v1.0 or skunkworks fan-out lands. Fold with the fan-out batch. |
| B | **§M5 PoC line-128 sharpen** (thin-PoC/`/intent` detail) | 2026-06-03 | PPM deferred folding it into v18 (didn't want v18 ahead of held fan-out). PM call: fold now or with fan-out. |
| C | **Attention Dashboard v0.2** — co-shape with CIO | 2026-06-03 | CIO named it a roadmap item; offered to co-shape v0.2. Rungs: auto-stale-flag → GitHub-state verify → dedupe → severity-parse → priority-rank. Build when PM/CIO prioritize. |

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. |
| 2 | **Year-anniversary milestone observance** — today | 2026-05-27 | PM directive: update MVP date 2026-07-04 (executing today). Future: celebrate the milestone. |

### Active

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Duty cycle on Model A — emeritus handoff to fresh session 5/31** | 2026-05-31 | Day 1-4 (5/28-5/31) ran in continuous emeritus session. Fresh session per `dev/active/pa-fresh-session-handoff-prompt-2026-05-31.md` takes over. Emeritus session paused, available for "from the future" POV checks. Cron unregistered at handoff. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| R4 | **Roadmap v17 §M5/BYOC review** delivered to PPM | 2026-05-31 | Fresh session. Full review `dev/active/pa-v17-m5-review-for-ppm-2026-05-31.md` (`71220bbfe`); cover memo to PPM cc PM/CIO (`0448f8e7d`). Verdict: §M5 sound — endorse structure + PDR-005-supersedes-PoC boundary + Klatch-pause framing. 2 corrections (Daedalus context-package referent gap → recommend soften; stale Outcomes ~May-30 target → recommend CIO-synthesis-gated sequence) + 2 sharpenings (PoC gate-PASS concreteness; Janus meta-coordinator line in §Autonomous Operations). PPM integrates into v18-draft. |
| R1 | check-branch.sh blocker memo → Lead (cc PM/CIO/Arch) | 2026-05-28 | `7670c2f3e` via bridge. v0.7 open-item #1 resolved (answer: hook blocks; needs fix). Now tracked as Pending-external #4. |
| R2 | Code/worktree restart + carry-forward recovery | 2026-05-28 | Prior session hit wall; delta-pa rescue confirmed on main (`f877ed84f`); continuation log + cycle log stood up. |
| R3 | Duty cycle v0.6.2 setup + MVP milestone update + first discovered-work sweep | 2026-05-27 | All executed 5/27 Fire 0 (milestone #5 → 2026-07-04; sweep = 0 buried, healthy baseline). |
