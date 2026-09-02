#!/usr/bin/env bash
# aging-standing-items.sh — catches items silently deferred inside a standing-items file
# WITHOUT anyone deciding to defer them, and reports honestly on how much of the
# population it could actually read.
#
# THE FAILURE THIS CATCHES (and the one it does NOT catch — read this before extending)
# ---------------------------------------------------------------------------------
# CLAUDE.md has a whole section ("Deferring unblocked work requires a NAMED TRIGGER")
# against silent deprioritization, and it keeps getting violated anyway — not because
# the rule is worded badly, but because it depends on the deferring agent noticing its
# OWN deferral and self-reporting it. That is the same structural gap this cohort has
# already fixed elsewhere with an external, mechanical check instead of a prose rule.
# Real instance: three CIO items sat in dev/active/cio-standing-items.md for 3.5 months,
# genuinely unblocked, never surfaced to PM — found only because PM happened to ask
# "what are you postponing." Luck, not process. This script is the process.
#
# WHY THIS IS NOT check-refresh-promises.py --state-files
# ---------------------------------------------------------------------------------
# That checker asks "is the WHOLE FILE fresh" via frontmatter (currency_claim /
# max_age_days / last_updated). A file can pass that check every single fire — rewritten
# today, last_updated today — while ONE LINE inside it sits completely unchanged since
# May, because "rewriting the file" just means copying the old line forward verbatim.
# File-level freshness and item-level staleness are orthogonal. This script measures the
# item, not the file, and does not touch --state-files or its frontmatter contract at all.
#
# WHAT COUNTS AS "AGING"
# ---------------------------------------------------------------------------------
# A table row OR an inline-bold-labeled item (see v1.1 note below) that (a) carries a
# parseable per-item date roughly >= AGE_THRESHOLD_DAYS old, AND (b) is not blocked — by
# either a blocking-language signal (Pending PM, waiting on, gated on, concurrence,
# trigger-bound, Watch, ...) anywhere in its own text, OR a non-empty "Blocked on"-shaped
# table column (v1.1, see below). That combination is exactly the shape of a
# silently-deferred item: no one is watching it, and no one decided to defer it either —
# it just stopped getting looked at.
#
# v1.1 (2026-08-31, same-day fixes from real first-use — both found by roles adopting the
# convention hours after it shipped, not by further self-testing):
#   1. STRUCTURAL BLOCKER COLUMN (CXO's finding). CXO's table has a literal "Blocked on"
#      column plus a "Recheck trigger" column — 2 of the 4 rows the checker flagged as
#      "aging, no blocking language found" were rows where the blocker was ONLY expressed
#      structurally ("Blocked on: PPM picking a slot"), never repeated as prose the phrase
#      list could match. A 50% false-positive rate on the very first adopting file would
#      have trained people to skim the report before it had a chance to earn trust — the
#      same credibility argument as the freeze-watchdog belt. Fix: any column whose header
#      contains "blocked" is now checked directly — a non-empty cell there is a blocker,
#      full stop, regardless of wording. Cheaper and more robust than growing the phrase
#      list indefinitely, and it rewards structure over incantation.
#   2. INLINE BOLD-LABEL DATES (Web's finding). The cohort broadcast said to date items
#      "the way you'd date a diary entry" — several roles (docs, and Web's own first
#      attempt) did exactly that: `**Added**: 2026-08-29` as a prose line under a `##`/`###`
#      heading, not a markdown table at all. The original parser only ever looked at table
#      rows and had zero path for this shape — a role could comply with the broadcast's own
#      words and still be invisible to the checker. Fix: a line matching
#      `**Added|Filed|Noted|Started**: <date>` under a heading is now a recognized item,
#      using the heading text as the description and a bounded look-ahead (to the next
#      heading, capped at 20 lines) for blocking language in the surrounding prose — a bold
#      label and its own blocker phrase are rarely on the same line.
#
# REAL, LOAD-BEARING VARIANCE ACROSS THE ACTUAL CORPUS (found before writing this parser
# — see the session's own report for the full sampling; summarized here so the next
# person extending this script doesn't have to re-derive it):
#   - host-standing-items.md is formally RETIRED via YAML frontmatter (`retired: <date>`
#     + `retirement_reason:`) — its function moved to the carry-forward. Skip entirely;
#     this is a deliberate, legitimate state, not a coverage gap.
#   - Per-item date columns are NOT uniformly named. Real headers seen: "Filed" (cio),
#     "Started" (cio's own Active table — same file, different table!), "Noted" (pa).
#     Some tables have NO date column at all (comms, cxo, ppm) — Item/Status/Gate shaped,
#     nothing dated per row. Some files aren't tabular at all (arch, docs, lead, web) —
#     bullet/checklist items with dates embedded in prose, not a parseable column.
#   - A single date CELL can carry more than one date ("May 11 (orig.), reverified twice
#     Aug 23") — this script takes the LATEST date found in the cell as the row's last-
#     touched date, on the theory that a cited reverification is a real touch and should
#     reset the clock, not just the original filing date.
#   - "Resolved"-shaped tables/sections (column named "Resolved", or a heading containing
#     "resolved"/"closed") are excluded from the aging population entirely — those rows
#     are already closed, and their date is a close date, not a silent-aging signal.
#
# WHAT THIS SCRIPT DELIBERATELY DOES NOT DO
# ---------------------------------------------------------------------------------
#   - Does not touch check-refresh-promises.py or its --state-files mode. Different
#     question, different substrate rule (file-level vs item-level).
#   - Does not invent a new convention roles must adopt to become parseable. A file with
#     no per-item date column is reported as an honest COVERAGE GAP, not silently
#     dropped and not "fixed" by guessing a convention here.
#   - Never writes anything. Read-only. Exit 0 always — this is advisory, like every
#     other checker in this family; it surfaces candidates for a human (PM) to judge,
#     it does not itself decide anything is wrong.
#
# DENOMINATOR HONESTY (m-44: "Clear" Is Not a Measurement)
# ---------------------------------------------------------------------------------
# A run that finds zero AGING items is not a claim that the cohort has no silently-aging
# work — most of the corpus (files with no parseable per-item date column) is currently
# invisible to this script, and the coverage block says so explicitly, every run, by
# name. See check-refresh-promises.py's own "── coverage ──" block for the discipline
# this follows: the denominator is the population that COULD be checked, and the report
# says exactly how much of the real population that denominator actually is.

