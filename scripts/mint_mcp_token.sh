#!/usr/bin/env bash
# mint_mcp_token.sh — mint an MCP server access token against PRODUCTION, narrowly.
#
# WHY THIS EXISTS (mirrors scripts/mint_prod_invite.sh, #1344's precedent):
# minting requires running code inside the prod container, and the only way
# to do that ad hoc is `fly ssh console -C "..."`. A permission rule broad
# enough to allow that is broad enough to run ANYTHING in production. This
# wrapper fixes the payload in git — reviewable, diffable — so the capability
# can be granted as one narrow rule (`Bash(scripts/mint_mcp_token.sh:*)`)
# instead of blanket remote-exec. The payload is scripts/mint_mcp_token.py,
# already in the image (Dockerfile `COPY . .` -> /app).
#
# ⚠️ Running scripts/mint_mcp_token.py directly from a worktree resolves the
# DEV database (localhost:5433) unless PIPER_ENVIRONMENT=production is set —
# see that script's _database_url() for the full guard. This wrapper exists
# so the prod-vs-dev target is impossible to get wrong.
#
# Trust-zone (#1462 condition 1): unlike an invite token, an MCP token is
# bound to an already-real user at mint time — this script (and the table
# behind it) never has an anonymous-owner path. Raw tokens are bearer
# credentials for that user's own data. NEVER paste one into a mailbox memo
# or any git-tracked file — deliver it the way an invite token is delivered
# (in-conversation or the gitignored roster, per PM ruling 2026-07-04).
#
# Usage:
#   scripts/mint_mcp_token.sh --user-email a@b.com --label "alpha tester"
#       # DRY RUN — shows the plan, generates and inserts nothing
#   scripts/mint_mcp_token.sh --user-email a@b.com --label "alpha tester" --apply
#       # mints exactly one token
#   scripts/mint_mcp_token.sh --user-email a@b.com --label "..." --expires-days 30 --apply
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: mint_mcp_token.sh --user-email you@example.com --label 'desc' [--expires-days N] [--apply]" >&2
  echo "   or: mint_mcp_token.sh --user-id <uuid> --label 'desc' [--expires-days N] [--apply]" >&2
  exit 2
fi

APPLY=0
for a in "$@"; do
  [ "$a" = "--apply" ] && APPLY=1
done

APP_DIR="/Users/xian/Development/piper-morgan-product"
cd "$APP_DIR" || { echo "mint_mcp_token: $APP_DIR not found" >&2; exit 2; }

if [ "$APPLY" -eq 0 ]; then
  echo "DRY RUN — would mint an MCP access token with: $*"
  echo "Re-run with the same args plus --apply to actually insert. Nothing was generated."
  exit 0
fi

# Build a safely-quoted argument string for the remote /bin/sh -c invocation.
# `fly ssh console -C` fork/execs the command DIRECTLY — there is no shell,
# so passing args unquoted would let a shell-meaningful character (spaces in
# --label especially) break the remote parse. See mint_prod_invite.sh for the
# fuller explanation of why the explicit /bin/sh -c wrapper is required at all
# (PYTHONPATH=/app as a bare prefix has no shell to interpret the assignment).
QUOTED_ARGS=""
for a in "$@"; do
  QUOTED_ARGS="$QUOTED_ARGS $(printf '%q' "$a")"
done

exec fly ssh console -C "/bin/sh -c 'cd /app && PYTHONPATH=/app python scripts/mint_mcp_token.py$QUOTED_ARGS'"
