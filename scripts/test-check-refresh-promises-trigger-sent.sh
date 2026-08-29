#!/usr/bin/env bash
# test-check-refresh-promises-trigger-sent.sh — tests the --trigger-sent mode added
# 2026-08-28/29 (CXO's relocation, wired into mail-send.sh).
#
# check-refresh-promises.py computes its ROOT relative to its OWN file location
# (Path(__file__).resolve().parent.parent), not an injectable env var like PIPER_REPO
# — so this can't use the isolated bare-origin+clone harness the other mail-send tests
# use. Instead: read-only checks against real promise-carrying docs (matches the
# script's own "reads only, never writes" contract), plus one temp fixture file
# created under a real sent/ dir and guaranteed removed by the trap, whether the test
# passes or fails.
set -uo pipefail

CHECK="$(cd "$(dirname "$0")" && pwd)/check-refresh-promises.py"
[ -f "$CHECK" ] || { echo "missing $CHECK"; exit 1; }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
FIXTURE=""
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }
cleanup(){ [ -n "$FIXTURE" ] && rm -f "$FIXTURE"; }
trap cleanup EXIT INT TERM

echo "── T1: a path with no ISO date in its filename is silent, exit 0 ──"
out=$(cd "$ROOT" && python3 "$CHECK" --trigger-sent "mailboxes/lead/inbox/no-date-here.md" 2>&1)
rc=$?
[ -z "$out" ] && ok "silent on a non-date filename" || no "unexpected output: $out"
[ "$rc" -eq 0 ] && ok "exit 0 (advisory, never fails)" || no "non-zero exit — must never fail the send"

echo "── T2: a path matching no refresh_trigger_glob anywhere is silent, exit 0 ──"
out=$(cd "$ROOT" && python3 "$CHECK" --trigger-sent "mailboxes/lead/inbox/some-memo-2026-08-29.md" 2>&1)
rc=$?
[ -z "$out" ] && ok "silent on a path matching no promise-carrying doc" || no "unexpected output: $out"
[ "$rc" -eq 0 ] && ok "exit 0" || no "non-zero exit"

echo "── T3: a real, currently-matching trigger reports CURRENT (uses real repo state) ──"
# Find any promise-carrying doc with a refresh_trigger_glob and a real matching file,
# then check whether the newest matching file's date is <= that doc's last_updated —
# if so, --trigger-sent on that exact file must report "still current", never a lapse.
newest_trigger_and_doc=$(cd "$ROOT" && python3 -c "
import glob, re
from pathlib import Path
ROOT = Path('.').resolve()
ISO = re.compile(r'(20\d{2})-(\d{2})-(\d{2})')
for p in sorted(glob.glob('docs/briefing/*.md')):
    path = Path(p)
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        continue
    end = text.find('\n---', 3)
    fm = {}
    for line in text[3:end].splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip().strip('\"').strip(\"'\")
    pattern = fm.get('refresh_trigger_glob')
    updated = fm.get('last_updated', '')
    if not pattern or not ISO.match(updated):
        continue
    triggers = sorted((m.group(0), tp) for tp in glob.glob(pattern) for m in [ISO.search(Path(tp).name)] if m)
    if not triggers:
        continue
    newest_date, newest_path = triggers[-1]
    if newest_date <= updated:
        print(f'{newest_path}|{p}|{updated}')
        break
")
if [ -n "$newest_trigger_and_doc" ]; then
    trig_path="${newest_trigger_and_doc%%|*}"
    rest="${newest_trigger_and_doc#*|}"
    doc_path="${rest%%|*}"
    out=$(cd "$ROOT" && python3 "$CHECK" --trigger-sent "$trig_path" 2>&1)
    echo "$out" | grep -q "still current" && ok "reports current for a real up-to-date trigger ($doc_path)" || no "expected 'still current', got: $out"
else
    echo "  (skipped — no real promise-carrying doc + trigger pair found in current repo state to test against)"
fi

echo "── T4: a synthetic future-dated trigger under a real glob reports LAPSED ──"
# Use CXO's real portfolio glob (mailboxes/cxo/sent/workstream-*-cxo-*.md) with a
# fixture file dated after its last_updated — must report a lapse, never silence.
CXO_UPDATED=$(cd "$ROOT" && python3 -c "
from pathlib import Path
text = Path('docs/briefing/ROLE-PORTFOLIO-CXO.md').read_text(encoding='utf-8')
end = text.find('\n---', 3)
for line in text[3:end].splitlines():
    if line.strip().startswith('last_updated:'):
        print(line.split(':',1)[1].strip())
        break
")
if [ -n "$CXO_UPDATED" ]; then
    FUTURE_DATE="2099-01-01"
    mkdir -p "$ROOT/mailboxes/cxo/sent"
    FIXTURE="$ROOT/mailboxes/cxo/sent/workstream-999-cxo-${FUTURE_DATE}.md"
    printf 'test fixture, safe to delete\n' > "$FIXTURE"
    out=$(cd "$ROOT" && python3 "$CHECK" --trigger-sent "mailboxes/cxo/sent/workstream-999-cxo-${FUTURE_DATE}.md" 2>&1)
    echo "$out" | grep -q "LAPSED" && ok "reports LAPSED for a future-dated trigger past last_updated ($CXO_UPDATED)" || no "expected LAPSED, got: $out"
    echo "$out" | grep -q "bump it now" && ok "includes the fix instruction" || no "missing the fix instruction"
    rm -f "$FIXTURE"; FIXTURE=""
else
    echo "  (skipped — could not read CXO portfolio's last_updated)"
fi

echo "── T5: mail-send.sh's wiring calls this mode without erroring on an ordinary path ──"
out=$(cd "$ROOT" && bash -c '
CHECKREF="'"$ROOT"'/scripts/check-refresh-promises.py"
if [ -f "$CHECKREF" ]; then
    python3 "$CHECKREF" --trigger-sent "mailboxes/lead/inbox/ordinary-memo-2026-08-29.md" 2>&1
fi
echo "WIRING_OK"
')
echo "$out" | grep -q "WIRING_OK" && ok "the exact snippet mail-send.sh runs completes without error" || no "wiring snippet failed: $out"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
