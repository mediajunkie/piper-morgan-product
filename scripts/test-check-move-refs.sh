#!/usr/bin/env bash
# Test for scripts/check-move-refs.sh (#1719): a path with a live reference fails, a path with none passes.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
S=scripts/check-move-refs.sh; fail=0
$S scripts/check-move-refs.sh >/dev/null 2>&1; r=$?          # referenced by the skill and this test
[ "$r" -eq 1 ] || { echo "FAIL: expected exit 1 for a referenced path, got $r"; fail=1; }
$S dev/active/no-such-file-zzz-1719.md >/dev/null 2>&1; r=$?
[ "$r" -eq 0 ] || { echo "FAIL: expected exit 0 for an unreferenced path, got $r"; fail=1; }
$S >/dev/null 2>&1; r=$?
[ "$r" -eq 2 ] || { echo "FAIL: expected exit 2 for no arguments, got $r"; fail=1; }
[ "$fail" -eq 0 ] && echo "test-check-move-refs: 3 of 3 OK"; exit "$fail"
