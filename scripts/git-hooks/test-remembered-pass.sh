#!/usr/bin/env bash
# Synthetic end-to-end test of the remembered pass in scripts/git-hooks/pre-push (standing row 9u).
# Usage: scripts/git-hooks/test-remembered-pass.sh <new empty scratch dir> scripts/git-hooks/pre-push
# Builds a bare remote and a seat clone whose gates and smoke are stand-ins that count their runs,
# and a second clone that lands a log while the gates run (the lost race).
# Touches nothing outside the scratch dir.
# Concept: docs/internal/operations/canonical-ops-recipes.md (section 5, pushing to main under contention)
set -u
S="$1"; HOOK="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
mkdir -p "$S" && cd "$S" || exit 2
S="$(pwd)"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
export GIT_AUTHOR_NAME=t GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=t GIT_COMMITTER_EMAIL=t@t
pass=0; fail=0
ok()  { echo "PASS $1"; pass=$((pass+1)); }
bad() { echo "FAIL $1"; fail=$((fail+1)); }
gates_runs() { wc -l < "$S/gates.count" 2>/dev/null | tr -d ' ' || echo 0; }
smoke_runs() { wc -l < "$S/smoke.count" 2>/dev/null | tr -d ' ' || echo 0; }
light_runs() { wc -l < "$S/light.count" 2>/dev/null | tr -d ' ' || echo 0; }
: > "$S/gates.count"; : > "$S/smoke.count"; : > "$S/light.count"

git init -q --bare -b main remote.git
git init -q -b main seed
cd seed
git remote add origin ../remote.git
mkdir -p scripts tests dev/2026/11/16 dev/active mailboxes/x/inbox
# Stand-in gates: count the run; fail when the tree holds a file named FAIL-GATE.
cat > scripts/run-push-gates.sh <<EOS
#!/usr/bin/env bash
# The narrowed run (the three lints that read dated logs and mail): counted on its own, and it
# fails when a dated log or a mail file holds the marker CREDENTIAL-SHAPE.
case " \$* " in *" --logs-and-mail "*)
  echo run >> "$S/light.count"
  if grep -rq "CREDENTIAL-SHAPE" dev/2026 mailboxes 2>/dev/null; then
    echo "FAIL  stand-in bearer lint"; echo "run-push-gates: 3 gates, 2 passed, 1 failed, 0 unchecked"; exit 1
  fi
  echo "run-push-gates: 3 gates, 3 passed, 0 failed, 0 unchecked"; exit 0 ;;
esac
echo run >> "$S/gates.count"
# While the gates "run", another seat lands a dated log and a mail file on main (the race).
if [ -e "$S/race" ]; then
  rm -f "$S/race"
  ( cd "$S/other" && git pull -q origin main && echo r >> dev/2026/11/16/other-log.md && echo r >> mailboxes/x/inbox/o.md \
    && git add -A && git commit -qm "log race" && git push -q origin HEAD:main ) >/dev/null 2>&1
fi
if [ -e scripts/FAIL-GATE ]; then echo "FAIL  stand-in"; echo "run-push-gates: 1 gates, 0 passed, 1 failed, 0 unchecked"; exit 1; fi
echo "run-push-gates: 1 gates, 1 passed, 0 failed, 0 unchecked"
EOS
# Stand-in pytest env: a "python" that counts the run and prints a passing summary.
cat > scripts/fake-python <<EOS
#!/usr/bin/env bash
echo run >> "$S/smoke.count"
echo "1 passed in 0.01s"
EOS
cat > scripts/ensure-pytest-env.sh <<'EOS'
#!/usr/bin/env bash
echo "$(cd "$(dirname "$0")" && pwd)/fake-python"
EOS
chmod +x scripts/run-push-gates.sh scripts/fake-python scripts/ensure-pytest-env.sh
echo a > tests/test_a.py; echo log > dev/2026/11/16/a-log.md; echo s > dev/active/standing.md; echo m > mailboxes/x/inbox/m.md
git add -A; git commit -qm seed; git push -q origin main
cd ..

