#!/usr/bin/env bash
# push-main.sh — push HEAD to origin/main with fetch-merge-retry on races.
#
# Born from the 360 (2026-08-15): on busy days plain `git push origin
# HEAD:main` races other agents 3+ times/day; mail-send.sh auto-retries but
# code pushes didn't. Same discipline as mail-send v3: rebuild on the new tip,
# retry, bounded attempts, never force.
set -u
MAX=${MAX_RETRIES:-4}
for i in $(seq 1 "$MAX"); do
  if OUT=$(git push origin HEAD:main 2>&1); then
    echo "$OUT" | grep -E -- "->|up-to-date" | tail -1 || echo "pushed"
    exit 0
  fi
  if ! echo "$OUT" | grep -qiE "fetch first|fast-forward|cannot lock ref|behind"; then
    # not a race — surface the real error, do not retry blindly
    echo "$OUT" >&2
    exit 1
  fi
  echo "push race (attempt $i/$MAX) — fetching + merging origin/main…" >&2
  git fetch origin main || { echo "fetch failed" >&2; exit 1; }
  git merge --no-edit origin/main || {
    echo "merge conflict — resolve manually; NOT retrying" >&2
    exit 1
  }
done
echo "push failed after $MAX race retries" >&2
exit 1
