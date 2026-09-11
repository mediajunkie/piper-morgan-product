#!/usr/bin/env bash
# Tests for scope-drift-check.sh (standing-item 7t, CIO's detection-predicate half).
#
# Mocks `gh` for determinism (no real network/auth dependency) and builds a real git repo with
# real commits — the negation-parsing logic in Signal A is exactly the kind of thing a hand-rolled
# string check could get subtly wrong, so this exercises the real script against real commit
# messages throughout, not a simulation of its output.
set -uo pipefail

SC="$(cd "$(dirname "$0")" && pwd)/scope-drift-check.sh"
PASS=0; FAIL=0; TMPS=()
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }
no(){ echo "  ✗ $1"; FAIL=$((FAIL+1)); }
cleanup(){ for d in "${TMPS[@]:-}"; do [ -n "$d" ] && rm -rf "$d"; done; }
trap cleanup EXIT INT TERM

# Fixture repo with a linear commit history exercising every case.
mkfixture(){
  local TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init -q "$TMP"
  ( cd "$TMP"
    git config user.email t@t.test; git config user.name tester
    echo base > f.txt; git add -A; git commit -qm "base commit"

    # Case A-positive: closure language immediately before #N (GitHub's own convention), issue
    # will be mocked OPEN -> should flag.
    echo a1 >> f.txt; git add -A; git commit -qm "fix: resolves #9001"

    # Case A-negated: "not yet resolved: #9002" -- issue mocked OPEN -> must NOT flag.
    echo a2 >> f.txt; git add -A; git commit -qm "Flagged, not yet resolved: #9002 needs more work"

    # Case A on a CLOSED issue -- correctly closed, no drift -> must NOT flag.
    echo a3 >> f.txt; git add -A; git commit -qm "fix: resolved #9003 cleanly"

    # Reference with no closure language at all -- pure mention -> must NOT flag under signal A.
    echo a4 >> f.txt; git add -A; git commit -qm "docs: note related to #9004, no fix here"

    # References for signal B (checkbox-complete vs not) -- any commit form is fine, signal B
    # reads the ISSUE body, not the commit language.
    echo b1 >> f.txt; git add -A; git commit -qm "chore: touched #9005 in passing"
    echo b2 >> f.txt; git add -A; git commit -qm "chore: touched #9006 in passing"
  )
  echo "$TMP"
}

# Mock `gh` covering every issue number used above.
mkmockgh(){
  local TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  cat > "$TMP/gh" <<'MOCKEOF'
#!/usr/bin/env bash
# usage inside the script under test: gh api repos/<repo>/issues/<N> --jq '<expr>'
path="$2"
jqexpr="$4"
num="${path##*/}"
case "$num" in
  9001) state="open"; body="" ;;
  9002) state="open"; body="" ;;
  9003) state="closed"; body="" ;;
  9004) state="open"; body="" ;;
  9005) state="open"; body=$'- [x] one\n- [x] two' ;;                    # 100% checked -> flag B
  9006) state="open"; body=$'- [x] one\n- [ ] two\n- [x] three' ;;       # not 100% -> no flag B
  *) state="open"; body="" ;;
esac
case "$jqexpr" in
  *state*) echo "$state" ;;
  *body*) printf '%s\n' "$body" ;;
  *) echo "" ;;
esac
MOCKEOF
  chmod +x "$TMP/gh"
  echo "$TMP"
}

echo "scope-drift-check tests:"

REPO=$(mkfixture)
MOCK=$(mkmockgh)
out=$(cd "$REPO" && PATH="$MOCK:$PATH" bash "$SC" "HEAD~6..HEAD" 2>/tmp/sdc-err.$$)
err=$(cat /tmp/sdc-err.$$); rm -f /tmp/sdc-err.$$

echo "$out" | grep -q "^DRIFT-A #9001" && ok "T1 closure-language + OPEN issue -> DRIFT-A fires" || no "T1 expected DRIFT-A for #9001, got: $out"
echo "$out" | grep -q "#9002" && no "T2 REGRESSION: negated closure language ('not yet resolved') wrongly flagged #9002: $out" || ok "T2 negated closure language correctly does NOT flag #9002"
echo "$out" | grep -q "#9003" && no "T3 correctly-closed issue (#9003) wrongly flagged: $out" || ok "T3 closure-language on an already-CLOSED issue does not flag (no drift, it's correct)"
echo "$out" | grep -q "#9004" && no "T4 a bare mention with no closure language wrongly flagged #9004: $out" || ok "T4 bare issue mention (no closure language) does not trigger signal A"
echo "$out" | grep -q "^DRIFT-B #9005" && ok "T5 100%-checked-but-open issue -> DRIFT-B fires" || no "T5 expected DRIFT-B for #9005, got: $out"
echo "$out" | grep -q "#9006" && no "T6 REGRESSION: partially-checked issue (#9006) wrongly flagged: $out" || ok "T6 partially-checked issue correctly does not flag"

echo "$err" | grep -qE "checked 6 commit" && ok "T7 denominator line states commits checked" || no "T7 missing commit count in denominator: $err"
echo "$err" | grep -qE "6 issue reference" && ok "T7b denominator line states issue-reference count" || no "T7b missing reference count: $err"
echo "$err" | grep -qE "2 flagged" && ok "T7c denominator line states flagged count correctly (2: #9001 + #9005)" || no "T7c wrong flagged count in denominator: $err"

# T8 -- non-git directory -> loud AND a distinguishable non-zero exit (v1.1 correction: Arch's
# Action already checked `rc -gt 1` to catch exactly this; v1.0 always exited 0, making that
# branch dead code that could never fire for the error it exists to catch).
NOTGIT=$(mktemp -d); TMPS+=("$NOTGIT")
out2=$(cd "$NOTGIT" && SCOPE_DRIFT_REPO="$NOTGIT" bash "$SC" 2>&1); rc2=$?
echo "$out2" | grep -q "measured NOTHING" && ok "T8 non-git directory reports 'measured NOTHING' rather than a silent empty pass" || no "T8 expected 'measured NOTHING' for a non-git dir, got: $out2"
[ "$rc2" -gt 1 ] && ok "T8b non-git-dir case exits with rc>1 (matches Arch's Action's error-detection contract)" || no "T8b expected rc>1 for a non-git dir, got rc=$rc2"

# T9 -- malformed commit range -> also loud AND rc>1, distinguished from a legitimately empty range
REPO2=$(mkfixture)
out3=$(cd "$REPO2" && bash "$SC" "not-a-real-range..also-not-real" 2>&1); rc3=$?
echo "$out3" | grep -q "measured NOTHING" && ok "T9 malformed range reports 'measured NOTHING'" || no "T9 expected 'measured NOTHING' for a bad range, got: $out3"
[ "$rc3" -gt 1 ] && ok "T9b malformed range exits with rc>1, not silently read as zero commits" || no "T9b expected rc>1 for a malformed range, got rc=$rc3"

# T10 -- a legitimately EMPTY (but valid) range must NOT be confused with the malformed case above
out4=$(cd "$REPO2" && bash "$SC" "HEAD..HEAD" 2>&1); rc4=$?
[ "$rc4" -eq 0 ] && ok "T10 a valid but empty range (HEAD..HEAD) exits 0, distinct from the malformed-range error" || no "T10 expected rc=0 for a valid empty range, got rc=$rc4"
echo "$out4" | grep -qE "checked 0 commit" && ok "T10b denominator correctly reports 0 commits for the empty range, not an error" || no "T10b expected 'checked 0 commit' for the empty range, got: $out4"

echo "── $PASS passed, $FAIL failed ──"
[ "$FAIL" -eq 0 ]
