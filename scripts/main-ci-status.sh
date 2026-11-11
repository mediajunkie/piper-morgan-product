#!/usr/bin/env bash
# main-ci-status.sh — latest COMPLETED conclusion on main for EVERY workflow that runs on push to main.
#
# Why (2026-10-05, Lead's finding): duty-cycle-tick Step 1e read only lint.yml (Code Quality), so the
# Architecture Enforcement ratchet sat red for 41 consecutive runs (10-01 → 10-05) with nobody looking
# — #1892's shape one workflow over. The list is DERIVED from .github/workflows (push triggers that
# include main), not hardcoded, so a new gating workflow is covered the day it lands.
#
# Per workflow: skips cancelled/skipped runs (a superseded run says nothing about the code) and prints
# the first success/failure among the last 100 main runs, with its age. Path-filtered workflows may be
# days old; the age column says so instead of implying "current".
# Window widened 20 → 100 runs (2026-10-09): e2e-aaxt.yml's live job went nightly (10-06), so its push runs
# finish 'skipped' and 20 of them hid the nightly result, reading UNMEASURED while the nightly was green.
# Stalled queue (2026-11-11, CIO): main queues instead of cancelling (lint.yml/test.yml concurrency, 10-15), so
# one run GitHub never closes holds every later verdict. On 11-11 Code Quality run 43095006321 finished its job
# at 12:18 and stayed in_progress, with 22 runs queued behind it, while this script kept printing the 12:11 red
# as current. Now a run in_progress for over PIPER_CI_STALL_MIN minutes (default 60; the slowest of 100 completed
# runs measured 11-11 took 43 min for Tests, 3 for Code Quality) with runs queued behind it prints STALLED.
# A failed run with no failed job (11-11: Tests 43094045741 ended failure with its one job skipped and Smoke
# never created, a GitHub-side startup fault) is skipped like a cancelled run, and the line names it.
# Costs one gh call per failed run, at most 5 per workflow.
# Exit 0 = all measured workflows green; 1 = at least one red or stalled; 3 = could not measure (gh error/none).
# Always prints its denominator: "N workflows: G green, R red, U unmeasured, S stalled".
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
g=0; r=0; u=0; st=0
printf '%-30s %-9s %s\n' "workflow" "result" "latest completed run on main"
for line in ${wfs[@]+"${wfs[@]}"}; do
  file="${line%%$'\t'*}"; name="${line#*$'\t'}"
  out=$(gh run list --repo "$repo" --workflow "$file" --branch main --limit 100 \
        --json conclusion,createdAt,status,startedAt,databaseId < /dev/null 2>/dev/null | REPO="$repo" STALL_MIN="${PIPER_CI_STALL_MIN:-60}" python3 -c '
import json, os, sys, datetime as dt
try:
    runs = json.load(sys.stdin)
except Exception:
    print("UNMEASURED gh-error"); sys.exit()
now = dt.datetime.now(dt.timezone.utc)
def ts(v):
    return dt.datetime.fromisoformat(v.replace("Z", "+00:00"))
queued = sum(1 for x in runs if x.get("status") in ("queued", "waiting", "pending"))
stall = ""
for x in runs:
    if x.get("status") == "in_progress" and x.get("startedAt") and queued:
        mins = (now - ts(x["startedAt"])).total_seconds() / 60
        if mins > float(os.environ.get("STALL_MIN", "60")):
            rid = x.get("databaseId")
            stall = f" STALLED: run {rid} in_progress {mins:.0f} min, {queued} queued behind it"
            break
import subprocess
def no_job_failed(rid):
    # A failure with no failed job (jobs never created, or all skipped) is GitHub-side, not a code result.
    try:
        r = subprocess.run(["gh", "run", "view", str(rid), "--repo", os.environ["REPO"], "--json", "jobs",
                            "--jq", "[.jobs[]|select(.conclusion==\"failure\")]|length"],
                           capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        return r.returncode == 0 and r.stdout.strip() == "0"
    except Exception:
        return False
skipped_nojob = []
for x in runs:
    if x.get("conclusion") in ("success", "failure"):
        if x["conclusion"] == "failure" and len(skipped_nojob) < 5 and no_job_failed(x.get("databaseId")):
            skipped_nojob.append(str(x.get("databaseId")))
            continue
        t = dt.datetime.fromisoformat(x["createdAt"].replace("Z", "+00:00"))
        age = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600
        note = f" (skipped {len(skipped_nojob)} failed run(s) with no failed job: {chr(44).join(skipped_nojob)})" if skipped_nojob else ""
        print(x["conclusion"].upper(), x["createdAt"], f"({age:.0f}h ago)" + note + stall)
        break
else:
    print("UNMEASURED no-completed-run-in-last-100" + stall)
')
  case "$out" in SUCCESS*) g=$((g+1));; FAILURE*) r=$((r+1));; *) u=$((u+1));; esac
  case "$out" in *STALLED*) st=$((st+1));; esac
  printf '%-30s %s\n' "$name" "$out"
done
n=${#wfs[@]}
echo "main-ci-status: $n workflows: $g green, $r red, $u unmeasured, $st stalled"
[ "$r" -gt 0 ] || [ "$st" -gt 0 ] && exit 1
[ "$n" -eq 0 ] || [ "$u" -eq "$n" ] && exit 3
exit 0
