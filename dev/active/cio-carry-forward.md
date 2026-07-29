# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — so this is one of the few real paths to PM.** Stale here propagates to PM's attention board.

---

## PM Attention

*(Whole-file rewrite 2026-07-29 08:35 PDT — timestamp verified with `date`, not estimated. Live items only.)*

- 🔴 **AMBER HAS NO PIPER BUILD STACK — this blocks the beta path, and it is the biggest open item.** Lead migrated 07:47 and found it; **CIO independently re-probed every claim** rather than relaying. Absent: venv · container runtime (docker/colima/orbstack all missing) · flyctl. Wrong: system python **3.14.6** where the project pins **3.11** (a 3.14 venv will not reproduce CI). Closed: Postgres **5433** and Redis **6379**, port-probed rather than inferred. **Blocked**: the #1452 burn-down method and beta deploys. **Not blocked**: coordination, GitHub/board work, backlog bookkeeping, design records, CI review, mail — so Lead is **half-productive, not stopped**. Routed to Pard (host-level tooling is a provisioning call); **PM sets the priority**. Why eight prior migrations passed clean: **none of them compiles anything** — Lead is the first migrant whose lane needs a toolchain.
- ⏰ **PA's two five-minute items — 10 days parked**, still the only board item with a clock we do not control. claude.ai account tier + **start OpenAI identity verification**.
- 🟡 **MIGRATION 8 of 10.** ✅ lead (07:47, verified, already logging + hook-probing). **Remaining: exec · comms · docs**, all three still **live on the old system**. Each asked ~07:35 to close cleanly, park/create its registry row, and reply. **As of 08:32 none has replied** — and none has *missed* anything: exec fires `32 8,20` (due now), comms `12 6,9,12,15,18,21` (09:12). **Successors are NOT provisioned while predecessors are live** — that is the 7/19 two-live-sessions shape that caused real data loss.
- 🟢 **Docs HOLD lifted.** Pard provisioned standing website worktrees for `docs` and `web` and shipped `--extra-repo`. Docs is now gated only on its own clean close.
- 🟡 **Five migrated roles still NOT duty-cycling** — arch/ppm/cxo/pa/web have no armed crons (PM-gated), all parked with falsifiable clearing conditions. **Lead is deliberately in the same state**: cron unarmed because PM is actively engaged (cron-off-while-engaged), row parked by design — **do not read Lead's parked row as a stall.**
- 🗣️ **Standing, from PM**: do not change an agreed process without asking · when a premise I stated to PM turns out false, **raise it** rather than working around it · **verify timestamps with `date`; never estimate one.**

## Shipped today

Ship #053 filed (one working day in-window, verified from logs **and** commits) · **checklist v1.8** + onboarding delta now **point at Pard's cross-project standup failure catalog** rather than paralleling it · **portfolio-framework Rule 5 amended** to PM's ruling (a late review refreshes the portfolio *through today*, not to the window) · lead migrated · build-stack gap found, re-probed, routed · PM's summary-report request relayed to Lead cc Exec.

## Lower priority / queued

- **Nothing reads a window's second-order findings forward.** Ship #053 surfaced that *"an escalation depends on its recipient being awake"* was sitting in a filed review **eight days** before we re-learned it as the parked-role catch-22. Reviews produce these; nothing consumes them.
- **A canonical index of which doc owns which concern** — I nearly edited a *database* migration checklist because filenames collide.
- **Watchdog concept revisit — PM-parked until the migration settles.** Five patches in five days, each correct, each revealing the next layer; that pattern wants a rethink, not a sixth patch, and not while we depend on it.

## Cron

⚠️ **TEMPORARILY `7,27,47` (20-min) — job `7bc44268`, bumped 2026-07-29 07:40 for the active migration window.** **REVERT to LEAN `7 10,16,22` once exec/comms/docs are provisioned or PM closes the window.** A temporary cadence that persists by inertia is the create-rule-without-a-cleanup-rule trap this lane exists to prevent.

<!-- Whole-file rewrite 2026-07-29. Rewriting the TOP is not rewriting the FILE. If you add a section,
     delete what it supersedes in the SAME edit. -->
