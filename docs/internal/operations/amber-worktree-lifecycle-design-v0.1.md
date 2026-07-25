# Amber per-agent worktree lifecycle — create / freshness / cleanup (v0.1 PROPOSED)

**Status**: PROPOSED — CIO draft for Pard, 2026-07-25. Not ratified. Gate on the remaining cohort migration.
**Authors**: CIO (Piper Morgan) — design; Pard (Mediajunkie) — owns `amber-agent.sh` implementation.
**Context**: `dev/2026/07/25/2026-07-25-1053-cio-code-log.md` (first-session findings), `mailboxes/cio/inbox/memo-pard-to-cio-cc-xian-exec-host-findings-verified-symlink-dropped-2026-07-25.md` (Pard's verification).

---

## Why three rules and not one

A create-rule without a cleanup-rule accumulates silently until the accumulation is its own problem — methodology-35, the asymmetric-discipline shape Janus already flagged on Pard's runbook. The old machine's ~30 stale worktrees are that shape having run to completion. Amber currently has **two** worktrees and zero prunable ones, so this is preventive, not remedial — which is the cheap moment to get it right.

The freshness rule is the third leg because staleness is the failure mode that *looks like working state*. A stale worktree throws no error; it just quietly hands the agent a six-week-old CLAUDE.md. That happened on the first migration (5,393 commits) and it should have been impossible.

---

## The distinction that shapes everything: standing vs. ad-hoc worktrees

These are two different objects and the lifecycle rules differ. Conflating them is how a reaper eats something it shouldn't.

| | **Standing** (per-role) | **Ad-hoc** (per-task) |
|---|---|---|
| Path | `~/Development/piper-morgan-worktrees/{role}` | `~/Development/piper-morgan-worktrees/_tmp/{slug}` |
| Branch | `claude/{role}-cycle` | `claude/{slug}` |
| Lifetime | **Indefinite** — reused across every session | Single task |
| Path stability | **Load-bearing** — Claude Code keys per-path state (transcripts, and historically memory) to the full path | Irrelevant |
| Auto-reap? | **NEVER** | Yes, under the gates below |

**The standing worktree must never be auto-removed.** Its path stability is exactly what makes it work — recreating it at a new path orphans accumulated per-path state, which is the failure the handoff warned about. Retiring a standing worktree is a deliberate human decision (a role is being decommissioned), never a sweep's call.

This means **the reaper's real target is the ad-hoc class**, plus reporting on standing worktrees that look wrong. That's a narrower and much safer mandate than "prune worktrees whose tmux session is gone."

---

## Rule 1 — CREATE (really: *ensure*)

Because standing paths are stable and reused, "create" is misleading. The operation is **ensure-exists-and-current**, and it must be **idempotent**: running it against a healthy existing worktree is a no-op that returns success, not a recreate.

```
ensure_worktree(role):
  path   = ~/Development/piper-morgan-worktrees/{role}
  branch = claude/{role}-cycle

  git -C <repo> fetch origin                 # MUST come first — see Rule 2
  if path exists and is a valid worktree:
      goto Rule 2 (freshness)                # reuse; never recreate
  if branch exists on origin:
      if branch is an ancestor of origin/main:
          fast-forward it to origin/main
      else:
          FAIL LOUD — branch has diverged/unmerged work; a human decides
  else:
      create branch at origin/main
  git worktree add <path> <branch>
  goto Rule 2
```

**Cut from `origin/main`, never from whatever the branch last pointed at.** The June-12 `claude/cio-cycle` leftover is the whole reason this rule exists.

**Assert before handing over**: the worktree's basename appears in its branch name. Cheap, and it's the fingerprint that caught the old provisioning defect.

---

## Rule 2 — FRESHNESS (the currency-assert)

Runs on every hand-over, including reuse of an existing worktree. This is the rule that was missing.

```
assert_current(path):
  git -C <repo> fetch origin                 # a stale fetch makes the assert meaningless
  behind = git -C <path> rev-list --count HEAD..origin/main
  if behind == 0: PASS
  else:
      if working tree is clean and HEAD is an ancestor of origin/main:
          fast-forward; re-assert; PASS
      else:
          FAIL LOUD with the specific reason; do NOT hand over
```

Three properties that matter:

1. **Fetch first.** Asserting currency against a stale remote-tracking ref proves nothing. The 5,393-commit gap would have passed a no-fetch check on a stale `origin/main`.
2. **Never auto-discard working-tree state.** If the tree is dirty, the script **surfaces and stops** — it does not stash, reset, or checkout. Uncommitted work in a standing worktree is legitimate carry-over from the prior session, and PM's directive after the 2026-07-05 incidents is explicit that irrevocable actions need a pause, not a default. *(I discarded 26 files of mechanical MANIFEST regen by hand this morning — that was a judgment call about regenerable artifacts. A script should not make that call; it should show the agent the list and let them decide.)*
3. **Fail loud, not quiet.** A stale worktree should be a startup error the agent cannot miss, not a condition they discover six weeks in.

---

## Rule 3 — CLEANUP (the reaper)

**Default action on any doubt is REPORT, not REMOVE.** The reaper's job is to keep the worktree set honest; the merge-keeper sweep's job is to rescue stranded work. The reaper should *feed* the merge-keeper, not race it.

**Reap an ad-hoc worktree only if ALL five gates pass:**

1. No live tmux session whose cwd is that worktree
2. Working tree clean — no modified, no staged, no untracked-that-aren't-ignored
3. Zero unpushed commits — `git log @{u}..HEAD` empty
4. Zero commits not on `origin/main` — `git rev-list --count origin/main..HEAD` == 0
5. Idle beyond a grace period (proposal: **7 days** since last commit *and* last mtime)

**If gates 2–4 fail, do not reap. Emit a `STRANDED` report naming the worktree, the branch, and exactly what's at risk** (N uncommitted files / N unpushed commits / N commits not on main). That report is merge-keeper input. Gate 1 alone failing means "in use" — skip silently.

**Two-phase, never single-shot.** Run 1 marks a candidate; Run 2 removes it only if it was *also* clean on the previous run. A worktree can be momentarily clean mid-session; a two-run confirmation makes a transient state un-reapable. This costs one cycle of latency and buys immunity to the entire class of "reaped something that was just between commits."

**Standing worktrees are never reaped** — they're only ever *reported* if they trip gates 2–4 while idle, which is a signal that a role signed off without pushing.

Why the gates are this strict: Lead's 59-line session log sat stranded on a branch for ~2 months and was only found by a hand audit. A reaper that had "cleaned up" that branch would have destroyed it silently. **The asymmetry is total** — a worktree left alive one extra week costs some disk; a worktree reaped with unpushed work costs unrecoverable institutional memory.

---

## Open question for Pard: what "collision" means now

`duty-cycle-tick` Step 2a's collision check (branch name must contain the worktree's basename) was built for Model B. It happens to still pass here — but its *reasoning* no longer applies, and it now detects the wrong thing.

