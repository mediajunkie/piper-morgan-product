#!/usr/bin/env bash
# mail-send.sh — safe mailbox bridge-commit-and-push (CIO streamlining #2, 2026-06-15).
#
# After you've written a memo / moved items in the MAIN checkout's mailboxes/, this commits ONLY the
# mailbox changes to `main` and pushes them — handling the shared-checkout realities that otherwise
# have to be hand-rolled every time:
#   - regenerate the derived MANIFESTs
#   - stage ONLY mailboxes/ (never sweep up another agent's uncommitted work)
#   - preserve any OTHER uncommitted (tracked) work across the rebase, then restore it
#   - resolve the derived-MANIFEST rebase conflicts by regenerating
#
# It does NOT write or route memos — that's your judgment (cc copies, sent mirror, inbox→read moves).
# Do those first (in the MAIN checkout), then run this to land them safely.
#
# Usage:  scripts/mail-send.sh "mail(cio): subject summary"
set -uo pipefail

MAIN="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
MSG="${1:-}"
[ -z "$MSG" ] && { echo "usage: mail-send.sh \"mail(role): subject\"" >&2; exit 2; }
G() { git -C "$MAIN" "$@"; }

# 1. Regenerate MANIFESTs so unread/read counts reflect the current files.
[ -x "$MAIN/scripts/regenerate-mailbox-manifests.py" ] && \
    "$MAIN/scripts/regenerate-mailbox-manifests.py" --quiet >/dev/null 2>&1 || true

# 2. Stage ONLY mailbox changes.
G add mailboxes/
if G diff --cached --quiet; then echo "mail-send: nothing in mailboxes/ to send."; exit 0; fi

# 3. Commit.
G commit -q -m "$MSG" || { echo "mail-send: commit failed" >&2; exit 1; }
echo "mail-send: committed — $MSG"

# 4. Preserve any OTHER uncommitted (tracked) work across the rebase (no -u: untracked don't block).
STASHED=0
if ! G diff --quiet; then
    G stash push -m "mail-send: preserve foreign WIP" >/dev/null 2>&1 && STASHED=1
fi

# 5. Pull --rebase; resolve derived-MANIFEST conflicts by regenerating + continuing.
if ! G pull --rebase origin main -q 2>/dev/null; then
    if [ -d "$MAIN/.git/rebase-merge" ] || [ -d "$MAIN/.git/rebase-apply" ]; then
        "$MAIN/scripts/regenerate-mailbox-manifests.py" --quiet >/dev/null 2>&1 || true
        G add mailboxes/ 2>/dev/null
        GIT_EDITOR=true G rebase --continue >/dev/null 2>&1 || \
            echo "mail-send: rebase hit a NON-MANIFEST conflict — resolve by hand (git -C $MAIN status)" >&2
    fi
fi

# 6. Push.
if G push origin main 2>/dev/null; then echo "mail-send: pushed to origin/main ✓"
else echo "mail-send: push failed — check 'git -C $MAIN status'" >&2; fi

# 7. Restore the preserved foreign WIP.
if [ "$STASHED" = 1 ]; then
    G stash pop >/dev/null 2>&1 && echo "mail-send: restored foreign WIP" || \
        echo "mail-send: foreign WIP kept in stash (pop conflict) — 'git -C $MAIN stash list'"
fi
exit 0
