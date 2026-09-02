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
echo "$out" | tail -1 | grep -q "left behind" && ok "alarm survives truncation to the last line (Lead 2026-08-26 fix)" || no "last line is not the alarm — truncation-safety regressed"
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

echo "── T9: Lead's 08-26 guard — half-pushed inbox->read move warns loudly ──"
# The exact incident: a read/ copy is pushed while its inbox/ sibling is left on origin/main,
# not part of this send. Seed a real inbox/ original, then push only its read/ sibling.
clone wtH
mkdir -p "$T/wtH/mailboxes/lead/inbox"
printf 'original, staying on main\n' > "$T/wtH/mailboxes/lead/inbox/memo-h.md"
git -C "$T/wtH" add mailboxes/lead/inbox/memo-h.md
git -C "$T/wtH" commit -qm "seed the stranded inbox original for T9" >/dev/null 2>&1
git -C "$T/wtH" push -q origin HEAD:main
mkdir -p "$T/wtH/mailboxes/lead/read"
printf 'original, staying on main\n' > "$T/wtH/mailboxes/lead/read/memo-h.md"   # read/ half only — inbox/ half NOT passed
out=$(PIPER_REPO="$T/wtH" bash "$V3" "mail(h): T9 half-pushed move" mailboxes/lead/read/memo-h.md 2>&1)
git -C "$T/wtH" fetch -q origin
onmain "$T/wtH" mailboxes/lead/read/memo-h.md && ok "the read/ half still landed" || no "the read/ half missing"
onmain "$T/wtH" mailboxes/lead/inbox/memo-h.md && ok "inbox/ half correctly still stranded on origin/main (reproduces the incident)" || no "inbox/ half unexpectedly gone"
echo "$out" | grep -q "mailboxes/lead/inbox/memo-h.md is STILL on" && ok "WARNING named the stranded inbox/ sibling" || no "warning did not fire for the stranded sibling"
echo "$out" | grep -q "pass both paths" && ok "warning told the caller what to do" || no "warning missing the fix instruction"
echo "$out" | tail -1 | grep -q "STRANDED" && ok "alarm survives truncation to the last line (Lead 2026-08-26 fix)" || no "last line is not the alarm — truncation-safety regressed"

echo "── T10: Lead's 08-26 guard — passing both halves together produces no warning ──"
clone wtI
mkdir -p "$T/wtI/mailboxes/lead/inbox"
printf 'original\n' > "$T/wtI/mailboxes/lead/inbox/memo-i.md"
git -C "$T/wtI" add mailboxes/lead/inbox/memo-i.md
git -C "$T/wtI" commit -qm "seed the inbox original for T10" >/dev/null 2>&1
git -C "$T/wtI" push -q origin HEAD:main
mkdir -p "$T/wtI/mailboxes/lead/read"
printf 'original\n' > "$T/wtI/mailboxes/lead/read/memo-i.md"
rm -f "$T/wtI/mailboxes/lead/inbox/memo-i.md"   # both halves of the move, both passed below
out=$(PIPER_REPO="$T/wtI" bash "$V3" "mail(i): T10 complete move" \
    mailboxes/lead/read/memo-i.md mailboxes/lead/inbox/memo-i.md 2>&1)
git -C "$T/wtI" fetch -q origin
onmain "$T/wtI" mailboxes/lead/read/memo-i.md && ok "the read/ half landed" || no "the read/ half missing"
gone   "$T/wtI" mailboxes/lead/inbox/memo-i.md && ok "the inbox/ half correctly removed" || no "the inbox/ half not removed"
echo "$out" | grep -q "is STILL on" && no "false-positive warning fired on a complete move" || ok "no warning on a correctly-complete move"

echo "── T11: Docs's 08-26 false-positive — inbox/ path passed but content unchanged (no tree delta) ──"
# Docs's exact shape: both read/ and inbox/ MANIFEST paths are passed, but inbox/MANIFEST.md's
# local content already matches what's on origin/main, so write-tree produces no delta for that
# path — the tree looks identical to "never touched" even though the caller explicitly named it.
clone wtJ
mkdir -p "$T/wtJ/mailboxes/docs/inbox" "$T/wtJ/mailboxes/docs/read"
printf 'manifest content\n' > "$T/wtJ/mailboxes/docs/inbox/MANIFEST.md"
git -C "$T/wtJ" add mailboxes/docs/inbox/MANIFEST.md
git -C "$T/wtJ" commit -qm "seed docs MANIFEST for T11" >/dev/null 2>&1
git -C "$T/wtJ" push -q origin HEAD:main
printf 'triage source memo\n' > "$T/wtJ/mailboxes/docs/inbox/memo-j.md"
mv "$T/wtJ/mailboxes/docs/inbox/memo-j.md" "$T/wtJ/mailboxes/docs/read/memo-j.md"
printf 'manifest content\n' > "$T/wtJ/mailboxes/docs/inbox/MANIFEST.md"   # re-write, SAME content as origin
out=$(PIPER_REPO="$T/wtJ" bash "$V3" "mail(j): T11 manifest already matches origin" \
    mailboxes/docs/read/memo-j.md mailboxes/docs/inbox/MANIFEST.md 2>&1)
