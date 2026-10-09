#!/usr/bin/env bash
# guard-pm-checkout.sh — PreToolUse (Bash): refuse destructive git aimed at PM's MAIN checkout.
#
# R6 step 1 (PM approved 2026-10-04, "guard first"). CLAUDE.md's HARD RULE (never discard working-tree
# state in /Users/xian/Development/piper-morgan-product) was prose-only, and the project allow-list
# then permitted `Bash(git:*)` / `Bash(git stash:*)` (both removed 2026-10-08, R6 step 1's second half:
# replaced by explicit routine subcommands; anything else goes to the auto-mode classifier). PM lost voice-pass edits twice on 2026-06-21 to
# `git checkout -- .` run there. This turns the rule into a mechanism.
#
# Refuses, when the git command's target directory is PM's main checkout (or a subdirectory):
#   checkout -- <path> | checkout <ref> -- <path> | checkout .   (overwrite working tree)
#   restore <path> without --staged                             (overwrite working tree)
#   reset --hard | clean -f/-fd/-x                              (discard state)
#   stash / stash push / stash -u / stash pop / stash drop / stash clear (anything but list/show)
# Target = `git -C <dir>` if given, else the last `cd <dir>` earlier in the command, else the tool cwd.
# Worktrees under ~/Development/piper-morgan-worktrees/ are NOT protected by this (they are yours).
#
# Cost:    one bash `case` per Bash call; Python only when the command mentions git (~30 ms).
# Benefit: none yet: measuring (prevention guard; argued per sunset-or-renew: no catches is the goal).
# Review:  2026-12-01.   Owner: CIO.
# Exit 2 + reason on STDERR (only stderr reaches the agent; see autoclose-guard.sh #1934).
set -u
in="$(cat)"
case "$in" in *git*) ;; *) exit 0 ;; esac
PM_CHECKOUT="${PIPER_PM_CHECKOUT:-/Users/xian/Development/piper-morgan-product}"
# Fail OPEN if the logic file is missing or Python itself errors (exit codes other than 0/2 pass):
# a broken guard must never wedge every seat's git.
here="$(cd "$(dirname "$0")" && pwd)"
[ -f "$here/guard_pm_checkout.py" ] || exit 0
printf '%s' "$in" | PM_CHECKOUT="$PM_CHECKOUT" python3 "$here/guard_pm_checkout.py"
rc=$?
[ "$rc" = 2 ] && exit 2
exit 0
