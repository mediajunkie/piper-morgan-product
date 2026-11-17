#!/usr/bin/env bash
# whats-armed.sh — one probe of what is actually armed on this host, with the layer each check
# measures and a denominator. Agent 360 v0.5 candidate 2 (CIO's 9.2, "name a mechanism you believe
# is running, and say how you last verified it"); xian "on board" 2026-10-13 via HOST.
#
# Replaces asking eleven seats to each probe a hook. Run it from any worktree; read-only except for
# the guards' own temp files. It never runs a git or fly command on your behalf.
#
# Layers, named per line (m-43):
#   live   — Claude Code itself ran the hook (only Pard's verify-hooks drumbeat measures this)
#   script — the hook script, run directly with a synthetic tool payload, gave the expected exit code
#   file   — present, executable, matches its tracked source; nothing was run
#   state  — a process or store reports itself (launchctl, the heartbeat store)
#
# Exit 0 = nothing NOT ARMED; 1 = at least one NOT ARMED. Unmeasured lines don't fail the run.
# Concept: docs/internal/operations/whats-armed.md. Owner: CIO. Review: 2026-12-08.
set -u
top="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "whats-armed: not in a git repo" >&2; exit 2; }
common="$(git -C "$top" rev-parse --git-common-dir)"
cd "$top" || exit 2
armed=0; not=0; unm=0
row() { # row <ARMED|NOT ARMED|UNMEASURED> <layer> <what> <detail>
  case "$1" in ARMED) armed=$((armed+1));; "NOT ARMED") not=$((not+1));; *) unm=$((unm+1));; esac
  printf '%-10s %-6s %-34s %s\n' "$1" "$2" "$3" "$4"
}
payload() { # payload <bash command> -> Claude Code PreToolUse JSON on stdout
  python3 -c 'import json,sys; print(json.dumps({"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":sys.argv[1]},"cwd":sys.argv[2]}))' "$1" "$top"
}
expect() { # expect <hook> <command> <want: allow|block> -> 0 if the exit code matched
  local rc; payload "$2" | bash ".claude/hooks/$1" >/dev/null 2>&1; rc=$?
  if [ "$3" = allow ]; then [ $rc -eq 0 ]; else [ $rc -ne 0 ]; fi
}

echo "whats-armed: $(hostname -s) $(TZ=America/Los_Angeles date '+%Y-%m-%d %H:%M %Z') worktree=$(basename "$top")"

# 1. Live layer: Pard's drumbeat runs claude -p and checks a commit is blocked by check-branch.
dlog="$HOME/Development/mediajunkie/logs/verify-hooks-drumbeat.log"
if [ -r "$dlog" ]; then
  last=$(tail -1 "$dlog"); verdict=$(printf '%s' "$last" | cut -f2); when=$(printf '%s' "$last" | cut -f1)
  if [ "$verdict" = PASS ]; then row ARMED live "check-branch.sh (drumbeat)" "last PASS $when"
  else row "NOT ARMED" live "check-branch.sh (drumbeat)" "last $verdict $when"; fi
else row UNMEASURED live "check-branch.sh (drumbeat)" "no drumbeat log at $dlog"; fi

# 2. Script layer: each PreToolUse guard with one benign and one should-refuse payload.
pm="$HOME/Development/piper-morgan-product"
g() { # g <hook> <benign cmd> <refuse cmd>
  local h="$1"
  [ -f ".claude/hooks/$h" ] || { row "NOT ARMED" file "$h" "missing"; return; }
  if ! expect "$h" "$2" allow; then row "NOT ARMED" script "$h" "refused a benign command: $2"
  elif [ -n "$3" ] && ! expect "$h" "$3" block; then row "NOT ARMED" script "$h" "allowed: $3"
  else row ARMED script "$h" "allows benign${3:+, refuses: $3}"; fi
}
g guard-pm-checkout.sh "git status" "cd $pm && git reset --hard"
g guard-browser-launch.sh "echo hi" "/nonexistent-dir/chromium --version"
g autoclose-guard.sh "echo hi" "git commit -m 'fix #1'"
g check-branch.sh "echo hi" ""
g pre-commit-reconcile-drafts.sh "echo hi" ""
for h in log-maintenance-reminder.sh issue-checkbox-lint.sh memory-index-overlimit-warn.sh session-start.sh; do
  if [ -f ".claude/hooks/$h" ] && bash -n ".claude/hooks/$h" 2>/dev/null; then row ARMED file "$h" "present, parses (not run: side effects)"
  else row "NOT ARMED" file "$h" "missing or does not parse"; fi
