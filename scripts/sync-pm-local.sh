#!/usr/bin/env bash
# sync-pm-local.sh — keep PM's local main checkout current after a push (HOST proposal, 2026-07-03).
#
# Problem: agents push to origin/main from their own ephemeral worktrees all session long, but PM's
# local main checkout (a separate working directory) doesn't auto-update. PM has to remember to `git
# pull` to see current inbox/carry-forward/session-log state — an easy-to-forget manual step.
#
# Mechanism choice (CIO, 2026-07-04, brokering HOST's ask): a named script, not a raw `git pull` copy-
# pasted into every agent's push routine. One place to audit/adjust the safety behavior.
#
# Safety, stricter than HOST's original raw-`git pull` proposal:
#   --ff-only : refuses to create a merge commit and refuses outright if a real merge would be needed
#               (e.g. PM has local commits not on origin, which discipline says shouldn't happen, but
#               this makes it a loud failure instead of a merge attempt). This is the HARD RULE's
#               "never destructive, never surprising" bar applied to an automated touch of PM's tree.
#   Uncommitted-changes guard: if PM's checkout has uncommitted changes, --ff-only pull still updates
#   tracked files that aren't dirty and leaves dirty files alone (git's normal merge safety) — but we
#   skip entirely instead, because PM's checkout is documented (CLAUDE.md HARD RULE) to carry
#   real-time unsaved prose edits, and a file changing under an open editor buffer — even safely at
#   the git level — can silently revert on PM's next editor-save. Skipping is the conservative choice;
#   it costs one missed sync, not a confusing revert.
#
# Cadence (CIO's answer to HOST's Q2): call this once per fire / at natural idle points, NOT after
# every single commit. Multiple pushes within one fire don't each need their own pull; one sync at
# the point an agent returns to idle keeps PM within a fire's latency, not a commit's, while avoiding
# concurrent agents racing on PM's checkout's .git/index.lock during a busy multi-agent stretch.
#
# Usage: scripts/sync-pm-local.sh   (no args; silent no-op on any non-fatal condition, per the
#   "never block agent work" principle other hooks in this repo already follow)
#
# Env override: PM_CHECKOUT (default: the canonical main checkout path)

set -uo pipefail

PM_CHECKOUT="${PM_CHECKOUT:-/Users/xian/Development/piper-morgan/piper-morgan-product}"

[ -d "$PM_CHECKOUT/.git" ] || { echo "sync-pm-local: $PM_CHECKOUT is not a git checkout — skipping" >&2; exit 0; }

# Uncommitted changes → skip. PM's checkout carries real-time unsaved edits (HARD RULE); don't risk
# an editor-buffer/disk-state surprise even though --ff-only itself would be safe.
if [ -n "$(git -C "$PM_CHECKOUT" status --porcelain 2>/dev/null)" ]; then
    echo "sync-pm-local: PM checkout has uncommitted changes — skipping (PM's WIP takes priority)" >&2
    exit 0
fi

# Only act if PM's checkout is actually on main — never touch it if PM has switched branches locally.
CUR_BRANCH=$(git -C "$PM_CHECKOUT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [ "$CUR_BRANCH" != "main" ]; then
    echo "sync-pm-local: PM checkout is on '$CUR_BRANCH', not main — skipping" >&2
    exit 0
fi

if git -C "$PM_CHECKOUT" pull origin main --ff-only -q 2>/dev/null; then
    echo "sync-pm-local: PM checkout fast-forwarded to $(git -C "$PM_CHECKOUT" rev-parse --short HEAD)"
else
    # --ff-only failure is loud-but-safe: no merge attempted, nothing changed. Common cause: PM's
    # checkout has local commits not on origin (shouldn't happen per discipline, but not our call to
    # fix automatically) or a network hiccup. Either way, surface it and move on — never retry-loop.
    echo "sync-pm-local: fast-forward failed (PM checkout may have local commits, or network issue) — left untouched" >&2
fi
