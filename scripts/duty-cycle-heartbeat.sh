#!/usr/bin/env bash
# duty-cycle-heartbeat.sh v1.0 (CIO 2026-07-28; proposed 07-27, HOST-approved 07-28 with 3 refinements)
#
# WHY THIS EXISTS
# The freeze-watchdog inferred liveness from WORK OUTPUT — commits and session-log updates. But the
# duty-cycle skill tells agents NOT to produce work output on quiet fires ("don't commit a
# near-duplicate entry each fire"; "trivial/quiet-hold fires don't need an entry"). So a CORRECTLY
# EXECUTED quiet fire left no trace on origin/main and was invisible to the belt BY CONSTRUCTION —
# we were alerting on compliance. lead was flagged 3x on 2026-07-27 while alive and working.
#
# ⚠️ HOW TO READ THIS SURFACE — 2026-08-05, added after its own author misread it.
# This file is APPEND-PER-FIRE, so a role has one row per fire that day. Reading it without filtering
# gives a DIFFERENT ANSWER depending on which row you grab, and the error is not random:
#
#   ⭐ IT SELECTIVELY HITS THE MOST ACTIVE ROLES. A role that fired once has no later row to misread;
#      a role that fired three times does. So a naive read reports the roles that emitted MOST as the
#      ones performing WORST. The measurement error correlates with compliance. (PA, 2026-08-05: I
#      published host as +203 and pa as +210 when they were +24 and +30 — they had 3 rows each; ppm
#      was the one I got right, purely because it had a single row.)
#
# For per-fire latency, FILTER ON THE FIRE TYPE — column 3 exists for exactly this:
#     awk -F'\t' '$3=="START"' dev/heartbeats/YYYY-MM-DD/{role}.tsv | head -1
# Prefer this over `head -1`: a role that never emitted a START returns EMPTY (a visible, correct
# signal) rather than silently handing you its 10:00 WORK row as if it were the morning fire.
#
# No threshold reconciles "detect a stall fast" with "tolerate legitimate quiet" when the only
# evidence is whether work happened. Widening trades false positives for latency, and for
# low-frequency roles the trade is unacceptable (exec fires 2x/day → a 25h threshold). The fix is to
# stop inferring liveness from work at all: emit a signal that means "I woke up", nothing more.
#
# HOST'S THREE REFINEMENTS, all implemented:
#  (a) COST IS PER QUIET FIRE, NOT PER FIRE. On a fire that does work, the work commit already IS a
#      heartbeat — it carries role and timestamp on origin/main. Only fires that would otherwise
#      leave no trace need this. Busy agents pay ~zero. See --if-quiet.
#  (b) SIZE DISCIPLINE ON DAY ONE. We have watched this exact append-only shape fail twice this month
#      (MEMORY.md byte truncation, then its line ceiling underneath). Rotation is structural here:
#      one file per role per day, so no file grows without bound and nothing needs pruning logic to
#      stay correct. It also removes write contention entirely — each role owns its own path, so ten
#      agents can never conflict on a shared append.
#  (c) SILENCE MUST BE DIAGNOSTIC (G6). A broken heartbeat WRITER looks exactly like a quiet cohort —
#      the file simply stops growing. So the reader side (duty-cycle-freeze-check.sh) distinguishes
#      "this role is missing" from "NOBODY wrote today", and reports the latter as a writer fault
#      rather than as N independent stalls. This file's job is to make that distinguishable; see
#      HEARTBEAT-WRITER-SILENT there.
#
# NOT A LOGGING SURFACE. This is machine-readable liveness, not a record. The session log remains the
# single canonical record (PM 2026-06-12). What the skill forbids is a near-duplicate PROSE entry
# polluting institutional memory — which is why the same line REQUIRES one-line WATCH/START entries.
# A TSV append was never in scope of that prohibition (HOST concurring, 2026-07-28).
#
# USAGE
#   scripts/duty-cycle-heartbeat.sh <role> [fire-type]      # always writes
#   scripts/duty-cycle-heartbeat.sh <role> [fire-type] --if-quiet
#       ↳ writes ONLY if this role has no commit on origin/main since its last heartbeat window,
#         i.e. only when the fire would otherwise be invisible. This is the form the skill calls.
set -uo pipefail

