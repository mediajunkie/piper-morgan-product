#!/usr/bin/env bash
# cohort-position.sh — "the position, not just the move log" (PM, 2026-08-20; design pass in
# dev/active/chess-board-design-pass-cio-2026-08-20.md; PM ruled the three open questions in that
# doc on scope/audience/cadence — see the doc's header note / commit that shipped this script).
#
# WHAT THIS IS: one composed markdown table, one row per role, answering "what is everyone doing
# right now" without opening all 11 dev/active/{role}-carry-forward.md files by hand.
#
# SCOPE (PM-ruled): role-state, not work-item-state. One row per role. Human-legible markdown for
# BOTH agents and PM — no renderer required. Regenerate-on-read: this script is idempotent and has
# NO side effects beyond stdout (no writes, no commits, no push). A separate day-close step is
# expected to redirect this script's stdout to a file and commit that file — this script does not
# do that itself; see item 7 in the issue this shipped against.
#
#   Usage:  scripts/cohort-position.sh                       # prints to stdout
#           scripts/cohort-position.sh > dev/active/cohort-position.md   # caller redirects+commits
#
#   COHORT_POSITION_REGISTRY overrides the registry path (mirrors cohort-freeze-detect.sh's
#   DUTY_CYCLE_REGISTRY convention) — used by the test script to exercise a scratch registry
#   without ever touching the real dev/active/duty-cycle-registry.tsv.
#
# DATA SOURCES, AND WHY EACH WAS CHOSEN:
#   1. dev/active/duty-cycle-registry.tsv — the role roster. Read fresh every run (never hardcoded)
#      so the roster tracks reality as roles are added/parked.
#   2. dev/active/{role}-carry-forward.md — prose, read for a best-effort "current focus" one-liner.
#      Headers are NOT identical across roles (confirmed directly: cio dates its H1 title, exec/host/
#      ppm use a "**Label**: date" line, cxo uses YAML frontmatter with a machine-checkable
#      `last_updated:` key, docs/lead/web vary the label text again, comms/pa/arch bury the date in
#      a prose paragraph). Extraction below tolerates this by pattern-scanning rather than assuming
#      one schema — see extract_focus()/self_reported_date().
#   3. dev/heartbeats/YYYY-MM-DD/{role}.tsv — real per-role liveness data, read from the SAME
#      underlying files `scripts/cohort-freeze-detect.sh` consumes (not shelled out to that script —
#      it only prints a cohort-wide aggregate, never a per-role timestamp, and its own wall-clock
#      window + `git fetch` would break this script's idempotency for no benefit). Read from the
#      LOCAL working tree (not origin/main) — cheaper, no network dependency, but can be behind a
#      checkout that hasn't fetched; the footer note says so.
#      ⚠️ NOT the primary liveness signal — see item 5. `duty-cycle-heartbeat.sh` writes these
#      DELIBERATELY SPARSELY for busy roles ("the work commit already IS a heartbeat... busy agents
#      pay ~zero", its own header, refinement (a) / `--if-quiet`). Reading this alone, as v1 of this
#      script did, INVERTS the column: the busier a role is, the fewer heartbeat rows it has, the
#      staler it reads. Exec caught this same-day (2026-08-29) — cxo read 19 days stale from
#      heartbeat data alone while having committed 40 minutes earlier. Kept as one input among three
#      (item 5), never trusted alone again.
#   4. `git log -1 --format=%ct -- <path>` on the carry-forward file itself — real git-commit time,
#      used for the Stale? column (unchanged) and as one input to Last Active (item 5).
#   5. `git log origin/main --since="14 days ago"` scanned ONCE for all roles, matched per-role by
#      the cohort's own commit-subject convention (`role: ...` or `verb(role): ...` — confirmed
#      against real history: `stop(cxo):`, `mail(host):`, `hb(pa):`, `cio: ...`, etc.). This is the
#      PRIMARY signal per the heartbeat script's own design (item 3's caveat) — Last Active is the
#      MAX of items 3, 4, and this, never heartbeat-first. Disclosed limitation: this is a
#      convention, not a guarantee — a role's plain conventional-commit work with no role tag in the
#      subject (this script's own `feat(cohort-position): ...` commit, for instance) won't match, so
#      this can still under-report — far less severely than trusting heartbeat data alone, but not
#      perfectly. See role_last_commit_epoch()'s own comment for the same note in context.
#
# IDEMPOTENCY: no randomness, no directory-order dependence (roles sorted alphabetically), and
# deliberately NO "generated at HH:MM:SS" stamp in the output — a wall-clock line would make two
# back-to-back runs differ by construction and defeat the byte-identical test this script is held
# to. The only wall-clock-derived values are per-role AGE-IN-HOURS figures (integer hour buckets),
# which are stable across any two runs that don't straddle an hour boundary — an accepted, disclosed
# property of a staleness feature, not the kind of nondeterminism this requirement is warning about.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REG="${COHORT_POSITION_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"
CF_DIR="$REPO/dev/active"
HB_DIR="$REPO/dev/heartbeats"
NOW_EPOCH=$(date +%s)
STALE_THRESHOLD_S=$((48 * 3600))

