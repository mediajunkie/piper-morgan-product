#!/usr/bin/env bash
# PPM criteria line: MVP open issues vs the order doc, plus open issues with no milestone.
# Prints counts with their denominators. Exit 0 = gap empty and 0 unmilestoned, 1 = something to place, 3 = could not measure.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 3
DOC=dev/active/mvp-epic-order-2026-09-09.md
[ -f "$DOC" ] || { echo "criteria-line: $DOC missing, NOT MEASURED"; exit 3; }
mvp=$(gh issue list --milestone MVP --state open --limit 500 --json number --jq '.[].number' 2>/dev/null | sort) || exit 3
all=$(gh issue list --state open --limit 500 --json number,milestone --jq '[.[]|select(.milestone==null)|.number]|sort|.[]' 2>/dev/null) || exit 3
total=$(gh issue list --state open --limit 500 --json number --jq 'length' 2>/dev/null) || exit 3
[ -n "$total" ] || exit 3
[ "$total" -ge 500 ] && echo "criteria-line: WARNING open issues hit the --limit 500 ceiling; counts below may be truncated"
mentioned=$(grep -oE '#[0-9]{4}' "$DOC" | tr -d '#' | sort -u)
n_mvp=$(printf '%s\n' "$mvp" | grep -c .)
gap=$(comm -23 <(printf '%s\n' "$mvp") <(printf '%s\n' "$mentioned") | tr '\n' ' ')
n_nomil=$(printf '%s\n' "$all" | grep -c .)
echo "criteria-line: $n_mvp open MVP of $total open; MVP issues not in the order doc: ${gap:-none}; open with no milestone: $n_nomil ${all:+($(echo $all | tr '\n' ' '))}"
[ -z "$gap" ] && [ "$n_nomil" -eq 0 ]
