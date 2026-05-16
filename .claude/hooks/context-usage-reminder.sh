#!/usr/bin/env bash
# context-usage-reminder.sh — proactive PostToolUse advisory.
#
# Fires once per session at high but pre-limit context usage (~75-85% based on
# transcript byte size). Surfaces a soft, non-blocking advisory: "consider
# /compact at your next natural break — running it now while you still have
# command room means you can stage/commit/push cleanly before compaction starts."
#
# Complement to PreCompact (not replacement):
#   - 90%-reminder (this hook): "compact while you can still act" — proactive, advisory
#   - PreCompact:                "did you?" — reactive backstop
#
# Provenance: Code-agent proposal 2026-05-15 after three week-of-May-12-onward
# incidents (PPM May 10, Lead Dev May 14, CXO May 15) where the PreCompact hook
# correctly surfaced state but the agent had no command-room left to resolve.
# CIO disposition: fits Pattern-069 refinement (Coarse Triggers → runway-aware
# trigger), not a new pattern. HOST stance: runway-awareness is the right shape;
# complement not replacement. Docs implementation 2026-05-15.
#
# Signal: transcript byte size from ~/.claude/projects/{project-hash}/{session-id}.jsonl
# (option 3 from the Code-agent proposal — directly measures the mechanism that
# causes compaction; doesn't require Claude Code to expose token-utilization).
#
# Threshold: 50 MB (conservative initial calibration; tune down based on use).
# False-positive on a healthy verbose-tool-output session is much less costly
# than false-negative on a session that ends up PreCompact-blocked.
#
# Throttle: once per session via marker file in dev/active/.
#
# Exit 0 always — this is advisory; must never block tool execution.

# Resolve repo root; exit silently if not in a git working tree.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi
cd "$REPO_ROOT" || exit 0

# Need the session ID to find the transcript. Claude Code passes it in CLAUDE_SESSION_ID
# env var for PostToolUse hooks. If not present, exit silently — without an ID we can't
# locate the transcript.
SESSION_ID="${CLAUDE_SESSION_ID:-}"
if [ -z "$SESSION_ID" ]; then
    exit 0
fi

# Find the session transcript jsonl. Claude Code stores it under
# ~/.claude/projects/{project-hash}/{session-id}.jsonl
SESSION_LOG=$(find ~/.claude/projects -name "${SESSION_ID}.jsonl" -type f 2>/dev/null | head -1)
if [ -z "$SESSION_LOG" ] || [ ! -f "$SESSION_LOG" ]; then
    exit 0
fi

# Get size in MB (integer; cross-platform stat).
if stat -f%z "$SESSION_LOG" >/dev/null 2>&1; then
    # macOS / BSD
    SIZE_BYTES=$(stat -f%z "$SESSION_LOG" 2>/dev/null)
else
    # Linux / GNU
    SIZE_BYTES=$(stat -c%s "$SESSION_LOG" 2>/dev/null)
fi
[ -z "$SIZE_BYTES" ] && exit 0
SIZE_MB=$(( SIZE_BYTES / 1048576 ))

# Threshold: 50 MB initial conservative calibration.
THRESHOLD_MB=50
if [ "$SIZE_MB" -lt "$THRESHOLD_MB" ]; then
    exit 0
fi

# Throttle: once per session via marker file.
mkdir -p "$REPO_ROOT/dev/active" 2>/dev/null
MARKER="$REPO_ROOT/dev/active/.context-usage-reminded-${SESSION_ID}"
if [ -f "$MARKER" ]; then
    exit 0
fi
touch "$MARKER" 2>/dev/null

# Emit the advisory to stderr (visible to agent; not blocking).
>&2 cat <<EOF

ℹ️  CONTEXT USAGE REMINDER

Session transcript has grown to ${SIZE_MB} MB (threshold ${THRESHOLD_MB} MB).
Consider /compact at your next natural break — running it now while you
still have command room means you can stage / commit / push cleanly
before compaction starts.

The PreCompact hook fires either way; landing there with a clean tree
means a QUIET-tier pass rather than a SOFT/HARD-tier scramble.

This advisory fires once per session.

EOF

exit 0
