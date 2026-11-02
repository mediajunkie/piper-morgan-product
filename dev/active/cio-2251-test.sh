#!/usr/bin/env bash
# cio-2251-test.sh — tests check-branch.sh's #2251 change in a throwaway repo (CIO, 2026-11-02).
# Usage: bash dev/active/cio-2251-test.sh [path-to-hook]   (default: .claude/hooks/check-branch.sh)
# CIO's seat refuses this test and the hook edit, so xian runs it. Expected results are on each line.
set -u
HOOK=$(cd "$(dirname "${1:-.claude/hooks/check-branch.sh}")" && pwd)/$(basename "${1:-.claude/hooks/check-branch.sh}")
R=$(mktemp -d "${TMPDIR:-/tmp}/t2251.XXXXXX")
cd "$R" || exit 1
git init -q -b main . && git config user.email t@t && git config user.name t
echo r > README && git add README && git commit -qm c0 --no-verify
mkdir -p mailboxes/x && echo a > mailboxes/x/a.md && git add mailboxes/x/a.md && git commit -qm c1 --no-verify
git update-ref refs/remotes/origin/main HEAD
echo b > mailboxes/x/b.md && git add mailboxes/x/b.md && git commit -qm c2 --no-verify
git branch side && git reset -q --hard HEAD~1
git checkout -q -b feat HEAD~1

FAILS=0
j() { python3 -c 'import json,sys; print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$1"; }
check() {  # name, expected exit, actual exit
    if [ "$2" = "$3" ]; then echo "PASS  $1 (exit $3)"; else echo "FAIL  $1 (expected $2, got $3)"; FAILS=$((FAILS+1)); fi
}

git merge -q --no-commit --no-ff origin/main >/dev/null 2>&1
j 'git commit -m merge' | bash "$HOOK" >/dev/null 2>&1; check "A: merge carrying only main's mail, commit" 0 $?
git merge --abort

git merge -q --no-commit --no-ff side >/dev/null 2>&1
j 'git commit -m x' | bash "$HOOK" >/dev/null 2>&1; check "B: new mail staged, commit" 2 $?
j 'git diff --cached --name-only | grep mail; git status -s' | bash "$HOOK" >/dev/null 2>&1; check "C: new mail staged, read-only compound" 0 $?
j 'git add README && git commit -m x' | bash "$HOOK" >/dev/null 2>&1; check "D: new mail staged, compound with a commit" 2 $?
bash "$HOOK" </dev/null >/dev/null 2>&1; check "E: new mail staged, no JSON (git pre-commit layer)" 2 $?
echo 'not json' | bash "$HOOK" >/dev/null 2>&1; check "F: new mail staged, unparseable stdin" 2 $?
git merge --abort

cd / && rm -rf "$R"
echo "$FAILS failed of 6"
[ "$FAILS" -eq 0 ]
