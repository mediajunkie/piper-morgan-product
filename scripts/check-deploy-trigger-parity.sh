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
# TWO DIRECTIONS, NOT ONE (issue 2369; CIO's placement and Arch's ruling, 2026-11-13):
#   * DANGEROUS: a pattern the trigger ignores that is NOT in .dockerignore. Such a push can change
#     the image and would not deploy. Always exit 1. Never exempted.
#   * HARMLESS: a .dockerignore row the trigger does not ignore. Such a push builds an identical
#     image for nothing. Printed as a warning, exit 0; with --strict, exit 1.
#   * EXEMPT (harmless direction only): a .dockerignore row that matches no tracked file AND that
#     .gitignore ignores. A push cannot change a path git does not track, so a paths-ignore row for it
#     would never fire (the reason `.git` is dropped below). Derived at run time from `git ls-files`
#     and `git check-ignore`, never from a hand list, and reported by name. If someone force-adds a
#     file under such a path the exemption lapses by itself and the row is reported as harmless.
#
# Exit 0 = no dangerous drift (and, with --strict, no harmless drift either). Exit 1 = drift, naming
# which way. Exit 2 = could not measure.

set -u
STRICT=0
for arg in "$@"; do
  case "$arg" in
    --strict) STRICT=1 ;;
    *) echo "deploy-trigger-parity: unknown argument '$arg' (only --strict)"; exit 2 ;;
  esac
done
cd "$(dirname "$0")/.." || exit 2
WF=".github/workflows/fly-deploy.yml"
DI=".dockerignore"
[ -f "$WF" ] || { echo "deploy-trigger-parity: UNMEASURABLE — $WF not found"; exit 2; }
[ -f "$DI" ] || { echo "deploy-trigger-parity: UNMEASURABLE — $DI not found"; exit 2; }

# One .dockerignore row -> the paths-ignore pattern that mirrors it. Two deliberate departures from a
# literal mirror, both because the file's EFFECT differs from its CONTENTS:
#   * `.dockerignore` itself is excluded. It is not copied into the image, but CHANGING it changes
#     which other files are -- so a push touching it must still deploy.
#   * `.git` is dropped. It never appears in a commit's changed-file list, so a pattern for it would
#     be dead weight rather than wrong.
# The mapping (Arch, 2369; CIO found the old one turned every row without a leading `*` into
# `<row>/**`, so the file glob `config/*.user.md` was expected as `config/*.user.md/**`, which
# matches nothing):
#   * a row starting with `*` (`*.log`) is a file glob anywhere       -> `**/<row>`
#   * a row ending in `/` (`dev/`) is a directory                     -> `<dir>/**`
#   * any other row holding a glob character (`config/*.user.md`)     -> itself, a file glob
#   * a bare name (`.github`) is a directory                          -> `<name>/**`
# awk, not sed: BSD sed rejects `t` with a following command on the same line.
map_row() {
  awk '{
    if (substr($0,1,1)=="*") { print "**/" $0; next }
    if ($0 ~ /\/$/) { sub(/\/$/,""); print $0 "/**"; next }
    if ($0 ~ /[*?\[]/) { print; next }
    print $0 "/**"
  }'
}
rows="$(grep -vE '^[[:space:]]*#|^[[:space:]]*$' "$DI" | grep -vxE '\.dockerignore|\.git')"
expected="$(printf '%s\n' "$rows" | map_row | sort -u)"

actual="$(awk '/paths-ignore:/{f=1;next} f&&/^[[:space:]]*-/{gsub(/^[[:space:]]*-[[:space:]]*/,"");gsub(/['"'"'"]/,"");print;next} f{exit}' "$WF" | sort -u)"

dangerous="$(comm -13 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") | grep . || true)"
missing="$(comm -23 <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") | grep . || true)"

# Harmless direction only: split the missing rows into exempt (untracked AND gitignored) and not.
# The probe is a path the row would match (`*` -> a name, a directory -> a file inside it), because
# `git check-ignore` answers for a path, not for a pattern.
exempt=""; harmless=""
if [ -n "$missing" ]; then
  in_git=0
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 && in_git=1
  while IFS= read -r row; do
    [ -n "$row" ] || continue
    pat="$(printf '%s\n' "$row" | map_row)"
    grep -qxF "$pat" <<<"$missing" || continue
    is_exempt=0
    if [ "$in_git" -eq 1 ]; then
      spec="${row%/}"
      tracked="$(git ls-files -- "$spec" | head -1)"
      probe="${spec//\*/parity-probe}"
      case "$row" in
        */) probe="$probe/parity-probe" ;;
        *[*?[]*) : ;;
        *) probe="$probe/parity-probe" ;;
      esac
      if [ -z "$tracked" ] && git check-ignore -q -- "$probe" 2>/dev/null; then is_exempt=1; fi
    fi
    if [ "$is_exempt" -eq 1 ]; then exempt="${exempt}${pat}"$'\n'; else harmless="${harmless}${pat}"$'\n'; fi
  done <<<"$rows"
fi
exempt="$(printf '%s' "$exempt" | grep . | sort -u || true)"
harmless="$(printf '%s' "$harmless" | grep . | sort -u || true)"

n_actual="$(printf '%s' "$actual" | grep -c . || true)"
if [ -n "$exempt" ]; then
  echo "deploy-trigger-parity: exempt — in .dockerignore, not in paths-ignore, and that is right: git tracks"
  echo "  no file under them and .gitignore ignores them, so no push can change them:"
  printf '%s\n' "$exempt" | sed 's/^/    /'
fi

if [ -z "$dangerous" ] && [ -z "$harmless" ]; then
  echo "deploy-trigger-parity: OK — paths-ignore mirrors .dockerignore (${n_actual} patterns, $(printf '%s' "$exempt" | grep -c . || true) exempt)"
  exit 0
fi

if [ -n "$harmless" ]; then
  echo "deploy-trigger-parity: WARNING — in .dockerignore but NOT ignored by the trigger (these pushes build"
  echo "  an identical image for nothing):"
  printf '%s\n' "$harmless" | sed 's/^/    /'
fi
if [ -n "$dangerous" ]; then
  echo "deploy-trigger-parity: DRIFT — ignored by the trigger but NOT in .dockerignore (DANGEROUS — these"
  echo "  pushes CAN change the image and would not deploy):"
  printf '%s\n' "$dangerous" | sed 's/^/    /'
  echo "  Fix one list or the other. This is the group that can ship a stale image behind a plausible"
  echo "  sha, which is what Arch's ruling exists to prevent."
  exit 1
fi
if [ "$STRICT" -eq 1 ]; then
  echo "deploy-trigger-parity: DRIFT (--strict) — the harmless rows above count as drift."
  exit 1
fi
echo "deploy-trigger-parity: OK with warnings — nothing dangerous (${n_actual} patterns)."
exit 0
