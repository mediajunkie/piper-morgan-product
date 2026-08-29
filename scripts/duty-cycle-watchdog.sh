#!/usr/bin/env bash
# duty-cycle-watchdog.sh v2.4 — detect + NUDGE PM + SPAWN-FRESH (Belt 4, default off).
#
# Run by launchd (a pure OS job — ZERO Claude agents, no persona-fork; the cure for the scheduled-task
# approach PM rejected 2026-06-14). Hourly it: fetches origin, runs the freeze-check, and on a NEWLY-stale
# role (or a cooldown re-ping) NUDGES PM via (1) a macOS desktop notification + (2) a durable mailbox
# memo (push-to-ref, so it survives being away from the desktop) + (3) Slack if configured. It does no
# duty-cycle work; the only repo state it writes is its audit log, its nudge-state file, and (via
# push-to-ref, touching no working tree) the alert memo. All three belts reach PM directly — see the
# v2.4 note below for why Belt 2's former CIO-relay hop was removed.
#
# v2.4 (2026-08-29, CIO — Exec's ruling on the carried watchdog-relay-latency question, PM-approved
#   "ok to remove the relay"): Belt 2 now writes straight to PM's own mailbox, not CIO's. The
#   2026-07-12 CIO-relay (below, kept for history) inserted an agent's own cadence — CIO's next mail
#   loop, then Exec's cohort-attention-rollup — into the critical path of a liveness alert that needs
#   no judgment before reaching PM, only speed. Exec's framing: "an agent relay on a watchdog alert
#   adds latency without adding judgment." Raised stakes, same day: a wedged session cannot report
#   itself (the 08-27 rate-limit-dialog gap), so external alerts carry more weight than assumed —
#   exactly the alert class this belt exists to deliver. Belts 1 (desktop) and 3 (Slack) already
#   reached PM with no relay; Belt 2 now matches them instead of being the odd one out.
#
# --- 2026-07-12 CIO-relay design, superseded above, kept for history ---
# Belt 2 routed to CIO's inbox as of 2026-07-12 (PM had retired direct mailbox monitoring at the time)
# -> CIO's carry-forward -> Exec's cohort-attention-rollup -> PM. That chain is gone as of v2.4.
#
# v2 (2026-06-20, PM-requested after the v1 detected the ~26h cohort stall but only logged it — never
# reached PM, who re-prodded manually ~5×):
#   - FETCH origin before checking — v1 read a possibly-stale local origin/main ref → false-stale on a role
#     that was actively committing. The fetch makes heartbeats accurate during normal operation.
#   - DEDUP — nudge on TRANSITION into stale, not every hour (v1 fired hourly = notification fatigue);
#     re-ping only after a cooldown (default 6h) while still stale. Per-role state in a gitignored TSV.
#   - MAILBOX-MEMO belt — PM asked for "both"; durable, survives being away from the desktop.
#   - INFRA-EVENT collapse — >=N roles stale at once = "infrastructure event suspected" (one nudge, the
#     machine-asleep/backgrounded signature) not N alarms (HOST multi-role-silence flag; CIO freeze lane).
#
# v2.3 (2026-06-29, CIO): Belt 4 — SPAWN-FRESH. On a single-role stall, invokes `claude -p` in a fresh
#   detached worktree so the role does a duty-cycle fire without depending on the suspended app. Default OFF
#   (WATCHDOG_AUTO_SPAWN_ROLES=""); enable per-role: WATCHDOG_AUTO_SPAWN_ROLES="cio exec". Validated-viable
#   2026-06-29: auth works headless (binary uses ~/.anthropic/ creds; stripped ANTHROPIC_* env safe).
# v2.2 (2026-06-28, CIO): Belt 0 (AUTO-FOREGROUND) **DISABLED by default** — validated-FAILED on its first
#   real stall (app-foreground can't reach a backgrounded role's window in the multi-window cohort; see the
#   Belt-0 block comment + liveness model). The nudge belts are the working net. Off-machine resume cure
#   (spawn-fresh) scoped separately; Mac Mini is the durable fix. Re-enable: WATCHDOG_AUTO_FOREGROUND=1.
# v2.1 (2026-06-27, CIO): Belt 0 — AUTO-FOREGROUND. `open -b`'s the Claude Code app on a stall to un-suspend
#   the in-app cron. Automated PM's manual resume — the (a) cure-shape. [Superseded by v2.2 — see above.]
#
# Test hooks (used by scripts/test-duty-cycle-watchdog.sh): WATCHDOG_FREEZE_CMD overrides the detector;
# WATCHDOG_DRYRUN=1 logs "WOULD-NUDGE/WOULD-FOREGROUND/WOULD-SPAWN …" instead of firing belts (+ skips fetch);
# WATCHDOG_LOG / WATCHDOG_STATE redirect runtime files; WATCHDOG_NUDGE_COOLDOWN / WATCHDOG_INFRA_THRESHOLD
# tune; WATCHDOG_AUTO_FOREGROUND=1 re-enables Belt 0 (default OFF — validated-failed 6/28);
# WATCHDOG_AUTO_SPAWN_ROLES="cio exec" enables Belt 4 for listed roles (default "" = off);
# WATCHDOG_B4_SPAWN_TTL overrides the lockfile TTL (default 7200 = 2h); WATCHDOG_CLAUDE_BIN overrides binary path.
#
# Design: docs/operations/duty-cycle design/wake-this-session-duty-cycle-design-2026-06-14.md
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
LOG="${WATCHDOG_LOG:-$REPO/dev/active/duty-cycle-watchdog.log}"
STATE="${WATCHDOG_STATE:-$REPO/dev/active/duty-cycle-watchdog-nudge-state.tsv}"
COOLDOWN="${WATCHDOG_NUDGE_COOLDOWN:-21600}"          # 6h re-ping while a role stays stale
INFRA_N="${WATCHDOG_INFRA_THRESHOLD:-3}"               # >=N simultaneous stale = infrastructure event
FREEZE_CMD="${WATCHDOG_FREEZE_CMD:-$REPO/scripts/duty-cycle-freeze-check.sh}"
DRYRUN="${WATCHDOG_DRYRUN:-0}"
SPAWN_ROLES="${WATCHDOG_AUTO_SPAWN_ROLES:-}"           # Belt 4 opt-in per-role; "" = off (default)
SPAWN_TTL="${WATCHDOG_B4_SPAWN_TTL:-7200}"             # Belt 4 lockfile TTL in seconds (default 2h)
CLAUDE_BIN="${WATCHDOG_CLAUDE_BIN:-/Users/xian/.local/bin/claude}"  # Belt 4 binary path
ts=$(date '+%Y-%m-%d %H:%M:%S'); now=$(date +%s)

