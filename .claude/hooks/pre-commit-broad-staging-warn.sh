#!/usr/bin/env bash
# pre-commit-broad-staging-warn.sh — PreToolUse hook for `git commit*`
#
# Detects cross-agent sweeps in the staged set. When a commit would touch
# multiple distinct mailbox role directories simultaneously, that's almost
# always evidence that the shared git index captured neighboring agents'
# unstaged work via the staging race (Pattern-068 family / Commit-Attribution
# Drift). Warn the agent before they commit so they can re-stage cleanly.
#
# Trigger thresholds:
#   - Staged set touches >= 3 distinct mailbox role directories — sweep signal
#   - Staged set touches >= 20 total files — mass-staging signal
#   - Staged set touches multiple distinct dev/active/*-{role}-* session logs
#     where files don't share a role slug — cross-agent log capture signal
#
# ⚠️ RULED 2026-09-13: WARN, NOT BLOCK. Two open questions closed here — a false documented
# escape hatch, and a behavioral decision that sat unanswered from 2026-08-03 to 2026-09-13
# (five weeks; HOST found and owned the silent gap).
#
# THE RULING (Arch's input, HOST's trust/safety concurrence, reasons 1+2 only — Arch withdrew
# a third reason after HOST caught it conflating two unrelated incidents by timestamp):
#   1. The header's OWN ORIGINAL INTENT (below) was always warn-only — block was never a
#      decided behavior, it was an undecided default that trapped a real case.
#   2. The 2026-09-12 incident (#1768) is the argument: delete-module-safely's same-commit
#      coherence discipline REQUIRES >=20 paths in one commit on exactly the commits where
#      coherence matters most (ruled deletions: exemption removal + ratchet ceiling + a
#      decisions.log entry, same commit, by design). An unconditional block put two of this
#      project's own ratified disciplines in direct conflict. The workaround (a 2-commit split
#      at a both-tips-green seam) was safe, but it existed only because a guard forced it.
#
# THE FALSE ESCAPE, REMOVED: this file used to tell the agent to "re-run with --no-verify" on
# block. That could never have worked, for a sharper reason than mistiming: `--no-verify` is a
# GIT-NATIVE flag that tells git to skip git's OWN `.git/hooks/*` chain. It has zero
# relationship to Claude Code's PreToolUse hook layer, which intercepts the tool call before
# git ever runs. No timing fix could have made it work — it was a category error, not a
# mistimed check (Lead found the hook fires before Bash runs; CIO's sharper read: the flag and
# the mechanism it claimed to escape don't share a layer at all).
#
# EXIT SEMANTICS, now decided: exit 0 (warn). The commit proceeds; the agent reads the warning
# and can inspect/restage if needed. With WARN, no escape hatch is needed at all — nothing
# needs escaping from a warning. (If a future ruling reverses this to BLOCK: a real escape IS
# buildable, unlike --no-verify — PreToolUse hooks receive the tool call's JSON payload on
# stdin, including the command text, the same mechanism `memory-index-overlimit-warn.sh`
# already uses to read `tool_input.file_path`. A real marker in the command text, visible to a
# reviewer in the commit rather than an invisible env var per Lead's condition, would work.)
#
# ⚠️ WORKTREE NOTE, found verifying this fix (2026-09-13): editing this file in an agent's own
# worktree has ZERO effect on live hook behavior. Claude Code resolves `.claude/hooks/*.sh`
# (registered via `.claude/settings.json`'s PreToolUse config) against a fixed canonical path
# — the main checkout — regardless of which worktree the active session is running in.
# Confirmed behaviorally: editing this exact file's exit code in a worktree copy, then
# triggering the hook from that same worktree, still ran the main checkout's unmodified
# version. A push to origin/main does NOT make a hook fix live — `scripts/sync-pm-local.sh`
# (or an equivalent pull in the main checkout) is also required. This is worth knowing before
# assuming any hook fix is "shipped" once it's on origin/main.
#
# History: found by Docs on 2026-08-03 during a 23-file archival sweep (blocked, split into 4
# batches; diagnosed by Comms). The 08-03 fix corrected only the FALSE STATEMENT that block
# didn't block — it deliberately left the actual block-vs-warn behavior undecided, "raised to
# PM/HOST," and that sat for five weeks until Lead's unrelated #1768 workaround surfaced it
# again on 2026-09-13.
#
# Rationale: B (worktree-per-agent for main) is the structural fix PM ratified
# via PPM May 15. This hook is the D-layer safety net for the residual
# mail-on-main pattern (agents writing quick mail from shared main without
# spinning up a worktree). Warn-only because false-positives on legitimate
# multi-mailbox commits (e.g., to-with-cc-copies) would be high-friction;
# the warning prompts the agent to inspect rather than blocking outright.

