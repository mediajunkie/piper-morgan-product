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
# Exit 2 = warn (stderr surfaces to agent; commit not blocked)
# Exit 0 = pass
#
# Rationale: B (worktree-per-agent for main) is the structural fix PM ratified
# via PPM May 15. This hook is the D-layer safety net for the residual
# mail-on-main pattern (agents writing quick mail from shared main without
# spinning up a worktree). Warn-only because false-positives on legitimate
# multi-mailbox commits (e.g., to-with-cc-copies) would be high-friction;
# the warning prompts the agent to inspect rather than blocking outright.
#
# Aligns with existing hook patterns: precompact-signoff-warning.sh severity
# tiering + check-branch.sh exit-2-stderr convention.

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
    echo "If the staged set is intentional (e.g., legitimate large multi-mailbox"
    echo "distribution), proceed. The warning is informational; commit is not"
    echo "blocked. Use --no-verify to skip future warnings on this commit."
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

# Exit 2 = warning, commit proceeds (matches precompact-signoff-warning.sh
# convention). Block (exit 1) would be too high-friction for false positives.
exit 2