# Accurate heartbeats: refresh origin/main before checking (read-only; graceful if offline). Skip in dryrun.
[ "$DRYRUN" = 1 ] || git -C "$REPO" fetch origin main -q 2>/dev/null \
  || echo "$ts WARN: fetch failed (heartbeats may be stale this run)" >> "$LOG"

STALE=$(eval "$FREEZE_CMD" 2>/dev/null)
if [ -z "$STALE" ]; then
  : > "$STATE" 2>/dev/null || true   # all healthy → clear state so a future stall nudges fresh
  exit 0
fi
SUMMARY=$(echo "$STALE" | tr '\n' ';' | sed 's/;$//; s/"/\\"/g')
echo "$ts DETECT: $SUMMARY" >> "$LOG"

# Belt 0 — AUTO-FOREGROUND — **DISABLED 2026-06-28 (PM-approved), default off.** VALIDATED-FAILED on its
# first real stall (6/28 AM): it FOREGROUND-fired 4× but the stalled roles did NOT resume, because `open -b`
# foregrounds the *app* (one window) while each role runs in its own window and macOS/Chromium keep BACKGROUND
# windows throttled even when the app is frontmost → app-foreground can't reach the specific stalled role's
# window. Too coarse for the multi-window cohort. The off-machine cure (spawn-fresh, not wake-existing) is the
# path — see duty-cycle-liveness-model + the off-machine-resume-cure scope. Block kept (off) for history +
# the single-window/Mac-Mini case where foregrounding the sole window WOULD work; set WATCHDOG_AUTO_FOREGROUND=1
# to re-enable. The nudge belts below are the working liveness net (detect+alert; dedup'd).
# --- original rationale (pre-failure), retained ---
# Belt 0 — AUTO-FOREGROUND (mode-1b resume; the (a) cure-shape). The in-process cron freezes when macOS
# suspends the backgrounded Claude Code app; this watchdog (a SEPARATE launchd process) survives that, so
# bringing the app forward un-suspends the process → the cron ticks again. This AUTOMATES PM's manual resume
# (which is itself just foregrounding the window — the proof the mechanism works). Uses `open -b` (Launch
# Services, NOT an Apple Event) so it needs no Automation/TCC grant and can't deadlock on the busy app
# (verified: osascript-activate hangs from-within; `open -b` returns clean). Fires on EVERY stale detection
# (the resume attempt) — self-limiting: once the cron resumes + commits a heartbeat, the next run sees fresh
# → not stale → no more foregrounding. Toggle WATCHDOG_AUTO_FOREGROUND=0 to disable; the nudge belts below
# remain the backstop if foreground fails (e.g. launchd-context Launch-Services denial — validates on the
# first real stall via this log: a FOREGROUND line followed by the role going fresh = it worked).
if [ "${WATCHDOG_AUTO_FOREGROUND:-0}" = 1 ]; then
  APP_ID="${WATCHDOG_CLAUDE_APP_ID:-com.anthropic.claude-code}"
  if [ "$DRYRUN" = 1 ]; then
    echo "$ts WOULD-FOREGROUND: open -b $APP_ID (stale: $SUMMARY)" >> "$LOG"
  elif open -b "$APP_ID" 2>/dev/null; then
    echo "$ts FOREGROUND: open -b $APP_ID (resume attempt; stale: $SUMMARY)" >> "$LOG"
  else
    echo "$ts FOREGROUND-FAIL: open -b $APP_ID errored — relying on nudge backstop" >> "$LOG"
  fi
