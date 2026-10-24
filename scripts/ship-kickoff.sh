#!/usr/bin/env bash
# ship-kickoff.sh — send the weekly Ship workstream-review kickoff without anyone remembering to.
#
# Why: the kickoff lived in Exec's standing items and habits, and was missed two Fridays running
# (#064, #065). xian 2026-10-16: make it automatic. Exec's every-fire command runs
#     scripts/ship-kickoff.sh --if-due
# before the heartbeat, so the first fire on Friday sends it.
#
# Rules:
#   - Window: Fri → Thu, the week that closed before the most recent Friday (Pacific).
#   - Ship number: #065 is the window 2026-10-09 → 10-15; +1 per week after.
#   - Due: Friday, Saturday or Sunday (Pacific) and no kickoff for that Ship in mailboxes/exec/sent/.
#     Mon–Thu it does nothing. Idempotent: a second run finds the sent file and exits.
#   - Sends to every leadership role. Exec adds the week's context by hand as a follow-up.
#
# Usage:
#   scripts/ship-kickoff.sh --if-due                 # normal: send if due, else silent
#   scripts/ship-kickoff.sh --dry-run [--date D]     # print what would be sent (D = YYYY-MM-DD, Pacific)
set -euo pipefail

MODE=""; TODAY=""
while [ $# -gt 0 ]; do
  case "$1" in
    --if-due) MODE=send ;;
    --dry-run) MODE=dry ;;
    --date) TODAY="$2"; shift ;;
    *) echo "usage: $0 --if-due | --dry-run [--date YYYY-MM-DD]" >&2; exit 2 ;;
  esac
  shift
done
[ -n "$MODE" ] || { echo "usage: $0 --if-due | --dry-run [--date YYYY-MM-DD]" >&2; exit 2; }
[ "$MODE" = dry ] || [ -z "$TODAY" ] || { echo "--date is for --dry-run only" >&2; exit 2; }

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
[ -n "$TODAY" ] || TODAY="$(TZ=America/Los_Angeles date +%Y-%m-%d)"

read -r SHIP WSTART WEND FRIDAY DOW < <(python3 - "$TODAY" <<'EOF'
import sys, datetime as dt
d = dt.date.fromisoformat(sys.argv[1])
fri = d - dt.timedelta(days=(d.weekday() - 4) % 7)        # most recent Friday, today included
ship = 65 + (fri - dt.date(2026, 10, 16)).days // 7
print(f"{ship:03d}", (fri - dt.timedelta(days=7)).isoformat(), (fri - dt.timedelta(days=1)).isoformat(),
      fri.isoformat(), d.weekday())
EOF
)

ROLES="arch cio cxo comms docs host lead pa ppm web"

# The cycle's status line, printed on every fire Fri → Wed once the kickoff is out (xian 2026-10-23,
# after Exec skipped the skill's synthesis step for #066 and went straight to a draft). It reads the
# files that define each step, so it cannot drift from what has actually happened, and it names the
# next step and the skill that runs it. Steps (draft-weekly-ship skill, process guide's ten steps):
#   reviews 10/10 → synthesis (Step 2c) → discussed with xian (step 7) → draft (step 8) → published.
# The synthesis lives at docs/internal/planning/comms/ship-reviews/ship-NNN-week-review.html and
# carries `<!-- discussed: YYYY-MM-DD -->` once xian has discussed it.
ship_status() {
  python3 - "$SHIP" "$ROLES" <<'EOF'
import sys, subprocess, csv, glob, os, re
ship, roles = sys.argv[1], sys.argv[2].split()
def tree(path):
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", "origin/main", path],
                         capture_output=True, text=True).stdout.split()
    return out
files = tree("mailboxes/exec/inbox") + tree("mailboxes/exec/read")
filed = sorted({r for r in roles for f in files if os.path.basename(f).startswith(f"workstream-{ship}-{r}-")})
missing = [r for r in roles if r not in filed]
syn = f"docs/internal/planning/comms/ship-reviews/ship-{ship}-week-review.html"
has_syn = os.path.exists(syn)
discussed = has_syn and re.search(r"<!-- discussed: \d{4}-\d{2}-\d{2} -->", open(syn).read())
drafts = glob.glob(f"docs/public/comms/drafts/weekly-ship-{ship}-draft-*.md") + \
         glob.glob(f"docs/public/comms/drafts/published/weekly-ship-{ship}-*.md")
status = ""
for row in csv.DictReader(open("docs/internal/planning/comms/editorial-calendar.csv")):
    if row.get("title", "").startswith(f"Weekly Ship #{ship}"):
        status = row.get("status", "")
parts = [f"reviews {len(filed)}/{len(roles)}",
         f"synthesis: {'discussed' if discussed else ('written, not yet discussed' if has_syn else 'none')}",
         f"draft: {'yes' if drafts else 'none'}", f"calendar: {status or '?'}"]
if missing:
    nxt = f"wait for reviews; missing: {', '.join(missing)} (nudge after Saturday midday)"
elif not has_syn:
    nxt = "INVOKE the draft-weekly-ship skill, Step 2c: write the synthesis for xian. No draft before it."
    if drafts:
        nxt = "A DRAFT EXISTS WITH NO SYNTHESIS (the skill was skipped). " + nxt
