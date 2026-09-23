#!/usr/bin/env bash
# test-usage-capture.sh — regression tests for usage-capture.sh and usage-lookup.sh (issue #1862).
# Mirrors test-duty-cycle-freeze-check.sh's style: isolated throwaway git repos, ok/no counters,
# a PASS/FAIL summary. Never touches the real dev/heartbeats/usage-per-account.tsv and never hits
# the real endpoint — every reader here is a local stub.
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
CAP="$HERE/usage-capture.sh"
LOOK="$HERE/usage-lookup.sh"
[ -f "$CAP" ] || { echo "missing $CAP"; exit 1; }
[ -f "$LOOK" ] || { echo "missing $LOOK"; exit 1; }

export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=t@t
T="$(mktemp -d "${TMPDIR:-/tmp}/usagetest.XXXXXX")"
trap 'rm -rf "$T"' EXIT
PASS=0; FAIL=0
ok(){ echo "  PASS: $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL: $1"; FAIL=$((FAIL+1)); }

mkrepo(){
  local d; d="$(mktemp -d "$T/repo.XXXXXX")"
  ( cd "$d" && git init -q && git config user.email t@t.test && git config user.name tester )
  echo "$d"
}

TSV_REL="dev/heartbeats/usage-per-account.tsv"

# ── four stub readers, one per reader outcome named in the build spec ──────────────────────────
STUB_GOOD="$T/stub-good.sh"
cat > "$STUB_GOOD" <<'EOF'
#!/usr/bin/env bash
printf '%s\t5\t2026-09-23T22:20\t100\t2026-09-25T05:00\n' "$1"
EOF
chmod +x "$STUB_GOOD"

STUB_UNREADABLE="$T/stub-unreadable.sh"
cat > "$STUB_UNREADABLE" <<'EOF'
#!/usr/bin/env bash
printf '%s\tUNREADABLE\tno credential under keychain service "test"\n' "$1"
exit 3
EOF
chmod +x "$STUB_UNREADABLE"

STUB_UNMEASURABLE="$T/stub-unmeasurable.sh"
cat > "$STUB_UNMEASURABLE" <<'EOF'
#!/usr/bin/env bash
printf '%s\tUNMEASURABLE\tendpoint shape changed or auth failed: ValueError\n' "$1"
EOF
chmod +x "$STUB_UNMEASURABLE"

STUB_GARBAGE="$T/stub-garbage.sh"
cat > "$STUB_GARBAGE" <<'EOF'
#!/usr/bin/env bash
printf 'not even close to tsv shape\n'
EOF
chmod +x "$STUB_GARBAGE"

echo "usage-capture / usage-lookup tests:"

# ── T1: good reader -> two correct rows appended, real numbers, no failure token ───────────────
R1="$(mkrepo)"
out=$(cd "$R1" && bash "$CAP" --reader "$STUB_GOOD" 2>&1)
tsv="$R1/$TSV_REL"
if [ -f "$tsv" ]; then ok "T1 TSV created"; else no "T1 TSV missing: $out"; fi
rows=$(grep -vc '^#' "$tsv" 2>/dev/null || echo 0)
[ "$rows" -eq 3 ] && ok "T1 header + 2 data rows present (3 non-comment lines)" || no "T1 wrong row count: $rows"

# field(file, account, N) -> Nth tab-separated field of the row for that account (portable, no PCRE)
field(){ awk -F'\t' -v acct="$2" -v n="$3" '$2==acct{print $n; exit}' "$1"; }

row1_pm=$(awk -F'\t' '$2=="pipermorgan.ai"{print}' "$tsv")
[ "$(field "$tsv" pipermorgan.ai 3)" = "~/.claude-pm" ] \
  && [ "$(field "$tsv" pipermorgan.ai 4)" = "5" ] \
  && [ "$(field "$tsv" pipermorgan.ai 5)" = "2026-09-23T22:20" ] \
  && [ "$(field "$tsv" pipermorgan.ai 6)" = "100" ] \
  && [ "$(field "$tsv" pipermorgan.ai 7)" = "2026-09-25T05:00" ] \
  && [ "$(field "$tsv" pipermorgan.ai 8)" = "stub-good.sh" ] \
  && [ "$(field "$tsv" pipermorgan.ai 9)" = "" ] \
  && ok "T1 pipermorgan.ai row has real numbers, empty note" \
  || no "T1 pipermorgan.ai row malformed: $row1_pm"

row1_dp=$(awk -F'\t' '$2=="designinproduct.com"{print}' "$tsv")
[ "$(field "$tsv" designinproduct.com 3)" = "~/.claude" ] \
  && [ "$(field "$tsv" designinproduct.com 4)" = "5" ] \
  && ok "T1 designinproduct.com row present" \
  || no "T1 designinproduct.com row missing/malformed: $row1_dp"

