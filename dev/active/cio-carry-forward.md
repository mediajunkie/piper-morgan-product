# CIO Carry-Forward — ephemeral session state

**Purpose**: the read-at-fire-time carry-forward for the duty-cycle-tick skill. Holds the genuinely transient "where am I right now" state. Durable owed/queued items live in `cio-standing-items.md` (the Task List); PM-attention items live in `duty-cycle-escalations-cio.md`.

**☀️ 6/25 morning (10:37 fire)** — Thu. **Cron `b1bb59a6` armed** (`7 3,10,13,16,19,22`; re-armed 6/24 after the prior died in Tue's rate-limit pause), next 13:07. Inbox drained.

### Live / in-flight
- **Iris Phase 3 cutover runbook — DELIVERED 6/25** (PM day-focus, via Janus relay; DinP `d0ade03`). Persistent worktree + dedicated `iris/heartbeat` branch + standing daily cron (`17 9`, durable) + verification + the foregrounded-idle caveat. **Offered Janus the Phase-4 off-machine-wake spec on request** — watch for a follow-up from Janus/Calliope.
- **Worktree cleanup (CIO-owned, pair w/ Docs)**: rubric LANDED canonical (`5b7cabc53`, discipline-doc Rule 5). **Two open pieces**: (1) the **sweep-CODE** (`prune_worktree` in `merge-keeper-sweep.py`) — *destructive* → **banked for a FRESH session** (explicit trigger, not "no rush"); (2) **one-time rescue+prune of the current 31** — pair with Docs (3 unmerged rescued first: determined-heisenberg/interesting-goodall/mux-ui).

### Queued (low-pri, unblocked when bandwidth)
- **threshold v0.4 = wake-window-aware** — cio's flat 8h is too coarse for a daytime stall; tune against Arch's `GAP-SINCE-LAST-FIRE` data.
- **Cohort-coverage expansion** — freeze-registry watches 5/11 (cio/exec/arch/cxo/ppm); extend to the rest via **owner-confirmed rows (Exec-coordinated opt-in)**, NOT inferred (false-nudge risk).
- **Sprint cluster**: #973 / #1277 left. (#1153 DONE+CLOSED `ab44e595c`; **#1287 CIO part DONE 6/25** → consumer-traced + Lead surfaced a 3rd edge into methodology/ → I made the **boundary call: Option 1 expand** (`442305797`); Lead executes the full services/+methodology/ deletion pass + closes. #1191 findings-log, not actionable.)

### Standing / PM-gated
- **Off-machine firing cure** — the deep structural fix for session-crons-don't-fire-while-backgrounded. Evidence now: ~7 stalls + the Tue rate-limit pause + the Iris caveat. **#1191 cloud-survey finding (folded in)**: the cloud Code surface has **no `CronCreate`** → off-machine firing needs an external trigger (**GitHub Actions cron**, Google Calendar recurring event, or Slack scheduled message). So the cure's option-space = {launchd-on-mac, GitHub Actions, Calendar/Slack scheduler, ~$70/mo Routines}. PM's call on cost; I can scope a comparison on request.
- **Freeze-watcher LIVE** (launchd, registry-driven `dev/active/duty-cycle-registry.tsv`) + **regression test** (`5d33a9c21`) locking the 6/22 false-stale fix. On-machine watcher can't catch machine-death during an outage (only after) — that's what the off-machine cure addresses.

### Recently closed (drop next cycle)
- **duty-cycle-tick structural rewrite — LOOP CLOSED** (6/24): flywheel-as-spine + save-for-next-fire-structurally-impossible + one cron rule; Lead-reviewed + folded (`ea20c381b`); **DinP hardened framing sent** (`982b830`). · **Ship-#048 workstream review** delivered (`f92d68f34`). · **MEM-EVAL** (#1272/#1274, MEMORY.md 42→22KB). · **#1292** closed.