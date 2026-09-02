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
#
# ⚠️ Probing this script by hand? Fetch + merge origin/main before staging your next fixture.
# The #1310 self-reconcile (below) removes just-sent paths from YOUR worktree right after a
# successful push — so if your probe's next step tries to `mv`/edit that same path without first
# syncing, the operation silently no-ops (file's already gone) and your "test" passes having
# tested nothing. Lead hit this 2026-08-26 verifying the inbox/read guard: the run reported success
# while the actual push it meant to test never happened. Caught only by reading stdout, not the
# exit code — same shape as the hook-probe confounds in CLAUDE.md, met here in the wild.
#
# ⚠️ LOCAL-BRANCH LAG (Agent 360 v0.4, 5 independent respondents, 2026-08-27 — the cheapest fix in
# the whole synthesis, documented here rather than fixed in code because there is nothing to fix:
# push-to-ref is deliberately branch-agnostic). A successful send lands the commit on origin/main —
# but it does NOT touch your local branch's HEAD, upstream, or reflog. Any command that inspects
# local git state right after a send (`git log`, `git status`, `git log origin/main..HEAD`, a
# freeze-check reading local heartbeats) reads a snapshot that is now one commit stale relative to
# what you just pushed, until you `git fetch origin main` (and merge, if you need the content
# locally). This is the send-side twin of the #1310 self-reconcile note above — that one covers your
# WORKING TREE for the exact paths you passed; this one covers your BRANCH/REF state for everything
# else. Fetch+merge origin/main before inspecting local state after any push-to-ref call.
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

        # --- Lead's 2026-08-26 suggestion: warn on a half-pushed inbox->read move ------------------
        # A caller who triages inbox/X -> read/X locally but only passes read/X here silently
        # strands the inbox/ original on main — invisible to everyone else, whose mail loop polls
        # `ls inbox/`. This is a DIFFERENT failure than #1296 below: it survives a fully-clean local
        # working tree (nothing "dirty" to flag) if the inbox/ deletion was never staged at all, and
        # it's checked against the TREE JUST PUSHED, not local git status. Incident: Lead's own seat
        # ran this exact gap for weeks — "inbox zero" was true locally and false on origin/main,
        # found only by accident. Warn, don't block (a one-sided read/ push is sometimes legitimate).
        for f in "$@"; do
            case "$f" in
                mailboxes/*/read/*)
                    role="${f#mailboxes/}"; role="${role%%/*}"
                    name="${f#mailboxes/*/read/}"
                    sib="mailboxes/$role/inbox/$name"
                    # Docs 2026-08-26 false-positive, same-day report with evidence: checking only
                    # "does sib exist in $tree" can't distinguish "caller forgot to pass sib" (real
                    # strand) from "caller DID pass sib, but its content already matched origin/main
                    # so write-tree produced no delta for that path" (nothing wrong — the tree looks
                    # unchanged either way). Fix: only warn if sib was NOT itself one of "$@" — if the
                    # caller explicitly named it, they handled it, whether or not it changed the tree.
                    sib_passed=0
                    for g in "$@"; do [ "$g" = "$sib" ] && sib_passed=1 && break; done
                    if [ "$sib_passed" -eq 0 ] && G cat-file -e "$tree:$sib" 2>/dev/null; then
                        # Alarm restated as the LAST line, not just the first (Lead 2026-08-26,
                        # with reproduced evidence): a habitual `| tail -1` on this script's output
                        # is what let the original incident hide for weeks — the last line of the
                        # ORIGINAL ordering was the innocuous fix instruction, not the alarm. Any
                        # tail-truncated consumer (a human skimming, a pipe, a log preview) now sees
                        # the alarm regardless of where it stops reading.
                        echo "mail-send: WARNING — $f was pushed but $sib is STILL on $REMOTE/$BRANCH and wasn't part of this send" >&2
                        echo "mail-send:   a half-pushed move leaves the memo unread for everyone else — pass both paths" >&2
                        echo "mail-send: ⚠️  $sib STRANDED on $REMOTE/$BRANCH — resend it" >&2
                    fi
                    ;;
            esac
        done

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
            # Alarm restated as the LAST line here too (Lead 2026-08-26): this exact NOTE fired on
            # every one of Lead's incident sends for weeks and was never seen, because the original
            # last line was a parenthetical suggestion, not an alarm — a `| tail -1` habit read that
            # single innocuous line as "nothing to worry about." Root-caused with reproduced evidence,
            # not assumed. Ending on the count + a visible marker survives truncation to any tail.
            n_dirty=$(printf '%s\n' "$other_dirty" | grep -c .)
            echo "mail-send: NOTE — other mailbox path(s) have uncommitted changes this send didn't include:" >&2
            echo "$other_dirty" | sed 's/^/mail-send:   /' >&2
            echo "mail-send:   if they belong to this mail-loop (e.g. a MANIFEST regen), send them in a follow-up mail-send call" >&2
            echo "mail-send: ⚠️  ${n_dirty} mailbox path(s) left behind — see above" >&2
        fi

        # --- #1716: warn when a named to:/cc: recipient has no matching inbox/ delivery -----------
        # CXO's finding, two independent instances (Arch's own 08-30 self-audit found three of
        # their own sends under-delivered; HOST caught a 09-01 case via `git log --all`, zero
        # commits, not even transient). Neither agent was careless — that's the tell it's
        # structural: a memo's `to:`/`cc:` header is a claim about delivery this script never
        # reads. It takes explicit paths; the frontmatter is prose. Nothing connects them, so they
        # silently disagree — and the failure mode is the bad one: the sender's sent/ copy shows a
        # header naming the recipient, so BOTH ends believe it happened. Advisory only, like every
        # other check in this family — mail-send.sh must never become a reason mail doesn't go out.
        # Checks against mailboxes/DIRECTORY.md-documented slugs (a real `mailboxes/<slug>/`
        # directory existing is the cheap proxy for "this is a real recipient," avoiding false
        # positives on garbled or non-slug header text).
        #
        # Reads content via `git cat-file -p "$tree:$f"`, NOT the worktree file — the #1310
        # reconcile above already ran and deletes just-sent NEW files from the worktree (they're
        # untracked-before, so "reset to HEAD state" means removing them), so `$REPO/$f` is
        # already gone for exactly the memos this check needs to read. The pushed tree object is
        # the one thing guaranteed to still hold the content that actually shipped.
        #
        # Only scans `*/sent/*` paths — NOT inbox/ or read/ — found live in testing: an ordinary
        # inbox→read triage move (archiving mail you already received) passes those same paths
        # through mail-send.sh, and that memo's to:/cc: header describes ITS ORIGINAL send, which
        # this call has nothing to do with. Scanning inbox/read fired this warning on every single
        # triage move in the cohort's own mail loop — the exact cry-wolf failure this file's own
        # sign-off-checklist history warns about (a mandatory check people learn to skim once it's
        # wrong often enough). `sent/` is written ONLY by the sender actually composing a new send
        # (the cohort convention: "write the memo + cc copies + sent mirror" — CLAUDE.md's mailbox
        # workflow section), so its presence in "$@" is the correct signal "this call is a send,"
        # not "this call moved a file that happens to live in a mailbox." Trade-off: a send that
        # skips writing its own sent/ mirror won't be checked — accepted, since every real instance
        # of this bug (Arch 08-30, HOST 09-01) included one, and false negatives are the safe side
        # for an advisory check.
        checked_basenames=""
        for f in "$@"; do
            case "$f" in mailboxes/*/sent/*) ;; *) continue ;; esac
            G cat-file -e "$tree:$f" 2>/dev/null || continue
            bn="$(basename "$f")"
            case "$'\n'$checked_basenames$'\n'" in *$'\n'"$bn"$'\n'*) continue ;; esac
            checked_basenames="${checked_basenames}${bn}"$'\n'

            recipients="$(G cat-file -p "$tree:$f" 2>/dev/null | awk '
                NR==1 && /^---[[:space:]]*$/ { infm=1; next }
                infm && /^---[[:space:]]*$/ { exit }
                infm && /^to:[[:space:]]*/ { sub(/^to:[[:space:]]*/, ""); print }
                infm && /^cc:[[:space:]]*/ { sub(/^cc:[[:space:]]*/, ""); print }
            ')"
            [ -z "$recipients" ] && continue

            # `recipients` holds one line per matched header (to: and cc: print separately) —
            # each line is itself comma-separated. `read -ra` only ever consumes ONE line from
            # a here-string, so a naive single read here silently drops every line but the
            # first (caught in testing: a to:+cc: capture dropped the whole cc: line).
            while IFS= read -r line; do
                [ -z "$line" ] && continue
                IFS=',' read -ra tokens <<<"$line"
                for tok in "${tokens[@]}"; do
                    slug="$(printf '%s' "$tok" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"//' -e 's/"$//')"
                    [ -z "$slug" ] && continue
                    [ -d "$REPO/mailboxes/$slug" ] || continue
                    expected="mailboxes/$slug/inbox/$bn"
                    found=0
                    for g in "$@"; do [ "$g" = "$expected" ] && found=1 && break; done
                    if [ "$found" -eq 0 ]; then
                        echo "mail-send: WARNING — '$bn' names '$slug' in to:/cc: but $expected wasn't part of this send" >&2
                        echo "mail-send:   the header and the delivery can silently disagree (#1716) — pass that path too if the recipient should get it" >&2
                    fi
                done
            done <<<"$recipients"
        done

        # --- CXO/HOST's 2026-08-28 relocation: check refresh-trigger promises AT the trigger ------
        # HOST's diff-checker (#1296-adjacent, shipped 08-26) caught "edited content, forgot to bump
        # last_updated" — but it lapsed a 4th time anyway, because the real failure is upstream of
        # any edit: nothing connects "I filed a workstream review" to "my portfolio doc promises to
        # refresh on exactly that event." CXO's relocation: hook the check to the moment the trigger
        # ARTIFACT is created, which is exactly a mail-send.sh call. PURE ADVISORY — this must never
        # slow or fail a send that matches nothing (the overwhelming majority); silent on no-match,
        # by design of check-refresh-promises.py's own --trigger-sent mode.
        CHECKREF="$REPO/scripts/check-refresh-promises.py"
        if [ -f "$CHECKREF" ]; then
            for f in "$@"; do
                python3 "$CHECKREF" --trigger-sent "$f" 2>/dev/null
            done
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