elif not discussed:
    nxt = "discuss the synthesis with xian (rollup card, notify Janus). No draft until he has."
    if drafts:
        nxt += " A draft already exists ahead of the discussion: hold it, and rebuild it from the discussion."
elif not drafts:
    nxt = "INVOKE the draft-weekly-ship skill, step 8: draft from the discussion, calendar row in the same commit."
elif status in ("distributed", "published"):
    nxt = "done."
else:
    nxt = "xian's first look (he gates the Comms handoff), then Comms review; publish Wednesday."
print(f"ship-status #{ship}: " + " · ".join(parts) + f" · NEXT: {nxt}")
EOF
}

# Due only Fri (4), Sat (5), Sun (6). Mon (0) to Wed (2) print the status line only. Thu is silent.
if [ "$MODE" = send ] && [ "$DOW" -eq 3 ]; then exit 0; fi

# Already sent? Check origin/main (the record other seats see) and the local tree. No `grep -q` in a
# pipe: under pipefail its early exit SIGPIPEs the producer and the test reads false (sent a
# duplicate #065 on 2026-10-16, the first live run).
git fetch -q origin main 2>/dev/null || true
SENT_ORIGIN="$(git ls-tree --name-only origin/main mailboxes/exec/sent/ | grep -c -- "-ship-${SHIP}-workstream-review" || true)"
SENT_LOCAL="$(find mailboxes/exec/sent -maxdepth 1 -name "*-ship-${SHIP}-workstream-review*" | wc -l | tr -d ' ')"
if [ "${SENT_ORIGIN:-0}" -gt 0 ] || [ "${SENT_LOCAL:-0}" -gt 0 ]; then
  [ "$MODE" = dry ] && echo "ship-kickoff: #${SHIP} kickoff already sent; nothing to do"
  ship_status || echo "ship-status #${SHIP}: could not read the cycle's state; check by hand" >&2
  exit 0
fi
# Mon–Wed with no kickoff sent: the cycle never started. Say so rather than stay silent.
if [ "$DOW" -lt 3 ]; then
  echo "ship-status #${SHIP}: NO KICKOFF was sent for this week. Send it now (--if-due works Fri–Sun) and tell xian." >&2
  exit 0
fi

NEXT_START="$FRIDAY"
NEXT_END="$(python3 -c "import datetime as d;print((d.date.fromisoformat('$FRIDAY')+d.timedelta(days=6)).isoformat())")"
NAME="kickoff-exec-to-leadership-ship-${SHIP}-workstream-review-${WSTART}-to-${WEND}-${FRIDAY}.md"
NOW="$(TZ=America/Los_Angeles date '+%Y-%m-%d %H:%M')"

write_body() {
cat <<EOF
---
from: exec
to: ${ROLES// /, }
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: ${NOW} PT
subject: "Ship #${SHIP} workstream review: window Fri ${WSTART} → Thu ${WEND}. File by Saturday midday. Task, owner: each of you for your own lane"
---

# Ship #${SHIP}: workstream review request

Sent automatically by \`scripts/ship-kickoff.sh\` on the first Exec fire after the window closed. Exec follows with the week's context.

**Kind:** a task. Each recipient owns their own lane's review. If you've already filed for #${SHIP}, nothing more is needed.

## Window

**Friday ${WSTART} → Thursday ${WEND}.** Work from ${FRIDAY} on belongs to the next Ship.

## When

**By Saturday midday.** Anything in by then goes into the synthesis with time for questions.

## The frame (xian's standing ask)

**Show what a user can do this week that they couldn't do last week.** If the honest answer is "nothing a user can see yet, and here is what it unblocks", write that.

## Progress claims

Every progress claim carries \`Verified how:\` with the method you ran **this time**, the layer it measured, and the denominator. If a claim rests on an earlier check, say so. Run \`date\` before writing any time.

## Next week

A short **"Next week"** section: what you intend to land ${NEXT_START} to ${NEXT_END}, and what you're blocked on. Two or three lines.

## File it

Write it as \`workstream-${SHIP}-{your-role}-{date}.md\` and send it to \`mailboxes/exec/inbox/\` with \`scripts/mail-send.sh\`.

— Exec
EOF
}

if [ "$MODE" = dry ]; then
  echo "ship-kickoff (dry run for ${TODAY}): would send ${NAME} to: ${ROLES}"
  echo "----"
  write_body
  exit 0
fi

PATHS=("mailboxes/exec/sent/$NAME")
write_body > "mailboxes/exec/sent/$NAME"
for r in $ROLES; do
  cp "mailboxes/exec/sent/$NAME" "mailboxes/$r/inbox/$NAME"
  PATHS+=("mailboxes/$r/inbox/$NAME")
done
scripts/mail-send.sh "mail(exec): Ship #${SHIP} workstream kickoff (automatic)" "${PATHS[@]}"
git fetch -q origin main
if git ls-tree origin/main "mailboxes/lead/inbox/$NAME" | grep -q .; then
  echo "ship-kickoff: #${SHIP} kickoff sent and landed (${#PATHS[@]} files)"
else
  echo "ship-kickoff: #${SHIP} kickoff NOT confirmed on origin/main — check by hand" >&2
  exit 1
fi
