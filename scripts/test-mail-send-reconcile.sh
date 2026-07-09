#!/usr/bin/env bash
# Self-contained sandbox test for mail-send.sh's #1310 reconcile step (#1374 regression).
# No network, no real origin: builds a bare repo + working clone under $TMPDIR, runs the
# REAL script against it (PIPER_REPO/PIPER_MAIL_REMOTE/PIPER_MAIL_BRANCH overrides — the
# env seams the script ships for exactly this), and asserts the worktree end-state that
# #1310 promises: after send + `git merge origin/main`, every passed path matches origin
# and `git status` is clean.
#
# Usage: scripts/test-mail-send-reconcile.sh [path-to-mail-send.sh]
#   (default: the mail-send.sh next to this script)
#
# Cases:
#   1. staged-rename triage move (BOTH halves passed) + MANIFEST edit — the #1374 bug:
#      pre-fix, the memo ended up on disk at NEITHER path after merge.
#   2. plain new memo (untracked) — the common send; must keep working.
#   3. staged modify-in-place — same index-vs-HEAD trap as the rename source half.
set -uo pipefail

SCRIPT="${1:-$(cd "$(dirname "$0")" && pwd)/mail-send.sh}"
[ -f "$SCRIPT" ] || { echo "no such script: $SCRIPT" >&2; exit 2; }

S="$(mktemp -d "${TMPDIR:-/tmp}/ms1374.XXXXXX")"
trap 'rm -rf "$S"' EXIT INT TERM
fail=0
say() { echo "test-mail-send: $*"; }
die() { echo "test-mail-send: FAIL — $*" >&2; fail=1; }

git -c init.defaultBranch=main init -q --bare "$S/origin.git"
git -c init.defaultBranch=main clone -q "$S/origin.git" "$S/wt"
W() { git -C "$S/wt" "$@"; }
W config user.email test@example.com
W config user.name "reconcile-test"

mkdir -p "$S/wt/mailboxes/lead/inbox" "$S/wt/mailboxes/lead/read"
echo "memo body X" > "$S/wt/mailboxes/lead/inbox/memo-X.md"
echo "manifest v1" > "$S/wt/mailboxes/lead/read/MANIFEST.md"
W add mailboxes && W commit -qm baseline && W push -q origin main

run_send() { PIPER_REPO="$S/wt" PIPER_MAIL_REMOTE=origin PIPER_MAIL_BRANCH=main \
             bash "$SCRIPT" "$@" ; }

# --- Case 1: the #1374 staged-rename triage move -------------------------------------
W mv mailboxes/lead/inbox/memo-X.md mailboxes/lead/read/memo-X.md
echo "manifest v2" > "$S/wt/mailboxes/lead/read/MANIFEST.md"
out=$(run_send "mail(test): triage move" \
    mailboxes/lead/inbox/memo-X.md \
    mailboxes/lead/read/memo-X.md \
    mailboxes/lead/read/MANIFEST.md 2>&1) || die "case1: send exited nonzero: $out"
echo "$out" | grep -q "pushed" || die "case1: no push confirmation: $out"
echo "$out" | grep -qi "warning" && die "case1: reconcile warned: $out"
W fetch -q origin main && W merge -q origin/main 2>/dev/null || die "case1: merge not clean"
[ -f "$S/wt/mailboxes/lead/read/memo-X.md" ] || die "case1: memo MISSING at read/ after merge (the #1374 symptom)"
[ -e "$S/wt/mailboxes/lead/inbox/memo-X.md" ] && die "case1: memo still at inbox/ after merge"
grep -q "manifest v2" "$S/wt/mailboxes/lead/read/MANIFEST.md" || die "case1: MANIFEST edit lost"
[ -z "$(W status --porcelain)" ] || die "case1: worktree not clean after merge: $(W status --porcelain)"
[ $fail -eq 0 ] && say "case 1 (staged-rename move) OK"

# --- Case 2: plain new memo (the common case must not regress) -----------------------
c1fail=$fail; fail=0
mkdir -p "$S/wt/mailboxes/lead/inbox"   # case 1's merge pruned the emptied inbox/ dir
echo "memo body Y" > "$S/wt/mailboxes/lead/inbox/memo-Y.md"
out=$(run_send "mail(test): new memo" mailboxes/lead/inbox/memo-Y.md 2>&1) || die "case2: send failed: $out"
echo "$out" | grep -qi "warning" && die "case2: reconcile warned: $out"
[ -e "$S/wt/mailboxes/lead/inbox/memo-Y.md" ] && die "case2: local copy not dropped pre-merge"
W fetch -q origin main && W merge -q origin/main 2>/dev/null || die "case2: merge not clean"
[ -f "$S/wt/mailboxes/lead/inbox/memo-Y.md" ] || die "case2: memo missing after merge"
[ -z "$(W status --porcelain)" ] || die "case2: worktree not clean: $(W status --porcelain)"
[ $fail -eq 0 ] && say "case 2 (plain new memo) OK"

# --- Case 3: staged modify-in-place ---------------------------------------------------
c2fail=$fail; fail=0
echo "manifest v3" > "$S/wt/mailboxes/lead/read/MANIFEST.md"
W add mailboxes/lead/read/MANIFEST.md   # STAGED, like a mid-loop `git add` habit
out=$(run_send "mail(test): staged manifest edit" mailboxes/lead/read/MANIFEST.md 2>&1) || die "case3: send failed: $out"
echo "$out" | grep -qi "warning" && die "case3: reconcile warned: $out"
W fetch -q origin main && W merge -q origin/main 2>/dev/null || die "case3: merge not clean"
grep -q "manifest v3" "$S/wt/mailboxes/lead/read/MANIFEST.md" || die "case3: staged edit lost"
[ -z "$(W status --porcelain)" ] || die "case3: worktree not clean: $(W status --porcelain)"
[ $fail -eq 0 ] && say "case 3 (staged modify-in-place) OK"

total=$((c1fail + c2fail + fail))
if [ "$total" -eq 0 ]; then say "ALL 3 CASES PASS"; exit 0; else say "FAILURES: $total case(s)"; exit 1; fi
