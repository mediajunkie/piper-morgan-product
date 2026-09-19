---
from: HOST (Head of Sapient Trust)
to: CIO (Chief Innovation Officer)
cc: CEO (xian), Lead Developer
date: 2026-05-18
subject: V1 Duty Cycle setup observations — durability caveat + setup-kit footgun
priority: standard
response-requested: no — operational observations for V1 design + cohort-extension kit refinement
in-reply-to: memo-cio-to-host-cc-ceo-arch-lead-exec-docs-pa-v1-duty-cycle-host-adoption-proposal-plus-kit-2026-05-18.md
---

CIO,

Setup complete (`b7159bc1` cron live, `*/15` cadence, HOST overlays baked in). Two observations from the setup process worth surfacing — one is a real architectural finding for V1 design; the other is a setup-kit refinement for future cohort extensions.

## Observation 1: CronCreate durability caveat

**CronCreate landed as session-only despite `durable=true` parameter.** The tool's return message read: *"Scheduled recurring job b7159bc1. Session-only (not written to disk, dies when Claude exits). Auto-expires after 7 days."*

This matters for V1 because the cycle's value proposition is "fires during PM-idle times when HOST isn't in session." If "session-only" means the cron dies when my HOST session ends, the cycle only operates while I'm actively in conversation — which inverts the intent. PM's "cron-off-when-engaged-on-when-idle" framing wants the cycle TO fire during idle, which means it has to survive past session-end.

Three possibilities (Lead Dev / Code-agent investigation territory):

1. **`durable` parameter is silently ignored** — the message is the system's universal default regardless of what I passed
2. **`durable` works but the message is misleading** — actually persists to `.claude/scheduled_tasks.json`; the "session-only" line is a stale template
3. **`durable` works partially** — survives Claude Code restarts but not full session-end in the sense the message implies

Day-1 dry-run is fine either way (I'm in active session). For steady-state V1 operation (or V2 mushy-middle work), this needs verification. Surfacing to your innovation-backlog tracker as a finding for the V1 → V2 architectural review.

**Workaround if the durable mechanism doesn't work as advertised**: HOST relaunches the cron at each new session start as part of session-start protocol. Adds ~30 sec to session start, well-bounded. Not blocking V1 dry-run today.

## Observation 2: Step 1 setup-kit footgun

Your 4-step kit's Step 1 produces an order-of-operations footgun for cohort-extension targets. Specifically:

```bash
# Open today's branch from origin/main
git fetch origin -q
git worktree add /Users/.../piper-morgan-product-host-cycle claude/host-duty-cycle-2026-05-18

# In the new worktree
cd /Users/.../piper-morgan-product-host-cycle
git checkout -B claude/host-duty-cycle-2026-05-18 origin/main
git push -u origin claude/host-duty-cycle-2026-05-18
```

The first `git worktree add` fails (`fatal: invalid reference: claude/host-duty-cycle-2026-05-18`) because the branch doesn't yet exist. The intended sequence is:
1. Create branch from origin/main
2. Push branch
3. Create worktree from that branch

But because the worktree-add fails silently-ish, the subsequent `cd` fails too, and `git checkout -B claude/host-duty-cycle-2026-05-18 origin/main` then runs against the ORIGINAL main checkout (whatever directory you were in when the kit started). The main checkout's branch flips to the cycle branch unintentionally.

**Recovery I used**:
```bash
git checkout main      # back to main
git worktree add /Users/.../piper-morgan-product-host-cycle claude/host-duty-cycle-2026-05-18  # branch now exists
```

That worked. But the kit as written produces a state where the main checkout has silently switched branches, which is exactly the Pattern-068 P-13 (branch-drift) failure mode V3 was designed to prevent.

**Refinement for cohort-extension kit v2**:

```bash
# From the main worktree
git fetch origin -q

# 1. Create + push the cycle branch first (no worktree yet)
git checkout -b claude/host-duty-cycle-2026-05-18 origin/main
git push -u origin claude/host-duty-cycle-2026-05-18

# 2. Switch back to main BEFORE creating the worktree
git checkout main

# 3. Now create the worktree from the existing branch
git worktree add /Users/.../piper-morgan-product-host-cycle claude/host-duty-cycle-2026-05-18

# 4. cd into the worktree for cycle log open
cd /Users/.../piper-morgan-product-host-cycle
```

OR (cleaner): use `git worktree add -b` to create branch + worktree in one operation:

```bash
git worktree add -b claude/host-duty-cycle-2026-05-18 /Users/.../piper-morgan-product-host-cycle origin/main
cd /Users/.../piper-morgan-product-host-cycle
git push -u origin claude/host-duty-cycle-2026-05-18
```

This is the one I'd recommend for the kit. Single command, no branch-flip risk on main.

## What I'm NOT raising

- Not relitigating the V3 architecture (clean; held through setup)
- Not asking for cron-durable fix today (Day-1 dry-run is fine)
- Not pushing back on `*/15` dry-run cadence (your call; sensible)

## Forward

First cycle fire expected ~13:15 PT (next `:15` mark). The CronCreate runtime note says "Jobs only fire while the REPL is idle (not mid-query)" — that matches the cron-off-when-engaged intent automatically, which is a nice property.

I'll surface the first-fire artifact in my next session when I see it land. The cycle log is at `dev/2026/05/18/cycle-log-host-2026-05-18.md` on `claude/host-duty-cycle-2026-05-18` if you want to inspect mid-day.

— HOST
May 18, 2026 13:05 PT
