#!/usr/bin/env bash
# check-deploy-trigger-parity.sh — assert fly-deploy.yml's paths-ignore still mirrors .dockerignore.
#
# WHY. Arch's ruling 2026-10-01: the deploy trigger may skip a push only when that push cannot change
# the image, and `.dockerignore` IS the definition of what reaches the image. So `paths-ignore` mirrors
# `.dockerignore` and nothing else. Two hand-maintained lists that must agree will drift; Arch's point
# 5 was to make the agreement checkable rather than remembered.
#
# THE TRAP THIS EXISTS TO PREVENT, measured before the trigger was changed: between staging's sha and
# origin/main one morning, 224 files changed. 179 were image-neutral. The other 45 were ALL `docs/` --
# and `docs/` is deliberately NOT in `.dockerignore`, because services/domain/pm_number_manager.py
# reads `docs/planning/*` AT RUNTIME. Ignoring docs/ would let staging serve stale runtime files behind
# a plausible sha. "Non-code" is not the same category as "not in the image", and only .dockerignore
# knows the difference.
#
# Exit 0 = the two agree. Exit 1 = they have drifted, naming which way.

set -u
cd "$(dirname "$0")/.." || exit 2
WF=".github/workflows/fly-deploy.yml"
DI=".dockerignore"
[ -f "$WF" ] || { echo "deploy-trigger-parity: UNMEASURABLE — $WF not found"; exit 2; }
[ -f "$DI" ] || { echo "deploy-trigger-parity: UNMEASURABLE — $DI not found"; exit 2; }

# Expected paths-ignore, derived from .dockerignore. Two deliberate departures from a literal mirror,
# both because the file's EFFECT differs from its CONTENTS:
#   * `.dockerignore` itself is excluded. It is not copied into the image, but CHANGING it changes
#     which other files are -- so a push touching it must still deploy.
#   * `.git` is dropped. It never appears in a commit's changed-file list, so a pattern for it would
#     be dead weight rather than wrong.
# awk, not sed: BSD sed rejects `t` with a following command on the same line, and the first version
# of this died with "undefined label" rather than producing a wrong answer -- loud, which is the right
# failure, but worth not repeating. A leading-glob pattern like `*.log` becomes `**/*.log`; everything
# else is a directory and becomes `<dir>/**`.
expected="$(grep -vE '^\s*#|^\s*$' "$DI" \
  | grep -vxE '\.dockerignore|\.git' \
  | awk '{ sub(/\/$/,""); if (substr($0,1,1)=="*") print "**/" $0; else print $0 "/**" }' \
  | sort -u)"

actual="$(awk '/paths-ignore:/{f=1;next} f&&/^[[:space:]]*-/{gsub(/^[[:space:]]*-[[:space:]]*/,"");gsub(/['"'"'"]/,"");print;next} f{exit}' "$WF" | sort -u)"

if [ "$expected" = "$actual" ]; then
  echo "deploy-trigger-parity: OK — paths-ignore mirrors .dockerignore ($(printf '%s' "$actual" | grep -c . ) patterns)"
  exit 0
fi

echo "deploy-trigger-parity: DRIFT — fly-deploy.yml's paths-ignore no longer mirrors .dockerignore."
echo "  in .dockerignore but NOT ignored by the trigger (these pushes build an identical image for nothing):"
comm -23 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") | sed 's/^/    /'
echo "  ignored by the trigger but NOT in .dockerignore (DANGEROUS — these pushes CAN change the image):"
comm -13 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") | sed 's/^/    /'
echo "  Fix one list or the other. The second group is the one that can ship a stale image behind a"
echo "  plausible sha, which is what Arch's ruling exists to prevent."
exit 1
