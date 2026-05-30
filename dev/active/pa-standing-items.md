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
| 1 | **Skunkworks writeup fan-out** — pending PM Desktop test of cold-start skill | 2026-05-21 | Draft at `dev/active/pa-skunkworks-byoc-poc-learnings-draft-2026-05-21.md`. **PM directive update 5/29 ~3:07 PM: "remind me to do that skunkworks desktop testing later today or this weekend please."** PA scheduled one-shot reminder for 18:33 today; will schedule a Sat-AM follow-up if no engagement tonight. |
| 2 | **Outcomes smoke test scope + start** | 2026-05-27 | PM approved 2026-05-27 ~2:30 PT. Execute after CIO methodology-34 synthesis lands (Day 28-29 per CIO commit). PA proposes to draft scope-memo to PM at that point. |

### Pending external action

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work tiered "buried" bar concur** — Lead Dev | 2026-05-27 | Tiered bar proposed in disposition memo: P:crit 3d/3d → P:low 21d/14d. Lead may flag-back if mechanically heavier than flat 14d/7d default. First sweep starts Fri 5/29 with flat default; tiered refinement after Lead concur. |
| 2 | **Memory pin draft on discovered-work discipline** — PA-or-Lead-Dev co-author | 2026-05-27 | PA offered to draft solo or co-author with Lead. Awaiting Lead's preference. Provisional name: `feedback_discovered_work_doesnt_get_lost.md`. |
| 3 | **MEM-975 cohort rollout PA slot (Week 2)** — Lead Dev | 2026-05-27 | PA in Week 2 (Days 8-12 post-launch); structured N=5 measurement Lead drives. Aligns with v0.6.1 stabilization ~May 31. |
| 4 | **check-branch.sh fix for Model-A mailbox-on-branch** — Lead Dev | 2026-05-28 | Memo `7670c2f3e` sent. Hook hard-blocks mailbox commits on cycle branch (no push-to-ref bypass); v0.7 template's per-fire-push mail path doesn't work. Until fixed, PA mail rides main-worktree bridge. **CIO concurs Option-1 (amend hook); template corrected `a5517ee02`.** Awaiting Lead Dev fix-choice (Lead owns the hook). |
| 5 | **Roadmap v17 §M5/BYOC review** — PPM | 2026-05-29 | PPM sole-authoring v17; PA reviews §M5/Distribution (BYOC) section. **BLOCKED: v17 draft not yet produced** (only delta-assessment exists). Nudged PPM `f342fbd36` (cc PM/CIO). PA ready to turn around fast once draft lands. PPM's 5/28 mail was stranded uncommitted — rescued to origin via Comms `5d61755e7`. |

### PA-queued

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Discovered-work weekly sweep** — Friday-to-Thursday cadence | 2026-05-27 | Ran Fri 5/29: 115 open, **0 buried, 0 high/crit unassigned — healthy**. Flat 14d/7d default (tiered bar pending Lead). Next: Fri 6/5. |
| 2 | **methodology-34 refresh review** — Day 28-29 when CIO lands | 2026-05-27 | PA welcome as Day-3/4 review feedback per CIO follow-up memo. |
| 3 | **Skunkworks sub-pass 4.b dispatch** (insight-journal-flat-file) | 2026-05-21 | Pending writeup fan-out + PM signoff. PA-queued behind item 1 above. |

### Watch

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Cross-pollination signal** — Klatch (paused), Atlas, Globe sibling projects | Pre-migration carry | Per `[[project_sibling_projects]]` memory. Surfaces if any sibling-project signal reactivates. |
| 2 | **Year-anniversary milestone observance** — today | 2026-05-27 | PM directive: update MVP date 2026-07-04 (executing today). Future: celebrate the milestone. |

### Active

| # | Item | Filed | Notes |
|---|---|---|---|
| 1 | **Duty cycle on Model A — Day 3 active** | 2026-05-30 | Day 1 (5/28): 4 clean fires + STOP. Day 2 (5/29): manual re-open + 5+ fires + Skunkworks reminder fired; no formal STOP (laptop slept first). Day 3 (5/30): continuous-session survived overnight; PM re-engaged 11:49 AM. Cron `85d6e4d0` still alive. |

### Resolved (preserved for one cycle)

| # | Item | Resolved | Notes |
|---|---|---|---|
| R1 | check-branch.sh blocker memo → Lead (cc PM/CIO/Arch) | 2026-05-28 | `7670c2f3e` via bridge. v0.7 open-item #1 resolved (answer: hook blocks; needs fix). Now tracked as Pending-external #4. |
| R2 | Code/worktree restart + carry-forward recovery | 2026-05-28 | Prior session hit wall; delta-pa rescue confirmed on main (`f877ed84f`); continuation log + cycle log stood up. |
| R3 | Duty cycle v0.6.2 setup + MVP milestone update + first discovered-work sweep | 2026-05-27 | All executed 5/27 Fire 0 (milestone #5 → 2026-07-04; sweep = 0 buried, healthy baseline). |
