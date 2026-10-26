#!/usr/bin/env bash
# briefing-pointer-check.sh — does each role briefing carry the pointers it is meant to carry?
#
# Why: HOST's 10-26 role-health audit (#2179, finding 2) found every briefing commit-fresh and
# content-stale. A `git log -1` date can't see that: a one-character edit makes it fresh. This reads
# the content instead. For each role briefing, it reports which of the expected pointers it names,
# and prints the commit date beside them so the two readings can be compared.
#
# Pointers (Exec's #2179 disposition, 10-26): the production map, the Readiness lane, #2157 (the
# restore-drill proofs), promises.yaml, ESSENCE v1.1. Override with POINTERS="label=regex;..." for a
# later list. A match is a name in the text, not proof the paragraph around it is right; read the
# briefing for that.
#
# Usage:  scripts/briefing-pointer-check.sh            (all role briefings)
#         scripts/briefing-pointer-check.sh CIO HOST   (briefings whose file name contains these)
# Exit:   0 when every briefing read carries every pointer, 1 when any is missing, 2 on a pattern
#         error, 3 when no briefing was found (nothing measured).
# Owner: CIO. Review: 2026-11-30.

cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 3
DEFAULT_POINTERS='production map=production-map\.html|production map;Readiness=Readiness;#2157=#?2157\b;promises.yaml=promises\.yaml;ESSENCE v1.1=ESSENCE[^.]{0,40}v?1\.1'
POINTERS="${POINTERS:-$DEFAULT_POINTERS}"

files=()
for f in docs/briefing/BRIEFING-ESSENTIAL-*.md docs/briefing/BRIEFING-piper-alpha.md; do
    [ -f "$f" ] || continue
    if [ $# -gt 0 ]; then
        keep=0
        for a in "$@"; do case "$f" in *"$a"*) keep=1 ;; esac; done
        [ $keep -eq 1 ] || continue
    fi
    files+=("$f")
done
[ ${#files[@]} -eq 0 ] && { echo "briefing-pointer-check: no briefing matched; nothing measured" >&2; exit 3; }

IFS=';' read -r -a pairs <<<"$POINTERS"
labels=(); regexes=()
for p in "${pairs[@]}"; do labels+=("${p%%=*}"); regexes+=("${p#*=}"); done

printf '%-36s %-11s' "briefing" "last commit"
for l in "${labels[@]}"; do printf ' %-14s' "$l"; done
echo
missing_total=0; full=0; errors=0
for f in "${files[@]}"; do
    d=$(git log -1 --format=%cs -- "$f" 2>/dev/null)
    printf '%-36s %-11s' "${f##*/}" "${d:-untracked}"
    miss=0; row_err=$errors
    for r in "${regexes[@]}"; do
        grep -qiE "$r" "$f" 2>/dev/null; rc=$?
        # A grep error (a bad pattern) must not read as "missing" (m-44): count it and fail with 2.
        case $rc in
            0) printf ' %-14s' "yes" ;;
            1) printf ' %-14s' "-"; miss=$((miss + 1)) ;;
            *) printf ' %-14s' "ERROR"; errors=$((errors + 1)) ;;
        esac
    done
    echo
    missing_total=$((missing_total + miss))
    [ $miss -eq 0 ] && [ $errors -eq $row_err ] && full=$((full + 1))
done
echo "briefing-pointer-check: ${#files[@]} briefings read, ${#labels[@]} pointers each; $full carry all; $missing_total pointer gaps; $errors pattern errors"
[ $errors -gt 0 ] && exit 2
[ $missing_total -eq 0 ]