ROLE="${1:-}"; FIRE="${2:-work}"; MODE="${3:-}"
[ -n "$ROLE" ] || { echo "usage: $0 <role> [fire-type] [--if-quiet]" >&2; exit 2; }
case "$FIRE" in --*) MODE="$FIRE"; FIRE="work";; esac

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "heartbeat: not in a git repo" >&2; exit 2; }

DAY="$(date +%Y-%m-%d)"
DIR="dev/heartbeats/$DAY"
FILE="$DIR/${ROLE}.tsv"
TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# v1.1 (2026-09-04, CXO's finding, Docs/Exec endorsed — standing-item 7j). Prior to this, an
# --if-quiet suppression wrote NOTHING: the freeze-watchdog then saw "no heartbeat row today" and
# could not tell (a) writer runs, correctly suppressed vs. (c) writer invoked once, then stopped
# entirely (CXO's real case: 7 real invocations, then silence for 24 days, masked the whole time by
# real commit output — Arch's incident shape exactly). `--if-quiet` making the writer's own health
# unobservable is precisely the failure mode CXO named: "a busy agent never writes a row, therefore
# never learns whether its writer works — until the day it goes quiet, and that is exactly the day
# the answer matters." Fix: this marker is OVERWRITTEN (not appended, so no unbounded growth like
# the per-day TSVs) on every invocation of this script, suppressed or not — so a role's writer
# health becomes checkable independent of whether today produced a real heartbeat row.
LAST_INVOKED_DIR="dev/heartbeats/last-invoked"
LAST_INVOKED_FILE="$LAST_INVOKED_DIR/${ROLE}.txt"
mkdir -p "$LAST_INVOKED_DIR"
printf '%s\t%s\n' "$TS" "$FIRE" > "$LAST_INVOKED_FILE"

# --if-quiet: skip when the fire already produced a role-tagged commit today. That commit IS the
# heartbeat (refinement a), so writing another would be pure churn.
# ⚠️ 2026-08-04: START ALWAYS WRITES, --if-quiet or not.
# Refinement (a) suppresses the write whenever the role committed, which on a busy cohort is every
# fire — so the surface is legitimately empty on a healthy day. That made the G6 writer-liveness
# check unable to distinguish "nobody ran the writer" from "everyone was busy", and after the 7/29
# correction (also require zero commits) G6 became PERMANENTLY SILENT on any active day.
# Consequence, observed: the writer has been unrun since 2026-07-28 by every role including me, and
# nothing could say so. Exactly the m-44 shape, inside the m-44 fix.
# One unconditional line per role per START (11 lines/day) restores the discriminator at trivial
# cost: an empty surface past midday now means the writer is dead, not that the day was productive.
if [ "$FIRE" = "START" ] && [ "$MODE" = "--if-quiet" ]; then
  echo "heartbeat: START always writes (surface must stay diagnostic) — ignoring --if-quiet"
  MODE=""
fi

