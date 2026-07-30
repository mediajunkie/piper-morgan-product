# CIO Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time state for `duty-cycle-tick`. **Exec's `cohort-attention-rollup` reads the PM Attention section directly, and PM does not read memos — this is one of the few real paths to PM.**

---

## PM Attention

*(Whole-file rewrite at the 2026-07-29 STOP. Timestamp verified with `date`. Live items only.)*

- ⏰ **PA's two five-minute items — 10+ days, the only board item with a clock we do not control.** claude.ai account tier + **start OpenAI identity verification**. PA is back and cycling as of 7/29, so the blocker is now purely PM-side.
- 🔴 **Lead cannot build, test, or deploy — the beta path is blocked on host tooling.** Amber has **no venv, no container runtime, no flyctl**, system python 3.14.6 against a 3.11 pin, and Postgres 5433 / Redis 6379 closed. `docker-compose.yml` declares **four** services, so native brew installs are not viable — a container runtime is required, not preferred. Spec is with Lead; **`colima start` is PM's call** because it runs a background VM on a host with eleven live sessions. **Lead is half-productive, not stopped** (coordination, board work, backlog bookkeeping, CI review all fine). Lead correctly refuses to substitute reading CI logs for the local sweep.
- 🔴 **The toolchain gap is cohort-wide, not Lead-specific.** Docs found **`node_modules` absent across the entire website repo including the shared checkout** — nobody on Amber has ever had working website dependencies — and it spans **both languages**, silently disabling a check inside `template-audit`. Routed to Pard.
- 🟢 **MIGRATION COMPLETE: 11 of 11 on Amber, 11/11 registry rows, 5 of 11 closing cleanly on day one.** All five predecessor handoffs landed (arch, pa, ppm, cxo, web). No role is structurally invisible to the freeze-watchdog for the first time.
- 🟡 **Still not duty-cycling: `lead` and `ppm`.** Everyone else armed and cleared their own rows.
- 🗣️ **PM wants the innovation agenda reviewed now the migration has landed.** That is the next substantive thread.
- ⏳ **Awaiting Exec/HOST pushback** on moving the registry-park check into provisioning pre-flight. Five instances with a failed checklist intervention behind it; deliberately not shipped before they respond, because I told HOST the same morning I would not build on two data points.

## Shipped today

**m-45 filed** (Agreement Is Not Replication — Arch's four-seat evidence) · **m-20 contradiction resolved** (two size rules unsatisfiable for five consecutive omnibus logs) · **`cohort-status.sh` built** (denominators + source disagreement + provenance) · **probe apparatus RETIRED at v1.22** — hooks were a time-of-check/time-of-use inversion, fixed in one file by Pard · G6 heartbeat false-alarm fixed · exec/docs/comms provisioned · **inbox 92 → 0** · arch orientation note's false negative claim corrected.

## Lower priority / queued

- **Nothing expires a negative claim.** Three of us held *"the blind-sweep note is unfiled"* two days after I filed it; the pinned rule has existed since 7/12 and nothing applies it. Best mechanism candidate on the list.
- **No composition test for multi-part changes** — I passed 3/3 on individual refinements and shipped a conflict between two of them.
- **Nothing consumes a review's second-order findings** — Ship #053 carried a lesson eight days before we re-learned it expensively.
- **Watchdog concept revisit** — PM-parked until things settle. Six patches in six days, each correct, each revealing the next layer.

## Cron

`7 10,16,22` LEAN — re-armed at the 2026-07-29 STOP (delete → create → verify; one job, `7b089a43`).

<!-- Whole-file rewrite 2026-07-29. Rewriting the TOP is not rewriting the FILE. -->