if [ ! -r "$REG" ]; then
  echo "cohort-position: FAIL cannot read registry $REG" >&2
  exit 1
fi

# One git-log call for all 11 roles rather than 11 shell-outs; 14-day window bounds cost.
ROLE_COMMIT_LOG="$(git -C "$REPO" log origin/main --since="14 days ago" --format='%ct %s' 2>/dev/null)"

# ── helpers ──────────────────────────────────────────────────────────────────────────────────

fmt_epoch() {
  # epoch -> "YYYY-MM-DD HH:MM TZ", tolerant of BSD date (macOS) vs GNU date (Linux/CI).
  local e="$1"
  date -r "$e" "+%Y-%m-%d %H:%M %Z" 2>/dev/null || date -d "@$e" "+%Y-%m-%d %H:%M %Z" 2>/dev/null
}

parse_ts_epoch() {
  # "2026-08-29 16:37:14 PDT" (or similar, TZ abbrev ignored) -> epoch. Empty on failure.
  local ts="$1" dt
  dt="$(printf '%s' "$ts" | awk '{print $1" "$2}')"
  [ -z "$dt" ] && return 0
  date -j -f "%Y-%m-%d %H:%M:%S" "$dt" +%s 2>/dev/null || date -d "$dt" +%s 2>/dev/null
}

role_last_commit_epoch() {
  # Newest commit on origin/main whose subject is tagged for $1, by the cohort's own convention:
  # "role: ..." or "verb(role): ...". Bounded to a 14-day window for performance (a role silent
  # 14 real days is legitimately stale regardless). Prints an epoch, or nothing if no match.
  #
  # KNOWN LIMITATION, disclosed rather than hidden (Exec's finding, 2026-08-29): this is a
  # CONVENTION, not a guarantee. It catches every duty-cycle fire/mail/log commit observed across
  # the cohort's actual history, but a role's own plain conventional-commit work (e.g. this
  # script's own "feat(cohort-position): ..." / "fix(watchdog): ..." commits carry no role tag at
  # all) will not match. That means this signal can still UNDER-report a role's true activity —
  # just far less severely than reading heartbeat data alone, which is the bug this function fixes.
  local role="$1"
  printf '%s\n' "$ROLE_COMMIT_LOG" | awk -v role="$role" '
    {
      ts=$1; sub(/^[^ ]+ /, ""); subject=$0
      if (subject ~ ("^" role ":") || subject ~ ("\\(" role "\\):")) { print ts; exit }
    }
  '
}

role_last_heartbeat() {
  # Scans dev/heartbeats/*/{role}.tsv for the newest timestamp line for $1. Prints
  # "epoch<TAB>state" (epoch=0, state="" if nothing found — never fabricated).
  local role="$1"
  local best_epoch=0 best_state="" d f ts who state e
  if [ -d "$HB_DIR" ]; then
    for d in "$HB_DIR"/*/; do
      [ -d "$d" ] || continue
      f="${d}${role}.tsv"
      [ -f "$f" ] || continue
      while IFS=$'\t' read -r ts who state; do
        [ -z "${ts:-}" ] && continue
        e="$(parse_ts_epoch "$ts")"
        [ -z "${e:-}" ] && continue
        if [ "$e" -gt "$best_epoch" ] 2>/dev/null; then
          best_epoch="$e"
          best_state="${state:-}"
        fi
      done < "$f"
    done
  fi
  printf '%s\t%s\n' "$best_epoch" "$best_state"
}

extract_focus() {
  # Best-effort "current focus" one-liner: skips YAML frontmatter (if present) and the H1 title,
  # then returns the first "## " heading whose alnum content is long enough to be substantive
  # (filters trivial section labels like "## Cron"). Falls back to the first non-blank,
  # non-metadata bullet/paragraph line if no such heading exists in the scanned window. Prints
  # nothing (never fabricates) if the window is exhausted without a candidate.
  local file="$1"
  awk '
    BEGIN { infm=0; h1skip=0; fallback="" }
    NR==1 && $0 ~ /^---[ \t]*$/ { infm=1; next }
    infm==1 { if ($0 ~ /^---[ \t]*$/) { infm=0 }; next }
    !h1skip && $0 ~ /^# / { h1skip=1; next }
    /^##[ ]/ {
      line=$0
      sub(/^##+[ \t]*/, "", line)
      plain=line
      gsub(/[^A-Za-z0-9]/, "", plain)
      if (length(plain) >= 10) { print line; exit }
      next
    }
    fallback == "" && /^[ \t]*[-*][ ]/ && $0 !~ /^\*\*[A-Za-z][^*]*\*\*:/ {
      line=$0
      sub(/^[ \t]*[-*][ ]+/, "", line)
      if (length(line) >= 10) fallback=line
    }
    NR>=80 { if (fallback != "") print fallback; exit }
    END { if (fallback != "") print fallback }
  ' "$file"
}

