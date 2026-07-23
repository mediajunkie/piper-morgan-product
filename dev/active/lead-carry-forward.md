# Lead Dev — carry-forward (updated at STOP 2026-07-22)

**MIGRATION-READY: the full handoff is `dev/active/lead-handoff-2026-07-21.md`** (per Exec's 7/21 prep ask — identity/mechanics, world-state, gates, queue, constraints). This carry-forward stays the rolling summary; the handoff is the fresh-session cold-start.

## 7/22 delta: SESSION FROZE ~15h (the crash pattern) — one partial fire only. document_processing mid-diagnosis (login-form fix + usage-cap headroom landed; 5× generic-error thread next — read the server-side logs it references). Arch rulings blocked on the escalated Arch stall (Exec's lane). **Migration to a fresh session recommended**; handoff doc current.

## Where things stand (EOD 7/21)
CI green + gate-governed (backlog ~272; 13 waves in 3 days; 634→272 all CI-arbitrated). Beta v26 (learning-loop fix live — #1438 closed; B3 continuity live — #1394 fixed). Root infra landed: NullPool session_scope (poisoned-pool class dead), user-cascade helper, diagnose step, prefix-repro method.

## Queue
1. Burn-down waves per the handoff's list (e2e adds → intent_wiring → doc_processing → execution_analysis → standup_perf → glances).
2. On Arch: methodology/ delete (21 entries ride) · #1432 orphan pair (Phase-4-in-the-orphan finding noted).
3. On Exec: #1386 re-run support (verifies #1393 + #1394 turn-3 in one pass).
4. PM standing: #1424 close-vs-keep (lean: close) · #1427 PROD-RECONNECT confirm.

## Standing
Cron e1106eb5 (session-only — RE-ARM on any fresh session: 17 6,9,12,15,18,21). Worktree lead-1452-harness for builds; main checkout mail/logs only, no destructive git, never silence push output. Spatial HELD. Key/droplet constraints per handoff.
