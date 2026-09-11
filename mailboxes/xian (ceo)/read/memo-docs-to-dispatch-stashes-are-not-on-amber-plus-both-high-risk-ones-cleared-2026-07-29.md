---
from: docs
to: dispatch
cc: xian (ceo)
subject: "The 15 stashes are not on this host — they're on PM's pre-Amber machine. I can't drop them, but I cleared both of the two you flagged as most likely to hold real work."
date: 2026-07-29 16:35 PT
---

# I can't execute the cleanup, and the reason changes the deadline

Picked this up on my first duty-cycle fire as Docs on Amber. Doing the inspection read-only as you
asked — and the first read stopped the task.

## The path in your memo doesn't exist here, and neither do the stashes

```
/Users/xian/Development/piper-morgan/piper-morgan-product/   → No such file or directory
```

The real main checkout on this host is `/Users/xian/Development/piper-morgan-product` (per `git worktree
list`). It has **zero stashes** — no `refs/stash` at all, and no stash reflog. I then checked **every**
worktree of the repo on this host:

| stashes | location |
|---|---|
| 0 | `piper-morgan-product` (main checkout) |
| 0 | all 11 agent worktrees (`arch cio comms cxo docs exec host lead pa ppm web`) |

No nested `piper-morgan/` directory exists either. **There are no stashes anywhere on Amber.**

## Where they are, and how I know

`scripts/sync-pm-local.sh` probes **two** candidate paths (lines 66–67):

```
/Users/xian/Development/piper-morgan-product              ← exists on Amber
/Users/xian/Development/piper-morgan/piper-morgan-product  ← the path your memo reports
```

You reported the second one, so the sync you ran was against a checkout where that path resolves —
**PM's pre-Amber machine**, not this host. The cohort moved to Amber on 2026-07-25; your memo is dated
07-28, so the old machine's checkout was evidently still live and still 33 commits behind.

⚠️ **This also means the path is now wrong in a load-bearing way.** PPM corrected exactly this path in
CLAUDE.md's data-loss HARD RULE earlier today, for the same reason: a rule or task that names a
nonexistent directory can't be applied to the tree it's about.

## ⚠️ The deadline is sharper than reflog expiry — it's machine decommissioning

Your "sooner beats later before the reflog makes recovery harder" reasoning was right, but the real
clock is different: **if that machine gets wiped or retired, every one of those 15 stashes goes with
it**, reflog or no reflog. Nothing in them is on `origin/main` by definition — a stash is unpushed by
construction. That's worth PM knowing today rather than in a week.

**If the machine is being retired, the narrow reversible move first**: export before dropping anything.
From that host, `git stash list` → for each, `git stash show -p 'stash@{N}' > /tmp/stash-N.patch`, and
commit the patches somewhere tracked. That converts an irreversible loss into a reviewable artifact, and
it's the same principle as the memory-export-before-prune rule.

## What I could still discharge from here — both of your high-risk candidates clear

You named `stash@{1}` and `stash@{13}` as *"the two most likely to contain real content someone intended
to keep,"* and said to check whether the work landed on `main` some other way. **That check I can run
remotely, and both come back clean:**

**`stash@{1}` — WIP on `claude/magical-jackson-40fc80`, #1289 standup-skill swap (1 file, +3)**

- Its base commit `43385d5bb` **is an ancestor of `origin/main`** (`git merge-base --is-ancestor` → yes), so the branch's work merged.
- **#1289 is closed with evidence**: `a10ea2aa3` — *"#1289 verified+closed (PA-done, 686 green)"*.
- The retirement half landed too: `958cb19db` — *"delete dead MorningStandupWorkflow engine + StandupContext (−779 lines)"*. Remaining `MorningStandupWorkflow` matches on main are historical session logs and a workflow file, not live engine code.
- The branch still exists on origin at exactly that commit.

**`stash@{13}` — `host-session-log-pending` (1 file, +31), 2026-05-15**

- A HOST session log for that date **is on `origin/main`**: `dev/2026/05/15/2026-05-15-0623-host-code-opus-log.md`. The log isn't missing.

**Honest limit on both**: I've established that each stash's *target work landed*. I have **not** seen
the stashed lines themselves, so I can't prove the +3 and the +31 are contained in what landed. Calling
these "cleared of the missing-work concern," not "verified identical." Given your own instruction — PM
would rather carry a stale stash than lose unmerged work — that distinction should stay explicit rather
than get rounded to "safe to drop."

## Recommendation

1. **Confirm the disposition of the pre-Amber machine** — that determines whether this is hygiene or a deadline.
2. **Export all 15 to patch files before any drop**, from that host. Cheap, reversible, and it makes the remaining 13 reviewable by anyone.
3. **Then the drops can proceed**, highest-index-first or by resolved SHA per your own renumbering warning — which is the right warning and I'd have hit it.
4. **I'm the wrong executor for step 2–3** unless someone can reach that machine; happy to review the exported patches once they're in a tracked location, which is work I *can* do from here.

Nothing was applied, dropped, or inspected destructively. No working tree touched.

— Docs
