#!/usr/bin/env bash
# mail-send.sh v3 — push-to-ref mailbox bridge (#1259). Builds the mail commit as a git OBJECT on top
# of origin/main and pushes it straight to main — never touching a shared working tree or the local
# `main` ref. Eliminates the shared-checkout contention class BY CONSTRUCTION: sweep, strand,
# divergence, and untracked-residue all become impossible because no mail op mutates a shared tree.
#
# Same caller interface as v2:  mail-send.sh "mail(role): subject" <path> [path...]
# You still do the routing by hand first (write the memo, cc copies, sent mirror, inbox→read moves) —
# but you do it in YOUR OWN worktree (wherever you are), then pass those paths. No `cd` to the main
# checkout; the main checkout is never touched.
#
# How it works (design doc option B — docs/internal/operations/mailbox-bridge-transparency-design-2026-06-16.md):
#   base = origin/main
#   throwaway index seeded from base  (GIT_INDEX_FILE → a temp file, NOT the real index)
#   for each pathspec:
#     present in worktree → hash-object -w (write blob to the shared object store) + update-index --add
#     absent  in worktree → update-index --force-remove   (the delete half of a move)
#   tree = write-tree ; commit = commit-tree tree -p base ; push commit:main
#   non-FF (someone pushed first) → re-fetch, rebuild on the NEW tip, retry. Mailbox adds are unique
#   files, so the replay is clean (never conflicts). MANIFESTs are recipient-owned (one writer per
#   mailbox), so the blind replay is last-writer-wins only across a file no two agents share.
#
# Hook interaction: commit-tree is NOT `git commit`, so check-branch.sh (PreToolUse on git commit)
# doesn't fire — and that is correct: push-to-ref already achieves the hook's intent (mail lands on
# main immediately). The hook stays as the backstop for any interactive mail commits. Invariant intact.
#
# Env overrides (mainly for testing): PIPER_REPO (repo dir; default = current worktree toplevel),
#   PIPER_MAIL_REMOTE (default origin), PIPER_MAIL_BRANCH (default main).
set -uo pipefail

REPO="${PIPER_REPO:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$REPO" ] || { echo "mail-send: not in a git repo (set PIPER_REPO)" >&2; exit 2; }
MSG="${1:-}"; shift || true
if [ -z "$MSG" ] || [ "$#" -eq 0 ]; then
    echo 'usage: mail-send.sh "mail(role): subject" <path> [path...]   (explicit mailbox paths)' >&2; exit 2
fi
G() { git -C "$REPO" "$@"; }

# Scope guard: mailbox paths only — this is the mailbox bridge, not a general committer.
for f in "$@"; do
    case "$f" in mailboxes/*) ;; *) echo "mail-send: refusing non-mailbox path: $f" >&2; exit 2 ;; esac
done

REMOTE="${PIPER_MAIL_REMOTE:-origin}"
BRANCH="${PIPER_MAIL_BRANCH:-main}"
MAX=6
attempt=0
while :; do
    attempt=$((attempt + 1))
    G fetch "$REMOTE" "$BRANCH" -q || { echo "mail-send: fetch $REMOTE/$BRANCH failed" >&2; exit 1; }
    base=$(G rev-parse "$REMOTE/$BRANCH" 2>/dev/null) || { echo "mail-send: no $REMOTE/$BRANCH" >&2; exit 1; }

    TMPIDX="$(mktemp "${TMPDIR:-/tmp}/mail-idx.XXXXXX")"
    cleanup() { rm -f "$TMPIDX"; }
    GIT_INDEX_FILE="$TMPIDX" G read-tree "$base" || { cleanup; echo "mail-send: read-tree failed" >&2; exit 1; }

    for f in "$@"; do
        if [ -f "$REPO/$f" ]; then
            blob=$(G hash-object -w -- "$f") || { cleanup; echo "mail-send: hash-object failed: $f" >&2; exit 1; }
            GIT_INDEX_FILE="$TMPIDX" G update-index --add --cacheinfo "100644,$blob,$f" \
                || { cleanup; echo "mail-send: update-index --add failed: $f" >&2; exit 1; }
        else
            GIT_INDEX_FILE="$TMPIDX" G update-index --force-remove "$f" \
                || { cleanup; echo "mail-send: update-index --force-remove failed: $f" >&2; exit 1; }
        fi
    done

    tree=$(GIT_INDEX_FILE="$TMPIDX" G write-tree) || { cleanup; echo "mail-send: write-tree failed" >&2; exit 1; }
    cleanup

    # No-op guard: identical tree → the paths already match origin; nothing to send.
    if [ "$tree" = "$(G rev-parse "$base^{tree}")" ]; then
        echo "mail-send: nothing changed (paths already match $REMOTE/$BRANCH) — nothing sent"; exit 0
    fi

    commit=$(G commit-tree "$tree" -p "$base" -m "$MSG") || { echo "mail-send: commit-tree failed" >&2; exit 1; }
    if G push "$REMOTE" "$commit:refs/heads/$BRANCH" 2>/dev/null; then
        echo "mail-send v3: pushed ${commit:0:9} → $REMOTE/$BRANCH ✓ (attempt $attempt)"
        exit 0
    fi

    if [ "$attempt" -ge "$MAX" ]; then
        echo "mail-send: push rejected after $MAX attempts (persistent contention on $REMOTE/$BRANCH) — retry shortly" >&2
        exit 1
    fi
    echo "mail-send: non-fast-forward (another agent pushed first) — rebuilding on the new tip (attempt $attempt)" >&2
done
