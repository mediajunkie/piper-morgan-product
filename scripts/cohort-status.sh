#!/usr/bin/env bash
# cohort-status.sh v1.0 — one instrument for "where does the cohort stand?"
# CIO 2026-07-29, at PM's request, after four report-without-checking lapses in one morning.
#
# WHY THIS EXISTS
# Every one of those lapses had the same mechanism, and none of them was carelessness:
#   1. "comms has closed"        — `grep -c DAY-CLOSED` counted two references to YESTERDAY's marker.
#   2. "predecessors produced nothing" — `--grep='(ppm)'` matches SUBJECT TAGS only, and the snapshot
#                                  was minutes stale; both handoffs landed at 09:42/09:46.
#   3. "10 of 10, the cohort is on Amber" — counted tmux SESSIONS as if they were the ROSTER. The
#                                  roster is 11. Said in the same breath as "exec is the last migration."
#   4. the mail-atrophy audit itself — `grep -c … || echo 0` emitted "0\n0"; the identical bug I had
#                                  fixed in freeze-check ~24h earlier.
#
# The common vector is NOT inattention. It is that each status claim was produced by a ONE-OFF QUERY
# hand-written at the moment of reporting, whose SCOPE was invisible in its own output. A number
# appeared, and the number got reported. `10` looks the same whether it counted the right set or not.
#
# So the fix cannot be "check more carefully" (m-36: mechanisms over vigilance). It has to be:
#   (a) stop hand-rolling the query — one instrument, reused, so bugs get fixed ONCE; and
#   (b) make every number carry its denominator and its provenance, so a wrong scope is VISIBLE
#       in the output rather than inferable only by someone who already knows the answer.
#
# THE DESIGN RULE THAT MATTERS MOST — when sources disagree, SAY SO; never silently pick one.
# Building this found that ROSTER.md omits `web`, while the duty-cycle registry, the mailboxes and
# the briefings all include it. A tool that quietly chose one source would have produced a confident
# wrong roster — exactly failure #3 again, one level down, inside the fix for it.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || { echo "cohort-status: not in a git repo" >&2; exit 2; }

FETCH="${COHORT_STATUS_FETCH:-yes}"
[ "$FETCH" = "yes" ] && git fetch origin main -q 2>/dev/null

TIP=$(git log origin/main -1 --format='%h' 2>/dev/null)
TIPTS=$(git log origin/main -1 --format='%ad' --date=format:'%Y-%m-%d %H:%M' 2>/dev/null)
NOW=$(date '+%Y-%m-%d %H:%M %Z')
TODAY=$(date +%Y/%m/%d); TODAY_DASH=$(date +%Y-%m-%d)

[ -n "$TIP" ] || { echo "cohort-status: FATAL — cannot read origin/main. This tool measured NOTHING." >&2; exit 3; }

