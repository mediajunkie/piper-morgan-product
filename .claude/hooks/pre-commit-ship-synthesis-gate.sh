#!/usr/bin/env bash
# pre-commit-ship-synthesis-gate.sh — PreToolUse hook for `git commit*`
#
# Blocks a commit that ADDS a new Weekly Ship draft (docs/public/comms/drafts/weekly-ship-NNN-draft-*.md)
# unless (each read from the index or, for a file the same command stages, the disk):
#   1. that Ship's synthesis exists: docs/internal/planning/comms/ship-reviews/ship-NNN-week-review.html
#   2. it carries xian's discussed marker: <!-- discussed: YYYY-MM-DD -->
#   3. the editorial calendar has a row whose draftPath names the new draft
#
# Why: the draft-weekly-ship skill's Step 2c (synthesis for xian, discussed before any draft) was skipped
# for #054 and again for #066 (2026-10-23), both times by an Exec working from habit, not the skill. A rule
# in prose was read past twice; this makes the shortcut fail at the commit with the reason and the fix.
# xian approved the two-part fix 2026-10-23 (this gate plus the status line in scripts/ship-kickoff.sh).
# Check 3 was added by CIO's review the same day: the #066 draft's missing calendar row was warned about
# by pre-commit-reconcile-drafts.sh (warn-only, whole-repo) and went unnoticed.
#
# Only added (or renamed-in) drafts are checked, so edits to an existing draft (Comms, xian's admin
# saves) pass. The time-of-check split applies (hooks-registry.md): a PreToolUse hook reads the index
# before the command runs, so for a compound `git add … && git commit` it also treats an untracked new
# draft named in the command as added. Not covered: commits made outside Claude Code (no PreToolUse).
#
# Exit 0 = allowed. Exit 2 = blocked, reason and fix on stderr.
# Cost:    one `git diff --cached` per commit; nothing more unless a new Ship draft is staged.
# Benefit: none yet: measuring (added 2026-10-23; would have refused #054's and #066's drafts).
# Review:  2026-12-04
# Owner:   CIO (mechanism); Exec (the Ship process it guards)
# Concept: .claude/skills/draft-weekly-ship/SKILL.md

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$REPO_ROOT" || exit 0

DRAFT_RE='^docs/public/comms/drafts/weekly-ship-[0-9]{3}-draft-.*\.md$'
SYN_DIR=docs/internal/planning/comms/ship-reviews
CAL=docs/internal/planning/comms/editorial-calendar.csv

ADDED=$(git diff --cached --name-only --diff-filter=AR 2>/dev/null | grep -E "$DRAFT_RE")

# Compound form: an untracked new draft whose path appears in the command about to run.
CMD=$(python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("tool_input",{}).get("command",""))
except Exception: pass' 2>/dev/null)
# 11-06 (Exec's report, CIO's probes): settings.json's `"if": "Bash(git commit*)"` fails open when Claude Code
# can't parse a command (a heredoc with nested quotes), so this hook ran on Exec's python edit that was adding
# the calendar row, and blocked it. check-branch.sh has had the same guard since #2251. With no command
# readable (a hand run), fall through to the index check as before.
if [ -n "$CMD" ] && ! printf '%s' "$CMD" | grep -qE '(^|[^[:alnum:]_-])git([[:space:]]+-[^[:space:]]+([[:space:]]+[^-[:space:]][^[:space:]]*)?)*[[:space:]]+commit([[:space:]]|$)'; then
  exit 0
fi
if [ -n "$CMD" ]; then
  while IFS= read -r u; do
    [ -n "$u" ] && case "$CMD" in *"$(basename "$u")"*|*"docs/public/comms/drafts"*) ADDED="$ADDED
$u" ;; esac
  done <<< "$(git ls-files --others --exclude-standard -- docs/public/comms/drafts/ 2>/dev/null | grep -E "$DRAFT_RE")"
fi
ADDED=$(printf '%s\n' "$ADDED" | grep -E "$DRAFT_RE" | sort -u)
[ -z "$ADDED" ] && exit 0

# A path's text in the index and on disk: either one passing counts, so a compound command that stages
# the synthesis or calendar row alongside the draft isn't refused for an index that isn't staged yet.
staged_or_disk() { git show ":$1" 2>/dev/null; cat "$1" 2>/dev/null; }

STATUS=0
while IFS= read -r f; do
  n=$(basename "$f" | sed -E 's/^weekly-ship-([0-9]{3})-draft-.*/\1/')
  syn="$SYN_DIR/ship-${n}-week-review.html"
  body=$(staged_or_disk "$syn")
  if [ -z "$body" ]; then
    echo "BLOCKED: $f adds Ship #${n}'s draft, but its synthesis ($syn) isn't in the repo." >&2
    echo "  Invoke the draft-weekly-ship skill at Step 2c: the synthesis for xian first, then his discussion, then the draft." >&2
    STATUS=2
  elif ! printf '%s' "$body" | grep -qE '<!-- discussed: [0-9]{4}-[0-9]{2}-[0-9]{2} -->'; then
    echo "BLOCKED: Ship #${n}'s synthesis exists but has no '<!-- discussed: YYYY-MM-DD -->' marker." >&2
    echo "  The draft follows xian's discussion of the synthesis. Add the marker the day he discusses it." >&2
    STATUS=2
  fi
  if ! staged_or_disk "$CAL" | grep -qF "$(basename "$f")"; then
    echo "BLOCKED: $f has no row in $CAL naming it in draftPath." >&2
    echo "  Add or update Ship #${n}'s calendar row (draftPath = the draft's path) in the same commit." >&2
    STATUS=2
  fi
done <<< "$ADDED"
exit $STATUS