git clone -q remote.git seat; git clone -q remote.git other
for c in seat other; do cp "$HOOK" $c/.git/hooks/pre-push; chmod +x $c/.git/hooks/pre-push; done

cd seat
# T1: a code push runs both checks once and records the pass.
echo b > tests/test_b.py; git add -A; git commit -qm code
touch "$S/race"
out=$(git push origin HEAD:main 2>&1); rc=$?
if [ $rc -ne 0 ] && [ "$(gates_runs)" = 1 ] && [ "$(smoke_runs)" = 1 ]; then ok "T1 first push runs gates and smoke once, then loses the race"; else bad "T1 rc=$rc gates=$(gates_runs) smoke=$(smoke_runs): $out"; fi

# T2: the retry after merging another seat's log is not re-run, and lands.
git fetch -q origin; git merge -q --no-edit origin/main
out=$(git push origin HEAD:main 2>&1); rc=$?
if [ $rc -eq 0 ] && [ "$(gates_runs)" = 1 ] && [ "$(smoke_runs)" = 1 ] && [ "$(light_runs)" = 1 ] && printf '%s' "$out" | grep -q "gates already passed" && printf '%s' "$out" | grep -q "smoke already passed"; then ok "T2 retry after a log-only merge: remembered, not re-run, landed"; else bad "T2 rc=$rc gates=$(gates_runs) smoke=$(smoke_runs): $out"; fi
grep -q "outcome=gates-cached" "$(git rev-parse --git-common-dir)/piper-prepush-smoke.log" && grep -q "outcome=smoke-cached" "$(git rev-parse --git-common-dir)/piper-prepush-smoke.log" && ok "T2b both skips are logged" || bad "T2b log lines"

# T3: any change outside dated logs and mail makes a new key and a full run.
echo c > tests/test_c.py; git add -A; git commit -qm code2
out=$(git push origin HEAD:main 2>&1); rc=$?
if [ $rc -eq 0 ] && [ "$(gates_runs)" = 2 ] && [ "$(smoke_runs)" = 2 ]; then ok "T3 a new code change runs both again"; else bad "T3 rc=$rc gates=$(gates_runs) smoke=$(smoke_runs): $out"; fi

# T4: a change under dev/active (not a dated log) also makes a new key.
echo d > tests/test_d.py; git add -A; git commit -qm code3
git push -q origin HEAD:main 2>/dev/null; g=$(gates_runs)
echo more >> dev/active/standing.md; echo e > tests/test_e.py; git add -A; git commit -qm "standing + code"
out=$(git push origin HEAD:main 2>&1); rc=$?
if [ $rc -eq 0 ] && [ "$(gates_runs)" = $((g+1)) ]; then ok "T4 dev/active is part of the key"; else bad "T4 rc=$rc gates=$(gates_runs) g=$g"; fi

# T5: a failing gate is never remembered.
touch scripts/FAIL-GATE; git add -A; git commit -qm "bad gate"
g=$(gates_runs)
out=$(git push origin HEAD:main 2>&1); rc1=$?
out=$(git push origin HEAD:main 2>&1); rc2=$?
if [ $rc1 -ne 0 ] && [ $rc2 -ne 0 ] && [ "$(gates_runs)" = $((g+2)) ]; then ok "T5 a failed gate blocks twice and is run twice"; else bad "T5 rc1=$rc1 rc2=$rc2 gates=$(gates_runs) g=$g"; fi
git rm -q scripts/FAIL-GATE; git commit -qm "fix gate"; git push -q origin HEAD:main 2>/dev/null

# T6: pushing a commit that is not checked out warns, and its pass is not recorded.
git checkout -q -b side; echo f > tests/test_f.py; git add -A; git commit -qm side; SIDE=$(git rev-parse HEAD)
git checkout -q main 2>/dev/null || git checkout -q -
g=$(gates_runs)
out=$(git push origin "$SIDE:refs/heads/side" 2>&1); rc=$?
out2=$(git push origin "$SIDE:refs/heads/side2" 2>&1)
if printf '%s' "$out" | grep -q "is not the one checked out" && [ "$(gates_runs)" = $((g+2)) ]; then ok "T6 a commit that is not checked out: warned, never remembered"; else bad "T6 gates=$(gates_runs) g=$g: $out"; fi

