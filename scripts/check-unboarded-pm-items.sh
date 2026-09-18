#!/usr/bin/env bash
# check-unboarded-pm-items.sh — PM-facing items that exist somewhere but have never reached a board.
#
# WHY (2026-09-18, Exec; surface 4 + the scan cadence are PM's design, same day):
#   "The board is the flag": if an item needing PM isn't on the attention board, PM has not been asked.
#   Three misses traced this morning had three different causes and ONE shape — a check ran, or a
#   person acted correctly, and the result landed where nothing downstream reads.
#
#   The sharpest: mail triage moves a memo inbox/ -> read/, and the board's mail sweep only looked at
#   inbox/. HOST's alpha-tester invite arrived and was triaged in the SAME COMMIT, 3h27m after that
#   day's board compiled, then sat unsurfaced for five days.
#   ** A memo left rotting unread WOULD have been caught. Prompt triage is what hid it. **
#   Diligence is the failure mode, so more diligence cannot fix it — only a check that looks at the
#   surface triage moves things TO.
#
#   PM's generalization, which is why this runs at TRIAGE and not only at board-compile:
#   "maybe triage needs to scan for recent changes in the full tree, including newly read mail since
#   last time-of-scan?" Triage happens every fire; a board compiles occasionally. Scanning at triage
#   catches things in hours instead of between boards — and "full tree" is what adds surface 4,
#   commit-message bodies, which is where the Apache-2.0 copyright flag sat unanswered for 16 days.
#
# WHAT IT IS NOT: it does not judge whether an item needs PM. It surfaces candidates and states its
#   coverage. Read-only, advisory, no verdicts. It cannot read intent and says so rather than guessing.
#
# Usage:
#   scripts/check-unboarded-pm-items.sh [role]              # window = last board compile
#   scripts/check-unboarded-pm-items.sh [role] --since-last-scan
#   scripts/check-unboarded-pm-items.sh [role] --since-last-scan --record   # then stamp the marker
#   BOARD_SINCE=2026-09-13 scripts/check-unboarded-pm-items.sh exec

set -uo pipefail

ROLE="exec"; MODE="board"; RECORD=0
for a in "$@"; do
  case "$a" in
    --since-last-scan) MODE="scan" ;;
    --record) RECORD=1 ;;
    -*) echo "unknown flag: $a" >&2; exit 2 ;;
    *) ROLE="$a" ;;
  esac
done

cd "$(git rev-parse --show-toplevel)" || exit 2

PM_BOX="mailboxes/xian (ceo)/inbox"
READ_BOX="mailboxes/${ROLE}/read"
STANDING="dev/active/${ROLE}-standing-items.md"
MARKER="dev/active/${ROLE}-last-pm-scan"

BOARD=$(git ls-files "dev/*${ROLE}-cohort-attention-rollup-*.html" 2>/dev/null | sort | tail -1)

# ---- window -------------------------------------------------------------------------------------
if [[ -n "${BOARD_SINCE:-}" ]]; then
  SINCE="$BOARD_SINCE"; WSRC="BOARD_SINCE override"
elif [[ "$MODE" == "scan" && -s "$MARKER" ]]; then
  SINCE=$(head -1 "$MARKER"); WSRC="last recorded scan ($MARKER)"
elif [[ "$MODE" == "scan" ]]; then
  SINCE=$(date -v-1d +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d '1 day ago' +%Y-%m-%dT%H:%M:%S)
  WSRC="NO MARKER YET — defaulted to 24h (first run; --record to start the chain)"
elif [[ -n "$BOARD" ]]; then
  SINCE=$(git log --format=%aI -1 -- "$BOARD"); WSRC="commit time of the last board"
else
  SINCE=$(date -v-7d +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -d '7 days ago' +%Y-%m-%dT%H:%M:%S)
  WSRC="NO PRIOR BOARD FOUND — defaulted to 7 days"
fi

echo "── unboarded PM items · role=${ROLE} · mode=${MODE} ────────────────"
echo "window starts: ${SINCE}"
echo "window source: ${WSRC}"
[[ -n "$BOARD" ]] && echo "latest board:  ${BOARD}"
echo

# addressed_to_pm <file> — TRUE only if PM is in the `to:` header, never `cc:`.
# ⚠️ This distinction is load-bearing and was learned the hard way: **cc is not briefing.** Cc'ing PM
# on an exchange with someone else does not brief them. The first version of this script matched on
# the FILENAME, and because `cc-pm` is the cohort's default habit it flagged 88 of 88 memos — a
# check that fires on everything is identical in value to one that fires on nothing.
addressed_to_pm() {
  local f="$1"; [[ -r "$f" ]] || return 1
  awk '/^---[[:space:]]*$/{n++; next} n==1 && /^[Tt][Oo]:/{print; exit}' "$f" 2>/dev/null \
    | grep -qiE 'xian|\bpm\b|ceo'
}

echo "1. MAIL TRIAGED TO read/ IN THE WINDOW — the surface triage moves things TO"
TRIAGED=$(git log --since="$SINCE" --diff-filter=A --name-only --format= -- "$READ_BOX" 2>/dev/null | sed '/^$/d' | sort -u)
N1_ALL=$(printf '%s' "$TRIAGED" | grep -c . || true); N1=0
if [[ "$N1_ALL" -gt 0 ]]; then
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    addressed_to_pm "$f" || continue           # to: PM only — cc is not briefing
    N1=$((N1+1)); printf '   %s\n' "$(basename "$f")"
  done <<< "$TRIAGED"
fi
[[ "$N1" -eq 0 ]] && echo "   none addressed to PM."
echo "   → ${N1} of ${N1_ALL} triaged memos name PM in \`to:\` (cc-only deliberately excluded)."
echo