git -C "$T/wtJ" fetch -q origin
onmain "$T/wtJ" mailboxes/docs/read/memo-j.md && ok "the read/ memo landed" || no "the read/ memo missing"
echo "$out" | grep -q "STRANDED" && no "false positive: warned even though inbox/MANIFEST.md was explicitly passed" || ok "no false-positive warning when the sibling path was explicitly passed, even with no tree delta"

echo "── T12: #1716 — cc: recipient named in frontmatter but not delivered triggers a warning ──"
# Reproduces the HOST/Arch shape: a memo's YAML frontmatter names `cio, cxo` in cc:, but the
# caller only passes the `to:` recipient's inbox path (plus the sender's own sent/ mirror,
# per cohort convention) — the cc'd recipients' inbox copies never made it into the argument
# list, so their inbox never gets the file. The check only scans sent/ paths (see mail-send.sh's
# #1716 comment) — an inbox/read-only call is a triage move, not a send, and must NOT trigger it.
clone wtK
mkdir -p "$T/wtK/mailboxes/lead/inbox" "$T/wtK/mailboxes/exec/sent"
cat > "$T/wtK/mailboxes/lead/inbox/memo-k.md" <<'EOF'
---
from: exec
to: lead
cc: cio, cxo
subject: "test"
date: 2026-09-01
---

body
EOF
cp "$T/wtK/mailboxes/lead/inbox/memo-k.md" "$T/wtK/mailboxes/exec/sent/memo-k.md"
out=$(PIPER_REPO="$T/wtK" bash "$V3" "mail(k): T12 cc gap" \
    mailboxes/lead/inbox/memo-k.md mailboxes/exec/sent/memo-k.md 2>&1)
git -C "$T/wtK" fetch -q origin
onmain "$T/wtK" mailboxes/lead/inbox/memo-k.md && ok "the passed memo still landed" || no "the passed memo missing"
echo "$out" | grep -q "names 'cio'.*wasn't part of this send" && ok "WARNING fired for missing cio delivery" || no "no warning for missing cio delivery"
echo "$out" | grep -q "names 'cxo'.*wasn't part of this send" && ok "WARNING fired for missing cxo delivery" || no "no warning for missing cxo delivery"

echo "── T13: #1716 — no false-positive when every named recipient's inbox copy is passed ──"
clone wtL
mkdir -p "$T/wtL/mailboxes/lead/inbox" "$T/wtL/mailboxes/cio/inbox" "$T/wtL/mailboxes/exec/sent"
cat > "$T/wtL/mailboxes/lead/inbox/memo-l.md" <<'EOF'
---
from: exec
to: lead
cc: cio
subject: "test"
date: 2026-09-01
---

body
EOF
cp "$T/wtL/mailboxes/lead/inbox/memo-l.md" "$T/wtL/mailboxes/cio/inbox/memo-l.md"
cp "$T/wtL/mailboxes/lead/inbox/memo-l.md" "$T/wtL/mailboxes/exec/sent/memo-l.md"
out=$(PIPER_REPO="$T/wtL" bash "$V3" "mail(l): T13 fully delivered" \
    mailboxes/lead/inbox/memo-l.md mailboxes/cio/inbox/memo-l.md mailboxes/exec/sent/memo-l.md 2>&1)
git -C "$T/wtL" fetch -q origin
onmain "$T/wtL" mailboxes/lead/inbox/memo-l.md && onmain "$T/wtL" mailboxes/cio/inbox/memo-l.md \
    && ok "both copies landed" || no "a copy is missing"
echo "$out" | grep -q "wasn't part of this send" && no "false-positive warning fired even though cio's inbox copy was passed" || ok "no false-positive when all named recipients are covered"

echo "── T14: #1716 — a plain inbox→read triage move never triggers the check (no sent/ path) ──"
# The false-positive this fix specifically guards against: archiving mail you already received
# (no sent/ mirror in this call, because you're not the sender) must produce zero #1716 warnings,
# even though the memo's own frontmatter still names cc's that obviously aren't part of this call.
clone wtM
mkdir -p "$T/wtM/mailboxes/cio/inbox" "$T/wtM/mailboxes/cio/read"
cat > "$T/wtM/mailboxes/cio/inbox/memo-m.md" <<'EOF'
---
from: exec
to: cio
cc: host, cxo
subject: "test"
date: 2026-09-01
---

body
EOF
git -C "$T/wtM" add mailboxes/cio/inbox/memo-m.md
git -C "$T/wtM" commit -qm "seed the inbox original for T14" >/dev/null 2>&1
git -C "$T/wtM" push -q origin HEAD:main
mv "$T/wtM/mailboxes/cio/inbox/memo-m.md" "$T/wtM/mailboxes/cio/read/memo-m.md"
out=$(PIPER_REPO="$T/wtM" bash "$V3" "mail(m): T14 pure triage move, not a send" \
    mailboxes/cio/read/memo-m.md mailboxes/cio/inbox/memo-m.md 2>&1)
git -C "$T/wtM" fetch -q origin
onmain "$T/wtM" mailboxes/cio/read/memo-m.md && ok "the read/ copy landed" || no "the read/ copy missing"
echo "$out" | grep -q "#1716" && no "false-positive: #1716 warning fired on a pure triage move" || ok "no #1716 warning on a pure inbox->read triage move"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
