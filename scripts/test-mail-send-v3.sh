#!/usr/bin/env bash
# test-mail-send-v3.sh — isolated test harness for the push-to-ref mail bridge (#1259).
# Builds a throwaway origin + clones in a temp dir; never touches the real repo or real mail.
# Exercises: add, move (inbox→read), no-op, real parallel concurrency (rebuild-retry), and the
# cure (v3 works while the shared "main checkout" is diverged+dirty, and never touches it).
set -uo pipefail

V3="$(cd "$(dirname "$0")" && pwd)/mail-send-v3.sh"
[ -f "$V3" ] || { echo "missing $V3"; exit 1; }
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=t@t
T="$(mktemp -d "${TMPDIR:-/tmp}/mailtest.XXXXXX")"
trap 'rm -rf "$T"' EXIT
PASS=0; FAIL=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }
onmain(){ git -C "$1" cat-file -e "origin/main:$2" 2>/dev/null; }   # path exists on origin/main?
gone(){ ! git -C "$1" cat-file -e "origin/main:$2" 2>/dev/null; }   # path absent on origin/main?

# ---- origin + seed ----
ORIGIN="$T/origin.git"; git init --bare -q "$ORIGIN"
SEED="$T/seed"; git clone -q "$ORIGIN" "$SEED"
mkdir -p "$SEED"/mailboxes/{cio,cxo,lead}/inbox "$SEED"/mailboxes/lead/read
printf 'x\n' > "$SEED/mailboxes/lead/inbox/memo-existing.md"   # a pre-existing inbox memo (for the move test)
printf 'manifest\n' > "$SEED/mailboxes/lead/read/MANIFEST.md"
: > "$SEED/mailboxes/cio/inbox/.gitkeep"   # git doesn't track empty dirs → keep cio/cxo inboxes present in clones
: > "$SEED/mailboxes/cxo/inbox/.gitkeep"
git -C "$SEED" add -A; git -C "$SEED" commit -qm "seed"; git -C "$SEED" push -q origin HEAD:main
clone(){ git clone -q "$ORIGIN" "$T/$1"; }   # a fresh worktree-clone = one agent

echo "── T1: happy-path add (memo lands on origin/main) ──"
clone wtA
printf 'hello from A\n' > "$T/wtA/mailboxes/cxo/inbox/memo-a.md"
PIPER_REPO="$T/wtA" bash "$V3" "mail(a): T1" mailboxes/cxo/inbox/memo-a.md >/dev/null 2>&1
git -C "$T/wtA" fetch -q origin
onmain "$T/wtA" mailboxes/cxo/inbox/memo-a.md && ok "memo-a on origin/main" || no "memo-a NOT on origin/main"
[ "$(git -C "$T/wtA" show origin/main:mailboxes/cxo/inbox/memo-a.md)" = "hello from A" ] && ok "content correct" || no "content wrong"
[ "$(git -C "$T/wtA" log --oneline origin/main | wc -l | tr -d ' ')" = "2" ] && ok "linear history (seed+1)" || no "history not linear"

echo "── T2: move (inbox→read: read added + inbox removed, both halves) ──"
clone wtB
mv "$T/wtB/mailboxes/lead/inbox/memo-existing.md" "$T/wtB/mailboxes/lead/read/memo-existing.md"
PIPER_REPO="$T/wtB" bash "$V3" "mail(b): T2 triage move" \
    mailboxes/lead/read/memo-existing.md mailboxes/lead/inbox/memo-existing.md >/dev/null 2>&1
git -C "$T/wtB" fetch -q origin
onmain "$T/wtB" mailboxes/lead/read/memo-existing.md && ok "read/ copy on origin" || no "read/ copy missing"
gone   "$T/wtB" mailboxes/lead/inbox/memo-existing.md && ok "inbox/ copy removed on origin" || no "inbox/ copy NOT removed"

