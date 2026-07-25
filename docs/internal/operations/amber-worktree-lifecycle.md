# Amber per-agent worktree lifecycle — create / freshness / cleanup / verify

**Version: v0.2** (2026-07-25). *The version lives in this header, not in the filename — a versioned filename means every inbound link goes stale on each bump, which is the drift this cohort keeps re-learning. This file was `…-design-v0.1.md`; it is now the single canonical path.*

**v0.2 adds Rule 4 (verify hooks fire).** See that section; it exists because Finding #4 proved that a present, correct, registered hook can still be inert, and Finding #5 proved a documented safety net can sit unwired for ten weeks while the docs assert it works.

---


**Status**: **RATIFIED 2026-07-25** (CIO), implemented and tested by Pard the same day. Supersedes the PROPOSED draft.

**Ratification decisions** (the two knobs Pard deliberately left unbuilt rather than bake in unratified):
- **7-day grace period — ADOPTED.** Principled rather than arbitrary: session crons auto-expire after 7 days, so a worktree whose session has been dead a week has also lost its self-wake and is genuinely dead rather than merely quiet.
- **Two-phase confirmation — ADOPTED.** Mark on run 1, remove only if still clean on run 2.
- **`.agent-session` lockfile — DECLINED for now.** Every agent launches via `amber-agent`→tmux, so the tmux-cwd gate covers the real path; the lockfile carries its own asymmetric-discipline trap (a crashed session leaves a stale lock that blocks legitimate relaunch, so it needs PID-liveness checking to be safe). Revisit only if a non-tmux Claude process is actually observed on Amber — abstractions earn their place by recurring.
- **Collision = two live sessions whose cwd is the same worktree, gated tmux-side. The Model-B basename fingerprint retires.**

**Two bugs this design caught in Pard's implementation before they met a real branch**: (1) the first reaper would have removed *any* session-less clean worktree — including a standing per-role one, orphaning its per-path state; (2) the create path used `git worktree add -B <branch> origin/main`, which silently discards un-merged branch commits. Both fixed and verified.

**⚠️ Open — a fourth assertion this spec still needs**: *verify hooks actually fire* before handover. Project hooks did **not** fire in the first Model-A worktree (`check-branch.sh` failed to block a `mailboxes/` commit from a feature branch; the hook works standalone and is correctly registered — the harness never invoked it). Presence of `.claude/settings.json` proves nothing; an absent hook and a silent hook are indistinguishable from inside. The assertion's shape depends on which fix is chosen (trust-accept per worktree vs. lifting hooks to user-level settings), so it lands in v0.2. **This gates the bulk cohort migration** — see the memo trail.
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

## Rule 4 — VERIFY (hooks actually fire) *(added v0.2)*

**Runs once at each agent's first session in a worktree, before the agent is trusted to operate unsupervised.** HOST widened this from "agent #2 only" to *every* subsequent agent's first session (ruling 2026-07-25) — hooks get verified as firing, never assumed.

**Config presence proves nothing.** This is the entire lesson of Finding #4: `check-branch.sh` was present in the worktree, correctly registered under `PreToolUse` with a well-formed matcher, and executed correctly when invoked by hand — and still never ran. Reading `settings.json` would have told you everything was fine. Only behavior tells the truth.

```
verify_hooks(worktree):
  # in the worktree, on a NON-main branch
  touch mailboxes/<role>/read/.hookprobe
  git add -f mailboxes/<role>/read/.hookprobe
  git commit -m "hook probe"        # ← MUST be blocked
  # PASS  = commit refused (check-branch.sh exit 2, BLOCKED message shown)
  # FAIL  = commit succeeds, OR no output at all
  git restore --staged mailboxes/<role>/read/.hookprobe
  rm -f mailboxes/<role>/read/.hookprobe
```

⚠️ **CORRECTED 2026-07-25 (same day): a bare block is NOT the pass. Read the output.**

| Result | Verdict |
|---|---|
| Refused with **check-branch.sh's own text** (`BLOCKED: You are on branch '<x>' and trying to commit mailbox files`) | ✅ **PASS** |
| Commit **succeeds**, or refused with **no output** | ❌ **FAIL** — stops the migration |
| Refused by the **permission classifier** (`Permission for this action was denied by the Claude Code auto mode classifier`) | ⚠️ **INCONCLUSIVE** — gate stays closed |

**Why this correction matters more than the rule it fixes.** The original wording was *"a block is the pass."* Lead Dev ran the probe the same day it shipped and the **permission classifier intercepted the commit before git hooks could run** — producing a refusal that looks identical to success from the outside. So the pass signal was producible by something other than the mechanism under test.

That is precisely the false-confidence shape this rule exists to catch — **occurring inside the verification protocol itself.** A check whose pass condition has an alternate cause is not a check; it is a second thing to verify. The corrected rule keys on the hook's *distinctive output*, which nothing else produces.

**Do not work around a classifier denial** to force the probe through — that defeats the denial's intent and converts an honest inconclusive into a manufactured pass. Report inconclusive, leave the gate closed, and enforce manually until a clean seat is available. Do not proceed to the next agent on a fail *or* an inconclusive.

### ★ PRECONDITION — the gate needs a clean seat, and "clean" means two things

*(Named 2026-07-25 after Lead Dev's inconclusive run. I should have stated this when I wrote the rule.)*

> **Run the gate only on a session that is BOTH (a) fresh — started after the hooks were wired, so it actually loaded them — AND (b) on a seat where `git commit` is not permission-gated.**

Miss (a) and a non-block is meaningless (the session never loaded the hooks). Miss (b) and the probe can't reach the hook layer at all — the classifier intercepts first, and the only honest verdict is inconclusive.

**Check (b) before spending the probe.** A trivial no-op commit answers it for free. If that prompts, the gate cannot run on that seat — say so cleanly rather than burning the probe and then having to explain an ambiguous result.

**Corollary — any qualifying session is a valid gate seat, not just the designated migrant.** If agent #2's seat turns out to be permission-gated, that is a *seat* problem, not evidence the fix is broken, and any other fresh+ungated session can run it. Don't re-litigate the fix on a bad seat.

Two properties worth stating because they're what make this rule work:

- **It is a negative-signal check, and negative signals are the ones that rot undetected.** An absent hook and a silent hook are indistinguishable from inside a session; there is no error, no log line, nothing. That's why this has to be an *action* with an expected refusal, not an inspection.
- **It is cheap and it is idempotent.** Ten seconds, no state left behind, safe to re-run. Anything more expensive would get skipped, which would reproduce the failure it exists to catch.

**Re-run it after any change to hook configuration** — including the move to user-level `~/.claude-pm/settings.json`. A config edit that *looks* right is exactly the condition under which this check earns its keep.

### The companion discipline: mirror + atomic update

The user-level fix (HOST-approved 2026-07-25) moves enforcement config out of the repo, so two conditions ride with it:

1. **A tracked, non-executing mirror** at `docs/internal/operations/amber-userlevel-hooks-mirror.json`, headed with an explicit statement that it is a reference copy of `~/.claude-pm/settings.json` and that the live copy is edited first. This keeps the config diffable and Docs-sweepable even though the executing copy is machine-local.
2. **Atomic update**: any agent modifying the live settings updates the mirror **in the same session**. HOST's reasoning is the load-bearing part — *a mirror that is current at creation and then drifts is not addressing the reviewability concern, it just looks like it is.* A stale mirror is worse than none, because it reads as verification.

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
