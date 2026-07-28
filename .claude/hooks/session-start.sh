#!/usr/bin/env bash
# session-start.sh — Enhanced SessionStart hook for Piper Morgan (#853)
#
# Performs four checks at agent session start:
#   1. Session log continuity (find today's log, warn if resuming)
#   2. Mailbox check (count unread messages)
#   3. Briefing freshness (warn if BRIEFING-CURRENT-STATE.md > 7 days old)
#   4. Role identity injection
#
# Token budget: Total stdout must stay under 500 characters.
# Safety: Must NEVER exit non-zero (exit 2 blocks agent start).

set -uo pipefail

# Project root — resolve relative to this script's location
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

output=""

# ─── 0. Mailbox manifest regeneration (deliver-mail b1) ─────────────────────
# Files in inbox/read are authoritative; MANIFEST.md is a derivative artifact.
# Regenerate quietly at session start so unread counts are accurate.
# Safety: --quiet suppresses per-file output; 2>/dev/null prevents stderr leak;
# script exits 0 on any error path so this never blocks session start.
if [ -x "$PROJECT_ROOT/scripts/regenerate-mailbox-manifests.py" ]; then
    # Only regenerate on main — the canonical home of mailbox MANIFESTs (they're committed there).
    # On a feature-branch worktree this regen just creates unstaged noise that breaks rebases (the
    # "git checkout -- mailboxes/ before every rebase" tax); mailbox writes go via the main-checkout
    # bridge, never on feature branches, so a worktree never needs to regenerate. Streamlining #1 (6/15).
    _cur_branch=$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
    if [ "$_cur_branch" = "main" ]; then
        "$PROJECT_ROOT/scripts/regenerate-mailbox-manifests.py" --quiet >/dev/null 2>&1 || true
    fi
fi

# ─── 1. Session Log Continuity ────────────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
LOG_DIR="$PROJECT_ROOT/dev/$YEAR/$MONTH/$DAY"

if [ -d "$LOG_DIR" ]; then
    # List today's session logs (any role). Agent should resume their own if listed.
    # Matches both formats (backward-compatible, same as section 6/7):
    #   New (2026-06-29+): YYYY-MM-DD-HHMM-{role}-code-log.md
    #   Old (pre-2026-06-29): YYYY-MM-DD-HHMM-{role}-code-opus-log.md (or -sonnet-/-haiku-)
    # #1153-adjacent fix (2026-07-03): this glob was missed in the 6/29 naming-convention
    # pass — it still required "-opus-log.md" so this signal silently stopped firing for
    # any new-format log. Section 6 got the fix; this one didn't.
    LOGS_TODAY=$(find "$LOG_DIR" -maxdepth 1 -name "*-log.md" -type f 2>/dev/null \
        -exec basename {} \; 2>/dev/null | tr '\n' ',' | sed 's/,$//;s/,/, /g')
    if [ -n "$LOGS_TODAY" ]; then
        output+="SESSION LOGS TODAY: $LOGS_TODAY — resume yours if listed."$'\n'
    fi
fi

# ─── 1b. Branch/Worktree Check (CXO gap, 2026-07-01) ─────────────────────────
# Backup-account sessions don't auto-create an ephemeral worktree — the agent
# lands directly on shared main. Surfaced when CXO's Jun 30 → Jul 1 session
# committed on main and picked up other agents' + PM's uncommitted state.
# Detection: a worktree checkout can never be on branch `main` (git refuses to
# check out a branch that's already checked out elsewhere, and main lives in
# the primary checkout) — so branch==main implies "this IS the main checkout."
# Detached-HEAD worktrees (e.g. Belt-4 spawn-fresh) report "HEAD", not "main",
# so they correctly don't trigger this.
CUR_BRANCH=$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
if [ "$CUR_BRANCH" = "main" ]; then
    output+="BRANCH: main (shared checkout, not a worktree) — substantive work needs a worktree (CLAUDE.md); mailbox/housekeeping-only is fine here."$'\n'
fi

# ─── 2. Mailbox Check (all role inboxes) ─────────────────────────────────────
MAILBOXES_DIR="$PROJECT_ROOT/mailboxes"
UNREAD_SUMMARY=""

