#!/usr/bin/env bash
# Regression + v0.4 tests for duty-cycle-freeze-check.sh.
#
# PART A — FALSE-STALE regression (PM caught 2026-06-22): ppm was flagged 40h-stale while
# firing every cycle, because (1) age_of() found a heartbeat only from a "(role)"-tagged
# commit (missed "docs(session): PPM …"), and (2) cycling_now() matched only "-opus-log.md"
# (missed Sonnet logs). Fix a92619f9b: heartbeat = (role)-tag OR the role's session-log path,
# any model. Tests reproduce the exact ppm shape (sonnet log + untagged commit) → must not flag;
# a genuinely-old heartbeat → must flag.
#
# PART B — v0.4 WAKE-WINDOW-AWARE threshold (2026-06-26): the flat per-role threshold is replaced
# by one derived from the role's cron cadence — the inter-fire gap bracketing the current hour ×
# ~1.5 + 1h grace. Tight in dense daytime, wide across the big overnight gap. Proof: the SAME age
# flags in daytime but not in the morning/overnight gap. Plus a fallback test (unparseable cron →
# flat thr). Uses the FREEZE_CHECK_NOW_HOUR hook to control time-of-day deterministically.
set -uo pipefail

FC="$(cd "$(dirname "$0")" && pwd)/duty-cycle-freeze-check.sh"
today=$(date +%Y/%m/%d); today_dash=$(date +%Y-%m-%d)
NOW=$(date +%s)
CRON="7 3,10,13,16,19,22"   # cio-shape: daytime gaps 3h (10-13-16-19-22), morning 3→10=7h, overnight 22→3=5h
PASS=0; FAIL=0; TMPS=()
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }
no(){ echo "  ✗ $1"; FAIL=$((FAIL+1)); }
cleanup(){ for d in "${TMPS[@]:-}"; do [ -n "$d" ] && rm -rf "$d"; done; }
trap cleanup EXIT INT TERM

