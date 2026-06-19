# INCIDENT — two lead sessions forked into one worktree (2026-06-19)

**For**: CIO (methodology codification) · **From**: Lead Dev · **PM-requested.**
**Reconciliation detail**: `dev/active/SESSION-FORK-DISENTANGLE-2026-06-19.md`.

## What happened
Two Claude **lead** sessions ran concurrently in the **same worktree** (`interesting-beaver-7ee19c`) on the **same branch** (`claude/interesting-beaver-7ee19c`) for ~9 hours (6/18 ~23:00 → 6/19 ~08:1x). Both wrote the same `…-0707-lead-…` session log + the same `dev/active/lead-carry-forward.md`, shared one running server (PID 39025), and pushed to `origin/main`.
- **Session A** — interactive; PM-prompted 07:07 START; commits carry **no** `Claude-Session` trailer; cron suspended. Did: #1280 v2 shell rebuild + deploy + the CXO/Arch/#1284 mail.
- **Session B** — autonomous/remote; cron `8278cd31`; commits stamped `Claude-Session: …01C3…` + `Co-Authored-By: Claude Opus 4.8`; resumed from the 6/18 22:52 day-close via the 07:17 cron. Did: #1283 resolver-shape design + #1269 /standup page migration.

## Root cause
A **fork of an earlier lead session**: PM established "remote control," which attached/spawned a **second live process pointed at the EXISTING worktree** instead of a fresh one. Result: two processes sharing one git working tree, index, server, session log, and carry-forward — exactly the failure mode the worktree-per-session rule (CLAUDE.md §"Git Worktrees") exists to prevent ("a git repo can have only one branch checked out per working tree … file contents change out from under the other session").

## Symptoms (the pattern signature)
- Shared `lead-carry-forward.md` header + cron/PID field **drifting** (two writers fighting one field).
- The `0707-lead` session log appearing **"ahead"** of each session's own view (interleaved authors; the on-disk state ran ahead of each post-compaction summary).
- Stray `pa/inbox` deletions + MANIFEST regen-noise in the main checkout (one session's mailbox-bridge ops seen by the other as foreign changes).
- **Verify-first repeatedly catching "work already done"** (each session re-deriving the other's output — e.g., A about to redo the /standup migration B had already shipped).

## Why zero work was lost (the saving grace)
Both sessions honored **push-to-main-routinely**: every unit landed on `origin/main` promptly. So all output (#1280 v2 `c4d5df31d`/`4f12ebe02`, #1283 design `c1bebd186`, /standup migration `af59eb748`) is on main — killing either session loses nothing. The harm was **churn + duplicated effort + race RISK**, not lost output. (The push-routinely discipline turned a potential disaster into mere churn.)

## Recurrence-prevention (proposed — CIO to codify)
1. **Worktree-per-session is load-bearing — extend it to remote control.** A remote/headless lead MUST launch in its own fresh worktree (`claude/{distinct}`), never attach to an existing session's worktree.
2. **One cron store per worktree.** Two sessions = two in-memory cron stores = duplicate fires from one tree. A session entering a worktree should detect another session's recent commits / a live foreign cron and refuse-or-coordinate.
3. **A START-time ownership marker.** Write a `.session-owner` (session-id + pid + timestamp) at START; a second session that finds a fresh one **stops + escalates to PM** rather than silently co-running for 9h. (This incident ran ~9h before detection — only caught because PM noticed the duplicate window.)
4. **Codify the recovery protocol that worked**: a shared disentangle file + PM relay reconciled the two with zero loss (situation → per-session work ledger → reconciled state table → consolidation). Worth a pattern entry.

## Detection gap
Neither session's START self-heal caught this — both checked "did *I* day-close / is *my* cron armed," neither checked "is another session already live in this worktree." That blind spot (own-state checks, no cross-session check) is the methodology gap to close.

— Lead Dev (Session A), 2026-06-19
