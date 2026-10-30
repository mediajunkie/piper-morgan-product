#!/usr/bin/env bash
# session_trailers.sh — print this session's commit attribution trailers, derived, never typed.
#
# Why (xian 10-30 via Exec, "without having to remember"): a cross-repo memo went out with no trailer
# because the trailer was a thing to remember. mail-send.sh and mail-send-external.sh append this output
# to their commits. Same derivation as Pard's mediajunkie scripts/mail-deliver.sh, so both agree:
#   Co-Authored-By  the model this session's transcript ran most in its last 400 lines
#   Claude-Session  https://claude.ai/code/$CLAUDE_CODE_BRIDGE_SESSION_ID
# A trailer that can't be derived is left off with a warning on stderr, never guessed. Exit is always 0.
#
# Cost:    one transcript tail per commit
# Benefit: every mail commit carries the attribution with nobody typing it
# Review:  2026-12-14
# Owner:   CIO
# Concept: mailboxes/DIRECTORY.md
set -uo pipefail
out=""
tx="$(ls "$HOME"/.claude*/projects/*/"${CLAUDE_CODE_SESSION_ID:-none}".jsonl 2>/dev/null | head -1)"
mid=""
[ -n "$tx" ] && mid="$(tail -400 "$tx" | grep -oE '"model":"claude-[a-z]+-[0-9-]+"' | sort | uniq -c | sort -rn \
  | head -1 | sed -E 's/.*"model":"([^"]+)"/\1/')"
if [ -n "$mid" ]; then
  pretty="$(sed -E 's/^claude-([a-z]+)-([0-9]+)-?([0-9]*)$/\1 \2.\3/; s/\.$//' <<<"$mid")"
  out="Co-Authored-By: Claude $(tr '[:lower:]' '[:upper:]' <<<"${pretty:0:1}")${pretty:1} <noreply@anthropic.com>"
else
  echo "session_trailers: WARN no session model found; Co-Authored-By left off (not guessed)" >&2
fi
if [ -n "${CLAUDE_CODE_BRIDGE_SESSION_ID:-}" ]; then
  out="${out:+$out
}Claude-Session: https://claude.ai/code/$CLAUDE_CODE_BRIDGE_SESSION_ID"
else
  echo "session_trailers: WARN no CLAUDE_CODE_BRIDGE_SESSION_ID; Claude-Session left off (not guessed)" >&2
fi
[ -n "$out" ] && printf '%s\n' "$out"
exit 0