# Fixture: bare origin + clone; testrole TODAY session log is a SONNET log committed at $1 (epoch),
# under an UNTAGGED "docs(session): …" message (the ppm shape). Epoch "@N +0000" is the portable
# GIT_*_DATE form. Echoes the clone path (use as PIPER_REPO).
mkfixture(){
  local when="$1" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    mkdir -p "dev/$today"
    echo "# session log testrole (sonnet)" > "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    git add -A
    GIT_AUTHOR_DATE="@$when +0000" GIT_COMMITTER_DATE="@$when +0000" \
      git commit -qm "docs(session): TestRole afternoon work"   # NO "(testrole)" tag
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

# Registry with just testrole. args: dir, cron_expr, flat_thr. window 0–24, first_fire 00:00 (past).
mkreg(){ local TMP="$1" cron="$2" thr="$3"; printf 'role\tcron\tthr\tws\twe\tff\tsince\n' > "$TMP/reg.tsv"
         printf 'testrole\t%s\t%s\t0\t24\t00:00\t%s\n' "$cron" "$thr" "$today_dash" >> "$TMP/reg.tsv"; echo "$TMP/reg.tsv"; }

run(){ PIPER_REPO="$1" DUTY_CYCLE_REGISTRY="$2" FREEZE_CHECK_NOW_HOUR="$3" bash "$FC" 2>/dev/null; }

echo "freeze-check regression + v0.4:"

# A1 — false-stale regression: fresh sonnet log + untagged commit → not flagged (daytime).
W=$(mkfixture "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
# v0.11 note: BELT-INVISIBLE is expected/orthogonal output here (this fixture writes no heartbeat
# file), so the assertion checks for the absence of a STALE line specifically, not bare emptiness.
echo "$out" | grep -q "^STALE" && no "A1 FALSE-STALE regressed: $out" || ok "A1 live role (sonnet log, untagged) → not flagged"

# A2 — negative control: 10h-old heartbeat in daytime (dyn thr ~5h) → flagged.
W=$(mkfixture "$(( NOW - 36000 ))"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "STALE testrole" && ok "A2 10h-old (daytime) → flagged" || no "A2 FALSE-NEGATIVE: '${out:-<empty>}'"
echo "$out" | grep -q "~2 missed fires" && ok "A2b message states '~2 missed fires' (v0.9 framing)" || no "A2b missing fires-count framing: '${out:-<empty>}'"

# B1+B2 — v0.4 proof: the SAME 9h age flags in daytime (thr~5) but NOT in the morning gap (thr~11).
W=$(mkfixture "$(( NOW - 32400 ))")   # 9h old
R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out_day=$(run "$W" "$R" 11)           # hour 11: between 10 and 13 → gap 3 → thr ~5
out_morn=$(run "$W" "$R" 5)           # hour 5: between 3 and 10 → gap 7 → thr ~11
echo "$out_day" | grep -q "STALE testrole" && ok "B1 v0.4 daytime (thr~5): 9h-old → flagged" || no "B1 v0.4 daytime missed 9h: '${out_day:-<empty>}'"
echo "$out_morn" | grep -q "^STALE" && no "B2 v0.4 false-flagged 9h overnight: $out_morn" || ok "B2 v0.4 morning gap (thr~11): same 9h-old → NOT flagged (wide)"

# B3 — fallback: unparseable cron hours → use the registry flat thr (6h); 7h-old → flagged.
W=$(mkfixture "$(( NOW - 25200 ))")   # 7h old
R=$(mkreg "$(dirname "$W")" "0 x,y" 6)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "STALE testrole" && ok "B3 fallback (unparseable cron → flat thr 6): 7h-old → flagged" || no "B3 fallback broken: '${out:-<empty>}'"
echo "$out" | grep -q "not fire-count-derived" && ok "B3b message labels fallback as non-fire-count (v0.9)" || no "B3b fallback wrongly claims a fires count: '${out:-<empty>}'"

# PART C — v0.10 (2026-09-02): the bare "role: ..." commit-subject form (no parens) must be read
# by ct just as readily as the parenthesized "verb(role):" form. Reproduces the real gap found
# verifying Exec's freeze-check proposal: cohort-position.sh's sibling function already ORs both
# forms; age_of() only had the parenthesized one. Fixture mirrors real history exactly (e.g. "arch:
# carry-forward state refreshed...") — a fresh BARE-form commit with NO session-log touch in the
# same commit (so ct2 can't be the one saving the result) and no heartbeat file at all (ct3 empty).
mkfixture_bare(){
  local when="$1" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    echo "state" > notes.txt
    git add -A
    GIT_AUTHOR_DATE="@$when +0000" GIT_COMMITTER_DATE="@$when +0000" \
      git commit -qm "testrole: state refreshed, bare form, no parens"   # the gap this reproduces
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

W=$(mkfixture_bare "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "^STALE" && no "C1 FALSE-STALE on bare form: $out" || ok "C1 bare 'role: ...' commit form (no parens, no session-log touch) → not flagged"

# PART D — v0.11 (2026-09-03): "alive but belt-invisible" state, distinct from and never affecting
# STALE. A role alive by commit signal but with no heartbeat row for TODAY should get a
# BELT-INVISIBLE line; a role alive AND heartbeat-current should get neither.
mkfixture_with_heartbeat(){
  local when="$1" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    mkdir -p "dev/$today" "dev/heartbeats/$today_dash"
    echo "# session log testrole (sonnet)" > "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    printf '%s\ttestrole\tWORK\n' "$(date -j -f %s "$when" '+%Y-%m-%d %H:%M:%S %Z' 2>/dev/null || date -d "@$when" '+%Y-%m-%d %H:%M:%S %Z')" \
      > "dev/heartbeats/$today_dash/testrole.tsv"
    git add -A
    GIT_AUTHOR_DATE="@$when +0000" GIT_COMMITTER_DATE="@$when +0000" \
      git commit -qm "docs(session): TestRole afternoon work"
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

W=$(mkfixture "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "^BELT-INVISIBLE testrole" && ok "D1 alive, no heartbeat row today → BELT-INVISIBLE fires" || no "D1 expected BELT-INVISIBLE, got: ${out:-<empty>}"
echo "$out" | grep -q "^STALE" && no "D1b BELT-INVISIBLE case wrongly ALSO flagged STALE: $out" || ok "D1b BELT-INVISIBLE never co-occurs with STALE"
echo "$out" | grep -q "last invoked: never" && ok "D1c no last-invoked marker at all → reports 'never' (case b: never invoked)" || no "D1c expected 'last invoked: never', got: $out"

W=$(mkfixture_with_heartbeat "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "BELT-INVISIBLE" && no "D2 alive WITH today's heartbeat row was WRONGLY flagged BELT-INVISIBLE: $out" || ok "D2 alive + heartbeat-current → no BELT-INVISIBLE"
[ -z "$out" ] && ok "D2b fully healthy role → no output at all" || no "D2b expected empty output, got: $out"

# PART E — v0.12 (2026-09-04): the last-invoked marker distinguishes case (a) [working as designed]
# from case (c) [invoked, then stopped — CXO's real incident shape] on the SAME BELT-INVISIBLE line.
mkfixture_with_last_invoked(){
  local commit_when="$1" marker_when="$2" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    mkdir -p "dev/$today" "dev/heartbeats/last-invoked"
    echo "# session log testrole (sonnet)" > "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    marker_ts="$(date -j -f %s "$marker_when" '+%Y-%m-%d %H:%M:%S %Z' 2>/dev/null || date -d "@$marker_when" '+%Y-%m-%d %H:%M:%S %Z')"
    printf '%s\twork\n' "$marker_ts" > "dev/heartbeats/last-invoked/testrole.txt"
    git add -A
    GIT_AUTHOR_DATE="@$commit_when +0000" GIT_COMMITTER_DATE="@$commit_when +0000" \
      git commit -qm "docs(session): TestRole afternoon work"
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

W=$(mkfixture_with_last_invoked "$NOW" "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "working as designed" && ok "E1 last-invoked recent (within threshold) → reports case (a), working as designed" || no "E1 expected 'working as designed', got: $out"

W=$(mkfixture_with_last_invoked "$NOW" "$(( NOW - 24*3600 ))"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "ran before, then stopped" && ok "E2 last-invoked 24h ago (past threshold) → reports case (c), CXO's real incident shape" || no "E2 expected 'ran before, then stopped', got: $out"
echo "$out" | grep -qE "last invoked 24h ago \([0-9]{4}-[0-9]{2}-[0-9]{2}\)" && ok "E2b message includes the actual last-invoked date, not just an hour count" || no "E2b missing the dated marker: $out"

# PART F — v0.13 (2026-09-05): cold-start backfill. A missing marker + REAL prior hb(role) history
# must NOT report "never" — it must derive from git log and say so explicitly. Reproduces Docs'
# exact incident: 20 real heartbeat commits, none since the marker mechanism existed.
mkfixture_hb_history_no_marker(){
  local hb_when="$1" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    mkdir -p "dev/$today" "dev/heartbeats/2026-08-01"
    echo "# session log testrole (sonnet)" > "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    echo "old heartbeat row" > "dev/heartbeats/2026-08-01/testrole.tsv"
    git add -A
    GIT_AUTHOR_DATE="@$hb_when +0000" GIT_COMMITTER_DATE="@$hb_when +0000" \
      git commit -qm "hb(testrole): WORK old real invocation, no last-invoked marker exists"
    # Second commit today keeps the role "alive" by age_of()'s own signal, matching Docs' real
    # shape (active elsewhere, just not on this specific step) — same-role, no marker either.
    echo "# session log testrole (sonnet) day 2" >> "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    git add -A
    GIT_AUTHOR_DATE="@$NOW +0000" GIT_COMMITTER_DATE="@$NOW +0000" \
      git commit -qm "docs(session): TestRole still active, untagged"
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

W=$(mkfixture_hb_history_no_marker "$(( NOW - 24*3600 ))"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "never" && no "F1 REGRESSION: real hb() history with no marker still reports 'never' — Docs' exact cold-start bug: $out" || ok "F1 real hb() history + no marker → does NOT report 'never'"
echo "$out" | grep -q "derived from git history" && ok "F1b message is explicitly labeled as derived, not a direct observation" || no "F1b missing the derived-from-git-history label: $out"
echo "$out" | grep -q "ran before, then stopped" && ok "F1c 24h-old derived invocation, past threshold → correctly reads as case (c)" || no "F1c expected case (c) framing: $out"

W=$(mkfixture_hb_history_no_marker "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "working as designed" && ok "F2 recent derived invocation, within threshold → correctly reads as case (a)" || no "F2 expected case (a) framing: $out"

W=$(mkfixture "$NOW"); R=$(mkreg "$(dirname "$W")" "$CRON" 8)
out=$(run "$W" "$R" 11)
echo "$out" | grep -q "no marker file AND no hb(testrole) commit in the last 9 days" && ok "F3 genuine never-invoked case still states its bound explicitly (no regression on D1c)" || no "F3 'never' message lost its stated bound: $out"

echo "── $PASS passed, $FAIL failed ──"
[ "$FAIL" -eq 0 ]