# T7: a dirty tree is not recorded.
git checkout -q side; echo g > tests/test_g.py; git add -A; git commit -qm side2
echo stray > stray.txt
g=$(gates_runs)
git push -q origin HEAD:refs/heads/side3 2>/dev/null; git push -q origin HEAD:refs/heads/side4 2>/dev/null
if [ "$(gates_runs)" = $((g+2)) ]; then ok "T7 a dirty tree's pass is not remembered"; else bad "T7 gates=$(gates_runs) g=$g"; fi
rm stray.txt

# T8: PIPER_PREPUSH_NO_CACHE=1 forces a full run.
git push -q origin HEAD:refs/heads/side5 2>/dev/null; g=$(gates_runs)
PIPER_PREPUSH_NO_CACHE=1 git push -q origin HEAD:refs/heads/side6 2>/dev/null
if [ "$(gates_runs)" = $((g+1)) ]; then ok "T8 PIPER_PREPUSH_NO_CACHE=1 runs the gates again"; else bad "T8 gates=$(gates_runs) g=$g"; fi

# T9: a pass older than the window is not honoured.
pf="$(git rev-parse --git-common-dir)/piper-prepush-pass.log"
sed -i.bak -E 's/^ts=[0-9]+ /ts=1000 /' "$pf"
g=$(gates_runs)
git push -q origin HEAD:refs/heads/side7 2>/dev/null
if [ "$(gates_runs)" = $((g+1)) ]; then ok "T9 a pass outside the 30-minute window is run again"; else bad "T9 gates=$(gates_runs) g=$g"; fi

# T10 (Lead's condition): a retry whose only change is a dated log holding a credential-shaped
# string is blocked by the narrowed lints, and the full gates are still not re-run.
echo h > tests/test_h.py; git add -A; git commit -qm code-h
git push -q origin HEAD:refs/heads/side8 2>/dev/null
g=$(gates_runs); l=$(light_runs)
echo "pasted CREDENTIAL-SHAPE here" >> dev/2026/11/16/a-log.md; git add -A; git commit -qm "log with a credential shape"
out=$(git push origin HEAD:refs/heads/side9 2>&1); rc=$?
if [ $rc -ne 0 ] && [ "$(gates_runs)" = "$g" ] && [ "$(light_runs)" = $((l+1)) ] && printf '%s' "$out" | grep -q "reads session logs and mail FAILED"; then ok "T10 a credential shape in a dated log blocks a remembered pass; full gates not re-run"; else bad "T10 rc=$rc gates=$(gates_runs) g=$g light=$(light_runs) l=$l: $out"; fi
grep -q "outcome=gates-cached-lint-fail" "$(git rev-parse --git-common-dir)/piper-prepush-smoke.log" && ok "T10b the block is logged" || bad "T10b log line"

# T11: with the string removed, the same remembered pass lets the push through.
sed -i.bak '/CREDENTIAL-SHAPE/d' dev/2026/11/16/a-log.md; rm -f dev/2026/11/16/a-log.md.bak; git add -A; git commit -qm "log cleaned"
out=$(git push origin HEAD:refs/heads/side9 2>&1); rc=$?
if [ $rc -eq 0 ] && [ "$(gates_runs)" = "$g" ]; then ok "T11 cleaned log: remembered pass honoured, landed"; else bad "T11 rc=$rc gates=$(gates_runs) g=$g: $out"; fi

# T12: the not-checked-out warning is logged.
grep -q "outcome=not-checked-out" "$(git rev-parse --git-common-dir)/piper-prepush-smoke.log" && ok "T12 a push of a commit that is not checked out is logged" || bad "T12 log line"

echo "remembered-pass: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
