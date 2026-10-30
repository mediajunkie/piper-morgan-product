#!/usr/bin/env bash
# mail-send-external.sh — deliver one memo to an agent whose inbox is in another of xian's repos (Janus, Pard, …).
#
# 10-20 (CIO): the hand-built cross-repo delivery (mailboxes/DIRECTORY.md, "Mail to an agent outside this repo")
# bypassed every check mail-send.sh runs. That day a memo reached Janus with a guessed `date:` 7 minutes ahead of the
# clock; only the later local send caught it (methodology-53: a chokepoint covers only what passes through it). The
# hand ritual also kept failing on zsh (`$C:refs` read as a modifier, 10-19). This script is that ritual with the
# checks in it, so the easy path is the checked one.
#
#   scripts/mail-send-external.sh <repo-path> <mail-dir-in-repo> <memo-file> [commit message]
#   e.g. scripts/mail-send-external.sh ~/Development/designinproduct docs/mail mailboxes/cio/sent/<name>.md
#
# Steps: stamp check (refuses on a date: that isn't a clock reading), bearer lint, then a commit built on the
# recipient's fresh origin/main with a scratch index (the recipient checkout's working tree and index are never
# touched), push to main (up to 3 tries, rebuilt from a fresh fetch each time), and a check that the exact blob is on
# origin/main. The file lands as <mail-dir>/<basename of memo-file>. Mirror it into your own sent/ as usual.
#
# Cost:    one fetch and one push per memo
# Benefit: the stamp and bearer checks on sibling-repo mail, which had none
# Review:  2026-12-14
# Owner:   CIO
# Concept: mailboxes/DIRECTORY.md
set -euo pipefail

if [ $# -lt 3 ]; then
  sed -n '12,13p' "$0" >&2
  exit 2
fi
DEST_REPO=$1
DEST_DIR=${2%/}
MEMO=$3
REPO=$(cd "$(dirname "$0")/.." && pwd)
NAME=$(basename "$MEMO")
MSG=${4:-"mail: ${NAME%.md}"}

[ -f "$MEMO" ] || { echo "mail-send-external: ⛔ no such file: $MEMO" >&2; exit 1; }
MEMO=$(cd "$(dirname "$MEMO")" && pwd)/$NAME  # absolute: the git calls below run inside the recipient repo
git -C "$DEST_REPO" rev-parse --git-dir >/dev/null 2>&1 || { echo "mail-send-external: ⛔ not a git repo: $DEST_REPO" >&2; exit 1; }
grep -q '^reply-to:' "$MEMO" || { echo "mail-send-external: ⛔ $MEMO has no reply-to: line" >&2; exit 1; }

set +e
python3 "$REPO/scripts/stamp_check.py" --stamp-now "$MEMO"  # `date: now` becomes the clock (10-30); copy cc's after
python3 "$REPO/scripts/stamp_check.py" --mail "$MEMO"
rc=$?
set -e
if [ "$rc" -eq 1 ]; then
  echo "mail-send-external: ⛔ REFUSING — a date: above isn't a clock reading. Run TZ=America/Los_Angeles date, fix it, re-run. Nothing was sent." >&2
  exit 1
elif [ "$rc" -ne 0 ]; then
  echo "mail-send-external: ⚠ the stamp check didn't run (rc $rc); dates NOT checked" >&2
fi

python3 "$REPO/scripts/mailbox_bearer_lint.py" --files "$MEMO" >&2 || {
  echo "mail-send-external: ⛔ REFUSING — bearer lint failed on $MEMO. Nothing was sent." >&2
  exit 1
}

TRAILERS=$("$REPO/scripts/session_trailers.sh" || true)  # derived attribution (10-30); warns, never guesses
IDX=$(mktemp "${TMPDIR:-/tmp}/mail-send-external.XXXXXX")
trap 'rm -f "${IDX:?}"' EXIT
BLOB=$(git -C "$DEST_REPO" hash-object -w "$MEMO")
for i in 1 2 3; do
  git -C "$DEST_REPO" fetch -q origin main
  PARENT=$(git -C "$DEST_REPO" rev-parse origin/main)
  GIT_INDEX_FILE=$IDX git -C "$DEST_REPO" read-tree "$PARENT"
  GIT_INDEX_FILE=$IDX git -C "$DEST_REPO" update-index --add --cacheinfo "100644,${BLOB},${DEST_DIR}/${NAME}"
  TREE=$(GIT_INDEX_FILE=$IDX git -C "$DEST_REPO" write-tree)
  [ -n "$TREE" ] && [ -n "$PARENT" ] || { echo "mail-send-external: ⛔ empty tree or parent hash; nothing pushed" >&2; exit 1; }
  COMMIT=$(git -C "$DEST_REPO" commit-tree "$TREE" -p "$PARENT" -m "$MSG" ${TRAILERS:+-m "$TRAILERS"})
  if git -C "$DEST_REPO" push -q origin "${COMMIT}:refs/heads/main" 2>/dev/null; then
    git -C "$DEST_REPO" fetch -q origin main
    if [ "$(git -C "$DEST_REPO" rev-parse "origin/main:${DEST_DIR}/${NAME}" 2>/dev/null)" = "$BLOB" ]; then
      echo "mail-send-external: landed ${COMMIT:0:10} → $(basename "$DEST_REPO") origin/main:${DEST_DIR}/${NAME} ✓"
      exit 0
    fi
    echo "mail-send-external: ⛔ pushed ${COMMIT:0:10} but the blob is not on origin/main; check by hand" >&2
    exit 1
  fi
  echo "mail-send-external: push attempt $i rejected; rebuilding on a fresh origin/main" >&2
done
echo "mail-send-external: ⛔ 3 pushes rejected; nothing landed" >&2
exit 1