# ── T2: --dry-run prints rows, appends nothing (no file at all) ────────────────────────────────
R2="$(mkrepo)"
out=$(cd "$R2" && bash "$CAP" --reader "$STUB_GOOD" --dry-run 2>&1)
echo "$out" | grep -q "pipermorgan.ai" && ok "T2 dry-run prints a would-be pipermorgan.ai row" || no "T2 dry-run printed nothing useful: $out"
[ -f "$R2/$TSV_REL" ] && no "T2 dry-run wrote a file — should touch nothing" || ok "T2 dry-run touched nothing"

# ── T3: UNREADABLE -> failure row, token verbatim, reason in note, numeric cols empty, exit 0 ──
R3="$(mkrepo)"
out=$(cd "$R3" && bash "$CAP" --reader "$STUB_UNREADABLE" 2>&1); rc=$?
[ "$rc" -eq 0 ] && ok "T3 UNREADABLE: exit 0 (recorded, not fatal)" || no "T3 UNREADABLE: wrong exit $rc"
line=$(awk -F'\t' '$2=="pipermorgan.ai"{print}' "$R3/$TSV_REL")
[ "$(field "$R3/$TSV_REL" pipermorgan.ai 4)" = "UNREADABLE" ] \
  && [ "$(field "$R3/$TSV_REL" pipermorgan.ai 5)" = "" ] \
  && [ "$(field "$R3/$TSV_REL" pipermorgan.ai 6)" = "" ] \
  && [ "$(field "$R3/$TSV_REL" pipermorgan.ai 7)" = "" ] \
  && ok "T3 UNREADABLE token verbatim, numeric cols empty" || no "T3 UNREADABLE row malformed: $line"
echo "$line" | grep -q "no credential under keychain service" && ok "T3 UNREADABLE reason text in note" || no "T3 UNREADABLE reason missing: $line"

# ── T4: UNMEASURABLE -> same shape, different token ─────────────────────────────────────────────
R4="$(mkrepo)"
out=$(cd "$R4" && bash "$CAP" --reader "$STUB_UNMEASURABLE" 2>&1); rc=$?
[ "$rc" -eq 0 ] && ok "T4 UNMEASURABLE: exit 0" || no "T4 UNMEASURABLE: wrong exit $rc"
line=$(awk -F'\t' '$2=="pipermorgan.ai"{print}' "$R4/$TSV_REL")
[ "$(field "$R4/$TSV_REL" pipermorgan.ai 4)" = "UNMEASURABLE" ] \
  && [ "$(field "$R4/$TSV_REL" pipermorgan.ai 5)" = "" ] \
  && [ "$(field "$R4/$TSV_REL" pipermorgan.ai 6)" = "" ] \
  && [ "$(field "$R4/$TSV_REL" pipermorgan.ai 7)" = "" ] \
  && ok "T4 UNMEASURABLE token verbatim, numeric cols empty" || no "T4 UNMEASURABLE row malformed: $line"
echo "$line" | grep -q "endpoint shape changed" && ok "T4 UNMEASURABLE reason text in note" || no "T4 UNMEASURABLE reason missing: $line"

# ── T5: garbage reader output -> ALWAYS lands as UNMEASURABLE, never a plausible number ─────────
R5="$(mkrepo)"
out=$(cd "$R5" && bash "$CAP" --reader "$STUB_GARBAGE" 2>&1); rc=$?
[ "$rc" -eq 0 ] && ok "T5 garbage: exit 0 (recorded, not fatal)" || no "T5 garbage: wrong exit $rc"
line=$(awk -F'\t' '$2=="pipermorgan.ai"{print}' "$R5/$TSV_REL")
pct=$(field "$R5/$TSV_REL" pipermorgan.ai 4)
[ "$pct" = "UNMEASURABLE" ] \
  && [ "$(field "$R5/$TSV_REL" pipermorgan.ai 5)" = "" ] \
  && [ "$(field "$R5/$TSV_REL" pipermorgan.ai 6)" = "" ] \
  && [ "$(field "$R5/$TSV_REL" pipermorgan.ai 7)" = "" ] \
  && ok "T5 garbage lands as UNMEASURABLE, numeric cols empty" || no "T5 garbage did NOT land as UNMEASURABLE: $line"
echo "$line" | grep -q "reader output not recognized" && ok "T5 garbage note explains the fallback" || no "T5 garbage note missing explanation: $line"
case "$pct" in
  ''|*[!0-9.]*) ok "T5 no plausible number leaked from garbage (got: '$pct')" ;;
  *) no "T5 REGRESSION: garbage produced a numeric-looking five_hour_pct: '$pct'" ;;