echo "2. MEMOS LANDED IN PM'S INBOX IN THE WINDOW, ADDRESSED TO PM"
PMNEW=$(git log --since="$SINCE" --diff-filter=A --name-only --format= -- "$PM_BOX" 2>/dev/null | sed '/^$/d' | sort -u)
N2_ALL=$(printf '%s' "$PMNEW" | grep -c . || true); N2=0
if [[ "$N2_ALL" -gt 0 ]]; then
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    addressed_to_pm "$f" || continue
    N2=$((N2+1)); printf '   %s\n' "$(basename "$f")"
  done <<< "$PMNEW"
fi
[[ "$N2" -eq 0 ]] && echo "   none addressed to PM."
echo "   → ${N2} of ${N2_ALL} landed memos are addressed TO PM. The rest are cc copies —"
echo "     real mail, but cc is not briefing, so they are not automatically PM's to action."
echo

# ---- 3. standing-items rows self-declaring a PM block --------------------------------------------
echo "3. ROWS IN ${STANDING} SELF-DECLARING A PM BLOCK"
N3=0; N3U=0
if [[ ! -f "$STANDING" ]]; then
  echo "   (no standing-items file for this role — no coverage here, not a clean result)"
else
  ROWS=$(grep -nE '^\|' "$STANDING" | grep -v '~~' | grep -iE 'blocked on pm|awaiting pm|PM decision' || true)
  N3=$(printf '%s' "$ROWS" | grep -c . || true)
  if [[ "$N3" -eq 0 ]]; then echo "   none open."; else
    while IFS= read -r row; do
      [[ -z "$row" ]] && continue
      ln=${row%%:*}
      item=$(printf '%s' "$row" | awk -F'|' '{print $3}' | tr -d '*`~' | sed 's/^ *//;s/ *$//')
      probe=$(printf '%s' "$item" | tr 'A-Z' 'a-z' | grep -oE '[a-z]{5,}' | head -3 | tr '\n' ' ')
      # ⚠️ m-44 guard, and this script committed the exact error it exists to catch: the first
      # version reported "NOT ON BOARD" when the probe was EMPTY — i.e. when it had measured
      # nothing at all. It did that to row 16 ("PM's six-item test round", whose words are all too
      # short), which WAS on the board. A verdict from a check that ran on nothing is m-44 wearing
      # a result's clothing. Three outcomes now, never two.
      if [[ -z "$BOARD" ]]; then       hit="NO BOARD"
      elif [[ -z "$probe" ]]; then     hit="UNTESTABLE"
      else
        found=1; for w in $probe; do grep -qi -- "$w" "$BOARD" || found=0; done
        if [[ "$found" -eq 1 ]]; then hit="on board"; else hit="NOT ON BOARD"; fi
      fi
      [[ "$hit" == "NOT ON BOARD" || "$hit" == "UNTESTABLE" ]] && N3U=$((N3U+1))
      printf '   %-13s L%-4s %s\n' "$hit" "$ln" "${item:0:76}"
    done <<< "$ROWS"
  fi
fi
echo "   → ${N3} open PM-blocked row(s); ${N3U} NOT confirmed present on the latest board"
echo "     (that count includes UNTESTABLE rows — not-confirmed is not the same as not-there)."
echo "     ⚠️  Keyword probe against the board's HTML: false 'on board' on common words, false"
echo "        'NOT ON BOARD' when the board rephrased it. Every line is a candidate to eyeball."
echo

# ---- 4. COMMIT MESSAGE BODIES (PM's "full tree" — the 16-day Apache-2.0 hole) ---------------------
echo "4. COMMIT MESSAGES IN THE WINDOW THAT FLAG SOMETHING FOR PM"
PAT='flagging (to|for) PM|for PM.s (confirmation|call|ruling|decision)|needs PM|PM to (confirm|decide|rule)|awaiting PM|not asserting it as settled|unowned'
CM=$(git log --since="$SINCE" --format='%h%x09%s%x09%b' --all 2>/dev/null | grep -iE "$PAT" | head -20 || true)
N4=$(printf '%s' "$CM" | grep -c . || true)
if [[ "$N4" -eq 0 ]]; then echo "   none."; else
  printf '%s\n' "$CM" | cut -c1-150 | sed 's/^/   /'
fi
echo "   → ${N4} commit(s). This is the surface that hid the Apache-2.0 copyright flag for 16 days:"
echo "     a commit body saying 'flagging to PM for confirmation' is NOT flagging. The board is."
echo

# ---- marker ---------------------------------------------------------------------------------------
if [[ "$RECORD" -eq 1 ]]; then
  date -u +%Y-%m-%dT%H:%M:%SZ > "$MARKER"
  echo "recorded scan time to ${MARKER} ($(cat "$MARKER"))"
  echo
fi

cat <<EOF
── coverage ────────────────────────────────────────────────────────
role '${ROLE}', window from ${SINCE}. Surfaces scanned — 4:
  · mailboxes/${ROLE}/read/           ${N1} added
  · ${PM_BOX}/    ${N2} added
  · ${STANDING}   ${N3} open PM rows (${N3U} unmatched)
  · commit message bodies (--all)     ${N4} flagged

  ⚠️ Deliberately NOT summed into one number. The four surfaces measure different things at
     different confidence, and a single "N candidates" figure would imply they are comparable.

NOT scanned — real gaps, do not infer safety from their absence:
  · GitHub issue comments — not a signalling surface by norm, but flags land there anyway
  · other roles' standing-items files — only '${ROLE}'; pass a role name to widen
  · the CONTENT of any memo — every flag above is a filename or regex heuristic
  · anything raised only in conversation and never written down

A clean run means "nothing found on the four surfaces above." It is NOT a claim that nothing
needs PM. Advisory: surfaces candidates, decides nothing.
EOF
exit 0