echo "── T3: no-op guard (paths already match origin → nothing sent, no new commit) ──"
clone wtC
before=$(git -C "$T/wtC" rev-parse origin/main)
# pass a path identical to origin (re-create memo-a with same content already on origin)
mkdir -p "$T/wtC/mailboxes/cxo/inbox"; printf 'hello from A\n' > "$T/wtC/mailboxes/cxo/inbox/memo-a.md"
out=$(PIPER_REPO="$T/wtC" bash "$V3" "mail(c): T3 noop" mailboxes/cxo/inbox/memo-a.md 2>&1)
git -C "$T/wtC" fetch -q origin
after=$(git -C "$T/wtC" rev-parse origin/main)
[ "$before" = "$after" ] && ok "no new commit on no-op" || no "no-op created a commit"
echo "$out" | grep -q "nothing to send" && ok "reported 'nothing changed'" || no "didn't report no-op"

echo "── T4: REAL concurrency — 5 parallel sends, all land, no lost updates ──"
git -C "$T/wtA" fetch -q origin; base4=$(git -C "$T/wtA" rev-parse origin/main)   # fresh tip right before the race
n=5; pids=()
for i in $(seq 1 $n); do
    clone "wtc$i"
    printf 'concurrent %s\n' "$i" > "$T/wtc$i/mailboxes/cio/inbox/memo-c$i.md"
    ( PIPER_REPO="$T/wtc$i" bash "$V3" "mail(c$i): T4 concurrent $i" mailboxes/cio/inbox/memo-c$i.md >/dev/null 2>&1 ) &
    pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
git -C "$T/wtA" fetch -q origin
landed=0
for i in $(seq 1 $n); do onmain "$T/wtA" "mailboxes/cio/inbox/memo-c$i.md" && landed=$((landed+1)); done
[ "$landed" = "$n" ] && ok "all $n concurrent memos landed (rebuild-retry held)" || no "only $landed/$n landed — LOST UPDATES"
# history must be linear (no merge commits, no losses): exactly +N over the pre-concurrency tip
depth_before=$(git -C "$T/wtA" rev-list --count "$base4")
depth_after=$(git -C "$T/wtA" rev-list --count origin/main)
[ "$((depth_after - depth_before))" = "$n" ] && ok "exactly +$n linear commits (no merges/losses)" || no "commit delta = $((depth_after-depth_before)), expected $n"

echo "── T5: THE CURE — v3 works while the 'main checkout' is diverged+dirty, and never touches it ──"
# Make SEED (the shared main checkout) diverged + dirty: a stranded local commit + uncommitted WIP + untracked junk.
printf 'stranded local commit\n' > "$SEED/mailboxes/cio/inbox/stranded.md"
git -C "$SEED" add -A; git -C "$SEED" commit -qm "stranded local (never pushed)" >/dev/null 2>&1
printf 'dirty wip\n' >> "$SEED/mailboxes/lead/read/MANIFEST.md"     # uncommitted modification
printf 'junk\n' > "$SEED/mailboxes/cio/inbox/untracked-junk.md"     # untracked residue
seed_head_before=$(git -C "$SEED" rev-parse HEAD)
seed_status_before=$(git -C "$SEED" status --porcelain | sort)
# Now an agent (wtD) sends mail via v3 — should SUCCEED despite SEED's mess, and leave SEED untouched.
clone wtD
printf 'sent despite the mess\n' > "$T/wtD/mailboxes/cxo/inbox/memo-d.md"
PIPER_REPO="$T/wtD" bash "$V3" "mail(d): T5 sent while main checkout is a mess" mailboxes/cxo/inbox/memo-d.md >/dev/null 2>&1
rc=$?
git -C "$T/wtD" fetch -q origin
[ "$rc" = 0 ] && onmain "$T/wtD" mailboxes/cxo/inbox/memo-d.md && ok "send SUCCEEDED despite diverged+dirty main checkout" || no "send failed/missing"
seed_head_after=$(git -C "$SEED" rev-parse HEAD)
seed_status_after=$(git -C "$SEED" status --porcelain | sort)
[ "$seed_head_before" = "$seed_head_after" ] && ok "main checkout's local HEAD untouched" || no "main checkout HEAD moved"
[ "$seed_status_before" = "$seed_status_after" ] && ok "main checkout's dirty WIP untouched (nothing swept/stranded)" || no "main checkout WIP changed"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
