#!/usr/bin/env bash
# deploy-mcp.sh — the one sanctioned way for an agent seat to deploy the MCP app (piper-morgan-mcp).
#
# Why a wrapper (CIO, 2026-10-13; xian's delegation: PA does the MCP deploys, #1982): PA's seat denies
# `fly deploy:*`, and deny beats allow, so no allow rule can carve one app out of it. A glob deny
# narrow enough to spare the MCP command would also spare a bare `fly deploy`, which reads fly.toml
# (production). So the deny stays for every direct `fly deploy`, and this script is the paved road:
#   - one target, fixed here: app piper-morgan-mcp from fly.mcp.toml, built remotely;
#   - no arguments except --dry-run (nothing can be appended to the fly command);
#   - only from a tree whose tracked content equals origin/main and that has no untracked,
#     non-ignored files (the remote build uploads the working tree, so stray files would ship);
#   - prints the sha it deploys and the latest releases afterwards, for the deploying seat's log.
# Permission rule on PA's seat (installed by Pard or xian): allow `Bash(scripts/deploy-mcp.sh)` and
# `Bash(scripts/deploy-mcp.sh --dry-run)`, exact strings. Limits, stated: like any script in this
# repo it is editable by any seat on the host, so it is a guard rail against accidents, not a
# control against a seat that means harm (prod-command-permissions.md, 2026-10-13).
# Review: 2026-11-24, or when an MCP deploy workflow exists (then retire this for `gh workflow run`).
set -euo pipefail
APP="piper-morgan-mcp"
CONFIG="fly.mcp.toml"
die() { echo "deploy-mcp: REFUSED: $*" >&2; exit 1; }

dry=0
case "$#:${1:-}" in
  0:) ;;
  1:--dry-run) dry=1 ;;
  *) die "takes no arguments except --dry-run (got: $*)" ;;
esac

top="$(git rev-parse --show-toplevel 2>/dev/null)" || die "not in a git checkout"
cd "$top"
[ -f "$CONFIG" ] || die "$CONFIG not found at $top"
grep -qx "app = \"$APP\"" "$CONFIG" || die "$CONFIG does not name app $APP"

git fetch -q origin main || die "could not fetch origin/main"
main_sha="$(git rev-parse origin/main)"
git diff --quiet origin/main -- || die "tracked files differ from origin/main ($(git diff --name-only origin/main -- | head -3 | tr '\n' ' ')...). Sync first."
git diff --cached --quiet origin/main -- || die "staged changes differ from origin/main"
stray="$(git ls-files --others --exclude-standard | head -5)"
[ -z "$stray" ] || die "untracked files would be uploaded to the build: $(echo "$stray" | tr '\n' ' ')"
# #2240: --exclude-standard skips gitignored files, and config/*.user.md is gitignored, so an
# operator overlay would have passed the guard above. .dockerignore now drops it from the context;
# refuse here too so the operator sees why, instead of a silent omission.
overlay="$(git ls-files --others --ignored --exclude-standard -- config/ | grep -E '\.user\.md$' | head -5 || true)"
[ -z "$overlay" ] || die "operator overlay in config/ would be excluded by .dockerignore; move it aside before deploying: $(echo "$overlay" | tr '\n' ' ')"

# The sha goes in as a build arg so the MCP /health names the deployed commit, as alpha's does (PA,
# 2026-10-16: it read "unknown" because nothing passed it). It is origin/main, checked above, not an input.
cmd=(fly deploy -c "$CONFIG" -a "$APP" --remote-only --build-arg "PIPER_GIT_SHA=$main_sha")
echo "deploy-mcp: content = origin/main ${main_sha:0:10}; command: ${cmd[*]}"
if [ "$dry" -eq 1 ]; then
  echo "deploy-mcp: dry run, nothing deployed"
  exit 0
fi
"${cmd[@]}"
echo "deploy-mcp: deployed origin/main ${main_sha:0:10} to $APP. Latest releases:"
fly releases -a "$APP" 2>/dev/null | head -4 || echo "deploy-mcp: (could not list releases)"
