#!/usr/bin/env bash
# worktree-safety-sweep.sh — content-based safety classification for orphaned subagent worktrees.
#
# Standing-item 7r (2026-09-06, PM-directed via Exec, off #1722). PM asked for a proposal on
# directing subagents to clean up after themselves, or being accountable when they don't. Exec's
# finding on #1722 (91 orphaned worktrees / 36 GB under .claude/worktrees/) supplied the shape:
# a dispatching session commits the subagent's work to main and abandons the worktree scaffolding.
# Exec sampled 20 of 91 (0 dirty, 18 "unmerged" that traced to real shipped work) and proposed a
# content-based test rather than a merged-ness test, because ahead/behind reports BRANCH divergence,
# not lost CONTENT — every one of these branches is months old and will read "unmerged" whether or
# not its content ever reached main.
#
# This checks ALL worktrees, not a sample — methodology-51 (filed the same morning this was scoped)
# is explicit that a bounded sample isn't a total, and Exec's own follow-up memo named their 20-of-91
# sample as exactly the thing that entry warns against. The one real precedent for caution (the
# 2026-09-03 #1602 recovery — genuinely stranded content, found by accident) is exactly the case a
# sample can miss, so the whole point of this script is to make that case findable by mechanism.
#
# Method: `git cherry <upstream> <branch>` lists commits on <branch> not reachable from <upstream>
# (prefixed '+') vs already-applied-by-content (prefixed '-', via patch-id, so a rebased-then-merged
# commit still counts as landed). This is CONTENT-based, unlike ahead/behind, which is REF-based.
#
# Output states, one line each, on stdout:
#   SAFE-TO-REMOVE <path> <branch> — every commit on this branch is already on <upstream> by content.
#   UNMERGED-CONTENT <path> <branch> — N commit(s) NOT reachable from <upstream>. DO NOT remove
#     without recovering this content first (the 2026-09-03 #1602 shape).
#   DIRTY <path> <branch> — uncommitted changes on disk. DO NOT remove.
#   UNRESOLVED <path> [<branch>] — detached HEAD, or `git cherry` itself failed. Reported so it is
#     never silently treated as safe.
#
# ALWAYS prints a denominator line on stderr (m-44/m-51 discipline: never let a partial count stand
# in for the total) — states how many worktree directories exist on disk vs how many `git worktree
# list` reported vs how many this run actually classified, and WARNS if they disagree rather than
# silently trusting `git worktree list`'s view of the world.
set -uo pipefail

REPO="${WORKTREE_SAFETY_REPO:-/Users/xian/Development/piper-morgan-product}"

if [ ! -d "$REPO/.git" ] && [ ! -f "$REPO/.git" ]; then
  echo "worktree-safety-sweep: ERROR — '$REPO' is not a git repo; this check measured NOTHING." >&2
  exit 3
fi
# Canonicalize to the resolved path (macOS: /tmp and /var are symlinks into /private/...). `git
# worktree list` always reports REAL paths, so comparing against an un-resolved $REPO silently
# matches nothing — found live while testing this script against a mktemp fixture, not a
# hypothetical: every worktree path failed to match and the run reported "checked 0" with no error.
REPO="$(cd "$REPO" && pwd -P)"
WTDIR="${WORKTREE_SAFETY_DIR:-$REPO/.claude/worktrees}"
WTDIR="$(cd "$WTDIR" 2>/dev/null && pwd -P || echo "$WTDIR")"
UPSTREAM="${WORKTREE_SAFETY_UPSTREAM:-origin/main}"

git -C "$REPO" fetch origin main -q 2>/dev/null || true

# Independent denominator: what's actually ON DISK, regardless of what git worktree list reports.
# A directory git doesn't know about (e.g. its .git worktree link was manually deleted) would be
# silently invisible to the git-worktree-list-driven loop below; counting the disk separately makes
# that gap visible instead of assumed away.
dir_total=0
if [ -d "$WTDIR" ]; then
  dir_total=$(find "$WTDIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
fi

checked=0; n_safe=0; n_unmerged=0; n_dirty=0; n_unresolved=0

wpath=""; wbranch=""
while IFS= read -r line; do
  case "$line" in
    worktree\ *) wpath="${line#worktree }" ;;
    branch\ *) wbranch="${line#branch }"; wbranch="${wbranch#refs/heads/}" ;;
    "")
      [ -z "$wpath" ] && continue
      case "$wpath" in
        "$REPO") wpath=""; wbranch=""; continue ;;                 # skip the main worktree itself
        "$WTDIR"/*) ;;                                              # only worktrees under WTDIR
        *) wpath=""; wbranch=""; continue ;;
      esac
      checked=$(( checked + 1 ))
      if [ -z "$wbranch" ]; then
        echo "UNRESOLVED $wpath — detached HEAD, no branch to check content against $UPSTREAM"
        n_unresolved=$(( n_unresolved + 1 ))
        wpath=""; wbranch=""
        continue
      fi
      if [ -n "$(git -C "$wpath" status --porcelain 2>/dev/null)" ]; then
        echo "DIRTY $wpath $wbranch — uncommitted changes on disk, do not remove"
        n_dirty=$(( n_dirty + 1 ))
        wpath=""; wbranch=""
        continue
      fi
      cherry_out=$(git -C "$REPO" cherry "$UPSTREAM" "$wbranch" 2>/dev/null)
      cherry_rc=$?
      if [ "$cherry_rc" -ne 0 ]; then
        echo "UNRESOLVED $wpath $wbranch — 'git cherry $UPSTREAM $wbranch' failed (rc=$cherry_rc)"
        n_unresolved=$(( n_unresolved + 1 ))
        wpath=""; wbranch=""
        continue
      fi
      unmerged_n=$(printf '%s\n' "$cherry_out" | grep -c '^+' || true)
      if [ "${unmerged_n:-0}" -gt 0 ]; then
        echo "UNMERGED-CONTENT $wpath $wbranch — $unmerged_n commit(s) not reachable from $UPSTREAM by content; DO NOT remove without recovering first"
        n_unmerged=$(( n_unmerged + 1 ))
      else
        echo "SAFE-TO-REMOVE $wpath $wbranch — every commit reachable from $UPSTREAM by content"
        n_safe=$(( n_safe + 1 ))
      fi
      wpath=""; wbranch=""
      ;;
  esac
done < <(git -C "$REPO" worktree list --porcelain 2>/dev/null; echo)

mismatch_note=""
if [ "$checked" -ne "$dir_total" ]; then
  mismatch_note=" ⚠️ MISMATCH: git-worktree-list saw $checked, but $dir_total directories exist on disk under $WTDIR — some worktrees may be untracked by git (manually deleted .git link) or vice versa; investigate before trusting this run as complete."
fi
echo "worktree-safety-sweep: checked $checked of $dir_total on-disk directories under $WTDIR (upstream=$UPSTREAM safe=$n_safe unmerged=$n_unmerged dirty=$n_dirty unresolved=$n_unresolved) at $(date '+%Y-%m-%d %H:%M')$mismatch_note" >&2
exit 0