done

# 3. File layer: shared git hooks match their tracked source.
for h in pre-commit pre-push commit-msg post-commit; do
  inst="$common/hooks/$h"; src="scripts/git-hooks/$h"
  if [ ! -e "$inst" ]; then
    if [ -e "$src" ]; then row "NOT ARMED" file "git hook $h" "source exists, not installed"; else row UNMEASURED file "git hook $h" "no source, not installed"; fi
  elif [ ! -x "$inst" ]; then row "NOT ARMED" file "git hook $h" "installed but not executable"
  elif [ -e "$src" ] && ! cmp -s "$inst" "$src"; then row "NOT ARMED" file "git hook $h" "installed copy differs from $src"
  else row ARMED file "git hook $h" "installed${src:+, matches source}"; fi
done
if [ -f "$common/piper-old-history-sentinels" ]; then row ARMED file "old-history guard" "sentinel file present ($(grep -vc '^#' "$common/piper-old-history-sentinels") lines)"
else row UNMEASURED file "old-history guard" "dormant: no sentinel file (normal outside a rewrite)"; fi

# 4. State layer: LaunchAgents for the PM cohort and the heartbeat store.
la=$(launchctl list 2>/dev/null | awk '$3 ~ /^com\.xian\.(pm-.*-cycle|mail-wake|usage-capture|verify-hooks-drumbeat)$/ {print $3, $2}')
if [ -z "$la" ]; then row UNMEASURED state "LaunchAgents" "launchctl shows none (not Amber?)"
else
  while read -r name code; do
    if [ "$code" = 0 ]; then row ARMED state "$name" "loaded, last exit 0"; else row "NOT ARMED" state "$name" "loaded, last exit $code"; fi
  done <<< "$la"
fi
store="${PIPER_HB_STORE:-$HOME/.local/state/piper-heartbeats}"
if [ -d "$store" ] && [ -w "$store" ]; then
  newest=$(ls -t "$store" 2>/dev/null | head -1)
  row ARMED state "heartbeat store" "writable; newest file ${newest:-none}"
else row "NOT ARMED" state "heartbeat store" "missing or not writable: $store"; fi
# The fleet's Read denies on ~/.piper-shared match names only (*credential*, *token*, *secret*), so a
# credential file named any other way is readable by every seat (2026-10-15: 6 found, 2 renamed that day). Counts
# only: a file name can carry a person's name (hard rule 8), and this output gets pasted into logs.
shared="${PIPER_SHARED:-$HOME/.piper-shared}"
if [ -d "$shared" ]; then
  total=0; open=0
  for f in "$shared"/*; do
    [ -f "$f" ] || continue
    total=$((total+1))
    case "${f##*/}" in *credential*|*token*|*secret*) ;; *) open=$((open+1)) ;; esac
  done
  if [ $open -eq 0 ]; then row ARMED file "piper-shared names under a deny" "$total of $total files match *credential*/*token*/*secret*"
  else row "NOT ARMED" file "piper-shared names under a deny" "$open of $total files match no deny pattern (rename to *credential*; names not printed)"; fi
else row UNMEASURED file "piper-shared names under a deny" "no $shared"; fi

# 5. File layer: pinned tools this worktree can resolve.
r=$(scripts/ensure-ruff.sh 2>/dev/null | tail -1)
if [ -n "$r" ] && [ -x "$r" ]; then row ARMED file "ruff (ensure-ruff.sh)" "$r"; else row "NOT ARMED" file "ruff (ensure-ruff.sh)" "did not resolve"; fi
p=$(scripts/ensure-pytest-env.sh 2>/dev/null | tail -1)
if [ -n "$p" ] && [ -x "$p" ]; then row ARMED file "pytest env (ensure-pytest-env.sh)" "$p"; else row "NOT ARMED" file "pytest env (ensure-pytest-env.sh)" "did not resolve (pre-push smoke runs unchecked)"; fi

echo "whats-armed: $((armed+not+unm)) checks: $armed armed, $not NOT ARMED, $unm unmeasured"
[ $not -eq 0 ]
