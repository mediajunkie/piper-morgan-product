#!/usr/bin/env bash
# test-mail-send.sh — isolated test harness for the push-to-ref mail bridge (#1259).
# Builds a throwaway origin + clones in a temp dir; never touches the real repo or real mail.
# Exercises: add, move (inbox→read), no-op, real parallel concurrency (rebuild-retry), and the
# cure (v3 works while the shared "main checkout" is diverged+dirty, and never touches it).
set -uo pipefail

V3="$(cd "$(dirname "$0")" && pwd)/mail-send.sh"
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

echo "── T6: #1310 self-reconcile — no residue left on the sender's worktree, later merge is clean ──"
# Realistic worktree: a feature branch with the agent's own commit ahead of main (so a plain
# reset-to-main can't apply — the reconcile must be path-scoped, not a branch reset).
clone wtE
git -C "$T/wtE" checkout -q -b claude/wtE-cycle
printf 'agent session-log work\n' > "$T/wtE/dev-note.txt"
git -C "$T/wtE" add dev-note.txt; git -C "$T/wtE" commit -qm "agent's own commit ahead of main" >/dev/null 2>&1
# Pre-seed a movable memo onto origin/main (clean ADD), then FF the feature branch to include it.
printf 'movable\n' > "$T/wtE/mailboxes/cxo/inbox/memo-move-e.md"
PIPER_REPO="$T/wtE" bash "$V3" "mail(e): T6 pre-seed movable" mailboxes/cxo/inbox/memo-move-e.md >/dev/null 2>&1
git -C "$T/wtE" fetch -q origin
git -C "$T/wtE" merge -q origin/main --no-edit >/dev/null 2>&1 || no "T6 pre-seed merge failed (harness bug)"
# The reconcile scenario: a NEW memo (untracked ADD) + a MOVE of the seeded memo (tracked delete +
# untracked ADD), all sent in one shot.
printf 'reconcile test\n' > "$T/wtE/mailboxes/cxo/inbox/memo-e.md"
mv "$T/wtE/mailboxes/cxo/inbox/memo-move-e.md" "$T/wtE/mailboxes/lead/read/memo-move-e.md"
PIPER_REPO="$T/wtE" bash "$V3" "mail(e): T6 reconcile" \
    mailboxes/cxo/inbox/memo-e.md \
    mailboxes/lead/read/memo-move-e.md \
    mailboxes/cxo/inbox/memo-move-e.md >/dev/null 2>&1
residue=$(git -C "$T/wtE" status --porcelain -- mailboxes)
[ -z "$residue" ] && ok "no mailbox residue left on worktree after send" || no "residue remains: $residue"
if git -C "$T/wtE" merge -q origin/main --no-edit >/dev/null 2>&1; then ok "later 'git merge origin/main' is collision-free"; else no "merge collided (residue not reconciled)"; fi
onmain "$T/wtE" mailboxes/cxo/inbox/memo-e.md && ok "the new memo still landed on origin/main" || no "new memo missing on origin"
gone   "$T/wtE" mailboxes/cxo/inbox/memo-move-e.md && ok "the move's inbox half removed on origin/main" || no "move inbox-half not removed"

echo "── T7: #1296 — NOTE flags an unpassed dirty mailbox path, but never touches it ──"
# Simulate the real-world gap: a MANIFEST regen written during the mail-loop but forgotten
# from the mail-send call (own-MANIFEST case, not the recipient's — recipient MANIFESTs are
# never sender-touched per convention).
clone wtF
printf 'sent normally\n' > "$T/wtF/mailboxes/cxo/inbox/memo-f.md"
mkdir -p "$T/wtF/mailboxes/cio/inbox"
printf 'regenerated manifest, forgotten from the send\n' > "$T/wtF/mailboxes/cio/inbox/MANIFEST.md"
out=$(PIPER_REPO="$T/wtF" bash "$V3" "mail(f): T7 forgot my own manifest regen" mailboxes/cxo/inbox/memo-f.md 2>&1)
git -C "$T/wtF" fetch -q origin
onmain "$T/wtF" mailboxes/cxo/inbox/memo-f.md && ok "the passed memo still landed" || no "the passed memo missing"
echo "$out" | grep -q "mailboxes/cio/inbox/MANIFEST.md" && ok "NOTE named the unpassed dirty path" || no "NOTE did not name the unpassed path"
[ -f "$T/wtF/mailboxes/cio/inbox/MANIFEST.md" ] && [ "$(cat "$T/wtF/mailboxes/cio/inbox/MANIFEST.md")" = "regenerated manifest, forgotten from the send" ] \
    && ok "unpassed path left untouched on disk (detection only, no mutation)" || no "unpassed path was mutated — should never happen"
onmain "$T/wtF" mailboxes/cio/inbox/MANIFEST.md && no "unpassed path leaked onto origin/main — should never happen" || ok "unpassed path correctly absent from origin/main"

echo "── T8: hardened warn-path — a reconcile failure names the specific path ──"
# Force the checkout-half of reconcile to fail for exactly one path by making its directory
# unwritable, while a sibling path in the same send reconciles normally.
clone wtG
mkdir -p "$T/wtG/mailboxes/lead/read"
printf 'existing\n' > "$T/wtG/mailboxes/lead/read/memo-existing-g.md"
git -C "$T/wtG" add mailboxes/lead/read/memo-existing-g.md
git -C "$T/wtG" commit -qm "seed a tracked file for T8" >/dev/null 2>&1
git -C "$T/wtG" push -q origin HEAD:main
printf 'ok path\n' > "$T/wtG/mailboxes/cxo/inbox/memo-g-ok.md"
printf 'modified, checkout will be blocked\n' > "$T/wtG/mailboxes/lead/read/memo-existing-g.md"
chmod 000 "$T/wtG/mailboxes/lead/read"
out=$(PIPER_REPO="$T/wtG" bash "$V3" "mail(g): T8 one path blocked" \
    mailboxes/cxo/inbox/memo-g-ok.md mailboxes/lead/read/memo-existing-g.md 2>&1)
chmod 755 "$T/wtG/mailboxes/lead/read"
git -C "$T/wtG" fetch -q origin
onmain "$T/wtG" mailboxes/cxo/inbox/memo-g-ok.md && ok "the send itself still succeeded" || no "the send failed — should have succeeded despite reconcile issue"
echo "$out" | grep -q "mailboxes/lead/read/memo-existing-g.md" && ok "warning named the specific blocked path" || no "warning did not name the blocked path"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