fi

stale_roles=$(echo "$STALE" | sed -n 's/^STALE \([^ ]*\).*/\1/p')
n_stale=$(printf '%s\n' "$stale_roles" | grep -c .)

# ── PARK-NO-EXIT routing (2026-07-27, CIO; gap found by HOST within hours of the detector shipping) ──
# freeze-check v0.6 emits `PARK-NO-EXIT <role>` for a parked row whose reason names no falsifiable
# clearing condition. That line matched NO recipient pattern here, so the detector fired correctly for
# 3.5 hours and notified nobody — a detector wired to a dead output is the same silence it exists to
# break (m-44).
#
# Routing matters as much as delivery, and HOST's split is the load-bearing part: v1.17 says the AGENT
# owns its registry row, which is right FOR A LIVE ROLE — only it knows its cron expression. But a
# PARKED role has no armed cron, so it never wakes to read the ask. **The one party structurally
# capable of acting is not the role.** So these route to CIO (registry owner) as `parkfix-<role>`,
# never to the parked role itself. They ride the existing cooldown machinery so they dedup like any
# other nudge, and they are deliberately kept OUT of n_stale so they can never trip the
# infrastructure-event collapse — a stale park reason is a bookkeeping defect, not a cohort outage.
park_roles=$(echo "$STALE" | sed -n 's/^PARK-NO-EXIT \([^ ]*\).*/\1/p')
n_park=$(printf '%s\n' "$park_roles" | grep -c .)
park_keys=$(printf '%s\n' $park_roles | sed -n 's/^\(..*\)$/parkfix-\1/p')