if [ "$MODE" = "--if-quiet" ]; then
  git fetch origin main -q 2>/dev/null || true
  # NO `git log ... | grep -q` here, and the reason is a real bug this replaced:
  # `grep -q` exits the instant it matches, which SIGPIPEs the still-writing `git log`; under
  # `set -o pipefail` that non-zero producer status becomes the pipeline's status, so the guard
  # reported NO MATCH *because it had matched*. Timing-dependent, so it passed when tested in
  # isolation and failed inside the script -- an intermittent false-negative in a guard, which is
  # the m-44 family exactly. Capture first, then test the string: no pipe, no race.
  #
  # ⚠️ 2026-08-28 (Web found it, CIO fixed it): window shortened 6h -> 3h. Suppression CASCADES —
  # a suppressed fire produces no new reference point, so consecutive quiet fires stack against the
  # SAME stale commit timestamp until the window finally elapses. On the cohort's tightest cadence
  # (3h, nine of eleven roles), a 6h window let TWO consecutive quiet fires suppress before a third
  # fire finally wrote — worst case ~9h of true silence (three fire-intervals) against those roles'
  # own 7h dynamic threshold, a false stale-alert on a role that never missed a beat (Web, 08-28:
  # every fire ran on schedule; the freeze-watchdog's own alert matched the gap almost to the
  # minute). 3h is the shortest inter-fire gap anywhere in the registry — at that window, AT MOST
  # ONE quiet fire in a row can suppress (elapsed 3h is right at the boundary; the second consecutive
  # quiet fire's elapsed 6h clears it and writes), bounding worst-case silence to ~2 fire-intervals,
  # safely under any role's 2x-gap+1 dynamic threshold with real margin. Costs looser-cadence roles
  # (cio, exec) some of the "free" suppression — cheap, since a heartbeat write is a few bytes.
  recent="$(git log origin/main --since="3 hours ago" --format=%s 2>/dev/null || true)"
  case "$recent" in *"($ROLE)"*) hb_already=1;; *) hb_already=0;; esac
  if [ "$hb_already" = 1 ]; then
    # v1.1: don't just exit — land the last-invoked marker so the suppression itself is observable.
    # Same failure posture as the full-write path below (fail loud, never silently), but this is a
    # single-line overwrite, not an unbounded append, so the "cost is per quiet fire" design intent
    # is preserved: the marker commit is the same trivial size a heartbeat row would have been.
    git add -- "$LAST_INVOKED_FILE" 2>/dev/null
    if git diff --cached --quiet -- "$LAST_INVOKED_FILE" 2>/dev/null; then
      echo "heartbeat: $ROLE committed within 3h — that commit IS the heartbeat; nothing written (refinement a)"
      exit 0
    fi
    if git commit -q -m "hb-last-invoked($ROLE): suppressed $FIRE $TS" -- "$LAST_INVOKED_FILE" 2>/dev/null \
       && git fetch origin main -q 2>/dev/null \
       && git merge origin/main --no-edit -q 2>/dev/null \
       && git push -q origin HEAD:main 2>/dev/null; then
      git push -q origin HEAD 2>/dev/null || true
      echo "heartbeat: $ROLE committed within 3h — row suppressed (refinement a), last-invoked marker updated"
      exit 0
    fi
    echo "heartbeat: WARNING — last-invoked marker failed to land for $ROLE (row itself correctly suppressed); not treated as fatal" >&2
    exit 0
  fi
fi

mkdir -p "$DIR"
printf '%s\t%s\t%s\n' "$TS" "$ROLE" "$FIRE" >> "$FILE"

# DELIVERY. mail-send.sh is deliberately NOT reused: it refuses non-mailbox paths on purpose, and
# that guardrail protects mail discipline (mail must land on main, from any worktree, without
# touching a shared checkout). Widening it to carry heartbeats would trade a real protection for a
# convenience. Heartbeats are ordinary agent-owned files, so they ship the ordinary way.
#
# Per-role daily paths mean two agents can never touch the same file, so no retry/rebase dance is
# needed — the only conflict possible is on the commit tip, which the push handles.
# v1.1: the last-invoked marker rides in the SAME commit as the heartbeat row (one push, not two).
git add -- "$FILE" "$LAST_INVOKED_FILE" 2>/dev/null
if git diff --cached --quiet -- "$FILE" 2>/dev/null; then
  echo "heartbeat: nothing staged for $FILE — refusing to report success (m-44: a no-op must not look like a write)" >&2
  exit 1
fi
if git commit -q -m "hb($ROLE): $FIRE $TS" -- "$FILE" "$LAST_INVOKED_FILE" 2>/dev/null \
   && git fetch origin main -q 2>/dev/null \
   && git merge origin/main --no-edit -q 2>/dev/null \
   && git push -q origin HEAD:main 2>/dev/null; then
  git push -q origin HEAD 2>/dev/null || true
  echo "heartbeat: $ROLE $FIRE -> $FILE (on origin/main)"
  exit 0
fi

# Fail LOUDLY rather than quietly (m-44): a heartbeat that silently fails to land is worse than none,
# because the belt would then read the role as stale and nobody would know why.
echo "heartbeat: FAILED to land $FILE on origin/main — the belt will read $ROLE as stale and the cause will not be visible. Investigate now." >&2
exit 1