esac

# ── T6: missing reader -> non-zero exit, no file written at all ────────────────────────────────
R6="$(mkrepo)"
out=$(cd "$R6" && bash "$CAP" --reader "$T/no-such-reader.sh" 2>&1); rc=$?
[ "$rc" -ne 0 ] && ok "T6 missing reader: non-zero exit ($rc)" || no "T6 missing reader: should have failed, got exit 0"
[ -f "$R6/$TSV_REL" ] && no "T6 missing reader: TSV should not exist — a row was written" || ok "T6 missing reader: nothing written"
echo "$out" | grep -qi "setup fault" && ok "T6 message distinguishes setup fault from a read fault" || no "T6 message doesn't name it a setup fault: $out"

# ── T7: token never appears anywhere in combined output across all runs above ──────────────────
combined="$out"
for r in "$R1" "$R3" "$R4" "$R5"; do combined="$combined $(cat "$r/$TSV_REL" 2>/dev/null)"; done
echo "$combined" | grep -qi "accessToken\|Bearer " && no "T7 REGRESSION: something resembling a token leaked into output" || ok "T7 no token-shaped string in any output or TSV"

echo
echo "usage-lookup tests:"

# ── T8: fixed TSV with two known readings; timestamp between them returns the earlier row ──────
R8="$(mkrepo)"
mkdir -p "$R8/dev/heartbeats"
cat > "$R8/$TSV_REL" <<'EOF'
ts_local	account	config_dir	five_hour_pct	five_hour_reset	seven_day_pct	seven_day_reset	source	note
2026-09-23 09:00 PDT	pipermorgan.ai	~/.claude-pm	5	2026-09-23T22:20	100	2026-09-25T05:00	usage-read.sh
2026-09-23 09:00 PDT	designinproduct.com	~/.claude	14	2026-09-23T21:00	88	2026-09-24T04:00	usage-read.sh
2026-09-23 15:00 PDT	pipermorgan.ai	~/.claude-pm	40	2026-09-23T22:20	100	2026-09-25T05:00	usage-read.sh
# account -> seats companion block
# pipermorgan.ai: arch cio comms cxo docs exec host lead pa ppm web
EOF
out=$(cd "$R8" && bash "$LOOK" "2026-09-23 11:00" pipermorgan.ai)
echo "$out" | grep -q "09:00 PDT" && ok "T8 between-readings lookup returns the earlier (09:00) row" || no "T8 wrong row: $out"

# ── T9: timestamp exactly at a reading returns that reading (at-or-before, inclusive) ──────────
out=$(cd "$R8" && bash "$LOOK" "2026-09-23 15:00" pipermorgan.ai)
echo "$out" | grep -q "15:00 PDT" && ok "T9 at-or-before is inclusive of an exact match" || no "T9 wrong row: $out"

# ── T10: timestamp before the first reading -> NO-ROW (literal, not empty) ─────────────────────
out=$(cd "$R8" && bash "$LOOK" "2026-09-20 00:00" pipermorgan.ai)
[ "$out" = "NO-ROW" ] && ok "T10 before-first-reading -> literal NO-ROW" || no "T10 expected NO-ROW, got: '$out'"

# ── T11: account filter respected — designinproduct.com lookup ignores pipermorgan.ai rows ─────
out=$(cd "$R8" && bash "$LOOK" "2026-09-23 23:59" designinproduct.com)
echo "$out" | grep -q "designinproduct.com" && ok "T11 account filter returns the right account's row" || no "T11 wrong account or row: $out"

# ── T12: unknown account with no rows at all -> NO-ROW ──────────────────────────────────────────
out=$(cd "$R8" && bash "$LOOK" "2026-09-23 23:59" nobody.example)
[ "$out" = "NO-ROW" ] && ok "T12 unknown account -> literal NO-ROW" || no "T12 expected NO-ROW, got: '$out'"

# ── T13: comment lines are skipped, never mistaken for a data row ──────────────────────────────
echo "$out" | grep -q "^#" && no "T13 REGRESSION: a comment line leaked as a result" || ok "T13 comment lines never surface as a result"

# ── T14: no TSV at all -> NO-ROW, not an error ──────────────────────────────────────────────────
R14="$(mkrepo)"
out=$(cd "$R14" && bash "$LOOK" "2026-09-23 12:00" pipermorgan.ai); rc=$?
[ "$out" = "NO-ROW" ] && [ "$rc" -eq 0 ] && ok "T14 no TSV file -> NO-ROW, exit 0" || no "T14 unexpected: out='$out' rc=$rc"

echo
echo "Summary: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
