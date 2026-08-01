#!/usr/bin/env bash
# memory-index-overlimit-warn.sh — PostToolUse hook for Edit|Write|MultiEdit
#
# Closes the one unguarded path to a silently-truncated shared memory index.
#
# THE GAP THIS EXISTS FOR (CIO's correction, 2026-07-31):
#
#   path                              at >=200 lines / >=24KB
#   --------------------------------  ------------------------------
#   rebuild-memory-index.py           LOUD refusal (SystemExit)  ✅ already guarded
#   direct Edit/Write of MEMORY.md    SUCCEEDS SILENTLY          ⚠️ THIS HOOK
#
# The guard was on the GENERATOR. The platform's built-in reminder says
# "compact this file" — an instruction to edit the ARTIFACT, not to re-run the
# generator. So the pressure points squarely at the unguarded path, and the
# only thing that has stopped it is four agents in a row declining on judgment
# (PA 07-26, CXO 07-29, Comms 07-30, HOST twice 07-30). That is the absence of
# a safety property, not one.
#
# Both limits were tested SILENT on Claude Code 2.1.220 despite the v2.1.210
# changelog claiming over-limit writes now error (lines: HOST; bytes: PA).
# Do not re-test; do not trust the changelog here.
#
# EXIT SEMANTICS: exit 0 always. This is a PostToolUse hook — the write has
# already happened, so blocking is meaningless; the job is to make the silent
# state LOUD in the same turn, before the agent moves on believing it complied.
# Warn-only is also correct because a legitimate over-limit intermediate state
# exists (editing the header before regenerating).
#
# Written by HOST 2026-07-31. Registration is CIO/Pard's surface.
# ⚠️ Testing this script by invoking it is NOT testing that it fires.
#    An absent hook and a silent hook are indistinguishable from inside a
#    session — verify behaviorally after registration.

set -uo pipefail

MEM="/Users/xian/.claude-pm/projects/-Users-xian-Development-piper-morgan-product/memory/MEMORY.md"
LINE_LIMIT=200
BYTE_LIMIT=24000
WARN_AT=90   # percent

payload="$(cat 2>/dev/null || true)"

# Only care about writes that touched the shared index. Cheap string test —
# the file path is unambiguous and appears in tool_input.file_path.
case "$payload" in
  *"memory/MEMORY.md"*) ;;
  *) exit 0 ;;
esac

[ -f "$MEM" ] || exit 0

# Convention: `wc -l`. rebuild-memory-index.py's guard counts ONE HIGHER (trailing
# newline), so it refuses one line earlier than this warns. Deliberate on both sides —
# the guard is conservative, this reports what you would measure by hand. Stated
# because two numbers for one file is how an afternoon disappears. (Comms, 2026-07-31.)
lines=$(wc -l < "$MEM" | tr -d ' ')
bytes=$(wc -c < "$MEM" | tr -d ' ')
entries=$(grep -c '^- ' "$MEM" 2>/dev/null || echo 0)

line_pct=$(( lines * 100 / LINE_LIMIT ))
byte_pct=$(( bytes * 100 / BYTE_LIMIT ))

over=0
[ "$lines" -ge "$LINE_LIMIT" ] && over=1
[ "$bytes" -ge "$BYTE_LIMIT" ] && over=1

if [ "$over" = "1" ]; then
  cat <<EOF
🛑 MEMORY.md IS NOW OVER A READ LIMIT AND IS TRUNCATING SILENTLY FOR EVERY AGENT.

   lines ${lines}/${LINE_LIMIT}   bytes ${bytes}/${BYTE_LIMIT}   entries ${entries}

Trailing entries are no longer reaching anyone's context, with no error anywhere.
The 'reference' bucket goes first by section order. This state persists until the
next regeneration.

DO NOT fix this by deleting memories. The index is a GENERATED artifact; the
memory files are the SOURCE. Pruning source to shrink a build output is a
category error, memory is NOT under version control, and the shared pool is the
whole cohort's. A compaction target below the entry count (${entries}) is
unreachable by editing no matter how short the text.

DO: run  python3 scripts/rebuild-memory-index.py
    It refuses to write an oversized index, so it will tell you loudly and
    correctly what this hook can only warn about.
    If it refuses, escalate to CIO/HOST — that is a format decision about
    shared state, not a formatting chore for whoever tripped the limit.

Context: docs/internal/operations/memory-index-size-limits.md
EOF
  exit 0
fi

if [ "$line_pct" -ge "$WARN_AT" ] || [ "$byte_pct" -ge "$WARN_AT" ]; then
  echo "⚠️  MEMORY.md at ${line_pct}% of the line limit (${lines}/${LINE_LIMIT}), ${byte_pct}% of bytes (${bytes}/${BYTE_LIMIT}), ${entries} entries."
  echo "   One entry = one line, so the floor is ${entries} lines. Do not delete memories to fit; see docs/internal/operations/memory-index-size-limits.md."
fi

exit 0