self_reported_date() {
  # Best-effort self-reported date: prefers a machine-checkable YAML `last_updated:` frontmatter
  # key (cxo's pattern); else the first ISO date found in the first 20 lines. Tier-3 fallback only
  # (see main loop) — the real signal is the heartbeat/git-commit data, not this.
  local file="$1" fm
  fm=$(awk '
    NR==1 && /^---[ \t]*$/ { c=1; next }
    c==1 {
      if ($0 ~ /^---[ \t]*$/) { c=2; next }
      if ($0 ~ /^last_updated:[ \t]*/) {
        v=$0; sub(/^last_updated:[ \t]*/,"",v); gsub(/"/,"",v); print v; exit
      }
      next
    }
    c==2 { exit }
  ' "$file" 2>/dev/null)
  if [ -n "$fm" ]; then
    printf '%s\n' "$fm"
    return
  fi
  head -n 20 "$file" 2>/dev/null | grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' | head -n1
}

sanitize_cell() {
  # Collapse to one line, escape pipes so the markdown table doesn't break, truncate to 100 chars.
  local s="$1"
  s="$(printf '%s' "$s" | tr '\n\r\t' '   ' | sed 's/|/\\|/g')"
  # collapse runs of whitespace
  s="$(printf '%s' "$s" | awk '{$1=$1; print}')"
  if [ "${#s}" -gt 100 ]; then
    s="${s:0:97}..."
  fi
  printf '%s' "$s"
}

# ── read roster (registry order preserved on disk; we sort for output determinism) ─────────────

roster_rows=()
while IFS=$'\t' read -r role cron threshold wstart wend ffire asince state; do
  case "$role" in ''|'#'*|role) continue;; esac   # blank / comment / literal header row
  is_parked=0
  case "${state:-}" in parked*) is_parked=1;; esac
  roster_rows+=("${role}|${is_parked}")
done < "$REG"

if [ "${#roster_rows[@]}" -eq 0 ]; then
  echo "cohort-position: FAIL registry $REG contained no role rows" >&2
  exit 1
fi

sorted_rows="$(printf '%s\n' "${roster_rows[@]}" | sort)"

# ── build table ──────────────────────────────────────────────────────────────────────────────

echo "# Cohort Position"
echo
echo "One row per role — what's active, last real signal seen, whether the carry-forward itself"
echo "looks stale. Composed from \`dev/active/duty-cycle-registry.tsv\`, each role's"
echo "\`dev/active/{role}-carry-forward.md\`, and \`dev/heartbeats/\` (the same data"
echo "\`scripts/cohort-freeze-detect.sh\` reads, at per-role granularity it doesn't itself expose)."
echo "Regenerate with \`scripts/cohort-position.sh\` — it has no side effects; redirect its stdout"
echo "and commit that file if you want a dated snapshot."
echo
echo "| Role | Last Active | Current Focus | Stale? |"
echo "|---|---|---|---|"