if [ -d "$MAILBOXES_DIR" ]; then
    for inbox in "$MAILBOXES_DIR"/*/inbox; do
        [ -d "$inbox" ] || continue
        role=$(basename "$(dirname "$inbox")")
        count=$(find "$inbox" -maxdepth 1 -type f ! -name '.*' ! -name 'MANIFEST.md' 2>/dev/null | wc -l | tr -d ' ')
        if [ "$count" -gt 0 ]; then
            UNREAD_SUMMARY+="$role:$count "
        fi
    done
fi

if [ -n "$UNREAD_SUMMARY" ]; then
    output+="MAILBOXES WITH UNREAD: ${UNREAD_SUMMARY% }"$'\n'
else
    output+="MAILBOXES: all empty"$'\n'
fi

# ─── 3. Briefing Freshness ───────────────────────────────────────────────────
# Uses the file's last COMMIT date (git log), not filesystem mtime (PM-requested
# investigation, 2026-07-10, via Lead Dev — "agents keep telling PM this file is
# stale when it was recently updated"). Root cause: filesystem mtime is decoupled
# from content freshness in a multi-worktree environment. `git worktree add`
# stamps every checked-out file with a fresh "now" mtime regardless of when its
# content last actually changed, and a long-lived worktree's on-disk mtime for a
# file it hasn't happened to re-touch reflects whenever it was last checked out
# or synced — neither has anything to do with when the CONTENT was last updated
# on origin. git's commit date does, and needs no network call (walks local
# HEAD's already-known history — no `git fetch` added to keep this hook fast).
# This was one of at least two independent staleness-loop causes; the other
# (banner/footer/frontmatter date fields drifting out of sync with each other)
# is a doc-convention issue, not a code bug — flagged separately, not fixed here.
BRIEFING="$PROJECT_ROOT/docs/briefing/BRIEFING-CURRENT-STATE.md"

if [ -f "$BRIEFING" ]; then
    LAST_COMMIT_EPOCH=$(git -C "$PROJECT_ROOT" log -1 --format=%ct -- "$BRIEFING" 2>/dev/null)
    if [ -n "$LAST_COMMIT_EPOCH" ]; then
        NOW_EPOCH=$(date +%s)
        AGE_DAYS=$(( (NOW_EPOCH - LAST_COMMIT_EPOCH) / 86400 ))

        if [ "$AGE_DAYS" -gt 7 ]; then
            MOD_DATE=$(date -r "$LAST_COMMIT_EPOCH" +%Y-%m-%d 2>/dev/null || date -d "@$LAST_COMMIT_EPOCH" +%Y-%m-%d 2>/dev/null || echo "unknown")
            output+="BRIEFING: STALE ($AGE_DAYS days, last $MOD_DATE) → refresh via update-current-state skill"$'\n'
        fi
    fi
fi

# ─── 4. Cross-Pollination Brief ──────────────────────────────────────────────
# Two signals:
#   (a) Producer-side: brief age in days. STALE if Dispatch hasn't produced lately.
#       Uses git commit date, not filesystem mtime — same fix + same reasoning as
#       Section 3 (2026-07-10); mtime is decoupled from content freshness across
#       worktrees.
#   (b) Consumer-side: brief mtime vs most-recent session-log mtime. NEW if brief
#       was updated AFTER any role's most recent session log — i.e., new content
#       since the agent (any role) last sessioned. Per CIO scoping memo 2026-05-08
#       (`memo-cio-to-lead-cc-host-pm-exec-cross-pollination-brief-session-start-hook-scoping`).
#       Approximation: hook can't know which role is starting, so uses
#       most-recent-log-anywhere as a proxy for "since someone last sessioned."
#       This one stays on filesystem mtime deliberately — it's a same-worktree
#       RELATIVE ordering (is the brief newer than the newest local session log?),
#       not an absolute-age claim, so the cross-worktree mtime-drift problem
#       that broke (a) doesn't apply here.
#       #1153-adjacent fix (2026-07-10): the glob below required "*opus-log.md"
#       (pre-6/29 naming) — silently dead since the 6/29 rename to "*-code-log.md"
#       (Section 1 got this fix 7/3; this twin instance was missed then).
# Priority: NEW > STALE > available. NEW is more actionable for the consumer.
XPOLL_BRIEF="$PROJECT_ROOT/docs/briefs/cross-pollination/current.md"

if [ -f "$XPOLL_BRIEF" ]; then
    BRIEF_EPOCH=$(git -C "$PROJECT_ROOT" log -1 --format=%ct -- "$XPOLL_BRIEF" 2>/dev/null)
    if [ -n "$BRIEF_EPOCH" ]; then
        NOW_EPOCH=$(date +%s)
        BRIEF_AGE=$(( (NOW_EPOCH - BRIEF_EPOCH) / 86400 ))

        # Consumer-side: is any dev/ session log newer than the brief? Matches both
        # formats: new (*-code-log.md) and old (*-code-opus-log.md/-sonnet-), last
        # 30 days only (older logs aren't load-bearing for this signal).
        # Uses `find -newer` (mtime comparison inside find) + `head -1` to
        # short-circuit on the first hit, not a per-file `stat` subprocess loop —
        # with ~1,600+ matching session logs in this repo once the dead glob above
        # was fixed (2026-07-10) and started actually matching files, the old
        # per-file-stat loop added several real seconds to every session start
        # (measured: ~6.5s -> ~11s). Two `find` calls here cost ~0.07s combined.
        ANY_LOG=$(find "$PROJECT_ROOT/dev" -maxdepth 5 -name "*-log.md" -type f -mtime -30 2>/dev/null | head -1)
        NEWER_LOG=$(find "$PROJECT_ROOT/dev" -maxdepth 5 -name "*-log.md" -type f -newer "$XPOLL_BRIEF" -mtime -30 2>/dev/null | head -1)

        if [ -n "$ANY_LOG" ] && [ -z "$NEWER_LOG" ]; then
            output+="XPOLL BRIEF: NEW since last session"$'\n'
        elif [ "$BRIEF_AGE" -gt 2 ]; then
            output+="XPOLL BRIEF: STALE ($BRIEF_AGE days)"$'\n'
        else
            output+="XPOLL BRIEF: current.md available"$'\n'
        fi
    fi
else
    output+="XPOLL BRIEF: not found"$'\n'
fi

# ─── 4b. Weekly Docs Audit (PM-requested 2026-07-28) ─────────────────────────
# The FLY-AUDIT weekly docs audit issue is auto-generated Monday. PM asked for a
# START-routine reminder so it gets prioritized rather than drifting.
#
# Deliberately fires Mon-Thu, not Monday-only. PM's ask was "check if it's Monday"
# but a Monday-only reminder would not have caught the case that prompted this:
# the 2026-07-27 audit went unrun Monday and PM had to raise it Tuesday. Two of
# the last six weekly audits were never executed at all (#1402, #1049) — the
# failure mode is silent drift past Monday, so the reminder has to outlive Monday.
# Stops Thursday: past that the next Monday's audit is closer than the last one,
# and the correct move becomes close-as-superseded, not run-it-late.
#
# No network call — deliberately consistent with Sections 3/4, which avoid even a
# `git fetch` to keep session start fast. That means this cannot know whether the
# audit was already closed, so it is worded as a prompt to check, not an assertion
# that work is outstanding. Verifying is one `gh issue list` on the agent's side.
#
# Not role-gated: the hook cannot know which role is starting (see Section 4's
# note). Docs owns the audit, but cohort-wide visibility matches the existing
# BRIEFING-staleness norm in CLAUDE.md — any agent who notices may act.
DOW=$(date +%u)   # 1=Monday .. 7=Sunday
if [ "$DOW" -le 4 ]; then
    # Kept deliberately short: Section 2's mailbox line is variable-length and
    # grows with unread counts, and total stdout is budgeted at 500 chars. A
    # verbose reminder here can push the ROLE line off the end — measured at 495
    # chars on the day this was added. Check the issue with:
    #   gh issue list --label fly-audit --state open
    if [ "$DOW" -eq 1 ]; then
        output+="DOCS AUDIT: due today (Mon) — prioritize"$'\n'
    else
        output+="DOCS AUDIT: Mon's is $((DOW - 1))d old — prioritize if open"$'\n'
    fi
fi

# ─── 5. Role Identity ────────────────────────────────────────────────────────
# No default role — agent infers from PM assignment or existing session log.
# See CLAUDE.md: general-purpose agents use the `code` slug.
output+="ROLE: check PM assignment or today's session log (no default)"$'\n'

# ─── 6. Per-role briefing freshness ──────────────────────────────────────────
# Detect agent's role from today's session log filename slug, then check the
# corresponding BRIEFING-ESSENTIAL file's age. Warn if >14 days stale.
# Per PM 2026-05-12: 14 days exactly (limited bandwidth = shorter signal).
# Skipped slugs: eta (one-session role; not worth process), llm (legacy
# duplicate of LEAD-DEV; pending consolidation), bare code (no role).
# If multiple role logs exist today (rare), check each.
#
# Supports both filename formats (backward-compatible):
#   New (2026-06-29+): YYYY-MM-DD-HHMM-{role}-code-log.md
#   Old (pre-2026-06-29): YYYY-MM-DD-HHMM-{role}-code-opus-log.md (or -sonnet-)
if [ -d "$LOG_DIR" ]; then
    SEEN_SLUGS=""
    for log in "$LOG_DIR"/*-log.md; do
        [ -f "$log" ] || continue
        # Extract slug from either old or new format.
        # Robust slug guard (#1153): require the exact digit YYYY-MM-DD-HHMM- prefix
        # before the positional strip. The old code blindly stripped ????-??-??-????-,
        # so a non-standard name like 2026-06-04-code-opus-log.md (no HHMM) had its
        # 4-char role "code" consumed as the HHMM field → slug="opus-log.md" → a
        # malformed delta-opus-log.md-*.md file. Skip non-conforming names instead.
        base=$(basename "$log")
        case "$base" in
            [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]-*-log.md) ;;
            *) continue ;;
        esac
        stripped=${base#????-??-??-????-}
        stripped=${stripped%-opus-log.md}   # old format: strip -opus-log.md
        stripped=${stripped%-sonnet-log.md} # old format: strip -sonnet-log.md
        stripped=${stripped%-haiku-log.md}  # old format: strip -haiku-log.md
        stripped=${stripped%-log.md}        # new format: strip -log.md (no-op for old)
        slug=${stripped%-code}
        # Dedup
        case " $SEEN_SLUGS " in *" $slug "*) continue;; esac
        SEEN_SLUGS="$SEEN_SLUGS $slug"
        # Map slug → briefing filename (bash 3.2 compatible; no assoc array).
        # Skipped: eta (one-session role), llm (legacy duplicate of LEAD-DEV),
        # code (no-role general-purpose).
        case "$slug" in
            lead)  briefing_name="BRIEFING-ESSENTIAL-LEAD-DEV.md" ;;
            docs)  briefing_name="BRIEFING-ESSENTIAL-DOCS.md" ;;
            host)  briefing_name="BRIEFING-ESSENTIAL-HOST.md" ;;
            cio)   briefing_name="BRIEFING-ESSENTIAL-CIO.md" ;;
            cxo)   briefing_name="BRIEFING-ESSENTIAL-CXO.md" ;;
            ppm)   briefing_name="BRIEFING-ESSENTIAL-PPM.md" ;;
            exec)  briefing_name="BRIEFING-ESSENTIAL-CHIEF-STAFF.md" ;;
            comms) briefing_name="BRIEFING-ESSENTIAL-COMMS.md" ;;
            arch)  briefing_name="BRIEFING-ESSENTIAL-ARCHITECT.md" ;;
            pa)    briefing_name="BRIEFING-piper-alpha.md" ;;
            prog)  briefing_name="BRIEFING-ESSENTIAL-AGENT.md" ;;
            *)     continue ;;
        esac
        briefing_path="$PROJECT_ROOT/docs/briefing/$briefing_name"
        [ -f "$briefing_path" ] || continue
        # git commit date, not filesystem mtime — same fix + reasoning as Section 3
        # (2026-07-10). Loop bound to today's LOG_DIR only (~10-14 roles), so no
        # performance concern here the way Section 4's dev/-wide loop had.
        B_EPOCH=$(git -C "$PROJECT_ROOT" log -1 --format=%ct -- "$briefing_path" 2>/dev/null)
        [ -n "$B_EPOCH" ] || continue
        B_AGE=$(( ($(date +%s) - B_EPOCH) / 86400 ))
        if [ "$B_AGE" -gt 14 ]; then
            output+="ROLE BRIEFING ($slug): STALE ($B_AGE days) — $briefing_name"$'\n'
        fi
    done
fi

# ─── 7. Delta-since-last-session signal (MEM-975) ────────────────────────────
# Generate a "delta since last session" file for the role(s) opening today,
# and emit a one-line signal pointing at it. Per MEM-975 + CIO May 26 design
# (dev/active/mem-975-delta-generator-design.md). The script computes detail;
# the hook adds ~50 tokens of signal.
#
# Role detection: reuse SEEN_SLUGS from section 6 (today's logs). If no logs
# today, no signal emitted (script not invoked).
#
# Safety: script wrapped in || true; output captured via $(...); failures
# don't block session start.
DELTA_SCRIPT="$PROJECT_ROOT/scripts/generate-delta.py"
if [ -x "$DELTA_SCRIPT" ] && [ -n "${SEEN_SLUGS// /}" ]; then
    for slug in $SEEN_SLUGS; do
        # Skip slugs we don't expect to track deltas for
        case "$slug" in
            code|eta|llm) continue ;;
        esac
        # Invoke script; capture signal line; tolerate failures silently.
        delta_signal=$("$DELTA_SCRIPT" --role "$slug" 2>/dev/null || true)
        if [ -n "$delta_signal" ]; then
            output+="$delta_signal"$'\n'
        fi
    done
fi

# ─── Output ───────────────────────────────────────────────────────────────────
if [ -n "$output" ]; then
    # Truncate to stay under 500 chars
    if [ ${#output} -gt 490 ]; then
        output="${output:0:480}... (truncated)"
    fi
    echo "$output"
fi

exit 0
