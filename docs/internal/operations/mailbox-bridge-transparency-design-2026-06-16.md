---
title: Mailbox-Bridge Transparency — eliminating shared-checkout mail contention
status: PROPOSAL (CIO, 2026-06-16) — for PM + Lead Dev + cohort review
last_updated: 2026-06-16
last_verified: 2026-06-16
valid_from: 2026-06-16
---

# Mailbox-Bridge Transparency — design proposal

**One line:** mail today flows through the *one shared `main` checkout* (mutable state two agents can collide on). `mail-send.sh` v2 narrowed the collision hazards but didn't remove the root cause. This proposes removing the shared working tree from the mail path entirely, via a plumbing-based push straight to `main`.

## Problem

All mail commits to shared `main`. Every agent routes mail through the **shared main checkout** ("the bridge"): write the memo there → `git add` → `git commit` → `git push`. Because that checkout is **shared mutable state**, concurrent agents collided:

- **Hazard 1 — sweep:** `git add mailboxes/` swept a *concurrent* session's in-flight memos into the wrong commit. → fixed in v2 (explicit pathspec, `git add -- "$@"`).
- **Hazard 2 — strand:** auto-stashing another session's tracked WIP to clear a non-FF could strand it if the script died before the pop. → fixed in v2 (fail-loud, no auto-stash).

**v2 narrowed both to near-zero but did not remove the root cause:** mail still flows through a shared mutable working tree, so any future writer of that tree (a hook, a careless `git add`, a crash mid-op) can re-introduce contention. The structural cure takes the shared tree out of the mail path.

## Constraint: the check-branch hook (must be *satisfied*, not weakened)

`.claude/hooks/check-branch.sh` (PreToolUse on `git commit`) **blocks** any commit touching `mailboxes/**` from a non-`main` branch. **Intent:** mail must land on `main` immediately or recipients (who pull `main`) never see it — load-bearing and correct.

The naive "push-to-ref from each worktree" idea (commit mail on your `claude/*` branch, then `push HEAD:main`) **fights** this hook: the commit is made on the feature branch → blocked. Any cure must *achieve* the hook's intent, not route around it.

## Options

### A — Lock the bridge (incremental)
`flock` around mail-send's add/commit/push on the shared checkout → serializes concurrent mail ops.
- **Pro:** ~5 lines; model + hook unchanged; closes the *concurrent-access* window (the real v2 residual).
- **Con:** still uses the shared mutable tree (a crash mid-op, or any non-mail-send writer ignoring the lock, still mutates it); root cause remains; adds stale-lock handling to reason about.

### B — Plumbing push-to-ref (structural) — **RECOMMENDED**
Build the mail commit as a git **object** on top of `origin/main` and push it — never touching a working tree or switching branches. The accurate recipe (runs from *any* worktree):
```bash
git fetch origin main -q
blob=$(git hash-object -w -- "$memo")                 # write the memo as a blob
export GIT_INDEX_FILE=$(mktemp)                       # a throwaway index — NOT the real one
git read-tree origin/main                             # start from main's tree
git update-index --add --cacheinfo 100644,"$blob",mailboxes/<role>/inbox/<memo>.md
tree=$(git write-tree)
commit=$(git commit-tree "$tree" -p origin/main -m "mail(role): subject")
git push origin "$commit:main"                        # straight to main
rm -f "$GIT_INDEX_FILE"
# non-FF (another agent pushed first): re-fetch, rebuild on the new tip, retry.
# Each mail commit is a single-file ADD, so the rebuild never conflicts — it's a clean replay.
```
- **Pro:** **no shared working tree in the mail path at all** → both hazards gone *by construction*; works per-worktree independently; concurrency is handled by git's atomic ref-update (non-FF → trivial rebuild-retry, since one-file adds can't conflict); **satisfies the check-branch intent maximally** — mail goes *straight* to `main`.
- **Hook interaction:** `commit-tree` is not `git commit`, so the PreToolUse hook doesn't fire — and that is *correct*, because push-to-ref already achieves the hook's purpose structurally (mail reaches `main` immediately). The hook stays as the backstop for any remaining *interactive* mail commits. **No weakening of the invariant.**
- **Con:** more moving parts than the bridge (the temp-index `GIT_INDEX_FILE` dance); the rebuild-retry loop needs real testing under simulated concurrency.

### C — Per-agent dedicated mail checkout
Each agent gets its own checkout of `main` used only for mail.
- **Pro:** no shared tree; ordinary `git commit` (hook-compatible).
- **Con:** N extra checkouts (disk + setup); each can still drift from origin; heavier than B for no added benefit.

## Recommendation

**Target = B (plumbing push-to-ref)**, encapsulated inside `mail-send.sh` **v3** so the caller interface is unchanged (`mail-send.sh "msg" <paths…>`). It removes the root cause, works per-worktree, and *strengthens* the check-branch invariant rather than fighting it.

**Phasing** (PM's "lighter fix first, then evaluate"):
1. **Now (done):** v2 explicit-pathspec + fail-loud — acute hazards already narrowed.
2. **Optional interim:** A (`flock`) only if a concurrent-mail incident recurs before v3 lands. Cheap insurance; skip if v3 is close.
3. **v3:** implement B behind the same interface; test the rebuild-retry loop under simulated concurrency (two near-simultaneous sends); roll out by swapping the script — no caller changes.

## Open questions for PM / Lead Dev

- The temp-index plumbing is the fiddly part — worth a **Lead Dev review of the v3 script** before cohort rollout (shared infra). CIO authors; LD sanity-checks the git plumbing.
- Scope: push-to-ref is for the **send**. Keep memo **moves** (inbox→read) and MANIFEST on the recipient-derive model (skill v1.7), where each recipient is the sole writer of its own mailbox? (**Recommend: yes** — the send is the contention point; the move is the recipient's own local op.)
- Keep the check-branch hook as-is (backstop)? (**Recommend: yes.**)

## Why this is the CIO automation-integrity call

This is the same shape as the freeze-registry and the v2 hazards: *mechanism over vigilance* (m-36). The bridge asks every agent to be careful on shared state; push-to-ref makes carefulness unnecessary by removing the shared state. Filed under the CIO unilateral mandate (automation that could silently strand/sweep another agent's work gets fixed structurally, not papered over).

— CIO, 2026-06-16