Under stable per-agent worktrees, a collision is **two live sessions sharing one worktree path** — which the basename check cannot see at all. Candidate detections, cheapest first:

- **tmux-side (preferred)**: count live sessions whose cwd is this worktree. >1 is a collision. Pard owns this surface and it needs no in-repo state.
- **In-worktree lockfile**: a gitignored `.agent-session` holding the owning session ID + PID, written at START. Detects the case tmux can't see (two Claude Code processes not under distinct tmux sessions).
- **Reflog remains the forensic tell**, not the detector — `commit:`/`rebase (pick):` entries you don't recognize mean someone else operated here. Good for confirming after the fact; too slow as a gate.

My inclination is tmux-side as the gate plus reflog as the forensic check, and to **retire the basename fingerprint** rather than leave a Model-B artifact firing on Model-A assumptions. Wanted your read before I change the skill, since detection lives on your side of the seam.

---

## What I'd need to change on the Piper Morgan side

- `duty-cycle-tick` Step 2a — replace the Model-B fingerprint per the above (blocked on Pard's read).
- `CLAUDE.md` — still says **"Model A … is DEPRECATED — no current exceptions"** in three places (lines ~88, ~533, ~575). This is now backwards for Amber and every migrating agent reads it. **Flagged to PM; not editing unilaterally** since CLAUDE.md is a shared behavioral contract, not a status doc.
- The session-start memory-scope verification check — **cancelled**, per Pard's finding that shared-by-construction removes the failure mode it was designed to catch.
