#!/usr/bin/env bash
# mint_prod_invite.sh — mint alpha invite tokens against PRODUCTION, narrowly.
#
# WHY THIS EXISTS (2026-09-13, Lead): minting requires running code inside the
# prod container, and the only way to do that ad hoc is `fly ssh console -C
# "python -c '<payload>'"`. A permission rule broad enough to allow that is
# broad enough to run ANYTHING in production. This script fixes the payload in
# git — reviewable, diffable, unchanging — so the capability can be granted as
# one narrow rule (`Bash(scripts/mint_prod_invite.sh:*)`) instead of blanket
# remote-exec. The payload it runs is scripts/mint_invite_tokens.py, which is
# already in the image (Dockerfile `COPY . .` → /app).
#
# ⚠️ The sibling script scripts/mint_invite_tokens.py defaults to LOCALHOST:5433
# (the DEV database) and loads a .env path that does not exist on any current
# seat. Running it from a worktree mints a token the alpha tester cannot use,
# and it fails SILENTLY — it looks exactly like success. This wrapper exists
# partly to make the prod-vs-dev target impossible to get wrong.
#
# Trust-zone split (#1344, ratified 2026-07-03): Lead mints and validates;
# HOST owns the identity/roster mapping; PM sends the invite. This script knows
# nothing about identities — only tokens.
#
# Usage:
#   scripts/mint_prod_invite.sh            # DRY RUN — generates nothing, shows the plan
#   scripts/mint_prod_invite.sh --apply    # mint exactly ONE token into prod
#   scripts/mint_prod_invite.sh --apply 3  # mint three
#
# Raw tokens are account-creation credentials. NEVER paste one into a mailbox
# memo or any git-tracked file (PM ruling, 2026-07-04) — the gitignored roster
# at dev/alpha/alpha-tester-roster.md is where they live.
set -euo pipefail

APPLY=0
COUNT=1
for a in "$@"; do
  case "$a" in
    --apply) APPLY=1 ;;
    ''|*[!0-9]*) echo "mint_prod_invite: unrecognized argument '$a'" >&2; exit 2 ;;
    *) COUNT="$a" ;;
  esac
done

if [ "$COUNT" -lt 1 ] || [ "$COUNT" -gt 20 ]; then
  echo "mint_prod_invite: refusing count=$COUNT (allowed 1..20)" >&2
  exit 2
fi

APP_DIR="/Users/xian/Development/piper-morgan-product"
cd "$APP_DIR" || { echo "mint_prod_invite: $APP_DIR not found" >&2; exit 2; }

if [ "$APPLY" -eq 0 ]; then
  echo "DRY RUN — would mint $COUNT token(s) into PRODUCTION invite_tokens."
  echo "Re-run with --apply to actually insert. Nothing was generated."
  exit 0
fi

# The payload is the committed script, run inside the prod container so it
# resolves the real database URL from the app's own config (never from a
# worktree's env). --apply is passed through deliberately and explicitly.
#
# PYTHONPATH=/app is load-bearing: invoking `python /app/scripts/foo.py` puts
# /app/scripts on sys.path, NOT /app, so `from services.…` raises
# ModuleNotFoundError. Verified locally (the same invocation fails without it)
# rather than assumed — this is the kind of thing that only surfaces at the
# moment you need the command to work.
#
# And `fly ssh console -C` fork/execs the command DIRECTLY — there is no shell,
# so a bare `VAR=x cmd` prefix is parsed as a binary named "VAR=x"
# ("fork/exec PYTHONPATH=/app: no such file or directory"). The explicit
# /bin/sh -c is what gives the assignment a shell to be interpreted by.
exec fly ssh console -C "/bin/sh -c 'cd /app && PYTHONPATH=/app python scripts/mint_invite_tokens.py $COUNT --apply'"
