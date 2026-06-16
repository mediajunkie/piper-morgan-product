#!/usr/bin/env bash
# mail-send.sh v2 — safe mailbox bridge-commit-push (CIO streamlining #2; v2 2026-06-16 fixes Exec's 2 hazards).
#
# Commits the EXACT memo files you pass to `main` and pushes them. You still do the routing by hand first
# (write the memo, cc copies, sent mirror, inbox→read moves), then pass those paths to this script.
#
# v2 changes (Exec 2026-06-15 memo — both hazards trace to the shared working tree):
#   - Stage by EXPLICIT pathspec (the files you pass) — NOT `git add mailboxes/`. On the shared tree that
#     directory-add swept a *concurrent* session's in-flight memos into your commit (hazard 1).
#   - NO auto-stash of foreign WIP. On a non-fast-forward this FAILS LOUD instead — auto-stashing another
#     session's tracked edits can strand them if this script dies before the pop (hazard 2).
#   - No MANIFEST regen here: the RECIPIENT is the sole MANIFEST writer (skill v1.7 derive model) and
#     regenerates during their own Mail Loop / session-start. The sender just commits the memo file(s).
# (The full race-free cure is push-to-ref from each session's own worktree index — the structural
#  "mailbox-bridge transparency" item; a wrapper on the shared checkout can only narrow these, not erase them.)
#
# Usage:  scripts/mail-send.sh "mail(cio): subject" <path1> [path2 ...]   (paths relative to repo root)
set -uo pipefail
MAIN="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
MSG="${1:-}"
shift || true
if [ -z "$MSG" ] || [ "$#" -eq 0 ]; then
    echo 'usage: mail-send.sh "mail(role): subject" <path> [path...]   (explicit mailbox paths)' >&2; exit 2
fi
G() { git -C "$MAIN" "$@"; }

# Refuse non-mailbox paths — this is the mailbox bridge, not a general committer (keeps it scoped + safe).
for f in "$@"; do
    case "$f" in mailboxes/*) ;; *) echo "mail-send: refusing non-mailbox path: $f" >&2; exit 2 ;; esac
done

G add -- "$@"
if G diff --cached --quiet; then echo "mail-send: nothing staged (paths unchanged?)"; exit 0; fi
G commit -q -m "$MSG" || { echo "mail-send: commit failed" >&2; exit 1; }
echo "mail-send: committed — $MSG"

G fetch origin -q
if G push origin main 2>/dev/null; then echo "mail-send: pushed to origin/main ✓"; exit 0; fi

# Non-fast-forward: integrate ONLY if the working tree is clean of OTHER work (never auto-stash → never strand).
if G diff --quiet && G diff --cached --quiet; then
    if G rebase origin/main 2>/dev/null && G push origin main 2>/dev/null; then
        echo "mail-send: rebased onto origin + pushed ✓"; exit 0
    fi
fi
echo "mail-send: NON-FF and other uncommitted work is present — NOT auto-stashing (would risk stranding a" >&2
echo "          concurrent session). Your commit is safe locally; resolve by hand:" >&2
echo "          git -C $MAIN status && git -C $MAIN pull --rebase origin main && git -C $MAIN push origin main" >&2
exit 1