set -uo pipefail
shopt -s nullglob

# ── tunable ─────────────────────────────────────────────────────────────────────
AGE_THRESHOLD_DAYS=21

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY_EPOCH=$(date +%s)
TODAY_YEAR=$(date +%Y)

# Blocking-language phrases (case-insensitive). Multi-word phrases are substring-matched;
# "watch" alone is whole-word-matched so it doesn't fire on unrelated text, and "blocked
# on" (not bare "blocked") avoids a false hit on "unblocked".
BLOCK_PHRASES=(
    "pending pm"
    "pending external"
    "trigger-bound"
    "blocked on"
    "waiting on"
    "concurrence"
    "gated on"
    "awaiting"
    "hold for"
    "recheck trigger"
    "not mine to drive"
)

is_blocked() {
    local t="$1" p
    for p in "${BLOCK_PHRASES[@]}"; do
        grep -qi -- "$p" <<<"$t" && return 0
    done
    grep -qiw "watch" <<<"$t" && return 0
    return 1
}

# Extract the LATEST date found in a cell's text, as epoch seconds. Empty output = no
# parseable date in this cell. Handles ISO (2026-06-07) and "Month Day" (May 9, Aug 23,
# August 23rd) forms; the latter is assumed to be TODAY_YEAR, rolled back one year if
# that would land in the future (defends against Jan/Feb cells read late in a year).
extract_latest_epoch() {
    local text="$1" best="" tok ep mon day mon3 cand_year

    while IFS= read -r tok; do
        [ -z "$tok" ] && continue
        ep=$(date -j -f "%Y-%m-%d" "$tok" +%s 2>/dev/null) || continue
        if [ -z "$best" ] || [ "$ep" -gt "$best" ]; then best="$ep"; fi
    done < <(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' <<<"$text")

    while IFS= read -r tok; do
        [ -z "$tok" ] && continue
        mon=$(awk '{print $1}' <<<"$tok")
        day=$(awk '{print $2}' <<<"$tok" | grep -oE '[0-9]+')
        [ -z "$day" ] && continue
        mon3="$(echo "${mon:0:3}" | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}')"
        cand_year="$TODAY_YEAR"
        ep=$(date -j -f "%b %d %Y" "$mon3 $day $cand_year" +%s 2>/dev/null) || continue
        if [ "$ep" -gt "$TODAY_EPOCH" ]; then
            cand_year=$((TODAY_YEAR - 1))
            ep=$(date -j -f "%b %d %Y" "$mon3 $day $cand_year" +%s 2>/dev/null) || continue
        fi
        if [ -z "$best" ] || [ "$ep" -gt "$best" ]; then best="$ep"; fi
    done < <(grep -oE '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-zA-Z]*\.?[[:space:]]+[0-9]{1,2}(st|nd|rd|th)?' <<<"$text")

    echo "$best"
}

# v1.2 (2026-09-02, CXO's "stale-blocker-rot" finding — 5 real instances in her own tracker
# within 36 hours). A THIRD failure mechanism, distinct from both silent deferral (what the rest
# of this script catches) and misfiling: a row's stated blocker CLEARS, but the row itself is
# never updated, so it goes on looking correctly-parked while being wrong. This script's own
# is_blocked()/BLOCKED_IDX logic is exactly what makes such a row invisible to the aging check —
# a recently-dated, blocker-stated row is precisely what HEALTHY looks like. The check is correct
# and the row is still wrong; a different mechanism is needed, not a wider aging net.
#
# Mechanical half only (CXO's own caveat: this "won't catch person-named blockers... those need
# the discipline change, not more tooling"): when a row's blocking text/column cites a GitHub
# issue (`#NNNN`), check whether that issue is closed. A closed #NNNN is checkable in one
# `gh issue view` call; a blocker like "waiting on PPM" is not, and this script doesn't guess.
#
# Cached per run (bash 3.2 has no associative arrays — macOS ships 3.2, see the mapfile note
# above) so a #NNNN cited on multiple rows costs one `gh` call, not N. `gh` unavailable/failed
# lookup is treated as "unknown," never as "closed" — a failed check must never manufacture a
# false STALE-BLOCKER flag.
ISSUE_STATE_CACHE=""

issue_num_in() {
    grep -oE '#[0-9]+' <<<"$1" | head -1 | tr -d '#'
}

issue_is_closed() {
    local num="$1" cached state
    cached="$(grep -m1 "^${num}|" <<<"$ISSUE_STATE_CACHE" 2>/dev/null)"
    if [ -n "$cached" ]; then
        state="${cached#*|}"
    else
        state="$(gh issue view "$num" --json state -q .state 2>/dev/null)"
        ISSUE_STATE_CACHE="${ISSUE_STATE_CACHE}${num}|${state}"$'\n'
    fi
    [ "$state" = "CLOSED" ]
}

# Split a markdown table row on '|', trimming each cell and dropping the empty
# leading/trailing element a leading/trailing pipe produces. Populates ROW_CELLS.
split_row() {
    local line="$1"
    line="${line#|}"
    line="${line%|}"
    IFS='|' read -ra ROW_CELLS <<<"$line"
    local i
    for i in "${!ROW_CELLS[@]}"; do
        ROW_CELLS[$i]="$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"${ROW_CELLS[$i]}")"
    done
}

# Reads the confirmed header row into DATE_IDX / ITEM_IDX / NUM_IDX / SKIP_TABLE.
# SKIP_TABLE=1 means: this table is a closed/resolved ledger (by column name) — never
# part of the aging population regardless of what dates it carries.
parse_header() {
    split_row "$1"
    DATE_IDX=-1
    ITEM_IDX=-1
    NUM_IDX=-1
    BLOCKED_IDX=-1
    SKIP_TABLE=0
    local i cell lc
    for i in "${!ROW_CELLS[@]}"; do
        cell="${ROW_CELLS[$i]}"
        lc="$(tr '[:upper:]' '[:lower:]' <<<"$cell")"
        case "$lc" in
            filed | started | noted | date) DATE_IDX=$i ;;
            resolved) SKIP_TABLE=1 ;;
            item | topic) [ "$ITEM_IDX" -eq -1 ] && ITEM_IDX=$i ;;
            "#") NUM_IDX=$i ;;
            *blocked*) BLOCKED_IDX=$i ;;
        esac
    done
    if [ "$ITEM_IDX" -eq -1 ]; then
        if [ "${#ROW_CELLS[@]}" -gt 1 ]; then ITEM_IDX=1; else ITEM_IDX=0; fi
    fi
    if grep -qiE 'resolved|closed' <<<"$heading"; then
        SKIP_TABLE=1
    fi
}

