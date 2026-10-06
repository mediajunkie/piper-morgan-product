#!/usr/bin/env bash
# main-ci-status.sh — latest COMPLETED conclusion on main for EVERY workflow that runs on push to main.
#
# Why (2026-10-05, Lead's finding): duty-cycle-tick Step 1e read only lint.yml (Code Quality), so the
# Architecture Enforcement ratchet sat red for 41 consecutive runs (10-01 → 10-05) with nobody looking
# — #1892's shape one workflow over. The list is DERIVED from .github/workflows (push triggers that
# include main), not hardcoded, so a new gating workflow is covered the day it lands.
#
# Per workflow: skips cancelled/skipped runs (a superseded run says nothing about the code) and prints
# the first success/failure among the last 20 main runs, with its age. Path-filtered workflows may be
# days old; the age column says so instead of implying "current".
# Exit 0 = all measured workflows green; 1 = at least one red; 3 = could not measure (gh error/none).
# Always prints its denominator: "N workflows: G green, R red, U unmeasured".
#
# Cost: ~12 gh API calls per run. Benefit: measuring. Review: 2026-12-01. Owner: CIO.
set -u
top="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "main-ci-status: not in a repo" >&2; exit 3; }
repo="${PIPER_GH_REPO:-mediajunkie/piper-morgan-product}"
wfs=()
while IFS= read -r _l; do [ -n "$_l" ] && wfs+=("$_l"); done < <(python3 - "$top/.github/workflows" <<'EOF'
import sys, os, yaml
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith(".yml"):
        continue
    try:
        y = yaml.safe_load(open(os.path.join(d, f)))
    except Exception:
        continue
    on = y.get(True, y.get("on")) if isinstance(y, dict) else None
    ok = False
    if isinstance(on, dict) and "push" in on:
        pv = on["push"] or {}
        br = pv.get("branches") if isinstance(pv, dict) else None
        ok = br is None or "main" in br
    elif on == "push" or (isinstance(on, list) and "push" in on):
        ok = True
    if ok:
        print(f"{f}\t{y.get('name', f)}")
EOF
)
g=0; r=0; u=0
printf '%-30s %-9s %s\n' "workflow" "result" "latest completed run on main"
for line in ${wfs[@]+"${wfs[@]}"}; do
  file="${line%%$'\t'*}"; name="${line#*$'\t'}"
  out=$(gh run list --repo "$repo" --workflow "$file" --branch main --limit 20 \
        --json conclusion,createdAt < /dev/null 2>/dev/null | python3 -c '
import json, sys, datetime as dt
try:
    runs = json.load(sys.stdin)
except Exception:
    print("UNMEASURED gh-error"); sys.exit()
for x in runs:
    if x.get("conclusion") in ("success", "failure"):
        t = dt.datetime.fromisoformat(x["createdAt"].replace("Z", "+00:00"))
        age = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600
        print(x["conclusion"].upper(), x["createdAt"], f"({age:.0f}h ago)")
        break
else:
    print("UNMEASURED no-completed-run-in-last-20")
')
  case "$out" in SUCCESS*) g=$((g+1));; FAILURE*) r=$((r+1));; *) u=$((u+1));; esac
  printf '%-30s %s\n' "$name" "$out"
done
n=${#wfs[@]}
echo "main-ci-status: $n workflows: $g green, $r red, $u unmeasured"
[ "$r" -gt 0 ] && exit 1
[ "$n" -eq 0 ] || [ "$u" -eq "$n" ] && exit 3
exit 0