# Resolve repo root; if we're not in a git working tree, exit silently.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi
cd "$REPO_ROOT" || exit 0

# Index state: list staged file paths.
STAGED=$(git diff --cached --name-only 2>/dev/null)

# Empty index → nothing to check (commit will fail on its own with no message).
if [ -z "$STAGED" ]; then
    exit 0
fi

# Total file count.
TOTAL_COUNT=$(printf '%s\n' "$STAGED" | grep -c '.')

# Distinct mailbox roles touched. Pattern: mailboxes/<role>/...
MAILBOX_ROLES=$(printf '%s\n' "$STAGED" \
    | grep -E '^mailboxes/' \
    | awk -F/ '{print $2}' \
    | sort -u)
MAILBOX_ROLE_COUNT=$(printf '%s\n' "$MAILBOX_ROLES" | grep -c '.' || true)
[ -z "$MAILBOX_ROLES" ] && MAILBOX_ROLE_COUNT=0

# Distinct session-log role slugs in staged set.
# dev/active/YYYY-MM-DD-HHMM-{role}-code-opus-log.md OR dev/YYYY/MM/DD/<same>
LOG_ROLES=$(printf '%s\n' "$STAGED" \
    | grep -E '/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}-[a-z-]+-code-opus-log\.md$' \
    | sed -E 's|.*/[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}-([a-z-]+)-code-opus-log\.md$|\1|' \
    | sort -u)
LOG_ROLE_COUNT=$(printf '%s\n' "$LOG_ROLES" | grep -c '.' || true)
[ -z "$LOG_ROLES" ] && LOG_ROLE_COUNT=0

# Threshold checks.
SWEEP_MAILBOX=$([ "$MAILBOX_ROLE_COUNT" -ge 3 ] && echo 1 || echo 0)
SWEEP_MASS=$([ "$TOTAL_COUNT" -ge 20 ] && echo 1 || echo 0)
SWEEP_LOGS=$([ "$LOG_ROLE_COUNT" -ge 2 ] && echo 1 || echo 0)

if [ "$SWEEP_MAILBOX" = "0" ] && [ "$SWEEP_MASS" = "0" ] && [ "$SWEEP_LOGS" = "0" ]; then
    exit 0  # All clear.
fi

# Build the warning message.
{
    echo "⚠️  BROAD-STAGING WARNING (PreCommit) — sweep signal in staged set"
    echo ""
    echo "Your staged commit looks like it may have captured neighboring agents' work"
    echo "via the shared git index. This is Pattern-068 family (Commit-Attribution Drift)."
    echo ""
    echo "Signals triggered:"
    if [ "$SWEEP_MAILBOX" = "1" ]; then
        echo "  • Touches $MAILBOX_ROLE_COUNT distinct mailbox roles:"
        printf '%s\n' "$MAILBOX_ROLES" | sed 's/^/      - /'
    fi
    if [ "$SWEEP_MASS" = "1" ]; then
        echo "  • Staged set has $TOTAL_COUNT total files (mass-staging signal)"
    fi
    if [ "$SWEEP_LOGS" = "1" ]; then
        echo "  • Staged set touches session logs from $LOG_ROLE_COUNT distinct roles:"
        printf '%s\n' "$LOG_ROLES" | sed 's/^/      - /'
    fi
    echo ""
    echo "Before proceeding:"
    echo "  1. Inspect: git diff --cached --name-only"
    echo "  2. If foreign files are present: git restore --staged <path>"
    echo "  3. Re-stage only your own files with explicit paths"
    echo "  4. Verify with: git diff --cached --name-only | head -20"
    echo ""
    echo "This is a WARNING, not a block (ruled 2026-09-13; see this file's own header for"
    echo "why) — the commit has not yet happened but WILL proceed immediately after this"
    echo "message unless you interrupt the tool call. If the staged set is intentional (e.g."
    echo "a legitimate large multi-mailbox distribution), no action is needed. If it looks"
    echo "wrong, stop before letting the commit run and restage explicit paths instead."
    echo ""
    echo "Root-cause fix (PM ratified May 15): worktree-per-agent for substantive"
    echo "work. See CLAUDE.md §Branch / Worktree / Mailbox Discipline."
} >&2

# Append to session-end log for the Docs merge-keeper sweep visibility.
WARN_LOG="dev/active/session-end-warnings.log"
if [ -d "dev/active" ]; then
    {
        echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] pre-commit-broad-staging-warn fired"
        echo "  total_count=$TOTAL_COUNT mailbox_roles=$MAILBOX_ROLE_COUNT log_roles=$LOG_ROLE_COUNT"
    } >> "$WARN_LOG" 2>/dev/null || true
fi

# Exit 0 = WARN, per the 2026-09-13 ruling (this file's header). Do not revert this to exit 2
# without re-litigating the ruling above, not just this line.
exit 0
