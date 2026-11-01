#!/usr/bin/env bash
# Synthetic end-to-end test of the old-history guard in scripts/git-hooks/pre-push.
# Usage: scripts/git-hooks/test-old-history-guard.sh <new empty scratch dir> scripts/git-hooks/pre-push
# Builds a bare remote, an old history, a rewrite and a seat clone, then pushes 9 ways. Touches nothing else.
# Concept: docs/internal/operations/history-rewrite-runbook.md (added 2026-11-01, sunset-or-renew inventory; CIO)
set -u
S="$1"; HOOK="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
mkdir -p "$S" && cd "$S" || exit 2
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
pass=0; fail=0
ok()  { echo "PASS $1"; pass=$((pass+1)); }
bad() { echo "FAIL $1"; fail=$((fail+1)); }

git init -q --bare remote.git
git init -q -b main old
cd old
git remote add origin ../remote.git
echo a > README; git add README; git commit -qm A; A=$(git rev-parse HEAD)
echo secret-name > people.txt; git add people.txt; git commit -qm B; B=$(git rev-parse HEAD)
echo c > notes.txt; git add notes.txt; git commit -qm C; C=$(git rev-parse HEAD)
git push -q origin main
git checkout -q -b fork-before-B "$A"; echo f > f.txt; git add f.txt; git commit -qm F
git push -q origin fork-before-B
cd ..

git clone -q remote.git seat
cd seat
git checkout -q -b claude/x-cycle origin/main
cp "$HOOK" .git/hooks/pre-push; chmod +x .git/hooks/pre-push
common=$(git rev-parse --git-common-dir)
cd ..

# The rewrite: B' and C' on top of A (people.txt redacted), force-pushed as main.
cd old
git checkout -q main
echo '[redacted]' > people.txt; git add people.txt
B2=$(git commit-tree "$(git write-tree)" -p "$A" -m "B'")
git read-tree "$B2"; echo c > notes.txt; git add notes.txt
C2=$(git commit-tree "$(git write-tree)" -p "$B2" -m "C'")
git push -q -f origin "${C2}:refs/heads/main"
cd ..
echo "old: A=${A:0:9} B=${B:0:9} C=${C:0:9}  new: B'=${B2:0:9} C'=${C2:0:9}"

cd seat
# T1: dormant without the sentinel file.
echo t1 > t1.txt; git add t1.txt; git commit -qm t1
if git push -q origin HEAD:refs/heads/t1 2>/dev/null; then ok "T1 dormant: old-history push allowed with no sentinel file"; else bad "T1 dormant"; fi

printf '# sentinels: oldest changed commit, old main tip, one sha not in the store\n%s\n%s\n0123456789012345678901234567890123456789\n' "$B" "$C" > "$common/piper-old-history-sentinels"

# T2: the danger. Merge the rewritten main into the old branch, push HEAD:main.
git fetch -q origin
git merge -q --no-edit origin/main >/dev/null 2>&1 || { git checkout -q --theirs . 2>/dev/null; git add -A; git commit -qm merge; }
git merge-base --is-ancestor "$B" HEAD && echo "     (merged branch does carry old B)"
out=$(git push origin HEAD:main 2>&1); rc=$?
if [ $rc -ne 0 ] && printf '%s' "$out" | grep -q REFUSED; then ok "T2 old branch merged with new main: push refused"; else bad "T2 rc=$rc: $out"; fi

# T3: the smoke skip does not skip the guard.
out=$(PIPER_SKIP_PREPUSH_SMOKE=1 git push origin HEAD:main 2>&1); rc=$?
if [ $rc -ne 0 ] && printf '%s' "$out" | grep -q REFUSED; then ok "T3 PIPER_SKIP_PREPUSH_SMOKE=1 still refused"; else bad "T3 rc=$rc"; fi

# T4: an old commit pushed to a side branch is refused too (any ref).
out=$(git push origin "${C}:refs/heads/oldside" 2>&1); rc=$?
if [ $rc -ne 0 ]; then ok "T4 old main tip pushed to a side ref: refused"; else bad "T4"; fi

# T5: the right path. Reset to the new main, commit, push.
git reset -q --hard origin/main
echo t5 > t5.txt; git add t5.txt; git commit -qm t5
if git push -q origin HEAD:main 2>/dev/null; then ok "T5 reset + new commit: push allowed"; else bad "T5"; fi

# T6: deleting a ref is allowed.
if git push -q origin :refs/heads/t1 2>/dev/null; then ok "T6 ref deletion allowed"; else bad "T6"; fi

# T7: a branch forked before the oldest changed commit carries no rewritten content: allowed.
if git push -q origin "origin/fork-before-B:refs/heads/fork2" 2>/dev/null; then ok "T7 branch forked before the sentinel: allowed"; else bad "T7"; fi

# T8: the remote's main never received old history.
if git -C ../remote.git merge-base --is-ancestor "$B" main; then bad "T8 remote main contains old B"; else ok "T8 remote main free of old history"; fi

# T9: refusals were logged.
n=$(grep -c outcome=refused "$common/piper-old-history-guard.log" 2>/dev/null || echo 0)
if [ "$n" -eq 3 ]; then ok "T9 guard log has 3 refusals"; else bad "T9 log count $n"; fi

echo "RESULT: $pass passed, $fail failed"
[ $fail -eq 0 ]