# Belt 4 — SPAWN-FRESH — default OFF (WATCHDOG_AUTO_SPAWN_ROLES="").
# On a single-role stall, invokes `claude -p` in a fresh detached worktree so the role does a full
# duty-cycle fire without depending on the suspended/backgrounded app. NOT for infra-events (whole
# cohort stale = likely machine-sleep; a single spawn won't cover it). Self-limiting via lockfile.
# Validated-viable 2026-06-29: headless auth works (binary uses ~/.anthropic/ creds; ANTHROPIC_* stripped).
# Enable per-role: launchd plist sets WATCHDOG_AUTO_SPAWN_ROLES="cio exec" in environment.
#
# Per-role spawn prompts: embedded below. Must be self-contained (fresh session, no prior context).
# Implemented: cio, exec, docs (added 2026-07-12). Extend by adding a case branch.
if [ -n "$SPAWN_ROLES" ] && [ "$n_stale" -lt "$INFRA_N" ]; then
  for role in $stale_roles; do
    # Is this role opted in?
    case " $SPAWN_ROLES " in *" $role "*) ;; *) continue ;; esac

    # Lockfile guard: skip if a spawn is already in-flight or recently completed
    LOCKFILE="${STATE%.tsv}.b4-lock-$role"
    if [ -f "$LOCKFILE" ]; then
      if stat -f %m "$LOCKFILE" >/dev/null 2>&1; then
        LMTIME=$(stat -f %m "$LOCKFILE")
      else
        LMTIME=$(stat -c %Y "$LOCKFILE")
      fi
      lockage=$(( now - LMTIME ))
      if [ "$lockage" -lt "$SPAWN_TTL" ]; then
        echo "$ts B4-SKIP: $role (lock within ${SPAWN_TTL}s TTL; age=${lockage}s)" >> "$LOG"
        continue
      fi
      rm -f "$LOCKFILE"  # stale lock — clear and re-spawn
    fi

    # Build per-role spawn prompt (must be self-contained)
    case "$role" in
      cio)
        SPAWN_PROMPT="You are CIO (Chief Innovation Officer) for Piper Morgan (role-slug: cio), resuming from a watchdog-detected stall (B4 spawn-fresh). Working directory is the repo root. Read dev/active/cio-carry-forward.md and dev/active/cio-standing-items.md. Check mailboxes/cio/inbox/ for new mail. Drain all unblocked CIO work using the duty-cycle-tick skill. Commit and push to origin/main when done. Exit when the fire is complete. This is a one-shot autonomous session."
        ;;
      exec)
        SPAWN_PROMPT="You are Chief of Staff (Exec) for Piper Morgan (role-slug: exec), resuming from a watchdog-detected stall (B4 spawn-fresh). Read dev/active/exec-carry-forward.md. Check mailboxes/exec/inbox/ for new mail. Drain all unblocked work using the duty-cycle-tick skill. Commit and push to origin/main. Exit when complete."
        ;;
      docs)
        SPAWN_PROMPT="You are Documentation Management (Docs) for Piper Morgan (role-slug: docs), resuming from a watchdog-detected stall (B4 spawn-fresh). Working directory is the repo root. Read dev/active/docs-carry-forward.md and dev/active/docs-standing-items.md. Check mailboxes/docs/inbox/ for new mail. Drain all unblocked Docs work using the duty-cycle-tick skill. Commit and push to origin/main when done. Exit when the fire is complete. This is a one-shot autonomous session."
        ;;
      *)
        echo "$ts B4-SKIP: $role (no spawn prompt defined; add a case branch)" >> "$LOG"
        continue
        ;;
    esac

    if [ "$DRYRUN" = 1 ]; then
      echo "$ts WOULD-SPAWN [b4]: $role → claude -p in /tmp/b4-spawn-$role" >> "$LOG"
      continue
    fi

    # Write lockfile BEFORE spawning (one-shot guard)
    touch "$LOCKFILE"

    # Create a fresh detached worktree in /tmp (avoids main-checkout HARD RULE; pushes HEAD:main)
    SPAWN_WDIR="/tmp/b4-spawn-$role-$$"  # PID-unique to avoid collisions
    if ! git -C "$REPO" worktree add --detach "$SPAWN_WDIR" origin/main >>"$LOG" 2>&1; then
      echo "$ts B4-FAIL: $role — worktree add failed; see log" >> "$LOG"
      rm -f "$LOCKFILE"
      continue
    fi

    # Spawn headless session; strip ANTHROPIC_* vars to avoid the empty-key trap (CLAUDE.md)
    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
      PIPER_REPO="$REPO" \
      HOME="$HOME" PATH="$PATH" \
      "$CLAUDE_BIN" -p "$SPAWN_PROMPT" \
        --model claude-sonnet-4-6 \
        2>>"$LOG" &
    SPAWN_PID=$!
    echo "$ts B4-SPAWNED: $role → pid=$SPAWN_PID wdir=$SPAWN_WDIR" >> "$LOG"

    # Cleanup worktree after spawn exits (background; watchdog exits independently)
    (wait "$SPAWN_PID" 2>/dev/null; git -C "$REPO" worktree remove --force "$SPAWN_WDIR" >>"$LOG" 2>&1; \
       rm -f "$LOCKFILE"; echo "$(date '+%Y-%m-%d %H:%M:%S') B4-DONE: $role (pid=$SPAWN_PID; worktree removed)" >> "$LOG") &
  done
fi