while IFS='|' read -r role is_parked; do
  [ -z "$role" ] && continue

  cf_path="$CF_DIR/${role}-carry-forward.md"
  cf_exists=0
  [ -f "$cf_path" ] && cf_exists=1

  # -- heartbeat signal (deliberately SPARSE for active roles — see role_last_commit_epoch's
  #    header note. Never trust this alone: it is a fallback for QUIET fires, not a liveness feed) --
  hb_result="$(role_last_heartbeat "$role")"
  hb_epoch="${hb_result%%$'\t'*}"
  hb_state="${hb_result#*$'\t'}"

  # -- carry-forward file's own git-commit time (used for BOTH last-active AND Stale?) --
  cf_commit_epoch=""
  if [ "$cf_exists" -eq 1 ]; then
    cf_commit_epoch=$(git -C "$REPO" log -1 --format=%ct -- "dev/active/${role}-carry-forward.md" 2>/dev/null)
  fi

  # -- role-tagged commit signal (the PRIMARY liveness data per the heartbeat script's own design:
  #    "the work commit already IS a heartbeat" — duty-cycle-heartbeat.sh header, refinement (a)) --
  role_commit_epoch="$(role_last_commit_epoch "$role")"

  # -- Last Active cell: MAX of all three real signals, never heartbeat alone (2026-08-29 fix —
  #    Exec found the prior heartbeat-first ordering INVERTED the column: heartbeats are sparse
  #    BY DESIGN for busy roles, so the busier a role was, the staler it read. cxo measured 19
  #    days stale while having committed 40 minutes earlier) --
  best_epoch=0; best_label=""
  for pair in "${hb_epoch:-0}|heartbeat${hb_state:+: $hb_state}" \
              "${role_commit_epoch:-0}|commit (role-tagged, on origin/main)" \
              "${cf_commit_epoch:-0}|file commit (carry-forward's own last edit)"; do
    e="${pair%%|*}"; lbl="${pair#*|}"
    if [ -n "$e" ] && [ "$e" -gt "$best_epoch" ] 2>/dev/null; then
      best_epoch="$e"; best_label="$lbl"
    fi
  done

  if [ "$best_epoch" -gt 0 ]; then
    last_active="$(fmt_epoch "$best_epoch") ($best_label)"
  else
    sr_date=""
    [ "$cf_exists" -eq 1 ] && sr_date="$(self_reported_date "$cf_path")"
    if [ -n "$sr_date" ]; then
      last_active="~${sr_date} (self-reported in file text, unverified — no heartbeat, no git history)"
    else
      last_active="unknown (no heartbeat, no git history, no carry-forward file)"
    fi
  fi

  # -- Current Focus cell --
  if [ "$cf_exists" -eq 1 ]; then
    focus="$(extract_focus "$cf_path")"
    [ -z "$focus" ] && focus="(no substantive heading/bullet found in the scanned window — see file directly)"
  else
    focus="(no carry-forward file found for this role)"
  fi

  # -- Stale? cell: driven ONLY by the carry-forward file's own git-commit age, per spec --
  if [ "$is_parked" -eq 1 ]; then
    stale="parked"
  elif [ "$cf_exists" -ne 1 ]; then
    stale="n/a (no file)"
  elif [ -z "${cf_commit_epoch:-}" ]; then
    stale="unknown (file untracked in git)"
  else
    age_s=$(( NOW_EPOCH - cf_commit_epoch ))
    age_h=$(( age_s / 3600 ))
    if [ "$age_s" -gt "$STALE_THRESHOLD_S" ]; then
      stale="YES (${age_h}h)"
    else
      stale="no (${age_h}h)"
    fi
  fi

  role_cell="$(sanitize_cell "$role")"
  la_cell="$(sanitize_cell "$last_active")"
  focus_cell="$(sanitize_cell "$focus")"
  stale_cell="$(sanitize_cell "$stale")"

  echo "| $role_cell | $la_cell | $focus_cell | $stale_cell |"
done <<< "$sorted_rows"

echo
echo "---"
echo "Notes: \"Last Active\" is the MAX of three real signals — heartbeat data, a role-tagged commit"
echo "on \`origin/main\` (the primary signal; heartbeats are deliberately sparse for busy roles, see"
echo "the script header), and the carry-forward file's own last edit — never heartbeat alone."
echo "Heartbeat data itself is read from this checkout's LOCAL working tree (not fetched from"
echo "\`origin/main\`) — a checkout that hasn't fetched recently may under-report it; run"
echo "\`git fetch origin main\` first for the freshest cross-check. Role-tagged-commit attribution is"
echo "by commit-subject CONVENTION (\`role: ...\` / \`verb(role): ...\`), not a guarantee — a role's"
echo "untagged commits won't match. \"Current Focus\" is a best-effort extraction (first substantive"
echo "\`##\` heading, else first substantive bullet) — read the role's own carry-forward for anything"
echo "nuanced. \"Stale?\" reflects only the carry-forward FILE's own last git-commit age (>48h = YES),"
echo "independent of whether the role itself is alive — it can legitimately disagree with Last Active"
echo "for a role that's active but hasn't touched its own carry-forward file recently."

exit 0
