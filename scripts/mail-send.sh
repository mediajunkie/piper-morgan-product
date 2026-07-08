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
TMPIDX=""
trap 'rm -f "$TMPIDX"' EXIT INT TERM   # temp-index never leaks — even on SIGINT/SIGTERM (LD review nit 1)
while :; do
    attempt=$((attempt + 1))
    G fetch "$REMOTE" "$BRANCH" -q || { echo "mail-send: fetch $REMOTE/$BRANCH failed" >&2; exit 1; }
    base=$(G rev-parse "$REMOTE/$BRANCH" 2>/dev/null) || { echo "mail-send: no $REMOTE/$BRANCH" >&2; exit 1; }

    TMPIDX="$(mktemp "${TMPDIR:-/tmp}/mail-idx.XXXXXX")"
    GIT_INDEX_FILE="$TMPIDX" G read-tree "$base" || { echo "mail-send: read-tree failed" >&2; exit 1; }

    for f in "$@"; do
        if [ -f "$REPO/$f" ]; then
            blob=$(G hash-object -w -- "$f") || { echo "mail-send: hash-object failed: $f" >&2; exit 1; }
            GIT_INDEX_FILE="$TMPIDX" G update-index --add --cacheinfo "100644,$blob,$f" \
                || { echo "mail-send: update-index --add failed: $f" >&2; exit 1; }
        else
            GIT_INDEX_FILE="$TMPIDX" G update-index --force-remove "$f" \
                || { echo "mail-send: update-index --force-remove failed: $f" >&2; exit 1; }
        fi
    done

    tree=$(GIT_INDEX_FILE="$TMPIDX" G write-tree) || { echo "mail-send: write-tree failed" >&2; exit 1; }
    rm -f "$TMPIDX"   # prompt per-iteration cleanup; the EXIT/INT/TERM trap is the signal/error backstop

    # No-op guard: identical tree → the paths already match origin; nothing to send.
    if [ "$tree" = "$(G rev-parse "$base^{tree}")" ]; then
        echo "mail-send: nothing to send — these paths already match $REMOTE/$BRANCH (already delivered, or a duplicate a concurrent send already landed)"; exit 0
    fi

    # commit-tree uses the agent's configured git identity (user.name/email) — all our agents have it set.
    commit=$(G commit-tree "$tree" -p "$base" -m "$MSG") || { echo "mail-send: commit-tree failed" >&2; exit 1; }
    if G push "$REMOTE" "$commit:refs/heads/$BRANCH" 2>/dev/null; then
        echo "mail-send v3: pushed ${commit:0:9} → $REMOTE/$BRANCH ✓ (attempt $attempt)"
        # --- #1310: self-reconcile the worktree residue ------------------------------------------
        # The just-sent paths now live on origin/main but still sit uncommitted in THIS worktree
        # (new files = untracked; moved/modified = working-tree changes). A later `git merge` then
        # collides ("untracked files would be overwritten" / "local changes would be overwritten").
        # Fix: return ONLY these exact paths to their HEAD state so the next merge is collision-free.
        # SURGICAL by construction — operates strictly on "$@" (paths the caller passed for THIS send,
        # written seconds ago), never a broad `checkout -- .` / `reset --hard` (HARD RULE). Best-effort:
        # the push already succeeded, so reconcile errors only warn — they never fail the send.
        reconcile_failed=""
        for f in "$@"; do
            # #1374: reset this path's INDEX entry to HEAD before touching the worktree.
            # A same-invocation staged rename (`git mv inbox/X read/X` before calling this
            # script) broke BOTH branches below without this: the source half's ref-less
            # `checkout -- f` restored from the INDEX (which the mv had already emptied →
            # silent no-op), and the destination half got rm'd from disk while the index
            # still claimed it — so the eventual merge saw index == incoming tree, never
            # rewrote the file, and the memo ended up at NEITHER path (3-for-3 on every
            # triage-move send). Still surgical: strictly per-path, never a broad reset.
            G reset -q HEAD -- "$f" 2>/dev/null
            if G cat-file -e "HEAD:$f" 2>/dev/null; then
                # tracked in HEAD → restore HEAD's version FROM HEAD explicitly (undo this
                # send's modify/delete); the eventual merge re-applies the change cleanly.
                err=$(G checkout HEAD -- "$f" 2>&1) || reconcile_failed="${reconcile_failed}${f}: ${err}"$'\n'
            else
                # not in HEAD (purely-new file, or a rename's destination) → drop the local
                # copy; with its index entry cleared above, the eventual merge re-creates it
                # as a tracked file cleanly.
                err=$(rm -f "$REPO/$f" 2>&1) || reconcile_failed="${reconcile_failed}${f}: ${err}"$'\n'
            fi
        done
        if [ -z "$reconcile_failed" ]; then
            echo "mail-send: worktree residue reconciled — a later 'git merge $REMOTE/$BRANCH' is now clean (#1310)"
        else
            echo "mail-send: warning — reconcile failed for one or more paths (mail was sent OK); fix these by hand before your next merge:" >&2
            echo "$reconcile_failed" | sed 's/^/mail-send:   /' >&2
        fi

        # --- #1296: flag OTHER dirty mailbox paths this send didn't touch --------------------------
        # Residue also comes from paths written during the same mail-loop but never passed to
        # mail-send (e.g. your own MANIFEST.md regen alongside a triage move). Reconcile above is
        # deliberately scoped to "$@" only (HARD RULE — no broad checkout/reset), so it can't know
        # about those. DETECTION ONLY: never touches a path outside "$@"; just stops the leftover
        # from going silent.
        other_dirty=""
        while IFS= read -r line; do
            [ -z "$line" ] && continue
            p="${line:3}"
            skip=0
            for f in "$@"; do [ "$f" = "$p" ] && skip=1 && break; done
            [ "$skip" -eq 0 ] && other_dirty="${other_dirty}${p}"$'\n'
        done <<< "$(G status --porcelain -- mailboxes 2>/dev/null)"
        if [ -n "$other_dirty" ]; then
            echo "mail-send: NOTE — other mailbox path(s) have uncommitted changes this send didn't include:" >&2
            echo "$other_dirty" | sed 's/^/mail-send:   /' >&2
            echo "mail-send:   if they belong to this mail-loop (e.g. a MANIFEST regen), send them in a follow-up mail-send call" >&2
        fi
        # ----------------------------------------------------------------------------------------
        exit 0
    fi

    if [ "$attempt" -ge "$MAX" ]; then
        echo "mail-send: push rejected after $MAX attempts (persistent contention on $REMOTE/$BRANCH) — retry shortly" >&2
        exit 1
    fi
    echo "mail-send: non-fast-forward (another agent pushed first) — rebuilding on the new tip (attempt $attempt)" >&2
done