# ── Roster: union of four independent sources, with disagreement reported ─────────────────────────
src_registry=$(grep -vE '^#|^role' dev/active/duty-cycle-registry.tsv 2>/dev/null | cut -f1 | grep -E '^[a-z]+$' | sort -u)
src_mailbox=$(ls -1d mailboxes/*/ 2>/dev/null | xargs -n1 basename | grep -E '^[a-z]+$' | grep -vE '^(ted-nadeau)$' | sort -u)
src_briefing=$(ls -1 docs/briefing/BRIEFING-ESSENTIAL-*.md 2>/dev/null | sed -E 's|.*BRIEFING-ESSENTIAL-||; s|\.md||' | tr 'A-Z' 'a-z' | sort -u)
src_roster=$(grep -oE '\b(arch|cio|comms|cxo|docs|exec|host|lead|pa|ppm|web)\b' docs/briefing/ROSTER.md 2>/dev/null | sort -u)
# A ROLE is a mailbox that ALSO has a registry row, a role briefing, or a ROSTER.md entry.
# Mailbox-alone is not sufficient: `xian`, `spec` and `ted-nadeau` are correspondence destinations,
# not cycling roles, and counting them inflated the denominator to 13 on the first run -- which is
# failure #3 (counting the wrong set) reappearing inside the tool built to prevent it. Caught by
# reading the tool's own output instead of trusting that it had the right list.
ROSTER=$(for r in $src_mailbox; do
  printf '%s\n' "$src_registry" | grep -qx "$r" && { echo "$r"; continue; }
  printf '%s\n' "$src_roster"   | grep -qx "$r" && { echo "$r"; continue; }
  [ -f "docs/briefing/BRIEFING-ESSENTIAL-$(printf '%s' "$r" | tr 'a-z' 'A-Z').md" ] && echo "$r"
done | sort -u)
N_ROSTER=$(printf '%s\n' "$ROSTER" | grep -c .)

echo "cohort-status v1.0 — read origin/main @ $TIP ($TIPTS), generated $NOW"
echo "roster = UNION of registry($(printf '%s\n' "$src_registry"|grep -c .)) + mailboxes($(printf '%s\n' "$src_mailbox"|grep -c .)) + ROSTER.md($(printf '%s\n' "$src_roster"|grep -c .)) = $N_ROSTER roles"
for r in $ROSTER; do
  miss=""
  printf '%s\n' "$src_registry" | grep -qx "$r" || miss="$miss registry"
  printf '%s\n' "$src_roster"   | grep -qx "$r" || miss="$miss ROSTER.md"
  [ -n "$miss" ] && echo "  ⚠️  SOURCE DISAGREEMENT: '$r' is absent from:$miss — do not trust any count that used only those."
done
echo

printf "  %-6s %-7s %-12s %-9s %-7s %-8s %s\n" ROLE SESSION LAST-CMT LOG-TODAY CLOSED REGISTRY INBOX/MAN
for r in $ROSTER; do
  sess=$(tmux list-panes -t "=$r" -F '#{pane_current_command}' 2>/dev/null | head -1); sess="${sess:-—}"
  case "$sess" in 2.*) sess="live";; zsh|bash|sh) sess="⚠️SHELL";; *) sess="—";; esac
  last=$(git log origin/main -1 --format='%ad' --date=format:'%m-%d %H:%M' --grep="($r)" 2>/dev/null); last="${last:-never}"
  logf=$(ls "dev/$TODAY/" 2>/dev/null | grep -- "-$r-code" | head -1)
  logt=$([ -n "$logf" ] && echo yes || echo "—")
  closed="—"
  # READ the marker for TODAY specifically -- counting bare "DAY-CLOSED" matched yesterday's references.
  [ -n "$logf" ] && { grep -qE "^(<!--[[:space:]]*)?#{0,4}[[:space:]]*DAY-CLOSED:?[[:space:]]+$TODAY_DASH" "dev/$TODAY/$logf" 2>/dev/null && closed="yes" || closed="no"; }
  # Mirror freeze-check's ACTUAL rule: only a state beginning `parked` suppresses watching.
  # v1.0 treated ANY non-empty state column as parked, so `arch` and `comms` -- which armed their
  # crons and cleared their notes by writing "active: cron armed <job>" -- were reported PARKED while
  # the belt correctly watched them. A disagreement between two of my own instruments, found within
  # three hours, by reading the registry beside the tool instead of trusting the tool. Same class the
  # tool exists to catch; it made the error visible, it did not prevent it.
  reg=$(grep -vE '^#|^role' dev/active/duty-cycle-registry.tsv 2>/dev/null | awk -F'\t' -v r="$r" '$1==r{ if ($8=="") print "watched"; else if ($8 ~ /^parked/) print "parked"; else print "watched*" }')
  reg="${reg:-NO-ROW}"
  n=$(ls -1 "mailboxes/$r/inbox" 2>/dev/null | grep -v MANIFEST | wc -l | tr -d ' ')
  m=$(grep -E '^\|.*\.md' "mailboxes/$r/inbox/MANIFEST.md" 2>/dev/null | wc -l | tr -d ' ')
  flag=""
  [ "$n" -gt 20 ] && flag=" ⚠️backlog"
  [ "$n" -gt 0 ] && [ "$m" -lt $(( n / 2 )) ] && flag="$flag 🔴manifest-stale"
  printf "  %-6s %-7s %-12s %-9s %-7s %-8s %s/%s%s\n" "$r" "$sess" "$last" "$logt" "$closed" "$reg" "$n" "$m" "$flag"
done

echo
echo "denominators — every count above is out of $N_ROSTER roster roles, NOT out of tmux sessions."
echo "  live sessions: $(for r in $ROSTER; do tmux has-session -t "=$r" 2>/dev/null && echo x; done | grep -c .) / $N_ROSTER"
echo "  registry rows: $(printf '%s\n' "$src_registry" | grep -c .) / $N_ROSTER   (a role with NO-ROW is invisible to the freeze-watchdog)"
echo "  closed today:  $(for r in $ROSTER; do f=$(ls "dev/$TODAY/" 2>/dev/null | grep -- "-$r-code" | head -1); [ -n "$f" ] && grep -qE "^(<!--[[:space:]]*)?#{0,4}[[:space:]]*DAY-CLOSED:?[[:space:]]+$TODAY_DASH" "dev/$TODAY/$f" 2>/dev/null && echo x; done | grep -c .) / $N_ROSTER"