# Nudge-worthy = newly stale OR cooldown elapsed. awk does the assoc (bash 3.2 has no associative arrays)
# and rewrites the state to ONLY currently-stale roles (recovered roles drop out → re-stall nudges fresh).
nudge_roles=$(printf '%s\n' $stale_roles $park_keys | awk -v now="$now" -v cd="$COOLDOWN" -v sf="$STATE" '
  BEGIN { while ((getline l < sf) > 0) { if (split(l,a,"\t")>=2) last[a[1]]=a[2] } close(sf) }
  { r=$1; if (r=="") next; prev=(r in last)?last[r]:0
    if (prev==0 || (now-prev)>=cd) { print r; cur[r]=now } else { cur[r]=prev } }
  END { t=sf".tmp"; for (r in cur) printf "%s\t%s\n", r, cur[r] > t; close(t) }
')
[ -f "$STATE.tmp" ] && mv "$STATE.tmp" "$STATE"

if [ -z "$nudge_roles" ]; then
  echo "$ts (no nudge — all $n_stale stale + $n_park park-no-exit item(s) within ${COOLDOWN}s cooldown)" >> "$LOG"
  exit 0
fi
nudge_list=$(printf '%s ' $nudge_roles | sed 's/ *$//')

# Framing: infrastructure-event (many at once) vs per-role.
if [ "$n_stale" -ge "$INFRA_N" ]; then
  TITLE="🔴 Piper Morgan: infrastructure event suspected — $n_stale roles silent"
  BODY="$n_stale duty-cycle roles silent at once ($SUMMARY) — likely machine-asleep/backgrounded (cron-survives-doesn't-fire), not individual failures. One wake of the machine/app likely covers it."
else
  TITLE="⚠️ Piper Morgan: duty-cycle stall — $nudge_list"
  BODY="duty-cycle stall ($SUMMARY). The cron object likely survives; the session needs a prod/resume to wake it."
fi

# DRY-RUN (test): record the decision, fire nothing.
if [ "$DRYRUN" = 1 ]; then
  frame=$([ "$n_stale" -ge "$INFRA_N" ] && echo infra || echo perrole)
  echo "$ts WOULD-NUDGE [$frame]: $nudge_list (n_stale=$n_stale)" >> "$LOG"
  exit 0
fi

# Belt 1 — macOS desktop notification (immediate).
/usr/bin/osascript -e "display notification \"$BODY\" with title \"$TITLE\" sound name \"Basso\"" 2>/dev/null

# Belt 2 — durable memo via push-to-ref (survives being away from the desktop).
# Goes straight to PM's own mailbox — no agent relay (v2.4, see the header note for why the
# 2026-07-12 CIO-hop was removed). This memo's only job is to survive being away from the desktop;
# belts 1 and 3 do the live delivery, so this one no longer depends on any agent's cadence to reach PM.
MEMO="mailboxes/xian (ceo)/inbox/alert-duty-cycle-stall-$(date '+%Y-%m-%d-%H%M').md"
cat > "$REPO/$MEMO" <<EOF
---
from: duty-cycle-watchdog (automated)
to: xian (ceo)
date: $(date '+%Y-%m-%d')
subject: $TITLE
priority: high — automated freeze-watcher nudge, delivered direct (no agent relay)
---

# $TITLE

$BODY

- **Detected**: $ts (freeze-watcher hourly run); thresholds per \`dev/active/duty-cycle-registry.tsv\`.
- **Newly nudge-worthy**: $nudge_list   ·   **all currently stale**: $SUMMARY
- **Action**: re-prod the listed role's session. If many at once, wake the machine/app — one wake covers it. (You likely already saw this via the desktop notification or Slack — this memo is the durable copy, in case both were missed.)

*(Automated nudge — duty-cycle-watchdog.sh. Dedup'd: re-pings ~$((COOLDOWN/3600))h while still stale. Delivered direct as of 2026-08-29 (v2.4) — see the header note for the removed CIO-relay history.)*
EOF
if PIPER_REPO="$REPO" "$REPO/scripts/mail-send.sh" "mail(watchdog): $TITLE" "$MEMO" >/dev/null 2>&1; then
  rm -f "$REPO/$MEMO"   # delivered to origin/main via push-to-ref; drop the local copy (no main-checkout residue)
  echo "$ts NUDGE sent — desktop + mailbox (roles: $nudge_list; n_stale=$n_stale)" >> "$LOG"
else
  rm -f "$REPO/$MEMO" 2>/dev/null
  echo "$ts NUDGE — desktop only (mail-send failed; roles: $nudge_list)" >> "$LOG"
fi

# Belt 3 — Slack incoming-webhook, if PM configured one (~/.piper-watchdog-slack-webhook).
HOOK_FILE="$HOME/.piper-watchdog-slack-webhook"
if [ -f "$HOOK_FILE" ]; then
  WEBHOOK=$(tr -d '[:space:]' < "$HOOK_FILE")
  [ -n "$WEBHOOK" ] && curl -s -m 10 -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\":rotating_light: ${TITLE} — ${SUMMARY}\"}" "$WEBHOOK" >/dev/null 2>&1
fi
exit 0