process_row() {
    local line="$1"
    split_row "$line"
    [ "$SKIP_TABLE" -eq 1 ] && return
    [ "$DATE_IDX" -eq -1 ] && return
    [ "$DATE_IDX" -ge "${#ROW_CELLS[@]}" ] && return

    local date_cell="${ROW_CELLS[$DATE_IDX]}"
    local item_cell=""
    [ "$ITEM_IDX" -lt "${#ROW_CELLS[@]}" ] && item_cell="${ROW_CELLS[$ITEM_IDX]}"
    # placeholder rows like "| (none currently) | | | |" — both the item and date
    # slots are blank; nothing to examine.
    if [ -z "$date_cell" ] && [ -z "$item_cell" ]; then return; fi

    ROWS_EXAMINED=$((ROWS_EXAMINED + 1))

    # Structural blocker: a non-empty "Blocked on"-shaped column beats phrase-matching —
    # CXO's 2026-08-31 finding, real same-day use: 2 of 4 flags on the first adopting file
    # were false positives because the blocker lived in a dedicated column ("Blocked on: PPM
    # picking a slot"), not repeated as prose the phrase list could match. A structured
    # column is a stronger, cheaper signal than growing the phrase list indefinitely.
    local blocked_cell=""
    if [ "$BLOCKED_IDX" -ge 0 ] && [ "$BLOCKED_IDX" -lt "${#ROW_CELLS[@]}" ]; then
        blocked_cell="${ROW_CELLS[$BLOCKED_IDX]}"
    fi
    local is_row_blocked=0
    if is_blocked "$line" || [ -n "$blocked_cell" ]; then
        is_row_blocked=1
    fi

    # v1.2 stale-blocker-rot check — deliberately runs BEFORE the age-threshold check below and
    # regardless of it. CXO's real instances were RECENTLY dated rows (a blocker that cleared
    # hours or days ago, not weeks) — gating this behind AGE_THRESHOLD_DAYS would silently
    # exclude exactly the rows this check exists to catch. Only fires on an otherwise-blocked
    # row whose blocker text/column names a checkable #NNNN.
    if [ "$is_row_blocked" -eq 1 ]; then
        local blocker_text="${blocked_cell:-$line}" issue_num
        issue_num="$(issue_num_in "$blocker_text")"
        if [ -n "$issue_num" ] && issue_is_closed "$issue_num"; then
            ROWS_STALE_BLOCKER=$((ROWS_STALE_BLOCKER + 1))
            local sb_num_cell="" sb_header="$ROLE" sb_desc="$item_cell"
            if [ "$NUM_IDX" -ge 0 ] && [ "$NUM_IDX" -lt "${#ROW_CELLS[@]}" ]; then
                sb_num_cell="${ROW_CELLS[$NUM_IDX]}"
            fi
            [ -n "$sb_num_cell" ] && sb_header="$ROLE #$sb_num_cell"
            [ "${#sb_desc}" -gt 70 ] && sb_desc="${sb_desc:0:67}..."
            printf 'STALE-BLOCKER: %s — %s (blocker cites #%s, which is CLOSED — row may be stale)\n' \
                "$sb_header" "$sb_desc" "$issue_num"
        fi
    fi

    local epoch
    epoch="$(extract_latest_epoch "$date_cell")"
    if [ -z "$epoch" ]; then
        ROWS_UNPARSEABLE=$((ROWS_UNPARSEABLE + 1))
        return
    fi

    local age_days=$(((TODAY_EPOCH - epoch) / 86400))
    [ "$age_days" -lt "$AGE_THRESHOLD_DAYS" ] && return

    if [ "$is_row_blocked" -eq 1 ]; then
        ROWS_BLOCKED=$((ROWS_BLOCKED + 1))
        return
    fi

    ROWS_AGING=$((ROWS_AGING + 1))
    local num_cell=""
    if [ "$NUM_IDX" -ge 0 ] && [ "$NUM_IDX" -lt "${#ROW_CELLS[@]}" ]; then
        num_cell="${ROW_CELLS[$NUM_IDX]}"
    fi
    local header="$ROLE"
    [ -n "$num_cell" ] && header="$ROLE #$num_cell"
    local desc="$item_cell"
    if [ "${#desc}" -gt 70 ]; then desc="${desc:0:67}..."; fi

    printf 'AGING: %s — %s (filed %s, %s days old)\n' "$header" "$desc" "$date_cell" "$age_days"
}

