# INCIDENT — two lead sessions forked into one worktree (2026-06-19)

**For**: CIO (methodology codification) · **From**: Lead Dev · **PM-requested.**
**Reconciliation detail**: `dev/active/SESSION-FORK-DISENTANGLE-2026-06-19.md`.

## What happened
Two Claude **lead** sessions ran concurrently in the **same worktree** (`interesting-beaver-7ee19c`) on the **same branch** (`claude/interesting-beaver-7ee19c`) for ~9 hours (6/18 ~23:00 → 6/19 ~08:1x). Both wrote the same `…-0707-lead-…` session log + the same `dev/active/lead-carry-forward.md`, shared one running server (PID 39025), and pushed to `origin/main`.
- **Session A** — interactive; PM-prompted 07:07 START; commits carry **no** `Claude-Session` trailer; cron suspended. Did: #1280 v2 shell rebuild + deploy + the CXO/Arch/#1284 mail.
- **Session B** — autonomous/remote; cron `8278cd31`; commits stamped `Claude-Session: …01C3…` + `Co-Authored-By: Claude Opus 4.8`; resumed from the 6/18 22:52 day-close via the 07:17 cron. Did: #1283 resolver-shape design + #1269 /standup page migration.

## Root cause — UNDETERMINED (do not over-attribute; needs investigation)
A **fork of an earlier lead session** into two live processes sharing one worktree / branch / index / server / log / carry-forward — the failure mode the worktree-per-session rule (CLAUDE.md §"Git Worktrees") exists to prevent. **But the *trigger* is not yet known, and should not be codified prematurely.**

Notably, the fork is **NOT** explained by the morning's remote-control change: Session B's commits begin **6/18 23:00 — hours before** that change. So remote control is most likely a red herring; do **not** record it as the cause.

**PM's working hypothesis (a lead to investigate, NOT a conclusion):** a laptop **battery-death yesterday** left sessions paused with their crons halted; PM then **directly resumed a paused conversation** (this thread), and around the same time a **cron revived on the terminal surface** so the paused session resumed *in parallel* — forking the original session into two. This is a **harness-interaction effect** (session pause/resume + session-scoped-cron lifecycle across the power event), entangled with how the Anthropic harness handles suspend/resume — genuinely tricky to pin down. **Treat the mechanism as open until investigated.**

## Symptoms (the pattern signature)
- Shared `lead-carry-forward.md` header + cron/PID field **drifting** (two writers fighting one field).
- The `0707-lead` session log appearing **"ahead"** of each session's own view (interleaved authors; the on-disk state ran ahead of each post-compaction summary).
- Stray `pa/inbox` deletions + MANIFEST regen-noise in the main checkout (one session's mailbox-bridge ops seen by the other as foreign changes).
- **Verify-first repeatedly catching "work already done"** (each session re-deriving the other's output — e.g., A about to redo the /standup migration B had already shipped).

## Why zero work was lost (the saving grace)
Both sessions honored **push-to-main-routinely**: every unit landed on `origin/main` promptly. So all output (#1280 v2 `c4d5df31d`/`4f12ebe02`, #1283 design `c1bebd186`, /standup migration `af59eb748`) is on main — killing either session loses nothing. The harm was **churn + duplicated effort + race RISK**, not lost output. (The push-routinely discipline turned a potential disaster into mere churn.)

## Recurrence-prevention (proposed — CIO to codify)
1. **Worktree-per-session is load-bearing (containment).** Whatever spawns OR *resumes* a lead — a cron revival, a manual resume, a remote attach — should land in its OWN worktree, never co-occupy an existing one. This limits blast radius even if the fork trigger itself can't be fully prevented (it's a mitigation, not necessarily a cure — see open root cause).
2. **One cron store per worktree.** Two sessions = two in-memory cron stores = duplicate fires from one tree. A session entering a worktree should detect another session's recent commits / a live foreign cron and refuse-or-coordinate.
3. **A START-time ownership marker.** Write a `.session-owner` (session-id + pid + timestamp) at START; a second session that finds a fresh one **stops + escalates to PM** rather than silently co-running for 9h. (This incident ran ~9h before detection — only caught because PM noticed the duplicate window.)
4. **Codify the recovery protocol that worked**: a shared disentangle file + PM relay reconciled the two with zero loss (situation → per-session work ledger → reconciled state table → consolidation). Worth a pattern entry.
5. **Doppelgänger check (PM's idea) — if we can't prevent the fork, detect it fast.** Have agents periodically (not just at START) verify they're not running as a clone sibling: on a heartbeat, check for another live process / a second cron / fresh foreign commits in the same worktree, and STOP + escalate on a match. This caps the ~9h undetected window even when the trigger is a harness suspend/resume race we can't fully control. **This is the most robust mitigation if the root cause proves unpreventable.**

## Detection gap
Neither session's START self-heal caught this — both checked "did *I* day-close / is *my* cron armed," neither checked "is another session already live in this worktree." That blind spot (own-state checks, no cross-session check) is the methodology gap to close.

## Open investigation (the mechanism is unknown — investigate before codifying a cause)
PM's priority: **don't let it recur** — which needs the mechanism understood, not guessed. Threads to pull:
- The **battery-death event** yesterday and how sessions were paused / resumed around it.
- **Session-scoped cron lifecycle across suspend/resume**: can a paused session's cron "revive" and run the session in parallel with a freshly-resumed copy of the same session? (How the Anthropic harness handles suspend/resume + session crons is central — and the hard part.)
- The exact fork moment: B's first trailered commit is **6/18 23:00** — reconstruct what happened on each surface at that point.
This is harness-level + tricky; if it can't be reliably prevented, the **doppelgänger check (#5)** + worktree containment (#1) are the fallback.

— Lead Dev (Session A), 2026-06-19

## Food for thought (PM, 2026-06-19): parallel *developers* vs. parallel *leads*
PM wants this question on the record (not an urgent change — reflection):

**The invariant: exactly ONE lead, always.** The lead coordinates — sequencing, integration, the carry-forward, the cron. Two *leads* (what happened here, by accident) = two coordinators with no subordination, racing the same shared state. That's the failure mode.

**The legitimate parallel model (we've used it before): one lead + dedicated developer(s).** For an unblocked, well-bounded task, the lead dispatches a *developer* (reporting to the lead) to work it **in its own worktree**, check the work in, and report back — the lead integrates. The subordination + the separate worktree are what make it safe; it's structurally different from two co-equal leads in one tree.

**So:** parallel *developers under one lead, each in their own worktree* = fine and useful. Parallel *leads* = the anomaly we just healed.

**Note for the design:** the existing duty-cycle + worktree-per-session model already supports the dispatched-developer pattern (own worktree, check-in, the lead integrates). What broke here wasn't that model — it was an accidental duplication of the *lead* role into one shared tree. So the methodology gap is narrow: **prevent accidental lead-duplication** (the START-time ownership marker above), while keeping the door open to *intentionally* spinning up lead-coordinated developers when there's unblocked parallel work. Net effect of this incident was benign — extra work got done, no harm — which is itself a small signal that lead-coordinated parallelism is worth designing deliberately.

— added at PM's request, Session A, 2026-06-19
