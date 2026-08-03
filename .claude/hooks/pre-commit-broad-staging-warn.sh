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
# ⚠️ CORRECTED 2026-08-03. This block used to read "Exit 2 = warn (stderr surfaces to agent;
# commit not blocked)". THAT IS FALSE FOR THIS HOOK. **This is a PreToolUse hook, and in
# PreToolUse `exit 2` BLOCKS** — stderr reaches the model and the tool call does not run.
#
# How the error got here, because it is instructive: the rationale below cites
# `precompact-signoff-warning.sh` as the convention being matched — but that hook is a
# **PreCompact** hook, where the exit codes mean something different. **The exit code was
# borrowed across an event boundary on which its meaning inverts.** (That hook has since
# moved to exit 0 anyway, so the cited convention no longer exists even at its source.)
#
# Found by Docs on 2026-08-03 during a 23-file archival sweep — it was blocked and had to
# split into 4 batches. Verified and diagnosed by Comms rather than relayed.
#
# ⚠️ BEHAVIOUR AND INTENT STILL DISAGREE. The intent, stated three times in this file, is
# "warn, do not block" ("Block would be too high-friction"). The behaviour blocks. This fix
# corrects only the FALSE STATEMENTS, so the hook no longer asserts the opposite of what it
# does. **Whether the exit code should change to 0 is NOT fixed here** — that turns on
# whether stderr still reaches the agent on exit 0 in PreToolUse, which I have not tested.
# Shipping an untested behaviour change to a cohort-wide gate is the failure mode this
# codebase has spent a fortnight cataloguing. Raised to PM/HOST for a behavioural decision.
#
# Exit 2 = BLOCKS the commit (PreToolUse semantics), stderr surfaces to the agent
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
    echo "⚠️ THIS COMMIT WAS BLOCKED. (Until 2026-08-03 this message claimed the opposite —"
    echo "if you have seen that text, the commit did not run.) If the staged set is"
    echo "intentional (e.g. a legitimate large multi-mailbox distribution), re-run with"
    echo "--no-verify, or split it into smaller explicit-path commits."
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

# ⚠️ Exit 2 in PreToolUse BLOCKS. The comment here used to claim "commit proceeds" and cited
# precompact-signoff-warning.sh — a PreCompact hook, different event, different semantics, and
# since changed to exit 0 itself. Left as exit 2 deliberately pending a behavioural test of
# whether exit 0 still surfaces stderr in PreToolUse; see the header note.
exit 2