# ── discovery ───────────────────────────────────────────────────────────────────
FILES=("$ROOT"/dev/active/*-standing-items.md)
TOTAL_FILES=${#FILES[@]}
RETIRED_ROLES=()
NO_DATE_COL_ROLES=()
TOTAL_ROWS_EXAMINED=0
TOTAL_AGING=0
TOTAL_BLOCKED=0
TOTAL_UNPARSEABLE=0
TOTAL_STALE_BLOCKER=0

echo "── aging-standing-items scan (threshold: ${AGE_THRESHOLD_DAYS}d) ──────────────────────"
AGING_OUTPUT="$(mktemp)"
trap 'rm -f "$AGING_OUTPUT"' EXIT

for f in "${FILES[@]}"; do
    ROLE="$(basename "$f" | sed 's/-standing-items\.md$//')"

    # RETIRED check: frontmatter `retired:` key near the top of the file. A retired
    # file has deliberately migrated its function elsewhere — skip entirely, not a gap.
    if sed -n '1,15p' "$f" | grep -qE '^retired:'; then
        RETIRED_ROLES+=("$ROLE")
        continue
    fi

    heading=""
    table_state=0 # 0=none, 1=saw candidate header (awaiting separator), 2=in table body
    header_line=""
    DATE_IDX=-1
    ITEM_IDX=-1
    NUM_IDX=-1
    BLOCKED_IDX=-1
    SKIP_TABLE=0
    ROWS_EXAMINED=0
    ROWS_AGING=0
    ROWS_BLOCKED=0
    ROWS_UNPARSEABLE=0
    ROWS_STALE_BLOCKER=0
    heading_dated=0 # guards against double-processing an inline label under the same heading

    # mapfile (not the old streaming `while read`) so the inline-label path below can look
    # AHEAD to the end of the current heading's section for blocking language — a bold-label
    # date and its own blocker phrase are rarely on the same line (2026-08-31 finding: Web's
    # broadcast said "date it like a diary entry," several roles did exactly that in prose
    # under a heading, not a table — the checker had no path for that shape at all until now).
    # Portable bash-3.2 equivalent of `mapfile -t` (macOS ships 3.2; no mapfile builtin).
    FLINES=()
    while IFS= read -r fl || [ -n "$fl" ]; do FLINES+=("$fl"); done <"$f"
    NLINES=${#FLINES[@]}
    idx=0
    while [ "$idx" -lt "$NLINES" ]; do
        raw_line="${FLINES[$idx]}"
        trimmed="$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"$raw_line")"

        if [[ "$trimmed" =~ ^#+[[:space:]] ]]; then
            heading="$trimmed"
            table_state=0
            heading_dated=0
            idx=$((idx + 1))
            continue
        fi

        is_pipe=0
        [[ "$trimmed" == \|* ]] && is_pipe=1

        case "$table_state" in
            0)
                if [ "$is_pipe" -eq 1 ]; then
                    header_line="$trimmed"
                    table_state=1
                elif [ "$heading_dated" -eq 0 ] && [[ "$trimmed" =~ ^\*\*(Added|Filed|Noted|Started)\*\*:[[:space:]]*(.+)$ ]]; then
                    inline_date_text="${BASH_REMATCH[2]}"
                    inline_epoch="$(extract_latest_epoch "$inline_date_text")"
                    if [ -n "$inline_epoch" ]; then
                        heading_dated=1
                        ROWS_EXAMINED=$((ROWS_EXAMINED + 1))
                        lookahead_text="$trimmed"
                        j=$((idx + 1))
                        window_end=$((idx + 21))
                        while [ "$j" -lt "$NLINES" ] && [ "$j" -lt "$window_end" ]; do
                            ntrim="$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<<"${FLINES[$j]}")"
                            [[ "$ntrim" =~ ^#+[[:space:]] ]] && break
                            lookahead_text="$lookahead_text"$'\n'"$ntrim"
                            j=$((j + 1))
                        done
                        inline_age_days=$(((TODAY_EPOCH - inline_epoch) / 86400))
                        if [ "$inline_age_days" -ge "$AGE_THRESHOLD_DAYS" ]; then
                            if is_blocked "$lookahead_text"; then
                                ROWS_BLOCKED=$((ROWS_BLOCKED + 1))
                            else
                                ROWS_AGING=$((ROWS_AGING + 1))
                                desc="$(sed -E 's/^#+[[:space:]]*//' <<<"$heading")"
                                if [ "${#desc}" -gt 70 ]; then desc="${desc:0:67}..."; fi
                                printf 'AGING: %s — %s (filed %s, %s days old)\n' "$ROLE" "$desc" "$inline_date_text" "$inline_age_days" >>"$AGING_OUTPUT"
                            fi
                        fi
                    fi
                fi
                ;;
            1)
                if [ "$is_pipe" -eq 1 ] && [[ "$trimmed" =~ ^\|[[:space:]:*-]+\|.*$ ]]; then
                    parse_header "$header_line"
                    table_state=2
                else
                    # header_line was a false alarm (no separator followed) — reset,
                    # and let the current line start a fresh candidate if it's a pipe line.
                    table_state=0
                    if [ "$is_pipe" -eq 1 ]; then
                        header_line="$trimmed"
                        table_state=1
                    fi
                fi
                ;;
            2)
                if [ "$is_pipe" -eq 1 ]; then
                    process_row "$trimmed" >>"$AGING_OUTPUT"
                else
                    table_state=0
                fi
                ;;
        esac
        idx=$((idx + 1))
    done

    TOTAL_ROWS_EXAMINED=$((TOTAL_ROWS_EXAMINED + ROWS_EXAMINED))
    TOTAL_AGING=$((TOTAL_AGING + ROWS_AGING))
    TOTAL_BLOCKED=$((TOTAL_BLOCKED + ROWS_BLOCKED))
    TOTAL_UNPARSEABLE=$((TOTAL_UNPARSEABLE + ROWS_UNPARSEABLE))
    TOTAL_STALE_BLOCKER=$((TOTAL_STALE_BLOCKER + ROWS_STALE_BLOCKER))

    if [ "$ROWS_EXAMINED" -eq 0 ]; then
        NO_DATE_COL_ROLES+=("$ROLE")
    fi
done

if [ -s "$AGING_OUTPUT" ]; then
    cat "$AGING_OUTPUT"
else
    echo "(none found above the threshold, within the population this script can read — see coverage below)"
fi

echo
echo "── coverage ─────────────────────────────────────────────────────────────────"
echo "standing-items files found: $TOTAL_FILES"
echo "  retired (skipped deliberately — not a gap): ${#RETIRED_ROLES[@]}"
for r in "${RETIRED_ROLES[@]:-}"; do [ -n "$r" ] && echo "    · $r"; done
echo "  no parseable per-item date column at all (COVERAGE GAP): ${#NO_DATE_COL_ROLES[@]}"
for r in "${NO_DATE_COL_ROLES[@]:-}"; do [ -n "$r" ] && echo "    · $r"; done
echo
echo "rows examined, across roles WITH a parseable date column: $TOTAL_ROWS_EXAMINED"
echo "  flagged AGING (>= ${AGE_THRESHOLD_DAYS}d old, no blocking language found): $TOTAL_AGING"
echo "  correctly excluded — blocking language present (filter is discriminating, not blanket): $TOTAL_BLOCKED"
echo "  unparseable date text within an otherwise-recognized column: $TOTAL_UNPARSEABLE"
echo "  of the blocked rows above, flagged STALE-BLOCKER (blocker cites a closed #NNNN): $TOTAL_STALE_BLOCKER"
echo "    coverage note: only checks rows whose blocker cites a #NNNN — a person-named blocker"
echo "    ('waiting on PPM') is not mechanically checkable and is never flagged here (CXO's own"
echo "    caveat: that class needs a discipline change, not more tooling)."
echo
CHECKABLE=$((TOTAL_FILES - ${#RETIRED_ROLES[@]} - ${#NO_DATE_COL_ROLES[@]}))
echo "Only $CHECKABLE of $TOTAL_FILES standing-items files have any per-item date this script"
echo "can currently read. A clean run above is NOT a claim that the other ${#NO_DATE_COL_ROLES[@]} files"
echo "carry no silently-aging items — it means this script cannot see inside them yet. Read-only,"
echo "advisory: this surfaces candidates for a human to judge, it does not decide anything by itself."

exit 0
